---
title: Codex Integration
type: reference
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
version: v1.0
tags:
  - codex
  - integration
  - config
  - developer-instructions
artifact_type: integration-guide
---

# Codex Integration

> How to wire this workspace into Codex so the doctrine, identity, and current focus load deterministically at every session start.

## The Design Pressure (Read This First)

Claude Code has `@-imports` in `CLAUDE.md` that auto-load files at session start. Codex does not have an equivalent — its closest mechanism is the `developer_instructions` block inside `~/.codex/config.toml`, which is a static string set when Codex starts.

**Two consequences:**

1. The startup payload has to be a **single file** that we point Codex at, not a list of files to remember.
2. That single file has to be **generated**, not hand-maintained — otherwise it drifts from the source files in `core/` and `memory/`.

The solution is `tools/scripts/build_session_context.sh` (synthesizes the context) plus the `config.toml` directive below (tells Codex to read it).

## Step 1 — Generate the Session Context

From the workspace root:

```sh
tools/scripts/build_session_context.sh
```

This writes `memory/session-context.md`. The script is idempotent — run it after any change to `core/`, `memory/identity.md`, `memory/current-focus.md`, or the skills map.

Verify the output:

```sh
wc -l memory/session-context.md
head -40 memory/session-context.md
```

## Step 2 — Wire Codex's `developer_instructions`

**Recommended path (TOML-aware, idempotent):**

```sh
tools/scripts/install-codex-config.py
```

This script reads `~/.codex/config.toml`, refuses to clobber an existing `developer_instructions` (rerun with `--force` to overwrite), writes a timestamped backup, prepends `developer_instructions` at the **top of the file** (as a top-level key — must appear before any `[section]` header), adds a `[projects."<this-workspace>"]` entry with `trust_level = "trusted"`, and round-trip-validates the resulting TOML before saving.

Flags:

