---
title: Work Notes
type: reference
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
tags:
  - work
  - readme
  - convention
artifact_type: directory-readme
---

# Work Notes (`memory/work/`)

> The constitution says: *ALWAYS create a WORK note at `memory/work/{slug}.md` for any non-trivial task.* This file documents the shape of those notes.

A WORK note is the system of record for a single non-trivial task running through the six-phase Algorithm. One file per task. Slug is kebab-case, short, and descriptive (e.g. `auth-token-rotation`, `ingest-pdf-pipeline`, `gateway-rate-limit`).

## Required Sections

Every WORK note contains, in order:

```markdown
# {{task title}}

## Intent
{{One sentence restating what the user actually asked for.}}

## Effort
{{Quick | Standard | Deep | Comprehensive}} — see `core/effort-tiering.md`.

## Reproduce (when applicable)
{{For bug-fix tasks: the exact reproduction artifact — command, error, screenshot path.}}

## Plan
{{The numbered Deliverable Manifest — every explicit user sub-task as its own line.}}
{{Each deliverable maps to ≥1 ISC below.}}

## Criteria
- [ ] ISC-1: {{criterion text — what tool returns yes/no on this}}
- [ ] ISC-2: ...
- [ ] ISC-N: Anti: {{what must NOT happen for this to count as done}}

## Test Strategy
| ISC | Type | Check | Threshold | Tool |
|-----|------|-------|-----------|------|
| ISC-1 | grep | <pattern in file X> | ≥1 match | `grep` |
| ISC-2 | ...  | ...  | ... | ... |

## Decisions
{{Timestamped decision log — including dead ends and refined-* updates.}}

## Verification
{{Per-ISC evidence as criteria pass.}}
{{Format: `ISC-N: [probe type] — [one-line evidence, quoted command output or file content]`}}

## Learn
{{What should I have done differently? Captured at LEARN phase.}}
```

The shape mirrors the ISA format documented in `core/ALGORITHM.md` and `core/ISC.md`. See those files for the doctrine; this README is the quick-reference for the file layout.

## Naming Convention

- Slug: kebab-case, ≤6 words, semantically descriptive
- Path: `memory/work/{slug}.md`
- For project-scoped work: `projects/{project-name}/WORK.md` (project-internal) or `projects/{project-name}/work/{slug}.md` (multiple in-flight)

## Lifecycle

- **Created at OBSERVE** of any Standard or Deep task
- **Updated through every phase** — Intent at OBSERVE, Plan at PLAN, Decisions throughout, Verification at VERIFY, Learn at LEARN
- **Marked complete** when all `[ ]` ISCs transitioned to `[x]` with verification evidence captured
- **Archived** (not deleted) — completed WORK notes stay in the repo as durable record

## What Does NOT Belong Here

- Quick one-off tasks (use the conversation directly; the constitution allows skipping the WORK note for Quick-tier work)
- Project-wide documentation (use `projects/{name}/` instead)
- Reusable knowledge (route via the learning router into `templates/learning-template.md` shape under `memory/learnings/`)

## Examples

The `templates/session-summary-template.md` and `templates/project-entry-template.md` files show adjacent shapes that share much of this structure. A WORK note is more granular (one task) than a session summary (one session) or a project entry (one workstream).
