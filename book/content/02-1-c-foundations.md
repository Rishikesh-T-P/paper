::: {.chapter .p2}
::: opener
[Part I · Pillar 2]{.part-label}

[2]{.num}

# Programming: C, Python, C++ {#ch2}

[Network software is written close to the machine; we learn to see the bytes behind every line.]{.promise}

1. [2.1 Memory layout of a process]{} [MUST]{}
2. [2.2 Types, sizes and conversions]{} [MUST]{}
3. [2.3 Pointers and pointer arithmetic]{} [MUST]{}
4. [2.4 Arrays, pointers and strings]{} [MUST]{}
5. [2.5 Declarations, const and function pointers]{} [MUST]{}
6. [2.6 Storage classes and qualifiers]{} [MUST]{}
7. [2.7 Structs, unions, padding and alignment]{} [MUST]{}
8. [2.8 Bit-fields and bit manipulation]{} [MUST]{}
9. [2.9 Endianness and byte order]{} [MUST]{}
10. [2.10 Dynamic memory and leaks]{} [MUST]{}
11. [2.11 The preprocessor and macros]{} [MUST]{}
12. [2.12 Undefined behaviour]{} [MUST]{}
13. [2.13 Writing the library: memcpy to itoa]{} [MUST]{}
14. [2.14 Parsing an IPv4 header]{} [MUST]{}
15. [2.15 The gotcha gallery: 36 output traps]{} [MUST]{}
16. [2.16 Python: the data model]{} [SHOULD]{}
17. [2.17 Python: comprehensions and generators]{} [SHOULD]{}
18. [2.18 Python: struct, re, subprocess, files, exceptions]{} [MUST]{}
19. [2.19 C++: references, classes and RAII]{} [SHOULD]{}
20. [2.20 C++: virtual functions and the vtable]{} [SHOULD]{}
21. [2.21 C++: STL containers and smart pointers]{} [SHOULD]{}
:::

## [2.0]{.sec}Why this pillar matters, and how to read it {#s2-0}

Switch operating systems, routing daemons and data-plane software are written largely in C and C++, because they must control memory layout and run without a garbage collector. Automation around them is mostly Python. Interviewers therefore test C hardest: pointers, structures, bytes and output prediction. Part A (sections 2.1–2.15) is the bulk of the pillar and is entirely Must. Part B covers the Python language only, and Part C the C++ that interviews reach.

