<!-- lesson-kind: standard -->
<!-- lesson-id: ordering-contracts -->
## Ordering Contracts

<!-- stage: context -->
### Which Shipment Comes First

A dispatch service receives shipments from several warehouses. Each record has a promised delivery day and an identifier. The dashboard must show earlier deliveries first. When two shipments share a day, the smaller identifier must appear first so every refresh produces the same result.

Before choosing an algorithm, we need a precise answer to one question: for any two records, which one belongs first? “Sort the shipments” is incomplete. It says nothing about ties, direction, or whether equal-looking records may exchange positions. The required output is defined by those pairwise decisions.

<!-- stage: naive -->
### Repeatedly Find The Smallest

For integers, an obvious method fixes the output from left to right. At each position, scan the unresolved suffix, find its smallest value, and swap it into place.

```java
static void selectionSort(int[] values) {
    for (int fixed = 0; fixed < values.length; fixed++) {
        int smallest = fixed;
        for (int scan = fixed + 1; scan < values.length; scan++) {
            if (values[scan] < values[smallest]) smallest = scan;
        }
        int temporary = values[fixed];
        values[fixed] = values[smallest];
        values[smallest] = temporary;
    }
}
```

The method is correct. After each outer iteration, the fixed prefix contains the smallest values in nondecreasing order.

<!-- stage: bottleneck -->
### The Suffix Keeps Shrinking

The first output position compares against nearly every value. The second position repeats the scan over nearly the entire remaining suffix, even though the first scan already compared many of those values. For four values the method makes six comparisons. For `n` values it makes `(n - 1) + (n - 2) + ... + 1`, which is `n(n - 1) / 2`.

That is O(n^2) time. At 50,000 values, the count is about 1.25 billion comparisons. The method also mutates the caller's array, which is wrong when the contract requires the original order to remain available. We need both a faster implementation and a statement precise enough that another implementation can produce the same result.

<!-- stage: insight -->
### Define Every Pair

An ordering begins with a decision for every pair `a` and `b`: `a` comes before `b`, `b` comes before `a`, or the two are interchangeable for this output. Those decisions form a **comparison contract**. A sorting implementation may choose pivots, merge runs, or use another internal strategy, but it must obey that contract.

For the result to be meaningful, the decisions must form a **total order**. Comparing an item with itself must report equality. Reversing the arguments must reverse the sign. Most importantly, the decisions must be transitive: if `a` belongs before `b` and `b` belongs before `c`, then `a` must belong before `c`. A comparator that violates transitivity does not describe a coherent sequence, so the sorting API cannot repair it.

<!-- names: comparison contract, total order, tie rule -->

The contract also owns equality. When two objects share the primary field, a **tie rule** decides whether they are interchangeable or whether a secondary field must break the tie. For the shipment dashboard, delivery day is primary and identifier is secondary. Writing both keys prevents output from changing merely because input arrival order changed.

For primitive integers in ascending order, Java's natural ordering already supplies these properties. For custom records, the code must express them explicitly. Use `Integer.compare(a, b)` or `Long.compare(a, b)` for numeric keys. Returning `a - b` can overflow and reverse the intended sign, so it can violate the contract even though it looks concise.

<!-- stage: variables -->
### Contract And Ownership

`input` is the caller-owned sequence. `ordered` is either that same array when mutation is permitted or a copy when it is not. `compare(a, b)` returns a negative value, zero, or a positive value according to the required sequence. Primary and secondary keys are evaluated in that order; the secondary key is consulted only when the primary comparison is zero.

<!-- stage: trace -->
### Count The Repeated Work

Use the direct method on `[7, -2, 7, 3]`. Position zero starts with `7` as its candidate. The scan reaches `-2` and replaces the candidate, then still examines both remaining values. After `-2` is placed, position one begins another suffix scan. It compares the two copies of `7`, then discovers `3` and places it next.

The duplicate values matter. Their comparison reports equality, so either copy may fill the next equal position unless the contract supplies additional identity and a tie rule. After six comparisons the array is `[-2, 3, 7, 7]`. The trace makes the quadratic pattern visible: fixing one position does not preserve the comparisons needed by the next position.

