<!-- solutions-for: 92-strings-and-two-pointers -->
### Strings And Two Pointers Solutions

#### Solution: [Build] Valid Palindrome (LeetCode 125)
<!-- id: tp-strings-valid-palindrome -->

**Approach.** Move each endpoint past characters excluded by the contract, then compare lowercase forms of the next participating pair. A mismatch ends the check; equality resolves both positions. The randomized oracle explicitly builds normalized text and reverses it, giving the test a different implementation shape.

**Complexity.** O(n) time because neither endpoint retreats, and O(1) auxiliary space in the submitted method.

```java run
import java.util.Random;

public final class TpStrings125 {
    static boolean isPalindrome(String text) {
        int left = 0;
        int right = text.length() - 1;
        while (left < right) {
            while (left < right && !Character.isLetterOrDigit(text.charAt(left))) left++;
            while (left < right && !Character.isLetterOrDigit(text.charAt(right))) right--;
            char a = Character.toLowerCase(text.charAt(left));
            char b = Character.toLowerCase(text.charAt(right));
            if (a != b) return false;
            left++;
            right--;
        }
        return true;
    }

    private static boolean oracle(String text) {
        StringBuilder cleaned = new StringBuilder();
        for (int i = 0; i < text.length(); i++) {
            char c = text.charAt(i);
            if (Character.isLetterOrDigit(c)) cleaned.append(Character.toLowerCase(c));
        }
        String forward = cleaned.toString();
        return forward.contentEquals(cleaned.reverse());
    }

    public static void main(String[] args) {
        if (!isPalindrome("Was it a rat I saw?")) throw new AssertionError("example 1");
        if (isPalindrome("0P")) throw new AssertionError("example 2");

        Random random = new Random(125);
        String alphabet = "aB0 !?,z";
        for (int test = 0; test < 3000; test++) {
            int length = random.nextInt(18);
            StringBuilder sample = new StringBuilder(length);
            for (int i = 0; i < length; i++) sample.append(alphabet.charAt(random.nextInt(alphabet.length())));
            String value = sample.toString();
            if (isPalindrome(value) != oracle(value)) throw new AssertionError(value);
        }
    }
}
```

#### Solution: [Vary] Reverse String (LeetCode 344)
<!-- id: tp-strings-reverse-string -->

**Approach.** Swap the characters at inclusive endpoints, then move both indices inward. At loop exit, every position outside the interval contains its final mirrored value, and the unresolved interval has length zero or one.

**Complexity.** O(n) time and O(1) auxiliary space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class TpStrings344 {
    static void reverse(char[] text) {
        int left = 0;
        int right = text.length - 1;
        while (left < right) {
            char saved = text[left];
            text[left] = text[right];
            text[right] = saved;
            left++;
            right--;
        }
    }

    private static char[] oracle(char[] input) {
        return new StringBuilder(new String(input)).reverse().toString().toCharArray();
    }

    public static void main(String[] args) {
        char[] first = {'j', 'a', 'v', 'a'};
        reverse(first);
        if (!Arrays.equals(first, new char[] {'a', 'v', 'a', 'j'})) throw new AssertionError("example 1");
        char[] single = {'Q'};
        reverse(single);
        if (!Arrays.equals(single, new char[] {'Q'})) throw new AssertionError("example 2");

        Random random = new Random(344);
        for (int test = 0; test < 2500; test++) {
            char[] sample = new char[random.nextInt(24)];
            for (int i = 0; i < sample.length; i++) sample[i] = (char) ('a' + random.nextInt(5));
            char[] expected = oracle(sample);
            reverse(sample);
            if (!Arrays.equals(sample, expected)) throw new AssertionError(Arrays.toString(sample));
        }
    }
}
```

#### Solution: [Boundary] Valid Palindrome II (LeetCode 680)
<!-- id: tp-strings-valid-palindrome-ii -->

**Approach.** Resolve equal endpoint pairs until the first mismatch. A valid single deletion must remove one of those two endpoints, so check the two resulting inclusive ranges with a helper that permits no further deletion. The brute-force oracle tries every legal deletion for small randomized inputs.

**Complexity.** O(n) time—the two helper scans add only a constant multiple of n—and O(1) auxiliary space.

```java run
import java.util.Random;

