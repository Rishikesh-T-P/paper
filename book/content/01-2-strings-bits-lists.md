::: {.p1}

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

A CIDR string `a.b.c.d/p` is handled by parsing the address up to the slash, then parsing *p* as a decimal number in 0–32 with the same no-leading-zero rule. Validation of IPv6 groups and the reporting problems built on these parsers are in the Problem Set ([Problem Set](#ps1){.ref}).

::: check
1. Why is `01.2.3.4` rejected even though `atoi("01")` is 1? [^c1-8]
2. What goes wrong with `char buf[15]` in `format_ipv4`? [^c1-9]
:::

[^c1-8]: Leading zeros are ambiguous (some parsers read them as octal), so strict validators reject them.
[^c1-9]: The longest address `255.255.255.255` has 15 characters, and the terminating zero needs a sixteenth byte.

## [1.5]{.sec}Bit manipulation and subnet code [Must · ■■□]{.tag} {#s1-5}

::: bigidea
An integer is a row of switches, and a mask with AND, OR, XOR and shifts reads or writes any group of them in one step, which is why addresses, flags and registers are all handled this way.
:::

The theory of subnetting, masks and CIDR is taught in the networking chapter (Pillar 3, §3.4); this section supplies only the bit code that implements it. The operators are `&` (AND), `|` (OR), `^` (XOR), `~` (NOT), `<<` and `>>`. We use unsigned types throughout, because left-shifting a negative signed value or shifting a `1` into the sign bit is undefined behaviour in C, and `>>` on a signed negative value is implementation-defined.

::: trap
*Claim:* `if (x & 1 == 0)` tests whether *x* is even. *Why it is wrong:* `==` binds tighter than `&`, so the expression means `x & (1 == 0)`, that is `x & 0`, which is always zero. *Correct statement:* write `(x & 1) == 0`, and parenthesise every bitwise sub-expression.
:::

| Task | Expression | Why it works |
|---|---|---|
| set bit *n* | `x \| (1u << n)` | OR with a one forces the bit to 1 |
| clear bit *n* | `x & ~(1u << n)` | AND with a zero forces the bit to 0 |
| toggle bit *n* | `x ^ (1u << n)` | XOR with a one flips the bit |
| test bit *n* | `(x >> n) & 1u` | brings the bit to position 0 |
| clear lowest set bit | `x & (x - 1)` | subtracting 1 flips the lowest 1 and the zeros below it |
| isolate lowest set bit | `x & -x` | two's complement negation keeps only that bit |
| power of two (x > 0) | `x && !(x & (x - 1))` | exactly one bit is set |
| count set bits | loop `x &= x - 1` | each pass removes one bit; runs popcount times |
| round up to multiple of *a* (power of two) | `(x + a - 1) & ~(a - 1)` | adds slack, then clears the low bits |

As macros for C, with arguments in parentheses and `1u` to avoid signed overflow, together with a population count and a byte swap (the conversion between big-endian and little-endian forms):

```c
#define SET_BIT(x, n)    ((x) |=  (1u << (n)))
#define CLEAR_BIT(x, n)  ((x) &= ~(1u << (n)))
#define TOGGLE_BIT(x, n) ((x) ^=  (1u << (n)))
#define TEST_BIT(x, n)   (((x) >> (n)) & 1u)

static unsigned popcount(uint32_t x) {
    unsigned c = 0;
    while (x) { x &= x - 1; c++; }
    return c;
}
static uint32_t swap32(uint32_t x) {
    return (x >> 24) | ((x >> 8) & 0x0000FF00u) |
           ((x << 8) & 0x00FF0000u) | (x << 24);
}
```

### Subnet arithmetic as bit operations

A prefix length *p* means that the top *p* bits are the network part. The mask has *p* ones followed by 32 − *p* zeros.

```c
static uint32_t mask_of(unsigned p) {            /* p in 0..32 */
    return p ? 0xFFFFFFFFu << (32 - p) : 0u;  /* shift by 32 would be UB */
}
bool same_subnet(uint32_t a, uint32_t b, unsigned p) {
    uint32_t m = mask_of(p);
    return (a & m) == (b & m);
}
void describe(uint32_t ip, unsigned p,
              uint32_t *net, uint32_t *bc, uint64_t *hosts) {
    uint32_t m = mask_of(p);  /* p <= 30 for a host range */
    *net = ip & m;
    *bc = *net | ~m;
    *hosts = (1ull << (32 - p)) - 2;  /* usable: net + 1 .. bc - 1 */
}
```

::: trap
*Claim:* `0xFFFFFFFFu << (32 - p)` is correct for every prefix length. *Why it is wrong:* for *p* = 0 the shift count is 32, which equals the width of the type, and the C standard leaves that undefined (x86 silently reduces the count modulo 32 and returns the unshifted value). *Correct statement:* special-case *p* = 0 as in `mask_of`.
:::

@<figure>
<svg viewBox="0 0 450 142" width="486">
<text class="sm" x="10" y="41" text-anchor="start">IP</text>
<rect class="lg" x="70" y="30" width="11" height="16"/>
<text class="mono" x="75.5" y="42" text-anchor="middle">0</text>
<rect class="lg" x="81" y="30" width="11" height="16"/>
<text class="mono" x="86.5" y="42" text-anchor="middle">0</text>
<rect class="lg" x="92" y="30" width="11" height="16"/>
<text class="mono" x="97.5" y="42" text-anchor="middle">0</text>
<rect class="lg" x="103" y="30" width="11" height="16"/>
<text class="mono" x="108.5" y="42" text-anchor="middle">0</text>
<rect class="lg" x="114" y="30" width="11" height="16"/>
<text class="mono" x="119.5" y="42" text-anchor="middle">1</text>
<rect class="lg" x="125" y="30" width="11" height="16"/>
<text class="mono" x="130.5" y="42" text-anchor="middle">0</text>
<rect class="lg" x="136" y="30" width="11" height="16"/>
<text class="mono" x="141.5" y="42" text-anchor="middle">1</text>
<rect class="lg" x="147" y="30" width="11" height="16"/>
<text class="mono" x="152.5" y="42" text-anchor="middle">0</text>
<rect class="lg" x="164" y="30" width="11" height="16"/>
<text class="mono" x="169.5" y="42" text-anchor="middle">0</text>
<rect class="lg" x="175" y="30" width="11" height="16"/>
<text class="mono" x="180.5" y="42" text-anchor="middle">0</text>
<rect class="lg" x="186" y="30" width="11" height="16"/>
<text class="mono" x="191.5" y="42" text-anchor="middle">0</text>
<rect class="lg" x="197" y="30" width="11" height="16"/>
<text class="mono" x="202.5" y="42" text-anchor="middle">1</text>
<rect class="lg" x="208" y="30" width="11" height="16"/>
<text class="mono" x="213.5" y="42" text-anchor="middle">0</text>
<rect class="lg" x="219" y="30" width="11" height="16"/>
<text class="mono" x="224.5" y="42" text-anchor="middle">1</text>
<rect class="lg" x="230" y="30" width="11" height="16"/>
<text class="mono" x="235.5" y="42" text-anchor="middle">0</text>
<rect class="lg" x="241" y="30" width="11" height="16"/>
<text class="mono" x="246.5" y="42" text-anchor="middle">0</text>
<rect class="lg" x="258" y="30" width="11" height="16"/>
<text class="mono" x="263.5" y="42" text-anchor="middle">0</text>
<rect class="lg" x="269" y="30" width="11" height="16"/>
<text class="mono" x="274.5" y="42" text-anchor="middle">0</text>
<rect class="lg" x="280" y="30" width="11" height="16"/>
<text class="mono" x="285.5" y="42" text-anchor="middle">0</text>
<rect class="lg" x="291" y="30" width="11" height="16"/>
<text class="mono" x="296.5" y="42" text-anchor="middle">1</text>
<rect class="lg" x="302" y="30" width="11" height="16"/>
<text class="mono" x="307.5" y="42" text-anchor="middle">1</text>
<rect class="lg" x="313" y="30" width="11" height="16"/>
<text class="mono" x="318.5" y="42" text-anchor="middle">1</text>
<rect class="hl" x="324" y="30" width="11" height="16"/>
<rect class="lg" x="324" y="30" width="11" height="16"/>
<text class="mono" x="329.5" y="42" text-anchor="middle">1</text>
<rect class="hl" x="335" y="30" width="11" height="16"/>
<rect class="lg" x="335" y="30" width="11" height="16"/>
<text class="mono" x="340.5" y="42" text-anchor="middle">0</text>
<rect class="hl" x="352" y="30" width="11" height="16"/>
<rect class="lg" x="352" y="30" width="11" height="16"/>
<text class="mono" x="357.5" y="42" text-anchor="middle">0</text>
<rect class="hl" x="363" y="30" width="11" height="16"/>
<rect class="lg" x="363" y="30" width="11" height="16"/>
<text class="mono" x="368.5" y="42" text-anchor="middle">0</text>
<rect class="hl" x="374" y="30" width="11" height="16"/>
<rect class="lg" x="374" y="30" width="11" height="16"/>
<text class="mono" x="379.5" y="42" text-anchor="middle">1</text>
<rect class="hl" x="385" y="30" width="11" height="16"/>
<rect class="lg" x="385" y="30" width="11" height="16"/>
<text class="mono" x="390.5" y="42" text-anchor="middle">0</text>
<rect class="hl" x="396" y="30" width="11" height="16"/>
<rect class="lg" x="396" y="30" width="11" height="16"/>
<text class="mono" x="401.5" y="42" text-anchor="middle">1</text>
<rect class="hl" x="407" y="30" width="11" height="16"/>
<rect class="lg" x="407" y="30" width="11" height="16"/>
<text class="mono" x="412.5" y="42" text-anchor="middle">0</text>
<rect class="hl" x="418" y="30" width="11" height="16"/>
<rect class="lg" x="418" y="30" width="11" height="16"/>
<text class="mono" x="423.5" y="42" text-anchor="middle">0</text>
<rect class="hl" x="429" y="30" width="11" height="16"/>
<rect class="lg" x="429" y="30" width="11" height="16"/>
<text class="mono" x="434.5" y="42" text-anchor="middle">0</text><text class="sm" x="10" y="71" text-anchor="start">mask /22</text>
<rect class="lg" x="70" y="60" width="11" height="16"/>
<text class="mono" x="75.5" y="72" text-anchor="middle">1</text>
<rect class="lg" x="81" y="60" width="11" height="16"/>
<text class="mono" x="86.5" y="72" text-anchor="middle">1</text>
<rect class="lg" x="92" y="60" width="11" height="16"/>
<text class="mono" x="97.5" y="72" text-anchor="middle">1</text>
<rect class="lg" x="103" y="60" width="11" height="16"/>
<text class="mono" x="108.5" y="72" text-anchor="middle">1</text>
<rect class="lg" x="114" y="60" width="11" height="16"/>
<text class="mono" x="119.5" y="72" text-anchor="middle">1</text>
<rect class="lg" x="125" y="60" width="11" height="16"/>
<text class="mono" x="130.5" y="72" text-anchor="middle">1</text>
<rect class="lg" x="136" y="60" width="11" height="16"/>
<text class="mono" x="141.5" y="72" text-anchor="middle">1</text>
<rect class="lg" x="147" y="60" width="11" height="16"/>
<text class="mono" x="152.5" y="72" text-anchor="middle">1</text>
<rect class="lg" x="164" y="60" width="11" height="16"/>
<text class="mono" x="169.5" y="72" text-anchor="middle">1</text>
<rect class="lg" x="175" y="60" width="11" height="16"/>
<text class="mono" x="180.5" y="72" text-anchor="middle">1</text>
<rect class="lg" x="186" y="60" width="11" height="16"/>
<text class="mono" x="191.5" y="72" text-anchor="middle">1</text>
<rect class="lg" x="197" y="60" width="11" height="16"/>
<text class="mono" x="202.5" y="72" text-anchor="middle">1</text>
<rect class="lg" x="208" y="60" width="11" height="16"/>
<text class="mono" x="213.5" y="72" text-anchor="middle">1</text>
<rect class="lg" x="219" y="60" width="11" height="16"/>
<text class="mono" x="224.5" y="72" text-anchor="middle">1</text>
<rect class="lg" x="230" y="60" width="11" height="16"/>
<text class="mono" x="235.5" y="72" text-anchor="middle">1</text>
<rect class="lg" x="241" y="60" width="11" height="16"/>
<text class="mono" x="246.5" y="72" text-anchor="middle">1</text>
<rect class="lg" x="258" y="60" width="11" height="16"/>
<text class="mono" x="263.5" y="72" text-anchor="middle">1</text>
<rect class="lg" x="269" y="60" width="11" height="16"/>
<text class="mono" x="274.5" y="72" text-anchor="middle">1</text>
<rect class="lg" x="280" y="60" width="11" height="16"/>
<text class="mono" x="285.5" y="72" text-anchor="middle">1</text>
<rect class="lg" x="291" y="60" width="11" height="16"/>
<text class="mono" x="296.5" y="72" text-anchor="middle">1</text>
<rect class="lg" x="302" y="60" width="11" height="16"/>
<text class="mono" x="307.5" y="72" text-anchor="middle">1</text>
<rect class="lg" x="313" y="60" width="11" height="16"/>
<text class="mono" x="318.5" y="72" text-anchor="middle">1</text>
<rect class="hl" x="324" y="60" width="11" height="16"/>
<rect class="lg" x="324" y="60" width="11" height="16"/>
<text class="mono" x="329.5" y="72" text-anchor="middle">0</text>
<rect class="hl" x="335" y="60" width="11" height="16"/>
<rect class="lg" x="335" y="60" width="11" height="16"/>
<text class="mono" x="340.5" y="72" text-anchor="middle">0</text>
<rect class="hl" x="352" y="60" width="11" height="16"/>
<rect class="lg" x="352" y="60" width="11" height="16"/>
<text class="mono" x="357.5" y="72" text-anchor="middle">0</text>
<rect class="hl" x="363" y="60" width="11" height="16"/>
<rect class="lg" x="363" y="60" width="11" height="16"/>
<text class="mono" x="368.5" y="72" text-anchor="middle">0</text>
<rect class="hl" x="374" y="60" width="11" height="16"/>
<rect class="lg" x="374" y="60" width="11" height="16"/>
<text class="mono" x="379.5" y="72" text-anchor="middle">0</text>
<rect class="hl" x="385" y="60" width="11" height="16"/>
<rect class="lg" x="385" y="60" width="11" height="16"/>
<text class="mono" x="390.5" y="72" text-anchor="middle">0</text>
<rect class="hl" x="396" y="60" width="11" height="16"/>
<rect class="lg" x="396" y="60" width="11" height="16"/>
<text class="mono" x="401.5" y="72" text-anchor="middle">0</text>
<rect class="hl" x="407" y="60" width="11" height="16"/>
<rect class="lg" x="407" y="60" width="11" height="16"/>
<text class="mono" x="412.5" y="72" text-anchor="middle">0</text>
<rect class="hl" x="418" y="60" width="11" height="16"/>
<rect class="lg" x="418" y="60" width="11" height="16"/>
<text class="mono" x="423.5" y="72" text-anchor="middle">0</text>
<rect class="hl" x="429" y="60" width="11" height="16"/>
<rect class="lg" x="429" y="60" width="11" height="16"/>
<text class="mono" x="434.5" y="72" text-anchor="middle">0</text><text class="sm" x="10" y="107" text-anchor="start">IP AND mask</text>
<rect class="lg" x="70" y="96" width="11" height="16"/>
<text class="mono" x="75.5" y="108" text-anchor="middle">0</text>
<rect class="lg" x="81" y="96" width="11" height="16"/>
<text class="mono" x="86.5" y="108" text-anchor="middle">0</text>
<rect class="lg" x="92" y="96" width="11" height="16"/>
<text class="mono" x="97.5" y="108" text-anchor="middle">0</text>
<rect class="lg" x="103" y="96" width="11" height="16"/>
<text class="mono" x="108.5" y="108" text-anchor="middle">0</text>
<rect class="lg" x="114" y="96" width="11" height="16"/>
<text class="mono" x="119.5" y="108" text-anchor="middle">1</text>
<rect class="lg" x="125" y="96" width="11" height="16"/>
<text class="mono" x="130.5" y="108" text-anchor="middle">0</text>
<rect class="lg" x="136" y="96" width="11" height="16"/>
<text class="mono" x="141.5" y="108" text-anchor="middle">1</text>
<rect class="lg" x="147" y="96" width="11" height="16"/>
<text class="mono" x="152.5" y="108" text-anchor="middle">0</text>
<rect class="lg" x="164" y="96" width="11" height="16"/>
<text class="mono" x="169.5" y="108" text-anchor="middle">0</text>
<rect class="lg" x="175" y="96" width="11" height="16"/>
<text class="mono" x="180.5" y="108" text-anchor="middle">0</text>
<rect class="lg" x="186" y="96" width="11" height="16"/>
<text class="mono" x="191.5" y="108" text-anchor="middle">0</text>
<rect class="lg" x="197" y="96" width="11" height="16"/>
<text class="mono" x="202.5" y="108" text-anchor="middle">1</text>
<rect class="lg" x="208" y="96" width="11" height="16"/>
<text class="mono" x="213.5" y="108" text-anchor="middle">0</text>
<rect class="lg" x="219" y="96" width="11" height="16"/>
<text class="mono" x="224.5" y="108" text-anchor="middle">1</text>
<rect class="lg" x="230" y="96" width="11" height="16"/>
<text class="mono" x="235.5" y="108" text-anchor="middle">0</text>
<rect class="lg" x="241" y="96" width="11" height="16"/>
<text class="mono" x="246.5" y="108" text-anchor="middle">0</text>
<rect class="lg" x="258" y="96" width="11" height="16"/>
<text class="mono" x="263.5" y="108" text-anchor="middle">0</text>
<rect class="lg" x="269" y="96" width="11" height="16"/>
<text class="mono" x="274.5" y="108" text-anchor="middle">0</text>
<rect class="lg" x="280" y="96" width="11" height="16"/>
<text class="mono" x="285.5" y="108" text-anchor="middle">0</text>
<rect class="lg" x="291" y="96" width="11" height="16"/>
<text class="mono" x="296.5" y="108" text-anchor="middle">1</text>
<rect class="lg" x="302" y="96" width="11" height="16"/>
<text class="mono" x="307.5" y="108" text-anchor="middle">1</text>
<rect class="lg" x="313" y="96" width="11" height="16"/>
<text class="mono" x="318.5" y="108" text-anchor="middle">1</text>
<rect class="hl" x="324" y="96" width="11" height="16"/>
<rect class="lg" x="324" y="96" width="11" height="16"/>
<text class="mono" x="329.5" y="108" text-anchor="middle">0</text>
<rect class="hl" x="335" y="96" width="11" height="16"/>
<rect class="lg" x="335" y="96" width="11" height="16"/>
<text class="mono" x="340.5" y="108" text-anchor="middle">0</text>
<rect class="hl" x="352" y="96" width="11" height="16"/>
<rect class="lg" x="352" y="96" width="11" height="16"/>
<text class="mono" x="357.5" y="108" text-anchor="middle">0</text>
<rect class="hl" x="363" y="96" width="11" height="16"/>
<rect class="lg" x="363" y="96" width="11" height="16"/>
<text class="mono" x="368.5" y="108" text-anchor="middle">0</text>
<rect class="hl" x="374" y="96" width="11" height="16"/>
<rect class="lg" x="374" y="96" width="11" height="16"/>
<text class="mono" x="379.5" y="108" text-anchor="middle">0</text>
<rect class="hl" x="385" y="96" width="11" height="16"/>
<rect class="lg" x="385" y="96" width="11" height="16"/>
<text class="mono" x="390.5" y="108" text-anchor="middle">0</text>
<rect class="hl" x="396" y="96" width="11" height="16"/>
<rect class="lg" x="396" y="96" width="11" height="16"/>
<text class="mono" x="401.5" y="108" text-anchor="middle">0</text>
<rect class="hl" x="407" y="96" width="11" height="16"/>
<rect class="lg" x="407" y="96" width="11" height="16"/>
<text class="mono" x="412.5" y="108" text-anchor="middle">0</text>
<rect class="hl" x="418" y="96" width="11" height="16"/>
<rect class="lg" x="418" y="96" width="11" height="16"/>
<text class="mono" x="423.5" y="108" text-anchor="middle">0</text>
<rect class="hl" x="429" y="96" width="11" height="16"/>
<rect class="lg" x="429" y="96" width="11" height="16"/>
<text class="mono" x="434.5" y="108" text-anchor="middle">0</text><text class="sm" x="70" y="18" text-anchor="start">10</text><text class="sm" x="164" y="18" text-anchor="start">20</text><text class="sm" x="258" y="18" text-anchor="start">30</text><text class="sm" x="352" y="18" text-anchor="start">40</text><line class="ln" x1="70" y1="86" x2="440" y2="86"/><text class="sm" x="70" y="130" text-anchor="start">network 10.20.28.0; broadcast = network OR NOT mask = 10.20.31.255; shaded = host bits</text>
</svg>
<figcaption><b>Figure 1.3</b> The same-subnet test in bits. AND with the mask keeps the 22 network bits and clears the 10 host bits.</figcaption>
</figure>

::: example
**Describe 10.20.30.40/22 with bit operations only.**

1. The mask has 22 ones: `0xFFFFFC00`, which is 255.255.252.0.
2. The network address is `ip & mask`. The third octet 30 = `00011110` keeps its top six bits, giving `00011100` = 28, and the fourth octet is cleared. Network: 10.20.28.0.
3. The broadcast address is `net | ~mask`, which sets the ten host bits: third octet 28 + 3 = 31, fourth octet 255. Broadcast: 10.20.31.255.
4. Usable hosts run from 10.20.28.1 to 10.20.31.254, which is 2^10 − 2 = 1022 addresses.
5. Test 10.20.29.7 against it: its third octet 29 = `00011101` also clears to 28, so it lies in the subnet.

[Result: network 10.20.28.0, broadcast 10.20.31.255, 1022 hosts.]{.result}
:::

*Complexity.* Every operation here is O(1); `popcount` by clearing the lowest bit is O(*number of set bits*). GCC and Clang offer `__builtin_popcount` and `__builtin_clz`, but interviewers usually want the loop.

::: lens
[QUALCOMM · BROADCOM · JUNIPER · CISCO]{.co}

Bit questions are asked in C and are examined for care with types: unsigned operands, `1u`, parentheses and the shift-by-width case. A strong answer states the idiom, explains why it works in one sentence, and mentions the undefined-behaviour pitfall unprompted. Typical follow-up: "do it without a loop" or "do it for a 64-bit value".
:::

::: check
1. What does `x & (x - 1)` return for *x* = 40 (101000)? [^c1-10]
2. How many usable hosts has a /27? [^c1-11]
:::

[^c1-10]: 32 (100000): the lowest set bit is cleared.
[^c1-11]: 2^5 − 2 = 30.

## [1.6]{.sec}Linked lists in C [Must · ■■□]{.tag} {#s1-6}

::: bigidea
A linked list is a chain of nodes joined by pointers, and every list problem is a question about which pointer to rewrite, and in which order, so that no node is lost.
:::

A singly linked list node holds a value and the address of the next node; the last node holds `NULL`. Access by position costs O(*n*), but inserting or deleting after a known node costs O(1) because only pointers change. Routers keep many such lists (the chains of a hash table, a queue of packet buffers), and interviews at Arista, Juniper, Nokia and Broadcom ask for them in C from a blank page.

```c
typedef struct Node { int val; struct Node *next; } Node;

Node *push_front(Node *head, int v) {
    Node *n = malloc(sizeof *n);
    if (!n) return head;  /* allocation failed: list unchanged */
    n->val = v; n->next = head;
    return n;                          /* the new head */
}
```

### The pointer-to-pointer idiom

To delete a node we must re-point the link that leads to it. For a middle node that link is the previous node's `next`; for the first node it is the `head` variable itself, which is why a naive version needs a special case for the head. If we hold a pointer to the link (a `Node **`), both cases are the same.

@<figure>
<svg viewBox="0 0 420 130" width="454"><defs><marker id="a4" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#1A1D23"/></marker><marker id="a4b" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#3D55A8"/></marker></defs>
<rect class="box" x="10" y="20" width="40" height="24"/><text class="mono" x="30" y="35" text-anchor="middle">head</text><rect class="box" x="100" y="20" width="60" height="24"/><line class="ln" x1="133.0" y1="20" x2="133.0" y2="44"/><text class="mono" x="116.5" y="35.0" text-anchor="middle">A</text><rect class="box" x="210" y="20" width="60" height="24"/><line class="ln" x1="243.0" y1="20" x2="243.0" y2="44"/><text class="mono" x="226.5" y="35.0" text-anchor="middle">B</text><rect class="box" x="320" y="20" width="60" height="24"/><line class="ln" x1="353.0" y1="20" x2="353.0" y2="44"/><text class="mono" x="336.5" y="35.0" text-anchor="middle">C</text><line class="ln" x1="50" y1="32" x2="100" y2="32" marker-end="url(#a4)"/><line class="ln" x1="133" y1="32" x2="210" y2="32" marker-end="url(#a4)"/><line class="ln" x1="243" y1="32" x2="320" y2="32" marker-end="url(#a4)"/><text class="sm" x="395" y="35" text-anchor="middle">NULL</text><line class="ln" x1="353" y1="32" x2="375" y2="32" marker-end="url(#a4)"/><path class="acc" d="M133,44 Q200,78 320,44" marker-end="url(#a4b)"/><text class="sm" x="240" y="84" text-anchor="middle">&#42;pp = (&#42;pp)->next  bypasses B</text><rect class="box" x="115" y="95" width="36" height="22"/><text class="mono" x="133" y="110" text-anchor="middle">pp</text><line class="ln" x1="133" y1="95" x2="133" y2="46" marker-end="url(#a4)"/>
</svg>
<figcaption><b>Figure 1.4</b> The pointer-to-pointer idiom. pp holds the address of the link that points at the current node (head, or the next field of the predecessor), so the head needs no special case.</figcaption>
</figure>

```c
Node *delete_value(Node *head, int key) {          /* first match only */
    Node **pp = &head;
    while (*pp && (*pp)->val != key) pp = &(*pp)->next;
    if (*pp) { Node *dead = *pp; *pp = dead->next; free(dead); }
    return head;
}
Node *delete_all(Node *head, int key) {            /* every match */
    Node **pp = &head;
    while (*pp) {
        if ((*pp)->val == key) {
            Node *dead = *pp; *pp = dead->next; free(dead);
        } else pp = &(*pp)->next;  /* advance only if nothing was removed */
    }
    return head;
}
```

For `3 → 5 → 3 → 7` and key 3, `delete_all` removes the head (the link `head` now points at the 5), skips the 5, removes the second 3 (the link `5.next` now points at the 7), and returns `5 → 7`. The alternative to `Node **` is a dummy node placed before the head; both remove the special case.

::: trap
*Claim:* after `free(dead)` the loop may continue with `dead->next`. *Why it is wrong:* the memory has been returned and reading it is undefined behaviour. *Correct statement:* read `dead->next` into a local (or into `*pp`) before calling `free`.
:::

### Reversal

Three pointers walk the list: `prev` (the already reversed part), `head` (the current node) and `next`, saved before the current `next` field is overwritten. The classic bug is to overwrite first and so lose the rest of the list.

@<figure>
<svg viewBox="0 0 400 170" width="432"><defs><marker id="a3" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#1A1D23"/></marker><marker id="a3b" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#3D55A8"/></marker></defs>
<text class="sm" x="10" y="24" text-anchor="start">before:  prev = NULL, curr = 1</text><rect class="box" x="80" y="30" width="60" height="24"/><line class="ln" x1="113.0" y1="30" x2="113.0" y2="54"/><text class="mono" x="96.5" y="45.0" text-anchor="middle">1</text><rect class="box" x="190" y="30" width="60" height="24"/><line class="ln" x1="223.0" y1="30" x2="223.0" y2="54"/><text class="mono" x="206.5" y="45.0" text-anchor="middle">2</text><rect class="box" x="300" y="30" width="60" height="24"/><line class="ln" x1="333.0" y1="30" x2="333.0" y2="54"/><text class="mono" x="316.5" y="45.0" text-anchor="middle">3</text><text class="sm" x="30" y="45" text-anchor="middle">NULL</text><line class="ln" x1="113" y1="42" x2="190" y2="42" marker-end="url(#a3)"/><line class="ln" x1="223" y1="42" x2="300" y2="42" marker-end="url(#a3)"/><text class="sm" x="375" y="45" text-anchor="middle">NULL</text><line class="ln" x1="333" y1="42" x2="355" y2="42" marker-end="url(#a3)"/><path class="accf" d="M96,56 l-4,7 l8,0 z"/><text class="lbl" x="96" y="73" text-anchor="middle">curr</text><path class="accf" d="M20,56 l-4,7 l8,0 z"/><text class="lbl" x="20" y="73" text-anchor="middle">prev</text><text class="sm" x="10" y="104" text-anchor="start">after one iteration:  curr = 2, prev = 1</text><rect class="box" x="80" y="110" width="60" height="24"/><line class="ln" x1="113.0" y1="110" x2="113.0" y2="134"/><text class="mono" x="96.5" y="125.0" text-anchor="middle">1</text><rect class="box" x="190" y="110" width="60" height="24"/><line class="ln" x1="223.0" y1="110" x2="223.0" y2="134"/><text class="mono" x="206.5" y="125.0" text-anchor="middle">2</text><rect class="box" x="300" y="110" width="60" height="24"/><line class="ln" x1="333.0" y1="110" x2="333.0" y2="134"/><text class="mono" x="316.5" y="125.0" text-anchor="middle">3</text><text class="sm" x="30" y="125" text-anchor="middle">NULL</text><path class="acc" d="M120,134 Q70,154 40,130" marker-end="url(#a3b)"/><line class="ln" x1="223" y1="122" x2="300" y2="122" marker-end="url(#a3)"/><text class="sm" x="375" y="125" text-anchor="middle">NULL</text><line class="ln" x1="333" y1="122" x2="355" y2="122" marker-end="url(#a3)"/><path class="accf" d="M96,136 l-4,7 l8,0 z"/><text class="lbl" x="96" y="153" text-anchor="middle">prev</text><path class="accf" d="M206,136 l-4,7 l8,0 z"/><text class="lbl" x="206" y="153" text-anchor="middle">curr</text>
</svg>
<figcaption><b>Figure 1.5</b> One step of in-place reversal. The accent arrow is the single pointer rewritten; next was saved first so that the rest of the list is not lost.</figcaption>
</figure>

```c
Node *reverse(Node *head) {
    Node *prev = NULL;
    while (head) {
        Node *next = head->next;       /* save */
        head->next = prev;             /* rewire */
        prev = head;                   /* advance both */
        head = next;
    }
    return prev;
}
```

| Step | head (current) | next saved | After rewire | prev |
|---|---|---|---|---|
| 1 | 1 | 2 | 1 → NULL | 1 |
| 2 | 2 | 3 | 2 → 1 | 2 |
| 3 | 3 | NULL | 3 → 2 | 3 |

The loop ends with `head == NULL` and `prev` pointing at the old tail, which is the new head. Time O(*n*), space O(1).

### Fast and slow pointers

Two pointers moving at speeds one and two give the middle node and detect cycles. For the middle, when `fast` reaches the end `slow` is halfway. For a cycle, `fast` closes on `slow` by one node per step, so inside a cycle they must meet.

```c
Node *middle(Node *head) {  /* second middle when the length is even */
    Node *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next; fast = fast->next->next;
    }
    return slow;
}
Node *cycle_start(Node *head) {            /* NULL if there is no cycle */
    Node *slow = head, *fast = head;
    while (fast && fast->next) {  /* test fast before fast->next */
        slow = slow->next; fast = fast->next->next;
        if (slow == fast) {
            for (slow = head; slow != fast; ) {
                slow = slow->next; fast = fast->next;
            }
            return slow;
        }
    }
    return NULL;
}
```

Why the second phase finds the start. Let *a* be the number of nodes from the head to the cycle start, *b* the distance from the start to the meeting point along the cycle, and *c* the remainder of the cycle, so the cycle length is *L* = *b* + *c*. When they meet, `slow` has taken *a* + *b* steps and `fast` twice as many, and the difference is a whole number *k* of laps: 2(*a* + *b*) − (*a* + *b*) = *kL*. Hence *a* = *kL* − *b* = (*k* − 1)*L* + *c*. A pointer from the head and one from the meeting point, both moving one step at a time, therefore reach the cycle start together, because the second one needs *c* steps to reach it and then some whole laps.

::: trap
*Claim:* `while (fast->next && fast)` is an equivalent loop condition. *Why it is wrong:* the first operand dereferences `fast` before it is known to be non-null, so an empty list crashes. *Correct statement:* test `fast` first, then `fast->next`, and only then use `fast->next->next`.
:::

### Merging with a dummy head

A temporary node on the stack gives the output list a fixed first node, so that the first append needs no special case.

```c
Node *merge(Node *a, Node *b) {            /* both sorted ascending */
    Node dummy = { 0, NULL }, *tail = &dummy;
    while (a && b) {
        if (a->val <= b->val) { tail->next = a; a = a->next; }
        else                  { tail->next = b; b = b->next; }
        tail = tail->next;
    }
    tail->next = a ? a : b;  /* append the non-empty remainder */
    return dummy.next;  /* the pointer, not the stack object */
}
```

Returning `dummy.next` is legal: it points to nodes that were allocated elsewhere, and only the local `dummy` itself vanishes on return. Returning `&dummy`, or a pointer to any local array, would be the classic dangling-pointer bug.

### Doubly linked lists

A doubly linked list adds a `prev` field, which makes deleting a *given* node O(1) with no search for its predecessor. Using a circular list with a sentinel node removes every `NULL` check:

```c
typedef struct DNode { int val; struct DNode *prev, *next; } DNode;

void dl_init(DNode *s) { s->prev = s->next = s; }  /* empty list */
void dl_insert_after(DNode *p, DNode *n) {
    n->prev = p; n->next = p->next;
    p->next->prev = n; p->next = n;
}
void dl_unlink(DNode *n) {
    n->prev->next = n->next; n->next->prev = n->prev;
}
```

The order of the four writes in `dl_insert_after` matters: `n` is wired to its neighbours first, and the neighbours are changed last. This structure is the core of the LRU cache in [§1.15](#s1-15){.ref} and of the intrusive lists inside operating-system kernels.

::: lens
[ARISTA · JUNIPER · NOKIA · BROADCOM]{.co}

The question is usually phrased as "write it in C on the shared editor": delete a node (head included), delete all nodes with a value, reverse, merge, find the loop. A strong answer draws the boxes first, names the three pointers, and checks the empty list, the one-node list and the head. Typical follow-ups are "what if the node is the tail" and "reverse it recursively".
:::

::: check
1. In `delete_value`, what does `pp` point to when the list is empty? [^c1-12]
2. Why does `reverse` need the variable `next`? [^c1-13]
:::

[^c1-12]: To `head` itself, which is `NULL`, so the loop does not run and nothing is freed.
[^c1-13]: Without it, writing `head->next = prev` destroys the only reference to the rest of the list.

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

### The ring buffer

Packet drivers hand frames from an interrupt handler to a consumer through a fixed array used circularly. The producer writes at `tail` and the consumer reads at `head`; both wrap with a modulus. The difficulty is that `head == tail` describes both an empty and a full buffer. Three remedies exist: keep a `count`, waste one slot, or let the indices run freely and compare their difference.

@<figure>
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
<figcaption><b>Figure 1.6</b> A circular buffer of capacity eight, before and after the write index wraps. A separate count removes the full-versus-empty ambiguity.</figcaption>
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
1. In the lock-free ring, why does `tail - head == N` identify a full buffer after both counters have wrapped past 2^32? [^c1-14]
2. What is the time complexity of `dailyTemps`, given the inner `while`? [^c1-15]
:::

[^c1-14]: Unsigned subtraction is modulo 2^32, so the difference is the true occupancy as long as it never exceeds *N*.
[^c1-15]: O(*n*): each index is pushed once and popped at most once.

:::
