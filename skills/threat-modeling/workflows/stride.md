---
title: Workflow — STRIDE
type: workflow
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
tags:
  - security
  - threat-modeling
  - workflow
  - stride
artifact_type: skill-workflow
---

# Workflow: STRIDE

Per-component / per-data-flow threat enumeration using Microsoft's STRIDE taxonomy.

## STRIDE Categories

| Letter | Threat | Property violated | Typical examples |
|---|---|---|---|
| **S** | Spoofing | Authentication | Stolen credentials, forged tokens, JWT alg=none, DNS hijack |
| **T** | Tampering | Integrity | Unauthorized DB write, MITM modification, malicious binary swap |
| **R** | Repudiation | Non-repudiation | User denies action; no audit trail tying them to it |
| **I** | Information Disclosure | Confidentiality | Verbose errors, S3 public bucket, log leakage, side-channel |
| **D** | Denial of Service | Availability | Resource exhaustion, algorithmic complexity attack, dependency outage |
| **E** | Elevation of Privilege | Authorization | IDOR, missing role check, sandbox escape, privileged container escape |

## Phase 1 — Build the Data-Flow Diagram

Identify and label:

- **External entities** (users, third-party services) — drawn as squares.
- **Processes** (your services, functions) — drawn as circles.
- **Data stores** (DBs, queues, caches, file storage) — drawn as parallel lines.
- **Data flows** (arrows between the above) — labeled with what travels (e.g. "session cookie", "PII profile fetch").
- **Trust boundaries** — dashed lines crossing flows where authority changes (Internet→DMZ, DMZ→app, app→DB).

Use the Mermaid diagram block in `templates/threat-model-template.md`. If the system is too large to fit on one diagram, decompose into per-feature DFDs.

**Exit probe:** DFD reviewed by at least one engineer who built the system; trust boundaries explicitly drawn.

## Phase 2 — Enumerate per Element

For **every** element (entity, process, store, flow), walk the STRIDE table:

| Element | Applicable STRIDE letters |
|---|---|
| External entity | S, R |
| Process | S, T, R, I, D, E |
| Data store | T, R, I, D |
| Data flow | T, I, D |

For each (element × applicable letter), ask: *"How could an attacker achieve this against this element?"* Record one threat row per realistic answer.

Don't force a threat per cell. If no realistic threat exists, write "N/A — no plausible vector" and move on.

**Exit probe:** every element has been walked through every applicable STRIDE letter; rationale logged for empty cells.

## Phase 3 — Score Each Threat

Likelihood (H/M/L):
- **H** — attacker capability widely available; pre-conditions trivially satisfied; observed in the wild against similar systems.
- **M** — requires specific skill or insider position; pre-conditions need effort.
- **L** — theoretical or requires resources only a nation-state would expend on this asset.

Impact (H/M/L):
- **H** — confidentiality/integrity loss of regulated data; full service outage > 1h; revenue impact > $X (set the bar with the business).
- **M** — limited data exposure, partial outage, recoverable damage.
- **L** — minor inconvenience, easily reverted.

Risk = matrix:

| L\I | L | M | H |
|---|---|---|---|
| **H** | MED | HIGH | CRITICAL |
| **M** | LOW | MED | HIGH |
| **L** | LOW | LOW | MED |

**Exit probe:** every threat has Likelihood, Impact, Risk filled.

## Phase 4 — Mitigations

For each CRITICAL/HIGH threat:
1. List existing controls that reduce L or I.
2. If residual risk is still HIGH+, propose a new control (specific, owned, dated).
3. If mitigation is "accept risk", record the approver and rationale.

For MED, propose mitigations but don't block on them. For LOW, document only.

Anti-patterns to avoid:
- "Add input validation" — too vague. Specify what input, what validation, where enforced.
- "Use HTTPS" — not a mitigation for a tampering threat that lives behind the TLS terminator.
- "Add logging" — only mitigates R (repudiation), not the underlying attack.

**Exit probe:** every CRITICAL/HIGH has a named mitigation + owner; MEDs have proposals.

## Phase 5 — Write to Template

Populate `templates/threat-model-template.md`:
- System Description ← from inputs
- DFD ← from Phase 1
- Trust Boundaries ← from Phase 1
- STRIDE Table ← Phases 2–4
- Mitigations summary ← Phase 4
- Residual Risk register ← any HIGH+ residuals
- Review Cadence ← set next review date and trigger conditions (e.g. "before adding payment provider")

## Acceptance Criteria (workflow-level)

- DFD present with trust boundaries.
- STRIDE table covers every applicable (element × letter) cell.
- All threats scored.
- All CRITICAL/HIGH mitigated or formally risk-accepted with named approver.
- Template populated; review date set.
