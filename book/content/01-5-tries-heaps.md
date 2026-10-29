::: {.p1}

## [1.9]{.sec}Tries and longest-prefix match [Must · ■■■]{.tag} {#s1-9}

::: bigidea
A router forwards a packet along the most specific route that contains its destination, and a trie finds that route by reading the address one bit at a time, in a number of steps bounded by the address length and independent of the number of routes.
:::

A *trie* (prefix tree) stores a set of strings along the edges of a tree: the path from the root spells the string, and a flag on a node marks that a stored string ends there. Lookup costs O(*L*) for a key of length *L*, regardless of how many keys are stored. *Recognise:* "words with this prefix", "autocomplete", "longest common prefix", "maximum XOR", and above all "longest prefix match" on IP addresses.

**The routing problem.** A forwarding table maps *prefixes* to next hops. A prefix `10.1.0.0/16` matches every address whose first 16 bits equal those of 10.1.0.0. Prefixes overlap: an address in 10.1.2.0/24 also lies in 10.1.0.0/16 and in 10.0.0.0/8. The forwarding rule is that the matching prefix with the greatest length wins, termed *longest-prefix match* (LPM), because the longer prefix is the more specific route. (Why routers need this, and how routes are learned, is taught in the routing chapter; here we implement the lookup.)

**Binary trie.** We treat a 32-bit address as a string over {0, 1}, with one level per bit. Inserting a prefix of length *p* follows (and creates) *p* edges and stores the next hop at the final node. A lookup follows the address bits from the root and records the next hop of every marked node it passes; when the next edge is missing, the last recorded hop is the longest match.

<figure>
<svg viewBox="0 0 440 200" width="475">
<line class="acc" x1="240" y1="24" x2="140" y2="64"/><text class="sm" x="182.0" y="42.0" text-anchor="middle">0</text><line class="ln" x1="240" y1="24" x2="340" y2="64"/><text class="sm" x="298.0" y="42.0" text-anchor="middle">1</text><line class="acc" x1="140" y1="64" x2="200" y2="104"/><text class="sm" x="178.0" y="82.0" text-anchor="middle">1</text><line class="acc" x1="200" y1="104" x2="260" y2="144"/><text class="sm" x="238.0" y="122.0" text-anchor="middle">1</text><line class="ln" x1="260" y1="144" x2="300" y2="184"/><text class="sm" x="272.0" y="162.0" text-anchor="middle">0</text><circle class="box" cx="240" cy="24" r="11" style="fill:#fff"/><circle class="box" cx="140" cy="64" r="11" style="fill:#FFF4C2"/><text class="lbl" x="140" y="67" text-anchor="middle">A</text><circle class="box" cx="340" cy="64" r="11" style="fill:#FFF4C2"/><text class="lbl" x="340" y="67" text-anchor="middle">D</text><circle class="box" cx="200" cy="104" r="11" style="fill:#FFF4C2"/><text class="lbl" x="200" y="107" text-anchor="middle">B</text><circle class="box" cx="260" cy="144" r="11" style="fill:#fff"/><circle class="box" cx="300" cy="184" r="11" style="fill:#FFF4C2"/><text class="lbl" x="300" y="187" text-anchor="middle">C</text><text class="sm" x="10" y="60" text-anchor="start">Prefixes (4-bit toy):</text><text class="mono" x="10" y="74" text-anchor="start">0&#42;   → A</text><text class="mono" x="10" y="86" text-anchor="start">01&#42;  → B</text><text class="mono" x="10" y="98" text-anchor="start">0110 → C</text><text class="mono" x="10" y="110" text-anchor="start">1&#42;   → D</text><text class="sm" x="330" y="140" text-anchor="start">lookup 0111 (accent path):</text><text class="sm" x="330" y="153" text-anchor="start">marks seen: A, then B;</text><text class="sm" x="330" y="166" text-anchor="start">no edge 0 below 011,</text><text class="lbl" x="330" y="179" text-anchor="start">so the answer is B</text>
</svg>
<figcaption><b>Figure 1.14</b> A binary trie for four toy prefixes. A shaded node carries a next hop; a lookup walks the address bits and remembers the deepest shaded node it passed.</figcaption>
</figure>

