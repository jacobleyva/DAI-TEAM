---
title: The Algorithm
type: rule
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
version: v1.1
tags:
  - algorithm
  - operating-loop
  - doctrine
artifact_type: operating-rule
---

# The Algorithm

> **Read this file before any non-trivial work.** It defines the universal loop the team and your coding-assistant CLI use to transition from a current state to an ideal state. Every multi-step task runs through these phases. Trivial single-edits do not — see `tier` rules below.

## Doctrine

**Every Algorithm run does one thing: transition from CURRENT STATE to IDEAL STATE.** The mechanism: articulate the ideal state as testable criteria (ISCs — see `core/ISC.md`), pursue them through phases, verify each one met. Same loop applies in any domain: code, infrastructure, documentation, governance, research.

**The WORK note is the system of record for a task.** When you start a non-trivial task, create `memory/work/{slug}.md` with frontmatter (`task`, `slug`, `phase`, `progress`, `started`, `updated`, `reasoning_effort`) and the ISCs as a checklist. Each phase edits this file. The WORK note IS the test harness — passing every ISC means the task is done.

**The unit of work is the thing being articulated, not the prompt.** For a project with persistent identity, the WORK note lives at `projects/{name}/WORK.md` and grows continuously across many tasks. For ad-hoc work, `memory/work/{slug}.md` is created at OBSERVE and archived at LEARN.

## Tier Rules

| Tier | Trigger | Use the loop? | WORK note? | Reasoning effort |
|------|---------|---------------|-----------|------------------|
| **Quick** | Single-file edit, single command, single fact lookup. No new artifact. | No — skip to execution | No | `low` (no extended thinking) |
| **Standard** | Multi-file, multi-step, anything ambiguous, anything touching `core/`, `memory/`, or `projects/{name}/` doctrine | Yes — full loop | Yes | `medium` (extended thinking on THINK + VERIFY) |
| **Deep** | Architecture decisions, cross-project changes, governance updates, anything that will be referenced again | Yes — full loop with explicit Decisions log | Yes | `high` (extended thinking on THINK + PLAN + VERIFY) |

**Bias toward Standard when in doubt.** Under-scoping is the failure mode this loop was built to prevent.

### Reasoning Effort — vendor-neutral budget signal

The WORK note's `reasoning_effort:` frontmatter is a vendor-neutral budget signal. Each vendor's harness maps it to the model's native control:

- **OpenAI Codex / GPT family** → `reasoning_effort: low | medium | high` (native parameter)
- **Anthropic Claude** → extended-thinking budget tokens (`low` ≈ 0 budget, `medium` ≈ 8K, `high` ≈ 24K+)
- **Google Gemini** → `thinkingConfig.thinkingBudget` (`low` ≈ 0, `medium` ≈ 2048, `high` ≈ 8192)
- **Other vendors** → map to their nearest equivalent; if none, ignore the field

The doctrine produces the *signal*; the harness produces the *behavior*. This lets DAI exploit native reasoning controls without vendor-specific code in the doctrine.

## The Six Phases

Every Standard or Deep task runs through these phases in order. Output the phase header line before each phase's work. Edit the WORK note's `phase:` frontmatter at every transition.

### 1. OBSERVE

Echo the user's intent in one sentence. **If you cannot restate it accurately, re-read the request.**

```
👁️ INTENT: [one-sentence restatement of what user actually asked for]
```

Then:
- Reverse-engineer the request: what is explicitly wanted, what is explicitly not wanted, what is implied not wanted, what is the speed signal
- Identify the WORK note location and create it if it doesn't exist
- Set the tier (Quick/Standard/Deep) and write it to frontmatter
- Set `reasoning_effort` per the table above
- Run preflight gates that match the task — diagnostic, deploy/API, external-service, research

```
🚦 PREFLIGHT:
 🚦 [gate]: [finding]
```

**Capture-Current-State rule (generalized from earlier Reproduce-First):** before any change, capture the current state of what's about to change. Cost is one extra probe; benefit is deterministic verification of effect and regression detection.

| Task shape | Required pre-change snapshot |
|------------|------------------------------|
| Bug fix / "X is broken" | A reproduction artifact — `curl`, screenshot, stdout, log line, `SELECT` |
| New feature | Grep for the new symbol/file (expect zero matches); a `curl` 404 against the not-yet-existing endpoint |
| Config change | `Read` of the config file before edit |
| Schema/DB change | `SELECT` of the existing schema or representative rows |
| Refactor | Test runner output passing before the refactor |
| Doctrine edit | The verbatim quote of the rule being changed |

