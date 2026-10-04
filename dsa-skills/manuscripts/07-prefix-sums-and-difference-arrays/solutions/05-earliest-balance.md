<!-- solutions-for: 05-earliest-balance -->
### Earliest Balance

#### Solution: [Build] Contiguous Array (LeetCode 525)
<!-- id: ps-contiguous-array -->

**Approach.** Add one for a one and subtract one for a zero. Store only the first index for each balance and measure every repeat against it.

**Complexity.** O(n) expected time and O(n) space.

```java run
import java.util.HashMap;
import java.util.Map;
import java.util.Random;
public final class ContiguousExercise {
    static int solve(int[] a) {
        Map<Integer,Integer> first = new HashMap<>(); first.put(0,-1);
        int balance=0,best=0;
        for(int i=0;i<a.length;i++){balance+=a[i]==1?1:-1;Integer old=first.get(balance);if(old==null)first.put(balance,i);else best=Math.max(best,i-old);}
        return best;
    }
    static int brute(int[] a){int best=0;for(int l=0;l<a.length;l++){int b=0;for(int r=l;r<a.length;r++){b+=a[r]==1?1:-1;if(b==0)best=Math.max(best,r-l+1);}}return best;}
    public static void main(String[] args){if(solve(new int[]{0,1,1,0,0})!=4)throw new AssertionError("example 1");if(solve(new int[]{1,1,1})!=0)throw new AssertionError("example 2");Random g=new Random(31);for(int t=0;t<500;t++){int[]a=new int[g.nextInt(10)];for(int i=0;i<a.length;i++)a[i]=g.nextInt(2);if(solve(a)!=brute(a))throw new AssertionError("random");}}
}
```

#### Solution: [Vary] Equal A And B (Author exercise)
<!-- id: ps-equal-a-b -->

**Approach.** Add one for `a`, subtract one for `b`, and add zero for everything else. Equal balances enclose equal counts, including spans containing neither value.

**Complexity.** O(n) expected time and O(n) space.

```java run
import java.util.HashMap;
import java.util.Map;
public final class EqualABExercise {
    static int solve(int[] values,int a,int b){Map<Integer,Integer>first=new HashMap<>();first.put(0,-1);int balance=0,best=0;for(int i=0;i<values.length;i++){if(values[i]==a)balance++;else if(values[i]==b)balance--;Integer old=first.get(balance);if(old==null)first.put(balance,i);else best=Math.max(best,i-old);}return best;}
    public static void main(String[] args){if(solve(new int[]{4,9,5,4,5},4,5)!=5)throw new AssertionError("example 1");if(solve(new int[]{7,7},1,2)!=2)throw new AssertionError("example 2");}
}
```

#### Solution: [Boundary] Prefix From Zero (Author exercise)
<!-- id: ps-balanced-prefix-zero -->

**Approach.** Preserve earliest balance indices and track the start of the best candidate. Replace the result only for a longer span or an equal span with an earlier start.

**Complexity.** O(n) expected time and O(n) space.

```java run
import java.util.HashMap;
import java.util.Map;
public final class BalancedPrefixExercise {
    record Result(int length,boolean startsAtZero){}
    static Result solve(int[]a){Map<Integer,Integer>first=new HashMap<>();first.put(0,-1);int balance=0,best=0,start=0;for(int i=0;i<a.length;i++){balance+=a[i]==1?1:-1;Integer old=first.get(balance);if(old==null)first.put(balance,i);else{int length=i-old,candidateStart=old+1;if(length>best||(length==best&&candidateStart<start)){best=length;start=candidateStart;}}}return new Result(best,best>0&&start==0);}
    public static void main(String[]args){Result first=solve(new int[]{0,1,1,0});if(first.length()!=4||!first.startsAtZero())throw new AssertionError("example 1");Result second=solve(new int[]{1,1,0});if(second.length()!=2||second.startsAtZero())throw new AssertionError("example 2");}
}
```

#### Solution: [Recognize] Even Vowel Counts (LeetCode 1371)
<!-- id: ps-even-vowel-parity -->

**Approach.** Toggle a dedicated bit whenever a vowel appears. Store the earliest index for each of 32 masks; a repeated mask means every vowel changed parity an even number of times.

**Complexity.** O(n) time and O(1) space for 32 states.

```java run
public final class VowelParityExercise {
    static int solve(String s){int[]first=new int[32];java.util.Arrays.fill(first,-2);first[0]=-1;int mask=0,best=0;for(int i=0;i<s.length();i++){int bit=switch(s.charAt(i)){case'a'->0;case'e'->1;case'i'->2;case'o'->3;case'u'->4;default->-1;};if(bit>=0)mask^=1<<bit;if(first[mask]!=-2)best=Math.max(best,i-first[mask]);else first[mask]=i;}return best;}
    public static void main(String[]args){if(solve("bcaac")!=5)throw new AssertionError("example 1");if(solve("bcdf")!=4)throw new AssertionError("example 2");}
}
```
