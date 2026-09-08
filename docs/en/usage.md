# Usage

## Start a node

Run the node from a directory that has `pages`, `files` and `node-config` subdirectories, or pass explicit paths.

```bash
rns-page-node
```

The first run creates a new RNS identity in `node-config/identity` and announces the destination. The node address is printed in the log.

## Start with options

```bash
rns-page-node myconfig.conf \
  --pages-dir ./pages \
  --files-dir ./files \
  --media-dir ./media \
  --node-name "My Page Node" \
  --announce-interval 60 \
  --log-level DEBUG
```

## Pages

Put Micron pages in the pages directory. The file `index.mu` becomes the home page at `/page/index.mu`. Subdirectories work and are mapped under the page route.

Executable `.mu` files are run as scripts. The node passes the request data as environment variables such as `var_action`, `field_message` and `field_username`. The script writes its response to stdout.

## Files

Put any file in the files directory. Files are served under the `/file/` route and are automatically compressed if they are larger than 32 MB.

## Media

NomadNet 1.4.x requests images through the `/media/` route. Put WebP images in the media directory and request them with a `path` and `key` dictionary.

If no media directory is set, the pages directory is used.

## Stop the node

Press `Ctrl-C`. The node shuts down its announce and refresh threads cleanly.