Three boundaries keep the book free of repetition. The sockets API belongs to [Pillar 7](#ch7){.ref}, shell scripting to [Pillar 8](#ch8){.ref}, Python's network libraries to [Pillar 10](#ch10){.ref}, and linked-list and tree algorithms to [Pillar 1](#ch1){.ref}. Here we meet only the language features those chapters rely on.

All code assumes 64-bit Linux (the LP64 data model), `gcc` 13 and an x86-64 processor, unless stated otherwise. Compile with `gcc -Wall -Wextra -g file.c -o file`. Every output printed below was produced by running the code under these assumptions. Where the standard leaves behaviour open, the text says so and does not print an output.

::: bigidea
A C program is a sequence of bytes at addresses; every type, pointer and structure is a rule for interpreting those bytes, and every trap in this pillar is a place where the rule and the bytes disagree.
:::

## [2.1]{.sec}Memory layout of a process [Must · ■□□]{.tag} {#s2-1}

When Linux starts a program it gives the process a private *virtual address space*, a range of addresses that the hardware maps to physical memory page by page. The kernel divides this space into regions called *segments* or *sections*, and the C compiler decides which region each object lives in. Knowing the regions answers a surprising share of interview questions, among them "where does a static local live?" and "why did this big array crash my program?".

<figure>
<svg viewBox="0 0 480 300" width="480">
  <defs><marker id="a21" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" class="accf"/></marker></defs>
  <text class="sm" x="20" y="14">high addresses</text>
  <rect class="fill" x="120" y="20" width="150" height="22"/>
  <text class="lbl" x="195" y="35" text-anchor="middle">kernel space</text>
  <rect class="box" x="120" y="42" width="150" height="46"/>
  <text class="lbl" x="195" y="63" text-anchor="middle">stack</text>
  <text class="sm" x="195" y="78" text-anchor="middle">grows towards lower addresses</text>
  <line class="acc" x1="285" y1="52" x2="285" y2="86" marker-end="url(#a21)"/>
  <rect class="box dash" x="120" y="88" width="150" height="40" style="fill:#fafafa"/>
  <text class="lbl" x="195" y="106" text-anchor="middle">unmapped gap</text>
  <text class="sm" x="195" y="119" text-anchor="middle">mmap area, shared libraries</text>
  <rect class="box" x="120" y="128" width="150" height="40"/>
  <text class="lbl" x="195" y="148" text-anchor="middle">heap</text>
  <text class="sm" x="195" y="160" text-anchor="middle">grows towards higher addresses</text>
  <line class="acc" x1="285" y1="166" x2="285" y2="132" marker-end="url(#a21)"/>
  <rect class="fill" x="120" y="168" width="150" height="28"/>
  <text class="lbl" x="195" y="186" text-anchor="middle">.bss</text>
  <rect class="box" x="120" y="196" width="150" height="28"/>
  <text class="lbl" x="195" y="214" text-anchor="middle">.data</text>
  <rect class="fill" x="120" y="224" width="150" height="28"/>
  <text class="lbl" x="195" y="242" text-anchor="middle">.rodata</text>
  <rect class="box" x="120" y="252" width="150" height="28"/>
  <text class="lbl" x="195" y="270" text-anchor="middle">.text</text>
  <text class="sm" x="20" y="294">low addresses</text>
  <text class="sm" x="305" y="62">locals, arguments, return addresses</text>
  <text class="sm" x="305" y="148">malloc blocks (brk, mmap)</text>
  <text class="sm" x="285" y="185">zero-initialised globals and statics</text>
  <text class="sm" x="285" y="213">initialised globals and statics</text>
  <text class="sm" x="285" y="241">string literals, const globals</text>
  <text class="sm" x="285" y="269">machine code (read-only, executable)</text>
  <text class="sm" x="20" y="213">in the file</text>
  <path class="lg" d="M92,196 L98,196 L98,280 L92,280"/>
</svg>
<figcaption><b>Figure 2.1</b> The layout of a Linux process. The three lowest sections come from the executable file; .bss occupies no space in the file.</figcaption>
</figure>

Figure 2.1 shows the regions from the high addresses downwards. The *text* section holds machine code and is read-only. The *rodata* section holds string literals and `const` globals. The *data* section holds globals and statics with a non-zero initial value, and the *BSS* (block started by symbol) holds those initialised to zero, which is why the file records only their total size. The *heap* serves `malloc`, and the *stack* serves function calls. Between them lies unmapped space, so that neither can grow into the other without a fault.

| Object | Section | Lifetime | Initial value |
|---|---|---|---|
| `int g = 7;` (global) | .data | whole program | 7 |
| `int g;` (global) | .bss | whole program | 0 |
| `static int s;` (file or function scope) | .bss (.data if initialised) | whole program | 0 |
| `const int k = 3;` (global) | .rodata | whole program | 3 |
| `"hello"` (string literal) | .rodata | whole program | the bytes |
| `int x;` (local) | stack | until the block ends | indeterminate |
| `malloc(n)` | heap | until `free` | indeterminate |

::: example
**Classify the objects in a small program.**

1. Compile the program below and print the address of one object from each row of the table.
2. Read the addresses in order. Code, literals and globals sit close together near the bottom, the heap lies above them, and the stack is far higher.
3. Check the sizes with `size`: the BSS figure counts the zero-initialised bytes, while `text` includes the read-only data.

```c
int g_init = 7;  int g_zero;  const int g_ro = 3;
int main(void) {
    static int s_init = 9;      /* .data */
    int local = 1;              /* stack */
    char *lit = "hello";        /* pointer: stack, bytes: .rodata */
    int *h = malloc(sizeof *h); /* heap */
    printf("%p %p %p\n", (void *)&g_ro, (void *)h, (void *)&local);
    free(h); (void)s_init; (void)lit; return 0;
}
```

[Result: on one run the three addresses were `0x5595455f9004`, `0x55954f44b2a0` and `0x7fffa525c4f4`, in increasing order. Exact values change on every run because of address-space randomisation; only the order is stable.]{.result}
:::

::: trap
*Claim:* a `static` local array is stored on the stack like any other local. *Why it is wrong:* `static` changes the lifetime, not just the visibility, so the array is placed in .data or .bss and exists for the whole run. *Correct statement:* making a large local array `static` removes the stack-overflow risk, but the function is then no longer re-entrant, because every call shares the same bytes.
:::

::: lens
[QUALCOMM · ARISTA · CISCO]{.co}

"What kind of variable is stored where?" is a reported Qualcomm question, and Arista has asked candidates to print and classify the addresses of a global, a static, a local, a heap object and a literal. A strong answer draws Figure 2.1 from memory, names the section for each object, and adds that the stack and heap grow towards each other. Follow-ups: what is the BSS for, and what happens on stack overflow (a segmentation fault from the guard page).
:::

::: check
1. In which section does `static int n = 0;` inside a function live? [^c2-1]
2. Why does the BSS take no room in the executable file? [^c2-2]
3. Where is the pointer `char *p = "abc";` stored, and where are the characters? [^c2-3]
:::

[^c2-1]: .bss, because the initial value is zero; `static int n = 5;` would be in .data.
[^c2-2]: Its contents are known to be zero, so the file records only the size and the loader supplies zeroed pages.
[^c2-3]: The pointer follows the rule for its own storage (stack for a local, .data for a global); the characters are in .rodata.

## [2.2]{.sec}Types, sizes and conversions [Must · ■□□]{.tag} {#s2-2}

The size of `int` is not fixed by the language. The standard guarantees only that `char` is one byte and that `sizeof(short) <= sizeof(int) <= sizeof(long)`. On 64-bit Linux (the *LP64* model) `int` is 4 bytes while `long` and pointers are 8; on 32-bit systems (*ILP32*) all three are 4. The full size table is in the [Revision Spread](#rv2){.ref}. Code that handles packet fields must therefore use the fixed-width types of `<stdint.h>`: `uint8_t`, `uint16_t`, `uint32_t` and `uint64_t`, printed with the macros `PRIu32` and its relatives from `<inttypes.h>`.

[**Integer promotion** — in an expression, any type narrower than `int` is first widened to `int`, so `char + char` is computed as `int`.]{.margin}Arithmetic does not happen in the narrow type. Two rules govern every mixed expression. First, the *integer promotions* widen `char` and `short` operands to `int`. Second, the *usual arithmetic conversions* bring the two operands to a common type: if one is `unsigned int` and the other `int`, the signed one is converted to unsigned. This is the origin of several famous surprises.

```c
uint8_t x = 200, y = 100;
printf("%d\n", x + y);                 /* 300, not 44: computed as int */
unsigned int u = 1; int b = -1;
printf("%s\n", b < u ? "true" : "false"); /* false: -1 becomes 4294967295 */
```

The first line prints `300` because both operands are promoted; the sum is truncated to 44 only when stored back into a `uint8_t`. The second prints `false` because `-1` converted to `unsigned int` is `UINT_MAX`. Hence, comparing a signed and an unsigned value is a defect unless one has first proved the signed value is non-negative; `gcc -Wextra` warns about it.

*Signedness of `char`* is implementation-defined: it is signed on x86 and unsigned on most ARM Linux builds. Thus `char c = 200;` stores -56 on x86 and 200 on ARM, and any code that indexes a table with a plain `char` is a latent bug. Use `unsigned char` or `uint8_t` for bytes.

*Overflow* behaves differently by signedness. Unsigned arithmetic wraps modulo 2^n and is fully defined, which is exactly what a 32-bit byte counter needs: with `uint32_t before, after`, the expression `after - before` yields the correct delta even after the counter wraps. Signed overflow is undefined behaviour ([2.12](#s2-12){.ref}).

## [2.3]{.sec}Pointers and pointer arithmetic [Must · ■□□]{.tag} {#s2-3}

A *pointer* is a variable that holds an address. If `int x = 5;` then `&x` is the address of `x`, and for `int *p = &x;` the expression `*p` is the object at that address, so `*p = 9;` changes `x`. A pointer that points nowhere holds `NULL`, and dereferencing it is undefined behaviour that in practice raises a segmentation fault. A pointer of type `T *` knows the size of `T`, and this size drives all pointer arithmetic.

::: bigidea
Adding `n` to a `T *` moves the address by `n * sizeof(T)` bytes, so pointer arithmetic counts elements, not bytes.
:::

<figure>
<svg viewBox="0 0 480 120" width="480">
  <defs><marker id="a22" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" class="accf"/></marker></defs>
  <rect class="box" x="60" y="40" width="90" height="30"/><rect class="box" x="150" y="40" width="90" height="30"/>
  <rect class="box" x="240" y="40" width="90" height="30"/><rect class="box" x="330" y="40" width="90" height="30"/>
  <text class="lbl" x="105" y="59" text-anchor="middle">a[0] = 10</text><text class="lbl" x="195" y="59" text-anchor="middle">a[1] = 20</text>
  <text class="lbl" x="285" y="59" text-anchor="middle">a[2] = 30</text><text class="lbl" x="375" y="59" text-anchor="middle">a[3] = 40</text>
  <text class="sm" x="60" y="84">0x100</text><text class="sm" x="150" y="84">0x104</text><text class="sm" x="240" y="84">0x108</text><text class="sm" x="330" y="84">0x10C</text>
  <text class="lbl" x="105" y="18" text-anchor="middle">p</text><text class="lbl" x="285" y="18" text-anchor="middle">p + 2</text>
  <line class="acc" x1="105" y1="22" x2="105" y2="38" marker-end="url(#a22)"/>
  <line class="acc" x1="285" y1="22" x2="285" y2="38" marker-end="url(#a22)"/>
  <path class="lg" d="M60,100 L420,100"/><text class="sm" x="240" y="113" text-anchor="middle">each int is 4 bytes, so p + 2 is 8 bytes beyond p</text>
</svg>
<figcaption><b>Figure 2.2</b> With <code>int *p = a;</code>, the pointer <code>p + 2</code> holds 0x108, because the address advances by two elements of four bytes.</figcaption>
</figure>

The rules are short. Adding or subtracting an integer moves the pointer by that many elements. Subtracting two pointers into the same array gives the number of elements between them, of type `ptrdiff_t`. Comparing pointers is meaningful only within one array. A `void *` carries no element size, so it cannot be dereferenced or incremented in standard C; it converts implicitly to and from any object pointer type in C, which is why `malloc` returns it. To step through raw bytes, cast to `unsigned char *`.

```c
int a[4] = {10, 20, 30, 40};
int *p = a;
printf("%d %d\n", *(p + 2), p[3]);                    /* 30 40 */
printf("%ld\n", (long)(&a[3] - &a[0]));               /* 3: elements   */
printf("%ld\n", (long)((char *)(p + 1) - (char *)p)); /* 4: bytes      */
```

A function receives copies of its arguments, so to modify the caller's variable it must receive its address. The same idea with one more level gives the pointer to pointer, needed whenever a function must change a pointer itself, as when it allocates memory for the caller.

```c
void swap(int *a, int *b) { int t = *a; *a = *b; *b = t; }

int make_buffer(char **out, size_t n) {   /* caller's pointer is changed */
    *out = malloc(n);
    return *out ? 0 : -1;
}
```

::: trap
*Claim:* `p + 1` always adds one to the address. *Why it is wrong:* the increment is scaled by the pointee size, so for `int *p` the address grows by 4, and for `struct ethhdr *` by 14. *Correct statement:* to move by bytes, cast to `unsigned char *` first, as in `(uint8_t *)p + 1`.
:::

::: check
1. If `long *q` holds 0x2000, what does `q + 3` hold? [^c2-4]
2. What does `&a[3] - &a[0]` evaluate to for `int a[4]`, and what is its type? [^c2-5]
:::

[^c2-4]: 0x2018, since 3 elements of 8 bytes add 24 bytes.
[^c2-5]: 3, of type `ptrdiff_t` (a signed integer); the unit is elements, not bytes.

## [2.4]{.sec}Arrays, pointers and strings [Must · ■□□]{.tag} {#s2-4}

An array is a contiguous block of elements, and a pointer is a single address; they are different things that the language lets one mix. In nearly every expression the name of an array *decays* to a pointer to its first element, so `a[i]` is defined as `*(a + i)`. The exceptions are the operand of `sizeof`, the operand of `&`, and a string literal that initialises an array. Because `a[i]` means `*(a + i)` and addition commutes, even `i[a]` is legal and means the same.

```c
int m[2][3] = {{1, 2, 3}, {4, 5, 6}};
printf("%d %d %zu\n", m[1][2], *(*(m + 1) + 2), sizeof m);  /* 6 6 24 */
printf("%zu %zu\n", sizeof(m[0]), sizeof(&m[0]));           /* 12 8   */
```

A two-dimensional array is an array of arrays laid out row by row, so `m[0]` is itself an array of 3 ints (12 bytes) and `&m[0]` is a pointer to it (8 bytes). Decay has one consequence that every interviewer tests: an array *parameter* is really a pointer. In `void f(int a[10])` the `10` is ignored and `sizeof(a)` is 8. Hence a function that needs the length must receive it as a separate argument.

A C *string* is an array of `char` ending with a zero byte `'\0'`. Its length excludes the terminator, while its storage includes it. Two declarations look alike and differ completely, as Figure 2.3 shows.

<figure>
<svg viewBox="0 0 480 130" width="480">
  <defs><marker id="a23" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" class="accf"/></marker></defs>
  <text class="mono" x="10" y="16">char s[] = "abc";</text>
  <rect class="box" x="10" y="26" width="30" height="26"/><rect class="box" x="40" y="26" width="30" height="26"/><rect class="box" x="70" y="26" width="30" height="26"/><rect class="fill" x="100" y="26" width="30" height="26"/>
  <text class="mono" x="25" y="43" text-anchor="middle">a</text><text class="mono" x="55" y="43" text-anchor="middle">b</text><text class="mono" x="85" y="43" text-anchor="middle">c</text><text class="mono" x="115" y="43" text-anchor="middle">\0</text>
  <text class="sm" x="10" y="68">4 bytes on the stack (or .data); writable</text>
  <text class="mono" x="250" y="16">char *p = "abc";</text>
  <rect class="box" x="250" y="26" width="64" height="26"/><text class="mono" x="282" y="43" text-anchor="middle">p</text>
  <rect class="fill" x="380" y="26" width="24" height="26"/><rect class="fill" x="404" y="26" width="24" height="26"/><rect class="fill" x="428" y="26" width="24" height="26"/><rect class="fill" x="452" y="26" width="24" height="26"/>
  <text class="mono" x="392" y="43" text-anchor="middle">a</text><text class="mono" x="416" y="43" text-anchor="middle">b</text><text class="mono" x="440" y="43" text-anchor="middle">c</text><text class="mono" x="464" y="43" text-anchor="middle">\0</text>
  <line class="acc" x1="314" y1="39" x2="378" y2="39" marker-end="url(#a23)"/>
  <text class="sm" x="250" y="68">8-byte pointer, then 4 bytes in .rodata; read-only</text>
  <text class="mono" x="10" y="100">sizeof s = 4   strlen(s) = 3</text>
  <text class="mono" x="250" y="100">sizeof p = 8   strlen(p) = 3</text>
</svg>
<figcaption><b>Figure 2.3</b> An array owns its characters; a pointer to a literal merely refers to read-only characters.</figcaption>
</figure>

Writing through `p[0] = 'A'` in the second form is undefined behaviour and normally faults, because the literal is in read-only memory. With the array form the write is legal, since the array is a private, writable copy.

The standard string functions all walk to the terminator. `strlen(s)` counts characters and is O(n). `strcpy(d, s)` copies until and including the terminator and does not check that `d` is large enough; this is the classic buffer overflow. `strncpy(d, s, n)` is not its safe version: if `s` has `n` or more characters it writes no terminator, and if it has fewer it pads `d` with zeros up to `n`. The reliable idiom is `snprintf(d, sizeof d, "%s", s)`, which always terminates. `strcmp` returns zero for equal strings and otherwise a negative or positive value, so `if (strcmp(a, b))` is true when the strings *differ*.

::: lab
`LAB 2.1 · 15 MIN`

```bash
gcc -Wall -g -o strdemo strdemo.c      # strdemo.c: the two declarations of Figure 2.3
./strdemo
gcc -g -fsanitize=address -o strdemo strdemo.c && ./strdemo
```

With `p[0] = 'A'` uncommented, the plain build prints `Segmentation fault`. The sanitised build prints `AddressSanitizer: SEGV on unknown address` and a stack trace whose top frame names the line.

**What you should notice:** the array form never faults, and the sanitiser reports the line, which is quicker than reading a core dump.
:::

::: check
1. What does `sizeof(a)` return inside `void f(int a[10])` on a 64-bit machine? [^c2-6]
2. After `strncpy(d, "abcdef", 3)`, is `d` a valid string? [^c2-7]
:::

[^c2-6]: 8, because the parameter is a pointer; the length 10 is ignored.
[^c2-7]: Not necessarily: three characters were copied and no terminator was written, so `d` is terminated only if its fourth byte happened to be zero.

:::
