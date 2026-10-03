<!-- solutions-for: 01-ordering-contracts -->
### Ordering Contracts

#### Solution: [Build] Sort An Array (LeetCode 912)
<!-- id: sort-array-merge-contract -->

**Approach.** Merge sort gives each recursive half the same ascending contract. Once both halves satisfy it, compare only their front values and move the smaller one into a shared buffer. Copying the merged range back establishes the invariant for the parent range.

**Complexity.** O(n log n) time because every recursion level processes all `n` values, and O(n) auxiliary space for the merge buffer plus O(log n) call-stack depth.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SortArrayMergeContract {
    static int[] sortArray(int[] nums) {
        int[] buffer = new int[nums.length];
        sort(nums, buffer, 0, nums.length);
        return nums;
    }

    static void sort(int[] a, int[] buffer, int from, int to) {
        if (to - from <= 1) return;
        int middle = from + (to - from) / 2;
        sort(a, buffer, from, middle);
        sort(a, buffer, middle, to);
        int left = from, right = middle, write = from;
        while (left < middle || right < to) {
            if (right == to || (left < middle && a[left] <= a[right])) buffer[write++] = a[left++];
            else buffer[write++] = a[right++];
        }
        System.arraycopy(buffer, from, a, from, to - from);
    }

    static void check(int[] input) {
        int[] expected = input.clone();
        Arrays.sort(expected);
        int[] actual = sortArray(input.clone());
        if (!Arrays.equals(actual, expected)) throw new AssertionError(Arrays.toString(input));
    }

    public static void main(String[] args) {
        check(new int[] {8, -1, 4, 4});
        check(new int[] {0});
        Random random = new Random(912);
        for (int trial = 0; trial < 2_000; trial++) {
            int[] values = new int[1 + random.nextInt(30)];
            for (int i = 0; i < values.length; i++) values[i] = random.nextInt(101) - 50;
            check(values);
        }
    }
}
```

#### Solution: [Vary] Sort Boxed Integers In Descending Order (Author exercise)
<!-- id: boxed-integers-descending -->

**Approach.** Copy the object array so the caller retains its sequence. Compare `b` with `a`, which directly describes descending order and avoids negating a potentially unsafe arithmetic difference.

**Complexity.** O(n log n) time for sorting and O(n) additional space for the returned copy.

```java run
import java.util.Arrays;
import java.util.Random;

public final class BoxedIntegersDescending {
    static Integer[] descending(Integer[] values) {
        Integer[] result = Arrays.copyOf(values, values.length);
        Arrays.sort(result, (a, b) -> Integer.compare(b, a));
        return result;
    }

    static Integer[] oracle(Integer[] values) {
        Integer[] result = Arrays.copyOf(values, values.length);
        Arrays.sort(result);
        for (int left = 0, right = result.length - 1; left < right; left++, right--) {
            Integer temporary = result[left];
            result[left] = result[right];
            result[right] = temporary;
        }
        return result;
    }

    static void check(Integer[] input) {
        Integer[] snapshot = input.clone();
        if (!Arrays.equals(descending(input), oracle(input))) throw new AssertionError(Arrays.toString(input));
        if (!Arrays.equals(input, snapshot)) throw new AssertionError("input mutated");
    }

    public static void main(String[] args) {
        check(new Integer[] {6, -3, 6, 2});
        check(new Integer[0]);
        Random random = new Random(51);
        for (int trial = 0; trial < 1_000; trial++) {
            Integer[] values = new Integer[random.nextInt(25)];
            for (int i = 0; i < values.length; i++) values[i] = random.nextInt();
            check(values);
        }
    }
}
```

#### Solution: [Boundary] Extreme Comparator (Author exercise)
<!-- id: extreme-integer-order -->

**Approach.** Sort a copy with `Integer.compare`. The method compares the values without subtracting them, so the sign remains correct across the entire 32-bit range and equal values return zero.

**Complexity.** O(n log n) time and O(n) space for the returned array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ExtremeIntegerOrder {
    static Integer[] ascending(Integer[] values) {
        Integer[] result = Arrays.copyOf(values, values.length);
        Arrays.sort(result, Integer::compare);
        return result;
    }

    static void check(Integer[] input) {
        Integer[] expected = input.clone();
        Arrays.sort(expected);
        if (!Arrays.equals(ascending(input), expected)) throw new AssertionError(Arrays.toString(input));
    }

    public static void main(String[] args) {
        check(new Integer[] {Integer.MAX_VALUE, Integer.MIN_VALUE, 0});
        check(new Integer[] {Integer.MIN_VALUE, Integer.MIN_VALUE});
        Random random = new Random(32);
        for (int trial = 0; trial < 1_000; trial++) {
            Integer[] values = new Integer[random.nextInt(20)];
            for (int i = 0; i < values.length; i++) values[i] = random.nextInt();
            check(values);
        }
    }
}
```

#### Solution: [Recognize] Largest Concatenated Number (LeetCode 179)
<!-- id: largest-concatenated-number -->

**Approach.** Convert each number to a decimal string. For two strings `a` and `b`, place `a` first exactly when `a + b` is lexicographically larger than `b + a`. After sorting, collapse the all-zero case before joining the strings.

**Complexity.** O(n log n * d) time, where `d` bounds the characters examined by one comparison, and O(n * d) space for strings and the result.

```java run
import java.util.Arrays;
import java.util.Random;

public final class LargestConcatenatedNumber {
    static String largestNumber(int[] nums) {
        String[] values = new String[nums.length];
        for (int i = 0; i < nums.length; i++) values[i] = Integer.toString(nums[i]);
        Arrays.sort(values, (a, b) -> (b + a).compareTo(a + b));
        if (values[0].equals("0")) return "0";
        return String.join("", values);
    }

    static String bruteForce(int[] nums) {
        boolean[] used = new boolean[nums.length];
        return choose(nums, used, new StringBuilder(), 0, "");
    }

    static String choose(int[] nums, boolean[] used, StringBuilder current, int depth, String best) {
        if (depth == nums.length) {
            String candidate = current.toString().replaceFirst("^0+(?!$)", "");
            return candidate.compareTo(best) > 0 || candidate.length() > best.length() ? candidate : best;
        }
        for (int i = 0; i < nums.length; i++) {
            if (used[i]) continue;
            used[i] = true;
            int before = current.length();
            current.append(nums[i]);
            best = choose(nums, used, current, depth + 1, best);
            current.setLength(before);
            used[i] = false;
        }
        return best;
    }

    static void check(int[] input) {
        String actual = largestNumber(input);
        String expected = bruteForce(input);
        if (!actual.equals(expected)) throw new AssertionError(Arrays.toString(input) + ": " + actual + " != " + expected);
    }

    public static void main(String[] args) {
        check(new int[] {8, 80, 808});
        check(new int[] {0, 0, 0});
        Random random = new Random(179);
        for (int trial = 0; trial < 500; trial++) {
            int[] values = new int[1 + random.nextInt(7)];
            for (int i = 0; i < values.length; i++) values[i] = random.nextInt(1_000);
            check(values);
        }
    }
}
```

