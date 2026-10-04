<!-- lesson-kind: standard -->
<!-- lesson-id: exclusion-state -->
## Exclusion State

<!-- stage: context -->
### Every Position Is Missing

A scoring pipeline assigns each participant the combined contribution of everyone except that participant. The output has one value per input position, and each answer excludes a different cell. Recomputing from scratch is easy, but almost all of the work overlaps. The real task is to bring information from the entire left side and the entire right side to every position without rescanning either side.

<!-- stage: naive -->
### Skip One Cell

For each output position, scan the array and skip that index. This directly follows the contract and is correct. It also works for zeros because it never divides, and its loop exposes exactly which value is excluded.

```java run
public final class ExclusionNaive {
    static long[] sums(int[] a){long[] r=new long[a.length];for(int i=0;i<a.length;i++)for(int j=0;j<a.length;j++)if(i!=j)r[i]+=a[j];return r;}
    public static void main(String[] z){if(!java.util.Arrays.equals(sums(new int[]{2,3,4}),new long[]{7,6,5}))throw new AssertionError();}
}
```

<!-- stage: bottleneck -->
### Almost Identical Rescans

With four values, each answer reads three cells, and adjacent answers differ only in which value was skipped. At 100,000 values, the double loop approaches ten billion visits and costs O(n^2) time. The scan repeatedly rebuilds two useful aggregates: everything strictly before `i`, and everything strictly after `i`. Neither aggregate is preserved for the next output position.

<!-- stage: insight -->
### Meet From Both Directions

Store the aggregate strictly to the left of each index during a forward pass. Then walk backward with a rolling aggregate of values strictly to the right. At position `i`, combine those two pieces; only afterward extend the right state with `nums[i]`. This is **prefix-suffix exclusion state**. For multiplication, the forward output begins with multiplicative identity `1`, and the rolling suffix also begins at `1`.

<!-- names: prefix-suffix exclusion state, rolling suffix -->

The order of mutation carries the proof. Before the backward assignment, output `i` contains the product of `nums[0..i-1]`, while the rolling suffix contains the product of `nums[i+1..n-1]`. Their product excludes exactly `nums[i]`. Updating the suffix after writing the answer preserves that claim for the next smaller index. No division is required, so zeros are ordinary factors rather than special cases. The safe move depends on associativity and an identity element, not on addition specifically.

<!-- stage: variables -->
### Left Then Right

`answer[i]` first stores the aggregate over indices strictly less than `i`. During the backward pass, `right` stores the aggregate over indices strictly greater than the current `i`. Both sides exclude the current cell. The output array doubles as prefix storage, while the suffix needs only one scalar.

<!-- stage: trace -->
### Products Around A Zero

Take `[2, 0, 4]`. The forward pass writes left products `[1, 2, 0]`: before index zero there are no factors, before index one there is `2`, and before index two the accumulated product has reached zero.

Start backward with `right = 1`. At index two, combine left `0` with right `1`, producing `0`, then absorb `4`. At index one, left is `2` and right is `4`, so the answer is `8`; only then does the suffix absorb the zero. At index zero, the right product is now zero, so the answer is zero. No branch counted zeros, yet `[0, 8, 0]` is correct.

```trace
{"cells":[2,0,4],"pointers":["i"],"steps":[{"at":{"i":2},"vars":{"left":0,"right":1,"answer":0},"note":"Combine factors around index 2, then absorb 4 into right."},{"at":{"i":1},"vars":{"left":2,"right":4,"answer":8},"note":"Both sides exclude the zero at index 1."},{"at":{"i":0},"vars":{"left":1,"right":0,"answer":0},"note":"The suffix now includes the zero, so the first answer is zero."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java run
public final class ExclusionBlueprint {
    static long[] products(int[] a){long[] r=new long[a.length];long left=1;for(int i=0;i<a.length;i++){r[i]=left;left*=a[i];}long right=1;for(int i=a.length-1;i>=0;i--){r[i]*=right;right*=a[i];}return r;}
    public static void main(String[] z){if(!java.util.Arrays.equals(products(new int[]{2,0,4}),new long[]{0,8,0}))throw new AssertionError();}
}
```

