::: {.p1}
::: pack
## Problem Set {#ps1}

Every question of this pillar is solved once, here. Difficulty is ■□□ (foundation), ■■□ (typical test) or ■■■ (hardest interviews). The tag **S** means that candidates report this specific question; **T** means that the topic is reported and the wording is ours. Round names are OA (online assessment), TECH-1 and TECH-2 (technical interviews) and HM (hiring manager). Code is C++ for general algorithms and C for networking and systems problems, and each solution is a complete function. The first table lists the problems whose full solutions are already in the teaching sections, so that nothing is solved twice.

| Q | Problem | Tags | Solved in |
|---|---|---|---|
| Q1.1 | Two Sum: indices of two values adding to a target | CISCO · AMAZON · OA · ■□□ · S | [§1.1](#s1-1){.ref} |
| Q1.2 | Longest substring without repeating characters | CISCO · OA · ■■□ · S | [§1.2](#s1-2){.ref} |
| Q1.3 | Number of subarrays with sum *k* (negatives allowed) | GOOGLE · MICROSOFT · TECH-1 · ■■□ · T | [§1.2](#s1-2){.ref} |
| Q1.4 | Longest consecutive sequence in O(*n*) | GOOGLE · TECH-1 · ■■□ · T | [§1.3](#s1-3){.ref} |
| Q1.5 | Validate a dotted-quad IPv4 address; parse a MAC address | CISCO · AMAZON · OA · ■■□ · T | [§1.4](#s1-4){.ref} |
| Q1.6 | Are two IPs in the same subnet (mask or prefix)? | CISCO · AMAZON · OA · ■□□ · T | [§1.5](#s1-5){.ref} |
| Q1.7 | Network, broadcast, first, last and host count of 10.20.30.40/22 | CISCO · TECH-1 · ■■□ · T | [§1.5](#s1-5){.ref} |
| Q1.8 | Set, clear and toggle the *k*-th bit as macros | QUALCOMM · TECH-1 · ■□□ · S | [§1.5](#s1-5){.ref} |
| Q1.9 | Delete a node by value (head included); delete all matches | ARISTA · OA · ■■□ · S | [§1.6](#s1-6){.ref} |
| Q1.10 | Reverse a singly linked list | BROADCOM · ARISTA · TECH-1 · ■□□ · S | [§1.6](#s1-6){.ref} |
| Q1.11 | Merge two sorted linked lists | ARISTA · TECH-1 · ■□□ · S | [§1.6](#s1-6){.ref} |
| Q1.12 | Detect a cycle; find where it starts; prove it | JUNIPER · NOKIA · TECH-1 · ■■□ · S | [§1.6](#s1-6){.ref} |
| Q1.13 | Middle node of a linked list | NOKIA · TECH-1 · ■□□ · T | [§1.6](#s1-6){.ref} |
| Q1.14 | Circular buffer for a producer and a consumer: full versus empty | BROADCOM · QUALCOMM · ARISTA · TECH-1 · ■■□ · T | [§1.7](#s1-7){.ref} |
| Q1.15 | Balanced brackets | NOKIA · OA · ■□□ · S | [§1.7](#s1-7){.ref} |
| Q1.16 | Days until a warmer temperature (next greater element) | MICROSOFT · TECH-1 · ■■□ · T | [§1.7](#s1-7){.ref} |
| Q1.17 | BST insert, search, delete; the effect of sorted input | ARISTA · TECH-1 · ■■□ · S | [§1.8](#s1-8){.ref} |
| Q1.18 | Validate a BST; level-order traversal | ARISTA · GOOGLE · TECH-1 · ■■□ · S | [§1.8](#s1-8){.ref} |
| Q1.19 | Longest-prefix match of an IP against a list of prefixes | GOOGLE · TECH-1 · ■■■ · S | [§1.9](#s1-9){.ref} |
| Q1.20 | Shortest paths in a weighted network; link-state versus distance-vector | CISCO · GOOGLE · TECH-1 · ■■□ · T | [§1.11](#s1-11){.ref} |
| Q1.21 | Depth-first search without recursion | NOKIA · OA · ■■□ · S | [§1.11](#s1-11){.ref} |
| Q1.22 | Restore IP addresses from a digit string | AMAZON · MICROSOFT · TECH-1 · ■■□ · T | [§1.12](#s1-12){.ref} |
| Q1.23 | Binary search: lower bound; minimum capacity to ship in *D* days | GOOGLE · MICROSOFT · TECH-1 · ■■□ · T | [§1.13](#s1-13){.ref} |
| Q1.24 | Merge overlapping intervals | GOOGLE · AMAZON · TECH-1 · ■■□ · T | [§1.13](#s1-13){.ref} |
| Q1.25 | Coin change: fewest coins for an amount | MICROSOFT · GOOGLE · TECH-1 · ■■□ · T | [§1.14](#s1-14){.ref} |
| Q1.26 | LRU cache with O(1) `get` and `put` | MICROSOFT · AMAZON · TECH-1 · ■■□ · S | [§1.15](#s1-15){.ref} |
| Q1.27 | Token-bucket rate limiter and its router parameters | CISCO · JUNIPER · ARISTA · MICROSOFT · TECH-1 · ■■□ · T | [§1.15](#s1-15){.ref} |
| Q1.28 | Validate a sequence of TCP-style events against a state machine | JUNIPER · BROADCOM · TECH-1 · ■■□ · S | [§1.16](#s1-16){.ref} |

### Arrays, hashing, strings and bits

::: problems

::: q
### Q1.29 Merge two sorted arrays in place
[JUNIPER · OA · ■□□ · S]{.meta}

*Array `a` holds `m` sorted values followed by `n` unused cells; array `b` holds `n` sorted values. Merge `b` into `a` with no extra array.*

[30-second answer: fill `a` from the back, taking the larger of the two current tails, so no unread value is overwritten.]{.short}

**Approach.** Writing from the front would overwrite elements of `a` not yet read; writing from the back cannot, because the free cells are at the back. When `a` runs out, the rest of `b` is copied; when `b` runs out, the rest of `a` is already in place.

```cpp
void mergeInto(vector<int>& a, int m,
               vector<int>& b, int n) {
  int i = m - 1, j = n - 1, k = m + n - 1;
  while (j >= 0)
    a[k--] = (i >= 0 && a[i] > b[j])
             ? a[i--] : b[j--];
}
```

**Complexity.** O(*m* + *n*) time, O(1) space. **Follow-ups.** Stability (use `>` so equal values keep the order of `a` first). **Mistakes.** Looping while `i >= 0 && j >= 0` and forgetting to copy the remainder of `b`.
:::

::: q
### Q1.30 Rotate an array right by one, then by k
[JUNIPER · TECH-1 · ■□□ · S]{.meta}

*Rotate an array right by `k` positions in O(1) extra space.*

[30-second answer: reverse the whole array, then reverse the first `k` and the last `n-k` elements.]{.short}

**Approach.** For one step, save the last element, shift the rest right, and store it at the front: O(*n*). For *k* steps, rotating one at a time costs O(*nk*). Three reversals do it in O(*n*): reversing everything puts the last *k* elements first but backwards, and reversing each part restores their order. Reduce *k* modulo *n* first.

```cpp
void rotateRight(vector<int>& a, int k) {
  int n = a.size();
  if (!n) return;
  k %= n;
  reverse(a.begin(), a.end());
  reverse(a.begin(), a.begin() + k);
  reverse(a.begin() + k, a.end());
}
```

[1,2,3,4,5], *k* = 2: reversed 5,4,3,2,1; first two reversed 4,5,3,2,1; rest reversed 4,5,1,2,3, which is the right rotation. **Complexity.** O(*n*) time, O(1) space. **Mistakes.** Forgetting `k %= n` (and `n == 0`).
:::

::: q
### Q1.31 Move zeroes and remove an element in place
[JUNIPER · AMAZON · OA · ■□□ · T]{.meta}

*Move all zeroes of an array to the end, keeping the order of the other elements.*

[30-second answer: read/write pointers: copy each non-zero forward, then fill the tail with zeroes.]{.short}

```cpp
void moveZeroes(vector<int>& a) {
  size_t w = 0;
  for (size_t r = 0; r < a.size(); ++r)
    if (a[r]) a[w++] = a[r];
  while (w < a.size()) a[w++] = 0;
}
```

Removing a given value is the same loop with the test `a[r] != val`, returning `w`. **Complexity.** O(*n*) time, O(1) space, one write per kept element. **Mistakes.** Starting `w` at 1, or swapping elements needlessly (correct, but it does more writes).
:::

::: q
### Q1.32 Three Sum
[GOOGLE · MICROSOFT · TECH-1 · ■■□ · T]{.meta}

*Return all unique triples of an array whose sum is zero.*

[30-second answer: sort, fix the first value, and run opposite-end two pointers on the rest, skipping duplicates.]{.short}

**Approach.** Brute force is O(*n*³). After sorting, for each `i` the pair sum `-a[i]` is searched with two pointers in O(*n*), giving O(*n*²). Uniqueness comes from skipping equal values at `i`, and, after a hit, at both pointers.

```cpp
vector<vector<int>> threeSum(vector<int> a) {
  sort(a.begin(), a.end());
  vector<vector<int>> r;
  int n = a.size();
  for (int i = 0; i + 2 < n; ++i) {
    if (i && a[i] == a[i-1]) continue;
    int l = i + 1, h = n - 1;
    while (l < h) {
      long long s = (long long)a[i] + a[l] + a[h];
      if (s < 0) ++l;
      else if (s > 0) --h;
      else {
        r.push_back({a[i], a[l], a[h]});
        ++l; --h;
        while (l < h && a[l] == a[l-1]) ++l;
      }
    }
  }
  return r;
}
```

**Complexity.** O(*n*²) time, O(1) extra. **Mistakes.** Not skipping duplicates (repeated triples); using `int` for the sum.
:::

::: q
### Q1.33 Container with most water
[GOOGLE · AMAZON · TECH-1 · ■■□ · T]{.meta}

*Given heights `h[i]`, choose two lines maximising `min(h[i], h[j]) * (j - i)`.*

[30-second answer: start with the widest pair and always move the pointer at the shorter line, because only a taller line can improve the area.]{.short}

**Approach.** Moving the taller pointer can only reduce the width and cannot raise the minimum height, so it never helps; moving the shorter one might.

```cpp
int maxArea(const vector<int>& h) {
  int l = 0, r = h.size() - 1, best = 0;
  while (l < r) {
    best = max(best,
               min(h[l], h[r]) * (r - l));
    if (h[l] < h[r]) ++l; else --r;
  }
  return best;
}
```

**Complexity.** O(*n*) time, O(1) space.
:::

::: q
### Q1.34 Product of array except self
[AMAZON · MICROSOFT · TECH-1 · ■■□ · T]{.meta}

*Return an array whose `i`-th element is the product of all others, without division and in O(*n*).*

[30-second answer: the answer at `i` is (product of the elements before `i`) times (product of the elements after `i`); build the first in a forward pass and multiply in the second in a backward pass.]{.short}

```cpp
vector<int> productExceptSelf(
    const vector<int>& a) {
  int n = a.size();
  vector<int> r(n, 1);
  for (int i = 1; i < n; ++i)
    r[i] = r[i-1] * a[i-1];
  for (int i = n - 1, s = 1; i >= 0; --i) {
    r[i] *= s;
    s *= a[i];
  }
  return r;
}
```

**Complexity.** O(*n*) time, O(1) extra beyond the output. **Mistakes.** Using division fails when a value is zero. **Follow-ups.** The same prefix-and-suffix idea gives "trapping rain water".
:::

::: q
### Q1.35 Maximum subarray (Kadane)
[MICROSOFT · GOOGLE · OA · ■■□ · T]{.meta}

*Find the largest sum of a non-empty contiguous subarray.*

[30-second answer: at each element, either extend the best subarray ending before it or start afresh; keep the maximum seen.]{.short}

```cpp
int maxSubarray(const vector<int>& a) {
  int cur = a[0], best = a[0];
  for (size_t i = 1; i < a.size(); ++i) {
    cur = max(a[i], cur + a[i]);
    best = max(best, cur);
  }
  return best;
}
```

For `[-2,1,-3,4,-1,2,1,-5,4]`: `cur` runs −2, 1, −2, 4, 3, 5, 6, 1, 5 and `best` is 6 (the subarray `4,-1,2,1`). **Complexity.** O(*n*) time, O(1) space. **Mistakes.** Initialising `best` to 0, which is wrong when every value is negative.
:::

::: q
### Q1.36 Group anagrams
[AMAZON · GOOGLE · OA · ■■□ · T]{.meta}

*Group the strings of a list that are anagrams of each other.*

[30-second answer: two strings are anagrams exactly when their sorted letters agree, so use the sorted string as the map key.]{.short}

```cpp
vector<vector<string>> groupAnagrams(
    const vector<string>& v) {
  unordered_map<string, vector<string>> m;
  for (auto& s : v) {
    string k = s;
    sort(k.begin(), k.end());
    m[k].push_back(s);
  }
  vector<vector<string>> r;
  for (auto& p : m) r.push_back(p.second);
  return r;
}
```

**Complexity.** O(*N* *L* log *L*) for *N* strings of length at most *L*. **Follow-ups.** For lowercase letters only, a 26-count signature as the key gives O(*NL*).
:::

::: q
### Q1.37 Extract IPs from a log and sort by frequency
[GOOGLE · TECH-1 · ■□□ · S]{.meta}

*Read a log, find every IPv4 address, and print the addresses ordered by how often they occur (most frequent first, ties by address).*

[30-second answer: split the input into tokens, keep those that parse as IPv4, count them in a hash map, then sort the (address, count) pairs.]{.short}

**Approach.** Validation reuses `parse_ipv4` of [§1.4](#s1-4){.ref}. A single pass counts; the sort costs O(*d* log *d*) for *d* distinct addresses. A heap of size *k* replaces the sort when only the top *k* are wanted.

```cpp
extern "C" bool parse_ipv4(const char*,
                           uint32_t*);
vector<pair<string,int>> topIPs(istream& in) {
  unordered_map<string,int> cnt;
  string t; uint32_t x;
  while (in >> t)
    if (parse_ipv4(t.c_str(), &x)) ++cnt[t];
  vector<pair<string,int>> v(cnt.begin(),
                             cnt.end());
  sort(v.begin(), v.end(),
       [](auto& a, auto& b) {
    return a.second != b.second
        ? a.second > b.second
        : a.first < b.first; });
  return v;
}
```

**Complexity.** O(*N* + *d* log *d*) time, O(*d*) space. **Mistakes.** Counting `10.0.0.1:80` or `10.0.0.1,` as a different token; real logs need a scan for the dotted pattern rather than whitespace tokens.
:::

::: q
### Q1.38 Design a hash map in C
[ARISTA · JUNIPER · TECH-1 · ■■□ · T]{.meta}

*Implement `put`, `get` and `remove` for integer keys without a library.*

[30-second answer: an array of bucket heads, each a linked list; the bucket is `key % size`, and collisions share a list.]{.short}

```c
#define B 1009
typedef struct E { int k, v;
                   struct E *next; } E;
static E *tab[B];

static E **slot(int k) {   /* link to entry */
  E **pp = &tab[(unsigned)k % B];
  while (*pp && (*pp)->k != k)
    pp = &(*pp)->next;
  return pp;
}
void put(int k, int v) {
  E **pp = slot(k);
  if (*pp) { (*pp)->v = v; return; }
  E *e = malloc(sizeof *e);
  if (!e) return;
  e->k = k; e->v = v; e->next = NULL;
  *pp = e;
}
int get(int k, int *out) {
  E *e = *slot(k);
  if (!e) return 0;
  *out = e->v; return 1;
}
void remove_key(int k) {
  E **pp = slot(k);
  if (*pp) {
    E *d = *pp; *pp = d->next; free(d);
  }
}
```

**Complexity.** O(1) average, O(*n*) worst. **Follow-ups.** Resize when the load factor exceeds one; a prime size spreads keys evenly for simple moduli. The pointer-to-pointer idiom of [§1.6](#s1-6){.ref} removes the head special case.
:::

::: q
### Q1.39 Classify a string as IPv4, IPv6 or neither
[CISCO · AMAZON · MICROSOFT · TECH-1 · ■■□ · T]{.meta}

*Return which kind of address a string is. IPv6 here means eight groups of one to four hexadecimal digits separated by colons (no `::` compression).*

[30-second answer: choose the parser by the separator, then validate group by group, rejecting empty groups, too many digits and trailing text.]{.short}

**Approach.** IPv4 uses `parse_ipv4` of [§1.4](#s1-4){.ref}. IPv6 reads, for each of eight groups, one to four hex digits and then a colon (not after the last group), and requires the end of the string.

```c
#include <ctype.h>
bool valid_ipv6(const char *s) {
  for (int g = 0; g < 8; g++) {
    int n = 0;
    while (isxdigit((unsigned char)*s)) {
      s++; n++;
    }
    if (n < 1 || n > 4) return false;
    if (g < 7 && *s++ != ':') return false;
  }
  return *s == '\0';
}
```

Classification: contains `.` and no `:` → test IPv4; contains `:` → test IPv6; otherwise neither. **Complexity.** O(*n*). **Mistakes.** Accepting `01.1.1.1` or `1.1.1.1.`; letters beyond `f`; groups of five digits. Real parsers such as `inet_pton` also accept `::`, which needs a count of groups on each side.
:::

::: q
### Q1.40 String to integer (atoi) with clamping
[QUALCOMM · BROADCOM · OA · ■■□ · T]{.meta}

*Skip leading spaces, read an optional sign and digits, stop at the first other character, and clamp to the `int` range.*

[30-second answer: accumulate in a 64-bit value, stop growing once it passes the limit, apply the sign and clamp.]{.short}

```c
#include <limits.h>
int my_atoi(const char *s) {
  while (*s == ' ') s++;
  int neg = 0;
  if (*s == '+' || *s == '-')
    neg = (*s++ == '-');
  long long v = 0;
  while (*s >= '0' && *s <= '9') {
    v = v * 10 + (*s++ - '0');
    if (v > 2147483648LL) break;
  }
  if (neg) v = -v;
  if (v > INT_MAX) return INT_MAX;
  if (v < INT_MIN) return INT_MIN;
  return (int)v;
}
```

**Complexity.** O(*n*). **Mistakes.** Overflowing the accumulator before checking; treating `-` followed by a space as a number; mishandling `"-2147483648"`, which is exactly `INT_MIN`.
:::

::: q
### Q1.41 Compare version numbers
[CISCO · AMAZON · OA · ■■□ · T]{.meta}

*Compare `"1.01"` with `"1.001"`: dot-separated revisions are compared numerically from the left; missing revisions count as zero.*

[30-second answer: walk both strings at once, parse one number from each up to the next dot, and compare.]{.short}

```cpp
int compareVersion(const string& a,
                   const string& b) {
  size_t i = 0, j = 0;
  while (i < a.size() || j < b.size()) {
    long x = 0, y = 0;
    while (i < a.size() && a[i] != '.')
      x = x * 10 + (a[i++] - '0');
    while (j < b.size() && b[j] != '.')
      y = y * 10 + (b[j++] - '0');
    if (x != y) return x < y ? -1 : 1;
    ++i; ++j;
  }
  return 0;
}
```

**Complexity.** O(*n* + *m*) time, O(1) space. **Mistakes.** Comparing revisions as strings (so `"9"` > `"10"`); splitting into arrays when a scan suffices.
:::

::: q
### Q1.42 Expressive words (stretchy strings)
[CISCO · OA · ■■□ · S]{.meta}

*A word is stretchy to `S` if repeated letter groups in the word can be extended to length at least three to give `S`. Count the stretchy words in a list.*

[30-second answer: compare run-length groups: each pair of groups has the same letter, and the group in `S` either equals the word's group or is longer and has length at least three.]{.short}

```cpp
bool stretchy(const string& s,
              const string& w) {
  size_t i = 0, j = 0;
  while (i < s.size() && j < w.size()) {
    if (s[i] != w[j]) return false;
    size_t i2 = i, j2 = j;
    while (i2 < s.size() && s[i2] == s[i])
      ++i2;
    while (j2 < w.size() && w[j2] == w[j])
      ++j2;
    size_t a = i2 - i, b = j2 - j;
    if (a < b || (a != b && a < 3))
      return false;
    i = i2; j = j2;
  }
  return i == s.size() && j == w.size();
}
```

For `S = "heeellooo"`, `"hello"` is stretchy (e: 3 ≥ 3, l: 2 = 2, o: 3 ≥ 3) but `"hi"` is not. **Complexity.** O(|`S`| + |word|) per word. **Mistakes.** Allowing a group of size two to stretch (it must already match or reach three).
:::

::: q
### Q1.43 Longest common prefix of strings
[GOOGLE · AMAZON · OA · ■□□ · T]{.meta}

*Return the longest string that begins every string of a list.*

[30-second answer: compare column by column against the first string and stop at the first mismatch.]{.short}

```cpp
string lcp(const vector<string>& v) {
  if (v.empty()) return "";
  for (size_t i = 0; i < v[0].size(); ++i)
    for (auto& s : v)
      if (i == s.size() || s[i] != v[0][i])
        return v[0].substr(0, i);
  return v[0];
}
```

**Complexity.** O(total characters). **Follow-ups.** For two IPv4 addresses the common prefix in *bits* is `clz(a ^ b)` (with 32 when equal), the shape of the CIDR block that covers both. A trie handles many strings with repeated queries.
:::

::: q
### Q1.44 Count the bits to flip to turn A into B
[QUALCOMM · TECH-1 · ■□□ · S]{.meta}

*How many bit positions differ between two integers?*

[30-second answer: XOR marks the differing positions; count the set bits of the result.]{.short}

```c
unsigned flips(uint32_t a, uint32_t b) {
  uint32_t x = a ^ b;
  unsigned c = 0;
  while (x) { x &= x - 1; c++; }
  return c;
}
```

`flips(10, 20)`: 01010 ^ 10100 = 11110, four set bits, so four flips. **Complexity.** O(number of differing bits). **Follow-ups.** The Hamming distance of two addresses; `__builtin_popcount` as the one-line form.
:::

::: q
### Q1.45 Multiply without the `*` operator
[JUNIPER · TECH-1 · ■■□ · S]{.meta}

*Multiply two integers using only shifts, additions and tests.*

[30-second answer: shift-and-add: for each set bit of the multiplier, add the shifted multiplicand.]{.short}

```c
unsigned mul(unsigned a, unsigned b) {
  unsigned r = 0;
  while (b) {
    if (b & 1) r += a;
    a <<= 1;
    b >>= 1;
  }
  return r;
}
```

`mul(6, 5)`: b = 101 adds 6 (b bit 0) and 6 << 2 = 24 (bit 2): 30. **Complexity.** O(bit-width) = O(32). **Follow-ups.** For signed operands, multiply the absolute values and apply the sign (the sign is the XOR of the signs). Also ask: what if the result overflows?
:::

::: q
### Q1.46 Power of two, and counting bits for 0 to n
[QUALCOMM · BROADCOM · OA · ■□□ · T]{.meta}

*Test whether *x* is a power of two in one expression. Then return the popcount of every number from 0 to *n*.*

[30-second answer: a power of two has exactly one set bit, so `x && !(x & (x-1))`; for the table, `bits[i] = bits[i >> 1] + (i & 1)`.]{.short}

```cpp
bool isPow2(unsigned x) {
  return x && !(x & (x - 1));
}
vector<int> countBits(int n) {
  vector<int> b(n + 1, 0);
  for (int i = 1; i <= n; ++i)
    b[i] = b[i >> 1] + (i & 1);
  return b;
}
```

**Complexity.** O(1) and O(*n*). **Mistakes.** Omitting `x &&`, which wrongly accepts zero.
:::

::: q
### Q1.47 Reverse the bits of a 32-bit integer
[QUALCOMM · BROADCOM · TECH-1 · ■■□ · T]{.meta}

*Reverse the bit order of a `uint32_t`. Make it fast for a million calls.*

[30-second answer: a loop over 32 bits works; for many calls, precompute a 256-entry byte-reversal table and swap the four bytes.]{.short}

```c
static uint8_t rev8[256];
void init_rev(void) {
  for (int i = 0; i < 256; i++)
    rev8[i] = (rev8[i >> 1] >> 1)
              | ((i & 1) << 7);
}
uint32_t rev32(uint32_t x) {
  return (uint32_t)rev8[x & 255] << 24
       | (uint32_t)rev8[(x >> 8) & 255] << 16
       | (uint32_t)rev8[(x >> 16) & 255] << 8
       | rev8[x >> 24];
}
```

The table recurrence reverses `i` by reversing `i >> 1`, moving it down one place and putting the low bit of `i` on top. **Complexity.** O(1) per call after an O(256) set-up. **Follow-ups.** The mask-and-swap ladder (swap halves, then pairs, then nibbles, bytes) needs no table.
:::

::: q
### Q1.48 Single number (every other value appears twice, or thrice)
[GOOGLE · QUALCOMM · OA · ■■□ · T]{.meta}

*In an array where every value appears exactly twice except one, find the odd one out. Then solve it when the others appear three times.*

[30-second answer: twice: XOR everything, since equal values cancel. Thrice: keep, per bit, a count modulo 3 using two accumulators.]{.short}

```cpp
int single2(const vector<int>& a) {
  int x = 0;
  for (int v : a) x ^= v;
  return x;
}
int single3(const vector<int>& a) {
  int ones = 0, twos = 0;
  for (int v : a) {
    ones = (ones ^ v) & ~twos;
    twos = (twos ^ v) & ~ones;
  }
  return ones;
}
```

In `single3`, `ones` holds the bits seen once (mod 3) and `twos` those seen twice; a third occurrence clears both. **Complexity.** O(*n*) time, O(1) space.
:::

::: q
### Q1.49 Bitwise AND of a range
[JUNIPER · GOOGLE · TECH-1 · ■■□ · T]{.meta}

*Return the AND of all integers in [`m`, `n`].*

[30-second answer: the answer is the common binary prefix of `m` and `n`, followed by zeros; shift both right until they are equal, then shift back.]{.short}

```cpp
int rangeAnd(int m, int n) {
  int s = 0;
  while (m != n) { m >>= 1; n >>= 1; ++s; }
  return m << s;
}
```

Any bit position that differs between `m` and `n` takes both values somewhere in the range, so it ANDs to zero, along with every lower bit. This is the same idea as the common prefix of two IP addresses. **Complexity.** O(32).
:::

::: q
### Q1.50 Add without `+`; divide without `/`
[JUNIPER · QUALCOMM · TECH-1 · ■■□ · T]{.meta}

*Add two integers with bit operations only. Then divide two integers without `*`, `/` or `%`.*

[30-second answer: addition is XOR (sum without carries) plus AND shifted left (carries), repeated until no carry remains; division is shift-and-subtract from the highest bit down.]{.short}

```c
int add(int a, int b) {
  unsigned x = a, y = b;
  while (y) {
    unsigned c = (x & y) << 1;
    x ^= y;
    y = c;
  }
  return (int)x;
}
```

```cpp
int divide(int a, int b) {
  if (a == INT_MIN && b == -1)
    return INT_MAX;
  bool neg = (a < 0) != (b < 0);
  unsigned long long x = llabs((long long)a),
                     y = llabs((long long)b), q = 0;
  for (int i = 31; i >= 0; --i)
    if ((x >> i) >= y) {
      x -= y << i;
      q |= 1ull << i;
    }
  return (int)(neg ? -(long long)q
                   : (long long)q);
}
```

**Complexity.** O(32) each. **Mistakes.** Negating `INT_MIN` in 32-bit arithmetic (undefined); not handling `INT_MIN / -1`, whose true result does not fit.
:::

::: q
### Q1.51 Convert an IP range to the fewest CIDR blocks
[CISCO · GOOGLE · TECH-2 · ■■■ · T]{.meta}

*Given a start address and a count `n`, cover exactly those `n` consecutive addresses with the fewest CIDR blocks.*

[30-second answer: repeatedly take the largest block that is aligned at the current address and no bigger than what remains.]{.short}

**Approach.** A block of size 2^*k* must start at a multiple of 2^*k*, so the largest allowed size at address `a` is its lowest set bit, `a & -a` (the whole space when `a` is zero). Shrink the size by halves until it fits in `n`, emit the block with prefix length 32 − *k*, and advance.

```cpp
vector<pair<uint32_t,int>> rangeToCidr(
    uint32_t a, uint64_t n) {
  vector<pair<uint32_t,int>> out;
  while (n > 0) {
    uint64_t size = a ? (a & -a) : (1ull << 32);
    while (size > n) size >>= 1;
    out.push_back({a, 32 - __builtin_ctzll(size)});
    a += size;
    n -= size;
  }
  return out;
}
```

For 255.0.0.7 and *n* = 10: block 255.0.0.7/32 (alignment 1), then 255.0.0.8/29 (alignment 8, 8 ≤ 9), then 255.0.0.16/32 (alignment 16 shrunk to 1). **Complexity.** O(32) blocks at most, each O(32). **Mistakes.** Choosing the largest power of two below `n` without the alignment test, which yields blocks that are not valid prefixes.
:::

::: q
### Q1.52 The Internet checksum
[CISCO · JUNIPER · BROADCOM · TECH-1 · ■■□ · T]{.meta}

*Compute the 16-bit one's-complement checksum of a byte buffer, as used by IPv4, ICMP, UDP and TCP.*

[30-second answer: add the data as 16-bit big-endian words, fold the carries back into the low 16 bits, and complement the result.]{.short}

```c
uint16_t checksum(const uint8_t *p, size_t n) {
  uint32_t sum = 0;
  for (; n > 1; p += 2, n -= 2)
    sum += (uint32_t)p[0] << 8 | p[1];
  if (n) sum += (uint32_t)p[0] << 8;
  while (sum >> 16)
    sum = (sum & 0xFFFF) + (sum >> 16);
  return (uint16_t)~sum;
}
```

For the bytes `45 00 00 73`, the words are 0x4500 and 0x0073, the sum is 0x4573 and the checksum is 0xBA8C. A receiver that sums the data including the checksum obtains 0xFFFF, which is the test. **Complexity.** O(*n*). **Mistakes.** Forgetting the odd trailing byte (padded with a zero low byte); folding the carry only once; reading the words in host byte order on a little-endian machine.
:::

::: q
### Q1.53 Allocate VLAN identifiers with a bitmap
[ARISTA · BROADCOM · TECH-1 · ■■□ · T]{.meta}

*Manage the 4096 VLAN IDs: allocate the lowest free one, free one, in constant time per word.*

[30-second answer: a bitmap of 64 words; find a word that is not all ones, take its lowest zero bit with a count-trailing-zeros instruction.]{.short}

```c
#define NW (4096 / 64)
static uint64_t used[NW];
int alloc_vlan(void) {
  for (int w = 0; w < NW; w++)
    if (~used[w]) {
      int b = __builtin_ctzll(~used[w]);
      used[w] |= 1ull << b;
      return w * 64 + b;
    }
  return -1;
}
void free_vlan(int id) {
  used[id / 64] &= ~(1ull << (id % 64));
}
```

**Complexity.** O(64) per allocation, O(1) per free. **Follow-ups.** Reserve IDs 0 and 4095 by presetting their bits; a two-level summary bitmap makes allocation O(1). **Mistakes.** Shifting a 32-bit `1` (use `1ull`).
:::

:::
:::
:::
