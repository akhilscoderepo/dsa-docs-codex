<!-- lesson-kind: combination -->
<!-- lesson-id: strings-and-two-pointers -->
## Strings And Two Pointers

<!-- stage: context -->
### Compare Without Rebuilding

A text-processing task often looks simple until the contract says which characters count. A phrase may contain spaces and punctuation, comparison may ignore case, or one bad character may be removed. Building a cleaned copy is an understandable first move, but it changes the space cost and can hide the real decision: which original character should be examined next? Other string tasks do not compare mirrored positions at all. They ask whether one sequence can be read, in order, from another.

The useful common ground is not “a problem involving text.” It is that each comparison can permanently resolve one or more character positions. Once a position has been resolved, the scan never needs to visit it again.

<!-- stage: contributions -->
### What Each Part Adds

String indexing supplies characters, their original positions, and the exact normalization rules from the contract. Opposite-end pointer movement supplies a shrinking unresolved interval for symmetry, reversal, and one-deletion validation. Same-direction pointer movement supplies a reader for each sequence when relative order matters but adjacency does not. The combination works only after we state which positions each pointer represents and what permits a move. Character comparison alone provides no traversal rule, while pointer movement without the string contract may compare punctuation or letter case incorrectly.

<!-- stage: naive -->
### Materialize The Comparison Text

The direct palindrome solution copies every relevant character into normalized form, reverses that text, and compares the two strings. It is correct because both strings contain exactly the characters that the contract asks us to compare.

```java
static boolean normalizedPalindromeCopy(String text) {
    StringBuilder cleaned = new StringBuilder();
    for (int i = 0; i < text.length(); i++) {
        char c = text.charAt(i);
        if (Character.isLetterOrDigit(c)) {
            cleaned.append(Character.toLowerCase(c));
        }
    }
    String forward = cleaned.toString();
    String backward = cleaned.reverse().toString();
    return forward.equals(backward);
}
```

This is often acceptable. It is also a useful oracle for testing an in-place scan because its structure is deliberately different.

<!-- stage: bottleneck -->
### Paying For A Second Representation

Consider a 200,000-character log line whose meaningful characters are mostly near the ends. The method still copies every accepted character, allocates the forward string, mutates the builder during reversal, and allocates the reversed string. The work is O(n), but the auxiliary storage is also O(n), even though each endpoint comparison needs only two current characters.

The waste becomes clearer for the one-deletion variant. Rebuilding a candidate after deleting every possible position takes O(n) work per deletion and O(n²) time overall. At length 100,000, that strategy can perform billions of character visits. Most deletions never need consideration: before the first mismatch, equal endpoint pairs are already settled, and after it, only the two mismatching endpoints are possible deletions.

<!-- stage: insight -->
### Give Every Pointer A Contract

The first decision is a **normalization rule**: determine whether a character participates and, if it does, which value is compared. Apply that rule at the current indices instead of materializing another string. For a palindrome, move each endpoint past ignored characters, compare the next participating pair, and close the interval only after equality. For reversal, no normalization is needed; exchange the endpoints and close the interval.

Allowing one deletion adds a **mismatch budget**. Matching pairs spend nothing. At the first unequal pair, a valid answer must delete either the left character or the right character, because deleting an interior character leaves the same unequal endpoints facing each other. Test those two remaining ranges with an ordinary palindrome check. Do not branch again: the entire budget was spent at the first mismatch.

A subsequence uses a different shape. One index is a **consumption pointer** for the characters still required from the short string. The other scans the long string. A match advances both; a nonmatch advances only the long-string index. This is safe because rejecting the current long-string character cannot remove a later occurrence, while advancing the required character without a match would falsely claim it was found.

<!-- names: normalization rule, mismatch budget, consumption pointer -->

Across these variants, the proof is the same kind of statement: every move permanently resolves a position without discarding a possible answer. The direction and move condition come from the output contract, not from the fact that the input happens to be a string.

<!-- stage: variables -->
### Indices And Their Meanings

For mirrored work, `left` and `right` are inclusive bounds of the unresolved range. A helper that checks `text[left..right]` must use the same convention. For a subsequence, `need` is the index of the next character required from the short string, and `scan` is the current candidate position in the long string. The one-deletion variant does not need a mutable counter when it branches only once; entering either helper call means the single deletion has already been spent.

<!-- stage: trace -->
### Spend The Deletion Once

Trace `abca`. The outer `a` characters match, so both endpoints move inward. The unresolved range is now `bc`, and those characters differ. This is the hardest step: there is no reason to try deleting every character in the string. Any successful deletion must remove the `b` at the left endpoint or the `c` at the right endpoint, because every other deletion leaves `b` facing `c`.

Skipping the left endpoint leaves the one-character range `c`; skipping the right leaves `b`. Either range is a palindrome, so the original text can become a palindrome after at most one deletion. Notice that the two branches are ordinary checks. If a branch encounters another mismatch, it fails instead of branching again.

```trace
{"cells":["a","b","c","a"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":3},"vars":{"match":true,"remainingSkips":1},"note":"a matches a; move both endpoints inward."},{"at":{"left":1,"right":2},"vars":{"match":false,"remainingSkips":1},"note":"b and c differ; spend the one deletion on exactly one endpoint."},{"at":{"left":2,"right":2},"vars":{"branch":"skip left","valid":true},"note":"Ignore index 1; the remaining range is a palindrome."},{"at":{"left":1,"right":1},"vars":{"branch":"skip right","valid":true},"note":"Ignore index 2; this branch is also a palindrome, so the answer is true."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java run
public final class StringsTwoPointerBlueprint {
    static boolean validAfterAtMostOneDeletion(String text) {
        int left = 0;
        int right = text.length() - 1;
        while (left < right && text.charAt(left) == text.charAt(right)) {
            left++;
            right--;
        }
        if (left >= right) return true;
        return isPalindrome(text, left + 1, right)
                || isPalindrome(text, left, right - 1);
    }

    private static boolean isPalindrome(String text, int left, int right) {
        while (left < right) {
            if (text.charAt(left) != text.charAt(right)) return false;
            left++;
            right--;
        }
        return true;
    }

    public static void main(String[] args) {
        if (!validAfterAtMostOneDeletion("abca")) throw new AssertionError("skip c");
        if (validAfterAtMostOneDeletion("abc")) throw new AssertionError("two mismatches remain");
    }
}
```

