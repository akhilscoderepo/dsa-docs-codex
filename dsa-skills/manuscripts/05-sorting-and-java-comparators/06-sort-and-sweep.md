<!-- lesson-kind: standard -->
<!-- lesson-id: sort-and-sweep -->
## Sort And Sweep

<!-- stage: context -->
### Repair Duplicate Locker Numbers

A warehouse imports requested locker numbers from several systems. Two workers cannot own the same number. A request may be increased, but it may never be decreased, and each increment costs one. For `[3, 2, 1, 2, 1, 7]`, the assignment should use the fewest total increments.

In arrival order, a request tells us little about what smaller requests will appear later. Once the values are sorted, every number already processed is no greater than the next request. The entire processed prefix can then be summarized by one frontier: the last number that has been assigned.

<!-- stage: naive -->
### Search From Every Request

A direct method keeps a set of used locker numbers. For each request, it repeatedly increments until it finds a free number.

```java nocompile
while (used.contains(value)) {
    value++;
    moves++;
}
used.add(value);
```

This produces a legal assignment. It does not use the fact that many duplicate requests may search through the same occupied stretch independently.

<!-- stage: bottleneck -->
### Dense Runs Are Searched Repeatedly

For thousands of requests for locker `0`, the second search checks `0`, the third checks `0` and `1`, and the final search walks across almost the whole assigned range. The total number of membership checks becomes `1 + 2 + ... + (n - 1)`, or O(n^2), even if each set lookup is expected O(1).

The set also stores every finalized number although the next decision needs only the greatest one. Sorting costs O(n log n), but it creates an order in which a constant-size summary can replace those repeated searches.

<!-- stage: insight -->
### Finalize A Prefix Behind One Frontier

**Sort-and-sweep** first orders the input and then scans from left to right while maintaining a compact summary of everything finalized so far. That summary is the **sweep frontier**. For the locker problem, `previous` is the last assigned number. The next assignment must be at least both its requested value and `previous + 1`.

<!-- names: sort-and-sweep, sweep frontier, finalized prefix -->

The assignment is therefore `current = max(requested, previous + 1)`. Choosing anything larger adds unnecessary cost. Choosing anything smaller either violates the request or duplicates an earlier assignment. This local choice is globally safe because sorting guarantees that no unseen request is smaller than the current request.

After each step, the **finalized prefix** is strictly increasing and has minimum possible cost among all legal assignments for those processed requests. Only its last value can constrain the next request, so earlier values never need to be revisited.

The frontier changes with the problem. It may be the previous value, the best adjacent difference, a merged boundary, or a partial output. The recognition cue is consistent: sorting makes all information that can affect the next item local to a neighbor or a compact prefix summary.

<!-- stage: variables -->
### Requested, Assigned, And Cost

`requested` is the current value in sorted order. `previous` is the number assigned to the preceding request. `assigned` is `max(requested, previous + 1)`. `moves` accumulates `assigned - requested` in a `long`, because many individually small increments can exceed the `int` range. The sweep invariant holds immediately after `previous` is updated.

<!-- stage: trace -->
### Advance Through A Duplicate Run

Sort `[3, 2, 1, 2, 1, 7]` into `[1, 1, 2, 2, 3, 7]`. The first `1` is accepted and establishes the frontier. The second `1` must become `2`, adding one move. The requested `2` behind it must then become `3`, also adding one.

The next `2` becomes `4`, adding two, and requested `3` becomes `5`, adding another two. The final `7` already lies beyond the frontier and costs nothing. The total is six. At no point does the sweep search a set or reconsider an earlier assignment; the frontier carries the only constraint that survives from the finalized prefix.

```trace
{"cells":[1,1,2,2,3,7],"pointers":["scan","frontier"],"steps":[{"at":{"scan":0,"frontier":0},"vars":{"requested":1,"assigned":1,"moves":0},"note":"Accept the first value and establish the frontier at 1."},{"at":{"scan":1,"frontier":1},"vars":{"requested":1,"assigned":2,"moves":1},"note":"Raise the duplicate 1 to the smallest free value, 2."},{"at":{"scan":2,"frontier":2},"vars":{"requested":2,"assigned":3,"moves":2},"note":"The requested 2 is occupied, so the frontier advances to 3."},{"at":{"scan":3,"frontier":3},"vars":{"requested":2,"assigned":4,"moves":4},"note":"The next duplicate crosses the frontier and adds two moves."},{"at":{"scan":4,"frontier":4},"vars":{"requested":3,"assigned":5,"moves":6},"note":"Assign 5; the finalized prefix remains minimally increasing."},{"at":{"scan":5,"frontier":5},"vars":{"requested":7,"assigned":7,"moves":6},"note":"Seven already lies beyond the frontier, so no increment is needed."}]}
```

<!-- stage: code -->
### Keep Only The Frontier

