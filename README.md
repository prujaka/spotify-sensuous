# spotify-sensuous-backend

## Old

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

Load environment variables:

```zsh
direnv reload .
```

Build container locally

```zsh
make docker_local_build
```

You can run container shell

```zsh
make docker_shell_run
```

You can run container locally

```zsh
make docker_local_run
```

And connect to it: http://localhost:8080/

List running containers

```zsh
docker ps
```

Stop container

```zsh
docker stop <container_id>
```

or

```zsh
docker kill <container_id>
```

## Push to Google Container Registry

Go to the GCP console, to Container Registry, and enable the service.

### Authenticate docker

```zsh
gcloud auth configure-docker
```

### Build for deployment

You need to define your project ID.

```zsh
docker build -t ${GCR_MULTI_REGION}/${GCP_PROJECT_ID}/${$DOCKER_IMAGE_NAME} .
```

⚠️ APPLE M1 Silicon users must build like this:

```zsh
make docker_gcr_build
```

At this point, check that it works locally before final push:

```zsh
make docker_gcr_local_check
```

And if it does, you can finally push to Google Container Registry:

```zsh
make docker_gcr_push
```

## Cloud run

Finally, you need to make your api continuously avilable. Go to the GCP console, to Cloud Run, and enable the service. You might also have to enable Cloud Run API.

```zsh
make docker_gcr_run
```
