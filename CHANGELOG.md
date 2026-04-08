# Changelog

All notable changes to this project will be documented in this file.

## [1.4.1] - 2026-04-08

### Dependencies
- **Runtime**: `rns` `>=1.1.3,<1.5.0` (lock: 1.1.4); `cryptography` `>=46.0.5,<47` (lock: 46.0.7).
- **Development**: `pytest` ^8.4 (lock: 8.4.2), `hypothesis` ^6.135 (lock: 6.141.1), `ruff` ^0.14.10 (lock: 0.14.14), `build` ^1.3 (lock: 1.4.2), `twine` ^6.2.0 (lock: 6.2.0). `pytest` configuration added under `[tool.pytest.ini_options]` in `pyproject.toml`.

### Security
- Page and file handlers now resolve paths under the configured root using `Path.resolve()` and `Path.relative_to()`, replacing string prefix checks so directory traversal and prefix edge cases are rejected consistently; invalid paths during resolution are handled safely. Relative segments reject embedded NUL bytes and normalize backslashes to forward slashes before resolving (Windows-style `..\\..\\file` cannot bypass checks on POSIX by being treated as a single file name).
- `tests/test_path_security.py`: parametrized traversal cases, outside-file marker never appears under Hypothesis fuzzing of path components, and invariants on `_safe_file_in_root` results.

### Changed
- `tests/run_tests.sh` runs `pytest` (unit, property, and advanced tests) before the local transport client script.
- `README.md` and localized readmes (`docs/languages/README.*.md`): Git install commands match the English guide; **Development** section added (Poetry, `tests/run_tests.sh`, Ruff). `Makefile` `test-advanced` target uses `pytest` like `Taskfile.yml`.

### Removed
- Nix-related Taskfile targets (`nix-shell`, `nix-build`). Project environments use Poetry (and Docker where documented); Renovate and Flake-based tooling were dropped from the repo.
- DeepSource configuration (`.deepsource.toml`) removed.

### Added
- `tests/test_handlers_unit.py` and `tests/test_config_unit.py`: unit coverage and Hypothesis-based checks for handlers and config loading.
- `tests/test_path_security.py`: security-focused and fuzz tests for path handling (included in `tests/run_tests.sh`).

## [1.4.0] - 2026-01-15

### Added
- **PyPI Support**: Added automation and workflows to publish the package to PyPI in addition to Gitea.
- **Manual Installation**: Added instructions and examples for downloading and installing `.whl` files directly from releases using `wget` or `curl`.
- **Docker Permissions**: Introduced `docker/entrypoint.sh` using `su-exec` to automatically fix volume permission issues when running in Docker.
- **Task Automation**: Added `publish`, `publish-gitea`, and `publish-pypi` targets to `Makefile` and `Taskfile.yml`.
- **Project Structure**: Created `cli.py`, `config.py`, `core.py`, and `handlers.py` to modularize the codebase.

### Changed
- **Refactoring**: Completely refactored the monolithic `main.py` into a modular package structure for better maintainability and testability.
- **Type Hinting**: Added full PEP 484 type hints across the entire codebase.
- **Documentation**: Comprehensive update of `README.md` and all translations (German, Italian, Japanese, Russian, Chinese) to reflect new installation methods.
- **Testing**: Updated the test suite (`run_tests.sh` and `test_advanced.py`) to support the new modular structure and improved reliability.
