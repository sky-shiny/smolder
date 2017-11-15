IMAGE_PATH=mcameron/smolder
TAG?=latest
IMAGE=$(IMAGE_PATH):$(TAG)


build:
	docker build -t $(IMAGE) .

push:
	docker push $(IMAGE)

run:
	docker run --rm -it $(IMAGE) $(COMMAND)

test:
	docker run --net host $(IMAGE) nosetests 


# Dependent / chained tasks
bootstrap: 
	build test
ci: 
	test push deploy

local:
	docker run -v $$(pwd):/src --rm -it $(IMAGE) 
