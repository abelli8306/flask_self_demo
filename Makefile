PROJECT = flask_self_demo
RegistryDomain := ccr.ccs.tencentyun.com
RegistryNamespace := tke-chaos
IMAGE := ${RegistryDomain}/${RegistryNamespace}/${PROJECT}
TAG := $(shell git describe --dirty --always --tags | sed 's/-/./g')
IMAGEID := ${IMAGE}:${TAG}
CONTAINID := $(shell docker ps -aq -f name=${PROJECT})

list:
	@echo "project: "${PROJECT}
	@echo "image: "${IMAGEID}

docker: build
	@docker build --network=host --no-cache -t ${IMAGEID} -f ./Dockerfile .

run: docker
ifneq ($(CONTAINID), )
	@docker stop ${CONTAINID}
	@docker rm ${CONTAINID}
endif
	@docker run -idt -p 80:80 --name ${PROJECT} ${IMAGEID}
	@docker logs ${PROJECT} -f

push: docker
	@docker push ${IMAGEID}

.PHONY: default build list docker run push