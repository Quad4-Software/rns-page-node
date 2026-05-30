# rns-page-node Makefile

VERSION := $(shell grep '^version =' pyproject.toml | cut -d '"' -f 2)

RNGIT ?= rngit
RNGIT_CONFIG ?= $(HOME)/.rngit
RNS_CONFIG ?= $(HOME)/.reticulum
RNGIT_REMOTE ?= $(shell git config --get remote.origin.url)
RNGIT_IDENTITY ?=
RNGIT_SIGNER ?=
RNGIT_NAME ?=
RELEASE_TAG ?= v$(shell poetry version -s 2>/dev/null || echo $(VERSION))
RELEASE_DIST ?= dist
RELEASE_ARTIFACT ?= all

RNGIT_RELEASE = $(RNGIT) release --config $(RNGIT_CONFIG) --rnsconfig $(RNS_CONFIG)
RNGIT_RELEASE_OPTS = $(if $(RNGIT_IDENTITY),-i $(RNGIT_IDENTITY),) \
	$(if $(RNGIT_SIGNER),-s $(RNGIT_SIGNER),) \
	$(if $(RNGIT_NAME),-n $(RNGIT_NAME),)
RELEASE_TARGET = $(RELEASE_TAG):$(RELEASE_DIST)

.PHONY: default help all build sdist wheel clean install install-dev
.PHONY: lint format check test test-advanced run
.PHONY: publish publish-pypi
.PHONY: release-dist release-tag release-push release-local release-upload release
.PHONY: release-list release-view release-fetch release-verify release-delete

default: help

help:
	@echo "rns-page-node $(VERSION)"
	@echo ""
	@echo "Build:     build sdist wheel clean install install-dev"
	@echo "Quality:   lint format check test test-advanced"
	@echo "Run:       run"
	@echo "Publish:   publish publish-pypi"
	@echo "Release:   release release-dist release-tag release-push release-local release-upload"
	@echo "           release-list release-view release-fetch release-verify release-delete"
	@echo "           (set RELEASE_TAG=vX.Y.Z, RNGIT_REMOTE, RNGIT_IDENTITY, etc.)"
	@echo "Other:     all"

all: clean lint test build

build: clean
	poetry run python3 -m build

sdist:
	poetry run python3 -m build --sdist

wheel:
	poetry run python3 -m build --wheel

clean:
	rm -rf build dist *.egg-info .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true

install: build
	pip install dist/*.whl

install-dev:
	poetry install

lint:
	poetry run ruff check .

format:
	poetry run ruff check --fix .

check: lint

test:
	bash tests/run_tests.sh

test-advanced:
	poetry run pytest tests/test_advanced.py

run:
	poetry run python3 -m rns_page_node.main

publish-pypi: build
	twine upload dist/*

publish: publish-pypi

release-dist: build

release-tag:
	@tag="$(RELEASE_TAG)"; \
	if git show-ref --verify --quiet "refs/tags/$$tag"; then \
		echo "Tag $$tag already exists"; \
	else \
		git tag -a "$$tag" -m "Release $$tag"; \
		echo "Created tag $$tag"; \
	fi

release-push: release-tag
	git push origin --follow-tags

release-local: release-dist
	$(RNGIT_RELEASE) $(RNGIT_RELEASE_OPTS) -L $(RNGIT_REMOTE) create $(RELEASE_TARGET)

release-upload: release-dist
	@test -n "$(RNGIT_REMOTE)" || (echo "RNGIT_REMOTE is empty; set it or configure git remote origin" && exit 1)
	$(RNGIT_RELEASE) $(RNGIT_RELEASE_OPTS) $(RNGIT_REMOTE) create $(RELEASE_TARGET)

release: release-dist release-tag release-push release-upload

release-list:
	@test -n "$(RNGIT_REMOTE)" || (echo "RNGIT_REMOTE is empty" && exit 1)
	$(RNGIT_RELEASE) $(RNGIT_REMOTE) list

release-view:
	@test -n "$(RELEASE_TAG)" || (echo "Set RELEASE_TAG=..." && exit 1)
	$(RNGIT_RELEASE) $(RNGIT_REMOTE) view $(RELEASE_TAG)

release-fetch:
	@test -n "$(RELEASE_TAG)" || (echo "Set RELEASE_TAG=... and optionally RELEASE_ARTIFACT=all" && exit 1)
	$(RNGIT_RELEASE) $(RNGIT_RELEASE_OPTS) $(RNGIT_REMOTE) fetch $(RELEASE_TAG):$(RELEASE_ARTIFACT)

release-verify:
	@test -n "$(RELEASE_TAG)" || (echo "Set RELEASE_TAG=... and optionally RELEASE_ARTIFACT=all" && exit 1)
	$(RNGIT_RELEASE) $(RNGIT_RELEASE_OPTS) -o $(RNGIT_REMOTE) verify $(RELEASE_TAG):$(RELEASE_ARTIFACT)

release-delete:
	@test -n "$(RELEASE_TAG)" || (echo "Set RELEASE_TAG=..." && exit 1)
	$(RNGIT_RELEASE) $(RNGIT_REMOTE) delete $(RELEASE_TAG)
