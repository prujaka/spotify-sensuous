# spotify-sensuous

Welcome to Sensuous Recommendation System for Spotify!
This is a prototype of a recommendation system which proposes you a song radio
based solely on the audio features of the track.
No collaborative filtering or listening history, only the pure sound.
Powered by a custom API built with FastAPI and a user interface
crafted with Streamlit.

## Getting started
Install the python package of the project by running the following command:
```zsh
pip install -r requirements.txt
```

First of all, you'll need your Spotify Client ID and Client Secret.
[This Spotify Web API page](https://developer.spotify.com/documentation/web-api/concepts/apps)
will guide you how to get them. Once you have got your secrets,
create a `secrets.toml` script in the `.streamlit` directory:
```zsh
mkdir .streamlit
cd .streamlit
touch secrets.toml
```

Then, put your secrets between the double quotation marks in the following
commands and run them:
```zsh
echo 'CLIENT_ID = "YOUR_CLIENT_ID"' >> secrets.toml
echo 'CLIENT_SECRET = "YOUR_CLIENT_SECRET"' >> secrets.toml
```

Run the API locally on your machine:
```zsh
make run_local_api
```

Then, run the Streamlit local server on your machine:
```zsh
streamlit run streamlit_app.py
```
and see further instructions on the web page that opens.

## API
If you don't wish to use the web interface, you can access the API directly
by the link http://0.0.0.0:8000 and use the `/predict` endpoint:
```
http://0.0.0.0:8000/predict?{artist}&{song}
```
For example, if you want to make a radio playlist for the song White Christmas
by Frank Sinatra, you would use the following link:
```
http://0.0.0.0:8000/predict?artist=Frank%20Sinatra&song=White%20Christmas
```

Otherwise, open the `/docs` endpoint via http://0.0.0.0:8000/docs and use the
API more interactively. Just press the "Try it out" button of the
`GET/predict` endpoint on the opened page and type in your query.
