#!/usr/bin/env python3
"""Lightweight navigation helper for the shared DAI."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

MAPS = {
    "overview": ROOT / "dai-overview.md",
    "active": ROOT / "active-work-map.md",
    "team": ROOT / "team" / "team-map.md",
    "members": ROOT / "members" / "members-map.md",
    "memory": ROOT / "memory" / "memory-map.md",
    "projects": ROOT / "projects" / "projects-map.md",
    "skills": ROOT / "skills" / "skills-map.md",
    "knowledge": ROOT / "knowledge" / "knowledge-map.md",
    "automations": ROOT / "automations" / "automations-index.md",
}

MEMBERS = {
    "nathan": ROOT / "members" / "nathan" / "member-context.md",
    "mike": ROOT / "members" / "mike" / "member-context.md",
    "johann": ROOT / "members" / "johann" / "member-context.md",
    "dana": ROOT / "members" / "dana" / "member-context.md",
    "jacob": ROOT / "members" / "jacob" / "member-context.md",
    "matt": ROOT / "members" / "matt" / "member-context.md",
    "julio": ROOT / "members" / "julio" / "member-context.md",
}

PROJECTS = {
    "fiserv": ROOT / "projects" / "fiserv-api-servicenow" / "fiserv-api-servicenow-project.md",
    "fiserv-api-servicenow": ROOT / "projects" / "fiserv-api-servicenow" / "fiserv-api-servicenow-project.md",
    "servicenow-core": ROOT / "projects" / "servicenow-core" / "servicenow-core-project.md",
    "dai-setup": ROOT / "projects" / "dai-setup" / "dai-setup-project.md",
}

TEAM = {
    "roster": ROOT / "team" / "roster.md",
    "collaboration": ROOT / "team" / "collaboration-model.md",
    "azure-devops": ROOT / "team" / "azure-devops-conventions.md",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Navigate the shared DAI structure.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("root", help="Print the DAI root path.")
    subparsers.add_parser("list", help="List the main navigation targets.")

    map_parser = subparsers.add_parser("map", help="Print a shared map file path.")
    map_parser.add_argument("name", choices=sorted(MAPS))

    member_parser = subparsers.add_parser("member", help="Print a member workspace path.")
    member_parser.add_argument("name", choices=sorted(MEMBERS))

    project_parser = subparsers.add_parser("project", help="Print a project entry path.")
    project_parser.add_argument("name", choices=sorted(PROJECTS))

    team_parser = subparsers.add_parser("team", help="Print a shared team doc path.")
    team_parser.add_argument("name", choices=sorted(TEAM))

    return parser.parse_args()


def print_list() -> None:
    print(f"root: {ROOT}")
    print("")
    print("maps:")
    for name, path in sorted(MAPS.items()):
        print(f"  {name}: {path}")
    print("")
    print("members:")
    for name, path in sorted(MEMBERS.items()):
        print(f"  {name}: {path}")
    print("")
    print("projects:")
    for name, path in sorted(PROJECTS.items()):
        print(f"  {name}: {path}")
    print("")
    print("team:")
    for name, path in sorted(TEAM.items()):
        print(f"  {name}: {path}")


def main() -> int:
    args = parse_args()
    if args.command in (None, "list"):
        print_list()
        return 0
    if args.command == "root":
        print(ROOT)
        return 0
    if args.command == "map":
        print(MAPS[args.name])
        return 0
    if args.command == "member":
        print(MEMBERS[args.name])
        return 0
    if args.command == "project":
        print(PROJECTS[args.name])
        return 0
    if args.command == "team":
        print(TEAM[args.name])
        return 0
    print(f"error: unsupported command: {args.command}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
