<!-- lesson-kind: standard -->
<!-- lesson-id: earliest-balance -->
## Earliest Balance

<!-- stage: context -->
### The Longest Balanced Stretch

A network log labels each minute as healthy or degraded. An investigator wants the longest contiguous period containing the same number of both labels. Counting every matching period would be useful for a different report, but here only maximum length matters. Once the current balance has appeared before, the choice of which earlier occurrence to preserve determines how long the recovered span can be.

<!-- stage: naive -->
### Test Every Interval

Start at each index, extend right, and update counts for the two labels. Whenever the counts match, compare the interval length with the best seen. This exhaustive method is correct because it evaluates every possible pair of endpoints.

```java run
public final class BalanceNaive {
    static int longest(int[] a){int best=0;for(int l=0;l<a.length;l++){int balance=0;for(int r=l;r<a.length;r++){balance+=a[r]==1?1:-1;if(balance==0)best=Math.max(best,r-l+1);}}return best;}
    public static void main(String[] z){if(longest(new int[]{0,1,1,0,1,0})!=6)throw new AssertionError();}
}
```

<!-- stage: bottleneck -->
### Rebuild The Same Balances

For 100,000 labels, the nested loops examine roughly five billion intervals and cost O(n^2) time. Moving the start from index zero to index one discards every balance already calculated, even though later boundaries are unchanged. The work we need is not the count of earlier equal states but the farthest possible distance back to one such state.

<!-- stage: insight -->
### Preserve The First Occurrence

Transform one category to `+1` and the other to `-1`. Equal cumulative balances at two boundaries mean the values between them sum to zero, so the interval contains equal counts. Store an **earliest-index map** from each balance to the first boundary index where it occurred. When the balance repeats at `i`, its longest interval ending at `i` begins after that earliest index.

<!-- names: earliest-index map, balance transform -->

The **balance transform** turns a two-count condition into one additive state. Seed balance zero at index `-1`, the boundary before the array, so a balanced prefix ending at `i` has length `i - (-1)`. Never overwrite a stored index: a later occurrence can only create a shorter future span than the earlier one. This map therefore answers a different question from the frequency map. Frequencies count all pairs; earliest positions maximize one distance. The safe move follows from equality of prefix state: subtracting equal balances leaves zero net contribution between their boundaries.

<!-- stage: variables -->
### Balance And Distance

`balance` is cumulative `ones - zeros` through the current index. `first` stores the smallest index for every balance encountered. `best` holds the largest difference between the current index and an earlier equal-balance index. The sentinel index `-1` represents the empty prefix before index zero.

<!-- stage: trace -->
### Keep The Oldest Zero

Scan `[0, 1, 1, 0, 1, 0]`. Seed balance zero at index `-1`. Index zero changes balance to `-1`, so store `-1 -> 0`. Index one restores balance zero; the seed produces length two. Index two raises balance to one and stores its first position.

Index three returns to zero. Do not replace the seed with index three; using `-1` gives length four. Index four repeats balance one, whose first index is two, producing length two. Index five again reaches zero, and the preserved seed gives length six. The hardest choice is doing nothing when a state repeats: retaining older information is precisely what maximizes future distance.

```trace
{"cells":[0,1,1,0,1,0],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"balance":-1,"first":0,"best":0},"note":"Store the first occurrence of balance -1."},{"at":{"i":1},"vars":{"balance":0,"earliest":-1,"best":2},"note":"The seeded zero balance creates a balanced prefix."},{"at":{"i":3},"vars":{"balance":0,"earliest":-1,"best":4},"note":"Keep the old seed instead of overwriting it."},{"at":{"i":5},"vars":{"balance":0,"earliest":-1,"best":6},"note":"The oldest equal state yields the entire array."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java run
import java.util.HashMap;
import java.util.Map;
public final class EarliestBalanceBlueprint {
    static int longest(int[] a){Map<Integer,Integer> first=new HashMap<>();first.put(0,-1);int balance=0,best=0;for(int i=0;i<a.length;i++){balance+=a[i]==1?1:-1;Integer old=first.get(balance);if(old!=null)best=Math.max(best,i-old);else first.put(balance,i);}return best;}
    public static void main(String[] z){if(longest(new int[]{0,1,1,0,1,0})!=6)throw new AssertionError();}
}
```

