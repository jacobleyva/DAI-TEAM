---
title: Core
type: map
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
tags:
  - core
  - governance
  - map
artifact_type: core-map
---

# Core

This directory contains the stable operating rules for the workspace. Read on day one in the order below; everything else extends from here.

## Doctrine — Read in This Order

1. [Constitution](./constitution.md) — hard NEVER / ALWAYS / BEFORE imperatives
2. [Algorithm](./ALGORITHM.md) — the six-phase loop (Observe → Think → Plan → Execute → Verify → Learn)
3. [ISC](./ISC.md) — Ideal-State Criteria; one binary tool probe per criterion
4. [Verification Doctrine](./verification-doctrine.md) — what counts as evidence; required probes per artifact type
5. [Effort Tiering](./effort-tiering.md) — Quick / Standard / Deep / Comprehensive tier rules
6. [Operating Principles](./operating-principles.md) — the why behind the rules
7. [Decision Rules](./decision-rules.md) — tradeoff guidance for the moments doctrine doesn't fully specify
8. [Style Guide](./style-guide.md) — writing conventions across the workspace
9. [Front Matter Standard](./front-matter-standard.md) — required YAML frontmatter shape

## Integration Guides — Read on Demand

- [Codex Integration](./CODEX_INTEGRATION.md) — wiring `~/.codex/config.toml`; four documented pitfalls and recovery path
- [AI CLI Adapters](./AI_CLI_ADAPTERS.md) — per-vendor wiring conventions across Codex, Claude Code, Gemini CLI, Cursor, Aider, Copilot Chat, Continue, and Cody; reasoning-effort and parallel-tool-call mapping per vendor
- [Repo Source Integration](./REPO_INTEGRATION.md) — side-by-side enablement steps for GitHub and Azure DevOps Repos
- [Agent Composition](./agent-composition.md) — `skills/{name}/agents/{vendor}.yaml` convention for delegated skill behavior

## Domain Overviews — Read When Working in That Domain

- [Security Domain Overview](./SECURITY_DOMAIN_OVERVIEW.md) — task routing across the three security skills; output schema; reference loading guide
