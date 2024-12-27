lint:
	ruff check keyfort
build: lint
	uv build
test:
	uv run pytest -v tests