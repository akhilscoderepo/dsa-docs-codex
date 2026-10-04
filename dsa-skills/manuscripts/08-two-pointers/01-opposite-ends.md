<!-- lesson-kind: standard -->
<!-- lesson-id: opposite-ends -->
## Opposite Ends

<!-- stage: context -->
### One Pair From Many

Suppose a sorted price list contains thousands of values and you need two entries whose sum equals a budget. Checking every pair works, but it ignores the order already present. Compare the first and last values. Their sum does more than classify that one pair: it tells us which endpoint cannot participate in any remaining answer. The central question is not merely which pointer to move, but what evidence makes that movement safe.

<!-- stage: naive -->
### Check Every Pair

The direct method enumerates every `i < j` and returns when a matching sum appears. It is easy to verify, works without sorted input, and provides a useful oracle for testing the faster scan on small arrays.

```java nocompile
for (int i = 0; i < values.length; i++) {
    for (int j = i + 1; j < values.length; j++) {
        if ((long) values[i] + values[j] == target) return new int[] {i, j};
    }
}
```

<!-- stage: bottleneck -->
### Repeated Comparisons

For `n` values, the nested loops inspect `n(n-1)/2` pairs, so the running time is O(n²). On a sorted list, many of those comparisons are already settled by one endpoint comparison. If the smallest remaining value plus the largest is below the target, pairing that smallest value with anything smaller than the largest cannot help. Retaining it only creates comparisons that order has already disproved.

<!-- stage: insight -->
### Eliminate An Endpoint

Place `left` at the smallest remaining value and `right` at the largest. If their sum equals the target, the search is over. If the sum is too small, every pair using `values[left]` is too small because all other partners are no larger than `values[right]`; advance `left`. If the sum is too large, every pair using `values[right]` is too large because all other partners are no smaller than `values[left]`; decrement `right`.

<!-- names: opposite-end scan, endpoint elimination -->

This is an **opposite-end scan**. Its progress comes from **endpoint elimination**: one comparison rules out an entire row or column of conceptual pairs. Each move has a proof tied to sorted order. The interval shrinks and neither pointer ever reverses, so at most `n-1` comparisons occur. Use `long` for the sum when inputs can approach integer limits.

<!-- stage: variables -->
### State And Meaning

`left` and `right` bound every candidate pair not yet ruled out. `sum` is computed from those endpoints using `long`. For closest-sum variants, `best` preserves the strongest candidate encountered before an endpoint is discarded. The invariant is that any exact answer still possible uses two indices within the closed interval from `left` through `right`.

<!-- stage: trace -->
### A Shrinking Search

For `[1, 3, 4, 6, 8, 11]` and target `10`, begin with 1 and 11. Their sum is 12, so 11 is too large even beside the smallest candidate; move `right`. The pair 1 and 8 sums to 9. Because 1 cannot reach 10 even with the largest remaining partner, move `left`. Now 3 and 8 sum to 11, which eliminates 8. Finally 3 and 6 sum to 9, eliminating 3; 4 and 6 produce 10.

Each move removes exactly the endpoint proved unusable. Notice that the algorithm never discards both endpoints after a mismatch. Only one side has enough evidence to leave.

```trace
{"cells":[1,3,4,6,8,11],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":5},"vars":{"sum":12,"target":10},"note":"The sum is too large, so index 5 cannot belong to an answer."},{"at":{"left":0,"right":4},"vars":{"sum":9,"target":10},"note":"The sum is too small, so index 0 cannot belong to an answer."},{"at":{"left":1,"right":4},"vars":{"sum":11,"target":10},"note":"Discard the right endpoint because the sum is too large."},{"at":{"left":1,"right":3},"vars":{"sum":9,"target":10},"note":"Discard the left endpoint because the sum is too small."},{"at":{"left":2,"right":3},"vars":{"sum":10,"target":10},"note":"The remaining endpoints form the requested pair."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java run
public final class SortedPairSearch {
    static int[] find(int[] a, int target) {
        int left = 0, right = a.length - 1;
        while (left < right) {
            long sum = (long) a[left] + a[right];
            if (sum == target) return new int[] {left, right};
            if (sum < target) left++;
            else right--;
        }
        return new int[] {-1, -1};
    }
    public static void main(String[] args) {
        int[] p = find(new int[] {1,3,4,6,8,11}, 10);
        if (p[0] != 2 || p[1] != 3) throw new AssertionError();
    }
}
```

