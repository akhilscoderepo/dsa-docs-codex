<!-- lesson-kind: standard -->
<!-- lesson-id: k-sum-reduction -->
## K-Sum Reduction

<!-- stage: context -->
### Reduce One Choice

A four-number target appears to demand four nested loops. Yet after choosing one value, the remaining question is a three-number target on a suffix; after choosing another, it becomes a sorted pair target. The important design decision is where exhaustive choice ends and monotone search begins. That boundary gives a reusable method instead of a separate memorized algorithm for every tuple size.

<!-- stage: naive -->
### Enumerate Every Tuple

Choose all `k` index combinations and test each sum. For 3Sum this means three nested loops; for 4Sum it means four. The code is direct and useful as a brute-force oracle on small random arrays, but it ignores sorted order and repeats equivalent branches when values are equal.

<!-- stage: bottleneck -->
### One Exponent Too Many

Straight enumeration of `k` values costs O(n^k). Sorting does not help if the loops still choose every dimension. Once only two choices remain, however, sorted order supports an O(n) opposite-end scan instead of O(n²) pair enumeration. Fixing `k-2` values and using that base case lowers the total to O(n^(k-1)); duplicate skipping prevents repeated value combinations.

<!-- stage: insight -->
### Recurse Toward Two

Sort the values. At a `k`-sum state, choose one fixed value at each legal position, subtract it from the remaining target, and solve `(k-1)`-sum on the suffix. When `k == 2`, run the opposite-end pair scan. The suffix start ensures indices are never reused, while skipping equal fixed values makes each value branch unique.

<!-- names: k-sum reduction, two-sum base case -->

This is **k-sum reduction**. Its **two-sum base case** is where ordering finally eliminates candidates rather than enumerating them. State consists of the suffix start, remaining `k`, and remaining target. Use `long` for both the target and every intermediate subtraction: four legal `int` values can overflow before comparison even when the requested target itself fits in `int`.

Backtracking removes the most recent fixed value before the loop tries its next candidate, keeping path state aligned with recursion depth.

<!-- stage: variables -->
### Recursive State

`start` is the first index available to the current depth. `k` counts how many values still must be chosen, and `target` is a `long` remainder. A path list stores fixed values. At the base case, `left` and `right` search within the suffix. Duplicate checks compare only with the previous choice at the same depth.

<!-- stage: trace -->
### Four Values To Two

For sorted `[-2,-1,0,0,1,2]`, target zero, and `k = 4`, choose `-2`; the remaining state needs three values summing to 2. Choose `-1`; the pair suffix must sum to 3, and endpoints 0 and 2 are too small, so the left pointer advances until 1 and 2 produce a match. That yields `[-2,-1,1,2]`.

Backtracking restores the path before the next fixed choice. Choosing the first 0 at the second depth eventually produces `[-2,0,0,2]`. The next equal 0 at that same depth is skipped, because it would open the identical suffix search and duplicate the result.

```trace
{"cells":[-2,-1,0,0,1,2],"pointers":["first","second","left","right"],"steps":[{"at":{"first":0,"second":1,"left":2,"right":5},"vars":{"remaining":3,"sum":2},"note":"Fix -2 and -1; the final pair must sum to 3."},{"at":{"first":0,"second":1,"left":4,"right":5},"vars":{"remaining":3,"sum":3},"note":"Advance the left pointer until 1 and 2 match the pair target."},{"at":{"first":0,"second":2,"left":3,"right":5},"vars":{"remaining":2,"sum":2},"note":"Backtrack, fix the first zero, and find the pair 0 and 2."},{"at":{"first":0,"second":3,"left":4,"right":5},"vars":{"remaining":2,"sum":3},"note":"Skip this equal fixed zero at the same depth."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java run
import java.util.*;
public final class GenericKSum {
 static List<List<Integer>> solve(int[]a,int k,long target){Arrays.sort(a);return go(a,0,k,target);}
 static List<List<Integer>> go(int[]a,int s,int k,long t){List<List<Integer>>out=new ArrayList<>();if(k==2){int l=s,r=a.length-1;while(l<r){long x=(long)a[l]+a[r];if(x==t){out.add(List.of(a[l],a[r]));int p=a[l],q=a[r];while(l<r&&a[l]==p)l++;while(l<r&&a[r]==q)r--;}else if(x<t)l++;else r--;}return out;}for(int i=s;i<=a.length-k;i++){if(i>s&&a[i]==a[i-1])continue;for(List<Integer>tail:go(a,i+1,k-1,t-a[i])){List<Integer>row=new ArrayList<>();row.add(a[i]);row.addAll(tail);out.add(row);}}return out;}
 public static void main(String[]z){if(solve(new int[]{1,0,-1,0,-2,2},4,0).size()!=3)throw new AssertionError();}
}
```