Two linear passes cost O(n) time. Beyond the returned array, the method uses O(1) space. `long` delays overflow but does not make arbitrary products safe; the contract must bound results. Empty input returns an empty output, and a one-value input returns `[1]`, the product of no remaining factors.

<!-- stage: applicability -->
### When It Applies

Use exclusion state when every output needs an associative aggregate of all values except itself. The invariant is that, before combining at `i`, the stored left state covers indices below `i` and the rolling suffix covers indices above it.

The false friend is total divided by the current value. Division fails at zero and may be forbidden or lossy. For additive sums, total-minus-current is simpler because addition has a direct inverse; two directional passes become valuable for products, maxima, or other aggregates. Java multiplication can overflow silently, and `int` operands overflow before assignment unless at least one operand is already `long`.

<!-- stage: exercises -->
### Exercises

#### [Build] Sum Except Self (Author exercise)
<!-- id: ps-sum-except-self -->

**Prerequisites.** Whole-array totals and long arithmetic.

**Problem.** Given an integer array, return a `long[]` where output `i` is the sum of every input value except `nums[i]`.

**Constraints.** `0 <= nums.length <= 10^5`; totals fit in `long`; target O(n) time.

**Example 1.** Input `nums = [4,-1,2]`, output `[1,6,3]`.

**Example 2.** Input `nums = [9]`, output `[0]`; the empty additive aggregate is zero.

**Hint.** Addition has an inverse. Can one whole-array total answer each position without storing two arrays?

**Changed decision.** This additive warm-up uses total-minus-current before multiplication removes that shortcut.

#### [Vary] Product of Array Except Self (LeetCode 238)
<!-- id: ps-product-except-self -->

**Prerequisites.** Forward prefix state and the rolling suffix invariant.

**Problem.** Return an array where output `i` equals the product of every input value except `nums[i]`, without division and in linear time.

**Constraints.** `2 <= nums.length <= 10^5`; every prefix, suffix, and answer fits in signed 32-bit range.

**Example 1.** Input `nums = [2,3,5]`, output `[15,10,6]`.

**Example 2.** Input `nums = [-2,4]`, output `[4,-2]`.

**Hint.** Store one direction in the output. Which single scalar can carry the other direction while walking backward?

**Changed decision.** Multiplication has no safe division shortcut, so two directional states must meet at each index.

#### [Boundary] Product With Zeros (LeetCode 238)
<!-- id: ps-product-with-zeros -->

**Prerequisites.** The no-division product method from the previous exercise.

**Problem.** Apply product-except-self to inputs containing one or several zeros, without adding a branch that counts zeros.

**Constraints.** `2 <= nums.length <= 10^5`; valid products fit in `int`; use O(1) extra space excluding output.

**Example 1.** Input `nums = [3,0,2]`, output `[0,6,0]`.

**Example 2.** Input `nums = [0,5,0]`, output `[0,0,0]`.

**Hint.** Trace what the ordinary left and right products contain when they cross a zero. Does the invariant require zero to be special?

**Changed decision.** Hostile zero inputs test whether the solution truly avoided division rather than disguising it.

#### [Recognize] Prefix And Suffix Maximums (Author exercise)
<!-- id: ps-prefix-suffix-maximums -->

**Prerequisites.** Strict-left and strict-right boundary state.

**Problem.** For each index, return the greatest value strictly to its left and strictly to its right as two arrays; use `Long.MIN_VALUE` when a side is empty.

**Constraints.** `1 <= nums.length <= 10^5`; target O(n) time.

**Example 1.** Input `nums = [3,1,5]`, output `left = [MIN,3,3]`, `right = [5,5,MIN]`.

**Example 2.** Input `nums = [7]`, output `left = [MIN]`, `right = [MIN]`.

**Hint.** Write the current rolling maximum before absorbing the current value. Repeat from the opposite direction.

**Changed decision.** The aggregate becomes maximum and both directional states are returned separately rather than multiplied.

