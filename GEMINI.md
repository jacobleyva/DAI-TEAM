# DAI System — Google Gemini CLI Wiring

> Google Gemini CLI reads this file at every session start. It's the Gemini-side equivalent of Codex's `developer_instructions` block in `~/.codex/config.toml` and Claude Code's `CLAUDE.md` — the entry point that loads DAI's doctrine, current focus, and skills catalog into the session before any work begins.

## Session Bootstrap

The synthesized startup context lives in `memory/session-context.md`. That single file catenates the constitution, the six-phase Algorithm, the ISC granularity discipline, the verification doctrine, effort tiering, identity, current focus, and the skills catalog.

**Read `memory/session-context.md` at the start of every session.** Treat it as the operating context for any non-trivial work. Regenerate it after any change to its sources with `tools/scripts/build_session_context.sh`.

If your Gemini CLI version supports markdown file references, follow the path above. If it requires inline content, the bootstrap script's printed wiring snippet provides the equivalent.

## What To Follow

For any **non-trivial work** (multi-file, ambiguous, touching `core/`, `memory/`, or `projects/{name}/`):

- Run the six-phase Algorithm. See `core/ALGORITHM.md`. Phases: OBSERVE → THINK → PLAN → EXECUTE → VERIFY → LEARN. The single sanctioned back-edge is an ISC failure routing back to THINK (max 3 attempts before escalation).
- Create a WORK note at `memory/work/{slug}.md` (or `projects/{name}/WORK.md` for project work). The WORK note is the system of record.
- Write acceptance criteria per `core/ISC.md`. Every criterion is one binary tool probe. Apply the Splitting Test. Tag independent ISCs with `parallel_group:` so VERIFY can batch them in a single response (Gemini's parallel-tool-call support exploits this directly).
- Hold to the verification doctrine. See `core/verification-doctrine.md`. Tool-verified evidence required before marking any ISC `[x]`.
- Read the constitution. See `core/constitution.md`. The NEVER / ALWAYS / BEFORE rules are non-negotiable defaults.

For **skills**, use the vendor-neutral CLI:

- `bin/dai-skill list` — one line per skill, name + description (cheap discovery, no eager file reads)
- `bin/dai-skill show <name>` — print the full `SKILL.md` to stdout, on-demand
- `bin/dai-skill path <name>` — print the absolute path

The CLI is the universal primitive — same convention works under Codex, Claude Code, Cursor, Aider, or any shell-capable assistant. Skills remain on disk at `skills/<name>/SKILL.md`; `skills/skills-map.md` stays for human browsing.

For **security work** (review, threat-modeling, incident-response), route through `core/SECURITY_DOMAIN_OVERVIEW.md`.

## Gemini-Specific Notes

- **Reasoning budget.** Map DAI's `reasoning_effort:` field (`low` / `medium` / `high` in the WORK note frontmatter) to Gemini's `thinkingConfig.thinkingBudget`. Recommended: `low` → 0, `medium` → 2048, `high` → 8192. The doctrine sets the signal; Gemini's harness chooses how to spend it. See `core/effort-tiering.md` for the full vendor-mapping table.
- **Parallel tool calls.** Gemini supports parallel function calls in a single response. ISCs tagged `parallel_group:` MUST be verified by batching the probes in one turn rather than serializing them. This is the primary speedup DAI's v1.1 Algorithm exploits.
- **Long context window.** Gemini's 1M+ token context lets the entire `memory/session-context.md` plus relevant `core/` files fit comfortably without context pressure. Use the room — fold the full doctrine into your operating context rather than reading on-demand.
- **Per-skill agent specs.** When a skill needs Gemini-specific behavior, drop a `skills/<skill-name>/agents/google.yaml` file alongside `openai.yaml` and `anthropic.yaml`. See `core/agent-composition.md` for the schema. Most skills don't need a vendor-specific spec.

## Keep Higher-Priority Instructions in Force

This file adds DAI scaffolding on top of Gemini CLI's defaults. It does not replace Gemini behavior or override the user's active prompt. When in doubt, the active prompt wins; DAI doctrine wins on anything the active prompt doesn't speak to.

## Verifying the Wiring

In a fresh Gemini CLI session, ask:

> What's in `memory/session-context.md`? Summarize what this workspace is and what rules I'm operating under.

If Gemini describes the constitution, the Algorithm, the ISC doctrine, the verification doctrine, the effort tiering, the identity, and the skills catalog — the wiring works. If Gemini says it doesn't see the file, the path resolution failed; either the file is missing (regenerate via `tools/scripts/build_session_context.sh`) or the wiring needs adjustment for your Gemini CLI version's file-loading convention.

## Related

- `~/.codex/config.toml` `developer_instructions` block — the Codex-side equivalent of this file. See `core/CODEX_INTEGRATION.md`.
- `CLAUDE.md` — the Claude Code-side equivalent of this file.
- `core/SECURITY_DOMAIN_OVERVIEW.md` — task routing across security skills.
- `core/REPO_INTEGRATION.md` — GitHub vs Azure DevOps wiring for the CI surface.
- `core/AI_CLI_ADAPTERS.md` — per-vendor wiring conventions for Cursor, Aider, Copilot Chat, Continue, Cody, and others.
