::: {.p2}

## [2.10]{.sec}Dynamic memory and leaks [Must · ■■□]{.tag} {#s2-10}

Automatic variables vanish when their block ends, so data that must outlive a call, or whose size is known only at run time, comes from the heap. `malloc(n)` returns a block of `n` uninitialised bytes or `NULL`; `calloc(k, size)` returns `k * size` zeroed bytes and fails cleanly if the product overflows; `realloc(p, n)` resizes a block, possibly moving it; `free(p)` returns it. All blocks come from the allocator, which keeps a few header bytes before each block, and `free(NULL)` is defined to do nothing.

```c
int *a = malloc(100 * sizeof *a);      /* sizeof *a stays correct if the type changes */
if (!a) return -1;                     /* always test */
int *tmp = realloc(a, 200 * sizeof *a);
if (!tmp) { free(a); return -1; }      /* on failure the old block is still valid */
a = tmp;
free(a); a = NULL;                     /* NULL makes a second free harmless */
```

The idiom with `tmp` is mandatory. In `p = realloc(p, n)` a failure overwrites `p` with `NULL` and the only reference to the old block is lost. When `realloc` cannot grow a block in place it allocates a new one, copies the contents and frees the old block, so every pointer into the old block becomes invalid.

Five defects account for nearly all heap bugs, and each has a tool that finds it.

| Defect | What happens | Tool that reports it |
|---|---|---|
| Memory leak | the last pointer to a block is lost or `free` is never called | valgrind, LeakSanitizer |
| Use after free | the block is read or written after `free` | AddressSanitizer, valgrind |
| Double free | `free` on the same pointer twice; the allocator's lists are corrupted | AddressSanitizer, glibc abort message |
| Buffer overflow | a write past the end of the block | AddressSanitizer, valgrind |
| Dangling pointer | a pointer outlives its object, whether freed heap or an expired local | AddressSanitizer (heap and stack) |

A *leak* costs nothing in a short program and exhausts memory in a router process that runs for months; it is therefore treated as a defect. The program below loses its only pointer.

```c
char *a = malloc(16);
strcpy(a, "leak");
a = NULL;                  /* last reference lost */
```

::: lab
`LAB 2.3 · 10 MIN`

```bash
gcc -g -fsanitize=address -o leak leak.c && ./leak
```

```
ERROR: LeakSanitizer: detected memory leaks
Direct leak of 16 byte(s) in 1 object(s) allocated from:
    #1 ... in main leak.c:4
SUMMARY: AddressSanitizer: 16 byte(s) leaked in 1 allocation(s).
```

**What you should notice:** the report names the size and the line of the `malloc`. With valgrind, `valgrind --leak-check=full ./leak` prints the same fact as "definitely lost: 16 bytes in 1 blocks".
:::

Returning a pointer to a local is the stack counterpart. `char *f(void) { char buf[16] = "x"; return buf; }` returns the address of storage that is dead the moment `f` returns; the compiler warns, and the behaviour is undefined. The remedies are to let the caller pass the buffer, to allocate on the heap, or to return a `static` buffer (not re-entrant).

::: trap
*Claim:* after `free(p)` the pointer is `NULL`, or at least safe to test. *Why it is wrong:* `free` receives a copy of `p` and cannot change the caller's variable, so `p` still holds the old address. *Correct statement:* assign `p = NULL` yourself after `free`; then a second `free(p)` is harmless and a dereference faults immediately instead of corrupting memory silently.
:::

::: check
1. Why does `calloc(n, 4)` differ from `malloc(n * 4)` apart from zeroing? [^c2-16]
2. What happens to other pointers into a block after `realloc` moves it? [^c2-17]
:::

[^c2-16]: `calloc` detects overflow of the multiplication and returns `NULL`, whereas `n * 4` may wrap and yield a block that is too small.
[^c2-17]: They dangle, because the old block has been freed.

## [2.11]{.sec}The preprocessor and macros [Must · ■■□]{.tag} {#s2-11}

Before compilation the *preprocessor* performs textual substitution; it knows nothing of types or scopes. A macro `#define NAME text` replaces each occurrence of `NAME` by `text`, and a function-like macro `#define F(x) text` does so with its arguments pasted in unevaluated. Everything that goes wrong follows from this single fact.

```c
#define SQ(x)  x*x
#define SQ2(x) ((x)*(x))
SQ(2+3)    /* 2+3*2+3  = 11 */      SQ2(2+3)  /* ((2+3)*(2+3)) = 25 */
10/SQ(2)   /* 10/2*2   = 10 */      #define MAX(a,b) ((a)>(b)?(a):(b))
MAX(i++, j)/* i++ is evaluated twice: with i = 1, j = 0 the result is 2 and i becomes 3 */
```

