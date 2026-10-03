# DSA chapter pipeline runbook

This repository publishes one interactive Java DSA chapter at a time. The Markdown manuscripts are canonical. Generated HTML is never edited by hand.

## Start of every run

1. Read this file, `skill/dsa-chapter-pipeline/SKILL.md`, and `PROGRESS.md`.
2. Read only the current chapter specification, its chapter map if present, and the gold exemplar named by the pipeline skill.
3. Check `git status --short`. Preserve unrelated changes. Do not start a second chapter while one is marked `in_progress`.
4. Resume the lesson named under the active chapter. If no chapter is active, claim the lowest chapter numbered 05 through 41 whose status is `not_started`.

## Canonical paths

- Specifications: `dsa-skills/chapter-specs/NN-topic.md`
- Manuscripts: `dsa-skills/manuscripts/NN-topic/`
- Validation stamps: `dsa-skills/validation/NN-topic.json`
- Published chapter: `output/NN-topic.html`
- Shared authoring, HTML, and audit skills: `dsa-skills/`

`review-log.md` belongs to Akhil. An automated run must never create or edit it.

## Lesson transaction

Complete one lesson and its paired solution before touching the next lesson.

1. Write `NN-lesson.md` and `solutions/NN-lesson.md`.
2. Generate trace JSON from executable code when a trace is algorithmic. Do not invent trace state by hand.
3. Run the draft audit:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/audit.ps1 -Chapter NN -Draft -UpdateIds
```

4. Fix every error. Investigate every warning; fix it or record a short disposition in `PROGRESS.md`.
5. Update the chapter's `completed_lessons`, `next_lesson`, and timestamp in `PROGRESS.md`.

The draft audit may warn that future lessons, wrap-up sections, and human review are missing. Java blocks already present must compile and run on JDK 25.

## Chapter completion

After the orientation, every specified lesson, unlocked-combinations section, paired solutions, and review are present:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/audit.ps1 -Chapter NN -UpdateIds
powershell -ExecutionPolicy Bypass -File scripts/build.ps1 -Chapter NN
```

The build wrapper runs the manuscript audit with `--release 25`, writes the validation stamp, builds self-contained HTML, runs the HTML audit and smoke test, and runs the installed Chromium render check at desktop and 390-pixel phone viewports. A skipped gate is not a pass.

The required automated result is zero errors. `no-human-review` remains open and is reported separately. A 390-pixel emulator is not a physical-device test, and a print stylesheet is not a human print review.

When the deterministic gates pass, set the chapter status exactly to `content_complete_human_review_pending`.

## Checkpoints and Git

The active run may commit a checkpoint at a complete lesson boundary. It must never commit half a lesson or mark a partial chapter complete.

Checkpoint commit subject:

```text
checkpoint(chapter-NN): complete through lesson-name
```

Completed chapter commit subject:

```text
chapter(NN): publish title
```

Before committing, inspect the staged paths. A checkpoint may contain repository infrastructure, the active chapter manuscripts and solutions, its `ids.lock`, generated trace helpers owned by that chapter, and `PROGRESS.md`. A publication commit may additionally contain its validation stamp and HTML. Do not stage `tmp/`, legacy PDFs, or unrelated generated files.

Push every checkpoint or completed chapter to `origin/main`. Confirm the push succeeded. If authentication or network access fails, keep the local commit, record `push_pending` in `PROGRESS.md`, and report the exact error.

## Recovery

An active chapter record contains `owner`, `started`, `updated`, `completed_lessons`, and `next_lesson`. Resume it when its files and Git history agree. If they disagree, stop and report the mismatch instead of regenerating accepted work. Only recover a stale claim when its last update is older than six hours and no process or newer commit owns it; record the recovery in the decision log.

## Final corpus

When chapters 05 through 41 are content-complete, run every chapter audit and rebuild the index:

```powershell
& $env:PYTHON dsa-skills/markdown-textbook-html/scripts/build_index.py dsa-skills/manuscripts output --title "Java DSA Curriculum"
```

Commit and push the index only after all deterministic chapter checks pass. Report the corpus as `content complete, human review pending` until Akhil supplies every review log.

