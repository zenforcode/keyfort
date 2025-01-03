lint:
	@uv run ruff check src/keyfort
checks:
	@uv run ruff check --fix
build: lint test
	@uv build
format:
	@uv run ruff check --fix src
	@uv run ruff format src
test:
	@uv run coverage run --source=./src -m pytest ./tests
	@uv run coverage report -m
run:
	@uv run .venv/bin/fastapi run src/keyfort/main.py --port 8080 --host 0.0.0.0
docker-build-local:
	docker build . -t artifactory.keyfort.zenforcode.com:latest