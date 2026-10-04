<!-- solutions-for: 10-two-dimensional-difference -->
### Two-Dimensional Difference

#### Solution: [Build] One Rectangle Add (Author exercise)
<!-- id: ps-2d-diff-one-rectangle -->

**Approach.** Store `+weight` at the rectangle's top-left corner, `-weight` at the two positions immediately beyond its right and bottom edges, and `+weight` at the diagonal cancellation corner. Reconstruct each real cell from the state above, to the left, and above-left.

**Complexity.** O(rows * cols) time and O(rows * cols) space; the rectangle itself is recorded in O(1) time.

```java run
import java.util.Arrays;
public final class OneRectangleAdd {
    static long[][] solve(int rows, int cols, int r1, int c1, int r2, int c2, long weight) {
        long[][] diff = new long[rows + 1][cols + 1];
        diff[r1][c1] += weight;
        diff[r1][c2 + 1] -= weight;
        diff[r2 + 1][c1] -= weight;
        diff[r2 + 1][c2 + 1] += weight;
        long[][] answer = new long[rows][cols];
        for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) {
            if (r > 0) diff[r][c] += diff[r - 1][c];
            if (c > 0) diff[r][c] += diff[r][c - 1];
            if (r > 0 && c > 0) diff[r][c] -= diff[r - 1][c - 1];
            answer[r][c] = diff[r][c];
        }
        return answer;
    }
    static long[][] brute(int rows, int cols, int r1, int c1, int r2, int c2, long weight) {
        long[][] a = new long[rows][cols];
        for (int r = r1; r <= r2; r++) for (int c = c1; c <= c2; c++) a[r][c] += weight;
        return a;
    }
    static boolean equal(long[][] a, long[][] b) { return Arrays.deepEquals(a, b); }
    public static void main(String[] args) {
        long[][] first = {{0,5,5,0},{0,5,5,0},{0,0,0,0}};
        if (!equal(solve(3,4,0,1,1,2,5), first)) throw new AssertionError("example 1");
        if (!equal(solve(1,1,0,0,0,0,-3), new long[][] {{-3}})) throw new AssertionError("example 2");
        var random = new java.util.Random(710);
        for (int t = 0; t < 500; t++) {
            int rows = random.nextInt(5) + 1, cols = random.nextInt(5) + 1;
            int r1 = random.nextInt(rows), r2 = r1 + random.nextInt(rows - r1);
            int c1 = random.nextInt(cols), c2 = c1 + random.nextInt(cols - c1);
            long w = random.nextInt(11) - 5;
            if (!equal(solve(rows,cols,r1,c1,r2,c2,w), brute(rows,cols,r1,c1,r2,c2,w))) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Vary] Increment Submatrices (LeetCode 2536)
<!-- id: ps-2d-diff-increment-submatrices -->

**Approach.** Add all four signed corners for every query to one `(n + 1)` square table. A single two-dimensional prefix pass converts the accumulated corner changes into the number of rectangles covering each cell.

**Complexity.** O(q + n^2) time and O(n^2) space, where `q` is the number of queries.

```java run
import java.util.Arrays;
public final class IncrementSubmatrices {
    static int[][] solve(int n, int[][] queries) {
        int[][] delta = new int[n + 1][n + 1];
        for (int[] q : queries) {
            delta[q[0]][q[1]]++;
            delta[q[0]][q[3] + 1]--;
            delta[q[2] + 1][q[1]]--;
            delta[q[2] + 1][q[3] + 1]++;
        }
        int[][] result = new int[n][n];
        for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) {
            int above = r == 0 ? 0 : delta[r - 1][c];
            int left = c == 0 ? 0 : delta[r][c - 1];
            int overlap = r == 0 || c == 0 ? 0 : delta[r - 1][c - 1];
            delta[r][c] += above + left - overlap;
            result[r][c] = delta[r][c];
        }
        return result;
    }
    static int[][] brute(int n, int[][] queries) {
        int[][] a = new int[n][n];
        for (int[] q : queries) for (int r = q[0]; r <= q[2]; r++) for (int c = q[1]; c <= q[3]; c++) a[r][c]++;
        return a;
    }
    public static void main(String[] args) {
        int[][] first = {{1,1,0},{1,2,1},{0,1,1}};
        if (!Arrays.deepEquals(solve(3,new int[][] {{0,0,1,1},{1,1,2,2}}), first)) throw new AssertionError("example 1");
        int[][] second = {{1,2},{1,1}};
        if (!Arrays.deepEquals(solve(2,new int[][] {{0,0,1,1},{0,1,0,1}}), second)) throw new AssertionError("example 2");
        var random = new java.util.Random(711);
        for (int t = 0; t < 400; t++) {
            int n = random.nextInt(5) + 1, qn = random.nextInt(8);
            int[][] q = new int[qn][4];
            for (int i = 0; i < qn; i++) {
                q[i][0] = random.nextInt(n); q[i][2] = q[i][0] + random.nextInt(n - q[i][0]);
                q[i][1] = random.nextInt(n); q[i][3] = q[i][1] + random.nextInt(n - q[i][1]);
            }
            if (!Arrays.deepEquals(solve(n,q), brute(n,q))) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Boundary] Bottom-Right Edge (Author exercise)
<!-- id: ps-2d-diff-bottom-right-edge -->

**Approach.** Allocate one extra row and column, then perform all four corner writes without checking whether an endpoint is final. The cancellations land in the sentinel storage and prevent the effect from escaping during reconstruction.

**Complexity.** O(u + rows * cols) time and O(rows * cols) space.

```java run
import java.util.Arrays;
public final class BottomRightEdge {
    record Result(long[][] matrix, int[] internalDimensions) {}
    static Result solve(int rows, int cols, long[][] updates) {
        long[][] changes = new long[rows + 1][cols + 1];
        for (long[] u : updates) {
            int r1 = (int) u[0], c1 = (int) u[1], r2 = (int) u[2], c2 = (int) u[3];
            changes[r1][c1] += u[4];
            changes[r1][c2 + 1] -= u[4];
            changes[r2 + 1][c1] -= u[4];
            changes[r2 + 1][c2 + 1] += u[4];
        }
        long[][] matrix = new long[rows][cols];
        for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) {
            long value = changes[r][c];
            if (r != 0) value += changes[r - 1][c];
            if (c != 0) value += changes[r][c - 1];
            if (r != 0 && c != 0) value -= changes[r - 1][c - 1];
            changes[r][c] = matrix[r][c] = value;
        }
        return new Result(matrix, new int[] {changes.length, changes[0].length});
    }
    public static void main(String[] args) {
        Result a = solve(2,3,new long[][] {{0,1,1,2,4}});
        if (!Arrays.deepEquals(a.matrix(), new long[][] {{0,4,4},{0,4,4}})
                || !Arrays.equals(a.internalDimensions(), new int[] {3,4})) throw new AssertionError("example 1");
        Result b = solve(1,2,new long[][] {{0,0,0,1,-2}});
        if (!Arrays.deepEquals(b.matrix(), new long[][] {{-2,-2}})
                || !Arrays.equals(b.internalDimensions(), new int[] {2,3})) throw new AssertionError("example 2");
    }
}
```

#### Solution: [Recognize] Weighted Rectangle Updates (Author exercise)
<!-- id: ps-2d-diff-weighted-updates -->

**Approach.** Keep the original matrix unchanged and accumulate only pending rectangle effects in a `long` difference table. Reconstruct each effect once and add it to the corresponding source value while writing the result.

**Complexity.** O(u + rows * cols) time and O(rows * cols) extra space.

```java run
import java.util.Arrays;
public final class WeightedRectangleUpdates {
    static long[][] solve(int[][] base, long[][] updates) {
        int rows = base.length, cols = base[0].length;
        long[][] diff = new long[rows + 1][cols + 1];
        for (long[] u : updates) {
            int top = (int) u[0], left = (int) u[1], bottom = (int) u[2], right = (int) u[3];
            long w = u[4];
            diff[top][left] += w; diff[top][right + 1] -= w;
            diff[bottom + 1][left] -= w; diff[bottom + 1][right + 1] += w;
        }
        long[][] answer = new long[rows][cols];
        for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) {
            diff[r][c] += (r == 0 ? 0 : diff[r - 1][c])
                    + (c == 0 ? 0 : diff[r][c - 1])
                    - (r == 0 || c == 0 ? 0 : diff[r - 1][c - 1]);
            answer[r][c] = base[r][c] + diff[r][c];
        }
        return answer;
    }
    static long[][] brute(int[][] base, long[][] updates) {
        long[][] a = new long[base.length][base[0].length];
        for (int r = 0; r < base.length; r++) for (int c = 0; c < base[0].length; c++) a[r][c] = base[r][c];
        for (long[] u : updates) for (int r = (int)u[0]; r <= u[2]; r++) for (int c = (int)u[1]; c <= u[3]; c++) a[r][c] += u[4];
        return a;
    }
    public static void main(String[] args) {
        int[][] base = {{3,1},{4,2}};
        long[][] updates = {{0,0,1,0,5},{0,1,1,1,-2}};
        if (!Arrays.deepEquals(solve(base,updates), new long[][] {{8,-1},{9,0}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(solve(new int[][] {{7}},new long[][] {{0,0,0,0,10000000000L}}), new long[][] {{10000000007L}})) throw new AssertionError("example 2");
        var random = new java.util.Random(712);
        for (int t = 0; t < 350; t++) {
            int rows = random.nextInt(4) + 1, cols = random.nextInt(4) + 1;
            int[][] b = new int[rows][cols];
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) b[r][c] = random.nextInt(11) - 5;
            long[][] q = new long[random.nextInt(7)][5];
            for (int i = 0; i < q.length; i++) {
                q[i][0] = random.nextInt(rows); q[i][2] = q[i][0] + random.nextInt(rows - (int)q[i][0]);
                q[i][1] = random.nextInt(cols); q[i][3] = q[i][1] + random.nextInt(cols - (int)q[i][1]); q[i][4] = random.nextInt(15) - 7;
            }
            if (!Arrays.deepEquals(solve(b,q), brute(b,q))) throw new AssertionError("random");
        }
    }
}
```
