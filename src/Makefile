test: clear_mypy_cache
	ruff format .
	ruff check . --fix
	mypy --python-version 3.13 .
	pytest

clear_mypy_cache:
	-rm -fr .mypy_cache

# for docker default cmd
bash:
	/bin/bash