The pre-change snapshot is the baseline against which the change is verified. Without it, the "after" probe proves nothing about the change's effect.

**End OBSERVE by writing the initial ISC list to the WORK note.** Apply the Splitting Test (see `core/ISC.md`): every criterion is one binary tool probe. Include at least one anti-criterion (what MUST NOT happen). Mark independent ISCs with the same `parallel_group:` so VERIFY can batch them in one turn.

### 2. THINK

Write to the WORK note under `## Risks`:

```
🎲 RISKIEST ASSUMPTIONS: [items the work depends on being true]
⚰️ PREMORTEM: [failure modes the work must withstand]
☑️ PREREQUISITES: [blockers and how preflight findings affect them]
```

Then refine ISCs. Add criteria for the premortem failure modes. Re-apply the Splitting Test. Drop or split as needed. Group ISCs by `parallel_group:` where parallelization is safe (independent probes, no shared mutable state).

### 3. PLAN

Output the scope and the deliverable manifest. Every explicit sub-task in the user's request is its own line item.

```
📐 SCOPE: [depth | breadth | breadth-then-depth] — [why]
📦 DELIVERABLES:
 📦 D1: [user sub-task — quote distinctive phrasing]
 📦 DN: [user sub-task]
```

Each deliverable must map to ≥1 ISC. **A deliverable without a matching ISC is a missed criterion — add it before EXECUTE.**

**Parallelism plan.** Walk the ISC list and identify groups that can be verified in a single turn (one model response, multiple parallel tool calls). Modern LLM tool harnesses support this natively — using it gives a free 2–4× speedup on the VERIFY phase.

```
🚀 PARALLEL GROUPS:
 🚀 group-A: ISC-1, ISC-3, ISC-7 — independent HTTP probes, safe to batch
 🚀 group-B: ISC-2, ISC-4 — independent file reads, safe to batch
 🚀 sequential: ISC-5, ISC-6 — depend on ISC-1 outcome, must run after
```

For code work: read the surrounding files, name the integration points, identify the upstream/downstream effects. Document significant decisions in the WORK note `## Decisions` log with timestamp.

**Root-cause-at-ingestion checkpoint:** before any fix that modifies output-side behavior, answer:

1. Where does this bad state enter the system? Name the ingestion point.
2. If I fix it at the ingestion point instead of here, do similar bugs disappear? If yes — move the fix upstream.
3. Am I tracing database-up or display-down? For UI bugs, the Capture-Current-State rule forces display-down.

**Stop-the-line rule:** if the user said "make a plan", end here. Do not execute without explicit approval.

### 4. EXECUTE

Do the work. Edit files. Run commands. Apply changes.

**As each ISC passes, immediately mark it `[x]` in the WORK note and append evidence under `## Verification`:**

```
ISC-N: [probe type] — [one-line evidence: command output or file content]
```

**Inline verification mandate.** No ISC may transition from `[ ]` to `[x]` without a tool-call probe in the same block or the immediately-following block.

| ISC type | Required probe |
|----------|----------------|
| File write | Read the file back, confirm content |
| Code edit | Grep for the new symbol, or Read the specific range |
| Command execution | Captured stdout/stderr |
| HTTP/API change | `curl -i` with status + body check |
| Deploy | Live URL probe showing deployed version |
| UI change | Browser screenshot at the target route |
| Schema/DB change | `SELECT` confirming the migration landed |
| Config change | Read-back of the file confirming the new value |

**Forbidden language:** "should work", "should be", "expected to", "the change is in place" (without Read/Grep), "done" (without tool evidence), "no errors" (without the actual log).

### The ISC Failure → THINK Loop

> Real engineering iterates. The Algorithm's phases are not strictly linear — they form a loop with one defined back-edge.

When an ISC probe at EXECUTE or VERIFY fails:

1. **Do not silently retry.** Capture the failure as evidence under `## Verification`.
2. **Return to THINK.** Write the failure as a refutation of the assumption that produced the ISC. Update `RISKIEST ASSUMPTIONS` (which one did the failure refute?). Re-split or refine the offending ISC if its shape was wrong.
3. **Return to EXECUTE.** Apply the refined approach.
4. **Cap at 3 attempts.** On the 4th failure of the same ISC, escalate to the user with all three attempts as the evidence chain — do not keep iterating in isolation.

```
🔁 ISC-N failure → THINK
 🔁 attempt 1: [what was tried, what failed, what it refuted]
 🔁 attempt 2: [what was tried, what failed, what it refuted]
 🔁 attempt 3: [what was tried, what failed]
 🔁 escalating to user — assumption refuted: [name the assumption]
```

