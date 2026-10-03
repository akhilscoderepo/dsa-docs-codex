<!-- solutions-for: 06-sort-and-sweep -->
### Sort And Sweep

#### Solution: [Build] Squares Of A Sorted Array (LeetCode 977)
<!-- id: sweep-sorted-squares-baseline -->

**Approach.** Square into a new array, widening before multiplication, and sort that array. The oracle repeatedly selects the smallest unused square, independent of the implementation sort.

**Complexity.** O(n log n) time and O(n) returned space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SweepSortedSquaresBaseline {
    static int[] sortedSquares(int[] nums) {
        int[] result = new int[nums.length];
        for (int i = 0; i < nums.length; i++) result[i] = (int) ((long) nums[i] * nums[i]);
        Arrays.sort(result);
        return result;
    }

    static int[] brute(int[] nums) {
        int[] squares = new int[nums.length];
        boolean[] used = new boolean[nums.length];
        for (int i = 0; i < nums.length; i++) squares[i] = (int) ((long) nums[i] * nums[i]);
        int[] result = new int[nums.length];
        for (int out = 0; out < result.length; out++) {
            int best = -1;
            for (int i = 0; i < squares.length; i++) if (!used[i] && (best < 0 || squares[i] < squares[best])) best = i;
            used[best] = true;
            result[out] = squares[best];
        }
        return result;
    }

    static void check(int[] nums) {
        if (!Arrays.equals(sortedSquares(nums), brute(nums))) throw new AssertionError(Arrays.toString(nums));
    }

    public static void main(String[] args) {
        check(new int[] {-4,-1,0,3,10});
        check(new int[] {-2,-2});
        Random random = new Random(97706);
        for (int trial = 0; trial < 1_000; trial++) {
            int[] values = random.ints(1 + random.nextInt(30), -100, 101).sorted().toArray();
            check(values);
        }
    }
}
```

#### Solution: [Vary] Queue Reconstruction By Height (LeetCode 406)
<!-- id: sweep-queue-reconstruction -->

**Approach.** Convert each row to a person record, sort height descending and `k` ascending, then sweep by inserting at index `k`. The oracle enumerates possible queues for small random cases and confirms that both a valid arrangement exists and the greedy result satisfies every descriptor.

**Complexity.** O(n^2) time because indexed insertion shifts a suffix, and O(n) returned space.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Random;

public final class SweepQueueReconstruction {
    record Person(int height, int k) {}

    static int[][] reconstruct(int[][] people) {
        List<Person> ordered = new ArrayList<>();
        for (int[] row : people) ordered.add(new Person(row[0], row[1]));
        ordered.sort(Comparator.comparingInt(Person::height).reversed().thenComparingInt(Person::k));
        List<Person> queue = new ArrayList<>();
        for (Person person : ordered) queue.add(person.k(), person);
        return queue.stream().map(p -> new int[] {p.height(), p.k()}).toArray(int[][]::new);
    }

    static boolean valid(int[][] queue) {
        for (int i = 0; i < queue.length; i++) {
            int count = 0;
            for (int j = 0; j < i; j++) if (queue[j][0] >= queue[i][0]) count++;
            if (count != queue[i][1]) return false;
        }
        return true;
    }

    static boolean sameRecords(int[][] a, int[][] b) {
        String[] left = Arrays.stream(a).map(p -> p[0] + ":" + p[1]).sorted().toArray(String[]::new);
        String[] right = Arrays.stream(b).map(p -> p[0] + ":" + p[1]).sorted().toArray(String[]::new);
        return Arrays.equals(left, right);
    }

    static boolean bruteExists(int[][] rows, int at) {
        if (at == rows.length) return valid(rows);
        for (int i = at; i < rows.length; i++) {
            int[] saved = rows[at]; rows[at] = rows[i]; rows[i] = saved;
            boolean found = bruteExists(rows, at + 1);
            saved = rows[at]; rows[at] = rows[i]; rows[i] = saved;
            if (found) return true;
        }
        return false;
    }

    static int[][] describe(int[] queue) {
        int[][] result = new int[queue.length][2];
        for (int i = 0; i < queue.length; i++) {
            int k = 0;
            for (int j = 0; j < i; j++) if (queue[j] >= queue[i]) k++;
            result[i] = new int[] {queue[i], k};
        }
        return result;
    }

    static void shuffle(int[][] rows, Random random) {
        for (int i = rows.length - 1; i > 0; i--) {
            int j = random.nextInt(i + 1);
            int[] saved = rows[i]; rows[i] = rows[j]; rows[j] = saved;
        }
    }

    static void check(int[][] input) {
        int[][] actual = reconstruct(input);
        int[][] copy = Arrays.stream(input).map(int[]::clone).toArray(int[][]::new);
        if (!bruteExists(copy, 0) || !valid(actual) || !sameRecords(input, actual))
            throw new AssertionError(Arrays.deepToString(input));
    }

    public static void main(String[] args) {
        check(new int[][] {{7,0},{4,4},{7,1},{5,0},{6,1},{5,2}});
        check(new int[][] {{6,0},{5,0}});
        Random random = new Random(40606);
        for (int trial = 0; trial < 100; trial++) {
            int[] queue = random.ints(1 + random.nextInt(8), 1, 9).toArray();
            int[][] rows = describe(queue);
            shuffle(rows, random);
            check(rows);
        }
    }
}
```

