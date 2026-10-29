::: {.p1}

### Linked lists, stacks and queues

::: problems

::: q
### Q1.54 Intersection of two linked lists
[NOKIA · TECH-1 · ■□□ · S]{.meta}

*Two singly linked lists may merge into a common tail. Return the first shared node, or `NULL`, in O(1) extra space.*

[30-second answer: let each pointer walk its own list and then the other; both cover the same total length, so they meet at the intersection, or both reach `NULL` together.]{.short}

```c
Node *intersect(Node *a, Node *b) {
  Node *p = a, *q = b;
  while (p != q) {
    p = p ? p->next : b;
    q = q ? q->next : a;
  }
  return p;
}
```

If the lists have *x* and *y* private nodes and *z* shared ones, each pointer travels *x* + *y* + *z* nodes before the meeting point, so the shared tail aligns. **Complexity.** O(*m* + *n*) time, O(1) space. **Mistakes.** Comparing values instead of node addresses.
:::

::: q
### Q1.55 Remove duplicates from a sorted list, linear and circular
[ARISTA · TECH-1 · ■■□ · S]{.meta}

*Remove repeated values from a sorted singly linked list. Then do it for a sorted circular list.*

[30-second answer: compare each node with its successor and unlink the successor while they are equal; for the circular list, stop when the walk returns to the head and finally compare the last node with the head.]{.short}

```c
Node *dedup(Node *h) {
  for (Node *p = h; p && p->next; ) {
    if (p->val == p->next->val) {
      Node *d = p->next;
      p->next = d->next;
      free(d);
    } else p = p->next;
  }
  return h;
}
void dedup_circ(Node *h) {
  if (!h) return;
  Node *p = h;
  while (p->next != h) {
    if (p->val == p->next->val) {
      Node *d = p->next;
      p->next = d->next;
      free(d);
    } else p = p->next;
  }
  if (p != h && p->val == h->val) {
    Node *q = h;
    while (q->next != p) q = q->next;
    q->next = h;
    free(p);
  }
}
```

In the circular version a duplicate may wrap around (the tail equals the head); the head is kept and the tail removed. **Complexity.** O(*n*). **Mistakes.** Advancing `p` after a deletion (it would skip a third copy); looping `while (p)` on a circular list, which never ends.
:::

::: q
### Q1.56 Delete a node given only a pointer to it
[ARISTA · TECH-1 · ■□□ · S]{.meta}

*You are given a pointer to a node that is not the tail of a singly linked list, and no head. Delete it.*

