import pandas as pd
import scipy as sp
from sklearn.preprocessing import MinMaxScaler

from sensuous.ml_logic.model import strip_artists
from sensuous.ml_logic.model import predict_playlist

from fastapi import FastAPI

api = FastAPI()

# root
@api.get("/")
def index():
    return {"status": "API connected"}

# dummy predict endpoint
@api.get("/dummy")
def dummy(song):
    return {'song recommendation': song}

# first model for predicting the 10 nearest songs
@api.get("/predict")
def predict(song, artist, n_neighbors=10):
    df = pd.read_csv('data/lewagon-spotify-data.csv')
    df = df.drop(['popularity'], axis=1)
    df_numeric = df.drop(columns=['name', 'artists'])
    columns = df_numeric.columns.values.tolist()
    df_scaler = MinMaxScaler()
    df[columns] = df_scaler.fit_transform(df[columns])

    # Seed song selection
    artists_formatted = f"['{artist}']"
    seed_song = df[(df['name'] == song) & (df['artists'] == artists_formatted)]

    if seed_song.shape[0] == 0:
        print("No such a song in the dataset. Returning the user's entry.")
        return f'{song} by {artist}'

    # Feature "preprocessing"
    seed_song_features = seed_song.select_dtypes(exclude='object')
    X = df.select_dtypes(exclude='object')

    # List of closest neighbors to the seed song
    tree = sp.spatial.KDTree(X.to_numpy())
    distances, indeces = tree.query([seed_song_features], k=n_neighbors)
    indeces = indeces.flatten()
    neighbors_df = df.loc[list(indeces)]
    songs = neighbors_df['name'].tolist()
    artists = [
        strip_artists(artist) for artist in neighbors_df['artists'].tolist()
    ]
    return dict(zip(songs, artists))