```trace
{"cells":[7,-2,7,3],"pointers":["fixed","scan"],"steps":[{"at":{"fixed":0,"scan":0},"vars":{"smallest":7,"comparisons":0},"note":"Position 0 is unresolved; start with 7 as its candidate."},{"at":{"fixed":0,"scan":1},"vars":{"smallest":-2,"comparisons":1},"note":"Compare index 1; -2 is smaller, so it becomes the candidate."},{"at":{"fixed":0,"scan":2},"vars":{"smallest":-2,"comparisons":2},"note":"Compare index 2; keep -2 as the candidate."},{"at":{"fixed":0,"scan":3},"vars":{"smallest":-2,"comparisons":3},"note":"Compare index 3; keep -2 as the candidate."},{"at":{"fixed":0,"scan":1},"vars":{"smallest":-2,"comparisons":3},"note":"Place -2 at index 0; that prefix now satisfies ascending order."},{"at":{"fixed":1,"scan":1},"vars":{"smallest":7,"comparisons":3},"note":"Position 1 is unresolved; start with 7 as its candidate."},{"at":{"fixed":1,"scan":2},"vars":{"smallest":7,"comparisons":4},"note":"Compare index 2; keep 7 as the candidate."},{"at":{"fixed":1,"scan":3},"vars":{"smallest":3,"comparisons":5},"note":"Compare index 3; 3 is smaller, so it becomes the candidate."},{"at":{"fixed":1,"scan":3},"vars":{"smallest":3,"comparisons":5},"note":"Place 3 at index 1; that prefix now satisfies ascending order."},{"at":{"fixed":2,"scan":2},"vars":{"smallest":7,"comparisons":5},"note":"Position 2 is unresolved; start with 7 as its candidate."},{"at":{"fixed":2,"scan":3},"vars":{"smallest":7,"comparisons":6},"note":"Compare index 3; keep 7 as the candidate."},{"at":{"fixed":2,"scan":2},"vars":{"smallest":7,"comparisons":6},"note":"Place 7 at index 2; that prefix now satisfies ascending order."},{"at":{"fixed":3,"scan":3},"vars":{"smallest":7,"comparisons":6},"note":"Position 3 is unresolved; start with 7 as its candidate."},{"at":{"fixed":3,"scan":3},"vars":{"smallest":7,"comparisons":6},"note":"Place 7 at index 3; that prefix now satisfies ascending order."}]}
```

<!-- stage: code -->
### Preserve The Caller

```java
static int[] sortedAscendingCopy(int[] input) {
    int[] ordered = java.util.Arrays.copyOf(input, input.length);
    java.util.Arrays.sort(ordered);
    return ordered;
}
```

This method makes two decisions explicit. The required relation is the natural ascending order of primitive integers, and the caller retains ownership of `input`, so the method sorts a copy. Java's library provides the O(n log n) sorting work for the general case. Copying costs O(n) time and O(n) space; sorting dominates the time bound, so the complete method is O(n log n) time and O(n) additional space for the returned copy.

If mutation is allowed, sort the original array and avoid the explicit copy. Do not add that optimization silently. Mutation is part of the method's contract, not an internal detail.

<!-- stage: applicability -->
### When It Applies

Write the ordering contract before sorting whenever the problem depends on direction, multiple keys, or deterministic treatment of equal primary keys. The invariant after sorting is that every adjacent pair appears in an order permitted by the same comparison relation; transitivity then extends that local fact across the whole sequence.

The nearest false friend is partitioning. A problem that merely wants all even values before all odd values may accept many outputs and does not require a total sequence within either group. Another false friend is selection: finding the kth value does not necessarily justify paying for the complete order.

The technique silently fails when the comparison is inconsistent. Numeric subtraction is the common Java failure because overflow can report that `Integer.MIN_VALUE` belongs after `Integer.MAX_VALUE`. A second failure is forgetting a required secondary key and then assuming equal primary keys will appear in a particular order. State whether ties are interchangeable, stable, or explicitly broken.

