<!-- lesson-kind: combination -->
<!-- lesson-id: sorting-and-two-pointers -->
## Sorting And Two Pointers

<!-- stage: context -->
### Create An Order

Some pair and tuple inputs arrive unsorted, yet their output depends on values rather than original positions. Sorting changes the representation: endpoint sums now move monotonically, equal values become adjacent, and bounds can reject impossible branches. The price is O(n log n) preprocessing and mutation. The gain is a scan whose movement has proof instead of guesswork.

That trade is deliberate and contract-dependent.

<!-- stage: contributions -->
### What Each Part Adds

Sorting contributes the monotone order, adjacent duplicates, and optional lower or upper sum bounds. Two pointers contribute linear elimination after fixed choices: a low sum advances the smallest candidate and a high sum retreats the largest. Duplicate skipping contributes unique outputs without a result set. None suffices alone. Sorting without pointer movement still enumerates pairs; pointers on unsorted values cannot justify a direction.

<!-- stage: naive -->
### Hash Or Enumerate

For one unsorted pair, a hash map is excellent and preserves original indices. For all unique triples or quadruples, nested enumeration plus a result set works but costs an extra factor of `n` and stores redundant tuples. This combination is appropriate only when sorting is compatible with the required output contract.

<!-- stage: bottleneck -->
### Repeated Pair Work

After fixing one value in 3Sum, enumerating every pair costs O(n²) for that fixed choice and O(n³) overall. Sorting makes the remaining pair target monotone, reducing each suffix search to O(n) and total time to O(n²). For 4Sum, two fixed choices plus the scan cost O(n³), again one factor better than direct enumeration.

Redundant equal branches would still waste part of that improvement.

<!-- stage: insight -->
### Sort Then Eliminate

First decide that original positions and order are irrelevant or preserved elsewhere. Sort the working array. At each fixed depth, skip equal choices and reduce the target. In the final suffix, compare endpoint sum with the remainder and eliminate one side. Record closest candidates before movement when an exact solution is not guaranteed.

<!-- names: sort-and-scan, monotone pair suffix -->

This combined pattern is **sort-and-scan**. The **monotone pair suffix** is the property that makes each endpoint move safe. Mutation is a contract decision, not an implementation detail: clone the array if callers require preservation and include O(n) space. Widen arithmetic before combining fixed values, because ordering does not prevent overflow.

Once sorted, lower and upper achievable sums can also prune a fixed branch, but those bounds are optimizations rather than the central proof. The essential reasoning remains: a comparison must eliminate every candidate using one endpoint, and duplicate movement must occur only after a representative choice has been processed.

<!-- stage: variables -->
### Combined State

Fixed indices define the current prefix of a tuple. `left` and `right` bound the pair suffix. A `long remaining` target accounts for fixed choices. Saved endpoint values control duplicate skips after a match. For closest variants, `bestSum` is updated before a movement eliminates the current pair.

<!-- stage: trace -->
### From Unsorted To Monotone

Given `[3,-1,0,2,-2,1]`, sorting yields `[-2,-1,0,1,2,3]`. Fix `-2` for a zero-sum triple, leaving pair target 2. Endpoints `-1` and 3 sum to 2, so record `[-2,-1,3]` and move beyond both values. The next pair 0 and 2 also matches, producing `[-2,0,2]`.

After that suffix closes, the fixed choice advances. Each later fixed value either opens a new monotone pair search or is skipped as a duplicate. The sort created both the direction rule and the adjacency needed for uniqueness.

If original indices were required, this transformation would need index-value records or a different algorithm. Here the requested output contains values, so the reordered representation preserves everything the answer needs.

