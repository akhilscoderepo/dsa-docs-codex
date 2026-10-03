<!-- lesson-kind: standard -->
<!-- lesson-id: sort-and-deduplicate -->
## Sort And Deduplicate

<!-- stage: context -->
### Publish One Copy Of Each Error Code

A monitoring service receives error codes in arbitrary order. A daily index must list every observed code once, in ascending order. The input `[4, 1, 4, 2, 1, 1]` should produce `[1, 2, 4]` without changing the caller's array.

The service does not need the original positions or the number of occurrences. It needs one representative from each equality group. Sorting changes scattered duplicates into contiguous runs, so the scan has only one unresolved group at a time.

<!-- stage: naive -->
### Search The Output Before Every Append

A direct solution builds a list and scans that list before adding each input value.

```java nocompile
for (int value : nums) {
    if (!result.contains(value)) result.add(value);
}
result.sort(Integer::compare);
```

The code is easy to read and returns the right values. However, `contains` performs a linear scan, and the result may already hold almost every preceding value.

<!-- stage: bottleneck -->
### Distinct Input Forces Repeated Searches

When all `n` values are distinct, the successive membership checks inspect lists of lengths 0, 1, 2, and so on. The total is O(n^2) equality checks before the final O(n log n) sort. The method repeatedly asks whether a value appeared anywhere in the past because arbitrary input order provides no local signal.

Sorting a copy costs O(n log n), but then equality with the immediately preceding value answers the membership question. The additional scan is linear, and no historical search is needed.

<!-- stage: insight -->
### Compress Contiguous Runs

**Sort-and-deduplicate** orders the values and emits one **run representative** from each contiguous group of equal values. A **run boundary** occurs at index zero or wherever `ordered[i] != ordered[i - 1]`. Only boundaries create output.

<!-- names: sort-and-deduplicate, run representative, run boundary -->

The invariant is: before index `i` is processed, the output contains exactly one representative for every complete run in `ordered[0..i-1]`. If the current value equals its predecessor, it belongs to the current run and is skipped. Otherwise it begins a new run and must be emitted.

This pattern can return representatives, run counts, or an aggregate per run. The sorting step supplies contiguity; the scan defines what information survives. For an unsorted input, applying the familiar in-place “compare with the last written value” loop without sorting first is incorrect because another copy may appear much later.

When preserving the input matters, sort owned storage. When only a boolean duplicate answer is needed, the scan may return at the first equal adjacent pair rather than materializing representatives.

<!-- stage: variables -->
### Read Index And Output Size

`read` visits the sorted copy from left to right. `previous` is the value in the preceding position and identifies the current run. `write` is the number of representatives already stored. The meaningful output region is `result[0..write-1]`; unused capacity beyond `write` is not part of the answer.

<!-- stage: trace -->
### Emit At Boundaries Only

Sort `[4, 1, 4, 2, 1, 1]` into `[1, 1, 1, 2, 4, 4]`. Index zero always starts a run, so emit `1`. The next two values equal their predecessor and remain inside that run; neither changes the output.

At index three, `2` differs from `1`, so it begins a second run and is emitted. The first `4` begins the final run, while the last `4` is skipped. The scan returns the written prefix `[1, 2, 4]`. Every decision compares neighbors, yet it represents a fact about all occurrences because sorting made each equality group contiguous. The write index advances exactly three times.

```trace
{"cells":[1,1,1,2,4,4],"pointers":["read","write"],"steps":[{"at":{"read":0,"write":0},"vars":{"emit":1},"note":"Index zero begins the first run, so write representative 1."},{"at":{"read":1,"write":1},"vars":{"value":1},"note":"This 1 equals its predecessor and remains inside the current run."},{"at":{"read":2,"write":1},"vars":{"value":1},"note":"A third 1 is skipped for the same reason."},{"at":{"read":3,"write":1},"vars":{"emit":2},"note":"Two differs from one, marking a new run boundary."},{"at":{"read":4,"write":2},"vars":{"emit":4},"note":"Four begins the final run and becomes its representative."},{"at":{"read":5,"write":3},"vars":{"value":4},"note":"The final duplicate is skipped; the written prefix is [1,2,4]."}]}
```

<!-- stage: code -->
### Return The Written Prefix

```java run
import java.util.Arrays;

public final class SortAndDeduplicate {
    static int[] distinctSorted(int[] nums) {
        if (nums.length == 0) return new int[0];
        int[] ordered = nums.clone();
        Arrays.sort(ordered);
        int write = 1;
        for (int read = 1; read < ordered.length; read++) {
            if (ordered[read] != ordered[read - 1]) ordered[write++] = ordered[read];
        }
        return Arrays.copyOf(ordered, write);
    }

    public static void main(String[] args) {
        int[] result = distinctSorted(new int[] {4,1,4,2,1,1});
        if (!Arrays.equals(result, new int[] {1,2,4})) throw new AssertionError(Arrays.toString(result));
    }
}
```

