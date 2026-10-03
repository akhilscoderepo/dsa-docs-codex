<!-- solutions-for: 04-object-ordering -->
### Object Ordering

#### Solution: [Build] Sort Scores (Author exercise)
<!-- id: object-sort-scores -->

**Approach.** Copy the list, order score with a reversed integer comparator, and pass equal scores to an ascending name comparison. The oracle checks every permutation for small inputs and chooses the lexicographically first sequence under the stated relation.

**Complexity.** O(n log n * s) time for names of maximum length `s`, and O(n) returned space.

```java run
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Random;

public final class ObjectSortScores {
    record Student(String name, int score) {}

    static final Comparator<Student> ORDER = Comparator.comparingInt(Student::score).reversed()
            .thenComparing(Student::name);

    static List<Student> order(List<Student> input) {
        List<Student> result = new ArrayList<>(input);
        result.sort(ORDER);
        return result;
    }

    static List<Student> brute(List<Student> input) {
        List<List<Student>> candidates = new ArrayList<>();
        permute(new ArrayList<>(input), 0, candidates);
        List<Student> best = null;
        for (List<Student> candidate : candidates)
            if (best == null || compareLists(candidate, best) < 0) best = candidate;
        return best == null ? List.of() : best;
    }

    static void permute(List<Student> values, int at, List<List<Student>> out) {
        if (at == values.size()) { out.add(List.copyOf(values)); return; }
        for (int i = at; i < values.size(); i++) {
            java.util.Collections.swap(values, at, i);
            permute(values, at + 1, out);
            java.util.Collections.swap(values, at, i);
        }
    }

    static int compareLists(List<Student> a, List<Student> b) {
        for (int i = 0; i < a.size(); i++) {
            int result = ORDER.compare(a.get(i), b.get(i));
            if (result != 0) return result;
        }
        return 0;
    }

    static void check(List<Student> input) {
        List<Student> snapshot = List.copyOf(input);
        if (!order(input).equals(brute(input)) || !input.equals(snapshot)) throw new AssertionError(input);
    }

    public static void main(String[] args) {
        check(List.of(new Student("Mira",92), new Student("Ben",85), new Student("Ana",92)));
        check(List.of(new Student("Zed",Integer.MIN_VALUE), new Student("Amy",Integer.MAX_VALUE)));
        Random random = new Random(5401);
        for (int trial = 0; trial < 150; trial++) {
            List<Student> values = new ArrayList<>();
            for (int i = 0, n = random.nextInt(8); i < n; i++)
                values.add(new Student("n" + random.nextInt(8), random.nextInt(7) - 3));
            check(values);
        }
    }
}
```

#### Solution: [Vary] Reorder Data In Log Files (LeetCode 937)
<!-- id: object-reorder-log-files -->

**Approach.** Partition the logs without changing digit-log order. Sort only the letter-logs by content and identifier, then append the untouched digit sequence. The oracle exhaustively chooses the smallest valid permutation of the letter section for small random inputs.

**Complexity.** O(n log n * s) time for maximum log length `s`, and O(n) returned space.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Random;

public final class ObjectReorderLogFiles {
    static boolean digit(String log) {
        return Character.isDigit(log.charAt(log.indexOf(' ') + 1));
    }

    static String id(String log) { return log.substring(0, log.indexOf(' ')); }
    static String body(String log) { return log.substring(log.indexOf(' ') + 1); }

    static final Comparator<String> LETTER_ORDER = Comparator.comparing(ObjectReorderLogFiles::body)
            .thenComparing(ObjectReorderLogFiles::id);

    static String[] reorder(String[] logs) {
        List<String> letters = new ArrayList<>(), digits = new ArrayList<>();
        for (String log : logs) (digit(log) ? digits : letters).add(log);
        letters.sort(LETTER_ORDER);
        letters.addAll(digits);
        return letters.toArray(String[]::new);
    }

