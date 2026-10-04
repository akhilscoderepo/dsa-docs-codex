<!-- section: orientation -->
## Orientation

Two pointers is not one algorithm. It is a way to describe algorithms that keep two positions whose movement discards work or constructs a result. The reason for moving a pointer must come from an invariant: sorted order can eliminate pair candidates, a written prefix can certify compacted output, and disjoint regions can certify a partition. If no property proves a move safe, two pointers is only a guess.

This chapter assumes arrays, strings, sorting, and Java index contracts. Before each problem, decide whether the input may be reordered, whether output order matters, and whether the returned value is a pair of indices, a length, or a mutated prefix. Those details decide whether sorting is legal and whether a stable read/write scan is required.

The lessons separate opposite-end elimination, same-direction compaction, two-way and three-way partitioning, duplicate control, k-sum reduction, and Floyd cycle detection over array values. The closing combination lessons make earlier prerequisites explicit. Sliding windows, greedy proofs, and linked-list pointer mechanics remain in their owning chapters.
