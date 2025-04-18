IMAGE_NAME=ask
CONTAINER_NAME=ask-container

all:
	python3 main.py

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -it --rm --name $(CONTAINER_NAME) $(IMAGE_NAME)

shell:
	docker run -it --rm --name $(CONTAINER_NAME) $(IMAGE_NAME) /bin/bash

clean:
	docker rmi -f $(IMAGE_NAME)
