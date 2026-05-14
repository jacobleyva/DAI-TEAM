---
name: cis-controls
description: Use when a user wants to align a configuration, design, integration, implementation plan, or operational workflow to the CIS Controls v8.1, or asks which CIS controls apply to a proposed change.
---

# CIS Controls

Use this skill when the task is to map future work to CIS Controls rather than only describing a technical change.

## Core model

Treat CIS alignment as a mapping exercise first, not a compliance claim.

- identify the configuration or design surface being changed
- map that surface to the smallest relevant set of CIS controls
- separate source-backed control intent from local implementation inference
- state what evidence would be needed for a stronger compliance claim

## Preferred workflow

1. Start with [CIS Controls Overview Topic](../../knowledge/collections/cis-controls-v8-1/documents/cis-controls-overview-topic.md).
2. Open the most relevant raw control chunks under [cis-controls-v8-1](../../knowledge/collections/cis-controls-v8-1/cis-controls-v8-1-collection.md).
3. For configuration-heavy work, check Controls `4`, `5`, `6`, `7`, `8`, `9`, `10`, `12`, `13`, and `16` first.
4. For data-handling work, also check Controls `1`, `2`, `3`, `11`, `15`, and `17`.
5. For internet-facing or major architecture changes, consider whether Control `18` should be part of the validation plan.

## Output shape

When the user asks for CIS alignment, prefer this structure:

- relevant controls
- why they apply
- configuration decisions that support the controls
- gaps or evidence still needed

## Guardrails

- do not say a system is "CIS compliant" unless evidence exists for the specific safeguards
- do not over-map every change to all 18 controls
- call out when a mapping is an inference from control scope rather than an explicit safeguard citation
- prefer practical configuration guidance over generic compliance language

