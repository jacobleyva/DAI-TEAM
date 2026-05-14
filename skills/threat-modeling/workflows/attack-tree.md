---
title: Workflow — Attack Tree
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
  - attack-tree
artifact_type: skill-workflow
---

# Workflow: Attack Tree

Goal-driven threat modeling. Start with an attacker's objective, decompose into the steps needed to achieve it, prune branches that don't apply. Useful when STRIDE produces too much noise and you want to focus on specific high-value adversary goals.

## When to Use

- A specific asset is unusually high-value (root signing key, customer financial records).
- Adversary capabilities are well-defined (you know it's a financially-motivated criminal, not a script kiddie).
- After STRIDE: the top 3 HIGH/CRITICAL findings each warrant an attack tree to validate mitigations cover all paths.

## Phase 1 — Define the Root Goal

Write one specific attacker objective. Bad: "Compromise the system." Good: "Exfiltrate customer PII from the user database." Better: "Exfiltrate >10K customer PII records without detection in <72 hours."

Specificity here gates branch pruning later.

**Exit probe:** root goal is concrete, measurable, and bounded in time/scale.

## Phase 2 — Decompose

Each node is a sub-goal or precondition. Children of a node combine with:

- **AND** — all children required to achieve parent (drawn with arc connecting child edges).
- **OR** — any child suffices (default; no arc).

Standard decomposition depth: 3–5 levels. Stop when leaves are concrete attacker actions (e.g. "phish a developer with `prod-deploy` role" rather than "obtain credentials").

Example skeleton (root: exfil PII):

```
ROOT: Exfiltrate >10K PII records in <72h
├── OR: Direct DB access
│   ├── AND
│   │   ├── Obtain DB credentials
│   │   │   ├── OR: Find in source control
│   │   │   ├── OR: Find in CI logs
│   │   │   ├── OR: Phish DBA
│   │   │   └── OR: Compromise build runner with secrets access
│   │   └── Reach DB network (VPC peering / VPN / bastion)
│   └── Run mass SELECT without alert
├── OR: API exfiltration
│   ├── AND
│   │   ├── Obtain API token with broad read scope
│   │   └── Pagination loop under rate-limit threshold
│   └── Hide in noise (off-hours, multiple IPs)
├── OR: Backup exfiltration
│   ├── Access backup storage (S3 / snapshot)
│   └── Decrypt if encrypted (CMK access)
└── OR: Insider exfiltration
    ├── Recruit / coerce insider
    └── Move data outside DLP coverage
```

**Exit probe:** every leaf is a concrete attacker action.

## Phase 3 — Annotate Leaves

For each leaf:
- **Cost** to attacker (Low / Med / High — money, time, skill).
- **Likelihood of success** given current controls (H/M/L).
- **Detection probability** (H/M/L — likelihood of getting caught given current monitoring).

Roll up to parent nodes: an OR node takes the **min** cost / **max** likelihood / **min** detection of its children; an AND node takes the **sum** cost / **product** likelihood / **max** detection.

**Exit probe:** all leaves annotated; root has propagated values.

## Phase 4 — Prune

Remove branches where:
- Cost ≥ value of asset to plausible attacker (no rational attacker takes this path).
- Detection probability ≈ 1 and consequences for being caught are severe (path is "noisy enough").

Keep what remains — these are realistic attack paths.

**Exit probe:** pruning rationale recorded for every removed branch.

## Phase 5 — Mitigate

Walk the surviving paths root-to-leaf. For each, identify the cheapest **chokepoint** node (the one node where a control breaks the most paths). Apply controls there.

Examples of high-value chokepoints:
- "Obtain DB credentials" — solved by short-lived IAM-issued credentials + no secrets in CI; breaks multiple paths.
- "Run mass SELECT without alert" — solved by DB query anomaly detection; breaks direct-access paths.

Record: existing control vs. proposed new control, owner, target date.

**Exit probe:** every surviving path has at least one node with a named control.

## Phase 6 — Write to Template

Insert the tree (ASCII / Mermaid) into the Attack Tree section of `templates/threat-model-template.md`. List the controls applied per chokepoint in the Mitigations section. Add an entry to the Residual Risk register for any path where no chokepoint control fully closes it.

## Acceptance Criteria (workflow-level)

- Root goal is specific, measurable, time-bounded.
- Tree decomposed to concrete leaf actions.
- Leaves annotated with cost / likelihood / detection.
- Pruning rationale logged.
- Each surviving path has a chokepoint control.
- Template populated.
