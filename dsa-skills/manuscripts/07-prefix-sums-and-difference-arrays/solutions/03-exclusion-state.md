<!-- solutions-for: 03-exclusion-state -->
### Exclusion State

#### Solution: [Build] Sum Except Self (Author exercise)
<!-- id: ps-sum-except-self -->

**Approach.** Compute one `long` total, then subtract the current value for each output. The additive identity gives zero for a one-element input.

**Complexity.** O(n) time and O(n) output space.

```java run
public final class SumExceptExercise {static long[] solve(int[] a){long s=0;for(int x:a)s+=x;long[] r=new long[a.length];for(int i=0;i<a.length;i++)r[i]=s-a[i];return r;}public static void main(String[]z){if(!java.util.Arrays.equals(solve(new int[]{4,-1,2}),new long[]{1,6,3}))throw new AssertionError("example 1");if(!java.util.Arrays.equals(solve(new int[]{9}),new long[]{0}))throw new AssertionError("example 2");}}
```

#### Solution: [Vary] Product of Array Except Self (LeetCode 238)
<!-- id: ps-product-except-self -->

**Approach.** Write strict-left products into the answer, then multiply them by a strict-right product carried backward. Updating after each write keeps the current value excluded.

**Complexity.** O(n) time and O(1) extra space excluding output.

```java run
public final class ProductExercise {static int[] solve(int[]a){int[]r=new int[a.length];int p=1;for(int i=0;i<a.length;i++){r[i]=p;p*=a[i];}p=1;for(int i=a.length-1;i>=0;i--){r[i]*=p;p*=a[i];}return r;}static int[] brute(int[]a){int[]r=new int[a.length];for(int i=0;i<a.length;i++){r[i]=1;for(int j=0;j<a.length;j++)if(i!=j)r[i]*=a[j];}return r;}public static void main(String[]z){if(!java.util.Arrays.equals(solve(new int[]{2,3,5}),new int[]{15,10,6}))throw new AssertionError("example 1");if(!java.util.Arrays.equals(solve(new int[]{-2,4}),new int[]{4,-2}))throw new AssertionError("example 2");var g=new java.util.Random(23);for(int t=0;t<500;t++){int[]a=new int[g.nextInt(6)+2];for(int i=0;i<a.length;i++)a[i]=g.nextInt(5)-2;if(!java.util.Arrays.equals(solve(a),brute(a)))throw new AssertionError("random");}}}
```

#### Solution: [Boundary] Product With Zeros (LeetCode 238)
<!-- id: ps-product-with-zeros -->

**Approach.** Use the same two-pass product algorithm. A zero naturally enters every side that crosses it, while the answer at the zero combines factors that exclude it.

**Complexity.** O(n) time and O(1) auxiliary space beyond output.

```java run
public final class ProductZeroExercise {static int[] solve(int[]a){int[]r=new int[a.length];int p=1;for(int i=0;i<a.length;i++){r[i]=p;p*=a[i];}p=1;for(int i=a.length-1;i>=0;i--){r[i]*=p;p*=a[i];}return r;}public static void main(String[]z){if(!java.util.Arrays.equals(solve(new int[]{3,0,2}),new int[]{0,6,0}))throw new AssertionError("example 1");if(!java.util.Arrays.equals(solve(new int[]{0,5,0}),new int[]{0,0,0}))throw new AssertionError("example 2");}}
```

#### Solution: [Recognize] Prefix And Suffix Maximums (Author exercise)
<!-- id: ps-prefix-suffix-maximums -->

**Approach.** Walk forward writing the maximum seen before each position, then backward doing the same for the right side. Absorb the current value only after writing its strict-side result.

**Complexity.** O(n) time and O(n) space for the two returned arrays.

```java run
public final class SideMaximumExercise {record Sides(long[]left,long[]right){}static Sides solve(int[]a){long[]l=new long[a.length],r=new long[a.length];long m=Long.MIN_VALUE;for(int i=0;i<a.length;i++){l[i]=m;m=Math.max(m,a[i]);}m=Long.MIN_VALUE;for(int i=a.length-1;i>=0;i--){r[i]=m;m=Math.max(m,a[i]);}return new Sides(l,r);}public static void main(String[]z){var x=solve(new int[]{3,1,5});if(!java.util.Arrays.equals(x.left(),new long[]{Long.MIN_VALUE,3,3})||!java.util.Arrays.equals(x.right(),new long[]{5,5,Long.MIN_VALUE}))throw new AssertionError("example 1");var y=solve(new int[]{7});if(y.left()[0]!=Long.MIN_VALUE||y.right()[0]!=Long.MIN_VALUE)throw new AssertionError("example 2");}}
```
