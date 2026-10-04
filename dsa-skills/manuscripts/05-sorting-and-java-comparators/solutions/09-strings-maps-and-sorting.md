<!-- solutions-for: 09-strings-maps-and-sorting -->
### Strings, Maps, And Sorting

#### Solution: [Build] Valid Anagram (LeetCode 242)
<!-- id: combo-valid-anagram-sort -->

**Approach.** Reject unequal lengths before allocating arrays. Sort private copies of both strings' characters and compare the resulting sequences. Sorting preserves every occurrence, so equality is equivalent to matching character multisets. The independent oracle removes matching characters one at a time rather than sorting or counting.

**Complexity.** O(m log(m + 1)) time and O(m) extra space for two character arrays of common length `m`; unequal lengths return in O(1) time.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ComboValidAnagramSort {
    static boolean solve(String a, String b) {
        if (a.length() != b.length()) return false;
        char[] left = a.toCharArray(), right = b.toCharArray();
        Arrays.sort(left);
        Arrays.sort(right);
        return Arrays.equals(left, right);
    }

    static boolean brute(String a, String b) {
        StringBuilder remaining = new StringBuilder(b);
        for (char value : a.toCharArray()) {
            int at = remaining.indexOf(String.valueOf(value));
            if (at < 0) return false;
            remaining.deleteCharAt(at);
        }
        return remaining.length() == 0;
    }

    static String randomWord(Random random) {
        StringBuilder word = new StringBuilder();
        int length = 1 + random.nextInt(14);
        for (int i = 0; i < length; i++) word.append((char) ('a' + random.nextInt(5)));
        return word.toString();
    }

    public static void main(String[] args) {
        if (!solve("abbc", "bcab") || !brute("abbc", "bcab")) throw new AssertionError("example 1");
        if (solve("abbc", "abcc") || brute("abbc", "abcc")) throw new AssertionError("example 2");
        Random random = new Random(24209);
        for (int trial = 0; trial < 3000; trial++) {
            String a = randomWord(random), b = randomWord(random);
            if (trial % 3 == 0) {
                char[] shuffled = a.toCharArray();
                for (int i = shuffled.length - 1; i > 0; i--) {
                    int j = random.nextInt(i + 1);
                    char old = shuffled[i];
                    shuffled[i] = shuffled[j];
                    shuffled[j] = old;
                }
                b = new String(shuffled);
            }
            if (solve(a, b) != brute(a, b)) throw new AssertionError(a + " / " + b);
        }
    }
}
```

#### Solution: [Vary] Group Anagrams (LeetCode 49)
<!-- id: combo-group-anagrams-sort-key -->

**Approach.** Compute one sorted signature per word and append the original word under that key. A `LinkedHashMap` preserves first-key appearance; lists preserve encounter order and multiplicity. The oracle scans representatives and matches characters by deletion. Comparing whole results detects both wrong memberships and equivalent words split into different groups.

**Complexity.** Expected O(n * (1 + m log(m + 1))) time and O(n * (m + 1)) space including retained keys and output references, for `n` words of maximum length `m`. Key construction and hashing cost O(m) per word; empty words still require map operations and output references.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class ComboGroupAnagramsSortKey {
    static List<List<String>> solve(String[] words) {
        Map<String, List<String>> groups = new LinkedHashMap<>();
        for (String word : words) {
            char[] chars = word.toCharArray();
            Arrays.sort(chars);
            String key = new String(chars);
            groups.computeIfAbsent(key, ignored -> new ArrayList<>()).add(word);
        }
        return new ArrayList<>(groups.values());
    }

    static boolean same(String a, String b) {
        StringBuilder remaining = new StringBuilder(b);
        for (char value : a.toCharArray()) {
            int at = remaining.indexOf(String.valueOf(value));
            if (at < 0) return false;
            remaining.deleteCharAt(at);
        }
        return remaining.length() == 0;
    }

    static List<List<String>> brute(String[] words) {
        List<List<String>> groups = new ArrayList<>();
        for (String word : words) {
            List<String> destination = null;
            for (List<String> candidate : groups) {
                if (same(word, candidate.get(0))) {
                    destination = candidate;
                    break;
                }
            }
            if (destination == null) {
                destination = new ArrayList<>();
                groups.add(destination);
            }
            destination.add(word);
        }
        return groups;
    }

    public static void main(String[] args) {
        String[] first = {"pots", "dog", "stop", "tops", "god", "pots"};
        List<List<String>> expected = List.of(List.of("pots", "stop", "tops", "pots"), List.of("dog", "god"));
        if (!solve(first).equals(expected) || !brute(first).equals(expected)) throw new AssertionError("example 1");
        String[] second = {"", "", "b"};
        expected = List.of(List.of("", ""), List.of("b"));
        if (!solve(second).equals(expected) || !brute(second).equals(expected)) throw new AssertionError("example 2");
        Random random = new Random(4909);
        for (int trial = 0; trial < 2000; trial++) {
            String[] words = new String[1 + random.nextInt(20)];
            for (int i = 0; i < words.length; i++) {
                StringBuilder word = new StringBuilder();
                int length = random.nextInt(7);
                for (int j = 0; j < length; j++) word.append((char) ('a' + random.nextInt(4)));
                words[i] = word.toString();
            }
            String[] original = words.clone();
            if (!solve(words).equals(brute(words)) || !Arrays.equals(words, original))
                throw new AssertionError(Arrays.toString(words));
        }
    }
}
```

#### Solution: [Boundary] Sort Characters By Frequency (LeetCode 451)
<!-- id: combo-sort-characters-frequency -->

**Approach.** Count characters, then sort only the distinct labels by decreasing count. An ascending character tie key makes the result reproducible within the prompt's tie freedom. Append each whole run so a label is never split across the output. The oracle repeatedly scans an ASCII count table to choose the highest remaining frequency, breaking ties by the smallest character.

