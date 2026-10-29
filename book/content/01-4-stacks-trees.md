::: {.p1}

## [1.7]{.sec}Stacks, queues, ring buffers and deques [Must · ■■□]{.tag} {#s1-7}

::: bigidea
A stack remembers the most recent unfinished thing and a queue remembers the oldest, and a ring buffer gives a queue of fixed size with no allocation, which is exactly what a network driver needs.
:::

A *stack* is last in, first out: `push`, `pop` and `top` are O(1) on an array with a top index. *Recognise:* nested structure, "undo", "matching", "most recent", expression evaluation. A *queue* is first in, first out and is the engine of breadth-first search and of packet queues. A *deque* allows insertion and removal at both ends in O(1); `std::deque` provides it, and Python's `collections.deque` does the same.

Matching brackets is the model stack problem. Each opening bracket is pushed; each closing bracket must match the top.

```c
bool balanced(const char *s) {
    size_t top = 0;
    char *st = malloc(strlen(s) + 1);
    if (!st) return false;
    bool ok = true;
    for (; *s && ok; s++) {
        switch (*s) {
        case '(': case '[': case '{': st[top++] = *s; break;
        case ')': ok = top && st[--top] == '('; break;
        case ']': ok = top && st[--top] == '['; break;
        case '}': ok = top && st[--top] == '{'; break;
        }
    }
    free(st);
    return ok && top == 0;  /* leftovers mean unclosed brackets */
}
```

### Stacks and queues in C

An array with a top index is the simplest stack. Every operation checks for overflow and underflow and reports it, because the caller, not the language, owns the error. A linked queue keeps pointers to both ends so that `enqueue` at the tail is O(1); with a single pointer it would be O(*n*).

```c
typedef struct { int a[64]; int top; } Stack;  /* top = element count */
bool st_push(Stack *s, int v) {
    if (s->top == 64) return false;
    s->a[s->top++] = v;
    return true;
}
bool st_pop(Stack *s, int *v) {
    if (s->top == 0) return false;
    *v = s->a[--s->top];
    return true;
}

typedef struct { Node *head, *tail; } Queue;      /* Node: list section */
bool enqueue(Queue *q, int v) {
    Node *n = malloc(sizeof *n);
    if (!n) return false;
    n->val = v; n->next = NULL;
    if (q->tail) q->tail->next = n;
    else q->head = n;                       /* empty queue: head too */
    q->tail = n;
    return true;
}
bool dequeue(Queue *q, int *v) {
    Node *n = q->head;
    if (!n) return false;
    *v = n->val;
    q->head = n->next;
    if (!q->head) q->tail = NULL;  /* queue became empty */
    free(n);
    return true;
}
```

The classic queue bug is leaving `tail` pointing at the freed last node after the queue empties, which the second-to-last line above prevents.

### The ring buffer

Packet drivers hand frames from an interrupt handler to a consumer through a fixed array used circularly. The producer writes at `tail` and the consumer reads at `head`; both wrap with a modulus. The difficulty is that `head == tail` describes both an empty and a full buffer. Three remedies exist: keep a `count`, waste one slot, or let the indices run freely and compare their difference.

