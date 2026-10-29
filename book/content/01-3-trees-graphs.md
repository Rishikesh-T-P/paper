::: {.p1}

## [1.8]{.sec}Trees and binary search trees [Must · ■■□]{.tag} {#s1-8}

::: bigidea
A binary search tree keeps its keys ordered so that each comparison discards a whole subtree, giving search in time proportional to the height, which is logarithmic only while the tree stays balanced.
:::

A *binary tree* is a node with at most two children; a *binary search tree* (BST) adds the rule that every key in the left subtree is smaller than the node and every key in the right subtree is larger. The *height* *h* is the number of edges on the longest root-to-leaf path. Search, insert and delete each follow one path, so they cost O(*h*). For *n* random keys *h* is about 2 log *n*, but inserting sorted keys produces a chain with *h* = *n*, and every operation degrades to O(*n*). Self-balancing trees (AVL, red-black) restore O(log *n*); C++ `std::map` and `std::set` are red-black trees.

<figure>
<svg viewBox="0 0 480 192" width="480">
<line class="ln" x1="240" y1="28" x2="140" y2="70"/><line class="ln" x1="240" y1="28" x2="340" y2="70"/><line class="ln" x1="140" y1="70" x2="90" y2="112"/><line class="ln" x1="140" y1="70" x2="190" y2="112"/><line class="ln" x1="340" y1="70" x2="390" y2="112"/><line class="ln" x1="190" y1="112" x2="160" y2="154"/><line class="ln" x1="190" y1="112" x2="220" y2="154"/><line class="ln" x1="390" y1="112" x2="360" y2="154"/><circle class="box" cx="240" cy="28" r="12" style="fill:#FFF4C2"/><text class="lbl" x="240" y="31" text-anchor="middle">8</text><circle class="box" cx="140" cy="70" r="12" style="fill:#FFF4C2"/><text class="lbl" x="140" y="73" text-anchor="middle">3</text><circle class="box" cx="340" cy="70" r="12"/><text class="lbl" x="340" y="73" text-anchor="middle">10</text><circle class="box" cx="90" cy="112" r="12"/><text class="lbl" x="90" y="115" text-anchor="middle">1</text><circle class="box" cx="190" cy="112" r="12" style="fill:#FFF4C2"/><text class="lbl" x="190" y="115" text-anchor="middle">6</text><circle class="box" cx="390" cy="112" r="12"/><text class="lbl" x="390" y="115" text-anchor="middle">14</text><circle class="box" cx="160" cy="154" r="12" style="fill:#FFF4C2"/><text class="lbl" x="160" y="157" text-anchor="middle">4</text><circle class="box" cx="220" cy="154" r="12"/><text class="lbl" x="220" y="157" text-anchor="middle">7</text><circle class="box" cx="360" cy="154" r="12"/><text class="lbl" x="360" y="157" text-anchor="middle">13</text><text class="sm" x="20" y="180" text-anchor="start">search 4: 4 &lt; 8 left, 4 > 3 right, 4 &lt; 6 left, found (4 comparisons). In-order: 1 3 4 6 7 8 10 13 14</text>
</svg>
<figcaption><b>Figure 1.7</b> A binary search tree. Everything left of a node is smaller and everything right is larger; the highlighted path is the search for 4.</figcaption>
</figure>

### Traversals

Depth-first traversals differ only in when the node is visited: *pre-order* (node, left, right), *in-order* (left, node, right) and *post-order* (left, right, node). The in-order traversal of a BST yields the keys in sorted order, which is the fact behind "k-th smallest" and "validate BST". Breadth-first traversal visits level by level with a queue. *Recognise:* "depth", "path", "subtree" (DFS, usually post-order, returning information to the parent); "level", "right side view", "shortest" (BFS); "sorted", "k-th", "validate" (in-order).

```cpp
struct TreeNode { int val; TreeNode *left = nullptr, *right = nullptr; };

int height(TreeNode* t) { return t ? 1 + max(height(t->left), height(t->right)) : 0; }   // nodes on longest path

vector<int> inorderIter(TreeNode* root) {              // no recursion: explicit stack
    vector<int> out; vector<TreeNode*> st; TreeNode* cur = root;
    while (cur || !st.empty()) {
        while (cur) { st.push_back(cur); cur = cur->left; }   // go as far left as possible
        cur = st.back(); st.pop_back();
        out.push_back(cur->val);
        cur = cur->right;
    }
    return out;
}

vector<vector<int>> levelOrder(TreeNode* root) {
    vector<vector<int>> res; if (!root) return res;
    queue<TreeNode*> q; q.push(root);
    while (!q.empty()) {
        int sz = q.size(); res.emplace_back();            // sz = nodes on this level
        while (sz--) {
            TreeNode* t = q.front(); q.pop();
            res.back().push_back(t->val);
            if (t->left) q.push(t->left);
            if (t->right) q.push(t->right);
        }
    }
    return res;
}
```

