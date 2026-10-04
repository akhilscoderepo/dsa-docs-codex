<!-- lesson-kind: standard -->
<!-- lesson-id: peak-search -->
## Peak Search

<!-- stage: context -->
### Find The Summit

A hiking profile records the elevation at evenly spaced points along a trail. The profile rises to a summit and then falls. You need the summit's index, but reading an elevation may be expensive because the data comes from a remote sensor. Scanning every point works, yet it ignores the shape promised by the input.

The more general version is less tidy: the profile may rise and fall several times, and any position higher than its immediate neighbors is acceptable. The question is whether one comparison between adjacent positions can prove that an entire part of the profile need not be inspected.

<!-- stage: naive -->
### Inspect Every Position

The direct method walks through the array and returns the largest value's index. For a guaranteed mountain, that position is the unique summit. It is correct, and it also works for strictly increasing or decreasing input when an endpoint is allowed to be the answer.

```java
static int peakLinear(int[] nums) {
    int best = 0;
    for (int i = 1; i < nums.length; i++) {
        if (nums[i] > nums[best]) best = i;
    }
    return best;
}
```

<!-- stage: bottleneck -->
### A Million Unneeded Reads

Suppose a mountain contains one million elevations and its summit is near the beginning. The scan still reads every remaining value even after the trail has begun its guaranteed descent. It performs O(n) comparisons and O(n) array reads. With a remote array such as the interface in the final exercise, those reads are not merely CPU instructions; each may be a metered method call.

The scan also learns more than the problem requests. It establishes which value is globally largest by comparing it with every later value. The contract only asks for a position that is higher than its neighbors, so a local direction should be enough to decide where to continue.

<!-- stage: insight -->
### Follow The Rising Side

Compare `nums[mid]` with the value immediately to its right. This comparison reveals the **local slope** at the midpoint. If `nums[mid] < nums[mid + 1]`, the profile is rising there. Continuing right from that edge must eventually reach an acceptable high point: either the rise ends inside the interval or the right endpoint itself is a high point under the virtual-boundary contract. Therefore `mid` cannot be the answer, and the remaining interval begins at `mid + 1`.

If `nums[mid] > nums[mid + 1]`, the edge falls. The midpoint may already be the high point, so it must remain. A high point also exists somewhere at or to the left of it. We keep `[lo, mid]` by assigning `hi = mid`.

<!-- names: local slope, peak search, peak-preserving invariant -->

This method is **peak search**. Its **peak-preserving invariant** says that the closed interval `[lo, hi]` contains at least one valid high point. Each comparison discards a side only after the direction of the edge proves that another high point survives on the kept side. The interval shrinks because the rising case removes `mid`, while the falling case removes everything strictly after it. Adjacent values must be unequal for this proof; equality supplies no direction unless the problem gives an additional rule.

<!-- stage: variables -->
### One Closed Interval

`lo` and `hi` are inclusive endpoints of an interval known to contain an answer. `mid` is chosen strictly before `hi` whenever the loop runs, so `mid + 1` is a valid index. The comparison needs no target and stores no candidate. When `lo == hi`, the invariant makes that single remaining index the answer.

<!-- stage: trace -->
### Keep The Possible Summit

Use the mountain `[1, 4, 8, 11, 7, 3]`. The search starts at `[0, 5]` and chooses midpoint 2. Elevation 8 is lower than 11 at index 3, so the edge rises. Index 2 cannot be the summit, and a summit survives to its right; `lo` becomes 3.

The interval is now `[3, 5]`. Midpoint 4 holds 7, which is higher than 3 at index 5. The edge falls, so index 4 might be a summit only if the unseen left side permits it. We therefore keep the midpoint and move `hi` to 4 rather than to 3.

The final comparison uses midpoint 3. Elevation 11 is above 7, so the falling case again keeps the midpoint by setting `hi = 3`. Both endpoints now name index 3. The important move is `hi = mid`: replacing it with `mid - 1` could discard the summit that the comparison has just shown to be possible.

```trace
{"cells":[1,4,8,11,7,3],"pointers":["lo","mid","hi"],"steps":[{"at":{"lo":0,"mid":2,"hi":5},"vars":{"rising":true},"note":"The rising edge keeps a peak to the right."},{"at":{"lo":3,"mid":4,"hi":5},"vars":{"rising":false},"note":"The flat-or-falling edge keeps mid and the left side."},{"at":{"lo":3,"mid":3,"hi":4},"vars":{"rising":false},"note":"The flat-or-falling edge keeps mid and the left side."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java
static int findPeak(int[] nums) {
    int lo = 0, hi = nums.length - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (nums[mid] < nums[mid + 1]) {
            lo = mid + 1;
        } else {
            hi = mid; // mid may itself be the peak
        }
    }
    return lo;
}
```

