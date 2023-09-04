import os

LOCAL_MP3_DIR = os.environ.get("LOCAL_MP3_DIR")
LOCAL_PNG_DIR = os.environ.get("LOCAL_PNG_DIR")
LOCAL_CSV_PATH = os.environ.get("LOCAL_CSV_PATH")

API_TYPE = os.environ.get("API_TYPE")
API_URL_LOCAL = os.environ.get("API_URL_LOCAL")
API_URL_CLOUD = os.environ.get("API_URL_GCR")

if __name__ == '__main__':
    print(f'LOCAL_MP3_DIR = {LOCAL_MP3_DIR}')
    print(f'LOCAL_PNG_DIR = {LOCAL_PNG_DIR}')
    print(f'LOCAL_CSV_PATH = {LOCAL_CSV_PATH}')
    print(f'API_TYPE = {API_TYPE}')
    print(f'API_URL_LOCAL = {API_URL_LOCAL}')
    print(f'API_URL_CLOUD = {API_URL_CLOUD}')
