::: {.p1}

## [1.11]{.sec}Graphs: networks are graphs [Must · ■■■]{.tag} {#s1-11}

::: bigidea
A network is a graph of nodes and links, so routing, loop detection and reachability become traversal, shortest-path and connectivity problems, each solved by one of five short templates.
:::

A *graph* has *V* vertices and *E* edges; an edge may be directed, may carry a weight (a link cost or delay), and the graph may be disconnected. The usual representation is an *adjacency list*: for each vertex, the list of its neighbours (with weights). It takes O(*V* + *E*) space, which suits the sparse graphs of networks. An *adjacency matrix* takes O(*V*²) space and answers "is there an edge" in O(1); it suits dense graphs and small *V*. The choice of algorithm follows the question.

| Question | Algorithm | Time |
|---|---|---|
| reachable? components? loop present? | DFS or BFS | O(*V* + *E*) |
| fewest hops (unweighted shortest path) | BFS | O(*V* + *E*) |
| cheapest path, non-negative weights | Dijkstra | O((*V* + *E*) log *V*) |
| negative weights, or at most *k* edges | Bellman–Ford | O(*VE*) |
| all pairs, *V* ≤ 400 | Floyd–Warshall | O(*V*³) |
| order tasks with dependencies | topological sort (Kahn) | O(*V* + *E*) |
| dynamic connectivity, "does this edge close a loop" | union–find | about O(α(*n*)) per operation |

**Graphs in C.** Without `vector`, the compact form is a set of arrays: `head[u]` holds the index of the first outgoing edge of *u*, each edge stores its target, weight and the index of the next edge of the same vertex, and a new edge is pushed on the front of its list. Visiting the neighbours of *u* is then a walk along that chain.

```c
#define MAXV 1000
#define MAXE 10000
static int head[MAXV], nxt[MAXE], to[MAXE], wt[MAXE], ecnt;

void g_init(int n) { for (int i = 0; i < n; i++) head[i] = -1; ecnt = 0; }
void add_edge(int u, int v, int w) {     /* directed edge */
    to[ecnt] = v; wt[ecnt] = w; nxt[ecnt] = head[u];
    head[u] = ecnt++;
}
/* for (int e = head[u]; e != -1; e = nxt[e]) { use to[e], wt[e]; } */
```

*Modelling.* Many problems are graph problems in disguise, and the skill is to name the vertices and edges. In snake and ladder the vertices are the board cells and the edges are the six throws; in a word ladder the vertices are words and an edge joins words that differ in one letter; in a maze the vertices are the free cells. When every edge costs one, BFS is the answer; when edges cost zero or one, a deque-based variant (0-1 BFS) pushes zero-cost edges at the front.

### Breadth-first and depth-first search

BFS explores in rings of increasing hop count, using a queue, so the first time it reaches a vertex is by a shortest path. Marking a vertex visited when it is *pushed* (not when it is popped) keeps duplicates out of the queue. DFS follows one path as deep as it goes, using a stack, and is the tool for connectivity, cycles and ordering. The iterative form avoids the recursion limit (about 1000 in Python, and the stack size in C).

```cpp
vector<int> bfs(const vector<vector<int>>& g, int src) {
    // hop distance from src, -1 if unreachable
    vector<int> dist(g.size(), -1);
    queue<int> q; dist[src] = 0; q.push(src);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : g[u])
            if (dist[v] < 0) {                      // mark on push
                dist[v] = dist[u] + 1; q.push(v);
            }
    }
    return dist;
}

vector<int> dfsOrder(const vector<vector<int>>& g, int s) {   // iterative
    vector<char> seen(g.size(), 0); vector<int> st{s}, order;
    while (!st.empty()) {
        int u = st.back(); st.pop_back();
        if (seen[u]) continue;
        seen[u] = 1; order.push_back(u);
        for (int i = (int)g[u].size() - 1; i >= 0; --i)  // reverse order
            if (!seen[g[u][i]]) st.push_back(g[u][i]);
    }
    return order;
}
```

