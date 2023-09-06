# Standard image which has python installed
FROM python:3.8.6-buster

# Api_folder and the requiremenets.txt file
COPY sensuous sensuous
COPY data data
COPY setup.py setup.py
COPY requirements.txt requirements.txt

# Upgrading pip and install the libraries in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install .

COPY Makefile Makefile

# install cv2 dependencies
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

# local
# CMD uvicorn sensuous.api.api_fast:api --host 0.0.0.0

# deploy to gcp
CMD uvicorn sensuous.api.api_fast:api --host 0.0.0.0 --port $PORT
