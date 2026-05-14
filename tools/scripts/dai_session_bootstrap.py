#!/usr/bin/env python3
"""Print the default startup context for a new DAI session."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LOCAL_MEMBER_FILE = ROOT / ".dai-local" / "active-member.txt"

MEMBERS = {
    "dana": ROOT / "members" / "dana" / "member-context.md",
    "jacob": ROOT / "members" / "jacob" / "member-context.md",
    "johann": ROOT / "members" / "johann" / "member-context.md",
    "julio": ROOT / "members" / "julio" / "member-context.md",
    "matt": ROOT / "members" / "matt" / "member-context.md",
    "mike": ROOT / "members" / "mike" / "member-context.md",
    "nathan": ROOT / "members" / "nathan" / "member-context.md",
}

STARTUP_FILES = [
    ("active-work-map", ROOT / "active-work-map.md"),
    ("operating-principles", ROOT / "core" / "operating-principles.md"),
    ("preferences", ROOT / "memory" / "preferences.md"),
    ("identity", ROOT / "memory" / "identity.md"),
    ("current-focus", ROOT / "memory" / "current-focus.md"),
]


def resolve_member() -> tuple[str, str]:
    if LOCAL_MEMBER_FILE.exists():
        name = LOCAL_MEMBER_FILE.read_text(encoding="utf-8").strip().lower()
        if name in MEMBERS:
            return name, "local machine identity"
    return "jacob", "repo default"


def main() -> int:
    member, source = resolve_member()
    member_path = MEMBERS[member]

    print("DAI session bootstrap")
    print("")
    print(f"active member: {member}")
    print(f"identity source: {source}")
    print("")
    print("startup files:")
    print(f"  member-context: {member_path}")
    for label, path in STARTUP_FILES:
        print(f"  {label}: {path}")
    print("")
    print("startup order:")
    print("  1. member-context")
    print("  2. active-work-map")
    print("  3. operating-principles")
    print("  4. preferences")
    print("  5. identity")
    print("  6. current-focus")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
