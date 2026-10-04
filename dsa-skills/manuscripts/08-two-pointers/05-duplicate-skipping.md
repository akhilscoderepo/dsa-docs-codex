<!-- lesson-kind: standard -->
<!-- lesson-id: duplicate-skipping -->
## Duplicate Skipping

<!-- stage: context -->
### Unique Combinations

Sorted input may contain many equal values. A tuple problem that asks for unique value combinations can therefore reach the same answer through different index choices. Removing duplicates from the final list works, but it stores redundant answers and repeats identical searches. A stronger traversal processes one representative for each value choice while preserving enough copies to occupy different tuple positions.

<!-- stage: naive -->
### Deduplicate Results

Enumerate every tuple, normalize it, and insert it into a set. This is a useful small-input oracle, but three nested loops cost O(n³). The set also allocates and hashes tuples that a sorted traversal could avoid generating. Deleting equal input values first is incorrect because an answer such as `[0,0,0]` needs three equal values at distinct indices.

<!-- stage: bottleneck -->
### Identical Branches

After sorting, equal fixed values launch identical suffix searches. Equal endpoints recreate a pair that was already emitted. If these choices remain, the traversal repeats work even when the number of unique outputs is tiny. We want the three-value search to cost O(n²) after sorting, with uniqueness enforced directly by pointer movement rather than an auxiliary result set.

<!-- stage: insight -->
### Process One Representative

At each fixed depth, process the first occurrence of a value and skip later equal occurrences before opening another branch. In the final pair scan, evaluate the current endpoints first. After a match, move both pointers, then pass all values equal to the endpoints just consumed.

<!-- names: duplicate skipping, representative branch -->

This is **duplicate skipping**. A **representative branch** owns all work for one value at one decision depth. Skipping before the first representative is evaluated can discard the only answer; skipping only after every tuple is generated saves no work. The rule is depth-specific: equal values remain legal in different positions of the same tuple. That is why `[0,0,0]` survives but appears only once. At a deeper fixed position, equality checks must stay within that depth's start boundary.

<!-- stage: variables -->
### Depth And Endpoints

The fixed index denotes the current tuple depth. `left` and `right` search its remaining sorted suffix. Comparing a fixed value with the preceding fixed value detects an equivalent branch at the same depth. After a pair match, saved endpoint values drive the skip loops and bounds checks keep the pointers inside the current interval.

<!-- stage: trace -->
### Four Zeros

For `[0,0,0,0]`, fix index 0 and search with endpoints 1 and 3. The sum is zero, so record `[0,0,0]`. Move both endpoints and skip further copies of the consumed endpoint values. The interval closes. When the outer loop reaches index 1, it skips that fixed zero because index 0 already represented the same branch.

The method returns exactly one triple. It did not remove equal input values, and it did not skip the second zero before the match. Three different indices supplied the values, while the branch policy controlled only duplicate output combinations. This separates index multiplicity from value uniqueness.

```trace
{"cells":[0,0,0,0],"pointers":["fixed","left","right"],"steps":[{"at":{"fixed":0,"left":1,"right":3},"vars":{"sum":0,"answers":0},"note":"The first fixed zero represents this branch and the endpoints complete a triple."},{"at":{"fixed":0,"left":2,"right":2},"vars":{"sum":0,"answers":1},"note":"Move inward and skip copies of both consumed endpoint values."},{"at":{"fixed":1,"left":2,"right":3},"vars":{"sum":0,"answers":1},"note":"Skip the repeated fixed zero because its branch was already processed."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java run
import java.util.*;
public final class UniquePairValues {static List<String> f(int[]a,int t){Arrays.sort(a);List<String>r=new ArrayList<>();int l=0,h=a.length-1;while(l<h){long s=(long)a[l]+a[h];if(s==t){int x=a[l],y=a[h];r.add(x+":"+y);while(l<h&&a[l]==x)l++;while(l<h&&a[h]==y)h--;}else if(s<t)l++;else h--;}return r;}public static void main(String[]z){if(!f(new int[]{1,1,2,2,3},4).equals(List.of("1:3","2:2")))throw new AssertionError();}}
```

