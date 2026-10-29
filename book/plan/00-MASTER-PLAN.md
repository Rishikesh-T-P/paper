# Network Engineer Placements 2027 — Master Plan

*A single, self-contained textbook that takes a beginner from first principles to the offer stage for network-engineer and networking-software roles at Cisco, Qualcomm, Google, Microsoft, Amazon, Juniper, Arista, Nokia and Broadcom.*

Status: **plan for approval** (29 October 2026). No chapter text has been written yet.
Detailed plans behind this summary (≈ 115,000 words in total):

| File | Scope | Size |
|---|---|---|
| `pillars-01-02.md` | DSA & coding; C, Python, C++, Bash | 17.9 k words |
| `pillars-03-04.md` | Computer Networks; Routing & Switching (CCNA → CCNP ENCOR) | 18.1 k words |
| `pillars-05-07.md` | Data centre & cloud; Wireless & cellular; OS & sockets | 22.0 k words |
| `pillars-08-12.md` | Linux tools; Security; Automation; Troubleshooting; Supporting subjects | 27.6 k words |
| `cheatcodes-apparatus.md` | Cheat-code layer; end-of-chapter apparatus; company question banks | 16.2 k words |
| `design-production.md` | Design system, figure language, toolchain, schedules, production | 13.0 k words |

---

## 1. What the book promises

Consider a student who has never configured a router and has not yet written a linked list in C. The book is designed so that such a reader, working through it in order, needs no second resource: (i) every concept is explained from first principles with a figure; (ii) every interview question is answered in full inside the book; (iii) every lab prints its expected output, so it can be followed on paper; and (iv) every chapter ends with a Problem Set in which every interview question is solved, and a two-page Revision Spread of short notes, key tables and flashcards. Nothing is printed twice: each concept and each solution has one home, and every other mention is a page reference. Sources are listed for credibility only; the reader is told they are not required reading.

Three design commitments follow from this:

1. **Comprehensive, not condensed.** The book is not trimmed to fit any schedule. Schedules choose a path through it.
2. **Navigable.** Every section carries a `● MUST / ◐ SHOULD / ○ OPTIONAL` badge per track, a difficulty marker (■□□ / ■■□ / ■■■) and a schedule tag (`8w D17 · 3m W5 · 6m W9`), so a reader with eight weeks reads the Must lane and nothing is lost for the reader with six months.
3. **Honest about evidence.** Company-specific claims rest on candidate reports (Glassdoor, GeeksforGeeks, Jointaro, Naukri, Reddit). Questions are tagged **[S]** (a candidate reported this specific question) or **[T]** (the topic was reported; the wording is ours). Formats are presented as "commonly reported", with the date of the evidence.

---

## 2. Architecture of the book

The book is one PDF with PDF bookmarks, clickable cross-references ("see p. 214") and page-edge colour tabs. It is organised in five parts.

| Part | Contents | Budget (pp) |
|---|---|---|
| **Part 0 — The Plans** | How to use the book (one annotated spread); three study tracks; schedule chooser; 8-week, 3-month and 6-month plans; progress tracker; 8 one-page checkpoints whose answers point to existing solutions | 20 |
| **Part I — The Twelve Pillars** | Twelve chapters: teaching sections, then one Problem Set with solutions and one Revision Spread (§4) | 970 |
| **Part II — Cheat Codes** | A *decoder* layer only: pattern decoder, mnemonics, speed tricks, OA tactics, each pointing to the page where the full treatment lives (§5) | 30 |
| **Part III — Company Playbooks & Mocks** | Nine 3-page playbooks (process, rounds, and the reported questions as page references); six mock OAs with solutions | 65 |
| **Part IV — Back matter** | Last-night pack; glossary; index | 30 |
| | **Total (hard budget, enforced at build)** | **≈ 1,100** |

**D1, page count — revised as you asked: zero redundancy, heavily optimised.** The pillar plans taken at face value sum to about 2,300 pages. Without cutting a single topic or a single solved interview question, the book is brought to **≈ 1,100 pages** by the rules in §2A. The 8-week Must lane is **≈ 260 pages** of that, plus the Part II decoder and one company playbook.

## 2A. Zero-redundancy rules (how the pages are saved)

