<!-- section: review -->
## Review

Use these questions after finishing the chapter and again after a few days. Each prompt asks which fact sorting makes local, what state the scan must retain, or which Java contract owns a tie.

### Recognition Questions

```quiz
{"id":"sort-rev-contract","q":"A comparator orders signed integer priorities by returning a.priority() - b.priority(). Which defect matters most?","options":["The comparator allocates too much memory.","Subtraction can overflow and reverse the required sign.","Comparators cannot read record fields.","Ascending order is illegal for priorities."],"answer":1,"explain":"Comparator results are interpreted by sign. Integer subtraction can overflow, so Integer.compare must express the relation safely."}
```

```quiz
{"id":"sort-rev-stability","q":"Equal-severity alerts must retain arrival order. The program uses stable List.sort. What should the comparator do when severities match?","options":["Compare alert identifiers.","Return zero so stability preserves arrival order.","Return one for both directions.","Shuffle the tied alerts."],"answer":1,"explain":"Arrival order owns the tie. Adding another key would replace that rule rather than preserve it."}
```

```quiz
{"id":"sort-rev-primitive","q":"Why can Arrays.sort(int[]) not use a Comparator<Integer>?","options":["Primitive-array sorting is always descending.","The comparator overload applies to object arrays, while int[] stores primitives.","Integer.compare works only on lists.","A comparator requires a hash map."],"answer":1,"explain":"Java's primitive overload has natural order only. Custom comparison requires objects or a different representation."}
```

```quiz
{"id":"sort-rev-sweep","q":"After sorting requests, each value must be raised to become unique. What prefix state is sufficient for the next request?","options":["A set containing the original input.","The last finalized assigned value.","The original index of every request.","The average assigned value."],"answer":1,"explain":"The next value must be at least its request and one beyond the last assignment; earlier assignments impose no additional constraint."}
```

```quiz
{"id":"sort-rev-runs","q":"An unsorted array must produce one copy of each value. When is comparing only with the previous value valid?","options":["Always.","After sorting has made equal values contiguous.","Only when every value is positive.","After reversing the array."],"answer":1,"explain":"Neighbor comparison represents global duplication only after equal values have been brought into one run."}
```

```quiz
{"id":"sort-rev-fallback","q":"A task asks for the kth distinct maximum and returns the maximum when fewer than k distinct values exist. What should represent the missing rank?","options":["Integer.MIN_VALUE.","A stored maximum plus an explicit end-of-scan branch.","Array index -1 returned directly.","Comparator zero."],"answer":1,"explain":"Every integer may be valid data. The scan should model the fallback contract without a numeric sentinel."}
```

```quiz
{"id":"sort-rev-signature","q":"Why does a sorted character sequence work as an anagram-group key?","options":["It keeps the original positions.","It removes permutation order while preserving each character and its multiplicity.","It stores only the set of characters.","It makes every string the same length."],"answer":1,"explain":"The transformation discards exactly the irrelevant difference and retains the complete multiset."}
```

```quiz
{"id":"sort-rev-false-binary","q":"An array has been sorted. Is binary search automatically the right next step?","options":["Yes, every sorted problem is logarithmic.","No, binary search also needs a monotone query predicate; many tasks require a linear scan.","No, Java forbids binary search after Arrays.sort.","Yes, unless duplicates exist."],"answer":1,"explain":"Sorting can expose adjacency or a sweep frontier without creating a monotone yes/no question."}
```