<figure>
<svg viewBox="0 0 470 190" width="508">
<text class="sm" x="20" y="14" text-anchor="start">head = 2 (next to read), tail = 6 (next to write), count = 4</text><rect class="box" style="fill:none" x="20" y="40" width="32" height="24"/>
<text class="mono" x="36.0" y="55.0" text-anchor="middle"></text>
<text class="sm" x="36.0" y="74" text-anchor="middle">0</text>
<rect class="box" style="fill:none" x="52" y="40" width="32" height="24"/>
<text class="mono" x="68.0" y="55.0" text-anchor="middle"></text>
<text class="sm" x="68.0" y="74" text-anchor="middle">1</text>
<rect class="hl" x="84" y="40" width="32" height="24"/>
<rect class="box" style="fill:none" x="84" y="40" width="32" height="24"/>
<text class="mono" x="100.0" y="55.0" text-anchor="middle">d</text>
<text class="sm" x="100.0" y="74" text-anchor="middle">2</text>
<rect class="hl" x="116" y="40" width="32" height="24"/>
<rect class="box" style="fill:none" x="116" y="40" width="32" height="24"/>
<text class="mono" x="132.0" y="55.0" text-anchor="middle">e</text>
<text class="sm" x="132.0" y="74" text-anchor="middle">3</text>
<rect class="hl" x="148" y="40" width="32" height="24"/>
<rect class="box" style="fill:none" x="148" y="40" width="32" height="24"/>
<text class="mono" x="164.0" y="55.0" text-anchor="middle">f</text>
<text class="sm" x="164.0" y="74" text-anchor="middle">4</text>
<rect class="hl" x="180" y="40" width="32" height="24"/>
<rect class="box" style="fill:none" x="180" y="40" width="32" height="24"/>
<text class="mono" x="196.0" y="55.0" text-anchor="middle">g</text>
<text class="sm" x="196.0" y="74" text-anchor="middle">5</text>
<rect class="box" style="fill:none" x="212" y="40" width="32" height="24"/>
<text class="mono" x="228.0" y="55.0" text-anchor="middle"></text>
<text class="sm" x="228.0" y="74" text-anchor="middle">6</text>
<rect class="box" style="fill:none" x="244" y="40" width="32" height="24"/>
<text class="mono" x="260.0" y="55.0" text-anchor="middle"></text>
<text class="sm" x="260.0" y="74" text-anchor="middle">7</text><path class="accf" d="M100,38 l-4,-7 l8,0 z"/><text class="lbl" x="100" y="28" text-anchor="middle">head</text><path class="accf" d="M228,66 l-4,7 l8,0 z"/><text class="lbl" x="228" y="83" text-anchor="middle">tail</text><text class="sm" x="20" y="104" text-anchor="start">after more writes the tail wraps: head = 6, tail = 2, count = 4</text><rect class="hl" x="20" y="134" width="32" height="24"/>
<rect class="box" style="fill:none" x="20" y="134" width="32" height="24"/>
<text class="mono" x="36.0" y="149.0" text-anchor="middle">h</text>
<text class="sm" x="36.0" y="168" text-anchor="middle">0</text>
<rect class="hl" x="52" y="134" width="32" height="24"/>
<rect class="box" style="fill:none" x="52" y="134" width="32" height="24"/>
<text class="mono" x="68.0" y="149.0" text-anchor="middle">i</text>
<text class="sm" x="68.0" y="168" text-anchor="middle">1</text>
<rect class="box" style="fill:none" x="84" y="134" width="32" height="24"/>
<text class="mono" x="100.0" y="149.0" text-anchor="middle"></text>
<text class="sm" x="100.0" y="168" text-anchor="middle">2</text>
<rect class="box" style="fill:none" x="116" y="134" width="32" height="24"/>
<text class="mono" x="132.0" y="149.0" text-anchor="middle"></text>
<text class="sm" x="132.0" y="168" text-anchor="middle">3</text>
<rect class="box" style="fill:none" x="148" y="134" width="32" height="24"/>
<text class="mono" x="164.0" y="149.0" text-anchor="middle"></text>
<text class="sm" x="164.0" y="168" text-anchor="middle">4</text>
<rect class="box" style="fill:none" x="180" y="134" width="32" height="24"/>
<text class="mono" x="196.0" y="149.0" text-anchor="middle"></text>
<text class="sm" x="196.0" y="168" text-anchor="middle">5</text>
<rect class="hl" x="212" y="134" width="32" height="24"/>
<rect class="box" style="fill:none" x="212" y="134" width="32" height="24"/>
<text class="mono" x="228.0" y="149.0" text-anchor="middle">f</text>
<text class="sm" x="228.0" y="168" text-anchor="middle">6</text>
<rect class="hl" x="244" y="134" width="32" height="24"/>
<rect class="box" style="fill:none" x="244" y="134" width="32" height="24"/>
<text class="mono" x="260.0" y="149.0" text-anchor="middle">g</text>
<text class="sm" x="260.0" y="168" text-anchor="middle">7</text><path class="accf" d="M228,132 l-4,-7 l8,0 z"/><text class="lbl" x="228" y="122" text-anchor="middle">head</text><path class="accf" d="M100,160 l-4,7 l8,0 z"/><text class="lbl" x="100" y="177" text-anchor="middle">tail</text><text class="sm" x="300" y="150" text-anchor="start">head == tail alone is ambiguous:</text><text class="sm" x="300" y="163" text-anchor="start">empty or full. count resolves it.</text>
</svg>
<figcaption><b>Figure 1.10</b> A circular buffer of capacity eight, before and after the write index wraps. A separate count removes the full-versus-empty ambiguity.</figcaption>
</figure>

