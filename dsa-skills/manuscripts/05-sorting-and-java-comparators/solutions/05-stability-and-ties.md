<!-- solutions-for: 05-stability-and-ties -->
### Stability And Ties

#### Solution: [Build] Stable Score Sort (Author exercise)
<!-- id: stable-score-sort -->

**Approach.** Copy the input and apply Java's stable list sort with score as the only comparator key. The oracle groups scores from greatest to least and scans the original list for each group, making encounter preservation explicit.

**Complexity.** O(n log n) time and O(n) returned space.

```java run
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Random;
import java.util.TreeSet;

public final class StableScoreSort {
    record Submission(String user, int score) {}

    static List<Submission> order(List<Submission> input) {
        List<Submission> result = new ArrayList<>(input);
        result.sort(Comparator.comparingInt(Submission::score).reversed());
        return result;
    }

    static List<Submission> brute(List<Submission> input) {
        TreeSet<Integer> scores = new TreeSet<>(Comparator.reverseOrder());
        for (Submission item : input) scores.add(item.score());
        List<Submission> result = new ArrayList<>();
        for (int score : scores) for (Submission item : input) if (item.score() == score) result.add(item);
        return result;
    }

    static void check(List<Submission> input) {
        List<Submission> snapshot = List.copyOf(input);
        if (!order(input).equals(brute(input)) || !input.equals(snapshot)) throw new AssertionError(input);
    }

    public static void main(String[] args) {
        check(List.of(new Submission("zoe",90), new Submission("amy",80), new Submission("ben",90)));
        check(List.of(new Submission("z",7), new Submission("a",7)));
        Random random = new Random(5501);
        for (int trial = 0; trial < 1_000; trial++) {
            List<Submission> values = new ArrayList<>();
            for (int i = 0, n = random.nextInt(30); i < n; i++)
                values.add(new Submission("u" + i, random.nextInt(9) - 4));
            check(values);
        }
    }
}
```

#### Solution: [Vary] Explicit Index Tie (Author exercise)
<!-- id: explicit-index-tie -->

**Approach.** Decorate each message with its input index, sort by topic and then index, and remove the decoration. The oracle emits topics in ascending order while scanning the original list for each topic.

**Complexity.** O(n log n * s) time for topics of maximum length `s`, and O(n) space.

```java run
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Random;
import java.util.TreeSet;

public final class ExplicitIndexTie {
    record Message(String topic, String text) {}
    record Indexed(Message message, int index) {}

    static List<Message> order(List<Message> input) {
        List<Indexed> decorated = new ArrayList<>();
        for (int i = 0; i < input.size(); i++) decorated.add(new Indexed(input.get(i), i));
        decorated.sort(Comparator.comparing((Indexed x) -> x.message().topic())
                .thenComparingInt(Indexed::index));
        List<Message> result = new ArrayList<>();
        for (Indexed item : decorated) result.add(item.message());
        return result;
    }

    static List<Message> brute(List<Message> input) {
        TreeSet<String> topics = new TreeSet<>();
        for (Message message : input) topics.add(message.topic());
        List<Message> result = new ArrayList<>();
        for (String topic : topics) for (Message message : input)
            if (message.topic().equals(topic)) result.add(message);
        return result;
    }

    static void check(List<Message> input) {
        if (!order(input).equals(brute(input))) throw new AssertionError(input);
    }

    public static void main(String[] args) {
        check(List.of(new Message("ops","third"), new Message("api","first"),
                new Message("ops","fourth"), new Message("api","second")));
        check(List.of(new Message("x","b"), new Message("x","a")));
        Random random = new Random(5502);
        for (int trial = 0; trial < 1_000; trial++) {
            List<Message> values = new ArrayList<>();
            for (int i = 0, n = random.nextInt(30); i < n; i++)
                values.add(new Message("t" + random.nextInt(5), "m" + i));
            check(values);
        }
    }
}
```

#### Solution: [Boundary] Comparator Equality (Author exercise)
<!-- id: comparator-equality-boundary -->

**Approach.** Build the complete three-key comparator. For every ordered pair, compare whether the comparator returns zero with whether all required key fields are equal. Random tests include extreme ranks and repeated tuples.

**Complexity.** O(n^2 * s) time for strings of maximum length `s`, and O(1) extra space.

