from sensuous.model.knn import predict_playlist_csv
from fastapi import FastAPI

api = FastAPI()


@api.get("/")
def index():
    """Displays welcome message when API is connected"""
    return {"status": "API connected"}


@api.get("/predict")
def predict(artist: str, song: str):
    """Predicts the playlist based on the user's input"""
    return predict_playlist_csv(artist, song)
