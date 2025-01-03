lint:
	@uv run ruff check src/keyfort
checks:
	@uv run ruff check --fix
build: lint
	@uv build
format:
	@uv run ruff check --fix src
	@uv run ruff format src
test:
	uv run coverage run -m pytest ./tests
run:
	@.venv/bin/fastapi run keyfort/main.py --port 80 --host 0.0.0.0
docker-build-local:
	docker build . -t artifactory.keyfort.zenforcode.com:latest

docker-build-aws:
	./scripts/build_aws_docker.sh