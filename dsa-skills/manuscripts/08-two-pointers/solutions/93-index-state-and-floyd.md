<!-- solutions-for: 93-index-state-and-floyd -->
### Index State And Floyd Solutions

#### Solution: [Build] Value As Next Index (Author exercise)
<!-- id: tp-index-state-path -->

**Approach.** Scan the array once to establish that every value names a legal index. If the representation is valid, allocate the requested output and follow exactly one link for each step, storing index zero before the first move.

**Complexity.** O(n + steps) time and O(steps) output space; traversal itself uses O(1) auxiliary state.

```java run
import java.util.Arrays;
import java.util.Random;

public final class IndexStatePath {
    static int[] path(int[] next, int steps) {
        for (int value : next) {
            if (value < 0 || value >= next.length) return new int[0];
        }
        int[] result = new int[steps + 1];
        int at = 0;
        result[0] = at;
        for (int move = 1; move <= steps; move++) {
            at = next[at];
            result[move] = at;
        }
        return result;
    }

    static int[] oracle(int[] next, int steps) {
        for (int value : next) if (value < 0 || value >= next.length) return new int[0];
        int[] result = new int[steps + 1];
        for (int i = 1; i <= steps; i++) result[i] = next[result[i - 1]];
        return result;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(path(new int[] {2, 0, 3, 1}, 5), new int[] {0, 2, 3, 1, 0, 2})) {
            throw new AssertionError("example 1");
        }
        if (path(new int[] {1, 3}, 2).length != 0) throw new AssertionError("example 2");

        Random random = new Random(8);
        for (int trial = 0; trial < 1000; trial++) {
            int n = 1 + random.nextInt(12);
            int[] next = new int[n];
            for (int i = 0; i < n; i++) next[i] = random.nextInt(n);
            if (trial % 7 == 0) next[random.nextInt(n)] = n;
            int steps = random.nextInt(25);
            if (!Arrays.equals(path(next, steps), oracle(next, steps))) {
                throw new AssertionError("random path");
            }
        }
    }
}
```

#### Solution: [Vary] Find The Duplicate Number (LeetCode 287)
<!-- id: tp-index-state-duplicate -->

**Approach.** Interpret each value as the next index. First use different speeds to obtain a meeting inside the cycle. Reset the slow position to `nums[0]`, then move both positions one edge per round; their next meeting is the cycle entry and therefore the duplicate.

**Complexity.** O(n) time and O(1) auxiliary space. The method does not modify the input.

```java run
import java.util.Random;

public final class IndexStateDuplicate {
    static int findDuplicate(int[] nums) {
        int slow = nums[0], fast = nums[0];
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);
        slow = nums[0];
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }
        return slow;
    }

    static int oracle(int[] nums) {
        int[] count = new int[nums.length];
        for (int value : nums) if (++count[value] > 1) return value;
        throw new AssertionError("invalid generated input");
    }

    static int[] generated(Random random, int n) {
        int duplicate = 1 + random.nextInt(n);
        int[] nums = new int[n + 1];
        for (int i = 0; i < n; i++) nums[i] = i + 1;
        nums[n] = duplicate;
        for (int i = nums.length - 1; i > 0; i--) {
            int j = random.nextInt(i + 1);
            int hold = nums[i]; nums[i] = nums[j]; nums[j] = hold;
        }
        return nums;
    }

    public static void main(String[] args) {
        if (findDuplicate(new int[] {1, 4, 3, 2, 2}) != 2) throw new AssertionError("example 1");
        if (findDuplicate(new int[] {2, 1, 2}) != 2) throw new AssertionError("example 2");

        Random random = new Random(287);
        for (int trial = 0; trial < 2000; trial++) {
            int[] nums = generated(random, 2 + random.nextInt(30));
            int[] copy = nums.clone();
            if (findDuplicate(nums) != oracle(nums)) throw new AssertionError("random duplicate");
            if (!java.util.Arrays.equals(nums, copy)) throw new AssertionError("mutation");
        }
    }
}
```

