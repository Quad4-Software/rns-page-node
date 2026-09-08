#!/usr/bin/env python3
"""Generate shell completion scripts for rns-page-node."""

import shtab

from rns_page_node.cli import setup_parser


def main() -> None:
    parser = setup_parser()
    parser.prog = "rns-page-node"
    output_dir = "completions"
    shells = {
        "bash": "rns-page-node.bash",
        "zsh": "_rns-page-node",
        "fish": "rns-page-node.fish",
        "tcsh": "rns-page-node.csh",
        "powershell": "rns-page-node.ps1",
    }
    for shell, filename in shells.items():
        completion = shtab.complete(parser, shell=shell)
        with open(f"{output_dir}/{filename}", "w", encoding="utf-8") as f:
            f.write(completion)


if __name__ == "__main__":
    main()
