---
title: Knowledge Map
type: map
domain: knowledge
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
tags:
  - knowledge
  - map
artifact_type: knowledge-map
---

# Knowledge Map

This is the main entry point for curated reference material — upstream catalogs ingested into the workspace so the doctrine can reference specific control IDs, weakness types, and threat categories without inventing them.

## Lifecycle

- [Knowledge Lifecycle](./knowledge-lifecycle.md) — how new reference material is added, validated, and retired

## Collections

The `collections/` subdirectory holds curated upstream catalogs:

- [CIS Critical Security Controls v8.1](./collections/cis-controls-v8.1.md) — 18 controls / 153 safeguards / 3 Implementation Groups
- [OWASP Top 10 (2021)](./collections/owasp-top-10.md) — web-application risk categories
- [OWASP API Security Top 10 (2023)](./collections/owasp-api-top-10.md) — API-specific risk categories
- [CWE Top 25 (2024)](./collections/cwe-top-25.md) — most dangerous software weakness types

When a doctrine file (constitution, algorithm, ISC, verification doctrine) or a skill (`skills/security-review/`, `skills/threat-modeling/`) needs to cite a specific control, CWE, or OWASP category, the reference should come from one of these collection files — not from generic model knowledge.
