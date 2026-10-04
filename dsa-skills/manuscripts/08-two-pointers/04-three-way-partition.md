<!-- lesson-kind: standard -->
<!-- lesson-id: three-way-partition -->
## Three-Way Partition

<!-- stage: context -->
### Three Final Regions

Suppose records are classified as below, equal to, or above a threshold. A two-way partition can separate one category, but applying it twice makes the boundaries harder to reason about and may revisit values. We want a single pass in which every inspected record immediately joins a final region while one contiguous interval remains unresolved. No category needs internal ordering.

<!-- stage: naive -->
### Count Then Rewrite

For the special values 0, 1, and 2, count each value and overwrite the array with the required numbers of each. That is linear, but it depends on a tiny known value domain and does not generalize to partitioning arbitrary objects around a pivot. Sorting is another valid answer, but it costs O(n log n).

<!-- stage: bottleneck -->
### General Categories

Repeated two-way partitions still cost O(n), but they classify the middle region indirectly and complicate a one-pass contract. General sorting performs O(n log n) comparisons even though no order is required inside any category. A direct one-pass method should inspect each unresolved value once, except when a swap brings in an uninspected value that must be examined next.

<!-- stage: insight -->
### Maintain Four Regions

Keep `low` at the first middle slot, `mid` at the next unresolved value, and `high` at the last unresolved value. Values before `low` are low; values from `low` to `mid-1` are middle; values from `mid` through `high` are unresolved; values after `high` are high.

<!-- names: Dutch national flag, unresolved region -->

This **Dutch national flag** partition reacts to `a[mid]`. A low value swaps with `a[low]`, then both `low` and `mid` advance. A middle value only advances `mid`. A high value swaps with `a[high]` and decrements `high`, but `mid` does not move because the incoming value belongs to the **unresolved region**. That last rule is the common correctness bug. Every action shrinks the unresolved interval, so the algorithm is O(n). The proof checks all four region definitions after each branch.

<!-- stage: variables -->
### Four Region Invariant

`[0,low)` contains low-category values. `[low,mid)` contains middle values. `[mid,high]` has not been classified, and `(high,n)` contains high values. The loop continues while `mid <= high`. A swap with `low` is safe because the value at `low` is middle whenever `low < mid`; both resulting positions are understood.

<!-- stage: trace -->
### Reinspect The Incoming Value

Start with `[2,0,2,1,1,0]`. At `mid = 0`, swap 2 with the final 0 and decrement `high`; do not advance `mid`. The incoming 0 is then swapped into the low region, moving both `low` and `mid`. Another 0 is placed low, while a 2 later swaps toward the high region. Values equal to 1 simply enlarge the middle region.

The crucial moment is the first high swap. Advancing `mid` there would skip the incoming 0 and leave it outside the certified low region. Reinspection is not wasted work; it is how the algorithm preserves the invariant. Eventually `mid` passes `high`, leaving no unclassified value.

```trace
{"cells":[2,0,2,1,1,0],"pointers":["low","mid","high"],"steps":[{"at":{"low":0,"mid":0,"high":5},"vars":{"value":2},"note":"Swap the high value with index 5; keep mid in place."},{"at":{"low":0,"mid":0,"high":4},"vars":{"value":0},"note":"Reinspect the incoming zero and place it in the low region."},{"at":{"low":1,"mid":1,"high":4},"vars":{"value":0},"note":"Place the next zero and advance both front boundaries."},{"at":{"low":2,"mid":2,"high":4},"vars":{"value":2},"note":"Move this two to the high region and reinspect index 2."},{"at":{"low":2,"mid":4,"high":3},"vars":{"value":1},"note":"Middle values advance mid until the unresolved region is empty."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java run
public final class FlagPartition {static void sort(int[]a){int low=0,mid=0,high=a.length-1;while(mid<=high){if(a[mid]==0){int t=a[low];a[low++]=a[mid];a[mid++]=t;}else if(a[mid]==1)mid++;else{int t=a[mid];a[mid]=a[high];a[high--]=t;}}}public static void main(String[]z){int[]a={2,0,2,1,1,0};sort(a);if(!java.util.Arrays.equals(a,new int[]{0,0,1,1,2,2}))throw new AssertionError();}}
```