**Complexity.** Expected O(n + u log u) time and O(n + u) space including the result, for `u <= 62` distinct labels. Counting is expected O(n); the sort orders `u` boxed characters, and the builder appends exactly `n` characters. Setting its capacity once avoids repeated growth.

```java run
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class ComboSortCharactersFrequency {
    static String solve(String input) {
        Map<Character, Integer> counts = new HashMap<>();
        for (int i = 0; i < input.length(); i++) counts.merge(input.charAt(i), 1, Integer::sum);
        List<Character> labels = new ArrayList<>(counts.keySet());
        labels.sort(Comparator.<Character>comparingInt(counts::get).reversed().thenComparingInt(value -> value));
        StringBuilder output = new StringBuilder(input.length());
        for (char label : labels) {
            for (int copies = counts.get(label); copies > 0; copies--) output.append(label);
        }
        return output.toString();
    }

    static String brute(String input) {
        int[] counts = new int[128];
        for (char label : input.toCharArray()) counts[label]++;
        StringBuilder output = new StringBuilder();
        while (output.length() < input.length()) {
            int best = -1;
            for (int label = 0; label < counts.length; label++) {
                if (counts[label] > 0 && (best < 0 || counts[label] > counts[best])) best = label;
            }
            for (int i = 0; i < counts[best]; i++) output.append((char) best);
            counts[best] = 0;
        }
        return output.toString();
    }

    public static void main(String[] args) {
        if (!solve("A2A2Abb").equals("AAA22bb") || !brute("A2A2Abb").equals("AAA22bb"))
            throw new AssertionError("example 1");
        if (!solve("aA11").equals("11Aa") || !brute("aA11").equals("11Aa")) throw new AssertionError("example 2");
        String alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
        Random random = new Random(45109);
        for (int trial = 0; trial < 2000; trial++) {
            StringBuilder input = new StringBuilder();
            int length = 1 + random.nextInt(80);
            for (int i = 0; i < length; i++) input.append(alphabet.charAt(random.nextInt(alphabet.length())));
            String word = input.toString();
            if (!solve(word).equals(brute(word))) throw new AssertionError(word);
        }
        String large = "A".repeat(500000);
        if (!solve(large).equals(large)) throw new AssertionError("maximum length");
    }
}
```

#### Solution: [Recognize] Determine If Two Strings Are Close (LeetCode 1657)
<!-- id: combo-close-strings-frequency-multiset -->

**Approach.** Count both words and compare the presence of each label before sorting the arrays. Then compare the sorted arrays of counts. Existing-label exchanges can permute count ownership, and position swaps can arrange the characters, so the tests are sufficient as well as necessary. The oracle enumerates assignments of source frequencies to target labels without sorting, using tiny alphabets to bound the search.

**Complexity.** O(n + a log a) time and O(a) extra space, where `n` is total input length and `a = 26`. Under this fixed alphabet, time is O(n) and extra space is O(1). The test-only enumeration is exponential in the number of present labels; `solve` never uses it.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ComboCloseStringsFrequencyMultiset {
    static int[] count(String word) {
        int[] counts = new int[26];
        for (int i = 0; i < word.length(); i++) counts[word.charAt(i) - 'a']++;
        return counts;
    }

    static boolean solve(String a, String b) {
        if (a.length() != b.length()) return false;
        int[] source = count(a), target = count(b);
        for (int label = 0; label < 26; label++) {
            if ((source[label] > 0) != (target[label] > 0)) return false;
        }
        // Sorting erases count ownership, so label presence was checked first.
        Arrays.sort(source);
        Arrays.sort(target);
        return Arrays.equals(source, target);
    }

    static boolean assign(int at, int[] source, int[] target, boolean[] used) {
        if (at == target.length) return true;
        for (int i = 0; i < source.length; i++) {
            if (!used[i] && source[i] == target[at]) {
                used[i] = true;
                if (assign(at + 1, source, target, used)) return true;
                used[i] = false;
            }
        }
        return false;
    }

    static boolean brute(String a, String b) {
        if (a.length() != b.length()) return false;
        int[] source = count(a), target = count(b);
        for (int label = 0; label < 26; label++) {
            if ((source[label] > 0) != (target[label] > 0)) return false;
        }
        int[] positiveSource = Arrays.stream(source).filter(value -> value > 0).toArray();
        int[] positiveTarget = Arrays.stream(target).filter(value -> value > 0).toArray();
        return assign(0, positiveSource, positiveTarget, new boolean[positiveSource.length]);
    }

    static String randomWord(Random random) {
        StringBuilder word = new StringBuilder();
        int length = 1 + random.nextInt(20);
        for (int i = 0; i < length; i++) word.append((char) ('a' + random.nextInt(5)));
        return word.toString();
    }

    public static void main(String[] args) {
        if (!solve("aabbbbcc", "aaaabbcc") || !brute("aabbbbcc", "aaaabbcc")) throw new AssertionError("example 1");
        if (solve("aabb", "ccdd") || brute("aabb", "ccdd")) throw new AssertionError("example 2");
        if (solve("aabbbbcc", "aaabbbcc")) throw new AssertionError("same set, wrong counts");
        Random random = new Random(165709);
        for (int trial = 0; trial < 3000; trial++) {
            String a = randomWord(random), b = randomWord(random);
            if (trial % 3 == 0) {
                a = "abcde" + a;
                StringBuilder renamed = new StringBuilder();
                for (char label : a.toCharArray()) renamed.append((char) ('a' + (label - 'a' + 1) % 5));
                b = renamed.reverse().toString();
            }
            if (solve(a, b) != brute(a, b)) throw new AssertionError(a + " / " + b);
        }
    }
}
```
