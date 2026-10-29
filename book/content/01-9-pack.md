::: {.p1}
::: pack
## Revision Spread {#rv1}

::: revision
::: top
**Ten facts.** (1) Read the constraints first: *n* ≤ 10^5 means O(*n* log *n*), *n* ≤ 10^3–10^4 means O(*n*²). (2) Say the six steps aloud: understand, examples, brute force, optimise, code, test. (3) Sorted input suggests two pointers or binary search; "contiguous" suggests a window or prefix sums. (4) Mask for prefix *p*: `p ? ~0u << (32-p) : 0`; network is `ip & mask`, broadcast is `net | ~mask`. (5) Delete from a list with `Node **pp`; test `fast` before `fast->next`. (6) A trie reads one bit per level; longest-prefix match keeps the deepest marked node and costs O(32). (7) BFS marks on push; Dijkstra skips stale entries and needs non-negative weights. (8) LRU is a hash map to doubly-linked-list nodes; every list change is mirrored in the map. (9) Token bucket: `tokens = min(B, tokens + r·Δt)`, pass if `tokens ≥ size`; integers and a monotonic clock. (10) Binary search: half-open `[lo, hi)`, `mid = lo + (hi-lo)/2`, never `lo = mid`.

**Three pictures to redraw.** The binary trie with a walk that remembers the deepest mark ([§1.9](#s1-9){.ref}); the pointer-to-pointer delete and the reversal rewiring ([§1.6](#s1-6){.ref}); the LRU map-plus-list diagram ([§1.15](#s1-15){.ref}).
:::

### Constraint to complexity

| Largest *n* | Aim for | Typical tools |
|---|---|---|
| 10–12 | O(*n*!) | permutations, backtracking |
| 20–25 | O(2^*n*) | subsets, bitmask |
| 100 | O(*n*⁴) | small DP |
| 500 | O(*n*³) | Floyd–Warshall |
| 2000–5000 | O(*n*²) | 2-D DP, all pairs |
| 10^5–2×10^5 | O(*n* log *n*) | sort, heap, binary search |
| 10^6 | O(*n*) | windows, prefix sums, hashing |
| 10^9 and up | O(log *n*) or O(1) | binary search on the answer, formula |

A judge performs about 10^8 simple operations per second; in Python step down one row. Values up to 10^9 mean no array indexed by value, and sums of 10^5 such values need 64 bits.

### Keyword to pattern

| If the problem says | Think | See |
|---|---|---|
| sorted; pair or triple with sum | two pointers, binary search | [§1.2](#s1-2){.ref} |
| longest or shortest contiguous … with a condition | variable sliding window | [§1.2](#s1-2){.ref} |
| subarray of size *k* | fixed window | [§1.2](#s1-2){.ref} |
| subarray sum equals *k*, negatives | prefix sums and a map | [§1.2](#s1-2){.ref} |
| seen before, count, group, duplicates | hash set or map | [§1.3](#s1-3){.ref} |
| valid, parse, split IP or MAC | single-scan validator | [§1.4](#s1-4){.ref} |
| mask, flag, single number, power of two | bit tricks | [§1.5](#s1-5){.ref} |
| cycle, middle, *k*-th from end | fast and slow pointers | [§1.6](#s1-6){.ref} |
| reverse, merge, delete in a list | rewire with `prev`, dummy head, `**pp` | [§1.6](#s1-6){.ref} |
| matching, undo, next greater | stack, monotonic stack | [§1.7](#s1-7){.ref} |
| fixed-size FIFO, driver buffer | ring buffer with a count | [§1.7](#s1-7){.ref} |
| window maximum | monotonic deque | [§1.7](#s1-7){.ref} |
| tree depth, path, subtree | DFS, post-order return | [§1.8](#s1-8){.ref} |
| level by level | BFS with a queue | [§1.8](#s1-8){.ref} |
| BST, *k*-th smallest, validate | in-order, interval bounds | [§1.8](#s1-8){.ref} |
| prefix, autocomplete, IP route lookup | trie | [§1.9](#s1-9){.ref} |
| top *k*, median of a stream, merge *k* lists | heap | [§1.10](#s1-10){.ref} |
| fewest hops; grid regions | BFS; flood fill | [§1.11](#s1-11){.ref} |
| cheapest path, non-negative | Dijkstra | [§1.11](#s1-11){.ref} |
| at most *k* edges; negative weights | Bellman–Ford | [§1.11](#s1-11){.ref} |
| prerequisites, order of tasks | topological sort | [§1.11](#s1-11){.ref} |
| loop in a network, components | union–find | [§1.11](#s1-11){.ref} |
| all combinations or permutations | backtracking | [§1.12](#s1-12){.ref} |
| minimise the maximum, "at most *D* days" | binary search on the answer | [§1.13](#s1-13){.ref} |
| overlapping ranges, IP ranges | sort by start, merge | [§1.13](#s1-13){.ref} |
| number of ways, min cost, can reach | dynamic programming | [§1.14](#s1-14){.ref} |
| O(1) get and recency | hash map and doubly linked list | [§1.15](#s1-15){.ref} |
| allow *r* per second with bursts | token bucket | [§1.15](#s1-15){.ref} |
| validate a sequence of protocol events | state table | [§1.16](#s1-16){.ref} |

### Big-O at a glance

| Structure | Access | Search | Insert | Delete |
|---|---|---|---|---|
| array | O(1) | O(*n*) | O(*n*) | O(*n*) |
| dynamic array | O(1) | O(*n*) | O(1) amortised at end | O(*n*) |
| singly linked list | O(*n*) | O(*n*) | O(1) after a known node | O(1) after the predecessor |
| stack, queue, deque, ring | end only | O(*n*) | O(1) | O(1) |
| hash table | – | O(1) avg, O(*n*) worst | O(1) avg | O(1) avg |
| BST balanced / skewed | – | O(log *n*) / O(*n*) | same | same |
| binary heap | min: O(1) | O(*n*) | O(log *n*) | O(log *n*) |
| trie, key length *L* | – | O(*L*) | O(*L*) | O(*L*) |
| union–find | – | O(α(*n*)) | O(α(*n*)) | – |

| Sort | Time (typical) | Worst | Extra space | Stable |
|---|---|---|---|---|
| insertion | O(*n*²), O(*n*) if nearly sorted | O(*n*²) | O(1) | yes |
| merge | O(*n* log *n*) | O(*n* log *n*) | O(*n*) | yes |
| quick | O(*n* log *n*) | O(*n*²) | O(log *n*) | no |
| heap | O(*n* log *n*) | O(*n* log *n*) | O(1) | no |
| counting, radix | O(*n* + *k*) | same | O(*k*) | yes |

C++ `std::sort` is introsort (not stable); `stable_sort` is a merge sort; Python's `sorted` is Timsort (stable).

| Graph algorithm | Time |
|---|---|
| BFS, DFS, topological sort | O(*V* + *E*) |
| Dijkstra with a binary heap | O((*V* + *E*) log *V*) |
| Bellman–Ford | O(*VE*) |
| Floyd–Warshall | O(*V*³) |
| Kruskal; Prim with a heap | O(*E* log *E*); O(*E* log *V*) |

Recurrences: *T*(*n*) = 2*T*(*n*/2) + O(*n*) gives O(*n* log *n*); *T*(*n*) = *T*(*n*/2) + O(1) gives O(log *n*); *T*(*n*) = 2*T*(*n* − 1) + O(1) gives O(2^*n*). Landmarks: log₂ 10^6 ≈ 20, log₂ 10^9 ≈ 30, 2^10 ≈ 10^3, `INT_MAX` ≈ 2.1×10^9, `LLONG_MAX` ≈ 9.2×10^18.

### Edge-case checklist

- **Size:** empty input, one element, two elements, *k* = 0, *k* > *n*.
- **Values:** duplicates, all equal, negatives, zero, `INT_MIN`, `INT_MAX`, overflow of a sum or product, `abs(INT_MIN)`.
- **Order:** sorted, reverse sorted, rotated.
- **Strings:** empty, spaces, case, one character, leading zeros.
- **Lists:** `NULL` head, one node, cycle, operating on the head or the tail.
- **Trees:** `NULL` root, single node, skewed (depth *n*), duplicate keys.
- **Graphs:** disconnected, self-loop, parallel edges, cycle, unreachable target.
- **Intervals:** touching endpoints, nested intervals, ask whether adjacent ranges merge.
- **Binary search:** target below all, above all, absent, at both ends.
- **Networking:** `01.2.3.4`, `256.1.1.1`, a missing octet, /0 and /32, network and broadcast addresses, port 0 and 65535.

### Code skeletons in one line each

- Prefix mask `p ? ~0u << (32-p) : 0`; same subnet `(a & m) == (b & m)`; IP to integer `a << 24 | b << 16 | c << 8 | d`.
- Bit idioms: `x & (x-1)` clears the lowest set bit; `x & -x` isolates it; `x && !(x & (x-1))` tests a power of two; `(x + a - 1) & ~(a - 1)` aligns up.
- List: `Node **pp = &head; while (*pp && (*pp)->val != k) pp = &(*pp)->next;` then `*pp = (*pp)->next`.
- Reverse: save `next`, set `head->next = prev`, advance `prev` and `head`.
- LPM walk: `best = root->hop; for i in 0..31: t = t->c[bit]; if (t && t->hop >= 0) best = t->hop`.
- Dijkstra: heap of (distance, vertex); `if (d > dist[u]) continue;` relax edges.
- Union–find: `find` with path compression; `unite` returns false if already joined.
- LRU: map key to list node; `get` moves the node to the front; `put` evicts the back and erases its map entry.
- Token bucket: refill on demand from a monotonic clock, cap at *B*, pass if the level covers the packet.

### Flashcards

::: flash
| Q | A |
|---|---|
| Complexity of a loop that halves *n*? [§1.1](#s1-1){.ref} | O(log *n*) |
| Why is `vector::push_back` O(1) amortised? | Copies at doublings total less than 2*n* |
| Two Sum in O(*n*)? [§1.1](#s1-1){.ref} | Hash map value to index; look up `target - a[i]`, then insert |
| Variable window: `if` or `while` to shrink? [§1.2](#s1-2){.ref} | `while`, until the window is valid again |
| Seed of the prefix-sum map? [§1.2](#s1-2){.ref} | `{0: 1}`, for subarrays starting at index 0 |
| Why is `m[key]` unsafe for lookup in C++? [§1.3](#s1-3){.ref} | It inserts a default value |
| Why reject `01.2.3.4`? [§1.4](#s1-4){.ref} | Leading zeros are ambiguous (octal) |
| Is `strncpy` safe? [§1.4](#s1-4){.ref} | No: it does not terminate when truncating |
| Hosts in a /27? [§1.5](#s1-5){.ref} | 2^5 − 2 = 30 |
| Why does `x & 1 == 0` fail? [§1.5](#s1-5){.ref} | `==` binds tighter; write `(x & 1) == 0` |
| Why special-case /0 in a mask? | Shifting a 32-bit value by 32 is undefined |
| Popcount by loop? [§1.5](#s1-5){.ref} | `x &= x - 1` until zero |
| Broadcast from network and mask? | `net \| ~mask` |
| Why use `Node **pp` for delete? [§1.6](#s1-6){.ref} | The head needs no special case |
| Floyd: why does resetting to the head find the cycle start? [§1.6](#s1-6){.ref} | *a* = (*k* − 1)*L* + *c*, so both pointers arrive together |
| Order of the loop test in Floyd? | `fast` first, then `fast->next` |
| Ring buffer, full or empty? [§1.7](#s1-7){.ref} | Keep a count (or waste a slot, or use free-running indices) |
| Monotonic stack stores? | Indices, not values |
| BST delete with two children? [§1.8](#s1-8){.ref} | Copy the in-order successor, delete it from the right subtree |
| Why does a sorted insertion hurt a BST? | The tree becomes a chain; operations cost O(*n*) |
| Validate a BST correctly? | Pass open bounds down, or check that in-order is increasing |
| LPM data structure and cost? [§1.9](#s1-9){.ref} | Binary trie, O(32) per lookup, independent of the table size |
| LPM without a trie? | One hash table per length, probe /32 down to /0 |
| Heap array parent and children? [§1.10](#s1-10){.ref} | Parent (*i*−1)/2; children 2*i*+1 and 2*i*+2 |
| Heap for the *k* largest? | A min-heap of size *k* |
| BFS: when to mark visited? [§1.11](#s1-11){.ref} | When pushed |
| Dijkstra stale check? | `if (d > dist[u]) continue;` |
| Dijkstra with a negative edge? | Wrong; use Bellman–Ford |
| Bellman–Ford with a hop limit? | Run *k* rounds, relaxing from a copy |
| OSPF versus RIP, algorithmically? | Dijkstra on the whole graph versus distributed Bellman–Ford |
| Union–find: `unite` returns false means? | The edge closes a loop |
| Topological sort detects a cycle how? | Fewer than *V* vertices are output |
| Backtracking steps? [§1.12](#s1-12){.ref} | Choose, explore, un-choose |
| Binary-search midpoint? [§1.13](#s1-13){.ref} | `lo + (hi - lo) / 2` |
| Binary search on the answer needs? | A monotone yes/no test |
| Merge intervals: sort by? | Start; compare with the last merged end |
| The five DP steps? [§1.14](#s1-14){.ref} | State, recurrence, base, order, answer cell |
| Why is greedy wrong for coins {1,3,4}, amount 6? | Greedy gives 4+1+1; the best is 3+3 |
| Why is LRU O(1)? [§1.15](#s1-15){.ref} | The map finds the node; the node unlinks itself from a doubly linked list |
| Common LRU bug? | Evicting from the list but not the map |
| Token-bucket refill formula? | `tokens = min(B, tokens + r·Δt)` |
| Fixed-window flaw? | Up to twice the limit across a window boundary |
| Table-driven FSM benefit? [§1.16](#s1-16){.ref} | Transitions are data, reviewable and testable |
:::
:::
:::
