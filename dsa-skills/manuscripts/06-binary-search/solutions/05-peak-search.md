<!-- solutions-for: 05-peak-search -->
### Peak Search Solutions

#### Solution: [Build] Peak Index In A Mountain Array (LeetCode 852)
<!-- id: bs-peak-index-mountain -->

**Approach.** Keep a closed interval containing the mountain's unique peak. A rising edge puts the peak strictly to the right of `mid`; a falling edge keeps `mid` as a possible peak and removes positions to its right. The single remaining index is the turning point.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.Random;

public final class PeakIndexMountain {
    static int peakIndex(int[] arr) {
        int lo = 0, hi = arr.length - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (arr[mid] < arr[mid + 1]) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }

    static int linear(int[] arr) {
        int best = 0;
        for (int i = 1; i < arr.length; i++) if (arr[i] > arr[best]) best = i;
        return best;
    }

    public static void main(String[] args) {
        if (peakIndex(new int[] {0, 3, 7, 12, 9, 2}) != 3) throw new AssertionError("example 1");
        if (peakIndex(new int[] {2, 10, 6}) != 1) throw new AssertionError("example 2");
        Random random = new Random(852);
        for (int trial = 0; trial < 800; trial++) {
            int n = 3 + random.nextInt(80);
            int peak = 1 + random.nextInt(n - 2);
            int[] arr = new int[n];
            for (int i = 1; i <= peak; i++) arr[i] = arr[i - 1] + 1 + random.nextInt(5);
            for (int i = peak + 1; i < n; i++) arr[i] = arr[i - 1] - 1 - random.nextInt(5);
            if (peakIndex(arr) != linear(arr)) throw new AssertionError("peak=" + peak);
        }
    }
}
```

#### Solution: [Vary] Find Any Peak Element (LeetCode 162)
<!-- id: bs-find-any-peak -->

**Approach.** Preserve an interval containing at least one peak. On a rising edge, an acceptable peak must occur to the right. Otherwise `mid` or a position to its left supplies one. The returned index need only satisfy the local peak condition.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.Random;

public final class FindAnyPeak {
    static int findPeak(int[] nums) {
        int lo = 0, hi = nums.length - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] < nums[mid + 1]) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }

    static boolean isPeak(int[] nums, int index) {
        return (index == 0 || nums[index] > nums[index - 1])
                && (index + 1 == nums.length || nums[index] > nums[index + 1]);
    }

    public static void main(String[] args) {
        int[] first = {2, 7, 4, 1, 8, 5};
        if (!isPeak(first, findPeak(first))) throw new AssertionError("example 1");
        if (findPeak(new int[] {9}) != 0) throw new AssertionError("example 2");
        Random random = new Random(162);
        for (int trial = 0; trial < 1000; trial++) {
            int n = 1 + random.nextInt(100);
            int[] nums = new int[n];
            nums[0] = random.nextInt(21) - 10;
            for (int i = 1; i < n; i++) {
                do nums[i] = random.nextInt(201) - 100; while (nums[i] == nums[i - 1]);
            }
            int index = findPeak(nums);
            if (!isPeak(nums, index)) throw new AssertionError("invalid peak at " + index);
        }
    }
}
```

#### Solution: [Boundary] Endpoint Peak (Author exercise)
<!-- id: bs-endpoint-peak -->

**Approach.** Use the ordinary slope search without endpoint cases. Every rising comparison removes its left endpoint, so a fully increasing input converges on `n - 1`. Every falling comparison keeps the midpoint and left side, so a decreasing input converges on zero.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.Random;

