<!-- lesson-kind: standard -->
<!-- lesson-id: array-cycle-state -->
## Array Cycle State

<!-- stage: context -->
### Values Become Links

An array usually stores data, but a strict value range can give each value a second meaning: the next index to visit. Starting from one index and repeatedly following `nums[index]` then traces a directed path. If every step remains inside a finite set and each position has exactly one outgoing link, the path must eventually repeat. That representation turns a duplicate-value contract into a cycle-entry question without mutating the array.

<!-- stage: naive -->
### Remember Every Visit

Follow links from the start and store visited indices in a boolean array or hash set. The first repeated index identifies the cycle. This is clear and linear, and it makes a good oracle. It also consumes O(n) memory. Sorting, sign marking, or cyclic placement can use less auxiliary space but changes input order or values.

<!-- stage: bottleneck -->
### The No-Mutation Constraint

The duplicate problem asks for O(1) extra space while preserving the array. A visited set violates the space bound, and marking or rearranging violates immutability. Rechecking earlier path positions would avoid storage but cost O(n²). We need to detect repetition and locate its entry while storing only a constant number of positions.

The answer must therefore emerge from pointer motion alone.

<!-- stage: insight -->
### Meet Then Find Entry

Advance `slow` by one link and `fast` by two. Once both enter the cycle, their relative distance changes by one per step, so they meet. This first meeting proves a cycle exists but does not generally reveal its entry. Reset one pointer to the starting position; move both one link at a time. They meet at the entry.

<!-- names: functional graph, Floyd cycle detection, cycle entry -->

The array defines a **functional graph** because every index has one outgoing edge. **Floyd cycle detection** uses the two speeds without marking nodes. The second phase finds the **cycle entry**: if the tail length is `mu`, the meeting offset makes equal-speed pointers starting at the path origin and meeting point arrive at the entry together after `mu` moves. The proof depends on a total next-link function and in-range values.

<!-- stage: variables -->
### Link State

`slow` and `fast` store indices, not array values detached from their index meaning. One phase uses `slow = nums[slow]` and `fast = nums[nums[fast]]`. The second pointer dereference is safe only because both values lie in the declared index domain. In phase two, `finder` starts at the path origin and both pointers advance once per iteration.

<!-- stage: trace -->
### Tail Into A Cycle

Use `[1,3,4,2,2]` and start from index 0. The links are `0→1→3→2→4→2`; indices 2 and 4 form a cycle, and index 2 is its entry. Slow moves to 1 while fast reaches 3. Next, slow reaches 3 and fast reaches 4. Then slow reaches 2 and fast also reaches 2, creating the phase-one meeting.

Reset a finder to index 0 while slow stays at 2. Finder moves to 1 and slow to 4; then finder reaches 3 and slow returns to 2; finally finder reaches 2 while slow reaches 4 only if initialization differs. Using the standard LC 287 start `nums[0]` for both phases gives the equal-distance alignment shown by the executable code: reset one pointer to `nums[0]`, not raw index zero.

```trace
{"cells":[1,3,4,2,2],"pointers":["slow","fast"],"steps":[{"at":{"slow":1,"fast":1},"vars":{"phase":1},"note":"Both pointers begin at the first value, which names index 1."},{"at":{"slow":3,"fast":2},"vars":{"phase":1},"note":"Slow follows one link while fast follows two."},{"at":{"slow":2,"fast":2},"vars":{"phase":1},"note":"The pointers meet inside the cycle."},{"at":{"slow":1,"fast":2},"vars":{"phase":2},"note":"Reset slow to the first value and keep fast at the meeting."},{"at":{"slow":3,"fast":4},"vars":{"phase":2},"note":"Move both pointers one link."},{"at":{"slow":2,"fast":2},"vars":{"phase":2},"note":"They meet at value 2, the duplicate and cycle entry."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java run
public final class DuplicateCycle {static int find(int[]a){int slow=a[0],fast=a[0];do{slow=a[slow];fast=a[a[fast]];}while(slow!=fast);slow=a[0];while(slow!=fast){slow=a[slow];fast=a[fast];}return slow;}public static void main(String[]z){if(find(new int[]{1,3,4,2,2})!=2||find(new int[]{3,1,3,4,2})!=3)throw new AssertionError();}}
```

