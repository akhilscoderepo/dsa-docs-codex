<!-- section: orientation -->
## Orientation

Binary search is not one algorithm with different variable names. It is a family of searches that discard part of an ordered space after proving that the answer cannot be there. This chapter starts with exact lookup, then separates occurrence boundaries, insertion bounds, and first-true predicates. It continues with local-slope searches, rotated arrays, integer answer spaces, and real-valued bisection. The final lessons combine the search invariant with hash-map histories and matrix index mapping.

You should already be comfortable with arrays, matrices, strings, hash maps, loops, and asymptotic analysis. Every exercise states whether its input is sorted, whether duplicates are possible, and what must be returned when no answer exists. Unless a prompt says otherwise, methods do not mutate their inputs.

For integer searches we use an inclusive interval `[lo, hi]` or a half-open interval `[lo, hi)`, and name the choice before writing the loop. The midpoint is computed as `lo + (hi - lo) / 2` so that adding the endpoints cannot overflow. The loop is correct only when every branch shrinks the interval and preserves the stated invariant.

Keep three questions beside you: What remains possible? What did this comparison prove impossible? What does the loop return when the interval becomes empty? If those answers are precise, the code is usually short. If they are vague, memorizing another template will not help.