```trace
{"cells":[-2,-1,0,1,2,3],"pointers":["fixed","left","right"],"steps":[{"at":{"fixed":0,"left":1,"right":5},"vars":{"pairTarget":2,"pairSum":2},"note":"Fix -2; endpoints -1 and 3 match the remaining target."},{"at":{"fixed":0,"left":2,"right":4},"vars":{"pairTarget":2,"pairSum":2},"note":"After moving inward, 0 and 2 form the next unique pair."},{"at":{"fixed":1,"left":2,"right":5},"vars":{"pairTarget":1,"pairSum":3},"note":"Advance the fixed choice and begin a new ordered suffix scan."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java run
import java.util.*;
public final class SortedTripleCount {static int count(int[]input){int[]a=input.clone();Arrays.sort(a);int ans=0;for(int i=0;i<a.length-2;i++){if(i>0&&a[i]==a[i-1])continue;int l=i+1,r=a.length-1;while(l<r){long s=(long)a[i]+a[l]+a[r];if(s==0){ans++;int x=a[l],y=a[r];while(l<r&&a[l]==x)l++;while(l<r&&a[r]==y)r--;}else if(s<0)l++;else r--;}}return ans;}public static void main(String[]z){if(count(new int[]{3,-1,0,2,-2,1})!=3)throw new AssertionError();}}
```

The clone preserves the input and makes the O(n) space cost explicit. The dominant runtime is O(n²), not the initial sort. Removing the clone would reduce auxiliary storage but would deliberately mutate the caller's array.

<!-- stage: applicability -->
### When It Applies

Use this combination when value combinations matter, reordering is legal or a copy is affordable, and sorting creates a monotone pair suffix. The invariant is that fixed choices are unique at their depths and every unruled final pair remains between the two endpoints.

The false friend is Two Sum returning original indices, where a hash map avoids losing identity. Another false friend is a pair condition with no monotone response to sorted values. Sorting alone does not authorize a pointer move; state the inequality that eliminates an endpoint.

<!-- stage: exercises -->
### Exercises

#### [Build] Two Sum II (LeetCode 167)
<!-- id: tp-combo-two-sum-ii -->

**Prerequisites.** Sorted order and endpoint elimination.

**Problem.** Given a nondecreasing array with exactly one valid pair, return the pair's one-based indices whose values sum to `target`.

**Constraints.** `2 <= numbers.length <= 3 * 10^4`; use O(1) auxiliary space.

**Example 1.** Input `numbers = [2,7,11,15]`, `target = 9`; output `[1,2]`.

**Example 2.** Input `numbers = [-1,0]`, `target = -1`; output `[1,2]`.

**Hint.** Translate a low or high endpoint sum into a proof about every partner for one endpoint.

**Changed decision.** The sorted representation is given, so no preprocessing is charged or allowed.

#### [Vary] 3Sum (LeetCode 15)
<!-- id: tp-combo-three-sum -->

**Prerequisites.** One fixed value, pair suffix scanning, and duplicate skipping.

**Problem.** Given an unsorted integer array, return all distinct value triples from different indices whose total is zero.

**Constraints.** `3 <= nums.length <= 3000`; sorting is permitted.

**Example 1.** Input `nums = [-1,0,1,2,-1,-4]`; output has two distinct triples.

**Example 2.** Input `nums = [0,1,1]`; output `[]`.

**Hint.** Sorting earns both monotone movement and adjacent duplicate detection.

**Changed decision.** One fixed choice turns a pair method into a triple method.

#### [Boundary] 3Sum Closest (LeetCode 16)
<!-- id: tp-combo-three-closest -->

**Prerequisites.** Best-candidate preservation during endpoint elimination.

**Problem.** Return the sum of three array values whose total is closest to the supplied target.

**Constraints.** `3 <= nums.length <= 500`; exactly one closest total exists.

**Example 1.** Input `nums = [-1,2,1,-4]`, `target = 1`; output `2`.

**Example 2.** Input `nums = [0,0,0]`, `target = 1`; output `0`.

**Hint.** Save the current total before its comparison causes an endpoint to be discarded.

**Changed decision.** The scan must return useful information even without equality.

#### [Recognize] 4Sum (LeetCode 18)
<!-- id: tp-combo-four-sum -->

**Prerequisites.** Two fixed depths, unique branches, and widened sums.

**Problem.** Given integers and a target, return every unique four-value combination from distinct indices that reaches the target.

**Constraints.** `1 <= nums.length <= 200`; use `long` for intermediate sums.

**Example 1.** Input `nums = [1,0,-1,0,-2,2]`, `target = 0`; output has three quadruples.

**Example 2.** Input `nums = [2,2,2,2,2]`, `target = 8`; output has one quadruple.

**Hint.** Apply the same skip rule at each fixed depth before reaching the pair suffix.

**Changed decision.** A second fixed choice adds another branch level but no new base algorithm.
