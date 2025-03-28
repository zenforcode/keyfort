lint:
	golangci-lint run ./...

checks:
	golangci-lint run --fix ./...

build: lint checks test
	go build -o ./bin/keyfort ./cmd/keyfort/main.go

format:
	go fmt ./...

test:
	go test -cover ./...

run:
	go run ./cmd/keyfort/main.go --port 8080 --host 0.0.0.0

version:
	$(eval VERSION := $(shell git describe --tags --always --dirty))
	@echo ${VERSION}

docker-build-local: build version
	docker build . -t artifactory.keyfort.zenforcode.com:${VERSION}

docker-compose-local: docker-build-local
	docker compose up

api-test:
	@echo "Running API tests..."
	@cd ./tests/api-test/ && bru run
