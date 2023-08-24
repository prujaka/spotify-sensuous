import streamlit as st
import numpy as np
import pandas as pd
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Define your Spotify API credentials
client_id = st.secrets['CLIENT_ID']
client_secret = st.secrets['CLIENT_SECRET']
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Define the URL of your FastAPI application
fastapi_url = "https://sensuous-kxfwockblq-ew.a.run.app"

st.set_page_config(page_title="Song Explorer", page_icon=":musical_note:")

# App title
st.title("""Song Explorer :rocket:: _Discover Similar Songs Based on 
Your Favorites_""")


# Add vinyl record image to header
st.image("img/image.jpg")

st.markdown(""" Just pop your favorite song into our machine learning tool, and let us take care of the rest!
            We'll analyze the song's spectrogram and suggest other tracks that match your style, making it super easy to discover new music that you're bound to love! :hearts:
""")


def predict_playlist(song, artist):
    # Make a request to FastAPI
    response = requests.get(fastapi_url + "/predict", params={"song": song, "artist": artist})

    # Return the prediction result
    return response.json()['playlist']


def main():
    # Header 2
    st.markdown("### Enter a song here :musical_note:")

    # Input song
    song = str(st.text_input('You can write the title of your favorite song here, but make sure you spell it right :eyes:'))

    # Header 2
    st.markdown("### Enter an artist here :singer:")

    # Input artist
    artist = str(st.text_input('You can write the artist of your favorite song here, but make sure you spell it right :eyes:'))

    # Display appropriate message
    if song == '' or artist == '':
        pass  # don't display any message if input is empty
    else:
        try:
            playlist = predict_playlist(song, artist)
            st.write(f"We will be happy to make suggestions based on your choice: {song} by {artist}")
            st.markdown("### Our ML model suggests the following songs :raised_hands::")
            for index, item in enumerate(playlist):
                # Retrieve the song's audio preview URL using the Spotify API
                track_results = sp.search(q=f"{item[0]} {item[1]}", type='track', limit=1)
                if len(track_results['tracks']['items']) > 0:
                    preview_url = track_results['tracks']['items'][0]['preview_url']
                else:
                    preview_url = ''

                # Display the song information and an audio player
                st.write(f"**{index + 1}.** {item[0]}\n by {item[1]}\n")
                if preview_url:
                    st.audio(preview_url, format='audio/mp3')
                st.write('---')
            st.write(":musical_note: Enjoy your playlist! :musical_note:", unsafe_allow_html=True)
        except:
            st.write(":rotating_light: Oops! Something went wrong. Please make sure you spelled the song and artist names correctly and try again.")

if __name__ == "__main__":
    main()
