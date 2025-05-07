install:
	python3 -m pip install -e '.[test]'
	python -m pip install git+https://github.com/networkx/networkx.git@main
	python -m pip install git+https://github.com/joblib/joblib.git@main
	pre-commit install

lint:
	pre-commit run --all-files

test-backend:
	export NETWORKX_TEST_BACKEND="parallel"; \
	export NETWORKX_FALLBACK_TO_NX=True; \
	python3 -m pytest --pyargs networkx
	pytest nx_parallel

test: lint test-backend
