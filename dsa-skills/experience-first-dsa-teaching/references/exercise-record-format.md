# Exercise and solution records

## Exercise record

```markdown
#### Title
<!-- id: permanent-slug -->
<!-- role: Build | Vary | Boundary | Recognize | ... -->
<!-- source: Author exercise | LeetCode N -->

##### Problem Statement

A formal statement in your own words. Identify the input, required output, and exact result to return.

##### Constraints

State precise legal limits and the required time and space targets.

##### Examples

**Example 1.** Input `...`; output `...`. Explain the result in one sentence.

**Example 2.** Use an adversarial boundary, duplicate, empty, extreme, or contract-sensitive case.

##### Prerequisites

Name only the ideas the learner already needs, with chapter references where useful.

##### Hint

Ask a diagnostic question that points toward the deciding invariant without revealing the implementation.

##### Learning Objective

State the one decision that changes from the previous problem in the staircase.
```

Roles, in ladder order: Build, Vary, Boundary, Recognize, then optionally Extend, Medium, Hard, Challenge. A lesson has at least one each of Build, Vary, Boundary and Recognize, between 4 and 7 exercises, and roles never go backward.

The `id`, `role`, and `source` comments sit directly below the H4 title. The ID uses lowercase letters, digits, and hyphens. It remains unique and permanent because learner notes and status use it as a key. The reader sees the title and academic sections; the renderer converts the role and source metadata into small badges. The matching solution record carries the same metadata.

The audit requires every section above, two examples that state an input and output, and enough detail to solve the problem without guessing. Internal staircase roles never appear in the reader-facing title.

## Content rules

- Author exercises are complete problems with precise constraints, not titles or one-line goals. When a specification supplies only a short goal, define a small checkable task and an adversarial second example.
- Restate LeetCode problems in your own words, verify the real constraints, and compute new examples. Never copy the original statement or samples.
- The Build problem uses only the current lesson's technique. Later problems may use earlier lessons but never an unreleased technique.
- Compute each example with executable code or a brute-force oracle. Keep every value inside the stated constraints.
- Never repeat the same sentence across exercises.

## Solution record

Store each solution in `solutions/<lesson file>`.

````markdown
#### Solution: Title
<!-- id: permanent-slug -->
<!-- role: Build | Vary | Boundary | Recognize | ... -->
<!-- source: Author exercise | LeetCode N -->

##### Algorithmic Solution

Explain the algorithm in two to five connected sentences. Tie each state update to the lesson's invariant and explain why the algorithm can discard or finalize data safely.

##### Complexity Analysis

State time and space complexity and name the operation that causes each bound.

```java run
public final class Name {
    // Time: O(n). Each input value contributes to one constant-time update.
    // Space: O(1). The method stores only fixed-size scalar state.
    static int solve(...) { ... }

    public static void main(String[] args) {
        if (solve(...) != ...) throw new AssertionError("example 1");
        if (solve(...) != ...) throw new AssertionError("example 2");
    }
}
```
````

The heading after `Solution:` matches the exercise title, and all metadata matches the exercise. Where a cheap brute force exists, add a deterministic randomized cross-check to `main`; it catches failures that two examples miss. The audit compiles every `java run` block and executes its assertions.

Comment every primary statement or control-flow decision that carries algorithmic meaning. Explain why the statement exists, which invariant it preserves, or which cost it controls. Put the time and space bounds beside the method. Do not comment braces, imports, declarations whose names already explain them, or syntax such as `i++`; comments that merely restate code reduce readability.
