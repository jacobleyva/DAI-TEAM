---
name: incident-response
description: Use during or after a security or operational incident to drive structured triage, containment, eradication, recovery, and lessons learned. Produces a written incident record using templates/incident-response-template.md. Lessons feed back into memory/effectus/wisdom.md and memory/security/incident-log.md.
---

# Incident Response

The job during an incident is to stop the bleeding, then learn. The job after an incident is to make sure the same incident can't happen the same way twice. The written record is what makes the second job possible.

## When to Run

- Active incident — work the response in real time using this workflow as the spine
- Post-incident — within 5 business days of containment, run the full workflow to produce the written record
- Near-miss — when something almost happened, run a lightweight version to capture the lesson before memory fades
- Tabletop exercise — use this workflow to walk through a hypothetical to stress-test the team's response capability

## Workflow

The six phases run in order during a real incident. For postmortems, walk them in retrospect.

1. **Detect.** What's the trigger? Capture the initial signal: log line, alert, user report, observed behavior. Note the timestamp and the source. The detection phase often determines blast radius — earlier detection = smaller blast.
2. **Triage.** Severity, scope, blast radius. How many users / records / systems affected? Is the incident still active? Is data leaving? Severity tier (SEV1–SEV4) determines who gets paged and how aggressive containment can be.
3. **Contain.** Stop the bleeding without destroying evidence. Options include: rotating credentials, disabling accounts, blocking IPs at the perimeter, isolating affected hosts, taking services offline. Document every action with timestamp and operator. Avoid actions that destroy forensic data (memory, logs, file timestamps) unless containment requires it.
4. **Eradicate.** Remove the cause. This is where you actually fix the vulnerability or remove the malicious artifact. The fix should be tool-verified per `core/verification-doctrine.md` — don't claim eradication without a probe that shows the issue is closed.
5. **Recover.** Restore service. Validate that the recovery path is safe — re-introducing a compromised system can re-trigger the incident. Monitor closely during the first 24–72 hours post-recovery.
6. **Lessons.** What was the root cause? Why did detection take as long as it did? What controls failed or were missing? What controls worked? What changes prevent recurrence? The lessons section is the most important part of the written record — everything else is logistics.

## Severity tiers (default; adapt per organization)

- **SEV1 — Critical.** Active compromise of production data or services; significant customer impact; legal/regulatory notification likely required.
- **SEV2 — High.** Significant security or availability impact; contained but ongoing; no confirmed data exfiltration.
- **SEV3 — Medium.** Limited scope; contained; investigation continues.
- **SEV4 — Low.** Near-miss, automated alert that proved benign with manual confirmation, low-risk policy violation.

## Output shape

Use `templates/incident-response-template.md`. The structure:

- Incident ID, date, severity, status
- Detection details
- Timeline (timestamped action log)
- Scope and blast radius
- Containment actions
- Eradication actions with verification evidence
- Recovery actions and monitoring
- Root cause analysis
- Lessons learned (categorized)
- Action items (with owner and target date)
- Communications log (who was notified, when)
- External references (CVE, vendor advisories, similar incidents)

## Guardrails

- Run the workflow even for small incidents. The discipline transfers more than the specific lesson does.
- Timestamp everything. The timeline is the most-referenced part of the written record.
- Don't destroy evidence unless containment requires it. Decide explicitly; document the trade-off.
- Don't blame people in the written record. Blame the system that let the person make the mistake.
- An action item without an owner and a date is a wish. Don't ship the writeup with wishes.
- The lessons feed `memory/effectus/wisdom.md` and `memory/security/incident-log.md` automatically — that's part of the workflow, not optional.

## Anti-criteria — incident response must not

- Mark `eradicated` without a tool-verified probe showing the issue is closed
- Use phrases like "should be safe now" or "looks contained" — name the probe
- Ship a writeup without action items
- Ship a writeup that blames a person instead of a system
- Skip the lessons step because "everyone was tired" — the lesson is the entire ROI of the incident

## Codex Trigger-Phrase Routing

When the user's request matches any of the patterns below, follow the listed workflow.

| Trigger phrase / context | Workflow file |
|---|---|
| Active alert escalation, page, suspected breach | `workflows/triage.md` |
| Confirmed incident, deciding isolate vs. block vs. patch | `workflows/containment.md` |
| Incident closed, retro pending | `workflows/postmortem.md` |
| Full lifecycle (drill or real) | all three in sequence |

