<!-- lesson-kind: standard -->
<!-- lesson-id: prefix-counts -->
## Prefix Counts

<!-- stage: context -->
### Count Every Matching Span

A transaction stream contains credits and debits, and an auditor asks how many contiguous periods net exactly `k`. Values may be negative, so extending a period can raise or lower its total. There may also be several valid starting boundaries for the same ending boundary. We need to count all of them without restarting a scan at every position in the stream.

<!-- stage: naive -->
### Try Every Start

For each left endpoint, extend right and accumulate the sum. This examines every contiguous subarray once, so it is correct. Negative values and repeated totals require no special handling because each pair of endpoints is tested explicitly.

```java run
public final class CountSumNaive {
    static long solve(int[] a, long k) {
        long count = 0;
        for (int left = 0; left < a.length; left++) {
            long sum = 0;
            for (int right = left; right < a.length; right++) {
                sum += a[right];
                if (sum == k) count++;
            }
        }
        return count;
    }
    public static void main(String[] args) {
        if (solve(new int[] {1, -1, 1}, 1) != 3) throw new AssertionError();
    }
}
```

<!-- stage: bottleneck -->
### Quadratic Endpoints

An array of 100,000 zeros has about five billion subarrays, and the nested loops spend O(n^2) time discovering them. For neighboring starts, most additions repeat. A sliding window cannot remove this cost when negatives are allowed because increasing `right` does not move the sum in one direction. We need an algebraic relation between two boundaries, not an ordering assumption.

<!-- stage: insight -->
### Ask For The Earlier Total

Let `current` be the prefix sum through the current value. A subarray ending here has sum `k` when `current - earlier = k`, or `earlier = current - k`. Store a **prefix-frequency map** from each earlier cumulative total to the number of boundaries that produced it. Before recording `current`, add the frequency of `current - k` to the answer.

<!-- names: prefix-frequency map, zero-prefix seed -->

The map stores frequencies rather than membership because repeated equal prefixes represent different starting boundaries. Seed it with the **zero-prefix seed** `{0: 1}` so a subarray beginning at index zero has a real earlier boundary to match. Lookup must happen before inserting the current prefix; otherwise `k = 0` would pair a boundary with itself and count an empty subarray. The invariant is that the map contains exactly the prefix values at boundaries strictly before the current ending boundary. That temporal order makes every counted range non-empty and counts it once.

<!-- stage: variables -->
### Counts At Boundaries

`prefix` is the sum through the current array index and is stored as `long`. `frequency` maps earlier prefix totals to their occurrence counts. `answer` is `long` because an all-zero array has `n(n+1)/2` matching subarrays. The current boundary joins the map only after its contribution is counted.

<!-- stage: trace -->
### Repeated Prefixes Matter

Use `[1, -1, 1]` with target `1`. Start with prefix zero recorded once. After reading the first `1`, the current prefix is `1`; look for `0`, find one boundary, and count `[0..0]`. Record prefix `1`.

After `-1`, current returns to zero. Looking for `-1` finds nothing, then prefix zero is recorded a second time. At the last `1`, current becomes one again. Looking for zero now finds two earlier boundaries, corresponding to `[0..2]` and `[2..2]`. Adding both gives three subarrays. A set would remember zero only once and undercount this final step by one entire valid range.

```trace
{"cells":[1,-1,1],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"prefix":1,"needed":0,"added":1,"answer":1},"note":"The seeded empty prefix starts a range at index zero."},{"at":{"i":1},"vars":{"prefix":0,"needed":-1,"added":0,"answer":1},"note":"Record a second occurrence of prefix zero after lookup."},{"at":{"i":2},"vars":{"prefix":1,"needed":0,"added":2,"answer":3},"note":"Two earlier zero-prefix boundaries create two ranges ending here."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java run
import java.util.HashMap;
import java.util.Map;
public final class PrefixCountBlueprint {
    static long count(int[] a, long k) {
        Map<Long, Integer> frequency = new HashMap<>();
        frequency.put(0L, 1);
        long prefix = 0, answer = 0;
        for (int value : a) {
            prefix += value;
            answer += frequency.getOrDefault(prefix - k, 0);
            frequency.merge(prefix, 1, Integer::sum);
        }
        return answer;
    }
    public static void main(String[] args) {
        if (count(new int[] {1, -1, 1}, 1) != 3) throw new AssertionError();
    }
}
```

