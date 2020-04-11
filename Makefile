#!/usr/bin/make -f

CURRENT := $(shell pwd)
VENV := $(CURRENT)/venv
PYTHON_FLASK := $(VENV)/bin/flask
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

run:
	export FLASK_DEBUG=1
	export FLASK_ENV=development
	export FLASK_APP=api.py
	$(PYTHON_FLASK) run --port 3692

docker-build: # --- builds docker image to run
	docker build . --tag currenciator_api

docker-run: # --- runs api
	docker run --name currenciator_api -it --rm --network host currenciator_api