Read the entire matching workflow file before producing recommendations or actions — they encode time-sensitive checklists where order matters.

## Severity Matrix (concrete tier criteria)

| SEV | Criteria | Response time | Notification |
|---|---|---|---|
| **SEV-1** | Active data exfiltration; production outage > 50% users; ransomware in progress; regulated data confirmed exposed | Immediate (page on-call + IC) | Exec + Legal + Comms within 30 min |
| **SEV-2** | Confirmed compromise of non-prod or single user; suspected exfil under investigation; partial outage | < 30 min | Security leadership + service owner |
| **SEV-3** | Anomalous activity confirmed not benign; failed-but-contained attempt; vuln being exploited at low volume | < 4 hours | Security team + service owner |
| **SEV-4** | Suspicious activity under investigation; false-positive likely but worth checking | < 24 hours | Security team |

## Incident Roles

- **Incident Commander (IC)** — drives the response; not the technical fixer. Makes scope/escalation calls. Singular.
- **Scribe** — timeline keeper. Logs every action with timestamp.
- **Technical Lead(s)** — investigates and executes containment.
- **Communications Lead** — handles internal/external comms (only for SEV-1/2).
- **Legal / Compliance** — engaged for SEV-1; on-call for SEV-2 if regulated data is involved.

The on-call security engineer fills IC + Tech Lead until handoff (within 15 minutes for SEV-1).

## Doctrine

- **Evidence before action.** Capture artifacts (memory, network captures, log snapshots) before any containment that changes state.
- **Containment beats eradication.** Stop the bleeding first; eradicate only after scope is understood.
- **Document in real time.** Every action: timestamp + executor + verification.
- **Assume compromise extends.** If host A is compromised, ask: what credentials were on host A? Where else were they used?
- **Don't tip off the adversary.** Avoid noisy "fix it" actions on a still-monitored compromised system until eviction is ready.
- **Blameless postmortems.** Frame issues as process/system failures, never name individuals as the cause.

## Acceptance — Incident is Closed Only When

1. Root cause identified (not just symptoms) and recorded in the template.
2. Containment, eradication, and recovery steps documented in `templates/incident-response-template.md`.
3. All identified IOCs (file hashes, IPs, domains, accounts) listed and marked for addition to detection rules.
4. Action items recorded with owners + dates; each tracked to completion.
5. Postmortem published to relevant stakeholders.
6. Entry added to `memory/security/incident-log.md`.

## Tool-Verifiable Completion Probe

The user can confirm the workflow completed by checking that the output contains:
- A populated copy of `templates/incident-response-template.md`.
- A timeline section with at least one timestamped row.
- An IOC table (rows may be zero only with explicit "none identified" note).
- An action items table with at least one row, every row populated across all 6 required fields.
- A proposed append-line for `memory/security/incident-log.md`.

## Workflow Files

- `workflows/triage.md` — first 60 minutes: acknowledge, classify severity, notify, preserve evidence, hypothesize scope, hand off if shift exceeds (6 phases)
- `workflows/containment.md` — short-term vs. long-term containment decision flow; rebuild, rotate, patch, hunt; recovery monitoring (6 phases)
- `workflows/postmortem.md` — blameless retro, five-whys / fishbone, action items with all 6 required fields, incident-log append (7 phases)

## Related

- `templates/incident-response-template.md` — the output structure
- `core/verification-doctrine.md` — eradication and recovery require tool-verified evidence
- `core/ALGORITHM.md` — the six-phase loop applies (Observe = detect; Think = scope hypothesis; Plan = containment plan; Execute = act; Verify = probe; Learn = lessons)
- `core/SECURITY_DOMAIN_OVERVIEW.md` — domain-wide doctrine that applies to all security skills
- `skills/threat-modeling/SKILL.md` — incidents reveal threats the threat model missed; loop back and update
- `memory/effectus/wisdom.md` — one-line lessons crystallize here
- `memory/security/incident-log.md` — durable record of every incident with date, root cause, lesson
- `memory/security/threat-landscape.md` — incident patterns update the threat landscape
- `memory/security/auth-patterns.md` — incident lessons sometimes retire or amend auth patterns
