<!-- solutions-for: 04-two-list-intersection -->
### Two-List Intersection

#### Solution: [Build] Intersect One Pair (Author exercise)
<!-- id: interval-intersect-one-pair -->

**Approach.** The common portion starts at the larger start and ends at the smaller end. Under a closed contract, equality still represents one shared point. The randomized check compares this formula with direct integer-point membership over a small domain.

**Complexity.** O(1) time and O(1) auxiliary space; the returned pair uses constant output space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class IntersectOnePair {
    static int[] solve(int[] a, int[] b) {
        int start = Math.max(a[0], b[0]);
        int end = Math.min(a[1], b[1]);
        return start <= end ? new int[] {start, end} : new int[0];
    }

    static int[] brute(int[] a, int[] b) {
        Integer first = null, last = null;
        for (int x = -12; x <= 12; x++) {
            if (a[0] <= x && x <= a[1] && b[0] <= x && x <= b[1]) {
                if (first == null) first = x;
                last = x;
            }
        }
        return first == null ? new int[0] : new int[] {first, last};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(solve(new int[] {2,9}, new int[] {6,12}), new int[] {6,9}))
            throw new AssertionError("example 1");
        if (solve(new int[] {-5,-2}, new int[] {-1,4}).length != 0)
            throw new AssertionError("example 2");
        Random random = new Random(1041);
        for (int trial = 0; trial < 2000; trial++) {
            int a0 = random.nextInt(17) - 8, b0 = random.nextInt(17) - 8;
            int[] a = {a0, a0 + random.nextInt(6)};
            int[] b = {b0, b0 + random.nextInt(6)};
            if (!Arrays.equals(solve(a, b), brute(a, b))) throw new AssertionError("oracle mismatch");
        }
    }
}
```

#### Solution: [Vary] One Interval Against A Sorted List (Author exercise)
<!-- id: interval-one-against-list -->

**Approach.** Skip rows that end before the query begins, emit each nonempty overlap, and stop as soon as a row begins after the query ends. A nested one-pair oracle checks the optimized early-stop scan on generated sorted, disjoint inputs.

**Complexity.** O(n) time in the worst case and O(r) output space for `r` intersections. The scan uses O(1) auxiliary state.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class OneIntervalAgainstList {
    static int[][] solve(int[] query, int[][] intervals) {
        List<int[]> result = new ArrayList<>();
        for (int[] row : intervals) {
            if (row[1] < query[0]) continue;
            if (row[0] > query[1]) break;
            result.add(new int[] {Math.max(row[0], query[0]), Math.min(row[1], query[1])});
        }
        return result.toArray(int[][]::new);
    }

    static int[][] brute(int[] query, int[][] intervals) {
        List<int[]> result = new ArrayList<>();
        for (int[] row : intervals) {
            int start = Math.max(row[0], query[0]);
            int end = Math.min(row[1], query[1]);
            if (start <= end) result.add(new int[] {start, end});
        }
        return result.toArray(int[][]::new);
    }

    public static void main(String[] args) {
        int[][] first = {{1,2},{3,6},{9,12},{15,18}};
        if (!Arrays.deepEquals(solve(new int[] {4,11}, first), new int[][] {{4,6},{9,11}}))
            throw new AssertionError("example 1");
        if (solve(new int[] {20,25}, new int[][] {{-3,0},{2,7},{9,19}}).length != 0)
            throw new AssertionError("example 2");
        Random random = new Random(1042);
        for (int trial = 0; trial < 1600; trial++) {
            int[][] rows = new int[random.nextInt(10)][2];
            int cursor = -10;
            for (int i = 0; i < rows.length; i++) {
                int start = cursor + random.nextInt(3);
                int end = start + random.nextInt(5);
                rows[i] = new int[] {start, end};
                cursor = end + 1 + random.nextInt(3);
            }
            int start = random.nextInt(25) - 12;
            int[] query = {start, start + random.nextInt(9)};
            if (!Arrays.deepEquals(solve(query, rows), brute(query, rows)))
                throw new AssertionError("oracle mismatch");
        }
    }
}
```

#### Solution: [Boundary] Touching Intersections (Author exercise)
<!-- id: interval-touching-intersections -->

**Approach.** Compute the common endpoints with `long` arithmetic. A closed integer overlap contains `end - start + 1` points when `start <= end`; a half-open overlap has span `end - start` only when `start < end`. The oracle enumerates scaled sample points for small ranges and checks both contracts.