<figure>
<svg viewBox="0 0 400 220" width="432">
<circle class="lg dash" cx="200" cy="95" r="45" style="fill:none"/><text class="sm" x="192" y="152" text-anchor="start">hop 1</text><circle class="lg dash" cx="200" cy="95" r="90" style="fill:none"/><text class="sm" x="192" y="196" text-anchor="start">hop 2</text><line class="ln" x1="200" y1="95" x2="155" y2="95"/><line class="ln" x1="200" y1="95" x2="230" y2="61"/><line class="ln" x1="200" y1="95" x2="230" y2="129"/><line class="ln" x1="155" y1="95" x2="110" y2="95"/><line class="ln" x1="155" y1="95" x2="140" y2="27"/><line class="ln" x1="230" y1="61" x2="290" y2="83"/><line class="ln" x1="230" y1="129" x2="260" y2="163"/><line class="ln" x1="230" y1="61" x2="230" y2="129"/><circle class="box" cx="200" cy="95" r="11" style="fill:#FFF4C2"/><text class="lbl" x="200" y="98" text-anchor="middle">S</text><circle class="box" cx="155" cy="95" r="11"/><text class="lbl" x="155" y="98" text-anchor="middle">A</text><circle class="box" cx="230" cy="61" r="11"/><text class="lbl" x="230" y="64" text-anchor="middle">B</text><circle class="box" cx="230" cy="129" r="11"/><text class="lbl" x="230" y="132" text-anchor="middle">C</text><circle class="box" cx="110" cy="95" r="11"/><text class="lbl" x="110" y="98" text-anchor="middle">D</text><circle class="box" cx="140" cy="27" r="11"/><text class="lbl" x="140" y="30" text-anchor="middle">E</text><circle class="box" cx="290" cy="83" r="11"/><text class="lbl" x="290" y="86" text-anchor="middle">F</text><circle class="box" cx="260" cy="163" r="11"/><text class="lbl" x="260" y="166" text-anchor="middle">G</text><text class="sm" x="10" y="212" text-anchor="start">queue order: S | A B C | D E F G. A vertex joins a ring when first reached.</text>
</svg>
<figcaption><b>Figure 1.17</b> Breadth-first search explores in rings of equal hop count, so the first time a vertex is reached is by a shortest path.</figcaption>
</figure>

::: trap
*Claim:* a traversal needs no visited set if the graph "looks like a tree". *Why it is wrong:* a single cycle, or a second path to the same vertex, makes the traversal revisit vertices, and on a cycle it never ends. This is a broadcast storm in code form: a frame flooded around a switched loop is never removed. *Correct statement:* mark each vertex when first reached and skip marked vertices.
:::

A grid is a graph whose vertices are cells and whose neighbours are the four adjacent cells; "number of islands" is the count of DFS starts, and "rotting oranges" and "distance to the nearest gate" are BFS started from all sources at once (multi-source BFS). These are in the Problem Set.

### Dijkstra's algorithm

*Idea.* Keep a tentative distance to each vertex. Repeatedly settle the unsettled vertex with the smallest tentative distance, and relax its edges: if going through it improves a neighbour's distance, update it. Because every weight is non-negative, no later path can reach a settled vertex more cheaply, so a settled distance is final. A min-heap supplies the next vertex. Entries are never updated in place; an improved vertex is pushed again, and the older, larger entry is discarded when it surfaces. *Recognise:* "cheapest", "minimum time", "network delay", weights present and non-negative.

<figure>
<svg viewBox="0 0 460 192" width="497">
<line class="lg" x1="50" y1="90" x2="170" y2="40"/><line class="lg" x1="50" y1="90" x2="170" y2="140"/><line class="lg" x1="170" y1="140" x2="170" y2="40"/><line class="lg" x1="170" y1="40" x2="300" y2="90"/><line class="lg" x1="170" y1="140" x2="300" y2="90"/><line class="lg" x1="300" y1="90" x2="420" y2="90"/><path class="acc" d="M50,90 L170,140 L170,40 L300,90 L420,90" stroke-linejoin="round"/><rect x="103.0" y="58.0" width="14" height="13" fill="#fff"/><text class="lbl" x="110.0" y="68.0" text-anchor="middle">4</text><rect x="103.0" y="108.0" width="14" height="13" fill="#fff"/><text class="lbl" x="110.0" y="118.0" text-anchor="middle">1</text><rect x="173.0" y="83.0" width="14" height="13" fill="#fff"/><text class="lbl" x="180.0" y="93.0" text-anchor="middle">2</text><rect x="228.0" y="58.0" width="14" height="13" fill="#fff"/><text class="lbl" x="235.0" y="68.0" text-anchor="middle">5</text><rect x="228.0" y="108.0" width="14" height="13" fill="#fff"/><text class="lbl" x="235.0" y="118.0" text-anchor="middle">8</text><rect x="353.0" y="83.0" width="14" height="13" fill="#fff"/><text class="lbl" x="360.0" y="93.0" text-anchor="middle">3</text><circle class="box" cx="50" cy="90" r="13"/><text class="lbl" x="50" y="93" text-anchor="middle">A</text><circle class="box" cx="170" cy="40" r="13"/><text class="lbl" x="170" y="43" text-anchor="middle">B</text><circle class="box" cx="170" cy="140" r="13"/><text class="lbl" x="170" y="143" text-anchor="middle">C</text><circle class="box" cx="300" cy="90" r="13"/><text class="lbl" x="300" y="93" text-anchor="middle">D</text><circle class="box" cx="420" cy="90" r="13"/><text class="lbl" x="420" y="93" text-anchor="middle">E</text><text class="sm" x="20" y="180" text-anchor="start">shortest path tree from A: A-C-B-D-E, total cost 1+2+5+3 = 11</text>
</svg>
<figcaption><b>Figure 1.18</b> A weighted undirected graph (link costs). The accent path is the shortest route from A to E.</figcaption>
</figure>

