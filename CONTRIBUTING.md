---
title: Contributing to DAI
type: reference
domain: dai
product: DAI
audience: contributors
owner: team
status: active
updated: 2026-05-14
tags:
  - contributing
  - onboarding
artifact_type: contributor-guide
---

# Contributing to DAI

> DAI — Domain AI Infrastructure — is a discipline layer that lives in files, not in models. Contributions are welcome. The bar is that every contribution leaves the doctrine sharper than it found it.

## Before You Open a PR

Read these three files, in this order. They are short.

1. `core/constitution.md` — the hard-imperative rules. The NEVER list below quotes the ones that bite hardest.
2. `core/operating-principles.md` — how the doctrine is meant to be applied day-to-day.
3. `core/verification-doctrine.md` — what counts as evidence. "Looks fine" is not evidence.

If a change you want to make would weaken any of those three, raise it in an issue first. The doctrine evolves through written argument, not silent edits.

## The Constitution's NEVER List

These rules are non-negotiable. A PR that violates one of them will be sent back without further review, regardless of how good the rest of it is.

- **NEVER bypass safety checks.** No `--no-verify` on commits; no commenting out pre-commit hooks; no disabling the secret scanner. If a hook fires, fix the underlying cause.
- **NEVER programmatically modify `~/.codex/config.toml`.** The TOML schema is rigid; line-based edits break it. Use `tools/scripts/install-codex-config.py` for any wiring change.
- **NEVER claim a criterion passed without tool-verified evidence.** "Should work" / "looks fine" / "expected to" are not evidence. The probe goes in `## Verification` with the actual output.
- **NEVER commit secrets.** Tokens, API keys, OAuth secrets, private SSH keys. The pre-commit hook scans for common shapes (`sk-...`, `AIza...`, `ghp_...`, `xoxb-...`). If you trip it, rotate the secret before pushing the fix.
- **NEVER skip the frontmatter.** Every markdown file in `core/`, `memory/`, `skills/`, `templates/` carries YAML frontmatter. The pre-commit hook blocks files without it. Use `tools/scripts/check_front_matter.py` to audit locally.

The full list lives in `core/constitution.md`. Read it before your first contribution; it is shorter than this file.

## Pre-commit Hook

DAI ships a pre-commit hook at `.githooks/pre-commit`. It runs two checks before every commit:

1. **Frontmatter check** — every modified markdown file in a managed directory (`core/`, `memory/`, `projects/`, `team/`, `knowledge/`, `templates/`, `skills/`) must open with `---` YAML frontmatter. The specific field shape is enforced by `tools/scripts/check_front_matter.py` (callable manually); the hook itself just verifies the file opens with `---`.
2. **Secret-pattern scan** — 16 patterns covering the major secret shapes (AWS classic + STS, OpenAI, Anthropic, PEM keys, Slack, GitHub classic PAT, GitHub fine-grained PAT, GitLab PAT, Azure storage AccountKey, GCP API key, GCP service-account JSON, Stripe, Twilio SID + auth token, JWT). The patterns are deliberately conservative; false positives are cheaper than false negatives.

Enable the hook on a fresh clone:

```sh
tools/scripts/install_git_hooks.sh
```

`bootstrap.sh` does this automatically on first run. If you've already cloned without bootstrapping, run the install script once.

**If the hook fires:** read its output carefully. It names the file and the line. Fix the cause; don't bypass.

## Skill Scaffolding

DAI's `skills/` directory holds the reusable workflows AI coding assistants compose with. Each skill is a self-contained folder with a `SKILL.md` entry point.

Add a new skill in three steps.

### 1. Scaffold the directory

```sh
mkdir -p skills/your-skill-name
touch skills/your-skill-name/SKILL.md
```

Optional: `Workflows/`, `Tools/`, `References/` subdirectories for skills with deeper internals.

### 2. Write the `SKILL.md`

Skills use the Anthropic-style minimal frontmatter — just `name` and `description`. This matches the upstream skill convention so a SKILL.md drops into Codex or Claude Code without modification:

```yaml
---
name: your-skill-name
description: "One sentence — what this skill does, when to invoke, NOT FOR list."
---
```

The richer DAI frontmatter standard (`title`, `type`, `domain`, `product`, `audience`, `owner`, `status`, `updated`, `tags`, `artifact_type` — see `core/front-matter-standard.md`) applies to durable shared files in `core/`, `memory/`, `projects/`, `templates/`, `knowledge/`, and `team/`. Skills are intentionally outside that schema to stay vendor-portable.

The body must cover:

- **Purpose** — one paragraph, what this skill exists to do
- **When to use** — concrete trigger phrases or task shapes
- **NOT FOR** — what this skill is explicitly the wrong tool for, with pointers to the right tool
- **Inputs** — what the skill expects from its caller
- **Outputs** — what shape the skill returns
- **Workflows** — the named subroutines, each one a heading
- **Gotchas** — the rakes that bit a previous user; one line each; dated

Reference: `skills/security-review/SKILL.md` is a good shape to copy.

### 3. Register and verify

Run `tools/scripts/skills_index.sh` to regenerate `memory/skills-catalog.md`. Run `tools/scripts/eval_templates.py` if your skill also adds templates. Commit; the pre-commit hook validates frontmatter shape and scans the diff for secret patterns.

A new skill is "done" when the catalog lists it, the frontmatter passes, and a second contributor can read the `SKILL.md` cold and invoke the workflow without asking questions.

## Repo Source — GitHub and Azure DevOps Repos

DAI is repo-source-neutral. The same pre-commit hook, the same `tools/scripts/*` checks, and the same PR template (just at the platform-expected path) run on both. Pick whichever platform your team already runs:

- **GitHub** — CI lives at `.github/workflows/dai-checks.yml`; PR template at `.github/PULL_REQUEST_TEMPLATE.md`; review routing via `.github/CODEOWNERS`
- **Azure DevOps Repos + Pipelines** — CI lives at `azure-pipelines.yml`; PR template at `.azuredevops/pull_request_template.md`; review routing via branch policy "Automatically include reviewers"

Side-by-side enablement steps live in `core/REPO_INTEGRATION.md`. The two pipelines stay in lockstep — if you change one CI workflow, change the other in the same PR.

## Filing Issues

Issues are welcome. Two GitHub issue templates ship with this repo:

- **Install Report (CR-5)** — for fresh-clone install transcripts, pass or fail
- **Doctrine Change Proposal** — for any change to `core/`

Azure DevOps Repos teams: the same shapes apply; create matching work item types or paste the issue-template body into the description. For broader technical reports, read `templates/learning-template.md` and `templates/threat-model-template.md` first.

For doctrine disagreements (something in `core/` you think should change), open the issue with:

- The exact file and line you want changed
- The current rule, quoted
- The proposed replacement, written out
- The concrete situation that drove the proposal — a reproducible scenario, not a hypothetical

## Review Cadence

- PRs are reviewed within five working days
- Doctrine changes (anything in `core/`) require a second reviewer
- Security-domain changes (anything in `skills/security-*`, `templates/threat-model-*`, `memory/security/`) require review from a security-domain owner

## Code of Conduct

Be sharp about ideas, kind about people. Disagree on the doctrine, never on the contributor. That's the whole policy.
