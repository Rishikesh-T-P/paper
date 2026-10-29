# Pillars 1 & 2: Chapter Plan
## Pillar 1: DSA & Coding · Pillar 2: Programming (C, Python, C++, Bash)

> Planning document for the placement textbook *From Zero to Network Engineer*. It is not prose. Every section lists **core idea → hook → worked example → figure(s)**. British spelling throughout.

---

## 0. Evidence base and how to read the tags

### 0.1 What the interview reports actually say (summarised from sources in §S)

| Company | Coding-round shape reported | Topics reported by candidates | Confidence |
|---|---|---|---|
| **Cisco** | HackerRank OA, 70–90 min: 2–3 coding problems plus ~25–40 MCQs on networking, OS, DS and maths. One report says the language choice was limited to C, Python and Java | Snake & Ladder (BFS/DFS); two graph problems; Expressive Words; Longest Substring Without Repeating Characters; Two Sum; pointer output-prediction MCQs; basic bit manipulation; recursion vs infinite loop; C memory allocation, static and global variables, **structure padding, macros, endianness**, `volatile` with a scenario; subnetting calculations in MCQs | High (many reports, 2020–2026) |
| **Juniper** | OA of ~35 MCQs plus 3 coding problems (90 min); clear at least 1 | Merge two sorted arrays; **multiply without `*`**; rotate array right by one; **cycle detection in a singly linked list**; strings, **bit manipulation**, linked lists, **state machines**; stacks/queues, trees, BSTs; OS, DBMS and CN theory | High |
| **Qualcomm** | Written/OA then 2–3 technical rounds | **Count bits to flip A→B**; set/clear/toggle/flip k-th bit; **struct vs union; structure padding; `sizeof` of a mixed `short/long/char` struct; size of a struct without `sizeof`**; `const` and `volatile`; then a bit problem | High |
| **Arista** | OA of 4 coding + 5 C MCQs (pointers, dynamic memory); CoderPad onsite | **Linked lists in C from scratch**: delete node (pointer-to-pointer trap), delete all nodes = key, add two lists, merge sorted, reverse a DLL, delete from DLL, remove duplicates in a circular list; **BST operations**; memory layout of a program (stack/heap); mutex; deadlock prevention; **edit, compile and run on the Linux CLI** | High |
| **Google** (NetEng / SWE-networking) | Screen, 2 coding, 2 networking, 1 behavioural (one report) | **Trie: longest common/longest-prefix match on a list of IPs against a target**; Python: **extract IPs from a log and sort by frequency**; parse RPC log for slowest method; VLANs, trunks, ARP, routing | Medium |
| **Microsoft** (Azure) | Standard SWE loop | **LRU cache (plus TTL variant and concurrency follow-up)**; distributed rate limiter design; file-system design | Medium |
| **Amazon NDE** | Networking-heavy loop plus Leadership Principles | OSPF/BGP/TCP at CCNP–CCIE depth; **Python automation questions**; your own automation project; OA of LeetCode easy + medium (NDE/"Non-SDE" reports); LRU-style question, trees, graphs, strings | Medium |
| **Nokia** | Aptitude + basic coding, then technical + HR | **Find the loop in a linked list; intersection of two lists; DFS with a stack**; C/C++, OOP; TCP/UDP, OSI; C/C++, Python and Bash in job descriptions | Medium |
| **Broadcom** | Phone and onsite rounds; take-home code in some | **Bit manipulation, linked lists (reverse, insert/delete), pointers, arrays, stacks, queues**; bit-level C; static variables; state machines; RTOS; "test memory bit-cells of a segment in C" | Medium (older reports) |

### 0.2 Tag legend used throughout
- **[S: Co]**: a candidate report names this problem or topic for that company (see §S).
- **[I: Co]**: inferred. It fits the company's known focus, but no report names it. Authors should keep this distinction visible in the book. Use a solid company chip for S and an outlined chip for I.
- Difficulty: **E** easy · **M** medium · **H** hard (interview-hard, not contest-hard).
- LeetCode/GfG numbers and titles are **cross-references only**. The book restates every problem in full (statement, constraints, examples), so the reader never has to leave the PDF. Premium problems **(P)** are restated the same way.

### 0.3 Book-wide design devices used in these two pillars
- **"Packet Lens" sidebar**: maps every abstract DS/algorithm to a real networking system (trie → FIB, LRU → ARP cache, ring buffer → NIC RX ring, Dijkstra → OSPF SPF).
- **"Trap!" box**: red-edged; common mistake plus the one-line fix.
- **"Interviewer's Follow-up" box**: the next question the interviewer usually asks.
- **Company chips**: small coloured pills (Cisco, Qualcomm, Google, Microsoft, Amazon, Juniper, Arista, Nokia, Broadcom) in the margin.
- **Complexity badge**: `O(n) time · O(1) space` pill under every solution.
- **Dual-language code**: C and Python side by side for core problems. Use C++ only where the STL is the point.

### 0.4 Book-wide conventions (user requirements: self-contained PDF, priority tags, full solutions, end-of-chapter pack)

**(a) Priority tags (navigation aid; nothing is trimmed).** Every section heading carries `[MUST · n d]`, `[SHOULD · n d]` or `[OPTIONAL]`, where *n d* is the suggested study days at ~2 h/day.
- **MUST:** asked repeatedly across several target companies, or a prerequisite for later pillars. Never skip.
- **SHOULD:** asked at some companies or needed for depth roles (Google/Microsoft SWE-networking, data-plane roles).
- **OPTIONAL:** enrichment, real-world depth or rare questions. These subsections are marked inline.
- Day totals: Pillar 1 ≈ 48 study days (MUST ≈ 38), Pillar 2 ≈ 43 study days (MUST ≈ 31). Both are comprehensive. A reader on a short personal timeline can follow MUST-only, then SHOULD. A colour-coded "Route map" page at the start of each pillar lists the sections in this order (green MUST, amber SHOULD, grey OPTIONAL) with day budgets and a tick-box.

**(b) Self-containment rule.** No section may depend on an external resource:
- Every problem is restated in full in the book.
- Every tool command (gcc, gdb, valgrind, Python modules, Bash utilities) is explained in the book with its output reproduced.
- Sample data files (logs, routing tables, hex dumps, pcaps) are printed in an appendix as text or hex. The book also lists a generator script the reader can type in.
- External URLs appear only in "Further reading" boxes and the sources list, never as required reading.

**(c) Full-solution template, applied to EVERY problem.** This covers each tiered problem, each question-bank entry and each worked example. Layout is 1–3 pp per problem:
1. **Problem statement** (restated in full), constraints, 2–3 examples, company chips (S/I).
2. **Clarifying questions** the candidate should ask (e.g. "Are leading zeros allowed?").
3. **Intuition / analogy** (2–4 lines) plus a small figure where helpful.
4. **Approach ladder:** brute force → better → optimal. Each rung gets one paragraph and a complexity badge.
5. **Code:** the optimal solution in **C** (mandatory for Pillar 2 and for all linked-list, bit and struct problems) and **Python** (mandatory for strings/parsing and design). Use **C++** where STL use is the point. Code is complete and compilable or runnable, with line-numbered annotations.
6. **Dry run:** a trace table on one example.
7. **Complexity:** time and space, with a one-line justification.
8. **Edge cases and tests:** a bulleted list plus the test harness snippet.
9. **Common mistakes:** 2–4 bullets, linked to the chapter's Trap boxes.
10. **Interviewer follow-ups:** 2–4 likely next questions, each with a short model answer (e.g. "Now make it thread-safe", "Now for IPv6").
11. **Related problems:** cross-references within the book.
Conceptual questions (e.g. "What does `volatile` do?") use a shorter template: **30-second answer** → **2-minute deep answer** with a code snippet or figure → **follow-ups with answers** → **mistakes candidates make**.

**(d) End-of-chapter pack (every pillar).** Each pillar closes with four tear-out sections:
1. **Short notes:** ~½ page per section in bullet form (definitions, key formula or idiom, one mini-example). This is revision without re-reading the chapter.
2. **One-page revision sheet:** the dense cheat-sheet specified for each pillar below, designed to print on a single A4 side.
3. **Flashcards:** a printable 2-column grid (question front / answer back, cut lines), each card tagged with section and priority.
4. **Solved interview problems:** every question-bank entry fully solved using template (c), grouped by company. Each group starts with a "company spotlight" (round format, what they emphasise, sourced chips).

---

# PILLAR 1: DSA & CODING

## Chapter header
- **Title:** *Pillar 1: Thinking in Data Structures: Coding Rounds for Network Engineers*
- **Promise:** "By the end you will solve the easy and medium problems that Cisco, Juniper, Arista and Qualcomm set in their online tests, and write a longest-prefix-match router table, an ARP-style LRU cache and a token-bucket limiter from a blank screen."
- **Prerequisites:** Pillar 2 §2.1–2.6 (C basics, pointers) **or** Python basics (§2.17), so the reader can write loops, functions and arrays. School maths (powers of 2, logarithms). Readers can work through Pillar 2 Part A in parallel with this pillar.
- **Estimated pages:** ~400 in total: teaching sections ~170 pp; full solutions to all ~105 tiered problems at ~1.5 pp ≈ 160 pp (worked examples inside sections are counted in the teaching pages); end-of-chapter pack ≈ 70 pp (short notes 10, revision sheet 1, flashcards 9, solved interview bank of 34 problems ≈ 50).
- **Weeks to study:** **8 weeks** at 2 h/day: weeks 1–2 §1.1–1.5; weeks 3–4 §1.6–1.10; weeks 5–6 §1.11–1.14; weeks 7–8 §1.15–1.18 plus mock interviews. Fast track (company visiting in 3 weeks): §1.1, 1.3–1.7, 1.9, 1.15 only. That path is ~70 pp and marked with a ⚡ icon.

## Learning objectives
1. Estimate the time and space complexity of any loop, recursion or data-structure operation using Big-O. Pick an algorithm whose complexity fits the input limit (n ≤ 10⁵ ⇒ O(n log n)).
2. Apply a fixed six-step routine (Understand → Examples → Brute force → Optimise → Code → Test) aloud in an interview.
3. Use arrays, strings, hash maps and sets with two-pointer, sliding-window and prefix-sum patterns.
4. Parse and validate network strings (IPv4, IPv6, CIDR, MAC) robustly, covering every edge case.
5. Manipulate bits fluently: masks, shifts, popcount, set/clear/toggle, subnet arithmetic, IP⇄integer.
6. Implement singly, doubly and circular linked lists in C, including deletion with pointer-to-pointer, reversal, cycle detection and intersection.
7. Implement stacks, queues, circular buffers and deques, and explain where routers use each.
8. Build, traverse and modify binary trees and BSTs from scratch (insert, delete, search, LCA, level order).
9. Build a binary trie and solve longest-prefix match, maximum XOR and CIDR-filter problems.
10. Use heaps for top-k, k-way merge and scheduling problems.
11. Model networks as graphs. Apply BFS, DFS, Dijkstra, Bellman–Ford, union–find, topological sort and bridge-finding, and link each to a routing protocol.
12. Recognise and solve introductory backtracking and dynamic-programming problems (1-D/2-D DP).
13. Use binary search and interval merging for IP-range problems.
14. Design and code stateful components: LRU/LFU cache, TTL cache, token bucket, sliding-window limiter, hit counter, consistent hashing.
15. Encode a protocol finite-state machine (TCP) and validate event sequences.
16. Write test cases (empty, single, boundary, overflow, malformed input) before declaring a solution done.

## Section-by-section outline

### 1.0 How network-company coding rounds work (4 pp) `[MUST · 0.5 d]`
- **Core idea:** Network companies test fundamentals in C or Python more than contest tricks, so breadth and clean code beat obscure algorithms.
- **Hook:** "Your OA is a 90-minute packet capture of how you think."
- **Worked example:** A reconstructed Cisco-style OA timeline (2 coding + 30 MCQs, 90 min). Show a minute-by-minute budget and a triage rule: read all problems first, then bank the easy one.
- **Figures:**
  1. *Swim-lane diagram:* rows = Cisco, Juniper, Qualcomm, Arista, Google, Microsoft, Amazon NDE, Nokia, Broadcom; columns = OA → Tech 1 → Tech 2 → Manager → HR. Cells hold icons (code, MCQ, network, behaviour). Source caption required.
  2. *Stacked bar chart:* reported topic mix per company (DSA / C internals / networking / behavioural). Label it "indicative, from candidate reports".
  3. *Decision tree:* "Which language should I code in?" (C if the role says embedded or data plane, or the OA allows only C, Python or Java; Python for NDE or automation; C++ if comfortable with the STL).

### 1.1 Complexity and the problem-solving routine (8 pp) `[MUST · 2 d]`
- **1.1.1 Big-O, Θ, Ω intuitively.** *Core:* Count how work grows, not seconds. *Hook:* flooding a frame to every port (O(n)) vs a MAC-table lookup (O(1)). *Example:* analyse three snippets: a single loop, nested loops, and a halving loop (`while (n) n >>= 1;` → O(log n)). *Figure:* log-log growth chart of 1, log n, n, n log n, n², 2ⁿ, with an "n = 10⁵ budget line" at ~10⁸ ops.
- **1.1.2 Constraints → target complexity table.** *Core:* Input size tells you the algorithm. *Example:* n ≤ 20 → 2ⁿ backtracking; n ≤ 10⁵ → n log n. *Figure:* lookup table graphic shaped like a speed-limit sign.
- **1.1.3 Space complexity and the call stack.** *Core:* Recursion costs memory. *Hook:* each nested function call is a plate on a stack. *Example:* recursive vs iterative factorial and the stack depth for n = 10⁶ (stack overflow). *Figure:* call-stack tower with frames labelled `fact(4)…fact(1)`, showing return addresses and locals.
- **1.1.4 The six-step interview routine (UMPIRE-style).** *Core:* A visible process earns marks even when the code is unfinished. *Example:* walk Two Sum [S: Cisco] through all six steps, from brute force O(n²) to hash map O(n). *Figure:* circular flow diagram of the six steps with "think aloud" speech bubbles.
- **1.1.5 Amortised analysis (dynamic array growth).** *Core:* Occasional expensive resizes average out. *Example:* push 1…16 into a doubling array and count copies. *Figure:* bar chart of per-push cost with spikes at 1, 2, 4, 8, 16 and a dashed amortised line.

### 1.2 Arrays and two-pointer and sliding-window patterns (10 pp) `[MUST · 3 d]`
- **1.2.1 Array memory model.** *Core:* Contiguous cells give O(1) indexing. *Hook:* numbered seats in a cinema row. *Example:* address of `a[i]` = base + i·sizeof(T). *Figure:* memory strip with addresses 0x1000, 0x1004…, highlighting `a[3]`.
- **1.2.2 Two pointers.** *Core:* Two indices moving inwards or in step remove a nested loop. *Example:* **Merge two sorted arrays** [S: Juniper], in place from the back (LC 88). *Figure:* two arrays with coloured arrows `i`, `j`, `k`, drawn as 4 frames.
- **1.2.3 Rotation.** *Core:* The reversal trick rotates in O(1) space. *Example:* **rotate right by one, then by k** [S: Juniper] (LC 189): reverse all, reverse first k, reverse rest. *Figure:* three-row "reverse" animation strip.
- **1.2.4 Sliding window.** *Core:* Maintain a window invariant, expand on the right, shrink on the left. *Hook:* TCP's sliding window moves across a byte stream. *Example:* **Longest Substring Without Repeating Characters** [S: Cisco] (LC 3). *Figure:* the string "abcabcbb" with a translucent window box at successive steps and a hash-set panel beside it.
- **1.2.5 Prefix sums.** *Core:* Precompute running totals to answer range sums in O(1). *Hook:* cumulative bytes per second on an interface counter. *Example:* "Total bytes between second l and r" plus Subarray Sum Equals K (LC 560). *Figure:* original array above, prefix array below, bracket showing `P[r]−P[l−1]`.
- **1.2.6 Kadane's algorithm.** *Example:* LC 53, framed as "busiest contiguous traffic burst". *Figure:* line plot of running sum with resets marked.
- **Trap box:** off-by-one at window edges; integer overflow when summing byte counters (use `uint64_t`).

