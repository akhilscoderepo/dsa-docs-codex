<!-- lesson-kind: standard -->
<!-- lesson-id: stability-and-ties -->
## Stability And Ties

<!-- stage: context -->
### Keep Earlier Alerts Ahead

An incident console receives alerts in arrival order. Operators want severity 1 alerts first, followed by severity 2 and severity 3. Within one severity, the earlier alert must remain ahead because another system has already announced that sequence to responders.

Severity determines the groups, but it does not determine the order inside a group. The missing requirement is temporal: equal-key alerts must retain the sequence in which they arrived. A correct solution must decide whether the sorting operation guarantees that behavior or whether the original position must become an explicit key.

<!-- stage: naive -->
### Add An Arbitrary Tie-Breaker

A developer notices that equal severities produce comparator zero and adds the alert identifier as a secondary key.

```java nocompile
Comparator<Alert> order = Comparator.comparingInt(Alert::severity)
        .thenComparing(Alert::id);
```

The result is deterministic, but it is not the required order. Identifiers describe identity, not arrival. An alert named `A-100` can move ahead of an earlier `Z-900` even though their severities match. A convenient tie-breaker is still wrong when it does not come from the problem contract.

<!-- stage: bottleneck -->
### Reconstructing Arrival Order Adds Work

One repair sorts by severity, scans every equal-severity run, looks up each alert's former index, and rearranges the run. The sort still costs O(n log n), while naive index lookup can add O(n^2) work. Even with an index map, the method duplicates the same tie rule across preprocessing and postprocessing.

The real bottleneck is uncertainty about who owns a tie. If encounter order owns it, a stable sort already preserves the needed information. If stability is not promised, original position must be stored before sorting. Guessing at either property makes correctness depend on an implementation detail outside the algorithm.

<!-- stage: insight -->
### Preserve Or Encode The Tie

A **stable sort** preserves the relative order of elements that compare as zero. Their order in the output matches their **encounter order** in the input. Java specifies stable sorting for `Arrays.sort(Object[])` and `List.sort`, so object records with equal comparator keys can deliberately rely on that contract.

<!-- names: stable sort, encounter order, explicit index tie-breaker -->

Stability applies only when the comparator returns zero. If the comparator uses an arbitrary secondary field, the elements are no longer tied and stability has nothing to preserve. Conversely, if the output needs a stated secondary order such as name ascending, returning zero and hoping stability will create that order is incorrect.

When the chosen operation does not promise stability, or when the data crosses an API boundary that may reorder equal keys, attach each element's original index and use an **explicit index tie-breaker**. Compare the business key first and the saved index second. This decorates the object with enough information to reproduce encounter order under any correct comparison sort.

Primitive-array sorting exposes no useful identity-preservation guarantee: equal primitive values are indistinguishable after sorting. Stability matters when separate records share an ordering key but retain different payloads, identifiers, or histories.

<!-- stage: variables -->
### Key, Position, And Payload

`key` determines the primary group. `originalIndex` records encounter order before any rearrangement. `payload` is the rest of the object that must travel with its key. `compare(a, b) == 0` is a semantic claim: under the requested ordering, either element may occupy the other's position unless a stable-sort requirement explicitly preserves their prior sequence.

<!-- stage: trace -->
### Watch Equal Alerts Stay In Order

The input is `Z-900(severity 1)`, `B-200(severity 2)`, and `A-100(severity 1)`. The primary comparison moves both severity 1 alerts before the severity 2 alert. The two severity 1 alerts compare as zero because arrival order—not identifier order—owns their tie.

A stable sort therefore produces `Z-900, A-100, B-200`. Adding identifier as a key would instead produce `A-100, Z-900, B-200`, which is deterministic but violates the temporal contract. If stability were unavailable, decorating the records with indices 0, 1, and 2 and comparing severity followed by index would reproduce the stable result explicitly.

```trace
{"cells":["Z-900:s1@0","B-200:s2@1","A-100:s1@2"],"pointers":["earlier","later"],"steps":[{"at":{"earlier":0,"later":2},"vars":{"severity":"1 vs 1"},"note":"The primary keys tie, so the severity comparator returns zero."},{"at":{"earlier":0,"later":2},"vars":{"stable":"index 0 before 2"},"note":"Stable sorting preserves Z-900 before A-100."},{"at":{"earlier":2,"later":1},"vars":{"severity":"1 vs 2"},"note":"A-100 moves ahead of the severity 2 alert."},{"at":{"earlier":0,"later":1},"vars":{"order":"Z-900, A-100, B-200"},"note":"The output groups severity while retaining encounter order inside the tied group."}]}
```

<!-- stage: code -->
### Use The Stable Object Sort Contract

```java run
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public final class StableAlertOrder {
    record Alert(String id, int severity) {}

    static List<Alert> bySeverity(List<Alert> alerts) {
        List<Alert> result = new ArrayList<>(alerts);
        result.sort(Comparator.comparingInt(Alert::severity));
        return result;
    }

    public static void main(String[] args) {
        List<Alert> result = bySeverity(List.of(
                new Alert("Z-900", 1),
                new Alert("B-200", 2),
                new Alert("A-100", 1)));
        List<Alert> expected = List.of(
                new Alert("Z-900", 1),
                new Alert("A-100", 1),
                new Alert("B-200", 2));
        if (!result.equals(expected)) throw new AssertionError(result);
    }
}
```

