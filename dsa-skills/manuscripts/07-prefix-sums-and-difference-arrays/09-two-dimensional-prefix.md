<!-- lesson-kind: standard -->
<!-- lesson-id: two-dimensional-prefix -->
## Two-Dimensional Prefix

<!-- stage: context -->
### Repeated Rectangle Totals

A monitoring dashboard stores one integer for every region and hour. An analyst repeatedly selects a rectangular block and asks for its total. The matrix does not change between requests, but the selected top, bottom, left, and right boundaries do. Adding the cells inside one rectangle is straightforward. Repeating that work for thousands of overlapping rectangles is the real problem: neighboring requests may rescan almost the same rows and columns.

<!-- stage: naive -->
### Scan Each Requested Rectangle

The direct method walks through every row and column inside the requested inclusive boundaries. It is correct because it visits every selected cell exactly once, and it is the simplest oracle for testing a faster implementation.

```java run
public final class RectangleSumNaive {
    static long sum(int[][] matrix, int row1, int col1, int row2, int col2) {
        long total = 0;
        for (int r = row1; r <= row2; r++) {
            for (int c = col1; c <= col2; c++) total += matrix[r][c];
        }
        return total;
    }
    public static void main(String[] args) {
        int[][] matrix = {{2,-1,4},{3,5,0},{-2,6,1}};
        if (sum(matrix, 1, 1, 2, 2) != 12) throw new AssertionError();
    }
}
```

<!-- stage: bottleneck -->
### Overlapping Queries Rescan Cells

Suppose a 2,000 by 2,000 matrix receives 100,000 requests, and most requests cover half the matrix. One answer performs about two million additions. The next request may shift one boundary by a single cell yet repeat nearly all of those additions. A rectangle with height `h` and width `w` costs O(hw), so the full workload can approach O(qrc) for `q` queries on `r` rows and `c` columns. The fixed matrix gives us a chance to preprocess that repeated work once.

<!-- stage: insight -->
### Summarize Origin Rectangles

Build a **two-dimensional prefix** table in which `prefix[r + 1][c + 1]` stores the sum of the rectangle from matrix cell `(0,0)` through `(r,c)`. A requested rectangle can then be recovered from four stored origin rectangles. Begin with the large rectangle ending at the request's bottom-right corner. Remove the origin rectangle above the request and the origin rectangle to its left.

<!-- names: two-dimensional prefix, inclusion-exclusion, sentinel border -->

Those two removed strips overlap in the top-left region, so that overlap was subtracted twice. Add it back once. This four-term rule is **inclusion-exclusion**:

`prefix[row2 + 1][col2 + 1] - prefix[row1][col2 + 1] - prefix[row2 + 1][col1] + prefix[row1][col1]`.

The extra top row and left column form a zero-valued **sentinel border**. They represent the empty area before row zero or column zero, so the same formula works when a requested rectangle touches either edge. During construction, the cell above and the cell to the left both contain the top-left overlap. We therefore add the current matrix value, add those two summaries, and subtract their shared overlap once. The move is safe because every cell inside the desired rectangle has net coefficient one, while every cell outside it cancels to zero.

<!-- stage: variables -->
### Coordinates And Stored Areas

`rows` and `cols` describe the original matrix. `prefix` has dimensions `(rows + 1) x (cols + 1)`. Matrix coordinates `row1`, `col1`, `row2`, and `col2` are inclusive. Their corresponding stored boundaries use `row2 + 1` and `col2 + 1`, while `row1` and `col1` already point to the boundaries immediately before the rectangle. All accumulated values use `long`.

<!-- stage: trace -->
### Build Once Then Subtract

Use the matrix `[[2,-1,4],[3,5,0],[-2,6,1]]`. The first row of stored areas becomes 2, 1, and 5. At matrix cell `(1,1)`, the current value is 5. The stored area above contributes 1 and the stored area to the left contributes 5. Both include cell `(0,0)`, whose stored area is 2, so subtracting that overlap gives `5 + 1 + 5 - 2 = 9`.

After all nine cells are processed, the stored bottom-right value is 18, the total of the whole matrix. Now query rows 1 through 2 and columns 1 through 2. Start with 18. Remove the top strip, worth 5, and the left strip, worth 3. Their shared top-left area, worth 2, was removed twice, so restore it. The answer is `18 - 5 - 3 + 2 = 12`. Restoring that overlap is the step most often missed.

