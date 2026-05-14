---
title: OWASP API Security Top 10 (2023)
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
  - api
  - knowledge
artifact_type: knowledge-collection
---

# OWASP API Security Top 10 — 2023

Source: https://owasp.org/API-Security/editions/2023/en/0x11-t10/
Retrieved: 2026-05-12
License: OWASP API Security docs are released under Creative Commons CC-BY-SA 4.0.

## What This Is

The OWASP API Security Top 10 enumerates the most critical risks specific to APIs (separate from the general OWASP Top 10 because APIs have distinct attack surface — they often skip the UI layer and lack browser-level protections). The 2023 edition is the current version as of May 2026.

## The 10

### API1:2023 — Broken Object Level Authorization (BOLA)
Most prevalent and impactful API risk. Endpoint authorizes the *user* but doesn't verify the user owns the *object* in the request. AKA IDOR at the API layer.

**Canonical example:** `GET /api/orders/12345` returns order 12345 whenever any authenticated user requests it, without checking ownership.

**Detection probe:** swap object IDs in API calls between two test users; if responses leak data, you have BOLA.

### API2:2023 — Broken Authentication
Weak or missing auth at the API layer. Compromised token, weak token validation, missing rate limits on auth endpoints, account-takeover flows.

**Canonical example:** API accepts JWT without verifying signature; uses `alg: none`; or has no rate limit on login endpoint.

### API3:2023 — Broken Object Property Level Authorization
Was two separate items in 2019 (Excessive Data Exposure + Mass Assignment), now merged. Either: the response includes more fields than the user should see, OR the request body can set fields the user shouldn't be able to set.

**Canonical examples:**
- **Excessive Data Exposure:** `GET /users/me` returns `internal_admin_notes` field that the client filters in JS but the API shouldn't return.
- **Mass Assignment:** `PATCH /users/me` body includes `{"is_admin": true}` and the API blindly persists it because the user model has that field.

### API4:2023 — Unrestricted Resource Consumption
Was "Lack of Resources & Rate Limiting" in 2019. APIs that allow unbounded compute / memory / network / cost.

**Canonical examples:** GraphQL endpoint accepting deeply-nested queries; export endpoint with no row limit; SMS-send API with no per-user quota leading to large telco bills.

### API5:2023 — Broken Function Level Authorization (BFLA)
User is authorized at the object level but not for the *function*. E.g. regular user can call admin-only endpoint because authZ only checks "is logged in" not "is admin".

**Canonical example:** `POST /api/admin/users/123/delete` succeeds when called by a non-admin user because the admin check exists only in the admin UI.

### API6:2023 — Unrestricted Access to Sensitive Business Flows (NEW)
Business-logic abuse: legitimate API calls used at illegitimate scale to harm the business. Scalping (sneakers), credential stuffing, reservation hoarding, comment-spam farms.

**Canonical example:** Ticketing API permits arbitrarily fast checkout; bot army buys all concert tickets in 4 seconds.

### API7:2023 — Server-Side Request Forgery (SSRF)
APIs that fetch remote resources by URL given in input. Increased prevalence in 2023 because of webhook/integration-heavy APIs.

**Canonical example:** Webhook setup API accepts any URL; attacker provides `http://169.254.169.254/...` and reads cloud metadata.

### API8:2023 — Security Misconfiguration
Same family as web Top 10 A05 but API-flavored: missing security headers, verbose errors, unnecessary HTTP methods enabled, CORS too permissive, TLS misconfig, default credentials on management API.

### API9:2023 — Improper Inventory Management
Was "Improper Assets Management" in 2019. Risks from "shadow" or "zombie" API versions: v1 still up after v1 release, dev/staging APIs internet-exposed, undocumented endpoints reachable.

**Canonical example:** v1 of an API was deprecated for security reasons but still receives requests because v1 servers were never shut down.

### API10:2023 — Unsafe Consumption of APIs
NEW category. Risk that flows *into* you when your API consumes another API: blind trust in third-party API responses, no input validation on responses, no rate-limit on outbound calls, plaintext callbacks.

**Canonical example:** Your API queries a third-party enrichment service and stores the response in your DB without validation; the third-party gets compromised and serves malicious payloads that propagate to your system.

## Map to General Top 10

| API Top 10 | Closest Web Top 10 |
|---|---|
| API1, API3, API5 | A01:2021 Broken Access Control |
| API2 | A07:2021 Identification & Auth Failures |
| API4, API6 | A04:2021 Insecure Design |
| API7 | A10:2021 SSRF |
| API8 | A05:2021 Security Misconfiguration |
| API9 | (cross-cutting: A04 + A05) |
| API10 | A08:2021 Software & Data Integrity Failures |

## How To Use This in Reviews

For any API surface in scope (your service's endpoints OR third-party APIs you call):
1. Run the API1–API10 checklist alongside the general code-audit checklist.
2. Findings reference API0X:2023 IDs.
3. Pay special attention to API1, API3, API5 — these are where most actual breaches happen.

## Notes for Ingestion

Full canonical content at https://owasp.org/API-Security/editions/2023/en/0x11-t10/. Each category has detailed mitigation guidance, references, and example payloads.