The loop requires distinct positions, hence `left < right`. It returns zero-based indices because this method owns its contract; LC 167 instead requests one-based positions. The time cost is O(n), and the method uses O(1) auxiliary space.

<!-- stage: applicability -->
### When It Applies

Use this pattern when endpoints have a monotone relationship: a sorted pair sum, a symmetric string comparison, or an objective whose limiting endpoint can be proved disposable. State the invariant that every unruled candidate remains inside `[left, right]`, then justify each move against it.

The false friend is an unsorted pair search. Without sorted order, a small endpoint sum does not prove that advancing the left index is safe. A hash map or an allowed preliminary sort is needed instead. Another false friend is binary search: binary search discards half a one-dimensional search space, while this scan removes one endpoint from a two-item candidate space.

<!-- stage: exercises -->
### Exercises

#### [Build] Two Sum II (LeetCode 167)
<!-- id: tp-two-sum-ii -->

**Prerequisites.** Sorted arrays and the endpoint elimination argument from this lesson.

**Problem.** Given a nondecreasing integer array `numbers` and an integer `target`, return the one-based indices of two distinct elements whose sum is `target`. Exactly one solution exists, and an element cannot be reused.

**Constraints.** `2 <= numbers.length <= 3 * 10^4`; values and target fit in signed 32-bit integers. Use O(1) auxiliary space.

**Example 1.** Input `numbers = [1,3,4,6,8,11]`, `target = 10`; output `[3,4]`.

**Example 2.** Input `numbers = [-5,-2,7,12]`, `target = 5`; output `[2,3]`.

**Hint.** Compare the endpoint sum with the target and ask which endpoint cannot succeed with any remaining partner.

**Changed decision.** Convert the internal zero-based pointer positions to the one-based output contract.

#### [Vary] Closest Pair Sum (Author exercise)
<!-- id: tp-closest-pair-sum -->

**Prerequisites.** Opposite-end movement and safe `long` arithmetic.

**Problem.** Given a sorted integer array `nums` and an integer `target`, return the pair of values whose sum has the smallest absolute distance from `target`. If several pairs tie, return the lexicographically smallest value pair.

**Constraints.** `2 <= nums.length <= 10^5`; each value is between `-10^9` and `10^9`. Target O(n) time.

**Example 1.** Input `nums = [1,4,7,10]`, `target = 12`; output `[1,10]`.

**Example 2.** Input `nums = [-8,-3,2,9]`, `target = 0`; output `[-8,9]`.

**Hint.** Record the current pair before discarding an endpoint; compare distances using `long`.

**Changed decision.** A missing exact match no longer ends the search without an answer, so preserve the best discarded candidate.

#### [Boundary] Two Values (Author exercise)
<!-- id: tp-two-values -->

**Prerequisites.** The `left < right` loop boundary.

**Problem.** Given a sorted array containing exactly two integers and a target, return `true` if those two values sum to the target and `false` otherwise. Do not access any position more than once.

**Constraints.** `nums.length == 2`; values may equal `Integer.MIN_VALUE` or `Integer.MAX_VALUE`.

**Example 1.** Input `nums = [4,4]`, `target = 8`; output `true`.

**Example 2.** Input `nums = [2147483647,2147483647]`, `target = -2`; output `false`.

**Hint.** Widen before addition; an overflowing `int` can look equal to an unrelated target.

**Changed decision.** The smallest legal interval exposes both the distinct-index rule and overflow risk.

#### [Recognize] Container With Most Water (LeetCode 11)
<!-- id: tp-container-water -->

**Prerequisites.** Endpoint elimination and maximum tracking.

**Problem.** Given nonnegative heights, choose two indices that form a container with the x-axis. Return the maximum area, computed as width times the shorter height.

**Constraints.** `2 <= height.length <= 10^5`; `0 <= height[i] <= 10^4`. Target O(n) time.

**Example 1.** Input `height = [1,8,6,2,5,4,8,3,7]`; output `49`.

**Example 2.** Input `height = [1,1]`; output `1`.

**Hint.** After measuring an endpoint pair, decide which wall limits its area and whether moving the other wall could improve that limit.

**Changed decision.** Pointer movement follows a limiting-height proof rather than comparison with a target sum.
