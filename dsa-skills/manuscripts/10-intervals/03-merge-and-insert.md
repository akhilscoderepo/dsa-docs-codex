<!-- lesson-kind: standard -->
<!-- lesson-id: merge-and-insert -->
## Merge And Insert

<!-- stage: context -->
### Add One Maintenance Window

A service team already stores maintenance windows in chronological order. The windows do not overlap, so the schedule is easy to read: `[1,2]`, `[3,5]`, `[6,7]`, `[8,9]`, `[12,15]`. A new repair needs the window `[4,10]`. It intersects three existing windows, but it does not affect the first or last one. The revised schedule should therefore be `[1,2]`, `[3,10]`, `[12,15]`.

This task has two related forms. In the general form, arbitrary intervals must first be placed in start order and then merged. In the insertion form, the input is already sorted and disjoint. That stronger contract lets us preserve the untouched prefix and suffix while changing only one contiguous block in the middle.

<!-- stage: naive -->
### Sort The Schedule Again

The direct solution appends the new interval, sorts every row by start, and then runs an ordinary merge.

```java nocompile
static int[][] insertBySorting(int[][] intervals, int[] added) {
    int[][] all = java.util.Arrays.copyOf(intervals, intervals.length + 1);
    all[intervals.length] = added.clone();
    java.util.Arrays.sort(all, java.util.Comparator.comparingInt(row -> row[0]));
    return mergeSorted(all);
}
```

This method is correct for valid closed intervals. It is also a useful fallback when the original list is not ordered or may already contain overlaps.

<!-- stage: bottleneck -->
### Paying Again For Known Order

For the schedule above, the sort compares rows that were already in their final relative order. Only `[4,10]` is new, yet the method sends all six rows through an O(n log n) sort. With one million stored windows and one insertion, that means roughly twenty million comparisons before the linear merge even begins.

The repeated work is not merely theoretical. A scheduling service may perform many insertions into lists whose order and disjointness were established when they were stored. Re-sorting discards both facts. The better scan should use the first interval that can overlap the new range to find the only region that may change.

<!-- stage: insight -->
### Preserve Before And After

For general merging, start order allows one **active union** to summarize every processed interval that has not been finalized. If the next start is at most the active end under a closed-interval contract, the intervals overlap and the active end becomes the larger end. Otherwise, the active interval is final: no later start can reach back to it.

Insertion adds a stronger idea, the **before-overlap-after partition**. Intervals whose ends are smaller than the new start belong to the before region and can be emitted unchanged. Intervals whose starts are at most the growing new end belong to the overlap region; their union is accumulated by taking the smaller start and larger end. Once an interval starts after that union ends, it and every later interval belong to the after region and can also be emitted unchanged.

<!-- names: active union, before-overlap-after partition -->

The overlap region is contiguous because the input is sorted and internally disjoint. After the scan reaches an interval that starts beyond the active union, every later start is at least as large, so none can overlap it. This monotone start order is the property that makes a single pass safe. No previously emitted interval needs to be revisited.

<!-- stage: variables -->
### One Cursor And One Union

`i` is the index of the first input interval not yet classified. `mergedStart` and `mergedEnd` are inclusive boundaries of the new interval after absorbing every overlapping row seen so far. `result` contains the finalized before region, followed later by the merged interval and the unchanged after region. The tests use `<` for intervals strictly before and `<=` for closed-interval overlap.

<!-- stage: trace -->
### Cross The Three Regions

Insert `[4,10]` into `[1,2]`, `[3,5]`, `[6,7]`, `[8,9]`, `[12,15]`. The first row ends at 2, before the new start 4, so it is copied directly to the result. The next row starts at 3, which is no later than the active end 10. It joins the overlap block and moves the active start left to 3.

The rows `[6,7]` and `[8,9]` also start before the active end. Both are contained by `[3,10]`, so the end stays 10. This containment case matters: assigning the current row's end instead of taking the maximum would incorrectly shrink the union. The next row starts at 12, beyond 10. We now emit `[3,10]`. Start order proves that `[12,15]` and every later row are in the after region, so they pass through unchanged.

```trace
{"cells":["[1,2]","[3,5]","[6,7]","[8,9]","[12,15]"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"region":"before","active":"[4,10]"},"note":"[1,2] ends before 4, so emit it unchanged."},{"at":{"left":1,"right":1},"vars":{"region":"overlap","active":"[3,10]"},"note":"[3,5] overlaps the active range and extends its start to 3."},{"at":{"left":2,"right":2},"vars":{"region":"overlap","active":"[3,10]"},"note":"[6,7] is contained by the active union, so its end does not replace 10."},{"at":{"left":3,"right":3},"vars":{"region":"overlap","active":"[3,10]"},"note":"[8,9] also belongs to the same contiguous overlap block."},{"at":{"left":4,"right":4},"vars":{"region":"after","active":"[3,10]"},"note":"[12,15] starts after 10, so finalize [3,10] and copy the suffix."}]}
```

