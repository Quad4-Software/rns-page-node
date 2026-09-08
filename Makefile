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

.PHONY: default help all build build-pure sdist wheel clean install install-dev
.PHONY: lint format check test test-advanced test-live run
.PHONY: publish publish-pypi publish-pypi-pure
.PHONY: pyz pyz-pure completions manpage docs-serve
.PHONY: release-dist release-tag release-push release-local release-upload release
.PHONY: release-list release-view release-fetch release-verify release-delete

default: help

help:
	@echo "rns-page-node $(VERSION)"
	@echo ""
	@echo "Build:     build build-pure sdist wheel pyz pyz-pure"
	@echo "Docs:      completions manpage docs-serve"
	@echo "Quality:   lint format check test test-advanced test-live"
	@echo "Run:       run"
	@echo "Publish:   publish publish-pypi publish-pypi-pure"
	@echo "Release:   release release-dist release-tag release-push release-local release-upload"
	@echo "           release-list release-view release-fetch release-verify release-delete"
	@echo "           (set RELEASE_TAG=vX.Y.Z, RNGIT_REMOTE, RNGIT_IDENTITY, etc.)"
	@echo "Other:     all clean install install-dev"

all: clean lint test build

build:
	poetry run python3 -m build

build-pure:
	rm -rf pure/rns_page_node pure/dist
	cp -r rns_page_node pure/rns_page_node
	poetry run python3 -m build pure --wheel

sdist:
	poetry run python3 -m build --sdist

wheel:
	poetry run python3 -m build --wheel

pyz: build
	mkdir -p dist
	poetry run shiv -c rns-page-node -o dist/rns-page-node.pyz .

pyz-pure: build-pure
	mkdir -p dist
	poetry run shiv -c rns-page-node -o dist/rns-page-node-pure.pyz pure/dist/rns_page_node_pure-1.7.0-py3-none-any.whl

completions:
	poetry run python3 tools/generate_completions.py

manpage:
	poetry run argparse-manpage --pyfile rns_page_node/cli.py --function setup_parser --manual-title "rns-page-node" --output docs/man/rns-page-node.1

docs-serve:
	python3 -m http.server 3000 --directory docs

clean:
	rm -rf build dist pure/dist pure/rns_page_node *.egg-info pure/*.egg-info .pytest_cache
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

test-live:
	poetry run pytest tests/test_live_transport.py

run:
	poetry run python3 -m rns_page_node.main

publish-pypi: build
	uv tool run twine upload dist/*

publish-pypi-pure: build-pure
	uv tool run twine upload pure/dist/*

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