Hence three rules: parenthesise every parameter and the whole body; never pass an argument with side effects; and prefer a `static inline` function when types are known, because it evaluates its arguments once and is type-checked. A macro remains the right tool for code that must stay generic, for `__FILE__` and `__LINE__` capture, and for conditional compilation.

A multi-statement macro must be wrapped as `do { ... } while (0)`. Without it, `#define SWAP(a,b) t=a; a=b; b=t;` used as `if (c) SWAP(x,y); else ...` breaks the `if` and fails to compile, because only the first statement belongs to the `if`. The wrapper turns the body into one statement that takes the trailing semicolon.

Two operators help. The `#` operator turns an argument into a string and `##` pastes two tokens. To stringify the *value* of a macro one needs two levels, because `#` stops expansion.

```c
#define N 4
#define STR(x)  #x
#define XSTR(x) STR(x)
#define CAT(a,b) a##b
STR(N)  /* "N" */    XSTR(N)  /* "4" */    int CAT(x,1) = 5;   /* declares x1 */
```

*Include guards* prevent a header being processed twice: wrap it in `#ifndef NET_H`, `#define NET_H`, ..., `#endif`, or use `#pragma once`. Conditional compilation (`#ifdef DEBUG`) selects code at build time.

The *X-macro* keeps a list in one place and generates several tables from it, so that an enumeration and its printable names can never fall out of step. It is a favourite way to write protocol state tables.

```c
#define STATES(X) X(CLOSED) X(LISTEN) X(ESTABLISHED)
#define AS_ENUM(n) S_##n,
#define AS_STR(n)  #n,
enum state { STATES(AS_ENUM) S_COUNT };               /* S_CLOSED, S_LISTEN, ..., 3 */
static const char *names[] = { STATES(AS_STR) };      /* "CLOSED", "LISTEN", ...    */
/* names[S_LISTEN] is "LISTEN" */
```

::: lens
[CISCO · QUALCOMM]{.co}

"What is wrong with `#define SQUARE(x) x*x`? What happens with `SQUARE(i++)`?" and "macro versus inline function" are reported Cisco questions. A strong answer shows `SQ(2+3)` giving 11, the parenthesised fix, and that `SQ2(i++)` multiplies `i++` by `i++`, an unsequenced double modification and therefore undefined. Follow-up: when is a macro better than an inline function (generic code, stringification, `__LINE__`).
:::

::: check
1. What does `XSTR(N)` give when `N` is defined as `4`, and why does `STR(N)` differ? [^c2-18]
2. Why wrap a multi-statement macro in `do { } while (0)`? [^c2-19]
:::

[^c2-18]: `"4"`; the argument of `STR` is not macro-expanded before `#` is applied, whereas the extra level in `XSTR` expands it first.
[^c2-19]: It makes the body a single statement, so the macro behaves correctly after `if` without braces and with a trailing semicolon.

## [2.12]{.sec}Undefined behaviour [Must · ■■□]{.tag} {#s2-12}

The standard distinguishes three kinds of unspecified outcome. *Implementation-defined* behaviour varies but must be documented, such as the signedness of `char` or the result of right-shifting a negative number. *Unspecified* behaviour is a choice among allowed outcomes that need not be documented, such as the order in which function arguments are evaluated. *Undefined behaviour* (UB) places no requirement at all on the program: it may crash, print the expected result, or be compiled to something else entirely.

::: bigidea
The compiler assumes that undefined behaviour never occurs and optimises on that assumption, so a program with UB can fail in ways unrelated to the faulty line.
:::

The common sources are the following. (i) Signed integer overflow. (ii) Dereferencing `NULL`, a dangling or an out-of-bounds pointer, including one past the end. (iii) Reading an uninitialised automatic variable. (iv) Modifying an object twice between sequence points, as in `i = i++ + ++i`. (v) Shifting by a negative count or by the type's width or more, and left-shifting into the sign bit. (vi) Modifying a string literal or a `const` object. (vii) Accessing an object through a pointer of an incompatible type (the *strict aliasing* rule). (viii) Using memory after `free`, or freeing twice. (ix) Falling off the end of a non-`void` function and using the result. (x) A data race between threads.

