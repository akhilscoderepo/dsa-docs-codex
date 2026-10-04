<!-- solutions-for: 03-merge-and-insert -->
### Merge And Insert

#### Solution: [Build] Merge Intervals (LeetCode 56)
<!-- id: interval-merge-intervals -->

**Approach.** Sort copied rows by start, then keep the last output row as the active union. A gap finalizes that row; an overlap can only enlarge its end. A pairwise-merging oracle checks small random inputs without relying on the optimized ordering proof.

**Complexity.** Sorting costs O(n log n) time. The output and copied rows use O(n) space; the scan after sorting is O(n).

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Random;

public final class MergeIntervalsExercise {
    static int[][] solve(int[][] intervals) {
        int[][] ordered = Arrays.stream(intervals).map(int[]::clone).toArray(int[][]::new);
        Arrays.sort(ordered, Comparator.comparingInt((int[] row) -> row[0]).thenComparingInt(row -> row[1]));
        List<int[]> result = new ArrayList<>();
        for (int[] row : ordered) {
            if (result.isEmpty() || row[0] > result.get(result.size() - 1)[1]) {
                result.add(row.clone());
            } else {
                int[] active = result.get(result.size() - 1);
                active[1] = Math.max(active[1], row[1]);
            }
        }
        return result.toArray(int[][]::new);
    }

