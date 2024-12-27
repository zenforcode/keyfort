lint:
	ruff check keyfort
build: lint
	uv build
format:
	ruff format keyfort
test:
	uv run pytest -v tests