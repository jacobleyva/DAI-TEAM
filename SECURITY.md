---
title: Security Policy
type: reference
domain: dai
product: DAI
audience: contributors
owner: team
status: active
updated: 2026-05-14
tags:
  - security
  - disclosure
  - vulnerability
artifact_type: security-policy
---

# Security Policy

> DAI ships discipline that runs alongside AI coding assistants in real engineering environments. A vulnerability in the doctrine or tooling could affect every team that adopts it. We take that responsibility seriously.

## Supported Versions

| Version | Supported | Notes |
|---------|-----------|-------|
| v1.0.x  | Yes — full support | Current line. Security patches land within the response windows below. |

When a new minor or major version ships, the prior line receives critical-only patches for 90 days, then enters end-of-life.

## Reporting a Vulnerability

**Please report security issues privately. Do not open a public issue or PR for security findings.**

DAI is repo-source-neutral; the private disclosure path depends on which platform hosts your DAI fork or clone:

- **GitHub-hosted:** open a **GitHub Security Advisory** on this repository — Settings → Security → Report a vulnerability. Gives us a private workspace and an audit trail.
- **Azure DevOps Repos-hosted:** open a private work item of type **Security Vulnerability** (see `core/REPO_INTEGRATION.md` for the work-item-type setup). Restrict view permissions to the security-domain group. Tag the maintainer.
- **GitLab / Bitbucket / on-prem hosted:** use that platform's private/confidential issue mechanism with restricted visibility.

For the upstream public repository, the preferred channel is the GitHub Security Advisory.

Fallback (any platform): email the maintainer at `jacobleyva@users.noreply.github.com` (GitHub-routed; the actual mailbox is on the maintainer's GitHub profile). Mark the subject `[DAI SECURITY]`.

Include in your report:

- A description of the issue and the impact, in plain English
- Steps to reproduce, with concrete inputs and expected vs. actual outputs
- The version (commit hash if possible) you observed it on
- Any proof-of-concept code or screenshots, attached or linked
- Your preferred contact method and whether you want credit in the eventual advisory

We will acknowledge receipt and assign a severity within the response window below.

## Response Windows

DAI is currently maintained by a small group of contributors on a best-effort basis. The windows below are realistic targets for a community-maintained open-source project, not enterprise-grade SLAs.

| Severity | First response | Status update cadence | Target fix window |
|----------|---------------|----------------------|-------------------|
| Critical (active exploitation possible, broad blast radius) | within 3 working days | every 5 working days | 14 days |
| High (significant impact, plausible attack path) | within 5 working days | weekly | 30 days |
| Medium (limited impact, requires specific conditions) | within 10 working days | bi-weekly | 90 days |
| Low (informational, hardening) | within 15 working days | none until fix lands | next minor release |

If a fix requires longer than the target window, we will say so explicitly in a status update, with the reason and the new estimate.

Teams adopting DAI in their own fork are encouraged to tighten these windows to match their staffing — the schema above is a starting floor, not a ceiling.

## Coordinated Disclosure

We follow a 90-day coordinated disclosure model by default.

- We will request that you keep the issue confidential until a fix is available
- We will not threaten or pursue legal action against good-faith researchers who follow this policy
- We will credit reporters in the published advisory unless asked otherwise
- If we cannot fix the issue within 90 days and the issue is actively exploitable, we will agree on a coordinated public disclosure date that gives users a fair chance to upgrade

## What Counts as a Security Issue

Examples that fall under this policy:

- Doctrine that, if followed, leads to a known-bad outcome (e.g., a recipe that recommends storing credentials in a way that exposes them)
- Tooling in `tools/scripts/` that has injection, path-traversal, or arbitrary-file-write vulnerabilities
- Pre-commit hook bypasses that allow secrets through undetected
- The bootstrap flow doing something on a host that exceeds what the documentation says it does
- Default skill configurations that would leak sensitive information when used as documented

## What Does Not Count

- Bugs without a security impact — file a normal issue
- Vulnerabilities in user-written workflows that the project does not ship
- Issues in third-party dependencies — report those upstream first; we'll coordinate

## Acknowledgments

Reported issues that lead to fixes will be acknowledged in the release notes of the patched version unless the reporter asks to remain anonymous.

Thank you for helping keep DAI safe to deploy.
