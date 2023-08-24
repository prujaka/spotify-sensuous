reinstall_package:
	@pip uninstall -y sensuous || :
	@pip install -e .

docker_local_build:
	@docker build -t ${DOCKER_IMAGE_NAME_LOCAL} .

docker_local_run:
	@docker run -p 8080:8000 ${DOCKER_IMAGE_NAME_LOCAL}

docker_shell_run:
	@docker run -it ${DOCKER_IMAGE_NAME_LOCAL} sh

docker_gcr_build:
	@docker buildx build --platform linux/amd64 -t ${GCR_MULTI_REGION}/${GCP_PROJECT_ID}/${DOCKER_IMAGE_NAME} .

docker_gcr_local_check:
	@docker run -e PORT=8000 -p 8080:8000 ${GCR_MULTI_REGION}/${GCP_PROJECT_ID}/${DOCKER_IMAGE_NAME}

docker_gcr_push:
	@docker push ${GCR_MULTI_REGION}/${GCP_PROJECT_ID}/${DOCKER_IMAGE_NAME}

docker_gcr_run:
	@gcloud run deploy --image ${GCR_MULTI_REGION}/${GCP_PROJECT_ID}/${DOCKER_IMAGE_NAME} --platform managed --region ${GCR_REGION}

api_test_white_christmas:
	@open http://localhost:8080/predict\?song\=White%20Christmas\&artist\=Frank%20Sinatra