All three run in O(*n*) time. Their space is O(*h*) for the explicit stack and O(*width*) for the queue. A skewed tree of 10^6 nodes also overflows the call stack of the recursive `height`, which is the reason for asking in an interview whether the tree may be skewed.

### BST operations in C

Insert and delete return the root of the (possibly changed) subtree, and the caller stores the result back into its link. Forgetting to return or store it is the standard delete bug.

```c
typedef struct T { int key; struct T *l, *r; } T;

T *bst_insert(T *t, int k) {
    if (!t) { t = calloc(1, sizeof *t); if (t) t->key = k; return t; }
    if (k < t->key)      t->l = bst_insert(t->l, k);
    else if (k > t->key) t->r = bst_insert(t->r, k);
    return t;                                       /* duplicates are ignored */
}
const T *bst_search(const T *t, int k) {
    while (t && t->key != k) t = k < t->key ? t->l : t->r;
    return t;
}
static T *min_node(T *t) { while (t->l) t = t->l; return t; }

T *bst_delete(T *t, int k) {
    if (!t) return NULL;
    if (k < t->key)      t->l = bst_delete(t->l, k);
    else if (k > t->key) t->r = bst_delete(t->r, k);
    else {
        if (!t->l || !t->r) {                       /* zero or one child */
            T *child = t->l ? t->l : t->r;
            free(t);
            return child;                           /* parent adopts the child */
        }
        T *s = min_node(t->r);                      /* in-order successor */
        t->key = s->key;
        t->r = bst_delete(t->r, s->key);
    }
    return t;
}
```

Deletion has three cases: a leaf is removed; a node with one child is replaced by that child; a node with two children takes the key of its in-order successor (the smallest key of the right subtree), and the successor, which has no left child, is then deleted by one of the first two cases.

::: example
**Delete 3 from the tree of Figure 1.7.**

1. Search: 3 < 8, so go left and find the node 3.
2. It has two children (1 and 6), so find the successor: the left-most node of the right subtree, `6 → 4`. The successor is 4.
3. Copy 4 into the node, so the node now holds 4.
4. Delete 4 from the right subtree. The node 4 is a leaf, so it is removed and the left link of 6 becomes `NULL`.
5. The in-order sequence is now 1 4 6 7 8 10 13 14: still sorted, with 3 removed.

[Result: the node 3 now holds 4, and the old leaf 4 is gone.]{.result}
:::

### Validating a BST

Checking each node only against its parent is wrong, since a node deep in the right subtree may still be smaller than an ancestor. We pass down the open interval that each key must lie in.

```cpp
bool valid(TreeNode* t, long long lo, long long hi) {      // lo < key < hi
    return !t || (lo < t->val && t->val < hi &&
                  valid(t->left, lo, t->val) && valid(t->right, t->val, hi));
}
// call: valid(root, LLONG_MIN, LLONG_MAX)
```

::: trap
*Claim:* a tree is a BST if every node is greater than its left child and smaller than its right child. *Why it is wrong:* the tree 5 with left child 1 and right child 6, where 6 has left child 4, satisfies the local rule but 4 sits in the right subtree of 5. *Correct statement:* every key must lie between the bounds inherited from all its ancestors, or the in-order sequence must be strictly increasing.
:::

::: check
1. What is the height of the BST built by inserting 1, 2, 3, 4, 5 in order? [^c1-16]
2. Which traversal prints a BST in sorted order? [^c1-17]
:::

[^c1-16]: 4 edges (5 nodes): each key becomes the right child of the previous one, so operations cost O(*n*).
[^c1-17]: In-order (left, node, right).

## [1.9]{.sec}Tries and longest-prefix match [Must · ■■■]{.tag} {#s1-9}

::: bigidea
A router forwards a packet along the most specific route that contains its destination, and a trie finds that route by reading the address one bit at a time, in a number of steps bounded by the address length and independent of the number of routes.
:::

