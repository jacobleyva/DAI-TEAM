---
name: security-review
description: Use when reviewing code, configuration, or infrastructure changes for security risk. Covers authn, authz, input validation, secrets handling, dependency risk, error handling, logging, and crypto. Prioritize findings over summary; cite file:line on every finding.
---

# Security Review

Review with an attacker's eye, but a defender's discipline. The goal is to find real risk that would actually get exploited — not theoretical noise.

## When to Run

- Before merging any change that touches auth, authz, data access, secrets, third-party integrations, or public-facing endpoints
- Before deploying a new service or feature to production
- After ingesting a new dependency
- After an incident in a related system (lessons-learned audit)

## Workflow

1. **Scope the change.** What files changed, what surface did they expose, what trust boundaries do they cross?
2. **Threat surface first.** Before reading line by line, name the assets at stake (customer PII, credentials, write access to systems of record, financial data). Findings are weighted against asset value.
3. **Authn (identity).** Is the user/service identity established by a tool you trust? Are tokens validated, not just parsed? Are sessions bounded? Are anonymous code paths intentional?
4. **Authz (access).** Is access scoped to the resource owner / role / tenant? Is the authorization decision made *server-side* on every request? Are there IDOR or BOLA-style risks?
5. **Input validation + output encoding.** Is untrusted input validated against an allowlist? Is output context-encoded (HTML, SQL, shell, LDAP, JSON, header)? Are file uploads bounded by type, size, and content sniffing?
6. **Secrets handling.** Are credentials referenced by env var or vault, never inlined? Are connection strings free of `password=` literals? Are logs scrubbed?
7. **Dependency risk.** Any new deps? Run `tools/scripts/dep_audit.py` if available. Pin versions; review the CVE status; check supply chain (was the package recently transferred or compromised?).
8. **Error handling + logging.** Does the system fail closed? Do errors leak stack traces, paths, or credentials to clients? Are security events logged (auth failures, privilege changes, admin actions)?
9. **Crypto.** Are algorithms current (no MD5/SHA1 for security, no RC4, no static IVs)? Are random values from a CSPRNG? Are TLS versions modern (1.2+; 1.3 preferred)?
10. **Map findings to a framework.** For each finding, name the CIS Control / OWASP item / CWE that applies. Helps with audit conversations.

## What to prioritize

- Authentication bypass or weakening
- Authorization gaps (horizontal or vertical privilege escalation)
- Injection (SQL, command, LDAP, XPath, NoSQL, template, header)
- Secrets in source, configs, or logs
- Outdated cryptographic primitives or weak random
- Deserialization of untrusted input
- SSRF / open-redirect / unrestricted file inclusion
- Missing rate limits on expensive or sensitive endpoints
- Information disclosure via error responses, debug headers, or stack traces
- Supply chain risk in new or recently-changed dependencies

## What to deprioritize (don't waste reviewer attention)

- Style-only comments unless they hide a real risk
- Theoretical risks with no realistic attack path
- "Best practice" violations that don't change the threat model
- Defense-in-depth gaps when the primary control is solid (note them once, move on)

## Output shape

```
## Findings — by severity

### CRITICAL — [Title]
- **File:** path/to/file:line
- **What:** [the vulnerability, one sentence]
- **Impact:** [what an attacker can do]
- **Reproduce:** [minimal steps or curl]
- **Fix:** [proposed change with file:line or new code]
- **Maps to:** [CIS Control N.N / OWASP A0X / CWE-NNN]

### HIGH — [Title]
…

### MEDIUM — [Title]
…

### LOW / informational — [Title]
…

## Open questions / assumptions
- [Things the reviewer couldn't determine without more context]

## Out of scope
- [Things explicitly not reviewed; why]

## Summary
- N critical, N high, N medium, N low findings
- Blocker for merge? yes/no, with rationale
```

## Guardrails

