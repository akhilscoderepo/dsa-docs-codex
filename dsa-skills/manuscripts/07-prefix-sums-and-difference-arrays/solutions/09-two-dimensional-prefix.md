<!-- solutions-for: 09-two-dimensional-prefix -->
### Two-Dimensional Prefix

#### Solution: [Build] Range Sum Query 2D (LeetCode 304)
<!-- id: ps-2d-range-sum-query -->

**Approach.** Store the sum of every origin-anchored rectangle behind a zero row and zero column. A query starts with the area through its bottom-right corner, removes the area above and the area to the left, then restores their shared overlap.

**Complexity.** O(rc) construction time and O(rc) space for `r` rows and `c` columns; each query takes O(1) time.

```java run
public final class RangeSumQuery2D {
    private final long[][] prefix;

    RangeSumQuery2D(int[][] matrix) {
        int rows = matrix.length, cols = matrix[0].length;
        prefix = new long[rows + 1][cols + 1];
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                prefix[r + 1][c + 1] = matrix[r][c] + prefix[r][c + 1]
                        + prefix[r + 1][c] - prefix[r][c];
            }
        }
    }

    long sumRegion(int row1, int col1, int row2, int col2) {
        return prefix[row2 + 1][col2 + 1] - prefix[row1][col2 + 1]
                - prefix[row2 + 1][col1] + prefix[row1][col1];
    }

    static long brute(int[][] matrix, int row1, int col1, int row2, int col2) {
        long total = 0;
        for (int r = row1; r <= row2; r++)
            for (int c = col1; c <= col2; c++) total += matrix[r][c];
        return total;
    }

    public static void main(String[] args) {
        int[][] sample = {{2,-1,4},{3,5,0},{-2,6,1}};
        if (new RangeSumQuery2D(sample).sumRegion(1,1,2,2) != 12) throw new AssertionError("example 1");
        if (new RangeSumQuery2D(new int[][] {{-7}}).sumRegion(0,0,0,0) != -7) throw new AssertionError("example 2");
        var random = new java.util.Random(91);
        for (int t = 0; t < 300; t++) {
            int rows = random.nextInt(6) + 1, cols = random.nextInt(6) + 1;
            int[][] matrix = new int[rows][cols];
            for (int[] row : matrix) for (int c = 0; c < cols; c++) row[c] = random.nextInt(21) - 10;
            var table = new RangeSumQuery2D(matrix);
            for (int q = 0; q < 20; q++) {
                int r1 = random.nextInt(rows), r2 = r1 + random.nextInt(rows - r1);
                int c1 = random.nextInt(cols), c2 = c1 + random.nextInt(cols - c1);
                if (table.sumRegion(r1,c1,r2,c2) != brute(matrix,r1,c1,r2,c2)) throw new AssertionError("random");
            }
        }
    }
}
```

#### Solution: [Vary] Matrix Block Sum (LeetCode 1314)
<!-- id: ps-2d-matrix-block-sum -->

**Approach.** Build one stored-area table, then derive the clipped top, left, bottom, and right boundary for every output cell. The ordinary rectangle formula answers each block without revisiting its contents.

**Complexity.** O(rc) time and O(rc) space for an `r` by `c` matrix.

