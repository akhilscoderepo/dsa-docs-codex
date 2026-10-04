<!-- lesson-kind: standard -->
<!-- lesson-id: exact-search -->
## Exact Search

<!-- stage: context -->
### A Known Identifier

A service keeps completed job identifiers in ascending order because it writes a compact daily index. Support asks whether job `13` is present and, if so, where it appears. Scanning from the beginning works, but it ignores the strongest fact in the contract: once we inspect a value, the ordering tells us that an entire side cannot contain the target. The task is an exact lookup, so the method returns one matching index or `-1` when the value is absent.

<!-- stage: naive -->
### Start With A Scan

The direct method checks every position until it finds the requested identifier. It is correct for any array, sorted or not, and gives us a useful baseline against which the ordered version can be measured.

```java
static int linearFind(int[] nums, int target) {
    for (int i = 0; i < nums.length; i++) {
        if (nums[i] == target) return i;
    }
    return -1;
}
```

<!-- stage: bottleneck -->
### Work We Can Eliminate

Suppose the array contains one million increasing identifiers and the requested value is missing near the upper end. The scan performs one million comparisons. After checking a middle value such as `400000`, however, every smaller identifier is immediately irrelevant when the target is larger. The scan still visits that proved-impossible prefix. Its O(n) time becomes visible at scale, while the sorted contract contains enough evidence to halve the remaining work after each comparison.

<!-- stage: insight -->
### Preserve The Possible Interval

**Binary search** keeps an inclusive **search interval** `[lo, hi]`. Its invariant is conditional but precise: if the target exists, some occurrence remains inside that interval. Inspect `mid = lo + (hi - lo) / 2`. Equality finishes the lookup. If `nums[mid] < target`, sortedness proves that indices `lo..mid` are too small, so the next interval begins at `mid + 1`. If `nums[mid] > target`, indices `mid..hi` are too large, so `hi` becomes `mid - 1`.

<!-- names: binary search, search interval -->

Both unequal branches remove `mid`, which matters: keeping it would allow a one-element interval to repeat forever. When `lo > hi`, the interval is empty and the invariant proves absence. The safe midpoint avoids overflow that `(lo + hi) / 2` could cause for large indices. Sortedness is the property that makes every discarded half impossible rather than merely unlikely.

<!-- stage: variables -->
### State The Boundaries

`lo` and `hi` are inclusive endpoints of the positions still under consideration. `mid` is recalculated inside that interval on every iteration. `target` never changes. The method returns as soon as equality is observed; otherwise crossing endpoints represents an empty interval and produces `-1`.

<!-- stage: trace -->
### Three Comparisons

Search for `13` in `[-8,-1,4,9,13,21,34]`. Initially every index is possible. The first midpoint is index 3 with value 9. Since 9 is too small, indices 0 through 3 are discarded together; none can equal 13 in an increasing array. The next midpoint is index 5 with value 21, so indices 5 and 6 are too large. Only index 4 remains. Its value is 13, and the method returns 4. Notice that neither discarded region is revisited and every unequal comparison removes the inspected midpoint. Had index 4 also failed, the appropriate endpoint would cross the other one, explicitly representing that no candidates remain.

```trace
{"cells":[-8,-1,4,9,13,21,34],"pointers":["lo","mid","hi"],"steps":[{"at":{"lo":0,"mid":3,"hi":6},"vars":{"value":9},"note":"Compare index 3 with target 13."},{"at":{"lo":4,"mid":5,"hi":6},"vars":{"value":21},"note":"Compare index 5 with target 13."},{"at":{"lo":4,"mid":4,"hi":4},"vars":{"value":13},"note":"Compare index 4 with target 13."}]}
```

<!-- stage: code -->
### The Exact Loop

```java
static int binarySearch(int[] nums, int target) {
    int lo = 0, hi = nums.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return mid;
        if (nums[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
```

The empty array starts with `hi = -1`, so the loop correctly does no indexing. Each comparison cuts away at least one position, giving O(log n) time and O(1) extra space. No defensive sorting belongs here: sorting would mutate or copy the input and would change both the contract and the cost.