```cpp
using Graph = vector<vector<pair<int, int>>>;  // g[u] = {(v, weight), ...}

vector<long long> dijkstra(const Graph& g, int src) {
    const long long INF = LLONG_MAX / 4;
    vector<long long> dist(g.size(), INF);
    using P = pair<long long, int>;
    priority_queue<P, vector<P>, greater<>> pq;
    dist[src] = 0; pq.push({0, src});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;  // stale entry
        for (auto [v, w] : g[u])
            if (d + w < dist[v]) { dist[v] = d + w; pq.push({dist[v], v}); }
    }
    return dist;
}
```

::: example
**Shortest paths from A in Figure 1.18.** Edges: A–B 4, A–C 1, C–B 2, B–D 5, C–D 8, D–E 3.

| Pop (d, u) | Action | dist after (A B C D E) | Heap after |
|---|---|---|---|
| (0, A) | relax B = 4, C = 1 | 0 4 1 ∞ ∞ | (1,C) (4,B) |
| (1, C) | B improves to 3; D = 9 | 0 3 1 9 ∞ | (3,B) (4,B) (9,D) |
| (3, B) | D improves to 8 | 0 3 1 8 ∞ | (4,B) (8,D) (9,D) |
| (4, B) | stale: 4 > 3, skipped | unchanged | (8,D) (9,D) |
| (8, D) | E = 11 | 0 3 1 8 11 | (9,D) (11,E) |
| (9, D) | stale: 9 > 8, skipped | unchanged | (11,E) |
| (11, E) | no edges to improve | final | empty |

[Result: distances 0, 3, 1, 8, 11; the route to E is A–C–B–D–E. Without the stale check, the entries (4,B) and (9,D) would be expanded again, repeating work.]{.result}
:::

*Complexity.* Each edge causes at most one push, so the heap holds at most *E* entries and the total cost is O((*V* + *E*) log *V*). The algorithm is wrong when an edge weight is negative, because a settled vertex could later be improved.

::: trap
*Claim:* the line `if (d > dist[u]) continue;` is an optimisation that can be left out. *Why it is wrong:* the result stays correct, but each stale entry re-expands its vertex, and on dense graphs the running time grows from O(*E* log *V*) to O(*VE*). *Correct statement:* always skip stale entries.
:::

### Bellman–Ford

Bellman–Ford relaxes every edge, *V* − 1 times. After round *r*, `dist[v]` is the cost of the best path using at most *r* edges, so stopping after *k* rounds answers "cheapest path with at most *k* edges", the hop-limited form that appears in "cheapest flights within *k* stops". Copying the array each round ensures that round *r* uses only distances from round *r* − 1. A further round that still improves some distance proves a negative cycle.

```cpp
struct Edge { int u, v, w; };
vector<long long> bellmanFord(int n, const vector<Edge>& es,
                              int src, int rounds) {
    const long long INF = LLONG_MAX / 4;
    vector<long long> dist(n, INF); dist[src] = 0;
    for (int r = 0; r < rounds; ++r) {  // rounds <= n - 1
        vector<long long> nxt = dist;  // use last round's values only
        for (const Edge& e : es)
            if (dist[e.u] < INF && dist[e.u] + e.w < nxt[e.v])
                nxt[e.v] = dist[e.u] + e.w;
        dist = nxt;
    }
    return dist;
}
```