For fixed `k`, the running time is O(n^(k-1)) plus output construction. Recursion uses O(k) stack depth, excluding results and the sorting implementation. The input is mutated by sorting, so a no-mutation contract requires a defensive copy.

<!-- stage: applicability -->
### When It Applies

Use this reduction when reordering is allowed, the output is based on value combinations rather than original indices, and fixing values leaves a monotone sorted pair problem. The invariant is that a recursive state considers every unique combination drawn from its suffix exactly once.

The false friend is unsorted Two Sum requiring original indices; sorting can destroy the required identity, so a hash map is preferable. Another false friend is subset sum with arbitrary subset size, where the number of selections is not a small fixed `k`. Dynamic programming or meet-in-the-middle techniques own that different state space.

<!-- stage: exercises -->
### Exercises

#### [Build] 3Sum (LeetCode 15)
<!-- id: tp-k-three-sum -->

**Prerequisites.** Sorting, duplicate skipping, and the two-sum base case.

**Problem.** Given integers `nums`, return all distinct triples from different indices whose values sum to zero.

**Constraints.** `3 <= nums.length <= 3000`; `-10^5 <= nums[i] <= 10^5`.

**Example 1.** Input `nums = [-1,0,1,2,-1,-4]`; output `[[-1,-1,2],[-1,0,1]]`.

**Example 2.** Input `nums = [1,2,-2,-1]`; output `[]`.

**Hint.** Fix one value, change the remaining target to its negation, and scan the suffix.

**Changed decision.** One exhaustive fixed choice reduces the problem directly to the pair base case.

#### [Vary] 3Sum Closest (LeetCode 16)
<!-- id: tp-three-sum-closest -->

**Prerequisites.** Pair movement with best-candidate tracking.

**Problem.** Choose three values whose sum is closest to `target` and return that sum. The closest sum is guaranteed unique.

**Constraints.** `3 <= nums.length <= 500`; values and target lie between `-10^4` and `10^4`.

**Example 1.** Input `nums = [-1,2,1,-4]`, `target = 1`; output `2`.

**Example 2.** Input `nums = [0,0,0]`, `target = 1`; output `0`.

**Hint.** Measure every fixed-plus-endpoints sum before the pair scan discards an endpoint.

**Changed decision.** Preserve the nearest total when exact equality may never occur.

#### [Boundary] Overflowing Sum (Author exercise)
<!-- id: tp-overflowing-k-sum -->

**Prerequisites.** Java numeric promotion and widened intermediate targets.

**Problem.** Decide whether four distinct values sum to a signed 64-bit `target`, even when intermediate 32-bit addition would overflow.

**Constraints.** `4 <= nums.length <= 200`; elements are arbitrary Java `int` values; target is `long`.

**Example 1.** Input `nums = [2147483647,2147483647,-1,-1]`, `target = 4294967292`; output `true`.

**Example 2.** Input `nums = [2147483647,2147483647,0,0]`, `target = -2`; output `false`.

**Hint.** Widen before the first addition and keep recursive target subtraction in `long`.

**Changed decision.** Arithmetic correctness becomes part of the state contract, not a final cast.

#### [Recognize] 4Sum (LeetCode 18)
<!-- id: tp-k-four-sum -->

**Prerequisites.** Two fixed depths, pair base case, and duplicate control.

**Problem.** Given an integer array and target, return every unique four-value combination from distinct indices whose total equals `target`.

**Constraints.** `1 <= nums.length <= 200`; values and target are signed 32-bit integers.

**Example 1.** Input `nums = [1,0,-1,0,-2,2]`, `target = 0`; output contains three unique quadruples.

**Example 2.** Input `nums = [2,2,2,2,2]`, `target = 8`; output `[[2,2,2,2]]`.

**Hint.** View the second fixed loop as another level of the same reduction, not a new algorithm.

**Changed decision.** An additional fixed dimension increases time by one factor of `n` while preserving the base case.
