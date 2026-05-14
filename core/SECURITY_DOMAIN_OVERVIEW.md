---
title: Security Domain Overview
type: reference
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
version: v1.0
tags:
  - security
  - doctrine
  - orchestrator
  - overview
artifact_type: domain-overview
---

# Security Domain Overview

> Read this file when working on any security task in the DAI workspace. Skill-level `SKILL.md` files in `skills/security-*/` add per-skill specifics on top of this domain-wide doctrine. Workflow files at `skills/<skill>/workflows/<name>.md` encode the phase-by-phase procedures.

This file is the orchestrator: it routes from the user's request to the right skill and reference material, and it states the doctrine that applies across every security task in this tree.

## Domain Map

```
core/SECURITY_DOMAIN_OVERVIEW.md       ← you are here (this file)

skills/security-review/SKILL.md         ← code / config / infra review
    workflows/code-audit.md
    workflows/config-audit.md

skills/threat-modeling/SKILL.md         ← STRIDE / attack-tree / kill-chain
    workflows/stride.md
    workflows/attack-tree.md
    workflows/kill-chain.md

skills/incident-response/SKILL.md       ← detect → triage → contain → eradicate → recover → learn
    workflows/triage.md
    workflows/containment.md
    workflows/postmortem.md

skills/cis-controls/                    ← control catalog mapping
    SKILL.md

templates/threat-model-template.md      ← fill-in for threat-modeling output
templates/incident-response-template.md ← fill-in for incident-response output

memory/security/threat-landscape.md     ← org-specific threat priorities
memory/security/auth-patterns.md        ← org-specific authN/authZ defaults
memory/security/incident-log.md         ← cumulative incident record

knowledge/collections/cis-controls-v8.1.md
knowledge/collections/owasp-top-10.md
knowledge/collections/owasp-api-top-10.md
knowledge/collections/cwe-top-25.md

tools/scripts/dep_audit.py              ← dependency vulnerability auditor
```

## Task Routing — How to Pick the Right Skill

When the user's request matches any of the following, read the listed `SKILL.md` next and follow its instructions.

| Request signals | Skill |
|---|---|
| "security review", "audit this code", "review this PR for security", "scan repo before release", "review Terraform/Dockerfile/K8s" | `skills/security-review/SKILL.md` |
| "threat model", "STRIDE", "attack tree", "kill chain", "design review for security", "what could an attacker do" | `skills/threat-modeling/SKILL.md` |
| "incident", "breach", "we got compromised", "triage this alert", "postmortem", "IOC", "containment" | `skills/incident-response/SKILL.md` |
| "run dependency audit", "check for vulnerable deps" | invoke `python3 tools/scripts/dep_audit.py --path <project>` |
| "control mapping", "CIS controls", "compliance crosswalk" | `skills/cis-controls/SKILL.md` |

When the request is ambiguous, ask the user to clarify scope before reading a workflow.

## Doctrine — Applies to ALL Security Work

These principles apply to every task performed in this domain. Per-skill `SKILL.md` files may add more specifics but never override these.

1. **Tool-verifiable acceptance.** Every check, every probe, every "done" claim must point to a command, regex, test, or file that confirms the state. No claims unsupported by an artifact that can be re-run. This is the same rule that lives in `core/verification-doctrine.md` — it applies here without modification.

2. **Reference, don't fabricate.** When citing CWE IDs, OWASP categories, CIS control numbers, MITRE ATT&CK techniques: look them up in `knowledge/collections/` first. If the answer isn't there, say so — never invent an ID.

3. **Scope discipline.** This tree's allow-list for new files: `skills/security-*/`, `templates/`, `memory/security/`, `knowledge/`, `.githooks/`, `tools/scripts/`. Flag any change requested outside this allow-list and confirm with the user before proceeding.

4. **Boundaries before content.** For reviews and threat models, identify trust boundaries before enumerating issues — that frames where to look.

5. **Fix beats finding.** Every finding includes a concrete remediation AND a verification step. A finding without those is half-done.

6. **Blameless framing.** When discussing incidents or process failures, attribute to systems and processes, never to individuals.

7. **Evidence before action.** For incident-related tasks, capture forensic artifacts (memory, logs, network captures) before recommending state-changing remediation.

8. **Living documents.** Threat models and the threat landscape decay with system changes. Always record (a) the system version analyzed and (b) the condition that should trigger the next review.

## Output Shape — Domain-Wide Conventions

- **For reviews:** a Markdown table of findings sorted by severity (CRITICAL → HIGH → MEDIUM → LOW → INFO).
- **For threat models:** a populated copy of `templates/threat-model-template.md`.
- **For incidents:** a populated copy of `templates/incident-response-template.md`.
- **For audit-script invocations:** the output file path + a 3-line summary (TOTAL / HIGH / CRITICAL counts).

## Reference Material — Load When Relevant

| When working on... | Read first |
|---|---|
| Application-layer findings | `knowledge/collections/owasp-top-10.md` |
| API findings | `knowledge/collections/owasp-api-top-10.md` |
| CWE assignment for any finding | `knowledge/collections/cwe-top-25.md` |
| Cloud / config / process maturity | `knowledge/collections/cis-controls-v8.1.md` |
| Org-specific threat priorities | `memory/security/threat-landscape.md` |
| Org auth conventions / patterns | `memory/security/auth-patterns.md` |
| Prior incidents in this org | `memory/security/incident-log.md` |

## Tools

| Tool | Purpose | How to call |
|---|---|---|
| `tools/scripts/dep_audit.py` | Walks the workspace for known manifests (pip, npm, cargo, go, bundler), runs the available auditor, writes structured Markdown report | `python3 tools/scripts/dep_audit.py [--check] [--quiet]` |
| `.githooks/pre-commit` | Frontmatter validation + 13-pattern secret scan at every local commit | Auto-installed by `bootstrap.sh` |
| `tools/scripts/secret_scan_diff.sh` | Same 13-pattern scan, applied to a git-diff between two refs | `bash tools/scripts/secret_scan_diff.sh [BASE [HEAD]]` |
| External: `semgrep`, `gitleaks`, `trivy`, `checkov`, `tfsec`, `kubescape` | Referenced from workflow files; install separately | See workflow files for exact commands |

## What Security Work in DAI Should NOT Do

- Don't write security findings or threat models from generic knowledge alone — always read the relevant workflow file first.
- Don't modify files outside the allow-list in section "Doctrine #3" without explicit user confirmation.
- Don't auto-execute destructive actions (deleting files, force-pushing, running `eradication` steps from incident response workflows) — those are user decisions; provide recommendations and let the user authorize execution.
- Don't invent CWE / OWASP / ATT&CK IDs. If the relevant knowledge file doesn't list it, say so explicitly.
- Don't condense the structured output format (severity, where, CWE, OWASP, impact, evidence, fix, verify). Each finding gets the full schema.

## Verification — Confirming Domain Doctrine Was Followed

After any security task in this domain, the repository owner can verify compliance:

```bash
# Output references at least one workflow file
grep -E 'workflows/[a-z-]+\.md' <output>

# Output includes the expected structured-finding schema
grep -E 'Where:|CWE:|OWASP:|Fix:|Verify:' <output>

# No invented CWE IDs (every CWE-XXX cited appears in cwe-top-25.md or has a source URL)
comm -23 \
  <(grep -oE 'CWE-[0-9]+' <output> | sort -u) \
  <(grep -oE 'CWE-[0-9]+' knowledge/collections/cwe-top-25.md | sort -u)
# Any IDs printed by `comm` should also appear in the output with a cwe.mitre.org source link.
```

