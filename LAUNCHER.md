---
title: Launcher
type: guide
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
tags:
  - launcher
  - startup
  - onboarding
artifact_type: guide
---

# Launcher

This is the first file to open in a new session.

## Session Order

**Preferred path:** read the synthesized `memory/session-context.md`. That single file catenates everything below in one deterministic block. Regenerate it with `tools/scripts/build_session_context.sh` after any change to its sources. Wire Codex to read it via `config.toml` — see `core/CODEX_INTEGRATION.md`.

**Manual path (fallback when the synthesized file is stale or absent):**

1. `LAUNCHER.md`
2. `WELCOME.md`
3. `START_HERE.md`
4. `dai-overview.md`
5. `active-work-map.md`
6. `core/constitution.md` — hard NEVER/ALWAYS/BEFORE imperatives
7. `core/ALGORITHM.md` — the operating loop
8. `core/ISC.md` — acceptance criteria doctrine
9. `core/effort-tiering.md` — Quick / Standard / Deep tier rules
10. `core/verification-doctrine.md` — required probes per artifact type
11. `memory/identity.md`
12. `memory/current-focus.md`
13. `memory/effectus/effectus-map.md` — deeper substrate, read on-demand when leverage matters

**Read on-demand (referenced when the task pattern matches):**

- `core/agent-composition.md` — `skills/{name}/agents/{vendor}.yaml` convention
- `core/CODEX_INTEGRATION.md` — wiring `~/.codex/config.toml` to this workspace
- `core/decision-rules.md` — tradeoff guidance

## What This Workspace Is

A shared operating system for a technical team. It keeps context, work, and reusable methods in one durable place.

## What It Does

- keeps shared context durable in files
- separates rules, memory, projects, knowledge, templates, skills, and tools
- gives each session a stable startup path
- makes handoffs, restarts, and recovery simpler
- preserves work even when chat history is gone

## What To Do First

1. Read the startup files in order.
2. Check `active-work-map.md` for current priorities.
3. Put shared rules in `core/`.
4. Put active context in `memory/`.
5. Put workstream details in `projects/`.

## Why It Exists

It is stronger than a single markdown note because structure, history, and reusable operating patterns stay separated, searchable, and easy to recover.