This is the only sanctioned back-edge in the Algorithm. It catches the real engineering pattern (try → fail → re-think → try again) without permitting infinite-loop thrash.

### 5. VERIFY

For every ISC, confirm it passed with tool-verified evidence. Cite the probe.

**Run parallel-group ISCs in batched tool calls.** If `core/ISC.md`-conformant ISCs are tagged `parallel_group: A`, verify them in a single turn (one model response, multiple parallel tool calls). This is the principal speedup the Algorithm exploits on modern LLMs.

```
✅ VERIFICATION:
 ISC-N: [method used] — [evidence summary]
 Coverage: N/N passed
```

**Deliverable compliance check** — walk each D1..DN from PLAN and confirm it shipped:

```
📦 DELIVERABLE COMPLIANCE:
 📦 D1: [✓ shipped | ✗ missed | DEFERRED — reason]
```

**Re-read check** — final gate. Re-read the user's most recent message verbatim. For each explicit ask, confirm it was addressed:

```
🔄 RE-READ:
 🔄 [ask 1 — quote distinctive phrasing]: [✓ addressed | ✗ missed]
```

Any `✗` blocks completion. Either ship the missing piece or surface it as a known gap before declaring done.

### 6. LEARN

Reflect. Write to the WORK note under `## Learnings`:

```
🧠 LEARNING:
 🧠 What should I have done differently?
 🧠 What would a smarter operator have done?
 🧠 Did preflight gates fire? Were they useful or wasted?
 🧠 Did the Capture-Current-State rule fire? Did it catch anything?
 🧠 Did the ISC failure loop fire? How many attempts before resolution?
 🧠 Did parallel-group batching actually run in parallel?
```

If something durable was learned — a rule, a gotcha, a piece of knowledge about a system or person — route it to the right surface:

| Type | Target |
|------|--------|
| Rule | `core/constitution.md` or `core/decision-rules.md` |
| Gotcha for a specific skill | That skill's `SKILL.md` |
| Knowledge about a system | `knowledge/collections/{topic}.md` |
| State to resume later | `memory/current-focus.md` |
| Decision that future work needs | `memory/decisions/{date}_{slug}.md` |
| Session summary | `memory/session-summaries/{date}_{slug}.md` |

Set `phase: complete` in the WORK note. If the work belonged to a project, also update that project's `projects/{name}/Overview.md`.

## Mandatory Closing Format

Every Standard or Deep run ends with this block. Zero exceptions.

```
━━━ SUMMARY ━━━
🔄 ITERATION on: [16 words of context — omit on first response]
📃 CONTENT: [the actual content if any]
🖊️ STORY: [4 bullets of ~8 words each — problem, action, result, next]
🗣️ NEXT: [one-sentence handoff or pause point]
```

After this block: nothing.

## Rules

- **No phantom phases.** If you skip a phase, name which one and why in the WORK note `## Decisions`.
- **Verification is required.** Tool-verified evidence per ISC. "Looks fine" is not evidence.
- **Parallel groups run in parallel.** If an ISC is tagged `parallel_group:`, the VERIFY phase must batch it with its peers in a single response. Sequential verification of independent probes is a doctrine violation.
- **ISC failures route back to THINK.** Three attempts max; escalate on the fourth. Do not silently retry.
- **WORK note is the source of truth.** Not chat history. Not memory alone.
- **No silent stalls.** If you're stuck for more than three investigative loops on the same ISC, write what you tried and surface the blocker.
- **Plan means stop.** Explicit "plan first" requests end at PLAN.
- **The Algorithm is for the team, not just one CLI.** A human teammate should be able to read a WORK note and continue the task without you.

## Why Six Phases

Six phases is the granularity the doctrine has converged on. Setup-reasoning lives in PLAN (where decisions get made before doing); the actual work lives in EXECUTE (where ISCs flip and evidence is captured). Splitting setup and execution into separate phases produces more ceremony than value — the model context-switches without earning anything from the split. Six phases maps cleanly to Deming/PDCA (Plan-Do-Check-Act expanded with explicit observation, thinking, and learning) and is the shape the team operates in.

## Why This Exists

The doctrine in this file is what makes the discipline portable across coding-assistant CLIs. A model with strong intrinsic discipline (Claude with hooks and a native Agent primitive) can fly on lighter scaffolding. A model with weaker intrinsic discipline (Codex without hooks) needs the scaffolding spelled out in the workspace. Same operational floor by different routes. Read this file; follow it; let it guide every non-trivial task.
