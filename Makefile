lint:
	@ruff check keyfort
build: lint
	@uv build
format:
	@uv run ruff format keyfort
test:
	uv run coverage run -m pytest ./tests
run:
	@.venv/bin/fastapi run keyfort/main.py --port 80 --host 0.0.0.0
docker-build-local:
	docker build . -t 

docker-build-aws:
	./scripts/build_aws_docker.sh