<!-- lesson-kind: standard -->
<!-- lesson-id: comparator-contracts -->
## Comparator Contracts

<!-- stage: context -->
### Order The Deployment Queue

A release system stores deployment requests as objects. Urgent requests should run before routine ones. Requests with the same urgency should follow their submission number so that operators see a deterministic queue. Java cannot infer that policy from the object fields. The program must supply a function that decides the relative position of any two requests.

That function is small enough to fit in one expression, but it defines the meaning of the entire output. A single incorrect sign can place an old urgent release behind a new routine release or make the result change between executions.

<!-- stage: naive -->
### Subtract The Keys

A tempting implementation subtracts numeric keys and falls through to the second key when the first difference is zero.

```java nocompile
Comparator<Request> order = (a, b) -> {
    int byUrgency = a.urgency() - b.urgency();
    if (byUrgency != 0) return byUrgency;
    return a.sequence() - b.sequence();
};
```

For small positive values this appears correct, and sorting still costs O(n log n) comparisons. The defect is hidden in the arithmetic rather than the sorting algorithm.

<!-- stage: bottleneck -->
### Overflow Changes The Sign

Suppose one key is `Integer.MIN_VALUE` and another is `Integer.MAX_VALUE`. Mathematically, subtracting the second from the first is negative. In a 32-bit `int`, the result wraps to `1`. The function therefore reports that the minimum value belongs after the maximum value.

The runtime remains O(n log n), so complexity analysis does not reveal the bug. Worse, inconsistent pairwise answers can violate assumptions used by the sorting implementation. The failure may produce a wrong order or an exception only on particular inputs. A valid comparison must describe a coherent relation over the full domain, not merely pass ordinary examples.

<!-- stage: insight -->
### Obey The Comparator Laws

A Java **Comparator** returns a negative integer when its first argument belongs earlier, zero when the two arguments are interchangeable for this ordering, and a positive integer when the first belongs later. The magnitude has no meaning. `Integer.compare`, `Long.compare`, and the `Comparator.comparing...` helpers produce the sign without overflow-prone subtraction.

<!-- names: antisymmetry, transitivity, comparison equivalence -->

Three laws keep the relation coherent. **Antisymmetry** means reversing the arguments reverses the sign. **Transitivity** means that if `a` precedes `b` and `b` precedes `c`, then `a` precedes `c`. **Comparison equivalence** means that when `compare(a, b) == 0`, either object can occupy that position without changing the required output. Java does not require comparator equality to be the same as `equals`, but the program must understand the consequences when they differ.

For multiple keys, evaluate them in priority order. Compare the primary key first. Only a zero result permits the secondary comparison. `Comparator.comparingInt(Request::urgency).thenComparingLong(Request::sequence)` expresses that structure directly. The safe move is not the fluent syntax itself; it is the fact that each component comparison obeys the same laws and ties are handed to the next declared key.

<!-- stage: variables -->
### Keys And Signs

`primary` is the first property that owns position. `secondary` breaks only primary-key ties. `result` is inspected by sign: negative, zero, or positive. The sorted region has an inclusive first element and an exclusive end supplied by the sorting API; the comparator itself has no index state and must return the same answer whenever it sees the same pair.

<!-- stage: trace -->
### One Overflowing Pair

Compare `Integer.MIN_VALUE` with `Integer.MAX_VALUE`. Subtraction wraps to positive `1`, so the naive function reports the opposite of the required ascending relation. `Integer.compare` returns `-1`, which correctly places the minimum first.

The self-comparison of zero returns `0`. Reversing the extreme arguments returns `1`, the opposite sign of the first safe comparison. These are small checks, but together they exercise the sign contract that the sort relies on. A chained comparator applies the same process to the next key only when the current result is zero.

Notice that the comparison function never reads an array index or remembers an earlier call. Its answer depends only on the two supplied values, which keeps repeated comparisons consistent throughout the sort.

```trace
{"cells":["MIN","0","MAX"],"pointers":["a","b"],"steps":[{"at":{"a":0,"b":2},"vars":{"a-b":1},"note":"Subtraction overflows to 1, falsely placing MIN after MAX."},{"at":{"a":0,"b":2},"vars":{"compare":-1},"note":"Integer.compare returns -1, so MIN correctly belongs first."},{"at":{"a":1,"b":1},"vars":{"compare":0},"note":"Comparing a value with itself returns zero."},{"at":{"a":2,"b":0},"vars":{"compare":1},"note":"Reversing the arguments reverses the sign."}]}
```

<!-- stage: code -->
### Chain The Declared Keys

```java run
public final class RequestOrdering {
    record Request(int urgency, long sequence, String service) {}

    static final java.util.Comparator<Request> REQUEST_ORDER =
            java.util.Comparator.comparingInt(Request::urgency)
                    .thenComparingLong(Request::sequence)
                    .thenComparing(Request::service);

    public static void main(String[] args) {
        Request earlier = new Request(1, 8, "search");
        Request later = new Request(1, 9, "billing");
        if (REQUEST_ORDER.compare(earlier, later) >= 0) throw new AssertionError();
    }
}
```