```c
#define N 8
typedef struct { uint8_t buf[N]; size_t head, tail, count; } Ring;

bool ring_push(Ring *r, uint8_t b) {
    if (r->count == N) return false;              /* full */
    r->buf[r->tail] = b;
    r->tail = (r->tail + 1) % N;
    r->count++;
    return true;
}
bool ring_pop(Ring *r, uint8_t *out) {
    if (r->count == 0) return false;              /* empty */
    *out = r->buf[r->head];
    r->head = (r->head + 1) % N;
    r->count--;
    return true;
}
```

When one thread produces and another consumes, the `count` variable is written by both and needs a lock. The lock-free alternative keeps `head` and `tail` as free-running unsigned counters and uses a power-of-two capacity: the slot is `idx & (N - 1)`, the buffer is empty when `head == tail` and full when `tail - head == N`. The subtraction is correct even after the counters wrap, because unsigned arithmetic is modular. The producer writes only `tail` and the consumer only `head`, so no lock is needed, provided each side publishes its index with the memory ordering that the concurrency chapters describe.

### The monotonic stack

*Idea.* To find, for each element, the next greater element, keep a stack of indices whose values are decreasing. A new value pops every smaller entry, and each popped entry has found its answer. Every index is pushed and popped once, so the cost is O(*n*). *Recognise:* "next greater or smaller", "days until", "span", "histogram".

```cpp
vector<int> dailyTemps(const vector<int>& t) {
    vector<int> ans(t.size(), 0), st;   // st: indices, temps decreasing
    for (int i = 0; i < (int)t.size(); ++i) {
        while (!st.empty() && t[st.back()] < t[i]) {
            ans[st.back()] = i - st.back();   // wait = index distance
            st.pop_back();
        }
        st.push_back(i);
    }
    return ans;  // never-warmer days stay 0
}
```

| i | t[i] | indices popped (answers set) | stack after |
|---|---|---|---|
| 0 | 73 | none | 0 |
| 1 | 74 | 0 → 1 | 1 |
| 2 | 75 | 1 → 1 | 2 |
| 3 | 71 | none | 2, 3 |
| 4 | 69 | none | 2, 3, 4 |
| 5 | 72 | 4 → 1, 3 → 2 | 2, 5 |
| 6 | 76 | 5 → 1, 2 → 4 | 6 |
| 7 | 73 | none | 6, 7 |

[Result for `[73, 74, 75, 71, 69, 72, 76, 73]`: `[1, 1, 4, 2, 1, 1, 0, 0]`. The classic bug is to store values instead of indices, which makes the distance impossible to compute.]{.result}

The sliding-window maximum uses the same idea with a deque; it is solved in the Problem Set.

::: check
1. In the lock-free ring, why does `tail - head == N` identify a full buffer after both counters have wrapped past 2<sup>32</sup>? [^c1-14]
2. What is the time complexity of `dailyTemps`, given the inner `while`? [^c1-15]
:::

[^c1-14]: Unsigned subtraction is modulo 2<sup>32</sup>, so the difference is the true occupancy as long as it never exceeds *N*.
[^c1-15]: O(*n*): each index is pushed once and popped at most once.

## [1.8]{.sec}Trees and binary search trees [Must · ■■□]{.tag} {#s1-8}