```trace
{"cells":[2,-1,4,3,5,0,-2,6,1],"pointers":["r","c"],"steps":[{"at":{"r":0,"c":0},"vars":{"cell":2,"above":0,"left":0,"overlap":0,"prefix":2},"note":"Build the origin rectangle ending at (0,0); subtract the overlap once."},{"at":{"r":0,"c":1},"vars":{"cell":-1,"above":0,"left":2,"overlap":0,"prefix":1},"note":"Build the origin rectangle ending at (0,1); subtract the overlap once."},{"at":{"r":0,"c":2},"vars":{"cell":4,"above":0,"left":1,"overlap":0,"prefix":5},"note":"Build the origin rectangle ending at (0,2); subtract the overlap once."},{"at":{"r":1,"c":0},"vars":{"cell":3,"above":2,"left":0,"overlap":0,"prefix":5},"note":"Build the origin rectangle ending at (1,0); subtract the overlap once."},{"at":{"r":1,"c":1},"vars":{"cell":5,"above":1,"left":5,"overlap":2,"prefix":9},"note":"Build the origin rectangle ending at (1,1); subtract the overlap once."},{"at":{"r":1,"c":2},"vars":{"cell":0,"above":5,"left":9,"overlap":1,"prefix":13},"note":"Build the origin rectangle ending at (1,2); subtract the overlap once."},{"at":{"r":2,"c":0},"vars":{"cell":-2,"above":5,"left":0,"overlap":0,"prefix":3},"note":"Build the origin rectangle ending at (2,0); subtract the overlap once."},{"at":{"r":2,"c":1},"vars":{"cell":6,"above":9,"left":3,"overlap":5,"prefix":13},"note":"Build the origin rectangle ending at (2,1); subtract the overlap once."},{"at":{"r":2,"c":2},"vars":{"cell":1,"above":13,"left":13,"overlap":9,"prefix":18},"note":"Build the origin rectangle ending at (2,2); subtract the overlap once."},{"at":{"r":2,"c":2},"vars":{"total":18,"top":5,"left":3,"overlap":2,"answer":12},"note":"Query rows 1..2 and columns 1..2; restore the top-left overlap after removing two strips."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java run
public final class PrefixMatrixBlueprint {
    private final long[][] prefix;

    PrefixMatrixBlueprint(int[][] matrix) {
        int rows = matrix.length, cols = matrix[0].length;
        prefix = new long[rows + 1][cols + 1];
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                prefix[r + 1][c + 1] = matrix[r][c]
                        + prefix[r][c + 1]
                        + prefix[r + 1][c]
                        - prefix[r][c]; // above-left was included twice
            }
        }
    }

    long sumRegion(int row1, int col1, int row2, int col2) {
        return prefix[row2 + 1][col2 + 1]
                - prefix[row1][col2 + 1]
                - prefix[row2 + 1][col1]
                + prefix[row1][col1];
    }

    public static void main(String[] args) {
        var table = new PrefixMatrixBlueprint(new int[][] {{2,-1,4},{3,5,0},{-2,6,1}});
        if (table.sumRegion(1, 1, 2, 2) != 12) throw new AssertionError("inner rectangle");
        if (table.sumRegion(0, 0, 0, 0) != 2) throw new AssertionError("single cell");
    }
}
```

Construction costs O(rc) time and O(rc) extra space. Each rectangle query performs four table reads and therefore costs O(1) time. The constructor assumes the stated contract of a non-empty rectangular matrix. A `long[][]` protects accumulated totals even when each source cell fits in `int`.

<!-- stage: applicability -->
### When It Applies

Use this technique when the matrix is fixed and many axis-aligned rectangle sums must be answered. The invariant is that `prefix[r][c]` equals the sum of original cells in the half-open rectangle from `(0,0)` to `(r,c)`, excluding row `r` and column `c`.

The nearest false friend is a two-dimensional difference table. This lesson preprocesses fixed cell values for repeated reads; a difference table records many rectangle writes before one materialization. It also does not answer rotated rectangles or arbitrary shapes with the four-corner formula. In Java, `long[][]` is an array of row objects rather than one contiguous numeric block, but direct row indexing remains clear and avoids boxing.

<!-- stage: exercises -->
### Exercises