The initial loop settles the common mirrored prefix. If it finishes the range, no deletion is needed. Otherwise the two helper calls encode the only legal choices at the first mismatch. Each call receives inclusive bounds, matching the outer loop, so an empty or one-character remainder succeeds naturally. The worst case performs one outer scan plus two scans of shorter ranges, which is O(n) time and O(1) auxiliary space; no substring is allocated.

<!-- stage: applicability -->
### When It Applies

Use this combination when the answer depends on the order of characters and each pointer move can be justified by a resolved comparison. For mirrored validation, the invariant is that every participating character outside `[left, right]` has already been matched with its partner. For subsequences, the invariant is that `source[0..need)` has already been matched in order within the scanned prefix of the target.

The nearest false friend is a substring requirement. A subsequence may skip arbitrary characters, while a substring must remain contiguous and usually needs a window. Another false friend is Unicode text whose user-visible symbols are not single Java `char` values. `Character.isLetterOrDigit(char)` and `charAt` operate on UTF-16 code units; full Unicode code-point or grapheme handling requires a different representation. Finally, the one-deletion proof does not extend unchanged to an unrestricted number of edits, because repeated branching is no longer bounded.

<!-- stage: exercises -->
### Exercises

#### [Build] Valid Palindrome (LeetCode 125)
<!-- id: tp-strings-valid-palindrome -->

**Prerequisites.** Chapter 03 string indexing and this lesson's normalized endpoint comparison.

**Problem.** Given a string, ignore every character that is not a letter or digit, compare letters without regard to case, and return whether the remaining sequence reads the same from both ends.

**Constraints.** `1 <= s.length <= 2 * 10^5`; `s` contains printable ASCII characters. Target O(n) time and O(1) auxiliary space.

**Example 1.** Input `s = "Was it a rat I saw?"`; output `true`, because normalization leaves a mirrored sequence.

**Example 2.** Input `s = "0P"`; output `false`, because `0` and `p` are both significant and do not match.

**Hint.** Before comparing endpoints, ask whether each current character participates. Which pointer can move without requiring a comparison?

**Changed decision.** This first rung applies filtering and case normalization directly at the original indices instead of creating cleaned text.

#### [Vary] Reverse String (LeetCode 344)
<!-- id: tp-strings-reverse-string -->

**Prerequisites.** Inclusive endpoint bounds and mutation of a `char[]`.

**Problem.** Reverse the supplied character array in place. Return nothing, allocate no second array, and leave every character at its mirrored position.

**Constraints.** `1 <= s.length <= 10^5`; each entry is a printable ASCII character. Use O(1) auxiliary space.

**Example 1.** Input `s = ['j','a','v','a']`; output state `s = ['a','v','a','j']` after the method returns.

**Example 2.** Input `s = ['Q']`; output state `['Q']`, since the endpoints already coincide.

**Hint.** A swap resolves both endpoint positions permanently. What loop condition prevents swapping the middle character with itself?

**Changed decision.** Comparison becomes mutation: equal values are irrelevant, and every iteration swaps before moving both endpoints.

#### [Boundary] Valid Palindrome II (LeetCode 680)
<!-- id: tp-strings-valid-palindrome-ii -->

**Prerequisites.** Ordinary range palindrome checking and this lesson's one-mismatch proof.

**Problem.** Given a lowercase string, return whether deleting at most one character can make the remaining characters a palindrome. Choosing no deletion is allowed.

**Constraints.** `1 <= s.length <= 10^5`; `s` contains only lowercase English letters. Target O(n) time and O(1) auxiliary space.

**Example 1.** Input `s = "abca"`; output `true`, because deleting either `b` or `c` leaves a palindrome.

**Example 2.** Input `s = "abc"`; output `false`, because every single deletion leaves two unequal characters.

**Hint.** At the first mismatch, why can deleting a character strictly inside the unresolved range not help? Test the only two endpoint choices without allowing another deletion.

**Changed decision.** One mismatch is tolerated, but it creates exactly two bounded checks rather than a general backtracking search.

#### [Recognize] Is Subsequence (LeetCode 392)
<!-- id: tp-strings-is-subsequence -->

**Prerequisites.** Same-direction scans and the distinction between a subsequence and a contiguous substring.

**Problem.** Given strings `s` and `t`, return whether all characters of `s` can be selected from `t` in the same order. Selected positions need not be adjacent.

**Constraints.** `0 <= s.length <= 100`, `0 <= t.length <= 10^4`; both strings contain lowercase English letters. Target O(`t.length`) time and O(1) auxiliary space.

**Example 1.** Input `s = "dog"`, `t = "doinggood"`; output `true`, using positions 0, 1, and 4 of `t`.

**Example 2.** Input `s = "odd"`, `t = "doinggood"`; output `false`, because only one `d` remains after the first matched `o`.

**Hint.** Keep one index on the next required character. When the current character of `t` does not satisfy it, which index can still advance safely?

**Changed decision.** Both indices move left to right, and only a successful match consumes a character from the required sequence.