Sorting costs O(n log n), and the compression scan costs O(n). The sorted copy and returned result use O(n) space. The temporary array is safely reused as the output buffer because every write index is at most the current read index.

<!-- stage: applicability -->
### When It Applies

Use sort-and-deduplicate when original order is irrelevant, equality under the chosen order defines groups, and the output needs one value or one summary per group. The invariant is that every completed sorted run has contributed exactly the required representation and the current run is the only unresolved group.

The false friend is in-place deduplication of an already sorted array. That loop is correct only when contiguity is an input guarantee; arbitrary input needs preprocessing or a different structure. A `HashSet` is another valid tool when output order is irrelevant, but it expresses membership rather than run processing.

This technique silently fails if the comparator groups values that are not interchangeable for the output, or if a required payload is discarded while sorting bare keys. Empty input returns no representatives. An all-equal array returns one. Extreme integers need no arithmetic and therefore add no overflow hazard.

<!-- stage: exercises -->
### Exercises

#### [Build] Contains Duplicate (LeetCode 217)
<!-- id: deduplicate-contains-duplicate -->

**Prerequisites.** Sorting a copy and recognizing a sorted run boundary.

**Problem.** Given an integer array `nums`, return `true` if any value occurs at least twice. Preserve the input and solve by sorting followed by an adjacent scan.

**Constraints.** `1 <= nums.length <= 10^5`; values span the signed 32-bit range.

**Example 1.** Input `[1,2,3,1]`, output `true`.

**Example 2.** Input `[1,2,3,4]`, output `false`.

**Hint.** After sorting, where must two equal occurrences meet? The method can stop as soon as one run has length two.

**Changed decision.** The run scan returns a boolean instead of emitting representatives.

#### [Vary] Intersection Of Two Arrays (LeetCode 349)
<!-- id: deduplicate-array-intersection -->

**Prerequisites.** Run representatives and set membership from Chapter 04.

**Problem.** Given integer arrays `nums1` and `nums2`, return their distinct intersection in ascending order. Each value must appear at most once in the result.

**Constraints.** `1 <= nums1.length, nums2.length <= 1000`; values span the signed 32-bit range.

**Example 1.** Input `nums1 = [1,2,2,1]`, `nums2 = [2,2]`, output `[2]`.

**Example 2.** Input `nums1 = [4,9,5]`, `nums2 = [9,4,9,8,4]`, output `[4,9]`.

**Hint.** Put the second array's values in a membership set. Sort the first array, then inspect only the first value of each run.

**Changed decision.** A run representative is emitted only when it also belongs to the second collection.

#### [Boundary] All Equal (Author exercise)
<!-- id: deduplicate-all-equal -->

**Prerequisites.** The core compression loop and output-prefix contracts.

**Problem.** Given an integer array, return its distinct values in ascending order. Your implementation must return exactly one value for any nonempty all-equal input and an empty array for empty input.

**Constraints.** `0 <= nums.length <= 2 * 10^5`; values span the signed 32-bit range.

**Example 1.** Input `[4,4,4]`, output `[4]`.

**Example 2.** Input `[]`, output `[]`; no run exists to contribute a representative.

**Hint.** Initialize the written prefix only after establishing that an element exists. What does the first value represent before the loop begins?

**Changed decision.** The implementation must establish and return the exact meaningful prefix at both size extremes.

#### [Recognize] Longest Word In Dictionary (LeetCode 720)
<!-- id: deduplicate-longest-buildable-word -->

**Prerequisites.** String sorting, sets, and deterministic tie rules.

**Problem.** Given lowercase words, return the longest word that can be built one character at a time such that every proper prefix is also present. If several answers have maximum length, return the lexicographically smallest one; return `""` when none qualifies.

**Constraints.** `1 <= words.length <= 1000`; `1 <= words[i].length <= 30`; words contain lowercase English letters.

**Example 1.** Input `["w","wo","wor","worl","world"]`, output `"world"`.

**Example 2.** Input `["a","banana","app","appl","ap","apply","apple"]`, output `"apple"`.

**Hint.** Sort by length and then lexicographically. A word becomes buildable exactly when its one-character-shorter prefix has already been accepted.

**Changed decision.** Sorting creates deterministic processing groups, while a set stores the accepted prefix frontier rather than numeric run representatives.
