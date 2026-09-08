# Configuration

Values are resolved in this order:

1. Command line flag.
2. Environment variable.
3. Config file key.
4. Built-in default.

## Config file format

The file is plain text. Each line is a `key=value` pair. Lines starting with `#` are comments. Empty lines are ignored.

```text
reticulum-config=~/.reticulum
pages-dir=./pages
files-dir=./files
media-dir=./media
node-name=My Page Node
announce-interval=360
log-level=INFO
```

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