::: bigidea
A binary search tree keeps its keys ordered so that each comparison discards a whole subtree, giving search in time proportional to the height, which is logarithmic only while the tree stays balanced.
:::

A *binary tree* is a node with at most two children; a *binary search tree* (BST) adds the rule that every key in the left subtree is smaller than the node and every key in the right subtree is larger. The *height* *h* is the number of edges on the longest root-to-leaf path. Search, insert and delete each follow one path, so they cost O(*h*). For *n* random keys *h* is about 2 log *n*, but inserting sorted keys produces a chain with *h* = *n*, and every operation degrades to O(*n*). Self-balancing trees (AVL, red-black) restore O(log *n*); C++ `std::map` and `std::set` are red-black trees.

<figure>
<svg viewBox="0 0 440 192" width="475">
<line class="ln" x1="240" y1="28" x2="140" y2="70"/><line class="ln" x1="240" y1="28" x2="340" y2="70"/><line class="ln" x1="140" y1="70" x2="90" y2="112"/><line class="ln" x1="140" y1="70" x2="190" y2="112"/><line class="ln" x1="340" y1="70" x2="390" y2="112"/><line class="ln" x1="190" y1="112" x2="160" y2="154"/><line class="ln" x1="190" y1="112" x2="220" y2="154"/><line class="ln" x1="390" y1="112" x2="360" y2="154"/><circle class="box" cx="240" cy="28" r="12" style="fill:#FFF4C2"/><text class="lbl" x="240" y="31" text-anchor="middle">8</text><circle class="box" cx="140" cy="70" r="12" style="fill:#FFF4C2"/><text class="lbl" x="140" y="73" text-anchor="middle">3</text><circle class="box" cx="340" cy="70" r="12"/><text class="lbl" x="340" y="73" text-anchor="middle">10</text><circle class="box" cx="90" cy="112" r="12"/><text class="lbl" x="90" y="115" text-anchor="middle">1</text><circle class="box" cx="190" cy="112" r="12" style="fill:#FFF4C2"/><text class="lbl" x="190" y="115" text-anchor="middle">6</text><circle class="box" cx="390" cy="112" r="12"/><text class="lbl" x="390" y="115" text-anchor="middle">14</text><circle class="box" cx="160" cy="154" r="12" style="fill:#FFF4C2"/><text class="lbl" x="160" y="157" text-anchor="middle">4</text><circle class="box" cx="220" cy="154" r="12"/><text class="lbl" x="220" y="157" text-anchor="middle">7</text><circle class="box" cx="360" cy="154" r="12"/><text class="lbl" x="360" y="157" text-anchor="middle">13</text><text class="sm" x="20" y="180" text-anchor="start">search 4: left at 8, right at 3, left at 6, found.  In-order: 1 3 4 6 7 8 10 13 14</text>
</svg>
<figcaption><b>Figure 1.11</b> A binary search tree. Everything left of a node is smaller and everything right is larger; the highlighted path is the search for 4.</figcaption>
</figure>

### Traversals

Depth-first traversals differ only in when the node is visited: *pre-order* (node, left, right), *in-order* (left, node, right) and *post-order* (left, right, node). The in-order traversal of a BST yields the keys in sorted order, which is the fact behind "k-th smallest" and "validate BST". Breadth-first traversal visits level by level with a queue. *Recognise:* "depth", "path", "subtree" (DFS, usually post-order, returning information to the parent); "level", "right side view", "shortest" (BFS); "sorted", "k-th", "validate" (in-order).

