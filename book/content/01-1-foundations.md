::: {.chapter .p1}
::: opener
[Part I · Pillar 1]{.part-label}

[1]{.num}

# Data Structures and Algorithms {#ch1}

[Coding rounds for network engineers: from a blank screen to a longest-prefix-match table, an LRU cache and a token bucket.]{.promise}

1. [1.0 How network-company coding rounds work]{} [MUST]{}
2. [1.1 Complexity and the problem-solving routine]{} [MUST]{}
3. [1.2 Arrays: two pointers, windows, prefix sums]{} [MUST]{}
4. [1.3 Hashing: maps and sets]{} [MUST]{}
5. [1.4 Strings and parsing network data]{} [MUST]{}
6. [1.5 Bit manipulation and subnet code]{} [MUST]{}
7. [1.6 Linked lists in C]{} [MUST]{}
8. [1.7 Stacks, queues, ring buffers, deques]{} [MUST]{}
9. [1.8 Trees and binary search trees]{} [MUST]{}
10. [1.9 Tries and longest-prefix match]{} [MUST]{}
11. [1.10 Heaps and priority queues]{} [SHOULD]{}
12. [1.11 Graphs: networks are graphs]{} [MUST]{}
13. [1.12 Recursion and backtracking]{} [SHOULD]{}
14. [1.13 Sorting, binary search, intervals]{} [MUST]{}
15. [1.14 Dynamic programming essentials]{} [SHOULD]{}
16. [1.15 Design-style coding: caches and rate limiters]{} [MUST]{}
17. [1.16 Finite-state machines]{} [SHOULD]{}
18. [1.17 Testing your own code]{} [MUST]{}
:::

## [1.0]{.sec}How network-company coding rounds work [Must · ■□□]{.tag} {#s1-0}

Candidate reports describe the coding rounds of networking companies as narrower than those of general software firms. The problems are mostly easy or medium, they favour linked lists, bits, strings and trees over contest techniques, and several companies expect the solution in C. Hence, breadth and clean code earn more than obscure algorithms. The table summarises what candidates report; it is indicative, not a guarantee, and every drive should be checked against its own invitation.

| Company | Reported shape of the coding part | Topics most often reported |
|---|---|---|
| Cisco | online test, about 90 min: 1–2 coding problems and 30–40 MCQs; C, Python or Java | graphs (snake and ladder), strings, longest substring, bits, pointer output |
| Juniper | online test, about 90 min: 1–3 coding problems and about 35 MCQs | merge sorted arrays, multiply without `*`, list cycles, bits, state machines |
| Qualcomm | written test then 2–3 technical rounds | bit counting and flipping, struct padding, `volatile` |
| Arista | online test in C or C++, then a shared-editor onsite | linked lists from scratch, BST operations, program memory layout |
| Google | phone screen with 1–2 problems | tries and prefix match on IPs, log parsing, frequency sorting |
| Microsoft | standard software loop | LRU cache with TTL and thread safety, rate limiters |
| Amazon (network development) | online test of one easy and one medium problem, plus Python in the loop | strings, trees, graphs, LRU variants |
| Nokia | aptitude test and two simple programs | list loops and intersection, depth-first search with a stack |
| Broadcom | phone and onsite rounds | bits, list reversal, stacks, queues, state machines |

