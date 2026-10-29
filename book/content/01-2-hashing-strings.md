::: {.p1}

## [1.3]{.sec}Hashing: maps and sets [Must · ■□□]{.tag} {#s1-3}

::: bigidea
A hash table turns "have I seen this?" from a scan into a single computed lookup, which is why so many O(*n*²) solutions collapse to O(*n*).
:::

[**Hash function** — a function mapping a key to an integer; equal keys must give equal values, and different keys should rarely collide.]{.margin}A hash table stores each key in a bucket chosen by `hash(key) mod m`. Two keys sharing a bucket collide, and the usual remedy, *chaining*, keeps a short list in each bucket. With a good hash and a load factor (entries per bucket) kept below about one, a lookup inspects a constant expected number of entries. Thus, insert, find and erase are O(1) on average, but O(*n*) in the worst case when many keys collide. The ordered `map` in C++ is a balanced tree instead: O(log *n*) per operation, but it keeps keys sorted.

| Need | Structure | Cost |
|---|---|---|
| membership, no order | `unordered_set` | O(1) average |
| key → value, no order | `unordered_map` | O(1) average |
| sorted iteration, nearest key | `set`, `map` | O(log *n*) |
| counts of small integers or letters | array indexed by value | O(1), smallest constant |

A switch's MAC table and a router's flow table are the networking forms of this structure: the key is the destination MAC or the 5-tuple, and the value is the egress port or the action. Further, when values are bounded by a small range, a plain array replaces the hash and is faster.

*Recognise:* "have we seen", "count occurrences", "pair that …", "group by", "first non-repeating", "duplicate". *Typical templates:* a set for membership, a map for counts, and a sorted or canonical form of an item as the key (for anagrams, the sorted letters).

<figure>
<svg viewBox="0 0 440 185" width="475"><defs><marker id="a10" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#1A1D23"/></marker></defs>
<text class="sm" x="10" y="12" text-anchor="start">bucket = key mod 6</text><rect class="box" x="10" y="22" width="30" height="22"/><text class="mono" x="25" y="37" text-anchor="middle">0</text><line class="ln" x1="40" y1="33" x2="70" y2="33" marker-end="url(#a10)"/><rect class="box" x="70" y="22" width="44" height="22"/><text class="mono" x="92" y="37" text-anchor="middle">12</text><line class="ln" x1="114" y1="33" x2="140" y2="33" marker-end="url(#a10)"/><rect class="box" x="140" y="22" width="44" height="22"/><text class="mono" x="162" y="37" text-anchor="middle">18</text><rect class="box" x="10" y="48" width="30" height="22"/><text class="mono" x="25" y="63" text-anchor="middle">1</text><text class="sm" x="60" y="63" text-anchor="start">empty</text><rect class="box" x="10" y="74" width="30" height="22"/><text class="mono" x="25" y="89" text-anchor="middle">2</text><line class="ln" x1="40" y1="85" x2="70" y2="85" marker-end="url(#a10)"/><rect class="box" x="70" y="74" width="44" height="22"/><text class="mono" x="92" y="89" text-anchor="middle">8</text><rect class="box" x="10" y="100" width="30" height="22"/><text class="mono" x="25" y="115" text-anchor="middle">3</text><line class="ln" x1="40" y1="111" x2="70" y2="111" marker-end="url(#a10)"/><rect class="box" x="70" y="100" width="44" height="22"/><text class="mono" x="92" y="115" text-anchor="middle">21</text><line class="ln" x1="114" y1="111" x2="140" y2="111" marker-end="url(#a10)"/><rect class="box" x="140" y="100" width="44" height="22"/><text class="mono" x="162" y="115" text-anchor="middle">9</text><line class="ln" x1="184" y1="111" x2="210" y2="111" marker-end="url(#a10)"/><rect class="box" x="210" y="100" width="44" height="22"/><text class="mono" x="232" y="115" text-anchor="middle">15</text><rect class="box" x="10" y="126" width="30" height="22"/><text class="mono" x="25" y="141" text-anchor="middle">4</text><text class="sm" x="60" y="141" text-anchor="start">empty</text><rect class="box" x="10" y="152" width="30" height="22"/><text class="mono" x="25" y="167" text-anchor="middle">5</text><line class="ln" x1="40" y1="163" x2="70" y2="163" marker-end="url(#a10)"/><rect class="box" x="70" y="152" width="44" height="22"/><text class="mono" x="92" y="167" text-anchor="middle">23</text><text class="sm" x="300" y="60" text-anchor="start">load factor = entries / buckets = 7 / 6</text><text class="sm" x="300" y="74" text-anchor="start">lookup(15): bucket 3, then walk</text><text class="sm" x="300" y="88" text-anchor="start">the chain 21, 9, 15</text><text class="sm" x="300" y="110" text-anchor="start">when the load factor passes 1:</text><text class="sm" x="300" y="124" text-anchor="start">double the buckets and re-insert</text>
</svg>
<figcaption><b>Figure 1.5</b> A hash table with chaining. Keys that collide share a bucket's list; the expected chain length equals the load factor.</figcaption>
</figure>

