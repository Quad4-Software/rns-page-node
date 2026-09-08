# Install from Reticulum

rns-page-node is released over the Reticulum network through the same repository remote that hosts the source. If you already have a Reticulum transport, you can install a release wheel or clone the source without using PyPI or HTTPS git.

The canonical RNS remote for this repository is:

```text
rns://06a54b505bb67b25ef3f8097e8001edc/public/rns-page-node
```

You can also see it by running `git config --get remote.origin.url` in a checkout.

## What you need

- Python 3.10 or newer.
- A working Reticulum transport, such as `rnsd` or a shared bus interface.
- Either `pip-rns` or `rngit` installed.

## Install pip-rns or rngit

Both tools are optional bridges. `pip-rns` is the easiest way to install a Python package from an rngit release. `rngit` gives you lower-level release commands.

Install `pip-rns` from PyPI:

```bash
pip install pip-rns
```

Or install `rngit`:

```bash
pip install rngit
```

If you want a standalone zipapp, `pip-rns` and `opip` ship as `.pyz` files from the pip-rns repository. See the [offline guide](offline) for zipapp details.

## Install with pip-rns

`pip-rns` prefers a pre-built release wheel when one exists. It fetches the wheel over Reticulum, verifies the signature, and installs it with pip.

Install the latest release:

```bash
pip-rns install --from-release rns://06a54b505bb67b25ef3f8097e8001edc/public/rns-page-node
```

Pin a version:

```bash
pip-rns install --from-release rns://06a54b505bb67b25ef3f8097e8001edc/public/rns-page-node --ref v1.7.0
```

Install the pure variant from a release:

```bash
pip-rns install --from-release rns://06a54b505bb67b25ef3f8097e8001edc/public/rns-page-node-pure --ref v1.7.0
```

Install from source over the mesh, for example to track the master branch:

```bash
pip-rns install --from-source rns://06a54b505bb67b25ef3f8097e8001edc/public/rns-page-node --ref master
```

Source clones are larger than release wheels. Use a release wheel unless you need an unreleased change.

### Trust a release signer

`pip-rns` can remember the signer identity of the release so future installs fail closed if the signer changes.

```bash
pip-rns trust add rns://06a54b505bb67b25ef3f8097e8001edc/public/rns-page-node e46112d44649266d71fe2193e00a4710
```

Then install without passing `--verify` each time:

```bash
pip-rns install --from-release rns://06a54b505bb67b25ef3f8097e8001edc/public/rns-page-node --ref v1.7.0
```

The exact signer hash is printed with `pip-rns release view` after the release is fetched. Replace the example hash with the real one.

### Use an alias

If the remote path is long, save a short alias:

```bash
pip-rns alias add rns-page-node 06a54b505bb67b25ef3f8097e8001edc/public/rns-page-node
pip-rns install --from-release rns-page-node --ref v1.7.0
```

## Install with rngit

`rngit release` fetches signed artifacts from the remote. You can then install the wheel with `pip`.

List releases:

```bash
rngit release rns://06a54b505bb67b25ef3f8097e8001edc/public/rns-page-node list
```

View a release and its signer:

```bash
rngit release rns://06a54b505bb67b25ef3f8097e8001edc/public/rns-page-node view v1.7.0
```

Fetch the release artifacts into the current directory:

```bash
rngit release rns://06a54b505bb67b25ef3f8097e8001edc/public/rns-page-node fetch v1.7.0:all
```

This creates a `v1.7.0` directory with the signed wheel, manifest, and any other artifacts. Verify the signature:

```bash
rngit release v1.7.0/manifest.rsm verify
```

Then install the wheel:

```bash
pip install v1.7.0/rns_page_node-1.7.0-py3-none-any.whl
```

For the pure variant, fetch and install the pure wheel:

```bash
rngit release rns://06a54b505bb67b25ef3f8097e8001edc/public/rns-page-node-pure fetch v1.7.0:all
pip install v1.7.0/rns_page_node_pure-1.7.0-py3-none-any.whl
```

## Clone the source with git

You can also clone the repository directly over Reticulum:

```bash
git clone rns://06a54b505bb67b25ef3f8097e8001edc/public/rns-page-node
```

Then install in editable mode:

```bash
cd rns-page-node
pip install -e .
```

Cloning is the most expensive option in terms of Reticulum traffic. Use a release wheel or a source install from `pip-rns` for a lighter transfer.