`List.sort` is stable, so the single-key comparator is complete for this contract. Copying costs O(n) space and preserves the caller's list. Sorting costs O(n log n) comparisons, each O(1) here.

<!-- stage: applicability -->
### When It Applies

Use stable sorting when the prompt says to preserve original, arrival, or encounter order among equal keys and the selected API explicitly guarantees stability. The invariant is two-part: primary keys are ordered, and for any two records with equal keys, their relative order matches the input.

The false friend is deterministic ordering. Sorting by a convenient identifier produces repeatable output but may replace the required encounter order. Another false friend is assuming that all Java sort overloads have the same guarantee. Check the exact API and representation; an object-array guarantee does not authorize claims about primitive arrays.

The technique silently fails when a comparator accidentally distinguishes supposed ties or when a later collection, serialization step, or distributed merge discards encounter order. Empty and singleton inputs are already stable. Duplicate references remain valid. If records enter from multiple sources with no shared encounter order, the contract needs a real sequence number rather than a local stable sort.

<!-- stage: exercises -->
### Exercises

#### [Build] Stable Score Sort (Author exercise)
<!-- id: stable-score-sort -->

**Prerequisites.** Object comparators and the stable `List.sort` contract.

**Problem.** Given a list of `Submission(user, score)` records in arrival order, return a new list ordered by higher score first. Preserve arrival order among equal scores and leave the input unchanged.

**Constraints.** `0 <= submissions.size() <= 10^5`; users are non-null ASCII strings of length 1 to 30; scores are signed 32-bit integers.

**Example 1.** Input `[("zoe",90),("amy",80),("ben",90)]`, output `[("zoe",90),("ben",90),("amy",80)]`.

**Example 2.** Input `[("z",7),("a",7)]`, output `[("z",7),("a",7)]`; the names do not own the tie.

**Hint.** Which single field belongs in the comparator, and what documented property supplies the equal-score order?

**Changed decision.** Comparator zero intentionally delegates equal-key ordering to a stable object sort.

#### [Vary] Explicit Index Tie (Author exercise)
<!-- id: explicit-index-tie -->

**Prerequisites.** The Build exercise and decorating records with their original positions.

**Problem.** Given `Message(topic, text)` records, return them ordered by topic ascending while preserving input order within each topic. Implement the preservation explicitly by attaching the original index rather than relying on sort stability.

**Constraints.** `0 <= messages.size() <= 10^5`; topic and text are non-null ASCII strings of length 1 to 40.

**Example 1.** Input `[("ops","third"),("api","first"),("ops","fourth"),("api","second")]`, output `[("api","first"),("api","second"),("ops","third"),("ops","fourth")]`.

**Example 2.** Input `[("x","b"),("x","a")]`, output remains `[("x","b"),("x","a")]`.

**Hint.** Store a position before sorting. Which key must be compared after equal topics to reconstruct encounter order independently of the sorting implementation?

**Changed decision.** Original position becomes data and owns every primary-key tie explicitly.

#### [Boundary] Comparator Equality (Author exercise)
<!-- id: comparator-equality-boundary -->

**Prerequisites.** Comparator zero semantics and exhaustive pair checks.

**Problem.** Given `Entry(group, rank, label)` records, return `true` if a comparator ordered by group, rank, and label returns zero exactly for pairs with equal values in all three fields. Return `false` otherwise.

**Constraints.** `0 <= entries.size() <= 200`; group and label are non-null ASCII strings of length 1 to 20; rank spans the signed 32-bit range.

**Example 1.** Input `[("a",1,"x"),("a",1,"y")]`, output `true`; the label key distinguishes the records.

**Example 2.** Input `[("a",MIN,"x"),("a",MIN,"x")]`, output `true`; equal tuples correctly compare as zero.

**Hint.** Inspect every pair. Compare the comparator's zero result with equality of the complete required key tuple.

**Changed decision.** Comparator equality itself becomes the property under test rather than an incidental sorting result.

#### [Recognize] Sort Integers By The Number Of 1 Bits (LeetCode 1356)
<!-- id: stable-sort-by-bit-count -->

**Prerequisites.** Key chaining and `Integer.bitCount`.

**Problem.** Given an integer array `arr`, return the values ordered by increasing number of set bits in their binary representation. When two values have the same bit count, place the smaller numeric value first.

**Constraints.** `1 <= arr.length <= 500`; `0 <= arr[i] <= 10^4`.

**Example 1.** Input `[0,1,2,3,4,5,6,7,8]`, output `[0,1,2,4,8,3,5,6,7]`.

**Example 2.** Input `[8,4,2,1]`, output `[1,2,4,8]`; all four values have one set bit, so numeric order owns the tie.

**Hint.** Stability cannot replace the stated numeric tie-break. What are the two comparator keys, in order?

**Changed decision.** Equal derived keys require a semantic numeric tie-break rather than encounter order.
