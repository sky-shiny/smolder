IMAGE_PATH=mcameron/smolder
TAG?=latest
IMAGE=$(IMAGE_PATH):$(TAG)
SHELL := /bin/bash

# From http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## Build docker image
	docker build -t $(IMAGE) .

push: ## Publish docker image
	docker push $(IMAGE)

test: ## Test docker image
	docker run --name smolder --rm -itd $(IMAGE) sh
	docker exec smolder nosetests
	docker rm -f smolder

all: ## build test push
	build test push

.DEFAULT_GOAL := help
.PHONY: all clean build run config test ssh