Both phases are O(n), the method uses O(1) extra space, and the array remains unchanged. No bounds guard is appropriate unless the contract permits invalid link values; the stated domain already proves every dereference safe.

<!-- stage: applicability -->
### When It Applies

Use this method when values are guaranteed legal next indices, repeated following must enter a cycle, mutation is forbidden, and the desired value corresponds to the cycle entry. The invariant is that every dereference follows a valid edge in the functional graph while the two speeds preserve Floyd's meeting relationship.

The false friend is an arbitrary integer array. Without the bounded value domain, nested dereferences may fail and a duplicate need not describe a cycle. Linked-list cycle detection shares the motion but not the representation contract. Sign marking and cyclic placement are alternatives only when mutation is explicitly allowed.

<!-- stage: exercises -->
### Exercises

#### [Build] Follow Links (Author exercise)
<!-- id: tp-follow-links -->

**Prerequisites.** Array values interpreted as valid next indices.

**Problem.** Starting at index zero, follow exactly `steps` links and return the final index. Reject no input because the contract guarantees every link is in range.

**Constraints.** `1 <= next.length <= 10^5`; `0 <= next[i] < next.length`; `0 <= steps <= 10^6`.

**Example 1.** Input `next = [1,2,0]`, `steps = 4`; output `1`.

**Example 2.** Input `next = [0]`, `steps = 7`; output `0`.

**Hint.** The current array value becomes the next index; do not increment an index numerically.

**Changed decision.** This isolates the value-as-link representation before cycle logic is introduced.

#### [Vary] Find The Duplicate Number (LeetCode 287)
<!-- id: tp-find-duplicate -->

**Prerequisites.** Floyd's meeting and entry phases over an array functional graph.

**Problem.** An array of `n+1` integers contains values from 1 through `n`, with exactly one value repeated. Return that duplicate without modifying the input and with constant auxiliary space.

**Constraints.** `1 <= n <= 10^5`; one value may appear more than twice; all others appear once.

**Example 1.** Input `nums = [1,3,4,2,2]`; output `2`.

**Example 2.** Input `nums = [3,1,3,4,2]`; output `3`.

**Hint.** Treat each value as the next index and identify why the repeated value has two incoming links.

**Changed decision.** The cycle entry now directly represents the requested duplicate value.

#### [Boundary] Immediate Cycle (Author exercise)
<!-- id: tp-immediate-array-cycle -->

**Prerequisites.** Do-while meeting loops and smallest legal domains.

**Problem.** Run Floyd's algorithm on the smallest legal duplicate array and return the entry, while documenting every dereference made by both phases.

**Constraints.** `nums.length == 2`; both values equal 1.

**Example 1.** Input `nums = [1,1]`; output `1`.

**Example 2.** Input `nums = [1,1]` with a copied array; output `1` and the copy remains unchanged.

**Hint.** A do-while loop performs one movement before testing the meeting, which handles an immediate self-cycle.

**Changed decision.** The tail is minimal and the cycle length is one, exposing initialization errors.

#### [Recognize] Duplicate Entry Proof (Author exercise)
<!-- id: tp-duplicate-entry-proof -->

**Prerequisites.** Tail length, cycle length, and phase-two pointer alignment.

**Problem.** Given a valid duplicate array and its phase-one meeting index, return the cycle entry and a count of phase-two moves. Explain why the meeting is the entry rather than an arbitrary cycle position.

**Constraints.** `2 <= nums.length <= 10^5`; values satisfy the LC 287 domain and duplicate guarantee.

**Example 1.** Input `nums = [1,3,4,2,2]`, meeting `2`; output entry `2` and moves `2`.

**Example 2.** Input `nums = [1,1]`, meeting `1`; output entry `1` and moves `0`.

**Hint.** Reset one pointer to `nums[0]`, then count equal-speed moves until equality.

**Changed decision.** The output exposes phase-two distance and requires the entry proof explicitly.
