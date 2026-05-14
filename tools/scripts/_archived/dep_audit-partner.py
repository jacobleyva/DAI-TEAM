#!/usr/bin/env python3
"""dep_audit — dependency vulnerability auditor.

Wraps `pip-audit` (Python) and `npm audit` (Node), normalizes their findings
into a unified schema, writes a JSON file, streams pretty-printed JSON to stdout,
exits non-zero if any HIGH/CRITICAL finding is present.

Usage:
    dep_audit.py [--path DIR] [--output PATH] [--fail-on SEV]
                 [--no-stdout] [--ecosystem {auto,python,node,all}]

Requires the external tools to be installed:
    pip install pip-audit          # for Python projects
    npm  install -g npm@latest     # `npm audit` ships with npm
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SEVERITY_ORDER = ["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
DEFAULT_FAIL_ON = "HIGH"


@dataclass
class Finding:
    ecosystem: str            # "python" | "node"
    package: str
    installed_version: str
    fixed_version: str | None
    severity: str             # "INFO" | "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"
    cve: list[str] = field(default_factory=list)
    cwe: list[str] = field(default_factory=list)
    advisory_url: str | None = None
    description: str | None = None


def severity_at_or_above(actual: str, threshold: str) -> bool:
    try:
        return SEVERITY_ORDER.index(actual) >= SEVERITY_ORDER.index(threshold)
    except ValueError:
        return False


def normalize_severity(raw: str | None) -> str:
    if not raw:
        return "INFO"
    raw = raw.strip().upper()
    aliases = {
        "MODERATE": "MEDIUM",
        "MED": "MEDIUM",
        "NEGLIGIBLE": "INFO",
        "UNKNOWN": "INFO",
    }
    return aliases.get(raw, raw if raw in SEVERITY_ORDER else "INFO")


def detect_ecosystems(path: Path) -> list[str]:
    found: list[str] = []
    if (path / "requirements.txt").exists() or (path / "pyproject.toml").exists() or (path / "Pipfile.lock").exists():
        found.append("python")
    if (path / "package.json").exists():
        found.append("node")
    return found


def run_pip_audit(path: Path) -> list[Finding]:
    if shutil.which("pip-audit") is None:
        print("warn: pip-audit not installed; skipping Python audit", file=sys.stderr)
        return []
    cmd = ["pip-audit", "--format=json", "--strict"]
    if (path / "requirements.txt").exists():
        cmd.extend(["-r", str(path / "requirements.txt")])
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=path)
    # pip-audit exits 1 on findings; 2 on tool error
    if proc.returncode not in (0, 1):
        print(f"warn: pip-audit exited {proc.returncode}: {proc.stderr.strip()}", file=sys.stderr)
        return []
    if not proc.stdout.strip():
        return []
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        print(f"warn: pip-audit returned non-JSON: {exc}", file=sys.stderr)
        return []

    findings: list[Finding] = []
    # pip-audit JSON shape: {"dependencies":[{"name","version","vulns":[{"id","fix_versions","aliases","description"}]}]}
    for dep in data.get("dependencies", []):
        name = dep.get("name", "")
        version = dep.get("version", "")
        for vuln in dep.get("vulns", []):
            aliases = vuln.get("aliases", []) or []
            cve = [a for a in aliases if a.upper().startswith("CVE-")]
            fix_versions = vuln.get("fix_versions") or []
            findings.append(Finding(
                ecosystem="python",
                package=name,
                installed_version=version,
                fixed_version=fix_versions[0] if fix_versions else None,
                severity=normalize_severity(vuln.get("severity")),
                cve=cve,
                advisory_url=f"https://osv.dev/vulnerability/{vuln.get('id')}" if vuln.get("id") else None,
                description=vuln.get("description"),
            ))
    return findings


def run_npm_audit(path: Path) -> list[Finding]:
    if shutil.which("npm") is None:
        print("warn: npm not installed; skipping Node audit", file=sys.stderr)
        return []
    proc = subprocess.run(
        ["npm", "audit", "--json"],
        capture_output=True, text=True, cwd=path,
    )
    # npm audit exits non-zero on findings — that's expected
    if not proc.stdout.strip():
        print(f"warn: npm audit returned empty output (stderr: {proc.stderr.strip()})", file=sys.stderr)
        return []
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        print(f"warn: npm audit returned non-JSON: {exc}", file=sys.stderr)
        return []

    findings: list[Finding] = []
    # npm v7+ shape: {"vulnerabilities": {"<pkg>": {"name","severity","via":[...]}}}
    for pkg_name, vuln_obj in (data.get("vulnerabilities") or {}).items():
        severity = normalize_severity(vuln_obj.get("severity"))
        installed = ""
        if isinstance(vuln_obj.get("range"), str):
            installed = vuln_obj["range"]
        fix_avail = vuln_obj.get("fixAvailable")
        fixed_version: str | None
        if isinstance(fix_avail, dict):
            fixed_version = fix_avail.get("version")
        elif fix_avail is True:
            fixed_version = "(see npm audit fix)"
        else:
            fixed_version = None

        cve_list: list[str] = []
        cwe_list: list[str] = []
        advisory_url: str | None = None
        description: str | None = None
        for via in vuln_obj.get("via", []) or []:
            if isinstance(via, dict):
                if via.get("url"):
                    advisory_url = advisory_url or via["url"]
                if via.get("title") and not description:
                    description = via["title"]
                for cwe in via.get("cwe") or []:
                    if cwe not in cwe_list:
                        cwe_list.append(cwe)
                # GHSA IDs and CVE aliases
                for src in (via.get("source"), via.get("name")):
                    if isinstance(src, str) and src.upper().startswith("CVE-") and src not in cve_list:
                        cve_list.append(src)
        findings.append(Finding(
            ecosystem="node",
            package=pkg_name,
            installed_version=installed,
            fixed_version=fixed_version,
            severity=severity,
            cve=cve_list,
            cwe=cwe_list,
            advisory_url=advisory_url,
            description=description,
        ))
    return findings


def summarize(findings: Iterable[Finding]) -> dict[str, int]:
    summary = {sev: 0 for sev in SEVERITY_ORDER}
    summary["TOTAL"] = 0
    for f in findings:
        summary[f.severity] = summary.get(f.severity, 0) + 1
        summary["TOTAL"] += 1
    return summary


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0] if __doc__ else "")
    p.add_argument("--path", default=".", help="Project root to audit (default: cwd)")
    p.add_argument("--output", default=None,
                   help="Output JSON file (default: ./audit-<UTC-ISO8601>.json)")
    p.add_argument("--fail-on", default=DEFAULT_FAIL_ON, choices=SEVERITY_ORDER,
                   help=f"Exit non-zero if any finding ≥ this severity (default: {DEFAULT_FAIL_ON})")
    p.add_argument("--no-stdout", action="store_true",
                   help="Suppress pretty-printed JSON to stdout (file output only)")
    p.add_argument("--ecosystem", default="auto",
                   choices=["auto", "python", "node", "all"],
                   help="Which ecosystems to scan (default: auto-detect)")
    args = p.parse_args()

    path = Path(args.path).resolve()
    if not path.is_dir():
        print(f"error: path is not a directory: {path}", file=sys.stderr)
        return 2

    if args.ecosystem == "auto":
        ecosystems = detect_ecosystems(path)
        if not ecosystems:
            print(f"error: no python or node manifest found in {path}", file=sys.stderr)
            return 2
    elif args.ecosystem == "all":
        ecosystems = ["python", "node"]
    else:
        ecosystems = [args.ecosystem]

    findings: list[Finding] = []
    if "python" in ecosystems:
        findings.extend(run_pip_audit(path))
    if "node" in ecosystems:
        findings.extend(run_npm_audit(path))

    findings.sort(
        key=lambda f: (-SEVERITY_ORDER.index(f.severity) if f.severity in SEVERITY_ORDER else 0, f.package),
    )

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    output_path = Path(args.output) if args.output else Path.cwd() / f"audit-{ts}.json"

    payload: dict[str, Any] = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "path_audited": str(path),
        "ecosystems_audited": ecosystems,
        "summary": summarize(findings),
        "findings": [asdict(f) for f in findings],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=False)
        fh.write("\n")

    if not args.no_stdout:
        json.dump(payload, sys.stdout, indent=2, sort_keys=False)
        sys.stdout.write("\n")

    print(f"\nWrote {len(findings)} findings to {output_path}", file=sys.stderr)
    print(f"Summary: {payload['summary']}", file=sys.stderr)

    has_blocking = any(
        severity_at_or_above(f.severity, args.fail_on) for f in findings
    )
    return 1 if has_blocking else 0


if __name__ == "__main__":
    sys.exit(main())
