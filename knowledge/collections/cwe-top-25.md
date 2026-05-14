---
title: CWE Top 25 Most Dangerous Software Weaknesses (2024)
type: knowledge
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
tags:
  - security
  - cwe
  - weaknesses
  - knowledge
artifact_type: knowledge-collection
---

# CWE Top 25 Most Dangerous Software Weaknesses — 2024

Source: https://cwe.mitre.org/top25/
Retrieved: 2026-05-12
License: CWE™ is sponsored by CISA and operated by MITRE; content released for public use.

## What This Is

The CWE Top 25 is an annual ranking of the most dangerous software weakness types, computed from CVE data over the prior two years. Maintained by the MITRE Corporation / CISA. Where OWASP Top 10 is web-focused and category-level, CWE Top 25 is more granular (specific weakness types) and language/platform-agnostic.

Scoring formula: each CWE's frequency in CVEs × average CVSS severity, normalized. 2024 list uses 2023–2024 CVE data.

## 2024 Top 25 (Current as of May 2026)

| Rank | CWE ID | Name | One-line description |
|---|---|---|---|
| 1 | CWE-787 | Out-of-bounds Write | Writing past the bounds of a buffer; leading cause of memory-corruption RCE. |
| 2 | CWE-79 | Improper Neutralization of Input During Web Page Generation (XSS) | User input rendered into HTML/JS context without escaping. |
| 3 | CWE-89 | SQL Injection | User input concatenated into SQL queries. |
| 4 | CWE-352 | Cross-Site Request Forgery (CSRF) | State-changing actions accept cross-origin requests without origin verification. |
| 5 | CWE-22 | Path Traversal | User-controlled file path lets attacker escape intended directory. |
| 6 | CWE-125 | Out-of-bounds Read | Reading past buffer bounds; leaks memory contents. |
| 7 | CWE-78 | OS Command Injection | User input concatenated into a command invocation. |
| 8 | CWE-416 | Use After Free | Memory used after being released; corruption/RCE vector. |
| 9 | CWE-862 | Missing Authorization | Endpoint with no auth check at all. |
| 10 | CWE-434 | Unrestricted Upload of File with Dangerous Type | Upload accepts executable types (.php, .jsp, .aspx) without validation. |
| 11 | CWE-94 | Improper Control of Generation of Code (Code Injection) | `eval()`, `Function()`, dynamic-load with attacker-controlled input. |
| 12 | CWE-20 | Improper Input Validation | Generic input validation failures (catch-all category). |
| 13 | CWE-77 | Command Injection | Cousin of CWE-78; broader scope (any command interpreter). |
| 14 | CWE-287 | Improper Authentication | Auth logic flaws that let users bypass (different from "missing" — broken). |
| 15 | CWE-269 | Improper Privilege Management | Permissions granted incorrectly; privilege escalation paths. |
| 16 | CWE-502 | Deserialization of Untrusted Data | Unsafe deserialization (pickle, fastjson, ObjectInputStream) -> RCE. |
| 17 | CWE-200 | Exposure of Sensitive Information to an Unauthorized Actor | Information disclosure: verbose errors, debug pages, side channels. |
| 18 | CWE-863 | Incorrect Authorization | Auth check exists but is wrong (compare CWE-862 = missing). |
| 19 | CWE-918 | Server-Side Request Forgery (SSRF) | Server fetches URL from user input; attacker pivots to internal services. |
| 20 | CWE-119 | Improper Restriction of Operations within Bounds of a Memory Buffer | Parent class of CWE-787, CWE-125; broader memory-safety failures. |
| 21 | CWE-476 | NULL Pointer Dereference | Crash / DoS, sometimes exploitable for RCE in C/C++. |
| 22 | CWE-798 | Use of Hard-coded Credentials | Credentials in source/config files. |
| 23 | CWE-190 | Integer Overflow or Wraparound | Arithmetic exceeds type bounds -> memory corruption or logic bypass. |
| 24 | CWE-400 | Uncontrolled Resource Consumption | DoS via resource exhaustion (memory, CPU, file handles, threads). |
| 25 | CWE-306 | Missing Authentication for Critical Function | No auth required where there should be (e.g. admin API). |

## Top 25 by Category

**Memory safety (C/C++ language risks)** — CWE-787, CWE-125, CWE-416, CWE-119, CWE-476, CWE-190. Six of 25. Memory-safe languages (Rust, Go, Java, Python, JS) eliminate or sharply reduce these.

**Injection** — CWE-79, CWE-89, CWE-78, CWE-77, CWE-94, CWE-918. Six of 25.

**Authorization / Authentication** — CWE-862, CWE-287, CWE-863, CWE-269, CWE-306, CWE-798. Six of 25.

**Web-specific** — CWE-352, CWE-22, CWE-434. Three of 25.

**Data handling** — CWE-502, CWE-200, CWE-20. Three of 25.

**Resource** — CWE-400. One of 25.

## How To Use This in Reviews

Every finding in `skills/security-review/SKILL.md` includes a CWE field. Prefer the most specific applicable CWE from this list. CWE Top 25 finding presence on a repo is a flag for additional review depth.

## Versioning Note

CWE Top 25 is republished annually. Check https://cwe.mitre.org/top25/ for the latest before treating any single year's list as authoritative. The 2024 list is the most recent as of this export's retrieval date.

## Notes for Ingestion

Full per-CWE documentation (description, examples, mitigations, taxonomy mappings) at https://cwe.mitre.org/data/definitions/{ID}.html. CWE entries cross-reference to CAPEC (attack patterns) and OWASP categories.