Urgency owns the first decision, sequence owns an urgency tie, and service makes the final output deterministic if both numeric keys match. Each helper uses a type-appropriate comparison rather than subtraction. Sorting `n` requests costs O(n log n) comparisons. The comparator stores no per-call collection, so its own additional space is O(1); comparing the final strings may inspect characters until they differ.

<!-- stage: applicability -->
### When It Applies

Use a comparator when objects or boxed values need an order other than their natural one. State the invariant as follows: for every adjacent pair in the result, the comparator returns a value less than or equal to zero, and the relation obeys antisymmetry and transitivity across the whole sequence.

The false friend is a predicate such as “has higher urgency.” A boolean does not distinguish earlier, equal, and later, so it cannot express the full contract. Another false friend is relying on input order for ties while using an API whose stability has not been established.

The technique silently fails when a comparator closes over mutable state, uses random values, or treats a required secondary distinction as zero. Java-specific hazards include subtraction overflow, accidentally reversing one key but not the next, and boxing primitive arrays merely to access a comparator overload. Test extreme values, equal keys, and triples—not just one ordinary pair.

<!-- stage: exercises -->
### Exercises

#### [Build] Safe Integer Comparator (Author exercise)
<!-- id: safe-integer-comparator -->

**Prerequisites.** The comparator sign contract and boxed integer arrays.

**Problem.** Given an `Integer[] values`, return a new ascending array using an explicit comparator that is correct for every signed 32-bit value. Leave the input unchanged.

**Constraints.** `0 <= values.length <= 10^5`; entries are non-null integers. Target O(n log n) time.

**Example 1.** Input `values = [3, -7, 3]`, output `[-7, 3, 3]`.

**Example 2.** Input `values = [2147483647, -2147483648]`, output `[-2147483648, 2147483647]`.

**Hint.** The comparator needs only the sign of the relation. Which standard method produces that sign without computing a potentially overflowing difference?

**Changed decision.** The ordering is written as an explicit safe comparator rather than delegated to primitive natural order.

#### [Vary] Chained Keys (Author exercise)
<!-- id: comparator-chained-keys -->

**Prerequisites.** The Build exercise and Java records.

**Problem.** Sort `Ticket(priority, owner)` records by smaller priority first, then by owner in lexicographic order. Return a new list and leave the input list unchanged.

**Constraints.** `0 <= tickets.size() <= 10^5`; priorities are signed integers and owners are non-null ASCII strings of length 1 to 30.

**Example 1.** Input `[(2,"zoe"),(1,"mia"),(1,"amy")]`, output `[(1,"amy"),(1,"mia"),(2,"zoe")]`.

**Example 2.** Input `[(0,"sam"),(0,"sam")]`, output contains the two interchangeable records consecutively.

**Hint.** When may the owner comparison affect the answer? Express that handoff directly instead of packing both keys into one arithmetic expression.

**Changed decision.** A secondary string key now owns primary-key ties.

#### [Boundary] Equal Keys And Extreme Values (Author exercise)
<!-- id: comparator-equal-extreme-keys -->

**Prerequisites.** Chained comparison and the three comparator laws.

**Problem.** Implement and test an ascending comparator for `Entry(value, id)`. Order by `value`, then `id`, across the full integer range. Return whether the comparator satisfies self-equality, reversed-sign, and transitivity checks for every triple in the supplied list.

**Constraints.** `0 <= entries.size() <= 40`; both fields are arbitrary 32-bit integers. An empty or one-element list satisfies the checks.

**Example 1.** Input `[(MIN,4),(MAX,1),(MIN,2)]`, output `true`; the safe comparison orders both extreme and tied values coherently.

**Example 2.** Input `[(7,1),(7,1),(7,1)]`, output `true`; interchangeable records compare as zero.

**Hint.** Pair checks catch reversed signs, but which nested-loop check exposes a broken relation across three values?

**Changed decision.** Instead of consuming a comparator, the exercise validates its laws over hostile keys.

#### [Recognize] Largest Number Comparator (LeetCode 179)
<!-- id: largest-number-comparator-contract -->

**Prerequisites.** String comparison and a descending domain-specific comparator.

**Problem.** Arrange non-negative integers so their concatenated decimal representation is as large as possible, then return that representation as a string.

**Constraints.** `1 <= nums.length <= 100` and `0 <= nums[i] <= 10^9`. The output may exceed every numeric type.

**Example 1.** Input `nums = [12, 121]`, output `"12121"`; the pair is decided by `"12121"` versus `"12112"`.

**Example 2.** Input `nums = [0, 0]`, output `"0"`; a valid result has no redundant leading zeroes.

**Hint.** For strings `a` and `b`, compare the two complete pair orders. Which concatenation should come first to maximize the prefix immediately?

**Changed decision.** Comparator correctness now depends on pairwise concatenation rather than numeric magnitude.

