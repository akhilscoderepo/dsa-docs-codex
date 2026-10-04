# Curriculum progress

The machine-readable lines below are the recovery ledger. Update them only at a completed lesson boundary.

## Chapter state

| Chapter | Topic | Status | Completed lessons | Next lesson |
| --- | --- | --- | --- | --- |
| 00 | Problem contracts, complexity, and sequence language | content_complete_human_review_pending | 8/8 | human review |
| 01 | Arrays core operations | content_complete_human_review_pending | 12/12 | human review |
| 02 | Matrices and 2D arrays | content_complete_human_review_pending | 7/7 | human review |
| 03 | Strings | content_complete_human_review_pending | 7/7 | human review |
| 04 | Hash maps and sets | content_complete_human_review_pending | 9/9 | human review |
| 05 | Sorting and Java comparators | content_complete_human_review_pending | 9/9 | human review |
| 06 | Binary search | in_progress | 4/11 | Peak Search |
| 07 | Prefix sums and difference arrays | in_progress | 7/11 | Difference Arrays |
| 08 | Two pointers | in_progress | 9/10 | Index State And Floyd |
| 09 | Sliding window | content_complete_human_review_pending | 10/10 | human review |
| 10 | Intervals | in_progress | 1/7 | Touching-Boundary Semantics |
| 11-41 | Remaining specifications | not_started | 0 | chapter 11 after active drafts |

## Active claim

- chapter: `05-sorting-and-java-comparators`
- owner: `codex-local-scheduled-pipeline`
- started: `2026-10-03T20:00:00+05:30`
- updated: `2026-10-04T09:34:24.0511369+05:30`
- completed_lessons: `[01-ordering-contracts, 02-arrays-sort, 03-comparator-contracts, 04-object-ordering, 05-stability-and-ties, 06-sort-and-sweep, 07-sort-and-deduplicate, 08-sort-then-scan, 09-strings-maps-and-sorting]`
- next_lesson: `release-build`
- push_status: `pushed at be4fd65`

## Decision log

- Chapters 00-04 use the full accepted Markdown manuscripts and shared renderer, not the earlier compact HTML source.
- Scheduled work processes one chapter per run and checkpoints only at complete lesson boundaries.
- Chapter 05 contains eight independent lessons plus one released combination lesson: Strings, Maps, and Sorting.
- Human review is never inferred from an automated audit.
- Chapter 05 lesson 01 passed the draft audit on JDK 25 with four compiled-and-run solution blocks. Remaining warnings identify the eight future lessons, the two chapter wrap-up sections, and human review.
- Chapter 05 lesson 02 passed the draft audit on JDK 25. The chapter now has eight exercise solutions compiled and run; remaining warnings name only future lessons, wrap-up sections, and human review.
- Chapter 05 lesson 03 passed the draft audit on JDK 25. Twelve exercises now have paired compiled-and-run solutions; the remaining nine warnings identify six future lessons, two wrap-up sections, and human review.
- Chapter 05 lesson 04 passed the draft audit on JDK 25. Sixteen exercises now have paired compiled-and-run solutions; the remaining eight warnings identify five future lessons, two wrap-up sections, and human review.
- Chapter 05 lesson 05 passed the draft audit on JDK 25. Twenty exercises now have paired compiled-and-run solutions; the remaining seven warnings identify four future lessons, two wrap-up sections, and human review.
- Chapter 05 lesson 06 passed the draft audit on JDK 25. Twenty-four exercises now have paired compiled-and-run solutions; the remaining six warnings identify three future lessons, two wrap-up sections, and human review. Queue Reconstruction is revisited from the partial-queue sweep invariant required by the source specification.
- Chapter 05 lesson 07 passed the draft audit on JDK 25. Twenty-eight exercises now have paired compiled-and-run solutions; the remaining five warnings identify two future lessons, two wrap-up sections, and human review.
- Chapter 05 lesson 08 passed the draft audit on JDK 25. Thirty-two exercises now have paired compiled-and-run solutions; the remaining four warnings identify the final combination lesson, two wrap-up sections, and human review.
- Chapter 05 lesson 09 and both wrap-up sections passed the manuscript and Java checks on JDK 25. The chapter has 36 paired solutions. The only non-draft manuscript error is the human-owned review log. HTML was generated, but smoke and Chromium render checks remain unverified because jsdom and playwright-core are not installed; publication is still pending.


