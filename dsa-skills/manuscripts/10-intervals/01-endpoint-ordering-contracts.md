<!-- lesson-kind: standard -->
<!-- lesson-id: endpoint-ordering-contracts -->
## Endpoint Ordering Contracts

<!-- stage: context -->
### Put Bookings In Processing Order

A calendar receives bookings as `[start, end]` pairs in arbitrary order. Before it can merge overlapping bookings, it must know which interval begins first. Equal starts also need a deterministic rule, because a short interval and a long interval expose different coverage information.

The order is part of the algorithm. Sorting by start makes every unresolved interval begin no earlier than the current one, which is the property that later permits one active interval to summarize the processed prefix.

<!-- stage: naive -->
### Subtract The Endpoints

A common comparator subtracts starts and then ends.

```java nocompile
(a, b) -> a[0] != b[0] ? a[0] - b[0] : a[1] - b[1]
```

The expression appears to implement lexicographic order, and it works on ordinary small coordinates. Its sign is not reliable over the complete integer domain.

<!-- stage: bottleneck -->
### Overflow Reverses The Relation

Comparing a start of `Integer.MIN_VALUE` with `Integer.MAX_VALUE` by subtraction wraps to a positive value. The comparator then claims that the earliest possible start belongs after the latest possible start. Sorting still performs O(n log n) comparisons, so the complexity looks healthy while the ordering contract is false.

An incorrect order invalidates every local overlap proof that follows. The defect must be removed at the comparator boundary rather than patched inside the merge scan.

<!-- stage: insight -->
### Declare Keys And Tie Ownership

An **endpoint ordering contract** states the key sequence, each key's direction, and the meaning of a tie. For ordinary merging, use **start order**: smaller start first, then smaller end for deterministic equal starts. `Integer.compare` returns a safe sign without subtraction.

<!-- names: endpoint ordering contract, start order, end order -->

Selection problems may instead need **end order**, because the earliest finishing compatible interval leaves the most room for later choices. That is a different contract, not a harmless comparator variation. The sort key must match the decision the following scan intends to make.

After sorting by start, the invariant is that every processed interval starts no later than every unresolved interval. Therefore, if the next start lies beyond the active end, no later interval can overlap the active interval. This monotone start property is what makes finalization safe.

<!-- stage: variables -->
### Primary And Secondary Endpoints

`start` is the primary key for merging. `end` breaks equal-start ties. `ordered` is a deep-enough copy when the caller's outer array and rows must remain unchanged. The comparator reads endpoint values only and carries no mutable state. Later scans may use `activeEnd`, but ordering itself does not decide whether touching endpoints overlap.

<!-- stage: trace -->
### Follow Equal And Extreme Starts

Consider `[5,8]`, `[1,4]`, `[1,3]`, and `[MIN,-1]`. Safe start comparison places the extreme interval first. The two intervals beginning at `1` tie on the primary key, so their ends decide the order: `[1,3]` precedes `[1,4]`.

The final sequence is `[MIN,-1], [1,3], [1,4], [5,8]`. Every unresolved start is now at least the current start. The trace does not yet merge anything; it establishes the precondition that makes a later overlap scan local and trustworthy. The secondary comparison also makes equal-start ordering reproducible instead of dependent on arrival order. Replacing safe comparison with subtraction can break the very first step.

```trace
{"cells":["[5,8]","[1,4]","[1,3]","[MIN,-1]"],"pointers":["left","right"],"steps":[{"at":{"left":3,"right":0},"vars":{"start":"MIN vs 5"},"note":"Safe comparison places the extreme negative start first."},{"at":{"left":1,"right":2},"vars":{"start":"1 vs 1"},"note":"Equal starts transfer ownership to the end key."},{"at":{"left":2,"right":1},"vars":{"end":"3 vs 4"},"note":"The smaller end places [1,3] before [1,4]."},{"at":{"left":0,"right":3},"vars":{"order":"[MIN,-1],[1,3],[1,4],[5,8]"},"note":"The completed order satisfies the start-order invariant."}]}
```

<!-- stage: code -->
### Copy Rows And Compare Safely

```java run
import java.util.Arrays;
import java.util.Comparator;

public final class EndpointOrdering {
    static int[][] byStart(int[][] intervals) {
        int[][] ordered = Arrays.stream(intervals).map(int[]::clone).toArray(int[][]::new);
        Arrays.sort(ordered, Comparator.<int[]>comparingInt(row -> row[0])
                .thenComparingInt(row -> row[1]));
        return ordered;
    }
    public static void main(String[] args) {
        int[][] result = byStart(new int[][] {{5,8},{1,4},{1,3},{Integer.MIN_VALUE,-1}});
        if (result[0][0] != Integer.MIN_VALUE || result[1][1] != 3) throw new AssertionError();
    }
}
```