This implementation assumes every value is 0, 1, or 2. A general pivot version branches on `<`, `==`, and `>` instead. It uses O(1) extra space, performs only a linear number of region changes, and allocates no category buffers.

<!-- stage: applicability -->
### When It Applies

Use three-way partitioning when all values belong to low, middle, or high categories and order inside a category does not matter. The invariant must name all four regions, especially the still-unresolved interval. It is useful for color sorting and duplicate-friendly quicksort partitions.

The false friend is a two-way partition, which cannot certify an equality region in the same pass. Stable grouping is another false friend: endpoint swaps do not preserve encounter order. Finally, do not advance `mid` after taking from `high`; only a value moved from the processed front is known, while a value from the back remains unclassified.

<!-- stage: exercises -->
### Exercises

#### [Build] Partition 0,1,2 (Author exercise)
<!-- id: tp-partition-012 -->

**Prerequisites.** The four-region invariant from this lesson.

**Problem.** Rearrange an array containing only 0, 1, and 2 into nondecreasing order in one pass and constant auxiliary space.

**Constraints.** `0 <= nums.length <= 10^5`; every value is 0, 1, or 2.

**Example 1.** Input `nums = [2,0,1]`; output `[0,1,2]`.

**Example 2.** Input `nums = []`; output `[]`.

**Hint.** Write down the exact half-open ranges certified by `low`, `mid`, and `high` before coding.

**Changed decision.** This first rung implements only category movement and region maintenance.

#### [Vary] Sort Colors (LeetCode 75)
<!-- id: tp-sort-colors -->

**Prerequisites.** One-pass Dutch national flag partitioning.

**Problem.** Sort red, white, and blue objects encoded as 0, 1, and 2 in place without using a library sort.

**Constraints.** `1 <= nums.length <= 300`; every element is 0, 1, or 2.

**Example 1.** Input `nums = [2,0,2,1,1,0]`; output `[0,0,1,1,2,2]`.

**Example 2.** Input `nums = [1]`; output `[1]`.

**Hint.** Treat 1 as the already-correct middle category rather than swapping it.

**Changed decision.** Apply the abstract regions to the formal in-place color contract.

#### [Boundary] Reinspect Swapped High (Author exercise)
<!-- id: tp-reinspect-high -->

**Prerequisites.** The distinction between processed and unresolved values.

**Problem.** Sort a 0/1/2 array and also return how many times a value swapped from `high` had to be inspected at `mid` before that position advanced.

**Constraints.** `1 <= nums.length <= 100`; all values are valid categories.

**Example 1.** Input `nums = [2,0]`; output sorted `[0,2]` and reinspection count `1`.

**Example 2.** Input `nums = [0,1]`; output sorted `[0,1]` and reinspection count `0`.

**Hint.** Increment the counter on the high branch, where `mid` deliberately remains fixed.

**Changed decision.** The output exposes the branch most likely to be implemented incorrectly.

#### [Recognize] Three-Way Pivot Partition (Author exercise)
<!-- id: tp-three-way-pivot -->

**Prerequisites.** Category replacement by comparisons with a pivot.

**Problem.** Rearrange an integer array into values less than `pivot`, equal to `pivot`, and greater than `pivot`; return the inclusive bounds of the equal region.

**Constraints.** `0 <= nums.length <= 10^5`; all integers are allowed.

**Example 1.** Input `nums = [4,2,4,7,1]`, `pivot = 4`; output bounds `[2,3]` for one valid arrangement `[2,1,4,4,7]`.

**Example 2.** Input `nums = [1,2]`, `pivot = 5`; output bounds `[2,1]`, representing an empty equal region.

**Hint.** At termination, `low` starts the equal region and `high` ends it, even when that region is empty.

**Changed decision.** Literal colors become relational categories, and the boundary becomes part of the result.
