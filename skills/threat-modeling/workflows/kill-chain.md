---
title: Workflow — Kill Chain (Lockheed + MITRE ATT&CK)
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
  - kill-chain
  - mitre-attack
artifact_type: skill-workflow
---

# Workflow: Kill Chain (Cyber Kill Chain + MITRE ATT&CK)

Adversary-lifecycle threat modeling. Walk the attacker's stages from outside the perimeter to objective; identify defender control opportunities at each stage. Use to validate that detection and response cover the full attack lifecycle, not just initial access.

## When to Use

- Validating SOC / detection-engineering coverage against a system.
- Red-team exercise scoping (defender side).
- After STRIDE + attack-tree, to confirm response controls (not just preventive) are in place.
- Specific concern: "do we have eyes anywhere along the chain for adversary X?"

## The Two Frameworks

**Lockheed Martin Cyber Kill Chain** (7 stages — strategic, vendor-agnostic):

1. **Reconnaissance** — adversary research on target.
2. **Weaponization** — coupling exploit with payload.
3. **Delivery** — transmission to target (phish, USB, watering hole).
4. **Exploitation** — code execution triggered.
5. **Installation** — persistence established.
6. **Command & Control (C2)** — adversary channel to compromised asset.
7. **Actions on Objectives** — data exfil, encryption, sabotage, pivot.

**MITRE ATT&CK** (14 tactics — operational, with specific techniques):

1. Reconnaissance · 2. Resource Development · 3. Initial Access · 4. Execution · 5. Persistence · 6. Privilege Escalation · 7. Defense Evasion · 8. Credential Access · 9. Discovery · 10. Lateral Movement · 11. Collection · 12. C2 · 13. Exfiltration · 14. Impact

Use Kill Chain for the narrative/executive view; ATT&CK for technique-level mapping.

## Phase 1 — Define the Adversary

Profile the relevant threat actor:

- **Motivation** — financial (ransomware/extortion), espionage (state), hacktivism, opportunistic.
- **Capability** — script kiddie / commodity malware / red team / APT.
- **Targeting** — opportunistic (you happened to be on a list) vs. targeted (someone wants *your* data).
- **Prior TTPs** — if known (e.g. "FIN7-style", "APT29-style").

This profile constrains which kill-chain stages need depth. A commodity ransomware actor doesn't do months of recon; an APT does.

**Exit probe:** adversary profile written in one paragraph.

## Phase 2 — Walk the Chain

For each Lockheed stage, ask:

1. **How would the adversary execute this stage against us specifically?** (Map to ATT&CK techniques.)
2. **What's our preventive control?** (Stops the action.)
3. **What's our detective control?** (Tells us it happened.)
4. **What's our responsive control?** (Action we take when detected.)

Use the table below. Fill one row per stage minimum; more if multiple distinct paths.

| Stage | ATT&CK techniques | Preventive | Detective | Responsive |
|---|---|---|---|---|
| Reconnaissance | T1595 Active Scanning, T1589 Gather Victim Identity Info | Cloud WAF + rate limit; reduce LinkedIn org footprint | NDR/IDS alerts on scan patterns; brand monitoring | Blocklist source; alert affected employees |
| Weaponization | T1587 Develop Capabilities | — (out of our reach) | Threat intel feeds | N/A |
| Delivery | T1566 Phishing, T1190 Exploit Public-Facing App | Email security gateway; patch SLA; WAF | DMARC reports; WAF logs; web error spikes | Quarantine inbox; block sender; emergency patch |
| Exploitation | T1203 Exploitation for Client Execution, T1059 Command and Scripting Interpreter | Up-to-date browsers/Office; EDR exploit prevention; ASLR/DEP | EDR alerts; suspicious child-process trees | Isolate host (EDR network containment) |
| Installation | T1547 Boot/Logon Autostart, T1543 Create or Modify System Process | Application allow-listing; least-privilege users | EDR persistence detections; file-integrity monitoring on startup folders | Kill process; remediate persistence; reimage |
| C2 | T1071 Application Layer Protocol, T1573 Encrypted Channel | Egress filtering; DNS firewall; proxy-only egress | DNS analytics; beacon detection; TLS JA3 fingerprinting | Block C2 domain/IP at egress; quarantine host |
| Actions on Objectives | T1486 Data Encrypted for Impact, T1041 Exfil Over C2, T1567 Exfil to Web Service | DLP; backup immutability; egress allow-list | DLP alerts; anomalous data volume; backup-deletion alerts | Activate IR plan; restore from backup; notify regulators if applicable |

**Exit probe:** every row has at least one Detective control filled (or explicit "none" + risk acceptance).

## Phase 3 — Identify Gaps

For each stage:
- If **Preventive is N/A**, you depend entirely on Detective + Responsive — verify those are strong.
- If **Detective is missing**, the chain breaks; adversary moves freely past this point.
- If **Responsive is missing**, you'll detect and watch the breach unfold without action.

Each gap becomes a finding for the threat model: "Stage X has no detection capability — adversary [profile] can proceed undetected to stage Y."

**Exit probe:** gap list produced; each gap has an owner and remediation proposal.

## Phase 4 — Validate with Purple-Team Test (if scoped)

For top-priority detective controls, run a controlled test:
1. Execute a representative ATT&CK technique (with authorization, in a documented window).
2. Confirm detection fires within expected MTTD.
3. Confirm responsive control executes correctly.
4. Document the test in the incident-log scaffold (date, technique, result).

**Exit probe:** at least one detective control validated end-to-end.

## Phase 5 — Write to Template

Insert the Kill Chain section into `templates/threat-model-template.md` after the STRIDE/attack-tree sections. Gaps go into the Residual Risk register with explicit "no detection coverage" labels.

## Acceptance Criteria (workflow-level)

- Adversary profile documented.
- All 7 Lockheed stages walked; each row filled.
- ATT&CK techniques mapped per stage (at least one per stage).
- Gaps enumerated with owners.
- At least one detective control validated (or test scheduled).
- Template populated.