The scan is O(n) after the O(n log n) sort and uses O(1) auxiliary state apart from output. Copy before sorting when mutation is forbidden, and include that copy in the space analysis.

<!-- stage: applicability -->
### When It Applies

Use duplicate skipping when sorted candidates can produce the same value tuple through different indices and output combinations must be unique. The invariant is that every smaller choice at the current depth has already had exactly one representative branch processed.

The false friend is an index-combination counting problem. There, equal values at different indices may represent distinct contributions, so skipping them undercounts. Another false friend is global input deduplication: multiplicity can be required inside one valid tuple. Always distinguish value uniqueness in output from identity of source indices.

<!-- stage: exercises -->
### Exercises

#### [Build] Unique Pairs (Author exercise)
<!-- id: tp-unique-pairs -->

**Prerequisites.** Sorted pair search and post-match skipping.

**Problem.** Given integers `nums` and `target`, return every distinct nondecreasing value pair whose sum equals `target`.

**Constraints.** `0 <= nums.length <= 10^5`; signed 32-bit values; sorting is allowed.

**Example 1.** Input `nums = [1,1,2,2,3]`, `target = 4`; output `[[1,3],[2,2]]`.

**Example 2.** Input `nums = [0,0,0]`, `target = 1`; output `[]`.

**Hint.** After a match, remember both values and advance beyond all their copies.

**Changed decision.** Pair search collects every unique answer instead of stopping after one.

#### [Vary] 3Sum (LeetCode 15)
<!-- id: tp-three-sum-dedup -->

**Prerequisites.** Fixed-value reduction and local duplicate control.

**Problem.** Given an integer array, return all distinct triples from three different indices whose values sum to zero.

**Constraints.** `3 <= nums.length <= 3000`; `-10^5 <= nums[i] <= 10^5`.

**Example 1.** Input `nums = [-1,0,1,2,-1,-4]`; output `[[-1,-1,2],[-1,0,1]]`.

**Example 2.** Input `nums = [0,0,0]`; output `[[0,0,0]]`.

**Hint.** Skip repeated fixed values before each suffix scan and endpoint repeats after matches.

**Changed decision.** Uniqueness is enforced at both the fixed and pair-search depths.

#### [Boundary] All Equal (Author exercise)
<!-- id: tp-all-equal-triplet -->

**Prerequisites.** Correct duplicate-skip timing.

**Problem.** Return unique zero-sum triples from an array whose values are all equal; three distinct indices are still required.

**Constraints.** `3 <= nums.length <= 10^5`; every element has the same value.

**Example 1.** Input `nums = [0,0,0,0]`; output `[[0,0,0]]`.

**Example 2.** Input `nums = [2,2,2]`; output `[]`.

**Hint.** Multiplicity supplies indices for one answer, not repeated copies of that answer.

**Changed decision.** Maximum duplication exposes whether skips happen before or after a representative.

#### [Recognize] 4Sum (LeetCode 18)
<!-- id: tp-four-sum-dedup -->

**Prerequisites.** Nested fixed choices and `long` sums.

**Problem.** Given an integer array and target, return all unique quadruples from four distinct indices whose values sum to `target`.

**Constraints.** `1 <= nums.length <= 200`; inputs are signed 32-bit integers.

**Example 1.** Input `nums = [1,0,-1,0,-2,2]`, `target = 0`; output has three unique quadruples.

**Example 2.** Input `nums = [2,2,2,2,2]`, `target = 8`; output `[[2,2,2,2]]`.

**Hint.** Apply the representative rule independently at both fixed loop depths.

**Changed decision.** A second fixed dimension adds another duplicate branch to control.