```cpp
struct TreeNode { int val; TreeNode *left = nullptr, *right = nullptr; };

int height(TreeNode* t) {                  // nodes on the longest path
    return t ? 1 + max(height(t->left), height(t->right)) : 0;
}

vector<int> inorderIter(TreeNode* root) {  // no recursion: explicit stack
    vector<int> out; vector<TreeNode*> st; TreeNode* cur = root;
    while (cur || !st.empty()) {
        while (cur) { st.push_back(cur); cur = cur->left; }  // far left
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
        int sz = q.size(); res.emplace_back();  // sz = nodes on this level
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

All three run in O(*n*) time. Their space is O(*h*) for the explicit stack and O(*width*) for the queue. A skewed tree of 10<sup>6</sup> nodes also overflows the call stack of the recursive `height`, which is the reason for asking in an interview whether the tree may be skewed.

### BST operations in C

Insert and delete return the root of the (possibly changed) subtree, and the caller stores the result back into its link. Forgetting to return or store it is the standard delete bug.

```c
typedef struct T { int key; struct T *l, *r; } T;

T *bst_insert(T *t, int k) {
    if (!t) { t = calloc(1, sizeof *t); if (t) t->key = k; return t; }
    if (k < t->key)      t->l = bst_insert(t->l, k);
    else if (k > t->key) t->r = bst_insert(t->r, k);
    return t;  /* duplicates are ignored */
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
        if (!t->l || !t->r) {  /* zero or one child */
            T *child = t->l ? t->l : t->r;
            free(t);
            return child;  /* parent adopts the child */
        }
        T *s = min_node(t->r);  /* in-order successor */
        t->key = s->key;
        t->r = bst_delete(t->r, s->key);
    }
    return t;
}
```

Deletion has three cases: a leaf is removed; a node with one child is replaced by that child; a node with two children takes the key of its in-order successor (the smallest key of the right subtree), and the successor, which has no left child, is then deleted by one of the first two cases.

<figure>
<svg viewBox="0 0 440 250" width="475">
<text class="sm" x="70" y="14" text-anchor="middle">leaf: unlink it</text><line class="ln" x1="70" y1="40" x2="42" y2="74"/><line class="ln" x1="70" y1="40" x2="98" y2="74"/><circle class="box" cx="70" cy="40" r="11"/><text class="lbl" x="70" y="43" text-anchor="middle">5</text><circle class="box" cx="42" cy="74" r="11" style="fill:#FFF4C2"/><text class="lbl" x="42" y="77" text-anchor="middle">3</text><circle class="box" cx="98" cy="74" r="11"/><text class="lbl" x="98" y="77" text-anchor="middle">8</text><path class="acc" d="M70,118 l0,12" /><path class="accf" d="M70,136 l-4,-8 l8,0 z"/><line class="ln" x1="70" y1="160" x2="98" y2="194"/><circle class="box" cx="70" cy="160" r="11"/><text class="lbl" x="70" y="163" text-anchor="middle">5</text><circle class="box" cx="98" cy="194" r="11"/><text class="lbl" x="98" y="197" text-anchor="middle">8</text><text class="sm" x="220" y="14" text-anchor="middle">one child: child replaces it</text><line class="ln" x1="220" y1="40" x2="192" y2="74"/><line class="ln" x1="220" y1="40" x2="248" y2="74"/><line class="ln" x1="192" y1="74" x2="172" y2="108"/><circle class="box" cx="220" cy="40" r="11"/><text class="lbl" x="220" y="43" text-anchor="middle">5</text><circle class="box" cx="192" cy="74" r="11" style="fill:#FFF4C2"/><text class="lbl" x="192" y="77" text-anchor="middle">3</text><circle class="box" cx="248" cy="74" r="11"/><text class="lbl" x="248" y="77" text-anchor="middle">8</text><circle class="box" cx="172" cy="108" r="11"/><text class="lbl" x="172" y="111" text-anchor="middle">1</text><path class="acc" d="M220,118 l0,12" /><path class="accf" d="M220,136 l-4,-8 l8,0 z"/><line class="ln" x1="220" y1="160" x2="192" y2="194"/><line class="ln" x1="220" y1="160" x2="248" y2="194"/><circle class="box" cx="220" cy="160" r="11"/><text class="lbl" x="220" y="163" text-anchor="middle">5</text><circle class="box" cx="192" cy="194" r="11"/><text class="lbl" x="192" y="197" text-anchor="middle">1</text><circle class="box" cx="248" cy="194" r="11"/><text class="lbl" x="248" y="197" text-anchor="middle">8</text><text class="sm" x="370" y="14" text-anchor="middle">two children: copy the successor</text><line class="ln" x1="370" y1="40" x2="336" y2="74"/><line class="ln" x1="370" y1="40" x2="404" y2="74"/><line class="ln" x1="404" y1="74" x2="384" y2="108"/><line class="ln" x1="404" y1="74" x2="424" y2="108"/><circle class="box" cx="370" cy="40" r="11" style="fill:#FFF4C2"/><text class="lbl" x="370" y="43" text-anchor="middle">5</text><circle class="box" cx="336" cy="74" r="11"/><text class="lbl" x="336" y="77" text-anchor="middle">3</text><circle class="box" cx="404" cy="74" r="11"/><text class="lbl" x="404" y="77" text-anchor="middle">8</text><circle class="box" cx="384" cy="108" r="11"/><text class="lbl" x="384" y="111" text-anchor="middle">6</text><circle class="box" cx="424" cy="108" r="11"/><text class="lbl" x="424" y="111" text-anchor="middle">9</text><path class="acc" d="M370,118 l0,12" /><path class="accf" d="M370,136 l-4,-8 l8,0 z"/><line class="ln" x1="370" y1="160" x2="336" y2="194"/><line class="ln" x1="370" y1="160" x2="404" y2="194"/><line class="ln" x1="404" y1="194" x2="424" y2="228"/><circle class="box" cx="370" cy="160" r="11"/><text class="lbl" x="370" y="163" text-anchor="middle">6</text><circle class="box" cx="336" cy="194" r="11"/><text class="lbl" x="336" y="197" text-anchor="middle">3</text><circle class="box" cx="404" cy="194" r="11"/><text class="lbl" x="404" y="197" text-anchor="middle">8</text><circle class="box" cx="424" cy="228" r="11"/><text class="lbl" x="424" y="231" text-anchor="middle">9</text>
</svg>
<figcaption><b>Figure 1.12</b> The three cases of BST deletion, with the deleted node shaded. In the third case the successor 6 is the left-most node of the right subtree; its key moves up and its old position is removed.</figcaption>
</figure>

::: example
**Delete 3 from the tree of Figure 1.11.**

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
bool valid(TreeNode* t, long long lo, long long hi) {  // lo < key < hi
    return !t || (lo < t->val && t->val < hi &&
                  valid(t->left, lo, t->val) &&
                  valid(t->right, t->val, hi));
}
// call: valid(root, LLONG_MIN, LLONG_MAX)
```

