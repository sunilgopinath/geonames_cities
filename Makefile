# Some simple testing tasks (sorry, UNIX only).

virtualenv_dir 	 = $(cwd)/venv

FLAGS=

create_venv:
	python3 -m virtualenv env

install:
	./env/bin/pip install -e .

install-deps:
	./env/bin/pip install -r requirements.txt

isort:
	isort --recursive --quiet geonames_sunil/ insert/ tests/ monitor.py setup.py  # --check-only

load:
	./load.sh

load-as-single-file:
	./sql/single_file.sh

pytest:
	py.test

test: isort yapf pytest

clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name '@*' `
	rm -f `find . -type f -name '#*#' `
	rm -f `find . -type f -name '*.orig' `
	rm -f `find . -type f -name '*.rej' `
	rm -f .coverage
	rm -rf coverage
	rm -rf build
	rm -rf htmlcov
	rm -rf dist

yapf:
	yapf --recursive --in-place geonames_sunil/ insert/ tests/ monitor.py setup.py

.PHONY: flake isort install-deps clean test yapf pytest load load-as-single-file
