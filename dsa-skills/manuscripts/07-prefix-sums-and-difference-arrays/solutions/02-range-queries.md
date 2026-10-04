<!-- solutions-for: 02-range-queries -->
### Range Queries

#### Solution: [Build] Range Sum Query Immutable (LeetCode 303)
<!-- id: ps-range-sum-immutable -->

**Approach.** Store sentinel prefix totals during construction. An inclusive query subtracts the boundary before `left` from the boundary after `right`.

**Complexity.** O(n) construction, O(1) per query, and O(n) space.

```java run
public final class ImmutableSumExercise {
    final long[] p; ImmutableSumExercise(int[] a){p=new long[a.length+1];for(int i=0;i<a.length;i++)p[i+1]=p[i]+a[i];}
    long sum(int l,int r){return p[r+1]-p[l];}
    public static void main(String[] z){var x=new ImmutableSumExercise(new int[]{3,-2,5,1});if(x.sum(1,3)!=4)throw new AssertionError("example 1");var y=new ImmutableSumExercise(new int[]{8});if(y.sum(0,0)!=8)throw new AssertionError("example 2");}
}
```

#### Solution: [Vary] Half-Open Query (Author exercise)
<!-- id: ps-half-open-query -->

**Approach.** A half-open request already names its two prefix boundaries, so subtract `prefix[left]` from `prefix[right]`. Equal boundaries cancel to zero.

**Complexity.** O(n) preprocessing, O(1) per query, and O(n) space.

```java run
public final class HalfOpenExercise {
    final long[] p; HalfOpenExercise(int[] a){p=new long[a.length+1];for(int i=0;i<a.length;i++)p[i+1]=p[i]+a[i];}
    long sum(int l,int r){return p[r]-p[l];}
    public static void main(String[] z){var x=new HalfOpenExercise(new int[]{6,2,-3,4});if(x.sum(1,4)!=3)throw new AssertionError("example 1");if(x.sum(1,1)!=0)throw new AssertionError("example 2");}
}
```

#### Solution: [Boundary] Whole Array (Author exercise)
<!-- id: ps-whole-array-query -->

**Approach.** The whole array lies between boundaries zero and `n`. Building the sentinel table also makes the empty case `prefix[0] - prefix[0]`.

**Complexity.** O(n) construction, O(1) query time, and O(n) space.

```java run
public final class WholeRangeExercise {
    static long solve(int[] a){long[] p=new long[a.length+1];for(int i=0;i<a.length;i++)p[i+1]=p[i]+a[i];return p[a.length]-p[0];}
    public static void main(String[] z){if(solve(new int[]{2,-5,9})!=6)throw new AssertionError("example 1");if(solve(new int[]{})!=0)throw new AssertionError("example 2");}
}
```

#### Solution: [Recognize] XOR Queries of a Subarray (LeetCode 1310)
<!-- id: ps-xor-range-query -->

**Approach.** Build a sentinel XOR prefix. Equal earlier bits cancel because `x ^ x` is zero, so each answer is `prefix[right + 1] ^ prefix[left]`.

**Complexity.** O(n + q) time and O(n) auxiliary space excluding answers.

```java run
public final class XorQueryExercise {
    static int[] solve(int[] a,int[][] q){int[] p=new int[a.length+1];for(int i=0;i<a.length;i++)p[i+1]=p[i]^a[i];int[] r=new int[q.length];for(int i=0;i<q.length;i++)r[i]=p[q[i][1]+1]^p[q[i][0]];return r;}
    static int[] brute(int[] a,int[][] q){int[] r=new int[q.length];for(int i=0;i<q.length;i++)for(int j=q[i][0];j<=q[i][1];j++)r[i]^=a[j];return r;}
    public static void main(String[] z){if(!java.util.Arrays.equals(solve(new int[]{5,1,7},new int[][]{{0,1},{1,2}}),new int[]{4,6}))throw new AssertionError("example 1");if(!java.util.Arrays.equals(solve(new int[]{9},new int[][]{{0,0}}),new int[]{9}))throw new AssertionError("example 2");var g=new java.util.Random(17);for(int t=0;t<400;t++){int n=g.nextInt(7)+1;int[] a=new int[n];for(int i=0;i<n;i++)a[i]=g.nextInt(16);int[][] q={{g.nextInt(n),0}};q[0][1]=q[0][0]+g.nextInt(n-q[0][0]);if(!java.util.Arrays.equals(solve(a,q),brute(a,q)))throw new AssertionError("random");}}
}
```
