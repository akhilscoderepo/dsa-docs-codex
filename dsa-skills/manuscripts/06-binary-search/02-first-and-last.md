<!-- lesson-kind: standard -->
<!-- lesson-id: first-and-last -->
## First And Last

<!-- stage: context -->
### A Range Of Duplicates

An event index stores timestamps in sorted order, and many events can share the same second. A query asks for the complete block belonging to timestamp `3`, not merely one event from it. Exact search can land anywhere inside that block. The desired output is instead the smallest and largest matching index, or `[-1,-1]` when the timestamp is absent. Duplicates turn equality from a stopping condition into evidence that must be saved while the search continues.

<!-- stage: naive -->
### Find Then Expand

One correct approach uses exact search, then walks left and right across equal values. It is simple and often the first implementation worth testing because each expansion ends exactly where equality ends.

```java
static int[] expand(int[] a, int target, int hit) {
    int first = hit, last = hit;
    while (first > 0 && a[first - 1] == target) first--;
    while (last + 1 < a.length && a[last + 1] == target) last++;
    return new int[] {first, last};
}
```

<!-- stage: bottleneck -->
### A Million Equal Values

If every element in a million-position array equals the target, exact lookup takes O(log n), but expansion touches nearly the entire array. The combined method therefore has O(n) worst-case time. More importantly, it abandons sorted-order reasoning precisely where duplicates are most numerous. The left edge is itself a searchable boundary: values before it are too small, while positions from the edge through the duplicate block satisfy equality.

<!-- stage: insight -->
### Equality Becomes A Candidate

A **boundary search** does not return immediately on equality. To find the **first occurrence**, keep `answer = mid` when a match appears and continue with `hi = mid - 1`. The saved index is a valid candidate; searching left asks whether a better candidate exists. Values below the target still move `lo` right, while values above it move `hi` left. For the last occurrence, save the same way but continue with `lo = mid + 1`.

<!-- names: boundary search, first occurrence -->

The invariant now has two parts: any better answer remains inside `[lo, hi]`, and `answer` is either `-1` or a confirmed match. That second clause lets the interval become empty without losing a match found earlier. Running the two directional searches independently is clearer than trying to discover both endpoints in one loop. Sortedness makes the moves safe, and the candidate protects information that ordinary exact search would discard.

<!-- stage: variables -->
### Candidate And Direction

`lo` and `hi` delimit the inclusive region that may contain an earlier or later match. `answer` stores the best confirmed position so far. The comparison rules are identical to exact search except on equality, where the requested direction decides which endpoint crosses `mid`.

<!-- stage: trace -->
### Search Past A Match

Find the first `3` in `[1,3,3,3,3,8,12]`. Index 3 matches, so it becomes the candidate, but the search continues through indices 0 to 2. Index 1 also matches and improves the candidate. The remaining interval contains only index 0, whose value 1 is too small, so `lo` moves to 1 and crosses `hi`. The loop returns candidate 1. The hard step is the first one: equality is recorded but deliberately does not terminate the search. A last-occurrence search would make the opposite move at that exact point. In either direction, the stored candidate remains valid while the interval asks whether a more extreme one exists.

```trace
{"cells":[1,3,3,3,3,8,12],"pointers":["lo","mid","hi"],"steps":[{"at":{"lo":0,"mid":3,"hi":6},"vars":{"candidate":-1},"note":"Keep the match and continue left."},{"at":{"lo":0,"mid":1,"hi":2},"vars":{"candidate":3},"note":"Keep the match and continue left."},{"at":{"lo":0,"mid":0,"hi":0},"vars":{"candidate":1},"note":"Move toward the target."}]}
```

<!-- stage: code -->
### Two Directed Searches

```java
static int boundary(int[] a, int target, boolean first) {
    int lo = 0, hi = a.length - 1, answer = -1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) {
            answer = mid;
            if (first) hi = mid - 1;
            else lo = mid + 1;
        } else if (a[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return answer;
}
```

