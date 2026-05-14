---
title: Incident Log
type: security-memory
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
version: v1.0
tags:
  - security
  - incidents
  - log
  - postmortem
artifact_type: security-memory
---

# Incident Log

Append-only chronological record of security incidents. Source of truth for incident metrics (MTTD/MTTR trends), repeat-cause detection, and onboarding context for new team members.

> **Origin:** schema and structure imported from partner contribution (Tier 9, 2026-05-13). The previous file contained a single SEED row. Replace the example row with real entries before relying on aggregates.

<!-- This file is sensitive; restrict access per your data classification policy -->

## Schema

| Column | Required | Notes |
|---|---|---|
| Date | yes | YYYY-MM-DD of declaration |
| Incident ID | yes | `INC-YYYY-NNNN` |
| Type | yes | Phishing / Credential abuse / Malware / Ransomware / Misconfig / Insider / Vuln-exploit / Supply-chain / DDoS / Other |
| Severity | yes | SEV-1 / SEV-2 / SEV-3 / SEV-4 |
| MTTD | yes | Time from first attacker action to detection (HH:MM or days) |
| MTTR | yes | Time from declaration to recovery (HH:MM or days) |
| Root cause (one line) | yes | Systemic, not individual |
| Postmortem link | yes for SEV-1/2 | URL/path |

## Log

| Date | ID | Type | Severity | MTTD | MTTR | Root Cause | Postmortem |
|---|---|---|---|---|---|---|---|
| 2024-01-01 | INC-2024-0001 | Misconfig | SEV-3 | 12d | 2h | Public S3 bucket — Terraform module defaulted to public; no policy-as-code guard | `<link>` |
<!-- TODO — DELETE EXAMPLE ROW ABOVE ONCE REAL ENTRIES EXIST -->

<!-- Append new rows below this line -->

## Quarterly Rollup (Auto-generate or Maintain Manually)

<!-- TODO — replace with your real numbers each quarter -->

| Quarter | Count | SEV-1/2 | SEV-3/4 | Avg MTTD | Avg MTTR | Top recurring cause |
|---|---|---|---|---|---|---|
| `YYYY-QN` | 0 | 0 | 0 | — | — | — |

## Repeat-Cause Watch

When the same root cause appears > 1× in trailing 12 months, escalate to a structural fix initiative.

<!-- TODO — list any repeat causes here with the action being taken -->

## Notable Patterns

(Update this section when 3+ incidents share a common pattern.)

- _no patterns yet_

## Cross-References

- Each incident row links to its full report following `templates/incident-response-template.md`.
- Threat-landscape file (`memory/security/threat-landscape.md`) updated quarterly with patterns observed here.
- Action items from each incident tracked in `<your tracker>` <!-- TODO --> with tag `incident-action`.

## Related

- `templates/incident-response-template.md` — structure for full incident writeups
- `skills/incident-response/SKILL.md` — workflow that produces those writeups
- `memory/effectus/wisdom.md` — one-line lessons crystallize here from incident reviews
- `memory/security/threat-landscape.md` — repeated incident patterns update the threat landscape
- `memory/security/auth-patterns.md` — incident lessons sometimes retire or amend auth patterns