A *trie* (prefix tree) stores a set of strings along the edges of a tree: the path from the root spells the string, and a flag on a node marks that a stored string ends there. Lookup costs O(*L*) for a key of length *L*, regardless of how many keys are stored. *Recognise:* "words with this prefix", "autocomplete", "longest common prefix", "maximum XOR", and above all "longest prefix match" on IP addresses.

**The routing problem.** A forwarding table maps *prefixes* to next hops. A prefix `10.1.0.0/16` matches every address whose first 16 bits equal those of 10.1.0.0. Prefixes overlap: an address in 10.1.2.0/24 also lies in 10.1.0.0/16 and in 10.0.0.0/8. The forwarding rule is that the matching prefix with the greatest length wins, termed *longest-prefix match* (LPM), because the longer prefix is the more specific route. (Why routers need this, and how routes are learned, is taught in the routing chapter; here we implement the lookup.)

**Binary trie.** We treat a 32-bit address as a string over {0, 1}, with one level per bit. Inserting a prefix of length *p* follows (and creates) *p* edges and stores the next hop at the final node. A lookup follows the address bits from the root and records the next hop of every marked node it passes; when the next edge is missing, the last recorded hop is the longest match.

<figure>
<svg viewBox="0 0 480 200" width="480">
<line class="ln" x1="240" y1="24" x2="140" y2="64"/><text class="sm" x="182.0" y="42.0" text-anchor="middle">0</text><line class="ln" x1="240" y1="24" x2="340" y2="64"/><text class="sm" x="298.0" y="42.0" text-anchor="middle">1</text><line class="ln" x1="140" y1="64" x2="200" y2="104"/><text class="sm" x="178.0" y="82.0" text-anchor="middle">1</text><line class="ln" x1="200" y1="104" x2="260" y2="144"/><text class="sm" x="238.0" y="122.0" text-anchor="middle">1</text><line class="ln" x1="260" y1="144" x2="300" y2="184"/><text class="sm" x="272.0" y="162.0" text-anchor="middle">0</text><circle class="box" cx="240" cy="24" r="11" style="fill:#fff"/><circle class="box" cx="140" cy="64" r="11" style="fill:#FFF4C2"/><text class="lbl" x="140" y="67" text-anchor="middle">A</text><circle class="box" cx="340" cy="64" r="11" style="fill:#FFF4C2"/><text class="lbl" x="340" y="67" text-anchor="middle">D</text><circle class="box" cx="200" cy="104" r="11" style="fill:#FFF4C2"/><text class="lbl" x="200" y="107" text-anchor="middle">B</text><circle class="box" cx="260" cy="144" r="11" style="fill:#fff"/><circle class="box" cx="300" cy="184" r="11" style="fill:#FFF4C2"/><text class="lbl" x="300" y="187" text-anchor="middle">C</text><text class="sm" x="20" y="60" text-anchor="start">Prefixes (4-bit toy):</text><text class="mono" x="20" y="74" text-anchor="start">0*  → A</text><text class="mono" x="20" y="86" text-anchor="start">01* → B</text><text class="mono" x="20" y="98" text-anchor="start">0110 → C</text><text class="mono" x="20" y="110" text-anchor="start">1*  → D</text><text class="sm" x="360" y="150" text-anchor="start">lookup 0111:</text><text class="sm" x="360" y="164" text-anchor="start">0 (A), 1 (B), 1, then no 0/1 child</text><text class="lbl" x="360" y="178" text-anchor="start">last mark seen = B</text>
</svg>
<figcaption><b>Figure 1.8</b> A binary trie for four toy prefixes. A shaded node carries a next hop; a lookup walks the address bits and remembers the deepest shaded node it passed.</figcaption>
</figure>

```c
#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct Node { struct Node *c[2]; int hop; } Node;   /* hop < 0: no route here */

static Node *new_node(void) {
    Node *n = malloc(sizeof *n);
    if (n) { n->c[0] = n->c[1] = NULL; n->hop = -1; }
    return n;
}
bool trie_insert(Node *root, uint32_t prefix, unsigned len, int hop) {   /* len <= 32 */
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
    int best = root->hop;                         /* the default route /0, if any */
    const Node *t = root;
    for (unsigned i = 0; i < 32 && t; i++) {
        t = t->c[(addr >> (31 - i)) & 1u];
        if (t && t->hop >= 0) best = t->hop;      /* a longer match than before */
    }
    return best;                                  /* -1: no matching prefix */
}
```

*Complexity.* Insert O(*p*), lookup O(32), independent of the table size *n*. The memory is at most 32 nodes per prefix in the worst case, and typically far fewer because prefixes share their upper bits. A linear scan of all prefixes costs O(*n*) per lookup, which is the baseline this structure replaces.

