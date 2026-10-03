<!-- lesson-kind: standard -->
<!-- lesson-id: object-ordering -->
## Object Ordering

<!-- stage: context -->
### Publish A Deterministic Leaderboard

A contest service receives `Student(name, score)` records. The public leaderboard places a higher score first. When two students have the same score, the lexicographically smaller name comes first. The second rule is not presentation polish: clients cache rows by position, so an unspecified tie can make equal-score students exchange places between otherwise identical responses.

The records already contain every fact needed to decide their order. What is missing is a precise statement of which field owns the first decision and which field owns a tie. That statement becomes executable when it is encoded as a comparator over the complete object.

<!-- stage: naive -->
### Sort One Field And Hope

A first attempt compares only scores.

```java nocompile
students.sort((a, b) -> Integer.compare(b.score(), a.score()));
```

The code correctly places higher scores first, but it returns zero for every equal-score pair. That answer means the records are interchangeable for the requested order. They are not: the contract still distinguishes them by name. The current result may appear correct when the input happens to arrive alphabetically, which makes the missing rule easy to overlook.

<!-- stage: bottleneck -->
### A Partial Order Leaves Work Unspecified

Adding a second pass over equal-score runs is possible. After sorting by score, the program can locate every run, sort that subrange by name, and then continue. The total comparison cost can remain O(n log n), but the implementation now has two sorting phases, run boundaries, and two places that must agree on the ordering contract.

The deeper problem is not asymptotic speed. The primary-only comparator describes less order than the output requires. Any later operation that uses the same comparator—sorting, a `TreeSet`, or a priority queue—will inherit the same omission. The complete key sequence should live in one reusable relation.

<!-- stage: insight -->
### Give Every Tie An Owner

**Object ordering** compares records by a declared sequence of fields. This is also called **lexicographic key ordering**: compare the first key; if it differs, return that decision; otherwise hand the pair to the next key. The first nonzero comparison determines the order.

<!-- names: object ordering, lexicographic key ordering, tie ownership -->

For the leaderboard, score is the primary key and name owns a score tie. This explicit **tie ownership** prevents the result from depending on accidental input order. Because score is descending, only that component is reversed. Name remains ascending. `Comparator.comparingInt(Student::score).reversed().thenComparing(Student::name)` says exactly that. Reversing the finished chain would reverse both fields and would therefore implement a different contract.

The same idea applies to rows represented as arrays. `Arrays.sort(intervals, Comparator.comparingInt(row -> row[0]))` is valid because `int[][]` is an array of `int[]` objects. By contrast, the elements of a plain `int[]` are primitives, so the comparator overload does not apply to them. A record is often clearer than an anonymous row because field names expose the key contract and prevent index mix-ups.

<!-- stage: variables -->
### Records, Keys, And Direction

`primary` is the field that usually decides the pair. `secondary` is consulted only when the primary comparison returns zero. `direction` belongs to each key separately: descending score does not imply descending name. `ordered` is a copy when the caller's list must remain unchanged. The comparator itself should be stateless; it reads only the two objects supplied to it.

<!-- stage: trace -->
### Follow One Tie

Start with `Mira(92)`, `Ben(85)`, and `Ana(92)`. Comparing Mira with Ben stops at score because 92 belongs before 85. Comparing Ana with Mira reaches a score tie, so name takes ownership. `"Ana"` is lexicographically smaller than `"Mira"`, placing Ana first.

The final order is `Ana(92), Mira(92), Ben(85)`. Each adjacent pair now satisfies the complete relation: score descends, and names ascend only inside an equal-score run. Notice that the comparison never needs the records' current indices. The order follows from object fields, so another collection can reuse it without reproducing the rule or carrying hidden position state.

```trace
{"cells":["Mira:92","Ben:85","Ana:92"],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":1},"vars":{"score":"92 vs 85"},"note":"The score comparison decides immediately: Mira belongs before Ben."},{"at":{"left":2,"right":0},"vars":{"score":"92 vs 92"},"note":"Equal scores transfer ownership to the name key."},{"at":{"left":2,"right":0},"vars":{"name":"Ana vs Mira"},"note":"Ana is lexicographically smaller, so Ana belongs before Mira."},{"at":{"left":0,"right":2},"vars":{"order":"Ana, Mira, Ben"},"note":"The completed order is score descending and name ascending within ties."}]}
```

<!-- stage: code -->
### Encode The Whole Contract Once

```java run
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public final class ObjectOrdering {
    record Student(String name, int score) {}

    static final Comparator<Student> LEADERBOARD_ORDER =
            Comparator.comparingInt(Student::score).reversed()
                    .thenComparing(Student::name);

    static List<Student> leaderboard(List<Student> students) {
        List<Student> ordered = new ArrayList<>(students);
        ordered.sort(LEADERBOARD_ORDER);
        return ordered;
    }

    public static void main(String[] args) {
        List<Student> result = leaderboard(List.of(
                new Student("Mira", 92),
                new Student("Ben", 85),
                new Student("Ana", 92)));
        List<Student> expected = List.of(
                new Student("Ana", 92),
                new Student("Mira", 92),
                new Student("Ben", 85));
        if (!result.equals(expected)) throw new AssertionError(result);
    }
}
```