```java run
import java.util.Arrays;

public final class SortAndSweep {
    static long minimumIncrements(int[] nums) {
        if (nums.length < 2) return 0;
        int[] ordered = nums.clone();
        Arrays.sort(ordered);
        long moves = 0;
        long previous = ordered[0];
        for (int i = 1; i < ordered.length; i++) {
            long assigned = Math.max((long) ordered[i], previous + 1);
            moves += assigned - ordered[i];
            previous = assigned;
        }
        return moves;
    }

    public static void main(String[] args) {
        if (minimumIncrements(new int[] {3,2,1,2,1,7}) != 6) throw new AssertionError();
    }
}
```

Sorting costs O(n log n) time and the sweep costs O(n). The copied array costs O(n) space and preserves the input. Both `previous` and `moves` are `long`; `previous + 1` can otherwise overflow when an extreme value is followed by duplicates.

<!-- stage: applicability -->
### When It Applies

Use sort-and-sweep when input order is irrelevant and sorting makes the next decision depend only on an adjacent item or a summary of the finalized prefix. State both pieces of the invariant: the prefix already satisfies the output condition, and the frontier contains everything from that prefix that can constrain the next item.

The false friend is a problem whose original order or indices are part of the answer. Sorting raw values would destroy that information unless the index travels with the record. Intervals often use a sweep frontier too, but endpoint semantics and overlap ownership require their own chapter.

The method silently fails when the frontier omits relevant state, when a greedy local move is not the smallest legal move, or when arithmetic overflows. Equal values and long duplicate runs are the hostile cases for this lesson. An empty input has no frontier and returns zero; a singleton is already valid.

<!-- stage: exercises -->
### Exercises

#### [Build] Squares Of A Sorted Array (LeetCode 977)
<!-- id: sweep-sorted-squares-baseline -->

**Prerequisites.** Array copying, integer widening, and complete sorting.

**Problem.** Given a nondecreasing integer array `nums`, return an array of the squares of each value in nondecreasing order. For this baseline, square every value and then sort the result.

**Constraints.** `1 <= nums.length <= 10^4`; `-10^4 <= nums[i] <= 10^4`; the returned squares fit in `int`.

**Example 1.** Input `[-4,-1,0,3,10]`, output `[0,1,9,16,100]`.

**Example 2.** Input `[-2,-2]`, output `[4,4]`.

**Hint.** The input order is not preserved by squaring across zero. Perform the transformation first, then restore the order needed by the scan.

**Changed decision.** Sorting is used after a value transformation rather than directly on the supplied values.

#### [Vary] Queue Reconstruction By Height (LeetCode 406)
<!-- id: sweep-queue-reconstruction -->

**Prerequisites.** Descending object order and insertion into a partial sequence.

**Problem.** Each person is `[height, k]`, where `k` counts people in front whose height is at least `height`. Reconstruct and return any queue satisfying every record.

**Constraints.** `1 <= people.length <= 2000`; `0 <= height <= 10^6`; `0 <= k < people.length`; a valid queue is guaranteed.

**Example 1.** Input `[[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]`, one valid output is `[[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]`.

**Example 2.** Input `[[6,0],[5,0]]`, output `[[5,0],[6,0]]`.

**Hint.** Sweep from taller people to shorter people. What does `k` mean when every record already in the partial queue is at least as tall as the current person?

**Changed decision.** The sweep frontier is now an entire valid partial queue, and sorting makes `k` a direct insertion index.

#### [Boundary] A Long Run Of Equal Values (Author exercise)
<!-- id: sweep-long-equal-run -->

**Prerequisites.** The frontier recurrence and `long` accumulation.

**Problem.** Given an already sorted integer array, return the minimum number of increments required to make every value unique. Do not allocate a set or modify the input.

**Constraints.** `0 <= nums.length <= 2 * 10^5`; values are signed 32-bit integers; the answer may exceed `Integer.MAX_VALUE`.

**Example 1.** Input `[5,5,5,5]`, output `6`; assign `[5,6,7,8]` at costs `0+1+2+3`.

**Example 2.** Input `[2147483647,2147483647]`, output `1`; the logical frontier advances beyond the `int` range.

**Hint.** Keep the frontier in a wider type. What is the smallest legal assignment after the previous finalized value?

**Changed decision.** Sorting is guaranteed at entry, so the solution is only the linear sweep and must survive an extreme frontier.

#### [Recognize] Minimum Increment To Make Array Unique (LeetCode 945)
<!-- id: sweep-minimum-increment-unique -->

**Prerequisites.** The Boundary exercise and sorting unsorted input before sweeping.

**Problem.** Given an integer array `nums`, increment any element by one per move. Return the minimum number of moves required to make every value unique.

**Constraints.** `1 <= nums.length <= 10^5`; `0 <= nums[i] <= 10^5`; the official answer fits in a signed 32-bit integer.

**Example 1.** Input `[1,2,2]`, output `1`; increment one `2` to `3`.

**Example 2.** Input `[3,2,1,2,1,7]`, output `6`.

**Hint.** Sort first. For each request, choose the smallest value that is both no smaller than the request and strictly beyond the frontier.

**Changed decision.** The sweep now includes the preprocessing step needed to create its local-order invariant.
