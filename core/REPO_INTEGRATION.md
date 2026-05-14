---
title: Repo Source Integration — GitHub and Azure DevOps Repos
type: reference
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
version: v1.0
tags:
  - repo-source
  - github
  - azure-devops
  - ci
  - integration
artifact_type: integration-guide
---

# Repo Source Integration

> DAI is repo-source-neutral. The doctrine, the pre-commit hook, the skills, the bootstrap flow — none of them assume GitHub. The CI side does need configuration, and most enterprise teams running this will use either **GitHub** or **Azure DevOps Repos + Azure Pipelines**. Both paths are first-class. This file shows the side-by-side enablement steps so a team can plug DAI into whichever stack they already run.

## What DAI Ships Pre-wired

The following are already in the repository and work identically on either platform:

| Artifact | Path | What it does |
|----------|------|--------------|
| Pre-commit hook | `.githooks/pre-commit` | Frontmatter validation + secret-pattern scan on every local commit |
| Secret-scan diff helper | `tools/scripts/secret_scan_diff.sh` | Same regex set, applied to a diff between two refs (used by CI) |
| Frontmatter validator | `tools/scripts/check_front_matter.py` | Strict frontmatter shape check, callable from CI |
| Template eval | `tools/scripts/eval_templates.py` | Verifies every template has real content, not stubs |
| Repo-health check | `tools/scripts/check_repo_health.py` | Inventory + drift detection across `core/`, `memory/`, `skills/`, `templates/` |
| Skills index regen | `tools/scripts/skills_index.sh` | Rebuilds `memory/skills-catalog.md` from the actual skills tree |
| Session context regen | `tools/scripts/build_session_context.sh` | Rebuilds `memory/session-context.md` from doctrine + identity + focus |
| GitHub Actions workflow | `.github/workflows/dai-checks.yml` | Runs all of the above on every PR and every push to main |
| Azure Pipelines workflow | `azure-pipelines.yml` | Mirror of the above for Azure DevOps Pipelines |
| GitHub PR template | `.github/PULL_REQUEST_TEMPLATE.md` | The PR shape contributors fill in |
| Azure PR template | `.azuredevops/pull_request_template.md` | The same shape, served at the Azure-expected path |
| GitHub issue templates | `.github/ISSUE_TEMPLATE/*.md` | Install-report + doctrine-change shapes |
| GitHub CODEOWNERS | `.github/CODEOWNERS` | Review-routing for protected paths |

## Side-by-Side: Enabling the CI Checks

The CI checks are identical in intent. The platform differs in how the pipeline is registered and where reviewers are enforced.

| Step | GitHub | Azure DevOps Repos + Pipelines |
|------|--------|---------------------------------|
| 1. Pipeline definition | `.github/workflows/dai-checks.yml` (auto-discovered) | `azure-pipelines.yml` at repo root |
| 2. Register the pipeline | Nothing to do — GitHub Actions reads the workflow file on first push | Pipelines → New pipeline → Azure Repos Git → select repo → "Existing Azure Pipelines YAML file" → `/azure-pipelines.yml` |
| 3. Trigger on PRs | Already declared in the workflow's `on.pull_request` block | Already declared in `pr.branches.include` |
| 4. Enforce as required check | Repo Settings → Branches → Branch protection rule for `main` → "Require status checks to pass" → select "Discipline checks" | Repos → Branches → main → Branch policies → "Build validation" → add the pipeline |
| 5. Review enforcement | Repo Settings → Branches → "Require pull request before merging" → "Require approvals" + "Require review from Code Owners" | Repos → Branches → main → Branch policies → "Require a minimum number of reviewers" + "Automatically include code reviewers" (configured per-path under Project Settings → Repositories → Security) |
| 6. PR template | `.github/PULL_REQUEST_TEMPLATE.md` auto-loaded | `.azuredevops/pull_request_template.md` auto-loaded; if your project uses a different convention, set it under Repos → Settings → Pull request templates |
| 7. Code-owners equivalent | `.github/CODEOWNERS` (auto-loaded) | Project Settings → Repositories → security per-path; or Project Settings → Cross-repo policies → "Automatically include reviewers" for org-wide rules |
| 8. Security disclosure | Repo Settings → Security → Private vulnerability reporting → Enable; published via Security Advisories | Project Settings → Boards → Process → add a private "Security Vulnerability" work item type; restrict view permissions per team |

## Step-by-Step — GitHub Path

