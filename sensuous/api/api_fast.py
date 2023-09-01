from sensuous.model.knn import predict_playlist_lewagon
from fastapi import FastAPI

# TODO: output a link to docs and to test prediction?

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
            artist: str):
    return predict_playlist_lewagon(song, artist)
