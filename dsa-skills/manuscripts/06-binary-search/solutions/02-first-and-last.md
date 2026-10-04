<!-- solutions-for: 02-first-and-last -->
### First And Last Solutions

#### Solution: [Build] First Occurrence (Author exercise)
<!-- id: bs-first-occurrence -->

**Approach.** Save each match and continue left. The candidate survives even when the remaining interval becomes empty.

**Complexity.** O(log n) time and O(1) space.

```java run
public final class FirstOccurrence { static int first(int[]a,int t){int l=0,h=a.length-1,r=-1;while(l<=h){int m=l+(h-l)/2;if(a[m]>=t){if(a[m]==t)r=m;h=m-1;}else l=m+1;}return r;} public static void main(String[]x){if(first(new int[]{2,2,2,5,9},2)!=0)throw new AssertionError();if(first(new int[]{1,4,4},3)!=-1)throw new AssertionError();}}
```

#### Solution: [Vary] Last Occurrence (Author exercise)
<!-- id: bs-last-occurrence -->

**Approach.** Store equality and search right, discarding the midpoint after it becomes the current best candidate.

**Complexity.** O(log n) time and O(1) space.

```java run
public final class LastOccurrence { static int last(int[]a,int t){int l=0,h=a.length-1,r=-1;while(l<=h){int m=l+(h-l)/2;if(a[m]<=t){if(a[m]==t)r=m;l=m+1;}else h=m-1;}return r;}public static void main(String[]x){if(last(new int[]{1,4,4,4,8},4)!=3)throw new AssertionError();if(last(new int[]{7,7},9)!=-1)throw new AssertionError();}}
```

#### Solution: [Boundary] Find First and Last Position (LeetCode 34)
<!-- id: bs-complete-target-range -->

**Approach.** Use a directional helper twice. Each invocation owns its candidate, so an absent target produces two independent `-1` results.

**Complexity.** O(log n) time overall and O(1) extra space.

```java run
import java.util.Arrays;
public final class CompleteTargetRange { static int edge(int[]a,int t,boolean left){int l=0,h=a.length-1,r=-1;while(l<=h){int m=l+(h-l)/2;if(a[m]==t){r=m;if(left)h=m-1;else l=m+1;}else if(a[m]<t)l=m+1;else h=m-1;}return r;}static int[] range(int[]a,int t){return new int[]{edge(a,t,true),edge(a,t,false)};}public static void main(String[]x){if(!Arrays.equals(range(new int[]{0,3,3,3,10},3),new int[]{1,3}))throw new AssertionError();if(!Arrays.equals(range(new int[]{5,5,5},5),new int[]{0,2}))throw new AssertionError();}}
```

#### Solution: [Recognize] First Bad Version (LeetCode 278)
<!-- id: bs-recognize-first-bad -->

**Approach.** Simulate the oracle with a threshold. A bad midpoint remains possible, while a good midpoint and every earlier version are discarded.

**Complexity.** O(log n) oracle calls and O(1) space.

```java run
public final class FirstBadVersion { static int firstBad(int n,int threshold){int l=1,h=n;while(l<h){int m=l+(h-l)/2;if(m>=threshold)h=m;else l=m+1;}return l;}public static void main(String[]x){if(firstBad(8,6)!=6)throw new AssertionError();if(firstBad(1,1)!=1)throw new AssertionError();}}
```
