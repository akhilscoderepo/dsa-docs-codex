<!-- lesson-kind: standard -->
<!-- lesson-id: prefix-xor -->
## Prefix XOR

<!-- stage: context -->
### Toggle History Queries

A device records each configuration change as a bit mask. A set bit means that feature was toggled during that event. Support engineers repeatedly ask which features were toggled an odd number of times between two event indices. The log never changes, but the queried range does. Scanning the same events for every request works, yet it repeats nearly all of the work. We need a boundary summary that matches the toggle operation itself.

<!-- stage: naive -->
### Replay Every Requested Range

The direct method starts with zero and XORs every value from `left` through `right`. It is correct because XOR records whether each bit appears an odd or even number of times in that range.

```java run
public final class XorRangeNaive {
    static int query(int[] values, int left, int right) {
        int answer = 0;
        for (int i = left; i <= right; i++) answer ^= values[i];
        return answer;
    }
    public static void main(String[] args) {
        if (query(new int[] {5, 1, 7, 3}, 1, 3) != 5) throw new AssertionError();
    }
}
```

<!-- stage: bottleneck -->
### The Same Prefix Is Replayed

Suppose 100,000 requests all begin near the front of a 100,000-event log. Each request replays tens of thousands of values that earlier requests already processed. One query costs O(n) in the worst case, so the full workload can cost O(nq), roughly ten billion XOR operations when both sizes are 100,000. The log is immutable, so paying again for a known boundary state is avoidable.

<!-- stage: insight -->
### Cancel Equal History

Build a **prefix XOR** array with a sentinel: `prefixXor[i]` is the XOR of the first `i` values, so it describes the boundary immediately before index `i`. For an inclusive range `[left, right]`, the state after `right` is `prefixXor[right + 1]`. That state contains both the history before `left` and the requested range. XOR it with `prefixXor[left]`.

<!-- names: prefix XOR, XOR cancellation -->

The history before `left` appears twice, and **XOR cancellation** removes it because `x ^ x = 0`; zero is the identity because `x ^ 0 = x`. Therefore `prefixXor[right + 1] ^ prefixXor[left]` leaves exactly the requested values. Unlike addition, XOR needs no inverse operator: applying the same aggregate again undoes it. The sentinel also gives a real state to the empty prefix, so a range beginning at index zero uses the same formula. The safe move follows from XOR being associative and every value being its own inverse.

<!-- stage: variables -->
### Boundaries And Queries

`prefixXor` has length `n + 1`, and `prefixXor[0]` represents no values. Entry `prefixXor[i + 1]` includes `values[i]`. A query uses inclusive input endpoints `left` and `right`, but reads the half-open boundaries `left` and `right + 1`. `answer` is the XOR between those two boundaries.

<!-- stage: trace -->
### One History Cancels

Use the event masks `[5, 1, 7, 3]` and ask for indices 1 through 3. Begin with boundary state zero. Including 5 produces the next state `5`. Including 1 changes it to `4`; including 7 changes it to `3`; including 3 changes it back to `0`.

The right boundary of the query is after index 3, where the stored state is `0`. Its left boundary is before index 1, where the stored state is `5`. XORing those boundaries gives `0 ^ 5 = 5`. The prefix containing index 0 was present in both histories and vanished. A direct replay confirms that `1 ^ 7 ^ 3` is also `5`. The important step is choosing `right + 1`; reading `prefixXor[right]` would omit the query's final value.

```trace
{"cells":[5,1,7,3],"pointers":["i","left","right"],"steps":[{"at":{"i":0},"vars":{"value":5,"prefixXor":5},"note":"Include index 0; the boundary after it now stores XOR 5."},{"at":{"i":1},"vars":{"value":1,"prefixXor":4},"note":"Include index 1; the boundary after it now stores XOR 4."},{"at":{"i":2},"vars":{"value":7,"prefixXor":3},"note":"Include index 2; the boundary after it now stores XOR 3."},{"at":{"i":3},"vars":{"value":3,"prefixXor":0},"note":"Include index 3; the boundary after it now stores XOR 0."},{"at":{"left":1,"right":3},"vars":{"prefixAfterRight":0,"prefixBeforeLeft":5,"answer":5},"note":"XOR the two boundary states; the shared prefix cancels."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java run
public final class PrefixXorBlueprint {
    static int[] build(int[] values) {
        int[] prefixXor = new int[values.length + 1];
        for (int i = 0; i < values.length; i++) {
            prefixXor[i + 1] = prefixXor[i] ^ values[i];
        }
        return prefixXor;
    }

    static int query(int[] prefixXor, int left, int right) {
        return prefixXor[right + 1] ^ prefixXor[left];
    }

    public static void main(String[] args) {
        int[] prefixXor = build(new int[] {5, 1, 7, 3});
        if (query(prefixXor, 1, 3) != 5) throw new AssertionError();
        if (query(prefixXor, 0, 0) != 5) throw new AssertionError();
    }
}
```