### 1.3 Hashing: maps and sets (8 pp) `[MUST · 2 d]`
- **1.3.1 How a hash table works.** *Core:* A hash function turns a key into a bucket index. *Hook:* the switch MAC address table: MAC → port. *Example:* hand-trace inserting 5 MAC addresses into 8 buckets with chaining. *Figure:* bucket array (0–7), each bucket a chain of nodes `{MAC, port}`, with one collision highlighted.
- **1.3.2 Collisions, load factor, rehashing.** *Example:* compare open addressing (linear probing) with chaining on the same keys. *Figure:* side-by-side panels; probe sequence arrows for linear probing.
- **1.3.3 Frequency counting.** *Example:* **extract IPv4 addresses from a log file and sort by occurrences** [S: Google], in Python with `re` + `Counter`, then in C with a fixed-size hash table. *Figure:* pipeline diagram: log lines → regex → counter dict → sorted list (top 5 bar chart).
- **1.3.4 Grouping and set tricks.** *Example:* Group Anagrams (LC 49); Longest Consecutive Sequence (LC 128) framed as the longest run of consecutive used host IDs. *Figure:* buckets keyed by sorted signature.
- **Packet Lens:** flow tables in firewalls hash the 5-tuple (src IP, dst IP, src port, dst port, protocol). *Figure:* 5-tuple → hash → flow entry.
- **Trap box:** using a mutable list as a dict key in Python; assuming hash-map iteration order in C++ `unordered_map`.

### 1.4 Strings and parsing network data (10 pp) ⚡ `[MUST · 3 d]`
- **1.4.1 String basics and complexity.** Immutability in Python, NUL-terminated strings in C (cross-reference §2.12).
- **1.4.2 Validating IPv4.** *Core:* Split on dots, check exactly 4 parts, digits only, 0–255, no leading zeros. *Hook:* a bouncer checking four ID details. *Example:* **Validate IP Address** (LC 468), with a full IPv4 branch in C (no `strtok` on const input) and in Python. Edge-case table: `"192.168.1.1"`, `"192.168.01.1"`, `"256.0.0.1"`, `"1.1.1."`, `"1e1.4.5.6"`, `""`, `"1..1.1"`. *Figure:* finite-state diagram for one octet (states: START, DIGIT1, DIGIT2, DIGIT3, DOT, REJECT), with transitions labelled by character classes.
- **1.4.3 Validating IPv6.** *Core:* 8 groups of 1–4 hex digits. The LC version disallows `::`; the book also covers real `::` compression. *Example:* LC 468 IPv6 branch plus an extension that expands `2001:db8::1` to its full form. *Figure:* IPv6 address split into 8 coloured hextets, with `::` shown as a collapsible accordion of zero groups.
- **1.4.4 Restore IP Addresses (backtracking teaser).** *Example:* LC 93 on input `"25525511135"`. *Figure:* recursion tree with pruned branches greyed out.
- **1.4.5 Parsing CIDR and MAC.** *Example:* parse `"10.1.0.0/16"` into (network uint32, prefix len); validate a MAC in `aa:bb:cc:dd:ee:ff`, `aa-bb-…` and Cisco dotted `aabb.ccdd.eeff` formats. *Figure:* the three MAC notations aligned to the same 48-bit bar.
- **1.4.6 Run-length and expressive words.** *Example:* **Expressive Words** [S: Cisco OA] (LC 809); String Compression (LC 443). *Figure:* run-length blocks for "heeellooo" vs "hello".
- **1.4.7 Robust number parsing.** *Example:* String to Integer (atoi) (LC 8) with overflow clamping. This leads into Valid Number (LC 65) as a DFA. *Figure:* number-line showing INT_MAX clamping.
- **1.4.8 Version strings.** *Example:* Compare Version Numbers (LC 165), framed as comparing IOS-XE 17.9.4 with 17.12.1. *Figure:* two dotted versions compared component-wise in a table.
- **Trap box:** `"01"` accepted as an octet; `atoi` returning 0 for garbage; forgetting empty segments after `split('.')`; Python `int("٣")` accepting Unicode digits (use `isdigit` with an ASCII check, or a regex).

### 1.5 Bit manipulation and subnet arithmetic (12 pp) ⚡ `[MUST · 4 d]`
- **1.5.1 Binary, hex and two's complement.** *Hook:* a light-switch panel of 8 switches. *Example:* convert 192, 0xC0, and −1 in 8-bit form. *Figure:* 8-bit register with place values 128…1 under each bit; a two's-complement wheel (circle of 16 values for 4-bit).
- **1.5.2 Operators &, |, ^, ~, <<, >>.** *Example:* truth tables plus a "bit-ops in action" table on 0b1011_0110. *Figure:* per-operator mini diagrams (two rows of bits → result row with the changed bits highlighted).
- **1.5.3 Set, clear, toggle, test and flip the k-th bit** [S: Qualcomm]. *Example:* `x | (1u<<k)`, `x & ~(1u<<k)`, `x ^ (1u<<k)`, `(x>>k)&1`, as C macros (link to §2.11). *Figure:* mask construction animation `1 → 1<<k → ~(1<<k)`.
- **1.5.4 Counting bits.** *Core:* `x & (x−1)` clears the lowest set bit. *Example:* **count bits to flip to convert A to B** [S: Qualcomm] = popcount(A ^ B) (LC 461 Hamming Distance / LC 2220). Also Number of 1 Bits (LC 191) and Counting Bits (LC 338). *Figure:* A, B, A^B rows with 1s highlighted, then the Kernighan loop showing successive `x & (x−1)`.
- **1.5.5 Arithmetic without operators.** *Example:* **multiply two numbers without `*`** [S: Juniper] via Russian-peasant shift-and-add; Sum of Two Integers (LC 371) via XOR and carry; Divide Two Integers (LC 29). *Figure:* table of shift-and-add steps (a, b, partial result).
- **1.5.6 Powers of two and alignment.** *Example:* Power of Two (LC 231): `x && !(x & (x−1))`; round up to the next multiple of 8 with `(x+7) & ~7` (links to struct padding §2.9). *Figure:* number line with multiples of 8 and arrows showing rounding.
- **1.5.7 XOR tricks.** *Example:* Single Number (LC 136), Missing Number (LC 268), swap without temp (and why not to use it). *Figure:* XOR cancellation diagram.
- **1.5.8 Reverse bits and byte swap.** *Example:* Reverse Bits (LC 190); 32-bit byte swap with masks, which is `htonl` on little-endian hosts (link to §2.10). *Figure:* 4 coloured bytes A B C D → D C B A, with shift arrows.
- **1.5.9 IPv4 ⇄ uint32 and subnet arithmetic (signature section).** *Core:* An IPv4 address is a 32-bit integer; masks are runs of 1s. *Example:* (a) `ip_to_u32("192.168.10.77")`; (b) `mask = prefix ? ~0u << (32−prefix) : 0` (the prefix 0 trap: shifting by 32 is undefined behaviour in C); (c) network = ip & mask, broadcast = network | ~mask, host count = 2^(32−p) − 2 (and /31 and /32 special cases); (d) **same-subnet check**: `(a & m) == (b & m)`; (e) is a mask valid? `~m & (~m + 1) == 0`; (f) Bitwise AND of Numbers Range (LC 201) = common prefix of a range. *Figure:* a large spread showing 192.168.10.77/26 as 32 bits, mask bits shaded blue, network bits outlined, host bits orange, with derived network, broadcast, first and last host in a side panel.
- **1.5.10 Gray code and parity (bonus).** `[OPTIONAL]` Parity for error detection, a preview of checksums.
- **Trap box:** right-shifting a negative signed int (implementation-defined); `1 << 31` on a signed int (UB); operator precedence `x & 1 == 0` parses as `x & (1 == 0)`.

### 1.6 Linked lists, C-first (14 pp) ⚡ `[MUST · 4 d]`
- **1.6.1 Node anatomy in C.** *Core:* each node owns data plus a pointer to the next. *Hook:* a treasure hunt where each clue tells you where the next one is. *Example:* `struct node { int val; struct node *next; };` plus push-front, push-back, print and free-all. *Figure:* boxes-and-arrows diagram showing heap addresses (0x55a0…) inside each box and `NULL` as a grounded symbol; the `head` pointer lives on the stack (two-region diagram: stack | heap).
- **1.6.2 Deletion and the pointer-to-pointer idiom** [S: Arista]. *Core:* `struct node **pp` lets you delete the head and middle nodes with the same code. *Example:* (a) delete the first node with value k, the naive way with a special head case; (b) the `**pp` way; (c) **delete all nodes matching a key** [S: Arista] (LC 203); (d) Delete Node given only that node (LC 237) plus why it fails on the tail. *Figure:* three-panel diagram where `pp` points first at `head`, then at `n1->next`, then at `n2->next`, with the unlinked node faded and labelled "free()". Second figure: memory diagram of `pp` (address of a pointer) vs `p`.
- **1.6.3 Reversal (iterative and recursive).** *Example:* LC 206 with `prev/curr/next` dance. *Figure:* 4-frame comic strip of pointer re-wiring, colour-coded prev (grey), curr (blue), next (green).
- **1.6.4 Fast and slow pointers.** *Example:* **cycle detection** [S: Juniper, Nokia] (LC 141), then finding the cycle start (LC 142) with a proof sketch; middle of list; nth from end (LC 19). *Figure:* "ρ-shaped" list with tortoise and hare icons, labelled distances `a` (head→entry), `b`, `c`, and the meeting point.
- **1.6.5 Intersection of two lists** [S: Nokia]. *Example:* LC 160 by the two-pointer switch-heads trick and by the length-difference method. *Figure:* Y-shaped list with pointer paths in two colours, both travelling a+c+b.
- **1.6.6 Merging and arithmetic.** *Example:* **merge two sorted lists** [S: Arista, Juniper] (LC 21) with a dummy head; **add two numbers as lists** [S: Arista] (LC 2, and LC 445 for most-significant-first). *Figure:* dummy-node diagram with a tail pointer; digit-wise addition table with carry row.
- **1.6.7 Doubly linked lists** [S: Arista]. *Example:* **reverse a DLL** (swap prev/next in each node); delete a node from a DLL; insert in sorted position. *Figure:* DLL with prev arrows above and next arrows below, before and after the swap.
- **1.6.8 Circular lists** [S: Arista]. *Example:* **remove consecutive duplicates in a circular list**; Josephus problem. *Figure:* ring of nodes with a "tail→head" arc highlighted.
- **1.6.9 Packet Lens: sk_buff queues and `list_head`.** *Core:* The Linux kernel uses intrusive doubly linked lists. *Figure:* `struct sk_buff` with embedded `next/prev`, chained in a NIC TX queue (forward link to §2.11 `container_of`).
- **Trap box:** losing the `next` pointer before `free`; use-after-free when freeing in the loop increment; not setting `head = NULL` after freeing the list; forgetting the empty-list and one-node cases.

### 1.7 Stacks, queues, ring buffers and deques (8 pp) `[MUST · 2 d]`
- **1.7.1 Stack.** *Hook:* a pile of plates; also the call stack. *Example:* Valid Parentheses (LC 20); Min Stack (LC 155); evaluate RPN (LC 150). *Figure:* stack with push and pop arrows; parentheses-matching trace table.
- **1.7.2 Queue and the circular buffer.** *Core:* head and tail indices mod capacity give an O(1) FIFO with no shifting. *Hook:* the NIC receive ring that DMA writes into. *Example:* **Design Circular Queue** (LC 622) in C with a power-of-two capacity and `idx & (N−1)`; full vs empty disambiguation (count vs one-slot-empty). *Figure:* ring diagram of 8 slots with head and tail arrows and occupied slots shaded; a second panel shows the wrap-around.
- **1.7.3 Queue via stacks and vice versa.** *Example:* LC 232 and LC 225. *Figure:* two-stack transfer diagram.
- **1.7.4 Monotonic stack and deque.** *Example:* Daily Temperatures (LC 739); Sliding Window Maximum (LC 239) framed as peak bandwidth in each 5-second window. *Figure:* deque contents per step, with indices and values.
- **1.7.5 Packet Lens: FIFO vs priority queuing.** Brief link to QoS (Pillar 4/5). *Figure:* tail-drop diagram of a full queue.
- **Trap box:** ring-buffer full/empty ambiguity; integer overflow of the free-running index if not masked.

### 1.8 Trees and binary search trees (12 pp) `[MUST · 3 d]`
- **1.8.1 Terminology and traversal.** *Hook:* a company org chart or a file system. *Example:* recursive and iterative pre-, in- and post-order; level order with a queue (LC 102); Max Depth (LC 104); Invert (LC 226). *Figure:* 7-node tree with traversal orders listed underneath in three colours; a queue snapshot for each level.
- **1.8.2 BST insert, search, delete from scratch** [S: Arista]. *Core:* left < node < right gives O(h) operations. *Example:* full C implementation, including the 3 deletion cases (leaf, one child, two children via in-order successor) (LC 701, 450); validate BST (LC 98) with bounds. *Figure:* three-panel deletion diagram with the successor highlighted and the replaced value struck through.
- **1.8.3 Balanced vs degenerate.** *Core:* Sorted inserts give a linked list. *Figure:* side-by-side balanced tree vs right-leaning chain, with heights labelled. Mention AVL/red-black (Linux uses rbtree) without code.
- **1.8.4 LCA, k-th smallest, path sums.** *Example:* LCA in a BST (LC 235) and a binary tree (LC 236); k-th smallest (LC 230). *Figure:* tree with two highlighted nodes and the LCA ringed.
- **1.8.5 Serialise/deserialise.** *Example:* LC 297, framed as sending a tree over a socket. *Figure:* tree ↔ string "1,2,#,#,3,4,#,#,5,#,#".
- **Trap box:** forgetting to return the new root after deletion; recursion depth on skewed trees; using `<=` inconsistently, which breaks duplicates.

### 1.9 Tries and longest-prefix match (12 pp) ⚡ signature chapter `[MUST · 3 d]`
- **1.9.1 Character trie.** *Core:* Each edge is one character, so shared prefixes are stored once. *Hook:* phone-book autocomplete. *Example:* Implement Trie (LC 208); Longest Common Prefix (LC 14). *Figure:* trie for {"cat","car","cart","dog"} with terminal nodes double-circled.
- **1.9.2 Binary trie on IP bits.** *Core:* Walk the 32 bits of an IPv4 address MSB-first; each node may store a next hop. *Hook:* a postal sorting office going country → state → city → street. *Example:* **Longest-prefix-match routing table** [S: Google, trie-based IP prefix-match question]: `insert(prefix, len, nexthop)`, `lookup(ip)` remembering the last node with a next hop. Test table: 0.0.0.0/0→A, 10.0.0.0/8→B, 10.1.0.0/16→C, 10.1.2.0/24→D; look up 10.1.2.9 (D), 10.1.9.9 (C), 10.200.0.1 (B), 8.8.8.8 (A). C and Python versions. *Figure:* binary trie drawn for those 4 prefixes, top 8 levels shown, with dotted ellipses for skipped levels and next-hop labels in coloured tags; the lookup path for 10.1.9.9 is highlighted in bold, ending at C.
- **1.9.3 Alternative LPM approaches.** *Core:* Hash per prefix length, scanning from /32 down to /0. *Example:* the same table with 33 hash maps (the approach in a reported CIDR-membership question). Complexity comparison table. *Figure:* 33 small buckets labelled /0…/32 with an arrow scanning downwards.
- **1.9.4 Path compression (Patricia/radix) and multibit tries (stride 8).** `[OPTIONAL]` Concept only, with a short "how real routers do it" note: TCAM vs tree bitmap. *Figure:* the same prefixes in an uncompressed vs Patricia trie, showing node-count savings; a TCAM row diagram with value/mask/priority columns.
- **1.9.5 Maximum XOR with a binary trie.** `[OPTIONAL]` *Example:* Maximum XOR of Two Numbers (LC 421). *Figure:* the greedy "go opposite bit" path.
- **1.9.6 CIDR firewall filter.** *Example:* a rule list `allow 10.0.0.0/8`, `deny 10.1.0.0/16`, default deny; evaluate IPs with the most specific rule winning (matches the "evaluate IP access rules" style questions found). *Figure:* nested-rectangles (Venn) diagram of address space for the rules.
- **Packet Lens:** FIB vs RIB; why routers need lookups in nanoseconds; Linux's LC-trie (`fib_trie`).
- **Trap box:** shifting by 32; storing the host-order vs network-order address inconsistently; not tracking "best so far" and returning the deepest node visited instead.

