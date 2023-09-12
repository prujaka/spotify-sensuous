import os

# If 'local', then the API link would be API_URL_LOCAL. Otherwise, it will
# be read from .streamlit/secrets.toml
# API_TYPE = 'local'
API_TYPE = 'cloud'

API_URL_LOCAL = "http://0.0.0.0:8000"

LOCAL_MP3_DIR = os.environ.get("LOCAL_MP3_DIR")
LOCAL_PNG_DIR = os.environ.get("LOCAL_PNG_DIR")
LOCAL_CSV_PATH = os.environ.get("LOCAL_CSV_PATH")
