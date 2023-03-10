import pandas as pd
import scipy as sp
from sklearn.preprocessing import MinMaxScaler

def recommend_songs (song, singer):

    # Data loading and scaling
    df = pd.read_csv('../data/lewagon-spotify-data.csv')
    df = df.drop(['popularity'],axis=1)
    df_numeric=df.drop(columns=['name','artists'])
    columns=df_numeric.columns.values.tolist()
    df_scaler = MinMaxScaler()
    df[columns] = df_scaler.fit_transform(df[columns])

    # Seed song selection
    artists_formatted = f"['{singer}']"
    seed_song = df[(df['name'] == song)
                   & (df['artists'] == artists_formatted)]

    # Feature "preprocessing"
    seed_song_features = seed_song.select_dtypes(exclude='object')
    X = df.select_dtypes(exclude='object')

    # List of closest neighbors to the seed song
    tree = sp.spatial.KDTree(X.to_numpy())
    distances, indeces = tree.query([seed_song_features], k=10)
    indeces = indeces.flatten()
    reco=[]
    for i in indeces:
        reco.append(f"*{df['name'].loc[i]}* by {df['artists'].loc[i]}")

    if reco==[]:
        return 'This song is not in the database'

    else:
        return reco

    #test