::: trap
*Claim:* a tree is a BST if every node is greater than its left child and smaller than its right child. *Why it is wrong:* the tree 5 with left child 1 and right child 6, where 6 has left child 4, satisfies the local rule but 4 sits in the right subtree of 5. *Correct statement:* every key must lie between the bounds inherited from all its ancestors, or the in-order sequence must be strictly increasing.
:::

### Keeping a BST balanced

An *AVL tree* stores in each node the height of its subtree and restores the rule that the heights of a node's two subtrees differ by at most one, after every insert or delete, using *rotations*. A rotation rearranges three pointers, lowers one side by a level and raises the other, and preserves the in-order sequence, so the search property survives.

<figure>
<svg viewBox="0 0 440 172" width="475"><defs><marker id="a11" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#3D55A8"/></marker></defs>
<text class="sm" x="80" y="14" text-anchor="middle">before: y is too deep on the left</text><text class="sm" x="340" y="14" text-anchor="middle">after rotate&#95;right(y)</text><line class="ln" x1="90" y1="40" x2="60" y2="80"/><line class="ln" x1="90" y1="40" x2="125" y2="90"/><line class="ln" x1="60" y1="80" x2="35" y2="115"/><line class="ln" x1="60" y1="80" x2="85" y2="115"/><circle class="box" cx="90" cy="40" r="12"/><text class="lbl" x="90" y="43" text-anchor="middle">y</text><circle class="box" cx="60" cy="80" r="12"/><text class="lbl" x="60" y="83" text-anchor="middle">x</text><path class="ln" style="fill:#F1F2F3" d="M125,90 l-14,28 l28,0 z"/><text class="lbl" x="125" y="112" text-anchor="middle">C</text><path class="ln" style="fill:#F1F2F3" d="M35,115 l-14,28 l28,0 z"/><text class="lbl" x="35" y="137" text-anchor="middle">A</text><path class="ln" style="fill:#F1F2F3" d="M85,115 l-14,28 l28,0 z"/><text class="lbl" x="85" y="137" text-anchor="middle">B</text><path class="acc" d="M170,70 L250,70" marker-end="url(#a11)"/><line class="ln" x1="340" y1="40" x2="305" y2="90"/><line class="ln" x1="340" y1="40" x2="375" y2="80"/><line class="ln" x1="375" y1="80" x2="350" y2="115"/><line class="ln" x1="375" y1="80" x2="400" y2="115"/><circle class="box" cx="340" cy="40" r="12"/><text class="lbl" x="340" y="43" text-anchor="middle">x</text><path class="ln" style="fill:#F1F2F3" d="M305,90 l-14,28 l28,0 z"/><text class="lbl" x="305" y="112" text-anchor="middle">A</text><circle class="box" cx="375" cy="80" r="12"/><text class="lbl" x="375" y="83" text-anchor="middle">y</text><path class="ln" style="fill:#F1F2F3" d="M350,115 l-14,28 l28,0 z"/><text class="lbl" x="350" y="137" text-anchor="middle">B</text><path class="ln" style="fill:#F1F2F3" d="M400,115 l-14,28 l28,0 z"/><text class="lbl" x="400" y="137" text-anchor="middle">C</text><text class="sm" x="10" y="160" text-anchor="start">x.right (subtree B) becomes y.left; y becomes x.right. In-order sequence A x B y C is unchanged.</text>
</svg>
<figcaption><b>Figure 1.13</b> A right rotation. Three pointer writes lower the left side by one level and raise the right, and the search order is preserved.</figcaption>
</figure>

