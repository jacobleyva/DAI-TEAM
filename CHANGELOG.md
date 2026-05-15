---
title: CHANGELOG
type: reference
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
tags:
  - changelog
  - versioning
artifact_type: changelog
---

# CHANGELOG

## v1.1 — 2026-05-14 — Vendor-Neutral Skill CLI

Added `bin/dai-skill`, the vendor-neutral primitive for skill discovery and on-demand load. Every coding-assistant CLI DAI supports — Codex, Claude Code, Gemini CLI, Cursor, Aider, and any shell-capable future entrant — uses the same convention via shell-out, no per-vendor slash-command implementation needed.

### What's New

```sh
bin/dai-skill list           # one line per skill: name + description
bin/dai-skill show <name>    # print the full SKILL.md to stdout
bin/dai-skill path <name>    # print the absolute path
bin/dai-skill help           # print full usage
```

Python 3 stdlib only. Auto-detects the workspace root (or accepts `--workspace` / `PAI_WORKSPACE`). Reads `skills/*/SKILL.md` frontmatter (`name:` and `description:`) — adding a new skill requires only creating the file; the CLI auto-discovers it with no registration step.

### Why a CLI Instead of Per-Vendor Slash Commands

Slash commands (`/dai-security-review`, `/skill ...`) are a Claude Code / Cursor surface that doesn't exist under Codex, Gemini CLI, or Aider. Building the discovery layer once as a CLI gives every vendor the same UX via shell-out, composes with standard tools (`bin/dai-skill list | grep security`), and keeps the source of truth in the `skills/` tree rather than duplicated across N vendor-specific command directories.

The full rationale lives in `core/AI_CLI_ADAPTERS.md` under "Skill Discovery & Loading — `bin/dai-skill`".

### Why Not Eager-Load Every SKILL.md

Each `SKILL.md` is ~100-200 lines. Loading all 9 into every session burns ~1,500 lines of context for skills that won't be invoked. The CLI's `list` returns ~10 lines (one per skill); `show` only fires when a skill is actually being run. Cheap discovery, on-demand load — the same pattern that `bin/dai-knowledge` uses for knowledge ingestion.

### Wiring Files Updated

All four vendor surfaces now teach their models to use the CLI:

- `CLAUDE.md` — Claude Code wiring
- `GEMINI.md` — Gemini CLI wiring
- `.cursorrules` — Cursor wiring
- `tools/scripts/install-codex-config.py` — Codex `developer_instructions` block
- `bootstrap.sh` heredoc Codex template + new "Step C — Skill discovery" block in the end-of-run output
- `core/CODEX_INTEGRATION.md` — Codex integration recipe
- `core/AI_CLI_ADAPTERS.md` — added the canonical "Skill Discovery & Loading" section

`skills/skills-map.md` remains as a human-browsable index. `memory/skills-catalog.md` remains as the auto-generated session-context catalog. No skill content changed.

---

## v1.0 — 2026-05-14 — DAI Team Launch

DAI Team v1.0 — *Discipline Externalized*. Initial public release.

The discipline layer lives in the files, not in the model. Drop DAI into a repo, point your coding-assistant CLI (Codex, Claude Code, Gemini CLI, Cursor, Aider, or others) at it, and the next session knows what the last one decided.

### LLM-Agnostic Wiring

DAI is vendor-neutral by design. The doctrine never branches per coding-assistant CLI — the constitution, the six-phase Algorithm, ISC granularity, the EFFECTUS substrate, the skills, the templates, the knowledge collections all run identically across vendors. Only the startup-wiring file differs.

DAI ships four wiring files in the box:

- **OpenAI Codex** → `~/.codex/config.toml` `developer_instructions` block (substituted by `bootstrap.sh` / `tools/scripts/install-codex-config.py`)
- **Anthropic Claude Code** → `CLAUDE.md` at repo root
- **Google Gemini CLI** → `GEMINI.md` at repo root
- **Cursor** (model of your choice — Claude / GPT / Gemini) → `.cursorrules` at repo root

Per-vendor adapter recipes for Aider, GitHub Copilot Chat, Continue, and Cody live in `core/AI_CLI_ADAPTERS.md` — adding a new CLI is a self-contained wiring file, no doctrine changes required.

### Security Response Windows — Community-Project Floors, Not Enterprise SLAs

`SECURITY.md` declares response-window targets sized for a community-maintained open-source project. Critical issues get an initial response within 3 working days and a target fix window of 14 days; non-critical issues scale from there. These are deliberately not enterprise-grade SLAs — DAI is currently maintained by a small group of contributors on a best-effort basis. Teams adopting DAI in their own fork are encouraged to tighten the windows to match their staffing.

### What Ships

**Core doctrine (`core/`)**

