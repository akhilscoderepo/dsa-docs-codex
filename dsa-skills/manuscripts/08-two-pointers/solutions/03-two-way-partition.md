<!-- solutions-for: 03-two-way-partition -->
### Two-Way Partition Solutions

#### Solution: [Build] Sort Array By Parity (LeetCode 905)
<!-- id: tp-sort-parity -->

**Approach.** Move endpoint scans across correctly placed values, then swap the two misplaced values.

**Complexity.** O(n) time and O(1) space.

```java run
public final class TpParity {static int[]f(int[]a){int l=0,r=a.length-1;while(l<r){while(l<r&&(a[l]&1)==0)l++;while(l<r&&(a[r]&1)!=0)r--;int t=a[l];a[l]=a[r];a[r]=t;}return a;}public static void main(String[]z){int[]a=f(new int[]{3,1,2,4});boolean o=false;for(int x:a){if((x&1)!=0)o=true;else if(o)throw new AssertionError();}f(new int[]{2,4});}}
```

#### Solution: [Vary] Partition Around Pivot (Author exercise)
<!-- id: tp-partition-pivot -->

**Approach.** Advance across low values and retreat across high values. Swap stopped endpoints and return `left` after the pointers cross.

**Complexity.** O(n) time and O(1) space.

```java run
public final class TpPivot {static int f(int[]a,int p){int l=0,r=a.length-1;while(l<=r){while(l<=r&&a[l]<p)l++;while(l<=r&&a[r]>=p)r--;if(l<r){int t=a[l];a[l++]=a[r];a[r--]=t;}}return l;}public static void main(String[]z){int[]a={5,1,7,3};if(f(a,4)!=2||f(new int[]{1,2},5)!=2)throw new AssertionError();}}
```

#### Solution: [Boundary] One Empty Region (Author exercise)
<!-- id: tp-empty-region -->

**Approach.** Use the ordinary parity partition and return its final left pointer, which is the even-region size.

**Complexity.** O(n) time and O(1) space.

```java run
public final class TpEmptyRegion {static int f(int[]a){int l=0,r=a.length-1;while(l<=r){while(l<=r&&(a[l]&1)==0)l++;while(l<=r&&(a[r]&1)!=0)r--;if(l<r){int t=a[l];a[l++]=a[r];a[r--]=t;}}return l;}public static void main(String[]z){if(f(new int[]{2,4,6})!=3||f(new int[]{-3,-1})!=0||f(new int[0])!=0)throw new AssertionError();}}
```

#### Solution: [Recognize] Sort Array By Parity II (LeetCode 922)
<!-- id: tp-parity-indices -->

**Approach.** Scan even indices for an odd value and odd indices for an even value. Swap each mismatched pair.

**Complexity.** O(n) time and O(1) auxiliary space.

```java run
public final class TpParityPositions {static int[]f(int[]a){int e=0,o=1;while(e<a.length&&o<a.length){while(e<a.length&&(a[e]&1)==0)e+=2;while(o<a.length&&(a[o]&1)!=0)o+=2;if(e<a.length&&o<a.length){int t=a[e];a[e]=a[o];a[o]=t;}}return a;}public static void main(String[]z){int[]a=f(new int[]{4,2,5,7});for(int i=0;i<a.length;i++)if((a[i]&1)!=(i&1))throw new AssertionError();}}
```
