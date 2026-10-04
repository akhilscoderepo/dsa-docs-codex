<!-- lesson-kind: standard -->
<!-- lesson-id: first-true -->
## First True

<!-- stage: context -->
### The First Broken Release

A service has one hundred numbered releases. Release 1 worked, a later release introduced a defect, and every release after that inherited it. You can run a diagnostic against any release, but each run takes several minutes. The question is not whether a broken release exists. You need the earliest release at which the diagnostic reports a failure, using far fewer than one hundred diagnostic runs.

The important part of the contract is the one-way change. Results begin with a stretch of working releases and end with a stretch of broken releases. We can exploit that order without storing the results in an array.

<!-- stage: naive -->
### Test Releases In Order

The direct method starts at release 1 and calls the diagnostic until it reports a failure. This is correct because the first failure encountered in increasing order must be the earliest broken release.

```java
static int firstBrokenLinear(int releaseCount, java.util.function.IntPredicate isBroken) {
    for (int release = 1; release <= releaseCount; release++) {
        if (isBroken.test(release)) return release;
    }
    return releaseCount + 1;
}
```

The sentinel `releaseCount + 1` represents the optional contract in which every release may work.

<!-- stage: bottleneck -->
### Expensive Calls Near The End

If the defect first appears in release 99 of 100, the scan runs the diagnostic 99 times. With one billion releases and the change near the end, it may make almost one billion remote calls. The loop costs O(n) time and O(n) diagnostic evaluations in the worst case. It also ignores the strongest guarantee in the problem: once a failure has appeared, all later results are already known without being tested.

<!-- stage: insight -->
### Search The Change Point

A **monotone predicate** is a yes-or-no test whose answers change in only one direction across the ordered search domain. Here `isBroken(version)` produces a false prefix followed by a true suffix. The position where that suffix starts is the **first-true boundary**. We can find it with the same half-open binary-search shape used for lower bounds, even when the answers come from a method call instead of a stored array.

<!-- names: monotone predicate, first-true boundary, oracle -->

Treat the diagnostic as an **oracle**: supply a position and receive a boolean answer. Maintain `[lo, hi)`, where every position before `lo` is known false and `hi` is still a possible answer. If the midpoint is true, keep it by moving `hi` to `mid`; an earlier true result may still exist. If it is false, the midpoint and everything before it cannot be the answer, so move `lo` to `mid + 1`.

The safe move depends entirely on monotonicity. A true midpoint proves that every later position is true but says nothing about earlier positions. A false midpoint proves that every earlier position is false. Those implications are what justify discarding half of the remaining domain.

<!-- stage: variables -->
### Boundaries And One Call

`lo` is the first position not yet proved false. `hi` is the exclusive endpoint and a possible sentinel when no position succeeds. `mid` is the position tested during the current iteration, and `value` is the one oracle result saved for that iteration. The interval is half-open, so an input of length `n` begins at `[0, n)` and may legitimately return `n`.

<!-- stage: trace -->
### Keep A True Midpoint

Consider `[false, false, false, true, true, true]`. The search begins with `[0, 6)`. Index 3 is true. It is a candidate, but it might not be the first one, so the interval becomes `[0, 3)`. Index 1 is false, which proves that indices 0 and 1 belong to the false prefix; `lo` moves to 2. Index 2 is also false, so `lo` becomes 3. The endpoints now meet at index 3.

The critical step is the first one. Moving to `hi = mid - 1` would discard a valid candidate under the half-open convention. Stopping immediately would return some true position without proving it is the earliest one.

```trace
{"cells":[false,false,false,true,true,true],"pointers":["lo","mid","hi"],"steps":[{"at":{"lo":0,"mid":3,"hi":6},"vars":{"predicate":true},"note":"A true result keeps mid as a candidate."},{"at":{"lo":0,"mid":1,"hi":3},"vars":{"predicate":false},"note":"A false result proves the prefix impossible."},{"at":{"lo":2,"mid":2,"hi":3},"vars":{"predicate":false},"note":"A false result proves the prefix impossible."}]}
```

<!-- stage: code -->
### A Reusable Boundary Search

```java
static int firstTrue(boolean[] values) {
    int lo = 0, hi = values.length;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (values[mid]) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}
```

The method returns the array length when every value is false. No separate candidate is needed because `hi` keeps a true midpoint possible and the two endpoints collapse onto the boundary. The search takes O(log n) time, performs O(log n) tests, and uses O(1) extra space. With a remote oracle, call it once per iteration and store the result; repeating the call inside several conditions adds avoidable latency and may violate an API call limit.

