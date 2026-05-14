---
title: Agent Composition
type: rule
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
version: v1.0
tags:
  - agents
  - composition
  - delegation
  - skills
artifact_type: operating-rule
---

# Agent Composition

> **Codex does not have a native `Agent(subagent_type=...)` primitive like Claude Code does.** It has skills. So in this workspace, *agents are properties of skills, not free-floating identities.* When a skill needs delegated behavior — a sub-task with a different persona, a different model, or a different rule set — the skill carries an `agents/{vendor}.yaml` spec that defines how the delegation works.

## The Convention

Every skill that wants delegated behavior puts its agent specs in a vendor-named YAML under its own `agents/` subdirectory:

```
skills/
├── <skill-name>/
│   ├── SKILL.md
│   ├── workflows/
│   │   └── <workflow-name>.md
│   ├── references/
│   │   └── <reference-name>.md
│   └── agents/
│       ├── openai.yaml         ← Codex / OpenAI-family spec
│       ├── anthropic.yaml      ← (optional) Claude-family spec
│       └── google.yaml         ← (optional) Gemini-family spec
```

The vendor filenames are exact: `openai.yaml`, `anthropic.yaml`, `google.yaml`. Other vendors get their own filename when adopted. The team avoids generic names like `agent.yaml` because the whole point is to make the vendor-specific contract visible.

## What an Agent Spec Looks Like

The minimum schema:

```yaml
interface:
  display_name: "Skill Display Name"
  short_description: "One-line description shown when picking the skill."
  default_prompt: "The system-like prompt that activates this skill in this vendor's harness."
```

The optional schema for richer delegation:

```yaml
interface:
  display_name: "..."
  short_description: "..."
  default_prompt: "..."

model:
  family: "gpt-5"        # or "claude-4.6", "gemini-3-pro"
  reasoning_effort: high # vendor-specific knob
  temperature: 0.7

tools:
  allow: ["filesystem", "web_search"]
  deny: ["shell"]

handoff:
  return_format: "markdown"
  required_sections: ["Findings", "Open Questions"]
```

Only the `interface` block is required. Add the optional blocks when the delegation actually needs them — speculative configuration is a known anti-pattern (`core/constitution.md` ALWAYS rule: prefer the smallest reversible step).

## When to Add an Agent Spec

A skill earns an `agents/{vendor}.yaml` when one of these is true:

1. **The skill needs to behave differently across vendors.** Codex and Claude do the same job but Codex needs more explicit guardrails — the `default_prompt` differs.
2. **The skill is opinionated about model selection.** A code-review skill might require a high-reasoning model; a synthesis skill might prefer a fast one.
3. **The skill needs to control its tool surface.** A read-only skill that should never touch the filesystem benefits from a `tools.deny: ["filesystem"]` spec.
4. **The skill produces a structured handoff.** When the downstream consumer (another skill, a human reviewer, a stakeholder summary) expects specific sections.

A skill **does not need** an agent spec when:

- The skill is generic and runs the same way across all vendors.
- The skill is a thin wrapper around a single command.
- The skill is brand-new and the team hasn't decided how it should differ.

Start without an agent spec. Add one when the skill's behavior across vendors actually diverges.

## How Codex Picks It Up

Codex's `~/.codex/config.toml` declares which skill paths are active:

```toml
[[skills.config]]
path = "/absolute/path/to/workspace/skills/<skill-name>"
enabled = true
```

When the skill activates and an `agents/openai.yaml` is present, Codex reads `interface.default_prompt` and adds it to the active prompt for that skill invocation. Other vendor specs are ignored when Codex is the active harness.

For Claude Code (if the same workspace is also used there), the equivalent of agent specs is the native `Agent(subagent_type=...)` primitive — the YAML is read by tooling that bridges into Claude Code, not by Claude Code itself. The convention is *Codex-first* because this workspace's design pressure is to externalize Codex's discipline.

## The Architectural Reason

Claude Code has hooks and a native subagent primitive — agent identity lives in the *harness*. Codex doesn't. If the workspace lets agents float free (a `team/agents/` directory unrelated to skills), Codex has no deterministic way to find them at activation time. Anchoring agents to skills means Codex finds them naturally when it activates the skill.

This is another instance of DAI's core architectural finding: Claude Code lets identity be ambient because the harness threads it through; Codex needs identity to be *located* — adjacent to the skill that needs it.

## How to Add a New Vendor

When the team adopts a new model vendor:

1. Pick the canonical filename (e.g. `anthropic.yaml`, `meta.yaml`, `mistral.yaml`).
2. Add the file alongside existing vendor specs in the skill that needs it.
3. Copy the `interface` block from the closest existing vendor spec; rewrite `default_prompt` for the new vendor's instruction style.
4. Document the new vendor's harness-side wiring (the equivalent of Codex's `skills.config` block) in `core/CODEX_INTEGRATION.md` or a new `core/{vendor}_INTEGRATION.md`.
5. Add the vendor to this file's list of recognized vendor filenames.

## What This File Does NOT Do

- It does not define the actual prompts. Each skill's `agents/{vendor}.yaml` does.
- It does not enforce a maximum number of vendors. Add as many as the team genuinely uses.
- It does not require every skill to have an agent spec. Most skills won't need one.

## Related

- `skills/skills-map.md` — index of skills in this workspace
- `core/CODEX_INTEGRATION.md` — how Codex wires skills.config
