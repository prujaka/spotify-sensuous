from fastapi import FastAPI

api = FastAPI()

# root
@api.get("/")
def index():
    return {"status": "API connected"}

# here we put our first model: for now it just returns the song
@api.get("/predict")
def predict(song):
    return {'song recommendation': song}