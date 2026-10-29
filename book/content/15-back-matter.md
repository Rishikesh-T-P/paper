::: {.chapter .p0}
::: opener
[Part IV · Back Matter]{.part-label}

[IV]{.num}

# Back Matter {#ch15}

[A last-night pack, a review calendar and a glossary; the book's index of terms and where each one is taught.]{.promise}

1. [IV.1 The last night before the interview]{} [★]{}
2. [IV.2 The 1-3-7-14-30 review calendar]{} [★]{}
3. [IV.3 Glossary of 163 terms]{} [★]{}
:::

## [IV.1]{.sec}The last night before the interview [Must · ■□□]{.tag} {#s15-1}

::: bigidea
The night before an interview is for retrieval and rest, because tired recall loses more marks than one further topic can win.
:::

This pack teaches nothing. Every item is either something to pack, something to say aloud, or a pointer to the page that holds the proof. There is no master cheat sheet in this book: the twelve Revision Spreads are it, and the pack tells one when to open which.

### An evening in blocks

The times assume an interview in the morning. Move the whole table later by the same amount if it is in the afternoon.

| Time | Do | Home |
|-----|--------------------------------------|----------|
| 18:00 | Work through the logistics list below; set two alarms | this page |
| 18:30 | Read your company's playbook: the process, then the row of the seven-day plan for today | [Part III](#ch14){.ref} |
| 19:15 | Say the twenty facts of your track aloud; mark each hesitation and follow its link | below |
| 20:00 | One timed warm-up: a problem you have already solved, rewritten from a blank page, or one section of a mock paper | [Part III](#s14-mocks){.ref} |
| 21:00 | "Tell me about yourself" aloud, then two STAR story titles | [§12.12](#s12-12){.ref} |
| 21:45 | Pack, lay out clothes, charge devices | below |
| 22:30 | Stop. No new topics, no reading of technical material | |

In the morning, follow the 15-minute page. In minutes 0 to 5, read aloud the boxed "ten facts" at the top of the Revision Spread of your weakest pillar. In minutes 5 to 10, cover the flashcard table beneath it and answer ten rows, ticking each correct answer. In minutes 10 to 15, redraw one figure or compute one subnet from memory, and then compare it with the book. Finally, say the three things you will remember if the rest goes: your approach to a problem, your project in one sentence, and one question for the interviewer.

### Logistics

| Area | Check |
|-------|----------------------------------------------|
| Documents | three printed résumés; photo ID and college ID; the interview or admit letter; mark sheets if asked |
| Device | laptop charged and the charger packed; headphones, webcam and microphone tested; a second connection (phone hotspot); `gcc` and `python3` run; unrelated tabs and notifications closed |
| Room for a virtual round | quiet, door closed, light in front of you, a plain background; water; phone on silent and out of reach; paper and pen for working |
| Online assessment | read the instruction page for negative marking and section locking; one screen, no phone on the desk; tab switches are logged |
| On site | route checked and a 30-minute margin; water and a snack; clothes laid out |

### The one thing to prepare for each company

Each line points to the playbook, which holds the process, the seven-day plan and the reported questions.

| Company | The one thing to have ready | Playbook |
|---------|--------------------------------------|----|
| Cisco | a scenario answered layer by layer, and subnetting without a calculator | [III.1](#s14-1){.ref} |
| Qualcomm | C declarations, structure sizes and bit manipulation | [III.2](#s14-2){.ref} |
| Google | two or three approaches before code; the google.com ladder at two lengths | [III.3](#s14-3){.ref} |
| Microsoft | an LRU cache in twenty minutes, and the thread-safety follow-up | [III.4](#s14-4){.ref} |
| Amazon (NDE) | troubleshooting aloud; one outage story with a root cause | [III.5](#s14-5){.ref} |
| Juniper | linked lists in C; OSPF and BGP basics | [III.6](#s14-6){.ref} |
| Arista | C debugging; spine-leaf and VXLAN arithmetic | [III.7](#s14-7){.ref} |
| Nokia | simple programs without bugs; OSI through routing | [III.8](#s14-8){.ref} |
| Broadcom | bits and C; how to test a memory segment | [III.9](#s14-9){.ref} |

### Twenty facts for each track

A track is the family of roles one prepares for ([§0.2](#s0-2){.ref}). Say the facts of your track aloud, and mark any that you cannot finish. The link beside each fact is the page that proves it, so a hesitation costs one look and not an hour of reading.

**Software track** (networking software at Cisco, Juniper, Arista, Nokia and Broadcom; software on networking teams at Google and Microsoft).

| # | Fact | Where |
|--|--------------------------------------------------|----|
| 1 | Read the constraints first: n up to 10<sup>5</sup> allows O(n log n), not O(n²). | [§1.1](#s1-1){.ref} |
| 2 | Say the six steps aloud: understand, examples, brute force, optimise, code, test. | [§1.1](#s1-1){.ref} |
| 3 | A variable window shrinks with `while`, not `if`; a prefix-sum map starts with `{0: 1}`. | [§1.2](#s1-2){.ref} |
| 4 | The mask for prefix p is `p ? ~0u << (32-p) : 0`; broadcast is `net \| ~mask`. | [§1.5](#s1-5){.ref} |
| 5 | In a C list, test `fast` before `fast->next`; delete with `Node **pp` so the head needs no special case. | [§1.6](#s1-6){.ref} |
| 6 | Longest-prefix match on a binary trie keeps the deepest marked node and costs O(32). | [§1.9](#s1-9){.ref} |
| 7 | BFS marks visited on push; Dijkstra skips stale entries and forbids negative weights. | [§1.11](#s1-11){.ref} |
| 8 | LRU is a hash map to doubly-linked-list nodes; every list change is mirrored in the map. | [§1.15](#s1-15){.ref} |
| 9 | Token bucket: tokens = min(B, tokens + r·Δt), and a packet passes if the tokens cover it. | [§1.15](#s1-15){.ref} |
| 10 | Struct members align to their size, so ordering them largest first minimises padding. | [§2.7](#s2-7){.ref} |
| 11 | `volatile` forces a memory access each time; it is not a thread-safety tool. | [§2.6](#s2-6){.ref} |
| 12 | Undefined behaviour includes signed overflow, shifts by the width or more, and two writes to one variable. | [§2.12](#s2-12){.ref} |
| 13 | Network byte order is big-endian: use `htons` and `htonl`, and never send a raw struct. | [§2.9](#s2-9){.ref} |
| 14 | Threads share code, heap and open files but have their own stack and registers. | [§7.3](#s7-3){.ref} |
| 15 | Deadlock needs mutual exclusion, hold and wait, no pre-emption and circular wait. | [§7.6](#s7-6){.ref} |
| 16 | `recv()` may return fewer bytes than were sent, so frame messages over TCP. | [§7.10](#s7-10){.ref} |
| 17 | Edge-triggered epoll needs non-blocking sockets read until `EAGAIN`. | [§7.11](#s7-11){.ref} |
| 18 | TIME_WAIT sits on the active closer; many CLOSE_WAIT sockets are an application bug. | [§3.9](#s3-9){.ref} |
| 19 | A routing decision tests longest prefix first, then administrative distance, then metric. | [§4.4](#s4-4){.ref} |
| 20 | BGP runs over TCP 179, and best-path selection begins with weight, then local preference. | [§4.7](#s4-7){.ref} |

**Infrastructure track** (network engineers, Amazon network development, Cisco consulting).

| # | Fact | Where |
|--|--------------------------------------------------|----|
| 1 | The MAC address changes at every hop; the IP address does not, except at NAT. | [§3.2](#s3-2){.ref} |
| 2 | Block size is 256 − mask octet; usable hosts are 2<sup>h</sup> − 2. | [§3.4](#s3-4){.ref} |
| 3 | TTL and header checksum change at every hop; MSS is MTU − 40. | [§3.5](#s3-5){.ref} |
| 4 | DHCP is DORA over UDP 68 to 67; T1 is 50% and T2 87.5% of the lease. | [§3.6](#s3-6){.ref} |
| 5 | STP: the lowest bridge ID is the root; the root port has the lowest root path cost. | [§4.3](#s4-3){.ref} |
| 6 | OSPF stuck in ExStart points to MTU; stuck in 2-Way between DROthers is normal. | [§4.5](#s4-5){.ref} |
| 7 | LSA types 1 and 2 stay in the area, 3 and 4 cross ABRs, 5 is domain-wide, 7 becomes 5. | [§4.5](#s4-5){.ref} |
| 8 | iBGP does not re-advertise iBGP routes, so it needs a full mesh or route reflectors. | [§4.7](#s4-7){.ref} |
| 9 | Local preference steers outbound traffic; prepending, MED and communities influence inbound. | [§4.7](#s4-7){.ref} |
| 10 | HSRP pre-emption is off by default, and tracking lowers priority when an uplink fails. | [§4.8](#s4-8){.ref} |
| 11 | ACLs are read top-down and end in an implicit deny; the wildcard is the inverted mask. | [§9.5](#s9-5){.ref} |
| 12 | PAT shares one address by rewriting source ports; know inside local and inside global. | [§3.6](#s3-6){.ref} |
| 13 | A timeout means no answer (filtered or dead); refused means a RST came back. | [§11.6](#s11-6){.ref} |
| 14 | SCALPEL fixes the order of a troubleshooting answer; state the layer before the fix. | [§11.2](#s11-2){.ref} |
| 15 | Oversubscription is server-facing bandwidth over uplink bandwidth: 48 × 10G over 6 × 40G is 2 : 1. | [§5.2](#s5-2){.ref} |
| 16 | ECMP hashes the five-tuple per flow, never per packet, to avoid reordering. | [§5.3](#s5-3){.ref} |
| 17 | VXLAN is UDP 4789 and adds 50 bytes, so the underlay MTU must be at least 1,550. | [§5.5](#s5-5){.ref} |
| 18 | Small packets work and large ones fail: suspect MTU and blocked ICMP type 3 code 4. | [§3.5](#s3-5){.ref} |
| 19 | The effective TCP window is min(rwnd, cwnd); throughput is at most window / RTT. | [§3.9](#s3-9){.ref} |
| 20 | For "type google.com", go from browser cache to DNS, TCP, TLS and HTTP, and stop at the depth asked. | [§3.11](#s3-11){.ref} |

**Wireless track** (WLAN and modem software, principally Qualcomm).

| # | Fact | Where |
|--|--------------------------------------------------|----|
| 1 | Wi-Fi uses CSMA/CA because a radio cannot hear a collision while it transmits. | [§6.4](#s6-4){.ref} |
| 2 | SIFS is shorter than DIFS, so acknowledgements win the medium. | [§6.4](#s6-4){.ref} |
| 3 | The hidden-node problem is solved with RTS/CTS and the NAV timer. | [§6.4](#s6-4){.ref} |
| 4 | Four address fields are used only when both To DS and From DS are set. | [§6.5](#s6-5){.ref} |
| 5 | The frame types are management, control and data. | [§6.5](#s6-5){.ref} |
| 6 | A connection is probe, authenticate, associate, and then the four-way handshake. | [§6.6](#s6-6){.ref} |
| 7 | The PTK is derived from the PMK, both nonces and both MAC addresses; the GTK protects group traffic. | [§6.7](#s6-7){.ref} |
| 8 | WPA3-SAE resists offline dictionary attacks; PMF stops forged deauthentication. | [§6.7](#s6-7){.ref} |
| 9 | OFDM subcarriers are orthogonal, and the cyclic prefix absorbs multipath echoes. | [§6.2](#s6-2){.ref} |
| 10 | OFDMA divides a channel into resource units shared by stations; trigger frames schedule uplink. | [§6.9](#s6-9){.ref} |
| 11 | BSS colouring reduces co-channel interference; TWT lets devices sleep between agreed times. | [§6.9](#s6-9){.ref} |
| 12 | Wi-Fi 7 adds 320 MHz channels, 4096-QAM and multi-link operation. | [§6.9](#s6-9){.ref} |
| 13 | A-MPDU aggregates frames that keep their own checks and are acknowledged by a Block Ack. | [§6.8](#s6-8){.ref} |
| 14 | EDCA gives voice the highest access category and the shortest waiting time. | [§6.8](#s6-8){.ref} |
| 15 | A DTIM beacon announces buffered multicast; the TIM lists stations with buffered unicast. | [§6.8](#s6-8){.ref} |
| 16 | 200 mW is 23 dBm, and every 3 dB doubles or halves the power. | [§6.1](#s6-1){.ref} |
| 17 | Only channels 1, 6 and 11 avoid overlap in the 2.4 GHz band. | [§6.1](#s6-1){.ref} |
| 18 | 802.11k, v and r help roaming: neighbour reports, steering and fast transition. | [§6.10](#s6-10){.ref} |
| 19 | The LTE core has MME, S-GW, P-GW and HSS; the 5G core has AMF, SMF and UPF. | [§6.12](#s6-12){.ref} |
| 20 | On Linux, cfg80211 configures, mac80211 implements the soft MAC, and nl80211 is the user interface. | [§6.11](#s6-11){.ref} |

### On the day, and afterwards

| Moment | Do | Because |
|-------|--------------------------------|----------------------|
| Arrival or login | Be ready 20 to 30 minutes early; for a virtual round, join five minutes early with the editor open | a late start spends the calm that the pack built |
| The first two minutes | Greet, name the role, and ask the format: "How long is the round, and do I code in a shared editor?" | the answer fixes your pacing |
| A technical round | Think aloud, restate the problem, give the brute force, and ask before assuming | a visible process earns marks even when the code is unfinished ([§1.17](#s1-17){.ref}) |
| When stuck | Say what you tried and what you would try next; take a hint openly | it shows how you work with others |
| Between rounds | Drink water, breathe, and do not replay the last answer | each round is a fresh start, whatever happened in the last |
| The same evening | Write down the questions asked, your slips and the topics to repair; add them to the error log and the calendar | the notes feed the next interview |
| Within a day | Send a short thank-you if you have the contact; ask about the timeline | it is courteous and costs a minute |
| After an offer | Read the whole letter before replying | see [A4](#s13-4){.ref} for the comparison and the words to use |

### Stories, questions and the blank mind

The behavioural minimum is three things: a "Tell me about yourself" of 60 to 90 seconds ([Q12.41](#ps12){.ref}); eight STAR stories, each titled and tagged with the principles it serves ([§12.12](#s12-12){.ref}); and three questions for the interviewer, namely the on-call load, the team's tools and how success is measured at six months. The C traps are indexed in [A3](#s13-3){.ref}; read the fifteen that you missed most often, not all thirty-six.

If the mind goes blank, there are three moves. (i) Restate the question and ask a clarifying question, which buys time and often reveals the answer. (ii) Say what you do know, and structure it: "I would start with the layer, then the protocol." (iii) For code, state the brute force first and its cost. None of the three needs a new fact, and each is a habit of the routine in [§1.1](#s1-1){.ref} and [§11.2](#s11-2){.ref}.

## [IV.2]{.sec}The 1-3-7-14-30 review calendar [Must · ■□□]{.tag} {#s15-2}

::: bigidea
A memory that is recalled just before it fades lasts longer than one that is re-read, so the gaps between reviews grow as the memory strengthens.
:::

A *block* is what one studies in one day: a few sections, a lab or a set of problems. The schedule reviews each block on days 1, 3, 7, 14 and 30 after it was first studied. A review is a recall and not a re-read: close the book and answer the flashcard rows of the block's pillar, or redo one worked example on paper, in about four minutes. Five reviews at four minutes is the twenty minutes of daily recall in the plan of [§0.3](#s0-3){.ref}.

★ **The calendar.** B*n* is the block first studied on day *n*; the table lists the reviews that fall due on each day. After day 35 the pattern continues unchanged.

| Day | New block | Reviews due |
|---|---|-------------|
| 1 | B1 | none |
| 2 | B2 | B1 (D1) |
| 3 | B3 | B2 (D1) |
| 4 | B4 | B3 (D1), B1 (D3) |
| 5 | B5 | B4 (D1), B2 (D3) |
| 6 | B6 | B5 (D1), B3 (D3) |
| 7 | B7 | B6 (D1), B4 (D3) |
| 8 | B8 | B7 (D1), B5 (D3), B1 (D7) |
| 9 | B9 | B8 (D1), B6 (D3), B2 (D7) |
| 10 | B10 | B9 (D1), B7 (D3), B3 (D7) |
| 11 | B11 | B10 (D1), B8 (D3), B4 (D7) |
| 12 | B12 | B11 (D1), B9 (D3), B5 (D7) |
| 13 | B13 | B12 (D1), B10 (D3), B6 (D7) |
| 14 | B14 | B13 (D1), B11 (D3), B7 (D7) |
| 15 | B15 | B14 (D1), B12 (D3), B8 (D7), B1 (D14) |
| 16 | B16 | B15 (D1), B13 (D3), B9 (D7), B2 (D14) |
| 17 | B17 | B16 (D1), B14 (D3), B10 (D7), B3 (D14) |
| 18 | B18 | B17 (D1), B15 (D3), B11 (D7), B4 (D14) |
| 19 | B19 | B18 (D1), B16 (D3), B12 (D7), B5 (D14) |
| 20 | B20 | B19 (D1), B17 (D3), B13 (D7), B6 (D14) |
| 21 | B21 | B20 (D1), B18 (D3), B14 (D7), B7 (D14) |
| 22 | B22 | B21 (D1), B19 (D3), B15 (D7), B8 (D14) |
| 23 | B23 | B22 (D1), B20 (D3), B16 (D7), B9 (D14) |
| 24 | B24 | B23 (D1), B21 (D3), B17 (D7), B10 (D14) |
| 25 | B25 | B24 (D1), B22 (D3), B18 (D7), B11 (D14) |
| 26 | B26 | B25 (D1), B23 (D3), B19 (D7), B12 (D14) |
| 27 | B27 | B26 (D1), B24 (D3), B20 (D7), B13 (D14) |
| 28 | B28 | B27 (D1), B25 (D3), B21 (D7), B14 (D14) |
| 29 | B29 | B28 (D1), B26 (D3), B22 (D7), B15 (D14) |
| 30 | B30 | B29 (D1), B27 (D3), B23 (D7), B16 (D14) |
| 31 | B31 | B30 (D1), B28 (D3), B24 (D7), B17 (D14), B1 (D30) |
| 32 | B32 | B31 (D1), B29 (D3), B25 (D7), B18 (D14), B2 (D30) |
| 33 | B33 | B32 (D1), B30 (D3), B26 (D7), B19 (D14), B3 (D30) |
| 34 | B34 | B33 (D1), B31 (D3), B27 (D7), B20 (D14), B4 (D30) |
| 35 | B35 | B34 (D1), B32 (D3), B28 (D7), B21 (D14), B5 (D30) |


Three variants cover other situations. *Under 30 days to the interview:* use gaps of 2, 3, 5 and 7 days, so a block studied on day *d* is reviewed on days *d* + 2, *d* + 5, *d* + 10 and *d* + 17. *Flashcards:* the Leitner boxes hold cards that are reviewed daily (box 1), every 2 days (box 2), every 4 days (box 3), weekly (box 4) and fortnightly (box 5); a correct answer moves a card up one box, and a wrong answer sends it back to box 1. *Coding problems:* re-solve from a blank page, not from the solution, on the third and fourteenth day, and retire a problem once it is solved without hints in under 25 minutes.

★ **A tracker strip for the foot of any page.**

| First studied | D1 | D3 | D7 | D14 | D30 |
|-------|----|----|----|-----|-----|
| \_\_ / \_\_ | □ | □ | □ | □ | □ |

Two sources feed the calendar. The first is the flashcard table of each Revision Spread: [1](#rv1){.ref}, [2](#rv2){.ref}, [3](#rv3){.ref}, [4](#rv4){.ref}, [5](#rv5){.ref}, [6](#rv6){.ref}, [7](#rv7){.ref}, [8](#rv8){.ref}, [9](#rv9){.ref}, [10](#rv10){.ref}, [11](#rv11){.ref} and [12](#rv12){.ref}. The second is the error log of each mock paper ([Part III](#s14-mocks){.ref}), whose "re-attempt on" column should hold the dates D+3 and D+14 of the day the mistake was made.

## [IV.3]{.sec}Glossary of 163 terms [Must · ■□□]{.tag} {#s15-3}

Each entry is a reminder of at most fifteen words. The link beside it is the one section where the term is taught, and it is the only place to learn it; the entries are in alphabetical order.

::: {.revision}
::: flash
| Term | Meaning, and where it is taught |
|--------|--------------------------------|
| **802.1X** | Port-based authentication with supplicant, authenticator and server. [§9.12](#s9-12){.ref} |
| **AAA** | Authentication, authorisation and accounting: who you are, what you may do, what you did. [§9.12](#s9-12){.ref} |
| **ACID** | Atomicity, consistency, isolation and durability of transactions. [§12.9](#s12-9){.ref} |
| **ACL** | Ordered permit or deny list, tested top-down, ending in an implicit deny. [§9.5](#s9-5){.ref} |
| **Administrative distance** | Trust rank of a route source; the lower value wins between protocols. [§4.4](#s4-4){.ref} |
| **AMF** | 5G core function for registration, access and mobility of devices. [§6.12](#s6-12){.ref} |
| **Ansible** | Agentless automation tool applying idempotent tasks from YAML playbooks. [§10.9](#s10-9){.ref} |
| **Anycast** | One address announced from many places; routing delivers to the nearest. [§5.10](#s5-10){.ref} |
| **ARP** | Maps an IPv4 address to a MAC address on the local link. [§3.6](#s3-6){.ref} |
| **Autonomous system** | Network under one routing policy, identified by an AS number. [§4.7](#s4-7){.ref} |
| **Bandwidth-delay product** | Bandwidth times round-trip time: the data in flight that fills a path. [§3.9](#s3-9){.ref} |
| **BFD** | Fast hello protocol that detects a failed link or neighbour in milliseconds. [§5.4](#s5-4){.ref} |
| **BGP** | Path-vector protocol exchanging routes between autonomous systems over TCP port 179. [§4.7](#s4-7){.ref} |
| **Big-O** | Upper bound on how work grows with input size, ignoring constants. [§1.1](#s1-1){.ref} |
| **Binary search tree** | Tree with smaller keys in the left subtree and larger in the right. [§1.8](#s1-8){.ref} |
| **Block size** | 256 minus the mask octet: the spacing of subnets in that octet. [§3.4](#s3-4){.ref} |
| **Bridge ID** | Priority plus MAC; the lowest in the network becomes the STP root. [§4.3](#s4-3){.ref} |
| **BSS colouring** | Wi-Fi 6 tag that lets stations ignore frames from overlapping cells. [§6.9](#s6-9){.ref} |
| **CDN** | Servers near users that cache content and cut latency. [§5.10](#s5-10){.ref} |
| **Certificate** | Signed statement binding a public key to a name. [§9.3](#s9-3){.ref} |
| **CIA triad** | Confidentiality, integrity, availability: the three goals of security. [§9.1](#s9-1){.ref} |
| **CIDR** | Prefix-length addressing that replaced classful boundaries and allows aggregation. [§3.4](#s3-4){.ref} |
| **Clos network** | Multi-stage fabric in which every leaf connects to every spine. [§5.2](#s5-2){.ref} |
| **Congestion window** | Sender's limit on unacknowledged data, adjusted by network feedback. [§3.9](#s3-9){.ref} |
| **Conntrack** | Linux table of tracked connections that stateful filtering relies on. [§8.12](#s8-12){.ref} |
| **Context switch** | Saving one thread's registers and loading another's so the CPU changes task. [§7.3](#s7-3){.ref} |
| **CRC** | Polynomial-division checksum that detects burst errors. [§3.3](#s3-3){.ref} |
| **CSMA/CA** | Wi-Fi access: listen, back off, transmit and wait for an acknowledgement. [§6.4](#s6-4){.ref} |
| **CSMA/CD** | Ethernet access: listen, send, detect collisions, back off. [§3.3](#s3-3){.ref} |
| **CTC** | Cost to company: the employer's total cost, not the cash received. [§12.12](#s12-12){.ref} |
| **Cut-through** | Switch forwards after reading the destination address, before the frame ends. [§3.3](#s3-3){.ref} |
| **Cyclic prefix** | Tail of an OFDM symbol copied in front to absorb multipath echoes. [§6.2](#s6-2){.ref} |
| **dBm** | Power relative to 1 mW on a logarithmic scale. [§6.1](#s6-1){.ref} |
| **Deadlock** | Processes wait for each other in a cycle and none can proceed. [§7.6](#s7-6){.ref} |
| **DHCP** | Gives hosts an address, mask, gateway and DNS server through DORA. [§3.6](#s3-6){.ref} |
| **Direct server return** | Backend replies straight to the client, bypassing the load balancer. [§5.9](#s5-9){.ref} |
| **DMA** | Device copies data to memory without the CPU moving each word. [§7.8](#s7-8){.ref} |
| **DNS** | Hierarchical system that maps names to addresses and other records. [§3.10](#s3-10){.ref} |
| **DNSSEC** | Signatures on DNS records that prove their origin and integrity. [§9.11](#s9-11){.ref} |
| **Dynamic programming** | Solve overlapping subproblems once and store the results in a table. [§1.14](#s1-14){.ref} |
| **eBGP** | BGP between different autonomous systems; administrative distance 20. [§4.7](#s4-7){.ref} |
| **ECMP** | Spreads flows across equal-cost paths by hashing header fields. [§5.3](#s5-3){.ref} |
| **EIGRP** | Cisco's advanced distance-vector protocol, using DUAL and feasible successors. [§4.6](#s4-6){.ref} |
| **Encapsulation** | Wrapping a payload in a new header at each layer on the way down. [§3.2](#s3-2){.ref} |
| **Endianness** | The order in which the bytes of a multi-byte value are stored. [§2.9](#s2-9){.ref} |
| **epoll** | Linux interface that reports ready descriptors without scanning them all. [§7.11](#s7-11){.ref} |
| **EtherChannel** | Several physical links bundled into one logical link. [§4.3](#s4-3){.ref} |
| **EVPN** | BGP control plane that distributes MAC and IP reachability for VXLAN. [§5.6](#s5-6){.ref} |
| **Feasible successor** | Loop-free backup route whose reported distance is below the feasible distance. [§4.6](#s4-6){.ref} |
| **FIB** | Forwarding table that the data plane reads, built from the RIB. [§5.8](#s5-8){.ref} |
| **Flow control** | Receiver limits the sender's rate through the advertised window. [§3.9](#s3-9){.ref} |
| **Four-way handshake** | Exchange that derives fresh Wi-Fi session keys from the PMK. [§6.7](#s6-7){.ref} |
| **Fragmentation** | Splitting a datagram so that it fits a smaller MTU. [§3.5](#s3-5){.ref} |
| **gNMI** | gRPC interface for configuration and streaming telemetry from devices. [§10.12](#s10-12){.ref} |
| **GRE** | Tunnel protocol that carries packets inside IP, adding 24 bytes. [§4.14](#s4-14){.ref} |
| **Hash table** | Array indexed by a hash of the key, giving O(1) average lookup. [§1.3](#s1-3){.ref} |
| **Heap** | Tree-shaped priority queue with the smallest or largest key at the root. [§1.10](#s1-10){.ref} |
| **HSRP** | Cisco first-hop redundancy: routers share one virtual IP and MAC. [§4.8](#s4-8){.ref} |
| **iBGP** | BGP inside one AS; routes learnt from iBGP are not re-advertised to iBGP peers. [§4.7](#s4-7){.ref} |
| **ICMP** | Control protocol for errors and diagnostics, such as echo and unreachable. [§3.5](#s3-5){.ref} |
| **Idempotent** | Applying it twice leaves the same state as applying it once. [§10.9](#s10-9){.ref} |
| **IKE** | Protocol that negotiates IPsec keys and security associations. [§9.7](#s9-7){.ref} |
| **Interrupt** | Hardware signal that makes the CPU run a handler. [§7.8](#s7-8){.ref} |
| **IPsec** | Suite that authenticates and encrypts IP packets using AH or ESP. [§9.7](#s9-7){.ref} |
| **IPv6** | 128-bit addressing with a fixed 40-byte header and no router fragmentation. [§3.7](#s3-7){.ref} |
| **Jinja2** | Python template language that renders configurations from data. [§10.6](#s10-6){.ref} |
| **LACP** | Standard protocol that negotiates EtherChannel bundles. [§4.3](#s4-3){.ref} |
| **Link-state** | Routers flood topology and each runs SPF to compute its own routes. [§4.5](#s4-5){.ref} |
| **Load balancer** | Spreads connections or requests over a pool of servers. [§5.9](#s5-9){.ref} |
| **Local preference** | BGP attribute, higher wins, steering outbound traffic inside an AS. [§4.7](#s4-7){.ref} |
| **Longest-prefix match** | Of the matching routes, use the one with the most specific mask. [§1.9](#s1-9){.ref} |
| **LRU cache** | Evicts the least recently used entry; a hash map plus a doubly linked list. [§1.15](#s1-15){.ref} |
| **LSA** | OSPF advertisement describing routers, networks or external routes. [§4.5](#s4-5){.ref} |
| **MAC address** | 48-bit Layer 2 address of an interface. [§3.3](#s3-3){.ref} |
| **MED** | BGP hint telling a neighbour AS which entry to prefer; lower wins. [§4.7](#s4-7){.ref} |
| **MIMO** | Several antennas send parallel streams over one channel. [§6.2](#s6-2){.ref} |
| **MLO** | Wi-Fi 7 feature that uses several bands or links at once. [§6.9](#s6-9){.ref} |
| **MPLS** | Forwards by short labels instead of IP lookups; carries L3VPNs. [§4.10](#s4-10){.ref} |
| **MSS** | Largest TCP payload per segment: the MTU minus IP and TCP headers. [§3.5](#s3-5){.ref} |
| **MTU** | Largest packet a link carries without fragmentation. [§3.5](#s3-5){.ref} |
| **Multicast** | One sender, many chosen receivers, using 224.0.0.0/4. [§4.12](#s4-12){.ref} |
| **Mutex** | Lock held by one thread at a time to protect a critical section. [§7.5](#s7-5){.ref} |
| **Namespace** | Kernel-isolated copy of network resources such as interfaces and routes. [§8.5](#s8-5){.ref} |
| **NAPI** | Linux receive mode that polls the NIC under load instead of interrupting. [§7.12](#s7-12){.ref} |
| **NAT** | Rewrites addresses in transit, usually private to public. [§3.6](#s3-6){.ref} |
| **NAV** | Wi-Fi timer that marks the medium busy for a duration heard in a frame. [§6.4](#s6-4){.ref} |
| **NETCONF** | XML protocol over SSH for configuring devices, with candidate datastores. [§10.11](#s10-11){.ref} |
| **Netfilter** | Linux packet-filtering framework behind iptables and nftables. [§8.12](#s8-12){.ref} |
| **Netmiko** | Python library for multi-vendor SSH sessions to network devices. [§10.4](#s10-4){.ref} |
| **Normalisation** | Splitting tables so that each fact is stored once. [§12.9](#s12-9){.ref} |
| **NSSA** | OSPF area that admits external routes as type 7 instead of type 5. [§4.5](#s4-5){.ref} |
| **OFDM** | Splits a channel into orthogonal subcarriers that carry data in parallel. [§6.2](#s6-2){.ref} |
| **OFDMA** | Wi-Fi 6 sharing of subcarriers among several stations in one transmission. [§6.9](#s6-9){.ref} |
| **OpenFlow** | Protocol by which a controller programs the flow tables of switches. [§5.7](#s5-7){.ref} |
| **OSI model** | Seven-layer reference model of network functions. [§3.2](#s3-2){.ref} |
| **OSPF** | Link-state interior protocol with areas and Dijkstra; IP protocol 89. [§4.5](#s4-5){.ref} |
| **Oversubscription** | Ratio of server-facing bandwidth to uplink bandwidth in a fabric. [§5.2](#s5-2){.ref} |
| **P4** | Language that defines how a programmable switch parses and forwards packets. [§5.7](#s5-7){.ref} |
| **Paging** | Memory divided into fixed-size pages mapped through page tables. [§7.7](#s7-7){.ref} |
| **PAT** | NAT that shares one address by using different port numbers. [§3.6](#s3-6){.ref} |
| **PDU** | Protocol data unit: segment, packet or frame, according to the layer. [§3.2](#s3-2){.ref} |
| **PKI** | Hierarchy of certificate authorities and certificates that establishes trust. [§9.3](#s9-3){.ref} |
| **PMF** | 802.11w protection of management frames against forged deauthentication. [§6.7](#s6-7){.ref} |
| **Pointer** | Variable that holds a memory address. [§2.3](#s2-3){.ref} |
| **Post-mortem** | Blameless written analysis of an incident and its fixes. [§11.7](#s11-7){.ref} |
| **Prefix list** | Matches routes by prefix and length range, using ge and le. [§4.9](#s4-9){.ref} |
| **Prefix sum** | Running total that answers range-sum queries in O(1). [§1.2](#s1-2){.ref} |
| **Priority inversion** | A low-priority lock holder delays a high-priority waiter. [§7.6](#s7-6){.ref} |
| **Process** | A running program with its own address space and resources. [§7.2](#s7-2){.ref} |
| **QoS** | Treating traffic classes differently by marking, queueing and policing. [§4.11](#s4-11){.ref} |
| **QUIC** | UDP-based transport with built-in TLS and per-stream loss recovery. [§3.10](#s3-10){.ref} |
| **Race condition** | Result depends on the timing of unsynchronised accesses. [§7.5](#s7-5){.ref} |
| **RADIUS** | UDP AAA protocol, common for network access and 802.1X. [§9.12](#s9-12){.ref} |
| **RIB** | Routing table of all learnt routes, from which the best are chosen. [§5.8](#s5-8){.ref} |
| **Route distinguisher** | Prefix that makes VPN routes unique; route targets control import. [§4.10](#s4-10){.ref} |
| **Route map** | Ordered match-and-set policy applied to routes or packets. [§4.9](#s4-9){.ref} |
| **Route reflector** | iBGP speaker that re-advertises routes so a full mesh is unnecessary. [§4.7](#s4-7){.ref} |
| **RTT** | Time for a packet to reach the peer and return. [§3.9](#s3-9){.ref} |
| **SCALPEL** | The seven-step troubleshooting framework of this book. [§11.2](#s11-2){.ref} |
| **SDN** | Separates the control plane from the data plane under a central controller. [§5.7](#s5-7){.ref} |
| **Security group** | Stateful cloud firewall attached to an instance. [§5.11](#s5-11){.ref} |
| **Semaphore** | Counter with wait and post operations, used for synchronisation. [§7.5](#s7-5){.ref} |
| **SLAAC** | IPv6 hosts build their own address from a router advertisement. [§3.7](#s3-7){.ref} |
| **Sliding window** | Technique that moves a range along an array while keeping a running summary. [§1.2](#s1-2){.ref} |
| **Slow start** | TCP phase in which cwnd doubles every round trip until ssthresh. [§3.9](#s3-9){.ref} |
| **Socket** | Communication endpoint identified by address, port and protocol. [§7.10](#s7-10){.ref} |
| **Source of truth** | Authoritative data from which device configuration is generated. [§10.6](#s10-6){.ref} |
| **Spanning tree** | Protocol that blocks redundant Layer 2 links to prevent loops. [§4.3](#s4-3){.ref} |
| **SPF** | Dijkstra run over the link-state database to compute shortest paths. [§4.5](#s4-5){.ref} |
| **SSID** | Network name that an access point advertises. [§6.3](#s6-3){.ref} |
| **STAR** | Situation, task, action, result: a frame for behavioural answers. [§12.12](#s12-12){.ref} |
| **Stateful firewall** | Tracks connections and permits replies to permitted flows. [§9.6](#s9-6){.ref} |
| **Structure padding** | Compiler-inserted bytes that align members to their natural boundary. [§2.7](#s2-7){.ref} |
| **Subnet mask** | Bits that mark the network part of an address. [§3.4](#s3-4){.ref} |
| **SYN flood** | Attack that fills a server with half-open connections; SYN cookies resist it. [§9.10](#s9-10){.ref} |
| **System call** | Controlled entry from user mode into the kernel. [§7.8](#s7-8){.ref} |
| **TCAM** | Memory that matches ternary patterns in one cycle, used for LPM and ACLs. [§5.8](#s5-8){.ref} |
| **TCP** | Reliable, ordered byte stream with flow and congestion control. [§3.9](#s3-9){.ref} |
| **TIME_WAIT** | State kept by the active closer for 2 MSL after closing. [§3.9](#s3-9){.ref} |
| **TLB** | Cache of recent page-table translations. [§7.7](#s7-7){.ref} |
| **TLS** | Protocol that gives encryption, integrity and authentication over TCP. [§9.4](#s9-4){.ref} |
| **Token bucket** | Tokens refill at rate r up to burst B; each packet spends tokens. [§1.15](#s1-15){.ref} |
| **Trie** | Tree indexed by the characters or bits of a key, used for prefix lookups. [§1.9](#s1-9){.ref} |
| **Trunk** | Link that carries several VLANs using 802.1Q tags. [§4.2](#s4-2){.ref} |
| **TTL** | Hop limit decremented at each router; at zero the packet is dropped. [§3.5](#s3-5){.ref} |
| **UDP** | Connectionless transport with an 8-byte header and no delivery guarantee. [§3.9](#s3-9){.ref} |
| **Undefined behaviour** | Code to which the C standard gives no meaning; any result is allowed. [§2.12](#s2-12){.ref} |
| **Union-find** | Disjoint-set structure with near-constant find and unite. [§1.11](#s1-11){.ref} |
| **UPF** | 5G user-plane function that forwards subscriber traffic. [§6.12](#s6-12){.ref} |
| **uRPF** | Drops packets whose source address has no valid reverse route. [§9.10](#s9-10){.ref} |
| **VLAN** | Virtual Layer 2 broadcast domain separated by tags. [§4.2](#s4-2){.ref} |
| **VLSM** | Subnets of different sizes carved from one block, largest first. [§3.4](#s3-4){.ref} |
| **volatile** | C qualifier that forces every access to memory; it gives no atomicity. [§2.6](#s2-6){.ref} |
| **VPC** | Isolated virtual network in a public cloud. [§5.11](#s5-11){.ref} |
| **VRF** | Separate routing-table instance on one router. [§4.9](#s4-9){.ref} |
| **vtable** | Table of function pointers used for virtual calls in C++. [§2.20](#s2-20){.ref} |
| **VTEP** | Device that encapsulates and decapsulates VXLAN traffic. [§5.5](#s5-5){.ref} |
| **VXLAN** | Layer 2 over UDP port 4789 with a 24-bit segment identifier. [§5.5](#s5-5){.ref} |
| **Wildcard mask** | Inverted mask used in ACLs and OSPF network statements. [§3.4](#s3-4){.ref} |
| **WPA3-SAE** | Password exchange that resists offline dictionary attacks. [§6.7](#s6-7){.ref} |
| **YANG** | Language that models configuration and state data of devices. [§10.10](#s10-10){.ref} |
| **Zero trust** | No implicit trust from network location; verify every request. [§9.14](#s9-14){.ref} |
| **Zombie process** | Exited process whose parent has not yet collected its status. [§7.2](#s7-2){.ref} |

:::
:::

:::