```c
#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct Node {
    struct Node *c[2];
    int hop;                       /* hop < 0: no route ends here */
} Node;

static Node *new_node(void) {
    Node *n = malloc(sizeof *n);
    if (n) { n->c[0] = n->c[1] = NULL; n->hop = -1; }
    return n;
}
bool trie_insert(Node *root, uint32_t prefix, unsigned len, int hop) {
    /* len <= 32 */
    Node *t = root;
    for (unsigned i = 0; i < len; i++) {
        unsigned bit = (prefix >> (31 - i)) & 1u;
        if (!t->c[bit] && !(t->c[bit] = new_node())) return false;
        t = t->c[bit];
    }
    t->hop = hop;
    return true;
}
int trie_lookup(const Node *root, uint32_t addr) {
    int best = root->hop;  /* the default route /0, if any */
    const Node *t = root;
    for (unsigned i = 0; i < 32 && t; i++) {
        t = t->c[(addr >> (31 - i)) & 1u];
        if (t && t->hop >= 0) best = t->hop;   /* longer match found */
    }
    return best;  /* -1: no matching prefix */
}
```

*Complexity.* Insert O(*p*), lookup O(32), independent of the table size *n*. The memory is at most 32 nodes per prefix in the worst case, and typically far fewer because prefixes share their upper bits. A linear scan of all prefixes costs O(*n*) per lookup, which is the baseline this structure replaces.

**Multibit tries.** Reading eight bits per level (a *stride* of 8) needs only four steps for IPv4, at the cost of nodes with 256 children. Figure 1.15 draws such a trie for four prefixes. Real routers go further: they use compressed tries or TCAM hardware (the device internals are treated in Pillar 5, §5.2.8). The software alternative to a trie is one hash table per prefix length: probe the /32 table, then /31, and so on, down to /0, and keep the first hit; this costs up to 32 hash lookups but needs no pointer chasing.

<figure>
<svg viewBox="0 0 440 222" width="475"><defs><marker id="a6" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#1A1D23"/></marker><marker id="a6b" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#3D55A8"/></marker></defs>
<rect class="box" x="20" y="60" width="50" height="26" rx="2"/><text class="lbl" x="45" y="77" text-anchor="middle">root</text><rect class="box" x="120" y="60" width="50" height="26" rx="2" style="fill:#FFF4C2"/><text class="mono" x="145" y="77" text-anchor="middle">10</text><text class="sm" x="145" y="100" text-anchor="middle">/8 → hopA</text><rect class="box" x="220" y="60" width="50" height="26" rx="2" style="fill:#FFF4C2"/><text class="mono" x="245" y="77" text-anchor="middle">1</text><text class="sm" x="245" y="100" text-anchor="middle">/16 → hopB</text><rect class="box" x="320" y="60" width="50" height="26" rx="2" style="fill:#FFF4C2"/><text class="mono" x="345" y="77" text-anchor="middle">2</text><text class="sm" x="345" y="100" text-anchor="middle">/24 → hopC</text><rect class="box" x="120" y="130" width="50" height="26" rx="2"/><text class="mono" x="145" y="147" text-anchor="middle">192</text><rect class="box" x="220" y="130" width="50" height="26" rx="2"/><text class="mono" x="245" y="147" text-anchor="middle">168</text><text class="sm" x="245" y="170" text-anchor="middle">/16 → hopD</text><line class="ln" x1="70" y1="73" x2="120" y2="73"/><line class="ln" x1="170" y1="73" x2="220" y2="73"/><line class="ln" x1="270" y1="73" x2="320" y2="73"/><line class="ln" x1="70" y1="80" x2="120" y2="143"/><line class="ln" x1="170" y1="143" x2="220" y2="143"/><path class="acc" d="M45,60 Q95,38 145,58 M170,58 Q205,40 245,58 M270,58 Q305,40 345,58" marker-end="url(#a6b)"/><text class="sm" x="20" y="195" text-anchor="start">10.1.2.77: octets 10, 1, 2 all exist; deepest mark /24 → hopC.</text><text class="sm" x="20" y="210" text-anchor="start">10.1.9.9: 9 is absent under 1; deepest mark /16 → hopB.  10.200.0.1: 200 absent under 10; /8 → hopA.</text>
</svg>
<figcaption><b>Figure 1.15</b> A stride-8 trie (one level per octet) for 10.0.0.0/8, 10.1.0.0/16, 10.1.2.0/24 and 192.168.0.0/16. The accent walk is the lookup of 10.1.2.77.</figcaption>
</figure>

