---
title: "Incident Response Template"
type: template
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
tags:
  - template
  - incident-response
  - security
  - postmortem
artifact_type: template
---

# Incident — {{incident-id}}: {{short-title}}

## Header

- **Incident ID:** {{INC-YYYY-MM-DD-NN}}
- **Severity:** SEV1 / SEV2 / SEV3 / SEV4
- **Status:** detecting / containing / eradicating / recovering / closed
- **Detected:** {{timestamp ISO-8601}}
- **Contained:** {{timestamp}}
- **Resolved:** {{timestamp}}
- **Incident commander:** {{name}}
- **Scribe:** {{name}}
- **Contributors:** {{names}}

## Detection

- **Detected by:** {{system / alert / user / external party}}
- **Initial signal:** {{exact log line, alert text, user report, or observed behavior}}
- **Time-to-detect:** {{from incident start to first detection}}

## Timeline

All timestamps in ISO-8601 / team timezone. Append each action as it happens.

| Timestamp | Actor | Action | Result |
|-----------|-------|--------|--------|
| {{ts}} | {{who}} | {{what they did}} | {{outcome}} |
| | | | |

## Scope and Blast Radius

- **Affected systems:** {{list}}
- **Affected users / records:** {{count + classification — PII, financial, etc.}}
- **Data exfiltration confirmed?** yes / no / under investigation
- **External notification required?** legal / regulator / customer / vendor — yes/no per category

## Containment Actions

For each action: what, when, by whom, side effects.

- **C-01:** {{action}} at {{timestamp}} by {{operator}} — side effect: {{e.g., "logs older than 4h rotated"}}
- **C-02:** …

## Eradication Actions

For each action: what was removed/fixed, and the **verification probe** that confirmed eradication.

- **E-01:** {{action}}
  - Verification: {{tool-verified probe per `core/verification-doctrine.md` — quote the command output}}
- **E-02:** …

## Recovery Actions

- **R-01:** {{service or component restored, validation that restoration is safe}}
- **R-02:** {{monitoring elevated for N hours/days}}
- **Recovery validated by:** {{name + timestamp + probe}}

## Root Cause Analysis

- **Proximate cause:** {{the immediate trigger}}
- **Underlying cause:** {{the system condition that made the trigger lethal}}
- **Contributing factors:** {{list — environmental, process, training, design}}
- **Why the controls didn't catch it earlier:** {{honest answer}}

## Lessons Learned

Categorize each lesson and route it to its home in the workspace.

- **Technical lesson:** {{lesson}} → updates {{file or skill}}
- **Process lesson:** {{lesson}} → updates {{runbook or skill}}
- **Detection lesson:** {{lesson}} → updates {{alerting / monitoring config}}
- **One-line takeaway** (goes to `memory/effectus/wisdom.md`): {{single sentence with past-tense origin}}

## Action Items

Every action item has an owner and a target date. Items without both are wishes.

| ID | Action | Owner | Target date | Status |
|----|--------|-------|------------|--------|
| AI-01 | {{action}} | {{name}} | {{YYYY-MM-DD}} | open |
| AI-02 | | | | |

## Communications Log

- **Internal:** {{who was notified, when, what channel}}
- **External:** {{customer notifications, regulator notifications, vendor disclosures}}
- **Status updates:** {{cadence and channel during the active incident}}

## External References

- **CVE / advisory:** {{if applicable}}
- **Vendor disclosure / patch:** {{links}}
- **Similar past incidents:** {{IDs from `memory/security/incident-log.md`}}
- **Threat model entries this incident invalidated or confirmed:** {{paths to threat models}}

## Routing After Closure

After the incident is closed:

- Append a one-line entry to `memory/security/incident-log.md` with date, severity, root cause, lesson
- Append the one-line takeaway to `memory/effectus/wisdom.md`
- Update relevant `skills/*/SKILL.md` Gotchas section if the lesson applies to a recurring task
- Update `memory/security/threat-landscape.md` if this incident reflects a new or escalating threat pattern
- Update `memory/security/auth-patterns.md` if the lesson changes recommended auth patterns
- Update relevant `core/*.md` if the lesson reveals a doctrine gap
- Link the incident from any threat model that should have caught it (and update the model if needed)