### 1.10 Heaps and priority queues (7 pp) `[SHOULD · 2 d]`
- **1.10.1 Binary heap in an array.** *Core:* parent i, children 2i+1 and 2i+2; sift up and sift down. *Hook:* A&E triage. *Example:* implement min-heap push and pop in C. *Figure:* tree view and array view of the same heap, with index arrows linking them.
- **1.10.2 Top-k.** *Example:* Top K Frequent (LC 347), framed as the **top-k talkers in a NetFlow log**; Kth Largest (LC 215). *Figure:* size-k min-heap evicting small elements.
- **1.10.3 k-way merge.** *Example:* Merge k Sorted Lists (LC 23), framed as merging per-router syslog files by timestamp. *Figure:* k arrows into a heap, producing a merged stream.
- **1.10.4 Scheduling.** *Example:* Task Scheduler (LC 621) as a weighted QoS analogy; Find Median from Data Stream (LC 295) for latency medians. *Figure:* two-heap balance diagram.
- **Trap box:** Python `heapq` is min-heap only (negate for max); stable ordering with tuples (add a counter).

### 1.11 Graphs: networks are graphs (16 pp) ⚡ `[MUST · 5 d]`
- **1.11.1 Representations.** *Hook:* a topology diagram is a graph. *Example:* the same 6-router topology as an adjacency matrix, adjacency list and edge list. *Figure:* topology drawing (routers R1–R6, link costs) next to its matrix (heat-shaded) and list.
- **1.11.2 BFS: hop count.** *Example:* **Snakes and Ladders minimum throws** [S: Cisco] (LC 909); shortest hop path between two routers; Number of Islands (LC 200). *Figure:* BFS wavefront rings coloured by distance on the topology; the snakes and ladders board with the BFS frontier.
- **1.11.3 DFS: iterative with an explicit stack** [S: Nokia]. *Example:* connected components (LC 547, Number of Provinces); Clone Graph (LC 133); iterative DFS in C with an array stack. *Figure:* DFS tree with discovery and finish times annotated.
- **1.11.4 Cycle detection and union–find.** *Core:* union–find tells you whether adding a link creates a loop. *Hook:* why Spanning Tree Protocol blocks ports. *Example:* Redundant Connection (LC 684); Number of Operations to Make Network Connected (LC 1319). *Figure:* forest of disjoint sets merging, with path compression arrows; a switch triangle with one link shown "blocked" in STP orange.
- **1.11.5 Dijkstra = OSPF SPF.** *Example:* **Network Delay Time** (LC 743) on a weighted topology; print the shortest-path tree and the next-hop table for R1 (that is exactly what OSPF installs). *Figure:* step table (iteration, visited set, dist[] row) beside the topology, with the final SPF tree in bold.
- **1.11.6 Bellman–Ford = distance-vector (RIP).** *Example:* Cheapest Flights Within K Stops (LC 787) as "max hop count"; a count-to-infinity demonstration. *Figure:* round-by-round distance-vector tables for 4 routers.
- **1.11.7 Minimum spanning tree.** *Example:* Min Cost to Connect All Points (LC 1584) with Kruskal and Prim; cable-laying in a campus. *Figure:* MST edges highlighted on a weighted graph.
- **1.11.8 Topological sort.** *Example:* Course Schedule I/II (LC 207/210), framed as the order to apply configuration dependencies (VRF before interface before BGP neighbour). *Figure:* DAG with Kahn's in-degree counters.
- **1.11.9 Bridges and articulation points.** *Example:* **Critical Connections in a Network** (LC 1192): single points of failure. *Figure:* topology with bridge links in red, plus a discovery/low-link table.
- **1.11.10 Bipartite check (bonus).** `[OPTIONAL]` LC 785.
- **Trap box:** forgetting the visited set (infinite loop, like a broadcast storm); using Dijkstra with negative weights; recursion depth in DFS on 10⁵ nodes (use an explicit stack).

### 1.12 Recursion and backtracking (6 pp) `[SHOULD · 1.5 d]`
- **Core:** Choose → explore → un-choose. *Hook:* trying every key on a keyring. *Examples:* Subsets (LC 78), Permutations (LC 46), Combination Sum (LC 39); revisit Restore IP Addresses (LC 93) with pruning on octet validity. *Figure:* decision tree for Subsets of {1,2,3}, with include/exclude edges and leaves listing subsets.
- **Trap box:** forgetting to undo state; copying the path at a leaf (Python `path[:]`).

### 1.13 Sorting, binary search and intervals (8 pp) `[MUST · 2 d]`
- **1.13.1 Sorts you must code.** `[OPTIONAL]` Merge sort and quicksort (Lomuto/Hoare) in C; counting sort. *Figure:* merge-sort split/merge tree; quicksort partition snapshots with the pivot highlighted.
- **1.13.2 Binary search templates.** *Example:* LC 704, 35, 34, 33 (rotated), 278; plus "find the IP range containing x" given sorted, non-overlapping ranges (GeoIP-style lookup). *Figure:* lo/mid/hi pointers on a sorted array across iterations; invariant box "answer ∈ [lo, hi]".
- **1.13.3 Intervals.** *Example:* Merge Intervals (LC 56), framed as **merging overlapping IP ranges / route summarisation**; Insert Interval (LC 57); Meeting Rooms II (LC 253 (P), free alternative on GfG). *Figure:* timeline bars before and after merging; IP ranges drawn on a number line from 10.0.0.0 to 10.0.3.255.
- **Trap box:** `mid = (lo+hi)/2` overflow in C (use `lo + (hi−lo)/2`); comparator returning `a−b` overflow.

### 1.14 Dynamic programming essentials (10 pp) `[SHOULD · 3 d]`
- **1.14.1 From recursion to memo to table.** *Hook:* writing down answers to exam questions you will be asked again. *Example:* Climbing Stairs (LC 70), with a recursion-tree explosion vs a memo table. *Figure:* recursion tree with repeated sub-calls in the same colour, collapsing to a 1-D table.
- **1.14.2 1-D DP.** *Example:* House Robber (LC 198); Coin Change (LC 322); Longest Increasing Subsequence (LC 300). *Figure:* dp array fill animation.
- **1.14.3 2-D DP.** *Example:* Unique Paths (LC 62); LCS (LC 1143); Edit Distance (LC 72), framed as diffing two router configs. *Figure:* LCS grid with arrows showing the traceback path.
- **1.14.4 Knapsack.** *Example:* Partition Equal Subset Sum (LC 416); 0/1 knapsack framed as fitting flows into link bandwidth. *Figure:* knapsack table capacity × items.
- **Scope note:** DP is lighter at network companies, so keep this to essentials; the higher-DP Google SWE track gets a "Further practice" list.

### 1.15 Design-style coding: caches and rate limiters (14 pp) ⚡ signature chapter `[MUST · 4 d]`
- **1.15.1 LRU cache** [S: Microsoft; Amazon NDE "LRU-style"]. *Core:* hash map + doubly linked list gives O(1) get/put. *Hook:* the **ARP cache**: recently used IP→MAC entries stay, stale ones are evicted. *Example:* LC 146 in C (hand-written hash + DLL) and Python (`OrderedDict` and manual). *Figure:* hash map on the left with arrows into a DLL on the right (MRU at head, LRU at tail); the `get(k)` move-to-front shown as 3 steps.
- **1.15.2 LRU with TTL** [S: Microsoft]. *Example:* ARP entries expire after N seconds; lazy expiry on `get` plus a periodic sweep. Design LC 1797 (Authentication Manager) as a TTL warm-up. *Figure:* timeline with insertion times, TTL bars and an "expired" grey zone.
- **1.15.3 Thread-safe cache (follow-up)** [S: Microsoft concurrency follow-up]. *Example:* coarse mutex vs striped locks, as pseudo-code (link to Pillar 7). *Figure:* lock-striping diagram with 4 buckets and 4 locks.
- **1.15.4 LFU cache.** *Example:* LC 460 with frequency buckets. *Figure:* frequency lists 1→2→3, each a DLL.
- **1.15.5 Token-bucket rate limiter** [I: Cisco, Juniper, Arista, Microsoft]. *Core:* tokens refill at rate r up to capacity b; a packet passes if a token is available. *Hook:* policing on a router interface (CIR/CBS) and API throttling. *Example:* `allow(now)` with lazy refill: `tokens = min(b, tokens + (now−last)·r)`; C version with integer microseconds to avoid floats; Python class; test with bursts. *Figure:* bucket graphic (tap filling at r, overflow spill at b, packets taking tokens), plus a time-series plot of tokens over time with packets marked allowed (green) or dropped (red).
- **1.15.6 Leaky bucket, fixed window, sliding-window log and sliding-window counter.** *Example:* Design Hit Counter (LC 362 (P); free alternative "hits in last 300 s" with a deque); Logger Rate Limiter (LC 359 (P)). *Figure:* comparison panel of the 4 algorithms on the same request trace, showing the fixed-window boundary burst problem.
- **1.15.7 Design HashMap and HashSet.** *Example:* LC 706 and 705 in C. *Figure:* reuse the bucket diagram.
- **1.15.8 Consistent hashing (ECMP and load balancers).** `[OPTIONAL]` *Example:* a hash ring with virtual nodes; add and remove a server and count remapped keys. *Figure:* ring with servers A, B, C and virtual nodes, with keys mapped clockwise.
- **1.15.9 Insert/Delete/GetRandom O(1)** `[OPTIONAL]` (LC 380), as a random backend picker.
- **Trap box:** forgetting to update the map on eviction; float drift in token refill; using wall-clock time instead of a monotonic clock (`CLOCK_MONOTONIC`, `time.monotonic()`).

### 1.16 Finite-state machines (6 pp) `[SHOULD · 1.5 d]`
- **Core:** A protocol is a set of states, events and transitions; encode it in a table. *Hook:* a traffic light. Reports name state machines for [S: Juniper, Broadcom].
- **Example:** a simplified **TCP connection FSM** (CLOSED, LISTEN, SYN_SENT, SYN_RCVD, ESTABLISHED, FIN_WAIT_1, FIN_WAIT_2, TIME_WAIT, CLOSE_WAIT, LAST_ACK). Given a list of events (`APP_ACTIVE_OPEN`, `RCV_SYN_ACK` …), return the final state or "ERROR". Version 1 uses switch-case; version 2 uses a 2-D transition table `next[state][event]`; version 3 uses a function-pointer table (links to §2.5). Second example: Valid Number (LC 65) as a DFA.
- **Figures:** (1) a TCP state diagram, cleanly redrawn with client path in blue and server path in green; (2) a transition-table heat-grid of states × events, with invalid cells hatched.
- **Trap box:** missing default/error state; enum-to-string mismatch.

### 1.17 Testing your own code and interview performance (4 pp) `[MUST · 0.5 d]`
- **Core:** List edge cases before you run anything. *Example:* an edge-case checklist applied to the LPM trie (empty table, /0 only, /32 host routes, duplicate inserts, overlapping prefixes). *Figure:* "edge-case radar" checklist graphic (empty, one, max, min, duplicates, negative, overflow, malformed).
- Includes how to narrate, how to recover from a bug, and when to ask clarifying questions (e.g. "Are IPs given as strings or integers?").

### 1.18 Pillar capstone: mock OAs (6 pp) `[SHOULD · 2 d]`
- Three full timed mock OAs (Cisco-style, Juniper-style, Arista-style) built from this pillar's problems, with model solutions in the appendix. *Figure:* score-tracker table template.

---

## Company-tag matrix, Pillar 1
Legend: ●●● very high · ●● high · ● relevant · ○ low. (S) means at least one report names the topic for that company; (I) means inferred.

| Section | Cisco | Qualcomm | Google | Microsoft | Amazon NDE | Juniper | Arista | Nokia | Broadcom |
|---|---|---|---|---|---|---|---|---|---|
| 1.1 Complexity & routine | ●● | ●● | ●●● | ●●● | ●● | ●● | ●● | ●● | ●● |
| 1.2 Arrays, windows | ●●(S) | ● | ●●● | ●●● | ●●(S) | ●●●(S) | ●●(S) | ●● | ●●(S) |
| 1.3 Hashing | ●● | ● | ●●●(S) | ●●● | ●● | ●● | ●● | ●● | ● |
| 1.4 Strings & IP parsing | ●●●(S) | ● | ●●●(S) | ●● | ●●(S) | ●●(S) | ●● | ●● | ●(S) |
| 1.5 Bits & subnets | ●●●(S) | ●●●(S) | ●● | ● | ●●(I) | ●●●(S) | ●●(I) | ●● | ●●●(S) |
| 1.6 Linked lists in C | ●● | ●● | ● | ●● | ● | ●●●(S) | ●●●(S) | ●●●(S) | ●●●(S) |
| 1.7 Stacks/queues/rings | ●● | ●●(I) | ●● | ●● | ● | ●●(S) | ●● | ●●(S) | ●●(S) |
| 1.8 Trees/BST | ●● | ●● | ●●● | ●●● | ●●(S) | ●●(S) | ●●●(S) | ●● | ● |
| 1.9 Tries & LPM | ●●(I) | ● | ●●●(S) | ●● | ●(I) | ●●(I) | ●●(I) | ● | ●(I) |
| 1.10 Heaps | ● | ○ | ●●● | ●● | ●● | ● | ● | ● | ○ |
| 1.11 Graphs | ●●●(S) | ● | ●●● | ●●● | ●●(S) | ●● | ●● | ●●(S) | ○ |
| 1.12 Backtracking | ● | ○ | ●● | ●● | ● | ● | ● | ● | ○ |
| 1.13 Sorting/search/intervals | ●● | ●● | ●●● | ●●● | ●● | ●● | ●● | ●● | ●● |
| 1.14 DP | ● | ● | ●●● | ●●● | ● | ● | ● | ● | ○ |
| 1.15 LRU/rate limiter | ●●(I) | ●(I) | ●● | ●●●(S) | ●●(S) | ●●(I) | ●●(I) | ● | ● |
| 1.16 FSMs | ●●(I) | ●●(I) | ● | ● | ● | ●●●(S) | ●●(I) | ●(I) | ●●(S) |

## Curated problem list, Pillar 1
(LC = LeetCode number; GfG = GeeksforGeeks practice title. Company tags follow §0.2.)

