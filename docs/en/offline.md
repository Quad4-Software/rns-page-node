# Offline install and zipapps

A zipapp is a single `.pyz` file that contains the package and its dependencies. It runs with Python and needs no separate installation step. This is useful on air-gapped systems or on machines without pip.

The repository also supports `opip` offline bundles and `pip-rns export` for mirroring a release to removable media.

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

## Install from a local wheel offline

If you have a wheel and its dependencies mirrored, pip can install it without reaching the network:

```bash
pip install --no-index --find-links ./wheels rns_page_node-1.7.0-py3-none-any.whl
```

The `./wheels` directory must contain `rns-page-node` and its dependencies: `rns`, `cryptography` and `pyserial`. For the pure variant, only `rnspure` is needed.

## Mirror a release for USB or air-gap with pip-rns

`pip-rns export` downloads a release and its wheels to a local directory. You can copy that directory to a USB drive or another machine.

```bash
pip-rns export rns://06a54b505bb67b25ef3f8097e8001edc/public/rns-page-node \
  --ref v1.7.0 -o /media/usb/rns-page-node
```

The export contains the signed wheel and manifest. To install on the offline machine:

```bash
pip-rns bundle install /media/usb/rns-page-node/rns_page_node-1.7.0-py3-none-any.whl
```

## Build an opip bundle

`opip` is a separate tool that builds and installs offline wheel bundles. It is part of the `pip-rns` package. If you already have `pip-rns` installed, `opip` is available.

Create a bundle from a requirements file or a wheel:

```bash
opip create -r requirements.txt -o ./rns-page-node.opip
```

Verify and install the bundle offline:

```bash
opip verify ./rns-page-node.opip --require-signature
opip install ./rns-page-node.opip
```

## Platform limits

The standard zipapp includes `cryptography`, which contains native code compiled for the platform that built the zipapp. Run it on the same architecture, Python version and libc. The pure zipapp contains only Python code and is portable to any platform that runs Python 3.10.
