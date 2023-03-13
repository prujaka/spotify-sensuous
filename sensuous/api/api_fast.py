import pandas as pd

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
def predict(song: str, 
            artist: str,
            n_neighbors=10):
    return predict_playlist(song, artist, n_neighbors)