#### Solution: [Boundary] A Long Run Of Equal Values (Author exercise)
<!-- id: sweep-long-equal-run -->

**Approach.** Sweep the already sorted input with a `long` frontier. A frequency-based oracle moves overflow from each occupied value to the next value on small random ranges.

**Complexity.** O(n) time and O(1) extra space beyond the returned scalar.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SweepLongEqualRun {
    static long minimumIncrements(int[] nums) {
        if (nums.length < 2) return 0;
        long previous = nums[0], moves = 0;
        for (int i = 1; i < nums.length; i++) {
            long assigned = Math.max((long) nums[i], previous + 1);
            moves += assigned - nums[i];
            previous = assigned;
        }
        return moves;
    }

    static long brute(int[] nums) {
        if (nums.length == 0) return 0;
        int min = nums[0], max = nums[nums.length - 1];
        long[] count = new long[max - min + nums.length + 1];
        for (int value : nums) count[value - min]++;
        long moves = 0;
        for (int i = 0; i + 1 < count.length; i++) if (count[i] > 1) {
            long excess = count[i] - 1;
            count[i + 1] += excess;
            moves += excess;
        }
        return moves;
    }

    static void check(int[] nums) {
        if (minimumIncrements(nums) != brute(nums)) throw new AssertionError(Arrays.toString(nums));
    }

    public static void main(String[] args) {
        check(new int[] {5,5,5,5});
        if (minimumIncrements(new int[] {Integer.MAX_VALUE,Integer.MAX_VALUE}) != 1) throw new AssertionError("extreme");
        Random random = new Random(5603);
        for (int trial = 0; trial < 1_000; trial++) {
            int[] values = random.ints(random.nextInt(30), 0, 20).sorted().toArray();
            check(values);
        }
    }
}
```

#### Solution: [Recognize] Minimum Increment To Make Array Unique (LeetCode 945)
<!-- id: sweep-minimum-increment-unique -->

**Approach.** Sort a copy and assign each value at the frontier or beyond it. The oracle uses a frequency array and carries duplicate demand one position at a time, providing an independent count on random bounded inputs.

**Complexity.** O(n log n) time and O(n) space for the preserved sorted copy.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SweepMinimumIncrementUnique {
    static int minimumIncrements(int[] nums) {
        int[] ordered = nums.clone();
        Arrays.sort(ordered);
        long previous = -1, moves = 0;
        for (int value : ordered) {
            long assigned = Math.max((long) value, previous + 1);
            moves += assigned - value;
            previous = assigned;
        }
        return Math.toIntExact(moves);
    }

    static int brute(int[] nums) {
        int max = Arrays.stream(nums).max().orElse(0);
        int[] count = new int[max + nums.length + 1];
        for (int value : nums) count[value]++;
        long moves = 0;
        for (int i = 0; i + 1 < count.length; i++) if (count[i] > 1) {
            int excess = count[i] - 1;
            count[i + 1] += excess;
            moves += excess;
        }
        return Math.toIntExact(moves);
    }

    static void check(int[] nums) {
        if (minimumIncrements(nums) != brute(nums)) throw new AssertionError(Arrays.toString(nums));
    }

    public static void main(String[] args) {
        check(new int[] {1,2,2});
        check(new int[] {3,2,1,2,1,7});
        Random random = new Random(94506);
        for (int trial = 0; trial < 2_000; trial++)
            check(random.ints(1 + random.nextInt(40), 0, 25).toArray());
    }
}
```