```c
T *rotate_right(T *y) {          /* y->l becomes the new subtree root */
    T *x = y->l;
    y->l = x->r;                 /* subtree B moves across */
    x->r = y;
    return x;                    /* caller stores x where y was */
}
T *rotate_left(T *x) {           /* mirror image */
    T *y = x->r;
    x->r = y->l;
    y->l = x;
    return y;
}
```

After an insertion, the first unbalanced node on the path back to the root is repaired by one of four cases, chosen by where the new key went.

| Imbalance | Where the key went | Repair |
|---|---|---|
| left-left | into the left subtree of the left child | rotate right at the node |
| right-right | into the right subtree of the right child | rotate left at the node |
| left-right | into the right subtree of the left child | rotate left at the child, then right at the node |
| right-left | into the left subtree of the right child | rotate right at the child, then left at the node |

Inserting 1, 2, 3 in order into an AVL tree leaves 1 → 2 → 3 as a chain after the third key; this is the right-right case, and one left rotation at 1 gives the balanced tree with 2 at the root. Height is then at most about 1.44 log₂ *n*, so every operation is O(log *n*). An interview rarely asks for the full AVL code; it asks why a plain BST degrades and what a rotation is, and expects `std::map` as the practical answer.

| Structure | Ordering rule | Find | Typical use |
|---|---|---|---|
| binary search tree | left < node < right | O(*h*) | ordered set, range queries |
| heap | parent ≤ children | O(*n*) | the minimum, the next event |
| trie | path spells the key | O(*L*) | prefixes, longest-prefix match |
| hash table | none | O(1) average | membership, counts |

::: check
1. What is the height of the BST built by inserting 1, 2, 3, 4, 5 in order? [^c1-16]
2. Which traversal prints a BST in sorted order? [^c1-17]
:::

[^c1-16]: 4 edges (5 nodes): each key becomes the right child of the previous one, so operations cost O(*n*).
[^c1-17]: In-order (left, node, right).

:::
