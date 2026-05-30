# RNS Page Node

[Русский](docs/languages/README.ru.md) | [中文](docs/languages/README.zh.md) | [日本語](docs/languages/README.ja.md) | [Italiano](docs/languages/README.it.md) | [Deutsch](docs/languages/README.de.md)

A simple way to serve simple pages and files over the [Reticulum network](https://reticulum.network/). Drop-in replacement for [NomadNet](https://github.com/markqvist/NomadNet) nodes that primarily serve pages and files. For more advanced pages and setups you should use NomadNet.

This project is no longer being updated, but it is configured to use RNS >= `1.3.4` so it will always use the latest compatible network stack.

**Source:** [GitHub](https://github.com/Quad4-Software/rns-page-node) (code mirror). **Releases:** [PyPI](https://pypi.org/project/rns-page-node/) and signed artifacts on Reticulum via [rngit](https://github.com/markqvist/Reticulum) (`origin` RNS remote).

## Features

- Serves simple pages and files over RNS
- Dynamic page support with environment variables
- Form data and request parameter parsing

## Installation

### From PyPI

```bash
pip install rns-page-node
# or
pipx install rns-page-node
```

### From GitHub (source)

```bash
pip install git+https://github.com/Quad4-Software/rns-page-node.git
# or
pipx install git+https://github.com/Quad4-Software/rns-page-node.git
```

### From an rngit release

If you use Reticulum and have [rngit](https://github.com/markqvist/Reticulum) configured, fetch a release from the project RNS remote (same URL as `git remote get-url origin` when using RNS):

```bash
rngit release fetch v1.6.0:all
pip install dist/rns_page_node-*.whl
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

## Build

```bash
make build
```

Build wheels only:

```bash
make wheel
```

## Development

```bash
poetry install
bash tests/run_tests.sh
make lint
```

`make test` runs the same script as `tests/run_tests.sh`.

## Releases

Distribution is **PyPI** plus **rngit** (Reticulum). Pushing tags/commits uses `origin`, which mirrors code to GitHub and the RNS remote.

```bash
make release-dist          # build dist/
make release               # tag, push (GitHub + RNS), upload rngit release
make release-local         # rngit release on local remote only
make publish               # upload wheels to PyPI
```

Other targets: `release-list`, `release-view`, `release-fetch`, `release-verify`, `release-delete`. Override `RELEASE_TAG`, `RNGIT_REMOTE`, `RNGIT_IDENTITY`, or `RNGIT_SIGNER` as needed.

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
