"""Command-line entry point: parses arguments, calls the domain, prints."""

import argparse
from collections.abc import Sequence
from importlib.metadata import version

from python_prj_seed.domain import greet


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python-prj-seed",
        description="Print a greeting.",
    )
    parser.add_argument(
        "name", nargs="?", default="world", help="who to greet (default: world)"
    )
    parser.add_argument(
        "--version", action="version", version=version("python-prj-seed")
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return its exit code.

    `argv` defaults to `sys.argv[1:]`; tests pass it explicitly.
    """
    args = build_parser().parse_args(argv)
    print(greet(args.name))
    return 0