::: example
**Lookup in a table of four prefixes and a default route.** Routes: 10.0.0.0/8 → A, 10.1.0.0/16 → B, 10.1.2.0/24 → C, 192.168.0.0/16 → D, 0.0.0.0/0 → E.

1. Insert each prefix: the /8 path has 8 edges and marks hop A; the /16 path shares those 8 edges and extends by 8 more; the /24 extends by 8 more again.
2. Look up 10.1.2.77. The first 8 bits (10) reach the node marked A, the next 8 (1) reach the node marked B, the next 8 (2) reach the node marked C, and no further route exists. The last mark seen is C.
3. Look up 10.1.9.9. The walk reaches B after 16 bits; the third octet 9 = `00001001` leaves the path of 10.1.2.0/24 (third octet `00000010`) at its fifth bit. The last mark seen is B.
4. Look up 10.200.0.1 → A (leaves the 10.1 path at the ninth bit). Look up 172.16.0.1: the walk follows the first bit (1) shared with 192.168.0.0/16 and leaves that path at the second bit, having passed no mark, so only the default route E matches.

| Address | Deepest mark on the walk | Next hop |
|---|---|---|
| 10.1.2.77 | /24 | C |
| 10.1.9.9 | /16 | B |
| 10.200.0.1 | /8 | A |
| 172.16.0.1 | /0 | E |

[Result: lookups touch at most 32 nodes whatever the table size; the answer is the last mark seen.]{.result}
:::

::: trap
*Claim:* stop the lookup at the first node that carries a next hop. *Why it is wrong:* a shorter prefix such as 10.0.0.0/8 is met before the longer 10.1.2.0/24, so stopping early returns the least specific route. *Correct statement:* keep walking while edges exist and remember the deepest marked node; return it when the walk ends.
:::

