<!-- solutions-for: 01-endpoint-ordering-contracts -->
### Endpoint Ordering Contracts

#### Solution: [Build] Order By Start Then End (Author exercise)
<!-- id: interval-order-start-end -->
**Approach.** Clone every row and sort with chained safe comparisons. A selection-sort oracle checks random arrays.
**Complexity.** Sorting dominates at O(n log n) time; cloned rows occupy O(n) returned space.
```java run
import java.util.*;
public final class IntervalOrderStartEnd {
 static final Comparator<int[]> C=Comparator.<int[]>comparingInt(x->x[0]).thenComparingInt(x->x[1]);
 static int[][] solve(int[][] a){int[][]r=Arrays.stream(a).map(int[]::clone).toArray(int[][]::new);Arrays.sort(r,C);return r;}
 static int[][] brute(int[][]a){List<int[]>r=new ArrayList<>();for(int[]x:a)r.add(x.clone());for(int i=0;i<r.size();i++){int b=i;for(int j=i+1;j<r.size();j++)if(C.compare(r.get(j),r.get(b))<0)b=j;Collections.swap(r,i,b);}return r.toArray(int[][]::new);}
 static void check(int[][]a){if(!Arrays.deepEquals(solve(a),brute(a)))throw new AssertionError();}
 public static void main(String[]z){check(new int[][]{{3,7},{1,8},{1,4}});check(new int[][]{{Integer.MAX_VALUE,Integer.MAX_VALUE},{Integer.MIN_VALUE,-1}});Random q=new Random(1001);for(int t=0;t<1000;t++){int[][]a=new int[q.nextInt(20)][2];for(int[]x:a){x[0]=q.nextInt();x[1]=q.nextInt();}check(a);}}
}
```

#### Solution: [Vary] Order By End Then Start (Author exercise)
<!-- id: interval-order-end-start -->
**Approach.** Clone rows and change the primary comparator key to end. The oracle performs repeated minimum selection.
**Complexity.** Comparator sorting takes O(n log n) time, and the independent result needs O(n) space.
```java run
import java.util.*;
public final class IntervalOrderEndStart {
 static final Comparator<int[]> C=Comparator.<int[]>comparingInt(x->x[1]).thenComparingInt(x->x[0]);
 static int[][] solve(int[][]a){int[][]r=Arrays.stream(a).map(int[]::clone).toArray(int[][]::new);Arrays.sort(r,C);return r;}
 static void check(int[][]a){int[][]r=solve(a);for(int i=1;i<r.length;i++)if(C.compare(r[i-1],r[i])>0)throw new AssertionError();}
 public static void main(String[]z){check(new int[][]{{1,8},{4,6},{2,6}});check(new int[0][2]);Random q=new Random(1002);for(int t=0;t<2000;t++){int[][]a=new int[q.nextInt(30)][2];for(int[]x:a){x[0]=q.nextInt();x[1]=q.nextInt();}check(a);}}
}
```

#### Solution: [Boundary] Equal And Extreme Endpoints (Author exercise)
<!-- id: interval-order-extreme-endpoints -->
**Approach.** Sort with safe comparisons and verify every adjacent relation. Random tests include unrestricted integer endpoints.
**Complexity.** Ordering requires O(n log n) time; the cloned verification array uses O(n) storage.
```java run
import java.util.*;
public final class IntervalOrderExtremeEndpoints {
 static final Comparator<int[]> C=Comparator.<int[]>comparingInt(x->x[0]).thenComparingInt(x->x[1]);
 static boolean solve(int[][]a){int[][]r=Arrays.stream(a).map(int[]::clone).toArray(int[][]::new);Arrays.sort(r,C);for(int i=1;i<r.length;i++)if(C.compare(r[i-1],r[i])>0)return false;return true;}
 public static void main(String[]z){if(!solve(new int[][]{{Integer.MIN_VALUE,Integer.MAX_VALUE},{Integer.MIN_VALUE,Integer.MIN_VALUE},{Integer.MAX_VALUE,Integer.MAX_VALUE}})||!solve(new int[][]{{7,7},{7,7}}))throw new AssertionError();Random q=new Random(1003);for(int t=0;t<2000;t++){int[][]a=new int[q.nextInt(30)][2];for(int[]x:a){x[0]=q.nextInt();x[1]=q.nextInt();}if(!solve(a))throw new AssertionError();}}
}
```

#### Solution: [Recognize] Merge Intervals (LeetCode 56)
<!-- id: interval-order-merge-recognition -->
**Approach.** Sort cloned rows by start, keep one active union, and finalize it when the next start exceeds its end. The oracle marks covered integer points for bounded random endpoints.
**Complexity.** O(n log n) time and O(n) returned space.
```java run
import java.util.*;
public final class IntervalOrderMergeRecognition {
 static int[][] solve(int[][]a){int[][]r=Arrays.stream(a).map(int[]::clone).toArray(int[][]::new);Arrays.sort(r,Comparator.comparingInt(x->x[0]));List<int[]>o=new ArrayList<>();for(int[]x:r){if(o.isEmpty()||x[0]>o.get(o.size()-1)[1])o.add(x.clone());else o.get(o.size()-1)[1]=Math.max(o.get(o.size()-1)[1],x[1]);}return o.toArray(int[][]::new);}
 static boolean[] cover(int[][]a){boolean[]c=new boolean[21];for(int[]x:a)for(int v=x[0];v<=x[1];v++)c[v]=true;return c;}
 static void check(int[][]a){int[][]r=solve(a);if(!Arrays.equals(cover(a),cover(r)))throw new AssertionError();for(int i=1;i<r.length;i++)if(r[i][0]<=r[i-1][1])throw new AssertionError();}
 public static void main(String[]z){check(new int[][]{{1,3},{2,6},{8,10},{15,18}});check(new int[][]{{1,4},{4,5}});Random q=new Random(5601);for(int t=0;t<1000;t++){int[][]a=new int[1+q.nextInt(15)][2];for(int[]x:a){x[0]=q.nextInt(20);x[1]=x[0]+q.nextInt(21-x[0]);}check(a);}}
}
```