### Tier A: warm-up (do all; ~35)
| # | Problem | Topic | Tags |
|---|---|---|---|
| 1 | LC 1 Two Sum | hash | [S: Cisco] |
| 2 | LC 88 Merge Sorted Array | two-pointer | [S: Juniper] |
| 3 | LC 189 Rotate Array | array | [S: Juniper] |
| 4 | LC 1108 Defanging an IP Address | string | networking |
| 5 | LC 20 Valid Parentheses | stack | |
| 6 | LC 206 Reverse Linked List | LL | [S: Broadcom] |
| 7 | LC 21 Merge Two Sorted Lists | LL | [S: Arista] |
| 8 | LC 141 Linked List Cycle | LL | [S: Juniper, Nokia] |
| 9 | LC 160 Intersection of Two Linked Lists | LL | [S: Nokia] |
| 10 | LC 203 Remove Linked List Elements | LL | [S: Arista] |
| 11 | LC 237 Delete Node in a Linked List | LL | [S: Arista] |
| 12 | LC 83 Remove Duplicates from Sorted List | LL | |
| 13 | GfG "Remove duplicates from a sorted circular linked list" | LL | [S: Arista] |
| 14 | GfG "Reverse a Doubly Linked List" | DLL | [S: Arista] |
| 15 | LC 191 Number of 1 Bits | bits | [S: Qualcomm] |
| 16 | LC 461 Hamming Distance / LC 2220 Minimum Bit Flips to Convert Number | bits | [S: Qualcomm] |
| 17 | LC 231 Power of Two | bits | |
| 18 | LC 136 Single Number | bits | |
| 19 | LC 268 Missing Number | bits | |
| 20 | LC 190 Reverse Bits | bits | [I: Qualcomm, Broadcom] |
| 21 | GfG "Multiply two integers without using multiplication operator" | bits | [S: Juniper] |
| 22 | LC 338 Counting Bits | bits/DP | |
| 23 | LC 104 Maximum Depth of Binary Tree | tree | |
| 24 | LC 226 Invert Binary Tree | tree | |
| 25 | LC 700 / 701 Search / Insert into a BST | BST | [S: Arista] |
| 26 | LC 704 Binary Search | search | |
| 27 | LC 70 Climbing Stairs | DP | |
| 28 | LC 232 Implement Queue using Stacks | queue | |
| 29 | LC 155 Min Stack | stack | |
| 30 | LC 14 Longest Common Prefix | string/trie | [I: Google] |
| 31 | LC 165 Compare Version Numbers | string | networking |
| 32 | LC 217 Contains Duplicate | hash | |
| 33 | LC 242 Valid Anagram | hash | |
| 34 | LC 876 Middle of the Linked List | LL | |
| 35 | Custom: "Are two IPs in the same subnet?" (book exercise) | bits | [I: Cisco] |

### Tier B: core (~45)
| # | Problem | Topic | Tags |
|---|---|---|---|
| 1 | LC 3 Longest Substring Without Repeating Characters | window | [S: Cisco] |
| 2 | LC 468 Validate IP Address | string | networking, [I: Cisco, Amazon, Microsoft] |
| 3 | LC 93 Restore IP Addresses | backtracking | networking |
| 4 | LC 809 Expressive Words | string | [S: Cisco OA] |
| 5 | LC 8 String to Integer (atoi) | string | [I: Qualcomm, Broadcom] |
| 6 | LC 443 String Compression | string | |
| 7 | LC 49 Group Anagrams | hash | |
| 8 | LC 128 Longest Consecutive Sequence | hash | |
| 9 | LC 560 Subarray Sum Equals K | prefix | |
| 10 | LC 238 Product of Array Except Self | array | |
| 11 | LC 53 Maximum Subarray | Kadane | |
| 12 | LC 2 Add Two Numbers | LL | [S: Arista] |
| 13 | LC 445 Add Two Numbers II | LL | [S: Arista] |
| 14 | LC 142 Linked List Cycle II | LL | [S: Juniper, Nokia] |
| 15 | LC 19 Remove Nth Node From End | LL | |
| 16 | LC 234 Palindrome Linked List | LL | |
| 17 | LC 138 Copy List with Random Pointer | LL | |
| 18 | LC 622 Design Circular Queue | ring | [I: Arista, Broadcom, Qualcomm] |
| 19 | LC 150 Evaluate Reverse Polish Notation | stack | |
| 20 | LC 739 Daily Temperatures | mono-stack | |
| 21 | LC 102 Binary Tree Level Order Traversal | tree | |
| 22 | LC 98 Validate BST | BST | [S: Arista] |
| 23 | LC 450 Delete Node in a BST | BST | [S: Arista] |
| 24 | LC 235 / 236 Lowest Common Ancestor | tree | |
| 25 | LC 230 Kth Smallest in BST | BST | |
| 26 | LC 208 Implement Trie | trie | [S: Google] |
| 27 | LC 201 Bitwise AND of Numbers Range | bits | networking (common prefix) |
| 28 | LC 371 Sum of Two Integers | bits | [I: Juniper] |
| 29 | LC 137 Single Number II | bits | |
| 30 | LC 347 Top K Frequent Elements | heap | [S: Google (IP frequency)] |
| 31 | LC 215 Kth Largest Element | heap | |
| 32 | LC 200 Number of Islands | graph | |
| 33 | LC 547 Number of Provinces | graph/DSU | [S: Nokia (DFS)] |
| 34 | LC 909 Snakes and Ladders | BFS | [S: Cisco] |
| 35 | LC 133 Clone Graph | graph | |
| 36 | LC 207 / 210 Course Schedule I/II | topo | |
| 37 | LC 684 Redundant Connection | DSU | networking (loops/STP) |
| 38 | LC 1319 Number of Operations to Make Network Connected | DSU | networking |
| 39 | LC 743 Network Delay Time | Dijkstra | networking |
| 40 | LC 56 Merge Intervals | intervals | networking (IP ranges) |
| 41 | LC 57 Insert Interval | intervals | |
| 42 | LC 33 Search in Rotated Sorted Array | search | |
| 43 | LC 322 Coin Change | DP | |
| 44 | LC 300 Longest Increasing Subsequence | DP | |
| 45 | LC 146 LRU Cache | design | [S: Microsoft, Amazon] |

### Tier C: interview-level / stretch (~25)
| # | Problem | Topic | Tags |
|---|---|---|---|
| 1 | Book problem: **Longest-prefix-match router (binary trie)**, C + Python | trie | [S: Google] |
| 2 | Book problem: **CIDR firewall rule evaluator (most specific wins)** | trie/hash | [I: Google, Cisco] |
| 3 | LC 421 Maximum XOR of Two Numbers in an Array | binary trie | |
| 4 | LC 1707 Maximum XOR With an Element From Array | binary trie | |
| 5 | LC 751 IP to CIDR (P); GfG alternative "convert IP range to CIDR blocks" (book) | bits | networking |
| 6 | Book problem: **Token-bucket limiter (integer µs)** | design | [I: Cisco, Juniper, Arista, Microsoft] |
| 7 | Book problem: **LRU cache with TTL (ARP cache) + thread safety discussion** | design | [S: Microsoft] |
| 8 | LC 460 LFU Cache | design | |
| 9 | LC 362 Design Hit Counter (P) / LC 359 Logger Rate Limiter (P); free deque version in book | design | [I: Microsoft] |
| 10 | LC 380 Insert Delete GetRandom O(1) | design | |
| 11 | LC 706 Design HashMap (in C) | design | [I: Arista, Juniper] |
| 12 | LC 787 Cheapest Flights Within K Stops | Bellman–Ford | networking (hop limit) |
| 13 | LC 1192 Critical Connections in a Network | bridges | networking |
| 14 | LC 1584 Min Cost to Connect All Points | MST | |
| 15 | LC 239 Sliding Window Maximum | deque | |
| 16 | LC 76 Minimum Window Substring | window | |
| 17 | LC 23 Merge k Sorted Lists | heap/LL | |
| 18 | LC 25 Reverse Nodes in k-Group | LL | [I: Arista] |
| 19 | LC 297 Serialise and Deserialise Binary Tree | tree | |
| 20 | LC 295 Find Median from Data Stream | heaps | |
| 21 | LC 65 Valid Number (DFA) | FSM | [I: Juniper] |
| 22 | Book problem: **TCP FSM validator (table-driven + function pointers)** | FSM | [S: Juniper (state machines)] |
| 23 | LC 72 Edit Distance | DP | |
| 24 | LC 127 Word Ladder | BFS | |
| 25 | LC 29 Divide Two Integers | bits | [I: Juniper, Qualcomm] |

## Interview question bank, Pillar 1 (34 questions)
| # | Question (as an interviewer would say it) | Diff | Tags |
|---|---|---|---|
| 1 | "Given an array and a target, return indices of two numbers adding to the target. Now do it in O(n)." | E | [S: Cisco] |
| 2 | "Merge two sorted arrays; the first has enough space at the end. No extra array." | E | [S: Juniper] |
| 3 | "Rotate an array right by one. Now by k, in O(1) extra space." | E | [S: Juniper] |
| 4 | "Find the length of the longest substring without repeating characters." | M | [S: Cisco] |
| 5 | "Write a function that tells me whether a string is a valid IPv4 address, IPv6 address, or neither." | M | [I: Cisco, Amazon] |
| 6 | "Given two IPs and a subnet mask, are they in the same subnet? What if the mask is given as a prefix length?" | E | [I: Cisco, Amazon NDE] |
| 7 | "Given 10.20.30.40/22, print the network address, broadcast address, first and last usable host and host count, using bit operations only." | M | [I: Cisco] |
| 8 | "How many bits must be flipped to convert A into B?" | E | [S: Qualcomm] |
| 9 | "Set, clear and toggle the k-th bit of an integer. Write them as macros." | E | [S: Qualcomm] |
| 10 | "Multiply two integers without using the * operator." | M | [S: Juniper] |
| 11 | "Check whether a number is a power of two in one expression." | E | [I: Qualcomm, Broadcom] |
| 12 | "Reverse the bits of a 32-bit unsigned integer. Optimise it if called a million times (lookup table)." | M | [I: Qualcomm, Broadcom] |
| 13 | "Detect a cycle in a singly linked list. Then find where the cycle starts and prove why it works." | M | [S: Juniper, Nokia] |
| 14 | "Two linked lists merge at some node. Find the intersection node in O(1) extra space." | E | [S: Nokia] |
| 15 | "Write, from scratch in C, a function that deletes a node with a given value from a singly linked list. Handle the head." | M | [S: Arista] |
| 16 | "Delete every node whose value equals key." | E | [S: Arista] |
| 17 | "Add two numbers stored as linked lists and return the result as a new list." | M | [S: Arista] |
| 18 | "Reverse a doubly linked list. Now delete a given node from it." | E | [S: Arista] |
| 19 | "Remove consecutive duplicates from a circular linked list." | M | [S: Arista] |
| 20 | "Implement insert, search and delete in a BST. What happens when you insert sorted data?" | M | [S: Arista] |
| 21 | "Find the minimum number of dice throws to finish a snake-and-ladder board." | M | [S: Cisco] |
| 22 | "Solve a graph problem with DFS, without recursion." | M | [S: Nokia] |
| 23 | "Given a log file, extract all IP addresses and print them sorted by how often they occur." | E | [S: Google] |
| 24 | "Given a list of IP prefixes and a target IP, find the longest matching prefix. Which data structure, and what is the lookup complexity?" | H | [S: Google] |
| 25 | "Design an LRU cache with O(1) get and put. Now entries expire after a TTL. Now make it thread-safe." | M→H | [S: Microsoft; Amazon] |
| 26 | "Implement a token-bucket rate limiter: allow(packet_size, now) → bool. What are its parameters in router terms?" | M | [I: Cisco, Juniper, Arista] |
| 27 | "Compare fixed-window and sliding-window rate limiting. Show a request trace where fixed-window fails." | M | [I: Microsoft] |
| 28 | "Given router links with delays, how long until a signal from router K reaches all routers?" (LC 743) | M | [I: Cisco, Google] |
| 29 | "Find every link whose failure would partition the network." | H | [I: Google, Arista] |
| 30 | "Given links being added one at a time, report the first one that creates a loop." | M | [I: Cisco, Juniper] |
| 31 | "Merge overlapping IP address ranges given as start-end strings." | M | [I: Google, Amazon] |
| 32 | "Implement a circular buffer for a producer and a consumer. How do you tell full from empty?" | M | [I: Broadcom, Qualcomm, Arista] |
| 33 | "Given a sequence of TCP events, validate that the connection follows the state machine and report the final state." | M | [S: Juniper (state machines)] |
| 34 | "Find the top 10 source IPs by bytes in a 10 GB flow log that does not fit in memory." | H | [I: Google, Amazon] |

## Trap boxes, Pillar 1 (collected; each appears inline at its section)
1. `1u << 32` / `~0u << 32` is UB, so special-case /0 in mask creation.
2. `x & 1 == 0` precedence bug.
3. Leading-zero octets (`"01"`) and empty segments in IP validation.
4. Deleting the head of a linked list without `**pp` or a dummy node.
5. Freeing a node and then reading `node->next`.
6. Floyd's algorithm: checking `fast->next` before `fast->next->next`.
7. Ring buffer full vs empty ambiguity.
8. BST delete not returning the new subtree root.
9. Forgetting the visited set in graph traversal (a broadcast storm in code form).
10. Dijkstra with a stale-entry check missing (`if d > dist[u] continue`).
11. Binary-search midpoint overflow.
12. LRU: updating the list but not the map, or vice versa, on eviction.
13. Rate limiter: using wall-clock time; float accumulation error.
14. Python recursion limit (1000) on deep DFS; use iteration.
15. Returning a pointer to a local array from a C function.

## One-page cheat-sheet, Pillar 1 (contents)
- **Complexity ladder** with n-limits: 10 → n!, 20 → 2ⁿ, 500 → n³, 10⁴ → n², 10⁶ → n log n, 10⁸ → n.
- **Pattern → trigger phrase table:** "subarray/substring" → sliding window; "sorted" → two pointers/binary search; "top k" → heap; "prefix of IP/strings" → trie; "connectivity/loop" → union–find; "shortest hops" → BFS; "weighted shortest" → Dijkstra; "all combinations" → backtracking; "count ways/min cost" → DP; "O(1) get/put + recency" → hash map + DLL.
- **Bit idioms:** set/clear/toggle/test; `x&(x−1)`; `x&−x`; popcount; power-of-two; align-up `(x+a−1)&~(a−1)`; swap32.
- **Subnet formulas:** mask from prefix; network, broadcast, hosts = 2^(32−p) − 2; same-subnet test; IP ⇄ u32.
- **Linked-list skeletons:** `**pp` delete; reverse; Floyd; dummy-head merge.
- **Graph templates:** BFS (queue + visited); iterative DFS (stack); Dijkstra (heap + stale check); DSU (find with path compression, union by rank).
- **LRU and token-bucket pseudocode** in 6 lines each.
- **Edge-case radar** icons.

## End-of-chapter pack, Pillar 1 (spec)
- **Short notes (≈10 pp):** one ½-page block per section 1.0–1.18. Each block gives: what it is, when to use it (trigger phrases), the template code skeleton in ≤10 lines, the complexity, and one trap.
- **One-page revision sheet:** the cheat-sheet contents listed above, set on one A4 side in a 3-column layout with colour bands per topic.
- **Flashcards (≈120 cards, 9 pp):** for example "Q: popcount trick? A: `x &= x−1` until 0" · "Q: LPM data structure? A: binary trie, O(32) lookup; or per-length hash /32→/0" · "Q: LRU O(1) structure? A: hash map + DLL" · "Q: Floyd: why does reset-to-head find the cycle start? A: a = c + (k−1)(b+c)" · "Q: hosts in /27? A: 30" · "Q: token-bucket refill formula?" · "Q: BFS vs Dijkstra when?" · "Q: Union–find detects…? A: a cycle when an edge joins the same set". Each card carries a section number and a MUST/SHOULD dot.
- **Solved interview problems (≈50 pp):** all 34 question-bank entries solved with template §0.4(c), grouped as Cisco (Q1, 4–7, 21, 28), Juniper (2, 3, 10, 13, 30, 33), Qualcomm (8, 9, 11, 12), Arista (15–20, 32), Google (23, 24, 29, 31, 34), Microsoft/Amazon (25–27), Nokia (14, 22). Each group gets a company spotlight. Tier A/B/C problems are solved in a separate "Problem solutions" section using the same template (Tier A: ~1 pp each; Tier B: ~1.5 pp; Tier C: ~2–3 pp).
- **Self-check quiz:** 20 MCQs in Cisco-OA style (complexity, bit results, subnet maths, data-structure choice), with answers explained.

