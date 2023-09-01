import pandas as pd
import scipy as sp
from sklearn.preprocessing import MinMaxScaler


def strip_artists(s):
    """Removes brackets and quotes in s string."""
    return s.replace("['", "").replace("']", "").replace("', '", ", ")


def predict_playlist_lewagon(song='White Christmas',
                             artist='Frank Sinatra',
                             n_neighbors=10):
    """Find `n_neighbors` closest neighbors of a given seed song in an audio
    feature space of le wagon spotify dataset. Only single artist is supported.
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

    # df = pd.read_csv('https://wagon-public-datasets.s3.amazonaws.com/'
    #                  'Machine%20Learning%20Datasets/ML_spotify_data.csv')
    df = pd.read_csv("data/lewagon-spotify-data.csv")
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


if __name__ == "__main__":
    print(predict_playlist_lewagon())
