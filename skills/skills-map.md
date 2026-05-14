---
title: Skills Index
type: map
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
tags:
  - dai
  - skills
  - map
  - reuse
artifact_type: skills-index
---

# Skills Index

This file links the reusable skills available in this workspace. Every skill has a `SKILL.md` entry point and may include `workflows/` for phase-by-phase procedures, `agents/` for per-vendor specs, and `references/` for supporting material.

## Available Skills

### General-purpose

- [Code Review](./code-review/SKILL.md) — review code with emphasis on bugs, regressions, risk, and missing tests
- [Feature Spec Writer](./feature-spec-writer/SKILL.md) — turn rough ideas into implementation-ready feature specifications
- [Planning](./planning/SKILL.md) — structure work into practical plans and execution steps
- [Repo Onboarding](./repo-onboarding/SKILL.md) — inspect an unfamiliar repository and summarize how to work in it
- [Research Synthesizer](./research-synthesizer/SKILL.md) — consolidate findings into decision-useful summaries

### Security domain

- [Security Review](./security-review/SKILL.md) — review code, config, or infrastructure for authn / authz / input validation / secrets / dependency / crypto risk
- [Threat Modeling](./threat-modeling/SKILL.md) — produce a structured threat model using STRIDE, attack trees, and kill-chain analysis
- [Incident Response](./incident-response/SKILL.md) — drive structured triage, containment, eradication, recovery, and lessons-learned during or after a security or operational incident
- [CIS Controls](./cis-controls/SKILL.md) — align designs, configurations, and implementation decisions to the CIS Controls v8.1

## Conventions

- Each skill lives in its own folder under `skills/`.
- Each skill folder exposes a `SKILL.md` entry point with frontmatter and a defined workflow.
- Per-skill `workflows/<name>.md` files hold phase-by-phase procedures referenced from `SKILL.md`.
- Per-vendor agent specs (e.g. `agents/openai.yaml`, `agents/anthropic.yaml`) live alongside `SKILL.md` when delegation behavior differs across vendors. See `core/agent-composition.md`.
- Reference material lives in `references/<name>.md` within the skill folder.

## Adding a New Skill

See `CONTRIBUTING.md` → "Skill Scaffolding" for the canonical recipe. A new skill is registered by adding an entry to this file and regenerating `memory/skills-catalog.md` with `tools/scripts/skills_index.sh`.

## Related Maps

- [DAI Overview](../dai-overview.md)
- [Projects Map](../projects/projects-map.md)
- [Core Doctrine Map](../core/core-map.md)
- [Security Domain Overview](../core/SECURITY_DOMAIN_OVERVIEW.md) — task routing across the four security skills
