::: {.p2}

## [2.5]{.sec}Declarations, const and function pointers [Must · ■■□]{.tag} {#s2-5}

C declarations are read from the identifier outwards: start at the name, look right, then left, and respect the parentheses. In `int *const p` the name `p` is a constant, and it is a pointer to `int`. The qualifier `const` applies to the thing immediately on its left, or to the type on its right when nothing stands on its left. Three forms cover every interview question.

| Declaration | Reads as | May change `*p`? | May change `p`? |
|---|---|---|---|
| `const int *p` (same as `int const *p`) | `p` is a pointer to a constant `int` | no | yes |
| `int *const p` | `p` is a constant pointer to `int` | yes | no |
| `const int *const p` | constant pointer to a constant `int` | no | no |

::: trap
*Claim:* `const char *s` means the string cannot change, so the pointer cannot move either. *Why it is wrong:* here `const` binds to `char`, the pointee; the pointer is free to move, as in `s++`. *Correct statement:* to forbid moving the pointer one writes `char *const s`, and to forbid both, `const char *const s`. Functions that only read a buffer should take `const T *`, which documents intent and lets the compiler reject accidental writes.
:::

A *function pointer* holds the address of code. Its declaration mirrors a function prototype with the name wrapped as `(*name)`: `int (*fp)(int, int);` declares `fp` as a pointer to a function taking two `int` and returning `int`. The parentheses matter, because `int *fp(int, int)` declares a function returning `int *`. A `typedef` makes such types readable, and calling through the pointer needs no dereference: `fp(2, 3)` and `(*fp)(2, 3)` are the same.

Function pointers appear in two interview patterns. The first is the *callback*: the library calls code the caller supplies, as `qsort` does with its comparator. The second is the *dispatch table*: an array of function pointers indexed by a small integer, replacing a long `switch`. Network code uses it to route a packet to a handler by IP protocol number.

```c
typedef int (*handler_fn)(const uint8_t *pkt, size_t len);

static int on_icmp(const uint8_t *p, size_t n) { (void)p; printf("icmp %zu\n", n); return 0; }
static int on_tcp (const uint8_t *p, size_t n) { (void)p; printf("tcp %zu\n",  n); return 0; }
static int on_udp (const uint8_t *p, size_t n) { (void)p; printf("udp %zu\n",  n); return 0; }

static handler_fn table[256] = { [1] = on_icmp, [6] = on_tcp, [17] = on_udp };

int dispatch(uint8_t proto, const uint8_t *pkt, size_t len) {
    handler_fn fn = table[proto];        /* unset entries are NULL        */
    if (!fn) { printf("proto %u: no handler\n", proto); return -1; }
    return fn(pkt, len);
}
```

Calling `dispatch(6, buf, 40)`, `dispatch(17, buf, 8)` and `dispatch(47, buf, 0)` prints `tcp 40`, `udp 8` and `proto 47: no handler`. The designated initialisers `[1] = on_icmp` set only the named slots, and a static array zeroes the rest, so the `NULL` test is reliable. The lookup costs one indexed load and one indirect call, independent of the number of protocols.

