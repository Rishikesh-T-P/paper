::: {.p2}

## [2.15]{.sec}The gotcha gallery: 36 output traps [Must · ■■□]{.tag} {#s2-15}

Output-prediction questions are a fixed ritual in online assessments at Cisco and Juniper and in Qualcomm and Arista interviews: a snippet of three to eight lines, and the question "what does this print?". The skill is to classify the snippet first as *defined*, *implementation-defined* or *undefined*, and to compute an output only in the first two cases. This section is the single home of the book's C traps. Each entry gives the code, the output on 64-bit Linux with gcc (so `int` is 4 bytes and `char` is signed), and the reason. Entries marked UB print nothing definite; any output seen is an accident.

::: trap
*Claim:* when a snippet compiles and runs, whatever it prints is "the answer". *Why it is wrong:* a program with undefined behaviour has no correct output, and the same source may print different results at `-O0` and `-O2`, or on the next compiler release. *Correct statement:* in an interview, say "undefined behaviour" and name the rule; computing a number from an unsequenced expression is the failure the question is designed to find.
:::

### Expressions and sequencing

**T1. Two writes to one variable.**
```c
int i = 1;
i = i++ + ++i;
```
*Answer:* undefined. `i` is modified twice with no sequence point between the modifications.

**T2. `sizeof` does not evaluate.**
```c
int i = 5;
printf("%zu %d\n", sizeof(i++), i);
```
*Answer:* `4 5`. The operand of `sizeof` is not evaluated (except for variable-length arrays), so `i` is unchanged.

**T3. `printf` returns a count.**
```c
printf("%d\n", printf("hello"));
```
*Answer:* `hello5` followed by a newline. The inner call prints five characters and returns 5, which the outer call then prints.

