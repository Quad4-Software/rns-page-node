# Offline zipapp

A zipapp is a single `.pyz` file that contains the package and its dependencies. It runs with Python and needs no separate installation step. This is useful on air-gapped systems or on machines without pip.

## Build the standard zipapp

From the repository root:

```bash
make pyz
```

The output is `dist/rns-page-node.pyz`.

## Build the pure zipapp

```bash
make pyz-pure
```

The output is `dist/rns-page-node-pure.pyz`.

## Run a zipapp

```bash
python3 dist/rns-page-node.pyz
```

You can pass the same flags and config file as the installed command:

```bash
python3 dist/rns-page-node.pyz myconfig.conf --log-level DEBUG
```

## Platform limits

The standard zipapp includes `cryptography`, which contains native code compiled for the platform that built the zipapp. Run it on the same architecture, Python version and libc. The pure zipapp contains only Python code and is portable to any platform that runs Python 3.10.
