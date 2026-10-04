<!-- solutions-for: 01-prefix-construction -->
### Prefix Construction

#### Solution: [Build] Running Sum of 1d Array (LeetCode 1480)
<!-- id: ps-running-sum -->

**Approach.** Copy each inclusive cumulative total into the result. A `long` running sum prevents intermediate overflow under the stated exercise contract.

**Complexity.** O(n) time and O(n) output space.

```java run
public final class RunningSumExercise {
    static long[] solve(int[] a){ long[] r=new long[a.length]; long s=0; for(int i=0;i<a.length;i++) r[i]=s+=a[i]; return r; }
    public static void main(String[] z){
        if(!java.util.Arrays.equals(solve(new int[]{2,5,-1}),new long[]{2,7,6}))throw new AssertionError("example 1");
        if(!java.util.Arrays.equals(solve(new int[]{0}),new long[]{0}))throw new AssertionError("example 2");
    }
}
```

#### Solution: [Vary] Find Pivot Index (LeetCode 724)
<!-- id: ps-pivot-index -->

**Approach.** Compute the total once. At index `i`, the right sum is `total - left - nums[i]`; test it before adding the current value to `left` so both sides exclude the pivot.

**Complexity.** O(n) time and O(1) auxiliary space.

```java run
public final class PivotExercise {
    static int solve(int[] a){long total=0,left=0;for(int x:a)total+=x;for(int i=0;i<a.length;i++){if(left==total-left-a[i])return i;left+=a[i];}return -1;}
    static int brute(int[] a){for(int i=0;i<a.length;i++){long l=0,r=0;for(int j=0;j<i;j++)l+=a[j];for(int j=i+1;j<a.length;j++)r+=a[j];if(l==r)return i;}return -1;}
    public static void main(String[] z){if(solve(new int[]{2,1,-1})!=0)throw new AssertionError("example 1");if(solve(new int[]{1,2,3})!=-1)throw new AssertionError("example 2");var q=new java.util.Random(7);for(int t=0;t<1000;t++){int[] a=new int[q.nextInt(8)+1];for(int i=0;i<a.length;i++)a[i]=q.nextInt(9)-4;if(solve(a)!=brute(a))throw new AssertionError("random");}}
}
```

#### Solution: [Boundary] Empty Prefix (Author exercise)
<!-- id: ps-empty-prefix -->

**Approach.** Allocate one cell per boundary and leave cell zero at its initialized value. Each input extends the previous boundary total.

**Complexity.** O(n) time and O(n) output space.

```java run
public final class EmptyPrefixExercise {
    static long[] solve(int[] a){long[] p=new long[a.length+1];for(int i=0;i<a.length;i++)p[i+1]=p[i]+a[i];return p;}
    public static void main(String[] z){if(!java.util.Arrays.equals(solve(new int[]{}),new long[]{0}))throw new AssertionError("example 1");if(!java.util.Arrays.equals(solve(new int[]{-4,4}),new long[]{0,-4,0}))throw new AssertionError("example 2");}
}
```

#### Solution: [Recognize] Prefix Averages (Author exercise)
<!-- id: ps-prefix-averages -->

**Approach.** Extend one `long` total and apply `Math.floorDiv(total, length)` at every index. Unlike `/`, `floorDiv` rounds a negative fractional result toward negative infinity.

**Complexity.** O(n) time and O(n) output space.

```java run
public final class PrefixAveragesExercise {
    static long[] solve(int[] a){long[] r=new long[a.length];long s=0;for(int i=0;i<a.length;i++){s+=a[i];r[i]=Math.floorDiv(s,i+1L);}return r;}
    static long[] brute(int[] a){long[] r=new long[a.length];for(int i=0;i<a.length;i++){long s=0;for(int j=0;j<=i;j++)s+=a[j];r[i]=Math.floorDiv(s,i+1L);}return r;}
    public static void main(String[] z){if(!java.util.Arrays.equals(solve(new int[]{5,1,6}),new long[]{5,3,4}))throw new AssertionError("example 1");if(!java.util.Arrays.equals(solve(new int[]{-1,0}),new long[]{-1,-1}))throw new AssertionError("example 2");var q=new java.util.Random(11);for(int t=0;t<500;t++){int[] a=new int[q.nextInt(9)+1];for(int i=0;i<a.length;i++)a[i]=q.nextInt(21)-10;if(!java.util.Arrays.equals(solve(a),brute(a)))throw new AssertionError("random");}}
}
```

