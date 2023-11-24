from sensuous.model.knn import predict_playlist_csv
from fastapi import FastAPI

api = FastAPI()

@api.get("/")
def index():
    return {"status": "API connected"}

@api.get("/predict")
def predict(artist: str, song: str):
    return predict_playlist_csv(artist, song)
