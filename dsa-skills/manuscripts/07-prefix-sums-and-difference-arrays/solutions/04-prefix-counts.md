<!-- solutions-for: 04-prefix-counts -->
### Prefix Counts

#### Solution: [Build] Subarray Sum Equals K (LeetCode 560)
<!-- id: ps-subarray-sum-k -->

**Approach.** Seed prefix zero, then for each current total count earlier totals equal to `current - k`. Insert current only after lookup.

**Complexity.** O(n) expected time and O(n) space.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;
public final class SumKExercise {
    static long solve(int[] a, long k) {
        Map<Long, Integer> frequency = new HashMap<>();
        frequency.put(0L, 1);
        long prefix = 0, count = 0;
        for (int value : a) {
            prefix += value;
            count += frequency.getOrDefault(prefix - k, 0);
            frequency.merge(prefix, 1, Integer::sum);
        }
        return count;
    }
    static long brute(int[] a, long k) {
        long count = 0;
        for (int left = 0; left < a.length; left++) {
            long sum = 0;
            for (int right = left; right < a.length; right++) {
                sum += a[right];
                if (sum == k) count++;
            }
        }
        return count;
    }
    public static void main(String[] args) {
        if (solve(new int[] {2, -1, 2}, 3) != 1) throw new AssertionError("example 1");
        if (solve(new int[] {0, 0}, 0) != 3) throw new AssertionError("example 2");
        Random random = new Random(29);
        for (int t = 0; t < 700; t++) {
            int[] a = new int[random.nextInt(8)];
            for (int i = 0; i < a.length; i++) a[i] = random.nextInt(7) - 3;
            long k = random.nextInt(9) - 4;
            if (solve(a, k) != brute(a, k)) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Vary] Binary Subarrays With Sum (LeetCode 930)
<!-- id: ps-binary-subarrays-sum -->

**Approach.** Apply the same frequency equation to the binary prefix sum. Zeros create repeated prefix totals, so every occurrence remains in the count.

**Complexity.** O(n) time and O(n) space.

```java run
public final class BinarySumExercise{static long solve(int[]a,int goal){int[]f=new int[a.length+1];f[0]=1;int p=0;long c=0;for(int x:a){p+=x;if(p>=goal)c+=f[p-goal];f[p]++;}return c;}public static void main(String[]z){if(solve(new int[]{1,0,1,0},2)!=2)throw new AssertionError("example 1");if(solve(new int[]{0,0,0},0)!=6)throw new AssertionError("example 2");}}
```

#### Solution: [Boundary] Zero Target (Author exercise)
<!-- id: ps-zero-target-count -->

**Approach.** Count earlier equal prefixes before inserting the current boundary. Track the greatest stored frequency after each merge, beginning with the seeded zero frequency of one.

**Complexity.** O(n) expected time and O(n) space.

```java run
import java.util.HashMap;
import java.util.Map;
public final class ZeroTargetExercise {
    record Result(long count, int maxFrequency) {}
    static Result solve(int[] a) {
        Map<Long, Integer> frequency = new HashMap<>();
        frequency.put(0L, 1);
        long prefix = 0, count = 0;
        int maximum = 1;
        for (int value : a) {
            prefix += value;
            count += frequency.getOrDefault(prefix, 0);
            int stored = frequency.merge(prefix, 1, Integer::sum);
            maximum = Math.max(maximum, stored);
        }
        return new Result(count, maximum);
    }
    public static void main(String[] args) {
        Result first = solve(new int[] {1, -1, 1, -1});
        if (first.count() != 4 || first.maxFrequency() != 3) throw new AssertionError("example 1");
        Result second = solve(new int[] {});
        if (second.count() != 0 || second.maxFrequency() != 1) throw new AssertionError("example 2");
    }
}
```

#### Solution: [Recognize] Count Number of Nice Subarrays (LeetCode 1248)
<!-- id: ps-nice-subarrays -->

**Approach.** Add one for an odd value and zero for an even value. Count earlier transformed prefixes equal to `oddCount - k`.

**Complexity.** O(n) time and O(n) space.

```java run
public final class NiceExercise{static long solve(int[]a,int k){int[]f=new int[a.length+1];f[0]=1;int p=0;long c=0;for(int x:a){p+=(x&1);if(p>=k)c+=f[p-k];f[p]++;}return c;}static long brute(int[]a,int k){long c=0;for(int i=0;i<a.length;i++){int o=0;for(int j=i;j<a.length;j++){o+=a[j]&1;if(o==k)c++;}}return c;}public static void main(String[]z){if(solve(new int[]{2,1,2,3},2)!=2)throw new AssertionError("example 1");if(solve(new int[]{2,4,6},1)!=0)throw new AssertionError("example 2");}}
```
