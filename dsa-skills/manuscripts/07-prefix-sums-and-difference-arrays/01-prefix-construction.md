<!-- lesson-kind: standard -->
<!-- lesson-id: prefix-construction -->
## Prefix Construction

<!-- stage: context -->
### Repeated Totals

A monitoring service stores the number of requests received each minute. A dashboard needs the total through every minute: after minute zero, after minute one, and so on. Recomputing each total from the beginning is correct, but it revisits almost the same data for every output position. The useful observation is that the total through the current minute differs from the previous total by exactly one value.

<!-- stage: naive -->
### Sum Every Prefix

The direct implementation starts a fresh scan for each output. It is correct because output `i` explicitly sums exactly the values from index zero through `i`. Nothing is reused, but nothing is omitted either.

```java run
public final class PrefixNaive {
    static long[] running(int[] nums) {
        long[] answer = new long[nums.length];
        for (int end = 0; end < nums.length; end++)
            for (int i = 0; i <= end; i++) answer[end] += nums[i];
        return answer;
    }
    public static void main(String[] args) {
        if (!java.util.Arrays.equals(running(new int[]{3,-1,4}), new long[]{3,2,6}))
            throw new AssertionError();
    }
}
```

<!-- stage: bottleneck -->
### The Triangle Of Work

For `[3, -1, 4, 2]`, the first value is read four times, the second three times, and the last once. The reads form `1 + 2 + ... + n`. With 100,000 measurements, that is roughly five billion additions merely to produce 100,000 totals. The method costs O(n^2) time even though consecutive outputs share all but one input value. That repeated prefix is the waste.

<!-- stage: insight -->
### Preserve The Previous Total

The earlier calculation already contains the sum we need to start the next one. Keep a **running sum**, add the current value once, and publish the new total. For later range work, a boundary-oriented **sentinel prefix** is even more useful: allocate `n + 1` cells, define `prefix[0] = 0`, and set `prefix[i + 1] = prefix[i] + nums[i]`. Now cell `i` always means “the sum of the first `i` values,” not “the sum through index `i`.”

<!-- names: running sum, sentinel prefix -->

The extra zero is meaningful state, not padding. It represents the empty choice before the array begins and lets the same recurrence handle index zero. The safe move is to extend a known prefix by exactly the next value. Inductively, if `prefix[i]` summarizes the first `i` values, adding `nums[i]` makes `prefix[i + 1]` summarize the first `i + 1`. Each input contributes once, so no earlier work is discarded.

<!-- stage: variables -->
### State And Boundaries

`i` is the array index being consumed. `prefix[i]` is the sum strictly before `i`, while `prefix[i + 1]` includes `nums[i]`. The array has `n + 1` boundaries for `n` values. Every stored total is a `long` so valid `int` inputs cannot overflow cumulative state.

<!-- stage: trace -->
### Building Five Boundaries

For `[3, -1, 4, 2]`, begin with boundary zero holding `0`. Consume `3`; boundary one becomes `3`. Adding `-1` does not reset anything—it produces boundary two, `2`. The third value, `4`, takes the total to `6`, and the last value takes it to `8`.

The hardest step is the negative value. A prefix total need not be increasing, so later techniques must never assume monotonicity merely because they use cumulative sums. What remains true is algebraic: every boundary stores the exact total before that boundary. The completed array is `[0, 3, 2, 6, 8]`, with one more cell than the input.

```trace
{"cells":[3,-1,4,2],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"before":0,"after":3},"note":"Extend the empty prefix with 3."},{"at":{"i":1},"vars":{"before":3,"after":2},"note":"Add -1; cumulative state may decrease."},{"at":{"i":2},"vars":{"before":2,"after":6},"note":"Boundary 3 now summarizes the first three values."},{"at":{"i":3},"vars":{"before":6,"after":8},"note":"The final boundary summarizes the whole array."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java run
public final class PrefixBlueprint {
    static long[] build(int[] nums) {
        long[] prefix = new long[nums.length + 1];
        for (int i = 0; i < nums.length; i++) prefix[i + 1] = prefix[i] + nums[i];
        return prefix;
    }
    public static void main(String[] args) {
        long[] got = build(new int[]{3,-1,4,2});
        if (!java.util.Arrays.equals(got, new long[]{0,3,2,6,8})) throw new AssertionError();
    }
}
```