- Cite `file:line` on every finding. "Somewhere in the auth flow" is not a finding.
- Never invent CVE numbers or vendor advisories. If you don't know, say so.
- Mark assumptions as assumptions. Distinguish "exploitable today" from "fragile and could become exploitable."
- Reproduce the issue (or describe how) before claiming exploitability.
- If no findings at a severity, say so explicitly ("No critical findings.") — silence reads as missed.
- Don't conflate compliance gaps (audit findings) with security gaps (exploitable issues). Both matter, but they get different treatment.

## Anti-criteria — review must not

- Mark findings `[x]` without a reproduction or a tool-verified probe (per `core/ISC.md` and `core/verification-doctrine.md`)
- Recommend "review everything more carefully" or other non-actionable mitigations
- Cite a control framework section that doesn't apply
- Bury blockers in low-severity sections

## Codex Trigger-Phrase Routing

When the user's request matches any of the patterns below, follow the listed workflow.

| Trigger phrase / context | Workflow file |
|---|---|
| "review this code for security issues" / "audit this PR" / "is this safe to merge" | `workflows/code-audit.md` |
| "review Terraform / Kubernetes / Dockerfile" / "check our cloud config" / "review IaC" | `workflows/config-audit.md` |
| "scan repo before release" | both workflows, code-audit first |

Read the entire matching workflow file before producing findings — they encode the checklist that defines completeness.

## Inputs to Confirm Before Starting

- **Scope** — file paths, PR diff, or directory. Don't expand beyond stated scope.
- **Threat model context** (optional) — if `memory/security/threat-landscape.md` or a feature-specific threat model exists, read it first and focus review on documented trust boundaries.
- **Severity baseline** (optional) — default to OWASP risk rating (likelihood × impact). Override only if the user states otherwise.

## Codex Finding Schema (the precise output shape)

Each finding emitted in this exact shape:

```
[severity] <short-title>
  Where:    path/to/file.ext:LINE-LINE
  CWE:      CWE-XXX (name)
  OWASP:    A0X:2021 — Category (if applicable)
  Impact:   one-sentence consequence
  Evidence: code excerpt or config snippet
  Fix:      concrete remediation, not just "validate input"
  Verify:   command or test that proves the fix
```

Findings are emitted as a Markdown table at the end of the review, sorted by severity (CRITICAL → HIGH → MEDIUM → LOW → INFO).

## Acceptance — Review is Complete Only When

1. Every file in scope has been examined (manual or tool-assisted).
2. At least one of: SAST tool run with output, regex-based secret scan, manual line-by-line for files < 200 lines.
3. Each finding has all 7 fields above (severity, where, CWE, OWASP, impact, evidence, fix, verify).
4. Output references this SKILL.md and any threat model consulted.

## Tool-Verifiable Completion Probe

The user can confirm the workflow completed by checking that the output contains:
- A findings table with at least the 7 fields above.
- A reference to which workflow file was followed.
- An "Adjacent Risks" section (may be empty, but must exist as a header).

## Workflow Files

- `workflows/code-audit.md` — source-code review (6 phases, manual checklist by domain)
- `workflows/config-audit.md` — IaC / cloud / container / CI / Kubernetes review (7 phases)

## Related

- `skills/threat-modeling/SKILL.md` — feeds the threat surface that grounds severity judgments
- `skills/code-review/SKILL.md` — for non-security correctness review on the same change
- `skills/cis-controls/SKILL.md` — for mapping findings to CIS controls
- `core/verification-doctrine.md` — the required-probe-per-artifact rule applies here too
- `core/SECURITY_DOMAIN_OVERVIEW.md` — domain-wide doctrine that applies to all security skills
- `memory/security/threat-landscape.md` — current threat intel for the domain
- `memory/security/auth-patterns.md` — defensive patterns specific to authn/authz threats
- `memory/security/incident-log.md` — past incidents that should inform what to look for
- `knowledge/collections/owasp-top-10.md` — application-layer threat categories
- `knowledge/collections/owasp-api-top-10.md` — API-specific risks
- `knowledge/collections/cwe-top-25.md` — specific weakness IDs for findings
- `knowledge/collections/cis-controls-v8.1.md` — control catalog for the mitigations matrix
