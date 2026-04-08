# Makefile for rns-page-node

# Extract version from pyproject.toml
VERSION := $(shell grep "^version =" pyproject.toml | cut -d '"' -f 2)
VCS_REF := $(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")
BUILD_DATE := $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")

# Detect if docker buildx is available
DOCKER_BUILD := $(shell docker buildx version >/dev/null 2>&1 && echo "docker buildx build" || echo "docker build")
DOCKER_BUILD_LOAD := $(shell docker buildx version >/dev/null 2>&1 && echo "docker buildx build --load" || echo "docker build")

# Build arguments for Docker
DOCKER_BUILD_ARGS := --build-arg VERSION=$(VERSION) \
                     --build-arg VCS_REF=$(VCS_REF) \
                     --build-arg BUILD_DATE=$(BUILD_DATE)

.PHONY: all build sdist wheel clean install lint format docker-wheels docker-build docker-run help test docker-test test-advanced publish publish-gitea publish-pypi

all: build

build: clean
	poetry run python3 -m build

sdist:
	poetry run python3 -m build --sdist

wheel:
	poetry run python3 -m build --wheel

clean:
	rm -rf build dist *.egg-info

install: build
	pip install dist/*.whl

lint:
	ruff check .

format:
	ruff check --fix .

docker-wheels:
	$(DOCKER_BUILD) --target builder -f docker/Dockerfile -t rns-page-node-builder .
	docker create --name builder-container rns-page-node-builder true
	docker cp builder-container:/app/dist ./dist
	docker rm builder-container

docker-build:
	$(DOCKER_BUILD_LOAD) $(DOCKER_BUILD_ARGS) $(BUILD_ARGS) -f docker/Dockerfile -t git.quad4.io/rns-things/rns-page-node:latest -t git.quad4.io/rns-things/rns-page-node:$(VERSION) .

docker-run: setup-dirs
	docker run --rm -it \
		-v ./pages:/app/pages \
		-v ./files:/app/files \
		-v ./node-config:/app/node-config \
		-v ./reticulum-config:/home/app/.reticulum \
		git.quad4.io/rns-things/rns-page-node:latest \
		--node-name "Page Node" \
		--pages-dir /app/pages \
		--files-dir /app/files \
		--identity-dir /app/node-config \
		--announce-interval 360

test:
	bash tests/run_tests.sh

test-advanced:
	poetry run pytest tests/test_advanced.py

docker-test:
	$(DOCKER_BUILD_LOAD) -f docker/Dockerfile.tests -t rns-page-node-tests .
	docker run --rm rns-page-node-tests

setup-dirs:
	mkdir -p pages files node-config reticulum-config

help:
	@echo "Makefile commands:"
	@echo "  all            - alias for build"
	@echo "  build          - clean and build sdist and wheel"
	@echo "  sdist          - build source distribution"
	@echo "  wheel          - build wheel"
	@echo "  clean          - remove build artifacts"
	@echo "  install        - install built wheel"
	@echo "  lint           - run ruff linter"
	@echo "  format         - run ruff --fix"
	@echo "  docker-wheels  - build Python wheels in Docker"
	@echo "  docker-build   - build runtime Docker image (version: $(VERSION))"
	@echo "  docker-run     - run runtime Docker image"
	@echo "  test                 - run local integration tests"
	@echo "  docker-test          - build and run integration tests in Docker"
	@echo "  test-advanced        - run advanced tests via pytest"
	@echo "  publish              - publish to both Gitea and PyPI"
	@echo "  publish-gitea        - publish to Gitea registry"
	@echo "  publish-pypi         - publish to PyPI"
publish-gitea: build
	twine upload --repository-url https://git.quad4.io/api/packages/RNS-Things/pypi dist/*

publish-pypi: build
	twine upload dist/*

publish: publish-gitea publish-pypi