The table traces the synchronous rounds on a four-router chain with costs A–B 1, B–C 1, C–D 1 and a direct A–D link of cost 10. After round *r*, `dist[v]` is the cheapest cost using at most *r* links.

| Round | dist[A] | dist[B] | dist[C] | dist[D] | What improved |
|---|---|---|---|---|---|
| 0 | 0 | ∞ | ∞ | ∞ | start |
| 1 | 0 | 1 | ∞ | 10 | B through A–B; D through the direct link |
| 2 | 0 | 1 | 2 | 10 | C through B |
| 3 | 0 | 1 | 2 | 3 | D through C replaces the direct link |

The direct link is cheaper in hops but dearer in cost, which is the reason a hop-limited query (at most one link) answers 10 while the unrestricted answer is 3.

**All pairs.** Floyd–Warshall computes the cheapest path between every pair by allowing, one vertex at a time, that vertex as an intermediate stop. The loop over the intermediate vertex *k* must be outermost, because `d[i][k]` and `d[k][j]` must already describe paths that use only the vertices before *k*.

```cpp
void floyd(vector<vector<long long>>& d) {   // d[i][j]: cost or INF
    int n = d.size();
    const long long INF = LLONG_MAX / 4;
    for (int k = 0; k < n; ++k)
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j)
                if (d[i][k] < INF && d[k][j] < INF)
                    d[i][j] = min(d[i][j], d[i][k] + d[k][j]);
}
```

It runs in O(*V*³) time and O(*V*²) space, which limits it to about *V* ≤ 400.

Dijkstra and Bellman–Ford are also the two shortest-path methods of routing protocols. Link-state protocols such as OSPF and IS-IS give every router the whole graph, and each router runs Dijkstra locally; distance-vector protocols such as RIP run Bellman–Ford in a distributed way, each router relaxing the costs its neighbours advertise. The protocols are taught in the routing chapter; the comparison is a common interview bridge question, and this paragraph is its core.

### Topological order and union–find

A *topological order* lists the vertices of a directed acyclic graph so that every edge goes forward; it is the order in which dependent tasks can run. Kahn's algorithm repeatedly removes a vertex of in-degree zero. If fewer than *V* vertices are output, a cycle exists.

```cpp
vector<int> topo(int n, const vector<vector<int>>& g) {
    vector<int> indeg(n, 0), order;
    for (const auto& adj : g) for (int v : adj) ++indeg[v];
    queue<int> q;
    for (int i = 0; i < n; ++i) if (!indeg[i]) q.push(i);
    while (!q.empty()) {
        int u = q.front(); q.pop(); order.push_back(u);
        for (int v : g[u]) if (--indeg[v] == 0) q.push(v);
    }
    return order;  // size < n: a cycle exists
}
```

*Union–find* (disjoint-set union, DSU) maintains a partition of vertices into components under "add edge". `find` returns a component's representative, with path compression; `unite` merges two components, attaching the smaller to the larger. An edge whose endpoints already share a representative closes a loop, which is how a network with redundant links, or a spanning-tree protocol, is reasoned about.

```cpp
struct DSU {
    vector<int> p, sz;
    explicit DSU(int n) : p(n), sz(n, 1) { iota(p.begin(), p.end(), 0); }
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;  // already connected: edge closes a loop
        if (sz[a] < sz[b]) swap(a, b);
        p[b] = a; sz[a] += sz[b];
        return true;
    }
};
```

