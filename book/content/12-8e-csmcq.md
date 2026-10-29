::: {.p12}

### Twenty-seven core-subject MCQs, with worked answers

These follow the CS-MCQ section of a typical paper ([§12.1](#s12-1){.ref}): C output, operating systems, DBMS, networks and data structures. Allow 45 seconds each. Output questions assume a 32-bit `int` and the usual two's-complement behaviour.

::: problems
::: q
[C output]{.meta}

**S1.** `printf("%d", 5/2 + 5%2*3);` prints (a) 2 (b) 5 (c) 7 (d) 8

**Answer (b).** Integer division gives 5/2 = 2; `%` and `*` bind left to right: 5%2 = 1, then 1 × 3 = 3; 2 + 3 = 5.
:::

::: q
[C output]{.meta}

**S2.** With `int a[] = {10,20,30,40}; int *p = a;`, the value of `*(p+2) + p[1]` is (a) 30 (b) 40 (c) 50 (d) 60

**Answer (c).** `*(p+2)` is `a[2]` = 30 and `p[1]` is 20; the sum is 50.
:::

::: q
[C output]{.meta}

**S3.** `unsigned char x = 255; x += 2; printf("%d", x);` prints (a) 257 (b) 1 (c) 2 (d) 0

**Answer (b).** Unsigned arithmetic wraps modulo 256: 257 mod 256 = 1.
:::

::: q
[C output]{.meta}

**S4.** `int i = 0; while (i++ < 3); printf("%d", i);` prints (a) 3 (b) 4 (c) 2 (d) infinite loop

**Answer (b).** The test uses i before incrementing; it succeeds for 0, 1, 2 and fails at 3, but the increment still occurs: i = 4.
:::

::: q
[C output]{.meta}

**S5.** `printf("%zu", sizeof("net"));` prints (a) 3 (b) 4 (c) 8 (d) undefined

**Answer (b).** The string literal has an array type of four chars including the terminating null.
:::

::: q
[C output]{.meta}

**S6.** `int x = 3; printf("%d", x << 2 | 1);` prints (a) 12 (b) 13 (c) 14 (d) 7

**Answer (b).** Shift binds tighter than OR: 3 << 2 = 12, and 12 | 1 = 13.
:::

::: q
[C output]{.meta}

**S7.** `printf("%d %d", 10/3, -10/3);` prints (C99 and later) (a) 3 -4 (b) 3 -3 (c) 4 -3 (d) 3 3

**Answer (b).** Integer division truncates toward zero, so −10/3 = −3.
:::

::: q
[C output]{.meta}

**S8.** A function has `static int s = 0; s++; printf("%d", s);` and is called three times. The output is (a) 000 (b) 111 (c) 123 (d) 321

**Answer (c).** A static local keeps its value between calls and is initialised once.
:::

::: q
[Operating systems]{.meta}

**S9.** Processes P1, P2, P3 arrive together with bursts 24, 3, 3 and run first come first served. Average waiting time? (a) 3 (b) 10 (c) 17 (d) 27

**Answer (c).** Waiting times 0, 24, 27; the average is 51/3 = 17.
:::

::: q
[Operating systems]{.meta}

**S10.** The same three processes under shortest job first. Average waiting time? (a) 3 (b) 5 (c) 10 (d) 17

**Answer (a).** Order 3, 3, 24: waiting 0, 3, 6; the average is 9/3 = 3.
:::

::: q
[Operating systems]{.meta}

**S11.** FIFO page replacement, 3 frames, references 1 2 3 4 1 2 5 1 2 3 4 5. Page faults? (a) 7 (b) 9 (c) 10 (d) 12

**Answer (b).** Faults on 1, 2, 3, 4, 1, 2, 5; then 1 and 2 hit; 3 and 4 fault; the final 5 hits. Total 9.
:::

::: q
[Operating systems]{.meta}

**S12.** The same references with 4 frames under FIFO. Page faults? (a) 8 (b) 9 (c) 10 (d) 6

**Answer (c).** Ten faults: more frames gave more faults, which is Belady's anomaly.
:::

::: q
[Operating systems]{.meta}

**S13.** The same references, 3 frames, LRU. Page faults? (a) 7 (b) 9 (c) 10 (d) 11

**Answer (c).** Simulation gives 10; LRU is a stack algorithm and so cannot show Belady's anomaly.
:::

::: q
[Operating systems]{.meta}

**S14.** Which is NOT a necessary condition for deadlock? (a) Mutual exclusion (b) Hold and wait (c) Pre-emption of resources (d) Circular wait

**Answer (c).** Deadlock needs the absence of pre-emption (no pre-emption), not its presence.
:::

::: q
[Operating systems]{.meta}

**S15.** A 32-bit address space with 4 KB pages. How many bits are the page offset? (a) 10 (b) 12 (c) 20 (d) 22

**Answer (b).** 4 KB = 2<sup>12</sup>, so 12 offset bits and 20 page-number bits.
:::

::: q
[DBMS]{.meta}

**S16.** R(A, B, C, D) with A → B, B → C, C → D and key A. The highest normal form? (a) 1NF (b) 2NF (c) 3NF (d) BCNF

**Answer (b).** The key is a single attribute so there is no partial dependency (2NF), but B → C and C → D are transitive, so 3NF fails.
:::

::: q
[DBMS]{.meta}

**S17.** Column x holds 1, NULL, 3, 3. What does `COUNT(x)` return? (a) 2 (b) 3 (c) 4 (d) 1

**Answer (b).** `COUNT(x)` skips nulls: 3 (`COUNT(*)` is 4 and `COUNT(DISTINCT x)` is 2).
:::

::: q
[DBMS]{.meta}

**S18.** A 4-row table cross-joined with a 5-row table gives how many rows? (a) 9 (b) 20 (c) 5 (d) 4

**Answer (b).** 4 × 5 = 20.
:::

::: q
[DBMS]{.meta}

**S19.** Which isolation level prevents dirty reads but allows non-repeatable reads? (a) Read uncommitted (b) Read committed (c) Repeatable read (d) Serializable

**Answer (b).** Read committed forbids dirty reads only.
:::

::: q
[Networks]{.meta}

**S20.** Usable host addresses in a /27? (a) 30 (b) 32 (c) 62 (d) 14

**Answer (a).** 2<sup>5</sup> − 2 = 30.
:::

::: q
[Networks]{.meta}

**S21.** The network address of 172.16.45.200/20? (a) 172.16.32.0 (b) 172.16.40.0 (c) 172.16.45.0 (d) 172.16.0.0

**Answer (a).** Block size 16 in the third octet; 45 lies in 32 to 47.
:::

::: q
[Networks]{.meta}

**S22.** DNS queries normally use which transport and port? (a) TCP 53 (b) UDP 53 (c) UDP 67 (d) TCP 80

**Answer (b).** UDP port 53 (TCP 53 for large responses and zone transfers).
:::

::: q
[Networks]{.meta}

**S23.** With an MTU of 1,500 and 20-byte IP and 20-byte TCP headers, the MSS is (a) 1,500 (b) 1,480 (c) 1,460 (d) 1,440

**Answer (c).** 1,500 − 20 − 20 = 1,460.
:::

::: q
[Networks]{.meta}

**S24.** Which layer does a router operate at? (a) Data link (b) Network (c) Transport (d) Session

**Answer (b).** Layer 3, the network layer.
:::

::: q
[Data structures]{.meta}

**S25.** Time to search a sorted array of *n* elements by binary search? (a) O(*n*) (b) O(log *n*) (c) O(*n* log *n*) (d) O(1)

**Answer (b).** The range halves at each step.
:::

::: q
[Data structures]{.meta}

**S26.** Push 1, push 2, push 3, pop, push 4, pop, pop. The popped values in order? (a) 3 4 2 (b) 3 2 1 (c) 3 4 1 (d) 1 2 3

**Answer (a).** Pops return 3, then 4, then 2.
:::

::: q
[Data structures]{.meta}

**S27.** The in-order traversal of a binary search tree visits keys in (a) Descending order (b) Ascending order (c) Level order (d) Insertion order

**Answer (b).** Left, node, right gives ascending order.
:::

:::
:::
