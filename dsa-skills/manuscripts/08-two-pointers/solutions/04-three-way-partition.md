<!-- solutions-for: 04-three-way-partition -->
### Three-Way Partition Solutions

#### Solution: [Build] Partition 0,1,2 (Author exercise)
<!-- id: tp-partition-012 -->

**Approach.** Maintain low, middle, unresolved, and high regions; recheck values swapped from the right.

**Complexity.** O(n) time and O(1) space.

```java run
public final class Tp012 {static void f(int[]a){int l=0,m=0,h=a.length-1;while(m<=h)if(a[m]==0){int t=a[l];a[l++]=a[m];a[m++]=t;}else if(a[m]==1)m++;else{int t=a[m];a[m]=a[h];a[h--]=t;}}public static void main(String[]z){int[]a={2,0,1};f(a);if(!java.util.Arrays.equals(a,new int[]{0,1,2}))throw new AssertionError();f(new int[0]);}}
```

#### Solution: [Vary] Sort Colors (LeetCode 75)
<!-- id: tp-sort-colors -->

**Approach.** Use the same one-pass region transitions, treating value 1 as the middle category.

**Complexity.** O(n) time and O(1) auxiliary space.

```java run
public final class TpColors {static void f(int[]a){int l=0,m=0,h=a.length-1;while(m<=h){switch(a[m]){case 0->{int t=a[l];a[l++]=a[m];a[m++]=t;}case 1->m++;default->{int t=a[m];a[m]=a[h];a[h--]=t;}}}}public static void main(String[]z){int[]a={2,0,2,1,1,0};f(a);if(!java.util.Arrays.equals(a,new int[]{0,0,1,1,2,2}))throw new AssertionError();}}
```

#### Solution: [Boundary] Reinspect Swapped High (Author exercise)
<!-- id: tp-reinspect-high -->

**Approach.** Count each high-branch swap. That branch leaves `mid` fixed, so every count corresponds to a required reinspection.

**Complexity.** O(n) time and O(1) space.

```java run
public final class TpReinspect {static int f(int[]a){int l=0,m=0,h=a.length-1,c=0;while(m<=h)if(a[m]==0){int t=a[l];a[l++]=a[m];a[m++]=t;}else if(a[m]==1)m++;else{int t=a[m];a[m]=a[h];a[h--]=t;c++;}return c;}public static void main(String[]z){int[]a={2,0};if(f(a)!=1||!java.util.Arrays.equals(a,new int[]{0,2})||f(new int[]{0,1})!=0)throw new AssertionError();}}
```

#### Solution: [Recognize] Three-Way Pivot Partition (Author exercise)
<!-- id: tp-three-way-pivot -->

**Approach.** Replace category equality tests with comparisons to the pivot and return `low, high` after resolution.

**Complexity.** O(n) time and O(1) extra space.

```java run
public final class TpPivot3 {static int[]f(int[]a,int p){int l=0,m=0,h=a.length-1;while(m<=h)if(a[m]<p){int t=a[l];a[l++]=a[m];a[m++]=t;}else if(a[m]==p)m++;else{int t=a[m];a[m]=a[h];a[h--]=t;}return new int[]{l,h};}public static void main(String[]z){int[]b=f(new int[]{4,2,4,7,1},4);if(b[0]!=2||b[1]!=3)throw new AssertionError();int[]e=f(new int[]{1,2},5);if(e[0]!=2||e[1]!=1)throw new AssertionError();}}
```
