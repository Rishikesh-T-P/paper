::: {.p1}

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

**Top-down and bottom-up.** The recurrence can be evaluated in two ways: *top-down*, as the recursive function with a memo table that stores each result on first computation (the `fib` of [§1.1](#s1-1){.ref}); or *bottom-up*, by filling a table in an order that respects the dependencies, as `coinChange` does. The results are the same; bottom-up avoids recursion depth and allows the space to be trimmed, while top-down is quicker to write when the order of evaluation is awkward.

**The 0/1 knapsack.** Given items with weights `w[i]` and values `v[i]` and a capacity *W*, choose items, each at most once, to maximise the total value. Let `dp[c]` be the best value achievable within capacity *c*. Processing the items one at a time, `dp[c] = max(dp[c], dp[c - w] + v)`. The loop over *c* must run *downwards*: it then reads `dp[c - w]` from before the current item was considered, so each item is used once. A loop running upwards would read a value that already includes the item, which is the unbounded knapsack and the coin-change case.

```cpp
int knapsack(const vector<int>& w, const vector<int>& v, int W) {
    vector<int> dp(W + 1, 0);
    for (size_t i = 0; i < w.size(); ++i)
        for (int c = W; c >= w[i]; --c)  // downwards: each item once
            dp[c] = max(dp[c], dp[c - w[i]] + v[i]);
    return dp[W];
}
```

| After item (w, v) | dp[0..7] |
|---|---|
| none | 0 0 0 0 0 0 0 0 |
| (1, 1) | 0 1 1 1 1 1 1 1 |
| (3, 4) | 0 1 1 4 5 5 5 5 |
| (4, 5) | 0 1 1 4 5 6 6 9 |
| (5, 7) | 0 1 1 4 5 7 8 9 |

[For capacity 7 the best value is 9, from the items of weight 3 and 4. Time O(*nW*), space O(*W*).]{.result}

**Two strings.** For the longest common subsequence of strings *s* and *t*, let `d[i][j]` be the answer for their first *i* and *j* characters. Matching last characters extend the diagonal answer by one; otherwise the answer is the larger of dropping a character from either string.

```cpp
int lcs(const string& s, const string& t) {
    int n = s.size(), m = t.size();
    vector<vector<int>> d(n + 1, vector<int>(m + 1, 0));
    for (int i = 1; i <= n; ++i)
        for (int j = 1; j <= m; ++j)
            d[i][j] = s[i-1] == t[j-1] ? d[i-1][j-1] + 1
                                       : max(d[i-1][j], d[i][j-1]);
    return d[n][m];
}
```

| | (empty) | A | C | B | D |
|---|---|---|---|---|---|
| (empty) | 0 | 0 | 0 | 0 | 0 |
| A | 0 | 1 | 1 | 1 | 1 |
| B | 0 | 1 | 1 | 2 | 2 |
| C | 0 | 1 | 2 | 2 | 2 |
| D | 0 | 1 | 2 | 2 | 3 |

[For `ABCD` and `ACBD` the table ends in 3 (for example `ABD`). Time and space O(*nm*). The edit-distance table of the Problem Set has the same shape.]{.result}

When counting *combinations* (order ignored), the loop over coins is the outer loop; when counting *sequences* (order matters), the loop over amounts is the outer loop. Swapping them changes the answer, and this is the standard knapsack bug. For two-string problems, edit distance and longest common subsequence are solved in the Problem Set with a two-dimensional table.

## [1.15]{.sec}Design-style coding: caches and rate limiters [Must · ■■■]{.tag} {#s1-15}

::: bigidea
Design-style questions combine two structures so that each covers the other's weakness: a hash map gives O(1) lookup, a doubly linked list gives O(1) reordering, and a counter driven by a clock gives rate control without storing history.
:::

### LRU cache

A *least-recently-used* (LRU) cache holds at most *c* entries and, when full, evicts the entry that was used longest ago. Router software uses the idea for ARP and route caches. The interface is `get(key)`, which returns the value or −1 and marks the entry as most recent, and `put(key, value)`, which inserts or updates and evicts if over capacity. Both must be O(1).

No single structure does both jobs: a hash map finds an entry in O(1) but keeps no order, and a list keeps order but finds in O(*n*). Combining them works because the map stores, for each key, the *address of its list node*; and a doubly linked list can unlink a node it has the address of in O(1), since the node knows both neighbours.

<figure>
<svg viewBox="0 0 470 190" width="508"><defs><marker id="a7" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#1A1D23"/></marker><marker id="a7b" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#3D55A8"/></marker></defs>
<text class="sm" x="20" y="14" text-anchor="start">hash map</text><text class="sm" x="190" y="14" text-anchor="start">doubly linked list: most recent at the head side</text><rect class="box" x="20" y="28" width="60" height="24"/><text class="mono" x="50" y="43" text-anchor="middle">k1 ●</text><rect class="box" x="20" y="66" width="60" height="24"/><text class="mono" x="50" y="81" text-anchor="middle">k2 ●</text><rect class="box" x="20" y="104" width="60" height="24"/><text class="mono" x="50" y="119" text-anchor="middle">k3 ●</text><rect class="fill" x="150" y="66" width="56" height="26"/><text class="sm" x="178" y="83" text-anchor="middle">head</text><rect class="box" x="230" y="66" width="56" height="26"/><text class="mono" x="258" y="83" text-anchor="middle">k3</text><rect class="box" x="310" y="66" width="56" height="26"/><text class="mono" x="338" y="83" text-anchor="middle">k1</text><rect class="box" x="390" y="66" width="56" height="26"/><text class="mono" x="418" y="83" text-anchor="middle">k2</text><rect class="fill" x="460" y="66" width="0" height="0"/><line class="ln" x1="206" y1="75" x2="230" y2="75" marker-end="url(#a7)"/><line class="lg" x1="230" y1="85" x2="206" y2="85" marker-end="url(#a7)"/><line class="ln" x1="286" y1="75" x2="310" y2="75" marker-end="url(#a7)"/><line class="lg" x1="310" y1="85" x2="286" y2="85" marker-end="url(#a7)"/><line class="ln" x1="366" y1="75" x2="390" y2="75" marker-end="url(#a7)"/><line class="lg" x1="390" y1="85" x2="366" y2="85" marker-end="url(#a7)"/><path class="acc" d="M80,40 C120,40 340,50 338,66" marker-end="url(#a7b)"/><path class="acc" d="M80,78 C120,110 380,120 418,92" marker-end="url(#a7b)"/><path class="acc" d="M80,116 C100,130 200,120 258,92" marker-end="url(#a7b)"/><text class="sm" x="20" y="160" text-anchor="start">get(k3) is a hit and already first. get(k2) unlinks k2 and relinks it after head: four pointer writes, O(1).</text><text class="sm" x="20" y="176" text-anchor="start">Eviction removes the node before the tail (here k2 is the least recent). The map entry must be erased too.</text><text class="sm" x="418" y="108" text-anchor="middle">least recent</text>
</svg>
<figcaption><b>Figure 1.19</b> LRU cache: the map finds a node in O(1); the list orders nodes by recency and lets us unlink one in O(1) because the node holds both neighbours.</figcaption>
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

<figure>
<svg viewBox="0 0 440 180" width="475"><defs><marker id="a8" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#1A1D23"/></marker></defs>
<path class="box" style="fill:none" d="M180,40 L180,130 L260,130 L260,40" /><rect class="hl" x="181" y="85" width="78" height="44"/><line class="dash lg" x1="170" y1="40" x2="270" y2="40"/><text class="sm" x="278" y="44" text-anchor="start">capacity B (burst)</text><text class="lbl" x="220" y="112" text-anchor="middle">tokens</text><line class="ln" x1="220" y1="6" x2="220" y2="38" marker-end="url(#a8)"/><text class="sm" x="230" y="20" text-anchor="start">refill: r tokens per second</text><line class="ln" x1="30" y1="150" x2="170" y2="150" marker-end="url(#a8)"/><text class="sm" x="100" y="143" text-anchor="middle">packet of size s</text><line class="ln" x1="270" y1="150" x2="400" y2="150" marker-end="url(#a8)"/><text class="sm" x="335" y="143" text-anchor="middle">pass if tokens ≥ s</text><text class="sm" x="220" y="170" text-anchor="middle">else drop (or delay)</text><text class="sm" x="10" y="70" text-anchor="start">on each packet:</text><text class="mono" x="10" y="83" text-anchor="start">tokens = min(B, tokens + r·Δt)</text><text class="mono" x="10" y="96" text-anchor="start">pass: tokens −= s</text>
</svg>
<figcaption><b>Figure 1.20</b> A token bucket. The long-run rate is r and the largest burst is B, because the level can never exceed the capacity.</figcaption>
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

A token bucket with equal-sized packets can be run with a single stored time instead of a level. The *generic cell rate algorithm* keeps the theoretical arrival time `tat` of the next conforming packet: a packet is accepted if it is not earlier than `tat` by more than the burst allowance `burst_us`, and each accepted packet pushes `tat` forward by one packet interval.

```c
bool gcra_allow(uint64_t *tat, uint64_t now,
                uint64_t interval, uint64_t burst) {
    uint64_t t = *tat > now ? *tat : now;      /* never in the past */
    if (t > now + burst) return false;         /* too early */
    *tat = t + interval;
    return true;
}
```

With `interval` = 1000 µs (1000 packets per second) and `burst` = 2000 µs, four packets arriving at time 0 give `tat` = 1000, 2000, 3000 and then a refusal: the first packet is on time, and the burst allowance admits two more, so three back-to-back packets pass, which is 1 + `burst`/`interval`. One 64-bit variable replaces the level and the timestamp, and no multiplication by the packet size is needed; for variable-size packets the interval becomes size / rate.

A fixed-window counter of five requests per ten seconds accepts five requests at second 9 and five more at second 11, ten in two seconds. A sliding log and a token bucket reject the excess; both are asked as follow-ups in the Problem Set.

::: lab
`LAB 1.15 · 10 MIN` Test the token bucket on the trace of the worked example. Save the `Bucket` code of this section together with this driver as `tb.c`, and compile with the sanitisers on, which catch overflow and invalid shifts.

```c
#include <stdio.h>
int main(void) {
    Bucket b;
    tb_init(&b, 1000, 1500, 0);  /* 1000 bytes/s, burst 1500 bytes */
    struct { uint64_t t_us, size; } ev[] = {
        {0, 1500}, {500000, 600}, {700000, 600},
        {2700000, 1500}, {2700000, 1} };
    for (int i = 0; i < 5; i++)
        printf("t=%.1fs size=%4llu -> %s\n", ev[i].t_us / 1e6,
               (unsigned long long)ev[i].size,
               tb_allow(&b, ev[i].size, ev[i].t_us) ? "pass" : "drop");
    return 0;
}
```

```
$ gcc -fsanitize=address,undefined -g -o tb tb.c && ./tb
t=0.0s size=1500 -> pass
t=0.5s size= 600 -> drop
t=0.7s size= 600 -> pass
t=2.7s size=1500 -> pass
t=2.7s size=   1 -> drop
```

**What you should notice:** the second packet is dropped although the bucket held 500 tokens, and the third passes 0.2 s later; the fourth empties the bucket and the fifth, in the same instant, is dropped. Change the burst to 1000 and rerun: the first 1500-byte packet is dropped at once, because no packet larger than the bucket can ever pass.
:::

::: lens
[MICROSOFT · AMAZON · CISCO · JUNIPER]{.co}

For the LRU cache the expected sequence is: hash map plus doubly linked list, the O(1) argument, code, then TTL and thread safety. For the rate limiter, interviewers listen for "token bucket", the two parameters, refill-on-demand rather than a timer thread, the monotonic clock and the integer arithmetic. A strong answer also names the concurrency model and what happens at the boundary.
:::

## [1.16]{.sec}Finite-state machines [Should · ■■□]{.tag} {#s1-16}

::: bigidea
A finite-state machine replaces tangled conditionals by a table that gives the next state for every state and event, so the protocol logic can be read, checked and extended as data.
:::

A *finite-state machine* (FSM) has a set of states, a set of events (or input symbols), a start state and a transition function from (state, event) to the next state; an event with no entry is illegal. Protocols such as TCP, link-state adjacency formation and DHCP are specified this way, and Juniper and Broadcom interviews ask for one in C. *Recognise:* "validate a sequence of events", "parse a protocol", "valid number" (a number grammar is an FSM over characters).

<figure>
<svg viewBox="0 0 480 126" width="518"><defs><marker id="a9" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#1A1D23"/></marker></defs>
<rect class="box" x="20" y="40" width="56" height="28" rx="14"/><text class="lbl" x="48" y="58" text-anchor="middle">CLOSED</text><rect class="box" x="120" y="40" width="56" height="28" rx="14"/><text class="lbl" x="148" y="58" text-anchor="middle">SYN&#95;SENT</text><rect class="box" x="220" y="40" width="56" height="28" rx="14"/><text class="lbl" x="248" y="58" text-anchor="middle">ESTAB</text><rect class="box" x="320" y="40" width="56" height="28" rx="14"/><text class="lbl" x="348" y="58" text-anchor="middle">FIN&#95;WAIT</text><rect class="box" x="420" y="40" width="56" height="28" rx="14"/><text class="lbl" x="448" y="58" text-anchor="middle">CLOSED</text><line class="ln" x1="76" y1="54" x2="120" y2="54" marker-end="url(#a9)"/><text class="sm" x="98.0" y="36" text-anchor="middle">send SYN</text><text class="sm" x="98.0" y="82" text-anchor="middle"></text><line class="ln" x1="176" y1="54" x2="220" y2="54" marker-end="url(#a9)"/><text class="sm" x="198.0" y="36" text-anchor="middle">rcv SYN+ACK /</text><text class="sm" x="198.0" y="82" text-anchor="middle">send ACK</text><line class="ln" x1="276" y1="54" x2="320" y2="54" marker-end="url(#a9)"/><text class="sm" x="298.0" y="36" text-anchor="middle">send FIN</text><text class="sm" x="298.0" y="82" text-anchor="middle"></text><line class="ln" x1="376" y1="54" x2="420" y2="54" marker-end="url(#a9)"/><text class="sm" x="398.0" y="36" text-anchor="middle">rcv ACK+FIN /</text><text class="sm" x="398.0" y="82" text-anchor="middle">send ACK</text><path class="acc dash" d="M248,68 Q248,110 48,68" /><text class="sm" x="150" y="112" text-anchor="middle">illegal event in any state: report error and keep state</text>
</svg>
<figcaption><b>Figure 1.21</b> A reduced connection state machine (handshake and teardown only). A table indexed by state and event replaces nested conditionals.</figcaption>
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

**A byte-stream parser.** An FSM is also the natural form of a parser that is fed one byte at a time, as a serial driver is. The framing used on many point-to-point links marks a frame boundary with the flag byte `0x7E`; a data byte equal to the flag or to the escape byte `0x7D` is sent as `0x7D` followed by the byte XOR `0x20`, so the flag never occurs inside a frame. Three states suffice: idle (hunting for a flag), body, and escaped (the next byte is stuffed).

```c
typedef struct {
    enum { IDLE, BODY, ESC } st;
    uint8_t buf[256];
    size_t len;
} Parser;

/* Feed one byte; returns 1 when a frame is in p->buf[0..p->len). */
int feed(Parser *p, uint8_t b) {
    switch (p->st) {
    case IDLE:
        if (b == 0x7E) { p->st = BODY; p->len = 0; }
        return 0;
    case BODY:
        if (b == 0x7E) { p->st = IDLE; return p->len > 0; }   /* end flag */
        if (b == 0x7D) { p->st = ESC; return 0; }
        break;
    case ESC:
        b ^= 0x20;
        p->st = BODY;
        break;
    }
    if (p->len == sizeof p->buf) p->st = IDLE;   /* overflow: resync */
    else p->buf[p->len++] = b;
    return 0;
}
```

For the stream `7E 01 7D 5E 02 7E` the parser enters BODY at the first flag, stores `01`, sees the escape `7D`, converts the next byte `5E` to `5E ^ 20 = 7E` and stores it, stores `02`, and on the closing flag returns 1 with the frame `01 7E 02`. Two flags in a row produce an empty frame, which `p->len > 0` filters out, and a missing flag costs one frame but not the following ones because the parser resynchronises at the next flag. The state variable, not a pile of flags, is what makes each of these cases a single line.

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

::: example
**What a good ten minutes sounds like.** The question is "delete a node with a given value from a singly linked list, in C". A concise version of the exchange follows; the candidate's statements are the point, not the interviewer's.

1. *Clarify.* "Is the list singly linked with a head pointer? May the value occur more than once? Should I delete the first occurrence or all? I will assume the first, and return the new head."
2. *Example.* "For 3 → 5 → 7 and key 5 the result is 3 → 7. For key 3 the head changes, and for key 9 nothing changes."
3. *Brute force.* "Walk with a trailing pointer to the previous node; special-case the head. That is O(*n*) time and O(1) space, which is optimal, since every node may have to be examined."
4. *Improve.* "The head special case is easy to get wrong, so I will hold the address of the link to rewrite instead, a `Node **`."
5. *Code.* The five-line function of [§1.6](#s1-6){.ref}, narrated: "`pp` starts at the head variable; I advance it to the link whose target has the key; then I rewrite that link and free the node after saving it."
6. *Test.* "Empty list: `*pp` is null, nothing happens. One node, key present: the head variable becomes null. Key at the tail: the previous node's link becomes null. Key absent: unchanged."
7. *Evaluate.* "O(*n*) time, O(1) space. If we must delete all occurrences, I do not advance `pp` after a deletion."

[Result: every step is stated aloud, the edge cases are named before the interviewer asks, and the follow-up is anticipated.]{.result}
:::

::: lab
`LAB 1.17 · 2–3 DAYS` **Pillar project: a mini-FIB.** Build a longest-prefix-match lookup engine and measure it. The project joins the pieces of this pillar and gives a concrete talking point for an interview: "I built a forwarding table lookup and compared four methods."

<figure>
<svg viewBox="0 0 440 160" width="475"><defs><marker id="a14" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#1A1D23"/></marker></defs>
<rect class="box" x="10" y="20" width="80" height="26" rx="2"/><text class="lbl" x="50.0" y="36" text-anchor="middle">routes.txt</text><rect class="box" x="120" y="20" width="70" height="26" rx="2"/><text class="lbl" x="155.0" y="36" text-anchor="middle">parser</text><rect class="box" x="220" y="20" width="90" height="26" rx="2"/><text class="lbl" x="265.0" y="36" text-anchor="middle">binary trie</text><rect class="box" x="340" y="20" width="80" height="26" rx="2"/><text class="lbl" x="380.0" y="36" text-anchor="middle">lookup(ip)</text><rect class="box" x="10" y="90" width="80" height="26" rx="2"/><text class="lbl" x="50.0" y="106" text-anchor="middle">queries.txt</text><rect class="box" x="220" y="90" width="90" height="26" rx="2"/><text class="lbl" x="265.0" y="106" text-anchor="middle">route cache</text><line class="ln" x1="90" y1="33" x2="120" y2="33" marker-end="url(#a14)"/><line class="ln" x1="190" y1="33" x2="220" y2="33" marker-end="url(#a14)"/><line class="ln" x1="340" y1="33" x2="310" y2="33" marker-end="url(#a14)"/><line class="ln" x1="90" y1="103" x2="215" y2="103" marker-end="url(#a14)"/><line class="ln" x1="265" y1="90" x2="265" y2="48" marker-end="url(#a14)"/><text class="sm" x="380" y="106" text-anchor="middle">hits/s, hit ratio</text><text class="sm" x="380" y="118" text-anchor="middle">(stretch goal)</text><text class="sm" x="10" y="150" text-anchor="start">stages 1-5: parser with tests, linear scan, trie, per-length hash, benchmark table; stage 6: LRU route cache</text>
</svg>
<figcaption><b>Figure 1.22</b> Architecture of the mini-FIB project. Queries are answered through the cache first, then the trie; the benchmark compares all lookup methods on the same inputs.</figcaption>
</figure>

1. *Parser.* Read lines `prefix/len next_hop` with the validating parsers of [§1.4](#s1-4){.ref}; reject malformed lines with a line number. Write unit tests with the `CHECK` harness above, including /0, /32 and host bits set beyond the prefix length.
2. *Linear scan.* The baseline: for each query, test every prefix with the mask and keep the longest. It is the oracle for the later steps.
3. *Binary trie.* The code of [§1.9](#s1-9){.ref}; compare every answer with the oracle on a million random queries.
4. *Per-length hash.* The 33 hash tables of [§1.9](#s1-9){.ref}'s alternative, probing from /32 downwards.
5. *Benchmark.* Generate a table of 10^4 to 10^6 prefixes with a realistic length mix (many /24, fewer /16 and /8) and report lookups per second for each method in a table.
6. *Stretch.* Put an LRU cache of recent destinations in front of the trie ([§1.15](#s1-15){.ref}) and report the hit ratio; add prefix deletion with pruning.

**What you should notice:** the oracle catches every off-by-one in the masks, which is why it is written first; and the ranking of the methods depends on the table, because the hash method is fast when few prefix lengths occur and the trie when many do. Check the program with `valgrind --leak-check=full` or the sanitisers before showing it.
:::

::: check
1. What are the first two edge cases to try on a linked-list function? [^c1-27]
2. Why state the brute force before the optimised method? [^c1-28]
:::

[^c1-27]: The empty list and the one-node list, followed by operating on the head and the tail.
[^c1-28]: It shows the problem is understood, gives a correct fallback, and makes the source of the improvement explicit.

:::
