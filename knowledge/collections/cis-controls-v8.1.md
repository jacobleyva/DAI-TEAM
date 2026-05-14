---
title: CIS Critical Security Controls v8.1
type: knowledge
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
tags:
  - security
  - cis
  - controls
  - knowledge
artifact_type: knowledge-collection
---

# CIS Critical Security Controls v8.1

Source: https://www.cisecurity.org/controls/v8-1
Retrieved: 2026-05-12
License: CIS Controls are released by the Center for Internet Security under Creative Commons (CC BY-NC-ND 4.0).

## What This Is

CIS Controls v8.1 is a prioritized set of 18 cybersecurity controls (153 safeguards) designed to defend against the most pervasive cyber-attacks. Released by the Center for Internet Security; updated 2024.

## Implementation Groups

- **IG1** — basic cyber hygiene; small enterprises with limited resources. ~56 safeguards.
- **IG2** — IG1 + safeguards for orgs with sensitive data / regulated requirements. ~74 additional safeguards.
- **IG3** — IG2 + all 153 safeguards; enterprises with mature security programs and high-value targets.

## The 18 Controls

| # | Control | IG1 / IG2 / IG3 | One-line summary |
|---|---|---|---|
| 1 | Inventory and Control of Enterprise Assets | All IGs | Know every device that processes/stores your data; act on unauthorized ones. |
| 2 | Inventory and Control of Software Assets | All IGs | Know every piece of software; act on unauthorized installations. |
| 3 | Data Protection | All IGs | Classify, encrypt, retain, and dispose of data per its sensitivity. |
| 4 | Secure Configuration of Enterprise Assets and Software | All IGs | Establish and maintain secure configs for hardware, OS, apps, and network gear. |
| 5 | Account Management | All IGs | Manage identity lifecycle: creation, use, dormancy, deletion. |
| 6 | Access Control Management | All IGs | Authorize, monitor, and revoke access — least privilege everywhere. |
| 7 | Continuous Vulnerability Management | All IGs | Find, prioritize, and remediate vulns continuously, not annually. |
| 8 | Audit Log Management | All IGs | Collect, alert, review, and retain audit logs. |
| 9 | Email and Web Browser Protections | All IGs | Reduce attack surface from the two most-exploited apps. |
| 10 | Malware Defenses | All IGs | Prevent and detect malicious code on endpoints. |
| 11 | Data Recovery | All IGs | Tested, immutable, isolated backups of in-scope data. |
| 12 | Network Infrastructure Management | IG2 + | Secure, segment, and monitor network devices. |
| 13 | Network Monitoring and Defense | IG2 + | Detect threats traversing the network; alert and respond. |
| 14 | Security Awareness and Skills Training | All IGs | Train the workforce; specialized training for IT and security staff. |
| 15 | Service Provider Management | IG2 + | Inventory, classify, and assess third parties holding your data. |
| 16 | Application Software Security | IG2 + | Manage security throughout the software development lifecycle. |
| 17 | Incident Response Management | All IGs | Establish a program: roles, plan, communication, lessons learned. |
| 18 | Penetration Testing | IG2 + | Regularly test defenses by simulating attacker behavior. |

## Notable v8 → v8.1 Changes (May 2024 release)

- Governance enhancements: added explicit safeguards for documented enterprise security governance.
- AI-related guidance alignments published as companion document.
- Refined mapping to NIST CSF 2.0.

## Mapping References (Public Crosswalks)

- NIST CSF 2.0
- NIST SP 800-53 Rev. 5
- ISO/IEC 27001:2022
- PCI DSS v4
- HIPAA Security Rule
- MITRE ATT&CK (defense priorities)

Crosswalks published by CIS at https://www.cisecurity.org/controls/cis-controls-navigator

## How To Use This in Reviews

When auditing a system:
1. For each in-scope control, identify the responsible safeguard ID (e.g. 6.5 = "Require MFA for administrative access").
2. Verify implementation with tool-verifiable evidence (config snapshot, query result, scan output).
3. Findings reference the specific safeguard ID + IG level, not just the control number.

## Notes for Ingestion

This is a summary cheat-sheet, not a substitute for the source document. For a full assessment, retrieve the official CIS Controls v8.1 PDF and CIS-CAT Pro tool from cisecurity.org. The full document includes per-safeguard implementation guidance and asset-type tables (Devices, Software, Network, Users, Data) that this summary omits.
