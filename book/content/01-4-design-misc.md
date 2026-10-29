::: {.p1}

## [1.12]{.sec}Recursion and backtracking [Should · ■■□]{.tag} {#s1-12}

::: bigidea
Backtracking builds an answer one choice at a time and undoes each choice after exploring it, so a single recursive function enumerates every candidate while the constraints prune the hopeless ones early.
:::

A recursive function needs a *base case* that stops the recursion and a *step* that moves towards it. Backtracking adds a *path* that is extended before the recursive call and restored after it: choose, explore, un-choose. *Recognise:* "all combinations, permutations or subsets", "generate all", "place so that no two conflict", and small limits (*n* ≤ 12 for permutations, *n* ≤ 20 for subsets). The cost is the size of the search tree: 2^*n* for subsets, *n*! for permutations.

```cpp
void subsets(const vector<int>& a, int i, vector<int>& path,
             vector<vector<int>>& out) {
    if (i == (int)a.size()) { out.push_back(path); return; }   // copy
    subsets(a, i + 1, path, out);  // skip a[i]
    path.push_back(a[i]);                                        // choose
    subsets(a, i + 1, path, out);  // explore
    path.pop_back();  // un-choose
}
```

The two classic bugs are forgetting the un-choose step, which leaks choices into sibling branches, and (in Python) appending `path` itself rather than a copy `path[:]`, so that every stored answer changes as the path changes.

::: example
**Restore IP addresses.** Given a string of digits such as `25525511135`, return every way to insert three dots so that the result is a valid IPv4 address (four parts, each 0–255, no leading zeros).

1. The search has four levels. At each level we choose the length of the next part, 1 to 3 digits.
2. A part is rejected if it has a leading zero and length above one, or exceeds 255.
3. After four parts, the answer is valid only if all digits have been consumed.
4. Pruning by these rules leaves very few branches: at most 3^4 = 81 leaves are ever reached.

```cpp
void restore(const string& s, int pos, int parts, string& cur,
             vector<string>& out) {
    if (parts == 4) {
        if (pos == (int)s.size())                    // all digits used
            out.push_back(cur.substr(0, cur.size() - 1));   // drop last '.'
        return;
    }
    size_t keep = cur.size();
    for (int len = 1; len <= 3 && pos + len <= (int)s.size(); ++len) {
        string seg = s.substr(pos, len);
        if ((len > 1 && seg[0] == '0') || stoi(seg) > 255) continue;
        cur += seg + '.';  // choose
        restore(s, pos + len, parts + 1, cur, out);  // explore
        cur.resize(keep);  // un-choose
    }
}
```

| Part lengths tried | Parts | Outcome |
|---|---|---|
| 3, 3, 2, 3 | 255.255.11.135 | all 11 digits used: accepted |
| 3, 3, 3, 2 | 255.255.111.35 | all 11 digits used: accepted |
| 3, 3, 1, ? | 255.255.1.? | the remaining `1135` has four digits, no length 1–3 uses them all: dead end |
| 2, 2, 2, 3 | 25.52.55.111 | four parts built but two digits are left over: rejected |
| 2, 5, ... | `25.5...` then `525` | a part such as `511` exceeds 255 and is skipped |

[Result for `25525511135`: `255.255.11.135` and `255.255.111.35`. Call as `restore(s, 0, 0, cur, out)` with an empty `cur`.]{.result}
:::

::: trap
*Claim:* Python's recursion handles a depth-first search of any size. *Why it is wrong:* CPython allows about 1000 nested calls by default, and a path graph of 10^5 vertices raises `RecursionError`; C overflows its stack in the same way. *Correct statement:* use an explicit stack for deep graphs, or raise the limit only when the depth is known and modest.
:::

## [1.13]{.sec}Sorting, binary search and intervals [Must · ■■□]{.tag} {#s1-13}

::: bigidea
Sorting costs O(*n* log *n*) once and then makes many questions cheap, because order lets us discard half the data at each comparison.
:::

