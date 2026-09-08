# Configuration

Values are resolved in this order:

1. Command line flag.
2. Environment variable.
3. Config file key.
4. Built-in default.

A value passed on the command line beats the same value from the config file. A config file value beats the default.

## Config file format

The file is plain text. Each line is a `key=value` pair. Lines starting with `#` are comments. Empty lines are ignored.

A minimal config file:

```text
# rns-page-node configuration file
# Lines starting with # are comments
# Format: key=value

# Node display name
node-name=My Page Node

# Directories
pages-dir=./pages
files-dir=./files
media-dir=./media
identity-dir=./node-config

# Announce interval in minutes (default: 360 = 6 hours)
announce-interval=360

# Page refresh interval in seconds (0 = disabled)
page-refresh-interval=300

# File refresh interval in seconds (0 = disabled)
file-refresh-interval=300

# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
log-level=INFO
```

You can find a working example in the repository at `config.example`.

## CLI flags and environment variables

| Config key | CLI flag | Environment variable | Default | Notes |
| --- | --- | --- | --- | --- |
| `reticulum-config` | `-c`, `--config` | none | none | Path to Reticulum config. |
| `pages-dir` | `-p`, `--pages-dir` | none | `./pages` | Directory of Micron pages. |
| `files-dir` | `-f`, `--files-dir` | none | `./files` | Directory of files to serve. |
| `media-dir` | `-m`, `--media-dir` | `RNS_PAGE_NODE_MEDIA_DIR` | same as pages-dir | WebP images for `/media/`. |
| `node-name` | `-n`, `--node-name` | none | none | Human-readable name in announces. |
| `announce-interval` | `-a`, `--announce-interval` | none | `360` | Minutes between announces. |
| `identity-dir` | `-i`, `--identity-dir` | none | `./node-config` | Where the node identity is stored. |
| `page-refresh-interval` | `--page-refresh-interval` | none | `0` | Seconds between page rescans, 0 disables. |
| `file-refresh-interval` | `--file-refresh-interval` | none | `0` | Seconds between file rescans, 0 disables. |
| `log-level` | `-l`, `--log-level` | none | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`. |

## Passing a config file on the command line

The first positional argument is the path to a config file.

```bash
rns-page-node myconfig.conf
```

You can still override a single value with a flag:

```bash
rns-page-node myconfig.conf --log-level DEBUG
```

## Environment variables

The only environment variable with a special name is `RNS_PAGE_NODE_MEDIA_DIR`. It sets the media directory if no `--media-dir` flag is given. It is checked before the config file.

Other settings do not use a prefix. They are read as plain keys, but the CLI flags are the usual way to set them.

## Multiple ways to set the same thing

This command sets the media directory with a flag:

```bash
rns-page-node -m ./media
```

This command sets it through the config file:

```text
media-dir=./media
```

And this sets it through the environment:

```bash
export RNS_PAGE_NODE_MEDIA_DIR=./media
rns-page-node
```

Only the first source in the precedence order is used for each setting.
