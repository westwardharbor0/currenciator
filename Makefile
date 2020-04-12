#!/usr/bin/make -f

#------------- Global variables ---------------#
CURRENT := $(shell pwd)
VENV := $(CURRENT)/venv
VENV_BIN := $(VENV)/bin
PYTHON_BIN := $(VENV_BIN)/python3
PYTHON_FLASK := $(VENV_BIN)/flask
PYTHON_PIP := $(VENV_BIN)/pip3
PYTHON_TEST := $(VENV_BIN)/unittest


#-------------- CLI variables ----------------#
amount :=
input_currency :=
output_currency := 


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
	
cli: $(objects)
ifeq ($(OUTPUT_CURRENCY), )
	$(PYTHON_BIN) currenciator_cli.py  --amount $(amount) --input_currency $(input_currency)
else
	$(PYTHON_BIN) currenciator_cli.py  --amount $(amount) --input_currency $(input_currency) --output_currency $(output_currency)
endif

run:
	export FLASK_DEBUG=1
	export FLASK_ENV=development
	export FLASK_APP=api.py
	$(PYTHON_FLASK) run --port 3692

docker-build: # --- builds docker image to run
	docker build . --tag currenciator_api

docker-run: # --- runs api
	docker run --name currenciator_api -it --rm --network host currenciator_api

