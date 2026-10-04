<!-- lesson-kind: standard -->
<!-- lesson-id: range-queries -->
## Range Queries

<!-- stage: context -->
### One Array Many Questions

A billing ledger is frozen at the end of the day, but analysts ask thousands of questions about it: total charges from record 20 through 80, then 4 through 11, then the whole day. The values do not change between questions. Scanning each requested interval works, yet it spends time rediscovering totals that preprocessing could preserve once for every future request.

<!-- stage: naive -->
### Walk Each Requested Range

The straightforward method visits every value named by a query. It is correct and often best for a single question. The loop mirrors the inclusive contract directly, so there is little room for an endpoint mistake.

```java run
public final class RangeNaive {
    static long sum(int[] a,int left,int right){long s=0;for(int i=left;i<=right;i++)s+=a[i];return s;}
    public static void main(String[] z){if(sum(new int[]{4,-2,7,1},1,3)!=6)throw new AssertionError();}
}
```

<!-- stage: bottleneck -->
### The Same Values Return

Suppose 100,000 queries each cover most of a 100,000-value ledger. The direct loop performs close to ten billion additions, or O(nq) time in the worst case. Two overlapping questions may rescan tens of thousands of identical cells. Because the array is immutable, those repeated additions reveal no new information; only the two query boundaries change between requests.

<!-- stage: insight -->
### Subtract Two Boundaries

Build the sentinel prefix from the previous lesson. The value at boundary `right + 1` contains everything through index `right`; the value at boundary `left` contains exactly the part before the requested interval. Subtracting removes that shared beginning. This is an **immutable range query** backed by **prefix cancellation**:

`sum(left..right) = prefix[right + 1] - prefix[left]`.

<!-- names: immutable range query, prefix cancellation -->

The formula is safer to derive from boundaries than memorize from array indices. Draw a cut before `left` and another after `right`; subtract the earlier cumulative state from the later one. The move is valid because addition has an inverse and the input does not change after preprocessing. Construction costs O(n), but every later query costs O(1). If updates occur between questions, the table becomes stale and a Fenwick tree or segment tree is a different future tool.

<!-- stage: variables -->
### Query Boundaries

`prefix[b]` stores the total strictly before boundary `b`. An inclusive request uses boundaries `left` and `right + 1`. A half-open request `[left, right)` uses `left` and `right` directly. Both indices are validated by the problem contract, so the query method does not invent fallback behavior.

<!-- stage: trace -->
### Remove The Shared Beginning

Build `[0, 4, 2, 9, 10]` from `[4, -2, 7, 1]`. To answer indices `1..3`, take the total through index three, which is boundary four with value `10`. The unwanted beginning before index one is boundary one with value `4`. Their difference is `6`.

The negative value causes no difficulty. Cancellation uses exact cumulative totals, not monotonicity. For the single-cell query `2..2`, subtract boundary two from boundary three: `9 - 2 = 7`. For the whole array, subtract boundary zero from boundary four. The sentinel makes both edge cases use the same expression without a conditional branch or special indexing rule.

```trace
{"cells":[4,-2,7,1],"pointers":["left","right"],"steps":[{"at":{"left":1,"right":3},"vars":{"endIndex":4},"note":"Move from inclusive right 3 to boundary 4."},{"at":{"left":1,"right":3},"vars":{"endBoundary":10,"startBoundary":4},"note":"Read the cumulative values at the two boundaries."},{"at":{"left":1,"right":3},"vars":{"rangeSum":6},"note":"Subtract the shared beginning; only indices 1 through 3 remain."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java run
public final class ImmutableRangeSums {
    private final long[] prefix;
    ImmutableRangeSums(int[] nums){prefix=new long[nums.length+1];for(int i=0;i<nums.length;i++)prefix[i+1]=prefix[i]+nums[i];}
    long sumRange(int left,int right){return prefix[right+1]-prefix[left];}
    public static void main(String[] z){var x=new ImmutableRangeSums(new int[]{4,-2,7,1});if(x.sumRange(1,3)!=6||x.sumRange(2,2)!=7)throw new AssertionError();}
}
```