Copying all rows costs O(n) time and O(n) output space. Sorting costs O(n log n) comparisons. Each comparison is O(1), and no endpoint subtraction can overflow.

<!-- stage: applicability -->
### When It Applies

Use an endpoint ordering contract before a scan whose correctness depends on earlier starts or earlier ends. The invariant must name the relation: under start order, the processed prefix begins no later than the unresolved suffix; under end order, processed intervals finish no later.

The false friend is choosing end order for merging merely because scheduling problems use it. End order supports compatibility selection, while start order exposes the next possible overlap. Another false friend is assuming that sorting decides whether `[1,3]` touches `[3,5]`; endpoint semantics own that question.

This technique fails when rows are malformed, endpoints violate the stated input contract, or subtraction corrupts comparison signs. Equal intervals are valid ties. Extreme coordinates require safe comparisons. If original positions matter, store them with the interval before sorting.

<!-- stage: exercises -->
### Exercises

#### [Build] Order By Start Then End (Author exercise)
<!-- id: interval-order-start-end -->

**Prerequisites.** Object-array comparators and copying nested arrays.

**Problem.** Given interval rows `[start,end]`, return a new array ordered by start ascending and then end ascending. Preserve every input row.

**Constraints.** `0 <= intervals.length <= 10^5`; endpoints span the signed 32-bit range; every row has length two.

**Example 1.** Input `[[3,7],[1,8],[1,4]]`, output `[[1,4],[1,8],[3,7]]`.

**Example 2.** Input `[[MAX,MAX],[MIN,-1]]`, output `[[MIN,-1],[MAX,MAX]]`.

**Hint.** Chain two safe integer comparisons; do not combine endpoints through subtraction.

**Changed decision.** Both endpoint keys and their tie ownership are explicit.

#### [Vary] Order By End Then Start (Author exercise)
<!-- id: interval-order-end-start -->

**Prerequisites.** The Build exercise and scheduling-by-finish motivation.

**Problem.** Return a new interval array ordered by end ascending and then start ascending. Leave the input unchanged.

**Constraints.** `0 <= intervals.length <= 10^5`; endpoints span the signed 32-bit range.

**Example 1.** Input `[[1,8],[4,6],[2,6]]`, output `[[2,6],[4,6],[1,8]]`.

**Example 2.** Input `[]`, output `[]` with independent outer storage.

**Hint.** Which coordinate owns the first comparison when the next scan wants the earliest finishing candidate?

**Changed decision.** The primary key changes to support a future compatibility choice.

#### [Boundary] Equal And Extreme Endpoints (Author exercise)
<!-- id: interval-order-extreme-endpoints -->

**Prerequisites.** Safe comparison and comparator-law checks.

**Problem.** Return whether the start-then-end comparator orders a supplied interval list nondecreasingly after sorting, including equal and extreme endpoints.

**Constraints.** `0 <= intervals.length <= 200`; endpoints are arbitrary signed integers.

**Example 1.** Input `[[MIN,MAX],[MIN,MIN],[MAX,MAX]]`, output `true`.

**Example 2.** Input `[[7,7],[7,7]]`, output `true`; identical intervals are interchangeable.

**Hint.** Verify each adjacent pair using the same comparator that performed the sort.

**Changed decision.** Hostile endpoint values test the comparator contract rather than interval geometry.

#### [Recognize] Merge Intervals (LeetCode 56)
<!-- id: interval-order-merge-recognition -->

**Prerequisites.** Start ordering and closed-interval overlap.

**Problem.** Given closed intervals, merge every overlapping group and return the resulting non-overlapping intervals in ascending start order.

**Constraints.** `1 <= intervals.length <= 10^4`; `0 <= start <= end <= 10^4`.

**Example 1.** Input `[[1,3],[2,6],[8,10],[15,18]]`, output `[[1,6],[8,10],[15,18]]`.

**Example 2.** Input `[[1,4],[4,5]]`, output `[[1,5]]`; closed intervals overlap at `4`.

**Hint.** After start sorting, which single active interval can still overlap the next row?

**Changed decision.** Ordering becomes preprocessing for an active-union scan.
