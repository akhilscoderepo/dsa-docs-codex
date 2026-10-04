<!-- solutions-for: 07-prefix-xor -->
### Prefix XOR

#### Solution: [Build] XOR Queries of a Subarray (LeetCode 1310)
<!-- id: ps-xor-range-queries -->

**Approach.** Store the XOR before each boundary. For query `[left, right]`, XOR the boundary after `right` with the boundary before `left`; their shared history cancels.

**Complexity.** O(n + q) time and O(n) extra space.

```java run
import java.util.Arrays;
public final class XorRangeQueries {
    static int[] solve(int[] arr, int[][] queries) {
        int[] prefix = new int[arr.length + 1];
        for (int i = 0; i < arr.length; i++) prefix[i + 1] = prefix[i] ^ arr[i];
        int[] answer = new int[queries.length];
        for (int i = 0; i < queries.length; i++) {
            answer[i] = prefix[queries[i][1] + 1] ^ prefix[queries[i][0]];
        }
        return answer;
    }
    static int brute(int[] a, int left, int right) {
        int value = 0;
        for (int i = left; i <= right; i++) value ^= a[i];
        return value;
    }
    public static void main(String[] args) {
        if (!Arrays.equals(solve(new int[] {6,2,9,4}, new int[][] {{0,1},{1,3}}), new int[] {4,15})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[] {12}, new int[][] {{0,0}}), new int[] {12})) throw new AssertionError("example 2");
        var random = new java.util.Random(71);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[random.nextInt(8) + 1];
            for (int i = 0; i < a.length; i++) a[i] = random.nextInt(32);
            int left = random.nextInt(a.length), right = left + random.nextInt(a.length - left);
            int actual = solve(a, new int[][] {{left, right}})[0];
            if (actual != brute(a, left, right)) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Vary] Count XOR K (Author exercise)
<!-- id: ps-count-xor-k -->

**Approach.** Let `prefix` be the XOR through the current value. An earlier state must equal `prefix ^ k` for the intervening subarray to have XOR `k`. Add its frequency before recording the current state, with zero seeded once.

**Complexity.** O(n) expected time and O(n) space.

```java run
import java.util.HashMap;
import java.util.Map;
public final class CountXorK {
    static long solve(int[] nums, int k) {
        Map<Integer, Long> frequency = new HashMap<>();
        frequency.put(0, 1L);
        int prefix = 0;
        long answer = 0;
        for (int value : nums) {
            prefix ^= value;
            answer += frequency.getOrDefault(prefix ^ k, 0L);
            frequency.merge(prefix, 1L, Long::sum);
        }
        return answer;
    }
    static long brute(int[] nums, int k) {
        long answer = 0;
        for (int left = 0; left < nums.length; left++) {
            int value = 0;
            for (int right = left; right < nums.length; right++) {
                value ^= nums[right];
                if (value == k) answer++;
            }
        }
        return answer;
    }
    public static void main(String[] args) {
        if (solve(new int[] {4,2,2,6}, 6) != 3) throw new AssertionError("example 1");
        if (solve(new int[] {0,0}, 0) != 3) throw new AssertionError("example 2");
        var random = new java.util.Random(72);
        for (int t = 0; t < 700; t++) {
            int[] a = new int[random.nextInt(9)];
            for (int i = 0; i < a.length; i++) a[i] = random.nextInt(16);
            int k = random.nextInt(16);
            if (solve(a, k) != brute(a, k)) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Boundary] Empty Prefix (Author exercise)
<!-- id: ps-xor-empty-prefix -->

**Approach.** Allocate one extra prefix entry and leave entry zero at the XOR identity. A query ending at `right` is `prefix[right + 1] ^ prefix[0]`, so it needs no exceptional branch.

**Complexity.** O(n + q) time and O(n + q) space including the returned answers.

```java run
import java.util.Arrays;
public final class XorEmptyPrefix {
    record Result(int[] answers, int sentinel) {}
    static Result solve(int[] nums, int[] rights) {
        int[] prefix = new int[nums.length + 1];
        for (int i = 0; i < nums.length; i++) prefix[i + 1] = prefix[i] ^ nums[i];
        int[] answers = new int[rights.length];
        for (int i = 0; i < rights.length; i++) answers[i] = prefix[rights[i] + 1] ^ prefix[0];
        return new Result(answers, prefix[0]);
    }
    public static void main(String[] args) {
        Result first = solve(new int[] {7,3,5}, new int[] {0,2});
        if (!Arrays.equals(first.answers(), new int[] {7,1}) || first.sentinel() != 0) throw new AssertionError("example 1");
        Result second = solve(new int[] {0}, new int[] {0});
        if (!Arrays.equals(second.answers(), new int[] {0}) || second.sentinel() != 0) throw new AssertionError("example 2");
    }
}
```

#### Solution: [Recognize] Count Triplets With Equal XOR (LeetCode 1442)
<!-- id: ps-xor-equal-triplets -->

**Approach.** Compute all prefix XOR states. When the boundaries at `i` and `k + 1` are equal, `arr[i..k]` has XOR zero. Every `j` from `i + 1` through `k` then splits that range into equal-XOR halves, contributing `k - i` triples.

**Complexity.** O(n^2) time and O(n) space.

```java run
public final class EqualXorTriplets {
    static int solve(int[] arr) {
        int[] prefix = new int[arr.length + 1];
        for (int i = 0; i < arr.length; i++) prefix[i + 1] = prefix[i] ^ arr[i];
        int answer = 0;
        for (int i = 0; i < arr.length; i++) {
            for (int k = i + 1; k < arr.length; k++) {
                if (prefix[i] == prefix[k + 1]) answer += k - i;
            }
        }
        return answer;
    }
    static int brute(int[] arr) {
        int answer = 0;
        for (int i = 0; i < arr.length; i++) for (int j = i + 1; j < arr.length; j++) for (int k = j; k < arr.length; k++) {
            int left = 0, right = 0;
            for (int x = i; x < j; x++) left ^= arr[x];
            for (int x = j; x <= k; x++) right ^= arr[x];
            if (left == right) answer++;
        }
        return answer;
    }
    public static void main(String[] args) {
        if (solve(new int[] {1,1,1}) != 2) throw new AssertionError("example 1");
        if (solve(new int[] {5}) != 0) throw new AssertionError("example 2");
        var random = new java.util.Random(73);
        for (int t = 0; t < 300; t++) {
            int[] a = new int[random.nextInt(7) + 1];
            for (int i = 0; i < a.length; i++) a[i] = random.nextInt(8) + 1;
            if (solve(a) != brute(a)) throw new AssertionError("random");
        }
    }
}
```
