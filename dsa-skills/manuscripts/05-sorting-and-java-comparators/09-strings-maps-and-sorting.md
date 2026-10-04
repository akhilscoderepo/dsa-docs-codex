<!-- lesson-kind: combination -->
<!-- lesson-id: strings-maps-and-sorting -->
## Strings, Maps, And Sorting

<!-- stage: context -->
### Group Equivalent Search Terms

A search service receives terms such as `"pots"`, `"stop"`, `"dog"`, and `"tops"`. Terms belong in the same group when they contain the same characters with the same multiplicities. Each input occurrence must survive, including repeated terms and empty strings. We will preserve encounter order within each group and order groups by their first appearance.

The strings look different, so the raw text cannot serve as that identity. We need a representation that is identical for equivalent terms and different when either a character or its count changes.

<!-- stage: contributions -->
### Three Earlier Ideas Cooperate

Chapter 03's string traversal exposes each term's characters and gives us an owned character array. This chapter's sorting gives all permutations of the same multiset one ordered representation. Chapter 04's map associates that representation with the list of original terms that produced it. A linked map adds the first-appearance group order required by our chosen contract.

Each prerequisite owns a separate decision. Strings provide the data, sorting normalizes order, and the map performs grouping. Removing any one changes the problem: sorting without a map produces keys but no groups, while a map keyed by raw strings treats anagrams as unrelated.

<!-- stage: naive -->
### Compare Every Pair

A direct grouping method scans existing groups for every term and compares it with one representative by rebuilding character counts.

```java
import java.util.ArrayList;
import java.util.List;

public final class PairwiseWordGrouping {
    static boolean sameCharacters(String a, String b) {
        if (a.length() != b.length()) return false;
        int[] counts = new int[26];
        for (int i = 0; i < a.length(); i++) {
            counts[a.charAt(i) - 'a']++;
            counts[b.charAt(i) - 'a']--;
        }
        for (int count : counts) if (count != 0) return false;
        return true;
    }

    static List<List<String>> group(String[] words) {
        List<List<String>> groups = new ArrayList<>();
        for (String word : words) {
            List<String> match = null;
            for (List<String> candidate : groups) {
                if (sameCharacters(word, candidate.get(0))) {
                    match = candidate;
                    break;
                }
            }
            if (match == null) {
                match = new ArrayList<>();
                groups.add(match);
            }
            match.add(word);
        }
        return groups;
    }
}
```

This method is correct for lowercase English words, including empty words: it tests exact character multiplicities and creates a group only when no representative matches. It repeats equivalence tests against many representatives, rebuilding counts for each comparison.

<!-- stage: bottleneck -->
### New Groups Repeat Full Comparisons

Consider `"aa"`, `"ab"`, `"ac"`, and `"ad"`. They create four groups. The last word tests all three earlier representatives, even though each comparison recounts the same two letters in `"ad"`. The executable trace helper checks this run: six pair comparisons visit twenty-four characters in total. With `n` unrelated words of equal length `m`, there are `n(n - 1) / 2` comparisons, producing O(n^2 * (m + 26)) time. For a fixed alphabet and nonempty words this simplifies to O(n^2 * m).

The comparison also throws away its work. Once a word's multiset has been computed, the next group test rebuilds it. A reusable canonical key lets one map lookup replace the representative scan.

<!-- stage: insight -->
### Normalize Before Grouping

The **canonical-signature grouping** pattern transforms each object into a **canonical signature** that represents exactly the equivalence relation in the prompt. For anagrams, sort a copied character array and create a string from it. `"pots"`, `"stop"`, and `"tops"` all become `"opst"`.

<!-- names: canonical signature, canonical-signature grouping, equivalence relation -->

The map invariant is: after processing the first `i` words, every map entry contains exactly those processed words whose sorted-character signature equals its key. A new word computes one key and performs one lookup. Because sorting preserves every character and multiplicity while discarding only permutation order, equal signatures are equivalent precisely when the problem's **equivalence relation** says they should be.

A frequency vector can also form a signature when the alphabet is fixed and stated. It is an implementation variation, not the reason grouping works. Unicode, case folding, or normalization rules change what a character means and therefore change the signature contract. For the lowercase contract, the safety argument has two directions: rearranging characters cannot change their sorted sequence, and equal sorted sequences contain exactly the same character copies, so one word can be rearranged into the other.

<!-- stage: variables -->
### Word, Signature, And Group