1. **One home per concept.** Every concept, figure, table and solved question has exactly one canonical page. Everywhere else it appears as a cross-reference ("→ p. 214"), never as a second explanation. The build fails if two sections define the same glossary term.
2. **One home per question.** Each interview question is solved once, in the Problem Set of the pillar that teaches it. Company playbooks, checkpoints, mock-OA debriefs and the cheat codes cite it by number (`Q4.37 → p. 388`) instead of reprinting it. This alone removes about 250 pages of duplicate solutions.
3. **One practice layer, not three.** The separate "Check Yourself answers", "graded exercises" and "interview question bank" of the earlier plans are merged into a single tiered **Problem Set** per pillar (■□□ / ■■□ / ■■■). Inline Check Yourself questions stay, with one-line answers in a footnote on the same page.
4. **One revision layer, not five.** Short notes, the one-page revision sheet, the 15-minute page, the cheat sheet and the master cheat sheet are merged into a single two-page **Revision Spread** per pillar. Its top box is the 15-minute version. Part IV has no master cheat sheet; the twelve Revision Spreads are it.
5. **Compact solution template.** Every answer opens with a bold **30-second answer** (which doubles as the rapid-fire version, so no separate rapid-fire section is printed), then *Approach · Answer/Code · Complexity · Follow-ups · Mistakes*, with empty fields omitted. Typical length: ¼ page for a concept question, ½–¾ page for a coding problem.
6. **One language per solution.** C for systems and networking-company problems, C++ for general DSA, Python for automation and scripting. No parallel versions in other languages; a one-line note gives the key difference where it matters.
7. **Tables over prose** for every comparison (TCP vs UDP vs QUIC, OSPF vs IS-IS vs BGP, STP vs RSTP vs MST, IPsec vs TLS VPN, mutex vs semaphore vs spinlock), and **figures over paragraphs** wherever a diagram carries the argument.
8. **Trimmed lab output.** Labs print only the output lines the reader must notice, highlighted, not whole screens.
9. **Dense layout.** A4 page with a narrow margin column; two-column layout for Problem Sets, flashcard tables, Revision Spreads and the glossary; flashcards printed as compact Q/A tables, not cut-out cards.
10. **One calendar.** Spaced-repetition prompts live once in Part 0, not at the end of every chapter. Mini-projects are one-page briefs with milestones and a key code skeleton.

### Canonical-home map (where each overlapping topic lives)

The detailed plans overlap in the places below. Each topic is taught once, at its canonical home; the other places carry a cross-reference only.

| Topic | Canonical home | Becomes a cross-reference in |
|---|---|---|
| Subnetting, VLSM, CIDR | P3 §3.4 | P1 §1.5 (keeps only the bit-mask *code*), Part II speed-trick table |
| Longest-prefix match | P1 §1.9 (algorithm, trie) | P4 §4.4 (one paragraph), P5 router internals |
| Dijkstra, Bellman–Ford | P1 §1.11 | P3 §3.8 (dropped; merged into P1 §1.11 and P4 §4.5) |
| TCP congestion control, BDP | P3 §3.9 | P5 (DCTCP note), P8 §8.13 (tooling only) |
| TLS handshake | P9 §9.4 | P3 §3.10 (one paragraph) |
| NAT/PAT | P3 §3.6 | P4 §4.13 (IOS configuration only), P9 §9.6 |
| ACLs | P9 §9.5 | P4 §4.13 (IOS syntax only) |
| 802.1X / EAP | P9 §9.12 | P6 §6.2.7 (Wi-Fi-specific parts only) |
| Device internals: RIB, FIB, TCAM, ASIC | P5 §5.2.8 | P4 §4.1 (reduced to the CLI) |
| Sockets API | P7 §7.2.10 | P2 Part B (Python `socket` reduced to a pointer) |
| Bash scripting | P8 §8.2–8.4 | P2 Part D (removed; merged into P8) |
| Python libraries for networks | P10 | P2 Part B (keeps the language only) |
| C output-prediction traps | P2 Part A | Part II (index of trap numbers only) |
| DSA pattern templates | P1 sections | Part II pattern decoder (one row per pattern, with a page reference) |
| Troubleshooting framework | P11 SCALPEL | Part II (one card) |
| Aptitude formulae | P12A | Part II (index only) |
| STAR, Amazon LPs, résumé, negotiation | P12F–G | Part II (index only) |
| Memory hierarchy, endianness | P2 Part A, P7 §7.2.7 | P12D (keeps caches and pipelining only) |
| LRU cache, rate limiter, load balancer, CDN | P1 §1.15, P5 | P12E (design framing and cross-references only) |
| Mock OAs | Part III | P1 §1.18 (removed) |
| Company-reported questions | The pillar that teaches the topic | Part III playbooks (page references) |

### Per-pillar page budgets

| Pillar | Teaching | Problem Set | Revision Spread | Total |
|---|---|---|---|---|
| 1 DSA | 95 | 55 | 2 | 152 |
| 2 C / Python / C++ | 55 | 20 | 2 | 77 |
| 3 Computer Networks | 85 | 16 | 2 | 103 |
| 4 Routing & Switching | 95 | 18 | 2 | 115 |
| 5 Data Centre & Cloud | 55 | 12 | 2 | 69 |
| 6 Wireless & Cellular | 55 | 13 | 2 | 70 |
| 7 OS & Sockets | 60 | 14 | 2 | 76 |
| 8 Linux & Tools | 40 | 9 | 2 | 51 |
| 9 Security | 45 | 10 | 2 | 57 |
| 10 Automation | 40 | 9 | 2 | 51 |
| 11 Troubleshooting | 50 (incl. 18 cases, 3 mocks) | 9 | 2 | 61 |
| 12 Supporting subjects | 70 | 14 | 4 | 88 |
| **Total** | | | | **≈ 970** |

