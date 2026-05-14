---
title: Workflow — Containment
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
  - containment
  - eradication
artifact_type: skill-workflow
---

# Workflow: Containment

Stop the bleeding. Decide between **short-term containment** (isolate fast, keep options open) and **long-term containment** (eradicate, rebuild, prevent recurrence). Order matters: short-term first, long-term after scope is understood.

## Decision Flow

```
                    Is the attacker active NOW?
                              │
                  ┌───────────┴───────────┐
                 YES                       NO
                  │                        │
        Short-term containment      Is exfil ongoing?
        (isolate immediately)               │
                  │                ┌────────┴────────┐
                  │               YES                NO
                  ▼                │                  │
       Investigate scope           ▼                  ▼
       under containment    Short-term      Investigate first,
                  │         containment     then contain
                  │                │                  │
                  └────────┬───────┴──────────────────┘
                           ▼
              Have we confirmed full scope?
                           │
                    ┌──────┴──────┐
                   YES            NO
                    │             │
                    ▼             ▼
              Long-term      Continue investigation;
              containment    expand short-term if pivot detected
              + eradication
```

## Phase 1 — Short-Term Containment

Goal: cut adversary access and stop ongoing harm **within minutes**. Reversible if possible. Preserves forensics.

### Network isolation
- EDR network containment on suspect host (severs all network except EDR mgmt channel).
- Move suspect VM to isolated security group / network ACL.
- Block C2 domains/IPs at egress firewall, DNS firewall, proxy.
- Suspend suspect service principal / API token (don't delete — preserve for forensics).

### Identity actions
- Force password reset + session revocation for implicated user account(s).
- Revoke active OAuth tokens / refresh tokens.
- Disable MFA enrollments under attacker control; re-enroll under help-desk verification.
- Disable suspect service accounts; rotate any credentials they could have read.

### Data actions
- Pause replication / backup deletion if ransomware-pattern (prevents poisoned backups overwriting clean ones).
- Set affected storage to read-only / WORM if supported.
- Block suspect outbound to exfiltration destinations.

### Validation
After each action, confirm it took effect — adversaries on the wire can race your containment.

**Exit probe:** for each action: timestamp + executor + verification result recorded.

## Phase 2 — Scope Confirmation

Before long-term containment / eradication, confirm:

- [ ] Every host the attacker touched is identified (pivot map).
- [ ] Every credential the attacker accessed or could have accessed is enumerated (treat all as compromised).
- [ ] Every persistence mechanism is found (autoruns, scheduled tasks, services, cron, systemd units, container restart policies, K8s CronJobs, Lambda triggers, browser extensions).
- [ ] Initial access vector is understood with high confidence.
- [ ] Timeline reconstructed back to first compromise (often weeks earlier than detection).

Tools / sources for confirmation:
- EDR timeline view + process trees.
- DNS query history (often the cleanest lateral-movement signal).
- Authentication logs across IdP, hosts, cloud control plane.
- File system timeline (MAC times of files in attacker's working dirs).
- Cloud trail / audit log for API actions taken with implicated credentials.

**Exit probe:** scope confirmation checklist all-green or explicit "accept unknown" with risk acceptance.

## Phase 3 — Communication Protocol

During investigation and containment:

**Internal updates:** every 60 minutes for SEV-1, every 4 hours for SEV-2, daily for SEV-3.

Template:
```
Update <timestamp UTC> — SEV-X incident #<id>
Status: <containing | investigating | recovering | resolved>
What changed since last update: <bullets>
Current scope: <hosts / accounts / data>
Next milestone: <containment complete | eradication complete | recovery complete>
Blockers: <if any>
Next update: <time>
```

**External communications (SEV-1 only)** — controlled by Comms Lead, reviewed by Legal:
- Customer notification triggered if regulated data confirmed exposed (timelines vary by jurisdiction: GDPR 72h, HIPAA 60d, US state laws vary, PCI 24h to acquirer).
- Regulator notification per applicable rule.
- Public statement only if exfiltration is public-facing or service-impacting visibly.

Do not speculate externally. "We are investigating an incident" beats "we believe X happened" until X is confirmed.

**Exit probe:** comms cadence honored; external comms sign-off logged.

## Phase 4 — Long-Term Containment / Eradication

Now that scope is confirmed, evict and rebuild:

- [ ] **Rebuild** every compromised host from known-good image rather than cleaning in place. Cleaning misses persistence.
- [ ] **Rotate** all credentials in the implicated scope: service account passwords, API tokens, signing keys, OAuth secrets, KMS keys (re-encrypt data), database passwords, SSH host keys, TLS private keys where compromise can't be ruled out.
- [ ] **Patch** the exploited vulnerability everywhere it exists (not just the entry point — adversary may have queued a re-entry).
- [ ] **Remove** persistence mechanisms found in Phase 2.
- [ ] **Block** all IOCs at every detection layer (firewall, EDR, email, DNS, SIEM).
- [ ] **Hunt** for the same TTPs across the rest of the environment (assume they tried elsewhere).
- [ ] **Verify** monitoring is back to baseline before declaring containment.

**Exit probe:** rebuild + rotation + patch + hunt completed; verification queries run with no positive hits.

## Phase 5 — Recovery

- [ ] Restore service from known-good backups where data was destroyed/encrypted. Verify backup integrity before restore.
- [ ] Re-enable affected user accounts after help-desk-verified password reset + MFA re-enrollment.
- [ ] Phased traffic return — internal users first, then customers, with monitoring at each step.
- [ ] Monitor for reinfection / re-entry for at least 30 days.

**Exit probe:** service restored to SLO; no anomalous activity for the watch period.

## Phase 6 — Closure

Incident transitions to closed when:
1. Containment + eradication + recovery completed.
2. Postmortem scheduled (within 7 days of recovery).
3. All IOCs detection-engineered into permanent rules.
4. Action items captured in `templates/incident-response-template.md` and assigned.

Route to `workflows/postmortem.md`.
