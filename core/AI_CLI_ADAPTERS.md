---
title: AI Coding-Assistant CLI Adapters
type: reference
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
version: v1.1
tags:
  - llm-agnostic
  - cli-adapters
  - integration
  - vendor-neutral
artifact_type: integration-guide
---

# AI Coding-Assistant CLI Adapters

> DAI is vendor-neutral by design. The doctrine never branches per coding-assistant CLI — the constitution's NEVER list, the six-phase Algorithm, ISC granularity, the EFFECTUS substrate, the skills, the templates all run identically across vendors. **Only the startup-wiring file differs.** This document is the table of those wiring conventions plus concrete adapter recipes.

## Shipped Wirings — First-Class

DAI ships three vendor-specific wiring files in the box:

| Vendor | Wiring file | Auto-installed? | Doctrine file |
|--------|-------------|----------------|---------------|
| OpenAI Codex (GPT family) | `~/.codex/config.toml` `developer_instructions` block | `bootstrap.sh` prints the block; `tools/scripts/install-codex-config.py` writes it safely | `core/CODEX_INTEGRATION.md` |
| Anthropic Claude Code (Claude family) | `CLAUDE.md` at repo root | Already in repo — no install step | `CLAUDE.md` itself |
| Google Gemini CLI (Gemini family) | `GEMINI.md` at repo root | Already in repo — no install step | `GEMINI.md` itself |

All three reference `memory/session-context.md` as the actual payload. The synthesized context is the same; the wiring is just a vendor-specific pointer.

## Adapter Recipes — Other CLIs

### Cursor

Cursor reads instruction files from either `.cursorrules` (legacy single-file) or `.cursor/rules/*.md` (newer multi-file structured rules). Both are at the repo root.

**Minimal adapter:**

```
# .cursorrules
This workspace is DAI (Domain AI Infrastructure). See memory/session-context.md
at the start of every session — it catenates the constitution, the six-phase
Algorithm, ISC doctrine, verification doctrine, effort tiering, identity,
current focus, and the skills catalog.

For non-trivial work, follow core/ALGORITHM.md (OBSERVE → THINK → PLAN →
EXECUTE → VERIFY → LEARN, with ISC failure routing back to THINK, max 3
attempts before escalation).

For acceptance criteria, follow core/ISC.md — every criterion is one binary
tool probe. Tag independent ISCs with parallel_group: to batch verification.

For the constitution's NEVER list, see core/constitution.md.
```

Map DAI's `reasoning_effort:` field to Cursor's model-selection (Cursor uses different model tiers; high → top-tier model, low → fast model).

### Aider

Aider reads `.aider.conf.yml` at the repo root. The doctrine wiring goes in the `read` field (files Aider auto-loads as read-only context):

```yaml
# .aider.conf.yml
read:
  - memory/session-context.md
  - core/constitution.md
  - core/ALGORITHM.md
  - core/ISC.md
  - core/verification-doctrine.md
```

Aider auto-includes these in every session's context. For larger context budgets, add `skills/skills-map.md` and the relevant `core/SECURITY_DOMAIN_OVERVIEW.md` etc.

### GitHub Copilot Chat (repo-level instructions)

GitHub Copilot Chat (in VS Code, JetBrains, etc.) reads `.github/copilot-instructions.md` for repo-level instructions:

```markdown
# .github/copilot-instructions.md
This workspace is DAI (Domain AI Infrastructure). When working in this repo,
follow the doctrine in `memory/session-context.md` — it carries the constitution,
the six-phase Algorithm, ISC granularity discipline, and the verification
doctrine.

For non-trivial work: create a WORK note at memory/work/{slug}.md, run the
Algorithm, mark ISCs [x] only with tool-verified evidence.

NEVER claim a criterion passed without showing the probe output.
NEVER edit files outside this workspace without an explicit instruction.
NEVER bypass safety checks (--no-verify, hook disabling, etc.).
```

### Continue.dev

Continue uses `.continuerc.json` or `config.json` at the user level. For repo-specific instructions, set `systemMessage` to reference the workspace:

```json
{
  "systemMessage": "When working in this repository, read memory/session-context.md for the operating context. Follow the six-phase Algorithm in core/ALGORITHM.md for non-trivial work. Use one-binary-tool-probe ISCs per core/ISC.md. Tool-verified evidence required before marking any ISC complete."
}
```