The build reports pages against these budgets for each pillar, and a pillar that exceeds its budget by more than 5 % is condensed before it is accepted.

---

## 3. The Twelve Pillars — chapter map

Each pillar opens with a two-page spread: a full-bleed hero diagram, the chapter's promise in one sentence, prerequisites, a section tracker with check-circles, a company-relevance strip and an estimated study time. Priority tags shown below are for the Infrastructure track unless noted; all three tracks are tagged in the book.

### Pillar 1 — Data Structures & Algorithms (cobalt `#3B5BDB`)
*Networks are graphs, routing tables are tries, and caches are hash maps; we learn DSA through the systems you will build.*

| § | Section | Tag |
|---|---|---|
| 1.0 | How coding rounds at network companies work | ● |
| 1.1 | Complexity and the problem-solving routine (UMPIRE) | ● |
| 1.2 | Arrays, two pointers, sliding window | ● |
| 1.3 | Hashing: maps and sets | ● |
| 1.4 | Strings and parsing network data (validate IPv4/IPv6, parse logs) | ● |
| 1.5 | Bit manipulation and subnet arithmetic | ● |
| 1.6 | Linked lists, written in C first | ● |
| 1.7 | Stacks, queues, ring buffers, deques | ● |
| 1.8 | Trees and BSTs | ● |
| 1.9 | **Tries and longest-prefix match** (signature section) | ● |
| 1.10 | Heaps and priority queues | ◐ |
| 1.11 | **Graphs: BFS/DFS, Dijkstra (= OSPF), Bellman–Ford (= RIP), MST, topological sort, union-find** | ● |
| 1.12 | Recursion and backtracking | ◐ |
| 1.13 | Sorting, binary search, intervals | ● |
| 1.14 | Dynamic programming essentials | ◐ |
| 1.15 | **Design-style coding: LRU/ARP cache, token-bucket rate limiter** (signature section) | ● |
| 1.16 | Finite-state machines (TCP and OSPF as FSMs) | ◐ |
| 1.17 | Testing your own code; performing in the room | ● |

Problem Set: about 110 problems in three tiers (the 105 practice problems and the 34 interview questions, de-duplicated), every statement restated in the book with a full solution. Mini-project: **mini-FIB**, a longest-prefix-match lookup engine in C.

### Pillar 2 — Programming: C, Python, C++, Bash (violet `#6741D9`)
*C is the language of the forwarding plane; Python is the language of the people who run it.*

- **Part A — C (critical):** memory model; pointers and pointer arithmetic; arrays vs pointers; structs, unions, **padding and alignment**, bit-fields; `volatile`, `static`, `const`, `extern`; function pointers and callbacks; dynamic memory and leaks; **endianness and `htonl`/`ntohs`**; macros and the preprocessor; undefined behaviour; writing `memcpy`, `strcpy`, `atoi` and a linked list from scratch; output-prediction drills.
- **Part B — Python:** data model; comprehensions and generators; `struct`; regex for log parsing; `subprocess`; file handling; writing clean scripts. (Sockets → P7; network libraries → P10.)
- **Part C — C++:** classes, RAII, references; STL containers and algorithms for interviews.
- **Bash** is taught once, in Pillar 8.

Problem Set: about 80 items (65 practice problems and 40 interview questions, de-duplicated). Mini-project: **pktpeek**, a packet decoder in C with a Python report tool and a Bash runner.

### Pillar 3 — Computer Networks Fundamentals (deep cyan `#0B7285`)
*Every packet tells a story; we learn to read it, layer by layer.*

| § | Section | Tag |
|---|---|---|
| 3.1 | Why networks exist: topologies, devices, the layered idea | ● |
| 3.2 | OSI and TCP/IP models; encapsulation | ● |
| 3.3 | Physical and data-link layers: Ethernet, framing, CRC, ARQ | ● (CRC/ARQ ◐) |
| 3.4 | **IPv4 addressing, subnetting, VLSM, CIDR** (with 60 speed drills) | ● |
| 3.5 | IPv4 header, fragmentation, MTU, ICMP (ping and traceroute internals) | ● |
| 3.6 | ARP, DHCP (DORA), NAT/PAT | ● |
| 3.7 | IPv6 essentials: addressing, NDP, SLAAC, dual stack | ◐ |
| 3.8 | Routing concepts (one page; algorithms → P1 §1.11, protocols → P4) | ● |
| 3.9 | **Transport: UDP, TCP, flow control, congestion control (Reno, CUBIC, BBR)** (flagship, ≈ 30 pp) | ● |
| 3.10 | Application layer: DNS, HTTP/1.1/2/3, TLS, QUIC | ◐ |
| 3.11 | **Capstone: "What happens when you type google.com?"** at three depths (2-, 5- and 15-minute answers) | ● |

Problem Set: 50 interview questions, including 10 long solved problems. Mini-project: **PacketScope**, a teaching packet dissector and subnet toolkit.

### Pillar 4 — Routing & Switching, CCNA → CCNP ENCOR (teal `#087F5B`)
*How a network decides, and how it recovers when something breaks.*

