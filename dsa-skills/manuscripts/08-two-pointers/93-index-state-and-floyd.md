<!-- lesson-kind: combination -->
<!-- lesson-id: index-state-and-floyd -->
## Index State And Floyd

<!-- stage: context -->
### When Values Direct The Walk

Suppose an array does more than store numbers. Each number names the position to visit next. Starting from the first named position produces a walk through the array, and a repeated value causes two parts of that walk to enter the same position. The interview problem adds two restrictions: the array must remain unchanged, and the method may keep only a constant amount of extra state. Those restrictions determine whether the representation is useful and which detection method is legal.

<!-- stage: contributions -->
### What The Combination Needs

The array contract contributes the representation. Its value range proves that every value is a legal next index, so nested lookups are safe. Fast and slow pointer motion contributes repetition detection without a visited table. The second pointer phase contributes the location of the repeated entry rather than merely proving that repetition exists. Remove any one contribution and the solution breaks: arbitrary values cannot be followed safely, one-speed traversal cannot detect a repeat without memory, and the first meeting need not be the requested duplicate.

<!-- stage: naive -->
### Record The Visited Positions

A direct solution follows the links and marks every position it has seen. The first position reached twice is the entry of the repeated part of the walk. This is correct and useful as a test oracle.

```java
static int repeatedPosition(int[] next, int start) {
    boolean[] seen = new boolean[next.length];
    int at = start;
    while (!seen[at]) {
        seen[at] = true;
        at = next[at];
    }
    return at;
}
```

The table costs O(n) extra space. Marking signs or rearranging values can remove that table, but both approaches change the caller's array.

<!-- stage: bottleneck -->
### Constraints Remove The Obvious Tools

On a walk through one hundred thousand positions, the visited table needs one hundred thousand flags. That is still practical software, but it violates an O(1)-space interview contract. Rewalking the path from the start after every move avoids the table but repeats a growing prefix and costs O(n²). Sign marking and cyclic placement remain O(n), yet even a temporary write violates a strict no-mutation promise unless the method restores every changed cell correctly.

The missing operation is a way to compare progress through the same links without recording the entire history.

<!-- stage: insight -->
### Interpret Then Detect

Treat the bounded array as an **index-state graph**: every reachable position has exactly one outgoing edge, defined by `next = nums[current]`. A finite one-outgoing-edge walk consists of a tail followed by a cycle. The duplicate value is the cycle entry because two different positions point to that same value.

<!-- names: index-state graph, tortoise-and-hare phase, entry phase -->

The **tortoise-and-hare phase** stores two positions. One follows one edge per round and the other follows two. After both enter the cycle, their relative offset changes by one each round, so they must meet. That meeting only locates a point inside the cycle. In the **entry phase**, reset one position to the first named position and move both one edge per round. If the tail length is `mu` and the cycle length is `lambda`, the meeting offset is congruent to `-mu` modulo `lambda`; after `mu` equal moves, both positions reach the entry.

This is Floyd's cycle-entry algorithm applied to array state. It is safe only because the value domain proves every dereference is in range, and it is preferable here because it satisfies both no mutation and constant auxiliary space. If mutation is allowed, sign marking or cyclic placement can also meet O(n) time and O(1) space, but they solve a different contract.

<!-- stage: variables -->
### Positions Not Detached Values

`slow` and `fast` always hold legal array indices. During the meeting phase, `slow` follows one edge and `fast` follows two. After equality, `slow` resets to `nums[0]`; `fast` remains at the meeting position. The entry phase advances each once. The method returns their common index, which is also the duplicated value under the duplicate-array contract.

<!-- stage: trace -->
### A Tail Before The Cycle

For `[1,4,3,2,2]`, the walk from the first named position is `1 → 4 → 2 → 3 → 2`. Positions 2 and 3 form the cycle, while positions 1 and 4 form the tail. The meeting phase starts both positions at 1. After one round, slow is at 4 and fast is at 2. After the next round, both are at 2.

Meeting at 2 happens to equal the entry on this input, but the algorithm cannot assume that. It still performs the entry setup: reset `slow` to 1 and keep `fast` at 2. One equal move produces positions 4 and 3. The next produces 2 and 2, proving that 2 is the entry. The trace below was emitted by the lesson's executable trace script.

```trace
{"cells":[1,4,3,2,2],"pointers":["slow","fast"],"steps":[{"at":{"slow":1,"fast":1},"vars":{"phase":"meeting","moves":0},"note":"Both positions start at the index named by nums[0]."},{"at":{"slow":4,"fast":2},"vars":{"phase":"meeting","moves":1},"note":"Slow follows one link; fast follows two links."},{"at":{"slow":2,"fast":2},"vars":{"phase":"meeting","moves":2},"note":"Slow follows one link; fast follows two links."},{"at":{"slow":1,"fast":2},"vars":{"phase":"entry","moves":0},"note":"Reset one position to nums[0] and keep the other at the meeting point."},{"at":{"slow":4,"fast":3},"vars":{"phase":"entry","moves":1},"note":"Equal-speed movement brings both positions to the cycle entry."},{"at":{"slow":2,"fast":2},"vars":{"phase":"entry","moves":2},"note":"Equal-speed movement brings both positions to the cycle entry."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java run
public final class DuplicateWithFloyd {
    static int findDuplicate(int[] nums) {
        int slow = nums[0];
        int fast = nums[0];

        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);

        slow = nums[0];
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }
        return slow;
    }

    public static void main(String[] args) {
        int[] first = {1, 4, 3, 2, 2};
        int[] copy = first.clone();
        if (findDuplicate(first) != 2) throw new AssertionError("duplicate");
        if (!java.util.Arrays.equals(first, copy)) throw new AssertionError("mutation");
        if (findDuplicate(new int[] {2, 1, 2}) != 2) throw new AssertionError("short cycle");
    }
}
```

