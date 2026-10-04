<!-- lesson-kind: standard -->
<!-- lesson-id: touching-boundary-semantics -->
## Touching-Boundary Semantics

<!-- stage: context -->
### The Handoff At Ten

A meeting room is reserved from 9:00 until 10:00, and another meeting begins at 10:00. Most calendar systems allow that handoff: the first reservation no longer owns the room when the second begins. Now change the records to coverage ranges. One sensor covers positions from 9 through 10, and another covers positions from 10 through 11. Both sensors cover position 10.

The endpoint values are identical in both stories. The answer changes because the first story excludes its end and the second includes it. Before an interval algorithm compares endpoints, its contract must say which model the endpoints use.

<!-- stage: naive -->
### Keep One Familiar Predicate

A first implementation often uses the overlap test remembered from merge intervals:

```java
static boolean overlaps(int[] first, int[] second) {
    return Math.max(first[0], second[0]) <= Math.min(first[1], second[1]);
}
```

This is correct when both boundary values belong to a range. Reusing it for reservations is the mistake: two back-to-back bookings are reported as competing for the same resource.

<!-- stage: bottleneck -->
### Equality Has Two Meanings

Take `[540,600)` and `[600,660)`. The code computes `600 <= 600`, returns `true`, and may allocate a second room even though the first meeting releases the room at minute 600. Changing the operator everywhere to `<` repairs that calendar but breaks closed ranges such as `[1,3]` and `[3,5]`, whose intersection is the single point `[3,3]`.

The predicate itself costs O(1); runtime is not the bottleneck. The failure is semantic duplication. If different methods silently choose different equality rules, a sort, merge, resource counter, and intersection routine can disagree on the same input.

<!-- stage: insight -->
### Make The Model Part Of State

The **endpoint contract** says whether a boundary belongs to its interval. A **closed interval** `[a,b]` contains both endpoints, so `[a,b]` and `[c,d]` overlap when `max(a,c) <= min(b,d)`. Equality represents a one-point intersection. A **half-open interval** `[a,b)` contains its start but excludes its end, so the corresponding predicate uses `<`. Equality represents a clean handoff.

<!-- names: endpoint contract, closed interval, half-open interval, degenerate interval -->

This distinction also determines the meaning of a **degenerate interval**. Under a valid closed contract, `[x,x]` contains one point. Under a half-open contract, `[x,x)` is empty. Empty ranges normally contribute no reservation, coverage, or merge output; the surrounding API must either allow and ignore them or reject them explicitly.

The safe move is to choose the model at the public boundary and pass it to every operation that depends on overlap. The invariant is then precise: the overlap predicate is true exactly when the mathematical intersection under that declared model is nonempty. No later scan has to reinterpret equality.

<!-- stage: variables -->
### The Intersection Boundaries

`left` is the later of the two starts. `right` is the earlier of the two ends. For closed ranges, the intersection is nonempty when `left <= right`; both bounds are included. For half-open ranges, it is nonempty when `left < right`; `right` is excluded. A `BoundaryModel` value owns that single equality decision.

<!-- stage: trace -->
### Follow The Equality Case

Compare `[1,3]` with `[3,5]`. The later start and earlier end are both `3`. Under the closed model, the candidate intersection is `[3,3]`. It contains position 3, so the predicate returns true. Under the half-open model, the same boundaries describe `[3,3)`. There is no value that is at least 3 and less than 3, so the predicate returns false.

The second pair makes the zero-length consequence visible. Closed `[2,2]` is a real one-point range and intersects closed `[2,4]`. Half-open `[2,2)` is empty and must not reserve a resource or enlarge a union. The arithmetic never changed; only the membership rule did. That is why the model belongs beside the data contract, not as a late patch to one loop.

```trace
{"cells":["[1,3]","[3,5]","[2,2]","[2,4]"],"pointers":["left","right"],"steps":[{"at":{"left":3,"right":3},"vars":{"model":"closed","intersection":"[3,3]","overlap":true},"note":"Equality leaves a shared endpoint, so the closed ranges overlap."},{"at":{"left":3,"right":3},"vars":{"model":"half-open","intersection":"[3,3)","overlap":false},"note":"The half-open intersection is empty, so the earlier reservation releases the resource."},{"at":{"left":2,"right":2},"vars":{"model":"closed","intersection":"[2,2]","overlap":true},"note":"Equality leaves a shared endpoint, so the closed ranges overlap."},{"at":{"left":2,"right":2},"vars":{"model":"half-open","intersection":"[2,2)","overlap":false},"note":"The half-open intersection is empty, so the earlier reservation releases the resource."}]}
```

<!-- stage: code -->
### Centralize The Equality Rule

```java run
public final class IntervalBoundaryModel {
    enum BoundaryModel { CLOSED, HALF_OPEN }

    static boolean overlaps(int[] first, int[] second, BoundaryModel model) {
        int left = Math.max(first[0], second[0]);
        int right = Math.min(first[1], second[1]);
        return model == BoundaryModel.CLOSED ? left <= right : left < right;
    }

    public static void main(String[] args) {
        int[] first = {1, 3};
        int[] second = {3, 5};
        if (!overlaps(first, second, BoundaryModel.CLOSED)) throw new AssertionError("closed touch");
        if (overlaps(first, second, BoundaryModel.HALF_OPEN)) throw new AssertionError("half-open handoff");
        if (!overlaps(new int[] {2, 2}, new int[] {2, 4}, BoundaryModel.CLOSED)) throw new AssertionError("closed point");
        if (overlaps(new int[] {2, 2}, new int[] {2, 4}, BoundaryModel.HALF_OPEN)) throw new AssertionError("empty half-open range");
    }
}
```