1. Push the DAI repo (this repo) to a GitHub repository. The workflow at `.github/workflows/dai-checks.yml` activates automatically on first push to `main`.
2. Open Settings → Branches → Add branch protection rule. Match `main`. Enable:
   - "Require a pull request before merging"
   - "Require approvals" — set to 1 (or 2 for doctrine-protected paths via separate rule)
   - "Require review from Code Owners"
   - "Require status checks to pass before merging" → search for and select **DAI Checks / Discipline checks**
   - "Require branches to be up to date before merging"
3. Open Settings → Security → "Private vulnerability reporting" → Enable. This wires the SECURITY.md flow.
4. Open Settings → Actions → General → "Workflow permissions" → leave at read-only (the workflow only needs `contents: read`).
5. Verify by opening a throwaway PR that adds a markdown file without frontmatter. The check should fail. Delete the PR.

## Step-by-Step — Azure DevOps Repos + Pipelines Path

1. Push the DAI repo to an Azure DevOps Repos repository.
2. Pipelines → New pipeline → "Azure Repos Git" → select the repo → "Existing Azure Pipelines YAML file" → choose `/azure-pipelines.yml`. Save and run once to verify the pipeline turns green.
3. Repos → Branches → `main` → "..." menu → Branch policies:
   - "Require a minimum number of reviewers" → set to 1; check "Reset code reviewer votes when there are new changes"
   - "Check for linked work items" → optional but recommended
   - "Check for comment resolution" → required = true
   - "Build validation" → add → select the pipeline you just registered. Set the policy to **Required**, trigger = **Automatic**.
   - "Automatically include code reviewers" → add a path filter like `/core/*` → required reviewer = `@<doctrine-owner-group>`. Repeat for `/skills/security-*/`, `/SECURITY.md`, `/memory/security/`.
4. Project Settings → Boards → Process → "Customize" → add a work item type named **Security Vulnerability** with restricted visibility (Project Settings → Security → set "View work items in this node" to specific group for that type). This serves the private-disclosure channel.
5. Verify by opening a throwaway PR that adds a markdown file without frontmatter. The build validation should fail. Discard the PR.

## CODEOWNERS-equivalent on Azure DevOps

Azure DevOps Repos does not have a `CODEOWNERS` file. The same enforcement happens via **branch policies + automatic reviewers** configured per-path. Translate `.github/CODEOWNERS` like this:

| `.github/CODEOWNERS` entry | Azure DevOps equivalent |
|---------------------------|-------------------------|
| `/core/                  @jacobleyva` | Branch policy on `main` → "Automatically include reviewers" → path: `/core/*` → required reviewer: doctrine-owner group |
| `/skills/security-*/     @jacobleyva` | Same, path: `/skills/security-*/*` → required reviewer: security-domain group |
| `/SECURITY.md            @jacobleyva` | Same, path: `/SECURITY.md` → required reviewer: security-domain group |
| `/memory/effectus/          @jacobleyva` | Same, path: `/memory/effectus/*` → required reviewer: doctrine-owner group |

The result is the same: protected paths cannot merge without the named reviewer's approval.

## Security Disclosure — Both Platforms

`SECURITY.md` names the preferred channel as the platform's private disclosure flow. Both paths give you an audit trail, restricted visibility, and a place to coordinate the fix without leaking the vuln.

- **GitHub:** Repository → Security → Advisories → "Report a vulnerability". Free, native, audit-trailed.
- **Azure DevOps:** A private "Security Vulnerability" work item type in the project's process template, with view permissions restricted to the security-domain group. Combine with email to the maintainer for the initial heads-up.

If your team uses a different repo-source platform (GitLab, Bitbucket, on-prem Gitea), the pattern transfers: a private issue-tracker channel + a CI pipeline that runs `tools/scripts/check_front_matter.py`, `tools/scripts/eval_templates.py`, and `tools/scripts/secret_scan_diff.sh`. Open a PR with the platform's pipeline file and we'll merge it.

## Keeping the Two Pipelines in Lockstep

`.github/workflows/dai-checks.yml` and `azure-pipelines.yml` call the same `tools/scripts/*` invocations. If you add a new check, add it to **both** files in the same PR. The CONTRIBUTING.md "Changes pre-commit hook or CI workflow" checkbox exists to remind you.

If a check works on one platform but not the other, that's a platform issue worth filing as an issue — DAI's intent is that the discipline floor is identical regardless of where the repo lives.

## Verification

After enabling either path, the green-light state is:

- A trivial PR (one-line docs change with proper frontmatter) merges in under five minutes once the checks run
- A bad PR (missing frontmatter, embedded secret, template stub) is blocked by the pipeline, not by manual reviewer attention
- A doctrine PR (touches `core/`) cannot merge without the named owner's approval
- A security PR opened publicly gets redirected to the private channel by the issue template

If any of those four behaviors aren't true, the wiring is incomplete — re-check the steps above.
