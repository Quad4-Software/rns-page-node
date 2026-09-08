# rns-page-node-pure

This is the pure Python variant of [rns-page-node](https://github.com/Quad4-Software/rns-page-node). It contains the same source code as the standard package, but depends on `rnspure` instead of `rns` and `cryptography`.

Install it when your target cannot install PyCA/cryptography. Reticulum will use its internal pure Python crypto backend when the OpenSSL backend is not available.

See the main repository for full documentation, usage and configuration.
