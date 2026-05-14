---
title: DAI Roadmap
type: reference
domain: dai
product: DAI
audience: contributors
owner: team
status: active
updated: 2026-05-14
tags:
  - roadmap
  - planning
artifact_type: roadmap
---

# DAI Roadmap

> The state of DAI today, what's coming next, and what's deliberately not in scope. This file is updated whenever the public direction changes — not on a fixed cadence.

## Where DAI Is Today (v1.0.x)

DAI v1.0 — codename *Discipline Externalized* — shipped on 2026-05-11. The build covers five doctrine tiers and one onboarding tier:

| Tier | Theme | Status |
|------|-------|--------|
| Tier 1 | Algorithm + ISC + session synthesizer + Codex integration recipe | Shipped |
| Tier 2 | Hard-imperative constitution + EFFECTUS substrate + verification doctrine | Shipped |
| Tier 3 | Effort tiering + agent composition + pre-commit hook + template eval | Shipped |
| Tier 3.5 | `bootstrap.sh` one-command setup | Shipped |
| Tier 4 | Security domain — review / threat modeling / incident response | Shipped |
| Tier 5 | Codex config safety — TOML-aware wiring helper | Shipped |
| Tier 6 | Publish prep — public-facing surface, LICENSE, CONTRIBUTING, SECURITY, README rewrite | Shipped |

CHANGELOG.md carries the per-tier detail.

## Validation Pending

The acceptance bar for v1.0 includes one criterion that cannot be verified by the maintainers alone:

- **Third-machine fresh-clone install.** A fresh `git clone` + `./bootstrap.sh` on a machine that has never seen DAI before, followed by a Codex session that confirms the doctrine loaded. This is the real proof that the bootstrap flow does what it says. The maintainers have run it on two machines so far; the third-machine validation is genuinely open and is the most useful first contribution a new user can make. Please open an issue with the install transcript whether it passes or fails.

## Near-term (next 90 days)

### Already in motion

- **Doctrine refinement from real installs.** Every install report (issue or PR) feeds back into `core/`. Expect minor patch versions through this window.
- **Security domain expansion.** The Tier 4 substrate — three skills, two templates, three seed memory files — is intentionally bare. A security-domain owner is filling the seeds with real intel and adding `Gotchas` sections to the skill files. Expect a Tier 4.1 patch.
- **Template fill-out.** All seven templates pass `tools/scripts/eval_templates.py` as of Tier 6. Refinements based on actual use are welcome.

### Open to contribution

- **Per-language skill packs.** Skills are language-agnostic today. A `skills/lang-typescript/`, `skills/lang-python/`, `skills/lang-rust/` set would let teams adopt DAI more quickly.
- **More effort-tier worked examples.** `core/effort-tiering.md` defines the tiers; concrete examples of E2/E3/E4 sessions captured as session-summaries would help new adopters calibrate.
- **CI integration recipes.** DAI now ships first-class CI workflows for **GitHub Actions** (`.github/workflows/dai-checks.yml`) and **Azure DevOps Pipelines** (`azure-pipelines.yml`) — both call the same `tools/scripts/*` checks. Recipes for GitLab CI, Jenkins, and CircleCI are open to contribution; see `core/REPO_INTEGRATION.md` for the integration pattern.
- **Vendor neutrality audit.** DAI is shaped around Codex but the doctrine is vendor-neutral by intent. A documented adapter pattern for Cursor, Aider, and other coding-assistant CLIs would broaden reach.

## Medium-term (90-180 days)

- **Multi-team workspace pattern.** DAI today targets a single team's workspace. A documented pattern for a parent organization with multiple DAI-using teams — shared `core/` doctrine, per-team `memory/` and `projects/` — is the natural next scale.
- **Observability hooks.** Optional event emission from `bootstrap.sh`, the pre-commit hook, and skill invocations so teams adopting DAI can measure usage without modifying the doctrine itself.
- **Skill versioning.** Today skills are mutable. A migration to versioned skill spec files would let teams pin to known-good versions and upgrade deliberately.

## Out of Scope (Deliberately)

These are not coming. They are listed here so contributors don't have to guess.

- **A managed cloud service.** DAI is files in a git repo. That's the point.
- **Telemetry by default.** Observability hooks (when they ship) will be opt-in.
- **A graphical UI.** The interface is the file tree and the CLI.
- **Replacement of Codex or any specific coding assistant.** DAI is the discipline layer that *augments* whichever assistant the team already uses.

## Release Cadence

- **Patch releases (v1.0.x):** as needed for doctrine refinements, security fixes, and template improvements
- **Minor releases (v1.x.0):** quarterly, gated on contributor input and concrete adoption signal
- **Major releases (vX.0.0):** only when the doctrine surface changes in a way that breaks existing installs

## How to Influence the Roadmap

Open an issue. Argue from a concrete experience — what you tried, what happened, what should have happened. Doctrine evolves through written argument, not voting.
