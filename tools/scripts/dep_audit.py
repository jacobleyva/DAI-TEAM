#!/usr/bin/env python3
"""dep_audit.py — run available dependency auditors and write a structured report.

What this does:
    Walks the workspace for known dependency manifests (requirements.txt,
    pyproject.toml, package.json, Cargo.toml, go.mod, Gemfile), runs the
    matching auditor when its CLI is available on PATH, and writes a
    Markdown report to memory/security/dependency-findings.md.

    Designed to be safe and non-fatal: a missing auditor produces a "skipped"
    entry, not a crash. Designed to be runnable from a pre-commit context
    (fast or skip) and from bootstrap (full run on demand).

Supported manifests and the auditor used:
    - requirements.txt, pyproject.toml         → pip-audit
    - package.json                              → npm audit --json
    - Cargo.toml                                → cargo audit --json
    - go.mod                                    → govulncheck -json ./...
    - Gemfile                                   → bundler-audit --update

Usage:
    tools/scripts/dep_audit.py                  # full run, write report
    tools/scripts/dep_audit.py --check          # exit non-zero if HIGH/CRITICAL findings
    tools/scripts/dep_audit.py --quiet          # write report; no stdout per-manifest

Output:
    memory/security/dependency-findings.md

Exit codes:
    0  success (or --check ran with no HIGH/CRITICAL findings)
    1  workspace not detected, or --check found HIGH/CRITICAL
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def find_workspace_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(8):
        if (cur / "LAUNCHER.md").exists() and (cur / "core").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    raise SystemExit(f"could not find workspace root from {start}")


def find_manifests(root: Path) -> list[tuple[str, Path]]:
    """Return [(manifest_kind, path_to_manifest), ...]"""
    found: list[tuple[str, Path]] = []
    # Ignore vendored / cache / build directories
    ignore_parts = {"node_modules", ".venv", "venv", "__pycache__", "target", "vendor",
                    "dist", "build", ".processed", ".failed"}

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in ignore_parts for part in path.parts):
            continue
        name = path.name
        if name == "requirements.txt":
            found.append(("python-pip", path))
        elif name == "pyproject.toml":
            found.append(("python-pyproject", path))
        elif name == "package.json":
            found.append(("npm", path))
        elif name == "Cargo.toml":
            found.append(("cargo", path))
        elif name == "go.mod":
            found.append(("go", path))
        elif name == "Gemfile":
            found.append(("bundler", path))
    return found


def run_auditor(kind: str, manifest: Path, workspace_root: Path) -> dict:
    """Run the appropriate auditor; return a normalized result dict."""
    result = {
        "kind": kind,
        "manifest": str(manifest.relative_to(workspace_root)),
        "auditor": None,
        "available": False,
        "exit_code": None,
        "stdout": "",
        "stderr": "",
        "findings_count": 0,
        "severity_counts": {"critical": 0, "high": 0, "medium": 0, "low": 0, "unknown": 0},
    }

    auditors = {
        "python-pip":       ("pip-audit", ["pip-audit", "--requirement", str(manifest), "--format", "json"]),
        "python-pyproject": ("pip-audit", ["pip-audit", "--format", "json"]),
        "npm":              ("npm",       ["npm", "audit", "--json"]),
        "cargo":            ("cargo-audit", ["cargo", "audit", "--json"]),
        "go":               ("govulncheck", ["govulncheck", "-json", "./..."]),
        "bundler":          ("bundler-audit", ["bundler-audit", "check", "--update"]),
    }

    auditor_name, cmd = auditors[kind]
    result["auditor"] = auditor_name

    if shutil.which(cmd[0]) is None:
        return result
    result["available"] = True

    cwd = manifest.parent if kind in {"npm", "cargo", "go", "bundler", "python-pyproject"} else workspace_root
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=120)
        result["exit_code"] = proc.returncode
        result["stdout"] = proc.stdout[:8000]
        result["stderr"] = proc.stderr[:2000]
        # Best-effort parse for finding counts; auditors vary in JSON shape
        try:
            data = json.loads(proc.stdout) if proc.stdout.strip() else {}
            count, severities = _count_findings(kind, data)
            result["findings_count"] = count
            for sev, n in severities.items():
                if sev in result["severity_counts"]:
                    result["severity_counts"][sev] += n
                else:
                    result["severity_counts"]["unknown"] += n
        except (json.JSONDecodeError, ValueError):
            pass
    except subprocess.TimeoutExpired:
        result["stderr"] = "auditor timed out after 120s"
    except Exception as exc:
        result["stderr"] = f"auditor invocation error: {exc}"

    return result


def _count_findings(kind: str, data) -> tuple[int, dict]:
    """Best-effort finding count from per-auditor JSON shapes."""
    severities = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    if kind in ("python-pip", "python-pyproject"):
        deps = data.get("dependencies", []) if isinstance(data, dict) else []
        count = 0
        for dep in deps:
            for vuln in dep.get("vulns", []) or []:
                count += 1
                sev = (vuln.get("severity") or "unknown").lower()
                severities[sev] = severities.get(sev, 0) + 1
        return count, severities
    if kind == "npm":
        meta = data.get("metadata", {}).get("vulnerabilities", {}) if isinstance(data, dict) else {}
        for sev in ("critical", "high", "moderate", "low"):
            n = int(meta.get(sev, 0) or 0)
            key = "medium" if sev == "moderate" else sev
            severities[key] = n
        return sum(severities.values()), severities
    if kind == "cargo":
        vulns = data.get("vulnerabilities", {}).get("list", []) if isinstance(data, dict) else []
        return len(vulns), severities
    if kind == "go":
        return 0, severities  # govulncheck JSON is stream-shaped; do a coarse count if needed
    if kind == "bundler":
        return 0, severities  # bundler-audit doesn't emit JSON; left as text
    return 0, severities


def write_report(workspace_root: Path, results: list[dict]) -> Path:
    out_dir = workspace_root / "memory" / "security"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "dependency-findings.md"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines = [
        "---",
        "title: Dependency Findings",
        "type: security-memory",
        "domain: dai",
        "product: DAI",
        "audience: team",
        "owner: team",
        "status: active",
        f"updated: {now}",
        "tags:",
        "  - security",
        "  - dependencies",
        "  - audit",
        "  - auto-generated",
        "artifact_type: security-memory",
        "generated_by: tools/scripts/dep_audit.py",
        "warning: do-not-edit-by-hand",
        "---",
        "",
        "# Dependency Findings",
        "",
        f"_Generated by `tools/scripts/dep_audit.py` at {now}._",
        "_Do not edit by hand. Re-run the script to refresh._",
        "",
        "## Summary",
        "",
        "| Manifest | Kind | Auditor | Available | Findings | Critical | High | Medium | Low |",
        "|----------|------|---------|-----------|---------:|---------:|-----:|-------:|----:|",
    ]
    for r in results:
        s = r["severity_counts"]
        lines.append(
            f"| `{r['manifest']}` | {r['kind']} | {r['auditor']} | "
            f"{'yes' if r['available'] else 'no'} | {r['findings_count']} | "
            f"{s['critical']} | {s['high']} | {s['medium']} | {s['low']} |"
        )
    if not results:
        lines.append("| _(no manifests found)_ | | | | | | | | |")
    lines.append("")
    lines.append("## Per-manifest details")
    lines.append("")

    for r in results:
        lines.append(f"### `{r['manifest']}` — {r['kind']}")
        lines.append(f"- **Auditor:** `{r['auditor']}`  |  **Available:** {'yes' if r['available'] else 'no'}")
        if not r["available"]:
            lines.append("- **Status:** SKIPPED — auditor not installed. Install to enable this check.")
        else:
            lines.append(f"- **Exit code:** `{r['exit_code']}`  |  **Findings:** `{r['findings_count']}`")
            sev = r["severity_counts"]
            lines.append(f"- **Severities:** critical={sev['critical']} high={sev['high']} medium={sev['medium']} low={sev['low']} unknown={sev['unknown']}")
            if r["stderr"]:
                lines.append("- **Stderr (truncated):**")
                lines.append("")
                lines.append("```")
                lines.append(r["stderr"])
                lines.append("```")
        lines.append("")

    lines.append("## How to interpret")
    lines.append("")
    lines.append("- `Available: no` means the auditor CLI is not on PATH; install it to enable that manifest's check.")
    lines.append("- A CRITICAL or HIGH finding should be triaged immediately — open a WORK note and follow `skills/security-review/`.")
    lines.append("- Findings with `unknown` severity need manual classification from the auditor's full output.")
    lines.append("- Re-run after upgrading a flagged dependency to confirm the fix.")
    lines.append("")

    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Run dependency auditors and write a report.")
    parser.add_argument("--check", action="store_true",
                        help="Exit non-zero if any HIGH or CRITICAL findings are present.")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress per-manifest stdout; only write the report.")
    args = parser.parse_args()

    workspace = find_workspace_root(Path(__file__).parent)
    manifests = find_manifests(workspace)
    if not args.quiet:
        print(f"workspace: {workspace}")
        print(f"manifests found: {len(manifests)}")

    results = []
    for kind, manifest in manifests:
        if not args.quiet:
            print(f"  auditing {kind}: {manifest.relative_to(workspace)}")
        results.append(run_auditor(kind, manifest, workspace))

    out = write_report(workspace, results)
    if not args.quiet:
        print(f"wrote {out.relative_to(workspace)}")

    if args.check:
        bad = sum(r["severity_counts"]["critical"] + r["severity_counts"]["high"] for r in results)
        if bad > 0:
            print(f"--check: {bad} HIGH/CRITICAL findings present", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