Preprocessing takes O(n) time and O(n) space. Each query performs two reads and one subtraction, hence O(1) time. `long` protects cumulative totals. The blueprint relies on the stated `0 <= left <= right < n` contract; throwing a custom value for invalid indices would hide a caller error.

<!-- stage: applicability -->
### When It Applies

Choose this pattern when the data is fixed and many arbitrary contiguous sums must be answered. The invariant is that `prefix[b]` equals the sum strictly before boundary `b`; cancellation therefore leaves precisely the requested cells.

The false friend is a sliding window, which incrementally visits one related sequence of ranges rather than answering arbitrary requests. A second false friend is a difference array: it batches updates before one reconstruction, whereas this structure preprocesses values before many reads. If callers mutate the original array, the prefix table does not update. Java's main hazard is returning `int` after correctly computing a `long` total.

<!-- stage: exercises -->
### Exercises

#### [Build] Range Sum Query Immutable (LeetCode 303)
<!-- id: ps-range-sum-immutable -->

**Prerequisites.** Sentinel prefix construction and inclusive boundary conversion.

**Problem.** Design an immutable array wrapper that preprocesses integers and returns the sum from `left` through `right` for every valid query.

**Constraints.** At most `10^4` values and `10^4` queries; target O(n) construction and O(1) query time.

**Example 1.** Input `nums = [3,-2,5,1]`, query `[1,3]`, output `4`.

**Example 2.** Input `nums = [8]`, query `[0,0]`, output `8`.

**Hint.** Identify the boundary immediately after `right`. Which earlier boundary contains exactly the values to remove?

**Changed decision.** This rung packages preprocessing and repeated queries behind an immutable API.

#### [Vary] Half-Open Query (Author exercise)
<!-- id: ps-half-open-query -->

**Prerequisites.** The inclusive query formula from this lesson.

**Problem.** Given an immutable array and queries `[left,right)`, return each requested sum; an empty range where `left == right` must return zero.

**Constraints.** `0 <= left <= right <= n`; totals fit in `long`; each query must take O(1) time.

**Example 1.** Input `nums = [6,2,-3,4]`, query `[1,4)`, output `3`.

**Example 2.** Input `nums = [6,2]`, query `[1,1)`, output `0`.

**Hint.** Half-open indices already name boundaries. Try the subtraction without adding one to either endpoint.

**Changed decision.** The query contract changes from inclusive endpoints to a half-open interval that permits emptiness.

#### [Boundary] Whole Array (Author exercise)
<!-- id: ps-whole-array-query -->

**Prerequisites.** Sentinel boundaries, including boundary zero and boundary `n`.

**Problem.** Implement a method that returns the sum of the entire immutable array through the same general range-query formula, including an empty array.

**Constraints.** `0 <= nums.length <= 10^5`; use O(n) preprocessing and O(1) query work.

**Example 1.** Input `nums = [2,-5,9]`, output `6`.

**Example 2.** Input `nums = []`, output `0`.

**Hint.** The whole array lies between which two sentinel boundaries? Avoid reading `prefix[-1]`.

**Changed decision.** Both outer boundaries are exercised, and the empty array is a valid whole-range request.

#### [Recognize] XOR Queries of a Subarray (LeetCode 1310)
<!-- id: ps-xor-range-query -->

**Prerequisites.** Boundary cancellation and Java's bitwise XOR operator.

**Problem.** Given an integer array and inclusive query pairs, return the XOR of the values in each requested subarray.

**Constraints.** Up to `3 * 10^4` values and queries; target O(n + q) total time.

**Example 1.** Input `arr = [5,1,7]`, queries `[[0,1],[1,2]]`, output `[4,6]`.

**Example 2.** Input `arr = [9]`, queries `[[0,0]]`, output `[9]`.

**Hint.** Addition cancels a shared prefix by subtraction. Which XOR identity cancels the same bits without subtraction?

**Changed decision.** The aggregate changes from addition to a self-inverse bitwise operation.

