<!-- solutions-for: 06-remainder-classes -->
### Remainder Classes

#### Solution: [Build] Subarray Sums Divisible by K (LeetCode 974)
<!-- id: ps-divisible-subarrays -->

**Approach.** Count earlier boundaries by normalized remainder. Each earlier copy of the current class forms one divisible subarray ending here.

**Complexity.** O(n + k) time and O(k) space.

```java run
public final class DivisibleExercise{static long solve(int[]a,int k){long[]f=new long[k];f[0]=1;long p=0,c=0;for(int x:a){p+=x;int r=(int)Math.floorMod(p,k);c+=f[r];f[r]++;}return c;}static long brute(int[]a,int k){long c=0;for(int l=0;l<a.length;l++){long s=0;for(int r=l;r<a.length;r++){s+=a[r];if(Math.floorMod(s,k)==0)c++;}}return c;}public static void main(String[]z){if(solve(new int[]{3,2,-5,5},5)!=6)throw new AssertionError("example 1");if(solve(new int[]{-1,1},2)!=1)throw new AssertionError("example 2");var g=new java.util.Random(37);for(int t=0;t<500;t++){int[]a=new int[g.nextInt(8)];for(int i=0;i<a.length;i++)a[i]=g.nextInt(9)-4;int k=g.nextInt(6)+1;if(solve(a,k)!=brute(a,k))throw new AssertionError("random");}}}
```

#### Solution: [Vary] Continuous Subarray Sum (LeetCode 523)
<!-- id: ps-continuous-divisible -->

**Approach.** Store the earliest index for each remainder, seeded with zero at `-1`. A repeated class qualifies only when the current index minus that earliest index is at least two.

**Complexity.** O(n) expected time and O(min(n,k)) space.

```java run
import java.util.*;
public final class ContinuousDivisibleExercise{static boolean solve(int[]a,int k){Map<Integer,Integer>first=new HashMap<>();first.put(0,-1);long p=0;for(int i=0;i<a.length;i++){p+=a[i];int r=(int)Math.floorMod(p,k);Integer old=first.get(r);if(old!=null&&i-old>=2)return true;if(old==null)first.put(r,i);}return false;}public static void main(String[]z){if(!solve(new int[]{6,1,5},6))throw new AssertionError("example 1");if(solve(new int[]{7},7))throw new AssertionError("example 2");}}
```

#### Solution: [Boundary] Negative Values (Author exercise)
<!-- id: ps-negative-remainders -->

**Approach.** Normalize every cumulative total before indexing its class count. Return the last normalized class along with the accumulated number of equal-class pairs.

**Complexity.** O(n + k) time and O(k) space.

```java run
public final class NegativeRemainderExercise{record Result(long count,int finalRemainder){}static Result solve(int[]a,int k){long[]f=new long[k];f[0]=1;long p=0,c=0;int r=0;for(int x:a){p+=x;r=(int)Math.floorMod(p,k);c+=f[r];f[r]++;}return new Result(c,r);}public static void main(String[]z){var x=solve(new int[]{-1,1},5);if(x.count()!=1||x.finalRemainder()!=0)throw new AssertionError("example 1");var y=solve(new int[]{-1},5);if(y.count()!=0||y.finalRemainder()!=4)throw new AssertionError("example 2");}}
```

#### Solution: [Recognize] Longest Divisible Span (Author exercise)
<!-- id: ps-longest-divisible-span -->

**Approach.** Preserve the first index of each normalized remainder. Every repetition makes a divisible interval, and the oldest boundary maximizes its length.

**Complexity.** O(n) expected time and O(min(n,k)) space.

```java run
import java.util.*;
public final class LongestDivisibleExercise{static int solve(int[]a,int k){Map<Integer,Integer>first=new HashMap<>();first.put(0,-1);long p=0;int best=0;for(int i=0;i<a.length;i++){p+=a[i];int r=(int)Math.floorMod(p,k);Integer old=first.get(r);if(old==null)first.put(r,i);else best=Math.max(best,i-old);}return best;}static int brute(int[]a,int k){int b=0;for(int l=0;l<a.length;l++){long s=0;for(int r=l;r<a.length;r++){s+=a[r];if(Math.floorMod(s,k)==0)b=Math.max(b,r-l+1);}}return b;}public static void main(String[]z){if(solve(new int[]{2,3,1,4},5)!=4)throw new AssertionError("example 1");if(solve(new int[]{1,1},3)!=0)throw new AssertionError("example 2");}}
```
