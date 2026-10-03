<!-- solutions-for: 08-sort-then-scan -->
### Sort Then Scan

#### Solution: [Build] Third Maximum Number (LeetCode 414)
<!-- id: scan-third-maximum -->

**Approach.** Sort a copy, scan distinct runs from right to left, and return the stored maximum if rank three is never reached. A tree set provides the oracle.

**Complexity.** O(n log n) time and O(n) space.

```java run
import java.util.Arrays;
import java.util.Random;
import java.util.TreeSet;

public final class ScanThirdMaximum {
    static int thirdMaximum(int[] nums) {
        int[] ordered = nums.clone(); Arrays.sort(ordered);
        int maximum = ordered[ordered.length - 1], rank = 1;
        for (int i = ordered.length - 2; i >= 0; i--)
            if (ordered[i] != ordered[i + 1] && ++rank == 3) return ordered[i];
        return maximum;
    }

    static int brute(int[] nums) {
        TreeSet<Integer> set = new TreeSet<>(); for (int value : nums) set.add(value);
        if (set.size() < 3) return set.last();
        set.pollLast(); set.pollLast(); return set.last();
    }

    static void check(int[] nums) { if (thirdMaximum(nums) != brute(nums)) throw new AssertionError(Arrays.toString(nums)); }

    public static void main(String[] args) {
        check(new int[] {3,2,1}); check(new int[] {2,2,3,1});
        check(new int[] {Integer.MIN_VALUE,1,2});
        Random random = new Random(41408);
        for (int trial = 0; trial < 2_000; trial++) check(random.ints(1 + random.nextInt(40), -20, 21).toArray());
    }
}
```

#### Solution: [Vary] Relative Ranks (LeetCode 506)
<!-- id: scan-relative-ranks -->

**Approach.** Pair each score with its original index, sort records by score descending, and write each scan rank into the saved output position. The oracle ranks each athlete by counting larger scores.

**Complexity.** O(n log n) time and O(n) space.

```java run
import java.util.Arrays;
import java.util.Comparator;
import java.util.Random;

public final class ScanRelativeRanks {
    record Athlete(int score, int index) {}

    static String label(int rank) {
        return switch (rank) { case 1 -> "Gold Medal"; case 2 -> "Silver Medal"; case 3 -> "Bronze Medal"; default -> String.valueOf(rank); };
    }

    static String[] ranks(int[] score) {
        Athlete[] ordered = new Athlete[score.length];
        for (int i = 0; i < score.length; i++) ordered[i] = new Athlete(score[i], i);
        Arrays.sort(ordered, Comparator.comparingInt(Athlete::score).reversed());
        String[] result = new String[score.length];
        for (int i = 0; i < ordered.length; i++) result[ordered[i].index()] = label(i + 1);
        return result;
    }

    static String[] brute(int[] score) {
        String[] result = new String[score.length];
        for (int i = 0; i < score.length; i++) {
            int rank = 1;
            for (int other : score) if (other > score[i]) rank++;
            result[i] = label(rank);
        }
        return result;
    }

    static void check(int[] score) { if (!Arrays.equals(ranks(score), brute(score))) throw new AssertionError(Arrays.toString(score)); }

    public static void main(String[] args) {
        check(new int[] {5,4,3,2,1}); check(new int[] {10,3,8,9,4});
        Random random = new Random(50608);
        for (int trial = 0; trial < 1_000; trial++) {
            java.util.Set<Integer> set = new java.util.LinkedHashSet<>();
            int n = 1 + random.nextInt(30); while (set.size() < n) set.add(random.nextInt(1_000));
            check(set.stream().mapToInt(Integer::intValue).toArray());
        }
    }
}
```

#### Solution: [Boundary] Fewer Than K Distinct Values (Author exercise)
<!-- id: scan-fewer-than-k-distinct -->

**Approach.** Generalize the distinct-run scan to target `k`, returning the precomputed maximum when the scan exhausts first. A descending tree set supplies the random oracle.

**Complexity.** O(n log n) time and O(n) space.

```java run
import java.util.Arrays;
import java.util.Comparator;
import java.util.Random;
import java.util.TreeSet;

public final class ScanFewerThanKDistinct {
    static int kthMaximum(int[] nums, int k) {
        int[] ordered = nums.clone(); Arrays.sort(ordered);
        int maximum = ordered[ordered.length - 1], rank = 1;
        if (k == 1) return maximum;
        for (int i = ordered.length - 2; i >= 0; i--)
            if (ordered[i] != ordered[i + 1] && ++rank == k) return ordered[i];
        return maximum;
    }

    static int brute(int[] nums, int k) {
        TreeSet<Integer> set = new TreeSet<>(Comparator.reverseOrder());
        for (int value : nums) set.add(value);
        if (set.size() < k) return set.first();
        int rank = 1; for (int value : set) if (rank++ == k) return value;
        throw new AssertionError();
    }

    static void check(int[] nums, int k) { if (kthMaximum(nums, k) != brute(nums, k)) throw new AssertionError(); }

    public static void main(String[] args) {
        check(new int[] {9,9,4},3); check(new int[] {Integer.MIN_VALUE,0,Integer.MAX_VALUE},2);
        Random random = new Random(5803);
        for (int trial = 0; trial < 2_000; trial++) {
            int[] values = random.ints(1 + random.nextInt(40), -15, 16).toArray();
            check(values, 1 + random.nextInt(45));
        }
    }
}
```

#### Solution: [Recognize] Missing Number (LeetCode 268)
<!-- id: scan-missing-number -->

**Approach.** Sort a copy and return the first index whose value differs from that index. If all stored positions match, return `n`. The oracle marks every present value.

**Complexity.** O(n log n) time and O(n) space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ScanMissingNumber {
    static int missingNumber(int[] nums) {
        int[] ordered = nums.clone(); Arrays.sort(ordered);
        for (int i = 0; i < ordered.length; i++) if (ordered[i] != i) return i;
        return ordered.length;
    }

    static int brute(int[] nums) {
        boolean[] present = new boolean[nums.length + 1];
        for (int value : nums) present[value] = true;
        for (int i = 0; i < present.length; i++) if (!present[i]) return i;
        throw new AssertionError();
    }

    static void check(int[] nums) { if (missingNumber(nums) != brute(nums)) throw new AssertionError(Arrays.toString(nums)); }

    public static void main(String[] args) {
        check(new int[] {3,0,1}); check(new int[] {0,1});
        Random random = new Random(26808);
        for (int trial = 0; trial < 2_000; trial++) {
            int n = 1 + random.nextInt(50), missing = random.nextInt(n + 1), write = 0;
            int[] values = new int[n];
            for (int value = 0; value <= n; value++) if (value != missing) values[write++] = value;
            for (int i = n - 1; i > 0; i--) { int j = random.nextInt(i + 1), t = values[i]; values[i] = values[j]; values[j] = t; }
            check(values);
        }
    }
}
```