    static int[][] brute(int[][] intervals) {
        List<int[]> work = new ArrayList<>();
        for (int[] row : intervals) work.add(row.clone());
        boolean changed;
        do {
            changed = false;
            outer: for (int i = 0; i < work.size(); i++) {
                for (int j = i + 1; j < work.size(); j++) {
                    int[] a = work.get(i), b = work.get(j);
                    if (Math.max(a[0], b[0]) <= Math.min(a[1], b[1])) {
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

    static void check(int[][] input) {
        if (!Arrays.deepEquals(solve(input), brute(input))) throw new AssertionError("oracle mismatch");
    }

    public static void main(String[] args) {
        int[][] first = {{5,8},{1,4},{3,6},{11,13}};
        if (!Arrays.deepEquals(solve(first), new int[][] {{1,8},{11,13}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(solve(new int[][] {{2,2},{2,5},{9,9}}), new int[][] {{2,5},{9,9}}))
            throw new AssertionError("example 2");
        Random random = new Random(1003);
        for (int trial = 0; trial < 1200; trial++) {
            int[][] input = new int[1 + random.nextInt(9)][2];
            for (int i = 0; i < input.length; i++) {
                int start = random.nextInt(18);
                input[i] = new int[] {start, start + random.nextInt(6)};
            }
            check(input);
        }
    }
}
```

#### Solution: [Vary] Merge Already-Sorted Intervals (Author exercise)
<!-- id: interval-merge-already-sorted -->

**Approach.** Traverse the supplied order and compare each row with the last output union. Copy a row when it starts a new component; otherwise enlarge the active end with `Math.max`. The oracle delegates to a separately sorted general merge.

**Complexity.** The scan costs O(n) time. The returned rows use O(n) space, while the active state is O(1).

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Random;

public final class MergeAlreadySorted {
    static int[][] solve(int[][] intervals) {
        List<int[]> result = new ArrayList<>();
        for (int[] row : intervals) {
            if (result.isEmpty() || row[0] > result.get(result.size() - 1)[1]) result.add(row.clone());
            else result.get(result.size() - 1)[1] = Math.max(result.get(result.size() - 1)[1], row[1]);
        }
        return result.toArray(int[][]::new);
    }

    static int[][] oracle(int[][] intervals) {
        int[][] copy = Arrays.stream(intervals).map(int[]::clone).toArray(int[][]::new);
        Arrays.sort(copy, Comparator.comparingInt(row -> row[0]));
        List<int[]> out = new ArrayList<>();
        for (int[] row : copy) {
            if (out.isEmpty() || row[0] > out.get(out.size() - 1)[1]) out.add(row.clone());
            else out.get(out.size() - 1)[1] = Math.max(out.get(out.size() - 1)[1], row[1]);
        }
        return out.toArray(int[][]::new);
    }

    public static void main(String[] args) {
        if (!Arrays.deepEquals(solve(new int[][] {{-4,-1},{-2,3},{7,8}}), new int[][] {{-4,3},{7,8}}))
            throw new AssertionError("example 1");
        int[][] empty = solve(new int[0][2]);
        if (empty.length != 0) throw new AssertionError("example 2");
        Random random = new Random(1013);
        for (int trial = 0; trial < 1200; trial++) {
            int[][] input = new int[random.nextInt(10)][2];
            for (int i = 0; i < input.length; i++) {
                int start = random.nextInt(21) - 10;
                input[i] = new int[] {start, start + random.nextInt(6)};
            }
            Arrays.sort(input, Comparator.comparingInt(row -> row[0]));
            if (!Arrays.deepEquals(solve(input), oracle(input))) throw new AssertionError("oracle mismatch");
        }
    }
}
```

#### Solution: [Boundary] One Interval Covers Many (Author exercise)
<!-- id: interval-one-covers-many -->

**Approach.** Count the number of union components without materializing them. A start beyond the active end opens a new component; otherwise the row disappears into the active union and the end can only increase. Subtracting the component count from the row count gives the number removed.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Comparator;
import java.util.Random;

public final class CoveredMergeCount {
    static int solve(int[][] intervals) {
        int components = 1;
        int activeEnd = intervals[0][1];
        for (int i = 1; i < intervals.length; i++) {
            if (intervals[i][0] > activeEnd) {
                components++;
                activeEnd = intervals[i][1];
            } else {
                activeEnd = Math.max(activeEnd, intervals[i][1]);
            }
        }
        return intervals.length - components;
    }

    static int oracle(int[][] intervals) {
        boolean[] covered = new boolean[61];
        for (int[] row : intervals) for (int x = row[0]; x <= row[1]; x++) covered[2 * x] = true;
        for (int[] row : intervals) for (int x = row[0]; x < row[1]; x++) covered[2 * x + 1] = true;
        int components = 0;
        boolean inside = false;
        for (boolean point : covered) {
            if (point && !inside) components++;
            inside = point;
        }
        return intervals.length - components;
    }

    public static void main(String[] args) {
        if (solve(new int[][] {{1,20},{2,3},{4,8},{20,25},{30,31}}) != 3) throw new AssertionError("example 1");
        if (solve(new int[][] {{1,2},{4,5},{7,9}}) != 0) throw new AssertionError("example 2");
        Random random = new Random(1023);
        for (int trial = 0; trial < 1500; trial++) {
            int[][] input = new int[1 + random.nextInt(10)][2];
            for (int i = 0; i < input.length; i++) {
                int start = random.nextInt(25);
                input[i] = new int[] {start, start + random.nextInt(6)};
            }
            Arrays.sort(input, Comparator.comparingInt(row -> row[0]));
            if (solve(input) != oracle(input)) throw new AssertionError("oracle mismatch");
        }
    }
}
```

#### Solution: [Recognize] Insert Interval (LeetCode 57)
<!-- id: interval-insert-interval -->

**Approach.** Copy the strict-before prefix, absorb the one contiguous overlap block into the new interval, and copy the strict-after suffix. The oracle adds the row to a general sort-and-merge routine, so random checks compare the linear method with a less specialized path.

**Complexity.** O(n) time. The returned rows use O(n) space and the scan uses O(1) extra state beyond that output.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Random;

public final class InsertIntervalExercise {
    static int[][] solve(int[][] intervals, int[] added) {
        List<int[]> result = new ArrayList<>(intervals.length + 1);
        int i = 0;
        while (i < intervals.length && intervals[i][1] < added[0]) result.add(intervals[i++].clone());
        int start = added[0], end = added[1];
        while (i < intervals.length && intervals[i][0] <= end) {
            start = Math.min(start, intervals[i][0]);
            end = Math.max(end, intervals[i][1]);
            i++;
        }
        result.add(new int[] {start, end});
        while (i < intervals.length) result.add(intervals[i++].clone());
        return result.toArray(int[][]::new);
    }

    static int[][] oracle(int[][] intervals, int[] added) {
        int[][] all = Arrays.copyOf(intervals, intervals.length + 1);
        all[intervals.length] = added.clone();
        Arrays.sort(all, Comparator.comparingInt(row -> row[0]));
        List<int[]> result = new ArrayList<>();
        for (int[] row : all) {
            if (result.isEmpty() || row[0] > result.get(result.size() - 1)[1]) result.add(row.clone());
            else result.get(result.size() - 1)[1] = Math.max(result.get(result.size() - 1)[1], row[1]);
        }
        return result.toArray(int[][]::new);
    }

    public static void main(String[] args) {
        int[][] first = {{1,2},{5,7},{9,12}};
        if (!Arrays.deepEquals(solve(first, new int[] {6,10}), new int[][] {{1,2},{5,12}}))
            throw new AssertionError("example 1");
        if (!Arrays.deepEquals(solve(new int[][] {{3,5},{8,11}}, new int[] {0,1}), new int[][] {{0,1},{3,5},{8,11}}))
            throw new AssertionError("example 2");

        Random random = new Random(1033);
        for (int trial = 0; trial < 1500; trial++) {
            int[][] input = new int[random.nextInt(10)][2];
            int cursor = random.nextInt(3);
            for (int i = 0; i < input.length; i++) {
                int start = cursor + random.nextInt(3);
                int end = start + random.nextInt(4);
                input[i] = new int[] {start, end};
                cursor = end + 1 + random.nextInt(3);
            }
            int start = random.nextInt(Math.max(1, cursor + 3));
            int[] added = {start, start + random.nextInt(7)};
            if (!Arrays.deepEquals(solve(input, added), oracle(input, added)))
                throw new AssertionError("oracle mismatch");
        }
    }
}
```
