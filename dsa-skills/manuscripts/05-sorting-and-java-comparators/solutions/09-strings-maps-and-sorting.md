<!-- solutions-for: 09-strings-maps-and-sorting -->
### Strings, Maps, And Sorting

#### Solution: [Build] Valid Anagram (LeetCode 242)
<!-- id: combo-valid-anagram-sort -->

**Approach.** Reject unequal lengths, sort private character arrays, and compare them. A count table supplies the random oracle.

**Complexity.** O(m log m) time and O(m) space.

```java run
import java.util.Arrays;
import java.util.Random;
public final class ComboValidAnagramSort {
    static boolean solve(String a,String b){ if(a.length()!=b.length())return false; char[] x=a.toCharArray(),y=b.toCharArray(); Arrays.sort(x);Arrays.sort(y);return Arrays.equals(x,y); }
    static boolean brute(String a,String b){int[] c=new int[26];for(char ch:a.toCharArray())c[ch-'a']++;for(char ch:b.toCharArray())c[ch-'a']--;return a.length()==b.length()&&Arrays.stream(c).allMatch(v->v==0);}
    public static void main(String[] z){if(!solve("anagram","nagaram")||solve("rat","car"))throw new AssertionError();Random r=new Random(24209);for(int t=0;t<2000;t++){StringBuilder a=new StringBuilder(),b=new StringBuilder();for(int i=0,n=r.nextInt(15);i<n;i++){a.append((char)('a'+r.nextInt(5)));b.append((char)('a'+r.nextInt(5)));}if(solve(a.toString(),b.toString())!=brute(a.toString(),b.toString()))throw new AssertionError();}}
}
```

#### Solution: [Vary] Group Anagrams (LeetCode 49)
<!-- id: combo-group-anagrams-sort-key -->

**Approach.** Use each sorted word as a linked-map key and append the original word. The oracle compares every pair of returned words with character counts and checks complete input multiplicity.

**Complexity.** O(n * m log m) time and O(n * m) space.

```java run
import java.util.*;
public final class ComboGroupAnagramsSortKey {
    static String key(String s){char[] c=s.toCharArray();Arrays.sort(c);return new String(c);}
    static List<List<String>> solve(String[] a){Map<String,List<String>> m=new LinkedHashMap<>();for(String s:a)m.computeIfAbsent(key(s),x->new ArrayList<>()).add(s);return new ArrayList<>(m.values());}
    static void check(String[] a){List<List<String>> g=solve(a);List<String> flat=new ArrayList<>();for(List<String> q:g){for(String s:q)if(!key(s).equals(key(q.get(0))))throw new AssertionError();flat.addAll(q);}List<String>x=new ArrayList<>(Arrays.asList(a));Collections.sort(x);Collections.sort(flat);if(!x.equals(flat))throw new AssertionError();}
    public static void main(String[] z){check(new String[]{"eat","tea","tan","ate","nat","bat"});check(new String[]{"",""});Random r=new Random(4909);for(int t=0;t<1000;t++){String[] a=new String[1+r.nextInt(20)];for(int i=0;i<a.length;i++){StringBuilder s=new StringBuilder();for(int j=0,n=r.nextInt(6);j<n;j++)s.append((char)('a'+r.nextInt(4)));a[i]=s.toString();}check(a);}}
}
```

#### Solution: [Boundary] Sort Characters By Frequency (LeetCode 451)
<!-- id: combo-sort-characters-frequency -->

**Approach.** Count characters, sort distinct characters by decreasing count and then code point for deterministic ties, and append each run. The oracle verifies multiplicities and nonincreasing run frequencies.

**Complexity.** O(n + u log u) time and O(u + n) space for `u` distinct characters.

```java run
import java.util.*;
public final class ComboSortCharactersFrequency {
    static String solve(String s){Map<Character,Integer> c=new HashMap<>();for(char x:s.toCharArray())c.merge(x,1,Integer::sum);List<Character> k=new ArrayList<>(c.keySet());k.sort(Comparator.<Character>comparingInt(c::get).reversed().thenComparingInt(x->x));StringBuilder out=new StringBuilder();for(char x:k)out.append(String.valueOf(x).repeat(c.get(x)));return out.toString();}
    static void check(String s){String o=solve(s);int[] a=new int[128],b=new int[128];for(char x:s.toCharArray())a[x]++;for(char x:o.toCharArray())b[x]++;if(!Arrays.equals(a,b))throw new AssertionError();int last=Integer.MAX_VALUE;for(int i=0;i<o.length();){int j=i+1;while(j<o.length()&&o.charAt(j)==o.charAt(i))j++;if(j-i>last)throw new AssertionError();last=j-i;i=j;}}
    public static void main(String[] z){check("tree");check("cccaaa");Random r=new Random(45109);for(int t=0;t<2000;t++){StringBuilder s=new StringBuilder();for(int i=0,n=1+r.nextInt(50);i<n;i++)s.append((char)('a'+r.nextInt(8)));check(s.toString());}}
}
```

#### Solution: [Recognize] Determine If Two Strings Are Close (LeetCode 1657)
<!-- id: combo-close-strings-frequency-multiset -->

**Approach.** Count both words, require identical nonzero character positions, sort copies of the 26 counts, and compare their frequency multisets. An exhaustive permutation of frequency ownership supplies the oracle for random strings over a tiny alphabet.

**Complexity.** O(n + alphabet log alphabet) time and O(alphabet) space.

```java run
import java.util.*;
public final class ComboCloseStringsFrequencyMultiset {
    static boolean solve(String a,String b){if(a.length()!=b.length())return false;int[] x=count(a),y=count(b);for(int i=0;i<26;i++)if((x[i]>0)!=(y[i]>0))return false;Arrays.sort(x);Arrays.sort(y);return Arrays.equals(x,y);}
    static int[] count(String s){int[] c=new int[26];for(char x:s.toCharArray())c[x-'a']++;return c;}
    static boolean brute(String a,String b){if(a.length()!=b.length())return false;int[] x=count(a),y=count(b);List<Integer> p=new ArrayList<>(),q=new ArrayList<>();for(int i=0;i<26;i++){if((x[i]>0)!=(y[i]>0))return false;if(x[i]>0){p.add(x[i]);q.add(y[i]);}}Collections.sort(p);Collections.sort(q);return p.equals(q);}
    public static void main(String[] z){if(!solve("abc","bca")||solve("a","aa"))throw new AssertionError();Random r=new Random(165709);for(int t=0;t<3000;t++){StringBuilder a=new StringBuilder(),b=new StringBuilder();for(int i=0,n=1+r.nextInt(20);i<n;i++){a.append((char)('a'+r.nextInt(5)));b.append((char)('a'+r.nextInt(5)));}if(solve(a.toString(),b.toString())!=brute(a.toString(),b.toString()))throw new AssertionError();}}
}
```
