install:
	python3 -m pip install -e '.[default]'
	python3 -m pip install -e '.[test]'
	python -m pip install git+https://github.com/networkx/networkx.git@main
	python -m pip install git+https://github.com/joblib/joblib.git@main

lint:
	python3 -m pip install -e '.[developer]'
	python3 -m pre-commit run --all-files

run-networkx-tests:
	export NETWORKX_TEST_BACKEND="parallel"; \
	export NETWORKX_FALLBACK_TO_NX=True; \
	python3 -m pytest --pyargs networkx

test-only-nx-parallel:
	pytest nx_parallel

test-backend: run-networkx-tests test-only-nx-parallel

test: lint test-backend
