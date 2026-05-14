<!--
DAI Pull Request Template — Azure DevOps Repos

Azure DevOps Repos honors this template when placed at .azuredevops/pull_request_template.md.
If your team uses Azure DevOps but with a different default location, adjust per the
project's "Repos → Settings → Pull request templates" configuration.

This template mirrors .github/PULL_REQUEST_TEMPLATE.md. The two stay in lockstep so a
contributor moving between stacks sees the same shape.
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

<!-- Check the boxes that apply. If any are checked, this PR needs a second
     reviewer (see CONTRIBUTING.md "Review Cadence"). Azure DevOps Repos
     enforces required reviewers via branch policy — see core/REPO_INTEGRATION.md
     for the policy setup. -->

- [ ] Edits `core/` (constitution, algorithm, ISC, verification doctrine, …)
- [ ] Edits `memory/effectus/` (mission, goals, beliefs, …)
- [ ] Edits a skill `SKILL.md` body (workflows, gotchas, NOT FOR list)
- [ ] Changes pre-commit hook or CI workflow
- [ ] Adds a `NEVER` rule
- [ ] None of the above

## Security Impact

<!-- Per SECURITY.md, security-sensitive changes route through a private
     disclosure channel rather than a public PR. If this PR is the public
     fix for a private disclosure, link the advisory work-item ID below. -->

- [ ] No security impact
- [ ] Security-relevant change, public-fix PR for advisory: <work-item ID>
- [ ] Security-relevant change, no prior advisory (please re-open privately)

## Repo Source

<!-- For maintainers tracking which integration path this PR was tested on.
     Both paths are first-class. -->

- [ ] Verified locally with `git` only (no remote)
- [ ] Tested against Azure DevOps Repos (Pipelines ran green)
- [ ] Tested against GitHub (Actions ran green)

## Linked Work Items

<!-- "Closes #123", "Refs AB#456", advisory work item IDs, etc. Use the
     Azure DevOps convention #N or AB#N for cross-project links. -->
