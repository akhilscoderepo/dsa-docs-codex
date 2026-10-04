<!-- solutions-for: 08-difference-arrays -->
### Difference Arrays

#### Solution: [Build] One Range Add (Author exercise)
<!-- id: ps-diff-one-range-add -->

**Approach.** Allocate a sentinel delta slot. Add `value` at `left`, subtract it at `right + 1`, and prefix the first `n` entries into the result. The running value is active exactly inside the requested interval.

**Complexity.** O(n) time and O(n) space.

```java run
import java.util.Arrays;
public final class OneRangeAdd {
    static long[] solve(int n, int left, int right, int value) {
        long[] delta = new long[n + 1];
        delta[left] += value;
        delta[right + 1] -= value;
        long[] answer = new long[n];
        long running = 0;
        for (int i = 0; i < n; i++) answer[i] = running += delta[i];
        return answer;
    }
    static long[] brute(int n, int left, int right, int value) {
        long[] answer = new long[n];
        for (int i = left; i <= right; i++) answer[i] += value;
        return answer;
    }
    public static void main(String[] args) {
        if (!Arrays.equals(solve(5, 1, 3, 4), new long[] {0,4,4,4,0})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(1, 0, 0, -2), new long[] {-2})) throw new AssertionError("example 2");
        var random = new java.util.Random(81);
        for (int t = 0; t < 500; t++) {
            int n = random.nextInt(12) + 1;
            int left = random.nextInt(n), right = left + random.nextInt(n - left);
            int value = random.nextInt(21) - 10;
            if (!Arrays.equals(solve(n, left, right, value), brute(n, left, right, value))) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Vary] Corporate Flight Bookings (LeetCode 1109)
<!-- id: ps-diff-flight-bookings -->

**Approach.** Convert `first` and `last` to zero-based inclusive indices. Record the seat increase at `first - 1` and its cancellation at zero-based `last`, then reconstruct the booked seats in flight order.

**Complexity.** O(n + b) time for `b` bookings and O(n) space.

```java run
import java.util.Arrays;
public final class CorporateFlightBookings {
    static int[] solve(int[][] bookings, int n) {
        int[] delta = new int[n + 1];
        for (int[] booking : bookings) {
            int left = booking[0] - 1;
            int stop = booking[1];
            delta[left] += booking[2];
            delta[stop] -= booking[2];
        }
        int[] answer = new int[n];
        int running = 0;
        for (int i = 0; i < n; i++) answer[i] = running += delta[i];
        return answer;
    }
    static int[] brute(int[][] bookings, int n) {
        int[] answer = new int[n];
        for (int[] booking : bookings) {
            for (int flight = booking[0] - 1; flight < booking[1]; flight++) answer[flight] += booking[2];
        }
        return answer;
    }
    public static void main(String[] args) {
        if (!Arrays.equals(solve(new int[][] {{1,2,7},{2,4,3}}, 4), new int[] {7,10,3,3})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[][] {{3,3,8}}, 3), new int[] {0,0,8})) throw new AssertionError("example 2");
        var random = new java.util.Random(82);
        for (int t = 0; t < 400; t++) {
            int n = random.nextInt(9) + 1, count = random.nextInt(8) + 1;
            int[][] bookings = new int[count][3];
            for (int i = 0; i < count; i++) {
                int first = random.nextInt(n) + 1;
                int last = first + random.nextInt(n - first + 1);
                bookings[i] = new int[] {first, last, random.nextInt(10) + 1};
            }
            if (!Arrays.equals(solve(bookings, n), brute(bookings, n))) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Boundary] Final Endpoint (Author exercise)
<!-- id: ps-diff-final-endpoint -->

**Approach.** Use `n + 1` delta entries, so every inclusive update can write its cancellation at index `n`. Prefix only indices `0` through `n - 1`; the final delta slot closes the bookkeeping but never becomes output.

**Complexity.** O(n + u) time for `u` updates and O(n) space.

```java run
import java.util.Arrays;
public final class FinalEndpointUpdates {
    static long[] solve(int n, long[][] updates) {
        long[] delta = new long[n + 1];
        for (long[] update : updates) {
            int left = Math.toIntExact(update[0]);
            int right = Math.toIntExact(update[1]);
            delta[left] += update[2];
            delta[right + 1] -= update[2];
        }
        long[] answer = new long[n];
        long running = 0;
        for (int i = 0; i < n; i++) answer[i] = running += delta[i];
        return answer;
    }
    static long[] brute(int n, long[][] updates) {
        long[] answer = new long[n];
        for (long[] update : updates) {
            for (int i = (int) update[0]; i <= (int) update[1]; i++) answer[i] += update[2];
        }
        return answer;
    }
    public static void main(String[] args) {
        if (!Arrays.equals(solve(4, new long[][] {{0,3,2},{3,3,-1}}), new long[] {2,2,2,1})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(1, new long[][] {{0,0,9},{0,0,-4}}), new long[] {5})) throw new AssertionError("example 2");
        var random = new java.util.Random(83);
        for (int t = 0; t < 400; t++) {
            int n = random.nextInt(10) + 1, count = random.nextInt(8) + 1;
            long[][] updates = new long[count][3];
            for (int i = 0; i < count; i++) updates[i] = new long[] {random.nextInt(n), n - 1, random.nextInt(21) - 10};
            if (!Arrays.equals(solve(n, updates), brute(n, updates))) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Recognize] Car Pooling (LeetCode 1094)
<!-- id: ps-diff-car-pooling -->

**Approach.** Treat each pickup as a positive event at `from` and each drop-off as a negative event at `to`. A prefix scan gives the load on the road segment beginning at each coordinate. Return false as soon as that load exceeds capacity.

**Complexity.** O(t + 1001) time for `t` trips and O(1001) space under the bounded-coordinate contract.

```java run
public final class CarPooling {
    static boolean solve(int[][] trips, int capacity) {
        int[] delta = new int[1001];
        for (int[] trip : trips) {
            delta[trip[1]] += trip[0];
            delta[trip[2]] -= trip[0];
        }
        int passengers = 0;
        for (int change : delta) {
            passengers += change;
            if (passengers > capacity) return false;
        }
        return true;
    }
    static boolean brute(int[][] trips, int capacity) {
        for (int position = 0; position <= 1000; position++) {
            int passengers = 0;
            for (int[] trip : trips) {
                if (trip[1] <= position && position < trip[2]) passengers += trip[0];
            }
            if (passengers > capacity) return false;
        }
        return true;
    }
    public static void main(String[] args) {
        if (!solve(new int[][] {{2,0,4},{3,4,7}}, 3)) throw new AssertionError("example 1");
        if (solve(new int[][] {{2,1,5},{2,3,6}}, 3)) throw new AssertionError("example 2");
        var random = new java.util.Random(84);
        for (int t = 0; t < 500; t++) {
            int count = random.nextInt(8) + 1;
            int[][] trips = new int[count][3];
            for (int i = 0; i < count; i++) {
                int from = random.nextInt(15), to = from + random.nextInt(15 - from) + 1;
                trips[i] = new int[] {random.nextInt(6) + 1, from, to};
            }
            int capacity = random.nextInt(15) + 1;
            if (solve(trips, capacity) != brute(trips, capacity)) throw new AssertionError("random");
        }
    }
}
```
