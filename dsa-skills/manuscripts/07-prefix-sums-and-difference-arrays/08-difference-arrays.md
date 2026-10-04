<!-- lesson-kind: standard -->
<!-- lesson-id: difference-arrays -->
## Difference Arrays

<!-- stage: context -->
### A Schedule Of Adjustments

A service begins with one staffing target for each day of the month. Operations then submits thousands of adjustments such as "add three engineers from day 6 through day 18" or "remove one engineer from day 12 through day 20." Only the final target for every day is needed. Applying each request day by day is easy to understand, but overlapping requests make the same positions change again and again. We need to record each request without walking across its entire interval.

<!-- stage: naive -->
### Apply Every Request Directly

The direct method visits every index covered by every inclusive update. It is correct because each position receives the value from exactly the updates that contain it. The implementation mirrors the statement and is a useful oracle for small tests.

```java run
public final class RangeUpdatesNaive {
    static long[] apply(int length, int[][] updates) {
        long[] answer = new long[length];
        for (int[] update : updates) {
            for (int i = update[0]; i <= update[1]; i++) answer[i] += update[2];
        }
        return answer;
    }
    public static void main(String[] args) {
        long[] actual = apply(5, new int[][] {{1, 3, 4}});
        if (!java.util.Arrays.equals(actual, new long[] {0, 4, 4, 4, 0})) throw new AssertionError();
    }
}
```

<!-- stage: bottleneck -->
### Wide Updates Repeat Work

Consider 100,000 updates on an array of length 100,000, with most requests covering nearly the whole array. One request performs almost 100,000 additions, and the next request walks across the same positions again. The worst-case cost is O(nu), where `u` is the number of updates. That is about ten billion additions at these limits, even though the result contains only 100,000 values and is materialized once at the end.

<!-- stage: insight -->
### Record Where Effects Change

An inclusive update `[left, right]` with value `v` has only two events: its effect begins at `left`, and its effect stops immediately after `right`. A **difference array** stores those events rather than every affected value. Add `v` at `delta[left]`, then add `-v` at `delta[right + 1]`. Later, a running sum of `delta` reconstructs how much adjustment is active at each position.

<!-- names: difference array, boundary delta -->

Each event is a **boundary delta**. When reconstruction crosses the left boundary, the running adjustment gains `v`. It keeps that value across the whole interval because nothing changes inside the interval. When reconstruction crosses `right + 1`, adding `-v` cancels the update. Overlapping requests combine automatically because their boundary deltas add at the same positions.

Allocate `n + 1` delta entries. The extra sentinel makes `right + 1` a valid write even when `right` is the final array index. We reconstruct only the first `n` positions; the sentinel exists to close effects cleanly. The safe move follows from addition being associative: boundary events may be recorded in any order, and one prefix scan accumulates exactly the events active at each position.

<!-- stage: variables -->
### Events And Materialized Values

`delta` has length `n + 1` and stores changes at boundaries, not final values. Each update uses inclusive `left` and `right` endpoints. `running` is the sum of all boundary events seen through the current index, so it equals the total adjustment active there. `answer[i]` stores that reconstructed value. Use `long` when overlapping updates can push the total outside the `int` range.

<!-- stage: trace -->
### Three Updates Become Events

Start with six zeroes. Record `+3` on indices 1 through 4 by writing `+3` at boundary 1 and `-3` at boundary 5. Record `-1` on indices 3 through 5 by writing `-1` at boundary 3 and `+1` at the sentinel boundary 6. Finally, record `+2` on indices 0 through 2. Its stop event also lands at boundary 3, so that slot becomes `-3`: one request stops contributing two while another begins contributing negative one.

The completed event array is `[2, 3, 0, -3, 0, -3, 1]`. Reconstruction now has no interval loop. The running sum becomes 2, 5, 5, 2, 2, and -1 across the six real positions. The sentinel value at index 6 would bring the running total back to zero, but it is not part of the answer. The difficult step is placing cancellation at `right + 1`; putting it at `right` would remove the update one position too early.

```trace
{"cells":[0,0,0,0,0,0],"pointers":["left","right","i"],"steps":[{"at":{"left":1,"right":4},"vars":{"update":1,"value":3,"startDelta":3,"stopDelta":-3},"note":"Record +3 at boundary 1 and -3 at boundary 5."},{"at":{"left":3,"right":5},"vars":{"update":2,"value":-1,"startDelta":-1,"stopDelta":1},"note":"Record -1 at boundary 3 and +1 at boundary 6."},{"at":{"left":0,"right":2},"vars":{"update":3,"value":2,"startDelta":2,"stopDelta":-3},"note":"Record +2 at boundary 0 and -2 at boundary 3."},{"at":{"i":0},"vars":{"delta":2,"running":2},"note":"Reconstruct index 0; its final value is 2."},{"at":{"i":1},"vars":{"delta":3,"running":5},"note":"Reconstruct index 1; its final value is 5."},{"at":{"i":2},"vars":{"delta":0,"running":5},"note":"Reconstruct index 2; its final value is 5."},{"at":{"i":3},"vars":{"delta":-3,"running":2},"note":"Reconstruct index 3; its final value is 2."},{"at":{"i":4},"vars":{"delta":0,"running":2},"note":"Reconstruct index 4; its final value is 2."},{"at":{"i":5},"vars":{"delta":-3,"running":-1},"note":"Reconstruct index 5; its final value is -1."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java run
public final class DifferenceArrayBlueprint {
    static long[] apply(int length, int[][] updates) {
        long[] delta = new long[length + 1];
        for (int[] update : updates) {
            int left = update[0], right = update[1];
            long value = update[2];
            delta[left] += value;
            delta[right + 1] -= value; // sentinel makes the final endpoint safe
        }

        long[] answer = new long[length];
        long running = 0;
        for (int i = 0; i < length; i++) {
            running += delta[i];
            answer[i] = running;
        }
        return answer;
    }

    public static void main(String[] args) {
        long[] actual = apply(6, new int[][] {{1,4,3},{3,5,-1},{0,2,2}});
        long[] expected = {2,5,5,2,2,-1};
        if (!java.util.Arrays.equals(actual, expected)) throw new AssertionError();
    }
}
```