[30-second answer: copy the successor's value into the node and unlink the successor.]{.short}

```c
void delete_node(Node *n) {
  Node *d = n->next;
  n->val = d->val;
  n->next = d->next;
  free(d);
}
```

**Complexity.** O(1). **Follow-ups.** The tail cannot be deleted this way, since it has no successor to copy; any other pointer held to the successor is now dangling. **Mistakes.** Trying to unlink `n` itself without access to its predecessor.
:::

::: q
### Q1.57 Remove the n-th node from the end
[AMAZON · MICROSOFT · TECH-1 · ■■□ · T]{.meta}

*Delete the *n*-th node from the end of a singly linked list in one pass.*

[30-second answer: advance one pointer *n* nodes ahead, then move both until the lead pointer reaches the last node; the trailing pointer is then the predecessor of the node to delete.]{.short}

```c
Node *remove_nth(Node *head, int n) {
  Node dummy = {0, head};
  Node *fast = &dummy, *slow = &dummy;
  while (n-- > 0 && fast) fast = fast->next;
  if (!fast) return head;     /* n too big */
  while (fast->next) {
    fast = fast->next;
    slow = slow->next;
  }
  Node *d = slow->next;
  slow->next = d->next;
  free(d);
  return dummy.next;
}
```

The dummy node lets the head itself be removed (*n* equal to the length). **Complexity.** O(*L*) time, O(1) space.
:::

::: q
### Q1.58 Palindrome linked list
[AMAZON · TECH-1 · ■■□ · T]{.meta}

*Decide whether the values of a singly linked list read the same in both directions, in O(1) extra space.*

[30-second answer: find the middle with fast and slow pointers, reverse the second half in place, compare it with the first half, and reverse it back.]{.short}

```c
bool is_pal(Node *h) {
  Node *slow = h, *fast = h;
  while (fast && fast->next) {
    slow = slow->next;
    fast = fast->next->next;
  }
  Node *r = reverse(slow), *save = r;
  bool ok = true;
  for (Node *p = h; ok && r;
       p = p->next, r = r->next)
    if (p->val != r->val) ok = false;
  reverse(save);          /* restore the list */
  return ok;
}
```

For `1 → 2 → 3 → 2 → 1` the middle is 3, the reversed half is `1 → 2 → 3`, and the comparison `1=1, 2=2, 3=3` succeeds (the middle compares with itself). `reverse` is the function of [§1.6](#s1-6){.ref}. **Complexity.** O(*n*) time, O(1) space.
:::

::: q
### Q1.59 Add two numbers stored as linked lists
[ARISTA · AMAZON · TECH-1 · ■■□ · S]{.meta}

*Each list holds a non-negative number with the least significant digit first. Return their sum as a new list.*

[30-second answer: add digit by digit with a carry, as on paper, appending to a result list through a dummy head; continue while either list or a carry remains.]{.short}

```c
Node *add_lists(Node *a, Node *b) {
  Node dummy = {0, NULL}, *t = &dummy;
  int carry = 0;
  while (a || b || carry) {
    int s = carry + (a ? a->val : 0)
                  + (b ? b->val : 0);
    carry = s / 10;
    Node *n = malloc(sizeof *n);
    if (!n) return NULL;  /* leaks partial */
    n->val = s % 10;
    n->next = NULL;
    t->next = n;
    t = n;
    if (a) a = a->next;
    if (b) b = b->next;
  }
  return dummy.next;
}
```

`[2,4,3] + [5,6,4]` gives `[7,0,8]` (342 + 465 = 807). **Complexity.** O(max(*m*, *n*)). **Follow-ups.** When the most significant digit comes first, reverse both inputs (or push digits on stacks), add, and reverse the result. **Mistakes.** Dropping a final carry (`5 + 5` must give `[0,1]`).
:::

::: q
### Q1.60 Reverse a doubly linked list; delete a given node
[ARISTA · TECH-1 · ■□□ · S]{.meta}

*Reverse a doubly linked list in place. Then delete a node given its pointer.*

[30-second answer: swap the `next` and `prev` pointers of every node and return the last node visited; deleting a node relinks its two neighbours and updates the head if the node was first.]{.short}

```c
typedef struct D { int val;
          struct D *prev, *next; } D;
D *dl_reverse(D *h) {
  D *cur = h, *last = NULL;
  while (cur) {
    D *nx = cur->next;
    cur->next = cur->prev;
    cur->prev = nx;
    last = cur;
    cur = nx;
  }
  return last;
}
D *dl_delete(D *h, D *n) {
  if (n->prev) n->prev->next = n->next;
  else h = n->next;
  if (n->next) n->next->prev = n->prev;
  free(n);
  return h;
}
```

**Complexity.** O(*n*) and O(1). **Mistakes.** Following `cur->next` after swapping (it now points backwards; hence the saved `nx`); forgetting the head and tail cases in deletion.
:::

::: q
### Q1.61 Reverse nodes in groups of k
[ARISTA · TECH-2 · ■■■ · T]{.meta}

*Reverse a list `k` nodes at a time; a final group shorter than `k` stays as it is.*

[30-second answer: check that `k` nodes remain, reverse the rest of the list recursively, then reverse this group onto the result.]{.short}

```c
Node *rev_k(Node *head, int k) {
  Node *p = head;
  for (int i = 0; i < k; i++) {
    if (!p) return head;   /* fewer than k */
    p = p->next;
  }
  Node *prev = rev_k(p, k), *cur = head;
  for (int i = 0; i < k; i++) {
    Node *nx = cur->next;
    cur->next = prev;
    prev = cur;
    cur = nx;
  }
  return prev;
}
```

The reversal loop is the ordinary one of [§1.6](#s1-6){.ref} with `prev` starting at the already processed remainder. **Complexity.** O(*n*) time, O(*n*/*k*) stack; an iterative version keeps the tail of the previous group and uses O(1) space. **Mistakes.** Reversing a short final group.
:::

::: q
### Q1.62 Copy a list with random pointers
[AMAZON · MICROSOFT · TECH-2 · ■■□ · T]{.meta}

*Each node has `next` and `rnd` (any node or `NULL`). Make a deep copy.*

[30-second answer: interleave a copy after every original node, set each copy's `rnd` from its original's `rnd->next`, then split the two lists.]{.short}

```c
typedef struct R { int val;
        struct R *next, *rnd; } R;
R *copy_random(R *h) {   /* checks omitted */
  if (!h) return NULL;
  for (R *p = h; p; p = p->next->next) {
    R *c = malloc(sizeof *c);
    c->val = p->val;
    c->next = p->next;
    c->rnd = NULL;
    p->next = c;
  }
  for (R *p = h; p; p = p->next->next)
    if (p->rnd) p->next->rnd = p->rnd->next;
  R *nh = h->next;
  for (R *p = h; p; p = p->next) {
    R *c = p->next;
    p->next = c->next;
    if (c->next) c->next = c->next->next;
  }
  return nh;
}
```

**Complexity.** O(*n*) time, O(1) extra beyond the copy. **Follow-ups.** The alternative is a hash map from original to copy, which uses O(*n*) memory but is simpler to write.
:::

::: q
### Q1.63 Merge k sorted lists
[AMAZON · GOOGLE · TECH-2 · ■■■ · T]{.meta}

*Merge `k` sorted linked lists into one sorted list.*

[30-second answer: keep the head of each list in a min-heap; repeatedly take the smallest and push its successor.]{.short}

```cpp
struct LN { int val; LN *next; };
LN *mergeK(vector<LN*> ls) {
  auto cmp = [](LN* a, LN* b) {
    return a->val > b->val; };
  priority_queue<LN*, vector<LN*>,
                 decltype(cmp)> pq(cmp);
  for (LN* l : ls) if (l) pq.push(l);
  LN dummy{0, nullptr}, *t = &dummy;
  while (!pq.empty()) {
    LN* n = pq.top(); pq.pop();
    t->next = n; t = n;
    if (n->next) pq.push(n->next);
  }
  return dummy.next;
}
```

**Complexity.** O(*N* log *k*) for *N* total nodes. **Follow-ups.** Merging pairwise in rounds (divide and conquer) has the same bound without a heap. This is the same k-way merge that combines sorted runs of an external sort.
:::

::: q
### Q1.64 Min stack
[AMAZON · MICROSOFT · OA · ■□□ · T]{.meta}

*A stack with `push`, `pop`, `top` and `getMin`, all O(1).*

[30-second answer: store with every element the minimum of the stack up to that element.]{.short}

```cpp
class MinStack {
  vector<pair<int,int>> s;  // value, min
public:
  void push(int x) {
    int m = s.empty() ? x
                      : min(x, s.back().second);
    s.push_back({x, m});
  }
  void pop() { s.pop_back(); }
  int top() { return s.back().first; }
  int getMin() { return s.back().second; }
};
```

**Complexity.** O(1) per operation, O(*n*) space. **Mistakes.** Keeping a single `min` variable, which cannot be restored after popping the minimum.
:::

::: q
### Q1.65 Queue using two stacks
[MICROSOFT · AMAZON · OA · ■□□ · T]{.meta}

*Implement a FIFO queue using only stack operations.*

[30-second answer: push onto an input stack; pop from an output stack, refilling it from the input stack only when it is empty. Each element moves at most twice.]{.short}

```cpp
class MyQueue {
  stack<int> in, out;
  void shift() {
    if (out.empty())
      while (!in.empty()) {
        out.push(in.top()); in.pop();
      }
  }
public:
  void push(int x) { in.push(x); }
  int pop() {
    shift(); int v = out.top();
    out.pop(); return v;
  }
  int peek() { shift(); return out.top(); }
  bool empty() { return in.empty() && out.empty(); }
};
```

**Complexity.** Amortised O(1) per operation. **Mistakes.** Refilling `out` while it still holds elements, which breaks the order.
:::

::: q
### Q1.66 Evaluate a reverse Polish expression
[AMAZON · OA · ■■□ · T]{.meta}

*Evaluate tokens such as `["2","1","+","3","*"]` (that is, (2 + 1) × 3 = 9). Division truncates towards zero.*

[30-second answer: push numbers; on an operator pop two operands (the right one first), apply, and push the result.]{.short}

```cpp
int evalRPN(const vector<string>& t) {
  vector<long long> st;
  for (auto& s : t) {
    if (s.size() == 1 && strchr("+-*/", s[0])) {
      long long b = st.back(); st.pop_back();
      long long a = st.back(); st.pop_back();
      char o = s[0];
      st.push_back(o == '+' ? a + b
                 : o == '-' ? a - b
                 : o == '*' ? a * b : a / b);
    } else st.push_back(stoll(s));
  }
  return (int)st.back();
}
```

**Complexity.** O(*n*). **Mistakes.** Swapping the operand order (matters for `-` and `/`); treating `"-3"` as an operator (hence the test on the token length).
:::

::: q
### Q1.67 Sliding window maximum
[GOOGLE · AMAZON · TECH-2 · ■■■ · T]{.meta}

*For every window of `k` consecutive elements, output its maximum, in O(*n*).*

[30-second answer: keep a deque of indices whose values decrease from front to back; the front is the maximum of the window. Drop the front when it leaves the window, and drop smaller values from the back before pushing the new index.]{.short}

```cpp
vector<int> maxWindow(const vector<int>& a,
                      int k) {
  deque<int> dq;
  vector<int> r;
  for (int i = 0; i < (int)a.size(); ++i) {
    if (!dq.empty() && dq.front() <= i - k)
      dq.pop_front();
    while (!dq.empty() && a[dq.back()] <= a[i])
      dq.pop_back();
    dq.push_back(i);
    if (i >= k - 1) r.push_back(a[dq.front()]);
  }
  return r;
}
```

For `[1,3,-1,-3,5,3,6,7]` and *k* = 3 the output is `[3,3,5,5,6,7]`. Each index enters and leaves the deque once, so the cost is O(*n*). **Mistakes.** Storing values rather than indices (the expiry test needs the index); using `<` so that equal values stay and the deque grows.
:::

:::

### Trees and tries

::: problems

::: q
### Q1.68 Invert a binary tree; test for symmetry
[GOOGLE · AMAZON · OA · ■□□ · T]{.meta}

*Swap the left and right child of every node. Then decide whether a tree is a mirror image of itself.*

[30-second answer: recurse: swap at each node; for symmetry compare the left subtree with the mirror of the right subtree.]{.short}

```cpp
TreeNode* invert(TreeNode* t) {
  if (!t) return t;
  swap(t->left, t->right);
  invert(t->left);
  invert(t->right);
  return t;
}
bool mirror(TreeNode* a, TreeNode* b) {
  if (!a || !b) return a == b;
  return a->val == b->val
      && mirror(a->left, b->right)
      && mirror(a->right, b->left);
}
// symmetric iff root == null ||
//   mirror(root->left, root->right)
```

**Complexity.** O(*n*) time, O(*h*) stack. **Mistakes.** Comparing `a->left` with `b->left` in the mirror test.
:::

::: q
### Q1.69 Lowest common ancestor
[MICROSOFT · AMAZON · TECH-1 · ■■□ · T]{.meta}

*Find the lowest node that has both `p` and `q` in its subtree, first in a BST and then in a general binary tree.*

[30-second answer: in a BST walk down, going left when both keys are smaller and right when both are larger; the first node that splits them is the answer. In a general tree, recurse and return the node where both sides report a hit.]{.short}

```cpp
TreeNode* lcaBST(TreeNode* t, int p, int q) {
  while (t) {
    if (p < t->val && q < t->val)
      t = t->left;
    else if (p > t->val && q > t->val)
      t = t->right;
    else return t;
  }
  return nullptr;
}
TreeNode* lca(TreeNode* t, TreeNode* p,
              TreeNode* q) {
  if (!t || t == p || t == q) return t;
  TreeNode* l = lca(t->left, p, q);
  TreeNode* r = lca(t->right, p, q);
  return l && r ? t : (l ? l : r);
}
```

**Complexity.** O(*h*) for the BST, O(*n*) for the general tree. **Mistakes.** Assuming both nodes exist in the general version; the code above then returns the one found.
:::

::: q
### Q1.70 Kth smallest element in a BST
[GOOGLE · AMAZON · TECH-1 · ■■□ · T]{.meta}

*Return the *k*-th smallest key of a BST.*

[30-second answer: in-order traversal visits keys in ascending order; stop at the *k*-th visit using an explicit stack.]{.short}

```cpp
int kthSmallest(TreeNode* t, int k) {
  vector<TreeNode*> st;
  while (t || !st.empty()) {
    while (t) { st.push_back(t); t = t->left; }
    t = st.back(); st.pop_back();
    if (--k == 0) return t->val;
    t = t->right;
  }
  return -1;
}
```

**Complexity.** O(*h* + *k*) time, O(*h*) space. **Follow-ups.** With frequent updates and queries, store the subtree size in each node and descend in O(*h*).
:::

::: q
### Q1.71 Diameter of a binary tree
[GOOGLE · MICROSOFT · TECH-1 · ■■□ · T]{.meta}

*Find the number of edges on the longest path between two nodes of a tree.*

[30-second answer: post-order recursion that returns the node's height to its parent while updating a global best with the left height plus the right height.]{.short}

```cpp
int diam(TreeNode* t, int& best) {
  if (!t) return 0;
  int l = diam(t->left, best);
  int r = diam(t->right, best);
  best = max(best, l + r);
  return 1 + max(l, r);
}
// call: int best = 0; diam(root, best);
```

The value returned upward (a height) differs from the value recorded (a path through the node); mixing them up is the classic bug. **Complexity.** O(*n*) time, O(*h*) space.
:::

::: q
### Q1.72 Serialise and deserialise a binary tree
[GOOGLE · AMAZON · TECH-2 · ■■■ · T]{.meta}

*Convert a binary tree to a string and back, losing no structure.*

[30-second answer: pre-order traversal with an explicit marker for each null child; the same order reads it back recursively.]{.short}

```cpp
void ser(TreeNode* t, string& o) {
  if (!t) { o += "#,"; return; }
  o += to_string(t->val) + ",";
  ser(t->left, o);
  ser(t->right, o);
}
TreeNode* de(istringstream& in) {
  string s;
  getline(in, s, ',');
  if (s == "#") return nullptr;
  auto* t = new TreeNode{stoi(s)};
  t->left = de(in);
  t->right = de(in);
  return t;
}
```

The tree `1 (2, 3)` becomes `1,2,#,#,3,#,#,`. Without the null markers the string would not determine the shape. **Complexity.** O(*n*). **Follow-ups.** Level-order form with a queue avoids deep recursion.
:::

::: q
### Q1.73 Implement a trie
[GOOGLE · AMAZON · TECH-1 · ■■□ · S]{.meta}

*Support `insert(word)`, `search(word)` and `startsWith(prefix)` for lowercase words.*

[30-second answer: a tree with 26 children per node and an end flag; each operation walks one edge per letter.]{.short}

```cpp
struct Trie {
  struct N { N* c[26] = {}; bool end = false; };
  N root;
  void insert(const string& w) {
    N* t = &root;
    for (char ch : w) {
      N*& nx = t->c[ch - 'a'];
      if (!nx) nx = new N;
      t = nx;
    }
    t->end = true;
  }
  N* walk(const string& p) {
    N* t = &root;
    for (char ch : p) {
      t = t->c[ch - 'a'];
      if (!t) return nullptr;
    }
    return t;
  }
  bool search(const string& w) {
    N* t = walk(w); return t && t->end;
  }
  bool startsWith(const string& p) {
    return walk(p) != nullptr;
  }
};
```

**Complexity.** O(*L*) per operation; memory up to 26 pointers per node. **Follow-ups.** A hash map of children saves memory for large alphabets; deletion needs the pruning of the next problem. **Mistakes.** Treating a prefix as a word (`search("app")` when only `"apple"` is stored).
:::

::: q
### Q1.74 Delete a prefix from the routing trie
[GOOGLE · JUNIPER · TECH-2 · ■■■ · T]{.meta}

*Remove a route from the binary trie of [§1.9](#s1-9){.ref}, freeing nodes that no longer lead anywhere.*

[30-second answer: recurse down the prefix; clear the next hop at its node; on the way back, free any child that has no route and no children.]{.short}

```c
static bool prune(Node *t, uint32_t p,
                  unsigned len, unsigned i) {
  if (i == len) t->hop = -1;
  else {
    unsigned b = (p >> (31 - i)) & 1u;
    if (t->c[b] && prune(t->c[b], p, len, i+1)) {
      free(t->c[b]);
      t->c[b] = NULL;
    }
  }
  return t->hop < 0 && !t->c[0] && !t->c[1];
}
void trie_delete(Node *root, uint32_t p,
                 unsigned len) {
  prune(root, p, len, 0);
}
```

The function returns whether its node is now useless; the root is never freed. Deleting 10.1.2.0/24 from the table of [§1.9](#s1-9){.ref} removes the nodes below 10.1.0.0/16 but keeps the /16 route. **Complexity.** O(*len*). **Mistakes.** Freeing a node that still carries a shorter prefix's route; clearing the hop without pruning (a slow memory leak under route churn).
:::

::: q
### Q1.75 CIDR firewall rules: the most specific rule wins
[GOOGLE · CISCO · TECH-2 · ■■■ · T]{.meta}

*A rule list maps CIDR blocks to allow or deny. For a packet's source address, apply the most specific matching rule; if two rules have the same prefix, the earlier rule wins; with no match, deny.*

[30-second answer: store the action at the prefix's node in the trie of [§1.9](#s1-9){.ref}, ignore a later rule for an already stored prefix, and answer with a longest-prefix lookup.]{.short}

```c
static Node *find_exact(Node *t, uint32_t p,
                        unsigned len) {
  for (unsigned i = 0; t && i < len; i++)
    t = t->c[(p >> (31 - i)) & 1u];
  return t;
}
bool add_rule(Node *root, uint32_t p,
              unsigned len, int act) {
  Node *e = find_exact(root, p, len);
  if (e && e->hop >= 0) return true;
  return trie_insert(root, p, len, act);
}
int decide(const Node *root, uint32_t ip) {
  int a = trie_lookup(root, ip);
  return a < 0 ? 0 : a;   /* 1 allow, 0 deny */
}
```

With the rules `10.0.0.0/8 allow` and `10.1.0.0/16 deny`, the address 10.1.5.5 is denied and 10.2.0.1 is allowed. **Complexity.** O(32) per rule and per lookup. **Mistakes.** Using first-match-in-list semantics (a scan) when the specification says most specific; a rule `0.0.0.0/0` is the default and sits at the root.
:::

::: q
### Q1.76 Longest-prefix match without a trie
[GOOGLE · TECH-2 · ■■□ · S]{.meta}

*The interviewer rejects the trie: "use hash tables".*

[30-second answer: one hash table per prefix length, mapping the masked prefix to the next hop; probe from /32 down to /0 and return the first hit.]{.short}

```cpp
struct LPM {
  unordered_map<uint32_t, int> t[33];
  static uint32_t mk(uint32_t a, int len) {
    return len ? a & (~0u << (32 - len)) : 0;
  }
  void add(uint32_t p, int len, int hop) {
    t[len][mk(p, len)] = hop;
  }
  int lookup(uint32_t a) {
    for (int len = 32; len >= 0; --len) {
      auto it = t[len].find(mk(a, len));
      if (it != t[len].end()) return it->second;
    }
    return -1;
  }
};
```

**Complexity.** At most 33 hash probes per lookup; O(1) insertion. **Follow-ups.** Keep a list of the prefix lengths that occur (real tables use few distinct lengths) and probe only those; binary search over lengths with "marker" entries gives O(log 32) probes. **Mistakes.** The shift `~0u << 32` for the /0 case (handled by `len ?`).
:::

::: q
### Q1.77 Maximum XOR of two numbers
[GOOGLE · TECH-2 · ■■■ · T]{.meta}

*Find the maximum of `a[i] ^ a[j]` over all pairs of a non-negative integer array in O(*n*).*

[30-second answer: insert every number into a binary trie, most significant bit first; for each number walk the trie choosing, at each bit, the child with the opposite bit when it exists.]{.short}

```cpp
int findMaxXor(const vector<int>& a) {
  vector<array<int,2>> t(1);   // 0 = root
  for (int x : a) {
    int u = 0;
    for (int i = 30; i >= 0; --i) {
      int b = (x >> i) & 1;
      if (!t[u][b]) {
        t[u][b] = t.size();
        t.push_back({0, 0});
      }
      u = t[u][b];
    }
  }
  int best = 0;
  for (int x : a) {
    int u = 0, cur = 0;
    for (int i = 30; i >= 0; --i) {
      int b = ((x >> i) & 1) ^ 1;
      if (t[u][b]) { cur |= 1 << i; u = t[u][b]; }
      else u = t[u][b ^ 1];
    }
    best = max(best, cur);
  }
  return best;
}
```

A higher bit set to one outweighs all lower bits, so the greedy choice of the opposite bit is optimal. **Complexity.** O(31 *n*) time and space. **Mistakes.** Starting at bit 31 for non-negative `int` (harmless but wasted), or building the trie with node pointers that reallocate (use indices, as here).
:::

:::
:::
