# This script has originally been written by Linda Sadrijaj
# Modified and adapted by Sergey Tkachenko
import streamlit as st
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

API_TYPE = 'local'
API_URL_LOCAL = 'http://0.0.0.0:8000'


def predict_playlist(artist, song, url):
    response = requests.get(f'{url}/predict', params={'artist': artist,
                                                      'song': song})
    return response.json()['playlist']


def main():
    # Define your Spotify API credentials
    client_id = st.secrets['CLIENT_ID']
    client_secret = st.secrets['CLIENT_SECRET']
    client_credentials_manager = SpotifyClientCredentials(client_id,
                                                          client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Define the URL of your FastAPI application
    if API_TYPE == 'local':
        fastapi_url = API_URL_LOCAL
    elif API_TYPE == 'cloud':
        fastapi_url = st.secrets['API_URL_CLOUD']
    else:
        raise Exception("API type unknown. Should be 'cloud' or 'local'")

    st.set_page_config(page_title='Sensuous Rec. System',
                       page_icon=':musical_note:')

    # App title
    st.title("Sensuous Recommendation System for Spotify")

    # Add vinyl record image to header
    st.image('img/sensuous-pic.jpg')

    st.markdown(
        "Simply input your cherished song into our tool, and we'll handle"
        " the rest! Our system will analyze the unique features of the track"
        " and recommend other songs that align with its style, using"
        " the audio profile. Explore new music effortlessly, discovering"
        " tunes that are sure to resonate with your preferences!")

    st.markdown("### Enter an artist here")
    artist = str(st.text_input("Please enter the artist's name exactly as"
                               " it is. In the case of multiple artists,"
                               " simply input one of them."))

    st.markdown("### Enter a song here")
    song = str(st.text_input("Please enter the song title exactly as it is."))

    if song == '' or artist == '':
        print("Empty artist or song name. Please enter the full search query.")
    else:
        playlist = predict_playlist(artist, song, url=fastapi_url)
        st.write(f"We will be happy to make suggestions based "
                 f"on your choice: {song} by {artist}")
        st.markdown("### Our ML model suggests the following songs:")
        for index, item in enumerate(playlist):
            # Retrieve the song's audio preview URL using the Spotify API
            results = sp.search(q=f"{item['artist']} {item['song']}",
                                type='track', limit=1)
            if len(results['tracks']['items']) > 0:
                preview_url = results['tracks']['items'][0]['preview_url']
            else:
                preview_url = ''

            # Display the song information and an audio player
            st.write(f"**{index + 1}.** {item['artist']}\n by {item['song']}\n")
            if preview_url:
                st.audio(preview_url, format='audio/mp3')
            st.write('---')
        st.write("Enjoy your playlist!", unsafe_allow_html=True)


if __name__ == '__main__':
    main()