### Cody (Sourcegraph)

Cody reads `.sourcegraph/codycontext.md` or `.cody/instructions.md` depending on version:

```markdown
# .sourcegraph/codycontext.md
DAI workspace. Operating context at memory/session-context.md. Six-phase
Algorithm at core/ALGORITHM.md. Constitution at core/constitution.md.
ISC doctrine at core/ISC.md. Verification doctrine at core/verification-doctrine.md.

Follow the doctrine on any non-trivial task.
```

## Per-Vendor Reasoning-Effort Mapping

DAI's WORK note carries `reasoning_effort: low | medium | high`. Each vendor's harness maps it to native controls:

| DAI signal | OpenAI GPT family | Anthropic Claude | Google Gemini | Cursor | Others |
|------------|-------------------|------------------|---------------|--------|--------|
| `low` | `reasoning_effort: low` | extended-thinking budget 0 | `thinkingBudget: 0` | fast model | minimum reasoning |
| `medium` | `reasoning_effort: medium` | ~8K tokens | ~2048 | mid-tier model | balanced reasoning |
| `high` | `reasoning_effort: high` | ~24K+ tokens | ~8192 | top-tier model | maximum reasoning |

The doctrine produces the *signal*; the harness produces the *behavior*. Vendors lacking a reasoning-budget control ignore the field — the doctrine remains valid.

## Per-Vendor Parallel-Tool-Call Support

DAI's `parallel_group:` ISC tag instructs the VERIFY phase to batch probes in a single response. Vendor support today:

| Vendor | Parallel function/tool calls in one response | DAI parallel_group exploits this? |
|--------|----------------------------------------------|-----------------------------------|
| OpenAI Codex / GPT family | Yes (native) | Fully |
| Anthropic Claude | Yes (native) | Fully |
| Google Gemini | Yes (native) | Fully |
| Cursor | Yes (depends on selected model) | Inherited from underlying model |
| Aider | Sequential by design | No — `parallel_group:` runs serially |
| GitHub Copilot Chat | Variable by version | Best-effort |
| Continue | Yes for supported models | Yes for GPT/Claude/Gemini-backed |

Where parallel-call support exists, DAI's VERIFY phase compresses N independent probes into one round-trip. Where it doesn't, the same probes run serially but the doctrine remains identical — the `parallel_group:` tag becomes a hint, not a directive.

## Adding a New CLI

When a new coding-assistant CLI is adopted:

1. Identify its convention for "load at session start" instruction file (it will have one; every modern CLI does).
2. Create a thin wiring file at the convention's location that references `memory/session-context.md` for the operating context and the relevant `core/*.md` doctrine files.
3. Document the convention in this file's "Adapter Recipes" section.
4. If the CLI supports a reasoning-budget control, add its mapping to the `reasoning_effort:` table above.
5. If the CLI supports parallel tool calls, mark it `Yes` in the parallel-tool-call table.
6. Submit a PR — the addition is a self-contained adapter, no doctrine changes required.

## Why This Architecture Works

The clean separation between doctrine and wiring is what makes DAI vendor-neutral. A user adopting DAI on Codex today and switching to Gemini CLI next year changes one wiring file — everything else (the constitution, the Algorithm, the EFFECTUS substrate, the skills, the workflows, the templates, the knowledge collections, the CI pipelines) stays untouched.

A team running Codex on some workstations and Claude Code on others operates from the same doctrine, the same workflows, the same skills catalog. Decisions made in one session compose with decisions made in another regardless of which CLI authored them. That's the operational guarantee LLM-agnosticism actually buys.

## Related

- `core/CODEX_INTEGRATION.md` — Codex-specific wiring with four documented pitfalls
- `CLAUDE.md` — Claude Code wiring (the actual file in production)
- `GEMINI.md` — Gemini CLI wiring (the actual file in production)
- `core/agent-composition.md` — per-skill `agents/{vendor}.yaml` convention for vendor-specific skill behavior
- `core/effort-tiering.md` — reasoning-effort mapping per tier
- `core/ISC.md` — the `parallel_group:` ISC primitive