<!-- stage: applicability -->
### When The Test Changes Once

Use first-true search when an ordered domain has a boolean condition that changes from false to true and the problem asks for the earliest success. State the invariant aloud: every position before `lo` is false, and the first true position, or the sentinel `n`, remains in `[lo, hi]`. This includes release diagnostics, minimum feasible capacities, and counts that eventually reach a target.

The false friend is any test that can alternate, such as `[false, true, false, true]`. One midpoint then tells you nothing reliable about an entire half, so binary search silently discards possible answers. Another false friend is an exact lookup: a true result is only a candidate here, not permission to stop. In Java, use `lo + (hi - lo) / 2`, and document whether all-false input returns `n`, `-1`, or is forbidden by the contract.

<!-- stage: exercises -->
### Exercises

#### [Build] First True Boolean (Author exercise)
<!-- id: bs-first-true-boolean -->

**Prerequisites.** Half-open binary search and the boundary invariant from this lesson.

**Problem.** Given a boolean array containing zero or more `false` values followed by one or more `true` values, return the smallest index whose value is `true`.

**Constraints.** `1 <= values.length <= 10^5`; at least one entry is true; require O(log n) time and O(1) extra space.

**Example 1.** Input `values = [false,false,true,true]`; output `2`.

**Example 2.** Input `values = [true,true,true]`; output `0`.

**Hint.** When the midpoint is true, why must that position remain inside the possible answer interval? Write the meaning of every position before `lo` before choosing the update.

**Changed decision.** The searched property is now a stored boolean transition rather than a comparison against a numeric target.

#### [Vary] First Bad Version (LeetCode 278)
<!-- id: bs-first-bad-version -->

**Prerequisites.** First-true boundary search and a one-based integer search domain.

**Problem.** Versions are numbered from `1` through `n`. An API `isBadVersion(version)` reports whether a version is bad, and every version after the first bad one is also bad. Return the first bad version while minimizing API calls.

**Constraints.** `1 <= firstBad <= n <= 2^31 - 1`; the API is monotone; target O(log n) calls and O(1) space.

**Example 1.** Input `n = 9`, `firstBad = 6`; output `6`.

**Example 2.** Input `n = 1`, `firstBad = 1`; output `1`.

**Hint.** The domain begins at one, and the contract guarantees a bad version. Which closed or half-open endpoints let you keep a bad midpoint without ever asking about version zero?

**Changed decision.** Values are no longer stored locally; each midpoint comparison is an API call on a one-based domain.

#### [Boundary] No True Value (Author exercise)
<!-- id: bs-no-true-value -->

**Prerequisites.** The first-true implementation and its exclusive endpoint convention.

**Problem.** Given a length `n` and a monotone test over indices `0` through `n - 1`, return its first true index. The test may be false everywhere; in that case return the sentinel `n`.

**Constraints.** `0 <= n <= 10^9`; evaluating the test is O(1); require O(log(n + 1)) evaluations and O(1) space.

**Example 1.** Input `n = 5`, test true for `index >= 3`; output `3`.

**Example 2.** Input `n = 4`, test always false; output `4`.

**Hint.** Start with an exclusive endpoint that is never passed to the test. What value remains when every real index joins the proved-false prefix?

**Changed decision.** A successful position is no longer guaranteed, so the exclusive endpoint becomes a meaningful returned sentinel.

#### [Recognize] Kth Missing Positive Number (LeetCode 1539)
<!-- id: bs-kth-missing-positive -->

**Prerequisites.** First-true search, zero-based indexing, and counting how many positive values are absent before an array entry.

**Problem.** Given a strictly increasing array of positive integers and a positive integer `k`, return the `k`th positive integer that does not appear in the array.

**Constraints.** `1 <= arr.length <= 1000`; `1 <= arr[i], k <= 1000`; `arr` is strictly increasing; target O(log n) time.

**Example 1.** Input `arr = [2,5,6,9]`, `k = 4`; output `7`.

**Example 2.** Input `arr = [1,2,4]`, `k = 5`; output `8`.

**Hint.** At index `i`, compare `arr[i]` with the value `i + 1` that would appear if nothing were missing. When does their difference first reach `k`?

**Changed decision.** The boolean transition is derived from a monotone missing-count formula, and the final answer is reconstructed from the boundary.
