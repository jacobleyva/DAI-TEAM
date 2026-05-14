---
name: Install Report (CR-5 third-machine validation)
about: Report a fresh-clone install transcript — pass or fail. This is the most useful first contribution a new user can make.
title: "[Install Report] <pass|fail> on <OS> with <Codex|other> "
labels: install-report, triage
assignees: ''
---

<!--
DAI ROADMAP.md flags one validation criterion that the maintainers can't run
alone: a fresh `git clone` + `./bootstrap.sh` on a machine that has never seen
DAI before. Whether yours passes or fails, the transcript is useful — please
file this issue either way.
-->

## Outcome

- [ ] Pass — `./bootstrap.sh` completed, Codex (or other CLI) loaded the doctrine
- [ ] Partial — `./bootstrap.sh` completed but the Codex side failed
- [ ] Fail — `./bootstrap.sh` did not complete

## Environment

- **OS / version:** <e.g. Ubuntu 24.04, macOS 14.5, Windows 11 + WSL2 Ubuntu 22.04>
- **Architecture:** <x86_64 / arm64>
- **Shell:** <bash / zsh / fish / dash>
- **Python version:** <output of `python3 --version`>
- **Git version:** <output of `git --version`>
- **AI coding assistant:** <Codex / Cursor / Aider / other> + version
- **Repo source platform (if relevant):** <GitHub / Azure DevOps Repos / GitLab / Bitbucket / local-only>

## Bootstrap Transcript

```
<paste the full output of ./bootstrap.sh here — even on success>
```

## First-Prompt Verification

After bootstrap, the recommended first prompt is:

> What's in memory/session-context.md? Summarize what this workspace is and what rules I'm operating under.

**What the assistant said:**

```
<paste the assistant's response>
```

**Did it correctly describe constitution + Algorithm + ISC + verification doctrine + tiering?**

- [ ] Yes — full description, all five doctrine pillars named
- [ ] Partial — some pillars described, others missed
- [ ] No — the assistant didn't see the file, or saw the wrong content

## What Went Wrong (if anything)

<!-- For partial / fail outcomes only. Quote the actual error message and the
     step where it appeared. If you patched something locally to get past it,
     show the patch. -->

## Anything Else

<!-- Things you noticed that aren't a pass/fail signal — surprising flows,
     unclear documentation, missing prerequisites the script didn't catch. -->
