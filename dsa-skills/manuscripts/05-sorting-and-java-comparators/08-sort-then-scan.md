<!-- lesson-kind: standard -->
<!-- lesson-id: sort-then-scan -->
## Sort Then Scan

<!-- stage: context -->
### Find The Third Distinct Score

A ranking service receives integer scores and needs the third distinct maximum. Repeated scores share one rank. If fewer than three distinct scores exist, the service must return the maximum instead. For `[2, 2, 3, 1]`, the answer is `1`; for `[1, 2]`, the fallback answer is `2`.

Sorting does not finish this problem. It exposes equal runs and rank order, after which a scan must count distinct values and enforce the required alternative answer. The post-sort state, not the library call, produces the answer.

<!-- stage: naive -->
### Read A Fixed Position

A tempting implementation sorts ascending and reads `ordered[n - 3]`.

```java nocompile
Arrays.sort(ordered);
return ordered[ordered.length - 3];
```

This works only when at least three elements exist and the top three positions are distinct. On `[3, 2, 2, 1]`, it returns `2`, although the third distinct maximum is `1`. On a two-element input, it indexes before the array.

<!-- stage: bottleneck -->
### Positions Do Not Equal Distinct Ranks

Removing duplicates into another collection before selecting a rank can be correct, but it creates an extra result structure and still needs a rule for fewer than three values. Repeatedly searching for the next lower score is worse: each rank query may scan the whole array, leading to O(kn) work for rank `k` and complicated sentinel handling at the integer extremes.

After sorting, one linear scan can skip equal neighbors, count only run boundaries, and stop at the requested distinct rank. The important work is the small state machine that interprets the new order.

<!-- stage: insight -->
### Separate Preprocessing From The Answer Scan

**Sort-then-scan** uses sorting as preprocessing that makes a later relation local. The scan carries the state required by the output contract. Here, every new value encountered while moving from right to left advances the **distinct rank** exactly once.

<!-- names: sort-then-scan, distinct rank, fallback contract -->

Initialize `maximum` from the greatest sorted value. Set `rank` to one because that value establishes the first distinct rank. For each lower index, skip the value if it equals its right neighbor. Otherwise increment `rank`; when it reaches three, return the current value.

If the scan ends first, return `maximum`. That branch is the **fallback contract**, not error recovery. It is part of the problem statement and must be represented deliberately rather than reached through an invalid index or a numeric sentinel.

The scan summary changes across problems. It may hold a best gap, a rank count, a mapping back to original indices, or the first position that violates an expected sequence. Sorting is useful only because it proves that local observations are sufficient for that summary.

<!-- stage: variables -->
### Rank, Neighbor, And Fallback

`ordered` is an owned sorted copy. `maximum` is `ordered[n - 1]` and remains the fallback. `rank` counts distinct runs seen from the high end. Index `i + 1` is the neighbor that tells whether `ordered[i]` begins another run. No sentinel value represents “not found,” so `Integer.MIN_VALUE` remains an ordinary valid score.

<!-- stage: trace -->
### Count Runs, Not Positions

Sort `[2, 2, 3, 1]` into `[1, 2, 2, 3]` and start at the right. Value `3` establishes rank one and the fallback maximum. Moving left reaches `2`, which differs from `3`, so `2` establishes rank two.

The next `2` equals its right neighbor and belongs to the same run; rank does not change. The final `1` differs from `2`, establishing rank three, so the scan returns `1`. On `[1, 2]`, the scan would establish only two ranks and then return the stored maximum `2`. Both outcomes follow from the same state rather than separate positional shortcuts. No array position is mistaken for a rank.

```trace
{"cells":[1,2,2,3],"pointers":["scan","neighbor"],"steps":[{"at":{"scan":3,"neighbor":3},"vars":{"value":3,"rank":1,"maximum":3},"note":"The greatest value establishes rank one and the fallback maximum."},{"at":{"scan":2,"neighbor":3},"vars":{"value":2,"rank":2},"note":"Two differs from three, so it begins the second distinct run."},{"at":{"scan":1,"neighbor":2},"vars":{"value":2,"rank":2},"note":"The duplicate two stays inside the current run and does not advance rank."},{"at":{"scan":0,"neighbor":1},"vars":{"value":1,"rank":3},"note":"One begins the third distinct run and is returned."}]}
```

<!-- stage: code -->
### Make The Fallback Explicit

