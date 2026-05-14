#!/usr/bin/env python3
"""Search local knowledge collections quickly."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


DEFAULT_COLLECTIONS_ROOT = Path(__file__).resolve().parents[2] / "knowledge" / "collections"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search DAI knowledge collections.")
    parser.add_argument("query", help="Text or regex to search for.")
    parser.add_argument(
        "--root",
        default=str(DEFAULT_COLLECTIONS_ROOT),
        help="Knowledge collections root.",
    )
    parser.add_argument("--collection", help="Only search one collection by name.")
    parser.add_argument("--context", type=int, default=2, help="Context lines for matches.")
    parser.add_argument("--files-only", action="store_true", help="Only print matching file paths.")
    parser.add_argument("--json", action="store_true", help="Return results as JSON.")
    return parser.parse_args()


def build_search_root(root: Path, collection: str | None) -> Path:
    return (root / collection) if collection else root


def run_rg(search_root: Path, query: str, files_only: bool, context: int) -> subprocess.CompletedProcess:
    cmd = ["rg", "--glob", "*.md", query, str(search_root)]
    if files_only:
        cmd = ["rg", "-l", "--glob", "*.md", query, str(search_root)]
    else:
        cmd = ["rg", "-n", "-C", str(context), "--glob", "*.md", query, str(search_root)]
    return subprocess.run(cmd, capture_output=True, text=True)


def collect_manifest_hits(search_root: Path) -> list[dict]:
    manifests = sorted(search_root.glob('*/manifest.json')) if search_root.name == 'collections' else [search_root / 'manifest.json']
    data = []
    for manifest in manifests:
        if manifest.exists():
            try:
                data.append({"manifest": str(manifest), "entries": json.loads(manifest.read_text())})
            except Exception:
                continue
    return data


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    search_root = build_search_root(root, args.collection)
    if not search_root.exists():
        print(f"error: search root not found: {search_root}", file=sys.stderr)
        return 1

    result = run_rg(search_root, args.query, args.files_only, args.context)
    if args.json:
        payload = {
            "query": args.query,
            "root": str(search_root),
            "files_only": args.files_only,
            "stdout": result.stdout,
            "returncode": result.returncode,
            "manifests": collect_manifest_hits(search_root),
        }
        print(json.dumps(payload, indent=2))
        return 0 if result.returncode in (0, 1) else result.returncode

    if result.stdout:
        print(result.stdout, end="")
    if result.returncode not in (0, 1):
        print(result.stderr, file=sys.stderr, end="")
        return result.returncode
    if result.returncode == 1:
        print("No matches found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