**T4. Signed meets unsigned.**
```c
puts(-1 < 1u ? "true" : "false");
```
*Answer:* `false`. The usual arithmetic conversions turn `-1` into `UINT_MAX`, which is larger than 1 ([2.2](#s2-2){.ref}).

**T5. Plain `char` above 127.**
```c
char c = 200;
printf("%d\n", c);
```
*Answer:* `-56` on x86-64, where `char` is signed (implementation-defined). On ARM Linux, where `char` is unsigned, it prints 200.

**T6. Array parameter.**
```c
void f(int a[10]) { printf("%zu\n", sizeof(a)); }
int main(void) { int a[10]; f(a); printf("%zu\n", sizeof a); }
```
*Answer:* `8` then `40`. Inside `f` the parameter is a pointer (8 bytes on LP64); in `main` the array has 10 elements of 4 bytes.

**T7. Macro without parentheses.**
```c
#define SQ(x) x*x
printf("%d %d\n", SQ(2+3), 10/SQ(2));
```
*Answer:* `11 10`. The first expands to `2+3*2+3`; the second to `10/2*2`, which evaluates left to right as `(10/2)*2`.

**T8. Fall-through.**
```c
int x = 2;
switch (x) { case 1: putchar('a');
             case 2: putchar('b');
             case 3: putchar('c'); break;
             default: putchar('d'); }
```
*Answer:* `bc`. Execution enters at `case 2` and continues into `case 3` until `break`.

**T9. Comma operator.**
```c
int x = (1, 2, 3);
printf("%d\n", x);
```
*Answer:* `3`. The comma operator evaluates its operands left to right and yields the last. Without the parentheses, `int x = 1, 2;` is a compile error, since `2` would be read as a second declarator.

**T10. Short-circuit evaluation.**
```c
int a = 0, b = 5;
if (a && b++) { }
printf("%d %d\n", a, b);
```
*Answer:* `0 5`. Because `a` is false, the right operand of `&&` is never evaluated. The same applies to `||` when the left side is true.

**T11. A static local keeps its value.**
```c
int cnt(void) { static int c; return ++c; }
for (int i = 0; i < 3; i++) printf("%d ", cnt());
```
*Answer:* `1 2 3`. The static `c` is zero-initialised once, before `main`, and survives between calls. Printing three calls in a single `printf` would be unspecified, because the order of evaluating arguments is unspecified.

### Pointers and declarations

**T12. Increment and dereference.**
```c
int a[] = {10, 20, 30}, *p = a;
int x = *p++;        /* post-increment the pointer, read the old target */
int y = (*p)++;      /* increment the value that p points to           */
int z = ++*p;        /* pre-increment the value                        */
printf("%d %d %d %d %ld\n", x, y, z, a[1], (long)(p - a));
```
*Answer:* `10 20 22 22 1`. Postfix `++` binds tighter than `*`, so `*p++` is `*(p++)`: the pointer moves, the old element is read. In `(*p)++` and `++*p` the value changes and the pointer does not.

**T13. Array address versus element address.**
```c
int a[5];
printf("%ld %ld\n", (long)((char *)(a + 1) - (char *)a),
                    (long)((char *)(&a + 1) - (char *)a));
```
*Answer:* `4 20`. `a + 1` steps over one `int`; `&a` has type `int (*)[5]`, so `&a + 1` steps over the whole array.

**T14. Where `const` binds.**
```c
int x = 1, y = 2;
const int *p = &x;   *p = 3;     /* line A */
p = &y;                          /* line B */
int *const q = &x;   q = &y;     /* line C */
```
*Answer:* line A is a compile error (`assignment of read-only location '*p'`), line B is accepted, and the assignment in line C is a compile error (`assignment of read-only variable 'q'`). `const int *` protects the pointee; `int *const` protects the pointer ([2.5](#s2-5){.ref}).

**T15. Writing to a literal.**
```c
char *p = "arista";  p[0] = 'A';
char  q[] = "arista"; q[0] = 'A';
```
*Answer:* the first write is undefined and normally ends in a segmentation fault, because the literal lives in .rodata. The second is defined: `q` is a writable copy.

**T16. Pointer to a dead local.**
```c
char *name(void) { char buf[8] = "eth0"; return buf; }
printf("%s\n", name());
```
*Answer:* undefined. `buf` ceases to exist when `name` returns. The compiler warns (`returns address of local variable`), and the output may look right, garbage, or crash.

**T17. Postfix decrement in recursion.**
```c
int sum(int n) { return n == 0 ? 0 : n + sum(n--); }
printf("%d\n", sum(3));
```
*Answer:* the program overflows the stack and ends with a segmentation fault. `n--` passes the *old* value, so the argument never decreases and the recursion never reaches 0. The fix is `sum(n - 1)`.

**T18. Padding.**
```c
struct A { char c; int i; char d; };
struct B { int i; char c; char d; };
printf("%zu %zu\n", sizeof(struct A), sizeof(struct B));
```
*Answer:* `12 8`. See Figure 2.4 on [padding](#s2-7){.ref}: three padding bytes after `c` and three after `d` in `A`, two at the end of `B`.

**T19. Union overlay.**
```c
union { int i; char c[4]; } u = { 1 };
printf("%zu %d\n", sizeof u, u.c[0]);
```
*Answer:* `4 1` on a little-endian machine, since the least significant byte of 1 is stored first. On a big-endian machine the second number is 0.

**T20. A flag polled in a loop.** Read the assembly in Lab 2.2 of [2.6](#s2-6){.ref}: without `volatile`, `while (!flag);` is compiled to read `flag` once. This is a question about the optimiser, not about the printed value.

### Numbers

**T21. Overflow, signed and unsigned.**
```c
printf("%u\n", UINT_MAX + 1u);
int m = INT_MAX;  m = m + 1;
```
*Answer:* the first line prints `0`, because unsigned arithmetic wraps modulo 2^32 (defined). The second is undefined; the UBSan message appears in Lab 2.4 of [2.12](#s2-12){.ref}.

**T22. Floating-point equality.**
```c
printf("%d\n", 0.1 + 0.2 == 0.3);
float f = 0.1;  printf("%d\n", f == 0.1);
```
*Answer:* `0` and `0`. The decimal fractions are not exactly representable in binary, and the sum differs from `0.3` in the last bit. In the second case `f` holds the nearest `float`, which differs from the nearest `double` that `0.1` denotes. Compare floating-point values with a tolerance.

**T23. Type of a character constant.**
```c
printf("%d %zu\n", 'A', sizeof('A'));
```
*Answer:* `65 4`. A character constant has type `int` in C; in C++ it has type `char` and the size is 1.

**T24. Shifts.**
```c
printf("%d\n", -8 >> 1);
int a = 1 << 31;   unsigned b = 1u << 32;
```
*Answer:* the first prints `-4`: right-shifting a negative value is implementation-defined, and gcc shifts arithmetically. `1 << 31` shifts into the sign bit of an `int` and is undefined; `1u << 32` shifts by the full width and is undefined.

**T25. `strlen` versus `sizeof`.**
```c
char s[] = "abc";
printf("%zu %zu\n", strlen(s), sizeof s);
```
*Answer:* `3 4`. `strlen` stops before the terminator; the array includes it.

**T26. Uninitialised local.**
```c
int n;
printf("%d\n", n);
```
*Answer:* undefined for an automatic variable (an indeterminate value). Had `n` been `static` or global, it would be 0. Compilers warn with `-Wall -O2`.

**T27. Double free.**
```c
char *p = malloc(8);  free(p);  free(p);
```
*Answer:* undefined. With glibc 2.39 the program aborts with `free(): double free detected in tcache 2`. Use after free and a missing `free` are the two related defects ([2.10](#s2-10){.ref}).

**T28. A countdown that never ends.**
```c
for (unsigned i = 3; i >= 0; i--) printf("%u ", i);
```
*Answer:* the loop prints `3 2 1 0 4294967295 4294967294 ...` without end, because an unsigned value is always `>= 0` and `0 - 1` wraps. Use `for (unsigned i = n; i-- > 0; )`.

**T29. Leading zero.**
```c
printf("%d %d\n", 010, 010 + 1);
```
*Answer:* `8 9`. A leading `0` makes an octal constant, and `08` would not compile.

**T30. Types in the conditional operator.**
```c
puts((1 ? -1 : 0u) > 0 ? "pos" : "neg");
```
*Answer:* `pos`. The two branches are converted to a common type, which is `unsigned int`, so `-1` becomes `UINT_MAX` even though the first branch is chosen.

**T31. A mismatched format specifier.**
```c
printf("%d\n", 3.5);          printf("%s\n", 5);
```
*Answer:* undefined. `printf` reads its arguments according to the format, not according to what was passed. The compiler warns with `-Wformat`, which is part of `-Wall`.

**T32. Division and remainder of negative numbers.**
```c
printf("%d %d\n", -7 / 2, -7 % 2);
```
*Answer:* `-3 -1`. Since C99 division truncates towards zero, and the remainder takes the sign of the dividend, so that `(a / b) * b + a % b == a`.

**T33. Assignment in a condition.**
```c
int x = 0;
if (x = 5) puts("yes");
printf("%d\n", x);
```
*Answer:* `yes` and then `5`. The expression `x = 5` assigns and has the value 5, which is true. The compiler suggests parentheses with `-Wall`.

**T34. Precedence of `==` over `&`.**
```c
int x = 4;
printf("%d\n", x & 1 == 0);
```
*Answer:* `0`. The comparison binds tighter than `&`, so the expression is `x & (1 == 0)`, which is `4 & 0`. The intended test is `(x & 1) == 0`; the precedence table is in the [Revision Spread](#rv2){.ref}.

**T35. Partial initialisation, and `i[a]`.**
```c
int a[5] = {1};
for (int i = 0; i < 5; i++) printf("%d ", a[i]);
int b[] = {10, 20, 30};   printf("%d\n", 2[b]);
```
*Answer:* `1 0 0 0 0 ` followed by `30`. Members without an initialiser are zeroed, and `2[b]` is `*(2 + b)`, the same as `b[2]`.

**T36. Where does each variable live?** The classification of globals, statics, locals, literals and `malloc` blocks is the table in [2.1](#s2-1){.ref}, with the effect of `static` on a large local array in the trap that follows it.

::: lens
[CISCO · JUNIPER · QUALCOMM · ARISTA]{.co}

A set of ten to fifteen of these, usually T1, T2, T7, T10 to T19, T25 and T28, makes up the C section of many online assessments. Qualcomm adds `const` placement, structure against union, padding, `volatile` and `static` (T11, T14 to T20); Arista adds the debugging variants, namely uninitialised variables (T26), returning a local (T16), `n--` in recursion (T17) and writing to a literal (T15). A strong answer names the category first and then the mechanism. If the output is undefined, one gives the rule that is broken and the tool that detects it (UBSan, ASan or a compiler warning).
:::

::: lab
`LAB 2.5 · 20 MIN`

Type the six snippets T2, T4, T12, T13, T18 and T25 into one file, predict each result on paper, then run:

```bash
gcc -Wall -Wextra -O0 -o gal gal.c && ./gal
```

Repeat with `-O2`. The defined traps print identical output at both levels; add T1 and T26 and observe the compiler warnings and, possibly, different output.

**What you should notice:** warnings from `-Wall -Wextra` already flag several entries (T1, T16, T26, T31, T33), and T14 is rejected outright, so reading them is the cheapest debugging step.
:::

::: check
1. Which entries of this section rely on implementation-defined behaviour rather than undefined behaviour? [^c2-26]
2. Why is T11 safe with a loop but not with three calls in one `printf`? [^c2-27]
:::

[^c2-26]: T5 (signedness of `char`) and T24 (right shift of a negative value); the others print a definite value or are undefined.
[^c2-27]: The loop sequences the calls statement by statement, whereas the order of evaluating the arguments of one call is unspecified.

:::
