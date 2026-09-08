"""Minimal Reticulum Page Node entry point."""

import time
from pathlib import Path

import RNS

from .cli import get_config_value, setup_logging, setup_parser
from .config import load_config
from .core import PageNode


def main() -> None:
    """Run the RNS page node application."""
    parser = setup_parser()
    args = parser.parse_args()

    config = {}
    if args.node_config:
        config = load_config(args.node_config)

    configpath = get_config_value(args.configpath, None, "reticulum-config", config)
    pages_dir = get_config_value(
        args.pages_dir,
        str(Path.cwd() / "pages"),
        "pages-dir",
        config,
    )
    files_dir = get_config_value(
        args.files_dir,
        str(Path.cwd() / "files"),
        "files-dir",
        config,
    )
    media_dir = get_config_value(
        args.media_dir,
        None,
        "media-dir",
        config,
        env="RNS_PAGE_NODE_MEDIA_DIR",
    )
    if not media_dir:
        media_dir = pages_dir
    node_name = get_config_value(args.node_name, None, "node-name", config)
    announce_interval = get_config_value(
        args.announce_interval,
        360,
        "announce-interval",
        config,
        int,
    )
    identity_dir = get_config_value(
        args.identity_dir,
        str(Path.cwd() / "node-config"),
        "identity-dir",
        config,
    )
    page_refresh_interval = get_config_value(
        args.page_refresh_interval,
        0,
        "page-refresh-interval",
        config,
        int,
    )
    file_refresh_interval = get_config_value(
        args.file_refresh_interval,
        0,
        "file-refresh-interval",
        config,
        int,
    )
    log_level = get_config_value(args.log_level, "INFO", "log-level", config)

    setup_logging(log_level)

    RNS.Reticulum(configpath)
    Path(identity_dir).mkdir(parents=True, exist_ok=True)
    identity_file = Path(identity_dir) / "identity"
    if identity_file.is_file():
        identity = RNS.Identity.from_file(str(identity_file))
    else:
        identity = RNS.Identity()
        identity.to_file(str(identity_file))

    Path(pages_dir).mkdir(parents=True, exist_ok=True)
    Path(files_dir).mkdir(parents=True, exist_ok=True)
    Path(media_dir).mkdir(parents=True, exist_ok=True)

    node = PageNode(
        identity,
        pages_dir,
        files_dir,
        media_dir,
        announce_interval,
        node_name,
        page_refresh_interval,
        file_refresh_interval,
    )
    RNS.log("Page node running. Press Ctrl-C to exit.", RNS.LOG_INFO)
    RNS.log(f"Node address: {RNS.prettyhexrep(node.destination.hash)}", RNS.LOG_INFO)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        RNS.log("Keyboard interrupt received, shutting down...", RNS.LOG_INFO)
        node.shutdown()


if __name__ == "__main__":
    main()