**Multibit tries.** Reading eight bits per level (a *stride* of 8) needs only four steps for IPv4, at the cost of nodes with 256 children. Figure 1.9 draws such a trie for four prefixes. Real routers go further: they use compressed tries or TCAM hardware (the device internals are treated in Pillar 5, §5.2.8). The software alternative to a trie is one hash table per prefix length: probe the /32 table, then /31, and so on, down to /0, and keep the first hit; this costs up to 32 hash lookups but needs no pointer chasing.

<figure>
<svg viewBox="0 0 480 222" width="480"><defs><marker id="a6" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#1A1D23"/></marker><marker id="a6b" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#3D55A8"/></marker></defs>
<rect class="box" x="20" y="60" width="50" height="26" rx="2"/><text class="lbl" x="45" y="77" text-anchor="middle">root</text><rect class="box" x="120" y="60" width="50" height="26" rx="2" style="fill:#FFF4C2"/><text class="mono" x="145" y="77" text-anchor="middle">10</text><text class="sm" x="145" y="100" text-anchor="middle">/8 → hopA</text><rect class="box" x="220" y="60" width="50" height="26" rx="2" style="fill:#FFF4C2"/><text class="mono" x="245" y="77" text-anchor="middle">1</text><text class="sm" x="245" y="100" text-anchor="middle">/16 → hopB</text><rect class="box" x="320" y="60" width="50" height="26" rx="2" style="fill:#FFF4C2"/><text class="mono" x="345" y="77" text-anchor="middle">2</text><text class="sm" x="345" y="100" text-anchor="middle">/24 → hopC</text><rect class="box" x="120" y="130" width="50" height="26" rx="2"/><text class="mono" x="145" y="147" text-anchor="middle">192</text><rect class="box" x="220" y="130" width="50" height="26" rx="2"/><text class="mono" x="245" y="147" text-anchor="middle">168</text><text class="sm" x="245" y="170" text-anchor="middle">/16 → hopD</text><rect class="box" x="220" y="20" width="50" height="22" rx="2"/><text class="mono" x="245" y="35" text-anchor="middle">9</text><text class="sm" x="300" y="35" text-anchor="start">10.9/16: none</text><line class="ln" x1="70" y1="73" x2="120" y2="73"/><line class="ln" x1="170" y1="73" x2="220" y2="73"/><line class="ln" x1="270" y1="73" x2="320" y2="73"/><line class="ln" x1="70" y1="80" x2="120" y2="143"/><line class="ln" x1="170" y1="143" x2="220" y2="143"/><line class="ln" x1="170" y1="66" x2="220" y2="31"/><path class="acc" d="M45,60 Q95,38 145,58 M170,58 Q205,40 245,58 M270,58 Q305,40 345,58" marker-end="url(#a6b)"/><text class="sm" x="20" y="195" text-anchor="start">lookup 10.1.2.77: 10, 1, 2 all exist, deepest mark /24 → hopC.   lookup 10.1.9.9: 9 absent under 1, deepest mark seen /16 → hopB.</text><text class="sm" x="20" y="210" text-anchor="start">lookup 10.200.0.1: 200 absent under 10, deepest mark /8 → hopA.</text>
</svg>
<figcaption><b>Figure 1.9</b> A stride-8 trie (one level per octet) for 10.0.0.0/8, 10.1.0.0/16, 10.1.2.0/24 and 192.168.0.0/16. The accent walk is the lookup of 10.1.2.77.</figcaption>
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

::: lens
[GOOGLE · CISCO · JUNIPER · ARISTA]{.co}

The reported form is: "given a list of IP prefixes and a target address, find the longest matching prefix; which data structure, and what is the lookup complexity?" A strong answer names the binary trie, states O(32) per lookup, explains why a hash set of prefixes needs up to 32 probes, and mentions that hardware uses TCAM. Follow-ups: deletion, memory use, updating the table while lookups continue, IPv6 (128 levels, hence compression).
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
<svg viewBox="0 0 480 215" width="480">
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
<text class="sm" x="350.0" y="184" text-anchor="middle">6</text><text class="sm" x="20" y="166" text-anchor="start">array</text><text class="sm" x="20" y="205" text-anchor="start">parent(i) = (i-1)/2     left(i) = 2i+1     right(i) = 2i+2.   Children of index 1 (value 5) are indices 3 and 4.</text>
</svg>
<figcaption><b>Figure 1.10</b> A min-heap as a tree and as the array that stores it. No pointers are needed because the shape is always a complete tree.</figcaption>
</figure>

