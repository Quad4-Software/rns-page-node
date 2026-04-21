# RNS Page Node

[Русский](docs/languages/README.ru.md) | [中文](docs/languages/README.zh.md) | [日本語](docs/languages/README.ja.md) | [Italiano](docs/languages/README.it.md) | [Deutsch](docs/languages/README.de.md)

A simple way to serve pages and files over the [Reticulum network](https://reticulum.network/). Drop-in replacement for [NomadNet](https://github.com/markqvist/NomadNet) nodes that primarily serve pages and files.

## Features

- Serves pages and files over RNS
- Dynamic page support with environment variables
- Form data and request parameter parsing

## Installation

### From PyPI

```bash
pip install rns-page-node
# or
pipx install rns-page-node
```

### From Gitea Packages

```bash
# Pip
pip install --index-url https://git.quad4.io/api/packages/RNS-Things/pypi/simple/ --extra-index-url https://pypi.org/simple rns-page-node

# Pipx
pipx install --pip-args "--index-url https://git.quad4.io/api/packages/RNS-Things/pypi/simple/ --extra-index-url https://pypi.org/simple" rns-page-node
```

**Permanent Configuration for Gitea (Optional):**

To avoid typing the index URLs every time when using the Gitea registry, add them to your `pip.conf`:

```ini
# ~/.config/pip/pip.conf
[global]
index-url = https://git.quad4.io/api/packages/RNS-Things/pypi/simple/
extra-index-url = https://pypi.org/simple
```

Then you can simply use:

```bash
pip install rns-page-node
# or
pipx install rns-page-node
```

**Manual Download (Latest Release):**

You can download the wheel file directly from the [latest release](https://git.quad4.io/RNS-Things/rns-page-node/releases/latest) and install it:

```bash
# Wget
wget https://git.quad4.io/RNS-Things/rns-page-node/releases/download/v1.5.0/rns_page_node-1.5.0-py3-none-any.whl
pip install rns_page_node-1.5.0-py3-none-any.whl

# Curl
curl -O -L https://git.quad4.io/RNS-Things/rns-page-node/releases/download/v1.5.0/rns_page_node-1.5.0-py3-none-any.whl
pip install rns_page_node-1.5.0-py3-none-any.whl
```

```bash
# Pip
pip install git+https://git.quad4.io/RNS-Things/rns-page-node.git --break-system-packages
# Pipx via Git
pipx install git+https://git.quad4.io/RNS-Things/rns-page-node.git
# UV
uv venv
source .venv/bin/activate
uv pip install git+https://git.quad4.io/RNS-Things/rns-page-node.git
```

## Usage

```bash
# will use current directory for pages and files
rns-page-node
```

or with command-line options:

```bash
rns-page-node --node-name "Page Node" --pages-dir ./pages --files-dir ./files --identity-dir ./node-config --announce-interval 360
```

or with a config file:

```bash
rns-page-node /path/to/config.conf
```

### Configuration File

You can use a configuration file to persist settings. See `config.example` for an example.

Config file format is simple `key=value` pairs:

```
# Comment lines start with #
node-name=My Page Node
pages-dir=./pages
files-dir=./files
identity-dir=./node-config
announce-interval=360
```

Priority order: Command-line arguments > Config file > Defaults

### Docker/Podman

```bash
docker run -it --rm -v ./pages:/app/pages -v ./files:/app/files -v ./node-config:/app/node-config -v ./reticulum-config:/home/app/.reticulum git.quad4.io/rns-things/rns-page-node:latest
```

### Docker/Podman Rootless

```bash
mkdir -p ./pages ./files ./node-config ./reticulum-config
chown -R 1000:1000 ./pages ./files ./node-config ./reticulum-config
podman run -it --rm -v ./pages:/app/pages -v ./files:/app/files -v ./node-config:/app/node-config -v ./reticulum-config:/home/app/.reticulum git.quad4.io/rns-things/rns-page-node:latest
```

Mounting volumes are optional, you can also copy pages and files to the container `podman cp` or `docker cp`.

## Build

```bash
make build
```

Build wheels:

```bash
make wheel
```

### Build Wheels in Docker

```bash
make docker-wheels
```

## Development

```bash
poetry install
bash tests/run_tests.sh
ruff check .
```

`make test` runs the same script as `tests/run_tests.sh`.

## Pages

Supports dynamic executable pages with full request data parsing. Pages can receive:
- Form fields via `field_*` environment variables
- Link variables via `var_*` environment variables
- Remote identity via `remote_identity` environment variable
- Link ID via `link_id` environment variable

This enables forums, chats, and other interactive applications compatible with NomadNet clients.

## Options

```
Positional arguments:
  node_config             Path to rns-page-node config file

Optional arguments:
  -c, --config            Path to the Reticulum config file
  -n, --node-name         Name of the node
  -p, --pages-dir         Directory to serve pages from
  -f, --files-dir         Directory to serve files from
  -i, --identity-dir      Directory to persist the node's identity
  -a, --announce-interval Interval to announce the node's presence (in minutes, default: 360 = 6 hours)
  --page-refresh-interval Interval to refresh pages (in seconds, 0 = disabled)
  --file-refresh-interval Interval to refresh files (in seconds, 0 = disabled)
  -l, --log-level         Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
```

## License

This project incorporates portions of the [NomadNet](https://github.com/markqvist/NomadNet) codebase, which is licensed under the GNU General Public License v3.0 (GPL-3.0). As a derivative work, this project is also distributed under the terms of the GPL-3.0. See the [LICENSE](LICENSE) file for full license.
