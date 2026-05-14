---
title: Front Matter Standard
type: rule
domain: dai
product: DAI
audience: team
owner: team
status: active
updated: 2026-05-14
tags:
  - front-matter
  - yaml
  - metadata
artifact_type: operating-rule
---

# Front Matter Standard

## Standard Schema — durable shared files

Use this schema for durable shared markdown files in `core/`, `memory/`, `projects/`, `team/`, `knowledge/`, and `templates/`. Every required field present; values populated:

```yaml
title:
type:
domain:
product:
audience:
owner:
status:
updated:
tags:
artifact_type:
```

Add only a few optional fields when needed:

```yaml
related_projects:
source:
source_type:
```

## Skills Schema — vendor-portable minimal

Skills (`skills/<name>/SKILL.md`) use the Anthropic-style minimal frontmatter so a SKILL.md drops into Codex, Claude Code, or any other coding-assistant CLI without modification:

```yaml
---
name: <skill-name>
description: "One sentence — what this skill does, when to invoke, NOT FOR list."
---
```

The two schemas are intentionally different. The standard schema is for files DAI's tooling and humans both read and route by metadata. The skills schema is for files an external coding-assistant CLI consumes and dispatches by `name` and `description`. The pre-commit hook verifies both shapes open with `---` but doesn't enforce field completeness — `tools/scripts/check_front_matter.py` is the manual auditor for richer compliance checks.
