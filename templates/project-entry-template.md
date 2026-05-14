---
title: Project Entry Template
type: template
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
tags:
  - template
  - project
artifact_type: template
---

# Project — {{project-name}}

> One file per active project. Lives at `projects/{{slug}}/overview.md`. Tasks, logs, and resources sit alongside; this file is the entry point.

## Header

- **Project name:** {{project-name}}
- **Slug:** {{kebab-case-slug}}
- **Created:** {{date}}
- **Owner:** {{name}}
- **Status:** active / paused / shipped / archived
- **Mission this rolls up to:** M1 / M2 / M3 (see `memory/effectus/mission.md`)
- **Linked goal:** G{{N}} (see `memory/effectus/goals.md`)

## Purpose

- **One-sentence purpose:** {{what becomes true in the world if this project succeeds}}
- **Why now:** {{the trigger or constraint that made this the current priority over alternatives}}
- **Falsification condition:** {{what observation would prove the project should be paused or killed}}

## Current State

| Area | State | Evidence |
|------|-------|----------|
| Scope | {{specifics — what's in and what's out}} | {{path to scope decision}} |
| Schedule | {{target date for the next visible deliverable}} | {{path to plan or estimate}} |
| Risks (top 2-3) | {{R-01, R-02 from the active risk register}} | {{path to risk log}} |
| Dependencies (people / systems) | {{names + nature of dependency}} | {{path to coordination notes}} |
| Last decision logged | {{date + one-line summary}} | {{path to `projects/{{slug}}/log.md`}} |

## Next Steps

1. {{Concrete next step — verb-led, deadline-attached, owner-named}}
2. {{Concrete next step}}
3. {{Concrete next step}}

## Acceptance Criteria

> Each line is a yes/no probe. The project is done when every line passes.

- [ ] {{ISC-1: criterion text — what tool-verifiable thing must be true}}
- [ ] {{ISC-2: criterion text}}
- [ ] {{ISC-3: criterion text}}
- [ ] {{ISC-N: Anti: {{what must NOT happen for this to count as done}}}}

## Folder Contents

| File | Purpose |
|------|---------|
| `projects/{{slug}}/overview.md` | This file — entry point and current state |
| `projects/{{slug}}/tasks.md` | Active task list and backlog |
| `projects/{{slug}}/log.md` | Running decision and dev log — append-only |
| `projects/{{slug}}/resources.md` | Links, docs, references, vendor contacts |

## Related Artifacts

- Linked WORK note: {{path}}
- Linked design doc: {{path or URL}}
- Linked code: {{path:lines}}
- Threat model (if applicable): {{path}}
- External tickets / issues: {{IDs and links}}

## Review Cadence

- **Status review:** {{weekly / bi-weekly / monthly}}
- **Status reviewers:** {{names or "the team"}}
- **Re-baseline trigger:** {{event that forces a full re-scoping — major dependency change, missed milestone, new info}}
