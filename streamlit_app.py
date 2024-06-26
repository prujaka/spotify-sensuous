# This script has originally been written by Linda Sadrijaj
# Modified and adapted by Sergey Tkachenko
import argparse
import pandas as pd
import requests
import spotipy
import streamlit as st
from spotipy.oauth2 import SpotifyClientCredentials
from sensuous.preprocessing.prepcsv import semicolonize


def api_predict_request(artist, song, url):
    response = requests.get(f'{url}/predict', params={'artist': artist,
                                                      'song': song})
    return response.json()


def output_message(request_code):
    if request_code == 0:
        return "### Sorry, no match to the user's input in our database." \
               "\n#### Also, you've been rickrolled:"

    if request_code == 1:
        return "### Several songs found from the user's input. " \
               "Take a listen and choose one of them as your input."

    if request_code == 2:
        return "### Our ML model suggests the following songs:"


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--api-url', default=st.secrets['API_URL_CLOUD'])
    args = parser.parse_args()
    fastapi_url = vars(args)['api_url']

    # Define your Spotify API credentials
    client_id = st.secrets['CLIENT_ID']
    client_secret = st.secrets['CLIENT_SECRET']
    client_credentials_manager = SpotifyClientCredentials(client_id,
                                                          client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Read the csv data and form sample suggestions
    df = pd.read_csv('data/all-songs.csv')
    df_suggestions = df[['artists', 'song_title']].sample(10).reset_index()
    df_suggestions = df_suggestions.drop('index', axis=1)
    df_suggestions['artists'] = df_suggestions['artists'].map(semicolonize)

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

    st.markdown(f"Our database currently contains {len(df)} songs."
                f" Here are some suggestions:")
    st.table(df_suggestions)

    with st.form(key='artist_song_form'):
        st.markdown("### Enter an artist here")
        artist = str(st.text_input("Please enter the artist's name exactly as"
                                   " it is. In the case of multiple artists,"
                                   " simply input one of them."))

        st.markdown("### Enter a song here")
        song = str(st.text_input("Please enter the song title exactly as"
                                 " it is."))
        submit_button = st.form_submit_button(label='Submit')

    if song.strip() == '' or artist.strip() == '':
        st.write("Empty artist or song name."
                 " Please enter the search query.")
    else:
        request = api_predict_request(artist, song, url=fastapi_url)
        playlist = request['playlist']

        message = output_message(request['code'])
        st.markdown(message)

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