<figure>
<svg viewBox="0 0 400 164" width="432"><defs><marker id="a13" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#3D55A8"/></marker></defs>
<text class="sm" x="80" y="14" text-anchor="middle">before find(3)</text><text class="sm" x="300" y="14" text-anchor="middle">after find(3) with path compression</text><circle class="box" cx="80" cy="36" r="12"/><text class="lbl" x="80" y="39" text-anchor="middle">0</text><circle class="box" cx="80" cy="72" r="12"/><text class="lbl" x="80" y="75" text-anchor="middle">1</text><line class="ln" x1="80" y1="60" x2="80" y2="48" marker-end="url(#a13)"/><circle class="box" cx="80" cy="108" r="12"/><text class="lbl" x="80" y="111" text-anchor="middle">2</text><line class="ln" x1="80" y1="96" x2="80" y2="84" marker-end="url(#a13)"/><circle class="box" cx="80" cy="144" r="12"/><text class="lbl" x="80" y="147" text-anchor="middle">3</text><line class="ln" x1="80" y1="132" x2="80" y2="120" marker-end="url(#a13)"/><circle class="box" cx="300" cy="36" r="12"/><text class="lbl" x="300" y="39" text-anchor="middle">0</text><circle class="box" cx="240" cy="100" r="12"/><text class="lbl" x="240" y="103" text-anchor="middle">1</text><line class="acc" x1="240" y1="88" x2="300" y2="48" marker-end="url(#a13)"/><circle class="box" cx="300" cy="100" r="12"/><text class="lbl" x="300" y="103" text-anchor="middle">2</text><line class="acc" x1="300" y1="88" x2="300" y2="48" marker-end="url(#a13)"/><circle class="box" cx="360" cy="100" r="12"/><text class="lbl" x="360" y="103" text-anchor="middle">3</text><line class="acc" x1="360" y1="88" x2="300" y2="48" marker-end="url(#a13)"/><text class="sm" x="300" y="140" text-anchor="middle">every node on the path now points</text><text class="sm" x="300" y="152" text-anchor="middle">straight at the representative</text>
</svg>
<figcaption><b>Figure 1.19</b> Path compression in union-find. Arrows are parent pointers; after one find, later finds on the same nodes take a single step.</figcaption>
</figure>

With both optimisations each operation is O(α(*n*)), where α is the inverse Ackermann function, below 5 for any input that fits in memory. Kruskal's minimum spanning tree sorts the edges by weight and adds each edge whose `unite` returns true. Floyd–Warshall computes all pairs with three nested loops, `for k, for i, for j: d[i][j] = min(d[i][j], d[i][k] + d[k][j])`, and the loop over *k* must be outermost.

**Minimum spanning tree.** A *spanning tree* connects all vertices with *V* − 1 edges and no loop; a minimum one has the least total weight. Kruskal's algorithm sorts the edges and adds each edge whose endpoints are still in different components, which union–find decides.

```cpp
long long kruskal(int n, vector<Edge> es) {   // Edge: see Bellman-Ford
    sort(es.begin(), es.end(),
         [](const Edge& a, const Edge& b) { return a.w < b.w; });
    DSU d(n);
    long long total = 0;
    for (const Edge& e : es)
        if (d.unite(e.u, e.v)) total += e.w;  // joins two components: keep
    return total;  // add a check for connectivity if needed
}
```

For the edges A–B 1, B–C 1, C–D 1, A–D 10 the sorted order is 1, 1, 1, 10; the three links of cost 1 are kept, and A–D is rejected because A and D are already joined, giving a tree of cost 3. The same loop-avoidance idea, applied to a switched network, is what a spanning-tree protocol does with its root election and blocked ports; those protocols are taught in the switching chapter.

::: lens
[CISCO · GOOGLE · AMAZON · NOKIA]{.co}

Reported problems include the minimum dice throws of a snake-and-ladder board (BFS on 100 cells), depth-first search without recursion, the time for a signal to reach all routers (Dijkstra), links whose failure partitions the network (bridges), and the first link that creates a loop (union–find). A strong answer names the graph (what is a vertex, what is an edge), picks the algorithm from the table above, and states its complexity. If asked "why not union–find, why BFS", answering with the trade-off, not defending one tool, is what is scored.
:::

::: check
1. Why must BFS mark a vertex when it is pushed rather than popped? [^c1-20]
2. What does Dijkstra do wrongly on a graph with a negative edge? [^c1-21]
3. In union–find, what does `unite` returning false mean? [^c1-22]
:::

[^c1-20]: Otherwise a vertex reachable by two paths can be queued twice before either copy is popped, doing the work again.
[^c1-21]: It may settle a vertex with a distance that a later negative edge would have lowered, and it never revisits settled vertices.
[^c1-22]: The two endpoints were already connected, so the edge would close a loop.

## [1.12]{.sec}Recursion and backtracking [Should · ■■□]{.tag} {#s1-12}

::: bigidea
Backtracking builds an answer one choice at a time and undoes each choice after exploring it, so a single recursive function enumerates every candidate while the constraints prune the hopeless ones early.
:::

A recursive function needs a *base case* that stops the recursion and a *step* that moves towards it. Backtracking adds a *path* that is extended before the recursive call and restored after it: choose, explore, un-choose. *Recognise:* "all combinations, permutations or subsets", "generate all", "place so that no two conflict", and small limits (*n* ≤ 12 for permutations, *n* ≤ 20 for subsets). The cost is the size of the search tree: 2<sup>*n*</sup> for subsets, *n*! for permutations.

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
4. Pruning by these rules leaves very few branches: at most 3<sup>4</sup> = 81 leaves are ever reached.

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