The consequences are visible in generated code. The function `int f(int x) { return x + 1 > x; }` is compiled by gcc to `movl $1, %eax; ret`: signed overflow cannot happen, so the comparison is always true, although for `x = INT_MAX` the machine addition would wrap. A check written as `if (x + 1 < x) overflow();` can be removed in the same way, so the correct test is `if (x == INT_MAX)`, or arithmetic done in unsigned types.

::: lab
`LAB 2.4 · 10 MIN`

```bash
gcc -g -fsanitize=undefined -o ub ub.c && ./ub     # prints x + 1 with x = INT_MAX
```

```
ub.c:3:75: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
-2147483648
```

**What you should notice:** the plain build prints only the wrapped value. The sanitiser reports the file, line and operands, so that a silent wrap becomes a located error. Run test suites with `-fsanitize=address,undefined` before concluding a program is correct.
:::

An interview answer about UB has three parts: name the category, say why the standard leaves it open (portability to processors that trap, and permission to optimise), and give the tool that detects it. Unsigned overflow, by contrast, is defined and wraps, which makes it the right type for counters, hashes and sequence numbers.

::: check
1. Is `a[i] = i++;` defined? [^c2-20]
2. Is `-8 >> 1` defined? [^c2-21]
:::

[^c2-20]: No; `i` is read and modified without sequencing, so the behaviour is undefined.
[^c2-21]: It is implementation-defined, not undefined; gcc performs an arithmetic shift and yields -4.

## [2.13]{.sec}Writing the library: memcpy to itoa [Must · ■■□]{.tag} {#s2-13}

Interviewers ask for the standard functions because each hides one subtle decision. The versions below are written for clarity; production libraries copy a word at a time but must give the same results.

```c
size_t my_strlen(const char *s) { const char *p = s; while (*p) p++; return (size_t)(p - s); }

char *my_strcpy(char *d, const char *s) {
    char *r = d;
    while ((*d++ = *s++)) ;               /* copies the terminator, then the test is 0 */
    return r;
}

int my_strcmp(const char *a, const char *b) {
    while (*a && *a == *b) { a++; b++; }
    return (unsigned char)*a - (unsigned char)*b;   /* compare as unsigned bytes */
}
```

`strcmp` compares as `unsigned char`, which is why the cast is present: with a plain signed `char`, a byte above 127 would compare below an ASCII letter. The pitfalls of `my_strcpy` are the missing size check and overlapping arguments.

`memcpy` copies `n` bytes and requires that the regions do not overlap. `memmove` allows overlap, so it must choose the copying direction: if the destination lies *before* the source, copy forwards; if it lies inside the source region *after* its start, copy backwards, otherwise a forward copy would overwrite source bytes that have not yet been read.

```c
void *my_memcpy(void *dst, const void *src, size_t n) {
    unsigned char *d = dst; const unsigned char *s = src;
    while (n--) *d++ = *s++;
    return dst;
}
void *my_memmove(void *dst, const void *src, size_t n) {
    unsigned char *d = dst; const unsigned char *s = src;
    if (d == s || n == 0) return dst;
    if ((uintptr_t)d < (uintptr_t)s || (uintptr_t)d >= (uintptr_t)s + n) {
        while (n--) *d++ = *s++;           /* forwards: safe when no harmful overlap */
    } else {
        d += n; s += n;
        while (n--) *--d = *--s;           /* backwards: destination overlaps the tail */
    }
    return dst;
}
```

With `char s[16] = "abcdef"`, calling `my_memmove(s+2, s, 4)` leaves `"ababcd"`, and `my_memmove(s, s+2, 4)` on a fresh copy leaves `"cdefef"`. Applying `my_memcpy` (or the real `memcpy`) to the first case is undefined, and a forward byte loop would give `"ababab"` because the first copied bytes are overwritten before they are read. Casting through `uintptr_t` before comparing pointers avoids comparing unrelated objects, which the standard does not define.

`atoi` hides four decisions: skip leading whitespace, accept one sign, stop at the first non-digit, and refuse to overflow. The version below clamps, as the common LeetCode variant requires; the overflow test is written so that it never overflows itself.

```c
int my_atoi(const char *s) {
    while (*s == ' ' || (*s >= '\t' && *s <= '\r')) s++;
    int neg = 0;
    if (*s == '-' || *s == '+') neg = (*s++ == '-');
    int v = 0;
    while (*s >= '0' && *s <= '9') {
        int d = *s++ - '0';
        if (v > (INT_MAX - d) / 10) return neg ? INT_MIN : INT_MAX;   /* v*10+d would overflow */
        v = v * 10 + d;
    }
    return neg ? -v : v;
}
```