public final class EndpointPeak {
    static int findPeak(int[] nums) {
        int lo = 0, hi = nums.length - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] < nums[mid + 1]) lo = mid + 1;
            else hi = mid;
        }
        return lo;
    }

    public static void main(String[] args) {
        if (findPeak(new int[] {1, 3, 6, 10}) != 3) throw new AssertionError("example 1");
        if (findPeak(new int[] {10, 6, 3, 1}) != 0) throw new AssertionError("example 2");
        if (findPeak(new int[] {4}) != 0) throw new AssertionError("single");
        Random random = new Random(605);
        for (int trial = 0; trial < 600; trial++) {
            int n = 1 + random.nextInt(100);
            int[] increasing = new int[n];
            int[] decreasing = new int[n];
            for (int i = 1; i < n; i++) increasing[i] = increasing[i - 1] + 1 + random.nextInt(8);
            for (int i = 1; i < n; i++) decreasing[i] = decreasing[i - 1] - 1 - random.nextInt(8);
            if (findPeak(increasing) != n - 1) throw new AssertionError("increasing n=" + n);
            if (findPeak(decreasing) != 0) throw new AssertionError("decreasing n=" + n);
        }
    }
}
```

#### Solution: [Recognize] Find In Mountain Array (LeetCode 1095)
<!-- id: bs-find-in-mountain-array -->

**Approach.** Locate the peak with adjacent comparisons, caching both reads made in each iteration. Search the increasing interval first with ordinary ascending comparisons. If it misses, search the strictly decreasing interval with reversed movement rules; searching the left slope first guarantees the smallest matching index.

**Complexity.** O(log n) time, O(log n) interface calls, and O(1) extra space.

```java run
import java.util.Random;

public final class FindInMountainArray {
    interface MountainArray {
        int get(int index);
        int length();
    }

    static final class MeteredMountain implements MountainArray {
        final int[] values;
        int calls;
        MeteredMountain(int[] values) { this.values = values; }
        public int get(int index) { calls++; return values[index]; }
        public int length() { return values.length; }
    }

    static int find(int target, MountainArray mountain) {
        int lo = 0, hi = mountain.length() - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            int middle = mountain.get(mid);
            int next = mountain.get(mid + 1);
            if (middle < next) lo = mid + 1;
            else hi = mid;
        }
        int peak = lo;
        int left = orderedSearch(mountain, target, 0, peak, true);
        return left != -1 ? left : orderedSearch(mountain, target, peak + 1, mountain.length() - 1, false);
    }

    static int orderedSearch(MountainArray mountain, int target, int lo, int hi, boolean ascending) {
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            int value = mountain.get(mid);
            if (value == target) return mid;
            if ((ascending && value < target) || (!ascending && value > target)) lo = mid + 1;
            else hi = mid - 1;
        }
        return -1;
    }

    static int linear(int[] values, int target) {
        for (int i = 0; i < values.length; i++) if (values[i] == target) return i;
        return -1;
    }

    public static void main(String[] args) {
        MeteredMountain first = new MeteredMountain(new int[] {1, 5, 9, 12, 8, 6, 2});
        if (find(6, first) != 5 || first.calls > 100) throw new AssertionError("example 1");
        MeteredMountain second = new MeteredMountain(new int[] {0, 4, 11, 9, 3});
        if (find(7, second) != -1 || second.calls > 100) throw new AssertionError("example 2");
        Random random = new Random(1095);
        for (int trial = 0; trial < 700; trial++) {
            int n = 3 + random.nextInt(200);
            int peak = 1 + random.nextInt(n - 2);
            int[] values = new int[n];
            for (int i = 1; i <= peak; i++) values[i] = values[i - 1] + 1 + random.nextInt(4);
            for (int i = peak + 1; i < n; i++) values[i] = values[i - 1] - 1 - random.nextInt(4);
            int target = random.nextBoolean() ? values[random.nextInt(n)] : random.nextInt(800) - 200;
            MeteredMountain mountain = new MeteredMountain(values);
            int actual = find(target, mountain);
            int expected = linear(values, target);
            if (actual != expected) throw new AssertionError("target=" + target + " actual=" + actual + " expected=" + expected);
            if (mountain.calls > 100) throw new AssertionError("call count=" + mountain.calls);
        }
    }
}
```
