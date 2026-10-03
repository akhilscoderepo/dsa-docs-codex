---
name: dsa-chapter-pipeline
description: Resume and publish exactly one chapter of Akhil's spec-driven Java DSA curriculum using its progress ledger, canonical manuscripts, paired solutions, deterministic audits, and checkpoint protocol. Use for scheduled or manual continuation of chapters 05-41; not for isolated DSA explanations.
---

# DSA chapter pipeline

Treat `RUNBOOK.md` as the operational authority and `PROGRESS.md` as the recovery state. Complete exactly one chapter per scheduled run. A manually supervised run may stop earlier, but only at a complete lesson boundary.

## Required skills

Read these repository skills before acting:

1. `dsa-skills/experience-first-dsa-teaching/SKILL.md` for manuscript and solution authoring.
2. `dsa-skills/dsa-curriculum-auditor/SKILL.md` for evidence and status language.
3. `dsa-skills/markdown-textbook-html/SKILL.md` only when the chapter is ready to build.

Read their directly required authoring references. For voice and depth, read only this gold pair unless the runbook explicitly replaces it:

- `dsa-skills/experience-first-dsa-teaching/references/exemplar/09-sliding-window/05-at-most-k-distinct-windows.md`
- `dsa-skills/experience-first-dsa-teaching/references/exemplar/09-sliding-window/solutions/05-at-most-k-distinct-windows.md`

Do not load completed chapters as a substitute for the gold pair.

## Resume rule

Resume the active claim in `PROGRESS.md`. Verify that every listed completed lesson has a manuscript, paired solutions, stable IDs, and a passing draft audit. Start at `next_lesson`; never regenerate a completed lesson unless an audit identifies a concrete defect.

If there is no active claim, claim the lowest unfinished chapter. Write the claim before authoring. Never work on two chapters in one scheduled run.

## Quality boundary

The compact specification is a contract, not prose. Every lesson must satisfy the authoring skill's complete stage architecture and carry the specification's exact Build, Vary, Boundary, Recognize ladder. Every solution includes executable assertions for both examples and a deterministic randomized comparison with a brute-force oracle whenever practical.

Use plain technical English. Vary sentence structure naturally. Do not reuse exercise boilerplate, splice specification labels into hints, or decorate a lesson with a story that contributes nothing to the algorithmic decision.

## Persistence

After each passing lesson audit, update `PROGRESS.md`. At the end of a run, follow the runbook's checkpoint procedure and push. A checkpoint represents a durable lesson boundary, not completion. Report exactly what passed and what remains.

Never create `review-log.md`. Until Akhil reviews the chapter, the strongest allowed status is `content complete, human review pending`.

