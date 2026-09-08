# Installation

## Requirements

- Python 3.10 or newer.
- A Reticulum transport on the local machine, such as an RNS daemon or a shared bus interface.

## Install the standard package

The default package uses the `rns` PyPI package, which installs PyCA/cryptography for fast OpenSSL-backed crypto. On most platforms this is a prebuilt wheel and needs no Rust compiler.

```bash
pip install rns-page-node
```

## Install the pure Python package

If your target cannot install PyCA/cryptography, install the `rns-page-node-pure` package. It depends on `rnspure`, which contains the same Reticulum source but has no compiled dependencies. Reticulum will use its internal pure Python crypto backend when cryptography is not present.

```bash
pip install rns-page-node-pure
```

The pure version is slower and uses crypto primitives that are not the same OpenSSL implementation. Use it only when the standard package cannot be installed.

## Install from source

```bash
git clone https://github.com/Quad4-Software/rns-page-node.git
cd rns-page-node
pip install -e .
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

## Offline zipapp

For air-gapped or offline systems, build a standalone `.pyz` zipapp. See the [offline zipapp guide](offline).
