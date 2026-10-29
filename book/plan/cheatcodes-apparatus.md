# Cheat Codes Layer and End-of-Chapter Apparatus: Plan

Book: placement textbook for Indian students targeting network-engineer and networking-software roles at Cisco, Qualcomm, Google, Microsoft, Amazon (NDE), Juniper, Arista, Nokia, Broadcom.
Scope of this file: (A) the "cheat codes" layer, meaning quick-recall pages, tables, templates and hacks that sit beside the 12 pillars, and (B) the specification of the end-of-chapter apparatus used in every chapter.
Spelling: British. Code comments in British spelling as well ("initialise", "behaviour", "neighbour").

## 0. Research notes and caveats (read first)

- Research was done through web search on 29 Oct 2026. Direct page fetches to geeksforgeeks.org, leetcode.com and naukri.com were blocked from this session's network, so question lists below come from search-result snippets and summaries of those pages, Glassdoor, Jointaro, Medium and prep sites. Every company question carries a confidence tag:
  - **[S]**: the specific question (or a near-verbatim form) appeared in a candidate report surfaced from the cited URL.
  - **[T]**: the topic was reported in the cited source for that company, but the exact wording is our own rendering of a standard question on that topic. Writers must reword [T] items as "commonly reported topic" in the book, never as "asked verbatim".
- Before typesetting, a writer with open network access should open each cited URL, confirm wording, and upgrade [T] to [S] where possible. Do not invent quotes.
- Candidate reports are anonymous, self-reported and span 2016–2026. Formats change every year; the book must say so in a margin note at the start of Part "Cheat Codes".
- Pass-rate figures (Jointaro) are from small samples; quote only with that caveat.

---

# PART A: THE CHEAT CODES LAYER

Design: each cheat-code page is a coloured "tear-out" spread (suggest teal header band, monospace code blocks, a small "Hack #n" badge). Each page fits on one or two A4/B5 pages and is referenced from the relevant chapter with a margin icon (a lightning bolt). A consolidated "Cheat Code Atlas" appendix reprints all of them.

## A1. DSA cheat codes

### A1.1 Constraint size to expected complexity ("read the constraints first")

Rule of thumb: a judge does about 10^8 simple operations per second (C++); Python is roughly 10–50x slower, so drop one row for Python. At n = 10^5, O(n log n) ≈ 1.7 × 10^6 operations (fine) while O(n²) = 10^10 (TLE). Sources differ slightly (Codeforces puts O(n log n) up to 10^6); for LeetCode/HackerRank plan to the stricter row.

| Largest n | Target complexity | Typical techniques |
|---|---|---|
| n ≤ 10–12 | O(n!) or O(n · n!) | permutations, brute-force backtracking |
| n ≤ 20–25 | O(2^n), O(2^n · n) | subsets, bitmask enumeration, meet-in-the-middle (n ≤ 40) |
| n ≤ 100 | O(n^4) | 4 nested loops, small DP |
| n ≤ 500 | O(n³) | Floyd–Warshall, interval DP, matrix chain |
| n ≤ 2 000–5 000 | O(n²) | 2-D DP (LCS, edit distance), all pairs naive |
| n ≤ 10^4 | O(n²) borderline, O(n√n) | careful O(n²), sqrt decomposition |
| n ≤ 10^5 – 2·10^5 | O(n log n) | sort, heap, binary search, segment tree/BIT, Dijkstra |
| n ≤ 10^6 | O(n) or O(n log n) tight | two pointers, sliding window, prefix sums, hashing, linear sieve |
| n ≤ 10^8 | O(n) tight, O(√n) | simple loop, maths |
| n ≤ 10^9 – 10^18 | O(log n), O(√n), O(1) | binary search on answer, fast exponentiation, maths formula, digit DP |

Also read: value ranges (values up to 10^9 means you cannot index an array by value, use hashing or coordinate compression; sums up to 10^5 × 10^9 overflow 32-bit, use `long long`); "return modulo 10^9+7" means counting/DP; small k (k ≤ 20) with big n suggests bitmask over k.

Sources: LeetCode discuss "Rule of thumb for avoiding TLE" https://leetcode.com/discuss/study-guide/1939806/rule-of-thumb-for-avoiding-tle ; "Understanding Time Complexity: The 10^8 Operations Rule" https://leetcode.com/discuss/post/7324952/understanding-time-complexity-the-108-op-qqno/ ; Codeforces blog 21344 https://codeforces.com/blog/entry/21344 ; https://qishiclub.github.io/python-for-leetcode/time-complexity-estimation/

### A1.2 Keyword to pattern decoder

Print as a two-column "if you see X, think Y" table with a third column "first problem to try".