## Mini-project, Pillar 1: **"mini-FIB": a longest-prefix-match lookup engine**
- **Brief:** a C program (with an optional Python twin) that loads a routing table file (`prefix/len next_hop iface`, ~10 000 lines generated by a provided script), builds a binary trie, answers lookups from a second file, and reports lookups per second.
- **Milestones:** (1) IP/CIDR parser with validation and unit tests; (2) linear-scan baseline; (3) binary trie; (4) per-length hash approach; (5) benchmark table and chart; (6) stretch: an LRU "route cache" in front of the trie with hit-ratio statistics, and deletion of prefixes.
- **Deliverables:** GitHub repo with Makefile, README, benchmark plot, and `valgrind` clean report. This gives the student a talking point in résumé and interviews ("I built a mini FIB…").
- **Figure:** architecture block diagram: `routes.txt → parser → trie ← lookup(ip) ← queries.txt`, with a cache box in front of the trie, plus a benchmark bar chart template.

---

# PILLAR 2: PROGRAMMING (C critical · Python · C++ · Bash)

## Chapter header
- **Title:** *Pillar 2: Speaking Machine: C, Python, C++ and Bash for Network Software*
- **Promise:** "You will predict the output of any tricky C snippet an interviewer puts in front of you, explain padding, endianness and `volatile` with diagrams, parse a real packet in C, and automate a network task in Python and Bash."
- **Prerequisites:** none for Part A (it starts from "hello, world"). The reader needs a Linux machine or WSL2 (Pillar 8 gives setup; a 1-page quick-setup box appears here). For Parts B–D, Part A §2.1–2.5 is recommended.
- **Estimated pages:** ~330 in total: teaching ~160 pp (Part A C ≈ 95, Part B Python ≈ 35, Part C C++ ≈ 15, Part D Bash ≈ 15); full solutions to ~65 tiered exercises at ~1.3 pp ≈ 85 pp; end-of-chapter pack ≈ 85 pp (short notes 12, revision sheet 1, flashcards 10, solved 40-question bank ≈ 55, output-prediction answer key 7).
- **Weeks to study:** **7 weeks** at 2 h/day: weeks 1–4 C (§2.1–2.16); week 5 Python; week 6 C++ and Bash; week 7 revision with output-prediction drills plus the mini-project. Fast track ⚡ (3 weeks): §2.2, 2.4–2.6, 2.8–2.10, 2.13, 2.17–2.18, 2.23.

## Why this pillar matters (opening spread, 2 pp)
- Network operating systems and data planes are written largely in C and C++ (Linux kernel networking, Junos on FreeBSD, Arista EOS on Linux, vendor SDKs for switch ASICs). Automation (Amazon NDE, Google NetEng) is mostly Python. Day-to-day operations need Bash. Phrase this as background, with no company-internal claims.
- *Figure:* a "language stack" layer diagram: ASIC/NIC firmware (C) → kernel/drivers (C) → control-plane daemons such as routing protocols (C/C++) → management and automation (Python, Go) → operator shell (Bash). Each layer shows example artefacts.

## Learning objectives
1. Compile, link, run and debug a multi-file C program on Linux using `gcc`, `make`, `gdb`, `valgrind` and sanitisers.
2. State the sizes, ranges and promotion rules of C integer types and avoid signed/unsigned and overflow traps. Use `<stdint.h>` fixed-width types.
3. Read and write pointer code confidently: arithmetic, arrays vs pointers, pointer to pointer, `const` placement, `void *`, function pointers and dispatch tables.
4. Draw the memory layout of a running C program (text, rodata, data, BSS, heap, stack) and say where every variable lives.
5. Use `malloc/calloc/realloc/free` correctly, and find leaks, double frees and use-after-free errors with tools.
6. Explain storage classes and qualifiers (`static`, `extern`, `const`, `volatile`, `register`, `inline`, `restrict`) with use cases.
7. Compute `sizeof` for any struct by hand: padding, alignment, packing, bitfields, unions. Explain why network headers need care.
8. Explain endianness and network byte order. Detect host endianness. Implement byte swaps and use `htons/htonl/ntohs/ntohl`.
9. Use the preprocessor safely: macro pitfalls, `#`/`##`, include guards, `offsetof`, `container_of`, X-macros.
10. Implement the standard string and memory functions (`strlen`, `strcpy`, `strcmp`, `memcpy`, `memmove`, `memset`) and explain buffer overflows.
11. Recognise undefined, unspecified and implementation-defined behaviour, and answer output-prediction questions.
12. Build reusable C data structures (generic list, hash table, ring buffer) and parse a packet from raw bytes, including the internet checksum.
13. Write idiomatic Python for parsing logs and CLI output, using `re`, `collections`, `ipaddress`, `struct`, `json`, `csv`, `argparse` and `subprocess`.
14. Use C++ classes, RAII, references, virtual dispatch (vtable), STL containers and smart pointers at interview depth.
15. Write safe Bash scripts with pipes, text tools (`grep`, `awk`, `sed`, `cut`, `sort`, `uniq`), loops, functions and exit codes.

## Section-by-section outline

### PART A: C (the critical language)

#### 2.1 Toolchain: from source to running process (7 pp) `[MUST · 1.5 d]`
- **2.1.1 The four stages.** *Core:* preprocess → compile → assemble → link. *Hook:* a recipe goes from shopping list to prepared ingredients to cooked dish to plated meal. *Example:* `gcc -E`, `-S`, `-c`, then link `main.c util.c`; inspect with `nm`, `objdump -d`, `file`. *Figure:* pipeline diagram with file artefacts at each arrow (`.c → .i → .s → .o → a.out`) and the tool name under each arrow.
- **2.1.2 Warnings and sanitisers.** *Example:* compile a buggy program with `-Wall -Wextra -Werror -g -fsanitize=address,undefined` and read the ASan report. *Figure:* annotated ASan output screenshot recreated as a styled terminal block with callouts.
- **2.1.3 Make.** *Example:* a 10-line Makefile with `CFLAGS` and pattern rules. *Figure:* dependency graph of targets.
- **2.1.4 gdb in 10 commands.** *Example:* debug a segfault in a linked-list delete with `break`, `run`, `bt`, `print *node`, `watch`. This matches the Arista report of editing, compiling and running on the Linux CLI [S: Arista]. *Figure:* terminal transcript with highlighted commands.
- **2.1.5 valgrind.** *Example:* leak report for a list that is never freed. *Figure:* "definitely lost" block diagram.

#### 2.2 Types, integers and conversions (8 pp) `[MUST · 2 d]`
- **2.2.1 Sizes and ranges.** *Core:* sizes are platform-dependent; `int` is not always 32 bits. *Example:* print `sizeof` for all basic types on LP64 and compare with ILP32. *Figure:* table plus bar graphic of byte widths for LP64 vs ILP32 vs LLP64 (Windows).
- **2.2.2 `<stdint.h>` and `<inttypes.h>`.** *Example:* `uint8_t`, `uint16_t`, `uint32_t` for header fields; `PRIu32` printing. *Figure:* "use this, not that" two-column panel.
- **2.2.3 Integer promotion and the usual arithmetic conversions.** *Core:* small types become `int`; signed meets unsigned → unsigned. *Example:* `unsigned int a = 1; int b = -1; if (b < a)` is false; `uint8_t x = 200, y = 100; x + y` → 300 (int). *Figure:* conversion-rank ladder diagram with arrows.
- **2.2.4 Overflow.** *Core:* unsigned wraps (defined); signed overflow is UB. *Example:* a 32-bit byte counter wrap and computing the delta correctly with unsigned subtraction. *Figure:* a 32-bit odometer wheel wrapping from 0xFFFFFFFF to 0.
- **2.2.5 char signedness and characters.** *Example:* `char c = 0xFF; printf("%d", c);` differs between x86 and ARM. *Figure:* two-column result table.
- **2.2.6 Floating point in brief.** `[OPTIONAL]` Why routers avoid floats in the fast path; `0.1+0.2 != 0.3`.
- **Trap box:** `for (unsigned i = n-1; i >= 0; i--)` loops forever; `sizeof(arr)/sizeof(arr[0])` gives the wrong answer on a pointer parameter.

#### 2.3 Operators, expressions and bitwise C (5 pp) `[MUST · 1 d]`
- Revisits §1.5 in C form. *Core:* precedence and sequence points. *Example:* precedence table drill: `*p++`, `++*p`, `*++p`, `a & b == c`, `x << 1 + 1`. *Figure:* precedence "pyramid" from postfix at the top to comma at the bottom, with the 6 most-confused rows highlighted.
- *Example 2:* register manipulation: given a 32-bit control register, set bits 4–7 to value 0xA without disturbing the others: `reg = (reg & ~(0xFu << 4)) | (0xAu << 4);` [S: Qualcomm, Broadcom bit-level C]. *Figure:* 32-bit register strip with the field outlined, showing the clear mask and set value as separate rows.

#### 2.4 Pointers I: addresses, arrays and arithmetic (10 pp) ⚡ `[MUST · 3 d]`
- **2.4.1 What a pointer is.** *Hook:* a house address written on a card is not the house. *Example:* `int x = 5; int *p = &x; *p = 7;`, printing `&x`, `p`, `*p`, `&p`. *Figure:* memory diagram with two cells (`x` at 0x7ffc10, value 5→7; `p` at 0x7ffc18, value 0x7ffc10) and an arrow from p to x.
- **2.4.2 Pointer arithmetic scales by type.** *Example:* `int *p; p+1` advances 4 bytes; `char *` advances 1 byte; walk a byte buffer as `uint8_t *`. *Figure:* byte strip with `char*` steps (1) above and `int*` steps (4) below.
- **2.4.3 Arrays vs pointers.** *Core:* an array name decays to a pointer except under `sizeof`, `&` and string-literal initialisation. *Example:* `char a[] = "hi"` vs `char *p = "hi"`: `sizeof`, modifiability, and where each lives. *Figure:* a stack array box vs a pointer pointing into `.rodata`.
- **2.4.4 Multi-dimensional arrays and arrays of pointers.** *Example:* `int m[3][4]` vs `int *m[3]` vs `int (*m)[4]`, and how to pass each to a function. *Figure:* row-major layout strip with row boundaries; the pointer-array fan-out diagram.
- **2.4.5 Pointer to pointer.** *Example:* a function that allocates and returns via an out-parameter, `int alloc_buf(uint8_t **out, size_t n)`; links back to `**pp` list deletion (§1.6.2) [S: Arista]. *Figure:* three-level chain `pp → p → x` with addresses.
- **2.4.6 Reading declarations (the clockwise/spiral rule).** *Example:* decode `char *(*f[3])(int)`. *Figure:* spiral-rule drawing over the declaration.
- **2.4.7 Output-prediction drill set (15 snippets)** [S: Cisco OA pointer MCQs]. *Figure:* each snippet in a card with a "predict, then flip" answer panel.
- **Trap box:** uninitialised pointer; returning the address of a local; `sizeof(p)` vs `sizeof(*p)`; comparing pointers into different arrays.

#### 2.5 Pointers II: `const`, `void *`, function pointers and callbacks (8 pp) `[MUST · 2 d]`
- **2.5.1 `const` placement.** *Example:* `const int *p`, `int *const p`, `const int *const p`, read right to left. *Figure:* 2×2 grid ("can change pointer?" × "can change pointee?") with lock icons.
- **2.5.2 `void *` and generic code.** *Example:* write a generic `swap(void *a, void *b, size_t n)`; use `qsort` with a comparator for a routing-table array sorted by prefix length (descending) then address. *Figure:* qsort call flow showing comparator callbacks.
- **2.5.3 Function pointers.** *Core:* code has an address too. *Hook:* speed-dial buttons on a phone. *Example:* a **protocol dispatch table**: `handler_t handlers[256]` indexed by IP protocol number (1 ICMP, 6 TCP, 17 UDP) calling `handle_icmp`, `handle_tcp` and `handle_udp`; plus an FSM driven by function pointers (link to §1.16). *Figure:* a table of 256 slots, mostly `NULL`, with three slots pointing to function boxes in the text segment.
- **2.5.4 Callbacks and registration.** *Example:* `register_rx_callback(cb, ctx)` with a context pointer, the pattern used in event loops. *Figure:* sequence diagram: driver → callback → user code.
- **Trap box:** casting function pointers between incompatible types; forgetting the parentheses, so `int *f(int)` is not `int (*f)(int)`.

#### 2.6 Memory layout of a C program (6 pp) ⚡ `[MUST · 1 d]`
- **Core:** every object lives in text, rodata, data, BSS, heap or stack. [S: Arista "memory layout of a program (stack, heap)"].
- **Hook:** a building with floors: code on the ground floor, globals above, a heap growing upwards, a stack growing downwards from the roof.
- **Example:** a program declaring a global initialised int, a global uninitialised int, a static local, a string literal, a malloc'd buffer and a local array. Print their addresses and classify each. Verify with `size a.out` and `/proc/self/maps`.
- **Figures:** (1) a tall vertical address-space diagram from 0x0 to 0x7fff… with segments coloured, arrows showing heap growth up and stack growth down, and each variable from the example pinned in place; (2) a stack-frame close-up during a call: return address, saved frame pointer, locals, arguments.
- **Trap box:** "static variables live on the stack" (they do not); assuming the heap is zeroed.

#### 2.7 Dynamic memory (8 pp) `[MUST · 2 d]`
- **2.7.1 `malloc`, `calloc`, `realloc`, `free`.** *Example:* a growable array of `struct route` using `realloc` with a temporary pointer. *Figure:* before and after `realloc`, showing either in-place growth or a copy to a new block.
- **2.7.2 Bugs.** *Example:* five broken snippets: leak, double free, use-after-free, off-by-one overflow, freeing a non-heap pointer. Run each under ASan or valgrind. *Figure:* a "rogues' gallery" with one card per bug type, icon, symptom and tool that catches it.
- **2.7.3 Implement `aligned_malloc`/`aligned_free`.** A classic embedded/network question [I: Qualcomm, Broadcom, Cisco]. *Example:* over-allocate by `align − 1 + sizeof(void*)`, round up, store the original pointer just before the returned address. *Figure:* byte strip showing the raw block, padding, stored original pointer, and the aligned address on a 64-byte boundary.
- **2.7.4 Memory pools / slab idea.** *Example:* a fixed-size buffer pool for packet buffers with a free list. *Figure:* pool array with a free-list arrow chain threading through unused slots.
- **Trap box:** `p = realloc(p, n)` loses the block on failure; `malloc(n * sizeof *p)` overflow (use `calloc` or check).

#### 2.8 Storage classes and qualifiers (7 pp) ⚡ `[MUST · 2 d]`
- **2.8.1 Scope vs lifetime vs linkage.** *Example:* a table of `auto`, `static` local, `static` global, `extern`, and `register` with where each lives, its default value and visibility [S: Cisco, Broadcom static/global questions]. *Figure:* matrix graphic with icons for file scope vs block scope.
- **2.8.2 `static` local: counting calls.** *Example:* `int next_id(void){ static int id; return ++id; }`. *Figure:* timeline of calls showing a persistent value.
- **2.8.3 `extern` and multi-file programs.** *Example:* a global config defined in `config.c` and declared in `config.h`. *Figure:* two files linked by an arrow through the header.
- **2.8.4 `volatile`** [S: Cisco, Qualcomm]. *Core:* it tells the compiler that the value can change outside the program's control, so every access must be re-read. *Hook:* checking the letterbox each time instead of remembering it was empty. *Examples:* (a) polling a memory-mapped NIC status register: `while (!(*(volatile uint32_t*)STATUS & RX_READY));`; (b) a flag set by a signal handler (`volatile sig_atomic_t`); (c) show the `-O2` assembly with and without `volatile`, where the loop is hoisted into an infinite loop. *Figure:* side-by-side code → assembly panels with the hoisted load highlighted; CPU ↔ device register diagram with the cache/compiler "shortcut" crossed out.
- **2.8.5 `const volatile`.** *Example:* a read-only hardware status register. *Figure:* annotated register map.
- **2.8.6 `volatile` is not atomic or a memory barrier.** Brief, links to Pillar 7.
- **2.8.7 `inline` and `restrict` (awareness level).** `[OPTIONAL]`
- **Trap box:** using `volatile` for thread synchronisation; `static` in a header creating per-file copies.

