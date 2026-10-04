<!-- solutions-for: 06-k-sum-reduction -->
### K-Sum Reduction Solutions

#### Solution: [Build] 3Sum (LeetCode 15)
<!-- id: tp-k-three-sum -->

**Approach.** Sort, choose one nonrepeated fixed value, and search its suffix for the negated pair target.

**Complexity.** O(n²) time and O(1) auxiliary space apart from output.

```java run
import java.util.*;
public final class TpK3 {static int f(int[]a){Arrays.sort(a);int c=0;for(int i=0;i<a.length-2;i++){if(i>0&&a[i]==a[i-1])continue;int l=i+1,r=a.length-1;while(l<r){long s=(long)a[i]+a[l]+a[r];if(s==0){c++;int x=a[l],y=a[r];while(l<r&&a[l]==x)l++;while(l<r&&a[r]==y)r--;}else if(s<0)l++;else r--;}}return c;}public static void main(String[]z){if(f(new int[]{-1,0,1,2,-1,-4})!=2||f(new int[]{1,2,-2,-1})!=0)throw new AssertionError();}}
```

#### Solution: [Vary] 3Sum Closest (LeetCode 16)
<!-- id: tp-three-sum-closest -->

**Approach.** Sort and run one pair scan per fixed value, replacing the saved sum whenever its distance is smaller.

**Complexity.** O(n²) time and O(1) space.

```java run
import java.util.*;
public final class Tp3Close {static int f(int[]a,int t){Arrays.sort(a);long best=(long)a[0]+a[1]+a[2];for(int i=0;i<a.length-2;i++){int l=i+1,r=a.length-1;while(l<r){long s=(long)a[i]+a[l]+a[r];if(Math.abs(s-t)<Math.abs(best-t))best=s;if(s<t)l++;else if(s>t)r--;else return t;}}return(int)best;}public static void main(String[]z){if(f(new int[]{-1,2,1,-4},1)!=2||f(new int[]{0,0,0},1)!=0)throw new AssertionError();}}
```

#### Solution: [Boundary] Overflowing Sum (Author exercise)
<!-- id: tp-overflowing-k-sum -->

**Approach.** Sort, fix two values, and compare a fully widened four-value sum in the final pair scan.

**Complexity.** O(n³) time and O(1) auxiliary space.

```java run
import java.util.*;
public final class TpOverflow4 {static boolean f(int[]a,long t){Arrays.sort(a);for(int i=0;i<a.length-3;i++)for(int j=i+1;j<a.length-2;j++){int l=j+1,r=a.length-1;while(l<r){long s=(long)a[i]+a[j]+a[l]+a[r];if(s==t)return true;if(s<t)l++;else r--;}}return false;}public static void main(String[]z){if(!f(new int[]{Integer.MAX_VALUE,Integer.MAX_VALUE,-1,-1},4294967292L)||f(new int[]{Integer.MAX_VALUE,Integer.MAX_VALUE,0,0},-2))throw new AssertionError();}}
```

#### Solution: [Recognize] 4Sum (LeetCode 18)
<!-- id: tp-k-four-sum -->

**Approach.** Sort, skip duplicates at two fixed depths, and collect unique final pairs using `long` arithmetic.

**Complexity.** O(n³) time and O(1) auxiliary space apart from output.

```java run
import java.util.*;
public final class TpK4 {static int f(int[]a,int t){Arrays.sort(a);int c=0;for(int i=0;i<a.length-3;i++){if(i>0&&a[i]==a[i-1])continue;for(int j=i+1;j<a.length-2;j++){if(j>i+1&&a[j]==a[j-1])continue;int l=j+1,r=a.length-1;while(l<r){long s=(long)a[i]+a[j]+a[l]+a[r];if(s==t){c++;int x=a[l],y=a[r];while(l<r&&a[l]==x)l++;while(l<r&&a[r]==y)r--;}else if(s<t)l++;else r--;}}}return c;}public static void main(String[]z){if(f(new int[]{1,0,-1,0,-2,2},0)!=3||f(new int[]{2,2,2,2,2},8)!=1)throw new AssertionError();}}
```