`push` appends at the end and swaps upward while smaller than the parent (sift-up); `pop` moves the last element to the root and swaps downward with the smaller child (sift-down). Each follows one root-to-leaf path, so both cost O(log *n*), and reading the minimum costs O(1). Building a heap from *n* elements by sifting down from the middle takes O(*n*), not O(*n* log *n*), because most nodes lie near the leaves.

*Recognise:* "k largest or smallest", "k most frequent", "merge k sorted", "median of a stream", "next event by time", "reorder packets by sequence number". In C++ `priority_queue<int>` is a max-heap; for a min-heap pass `greater<int>`. Python's `heapq` is a min-heap; negate values for a max-heap.

```cpp
vector<int> topK(const vector<int>& a, int k) {              // the k largest, ascending
    priority_queue<int, vector<int>, greater<int>> h;         // min-heap of size <= k
    for (int x : a) {
        h.push(x);
        if ((int)h.size() > k) h.pop();                       // discard the smallest
    }
    vector<int> out;
    while (!h.empty()) { out.push_back(h.top()); h.pop(); }
    return out;
}
```

The heap holds the *k* best seen so far; its root is the weakest of them, which is the one to evict. For `[3, 1, 5, 12, 2, 11]` and *k* = 3 the heap evolves as {3}, {1,3}, {1,3,5}, then 12 arrives and 1 is evicted giving {3,5,12}, then 2 arrives and is itself evicted, then 11 evicts 3, giving {5,11,12}. The cost is O(*n* log *k*) time and O(*k*) space. For the median of a stream, a max-heap holds the lower half and a min-heap the upper half, rebalanced so that their sizes differ by at most one; the median is at one of the two roots (Problem Set).

::: trap
*Claim:* use a max-heap of size *k* to keep the *k* largest values. *Why it is wrong:* the root of a max-heap is the largest element, but the element to evict is the smallest of the kept ones. *Correct statement:* keep the *k* largest in a min-heap, and the *k* smallest in a max-heap.
:::

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

### Breadth-first and depth-first search

BFS explores in rings of increasing hop count, using a queue, so the first time it reaches a vertex is by a shortest path. Marking a vertex visited when it is *pushed* (not when it is popped) keeps duplicates out of the queue. DFS follows one path as deep as it goes, using a stack, and is the tool for connectivity, cycles and ordering. The iterative form avoids the recursion limit (about 1000 in Python, and the stack size in C).

```cpp
vector<int> bfs(const vector<vector<int>>& g, int src) {      // hop distance, -1 if unreachable
    vector<int> dist(g.size(), -1);
    queue<int> q; dist[src] = 0; q.push(src);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : g[u])
            if (dist[v] < 0) { dist[v] = dist[u] + 1; q.push(v); }   // visited on push
    }
    return dist;
}

vector<int> dfsOrder(const vector<vector<int>>& g, int s) {  // iterative DFS
    vector<char> seen(g.size(), 0); vector<int> st{s}, order;
    while (!st.empty()) {
        int u = st.back(); st.pop_back();
        if (seen[u]) continue;
        seen[u] = 1; order.push_back(u);
        for (int i = (int)g[u].size() - 1; i >= 0; --i)      // reverse: match recursive order
            if (!seen[g[u][i]]) st.push_back(g[u][i]);
    }
    return order;
}
```

::: trap
*Claim:* a traversal needs no visited set if the graph "looks like a tree". *Why it is wrong:* a single cycle, or a second path to the same vertex, makes the traversal revisit vertices, and on a cycle it never ends. This is a broadcast storm in code form: a frame flooded around a switched loop is never removed. *Correct statement:* mark each vertex when first reached and skip marked vertices.
:::

A grid is a graph whose vertices are cells and whose neighbours are the four adjacent cells; "number of islands" is the count of DFS starts, and "rotting oranges" and "distance to the nearest gate" are BFS started from all sources at once (multi-source BFS). These are in the Problem Set.

### Dijkstra's algorithm

*Idea.* Keep a tentative distance to each vertex. Repeatedly settle the unsettled vertex with the smallest tentative distance, and relax its edges: if going through it improves a neighbour's distance, update it. Because every weight is non-negative, no later path can reach a settled vertex more cheaply, so a settled distance is final. A min-heap supplies the next vertex. Entries are never updated in place; an improved vertex is pushed again, and the older, larger entry is discarded when it surfaces. *Recognise:* "cheapest", "minimum time", "network delay", weights present and non-negative.