- `--dry-run` — print the proposed new file to stdout without writing
- `--workspace PATH` — wire a workspace other than the one the script lives in (defaults to the script's own repo root)
- `--config PATH` — target a config file other than `~/.codex/config.toml`
- `--force` — overwrite an existing `developer_instructions` block

**Manual path (if you cannot run Python or want to inspect by hand):** see Step 2.5 below — read the Critical Pitfalls first; the manual path is where every known config break has happened.

The block the script writes is:

```toml
developer_instructions = """
This workspace is at WORKSPACE_PATH.

At the start of every session, read WORKSPACE_PATH/memory/session-context.md.
That file is the synthesized startup context: constitution, algorithm, ISC
doctrine, identity, current focus, decision rules, and the skills catalog.

For any non-trivial work (multi-file, ambiguous, or touching core/, memory/,
or projects/{name}/), follow core/ALGORITHM.md — create a WORK note at
memory/work/{slug}.md and run the six phases (Observe, Think, Plan,
Execute, Verify, Learn).

For acceptance criteria, follow core/ISC.md — every criterion is one binary
tool probe; tool-verified evidence required before marking [x].

For skills, use the vendor-neutral CLI at bin/dai-skill:
  bin/dai-skill list           list every skill, one line each (cheap discovery)
  bin/dai-skill show <name>    print the full SKILL.md to stdout (on-demand load)
  bin/dai-skill path <name>    print the absolute path
This convention is shared by every coding-assistant CLI DAI supports.
skills/skills-map.md remains as a human-browsable index.

Keep higher-priority system instructions in force. Use this workspace as
added scaffolding, not as a replacement for Codex behavior.
"""

[projects."WORKSPACE_PATH"]
trust_level = "trusted"
```

`WORKSPACE_PATH` is substituted with the workspace's real absolute path.

## Step 2.5 — Critical Pitfalls (read before any manual edit)

The single highest-cost defect this workspace has ever produced was Codex auto-editing `~/.codex/config.toml` and breaking its own ability to launch. The failure mode is mechanical and reproducible — these are the four pitfalls that combine to cause it.

### Pitfall 1 — `developer_instructions` is a TOP-LEVEL key

It must appear in `config.toml` **before any `[section]` header**. TOML scoping is positional: every key after a `[section]` header is owned by that section until the next header. If `developer_instructions = """..."""` lands after `[tui.model_availability_nux]`, the parser tries to validate the string against that section's schema (declared as `u32`-only model availability counts) and refuses the file with:

```
Error loading config.toml: invalid type: string "...", expected u32 in `tui.model_availability_nux`
```

Codex then refuses to launch — no fallback, no defaults, no graceful degradation. One bad key = no app.

✅ **Correct (top of file, before any `[section]`):**

```toml
model = "gpt-5.4-mini"

developer_instructions = """
...
"""

[projects."/path/to/workspace"]
trust_level = "trusted"
```

❌ **Wrong (after a section header):**

```toml
[tui.model_availability_nux]
"gpt-5.5" = 4
developer_instructions = """     # ← parser binds this to [tui.model_availability_nux] → schema break
...
"""
```

### Pitfall 2 — Codex must NOT auto-edit `~/.codex/config.toml`

Codex's Edit tool is line-based and TOML-AST-blind. When asked (or implicitly invited by a "check that config has X" test step) to fix a missing `developer_instructions`, Codex will append the key at end-of-file. End-of-file is almost always inside a `[section]` — see Pitfall 1.

The constitution forbids this: `NEVER programmatically modify ~/.codex/config.toml`. If a session asks Codex about config wiring, Codex should surface the change in `## Decisions` for operator-manual application, or recommend `tools/scripts/install-codex-config.py`. **Do not invite Codex to auto-fix the wiring.**

### Pitfall 3 — TextEdit silently corrupts TOML

macOS TextEdit's default mode is rich-text. Opening `config.toml` in TextEdit and saving it converts straight quotes `"` to smart quotes `"` `"` — TOML's parser does not recognize smart quotes as string delimiters, and the file becomes invalid with errors like:

```
key with no value, expected '='
```

Use `nano`, `vim`, `micro`, VS Code, or any plain-text editor. Verify after edit with:

```sh
file ~/.codex/config.toml      # should say: ASCII text  or  UTF-8 Unicode text
```

If it says `RTF` or anything else, TextEdit (or another rich-text editor) corrupted it.

### Pitfall 4 — Terminal paste can break long array lines

The `notify = [...]` line in a typical Codex config is ~200+ chars. Pasting into Terminal occasionally inserts a soft-wrap newline into the middle of the array, producing:

```
toml 4:3: missing comma between array elements, expected ','
```

When writing long arrays via heredoc, **break them across lines manually**:

```toml
notify = [
    "/path/with spaces/to/some/long/binary",
    "turn-ended",
]
```

The `install-codex-config.py` helper handles this automatically — multi-line array form for any value >80 chars.

### Recovery — if config.toml is already broken

```sh
ls -t ~/.codex/config.toml.bak.* | head -1 | xargs -I{} cp {} ~/.codex/config.toml
codex
```

Restores the most recent timestamped backup (created by `install-codex-config.py` or any previous safe-wiring run).

## Step 3 — Refresh on Source Changes

Every time someone edits one of the files synthesized into `memory/session-context.md`, the synthesized file drifts. Two options for keeping it current:

**Option A — Manual refresh (simplest):**

```sh
tools/scripts/build_session_context.sh
git add memory/session-context.md
git commit -m "refresh session context"
```

**Option B — Pre-commit git hook (recommended for active teams):**

Add this hook to `.git/hooks/pre-commit` (or install via `tools/scripts/install_git_hooks.sh` if you have it):

```sh
#!/bin/sh
# Auto-regenerate session-context.md when its source files change.
if git diff --cached --name-only | grep -qE '^(core/|memory/identity\.md|memory/current-focus\.md|skills/skills-map\.md|LAUNCHER\.md|active-work-map\.md)'; then
    tools/scripts/build_session_context.sh
    git add memory/session-context.md
fi
```

That keeps the synthesized file in lockstep with its sources.

## Step 4 — Confirm Codex Is Reading It

In a fresh Codex session, ask:

> "What's in memory/session-context.md?"

If Codex describes the constitution + Algorithm + ISC + identity + current focus, the wiring works. If Codex says "I don't see that file", the path in `developer_instructions` is wrong or the file wasn't generated.

## What This Does NOT Do

- **No hooks.** Codex does not have `PreToolUse`/`PostToolUse`/`SessionStart` hook events. If you want runtime checks (security inspection, pattern matching), put them in a **git pre-commit hook** instead. The workspace already ships `tools/scripts/install_git_hooks.sh` for that pattern.
- **No subagents.** Codex does not have a native `Agent(subagent_type=...)` primitive. If a skill needs delegation, the skill itself defines the shape of the sub-call (e.g. a CLI it invokes). The convention is to put per-vendor agent specs in `skills/{name}/agents/{vendor}.yaml` — see `core/agent-composition.md` for the schema.
- **No voice.** Skip the voice-announcement pattern entirely.

## Compared to Claude Code's DAI

| Concern | Claude Code's DAI | This Workspace |
|---------|-------------------|----------------|
| Startup context load | `@-imports` in `CLAUDE.md` | Synthesized `memory/session-context.md` + `config.toml` `developer_instructions` |
| Phase enforcement | Hooks + model self-discipline | The WORK note format + the team reading it |
| Runtime tool inspection | `hooks/security/inspectors/*.ts` | Pre-commit git hooks |
| Specialized agents | `Agent(subagent_type=...)` | Per-skill `agents/{vendor}.yaml` specs |
| Verification | `Verification Doctrine` + hooks | Inline `## Verification` evidence in WORK notes |

The architectural finding: **Claude Code lets the harness be light because the model carries discipline. Codex needs the harness to be deterministic because the model won't.** This workspace externalizes the discipline that Claude Code provides intrinsically. That's not a weakness of Codex — it's a different design pressure with the same destination.
