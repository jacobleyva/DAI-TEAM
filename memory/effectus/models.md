---
title: Models
type: effectus
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
version: v1.0
tags:
  - effectus
  - models
  - mental-models
  - frames
artifact_type: effectus-models
---

# Models

> **Mental models the team uses to make sense of its domain.** These are the lenses behind decisions. A good model is portable — it explains more than one situation. The library grows when a new frame proves itself useful across multiple decisions.

## How to write a model entry

- **Name the model.** A short handle the team can refer to in conversation.
- **One-paragraph explanation.** What the model says, and what it predicts or distinguishes.
- **At least one concrete example.** Where this model has actually changed a decision in the team's recent work.
- **Source if borrowed.** Models often come from books, papers, mentors, or domain experience — credit the source.

## Active models

(Replace the `(SEED)` entries below.)

### M1 — Scaffolding vs. Model (SEED)

The leverage on an AI-assisted system lives more in the surrounding scaffolding (rules, files, hooks, deterministic startup) than in the underlying model. A weaker model with stronger scaffolding tends to outperform a stronger model with weaker scaffolding on production work — because production work runs into the same operational shapes repeatedly.

**Concrete example:** Codex with weak scaffolding (values-prose constitution, no algorithm primitive, no ISC) versus the same model with strong scaffolding (hard imperatives, the six-phase Algorithm, granular ISC criteria). Same underlying model; materially different operational floor.

**Source:** *Domain AI Infrastructure* — the principle that discipline lives in the files, not in the model.

### M2 — Design-pressure differential (SEED)

Different AI tools have different design pressures even when they aim at the same destination. Claude Code can have a *light* scaffolding because the model carries operational discipline intrinsically. Codex needs *deterministic* scaffolding because the model won't carry the same discipline. Same destination; different route.

**Concrete example:** This workspace exists because Codex needs externalized discipline — written-down rules, an explicit algorithm, granular acceptance criteria, file-based memory — that a model with internal discipline could leave implicit.

**Source:** Internal — observed during cross-vendor work where the same task succeeded with explicit scaffolding and failed without it.

### M3 — Reproduce-first (SEED)

For any "X is broken" problem, the work begins with capturing a reproduction — not with reading the suspect code. Code-reading without a reproduction is theory; reproduction is data. The reproduction is also the baseline against which the fix is verified.

**Concrete example:** Every bug-fix WORK note in this workspace starts with a reproduction artifact under `## Reproduction`. See `core/verification-doctrine.md` § Reproduce-First Rule.

**Source:** Long-standing engineering wisdom (Brian Kernighan, "Debugging is twice as hard as writing the code in the first place"). Adopted explicitly into this team's algorithm.

## Retired models

(When a model stops being useful or gets refuted, move it here with the date and the replacement.)

- _none yet_

## Related

- See `memory/effectus/beliefs.md` for the convictions these models support.
- See `memory/effectus/wisdom.md` for the operating rules these models produced.