Comparison sorts cannot beat O(*n* log *n*); the table of algorithms is in the Revision Spread ([the Revision Spread](#rv1){.ref}). In C, `qsort` takes a comparator that must return negative, zero or positive, and it must never be written as `return a - b`, which overflows for large values.

```c
int cmp_int(const void *pa, const void *pb) {
    int a = *(const int *)pa, b = *(const int *)pb;
    return (a > b) - (a < b);  /* -1, 0 or 1; no overflow */
}
/* qsort(arr, n, sizeof arr[0], cmp_int); */
```

### Binary search

*Idea.* In a sorted range, compare with the middle element and discard the half that cannot contain the target. We use one canonical form with a half-open range `[lo, hi)`, which finds the first index whose value is not less than *x*, termed the *lower bound*. Every variant (first occurrence, insertion point, first true of a monotone predicate) is this loop.

```cpp
int lowerBound(const vector<int>& a, int x) {   // first a[i] >= x, or n
    int lo = 0, hi = (int)a.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;  // not (lo + hi) / 2: avoids overflow
        if (a[mid] < x) lo = mid + 1; else hi = mid;
    }
    return lo;
}
```

The two classic bugs are the midpoint overflow in `(lo + hi) / 2` for ranges beyond 2^30, and an update such as `lo = mid`, which loops forever when `hi = lo + 1`. The loop runs ⌈log₂ *n*⌉ times.

**Binary search on the answer.** When the answer is a number and a yes/no test "is *x* enough?" is monotone (false up to a threshold, true after it), the same loop searches the range of possible answers. *Recognise:* "minimise the maximum", "smallest capacity such that …", "at most *D* days".

::: example
**Ship packages within D days.** Packages of weights `1..10` must be shipped in order; a ship carries at most its capacity per day. Find the smallest capacity that ships everything in 5 days.

1. The capacity is at least the heaviest package (10) and at most the total (55).
2. For a trial capacity, load greedily and count days: a larger capacity never needs more days, so the test is monotone.
3. Search the range for the first capacity needing at most 5 days.

```cpp
int shipWithinDays(const vector<int>& w, int days) {
    int lo = *max_element(w.begin(), w.end());
    int hi = accumulate(w.begin(), w.end(), 0);  // answer lies in [lo, hi]
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2, need = 1, load = 0;
        for (int x : w) {
            if (load + x > mid) { ++need; load = 0; }  // start the next day
            load += x;
        }
        if (need <= days) hi = mid; else lo = mid + 1;
    }
    return lo;
}
```

| lo | hi | mid | days needed | action |
|---|---|---|---|---|
| 10 | 55 | 32 | 2 | hi = 32 |
| 10 | 32 | 21 | 3 | hi = 21 |
| 10 | 21 | 15 | 5 | hi = 15 |
| 10 | 15 | 12 | 6 | lo = 13 |
| 13 | 15 | 14 | 6 | lo = 15 |

[Result: 15. Time O(*n* log(sum)).]{.result}
:::

### Intervals

*Idea.* Sorting intervals by start brings overlapping ones next to each other, so one pass can merge them: an interval overlaps the last merged interval when its start is at most that interval's end. *Recognise:* "merge", "overlapping", "meeting rooms", "insert interval", IP address ranges (as pairs of 32-bit integers).

```cpp
vector<array<long long, 2>> mergeIntervals(vector<array<long long, 2>> v) {
    sort(v.begin(), v.end());  // by start, then end
    vector<array<long long, 2>> out;
    for (auto& iv : v) {
        if (!out.empty() && iv[0] <= out.back()[1])   // overlaps the last
            out.back()[1] = max(out.back()[1], iv[1]);
        else
            out.push_back(iv);
    }
    return out;
}
```

For `[1,3], [2,6], [8,10], [15,18]`: `[2,6]` starts at 2 ≤ 3 and extends the first interval to `[1,6]`; `[8,10]` starts after 6 and is kept; `[15,18]` is kept. Whether `[1,2]` and `[3,4]` should merge (as integer ranges they are adjacent) or `[1,2]` and `[2,3]` should (they touch) is a question to ask; the code above merges touching intervals but not adjacent ones, and `iv[0] <= out.back()[1] + 1` merges adjacent integer ranges as well. Time O(*n* log *n*) for the sort.

::: check
1. Why does `lo = mid` in a half-open search risk an infinite loop? [^c1-23]
2. After sorting by start, why is it enough to compare with only the last merged interval? [^c1-24]
:::

[^c1-23]: With `hi = lo + 1`, `mid` equals `lo`, so the range never shrinks.
[^c1-24]: Every earlier merged interval ends before the last one starts, so a later interval cannot reach them.

## [1.14]{.sec}Dynamic programming essentials [Should · ■■■]{.tag} {#s1-14}

::: bigidea
Dynamic programming replaces an exponential recursion by a table, because the same subproblems recur and each need be solved only once.
:::

*Recognise:* "number of ways", "minimum or maximum cost", "can we reach", and a choice at each step whose consequences depend only on a small *state*. The routine has five steps: (i) define the state (what `dp[i]` means in words); (ii) write the recurrence relating it to smaller states; (iii) set the base cases; (iv) choose an evaluation order in which dependencies come first; (v) read the answer from the right cell. Space often reduces to the last row or two.

| Family | State | Recurrence (sketch) |
|---|---|---|
| linear | `dp[i]` best for prefix *i* | `dp[i] = f(dp[i-1], dp[i-2])` (stairs, house robber) |
| knapsack / coins | `dp[c]` for capacity or amount *c* | `dp[c] = min(dp[c - coin] + 1)` |
| subsequence | `dp[i][j]` for prefixes of two strings | match: `dp[i-1][j-1] + 1`; else max or min of neighbours (LCS, edit distance) |
| grid | `dp[r][c]` | from the cell above and the cell to the left |
| increasing subsequence | `dp[i]` ending at *i* | `1 + max dp[j]` over smaller `a[j]`, j < i |

::: example
**Coin change.** With coins `{1, 3, 4}`, find the fewest coins that sum to 6, or −1 if impossible.

1. State: `dp[a]` is the fewest coins for amount *a*.
2. Recurrence: `dp[a] = 1 + min over coins c ≤ a of dp[a - c]`.
3. Base: `dp[0] = 0`; unreachable amounts hold a large sentinel.
4. Fill *a* = 1 to 6 in increasing order, since `dp[a]` needs smaller amounts.

```cpp
int coinChange(const vector<int>& coins, int amount) {
    const int INF = 1e9;
    vector<int> dp(amount + 1, INF); dp[0] = 0;
    for (int a = 1; a <= amount; ++a)
        for (int c : coins)
            if (c <= a && dp[a - c] + 1 < dp[a]) dp[a] = dp[a - c] + 1;
    return dp[amount] >= INF ? -1 : dp[amount];
}
```

| a | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| dp[a] | 0 | 1 | 2 | 1 | 1 | 2 | 2 |

[Result: 2 (3 + 3). A greedy choice of the largest coin gives 4 + 1 + 1 = 3 coins, which shows why greedy is unsafe here. Time O(amount × coins), space O(amount).]{.result}
:::

When counting *combinations* (order ignored), the loop over coins is the outer loop; when counting *sequences* (order matters), the loop over amounts is the outer loop. Swapping them changes the answer, and this is the standard knapsack bug. For two-string problems, edit distance and longest common subsequence are solved in the Problem Set with a two-dimensional table.

## [1.15]{.sec}Design-style coding: caches and rate limiters [Must · ■■■]{.tag} {#s1-15}

::: bigidea
Design-style questions combine two structures so that each covers the other's weakness: a hash map gives O(1) lookup, a doubly linked list gives O(1) reordering, and a counter driven by a clock gives rate control without storing history.
:::

### LRU cache

A *least-recently-used* (LRU) cache holds at most *c* entries and, when full, evicts the entry that was used longest ago. Router software uses the idea for ARP and route caches. The interface is `get(key)`, which returns the value or −1 and marks the entry as most recent, and `put(key, value)`, which inserts or updates and evicts if over capacity. Both must be O(1).

No single structure does both jobs: a hash map finds an entry in O(1) but keeps no order, and a list keeps order but finds in O(*n*). Combining them works because the map stores, for each key, the *address of its list node*; and a doubly linked list can unlink a node it has the address of in O(1), since the node knows both neighbours.

@<figure>
<svg viewBox="0 0 470 190" width="508"><defs><marker id="a7" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#1A1D23"/></marker><marker id="a7b" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#3D55A8"/></marker></defs>
<text class="sm" x="20" y="14" text-anchor="start">hash map</text><text class="sm" x="190" y="14" text-anchor="start">doubly linked list: most recent at the head side</text><rect class="box" x="20" y="28" width="60" height="24"/><text class="mono" x="50" y="43" text-anchor="middle">k1 ●</text><rect class="box" x="20" y="66" width="60" height="24"/><text class="mono" x="50" y="81" text-anchor="middle">k2 ●</text><rect class="box" x="20" y="104" width="60" height="24"/><text class="mono" x="50" y="119" text-anchor="middle">k3 ●</text><rect class="fill" x="150" y="66" width="56" height="26"/><text class="sm" x="178" y="83" text-anchor="middle">head</text><rect class="box" x="230" y="66" width="56" height="26"/><text class="mono" x="258" y="83" text-anchor="middle">k3</text><rect class="box" x="310" y="66" width="56" height="26"/><text class="mono" x="338" y="83" text-anchor="middle">k1</text><rect class="box" x="390" y="66" width="56" height="26"/><text class="mono" x="418" y="83" text-anchor="middle">k2</text><rect class="fill" x="460" y="66" width="0" height="0"/><line class="ln" x1="206" y1="75" x2="230" y2="75" marker-end="url(#a7)"/><line class="lg" x1="230" y1="85" x2="206" y2="85" marker-end="url(#a7)"/><line class="ln" x1="286" y1="75" x2="310" y2="75" marker-end="url(#a7)"/><line class="lg" x1="310" y1="85" x2="286" y2="85" marker-end="url(#a7)"/><line class="ln" x1="366" y1="75" x2="390" y2="75" marker-end="url(#a7)"/><line class="lg" x1="390" y1="85" x2="366" y2="85" marker-end="url(#a7)"/><path class="acc" d="M80,40 C120,40 340,50 338,66" marker-end="url(#a7b)"/><path class="acc" d="M80,78 C120,110 380,120 418,92" marker-end="url(#a7b)"/><path class="acc" d="M80,116 C100,130 200,120 258,92" marker-end="url(#a7b)"/><text class="sm" x="20" y="160" text-anchor="start">get(k3) is a hit and already first. get(k2) unlinks k2 and relinks it after head: four pointer writes, O(1).</text><text class="sm" x="20" y="176" text-anchor="start">Eviction removes the node before the tail (here k2 is the least recent). The map entry must be erased too.</text><text class="sm" x="418" y="108" text-anchor="middle">least recent</text>
</svg>
<figcaption><b>Figure 1.12</b> LRU cache: the map finds a node in O(1); the list orders nodes by recency and lets us unlink one in O(1) because the node holds both neighbours.</figcaption>
</figure>

```cpp
class LRU {
    using Item = pair<int, int>;                         // (key, value)
    size_t cap;
    list<Item> items;  // front = most recent
    unordered_map<int, list<Item>::iterator> pos;        // key -> node
public:
    explicit LRU(size_t c) : cap(c) {}
    int get(int k) {
        auto it = pos.find(k);
        if (it == pos.end()) return -1;
        items.splice(items.begin(), items, it->second);   // to front, O(1)
        return it->second->second;
    }
    void put(int k, int v) {
        if (cap == 0) return;
        auto it = pos.find(k);
        if (it != pos.end()) {  // update and refresh
            it->second->second = v;
            items.splice(items.begin(), items, it->second);
            return;
        }
        if (items.size() == cap) {  // evict the least recent
            pos.erase(items.back().first);  // erase from the map as well
            items.pop_back();
        }
        items.emplace_front(k, v);
        pos[k] = items.begin();
    }
};
```

::: example
**Trace of a cache of capacity 2.**

| Operation | List after (front = most recent) | Result |
|---|---|---|
| put(1,1) | [1] | |
| put(2,2) | [2, 1] | |
| get(1) | [1, 2] | 1 |
| put(3,3) | [3, 1] (key 2 evicted) | |
| get(2) | [3, 1] | −1 |
| put(4,4) | [4, 3] (key 1 evicted) | |
| get(1) | [4, 3] | −1 |
| get(3) | [3, 4] | 3 |
| get(4) | [4, 3] | 4 |

[Result: every operation is O(1) on average: one hash lookup and at most four pointer writes.]{.result}
:::

::: trap
*Claim:* on eviction it is enough to remove the least recent node from the list. *Why it is wrong:* the map still holds a pointer to the freed node, so a later `get` of that key reads freed memory or reports a stale hit. *Correct statement:* every list change must be mirrored in the map: erase the key on eviction, and re-point it on insertion.
:::

*Variants.* With a time-to-live (an ARP entry expires after a fixed time), store an expiry time in each node and treat an expired entry as a miss on `get`; entries expire lazily, or a sweep removes them from the tail end. For thread safety, a single mutex around `get` and `put` is correct because even `get` modifies the list; sharding the cache by key hash across several mutexes reduces contention. LFU (least frequently used) needs a second ordering and is solved in the Problem Set.

### Token-bucket rate limiter

A *token bucket* limits the average rate to *r* tokens per second while allowing bursts of at most *B* tokens. The bucket holds up to *B* tokens, and tokens arrive at *r* per second. A packet of size *s* may pass if the bucket holds at least *s* tokens, which it then removes; otherwise the packet is dropped (policing) or delayed (shaping). In router terms, *r* is the committed information rate and *B* the committed burst size.

@<figure>
<svg viewBox="0 0 440 180" width="475"><defs><marker id="a8" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#1A1D23"/></marker></defs>
<path class="box" style="fill:none" d="M180,40 L180,130 L260,130 L260,40" /><rect class="hl" x="181" y="85" width="78" height="44"/><line class="dash lg" x1="170" y1="40" x2="270" y2="40"/><text class="sm" x="278" y="44" text-anchor="start">capacity B (burst)</text><text class="lbl" x="220" y="112" text-anchor="middle">tokens</text><line class="ln" x1="220" y1="6" x2="220" y2="38" marker-end="url(#a8)"/><text class="sm" x="230" y="20" text-anchor="start">refill: r tokens per second</text><line class="ln" x1="30" y1="150" x2="170" y2="150" marker-end="url(#a8)"/><text class="sm" x="100" y="143" text-anchor="middle">packet of size s</text><line class="ln" x1="270" y1="150" x2="400" y2="150" marker-end="url(#a8)"/><text class="sm" x="335" y="143" text-anchor="middle">pass if tokens ≥ s</text><text class="sm" x="220" y="170" text-anchor="middle">else drop (or delay)</text><text class="sm" x="10" y="70" text-anchor="start">on each packet:</text><text class="mono" x="10" y="83" text-anchor="start">tokens = min(B, tokens + r·Δt)</text><text class="mono" x="10" y="96" text-anchor="start">pass: tokens −= s</text>
</svg>
<figcaption><b>Figure 1.13</b> A token bucket. The long-run rate is r and the largest burst is B, because the level can never exceed the capacity.</figcaption>
</figure>

We do not run a timer. Instead, on each packet we compute how many tokens would have arrived since the last update, add them, and cap the total at *B*. The state is only the current level and the last timestamp. Two details matter. First, time must come from a monotonic clock, because wall-clock time can jump backwards. Secondly, floating-point accumulation drifts, so we use integers: the level is stored in *micro-tokens* (tokens × 10^6), and with a clock in microseconds the refill over Δt µs is exactly `r × Δt` micro-tokens.

```c
#include <stdint.h>
#include <stdbool.h>

typedef struct {
    uint64_t rate;       /* tokens (bytes) per second            */
    uint64_t burst;      /* capacity B in tokens                 */
    uint64_t level;      /* current level, in micro-tokens       */
    uint64_t last_us;    /* timestamp of the last update (µs)    */
} Bucket;

void tb_init(Bucket *b, uint64_t rate, uint64_t burst, uint64_t now_us) {
    b->rate = rate; b->burst = burst;
    b->level = burst * 1000000ull;                 /* start full */
    b->last_us = now_us;
}
bool tb_allow(Bucket *b, uint64_t size, uint64_t now_us) {
    uint64_t cap = b->burst * 1000000ull;
    uint64_t dt = now_us - b->last_us;  /* monotonic: never negative */
    b->last_us = now_us;
    if (b->rate && dt > cap / b->rate)  /* long idle: bucket is full, and */
        b->level = cap;  /* r*dt could overflow otherwise   */
    else {
        b->level += b->rate * dt;
        if (b->level > cap) b->level = cap;
    }
    uint64_t need = size * 1000000ull;
    if (b->level < need) return false;  /* not enough tokens: drop */
    b->level -= need;
    return true;
}
```

::: example
**Rate 1000 bytes per second, burst 1500 bytes.** The bucket starts full (1500 tokens).

| Time (s) | Packet (bytes) | Tokens before | Decision | Tokens after |
|---|---|---|---|---|
| 0.0 | 1500 | 1500 | pass | 0 |
| 0.5 | 600 | 500 | drop (500 < 600) | 500 |
| 0.7 | 600 | 700 | pass | 100 |
| 2.7 | 1500 | 1500 (capped; 2100 earned) | pass | 0 |

[Result: the long-run rate is 1000 bytes per second and no burst exceeds 1500 bytes. Note that the dropped packet still advances the timestamp, so its interval is not credited twice.]{.result}
:::

| Scheme | Memory | Behaviour at the boundary | Use |
|---|---|---|---|
| fixed window counter | one counter | up to 2× the limit across a window edge | simplest; coarse |
| sliding window log | one timestamp per request | exact | strict limits, small limits |
| token bucket | two numbers | bursts up to *B*, exact average | traffic policing, API limits |
| leaky bucket | queue and a drain rate | smooth output, no bursts | traffic shaping |

A fixed-window counter of five requests per ten seconds accepts five requests at second 9 and five more at second 11, ten in two seconds. A sliding log and a token bucket reject the excess; both are asked as follow-ups in the Problem Set.

::: lens
[MICROSOFT · AMAZON · CISCO · JUNIPER]{.co}

For the LRU cache the expected sequence is: hash map plus doubly linked list, the O(1) argument, code, then TTL and thread safety. For the rate limiter, interviewers listen for "token bucket", the two parameters, refill-on-demand rather than a timer thread, the monotonic clock and the integer arithmetic. A strong answer also names the concurrency model and what happens at the boundary.
:::

## [1.16]{.sec}Finite-state machines [Should · ■■□]{.tag} {#s1-16}

::: bigidea
A finite-state machine replaces tangled conditionals by a table that gives the next state for every state and event, so the protocol logic can be read, checked and extended as data.
:::

A *finite-state machine* (FSM) has a set of states, a set of events (or input symbols), a start state and a transition function from (state, event) to the next state; an event with no entry is illegal. Protocols such as TCP, link-state adjacency formation and DHCP are specified this way, and Juniper and Broadcom interviews ask for one in C. *Recognise:* "validate a sequence of events", "parse a protocol", "valid number" (a number grammar is an FSM over characters).

@<figure>
<svg viewBox="0 0 480 126" width="518"><defs><marker id="a9" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#1A1D23"/></marker></defs>
<rect class="box" x="20" y="40" width="56" height="28" rx="14"/><text class="lbl" x="48" y="58" text-anchor="middle">CLOSED</text><rect class="box" x="120" y="40" width="56" height="28" rx="14"/><text class="lbl" x="148" y="58" text-anchor="middle">SYN&#95;SENT</text><rect class="box" x="220" y="40" width="56" height="28" rx="14"/><text class="lbl" x="248" y="58" text-anchor="middle">ESTAB</text><rect class="box" x="320" y="40" width="56" height="28" rx="14"/><text class="lbl" x="348" y="58" text-anchor="middle">FIN&#95;WAIT</text><rect class="box" x="420" y="40" width="56" height="28" rx="14"/><text class="lbl" x="448" y="58" text-anchor="middle">CLOSED</text><line class="ln" x1="76" y1="54" x2="120" y2="54" marker-end="url(#a9)"/><text class="sm" x="98.0" y="36" text-anchor="middle">send SYN</text><text class="sm" x="98.0" y="82" text-anchor="middle"></text><line class="ln" x1="176" y1="54" x2="220" y2="54" marker-end="url(#a9)"/><text class="sm" x="198.0" y="36" text-anchor="middle">rcv SYN+ACK /</text><text class="sm" x="198.0" y="82" text-anchor="middle">send ACK</text><line class="ln" x1="276" y1="54" x2="320" y2="54" marker-end="url(#a9)"/><text class="sm" x="298.0" y="36" text-anchor="middle">send FIN</text><text class="sm" x="298.0" y="82" text-anchor="middle"></text><line class="ln" x1="376" y1="54" x2="420" y2="54" marker-end="url(#a9)"/><text class="sm" x="398.0" y="36" text-anchor="middle">rcv ACK+FIN /</text><text class="sm" x="398.0" y="82" text-anchor="middle">send ACK</text><path class="acc dash" d="M248,68 Q248,110 48,68" /><text class="sm" x="150" y="112" text-anchor="middle">illegal event in any state: report error and keep state</text>
</svg>
<figcaption><b>Figure 1.14</b> A reduced connection state machine (handshake and teardown only). A table indexed by state and event replaces nested conditionals.</figcaption>
</figure>

A two-dimensional array indexed by state and event is the compact form. Entries of −1 mark illegal transitions; the driver loop reads the table and stops at the first illegal event.

```c
#include <stddef.h>
#include <stdint.h>

typedef enum { CLOSED, SYN_SENT, ESTAB, FIN_WAIT, NSTATES } State;
typedef enum { E_SEND_SYN, E_RCV_SYNACK, E_SEND_FIN, E_RCV_FINACK,
               NEVENTS } Event;

static const int8_t next_state[NSTATES][NEVENTS] = {
    /* CLOSED   */ { SYN_SENT, -1,    -1,       -1     },
    /* SYN_SENT */ { -1,       ESTAB, -1,       -1     },
    /* ESTAB    */ { -1,       -1,    FIN_WAIT, -1     },
    /* FIN_WAIT */ { -1,       -1,    -1,       CLOSED },
};

/* Final state, or -1 if event *bad is illegal. */
int run_fsm(const Event *ev, size_t n, size_t *bad) {
    State s = CLOSED;
    for (size_t i = 0; i < n; i++) {
        int t = (ev[i] < NEVENTS) ? next_state[s][ev[i]] : -1;
        if (t < 0) { *bad = i; return -1; }
        s = (State)t;
    }
    return s;
}
```

For the events (send SYN, receive SYN+ACK, send FIN) the machine moves CLOSED → SYN_SENT → ESTAB → FIN_WAIT and returns FIN_WAIT. For (send SYN, send FIN) the second event is illegal in SYN_SENT, so the function returns −1 with `*bad = 1`. When actions must accompany transitions, the table cells hold function pointers instead of states, which is how production protocol code is written. Table size is *states* × *events*, so the transition lookup is O(1).

::: check
1. Why is a table preferable to nested `switch` statements for a protocol with 11 states? [^c1-25]
2. How does an FSM relate to "valid number"? [^c1-26]
:::

[^c1-25]: The table is data, so the full set of transitions can be reviewed at a glance and tested exhaustively; nested switches hide missing cases.
[^c1-26]: States record how much of a number has been read (sign, digits, point, exponent), and each character class is an event.

## [1.17]{.sec}Testing your own code and interview performance [Must · ■□□]{.tag} {#s1-17}

::: bigidea
Code that has been traced by hand on one normal case and three edge cases is usually correct, and showing that trace is itself what the interviewer is assessing.
:::

Before declaring a solution finished, one performs four checks in order. (i) *Dry-run*: execute the code on the worked example, line by line, keeping a small table of variable values, exactly as this chapter's tables do. (ii) *Edge cases*: run the list in the Revision Spread ([the Revision Spread](#rv1){.ref}): empty input, one element, duplicates, extremes of the value range, and for networking input the "/0", "/32", leading-zero and 256 cases. (iii) *Complexity*: state time and space, and justify them by pointing to the loop or the recursion. (iv) *Cross-check*: if time remains, compare against the brute force on small inputs.

In C, a tiny harness costs a minute and catches most mistakes:

```c
#include <stdio.h>
static int fails;
#define CHECK(c) do { if (!(c)) { fails++; \
    printf("FAIL line %d: %s\n", __LINE__, #c); } } while (0)

int main(void) {
    uint32_t a;
    CHECK(parse_ipv4("10.0.0.1", &a) && a == 0x0A000001u);
    CHECK(!parse_ipv4("01.0.0.1", &a));
    CHECK(mask_of(0) == 0 && mask_of(32) == 0xFFFFFFFFu);
    printf(fails ? "%d failures\n" : "all passed\n", fails);
    return fails != 0;
}
```

| Symptom | Likely cause | Where to look |
|---|---|---|
| crash on empty input | missing null or length guard | first lines of the function |
| off by one in the last element | `<` against `<=`, or a window not evicted | loop bounds, eviction index |
| works on small input, times out on large | hidden O(*n*) inside a loop (`strlen`, list `size`, `erase` at front) | the loop body |
| wrong answer only with duplicates | strict versus non-strict comparison | comparisons and the map update |
| garbage or a crash after `free` | use after free, or a stale pointer in a second structure | the deletion path |
| sign or overflow surprises | `int` where `long long` or unsigned is needed | sums, shifts, products |

**Communication.** A round is scored on four things: the correctness of the code, the choice of algorithm, the testing, and the communication. The following habits cost nothing. State the brute force first and its cost, then the improvement and why it is valid. Name the invariant of each loop in a comment. When stuck, say what repeated work you are trying to remove. When given a hint, adopt it openly. Never code silently for more than two minutes, and never claim a complexity without pointing at the loop that produces it.

| Minute (45-min round) | Step |
|---|---|
| 0–5 | restate, ask about size, duplicates, negatives, empty input; work one example |
| 5–15 | brute force, optimisation, and agreement on the plan |
| 15–32 | write code in small named pieces, narrating intent |
| 32–38 | dry-run and edge cases |
| 38–45 | complexity, trade-offs and follow-ups |

::: check
1. What are the first two edge cases to try on a linked-list function? [^c1-27]
2. Why state the brute force before the optimised method? [^c1-28]
:::

[^c1-27]: The empty list and the one-node list, followed by operating on the head and the tail.
[^c1-28]: It shows the problem is understood, gives a correct fallback, and makes the source of the improvement explicit.

:::
