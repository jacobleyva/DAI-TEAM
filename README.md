---
title: DAI — Domain AI Infrastructure
type: overview
domain: dai
product: DAI
audience: technical-teams
owner: team
status: active
updated: 2026-05-14
version: v1.0
tags:
  - start-here
  - overview
  - workspace
  - bootstrap
  - dai
artifact_type: workspace-overview
---

# DAI — Domain AI Infrastructure

> **DAI ties an actual brain to Codex.** Codex on its own is a sharp tool with no memory and a goldfish's attention span. DAI is the persistent reasoning scaffold that gives it discipline — a constitution it reads at every session start, an algorithm it follows for non-trivial work, an EFFECTUS substrate that grounds decisions in the team's actual mission, and a verification doctrine that refuses unverified claims. Drop DAI into your repo, point Codex at it, and the next session knows what the last one decided.

---

## What This Is

A Git-backed operating workspace for technical teams that run their daily output through Codex (or any Codex-shaped coding-assistant CLI). DAI's premise: *the discipline lives in the files, not in the model.* Same workspace, different teammates, same operational floor — what one session produces composes cleanly with what another did yesterday.

## Who It's For

Engineers, platform, infrastructure, SRE-adjacent — anyone whose work feels the model drift session to session because the scaffolding around it is thin. If you've ever opened a new Codex session and watched it re-litigate a decision the team made a week ago, that's the problem DAI solves.

## 30-Second Install

From the repo root, after `git clone`:

```sh
./bootstrap.sh
```

That's it. `bootstrap.sh`:

1. Verifies prerequisites (`python3`, `git`; optionally `pdftotext` for PDF ingest)
2. Generates `memory/session-context.md` — the file your coding-assistant CLI reads at every session start
3. Generates `memory/skills-catalog.md` — one-line-per-skill index
4. Installs the pre-commit hooks (frontmatter validation + secret-pattern scan)
5. Prints the per-vendor wiring snippet for your CLI of choice (Codex / Claude Code / Gemini CLI / others)

After running `./bootstrap.sh`, the path forks by which CLI you use:

**OpenAI Codex:**

1. Paste the printed `developer_instructions` block into `~/.codex/config.toml` (or run `tools/scripts/install-codex-config.py` to wire it safely)
2. Start Codex from this directory
3. Ask: *"What's in memory/session-context.md? Summarize what this workspace is and what rules I'm operating under."* — Codex confirms the workspace context loaded

Every subsequent Codex session reads `memory/session-context.md` automatically via `developer_instructions`.

**Anthropic Claude Code:**

No config edit needed — `CLAUDE.md` at the repo root is already wired. Start Claude Code from this directory and the `@`-import in `CLAUDE.md` pulls `memory/session-context.md` into every session start. Ask the same first prompt to confirm.

**Google Gemini CLI:**

No config edit needed — `GEMINI.md` at the repo root is already wired. Start Gemini CLI from this directory and it loads `GEMINI.md` automatically, which references `memory/session-context.md` for the synthesized startup context. Ask the same first prompt to confirm.

**Cursor:**

No config edit needed — `.cursorrules` at the repo root is already wired. Open the repo in Cursor and the rules load automatically on every session. Works on all Cursor versions (legacy `.cursorrules` is still supported alongside the newer `.cursor/rules/` format). Ask the same first prompt to confirm.

**Aider, GitHub Copilot Chat, Continue, Cody, or any other coding-assistant CLI:** the doctrine is vendor-neutral; the only piece that needs adaptation is the startup wiring file. See `core/AI_CLI_ADAPTERS.md` for the per-vendor convention table with concrete adapter recipes.

## What's in the Box

DAI is plain markdown, plain shell, plain Python. No daemons, no telemetry, no cloud service. The discipline is the file shape.

- `core/` — durable rules and standards: the constitution, the algorithm, the ISC granularity discipline, the verification doctrine, effort tiering, agent composition, the Codex integration recipe.
- `memory/` — durable shared state, including the `effectus/` substrate (mission, goals, beliefs, wisdom, challenges, strategies, models) that grounds every session.
- `projects/` — active workstreams. One folder per project; templates show the shape.
- `knowledge/` — curated reference material. Use `bin/dai-knowledge process` to ingest PDFs, DOCX, HTML, MD, CSV.
- `templates/` — reusable note formats. Run `tools/scripts/eval_templates.py` to verify quality.
- `skills/` — reusable AI workflows. Each skill is a folder with `SKILL.md` + optional per-vendor agent specs. Includes security-review, threat-modeling, incident-response, and 6 more.
- `team/` — collaboration and handoff conventions.
- `tools/scripts/` — the deterministic discipline layer (frontmatter check, repo health, knowledge indexing, session bootstrap, dependency audit, Codex config helper).
- `bin/` — executables (`dai-knowledge` and others).
- `.githooks/` — pre-commit guardrails.

## Why It Helps

- **Work is restartable.** State lives in files. A session that ends mid-task can be picked up by anyone — yourself tomorrow, a teammate next week — without a walkthrough.
- **Teammates reach the same operating context.** Same files, same rules, same algorithm. Decisions compose instead of conflict.
- **Decisions become durable.** Logged in the project's `log.md`; surfaced in the next session's auto-loaded context.
- **The workspace grows without turning into one giant note.** Discipline lives in folder shape, not in one file's length.
- **New sessions orient quickly.** No re-learning what the system is; the system reads itself at startup.
- **AI coding assistants behave consistently across sessions.** Because the rules are *enforced* at pre-commit and *re-read* at every session start, not *remembered*.

