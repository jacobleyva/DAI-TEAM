---
name: Doctrine Change Proposal
about: Propose a change to anything in `core/` — the constitution, algorithm, ISC, verification doctrine, effort tiering, agent composition, or operating principles.
title: "[Doctrine] <file>: <one-line proposed change>"
labels: doctrine, needs-discussion
assignees: ''
---

<!--
Doctrine evolves through written argument, not silent edits. Before sending a
PR that changes `core/`, open this issue so the rationale gets debated in the
open.
-->

## Target File and Line

- **File:** `core/<filename>.md`
- **Line(s):** <e.g. 42-48>
- **Current rule, quoted verbatim:**

> <paste the exact existing text>

## Proposed Replacement

> <paste the exact text you want to replace it with>

## Driving Situation

<!-- A reproducible scenario that the current rule fails to handle. Concrete —
     a specific session, a specific PR, a specific failure mode. Not a
     hypothetical "what if". -->

## Why The Current Rule Fails

<!-- What the current rule produced in the driving situation, and why that
     outcome is wrong by the rule's own stated goal. -->

## Why The Proposed Rule Is Better

<!-- The mechanism — first-principles, not just symptom. What does the new
     rule cover that the old one doesn't? -->

## Cost of Change

- [ ] Touches one file in `core/`
- [ ] Touches multiple files in `core/`
- [ ] Affects existing PRs in flight (list them below)
- [ ] Affects existing skills (list which `SKILL.md` files need to react)
- [ ] Affects templates (list which templates need to change)
- [ ] Affects the pre-commit hook
- [ ] Affects CI workflows (`.github/workflows/` and/or `azure-pipelines.yml`)

## Migration Plan

<!-- If the change isn't atomic, how do existing workspaces upgrade? What's
     the order of operations? -->

## Falsification Condition

<!-- What would we see later that would prove the new rule was the wrong
     call? Write this so future-you can revisit honestly. -->

## Linked Discussions / Sessions / PRs

<!-- Slack threads, prior issues, PR conversations, session-summaries that
     gave rise to this proposal. -->