<!-- stage: code -->
### Scan Without Resorting

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public final class InsertClosedInterval {
    static int[][] insert(int[][] intervals, int[] added) {
        List<int[]> result = new ArrayList<>(intervals.length + 1);
        int i = 0;
        while (i < intervals.length && intervals[i][1] < added[0]) {
            result.add(intervals[i].clone());
            i++;
        }

        int mergedStart = added[0];
        int mergedEnd = added[1];
        while (i < intervals.length && intervals[i][0] <= mergedEnd) {
            mergedStart = Math.min(mergedStart, intervals[i][0]);
            mergedEnd = Math.max(mergedEnd, intervals[i][1]);
            i++;
        }
        result.add(new int[] {mergedStart, mergedEnd});

        while (i < intervals.length) {
            result.add(intervals[i].clone());
            i++;
        }
        return result.toArray(int[][]::new);
    }

    public static void main(String[] args) {
        int[][] schedule = {{1,2},{3,5},{6,7},{8,9},{12,15}};
        int[][] expected = {{1,2},{3,10},{12,15}};
        if (!Arrays.deepEquals(insert(schedule, new int[] {4,10}), expected))
            throw new AssertionError("trace case");
    }
}
```

Each input row is classified once, so insertion takes O(n) time. The returned schedule takes O(n) space, while the scan itself holds O(1) state. Cloning pass-through rows prevents the result from sharing mutable row arrays with the caller. An insertion before every row skips the first loop; an insertion after every row skips the overlap loop and is appended before the empty suffix.

<!-- stage: applicability -->
### When It Applies

Use one active union when intervals can be brought into start order and the output asks for their union. Use the three-region insertion scan when the existing intervals are already sorted and disjoint. The invariant to say aloud is: the result contains finalized disjoint intervals, and at most one active interval may still grow by meeting unresolved input.

The nearest false friend is re-sorting an insertion input even though its contract already provides the order. Another false friend is replacing `mergedEnd` with the next end; containment requires `Math.max`. The scan silently fails if the original list contains an overlap that the insertion never touches, because it assumes those rows are already normalized.

Endpoint semantics still control equality. This lesson uses closed intervals, so a next start equal to the active end overlaps. For half-open reservations, equality is a handoff and the overlap loop needs `<`. Java's `ArrayList<int[]>` stores row references, so clone rows when the API promises an independent result and avoid comparator subtraction if a general merge first sorts arbitrary integer endpoints.

<!-- stage: exercises -->
### Exercises

#### [Build] Merge Intervals (LeetCode 56)
<!-- id: interval-merge-intervals -->

**Prerequisites.** Start-order comparators, closed-boundary overlap, and this lesson's active-union invariant.

**Problem.** Given an unsorted array of closed intervals, combine every overlapping group and return the resulting disjoint intervals in ascending start order.

**Constraints.** `1 <= intervals.length <= 10^4`; `0 <= start <= end <= 10^4`; target O(n log n) time including sorting.

**Example 1.** Input `[[5,8],[1,4],[3,6],[11,13]]`, output `[[1,8],[11,13]]` because the first three ranges form one connected overlap group.

**Example 2.** Input `[[2,2],[2,5],[9,9]]`, output `[[2,5],[9,9]]`; the point interval at 2 overlaps the range beginning at 2.

**Hint.** After sorting by start, ask whether any interval earlier than the active one can still need separate attention. What fact lets one end value summarize the whole processed overlap group?

**Changed decision.** The input has no ordering guarantee, so sorting is required before the active-union scan.

#### [Vary] Merge Already-Sorted Intervals (Author exercise)
<!-- id: interval-merge-already-sorted -->

**Prerequisites.** The Build exercise and an explicit ascending-start input contract.

**Problem.** Given closed intervals already sorted by start, merge all overlaps into a new array without sorting and without mutating any input row.

**Constraints.** `0 <= intervals.length <= 10^5`; endpoints are signed 32-bit integers; starts are nondecreasing; target O(n) time.

**Example 1.** Input `[[-4,-1],[-2,3],[7,8]]`, output `[[-4,3],[7,8]]`.

**Example 2.** Input `[]`, output `[]`; the returned outer array must still be a distinct object.

**Hint.** The comparator's job has already been done by the contract. Which row should be copied when a gap proves that the current union is final?

**Changed decision.** Supplied start order removes the O(n log n) preprocessing step and leaves a linear scan.

#### [Boundary] One Interval Covers Many (Author exercise)
<!-- id: interval-one-covers-many -->

**Prerequisites.** Linear merging of start-sorted closed intervals.

**Problem.** Given start-sorted closed intervals, return how many input rows disappear when the complete union is produced. Contained rows and rows joined through touching endpoints both count as removed.

**Constraints.** `1 <= intervals.length <= 10^5`; `-10^9 <= start <= end <= 10^9`; target O(n) time and O(1) auxiliary state excluding the output-free integer result.

**Example 1.** Input `[[1,20],[2,3],[4,8],[20,25],[30,31]]`, output `3`; the first four rows become one union and only two rows remain.

**Example 2.** Input `[[1,2],[4,5],[7,9]]`, output `0` because every gap finalizes the active interval.

**Hint.** You do not need to store the merged rows. Count how many active unions are finalized, then compare that count with the input size.

**Changed decision.** The output is a removal count, and containment tests whether the active end is preserved with a maximum.

#### [Recognize] Insert Interval (LeetCode 57)
<!-- id: interval-insert-interval -->

**Prerequisites.** The before-overlap-after partition and closed-interval boundary semantics.

**Problem.** Given closed intervals sorted by start and pairwise non-overlapping, insert one new closed interval. Merge every overlap and return a sorted, disjoint array without mutating the inputs.

**Constraints.** `0 <= intervals.length <= 10^4`; `0 <= start <= end <= 10^5`; existing rows are sorted and disjoint; target O(n) time.

**Example 1.** Input `intervals = [[1,2],[5,7],[9,12]]`, `newInterval = [6,10]`, output `[[1,2],[5,12]]`.

**Example 2.** Input `intervals = [[3,5],[8,11]]`, `newInterval = [0,1]`, output `[[0,1],[3,5],[8,11]]`; the overlap region is empty.

**Hint.** Which rows are certainly before the new interval? After merging the only possible overlap block, why can the rest be copied without more comparisons against earlier rows?

**Changed decision.** Only one new interval can disturb the normalized list, so preserve the untouched prefix and suffix instead of sorting again.
