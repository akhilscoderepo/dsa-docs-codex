<!-- solutions-for: 91-sorting-and-two-pointers -->
### Sorting And Two Pointers Solutions

#### Solution: [Build] Two Sum II (LeetCode 167)
<!-- id: tp-combo-two-sum-ii -->

**Approach.** Compare endpoint sums and eliminate the side that cannot reach the target with any remaining partner.

**Complexity.** O(n) time and O(1) space.

```java run
public final class TpC167 {static int[]f(int[]a,int t){int l=0,r=a.length-1;while(l<r){long s=(long)a[l]+a[r];if(s==t)return new int[]{l+1,r+1};if(s<t)l++;else r--;}throw new AssertionError();}public static void main(String[]z){int[]p=f(new int[]{2,7,11,15},9);if(p[0]!=1||p[1]!=2)throw new AssertionError();}}
```

#### Solution: [Vary] 3Sum (LeetCode 15)
<!-- id: tp-combo-three-sum -->

**Approach.** Sort, skip repeated fixed values, and count unique matching pairs in each suffix.

**Complexity.** O(n²) time and O(1) auxiliary space apart from output.

```java run
import java.util.*;
public final class TpC15 {static int f(int[]a){Arrays.sort(a);int n=0;for(int i=0;i<a.length-2;i++){if(i>0&&a[i]==a[i-1])continue;int l=i+1,r=a.length-1;while(l<r){long s=(long)a[i]+a[l]+a[r];if(s==0){n++;int x=a[l],y=a[r];while(l<r&&a[l]==x)l++;while(l<r&&a[r]==y)r--;}else if(s<0)l++;else r--;}}return n;}public static void main(String[]z){if(f(new int[]{-1,0,1,2,-1,-4})!=2||f(new int[]{0,1,1})!=0)throw new AssertionError();}}
```

#### Solution: [Boundary] 3Sum Closest (LeetCode 16)
<!-- id: tp-combo-three-closest -->

**Approach.** Measure and save every endpoint total, then move according to its relation with the target.

**Complexity.** O(n²) time and O(1) extra space.

```java run
import java.util.*;
public final class TpC16 {static int f(int[]a,int t){Arrays.sort(a);long b=(long)a[0]+a[1]+a[2];for(int i=0;i<a.length-2;i++)for(int l=i+1,r=a.length-1;l<r;){long s=(long)a[i]+a[l]+a[r];if(Math.abs(s-t)<Math.abs(b-t))b=s;if(s<t)l++;else if(s>t)r--;else return t;}return(int)b;}public static void main(String[]z){if(f(new int[]{-1,2,1,-4},1)!=2||f(new int[]{0,0,0},1)!=0)throw new AssertionError();}}
```

#### Solution: [Recognize] 4Sum (LeetCode 18)
<!-- id: tp-combo-four-sum -->

**Approach.** Sort, choose two distinct fixed depths, and run a duplicate-aware final pair scan with `long` sums.

**Complexity.** O(n³) time and O(1) auxiliary space apart from output.

```java run
import java.util.*;
public final class TpC18 {static int f(int[]a,int t){Arrays.sort(a);int n=0;for(int i=0;i<a.length-3;i++){if(i>0&&a[i]==a[i-1])continue;for(int j=i+1;j<a.length-2;j++){if(j>i+1&&a[j]==a[j-1])continue;int l=j+1,r=a.length-1;while(l<r){long s=(long)a[i]+a[j]+a[l]+a[r];if(s==t){n++;int x=a[l],y=a[r];while(l<r&&a[l]==x)l++;while(l<r&&a[r]==y)r--;}else if(s<t)l++;else r--;}}}return n;}public static void main(String[]z){if(f(new int[]{1,0,-1,0,-2,2},0)!=3||f(new int[]{2,2,2,2,2},8)!=1)throw new AssertionError();}}
```
