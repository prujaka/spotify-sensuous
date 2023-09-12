import pandas as pd
import scipy as sp
import os
from sklearn.preprocessing import MinMaxScaler
from sensuous.preprocessing import prepcsv as prep


def strip_artists(s):
    """Removes brackets and quotes in s string."""
    return s.replace("['", "").replace("']", "").replace("', '", ", ")


def predict_playlist_csv(artist: str = 'Frank Sinatra',
                         song_title: str = 'White Christmas',
                         n_neighbors: int = 10,
                         data_dir: str = 'data'):
    """Find `n_neighbors` closest neighbors of a given seed song in an audio
    feature space of le wagon spotify dataset. Only single artist is supported.
    If the song is not in the dataset, return the song's name.

    Parameters
    ----------
    artist : str
        Artist's name.

    song_title : str
        Song's name.

    n_neighbors : int
        Number of neighbors to the seed song.

    data_dir : str
        CSV file directory

    Returns
    -------
    neighbors : list of shape (n_neighbors,) of tuples of shape (2,) of str
        List of tuples of the closest songs. First element of a tuple is
        a song name, the second one is the artist(s).
    """
    prep.preprocess_csv_data(csv_dir=data_dir)
    df = pd.read_csv(os.path.join(data_dir, 'all-songs.csv'))
    df_numeric = df.drop(columns=['artists', 'song_title'])
    columns = df_numeric.columns.values.tolist()
    df_scaler = MinMaxScaler()
    df[columns] = df_scaler.fit_transform(df[columns])

    criterion = ((df['artists'].map(lambda x: artist in x)
                  | df['song_title'].map(lambda x: 'feat. ' + artist in x))
                 & (df['song_title'].map(lambda x: song_title in x)))

    seed_song = df[criterion]

    if seed_song.shape[0] == 0:
        print("No such a song in the dataset. Returning the user's entry.")
        return f'{song_title} by {artist}'
    elif seed_song.shape[0] > 1:
        print("There is more than one entry. Returning the user's entry.")
        return seed_song

    # Feature "preprocessing"
    seed_song_features = seed_song.select_dtypes(exclude='object')
    X = df.select_dtypes(exclude='object')

    # List of closest neighbors to the seed song
    tree = sp.spatial.KDTree(X.to_numpy())
    distances, indices = tree.query([seed_song_features], k=n_neighbors)
    indices = indices.flatten()
    neighbors_df = df.loc[list(indices)]
    songs = neighbors_df['song_title'].tolist()
    artists = [
        strip_artists(artist) for artist in neighbors_df['artists'].tolist()
    ]
    playlist = {'playlist': list(zip(artists, songs))}
    return playlist


if __name__ == "__main__":
    print(predict_playlist_csv(data_dir="../../data"))