    static String[] brute(String[] logs) {
        List<String> letters = new ArrayList<>(), digits = new ArrayList<>();
        for (String log : logs) (digit(log) ? digits : letters).add(log);
        List<List<String>> choices = new ArrayList<>();
        permute(letters, 0, choices);
        List<String> best = null;
        for (List<String> choice : choices) if (best == null || compare(choice, best) < 0) best = choice;
        List<String> result = new ArrayList<>(best == null ? List.of() : best);
        result.addAll(digits);
        return result.toArray(String[]::new);
    }

    static void permute(List<String> values, int at, List<List<String>> out) {
        if (at == values.size()) { out.add(List.copyOf(values)); return; }
        for (int i = at; i < values.size(); i++) {
            java.util.Collections.swap(values, at, i);
            permute(values, at + 1, out);
            java.util.Collections.swap(values, at, i);
        }
    }

    static int compare(List<String> a, List<String> b) {
        for (int i = 0; i < a.size(); i++) {
            int result = LETTER_ORDER.compare(a.get(i), b.get(i));
            if (result != 0) return result;
        }
        return 0;
    }

    static void check(String[] logs) {
        if (!Arrays.equals(reorder(logs), brute(logs))) throw new AssertionError(Arrays.toString(logs));
    }

    public static void main(String[] args) {
        check(new String[] {"dig1 8 1","let1 art can","let2 own kit","let3 art can"});
        check(new String[] {"d1 3 4","d2 1 2"});
        Random random = new Random(93704);
        for (int trial = 0; trial < 200; trial++) {
            List<String> logs = new ArrayList<>();
            for (int i = 0, n = 1 + random.nextInt(7); i < n; i++) {
                if (random.nextBoolean()) logs.add("l" + i + " w" + random.nextInt(4) + " x" + random.nextInt(3));
                else logs.add("d" + i + " " + random.nextInt(10) + " " + random.nextInt(10));
            }
            java.util.Collections.shuffle(logs, random);
            check(logs.toArray(String[]::new));
        }
    }
}
```

#### Solution: [Boundary] Equal Primary Keys (Author exercise)
<!-- id: object-equal-primary-keys -->

**Approach.** Chain all three stated keys and use comparison helpers for both integer fields. An exhaustive permutation oracle selects the first valid tuple sequence on small random cases.

**Complexity.** O(n log n * s) time for owner strings of maximum length `s`, and O(n) returned space.

```java run
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Random;

public final class ObjectEqualPrimaryKeys {
    record Job(int priority, String owner, int id) {}

    static final Comparator<Job> ORDER = Comparator.comparingInt(Job::priority)
            .thenComparing(Job::owner).thenComparingInt(Job::id);

    static List<Job> order(List<Job> input) {
        List<Job> result = new ArrayList<>(input);
        result.sort(ORDER);
        return result;
    }

    static List<Job> brute(List<Job> input) {
        List<List<Job>> choices = new ArrayList<>();
        permute(new ArrayList<>(input), 0, choices);
        List<Job> best = null;
        for (List<Job> choice : choices) if (best == null || compare(choice, best) < 0) best = choice;
        return best == null ? List.of() : best;
    }

    static void permute(List<Job> values, int at, List<List<Job>> out) {
        if (at == values.size()) { out.add(List.copyOf(values)); return; }
        for (int i = at; i < values.size(); i++) {
            java.util.Collections.swap(values, at, i);
            permute(values, at + 1, out);
            java.util.Collections.swap(values, at, i);
        }
    }

    static int compare(List<Job> a, List<Job> b) {
        for (int i = 0; i < a.size(); i++) {
            int result = ORDER.compare(a.get(i), b.get(i));
            if (result != 0) return result;
        }
        return 0;
    }

    static void check(List<Job> input) {
        if (!order(input).equals(brute(input))) throw new AssertionError(input);
    }