#### 2.9 Structs, unions, padding, packing and bitfields (12 pp) ⚡ signature section `[MUST · 3 d]`
- **2.9.1 Struct basics.** Declaration, `typedef`, designated initialisers, passing by pointer.
- **2.9.2 Alignment and padding** [S: Qualcomm, Cisco]. *Core:* each member sits at an offset that is a multiple of its alignment, and the struct size rounds up to the largest alignment. *Hook:* parking cars in bays that only start at certain markings. *Example:* compute by hand, then verify with `sizeof` and `offsetof`: (a) `struct { char a; int b; short c; }` → 12; (b) the reordered `struct { int b; short c; char a; }` → 8; (c) `struct { char a; double d; char c; }` → 24 on x86-64; (d) the **Qualcomm-reported mixed short/long/char** struct on LP64 vs ILP32; (e) nested structs and arrays of structs. *Figure:* **byte-grid memory diagram for each struct**: 1 row = 4 or 8 bytes, member bytes in distinct colours, padding bytes cross-hatched grey and labelled "pad", offsets above each column, total size on the right. Before/after reordering shown as a pair.
- **2.9.3 Size of a struct without `sizeof`** [S: Qualcomm]. *Example:* `(char*)(&s + 1) − (char*)&s`, and `((struct T*)0) + 1` (explain why it is technically UB and when interviewers accept it). *Figure:* two consecutive structs in an array with the pointer difference bracketed.
- **2.9.4 `#pragma pack` / `__attribute__((packed))`.** *Core:* removes padding at the cost of unaligned access. *Example:* a packed `struct ipv4_hdr` (20 bytes) and why unaligned access can fault on some architectures; the `memcpy` safe-read idiom. *Figure:* the same struct packed vs unpacked, with the unaligned 4-byte field straddling a word boundary highlighted in red.
- **2.9.5 Bitfields.** *Example:* `struct { unsigned version:4; unsigned ihl:4; }` for the first IPv4 byte; why bit order is implementation-defined, so production code uses masks and shifts instead. *Figure:* the IPv4 header first byte with nibble boundaries shown in both possible bitfield orders.
- **2.9.6 Unions.** *Core:* all members share the same storage. *Example:* (a) struct vs union `sizeof` [S: Qualcomm]; (b) a tagged union for a message type (`enum type; union { arp_t; icmp_t; }`); (c) a union of `uint32_t` and `uint8_t[4]` to view an IPv4 address bytewise (and the endianness surprise, leading into §2.10). *Figure:* overlapping boxes showing the union members occupying the same bytes, with the size equal to the largest member.
- **2.9.7 Flexible array members.** *Example:* `struct pkt { uint16_t len; uint8_t data[]; };` allocation. *Figure:* header plus a variable tail.
- **2.9.8 Packet Lens: the IPv4 header as a C struct.** *Figure:* RFC 791-style 32-bit-wide header diagram (Version, IHL, DSCP/ECN, Total Length, … Destination Address) with the mapped C field type beside each row.
- **Trap box:** assuming `sizeof(struct)` = sum of members; comparing structs with `memcmp` (padding garbage); sending structs over the wire unpacked (padding and endianness).

#### 2.10 Endianness and network byte order (6 pp) ⚡ `[MUST · 1.5 d]`
- **Core:** multi-byte values are stored most significant byte first (big-endian, "network order") or least significant byte first (little-endian, x86/most ARM configurations). [S: Cisco endianness.]
- **Hook:** writing dates as YYYY-MM-DD vs DD-MM-YYYY. Both are fine until two systems swap files.
- **Examples:** (a) **detect endianness** with a `uint16_t` and a `char*` cast, and with a union; (b) implement `swap16` and `swap32` with shifts and masks, comparing with `__builtin_bswap32`; (c) correct use of `htons(port)` and `htonl(INADDR_ANY)` in a `sockaddr_in` (preview of Pillar 7); (d) a bug hunt where a port 8080 is sent without `htons` and the server listens on 36895; (e) `inet_pton`/`inet_ntop`.
- **Figures:** (1) the value 0x0A0B0C0D laid out in 4 memory cells at addresses 0x100–0x103, with a big-endian row and a little-endian row and the bytes colour-matched; (2) a wire diagram: host (LE) → `htonl` → wire (BE) → `ntohl` → host (BE or LE), with byte boxes at each stage; (3) the port-8080 bug: 0x1F90 vs 0x901F.
- **Trap box:** applying `htonl` twice; byte-swapping single-byte fields; assuming bitfields follow byte order.

#### 2.11 The preprocessor (6 pp) `[SHOULD · 1.5 d]`
- **2.11.1 Macro pitfalls** [S: Cisco "macros"]. *Example:* `#define SQUARE(x) x*x` with `SQUARE(1+2)` → 5; with parentheses but `SQUARE(i++)` → double increment (UB); the `do { } while (0)` idiom for multi-statement macros. *Figure:* expansion "before → after" panels with the substituted tokens highlighted.
- **2.11.2 `#` and `##`.** *Example:* stringify and token-paste to generate `handle_tcp`/`handle_udp` names.
- **2.11.3 Include guards and `#pragma once`.**
- **2.11.4 Conditional compilation.** *Example:* `#ifdef DEBUG` logging; per-architecture endianness macros.
- **2.11.5 X-macros.** *Example:* one list of TCP states generating both the `enum` and a `state_name[]` string table (ties to §1.16). *Figure:* one source list fanning out to two generated artefacts.
- **2.11.6 `offsetof` and `container_of`.** *Example:* recover the parent `struct sk_buff_like` from an embedded `struct list_head` pointer. *Figure:* struct box with an embedded member; the arrow back to the struct start is labelled `ptr − offsetof(type, member)`.
- **2.11.7 Macro vs inline function.** Comparison table: type safety, debugging, side effects.

#### 2.12 Strings and memory functions in C (7 pp) `[MUST · 2 d]`
- **2.12.1 NUL-terminated strings.** *Figure:* char cells `'1' '0' '.' '0' … '\0'` with an index row.
- **2.12.2 Implement the library.** *Example:* write `my_strlen`, `my_strcpy`, `my_strncpy` (and its non-termination trap), `my_strcmp`, `my_strrev`, `my_atoi`, **`my_memcpy` vs `my_memmove`** (overlap handling with direction choice), `my_memset`. *Figure:* overlapping-copy diagram for `memmove`: source and destination ranges on one strip with forward vs backward copy arrows, showing the corruption when copying forward.
- **2.12.3 Tokenising safely.** *Example:* parse `"GigabitEthernet0/1 is up, line protocol is up"` with `strtok_r` vs manual scanning; `sscanf` for an IPv4 dotted quad with range checks. *Figure:* string with token boundaries and inserted NULs (showing `strtok` mutates the input).
- **2.12.4 Buffer overflows.** *Example:* a `gets`/`strcpy` overflow overwriting a return address (conceptual), then the fix with `fgets`/`snprintf`. *Figure:* stack frame showing a buffer overrunning into the saved return address (links to Pillar 9).
- **Trap box:** modifying a string literal; `strncpy` not terminating; `sizeof` of a `char *` parameter.

#### 2.13 Undefined behaviour and output-prediction mastery (6 pp) ⚡ `[MUST · 1.5 d]`
- **Core:** know the categories (undefined, unspecified, implementation-defined) and say "this is UB" rather than guessing. [S: Cisco pointer output questions; recursion vs infinite loop.]
- **Example:** 20-snippet drill, including `i = i++ + ++i`; `printf("%d %d", i++, i++)`; signed overflow; `sizeof(i++)` (not evaluated); `char *s = "abc"; s[0] = 'x';`; uninitialised local; infinite recursion → stack overflow vs `while(1)`; `switch` fall-through; comma operator; `printf` return value; integer division and modulo with negatives; shifting by ≥ width.
- **Figure:** a classification chart (three columns: UB / unspecified / impl-defined), with each snippet placed as a sticky note; plus a recursion-depth illustration showing stack frames until the guard page.

#### 2.14 Data structures in C, production style (8 pp) `[SHOULD · 2 d]`
- **2.14.1 Generic singly linked list with `void *`.** *Example:* API `list_push`, `list_find(cmp)`, `list_free(free_fn)`.
- **2.14.2 Intrusive list (`list_head`).** *Example:* a minimal Linux-style list with `container_of`.
- **2.14.3 Hash table with chaining: a MAC learning table.** *Example:* key = 6-byte MAC, value = port + timestamp; FNV-1a hash; learn, lookup and age-out. *Figure:* bucket array with chains; one entry expanded to show its fields.
- **2.14.4 Lock-free-ish SPSC ring buffer.** `[OPTIONAL]` *Example:* power-of-two ring with head and tail indices (concept only; atomics in Pillar 7). *Figure:* producer and consumer arrows around a ring.
- **2.14.5 API design and error handling in C.** Return codes, `errno`, out-parameters; a consistent naming convention.

#### 2.15 Concurrency primer in C (4 pp) `[SHOULD · 1 d]`
- Bridge to Pillar 7. *Core:* threads share memory, so races need locks. [S: Arista mutex and deadlock prevention questions.] *Example:* two `pthread`s incrementing a counter without and then with a mutex; a deadlock with two mutexes and the lock-ordering fix. *Figures:* interleaving timeline showing a lost update (Thread A and B rows, read/modify/write boxes); a cycle diagram for deadlock (T1 holds L1 and wants L2; T2 holds L2 and wants L1).

#### 2.16 Capstone C: parse a packet from bytes (8 pp) ⚡ `[SHOULD · 2.5 d]`
- **Core:** a packet is a byte array; headers are views at offsets.
- **Example:** given a hex dump of an Ethernet + IPv4 + UDP frame (supplied as a `uint8_t[]`): (1) parse dst/src MAC and EtherType (0x0800) with `ntohs`; (2) parse IPv4 version, IHL, total length, TTL, protocol, src and dst (`inet_ntop`); (3) validate IHL ≥ 5 and length bounds; (4) compute and verify the **internet checksum (RFC 1071)**: one's-complement sum of 16-bit words, folding the carries; (5) parse UDP ports and length; (6) print a `tcpdump`-like one-liner. Bounds-checked with no packed-struct casts (the `memcpy` approach), and a second version using packed structs for comparison.
- **Figures:** (1) a hex dump with byte ranges bracketed and labelled (Ethernet 0–13, IPv4 14–33, UDP 34–41, payload); (2) a nested-header "Russian doll" diagram; (3) a checksum worked table of 16-bit words, the running sum, the carry fold and the final complement.

### PART B: PYTHON (for interviews and automation)

#### 2.17 Python essentials, fast (8 pp) `[MUST · 1.5 d]`
- **2.17.1 Running Python; REPL; virtual environments (`python -m venv`).**
- **2.17.2 Core types and their costs.** *Example:* list vs tuple vs dict vs set, with Big-O of common operations. *Figure:* operation-cost table with green/amber/red cells.
- **2.17.3 Names, references and mutability.** *Hook:* name tags on luggage. *Example:* `a = [1]; b = a; b.append(2)`; the mutable default argument trap; `is` vs `==`. *Figure:* name → object arrow diagram (Python Tutor style).
- **2.17.4 Comprehensions, slicing, unpacking, f-strings.** *Example:* build `{iface: status}` from a list of lines in one comprehension.
- **2.17.5 Functions, `*args/**kwargs`, lambdas, `sorted(key=)`.** *Example:* sort routes by `(−prefixlen, ip)`.
- **2.17.6 Exceptions and `with`.** *Example:* safe file reading; custom `InvalidIPError`.
- **Trap box:** mutable defaults; modifying a list while iterating; integer division `//` vs `/`.

#### 2.18 Parsing text and network data in Python (10 pp) ⚡ `[MUST · 2.5 d]`
- **2.18.1 Regular expressions.** *Example:* regexes for IPv4 (with an octet-range check done in code, not in the regex), MAC, and interface names; named groups. *Figure:* regex railroad diagram for the IPv4 pattern.
- **2.18.2 `collections`.** *Example:* **IP frequency from a log** [S: Google] with `Counter.most_common(10)`; `defaultdict(list)` grouping syslog by host; `deque(maxlen=N)` for last-N lines; `namedtuple`/`dataclass` for a route. *Figure:* data-flow diagram from file through regex to Counter to report.
- **2.18.3 The `ipaddress` module.** *Example:* subnet membership, overlaps (`overlaps`), `collapse_addresses` (summarisation), iterating hosts, IPv6 compression. *Figure:* nested-subnet diagram 10.0.0.0/22 split into four /24s.
- **2.18.4 Parsing CLI output** [S: Amazon NDE Python automation; Google parse-log]. *Example:* parse a provided `show ip interface brief` text block into a list of dicts and report interfaces that are administratively up but protocol down; parse `ping` and `traceroute` output for loss and RTT. *Figure:* fixed-width text block with column boundaries drawn, mapped to a JSON object.
- **2.18.5 JSON, CSV and YAML.** *Example:* convert an inventory CSV to JSON; read a YAML config (PyYAML). Bridge to Pillar 10.
- **2.18.6 Large files.** *Example:* stream a 10 GB log line by line with generators; memory comparison. *Figure:* memory-over-time graph, `readlines()` vs a generator.

#### 2.19 Python for coding interviews (7 pp) `[MUST · 1.5 d]`
- **Core:** know the standard library that replaces hand-written data structures. *Examples:* `heapq` (min-heap, tuples, `nlargest`); `deque` for BFS; `bisect` for range lookup; `OrderedDict.move_to_end` for LRU; `functools.lru_cache` for memoised DP; `itertools` (`combinations`, `accumulate`, `groupby`); `sys.setrecursionlimit` and why to avoid it.
- **Figure:* "Python STL cheat-card" grid: task → module → one-line call → complexity.
- **Example problem:** LRU (LC 146) in 12 lines with `OrderedDict`, then the manual DLL version the interviewer will ask for next.

#### 2.20 Python OOP, modules and scripting hygiene (5 pp) `[SHOULD · 1 d]`
- *Example:* a `class Device` with `hostname`, `mgmt_ip` and `interfaces`, plus `__repr__` and `@property`; a `Router(Device)` subclass; package layout; `argparse` CLI; `logging` instead of `print`; `if __name__ == "__main__":`. *Figure:* UML-lite class diagram, `Device` ← `Router`, `Switch`.

#### 2.21 Bytes, `struct` and a peek at sockets (5 pp) `[SHOULD · 1 d]`
- *Core:* `bytes` are the Python twin of `uint8_t[]`. *Example:* `struct.unpack('!BBHHHBBH4s4s', data[:20])` to parse the same IPv4 header as §2.16 (`!` = network byte order); compute the checksum in Python; `socket.inet_ntoa`; a 15-line UDP echo client (full sockets in Pillar 7). *Figure:* format-string decoder ring mapping each format character to a header field and byte width.

### PART C: C++ (interview depth)

#### 2.22 C++ for C programmers (15 pp) `[SHOULD · 3 d]`
- **2.22.1 References vs pointers.** *Example:* swap by reference; `const &` parameters. *Figure:* alias diagram.
- **2.22.2 Classes, constructors, destructors and RAII.** *Hook:* a hotel key card that deactivates when you check out. *Example:* `class FileHandle` / `class LockGuard` closing in the destructor. *Figure:* object lifetime timeline with constructor and destructor markers at scope boundaries.
- **2.22.3 Rule of three/five; copy vs move (light).** *Example:* a `Buffer` class with a deep copy; `std::move` into a vector.
- **2.22.4 Inheritance, virtual functions and the vtable.** [Glassdoor C/C++ reports mention polymorphism, virtual functions and the vtable.] *Example:* `class Interface { virtual void send(...) = 0; }` with `EthernetIf`/`LoopbackIf`; `sizeof` with and without virtuals; why the destructor must be virtual. *Figure:* object memory with a vptr pointing to a per-class vtable of function addresses; two derived classes' vtables side by side.
- **2.22.5 STL containers and complexity.** *Example:* `vector`, `deque`, `list`, `map` (red-black tree), `unordered_map`, `set`, `priority_queue`, with `std::map::upper_bound` as a quick LPM-by-range trick. *Figure:* container → underlying structure → complexity table.
- **2.22.6 Smart pointers.** *Example:* `unique_ptr<Node>` linked list; `shared_ptr` cycles and `weak_ptr`. *Figure:* reference-count boxes.
- **2.22.7 C vs C++ interview differences.** `malloc` vs `new`; `struct` vs `class`; overloading; name mangling and `extern "C"`.
- **2.22.8 Templates (awareness).** `[OPTIONAL]` A generic `RingBuffer<T, N>`.
- **Trap box:** object slicing; non-virtual destructor in a base class; iterator invalidation after `vector::push_back`.

