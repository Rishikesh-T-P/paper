::: {.p2}

::: pack
## Revision Spread {#rv2}

::: revision
::: top
**Ten facts.** (1) Sections: text, rodata, data, BSS, heap, stack; a `static` local is in data or BSS. (2) `p + n` moves `n * sizeof(*p)` bytes; an array parameter is a pointer. (3) `const` binds to what is on its left: `const int *p` protects the pointee, `int *const p` the pointer. (4) Padding: each member at a multiple of its alignment; size rounded to the largest alignment; reorder by decreasing size. (5) Network order is big-endian; `0x0A0B0C0D` is `0D 0C 0B 0A` in little-endian memory. (6) `volatile` is not atomic; signed overflow, null dereference, unsequenced writes and shifts by the width are undefined. (7) Macros: parenthesise everything, never pass side effects, wrap statements in `do { } while (0)`. (8) `realloc` through a temporary; `free` then `NULL`; ASan for memory errors, UBSan for undefined behaviour, valgrind for leaks. (9) Parse packets by offset with length checks first; never cast a byte buffer to a structure. (10) Python names are references, defaults are evaluated once, generators are lazy; C++ releases resources in destructors, and a polymorphic base needs a virtual destructor.

**Three figures to redraw.** The process layout ([Figure 2.1](#s2-1){.ref}), the padding byte map ([Figure 2.4](#s2-7){.ref}) and the byte-order diagram ([Figure 2.5](#s2-9){.ref}).
:::

### Sizes of the basic types, in bytes

| Type | ILP32 | LP64 (Linux) | LLP64 (Win64) |
|---|---|---|---|
| `char` | 1 | 1 | 1 |
| `short` | 2 | 2 | 2 |
| `int` | 4 | 4 | 4 |
| `long` | 4 | 8 | 4 |
| `long long` | 8 | 8 | 8 |
| pointer, `size_t` | 4 | 8 | 8 |
| `float`, `double` | 4, 8 | 4, 8 | 4, 8 |

Alignment equals size for scalars on LP64. `uint8_t`..`uint64_t` are exact on all three.

### Operator precedence, high to low

| Level | Operators | Assoc. |
|---|---|---|
| 1 | `()` `[]` `.` `->` `x++` `x--` | L to R |
| 2 | `!` `~` `++x` `--x` unary `+ -` `*p` `&x` `sizeof` cast | R to L |
| 3 | `*` `/` `%` | L to R |
| 4 | `+` `-` | L to R |
| 5 | `<<` `>>` | L to R |
| 6 | `<` `<=` `>` `>=` | L to R |
| 7 | `==` `!=` | L to R |
| 8 to 10 | `&` then `^` then `\|` | L to R |
| 11, 12 | `&&` then `\|\|` | L to R |
| 13 | `?:` | R to L |
| 14 | `=` `+=` `<<=` ... | R to L |
| 15 | `,` | L to R |

Infamous: `*p++` is `*(p++)`; `x & 1 == 0` is `x & (1 == 0)`; `a << 1 + 2` is `a << 3`; `a + b << c` is `(a + b) << c`.

### Format specifiers

| Spec | Type |
|---|---|
| `%d` `%i` | `int` |
| `%u` `%x` `%o` | `unsigned` (decimal, hex, octal) |
| `%ld` `%lu` | `long`, `unsigned long` |
| `%lld` `%llu` | `long long` |
| `%zu` `%zd` | `size_t`, `ssize_t` |
| `%c` `%s` | `char`, string |
| `%f` `%e` `%g` | `double` |
| `%p` | `void *` |
| `%02x` `%5.2f` `%-8s` `%*d` | zero-pad, width.precision, left-align, width from argument |
| `PRIu32` `PRId64` | `<inttypes.h>` for `uint32_t`, `int64_t` |

A mismatch is undefined; `uint8_t` promotes to `int`, so `%d` is correct for it.

### Storage classes

| Declaration | Scope | Lifetime | Linkage | Default |
|---|---|---|---|---|
| local (`auto`) | block | block | none | indeterminate |
| `static` local | block | program | none | 0 |
| global | file and others | program | external | 0 |
| `static` global or function | file | program | internal | 0 |
| `extern` | declares, no storage | n/a | external | n/a |
| `malloc` block | by pointer | until `free` | n/a | indeterminate |

### Qualifiers

| Qualifier | Promise or effect | Does not mean |
|---|---|---|
| `const` | no writes through this name | not stored in ROM unless global |
| `volatile` | every access really happens, in order | not atomic, not a barrier |
| `restrict` | no other pointer to the same object | checked by the compiler |
| `_Atomic` | indivisible access, ordering | free of locks |
| `inline` | body may be substituted | guaranteed inlining |
| `register` | historical hint; address not allowed | faster today |

### Padding rule, endianness, macros

Offset of a member is the next multiple of its alignment; `sizeof` is a multiple of the largest alignment. `{char; int; char}` is 12; `{int; char; char}` is 8; `{char a[3]; short; int}` is 12. `packed` removes padding at the price of misaligned access. `htons` and `htonl` convert host to network order and are no-ops on big-endian machines. Safe macro: `#define MAX(a,b) ((a)>(b)?(a):(b))` still evaluates an argument twice.

### Memory bug to tool

| Symptom | Tool |
|---|---|
| leak | `valgrind --leak-check=full`, LeakSanitizer |
| overflow, use after free | `-fsanitize=address` |
| undefined behaviour | `-fsanitize=undefined` |
| crash, wrong value | `gdb`: `run`, `bt`, `print`, `watch` |
| warnings | `-Wall -Wextra -Werror` |

### STL: which container?

Use `vector` unless you can say why not. Need sorted order or range queries: `map` or `set` (O(log n)). Need fastest lookup and no order: `unordered_map` (O(1) average). Need stable iterators and cheap insertion in the middle: `list`. Need both ends: `deque`. Need the largest element repeatedly: `priority_queue`. Complexity table: [2.21](#s2-21){.ref}.

### Python quick reference

`struct` formats: `!` network order, `<` little, `B` 1 byte, `H` 2, `I` 4, `Q` 8, `Ns` N bytes; native alignment only without a prefix. `list`: append O(1) amortised, `insert(0, x)` O(n), `x in` O(n). `set` and `dict`: O(1) on average, keys hashable. `Counter.most_common(k)`, `defaultdict(list)`, `deque` for queues, `heapq.nlargest`. `subprocess.run([...], check=True, capture_output=True, text=True, timeout=t)`; never `shell=True` with data. `//` floors, `%` takes the divisor's sign.

### Flashcards

::: flash
| Question | Answer |
|---|---|
| `sizeof(struct{char; int; short;})` on x86-64? | 12 |
| `sizeof` of `{short; long; char;}` on LP64 and ILP32? | 24 and 12 |
| Size of `union { int i; char c[5]; }`? | 8 |
| `const int *p`: what is constant? | the pointee |
| `int *const p`: what is constant? | the pointer |
| Where does a static local live? | data or BSS |
| Where does `"abc"` live? | rodata (read-only) |
| Why is BSS free in the file? | zero contents; only the size is stored |
| `0x0A0B0C0D` in little-endian memory? | `0D 0C 0B 0A` |
| Network byte order? | big-endian |
| Is `volatile` atomic? | no |
| Can a variable be `const volatile`? | yes: read-only hardware register |
| `sizeof(a)` for an array parameter? | pointer size, 8 on LP64 |
| `strlen("abc")` and `sizeof("abc")`? | 3 and 4 |
| Result of `-1 < 1u`? | false |
| `uint8_t` 200 + 100? | 300 (promoted to `int`) |
| `char c = 200` prints? | -56 where `char` is signed |
| `SQ(2+3)` with `x*x`? | 11 |
| Why `do { } while (0)` in macros? | one statement, safe after `if` |
| `STR(N)` versus `XSTR(N)`? | name versus expanded value |
| Signed overflow? | undefined |
| Unsigned overflow? | defined, wraps modulo 2^n |
| `1 << 31` on `int`? | undefined |
| `i = i++ + ++i;`? | undefined |
| `memcpy` versus `memmove`? | `memmove` handles overlap |
| Safe `realloc` pattern? | assign to a temporary first |
| `strncpy` guarantee? | none: may not terminate |
| `free` twice? | undefined; glibc aborts |
| Static array in a function: effect? | off the stack; not re-entrant |
| Offset of the header version nibble? | byte 0, high four bits |
| Valid IPv4 header checksum sum? | `0xFFFF` (zero after complement) |
| Fix for `for (unsigned i = n; i >= 0; i--)`? | `for (unsigned i = n; i-- > 0; )` |
| What does `container_of` compute? | enclosing struct from member pointer |
| `*p++` means? | `*(p++)`: read, then advance |
| Python default `acc=[]`: problem? | one list shared by all calls |
| `x in list` versus `x in set`? | O(n) versus O(1) average |
| `!` in a `struct` format? | network (big-endian) order |
| Why `subprocess` with a list? | no shell parsing, no injection |
| C++ vptr: how many per object? | one, pointing to the class vtable |
| Why virtual destructor? | `delete` via base runs derived destructor |
| `map` versus `unordered_map`? | O(log n) ordered versus O(1) average |
| Smart pointer for sole ownership? | `unique_ptr` |
| Break a `shared_ptr` cycle with? | `weak_ptr` |
:::
:::
:::

:::