Each value causes expected O(1) map work, so time is O(n) expected and space is O(n). `Long` keys and `Integer` counts incur boxing; primitive maps can reduce allocation in performance-sensitive code. The empty array returns zero, while the seeded boundary remains an internal identity rather than an empty result.

<!-- stage: applicability -->
### When It Applies

Use this method when a contiguous additive condition can be rearranged into “current prefix needs an earlier prefix with value X,” and the output asks how many ranges exist. The invariant is that map frequencies describe all and only earlier boundaries.

The false friend is an earliest-index map, which preserves one occurrence to maximize length but loses multiplicity. Another false friend is a positive-only sliding window; negatives destroy its monotone repair rule. Never insert before lookup when empty ranges are disallowed. In Java, use `long` keys and a `long` answer even if every element is `int`.

<!-- stage: exercises -->
### Exercises

#### [Build] Subarray Sum Equals K (LeetCode 560)
<!-- id: ps-subarray-sum-k -->

**Prerequisites.** Prefix construction and hash-map frequencies.

**Problem.** Given an integer array and integer `k`, return the number of non-empty contiguous subarrays whose sum equals `k`.

**Constraints.** `1 <= nums.length <= 2 * 10^4`; values and `k` may be negative; target O(n) expected time.

**Example 1.** Input `nums = [2,-1,2]`, `k = 3`, output `1`.

**Example 2.** Input `nums = [0,0]`, `k = 0`, output `3`.

**Hint.** At each ending boundary, solve `current - earlier = k`. Why must the map store a count rather than a boolean?

**Changed decision.** This rung directly implements target lookup with frequency state.

#### [Vary] Binary Subarrays With Sum (LeetCode 930)
<!-- id: ps-binary-subarrays-sum -->

**Prerequisites.** The prefix-frequency algorithm above.

**Problem.** Given a binary array and integer `goal`, count non-empty contiguous subarrays whose values sum to `goal`.

**Constraints.** `1 <= nums.length <= 3 * 10^4`; `nums[i]` is zero or one; target O(n) time.

**Example 1.** Input `nums = [1,0,1,0]`, `goal = 2`, output `2`.

**Example 2.** Input `nums = [0,0,0]`, `goal = 0`, output `6`.

**Hint.** The binary domain does not change the prefix equation. Which repeated prefix appears many times when zeros arrive?

**Changed decision.** The data domain narrows, making repeated equal prefixes especially common.

#### [Boundary] Zero Target (Author exercise)
<!-- id: ps-zero-target-count -->

**Prerequisites.** Frequency maps and lookup-before-insert ordering.

**Problem.** Count zero-sum subarrays and additionally return the largest frequency ever held by any prefix value during the scan.

**Constraints.** `0 <= nums.length <= 10^5`; target O(n) expected time.

**Example 1.** Input `nums = [1,-1,1,-1]`, output `count = 4`, `maxFrequency = 3`.

**Example 2.** Input `nums = []`, output `count = 0`, `maxFrequency = 1` for the seeded empty prefix.

**Hint.** For target zero, the needed prefix equals the current one. Record the maximum only after merging the current boundary.

**Changed decision.** The target exposes equal-prefix multiplicity and makes the seed part of a second observable result.

#### [Recognize] Count Number of Nice Subarrays (LeetCode 1248)
<!-- id: ps-nice-subarrays -->

**Prerequisites.** Transforming values before applying a known prefix relation.

**Problem.** Given positive integers and `k`, return how many contiguous subarrays contain exactly `k` odd values.

**Constraints.** `1 <= nums.length <= 5 * 10^4`, `1 <= k <= nums.length`; target O(n) time.

**Example 1.** Input `nums = [2,1,2,3]`, `k = 2`, output `2`.

**Example 2.** Input `nums = [2,4,6]`, `k = 1`, output `0`.

**Hint.** Replace each value by the contribution it makes to the odd-count total. Which earlier prefix is then needed?

**Changed decision.** Values contribute a derived zero-or-one feature instead of their numeric magnitude.

