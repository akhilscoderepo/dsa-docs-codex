<!-- solutions-for: 07-array-cycle-state -->
### Array Cycle State Solutions

#### Solution: [Build] Follow Links (Author exercise)
<!-- id: tp-follow-links -->

**Approach.** Store the current index and replace it with `next[current]` exactly once per requested step.

**Complexity.** O(steps) time and O(1) space.

```java run
public final class TpLinks {static int f(int[]n,int s){int at=0;while(s-->0)at=n[at];return at;}public static void main(String[]z){if(f(new int[]{1,2,0},4)!=1||f(new int[]{0},7)!=0)throw new AssertionError();}}
```

#### Solution: [Vary] Find The Duplicate Number (LeetCode 287)
<!-- id: tp-find-duplicate -->

**Approach.** Find a meeting with one-step and two-step movement, then reset one pointer to the first value and move both one step to the entry.

**Complexity.** O(n) time and O(1) auxiliary space.

```java run
public final class TpDup {static int f(int[]a){int s=a[0],q=a[0];do{s=a[s];q=a[a[q]];}while(s!=q);s=a[0];while(s!=q){s=a[s];q=a[q];}return s;}public static void main(String[]z){if(f(new int[]{1,3,4,2,2})!=2||f(new int[]{3,1,3,4,2})!=3)throw new AssertionError();}}
```

#### Solution: [Boundary] Immediate Cycle (Author exercise)
<!-- id: tp-immediate-array-cycle -->

**Approach.** Use the standard do-while phase so even a self-cycle performs valid movement before comparison.

**Complexity.** O(1) time and O(1) space for this fixed-size boundary input.

```java run
public final class TpImmediate {static int f(int[]a){int s=a[0],q=a[0];do{s=a[s];q=a[a[q]];}while(s!=q);s=a[0];while(s!=q){s=a[s];q=a[q];}return s;}public static void main(String[]z){int[]a={1,1},copy=a.clone();if(f(a)!=1||!java.util.Arrays.equals(a,copy))throw new AssertionError();}}
```

#### Solution: [Recognize] Duplicate Entry Proof (Author exercise)
<!-- id: tp-duplicate-entry-proof -->

**Approach.** Starting from the supplied meeting and `nums[0]`, move equally until entry and return both the index and move count.

**Complexity.** O(n) time and O(1) space.

```java run
public final class TpEntryProof {static int[]f(int[]a,int meet){int x=a[0],m=0;while(x!=meet){x=a[x];meet=a[meet];m++;}return new int[]{x,m};}public static void main(String[]z){int[]p=f(new int[]{1,3,4,2,2},2);if(p[0]!=2||p[1]!=2)throw new AssertionError();int[]q=f(new int[]{1,1},1);if(q[0]!=1||q[1]!=0)throw new AssertionError();}}
```
