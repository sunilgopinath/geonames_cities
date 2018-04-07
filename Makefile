# Some simple testing tasks (sorry, UNIX only).

virtualenv_dir 	 = $(cwd)/venv

FLAGS=

create_venv:
	python3 -m virtualenv env
	
start_venv:
	source env/bin/activate

ensure_env:
	test -d venv || virtualenv -p $(python_base_path) $(virtualenv_dir)

install-deps: ensure_env
	./env/bin/pip install -r requirements.txt

isort:
	isort --recursive --quiet geonames_sunil/ insert/ tests/ monitor.py setup.py  # --check-only

load:
	./load.sh & echo $! > pid.txt

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

.PHONY: flake isort install-deps clean test yapf pytest load