<!-- stage: exercises -->
### Exercises

#### [Build] Sort An Array (LeetCode 912)
<!-- id: sort-array-merge-contract -->

**Prerequisites.** Arrays, recursion, and the ordering contract from this lesson.

**Problem.** Given an integer array `nums`, return its values in ascending order. Do not call a library sorting method in the submitted algorithm. Implement a comparison-based O(n log n) method and return the sorted array.

**Constraints.** `1 <= nums.length <= 5 * 10^4` and `-5 * 10^4 <= nums[i] <= 5 * 10^4`. Target O(n log n) time.

**Example 1.** Input `nums = [8, -1, 4, 4]`, output `[-1, 4, 4, 8]`; equal values remain adjacent under ascending order.

**Example 2.** Input `nums = [0]`, output `[0]`; a one-element range is already ordered.

**Hint.** Split the range until each piece contains one value. During reconstruction, what information lets you choose the next value without scanning either half again?

**Changed decision.** Build the complete ascending order without relying on Java's library implementation.

#### [Vary] Sort Boxed Integers In Descending Order (Author exercise)
<!-- id: boxed-integers-descending -->

**Prerequisites.** The Build exercise and Java arrays of reference types.

**Problem.** Given an `Integer[] values`, return a new array containing the same references in descending numeric order. Leave the input array unchanged and use a comparator rather than reversing an ascending result.

**Constraints.** `0 <= values.length <= 10^5`; every entry is non-null and may be any 32-bit signed integer. Target O(n log n) time.

**Example 1.** Input `values = [6, -3, 6, 2]`, output `[6, 6, 2, -3]`; the comparator places larger values first.

**Example 2.** Input `values = []`, output `[]`; copying and sorting an empty object array is valid.

**Hint.** The comparator overload accepts an object array, not `int[]`. Which comparison reverses the argument order without negating or subtracting extreme integers?

**Changed decision.** Direction changes to descending, and caller ownership requires sorting a copy of a boxed array.

#### [Boundary] Extreme Comparator (Author exercise)
<!-- id: extreme-integer-order -->

**Prerequisites.** The Vary exercise and the sign contract of a Java comparator.

**Problem.** Given an `Integer[] values`, return a new ascending array that remains correct when the input contains `Integer.MIN_VALUE` and `Integer.MAX_VALUE`. Implement the comparator explicitly and do not use subtraction.

**Constraints.** `0 <= values.length <= 10^5`; entries are non-null 32-bit signed integers. Target O(n log n) time and O(n) returned space.

**Example 1.** Input `values = [2147483647, -2147483648, 0]`, output `[-2147483648, 0, 2147483647]`.

**Example 2.** Input `values = [-2147483648, -2147483648]`, output `[-2147483648, -2147483648]`; equal extremes compare as zero.

**Hint.** Evaluate what `Integer.MIN_VALUE - Integer.MAX_VALUE` becomes in a 32-bit `int`. Which standard comparison method returns only the required sign without arithmetic overflow?

**Changed decision.** The hostile values make overflow safety part of correctness rather than a style preference.

#### [Recognize] Largest Concatenated Number (LeetCode 179)
<!-- id: largest-concatenated-number -->

**Prerequisites.** Comparator direction, string construction, and explicit tie handling.

**Problem.** Given non-negative integers, arrange their decimal strings so their concatenation is numerically largest. Return the result as a string because it may not fit a numeric type.

**Constraints.** `1 <= nums.length <= 100` and `0 <= nums[i] <= 10^9`. Target O(n log n) comparisons, excluding the characters inspected by each comparison.

**Example 1.** Input `nums = [8, 80, 808]`, output `"880880"`; comparing concatenations places `8` before `808`, then `80`.

**Example 2.** Input `nums = [0, 0, 0]`, output `"0"`; the representation must collapse multiple leading zeroes.

**Hint.** Numeric magnitude is not the decisive relation: `80` and `808` must be judged by two possible pairwise concatenations. Which of `a + b` and `b + a` should appear first?

**Changed decision.** Natural integer order is replaced by a domain-specific pairwise contract over decimal strings.

