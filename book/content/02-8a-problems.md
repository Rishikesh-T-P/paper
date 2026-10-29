::: {.p2}

::: pack
## Problem Set {#ps2}

Every interview question of this pillar is solved once, here, in the compact template: a 30-second answer first, then the approach, code, follow-ups and common mistakes where they apply. Tags give the companies and round where the question was reported, the difficulty (■□□ easy, ■■□ medium, ■■■ hard), and **S** when a specific question was reported by candidates or **T** when only the topic was reported and the wording is ours. Questions whose subject belongs to another pillar are listed at the end of the second part with a pointer.

::: problems

::: q
### Q2.1 What is the difference between a structure and a union? Give a use for a union.
[QUALCOMM · CISCO · TECH-1 · ■□□ · S]{.meta}

[30-second answer: a structure stores every member one after another; a union stores all members at the same address, so its size is that of its largest member and only one is valid at a time.]{.short}

**Answer.** `struct { int i; char c; }` is 8 bytes on LP64; `union { int i; char c; }` is 4. Use a union for one storage that holds alternative message formats, selected by a tag ([2.7](#s2-7){.ref}), or to view the same bytes as different types (endianness test). **Mistakes.** Reading a member other than the last written is reinterpretation of bytes, not conversion.
:::

::: q
### Q2.2 What is structure padding and why does the compiler add it?
[QUALCOMM · CISCO · TECH-1 · ■□□ · S]{.meta}

[30-second answer: the compiler inserts unused bytes so that each member starts at an address divisible by its alignment, because misaligned access is slower or faults on some processors.]{.short}

**Answer.** `struct { char c; int i; char d; }` has offsets 0, 4, 8 and size 12, with 6 bytes of padding (Figure 2.4). The size is rounded to a multiple of the largest alignment so arrays of the structure stay aligned. **Follow-ups.** Reorder by decreasing size, or pack with `__attribute__((packed))` at the cost of misaligned access.
:::

::: q
### Q2.3 What is `sizeof(struct { char a; int b; short c; })`? Reorder it to minimise the size.
[QUALCOMM · TECH-1 · ■■□ · S]{.meta}

[30-second answer: 12 bytes; ordering as `int b; short c; char a;` gives 8.]{.short}

**Approach.** `a` at 0; `b` needs a multiple of 4, so 4; `c` needs a multiple of 2, so 8 to 10; round to a multiple of 4: 12. Reordered: `b` at 0, `c` at 4, `a` at 6, end 7, round to 8. **Mistake.** Adding the member sizes (7) and forgetting alignment.
:::

::: q
### Q2.4 What is the size of a structure with a `short`, a `long` and a `char` on 32-bit and 64-bit machines?
[QUALCOMM · TECH-1 · ■■□ · S]{.meta}

[30-second answer: 24 bytes on 64-bit Linux (LP64) and 12 on 32-bit x86, because `long` is 8 bytes there and 4 here.]{.short}

**Approach.** For `{ short s; long l; char c; }`: LP64 offsets 0, 8, 16, end 17, rounded to 24. ILP32 offsets 0, 4, 8, end 9, rounded to 12. Order `long, short, char` gives 16 and 8. **Mistake.** Assuming `long` is 4 bytes everywhere; on 64-bit Windows (LLP64) it is 4, so the answer is machine-specific.
:::

::: q
### Q2.5 Find the size of a structure without using `sizeof`.
[QUALCOMM · TECH-1 · ■■□ · S]{.meta}

[30-second answer: take two consecutive objects and subtract their addresses as bytes.]{.short}

**Code.** For a variable: `(char *)(&x + 1) - (char *)&x`. For an array element: `(char *)&a[1] - (char *)&a[0]`. **Why.** `&x + 1` advances by one whole object, and the `char *` cast makes the difference count bytes. **Follow-up.** The macro form `((size_t)((T *)0 + 1))` relies on a null pointer and is formally undefined.
:::

::: q
### Q2.6 Worksheet: sizes of six structures on LP64.
[QUALCOMM · OA · ■■□ · S]{.meta}

[30-second answer: 24, 16, 12, 4, 8, 16.]{.short}

| Structure | Offsets | Size |
|---|---|---|
| `{char a; double d; char b;}` | 0, 8, 16 | 24 |
| `{double d; char a, b;}` | 0, 8, 9 | 16 |
| `{char a[3]; short s; int i;}` | 0, 4, 8 | 12 |
| `{short s; char c;}` | 0, 2 | 4 |
| `{int i; struct {char c; short s;} in;}` | 0, 4 (inner size 4) | 8 |
| `{char *p; char c;}` | 0, 8 | 16 |
:::

::: q
### Q2.7 What does `volatile` do? Give a scenario where you must use it.
[CISCO · QUALCOMM · TECH-1 · ■■□ · S]{.meta}

[30-second answer: `volatile` tells the compiler that an object may change outside the program's control, so every source-level access must really be performed and not cached in a register or removed.]{.short}

**Answer.** Scenarios: a memory-mapped device register, a flag set in a signal handler or interrupt routine, and variables across `setjmp`. Evidence: at `-O2` a plain `while (!flag);` loads `flag` once and spins on a `jmp`, whereas the `volatile` version reloads (Lab 2.2, [2.6](#s2-6){.ref}). **Mistake.** Using it for thread synchronisation (Q2.9).
:::

::: q
### Q2.8 Can a variable be both `const` and `volatile`? When?
[QUALCOMM · TECH-1 · ■■□ · S]{.meta}

[30-second answer: yes; the program must not write it, but hardware may change it, as with a read-only status register.]{.short}

**Answer.** `volatile const uint32_t *status = (volatile const uint32_t *)0x40021000;` forbids stores through `status` and forces a fresh load on each read. `const` alone would allow the compiler to assume the value never changes.
:::

::: q
### Q2.9 Is `volatile` enough to share a flag between two threads?
[ARISTA · QUALCOMM · TECH-2 · ■■■ · T]{.meta}

[30-second answer: no; it stops compiler caching but gives neither atomicity nor ordering between processors.]{.short}

**Answer.** Another core may see the write late or out of order relative to other writes, and a multi-word update may be seen torn. Use `_Atomic` (C11) or `atomic_flag`, or a mutex with a condition variable (Pillar 7). **Follow-up.** For a single-core signal handler, `volatile sig_atomic_t` is the correct pairing.
:::

::: q
### Q2.10 Write a program to detect whether the machine is little- or big-endian.
[CISCO · OA · ■□□ · S]{.meta}

[30-second answer: store 1 in a 32-bit integer and read its first byte; 1 means little-endian.]{.short}

**Code.** `union { unsigned i; unsigned char c[4]; } u = { .i = 1 }; return u.c[0] == 1;` An equivalent form is `*(unsigned char *)&one`, which is allowed because character types may alias anything. **Mistake.** Testing with bit shifts: shifts act on values and give the same result on both kinds of machine.
:::

::: q
### Q2.11 Why do we need `htons` and `htonl`? What breaks if we forget them?
[CISCO · JUNIPER · TECH-1 · ■□□ · S]{.meta}

[30-second answer: the network uses big-endian order and x86 is little-endian, so multi-byte fields must be converted; otherwise the peer reads the bytes reversed.]{.short}

**Answer.** Port 80 (`0x0050`) stored little-endian is `50 00`, which the peer reads as `0x5000`, i.e. 20480. On a big-endian host the functions do nothing, so the code is portable. **Mistakes.** Converting twice (which restores the wrong order), converting a value that is not in host order, and using `htons` on a 32-bit value.
:::

::: q
### Q2.12 Swap the byte order of a 32-bit integer without library calls.
[CISCO · BROADCOM · TECH-1 · ■■□ · T]{.meta}

[30-second answer: shift each byte to its mirrored position and OR them together.]{.short}

**Code.** `(x >> 24) | ((x >> 8) & 0xFF00) | ((x << 8) & 0xFF0000) | (x << 24)` with `uint32_t x`; `swap16` is `(uint16_t)((x << 8) | (x >> 8))`. `swap32(0x0A0B0C0D)` is `0x0D0C0B0A`. **Mistake.** Using signed `int`, so that `x >> 24` sign-extends. GCC offers `__builtin_bswap32`.
:::

::: q
### Q2.13 Explain the memory layout of a C program. Where do globals, statics, locals, `malloc` memory and literals live?
[ARISTA · QUALCOMM · TECH-1 · ■□□ · S]{.meta}

[30-second answer: text holds code, rodata holds literals and const globals, data holds initialised globals and statics, BSS holds zero-initialised ones, the heap holds `malloc` blocks, and the stack holds locals and return addresses.]{.short}

**Answer.** Draw Figure 2.1 in the order text, rodata, data, BSS, heap (growing up), gap, stack (growing down). A `static` local is in data or BSS. **Follow-ups.** Why BSS is not stored in the file; why the heap and stack grow towards each other; what happens on stack overflow (a fault on the guard page).
:::

::: q
### Q2.14 What is the difference between a stack and a heap allocation?
[CISCO · QUALCOMM · TECH-1 · ■□□ · T]{.meta}

[30-second answer: stack storage is automatic, fast and fixed in size per thread, and ends with the function; heap storage is explicit, slower, large, and lives until `free`.]{.short}

**Answer.** The stack is typically 8 MB per thread on Linux (`ulimit -s`), so a large local array overflows it; the heap is limited by memory. Stack allocation is a pointer adjustment; `malloc` searches free lists and can fail. Heap errors are leaks and double frees; stack errors are overflow and dangling pointers to dead frames.
:::

::: q
### Q2.15 What causes a segmentation fault?
[ARISTA · CISCO · TECH-1 · ■□□ · T]{.meta}

[30-second answer: an access to an address that is unmapped or not permitted, such as a null or wild pointer, a write to read-only memory, or a stack overflow.]{.short}

**Answer.** Typical C causes: dereferencing `NULL`, use after free, writing to a string literal, indexing far outside an array, and unbounded recursion. Method: compile with `-g -fsanitize=address`, rerun, and read the first frame of the report; or run under `gdb` and type `bt`.
:::

::: q
### Q2.16 What is the difference between a static global variable, a static local variable and a static function?
[CISCO · BROADCOM · TECH-1 · ■□□ · S]{.meta}

[30-second answer: a static local keeps its value across calls; a static global or function is visible only within its file.]{.short}

**Answer.** Local: static storage duration, zero-initialised, one instance, lives in data or BSS. Global and function: internal linkage, so other files cannot link to the name and the same name may be reused in another file. **Mistake.** Putting `static int x;` in a header: each including file gets a private copy.
:::

::: q
### Q2.17 What is wrong with `#define SQUARE(x) x*x`? Fix it. What does `SQUARE(i++)` do?
[CISCO · OA · ■□□ · S]{.meta}

[30-second answer: the argument is pasted without parentheses, so `SQUARE(2+3)` is `2+3*2+3 = 11`; the fix is `((x)*(x))`, and `i++` is then evaluated twice, which is undefined.]{.short}

**Answer.** Also `10/SQUARE(2)` expands to `10/2*2 = 10`, which shows why the whole body needs parentheses. For side effects use a `static inline` function, which evaluates its argument once ([2.11](#s2-11){.ref}).
:::

::: q
### Q2.18 Macro versus inline function: when would you use each?
[CISCO · TECH-1 · ■■□ · S]{.meta}

[30-second answer: prefer `static inline` for typed computation; use a macro only for generic code, stringification, token pasting, source location capture and conditional compilation.]{.short}

| | Macro | `static inline` |
|---|---|---|
| Type checking | none | full |
| Argument evaluation | each use re-evaluates | once |
| Debugging | expanded text, no symbol | steppable |
| Generic over types | yes | no (C11 `_Generic` aside) |
:::

::: q
### Q2.19 Predict the output: `int a[] = {1,2,3}; int *p = a; printf("%d %d", *p++, *++p);`
[CISCO · OA · ■■□ · S]{.meta}

[30-second answer: undefined behaviour; `p` is modified twice without sequencing, and the order of evaluating arguments is unspecified.]{.short}

**Answer.** Say so first, then show the defined rewrite: `int x = *p++; int y = *++p;` gives `x = 1` and `y = 3`, printed as `1 3`, because the statements are sequenced and `p` visits `a[1]` between them.
:::

::: q
### Q2.20 Explain `const int *p`, `int *const p` and `const int *const p`. Quiz of six declarations.
[CISCO · QUALCOMM · TECH-1 · ■□□ · I]{.meta}

[30-second answer: read right to left; `const` applies to what is on its left, so the first protects the pointee, the second the pointer, the third both.]{.short}

| Declaration | `*p = x` allowed? | `p = &y` allowed? |
|---|---|---|
| `const int *p` | no | yes |
| `int const *p` | no | yes |
| `int *const p` | yes | no |
| `const int *const p` | no | no |
| `const char *s` | no | yes |
| `char *const s` | yes | no |
:::

::: q
### Q2.21 What is a dangling pointer? A memory leak? How would you find each on Linux?
[CISCO · TECH-1 · ■□□ · S]{.meta}

[30-second answer: a dangling pointer refers to storage that has been freed or has gone out of scope; a leak is allocated storage with no remaining pointer. AddressSanitizer finds the first; valgrind or LeakSanitizer finds the second.]{.short}

**Answer.** Build with `-fsanitize=address`: a use after free prints a report with the allocation and free stacks; a leak prints the allocation line (Lab 2.3). Prevention: set pointers to `NULL` after `free`, never return the address of a local, and own each block in exactly one place.
:::

::: q
### Q2.22 `malloc` versus `calloc`. What does `realloc` do if it cannot grow in place?
[ARISTA · CISCO · OA · ■□□ · S]{.meta}

[30-second answer: `malloc` returns uninitialised memory; `calloc` returns zeroed memory and checks the multiplication for overflow; `realloc` moves the block, copying the data and freeing the old one.]{.short}

**Answer.** If it fails it returns `NULL` and leaves the old block valid, so `p = realloc(p, n)` leaks on failure; use a temporary. Pointers into the old block dangle after a move. `free(NULL)` is a no-op.
:::

::: q
### Q2.23 Implement `memmove`. Why is `memcpy` unsafe for overlapping regions?
[QUALCOMM · BROADCOM · TECH-1 · ■■□ · T]{.meta}

[30-second answer: when the destination starts inside the source, a forward copy overwrites bytes before they are read, so `memmove` copies backwards in that case.]{.short}

**Code.** The function of [2.13](#s2-13){.ref}: if `d < s` or `d >= s + n` copy forwards, otherwise from the end. `memmove(s+2, s, 4)` on `"abcdef"` gives `"ababcd"`. Compare addresses through `uintptr_t`. **Follow-up.** `memcpy` may assume no overlap (`restrict`) and use wide copies.
:::

::: q
### Q2.24 Implement an aligned `malloc` that returns memory aligned to any power of two.
[QUALCOMM · BROADCOM · CISCO · TECH-2 · ■■■ · T]{.meta}

[30-second answer: allocate extra, round the address up to the alignment, and store the original pointer just before the returned address so that `aligned_free` can recover it.]{.short}

```c
void *aligned_malloc(size_t size, size_t align) {      /* align: power of two */
    void *raw = malloc(size + align - 1 + sizeof(void *));
    if (!raw) return NULL;
    uintptr_t a = ((uintptr_t)raw + sizeof(void *) + align - 1) & ~(uintptr_t)(align - 1);
    ((void **)a)[-1] = raw;                            /* remember the real block */
    return (void *)a;
}
void aligned_free(void *p) { if (p) free(((void **)p)[-1]); }
```

**Why.** Adding `align - 1` guarantees an aligned address inside the block; the mask `~(align - 1)` rounds down to a multiple. Room for the saved pointer is reserved before rounding. Check: `aligned_malloc(100, 64)` returns an address with `a % 64 == 0`. **Follow-up.** C11 offers `aligned_alloc`; POSIX `posix_memalign`.
:::

::: q
### Q2.25 Write a function to delete a node from a singly linked list; then do it without special-casing the head.
[ARISTA · TECH-1 · ■■□ · S]{.meta}

[30-second answer: walk with a pointer to the link, not to the node, so the head and an inner node are handled identically.]{.short}

```c
void list_delete(struct node **pp, int key) {
    while (*pp && (*pp)->v != key) pp = &(*pp)->next;   /* pp points at the link */
    if (*pp) { struct node *dead = *pp; *pp = dead->next; free(dead); }
}
```

**Complexity.** O(n) time, O(1) space. With list `1,2,3`, deleting 1, 3 and 9 leaves `2`. The classic version keeps a `prev` pointer and tests `if (!prev)` for the head. The full list library (reverse, cycle detection) belongs to [Pillar 1](#ch1){.ref}.
:::

::: q
### Q2.26 What are function pointers? Show how to dispatch packets to handlers by protocol number.
[CISCO · JUNIPER · TECH-1 · ■■□ · T]{.meta}

[30-second answer: a function pointer holds the address of code; a 256-entry array of them indexed by the protocol field replaces a `switch`, and an empty slot is `NULL`.]{.short}

**Answer.** `typedef int (*handler_fn)(const uint8_t *, size_t); static handler_fn table[256] = { [6] = on_tcp, [17] = on_udp };` then `fn = table[proto]; if (fn) fn(pkt, len);`. Handlers can register at run time by writing a slot. Full code and output in [2.5](#s2-5){.ref}.
:::

::: q
### Q2.27 What happens in recursion versus an infinite loop?
[CISCO · TECH-1 · ■□□ · S]{.meta}

[30-second answer: infinite recursion consumes a stack frame per call and ends with a stack-overflow crash, whereas an infinite loop uses constant space and runs forever.]{.short}

**Answer.** The default stack of 8 MB holds on the order of 10^5 small frames. Compilers may turn tail calls into loops at `-O2`, in which case recursion also spins. Example: `sum(n--)` never reduces its argument (T17, [2.15](#s2-15){.ref}).
:::

::: q
### Q2.28 Is `i = i++ + ++i;` valid? What does it print?
[CISCO · QUALCOMM · OA · ■□□ · T]{.meta}

[30-second answer: it compiles but has undefined behaviour, because `i` is modified twice without a sequence point; no output can be called correct.]{.short}

**Answer.** Name the rule, say that gcc's `-Wsequence-point` (in `-Wall`) warns, and state that different compilers or optimisation levels may give different values. Similar: `a[i] = i++`, `f(i++, i++)`.
:::

::: q
### Q2.29 What is `offsetof`? How does `container_of` work?
[ARISTA · BROADCOM · TECH-2 · ■■■ · T]{.meta}

[30-second answer: `offsetof(T, m)` is the byte offset of member `m` within `T`; `container_of` subtracts that offset from a pointer to the member to recover the enclosing structure.]{.short}

**Answer.** `#define container_of(ptr, T, m) ((T *)((char *)(ptr) - offsetof(T, m)))`. If `struct pkt { int id; struct list_head node; }` and `n` points at a `node`, `container_of(n, struct pkt, node)` is the packet. This lets one generic list implementation link any structure (intrusive list), as in the Linux kernel.
:::

::: q
### Q2.30 Can you send a C structure directly over a socket? What could go wrong?
[CISCO · JUNIPER · ARISTA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: not safely; padding, member sizes and byte order differ between machines and compilers, and pointers are meaningless to the receiver.]{.short}

**Answer.** Serialise field by field into a byte buffer in network order, as in [2.14](#s2-14){.ref}, and send the buffer. Packing removes padding but not endianness, and risks misaligned access. Also never send structures holding pointers. Sockets themselves are in [Pillar 7](#ch7){.ref}.
:::

::: q
### Q2.31 Bit-fields for protocol headers: good idea or not?
[QUALCOMM · BROADCOM · TECH-1 · ■■□ · T]{.meta}

[30-second answer: not for wire formats; the standard leaves field order and straddling to the implementation, so portable code uses shifts and masks.]{.short}

**Answer.** The experiment of [2.8](#s2-8){.ref} shows `{version:4, ihl:4}` giving `0x54` and `{ihl:4, version:4}` giving `0x45` on x86-64 gcc; a big-endian compiler reverses this. Bit-fields suit private structures and registers on a known compiler. `(b >> 4)` and `(b & 0x0F)` work everywhere.
:::

::: q
### Q2.32 How would you test the memory bit-cells of a memory segment using C?
[BROADCOM · TECH-2 · ■■■ · S]{.meta}

[30-second answer: write walking-one patterns and their complements to every byte, read them back, and report the first mismatch; use a `volatile` pointer so the accesses really happen.]{.short}

```c
int memtest(volatile uint8_t *p, size_t n) {
    for (int bit = 0; bit < 8; bit++) {
        uint8_t pat = (uint8_t)(1u << bit);
        for (size_t i = 0; i < n; i++) p[i] = pat;
        for (size_t i = 0; i < n; i++) if (p[i] != pat) return -1;
        for (size_t i = 0; i < n; i++) p[i] = (uint8_t)~pat;
        for (size_t i = 0; i < n; i++) if (p[i] != (uint8_t)~pat) return -1;
    }
    return 0;
}
```

**Complexity.** O(16 n) accesses. A healthy region returns 0. **Follow-ups.** A single pattern misses stuck-at and coupling faults, hence both polarities; address-line faults need a separate test that writes a unique value to addresses that are powers of two. Run it with caches disabled or on uncached memory, or the cache hides the cell.
:::

::: q
### Q2.33 Edit, compile and run this program from the Linux command line. It crashes; debug it.
[ARISTA · TECH-1 · ■■□ · S]{.meta}

[30-second answer: compile with `-g -Wall -Wextra -fsanitize=address,undefined`, run, and read the first report frame; if needed use `gdb` with `run`, `bt`, `frame`, `print`.]{.short}

**Approach.** (i) Read the compiler warnings: uninitialised variables, returning a local, format mismatches. (ii) Run under ASan: it names the line of an out-of-bounds or use-after-free access. (iii) In `gdb ./a.out`: `run`, then at the crash `bt` (call chain), `frame 1`, `print *node`, `info locals`; `watch x` stops when `x` changes. (iv) Fix, rebuild, and rerun. **Mistake.** Adding `printf` calls without understanding, which can hide a race or an overflow by changing layout.
:::

::: q
### Q2.34 `uint8_t a = 200, b = 100;` What does `printf("%d", a + b)` print, and why?
[CISCO · OA · ■□□ · T]{.meta}

[30-second answer: 300, because both operands are promoted to `int` before the addition, so nothing wraps.]{.short}

**Answer.** Only `uint8_t c = a + b;` would truncate to 44. Contrast `unsigned a = 1; int b = -1; b < a` which is false because `b` converts to unsigned ([2.2](#s2-2){.ref}).
:::

::: q
### Q2.35 `char *s = "abc"` versus `char s[] = "abc"`: what differs?
[ARISTA · QUALCOMM · OA · ■□□ · T]{.meta}

[30-second answer: the pointer refers to read-only characters in .rodata and has size 8; the array is a writable 4-byte copy.]{.short}

**Answer.** `sizeof` gives 8 and 4; writing `s[0]` faults in the first case. The pointer can be reassigned, the array name cannot. Figure 2.3.
:::

::: q
### Q2.36 What do `restrict` and `inline` mean?
[BROADCOM · NOKIA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: `restrict` promises that no other pointer accesses the same object during the pointer's lifetime, enabling optimisation; `inline` suggests substituting the function body at call sites.]{.short}

**Answer.** `memcpy(void *restrict, const void *restrict, size_t)` carries the promise, which is why overlap is undefined. A broken promise is undefined behaviour. `static inline` in a header avoids multiple definitions.
:::

::: q
### Q2.37 Why use `<stdint.h>` types for packet fields?
[BROADCOM · QUALCOMM · TECH-1 · ■□□ · T]{.meta}

[30-second answer: `int` and `long` change size between platforms, whereas `uint16_t` and `uint32_t` have exactly the width the protocol specifies.]{.short}

**Answer.** A TCP port is `uint16_t`, an IPv4 address `uint32_t`, a byte `uint8_t`. Print with `PRIu32` from `<inttypes.h>`. Unsigned types also give defined wrap-around for sequence numbers.
:::

::: q
### Q2.38 What is the effect of making a big local array `static`?
[QUALCOMM · TECH-1 · ■■□ · S]{.meta}

[30-second answer: the array moves from the stack to .data or .bss, which removes the stack-overflow risk and keeps its contents between calls, but the function is no longer re-entrant or thread-safe.]{.short}

**Answer.** The binary's BSS grows but its file size does not. Two callers, or two threads, share the same bytes. The alternative is `malloc`, freed by the caller.
:::

:::
:::

:::