The loop condition guarantees that `mid < hi`, which makes `mid + 1` safe without a separate bounds check. Both updates preserve a nonempty closed interval and remove at least one index. The method takes O(log n) time and O(1) extra space. For a mountain array, it returns the unique summit. For the broader contract with unequal adjacent values and virtual negative-infinity neighbors, it returns one valid peak, not necessarily the largest value.

<!-- stage: applicability -->
### When Direction Is Enough

Use peak search when adjacent direction proves that at least one acceptable high point remains on a chosen side. State the invariant aloud: `[lo, hi]` always contains a peak, and `mid + 1` is read only while `mid < hi`. The recognition cue is a request for any local maximum or for the turning point of a rise-then-fall sequence.

The false friend is exact target search. There is no target comparison here, and finding a value equal to something does not end the method. Another false friend is an arbitrary array that permits equal neighbors without defining how plateaus count; equality then breaks the directional proof and the method can silently choose an invalid position. In Java, remote-array interfaces make call counts important, so cache `get(mid)` and `get(mid + 1)` if the API charges for repeated reads.

<!-- stage: exercises -->
### Exercises

#### [Build] Peak Index In A Mountain Array (LeetCode 852)
<!-- id: bs-peak-index-mountain -->

**Prerequisites.** Closed-interval binary search and the slope invariant from this lesson.

**Problem.** Given an integer array that strictly increases to one interior index and then strictly decreases, return the index of that unique peak.

**Constraints.** `3 <= arr.length <= 10^5`; `0 <= arr[i] <= 10^6`; the mountain guarantee holds; require O(log n) time and O(1) space.

**Example 1.** Input `arr = [0,3,7,12,9,2]`; output `3`, where value 12 is the turning point.

**Example 2.** Input `arr = [2,10,6]`; output `1`, the only possible interior peak.

**Hint.** Compare the midpoint with its right neighbor, not with a target. On which side must the unique turning point lie when that edge rises?

**Changed decision.** This first rung uses a strict rise-then-fall contract, so the surviving peak is unique.

#### [Vary] Find Any Peak Element (LeetCode 162)
<!-- id: bs-find-any-peak -->

**Prerequisites.** The mountain search above and the virtual-boundary definition of an endpoint peak.

**Problem.** Given a nonempty integer array whose adjacent values are unequal, return any index whose value is greater than its immediate neighbors. Treat positions outside the array as having negative infinity.

**Constraints.** `1 <= nums.length <= 1000`; values fit in `int`; `nums[i] != nums[i + 1]`; require O(log n) time.

**Example 1.** Input `nums = [2,7,4,1,8,5]`; output `1` is valid because 7 exceeds both neighbors.

**Example 2.** Input `nums = [9]`; output `0`, because both virtual neighbors are lower.

**Hint.** The array may contain several peaks, so do not try to preserve a particular one. Why does a rising edge still guarantee that some acceptable peak exists to its right?

**Changed decision.** The input may rise and fall repeatedly, and the method may return any peak rather than one unique summit.

#### [Boundary] Endpoint Peak (Author exercise)
<!-- id: bs-endpoint-peak -->

**Prerequisites.** Find-any-peak semantics and inclusive interval updates.

**Problem.** Implement peak search for a strictly monotone nonempty array. Return the last index when the values strictly increase and index zero when they strictly decrease, without adding special endpoint branches.

**Constraints.** `1 <= nums.length <= 10^5`; all adjacent values differ; input is strictly increasing or strictly decreasing; target O(log n) time and O(1) space.

**Example 1.** Input `nums = [1,3,6,10]`; output `3`, the right endpoint.

**Example 2.** Input `nums = [10,6,3,1]`; output `0`, the left endpoint.

**Hint.** Trace the same two updates used for an interior peak. Which endpoint survives if every tested edge rises, and which survives if every edge falls?

**Changed decision.** The answer is forced onto an endpoint, exposing off-by-one errors in both interval updates.

#### [Recognize] Find In Mountain Array (LeetCode 1095)
<!-- id: bs-find-in-mountain-array -->

**Prerequisites.** Peak search from this lesson, exact binary search, descending-order search, and API-call accounting.

**Problem.** A read-only `MountainArray` exposes `get(index)` and `length()`. Return the smallest index whose value equals `target`, or `-1` if absent. Minimize calls to `get` by first locating the peak and then searching the increasing and decreasing sides.

**Constraints.** `3 <= length <= 10^4`; values and `target` are between 0 and `10^9`; the array is a strict mountain; stay within the interface's 100-call limit.

**Example 1.** Input `mountain = [1,5,9,12,8,6,2]`, `target = 6`; output `5`.

**Example 2.** Input `mountain = [0,4,11,9,3]`, `target = 7`; output `-1` because neither ordered side contains it.

**Hint.** After finding the turning point, what order does each side have? Search the increasing side first so that a value occurring on both slopes returns its smaller index.

**Changed decision.** Peak discovery becomes the first phase of a three-search algorithm, and interface calls are now a constrained resource.