<figure>
<svg viewBox="0 0 480 192" width="480">
<line class="ln" x1="50" y1="90" x2="170" y2="40"/><line class="ln" x1="50" y1="90" x2="170" y2="140"/><line class="ln" x1="170" y1="140" x2="170" y2="40"/><line class="ln" x1="170" y1="40" x2="300" y2="90"/><line class="ln" x1="170" y1="140" x2="300" y2="90"/><line class="ln" x1="300" y1="90" x2="420" y2="90"/><rect x="102.0" y="58.0" width="16" height="13" fill="#fff"/><text class="sm" x="110.0" y="68.0" text-anchor="middle">4</text><rect x="102.0" y="108.0" width="16" height="13" fill="#fff"/><text class="sm" x="110.0" y="118.0" text-anchor="middle">1</text><rect x="162.0" y="83.0" width="16" height="13" fill="#fff"/><text class="sm" x="170.0" y="93.0" text-anchor="middle">2</text><rect x="227.0" y="58.0" width="16" height="13" fill="#fff"/><text class="sm" x="235.0" y="68.0" text-anchor="middle">5</text><rect x="227.0" y="108.0" width="16" height="13" fill="#fff"/><text class="sm" x="235.0" y="118.0" text-anchor="middle">8</text><rect x="352.0" y="83.0" width="16" height="13" fill="#fff"/><text class="sm" x="360.0" y="93.0" text-anchor="middle">3</text><circle class="box" cx="50" cy="90" r="13"/><text class="lbl" x="50" y="93" text-anchor="middle">A</text><circle class="box" cx="170" cy="40" r="13"/><text class="lbl" x="170" y="43" text-anchor="middle">B</text><circle class="box" cx="170" cy="140" r="13"/><text class="lbl" x="170" y="143" text-anchor="middle">C</text><circle class="box" cx="300" cy="90" r="13"/><text class="lbl" x="300" y="93" text-anchor="middle">D</text><circle class="box" cx="420" cy="90" r="13"/><text class="lbl" x="420" y="93" text-anchor="middle">E</text><path class="acc" d="M50,90 L170,140 L170,40 L300,90 L420,90" stroke-linejoin="round"/><text class="sm" x="20" y="180" text-anchor="start">shortest path tree from A: A-C-B-D-E with total cost 1+2+5+3 = 11</text>
</svg>
<figcaption><b>Figure 1.11</b> A weighted undirected graph (link costs). The accent path is the shortest route from A to E.</figcaption>
</figure>

```cpp
using Graph = vector<vector<pair<int, int>>>;                 // g[u] = {(v, weight), ...}

vector<long long> dijkstra(const Graph& g, int src) {
    const long long INF = LLONG_MAX / 4;
    vector<long long> dist(g.size(), INF);
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<>> pq;
    dist[src] = 0; pq.push({0, src});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;                            // stale entry
        for (auto [v, w] : g[u])
            if (d + w < dist[v]) { dist[v] = d + w; pq.push({dist[v], v}); }
    }
    return dist;
}
```

::: example
**Shortest paths from A in Figure 1.11.** Edges: A–B 4, A–C 1, C–B 2, B–D 5, C–D 8, D–E 3.

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
vector<long long> bellmanFord(int n, const vector<Edge>& es, int src, int rounds) {
    const long long INF = LLONG_MAX / 4;
    vector<long long> dist(n, INF); dist[src] = 0;
    for (int r = 0; r < rounds; ++r) {                         // rounds <= n - 1
        vector<long long> nxt = dist;                          // use last round's values only
        for (const Edge& e : es)
            if (dist[e.u] < INF && dist[e.u] + e.w < nxt[e.v]) nxt[e.v] = dist[e.u] + e.w;
        dist = nxt;
    }
    return dist;
}
```

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
    return order;                                              // size < n: a cycle exists
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
        if (a == b) return false;                              // already connected: edge closes a loop
        if (sz[a] < sz[b]) swap(a, b);
        p[b] = a; sz[a] += sz[b];
        return true;
    }
};
```

With both optimisations each operation is O(α(*n*)), where α is the inverse Ackermann function, below 5 for any input that fits in memory. Kruskal's minimum spanning tree sorts the edges by weight and adds each edge whose `unite` returns true. Floyd–Warshall computes all pairs with three nested loops, `for k, for i, for j: d[i][j] = min(d[i][j], d[i][k] + d[k][j])`, and the loop over *k* must be outermost.

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

:::
