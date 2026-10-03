<!-- lesson-kind: standard -->
<!-- lesson-id: arrays-sort -->
## Arrays Sort

<!-- stage: context -->
### Preserve The Raw Readings

A monitoring service receives a day's latency readings as an `int[]`. One report needs percentiles, which are easiest to compute from ordered values. A second report must replay the measurements in arrival order. If the percentile method sorts the caller's array directly, the replay report quietly receives different data.

The algorithmic question is simple, but the API decision is not: may the method rearrange the supplied array, or must it return a separate ordered sequence? Java provides the operation, yet the method still owns mutation, range, and output contracts.

<!-- stage: naive -->
### Insert Each Reading

One direct implementation keeps a sorted prefix. Each new reading shifts larger prefix values one position right, then enters the gap.

```java
static void insertionSort(int[] values) {
    for (int i = 1; i < values.length; i++) {
        int key = values[i];
        int j = i - 1;
        while (j >= 0 && values[j] > key) {
            values[j + 1] = values[j];
            j--;
        }
        values[j + 1] = key;
    }
}
```

The method is correct because each iteration extends an already ordered prefix by one value.

<!-- stage: bottleneck -->
### Reverse Input Forces Shifts

When the input is descending, the second reading shifts once, the third shifts twice, and the final reading shifts across the entire prefix. The total number of moves is `1 + 2 + ... + (n - 1)`. That makes the method O(n^2) time in the hostile case, even though nearly sorted inputs can be cheap.

At 100,000 readings, a reverse-ordered day would require roughly five billion shifts. The code also mutates its argument unconditionally. A library sort solves the general ordering work efficiently, but we still need to decide whether it receives the original array, a copy, or only a bounded range.

<!-- stage: insight -->
### Choose The Array Contract

For primitive values that need complete ascending order, Java provides **natural order** through `Arrays.sort(int[])`. The method rearranges the supplied array in place. It does not return a new one, so a caller that must retain the original sequence needs an explicit copy before the call.

<!-- names: natural order, half-open range, mutation contract -->

The overloaded range form uses a **half-open range**: `Arrays.sort(values, from, to)` may rearrange indices `from` through `to - 1`, while indices outside that range remain unchanged. This matches loop bounds and permits an empty range when `from == to`. Passing `to` as though it were inclusive sorts one unintended value or fails at the end of the array.

The **mutation contract** decides which call is correct. If the problem permits rearranging `nums`, pass it directly. If another result still needs arrival order, use `Arrays.copyOf` or `clone`, then sort the copy. The useful invariant is about the result, not Java's internal sorting algorithm: after the call, every adjacent pair in the chosen range is nondecreasing. Equal primitive values become adjacent, but no correctness argument should depend on preserving their former identities or positions.

<!-- stage: variables -->
### Range And Ownership

`input` remains caller-owned when preservation is required. `ordered` is the copied array that this method owns and may mutate. In a range call, `from` is inclusive and `to` is exclusive, so the sortable length is `to - from`. Indices below `from` and at or above `to` must retain their original values.

<!-- stage: trace -->
### Watch The Prefix Grow

The direct method on `[5, 2, 5, -1]` shows why a general library operation matters. The first `5` forms the initial ordered prefix. Taking `2` shifts that `5` right, then inserts `2` at index zero. The next `5` already belongs after the prefix, so no shift occurs.

The hostile step is the final `-1`. It moves past both copies of `5` and then past `2`, producing `[-1, 2, 5, 5]`. Equal values compare without a shift because the loop uses `>` rather than `>=`. That detail gives this insertion implementation stable behavior, but primitive `Arrays.sort` exposes no stability guarantee that a solution may rely on. This chapter will handle stability explicitly in Lesson 05.

```trace
{"cells":[5,2,5,-1],"pointers":["sorted","scan"],"steps":[{"at":{"sorted":0,"scan":0},"vars":{"key":5},"note":"A one-value prefix is already ordered."},{"at":{"sorted":0,"scan":1},"vars":{"key":2},"note":"Take 2; indices 0 through 0 are the ordered prefix."},{"at":{"sorted":1,"scan":0},"vars":{"key":2},"note":"Shift 5 right because it is greater than 2."},{"at":{"sorted":1,"scan":0},"vars":{"key":2},"note":"Insert 2; indices 0 through 1 are ordered."},{"at":{"sorted":1,"scan":2},"vars":{"key":5},"note":"Take 5; indices 0 through 1 are the ordered prefix."},{"at":{"sorted":2,"scan":2},"vars":{"key":5},"note":"Insert 5; indices 0 through 2 are ordered."},{"at":{"sorted":2,"scan":3},"vars":{"key":-1},"note":"Take -1; indices 0 through 2 are the ordered prefix."},{"at":{"sorted":3,"scan":2},"vars":{"key":-1},"note":"Shift 5 right because it is greater than -1."},{"at":{"sorted":3,"scan":1},"vars":{"key":-1},"note":"Shift 5 right because it is greater than -1."},{"at":{"sorted":3,"scan":0},"vars":{"key":-1},"note":"Shift 2 right because it is greater than -1."},{"at":{"sorted":3,"scan":0},"vars":{"key":-1},"note":"Insert -1; indices 0 through 3 are ordered."}]}
```

