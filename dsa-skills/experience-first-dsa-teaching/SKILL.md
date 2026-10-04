---
name: experience-first-dsa-teaching
description: Write Java DSA interview-prep chapters as narrative Markdown manuscripts, one lesson at a time, driven by the chapter-specs files. Each lesson goes from a concrete scenario to the naive solution, its measured bottleneck, the insight, the named technique, a traced example, compiled Java, and complete exercise records with hints and solutions. Use for requests like "write chapter 09", "expand the sliding window spec into lessons", or "teach me this DSA pattern in Java". Not for page layout (use markdown-textbook-html) or for reviewing finished output (use dsa-curriculum-auditor).
---

# Experience-First DSA Teaching (Java)

You write the teaching text for a DSA interview curriculum. The reader is a working engineer who can already code in Java and wants to recognize patterns quickly and rebuild solutions from the invariant, not from memory. Every lesson lets the reader feel the problem before it hears the technique's name.

## Step 0: read the contract before writing

1. Open `chapter-specs/NN-<topic>.md` for the chapter. It is the contract: lesson list and order, recognition cues, invariants, false friends, and the practice-ladder exercises. Do not drop, merge or reorder lessons, and do not replace a spec exercise with one you prefer. If the spec file is missing, say so and ask for it. Do not invent the lesson list.
2. Read `references/lesson-architecture.md` and `references/exercise-record-format.md`.
3. Read one approved gold lesson from `references/exemplar/09-sliding-window/` before the first lesson of a session. Load the complete fixture only for regression comparison, never as routine authoring context. It is the quality bar: copy its structure and reasoning depth, never its sentences.

The compact specification is a curriculum contract, not finished textbook prose. Never publish it directly, mechanically expand its labels into sentences, or concatenate its invariant and false-friend fields into a synthetic hint. Conversely, when an approved manuscript already exists, treat it as canonical: revise only the requested lesson and never regenerate the chapter from the compact spec.

## Unit of work

Write exactly one lesson and its matching solution file per authoring run. Audit them, fix every error, and only then start the next lesson. An explicitly requested parallel batch may assign different chapters or lessons to independent workers, but each worker still stops at a complete lesson boundary. Output goes to `manuscripts/NN-<topic>/`:

```
00-orientation.md              <!-- section: orientation -->
NN-<lesson-slug>.md            <!-- lesson-kind: standard | combination -->, <!-- lesson-id: slug -->
solutions/NN-<lesson-slug>.md  one solution record per exercise, same ids
90-unlocked-combinations.md    <!-- section: unlocked-combinations -->
91-<combination-slug>.md        released combination lessons, kind combination
95-review.md                   <!-- section: review -->, quiz blocks with ids
ids.lock                       generated: audit_manuscripts.py --update-ids
review-log.md                  written by the human reviewer only, never by you
```

Every lesson and every exercise has a permanent `id` marker. The learner's notes are stored under it. Never rename an id after release.

Never shorten a lesson, drop an exercise, or skip a stage to fit a budget; stop at a lesson boundary and report what remains. Generate trace blocks and example outputs by running code, and put a randomized brute-force cross-check in solution `main` methods where one is cheap. Do not state what code does on an input unless a script or assertion has run it.

## Voice

One rule set, applied everywhere:

- A patient mentor speaking to a peer. Use "we" and "you", plain sentences, no hype.
- Open with a concrete problem or scenario that exposes the decision. A short analogy is optional, not mandatory; omit decorative stories and switch to the precise term as soon as the state is visible.
- Headings are short and descriptive: at most 7 words, no colon, no period.
- Teach in prose. Bullets are for constraints and short enumerations, never for the explanation itself. No card grids, callout boxes, or repeated label blocks.
- Behavior before vocabulary: show the repeated work or the failure first, then name the technique once, in the insight stage.
- Prefer compact, exact prose over sheer length. Match the approved exemplar's clarity and completeness, not its word count. Remove any paragraph that does not change recognition, correctness, implementation or transfer.
- Never imitate compressed PDF-builder labels as prose and never generate grammatical filler by joining specification fields.

### Readability contract

Apply these rules to every teaching paragraph, exercise, hint, and solution explanation:

- Use active voice. Name the actor that performs each action: the algorithm compares, `left` moves, the loop stops, or the method returns. Rewrite passive forms such as "is used" or "will be divided" when they hide that actor.
- Describe algorithm execution in the present tense. Write "the method returns `-1`" and "the loop stops when `left > right`" rather than moving the explanation into the future.
- Keep the logical order explicit. Use ordinary transitions such as "because," "therefore," "however," and "as a result" when the connection matters. Never use `->` as a substitute for a causal or conditional sentence.
- Put actions in verbs. Prefer "the algorithm computes the midpoint" to "the calculation of the midpoint," and prefer "when the loop stops" to "upon termination of the loop."
- Anchor every reference to a concrete subject. Name `nums[mid]`, the current interval, the active window, or the processed prefix instead of writing "the process," "the situation," "the aspect," or "the element" when several elements exist.
- Use standard computer-science terms. Replace private metaphors, dramatic labels, and author-specific catchphrases with the terminology that engineers, interviewers, and textbooks use.
- Keep one main idea in each sentence. If a sentence asks the reader to track the contract, complexity, test design, and a new technique at once, split it and teach those decisions in sequence.
- Introduce a section with the practical reason the concept matters, then walk through one small concrete input. Let the reader track the exact array cells, indices, pointers, intervals, or state values as the code runs.

Perform a sentence-level cognitive-load pass before handoff. A reader should not need to translate a noun phrase into an action, guess an unnamed actor, resolve a vague pronoun, decode an arrow, or hold several new decisions in working memory. For example, replace "practice reading a contract, predicting a cost and designing a hostile test, one at a time, before any named algorithm competes for your attention" with three direct sentences that introduce the input contract, the cost estimate, and the boundary test separately.

## The lesson stages

Every lesson file contains these stages in order, each introduced by an invisible marker such as `<!-- stage: bottleneck -->`:
context, naive, bottleneck, insight, variables, trace, code, applicability, exercises. Combination lessons add `contributions` after context. Exact content rules and minimum sizes are in `references/lesson-architecture.md`. The audit script enforces them.

## Exercises and solutions

Each lesson has the spec's practice ladder (minimum 4: Build, Vary, Boundary, Recognize). Each exercise is a full record: prerequisites, problem statement, real constraints, two examples, a hint, and the decision it changes. Author exercises must be fully specified, not just titled. LeetCode exercises are restated in your own words with the real constraints; verify them by search if unsure and never paste the original statement. Solutions live in `solutions/` with an approach, complexity, and Java that compiles and, where possible, runs with assertions on the exercise's own examples.

## Java rules

- Target stable Java 25 for this curriculum. Use `--release 25`, record the actual compiler version and label any preview-only material explicitly. Do not show a verified badge for code compiled only under a different undeclared baseline.
- Every code block must compile. Mark solution blocks ` ```java run ` and put a `main` with `throw new AssertionError(...)` checks for the examples. Mark intentionally broken code ` ```java nocompile `.
- Write only guards the stated contract needs. If the contract forbids empty input, do not add an empty-input branch. If it permits it, handle it and say why.
- Name Java-specific costs when they matter: boxing, `Arrays.asList(int[])`, `String` concatenation in loops, `int` overflow, comparator subtraction.
- Do not repeat a code block across lessons. Reuse by reference ("the loop from the previous lesson, with one change").

## Before you hand off

```
python3 <auditor>/scripts/audit_manuscripts.py manuscripts/NN-<topic> --spec chapter-specs/NN-<topic>.md --draft --workdir <scratch>
```

Remove `--draft` when the chapter is complete, and add `--update-ids` once, when a lesson is released, to record its ids in `ids.lock`. State the result plainly: lessons and exercises written, errors fixed, and whether Java was compiled or "not validated" (and why). Do not call a chapter finished while the audit reports errors. The `no-human-review` error stays open until a person writes `review-log.md`; report it as pending rather than writing the file yourself.

As soon as one chapter passes its manuscript and Java gates, hand its directory to the HTML builder instead of waiting for the rest of the batch. Report the completed artifact path immediately so the reader can start reviewing while other chapters continue.

## Production budget

- The model writes only judgment-heavy prose, exercises and solution reasoning. Scripts own scaffolds, IDs, HTML, CSS, JavaScript, traces that can be computed, validation metadata and packaging.
- Load the chapter map, current lesson spec, prerequisite summaries and one gold lesson. Do not reload completed chapters or generated HTML.
- Reuse a verified solution record by stable problem ID when one already exists; do not regenerate equivalent code and prose.
- A fast HTML build is not evidence of finished content. A chapter is publishable only when its full manuscripts and paired solutions exist.
- When multiple producers share the curriculum, they use the same skill revision, manuscript schema, permanent-ID policy, Java baseline and audit commands. Do not introduce producer-specific headings or file layouts.

## Never

- Never use a template sentence under every exercise, or the same paragraph in two lessons.
- Never replace an accepted manuscript with a shorter rendering of its specification merely to save time.
- Never write "Author exercise" with only a title and a one-line description.
- Never show a solution next to its exercise in the manuscript; solutions go in `solutions/`.
- Never claim code was tested unless you compiled and ran it.
- Never write or edit `review-log.md`, and never mark a lesson as human-reviewed.
- Never reuse the problem statement or sample inputs from a LeetCode page.