- Automation run on 2026-10-04 resumed the recorded lesson-08 boundary and preserved the pre-existing lesson-09 drafts. During repair, another process advanced HEAD from 9453aa1 to 4864436 and committed the live manuscript before its paired repair was complete. No earlier completed lesson was regenerated. Work stopped after the latest lesson-09 draft audit passed; next_lesson remains release-build.
- The current chapter draft audit ran on Oracle JDK 25.0.1 with --release 25: 9 lessons, 36 exercises, 0 errors, 1 warning (no-human-review, left open for Akhil). Of 54 Java blocks, 48 compiled and 43 ran with assertions; 6 intentionally marked nocompile blocks were skipped. Lesson 09 now has independent randomized solution comparisons, own computed samples, and a trace generated from executable grouping code; the review ends with three rebuild tasks and a fresh composition problem.
- Publication blockers verified this run: Node module resolution reports MODULE_NOT_FOUND for both jsdom and playwright-core. Smoke and Chromium render gates did not run. The installed stamp/build/audit tools bind only a Java digest and lack the required manuscriptDigest; the non-draft wrapper also treats no-human-review as fatal rather than a separately open human gate. These infrastructure discrepancies remain unresolved because the concurrent checkpoint required stopping. The existing untracked HTML is not a validated publication.
- Remote verification failed: fatal: unable to access 'https://github.com/akhilscoderepo/dsa-docs-codex.git/': Failed to connect to github.com port 443 via 127.0.0.1 after 2063 ms: Could not connect to server. The subsequent authorized push outside the restricted network succeeded: checkpoint be4fd65 reached origin/main.
- User explicitly requested a parallel Chapters 06-10 batch. Chapter 06 reached 2/11 lessons with 8 solutions and zero draft-audit errors; next is Lower And Upper Bounds.
- Chapter 07 reached 4/11 lessons with 16 solutions and zero draft-audit errors; next is Earliest Balance. One advisory role warning reflects LC 238 appearing twice in the specification.
- Chapter 08 reached 5/10 lessons with 20 solutions and zero draft-audit errors; next is K-Sum Reduction.
- The complete approved Chapter 09 exemplar was promoted to the canonical manuscript directory: 10 lessons, 45 solutions, zero draft-audit errors, and Java validated on JDK 25. Low-diversity and template-phrase warnings remain for human review.
- Chapter 10 reached 1/7 lessons with 4 solutions and zero draft-audit errors; next is Touching-Boundary Semantics.
- Parallel continuation advanced Chapter 07 through Remainder Classes: 6/11 lessons, 24 paired solutions, zero draft-audit errors; next is Prefix XOR.
- Parallel continuation advanced Chapter 08 through Array Cycle State and the Sorting And Two Pointers combination: 8/10 lessons, 32 paired solutions, zero draft-audit errors; next is Strings And Two Pointers.
- The user authorized continuous rolling batches: finish the active five chapters, immediately claim the next five unfinished chapters, and continue through Chapter 41 without waiting for another prompt. Parallel workers own separate chapter directories; only the coordinator edits shared state and Git.
- Chapter 06 Lower And Upper Bounds passed the JDK 25 draft audit: 3/11 lessons, 12 paired solutions, zero errors; next is First True.
- Chapter 07 Prefix XOR passed the JDK 25 draft audit: 7/11 lessons, 28 paired solutions, zero errors; next is Difference Arrays. The pre-existing Lesson 03 role advisory remains open for chapter completion.
- Chapters 05 and 09 passed source-bound HTML audits with jsdom smoke tests and real Chrome desktop/phone render checks. Both are content complete with only the human-owned review gate open.
- The recovery ledger correction for Chapter 07 points to Difference Arrays: Earliest Balance was already released as lesson 05 in commit 14c860c.
- Chapter 08 Strings And Two Pointers passed the JDK 25 draft audit: 9/10 lessons, 36 paired solutions, zero errors; next is Index State And Floyd.
- Chapter 06 First True passed the JDK 25 draft audit: 4/11 lessons, 16 paired solutions, zero errors; next is Peak Search.

