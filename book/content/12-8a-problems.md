::: {.p12}
::: pack
## Problem Set {#ps12}

::: problems
::: q
### Q12.1 A sum doubles in 8 years at simple interest. In how many years does it triple?
[ALL · OA · ■□□ · T]{.meta}

[30-second answer: 16 years.]{.short}

**Fast method.** Doubling means the interest equals the principal after 8 years, so each 8 years adds one principal; tripling needs interest of two principals, which is 16 years. **Conventional.** Rate = 100/8 = 12.5% per annum; for tripling, 200 = 12.5 × *T*, so *T* = 16. **Mistake.** Answering 12 by adding half as much again.
:::

::: q
### Q12.2 Find the unit digit of 7<sup>95</sup>.
[ALL · OA · ■□□ · T]{.meta}

[30-second answer: 3.]{.short}

**Approach.** The unit digits of powers of 7 cycle as 7, 9, 3, 1 with length 4. 95 = 4 × 23 + 3, so take the third entry: 3. **Mistake.** Reading remainder 0 as "first entry" instead of the last. See [§12.2](#s12-2){.ref}.
:::

::: q
### Q12.3 A can finish a job in 12 days and B in 18. How long together?
[ALL · OA · ■□□ · T]{.meta}

[30-second answer: 7.2 days (7 days 4.8 hours).]{.short}

**Fast method.** Take 36 units; A does 3 and B does 2 per day; together 5, so 36/5 = 7.2. **Conventional.** 1/12 + 1/18 = 5/36 of the job per day, so 36/5 days. **Check.** 12 × 18/(12 + 18) = 216/30 = 7.2.
:::

::: q
### Q12.4 Trains of 150 m and 100 m run at 54 and 36 km/h in opposite directions. Crossing time?
[ALL · OA · ■■□ · T]{.meta}

[30-second answer: 10 seconds.]{.short}

**Approach.** Opposite directions: speeds add, 54 + 36 = 90 km/h = 90 × 5/18 = 25 m/s. Distance is the sum of the lengths, 250 m. Time = 250/25 = 10 s. **Mistake.** Subtracting the speeds, which is for the same direction (it would give 250/5 = 50 s).
:::

::: q
### Q12.5 In how many ways can the letters of NETWORK be arranged so that the vowels are together?
[ALL · OA · ■■□ · T]{.meta}

[30-second answer: 1,440.]{.short}

**Approach.** The vowels E and O are glued into one block, giving 6 objects (N, T, W, R, K and the block): 6! = 720 arrangements. The block can be EO or OE: × 2. All letters are distinct, so no division is needed: 720 × 2 = 1,440. **Mistake.** Forgetting the internal order of the block.
:::

::: q
### Q12.6 Two cards are drawn without replacement. Probability that both are aces?
[ALL · OA · ■■□ · T]{.meta}

[30-second answer: 1/221.]{.short}

**Approach.** (4/52) × (3/51) = 12/2,652 = 1/221. **Check.** C(4, 2)/C(52, 2) = 6/1,326 = 1/221. **Mistake.** Using 4/52 twice, which assumes replacement.
:::

::: q
### Q12.7 All routers are devices; some devices are switches. Does "Some routers are switches" follow?
[ALL · OA · ■■□ · T]{.meta}

[30-second answer: No.]{.short}

**Approach.** Draw routers inside devices. The switches overlap devices, but nothing forces the overlap to fall inside routers; a legal drawing puts every switch in the part of devices outside routers, so the conclusion fails in that drawing. A conclusion must hold in every drawing ([Figure 12.4](#s12-6){.ref}). **Mistake.** Treating "some" as transferable through "all".
:::

::: q
### Q12.8 Round robin, quantum 2: P1 (arrives 0, burst 5), P2 (1, 3), P3 (2, 1), P4 (3, 2). Average waiting time?
[CISCO · QUALCOMM · OA · ■■□ · T]{.meta}

[30-second answer: 4.5 time units.]{.short}

**Approach.** New arrivals join the queue before the pre-empted process does. Order of execution (Gantt chart): P1 0 to 2, P2 2 to 4, P3 4 to 5, P1 5 to 7, P4 7 to 9, P2 9 to 10, P1 10 to 11.

| Process | Completion | Turnaround (completion − arrival) | Waiting (turnaround − burst) |
|---|---|---|---|
| P1 | 11 | 11 | 6 |
| P2 | 10 | 9 | 6 |
| P3 | 5 | 3 | 2 |
| P4 | 9 | 6 | 4 |

**Answer.** (6 + 6 + 2 + 4)/4 = 4.5. **Mistake.** Queueing the pre-empted process before the new arrival, which gives a different order; state the convention. See [§7.4](#s7-4){.ref}.
:::

::: q
### Q12.9 What does `int i = 5; printf("%d %d", i++, ++i);` print?
[CISCO · QUALCOMM · OA · ■■□ · T]{.meta}

[30-second answer: undefined behaviour; no single output is correct.]{.short}

**Answer.** Two modifications of `i` occur with no sequence point between them, and the order of evaluating function arguments is unspecified. We tested two compilers: GCC printed `6 7` and Clang printed `5 7`. **What to choose in an OA.** If "undefined" or "compiler dependent" is an option, choose it. If not, choose the output the setter's own compiler most plausibly produced, and note the doubt. **Mistake.** Giving "5 7" as if it were guaranteed. See [§2.12](#s2-12){.ref}.
:::

::: q
### Q12.10 Eight people A to H sit round a circular table facing the centre. Find the arrangement.
[CISCO · NOKIA · OA · ■■■ · T]{.meta}

[30-second answer: clockwise from A: A, H, B, C, E, G, D, F.]{.short}

**Clues.** (1) A sits opposite E. (2) B is second to the left of A. (3) C sits immediately to the right of E. (4) D sits opposite B. (5) F sits next to D. (6) G does not sit next to A.

**Approach.** Facing the centre, left is clockwise. Number the seats 0 to 7 clockwise and put A at 0.

1. Clue 1: E is at 4.
2. Clue 2: B is two seats clockwise of A, so seat 2.
3. Clue 3: the right of E is anticlockwise, so C is at 3.
4. Clue 4: D is opposite B, so seat 6.
5. Remaining people F, G, H take seats 1, 5, 7. By clue 5, F is next to D (seat 6), so F is at 5 or 7; by clue 6, G is not next to A (seats 1 and 7 are), so G is at 5. Then F is at 7 and H is at 1.

**Answer.** Seats 0 to 7: A, H, B, C, E, G, D, F. **Check.** All six clues hold, and each is needed (dropping any one allows at least two arrangements).
:::

::: q
### Q12.11 Explain the four pillars of OOP with a networking example.
[CISCO · JUNIPER · TECH-1 · ■□□ · S]{.meta}

[30-second answer: encapsulation bundles data with the code that guards it (`Interface.set_mtu()` validates the value); abstraction exposes what an object does and hides how (`device.get_config()`); inheritance reuses a base class (`CiscoIOS` extends `Device`); polymorphism gives one call different behaviour by real type (looping over devices calling `get_config()`).]{.short}

**Follow-ups.** The mechanism of polymorphism (Q12.13); the difference between encapsulation and abstraction (protect versus simplify). **Mistake.** Reciting definitions without one example. Table in [§12.8](#s12-8){.ref}.
:::

::: q
### Q12.12 Overloading versus overriding.
[CISCO · QUALCOMM · TECH-1 · ■□□ · S]{.meta}

[30-second answer: overloading is several functions of one name with different parameter lists in one scope, resolved by the compiler; overriding is a derived class replacing a virtual function of the base with the same signature, resolved at run time.]{.short}

**Follow-ups.** Python has no overloading (the last definition wins; use default arguments or `singledispatch`). A non-virtual function that is redefined in a derived class is *hiding*, not overriding. **Mistake.** Saying that return type alone can distinguish overloads; it cannot.
:::

::: q
### Q12.13 How do virtual functions work internally, and what do they cost?
[QUALCOMM · ARISTA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: each class with virtual functions has a vtable of function pointers; each object holds a hidden vptr to its class's table; a virtual call loads the vptr, indexes the table and jumps. The cost is one pointer per object, one extra memory read per call and no inlining.]{.short}

**Evidence.** For `struct A { virtual void f(){} int x; };` against `struct B { int x; };`, `sizeof(A)` is 16 and `sizeof(B)` is 4 on a 64-bit machine: 8 bytes of vptr plus padding to alignment. **Follow-ups.** Why constructors cannot be virtual (vptr not yet set); why base destructors should be. See [§2.20](#s2-20){.ref}.
:::

::: q
### Q12.14 Abstract class versus interface.
[CISCO · MICROSOFT · TECH-1 · ■■□ · T]{.meta}

[30-second answer: an abstract class may hold data and implemented methods and cannot be instantiated; an interface is a pure contract with no instance state. In C++ an interface is an abstract class with only pure virtual functions (`= 0`); in Python, `abc.ABC` with `@abstractmethod`, or `typing.Protocol`.]{.short}

**Answer.** Use an abstract class when related types share code and a contract; use an interface when unrelated types share only a contract. A class can implement many interfaces but, in Java, extend one class. Table in [§12.8](#s12-8){.ref}.
:::

::: q
### Q12.15 Shallow versus deep copy; the rule of three and five.
[ARISTA · BROADCOM · TECH-1 · ■■□ · T]{.meta}

[30-second answer: a shallow copy copies the pointer so two objects share one block, and the second destructor frees it again (double free); a deep copy allocates a new block. Rule of three: if a class needs a destructor, copy constructor or copy assignment, it needs all three; rule of five adds move constructor and move assignment.]{.short}

```cpp
Buf(const Buf &o) : n(o.n) { p = new char[n]; memcpy(p, o.p, n); }   // deep copy
Buf &operator=(const Buf &o) {
    if (this != &o) { char *q = new char[o.n]; memcpy(q, o.p, o.n);
                      delete[] p; p = q; n = o.n; }
    return *this;
}
```

**Mistake.** Self-assignment: freeing `p` before copying from it. Smart pointers and `std::string` remove the need for the three. See [§2.19](#s2-19){.ref}.
:::

::: q
### Q12.16 Explain SOLID with one example per letter.
[MICROSOFT · AMAZON · TECH-1 · ■■□ · T]{.meta}

[30-second answer: S, a class has one reason to change (split `Router` from `ConfigParser`). O, extend by adding classes, not editing chains (new vendor, new subclass). L, a subclass works wherever its base does (no `ReadOnlyDevice` that throws in `set_config`). I, small interfaces (`Routing`, `Switching`). D, depend on abstractions (the monitor takes a `Device`).]{.short}

**Follow-up.** Which letter does an `if vendor == ...` chain break (O)? Table with violation and repair in [§12.8](#s12-8){.ref}.
:::

::: q
### Q12.17 Implement a thread-safe Singleton in C++. Why might you avoid it?
[MICROSOFT · ARISTA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: use a function-local static, which C++11 guarantees is initialised exactly once even with several threads; delete copying. Avoid Singletons because they are hidden global state, which makes unit tests order-dependent and hard to isolate.]{.short}

```cpp
class Logger {
public:
    static Logger& get() { static Logger inst; return inst; }
    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;
    void log(const char* m);
private:
    Logger() = default;
};
```

**Follow-ups.** Python: a module-level object is already a singleton. Alternative: pass the logger in (dependency inversion). **Mistake.** Double-checked locking written by hand, which is easy to get wrong.
:::

::: q
### Q12.18 Design classes for a routing table with add, delete and longest-prefix lookup.
[ARISTA · JUNIPER · CISCO · TECH-2 · ■■■ · T]{.meta}

[30-second answer: one `RoutingTable` class holding a dictionary per prefix length; lookup tries lengths from 32 down to 0 and returns the first match, so it costs at most 33 hash probes. For millions of routes use a trie ([§1.9](#s1-9){.ref}).]{.short}

```python
import ipaddress

class RoutingTable:
    def __init__(self):
        self.by_len = {}                      # prefix length -> {network: next hop}
    def add(self, prefix, next_hop):
        net = ipaddress.ip_network(prefix)
        self.by_len.setdefault(net.prefixlen, {})[net] = next_hop
    def delete(self, prefix):
        net = ipaddress.ip_network(prefix)
        self.by_len.get(net.prefixlen, {}).pop(net, None)
    def lookup(self, ip):
        a = int(ipaddress.ip_address(ip))
        for plen in sorted(self.by_len, reverse=True):          # longest first
            net = ipaddress.ip_network(((a >> (32 - plen)) << (32 - plen), plen))
            if net in self.by_len[plen]:
                return self.by_len[plen][net]
        return None
```

With 0.0.0.0/0 to `isp`, 10.0.0.0/8 to `core` and 10.1.0.0/16 to `b1`, the lookups of 10.1.2.3, 10.9.9.9 and 8.8.8.8 return `b1`, `core`, `isp`; after deleting the /16, 10.1.2.3 returns `core`. **Complexity.** Add and delete O(1); lookup O(33). **Design note.** `Route` could be its own class for attributes (metric, source); composition ("table has routes") is preferred to inheriting from `dict`.
:::
:::
:::
:::
