IMAGE_PATH=sky-shiny/smolder
TAG?=latest
IMAGE=$(IMAGE_PATH):$(TAG)
COMMAND?=
SUDO?=
DOCKER_ARGS?=


build:
	$(SUDO) docker build -t $(IMAGE) .

push:
	$(SUDO) docker push $(IMAGE)

run:
	$(SUDO) docker run ${DOCKER_ARGS} --rm -it $(IMAGE) $(COMMAND)

test:
	make run DOCKER_ARGS="--net host --entrypoint=nosetests"

# Dependent / chained tasks
bootstrap: build test
ci: test push deploy


local:
	$(SUDO) docker run \
		-v $$(pwd):/src \
		${DOCKER_ARGS} \
		--entrypoint sh \
		--rm -it $(IMAGE)
