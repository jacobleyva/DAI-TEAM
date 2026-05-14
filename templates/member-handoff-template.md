---
title: Member Handoff Template
type: template
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
tags:
  - template
  - handoff
artifact_type: template
---

# Member Handoff — {{outgoing-name}} → {{incoming-name}}

> A handoff that a stranger can read cold and pick up the work without a walkthrough. Date everything; cite files by path.

## Header

- **Outgoing owner:** {{outgoing-name}}
- **Incoming owner:** {{incoming-name}}
- **Handoff date:** {{date}}
- **Last working day in role:** {{date}}
- **Coverage during transition:** {{name and contact for questions in the first 2 weeks}}

## Status

| Area | State | Evidence | Confidence |
|------|-------|----------|-----------|
| {{Current sprint / cycle}} | {{green / yellow / red — one phrase}} | {{path to active project file or PR}} | {{high / medium / low}} |
| {{Open commitments}} | | | |
| {{Vendor / external relationships}} | | | |
| {{Pending decisions}} | | | |
| {{Operational health}} | | | |

## Next Step

> The single action the incoming owner should take in their first working session.

1. {{First concrete step — read this file at this path, run this command, attend this meeting}}
2. {{Second concrete step}}
3. {{Third concrete step}}

## Blockers

| Blocker | Owner to unblock | Channel | Expected resolution |
|---------|------------------|---------|---------------------|
| {{blocker 1}} | {{name / team}} | {{Slack / email / ticket}} | {{date or trigger}} |
| {{blocker 2}} | | | |

## Living Context

- **Where the work lives:** {{paths into `projects/`, `memory/`, external repos}}
- **What to read first (in order):** {{file 1, file 2, file 3 — annotated with why}}
- **Who knows what:** {{name → domain mapping for institutional knowledge that isn't yet in files}}
- **Recent decisions worth absorbing:** {{paths to decision logs or PR threads}}
- **Conventions that aren't obvious from the code:** {{the local norms a new reader would miss}}

## Open Threads

- {{Conversation in flight — channel, last update, expected next move}}
- {{External commitment in flight — vendor, date, owner}}
- {{Internal commitment in flight — owner, deadline}}

## Sunset Plan

- **Re-evaluate this handoff on:** {{date — typically 30 / 60 / 90 days after transition}}
- **Signal that the handoff is complete:** {{specific observable — incoming owner has shipped X, made decision Y, closed thread Z}}
- **Archive trigger:** {{when this file moves from active to archived state}}
