<!-- lesson-kind: standard -->
<!-- lesson-id: remainder-classes -->
## Remainder Classes

<!-- stage: context -->
### Divisible Without Enumerating

A reporting service groups transaction periods whose total is divisible by a billing cycle `k`. The exact total is irrelevant; only divisibility matters. Negative adjustments are permitted, and the report may ask either how many periods qualify or how long the longest one is. We need a compact prefix state that preserves precisely the information that this divisibility requirement needs.

<!-- stage: naive -->
### Sum Every Period

The direct method extends every start and tests each accumulated sum with `floorMod`. It is correct for positive `k`, including negative values in the input. Every interval is checked against the stated modular condition.

```java run
public final class RemainderNaive {static long count(int[]a,int k){long c=0;for(int l=0;l<a.length;l++){long s=0;for(int r=l;r<a.length;r++){s+=a[r];if(Math.floorMod(s,k)==0)c++;}}return c;}public static void main(String[]z){if(count(new int[]{4,-1,2},5)!=1)throw new AssertionError();}}
```

<!-- stage: bottleneck -->
### Exact Sums Are Excess State

The nested loops cost O(n^2), about five billion extensions at length 100,000. They also retain more information than the question needs. Two large prefix totals may differ greatly yet be equivalent for divisibility. Recomputing every interval sum ignores that a small set of `k` remainder classes can summarize all prior boundaries relevant to the very next answer.

<!-- stage: insight -->
### Match Normalized Remainders

If two prefix sums have the same remainder modulo `k`, their difference is divisible by `k`. Replace raw totals with a **normalized remainder class** computed by `Math.floorMod(prefix, k)`. For counting, store a **remainder-frequency map**; for maximum length, store the earliest index of each remainder.

<!-- names: normalized remainder class, remainder-frequency map -->

Seed remainder zero for the empty prefix. At each boundary, all earlier copies of the current remainder create divisible subarrays ending here, so add their frequency before recording the new boundary. This is the prefix-count equation compressed into at most `k` equivalence classes. Normalization is essential in Java: `-1 % 5` is `-1`, while a mathematically equivalent positive prefix may have remainder `4`. `Math.floorMod(-1, 5)` returns `4`, allowing equivalent states to meet. The safe move follows because equal normalized remainders differ by an integer multiple of `k`.

<!-- stage: variables -->
### Class Not Magnitude

`prefix` is a `long` cumulative total. `remainder` is an `int` in `[0, k)`. `frequency[r]` counts earlier boundaries in class `r`; a map can replace the array when `k` is large. `answer` is `long` because the number of qualifying subarrays may be quadratic.

<!-- stage: trace -->
### A Negative Prefix Joins

Use `[4, -5, 1]` with `k = 5`. Seed class zero once. After `4`, the prefix is four and class four has no earlier copy, so record it. After `-5`, the prefix is `-1`; Java's raw remainder is `-1`, but normalized class is four. It matches the earlier boundary, counting subarray `[-5]`.

After the final `1`, prefix becomes zero and normalized class zero matches the seed, counting the whole array. Record zero a second time. The answer is two. Without normalization, the two equivalent class-four states would use keys `4` and `-1`, and the valid negative-valued subarray would disappear silently.

```trace
{"cells":[4,-5,1],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"prefix":4,"remainder":4,"answer":0},"note":"Record the first boundary in class 4."},{"at":{"i":1},"vars":{"prefix":-1,"remainder":4,"answer":1},"note":"floorMod maps -1 to class 4, revealing the divisible subarray."},{"at":{"i":2},"vars":{"prefix":0,"remainder":0,"answer":2},"note":"Class zero meets the seeded empty boundary."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java run
public final class RemainderBlueprint {static long count(int[]a,int k){long[]f=new long[k];f[0]=1;long p=0,ans=0;for(int x:a){p+=x;int r=(int)Math.floorMod(p,k);ans+=f[r];f[r]++;}return ans;}public static void main(String[]z){if(count(new int[]{4,-5,1},5)!=2)throw new AssertionError();}}
```

