import cv2
import os
import pandas as pd
import scipy as sp
from sklearn.preprocessing import MinMaxScaler

from sensuous.parameters import *


def strip_artists(s):
    """Removes brackets and quotes in s string."""
    return s.replace("['", "").replace("']", "").replace("', '", ", ")


def predict_playlist(song='White Christmas',
                     artist='Frank Sinatra',
                     n_neighbors=10):
    """Find `n_neighbors` closest neighbors of a given seed song in an audio
    feature space of le wagon sporify dataset. Only single artist is supported.
    If the song is not in the dataset, return the song's name.

    Parameters
    ----------
    song : str
        Song's name.

    artist : str
        Artist's name.

    n_neighbors : int
        Number of neighbors to the seed song.

    Returns
    -------
    neighbors : list of shape (n_neighbors,) of tuples of shape (2,) of str
        List of tuples of the closest songs. First element of a tuple is
        a song name, the second one is the artist(s).
    """

    df = pd.read_csv('https://wagon-public-datasets.s3.amazonaws.com/'
                     'Machine%20Learning%20Datasets/ML_spotify_data.csv')
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
    return {'playlist': list(zip(songs, artists))}


def img_id(img_path):
    """Returns the track id of the given path to a png file"""

    return int(img_path.split('/')[-1].split('.')[0])


def img_dict(img_path, df):
    """Returns a dictionary containing the track_id, the artist name
    and the song name"""

    track_id = img_id(img_path)
    return df[df['track_id'] == track_id].squeeze(axis=0).to_dict()


def img_neighbors(ref_image, png_dir):
    """Returns 10 closest images in png_dir to ref_image"""
    image1 = ref_image

    # resize reference image
    image1 = cv2.resize(image1, (128, 128))

    # calculate histogram for reference image
    hist1 = cv2.calcHist([image1], [0], None, [128], [0, 128])

    # precompute histograms for all images in data folder
    histograms = {}
    for filename in os.listdir(png_dir):
        image2 = cv2.imread(os.path.join(png_dir, filename))

        # resize image
        image2 = cv2.resize(image2, (128, 128))

        # calculate histogram
        hist2 = cv2.calcHist([image2], [0], None, [128], [0, 128])

        histograms[filename] = hist2

    # compare histograms and store distances in dictionary
    distances = {}
    for filename, hist2 in histograms.items():
        distance = cv2.compareHist(hist1, hist2, cv2.HISTCMP_INTERSECT)
        distances[filename] = distance

    # sort distances and return top 10 closest images
    sorted_distances = sorted(distances.items(),
                              key=lambda x: x[1],
                              reverse=True)
    closest_images = [x[0] for x in sorted_distances[0:10]]
    closest_images_paths = list(
        map(lambda x: os.path.join(png_dir, x), closest_images))

    return closest_images_paths


def predict_playlist_spectrograms(song='Castle Of Stars', artist='Ed Askew'):
    """Find 10 closest neighbors of the spectrogram of a given seed song
    to spectrograms of the songs in the png folder. Only single artist is
    supported. If the song is not in the dataset, return the song's name.

    Parameters
    ----------
    song : str
        Song's name.

    artist : str
        Artist's name.

    Returns
    -------
    neighbors : list of shape (n_neighbors,) of tuples of shape (2,) of str
        List of tuples of the closest songs. First element of a tuple is
        a song name, the second one is the artist(s).
    """

    png_dir = LOCAL_PNG_DIR
    raw_tracks_df = pd.read_csv(LOCAL_CSV_PATH)

    df = raw_tracks_df[['track_id', 'artist_name', 'track_title']]

    seed_song_df = df[(df['track_title'] == song) &
                      (df['artist_name'] == artist)]
    if seed_song_df.shape[0] == 0:
        print("No such a song in the dataset. Returning the user's entry.")
        return f'{song} by {artist}'
    seed_song_dict = seed_song_df.squeeze(axis=0).to_dict()
    seed_song_id = seed_song_dict['track_id']

    seed_img_name = f"{seed_song_id:06}.png"
    seed_img = os.path.join(png_dir, seed_img_name)
    ref_img = cv2.imread(seed_img, cv2.IMREAD_GRAYSCALE)
    closest_images = img_neighbors(ref_img, png_dir)

    img_dicts = [img_dict(img, df) for img in closest_images]
    playlist = [(d['artist_name'], d['track_title']) for d in img_dicts]
    playlist_dict = {'playlist': playlist}
    return playlist_dict


if __name__ == "__main__":
    print(predict_playlist_spectrograms())
