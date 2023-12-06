import pandas as pd


def semicolonize(s: str) -> str:
    """Strip a list-looking string s from brackets and single quotes
    and put a semicolon as a separator instead"""
    return ';'.join(s.strip("[]'").split("', '"))


def listify(s: str) -> str:
    """Remove a semicolon as a separator of a string s and format it as
    a list-looking string"""
    s = s.split(';')
    return str(s)


def preprocess_csv_data(csv_dir: str = '../data') -> None:
    """Clean the four available datasets and merge them into one"""
    df_lewagon_init = pd.read_csv(f'{csv_dir}/lewagon-spotify-data.csv')
    df_georg_init = pd.read_csv(f'{csv_dir}/data-georgemcintire.csv')
    df_mahar_init = pd.read_csv(f'{csv_dir}/data-maharshipandya.csv')
    df_tom_init = pd.read_csv(f'{csv_dir}/data-tomigelo-2019-04.csv')

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
    df = pd.concat(dfs)
    df = df[columns]
    df = df.dropna().drop_duplicates().reset_index().drop(columns='index')

    df['artists'] = df['artists'].map(listify)

    df.to_csv(f'{csv_dir}/all-songs.csv')

    print('Csv data preprocessing done, saved the cleaned data to file '
          f'"{csv_dir}/all-songs.csv"')


if __name__ == '__main__':
    data_dir = "../../data"
    preprocess_csv_data(csv_dir=data_dir)
