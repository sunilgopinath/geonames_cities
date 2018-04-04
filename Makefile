# Some simple testing tasks (sorry, UNIX only).

FLAGS=

isort:
	isort --recursive --quiet geonames_sunil/ tests/ setup.py  # --check-only

pytest:
	py.test --cov=loader

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
	yapf --recursive --in-place setup.py geonames_sunil/ tests/

.PHONY: flake isort clean test yapf pytest