### PART D: BASH

#### 2.23 Bash for network engineers (15 pp) `[MUST · 3 d]`
- **2.23.1 Shell fundamentals.** Commands, arguments, quoting (`'` vs `"`), variables, `$?`, `PATH`. *Figure:* annotated command-line anatomy (`command -flags args < in > out 2>&1 | next`).
- **2.23.2 Pipes and redirection.** *Hook:* plumbing pipes joining tools. *Figure:* pipeline of boxes with stdin, stdout and stderr streams drawn as coloured pipes.
- **2.23.3 Text toolkit.** `grep -E`, `cut`, `awk`, `sed`, `sort`, `uniq -c`, `wc`, `head`/`tail -f`, `tr`, `xargs`. *Example:* **count unique source IPs in an access log and show the top 10**: `awk '{print $1}' access.log | sort | uniq -c | sort -rn | head`. *Figure:* each stage's output shown as a mini table under the pipeline.
- **2.23.4 Scripts: variables, `if`, `for`, `while`, functions, arrays, `case`.** *Example:* `ping_sweep.sh 192.168.1.0/24` (loop over hosts 1–254 with `ping -c1 -W1`, run in parallel with `&` and `wait`, print live hosts).
- **2.23.5 Robust scripts.** `set -euo pipefail`, `trap`, `getopts`, quoting `"$@"`, `shellcheck`. *Example:* a config-backup script that scp's files from a list of hosts and logs failures.
- **2.23.6 Networking one-liners.** `ip -br a`, `ss -tulpn`, `dig +short`, `curl -w` timings, `nc -zv` port checks (detailed in Pillar 8). *Figure:* reference card.
- **2.23.7 cron and scheduling.** A health check every 5 minutes.
- **Trap box:** unquoted variables with spaces; `for f in $(ls)`; `[ $a == $b ]` with empty variables; forgetting `pipefail`.

---

## Company-tag matrix, Pillar 2
| Section | Cisco | Qualcomm | Google | Microsoft | Amazon NDE | Juniper | Arista | Nokia | Broadcom |
|---|---|---|---|---|---|---|---|---|---|
| 2.1 Toolchain/gdb | ●● | ●● | ● | ● | ● | ●● | ●●●(S) | ●● | ●● |
| 2.2 Types/conversions | ●●● | ●●● | ● | ● | ○ | ●● | ●● | ●● | ●●● |
| 2.3 Bitwise C | ●●(S) | ●●●(S) | ● | ● | ○ | ●●(S) | ●● | ●● | ●●●(S) |
| 2.4 Pointers I | ●●●(S) | ●●● | ● | ● | ○ | ●● | ●●●(S) | ●●(S) | ●●●(S) |
| 2.5 Function pointers/const | ●● | ●●● | ○ | ● | ○ | ●● | ●● | ●● | ●● |
| 2.6 Memory layout | ●●● | ●●● | ● | ● | ○ | ●● | ●●●(S) | ●● | ●● |
| 2.7 Dynamic memory | ●●●(S) | ●●● | ● | ● | ○ | ●● | ●●●(S) | ●● | ●● |
| 2.8 static/volatile | ●●●(S) | ●●●(S) | ○ | ● | ○ | ●● | ●● | ●● | ●●●(S) |
| 2.9 Struct/union/padding | ●●●(S) | ●●●(S) | ○ | ● | ○ | ●● | ●● | ●● | ●●● |
| 2.10 Endianness | ●●●(S) | ●●● | ● | ● | ●(I) | ●●● | ●●● | ●● | ●●● |
| 2.11 Preprocessor | ●●●(S) | ●●● | ○ | ○ | ○ | ●● | ●● | ●● | ●● |
| 2.12 String/memory functions | ●● | ●●● | ● | ●● | ○ | ●● | ●● | ●● | ●●(S) |
| 2.13 UB/output prediction | ●●●(S) | ●●● | ○ | ● | ○ | ●●(S) | ●●(S) | ●● | ●● |
| 2.14 C data structures | ●● | ●● | ● | ● | ○ | ●●(S) | ●●●(S) | ●● | ●●(S) |
| 2.15 Concurrency primer | ●● | ●● | ● | ●●(S) | ○ | ●● | ●●●(S) | ●● | ●●(S RTOS) |
| 2.16 Packet parsing in C | ●●(I) | ●●(I) | ●(I) | ●(I) | ○ | ●●(I) | ●●(I) | ●●(I) | ●●(I) |
| 2.17–2.21 Python | ●●(S) | ● | ●●●(S) | ●●● | ●●●(S) | ●● | ●● | ●●(S) | ● |
| 2.22 C++ | ●● | ●● | ●●● | ●●● | ● | ●● | ●●(I) | ●●(S) | ●● |
| 2.23 Bash | ●● | ● | ●● | ● | ●●(I) | ●● | ●●(S CLI) | ●●(S JD) | ● |

## Curated problem list, Pillar 2
These are mostly implementation exercises rather than LeetCode, because interviewers write them on a whiteboard.

### Tier A: warm-up (~25)
1. Print `sizeof` of all basic types; explain the LP64 output.
2. Swap two numbers three ways (temp, arithmetic, XOR) and explain why XOR swap fails when both pointers alias.
3. Write SET_BIT / CLEAR_BIT / TOGGLE_BIT / TEST_BIT macros [S: Qualcomm].
4. Count set bits (Kernighan) in C [S: Qualcomm].
5. Detect machine endianness [S: Cisco].
6. Implement `my_strlen`, `my_strcpy`, `my_strcmp`.
7. Reverse a string in place.
8. Write a function using a `static` counter [S: Cisco, Broadcom].
9. Print the addresses of global, static, local, heap and literal objects and classify them [S: Arista].
10. Struct vs union `sizeof` demo [S: Qualcomm].
11. Compute `sizeof` of 10 given structs by hand (worksheet) [S: Qualcomm].
12. Pointer output-prediction set 1 (10 snippets) [S: Cisco].
13. Fix the `SQUARE(x)` macro.
14. `const` pointer quiz (6 declarations).
15. Python: read a file and count lines containing "ERROR".
16. Python: `ipaddress` checks (is 10.1.2.3 in 10.0.0.0/8?).
17. Python: dict comprehension from `show` output lines.
18. Bash: top 10 IPs in an access log.
19. Bash: loop over a hosts file and ping each.
20. C++: class with constructor and destructor that prints; observe scope exit.
21. GfG "Find size of a structure without using sizeof" [S: Qualcomm].
22. GfG "Write a C program to check little or big endian" [S: Cisco].
23. GfG "Difference between structure and union" (explain plus code) [S: Qualcomm].
24. GfG "Static variables in C" output questions [S: Cisco, Broadcom].
25. Implement `swap16` and `swap32`.

### Tier B: core (~25)
1. Implement `my_memcpy` and `my_memmove` with overlap handling.
2. Implement `my_atoi` with whitespace, sign and overflow handling (LC 8).
3. Implement `inet_pton`-lite: dotted quad → `uint32_t` (network order) with validation.
4. Implement `u32_to_dotted(uint32_t ip, char out[16])`.
5. Generic `qsort` comparator for routes (prefix length desc, then address).
6. Function-pointer dispatch table for IP protocol numbers.
7. Singly linked list library (`push`, `pop`, `delete(**pp)`, `reverse`, `free_all`) with valgrind-clean tests [S: Arista].
8. Doubly linked list insert, delete and reverse [S: Arista].
9. Circular buffer (power-of-two) with tests [I: Broadcom, Qualcomm].
10. Register field read/modify/write helper `set_field(reg, shift, width, val)` [S: Broadcom bit-level C].
11. Packed vs unpacked `ipv4_hdr`: print `sizeof` and offsets.
12. Tagged union message decoder.
13. X-macro TCP state enum with string table.
14. `container_of` demo with an intrusive list.
15. MAC learning table (hash + ageing).
16. Pthreads race demo and mutex fix [S: Arista mutex].
17. Python: parse `show ip interface brief` and list up/down mismatches [S: Amazon NDE automation].
18. Python: log → `Counter` → top-k report with `argparse` [S: Google].
19. Python: `struct.unpack` IPv4 header and checksum verify.
20. Python: `collapse_addresses` summarisation of a prefix list.
21. Bash: `ping_sweep.sh` with parallelism and a CIDR argument.
22. Bash: backup script with `set -euo pipefail`, `trap` and logging.
23. C++: `RingBuffer<T,N>` template.
24. C++: polymorphic `Interface` hierarchy; print `sizeof` with and without virtuals.
25. C++: `unordered_map` + `list` LRU.

### Tier C: interview-level / stretch (~15)
1. `aligned_malloc`/`aligned_free` [I: Qualcomm, Broadcom, Cisco].
2. Fixed-size memory pool allocator for packet buffers.
3. Full Ethernet/IPv4/UDP parser from a hex dump with RFC 1071 checksum (§2.16).
4. Bounds-safe TLV (type-length-value) parser that rejects truncated and overlong TLVs.
5. Implement `strtok_r`-like re-entrant tokeniser.
6. Write a `printf`-lite supporting `%d %x %s %c`, using `stdarg.h`.
7. Detect and explain 20 UB snippets (§2.13) under `-fsanitize=undefined`.
8. Demonstrate the `volatile` effect at `-O2` with assembly output [S: Cisco, Qualcomm].
9. "Test the memory bit-cells of a segment in C" (walking-ones/zeros test) [S: Broadcom].
10. Lock-ordering deadlock demo and fix [S: Arista deadlock].
11. Python: a concurrent multi-device reachability checker with `concurrent.futures` and timeouts.
12. Python: a generator-based streaming parser for a 10 GB flow log, top-k by bytes.
13. C++: implement `unique_ptr`-lite (move-only).
14. Bash + awk: a syslog summariser (per-host error counts per hour).
15. Port the §1.9 LPM trie to C++ with `unique_ptr` children.

## Interview question bank, Pillar 2 (40 questions)
| # | Question | Diff | Tags |
|---|---|---|---|
| 1 | "What is the difference between a structure and a union? Give a use case for a union." | E | [S: Qualcomm] |
| 2 | "What is structure padding and why does the compiler do it? Show an example." | E | [S: Qualcomm, Cisco] |
| 3 | "What is `sizeof(struct { char a; int b; short c; })`? Reorder it to minimise size." | M | [S: Qualcomm] |
| 4 | "What is the size of a struct with a short, a long and a char on a 32-bit vs a 64-bit machine?" | M | [S: Qualcomm] |
| 5 | "Find the size of a structure without using `sizeof`." | M | [S: Qualcomm] |
| 6 | "What does `volatile` do? Give a scenario where you must use it." | M | [S: Cisco, Qualcomm] |
| 7 | "Can a variable be both `const` and `volatile`? When?" | M | [S: Qualcomm (const & volatile)] |
| 8 | "Is `volatile` enough for sharing a flag between two threads? Why not?" | H | [I: Arista, Qualcomm] |
| 9 | "Write a program to detect whether your machine is little- or big-endian." | E | [S: Cisco] |
| 10 | "Why do we need `htons`/`htonl`? What breaks if you forget them?" | E | [S: Cisco (endianness)] |
| 11 | "Write a function to swap the byte order of a 32-bit integer without library calls." | M | [I: Cisco, Broadcom] |
| 12 | "Explain the memory layout of a C program. Where do globals, statics, locals, `malloc` memory and string literals live?" | E | [S: Arista] |
| 13 | "Difference between a static global variable, a static local variable and a static function?" | E | [S: Cisco, Broadcom] |
| 14 | "What is wrong with `#define SQUARE(x) x*x`? Fix it. What happens with `SQUARE(i++)`?" | E | [S: Cisco (macros)] |
| 15 | "Macro vs inline function: when would you use each?" | M | [S: Cisco (macros)] |
| 16 | "Predict the output: `int a[] = {1,2,3}; int *p = a; printf("%d %d", *p++, *++p);`" | M | [S: Cisco (pointer output)] |
| 17 | "Explain `const int *p`, `int *const p` and `const int *const p`." | E | [I: Cisco, Qualcomm] |
| 18 | "What is a dangling pointer? A memory leak? How would you find each on Linux?" | E | [S: Cisco (memory allocation)] |
| 19 | "Difference between `malloc` and `calloc`? What does `realloc` do if it cannot grow in place?" | E | [S: Arista (dynamic memory MCQs)] |
| 20 | "Implement `memmove`. Why is `memcpy` not safe for overlapping regions?" | M | [I: Qualcomm, Broadcom] |
| 21 | "Implement an aligned malloc that returns memory aligned to any power of two." | H | [I: Qualcomm, Broadcom] |
| 22 | "Write a function from scratch in C to delete a node from a singly linked list. Now do it without special-casing the head." | M | [S: Arista] |
| 23 | "What are function pointers? Show how you would dispatch packets to handlers by protocol number." | M | [I: Cisco, Juniper] |
| 24 | "What is the difference between recursion and an infinite loop in terms of what eventually happens?" | E | [S: Cisco] |
| 25 | "Is `i = i++ + ++i;` valid C? What will it print?" | E | [I: Cisco, Qualcomm] |
| 26 | "What is `offsetof`? How does `container_of` work?" | H | [I: Arista, Broadcom] |
| 27 | "Can you send a C struct directly over a socket? What could go wrong?" | M | [I: Cisco, Juniper, Arista] |
| 28 | "Bitfields for protocol headers: good idea or not?" | M | [I: Qualcomm, Broadcom] |
| 29 | "What is a mutex? How do you prevent deadlock?" | M | [S: Arista] |
| 30 | "How would you test the memory bit-cells of a memory segment using C?" | H | [S: Broadcom] |
| 31 | "Edit, compile and run this program from the Linux command line. It crashes; debug it." | M | [S: Arista] |
| 32 | "Python: given `show ip interface brief` output as text, return the interfaces that are up/down." | E | [S: Amazon NDE (automation)] |
| 33 | "Python: extract IP addresses from a log and sort them by frequency. What if the file is 50 GB?" | M | [S: Google] |
| 34 | "Python: what is the time complexity of `x in list` vs `x in set`? Why?" | E | [I: Google, Amazon] |
| 35 | "Python: explain the mutable-default-argument bug." | E | [I: Google, Microsoft] |
| 36 | "Tell me about an automation script you wrote: what it did, how you tested it and how it failed." | M | [S: Amazon NDE] |
| 37 | "C++: what is a virtual function and how is it implemented (vptr/vtable)? Why a virtual destructor?" | M | [I: Nokia (C++/OOP), Cisco] |
| 38 | "C++: what is RAII? Give an example with locks or files." | M | [I: Microsoft, Google] |
| 39 | "C++: `map` vs `unordered_map`: implementation and complexity?" | E | [I: Google, Microsoft] |
| 40 | "Bash: one-liner to find the 10 most frequent source IPs in a log; then make it a script with argument checking." | E | [I: Amazon NDE, Google] |

