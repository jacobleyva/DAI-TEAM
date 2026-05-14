<!--
DAI Pull Request Template

Fill in every section that applies. Delete sections that are explicitly N/A
only after writing a one-line reason. If you're touching `core/`, you also
need a second reviewer per CONTRIBUTING.md.
-->

## What This Changes

<!-- One paragraph. What's different after this PR lands than before. Quote
     specific files and line ranges where useful (path:line). -->

## Why

<!-- What concrete situation drove this change. A reproducible scenario, not
     a hypothetical. If this is a doctrine change (anything in `core/`),
     name the situation that the current rule fails to handle. -->

## Acceptance Criteria

<!-- Yes/no probes. Each line is one tool-verifiable thing. Mark [x] when the
     evidence is captured in the section below. -->

- [ ] ISC-1: <criterion text — what tool returns yes/no on this>
- [ ] ISC-2: …
- [ ] ISC-N: Anti: <what must NOT happen for this to count as done>

## Verification Evidence

<!-- For each ISC marked [x], paste the actual tool output / command result /
     screenshot path / SELECT result that proves it. "Looks fine" is not
     evidence (see core/verification-doctrine.md). -->

- ISC-1: <tool used — quoted evidence>
- ISC-2: …

## Doctrine Impact

<!-- Check the boxes that apply. If any are checked, the PR needs a second
     reviewer (see CONTRIBUTING.md "Review Cadence"). -->

- [ ] Edits `core/` (constitution, algorithm, ISC, verification doctrine, …)
- [ ] Edits `memory/effectus/` (mission, goals, beliefs, …)
- [ ] Edits a skill `SKILL.md` body (workflows, gotchas, NOT FOR list)
- [ ] Changes pre-commit hook or CI workflow
- [ ] Adds a `NEVER` rule
- [ ] None of the above

## Security Impact

<!-- Per SECURITY.md, security-sensitive changes route through a private
     disclosure channel rather than a public PR. If this PR is the public
     fix for a private disclosure, link the advisory ID below. -->

- [ ] No security impact
- [ ] Security-relevant change, public-fix PR for advisory: <ID>
- [ ] Security-relevant change, no prior advisory (please re-open privately)

## Repo Source

<!-- For maintainers tracking which integration path this PR was tested on.
     Both paths are first-class. -->

- [ ] Verified locally with `git` only (no remote)
- [ ] Tested against GitHub (Actions ran green)
- [ ] Tested against Azure DevOps Repos (Pipelines ran green)

## Linked Issues / Advisories

<!-- "Closes #123", "Refs DAI-456", "Advisory GHSA-…", etc. -->
