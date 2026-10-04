<!-- section: unlocked-combinations -->
## Unlocked Combinations

Two-pointer movement now combines with sorting, strings, and array-valued index state because each prerequisite has been taught. Every released combination has a separate lesson and practice staircase. The point of those lessons is not merely to place two familiar techniques in the same method; each one establishes a movement rule that neither prerequisite supplies alone.

### Teach Now

Sorting with two pointers is released in Lesson 91. Sorting creates a monotone relation between pointer movement and the remaining sum. The pointers then discard a complete class of impossible pairs after one comparison. The lesson grows from sorted pair search to fixed-value reduction, closest-sum tracking, and 4Sum with duplicate control and `long` arithmetic.

Strings with two pointers is released in Lesson 92. String indexing and normalization determine which characters participate, while the pointers express either symmetry or ordered consumption. Its staircase separates opposite-end palindrome checks, in-place reversal, one-deletion branching, and same-direction subsequence matching so that “two pointers” does not hide four different movement decisions.

Index state with Floyd's algorithm is released in Lesson 93. The array's bounded values prove that each value is a legal next index. Floyd's meeting and entry phases then find the repeated entry without changing the array or storing visited positions. The lesson contrasts that contract with cyclic placement and sign marking, which are valid only when mutation is allowed.

### Already Covered

Arrays with same-direction read/write pointers is fully covered in Lesson 02. The written-prefix invariant supplies stable compaction, so it does not need another combination lesson. Sorting also appears inside duplicate skipping and k-sum reduction, but Lessons 05, 06, and 91 already provide their distinct invariants and staircases rather than leaving sorting as an implicit prerequisite.

### Deferred

Two pointers with sliding windows waits for Chapter 09. A window needs maintained range state and a proof about when the left boundary may remove it; the read/write pointer taught here constructs output instead. Two pointers with interval sweeps waits for Chapter 10, where endpoint semantics and overlap ownership become explicit. Greedy pointer movement remains deferred until the greedy chapter proves that a locally chosen endpoint cannot damage the global answer. Linked-list fast/slow techniques stay with linked lists because node references, termination, and cycle contracts differ from the array value-as-index representation. No exercise in this chapter assumes those unreleased invariants.