## Trap boxes, Pillar 2 (collected)
1. `sizeof(arr)` on an array parameter is the pointer size.
2. Signed vs unsigned comparison (`-1 > 1u` is true).
3. `unsigned` loop counter counting down to `>= 0`.
4. Signed overflow and shift-by-width UB.
5. `char` signedness differs by platform.
6. Returning the address of a local variable.
7. `p = realloc(p, n)` leaks on failure.
8. Freeing twice; using after free.
9. `volatile` ≠ atomic, ≠ barrier.
10. Unparenthesised macros and macro arguments with side effects.
11. `static` in a header file.
12. `strncpy` without NUL termination; modifying string literals.
13. `memcmp` on structs with padding.
14. Forgetting `htons` on ports; double conversion.
15. Packed-struct unaligned access on strict-alignment CPUs.
16. Python: mutable defaults; `is` vs `==`; modifying a list while iterating.
17. C++: slicing; missing virtual destructor; iterator invalidation.
18. Bash: unquoted variables; missing `pipefail`; `for f in $(ls)`.

## One-page cheat-sheet, Pillar 2 (contents)
- **C type sizes** (LP64 vs ILP32) and `<stdint.h>` map.
- **Precedence top 10** with the infamous ones (`*p++`, `&` vs `==`, `<<` vs `+`).
- **Declaration decoder:** `const` placement grid; function-pointer syntax template `ret (*name)(args)`; `typedef` form.
- **Memory layout diagram** (mini) with "who lives where" legend.
- **Storage-class table:** scope, lifetime, linkage, default value.
- **Padding rule in three lines** plus a worked mini example; `offsetof`/`container_of` macros.
- **Endianness card:** 0x0A0B0C0D in BE and LE; `htons/htonl/ntohs/ntohl`; `inet_pton/ntop`.
- **Safe macro rules:** parenthesise everything; `do{}while(0)`; never pass side effects.
- **Memory bug → tool map:** leak → valgrind; overflow/UAF → ASan; UB → UBSan; crash → gdb `bt`.
- **Python quick-ref:** `Counter`, `defaultdict`, `deque`, `heapq`, `bisect`, `ipaddress`, `re`, `struct` format characters (`! B H I 4s`).
- **C++ quick-ref:** container complexity table; Rule of 0/3/5; smart pointers.
- **Bash quick-ref:** quoting rules; `set -euo pipefail`; the `awk | sort | uniq -c | sort -rn | head` idiom; test operators.

## End-of-chapter pack, Pillar 2 (spec)
- **Short notes (≈12 pp):** ½ page per section 2.1–2.23 in bullets, each with a 3–6 line code idiom (e.g. the `**pp` delete, `swap32`, `aligned_malloc` core lines, `struct.unpack('!…')`, `set -euo pipefail` header).
- **One-page revision sheet:** the cheat-sheet above on a single A4 side. The left half is C (types, precedence, declarations, memory map, padding, endianness, macros, bug→tool); the right half is Python, C++ and Bash quick-refs.
- **Flashcards (≈140 cards, 10 pp):** for example "Q: `sizeof(struct{char;int;short})` on x86-64? A: 12" · "Q: `const int *p`: what is const? A: the pointee" · "Q: where does a static local live? A: .data or .bss" · "Q: 0x0A0B0C0D in LE memory? A: 0D 0C 0B 0A" · "Q: Is `volatile` atomic? A: no" · "Q: `memcpy` vs `memmove`?" · "Q: Python `!` in a struct format? A: network (big-endian) order" · "Q: why a virtual destructor?" · "Q: what does `pipefail` do?". Each card carries a section number and priority.
- **Output-prediction answer key (≈7 pp):** all 35 snippets from §2.4.7 and §2.13, each with the answer, the one-line reason, and a UB/impl-defined/defined classification.
- **Solved interview problems (≈55 pp):** all 40 question-bank entries solved with template §0.4(c) (the conceptual-question format for Q1–19, 24–29 and 34–39; the full coding template for 20–23, 30–33 and 40), grouped by company with spotlights: Qualcomm (1–7), Cisco (9–18, 24), Arista (12, 19, 22, 29, 31), Broadcom (13, 30), Amazon NDE (32, 36), Google (33), C++/Python general (34–40). Each Tier A/B/C exercise also has a full solution in the "Exercise solutions" section.
- **Self-check quiz:** 25 C MCQs in Arista- and Cisco-OA style (pointers, dynamic memory, output prediction), with explained answers.

## Mini-project, Pillar 2: **"pktpeek": a tiny packet decoder (C) plus a report tool (Python) plus a runner (Bash)**
- **Brief:** (1) **C:** `pktpeek` reads a classic `.pcap` file (24-byte global header and 16-byte record headers, documented in the chapter) without libpcap. For each frame it decodes Ethernet, IPv4/IPv6 (basic), TCP/UDP/ICMP, verifies IPv4 checksums, and prints a one-line summary. It must be valgrind- and ASan-clean and handle truncated packets safely. (2) **Python:** `pkreport.py` consumes `pktpeek --json` output and prints the top talkers, a protocol mix, and the per-flow (5-tuple) byte count, with optional CSV export. (3) **Bash:** `run.sh` captures 30 s of traffic with `tcpdump -w` (or uses a provided sample pcap), runs both tools, and archives a dated report.
- **Milestones:** pcap header parsing → Ethernet → IPv4 + checksum → L4 → JSON output → Python report → Bash glue → tests with crafted malformed pcaps → README with an architecture diagram.
- **Stretch:** a function-pointer dispatch table for EtherType and IP protocol (§2.5); `--filter "udp port 53"` mini-parser; C++ port with RAII file handles.
- **Figures:** component diagram (Bash runner → C decoder → JSON → Python report); a pcap file-format byte map (global header fields, then repeating record header + data blocks).
- **Interview value:** it lets the student say "I wrote a pcap decoder in C" and answer endianness, padding, bounds-checking and checksum questions from first-hand experience.

---

## Cross-pillar links for the editor
- §1.5 bits ↔ §2.3 bitwise C ↔ Pillar 3 subnetting chapter (share the 192.168.10.77/26 figure).
- §1.6 linked lists ↔ §2.4.5 pointer to pointer ↔ §2.14 intrusive lists ↔ Pillar 7 kernel networking.
- §1.9 LPM trie ↔ Pillar 4 routing table/FIB ↔ Pillar 5 data-centre ECMP (consistent hashing §1.15.8).
- §1.15 token bucket ↔ Pillar 4/5 QoS policing and shaping ↔ Pillar 9 DDoS mitigation.
- §1.16 TCP FSM ↔ Pillar 3 TCP chapter ↔ §2.11 X-macros.
- §2.10 endianness and §2.16 packet parsing ↔ Pillar 7 sockets ↔ Pillar 8 tcpdump/Wireshark.
- §2.18 Python parsing ↔ Pillar 10 automation (Netmiko, NAPALM, TextFSM).
- §2.23 Bash ↔ Pillar 8 Linux tools.

---

## §S Sources (consulted via web search on 2026-10-29)
Note on method: direct page fetches to geeksforgeeks.org and leetcode.com were blocked by this session's network policy. Evidence was taken from search-engine summaries of the pages below. Before printing, an editor should open each page and confirm the quoted problem names. Reports are self-submitted and span roughly 2017–2026.

**Cisco**
- https://www.geeksforgeeks.org/?p=486894 (Cisco Interview Experience 2020: Snake and Ladder; router vs switch; OSI)
- https://www.geeksforgeeks.org/?p=838349 (Cisco Network Engineer On-Campus 2021)
- https://www.geeksforgeeks.org/?p=330663 (Cisco SE On-Campus: HackerRank 2 coding + ~20 MCQs; pointer output questions; bit manipulation; recursion vs infinite loop)
- https://www.geeksforgeeks.org/?p=232415 (Cisco 2+ years experience)
- https://leetcode.com/discuss/interview-experience/1038973/cisco-software-engineer-1-bangalore-jan-2021 (C memory allocation, static/global, structure padding, macros, endianness)
- https://leetcode.com/discuss/interview-experience/1384489/ (Cisco OA 2022 grad: Expressive Words)
- https://www.geeksforgeeks.org/cisco-interview-experience-on-campus-2021/
- https://www.naukri.com/code360/interview-experiences/cisco/cisco-interview-experience-software-developer-aug-2022-exp-0-2-years (Longest substring without repeating characters; Python and CN)
- https://www.glassdoor.com/Interview/Cisco-Interview-E1425-RVW98493976.htm (2-sum)
- https://www.glassdoor.com/Interview/Cisco-Interview-E1425-RVW4319180.htm (volatile scenario)
- https://dev.to/net_programhelp_e160eef28/cisco-hackerrank-online-assessment-2026-real-questions-preparation-guide-4e21 (OA format, subnetting MCQs)
- https://prepinsta.com/cisco/
- https://www.lets-code.co.in/previousyearcodingquestion/cisco-previous-year-coding-questions
- https://www.interviewquery.com/guides/cisco-software-engineer

**Juniper**
- https://www.geeksforgeeks.org/?p=162774 (Set 4 On-Campus)
- https://www.geeksforgeeks.org/juniper-networks-interview-experience-2/amp/ (online test: merge sorted arrays, multiply without *, rotate array, cycle detection)
- https://www.geeksforgeeks.org/juniper-networks-interview-experience-3/
- https://www.geeksforgeeks.org/juniper-interview-experience-set-3-campus/
- https://www.geeksforgeeks.org/?p=1211617 (2.6 years experience)
- https://www.glassdoor.sg/Interview/Juniper-Networks-Interview-E7224-RVW51117152.htm (strings, bit manipulation, linked lists, state machines)
- https://www.interviewquery.com/guides/juniper-networks-software-engineer
- https://www.naukri.com/code360/interview-experiences/juniper-networks/juniper-networks-interview-experience-on-campus-dec-2021-2018

**Qualcomm**
- https://www.geeksforgeeks.org/?p=378323 (Off-Campus Nov 2019: count bits to flip A→B)
- https://www.geeksforgeeks.org/?p=1115092 (SWE On-Campus 2023)
- https://www.geeksforgeeks.org/?p=855480 (On-Campus: struct vs union, structure padding)
- https://www.geeksforgeeks.org/?p=250860 (Off-Campus)
- https://www.geeksforgeeks.org/?p=477855 (SE On-Campus)
- https://www.glassdoor.com.ar/Entrevista/Qualcomm-Entrevista-E640-RVW16345495.htm (sizeof of mixed short/long/char struct)
- https://static.glassdoor.it/Interview/Qualcomm-Interview-E640-RVW100652142.htm (2025: const, volatile, bit manipulation)
- https://leetcode.com/discuss/post/8472889/qualcomm-software-engineer-oncampus-inte-sfli/

**Arista**
- https://www.glassdoor.co.in/Interview/Write-a-function-from-scratch-to-delete-a-node-from-a-singly-linked-list-in-C-They-wrote-a-driver-program-already-so-yo-QTN_2283028.htm (delete node in C; pointer-to-pointer)
- https://www.geeksforgeeks.org/?p=225965 (Internship On-Campus)
- https://www.geeksforgeeks.org/?p=138791 (Set 4)
- https://www.geeksforgeeks.org/?p=154422 (Set 6)
- https://www.geeksforgeeks.org/?p=156099 (Set 7)
- https://leetcode.com/discuss/interview-experience/7064035
- https://www.naukri.com/code360/interview-experiences/arista-networks/interview-experience-on-campus-aug-2022-2-5044
- https://clear.glassdoor.nl/Interview/Arista-Networks-Senior-Software-Engineer-Network-system-Interview-Questions-EI_IE295128.0,15_KO16,55.htm (2026: BST and linked lists on CoderPad)
- https://www.jointaro.com/interviews/companies/arista-networks/experiences/sde-intern-pune-august-29-2025-no-offer-negative-643e2da0/
- https://www.interviewquery.com/guides/arista-networks-software-engineer

**Google**
- https://www.jointaro.com/interviews/companies/google/experiences/senior-swe-hyderabad-may-26-2025-no-offer-positive-0f419753/ (trie: longest prefix match of IPs vs target)
- https://fr.glassdoor.be/Entretien/Python-coding-interview-asking-to-extract-IP-addresses-from-a-log-file-and-sort-them-by-occurrences-QTN_3827018.htm (extract IPs from log, sort by occurrences)
- https://www.glassdoor.co.in/Interview/Google-Interview-E9079-RVW73046674.htm (Network Engineer process)
- https://www.1point3acres.com/interview/thread/1184361 (parsing complex logs, SWE phone screen)
- https://prachub.com/coding-questions/ipv4-cidr-range-membership-queries (CIDR membership approach)
- https://prachub.com/coding-questions/evaluate-ip-access-rules
- https://prachub.com/coding-questions/design-an-ip-filter-using-cidr-rules

**Microsoft**
- https://leetcode.com/discuss/post/8300781/microsoft-senior-se-l63l64-interview-exp-14r4/ (Azure Storage: LRU with TTL and concurrency)
- https://leetcode.com/discuss/interview-experience/427250/ (Azure Bangalore: distributed rate limiter)
- https://leetcode.com/discuss/interview-question/6403987/Microsoft-SDE-2-Recent-questions-2025-or-Consolidated/
- https://www.techinterview.org/post/3233459770/implement-a-rate-limiter/ (token, leaky and sliding-window reference)

**Amazon NDE**
- https://static-pc.glassdoor.de/Interview/Amazon-Network-Development-Engineer-Interview-Questions-EI_IE6036.0,6_KO7,35.htm
- https://www.jointaro.com/interviews/companies/amazon/work-experiences/network-development-engineer-dublin-dublin-may-18-2025-4-91d2d903/
- https://www.jointaro.com/interviews/companies/amazon/work-experiences/network-development-engineer-austin-tx-october-22-2024-2-443f1cee/
- https://www.jointaro.com/interviews/companies/amazon/work-experiences/network-development-engineer-sydney-april-8-2021-4-c6e6ed3e/
- https://static.glassdoor.com.ar/Interview/Amazon-Non-Software-Development-Engineer-Interview-Questions-EI_IE6036.0,6_KO7,40_IP44.htm (OA: LeetCode easy + medium; LRU-style)

**Nokia**
- https://www.jointaro.com/interviews/companies/nokia/experiences/software-engineer-chennai-tamil-nadu-august-7-2024-no-offer-positive-8b1ff41a
- https://www.jointaro.com/interviews/companies/nokia/experiences/software-development-engineer-bengaluru-karnataka-june-1-2021-accepted-offer-positive-045eda07
- https://www.jointaro.com/interviews/companies/nokia/experiences/software-engineer-internship-bhopal-madhya-pradesh-april-1-2025-no-offer-positive-a70ea492
- https://www.interviewquery.com/interview-guides/nokia-software-engineer

**Broadcom**
- https://www.glassdoor.com/Interview/Broadcom-Interview-E6926-RVW58023898.htm
- https://www.glassdoor.co.in/Interview/Broadcom-Interview-E6926-RVW3780027.htm
- https://www.glassdoor.ie/Interview/Broadcom-Interview-E6926-RVW13043050.htm
- https://www.jointaro.com/interviews/companies/broadcom/experiences/engineering-san-diego-ca-january-1-2012-declined-offer-neutral-8e6194ac/ (test memory bit-cells in C)

**General C and problem references**
- https://aticleworld.com/c-interview-questions/3
- https://medium.com/nerd-for-tech/c-interview-questions-01-pointer-c35df76f5252
- https://www.glassdoor.ca/Interview/C-predict-the-output-questions-Stacks-queues-write-programs-endianity-and-byte-allignment-volatile-usage-optimizing-QTN_271827.htm (peer networking-silicon firm: endianness, alignment, volatile)
- https://clear.glassdoor.nl/Interview/volatile-keyword-memory-map-of-C-program-code-to-detect-endianness-c-basics-polymorphism-virtual-functions-how-virt-QTN_1760582.htm (volatile, memory map, endianness, vtable)
- https://designgurus.io/answers/detail/468-validate-ip-address-6valid8ip (LC 468 details)
- https://doocs.github.io/leetcode/en/lc/468
- https://jumpcloud.com/it-index/what-is-longest-prefix-match-lpm
- RFC 791 (IPv4 header) https://www.rfc-editor.org/rfc/rfc791 and RFC 1071 (internet checksum) https://www.rfc-editor.org/rfc/rfc1071 are cited for §2.9.8/§2.16 as standards references. They were not fetched in this session; verify the links.
