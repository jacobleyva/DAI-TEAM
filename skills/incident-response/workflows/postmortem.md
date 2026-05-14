---
title: Workflow — Postmortem
type: workflow
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
tags:
  - security
  - incident-response
  - workflow
  - postmortem
  - blameless
artifact_type: skill-workflow
---

# Workflow: Postmortem

Blameless retro to extract durable learning from an incident. Scheduled within 7 days of recovery. Output: postmortem doc + tracked action items + entry in `memory/security/incident-log.md`.

## Doctrine

- **Blameless.** Process and system failures, not people failures. If a person made a mistake, the system allowed the mistake. Fix the system.
- **Five whys plus.** Don't stop at "Alice deployed bad config." Keep asking why until you reach a systemic cause — usually 4–7 levels deep.
- **Action items must be specific, owned, and dated.** "Improve monitoring" is not an action item. "Add Datadog monitor for X with PagerDuty escalation, owned by @y, due YYYY-MM-DD" is.
- **Publish even when embarrassing.** Hidden incidents repeat.

## Phase 1 — Prep (T-24h before the meeting)

The IC drafts a timeline-only document:

- Reconstructed sequence: `<timestamp UTC> — <action / event> — <actor / system>` rows.
- Source artifacts referenced (logs, channel messages, ticket IDs).
- No analysis, no blame, no fixes yet — just facts.

Share draft 24h in advance. Attendees pre-read.

**Exit probe:** timeline draft circulated; attendees confirmed.

## Phase 2 — Meeting (60–90 min)

**Attendees:** IC, Scribe, Tech Lead, service owner(s), one senior engineer outside the response (fresh eyes), security leadership for SEV-1/2.

**Agenda:**

1. **Walk the timeline** (15 min) — IC narrates; participants correct / add missing events.
2. **Detection retrospective** (10 min) — Could we have detected sooner? What signal existed but wasn't surfaced? What detection didn't exist?
3. **Containment retrospective** (10 min) — Were containment actions effective? Anything that surprised us (took longer, didn't work, made it worse)?
4. **Five-whys on the root cause** (15 min) — start with the immediate trigger, ask why iteratively. Capture each level.
5. **Ishikawa / fishbone** (15 min, optional for complex incidents) — for incidents with multiple contributing factors, categorize:
   - People: training, staffing, communication
   - Process: runbooks, change mgmt, on-call
   - Tools: detection, response, recovery
   - Environment: dependencies, infra, third-party
6. **What went well** (5 min) — explicit list. Don't only collect failures; we want to repeat what worked.
7. **Action items** (15 min) — generate, prioritize, assign.

**Exit probe:** meeting notes capture all 7 sections.

## Phase 3 — Root Cause Statement

Write a single paragraph that:
- States the immediate trigger.
- Names the underlying systemic cause(s).
- Avoids attributing to individual decisions ("Alice did X" → "the deployment process allowed unreviewed prod changes").

Example:
> An expired TLS cert on the internal auth service was renewed manually 30 minutes after expiry. The immediate trigger was the absence of an active cert. The underlying cause was that cert lifecycle was tracked manually in a shared calendar with no alerting, no failover cert pre-provisioned, and the renewal runbook was three years out of date and untested. The on-call engineer recovered service through individual heroics that aren't repeatable.

## Phase 4 — Action Items

Each action item has:

```
AI-<id>: <imperative description>
  Type: Detective | Preventive | Responsive | Process | Documentation
  Owner: @<single person>
  Due: YYYY-MM-DD (max 90 days; if longer, split or escalate)
  Tracker: <Jira / Linear / GH issue link>
  Acceptance: <how we'll know it's done — tool-verifiable>
  Risk if not done: <one sentence>
```

Anti-patterns to reject:
- Owner: "the team" → no, single human.
- Due: "ASAP" / "Q3" → specific date.
- Acceptance: "improve X" → no, a probe (regex, query, test).
- Action items > 90 days from now → almost certainly never happen; split smaller.

Prioritize:
- **P0** — required for the same incident class to not repeat. Block on this.
- **P1** — significantly reduces likelihood or impact.
- **P2** — defense in depth; nice to have.

Cap P0 + P1 at ~10 items total; long lists don't ship.

**Exit probe:** every action item has all 6 fields above.

## Phase 5 — Publish

Postmortem doc goes to:
- Engineering org (internal blog / shared doc).
- Security leadership.
- Service owner team.
- Original incident channel (link pinned).

For SEV-1: exec summary to leadership; sanitized external comms only if customer-impacting.

**Exit probe:** publication link recorded.

## Phase 6 — Track to Completion

Action item tracking is the **IC's** responsibility for the first 30 days post-publication. Then transfer to security PM / service owner.

Weekly status: list each AI, owner, due date, status (not-started / in-progress / blocked / done). Re-publish stalled items. Escalate items > 14 days past due.

**Exit probe:** all P0 items closed before the 90-day mark; P1 items closed or formally re-scoped.

## Phase 7 — Log

Add to `memory/security/incident-log.md`:

```
| YYYY-MM-DD | <id> | <type> | SEV-X | <MTTD> | <MTTR> | <one-line root cause> | <link to postmortem> |
```

This is the cumulative organizational memory. Future incidents are triaged faster by checking this log first.

## Acceptance Criteria (workflow-level)

- Timeline reconstructed and reviewed.
- Five-whys (or fishbone) completed and recorded.
- Root cause statement written without naming individuals.
- Action items meet all 6 required fields; each P0/P1 has explicit acceptance probe.
- Postmortem published to defined audiences.
- Incident-log entry added.
- 30-day follow-up assigned.
