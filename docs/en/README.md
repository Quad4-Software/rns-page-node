# rns-page-node

rns-page-node turns a directory of Micron pages and files into a destination on the [Reticulum](https://reticulum.network) network. It answers page, file and media requests from clients such as [NomadNet](https://github.com/markqvist/NomadNet).

It is a single Python package with one job: read pages and files from disk, keep them inside a path jail, and serve them over an RNS destination.

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

This starts a node with the default pages, files and node-config directories in the current working directory. Read the [installation guide](installation) for pip, source, zipapp and pure package options.

## Quick links

- [Installation](installation)
- [Usage](usage)
- [Configuration](configuration)
- [Offline zipapp](offline)
- [Pure Python variant](pure)
