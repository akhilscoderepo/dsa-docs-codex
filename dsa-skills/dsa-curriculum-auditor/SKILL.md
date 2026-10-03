---
name: dsa-curriculum-auditor
description: Audit a multi-chapter Java DSA interview curriculum for missing micro-patterns, thin or templated lessons, incomplete exercise records, missing solutions, uncompiled Java, specification-to-manuscript drift, and broken HTML builds. Runs deterministic scripts and reports verified facts separately from judgment. Use before declaring any chapter or the whole curriculum complete; not the primary writing skill.
---

# DSA Curriculum Auditor

Treat completion as an evidence claim. A chapter count, a passing structure check, or a successful build does not prove the chapter teaches anything. Earlier output of this project passed structural checks while every exercise was a one-line title and the same filler sentence appeared 1,280 times. These scripts exist to catch that.

Use `experience-first-dsa-teaching` for writing and `markdown-textbook-html` for building. This skill owns verification and the completion verdict.

## Audit sequence

### 1. Establish the canonical set

Read the curriculum map and `chapter-specs/` first. Canonical chapters are identified by numeric prefix. Compare spec, manuscript and HTML identifiers and report anything missing, duplicated or orphaned. Prototypes and legacy exports stay outside the count. If specs or manuscripts are not provided, say so; do not infer coverage from artifacts alone.

When multiple producers share the curriculum, record one canonical toolchain and manuscript-schema revision. Reject producer-specific layouts or IDs. A change that adds, removes or splits a lesson must update the chapter map and specification before the HTML becomes canonical; useful coverage discovered during authoring is not allowed to live only in one producer's manuscript.

### 2. Run the scripts (these produce the evidence)

```
# One-time setup from the toolchain root: pinned Python and Node dependencies
pip install -r requirements.txt && npm ci

# Manuscripts: structure, substance, spec parity, ids, duplicates, filler, human-review gate, Java compile and run
python3 scripts/audit_manuscripts.py manuscripts/09-sliding-window --spec chapter-specs/09-sliding-window.md \
        [--draft] [--release 25] [--workdir SCRATCH] [--stamp stamp.json] [--update-ids]

# Java only, any set of Markdown files
python3 scripts/compile_java.py manuscripts/09-sliding-window --stamp stamp.json

# Built HTML: self-contained, one notes box per exercise, valid trace/quiz data, JS syntax, parity with Markdown, footer matches the stamp
python3 scripts/audit_html.py output/09-sliding-window.html --manuscripts manuscripts/09-sliding-window --smoke

# Real browser (Chromium): desktop and phone layout, no horizontal scroll, tap targets, persistence across reload, screenshots
node scripts/render_check.mjs output/09-sliding-window.html shots/
```

`--draft` downgrades missing lessons, sections and the human-review gate to warnings for a chapter in progress. Drop it for a completion claim. `--stamp` writes a JSON record of the JDK actually used, which `build_html.py --validation` turns into the footer and the verified badges, so the page can only claim what was run. `--update-ids` records released lesson and exercise ids in `ids.lock`; afterwards a removed or renamed id is an `id-removed` error. Scratch files go to `--workdir`, then `$DSA_WORKDIR`, then the system temp directory. `--smoke` runs the jsdom interaction test, and `render_check.mjs` needs Chromium (set `CHROMIUM_PATH` or `PLAYWRIGHT_BROWSERS_PATH`); it exits with `SKIPPED` and code 2 when no browser is found, which is not a pass.

Each script exits nonzero on errors. Quote the counts it prints. Never describe a gate as passed unless a script or a direct inspection you performed showed it.

### 3. Report Java validation honestly

The compile check needs a JDK (the compiler, not just a JRE). The canonical baseline is stable JDK 25 with `--release 25`. If none is found the script prints `NOT VALIDATED`. Report that status as is, list which JDK version did compile, and do not treat an older-JDK preview build as the canonical validation. Do not mark unvalidated code as verified.

### 3b. The human-review gate

Scripts cannot judge whether a lesson teaches. A chapter is not Complete until `review-log.md` in the manuscript directory carries `Reviewed-by:` and `Date:` lines and a `- lesson-id: pass` line for every lesson. Only a person writes that file. Never create it, never mark a verdict on the reader's behalf, and report `no-human-review` as the open item. A `revise` verdict is an error until fixed.

### 4. Judge what scripts cannot

Read at least two full lessons per chapter and check against `references/acceptance-gates.md`:

- Does the bottleneck stage show waste you can see, or only assert a Big-O bound?
- Is the insight stage a real explanation, with the property that makes the move safe?
- Is the trace accurate, and does it include the hardest step?
- Do hints guide without revealing the answer, and do examples exercise a real boundary?
- Do any exercises require an untaught technique?
- Are Java costs and hazards named where they matter (boxing, overflow, comparators, `Arrays.asList(int[])`)?
- Does the prose read like a coherent technical lesson rather than specification fields placed under headings?
- Are scenarios doing explanatory work, or are they decorative padding that delays the technical model?
- Did any generated hint splice together invariant and false-friend text into awkward or ungrammatical prose?

### 5. Verify coverage

For every micro-pattern in the spec, require a distinct recognition cue, invariant, nearest false friend, owner chapter, and a full practice ladder. Do not accept a macro heading as evidence its internal families are covered. Unlocked combinations are full lessons; deferred ones name the missing prerequisite and future owner and have no exercises yet.

Also reconcile exact exercise roles. `Build`, `Vary`, `Boundary` and `Recognize` in the manuscript must match the owning specification; a complete solution does not excuse a role mismatch. Report low-diversity traces, repeated template phrases and duplicated paragraphs for human review rather than dismissing them because structure passes.

### 6. Close the track

Do not say the curriculum is complete until every script reports zero errors without `--draft`, the human review log is in place, Java is validated or its status is stated, the render check passes on a real browser, and the reader package (HTML files, a reading-order index, and a manifest) contains only canonical files.

The validation stamp and HTML must contain matching `javaDigest` and `manuscriptDigest` values. Recompute the artifact hash in the package manifest. A Java-only digest is insufficient because prose, exercises or solutions can change without altering code.

For a production batch, release chapters independently. Once one chapter passes, report its artifact path immediately and continue auditing the remaining chapters. A batch summary never replaces per-chapter status.

Before dividing work between producers, verify that both sides use the same skill revision, gold exemplar, chapter assignments, Java baseline, IDs, assets and audit scripts. Sample at least one lesson from each producer side by side; the reader should not be able to identify the producer from structure or voice.

## Reporting

Lead with one of:

- `Complete`: every gate passed with evidence, including a human review log.
- `Content complete, review pending`: every script check passes and only the human review log is missing.
- `Content complete, build pending`: manuscripts pass without `--draft`, HTML not yet built or audited.
- `Draft`: audited with `--draft`; list the lessons and sections still missing.
- `Incomplete`: name the failing chapters, lessons and error codes.

Then give counts: canonical chapters, lessons, exercises expected and found, solutions found, Java blocks compiled and run, error and warning totals by code. Separate verified facts from recommendations. If an input was empty or unreadable (for example an upload that arrived as a zero-byte file), say so and name which checks could not run.