<!-- stage: applicability -->
### When Exact Search Fits

Use this form when the input is ordered and any matching index is acceptable. Say the invariant aloud: if the target exists, it remains in inclusive interval `[lo, hi]`. The false friend is an unsorted collection; a comparison there gives no proof about either side. Another false friend is an insertion-position or first-occurrence request, because returning on equality loses the boundary information. In Java, keep the overflow-safe midpoint even though ordinary arrays rarely approach the maximum index. Silent failure usually comes from using `lo = mid` or `hi = mid`, which may stop shrinking.

<!-- stage: exercises -->
### Exercises

#### [Build] Binary Search (LeetCode 704)
<!-- id: bs-exact-target -->

**Prerequisites.** Sorted arrays, inclusive intervals, and the invariant from this lesson.

**Problem.** Given a strictly increasing integer array `nums` and an integer `target`, return the index containing `target`. Return `-1` if the value does not occur.

**Constraints.** `1 <= nums.length <= 10^4`; values and target fit in `int`; target O(log n) time.

**Example 1.** Input `nums = [-7,-2,3,8,14]`, `target = 8`; output `3` because index 3 stores 8.

**Example 2.** Input `nums = [6]`, `target = 2`; output `-1` because the only position is too large.

**Hint.** Write the meaning of `[lo, hi]` before the loop. Which endpoint moves when the middle value is smaller than the target?

**Changed decision.** This first rung implements the inclusive exact-match loop without another output requirement.

#### [Vary] Descending Search (Author exercise)
<!-- id: bs-descending-target -->

**Prerequisites.** Exact search and careful interpretation of the ordering contract.

**Problem.** Given a strictly decreasing integer array and a target, return its index or `-1` when absent without reversing or copying the array.

**Constraints.** `0 <= nums.length <= 10^5`; all elements are distinct; use O(log n) time and O(1) space.

**Example 1.** Input `nums = [20,13,9,4,-1]`, `target = 9`; output `2`.

**Example 2.** Input `nums = [5,1]`, `target = 7`; output `-1` because 7 lies above the descending range.

**Hint.** In descending order, a middle value smaller than the target points toward which side? Keep the interval convention unchanged and reverse only the movement rule.

**Changed decision.** The data order reverses, so comparison signs no longer imply the same endpoint update.

#### [Boundary] Two Elements (Author exercise)
<!-- id: bs-two-element-proof -->

**Prerequisites.** Inclusive endpoint movement and termination reasoning.

**Problem.** Search a sorted array whose length is at most two, returning a matching index or `-1`. The implementation must use the general exact-search loop rather than special cases.

**Constraints.** `0 <= nums.length <= 2`; elements are distinct and increasing; O(log n) target time.

**Example 1.** Input `nums = [1,3]`, `target = 3`; output `1` after the right position remains alone.

**Example 2.** Input `nums = [1,3]`, `target = 2`; output `-1` after both endpoints are discarded.

**Hint.** Trace the one-element interval reached after the first comparison. Does every unequal branch remove `mid` itself?

**Changed decision.** Tiny inputs expose whether endpoint updates strictly shrink the inclusive interval.

#### [Recognize] Search A Row-Major Matrix (LeetCode 74)
<!-- id: bs-recognize-row-major -->

**Prerequisites.** Exact search and matrix row-column index conversion from Chapter 02.

**Problem.** Given a non-empty matrix whose rows are increasing and whose first value in each row exceeds the previous row's last value, report whether `target` occurs using O(log(rows * cols)) time.

**Constraints.** `1 <= rows, cols <= 100`; all matrix values are distinct integers; do not flatten or copy the matrix.

**Example 1.** Input `matrix = [[1,4,7],[10,13,18]]`, `target = 13`; output `true`.

**Example 2.** Input `matrix = [[2,5],[9,12]]`, `target = 6`; output `false`.

**Hint.** Imagine one sorted array of length `rows * cols`. How do quotient and remainder translate its middle index back to a cell?

**Changed decision.** The ordered positions are virtual, so indexing changes while the exact-search invariant remains intact.
