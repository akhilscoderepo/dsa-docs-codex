<!-- solutions-for: 01-exact-search -->
### Exact Search Solutions

#### Solution: [Build] Binary Search (LeetCode 704)
<!-- id: bs-exact-target -->

**Approach.** Keep an inclusive interval containing every possible match. Sortedness determines which half, including the inspected midpoint, cannot contain the target.

**Complexity.** O(log n) time and O(1) extra space.

```java run
public final class ExactTarget {
    static int search(int[] a, int t) { int l=0,h=a.length-1; while(l<=h){int m=l+(h-l)/2; if(a[m]==t)return m; if(a[m]<t)l=m+1; else h=m-1;} return -1; }
    public static void main(String[] x){if(search(new int[]{-7,-2,3,8,14},8)!=3)throw new AssertionError();if(search(new int[]{6},2)!=-1)throw new AssertionError();}
}
```

#### Solution: [Vary] Descending Search (Author exercise)
<!-- id: bs-descending-target -->

**Approach.** Preserve the inclusive exact-search structure, but move left when the midpoint is smaller because larger values lie at lower indices.

**Complexity.** O(log n) time and O(1) space.

```java run
public final class DescendingTarget {
    static int find(int[] a,int t){int l=0,h=a.length-1;while(l<=h){int m=l+(h-l)/2;if(a[m]==t)return m;if(a[m]<t)h=m-1;else l=m+1;}return -1;}
    public static void main(String[]z){if(find(new int[]{20,13,9,4,-1},9)!=2)throw new AssertionError();if(find(new int[]{5,1},7)!=-1)throw new AssertionError();}
}
```

#### Solution: [Boundary] Two Elements (Author exercise)
<!-- id: bs-two-element-proof -->

**Approach.** Use the unchanged inclusive loop. Updating past `mid` guarantees progress even when only one position remains.

**Complexity.** O(log n) time, which is constant for this restricted input, and O(1) space.

```java run
public final class TwoElementLookup {
    static int locate(int[]a,int t){int l=0,r=a.length-1;while(l<=r){int m=l+(r-l)/2;if(a[m]==t)return m;if(a[m]<t)l=m+1;else r=m-1;}return -1;}
    public static void main(String[]q){if(locate(new int[]{1,3},3)!=1)throw new AssertionError();if(locate(new int[]{1,3},2)!=-1)throw new AssertionError();if(locate(new int[0],4)!=-1)throw new AssertionError();}
}
```

#### Solution: [Recognize] Search A Row-Major Matrix (LeetCode 74)
<!-- id: bs-recognize-row-major -->

**Approach.** Binary-search virtual indices from zero through `rows * cols - 1`. Division selects the row and remainder selects the column.

**Complexity.** O(log(rows * cols)) time and O(1) space.

```java run
public final class VirtualMatrixSearch {
    static boolean has(int[][]m,int t){int c=m[0].length,l=0,h=m.length*c-1;while(l<=h){int k=l+(h-l)/2,v=m[k/c][k%c];if(v==t)return true;if(v<t)l=k+1;else h=k-1;}return false;}
    public static void main(String[]s){if(!has(new int[][]{{1,4,7},{10,13,18}},13))throw new AssertionError();if(has(new int[][]{{2,5},{9,12}},6))throw new AssertionError();}
}
```