Three consequences follow. First, a test with partial marks per test case rewards a correct brute force submitted early; one should read all problems, bank the easiest, then return. Secondly, an onsite round is judged on the visible process as much as on the code, which is the reason for the routine of [§1.1](#s1-1){.ref}. Thirdly, the language is a decision to be made before the clock starts.

| If … | Write in … | Because |
|---|---|---|
| the role mentions embedded, data plane, drivers or the company is Qualcomm, Broadcom or Arista | C | pointer questions are the point; the STL is unavailable or disapproved |
| the role is network development or automation | Python | brevity; built-in dictionaries, `heapq`, `deque` |
| the test allows it and you know the STL | C++ | brevity close to Python, with no hidden costs |

This chapter uses C++ for general algorithms and C for linked lists, bit tricks and networking problems, as the interviews do. One language is used for each solution; where Python differs materially, one sentence says so.

::: example
**A 90-minute test with about 40 multiple-choice questions and two coding problems.** The format is typical of the reports for Cisco and Juniper; the aim is to spend the time where marks are cheapest.

1. Minutes 0–3: read every question title and the marking scheme. Note whether wrong answers are penalised and whether sections lock after submission.
2. Minutes 3–33: answer the multiple-choice questions in two passes. In the first, answer anything that takes under 45 seconds and flag the rest; in the second, return to the flagged ones in order of confidence. Never leave a blank if there is no penalty.
3. Minutes 33–38: read both coding problems and their constraints, and choose the easier one first.
4. Minutes 38–63: solve the first problem. Submit a correct brute force early, because most platforms award marks per passed test case, and then optimise.
5. Minutes 63–83: solve the second problem in the same way.
6. Minutes 83–90: re-run the edge cases of [§1.17](#s1-17){.ref} on both, then submit.

| Block | Minutes | Rule |
|---|---|---|
| read and plan | 3 | titles, marking, negative marking |
| multiple choice | 30 | 45 seconds each, two passes |
| coding problem 1 | 25 | brute force first |
| coding problem 2 | 20 | partial credit counts |
| buffer | 12 | edge cases, resubmission |

[Result: a plan that banks the certain marks first. Rehearse it on a timer before the real test.]{.result}
:::

::: lens
[CISCO · JUNIPER · ARISTA]{.co}

Interviewers ask for a complete, compilable function, not pseudocode. A strong answer states the signature and the edge cases first, writes the code in small named steps, and ends by tracing one example aloud. Expect "now do it without extra memory" or "now in C" as the follow-up.
:::

## [1.1]{.sec}Complexity and the problem-solving routine [Must · ■□□]{.tag} {#s1-1}

::: bigidea
The input size in the problem statement tells us which algorithms can finish in time, because a judge performs about 10^8 simple operations per second.
:::

[**Big-O** — an upper bound on how the work grows with the input size *n*, ignoring constants and lower-order terms.]{.margin}We count growth, not seconds. An algorithm taking *c·n* steps and one taking *c′·n + 50* steps are both O(*n*), since for large *n* the constants do not change the shape of the curve. The three loops below show the three cases that cover most code.

```c
for (i = 0; i < n; i++) sum += a[i];  /* O(n): one pass          */
for (i = 0; i < n; i++)
    for (j = i + 1; j < n; j++) pairs++;  /* O(n^2): n(n-1)/2 steps  */
while (n) n >>= 1;  /* O(log n): halves n      */
```

Consider a switch. Flooding a frame to every port costs O(*p*) for *p* ports, whereas finding the egress port in the MAC table costs O(1) on average because the table is hashed. Thus, the data structure, not the hardware speed, sets the cost per frame.

**Reading the constraints.** A test limits *n*, and the limit selects the algorithm. At *n* = 10^5 an O(*n*²) method needs 10^10 steps and fails, whereas O(*n* log *n*) needs about 1.7 × 10^6 and passes. The full table from *n* ≤ 12 up to *n* ≤ 10^9 is in [the Revision Spread](#rv1){.ref}; the two rules to remember are that 10^5 allows O(*n* log *n*) and 10^3–10^4 allows O(*n*²). Python is slower by a factor of 10 to 50, so one steps down a row.

**Space and the call stack.** A recursive call stores a frame holding its arguments, locals and return address. Hence, a recursion of depth *d* uses O(*d*) memory even when it allocates nothing, and a depth of 10^6 overflows a typical 8 MB stack. Space counts the extra memory only; the input and the required output are excluded, so "O(1) extra" permits a few variables.

**Amortised cost.** A dynamic array doubles its capacity when full. A push is normally one write, but a push into a full array copies every element. Sixteen pushes starting from capacity one copy 1 + 2 + 4 + 8 = 15 elements in total, fewer than the number of pushes. In general the copies sum to less than 2*n*, so the cost per push averages to O(1); we call this an *amortised* bound. It holds for the whole sequence, not for each push.

| Push number | 1 | 2 | 3 | 5 | 9 | 17 |
|---|---|---|---|---|---|---|
| Capacity after | 1 | 2 | 4 | 8 | 16 | 32 |
| Elements copied | 0 | 1 | 2 | 4 | 8 | 16 |

### Counting operations in practice

The table gives the number of steps for *n* = 10^5, and the time they take at 10^8 steps per second. It shows why the ladder of growth rates, and not the constant factors, decides whether a solution passes.

| Growth | Steps for *n* = 10^5 | Time at 10^8 steps/s | Typical source |
|---|---|---|---|
| O(1) | 1 | instant | array index, hash lookup |
| O(log *n*) | 17 | instant | binary search, heap operation |
| O(*n*) | 10^5 | 1 ms | one pass |
| O(*n* log *n*) | 1.7 × 10^6 | 17 ms | sorting |
| O(*n*²) | 10^10 | 100 s | all pairs |
| O(2^*n*) | more than the atoms in the universe | never | all subsets |

<figure>
<svg viewBox="0 0 420 190" width="454">
<text class="sm" x="10" y="14" text-anchor="start">steps for n = 10^5 (log scale, one tick per power of ten)</text><line class="lg" x1="90" y1="26" x2="90" y2="150"/><text class="sm" x="90" y="162" text-anchor="middle">0</text><line class="lg" x1="120" y1="26" x2="120" y2="150"/><text class="sm" x="120" y="162" text-anchor="middle"></text><line class="lg" x1="150" y1="26" x2="150" y2="150"/><text class="sm" x="150" y="162" text-anchor="middle">2</text><line class="lg" x1="180" y1="26" x2="180" y2="150"/><text class="sm" x="180" y="162" text-anchor="middle"></text><line class="lg" x1="210" y1="26" x2="210" y2="150"/><text class="sm" x="210" y="162" text-anchor="middle">4</text><line class="lg" x1="240" y1="26" x2="240" y2="150"/><text class="sm" x="240" y="162" text-anchor="middle"></text><line class="lg" x1="270" y1="26" x2="270" y2="150"/><text class="sm" x="270" y="162" text-anchor="middle">6</text><line class="lg" x1="300" y1="26" x2="300" y2="150"/><text class="sm" x="300" y="162" text-anchor="middle"></text><line class="lg" x1="330" y1="26" x2="330" y2="150"/><text class="sm" x="330" y="162" text-anchor="middle">8</text><line class="lg" x1="360" y1="26" x2="360" y2="150"/><text class="sm" x="360" y="162" text-anchor="middle"></text><line class="lg" x1="390" y1="26" x2="390" y2="150"/><text class="sm" x="390" y="162" text-anchor="middle">10</text><text class="lbl" x="10" y="41" text-anchor="start">O(1)</text><rect class="fill" x="90" y="30" width="2" height="14"/><text class="lbl" x="10" y="65" text-anchor="start">O(log n)</text><rect class="fill" x="90" y="54" width="36.9" height="14"/><text class="lbl" x="10" y="89" text-anchor="start">O(n)</text><rect class="fill" x="90" y="78" width="150" height="14"/><text class="lbl" x="10" y="113" text-anchor="start">O(n log n)</text><rect class="fill" x="90" y="102" width="186.9" height="14"/><text class="lbl" x="10" y="137" text-anchor="start">O(n^2)</text><rect class="fill" x="90" y="126" width="300" height="14"/><line class="acc dash" x1="330" y1="22" x2="330" y2="150"/><text class="acct" x="334" y="22" text-anchor="start">1 s of work: 10^8</text><text class="sm" x="210" y="176" text-anchor="middle">exponent of 10</text>
</svg>
<figcaption><b>Figure 1.1</b> Growth rates at n = 10^5. The accent line is the budget of about 10^8 simple steps per second; quadratic work lies two decades beyond it.</figcaption>
</figure>

**Recursion.** To find the cost of a recursive function, write the recurrence and solve it. A function that makes two calls on halves and does a linear amount of work, `T(n) = 2T(n/2) + O(n)`, as in merge sort, costs O(*n* log *n*): there are log *n* levels and each level does O(*n*) work in total. A function that halves and does constant work, `T(n) = T(n/2) + O(1)`, as in binary search, costs O(log *n*). A function that makes two calls on `n - 1`, `T(n) = 2T(n-1) + O(1)`, costs O(2^*n*), which is why the naive Fibonacci function is unusable beyond *n* ≈ 40. Remembering the results of earlier calls, termed *memoisation*, removes the repeated work and reduces it to O(*n*):

```cpp
long long fib(int n, vector<long long>& memo) {   // memo sized n + 1, zeros
    if (n < 2) return n;
    if (memo[n]) return memo[n];                    // already computed
    return memo[n] = fib(n - 1, memo) + fib(n - 2, memo);
}
```

The same idea, applied to a table filled in order, is dynamic programming ([§1.14](#s1-14){.ref}). Further, the *best*, *average* and *worst* cases may differ: a hash lookup is O(1) on average but O(*n*) at worst, and quicksort is O(*n* log *n*) on average but O(*n*²) at worst. In an interview one states which case is meant.

### The six-step routine

A visible process earns marks even when the code is unfinished. The steps are: (i) *understand*, by restating the problem and asking about size, duplicates, negatives and empty input; (ii) *examples*, by working one by hand; (iii) *brute force*, stated with its complexity; (iv) *optimise*, by finding the repeated work; (v) *code*; and (vi) *test*, by tracing the example and the edge cases of [§1.17](#s1-17){.ref}.

::: example
**Two Sum, through all six steps.** Given an array of integers and a target, return the indices of two elements that add to the target. Exactly one answer exists and an element may not be used twice.

1. *Understand.* Ask whether the array is sorted (no), whether it may hold negatives (yes), and what to return when no pair exists (an empty result).
2. *Example.* `[2, 7, 11, 15]`, target 9 gives indices `{0, 1}`.
3. *Brute force.* Test every pair: O(*n*²) time, O(1) space.
4. *Optimise.* The inner loop searches for `target - a[i]`. A hash map from value to index answers that search in O(1), so one pass suffices.
5. *Code.* Below.
6. *Test.* Trace the example, then `[3, 3]` with target 6 (a duplicate value) and a single element.

```cpp
vector<int> twoSum(const vector<int>& a, int target) {
    unordered_map<int, int> seen;                 // value -> index
    for (int i = 0; i < (int)a.size(); ++i) {
        auto it = seen.find(target - a[i]);
        if (it != seen.end()) return {it->second, i};
        seen[a[i]] = i;  // insert after the lookup
    }
    return {};
}
```

| i | a[i] | need | in map? | map after |
|---|---|---|---|---|
| 0 | 2 | 7 | no | {2→0} |
| 1 | 7 | 2 | yes, index 0 | return {0, 1} |

[Result: O(*n*) time and O(*n*) space. Inserting after the lookup is what prevents an element pairing with itself.]{.result}
:::

::: check
1. What is the complexity of `for (i = 1; i < n; i *= 2) work();`? [^c1-1]
2. A function recurses to depth *n* and allocates nothing. What is its space complexity? [^c1-2]
3. Why is appending to a dynamic array O(1) amortised although one push can copy *n* elements? [^c1-3]
:::

[^c1-1]: O(log *n*), because *i* doubles each time.
[^c1-2]: O(*n*), from the call stack.
[^c1-3]: Copies occur only at doublings and total fewer than 2*n* over *n* pushes.

## [1.2]{.sec}Arrays: two pointers, windows and prefix sums [Must · ■□□]{.tag} {#s1-2}

::: bigidea
Most array problems become linear when we maintain two indices or one running total, because each element is then inspected a constant number of times.
:::

An array stores its elements contiguously, so the address of `a[i]` is `base + i * sizeof(T)` and indexing costs O(1). For the same reason, inserting or deleting in the middle costs O(*n*), since the later elements must move. A two-dimensional array in C is stored row by row, so `m[r][c]` sits at offset `r * cols + c`; scanning along a row is therefore faster than scanning down a column, because it follows memory order.

<figure>
<svg viewBox="0 0 390 118" width="421">
<text class="sm" x="10" y="14" text-anchor="start">int a[6], 4 bytes per element, base address 0x1000</text><rect class="box" style="fill:none" x="20" y="30" width="60" height="26"/><text class="mono" x="50" y="47" text-anchor="middle">a[0]</text><text class="sm" x="50" y="72" text-anchor="middle">0x1000</text><rect class="box" style="fill:none" x="80" y="30" width="60" height="26"/><text class="mono" x="110" y="47" text-anchor="middle">a[1]</text><text class="sm" x="110" y="72" text-anchor="middle">0x1004</text><rect class="box" style="fill:none" x="140" y="30" width="60" height="26"/><text class="mono" x="170" y="47" text-anchor="middle">a[2]</text><text class="sm" x="170" y="72" text-anchor="middle">0x1008</text><rect class="hl" x="200" y="30" width="60" height="26"/><rect class="box" style="fill:none" x="200" y="30" width="60" height="26"/><text class="mono" x="230" y="47" text-anchor="middle">a[3]</text><text class="sm" x="230" y="72" text-anchor="middle">0x100c</text><rect class="box" style="fill:none" x="260" y="30" width="60" height="26"/><text class="mono" x="290" y="47" text-anchor="middle">a[4]</text><text class="sm" x="290" y="72" text-anchor="middle">0x1010</text><rect class="box" style="fill:none" x="320" y="30" width="60" height="26"/><text class="mono" x="350" y="47" text-anchor="middle">a[5]</text><text class="sm" x="350" y="72" text-anchor="middle">0x1014</text><path class="accf" d="M200,88 l-4,7 l8,0 z"/><text class="lbl" x="200" y="108" text-anchor="middle">address of a[3] = 0x1000 + 3 &#42; 4 = 0x100C</text>
</svg>
<figcaption><b>Figure 1.2</b> An array is one contiguous block. The address of a[i] is base + i times the element size, so indexing is one multiplication and one addition.</figcaption>
</figure>

### Two pointers, opposite ends

*Idea.* On a sorted array, one pointer at each end moves inward, and each step discards an element that cannot be part of any answer. *Recognise:* "sorted", "pair with sum", "palindrome", "container". *Complexity:* O(*n*) time, O(1) space.

<figure>
<svg viewBox="0 0 360 190" width="389"><defs><marker id="a1" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#1A1D23"/></marker></defs>
<text class="sm" x="20" y="14" text-anchor="start">start: L = 0, R = 5, a[L] + a[R] = 12 > 10, so R moves left</text><rect class="box" style="fill:none" x="20" y="40" width="30" height="24"/>
<text class="mono" x="35.0" y="55.0" text-anchor="middle">1</text>
<text class="sm" x="35.0" y="74" text-anchor="middle">0</text>
<rect class="box" style="fill:none" x="50" y="40" width="30" height="24"/>
<text class="mono" x="65.0" y="55.0" text-anchor="middle">3</text>
<text class="sm" x="65.0" y="74" text-anchor="middle">1</text>
<rect class="box" style="fill:none" x="80" y="40" width="30" height="24"/>
<text class="mono" x="95.0" y="55.0" text-anchor="middle">4</text>
<text class="sm" x="95.0" y="74" text-anchor="middle">2</text>
<rect class="box" style="fill:none" x="110" y="40" width="30" height="24"/>
<text class="mono" x="125.0" y="55.0" text-anchor="middle">6</text>
<text class="sm" x="125.0" y="74" text-anchor="middle">3</text>
<rect class="box" style="fill:none" x="140" y="40" width="30" height="24"/>
<text class="mono" x="155.0" y="55.0" text-anchor="middle">8</text>
<text class="sm" x="155.0" y="74" text-anchor="middle">4</text>
<rect class="box" style="fill:none" x="170" y="40" width="30" height="24"/>
<text class="mono" x="185.0" y="55.0" text-anchor="middle">11</text>
<text class="sm" x="185.0" y="74" text-anchor="middle">5</text><path class="accf" d="M35,38 l-4,-7 l8,0 z"/><text class="lbl" x="35" y="28" text-anchor="middle">L</text><path class="accf" d="M185,38 l-4,-7 l8,0 z"/><text class="lbl" x="185" y="28" text-anchor="middle">R</text><text class="sm" x="20" y="112" text-anchor="start">end: L = 2, R = 3, 4 + 6 = 10, found</text><rect class="box" style="fill:none" x="20" y="136" width="30" height="24"/>
<text class="mono" x="35.0" y="151.0" text-anchor="middle">1</text>
<text class="sm" x="35.0" y="170" text-anchor="middle">0</text>
<rect class="box" style="fill:none" x="50" y="136" width="30" height="24"/>
<text class="mono" x="65.0" y="151.0" text-anchor="middle">3</text>
<text class="sm" x="65.0" y="170" text-anchor="middle">1</text>
<rect class="hl" x="80" y="136" width="30" height="24"/>
<rect class="box" style="fill:none" x="80" y="136" width="30" height="24"/>
<text class="mono" x="95.0" y="151.0" text-anchor="middle">4</text>
<text class="sm" x="95.0" y="170" text-anchor="middle">2</text>
<rect class="hl" x="110" y="136" width="30" height="24"/>
<rect class="box" style="fill:none" x="110" y="136" width="30" height="24"/>
<text class="mono" x="125.0" y="151.0" text-anchor="middle">6</text>
<text class="sm" x="125.0" y="170" text-anchor="middle">3</text>
<rect class="box" style="fill:none" x="140" y="136" width="30" height="24"/>
<text class="mono" x="155.0" y="151.0" text-anchor="middle">8</text>
<text class="sm" x="155.0" y="170" text-anchor="middle">4</text>
<rect class="box" style="fill:none" x="170" y="136" width="30" height="24"/>
<text class="mono" x="185.0" y="151.0" text-anchor="middle">11</text>
<text class="sm" x="185.0" y="170" text-anchor="middle">5</text><path class="accf" d="M95,134 l-4,-7 l8,0 z"/><text class="lbl" x="95" y="124" text-anchor="middle">L</text><path class="accf" d="M125,134 l-4,-7 l8,0 z"/><text class="lbl" x="125" y="124" text-anchor="middle">R</text><text class="sm" x="225" y="52" text-anchor="start">sum too large: R--</text><text class="sm" x="225" y="66" text-anchor="start">sum too small: L++</text><text class="sm" x="225" y="80" text-anchor="start">sum equal: answer</text>
</svg>
<figcaption><b>Figure 1.3</b> Opposite-end pointers on a sorted array with target 10. Each step discards one element that cannot belong to any answer, so at most n steps occur.</figcaption>
</figure>

```cpp
pair<int,int> pairSum(const vector<int>& a, long long t) {   // a sorted
    int l = 0, r = (int)a.size() - 1;
    while (l < r) {
        long long s = (long long)a[l] + a[r];
        if (s == t) return {l, r};
        if (s < t) ++l; else --r;  // too small: need a larger left value
    }
    return {-1, -1};
}
```

The argument for correctness is that if `a[l] + a[r]` exceeds *t*, then `a[r]` plus any element at or right of `l` also exceeds *t*, so `r` can move without losing an answer. The same argument for `s < t` justifies moving `l`. For `[1, 3, 4, 6, 8, 11]` and *t* = 10 the pointers visit (0,5) → (0,4) → (1,4) → (1,3) → (2,3), and the last pair sums to 10.

### Two pointers, read and write

*Idea.* A fast index `r` reads every element; a slow index `w` marks the end of the answer built so far. *Recognise:* "in place", "remove duplicates", "move zeroes", "partition". *Complexity:* O(*n*) time, O(1) space.

```cpp
int dedupe(vector<int>& a) {  // a sorted; returns the new length
    int w = 0;                          // a[0..w) holds the answer so far
    for (int r = 0; r < (int)a.size(); ++r)
        if (w == 0 || a[r] != a[w - 1]) a[w++] = a[r];
    return w;
}
```

| r | a[r] | compared with | action | answer so far |
|---|---|---|---|---|
| 0 | 1 | none | write | 1 |
| 1 | 1 | a[w-1] = 1 | skip | 1 |
| 2 | 2 | 1 | write | 1 2 |
| 3 | 2 | 2 | skip | 1 2 |
| 4 | 3 | 2 | write | 1 2 3 |

::: trap
*Claim:* compare `a[r]` with `a[r-1]` to detect a duplicate. *Why it is wrong:* once the writer has overwritten earlier cells, `a[r-1]` may no longer be the previous kept value. *Correct statement:* compare with `a[w-1]`, the last element of the answer, and never write before the cell has been read.
:::

### Three-way partition (the Dutch national flag)

*Idea.* To sort an array that holds only three distinct values in one pass, keep three regions: values equal to the first class at the left, the second class in the middle, and the third class at the right, with an unexamined region between the middle and the right. The same partition step sorts packets into three priority classes in place, and it is the core of quicksort for inputs with many equal keys. *Recognise:* "sort an array of 0, 1 and 2", "partition around a pivot", "segregate". *Complexity:* O(*n*) time, O(1) space, one pass.

```cpp
void sortColors(vector<int>& a) {        // values 0, 1, 2 only
    int lo = 0, mid = 0, hi = (int)a.size() - 1;
    while (mid <= hi) {                  // [mid, hi] is unexamined
        if (a[mid] == 0)      swap(a[lo++], a[mid++]);
        else if (a[mid] == 1) ++mid;
        else                  swap(a[mid], a[hi--]);   // do not advance mid
    }
}
```

The invariant is: `a[0..lo)` holds zeros, `a[lo..mid)` holds ones, `a[hi+1..n)` holds twos. A value swapped in from the right has not been examined, so `mid` stays; a value swapped in from the left is a one and is already in its region.

| lo | mid | hi | `a[mid]` | action | array after |
|---|---|---|---|---|---|
| 0 | 0 | 5 | 2 | swap with `a[hi]` | 0 0 2 1 1 2 |
| 0 | 0 | 4 | 0 | `lo++`, `mid++` | 0 0 2 1 1 2 |
| 1 | 1 | 4 | 0 | `lo++`, `mid++` | 0 0 2 1 1 2 |
| 2 | 2 | 4 | 2 | swap with `a[hi]` | 0 0 1 1 2 2 |
| 2 | 2 | 3 | 1 | `mid++` | 0 0 1 1 2 2 |
| 2 | 3 | 3 | 1 | `mid++`, loop ends | 0 0 1 1 2 2 |

[Starting array `2 0 2 1 1 0`; result `0 0 1 1 2 2`. The classic bug is advancing `mid` after swapping with `hi`, which skips an unexamined value.]{.result}

### Sliding window, fixed size

*Idea.* Instead of re-summing *k* elements for each position, add the entering element and subtract the leaving one. *Recognise:* "subarray of size *k*", "every window of length *k*". *Complexity:* O(*n*) time, O(1) space.

```cpp
long long maxSumK(const vector<int>& a, int k) {  // requires 1 <= k <= n
    long long cur = 0, best = LLONG_MIN;
    for (int i = 0; i < (int)a.size(); ++i) {
        cur += a[i];
        if (i >= k) cur -= a[i - k];                 // element leaving
        if (i >= k - 1) best = max(best, cur);       // window is full
    }
    return best;
}
```

The classic bug is the off-by-one at eviction: the element leaving when index `i` enters is `a[i-k]`, not `a[i-k+1]`. For `[2, 1, 5, 1, 3, 2]` with *k* = 3 the window sums are 8, 7, 9, 6, so the answer is 9.

### Sliding window, variable size

*Idea.* The right edge advances every step; the left edge advances only while the window violates a condition. Each index enters and leaves once, so the work is O(*n*) although two loops are nested. *Recognise:* "longest or shortest contiguous subarray or substring such that …". *Complexity:* O(*n*) time, O(*alphabet*) space.

<figure>
<svg viewBox="0 0 330 152" width="356">
<text class="sm" x="20" y="14" text-anchor="start">s = abcabcbb. State after right = 4 (character b); the repeat moved left from 0 to 2.</text><rect class="box" style="fill:none" x="20" y="40" width="34" height="24"/>
<text class="mono" x="37.0" y="55.0" text-anchor="middle">a</text>
<text class="sm" x="37.0" y="74" text-anchor="middle">0</text>
<rect class="box" style="fill:none" x="54" y="40" width="34" height="24"/>
<text class="mono" x="71.0" y="55.0" text-anchor="middle">b</text>
<text class="sm" x="71.0" y="74" text-anchor="middle">1</text>
<rect class="hl" x="88" y="40" width="34" height="24"/>
<rect class="box" style="fill:none" x="88" y="40" width="34" height="24"/>
<text class="mono" x="105.0" y="55.0" text-anchor="middle">c</text>
<text class="sm" x="105.0" y="74" text-anchor="middle">2</text>
<rect class="hl" x="122" y="40" width="34" height="24"/>
<rect class="box" style="fill:none" x="122" y="40" width="34" height="24"/>
<text class="mono" x="139.0" y="55.0" text-anchor="middle">a</text>
<text class="sm" x="139.0" y="74" text-anchor="middle">3</text>
<rect class="hl" x="156" y="40" width="34" height="24"/>
<rect class="box" style="fill:none" x="156" y="40" width="34" height="24"/>
<text class="mono" x="173.0" y="55.0" text-anchor="middle">b</text>
<text class="sm" x="173.0" y="74" text-anchor="middle">4</text>
<rect class="box" style="fill:none" x="190" y="40" width="34" height="24"/>
<text class="mono" x="207.0" y="55.0" text-anchor="middle">c</text>
<text class="sm" x="207.0" y="74" text-anchor="middle">5</text>
<rect class="box" style="fill:none" x="224" y="40" width="34" height="24"/>
<text class="mono" x="241.0" y="55.0" text-anchor="middle">b</text>
<text class="sm" x="241.0" y="74" text-anchor="middle">6</text>
<rect class="box" style="fill:none" x="258" y="40" width="34" height="24"/>
<text class="mono" x="275.0" y="55.0" text-anchor="middle">b</text>
<text class="sm" x="275.0" y="74" text-anchor="middle">7</text><path class="acc" d="M90,76 v6 h98 v-6"/><path class="accf" d="M105,38 l-4,-7 l8,0 z"/><text class="lbl" x="105" y="28" text-anchor="middle">left</text><path class="accf" d="M173,38 l-4,-7 l8,0 z"/><text class="lbl" x="173" y="28" text-anchor="middle">right</text><text class="lbl" x="139.0" y="96" text-anchor="middle">window = "cab", length 3</text><text class="sm" x="20" y="128" text-anchor="start">every count in the window is at most 1, so the window is valid</text><text class="sm" x="20" y="142" text-anchor="start">best = 3 so far; the next c repeats, so left moves to 3 (shrink with while)</text>
</svg>
<figcaption><b>Figure 1.4</b> Variable sliding window. The right edge always advances; the left edge advances only to restore the invariant.</figcaption>
</figure>

```cpp
int lengthOfLongest(const string& s) {  // longest run with no repeats
    int cnt[256] = {0}, best = 0, left = 0;
    for (int right = 0; right < (int)s.size(); ++right) {
        ++cnt[(unsigned char)s[right]];
        while (cnt[(unsigned char)s[right]] > 1)  // shrink: while, not if
            --cnt[(unsigned char)s[left++]];
        best = max(best, right - left + 1);
    }
    return best;
}
```

| right | char | window after shrinking | length | best |
|---|---|---|---|---|
| 0 | a | a | 1 | 1 |
| 1 | b | ab | 2 | 2 |
| 2 | c | abc | 3 | 3 |
| 3 | a | bca | 3 | 3 |
| 4 | b | cab | 3 | 3 |
| 5 | c | abc | 3 | 3 |
| 6 | b | cb | 2 | 3 |
| 7 | b | b | 1 | 3 |

At `right = 6` the window `abc` meets a second `b`; the loop removes `a`, then `b`, leaving `cb`. A single `if` would remove only `a` and leave the invalid window `bcb`. This is the standard bug, and it is the reason the template uses `while`.

### Prefix sums and the hash map

*Idea.* Let `pre[i]` be the sum of the first *i* elements. The sum of `a[j..i)` is `pre[i] - pre[j]`, so "a subarray with sum *k* ends here" means "an earlier prefix equals `pre[i] - k`". A map from prefix value to occurrence count answers this in O(1). *Recognise:* "subarray sum equals *k*", negatives present (which defeats a sliding window), "divisible by *k*". *Complexity:* O(*n*) time and space.

```cpp
int subarraySum(const vector<int>& a, int k) {
    unordered_map<long long, int> seen{{0, 1}};  // the empty prefix, seeded
    long long pre = 0; int count = 0;
    for (int x : a) {
        pre += x;
        auto it = seen.find(pre - k);
        if (it != seen.end()) count += it->second;
        ++seen[pre];
    }
    return count;
}
```

For `[1, 2, 3, -2, 2]` and *k* = 3, the prefixes are 1, 3, 6, 4, 6. At prefix 3 we find the seed 0 (subarray `[1,2]`); at 6 we find 3 (`[3]`); at 4 we find 1 (`[2,3,-2]`); at the second 6 we find 3 again (`[3,-2,2]`). The count is 4. Omitting the seed `{0, 1}` loses every subarray that starts at index 0, which is the classic bug.

::: check
1. In `maxSumK`, why is `best` initialised to `LLONG_MIN` rather than 0? [^c1-4]
2. Why does a sliding window fail on `[1, -1, 5]` with the condition "sum at most 5"? [^c1-5]
:::

[^c1-4]: Every window sum may be negative, and 0 would then be returned wrongly.
[^c1-5]: The window sum is not monotone in its length when negatives exist, so shrinking cannot restore validity reliably; prefix sums are used instead.

## [1.3]{.sec}Hashing: maps and sets [Must · ■□□]{.tag} {#s1-3}

::: bigidea
A hash table turns "have I seen this?" from a scan into a single computed lookup, which is why so many O(*n*²) solutions collapse to O(*n*).
:::

[**Hash function** — a function mapping a key to an integer; equal keys must give equal values, and different keys should rarely collide.]{.margin}A hash table stores each key in a bucket chosen by `hash(key) mod m`. Two keys sharing a bucket collide, and the usual remedy, *chaining*, keeps a short list in each bucket. With a good hash and a load factor (entries per bucket) kept below about one, a lookup inspects a constant expected number of entries. Thus, insert, find and erase are O(1) on average, but O(*n*) in the worst case when many keys collide. The ordered `map` in C++ is a balanced tree instead: O(log *n*) per operation, but it keeps keys sorted.

| Need | Structure | Cost |
|---|---|---|
| membership, no order | `unordered_set` | O(1) average |
| key → value, no order | `unordered_map` | O(1) average |
| sorted iteration, nearest key | `set`, `map` | O(log *n*) |
| counts of small integers or letters | array indexed by value | O(1), smallest constant |

A switch's MAC table and a router's flow table are the networking forms of this structure: the key is the destination MAC or the 5-tuple, and the value is the egress port or the action. Further, when values are bounded by a small range, a plain array replaces the hash and is faster.

*Recognise:* "have we seen", "count occurrences", "pair that …", "group by", "first non-repeating", "duplicate". *Typical templates:* a set for membership, a map for counts, and a sorted or canonical form of an item as the key (for anagrams, the sorted letters).

<figure>
<svg viewBox="0 0 440 185" width="475"><defs><marker id="a10" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#1A1D23"/></marker></defs>
<text class="sm" x="10" y="12" text-anchor="start">bucket = key mod 6</text><rect class="box" x="10" y="22" width="30" height="22"/><text class="mono" x="25" y="37" text-anchor="middle">0</text><line class="ln" x1="40" y1="33" x2="70" y2="33" marker-end="url(#a10)"/><rect class="box" x="70" y="22" width="44" height="22"/><text class="mono" x="92" y="37" text-anchor="middle">12</text><line class="ln" x1="114" y1="33" x2="140" y2="33" marker-end="url(#a10)"/><rect class="box" x="140" y="22" width="44" height="22"/><text class="mono" x="162" y="37" text-anchor="middle">18</text><rect class="box" x="10" y="48" width="30" height="22"/><text class="mono" x="25" y="63" text-anchor="middle">1</text><text class="sm" x="60" y="63" text-anchor="start">empty</text><rect class="box" x="10" y="74" width="30" height="22"/><text class="mono" x="25" y="89" text-anchor="middle">2</text><line class="ln" x1="40" y1="85" x2="70" y2="85" marker-end="url(#a10)"/><rect class="box" x="70" y="74" width="44" height="22"/><text class="mono" x="92" y="89" text-anchor="middle">8</text><rect class="box" x="10" y="100" width="30" height="22"/><text class="mono" x="25" y="115" text-anchor="middle">3</text><line class="ln" x1="40" y1="111" x2="70" y2="111" marker-end="url(#a10)"/><rect class="box" x="70" y="100" width="44" height="22"/><text class="mono" x="92" y="115" text-anchor="middle">21</text><line class="ln" x1="114" y1="111" x2="140" y2="111" marker-end="url(#a10)"/><rect class="box" x="140" y="100" width="44" height="22"/><text class="mono" x="162" y="115" text-anchor="middle">9</text><line class="ln" x1="184" y1="111" x2="210" y2="111" marker-end="url(#a10)"/><rect class="box" x="210" y="100" width="44" height="22"/><text class="mono" x="232" y="115" text-anchor="middle">15</text><rect class="box" x="10" y="126" width="30" height="22"/><text class="mono" x="25" y="141" text-anchor="middle">4</text><text class="sm" x="60" y="141" text-anchor="start">empty</text><rect class="box" x="10" y="152" width="30" height="22"/><text class="mono" x="25" y="167" text-anchor="middle">5</text><line class="ln" x1="40" y1="163" x2="70" y2="163" marker-end="url(#a10)"/><rect class="box" x="70" y="152" width="44" height="22"/><text class="mono" x="92" y="167" text-anchor="middle">23</text><text class="sm" x="300" y="60" text-anchor="start">load factor = entries / buckets = 7 / 6</text><text class="sm" x="300" y="74" text-anchor="start">lookup(15): bucket 3, then walk</text><text class="sm" x="300" y="88" text-anchor="start">the chain 21, 9, 15</text><text class="sm" x="300" y="110" text-anchor="start">when the load factor passes 1:</text><text class="sm" x="300" y="124" text-anchor="start">double the buckets and re-insert</text>
</svg>
<figcaption><b>Figure 1.5</b> A hash table with chaining. Keys that collide share a bucket's list; the expected chain length equals the load factor.</figcaption>
</figure>

Two collision strategies exist. *Chaining* keeps a list per bucket, as drawn; deletion is easy and the table degrades gracefully when full. *Open addressing* stores entries in the array itself and probes to the next free cell (linear probing) after a collision; it is more compact and faster to scan, but it needs a load factor well below one, and deletion needs a tombstone marker. When the load factor passes a threshold the table doubles its bucket count and re-inserts every entry, an O(*n*) step that is amortised over the insertions exactly as for the dynamic array of [§1.1](#s1-1){.ref}.

::: example
**Longest consecutive sequence.** Given an unsorted array, find the length of the longest run of consecutive integers (for example 1, 2, 3, 4), in O(*n*) time.

1. Sorting gives O(*n* log *n*); the target forbids it.
2. Put all values in a set. A value *x* starts a run exactly when *x* − 1 is absent.
3. For each start, extend with `x+1, x+2, …` while present. Each element is visited once as a start-check and at most once inside a run, so the total is O(*n*).

```cpp
int longestConsecutive(const vector<int>& a) {
    unordered_set<int> s(a.begin(), a.end());
    int best = 0;
    for (int x : s) {
        if (s.count(x - 1)) continue;          // not the start of a run
        int y = x;
        while (y < INT_MAX && s.count(y + 1)) ++y;
        best = max(best, y - x + 1);               // run length
    }
    return best;
}
```

| x | x − 1 present? | run extended | length |
|---|---|---|---|
| 100 | no | 100 | 1 |
| 4 | yes | skipped | – |
| 200 | no | 200 | 1 |
| 1 | no | 1, 2, 3, 4 | 4 |

[Result for `[100, 4, 200, 1, 3, 2]`: 4. Time O(*n*), space O(*n*).]{.result}
:::

::: trap
*Claim:* `m[key]` is a harmless way to test whether a key exists. *Why it is wrong:* in C++ the subscript operator inserts a default value when the key is absent, which changes the map and its size during the test. *Correct statement:* use `find` or `count` to test, and `[]` only when inserting or incrementing is intended.
:::

### Hashing network keys: a flow table

A router or firewall keeps per-flow state in a hash table whose key is the 5-tuple (source address, destination address, source port, destination port, protocol). Two points make this a favourite question. First, one must hash the *fields*, not the bytes of the struct, because a C struct may contain padding bytes whose values are unspecified; two equal keys could then hash differently. Secondly, equality must compare the same fields.

```c
#include <stdint.h>
#include <stdbool.h>

typedef struct {
    uint32_t src, dst;
    uint16_t sport, dport;
    uint8_t  proto;
} FlowKey;

static uint32_t fnv_byte(uint32_t h, uint8_t b) {
    return (h ^ b) * 16777619u;
}

uint32_t flow_hash(const FlowKey *k) {  /* FNV-1a over the fields */
    uint32_t h = 2166136261u;
    uint32_t w[3] = { k->src, k->dst, (uint32_t)k->sport << 16 | k->dport };
    for (int i = 0; i < 3; i++)
        for (int b = 0; b < 32; b += 8)
            h = fnv_byte(h, (uint8_t)(w[i] >> b));
    return fnv_byte(h, k->proto);
}
bool flow_eq(const FlowKey *a, const FlowKey *b) {
    return a->src == b->src && a->dst == b->dst && a->sport == b->sport
        && a->dport == b->dport && a->proto == b->proto;
}
```

The bucket is `flow_hash(k) % nbuckets`. *Follow-ups.* To make the two directions of a connection land in the same entry, order the two (address, port) pairs before hashing. Equal-cost multipath forwarding applies the same idea in hardware: a hash of the 5-tuple selects the path, so all packets of a flow take one path and arrive in order, while different flows spread over the paths.

::: check
1. Which is faster for counting lowercase letters: `unordered_map<char,int>` or `int cnt[26]`? [^c1-6]
2. What is the worst-case lookup in a chained hash table, and when does it occur? [^c1-7]
:::

[^c1-6]: The array, since it has no hashing or allocation; both are O(*n*) overall.
[^c1-7]: O(*n*), when every key lands in one bucket, for example with a poor hash or adversarial input.

:::
