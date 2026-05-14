---
name: repo-onboarding
description: Use when entering an unfamiliar codebase and you need a quick, reliable understanding of structure, entry points, commands, risks, and where to make changes.
---

# Repo Onboarding

Map an unfamiliar repository before making substantial changes.

## Workflow

1. Inspect top-level files and package manifests.
2. Identify the main runtime, framework, and test commands.
3. Find the feature area relevant to the request.
4. Note conventions, generated files, and likely ownership boundaries.
5. Summarize the minimum context needed to start editing safely.

## Focus areas

- app entry points
- build and test commands
- routing or feature boundaries
- configuration and environment files
- existing patterns in the target area

## Guardrails

- prefer `rg` for search
- do not assume a stack from folder names alone
- before editing, read the nearest related implementation
