<!-- lesson-kind: standard -->
<!-- lesson-id: two-way-partition -->
## Two-Way Partition

<!-- stage: context -->
### Separate Two Categories

A scheduler stores urgent and ordinary job identifiers in one array. It needs urgent jobs before ordinary jobs, but it does not care about order inside either group. Stable compaction could copy every item and later repair a suffix. The weaker order contract permits a different approach: find a misplaced item at each end and exchange them, making two final placements with one swap.

<!-- stage: naive -->
### Collect Then Copy

One direct method writes the first category to a temporary array, then the second category, and finally copies the result back. It is linear and simple, but it consumes O(n) extra space. A stable in-place shift avoids allocation yet can take O(n²) time when each newly found first-category item crosses a long block.

<!-- stage: bottleneck -->
### Preserve Only Required Order

Both naive methods preserve more information than the contract asks for. Internal order inside the two groups is irrelevant, yet stable shifting pays for it with repeated writes. In the alternating worst case, long shifts produce O(n²) assignments. Even the temporary-array version writes every value twice. We need only certify which side of one boundary each processed item occupies.

<!-- stage: insight -->
### Swap Misplaced Endpoints

Keep `left` at the first unresolved position from the front and `right` at the first unresolved position from the back. Advance `left` over values already belonging to the first region. Retreat `right` over values already belonging to the second. If the pointers have not crossed, both stopped values are misplaced, so swapping them finalizes one position in each region.

<!-- names: two-way partition, region boundary -->

This is a **two-way partition**. The pointers define a moving **region boundary**: everything before `left` belongs to the first category, everything after `right` belongs to the second, and the closed interval remains unresolved. The swap is safe only because relative order is not promised. Each pointer moves monotonically, giving O(n) inspections and O(1) extra space.

Termination follows because every scan or swap reduces the unresolved interval.

<!-- stage: variables -->
### Three Regions

`left` begins at zero and `right` at `n-1`. The prefix `[0,left)` satisfies the first predicate; the suffix `(right,n)` satisfies its complement. The middle `[left,right]` has not been classified. After a swap, increment `left` and decrement `right` because both incoming values have just been placed in their correct regions.

<!-- stage: trace -->
### Parity Partition

Partition `[3, 2, 4, 1, 6]` so even values come first. The left pointer stops immediately at 3, while the right pointer stops at 6. Swap them, producing `[6,2,4,1,3]`; both endpoints are final. The left scan now passes 2 and 4. The right scan stops at 1. Once the pointers meet or cross, there is no misplaced pair left to exchange.

The result is not a sort. `[6,2,4]` is a valid even region even though it is not ordered. That distinction prevents accidental promises and unnecessary work.

An input already partitioned performs no swaps; both scans simply certify their regions. An all-even input advances `left` beyond `right`, which is why every inner scan checks the crossing condition before dereferencing.

```trace
{"cells":[3,2,4,1,6],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":4},"vars":{"swaps":0},"note":"Both endpoints are in the wrong regions, so swap 3 and 6."},{"at":{"left":1,"right":3},"vars":{"swaps":1},"note":"Position 0 is even and position 4 is odd; both are final."},{"at":{"left":2,"right":3},"vars":{"swaps":1},"note":"Advance across the even value 2."},{"at":{"left":3,"right":3},"vars":{"swaps":1},"note":"Advance across 4; the unresolved interval is exhausted."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java run
public final class ParityPartition {
 static void apply(int[]a){int l=0,r=a.length-1;while(l<=r){while(l<=r&&(a[l]&1)==0)l++;while(l<=r&&(a[r]&1)!=0)r--;if(l<r){int t=a[l];a[l++]=a[r];a[r--]=t;}}}
 public static void main(String[]z){int[]a={3,2,4,1,6};apply(a);boolean odd=false;for(int x:a){if((x&1)!=0)odd=true;else if(odd)throw new AssertionError();}}
}
```

The bit test works for negative odd numbers as well. A remainder test `x % 2 == 1` would fail for negative odds because Java returns `-1`. The crossing checks also prevent either inner scan from reading past the array.

<!-- stage: applicability -->
### When It Applies

Choose two-way partitioning when output needs two contiguous categories and internal order is explicitly irrelevant. The invariant is that the prefix and suffix are already final while only the interval between the pointers remains unresolved. A predicate and its complement should classify every value.

The false friend is stable filtering or grouping. If equal-priority jobs must retain arrival order, swapping endpoints violates the contract; use read/write compaction or auxiliary storage. Another false friend is three-way classification. A pivot with less-than, equal-to, and greater-than regions needs an additional boundary and different handling for the unresolved value.

<!-- stage: exercises -->
### Exercises

#### [Build] Sort Array By Parity (LeetCode 905)
<!-- id: tp-sort-parity -->

**Prerequisites.** Complementary predicates and endpoint swaps.

**Problem.** Rearrange an integer array in place so every even value appears before every odd value. Any valid internal order is accepted.

**Constraints.** `1 <= nums.length <= 5000`; `0 <= nums[i] <= 5000`. Target O(n) time.

**Example 1.** Input `nums = [3,1,2,4]`; output could be `[4,2,1,3]`.

**Example 2.** Input `nums = [2,4]`; output `[2,4]`.

**Hint.** Stop each endpoint only on a value that belongs on the other side.

**Changed decision.** Internal order is discarded, which makes paired endpoint swaps legal.

#### [Vary] Partition Around Pivot (Author exercise)
<!-- id: tp-partition-pivot -->

**Prerequisites.** Two-region invariants and comparisons against a pivot.

**Problem.** Rearrange `nums` so every value smaller than `pivot` precedes every value greater than or equal to it. Return the first index of the second region.

**Constraints.** `0 <= nums.length <= 10^5`; values and `pivot` fit in signed 32-bit integers.

**Example 1.** Input `nums = [5,1,7,3]`, `pivot = 4`; output boundary `2`, with a valid array such as `[3,1,7,5]`.

**Example 2.** Input `nums = [1,2]`, `pivot = 5`; output boundary `2`.

**Hint.** On termination, the left pointer is the first position that does not belong to the low region.

**Changed decision.** The method must return its final boundary in addition to mutating the array.

#### [Boundary] One Empty Region (Author exercise)
<!-- id: tp-empty-region -->

**Prerequisites.** Crossing-pointer termination.

**Problem.** Apply an in-place parity partition and return the count of even values. Correctly handle inputs in which either the even region or odd region is empty.

**Constraints.** `0 <= nums.length <= 10^5`; values may be negative.

**Example 1.** Input `nums = [2,4,6]`; output `3`.

**Example 2.** Input `nums = [-3,-1]`; output `0`.

**Hint.** The final left boundary equals the size of the first region even when no swap occurs.

**Changed decision.** All elements can satisfy the same category, so scanning must stop safely at array boundaries.

#### [Recognize] Sort Array By Parity II (LeetCode 922)
<!-- id: tp-parity-indices -->

**Prerequisites.** Position classes and paired correction.

**Problem.** Rearrange an equal-count array so every even index stores an even value and every odd index stores an odd value.

**Constraints.** `2 <= nums.length <= 2 * 10^4`; the input contains equally many even and odd values.

**Example 1.** Input `nums = [4,2,5,7]`; output could be `[4,5,2,7]`.

**Example 2.** Input `nums = [2,3]`; output `[2,3]`.

**Hint.** Advance one pointer through even indices and the other through odd indices, stopping only at misplaced values.

**Changed decision.** Destination index parity, rather than a single contiguous boundary, defines the two regions.
