<!-- lesson-kind: standard -->
<!-- lesson-id: lower-and-upper-bounds -->
## Lower And Upper Bounds

<!-- stage: context -->
### Where A Value Belongs

A sorted price list receives a new price. The value may already appear several times, but the insertion rule is precise: place it before the first value that is not smaller. For `[2,2,5,5,5,9]`, a new `5` belongs at index 2 under that rule. Another API might place it after every existing `5`, at index 5. Neither request is an exact lookup. Both ask for the boundary where a comparison changes from false to true.

<!-- stage: naive -->
### Scan Until The Rule Changes

A left-to-right scan can stop at the first qualifying value. Changing `>=` to `>` decides whether equal values remain after the returned position or before it.

```java
static int lowerBoundLinear(int[] nums, int target) {
    int i = 0;
    while (i < nums.length && nums[i] < target) i++;
    return i;
}
```

This implementation is correct, including the case where it returns `nums.length`. Its weakness is not the contract but the amount of sorted data it ignores.

<!-- stage: bottleneck -->
### A Long Sorted Prefix

Suppose a catalogue contains ten million prices and the insertion point is near the end. The scan performs almost ten million comparisons even though one comparison at the middle proves that an entire half is too small or contains the answer. Repeating this operation for many insertions or queries makes the linear walk the dominant cost. A scan takes O(n) time per query; the sorted order can reduce that to O(log n).

<!-- stage: insight -->
### Search For A Transition

A **lower bound** is the first index `i` for which `nums[i] >= target`. An **upper bound** is the first index `i` for which `nums[i] > target`. Think of either comparison as a predicate over the sorted array. It is false for a prefix and true for the remaining suffix. Binary search locates the first true position.

<!-- names: lower bound, upper bound, half-open interval -->

Use the half-open interval `[lo, hi)`, beginning with `lo = 0` and `hi = nums.length`. Positions before `lo` are known to fail the predicate. The answer remains somewhere in `[lo, hi]`, where the value `nums.length` is a legitimate boundary after the last element. If `mid` satisfies the predicate, keep it by assigning `hi = mid`. Otherwise, discard it with the false prefix by assigning `lo = mid + 1`. Equality therefore stays on the right for a lower bound and moves left for an upper bound.

<!-- stage: variables -->
### Two Endpoints One Predicate

`lo` is the first position not yet proved to fail. `hi` is an exclusive array endpoint and also a possible insertion result. `mid` is safe to index only while `lo < hi`, because then `mid < hi <= nums.length`. No separate candidate is required: when the interval collapses, `lo` itself is the first true position, or `nums.length` when the predicate never becomes true.

<!-- stage: trace -->
### Equality Does Not Stop

Find the lower bound of `5` in `[2,2,5,5,5,9]`. Start with `[lo, hi) = [0,6)`. Index 3 contains `5`, so the predicate `value >= 5` is true. Index 3 might still be too late, which means it must remain possible while the right endpoint moves to 3. Index 1 contains `2`; it and every earlier position are too small, so `lo` moves to 2. Index 2 contains `5`, so `hi` becomes 2. The endpoints meet at 2, the first qualifying position. The important move occurs on equality: an exact search would return, but a lower-bound search keeps looking left.

```trace
{"cells":[2,2,5,5,5,9],"pointers":["lo","mid","hi"],"steps":[{"at":{"lo":0,"mid":3,"hi":6},"vars":{"value":5},"note":"Equality still belongs to the possible lower-bound suffix."},{"at":{"lo":0,"mid":1,"hi":3},"vars":{"value":2},"note":"This position is strictly too small."},{"at":{"lo":2,"mid":2,"hi":3},"vars":{"value":5},"note":"Equality still belongs to the possible lower-bound suffix."}]}
```

<!-- stage: code -->
### Change One Comparison

```java
static int lowerBound(int[] nums, int target) {
    int lo = 0, hi = nums.length;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] >= target) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}

static int upperBound(int[] nums, int target) {
    int lo = 0, hi = nums.length;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] > target) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}
```

Both methods take O(log n) time and O(1) space. Their only algorithmic difference is whether equality satisfies the predicate. The half-open convention also removes special handling for empty input and insertion after the last element. The return value is a position, not necessarily a valid array index, so callers must check it before reading `nums[result]`.