#### Solution: [Boundary] Duplicate Near Start (Author exercise)
<!-- id: tp-index-state-near-start -->

**Approach.** Count each slow advance in the meeting phase and each equal-speed advance in the entry phase. A do-while loop prevents the initial equality from being mistaken for a discovered meeting, while the second loop may correctly execute zero times.

**Complexity.** O(n) time and O(1) auxiliary space.

```java run
import java.util.Arrays;

public final class NearStartCycle {
    static int[] measure(int[] nums) {
        int slow = nums[0], fast = nums[0], meetingMoves = 0;
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
            meetingMoves++;
        } while (slow != fast);

        slow = nums[0];
        int entryMoves = 0;
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
            entryMoves++;
        }
        return new int[] {slow, meetingMoves, entryMoves};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(measure(new int[] {2, 2, 1}), new int[] {2, 2, 0})) {
            throw new AssertionError("example 1");
        }
        if (!Arrays.equals(measure(new int[] {1, 1}), new int[] {1, 1, 0})) {
            throw new AssertionError("example 2");
        }
        int[] longer = measure(new int[] {1, 4, 3, 2, 2});
        if (longer[0] != 2 || longer[1] <= 0 || longer[2] <= 0) {
            throw new AssertionError("nonzero tail");
        }
    }
}
```

#### Solution: [Recognize] Compare Alternatives (Author exercise)
<!-- id: tp-index-state-alternatives -->

**Approach.** When mutation is forbidden, use Floyd's link-following phases. When mutation is allowed, repeatedly place the value at index zero into the index it names; equality between those two positions reveals the duplicate. The branch is chosen from the caller's contract, not from a runtime performance guess.

**Complexity.** Both branches take O(n) time and O(1) auxiliary space. The Floyd branch preserves the array; the placement branch may reorder it.

```java run
import java.util.Arrays;
import java.util.Random;

public final class DuplicateStrategy {
    static int findDuplicate(int[] nums, boolean mayMutate) {
        if (!mayMutate) return floyd(nums);
        while (nums[0] != nums[nums[0]]) {
            int destination = nums[0];
            int hold = nums[destination];
            nums[destination] = nums[0];
            nums[0] = hold;
        }
        return nums[0];
    }

    static int floyd(int[] nums) {
        int slow = nums[0], fast = nums[0];
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);
        slow = nums[0];
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }
        return slow;
    }

    static int oracle(int[] nums) {
        int[] count = new int[nums.length];
        for (int value : nums) if (++count[value] > 1) return value;
        throw new AssertionError("missing duplicate");
    }

    static int[] generated(Random random, int n) {
        int[] nums = new int[n + 1];
        int duplicate = 1 + random.nextInt(n);
        for (int i = 0; i < n; i++) nums[i] = i + 1;
        nums[n] = duplicate;
        for (int i = nums.length - 1; i > 0; i--) {
            int j = random.nextInt(i + 1);
            int hold = nums[i]; nums[i] = nums[j]; nums[j] = hold;
        }
        return nums;
    }

    public static void main(String[] args) {
        int[] preserved = {1, 4, 3, 2, 2};
        int[] copy = preserved.clone();
        if (findDuplicate(preserved, false) != 2 || !Arrays.equals(preserved, copy)) {
            throw new AssertionError("example 1");
        }
        if (findDuplicate(new int[] {2, 1, 2}, true) != 2) throw new AssertionError("example 2");

        Random random = new Random(808);
        for (int trial = 0; trial < 2000; trial++) {
            int[] source = generated(random, 2 + random.nextInt(30));
            int expected = oracle(source);
            int[] fixed = source.clone();
            if (findDuplicate(fixed, false) != expected || !Arrays.equals(fixed, source)) {
                throw new AssertionError("Floyd contract");
            }
            int[] mutable = source.clone();
            if (findDuplicate(mutable, true) != expected) throw new AssertionError("placement contract");
        }
    }
}
```
