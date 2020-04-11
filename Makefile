#!/usr/bin/make -f

CURRENT := $(shell pwd)
VENV := $(CURRENT)/venv
PYTHON_BIN := $(VENV)/bin/python3
PYTHON_PIP := $(VENV)/bin/pip3
PYTHON_TEST := $(VENV)/bin/unittest

all: help
	$(error "make without target")

help: # --- help doh ?
	@echo "Available targets are:"
	@grep -E "^[^_.][a-zA-Z0-9_-]+:" $(realpath $(firstword $(MAKEFILE_LIST))) | sed "s/^/  /g"

bootstrap: # --- prepares the local enviroment for running and developing
	virtualenv -p /usr/bin/python3 --no-download --clear $(VENV)
	$(PYTHON_PIP) install -r requirements.txt

tests: # --- runs tests
	$(PYTHON_TEST) $(CURRENT)/tests/*

docker-build: # --- builds docker image to run
	docker build . --tag currenciator_api

docker-run: # --- runs api
	docker run --rm currenciator_api

docker-run-dev: # --- runs api and mounts folder to develop in docker
	docker run -it --rm -v $(CURRENT)/currenciator/:/currenciator/ currenciator_api