```java run
import java.util.Arrays;
public final class MatrixBlockSum {
    static long[][] solve(int[][] matrix, int k) {
        int rows = matrix.length, cols = matrix[0].length;
        long[][] prefix = new long[rows + 1][cols + 1];
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                prefix[r + 1][c + 1] = matrix[r][c] + prefix[r][c + 1]
                        + prefix[r + 1][c] - prefix[r][c];
            }
        }
        long[][] answer = new long[rows][cols];
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                int top = Math.max(0, r - k), left = Math.max(0, c - k);
                int bottom = Math.min(rows - 1, r + k), right = Math.min(cols - 1, c + k);
                answer[r][c] = prefix[bottom + 1][right + 1] - prefix[top][right + 1]
                        - prefix[bottom + 1][left] + prefix[top][left];
            }
        }
        return answer;
    }

    static long[][] brute(int[][] matrix, int k) {
        int rows = matrix.length, cols = matrix[0].length;
        long[][] answer = new long[rows][cols];
        for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) {
            for (int rr = Math.max(0, r-k); rr <= Math.min(rows-1, r+k); rr++)
                for (int cc = Math.max(0, c-k); cc <= Math.min(cols-1, c+k); cc++) answer[r][c] += matrix[rr][cc];
        }
        return answer;
    }

    static boolean same(long[][] a, long[][] b) { return Arrays.deepEquals(a, b); }

    public static void main(String[] args) {
        if (!same(solve(new int[][] {{1,2,3},{4,5,6}}, 1), new long[][] {{12,21,16},{12,21,16}})) throw new AssertionError("example 1");
        if (!same(solve(new int[][] {{3,1},{2,4}}, 0), new long[][] {{3,1},{2,4}})) throw new AssertionError("example 2");
        var random = new java.util.Random(92);
        for (int t = 0; t < 300; t++) {
            int rows = random.nextInt(6)+1, cols = random.nextInt(6)+1, k = random.nextInt(7);
            int[][] matrix = new int[rows][cols];
            for (int[] row : matrix) for (int c = 0; c < cols; c++) row[c] = random.nextInt(11);
            if (!same(solve(matrix,k), brute(matrix,k))) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Boundary] Single Cell Rectangle (Author exercise)
<!-- id: ps-2d-single-cell-rectangle -->

**Approach.** Build the usual sentinel-bordered table. For every coordinate, call the same four-term query with identical top and bottom rows and identical left and right columns; all neighboring areas cancel, leaving that cell.

**Complexity.** O(rc + q) time and O(rc + q) space for `q` requested coordinates, including the returned array.

```java run
import java.util.Arrays;
public final class SingleCellRectangles {
    static long[] solve(int[][] matrix, int[][] queries) {
        int rows = matrix.length, cols = matrix[0].length;
        long[][] prefix = new long[rows + 1][cols + 1];
        for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++)
            prefix[r+1][c+1] = matrix[r][c] + prefix[r][c+1] + prefix[r+1][c] - prefix[r][c];
        long[] answer = new long[queries.length];
        for (int i = 0; i < queries.length; i++) {
            int r = queries[i][0], c = queries[i][1];
            answer[i] = prefix[r+1][c+1] - prefix[r][c+1] - prefix[r+1][c] + prefix[r][c];
        }
        return answer;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(solve(new int[][] {{8,1},{-3,6}}, new int[][] {{0,1},{1,0}}), new long[] {1,-3})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[][] {{5}}, new int[][] {{0,0}}), new long[] {5})) throw new AssertionError("example 2");
        var random = new java.util.Random(93);
        for (int t = 0; t < 300; t++) {
            int rows = random.nextInt(7)+1, cols = random.nextInt(7)+1, q = random.nextInt(15)+1;
            int[][] matrix = new int[rows][cols], queries = new int[q][2];
            for (int[] row : matrix) for (int c = 0; c < cols; c++) row[c] = random.nextInt(31)-15;
            long[] expected = new long[q];
            for (int i = 0; i < q; i++) {
                int r = random.nextInt(rows), c = random.nextInt(cols);
                queries[i] = new int[] {r,c};
                expected[i] = matrix[r][c];
            }
            if (!Arrays.equals(solve(matrix,queries), expected)) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Recognize] Whole Matrix Query (Author exercise)
<!-- id: ps-2d-whole-matrix-query -->

**Approach.** Construct the stored-area table, then issue the public rectangle query from `(0,0)` through the final row and column. The three correction terms read the sentinel row or column and therefore contribute zero.

**Complexity.** O(rc) construction time, O(1) query time, and O(rc) extra space.

```java run
public final class WholeMatrixQuery {
    private final long[][] prefix;

    WholeMatrixQuery(int[][] matrix) {
        int rows = matrix.length, cols = matrix[0].length;
        prefix = new long[rows + 1][cols + 1];
        for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++)
            prefix[r+1][c+1] = matrix[r][c] + prefix[r][c+1] + prefix[r+1][c] - prefix[r][c];
    }

    long query(int row1, int col1, int row2, int col2) {
        return prefix[row2+1][col2+1] - prefix[row1][col2+1]
                - prefix[row2+1][col1] + prefix[row1][col1];
    }

    static long solve(int[][] matrix) {
        return new WholeMatrixQuery(matrix).query(0, 0, matrix.length-1, matrix[0].length-1);
    }

    static long brute(int[][] matrix) {
        long total = 0;
        for (int[] row : matrix) for (int value : row) total += value;
        return total;
    }

    public static void main(String[] args) {
        if (solve(new int[][] {{2,-1,4},{3,5,0}}) != 13) throw new AssertionError("example 1");
        if (solve(new int[][] {{-5,-2}}) != -7) throw new AssertionError("example 2");
        var random = new java.util.Random(94);
        for (int t = 0; t < 500; t++) {
            int rows = random.nextInt(8)+1, cols = random.nextInt(8)+1;
            int[][] matrix = new int[rows][cols];
            for (int[] row : matrix) for (int c = 0; c < cols; c++) row[c] = random.nextInt(101)-50;
            if (solve(matrix) != brute(matrix)) throw new AssertionError("random");
        }
    }
}
```
