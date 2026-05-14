---
title: Templates Map
type: map
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
tags:
  - templates
  - map
artifact_type: templates-map
---

# Templates Map

Reusable note formats. Every template carries real content, not stubs — `tools/scripts/eval_templates.py` enforces this in CI.

## Available Templates

| Template | Purpose | Use when |
|----------|---------|----------|
| [executive-stakeholder-summary-template.md](executive-stakeholder-summary-template.md) | One-page exec summary — decisions, not narrative | Reporting initiative status to stakeholders / sponsors / steering |
| [learning-template.md](learning-template.md) | Capture a refutable claim about system behavior with evidence | A session produced a learning worth keeping — route via the learning router |
| [member-handoff-template.md](member-handoff-template.md) | Walk-cold handoff between team members | Outgoing owner transitions a project / role / domain |
| [project-entry-template.md](project-entry-template.md) | Per-project overview file — `projects/{slug}/overview.md` | Starting a new project; need acceptance criteria + mission roll-up |
| [session-summary-template.md](session-summary-template.md) | Session close note — pick-up-cold context | Ending a working session worth documenting |
| [threat-model-template.md](threat-model-template.md) | STRIDE + attack-tree + kill-chain threat model | Modeling threats against a system or proposed change |
| [incident-response-template.md](incident-response-template.md) | Six-phase IR record — detect → triage → contain → eradicate → recover → lessons | Active or post-incident documentation |

## Verification

Every template above passes `tools/scripts/eval_templates.py`. New templates must pass before merge — CI enforces this on every PR. A template "passes" when its body contains at least one bullet list or table — no heading-only stubs.
