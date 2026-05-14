---
title: Auth Patterns
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
  - authentication
  - authorization
  - patterns
artifact_type: security-memory
---

# Authentication & Authorization Patterns

Preferred patterns for new services. Reviewed and adopted as defaults; deviations need security review.

> **Origin:** filled-in body imported from partner contribution (Tier 9, 2026-05-13). The previous file contained SEED placeholders only. Replace `<your IdP>`, `<your CIAM>`, and any other `<placeholder>` markers with your organization's actual defaults before treating as authoritative.

<!-- Last review date: YYYY-MM-DD by @name -->

## Identity Providers

- **Workforce identity (employees):** `<your IdP>` (e.g. Okta / Entra ID / Google Workspace) <!-- TODO -->. Single source of truth; no local accounts on workforce-facing apps except break-glass.
- **Customer identity (B2C/B2B end-users):** `<your CIAM>` (e.g. Auth0 / Cognito / WorkOS / Stytch) <!-- TODO -->. SAML/OIDC federation supported for B2B SSO customers.
- **Service-to-service:** workload identity (IAM roles, IRSA, GKE Workload Identity, Azure Managed Identity). **No long-lived API keys** for service accounts that can use platform identity.

## Public-Facing Authentication

### Web SPA → API
- **Pattern:** OIDC Authorization Code + PKCE (RFC 7636).
- **Token type:** short-lived access token (10–15 min) + rotating refresh token in HttpOnly + Secure + SameSite=Strict cookie (or via BFF pattern).
- **No tokens in localStorage.** Susceptible to XSS exfil.

### Mobile → API
- **Pattern:** OIDC Authorization Code + PKCE.
- **Token storage:** platform secure storage (iOS Keychain / Android Keystore + StrongBox-backed key).
- **Bind tokens to device** via DPoP (RFC 9449) where library support allows.

### Server-to-API (machine clients)
- **Pattern:** OAuth 2.0 Client Credentials with mTLS-bound or DPoP-bound tokens.
- **Reject:** static bearer tokens with unbounded lifetimes.

## Multi-Factor Authentication

- **Workforce admins:** **phishing-resistant MFA required** — FIDO2/WebAuthn (hardware key or platform passkey). TOTP fallback only with help-desk recovery process.
- **Workforce general users:** TOTP at minimum; passkey preferred.
- **Customer end-users:** TOTP or passkey; SMS only as last resort and never for high-value transactions.
- **Reject:** SMS-only for admins; OTP via email as primary factor; push approval without number-matching (MFA fatigue mitigation).

## Service-to-Service Authentication

- **Within a cluster / private network:** **mTLS** via service mesh (Istio strict mode, Linkerd, Consul Connect). Cert lifecycle managed by mesh CA (SPIRE or built-in).
- **Across trust zones / external:** OAuth Client Credentials with workload identity issuing the credential; tokens bound to caller via mTLS or DPoP.
- **Cloud APIs (within same cloud account):** native workload identity, never access keys.
- **Cloud APIs (cross-cloud or external):** federated identity via OIDC trust (e.g. GitHub Actions → AWS via `sts:AssumeRoleWithWebIdentity`); reject hardcoded keys.

## Session Management

- **Session storage:** server-side session ID lookup or cryptographically-signed stateless tokens. Don't put authorization claims in the session/JWT — fetch fresh from authoritative source.
- **Session lifetime:** access ≤ 15 min, refresh ≤ 24 h for SPA; 8 h max for sensitive admin sessions.
- **Idle timeout:** 30 min for admin, 24 h for general.
- **Reauth required for:** password change, MFA change, payment method add, role elevation, sensitive data export.
- **Logout invalidates:** server-side session record AND all refresh tokens for that session.

## Token Patterns

- **JWT:**
  - Algorithm pinned in verification (don't trust `alg` from header alone — reject `none`, reject algorithm switching).
  - Short TTL.
  - Audience (`aud`) and issuer (`iss`) checked on every verification.
  - Signing key rotation supported via JWKS.
- **Opaque tokens** (preferred for sensitive systems) — server lookup on each use; immediate revocation possible.

## Authorization

- **Default deny.** Every route, every action requires explicit permission check.
- **Object-level authorization** on every read/write of user-owned data — prevents IDOR / BOLA (OWASP API1:2023).
- **Role/permission strings never derived from client input.** Server-side mapping only.
- **Admin operations** require fresh-auth (re-prompt for MFA within last N minutes) AND step-up logging.
- **Just-in-time access** for production / sensitive systems: time-bounded grants via approval workflow; no standing admin access.

## Secrets Management

- **Secrets in code:** never. Enforced by pre-commit hook + CI scanning. <!-- partner's pre-commit-secrets-extension.sh referenced but absent from the import; existing DAI hook covers the major shapes. -->
- **Secrets in env at runtime:** acceptable for short-lived workload-identity-issued tokens; not acceptable for long-lived API keys.
- **Preferred:** secrets manager / vault, fetched via workload identity at startup or per-use.
- **Rotation:** automated where provider supports; 90-day max for any long-lived credential.
- **No secrets in images.** Build-time secrets via `--mount=type=secret`, not `ARG` or `ENV`.

## Account Recovery

- **High-risk path** — single most-attacked surface.
- Require multiple proofs (verified email + verified phone + known-device cookie at minimum).
- Trigger high-friction recovery for: changes to MFA, changes to recovery email, after suspicious-activity flag.
- Notify on every recovery attempt to all known channels.

## Anti-Patterns (Reject These on Sight)

- Custom crypto (rolling our own hash, encryption, signing).
- Plaintext password storage or non-adaptive hashes (MD5, SHA1, plain SHA2).
- Long-lived bearer tokens with broad scope.
- Authorization checks only in UI (must be server-side).
- "Trust the network" service-to-service auth (network position ≠ identity).
- API keys in URLs (logged everywhere).
- Static service account passwords > 90 days.
- MFA bypass via "remember device forever".

## Retired Patterns

(Move retired patterns here with date and reason.)

- _none yet_

## References

- OAuth 2.0 Security BCP: https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics
- NIST SP 800-63B (Authenticator Assurance Levels): https://pages.nist.gov/800-63-3/sp800-63b.html
- OWASP ASVS v4 (Authentication / Session / Access Control chapters): https://owasp.org/www-project-application-security-verification-standard/
- `knowledge/collections/owasp-api-top-10.md` — API1 BOLA, API2 Auth, API5 BFLA

## Related

- `skills/security-review/SKILL.md` — references these patterns when reviewing auth code
- `skills/threat-modeling/SKILL.md` — the patterns inform threat-mitigation choices
- `memory/security/threat-landscape.md` — threats that motivate the patterns