```java run
import java.util.Arrays;

public final class SortThenScan {
    static int thirdMaximum(int[] nums) {
        int[] ordered = nums.clone();
        Arrays.sort(ordered);
        int maximum = ordered[ordered.length - 1];
        int rank = 1;
        for (int i = ordered.length - 2; i >= 0; i--) {
            if (ordered[i] == ordered[i + 1]) continue;
            if (++rank == 3) return ordered[i];
        }
        return maximum;
    }

    public static void main(String[] args) {
        if (thirdMaximum(new int[] {2,2,3,1}) != 1) throw new AssertionError();
        if (thirdMaximum(new int[] {1,2}) != 2) throw new AssertionError();
    }
}
```

Sorting costs O(n log n) and the scan costs O(n). The copy costs O(n) space and preserves the input. The contract guarantees a nonempty array, so establishing `maximum` requires no defensive branch.

<!-- stage: applicability -->
### When It Applies

Use sort-then-scan when sorting exposes an adjacent relation but a separate scan must compute ranks, gaps, mismatches, or mapped output. State the scan invariant independently of the sort: before each iteration, the retained variables summarize every processed run or position needed by the final answer.

The false friend is binary search. Sorted input alone does not create a monotone yes/no predicate, so not every post-sort question supports binary search. Another false friend is treating a sorted position as a distinct rank without accounting for duplicate runs.

The method silently fails when the scan discards original indices that the output still needs, when a fallback is not modeled, or when arithmetic across adjacent extremes uses `int`. Empty-input behavior must follow the problem contract. For this problem the array is nonempty, duplicates are meaningful, and integer extremes require no sentinel workaround.

<!-- stage: exercises -->
### Exercises

#### [Build] Third Maximum Number (LeetCode 414)
<!-- id: scan-third-maximum -->

**Prerequisites.** Sorting a copy and counting distinct runs.

**Problem.** Given a nonempty integer array, return its third distinct maximum. If fewer than three distinct values exist, return the maximum.

**Constraints.** `1 <= nums.length <= 10^4`; values span the signed 32-bit range.

**Example 1.** Input `[3,2,1]`, output `1`.

**Example 2.** Input `[2,2,3,1]`, output `1`; the repeated `2` owns one rank.

**Hint.** Scan the sorted array from greatest to least and advance the rank only at a run boundary.

**Changed decision.** The scan selects a distinct rank and owns a specified maximum fallback.

#### [Vary] Relative Ranks (LeetCode 506)
<!-- id: scan-relative-ranks -->

**Prerequisites.** Object ordering and preserving original indices in records.

**Problem.** Given distinct athlete scores, return a label for each original position. The highest three receive `"Gold Medal"`, `"Silver Medal"`, and `"Bronze Medal"`; every other athlete receives the decimal form of the athlete's one-based rank.

**Constraints.** `1 <= score.length <= 10^4`; scores are distinct positive integers.

**Example 1.** Input `[5,4,3,2,1]`, output `["Gold Medal","Silver Medal","Bronze Medal","4","5"]`.

**Example 2.** Input `[10,3,8,9,4]`, output `["Gold Medal","5","Bronze Medal","Silver Medal","4"]`.

**Hint.** Sort records containing both score and original index. During the scan, where should each rank label be written?

**Changed decision.** The sorted scan writes results back through saved positions rather than returning sorted values.

#### [Boundary] Fewer Than K Distinct Values (Author exercise)
<!-- id: scan-fewer-than-k-distinct -->

**Prerequisites.** Distinct-run counting and explicit fallback behavior.

**Problem.** Given a nonempty integer array and positive `k`, return the `k`th distinct maximum. If fewer than `k` distinct values exist, return the maximum.

**Constraints.** `1 <= nums.length <= 10^5`; `1 <= k <= 10^5`; values span the signed 32-bit range.

**Example 1.** Input `nums = [9,9,4]`, `k = 3`, output `9`; only two distinct values exist.

**Example 2.** Input `nums = [MIN,0,MAX]`, `k = 2`, output `0`.

**Hint.** Store the maximum before scanning. Never encode “rank not reached” as a special integer value.

**Changed decision.** The target rank becomes input, so the scan must handle ranks larger than the number of runs.

#### [Recognize] Missing Number (LeetCode 268)
<!-- id: scan-missing-number -->

**Prerequisites.** Sorted expected positions and complete end-of-scan handling.

**Problem.** Given `n` distinct values drawn from `[0, n]`, return the only missing value. Solve this version by sorting and scanning.

**Constraints.** `1 <= n <= 10^4`; `nums.length == n`; every value lies in `[0, n]` and is distinct.

**Example 1.** Input `[3,0,1]`, output `2`.

**Example 2.** Input `[0,1]`, output `2`; every stored position matches, so the missing value is the endpoint `n`.

**Hint.** In sorted order, which value should appear at index `i` before the missing position shifts every later value?

**Changed decision.** The scan searches for the first mismatch against an expected sequence and uses `n` as the end fallback.