| § | Section | Tag |
|---|---|---|
| 4.1 | The CLI and device access (internals → P5 §5.2.8) | ◐ |
| 4.2 | Switching, VLANs, 802.1Q trunking, inter-VLAN routing | ● |
| 4.3 | Spanning Tree (STP, RSTP, PVST+, MST) and EtherChannel/LACP | ● |
| 4.4 | Routing table, longest-prefix match, AD vs metric, static and default routes | ● |
| 4.5 | **OSPF** single and multi-area, neighbour states, LSA types, OSPFv3 | ● |
| 4.6 | EIGRP | ○ (◐ Cisco) |
| 4.7 | **BGP** eBGP/iBGP, states, attributes, best-path selection, route reflectors (flagship, ≈ 30 pp) | ● |
| 4.8 | First-hop redundancy: HSRP, VRRP, GLBP | ◐ |
| 4.9 | Route control: prefix lists, route maps, redistribution, PBR, VRF-lite | ◐ |
| 4.10 | MPLS and L3VPN | ◐ |
| 4.11 | Quality of Service | ◐ |
| 4.12 | IP multicast: IGMP, PIM | ○ |
| 4.13 | IP services and access control: ACLs, NAT, NTP, SNMP, syslog | ● |
| 4.14 | Tunnels and enterprise architecture (GRE, SD-WAN overview) | ○ |

Problem Set: 55 interview questions, including 12 long solved problems. Mini-project: **Campus-to-Internet**, a dual-homed enterprise built and verified as code.

### Pillar 5 — Data Centre & Cloud Networking (steel blue `#1864AB`)
*How hyperscalers connect millions of servers, and how the cloud hides it.*

Why data centres broke the campus model → Clos and spine-leaf arithmetic → ECMP and flow hashing → eBGP underlay, BFD, unnumbered links → VXLAN → EVPN → SDN, OpenFlow, P4 → **router and switch internals: RIB, FIB, TCAM, ASIC pipeline** → L4/L7 load balancers → anycast and CDNs → AWS VPC → Azure VNet → Direct Connect, ExpressRoute, VPN → the life of a request in the cloud.
Problem Set: 40 questions; 12 labs (Containerlab, Mininet). Mini-project: **Pocket Hyperscaler**.

### Pillar 6 — Wireless & Cellular (raspberry `#C2255C`; core for Qualcomm)
*From radio waves to roaming: what happens before your laptop sends its first byte.*

RF in one sitting (decibels, link budget, Shannon) → OFDM, QAM, MIMO → 802.11 architecture and the family tree (a/b/g/n/ac/ax/be) → **the MAC: CSMA/CA, DCF timing, RTS/CTS, hidden node** → the 802.11 frame bit by bit → **connection lifecycle: scan, authenticate, associate, 4-way handshake, DHCP** → WPA2, 802.1X, WPA3, PMF → QoS (EDCA), aggregation, power save → Wi-Fi 6/6E and Wi-Fi 7 (OFDMA, MLO) → roaming → the Linux and firmware view (mac80211, nl80211) → LTE to 5G in one chapter.
Problem Set: 42 questions; 9 labs (monitor-mode capture). Mini-project: **Air Sniffer**, a Wi-Fi connection doctor.

### Pillar 7 — Operating Systems & Socket Programming (vermilion `#C2410C`)
*What the kernel does between the network card and your `recv()`.*

What an OS does → processes, `fork`/`exec` → threads and context switches → scheduling → **synchronisation: mutex, semaphore, spinlock, condition variable** → deadlock, starvation, priority inversion → memory, paging, TLB, virtual memory → interrupts, system calls, DMA → IPC and signals → **sockets from first principles** → **concurrency models: threads, `select`, `poll`, `epoll`** → the Linux network stack (`sk_buff`, NAPI, XDP) → firmware and embedded essentials → debugging a slow server.
Problem Set: 45 questions; 12 labs, including an epoll TCP server in C. Mini-project: **TinyRelay**.

### Pillar 8 — Linux & Network Tools (olive `#4D7C0F`)
*The command line is the network engineer's stethoscope.*

Shell survival kit → text processing for log hunting (`grep`, `awk`, `sed`, `jq`) → Bash that survives production → **iproute2** (`ip link/addr/route/neigh/rule/netns`) → `ss` → **`tcpdump`** → **Wireshark** → `dig` and friends → `ping`, `traceroute`, `mtr`, `nc`, `curl` → `ethtool` and NIC health → `iptables`/`nftables` → `iperf3`, BDP, socket buffers, `sysctl` → `/proc`, `lsof`, `strace`, `journalctl`.
Problem Set: 30 questions. Mini-project: **netdoctor**, a one-command connectivity diagnoser.

### Pillar 9 — Network Security (crimson `#B91C1C`)
*Every protocol you have learnt can be attacked; we learn how, and how to defend it.*

