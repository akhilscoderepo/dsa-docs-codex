<!-- solutions-for: 07-sort-and-deduplicate -->
### Sort And Deduplicate

#### Solution: [Build] Contains Duplicate (LeetCode 217)
<!-- id: deduplicate-contains-duplicate -->

**Approach.** Sort a copy and return at the first equal adjacent pair. The quadratic oracle compares every original pair on random inputs.

**Complexity.** O(n log n) time and O(n) space for the preserved copy.

```java run
import java.util.Arrays;
import java.util.Random;

public final class DeduplicateContainsDuplicate {
    static boolean containsDuplicate(int[] nums) {
        int[] ordered = nums.clone();
        Arrays.sort(ordered);
        for (int i = 1; i < ordered.length; i++) if (ordered[i] == ordered[i - 1]) return true;
        return false;
    }

    static boolean brute(int[] nums) {
        for (int i = 0; i < nums.length; i++) for (int j = i + 1; j < nums.length; j++)
            if (nums[i] == nums[j]) return true;
        return false;
    }

    static void check(int[] nums) {
        if (containsDuplicate(nums) != brute(nums)) throw new AssertionError(Arrays.toString(nums));
    }

    public static void main(String[] args) {
        check(new int[] {1,2,3,1});
        check(new int[] {1,2,3,4});
        Random random = new Random(21707);
        for (int trial = 0; trial < 2_000; trial++) check(random.ints(1 + random.nextInt(40), -20, 21).toArray());
    }
}
```

#### Solution: [Vary] Intersection Of Two Arrays (LeetCode 349)
<!-- id: deduplicate-array-intersection -->

**Approach.** Store values from the second array in a set, sort a copy of the first, and test only run starts. A direct set intersection is the independent oracle.

**Complexity.** O(n log n + m) expected time and O(n + m) space, where `n` and `m` are the array lengths.

```java run
import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;
import java.util.TreeSet;

public final class DeduplicateArrayIntersection {
    static int[] intersection(int[] nums1, int[] nums2) {
        Set<Integer> present = new HashSet<>();
        for (int value : nums2) present.add(value);
        int[] ordered = nums1.clone();
        Arrays.sort(ordered);
        int write = 0;
        for (int read = 0; read < ordered.length; read++) {
            if (read > 0 && ordered[read] == ordered[read - 1]) continue;
            if (present.contains(ordered[read])) ordered[write++] = ordered[read];
        }
        return Arrays.copyOf(ordered, write);
    }

    static int[] brute(int[] a, int[] b) {
        Set<Integer> left = new HashSet<>(), right = new HashSet<>();
        for (int value : a) left.add(value);
        for (int value : b) right.add(value);
        TreeSet<Integer> result = new TreeSet<>(left);
        result.retainAll(right);
        return result.stream().mapToInt(Integer::intValue).toArray();
    }

    static void check(int[] a, int[] b) {
        if (!Arrays.equals(intersection(a, b), brute(a, b)))
            throw new AssertionError(Arrays.toString(a) + Arrays.toString(b));
    }

    public static void main(String[] args) {
        check(new int[] {1,2,2,1}, new int[] {2,2});
        check(new int[] {4,9,5}, new int[] {9,4,9,8,4});
        Random random = new Random(34907);
        for (int trial = 0; trial < 2_000; trial++)
            check(random.ints(1 + random.nextInt(30), -15, 16).toArray(),
                    random.ints(1 + random.nextInt(30), -15, 16).toArray());
    }
}
```

#### Solution: [Boundary] All Equal (Author exercise)
<!-- id: deduplicate-all-equal -->

**Approach.** Handle empty input before establishing the first representative. Sort and compress into the front of the owned copy. A tree set supplies the random-test oracle.

**Complexity.** O(n log n) time and O(n) returned space.

```java run
import java.util.Arrays;
import java.util.Random;
import java.util.TreeSet;

public final class DeduplicateAllEqual {
    static int[] distinct(int[] nums) {
        if (nums.length == 0) return new int[0];
        int[] ordered = nums.clone();
        Arrays.sort(ordered);
        int write = 1;
        for (int read = 1; read < ordered.length; read++)
            if (ordered[read] != ordered[read - 1]) ordered[write++] = ordered[read];
        return Arrays.copyOf(ordered, write);
    }

    static int[] brute(int[] nums) {
        TreeSet<Integer> set = new TreeSet<>();
        for (int value : nums) set.add(value);
        return set.stream().mapToInt(Integer::intValue).toArray();
    }

    static void check(int[] nums) {
        if (!Arrays.equals(distinct(nums), brute(nums))) throw new AssertionError(Arrays.toString(nums));
    }

    public static void main(String[] args) {
        check(new int[] {4,4,4});
        check(new int[0]);
        check(new int[] {Integer.MIN_VALUE,Integer.MAX_VALUE,Integer.MIN_VALUE});
        Random random = new Random(5703);
        for (int trial = 0; trial < 2_000; trial++) check(random.ints(random.nextInt(50), -10, 11).toArray());
    }
}
```

#### Solution: [Recognize] Longest Word In Dictionary (LeetCode 720)
<!-- id: deduplicate-longest-buildable-word -->

**Approach.** Sort by length and then lexicographically. A word is accepted if it has length one or its one-character-shorter prefix is already accepted. The first accepted word at a greater length becomes the answer. The oracle checks every word's complete prefix chain directly.

**Complexity.** O(n log n * s + n * s) time and O(n * s) space for maximum word length `s`.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class DeduplicateLongestBuildableWord {
    static String longestWord(String[] words) {
        String[] ordered = words.clone();
        Arrays.sort(ordered, Comparator.comparingInt(String::length).thenComparing(Comparator.naturalOrder()));
        Set<String> accepted = new HashSet<>();
        String best = "";
        for (String word : ordered) {
            if (word.length() == 1 || accepted.contains(word.substring(0, word.length() - 1))) {
                accepted.add(word);
                if (word.length() > best.length()) best = word;
            }
        }
        return best;
    }

    static String brute(String[] words) {
        Set<String> all = new HashSet<>(Arrays.asList(words));
        String best = "";
        for (String word : words) {
            boolean valid = true;
            for (int length = 1; length < word.length(); length++)
                if (!all.contains(word.substring(0, length))) { valid = false; break; }
            if (valid && (word.length() > best.length()
                    || (word.length() == best.length() && word.compareTo(best) < 0))) best = word;
        }
        return best;
    }

    static void check(String[] words) {
        if (!longestWord(words).equals(brute(words))) throw new AssertionError(Arrays.toString(words));
    }

    public static void main(String[] args) {
        check(new String[] {"w","wo","wor","worl","world"});
        check(new String[] {"a","banana","app","appl","ap","apply","apple"});
        Random random = new Random(72007);
        for (int trial = 0; trial < 1_000; trial++) {
            List<String> words = new ArrayList<>();
            for (int i = 0, n = 1 + random.nextInt(30); i < n; i++) {
                int length = 1 + random.nextInt(5);
                StringBuilder word = new StringBuilder();
                for (int j = 0; j < length; j++) word.append((char) ('a' + random.nextInt(4)));
                words.add(word.toString());
            }
            check(words.toArray(String[]::new));
        }
    }
}
```
