<!-- solutions-for: 02-touching-boundary-semantics -->
### Touching-Boundary Semantics

#### Solution: [Build] Closed Interval Overlap (Author exercise)
<!-- id: interval-closed-overlap -->

**Approach.** The intersection starts at the later start and ends at the earlier end. A closed intersection is nonempty when those boundaries are equal or ordered from left to right. A bounded exhaustive oracle checks whether any integer point belongs to both ranges.

**Complexity.** O(1) time and O(1) extra space.

```java run
public final class ClosedIntervalOverlap {
    static boolean solve(int[] first, int[] second) {
        return Math.max(first[0], second[0]) <= Math.min(first[1], second[1]);
    }

    static boolean brute(int[] first, int[] second) {
        for (int point = -5; point <= 5; point++) {
            if (first[0] <= point && point <= first[1]
                    && second[0] <= point && point <= second[1]) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        if (!solve(new int[] {1,3}, new int[] {3,8})) throw new AssertionError("example 1");
        if (solve(new int[] {-5,-2}, new int[] {-1,4})) throw new AssertionError("example 2");
        for (int a = -5; a <= 5; a++) for (int b = a; b <= 5; b++)
            for (int c = -5; c <= 5; c++) for (int d = c; d <= 5; d++)
                if (solve(new int[] {a,b}, new int[] {c,d}) != brute(new int[] {a,b}, new int[] {c,d}))
                    throw new AssertionError("oracle mismatch");
    }
}
```

#### Solution: [Vary] Half-Open Reservations (Author exercise)
<!-- id: interval-half-open-shared-resource -->

**Approach.** The reservations can share a resource if either one ends no later than the other begins. Using both orders makes the result independent of which reservation is passed first. The oracle enumerates occupied integer time units on a small domain.

**Complexity.** O(1) time and O(1) extra space.

```java run
public final class HalfOpenSharedResource {
    static boolean solve(int[] first, int[] second) {
        return first[1] <= second[0] || second[1] <= first[0];
    }

    static boolean brute(int[] first, int[] second) {
        for (int time = 0; time < 8; time++) {
            boolean inFirst = first[0] <= time && time < first[1];
            boolean inSecond = second[0] <= time && time < second[1];
            if (inFirst && inSecond) return false;
        }
        return true;
    }

    public static void main(String[] args) {
        if (!solve(new int[] {10,20}, new int[] {20,35})) throw new AssertionError("example 1");
        if (solve(new int[] {18,25}, new int[] {10,20})) throw new AssertionError("example 2");
        for (int a = 0; a < 8; a++) for (int b = a + 1; b <= 8; b++)
            for (int c = 0; c < 8; c++) for (int d = c + 1; d <= 8; d++)
                if (solve(new int[] {a,b}, new int[] {c,d}) != brute(new int[] {a,b}, new int[] {c,d}))
                    throw new AssertionError("oracle mismatch");
    }
}
```

#### Solution: [Boundary] Zero-Length Range (Author exercise)
<!-- id: interval-zero-length-models -->

**Approach.** The input contract already guarantees `start <= end`, so the closed range is always nonempty. The half-open range needs at least one value before the excluded end, which requires `start < end`. Direct comparison also works at integer extremes.

**Complexity.** O(1) time and O(1) extra space.

```java run
import java.util.Arrays;

public final class ZeroLengthIntervalModels {
    static boolean[] solve(int start, int end) {
        return new boolean[] {start <= end, start < end};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(solve(7, 7), new boolean[] {true, false})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(Integer.MIN_VALUE, Integer.MAX_VALUE), new boolean[] {true, true})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(-4, -3), new boolean[] {true, true})) throw new AssertionError("negative range");
    }
}
```

#### Solution: [Recognize] Merge Under A Supplied Contract (Author exercise)
<!-- id: interval-merge-supplied-contract -->

**Approach.** Copy the first row into an active union. For each later row, use the selected endpoint model to decide whether equality extends the active union or finalizes it. The quadratic oracle repeatedly merges any overlapping pair, so it does not depend on the optimized scan's start-order argument.

**Complexity.** The supplied start order makes the main scan O(n) time. The returned rows use O(n) space; excluding output, the scan uses O(1) extra state.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Random;

public final class MergeWithEndpointContract {
    enum Model { CLOSED, HALF_OPEN }

    static boolean overlaps(int[] left, int[] right, Model model) {
        return model == Model.CLOSED ? right[0] <= left[1] : right[0] < left[1];
    }

    static int[][] solve(int[][] intervals, Model model) {
        List<int[]> merged = new ArrayList<>();
        for (int[] interval : intervals) {
            if (merged.isEmpty() || !overlaps(merged.get(merged.size() - 1), interval, model)) {
                merged.add(interval.clone());
            } else {
                int[] active = merged.get(merged.size() - 1);
                active[1] = Math.max(active[1], interval[1]);
            }
        }
        return merged.toArray(int[][]::new);
    }

    static int[][] brute(int[][] intervals, Model model) {
        List<int[]> work = new ArrayList<>();
        for (int[] interval : intervals) work.add(interval.clone());
        boolean changed;
        do {
            changed = false;
            outer:
            for (int i = 0; i < work.size(); i++) {
                for (int j = i + 1; j < work.size(); j++) {
                    int[] a = work.get(i), b = work.get(j);
                    int laterStart = Math.max(a[0], b[0]);
                    int earlierEnd = Math.min(a[1], b[1]);
                    boolean meet = model == Model.CLOSED ? laterStart <= earlierEnd : laterStart < earlierEnd;
                    if (meet) {
                        work.set(i, new int[] {Math.min(a[0], b[0]), Math.max(a[1], b[1])});
                        work.remove(j);
                        changed = true;
                        break outer;
                    }
                }
            }
        } while (changed);
        work.sort(Comparator.comparingInt(row -> row[0]));
        return work.toArray(int[][]::new);
    }

    static void check(int[][] intervals, Model model) {
        if (!Arrays.deepEquals(solve(intervals, model), brute(intervals, model)))
            throw new AssertionError(model + " mismatch");
    }

    public static void main(String[] args) {
        int[][] touching = {{1,3},{3,5},{8,9}};
        if (!Arrays.deepEquals(solve(touching, Model.CLOSED), new int[][] {{1,5},{8,9}}))
            throw new AssertionError("example 1");
        if (!Arrays.deepEquals(solve(touching, Model.HALF_OPEN), touching))
            throw new AssertionError("example 2");

        Random random = new Random(1002);
        for (int trial = 0; trial < 1500; trial++) {
            int[][] intervals = new int[1 + random.nextInt(10)][2];
            for (int i = 0; i < intervals.length; i++) {
                int start = random.nextInt(20);
                intervals[i][0] = start;
                intervals[i][1] = start + 1 + random.nextInt(6);
            }
            Arrays.sort(intervals, Comparator.comparingInt(row -> row[0]));
            check(intervals, Model.CLOSED);
            check(intervals, Model.HALF_OPEN);
        }
    }
}
```