CIA, AAA, STRIDE, defence in depth → cryptography you must be able to explain (symmetric, asymmetric, hashing, Diffie–Hellman with a worked example) → PKI and certificates → **TLS 1.3 handshake step by step** → ACLs → stateful firewalls, NGFW, NAT interplay → **IPsec and IKE** → VPN families → Layer-2 attacks and switch hardening (ARP spoofing, VLAN hopping, DHCP snooping) → Layer-3/4 attacks and DDoS (SYN flood, amplification) → DNS security → RADIUS, TACACS+, 802.1X, NAC → IDS/IPS and device hardening → zero trust.
Problem Set: 32 questions. Mini-project: **Campus Shield**, an attack-and-defend lab report.

### Pillar 10 — Network Automation & Programmability (grape `#9C36B5`)
*Configure one device by hand; configure a thousand with code.*

The automation maturity ladder → JSON, YAML, XML → Paramiko → **Netmiko** → parsing CLI output (TextFSM, TTP, Genie) → Jinja2 and the source of truth → NAPALM → Nornir → **Ansible for networks** → **YANG** → **NETCONF and RESTCONF** → gNMI and streaming telemetry → Git for network engineers → CI/CD and network testing → safety at scale.
Problem Set: 30 questions. Mini-project: **FabricOps**, GitOps for a Containerlab leaf-spine.

### Pillar 11 — Troubleshooting Methodology (ochre `#A16207`)
*Method beats memory: a framework that turns a vague diagram into a diagnosis.*

The chapter is built on one reusable framework, **SCALPEL** (Symptom → Clarify → Assess → Layer walk → Pinpoint → Execute → Lock in), printed on the inside back cover. Sections: why method beats memory → SCALPEL in detail → the clarifying questions interviewers grade you on → strategies (bottom-up, top-down, divide-and-conquer, follow the packet) → a layer-by-layer command matrix for Cisco, Juniper and Linux, with how to read the output → symptom look-alikes → incident overlay and post-mortems → **The Case File: 18 fully specified scenarios** (for example "host can't reach the internet", "website slow only for some users", "OSPF stuck in EXSTART", "BGP session flapping", "duplicate IP", "MTU black hole") → **three mock rounds with interviewer scripts** modelled on the Cisco vague-diagram round and the Google and Amazon troubleshooting rounds.
Problem Set: 30 questions. Mini-project: **Fault Injector & Runbook Library**.

### Pillar 12 — Supporting Subjects (slate `#495057`)
*What decides the shortlist and the final yes.*

Seven sub-chapters, each with its own pack:
- **12A Aptitude & online assessments** (Indian campus formats; percentages, ratios, time-work, speed-distance, probability, permutations, number system, logical and verbal reasoning, each with formula cards and solved examples)
- **12B Object-oriented programming**
- **12C DBMS** (normalisation, SQL, transactions, indexing, at OA-MCQ depth)
- **12D Computer organisation** for network engineers (caches, pipelining, memory hierarchy, number representation)
- **12E Light system design for networking roles** (design a campus network, a rate limiter, a CDN, a load balancer)
- **12F Behavioural interviews**: STAR, Amazon Leadership Principles story bank, "Tell me about yourself"
- **12G Résumé and project deep-dives** for networking roles

Problem Set: 54 questions. Mini-project: **Placement Readiness Portfolio**.

**Cross-pillar thread.** One fictional organisation, **Campus Net**, recurs across all labs and worked examples: its addressing plan appears in Pillar 3, its VLANs and OSPF in Pillar 4, its data-centre extension in Pillar 5, its Wi-Fi in Pillar 6, its firewall in Pillar 9, its automation in Pillar 10 and its outages in Pillar 11. The reader therefore sees one network grow from a single subnet into a complete enterprise.

---

## 4. Inside every chapter, and after every chapter

### 4.1 Recurring learning elements (six forms only; see §8)

| Element | Purpose | Form | Frequency |
|---|---|---|---|
| **Big Idea** | The one sentence the section exists to teach, with its cause | Small-caps label, accent hairline, text one step larger | 1 per major section |
| **Worked Example** | Numbered steps with the reasoning, ending in a one-line Result | Numbered steps in a hanging gutter; Result set in semibold | 2–4 per section |
| **Trap** | *Claim / Why it is wrong / Correct statement* | Crimson hairline, small-caps label | 1–3 per section |
| **Interview Lens** | How the topic is examined, what a strong answer contains, likely follow-ups | Small-caps label; company names as plain small-caps text (CISCO · QUALCOMM · GOOGLE) | 1 per section |
| **Lab** | Commands, the key output lines highlighted, and "What you should notice" | Grey code block with a one-line small-caps header (`LAB 4.2 · 20 MIN`) | 1–2 per section |
| **Check Yourself** | 2–4 quick questions; one-line answers in a footnote on the same page | Numbered list under a small-caps label | 1 per section |

Other content is placed as follows:
- **Margin column:** analogies (with a note on where the analogy fails), mnemonics, speed tricks and term definitions, at most two per page.
- **Deep Dive:** set as an indented passage in a smaller size, labelled as skippable.
- **Real-system links:** one line in the secondary colour after a worked example (for example, "Linux `fib_trie`, Cisco CEF").