Each phase follows at most O(n) edges, so total time is O(n) and auxiliary space is O(1). The code has no bounds checks because the input contract already guarantees values from 1 through `n` in an array of length `n + 1`. Adding defensive checks inside this loop would obscure rather than strengthen that proof.

<!-- stage: applicability -->
### Read The Contract First

Use this combination when the values form a total next-index relation, a repeated value corresponds to the entry you need, mutation is forbidden, and extra space must remain constant. The invariant is that both variables always name reachable legal indices; after the reset, equal-speed motion preserves the distance relationship that ends at the entry.

The nearest false friend is an arbitrary array containing a duplicate. Values such as `-3` or `500000` do not define safe links, and a repeated value alone does not prove that the resulting entry answers the problem. Another false friend is a linked-list cycle problem: the pointer motion is shared, but the array's value-domain proof is separate. In Java, nested indexing performs no allocation, but an invalid domain fails with `ArrayIndexOutOfBoundsException`; do not apply this technique before checking the contract.

<!-- stage: exercises -->
### Exercises

#### [Build] Value As Next Index (Author exercise)
<!-- id: tp-index-state-path -->

**Prerequisites.** Array bounds, index access, and the value-as-link representation.

**Problem.** Given an integer array `next` and a nonnegative number of steps, first verify that every value is a legal index. Then return the sequence of visited indices, including index zero before the first move and one new index after each move. Return an empty array if any value is invalid.

**Constraints.** `1 <= next.length <= 10^5`; `0 <= steps <= 10^5`; target O(next.length + steps) time.

**Example 1.** Input `next = [2,0,3,1]`, `steps = 5`; output `[0,2,3,1,0,2]`.

**Example 2.** Input `next = [1,3]`, `steps = 2`; output `[]` because value 3 is not a legal index.

**Hint.** Separate representation validation from traversal. Once validation succeeds, each visited value can safely become the next index.

**Changed decision.** This rung proves the index-state contract before adding cycle detection.

#### [Vary] Find The Duplicate Number (LeetCode 287)
<!-- id: tp-index-state-duplicate -->

**Prerequisites.** The index-state graph, Floyd's meeting phase, and the entry phase.

**Problem.** An array of length `n + 1` contains only values from 1 through `n`, and one value occurs at least twice. Return that repeated value without modifying the array and while using O(1) auxiliary space.

**Constraints.** `1 <= n <= 10^5`; exactly one distinct value is duplicated; target O(n) time.

**Example 1.** Input `nums = [1,4,3,2,2]`; output `2`.

**Example 2.** Input `nums = [2,1,2]`; output `2`.

**Hint.** Explain why the first equality only proves that both positions are inside the cycle. Which reset turns that meeting into the cycle entry?

**Changed decision.** The repeated entry is now the requested answer, and the space and mutation limits rule out the visited table.

#### [Boundary] Duplicate Near Start (Author exercise)
<!-- id: tp-index-state-near-start -->

**Prerequisites.** Do-while initialization and both phases of Floyd's algorithm.

**Problem.** For a valid duplicate array, return `[duplicate, meetingMoves, entryMoves]`, counting one meeting move per slow-pointer advance and one entry move per equal-speed advance. This exposes immediate-entry cycles that often cause incorrect initialization.

**Constraints.** `2 <= nums.length <= 10^5`; values and duplication follow the LeetCode 287 contract.

**Example 1.** Input `nums = [2,2,1]`; output `[2,2,0]`.

**Example 2.** Input `nums = [1,1]`; output `[1,1,0]`.

**Hint.** Start both positions at `nums[0]`, but use a do-while loop so phase one follows at least one edge before testing equality.

**Changed decision.** The output makes phase lengths observable, especially when the entry phase needs zero moves.

#### [Recognize] Compare Alternatives (Author exercise)
<!-- id: tp-index-state-alternatives -->

**Prerequisites.** Floyd cycle entry, sign marking, cyclic placement, and input mutation contracts.

**Problem.** Implement `findDuplicate(nums, mayMutate)`. When `mayMutate` is false, return the duplicate without changing any array cell. When it is true, use in-place cyclic placement instead. Both branches must use O(1) auxiliary space.

**Constraints.** `2 <= nums.length <= 10^5`; values follow the LeetCode 287 contract; target O(n) time.

**Example 1.** Input `nums = [1,4,3,2,2]`, `mayMutate = false`; output `2`, and the array remains unchanged.

**Example 2.** Input `nums = [2,1,2]`, `mayMutate = true`; output `2`; array order after the call is unspecified.

**Hint.** The false branch must follow links only. In the true branch, compare the value at index zero with the value at the index it names before deciding whether to swap.

**Changed decision.** The algorithm is selected from the mutation contract rather than from the presence of duplicate values alone.
