lint:
	@uv run ruff check src/keyfort
checks:
	@uv run ruff check --fix
build: lint checks test
	@uv build
format:
	@uv run ruff check --fix src
	@uv run ruff format src
test:
	@uv run coverage run --source=./src -m pytest ./tests
	@uv run coverage report -m
run:
	@uv run .venv/bin/fastapi run src/keyfort/main.py --port 8080 --host 0.0.0.0
docker-build-local:	build
	docker build . -t artifactory.keyfort.zenforcode.com:latest
docker-compose-local:	docker-build-local
	docker compose up

api-test:
	@echo "Installing Bruno CLI..."
	@shell command -v bru >/dev/null 2>&1 || sudo npm install -g @usebruno/cli
	@echo "Running API tests..."
	@cd ./tests/api-test/ && bru run

