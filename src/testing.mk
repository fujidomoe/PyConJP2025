export APP_ENV=testing
export DB_NAME=pyconjp2025_test

test: clear_mypy_cache
	ruff format .
	ruff check . --fix
	mypy --python-version 3.13 .
	pytest

test_ci: clear_mypy_cache
	ruff check . --diff
	ruff format . --check --diff
	mypy --python-version 3.13 .
	pytest

clear_mypy_cache:
	-rm -fr .mypy_cache
