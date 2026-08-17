"""Entry point for the `browserpom` command-line tool."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from BrowserPOM.cli.config import load
from BrowserPOM.cli.exceptions import BrowserPOMCLIError
from BrowserPOM.cli.formatting import format_pageobject, format_uiobject
from BrowserPOM.cli.scanner import Scanner


def cmd_discover_pages(_args: argparse.Namespace) -> None:
    """Run `browserpom discover pages`, raising domain exceptions on failure."""
    config = load()
    scanner = Scanner(Path.cwd(), config.paths)
    pages = scanner.scan_pages()
    blocks = [format_pageobject(page, Path.cwd()) for page in pages]
    if blocks:
        print("\n\n".join(blocks))  # noqa: T201


def cmd_discover_objects(_args: argparse.Namespace) -> None:
    """Run `browserpom discover objects`, raising domain exceptions on failure."""
    config = load()
    scanner = Scanner(Path.cwd(), config.paths)
    classes = scanner.scan()
    blocks = [format_uiobject(cls, Path.cwd()) for cls in classes]
    print("\n\n".join(blocks))  # noqa: T201


def build_parser() -> argparse.ArgumentParser:
    """Build and return the top-level argument parser."""
    parser = argparse.ArgumentParser(
        prog="browserpom",
        description="CLI tools for robotframework-browserpom.",
    )
    sub = parser.add_subparsers(dest="command")

    discover = sub.add_parser("discover", help="Discover PageObjects and UIObjects.")
    discover_sub = discover.add_subparsers(dest="subcommand")

    discover_sub.add_parser("pages", help="List all PageObjects.")
    discover_sub.add_parser("objects", help="List all UIObject subclasses.")

    return parser


def main(argv: list[str] | None = None) -> None:
    """Entry point for the `browserpom` console script."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "discover":
            if args.subcommand == "pages":
                cmd_discover_pages(args)
            elif args.subcommand == "objects":
                cmd_discover_objects(args)
            else:
                parser.parse_args(["discover", "--help"])
        else:
            parser.print_help()
    except BrowserPOMCLIError as exc:
        print(str(exc), file=sys.stderr)  # noqa: T201
        raise SystemExit(1) from exc