The comparator of `qsort` receives `const void *` and must cast back. The safe return expression is `(x < y) - (x > y)`, because the shortcut `x - y` overflows for extreme values, which is undefined behaviour ([2.12](#s2-12){.ref}).

```c
int cmp_desc(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (x < y) - (x > y);               /* descending order */
}
/* int v[] = {3, 9, 1, 7};  qsort(v, 4, sizeof v[0], cmp_desc);  ->  9 7 3 1 */
```

Sorting a routing table needs two keys, longest prefix first and then address ascending. The comparator tests the length first and falls through to the address only on a tie: `if (x->len != y->len) return (int)y->len - (int)x->len;`. With prefixes `10.0.0.0/8`, `192.168.1.0/24`, `10.1.0.0/16` and `192.168.0.0/24` the sorted order is `192.168.0.0/24`, `192.168.1.0/24`, `10.1.0.0/16`, `10.0.0.0/8`.

::: lens
[CISCO · JUNIPER]{.co}

"What are function pointers? Show how you would dispatch packets by protocol number." is reported as an interview topic at both companies. A strong answer shows the `typedef`, the table with designated initialisers, the `NULL` check, and says why a table beats a `switch` when handlers are registered at run time. Follow-up: how would a module register its own handler (a `register_handler(proto, fn)` function that writes the slot).
:::

::: check
1. What does `const char *const s` forbid? [^c2-8]
2. Why is `int *fp(int, int)` not a function pointer? [^c2-9]
:::

[^c2-8]: Both modifying the characters through `s` and reassigning `s` itself.
[^c2-9]: Without parentheses around `*fp` the declarator binds as a function returning `int *`; a pointer needs `int (*fp)(int, int)`.

## [2.6]{.sec}Storage classes and qualifiers [Must · ■■□]{.tag} {#s2-6}

The *storage class* of an object fixes its lifetime and linkage, and a *qualifier* restricts how the compiler may treat accesses. Both are interview staples, and the word `static` alone has three meanings.

**`static`.** (i) On a local variable it gives the variable static storage duration: one instance, created before `main`, zero-initialised, keeping its value between calls. (ii) On a global variable or function it gives *internal linkage*: the name is visible only inside that translation unit (one `.c` file after preprocessing), so two files may each define `static int count;` without a clash. (iii) A `static` array inside a function therefore moves from the stack to .data or .bss, as noted in [2.1](#s2-1){.ref}.

**`extern`.** It declares an object defined elsewhere and allocates nothing. A header should declare (`extern int g;`) and exactly one `.c` file should define (`int g = 0;`). Defining a variable in a header gives each including file its own copy, or a linker error for duplicates; marking it `static` in the header silently gives every file a private copy, which is almost never intended.

**`auto` and `register`.** `auto` is the default for locals and is never written. `register` is a historical hint that forbids taking the object's address; compilers now ignore it for optimisation.

**`const`.** It makes writes through that name an error. A global `const` usually lives in .rodata, so casting `const` away and writing to it is undefined behaviour. A `const` local is still on the stack but the compiler may assume it never changes.

**`volatile`.** It tells the compiler that an object may change in ways the code does not show, so every access in the source must really happen, in order. Three situations need it: a memory-mapped hardware register, a flag set by a signal handler or interrupt service routine, and a variable modified by `setjmp`/`longjmp` paths. Consider the loop `while (!flag) ;` waiting for an interrupt.

```c
int flag;            void wait_plain(void) { while (!flag) ; }
volatile int vflag;  void wait_vol(void)   { while (!vflag) ; }
```

::: lab
`LAB 2.2 · 10 MIN`

```bash
gcc -O2 -S -o - v.c | grep -v '^\s*\.'
```

```
wait_plain:  movl flag(%rip),%eax ; testl %eax,%eax ; jne .L1 ; jmp .L3
wait_vol:    movl vflag(%rip),%eax ; testl %eax,%eax ; je .L6 ; ret
```

**What you should notice:** `wait_plain` loads `flag` once and then spins on `jmp .L3` without reading memory again, so it never sees the change. `wait_vol` branches back to the load on each pass (the `.L6` label), because every access to a `volatile` object must happen.
:::

A `const volatile` object is legal and useful: the program may not write it, but hardware may change it, as with a read-only status register. In an embedded driver one writes `volatile const uint32_t *status = (volatile const uint32_t *)0x40021000;`.

::: trap
*Claim:* `volatile` makes a shared flag safe between two threads. *Why it is wrong:* `volatile` prevents the compiler from caching a value but provides neither atomicity nor memory ordering between processors, so a read may see a stale value or a torn one on a multi-core machine. *Correct statement:* use `_Atomic` (C11) or the primitives of Pillar 7 for threads; reserve `volatile` for hardware registers and signal handlers (and there prefer `volatile sig_atomic_t`).
:::

**`restrict` and `inline`.** `restrict` is a promise by the programmer that, during the pointer's lifetime, no other pointer reaches the same object; `memcpy` is declared with `restrict` parameters, which is exactly why overlapping use is undefined. `inline` suggests substituting the function body at the call site; the compiler decides. Together with `static` it is the type-safe alternative to a function-like macro ([2.11](#s2-11){.ref}). The two tables that summarise qualifiers and storage classes are in the [Revision Spread](#rv2){.ref}.

::: check
1. Two files each contain `static int n;`. Does the linker report a clash? [^c2-10]
2. Why can a `volatile` read not be removed by the optimiser even when its result is unused? [^c2-11]
:::

[^c2-10]: No; `static` gives internal linkage, so each file has its own `n`.
[^c2-11]: The access may itself have an effect, such as clearing a status bit in a device register, so the standard treats it as observable behaviour.

## [2.7]{.sec}Structs, unions, padding and alignment [Must · ■■□]{.tag} {#s2-7}

A `struct` groups members laid out in declaration order. The compiler may not reorder them, but it may insert unused bytes called *padding*, because processors read an `n`-byte value most efficiently, or only correctly, at an address divisible by `n`. This divisibility rule is the member's *alignment requirement*. Three rules give the layout of any structure.

::: bigidea
Each member sits at the next offset divisible by its own alignment, and the structure's size is rounded up to a multiple of its largest member's alignment so that arrays of the structure stay aligned.
:::

On LP64 the alignment of each basic type equals its size: `char` 1, `short` 2, `int` 4, `long` and pointers 8, `double` 8. Figure 2.4 applies the rules to one structure and to its reordering.

<figure>
<svg viewBox="0 0 480 190" width="480">
  <text class="mono" x="4" y="14">struct A { char c; int i; char d; };   sizeof = 12</text>
  <g transform="translate(10,22)">
    <rect class="box" x="0" y="0" width="30" height="24"/><text class="lbl" x="15" y="16" text-anchor="middle">c</text>
    <rect class="fill" x="30" y="0" width="90" height="24"/><text class="sm" x="75" y="15" text-anchor="middle">padding 3</text>
    <rect class="box" x="120" y="0" width="120" height="24"/><text class="lbl" x="180" y="16" text-anchor="middle">i (4 bytes)</text>
    <rect class="box" x="240" y="0" width="30" height="24"/><text class="lbl" x="255" y="16" text-anchor="middle">d</text>
    <rect class="fill" x="270" y="0" width="90" height="24"/><text class="sm" x="315" y="15" text-anchor="middle">padding 3</text>
    <text class="sm" x="0" y="38">offset 0</text><text class="sm" x="120" y="38">4</text><text class="sm" x="240" y="38">8</text><text class="sm" x="345" y="38">12</text>
  </g>
  <text class="mono" x="4" y="94">struct B { int i; char c; char d; };   sizeof = 8</text>
  <g transform="translate(10,102)">
    <rect class="box" x="0" y="0" width="120" height="24"/><text class="lbl" x="60" y="16" text-anchor="middle">i (4 bytes)</text>
    <rect class="box" x="120" y="0" width="30" height="24"/><text class="lbl" x="135" y="16" text-anchor="middle">c</text>
    <rect class="box" x="150" y="0" width="30" height="24"/><text class="lbl" x="165" y="16" text-anchor="middle">d</text>
    <rect class="fill" x="180" y="0" width="60" height="24"/><text class="sm" x="210" y="15" text-anchor="middle">padding 2</text>
    <text class="sm" x="0" y="38">offset 0</text><text class="sm" x="120" y="38">4</text><text class="sm" x="150" y="38">5</text><text class="sm" x="225" y="38">8</text>
  </g>
  <rect class="fill" x="380" y="26" width="14" height="14"/><text class="sm" x="400" y="37">padding byte</text>
  <text class="sm" x="10" y="170">One cell is one byte (30 units wide). Reordering the members by decreasing size removes 4 of the 12 bytes.</text>
</svg>
<figcaption><b>Figure 2.4</b> Padding in <code>struct A</code> and its reordering. Shaded cells are padding and hold unspecified values.</figcaption>
</figure>

In `struct A` the `int` cannot start at offset 1, so three padding bytes follow `c`. The last `char` ends at offset 9, but the size must be a multiple of 4, so three more bytes follow it. Placing the members in decreasing size order, as in `struct B`, needs only two. The same method answers the reported Qualcomm questions: for `struct { char a; int b; short c; }` the offsets are 0, 4 and 8 and the size is 12; reordered as `int, short, char` it is 8. For `struct { short s; long l; char c; }` the offsets on LP64 are 0, 8 and 16 and the size is 24; on a 32-bit x86 system `long` is 4 bytes with alignment 4, so the offsets are 0, 4 and 8 and the size is 12.

A `union` stores all its members at offset 0, so its size is the largest member rounded up to the strictest alignment. For `union { int i; char c[5]; }` the size is 8, not 5. Only the member last written is meaningful in the portable sense; reading another member reinterprets the bytes (*type punning*), which C99 permits through unions but C++ does not. The usual use is the *tagged union*, a structure with a tag and a union of alternatives, which stores one of several message formats in the space of the largest.

```c
struct msg { enum { MSG_HELLO, MSG_DATA } type;
             union { struct { uint32_t id; }            hello;
                     struct { uint16_t len; uint8_t b[64]; } data; } u; };
```

Padding can be removed with `__attribute__((packed))` or `#pragma pack(1)`, which gives `struct A` the size 6. The price is misaligned member access: x86 handles it at some cost, but strict-alignment processors may fault or take a trap, and taking a pointer to a packed member is a warning for this reason. Packing is therefore acceptable for describing a layout that a protocol dictates, provided members are read with `memcpy` or byte shifts. Two further hazards are worth knowing. Comparing structures with `memcmp` is wrong, because the padding bytes are unspecified. Sending a structure straight over a socket is wrong, because padding, member sizes and byte order all differ between machines ([2.9](#s2-9){.ref}); fields must be serialised one by one.

The standard macro `offsetof(type, member)` from `<stddef.h>` gives a member's byte offset. Its inverse, `container_of`, recovers the enclosing structure from a pointer to a member, and is the basis of the intrusive lists of the Linux kernel.

```c
#define container_of(ptr, type, member) \
    ((type *)((char *)(ptr) - offsetof(type, member)))
```

::: example
**Size of a structure without `sizeof`** (a reported Qualcomm question).

1. Declare one object `struct A a;`.
2. Take the address one element past it, `&a + 1`; pointer arithmetic scales by the whole structure.
3. Cast both addresses to `char *` and subtract, so that the unit becomes bytes.

[Result: `(char *)(&a + 1) - (char *)&a` evaluates to 12 for `struct A`.]{.result}
:::

::: lens
[QUALCOMM · CISCO · BROADCOM]{.co}

Structure versus union, padding with a worked size, and reordering to minimise size are the most frequently reported C questions. A strong answer states the three rules, draws the byte map as in Figure 2.4, and mentions packing and its cost. The follow-up is nearly always "can you send this over the network?".
:::

::: check
1. What is `sizeof(struct { char a; short b; char c; })` on LP64? [^c2-12]
2. What is the minimum size after reordering? [^c2-13]
:::

[^c2-12]: Offsets 0, 2, 4, so the members end at 5; rounding to a multiple of 2 gives 6.
[^c2-13]: Order `short, char, char` gives offsets 0, 2, 3, ending at 4, and the size is 4.

## [2.8]{.sec}Bit-fields and bit manipulation [Must · ■■□]{.tag} {#s2-8}

Embedded and protocol code reads and writes individual bits constantly. The four basic operations on an unsigned integer `x` use a mask with a single 1 at bit `n`: set with `x |= 1u << n`, clear with `x &= ~(1u << n)`, toggle with `x ^= 1u << n`, and test with `(x >> n) & 1u`. The `u` suffix matters, because `1 << 31` shifts into the sign bit of an `int`, which is undefined ([2.12](#s2-12){.ref}). As macros, with every argument parenthesised ([2.11](#s2-11){.ref}):

```c
#define SET_BIT(x, n)    ((x) |=  (1u << (n)))
#define CLEAR_BIT(x, n)  ((x) &= ~(1u << (n)))
#define TOGGLE_BIT(x, n) ((x) ^=  (1u << (n)))
#define TEST_BIT(x, n)   (((x) >> (n)) & 1u)
```

A multi-bit *field* is read by shifting and masking, and written by clearing the field before inserting the value. This read-modify-write helper is the classic register-access question.

```c
static inline uint32_t get_field(uint32_t reg, unsigned shift, unsigned width) {
    return (reg >> shift) & ((1u << width) - 1u);
}
static inline uint32_t set_field(uint32_t reg, unsigned shift, unsigned width, uint32_t val) {
    uint32_t mask = ((1u << width) - 1u) << shift;     /* width < 32 assumed */
    return (reg & ~mask) | ((val << shift) & mask);
}
```

Two idioms recur. Kernighan's population count loops `while (x) { x &= x - 1; n++; }`, because `x & (x - 1)` clears the lowest set bit, so the loop runs once per set bit. A power-of-two test is `x != 0 && (x & (x - 1)) == 0`, since a power of two has a single set bit. Further bit-level exercises appear in [Pillar 1](#ch1){.ref}.

*Bit-fields* let the compiler do the shifting: `struct { unsigned ihl:4, version:4; }`. They are convenient, yet the standard leaves the order of fields within a byte, the byte order of larger units and the behaviour of fields straddling units to the implementation. The experiment below shows the same value assigned to the same two fields in two declaration orders.

```c
struct bf1 { unsigned int version:4, ihl:4; };   /* version declared first */
struct bf2 { unsigned int ihl:4, version:4; };   /* ihl declared first     */
/* with version = 4, ihl = 5, first byte on x86-64 gcc:  bf1 -> 0x54,  bf2 -> 0x45 */
```

On this platform gcc places the first-declared field in the low-order bits, so only `bf2` produces the wire byte `0x45` of an IPv4 header, and the correct declaration order is reversed on a big-endian target. Hence, bit-fields are a poor choice for wire formats and are best kept for private data and hardware registers of a known compiler; portable code extracts fields with shifts and masks, as in [2.14](#s2-14){.ref}.

## [2.9]{.sec}Endianness and byte order [Must · ■■□]{.tag} {#s2-9}

A 32-bit integer occupies four bytes, and *endianness* is the order in which they are stored. A *big-endian* machine stores the most significant byte at the lowest address; a *little-endian* machine stores the least significant byte first. x86 and most ARM systems run little-endian, whereas the Internet protocols are defined in big-endian order, termed *network byte order*.

<figure>
<svg viewBox="0 0 480 150" width="480">
  <text class="lbl" x="4" y="14">Value 0x0A0B0C0D stored at address 0x100</text>
  <text class="sm" x="4" y="42">address</text><text class="sm" x="100" y="42" text-anchor="middle">0x100</text><text class="sm" x="170" y="42" text-anchor="middle">0x101</text><text class="sm" x="240" y="42" text-anchor="middle">0x102</text><text class="sm" x="310" y="42" text-anchor="middle">0x103</text>
  <text class="lbl" x="4" y="68">Big-endian</text>
  <rect class="box" x="65" y="50" width="70" height="28"/><rect class="box" x="135" y="50" width="70" height="28"/><rect class="box" x="205" y="50" width="70" height="28"/><rect class="box" x="275" y="50" width="70" height="28"/>
  <text class="mono" x="100" y="68" text-anchor="middle">0A</text><text class="mono" x="170" y="68" text-anchor="middle">0B</text><text class="mono" x="240" y="68" text-anchor="middle">0C</text><text class="mono" x="310" y="68" text-anchor="middle">0D</text>
  <text class="sm" x="360" y="68">most significant byte first = network order</text>
  <text class="lbl" x="4" y="108">Little-endian</text>
  <rect class="box" x="65" y="90" width="70" height="28"/><rect class="box" x="135" y="90" width="70" height="28"/><rect class="box" x="205" y="90" width="70" height="28"/><rect class="box" x="275" y="90" width="70" height="28"/>
  <text class="mono" x="100" y="108" text-anchor="middle">0D</text><text class="mono" x="170" y="108" text-anchor="middle">0C</text><text class="mono" x="240" y="108" text-anchor="middle">0B</text><text class="mono" x="310" y="108" text-anchor="middle">0A</text>
  <text class="sm" x="360" y="108">least significant byte first (x86, ARM)</text>
  <path class="acc" d="M65,128 L345,128"/><text class="sm" x="205" y="142" text-anchor="middle">htonl swaps these four bytes on a little-endian host</text>
</svg>
<figcaption><b>Figure 2.5</b> The same 32-bit value in memory on a big-endian and a little-endian machine.</figcaption>
</figure>

Byte order concerns bytes, not bits: the bits inside a byte are not reordered by any API. The headers `<arpa/inet.h>` provide four conversions: `htons` and `htonl` (host to network, 16- and 32-bit) and `ntohs` and `ntohl` (network to host). On a big-endian host they do nothing, so code that calls them is correct on both kinds of machine. If the call is forgotten, the program works against itself and fails against others: the port 80 is `0x0050`, which a little-endian host stores as the bytes `50 00`, and a peer reading those bytes in network order sees `0x5000`, which is 20480.

```c
uint16_t port = 80;
printf("%04x %04x\n", port, htons(port));              /* 0050 5000 */
uint8_t w[2] = {0x00, 0x50};  uint16_t raw;  memcpy(&raw, w, 2);
printf("%u %u\n", raw, ntohs(raw));                    /* 20480 80  */
```

To detect the host order, store 1 in an integer and inspect the byte at the lowest address. The union form is defined behaviour; reading through an `unsigned char *` also works, because character types may alias any object.

```c
int is_little_endian(void) {
    union { unsigned int i; unsigned char c[4]; } u = { .i = 1 };
    return u.c[0] == 1;                 /* least significant byte stored first */
}
uint32_t swap32(uint32_t x) {
    return (x >> 24) | ((x >> 8) & 0x0000FF00u) | ((x << 8) & 0x00FF0000u) | (x << 24);
}
```

For `x = 0x0A0B0C0D`, `swap32(x)` returns `0x0D0C0B0A`, which is what `htonl` produces on this host. A final rule governs reading wire data: do not cast a byte pointer to `uint32_t *` and dereference, because the address may be misaligned and the cast violates aliasing rules. Assemble the value from bytes, `(p[0] << 24) | (p[1] << 16) | (p[2] << 8) | p[3]`, which is correct on every host without any conversion call. The socket calls that use `htons` for ports are treated in [Pillar 7](#ch7){.ref}.

::: lens
[CISCO · JUNIPER · ARISTA · BROADCOM]{.co}

"Write a program to detect endianness" and "why do we need `htons`?" are reported at Cisco, and byte-order questions are common at every systems employer. A strong answer draws Figure 2.5, writes the union test, implements `swap32` with shifts, and explains that the conversion functions are portable no-ops on big-endian hosts. Follow-up: are the bits inside a byte also swapped (no, bits are not addressable, so only bytes move).
:::

::: check
1. What are the four bytes of 0x12345678 in memory on x86? [^c2-14]
2. Why is `*(uint32_t *)buf` a poor way to read a header field? [^c2-15]
:::

[^c2-14]: `78 56 34 12`, in increasing address order, since x86 is little-endian.
[^c2-15]: The address may be misaligned, the cast breaks the aliasing rules, and the value is in network order and still needs `ntohl`.

:::
