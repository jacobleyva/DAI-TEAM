---
name: threat-modeling
description: Use when designing a new system, feature, or integration that handles sensitive data, crosses trust boundaries, or exposes an attack surface. Produces a structured threat model with STRIDE enumeration, attack trees for high-impact threats, and proposed mitigations. Output goes to templates/threat-model-template.md format.
---

# Threat Modeling

A threat model is not a checkbox. It is a working artifact that names what you're protecting, what could realistically go wrong, and what you'll do about it. The output is a written model, not a meeting.

## When to Run

- Before building a new service or feature that handles sensitive data
- Before integrating a new third-party service
- When a system crosses a new trust boundary (e.g., adding internet exposure to an internal tool)
- After a significant architecture change to an existing system
- Periodically (annually at minimum) for any system whose threat surface has shifted

## Workflow

1. **Name the system and scope.** What is being modeled? What is explicitly out of scope? Without scope discipline, the model becomes infinite and useless.
2. **Diagram the data flow.** Identify entities (users, services, data stores), data flows between them, and trust boundaries. A whiteboard sketch or a simple block diagram in markdown works — the goal is shared understanding, not aesthetics.
3. **Enumerate assets.** What is worth protecting? Customer PII, credentials, write access to systems of record, financial transaction data, intellectual property, system availability. Assign each asset an impact tier (Critical / High / Medium / Low).
4. **Enumerate threats per asset using STRIDE.** For every asset, work through:
   - **S — Spoofing** identity (impersonation)
   - **T — Tampering** with data or code
   - **R — Repudiation** (denying an action)
   - **I — Information disclosure** (leakage)
   - **D — Denial of service** (availability)
   - **E — Elevation of privilege** (gaining unauthorized access)
5. **Rank threats by likelihood × impact.** Use a 1–5 scale for each axis. Anything ≥ 15 is a primary concern; 9–14 secondary; below 9 acknowledge and move on.
6. **For each primary-concern threat, build an attack tree.** Root node is the attacker's goal; child nodes are sub-goals; leaves are concrete actions. Tree depth typically 3–5 levels.
7. **For the top 2–3 attack chains, do a kill-chain analysis.** Walk through reconnaissance → weaponization → delivery → exploitation → installation → command & control → actions on objectives. Note which stages your defenses already cover.
8. **Propose mitigations.** For each primary-concern threat, name the specific control (or combination of controls) that closes the gap. Map to CIS / NIST / OWASP where applicable.
9. **Identify residual risks.** Threats that mitigations don't fully close, and why accepting them is reasonable. Future-you wants to know which risks were known and accepted vs. missed.
10. **Write the model** using `templates/threat-model-template.md`. The written artifact is the deliverable.

## Output shape

Use `templates/threat-model-template.md`. The structure:

- System name + scope (in/out)
- Data flow diagram (markdown sketch or external link)
- Asset inventory with impact tiers
- STRIDE threat enumeration table
- Top-N attack trees
- Top 2–3 kill-chain walkthroughs
- Mitigations matrix (threat → control → owner → status)
- Residual risks (accepted, with rationale)
- Date, model version, contributors

## Guardrails

- A threat model with no scope is useless. State what is *not* being modeled.
- Don't enumerate threats that have no realistic attack path against this system's assets. The point is leverage, not completeness.
- Don't list every CIS control. List the ones that close *named threats* in this model.
- Don't conflate "we have a control" with "the control works." Mitigations should reference where the control is implemented and how it would be verified.
- Update the model when the system changes. A stale threat model is worse than no threat model because it creates false confidence.

## Anti-criteria — threat model must not

- Be a meeting that didn't produce a written artifact
- Skip the asset inventory (no assets = no threats = no leverage)
- Use STRIDE as a literal checklist for every entity (it's a prompt, not a template)
- Recommend "do more security" without naming the specific control and where it lives
- Claim a threat is mitigated without naming the control that mitigates it

## Codex Trigger-Phrase Routing

When the user's request matches any of the patterns below, follow the listed workflow.

| Trigger phrase / context | Workflow file |
|---|---|
| "new feature design review" / "architecture review" | `workflows/stride.md` |
| "what could go wrong if an attacker tries X" | `workflows/attack-tree.md` |
| "map this to MITRE / red-team perspective" | `workflows/kill-chain.md` |
| "full threat model from scratch" | all three: STRIDE first for breadth, attack-tree on top-3 STRIDE findings, kill-chain to validate detection/response coverage |

Read the entire matching workflow file before producing the threat model — they encode the procedure that defines completeness.

## Inputs to Confirm Before Starting

- **System under analysis** — architecture diagram, data-flow diagram, or written description.
- **Assets** — what's worth protecting (data, money, reputation, availability).
- **Trust boundaries** — where authority/trust level changes (Internet→edge, edge→app, app→DB, app→3rd-party API).
- **Existing controls** — what's already in place (authN/Z, network seg, monitoring).

## Codex Threat-Row Schema (the precise output shape)

Each identified threat populates a row with all 9 fields:

```
Threat-ID:   TM-<system>-<NNN>
Category:    S/T/R/I/D/E (or attack-tree node ID, or kill-chain phase)
Vector:      how the attack happens
Asset:       what's at risk
Likelihood:  H/M/L (with one-sentence reasoning)
Impact:      H/M/L (with one-sentence reasoning)
Risk:        Likelihood × Impact (CRITICAL/HIGH/MED/LOW)
Mitigation:  existing or proposed control
Residual:    risk remaining after mitigation
Owner:       person/team responsible for the mitigation
```

## Acceptance — Threat Model is Complete Only When

1. Data-flow diagram exists in the output and trust boundaries are explicitly marked.
2. At least one workflow (STRIDE, attack-tree, or kill-chain) has been completed end-to-end.
3. Every threat row has all 9 fields above.
4. CRITICAL and HIGH threats each have a named mitigation + owner.
5. Review date and next-review trigger are recorded in the template.

## Tool-Verifiable Completion Probe

The user can confirm the workflow completed by checking that the output:
- Is a populated copy of `templates/threat-model-template.md` (all sections filled or marked N/A with rationale).
- Contains at least one Mermaid `flowchart` block for the DFD.
- Has zero `<placeholder>` strings remaining.

## Workflow Files

- `workflows/stride.md` — per-component / per-data-flow threat enumeration (5 phases, STRIDE-table scoring rubric)
- `workflows/attack-tree.md` — goal-driven decomposition with leaf annotation + pruning + chokepoint controls (6 phases)
- `workflows/kill-chain.md` — adversary-lifecycle walk (Lockheed 7 stages + MITRE ATT&CK technique mapping) (5 phases)

## Related

- `templates/threat-model-template.md` — the output structure
- `skills/security-review/SKILL.md` — uses the threat model to weight findings
- `skills/incident-response/SKILL.md` — incident postmortems feed back into the threat model
- `core/SECURITY_DOMAIN_OVERVIEW.md` — domain-wide doctrine that applies to all security skills
- `memory/security/threat-landscape.md` — current threat intel that informs likelihood judgments
- `memory/security/auth-patterns.md` — defensive patterns relevant to mitigation choices
- `knowledge/collections/owasp-top-10.md` — application-layer threat catalog
- `knowledge/collections/owasp-api-top-10.md` — API-specific risks
- `knowledge/collections/cwe-top-25.md` — weakness IDs for threat-mapping
- `knowledge/collections/cis-controls-v8.1.md` — control catalog for the mitigations matrix
