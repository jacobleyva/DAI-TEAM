#!/usr/bin/env python3
"""eval_templates.py — structural evaluation of templates/*.md

What this does:
    Walks the workspace's templates/ directory and verifies that each
    template file meets baseline structural rules. This is not a render
    engine — templates here are markdown skeletons, not Jinja templates.
    The "eval" is whether each template, considered as a reusable
    structure, satisfies the workspace's conventions.

Checks per template:
    1. File starts with YAML frontmatter (delimited by --- / ---).
    2. Frontmatter contains: title, type, status, updated.
    3. Body (post-frontmatter) contains at least one ## heading.
    4. Body contains at least one bullet list OR table.
    5. (Optional) If templates/golden/{name}.expected.md exists, the
       template's normalized structure matches the golden file's
       normalized structure.

Output:
    Per-template PASS / FAIL with reason. Exit code 1 if any FAIL.

Usage:
    tools/scripts/eval_templates.py
    tools/scripts/eval_templates.py --templates-dir templates
    tools/scripts/eval_templates.py --quiet  # only print failures

This is the deterministic Codex-side equivalent of "tests for prompts":
templates are reused across the team, drift silently, and a single broken
template can corrupt every artifact it produces.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_FRONTMATTER_FIELDS = ["title", "type", "status", "updated"]


def find_workspace_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(8):
        if (cur / "LAUNCHER.md").exists() and (cur / "core").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    raise SystemExit(f"could not find workspace root from {start}")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Return (frontmatter_dict, body). Empty dict if no frontmatter."""
    if not text.startswith("---\n"):
        return {}, text
    end_match = re.search(r"\n---\s*(\n|$)", text[4:])
    if not end_match:
        return {}, text
    raw = text[4 : 4 + end_match.start()]
    body_start = 4 + end_match.end()
    fields: dict[str, str] = {}
    for line in raw.splitlines():
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return fields, text[body_start:]


def check_template(path: Path) -> list[str]:
    """Return a list of failure reasons; empty list = PASS."""
    failures: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        return [f"could not read file: {exc}"]

    fm, body = parse_frontmatter(text)
    if not fm:
        failures.append("missing YAML frontmatter")

    for field in REQUIRED_FRONTMATTER_FIELDS:
        if field not in fm:
            failures.append(f"frontmatter missing required field: {field}")

    if not re.search(r"^## ", body, flags=re.MULTILINE):
        failures.append("body has no '## ' heading")

    has_bullet = bool(re.search(r"^- ", body, flags=re.MULTILINE))
    has_table = bool(re.search(r"^\|", body, flags=re.MULTILINE))
    if not (has_bullet or has_table):
        failures.append("body has neither a bullet list nor a table")

    return failures


def normalize_structure(text: str) -> str:
    """Reduce a template to its structural skeleton for golden-file comparison."""
    _, body = parse_frontmatter(text)
    lines = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            lines.append(f"HEADING2:{stripped[3:].lower()}")
        elif stripped.startswith("### "):
            lines.append(f"HEADING3:{stripped[4:].lower()}")
        elif stripped.startswith("- "):
            lines.append("BULLET")
        elif stripped.startswith("|"):
            lines.append("TABLE_ROW")
    return "\n".join(lines)


def check_golden(template_path: Path, golden_dir: Path) -> list[str]:
    name = template_path.stem
    golden = golden_dir / f"{name}.expected.md"
    if not golden.exists():
        return []
    actual = normalize_structure(template_path.read_text(encoding="utf-8"))
    expected = normalize_structure(golden.read_text(encoding="utf-8"))
    if actual != expected:
        return [f"structural drift vs {golden.relative_to(golden_dir.parent.parent)}"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Structural evaluation of templates.")
    parser.add_argument("--templates-dir", default="templates")
    parser.add_argument("--quiet", action="store_true", help="print only failures + final summary")
    args = parser.parse_args()

    root = find_workspace_root(Path(__file__).parent)
    templates_dir = root / args.templates_dir
    golden_dir = templates_dir / "golden"

    if not templates_dir.is_dir():
        print(f"templates directory not found: {templates_dir}", file=sys.stderr)
        return 1

    templates = sorted(
        p for p in templates_dir.glob("*.md")
        if p.name != "templates-map.md" and not p.name.startswith(".")
    )

    if not templates:
        print(f"no templates found in {templates_dir}")
        return 0

    total = len(templates)
    failed = 0

    for path in templates:
        failures = check_template(path)
        failures.extend(check_golden(path, golden_dir))
        rel = path.relative_to(root)
        if failures:
            failed += 1
            print(f"FAIL  {rel}")
            for reason in failures:
                print(f"        - {reason}")
        elif not args.quiet:
            print(f"PASS  {rel}")

    print()
    print(f"templates: {total} | passed: {total - failed} | failed: {failed}")
    return 1 if failed > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
