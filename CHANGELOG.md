# Changelog

All notable changes to this project will be documented in this file.

## [1.7.0] - 2026-09-08

### Added
- Support for serving WebP images to NomadNet 1.4.x clients through a new /media request handler.
- Images are served from the pages directory and must use the .webp extension.
- Traversal, non-WebP, and malformed media requests are rejected.
- Unit, security fuzz, and live RNS transport tests cover the /media handler.

### Changed
- Minimum RNS dependency raised to 1.5.0. Cryptography lower bound set to 3.4.7 with no upper cap.
- Added live RNS link integration tests, a shared live test harness, and a test-live make target.

## [1.6.0] - 2026-05-30

This project will no longer be updated, but is configured to use RNS 1.3.4 or newer so it will always use the latest compatible stack.

### Changed
- Minimum RNS dependency set to 1.3.4 with an open upper bound.
- Minimum Python version remains 3.9.2. Dev tooling capped to versions that support 3.9.
- README and translations updated for final maintenance mode. Docker install and build sections removed.
- Makefile Docker targets removed. rngit release targets added (release, release-upload, release-fetch, and related targets).
- Taskfile Docker tasks removed to match dropped container support.

### Removed
- Docker support (docker directory, images, and all make docker-* / Taskfile docker tasks).

## [1.5.1] - 2026-04-30

### Security
- Docker images install pip 26.1 or newer in builder, runtime, and base image Python to address CVE-2026-3219.

### Dependencies
- Updated rns to >=1.2.0,<1.5.0 and cryptography to >=47.0.0,<48.

## [1.5.0] - 2026-04-20

### Dependencies
- Runtime: rns >=1.1.6,<1.5.0 and cryptography >=46.0.7,<47.
- Development: pytest, hypothesis, ruff, build, and twine updates. Pytest configuration added in pyproject.toml.

### Security
- Page and file handlers resolve paths under the configured root with Path.resolve() and Path.relative_to(), replacing string prefix checks. Directory traversal and prefix edge cases are rejected consistently.
- Relative path segments reject embedded NUL bytes and normalize backslashes before resolving.
- Added test_path_security.py with parametrized traversal cases and Hypothesis fuzzing.

### Changed
- run_tests.sh runs pytest before the local transport client script.
- README and localized readmes updated. Development section added. Makefile test-advanced uses pytest.

### Removed
- Nix-related Taskfile targets. Renovate and Flake-based tooling dropped.
- DeepSource configuration removed.

### Added
- Unit tests for handlers and config loading.
- Security-focused path handling tests included in run_tests.sh.

## [1.4.0] - 2026-01-15

### Added
- PyPI publishing automation and workflows.
- Manual installation instructions for wheel files from releases.
- Docker entrypoint using su-exec for volume permission fixes.
- Publish targets in Makefile and Taskfile.
- Modular package layout: cli, config, core, and handlers modules.

### Changed
- Refactored monolithic main.py into a modular package structure.
- Full PEP 484 type hints across the codebase.
- README and all translations updated for new installation methods.
- Test suite updated for the modular structure.
