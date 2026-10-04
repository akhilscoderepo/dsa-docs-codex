<!-- lesson-kind: standard -->
<!-- lesson-id: two-dimensional-difference -->
## Two-Dimensional Difference

<!-- stage: context -->
### Many Rectangle Adjustments

A simulation stores one value for every cell in a rectangular region. Before anyone reads the result, a long list of adjustments arrives. Each adjustment adds a signed weight to every cell inside an axis-aligned rectangle. Rectangles overlap, some touch the matrix boundary, and a later adjustment may subtract an earlier one. Updating every covered cell is easy to understand, but large rectangles make that work repeat across the same cells. We need to record each rectangle cheaply and build the final matrix only once.

<!-- stage: naive -->
### Visit Every Covered Cell

The direct method handles one update by looping through its inclusive row and column boundaries. It is correct because it adds the requested weight to every covered cell exactly once.

```java run
public final class RectangleUpdatesNaive {
    static long[][] apply(int rows, int cols, int[][] updates) {
        long[][] answer = new long[rows][cols];
        for (int[] u : updates) {
            for (int r = u[0]; r <= u[2]; r++) {
                for (int c = u[1]; c <= u[3]; c++) answer[r][c] += u[4];
            }
        }
        return answer;
    }
    public static void main(String[] args) {
        long[][] result = apply(2, 3, new int[][] {{0,1,1,2,5}});
        if (result[0][0] != 0 || result[1][2] != 5) throw new AssertionError();
    }
}
```

<!-- stage: bottleneck -->
### Large Rectangles Repeat Writes

Suppose a 2,000 by 2,000 grid receives 100,000 updates, and most rectangles cover half of the cells. One update performs about two million writes. The next rectangle may differ by one row yet rewrite almost the same area. An update of height `h` and width `w` costs O(hw), so the workload can approach O(urc) for `u` updates on `r` rows and `c` columns. Only the final matrix is requested, which means those intermediate cell values are work we never needed to materialize.

<!-- stage: insight -->
### Record Where Effects Change

A one-dimensional difference array records where a range effect starts and where it stops. Extend that idea across both axes with a **two-dimensional difference array**. For an inclusive rectangle from `(row1,col1)` through `(row2,col2)`, add the weight at its top-left corner. Subtract the weight immediately to the right and immediately below. Those two cancellations overlap in the lower-right exterior region, so add the weight back at the diagonal corner.

<!-- names: two-dimensional difference array, corner deltas, sentinel border -->

These four **corner deltas** are written at `(row1,col1)`, `(row1,col2+1)`, `(row2+1,col1)`, and `(row2+1,col2+1)`, with signs `+`, `-`, `-`, and `+`. A two-dimensional prefix reconstruction then spreads each start until it meets the matching cancellations. Allocate an extra bottom row and right column as a **sentinel border**. Updates that reach the final real row or column can write their cancellation one step beyond the matrix without a branch.

The four signs are inclusion-exclusion applied to changes rather than queries. After reconstruction, a cell inside the rectangle includes the positive start and neither cancellation. A cell beyond one edge includes one cancellation and returns to zero. A cell beyond both edges includes both negative corners, so the positive diagonal corner corrects the double cancellation. The move is safe because prefix reconstruction gives every real cell a net coefficient of one inside the rectangle and zero outside it.

<!-- stage: variables -->
### Corners And Boundaries

`rows` and `cols` describe the real output. `diff` has dimensions `(rows + 1) x (cols + 1)`. Each update uses inclusive corners `row1`, `col1`, `row2`, and `col2`, plus a signed `weight`. During reconstruction, `above`, `left`, and `overlap` are already reconstructed states. Only indices below `rows` and left of `cols` are copied into the answer.

<!-- stage: trace -->
### Four Marks Become A Rectangle

Start with a 3 by 4 zero matrix and add 5 to rows 0 through 1 and columns 1 through 2. The start marker `+5` goes at `(0,1)`. The right cancellation `-5` goes at `(0,3)`, and the lower cancellation `-5` goes at `(2,1)`. Cell `(2,3)` receives `+5` because the two cancellation regions overlap there.

Reconstruction proceeds from top to bottom and left to right. Cell `(0,1)` becomes 5, and that value spreads to `(0,2)`. At `(0,3)`, the stored `-5` cancels the value coming from the left. On the next row, the value arrives from above and fills columns 1 and 2. At row 2, the lower cancellation removes it. The diagonal `+5` matters at `(2,3)`: without it, combining the upper and left states would subtract the rectangle's effect twice. The final real matrix is `[[0,5,5,0],[0,5,5,0],[0,0,0,0]]`.