`word` is the original value retained in the output. `chars` is a private array that may be sorted. `signature(word)` returns the immutable map key built from that array. `groups` maps each key to its encounter-ordered list. Before processing index `i`, the map owns exactly the occurrences in the half-open prefix `[0, i)`. The signature must encode multiplicity; a set of characters would erase a relevant difference.

<!-- stage: trace -->
### Watch Keys Converge

Process `"pots"` first. Sorting its characters yields `"opst"`, so the map creates the first group. `"stop"` produces the same key and joins it. `"dog"` yields `"dgo"` and creates the second group. At index three, `"tops"` returns to the first key even though a different group was created in between. Group membership follows the key, not adjacency in the input.

The next `"pots"` is a second input occurrence. It joins the first list rather than being deduplicated. Finally, each empty string produces the empty key: the first creates the third group and the second joins it. The final lists are `[pots, stop, tops, pots]`, `[dog]`, and two empty strings together. Only the private keys are sorted; the stored words retain their spelling and encounter order. The trace helper calculates each key and copies the current list into every step, so the stepper shows the state after the append.

```trace
{"cells":["eat","tea","tan","ate"],"pointers":["scan","group"],"steps":[{"at":{"scan":0,"group":0},"vars":{"signature":"aet"},"note":"eat creates the first group under canonical key aet."},{"at":{"scan":1,"group":0},"vars":{"signature":"aet"},"note":"tea has the same sorted signature and joins the existing group."},{"at":{"scan":2,"group":1},"vars":{"signature":"ant"},"note":"tan produces a different key, so the map creates a second group."},{"at":{"scan":3,"group":0},"vars":{"signature":"aet"},"note":"ate returns to key aet; original spelling is stored without modification."}]}
```

