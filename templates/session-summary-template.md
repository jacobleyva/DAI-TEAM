---
title: Session Summary Template
type: template
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
tags:
  - template
  - session-summary
artifact_type: template
---

# Session Summary — {{date}} — {{8-word title}}

> Written at session close. Future-you and the next teammate read this to pick up cold. Date everything, cite files by path, quote tool output.

## Header

- **Session date:** {{date}}
- **Session owner:** {{name}}
- **Effort tier:** E1 / E2 / E3 / E4 / E5 (see `core/effort-tiering.md`)
- **Project / context:** {{path to project overview or "ad-hoc"}}
- **Started phase:** {{phase the session opened in}}
- **Closed phase:** {{phase the session reached at close}}
- **Outcome:** Completed / Paused / Blocked / Abandoned with reason

## What Changed

| File / system / external | Change | Evidence |
|--------------------------|--------|----------|
| {{path or URL}} | {{verb-led one-line description}} | {{commit hash / tool output / screenshot path}} |
| {{path}} | | |
| {{path}} | | |
| {{path}} | | |

**Commit list:**

- `{{hash}}` — {{title}}
- `{{hash}}` — {{title}}

## Current State

- **Where the work is right now:** {{1-2 sentences a stranger can read cold}}
- **Last passing acceptance criterion:** {{ISC-N — name + how it was verified}}
- **Next pending acceptance criterion:** {{ISC-N — what blocks it from passing}}
- **Cleanup state:** {{working tree clean / N uncommitted files at paths X, Y}}

## Decisions

| Decision | Reasoning | Reversibility |
|----------|-----------|---------------|
| {{what was decided}} | {{why this over the alternatives}} | {{cheap / costly / one-way door}} |
| | | |

## Open Questions

- {{Question that needs answering before the next session can proceed}}
- {{Question that someone outside the session has to weigh in on}}
- {{Question that depends on an external event}}

## Learnings to Route

> Anything worth keeping out of session history goes through the learning router.

- {{learning 1 — 8-12 word description}} → route to: {{learning template / skill gotcha / constitution rule}}
- {{learning 2}} → route to: {{...}}

## Resume Instructions

1. {{First action the next session should take}}
2. {{Second action}}
3. {{Third action — typically "verify the last criterion is still passing"}}

## Linked Artifacts

- Related project: {{path to `projects/{{slug}}/overview.md`}}
- Source WORK note: {{path}}
- Related session summaries: {{paths}}
- Related learnings: {{paths to learning files}}
