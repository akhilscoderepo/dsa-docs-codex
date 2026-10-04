<!-- solutions-for: 05-duplicate-skipping -->
### Duplicate Skipping Solutions

#### Solution: [Build] Unique Pairs (Author exercise)
<!-- id: tp-unique-pairs -->

**Approach.** Sort, scan inward, and skip every copy of both values after recording a match.

**Complexity.** O(n log n) time and O(1) auxiliary space apart from output.

```java run
import java.util.*;
public final class TpUP{static List<String>f(int[]a,int t){Arrays.sort(a);List<String>r=new ArrayList<>();int l=0,h=a.length-1;while(l<h){long s=(long)a[l]+a[h];if(s==t){int x=a[l],y=a[h];r.add(x+":"+y);while(l<h&&a[l]==x)l++;while(l<h&&a[h]==y)h--;}else if(s<t)l++;else h--;}return r;}public static void main(String[]z){if(f(new int[]{1,1,2,2,3},4).size()!=2||!f(new int[]{0,0,0},1).isEmpty())throw new AssertionError();}}
```

#### Solution: [Vary] 3Sum (LeetCode 15)
<!-- id: tp-three-sum-dedup -->

**Approach.** Sort, skip repeated fixed values, and use a duplicate-aware pair search on each suffix.

**Complexity.** O(n²) time and O(1) auxiliary space apart from output.

```java run
import java.util.*;
public final class Tp3S{static List<List<Integer>>f(int[]a){Arrays.sort(a);List<List<Integer>>r=new ArrayList<>();for(int i=0;i<a.length-2;i++){if(i>0&&a[i]==a[i-1])continue;int l=i+1,h=a.length-1;while(l<h){long s=(long)a[i]+a[l]+a[h];if(s==0){r.add(List.of(a[i],a[l],a[h]));int x=a[l],y=a[h];while(l<h&&a[l]==x)l++;while(l<h&&a[h]==y)h--;}else if(s<0)l++;else h--;}}return r;}public static void main(String[]z){if(f(new int[]{-1,0,1,2,-1,-4}).size()!=2||f(new int[]{0,0,0}).size()!=1)throw new AssertionError();}}
```

#### Solution: [Boundary] All Equal (Author exercise)
<!-- id: tp-all-equal-triplet -->

**Approach.** One triple exists exactly when the common value is zero; extra copies do not create new value combinations.

**Complexity.** O(1) time and O(1) auxiliary space.

```java run
public final class TpEqual3{static int f(int[]a){return a[0]==0?1:0;}public static void main(String[]z){if(f(new int[]{0,0,0,0})!=1||f(new int[]{2,2,2})!=0)throw new AssertionError();}}
```

#### Solution: [Recognize] 4Sum (LeetCode 18)
<!-- id: tp-four-sum-dedup -->

**Approach.** Sort, choose two nonrepeated fixed values, then run a unique-pair scan with widened sums.

**Complexity.** O(n³) time and O(1) auxiliary space apart from output.

```java run
import java.util.*;
public final class Tp4S{static int f(int[]a,int t){Arrays.sort(a);int c=0;for(int i=0;i<a.length-3;i++){if(i>0&&a[i]==a[i-1])continue;for(int j=i+1;j<a.length-2;j++){if(j>i+1&&a[j]==a[j-1])continue;int l=j+1,h=a.length-1;while(l<h){long s=(long)a[i]+a[j]+a[l]+a[h];if(s==t){c++;int x=a[l],y=a[h];while(l<h&&a[l]==x)l++;while(l<h&&a[h]==y)h--;}else if(s<t)l++;else h--;}}}return c;}public static void main(String[]z){if(f(new int[]{1,0,-1,0,-2,2},0)!=3||f(new int[]{2,2,2,2,2},8)!=1)throw new AssertionError();}}
```
