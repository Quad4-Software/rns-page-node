# Pure Python variant

The standard package depends on `rns`, which installs PyCA/cryptography. On some systems, cryptography cannot be installed because it needs a compiled wheel or a Rust compiler.

The `rns-page-node-pure` package depends on `rnspure` instead. The `rnspure` package contains the same Reticulum source as `rns`, but declares no compiled dependencies. When cryptography is not installed, Reticulum falls back to its internal pure Python crypto backend.

## When to use the pure package

- The target has no Rust compiler and no prebuilt cryptography wheel.
- You are running on an unusual architecture.
- You want the smallest dependency tree and are willing to trade speed.

## How to install

```bash
pip install rns-page-node-pure
```

## Performance and security note

The pure backend is much slower than OpenSSL. It also uses crypto primitives implemented in Python instead of the OpenSSL primitives used by the standard package. Use the standard package unless the pure package is the only one that installs on your target.
