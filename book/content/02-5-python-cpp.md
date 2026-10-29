::: {.p2}

## [2.16]{.sec}Python: the data model [Should · ■□□]{.tag} {#s2-16}

This part treats the Python language only. The libraries for networks and devices are in [Pillar 10](#ch10){.ref}, sockets in [Pillar 7](#ch7){.ref}, and shell pipelines in [Pillar 8](#ch8){.ref}. Examples assume Python 3.10 or later.

In Python every value is an object, and a variable is a *name* bound to an object, not a box that holds a value. Assignment `b = a` therefore binds a second name to the same object. Objects are either *mutable* (list, dict, set, bytearray) or *immutable* (int, float, str, bytes, tuple), and the difference explains most interview traps.

::: bigidea
Names refer to objects; assignment copies the reference, never the object, so a change made through one name is visible through every name bound to the same mutable object.
:::

```python
a = [1, 2]; b = a; c = a[:]            # b is an alias; c is a shallow copy
b.append(3)
print(a, c, a is b, a == c, a is c)    # [1, 2, 3] [1, 2] True False False
grid = [[0] * 2] * 2; grid[0][0] = 9
print(grid)                            # [[9, 0], [9, 0]]: both rows are one list
t = (1, [2]); t[1].append(3); print(t) # (1, [2, 3]): the tuple holds the same list
```

The operator `==` compares values and `is` compares identity. Use `is` only for `None` (`if x is None`), because the identity of small integers and strings is an implementation detail. A *shallow copy* (`a[:]`, `list(a)`, `a.copy()`) copies the outer container but shares the elements; `copy.deepcopy` copies recursively.

The two most reported Python traps are both consequences of the model. A default argument is evaluated once, when the function is defined, so a mutable default is shared by all calls. Removing items from a list while iterating over it skips elements, because the iterator tracks a position, not the items.

```python
def bad(x, acc=[]):                    # one list, created at definition time
    acc.append(x); return acc
print(bad(1), bad(2))                  # [1, 2] [1, 2]  (the same list twice)
def good(x, acc=None):
    if acc is None: acc = []
    acc.append(x); return acc
print(good(1), good(2))                # [1] [2]

nums = [1, 2, 2, 3]
for n in nums:
    if n == 2: nums.remove(n)
print(nums)                            # [1, 2, 3]: the second 2 was skipped
```

The fix for the second case is to build a new list, `nums = [n for n in nums if n != 2]` ([2.17](#s2-17){.ref}). The first output line shows `[1, 2] [1, 2]` because both calls return the same list object, and `print` shows its final state.

Built-in containers have the complexity one expects from their implementations, which is a frequent question: `x in list` scans linearly and costs O(n), whereas `x in set` and `x in dict` hash the key and cost O(1) on average; `list.append` is amortised O(1), `list.insert(0, x)` is O(n), and `collections.deque` offers O(1) at both ends. Dictionary keys must be *hashable*, which means immutable: a tuple is a valid key, a list is not.

Special methods, written with double underscores, let a class join the language's protocols: `__repr__` for printing, `__eq__` and `__hash__` for equality and hashing, `__lt__` for sorting, `__len__`, `__iter__` and `__contains__` for containers. A class that defines `__eq__` must define `__hash__` consistently, or it becomes unhashable.

```python
class Prefix:
    __slots__ = ("addr", "length")
    def __init__(self, addr, length): self.addr, self.length = addr, length
    def __repr__(self): return f"Prefix({self.addr!r}, {self.length})"
    def __eq__(self, o): return (self.addr, self.length) == (o.addr, o.length)
    def __hash__(self): return hash((self.addr, self.length))
    def __lt__(self, o): return (-self.length, self.addr) < (-o.length, o.addr)

ps = [Prefix("10.0.0.0", 8), Prefix("10.1.0.0", 16), Prefix("10.0.0.0", 8)]
print(sorted(ps), len(set(ps)))
# [Prefix('10.1.0.0', 16), Prefix('10.0.0.0', 8), Prefix('10.0.0.0', 8)] 2
```

Python's integers have arbitrary precision, so there is no overflow, and `//` floors (`-7 // 2` is `-4`, `-7 % 2` is `1`), unlike C, where division truncates towards zero ([2.15](#s2-15){.ref}, T32). The conversion `int("ff", 16)` gives 255, `int.from_bytes(b"\x00\x50", "big")` gives 80 and `(80).to_bytes(2, "big")` gives `b'\x00P'`.

::: check
1. What does `bool("0")` return, and why? [^c2-28]
2. Why is `{[1, 2]: "x"}` an error? [^c2-29]
:::

[^c2-28]: `True`; any non-empty string is true, whatever its characters.
[^c2-29]: A list is mutable and therefore unhashable, so it cannot be a dictionary key.

## [2.17]{.sec}Python: comprehensions and generators [Should · ■■□]{.tag} {#s2-17}

A *comprehension* builds a list, set or dictionary from an iterable in one expression: `[x * x for x in range(5) if x % 2 == 0]` is `[0, 4, 16]`, `{x % 3 for x in range(10)}` is `{0, 1, 2}`, and `{w: len(w) for w in words}` maps each word to its length. A comprehension is shorter than the equivalent loop and avoids the repeated attribute lookup of `append`, but one that needs more than one condition is clearer as a loop.

A *generator* produces its values one at a time instead of storing them. The generator expression `(x * x for x in range(5))` looks like a list comprehension in round brackets, and a function containing `yield` is a generator function: each call to `next` runs the body until the next `yield`, then pauses with its local state intact. A generator is *exhausted* after one pass.

```python
sq = (x * x for x in range(5))
print(next(sq), next(sq), sum(sq), sum(sq))   # 0 1 29 0: the second sum finds nothing left

def fib():
    a, b = 0, 1
    while True:                                # infinite, yet uses constant memory
        yield a
        a, b = b, a + b
print(list(islice(fib(), 8)))                 # [0, 1, 1, 2, 3, 5, 8, 13]   (from itertools import islice)
```

The benefit is memory. Reading a 50 GB log into a list needs 50 GB, whereas a generator pipeline holds one line at a time. A `for` loop over a file object already reads lazily, so a pipeline chains generators, each consuming the previous one.

```python
from collections import Counter

def read_lines(path):
    with open(path) as f:                      # closed even if the consumer stops early
        for line in f:
            yield line.rstrip("\n")

def src_ips(lines):
    for line in lines:
        yield line.split(None, 1)[0]           # first whitespace-separated field

counts = Counter(src_ips(read_lines("access.log")))
print(counts.most_common(3))                   # the three most frequent addresses with counts
```

For lines `10.0.0.1 GET /a`, `10.0.0.2 GET /b`, `10.0.0.1 POST /c`, `10.0.0.3 GET /a`, `10.0.0.1 GET /d`, `10.0.0.2 GET /e` the call prints `[('10.0.0.1', 3), ('10.0.0.2', 2), ('10.0.0.3', 1)]`. The memory used is proportional to the number of *distinct* addresses, not to the file size, which is the answer to the "what if the file is 50 GB?" follow-up. If even the distinct set is too large, one sorts externally or uses a counting sketch, as discussed in [Pillar 1](#ch1){.ref}. For the top `k` only, `heapq.nlargest(k, counts.items(), key=lambda kv: kv[1])` costs O(n log k).

::: lens
[GOOGLE · AMAZON · MICROSOFT]{.co}

"Extract the IP addresses from a log and sort by frequency; what if the file is 50 GB?" is a reported Google question. A strong answer streams with a generator, counts with a `Counter`, and states the memory bound and the point at which one would switch to external sorting. Follow-ups: the difference between `most_common(k)` and a heap, and why a list comprehension over the whole file would fail.
:::

::: check
1. How does `[f(x) for x in xs]` differ from `(f(x) for x in xs)` in memory? [^c2-30]
2. What does a generator return when called a second time after exhaustion? [^c2-31]
:::

[^c2-30]: The list comprehension builds all results at once; the generator expression computes one at a time on demand.
[^c2-31]: Nothing: the iteration is already finished, so `next` raises `StopIteration` and a `for` loop ends immediately.

## [2.18]{.sec}Python: struct, re, subprocess, files, exceptions [Must · ■■□]{.tag} {#s2-18}

**Binary data with `struct`.** The module `struct` converts between Python values and packed bytes, using a format string. The first character selects byte order and alignment: `!` means network (big-endian) order with no padding, `<` little-endian, and no prefix means *native* order with C-style padding. The letters are `B` (1 byte), `H` (2), `I` (4), `Q` (8) and `Ns` for `N` raw bytes. Unpacking the IPv4 header of [2.14](#s2-14){.ref} takes one line.

```python
hdr = bytes.fromhex("45000073000040004011b861c0a80001c0a800c7")
fmt = "!BBHHHBBH4s4s"                         # 1+1+2+2+2+1+1+2+4+4 = 20 bytes
v_ihl, tos, total, ident, frag, ttl, proto, csum, src, dst = struct.unpack(fmt, hdr)
print(v_ihl >> 4, v_ihl & 15, total, ttl, proto, hex(csum))   # 4 5 115 64 17 0xb861
print(".".join(map(str, src)), struct.calcsize(fmt))           # 192.168.0.1 20
print(struct.pack("!HI", 80, 1), struct.calcsize("BI"), struct.calcsize("!BI"))
# b'\x00P\x00\x00\x00\x01' 8 5
```

The last line shows the padding rule of [2.7](#s2-7){.ref} in Python: `"BI"` uses native alignment and occupies 8 bytes, while `"!BI"` is packed into 5. For a wire format the prefix `!` is always correct.

**Regular expressions with `re`.** A regular expression describes a text pattern. The functions are `re.search` (first match anywhere), `re.match` (match at the start), `re.findall` and `re.sub`. Named groups `(?P<name>...)` make a log parser self-documenting, and `re.compile` avoids recompiling the pattern in a loop.

```python
log = "Oct 29 10:01:02 sw1 %LINK-3-UPDOWN: Interface Gi0/1, changed state to down"
pat = re.compile(r"(?P<host>\S+) %(?P<fac>[A-Z]+)-(?P<sev>\d)-(?P<mn>[A-Z_]+): "
                 r"Interface (?P<ifc>\S+), changed state to (?P<st>up|down)")
m = pat.search(log)
print(m["host"], m["sev"], m["ifc"], m["st"])      # sw1 3 Gi0/1 down
```

Use raw strings (`r"..."`) so that backslashes reach the regular-expression engine. Quantifiers are greedy by default, so `.*` consumes as much as it can; `.*?` is the minimal form. When the input has fixed whitespace-separated columns, `line.split()` is faster and clearer than a regular expression, as in the table-parsing exercise of the [Problem Set](#ps2){.ref}.

**Running programs with `subprocess`.** `subprocess.run` starts a command, waits, and returns a result. Pass the command as a *list* so that no shell is involved and no argument can be interpreted as shell syntax; this is the main defence against command injection. `check=True` raises `CalledProcessError` on a non-zero exit status, `capture_output=True` collects the output, `text=True` decodes it, and `timeout` raises `TimeoutExpired` for a hung command.

```python
r = subprocess.run(["echo", "hi"], capture_output=True, text=True, check=True, timeout=5)
print(repr(r.stdout), r.returncode)                # 'hi\n' 0
try:
    subprocess.run(["false"], check=True)
except subprocess.CalledProcessError as e:
    print("rc", e.returncode)                       # rc 1
```

**Files.** Open files with a `with` block, which closes the file even when an exception occurs. `for line in f` reads lazily; `f.read()` loads everything. Open in text mode (`"r"`) for logs and in binary mode (`"rb"`) for packets and captures. The encoding defaults to the platform's, so give `encoding="utf-8"` for portable code.

**Exceptions.** `try` runs the code, `except E as e` handles a named error type, `else` runs only when no exception occurred, and `finally` always runs. Catch the narrowest type that you can handle; a bare `except:` also swallows `KeyboardInterrupt`. To translate an error and keep the original, use `raise New(...) from e`.

```python
class ParseError(Exception): pass
def parse(s):
    try:
        return int(s)
    except ValueError as e:
        raise ParseError(f"bad number {s!r}") from e
try: parse("x")
except ParseError as e: print(e, type(e.__cause__).__name__)   # bad number 'x' ValueError
```

::: trap
*Claim:* `subprocess.run(f"ping -c1 {host}", shell=True)` is fine because the hostnames come from our own inventory. *Why it is wrong:* the string is parsed by the shell, so a value such as `8.8.8.8; rm -rf ~` runs a second command, and inventories do get corrupted. *Correct statement:* pass an argument list, `["ping", "-c1", host]`, without `shell=True`.
:::

::: check
1. What is the byte string produced by `struct.pack("!H", 80)`? [^c2-32]
2. When does the `else` clause of a `try` statement run? [^c2-33]
:::

[^c2-32]: `b'\x00P'`, the two bytes `00 50`, since `P` is the character 0x50.
[^c2-33]: Only when the `try` body finished without raising an exception.

## [2.19]{.sec}C++: references, classes and RAII [Should · ■■□]{.tag} {#s2-19}

C++ is C with abstractions that cost nothing when unused. Interviews ask for a small, repeatable core: references, constructors and destructors, resource ownership, and move semantics. Examples assume `g++ -std=c++17`.

A *reference* is a second name for an existing object: `int &r = x; r = 9;` changes `x`. Unlike a pointer, a reference must be bound when created, cannot be rebound, and cannot be null. Its main use is a parameter: `void f(const Packet &p)` passes without copying and without allowing modification, and `void g(Packet &p)` lets the callee modify the caller's object.

A *class* bundles data and functions and controls access with `private` and `public`. A *constructor* initialises an object and a *destructor* `~T()` runs when the object's lifetime ends, whether the scope exits normally or by an exception. This guaranteed call is the basis of **RAII** (resource acquisition is initialisation): acquire a resource in a constructor and release it in the destructor, so that the resource cannot leak on any path.

::: bigidea
Tie every resource, whether memory, file, lock or socket, to the lifetime of an object, because the destructor runs on every exit path, including exceptions.
:::

```cpp
struct Guard {
    const char *name;
    explicit Guard(const char *n) : name(n) { std::printf("acquire %s\n", name); }
    ~Guard() { std::printf("release %s\n", name); }
    Guard(const Guard &) = delete;            // a guard must not be copied
    Guard &operator=(const Guard &) = delete;
};
void work(bool fail) {
    Guard a("A");  Guard b("B");
    if (fail) throw std::runtime_error("boom");
    std::puts("work done");
}
```

Calling `work(false)` prints `acquire A`, `acquire B`, `work done`, `release B`, `release A`. Calling `work(true)` inside a `try` prints `acquire A`, `acquire B`, `release B`, `release A` and then, in the handler, `caught boom`. Destructors run in reverse order of construction, and they run during the unwinding caused by the exception. The standard library applies the same pattern: `std::lock_guard` holds a mutex, `std::ifstream` closes its file, `std::vector` frees its memory.

The compiler generates five special members when asked or needed: the copy constructor, copy assignment, move constructor, move assignment and destructor. The *rule of zero* says to write none of them and let members such as `std::vector` and `std::unique_ptr` manage themselves. The *rule of three/five* says that if a class defines a destructor, copy operation or move operation to manage a raw resource, it should define or delete all five. A *move* transfers a resource from a temporary or an `std::move`d object instead of copying it, leaving the source empty but valid.

```cpp
class File {
    std::FILE *f_;
public:
    explicit File(const char *p) : f_(std::fopen(p, "r")) { if (!f_) throw std::runtime_error("open"); }
    ~File() { if (f_) std::fclose(f_); }
    File(File &&o) noexcept : f_(o.f_) { o.f_ = nullptr; }   // ownership moves
    File(const File &) = delete;                             // two owners would close twice
};
```

::: trap
*Claim:* in C++ it is enough to call `delete` at the end of the function. *Why it is wrong:* an exception or an early `return` before that line skips it, and the memory leaks. *Correct statement:* never write a bare `new` in application code; use `std::make_unique<T>()` or a container, so that the destructor frees the memory on every path.
:::

::: check
1. In which order are local objects destroyed? [^c2-34]
2. Why delete the copy constructor of a class that owns a `FILE *`? [^c2-35]
:::

[^c2-34]: In reverse order of construction, when the scope ends.
[^c2-35]: A copy would give two owners of one handle, and both destructors would close it, which is a double free.

## [2.20]{.sec}C++: virtual functions and the vtable [Should · ■■□]{.tag} {#s2-20}

*Inheritance* lets a derived class reuse a base class, and *polymorphism* lets code written against the base call the derived behaviour. By default C++ binds a member function at compile time, according to the static type of the pointer. Declaring the function `virtual` makes the call dispatch at run time, according to the dynamic type of the object.

```cpp
struct Shape  { virtual double area() const { return 0; }
                virtual ~Shape() { std::puts("~Shape"); } };
struct Circle : Shape { double r; explicit Circle(double r) : r(r) {}
                double area() const override { return 3 * r * r; }
                ~Circle() override { std::puts("~Circle"); } };

Shape *s = new Circle(2);
std::printf("%g\n", s->area());      // 12: Circle::area, chosen at run time
delete s;                            // ~Circle, then ~Shape
```

The standard implementation is the *vtable*. For each class with virtual functions the compiler builds one table of function addresses, and each object carries a hidden pointer to its class's table, the *vptr*, stored in the object (typically at offset 0). A virtual call loads the vptr, indexes the table and calls through the result, which costs one extra load and an indirect call. Figure 2.7 shows two objects sharing one table per class.

<figure>
<svg viewBox="0 0 480 170" width="480">
  <defs><marker id="a27" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" class="accf"/></marker></defs>
  <text class="lbl" x="10" y="14">objects (heap or stack)</text>
  <rect class="box" x="10" y="22" width="90" height="26"/><text class="mono" x="55" y="39" text-anchor="middle">vptr</text>
  <rect class="box" x="10" y="48" width="90" height="26"/><text class="mono" x="55" y="65" text-anchor="middle">r = 2</text>
  <text class="sm" x="10" y="88">Circle c1</text>
  <rect class="box" x="10" y="100" width="90" height="26"/><text class="mono" x="55" y="117" text-anchor="middle">vptr</text>
  <rect class="box" x="10" y="126" width="90" height="26"/><text class="mono" x="55" y="143" text-anchor="middle">r = 5</text>
  <text class="sm" x="105" y="146">Circle c2</text>
  <text class="lbl" x="250" y="14">vtable of Circle (one per class, in .rodata)</text>
  <rect class="fill" x="250" y="22" width="220" height="26"/><text class="mono" x="360" y="39" text-anchor="middle">[0] &amp;Circle::area</text>
  <rect class="fill" x="250" y="48" width="220" height="26"/><text class="mono" x="360" y="65" text-anchor="middle">[1] &amp;Circle::~Circle</text>
  <text class="sm" x="250" y="88">a Shape object would point to its own table</text>
  <text class="sm" x="250" y="100">with &amp;Shape::area and &amp;Shape::~Shape</text>
  <line class="acc" x1="100" y1="35" x2="248" y2="35" marker-end="url(#a27)"/>
  <path class="acc" d="M100,113 L180,113 L180,60 L248,60" marker-end="url(#a27)"/>
  <text class="sm" x="250" y="150">s-&gt;area() compiles to: load s-&gt;vptr, load slot [0], call it</text>
</svg>
<figcaption><b>Figure 2.7</b> Two <code>Circle</code> objects point to the same vtable; the call chooses its target through the pointer, not the type of <code>s</code>.</figcaption>
</figure>

A consequence is visible in the size of objects. `struct Plain { int x; void f() {} };` is 4 bytes, because non-virtual functions are not stored in the object, while `struct Virt { int x; virtual void f() {} };` is 16 bytes on LP64: an 8-byte vptr, the 4-byte `int` and 4 bytes of padding. An empty-looking `Shape` with only virtual functions is 8 bytes, just the vptr.

::: trap
*Claim:* a base class needs no virtual destructor if the derived class adds no data. *Why it is wrong:* `delete` on a `Base *` that points to a `Derived` calls only `~Base` when the destructor is not virtual, which is undefined behaviour and skips the derived cleanup. *Correct statement:* any class meant to be used polymorphically gets a `virtual` destructor. The experiment with `NShape` and `NCircle` (no `virtual`) prints only `~NShape`, and `s->area()` returns the base result 0, not 3.
:::

Two related hazards. *Slicing*: assigning a `Circle` to a `Shape` object, as in `Shape sl = c;`, copies only the base part; `sl.area()` then returns 0, the base version, because `sl` is a real `Shape`, so polymorphism needs a pointer or reference. *Calling virtual functions in constructors*: while a base constructor runs the object is still a base, so the base version is called. A `= 0` after the declaration makes a function *pure virtual* and the class *abstract*, which cannot be instantiated and serves as an interface.

::: lens
[NOKIA · CISCO · MICROSOFT]{.co}

"What is a virtual function and how is it implemented? Why a virtual destructor?" is a reported C++ question. A strong answer draws Figure 2.7, states the cost (one pointer per object, one indirect call), and explains the destructor rule with the `delete base_ptr` case. Follow-ups: the size of an object with virtual functions, what a pure virtual function is, and why virtual calls resist inlining.
:::

::: check
1. How many vtables exist for ten `Circle` objects? [^c2-36]
2. What does `sizeof(Shape)` report on LP64 for a class with only virtual functions? [^c2-37]
:::

[^c2-36]: One for the class `Circle`; the ten objects each hold a pointer to it.
[^c2-37]: 8, the size of the vptr, since the class has no data members.

## [2.21]{.sec}C++: STL containers and smart pointers [Should · ■■□]{.tag} {#s2-21}

The Standard Template Library supplies containers, iterators and algorithms. The interview skill is to choose the container by the operations needed, and to state the cost. The table gives the usual figures; "amortised" means averaged over a sequence of operations, and "average" for hashed containers assumes a good hash function.

| Container | Access | Insert / erase | Find | Notes |
|---|---|---|---|---|
| `vector` | O(1) by index | back: amortised O(1); middle: O(n) | O(n) | contiguous; best default |
| `deque` | O(1) by index | both ends O(1); middle O(n) | O(n) | blocks of memory; no contiguity |
| `list` | O(n) | O(1) given an iterator | O(n) | doubly linked; stable iterators |
| `set`, `map` | none by position | O(log n) | O(log n) | red-black tree; sorted order |
| `unordered_set`, `unordered_map` | none | average O(1), worst O(n) | average O(1), worst O(n) | hash table; no order |
| `priority_queue` | top O(1) | push, pop O(log n) | none | binary heap; max-heap by default |

`std::map` keeps keys sorted, so iteration yields `a=1 b=2` for keys inserted as `b`, `a`, and range queries (`lower_bound`) are possible; `unordered_map` is faster for plain lookup. `vector::push_back` doubles the capacity when full: in libstdc++ 1000 insertions cause 11 reallocations, which is why the cost is amortised O(1). `map::operator[]` inserts a default element if the key is absent, so use `count` or `find` to test membership without modifying the map.

::: trap
*Claim:* a pointer or iterator into a `vector` stays valid while the vector grows. *Why it is wrong:* when the capacity is exceeded, the vector allocates a new block, copies the elements and frees the old block, so every saved pointer, reference and iterator dangles. *Correct statement:* after any operation that may reallocate (`push_back`, `insert`, `reserve`), re-obtain iterators, or store indices instead. In the test `v{1,2,3}; p = &v[0]; v.reserve(100);` the comparison `p == &v[0]` is false.
:::

*Smart pointers* apply RAII to heap objects. A `std::unique_ptr<T>` has exactly one owner, costs nothing beyond the raw pointer, cannot be copied and can be moved; create it with `std::make_unique<T>(args)`. A `std::shared_ptr<T>` shares ownership through a reference count and frees the object when the last owner is destroyed. A `std::weak_ptr<T>` observes a `shared_ptr` object without owning it.

```cpp
auto up  = std::make_unique<int>(5);
auto up2 = std::move(up);            // up is now null; ownership moved
auto sp  = std::make_shared<int>(7);
auto sp2 = sp;                       // sp.use_count() == 2
```

`shared_ptr` has a failure mode that garbage-collected languages do not: a reference cycle. If two nodes hold `shared_ptr` to each other, neither count reaches zero and both leak. In the test, the destructors of two cyclic `Node` objects never run, whereas replacing the back-pointer by a `weak_ptr` (as in a doubly linked list's `prev`) prints `~NodeW` twice. Hence the guideline: `unique_ptr` by default, `shared_ptr` only for genuinely shared ownership, and `weak_ptr` for back-references and caches.

::: check
1. Which container gives sorted iteration, and what does a lookup cost? [^c2-38]
2. Why do two `shared_ptr` nodes pointing at each other leak? [^c2-39]
:::

[^c2-38]: `std::map` or `std::set`, with O(log n) per lookup.
[^c2-39]: Each holds a reference to the other, so neither count falls to zero and neither destructor runs.

:::
