---
title: Archived Scripts — Reference Only
type: reference
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
tags:
  - tools
  - archive
  - reference
artifact_type: reference
---

# Archived Scripts

Scripts kept here for reference but NOT invoked by the active workspace.

## dep_audit-partner.py

The Tier 9 (2026-05-13) partner-contributed `dep_audit.py` (262 lines, dataclass-based, pip-audit + npm-audit wrapper with unified JSON output). Archived because the active `tools/scripts/dep_audit.py` covers more ecosystems (Python + npm + cargo + go + bundler) and writes a Markdown report integrated with `memory/security/dependency-findings.md`.

Useful reference for:
- The unified `Finding` dataclass schema (lines ~34–50) — cleaner shape than the active script's per-tool output, worth considering when the active script adds a `--json` output mode.
- The severity normalization map (`SEVERITY_ORDER`) — used to compare findings across tool-specific severity vocabularies.

Do not invoke this file directly. It will not be added to `bootstrap.sh` or any CI step.
