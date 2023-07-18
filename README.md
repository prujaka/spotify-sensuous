# spotify-sensuous-backend

## Old Garbage

To install the python package of the project, run the following command:

```py
pip install -e .
```

To convert mp3 files to png spectrograms:
```py
python -m sensuous.preprocessing.preprocessing
```
Before conversion, make sure that the local `img_spec` directory exists

## Deploy

```zsh
direnv reload .
```

