<!-- lesson-kind: standard -->
<!-- lesson-id: read-and-write -->
## Read And Write

<!-- stage: context -->
### Compact In Place

An array-backed API must sometimes filter values without allocating another array. The array itself cannot shrink, so the method returns a length `k` and promises that only `nums[0..k-1]` contains the retained result. One position reads every original value; another identifies where the next accepted value belongs. The difficult part is stating exactly which prefix is already final while the scan is still running.

<!-- stage: naive -->
### Allocate A Result

The obvious solution appends retained values to a new list and copies them back. It is clear and stable, but it uses O(n) additional memory and performs a second pass. A second in-place attempt that removes an element by shifting the suffix avoids the list but can move the same values repeatedly.

<!-- stage: bottleneck -->
### Shifting The Suffix

Deleting at index `i` by shifting every later value left costs O(n-i). If many early values are removed, the total becomes O(n²), and a value near the end may be copied almost `n` times. The output only needs each retained value once. Repeated suffix repair does work that a direct destination index can avoid.

The waste grows precisely when filtering removes many values.

<!-- stage: insight -->
### Build A Certified Prefix

Let `read` visit every original position exactly once. Let `write` equal the number of accepted values seen so far, which is also the destination of the next accepted value. When `nums[read]` passes the admission rule, assign it to `nums[write]` and increment `write`. Rejected values change no output state.

<!-- names: read pointer, write pointer, stable compaction -->

The **read pointer** owns traversal, and the **write pointer** owns output construction. Together they perform **stable compaction** because retained values are written in encounter order. Before each read, `nums[0..write-1]` is the final filtered version of the already inspected prefix. Since `write <= read`, a write never destroys unread input. Each original value is inspected once and written at most once.

This separates two concerns cleanly: the admission predicate decides what survives, while pointer movement decides where a survivor is stored. Changing the predicate does not change the proof that the prefix is safe.

<!-- stage: variables -->
### Prefix State

`read` identifies the next source element. `write` is both the retained count and the first unused output slot. The admission rule may compare with a supplied value, zero, or the already written prefix. After the loop, `write` is the returned logical length; positions from `write` onward are intentionally unspecified unless the problem explicitly requests suffix repair.

<!-- stage: trace -->
### Keeping Nonzero Values

Scan `[0, 4, 0, 3, 3]`. At read index 0, zero is rejected and the empty written prefix remains valid. At index 1, write 4 at position 0 and advance `write` to 1. The zero at index 2 is rejected. Values 3 at indices 3 and 4 are accepted into positions 1 and 2.

The scan finishes with logical prefix `[4, 3, 3]` and length 3. Old values beyond that length do not belong to the filtered result. If the contract is Move Zeroes instead, a second phase fills those positions with zero; that suffix repair is a separate promise.

```trace
{"cells":[0,4,0,3,3],"pointers":["read","write"],"steps":[{"at":{"read":0,"write":0},"vars":{"kept":0},"note":"Reject zero; the output prefix stays empty."},{"at":{"read":1,"write":0},"vars":{"kept":0},"note":"Accept 4 and write it at output position 0."},{"at":{"read":2,"write":1},"vars":{"kept":1},"note":"Reject the second zero without shifting a suffix."},{"at":{"read":3,"write":1},"vars":{"kept":1},"note":"Accept 3 into output position 1."},{"at":{"read":4,"write":2},"vars":{"kept":2},"note":"Accept the final 3; the logical result length becomes 3."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java run
public final class StableFilter {
 static int remove(int[] a,int value){int write=0;for(int read=0;read<a.length;read++)if(a[read]!=value)a[write++]=a[read];return write;}
 public static void main(String[]z){int[]a={3,2,2,3};int k=remove(a,3);if(k!=2||a[0]!=2||a[1]!=2)throw new AssertionError();}
}
```

The O(n) scan uses O(1) auxiliary space. It does not promise anything about the suffix. Avoid clearing it unless the contract requires that work, because callers must ignore every position at or beyond the returned logical length.

<!-- stage: applicability -->
### When It Applies

Use read/write pointers when one pass decides whether each item belongs in an in-place logical output. The invariant is that the written prefix already equals the final answer for the consumed input prefix. This covers filtering, stable movement, and capped duplicate retention.

The false friend is a sliding window. A window’s left edge removes values from active range state; a write pointer constructs permanent output. Another false friend is unstable partitioning. If output order does not matter, swaps from both ends may use fewer writes. Read the mutation and order guarantees before selecting either form.

<!-- stage: exercises -->
### Exercises

#### [Build] Remove Element (LeetCode 27)
<!-- id: tp-remove-element -->

**Prerequisites.** Logical array length and stable read/write compaction.

**Problem.** Given an integer array `nums` and value `val`, remove every occurrence in place and return the count `k` of retained values. The first `k` positions must hold the result; the suffix is unspecified.

**Constraints.** `0 <= nums.length <= 100`; each value and `val` is between 0 and 100.

**Example 1.** Input `nums = [3,2,2,3]`, `val = 3`; output `2`, with prefix `[2,2]`.

**Example 2.** Input `nums = []`, `val = 4`; output `0`.

**Hint.** Make the write index count accepted values rather than deleted values.

**Changed decision.** The API returns a logical prefix instead of a new array.

#### [Vary] Move Zeroes (LeetCode 283)
<!-- id: tp-move-zeroes -->

**Prerequisites.** Stable compaction and explicit suffix contracts.

**Problem.** Move every zero to the end of `nums` in place while preserving the relative order of nonzero values. Return nothing.

**Constraints.** `1 <= nums.length <= 10^4`; values fit in a signed 32-bit integer.

**Example 1.** Input `nums = [0,1,0,3,12]`; output `[1,3,12,0,0]`.

**Example 2.** Input `nums = [0]`; output `[0]`.

**Hint.** Compact the nonzero prefix first, then fill every remaining output slot with zero.

**Changed decision.** The suffix is now specified and requires a repair phase after compaction.

#### [Boundary] Remove Duplicates (LeetCode 26)
<!-- id: tp-remove-sorted-duplicates -->

**Prerequisites.** Sorted runs and a written-prefix invariant.

**Problem.** Given a nondecreasing array, keep one copy of each distinct value in place and return the logical length of the unique prefix.

**Constraints.** `1 <= nums.length <= 3 * 10^4`; values are nondecreasing.

**Example 1.** Input `nums = [1,1,2]`; output `2`, with prefix `[1,2]`.

**Example 2.** Input `nums = [5]`; output `1`, with prefix `[5]`.

**Hint.** A new value differs from the last value already accepted, not necessarily from an arbitrary output slot.

**Changed decision.** Admission depends on the retained prefix rather than a fixed forbidden value.

#### [Recognize] Remove Duplicates II (LeetCode 80)
<!-- id: tp-remove-duplicates-two -->

**Prerequisites.** Capped run retention and safe access to the written prefix.

**Problem.** Given a nondecreasing array, keep at most two copies of every value in place and return the logical result length.

**Constraints.** `1 <= nums.length <= 3 * 10^4`; values are sorted in nondecreasing order.

**Example 1.** Input `nums = [1,1,1,2,2,3]`; output `5`, with prefix `[1,1,2,2,3]`.

**Example 2.** Input `nums = [7,7]`; output `2`.

**Hint.** Once two values are written, compare a candidate with the value two output positions behind it.

**Changed decision.** The admission rule retains a bounded number of equal values instead of only one.