#### [Build] Range Sum Query 2D (LeetCode 304)
<!-- id: ps-2d-range-sum-query -->

**Prerequisites.** Sentinel prefix arrays and inclusive matrix coordinates from this lesson.

**Problem.** Construct an immutable matrix query object. For each call with inclusive corners `(row1,col1)` and `(row2,col2)`, return the sum of every cell inside that rectangle.

**Constraints.** `1 <= rows, cols <= 200`; `-10^5 <= matrix[r][c] <= 10^5`; at most `10^4` valid queries; target O(rows * cols) preprocessing and O(1) per query.

**Example 1.** Input `matrix = [[2,-1,4],[3,5,0],[-2,6,1]]`, query `(1,1,2,2)`, output `12` because `5 + 0 + 6 + 1 = 12`.

**Example 2.** Input `matrix = [[-7]]`, query `(0,0,0,0)`, output `-7`.

**Hint.** Draw the origin rectangle ending at the requested bottom-right cell. Which two outside strips must leave, and which shared corner then needs to return?

**Changed decision.** The matrix is preprocessed once so every later rectangle query uses four stored areas.

#### [Vary] Matrix Block Sum (LeetCode 1314)
<!-- id: ps-2d-matrix-block-sum -->

**Prerequisites.** Constant-time rectangle queries and clipping integer boundaries to a matrix.

**Problem.** Given a matrix and integer `k`, return a matrix where output cell `(r,c)` is the sum of source cells whose row differs from `r` by at most `k` and whose column differs from `c` by at most `k`. Ignore coordinates outside the matrix.

**Constraints.** `1 <= rows, cols <= 100`; `1 <= matrix[r][c] <= 100`; `0 <= k <= 100`; target O(rows * cols) time after preprocessing.

**Example 1.** Input `matrix = [[1,2,3],[4,5,6]]`, `k = 1`, output `[[12,21,16],[12,21,16]]` after each block is clipped to the two available rows.

**Example 2.** Input `matrix = [[3,1],[2,4]]`, `k = 0`, output `[[3,1],[2,4]]` because every block is one cell.

**Hint.** Convert each cell's radius into four inclusive coordinates. Clamp the top and left at zero and the bottom and right at the final valid indices before querying.

**Changed decision.** Instead of receiving query corners, the method derives and clips one rectangle around every matrix cell.

#### [Boundary] Single Cell Rectangle (Author exercise)
<!-- id: ps-2d-single-cell-rectangle -->

**Prerequisites.** The four-term inclusion-exclusion formula and sentinel coordinates.

**Problem.** Build the stored-area table for an integer matrix, then return an array containing the rectangle-sum answer for every single-cell query `(r,c,r,c)` in a supplied list of coordinates.

**Constraints.** `1 <= rows, cols <= 300`; `1 <= queries.length <= 10000`; coordinates are valid; source values and answers fit in `long`; target O(rows * cols + queries.length) time.

**Example 1.** Input `matrix = [[8,1],[-3,6]]`, `queries = [[0,1],[1,0]]`, output `[1,-3]`.

**Example 2.** Input `matrix = [[5]]`, `queries = [[0,0]]`, output `[5]`.

**Hint.** Substitute `row1 = row2` and `col1 = col2` into the normal formula. Do not invent a special-case branch; the surrounding areas should cancel.

**Changed decision.** Every requested rectangle has minimum width and height, exposing any off-by-one error in the stored boundaries.

#### [Recognize] Whole Matrix Query (Author exercise)
<!-- id: ps-2d-whole-matrix-query -->

**Prerequisites.** Origin-rectangle summaries and the zero-valued sentinel border.

**Problem.** Given a non-empty integer matrix, build the same rectangle-query structure and use its public query operation to return the sum of the entire matrix. Do not rescan the input after construction.

**Constraints.** `1 <= rows, cols <= 1000`; `-10^6 <= matrix[r][c] <= 10^6`; the result fits in `long`; target O(rows * cols) construction and O(1) for the final query.

**Example 1.** Input `matrix = [[2,-1,4],[3,5,0]]`, output `13`.

**Example 2.** Input `matrix = [[-5,-2]]`, output `-7`.

**Hint.** The requested top and left boundaries are both zero. Which sentinel entries are read by the three correction terms, and what values must they contain?

**Changed decision.** The query touches every outer boundary, testing whether the sentinel convention eliminates negative indices cleanly.