Calling this method once with `true` and once with `false` gives the range. Each pass costs O(log n), so two passes remain O(log n); the method uses O(1) extra space. Empty input naturally returns `-1`, and all-equal input still halves its interval rather than expanding linearly.

<!-- stage: applicability -->
### When A Match Is Not Enough

Use this pattern when sorted duplicates are allowed and the output asks for an extreme equal position. State the invariant as: `answer` is a confirmed match, while any earlier or later match that could improve it remains in `[lo, hi]`. The false friend is ordinary exact search, which stops too early. Another false friend is lower bound; it returns an insertion index even when the target is absent, whereas this method returns `-1`. Java's midpoint rule remains relevant, and a shared mutable `answer` across the two passes can silently mix their results.

<!-- stage: exercises -->
### Exercises

#### [Build] First Occurrence (Author exercise)
<!-- id: bs-first-occurrence -->

**Prerequisites.** Exact binary search and candidate preservation from this lesson.

**Problem.** Given a nondecreasing integer array and a target, return the smallest index whose value equals the target, or `-1` if no match exists.

**Constraints.** `0 <= nums.length <= 10^5`; duplicates are allowed; require O(log n) time and O(1) space.

**Example 1.** Input `nums = [2,2,2,5,9]`, `target = 2`; output `0`.

**Example 2.** Input `nums = [1,4,4]`, `target = 3`; output `-1`.

**Hint.** Treat equality as a valid candidate rather than an instruction to return. Which half can still contain an earlier equal value?

**Changed decision.** A match is retained while the search deliberately continues toward lower indices.

#### [Vary] Last Occurrence (Author exercise)
<!-- id: bs-last-occurrence -->

**Prerequisites.** The first-occurrence loop immediately above.

**Problem.** Given a sorted array with possible duplicates, return the greatest index equal to `target`, or `-1` when the target is absent.

**Constraints.** `0 <= nums.length <= 10^5`; use logarithmic time and constant auxiliary space.

**Example 1.** Input `nums = [1,4,4,4,8]`, `target = 4`; output `3`.

**Example 2.** Input `nums = [7,7]`, `target = 9`; output `-1`.

**Hint.** Keep the candidate rule unchanged. Reverse only the direction selected after equality.

**Changed decision.** Equality now preserves the right side because only a later match can improve the answer.

#### [Boundary] Find First and Last Position (LeetCode 34)
<!-- id: bs-complete-target-range -->

**Prerequisites.** Both directional occurrence searches.

**Problem.** Return the first and last index of `target` in a nondecreasing array. Return `[-1,-1]` if the target does not appear.

**Constraints.** `0 <= nums.length <= 10^5`; values fit in `int`; required O(log n) time.

**Example 1.** Input `nums = [0,3,3,3,10]`, `target = 3`; output `[1,3]`.

**Example 2.** Input `nums = [5,5,5]`, `target = 5`; output `[0,2]`.

**Hint.** Run the same helper in two directions. Can an absent result be handled without a separate linear check?

**Changed decision.** The output combines both extremes and must preserve the absent sentinel in both positions.

#### [Recognize] First Bad Version (LeetCode 278)
<!-- id: bs-recognize-first-bad -->

**Prerequisites.** First-occurrence reasoning and a monotone boolean oracle.

**Problem.** Versions `1..n` change once from good to bad. Given an oracle `isBadVersion(v)`, return the smallest bad version while minimizing oracle calls.

**Constraints.** `1 <= n <= 2^31 - 1`; at least one version is bad; target O(log n) oracle calls.

**Example 1.** Input `n = 8`, first bad `6`; output `6`.

**Example 2.** Input `n = 1`, first bad `1`; output `1`.

**Hint.** A bad midpoint is a candidate, but an earlier bad version may exist. Which endpoint can keep `mid` without calling the oracle again?

**Changed decision.** Explicit duplicate values disappear; a monotone predicate supplies the same left-boundary shape.
