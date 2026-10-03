<!-- solutions-for: 02-arrays-sort -->
### Arrays Sort

#### Solution: [Build] Sort A Primitive Copy (Author exercise)
<!-- id: sort-primitive-copy -->

**Approach.** Clone the input, sort the clone with the primitive overload, and return it. The snapshot assertion makes the non-mutation contract observable rather than assumed.

**Complexity.** O(n log n) time and O(n) returned space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SortPrimitiveCopy {
    static int[] sortedCopy(int[] nums) {
        int[] result = nums.clone();
        Arrays.sort(result);
        return result;
    }

    static void check(int[] input) {
        int[] snapshot = input.clone();
        int[] result = sortedCopy(input);
        if (!Arrays.equals(input, snapshot)) throw new AssertionError("input changed");
        for (int i = 1; i < result.length; i++) if (result[i - 1] > result[i]) throw new AssertionError("not sorted");
    }

    public static void main(String[] args) {
        check(new int[] {9, -4, 9, 1});
        check(new int[0]);
        Random random = new Random(501);
        for (int trial = 0; trial < 2_000; trial++) {
            int[] values = random.ints(random.nextInt(40), -100, 101).toArray();
            check(values);
        }
    }
}
```

#### Solution: [Vary] Sort A Subrange (Author exercise)
<!-- id: sort-array-subrange -->

**Approach.** Copy the complete input, then call the range overload with the same half-open bounds. Compare the prefix and suffix with the original in tests, because a globally sorted-looking middle does not prove that the API boundaries were correct.

**Complexity.** O(n + r log r) time and O(n) returned space, where `r = to - from`.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SortArraySubrange {
    static int[] sortRange(int[] nums, int from, int to) {
        int[] result = Arrays.copyOf(nums, nums.length);
        Arrays.sort(result, from, to);
        return result;
    }

    static int[] oracle(int[] nums, int from, int to) {
        int[] middle = Arrays.copyOfRange(nums, from, to);
        Arrays.sort(middle);
        int[] expected = nums.clone();
        System.arraycopy(middle, 0, expected, from, middle.length);
        return expected;
    }

    static void check(int[] nums, int from, int to) {
        if (!Arrays.equals(sortRange(nums, from, to), oracle(nums, from, to))) throw new AssertionError();
    }

    public static void main(String[] args) {
        check(new int[] {8, 5, 3, 7, 1}, 1, 4);
        check(new int[] {4, 2}, 1, 1);
        Random random = new Random(502);
        for (int trial = 0; trial < 1_000; trial++) {
            int[] values = random.ints(random.nextInt(30), -20, 21).toArray();
            int from = random.nextInt(values.length + 1);
            int to = from + random.nextInt(values.length - from + 1);
            check(values, from, to);
        }
    }
}
```

#### Solution: [Boundary] Empty, Singleton, And Extreme Values (Author exercise)
<!-- id: sort-boundary-values -->

**Approach.** Natural primitive ordering already handles empty arrays, singleton arrays, duplicates, and both integer extremes. Copy first to preserve ownership, then apply the overload that requires no comparator.

**Complexity.** O(n log n) time and O(n) returned space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SortBoundaryValues {
    static int[] order(int[] nums) {
        int[] ordered = Arrays.copyOf(nums, nums.length);
        Arrays.sort(ordered);
        return ordered;
    }

    static void check(int[] nums) {
        int[] expected = nums.clone();
        Arrays.sort(expected);
        if (!Arrays.equals(order(nums), expected)) throw new AssertionError(Arrays.toString(nums));
    }

    public static void main(String[] args) {
        check(new int[] {Integer.MAX_VALUE, 0, Integer.MIN_VALUE});
        check(new int[] {42});
        check(new int[0]);
        Random random = new Random(503);
        for (int trial = 0; trial < 1_000; trial++) {
            int[] values = new int[random.nextInt(30)];
            for (int i = 0; i < values.length; i++) values[i] = random.nextInt();
            check(values);
        }
    }
}
```

#### Solution: [Recognize] Contains Duplicate (LeetCode 217)
<!-- id: sort-contains-duplicate -->

**Approach.** Sort a clone so equal values become adjacent, then return as soon as one neighboring pair matches. The oracle uses a set, which is structurally independent from the sort-and-scan implementation.

**Complexity.** O(n log n) time and O(n) space for the clone.

```java run
import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class SortContainsDuplicate {
    static boolean containsDuplicate(int[] nums) {
        int[] ordered = nums.clone();
        Arrays.sort(ordered);
        for (int i = 1; i < ordered.length; i++) {
            if (ordered[i - 1] == ordered[i]) return true;
        }
        return false;
    }

    static boolean bruteForce(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int value : nums) if (!seen.add(value)) return true;
        return false;
    }

    static void check(int[] nums) {
        if (containsDuplicate(nums) != bruteForce(nums)) throw new AssertionError(Arrays.toString(nums));
    }

    public static void main(String[] args) {
        check(new int[] {11, 3, 5, 11});
        check(new int[] {-2, 0, 7, 9});
        Random random = new Random(217);
        for (int trial = 0; trial < 3_000; trial++) {
            int[] values = random.ints(1 + random.nextInt(35), -15, 16).toArray();
            check(values);
        }
    }
}
```

