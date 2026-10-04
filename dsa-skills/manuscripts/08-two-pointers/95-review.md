<!-- section: review -->
## Review

Use these questions to identify the proof behind a pointer move. A pointer is not justified because the loop looks familiar; the current contract and invariant must show which candidates, values, or regions become final.

### Recognition Questions

```quiz
{"id":"tp-rev-unsorted-pair","q":"An unsorted array must yield two values whose sum equals a target, and the input may not be reordered. Can opposite-end movement discard one side after comparing the current sum?","options":["Yes, move the side with the smaller absolute value.","Yes, always move the left side first.","No, without a monotone property the comparison does not rule out the skipped pairs.","No, two-pointer methods require distinct values."],"answer":2,"explain":"The elimination proof comes from order or another monotone relation. On arbitrary unsorted input, either endpoint may still pair with an interior value."}
```

```quiz
{"id":"tp-rev-read-write","q":"During stable in-place filtering, what does the write pointer represent?","options":["The last input value inspected.","The first unresolved output position after a prefix that already satisfies the final contract.","The left boundary of a range whose aggregate is maintained.","The number of rejected values only."],"answer":1,"explain":"The read pointer inspects input, while the write pointer marks where the next admitted value belongs. The prefix before write is already final."}
```

```quiz
{"id":"tp-rev-partition-stability","q":"A method may swap values freely and needs all values below a pivot before all other values. Which guarantee should it avoid making?","options":["Linear running time.","Constant auxiliary space.","Preservation of the original relative order inside each region.","A boundary separating the two categories."],"answer":2,"explain":"A two-way swap partition establishes category regions, not stable order. Requiring stability changes the contract and usually the implementation."}
```

```quiz
{"id":"tp-rev-dnf-high-swap","q":"In a Dutch-national-flag scan, mid is swapped with high because the current value belongs in the high region. Why must mid stay in place for the next iteration?","options":["The incoming value from high has not been classified.","The low region must shrink first.","Advancing mid would make the algorithm quadratic.","Java swaps are lazy."],"answer":0,"explain":"Only the value moved to the high region is final. The value arriving at mid came from the unresolved region and still needs classification."}
```

```quiz
{"id":"tp-rev-duplicate-timing","q":"A sorted pair scan has just recorded one valid value pair. When should it skip repeated endpoint values?","options":["Before evaluating the first representative.","After consuming the representative pair and moving both endpoints.","Only after the complete outer loop ends.","Never; a set must remove duplicates later."],"answer":1,"explain":"Evaluating one representative preserves the valid combination. Skipping its equal successors afterward prevents the same value pair from being emitted again."}
```

```quiz
{"id":"tp-rev-ksum-overflow","q":"Why should a Java 4Sum implementation promote operands to long before adding them?","options":["A long comparison sorts faster.","Several valid int values can overflow an int total and reverse the pointer decision.","Java arrays cannot contain four int values.","Duplicate skipping requires boxed Long objects."],"answer":1,"explain":"Pointer movement depends on the sign of the comparison with the target. Overflow can corrupt that sign even though every individual input fits in int."}
```

```quiz
{"id":"tp-rev-container-move","q":"For the container-area problem, why is moving the shorter wall safe?","options":["The taller wall can never be part of an answer.","Any narrower container that keeps the shorter wall cannot gain height beyond that limiting wall.","The shorter wall always has the smaller index.","Moving either wall is equally safe on every input."],"answer":1,"explain":"Width decreases after either move. Keeping the limiting height cannot improve area, so only replacing the shorter wall can possibly compensate for the lost width."}
```

```quiz
{"id":"tp-rev-floyd-domain","q":"An array contains one repeated integer but may also contain negative values and values larger than its last index. Why is Floyd's array-cycle method not justified?","options":["Floyd's method works only on sorted arrays.","The values do not define a total, safe next-index relation.","Negative numbers create more than one duplicate.","The method requires O(n) extra memory for bounds checks."],"answer":1,"explain":"The representation is part of the proof. If a stored value is not a legal next index, following nums[nums[i]] is unsafe and the functional-graph model does not hold."}
```

```quiz
{"id":"tp-rev-palindrome-branch","q":"At the first mismatch in the one-deletion palindrome problem, what must be tested?","options":["Delete both mismatched characters.","Try the two remaining ranges formed by skipping exactly the left endpoint or exactly the right endpoint.","Sort the remaining characters.","Continue inward without changing either endpoint."],"answer":1,"explain":"Before the mismatch, the outer characters already agree. A valid single deletion must remove one of the two characters at the first unresolved mismatch."}
```

### Rebuild From The Invariant

Close the solutions and rewrite three techniques. First, implement a sorted pair search and state exactly which pairs become impossible after a sum is too small or too large. Second, implement Dutch-national-flag partitioning while naming all four regions and explaining why a value swapped in from `high` must be inspected. Third, implement Floyd's meeting and entry phases for the duplicate-number contract, including the value-domain argument that makes every nested lookup safe.

For a fresh problem, an integer array is sorted in nondecreasing order. Return every distinct pair of values whose absolute difference equals `k`, where `k` is nonnegative. Duplicate occurrences must not produce duplicate value pairs, and the caller's array must remain unchanged. For example, `values = [1,1,3,3,5,8]` and `k = 2` returns `[[1,3],[3,5]]`; `values = [4,4,4]` and `k = 0` returns `[[4,4]]`. Assume at most 100,000 values. Before writing code, define what each pointer means, decide which side moves for each comparison, and explain when equal values may be skipped without losing the `k = 0` case. Then give the O(n) time and output-space bounds.