The array version costs O(n + k) time including initialization and O(k) space. A hash map costs O(n) expected time and stores only seen classes. The contract requires `k > 0`; division by zero is undefined. Casting is safe only after `floorMod(long, int)` has produced a value below positive `k`.

<!-- stage: applicability -->
### When It Applies

Use remainder classes when the range condition is divisibility by a fixed positive `k`. The invariant is that frequency class `r` counts earlier boundaries whose normalized prefix remainder equals `r`; matching it makes the intervening sum divisible.

The false friend is storing raw prefix sums, which solves equality to a specific target but misses the intended equivalence compression. Another false friend is using frequencies for a longest-span request; preserve earliest indices instead. Java's `%` keeps the dividend's sign, so negative inputs silently split one mathematical class unless `Math.floorMod` is used.

<!-- stage: exercises -->
### Exercises

#### [Build] Subarray Sums Divisible by K (LeetCode 974)
<!-- id: ps-divisible-subarrays -->

**Prerequisites.** Prefix frequencies and normalized modular arithmetic.

**Problem.** Given an integer array and positive integer `k`, return the number of non-empty contiguous subarrays whose sum is divisible by `k`.

**Constraints.** `1 <= nums.length <= 3 * 10^4`, `1 <= k <= 10^4`; values may be negative; target O(n + k) time.

**Example 1.** Input `nums = [3,2,-5,5]`, `k = 5`, output `6`.

**Example 2.** Input `nums = [-1,1]`, `k = 2`, output `1`.

**Hint.** Which earlier boundaries share the current normalized remainder? Count every copy, not only the first.

**Changed decision.** Raw prefix keys are compressed into modular equivalence classes.

#### [Vary] Continuous Subarray Sum (LeetCode 523)
<!-- id: ps-continuous-divisible -->

**Prerequisites.** Remainder classes and earliest-index maps.

**Problem.** Given non-negative integers and positive `k`, return whether a contiguous subarray of length at least two has a sum divisible by `k`.

**Constraints.** `1 <= nums.length <= 10^5`, `1 <= k <= 2^31-1`; target O(n) expected time.

**Example 1.** Input `nums = [6,1,5]`, `k = 6`, output `true` from `[1,5]`.

**Example 2.** Input `nums = [7]`, `k = 7`, output `false` because length one is forbidden.

**Hint.** A repeated remainder proves divisibility, but what difference between boundary indices proves the minimum length? Preserve the earliest occurrence.

**Changed decision.** The map changes from counts to earliest positions and adds a length contract.

#### [Boundary] Negative Values (Author exercise)
<!-- id: ps-negative-remainders -->

**Prerequisites.** `Math.floorMod` and frequency counting.

**Problem.** Count divisible-sum subarrays in an array that may contain negative values, and return the normalized final prefix remainder as a diagnostic value.

**Constraints.** `0 <= nums.length <= 10^5`, `1 <= k <= 10^4`; target O(n + k) time.

**Example 1.** Input `nums = [-1,1]`, `k = 5`, output `count = 1`, `finalRemainder = 0`.

**Example 2.** Input `nums = [-1]`, `k = 5`, output `count = 0`, `finalRemainder = 4`.

**Hint.** Inspect Java's result for `-1 % 5`. Which standard method returns the class in `[0, k)`?

**Changed decision.** Negative prefix totals make normalization visible in the returned diagnostic.

#### [Recognize] Longest Divisible Span (Author exercise)
<!-- id: ps-longest-divisible-span -->

**Prerequisites.** Earliest-state storage and normalized remainder classes.

**Problem.** Given integers and positive `k`, return the maximum length of a contiguous subarray whose sum is divisible by `k`.

**Constraints.** `0 <= nums.length <= 10^5`; values may be negative; target O(n) expected time.

**Example 1.** Input `nums = [2,3,1,4]`, `k = 5`, output `4`.

**Example 2.** Input `nums = [1,1]`, `k = 3`, output `0`.

**Hint.** Frequency answers how many pairs exist. Which one occurrence of each remainder makes a future distance as large as possible?

**Changed decision.** The output switches from count to maximum length, so map values become earliest indices.