Deleting a prefix clears the hop at its node and removes any chain of childless, unmarked nodes below the last useful ancestor. For text keys the same code applies with 26 children per node and an `end` flag in place of `hop`; "implement a trie" and "maximum XOR of two numbers" (a binary trie of the numbers' bits, queried greedily for the opposite bit) are solved in the Problem Set.

**Choosing a lookup structure.** The binary trie is the baseline; every other method trades memory, update cost or hardware for speed. A *path-compressed* trie (a Patricia or radix tree) merges chains of single-child nodes into one edge labelled with the skipped bits, so the number of nodes is proportional to the number of prefixes instead of the number of bits.

| Method | Lookup | Memory | Updates | Where used |
|---|---|---|---|---|
| linear scan of prefixes | O(*n*) | O(*n*) | trivial | tiny tables, tests |
| binary trie | O(32) steps | up to 32 nodes per prefix | easy | teaching, software routers |
| path-compressed trie | O(32) steps, fewer nodes | O(*n*) | moderate | Linux and BSD routing tables |
| multibit trie (stride 8) | 4 steps | large nodes, 256 pointers | prefix expansion | high-speed software |
| hash per prefix length | up to 33 probes | O(*n*) | easy | simple fast paths |
| TCAM | one clock cycle | expensive, power-hungry | slow, ordered by length | hardware line cards |

::: lens
[GOOGLE · CISCO · JUNIPER · ARISTA]{.co}

The reported form is: "given a list of IP prefixes and a target address, find the longest matching prefix; which data structure, and what is the lookup complexity?" A strong answer names the binary trie, states O(32) per lookup, explains why a hash set of prefixes needs up to 32 probes, and mentions that hardware uses TCAM. Follow-ups: deletion, memory use, updating the table while lookups continue, IPv6 (128 levels, hence compression).
:::

::: lab
`LAB 1.9 · 30 MIN` Build the trie above into a small lookup engine and measure it against a linear scan. Append this `main` to the code of this section (with `<stdio.h>` and `<time.h>`), save the result as `minifib.c`, compile with optimisation, and run.

```c
int main(void) {
    enum { N = 20000, Q = 1000000, L = 2000 };
    static uint32_t pre[N], qa[L]; static unsigned len[N];
    Node *root = new_node();
    srand(1);
    for (int i = 0; i < N; i++) {
        len[i] = 8 + rand() % 17;                          /* /8 .. /24 */
        pre[i] = ((uint32_t)rand() << 16) ^ (uint32_t)rand();
        pre[i] &= ~0u << (32 - len[i]);
        trie_insert(root, pre[i], len[i], i);
    }
    for (int i = 0; i < L; i++)
        qa[i] = ((uint32_t)rand() << 16) ^ (uint32_t)rand();

    clock_t t0 = clock(); long agree = 0;
    for (int q = 0; q < L; q++) {  /* linear scan */
        int best = -1; unsigned bl = 0;
        for (int i = 0; i < N; i++)
            if (len[i] >= bl &&
                (qa[q] >> (32 - len[i])) == (pre[i] >> (32 - len[i])))
                best = i, bl = len[i];
        agree += (best == trie_lookup(root, qa[q]));
    }
    double ls = (double)(clock() - t0) / CLOCKS_PER_SEC;
    printf("linear: %d lookups in %.3f s (%.2f M/s), trie agrees on %ld\n",
           L, ls, L / ls / 1e6, agree);

    t0 = clock(); long sum = 0;
    for (int q = 0; q < Q; q++)
        sum += trie_lookup(root,
                   ((uint32_t)rand() << 16) ^ (uint32_t)rand());
    double ts = (double)(clock() - t0) / CLOCKS_PER_SEC;
    printf("trie  : %d lookups in %.3f s (%.2f M/s)  check %ld\n",
           Q, ts, Q / ts / 1e6, sum);
    return 0;
}
```

```
$ gcc -O2 -Wall -o minifib minifib.c && ./minifib
linear: 2000 lookups in 0.105 s (0.02 M/s), trie agrees on 2000
trie  : 1000000 lookups in 0.133 s (7.52 M/s)  check 11280283566
```

**What you should notice:** the trie answers about 300 times faster than the scan, and the two agree on every query, which is the correctness check. The scan examines all *N* prefixes per lookup; the trie walks at most 32 nodes. Change `N` to 200000 and rerun: the scan becomes ten times slower, as its cost is proportional to *N*, while the trie slows only from roughly 7.5 to 1.6 million lookups per second on the machine used here, because a larger trie no longer fits in the processor cache and each step of the walk becomes a slow dependent memory load. The figures depend on the machine; the ratio and the trend are what to look for.
:::

::: check
1. How many nodes does a binary trie contain after inserting only 10.0.0.0/8? [^c1-18]
2. Why is lookup time independent of the number of prefixes? [^c1-19]
:::

[^c1-18]: Nine: the root and one node per bit of the prefix, eight in all.
[^c1-19]: The walk consumes one address bit per step and stops after at most 32 steps, whatever else the trie holds.

## [1.10]{.sec}Heaps and priority queues [Should · ■■□]{.tag} {#s1-10}

::: bigidea
A heap keeps the smallest (or largest) element at the front of a partially ordered array, so that the extreme can be read at once and replaced in logarithmic time, which suits "the best k so far".
:::

A *binary min-heap* is a complete binary tree in which every parent is no larger than its children. Because the tree is complete, it is stored in an array with no pointers: the children of index *i* are `2i+1` and `2i+2`, and its parent is `(i-1)/2`.

<figure>
<svg viewBox="0 0 440 215" width="475">
<line class="ln" x1="240" y1="26" x2="150" y2="70"/><line class="ln" x1="240" y1="26" x2="330" y2="70"/><line class="ln" x1="150" y1="70" x2="105" y2="114"/><line class="ln" x1="150" y1="70" x2="195" y2="114"/><line class="ln" x1="330" y1="70" x2="285" y2="114"/><line class="ln" x1="330" y1="70" x2="375" y2="114"/><circle class="box" cx="240" cy="26" r="12"/><text class="lbl" x="240" y="29" text-anchor="middle">2</text><circle class="box" cx="150" cy="70" r="12" style="fill:#FFF4C2"/><text class="lbl" x="150" y="73" text-anchor="middle">5</text><circle class="box" cx="330" cy="70" r="12"/><text class="lbl" x="330" y="73" text-anchor="middle">3</text><circle class="box" cx="105" cy="114" r="12" style="fill:#FFF4C2"/><text class="lbl" x="105" y="117" text-anchor="middle">9</text><circle class="box" cx="195" cy="114" r="12" style="fill:#FFF4C2"/><text class="lbl" x="195" y="117" text-anchor="middle">6</text><circle class="box" cx="285" cy="114" r="12"/><text class="lbl" x="285" y="117" text-anchor="middle">8</text><circle class="box" cx="375" cy="114" r="12"/><text class="lbl" x="375" y="117" text-anchor="middle">4</text><rect class="box" style="fill:none" x="90" y="150" width="40" height="24"/>
<text class="mono" x="110.0" y="165.0" text-anchor="middle">2</text>
<text class="sm" x="110.0" y="184" text-anchor="middle">0</text>
<rect class="box" style="fill:none" x="130" y="150" width="40" height="24"/>
<text class="mono" x="150.0" y="165.0" text-anchor="middle">5</text>
<text class="sm" x="150.0" y="184" text-anchor="middle">1</text>
<rect class="box" style="fill:none" x="170" y="150" width="40" height="24"/>
<text class="mono" x="190.0" y="165.0" text-anchor="middle">3</text>
<text class="sm" x="190.0" y="184" text-anchor="middle">2</text>
<rect class="box" style="fill:none" x="210" y="150" width="40" height="24"/>
<text class="mono" x="230.0" y="165.0" text-anchor="middle">9</text>
<text class="sm" x="230.0" y="184" text-anchor="middle">3</text>
<rect class="box" style="fill:none" x="250" y="150" width="40" height="24"/>
<text class="mono" x="270.0" y="165.0" text-anchor="middle">6</text>
<text class="sm" x="270.0" y="184" text-anchor="middle">4</text>
<rect class="box" style="fill:none" x="290" y="150" width="40" height="24"/>
<text class="mono" x="310.0" y="165.0" text-anchor="middle">8</text>
<text class="sm" x="310.0" y="184" text-anchor="middle">5</text>
<rect class="box" style="fill:none" x="330" y="150" width="40" height="24"/>
<text class="mono" x="350.0" y="165.0" text-anchor="middle">4</text>
<text class="sm" x="350.0" y="184" text-anchor="middle">6</text><text class="sm" x="20" y="166" text-anchor="start">array</text><text class="sm" x="20" y="205" text-anchor="start">parent(i) = (i-1)/2;  left(i) = 2i+1;  right(i) = 2i+2.  Index 1 (value 5) has children 3 and 4.</text>
</svg>
<figcaption><b>Figure 1.16</b> A min-heap as a tree and as the array that stores it. No pointers are needed because the shape is always a complete tree.</figcaption>
</figure>

`push` appends at the end and swaps upward while smaller than the parent (sift-up); `pop` moves the last element to the root and swaps downward with the smaller child (sift-down). Each follows one root-to-leaf path, so both cost O(log *n*), and reading the minimum costs O(1). Building a heap from *n* elements by sifting down from the middle takes O(*n*), not O(*n* log *n*), because most nodes lie near the leaves.

*Recognise:* "k largest or smallest", "k most frequent", "merge k sorted", "median of a stream", "next event by time", "reorder packets by sequence number". In C++ `priority_queue<int>` is a max-heap; for a min-heap pass `greater<int>`. Python's `heapq` is a min-heap; negate values for a max-heap.

```cpp
vector<int> topK(const vector<int>& a, int k) {  // the k largest, ascending
    priority_queue<int, vector<int>, greater<int>> h;  // min-heap of k
    for (int x : a) {
        h.push(x);
        if ((int)h.size() > k) h.pop();  // discard the smallest
    }
    vector<int> out;
    while (!h.empty()) { out.push_back(h.top()); h.pop(); }
    return out;
}
```

The heap holds the *k* best seen so far; its root is the weakest of them, which is the one to evict. For `[3, 1, 5, 12, 2, 11]` and *k* = 3 the heap evolves as {3}, {1,3}, {1,3,5}, then 12 arrives and 1 is evicted giving {3,5,12}, then 2 arrives and is itself evicted, then 11 evicts 3, giving {5,11,12}. The cost is O(*n* log *k*) time and O(*k*) space. For the median of a stream, a max-heap holds the lower half and a min-heap the upper half, rebalanced so that their sizes differ by at most one; the median is at one of the two roots (Problem Set).

The library hides the two moves; in C they are written by hand on a plain array, and an interviewer may ask for them.

```c
static void swap_int(int *a, int *b) { int t = *a; *a = *b; *b = t; }

static void sift_up(int *a, size_t i) {
    while (i && a[(i - 1) / 2] > a[i]) {
        swap_int(&a[(i - 1) / 2], &a[i]);
        i = (i - 1) / 2;
    }
}
static void sift_down(int *a, size_t n, size_t i) {
    for (;;) {
        size_t l = 2 * i + 1, r = l + 1, m = i;
        if (l < n && a[l] < a[m]) m = l;
        if (r < n && a[r] < a[m]) m = r;
        if (m == i) return;
        swap_int(&a[i], &a[m]);
        i = m;
    }
}
void heap_push(int *a, size_t *n, int v) {
    a[(*n)++] = v;
    sift_up(a, *n - 1);
}
int  heap_pop(int *a, size_t *n) {                /* requires *n > 0 */
    int top = a[0];
    a[0] = a[--*n];
    sift_down(a, *n, 0);
    return top;
}
```

Pushing 5, 3, 8, 1 gives `[5]`, `[3, 5]`, `[3, 5, 8]`, and then 1 is appended at index 3 and moves up past its parent 5 and past 3, leaving `[1, 3, 8, 5]`. A pop returns 1, moves the last element 5 to the root, and sifts it down: the smaller child is 3, so the heap becomes `[3, 5, 8]`. Repeatedly popping a heap built from an array sorts it in O(*n* log *n*) time and O(1) extra space; this is heapsort.

::: trap
*Claim:* use a max-heap of size *k* to keep the *k* largest values. *Why it is wrong:* the root of a max-heap is the largest element, but the element to evict is the smallest of the kept ones. *Correct statement:* keep the *k* largest in a min-heap, and the *k* smallest in a max-heap.
:::

:::