Rhythm rule: every two-page spread carries at least one figure, table or element, so no reader faces more than about 1,000 words of unbroken text.

### 4.2 The end-of-chapter pack (identical in all twelve pillars; ≈ 12–20 pp per pillar)

1. **Problem Set** (the single practice layer). Every interview question and practice problem for the pillar appears once, solved in full and tiered ■□□ / ■■□ / ■■■, with company and round tags and [S]/[T] evidence tags. There are about 470 interview questions plus the DSA and C practice problems, after de-duplication. Each uses the compact template of §2A rule 5: **30-second answer** → *Approach · Answer/Code · Complexity · Follow-ups · Mistakes*, with empty fields omitted.
2. **Revision Spread** (the single revision layer, two pages). The top box is the **15-minute version** (ten facts, three mini-diagrams). Below it come short notes as dense bullets, the key tables (ports, AD values, states, formulae, commands) and a two-column **flashcard table** of 40–80 Q/A pairs. Designed to be printed and pinned.
3. **Mini-project brief** (one page): goal, milestones, acceptance test and the key code skeleton.

Answers to inline Check Yourself questions sit in a footnote on the same page, so they need no pages of their own. Spaced-repetition prompts are given once, in the Part 0 calendar.

---

## 5. Part II — Cheat Codes (≈ 30 pp; gathered from the internet, canonical only where noted)

Part II follows the zero-redundancy rule in a simple way. Material that exists nowhere else in the book is printed here in full (**★ canonical here**). Material taught in a pillar appears only as a one-line decoder entry with its page reference.

**A1 DSA (≈ 8 pp).**
- ★ **Constraint decoder:** n ≤ 10 → backtracking; n ≤ 20 → bitmask; n ≤ 10³ → O(n²); n ≤ 10⁵ → O(n log n); n ≥ 10⁶ → O(n).
- ★ **Keyword-to-pattern decoder:** "sorted" → binary search or two pointers; "top k" → heap; "subarray sum" → prefix sum with a hash map; and about 30 more rows.
- **Pattern index:** 22 rows of *pattern · one-line trigger · classic bug · page of its template in P1*. The templates themselves are printed once, in P1.
- ★ **Big-O table** and ★ **edge-case checklist**.
- ★ **UMPIRE method** mapped to a 45-minute round, with a talk-track of phrases for thinking aloud.
- ★ **STL and Python standard-library quick reference.**

**A2 Networking (≈ 8 pp).**
- ★ **Mnemonic page:** OSI, DORA, OSPF states, BGP best-path ("We Love Oranges AS Oranges Mean Pure Refreshment"), STP election.
- ★ **Speed-trick tables:** subnetting by the magic-number and block-size methods, the /24–/32 table, powers of two.
- ★ **Reference tables:** ports and protocol numbers; Cisco and Juniper route preferences.
- **Header quick reference:** pointers to the canonical bit-layout figures in P3, P4 and P6.
- **Cross-references:** the google.com answer ladder (→ P3 §3.11) and the SCALPEL card (→ P11).

**A3 Online assessments (≈ 8 pp).**
- ★ **Reported formats** for all nine companies.
- ★ **Time-management plan** and ★ **MCQ elimination tactics**.
- **Indexes:** aptitude formula cards (→ P12A) and the 31 C output traps (→ P2 Part A).

**A4 HR (≈ 6 pp).**
- ★ **Offer negotiation for Indian offers.**
- ★ **HR question bank** with answer frames.
- **Cross-references:** STAR, the Amazon LP story bank, "Tell me about yourself" and the résumé checklist (→ P12F–G).

---

## 6. Part III — Company Playbooks & Mocks (≈ 65 pp)

**Company playbooks (about 3 pages each).** One each for **Cisco, Qualcomm, Google, Microsoft, Amazon (NDE), Juniper, Arista, Nokia, Broadcom**. Each contains:
- the reported process and rounds, dated;
- what each round tests, mapped to book sections with page numbers;
- a "last 7 days" plan;
- the 15–17 reported questions for that company, listed as `Q-number → page` with source and date. Each question is solved once, in its pillar's Problem Set.

**Cross-company top-30 must-solve list.** One page of page references.

**Six mock OAs** (about 6 pages each), timed and in the reported formats:
- The questions are new; they are not reprints of Problem Set items.
- Solutions are compact.
- Each mock ends with a debrief table that maps every mistake to the page to re-read.

---

## 7. Schedules

The three schedules share the book; they differ only in which tags they cover.

| Schedule | Covers | Daily budget | Total |
|---|---|---|---|
| **8-week fast plan** (yours) | Must lane | Mon–Fri 4 h, Sat 6 h, Sun 4 h | ≈ 240 h |
| 3-month plan | Must + Should | ≈ 3 h a day | ≈ 300 h |
| 6-month full plan | Everything | ≈ 2 h a day | ≈ 420 h |