```trace
{"cells":[0,0,0,0,0,0,0,0,0,0,0,0],"pointers":["r","c"],"steps":[{"at":{"r":0,"c":1},"vars":{"delta":5,"stored":5},"note":"Start the rectangle at its top-left corner."},{"at":{"r":0,"c":3},"vars":{"delta":-5,"stored":-5},"note":"Cancel the effect immediately to the right."},{"at":{"r":2,"c":1},"vars":{"delta":-5,"stored":-5},"note":"Cancel the effect immediately below."},{"at":{"r":2,"c":3},"vars":{"delta":5,"stored":5},"note":"Restore the region canceled twice at the diagonal corner."},{"at":{"r":0,"c":0},"vars":{"corner":0,"above":0,"left":0,"overlap":0,"value":0},"note":"Reconstruct cell (0,0) from the signed corner state."},{"at":{"r":0,"c":1},"vars":{"corner":5,"above":0,"left":0,"overlap":0,"value":5},"note":"Reconstruct cell (0,1) from the signed corner state."},{"at":{"r":0,"c":2},"vars":{"corner":0,"above":0,"left":5,"overlap":0,"value":5},"note":"Reconstruct cell (0,2) from the signed corner state."},{"at":{"r":0,"c":3},"vars":{"corner":-5,"above":0,"left":5,"overlap":0,"value":0},"note":"Reconstruct cell (0,3) from the signed corner state."},{"at":{"r":1,"c":0},"vars":{"corner":0,"above":0,"left":0,"overlap":0,"value":0},"note":"Reconstruct cell (1,0) from the signed corner state."},{"at":{"r":1,"c":1},"vars":{"corner":0,"above":5,"left":0,"overlap":0,"value":5},"note":"Reconstruct cell (1,1) from the signed corner state."},{"at":{"r":1,"c":2},"vars":{"corner":0,"above":5,"left":5,"overlap":5,"value":5},"note":"Reconstruct cell (1,2) from the signed corner state."},{"at":{"r":1,"c":3},"vars":{"corner":0,"above":0,"left":5,"overlap":5,"value":0},"note":"Reconstruct cell (1,3) from the signed corner state."},{"at":{"r":2,"c":0},"vars":{"corner":0,"above":0,"left":0,"overlap":0,"value":0},"note":"Reconstruct cell (2,0) from the signed corner state."},{"at":{"r":2,"c":1},"vars":{"corner":-5,"above":5,"left":0,"overlap":0,"value":0},"note":"Reconstruct cell (2,1) from the signed corner state."},{"at":{"r":2,"c":2},"vars":{"corner":0,"above":5,"left":0,"overlap":5,"value":0},"note":"Reconstruct cell (2,2) from the signed corner state."},{"at":{"r":2,"c":3},"vars":{"corner":5,"above":0,"left":0,"overlap":5,"value":0},"note":"Reconstruct cell (2,3) from the signed corner state."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java run
public final class DifferenceMatrixBlueprint {
    static long[][] apply(int rows, int cols, long[][] updates) {
        long[][] diff = new long[rows + 1][cols + 1];
        for (long[] u : updates) {
            int r1 = (int) u[0], c1 = (int) u[1];
            int r2 = (int) u[2], c2 = (int) u[3];
            long weight = u[4];
            diff[r1][c1] += weight;
            diff[r1][c2 + 1] -= weight;
            diff[r2 + 1][c1] -= weight;
            diff[r2 + 1][c2 + 1] += weight;
        }

        long[][] answer = new long[rows][cols];
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                long above = r == 0 ? 0 : diff[r - 1][c];
                long left = c == 0 ? 0 : diff[r][c - 1];
                long overlap = r == 0 || c == 0 ? 0 : diff[r - 1][c - 1];
                diff[r][c] += above + left - overlap;
                answer[r][c] = diff[r][c];
            }
        }
        return answer;
    }

    public static void main(String[] args) {
        long[][] result = apply(3, 4, new long[][] {{0,1,1,2,5}});
        if (result[0][1] != 5 || result[1][2] != 5 || result[2][2] != 0) {
            throw new AssertionError();
        }
    }
}
```

Writing all updates costs O(u) time. Reconstructing the matrix costs O(rows * cols), so the total is O(u + rows * cols), with O(rows * cols) extra space. The sentinel border makes all four corner writes valid, including an update that ends at the bottom-right cell. Use `long[][]` when overlapping signed weights may push a cell total beyond `int`. Java represents each row as a separate array object, so very large matrices also carry per-row allocation overhead.

<!-- stage: applicability -->
### When It Applies

Use a two-dimensional difference array when many axis-aligned rectangle additions are known before the final grid is needed. The invariant is that `diff` stores signed changes whose two-dimensional prefix reconstruction equals the sum of all update weights covering each cell.