The method performs O(1) work and uses O(1) extra space. `Math.max` and `Math.min` avoid subtraction and therefore cannot overflow while comparing extreme endpoints. The enum makes callers acknowledge the contract. In a performance-sensitive inner loop where the model never changes, use a model-specific method so the branch is outside the scan, but keep the name explicit.

<!-- stage: applicability -->
### When It Applies

Ask about boundary semantics whenever the prompt says that ranges touch, a resource is released at an end time, endpoints are inclusive, or a zero-length range is possible. The invariant to state aloud is: `overlaps` is true exactly when the two intervals share at least one member under the declared endpoint contract.

The nearest false friend is memorizing `nextStart <= activeEnd` as “the merge condition.” It is only the closed-interval merge condition. For half-open ranges the equality case is separation. Another false friend is treating a duration of zero as automatically invalid: `[x,x]` is a valid point in the closed model, while `[x,x)` is empty.

This method silently fails if one input mixes models, such as interpreting one row as closed and another as half-open without carrying that metadata. Java adds no interval type to protect the distinction; raw `int[]` rows look identical. Name the model in the API, validate `start <= end` at the boundary if inputs are untrusted, and never encode infinity by adding one to `Integer.MAX_VALUE`.

<!-- stage: exercises -->
### Exercises

#### [Build] Closed Interval Overlap (Author exercise)
<!-- id: interval-closed-overlap -->

**Prerequisites.** Endpoint ordering vocabulary and integer comparisons.

**Problem.** Given two valid closed integer intervals `[a,b]` and `[c,d]`, return whether their intersection contains at least one point. Both endpoints belong to their intervals.

**Constraints.** `-10^9 <= a <= b <= 10^9` and `-10^9 <= c <= d <= 10^9`; target O(1) time and space.

**Example 1.** Input `[1,3]` and `[3,8]`, output `true` because point `3` belongs to both intervals.

**Example 2.** Input `[-5,-2]` and `[-1,4]`, output `false` because the first range ends before the second begins.

**Hint.** Compute the later start and the earlier end. What relation between them leaves a point in both closed ranges?

**Changed decision.** Equality is accepted because closed intervals include their endpoints.

#### [Vary] Half-Open Reservations (Author exercise)
<!-- id: interval-half-open-shared-resource -->

**Prerequisites.** The closed-overlap predicate and half-open endpoint notation.

**Problem.** Given two valid nonempty reservations `[start,end)`, return whether one resource can serve both without a time conflict. Reservations may appear in either chronological order.

**Constraints.** `0 <= start < end <= 10^9` for each reservation; target O(1) time and space.

**Example 1.** Input `[10,20)` and `[20,35)`, output `true` because the first reservation releases the resource at `20`.

**Example 2.** Input `[18,25)` and `[10,20)`, output `false` because both own the resource from `18` until `20`.

**Hint.** Sharing is possible when one reservation ends no later than the other begins. Write the test symmetrically so input order does not matter.

**Changed decision.** The result asks for compatibility, and equality now represents a legal handoff.

#### [Boundary] Zero-Length Range (Author exercise)
<!-- id: interval-zero-length-models -->

**Prerequisites.** Closed and half-open membership rules.

**Problem.** Given integers `start` and `end` with `start <= end`, return `[closedNonempty, halfOpenNonempty]`, indicating whether the same endpoint pair denotes a nonempty range under each model.

**Constraints.** Endpoints may be any signed 32-bit integers; use no endpoint arithmetic.

**Example 1.** Input `start = 7, end = 7`, output `[true,false]`; `[7,7]` contains one point and `[7,7)` is empty.

**Example 2.** Input `start = MIN, end = MAX`, output `[true,true]` without overflowing either endpoint.

**Hint.** A valid closed range may have equal endpoints. What strict relation is required for a half-open range to contain a member?

**Changed decision.** The overlap rule is applied to one degenerate range rather than to a pair of ranges.

#### [Recognize] Merge Under A Supplied Contract (Author exercise)
<!-- id: interval-merge-supplied-contract -->

**Prerequisites.** Start-ordered intervals, one active union, and this lesson's endpoint models.

**Problem.** Given intervals sorted by start and a model `CLOSED` or `HALF_OPEN`, return their union as sorted, disjoint intervals. Closed ranges that touch must merge; nonempty half-open ranges that touch must remain separate. Do not mutate the input.

**Constraints.** `1 <= intervals.length <= 10^4`; rows satisfy start order; closed rows have `start <= end`, and half-open rows have `start < end`; endpoints fit in signed integers.

**Example 1.** Input `[[1,3],[3,5],[8,9]]` with `CLOSED`, output `[[1,5],[8,9]]` because the first two share endpoint `3`.

**Example 2.** Input `[[1,3],[3,5],[8,9]]` with `HALF_OPEN`, output `[[1,3],[3,5],[8,9]]` because equality is a boundary handoff.

**Hint.** Keep the active interval logic unchanged. Which single comparison decides whether the next row extends it or starts a new output interval?

**Changed decision.** One scan supports two contracts by changing only the equality policy in its overlap predicate.
