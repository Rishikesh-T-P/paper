::: {.p1}

### Heaps, large data and graphs

::: problems

::: q
### Q1.78 Kth largest element
[AMAZON · GOOGLE · OA · ■■□ · T]{.meta}

*Return the *k*-th largest value of an unsorted array (counting duplicates).*

[30-second answer: keep a min-heap of the *k* largest values seen; its root is the answer.]{.short}

```cpp
int kthLargest(const vector<int>& a, int k) {
  priority_queue<int, vector<int>,
                 greater<int>> h;
  for (int x : a) {
    h.push(x);
    if ((int)h.size() > k) h.pop();
  }
  return h.top();
}
```

**Complexity.** O(*n* log *k*) time, O(*k*) space. **Follow-ups.** `nth_element` (quickselect) gives O(*n*) on average but modifies the array; a heap also handles a stream. **Mistakes.** Using a max-heap of size *k* (the trap of [§1.10](#s1-10){.ref}).
:::

::: q
### Q1.79 Median of a data stream
[GOOGLE · AMAZON · TECH-2 · ■■■ · T]{.meta}

*Support `add(x)` and `median()` on a growing stream.*

[30-second answer: a max-heap for the lower half and a min-heap for the upper half, kept equal in size (or one larger below); the median sits at the roots.]{.short}

```cpp
class Median {
  priority_queue<int> lo;   // lower half
  priority_queue<int, vector<int>,
                 greater<int>> hi;
public:
  void add(int x) {
    lo.push(x);
    hi.push(lo.top()); lo.pop();
    if (hi.size() > lo.size()) {
      lo.push(hi.top()); hi.pop();
    }
  }
  double median() {   // after >= 1 add
    return lo.size() > hi.size()
      ? lo.top()
      : ((double)lo.top() + hi.top()) / 2;
  }
};
```

Each `add` sends the new value through `lo` to `hi`, which keeps every value of `lo` no larger than every value of `hi`, and then rebalances. **Complexity.** O(log *n*) per `add`, O(1) per `median`.
:::

::: q
### Q1.80 Top 10 source IPs by bytes in a 10 GB flow log
[GOOGLE · AMAZON · TECH-2 · ■■■ · T]{.meta}

*A flow log of `src_ip bytes` lines is far larger than memory. Report the ten sources with the most bytes.*

[30-second answer: if the distinct addresses fit in memory, one pass with a hash map of totals and a size-10 min-heap suffices; if not, hash-partition the log into files by address, total each file separately, and merge the per-file top tens.]{.short}

**Approach.** Memory is set by the number of *distinct* keys, not by the log size: 10<sup>7</sup> addresses need about 10<sup>7</sup> × (4 + 8) bytes for the totals, which is modest. If even that is too large, partition: a hash of the address picks one of *P* files, so every record of an address lands in the same file, and each file then fits in memory. The top ten overall are among the union of the per-file top tens. When an approximate answer is acceptable, a count-min sketch with a heap of candidates uses fixed memory.

```cpp
using P = pair<uint64_t, uint32_t>;
vector<P> top10(
    unordered_map<uint32_t, uint64_t>& m) {
  priority_queue<P, vector<P>, greater<P>> h;
  for (auto& [ip, b] : m) {
    h.push({b, ip});
    if (h.size() > 10) h.pop();
  }
  vector<P> r;
  while (!h.empty()) {
    r.push_back(h.top()); h.pop();
  }
  reverse(r.begin(), r.end());
  return r;
}
```

**Complexity.** O(*N*) to read, O(*d* log 10) for *d* distinct keys, and two passes of disk I/O when partitioning. **Mistakes.** Partitioning by line number or by byte range (one address then appears in many files and its total is split); sorting all *d* totals when only ten are needed.
:::

::: q
### Q1.81 Reorder packets by sequence number
[ARISTA · BROADCOM · TECH-1 · ■■□ · T]{.meta}

*Packets arrive out of order with sequence numbers. Deliver the data in sequence order, as soon as the next expected number is available, ignoring duplicates.*

[30-second answer: hold arrivals in a min-heap keyed by sequence number; after each arrival release the top while it equals the next expected number.]{.short}

```cpp
struct Reorder {
  using Pk = pair<uint32_t, string>;
  uint32_t next = 0;
  priority_queue<Pk, vector<Pk>,
                 greater<Pk>> pq;
  vector<string> push(uint32_t seq,
                      string data) {
    vector<string> out;
    pq.push({seq, move(data)});
    while (!pq.empty() &&
           pq.top().first <= next) {
      if (pq.top().first == next) {
        out.push_back(pq.top().second);
        ++next;
      }
      pq.pop();   // delivered or duplicate
    }
    return out;
  }
};
```

Arrivals 1, 0, 2 deliver nothing, then `[d0, d1]`, then `[d2]`. **Complexity.** O(log *n*) per packet. **Follow-ups.** Real sequence numbers wrap; compare with `(int32_t)(a - b) < 0`. A bounded window and a timeout decide when to skip a lost packet. **Mistakes.** Letting a duplicate with a smaller number block the heap top forever.
:::

::: q
### Q1.82 Minimum dice throws to finish a snake-and-ladder board
[CISCO · OA · ■■□ · S]{.meta}

*A board has cells 1 to *N*. Landing on a ladder foot or snake head moves you to its other end. A throw advances 1 to 6 cells. Find the fewest throws from cell 1 to cell *N*.*

[30-second answer: model cells as vertices and each throw as an edge of weight one, so breadth-first search from cell 1 gives the minimum.]{.short}

```cpp
int minThrows(const vector<int>& jump) {
  int N = jump.size() - 1;
  vector<int> dist(N + 1, -1);
  queue<int> q;
  dist[1] = 0; q.push(1);
  while (!q.empty()) {
    int u = q.front(); q.pop();
    if (u == N) return dist[u];
    for (int d = 1; d <= 6 && u + d <= N;
         ++d) {
      int v = jump[u + d] > 0
              ? jump[u + d] : u + d;
      if (dist[v] < 0) {
        dist[v] = dist[u] + 1;
        q.push(v);
      }
    }
  }
  return -1;
}
```

With *N* = 30, ladders 3→22, 5→8, 11→26, 20→29 and snakes 27→1, 21→9, 17→4, 19→7, the answer is 3: throw 2 (to 3, up to 22), then 6 (to 28), then 2. **Complexity.** O(6*N*). **Mistakes.** Plain DFS (finds a path, not the shortest); applying a second jump after landing on a jump's end (one throw gives one jump).
:::

::: q
### Q1.83 Number of islands
[AMAZON · MICROSOFT · OA · ■■□ · T]{.meta}

*In a grid of `'1'` (land) and `'0'` (water), count the groups of land cells connected horizontally or vertically.*

[30-second answer: scan the grid; on each unvisited land cell, count one island and flood-fill it (DFS or BFS) so its cells are not counted again.]{.short}

```cpp
int numIslands(vector<string>& g) {
  int R = g.size(), C = R ? g[0].size() : 0;
  int n = 0;
  function<void(int,int)> fill =
      [&](int r, int c) {
    if (r < 0 || c < 0 || r >= R || c >= C
        || g[r][c] != '1') return;
    g[r][c] = '0';   // mark visited
    fill(r + 1, c); fill(r - 1, c);
    fill(r, c + 1); fill(r, c - 1);
  };
  for (int r = 0; r < R; ++r)
    for (int c = 0; c < C; ++c)
      if (g[r][c] == '1') {
        ++n; fill(r, c);
      }
  return n;
}
```

**Complexity.** O(*RC*) time; the recursion depth can reach *RC*, so for large grids use the explicit stack of [§1.11](#s1-11){.ref}. **Mistakes.** No visited marking (infinite recursion); checking bounds after indexing.
:::

::: q
### Q1.84 Can all tasks be finished (course schedule)
[AMAZON · GOOGLE · OA · ■■□ · T]{.meta}

*There are `n` tasks and pairs `[a, b]` meaning "task `b` must precede task `a`". Is there an order that satisfies all pairs?*

[30-second answer: build the dependency graph and run Kahn's topological sort; all tasks can be finished exactly when every vertex is output, i.e. there is no cycle.]{.short}

```cpp
bool canFinish(int n,
               const vector<vector<int>>&
               pre) {
  vector<vector<int>> g(n);
  for (auto& p : pre)
    g[p[1]].push_back(p[0]);
  return (int)topo(n, g).size() == n;
}
```

`topo` is the function of [§1.11](#s1-11){.ref}; returning its order instead of a boolean answers the "find a valid order" variant. **Complexity.** O(*V* + *E*). **Mistakes.** Reversing the edge direction (harmless for the yes/no answer, wrong for the order).
:::

::: q
### Q1.85 Network delay time
[CISCO · GOOGLE · TECH-1 · ■■□ · T]{.meta}

*A signal starts at router `k`. Directed links `[u, v, w]` take `w` time units. How long until all `n` routers (numbered 1 to `n`) have the signal, or −1 if some never do?*

[30-second answer: run Dijkstra from `k`; the answer is the largest shortest distance, or −1 if any router is unreachable.]{.short}

```cpp
int networkDelay(
    const vector<vector<int>>& times,
    int n, int k) {
  Graph g(n + 1);
  for (auto& t : times)
    g[t[0]].push_back({t[1], t[2]});
  auto d = dijkstra(g, k);
  long long worst = 0;
  for (int i = 1; i <= n; ++i)
    worst = max(worst, d[i]);
  return worst >= LLONG_MAX / 4
         ? -1 : (int)worst;
}
```

`Graph` and `dijkstra` are those of [§1.11](#s1-11){.ref}. The signal reaches the last router at the *maximum* of the shortest arrival times, not their sum. **Complexity.** O((*V* + *E*) log *V*). **Mistakes.** Using BFS on weighted links; forgetting that vertex 0 does not exist.
:::

::: q
### Q1.86 Cheapest route with at most k stops
[CISCO · AMAZON · TECH-2 · ■■■ · T]{.meta}

*Given directed priced links `[u, v, price]`, find the cheapest route from `src` to `dst` using at most `k` intermediate stops, or −1.*

[30-second answer: Bellman–Ford with exactly *k* + 1 rounds, each using only the previous round's distances, so a path never exceeds *k* + 1 links.]{.short}

```cpp
int cheapest(int n, vector<vector<int>>& f,
             int src, int dst, int k) {
  vector<Edge> es;
  for (auto& x : f)
    es.push_back({x[0], x[1], x[2]});
  auto d = bellmanFord(n, es, src, k + 1);
  return d[dst] >= LLONG_MAX / 4
         ? -1 : (int)d[dst];
}
```

`Edge` and `bellmanFord` are those of [§1.11](#s1-11){.ref}; the round count is the hop limit, as in a protocol that counts hops. **Complexity.** O((*k* + 1)*E*). **Mistakes.** Dijkstra with a plain distance array (the cheapest route may use too many stops, and a dearer route with fewer stops is then lost).
:::

::: q
### Q1.87 First link that creates a loop
[CISCO · JUNIPER · TECH-1 · ■■□ · T]{.meta}

*Links between nodes 1 to `n` are added in order. Report the first link that connects two nodes that are already connected.*

[30-second answer: union–find over the nodes; the first link whose `unite` returns false closes a loop.]{.short}

```cpp
vector<int> firstLoop(
    int n, const vector<vector<int>>& e) {
  DSU d(n + 1);
  for (auto& x : e)
    if (!d.unite(x[0], x[1])) return x;
  return {};
}
```

`DSU` is the structure of [§1.11](#s1-11){.ref}. In a switched network the same test finds the link that a spanning-tree protocol must block. **Complexity.** O(*E* α(*n*)). **Follow-ups.** For a graph that is a tree plus one extra link, the answer is the last link of the input that lies on the cycle (the variant asked on some sites).
:::

::: q
### Q1.88 Make a network connected
[CISCO · AMAZON · TECH-1 · ■■□ · T]{.meta}

*`n` computers and cables `[a, b]`. In one operation you move a cable to join two computers. Return the fewest operations to connect everything, or −1 if impossible.*

[30-second answer: connecting *c* components needs *c* − 1 spare cables; there are enough exactly when there are at least *n* − 1 cables, so count the components with union–find.]{.short}

```cpp
int makeConnected(
    int n, const vector<vector<int>>& c) {
  if ((int)c.size() < n - 1) return -1;
  DSU d(n);
  int comps = n;
  for (auto& x : c)
    if (d.unite(x[0], x[1])) --comps;
  return comps - 1;
}
```

Every cable that does not merge two components is spare, and with at least *n* − 1 cables there are always enough spares. **Complexity.** O(*E* α(*n*)).
:::

::: q
### Q1.89 Links whose failure splits the network (bridges)
[GOOGLE · ARISTA · TECH-2 · ■■■ · T]{.meta}

*Find every link whose removal disconnects the network (a *bridge*).*

[30-second answer: depth-first search records the entry time `tin` of each vertex and `low`, the earliest entry time reachable from its subtree using one back edge; a tree edge (u, v) is a bridge when `low[v] > tin[u]`.]{.short}

```cpp
vector<vector<int>> bridges(int n,
    const vector<vector<int>>& edges) {
  vector<vector<int>> g(n), out;
  for (auto& e : edges) {
    g[e[0]].push_back(e[1]);
    g[e[1]].push_back(e[0]);
  }
  vector<int> tin(n, -1), low(n, 0);
  int timer = 0;
  function<void(int,int)> dfs =
      [&](int u, int par) {
    tin[u] = low[u] = timer++;
    for (int v : g[u]) {
      if (v == par) continue;
      if (tin[v] >= 0)
        low[u] = min(low[u], tin[v]);
      else {
        dfs(v, u);
        low[u] = min(low[u], low[v]);
        if (low[v] > tin[u])
          out.push_back({u, v});
      }
    }
  };
  for (int i = 0; i < n; ++i)
    if (tin[i] < 0) dfs(i, -1);
  return out;
}
```

If nothing in the subtree below `v` can reach `u` or above except through the edge (u, v), the edge is a bridge. **Complexity.** O(*V* + *E*). **Mistakes.** Skipping a parent edge when links are duplicated (parallel links are never bridges, so a multigraph needs the edge identifier, not the parent vertex).
:::

::: q
### Q1.90 Minimum cost to connect all points
[GOOGLE · AMAZON · TECH-2 · ■■□ · T]{.meta}

*Points on a plane are joined by cables costing the Manhattan distance between endpoints. Find the least total cost that connects all points.*

[30-second answer: this is a minimum spanning tree on a dense graph; Prim's algorithm in O(*n*²), or Kruskal on sorted pair edges with union–find.]{.short}

```cpp
int minCostConnect(
    const vector<vector<int>>& p) {
  int n = p.size(), total = 0;
  vector<int> d(n, INT_MAX);
  vector<char> in(n, 0);
  d[0] = 0;
  for (int it = 0; it < n; ++it) {
    int u = -1;
    for (int i = 0; i < n; ++i)
      if (!in[i] && (u < 0 || d[i] < d[u]))
        u = i;
    in[u] = 1;
    total += d[u];
    for (int v = 0; v < n; ++v)
      if (!in[v])
        d[v] = min(d[v],
          abs(p[u][0] - p[v][0]) +
          abs(p[u][1] - p[v][1]));
  }
  return total;
}
```

`d[v]` is the cheapest cable from the tree to `v`; each round adds the nearest outside point. **Complexity.** O(*n*²) time, O(*n*) space. **Follow-ups.** For sparse graphs, Kruskal costs O(*E* log *E*).
:::

::: q
### Q1.91 Number of provinces (connected components)
[NOKIA · AMAZON · OA · ■■□ · S]{.meta}

*A matrix `m[i][j] = 1` states that nodes `i` and `j` are directly connected. Count the groups of connected nodes.*

[30-second answer: depth-first search with an explicit stack from every unvisited node; the number of starts is the number of groups.]{.short}

```cpp
int provinces(const vector<vector<int>>& m) {
  int n = m.size(), cnt = 0;
  vector<char> seen(n, 0);
  for (int s = 0; s < n; ++s) {
    if (seen[s]) continue;
    ++cnt;
    vector<int> st{s};
    seen[s] = 1;
    while (!st.empty()) {
      int u = st.back(); st.pop_back();
      for (int v = 0; v < n; ++v)
        if (m[u][v] && !seen[v]) {
          seen[v] = 1;
          st.push_back(v);
        }
    }
  }
  return cnt;
}
```

**Complexity.** O(*n*²) for the matrix form. **Follow-ups.** Union–find gives the same count and also handles edges that arrive over time.
:::

:::

### Backtracking, searching, intervals and dynamic programming

::: problems

::: q
### Q1.92 Permutations and combination sum
[GOOGLE · MICROSOFT · TECH-1 · ■■□ · T]{.meta}

*Generate all permutations of distinct integers. Then, from positive integers, list all combinations that sum to a target, each value reusable.*

[30-second answer: choose, explore, un-choose. For permutations, swap each remaining element into position `i` and recurse. For combinations, either take `c[i]` again or skip to `c[i+1]`.]{.short}

```cpp
void perm(vector<int>& a, int i,
          vector<vector<int>>& out) {
  if (i == (int)a.size()) {
    out.push_back(a); return;
  }
  for (int j = i; j < (int)a.size(); ++j) {
    swap(a[i], a[j]);
    perm(a, i + 1, out);
    swap(a[i], a[j]);   // un-choose
  }
}
void comb(const vector<int>& c, int i,
          int rem, vector<int>& path,
          vector<vector<int>>& out) {
  if (rem == 0) {
    out.push_back(path); return;
  }
  if (rem < 0 || i == (int)c.size()) return;
  path.push_back(c[i]);
  comb(c, i, rem - c[i], path, out);
  path.pop_back();
  comb(c, i + 1, rem, path, out);
}
```

**Complexity.** O(*n*·*n*!) for permutations; combinations are bounded by the search tree. **Mistakes.** Forgetting the second `swap` or the `pop_back`; for repeated inputs, duplicates need a sorted array and a skip rule.
:::

::: q
### Q1.93 Search in a rotated sorted array
[GOOGLE · MICROSOFT · TECH-1 · ■■□ · T]{.meta}

*A sorted array of distinct values has been rotated at an unknown point (`4 5 6 7 0 1 2`). Find the index of a target in O(log *n*).*

[30-second answer: in each step one half is sorted; test whether the target lies in the sorted half and discard the other half.]{.short}

```cpp
int searchRot(const vector<int>& a, int x) {
  int lo = 0, hi = (int)a.size() - 1;
  while (lo <= hi) {
    int mid = lo + (hi - lo) / 2;
    if (a[mid] == x) return mid;
    if (a[lo] <= a[mid]) {   // left sorted
      if (a[lo] <= x && x < a[mid])
        hi = mid - 1;
      else lo = mid + 1;
    } else {                 // right sorted
      if (a[mid] < x && x <= a[hi])
        lo = mid + 1;
      else hi = mid - 1;
    }
  }
  return -1;
}
```

Searching 0 in `4 5 6 7 0 1 2`: at mid = 3 (value 7) the left half `4..7` is sorted and excludes 0, so `lo = 4`; at mid = 5 (value 1) the left half `0 1` is sorted and contains 0, so `hi = 4`; mid = 4 then finds index 4. **Complexity.** O(log *n*). **Mistakes.** `<` instead of `<=` in `a[lo] <= a[mid]` when `lo == mid`; duplicates break the test (worst case O(*n*)).
:::

::: q
### Q1.94 Merge overlapping IP address ranges
[GOOGLE · AMAZON · TECH-1 · ■■□ · T]{.meta}

*Given ranges as strings `"a.b.c.d-e.f.g.h"`, merge overlapping ranges and print them in order.*

[30-second answer: convert each end to a 32-bit integer, sort and merge as intervals ([§1.13](#s1-13){.ref}), and convert back.]{.short}

```cpp
extern "C" {
bool parse_ipv4(const char*, uint32_t*);
void format_ipv4(uint32_t, char[16]);
}
vector<string> mergeRanges(
    const vector<string>& in) {
  auto fmt = [](long long x) {
    char b[16];
    format_ipv4((uint32_t)x, b);
    return string(b);
  };
  vector<array<long long, 2>> v;
  for (auto& s : in) {
    size_t d = s.find('-');
    uint32_t a = 0, b = 0;
    parse_ipv4(s.substr(0, d).c_str(), &a);
    parse_ipv4(s.substr(d + 1).c_str(), &b);
    v.push_back({a, b});
  }
  vector<string> out;
  for (auto& r : mergeIntervals(v))
    out.push_back(fmt(r[0]) + "-" +
                  fmt(r[1]));
  return out;
}
```

`10.0.0.1-10.0.0.9` and `10.0.0.5-10.0.0.20` merge to `10.0.0.1-10.0.0.20`. **Complexity.** O(*n* log *n*). **Mistakes.** Comparing the strings (lexicographic order is not numeric order); a signed 32-bit integer for the address (use 64-bit or unsigned). **Follow-ups.** Ask whether adjacent ranges (`…9` and `…10`) should merge.
:::

::: q
### Q1.95 Peak number of simultaneous flows
[CISCO · AMAZON · TECH-1 · ■■□ · T]{.meta}

*Given flow intervals `[start, end)`, find the largest number that overlap at one instant (the meeting-rooms problem).*

[30-second answer: sweep line: turn each interval into a +1 event at its start and a −1 event at its end, sort the events, and track the running total.]{.short}

```cpp
int maxConcurrent(
    const vector<array<int,2>>& iv) {
  vector<pair<int,int>> ev;
  for (auto& x : iv) {
    ev.push_back({x[0], +1});
    ev.push_back({x[1], -1});
  }
  sort(ev.begin(), ev.end());
  int cur = 0, best = 0;
  for (auto& e : ev) {
    cur += e.second;
    best = max(best, cur);
  }
  return best;
}
```

Sorting the pairs puts −1 before +1 at equal times, so an interval ending at *t* frees its slot before another starting at *t* takes it. **Complexity.** O(*n* log *n*). **Follow-ups.** A min-heap of end times gives the same count and the actual assignment.
:::

::: q
### Q1.96 Climbing stairs and house robber (one-dimensional DP)
[AMAZON · MICROSOFT · OA · ■□□ · T]{.meta}

*(a) Count the ways to climb `n` stairs taking 1 or 2 steps at a time. (b) Choose non-adjacent houses to maximise the total loot.*

[30-second answer: (a) `ways[i] = ways[i-1] + ways[i-2]`; (b) the best up to house *i* either skips it or takes it with the best up to *i* − 2. Two variables replace the table.]{.short}

```cpp
int climb(int n) {
  int a = 1, b = 1;   // ways[0], ways[1]
  for (int i = 2; i <= n; ++i) {
    int c = a + b; a = b; b = c;
  }
  return b;
}
int rob(const vector<int>& h) {
  int take = 0, skip = 0;
  for (int x : h) {
    int t = skip + x;
    skip = max(skip, take);
    take = t;
  }
  return max(take, skip);
}
```

`climb(5)` is 8. For houses `[2,7,9,3,1]` the answer is 12 (2 + 9 + 1). **Complexity.** O(*n*) time, O(1) space. **Mistakes.** Taking the maximum of adjacent pairs greedily.
:::

::: q
### Q1.97 Longest increasing subsequence
[GOOGLE · MICROSOFT · TECH-2 · ■■□ · T]{.meta}

*Find the length of the longest strictly increasing subsequence (not necessarily contiguous).*

[30-second answer: keep `t[i]`, the smallest possible last value of an increasing subsequence of length `i + 1`; each new value replaces the first entry that is not smaller, found by binary search.]{.short}

```cpp
int lis(const vector<int>& a) {
  vector<int> t;
  for (int x : a) {
    auto it = lower_bound(t.begin(),
                          t.end(), x);
    if (it == t.end()) t.push_back(x);
    else *it = x;
  }
  return t.size();
}
```

For `[10, 9, 2, 5, 3, 7, 101, 18]` the array `t` evolves 10; 9; 2; 2,5; 2,3; 2,3,7; 2,3,7,101; 2,3,7,18, so the length is 4. Note that `t` is not itself a subsequence of the input. **Complexity.** O(*n* log *n*). The quadratic DP, `dp[i] = 1 + max dp[j]` over smaller `a[j]`, is the form to state first. **Mistakes.** `upper_bound` (allows equal values, giving the non-decreasing variant).
:::

::: q
### Q1.98 Edit distance
[GOOGLE · MICROSOFT · TECH-2 · ■■■ · T]{.meta}

*Find the fewest single-character insertions, deletions and replacements that turn one string into another.*

[30-second answer: `d[i][j]` is the distance between the first `i` characters of `s` and the first `j` of `t`; if the last characters match it equals `d[i-1][j-1]`, otherwise one plus the best of replace, delete and insert.]{.short}

```cpp
int editDistance(const string& s,
                 const string& t) {
  int n = s.size(), m = t.size();
  vector<vector<int>> d(n + 1,
                        vector<int>(m + 1));
  for (int i = 0; i <= n; ++i) d[i][0] = i;
  for (int j = 0; j <= m; ++j) d[0][j] = j;
  for (int i = 1; i <= n; ++i)
    for (int j = 1; j <= m; ++j)
      d[i][j] = s[i-1] == t[j-1]
        ? d[i-1][j-1]
        : 1 + min({d[i-1][j-1],
                   d[i-1][j], d[i][j-1]});
  return d[n][m];
}
```

`"kitten"` to `"sitting"` costs 3 (two replacements and one insertion). **Complexity.** O(*nm*) time and space, reducible to O(min(*n*, *m*)) space by keeping two rows. **Follow-ups.** The longest common subsequence uses the same table with `d[i][j] = d[i-1][j-1] + 1` on a match and `max(d[i-1][j], d[i][j-1])` otherwise.
:::

:::

### Design, rate limiting and finite-state machines

::: problems

::: q
### Q1.99 LRU cache with a time-to-live (an ARP cache), thread-safe
[MICROSOFT · AMAZON · TECH-2 · ■■■ · S]{.meta}

*Extend the LRU cache of [§1.15](#s1-15){.ref}: every entry expires `ttl` time units after it was written, and the cache is used by several threads.*

[30-second answer: store an expiry time in each node and treat an expired entry as a miss; guard every method with one mutex, because even `get` reorders the list.]{.short}

```cpp
class ArpCache {
  struct Item { int key; string mac;
                long long expires; };
  size_t cap; long long ttl;
  list<Item> items;
  unordered_map<int,
      list<Item>::iterator> pos;
  mutex m;
public:
  ArpCache(size_t c, long long t)
      : cap(c), ttl(t) {}
  optional<string> get(int ip,
                       long long now) {
    lock_guard<mutex> g(m);
    auto it = pos.find(ip);
    if (it == pos.end()) return nullopt;
    if (it->second->expires <= now) {
      items.erase(it->second);
      pos.erase(it);
      return nullopt;
    }
    items.splice(items.begin(), items,
                 it->second);
    return it->second->mac;
  }
  void put(int ip, string mac,
           long long now) {
    lock_guard<mutex> g(m);
    if (!cap) return;
    auto it = pos.find(ip);
    if (it != pos.end()) {
      items.erase(it->second);
      pos.erase(it);
    } else if (items.size() == cap) {
      pos.erase(items.back().key);
      items.pop_back();
    }
    items.push_front({ip, move(mac),
                      now + ttl});
    pos[ip] = items.begin();
  }
};
```

The caller supplies `now`, which makes the class testable and lets it use a monotonic clock. Expiry is lazy: an expired entry is removed when it is looked up. **Complexity.** O(1) average per call. **Follow-ups.** A background sweep, or a min-heap of expiry times, frees memory for entries never looked up again; shard the cache by key hash, each shard with its own mutex, to reduce contention; a reader-writer lock does not help because `get` writes. **Mistakes.** Locking only `put`; refreshing the expiry on `get` when the specification says the TTL runs from the write.
:::

::: q
### Q1.100 LFU cache
[AMAZON · GOOGLE · TECH-2 · ■■■ · T]{.meta}

*Like an LRU cache, but evict the least frequently used key; among equals, evict the least recently used. `get` and `put` must be O(1).*

[30-second answer: map each key to its value, count and list position; keep one list of keys per count, and the minimum count so that the victim is the back of that list.]{.short}

```cpp
class LFU {
  struct E { int v, f;
             list<int>::iterator it; };
  int cap, minf = 0;
  unordered_map<int, E> kv;
  unordered_map<int, list<int>> fl;
  void touch(int k) {
    E& e = kv[k];
    fl[e.f].erase(e.it);
    if (fl[e.f].empty()) {
      fl.erase(e.f);
      if (minf == e.f) ++minf;
    }
    ++e.f;
    fl[e.f].push_front(k);
    e.it = fl[e.f].begin();
  }
public:
  explicit LFU(int c) : cap(c) {}
  int get(int k) {
    if (!kv.count(k)) return -1;
    touch(k);
    return kv[k].v;
  }
  void put(int k, int v) {
    if (!cap) return;
    if (kv.count(k)) {
      kv[k].v = v; touch(k); return;
    }
    if ((int)kv.size() == cap) {
      int old = fl[minf].back();
      fl[minf].pop_back();
      if (fl[minf].empty()) fl.erase(minf);
      kv.erase(old);
    }
    minf = 1;
    fl[1].push_front(k);
    kv[k] = {v, 1, fl[1].begin()};
  }
};
```

**Complexity.** O(1) average per operation. **Mistakes.** Not updating `minf` when a frequency list empties; resetting `minf` to 1 only after eviction, not on a new insertion; erasing the key from `kv` but not its list node.
:::

::: q
### Q1.101 Fixed-window versus sliding-window rate limiting
[MICROSOFT · AMAZON · TECH-1 · ■■□ · T]{.meta}

*Implement a limit of `lim` requests per window of `w` time units in two ways, and show a request trace on which the fixed-window version lets through twice the limit.*

[30-second answer: a fixed window keeps one counter per aligned window and resets it at the boundary; a sliding log keeps the timestamps of accepted requests and drops those older than `w`.]{.short}

```cpp
struct Fixed {
  long long w, win = -1;
  int lim, n = 0;
  Fixed(long long w, int lim)
      : w(w), lim(lim) {}
  bool allow(long long t) {
    if (t / w != win) { win = t / w; n = 0; }
    return n < lim && ++n;
  }
};
struct SlidingLog {
  long long w; size_t lim;
  deque<long long> q;
  SlidingLog(long long w, size_t lim)
      : w(w), lim(lim) {}
  bool allow(long long t) {
    while (!q.empty() && q.front() <= t - w)
      q.pop_front();
    if (q.size() >= lim) return false;
    q.push_back(t);
    return true;
  }
};
```

With *lim* = 5 and *w* = 10: five requests at time 9 and five at time 11. The fixed window starts a new window at time 10, so it accepts all ten (ten requests in two time units). The sliding log still holds the five requests of time 9 at time 11 (since 9 > 11 − 10), so it rejects the second batch. **Complexity.** Fixed: O(1) time and space. Log: O(1) amortised time, O(*lim*) space. **Follow-ups.** The token bucket of [§1.15](#s1-15){.ref} is a middle course: two numbers of state and bounded bursts.
:::

::: q
### Q1.102 Rate-limit repeated log messages
[MICROSOFT · AMAZON · OA · ■□□ · T]{.meta}

*A logger prints a message only if the same message has not been printed in the last 10 seconds. Timestamps are non-decreasing.*

[30-second answer: a hash map from message to the time of its last print.]{.short}

```cpp
class Logger {
  unordered_map<string, int> last;
public:
  bool shouldPrint(int t, const string& m) {
    auto it = last.find(m);
    if (it != last.end() &&
        t - it->second < 10)
      return false;
    last[m] = t;
    return true;
  }
};
```

**Complexity.** O(1) average. **Follow-ups.** The map grows without bound; drop entries older than ten seconds with a queue of (time, message) pairs from the front. **Mistakes.** Updating the time of a message that was suppressed (the window would then never end for a steady stream).
:::

::: q
### Q1.103 Insert, delete and get-random in O(1)
[GOOGLE · AMAZON · TECH-1 · ■■□ · T]{.meta}

*Design a set with `insert(x)`, `remove(x)` and `getRandom()` (uniform over the elements), all O(1) on average.*

[30-second answer: keep the elements in a vector for random access and a hash map from value to its index; remove by moving the last element into the removed slot.]{.short}

```cpp
class RandomSet {
  vector<int> v;
  unordered_map<int, int> pos;
public:
  bool insert(int x) {
    if (pos.count(x)) return false;
    pos[x] = v.size();
    v.push_back(x);
    return true;
  }
  bool remove(int x) {
    auto it = pos.find(x);
    if (it == pos.end()) return false;
    int last = v.back(), i = it->second;
    v[i] = last;
    pos[last] = i;
    v.pop_back();
    pos.erase(x);
    return true;
  }
  int getRandom() {
    return v[rand() % v.size()];
  }
};
```

Moving the last element avoids shifting the vector. When `x` is itself the last element, `v[i] = last` and `pos[last] = i` are harmless self-assignments, and `pos.erase(x)` then removes it. **Complexity.** O(1) average. **Mistakes.** Erasing from the middle of the vector (O(*n*)); forgetting to update the index of the moved element.
:::

::: q
### Q1.104 Valid number (a finite-state scan)
[JUNIPER · MICROSOFT · TECH-2 · ■■■ · T]{.meta}

*Decide whether a string is a valid decimal number: optional sign, digits with an optional point (at least one digit overall), and an optional exponent `e` or `E` with an optional sign and at least one digit.*

[30-second answer: scan in the order sign, integer part, point and fraction, exponent; each stage is a state, and a stage needing a digit fails if none follows.]{.short}

```cpp
bool isNumber(const string& s) {
  size_t i = 0, n = s.size();
  bool dig = false;
  auto D = [&](size_t k) {
    return k < n &&
        isdigit((unsigned char)s[k]);
  };
  if (i < n && (s[i] == '+' || s[i] == '-'))
    ++i;
  while (D(i)) { ++i; dig = true; }
  if (i < n && s[i] == '.') {
    ++i;
    while (D(i)) { ++i; dig = true; }
  }
  if (!dig) return false;
  if (i < n && (s[i] == 'e' ||
                s[i] == 'E')) {
    ++i;
    if (i < n && (s[i] == '+' || s[i] == '-'))
      ++i;
    if (!D(i)) return false;
    while (D(i)) ++i;
  }
  return i == n;
}
```

Accepted: `"2"`, `".5"`, `"3."`, `"-1.2e+10"`. Rejected: `"."`, `"e3"`, `"1e"`, `"1e+"`, `"--1"`, `"1 "`. The same logic as a table over (state, character class) is the form to present for a state-machine question: the states are start, sign, integer, point, fraction, exponent, exponent sign and exponent digits. **Complexity.** O(*n*). **Mistakes.** Accepting a bare point, or an exponent with no digits.
:::

:::
:::
