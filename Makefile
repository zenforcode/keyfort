lint:
	@uv run ruff check src/keyfort
checks:
	@uv run ruff check --fix
build: lint checks test
	@uv build go build
format:
	@uv run ruff check --fix src
	@uv run ruff format src
test:
	@uv run coverage run --source=./src -m pytest ./tests
	@uv run coverage report -m
run:
	@uv run .venv/bin/fastapi run src/keyfort/main.py --port 8080 --host 0.0.0.0
version:
	$(eval VERSION := $(shell uv run dunamai from git --no-metadata --format "{base}-{commit}"))
	@echo ${VERSION}
docker-build-local:	build	version
	docker build . -t artifactory.keyfort.zenforcode.com:${VERSION}
docker-compose-local:	docker-build-local
	docker compose up

api-test:
	@echo "Running API tests..."
	@cd ./tests/api-test/ && bru run