Copying the references costs O(n) space and protects the input list. Sorting performs O(n log n) comparisons. Integer comparison is O(1); a name tie-break may inspect up to O(s) characters, so the worst-case time is O(n log n * s) for maximum name length `s`.

<!-- stage: applicability -->
### When It Applies

Use object ordering when each item has several fields and the prompt assigns those fields different priorities or directions. The invariant is precise: for every adjacent pair in the result, the complete comparator returns a nonpositive value, and every zero result means the two records are interchangeable under all output rules.

The false friend is stability. A stable sort preserves input order when the comparator returns zero, but stability cannot invent an alphabetical tie rule. If arrival order really is the required tie-break, say so explicitly and verify that the chosen sort promises stability; Lesson 05 treats that contract separately. Another false friend is sorting a field and losing the association with the rest of its record.

This technique fails when a field direction is reversed at the wrong level, when parsing logic disagrees about where a key begins, or when zero is returned before all required tie-breakers have been examined. Empty input needs no branch. Duplicate records may compare as zero. Extreme numeric keys remain safe when comparison helpers are used rather than subtraction.

<!-- stage: exercises -->
### Exercises

#### [Build] Sort Scores (Author exercise)
<!-- id: object-sort-scores -->

**Prerequisites.** Java records, comparator chaining, and copying a list before sorting.

**Problem.** Given a list of `Student(name, score)` records, return a new list ordered by higher score first and then by lexicographically smaller name. Do not modify the input list.

**Constraints.** `0 <= students.size() <= 10^5`; names are non-null ASCII strings of length 1 to 30; scores are signed 32-bit integers.

**Example 1.** Input `[("Mira",92),("Ben",85),("Ana",92)]`, output `[("Ana",92),("Mira",92),("Ben",85)]`.

**Example 2.** Input `[("Zed",MIN),("Amy",MAX)]`, output `[("Amy",MAX),("Zed",MIN)]`.

**Hint.** Reverse only the score component. Which method should receive `thenComparing` so that the name direction remains ascending?

**Changed decision.** The comparator now reads named fields from a record and assigns a direction to each key.

#### [Vary] Reorder Data In Log Files (LeetCode 937)
<!-- id: object-reorder-log-files -->

**Prerequisites.** The Build exercise, string slicing, and stable treatment of records excluded from the comparator order.

**Problem.** Given logs whose first token is an identifier, reorder them so that letter-logs precede digit-logs. Sort letter-logs by content and then identifier. Preserve the original relative order of digit-logs.

**Constraints.** `1 <= logs.length <= 100`; each log contains an identifier followed by at least one lowercase word or digit token; all logs fit within 100 characters.

**Example 1.** Input `["dig1 8 1","let1 art can","let2 own kit","let3 art can"]`, output `["let1 art can","let3 art can","let2 own kit","dig1 8 1"]`.

**Example 2.** Input `["d1 3 4","d2 1 2"]`, output `["d1 3 4","d2 1 2"]`; digit-log arrival order is retained.

**Hint.** Split each log only at its first space. Which records participate in content ordering, and which records should bypass it entirely?

**Changed decision.** Some objects are ordered by parsed fields while a second category preserves its existing sequence.

#### [Boundary] Equal Primary Keys (Author exercise)
<!-- id: object-equal-primary-keys -->

**Prerequisites.** Chained keys and safe comparisons over extreme integers.

**Problem.** Given `Job(priority, owner, id)` records, return a new list ordered by smaller priority, then owner, then smaller id. The final id key must make jobs with equal priority and owner deterministic.

**Constraints.** `0 <= jobs.size() <= 10^5`; priority and id span the full signed 32-bit range; owner is a non-null ASCII string of length 1 to 20.

**Example 1.** Input `[(1,"ops",9),(1,"ops",2),(1,"api",7)]`, output `[(1,"api",7),(1,"ops",2),(1,"ops",9)]`.

**Example 2.** Input `[(MIN,"x",MAX),(MIN,"x",MIN)]`, output `[(MIN,"x",MIN),(MIN,"x",MAX)]`.

**Hint.** Write the three-key tuple on paper. A comparison may advance to the next component only after what result from the current component?

**Changed decision.** A tertiary key now owns a tie that two visible business fields cannot resolve.

#### [Recognize] Queue Reconstruction By Height (LeetCode 406)
<!-- id: object-queue-reconstruction -->

**Prerequisites.** Object ordering, list insertion, and interpreting a field relative to a partial result.

**Problem.** Each person is `[height, k]`, where `k` is the number of people in front whose height is at least `height`. Reconstruct and return any queue satisfying every record.

**Constraints.** `1 <= people.length <= 2000`; `0 <= height <= 10^6`; `0 <= k < people.length`; the input is guaranteed to admit a valid queue.

**Example 1.** Input `[[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]`, one valid output is `[[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]`.

**Example 2.** Input `[[6,0],[5,0]]`, output `[[5,0],[6,0]]`.

**Hint.** If every already-placed person is at least as tall as the next person, what does that person's `k` value become inside the partial list?

**Changed decision.** The object order is chosen to make an insertion index meaningful, not merely to produce the final sorted sequence.
