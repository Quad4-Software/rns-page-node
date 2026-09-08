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

## Run from a zipapp

If you built the offline zipapp, run it with `python3`:

```bash
python3 dist/rns-page-node.pyz
```

The same flags and config file work:

```bash
python3 dist/rns-page-node.pyz myconfig.conf --log-level DEBUG
```

## Pages

Put Micron pages in the pages directory. The file `index.mu` becomes the home page at `/page/index.mu`. Subdirectories work and are mapped under the page route.

Executable `.mu` files are run as scripts. The node passes the request data as environment variables such as `var_action`, `field_message` and `field_username`. The script writes its response to stdout.

A simple static `index.mu` looks like this:

```text
# Welcome

This is the home page of the node.
```

A dynamic `index.mu` can read environment variables:

```bash
#!/bin/bash
echo "# Hello"
echo "Action: $var_action"
```

Make the script executable and request it from a client. The node runs it and returns the stdout as the page body.

## Files

Put any file in the files directory. Files are served under the `/file/` route and are automatically compressed if they are larger than 32 MB.

A file at `files/manual.pdf` is requested as `/file/manual.pdf`.

## Media

NomadNet 1.4.x requests images through the `/media/` route. Put WebP images in the media directory and request them with a `path` and `key` dictionary.

A media request from a client looks like this:

```json
{
  "path": "logo.webp",
  "key": "site"
}
```

The file `media/logo.webp` is returned. If no media directory is set, the pages directory is used.

## View the node with NomadNet

After the node announces, you can browse its pages and files with a NomadNet client. Open the page destination and go to `/page/index.mu`, `/file/<name>` or `/media/<name>` as needed.

The node address is printed on startup. You can also find it by looking at the announced destination in the Reticulum log.

## Stop the node

Press `Ctrl-C`. The node shuts down its announce and refresh threads cleanly.

## Running as a long-lived service

For a daemon, run the node under a process supervisor such as `systemd`, `runit`, or `supervisord`. The node does not daemonise itself. A minimal `systemd` service file might look like this:

```text
[Unit]
Description=rns-page-node

[Service]
Type=simple
WorkingDirectory=/var/lib/rns-page-node
ExecStart=/usr/local/bin/rns-page-node /etc/rns-page-node.conf
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Adjust the working directory, config path and user to match your system.