The nearest false friend is a two-dimensional prefix-query table. That table preprocesses fixed cell values for repeated rectangle reads; this table postpones rectangle writes and then materializes once. The method silently fails as an online solution when a query must be answered between updates, because the grid is not current until reconstruction. Rotated rectangles and irregular shapes also do not obey the four-corner rule. In Java, accumulate into `long` and avoid allocating one temporary rectangle-sized object per update.

<!-- stage: exercises -->
### Exercises

#### [Build] One Rectangle Add (Author exercise)
<!-- id: ps-2d-diff-one-rectangle -->

**Prerequisites.** One-dimensional difference arrays and the four-corner construction from this lesson.

**Problem.** Given positive dimensions `rows` and `cols`, an inclusive rectangle, and a signed weight, return the zero matrix after that weight has been added to every cell inside the rectangle.

**Constraints.** `1 <= rows, cols <= 500`; rectangle coordinates are valid; `-10^9 <= weight <= 10^9`; target O(rows * cols) time and O(rows * cols) space.

**Example 1.** Input `rows = 3`, `cols = 4`, rectangle `(0,1,1,2)`, `weight = 5`, output `[[0,5,5,0],[0,5,5,0],[0,0,0,0]]`.

**Example 2.** Input `rows = 1`, `cols = 1`, rectangle `(0,0,0,0)`, `weight = -3`, output `[[-3]]`.

**Hint.** Mark the start, then ask where the effect must stop along each axis. Why does the diagonally opposite cancellation need the original sign?

**Changed decision.** This first rung records one rectangle with four writes before reconstructing any real cell.

#### [Vary] Increment Submatrices (LeetCode 2536)
<!-- id: ps-2d-diff-increment-submatrices -->

**Prerequisites.** The four corner deltas for one inclusive rectangle.

**Problem.** Given `n` and a list of inclusive square-matrix rectangles, begin with an `n` by `n` zero matrix, add one to every cell in every rectangle, and return the final matrix.

**Constraints.** `1 <= n <= 500`; `1 <= queries.length <= 10^4`; all rectangle coordinates are valid; target O(n^2 + queries.length) time.

**Example 1.** Input `n = 3`, rectangles `[(0,0,1,1),(1,1,2,2)]`, output `[[1,1,0],[1,2,1],[0,1,1]]`.

**Example 2.** Input `n = 2`, rectangles `[(0,0,1,1),(0,1,0,1)]`, output `[[1,2],[1,1]]`, including an update that touches the outer edge.

**Hint.** Do not reconstruct after each query. What information can every query add to the same difference table in constant time?

**Changed decision.** Many unit-weight rectangles share one delta table and one reconstruction pass.

#### [Boundary] Bottom-Right Edge (Author exercise)
<!-- id: ps-2d-diff-bottom-right-edge -->

**Prerequisites.** Sentinel borders and inclusive rectangle endpoints.

**Problem.** Apply weighted rectangle updates that are all guaranteed to end at the matrix's bottom-right cell. Return the final matrix and the dimensions of the internal difference table.

**Constraints.** `1 <= rows, cols <= 400`; `0 <= updates.length <= 10^4`; signed cell totals fit in `long`; target O(updates.length + rows * cols) time.

**Example 1.** Input `rows = 2`, `cols = 3`, updates `[(0,1,1,2,4)]`, output matrix `[[0,4,4],[0,4,4]]`, internal dimensions `[3,4]`.

**Example 2.** Input `rows = 1`, `cols = 2`, updates `[(0,0,0,1,-2)]`, output matrix `[[-2,-2]]`, internal dimensions `[2,3]`.

**Hint.** The stop markers belong one row and one column beyond the final covered cells. Where can those markers be stored without conditional writes?

**Changed decision.** Every update forces both cancellation coordinates onto the sentinel border, exposing undersized storage.

#### [Recognize] Weighted Rectangle Updates (Author exercise)
<!-- id: ps-2d-diff-weighted-updates -->

**Prerequisites.** Batched rectangle increments, signed arithmetic, and `long` accumulation.

**Problem.** Start from a given integer matrix, apply inclusive rectangle updates with arbitrary signed `long` weights, and return the final `long` matrix without modifying the input.

**Constraints.** `1 <= rows, cols <= 500`; at most `2 * 10^4` updates; each weight has absolute value at most `10^12`; target O(updates.length + rows * cols) time.

**Example 1.** Input matrix `[[3,1],[4,2]]`, updates `[(0,0,1,0,5),(0,1,1,1,-2)]`, output `[[8,-1],[9,0]]`.

**Example 2.** Input matrix `[[7]]`, updates `[(0,0,0,0,10000000000)]`, output `[[10000000007]]`, which requires `long`.

**Hint.** Keep the source matrix separate from the pending changes. At what point should each reconstructed delta be combined with its original cell?

**Changed decision.** The base matrix is nonzero and update magnitudes require a wider numeric type than `int`.
