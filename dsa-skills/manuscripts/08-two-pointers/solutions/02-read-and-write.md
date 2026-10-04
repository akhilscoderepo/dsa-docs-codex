<!-- solutions-for: 02-read-and-write -->
### Read And Write Solutions

#### Solution: [Build] Remove Element (LeetCode 27)
<!-- id: tp-remove-element -->

**Approach.** Copy each value unequal to `val` into the next output position and return the number copied.

**Complexity.** O(n) time and O(1) space.

```java run
public final class TpRemove {static int f(int[]a,int v){int w=0;for(int x:a)if(x!=v)a[w++]=x;return w;}public static void main(String[]z){int[]a={3,2,2,3};if(f(a,3)!=2||a[0]!=2||a[1]!=2||f(new int[0],4)!=0)throw new AssertionError();}}
```

#### Solution: [Vary] Move Zeroes (LeetCode 283)
<!-- id: tp-move-zeroes -->

**Approach.** Compact nonzero values in order, then write zeros from the logical end through the physical end.

**Complexity.** O(n) time and O(1) extra space.

```java run
public final class TpMoveZero {static void f(int[]a){int w=0;for(int x:a)if(x!=0)a[w++]=x;while(w<a.length)a[w++]=0;}public static void main(String[]z){int[]a={0,1,0,3,12};f(a);if(!java.util.Arrays.equals(a,new int[]{1,3,12,0,0}))throw new AssertionError();int[]b={0};f(b);if(b[0]!=0)throw new AssertionError();}}
```

#### Solution: [Boundary] Remove Duplicates (LeetCode 26)
<!-- id: tp-remove-sorted-duplicates -->

**Approach.** Accept the first value, then accept a later value only when it differs from the last written value.

**Complexity.** O(n) time and O(1) space.

```java run
public final class TpUnique {static int f(int[]a){int w=0;for(int x:a)if(w==0||a[w-1]!=x)a[w++]=x;return w;}public static void main(String[]z){int[]a={1,1,2};if(f(a)!=2||a[1]!=2||f(new int[]{5})!=1)throw new AssertionError();}}
```

#### Solution: [Recognize] Remove Duplicates II (LeetCode 80)
<!-- id: tp-remove-duplicates-two -->

**Approach.** Accept every candidate while fewer than two outputs exist; afterward accept it only when it differs from `a[write-2]`.

**Complexity.** O(n) time and O(1) space.

```java run
public final class TpKeepTwo {static int f(int[]a){int w=0;for(int x:a)if(w<2||a[w-2]!=x)a[w++]=x;return w;}public static void main(String[]z){int[]a={1,1,1,2,2,3};if(f(a)!=5||!java.util.Arrays.equals(java.util.Arrays.copyOf(a,5),new int[]{1,1,2,2,3})||f(new int[]{7,7})!=2)throw new AssertionError();}}
```