**Complexity.** O(1) time and O(1) extra space.

```java run
import java.util.Random;

public final class TouchingIntersectionLength {
    static long solve(int[] a, int[] b, boolean closed) {
        long start = Math.max((long) a[0], b[0]);
        long end = Math.min((long) a[1], b[1]);
        if (closed) return start <= end ? end - start + 1 : 0;
        return start < end ? end - start : 0;
    }

    static long closedBrute(int[] a, int[] b) {
        long count = 0;
        for (int x = -12; x <= 12; x++)
            if (a[0] <= x && x <= a[1] && b[0] <= x && x <= b[1]) count++;
        return count;
    }

    static long halfOpenBrute(int[] a, int[] b) {
        long halfSteps = 0;
        for (int twiceX = -24; twiceX < 24; twiceX++) {
            double x = twiceX / 2.0;
            if (a[0] <= x && x < a[1] && b[0] <= x && x < b[1]) halfSteps++;
        }
        return halfSteps / 2;
    }

    public static void main(String[] args) {
        if (solve(new int[] {1,5}, new int[] {5,9}, true) != 1) throw new AssertionError("example 1");
        if (solve(new int[] {1,5}, new int[] {5,9}, false) != 0) throw new AssertionError("example 2");
        Random random = new Random(1043);
        for (int trial = 0; trial < 2000; trial++) {
            int a0 = random.nextInt(17) - 8, b0 = random.nextInt(17) - 8;
            int[] a = {a0, a0 + random.nextInt(6)};
            int[] b = {b0, b0 + random.nextInt(6)};
            if (solve(a, b, true) != closedBrute(a, b)) throw new AssertionError("closed oracle");
            if (solve(a, b, false) != halfOpenBrute(a, b)) throw new AssertionError("half-open oracle");
        }
    }
}
```

#### Solution: [Recognize] Interval List Intersections (LeetCode 986)
<!-- id: interval-list-intersections -->

**Approach.** For each current pair, emit the maximum-start to minimum-end range when it is nonempty. Then advance the interval with the smaller end, because it cannot intersect a later interval in the opposite list. The oracle compares every cross-list pair and sorts the resulting intersections.

**Complexity.** O(m + n) time and O(r) output space for `r` intersections; pointer state uses O(1) extra space.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Random;

public final class IntervalListIntersectionsExercise {
    static int[][] solve(int[][] first, int[][] second) {
        List<int[]> result = new ArrayList<>();
        int i = 0, j = 0;
        while (i < first.length && j < second.length) {
            int start = Math.max(first[i][0], second[j][0]);
            int end = Math.min(first[i][1], second[j][1]);
            if (start <= end) result.add(new int[] {start, end});
            if (first[i][1] < second[j][1]) i++;
            else if (second[j][1] < first[i][1]) j++;
            else { i++; j++; }
        }
        return result.toArray(int[][]::new);
    }

    static int[][] brute(int[][] first, int[][] second) {
        List<int[]> result = new ArrayList<>();
        for (int[] a : first) for (int[] b : second) {
            int start = Math.max(a[0], b[0]);
            int end = Math.min(a[1], b[1]);
            if (start <= end) result.add(new int[] {start, end});
        }
        result.sort(Comparator.comparingInt((int[] row) -> row[0]).thenComparingInt(row -> row[1]));
        return result.toArray(int[][]::new);
    }

    static int[][] makeList(Random random) {
        int[][] rows = new int[random.nextInt(9)][2];
        int cursor = random.nextInt(4);
        for (int i = 0; i < rows.length; i++) {
            int start = cursor + random.nextInt(3);
            int end = start + random.nextInt(5);
            rows[i] = new int[] {start, end};
            cursor = end + 1 + random.nextInt(3);
        }
        return rows;
    }

    public static void main(String[] args) {
        int[][] first = {{0,3},{7,11},{15,18}};
        int[][] second = {{1,5},{8,10},{11,16}};
        int[][] expected = {{1,3},{8,10},{11,11},{15,16}};
        if (!Arrays.deepEquals(solve(first, second), expected)) throw new AssertionError("example 1");
        if (solve(new int[0][2], new int[][] {{2,4}}).length != 0) throw new AssertionError("example 2");
        Random random = new Random(1044);
        for (int trial = 0; trial < 2000; trial++) {
            int[][] a = makeList(random), b = makeList(random);
            if (!Arrays.deepEquals(solve(a, b), brute(a, b))) throw new AssertionError("oracle mismatch");
        }
    }
}
```
