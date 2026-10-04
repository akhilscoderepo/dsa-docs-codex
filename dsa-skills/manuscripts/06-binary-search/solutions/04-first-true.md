<!-- solutions-for: 04-first-true -->
### First True Solutions

#### Solution: [Build] First True Boolean (Author exercise)
<!-- id: bs-first-true-boolean -->

**Approach.** Keep a half-open interval containing the earliest true value. A false midpoint joins the rejected prefix, while a true midpoint remains possible and moves the exclusive right endpoint. The exercise guarantees that the final boundary indexes a true value.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.Random;

public final class FirstTrueBoolean {
    static int firstTrue(boolean[] values) {
        int lo = 0, hi = values.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (values[mid]) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }

    static int linear(boolean[] values) {
        for (int i = 0; i < values.length; i++) if (values[i]) return i;
        throw new AssertionError("contract requires a true value");
    }

    public static void main(String[] args) {
        if (firstTrue(new boolean[] {false, false, true, true}) != 2) throw new AssertionError("example 1");
        if (firstTrue(new boolean[] {true, true, true}) != 0) throw new AssertionError("example 2");
        Random random = new Random(604);
        for (int trial = 0; trial < 600; trial++) {
            int n = 1 + random.nextInt(80);
            int boundary = random.nextInt(n);
            boolean[] values = new boolean[n];
            for (int i = boundary; i < n; i++) values[i] = true;
            if (firstTrue(values) != linear(values)) throw new AssertionError("boundary=" + boundary);
        }
    }
}
```

#### Solution: [Vary] First Bad Version (LeetCode 278)
<!-- id: bs-first-bad-version -->

**Approach.** Search the closed domain from `1` through `n`, which contains a bad version by contract. A bad midpoint stays as a candidate by moving `hi` to it; a good midpoint and every earlier version are discarded. The endpoints meet at the first bad version.

**Complexity.** O(log n) API calls and O(1) extra space.

```java run
import java.util.Random;

public final class FirstBadVersion {
    static int configuredFirstBad;

    static boolean isBadVersion(int version) {
        return version >= configuredFirstBad;
    }

    static int firstBadVersion(int n) {
        int lo = 1, hi = n;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (isBadVersion(mid)) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }

    public static void main(String[] args) {
        configuredFirstBad = 6;
        if (firstBadVersion(9) != 6) throw new AssertionError("example 1");
        configuredFirstBad = 1;
        if (firstBadVersion(1) != 1) throw new AssertionError("example 2");
        Random random = new Random(278);
        for (int trial = 0; trial < 800; trial++) {
            int n = 1 + random.nextInt(100_000);
            configuredFirstBad = 1 + random.nextInt(n);
            if (firstBadVersion(n) != configuredFirstBad) throw new AssertionError("n=" + n);
        }
        configuredFirstBad = Integer.MAX_VALUE;
        if (firstBadVersion(Integer.MAX_VALUE) != Integer.MAX_VALUE) throw new AssertionError("overflow boundary");
    }
}
```

#### Solution: [Boundary] No True Value (Author exercise)
<!-- id: bs-no-true-value -->

**Approach.** Search `[0, n)` and reserve `n` as the not-found boundary. Only real midpoints are passed to the test. If every result is false, each one joins the rejected prefix and `lo` eventually reaches the untouched sentinel.

**Complexity.** O(log(n + 1)) test evaluations and O(1) extra space.

```java run
import java.util.Random;
import java.util.function.IntPredicate;

public final class NoTrueValue {
    static int firstTrue(int n, IntPredicate test) {
        int lo = 0, hi = n;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (test.test(mid)) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }

    static int linear(int n, IntPredicate test) {
        for (int i = 0; i < n; i++) if (test.test(i)) return i;
        return n;
    }

    public static void main(String[] args) {
        if (firstTrue(5, i -> i >= 3) != 3) throw new AssertionError("example 1");
        if (firstTrue(4, i -> false) != 4) throw new AssertionError("example 2");
        if (firstTrue(0, i -> true) != 0) throw new AssertionError("empty domain");
        Random random = new Random(6004);
        for (int trial = 0; trial < 800; trial++) {
            int n = random.nextInt(200);
            int boundary = random.nextInt(n + 1);
            IntPredicate test = i -> i >= boundary;
            if (firstTrue(n, test) != linear(n, test)) throw new AssertionError("boundary=" + boundary);
        }
    }
}
```

#### Solution: [Recognize] Kth Missing Positive Number (LeetCode 1539)
<!-- id: bs-kth-missing-positive -->

**Approach.** Before `arr[i]`, exactly `arr[i] - (i + 1)` positive integers are missing. This count never decreases, so find the first index where it is at least `k`. If `lo` stored values occur before the answer, the `k` missing values and those `lo` present values place the answer at `lo + k`.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class KthMissingPositive {
    static int findKthPositive(int[] arr, int k) {
        int lo = 0, hi = arr.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            int missingThroughMid = arr[mid] - (mid + 1);
            if (missingThroughMid >= k) hi = mid;
            else lo = mid + 1;
        }
        return lo + k;
    }

    static int brute(int[] arr, int k) {
        int index = 0;
        for (int value = 1; ; value++) {
            if (index < arr.length && arr[index] == value) index++;
            else if (--k == 0) return value;
        }
    }

    public static void main(String[] args) {
        if (findKthPositive(new int[] {2, 5, 6, 9}, 4) != 7) throw new AssertionError("example 1");
        if (findKthPositive(new int[] {1, 2, 4}, 5) != 8) throw new AssertionError("example 2");
        Random random = new Random(1539);
        for (int trial = 0; trial < 800; trial++) {
            int[] arr = new int[1 + random.nextInt(35)];
            int value = 0;
            for (int i = 0; i < arr.length; i++) {
                value += 1 + random.nextInt(4);
                arr[i] = value;
            }
            int k = 1 + random.nextInt(50);
            int actual = findKthPositive(arr, k);
            int expected = brute(arr, k);
            if (actual != expected) {
                throw new AssertionError(Arrays.toString(arr) + " k=" + k + " actual=" + actual + " expected=" + expected);
            }
        }
    }
}
```