```java run
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Random;

public final class ComparatorEqualityBoundary {
    record Entry(String group, int rank, String label) {}

    static final Comparator<Entry> ORDER = Comparator.comparing(Entry::group)
            .thenComparingInt(Entry::rank).thenComparing(Entry::label);

    static boolean complete(List<Entry> entries) {
        for (Entry a : entries) for (Entry b : entries) {
            boolean tupleEqual = a.group().equals(b.group()) && a.rank() == b.rank()
                    && a.label().equals(b.label());
            if ((ORDER.compare(a, b) == 0) != tupleEqual) return false;
        }
        return true;
    }

    static boolean brute(List<Entry> entries) {
        for (Entry a : entries) for (Entry b : entries) {
            int expected = a.group().compareTo(b.group());
            if (expected == 0) expected = Integer.compare(a.rank(), b.rank());
            if (expected == 0) expected = a.label().compareTo(b.label());
            boolean equalKeys = expected == 0;
            boolean equalFields = a.group().equals(b.group()) && a.rank() == b.rank() && a.label().equals(b.label());
            if (equalKeys != equalFields) return false;
        }
        return true;
    }

    static void check(List<Entry> entries) {
        if (complete(entries) != brute(entries)) throw new AssertionError(entries);
    }

    public static void main(String[] args) {
        check(List.of(new Entry("a",1,"x"), new Entry("a",1,"y")));
        check(List.of(new Entry("a",Integer.MIN_VALUE,"x"), new Entry("a",Integer.MIN_VALUE,"x")));
        Random random = new Random(5503);
        for (int trial = 0; trial < 1_000; trial++) {
            List<Entry> values = new ArrayList<>();
            for (int i = 0, n = random.nextInt(20); i < n; i++) {
                int rank = random.nextInt(10) == 0 ? Integer.MIN_VALUE : random.nextInt(5) - 2;
                values.add(new Entry("g" + random.nextInt(4), rank, "l" + random.nextInt(4)));
            }
            check(values);
        }
    }
}
```

#### Solution: [Recognize] Sort Integers By The Number Of 1 Bits (LeetCode 1356)
<!-- id: stable-sort-by-bit-count -->

**Approach.** Box the integers so a comparator can order by `Integer.bitCount` and then by numeric value. The exhaustive oracle checks every permutation of small random arrays and selects the smallest sequence under those two keys.

**Complexity.** O(n log n) time and O(n) space for boxed values and the returned array.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Random;

public final class StableSortByBitCount {
    static final Comparator<Integer> ORDER = Comparator.comparingInt(Integer::bitCount)
            .thenComparingInt(Integer::intValue);

    static int[] order(int[] arr) {
        Integer[] boxed = Arrays.stream(arr).boxed().toArray(Integer[]::new);
        Arrays.sort(boxed, ORDER);
        return Arrays.stream(boxed).mapToInt(Integer::intValue).toArray();
    }

    static int[] brute(int[] arr) {
        List<int[]> choices = new ArrayList<>();
        permute(arr.clone(), 0, choices);
        int[] best = null;
        for (int[] choice : choices) if (best == null || compare(choice, best) < 0) best = choice;
        return best == null ? new int[0] : best;
    }

    static void permute(int[] values, int at, List<int[]> out) {
        if (at == values.length) { out.add(values.clone()); return; }
        for (int i = at; i < values.length; i++) {
            int temp = values[at]; values[at] = values[i]; values[i] = temp;
            permute(values, at + 1, out);
            temp = values[at]; values[at] = values[i]; values[i] = temp;
        }
    }

    static int compare(int[] a, int[] b) {
        for (int i = 0; i < a.length; i++) {
            int result = ORDER.compare(a[i], b[i]);
            if (result != 0) return result;
        }
        return 0;
    }

    static void check(int[] arr) {
        if (!Arrays.equals(order(arr), brute(arr))) throw new AssertionError(Arrays.toString(arr));
    }

    public static void main(String[] args) {
        check(new int[] {0,1,2,3,4,5,6,7,8});
        check(new int[] {8,4,2,1});
        Random random = new Random(135605);
        for (int trial = 0; trial < 250; trial++) {
            int[] values = random.ints(1 + random.nextInt(8), 0, 64).toArray();
            check(values);
        }
    }
}
```