| Signal in the problem | Think | Anchor problem (LeetCode #) |
|---|---|---|
| input sorted / "non-decreasing" | binary search, two pointers | 704, 167 |
| "pair/triplet summing to target" | hash map (unsorted) or two pointers (sorted) | 1, 15 |
| "contiguous subarray/substring" + "longest/shortest with condition" | sliding window (variable) | 3, 209, 76 |
| "subarray of size k" | fixed sliding window | 643 |
| "subarray sum equals k" / "divisible by k" / negatives present | prefix sum + hash map of counts | 560, 974 |
| range sum queries, no updates | prefix sums | 303 |
| range queries with updates | Fenwick tree / segment tree | 307 |
| "top k", "k largest/smallest", "k closest", "k most frequent" | heap of size k (or quickselect, bucket sort) | 215, 347, 973 |
| "median of stream" | two heaps | 295 |
| "merge k sorted" | min-heap k-way merge | 23 |
| intervals, "overlapping", "meeting rooms" | sort by start, merge; sweep line; min-heap of end times | 56, 253 |
| numbers in range 1..n, "missing/duplicate" | cyclic sort / index marking | 268, 287, 448 |
| linked list cycle, middle, kth from end | fast and slow pointers | 141, 142, 876, 19 |
| reverse part of a list | in-place reversal | 206, 92, 25 |
| "next greater/smaller", "span", histogram | monotonic stack | 739, 496, 84 |
| "sliding window maximum" | monotonic deque | 239 |
| valid brackets, undo, nested structure, expression evaluation | stack | 20, 150, 394 |
| "minimum/maximum value such that feasible", "minimise the largest" | binary search on answer + greedy check | 875, 1011, 410 |
| rotated sorted array, peak | modified binary search | 33, 153, 162 |
| tree: depth, path, subtree property | DFS recursion (post-order returns info) | 104, 124, 543 |
| tree: level by level, "right side view" | BFS with queue | 102, 199 |
| BST, "kth smallest", validate | in-order traversal | 98, 230 |
| grid, "islands", connected regions | DFS/BFS flood fill, union-find | 200, 695 |
| "shortest path", unweighted | BFS (multi-source BFS for "rotting", "distance to nearest") | 994, 542, 127 |
| shortest path, non-negative weights | Dijkstra | 743, 1631 |
| negative weights / "at most k stops" | Bellman–Ford (k rounds) | 787 |
| "prerequisites", "order of tasks", dependency, "alien dictionary" | topological sort (Kahn BFS) | 207, 210, 269 |
| "connected components", "redundant connection", dynamic connectivity, "accounts merge" | union-find (DSU) | 547, 684, 721 |
| minimum spanning tree, "connect all points at min cost" | Kruskal (DSU) / Prim (heap) | 1584 |
| prefix, "words starting with", autocomplete, IP longest-prefix match | trie | 208, 211, 421 |
| "all combinations/permutations/subsets", "generate all" | backtracking | 78, 46, 39, 51 |
| "number of ways", "min/max cost", "can you reach", overlapping subproblems | dynamic programming | 70, 322, 300 |
| two strings, "edit", "common subsequence" | 2-D DP | 1143, 72 |
| "choose items with capacity" | knapsack DP | 416, 494 |
| "split into parts", "burst", "matrix chain" | interval DP | 312 |
| "maximum subarray" | Kadane | 53 |
| "greedy feels right": jumps, scheduling, gas station | greedy with exchange argument | 55, 134, 435 |
| "single number", XOR, "power of two", "count bits", subsets of small set | bit manipulation | 136, 191, 338, 231 |
| "LRU / LFU cache" | hash map + doubly linked list (OrderedDict) | 146, 460 |
| "design a data structure with O(1)" | hash map + array/list combos | 380 |
| string matching, repeated pattern | KMP / Z / rolling hash | 28, 459 |
| "anagram", frequency compare | count array of 26 / hash map | 242, 49, 438 |
| very large n, maths flavour | GCD, modular exponentiation, sieve | 50, 204 |

Sources: Sean Prashad LeetCode Patterns (grouped by sub-pattern) https://seanprashad.com/leetcode-patterns/ and https://github.com/seanprashad/leetcode-patterns ; Grokking pattern list (merge intervals, cyclic sort, two heaps, k-way merge, etc.) https://www.designgurus.io/course-play/grokking-the-coding-interview/doc/coding-patterns-a-cheat-sheet ; "14 Patterns to Ace Any Coding Interview Question" https://leetcode.com/discuss/post/4039411/14-Patterns-to-Ace-Any-Coding-Interview-Question/ ; heap "keep a heap of size k" framing from https://interview-prep-3ci.pages.dev/coding-patterns ; NeetCode roadmap https://neetcode.io/roadmap ; Striver A2Z sheet https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/

### A1.3 The 22 core patterns with templates

Each pattern gets a half-page card with: (1) one-line idea, (2) recognition cues, (3) template in **C++ and Python side by side** (C for pointer-heavy ones such as linked lists, since Qualcomm/Broadcom/Arista interview in C), (4) complexity, (5) three anchor problems (easy/medium/hard), (6) "classic bug" box.

List and the bug box for each:

1. **Two pointers (opposite ends)**: sorted pair sum, container with most water, 3Sum. Bug: not skipping duplicates in 3Sum.
2. **Two pointers (same direction / read-write)**: remove duplicates in place, move zeroes. Bug: writing before reading.
3. **Fixed sliding window**: max sum of size k. Bug: off-by-one when evicting `a[i-k]`.
4. **Variable sliding window**: longest substring without repeat (asked at Cisco), minimum window substring. Template:
   ```python
   def longest_window(s):
       seen = {}            # char -> count in window
       left = best = 0
       for right, ch in enumerate(s):
           seen[ch] = seen.get(ch, 0) + 1
           while seen[ch] > 1:          # window invalid: shrink
               seen[s[left]] -= 1
               left += 1
           best = max(best, right - left + 1)
       return best
   ```
   Bug: shrinking with `if` instead of `while`.
5. **Prefix sum + hash map**: `count[0] = 1` initialisation. Bug: forgetting the seed entry.
6. **Fast and slow pointers**: cycle detection (Floyd), cycle start, middle node, happy number. Bug: `fast->next` null check order.
7. **In-place linked-list reversal** (C template with `prev, curr, next`). Bug: losing `next` before re-pointing.
8. **Binary search (classic and lower/upper bound)**: one canonical template only, `lo = 0, hi = n` (half-open), `while lo < hi`, `mid = lo + (hi - lo) / 2`. Bug: `(lo+hi)/2` overflow in C; infinite loop when `lo = mid`.
9. **Binary search on the answer**: monotone predicate `feasible(x)`; Koko bananas, ship packages, split array largest sum. Bug: wrong search bounds (low = max element, high = sum).
10. **Monotonic stack**: next greater element, daily temperatures, largest rectangle in histogram. Bug: storing values instead of indices.
11. **Monotonic deque**: sliding window maximum.
12. **Heap / top-k / two heaps / k-way merge**: C++ `priority_queue` is a max-heap by default; Python `heapq` is min-heap (negate for max). Bug: mixing these up.
13. **Intervals (sort + merge, sweep line)**. Bug: sorting by end when start is needed (or vice versa for "erase overlap").
14. **Cyclic sort / index marking**. Bug: swapping with `nums[i]-1` without the "while not in place" loop.
15. **Tree DFS (pre/in/post) and "return a pair" post-order** (diameter, max path sum). Bug: mixing the value returned upward with the global answer.
16. **Tree/graph BFS (level order, multi-source BFS)**. Bug: marking visited on pop instead of on push (duplicates in queue).
17. **Graph DFS / flood fill / cycle detection** (three colours for directed). Bug: recursion depth in Python (`sys.setrecursionlimit`) or use iterative.
18. **Topological sort (Kahn)**: indegree array, queue; if output length < V, there is a cycle.
19. **Union-find (DSU)** with path compression + union by rank/size; near O(α(n)). Template:
   ```cpp
   struct DSU {
       vector<int> p, sz;
       DSU(int n) : p(n), sz(n, 1) { iota(p.begin(), p.end(), 0); }
       int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
       bool unite(int a, int b) {
           a = find(a); b = find(b);
           if (a == b) return false;          // already connected: edge is redundant
           if (sz[a] < sz[b]) swap(a, b);
           p[b] = a; sz[a] += sz[b];
           return true;
       }
   };
   ```
20. **Shortest paths**: BFS (unweighted), 0-1 BFS (deque), Dijkstra (heap, skip stale entries), Bellman–Ford (negative edges, k-limited), Floyd–Warshall (n ≤ 400). Networking tie-in box: Dijkstra = OSPF/IS-IS SPF; Bellman–Ford = RIP distance-vector; this link is a favourite interview bridge question.
21. **Backtracking** (choose, explore, un-choose): subsets, permutations, combination sum, N-Queens, word search. Bug: appending the list reference instead of a copy (`path[:]`).
22. **Dynamic programming families**, each with a recurrence card:
    - 1-D linear (climbing stairs, house robber): `dp[i] = f(dp[i-1], dp[i-2])`
    - Kadane / max subarray
    - 0/1 knapsack and unbounded knapsack (coin change: order of loops decides combinations vs permutations)
    - LIS: O(n²) DP and O(n log n) patience sorting with `lower_bound`
    - 2-D strings: LCS, edit distance, longest palindromic subsequence
    - Grid paths: unique paths, minimum path sum
    - Interval DP: burst balloons, matrix chain
    - DP on trees: house robber III
    - Bitmask DP: TSP for n ≤ 20
    - State machine: stock buy/sell with cooldown
    - The "5-step DP recipe": define state, recurrence, base case, order of computation, answer location; then optimise space.
23. **Bit tricks** (bonus card, heavily used at Qualcomm/Broadcom): `x & (x-1)` clears lowest set bit (popcount loop, power-of-two test `x && !(x & (x-1))`); `x & -x` isolates lowest set bit; XOR swap and XOR to find the single number; set/clear/toggle/test bit n: `x | (1<<n)`, `x & ~(1<<n)`, `x ^ (1<<n)`, `(x>>n)&1`; reverse bits of a 32-bit word (mask-and-swap ladder); detect endianness with a `union` or `char*` cast; `__builtin_popcount`, `__builtin_clz`; check if two ints have opposite signs `(a ^ b) < 0`; subnet mask from prefix length `mask = prefix ? 0xFFFFFFFFu << (32 - prefix) : 0` (avoid shift by 32, which is undefined behaviour).

Additional networking-flavoured DSA card ("problems that smell like networking"): longest-prefix match with a binary trie; IP address validation and conversion (`inet_pton` logic by hand); restore IP addresses (LC 93, backtracking); rate limiter (token bucket, sliding window log); LRU cache as a route/ARP cache; Dijkstra as OSPF SPF; detect routing loop = cycle detection; packet reordering = min-heap by sequence number; checksum computation (16-bit one's complement sum); bitmap allocation for VLAN IDs/ports.

### A1.4 Big-O cheat sheet

Tables to print:
- Data structure operations (access/search/insert/delete, average and worst): array, dynamic array, linked list (singly/doubly), stack, queue, hash table, BST (balanced vs skewed), heap, trie (O(L)), DSU.
- Sorting: bubble, selection, insertion (best O(n) on nearly sorted), merge (stable, O(n) extra), quick (O(n²) worst, in place), heap (not stable), counting/radix (O(n+k)); which are stable; which in place. Note C++ `std::sort` is introsort, not stable; `stable_sort` is merge-based; Python `sorted` is Timsort, stable.
- Graph algorithms: BFS/DFS O(V+E); Dijkstra O((V+E) log V) with binary heap; Bellman–Ford O(VE); Floyd–Warshall O(V³); Kruskal O(E log E); Prim O(E log V); topological sort O(V+E).
- Recursion recurrences via Master theorem: T(n)=2T(n/2)+O(n) → O(n log n); T(n)=T(n/2)+O(1) → O(log n); T(n)=2T(n-1)+O(1) → O(2^n).
- Space: recursion depth counts; "O(1) extra" excludes output.
- Common growth sanity: log2(10^6) ≈ 20, log2(10^9) ≈ 30, 2^10 ≈ 10^3, 2^20 ≈ 10^6, 2^31 − 1 = 2 147 483 647, `INT_MAX` ≈ 2.1 × 10^9, `LLONG_MAX` ≈ 9.2 × 10^18.

Source for structure: Tech Interview Handbook algorithms study cheatsheet (sections "Time complexities", "Corner cases", "Things to look out for") https://www.techinterviewhandbook.org/algorithms/study-cheatsheet/ (mirror seen: https://git.mashibing.com/msb-public/tech-interview-handbook/src/commit/6131f64e71dc24e7cfd48e0b68bbabd028efea0b/contents/algorithms/study-cheatsheet.md ); https://www.bigocheatsheet.com/

### A1.5 Edge-case checklist (laminated card style)

Before saying "done", test against:
- **Empty / minimal**: empty array or string, single element, two elements, `n = 0`, `k = 0`, `k > n`.
- **Duplicates**: all equal, many duplicates, duplicate answers to be de-duplicated.
- **Order**: already sorted, reverse sorted, rotated.
- **Values**: negatives, zero, `INT_MIN`/`INT_MAX`, overflow on sum/product, `abs(INT_MIN)`.
- **Strings**: spaces, upper/lower case, non-alphabetic, Unicode (ask), palindrome of length 1.
- **Linked lists**: null head, one node, cycle, operating on head or tail node.
- **Trees**: null root, single node, skewed (depth = n; recursion stack), duplicate keys in BST.
- **Graphs**: disconnected graph, self-loop, parallel edges, cycle, single node, unreachable target.
- **Intervals**: touching endpoints (`[1,2],[2,3]`: overlap or not? ask), nested intervals.
- **Matrices**: 1 × n, n × 1, empty rows.
- **Binary search**: target smaller than all, larger than all, absent, at both ends.
- **Networking-specific inputs**: IP strings with leading zeros ("01.2.3.4"), octet 256, missing octet, /0 and /32 prefixes, broadcast/network address, port 0 and 65535.

Sources: https://www.techinterviewhandbook.org/algorithms/study-cheatsheet/ ; https://algocademy.com/blog/handling-edge-cases-why-its-critical-to-think-beyond-the-obvious-in-coding-interviews/ ; https://levelop.dev/blog/coding-interview-cheat-sheet-edge-cases

### A1.6 STL and standard-library quick reference

Three facing columns (C, C++, Python) on one spread.

- **C** (Qualcomm/Broadcom/Arista rounds are often C-only): `qsort(arr, n, sizeof(int), cmp)` with `int cmp(const void *a, const void *b){ int x=*(const int*)a, y=*(const int*)b; return (x>y)-(x<y); }` (never `return x-y`, it overflows); `bsearch`; `memset` only for 0/−1 byte patterns; `strlen` vs `sizeof`; `strncpy` does not null-terminate when truncating; `malloc`/`calloc`/`realloc`/`free` rules; hand-written stack/queue/linked list/hash table (chaining) templates included because C has no STL.
- **C++**: `vector` (`reserve`, `emplace_back`), `string` (`substr(pos, len)`, `find` returns `npos`), `pair`/`tuple`, `stack`, `queue`, `deque`, `priority_queue<int>` (max) and `priority_queue<int, vector<int>, greater<int>>` (min), `set`/`map` (ordered, O(log n), `lower_bound`, `upper_bound`, `prev`), `unordered_map`/`unordered_set` (average O(1), use `.count()` or `.find()` to avoid inserting with `[]`), `multiset` (erase one: `ms.erase(ms.find(x))`), `bitset<32>`, algorithms (`sort` with lambda, `reverse`, `accumulate` with `0LL`, `max_element`, `next_permutation`, `iota`, `unique` + `erase`, `lower_bound` on sorted vector), `__gcd`/`std::gcd`, `INT_MAX`, `LLONG_MAX`, fast I/O `ios::sync_with_stdio(false); cin.tie(nullptr);`.
- **Python**: `collections.Counter`, `defaultdict(list)`, `deque` (`appendleft`, `popleft` O(1)), `OrderedDict.move_to_end` (LRU), `heapq` (`heappush`, `heappop`, `heapify`, `nlargest`, tuples for priority), `bisect_left/right`, `itertools` (`permutations`, `combinations`, `accumulate`, `product`), `functools.lru_cache` / `cache` for memoised DP, `sorted(key=lambda x: (x[0], -x[1]))`, `math.gcd`, `math.inf`, `int` is arbitrary precision (but modulo still required), `sys.setrecursionlimit`, `sys.stdin.readline` for fast input in OAs, string `join` instead of `+=` in loops, `ipaddress` module (handy for automation chapter but usually not allowed in DSA rounds).

### A1.7 The structured approach for coding rounds (UMPIRE + talk track)

Present UMPIRE (CodePath): **U**nderstand, **M**atch, **P**lan, **I**mplement, **R**eview, **E**valuate. Map it to a 45-minute round:

| Minute | Step | What you do and say |
|---|---|---|
| 0–5 | Understand | Restate the problem in your own words. Ask about input size, value range, duplicates, negatives, empty input, return format, sortedness, in-place allowed. Work one example by hand and agree on expected output. |
| 5–8 | Match | Name candidate patterns from the decoder table: "Contiguous plus longest suggests sliding window." |
| 8–15 | Plan | State brute force and its complexity first, then the optimisation and why it works. Get a nod before coding. Write the plan as 4–6 comment lines. |
| 15–32 | Implement | Code in small, named pieces; narrate intent, not keystrokes. |
| 32–38 | Review | Dry-run the agreed example line by line; then run the edge-case checklist. |
| 38–45 | Evaluate | State time and space complexity; discuss trade-offs and follow-ups (streaming input, memory limit, multithreaded, very large n). |

"How to talk while coding" box (phrases to rehearse):
- Clarifying: "Can the input be empty? Are values bounded? Should I optimise for time or memory?"
- Brute force first: "A naive way is O(n²) by checking all pairs; let me improve on that."
- Thinking aloud when stuck: "I am looking for repeated work; the inner loop recomputes the same sum, so a prefix sum removes it."
- Signposting: "I will write a helper `isValid` and come back to it."
- Taking hints well: "That is a good point; if the array is sorted I can use two pointers instead of the hash set."
- Testing: "Let me trace `[2, 7, 11, 15]`, target 9: i = 0, need 7, not seen; i = 1, need 2, seen at 0, return [0, 1]."
- Admitting a bug: "This fails for a single element; I will add a guard."
- Don'ts: silent coding for more than two minutes; arguing with hints; claiming complexity without justification; renaming the problem into one you know.

Google-specific note from candidate reports: interviewers expect discussion of several approaches and trade-offs before coding (Medium, Google India experience https://medium.com/jinal-parikh/google-india-interview-experience-6589600ac4f8 ). Teamblind L3 report: candidate proposed union-find, interviewer asked for BFS because union-find is "lengthy to implement", showing the value of offering alternatives (https://www.teamblind.com/post/google-phone-screen-l3-m1wkhbxc ).

Sources: CodePath UMPIRE guide https://guides.codepath.com/compsci/UMPIRE-Interview-Strategy ; https://www.designgurus.io/blog/mastering-the-umpire-interview-strategy-in-coding-a-step-by-step-guide ; Tech Interview Handbook coding interview cheatsheet https://www.techinterviewhandbook.org/coding-interview-cheatsheet/

### A1.8 Study sheets to cross-reference

Name the sheets once in a "Which list should I do?" box: Blind 75, NeetCode 150 (https://neetcode.io/practice), Striver SDE / A2Z sheet (https://takeuforward.org), Sean Prashad patterns (https://seanprashad.com/leetcode-patterns/), Grokking patterns. Recommendation for this book's audience: NeetCode 150 core + the "networking-flavoured" 20 from A1.3 + the C-specific list in A3.5.

## A2. Networking interview hacks

### A2.1 Mnemonics page

| Topic | Mnemonic | Expansion and the trap to mention |
|---|---|---|
| OSI layers, 1 → 7 | **P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way | Physical, Data link, Network, Transport, Session, Presentation, Application |
| OSI layers, 7 → 1 | **A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing | Same, top-down. Interview trap: TCP/IP model has 4 layers (or 5 in Tanenbaum/Kurose teaching). Nokia candidates were asked which came first, OSI or TCP/IP (TCP/IP in practice; OSI was standardised 1984). |
| PDU names | "**D**on't **S**top **P**acking **F**rames **B**its" (Data, Segment, Packet, Frame, Bits) | L4 segment (TCP) / datagram (UDP) |
| DHCP | **DORA** | Discover (broadcast, client UDP 68 → server 67), Offer, Request (broadcast, so other servers withdraw), Acknowledge. Renewal at T1 = 50% lease (unicast), rebinding at T2 = 87.5%. Relay: `ip helper-address`, giaddr field. |
| TCP handshake / teardown | "SYN, SYN-ACK, ACK" ; teardown "FIN, ACK, FIN, ACK" | TIME_WAIT = 2 × MSL on the side that closes first. RST aborts. |
| TCP state names | "**L**isten, **S**yn-sent, **S**yn-received, **E**stablished" then "FIN-WAIT-1, FIN-WAIT-2, CLOSE-WAIT, CLOSING, LAST-ACK, TIME-WAIT, CLOSED" | Draw the state diagram once in Chapter CN; reprint here as thumbnail. |
| OSPF neighbour states | "**D**own, **A**ttempt (NBMA only), **I**nit, **2**-Way, **E**xStart, **E**xchange, **L**oading, **F**ull". Book mnemonic: "**D**o **A**ll **I**ndian **T**eams **E**ver **E**at **L**ots of **F**ood?" | Stuck in ExStart/Exchange usually means MTU mismatch; stuck in 2-Way between DROthers is normal; stuck in Init means one-way hellos (ACL, unidirectional link). Hello/dead mismatch, area ID, authentication, subnet/mask, stub flag must match for adjacency. |
| OSPF LSA types | "**R**eally **N**ice **S**ummaries **A**re **E**asy **N**ow" = 1 Router, 2 Network, 3 Summary, 4 ASBR summary, 5 External, 7 NSSA external | Area types: standard, stub (no 5), totally stubby (no 3/4/5), NSSA (7 instead of 5). |
| BGP best-path (Cisco order) | **W**e **L**ove **O**ranges **AS** **O**ranges **M**ean **P**ure **R**efreshment | Weight (highest, Cisco-local), Local preference (highest), Originated locally, AS_PATH (shortest), Origin (IGP < EGP < incomplete), MED (lowest), Paths: eBGP over iBGP, then lowest IGP metric to next hop, oldest eBGP path, Router ID (lowest), cluster list length, neighbour address. Mnemonic stops before IGP metric/age, say so. Alternative fuller mnemonic: "**N** WLLA OMNI" (Next-hop reachable, Weight, Local pref, Locally originated, AIGP, AS path, Origin, MED, Neighbour type, IGP metric). |
| BGP neighbour states | "**I**dle **C**ats **A**lways **O**pen **O**ld **E**nvelopes" | Idle, Connect, Active, OpenSent, OpenConfirm, Established. Trap: "Active" means it is actively trying and failing (TCP 179 not reaching), not healthy. |
| STP root bridge election | "**Lowest wins everything**" | Root bridge = lowest Bridge ID (priority, default 32768 + VLAN ID in PVST+ extended system ID, then lowest MAC). Root port per non-root switch = lowest root path cost → lowest sender BID → lowest sender port ID (priority then number). Designated port per segment = lowest cost to root → lowest BID → lowest port ID. Everything else blocks. |
| STP port states (802.1D) | "**B**ig **L**ions **L**ike **F**ood" | Blocking (20 s max age), Listening (15 s), Learning (15 s), Forwarding; Disabled. Convergence ≈ 30–50 s. RSTP: Discarding, Learning, Forwarding; roles root/designated/alternate/backup. Costs: 10 Mb/s 100, 100 Mb/s 19, 1 Gb/s 4, 10 Gb/s 2 (short method). |
| EIGRP K-values | "**B**ig **L**orries **D**rive **R**eally **L**oaded" | K1 bandwidth, K2 load, K3 delay, K4 reliability, K5 load (default K1 = K3 = 1, others 0). Feasibility condition: reported distance < feasible distance. |
| ARP | "Who has? Tell me." | ARP request broadcast (ff:ff:ff:ff:ff:ff), reply unicast; gratuitous ARP for duplicate-address detection and failover; proxy ARP; ARP cache timeout (Cisco 4 h, Linux ~minutes). |
| VLAN trunking | "**802.1Q puts four bytes in**" | TPID 0x8100, PCP 3 bits, DEI 1, VID 12 bits (4094 usable). Native VLAN is untagged; native-VLAN mismatch causes leaks/CDP warnings. |
| NAT terms | "**I**nside **L**ocal is what **I** **L**ive with" | Inside local (private), inside global (public), outside global, outside local. PAT = overload. |
| TCP congestion control | "**S**low start **C**limbs, **F**ast **R**ecovery **R**escues" | Slow start (cwnd doubles per RTT until ssthresh), congestion avoidance (+1 MSS per RTT), fast retransmit on 3 duplicate ACKs, fast recovery; timeout → cwnd = 1 MSS. Flow control (rwnd, receiver protection) vs congestion control (cwnd, network protection): asked at Meta/Google network-engineer interviews. CUBIC is Linux default; BBR is Google's. |
| Wireless (802.11) association | "**P**robe, **A**uth, **A**ssoc, **4-way**" | Probe request/response, open authentication, association, then 802.1X/EAP (enterprise) and the WPA2/WPA3 4-way handshake (PTK/GTK). CSMA/CA, RTS/CTS for hidden node. |
| IPsec | "**I**KE **K**eeps **E**ncryption" | IKE phase 1 (UDP 500, ISAKMP SA), phase 2 (IPsec SAs), ESP (protocol 50, encrypts) vs AH (51, no encryption, breaks with NAT), NAT-T UDP 4500. |

Sources: BGP mnemonic thread https://community.cisco.com/t5/switching/is-it-possible-to-know-why-would-bgp-prefer-path-over-the-other/m-p/3012915/highlight/true ; ACI forum on AIGP in path selection https://forums.acilearning.com/topic/3388/aigp-in-bgp-path-selection-350-401-encor ; Noction BGP best-path https://www.noction.com/blog/bgp_bestpath_selection_algorithm ; Safari CCNP "Memorization Tips for BGP Best Path" https://www.safaribooksonline.com/library/view/ccnp-routing-and/9780133149883/ch14lev3sec16.html ; Cisco BGP path selection https://docs.manage.security.cisco.com/cdfmc/c_bgp_path_selection.html

### A2.2 Subnetting speed tricks

Page 1: **Powers of two strip** (print across the top margin of every subnetting page):
2^0..2^16 = 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536.

Page 2: **Mask value ladder** (bits set in one octet → decimal): 1 → 128, 2 → 192, 3 → 224, 4 → 240, 5 → 248, 6 → 252, 7 → 254, 8 → 255. Memory hook: "each step adds the next half: 128, +64, +32, +16, +8, +4, +2, +1".

Page 3: **/24 to /32 table** (the range CCNA and campus MCQs test hardest):

| Prefix | Mask | Block size (magic number) | Total addresses | Usable hosts | Subnets in a /24 |
|---|---|---|---|---|---|
| /24 | 255.255.255.0 | 256 | 256 | 254 | 1 |
| /25 | .128 | 128 | 128 | 126 | 2 |
| /26 | .192 | 64 | 64 | 62 | 4 |
| /27 | .224 | 32 | 32 | 30 | 8 |
| /28 | .240 | 16 | 16 | 14 | 16 |
| /29 | .248 | 8 | 8 | 6 | 32 |
| /30 | .252 | 4 | 4 | 2 | 64 |
| /31 | .254 | 2 | 2 | 2 (RFC 3021 point-to-point) | 128 |
| /32 | .255 | 1 | 1 | 1 (host route, loopback) | 256 |

Extend with a /16–/23 mini-table (block size in third octet: /23 → 2, /22 → 4, /21 → 8, /20 → 16, /19 → 32, /18 → 64, /17 → 128).

Page 4: **The magic-number method, 5 steps** (worked on 172.16.45.14/20):
1. Find the interesting octet (the mask octet that is neither 255 nor 0): /20 = 255.255.240.0, third octet.
2. Magic number = 256 − 240 = 16.
3. Network = largest multiple of 16 ≤ 45 → 32 → network 172.16.32.0.
4. Next network = 32 + 16 = 48 → broadcast = 172.16.47.255.
5. Usable range = 172.16.32.1 – 172.16.47.254; hosts = 2^12 − 2 = 4094.

Further tricks:
- **Hosts needed → prefix**: smallest h with 2^h − 2 ≥ hosts; prefix = 32 − h. (50 hosts → h = 6 → /26.)
- **Subnets needed → borrowed bits**: smallest s with 2^s ≥ subnets.
- **Is it a valid host?** Not the network (multiple of block) and not broadcast (next multiple − 1).
- **Same subnet test**: AND both IPs with the mask (or check both fall in the same block).
- **Wildcard mask** = 255.255.255.255 − subnet mask (for ACLs and OSPF network statements): /26 → 0.0.0.63.
- **Summarisation (supernetting)**: write the varying octet in binary, count common leading bits. 192.168.8.0 – 192.168.15.0 → 8 = 00001000, 15 = 00001111 → 5 common bits in the third octet → 16 + 5 = /21 → 192.168.8.0/21. Shortcut: a range of 2^k contiguous, aligned blocks summarises to prefix − k.
- **VLSM order**: allocate largest subnets first, keep blocks aligned to their own size.
- **Private ranges**: 10.0.0.0/8, 172.16.0.0/12 (172.16–172.31), 192.168.0.0/16; CGNAT 100.64.0.0/10; link-local 169.254.0.0/16 (APIPA); loopback 127.0.0.0/8; multicast 224.0.0.0/4 (224.0.0.5/6 OSPF, 224.0.0.10 EIGRP, 224.0.0.9 RIPv2, 224.0.0.18 VRRP, 224.0.0.102 HSRPv2).
- **Classful leftovers (still asked in Indian MCQs)**: first-octet ranges A 1–126, B 128–191, C 192–223, D 224–239, E 240–255.
- **IPv6 quick facts**: 128 bits, `::` once only, drop leading zeros per hextet; /64 for LANs; link-local fe80::/10; unique local fc00::/7; global unicast 2000::/3; multicast ff00::/8 (ff02::1 all nodes, ff02::2 all routers, ff02::1:ffXX:XXXX solicited-node); EUI-64 flips the 7th bit and inserts ff:fe; no broadcast; NDP (ICMPv6 133–137) replaces ARP; SLAAC vs DHCPv6.
- **Speed drill spec**: "60-second subnet" drills, 20 per chapter page, answers upside down at page foot; target under 30 s each by the end of the networking pillar.

Sources: Professor Messer magic number method https://www.professormesser.com/network-plus/n10-009/n10-009-video/magic-number-subnetting-n10-009/ ; https://oneuptime.com/blog/post/2026-03-20-subnetting-magic-number-method/view ; https://smenode-academy.com/blog/subnetting-practice-questions/ ; https://computingforgeeks.com/subnetting-cheat-sheet/

### A2.3 Well-known ports and protocol numbers

Port table (group by "must know" vs "good to know"; mark TCP/UDP):

Must know: 20/21 FTP (TCP), 22 SSH (TCP), 23 Telnet (TCP), 25 SMTP (TCP), 53 DNS (UDP for queries, TCP for zone transfer and large responses), 67/68 DHCP (UDP, server/client), 69 TFTP (UDP), 80 HTTP (TCP), 110 POP3, 123 NTP (UDP), 143 IMAP, 161/162 SNMP (UDP, agent/trap), 179 BGP (TCP), 443 HTTPS (TCP; HTTP/3 over UDP 443 QUIC), 514 Syslog (UDP), 520 RIP (UDP), 3389 RDP.

Good to know (networking roles): 49 TACACS+ (TCP), 1812/1813 RADIUS (UDP auth/accounting), 389/636 LDAP/LDAPS, 500 IKE and 4500 NAT-T (UDP), 646 LDP, 830 NETCONF over SSH, 57400 gNMI (common default, vendor dependent), 3784/3785 BFD (UDP), 4789 VXLAN (UDP), 6081 Geneve, 2049 NFS, 5060/5061 SIP, 1701 L2TP, 1723 PPTP, 1985 HSRP (UDP), 6633/6653 OpenFlow, 8080 HTTP alternate, 2222/830 sometimes used for device management, 5353 mDNS.

Ephemeral port ranges: IANA 49152–65535; Linux default 32768–60999 (`/proc/sys/net/ipv4/ip_local_port_range`).

IP protocol numbers: 1 ICMP, 2 IGMP, 4 IP-in-IP, 6 TCP, 17 UDP, 41 IPv6 encapsulation, 47 GRE, 50 ESP, 51 AH, 58 ICMPv6, 88 EIGRP, 89 OSPF, 103 PIM, 112 VRRP, 132 SCTP. EtherTypes: 0x0800 IPv4, 0x0806 ARP, 0x86DD IPv6, 0x8100 802.1Q, 0x88A8 802.1ad (QinQ), 0x8847 MPLS unicast, 0x88CC LLDP, 0x8863/0x8864 PPPoE.

ICMP types worth memorising: 0 echo reply, 3 destination unreachable (code 3 port unreachable; code 4 fragmentation needed and DF set, which drives PMTUD), 5 redirect, 8 echo request, 11 time exceeded (traceroute), 12 parameter problem.

"Trick" box: protocols that ride on others: BGP rides TCP 179; OSPF is IP protocol 89 (no TCP/UDP); EIGRP is IP 88; RIP is UDP 520; IS-IS sits directly on layer 2 (no IP); DHCP and DNS are application layer over UDP; ICMP is layer 3 but is carried inside IP. Why BGP uses TCP: reliable, ordered delivery for incremental updates, so BGP needs no own retransmission; question appears in BGP interview lists (https://www.pynetlabs.com/bgp-interview-questions-and-answers/ ).

### A2.4 Administrative distance (Cisco defaults)

| Source | AD |
|---|---|
| Connected interface | 0 |
| Static route | 1 |
| EIGRP summary | 5 |
| eBGP | 20 |
| EIGRP internal | 90 |
| IGRP (legacy) | 100 |
| OSPF | 110 |
| IS-IS | 115 |
| RIP | 120 |
| EIGRP external | 170 |
| iBGP | 200 |
| Unknown / unusable | 255 |

Mnemonic: "**0-1-5-20-90-110-115-120-170-200-255**: Connected, Static, Summary, eBGP, EIGRP, OSPF, IS-IS, RIP, EIGRP-ex, iBGP, Unreachable." Also note route-selection order: longest prefix match first, then AD, then metric. Juniper uses "route preference" with different numbers (direct 0, static 5, OSPF internal 10, IS-IS L1 15, IS-IS L2 18, RIP 100, OSPF external 150, BGP 170), print a side column for Juniper candidates. Floating static route = static with AD set higher than the dynamic protocol.

### A2.5 Header field quick reference

One page with box diagrams (32-bit rows) for: Ethernet II, 802.1Q tag, ARP, IPv4, IPv6, TCP, UDP, ICMP, plus a "sizes" sidebar.

- **Ethernet II**: preamble 7 B + SFD 1 B (not counted in frame size), destination MAC 6, source MAC 6, (optional 802.1Q 4), EtherType 2, payload 46–1500, FCS 4 (CRC-32). Minimum frame 64 B, maximum 1518 B (1522 with a tag); jumbo frames to ~9000 B. Interframe gap 12 B. MAC: first 3 bytes OUI; I/G bit (multicast) is the LSB of the first byte; U/L bit next.
- **IPv4** (20–60 B): Version 4, IHL 4 (in 32-bit words), DSCP 6 + ECN 2, Total length 16, Identification 16, Flags 3 (reserved, DF, MF), Fragment offset 13 (in 8-byte units), TTL 8, Protocol 8, Header checksum 16 (header only, recomputed at each hop because TTL changes), Source 32, Destination 32, Options.
- **IPv6** (40 B fixed): Version, Traffic class 8, Flow label 20, Payload length 16, Next header 8, Hop limit 8, Source 128, Destination 128. No header checksum, no router fragmentation (only source, via Fragment extension header), minimum MTU 1280.
- **TCP** (20–60 B): Source port, Destination port, Sequence number 32, Acknowledgement number 32, Data offset 4, reserved, flags (CWR, ECE, URG, ACK, PSH, RST, SYN, FIN: mnemonic "**C**ats **E**at **U**nder **A**ll **P**eople's **R**ed **S**ofas **F**reely"), Window 16 (scaled by Window Scale option), Checksum (with pseudo-header), Urgent pointer, Options (MSS, Window Scale, SACK permitted, Timestamps).
- **UDP** (8 B): Source port, Destination port, Length, Checksum (optional in IPv4, mandatory in IPv6).
- **ARP** (28 B for IPv4 over Ethernet): HTYPE, PTYPE, HLEN 6, PLEN 4, Opcode (1 request, 2 reply), sender MAC, sender IP, target MAC, target IP.
- **Sizes sidebar**: MTU 1500 → IPv4 + TCP headers 40 → MSS 1460; over PPPoE MTU 1492 → MSS 1452; GRE adds 24 B; IPsec ESP adds ~50–73 B; VXLAN adds 50 B (so underlay MTU ≥ 1550); MPLS label 4 B each. MSS vs MTU and MTU-mismatch symptoms are a reported Amazon NDE topic.

### A2.6 "What happens when you type google.com and press Enter": master answer skeleton

Teach as a 9-stage ladder; the student picks depth according to time ("2-minute version" vs "15-minute version"). Glassdoor reports Google network-engineer candidates being asked to explain how a device reaches google.com using the OSI model (https://www.glassdoor.com/Interview/Google-Network-Engineer-Interview-Questions-EI_IE9079.0,6_KO7,23.htm ).

0. **Before anything**: the host already has an IP, mask, default gateway, DNS server (from DHCP: DORA). Mention once.
1. **Browser side**: URL parsing, HSTS preload check (forces HTTPS), browser cache, service worker.
2. **Name resolution**: browser DNS cache → OS cache / hosts file → stub resolver queries recursive resolver (UDP 53; or DoH/DoT) → resolver does iterative lookup: root → .com TLD → google.com authoritative → A/AAAA record (often a GeoDNS/anycast answer). TTL caching.
3. **Next-hop decision**: destination IP not on local subnet (AND with mask) → send to default gateway; ARP for the gateway's MAC if not cached (broadcast request, unicast reply).
4. **Transport setup**: TCP 3-way handshake to port 443 (SYN with MSS/window scale/SACK options, SYN-ACK, ACK); or QUIC over UDP 443 for HTTP/3.
5. **TLS 1.3 handshake**: ClientHello (SNI, ALPN h2/h3, key share), ServerHello, certificate chain verified against trust store, session keys derived; 1-RTT (0-RTT on resumption).
6. **The packet's journey**: encapsulation down the stack (HTTP → TLS records → TCP segment → IP packet → Ethernet frame); home router NAT/PAT rewrites source IP/port; ISP routing; BGP between ASes chooses the path; arrives at Google's edge (anycast front end, load balancer). At every router: decapsulate L2, longest-prefix match, decrement TTL, recompute IPv4 checksum, re-encapsulate with new L2 header (MAC changes every hop, IP stays the same except at NAT).
7. **Server side**: load balancer → front-end server; HTTP request (GET /, headers, cookies); response 200 or 301/302 redirect; compression; CDN caching.
8. **Rendering**: HTML parse, DOM, CSSOM, render tree, JavaScript, further requests (parallel streams over HTTP/2 or HTTP/3), connection reuse.
9. **Teardown / keep-alive**: persistent connections; FIN sequence later.

"Interviewer follow-up bank" box: What if DNS is UDP and the response is large (TCP fallback / EDNS0)? What changes in IPv6 (NDP instead of ARP, no NAT)? What if the ARP reply never arrives? How does the gateway know the route (routing table, default route from ISP)? What does traceroute show here? What changes behind a corporate proxy? How does anycast deliver you to the nearest Google front end? Where can it break and how would you troubleshoot each stage?

Sources: https://github.com/alex/what-happens-when ; Glassdoor Google network engineer page above.

### A2.7 Troubleshooting answer framework

Name: **"SCOPE-LAYER-FIX-PROVE"** (book's own framing; based on the standard structured approaches: bottom-up/top-down/divide-and-conquer/follow-the-path from Cisco troubleshooting methodology).

1. **Scope** (ask before touching anything): What exactly fails? One user or many? One application or all? Since when? What changed (config, upgrade, cabling)? Can I reproduce it? Is there a known-good comparison?
2. **Layer it**: choose method aloud: bottom-up (physical first: link lights, `show interfaces` errors/CRC, duplex mismatch, speed), top-down (application first), divide-and-conquer (start at layer 3 with `ping`), follow-the-path (hop by hop with `traceroute`), compare-configurations (diff against a working device).
3. **Gather evidence by layer**:
   - L1: interface up/down, CRC/input errors, optics levels (`show interfaces transceiver`), cable.
   - L2: VLAN membership, trunk allowed list, native VLAN, STP state (blocking?), MAC address table, ARP table, duplex.
   - L3: IP/mask/gateway correct, routing table (`show ip route x.x.x.x`), neighbour adjacencies (OSPF/BGP state), ACLs, NAT translations, MTU (`ping` with DF bit and size).
   - L4–7: port reachability (`telnet host port`/`nc -vz`), firewall, DNS (`nslookup`/`dig`), TLS certificate, application logs.
   - Tools card: `ping`, `traceroute`/`tracert`/`mtr`, `arp -a`/`ip neigh`, `ip route`, `ss -tulpn`, `tcpdump -i eth0 host x and port 443`, Wireshark filters, `dig +trace`, `curl -v`, `ethtool`.
4. **Hypothesise and fix**: one change at a time, with rollback plan and change window; say "I would check X because symptom Y points to Z".
5. **Prove and prevent**: verify from the user's view, monitor, document root cause, add alerting/automation (links to the Automation pillar).

Practice scenarios to include (each with a 5-line model answer): "User can ping IP but not name" (DNS); "Can ping gateway but not internet" (default route/NAT/ISP); "Works for small packets, large transfers hang" (MTU/PMTUD black hole, ICMP type 3 code 4 blocked; fix MSS clamping); "Two hosts in same VLAN on different switches can't talk" (trunk allowed list / native VLAN); "OSPF neighbour stuck in ExStart" (MTU); "BGP stuck in Active" (TCP 179 blocked, wrong neighbour IP, update-source/ebgp-multihop for loopbacks); "Intermittent slowness every few minutes" (STP topology changes, duplex mismatch, broadcast storm); "New VLAN users don't get DHCP" (missing helper address/relay); "Website slow only for some users" (DNS GeoIP, asymmetric routing, ECMP hashing). Amazon NDE phone screens are reported as "all troubleshooting" (https://www.jointaro.com/interviews/companies/amazon/experiences/network-development-engineer-sydney-january-1-2024-no-offer-neutral-2399baf2/ ).

### A2.8 One-liners interviewers love (rapid-fire page)

Fifty one-line Q&As in two columns. Examples: hub vs switch vs router (L1 repeater / L2 MAC learning, per-port collision domain / L3, per-port broadcast domain); collision domain vs broadcast domain; TCP vs UDP (8 differences); why the MAC changes every hop but the IP does not; ARP vs RARP vs GARP; static vs dynamic routing; distance vector vs link state; OSPF vs BGP (IGP/EGP, metric cost vs path attributes, IP 89 vs TCP 179); iBGP split horizon and full-mesh/route reflectors; why loopbacks for iBGP peering; VLAN vs subnet; access vs trunk port; STP purpose; EtherChannel/LACP; HSRP vs VRRP vs GLBP; NAT vs PAT; stateful vs stateless firewall; IDS vs IPS; symmetric vs asymmetric encryption; SSL/TLS handshake; IPv4 vs IPv6; what is MPLS (label swapping, LSP, LDP); VXLAN and EVPN in one line; spine-leaf vs three-tier; QoS (classification, marking DSCP EF = 46, queuing, policing vs shaping); multicast IGMP and PIM; what is a socket; `select` vs `poll` vs `epoll`; process vs thread; zombie vs orphan (asked at Arista).

## A3. Online-assessment (OA) hacks

### A3.1 What the OAs look like (reported formats; verify per drive)

| Company | Platform reported | Reported format | Sources |
|---|---|---|---|
| Cisco | HackerRank (and Code with Cisco) | 2023: 90 min, 42 questions (40 MCQ on CS fundamentals + 2 coding), languages C/Python/Java only. 2024: 41 MCQ + 1 coding. 2026 prep guides: ~90 min, ~40 MCQ + 2 DSA, AI proctoring, no negative marking. MCQs heavy on networking (TCP/IP, OSI, routing, security) plus OS, DBMS, aptitude. Network-engineer drive 2025 (Bengaluru): OA with networking + coding, then a PPT submission. | https://dev.to/net_programhelp_e160eef28/cisco-hackerrank-online-assessment-2026-real-questions-preparation-guide-4e21 ; https://faceprep.in/article/cisco-hiring-process-for-freshers-2026/ ; https://www.geeksforgeeks.org/cisco-interview-experience-sde-for-cloud-applications-6-month-internship-fte-on-campus/ ; https://static.glassdoor.nl/Interview/Cisco-Interview-E1425-RVW92472623.htm |
| Juniper | HackerRank | 90 min, 33 questions (32 MCQ + 1 coding): aptitude, CN, DBMS, OS, HTML/CSS, output prediction. Oct 2024 intern: 38 questions (35 MCQ on networks, time complexity, C + 3 coding), tight on time. Older: ~50 networking + C MCQs. Process 4–5 rounds. | https://www.geeksforgeeks.org/juniper-networks-interview-experience-3/ ; https://www.geeksforgeeks.org/interview-experiences/juniper-networks-recruitment-process/ ; https://leetcode.com/discuss/post/2936128/juniper-networks-swe-intern6-months-bangalore-dec-2022-offer |
| Qualcomm | Varies (written / online) | Sectioned MCQs: aptitude + C programming + CS fundamentals (DS, OS, architecture, networking, digital logic), most questions C and OOP. | https://www.geeksforgeeks.org/?p=463420 ; https://www.geeksforgeeks.org/qualcomm-interview-experience-pool-campus-drive/ |
| Arista | HackerRank | 1.5 h test in C/C++; 4–5 coding problems or mix of coding + MCQ on C/C++, networking, OS; another report: 2 medium–hard coding questions. Later rounds on CoderPad. | https://www.glassdoor.co.in/Interview/Arista-Networks-Interview-Questions-E295128.htm ; https://www.geeksforgeeks.org/interview-experiences/arista-networks-recruitment-process/ |
| Nokia | AMCAT | Aptitude, logical, verbal + 2 basic coding (C/C++ only in some drives; e.g. GCD of numbers, sort and print alternate elements, balanced parentheses). Then technical + HR interviews. | https://www.geeksforgeeks.org/nokia-networks-interview-experienceon-campus-set-6/ ; https://www.geeksforgeeks.org/?p=425992 |
| Microsoft | Codility / HackerRank / AMCAT reported | 2 coding questions (medium–hard, DP/graph/greedy/binary search); on-campus timelines short. | https://www.jointaro.com/interviews/companies/microsoft/experiences/software-developer-intern-bengaluru-july-1-2024-no-offer-positive-b1cb2adb ; https://www.jointaro.com/interviews/companies/microsoft/experiences/software-development-engineer-sde-intern-bengaluru-september-2-2025-accepted-offer-positive-039cdaca |
| Amazon (NDE) | Amazon's own OA (varies) / phone screens | NDE loops: CV review, phone screen (troubleshooting-heavy), loop of 4–5 rounds mixing networking depth (BGP, OSPF, TCP/IP, MTU/MSS), Python automation, Leadership Principles. | https://www.glassdoor.co.in/Interview/Amazon-Network-Development-Engineer-Interview-Questions-EI_IE6036.0,6_KO7,35.htm ; https://www.jointaro.com/interviews/companies/amazon/experiences/network-development-engineer-sydney-january-1-2024-no-offer-neutral-2399baf2/ |
| Google | Online coding / phone screen | Phone screen: 1–2 LeetCode-style questions; onsite 3–4 technical + Googleyness & Leadership; network-engineer track adds networking rounds and a basic Python question in a shared doc. | https://leetcode.com/discuss/post/6848596/google-l3-sde-ii-interview-experience-5-9ffz2/ ; https://www.glassdoor.com/Interview/Google-Network-Engineer-Interview-Questions-EI_IE9079.0,6_KO7,23.htm |
| Broadcom | Varies | C-heavy technical rounds (bit manipulation, linked lists, pointers, arrays, stacks/queues), OS and some networking; several interview rounds with hiring manager and engineers. | https://www.glassdoor.co.in/Interview/Broadcom-Interview-Questions-E6926.htm ; https://dataford.io/interview-guides/broadcom/software-engineer |

Generic platform facts (for a "Know your battlefield" box):
- **AMCAT**: three compulsory adaptive sections (English, quantitative, logical; one 2026 guide lists 18 + 16 + 14 questions) + personality inventory (AMPI) + optional modules; Automata = 2 coding problems (~45 min in one source, ~30 in another); Automata Fix = 7 debugging questions in 20 min (C/C++/Java); total ~100 min depending on modules. Adaptive means early accuracy matters more than speed. Sources: https://faceprep.in/article/amcat-test-2026-complete-guide-pattern-and-scoring/ ; https://prepinsta.com/amcat/syllabus/
- **Mercer Mettl**: the employer configures section order, timings, negative marking and section locking; read the instructions screen carefully, as you may not be able to return to a locked section. Source: https://www.careertestprep.com/knowledge/mercer-mettl-assessment ; https://prepinsta.com/mettl/syllabus/
- **CoCubes**: modular (aptitude, computer fundamentals, domain, coding, English, psychometric); standard configurations report no negative marking. Source: https://faceprep.in/article/cocubes-test-2026-pattern-sections-and-preparation/
- **HackerRank**: hidden test cases; partial marks per test case; custom input box; you can usually switch languages per question; stdin parsing is your job (practise reading `n` then `n` integers fast); proctoring with tab-switch detection.

### A3.2 OA strategy and time management

- **First 3 minutes**: read every question title and the marking scheme; note whether negative marking applies and whether sections lock.
- **MCQ sections**: two-pass method. Pass 1: answer anything you can do in under 45 s; flag the rest. Pass 2: flagged ones in order of confidence. Never leave blanks if there is no negative marking.
- **Coding sections**: read constraints first (A1.1). Submit a correct brute force early to bank partial test cases, then optimise. Write the I/O skeleton before thinking hard. Keep a personal template file in memory (fast I/O, `long long`, common includes).
- **Partial-credit hacks**: handle obvious edge cases first (empty input, n = 1); if TLE, check for `endl` flushing in C++ (use `'\n'`), Python `input()` vs `sys.stdin`; recursion depth.
- **Time budget for a 90-minute Cisco-style paper (40 MCQ + 2 coding)**: 30 min MCQ (45 s each), 25 min per coding question, 10 min buffer. Rehearse this in the mock papers.
- **Proctoring etiquette**: one screen, stable light, no phone on desk, do not read aloud, keep face in frame; tab switches are logged.

### A3.3 MCQ elimination tactics

1. Eliminate absolute words in conceptual MCQs ("always", "never") unless the statement is definitional.
2. For networking MCQs, map each option to its OSI layer; options at the wrong layer are usually distractors (e.g. "Which device separates broadcast domains? Hub/Switch/Router/Repeater": only a router (or L3 switch/VLAN) works).
3. Numeric MCQs: estimate first, then eliminate by parity, units digit or order of magnitude before computing fully.
4. Output-prediction: look first for compile errors and undefined behaviour; "Compiler error" and "Undefined" are frequently the intended answer.
5. Two options that are opposites: one is usually right.
6. If two options are identical in effect, both are wrong (in single-answer MCQs).
7. Check edge readings: "maximum number of hosts" (subtract 2) vs "number of addresses" (do not).

### A3.4 Aptitude shortcuts (one formula card per topic, each with two solved examples)

- **Percentages**: successive change a% then b% → net a + b + ab/100. If price rises r%, consumption must fall r/(100 + r) × 100% to keep expenditure fixed. Fraction table: 1/6 = 16.67%, 1/7 = 14.28%, 1/8 = 12.5%, 1/9 = 11.11%, 1/11 = 9.09%, 1/12 = 8.33%.
- **Profit and loss**: profit% on cost price; with false weights, gain% = (error / true value − error) × 100; successive discounts as successive percentages.
- **Simple and compound interest**: CI − SI for 2 years = P(r/100)²; for 3 years = P(r/100)²(3 + r/100). Rule of 72 for doubling.
- **Ratio, mixtures, alligation**: alligation cross rule (mean − cheaper) : (dearer − mean).
- **Time and work**: LCM method (take total work = LCM of days, compute units/day); A and B together = ab/(a + b) days; pipes: filling positive, leaking negative.
- **Time, speed, distance**: average speed for equal distances = 2xy/(x + y); relative speed (same direction subtract, opposite add); train crossing a pole = length/speed, crossing a platform = (train + platform)/speed; km/h to m/s × 5/18; boats: downstream u + v, upstream u − v.
- **Number system**: divisibility rules (3, 4, 8, 9, 11, 7 via doubling trick); number of divisors from prime factorisation ∏(e + 1); sum of divisors; HCF × LCM = product of two numbers; unit-digit cyclicity (2, 3, 7, 8 cycle of 4; 4 and 9 cycle of 2; 0, 1, 5, 6 fixed); remainders: Fermat's little theorem, (a × b) mod n; trailing zeros of n! = Σ ⌊n/5^k⌋; base conversion (binary/octal/hex, very common in networking MCQs).
- **Permutations and combinations**: nPr, nCr, circular (n − 1)!, identical objects n!/(p!q!), stars and bars C(n + r − 1, r − 1), derangements.
- **Probability**: complement trick (P(at least one) = 1 − P(none)); dice (36 outcomes), cards (52, 4 suits, 12 face cards), coins (2^n); conditional and Bayes on one line; birthday-type questions.
- **Clocks and calendars**: angle = |30H − 5.5M|; hands overlap every 65 5/11 min; odd days (normal year 1, leap year 2; century rule).
- **Averages, ages, series, coding-decoding, blood relations, seating arrangement, syllogisms, data sufficiency, data interpretation**: one card each with a decision procedure (e.g. syllogisms: Venn diagram the "definitely true" case only).
- **Verbal**: reading-comprehension skim order (questions first), sentence correction rules (subject–verb agreement, tense consistency), para-jumbles (find the opening sentence that introduces a noun without a pronoun).

Sources (formats and topic coverage): https://faceprep.in/article/amcat-syllabus-2026-section-wise-breakdown/ ; https://prepinsta.com/amcat/ ; https://cpt.hitbullseye.com/CoCubes/Co-Cubes-Test-Pattern.php

### A3.5 C output-prediction traps (the "gotcha gallery")

Format: 30 snippets, each 3–8 lines, answer and one-line reason on the back. Reported C focus: Qualcomm (pointers, `const` placement, structure vs union, padding, `volatile`, `static`, memory sections), Arista (debugging buggy C: uninitialised variables, returning a pointer to a local array, `x++` passed into recursion, modifying a string literal), Juniper/Cisco OAs (output-based MCQs).

Trap catalogue:
1. `i = i++ + ++i;` → undefined behaviour (unsequenced modifications).
2. `sizeof(i++)` → `i` not incremented (operand not evaluated, except VLAs).
3. `printf("%d", printf("hello"));` → prints `hello5` (printf returns characters printed).
4. `if (-1 < 1u)` → false: `-1` converts to `UINT_MAX`.
5. `char c = 200; printf("%d", c);` → −56 where `char` is signed (implementation-defined).
6. Array parameter decay: `void f(int a[10]) { sizeof(a); }` → size of a pointer (8 on 64-bit).
7. `char *p = "arista"; p[0] = 'A';` → undefined behaviour (string literal), versus `char p[] = "arista";` which is fine.
8. Returning address of a local array → dangling pointer.
9. `#define SQ(x) x*x` then `SQ(2+3)` → 11; fix with `((x)*(x))`; and `SQ(i++)` double-increments.
10. `switch` without `break` → fall-through.
11. Comma operator: `int x = (1, 2, 3);` → 3; `int x = 1, 2;` → compile error.
12. Short-circuit: `if (a && b++)` → `b` unchanged when `a == 0`.
13. `static int count;` inside a function keeps its value across calls; default initialised to 0.
14. `*p++` vs `(*p)++` vs `++*p` (precedence and associativity).
15. `int a[5]; &a + 1` vs `a + 1` (pointer to array vs pointer to element).
16. `const int *p` (pointee const) vs `int *const p` (pointer const) vs `const int *const p`: reported Qualcomm question.
17. Structure padding: `struct { char c; int i; char d; }` → 12 bytes typical; reorder to `int, char, char` → 8; `#pragma pack(1)` / `__attribute__((packed))` trade-offs (misaligned access cost or faults on some architectures).
18. Union size = largest member (plus alignment); writing one member and reading another (type punning) and endianness check:
    ```c
    int is_little_endian(void) {
        union { unsigned int i; unsigned char c[4]; } u = { .i = 1 };
        return u.c[0] == 1;   /* least significant byte stored first */
    }
    ```
19. `volatile`: prevents the compiler caching a value in a register (memory-mapped I/O, signal handlers, variables shared with an ISR); it does **not** make code thread-safe.
20. Integer overflow of signed `int` is undefined; unsigned wraps modulo 2^n.
21. Floating-point equality: `0.1 + 0.2 == 0.3` → false; `float f = 0.1; if (f == 0.1)` → false (double vs float).
22. `printf("%d", 'A')` → 65; `sizeof('A')` → 4 in C (int), 1 in C++.
23. Shift pitfalls: `1 << 31` on 32-bit `int` is undefined; right-shifting negative numbers is implementation-defined; shifting by ≥ width is undefined.
24. `strlen` vs `sizeof` on `char s[] = "abc"` → 3 vs 4.
25. Uninitialised local variable → indeterminate value (Arista debugging question).
26. Missing `free` / double `free` / use after free.
27. `for (unsigned i = n - 1; i >= 0; i--)` → infinite loop.
28. Octal literal: `int x = 010;` → 8.
29. Ternary type promotion and `?:` associativity.
30. `main()` recursion and stack overflow; tail of `printf` with mismatched format specifier (undefined).
31. Memory sections: text (code), data (initialised globals/statics), BSS (zero-initialised globals/statics), heap (`malloc`), stack (locals, return addresses): reported Qualcomm question "what kind of variable is stored where" and effect of `static` on a big array inside a function (moves it from stack to BSS/data; avoids stack overflow; not re-entrant).

Sources: Qualcomm C questions https://www.glassdoor.com/Interview/what-is-volatile-static-how-would-it-affect-if-the-static-keyword-used-for-big-array-inside-a-function-what-are-section-QTN_212927.htm ; https://www.geeksforgeeks.org/interview-experiences/qualcomm-software-engineer-interview-experience-on-campus/ ; https://dataford.io/interview-guides/qualcomm/embedded-engineer ; Arista C debugging reports https://www.glassdoor.co.in/Interview/Arista-Networks-Interview-Questions-E295128.htm

## A4. HR and behavioural hacks

### A4.1 STAR and its cousins

- **STAR**: Situation (2 lines), Task (1 line, your responsibility), Action (60% of airtime; "I", not "we"; 3 concrete steps), Result (numbers, plus what you learnt). Target 90–120 s per story.
- **STAR+L** (add "Learning") for failure stories; **CAR** (Challenge, Action, Result) for a 30-second version.
- Template card (fill-in-the-blanks):
  > "In [semester/internship], our team of [n] was [situation]. I was responsible for [task]. First I [action 1, with a tool/technique], then I [action 2], and when [obstacle] happened I [action 3]. As a result, [metric: latency down 40%, 3 days saved, grade, adoption]. If I did it again, I would [learning]."
- Networking flavour examples for students: building a campus LAN in Packet Tracer/GNS3 and debugging an OSPF adjacency; automating config backups with Python Netmiko; a socket chat server that dropped messages under load (TCP stream framing bug); hackathon outage and how you recovered.

### A4.2 Amazon Leadership Principles story bank

Amazon interviews are built on behavioural questions mapped to its 16 Leadership Principles, answered in STAR. Sources disagree on story count (one per LP vs 8–10 reusable stories); the book recommends **8 core stories, each tagged to 2–4 LPs**, plus 2 spares.

Story bank grid (student fills it in; the book provides a worked example row for each):

| # | Story theme | Primary LPs | Secondary LPs | Typical prompts it answers |
|---|---|---|---|---|
| 1 | Customer impact (helped a user/client) | Customer Obsession | Earn Trust, Deliver Results | "Tell me about a time you went above and beyond for a customer." |
| 2 | Ownership beyond your role | Ownership | Bias for Action | "Time you took on something outside your responsibility." |
| 3 | Deep technical investigation (root-causing a bug or outage) | Dive Deep | Insist on the Highest Standards | "Time you used data to find the root cause." (NDE favourite: network outage RCA) |
| 4 | Failure and recovery | Learn and Be Curious, Earn Trust | Ownership | "Tell me about a time you failed." |
| 5 | Disagreement with a peer/senior | Have Backbone; Disagree and Commit | Earn Trust | "Time you disagreed with your manager/teammate." |
| 6 | Decision under ambiguity or tight deadline | Bias for Action | Are Right, A Lot | "Time you made a decision without full information." |
| 7 | Simplification / automation (scripted a manual process) | Invent and Simplify | Frugality, Deliver Results | "Time you found a simpler way." |
| 8 | Raising the bar / quality | Insist on the Highest Standards | Hire and Develop the Best (mentoring juniors) | "Time you refused to compromise on quality." |
| 9 | Delivering under constraints | Deliver Results, Frugality | Ownership | "Time you delivered with limited resources." |
| 10 | Helping others grow / teamwork | Hire and Develop the Best, Strive to be Earth's Best Employer | Earn Trust | "Time you helped a struggling teammate." |

Also list all 16 LPs on the page with a one-line meaning and the two follow-up probes interviewers use ("What would you do differently?", "What was the data?"). Tips: quantify; keep stories genuine (bar raisers probe with follow-ups); avoid "we"; have a fresh story per round, since interviewers in a loop each own different LPs.

Sources: Amazon in-person interview page https://origin.gamma.amazon.jobs/en-gb/landing_pages/in-person-interview ; Amazon interview guide https://amazonstores.turtl.co/story/interviewing-at-amazon-guide/page/5 ; https://www.interviewquery.com/p/amazon-star-method ; https://prachub.com/resources/amazon-behavioral-interview-questions-for-software-engineers-leadership-principles-star-stories-and-follow-ups ; https://www.amazon.jobs/content/en/our-workplace/leadership-principles

### A4.3 "Tell me about yourself" template (60–90 s, Present–Past–Future)

> "I am [name], a final-year [branch] student at [college]. **Present**: I am focused on networking and systems: I [one strong project in one line, with a number]. **Past**: I got here through [internship / CCNA / research / competitive programming: 1–2 proof points]. **Future / fit**: I am excited about [company]'s [specific product: Catalyst/Meraki, Junos/Mist, Snapdragon connectivity, EOS/CloudVision, AWS backbone, Azure networking, SR Linux], because [link to your skills]. That is why I applied for this role."

Variants: HR round (add one personal trait with evidence), technical round (lead with the project they will ask about), managerial round (lead with impact and teamwork). Companies-to-product map table so students can personalise the "Future" line. "Why Qualcomm?" and "Tell me about yourself" are reported as standard HR questions at Qualcomm.

### A4.4 Resume tips for networking roles

- One page; reverse chronological; PDF; ATS-friendly single column; no photo, no marital status (common in Indian résumés, omit).
- Sections: Education (CGPA if ≥ 7.5) → Skills (grouped: Languages: C, Python; Networking: TCP/IP, OSPF, BGP, VLAN, STP, ACL, NAT; Tools: Wireshark, GNS3/EVE-NG, Packet Tracer, tcpdump, Linux; Automation: Netmiko, NAPALM, Ansible, REST/NETCONF; Cloud: AWS VPC) → Experience/Internships → Projects (3, each with tech stack and a number) → Certifications (CCNA, JNCIA-Junos, AWS Cloud Practitioner/Advanced Networking, Nokia SRA basics) → Achievements (LeetCode/Codeforces ratings, hackathons).
- Bullet formula (XYZ): "Accomplished X, measured by Y, by doing Z." e.g. "Cut lab-network configuration time from 2 h to 5 min by writing a Python/Netmiko script that pushes templated configs to 12 routers."
- Project ideas that score in networking interviews: multi-area OSPF + eBGP lab with route-maps; packet sniffer in C with raw sockets; mini TCP over UDP with sliding window; DHCP or DNS server in Python; SDN controller app (Mininet + Ryu); network monitoring dashboard (SNMP/gNMI → Prometheus/Grafana); VXLAN-EVPN lab on containerlab.
- Everything on the résumé is fair game: be able to whiteboard every keyword for 5 minutes (multiple reports show interviewers drilling into résumé projects: Juniper, Arista, Broadcom).
- Red flags: listing "OSI model" as a skill; percentage skill bars; unverifiable buzzwords; links that 404.

### A4.5 Offer negotiation for Indian offers

- **Read the CTC**: break into fixed base, variable/performance bonus, joining (sign-on) bonus, relocation, RSUs/ESOPs (vesting schedule, e.g. 25/25/25/25 or front-loaded), retention bonus, PF (employer share is counted in CTC), gratuity, insurance, meal cards. Compute **first-year in-hand** and **guaranteed annual cash** separately.
- Red flags: variable > 30% of CTC; one-time joining bonus shown inside "annual CTC"; long joining-bonus clawbacks (often 1–2 years); service bonds; ESOPs in illiquid start-ups counted at face value. A fixed-heavy ₹24 LPA can beat a ₹30 LPA offer with a large variable component.
- **Campus reality**: on-campus offers are usually standardised and non-negotiable on base; placement-cell rules may forbid negotiating or holding multiple offers ("one student, one offer" policies), so read your college's policy first. Off-campus and lateral offers are more negotiable.
- **What can move**: joining bonus, relocation, joining date, location/team, level/title, RSU grant, a written review date. Pick the one or two that matter most, not every line.
- **Script**: thank → state enthusiasm → present a competing offer or market data (levels.fyi, Glassdoor, AmbitionBox, Blind) → ask a specific, reasonable number → pause. Let the company make the first offer; do not reveal current or expected CTC first if avoidable.
- Taxes: new vs old regime one-liner; RSU taxed as perquisite at vest.

Sources: https://www.greatfrontend.com/blog/how-to-evaluate-tech-job-offer-india ; https://www.unboxcareer.com/blog/offer-comparison-framework-indians-2026 ; https://jobrise.io/en/blog/salary-negotiation-kaise-kare/ ; https://www.teamblind.com/post/FLU4sc4c ; https://leetcode.com/discuss/compensation/1090013/microsoft-l64-bangalore

### A4.6 HR question bank (with answer frames)

Why this company? Why networking? Strengths/weaknesses (weakness + mitigation); where in 5 years; relocation and shift flexibility (common for NOC/NDE roles: on-call); handling pressure; biggest achievement; a conflict; why should we hire you; questions to ask the interviewer (team's tech stack, on-call, what success in 6 months looks like); service bond acceptance; higher studies plans (answer honestly but signal commitment).

## A5. Real interview questions by company

Format for the book: one table per company, columns: #, Question, Round/area, Tag ([S]/[T], see section 0), Source, One-line solution sketch, Book chapter link. Each company opens with a 4-line "process at a glance" box. In the book, every [S] item that is a coding problem also appears with a full worked solution in the relevant chapter's "Problems asked in interviews" section (spec in B4).

### A5.1 Cisco

Process: OA (HackerRank, ~40 MCQ + 1–2 coding, networking-heavy) → 2 technical → managerial → HR. Network-engineer drive 2025 added a PPT submission.

| # | Question | Area | Tag | Source | Sketch |
|---|---|---|---|---|---|
| 1 | Explain the OSI model and the function of each layer | CN | [S] | Glassdoor Cisco network engineer reviews https://www.glassdoor.com/Interview/Cisco-Interview-E1425-RVW95762641.htm | 7 layers, PDU, device and protocol per layer; contrast with TCP/IP 4-layer |
| 2 | Which layer does DHCP belong to? | CN | [S] | same Glassdoor set | Application layer over UDP 67/68; explain DORA |
| 3 | How would you troubleshoot a network failure? | Troubleshooting | [S] | same | SCOPE-LAYER-FIX-PROVE (A2.7) |
| 4 | Design a corporate network | Design | [S] | same | Core/distribution/access or spine-leaf, VLANs per department, redundancy (HSRP, EtherChannel), firewall/DMZ, IP plan with VLSM |
| 5 | What is TCP/IP? | CN | [S] | same | 4-layer suite; IP best-effort, TCP reliable stream (handshake, seq/ack, windowing) |
| 6 | Subnetting and CIDR problems | CN | [S] | GfG Cisco network consultant engineer https://www.geeksforgeeks.org/cisco-interview-experience-set-11-network-consultant-engineer/ | Magic-number method (A2.2) |
| 7 | ARP, RARP, DHCP, loopback address | CN | [S] | same | ARP IP→MAC broadcast/unicast; RARP obsolete (MAC→IP), replaced by BOOTP/DHCP; 127.0.0.0/8 |
| 8 | Longest substring without repeating characters | DSA | [S] | Code360 Cisco 2019 campus https://www.naukri.com/code360/interview-experiences/cisco/cisco-interview-experience-on-campus-sep-2019-1318 ; Glassdoor OA | Variable sliding window with last-seen index map, O(n) |
| 9 | Implement an LRU cache | DSA/design | [S] | Code360 2019 campus, Jan 2023 report https://www.naukri.com/code360/interview-experiences/cisco/cisco-interview-experience-on-campus-jan-2023 | Hash map + doubly linked list; O(1) get/put |
| 10 | LFU cache; trie question | DSA | [S] | Jointaro Bengaluru 2025 https://www.jointaro.com/interviews/companies/cisco/experiences/software-developer-bengaluru-august-1-2025-no-offer-positive-f909db9a | LFU: key→(val,freq), freq→ordered list, track minFreq; trie insert/search/startsWith |
| 11 | Trapping rain water | DSA | [T] | Code360 Jan 2022 off-campus https://www.naukri.com/code360/interview-experiences/cisco-systems-pvt-ltd/cisco-interview-experience-off-campus-jan-2022-2 | Two pointers with leftMax/rightMax, O(n) O(1) |
| 12 | Shortest substring containing all characters (minimum window) | DSA | [T] | same | Sliding window with need/have counters |
| 13 | Difference between switch and router; hub | CN | [T] | Cisco question banks https://unstop.com/blog/cisco-interview-questions | L2 MAC table vs L3 routing table; broadcast/collision domains |
| 14 | What happens when you ping a host on another subnet? | CN | [T] | Unstop ARP question set above | ARP for gateway, ICMP echo, routing, TTL; reply path |
| 15 | VLAN and trunking, native VLAN | R&S | [T] | https://copilotinterview.com/blog/network-engineer-interview-questions | 802.1Q tag; access vs trunk; native untagged |
| 16 | Puzzles (campus drive) | Puzzles | [S] | GfG Cisco network engineer 2021 https://www.geeksforgeeks.org/?p=838349 | Keep a 25-puzzle appendix (e.g. 3 bulbs 3 switches, 2 eggs 100 floors, 25 horses) |
| 17 | Project deep-dive and past internship | Résumé | [S] | GfG summer internship 2025 https://geeksforgeeks.org/cisco-interview-experience-off-campus-2025-summer-internship | Be able to draw the architecture and justify every tool |

### A5.2 Juniper Networks

Process: HackerRank OA (32–35 MCQ: CN, OS, DBMS, C output, time complexity + 1–3 coding) → 2 technical → HR (4–5 rounds total).

| # | Question | Area | Tag | Source | Sketch |
|---|---|---|---|---|---|
| 1 | Reverse a linked list | DSA (C) | [S] | https://github.com/sumitsingh4411/interview-rounds/blob/main/content/interviews/juniper-3.md | Iterative prev/curr/next; also recursive |
| 2 | Linked-list question + circular linked-list question | DSA | [S] | Medium SWE intern 2023 https://akash-kumar916.medium.com/juniper-networks-interview-experience-swe-intern-2023-selected-cd9a7868d25 | Insert/delete in circular list; detect circularity with fast/slow |
| 3 | Decimal equivalent of a binary number stored in a linked list | DSA | [S] | GfG Juniper on-campus https://www.geeksforgeeks.org/juniper-networks-interview-experience-on-campus/ | Traverse: `val = val*2 + node->bit` |
| 4 | Merge two sorted arrays | DSA | [S] | same | Two pointers from the end for in-place merge (LC 88) |
| 5 | Detect a loop in a linked list | DSA | [S] | GfG Juniper set 3 https://www.geeksforgeeks.org/juniper-interview-experience-set-3-campus/ | Floyd's cycle detection; find start by resetting one pointer |
| 6 | Quick sort on a linked list | DSA | [S] | same | Partition around head; or prefer merge sort for lists (O(1) extra, stable) |
| 7 | Explain the TCP three-way handshake and TCP segment structure | CN | [S] | GfG Juniper set 4 https://www.geeksforgeeks.org/interview-experiences/juniper-networks-interview-experience-set-4-campus/ | SYN/SYN-ACK/ACK with ISNs; header fields (A2.5) |
| 8 | How do ping and traceroute work? | CN | [S] | same family of reports | ICMP echo; traceroute increments TTL, uses ICMP time exceeded (UDP high ports on Unix, ICMP on Windows) |
| 9 | OSI model, TCP vs UDP, ARP, subnetting, OSPF | CN | [S] | Juniper OA/interview reports https://www.glassdoor.co.in/Interview/Juniper-Networks-Interview-E7224-RVW71834293.htm | Standard answers; OSPF: link-state, Dijkstra, areas, DR/BDR |
| 10 | MAC addressing, IP addressing, routing tables | CN | [S] | same | MAC 48-bit flat, IP hierarchical; longest-prefix match |
| 11 | C output-based MCQs | C | [S] | https://www.geeksforgeeks.org/juniper-networks-interview-experience-3/ | See A3.5 gallery |
| 12 | Time-complexity MCQs | DSA | [S] | LeetCode Dec 2022 intern https://leetcode.com/discuss/post/2936128/juniper-networks-swe-intern6-months-bangalore-dec-2022-offer | Master theorem, nested-loop counting |
| 13 | BGP, OSPF, scripting, switching, troubleshooting (experienced/networking roles) | R&S | [S] | GfG 2.6 yrs experience https://www.geeksforgeeks.org/interview-experiences/juniper-networks-interview-experience-2-6-years-experience/ | Path attributes; OSPF LSAs/areas; Python parsing of `show` output |
| 14 | Project-related questions | Résumé | [S] | Jointaro SE-1 Bengaluru 2022 https://www.jointaro.com/interviews/companies/juniper-networks/experiences/software-engineer-1-bengaluru-karnataka-september-1-2022-accepted-offer-positive-befd747b | Architecture, trade-offs, what you would change |
| 15 | Process vs thread; mutex vs semaphore | OS | [T] | GfG Juniper recruitment process https://www.geeksforgeeks.org/interview-experiences/juniper-networks-recruitment-process/ | Shared address space; binary lock with ownership vs counting signal |
| 16 | Junos vs IOS concepts (commit model, candidate config) | Vendor | [T] | (book addition for Juniper candidates) | Candidate/active config, `commit confirmed`, rollback 0–49 |

### A5.3 Qualcomm

Process: written/online test (aptitude + C + CS fundamentals) → 1–2 technical → HR ("Why Qualcomm?", "Tell me about yourself").

| # | Question | Area | Tag | Source | Sketch |
|---|---|---|---|---|---|
| 1 | Difference between structure and union | C | [S] | GfG Qualcomm on-campus https://www.geeksforgeeks.org/?p=855480 | Separate vs shared storage; size; use cases (variant types, register views) |
| 2 | Structure padding: size of a struct with mixed members; how to avoid it | C | [S] | same; https://www.geeksforgeeks.org/interview-experiences/qualcomm-interview-experience-off-campus-2020/ | Alignment rules; reorder largest-first; `packed` trade-offs |
| 3 | `int const *ptr` vs `int *const ptr` | C | [S] | GfG Qualcomm set 13 https://www.geeksforgeeks.org/qualcomm-interview-experience-set-13-campus/ | Read right to left: pointer to const int vs const pointer to int |
| 4 | What is `volatile`, what is `static`; effect of `static` on a big array inside a function; memory sections | C | [S] | Glassdoor Qualcomm question https://www.glassdoor.com/Interview/what-is-volatile-static-how-would-it-affect-if-the-static-keyword-used-for-big-array-inside-a-function-what-are-section-QTN_212927.htm | See A3.5 items 19 and 31 |
| 5 | Detect big- vs little-endian | C | [S] | GfG Qualcomm SE on-campus https://www.geeksforgeeks.org/interview-experiences/qualcomm-software-engineer-interview-experience-on-campus/ | Union or `char*` cast on `int x = 1`; note interviewer rejected a shift-based approach (shifts are endianness-independent) |
| 6 | Reverse the bits of a number | Bits | [S] | GfG Qualcomm on-campus https://www.geeksforgeeks.org/?p=463420 | Loop 32 times or mask-swap ladder (16, 8, 4, 2, 1) |
| 7 | Reverse a linked list | DSA | [S] | same | Iterative three-pointer |
| 8 | Semaphores, mutex, producer–consumer (with code) | OS | [S] | same | Bounded buffer: `empty`, `full` counting semaphores + mutex |
| 9 | TCP, UDP, OSI layers | CN | [S] | same | Comparison table |
| 10 | Router, switch, hub and other connecting devices; TCP/IP | CN | [S] | GfG Qualcomm pool drive https://www.geeksforgeeks.org/qualcomm-interview-experience-pool-campus-drive/ | Layer of operation, domains, forwarding basis |
| 11 | Paging, virtual memory; mutex vs semaphore vs spinlock | OS | [T] | https://www.techprep.app/blog/qualcomm-interview-process | Page tables, TLB, page faults; spinlock busy-waits (short critical sections, no sleeping) |
| 12 | Single number / XOR problems | Bits | [T] | https://dataford.io/interview-guides/qualcomm/embedded-engineer | XOR of all elements |
| 13 | Set/clear/toggle bit n; count set bits | Bits | [T] | same | Masks; Kernighan's `x &= x-1` |
| 14 | `malloc` vs `calloc`; memory leak | C | [T] | same | `calloc` zero-initialises, two arguments; leaks via lost pointers |
| 15 | Union of `int` and `char`: memory layout | C | [S] | search summary of Qualcomm reports (see A5.3 #2 sources) | Same base address; `char` overlays lowest-address byte |
| 16 | Wireless basics for connectivity teams: Wi-Fi vs cellular, 802.11 MAC (CSMA/CA) | Wireless | [T] | (book addition aligned with Qualcomm connectivity roles) | Hidden node, RTS/CTS, ACKs |

### A5.4 Arista Networks

Process: HackerRank OA in C/C++ (90 min) → 2 technical (CoderPad; C debugging, DSA, networking, Linux) → HR.

| # | Question | Area | Tag | Source | Sketch |
|---|---|---|---|---|---|
| 1 | Store each digit of a very large integer | DSA/C | [S] | GfG Arista intern https://www.geeksforgeeks.org/?p=679670 | Read as string; array/linked list of digits; big-number addition |
| 2 | Count sub-arrays that begin with 3 and end with 6 | DSA | [S] | https://gdpi.hitbullseye.com/arista-networks/arista-networks-interview-questions.php | One pass: keep count of 3s seen; at each 6 add count, O(n) |
| 3 | Zombie vs orphan process | OS | [S] | same | Zombie: exited, parent has not `wait()`ed; orphan: parent died, adopted by init/systemd |
| 4 | Merge two sorted singly linked lists without allocating extra nodes | DSA (C) | [S] | https://ambitionbox.com/interviews/arista-networks-interview-questions?page=2 | Dummy head on stack, re-link nodes |
| 5 | Why does a recursive call loop forever when called with `x++`? | C debugging | [S] | Glassdoor Arista https://www.glassdoor.co.in/Interview/Arista-Networks-Interview-Questions-E295128.htm | Post-increment passes old value; use `x+1` |
| 6 | `char *ptr = "arista";` then modify: what happens? | C | [S] | same | String literal in read-only memory → UB/segfault; use array |
| 7 | Fix buggy C code: uninitialised variable, returning pointer to local array | C debugging | [S] | same (SONiC team report) | Initialise; return heap memory or caller-provided buffer |
| 8 | Sizes of types and struct padding | C | [S] | same | `sizeof` on LP64; alignment |
| 9 | Remove nodes from a singly linked list (by value) | DSA | [S] | same | Pointer-to-pointer technique `Node **pp` |
| 10 | Where are different variables stored in C memory layout? | C | [S] | same | text/data/BSS/heap/stack |
| 11 | Simulate a multi-host topology using Linux network namespaces | Linux | [S] | same | `ip netns add`, veth pairs, bridge, `ip addr`, `ip route`, ping between namespaces |
| 12 | Process vs thread; test-and-set, locks, mutexes | OS | [S] | same | Atomic TAS spinlock; mutex sleeps |
| 13 | What happens when a MAC address is rewritten in a packet? | CN | [S] | same | Per-hop L2 rewrite by routers; L2 switches do not rewrite |
| 14 | DHCP, ARP, Ethernet encapsulation, OSPF neighbour states, packet-flow reasoning | CN | [S] | Medium Arista round 2 https://ruchicodess.medium.com/arista-networks-swe-interview-experience-round-2-system-design-networking-debugging-e6847d3b749e | Walk the packet; A2.1 OSPF states |
| 15 | Why do you want to join Arista? | HR | [S] | GfG Arista set 3 https://www.geeksforgeeks.org/interview-experiences/arista-networks-interview-set-3/ | EOS single-image, SysDB state-driven architecture, cloud networking, CloudVision |
| 16 | OA: 2 medium-to-hard coding questions | DSA | [S] | https://www.glassdoor.ie/Interview/Arista-Networks-Interview-E295128-RVW94102396.htm | Practise NeetCode mediums in C++ |

### A5.5 Amazon (Network Development Engineer)

Process: CV review → phone screen (troubleshooting-heavy) → loop (networking depth, Python automation, LPs; bar raiser).

| # | Question | Area | Tag | Source | Sketch |
|---|---|---|---|---|---|
| 1 | Routing and switching, BGP, TCP/IP, MSS and MTU | CN | [S] | Glassdoor NDE https://www.glassdoor.co.in/Interview/Amazon-Network-Development-Engineer-Interview-Questions-EI_IE6036.0,6_KO7,35.htm | MSS = MTU − 40 (IPv4+TCP); mismatch → PMTUD black hole |
| 2 | Given an iBGP/eBGP topology, manipulate the path; explain attributes | BGP | [S] | same | Local pref outbound, AS-path prepend / MED inbound, weight locally |
| 3 | What is BGP path hunting? | BGP | [S] | same | After a withdrawal, routers try progressively longer stale paths before convergence; MRAI timer, route-flap dampening |
| 4 | OSPF at CCNP depth | OSPF | [S] | Glassdoor NDE (same page) | LSA types, areas, DR/BDR election, SPF, stub/NSSA |
| 5 | Phone screen: all troubleshooting scenarios | Troubleshooting | [S] | Jointaro Sydney 2024 https://www.jointaro.com/interviews/companies/amazon/experiences/network-development-engineer-sydney-january-1-2024-no-offer-neutral-2399baf2/ | A2.7 framework |
| 6 | Python automation questions | Automation | [S] | Glassdoor NDE | Parse `show` output, regex, Netmiko loop over devices, error handling |
| 7 | Advice: basic Python/Ansible knowledge will not suffice | Automation | [S] | same | Practise writing scripts end to end (inventory → connect → parse → report) |
| 8 | Leadership-principle behavioural questions | LP | [S] | same | A4.2 story bank |
| 9 | Scenario questions from previous experience (outages) | LP/troubleshooting | [S] | same | Dive Deep + Ownership story with RCA |
| 10 | Difference between MSS and MTU; issues on mismatch | CN | [T] | https://dataford.io/interview-guides/amazon/network-engineer | Large-packet drops, hanging TLS/SSH; fix MSS clamping, allow ICMP 3/4 |
| 11 | ICMP, ping and traceroute mechanics | CN | [T] | https://interviewstack.io/preparation-guide/amazon/network_engineer/entry | TTL expiry, ICMP types |
| 12 | Linux networking commands for debugging | Linux | [T] | same | `ip`, `ss`, `tcpdump`, `mtr`, `ethtool` |
| 13 | Explain how TCP handles packet loss | CN | [T] | same | Retransmission timeout, fast retransmit, SACK, cwnd reduction |
| 14 | ECMP and hashing; why flows polarise | DC | [T] | (book addition: AWS backbone context) | 5-tuple hashing; polarisation fixed by varying hash seeds |
| 15 | Design a network for a new data-centre pod | Design | [T] | same | Clos/spine-leaf, BGP unnumbered/eBGP per leaf, oversubscription ratio |
| 16 | Coding: string/array manipulation in Python | DSA | [T] | Blind thread https://teamblind.com/post/amazon-network-development-engineer-interview-6kyabufd | Log parsing, counting with dict, sorting |

### A5.6 Google (SWE and network-engineer tracks)

Process: phone screen (1–2 problems) → 3–4 technical + Googleyness & Leadership → team match. Network-engineer track adds networking, troubleshooting, scripting rounds.

| # | Question | Area | Tag | Source | Sketch |
|---|---|---|---|---|---|
| 1 | Explain how a device reaches google.com using the OSI model | CN | [S] | Glassdoor Google network engineer https://www.glassdoor.com/Interview/Google-Network-Engineer-Interview-Questions-EI_IE9079.0,6_KO7,23.htm | A2.6 skeleton |
| 2 | A lot of networking questions then a basic Python question in a Google Doc | CN/Python | [S] | same | Write clean Python without an IDE; practise in plain text |
| 3 | Arrays, sliding window and graph problems (London 2025) | DSA | [S] | same | Patterns 3–4, 16–18 |
| 4 | Graph question: two people meeting on the way to a destination | DSA | [S] | LeetCode L3 2025 https://leetcode.com/discuss/post/6848596/google-l3-sde-ii-interview-experience-5-9ffz2/ | BFS from both sources and destination; minimise sum of distances over meeting node |
| 5 | Counting rectangles formed by lines | DSA | [S] | same | Hash set of points; for each diagonal pair check other two corners, O(n²) |
| 6 | Graph problem where union-find was proposed, BFS preferred | DSA | [S] | Teamblind L3 https://www.teamblind.com/post/google-phone-screen-l3-m1wkhbxc | Connected components; know both |
| 7 | Single BFS graph question in phone screen | DSA | [S] | LeetCode L3 phone screen https://leetcode.com/discuss/interview-question/6326275/Google-L3-Phone-Screen | Level-order BFS with visited set |
| 8 | Binary search: first bad commit | DSA | [S] | LeetCode L5 2025 https://leetcode.com/discuss/post/7610148/google-l5-interview-experience-onsite-ba-mk1z/ | Lower-bound binary search (LC 278) |
| 9 | Binary search over prefix sums inside a tree-like graph problem | DSA | [S] | LeetCode L4 2025 https://leetcode.com/discuss/post/7428246/google-l4-interview-experience-2025-by-a-8nsm/ | Prefix sums along root-to-node path + `bisect` |
| 10 | Googleyness: questions linked to résumé projects | Behavioural | [S] | LeetCode on-campus Dec 2023 https://leetcode.com/discuss/post/4771929/google-on-campus-interview-experience-de-9be3/ | STAR stories on collaboration, ambiguity, feedback |
| 11 | TCP/IP fragmentation in detail; path MTU trace | CN | [S] | Blind Google NE https://www.teamblind.com/post/Google-network-engineer-interview-Pb7LjBGG | DF bit, ICMP 3/4, IPv6 no router fragmentation |
| 12 | Single-area OSPF; BGP transit avoidance | R&S | [S] | same | Filter routes so you do not advertise one provider's routes to another (AS-path `^$` outbound) |
| 13 | Process switching vs fast/CEF switching | R&S | [S] | same | CPU per packet vs cached FIB/adjacency table in data plane |
| 14 | OS, networking, scripting, troubleshooting, behavioural rounds (systems engineer) | Mixed | [S] | Glassdoor Google systems engineer https://www.glassdoor.com/Interview/Google-Systems-Engineer-Interview-Questions-EI_IE9079.0,6_KO7,23.htm | Prepare all five pillars |
| 15 | Two easy LeetCode questions in phone screen; discuss trade-offs before coding | DSA | [S] | Medium Google India https://medium.com/jinal-parikh/google-india-interview-experience-6589600ac4f8 | UMPIRE talk track |
| 16 | Flow control vs congestion control | CN | [T] | reported for Meta network engineer, common at Google https://www.glassdoor.com/Interview/Facebook-Network-Engineer-Interview-Questions-EI_IE40772.0,8_KO9,25.htm | rwnd vs cwnd |

### A5.7 Microsoft

Process: OA (Codility/HackerRank, 2 problems) → 2–3 technical (DSA, sometimes design/pointers) → AA/HR.

| # | Question | Area | Tag | Source | Sketch |
|---|---|---|---|---|---|
| 1 | LRU cache | DSA | [S] | Jointaro SDE Sept 2024 https://www.jointaro.com/interviews/companies/microsoft/experiences/software-development-engineer-sde-bangalore-rural-september-11-2024-no-offer-positive-87c4ba74 | Hash map + DLL |
| 2 | Rat in a maze | DSA | [S] | same | Backtracking on grid, mark visited, collect paths |
| 3 | LRU cache (intern 2025) | DSA | [S] | Jointaro intern March 2025 https://www.jointaro.com/interviews/companies/microsoft/experiences/software-development-engineer-sde-intern-bengaluru-march-24-2025-no-offer-neutral-a1857d66 | as above |
| 4 | OA: 1 greedy + 1 graph, LC medium–hard | DSA | [S] | Jointaro intern Sept 2025 https://www.jointaro.com/interviews/companies/microsoft/experiences/software-development-engineer-sde-intern-bengaluru-september-2-2025-accepted-offer-positive-039cdaca | Greedy with sort; BFS/Dijkstra |
| 5 | OA: binary search medium + DP/graph medium-hard | DSA | [S] | LeetCode SDE2 Hyderabad https://leetcode.com/discuss/post/7541629/ | Binary search on answer; DP over DAG |
| 6 | Two Sum | DSA | [S] | Jointaro new grad 2024 https://www.jointaro.com/interviews/companies/microsoft/experiences/software-engineer-new-grad-india-april-1-2024-no-offer-positive-fc1017bb/ | Hash map complement, O(n) |
| 7 | A pointers question | C | [S] | same | Pointer arithmetic, double pointers |
| 8 | A system design question (new grad) | Design | [S] | same | Scope small: URL shortener / rate limiter; API, data model, scaling |
| 9 | Deep copy of a graph (full code) | DSA | [S] | GfG on-campus 2022 https://www.geeksforgeeks.org/?p=882294 | BFS/DFS with old→new node map (LC 133) |
| 10 | Shortest-path graph problem; design LRU (intern samples) | DSA | [S] | Jointaro intern July 2024 https://www.jointaro.com/interviews/companies/microsoft/experiences/software-developer-intern-bengaluru-july-1-2024-no-offer-positive-b1cb2adb | BFS/Dijkstra |
| 11 | OA with harder DP; two medium DSA in interview | DSA | [S] | Jointaro SWE-2 Hyderabad Oct 2024 https://www.jointaro.com/interviews/companies/microsoft/work-experiences/swe-2-hyderabad-october-21-2024-4-ff01c7de | DP recipe |
| 12 | Three DSA questions straight away | DSA | [S] | GfG internship + FTE 2022–23 https://www.geeksforgeeks.org/microsoft-interview-experience-for-internship-fte-on-campus-2022-23/ | Speed + communication |
| 13 | Azure networking: VNet peering and limits | Cloud | [T] | https://thinkcloudly.com/blog/azure-interview-questions/top-21-azure-networking-interview-questions/ | Non-transitive; no overlapping address spaces |
| 14 | NSG vs Azure Firewall; are NSGs stateful? | Cloud | [T] | https://copilotinterview.com/blog/azure-interview-questions | NSG stateful L3/L4 per subnet/NIC; Firewall managed, L7 FQDN rules |
| 15 | Load Balancer vs Application Gateway vs Front Door vs Traffic Manager | Cloud | [T] | https://intellipaat.com/blog/interview-question/microsoft-azure-interview-questions/ | L4 regional / L7 regional + WAF / L7 global anycast / DNS-based global |
| 16 | Private endpoint vs service endpoint | Cloud | [T] | https://hemasundharamkolla.hashnode.dev/top-azure-networking-interview-questions-and-answers | Private IP in your VNet vs optimised route to public endpoint |

### A5.8 Nokia

Process: AMCAT (aptitude, logical, verbal, 2 coding in C/C++ or Java) → 2–3 technical → HR.

| # | Question | Area | Tag | Source | Sketch |
|---|---|---|---|---|---|
| 1 | String reversal | DSA | [S] | GfG Nokia R&D internship https://www.geeksforgeeks.org/?p=1203448 | Two pointers swap in place |
| 2 | Linked-list implementation in C/C++ | DSA | [S] | same | Struct node, insert/delete/print |
| 3 | Networking scenario on OSI layers and their functions | CN | [S] | same | Map each scenario step to a layer |
| 4 | AMCAT coding: GCD of a set of numbers | DSA | [S] | GfG Nokia reports (search summary) https://www.geeksforgeeks.org/nokia-interview-experience/ | Fold `gcd` over array |
| 5 | AMCAT coding: sort an array and print alternate elements | DSA | [S] | same | `sort`, step 2 |
| 6 | Number of balanced parentheses in a string | DSA | [S] | same | Stack or counter |
| 7 | Two simple array coding questions (AMCAT 2021) | DSA | [S] | GfG Nokia internship 2021 https://www.geeksforgeeks.org/?p=425992 | Array basics |
| 8 | Define a pointer; what does `*` indicate? | C | [S] | GfG Nokia networks https://www.geeksforgeeks.org/nokia-networks-interview-experience/ | Declaration vs dereference |
| 9 | Memory layout of a C program; `malloc` vs `calloc` | C | [S] | same family | A3.5 #31 |
| 10 | Name OSI layers; TCP/IP model; which came first; how they differ | CN | [S] | same family | A2.1 |
| 11 | TCP, UDP, DNS; why IPv6; subnetting | CN | [S] | same family | Address exhaustion, no NAT, SLAAC |
| 12 | Virtual memory | OS | [S] | same family | Paging, demand paging |
| 13 | Virtual function with code; inline functions; copy constructor | OOP | [S] | same family | vtable, runtime polymorphism; deep vs shallow copy |
| 14 | VLAN concepts, routing protocols | R&S | [S] | Glassdoor Nokia https://www.glassdoor.com.au/Interview/Nokia-Interview-E3494-RVW45960465.htm | 802.1Q, OSPF vs RIP |
| 15 | Networking fundamentals, Python basics, C++ | Mixed | [S] | same | Python list/dict comprehension, file parsing |
| 16 | DBMS basics: normalisation, joins | DBMS | [S] | Nokia GET report https://www.geeksforgeeks.org/?p=498036 | 1NF–BCNF, inner vs outer join |
| 17 | 4G/5G basics for Nokia Networks roles (eNodeB/gNodeB, core) | Telecom | [T] | (book addition: Nokia Networks R&D context) https://www.geeksforgeeks.org/nokia-interview-experience-for-networks-rd-engineer-fresher-off-campus/ | RAN vs core; EPC vs 5GC |

### A5.9 Broadcom

Process: 2–3 technical rounds (C-heavy), hiring manager, sometimes a full onsite day.

| # | Question | Area | Tag | Source | Sketch |
|---|---|---|---|---|---|
| 1 | Reverse a linked list | DSA (C) | [S] | Glassdoor Broadcom Bengaluru https://www.glassdoor.co.in/Interview/Broadcom-Interview-Questions-E6926.htm | Three pointers |
| 2 | Bit manipulation questions | Bits | [S] | same | A1.3 card 23 |
| 3 | Pointers, arrays, stacks and queues in C | C/DSA | [S] | same | Implement stack with array; queue with circular buffer |
| 4 | Insert and delete an element in a linked list | DSA | [S] | Glassdoor Broadcom engineering https://www.glassdoor.com/Interview/Broadcom-Engineering-Interview-Questions-EI_IE6926.0,8_KO9,20.htm | Handle head deletion with pointer-to-pointer |
| 5 | How would you test memory bit-cells of a segment using C? | Embedded | [S] | same | March test / walking 1s and 0s with `volatile` pointer; write pattern, read back, inverse pattern |
| 6 | Static vs auto variables | C | [S] | same | Lifetime and storage class |
| 7 | Race conditions | OS | [S] | same | Unsynchronised read-modify-write; fix with mutex/atomics |
| 8 | Process vs thread | OS | [S] | same | |
| 9 | Design an LRU cache | DSA | [S] | Glassdoor Broadcom SE https://static-pc.glassdoor.de/Interview/Broadcom-Software-Engineer-Interview-Questions-EI_IE6926.0,8_KO9,26.htm | |
| 10 | Write a C function to reverse a string | C | [S] | https://www.lockedinai.com/company-details/AVGO | In place with two indices |
| 11 | Count set bits in a 32-bit integer | Bits | [T] | https://dataford.io/interview-guides/broadcom/software-engineer | Kernighan / lookup table / `__builtin_popcount` |
| 12 | Reverse a linked list and find its middle in one traversal | DSA | [T] | same | Fast/slow while reversing first half |
| 13 | Producer–consumer queue | OS | [S] | PracHub intern https://prachub.com/resources/broadcom-software-engineering-intern-interview-2027-c-c-networking-and-firmware | Ring buffer + condition variables |
| 14 | Algorithms, data structures, databases focus | Mixed | [S] | Glassdoor SE pages above | Broad revision |
| 15 | Describe your projects in detail | Résumé | [S] | same | |
| 16 | How does an Ethernet switch learn and forward (MAC learning, flooding, aging)? | Switching | [T] | (book addition aligned with Broadcom switch-silicon teams) | Source-MAC learning, unknown-unicast flood, 300 s ageing; TCAM for ACLs |

### A5.10 Cross-company "top 30 must-solve" list

Derived from the frequencies above (ranked by number of companies reporting): LRU cache (Cisco, Microsoft, Broadcom); reverse linked list (Juniper, Qualcomm, Broadcom); detect loop in linked list; merge two sorted lists; longest substring without repeat; two sum; reverse bits / count bits / endianness; struct padding / union; `const` pointer variants; `volatile`/`static`; producer–consumer; process vs thread; zombie/orphan; OSI + TCP/IP; TCP handshake; ping/traceroute; ARP/DHCP; subnetting; OSPF states; BGP attributes and path selection; MTU/MSS; "what happens when google.com"; troubleshooting scenario; clone graph; rat in a maze; trapping rain water; minimum window substring; first bad version; BFS shortest path; trie.

---

# PART B: END-OF-CHAPTER APPARATUS SPECIFICATION

Every chapter ends with the same ordered set of sections so students build a habit. Order and approximate page budget per chapter (for a 25–35 page chapter):

| Order | Section | Pages | Visual identity |
|---|---|---|---|
| B1 | Chapter summary / short notes | 2–3 | cream background, numbered key-point boxes |
| B2 | One-page revision sheet | 1 | dense, two-column, can be photocopied |
| B3 | Flashcards | 2 (16–24 cards) | cut-out grid, front/back on facing pages |
| B4 | Problems asked in interviews (full worked solutions) | 6–10 | company badges, code in shaded boxes |
| B5 | Graded exercises | 3–4 | difficulty dots ●○○ / ●●○ / ●●● |
| B6 | Answer key and hints | 2–3 | upside-down hints at page foot, answers at chapter end |
| B7 | 15-minute revision page | 1 | timer icon, checkboxes |
| B8 | Spaced-repetition tracker | ½ | calendar strip |
| Book-level | Last-night-before-interview pack, mock OA papers | appendices | see B9, B10 |

## B1. Chapter summary and short notes

Format rules:
- 10–20 numbered "key points", each ≤ 2 lines, written as testable facts ("OSPF uses IP protocol 89 and multicast 224.0.0.5/224.0.0.6"), not vague statements.
- A **concept map** (one diagram) linking the chapter's ideas, e.g. for TCP: handshake → seq/ack → windowing → congestion control → teardown.
- **"Must remember" numbers box**: all constants in the chapter (ports, timers, sizes, AD values, complexities).
- **"Commonly confused" box**: 3–6 pairs with a one-line distinction (flow vs congestion control; MTU vs MSS; mutex vs semaphore; stable vs in-place sort).
- **"Interviewers love to ask" box**: top 5 questions from this chapter with page references to B4.
- **"Connects to" footer**: cross-links to other pillars (e.g. Dijkstra ↔ OSPF).

## B2. One-page revision sheet

- Exactly one page, two columns, 8–9 pt, designed to be photocopied or photographed.
- Contents: definitions in 1 line, the one diagram that matters, formulas/commands/templates, a mini-table of complexities or protocol fields, the top 3 traps.
- For DSA chapters: the pattern template (≤ 15 lines) + recognition cues + 5 anchor problems with LeetCode numbers.
- For networking chapters: packet/header diagram + state machine + 5 `show`/Linux commands with what to look for in output.
- All one-page sheets are reprinted together in the "Cheat Code Atlas" appendix.

## B3. Flashcards

- 16–24 cards per chapter; front = question or cue, back = answer ≤ 30 words + page reference.
- Card types (mix in every chapter): definition, "fill the number" (AD of OSPF?), "spot the bug" (C snippet), "which pattern?" (problem statement → pattern), "order these" (OSPF states), "compare" (TCP vs UDP: 3 differences), "draw" (sketch the TCP header).
- Each card carries a Leitner box marker strip (□1 □2 □3 □4 □5) for the student to tick.
- Provide a printable CSV/Anki deck export (one deck per pillar) as a companion download; card IDs `P<pillar>-C<chapter>-<n>` so errata can reference them.

## B4. "Problems asked in interviews" with full worked solutions

Selection: 5–10 problems per chapter, drawn from Part A5 (company-tagged), always including at least one [S] item, at least one C problem for low-level chapters, and one networking-flavoured problem where relevant.

Fixed layout for every problem (each 1–2 pages):

1. **Header strip**: title; company badges (Cisco / Juniper / …); round type (OA, phone, onsite); difficulty (Easy/Medium/Hard); pattern tag; LeetCode/GfG number if any; source footnote with URL and [S]/[T] tag.
2. **Problem statement**: precise, with constraints and 2 examples (one normal, one edge).
3. **Clarifying questions to ask**: 3–5 bullets with the assumed answers.
4. **Intuition**: 3–6 sentences, how you would think of it, which keyword triggered which pattern.
5. **Approach 1: brute force**: idea + complexity (no code unless short).
6. **Approach 2 (and 3): optimal**: step-by-step algorithm, a small diagram or trace table of the first iterations.
7. **Code**: C++ and Python (C instead of C++ for pointer/bit/embedded problems; Python only for automation problems). Rules: ≤ 40 lines, meaningful names, comments on non-obvious lines, compiles as printed (all code tested in CI before print).
8. **Dry run**: table tracing variables on Example 1.
9. **Complexity**: time and space with one-line justification each.
10. **Edge cases handled**: tick-list referencing A1.5.
11. **Common mistakes**: 3–5 bullets (the bug students actually make, e.g. "using `if` instead of `while` when shrinking the window").
12. **Follow-ups interviewers ask**: 3–5 with a one-line answer each (e.g. LRU: "make it thread-safe" → lock striping / `std::shared_mutex`; "what if capacity is huge" → approximate LRU / CLOCK).
13. **What a strong answer sounds like**: a 4–6 line script of the spoken explanation (ties into A1.7).
14. **Related problems**: 3 LeetCode/GfG numbers for practice.

Conceptual (non-coding) interview questions use a lighter layout: question → 30-second answer → 2-minute answer (with diagram) → follow-ups → common wrong answers.

## B5. Graded exercises

Three tiers, roughly 30 exercises per chapter:
- **Level 1: Warm-up (10)**: recall and direct application: MCQs, fill-in-the-blank, true/false with justification, small subnetting or output-prediction items.
- **Level 2: Interview-level (12)**: standard problems at OA difficulty; short coding tasks; "explain what happens when…"; config interpretation (`show ip ospf neighbor` output → diagnose).
- **Level 3: Challenge (8)**: LeetCode medium–hard, multi-step troubleshooting scenarios, design questions, lab tasks (Packet Tracer/GNS3/containerlab/Linux namespaces), "prove why" questions.
- Each exercise: ID (e.g. `E7.2.05`), difficulty dots, estimated time, pattern/topic tag, company tag where the exercise mirrors a real question.
- Mixed "interleaved" set of 5 exercises from previous chapters at the end of each chapter (interleaving aids retention).

## B6. Answer key

- Level 1: full answers.
- Level 2: answer + 2–4 line explanation; code for coding tasks in the companion repository, with the key solution printed.
- Level 3: hint ladder (Hint 1: pattern; Hint 2: key observation; Hint 3: outline) printed upside down at page foot; full solutions at the end of the chapter or in the companion repository.
- Every answer references the page where the concept is taught.

## B7. 15-minute revision page

A timed checklist the student can run through the morning of an interview:
- **Minutes 0–5**: read the 10 key points (from B1) aloud.
- **Minutes 5–10**: recall test: 10 rapid questions with answers hidden under a fold line; tick if correct.
- **Minutes 10–15**: re-derive one template or diagram from memory (e.g. write the binary-search template, draw the TCP state diagram, compute one subnet), then compare with B2.
- Bottom strip: "If you only remember three things from this chapter…".

## B8. Spaced-repetition schedule

- Default schedule per chapter: review on **Day 1, Day 3, Day 7, Day 14, Day 30** after first study (a fixed 1-3-7-14-30 plan is the common manual baseline; adaptive tools such as Anki are more efficient for long preparation).
- Compressed plan when the interview is under 30 days away: **2–3–5–7** day gaps.
- Leitner integration with flashcards: Box 1 daily, Box 2 every 2 days, Box 3 every 4 days, Box 4 weekly, Box 5 fortnightly; a wrong answer sends the card back to Box 1.
- Each chapter's final page carries a tracker strip: "First studied: __ / D1 □ D3 □ D7 □ D14 □ D30 □".
- Book-level: a 12-week master plan in the front matter that interleaves pillars (e.g. weekdays DSA 90 min + one networking pillar 60 min; Saturday mock OA; Sunday spaced reviews and weak-area log).
- For DSA problems specifically: re-solve from scratch (not re-read) on D3 and D14; mark "solved without hints in < 25 min" to retire.

Sources: https://studycardsai.com/blog/spaced-repetition-schedule-guide ; https://leitnerbox.pages.dev/blog/leitner-box-schedule/ ; https://mindedge.com/learning-theory/the-leitner-system-how-does-it-work/

## B9. Last-night-before-interview pack (book appendix, ~12 pages)

Contents in order:
1. **Logistics checklist**: résumé copies, ID, offer-letter folder, laptop charged, stable internet for virtual rounds, IDE/editor ready, quiet room, water.
2. **Company crib card** (one per company, half page): process at a glance, reported favourite topics (from A5), 3 product names to mention, one "why us" line.
3. **The 25 networking facts** that are asked most (OSI, TCP handshake, ARP, DHCP DORA, subnetting /24–/30, AD values, OSPF states, BGP path selection, STP rules, VLAN/trunk, NAT, MTU/MSS, ports top 15, ICMP types, IPv6 basics).
4. **The 12 DSA templates** in compressed form (sliding window, two pointers, binary search, BFS, DFS, topo sort, DSU, Dijkstra, monotonic stack, heap top-k, backtracking, 1-D DP).
5. **C traps top 15** (from A3.5).
6. **OS top 10**: process vs thread, context switch, deadlock conditions (mutual exclusion, hold and wait, no pre-emption, circular wait), mutex vs semaphore, paging vs segmentation, virtual memory, thrashing, scheduling algorithms, IPC methods, `fork()` output counting.
7. **Behavioural**: your "Tell me about yourself" script, your 8 STAR story titles with the LPs they cover, 3 questions to ask the interviewer.
8. **What-happens-when skeleton** (A2.6) and troubleshooting framework (A2.7) as single diagrams.
9. **Mindset and sleep**: stop studying by 22:30; no new topics; the night is for revision only; morning: 15-minute revision page of your weakest pillar.

## B10. Mock OA papers with solutions (book appendix)

Six full mock papers, each mirroring a reported format, timed, with an answer sheet, solutions and a scoring guide ("score ≥ 70% → you are ready for this company's OA").

| Mock | Mirrors | Structure | Time |
|---|---|---|---|
| M1 | Cisco | 40 MCQ (15 CN, 8 OS, 5 DBMS, 6 C/DSA, 6 aptitude) + 2 coding (one sliding window/string, one hash map/heap) | 90 min |
| M2 | Juniper | 32 MCQ (CN, OS, DBMS, C output, time complexity, aptitude) + 1–3 coding (linked list, arrays) | 90 min |
| M3 | Qualcomm | 50 MCQ in sections: aptitude 15, C 20, OS/architecture 10, CN 5 | 60–75 min |
| M4 | Arista | 4 coding problems in C (one debugging task, one linked list, one bit problem, one array) | 90 min |
| M5 | Nokia (AMCAT style) | English 18, Quant 16, Logical 14 (adaptive-style ordering easy→hard) + 2 coding in C/C++ (GCD, balanced brackets type) | ~100 min |
| M6 | Amazon / Microsoft style coding OA | 2 coding problems (medium + medium-hard: binary search on answer, graph/DP) + short work-style section placeholder | 90 min |

Solution layout for mock papers:
- MCQs: answer letter, 1–2 line justification, and the elimination route (which options are wrong and why).
- Coding: brief B4-style solution (intuition, code, complexity, edge cases, partial-credit brute force).
- A post-mock **error log** template: question ID, topic, mistake type (concept / careless / time / misread), fix, re-attempt date (feeds the spaced-repetition tracker).
- Each mock ends with a "time audit" table: planned vs actual minutes per section.

Sample items to seed each mock (writers expand):
- M1 MCQ: "A host 192.168.10.77/27 sends to 192.168.10.95. This is: (a) unicast in same subnet (b) directed broadcast (c) another subnet (d) invalid." → (b): block 32, subnet .64–.95, .95 is broadcast.
- M1 coding: longest substring without repeating characters; top-k frequent IP addresses from a log.
- M2 MCQ: `int x = 5; printf("%d %d", x++, x);` → undefined/unspecified order of evaluation; the correct option is "undefined behaviour".
- M3 MCQ: `struct { char a; double b; int c; }` size on x86-64 → 24.
- M4 debugging: function returns pointer to local buffer; recursion with `n--`.
- M5 coding: count balanced bracket substrings; GCD of an array.
- M6 coding: minimum capacity to ship packages within D days (LC 1011); network delay time (LC 743).

---

## C. Production notes for writers

- Every cheat-code page must list its sources in a footnote; every company question must keep its URL and [S]/[T] tag through editing.
- All code is compiled and unit-tested (C with `-Wall -Wextra -fsanitize=address,undefined`, C++17, Python 3.11) before typesetting.
- Use British spelling throughout (behaviour, neighbour, optimise, initialise, normalisation, centre) but keep code identifiers, CLI commands and RFC terms as written (e.g. `color` in a CSS snippet, "neighbor" in `show ip ospf neighbor`).
- Indian context: amounts in ₹ and LPA; mention placement-cell rules; sample names diverse.
- Re-verify formats each placement season; add a "Last verified: <month year>" line under each company box.
- Network-access note: geeksforgeeks.org, leetcode.com and naukri.com could not be fetched from the research session; allow them in the session network settings for the verification pass.

## D. Sources used (consolidated)

DSA and approach
- https://leetcode.com/discuss/study-guide/1939806/rule-of-thumb-for-avoiding-tle
- https://leetcode.com/discuss/post/7324952/understanding-time-complexity-the-108-op-qqno/
- https://codeforces.com/blog/entry/21344
- https://qishiclub.github.io/python-for-leetcode/time-complexity-estimation/
- https://seanprashad.com/leetcode-patterns/ and https://github.com/seanprashad/leetcode-patterns
- https://www.designgurus.io/course-play/grokking-the-coding-interview/doc/coding-patterns-a-cheat-sheet
- https://www.educative.io/courses/grokking-coding-interview
- https://leetcode.com/discuss/post/4039411/14-Patterns-to-Ace-Any-Coding-Interview-Question/
- https://interview-prep-3ci.pages.dev/coding-patterns
- https://neetcode.io/roadmap ; https://takeuforward.org/strivers-a2z-dsa-course/strivers-a2z-dsa-course-sheet-2/
- https://www.techinterviewhandbook.org/algorithms/study-cheatsheet/ (mirror: https://git.mashibing.com/msb-public/tech-interview-handbook/src/commit/6131f64e71dc24e7cfd48e0b68bbabd028efea0b/contents/algorithms/study-cheatsheet.md )
- https://www.techinterviewhandbook.org/coding-interview-cheatsheet/
- https://algocademy.com/blog/handling-edge-cases-why-its-critical-to-think-beyond-the-obvious-in-coding-interviews/
- https://levelop.dev/blog/coding-interview-cheat-sheet-edge-cases
- https://guides.codepath.com/compsci/UMPIRE-Interview-Strategy
- https://www.designgurus.io/blog/mastering-the-umpire-interview-strategy-in-coding-a-step-by-step-guide

Networking
- https://community.cisco.com/t5/switching/is-it-possible-to-know-why-would-bgp-prefer-path-over-the-other/m-p/3012915/highlight/true
- https://forums.acilearning.com/topic/3388/aigp-in-bgp-path-selection-350-401-encor
- https://www.noction.com/blog/bgp_bestpath_selection_algorithm
- https://www.safaribooksonline.com/library/view/ccnp-routing-and/9780133149883/ch14lev3sec16.html
- https://docs.manage.security.cisco.com/cdfmc/c_bgp_path_selection.html
- https://www.professormesser.com/network-plus/n10-009/n10-009-video/magic-number-subnetting-n10-009/
- https://oneuptime.com/blog/post/2026-03-20-subnetting-magic-number-method/view
- https://smenode-academy.com/blog/subnetting-practice-questions/
- https://computingforgeeks.com/subnetting-cheat-sheet/
- https://www.pynetlabs.com/bgp-interview-questions-and-answers/
- https://copilotinterview.com/blog/network-engineer-interview-questions
- https://unstop.com/blog/cisco-interview-questions
- https://github.com/alex/what-happens-when

OA formats and aptitude
- https://dev.to/net_programhelp_e160eef28/cisco-hackerrank-online-assessment-2026-real-questions-preparation-guide-4e21
- https://faceprep.in/article/cisco-hiring-process-for-freshers-2026/
- https://www.geeksforgeeks.org/cisco-interview-experience-sde-for-cloud-applications-6-month-internship-fte-on-campus/
- https://www.geeksforgeeks.org/juniper-networks-interview-experience-3/
- https://www.geeksforgeeks.org/interview-experiences/juniper-networks-recruitment-process/
- https://www.geeksforgeeks.org/interview-experiences/arista-networks-recruitment-process/
- https://faceprep.in/article/amcat-test-2026-complete-guide-pattern-and-scoring/ ; https://faceprep.in/article/amcat-syllabus-2026-section-wise-breakdown/
- https://prepinsta.com/amcat/syllabus/ ; https://prepinsta.com/amcat/ ; https://prepinsta.com/mettl/syllabus/
- https://www.careertestprep.com/knowledge/mercer-mettl-assessment
- https://faceprep.in/article/cocubes-test-2026-pattern-sections-and-preparation/
- https://cpt.hitbullseye.com/CoCubes/Co-Cubes-Test-Pattern.php

Behavioural, résumé, negotiation, revision
- https://origin.gamma.amazon.jobs/en-gb/landing_pages/in-person-interview
- https://amazonstores.turtl.co/story/interviewing-at-amazon-guide/page/5
- https://www.amazon.jobs/content/en/our-workplace/leadership-principles
- https://www.interviewquery.com/p/amazon-star-method
- https://prachub.com/resources/amazon-behavioral-interview-questions-for-software-engineers-leadership-principles-star-stories-and-follow-ups
- https://www.greatfrontend.com/blog/how-to-evaluate-tech-job-offer-india
- https://www.unboxcareer.com/blog/offer-comparison-framework-indians-2026
- https://jobrise.io/en/blog/salary-negotiation-kaise-kare/
- https://www.teamblind.com/post/FLU4sc4c
- https://leetcode.com/discuss/compensation/1090013/microsoft-l64-bangalore
- https://studycardsai.com/blog/spaced-repetition-schedule-guide
- https://leitnerbox.pages.dev/blog/leitner-box-schedule/
- https://mindedge.com/learning-theory/the-leitner-system-how-does-it-work/

Company interview reports: all URLs are listed inline in the tables in A5.1–A5.9 (Glassdoor, GeeksforGeeks, Jointaro, Naukri Code360, LeetCode Discuss, Teamblind, Medium, AmbitionBox, hitbullseye, Dataford, techprep.app, InterviewStack, PracHub, LockedInAI, ThinkCloudly, Intellipaat, CoPilot Interview).
