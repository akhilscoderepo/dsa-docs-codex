<!-- solutions-for: 03-comparator-contracts -->
### Comparator Contracts

#### Solution: [Build] Safe Integer Comparator (Author exercise)
<!-- id: safe-integer-comparator -->

**Approach.** Copy the boxed array and sort it with `Integer.compare`. The standard method handles the complete integer domain and returns zero for equal values.

**Complexity.** O(n log n) time and O(n) returned space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SafeIntegerComparator {
    static Integer[] order(Integer[] values) {
        Integer[] result = values.clone();
        Arrays.sort(result, Integer::compare);
        return result;
    }

    static void check(Integer[] values) {
        Integer[] expected = values.clone();
        Arrays.sort(expected);
        if (!Arrays.equals(order(values), expected)) throw new AssertionError(Arrays.toString(values));
    }

    public static void main(String[] args) {
        check(new Integer[] {3, -7, 3});
        check(new Integer[] {Integer.MAX_VALUE, Integer.MIN_VALUE});
        Random random = new Random(5301);
        for (int trial = 0; trial < 1_000; trial++) {
            Integer[] values = new Integer[random.nextInt(25)];
            for (int i = 0; i < values.length; i++) values[i] = random.nextInt();
            check(values);
        }
    }
}
```

#### Solution: [Vary] Chained Keys (Author exercise)
<!-- id: comparator-chained-keys -->

**Approach.** Copy the list, compare priorities with `comparingInt`, and hand equal priorities to `thenComparing` for the owner. The input list remains untouched.

**Complexity.** O(n log n * s) time in the worst case for owner strings of length `s`, and O(n) returned space.

```java run
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Random;

public final class ComparatorChainedKeys {
    record Ticket(int priority, String owner) {}

    static List<Ticket> order(List<Ticket> tickets) {
        List<Ticket> result = new ArrayList<>(tickets);
        result.sort(Comparator.comparingInt(Ticket::priority).thenComparing(Ticket::owner));
        return result;
    }

    static void check(List<Ticket> tickets) {
        List<Ticket> result = order(tickets);
        for (int i = 1; i < result.size(); i++) {
            Ticket a = result.get(i - 1), b = result.get(i);
            if (a.priority() > b.priority() || (a.priority() == b.priority() && a.owner().compareTo(b.owner()) > 0))
                throw new AssertionError(result.toString());
        }
    }

    public static void main(String[] args) {
        check(List.of(new Ticket(2,"zoe"), new Ticket(1,"mia"), new Ticket(1,"amy")));
        check(List.of(new Ticket(0,"sam"), new Ticket(0,"sam")));
        Random random = new Random(5302);
        for (int trial = 0; trial < 1_000; trial++) {
            List<Ticket> values = new ArrayList<>();
            for (int i = 0, n = random.nextInt(20); i < n; i++) values.add(new Ticket(random.nextInt(), "u" + random.nextInt(8)));
            check(values);
        }
    }
}
```

#### Solution: [Boundary] Equal Keys And Extreme Values (Author exercise)
<!-- id: comparator-equal-extreme-keys -->

**Approach.** Chain safe integer comparisons for `value` and `id`. Exhaustively test self-comparison, signs in both directions, and every ordered triple in the supplied list.

**Complexity.** O(n^3) time for validation and O(1) extra space.

```java run
import java.util.Comparator;
import java.util.List;
import java.util.Random;
import java.util.ArrayList;

public final class ComparatorEqualExtremeKeys {
    record Entry(int value, int id) {}
    static final Comparator<Entry> ORDER = Comparator.comparingInt(Entry::value).thenComparingInt(Entry::id);

    static int sign(int value) { return Integer.compare(value, 0); }

    static boolean obeysLaws(List<Entry> entries) {
        for (Entry a : entries) {
            if (ORDER.compare(a, a) != 0) return false;
            for (Entry b : entries) {
                if (sign(ORDER.compare(a, b)) != -sign(ORDER.compare(b, a))) return false;
                for (Entry c : entries) {
                    if (ORDER.compare(a, b) <= 0 && ORDER.compare(b, c) <= 0 && ORDER.compare(a, c) > 0) return false;
                }
            }
        }
        return true;
    }

    public static void main(String[] args) {
        if (!obeysLaws(List.of(new Entry(Integer.MIN_VALUE,4), new Entry(Integer.MAX_VALUE,1), new Entry(Integer.MIN_VALUE,2)))) throw new AssertionError("extremes");
        if (!obeysLaws(List.of(new Entry(7,1), new Entry(7,1), new Entry(7,1)))) throw new AssertionError("equal");
        Random random = new Random(5303);
        for (int trial = 0; trial < 300; trial++) {
            List<Entry> entries = new ArrayList<>();
            for (int i = 0, n = random.nextInt(9); i < n; i++) entries.add(new Entry(random.nextInt(), random.nextInt()));
            if (!obeysLaws(entries)) throw new AssertionError(entries.toString());
        }
    }
}
```

#### Solution: [Recognize] Largest Number Comparator (LeetCode 179)
<!-- id: largest-number-comparator-contract -->

**Approach.** Store decimal strings in a list and order two strings by the descending comparison of their possible concatenations. Join the result, reducing an all-zero prefix to one zero.

**Complexity.** O(n log n * d) time for comparisons over at most `d` characters and O(n * d) space.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.Arrays;

public final class LargestNumberComparatorContract {
    static String largestNumber(int[] nums) {
        List<String> parts = new ArrayList<>();
        for (int value : nums) parts.add(String.valueOf(value));
        parts.sort((a, b) -> (b + a).compareTo(a + b));
        if (parts.get(0).equals("0")) return "0";
        return String.join("", parts);
    }

    static String brute(int[] nums, boolean[] used, String current, int depth) {
        if (depth == nums.length) return current.replaceFirst("^0+(?!$)", "");
        String best = "";
        for (int i = 0; i < nums.length; i++) if (!used[i]) {
            used[i] = true;
            String candidate = brute(nums, used, current + nums[i], depth + 1);
            used[i] = false;
            if (candidate.length() > best.length() || (candidate.length() == best.length() && candidate.compareTo(best) > 0)) best = candidate;
        }
        return best;
    }

    static void check(int[] nums) {
        String expected = brute(nums, new boolean[nums.length], "", 0);
        String actual = largestNumber(nums);
        if (!actual.equals(expected)) throw new AssertionError(Arrays.toString(nums));
    }

    public static void main(String[] args) {
        check(new int[] {12,121});
        check(new int[] {0,0});
        Random random = new Random(17903);
        for (int trial = 0; trial < 300; trial++) {
            int[] values = random.ints(1 + random.nextInt(7), 0, 1_000).toArray();
            check(values);
        }
    }
}
```