Recording `u` updates costs O(u) time. Reconstruction costs O(n) time, giving O(n + u) overall and O(n) extra space. The sentinel removes a branch from the update loop, but it must not be returned as a real element. If an existing base array is supplied, add `running` to `base[i]` during reconstruction instead of replacing the value.

<!-- stage: applicability -->
### When It Applies

Use a difference array when many range additions arrive first and the final array is read only after all updates are known. The invariant is that the running sum through boundary `i` equals the total effect of exactly the updates whose inclusive intervals contain `i`.

The nearest false friend is a prefix-sum query table. Prefix sums preprocess fixed values so many ranges can be read; difference arrays preprocess range writes so final point values can be materialized. This method silently fails as an online structure when a query must be answered between updates, because reconstruction would have to be repeated. Fenwick and segment trees handle that later contract. In Java, store `delta` as `long[]` if `numberOfUpdates * maximumAbsoluteValue` can exceed `Integer.MAX_VALUE`, even when each individual update fits in `int`.

<!-- stage: exercises -->
### Exercises

#### [Build] One Range Add (Author exercise)
<!-- id: ps-diff-one-range-add -->

**Prerequisites.** Inclusive array endpoints and the boundary-event model from this lesson.

**Problem.** Given a length `n`, inclusive endpoints `left` and `right`, and an integer `value`, return the length-`n` zero-filled array after adding `value` to every index from `left` through `right`.

**Constraints.** `1 <= n <= 100000`; `0 <= left <= right < n`; `-10^9 <= value <= 10^9`; use O(n) time and O(n) space.

**Example 1.** Input `n = 5`, `left = 1`, `right = 3`, `value = 4`, output `[0,4,4,4,0]`.

**Example 2.** Input `n = 1`, `left = 0`, `right = 0`, `value = -2`, output `[-2]`.

**Hint.** Which boundary turns the value on, and which boundary lies just beyond the final affected index? Reconstruct only after recording both events.

**Changed decision.** The update is represented by two writes instead of one write per covered position.

#### [Vary] Corporate Flight Bookings (LeetCode 1109)
<!-- id: ps-diff-flight-bookings -->

**Prerequisites.** One-based to zero-based conversion and difference-array reconstruction.

**Problem.** There are `n` flights numbered from 1 through `n`. Each booking `[first, last, seats]` adds `seats` reservations to every flight from `first` through `last`, inclusive. Return the total seats booked on each flight.

**Constraints.** `1 <= n, bookings.length <= 20000`; `1 <= first <= last <= n`; `1 <= seats <= 10000`; target O(n + bookings.length) time.

**Example 1.** Input `n = 4`, `bookings = [[1,2,7],[2,4,3]]`, output `[7,10,3,3]`.

**Example 2.** Input `n = 3`, `bookings = [[3,3,8]]`, output `[0,0,8]`.

**Hint.** Convert both flight endpoints before writing events. After conversion, where does an inclusive update stop contributing?

**Changed decision.** Many one-based inclusive updates now share the same event array before one reconstruction pass.

#### [Boundary] Final Endpoint (Author exercise)
<!-- id: ps-diff-final-endpoint -->

**Prerequisites.** Sentinel allocation and signed range additions.

**Problem.** Given `n` and updates `[left, right, value]`, apply all inclusive updates to an initially zero array. Every update is guaranteed to have `right = n - 1`; return the final array without branching on the ending boundary.

**Constraints.** `1 <= n <= 100000`; `1 <= updates.length <= 100000`; values may be negative; totals fit in `long`; target O(n + updates.length) time.

**Example 1.** Input `n = 4`, `updates = [[0,3,2],[3,3,-1]]`, output `[2,2,2,1]`.

**Example 2.** Input `n = 1`, `updates = [[0,0,9],[0,0,-4]]`, output `[5]`.

**Hint.** Reserve one location that is never copied into the result. What valid index then receives every cancellation event?

**Changed decision.** Every cancellation lies beyond the final real position, forcing the sentinel contract to be explicit.

#### [Recognize] Car Pooling (LeetCode 1094)
<!-- id: ps-diff-car-pooling -->

**Prerequisites.** Difference arrays and half-open trip intervals.

**Problem.** A vehicle travels only east. Each trip `[passengers, from, to]` picks up at `from` and drops off at `to`, so its passengers occupy the vehicle on `[from, to)`. Return whether the passenger count ever exceeds `capacity`.

**Constraints.** `1 <= trips.length <= 1000`; `1 <= passengers <= 100`; `0 <= from < to <= 1000`; `1 <= capacity <= 100000`; target O(trips.length + 1001) time.

**Example 1.** Input `trips = [[2,0,4],[3,4,7]]`, `capacity = 3`, output `true` because the first group exits where the second enters.

**Example 2.** Input `trips = [[2,1,5],[2,3,6]]`, `capacity = 3`, output `false` because four passengers overlap from location 3 to 5.

**Hint.** A trip already supplies its cancellation boundary: passengers leave at `to`, not after it. Process all deltas at a coordinate before testing the load there.

**Changed decision.** The intervals are half-open and reconstruction may stop early as soon as capacity is violated.
