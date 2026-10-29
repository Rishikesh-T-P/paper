::: {.p2}

::: pack
## Problem Set, continued: Python, C++ and coding items {#ps2b}

::: problems

::: q
### Q2.39 Python: given `show ip interface brief` text, list the interfaces whose status or protocol is not up.
[AMAZON NDE · TECH-1 · ■□□ · S]{.meta}

[30-second answer: split each line into whitespace-separated fields, take the name from the first and the status and protocol from the last fields, and filter.]{.short}

```python
def parse_brief(text):
    out = {}
    for line in text.splitlines():
        f = line.split()
        if len(f) < 6 or not re.match(r"[A-Za-z]+\d", f[0]):
            continue                                   # skips the header and blank lines
        out[f[0]] = (" ".join(f[4:-1]), f[-1])         # status may be two words
    return out
bad = [i for i, sp in parse_brief(text).items() if sp != ("up", "up")]
```

For the three-interface sample (Gi0/1 up/up, Gi0/2 `administratively down`/down, Gi0/3 up/down) the result is `['GigabitEthernet0/2', 'GigabitEthernet0/3']`. **Mistake.** `split(" ")` instead of `split()`, which breaks on runs of spaces. **Follow-up.** Structured output (JSON) is preferable when the device offers it; see [Pillar 10](#ch10){.ref}.
:::

::: q
### Q2.40 Python: extract IP addresses from a log and sort by frequency. What if the file is 50 GB?
[GOOGLE · TECH-1 · ■■□ · S]{.meta}

[30-second answer: stream the file line by line into a `Counter`; memory depends on the number of distinct addresses, not on the file size.]{.short}

**Answer.** The pipeline `Counter(src_ips(read_lines(path))).most_common(k)` of [2.17](#s2-17){.ref} runs in one pass, O(n) time. If the distinct set does not fit, partition addresses by hash into several files and count each, or sort externally. For the top `k` only, `heapq.nlargest` costs O(n log k). **Mistake.** `f.readlines()`, which loads everything.
:::

::: q
### Q2.41 Python: time complexity of `x in list` versus `x in set`? Why?
[GOOGLE · AMAZON · OA · ■□□ · I]{.meta}

[30-second answer: O(n) for a list, because it compares each element; O(1) on average for a set, because it hashes the key and inspects one bucket.]{.short}

**Answer.** Hence membership tests inside loops should use a set built once. The set requires hashable (immutable) elements, and its worst case is O(n) with many collisions.
:::

::: q
### Q2.42 Python: explain the mutable default argument bug.
[GOOGLE · MICROSOFT · OA · ■□□ · I]{.meta}

[30-second answer: a default value is evaluated once at definition time, so a default list or dict is shared by all calls that omit the argument.]{.short}

**Answer.** `def f(x, acc=[])` returns `[1, 2]` for both `f(1)` and `f(2)` as printed after the second call. Fix: `acc=None` and `if acc is None: acc = []` ([2.16](#s2-16){.ref}).
:::

::: q
### Q2.43 Python: what is the difference between `is` and `==`? What is a shallow copy?
[MICROSOFT · GOOGLE · OA · ■□□ · T]{.meta}

[30-second answer: `==` compares values and `is` compares object identity; a shallow copy duplicates the container but shares the elements.]{.short}

**Answer.** `a = [[0]] * 2` makes two references to one inner list; `a[0].append(1)` changes both rows. Use `is` only against `None`. For independent nested copies use `copy.deepcopy` or a comprehension `[[0] for _ in range(2)]`.
:::

::: q
### Q2.44 Tell me about an automation script you wrote: what it did, how you tested it and how it failed.
[AMAZON NDE · TECH-2 · ■■□ · S]{.meta}

[30-second answer: describe one concrete script in four parts: the manual task it replaced, how it handled bad input and device errors, how you tested it safely, and one failure with the fix and what you now do differently.]{.short}

**Approach.** Choose a script of your own, for example one that collects `show` output from several devices and reports mismatches. State the scale (devices, minutes saved). Testing: a dry-run mode, a lab or a single device first, unit tests on saved outputs. Failure: a timeout on one device that stopped the run, fixed with per-device `try/except`, a timeout and a summary. Use the STAR frame of Part II. **Mistake.** Claiming no failures.
:::

::: q
### Q2.45 C++: what is a virtual function and how is it implemented? Why a virtual destructor?
[NOKIA · CISCO · TECH-1 · ■■□ · I]{.meta}

[30-second answer: a virtual function is chosen by the object's dynamic type through a hidden vptr to a per-class vtable; the destructor must be virtual so that `delete` through a base pointer runs the derived destructor.]{.short}

**Answer.** Figure 2.7. Cost: one pointer per object and one indirect call. A class with `virtual` members and an `int` is 16 bytes on LP64, without them 4. Without a virtual destructor, `delete base_ptr` runs only `~Base`, which is undefined. **Follow-up.** Pure virtual (`= 0`) makes the class abstract.
:::

::: q
### Q2.46 C++: what is RAII? Give an example with locks or files.
[MICROSOFT · GOOGLE · TECH-1 · ■■□ · I]{.meta}

[30-second answer: tie a resource to an object's lifetime, acquiring in the constructor and releasing in the destructor, so that every exit path, including an exception, releases it.]{.short}

**Answer.** `std::lock_guard<std::mutex> g(m);` locks at construction and unlocks when `g` leaves scope; `std::ifstream` closes its file; `std::unique_ptr` frees memory. Destruction order is the reverse of construction (output of `work(true)` in [2.19](#s2-19){.ref}).
:::

::: q
### Q2.47 C++: `map` versus `unordered_map`: implementation and complexity?
[GOOGLE · MICROSOFT · TECH-1 · ■□□ · I]{.meta}

[30-second answer: `map` is a balanced tree, ordered, O(log n) per operation; `unordered_map` is a hash table, unordered, O(1) on average and O(n) worst case.]{.short}

**Answer.** Choose `map` when sorted iteration or range queries (`lower_bound`) are needed, `unordered_map` for plain lookup. `operator[]` inserts a default value for a missing key; use `find` or `count` to test. Keys of `unordered_map` need a hash function.
:::

::: q
### Q2.48 C++: when are iterators and pointers into a `vector` invalidated?
[GOOGLE · TECH-1 · ■■□ · T]{.meta}

[30-second answer: whenever the vector reallocates (growth beyond capacity, `reserve`), and for elements at or after the point of an `insert` or `erase`.]{.short}

**Answer.** With `v{1,2,3}`, `p = &v[0]` and `v.reserve(100)`, the comparison `p == &v[0]` is false. Fixes: reserve before taking pointers, keep indices, or use `list`. **Mistake.** Erasing inside a range-for; use `it = v.erase(it)` or the erase-remove idiom.
:::

::: q
### Q2.49 C++: explain `unique_ptr`, `shared_ptr` and `weak_ptr`. How do cycles leak?
[MICROSOFT · GOOGLE · TECH-1 · ■■□ · T]{.meta}

[30-second answer: `unique_ptr` is a sole, movable owner; `shared_ptr` shares ownership by reference count; `weak_ptr` observes without owning and breaks cycles.]{.short}

**Answer.** Two `shared_ptr` nodes pointing at each other keep both counts at least 1, so neither destructor runs; making the back-link a `weak_ptr` frees both. Default to `unique_ptr`; create with `make_unique` or `make_shared`.
:::

::: q
### Q2.50 C++: what is object slicing, and what are the rules of zero, three and five?
[NOKIA · MICROSOFT · TECH-2 · ■■□ · T]{.meta}

[30-second answer: slicing copies only the base part of a derived object into a base object, losing derived data and virtual behaviour; the rules say which special members to write when a class owns a resource.]{.short}

**Answer.** `Shape sl = circle;` makes `sl.area()` return the base result 0. Pass polymorphic objects by pointer or reference. Rule of zero: own resources through members such as `vector` and `unique_ptr` and write no special members. Rules of three and five: if you write a destructor, copy or move operation, define or delete all of copy constructor, copy assignment, destructor and (five) the two move operations.
:::

::: q
### Q2.51 Describe what happens on the stack when a function is called.
[CISCO · QUALCOMM · TECH-1 · ■■□ · T]{.meta}

[30-second answer: the caller places arguments (in registers on x86-64, the rest on the stack) and a call instruction pushes the return address; the callee saves the frame pointer and reserves space for its locals; return reverses this.]{.short}

**Answer.** A frame holds the return address, the saved frame pointer, locals and spills. A buffer overflow of a local array can overwrite the return address, which is why `gets` and unchecked `strcpy` are exploitable and why stack protectors place a canary value before the return address. Details of the call stack and virtual memory: [Pillar 7](#ch7){.ref}.
:::

::: q
### Q2.52 Swap two integers in three ways. Why does the XOR swap fail when both pointers are the same?
[QUALCOMM · TECH-1 · ■□□ · T]{.meta}

[30-second answer: with a temporary, with addition and subtraction, and with XOR; the XOR swap sets the value to zero if both pointers alias the same object.]{.short}

```c
void swap_tmp(int *a, int *b)       { int t = *a; *a = *b; *b = t; }
void swap_add(unsigned *a, unsigned *b) { *a = *a + *b; *b = *a - *b; *a = *a - *b; }
void swap_xor(unsigned *a, unsigned *b) { *a ^= *b; *b ^= *a; *a ^= *b; }
```

**Why.** If `a == b`, the first XOR makes the object `x ^ x = 0`, and the rest keep it zero. The unsigned types avoid signed overflow in the addition version. The temporary version is the one to write: it is clearest and compilers optimise it.
:::

::: q
### Q2.53 Count the set bits of a 32-bit value; test for a power of two.
[QUALCOMM · TECH-1 · ■□□ · S]{.meta}

[30-second answer: `x &= x - 1` clears the lowest set bit, so count the iterations; a power of two has exactly one set bit.]{.short}

```c
int popcount(uint32_t x) { int n = 0; while (x) { x &= x - 1; n++; } return n; }
int is_pow2(uint32_t x)  { return x && !(x & (x - 1)); }
```

**Complexity.** O(number of set bits). `popcount(0xF0F0)` is 8, `is_pow2(64)` is 1 and `is_pow2(96)` is 0. GCC: `__builtin_popcount`.
:::

::: q
### Q2.54 Reverse a string in place.
[BROADCOM · OA · ■□□ · T]{.meta}

[30-second answer: swap characters from both ends with two pointers until they meet.]{.short}

```c
void reverse(char *s) {
    if (!*s) return;
    char *i = s, *j = s + strlen(s) - 1;
    while (i < j) { char t = *i; *i++ = *j; *j-- = t; }
}
```

`"router"` becomes `"retuor"`. **Mistakes.** Passing a string literal (read-only; use an array) and computing `strlen(s) - 1` for the empty string, where `size_t` wraps.
:::

::: q
### Q2.55 Convert a dotted quad to a `uint32_t` with validation, and back.
[CISCO · JUNIPER · TECH-1 · ■■□ · T]{.meta}

[30-second answer: parse four decimal fields of at most three digits and value at most 255, separated by single dots, shifting each into place; reject anything else.]{.short}

```c
int dotted_to_u32(const char *s, uint32_t *out) {
    uint32_t addr = 0; int parts = 0;
    for (;;) {
        if (*s < '0' || *s > '9') return -1;
        unsigned v = 0; int digits = 0;
        while (*s >= '0' && *s <= '9') {
            v = v * 10 + (unsigned)(*s++ - '0');
            if (++digits > 3 || v > 255) return -1;
        }
        addr = (addr << 8) | v;
        if (++parts == 4) break;
        if (*s++ != '.') return -1;
    }
    if (*s != '\0') return -1;
    *out = addr; return 0;
}
```

`"192.168.1.10"` returns 0 with `0xC0A8010A` (host order; apply `htonl` for the wire). `"1.2.3"`, `"1.2.3.256"` and `"1.2.3.4.5"` return -1. The reverse is `u32_to_dotted` in [2.14](#s2-14){.ref}. **Mistake.** Accepting empty fields (`1..2.3`) or trailing junk.
:::

::: q
### Q2.56 Implement a circular buffer with power-of-two size.
[BROADCOM · QUALCOMM · TECH-1 · ■■□ · I]{.meta}

[30-second answer: keep two free-running counters and mask them with `size - 1`; the buffer is empty when they are equal and full when they differ by the size.]{.short}

```c
#define RB_SIZE 8                                  /* power of two */
struct ring { uint8_t buf[RB_SIZE]; unsigned head, tail; };
int rb_put(struct ring *r, uint8_t b) {
    if (r->head - r->tail == RB_SIZE) return -1;   /* full  */
    r->buf[r->head++ & (RB_SIZE - 1)] = b; return 0;
}
int rb_get(struct ring *r, uint8_t *b) {
    if (r->head == r->tail) return -1;             /* empty */
    *b = r->buf[r->tail++ & (RB_SIZE - 1)]; return 0;
}
```

Ten puts into an empty ring succeed 8 times; the first get returns 0. Unsigned subtraction keeps `head - tail` correct after the counters wrap. **Why the mask.** `& (N-1)` replaces `% N` and wastes no slot. One producer and one consumer need no lock if the counters are atomic.
:::

::: q
### Q2.57 Write a bounds-safe TLV (type-length-value) parser that rejects truncated and overlong items.
[CISCO · JUNIPER · TECH-2 · ■■■ · T]{.meta}

[30-second answer: before reading each item, check that two header bytes remain, then that the declared length fits in what remains; subtract rather than add, to avoid overflow.]{.short}

```c
int tlv_walk(const uint8_t *p, size_t len) {
    size_t off = 0;
    while (off < len) {
        if (len - off < 2) return -1;              /* no room for type and length */
        unsigned t = p[off], l = p[off + 1];
        if (l > len - off - 2) return -1;          /* value would run past the end */
        printf("type %u len %u\n", t, l);
        off += 2 + l;
    }
    return 0;
}
```

For `{1,2,0xAA,0xBB,2,0}` it prints `type 1 len 2` and `type 2 len 0`, returning 0; for `{1,5,0xAA}` it returns -1. **Mistake.** Testing `off + 2 + l > len`, which can overflow for wide length fields. Use a 16- or 32-bit length the same way.
:::

::: q
### Q2.58 Build a MAC learning table with a hash and ageing.
[ARISTA · BROADCOM · TECH-2 · ■■□ · T]{.meta}

[30-second answer: hash the 6-byte MAC into a bucket of chained entries; a frame refreshes or inserts the entry for its source MAC, lookups return the port, and an ageing sweep removes entries not seen for the timeout.]{.short}

```c
struct mac_ent { uint8_t mac[6]; uint16_t port; uint32_t seen; struct mac_ent *next; };
static struct mac_ent *tab[8];
static unsigned h(const uint8_t *m) { uint32_t x = 2166136261u; for (int i = 0; i < 6; i++) { x ^= m[i]; x *= 16777619u; } return x % 8; }
void learn(const uint8_t *m, uint16_t port, uint32_t now) {
    struct mac_ent **pp = &tab[h(m)];
    for (; *pp; pp = &(*pp)->next)
        if (!memcmp((*pp)->mac, m, 6)) { (*pp)->port = port; (*pp)->seen = now; return; }
    struct mac_ent *e = calloc(1, sizeof *e); if (!e) return;
    memcpy(e->mac, m, 6); e->port = port; e->seen = now; *pp = e;
}
void age(uint32_t now, uint32_t max) {
    for (int i = 0; i < 8; i++)
        for (struct mac_ent **pp = &tab[i]; *pp; ) {
            if (now - (*pp)->seen > max) { struct mac_ent *d = *pp; *pp = d->next; free(d); }
            else pp = &(*pp)->next;
        }
}
```

Learning MAC A on port 3 at time 100, B on port 4 at 200, and A again on port 5 at 210, a lookup gives 5 and 4; `age(305, 100)` removes B (105 s old) and keeps A (95 s). The lookup loop is the same as in `learn`. A station moving between ports is handled by the update branch. Why the switch behaves this way: [Pillar 4](#ch4){.ref}.
:::

::: q
### Q2.59 Write a fixed-size pool allocator for packet buffers.
[BROADCOM · CISCO · TECH-2 · ■■■ · T]{.meta}

[30-second answer: carve a static array into equal blocks and keep free blocks on a singly linked list threaded through the blocks themselves; allocation and free are O(1) pointer swaps.]{.short}

```c
#define POOL_N 4
#define BUF_SZ 64
static union blk { union blk *next; uint8_t data[BUF_SZ]; } pool[POOL_N];
static union blk *freelist;
void  pool_init(void)   { for (int i = 0; i < POOL_N; i++) { pool[i].next = freelist; freelist = &pool[i]; } }
void *pool_alloc(void)  { union blk *b = freelist; if (b) freelist = b->next; return b; }
void  pool_free(void *p){ union blk *b = p; b->next = freelist; freelist = b; }
```

The union lets a free block store the link where an allocated block stores data, so there is no per-block overhead. After four allocations the fifth returns `NULL`; after `pool_free(y)` the next allocation returns `y`. **Benefits.** No fragmentation, no `malloc` latency, bounded memory. **Follow-ups.** Thread safety (a lock or per-core pools) and alignment of `BUF_SZ`.
:::

::: q
### Q2.60 Write a re-entrant tokeniser in the style of `strtok_r`.
[BROADCOM · QUALCOMM · TECH-2 · ■■■ · T]{.meta}

[30-second answer: keep the scan position in a caller-supplied pointer instead of a static variable; skip leading delimiters, mark the token's end with a NUL, and save the position after it.]{.short}

```c
char *my_strtok_r(char *s, const char *delim, char **save) {
    if (!s) s = *save;
    s += strspn(s, delim);                 /* skip leading delimiters */
    if (!*s) { *save = s; return NULL; }
    char *tok = s;
    s += strcspn(s, delim);                /* find the end of the token */
    if (*s) *s++ = '\0';
    *save = s;
    return tok;
}
```

On `"a,b;;c"` with delimiters `",;"` the tokens are `[a][b][c]`; consecutive delimiters give no empty token. The input is modified, so it must be writable. Plain `strtok` keeps its state in a hidden static, so it is not thread-safe.
:::

::: q
### Q2.61 Write a `printf`-lite supporting `%d %x %s %c` using `stdarg.h`.
[BROADCOM · QUALCOMM · TECH-2 · ■■■ · T]{.meta}

[30-second answer: walk the format string; copy ordinary characters, and on `%` read the matching argument with `va_arg` and print it in the right base.]{.short}

```c
int my_printf(const char *fmt, ...) {
    va_list ap; va_start(ap, fmt); int n = 0;
    for (; *fmt; fmt++) {
        if (*fmt != '%') { putchar(*fmt); n++; continue; }
        switch (*++fmt) {
        case 'd': { int v = va_arg(ap, int); char b[12]; int i = 0;
                    unsigned u = v < 0 ? 0u - (unsigned)v : (unsigned)v;
                    do { b[i++] = (char)('0' + u % 10); u /= 10; } while (u);
                    if (v < 0) { putchar('-'); n++; }
                    while (i) { putchar(b[--i]); n++; } break; }
        case 'x': { unsigned u = va_arg(ap, unsigned); char b[9]; int i = 0;
                    do { b[i++] = "0123456789abcdef"[u & 15]; u >>= 4; } while (u);
                    while (i) { putchar(b[--i]); n++; } break; }
        case 's': { const char *s = va_arg(ap, const char *); while (*s) { putchar(*s++); n++; } break; }
        case 'c': putchar(va_arg(ap, int)); n++; break;
        case '%': putchar('%'); n++; break;
        default:  putchar('%'); putchar(*fmt); n += 2;
        }
    }
    va_end(ap); return n;
}
```

`my_printf("%s=%d %x %c %% %d\n", "ttl", 64, 255, 'z', -5)` prints `ttl=64 ff z % -5` and returns 17. `char` is read as `int` because of the default argument promotions. **Mistake.** Reading with the wrong type, which is undefined, exactly as in a real `printf`.
:::

::: q
### Q2.62 Python: count the lines containing `ERROR`; build a dictionary from `show` output lines.
[GOOGLE · AMAZON · OA · ■□□ · T]{.meta}

[30-second answer: a generator expression with `sum` counts lazily; a dictionary comprehension pairs the first two fields of each line.]{.short}

```python
n = sum(1 for line in open(path) if "ERROR" in line)          # 2 for lines ERROR a, ok, ERROR b
states = {k: v for k, v in (l.split()[:2] for l in lines)}    # {'Gi0/1': 'up', 'Gi0/2': 'down'}
```

Use `with open(path) as f` in production so the file is closed. For the dictionary, skip blank lines first, since `l.split()[:2]` of an empty line unpacks to the wrong length.
:::

::: q
### Q2.63 Python: unpack an IPv4 header with `struct` and verify its checksum.
[CISCO · JUNIPER · TECH-1 · ■■□ · T]{.meta}

[30-second answer: unpack with `"!BBHHHBBH4s4s"`, then add all 16-bit words with end-around carry; a valid header sums to `0xFFFF`.]{.short}

```python
def csum_ok(hdr: bytes) -> bool:
    if len(hdr) % 2: hdr += b"\x00"
    total = sum(struct.unpack(f"!{len(hdr) // 2}H", hdr))
    while total >> 16: total = (total & 0xFFFF) + (total >> 16)    # fold the carries
    return total == 0xFFFF
```

For the header of [2.14](#s2-14){.ref} it returns `True`; clearing the checksum bytes (positions 10 and 11) gives `False`. The unpack is in [2.18](#s2-18){.ref}. **Mistake.** Native format `"BBHH..."` instead of `!`, giving the wrong order and padding.
:::

::: q
### Q2.64 Python: a log-to-`Counter`-to-top-k report with `argparse`.
[GOOGLE · TECH-1 · ■■□ · S]{.meta}

[30-second answer: parse arguments, stream the file into a `Counter` keyed by the first field, and print `most_common(k)`.]{.short}

```python
def main(argv=None):
    ap = argparse.ArgumentParser(description="Top talkers")
    ap.add_argument("logfile"); ap.add_argument("-k", type=int, default=3)
    a = ap.parse_args(argv)
    c = Counter()
    with open(a.logfile) as f:
        for line in f:
            parts = line.split()
            if parts: c[parts[0]] += 1                 # skip blank lines
    for ip, n in c.most_common(a.k): print(f"{n:6d}  {ip}")
```

On a file with `1.1.1.1` three times, `2.2.2.2` twice and `3.3.3.3` once, `-k 2` prints `     3  1.1.1.1` and `     2  2.2.2.2`. `argparse` supplies `--help` and error messages free. Add `if __name__ == "__main__": main()`.
:::

::: q
### Q2.65 Python: a streaming parser for a 10 GB flow log, reporting the top sources by bytes.
[GOOGLE · AMAZON NDE · TECH-2 · ■■■ · T]{.meta}

[30-second answer: a generator yields (source, bytes) pairs and skips malformed lines; a dictionary accumulates totals; `heapq.nlargest` selects the top k.]{.short}

```python
def flow_bytes(lines):
    for l in lines:
        p = l.split()
        if len(p) == 3 and p[2].isdigit(): yield p[0], int(p[2])   # src dst bytes

tot = defaultdict(int)
for src, b in flow_bytes(open(path)): tot[src] += b
top = heapq.nlargest(2, tot.items(), key=lambda kv: kv[1])
```

With lines `10.0.0.1 10.0.0.9 1500`, `10.0.0.2 10.0.0.9 40`, `10.0.0.1 10.0.0.8 900`, `10.0.0.3 10.0.0.9 2000` and a malformed line, the result is `[('10.0.0.1', 2400), ('10.0.0.3', 2000)]`. Memory is proportional to the number of sources. **Follow-up.** For billions of sources use sampling or a count-min sketch; neither is needed at interview depth.
:::

::: q
### Q2.66 C++: implement `RingBuffer<T, N>` as a template.
[BROADCOM · QUALCOMM · TECH-2 · ■■□ · T]{.meta}

[30-second answer: the C ring buffer of Q2.56 with the element type and capacity as template parameters and a compile-time check that `N` is a power of two.]{.short}

```cpp
template <typename T, std::size_t N>
class RingBuffer {
    static_assert(N > 0 && (N & (N - 1)) == 0, "N must be a power of two");
    std::array<T, N> buf_{};
    std::size_t head_ = 0, tail_ = 0;                  // free-running counters
public:
    bool push(const T &v) { if (size() == N) return false; buf_[head_++ & (N - 1)] = v; return true; }
    bool pop(T &out)      { if (empty()) return false; out = buf_[tail_++ & (N - 1)]; return true; }
    std::size_t size() const { return head_ - tail_; }
    bool empty() const { return head_ == tail_; }
};
```

For `RingBuffer<int, 4>`, six pushes give four successes; the first `pop` yields 0 and `size()` is then 3. Storage is inside the object, so there is no allocation.
:::

::: q
### Q2.67 C++: implement a move-only `unique_ptr`-lite.
[MICROSOFT · GOOGLE · TECH-2 · ■■■ · T]{.meta}

[30-second answer: own a raw pointer, delete it in the destructor, delete the copy operations and implement the move operations by stealing the pointer and nulling the source.]{.short}

```cpp
template <typename T> class UniquePtr {
    T *p_;
public:
    explicit UniquePtr(T *p = nullptr) noexcept : p_(p) {}
    ~UniquePtr() { delete p_; }
    UniquePtr(const UniquePtr &) = delete;
    UniquePtr &operator=(const UniquePtr &) = delete;
    UniquePtr(UniquePtr &&o) noexcept : p_(o.p_) { o.p_ = nullptr; }
    UniquePtr &operator=(UniquePtr &&o) noexcept {
        if (this != &o) { delete p_; p_ = o.p_; o.p_ = nullptr; }
        return *this;
    }
    T &operator*() const { return *p_; }
    T *operator->() const { return p_; }
    T *release() { T *t = p_; p_ = nullptr; return t; }
    explicit operator bool() const { return p_ != nullptr; }
};
```

For an object that prints in its constructor and destructor, `UniquePtr<Tr> b = std::move(a);` leaves `a` empty and `b` owning, and "dtor" is printed exactly once. **Mistakes.** Forgetting the self-assignment check and `noexcept` on the move operations (containers use the copy path otherwise).
:::

:::

**Questions solved in other pillars.** Several topics reported for this pillar's companies belong elsewhere and are solved there once. The mutex and deadlock question ("What is a mutex? How do you prevent deadlock?"), thread-safe flags and the socket API belong to [Pillar 7](#ch7){.ref}. The Bash one-liner for the ten most frequent source addresses, and the scripting items, belong to [Pillar 8](#ch8){.ref}. The linked-list library, the least-recently-used cache and the longest-prefix-match trie belong to [Pillar 1](#ch1){.ref}. Python libraries for devices (`ipaddress`, `netmiko`, concurrent reachability checks) belong to [Pillar 10](#ch10){.ref}.
:::

:::
