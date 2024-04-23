SHELL = /bin/bash
PYTHON ?= python

init:
	sh scripts/init.sh

install_dev:
	$(PYTHON) -m pip install -r requirements-ci.txt -e .