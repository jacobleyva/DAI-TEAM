---
title: Workflow — Code Audit
type: workflow
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
tags:
  - security
  - code-audit
  - workflow
  - sast
artifact_type: skill-workflow
---

# Workflow: Code Audit

Source-code security review. Follow phases in order. Each phase has a tool-verifiable exit probe.

## Phase 1 — Scope

1. List target files. If reviewing a PR, use `git diff --name-only $BASE..HEAD`.
2. Identify the language(s) and frameworks in scope.
3. Read any existing threat model for the system (`memory/security/threat-landscape.md` if relevant).

**Exit probe:** scope list produced and confirmed with requester.

## Phase 2 — Automated SAST

Run at least one of:

| Language | Tool | Command |
|---|---|---|
| Polyglot | Semgrep | `semgrep --config=auto --json -o sast.json <scope>` |
| Python | Bandit | `bandit -r <scope> -f json -o bandit.json` |
| JavaScript/TS | ESLint security | `npx eslint --ext .js,.ts -f json <scope> > eslint.json` |
| Go | gosec | `gosec -fmt=json -out=gosec.json <scope>` |
| Java | SpotBugs / Find Security Bugs | `spotbugs -textui -xml:withMessages <scope>` |

Triage findings: keep CRITICAL/HIGH and language/framework-relevant MEDIUMs.

**Exit probe:** SAST output file exists and has been triaged into a shortlist.

## Phase 3 — Secrets

```bash
# Quick regex pass (extends pre-commit hook patterns)
grep -rEn '(sk_live_|rk_live_|AIza[0-9A-Za-z\-_]{35}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|eyJ[A-Za-z0-9_=-]+\.[A-Za-z0-9_=-]+\.[A-Za-z0-9_.+/=-]*)' <scope>

# Better: gitleaks or trufflehog
gitleaks detect --source=<scope> --report-format=json --report-path=secrets.json
```

**Exit probe:** zero unexplained matches, or all matches documented as false positives.

## Phase 4 — Manual Checklist

For each file in scope, walk the checklist. Mark each item Pass / Fail / N/A.

### Authentication & Session
- [ ] No credentials, tokens, or keys hardcoded.
- [ ] Password storage uses adaptive hash (argon2id, bcrypt, scrypt) — not MD5, SHA1, plain SHA256.
- [ ] Session tokens generated from CSPRNG (`secrets.token_urlsafe`, `crypto.randomBytes`).
- [ ] Token validation is constant-time (`hmac.compare_digest`, `crypto.timingSafeEqual`).
- [ ] Session/JWT expiration enforced; refresh tokens rotated on use.
- [ ] Logout invalidates server-side state (not just client cookie).

### Authorization
- [ ] Every route/handler enforces authZ — not just authN ("logged in" ≠ "allowed").
- [ ] Object-level access checks before any read/write of user-owned data (prevents IDOR, OWASP API1).
- [ ] No role/permission strings derived from client-controllable input.
- [ ] Admin endpoints isolated and explicit (no implicit role escalation paths).

### Input Validation
- [ ] All external input validated at the boundary (type, length, format, allowed values).
- [ ] Validation is allow-list, not deny-list, where possible.
- [ ] Parameterized queries / prepared statements for SQL (no string concat).
- [ ] HTML output escaped by template engine or explicit sanitizer (DOMPurify, Bleach).
- [ ] Shell command construction uses argv lists, not concatenated strings (`subprocess.run([...], shell=False)`).
- [ ] File paths normalized and confined to expected base directory (`os.path.commonpath`, `path.resolve` checks).

### Crypto
- [ ] No custom crypto. Algorithms from vetted libraries (`cryptography`, `libsodium`, platform stdlib).
- [ ] AES uses authenticated mode (GCM, ChaCha20-Poly1305) — never ECB, rarely CBC.
- [ ] IVs/nonces unique per encryption operation.
- [ ] TLS verification enabled (`verify=True`, `rejectUnauthorized=true`).
- [ ] Key material loaded from KMS/vault, not source or env-in-image.

### Deserialization & Parsing
- [ ] No `pickle.loads`, `yaml.load` (without SafeLoader), `eval`, `Function()`, `unserialize()` on untrusted input.
- [ ] JSON parsers configured with depth/size limits where the library supports it.
- [ ] XML parsers disable DTDs and external entities (defusedxml, `DocumentBuilderFactory.setFeature("...disallow-doctype-decl", true)`).

### SSRF / Network
- [ ] Outbound HTTP from server-side never built from raw user input. If it must, allow-list the destination domain and block private CIDRs (RFC 1918, 169.254.169.254, ::1, fc00::/7).
- [ ] No URL fetchers follow redirects without re-checking destination.
- [ ] Webhooks / file URL features validate scheme (`https://` only) before fetch.

### Logging & Monitoring
- [ ] Auth events (success, failure, lockout), authZ failures, and admin actions logged.
- [ ] Logs DO NOT contain: passwords, tokens, full PAN, full SSN, full session cookies.
- [ ] Correlation IDs propagated across services.
- [ ] No raw user input echoed into structured logs without sanitization (log injection).

### Error Handling
- [ ] Stack traces / framework debug pages disabled in production.
- [ ] Generic error messages to clients; details only in server logs.
- [ ] Sensitive operations fail closed (deny by default).

### Dependencies
- [ ] Lockfile present and pinned.
- [ ] `dep_audit.py` (this skill's bundled tool) run on the project's manifest.

**Exit probe:** every checklist item resolved (Pass / Fail / N/A); all Fails enumerated as findings.

## Phase 5 — Emit Findings

Produce the table per the output format in the parent `SKILL.md`. For each finding, include the `Verify:` command — typically the inverse of the regex/check that found it, or a unit test asserting the fixed behavior.

## Phase 6 — Adjacent Risks

Note out-of-scope concerns observed during review (e.g. "the auth module isn't in this PR but reuses the same flawed `validate_session()` helper"). Don't audit them; flag them.

## Acceptance Criteria (workflow-level)

- All 6 phases completed; exit probes documented.
- Findings table emitted with all 7 fields per finding.
- SAST tool output file retained as evidence.
- Adjacent risks listed separately.