**The 8-week plan at a glance.** Every weekday uses the same template: 60 min DSA practice, 120 min of the day's Must sections, 40 min lab or worked-example redo, 20 min recall. Sunday is a checkpoint plus a buffer, because a plan with no slack fails at the first missed day.

| Week | Main topic | DSA strand (daily) | Sunday |
|---|---|---|---|
| 1 | Layers, Ethernet, ARP, **subnetting**, C pointers and structs, Python basics | Complexity, arrays, strings, hashing, bits | Checkpoint 1 |
| 2 | **TCP/UDP**, congestion control, DNS, DHCP, TLS, "type google.com"; C traps; shell | Linked lists, stacks, queues, sliding window, binary search | Checkpoint 2 |
| 3 | VLANs, STP, routing table, **OSPF, BGP**, FHRP, ACL/NAT | Trees, tries (LPM), heaps, BFS/DFS | Checkpoint 3 + Mock OA 1 |
| 4 | **OS**: processes, threads, synchronisation, memory, interrupts; **sockets and epoll**; Linux tools | Dijkstra, Bellman–Ford, union-find, backtracking, intervals | Checkpoint 4 |
| 5 | Spine-leaf, ECMP, VXLAN/EVPN, cloud VPC; crypto, TLS, IPsec, firewalls | DP, greedy, grids | Checkpoint 5 |
| 6 | **Track variant**: Infra → troubleshooting cases + automation; Software → design coding (LRU, rate limiter) + OS depth; Wireless → Pillar 6 Must lane | LRU cache, rate limiter, mixed sets | Checkpoint 6 + Mock OA 2 |
| 7 | Troubleshooting mock rounds; aptitude; OOP/DBMS for OA MCQs; system design | Mixed timed sets | Checkpoint 7 + Mock OA 3 |
| 8 | Company playbook for your target; behavioural stories; revision sheets; last-night pack | Top-30 must-solve | Checkpoint 8 + Mock OA 4 |

---

## 8. Design system: aesthetic, minimalist, professional

The visual model is the restrained professional textbook (MIT Press, Stripe Press, the Tufte tradition), not the zine or the coaching workbook. The aesthetic comes from typography, whitespace and the quality of the figures. Decoration contributes nothing to it. Every visual element must carry information; anything that only decorates is removed.

**Principles**
1. **Restraint in colour.** The page is ink on white. Each pillar has one accent colour, used only for the chapter number, the running head, a 2 pt rule on callouts and highlighted lines in figures, and never as a large fill. Accents are muted (§3 hex values, desaturated by about 15 % in the final palette). Figures use greys plus at most one accent and one highlight.
2. **Typography does the work.** One serif for reading (Source Serif 4, 10/14.5 pt), one sans for structure (Inter: headings, labels, tables), one mono for code (JetBrains Mono, no ligatures). Hierarchy comes from size, weight and space, never from colour blocks. The hand-drawn font of the earlier plan is dropped. Small-caps labels (BIG IDEA, TRAP, LAB) replace badges and pills.
3. **A strict grid.** A4, a 12-column grid with a narrow outer margin column for definitions and notes, and generous margins. Elements align to the baseline grid, so pages look calm even when dense.
4. **Hairlines, not boxes.** Callouts are set off by a thin left rule and a label, with no heavy borders, no drop shadows and no rounded cards. A Trap uses the same form as other callouts, with a crimson rule; the meaning is carried by the label, so it also reads in greyscale.
5. **Fewer element types.** The learning elements are consolidated into six forms: **Big Idea · Worked Example · Trap · Interview Lens · Lab · Check Yourself**. Analogies and "where this shows up" notes are written into the prose or the margin, and do not get their own boxes. Mnemonics and speed tricks sit in the margin column.
6. **Icons: none in the text.** Each pillar has one geometric line mark, used only on its opener and in the contents. Navigation tags are plain small-caps text with a single shape glyph (`●  ◐  ○`), and difficulty uses `■□□`.
7. **Quiet navigation.** Running heads in small caps; folios in the outer corner; a thin accent tab at the page edge for the pillar. The footer progress bar is dropped. Progress tracking lives in the Part 0 tracker and on pillar openers only.
8. **Chapter openers.** A right-hand page with generous whitespace: the pillar number set large in the accent colour, the title, the one-sentence promise, a short section list with Must/Should/Optional tags, and one hero figure. There is no photography, illustration or gradient.
9. **Figures at professional standard.** One drawing system for about a thousand vector figures: thin strokes (0.6–1 pt), a neutral grey palette, one accent for "the thing to notice", Inter labels at 7 pt, no 3-D, no clip-art, no shading gradients, no vendor logos. Fixed shapes for router, switch, host, access point and cloud; fixed line styles for data, control and failure paths. Figure types include:
   - topology diagrams;
   - ladder (sequence) diagrams for handshakes;
   - header bit-layouts;
   - state machines (TCP, OSPF, BGP);
   - memory diagrams (struct padding, pointers, page tables);
   - Clos fabrics;
   - Wi-Fi timing diagrams;
   - packet walks showing MAC and IP at each hop.