<!-- stage: code -->
### Sort Only What You Own

```java
static int[] sortedCopy(int[] input) {
    int[] ordered = input.clone();
    java.util.Arrays.sort(ordered);
    return ordered;
}

static int[] withSortedRange(int[] input, int from, int to) {
    int[] result = input.clone();
    java.util.Arrays.sort(result, from, to);
    return result;
}
```

Both methods make ownership visible. The first orders every copied value. The second changes only `[from, to)`, relying on the stated valid-bound contract rather than adding unrelated defensive behavior. Copying costs O(n) time and O(n) returned space. The sort costs O(n log n) time for the complete array, or O(r log r) for a range of length `r`; the explicit copy remains O(n) in either method.

<!-- stage: applicability -->
### When It Applies

Use `Arrays.sort(int[])` when primitive integers need their complete natural order and the method may mutate the chosen array. The invariant is that every adjacent pair in the sorted region is nondecreasing, while every index outside a range call is unchanged. That invariant unlocks later scans for equal runs, gaps, and local minima.

The false friend is a custom order. The `int[]` overload accepts no comparator; box the values or sort records when the decision is not natural ascending order. A second false friend is a problem that requires the original indices. Sorting raw values destroys that association unless you store values with their indices first.

This technique silently fails at the API boundary when `to` is treated as inclusive or when a supposedly read-only method sorts its argument. Empty arrays and singleton arrays are already ordered, and the library handles them without special branches. Extreme integer values are also safe under natural ordering because no user-written subtraction comparator is involved.

<!-- stage: exercises -->
### Exercises

#### [Build] Sort A Primitive Copy (Author exercise)
<!-- id: sort-primitive-copy -->

**Prerequisites.** Array cloning and the mutation contract from this lesson.

**Problem.** Given an `int[] nums`, return a new array containing the same values in nondecreasing order. The input array must remain byte-for-byte unchanged.

**Constraints.** `0 <= nums.length <= 10^5` and each value is a signed 32-bit integer. Target O(n log n) time.

**Example 1.** Input `nums = [9, -4, 9, 1]`, output `[-4, 1, 9, 9]`; the original remains `[9, -4, 9, 1]`.

**Example 2.** Input `nums = []`, output `[]`; copying an empty array produces an independent empty result.

**Hint.** Which operation establishes ownership before the mutating library call? Test both the returned values and the untouched input.

**Changed decision.** The method preserves caller order by sorting storage that it owns.

#### [Vary] Sort A Subrange (Author exercise)
<!-- id: sort-array-subrange -->

**Prerequisites.** The Build exercise and half-open interval notation.

**Problem.** Given `nums`, `from`, and `to`, return a copy in which only indices in `[from, to)` are sorted in nondecreasing order. Values outside the range must remain at their original indices.

**Constraints.** `0 <= nums.length <= 10^5` and `0 <= from <= to <= nums.length`. Target O(n + r log r) time for range length `r`.

**Example 1.** Input `nums = [8, 5, 3, 7, 1]`, `from = 1`, `to = 4`, output `[8, 3, 5, 7, 1]`.

**Example 2.** Input `nums = [4, 2]`, `from = 1`, `to = 1`, output `[4, 2]`; an empty range changes nothing.

**Hint.** Write down the first index excluded from the operation before calling the API. Which two slices must compare equal to the original afterward?

**Changed decision.** Only one half-open region is owned by the sorting operation.

#### [Boundary] Empty, Singleton, And Extreme Values (Author exercise)
<!-- id: sort-boundary-values -->

**Prerequisites.** The preceding two exercises and Java's signed integer range.

**Problem.** Return an ascending copy of an integer array that may be empty, contain one value, or contain either 32-bit extreme. Do not add a subtraction-based comparator or special-case the extreme values.

**Constraints.** `0 <= nums.length <= 10^5`; each entry lies from `Integer.MIN_VALUE` through `Integer.MAX_VALUE`. Target O(n log n) time.

**Example 1.** Input `nums = [2147483647, 0, -2147483648]`, output `[-2147483648, 0, 2147483647]`.

**Example 2.** Input `nums = [42]`, output `[42]`; a singleton requires no movement.

**Hint.** The primitive overload already knows natural integer order. Which extra comparator code would add risk without adding information?

**Changed decision.** Hostile sizes and values test the library contract instead of introducing new sorting logic.

#### [Recognize] Contains Duplicate (LeetCode 217)
<!-- id: sort-contains-duplicate -->

**Prerequisites.** Sorted copies and an adjacent scan.

**Problem.** Given an integer array `nums`, return `true` when some value occurs at least twice; otherwise return `false`. Preserve the input and solve this version by sorting rather than with a set.

**Constraints.** `1 <= nums.length <= 10^5` and `-10^9 <= nums[i] <= 10^9`. Target O(n log n) time.

**Example 1.** Input `nums = [11, 3, 5, 11]`, output `true`; sorting makes the two `11` values adjacent.

**Example 2.** Input `nums = [-2, 0, 7, 9]`, output `false`; no adjacent pair is equal after sorting.

**Hint.** Once equal values form one contiguous run, how many neighboring pairs must the scan inspect before it can return?

**Changed decision.** The ordered array is now preprocessing for a local equality test rather than the final output.

