---
title: Learning Template
type: template
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
tags:
  - template
  - learning
artifact_type: template
---

# Learning — {{short-title}}

> A learning is a refutable claim about how this system behaves, born from concrete evidence and useful to a future teammate. Not a journal entry.

## Header

- **Captured:** {{date}}
- **Captured by:** {{name}}
- **Source session:** {{path to session-summary or work note that produced it}}
- **Category:** Doctrine / Tooling / Process / Domain knowledge / Operational
- **Confidence:** Strongly held / Working hypothesis / Single-data-point

## Context

- **Where this happened:** {{file path / system / tool / external service}}
- **What was being attempted:** {{1-2 sentences naming the actual goal}}
- **What you expected:** {{the model of the system you walked in with}}
- **What actually happened:** {{the observed deviation — tool-verified, with output if possible}}

## Lesson

> One sentence stating the rule this learning crystallizes.

- **Why it's true:** {{the mechanism / first-principles reason, not just the symptom}}
- **Falsification condition:** {{what would prove this learning wrong if seen later}}
- **Scope of applicability:** {{only this tool / this domain / general system behavior}}

## Reuse

| Where this applies | What to do differently |
|--------------------|-----------------------|
| {{situation 1}} | {{the concrete adjustment}} |
| {{situation 2}} | |
| {{situation 3}} | |

## Linked Artifacts

- Originating evidence: {{paste the actual command output, error message, or screenshot path}}
- Related learnings: {{paths to other learning files this reinforces or contradicts}}
- Routed-to constitution rule: {{path to `core/constitution.md` entry if this became doctrine}}
- Routed-to skill gotcha: {{path to `skills/<name>/SKILL.md` Gotchas section if this became a skill-local rule}}

## Review Trigger

- **Re-examine when:** {{the next deploy of X / quarterly / when teammate Y joins / when system Z changes}}
- **Sunset condition:** {{the change that would make this learning obsolete}}
