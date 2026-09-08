"""CLI argument parsing and logging configuration for rns-page-node."""

import argparse
import os
from pathlib import Path
from typing import Optional, Type, TypeVar

import RNS

T = TypeVar("T")


def setup_parser() -> argparse.ArgumentParser:
    """Initialize and return the argument parser.

    Returns:
        Configured ArgumentParser instance

    """
    parser = argparse.ArgumentParser(
        prog="rns-page-node",
        description="Minimal Reticulum Page Node",
    )
    parser.add_argument(
        "node_config",
        nargs="?",
        help="Path to rns-page-node config file",
        default=None,
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="configpath",
        help="Reticulum config path",
        default=None,
    )
    parser.add_argument(
        "-p",
        "--pages-dir",
        dest="pages_dir",
        help="Pages directory",
        default=str(Path.cwd() / "pages"),
    )
    parser.add_argument(
        "-f",
        "--files-dir",
        dest="files_dir",
        help="Files directory",
        default=str(Path.cwd() / "files"),
    )
    parser.add_argument(
        "-m",
        "--media-dir",
        dest="media_dir",
        help="Media directory for images, defaults to pages directory",
        default=None,
    )
    parser.add_argument(
        "-n",
        "--node-name",
        dest="node_name",
        help="Node display name",
        default=None,
    )
    parser.add_argument(
        "-a",
        "--announce-interval",
        dest="announce_interval",
        type=int,
        help="Announce interval in minutes",
        default=360,
    )
    parser.add_argument(
        "-i",
        "--identity-dir",
        dest="identity_dir",
        help="Directory to store node identity",
        default=str(Path.cwd() / "node-config"),
    )
    parser.add_argument(
        "--page-refresh-interval",
        dest="page_refresh_interval",
        type=int,
        default=0,
        help="Page refresh interval in seconds, 0 disables auto-refresh",
    )
    parser.add_argument(
        "--file-refresh-interval",
        dest="file_refresh_interval",
        type=int,
        default=0,
        help="File refresh interval in seconds, 0 disables auto-refresh",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        dest="log_level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level",
    )
    return parser


def get_config_value(
    arg_value: T,
    arg_default: T,
    config_key: str,
    config: dict[str, str],
    value_type: Type[T] = str,
    env: Optional[str] = None,
) -> T:
    """Get value from CLI args, environment, config file, or default.

    Priority: CLI arg > environment > config file > default

    Args:
        arg_value: Value from command line argument
        arg_default: Default value for the argument
        config_key: Key in the configuration dictionary
        config: Configuration dictionary
        value_type: Expected type of the value
        env: Optional environment variable name

    Returns:
        The resolved value

    """
    if arg_value != arg_default:
        return arg_value
    if env and env in os.environ:
        env_value = os.environ[env]
        try:
            if value_type is int:
                return int(env_value)  # type: ignore
            return env_value  # type: ignore
        except (ValueError, TypeError):
            RNS.log(
                f"Invalid {value_type.__name__} value for {env}: {env_value}",
                RNS.LOG_WARNING,
            )
    if config_key in config:
        try:
            if value_type is int:
                return int(config[config_key])  # type: ignore
            return config[config_key]  # type: ignore
        except (ValueError, TypeError):
            RNS.log(
                f"Invalid {value_type.__name__} value for {config_key}: {config[config_key]}",
                RNS.LOG_WARNING,
            )
    return arg_default


def setup_logging(log_level: str) -> None:
    """Configure RNS logging level.

    Args:
        log_level: String representation of the log level

    """
    log_level_map = {
        "CRITICAL": RNS.LOG_CRITICAL,
        "ERROR": RNS.LOG_ERROR,
        "WARNING": RNS.LOG_WARNING,
        "INFO": RNS.LOG_INFO,
        "DEBUG": RNS.LOG_DEBUG,
    }
    RNS.loglevel = log_level_map.get(log_level.upper(), RNS.LOG_INFO)
