<!-- section: orientation -->
## Orientation

This chapter is about preserving cumulative state so that later work does not rescan earlier values. You already know arrays, matrices, maps, and the difference between an index and a boundary. We will use those tools in three different ways: preprocess fixed data for fast queries, remember earlier prefix states while scanning, and record range updates as boundary changes before materializing the result.

The central convention is a sentinel prefix. For an array of length `n`, `prefix[i]` describes the first `i` values, so `prefix[0]` describes the empty prefix and `prefix[n]` describes the whole array. This boundary-based definition removes special cases at index zero. It also explains why a range from `left` through `right` is recovered from boundaries `left` and `right + 1`.

Read the contracts carefully. Some lessons count ranges, some ask for the longest range, and others answer immutable queries or batch updates. Those outputs require different map values and different invariants even when their loops look similar. Use `long` whenever the largest possible cumulative total exceeds the `int` range. None of the examples silently changes an input unless the problem explicitly permits it.