Two collision strategies exist. *Chaining* keeps a list per bucket, as drawn; deletion is easy and the table degrades gracefully when full. *Open addressing* stores entries in the array itself and probes to the next free cell (linear probing) after a collision; it is more compact and faster to scan, but it needs a load factor well below one, and deletion needs a tombstone marker. When the load factor passes a threshold the table doubles its bucket count and re-inserts every entry, an O(*n*) step that is amortised over the insertions exactly as for the dynamic array of [§1.1](#s1-1){.ref}.

::: example
**Longest consecutive sequence.** Given an unsorted array, find the length of the longest run of consecutive integers (for example 1, 2, 3, 4), in O(*n*) time.

1. Sorting gives O(*n* log *n*); the target forbids it.
2. Put all values in a set. A value *x* starts a run exactly when *x* − 1 is absent.
3. For each start, extend with `x+1, x+2, …` while present. Each element is visited once as a start-check and at most once inside a run, so the total is O(*n*).

```cpp
int longestConsecutive(const vector<int>& a) {
    unordered_set<int> s(a.begin(), a.end());
    int best = 0;
    for (int x : s) {
        if (s.count(x - 1)) continue;          // not the start of a run
        int y = x;
        while (y < INT_MAX && s.count(y + 1)) ++y;
        best = max(best, y - x + 1);               // run length
    }
    return best;
}
```

| x | x − 1 present? | run extended | length |
|---|---|---|---|
| 100 | no | 100 | 1 |
| 4 | yes | skipped | – |
| 200 | no | 200 | 1 |
| 1 | no | 1, 2, 3, 4 | 4 |

[Result for `[100, 4, 200, 1, 3, 2]`: 4. Time O(*n*), space O(*n*).]{.result}
:::

::: trap
*Claim:* `m[key]` is a harmless way to test whether a key exists. *Why it is wrong:* in C++ the subscript operator inserts a default value when the key is absent, which changes the map and its size during the test. *Correct statement:* use `find` or `count` to test, and `[]` only when inserting or incrementing is intended.
:::

### Hashing network keys: a flow table

A router or firewall keeps per-flow state in a hash table whose key is the 5-tuple (source address, destination address, source port, destination port, protocol). Two points make this a favourite question. First, one must hash the *fields*, not the bytes of the struct, because a C struct may contain padding bytes whose values are unspecified; two equal keys could then hash differently. Secondly, equality must compare the same fields.

```c
#include <stdint.h>
#include <stdbool.h>

typedef struct {
    uint32_t src, dst;
    uint16_t sport, dport;
    uint8_t  proto;
} FlowKey;

static uint32_t fnv_byte(uint32_t h, uint8_t b) {
    return (h ^ b) * 16777619u;
}

uint32_t flow_hash(const FlowKey *k) {  /* FNV-1a over the fields */
    uint32_t h = 2166136261u;
    uint32_t w[3] = { k->src, k->dst, (uint32_t)k->sport << 16 | k->dport };
    for (int i = 0; i < 3; i++)
        for (int b = 0; b < 32; b += 8)
            h = fnv_byte(h, (uint8_t)(w[i] >> b));
    return fnv_byte(h, k->proto);
}
bool flow_eq(const FlowKey *a, const FlowKey *b) {
    return a->src == b->src && a->dst == b->dst && a->sport == b->sport
        && a->dport == b->dport && a->proto == b->proto;
}
```

The bucket is `flow_hash(k) % nbuckets`. *Follow-ups.* To make the two directions of a connection land in the same entry, order the two (address, port) pairs before hashing. Equal-cost multipath forwarding applies the same idea in hardware: a hash of the 5-tuple selects the path, so all packets of a flow take one path and arrive in order, while different flows spread over the paths.

::: check
1. Which is faster for counting lowercase letters: `unordered_map<char,int>` or `int cnt[26]`? [^c1-6]
2. What is the worst-case lookup in a chained hash table, and when does it occur? [^c1-7]
:::

[^c1-6]: The array, since it has no hashing or allocation; both are O(*n*) overall.
[^c1-7]: O(*n*), when every key lands in one bucket, for example with a poor hash or adversarial input.

## [1.4]{.sec}Strings and parsing network data [Must · ■■□]{.tag} {#s1-4}

::: bigidea
Parsing is validation first and conversion second, because network input is untrusted and every malformed case an interviewer can imagine is a test case.
:::

A C string is an array of `char` ended by a zero byte, so `strlen` must walk the whole string and costs O(*n*). Hence a loop written `for (i = 0; i < strlen(s); i++)` is O(*n*²), because the length is recomputed on every iteration. A C++ `string` stores its length and answers `size()` in O(1). A string literal in C is read-only, so writing to `char *p = "abc"` is undefined behaviour; copy it into an array first.

::: trap
*Claim:* `strncpy(dst, src, n)` is a safe `strcpy`. *Why it is wrong:* when `src` has `n` or more characters, `strncpy` copies exactly `n` characters and writes no terminating zero. *Correct statement:* always set `dst[n-1] = '\0'` after `strncpy`, or use `snprintf(dst, n, "%s", src)`, which always terminates.
:::

*Recognise:* "valid", "parse", "split", "tokens", dotted or colon-separated text, "log lines". *Method:* scan once with an index; at each field check its character class, its length and its numeric range, and then check that nothing remains. Do not use `atoi` or `strtok` for validation: `atoi` accepts leading spaces, signs and trailing garbage and cannot report an error, and `strtok` modifies its input and keeps hidden state.

The function below parses a dotted-quad IPv4 address into a host-order 32-bit integer. It rejects an empty octet, a non-digit, a value above 255, a leading zero ("01") and trailing characters.

```c
#include <stdint.h>
#include <stdbool.h>

bool parse_ipv4(const char *s, uint32_t *out) {
    uint32_t addr = 0;
    for (int part = 0; part < 4; part++) {
        if (*s < '0' || *s > '9') return false;  /* empty octet or junk */
        const char *start = s;
        int val = 0, digits = 0;
        while (*s >= '0' && *s <= '9') {
            val = val * 10 + (*s - '0');
            if (++digits > 3 || val > 255) return false;
            s++;
        }
        if (digits > 1 && *start == '0') return false;  /* leading zero */
        addr = (addr << 8) | (uint32_t)val;
        if (part < 3) {
            if (*s != '.') return false;
            s++;
        }
    }
    if (*s != '\0') return false;  /* trailing junk */
    *out = addr;
    return true;
}
```

| Input | Result | Reason |
|---|---|---|
| `192.168.1.1` | true, 0xC0A80101 | four valid octets |
| `01.2.3.4` | false | leading zero in first octet |
| `1.2.3` | false | after the third octet the next character is the terminator, not a dot |
| `1.2.3.4.5` | false | trailing characters remain after the fourth octet |
| `1..2.3` | false | second octet is empty |
| `256.1.1.1` | false | value exceeds 255 |

The reverse conversion extracts each byte with a shift and a mask, using `%u` with an explicit cast because `uint32_t` is not guaranteed to be `unsigned int`:

```c
void format_ipv4(uint32_t a, char buf[16]) {  /* 15 characters + NUL */
    snprintf(buf, 16, "%u.%u.%u.%u",
             (unsigned)(a >> 24), (unsigned)((a >> 16) & 255),
             (unsigned)((a >> 8) & 255), (unsigned)(a & 255));
}
```

A MAC address follows the same pattern with hexadecimal digits and colons. Note how the second digit is read only after the first has been validated, so the code never reads past the terminator.

```c
static int hexval(char c) {
    if (c >= '0' && c <= '9') return c - '0';
    if (c >= 'a' && c <= 'f') return c - 'a' + 10;
    if (c >= 'A' && c <= 'F') return c - 'A' + 10;
    return -1;
}
bool parse_mac(const char *s, uint8_t mac[6]) {
    for (int i = 0; i < 6; i++) {
        int hi = hexval(s[0]), lo = hi < 0 ? -1 : hexval(s[1]);
        if (hi < 0 || lo < 0) return false;
        mac[i] = (uint8_t)(hi << 4 | lo);
        s += 2;
        if (i < 5) { if (*s != ':') return false; s++; }
    }
    return *s == '\0';
}
```

An IPv6 address adds one difficulty, the *zero compression* `::`, which stands for one or more groups of zeros and may appear once. The method is to collect the groups before and after the `::` in two arrays, and to place the second array at the end of the 16 bytes, leaving the zeros in between.

```c
bool parse_ipv6(const char *s, uint8_t out[16]) {
    uint16_t g[2][8];                     /* groups before and after "::" */
    int n[2] = {0, 0}, side = 0;
    if (s[0] == ':') {                    /* a leading colon must be "::" */
        if (s[1] != ':') return false;
        side = 1; s += 2;
    }
    while (*s) {
        unsigned v = 0; int digits = 0;
        while (isxdigit((unsigned char)*s)) {
            v = v * 16 + (unsigned)hexval(*s++);
            if (++digits > 4) return false;
        }
        if (digits == 0 || n[0] + n[1] >= 8) return false;
        g[side][n[side]++] = (uint16_t)v;
        if (!*s) break;
        if (*s++ != ':') return false;
        if (*s == ':') {                  /* "::" */
            if (side == 1) return false;  /* only one allowed */
            side = 1; s++;
        } else if (!*s) return false;     /* trailing single colon */
    }
    int total = n[0] + n[1];
    if (side == 0 ? total != 8 : total > 7) return false;
    memset(out, 0, 16);
    for (int i = 0; i < n[0]; i++) {
        out[2*i] = g[0][i] >> 8;  out[2*i + 1] = g[0][i] & 0xFF;
    }
    for (int i = 0; i < n[1]; i++) {
        int pos = 8 - n[1] + i;           /* right-aligned */
        out[2*pos] = g[1][i] >> 8;  out[2*pos + 1] = g[1][i] & 0xFF;
    }
    return true;
}
```

Without a `::` exactly eight groups are required; with one, at most seven, because `::` must replace at least one group. For `2001:db8::1`, the groups before the gap are `2001` and `0db8`, the group after it is `1`, and the 16 bytes are `20 01 0d b8` followed by ten zero bytes and `00 01`. The forms with an embedded IPv4 suffix (`::ffff:192.0.2.1`) are omitted here; they add a final step that calls `parse_ipv4`.

A CIDR string `a.b.c.d/p` is handled by parsing the address up to the slash, then parsing *p* as a decimal number in 0–32 with the same no-leading-zero rule. Validation of IPv6 groups and the reporting problems built on these parsers are in the Problem Set ([Problem Set](#ps1){.ref}).

### Substring search

*Idea.* To find a pattern of length *m* in a text of length *n*, the naive method compares at every start position and costs O(*nm*) in the worst case (`aaaa…ab` against `aaab`). The Knuth–Morris–Pratt (KMP) method never moves backwards in the text. It precomputes, for each prefix of the pattern, the length of the longest proper prefix that is also a suffix; after a mismatch, that length says how much of the pattern is still known to match. *Recognise:* "find the pattern", "repeated substring", "does *B* occur in *A*". *Complexity:* O(*n* + *m*) time, O(*m*) space.

```cpp
vector<int> prefixFunction(const string& p) {   // pi[i]: border of p[0..i]
    vector<int> pi(p.size(), 0);
    for (size_t i = 1, k = 0; i < p.size(); ++i) {
        while (k && p[i] != p[k]) k = pi[k - 1];   // shorter border
        if (p[i] == p[k]) ++k;
        pi[i] = k;
    }
    return pi;
}
int findFirst(const string& s, const string& p) {  // first index or -1
    if (p.empty()) return 0;
    vector<int> pi = prefixFunction(p);
    for (size_t i = 0, k = 0; i < s.size(); ++i) {
        while (k && s[i] != p[k]) k = pi[k - 1];
        if (s[i] == p[k]) ++k;
        if (k == p.size()) return (int)(i - k + 1);
    }
    return -1;
}
```

For the pattern `ababc`, the table is `pi = [0, 0, 1, 2, 0]`: for example `abab` has the border `ab`, so `pi[3] = 2`. Searching `abababc`, the match length `k` runs 1, 2, 3, 4 over `abab`, then the text character `a` meets pattern character `c` and `k` falls back from 4 to `pi[3] = 2` instead of restarting at zero; the match then continues 3, 4, 5 and ends at index 6, so the answer is 6 − 5 + 1 = 2. The pointer `i` never moves back, which is the source of the linear bound. A common alternative is the rolling hash of Rabin and Karp: hash each window of length *m* in O(1) by removing the leading character and adding the trailing one, and verify only on a hash match; it runs in O(*n* + *m*) on average and extends to many patterns at once.

::: lab
`LAB 1.4 · 10 MIN` Check the parser against the C library, which is the reference implementation. Put `hexval` and `parse_ipv6` of this section in `v6.c`, with the driver below, and compile.

```c
#include <arpa/inet.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
/* ... hexval() and parse_ipv6() from this section ... */
int main(void) {
    const char *t[] = { "::", "::1", "1::", "2001:db8::ff00:42:8329",
        "1:2:3:4:5:6:7:8", "1:2:3:4:5:6:7::", "1::2::3", ":1:2:3:4:5:6:7",
        "12345::", "1:2:3:4:5:6:7:8:9", "1:2:3:4:5:6:7:8:", "g::1",
        "1:::2" };
    int bad = 0;
    for (size_t i = 0; i < sizeof t / sizeof *t; i++) {
        uint8_t mine[16], ref[16];
        int a = parse_ipv6(t[i], mine);
        int b = inet_pton(AF_INET6, t[i], ref) == 1;
        int same = (a == b) && (!a || memcmp(mine, ref, 16) == 0);
        printf("%-26s mine=%d lib=%d %s\n", t[i], a, b,
               same ? "ok" : "MISMATCH");
        bad += !same;
    }
    printf("%d mismatches\n", bad);
    return bad != 0;
}
```

```
$ gcc -Wall -o v6 v6.c && ./v6
::                         mine=1 lib=1 ok
::1                        mine=1 lib=1 ok
1::                        mine=1 lib=1 ok
2001:db8::ff00:42:8329     mine=1 lib=1 ok
1:2:3:4:5:6:7:8            mine=1 lib=1 ok
1:2:3:4:5:6:7::            mine=1 lib=1 ok
1::2::3                    mine=0 lib=0 ok
:1:2:3:4:5:6:7             mine=0 lib=0 ok
12345::                    mine=0 lib=0 ok
1:2:3:4:5:6:7:8:9          mine=0 lib=0 ok
1:2:3:4:5:6:7:8:           mine=0 lib=0 ok
g::1                       mine=0 lib=0 ok
1:::2                      mine=0 lib=0 ok
0 mismatches
```

**What you should notice:** the seven malformed strings (two `::`, a leading single colon, five-digit group, nine groups, trailing colon, non-hex letter, three colons) are all rejected by both, and the valid ones give identical bytes. Add your own cases; every mismatch is a bug in one of the two, and the library is usually right.
:::

::: check
1. Why is `01.2.3.4` rejected even though `atoi("01")` is 1? [^c1-8]
2. What goes wrong with `char buf[15]` in `format_ipv4`? [^c1-9]
:::

[^c1-8]: Leading zeros are ambiguous (some parsers read them as octal), so strict validators reject them.
[^c1-9]: The longest address `255.255.255.255` has 15 characters, and the terminating zero needs a sixteenth byte.

:::
