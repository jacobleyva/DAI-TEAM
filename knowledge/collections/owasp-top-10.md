---
title: OWASP Top 10 (2021)
type: knowledge
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
tags:
  - security
  - owasp
  - web
  - knowledge
artifact_type: knowledge-collection
---

# OWASP Top 10 — 2021 (Web Application Risks)

Source: https://owasp.org/Top10/
Retrieved: 2026-05-12
License: OWASP Top 10 documents are released under Creative Commons CC-BY-SA 4.0.

## What This Is

The OWASP Top 10 is the most-cited list of critical web application security risks. The 2021 edition (current as of May 2026) is data-driven from contributed CVE/CWE statistics across hundreds of organizations and a community survey for emerging risks. Compiled by the Open Web Application Security Project (OWASP) — a non-profit.

> A new edition is in active development; check https://owasp.org/Top10/ for the latest before treating any item as final.

## The 10

### A01:2021 — Broken Access Control
Moved up from #5 in 2017. Failures enforcing what authenticated users are allowed to do. **94% of tested apps** had some form of broken access control.

**Common manifestations:** IDOR, missing function-level auth checks, JWT tampering, CORS misconfig allowing untrusted origins, force-browsing to authenticated pages, privilege escalation via metadata.

**Canonical example:** `GET /api/account/123` returns account 123's data without verifying the authenticated user owns account 123.

**Map to:** CWE-22, CWE-23, CWE-35, CWE-59, CWE-200, CWE-201, CWE-264, CWE-275, CWE-276, CWE-284, CWE-285, CWE-352, CWE-359, CWE-377, CWE-402, CWE-425, CWE-441, CWE-497, CWE-538, CWE-540, CWE-548, CWE-552, CWE-566, CWE-601, CWE-639, CWE-651, CWE-668, CWE-706, CWE-862, CWE-863, CWE-913, CWE-922, CWE-1275.

### A02:2021 — Cryptographic Failures
Renamed from "Sensitive Data Exposure". Focus shifted from symptom (data leak) to cause (weak crypto). Covers missing encryption, weak algorithms, poor key management, deprecated TLS, missing integrity checks.

**Canonical example:** Passwords stored with unsalted SHA1, or TLS 1.0/1.1 enabled, or AES in ECB mode for sensitive plaintext.

**Map to:** CWE-261, CWE-296, CWE-310, CWE-319, CWE-321, CWE-322, CWE-323, CWE-324, CWE-325, CWE-326, CWE-327, CWE-328, CWE-329, CWE-330, CWE-331, CWE-335, CWE-336, CWE-337, CWE-338, CWE-340, CWE-347, CWE-523, CWE-720, CWE-757, CWE-759, CWE-760, CWE-780, CWE-818, CWE-916.

### A03:2021 — Injection
Was #1 in 2017. Cross-Site Scripting (XSS) merged in. SQL injection, NoSQL injection, OS command injection, LDAP injection, expression-language injection, ORM injection. Common factor: unvalidated user input concatenated into an interpreter context.

**Canonical example:** `db.query("SELECT * FROM users WHERE id=" + request.params.id)` — adversary sends `1 OR 1=1; DROP TABLE users; --`.

**Map to:** CWE-20, CWE-74, CWE-75, CWE-77, CWE-78, CWE-79, CWE-80, CWE-83, CWE-87, CWE-88, CWE-89, CWE-90, CWE-91, CWE-93, CWE-94, CWE-95, CWE-96, CWE-97, CWE-98, CWE-99, CWE-100, CWE-113, CWE-116, CWE-138, CWE-184, CWE-470, CWE-471, CWE-564, CWE-610, CWE-643, CWE-644, CWE-652, CWE-917.