10. **Tables in the book style.** Three horizontal rules (top, header, bottom); no vertical lines, no zebra striping, numbers right-aligned in tabular figures.
11. **Code that looks like a reference manual.** Light grey background (`#F6F6F4`), restrained syntax colouring (keywords and comments only), line numbers only where the text refers to them, and highlighted lines marked by a thin accent bar.
12. **Consistency enforced by the build.** Lint rules reject any colour outside the palette, any font outside the three families, more than one accent per figure, and any callout type outside the six forms.

**Colour palette (final)**

| Token | Value | Use |
|---|---|---|
| Paper | `#FFFFFF` | page (print and screen) |
| Ink | `#1A1D23` | body text |
| Secondary | `#5F6670` | captions, margin notes, running heads |
| Rule | `#D8DADD` | hairlines, table rules |
| Code background | `#F6F6F4` | listings and CLI |
| Highlight | `#FFF4C2` | one highlighted region per figure or listing, at most |
| Trap rule | `#A61B1B` | Trap callouts only |
| Pillar accents | the twelve hues of §3, desaturated | one per pillar, used sparingly as above |

**Motivation without decoration.** The pull to keep reading comes from four quieter sources: (i) a figure on almost every spread; (ii) short sections, each opening with its Big Idea; (iii) visible progress in the tracker and on the chapter openers; and (iv) the Campus Net storyline, in which one network grows across the book.

**Voice (guide-style skill, senior era).**
- **Prose:** plain and sober; British spelling; "we" for author and reader working together; sections open with "Consider …".
- **Rigour:** terms defined in passing; (i)/(ii) lists; a cause given for every claim ("This is because …"); takeaways closed with "Thus," or "Hence,".
- **Excluded:** hype, rhetorical questions and exclamation marks.
- **Domain pack:** the guide-style TCP/AQM pack applies to §3.9 (congestion control); other chapters follow the general rules.

---

## 9. Production (how the book is built)

**Toolchain (tested in this container).** Pandoc Markdown → HTML/CSS → Paged.js → Chromium via Playwright → PDF.
- A 2-page specimen confirmed working page references, margin notes, running heads, bookmarks, embedded fonts and a tagged PDF.
- Figures are generated as SVG from short YAML specs by a small in-house Python library, with Graphviz used only for layout. This keeps a thousand figures consistent.
- Source layout: `content/NN-pillar/*.md`, `figures/NN/*.yml`, `code/NN/` (every listing compiled and tested), `labs/NN/`.

**Writing process, pillar by pillar.**
1. Specimen: 12 pages showing a pillar opener, one complete section with every element, a Problem Set page, a Revision Spread and a playbook page. **Approved by you before anything else is written.**
2. Pilot pillar: Pillar 3, because every other pillar depends on its terms and figures.
3. The remaining pillars, in dependency order: wave A (1, 2, 4, 7), wave B (5, 6, 8, 9), wave C (10, 11, 12); then Parts II–IV.
4. For each pillar, one agent drafts from the detailed plan and a second agent does technical review. The reviewer checks every number, every command and every code listing (compiled and run), then runs the guide-style lint and stylometrics.
5. Each pillar is built to PDF and sent to you for review before the next wave begins.

**Ordering for your 8 weeks.** Because you start soon, I propose releasing the **Must lane first** (v0.9: Part 0, every Must section, all cheat codes and revision sheets), then filling in the Should and Optional sections (v1.0). You can start studying from v0.9 while the rest is written.

---

## 10. Known limits and verification

1. **Blocked sites.** GeeksforGeeks, LeetCode, Naukri and Cisco's learning portal were blocked by this session's network settings, so company questions come from search-result summaries. Before the book is final, every [S] question should be checked against its original post; this needs those sites allowed in the environment's network settings.
2. **CCNA version.** Third-party sites report that CCNA v2.0 replaces v1.1 in February 2027; Pillar 4 will be aligned to the blueprint current at release, with a dated note.
3. **Volatile figures** (OA formats, salary ranges, Wi-Fi 7 details) are marked `[VERIFY]` in the plans and dated in the book.
4. **Company formats** are presented as reported patterns, never as official processes.

---

## 11. Decisions for you

| # | Decision | My recommendation |
|---|---|---|
| D1 | Page count | **Decided:** zero redundancy, ≈ 1,100 pages, hard per-pillar budgets, no topic or solved question cut (§2A) |
| D2 | Release order | v0.9 Must lane first, then v1.0 complete (§9) |
| D3 | First deliverable | 12-page specimen in the minimalist professional style (§8), for your approval of the look and voice |
| D4 | Voice | The guide's sober voice in the prose; engagement through design. The "Cheat Codes" name stays as you asked, but the boxes inside use plain labels ("Mnemonic", "Speed Trick") |
| D5 | Your track for the 8-week plan | Tell me: Software, Infrastructure or Wireless, and your top two target companies, so the Week 6 variant and the playbook order fit you |
| D6 | Where the work lives | Commit the plans and the book source to this repository's working branch so nothing is lost when the container is reclaimed (the scratchpad is temporary) |