`my_atoi("  -42xyz")` returns -42, `"+7"` returns 7, `"2147483648"` returns 2147483647, `"-2147483649"` returns -2147483648 and `"abc"` returns 0. The test `v > (INT_MAX - d) / 10` is equivalent to `v * 10 + d > INT_MAX` but is computed without overflow.

`itoa` is not standard, and the task is to build it. Digits come out least-significant first, so they are collected and reversed. The sign needs care: `-n` overflows for `INT_MIN`, so the magnitude is computed in unsigned arithmetic, where negation is defined.

```c
char *my_itoa(int n, char *buf) {            /* buf must hold at least 12 bytes */
    char tmp[12]; int i = 0;
    unsigned u = n < 0 ? 0u - (unsigned)n : (unsigned)n;
    do { tmp[i++] = (char)('0' + u % 10); u /= 10; } while (u);   /* do-while: 0 gives "0" */
    char *o = buf;
    if (n < 0) *o++ = '-';
    while (i) *o++ = tmp[--i];
    *o = '\0';
    return buf;
}
```

For 0, -1234 and `INT_MIN` the results are `0`, `-1234` and `-2147483648`. The buffer size is 12 because `INT_MIN` has ten digits, a sign and the terminator. The conversion of an address to dotted-quad text and back is the same exercise with four numbers and is solved in the [Problem Set](#ps2){.ref}.

::: check
1. Why does `my_memmove(s+2, s, 4)` copy backwards? [^c2-22]
2. Why compute `0u - (unsigned)n` rather than `-n`? [^c2-23]
:::

[^c2-22]: The destination begins inside the source region, so a forward copy would overwrite source bytes before they are read.
[^c2-23]: `-INT_MIN` overflows a signed `int`, which is undefined; unsigned negation is defined and gives 2147483648.

## [2.14]{.sec}Parsing an IPv4 header from a byte buffer [Must · ■■□]{.tag} {#s2-14}

A packet arrives as an array of bytes. The task is to extract the fields safely: check the length before reading, read multi-byte fields in network order, and verify the checksum. The meaning of each field belongs to [Pillar 3](#ch3){.ref}; here we consider only offsets and C technique.

<figure>
<svg viewBox="0 0 480 190" width="480">
  <text class="sm" x="2" y="22">byte</text>
  <text class="sm" x="34" y="22">0</text><text class="sm" x="114" y="22">1</text><text class="sm" x="194" y="22">2</text><text class="sm" x="274" y="22">3</text>
  <g transform="translate(30,26)">
    <rect class="box" x="0" y="0" width="40" height="26"/><text class="lbl" x="20" y="16" text-anchor="middle">Ver</text>
    <rect class="box" x="40" y="0" width="40" height="26"/><text class="lbl" x="60" y="16" text-anchor="middle">IHL</text>
    <rect class="box" x="80" y="0" width="80" height="26"/><text class="lbl" x="120" y="16" text-anchor="middle">DSCP / ECN</text>
    <rect class="box" x="160" y="0" width="160" height="26"/><text class="lbl" x="240" y="16" text-anchor="middle">Total length (offset 2)</text>
    <rect class="box" x="0" y="26" width="160" height="26"/><text class="lbl" x="80" y="42" text-anchor="middle">Identification (4)</text>
    <rect class="box" x="160" y="26" width="160" height="26"/><text class="lbl" x="240" y="42" text-anchor="middle">Flags + fragment offset (6)</text>
    <rect class="box" x="0" y="52" width="80" height="26"/><text class="lbl" x="40" y="68" text-anchor="middle">TTL (8)</text>
    <rect class="box" x="80" y="52" width="80" height="26"/><text class="lbl" x="120" y="68" text-anchor="middle">Protocol (9)</text>
    <rect class="box" x="160" y="52" width="160" height="26"/><text class="lbl" x="240" y="68" text-anchor="middle">Header checksum (10)</text>
    <rect class="box" x="0" y="78" width="320" height="26"/><text class="lbl" x="160" y="94" text-anchor="middle">Source address (12)</text>
    <rect class="box" x="0" y="104" width="320" height="26"/><text class="lbl" x="160" y="120" text-anchor="middle">Destination address (16)</text>
    <rect class="fill dash" x="0" y="130" width="320" height="22"/><text class="sm" x="160" y="144" text-anchor="middle">options, present only when IHL &gt; 5 (up to offset 60)</text>
  </g>
  <line class="acc" x1="30" y1="170" x2="350" y2="170"/>
  <text class="sm" x="190" y="184" text-anchor="middle">each row is 32 bits = 4 bytes; fixed part 20 bytes</text>
</svg>
<figcaption><b>Figure 2.6</b> The IPv4 header as a C programmer reads it. Offsets in parentheses are in bytes; every multi-byte field is big-endian.</figcaption>
</figure>

Two designs exist. One may declare a packed structure and cast the buffer to it, which is short but wrong for the reasons of [2.7](#s2-7){.ref}: the buffer may be misaligned, bit-fields vary, and every field still needs `ntohs`. The robust design reads each field from its offset with small helpers that assemble bytes, and fills an ordinary structure. Version and header length share byte 0 and are split with a shift and a mask.

```c
struct ipv4 { uint8_t version, ihl; uint16_t total_len, id, frag;
              uint8_t ttl, proto; uint16_t csum; uint32_t src, dst; };

static inline uint16_t rd16(const uint8_t *p) { return (uint16_t)((p[0] << 8) | p[1]); }
static inline uint32_t rd32(const uint8_t *p) {
    return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) | ((uint32_t)p[2] << 8) | p[3];
}

uint16_t inet_csum(const uint8_t *p, size_t n) {     /* ones-complement sum, RFC 1071 */
    uint32_t sum = 0;
    for (; n > 1; p += 2, n -= 2) sum += rd16(p);
    if (n) sum += (uint32_t)p[0] << 8;               /* odd trailing byte, padded with 0 */
    while (sum >> 16) sum = (sum & 0xFFFF) + (sum >> 16);   /* fold carries back in */
    return (uint16_t)~sum;
}

int ipv4_parse(const uint8_t *buf, size_t len, struct ipv4 *h) {
    if (len < 20) return -1;                         /* too short to read the fixed part */
    h->version = buf[0] >> 4;  h->ihl = buf[0] & 0x0F;
    if (h->version != 4 || h->ihl < 5) return -2;    /* wrong version or impossible IHL */
    size_t hlen = (size_t)h->ihl * 4;                /* IHL counts 32-bit words */
    if (len < hlen) return -1;
    h->total_len = rd16(buf + 2);
    if (h->total_len < hlen || h->total_len > len) return -3;
    h->id = rd16(buf + 4);  h->frag = rd16(buf + 6);
    h->ttl = buf[8];  h->proto = buf[9];  h->csum = rd16(buf + 10);
    h->src = rd32(buf + 12);  h->dst = rd32(buf + 16);
    return inet_csum(buf, hlen) == 0 ? 0 : -4;       /* a valid header sums to zero */
}
```

The helper `u32_to_dotted` prints an address held in host order: `snprintf(out, 16, "%u.%u.%u.%u", ip >> 24, (ip >> 16) & 255, (ip >> 8) & 255, ip & 255)`. For the header bytes `45 00 00 73 00 00 40 00 40 11 b8 61 c0 a8 00 01 c0 a8 00 c7`, supplied in a buffer of at least 115 bytes, `ipv4_parse` returns 0 and the structure holds version 4, IHL 5 (20 bytes), total length 115, TTL 64, protocol 17 (UDP), source 192.168.0.1 and destination 192.168.0.199. With the checksum field zeroed, `inet_csum` returns `0xb861`, the stored value. Passing a length of 19 returns -1, and changing the TTL byte to `0x3f` without updating the checksum returns -4.

The order of the checks is the point of the exercise. Every read is guarded by a prior length test, and `total_len` is trusted only after it has been compared with the number of bytes actually received. A parser that reads `ihl` and then indexes options without checking is the template of a remote vulnerability. The more general loop for variable-length options, a type-length-value parser, appears in the [Problem Set](#ps2){.ref}.

::: lens
[CISCO · JUNIPER · ARISTA · BROADCOM]{.co}

"Parse this header from a hex dump" is reported as a networking-software exercise, and "Can you send a C struct directly over a socket?" as a conceptual follow-up. A strong answer reads fields by offset, validates lengths first, converts byte order, and explains why the packed-structure cast is fragile. Follow-ups: how to extend the parser to TCP or UDP (the next header starts at offset `ihl * 4`), and how to verify the checksum incrementally.
:::

::: check
1. A packet has `buf[0] = 0x47`. What are the version and the header length in bytes? [^c2-24]
2. Why must `len` be tested before `total_len` is trusted? [^c2-25]
:::

[^c2-24]: Version 4 (high nibble) and IHL 7, so the header is 28 bytes.
[^c2-25]: The field comes from the sender and may claim more bytes than were received; using it unchecked allows reads beyond the buffer.

:::
