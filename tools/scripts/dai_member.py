#!/usr/bin/env python3
"""Manage the local active member identity for this shared DAI repo."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LOCAL_DIR = ROOT / ".dai-local"
ACTIVE_MEMBER_FILE = LOCAL_DIR / "active-member.txt"

MEMBERS = {
    "dana": ROOT / "members" / "dana" / "member-context.md",
    "jacob": ROOT / "members" / "jacob" / "member-context.md",
    "johann": ROOT / "members" / "johann" / "member-context.md",
    "julio": ROOT / "members" / "julio" / "member-context.md",
    "matt": ROOT / "members" / "matt" / "member-context.md",
    "mike": ROOT / "members" / "mike" / "member-context.md",
    "nathan": ROOT / "members" / "nathan" / "member-context.md",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Manage the local active member identity for DAI."
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("show", help="Print the locally configured active member.")
    subparsers.add_parser("list", help="List valid member names.")

    set_parser = subparsers.add_parser("set", help="Set the active member for this machine.")
    set_parser.add_argument("name", choices=sorted(MEMBERS))

    clear_parser = subparsers.add_parser("clear", help="Remove the local active member.")
    clear_parser.add_argument(
        "--quiet",
        action="store_true",
        help="Do not print a confirmation message.",
    )

    path_parser = subparsers.add_parser(
        "path", help="Print the member context path for the active or specified member."
    )
    path_parser.add_argument("name", nargs="?", choices=sorted(MEMBERS))

    return parser.parse_args()


def read_active_member() -> str | None:
    if not ACTIVE_MEMBER_FILE.exists():
        return None
    value = ACTIVE_MEMBER_FILE.read_text(encoding="utf-8").strip().lower()
    return value or None


def write_active_member(name: str) -> None:
    LOCAL_DIR.mkdir(parents=True, exist_ok=True)
    ACTIVE_MEMBER_FILE.write_text(f"{name}\n", encoding="utf-8")


def clear_active_member() -> None:
    if ACTIVE_MEMBER_FILE.exists():
        ACTIVE_MEMBER_FILE.unlink()


def main() -> int:
    args = parse_args()

    if args.command == "list":
        for name in sorted(MEMBERS):
            print(name)
        return 0

    if args.command == "set":
        write_active_member(args.name)
        print(f"active member set to {args.name}")
        print(MEMBERS[args.name])
        return 0

    if args.command == "clear":
        clear_active_member()
        if not args.quiet:
            print("cleared local active member")
        return 0

    if args.command == "path":
        name = args.name or read_active_member()
        if not name:
            print("error: no local active member is set", file=sys.stderr)
            return 1
        print(MEMBERS[name])
        return 0

    active_member = read_active_member()
    if args.command in (None, "show"):
        if active_member:
            print(active_member)
            print(MEMBERS[active_member])
            return 0
        print("unset")
        return 0

    print(f"error: unsupported command: {args.command}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
