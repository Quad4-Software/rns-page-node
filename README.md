# RNS Page Node

A simple way to serve pages and files over the [Reticulum network](https://reticulum.network/). It is a drop-in replacement for [NomadNet](https://github.com/markqvist/NomadNet) nodes that primarily serve pages and files. For more advanced setups, use NomadNet.

Full documentation lives in [docs/](docs). The rendered site is at https://quad4-software.github.io/rns-page-node.

The project targets RNS 1.5.2 and newer and Python 3.10 and newer.

**Source:** [GitHub](https://github.com/Quad4-Software/rns-page-node) (code mirror). **Releases:** [PyPI](https://pypi.org/project/rns-page-node/) and signed artifacts on Reticulum via [rngit](https://github.com/markqvist/Reticulum) (`origin` RNS remote).

## Features

- Serves simple pages and files over RNS
- Dynamic page support with environment variables
- Form data and request parameter parsing
- Image Support

## Installation

Requires Python 3.10 or newer. The package depends on RNS 1.5.0 or newer and cryptography 50.0.0 or newer. Older releases cap these below the required versions, which conflicts with current Reticulum.

### From PyPI

```bash
pip install "rns-page-node>=1.7.0"
# or
pipx install "rns-page-node>=1.7.0"
```

With uv:

```bash
uv tool install "rns-page-node>=1.7.0"
```

If PyPI does not list 1.7.0 yet, install from GitHub (below) or upgrade an existing pipx app:

```bash
pipx install "git+https://github.com/Quad4-Software/rns-page-node.git" --force
```

### From GitHub (source)

```bash
pip install git+https://github.com/Quad4-Software/rns-page-node.git
# or
pipx install git+https://github.com/Quad4-Software/rns-page-node.git
```

With uv:

```bash
uv tool install "git+https://github.com/Quad4-Software/rns-page-node.git"
```

### From an rngit release

If you use Reticulum and have `rngit` configured, fetch a release from the project RNS remote. The remote is `rns://06a54b505bb67b25ef3f8097e8001edc/public/rns-page-node`, which is the same URL as `git remote get-url origin` when using the RNS remote.

```bash
rngit release rns://06a54b505bb67b25ef3f8097e8001edc/public/rns-page-node fetch v1.7.0:all
pip install v1.7.0/rns_page_node-1.7.0-py3-none-any.whl
```

With `pip-rns`:

```bash
pip-rns install --from-release rns://06a54b505bb67b25ef3f8097e8001edc/public/rns-page-node --ref v1.7.0
```

## Usage

```bash
# will use current directory for pages and files
rns-page-node
```

or with command-line options:

```bash
rns-page-node --node-name "Page Node" --pages-dir ./pages --files-dir ./files --media-dir ./media --identity-dir ./node-config --announce-interval 360
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
media-dir=./media
identity-dir=./node-config
announce-interval=360
```

Priority order: Command-line arguments > Environment variables > Config file > Defaults

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

## Pure Python variant

For targets that cannot install PyCA/cryptography, install the pure package:

```bash
pip install rns-page-node-pure
```

It depends on `rnspure` and uses Reticulum's internal pure Python crypto backend.

## Shell completions, manpage and docs

- Completions for bash, zsh, fish, tcsh and PowerShell are in `completions/`.
- The manpage is at `docs/man/rns-page-node.1`.
- Docsify documentation is in `docs/` and deploys to GitHub Pages.

Build the files with:

```bash
make completions
make manpage
```

## Offline zipapps

Build a single `.pyz` file with all dependencies included:

```bash
make pyz
make pyz-pure
```

Run it with `python3 dist/rns-page-node.pyz`.

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
  -m, --media-dir         Directory to serve images from (defaults to pages directory)
  -i, --identity-dir      Directory to persist the node's identity
  -a, --announce-interval Interval to announce the node's presence (in minutes, default: 360 = 6 hours)
  --page-refresh-interval Interval to refresh pages (in seconds, 0 = disabled)
  --file-refresh-interval Interval to refresh files (in seconds, 0 = disabled)
  -l, --log-level         Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
```

## License

This project incorporates portions of the [NomadNet](https://github.com/markqvist/NomadNet) codebase, which is licensed under the GNU General Public License v3.0 (GPL-3.0). As a derivative work, this project is also distributed under the terms of the GPL-3.0. See the [LICENSE](LICENSE) file for full license.