<!-- stage: applicability -->
### When The Answer Is A Boundary

Use a lower or upper bound when the output is an insertion position, the first value meeting an inequality, or the size of a sorted prefix. State the invariant in predicate language: every position before `lo` is false, and the first true position remains at or before `hi`. The false friend is exact search, which may stop at any equal value and returns failure when the target is absent. Bounds are defined even when the target is missing.

Choose the inequality from the contract. Lower bound uses `>=` and places a value before equals. Upper bound uses `>` and places it after equals. Their difference also counts occurrences: `upperBound(nums, x) - lowerBound(nums, x)` is the number of copies of `x`. In Java, retain the overflow-safe midpoint and remember that `nums.length` is a valid result but not an index.

<!-- stage: exercises -->
### Exercises

#### [Build] Search Insert Position (LeetCode 35)
<!-- id: bs-search-insert-position -->

**Prerequisites.** Exact binary search and the lower-bound invariant from this lesson.

**Problem.** Given a strictly increasing integer array `nums` and an integer `target`, return the index of `target` if it exists. Otherwise, return the index where `target` should be inserted to keep the array sorted. Your algorithm must run in O(log n) time.

**Constraints.** `1 <= nums.length <= 10^4`; `-10^4 <= nums[i], target <= 10^4`; `nums` is strictly increasing.

**Example 1.** Input `nums = [1,3,6,8]`, `target = 6`; output `2`.

**Example 2.** Input `nums = [1,3,6,8]`, `target = 5`; output `2`.

**Hint.** Search for the first value that is not smaller than `target`. The returned position is useful whether equality is found or not.

**Changed decision.** The search returns a boundary unconditionally instead of using `-1` for an absent target.

#### [Vary] Upper Bound (Author exercise)
<!-- id: bs-upper-bound -->

**Prerequisites.** The lower-bound implementation immediately above.

**Problem.** Given a nondecreasing integer array `nums` and a target, return the first index whose value is strictly greater than the target. Return `nums.length` if no such value exists.

**Constraints.** `0 <= nums.length <= 10^5`; values and `target` fit in `int`; require O(log n) time and O(1) space.

**Example 1.** Input `nums = [1,3,3,7]`, `target = 3`; output `3`.

**Example 2.** Input `nums = [2,4,8]`, `target = 8`; output `3`.

**Hint.** Decide whether equality belongs to the rejected prefix or the possible suffix. Only one comparison changes from lower bound.

**Changed decision.** Equal values now belong before the boundary, so the predicate is strict.

#### [Boundary] Outside Range (Author exercise)
<!-- id: bs-outside-range -->

**Prerequisites.** Half-open binary search and the `nums.length` return contract.

**Problem.** Given a nondecreasing array `nums` and an array of query values, return the lower-bound insertion position for every query. Queries may be smaller than every stored value or larger than every stored value.

**Constraints.** `0 <= nums.length <= 10^5`; `1 <= queries.length <= 10^4`; all values fit in `int`; target O(log n) time per query, excluding the output array.

**Example 1.** Input `nums = [4,9,13]`, `queries = [2,20]`; output `[0,3]`.

**Example 2.** Input `nums = []`, `queries = [-5,5]`; output `[0,0]`.

**Hint.** Let the exclusive endpoint participate in the search. Do not index the returned position merely to prove that it may equal `nums.length`.

**Changed decision.** Both legal sentinel boundaries, zero and `n`, must survive repeated queries and empty input.

#### [Recognize] Smallest Greater Letter (LeetCode 744)
<!-- id: bs-smallest-greater-letter -->

**Prerequisites.** Upper bound and modular wraparound.

**Problem.** Given a sorted array of lowercase letters and a target letter, return the smallest stored letter strictly greater than the target. If no stored letter is greater, return the first letter in the array.

**Constraints.** `2 <= letters.length <= 10^4`; `letters` is sorted and contains at least two distinct lowercase letters; `target` is lowercase.

**Example 1.** Input `letters = ['c','f','j']`, `target = 'd'`; output `'f'`.

**Example 2.** Input `letters = ['b','e','e','k']`, `target = 'k'`; output `'b'`.

**Hint.** First compute an ordinary upper bound. Which existing position should replace the legal boundary `letters.length`?

**Changed decision.** The first-greater boundary remains the core result, but the output contract wraps an exhausted suffix to index zero.
