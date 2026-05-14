---
title: Start Here
type: guide
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
tags:
  - start-here
  - quick-start
artifact_type: guide
---

# Start Here

This workspace is built to help a team work in a durable, shared way.

## Read Order

The canonical session-start read order is defined in `LAUNCHER.md`. Open that file next; it is the single source of truth for how a new session orients itself.

For the impatient one-line summary: read `README.md` to understand what DAI is, then `LAUNCHER.md` for the order.

## What To Put Where

- `core/` — rules and standards (constitution, Algorithm, ISC, verification doctrine, integration recipes)
- `team/` — collaboration and handoff conventions
- `memory/` — shared durable state (identity, current focus, EFFECTUS substrate, security memory)
- `projects/` — active workstreams, one folder per project
- `knowledge/` — curated reference material (CIS, OWASP, CWE collections)
- `templates/` — repeatable note structures
- `skills/` — reusable AI workflows (each with `SKILL.md`)
- `tools/scripts/` — helper scripts (frontmatter check, repo health, session-context generator, dependency audit, Codex config helper)
- `.githooks/` — pre-commit hook

## Why This Is Powerful

This workspace is stronger than a plain RAG system or one giant markdown note because it separates memory, method, and retrieval.

### Compared With RAG Alone

- RAG answers questions from text, but it does not enforce structure.
- RAG is weak at preserving ownership, handoffs, and project state.
- This workspace keeps the source of truth in editable files the whole team can inspect.

### Compared With One Big Markdown Page

- one page becomes a dumping ground
- one page is hard to route, index, and divide by purpose
- separate maps for core, memory, team, projects, and knowledge make the system easier to scale
- the team can keep structure without locking itself into a rigid app

### Compared With Simple Skills Only

- skills help with execution patterns
- skills do not hold durable team state by themselves
- the workspace plus skills gives both memory and method
- that combination is easier to evolve than a single monolithic system

## Bottom Line

The power comes from combining:

- durable files
- clear maps
- small repeatable skills
- a defined startup order
- Git history for traceability
- a shared language for where things belong

That makes the workspace easier to restart, easier to hand off, and easier to grow.