    public static void main(String[] args) {
        check(List.of(new Job(1,"ops",9), new Job(1,"ops",2), new Job(1,"api",7)));
        check(List.of(new Job(Integer.MIN_VALUE,"x",Integer.MAX_VALUE), new Job(Integer.MIN_VALUE,"x",Integer.MIN_VALUE)));
        Random random = new Random(5403);
        for (int trial = 0; trial < 150; trial++) {
            List<Job> values = new ArrayList<>();
            for (int i = 0, n = random.nextInt(8); i < n; i++)
                values.add(new Job(random.nextInt(5) - 2, "o" + random.nextInt(4), random.nextInt(9) - 4));
            check(values);
        }
    }
}
```

#### Solution: [Recognize] Queue Reconstruction By Height (LeetCode 406)
<!-- id: object-queue-reconstruction -->

**Approach.** Sort people by height descending and `k` ascending. Every person already in the partial queue is at least as tall as the next person, so inserting that person at index `k` establishes exactly the required count without invalidating taller people. Random tests derive valid inputs from concrete queues and compare the greedy result with an exhaustive existence oracle.

**Complexity.** O(n^2) time because array-list insertion shifts elements, and O(n) returned space.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Random;

public final class ObjectQueueReconstruction {
    static int[][] reconstruct(int[][] people) {
        int[][] ordered = Arrays.stream(people).map(int[]::clone).toArray(int[][]::new);
        Arrays.sort(ordered, Comparator.<int[]>comparingInt(p -> p[0]).reversed()
                .thenComparingInt(p -> p[1]));
        List<int[]> queue = new ArrayList<>();
        for (int[] person : ordered) queue.add(person[1], person);
        return queue.toArray(int[][]::new);
    }

    static boolean valid(int[][] queue) {
        for (int i = 0; i < queue.length; i++) {
            int count = 0;
            for (int j = 0; j < i; j++) if (queue[j][0] >= queue[i][0]) count++;
            if (count != queue[i][1]) return false;
        }
        return true;
    }

    static String key(int[] p) { return p[0] + ":" + p[1]; }

    static boolean samePeople(int[][] a, int[][] b) {
        String[] x = Arrays.stream(a).map(ObjectQueueReconstruction::key).sorted().toArray(String[]::new);
        String[] y = Arrays.stream(b).map(ObjectQueueReconstruction::key).sorted().toArray(String[]::new);
        return Arrays.equals(x, y);
    }

    static boolean bruteExists(int[][] people, int at) {
        if (at == people.length) return valid(people);
        for (int i = at; i < people.length; i++) {
            int[] temp = people[at]; people[at] = people[i]; people[i] = temp;
            if (bruteExists(people, at + 1)) { temp = people[at]; people[at] = people[i]; people[i] = temp; return true; }
            temp = people[at]; people[at] = people[i]; people[i] = temp;
        }
        return false;
    }

    static int[][] descriptors(int[] heights) {
        int[][] people = new int[heights.length][2];
        for (int i = 0; i < heights.length; i++) {
            int k = 0;
            for (int j = 0; j < i; j++) if (heights[j] >= heights[i]) k++;
            people[i] = new int[] {heights[i], k};
        }
        return people;
    }

    static void shuffle(int[][] values, Random random) {
        for (int i = values.length - 1; i > 0; i--) {
            int j = random.nextInt(i + 1);
            int[] temp = values[i]; values[i] = values[j]; values[j] = temp;
        }
    }

    static void check(int[][] input) {
        int[][] actual = reconstruct(input);
        int[][] copy = Arrays.stream(input).map(int[]::clone).toArray(int[][]::new);
        if (!bruteExists(copy, 0) || !valid(actual) || !samePeople(input, actual))
            throw new AssertionError(Arrays.deepToString(input));
    }

    public static void main(String[] args) {
        check(new int[][] {{7,0},{4,4},{7,1},{5,0},{6,1},{5,2}});
        check(new int[][] {{6,0},{5,0}});
        Random random = new Random(40604);
        for (int trial = 0; trial < 120; trial++) {
            int[] heights = random.ints(1 + random.nextInt(8), 1, 8).toArray();
            int[][] people = descriptors(heights);
            shuffle(people, random);
            check(people);
        }
    }
}
```
