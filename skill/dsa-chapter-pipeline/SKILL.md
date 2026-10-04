---
name: dsa-chapter-pipeline
description: Resume and publish rolling five-chapter batches of Akhil's spec-driven Java DSA curriculum using its progress ledger, canonical manuscripts, paired solutions, deterministic audits, and checkpoint protocol. Use for scheduled or manual continuation of chapters 05-41; not for isolated DSA explanations.
---

# DSA chapter pipeline

Treat `RUNBOOK.md` as the operational authority and `PROGRESS.md` as the recovery state. Work through the active batch of up to five consecutive chapters. When that batch finishes, claim the next five without waiting for the user. End a run only at complete lesson boundaries, with every unfinished chapter's next lesson recorded.

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

Resume every active batch claim in `PROGRESS.md`. Verify that every listed completed lesson has a manuscript, paired solutions, stable IDs, and a passing draft audit. Start each chapter at `next_lesson`; never regenerate a completed lesson unless an audit identifies a concrete defect.

If there is no active batch, claim the five lowest unfinished chapters, or all remaining chapters when fewer than five remain. Write the claims before authoring. Assign one worker per chapter when parallel workers are available; only the coordinator edits shared state or Git.

## Quality boundary

The compact specification is a contract, not prose. Every lesson must satisfy the authoring skill's complete stage architecture and carry the specification's exact Build, Vary, Boundary, Recognize ladder. Every solution includes executable assertions for both examples and a deterministic randomized comparison with a brute-force oracle whenever practical.

Use plain technical English. Vary sentence structure naturally. Do not reuse exercise boilerplate, splice specification labels into hints, or decorate a lesson with a story that contributes nothing to the algorithmic decision.

Apply the authoring skill's readability contract before accepting a lesson. The prose uses active subjects and present tense, expresses causal links in words rather than arrows, turns abstract noun phrases back into verbs, anchors references to exact variables or data regions, and uses standard computer-science terminology. Split any sentence that introduces several independent decisions at once; audit cognitive load as seriously as technical correctness.

## Persistence

After each passing lesson audit, the coordinator updates `PROGRESS.md`. At the end of a run, follow the runbook's checkpoint procedure and push every chapter boundary. A checkpoint represents a durable lesson boundary, not completion. Do not stop for user confirmation after a chapter or batch; continue with the next recorded work while execution time remains.

Never create `review-log.md`. Until Akhil reviews the chapter, the strongest allowed status is `content complete, human review pending`.