public final class TpStrings680 {
    static boolean validPalindrome(String text) {
        int left = 0;
        int right = text.length() - 1;
        while (left < right && text.charAt(left) == text.charAt(right)) {
            left++;
            right--;
        }
        return left >= right || palindromeRange(text, left + 1, right)
                || palindromeRange(text, left, right - 1);
    }

    private static boolean palindromeRange(String text, int left, int right) {
        while (left < right) {
            if (text.charAt(left++) != text.charAt(right--)) return false;
        }
        return true;
    }

    private static boolean oracle(String text) {
        if (palindromeRange(text, 0, text.length() - 1)) return true;
        for (int removed = 0; removed < text.length(); removed++) {
            String candidate = text.substring(0, removed) + text.substring(removed + 1);
            if (palindromeRange(candidate, 0, candidate.length() - 1)) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        if (!validPalindrome("abca")) throw new AssertionError("example 1");
        if (validPalindrome("abc")) throw new AssertionError("example 2");

        Random random = new Random(680);
        for (int test = 0; test < 4000; test++) {
            int length = 1 + random.nextInt(12);
            StringBuilder sample = new StringBuilder(length);
            for (int i = 0; i < length; i++) sample.append((char) ('a' + random.nextInt(4)));
            String value = sample.toString();
            if (validPalindrome(value) != oracle(value)) throw new AssertionError(value);
        }
    }
}
```

#### Solution: [Recognize] Is Subsequence (LeetCode 392)
<!-- id: tp-strings-is-subsequence -->

**Approach.** Keep `need` on the next required character of `s` and scan every character of `t` once. Advance `need` only on equality. The dynamic-programming oracle independently asks whether each suffix pair can form the required subsequence.

**Complexity.** O(`t.length`) time and O(1) auxiliary space in the submitted method.

```java run
import java.util.Random;

public final class TpStrings392 {
    static boolean isSubsequence(String source, String target) {
        int need = 0;
        for (int scan = 0; scan < target.length() && need < source.length(); scan++) {
            if (source.charAt(need) == target.charAt(scan)) need++;
        }
        return need == source.length();
    }

    private static boolean oracle(String source, String target) {
        boolean[][] possible = new boolean[source.length() + 1][target.length() + 1];
        for (int j = 0; j <= target.length(); j++) possible[source.length()][j] = true;
        for (int i = source.length() - 1; i >= 0; i--) {
            for (int j = target.length() - 1; j >= 0; j--) {
                possible[i][j] = possible[i][j + 1]
                        || (source.charAt(i) == target.charAt(j) && possible[i + 1][j + 1]);
            }
        }
        return possible[0][0];
    }

    public static void main(String[] args) {
        if (!isSubsequence("dog", "doinggood")) throw new AssertionError("example 1");
        if (isSubsequence("odd", "doinggood")) throw new AssertionError("example 2");
        if (!isSubsequence("", "abc")) throw new AssertionError("empty source");

        Random random = new Random(392);
        for (int test = 0; test < 3500; test++) {
            StringBuilder source = new StringBuilder();
            StringBuilder target = new StringBuilder();
            for (int i = 0, n = random.nextInt(7); i < n; i++) source.append((char) ('a' + random.nextInt(3)));
            for (int i = 0, n = random.nextInt(11); i < n; i++) target.append((char) ('a' + random.nextInt(3)));
            String a = source.toString();
            String b = target.toString();
            if (isSubsequence(a, b) != oracle(a, b)) throw new AssertionError(a + " / " + b);
        }
    }
}
```