Preprocessing costs O(n) time and O(n) space. Each later query costs O(1) time and no additional space. Java's `^` works bit by bit on signed integers; the sign bit participates like every other bit, so negative values need no special branch. Parenthesize mixed bitwise expressions instead of relying on precedence that a reviewer must remember.

<!-- stage: applicability -->
### When It Applies

Use prefix XOR when immutable contiguous ranges ask for XOR, parity masks, or odd-versus-even occurrence state. The invariant is that `prefixXor[i]` equals the XOR of exactly the values before boundary `i`; combining two boundaries cancels their shared history.

The false friend is a prefix sum: subtraction reverses addition, but subtraction does not reverse XOR. Another false friend is using this table for updates; changing one source value invalidates every later prefix state. A Fenwick tree or segment tree belongs to a later chapter when queries and updates are interleaved. A frequency map becomes useful only when the task counts ranges with a target XOR rather than answering specified queries.

<!-- stage: exercises -->
### Exercises

#### [Build] XOR Queries of a Subarray (LeetCode 1310)
<!-- id: ps-xor-range-queries -->

**Prerequisites.** Prefix boundary conventions and the XOR cancellation identity from this lesson.

**Problem.** Given an integer array `arr` and inclusive queries `[left, right]`, return the XOR of the values in each queried subarray in the original query order.

**Constraints.** `1 <= arr.length, queries.length <= 3 * 10^4`; all indices are valid; target O(n + q) time and O(n) preprocessing space.

**Example 1.** Input `arr = [6,2,9,4]`, `queries = [[0,1],[1,3]]`, output `[4,15]`.

**Example 2.** Input `arr = [12]`, `queries = [[0,0]]`, output `[12]`.

**Hint.** Store a state for every boundary, including the boundary before index zero. Which two boundaries enclose an inclusive query?

**Changed decision.** The prefix operation changes from addition to XOR, so cancellation replaces subtraction.

#### [Vary] Count XOR K (Author exercise)
<!-- id: ps-count-xor-k -->

**Prerequisites.** Prefix-count maps and prefix XOR states.

**Problem.** Given an integer array `nums` and integer `k`, return how many non-empty contiguous subarrays have XOR exactly `k`.

**Constraints.** `0 <= nums.length <= 10^5`; the answer fits in `long`; target O(n) expected time and O(n) space.

**Example 1.** Input `nums = [4,2,2,6]`, `k = 6`, output `3`.

**Example 2.** Input `nums = [0,0]`, `k = 0`, output `3`.

**Hint.** If the current prefix state is `p`, which earlier state `e` makes `e ^ p = k`? Seed the state before the first element.

**Changed decision.** Queries are no longer supplied; a frequency map counts every compatible earlier boundary.

#### [Boundary] Empty Prefix (Author exercise)
<!-- id: ps-xor-empty-prefix -->

**Prerequisites.** Sentinel prefix arrays and inclusive endpoint conversion.

**Problem.** Build a prefix-XOR table and answer only queries whose left endpoint is zero, returning both the answers and the table's first entry for inspection.

**Constraints.** `1 <= nums.length <= 10^5`; every query is `[0, right]`; target O(n + q) time.

**Example 1.** Input `nums = [7,3,5]`, `rights = [0,2]`, output `answers = [7,1]`, `sentinel = 0`.

**Example 2.** Input `nums = [0]`, `rights = [0]`, output `answers = [0]`, `sentinel = 0`.

**Hint.** Do not special-case the left endpoint. What value must represent the empty history so the ordinary two-boundary formula still works?

**Changed decision.** Every range touches the first value, exposing whether the empty-prefix sentinel was modeled correctly.

#### [Recognize] Count Triplets With Equal XOR (LeetCode 1442)
<!-- id: ps-xor-equal-triplets -->

**Prerequisites.** Prefix XOR equality and counting index choices inside a zero-XOR range.

**Problem.** Given `arr`, count triples `(i, j, k)` with `0 <= i < j <= k < n` such that the XOR of `arr[i..j-1]` equals the XOR of `arr[j..k]`.

**Constraints.** `1 <= arr.length <= 300`, `1 <= arr[i] <= 10^8`; target O(n^2) time and O(n) space or better.

**Example 1.** Input `arr = [1,1,1]`, output `2`.

**Example 2.** Input `arr = [5]`, output `0` because no valid middle index exists.

**Hint.** Equal left and right XOR values mean the full range from `i` through `k` has XOR zero. Once its two prefix boundaries match, how many positions may `j` occupy?

**Changed decision.** A repeated prefix state contributes several middle-index choices instead of one range answer.
