<!-- solutions-for: 03-lower-and-upper-bounds -->
### Lower And Upper Bounds Solutions

#### Solution: [Build] Search Insert Position (LeetCode 35)
<!-- id: bs-search-insert-position -->

**Approach.** Maintain a half-open interval containing the first value greater than or equal to the target. A midpoint below the target joins the rejected prefix; every other midpoint remains possible and moves the exclusive right endpoint.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SearchInsertPosition {
    static int searchInsert(int[] nums, int target) {
        int lo = 0, hi = nums.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] >= target) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }

    static int linear(int[] nums, int target) {
        int i = 0;
        while (i < nums.length && nums[i] < target) i++;
        return i;
    }

    public static void main(String[] args) {
        if (searchInsert(new int[] {1, 3, 6, 8}, 6) != 2) throw new AssertionError("example 1");
        if (searchInsert(new int[] {1, 3, 6, 8}, 5) != 2) throw new AssertionError("example 2");
        Random random = new Random(35);
        for (int trial = 0; trial < 500; trial++) {
            int[] nums = random.ints(1 + random.nextInt(30), -60, 61).distinct().sorted().toArray();
            int target = random.nextInt(141) - 70;
            if (searchInsert(nums, target) != linear(nums, target)) {
                throw new AssertionError(Arrays.toString(nums) + " target=" + target);
            }
        }
    }
}
```

#### Solution: [Vary] Upper Bound (Author exercise)
<!-- id: bs-upper-bound -->

**Approach.** Search for the first value that satisfies `nums[i] > target`. Equality therefore moves `lo` past the midpoint instead of retaining the midpoint in the possible suffix.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class UpperBound {
    static int upperBound(int[] nums, int target) {
        int lo = 0, hi = nums.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] > target) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }

    static int linear(int[] nums, int target) {
        int i = 0;
        while (i < nums.length && nums[i] <= target) i++;
        return i;
    }

    public static void main(String[] args) {
        if (upperBound(new int[] {1, 3, 3, 7}, 3) != 3) throw new AssertionError("example 1");
        if (upperBound(new int[] {2, 4, 8}, 8) != 3) throw new AssertionError("example 2");
        Random random = new Random(744);
        for (int trial = 0; trial < 500; trial++) {
            int[] nums = random.ints(random.nextInt(35), -12, 13).sorted().toArray();
            int target = random.nextInt(31) - 15;
            if (upperBound(nums, target) != linear(nums, target)) {
                throw new AssertionError(Arrays.toString(nums) + " target=" + target);
            }
        }
    }
}
```

#### Solution: [Boundary] Outside Range (Author exercise)
<!-- id: bs-outside-range -->

**Approach.** Run the same lower-bound helper independently for every query. The half-open interval makes zero, `nums.length`, and zero-length input ordinary outcomes rather than exceptional cases.

**Complexity.** O(q log n) time for `q` queries and O(q) space for the returned array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class OutsideStoredRange {
    static int lowerBound(int[] nums, int target) {
        int lo = 0, hi = nums.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] >= target) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }

    static int[] positions(int[] nums, int[] queries) {
        int[] answer = new int[queries.length];
        for (int i = 0; i < queries.length; i++) answer[i] = lowerBound(nums, queries[i]);
        return answer;
    }

    static int linear(int[] nums, int target) {
        int i = 0;
        while (i < nums.length && nums[i] < target) i++;
        return i;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(positions(new int[] {4, 9, 13}, new int[] {2, 20}), new int[] {0, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(positions(new int[0], new int[] {-5, 5}), new int[] {0, 0})) throw new AssertionError("example 2");
        Random random = new Random(206);
        for (int trial = 0; trial < 400; trial++) {
            int[] nums = random.ints(random.nextInt(30), -20, 21).sorted().toArray();
            int[] queries = random.ints(1 + random.nextInt(12), -25, 26).toArray();
            int[] actual = positions(nums, queries);
            for (int i = 0; i < queries.length; i++) {
                if (actual[i] != linear(nums, queries[i])) throw new AssertionError(Arrays.toString(nums));
            }
        }
    }
}
```

#### Solution: [Recognize] Smallest Greater Letter (LeetCode 744)
<!-- id: bs-smallest-greater-letter -->

**Approach.** Compute the upper bound of `target` in the letter array. When the boundary equals the length, wrap to index zero; otherwise return the letter at the boundary.

**Complexity.** O(log n) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SmallestGreaterLetter {
    static char nextGreatestLetter(char[] letters, char target) {
        int lo = 0, hi = letters.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (letters[mid] > target) hi = mid;
            else lo = mid + 1;
        }
        return letters[lo == letters.length ? 0 : lo];
    }

    static char linear(char[] letters, char target) {
        for (char letter : letters) if (letter > target) return letter;
        return letters[0];
    }

    public static void main(String[] args) {
        if (nextGreatestLetter(new char[] {'c', 'f', 'j'}, 'd') != 'f') throw new AssertionError("example 1");
        if (nextGreatestLetter(new char[] {'b', 'e', 'e', 'k'}, 'k') != 'b') throw new AssertionError("example 2");
        Random random = new Random(744);
        for (int trial = 0; trial < 500; trial++) {
            char[] letters = new char[2 + random.nextInt(25)];
            for (int i = 0; i < letters.length; i++) letters[i] = (char) ('a' + random.nextInt(26));
            Arrays.sort(letters);
            char target = (char) ('a' + random.nextInt(26));
            if (nextGreatestLetter(letters, target) != linear(letters, target)) {
                throw new AssertionError(Arrays.toString(letters) + " target=" + target);
            }
        }
    }
}
```
