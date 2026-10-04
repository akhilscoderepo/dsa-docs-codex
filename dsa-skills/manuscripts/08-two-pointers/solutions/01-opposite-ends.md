<!-- solutions-for: 01-opposite-ends -->
### Opposite Ends Solutions

#### Solution: [Build] Two Sum II (LeetCode 167)
<!-- id: tp-two-sum-ii -->

**Approach.** Scan inward from both ends. A small sum eliminates the left endpoint; a large sum eliminates the right endpoint. Return one-based positions when equality is reached.

**Complexity.** O(n) time and O(1) auxiliary space.

```java run
public final class TpTwoSumII {
 static int[] solve(int[] a,int t){int l=0,r=a.length-1;while(l<r){long s=(long)a[l]+a[r];if(s==t)return new int[]{l+1,r+1};if(s<t)l++;else r--;}throw new IllegalArgumentException();}
 public static void main(String[] z){int[] x=solve(new int[]{1,3,4,6,8,11},10);if(x[0]!=3||x[1]!=4)throw new AssertionError();int[] y=solve(new int[]{-5,-2,7,12},5);if(y[0]!=2||y[1]!=3)throw new AssertionError();}
}
```

#### Solution: [Vary] Closest Pair Sum (Author exercise)
<!-- id: tp-closest-pair-sum -->

**Approach.** Measure every endpoint pair before moving. Replace the saved pair on a smaller distance or a lexicographically smaller tie, then move by the ordinary sum comparison.

**Complexity.** O(n) time and O(1) space besides the answer.

```java run
public final class TpClosestPair {
 static int[] solve(int[]a,int t){int l=0,r=a.length-1,bl=l,br=r;long bd=Long.MAX_VALUE;while(l<r){long s=(long)a[l]+a[r],d=Math.abs(s-t);if(d<bd||(d==bd&&(a[l]<a[bl]||(a[l]==a[bl]&&a[r]<a[br])))){bd=d;bl=l;br=r;}if(s<t)l++;else r--;}return new int[]{a[bl],a[br]};}
 public static void main(String[]z){if(!java.util.Arrays.equals(solve(new int[]{1,4,7,10},12),new int[]{1,10}))throw new AssertionError();if(!java.util.Arrays.equals(solve(new int[]{-8,-3,2,9},0),new int[]{-8,9}))throw new AssertionError();}
}
```

#### Solution: [Boundary] Two Values (Author exercise)
<!-- id: tp-two-values -->

**Approach.** The only candidate uses both elements. Widen the first operand before adding so Java performs the sum as a `long`.

**Complexity.** O(1) time and O(1) space.

```java run
public final class TpTwoValues {
 static boolean solve(int[]a,int t){return (long)a[0]+a[1]==t;}
 public static void main(String[]z){if(!solve(new int[]{4,4},8))throw new AssertionError();if(solve(new int[]{Integer.MAX_VALUE,Integer.MAX_VALUE},-2))throw new AssertionError();}
}
```

#### Solution: [Recognize] Container With Most Water (LeetCode 11)
<!-- id: tp-container-water -->

**Approach.** Measure the current container, then move the shorter wall. Keeping that wall while reducing width cannot improve its limiting height, whereas replacing it might.

**Complexity.** O(n) time and O(1) extra space.

```java run
public final class TpContainer {
 static int solve(int[]h){int l=0,r=h.length-1,b=0;while(l<r){b=Math.max(b,(r-l)*Math.min(h[l],h[r]));if(h[l]<=h[r])l++;else r--;}return b;}
 public static void main(String[]z){if(solve(new int[]{1,8,6,2,5,4,8,3,7})!=49)throw new AssertionError();if(solve(new int[]{1,1})!=1)throw new AssertionError();}
}
```
