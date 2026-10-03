<!-- section: orientation -->
## Orientation

Sorting is useful because it changes which facts are local. Once values follow a deliberate order, duplicates form runs, interval starts can be processed from left to right, and a scan can compare the current item with a small frontier instead of searching the entire input. The sort is therefore usually a preprocessing step. The real question is what decision becomes safe after the order is established.

This chapter separates that idea into nine lessons. We begin by writing the ordering contract itself, then examine Java's primitive-array API, comparator rules, object ordering, stability and tie ownership. The final independent lessons use sorted order to support sweeps, deduplication, and adjacent scans. A released combination lesson then joins strings, maps, and sorting through canonical signatures.

You should already be comfortable with arrays, strings, maps, sets, mutation contracts, and asymptotic complexity. Two later families remain deliberately outside this chapter. Two-pointer movement belongs to Chapter 08, and interval endpoint semantics belong to Chapter 10. Their problems may sort first, but sorting alone does not supply their invariants.

