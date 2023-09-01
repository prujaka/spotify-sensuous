import os
import numpy as np
import pandas as pd
import cv2
import librosa
from skimage.io import imsave
from skimage.transform import resize
from sensuous.parameters import *


def semicolonize(s: str) -> str:
    """Strip a list-looking string s from brackets and single quotes
    and put a semicolon as a separator instead"""
    return ';'.join(s.strip("[]'").split("', '"))


def listify(s: str) -> str:
    """Remove a semicolon as a separator of a string s and format it as
    a list-looking string"""
    s = s.split(';')
    return str(s)


def preprocess_csv_data() -> None:
    df_lewagon_init = pd.read_csv('../data/lewagon-spotify-data.csv')
    df_georg_init = pd.read_csv('../data/data-georgemcintire.csv')
    df_mahar_init = pd.read_csv('../data/data-maharshipandya.csv')
    df_tom_init = pd.read_csv('../data/data-tomigelo-2019-04.csv')

    dfs_init = [df_lewagon_init, df_georg_init, df_mahar_init, df_tom_init]
    columns_common_set = set.intersection(
        *list(map(lambda df: set(df.columns), dfs_init)))
    audio_features = sorted(list(columns_common_set))
    columns = ['artists', 'song_title'] + audio_features

    df_lewagon = df_lewagon_init.copy()
    df_georg = df_georg_init.copy()
    df_mahar = df_mahar_init.copy()
    df_tom = df_tom_init.copy()

    df_lewagon['artists'] = df_lewagon['artists'].map(semicolonize)
    df_lewagon = df_lewagon.rename(columns={'name': 'song_title'})
    df_georg = df_georg.rename(columns={'artist': 'artists'})
    df_mahar = df_mahar.rename(columns={'track_name': 'song_title'})
    df_tom = df_tom.rename(
        columns={'track_name': 'song_title', 'artist_name': 'artists'})

    df_lewagon = df_lewagon[columns]
    df_georg = df_georg[columns]
    df_mahar = df_mahar[columns]
    df_tom = df_tom[columns]

    dfs = [df_lewagon, df_georg, df_mahar, df_tom]

    df = pd.concat([df_lewagon, df_georg, df_mahar, df_tom])
    df = df[columns]
    df = df.dropna().drop_duplicates().reset_index().drop(columns='index')

    df['artists'] = df['artists'].map(listify)
    df.to_csv('../data/all-songs.csv')


def convert_audios_to_spectrograms(mp3_dir, png_dir):
    """Convert all mp3 files in mp3_dir to spectrograms and save them
    as png files to png_dir"""
    for mp3_file in os.listdir(mp3_dir):
        if mp3_file.endswith(".mp3"):

            # Convert the mp3 file into a spectrogram
            spec = mp3_to_spectrogram(os.path.join(mp3_dir, mp3_file))

            # Save the spectrogram as an image file
            output_file = os.path.join(png_dir,
                                       os.path.splitext(mp3_file)[0] + ".png")

            # imsave(output_file, spec)
            imsave(output_file, (spec).astype(np.uint8))


def mp3_to_spectrogram(mp3_file):
    """Converts a single mp3 file to a png spectrogram"""
    # Load the mp3 file
    y, sr = librosa.load(mp3_file)

    # Calculate the Mel spectrogram
    spec = librosa.stft(y)
    spec_mag, _ = librosa.magphase(spec)
    mel_spec = librosa.feature.melspectrogram(S=spec_mag, sr=sr)
    spec_db = librosa.amplitude_to_db(abs(mel_spec))

    # Resize the spectrogram
    spec_resized = resize(spec_db, (128, 128))
    spec_resized = cv2.normalize(spec_resized, None, 255, 0, cv2.NORM_MINMAX,
                                 cv2.CV_8U)

    return spec_resized


if __name__ == "__main__":
    mp3_dir = LOCAL_MP3_DIR
    png_dir = LOCAL_PNG_DIR
    convert_audios_to_spectrograms(mp3_dir, png_dir)
    print('mp3 files successfully converted to png spectrograms.')
