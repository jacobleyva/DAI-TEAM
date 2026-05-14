---
title: Threat Landscape
type: security-memory
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
version: v1.0
tags:
  - security
  - threats
  - intelligence
artifact_type: security-memory
---

# Threat Landscape

Snapshot of the org-relevant threats this team should plan against. Updated quarterly or after a significant industry incident. Used as input to threat-modeling (`skills/threat-modeling/`) and as a finding-weighting signal during security review (`skills/security-review/`).

> **Origin:** filled-in body imported from partner contribution (Tier 9, 2026-05-13). The previous file contained SEED placeholders only. Replace `<H/M/L>` likelihood/impact markers, `<one sentence>` rationale slots, and `<your-org>` references with your organization's specifics before treating as authoritative.

<!-- Last review date: YYYY-MM-DD by @name -->

## Top Threats (Industry Baseline — Refine for Your Org)

### 1. Ransomware-as-a-Service (RaaS)

- **Adversary profile:** financially-motivated affiliates using rented infrastructure (LockBit successors, BlackCat/ALPHV successors, BlackBasta, Akira, Play, etc.).
- **Typical kill chain:** phishing / exposed RDP / unpatched VPN appliance → credential harvesting → AD enumeration → lateral movement via SMB+WinRM → backup destruction → mass encryption → double-extortion leak site.
- **Org likelihood:** `<H/M/L>` <!-- TODO -->
- **Org impact:** `<H/M/L>` <!-- TODO: estimate downtime cost + reputational impact -->
- **Key controls relied upon:** offline immutable backups, EDR, MFA on all remote access, AD tiering, no privileged accounts cached on workstations.

### 2. Identity-as-Perimeter Compromise

- **Adversary profile:** opportunistic credential phishers, MFA-fatigue attackers, OAuth consent-phishing groups, SIM-swap operators targeting high-value accounts.
- **Typical TTPs:** AiTM phishing (Evilginx/EvilProxy), MFA push bombing, OAuth app consent abuse, primary-refresh-token theft, session-cookie theft via infostealer.
- **Org likelihood:** `<H/M/L>` <!-- TODO -->
- **Org impact:** `<H/M/L>` <!-- TODO: depends on what data your IdP gates -->
- **Key controls relied upon:** phishing-resistant MFA (FIDO2/WebAuthn) for admins, Conditional Access with device compliance, OAuth app governance, anomalous-login detection, session-binding to device.

### 3. Supply-Chain Compromise

- **Adversary profile:** state-aligned actors targeting software providers, opportunistic typosquatters on npm/PyPI, malicious GitHub Actions / VS Code extensions.
- **Typical vectors:** dependency confusion, typosquatting, compromised maintainer accounts, malicious updates to legit packages, build-system tampering, GH Action SHA replacement.
- **Org likelihood:** `<H/M/L>` <!-- TODO -->
- **Org impact:** `<H/M/L>` <!-- TODO: depends on dependency surface -->
- **Key controls relied upon:** lockfile pinning, dependency audit in CI (see `tools/scripts/dep_audit.py`), GH Action SHA pinning, SBOM generation, signed artifacts (Sigstore/cosign), build-runner hardening, isolated build environments.

### 4. AI / LLM Prompt Injection & Data Exfiltration

- **Adversary profile:** opportunistic researchers + targeted operators against AI-integrated products.
- **Typical vectors:** direct prompt injection in user input, indirect injection via retrieved documents (RAG poisoning), tool-use abuse, output-rendering exploits (Markdown image to attacker domain), training-data extraction.
- **Org likelihood:** `<H/M/L>` <!-- TODO — high if you ship LLM features, low otherwise -->
- **Org impact:** `<H/M/L>` <!-- TODO -->
- **Key controls relied upon:** input/output filtering, isolated tool-use sandbox, no privileged tools available to LLM without confirmation, RAG source vetting, output-domain allow-listing, prompt-injection eval suite in CI.

### 5. Cloud Misconfiguration (BYOC / Tenant-Sprawl)

- **Adversary profile:** opportunistic scanners (Shodan, internet-wide GET probes) + targeted operators.
- **Typical vectors:** public S3/GCS buckets, exposed admin consoles, IAM role assumable by `*`, leaked CI tokens with `s3:*`, snapshot-publishing misconfigs.
- **Org likelihood:** `<H/M/L>` <!-- TODO -->
- **Org impact:** `<H/M/L>` <!-- TODO -->
- **Key controls relied upon:** CSPM (Checkov / tfsec / cloud-native posture), block-public-access at account level, IaC review (see `skills/security-review/workflows/config-audit.md`), least-privilege IAM, drift detection.

### 6. Insider Risk (Malicious or Negligent)

- **Adversary profile:** disgruntled departing employee, compromised account holder, well-intentioned employee bypassing controls.
- **Typical vectors:** mass download before resignation, unauthorized data sharing to personal email/drive, credential reuse, weak-shadow-IT integrations.
- **Org likelihood:** `<H/M/L>` <!-- TODO -->
- **Org impact:** `<H/M/L>` <!-- TODO -->
- **Key controls relied upon:** DLP, off-boarding automation, anomalous-data-movement alerts, just-in-time access for sensitive systems, role separation.

## Threats Explicitly De-Prioritized

<!-- TODO — list threats your org has assessed as low likelihood/impact and is not investing against (e.g. nation-state physical implant) with one-line rationale each -->

- `<threat>` — rationale: `<one sentence>`

## Recent Incidents Affecting Our Vertical (Industry-Level)

<!-- TODO — list 3–5 public incidents from the past 12 months in your vertical, with one-line takeaway each -->

- `YYYY-MM-DD` — `<company>` — `<incident type>` — Takeaway: `<one sentence>`

## Review Triggers

- Quarterly scheduled review.
- Any SEV-1/2 incident in the org.
- Any significant industry incident in our vertical.
- Material change in business model (new data class, new geography, new customer segment).

## Retired Threats

(Move retired threats here with date and reason. Do not delete — retired threats document what the landscape looked like at past moments.)

- _none yet_

## References

- MITRE ATT&CK: https://attack.mitre.org/
- Verizon DBIR (annual): https://www.verizon.com/business/resources/reports/dbir/
- CISA Known Exploited Vulnerabilities Catalog: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- `knowledge/collections/cis-controls-v8.1.md` — control mapping
- `knowledge/collections/owasp-top-10.md` — application-layer threats
- `knowledge/collections/owasp-api-top-10.md` — API-specific risks
- `knowledge/collections/cwe-top-25.md` — specific weakness types

## Related

- `skills/threat-modeling/SKILL.md` — uses this file to inform likelihood judgments
- `skills/security-review/SKILL.md` — uses this file to weight findings
- `memory/security/incident-log.md` — confirmed instances feed back into this file
- `memory/security/auth-patterns.md` — defensive patterns specific to authn/authz threats