**Pruning in practice.** The power of backtracking comes from rejecting a partial answer at once. In the *N*-queens problem we place one queen per row and must avoid shared columns and diagonals. A bitmask per constraint makes the test a single AND: `cols` marks the occupied columns, and the two diagonal masks shift by one place at each new row.

```cpp
int nQueens(int n) {
    int count = 0;
    function<void(int,int,int,int)> go =
        [&](int row, int cols, int d1, int d2) {
        if (row == n) { ++count; return; }
        int free = ((1 << n) - 1) & ~(cols | d1 | d2);   // safe columns
        while (free) {
            int bit = free & -free;  // lowest safe column
            free -= bit;
            go(row + 1, cols | bit, (d1 | bit) << 1, (d2 | bit) >> 1);
        }
    };
    go(0, 0, 0, 0);
    return count;
}
```

The counts are 2 for *n* = 4 and 92 for *n* = 8. Without pruning the search would examine 8<sup>8</sup> ≈ 1.7 × 10<sup>7</sup> placements; with it, only a few thousand partial boards are visited. The same shape (choose a candidate from a mask of the allowed ones, recurse, undo) solves Sudoku and word-search problems.

::: trap
*Claim:* Python's recursion handles a depth-first search of any size. *Why it is wrong:* CPython allows about 1000 nested calls by default, and a path graph of 10<sup>5</sup> vertices raises `RecursionError`; C overflows its stack in the same way. *Correct statement:* use an explicit stack for deep graphs, or raise the limit only when the depth is known and modest.
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

### Merge sort, partition and quickselect

Two sorting ideas recur in interviews. *Merge sort* splits the array, sorts both halves and merges them, with the recurrence `T(n) = 2T(n/2) + O(n)` that gives O(*n* log *n*) in every case; it is stable and needs O(*n*) extra space, and its merge step is exactly the merge of two sorted lists. *Partitioning* rearranges an array around a pivot so that smaller values precede it and larger values follow; it is the step of quicksort, and it leads to *quickselect*, which finds the *k*-th smallest value without sorting everything.

```cpp
void mergeSort(vector<int>& a, int l, int r,
               vector<int>& tmp) {                    // sorts [l, r)
    if (r - l < 2) return;
    int m = l + (r - l) / 2;
    mergeSort(a, l, m, tmp);
    mergeSort(a, m, r, tmp);
    merge(a.begin() + l, a.begin() + m, a.begin() + m, a.begin() + r,
          tmp.begin() + l);
    copy(tmp.begin() + l, tmp.begin() + r, a.begin() + l);
}

int partition(vector<int>& a, int lo, int hi) {   // [lo, hi]; pivot index
    swap(a[hi], a[lo + rand() % (hi - lo + 1)]);   // random pivot
    int p = a[hi], i = lo;
    for (int j = lo; j < hi; ++j)
        if (a[j] < p) swap(a[i++], a[j]);
    swap(a[i], a[hi]);
    return i;
}
int quickselect(vector<int> a, int k) {  // k-th smallest, k from 0
    int lo = 0, hi = (int)a.size() - 1;
    while (true) {
        int p = partition(a, lo, hi);
        if (p == k) return a[p];
        if (p < k) lo = p + 1; else hi = p - 1;   // side holding k
    }
}
```

For `[7, 2, 9, 4, 1]` with *k* = 1 (the second smallest), a partition around the pivot 4 produces `[2, 1, 4, 7, 9]` with the pivot at index 2; since 2 > 1 the search continues on the left part `[2, 1]`, whose partition places 1 at index 0 and 2 at index 1. Index 0 is below *k*, so the search narrows to index 1, which holds 2, and the answer is 2. Each partition discards a constant fraction of the data on average, so the work is *n* + *n*/2 + *n*/4 + … = O(*n*) on average, and O(*n*²) only for an unlucky sequence of pivots. When the keys are small integers, *counting sort* beats all of these: count the occurrences of each value in O(*n* + *k*) and write the values out in order.

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

The two classic bugs are the midpoint overflow in `(lo + hi) / 2` for ranges beyond 2<sup>30</sup>, and an update such as `lo = mid`, which loops forever when `hi = lo + 1`. The loop runs ⌈log₂ *n*⌉ times.

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

:::
