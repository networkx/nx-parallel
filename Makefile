install:
	python3 -m pip install -e '.[developer, test]'
	pre-commit install

lint:
	pre-commit run --all-files

test-backend:
	export NETWORKX_TEST_BACKEND="parallel"
	export NETWORKX_FALLBACK_TO_NX=True
	python3 -m pytest --pyargs networkx
	pytest nx_parallel

test: lint test-backend