### A04:2021 — Insecure Design (NEW)
First time appearing. Failures in threat modeling, secure-by-design patterns, business-logic enforcement. Distinguishes design flaws (can't be patched out) from implementation flaws (this whole list normally).

**Canonical example:** A "view your friend's profile" feature designed without rate limiting, enabling enumeration of all profiles via sequential IDs.

**Map to:** CWE-73, CWE-183, CWE-209, CWE-213, CWE-235, CWE-256, CWE-257, CWE-266, CWE-269, CWE-280, CWE-311, CWE-312, CWE-313, CWE-316, CWE-419, CWE-430, CWE-434, CWE-444, CWE-451, CWE-472, CWE-501, CWE-522, CWE-525, CWE-539, CWE-579, CWE-598, CWE-602, CWE-642, CWE-646, CWE-650, CWE-653, CWE-656, CWE-657, CWE-799, CWE-807, CWE-840, CWE-841, CWE-927, CWE-1021, CWE-1173.

### A05:2021 — Security Misconfiguration
XML External Entities (XXE) from 2017 merged in. Default accounts/passwords, unnecessary features enabled, verbose error messages, missing security headers, outdated software.

**Canonical example:** Production app returns full stack traces on errors; admin console reachable on default port with default credentials.

**Map to:** CWE-2, CWE-11, CWE-13, CWE-15, CWE-16, CWE-260, CWE-315, CWE-520, CWE-526, CWE-537, CWE-541, CWE-547, CWE-611, CWE-614, CWE-756, CWE-776, CWE-942, CWE-1004, CWE-1032, CWE-1174.

### A06:2021 — Vulnerable and Outdated Components
Was "Using Components with Known Vulnerabilities". Dependency-related risk: known CVEs in libraries, unmaintained software, missing patches.

**Canonical example:** App pinned to Log4j 2.14 in December 2021 — CVE-2021-44228 (Log4Shell) RCE.

**Map to:** CWE-937, CWE-1035, CWE-1104.

### A07:2021 — Identification and Authentication Failures
Was "Broken Authentication". Weak passwords allowed, credential stuffing not detected, weak MFA, predictable session tokens, JWT verification bugs.

**Canonical example:** Login endpoint with no rate limit, allows password spraying.

**Map to:** CWE-255, CWE-259, CWE-287, CWE-288, CWE-290, CWE-294, CWE-295, CWE-297, CWE-300, CWE-302, CWE-304, CWE-306, CWE-307, CWE-346, CWE-384, CWE-521, CWE-613, CWE-620, CWE-640, CWE-798, CWE-940, CWE-1216.

### A08:2021 — Software and Data Integrity Failures (NEW)
Focus on supply-chain and CI/CD. Dependency confusion, unsigned artifacts, insecure deserialization, auto-update without integrity checks.

**Canonical example:** A build pipeline that pulls Docker base images via `:latest` tag with no digest pinning.

**Map to:** CWE-345, CWE-353, CWE-426, CWE-494, CWE-502, CWE-565, CWE-784, CWE-829, CWE-830, CWE-915.

### A09:2021 — Security Logging and Monitoring Failures
Was "Insufficient Logging & Monitoring". Auth events not logged, failures not alerted, logs purged too early, lacking correlation, log injection.

**Canonical example:** Failed-login spike from one IP across thousands of accounts not detected because the auth service logs to console only.

**Map to:** CWE-117, CWE-223, CWE-532, CWE-778.

### A10:2021 — Server-Side Request Forgery (SSRF)
Promoted from community survey. Server fetches a URL from user input; attacker points it at internal services or cloud metadata.

**Canonical example:** Image-upload feature accepts `https://attacker.com/img.png`, but also `http://169.254.169.254/latest/meta-data/iam/security-credentials/` to steal AWS instance creds.

**Map to:** CWE-918.

## How To Use This in Reviews

When emitting findings (per `skills/security-review/SKILL.md`), every applicable finding maps to:
- An OWASP A0X:2021 category (or "N/A — operational" if neither web-app risk).
- A specific CWE from the lists above (the most specific applicable one).

This lets findings roll up to the Top 10 dashboard the org tracks.

## Notes for Ingestion

The full OWASP Top 10 docs include data-collection methodology, contributor lists, per-category mitigation chapters, and per-CWE deep-dives. Pull the canonical content from owasp.org for any work beyond ranking/categorization.
