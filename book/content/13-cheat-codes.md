::: {.chapter .p0}
::: opener
[Part II · Cheat Codes]{.part-label}

[II]{.num}

# Cheat Codes {#ch13}

[Decoders and quick tables for the minutes when the clock is running and the explanation is already learnt.]{.promise}

1. [A1 DSA: constraints, patterns and the 45-minute round]{} [★]{}
2. [A2 Networking: mnemonics, speed tricks and reference tables]{} [★]{}
3. [A3 Online assessments: formats, pacing and elimination]{} [★]{}
4. [A4 HR: the question bank and the offer]{} [★]{}
:::

## [II.0]{.sec}How to use this part [Must · ■□□]{.tag} {#s13-0}

This part is a *decoder* layer. A table marked ★ exists nowhere else in the book and is printed here in full. Everything else is a single line that names the pillar section where the idea is taught, so that a topic is never explained twice. Consequently, if a row looks too short to learn from, the page printed beside it is the place to read.

[**Candidate reports** — anonymous, self-reported accounts on sites such as GeeksforGeeks, Glassdoor, Jointaro and Medium. They span 2016 to 2026, formats change every year, and a drive's own invitation always overrides this book.]{.margin}Wherever a table states what a company asks or how its test is laid out, the source is a set of candidate reports. We therefore write "reported" and give the year, and we never present a report as a rule. Use the tables to plan; confirm on the day.

| You have | Open |
|----------------------------------------|------------------------------|
| 30 seconds in a coding round | the decoders of [A1](#s13-1){.ref} |
| the night before a networking round | the mnemonics and tables of [A2](#s13-2){.ref} |
| an online assessment tomorrow | [A3](#s13-3){.ref}, then the mock papers of [Part III](#ch14){.ref} |
| an HR round or an offer letter | [A4](#s13-4){.ref} |

## [A1]{.sec}DSA cheat codes [Must · ■□□]{.tag} {#s13-1}

::: bigidea
A coding problem announces its algorithm twice, once in the size of its input and once in its wording, and reading both before writing anything removes most wrong starts.
:::

### The constraint decoder

The basic table, from *n* ≤ 12 to *n* ≥ 10<sup>9</sup>, is printed in the Revision Spread of Pillar 1 ([the table](#rv1){.ref}). Its rule of thumb is that a judge performs about 10<sup>8</sup> simple operations per second. For example, at *n* = 10<sup>5</sup> an O(*n* log *n*) method costs about 1.7 × 10<sup>6</sup> steps, an O(*n*√*n*) method about 3.2 × 10<sup>7</sup>, and an O(*n*²) method 10<sup>10</sup>, which is far too slow. The statement carries other numbers besides *n*, and these select the technique as well.

★ **Constraint signals other than *n*.**

| Signal in the statement | It implies | Reach for |
|------------------------|------------------------|----------------------------|
| *n* ≤ 40 | 2<sup>40</sup> is too large, but two halves of 2<sup>20</sup> are not | meet in the middle: enumerate each half, combine by sorting or hashing |
| *k* ≤ 20 with large *n* | state is a subset of *k* items | bitmask DP over *k*, 2<sup>*k*</sup> × *k* |
| values up to 10<sup>9</sup> | no array can be indexed by value | hash map, or coordinate compression after sorting |
| "return the answer modulo 10<sup>9</sup> + 7" | the count is astronomically large | DP or combinatorics; reduce after every product, in 64 bits |
| sum of *n* over all tests ≤ 2 × 10<sup>5</sup> | per-test O(*n* log *n*) is fine | never re-allocate a large array per test |
| *q* queries and *n*, *q* ≤ 10<sup>5</sup> | answer each in O(log *n*) or O(1) | preprocess once: sort, prefix sums, a Fenwick tree |
| grid up to 1000 × 1000 | 10<sup>6</sup> cells | one O(cells) BFS; avoid deep recursion |
| string length ≤ 10<sup>5</sup> | comparing all substrings is hopeless | window, hash, KMP; never O(*n*²) |
| *n* up to 10<sup>18</sup> | the loop cannot run *n* times | O(log *n*): binary search on the value, fast exponentiation |
| memory limit 256 MB | about 6 × 10<sup>7</sup> 32-bit integers in all | no 10<sup>5</sup> × 10<sup>5</sup> table; roll the DP rows |
| Python, 1 second | about 10<sup>7</sup> simple operations | built-ins (`sort`, `Counter`, `heapq`), not nested loops |
| a stream, or "one pass" | memory must stay bounded | heap of size *k*, reservoir sampling, a counter table |

### The keyword decoder

The first 31 rows of the decoder, from "sorted" to "validate a sequence of protocol events", are in the same Revision Spread ([the keyword table](#rv1){.ref}) with the section of each template. The table below holds the rows that one does not find there, with LeetCode numbers as anchors: each number names one standard problem for practice, and none is a prediction of what will be asked.

★ **Keyword decoder, second half.**

| Signal in the problem | Think | Anchors |
|------------------------------|--------------------------------|----------|
| minimum meeting rooms; peak overlap | sort starts, min-heap of end times; or a sweep line | 253, 1094 |
| insert into sorted intervals; remove fewest to avoid overlap | one linear merge; greedy by earliest end | 57, 435 |
| add *v* to every element of [*l*, *r*], many times | difference array, then one prefix pass | 1094, 1109 |
| 1 to *n* with one missing or repeated | cyclic sort, sign marking, or XOR | 268, 287, 448 |
| rotated sorted array; minimum; peak | binary search on which half is sorted | 33, 153, 162 |
| median of two sorted arrays | binary search on the partition | 4 |
| smallest window containing all of …; permutation in a string | variable window with need/have counters | 76, 567 |
| at most *K* distinct; replace at most *K* | variable window with counts | 424, 904, 1004 |
| product or sum below *K*, positives only | shrink the window while it is too large | 713, 209 |
| trapped water; container | two pointers with running maxima, or a monotonic stack | 42, 11 |
| longest palindromic substring | expand around each centre, O(*n*²) | 5 |
| matrix: rotate, spiral, zero rows | index arithmetic; transpose then reverse rows | 48, 54, 73 |
| grid: find a word or a path with moves | DFS that marks and unmarks cells | 79 |
| nearest gate; rot spreads each minute | multi-source BFS from all sources at once | 542, 994 |
| minimum steps between words or states | BFS over an implicit graph | 127 |
| edge weights are only 0 or 1 | 0-1 BFS with a deque | 1368 |
| minimise the largest edge or effort on a path | Dijkstra with max instead of sum; or binary search plus BFS | 1631, 778 |
| number of paths in a grid or DAG | DP in topological order | 62, 63 |
| copy a structure with arbitrary pointers | hash map from old node to new node | 133, 138 |
| custom alphabet order | build edges from adjacent words, topological sort | 269, 953 |
| each item once, can a total be reached | 0/1 knapsack, capacity looped downwards | 416, 494 |
| unlimited coins: fewest, or number of ways | unbounded knapsack; for ways, coins in the outer loop | 322, 518 |
| stock trades with cooldown or *k* trades | state-machine DP | 121, 309, 188 |
| split a string into valid words; decode ways | 1-D DP over prefixes | 139, 91 |
| *k*-th largest in an unsorted array or stream | heap of size *k*, or quickselect | 215, 703 |
| no two adjacent equal; cooldown between tasks | max-heap by count, greedy | 767, 621 |
| most frequent words | counter, then heap or bucket sort | 347, 692 |
| random element with equal probability from a stream | reservoir sampling | 382, 398 |
| insert, delete and random in O(1) | array plus index map; swap with the last | 380 |
| least frequently used; value at a time | frequency lists; binary search on timestamps | 460, 981 |
| find a pattern fast; repeated substring | KMP failure function or rolling hash | 28, 459 |
| maximum XOR of a pair | trie over bits | 421 |
| primes up to *n*; huge power; gcd | sieve; fast exponentiation; Euclid | 204, 50 |
| tree path sum through a node | post-order returns one-sided gain, a global holds the best | 124, 543 |
| serialise or rebuild a tree | preorder with null markers | 297, 105 |
| jump, gas station, scheduling | greedy; justify with an exchange argument | 55, 134 |
| *k*-th smallest in a sorted matrix | heap of rows, or binary search on the value | 378, 23 |
| stack or queue with an extra query | pair each element with the auxiliary value | 155, 232 |

Four of these ideas are not taught as templates in Pillar 1, so they are printed here once. Each is a few lines and is tested.

★ **Four small templates.**

```cpp
// 1. Cyclic sort: values 0..n with one missing -> send each value home
int missing(vector<int> a) {
    int n = a.size(), i = 0;
    while (i < n) {
        int j = a[i];
        if (j < n && a[j] != j) swap(a[i], a[j]);   // while, not if
        else i++;
    }
    for (i = 0; i < n; i++) if (a[i] != i) return i;
    return n;                                        // {3,0,1} -> 2
}
// 2. Difference array: add v to a[l..r] in O(1), rebuild once
//    d[l] += v; d[r+1] -= v;  then  d[i] += d[i-1]  for i = 1..n-1
// 3. Reservoir sampling of one item from a stream of unknown length
//    seen = 0; for x in stream: if rand(0..seen) == 0: chosen = x; seen++
//    (item i survives with probability 1/(i+1) * (i+1)/(i+2) * ... = 1/n)
// 4. 0-1 BFS: relax as in Dijkstra, but push_front when w == 0, push_back when w == 1
```

### The pattern index

The twenty-two patterns below are the reusable shapes of the pillar. The template of each is printed once, in the section named; the bug is the one interviewers most often see, and checking for it is the cheapest review one can run.

| # | Pattern | Trigger | Classic bug | Template |
|--|--------------|------------------|----------------------------|--------|
| 1 | Two pointers, opposite ends | sorted; pair or triple | 3Sum without skipping duplicates | [§1.2](#s1-2){.ref} |
| 2 | Two pointers, read and write | in place; remove or compact | writing over an element not yet read | [§1.2](#s1-2){.ref} |
| 3 | Fixed window | "of size *k*" | evicting `a[i-k]` off by one | [§1.2](#s1-2){.ref} |
| 4 | Variable window | longest or shortest with a condition | shrinking with `if` instead of `while` | [§1.2](#s1-2){.ref} |
| 5 | Prefix sums and a map | subarray sum equals *k* | forgetting the seed `{0: 1}` | [§1.2](#s1-2){.ref} |
| 6 | Fast and slow pointers | cycle, middle, *k*-th from end | testing `fast->next` before `fast` | [§1.6](#s1-6){.ref} |
| 7 | List reversal | reverse a part; reorder | losing `next` before re-pointing | [§1.6](#s1-6){.ref} |
| 8 | Binary search | sorted; first or last position | `(lo+hi)/2` overflow; `lo = mid` loops forever | [§1.13](#s1-13){.ref} |
| 9 | Binary search on the answer | minimise the maximum | bounds: low is the largest item, high is the sum | [§1.13](#s1-13){.ref} |
| 10 | Monotonic stack | next greater; histogram | storing values instead of indices | [§1.7](#s1-7){.ref} |
| 11 | Monotonic deque | window maximum | not popping the expired index at the front | [§1.7](#s1-7){.ref} |
| 12 | Heap | top *k*; stream median; merge *k* | C++ heap is a max-heap, Python's a min-heap | [§1.10](#s1-10){.ref} |
| 13 | Intervals | overlap; merge | sorting by end when start is needed | [§1.13](#s1-13){.ref} |
| 14 | Cyclic sort | 1 to *n*, missing or repeated | `if` instead of `while` when swapping | printed above |
| 15 | Tree DFS | depth, path, subtree | mixing the returned value with the global answer | [§1.8](#s1-8){.ref} |
| 16 | BFS | fewest steps; level order | marking visited on pop, not on push | [§1.11](#s1-11){.ref} |
| 17 | Graph DFS and cycles | components; cycle in a directed graph | two colours where three are needed | [§1.11](#s1-11){.ref} |
| 18 | Topological sort | prerequisites; ordering | not comparing the output length with *V* | [§1.11](#s1-11){.ref} |
| 19 | Union–find | dynamic connectivity; loop edge | uniting nodes instead of their roots | [§1.11](#s1-11){.ref} |
| 20 | Shortest paths | cheapest route | Dijkstra with a negative edge; no stale check | [§1.11](#s1-11){.ref} |
| 21 | Backtracking | all combinations | storing the path itself instead of a copy | [§1.12](#s1-12){.ref} |
| 22 | Dynamic programming | ways, minimum cost, reachability | wrong loop order; missing base case | [§1.14](#s1-14){.ref} |

A twenty-third card, bit tricks, is used heavily at Qualcomm and Broadcom: its bug is `1 << 31` on a signed `int`, and its home is [§1.5](#s1-5){.ref}. The shortest-path row has a networking tie, which interviewers like as a bridge question: Dijkstra is the SPF of OSPF and IS-IS ([§4.5](#s4-5){.ref}), and Bellman–Ford is the distance-vector idea of RIP.

### Problems that smell like networking

Network-company rounds dress ordinary algorithms in network clothes, and the disguise is the decoder. Each row names the task, the algorithm underneath and the question that solves it.

| The task as stated | The algorithm beneath | Solved in |
|---|---|---|
| route lookup; most specific firewall rule; delete a prefix | binary trie, deepest marked node | [Q1.19](#ps1){.ref}, [Q1.75](#ps1){.ref}, [Q1.74](#ps1){.ref}, [Q1.76](#ps1){.ref} |
| validate, convert or restore an IP string | single-scan validator; backtracking | [Q1.5](#ps1){.ref}, [Q1.39](#ps1){.ref}, [Q1.22](#ps1){.ref} |
| same subnet; network and broadcast of an address | mask and compare | [Q1.6](#ps1){.ref}, [Q1.7](#ps1){.ref} |
| merge address ranges; ranges to the fewest CIDR blocks | sort and merge; align and split | [Q1.94](#ps1){.ref}, [Q1.51](#ps1){.ref} |
| rate limiting, with bursts | token bucket; sliding window | [Q1.27](#ps1){.ref}, [Q1.101](#ps1){.ref}, [Q1.102](#ps1){.ref} |
| an ARP or route cache with expiry | hash map and doubly linked list | [Q1.26](#ps1){.ref}, [Q1.99](#ps1){.ref} |
| SPF, and "cheapest route" | Dijkstra | [Q1.20](#ps1){.ref}, [Q1.85](#ps1){.ref} |
| a routing loop; a link whose failure splits the network | cycle detection; bridges | [Q1.12](#ps1){.ref}, [Q1.87](#ps1){.ref}, [Q1.89](#ps1){.ref} |
| reorder packets by sequence number | min-heap | [Q1.81](#ps1){.ref} |
| the Internet checksum | 16-bit one's-complement sum | [Q1.52](#ps1){.ref} |
| allocate VLAN identifiers or ports | bitmap | [Q1.53](#ps1){.ref} |
| peak simultaneous flows; top sources by bytes in a huge log | sweep line; heap of size *k* | [Q1.95](#ps1){.ref}, [Q1.80](#ps1){.ref}, [Q1.37](#ps1){.ref} |
| validate a sequence of TCP events | table-driven state machine | [Q1.28](#ps1){.ref} |

### Which practice list

Four public lists are in common use: Blind 75 (the shortest), NeetCode 150 (the same families, more depth), the Striver SDE and A2Z sheets (broad, many topics), and Sean Prashad's list grouped by pattern. They overlap heavily, so one should be chosen and finished. For this book's readers the order is: the pattern families of the NeetCode list for breadth, then the networking problems of the table above, which no public list collects, and then the C output traps of [§2.15](#s2-15){.ref}, because Qualcomm, Broadcom and Arista examine C directly. Re-solve a problem from a blank page on the third and fourteenth day after the first attempt ([the calendar](#s15-2){.ref}), and retire it once it is solved without hints in under 25 minutes.

### The Big-O and edge-case cards

The data-structure, sorting and graph tables, the recurrences and the landmark numbers (log<sub>2</sub> 10<sup>6</sup> ≈ 20, `INT_MAX` ≈ 2.1 × 10<sup>9</sup>) are in the Revision Spread of Pillar 1 ([Big-O](#rv1){.ref}), as is the edge-case checklist with its networking inputs. They are not reprinted. Before saying "done", run that checklist aloud.

### The 45-minute round and the talk-track

UMPIRE, from CodePath, names six steps: **U**nderstand, **M**atch, **P**lan, **I**mplement, **R**eview, **E**valuate. They are the six-step routine of [§1.1](#s1-1){.ref} under other names, and the minute-by-minute table of [§1.17](#s1-17){.ref} already allots the time. What the book does not print elsewhere is the spoken script, which is the part that earns the communication marks.

★ **UMPIRE, minutes and phrases.**

| Step | Minutes | Say this | Not this |
|--------|------|------------------------------------|----------------|
| Understand | 0–5 | "Let me restate it: given … return …. Can the input be empty? Are values bounded? Duplicates, negatives?" | starting to type |
| Match | 5–8 | "Contiguous and longest suggests a sliding window; let me check that it fits." | "I think I have seen this one." |
| Plan | 8–15 | "A naive way is O(*n*²) over all pairs. The inner loop repeats a sum, so a prefix sum removes it. Is that direction fine with you?" | coding before agreement |
| Implement | 15–32 | "I will write `isValid` first and come back to it." / "This loop keeps the window valid." | silence for more than two minutes |
| Review | 32–38 | "Trace `[2, 7, 11, 15]`, target 9: at *i* = 1 I need 2, it is in the map at 0, so I return `[0, 1]`." | "It should work." |
| Evaluate | 38–45 | "O(*n*) time, O(*n*) space for the map. If memory is tight, sort and use two pointers: O(*n* log *n*), O(1)." | claiming a complexity without a reason |

Three further phrases cover the awkward moments. When stuck: "I am looking for repeated work; this recomputation is the candidate." When given a hint: "That helps; if the array is sorted, two pointers replace the hash set." When one finds a bug: "This fails for a single element; I will add a guard and re-run the trace." Candidate reports for Google add that interviewers expect two or three approaches and their trade-offs before any code, and one report describes an interviewer steering a candidate from union–find to BFS because the first was lengthy to write. Hence, always offer the simpler alternative and say why it suffices.

### The standard-library quick reference

The containers are taught in [§2.21](#s2-21){.ref} (C++) and [§2.16](#s2-16){.ref} to [§2.18](#s2-18){.ref} (Python); C has none, and its hash-table and list templates are in [§1.3](#s1-3){.ref} and [§1.6](#s1-6){.ref}. This table answers the question asked at the keyboard: "what do I type?"

★ **I need …, in C++ and in Python.**

| I need | C++ | Python |
|----------------|----------------------------------|--------------------------|
| sort by a key, ties by another | `sort(v.begin(), v.end(), [](auto& a, auto& b){ return a.x < b.x; })` (not stable) | `v.sort(key=lambda t: (t[0], -t[1]))` (stable) |
| a min-heap | `priority_queue<int, vector<int>, greater<int>> pq;` | `heapq.heappush(h, x)`; negate for a max-heap |
| first element not less than *x* | `lower_bound(v.begin(), v.end(), x)` | `bisect.bisect_left(a, x)` |
| frequency count | `unordered_map<int,int> c; c[x]++;` | `Counter(a)` |
| adjacency list | `vector<vector<int>> g(n); g[u].push_back(v);` | `defaultdict(list)` |
| a double-ended queue | `deque<int> d; d.push_front(x);` | `deque(); d.appendleft(x)` |
| remove duplicates after sorting | `v.erase(unique(v.begin(), v.end()), v.end());` | `sorted(set(a))` |
| prefix sums | `partial_sum(a.begin(), a.end(), p.begin());` | `list(accumulate(a))` |
| a 64-bit sum | `accumulate(a.begin(), a.end(), 0LL)` | `sum(a)` (no overflow) |
| memoisation | `vector` or `unordered_map` table | `@functools.cache` |
| "infinity" | `INT_MAX`, or `1e9` for sums; `LLONG_MAX` | `math.inf` |
| copy the current path in backtracking | `res.push_back(path);` | `res.append(path[:])` |
| fast input | `ios::sync_with_stdio(false); cin.tie(nullptr);` | `input = sys.stdin.readline` |
| delete one copy from a multiset | `ms.erase(ms.find(x));` (`erase(x)` deletes all) | `Counter` and decrement |

Four costs are worth knowing by heart. In Python, `list.pop(0)` and `insert(0, x)` are O(*n*) (use `deque`), `x in list` is O(*n*) whereas `x in set` is O(1) on average, and `s += c` in a loop can be quadratic (use `"".join`). In C++, `m[key]` on a `map` inserts a default value when the key is absent, so use `count` or `find` for a pure lookup. In C there is no library: the comparator for `qsort` must return `(x > y) - (x < y)` and never `x - y`, which overflows ([§2.5](#s2-5){.ref}); `strncpy` does not terminate a truncated string ([§1.4](#s1-4){.ref}); and `memset` is safe only for the byte patterns 0 and −1.

## [A2]{.sec}Networking cheat codes [Must · ■□□]{.tag} {#s13-2}

::: bigidea
Networking answers are lists with an order, such as states, tie-breakers and numbers, and a list is retrieved far more reliably from a hook than from a paragraph.
:::

Most reference tables already sit in the Revision Spreads of the pillars: the /8 to /32 mask table, the ports and protocol numbers, the TCP states and the IPv6 prefixes in Pillar 3 ([the spread](#rv3){.ref}), and administrative distance, the OSPF states and LSAs, the BGP best-path order and the STP timers in Pillar 4 ([the spread](#rv4){.ref}). They are not reprinted. This section holds what those spreads lack.

### The mnemonic page

Mnemonics that live elsewhere: the OSI order (*All People Seem To Need Data Processing*, [§3.2](#s3-2){.ref}), the BGP order (*N WLLA OMNI*, [§4.7](#s4-7){.ref}), the syslog levels (*Every Awesome Cisco Engineer Will Need Ice cream Daily*, [§4.13](#s4-13){.ref}) and DORA ([§3.6](#s3-6){.ref}). The rest are printed here. They are our own inventions unless stated, and a silly sentence is easier to keep than a sensible one.

★ **Mnemonics.**

| Topic | Hook | It decodes to |
|----------------|----------------------|----------------------------------------|
| TCP/IP layers, top to bottom | *Aunt Tina Is Nice* | Application, Transport, Internet, Network access |
| PDU names, top to bottom | *Do Some People Fear Birthdays* | Data, Segment, Packet, Frame, Bits |
| TCP flags in header order | *Cats Eat Under All People's Red Sofas Freely* | CWR, ECE, URG, ACK, PSH, RST, SYN, FIN |
| IPv4 flag bits | *Zero, Don't, More* | reserved 0, DF, MF |
| 802.1Q tag | *3-1-12 after 8100* | TPID 0x8100, then PCP 3 bits, DEI 1 bit, VID 12 bits |
| OSPF neighbour states | *Don't Ignore Two Excited Elephants Leaving Fridges* | Down, Init, 2-Way, ExStart, Exchange, Loading, Full. Stuck in ExStart or Exchange: MTU. Stuck in Init: one-way hellos. Stuck in 2-Way between DROthers: normal. |
| OSPF packet types 1 to 5 | *Hello Dear Little Sweet Angel* | Hello, Database Description, Link-State Request, Link-State Update, Link-State Acknowledgement |
| OSPF LSA types | *Really Nice Summaries Are Easy Now* | 1 Router, 2 Network, 3 Summary, 4 ASBR summary, 5 External, 7 NSSA external |
| BGP session states | *Idle Cats Always Open Old Envelopes* | Idle, Connect, Active, OpenSent, OpenConfirm, Established. Active means "still trying to connect", not "healthy". |
| STP 802.1D port states | *Big Lions Like Food* | Blocking, Listening, Learning, Forwarding |
| Process memory, low to high | *Terrible Dogs Bark, Hounds Squeal* | Text, Data, BSS, Heap, Stack |
| Deadlock conditions | *My Hungry Nephew Cries* | Mutual exclusion, Hold and wait, No pre-emption, Circular wait |
| Early ports | *the 21-22-23-25 walk* | FTP 21, SSH 22, Telnet 23, then SMTP 25 (24 is skipped) |

### Subnetting speed tricks

The method (block size, then the multiple not above the address) is taught in [§3.4](#s3-4){.ref} and the master table is there. Speed comes from not computing what can be recalled, so four strips are worth learning cold.

★ **Strip 1: powers of two.**

| 2<sup>0</sup> | 2<sup>1</sup> | 2<sup>2</sup> | 2<sup>3</sup> | 2<sup>4</sup> | 2<sup>5</sup> | 2<sup>6</sup> | 2<sup>7</sup> | 2<sup>8</sup> | 2<sup>9</sup> | 2<sup>10</sup> | 2<sup>11</sup> | 2<sup>12</sup> | 2<sup>16</sup> | 2<sup>20</sup> | 2<sup>24</sup> | 2<sup>32</sup> |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 | 512 | 1,024 | 2,048 | 4,096 | 65,536 | 1,048,576 | 16,777,216 | 4,294,967,296 |

★ **Strip 2: the mask octet ladder.** Each extra bit adds half of the previous step: 128, then +64, then +32 and so on. The block size is 256 minus the octet.

| Bits set in the octet | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Octet value | 128 | 192 | 224 | 240 | 248 | 252 | 254 | 255 |
| Block size | 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |

★ **Strip 3: hosts needed to prefix.** Find the first row whose usable hosts are at least the requirement. The same table reads backwards for "how many hosts fit".

| Prefix | /30 | /29 | /28 | /27 | /26 | /25 | /24 | /23 | /22 | /21 | /20 | /19 | /18 | /17 | /16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Usable hosts | 2 | 6 | 14 | 30 | 62 | 126 | 254 | 510 | 1,022 | 2,046 | 4,094 | 8,190 | 16,382 | 32,766 | 65,534 |

For subnets rather than hosts, borrow the smallest *s* with 2<sup>*s*</sup> at least the number required: 2 or fewer subnets need 1 bit, 3 or 4 need 2, 5 to 8 need 3, 9 to 16 need 4. Thus, six subnets from a /24 borrow 3 bits and give /27.

★ **Strip 4: summarising.** A run of 2<sup>*k*</sup> equal-sized blocks can become one route only if the run is contiguous and its first block starts at a multiple of the whole run. The prefix then shortens by *k*.

| Blocks in the run | 2 | 4 | 8 | 16 | 32 | 64 |
|---|---|---|---|---|---|---|
| Prefix shortens by | 1 | 2 | 3 | 4 | 5 | 6 |
| The first block must be a multiple of | 2 | 4 | 8 | 16 | 32 | 64 |

For example, eight /24 blocks from 192.168.24.0 form 192.168.24.0/21, because 24 is a multiple of 8. Four blocks from 10.1.3.0 do not combine, because 3 is not a multiple of 4; the run 10.1.3.0 to 10.1.6.0 needs three routes (10.1.3.0/24, 10.1.4.0/23, 10.1.6.0/24).

★ **Sixty-second drills.** Cover the answer column, give each result in under a minute, and aim for thirty seconds by the end of Pillar 3.

| Address and prefix | Network | Broadcast | Usable hosts |
|---|---|---|---|
| 10.9.77.18/22 | 10.9.76.0 | 10.9.79.255 | 1,022 |
| 172.17.130.9/19 | 172.17.128.0 | 172.17.159.255 | 8,190 |
| 192.168.40.201/27 | 192.168.40.192 | 192.168.40.223 | 30 |
| 203.0.113.90/26 | 203.0.113.64 | 203.0.113.127 | 62 |
| 10.200.5.99/20 | 10.200.0.0 | 10.200.15.255 | 4,094 |
| 172.30.9.250/23 | 172.30.8.0 | 172.30.9.255 | 510 |
| 192.0.2.37/29 | 192.0.2.32 | 192.0.2.39 | 6 |
| 10.77.130.1/17 | 10.77.128.0 | 10.77.255.255 | 32,766 |
| 198.51.100.130/25 | 198.51.100.128 | 198.51.100.255 | 126 |
| 172.16.7.7/21 | 172.16.0.0 | 172.16.7.255 | 2,046 |
| 10.3.3.3/28 | 10.3.3.0 | 10.3.3.15 | 14 |
| 100.100.100.100/18 | 100.100.64.0 | 100.100.127.255 | 16,382 |

Three more kinds of drill complete the set. *Same subnet?* 172.16.20.30 and 172.16.31.1 under 255.255.240.0: yes, both lie in 172.16.16.0 to 172.16.31.255. 10.0.5.250 and 10.0.6.2 under 255.255.254.0: no, the blocks are 10.0.4.0 and 10.0.6.0. 192.168.1.62 and 192.168.1.65 under 255.255.255.192: no, because 64 divides them. *Wildcard:* the wildcard of /26 is 0.0.0.63 and of /21 is 0.0.7.255. *Summary:* 192.168.9.0/26 to 192.168.9.192/26 (four blocks, start 0) is 192.168.9.0/24.

### Ports and protocol numbers, second page

The ports every candidate knows (FTP, SSH, Telnet, SMTP, DNS, DHCP, HTTP, BGP, HTTPS and so on), the IP protocol numbers up to OSPF and the common EtherTypes are in the Revision Spread of Pillar 3 ([the table](#rv3){.ref}). The table below adds the ports and numbers that networking roles are asked about.

★ **Good to know, for networking roles.**

| Port or number | Service | Note |
|----------------|------------------|----------------------------------|
| TCP 49 | TACACS+ | device administration; RADIUS is UDP 1812 and 1813 |
| UDP 500, UDP 4500 | IKE, IPsec NAT traversal | ESP is IP protocol 50 and AH is 51 |
| TCP 646 | LDP | also UDP 646 for hellos |
| TCP 830 | NETCONF over SSH | gNMI has no old default; many devices use 9339 or 57400 |
| UDP 3784, 3785 | BFD single-hop control, echo | multi-hop control is UDP 4784 |
| UDP 4789, UDP 6081 | VXLAN, Geneve | VXLAN adds 50 bytes of overhead |
| UDP 1985 | HSRP | 224.0.0.2 (v1) and 224.0.0.102 (v2); VRRP is IP protocol 112 |
| UDP 521 | RIPng | RIP is UDP 520 |
| TCP/UDP 389, 636 | LDAP, LDAPS | |
| TCP/UDP 2049 | NFS | |
| TCP/UDP 5060, 5061 | SIP, SIP over TLS | |
| UDP 5353 | mDNS | |
| TCP 6653 | OpenFlow | 6633 in older controllers |
| IP protocol 4, 41 | IP-in-IP, IPv6-in-IPv4 | 6in4 tunnels |
| IP protocol 88, 103, 132 | EIGRP, PIM, SCTP | |
| EtherType 0x8809 | slow protocols | LACP is the best-known user |
| EtherType 0x88CC | LLDP | |
| EtherType 0x8847 | MPLS unicast | multicast is 0x8848 |
| EtherType 0x88A8 | 802.1ad (QinQ) | outer tag of a double-tagged frame |
| EtherType 0x8863, 0x8864 | PPPoE discovery, session | MTU 1492 |

Ephemeral ports: IANA recommends 49152 to 65535, whereas Linux defaults to 32768 to 60999 (`/proc/sys/net/ipv4/ip_local_port_range`). Control-plane multicast addresses are also asked: OSPF 224.0.0.5 and .6, RIPv2 .9, EIGRP .10, PIM .13, VRRP .18; Layer 2: STP 01:80:C2:00:00:00, LACP 01:80:C2:00:00:02, LLDP 01:80:C2:00:00:0E, and CDP, VTP and UDLD 01:00:0C:CC:CC:CC.

★ **Protocols that ride on others.** BGP rides TCP 179. OSPF and EIGRP are IP protocols 89 and 88, with no TCP or UDP. RIP rides UDP 520. IS-IS sits directly on Layer 2 and has no IP header at all. DHCP and DNS are applications over UDP. ICMP is a Layer 3 protocol that travels inside IP. BGP uses TCP because it needs reliable, ordered delivery of incremental updates, and so need not build its own retransmission ([Q4.32](#ps4){.ref}).

### Route preference across vendors

The Cisco administrative-distance table is in the Revision Spread of Pillar 4 ([the table](#rv4){.ref}); the decision order (longest prefix, then distance, then metric) is in [§4.4](#s4-4){.ref}. Junos calls the same idea *route preference*, and Arista and Nokia use numbers of their own, so the table puts them side by side.

★ **Default distance or preference; lower wins everywhere.**

| Source | Cisco IOS | Junos | Arista EOS | Nokia SR OS |
|----------------|----------|----------------|----------|--------------|
| Connected, local | 0 | 0 | 0 | 0 |
| Static | 1 | 5 | 1 | 5 |
| OSPF internal | 110 | 10 | 110 | 10 |
| OSPF external | 110 | 150 | 110 | 150 |
| IS-IS | 115 | 15 (L1), 18 (L2) internal | 115 | 15 (L1), 18 (L2) internal |
| RIP | 120 | 100 | 120 | 100 |
| eBGP | 20 | 170 | 200 | 170 |
| iBGP | 200 | 170 | 200 | 170 |

::: trap
*Claim:* "eBGP beats OSPF for the same prefix." *Why it is wrong:* on Cisco IOS it does (20 against 110), but on Junos and SR OS the OSPF route wins (10 against 170), and on EOS it also wins (110 against 200). *Correct statement:* name the platform first; distance is a vendor default, and a floating static route must be set above the number of the protocol it backs up, not above 1. Treat the Arista and Nokia columns as reported defaults and confirm them with `show ip route` or the platform documentation.
:::

### Pointers

| Need | Where | Question |
|----------------------------------------|--------------------------|--------|
| Header bit layouts: Ethernet, 802.1Q, ARP, IPv4, IPv6, TCP, UDP | [§3.3](#s3-3){.ref}, [§3.5](#s3-5){.ref}, [§3.6](#s3-6){.ref}, [§3.7](#s3-7){.ref}, [§3.9](#s3-9){.ref}, [§4.2](#s4-2){.ref} | [Q3.3](#ps3){.ref} |
| "What happens when you type google.com": the nine-stage ladder and its two-minute version | [§3.11](#s3-11){.ref} | [Q3.45](#ps3){.ref} |
| Troubleshooting skeleton, the SCALPEL card and the layer command matrix | [§11.2](#s11-2){.ref}, [§11.5](#s11-5){.ref} | [Q11.1](#ps11){.ref} |
| MTU, MSS and overheads (PPPoE 1492, GRE 24 bytes) | [§3.5](#s3-5){.ref}, [§4.14](#s4-14){.ref} | [Q3.16](#ps3){.ref} |
| Wi-Fi and cellular standards | [Pillar 6](#ch6){.ref} | |

## [A3]{.sec}Online-assessment cheat codes [Must · ■□□]{.tag} {#s13-3}

::: bigidea
An online assessment rewards the candidate who knows the format before it starts, because the format fixes the time per question and hence which questions to skip.
:::

### Reported formats

The platforms (HackerRank, AMCAT, Mercer Mettl, CoCubes) and their habits, such as hidden test cases, adaptive sections and locked sections, are tabulated in [§12.1](#s12-1){.ref}. What differs by company is the paper itself. The table records what candidates report, with the year where a report gave one, and nothing in it is a rule.

★ **Reported OA formats, nine companies (candidate reports, 2022 to 2026).**

| Company | Platform reported | Reported format | Topics |
|--------|----------|--------------------------------------|----------------------|
| Cisco | HackerRank | 2023: 90 min, 42 questions (40 MCQ and 2 coding); 2024: 41 MCQ and 1 coding; 2026 guides: about 90 min, about 40 MCQ and 2 DSA. Coding in C, Python or Java; AI proctoring; no negative marking reported. The 2025 network-engineer drive (Bengaluru) added a presentation after the test. | networking (TCP/IP, OSI, routing, security), OS, DBMS, aptitude, C output |
| Juniper | HackerRank | 90 min, 33 questions (32 MCQ and 1 coding). October 2024 internship: 38 questions (35 MCQ and 3 coding), tight on time. Older reports: about 50 networking and C MCQs. Four to five rounds in all. | aptitude, CN, DBMS, OS, HTML/CSS, output prediction, time complexity |
| Qualcomm | varies by drive | sectioned MCQs; no fixed duration reported | aptitude, C (pointers, `const`, structs and unions, padding, `volatile`, `static`), OS, architecture, digital logic, networking |
| Arista | HackerRank, then CoderPad | 1.5 h test in C or C++: four to five coding problems, or a mix of coding and MCQs; another report gives two medium-to-hard problems | C debugging, linked lists, bits, arrays, OS, networking |
| Nokia | AMCAT | English, quantitative and logical sections (one guide lists 18, 16 and 14 questions), then 2 basic programs, in C or C++ in some drives | aptitude, GCD, sorting, balanced brackets |
| Microsoft | Codility, HackerRank or AMCAT | 2 coding problems, medium to hard; on-campus timelines are short | DP, graphs, greedy, binary search |
| Amazon (NDE) | Amazon's own tests, varies | CV screen, a phone screen heavy on troubleshooting, then a loop of four to five rounds | BGP, OSPF, TCP/IP, MTU and MSS, Python, Leadership Principles |
| Google | online coding or phone screen | one to two LeetCode-style problems; the network-engineer track adds networking and a basic Python question in a shared document | DSA, networking, scripting |
| Broadcom | varies | C-heavy technical rounds; several interviews | bits, linked lists, pointers, stacks and queues, OS |

[**Know your battlefield** — before each drive, read three things on the instruction screen: negative marking, section locking, and whether a language is forced. Everything in A3.2 depends on them.]{.margin}Note that the Cisco and Juniper rows are the best documented, because both recur in reports every year; the others are thin. The coding half of each company is described in [§1.0](#s1-0){.ref}.

### The time-management plan

The method is the two-pass method of [§12.1](#s12-1){.ref}: read for three minutes, answer under 45 seconds in pass one, flag, and return. The worked 90-minute plan for a Cisco-style paper is in [§1.0](#s1-0){.ref}. The table applies the same rules to the other reported formats; each row sums to the stated total.

★ **Budgets by format (minutes).**

| Format | Read | MCQ | Coding | Buffer | Total | Rule of thumb |
|----------------|-----|------------------|----------|------|-----|------------------------|
| Juniper A: 32 MCQ and 1 coding, 90 min | 3 | 27 | 45 | 15 | 90 | about 50 s per MCQ; the buffer funds a second pass |
| Juniper B: 35 MCQ and 3 coding, 90 min | 3 | 26 | 20 + 20 + 15 | 6 | 90 | 45 s per MCQ; bank every easy coding case first |
| Qualcomm: 50 MCQ, 60 min | 2 | 17 (aptitude, 15) + 20 (C, 20) + 8 (OS and architecture, 10) + 4 (CN, 5) | none | 9 | 60 | answer CN and OS first if sections are not locked: they are the quickest marks |
| Arista: 4 coding problems, 90 min | 5 | none | 18 × 4 = 72 | 13 | 90 | order by ease; submit a brute force at minute 10 of each |
| Nokia: 48 MCQ then 2 programs, about 100 min | 0 | 15 (English) + 22 (quantitative) + 18 (logical) | 20 + 20 (after the MCQs) | 5 | 100 | AMCAT times its own sections and adapts to accuracy, so early answers matter most |
| Microsoft or Amazon: 2 coding problems, 90 min | 5 | none | 35 + 40 | 10 | 90 | give the harder problem the extra five minutes only if the first is complete |

The checks in each row are arithmetic: 3 + 27 + 45 + 15 = 90; 3 + 26 + 55 + 6 = 90; 2 + 49 + 9 = 60; 5 + 72 + 13 = 90; 55 + 40 + 5 = 100; 5 + 75 + 10 = 90. For the Qualcomm paper, 17 + 20 + 8 + 4 = 49. In every case the buffer is for re-running edge cases, not for starting a new problem.

★ **Coding triage: when the verdict is not "accepted".**

| Verdict or symptom | Usual cause | Fix |
|----------------------|--------------------------|----------------------------|
| time limit exceeded, C++ | `cin`/`cout` unsynchronised, or `endl` flushing every line | `ios::sync_with_stdio(false); cin.tie(nullptr);` and `'\n'` |
| time limit exceeded, Python | `input()` on large input; a nested loop | `sys.stdin.readline`; a built-in or a hash map |
| wrong answer on a few hidden cases | overflow in a sum or product | `long long`; reduce modulo early |
| runtime error on one case | empty input, *n* = 1, an index of −1 | guard before the loop |
| recursion error or crash on a deep case | recursion depth about 10<sup>5</sup> in Python or a skewed tree | iterative version, or raise the limit |
| wrong format | trailing space or missing newline; reading *n* lines when input ends at end of file | print exactly as the sample; read to end of file when *n* is not given |
| memory limit exceeded | an *n* × *n* table | a rolling row, or a map of used cells |
| passes samples only | the brute-force logic is wrong, not the speed | write a 10-line brute force and compare on random small input |

### MCQ elimination tactics

Eight habits remove options before any arithmetic starts. A seconds budget applies to all of them: if no option has fallen after 90 seconds, flag the question and leave.

★ **Elimination, with one worked case each.**

| # | Tactic | Worked case |
|--|----------------------|--------------------------------------------------|
| 1 | Strike absolute words ("always", "never", "guarantees") unless the statement is a definition | *Which statement about UDP is correct? (a) It always delivers in order (b) It never uses a checksum (c) It has no connection set-up (d) It guarantees delivery.* Three options carry absolutes and are false; the answer is (c). |
| 2 | Map each option to its layer; wrong-layer options are distractors | *Which device separates broadcast domains? Hub, switch, router, repeater.* Only a router (or a Layer 3 switch with VLANs) works. |
| 3 | Estimate the order of magnitude first | *Transmission time of a 1,500-byte frame on 1 Gb/s: (a) 12 ms (b) 1.2 ms (c) 12 µs (d) 1.2 µs.* 1,500 bytes is about 10<sup>4</sup> bits and 10<sup>4</sup> / 10<sup>9</sup> is 10<sup>−5</sup> s, so (c); exact: 12,000 / 10<sup>9</sup> = 12 µs. |
| 4 | In output questions, look first for a compile error or undefined behaviour | *`const int c = 5; c = 6; printf("%d", c);` prints (a) 5 (b) 6 (c) compile-time error (d) undefined.* The assignment to a `const` object is rejected: (c). |
| 5 | If two options are opposites, one of them is probably right | *TCP is (a) connectionless (b) connection-oriented (c) without flow control (d) unordered.* (a) and (b) contradict each other; (c) and (d) are false, so (b). |
| 6 | Options that are identical in effect cannot be a unique answer; in a "which is NOT" question the odd one out is | *Which does not add one to *x*? (a) `x++` (b) `++x` (c) `x += 1` (d) `x == x + 1`.* Three are equivalent, so the odd one is (d), a comparison. |
| 7 | Read the unit of the question: "hosts" subtracts two, "addresses" does not | *192.168.5.0/26: maximum hosts?* 2<sup>6</sup> − 2 = 62, not 64. |
| 8 | Check the units digit and the digit sum before multiplying | *143 × 87 is (a) 12,341 (b) 12,441 (c) 12,451 (d) 12,641.* The units digit is 3 × 7 = 21, so 1: (b) or (c). Digit sums: 143 gives 8, 87 gives 6, 48 gives 3 (mod 9); 12,441 sums to 12, then 3; 12,451 sums to 13, then 4. So (b); exact: 143 × 87 = 12,441. |

### Aptitude and C-trap indexes

Aptitude formula cards are not repeated here. Each topic has one card with two solved examples, and the forty further MCQs of [the Pillar 12 set](#ps12){.ref} follow the same order.

| Aptitude topic | Card |
|------------------------------------------------------------|--------|
| Divisibility, divisors, cycles of unit digits, remainders, HCF and LCM, bases | [§12.2](#s12-2){.ref} |
| Percentages, profit and loss, ratio, mixtures, averages | [§12.3](#s12-3){.ref} |
| Work and pipes, speed, trains, boats | [§12.4](#s12-4){.ref} |
| Interest, permutations, probability, ages, clocks and calendars | [§12.5](#s12-5){.ref} |
| Series, coding, blood relations, seating, syllogisms | [§12.6](#s12-6){.ref} |
| Data interpretation, sufficiency, verbal ability | [§12.7](#s12-7){.ref} |

The C output traps are numbered T1 to T36 in [§2.15](#s2-15){.ref}. Use the index below to jump from what a snippet contains to the trap that explains it.

| The snippet contains | Look at |
|--------------------------------------------------|--------------------|
| two writes to one variable, `i++` with `++i` | T1, T12, T17 |
| `sizeof`, array parameters, `strlen` | T2, T6, T25 |
| `printf` return value, format specifiers | T3, T31 |
| signed with unsigned, plain `char`, overflow, a countdown loop | T4, T5, T21, T28 |
| macros, `static` locals | T7, T11 |
| `switch` without `break`; comma and `?:` operators | T8, T9, T30 |
| `&&` and `||` with side effects | T10 |
| pointer arithmetic, `const`, string literals, dead locals | T12, T13, T14, T15, T16 |
| structures, padding and unions | T18, T19 |
| `volatile` | T20 |
| floating point, shifts, division of negatives | T22, T24, T32 |
| character constants, octal literals | T23, T29 |
| uninitialised data, double free, where a variable lives | T26, T27, T36 |
| `=` in a condition, `==` against `&`, `i[a]` | T33, T34, T35 |

## [A4]{.sec}HR cheat codes [Must · ■□□]{.tag} {#s13-4}

::: bigidea
An HR round is short, and the offer that follows it is a document, so both reward the candidate who has prepared a frame in advance, not a speech.
:::

### Pointers

The behavioural material is taught once, in Pillar 12.

| Need | Home | Model answers |
|----------------------------------------|------------|------------------|
| STAR and STAR-L, with the Action share of the time | [§12.12](#s12-12){.ref} | [Q12.43 to Q12.50](#ps12){.ref} |
| The sixteen Amazon Leadership Principles and the story bank | [§12.12](#s12-12){.ref} | [Q12.43 to Q12.50](#ps12){.ref} |
| "Tell me about yourself", with the product named for each company | [§12.12](#s12-12){.ref} | [Q12.41](#ps12){.ref} |
| The eleven standard HR questions and their frames | [§12.12](#s12-12){.ref} | [Q12.42](#ps12){.ref} |
| The résumé, the bullet formula and project defence | [§12.13](#s12-13){.ref} | [Q12.51 to Q12.54](#ps12){.ref} |

### The HR question bank, continued

Every frame has the same three parts: a plain claim, one piece of evidence, and a link to the role. Keep the answer under 60 seconds and finish with the link. The eleven questions already framed in [§12.12](#s12-12){.ref} (why this company, why networking, strengths, weakness, five years, relocation and on-call, a conflict, why hire you, higher studies, fresher salary, questions for us) are not repeated.

★ **Twenty further questions.**

| Question | Frame |
|------------------------|----------------------------------------------------|
| What do you know about us? | One product, one recent public announcement, one team; check the careers page the day before. Then: "this is why the role interests me." |
| Your biggest achievement? | One project or result with a number, in two sentences; then what it taught you. |
| How do you handle pressure? | Name a method (list tasks, ask early for help, cut scope), then a deadline from a project or exam that shows it working. |
| Night shifts or on-call? | Answer honestly. Operations teams run around the clock, so show that you know it; ask about the rota after the offer, not before. |
| Do you have other offers? | Tell the truth. "I am in process elsewhere, and this role is a strong fit because …". Name no company unless asked directly. |
| Why is your CGPA low, or why a backlog? | State the fact, the cause in one clause, and the recovery: a rising trend, a cleared backlog, a project built meanwhile. No excuses. |
| Why did you choose your branch (non-CS)? | Link it to networking: signals, communication systems, embedded hardware. Add a lab that bridged the two. |
| How do you keep up with technology? | Name sources and a habit: vendor documentation, RFCs, a home lab, one recent topic you learnt and what you did with it. |
| How do you take criticism? | One instance, what you changed, and how the next result differed. |
| Describe your ideal manager or team. | Clear goals, regular feedback, technical depth. Avoid "no supervision" and any complaint about a former guide. |
| What will you do in your first 90 days? | Learn the systems, shadow on-call, fix one small defect, ask questions. Never promise to rebuild anything. |
| Will you do support or legacy work? | Yes; operations work is where networks are learnt. Add the skill you expect to gain from it. |
| Gap in studies or a delayed degree? | One factual sentence, then what you did in the gap (course, certification, project). |
| How would friends describe you? | Two traits, each with a small example. Choose traits the job needs, such as patience when debugging. |
| Alone or in a team? | Both: the example should show individual ownership inside a team result. |
| Would you take a different team? | Yes if the scope is technical; ask what the team owns and how success is measured. |
| Salary expectation (lateral)? | Give a range anchored in market data and the scope, after learning the scope: "for this scope I would expect …". |
| Why are you leaving your current role? | Forward-looking: what you want to learn and cannot learn there. No blame. |
| Notice period and joining date? | State it plainly; mention a buyout only if the company has offered one. |
| You disagree with a senior's technical choice? | Raise it privately with data, accept the decision if it stands, and support it ([Q12.46](#ps12){.ref}). |

### Offer negotiation, continued

The basic lesson (compare *guaranteed annual cash*, and see which items can move off campus) and the first worked comparison are in [§12.12](#s12-12){.ref}. The tables below add what an Indian offer letter hides, a second comparison that includes shares, and the words to use.

★ **What each component is and how to value it.**

| Component | What to ask | How to value it |
|------------|------------------------------|----------------------------------|
| Fixed base | monthly gross, and the split into basic, house-rent allowance and special allowance | fully; the basic sets the provident-fund and gratuity amounts |
| Employer provident fund | percentage of basic, and whether it is inside or outside the base | counted in CTC but not in monthly pay; value it, but it is not cash you can spend |
| Gratuity | confirm it is accrued, not paid yearly | last drawn basic × 15 / 26 × years of service, payable after five years under the Payment of Gratuity Act; value at zero for a short stay |
| Variable pay | the payout percentage of the last two years | target × the recent payout, never the target |
| Joining bonus | the clawback period and whether it is taxed at once | one-off; spread over the clawback period, and drop it if you doubt the stay |
| Relocation | amount, whether it is reimbursed or lump-sum, any repayment | one-off, near face value |
| RSUs | vesting schedule (25% a year, or front-loaded), grant value, the currency of the share price | grant value ÷ years, then discount for share-price risk; unlisted shares at a large haircut |
| Insurance, meal cards | cover amount; whether it extends to family | small; compare only if the rest is equal |
| Notice period, bond | length, and any recovery amount | a cost if you leave early; ask for it to be waived or reduced |

★ **A second comparison, with shares.** Offer C is advertised at ₹21 LPA and Offer D at ₹18 LPA. All figures are in lakhs of rupees.

| Item | Offer C | Offer D |
|---|---|---|
| Fixed base | 14 | 17 |
| Variable: target, payout last year | 2, paid at 90% | 1, paid at 100% |
| Joining bonus (year one only) | 2 | none |
| RSU grant, vesting 25% a year | 12 in total, so 3 a year | none |
| Headline CTC (base + variable target + RSU per year + bonus) | 14 + 2 + 3 + 2 = 21 | 17 + 1 = 18 |
| Cash in year one | 14 + 1.8 + 2 = 17.8 | 17 + 1 = 18 |
| Cash in years two to four, each | 14 + 1.8 = 15.8 | 18 |
| Four-year cash | 17.8 + 3 × 15.8 = 65.2 | 4 × 18 = 72 |
| Four-year total if the shares hold their grant value | 65.2 + 12 = 77.2 | 72 |
| Four-year total if the shares halve | 65.2 + 6 = 71.2 | 72 |

Hence the headline ranks C above D by 3 per year, whereas the cash ranks D above C by 6.8 over four years, and C wins only if its shares keep at least 6.8 of their 12 (about 57%). Further, RSUs are taxed as salary on the date they vest, at the market value then, so tax in cash is payable even if the shares are unsold. The tax regime (new or old) is chosen in the employer's payroll declaration and its slabs change often, so use the company's calculator and not a rule from this page.

★ **Words for the conversation.**

| Step | Say | Because |
|----------|--------------------------------------------|--------------------------|
| Thank | "Thank you; I am glad to receive this offer and I would like to join." | enthusiasm comes first and costs nothing |
| Ask for the details | "Could you share the break-up in writing: base, variable payout history, bonus terms and vesting?" | you cannot negotiate what you cannot see |
| Ask for time | "May I have a few working days to decide?" | a considered answer is normal; pressure is a signal |
| Make one request | "With the competing offer at ₹X guaranteed cash, could the base be ₹Y?" | one figure with one data point is easy to approve |
| Pause | say nothing after the request | the next speaker concedes or explains |
| Close | "If that is possible, I will accept today." | it gives the manager a reason to act |

Courtesy rules apply after the call. Do not decline other offers or resign before the signed letter arrives; verify the joining conditions and background check in the letter; and read the placement cell's policy before declining a campus offer, since some forbid reneging. Do not invent a competing offer, because a recruiter may ask for the letter.


:::