The scan costs O(n) expected time and O(n) space. A primitive balance range from `-n` to `n` can use an offset array to avoid boxing, though a map states the idea more clearly. Empty input returns zero. The binary contract matters: treating every non-one value as zero would be wrong if arbitrary integers were allowed.

<!-- stage: applicability -->
### When It Applies

Use earliest-state memory when the goal is the longest interval between two equal cumulative states. The invariant is that `first[s]` is the smallest index at which state `s` occurred, so a repeat at `i` creates the longest possible span ending at `i` for that state.

The false friend is a frequency map, which retains multiplicity for counting but not the boundary needed for length. Another false friend is resetting a balance when it becomes unfavorable; balance is an identity for future cancellation, not a score. In Java, `putIfAbsent` expresses the no-overwrite rule, but an explicit lookup avoids a second boxed operation when also computing the distance.

<!-- stage: exercises -->
### Exercises

#### [Build] Contiguous Array (LeetCode 525)
<!-- id: ps-contiguous-array -->

**Prerequisites.** Prefix boundaries, hash maps, and the `+1/-1` balance transform.

**Problem.** Given a binary array, return the maximum length of a contiguous subarray containing an equal number of zeroes and ones.

**Constraints.** `1 <= nums.length <= 5 * 10^4`; target O(n) expected time.

**Example 1.** Input `nums = [0,1,1,0,0]`, output `4`.

**Example 2.** Input `nums = [1,1,1]`, output `0`.

**Hint.** Convert zero to a negative contribution. When the same balance returns, which occurrence produces the greatest distance?

**Changed decision.** This first rung stores the earliest boundary rather than a frequency.

#### [Vary] Equal A And B (Author exercise)
<!-- id: ps-equal-a-b -->

**Prerequisites.** The binary balance method and conditional contributions.

**Problem.** Given an integer array and distinct values `a` and `b`, return the longest contiguous subarray containing equally many copies of `a` and `b`; other values are allowed and contribute zero.

**Constraints.** `0 <= nums.length <= 10^5`; target O(n) expected time.

**Example 1.** Input `nums = [4,9,5,4,5]`, `a = 4`, `b = 5`, output `5`.

**Example 2.** Input `nums = [7,7]`, `a = 1`, `b = 2`, output `2` because both counts are zero.

**Hint.** Assign opposite contributions to `a` and `b`. What contribution should an irrelevant value make without breaking a valid span?

**Changed decision.** A third category contributes zero and may extend the answer.

#### [Boundary] Prefix From Zero (Author exercise)
<!-- id: ps-balanced-prefix-zero -->

**Prerequisites.** Sentinel boundary index `-1` and earliest-state storage.

**Problem.** Return the longest equal-zero-and-one subarray and a boolean indicating whether the chosen maximum begins at index zero. Prefer the earliest start on ties.

**Constraints.** `1 <= nums.length <= 10^5`; target O(n) time.

**Example 1.** Input `nums = [0,1,1,0]`, output `length = 4`, `startsAtZero = true`.

**Example 2.** Input `nums = [1,1,0]`, output `length = 2`, `startsAtZero = false`.

**Hint.** Keep the start associated with every candidate. What start follows from matching the sentinel at index `-1`?

**Changed decision.** The result exposes whether the sentinel participates and defines a tie rule.

#### [Recognize] Even Vowel Counts (LeetCode 1371)
<!-- id: ps-even-vowel-parity -->

**Prerequisites.** Earliest repeated state and bit-mask basics.

**Problem.** Given a lowercase string, return the longest substring in which each vowel appears an even number of times.

**Constraints.** `1 <= s.length <= 5 * 10^5`; target O(n) time with constant-sized state storage.

**Example 1.** Input `s = "bcaac"`, output `5`; the two copies of `a` make every vowel count even.

**Example 2.** Input `s = "bcdf"`, output `4`; every vowel count is zero and therefore even.

**Hint.** Toggle one bit for each vowel. Why does seeing the same five-bit state twice prove every vowel changed an even number of times?

**Changed decision.** The repeated state expands from one integer balance to a five-bit parity signature.

