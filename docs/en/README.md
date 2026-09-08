# rns-page-node

rns-page-node turns a directory of Micron pages and files into a destination on the [Reticulum](https://reticulum.network) network. It answers page, file and media requests from clients such as [NomadNet](https://github.com/markqvist/NomadNet).

It is a single Python package with one job: read pages and files from disk, keep them inside a path jail, and serve them over an RNS destination.

You can install it from PyPI, from a release over the Reticulum network, from a local wheel, as an offline `.pyz` zipapp, or by cloning the source.

## What it serves

- Micron pages ending in .mu under the page route.
- Any static file under the file route.
- WebP images under the media route for NomadNet 1.4.x image requests.
- A generated index.mu if none exists in the pages directory.

## Safety and speed

- Paths are resolved to real files and checked against the root directory, so parent-directory tricks, symlinks and mixed slashes are caught.
- Only WebP files are accepted for media.
- The media handler runs in about 0.08 ms per request in local benchmarks.
- All handlers are covered by unit, adversarial, oracle, stress, performance and live transport tests.

## Install and run

```bash
pip install rns-page-node
rns-page-node
```

This starts a node with the default pages, files and node-config directories in the current working directory.

## Install paths

- [Installation](installation) covers pip, wheels, zipapps, source clones and shell completions.
- [Install from Reticulum](reticulum-install) explains how to fetch a signed release with `pip-rns` or `rngit`.
- [Offline install and zipapps](offline) covers `.pyz`, `opip` bundles and `pip-rns export` for USB sharing.
- [Pure Python variant](pure) explains the `rns-page-node-pure` package for systems without compiled dependencies.

## Quick links

- [Usage](usage)
- [Configuration](configuration)
