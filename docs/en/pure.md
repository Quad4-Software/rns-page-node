# Pure Python variant

The standard package depends on `rns`, which installs PyCA/cryptography. On some systems, cryptography cannot be installed because it needs a compiled wheel or a Rust compiler.

The `rns-page-node-pure` package depends on `rnspure` instead. The `rnspure` package contains the same Reticulum source as `rns`, but declares no compiled dependencies. When cryptography is not installed, Reticulum falls back to its internal pure Python crypto backend.

## When to use the pure package

- The target has no Rust compiler and no prebuilt cryptography wheel.
- You are running on an unusual architecture.
- You want the smallest dependency tree and are willing to trade speed.

## Install from PyPI

```bash
pip install rns-page-node-pure
```

## Install from the RNS remote

With `pip-rns`:

```bash
pip-rns install --from-release rns://06a54b505bb67b25ef3f8097e8001edc/public/rns-page-node-pure --ref v1.7.0
```

With `rngit`:

```bash
rngit release rns://06a54b505bb67b25ef3f8097e8001edc/public/rns-page-node-pure fetch v1.7.0:all
pip install v1.7.0/rns_page_node_pure-1.7.0-py3-none-any.whl
```

The pure package has a separate RNS remote and package name because it depends on `rnspure` instead of `rns`. Do not install both packages into the same environment.

## Build a pure zipapp

From the repository root:

```bash
make pyz-pure
```

The output is `dist/rns-page-node-pure.pyz`. It contains `rnspure` and the node source and runs on any system with Python 3.10.

## Performance and security note

The pure backend is much slower than OpenSSL. It also uses crypto primitives implemented in Python instead of the OpenSSL primitives used by the standard package. Use the standard package unless the pure package is the only one that installs on your target.
