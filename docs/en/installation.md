# Installation

## Requirements

- Python 3.10 or newer.
- A Reticulum transport on the local machine, such as `rnsd` or a shared bus interface.

If you only want to read the manpage, build the docs, or run the offline zipapp, you do not need Reticulum. Any feature that publishes or requests a page over the network needs it.

## Choose an install path

| Method | Best for | Needs internet |
| --- | --- | --- |
| `pip install rns-page-node` | Normal installs with PyPI | Yes |
| `pip-rns install --from-release ...` | Install from the RNS remote | No, needs Reticulum |
| `rngit release fetch ...` then `pip install` wheel | Manual release verification | No, needs Reticulum |
| Local wheel | Air-gapped or pre-staged installs | No |
| `.pyz` zipapp | No install step, portable | No after download |
| `git clone` | Hacking on the source | Yes, or Reticulum for `rns://` |

## Install from PyPI

The default package uses the `rns` PyPI package, which installs PyCA/cryptography for fast OpenSSL-backed crypto. On most platforms this is a prebuilt wheel and needs no Rust compiler.

```bash
pip install rns-page-node
```

With `pipx`:

```bash
pipx install rns-page-node
```

With `uv`:

```bash
uv tool install rns-page-node
```

## Install the pure Python package

If your target cannot install PyCA/cryptography, install the `rns-page-node-pure` package. It depends on `rnspure`, which contains the same Reticulum source but has no compiled dependencies. Reticulum will use its internal pure Python crypto backend when cryptography is not present.

```bash
pip install rns-page-node-pure
```

The pure version is slower and uses crypto primitives that are not the same OpenSSL implementation. Use it only when the standard package cannot be installed.

## Install from the RNS remote

The repository is published on Reticulum as `rns://06a54b505bb67b25ef3f8097e8001edc/public/rns-page-node`. You can install a signed release wheel with `pip-rns` or `rngit`. See the [Reticulum install guide](reticulum-install) for the full set of commands, including trust, verification, and source installs.

Quick example with `pip-rns`:

```bash
pip-rns install --from-release rns://06a54b505bb67b25ef3f8097e8001edc/public/rns-page-node --ref v1.7.0
```

Quick example with `rngit`:

```bash
rngit release rns://06a54b505bb67b25ef3f8097e8001edc/public/rns-page-node fetch v1.7.0:all
pip install v1.7.0/rns_page_node-1.7.0-py3-none-any.whl
```

## Install from a local wheel

If you already have a wheel, install it directly with `pip`:

```bash
pip install rns_page_node-1.7.0-py3-none-any.whl
```

For the pure variant:

```bash
pip install rns_page_node_pure-1.7.0-py3-none-any.whl
```

You can build a wheel from a checkout with `make build` or `make build-pure`.

## Install from source

Clone from GitHub or the RNS remote, then install in editable mode:

```bash
git clone https://github.com/Quad4-Software/rns-page-node.git
cd rns-page-node
pip install -e .
```

Over Reticulum:

```bash
git clone rns://06a54b505bb67b25ef3f8097e8001edc/public/rns-page-node
cd rns-page-node
pip install -e .
```

## Offline install with a zipapp

Build a single `.pyz` file with all dependencies, then run it without installing. This works well on air-gapped systems. See the [offline zipapp guide](offline).

```bash
make pyz
python3 dist/rns-page-node.pyz
```

## Shell completions

Completion scripts for bash, zsh, fish, tcsh and PowerShell are included in the repository under `completions/`. Copy the file for your shell to the standard completion directory, or source it from your shell profile.

For example, on bash:

```bash
sudo cp completions/rns-page-node.bash /etc/bash_completion.d/rns-page-node
```

On zsh:

```bash
cp completions/_rns-page-node ~/.zsh/site-functions/
```

## Manpage

The manpage source is in `docs/man/rns-page-node.1`. To install it system-wide:

```bash
sudo cp docs/man/rns-page-node.1 /usr/share/man/man1/
```
