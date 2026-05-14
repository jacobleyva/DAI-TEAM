---
title: "Threat Model Template"
type: template
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
tags:
  - template
  - threat-model
  - security
artifact_type: template
---

# Threat Model — {{system-name}}

> Fill in each section. Delete sections that are explicitly N/A only after writing why.

## System & Scope

- **System name:** {{system-name}}
- **Version / revision:** {{version}}
- **Date modeled:** {{date}}
- **Contributors:** {{names}}
- **In scope:** {{what is being modeled — be specific}}
- **Out of scope:** {{what is explicitly NOT modeled and why}}

## Data Flow Diagram

```
{{Sketch entities (users, services, data stores), data flows (arrows with payload type),
and trust boundaries (dashed lines / labeled boundaries). Markdown ASCII or external link.}}
```

## Asset Inventory

| Asset | Description | Impact tier | Owner |
|-------|-------------|-------------|-------|
| {{asset-1}} | {{what it is, why it matters}} | Critical / High / Med / Low | {{owner}} |
| {{asset-2}} | | | |

## Threat Enumeration — STRIDE

Walk each asset against each STRIDE category. Skip combinations that have no realistic attack path against this system.

| ID | Asset | STRIDE | Threat description | Likelihood (1-5) | Impact (1-5) | Score |
|----|-------|--------|--------------------|------------------|--------------|-------|
| T-01 | {{asset}} | S | {{threat}} | | | |
| T-02 | | T | | | | |
| T-03 | | R | | | | |
| T-04 | | I | | | | |
| T-05 | | D | | | | |
| T-06 | | E | | | | |

**Primary concerns** (score ≥ 15): {{list IDs}}
**Secondary concerns** (score 9–14): {{list IDs}}
**Acknowledged-and-accepted** (score < 9): {{list IDs}}

## Attack Trees — Primary Concerns

For each primary-concern threat, build an attack tree. Root node is the attacker's goal; children are sub-goals; leaves are concrete actions.

### Attack Tree for T-NN — {{threat title}}

```
GOAL: {{attacker's goal}}
├── Sub-goal A: {{...}}
│   ├── Action: {{...}}
│   └── Action: {{...}}
└── Sub-goal B: {{...}}
    ├── Action: {{...}}
    └── Action: {{...}}
```

(Add additional trees per primary-concern threat.)

## Kill-Chain Walkthrough — Top 2–3 Attack Chains

For the top attack chains, walk each stage. Mark which stages your defenses currently cover.

### Chain 1 — {{name}}

| Stage | Attacker action | Defenses currently in place | Gap |
|-------|------------------|----------------------------|-----|
| Reconnaissance | | | |
| Weaponization | | | |
| Delivery | | | |
| Exploitation | | | |
| Installation | | | |
| Command & Control | | | |
| Actions on Objectives | | | |

(Add additional chains for chain 2, chain 3.)

## Mitigations Matrix

| Threat ID | Control name | Owner | Status (planned / in-progress / done / verified) | Verification probe |
|-----------|--------------|-------|--------------------------------------------------|-------------------|
| T-01 | {{control}} | {{owner}} | | {{how this control would be verified working}} |
| T-02 | | | | |

## Residual Risks

Risks that mitigations don't fully close. Document the reasoning for acceptance.

- **R-01:** {{risk}} — accepted because {{reasoning}}; revisit when {{trigger}}.
- **R-02:** …

## Related Artifacts

- Related WORK note: {{path}}
- Linked design doc: {{path or URL}}
- Linked code: {{path:lines}}
- Source incidents that informed this model: {{IDs from memory/security/incident-log.md}}
- Mapped frameworks: {{CIS Controls / OWASP / NIST entries that apply}}

## Review Cadence

- **Next review date:** {{date}}
- **Review triggers:** {{what changes invalidate this model and force a re-do}}
