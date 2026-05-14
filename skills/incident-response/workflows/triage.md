---
title: Workflow — Triage (First 60 Minutes)
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
  - triage
artifact_type: skill-workflow
---

# Workflow: Triage (First 60 Minutes)

The first hour drives the outcome. Goal: classify severity, freeze evidence, assemble the right team, start the clock.

## Phase 1 — Acknowledge (T+0 to T+5 min)

1. **Acknowledge the alert** in the paging system. Stops re-pages, starts on-call attribution.
2. **Open the incident channel.** Naming convention: `incident-<YYYY-MM-DD>-<short-slug>`. Pin a thread for status updates.
3. **Declare IC.** Default: the responding on-call until handoff. State explicitly in channel: "I am Incident Commander."
4. **Designate scribe.** If alone, you're scribe too — note timestamp on every action.

**Exit probe:** channel exists; IC declared in channel; first scribe entry logged.

## Phase 2 — Initial Severity Call (T+5 to T+15 min)

Use the severity matrix in the parent `SKILL.md`. When in doubt, **classify high and downgrade later** — easier than the reverse.

Ask these five questions:

1. **Is data leaving the environment now?** (Exfil in progress = SEV-1.)
2. **Are users affected now?** (> 50% prod degraded = SEV-1 from availability angle.)
3. **Is regulated data involved?** (PII/PCI/PHI confirmed exposed = SEV-1; suspected = SEV-2 until ruled out.)
4. **Is the attacker still active?** (Live adversary = SEV-1 or SEV-2; dormant artifact = SEV-3.)
5. **Is this likely a false positive?** (FP signals: matches known maintenance window, matches recent change, alert noisy historically — go SEV-4 and investigate.)

Record the answers and the resulting SEV in the timeline.

**Exit probe:** SEV declared in channel with one-sentence rationale.

## Phase 3 — Notifications (T+15 to T+30 min)

Per the SEV matrix:

| SEV | Who to notify | Channel |
|---|---|---|
| SEV-1 | Exec sponsor, Legal, Comms, Security leadership | Direct page + email |
| SEV-2 | Security leadership, service owner team | Page on-call, Slack to team lead |
| SEV-3 | Service owner | Slack DM |
| SEV-4 | (none until findings) | — |

Template for the initial notification:

```
SEV-X incident declared at <timestamp UTC>
Summary: <one sentence>
Status: investigating
Possible impact: <one sentence; what's at stake>
What we don't know yet: <one sentence>
Next update: <time>
Channel: #incident-...
IC: @<name>
```

Avoid speculation. Say "investigating" not "we think it's...".

**Exit probe:** notification sent; "Next update" time recorded.

## Phase 4 — Evidence Preservation (T+15 to T+45 min, parallel with Phase 3)

Before changing system state, capture:

- [ ] **Memory snapshot** of suspect host(s) — most volatile, captures running malware / decrypted keys.
- [ ] **Network capture** at egress — 30+ minutes if feasible.
- [ ] **Log snapshot** with current timestamps: auth, app, DNS, proxy, EDR, cloud trail. Pull to forensic bucket immediately (logs can be tampered with or rolled over).
- [ ] **Disk image** of suspect hosts — secondary to memory but mandatory for SEV-1/2.
- [ ] **Cloud snapshot** of affected resources before any modification.
- [ ] **Identity events** for any suspect user/service principal: recent logins, sessions, permission grants.

Each artifact: record hash + collection time + collector + chain-of-custody location.

**Exit probe:** artifact inventory recorded with hashes.

## Phase 5 — Initial Scope Hypothesis (T+30 to T+60 min)

Working hypothesis answers:

1. **What's the entry point?** (Initial access vector — what we think it is, with confidence level.)
2. **What identities/credentials are implicated?** (Every account that could have been used.)
3. **What systems are touched?** (Every host the implicated identity has reached, plus pivot candidates.)
4. **What's the blast radius if hypothesis is correct?** (Worst plausible case, used to size response.)
5. **What confirms or refutes the hypothesis?** (The next investigation steps.)

Write it explicitly. A vague hypothesis produces vague response.

**Exit probe:** hypothesis section of incident template populated; confirmation queries identified.

## Phase 6 — Handoff (T+45 to T+60 min)

If response will exceed shift length:

1. Identify next IC and Tech Lead.
2. Walk them through: timeline, hypothesis, evidence collected, in-flight investigation queries, blockers.
3. Update channel with handoff explicit ("@new-ic is now IC at <timestamp>").
4. Outgoing IC steps back; doesn't shadow-command.

**Exit probe:** handoff explicitly noted in channel.

## Triage Output

By T+60 minutes you should have:

- SEV classified with rationale.
- Notifications sent per matrix.
- Evidence inventory with hashes.
- Working hypothesis written.
- Next investigation steps queued.
- IC and Tech Lead clearly identified.

Now route to `workflows/containment.md`.