<!-- stage: code -->
### Map The Canonical Key

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class CanonicalGrouping {
    static String signature(String word) {
        char[] chars = word.toCharArray();
        Arrays.sort(chars);
        return new String(chars);
    }

    static List<List<String>> group(String[] words) {
        Map<String,List<String>> groups = new LinkedHashMap<>();
        for (String word : words)
            groups.computeIfAbsent(signature(word), ignored -> new ArrayList<>()).add(word);
        return new ArrayList<>(groups.values());
    }

    public static void main(String[] args) {
        List<List<String>> actual = group(new String[] {"pots","stop","dog","tops","pots","",""});
        List<List<String>> expected = List.of(List.of("pots","stop","tops","pots"), List.of("dog"), List.of("",""));
        if (!actual.equals(expected)) throw new AssertionError(actual);
    }
}
```

For `n` words of maximum length `m`, expected time is O(n * (1 + m log(m + 1))). The added one accounts for empty words. Constructing and hashing each key costs O(m), as does a key comparison in the worst case. Sorting dominates for longer words. Retained keys and output references use O(n * (m + 1)) space; the temporary character array uses O(m). A `LinkedHashMap` preserves the specified group order, while the lists preserve word order. Input strings and the caller's array remain unchanged.

<!-- stage: applicability -->
### When It Applies

Use canonical signatures when objects should group by an equivalence relation and a deterministic transformation can erase irrelevant differences while retaining every relevant one. The invariant is that every processed object appears in exactly one map list, under the canonical key produced by its relevant content. State why both directions hold: equivalent objects produce the same key, and equal keys cannot hide a distinction required by the output.

The false friend is a signature that assumes an unstated alphabet. A 26-entry lowercase count is excellent under a lowercase-English contract and wrong for general text. Another false friend is sorting the original strings when the output must preserve their spelling or encounter order.

The method silently fails when delimiters make a structured signature ambiguous, when mutable objects are used as map keys, or when the problem compares only frequency multisets rather than which character owns each frequency. Empty strings legitimately share the empty signature. Duplicate words remain separate output entries unless the contract also asks for deduplication.

The last two exercises change what the counts mean. Frequency ordering counts each character first, orders distinct character records by descending count, then writes each whole run. That is an output order, not an anagram key. For close strings, swapping positions preserves counts, while exchanging two existing labels swaps their entire counts. Those operations preserve both the set of present labels and the multiset of positive frequencies. Conversely, matching sets and frequency multisets lets us assign counts to the target labels by exchanges, then arrange positions by swaps. Check label presence before sorting count arrays, because sorting erases ownership. In Java, `char[]` represents UTF-16 code units; our English-letter contracts avoid splitting supplementary characters.

<!-- stage: exercises -->
### Exercises

#### [Build] Valid Anagram (LeetCode 242)
<!-- id: combo-valid-anagram-sort -->

**Prerequisites.** Character arrays and natural sorting.

**Problem.** Given lowercase strings `s` and `t`, return `true` when one can be rearranged into the other, using every character occurrence exactly once. Return `false` otherwise. Compare sorted private character arrays without modifying the strings.

**Constraints.** `1 <= s.length, t.length <= 5 * 10^4`; both strings contain lowercase English letters.

**Example 1.** Input `s = "abbc"`, `t = "bcab"`, output `true`; both contain one `a`, two `b` characters, and one `c`.

**Example 2.** Input `s = "abbc"`, `t = "abcc"`, output `false`; equal character sets and lengths do not guarantee equal multiplicities.

**Hint.** Reject unequal lengths first. What canonical representation should both remaining strings share?

**Changed decision.** Two objects are compared by canonical form without storing groups.

#### [Vary] Group Anagrams (LeetCode 49)
<!-- id: combo-group-anagrams-sort-key -->

**Prerequisites.** The Build exercise and map-of-lists construction.

**Problem.** Given lowercase words, return groups of anagrams. Preserve encounter order inside each group; group order may follow first signature appearance.

**Constraints.** `1 <= words.length <= 10^4`; `0 <= words[i].length <= 100`; characters are lowercase English letters. Use expected O(n * (1 + m log(m + 1))) time for `n` words of maximum length `m`, with O(n * (m + 1)) space including keys and output references. The original problem permits any group order; this chapter chooses first-appearance order for reproducibility.

**Example 1.** Input `["pots","dog","stop","tops","god","pots"]`, output `[["pots","stop","tops","pots"],["dog","god"]]`; the repeated term remains a separate occurrence.

**Example 2.** Input `["","","b"]`, output `[["",""],["b"]]`; both empty strings share the empty signature.

**Hint.** The sorted form belongs in the map key; which value should the map retain for the learner-visible output?

**Changed decision.** Repeated canonical keys now accumulate original objects rather than produce a boolean.

#### [Boundary] Sort Characters By Frequency (LeetCode 451)
<!-- id: combo-sort-characters-frequency -->

**Prerequisites.** Character frequency maps and object comparators.

**Problem.** Given a string, return its characters ordered by decreasing frequency. Equal-frequency characters may appear in any deterministic order, and equal characters must remain contiguous.

**Constraints.** `1 <= s.length <= 5 * 10^5`; `s` contains uppercase and lowercase English letters and digits, treated as distinct characters. Target O(n + u log u) time and O(n + u) space including the output, where `u <= 62` is the number of distinct characters.

**Example 1.** Input `"A2A2Abb"`, output `"AAA22bb"`; `A` appears three times, and the two remaining runs each have length two. `"AAAbb22"` is also valid.

**Example 2.** Input `"aA11"`, output `"11Aa"`; `"11aA"` is also valid. Uppercase `A` and lowercase `a` are separate labels.

**Hint.** What should be compared once per distinct character rather than once per input position? How will you keep all copies of one character together?

**Changed decision.** Frequencies determine output order instead of serving as an equality signature.

#### [Recognize] Determine If Two Strings Are Close (LeetCode 1657)
<!-- id: combo-close-strings-frequency-multiset -->

**Prerequisites.** Frequency arrays, sets, and sorting small numeric signatures.

**Problem.** Given lowercase strings `word1` and `word2`, return whether they can be made identical by repeating either permitted operation: swap two positions, or choose two distinct labels already present and exchange every occurrence of those labels simultaneously. The operations may be applied to either string. A label absent from a string cannot be introduced by an exchange.

**Constraints.** `1 <= word1.length, word2.length <= 10^5`; both contain lowercase English letters.

**Example 1.** Input `word1 = "aabbbbcc"`, `word2 = "aaaabbcc"`, output `true`; exchanging labels `a` and `b` transfers their counts, after which position swaps can arrange the target.

**Example 2.** Input `word1 = "aabb"`, `word2 = "ccdd"`, output `false`; matching frequency multisets cannot introduce absent labels.

**Hint.** Which two facts survive a global label exchange? Which of those facts would disappear if you sorted the count array before inspecting label presence?

**Changed decision.** A raw sorted string is too strict; the invariant separates character presence from ownership of each frequency.