## Plug In to Your Repo Stack

DAI is repo-source-neutral. The same pre-commit hook, same `tools/scripts/*` checks, same skills, same doctrine — running on either platform.

- **GitHub** — CI ships at `.github/workflows/dai-checks.yml`; PR template at `.github/PULL_REQUEST_TEMPLATE.md`; review routing via `.github/CODEOWNERS`; issue templates for install reports and doctrine-change proposals
- **Azure DevOps Repos + Azure Pipelines** — CI ships at `azure-pipelines.yml`; PR template at `.azuredevops/pull_request_template.md`; review routing via branch policy "Automatically include reviewers" (path-scoped)

Side-by-side enablement steps live in `core/REPO_INTEGRATION.md`. Both stacks are first-class — pick whichever your team already runs.

## AI Coding Assistant — LLM-Agnostic by Design

DAI is vendor-neutral. The doctrine — constitution, six-phase Algorithm, ISC granularity, verification doctrine, EFFECTUS substrate, skills, templates, knowledge — does not depend on which coding-assistant CLI reads it. Only the startup-wiring file differs per vendor. DAI ships four of those wiring files in the box and documents the convention for everything else.

**First-class wired (shipped in the repo):**

| Vendor | Wiring file | How it loads at session start |
|--------|-------------|-------------------------------|
| **OpenAI Codex** (GPT family) | `~/.codex/config.toml` `developer_instructions` block (substituted by `bootstrap.sh` / `tools/scripts/install-codex-config.py`) | Codex reads `developer_instructions` on every session start; the block points it at `memory/session-context.md` |
| **Anthropic Claude Code** (Claude family) | `CLAUDE.md` at repo root | Claude Code reads `CLAUDE.md` on every session start; the `@`-import pulls `memory/session-context.md` |
| **Google Gemini CLI** (Gemini family) | `GEMINI.md` at repo root | Gemini CLI reads `GEMINI.md` on every session start; the file references `memory/session-context.md` for the synthesized context |
| **Cursor** (model of user's choice — Claude / GPT / Gemini) | `.cursorrules` at repo root | Cursor reads `.cursorrules` on every session start; works on legacy and current Cursor versions (also copyable to `.cursor/rules/dai.mdc` for the newer structured format) |

Across the four, the same `memory/session-context.md` file is the actual payload — the doctrine, the EFFECTUS substrate, the skills catalog. The wiring file is just a vendor-specific pointer. The architectural finding is that **discipline lives in the workspace, not in the model**: a vendor-neutral substrate is the natural shape of that idea.

**Adaptable to other CLIs (documented convention, no shipped file):**

| Vendor | Wiring file convention |
|--------|-----------------------|
| Aider | `.aider.conf.yml` with `read-only` / `chat-history` paths |
| GitHub Copilot Chat | `.github/copilot-instructions.md` (repo-level instructions) |
| Continue | `.continuerc.json` with `systemMessage` pointing at session-context |
| Cody (Sourcegraph) | `.sourcegraph/codycontext.md` |
| Any future CLI | Whatever the vendor's "load at session start" convention is — the doctrine itself doesn't change |

See `core/AI_CLI_ADAPTERS.md` for the full table with concrete adapter recipes per vendor.

The doctrine itself never branches per vendor. The constitution's NEVER list, the Algorithm's six phases, ISC granularity, the EFFECTUS substrate — those run identically regardless of which CLI consumes them. Switching CLIs (or running multiple in parallel for different team members) requires zero changes to `core/`, `memory/`, `skills/`, or `templates/`.

The architectural finding behind DAI: **Claude Code lets the harness be light because the model carries discipline; Codex needs the harness to be deterministic because the model won't.** Different design pressures, same destination. The doctrine itself — constitution, Algorithm, ISC, verification doctrine, EFFECTUS substrate, skills, templates, knowledge — is vendor-neutral. Only the startup-wiring file differs per vendor.

For other coding-assistant CLIs (Cursor, Aider, etc.), the doctrine still applies; the integration recipe is the only piece that needs an adapter. A documented adapter pattern is on the roadmap; contributions welcome.

## Doctrine Tour

The discipline layer is short, by design. The doctrine files in `core/` total under 6,000 words. Read them in this order on day one:

1. `core/operating-principles.md` — the why
2. `core/algorithm.md` — the how
3. `core/isc.md` — the granularity discipline that makes verification possible
4. `core/verification-doctrine.md` — what counts as evidence
5. `core/constitution.md` — the NEVER list

That's the spine. The rest extends it.

## Validation Status

The maintainers have run the full install flow on two machines. The third-machine validation — a fresh `git clone` + `./bootstrap.sh` on a host that has never seen DAI before — is open. If you run it, please open an issue with the transcript whether it passes or fails. That signal is the most useful first contribution a new user can make.

## Contributing

See `CONTRIBUTING.md`. The short version: read the three doctrine files first, never bypass pre-commit, never claim a criterion passed without tool-verified evidence, and disagree on the doctrine — never on the contributor.

## Security

See `SECURITY.md`. Report vulnerabilities privately via GitHub Security Advisory on this repo, not via public issues.

## Roadmap

See `ROADMAP.md`. The doctrine evolves through written argument, not voting.

## License

Apache License 2.0. See `LICENSE`.