The loop performs one addition per value, so construction costs O(n) time and O(n) space. The empty array produces the one-cell prefix `[0]`, which is the correct representation of its only boundary. An in-place running-sum problem may overwrite the input, but this sentinel form deliberately preserves it.

<!-- stage: applicability -->
### When It Applies

Use prefix construction when later operations repeatedly need the aggregate of everything before a position. State the invariant as: before iteration `i`, `prefix[i]` equals the sum of `nums[0..i-1]`; after the assignment, it also holds for boundary `i + 1`.

The nearest false friend is Kadane's algorithm. Kadane discards harmful earlier sums to optimize one subarray, while a prefix array records exact totals at every boundary. Another false friend is assuming totals are sorted; negative values invalidate binary search over prefix sums. In Java, accumulate into `long` before assignment. Writing `prefix[i] + nums[i]` is safe because `prefix[i]` is already a `long`.

<!-- stage: exercises -->
### Exercises

#### [Build] Running Sum of 1d Array (LeetCode 1480)
<!-- id: ps-running-sum -->

**Prerequisites.** Array traversal and the running-sum state from this lesson.

**Problem.** Given an integer array `nums`, return an array whose value at index `i` is the sum of `nums[0]` through `nums[i]`, inclusive.

**Constraints.** `1 <= nums.length <= 1000` and `-10^6 <= nums[i] <= 10^6`. Target O(n) time.

**Example 1.** Input `nums = [2, 5, -1]`, output `[2, 7, 6]`; each cell extends the previous total.

**Example 2.** Input `nums = [0]`, output `[0]`; the first running total may be zero.

**Hint.** What single value from the previous iteration contains all earlier contributions? Decide whether the returned array may reuse the input storage.

**Changed decision.** This first rung stores inclusive totals rather than the lesson's extra sentinel boundary.

#### [Vary] Find Pivot Index (LeetCode 724)
<!-- id: ps-pivot-index -->

**Prerequisites.** Running totals and computing a whole-array total in `long`.

**Problem.** Given an integer array, return the leftmost index whose strictly-left sum equals its strictly-right sum. Return `-1` when no such index exists.

**Constraints.** `1 <= nums.length <= 10^4` and `-1000 <= nums[i] <= 1000`. Target O(n) time and O(1) auxiliary space.

**Example 1.** Input `nums = [2, 1, -1]`, output `0`; both sides of index zero sum to zero.

**Example 2.** Input `nums = [1, 2, 3]`, output `-1`; no boundary balances the two sides.

**Hint.** If `left` is known and `total` is fixed, express the right side without scanning it. Update `left` only after testing the current index.

**Changed decision.** The cumulative value is now rolling state used for a comparison rather than an output array.

#### [Boundary] Empty Prefix (Author exercise)
<!-- id: ps-empty-prefix -->

**Prerequisites.** The sentinel-prefix convention introduced in this lesson.

**Problem.** Given an integer array, return its `n + 1` boundary sums, including zero for the empty prefix before the first value.

**Constraints.** `0 <= nums.length <= 10^5`; totals fit in `long`. Target O(n) time and O(n) output space.

**Example 1.** Input `nums = []`, output `[0]`; an empty array still has one boundary.

**Example 2.** Input `nums = [-4, 4]`, output `[0, -4, 0]`; cumulative state may return to zero.

**Hint.** Allocate for boundaries, not values. Which output index represents the state before any input has been consumed?

**Changed decision.** Empty input becomes observable state instead of being excluded by the contract.

#### [Recognize] Prefix Averages (Author exercise)
<!-- id: ps-prefix-averages -->

**Prerequisites.** Long cumulative totals and integer division rules in Java.

**Problem.** Given an integer array, return a `long[]` where output `i` is the floor average of the first `i + 1` values, using mathematical floor for negative totals.

**Constraints.** `1 <= nums.length <= 10^5`; use O(n) time and only the returned array beyond scalar state.

**Example 1.** Input `nums = [5, 1, 6]`, output `[5, 3, 4]`.

**Example 2.** Input `nums = [-1, 0]`, output `[-1, -1]`; mathematical floor of `-0.5` is `-1`.

**Hint.** Preserve one cumulative total, but do not use `/` when a negative non-divisible total must round downward. Which Java helper implements floor division?

**Changed decision.** The aggregate is divided by a growing prefix length with explicit negative-rounding semantics.