- Constitution — hard-imperative NEVER / ALWAYS / BEFORE rules
- Algorithm — six-phase loop (OBSERVE → THINK → PLAN → EXECUTE → VERIFY → LEARN) with one sanctioned back-edge: ISC failure routes to THINK, max 3 attempts before escalation
- ISC (Ideal-State Criteria) — granularity discipline; one binary tool probe per criterion; `parallel_group:` tag for batched verification on modern LLMs
- Verification doctrine — what counts as evidence; Capture-Current-State rule — every non-trivial change captures the pre-change state for deterministic effect-verification
- Effort tiering — Quick / Standard / Deep tiers; each maps to a vendor-neutral `reasoning_effort:` signal (`low` / `medium` / `high`) that LLM harnesses translate to native controls (GPT `reasoning_effort`, Claude extended-thinking budget, Gemini `thinkingConfig`)
- Agent composition — `skills/{name}/agents/{vendor}.yaml` convention for vendor-specific skill behavior
- Operating principles, decision rules, style guide, frontmatter standard, core-map
- Codex integration recipe — TOML-aware wiring, four documented pitfalls, recovery path
- AI CLI adapters — per-vendor wiring conventions for Codex, Claude Code, Gemini CLI, Cursor, Aider, Copilot Chat, Continue, Cody
- Repo-source integration — side-by-side enablement for GitHub and Azure DevOps Repos
- Security domain overview — task routing, doctrine, output conventions

**EFFECTUS substrate (`memory/effectus/`)**

The long-arc-intent substrate that grounds every session in the team's actual mission:

- Mission, goals, beliefs, wisdom, challenges, strategies, models, effectus-map

**Skills (`skills/`)**

9 reusable AI workflows, each with `SKILL.md` entry point and optional per-vendor agent specs:

- security-review (workflows: code-audit, config-audit)
- threat-modeling (workflows: STRIDE, attack-tree, kill-chain)
- incident-response (workflows: triage, containment, postmortem)
- cis-controls — align designs to CIS Controls v8.1
- code-review, feature-spec-writer, planning, repo-onboarding, research-synthesizer

**Templates (`templates/`)**

7 reusable note formats — all pass `tools/scripts/eval_templates.py`:

- executive-stakeholder-summary, learning, member-handoff, project-entry, session-summary
- threat-model, incident-response

**Knowledge collections (`knowledge/collections/`)**

- CIS Critical Security Controls v8.1 — 18 controls / 153 safeguards / 3 Implementation Groups
- OWASP Top 10 (2021) — web-app risks with CWE mappings
- OWASP API Security Top 10 (2023) — API-specific risks
- CWE Top 25 (2024) — most dangerous software weakness types

**Memory (`memory/security/`)**

- Threat landscape — 6 industry-baseline threats with org-tuning slots
- Auth patterns — IdP / MFA / mTLS / JWT / session / secrets defaults
- Incident log — append-only schema with quarterly rollup

**CI workflows — first-class on either repo stack**

- GitHub Actions: `.github/workflows/dai-checks.yml`
- Azure Pipelines: `azure-pipelines.yml`
- PR templates: `.github/PULL_REQUEST_TEMPLATE.md`, `.azuredevops/pull_request_template.md`
- GitHub issue templates: install-report, doctrine-change
- Review routing: `.github/CODEOWNERS` + Azure branch-policy translation guide in `core/REPO_INTEGRATION.md`

**Discipline tooling (`tools/scripts/`, `.githooks/`)**

- Pre-commit hook — frontmatter validation + 13-pattern secret scan
- `secret_scan_diff.sh` — same regex set applied to a diff between two refs (used by CI)
- `dep_audit.py` — multi-ecosystem dependency auditor (pip + npm + cargo + go + bundler)
- `eval_templates.py` — verifies templates have real content, not stubs
- `check_front_matter.py` — strict frontmatter shape check
- `check_repo_health.py` — repo inventory and drift detection
- `build_session_context.sh` — synthesizes the Codex startup payload
- `install-codex-config.py` — TOML-aware Codex config wiring (refuses to clobber, writes backup, round-trip validates)
- `install_git_hooks.sh` — pre-commit hook installer
- `skills_index.sh` — auto-generates `memory/skills-catalog.md`

**One-command bootstrap (`bootstrap.sh`)**

After `git clone`:

```sh
./bootstrap.sh
```

Verifies prerequisites, generates session-context, installs pre-commit hooks, prints the exact `~/.codex/config.toml` block with the workspace path substituted, prints the recommended first prompt.

### Validation Pending

The acceptance bar for v1.0 includes one criterion that cannot be verified by the maintainers alone: a fresh `git clone` + `./bootstrap.sh` on a machine that has never seen DAI before, followed by a Codex session confirming the doctrine loaded. The maintainers have run this on two machines so far. The third-machine validation is open and is the most useful first contribution a new user can make — see `.github/ISSUE_TEMPLATE/install-report.md`.
