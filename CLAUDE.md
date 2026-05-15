# DAI System — Claude Code Wiring

> Claude Code reads this file at every session start. It's the Claude-side equivalent of Codex's `developer_instructions` block in `~/.codex/config.toml` — the entry point that loads DAI's doctrine, current focus, and skills catalog into the session before any work begins.

## Session Bootstrap

The synthesized startup context lives in `memory/session-context.md`. Claude Code `@`-imports load that file automatically on session start:

@memory/session-context.md

That single file catenates the constitution, the six-phase Algorithm, the ISC granularity discipline, the verification doctrine, effort tiering, identity, current focus, and the skills catalog. Regenerate it after any change to its sources with `tools/scripts/build_session_context.sh`.

## What To Follow

For any **non-trivial work** (multi-file, ambiguous, touching `core/`, `memory/`, or `projects/{name}/`):

- Run the six-phase Algorithm. See `core/ALGORITHM.md`. Phases: OBSERVE → THINK → PLAN → EXECUTE → VERIFY → LEARN.
- Create a WORK note at `memory/work/{slug}.md` (or `projects/{name}/WORK.md` for project work). The WORK note is the system of record.
- Write acceptance criteria per `core/ISC.md`. Every criterion is one binary tool probe. Apply the Splitting Test.
- Hold to the verification doctrine. See `core/verification-doctrine.md`. Tool-verified evidence required before marking any ISC `[x]`.
- Read the constitution. See `core/constitution.md`. The NEVER / ALWAYS / BEFORE rules are non-negotiable defaults.

For **skills**, use the vendor-neutral CLI:

- `bin/dai-skill list` — one line per skill, name + description (cheap discovery, no eager file reads)
- `bin/dai-skill show <name>` — print the full `SKILL.md` to stdout, on-demand
- `bin/dai-skill path <name>` — print the absolute path (use with `@` for Claude Code's file reference)

The CLI is the universal primitive — same convention works under Codex, Gemini CLI, Cursor, Aider, or any shell-capable assistant. Skills remain on disk at `skills/<name>/SKILL.md`; `skills/skills-map.md` stays for human browsing.

For **security work** (review, threat-modeling, incident-response), route through `core/SECURITY_DOMAIN_OVERVIEW.md`.

## Claude Code-Specific Notes

- **Hooks.** Claude Code's `PreToolUse` / `PostToolUse` / `SessionStart` hooks are not required by DAI but can add runtime enforcement on top of the pre-commit floor. The pre-commit hook at `.githooks/pre-commit` already covers frontmatter validation and secret-pattern scanning; hooks would complement, not replace.
- **Subagents.** Claude Code's native `Agent(subagent_type=...)` primitive can read a skill's `agents/anthropic.yaml` spec when present (the per-vendor convention documented in `core/agent-composition.md`). Most skills don't need a vendor-specific spec.
- **The architectural reason DAI exists.** *Claude Code lets the harness be light because the model carries discipline; Codex needs the harness to be deterministic because the model won't.* DAI externalizes discipline that Claude Code provides intrinsically — which means DAI on Claude is a tighter scaffold than Claude strictly needs. The upside is cross-vendor portability: the same file shape runs identically under Codex, Cursor, Aider, or any future coding-assistant CLI.

## Keep Higher-Priority Instructions in Force

This file adds DAI scaffolding on top of Claude Code's defaults. It does not replace Claude Code behavior or override the user's active prompt. When in doubt, the active prompt wins; DAI doctrine wins on anything the active prompt doesn't speak to.

## Verifying the Wiring

In a fresh Claude Code session, ask:

> What's in `memory/session-context.md`? Summarize what this workspace is and what rules I'm operating under.

If Claude describes the constitution, the Algorithm, the ISC doctrine, the verification doctrine, the effort tiering, the identity, and the skills catalog — the wiring works. If Claude says it doesn't see the file, the `@`-import resolved to nothing; either the file is missing (regenerate via `tools/scripts/build_session_context.sh`) or the path is wrong.

## Related

- `~/.codex/config.toml` `developer_instructions` block — the Codex-side equivalent of this file. See `core/CODEX_INTEGRATION.md`.
- `core/SECURITY_DOMAIN_OVERVIEW.md` — task routing across security skills.
- `core/REPO_INTEGRATION.md` — GitHub vs Azure DevOps wiring for the CI surface.
