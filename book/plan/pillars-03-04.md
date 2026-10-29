# Chapter Plan — Pillar 3 (Computer Networks Fundamentals) and Pillar 4 (Routing & Switching, CCNA → CCNP)

> Planning document only. No final prose. British spelling throughout (CLI keywords such as `neighbor` keep vendor spelling).
> Difficulty tags: **[E]** easy / fresher screen, **[M]** medium / core technical round, **[H]** hard / bar-raiser or CCNP-level.
> Company tags: CSC Cisco · QCM Qualcomm · GOO Google · MSF Microsoft · AMZ Amazon (NDE) · JNP Juniper · ARI Arista · NOK Nokia · BRC Broadcom.

## Blueprint alignment notes (read before writing)

- **CCNA 200-301 v1.1** domains (weights to be re-verified against Cisco's official exam-topics PDF before print; the PDF host was not reachable from the research session): 1.0 Network Fundamentals 20% · 2.0 Network Access 20% · 3.0 IP Connectivity 25% · 4.0 IP Services 10% · 5.0 Security Fundamentals 15% · 6.0 Automation & Programmability 10%. v1.1 adds AI/ML-in-networking and Terraform mentions in 6.0. **Third-party sources report v1.1 retires 2 Feb 2027 and CCNA v2.0 goes live 3 Feb 2027 under the same 200-301 code. Plan a revision pass for the book's second print.**
- **CCNP ENCOR 350-401**: v1.2 reported live from 19 Mar 2026. Domains: 1.0 Architecture 15% · 2.0 Virtualisation 10% · 3.0 Infrastructure 30% · 4.0 Network Assurance 10% · 5.0 Security 20% · 6.0 Automation & AI 15%. Pillar 4 covers mainly 3.0 (L2, L3, IP services, multicast) and parts of 1.0 (QoS, design) and 2.0 (VRF, GRE). VXLAN/LISP/SD-Access go to Pillar 5. IPsec and 802.1X go to Pillar 9. NETCONF/RESTCONF go to Pillar 10.
- **What interviewers actually ask** (from Glassdoor, Naukri Code360, Jointaro and Reddit reports, 2012–2026, all self-reported):
  - Cisco wants subnetting without a calculator (network, broadcast and usable range), STP scenarios, OSPF LSA types, BGP attributes and path selection. One candidate was asked to code "does IP X belong to subnet Y" with bitwise operations.
  - Amazon NDE covers iBGP/eBGP topologies and path manipulation, BGP attributes, MSS vs MTU, TCP "know it well", Python, and Leadership Principles stories (worst outage). One reviewer called it "CCIE level".
  - Meta, Arista and Juniper style rounds ask about iBGP loop avoidance, route reflectors and clusters, BGP ECMP, spine-leaf, and where EVPN fits.
  - Qualcomm and Google ask about sliding window, flow control vs congestion control, and "simulate the TCP window" as a coding task.
- Cross-pillar handshakes:
  - P1 DSA: Dijkstra/Bellman-Ford, trie-based longest-prefix match.
  - P2 Programming: bit manipulation for subnet calculation, struct packing for headers.
  - P7 OS & sockets: socket API and the kernel TCP stack.
  - P8 Linux: `ip`, `ss`, `tcpdump`, `tc`.
  - P9 Security: ACLs in depth, IPsec, L2 security.
  - P11 Troubleshooting: layered methodology. Every chapter ends with a "fault-find" box feeding P11.

## Book-wide conventions applied to Pillars 3–4 (added per user update)

1. **Priority tags (navigation aid, not a trimming device).** Every section heading carries `[MUST]`, `[SHOULD]` or `[OPTIONAL]`, sometimes with a company qualifier (e.g. `[SHOULD, MUST for JNP/NOK]`). All content stays in the book; tags only help readers order their study.
   - **MUST:** asked in most fresher loops at most target companies.
   - **SHOULD:** frequently asked, or core for a subset of companies.
   - **OPTIONAL:** depth/CCNP-level material that differentiates candidates.
   - Typeset the tags as coloured pills in the margin (MUST = solid indigo, SHOULD = outlined indigo, OPTIONAL = grey). Repeat them in the chapter TOC and in every question-bank entry.
2. **Full in-book solutions for every question.** Every interview question (50 in P3, 55 in P4) and every worked example, drill and lab task has a complete answer printed in the book. Each solution follows a fixed template:
   - **30-second answer:** what to say first in an interview.
   - **Full answer:** the derivation and reasoning, with numbers.
   - **Diagram:** a reference to the in-book figure, or a mini-diagram inline.
   - **Likely follow-ups:** 2–3 interviewer follow-ups, each with a short answer.
   - **Common wrong answers:** each with an explanation of why it is wrong.
   - **Section back-reference.**
   - **Scenario and coding questions:** these also get a step-by-step troubleshooting/solution path, plus complete, tested code (Python/C) with sample I/O.
   - **Placement:** solutions sit in the end-of-chapter pack, not beside the questions, so readers can self-test first. Questions carry a page link to their solution.
3. **Self-contained rule.** Nothing requires external lookup.
   - Every lab prints its full topology, full startup and solution configs, expected `show` outputs, and an annotated table of the key capture frames. The companion repo is a convenience copy only.
   - An appendix covers tool installation (Packet Tracer, GNS3, Containerlab + FRR/cEOS/SR Linux, Wireshark, iperf3, netns/tc) and a Linux/IOS command primer.
   - RFC facts used in the text are stated in the text, and RFC numbers are for optional further reading only.
4. **Page impact.** Solutions and the end-of-chapter pack add ~50 pp to P3 (new total ≈ 240 pp) and ~65 pp to P4 (new total ≈ 295 pp).
5. **Fast path (optional reading-order aid).** A boxed "Fast path through MUST sections" on each pillar's opener lists study days for MUST-only coverage. This is a navigation aid only; the full chapter plan is unchanged.
   - **P3 MUST path ≈ 12 study days:** 3.1 ½, 3.2 ½, 3.3-Ethernet 1, 3.4 2, 3.5 1, 3.6 1½, 3.9 3, 3.11 1, plus pack/revision 1½.
   - **P4 MUST path ≈ 15 study days:** 4.2 1½, 4.3 2, 4.4 1, 4.5 3, 4.7 4, 4.13 1½, plus pack/revision 2.
   - **Full chapters:** keep the week estimates given in each pillar header.

---

# PILLAR 3 — Computer Networks Fundamentals

**Title:** *"From Cable to Cloud: How the Internet Really Works"*
**One-line promise:** You will be able to trace any packet, from a keystroke to a Google data centre and back, naming every header field, address and protocol decision on the way.

- **Prerequisites:** Binary/hex conversion and bitwise AND/OR (P2 ch. 1 or appendix A), basic probability (for efficiency formulas), and the ability to run Wireshark and a Linux shell (P8 ch. 1). No prior networking assumed.
- **Estimated pages:** ~190, made up of 11 sections of ~15 pp, plus a 12 pp cheat-sheet/question bank and a 10 pp capstone.
- **Weeks to study:** 5 weeks at ~12 h/week (4 for a CS student who has done a CN course, 6 for ECE/EEE).
- **Suggested week split:** W1 3.1–3.3 · W2 3.4–3.5 (subnetting drills daily) · W3 3.6–3.8 · W4 3.9 (TCP deep dive) · W5 3.10–3.11 + capstone + mock interview.

## Learning objectives

1. Explain the OSI and TCP/IP models and map 25 named protocols to their layer, giving the PDU name at each layer.
2. Describe encapsulation and decapsulation, and state which header fields change at each router hop and which do not.
3. Decode an Ethernet II / 802.1Q frame, an IPv4 header, an IPv6 header, and TCP and UDP headers from a hex dump.
4. Compute CRC remainders, Hamming codes and Stop-and-Wait / Go-Back-N / Selective-Repeat efficiency and window limits.
5. Subnet any IPv4 block by hand in under 60 seconds: network, broadcast, usable range, host count, wildcard mask. Design VLSM plans and summarise routes.
6. Explain ARP, gratuitous ARP and proxy ARP, DHCP DORA with relay, and NAT/PAT translation tables, with packet-level detail.
7. Write IPv6 addresses in compressed form, derive EUI-64 and solicited-node addresses, and explain NDP (RS/RA/NS/NA), SLAAC and DHCPv6.
8. Explain IPv4 fragmentation, MTU, Path MTU Discovery and MSS clamping, and diagnose PMTUD black holes.
9. Draw the TCP state machine, handshake and teardown with sequence/ACK numbers. Explain TIME_WAIT, RST, SYN cookies, window scaling and SACK.
10. Distinguish flow control from congestion control. Trace cwnd/ssthresh through slow start, congestion avoidance, fast retransmit and fast recovery (Tahoe, Reno, NewReno). Contrast CUBIC and BBR.
11. Explain DNS resolution (recursive vs iterative), record types, TTL/caching, and the HTTP/1.1 → HTTP/2 → HTTP/3 (QUIC) evolution with the TLS 1.3 handshake.
12. Deliver a fluent, 5-minute, layer-by-layer answer to "What happens when you type google.com and press Enter?".
13. Contrast distance-vector and link-state routing (Bellman-Ford vs Dijkstra), including count-to-infinity and its fixes. This bridges to Pillar 4.

## Section-by-section outline

### 3.1 Why networks exist: topologies, devices and the layered idea  `[MUST]`
- **Core idea:** A network shares resources by moving bits between devices. Layering lets each part evolve independently.
- **Analogy:** A city's road system. Hubs are a roundabout where everyone hears every horn, switches are a smart junction with signposts per house, and routers are inter-city motorway interchanges.
- **Content:**
  - LAN/MAN/WAN.
  - Bus/star/ring/mesh, with a full-mesh link count of n(n−1)/2.
  - Hub vs switch vs router vs L3 switch vs firewall vs AP.
  - Collision and broadcast domains.
  - Circuit vs packet switching.
  - Bandwidth, throughput, latency (transmission, propagation, queuing, processing) and jitter.
- **Worked example:** Send a 1 MB file over a 10 Mb/s link 2,000 km long (v = 2×10⁸ m/s).
  - Transmission delay = 8×10⁶ / 10⁷ = 0.8 s.
  - Propagation delay = 2×10⁶ / 2×10⁸ = 10 ms.
  - Total ≈ 0.81 s (ignoring queuing).
  - Then the same file over 1 Gb/s: transmission 8 ms, propagation still 10 ms. Lesson: on fast links, latency is dominated by distance.
- **Figures:**
  - F3.1a: Four-panel topology icons (bus, star, ring, partial mesh), each with link-count formula labels.
  - F3.1b: "Domain counting" diagram of 1 router, 2 switches, 1 hub and 8 PCs, with collision domains outlined in dashed orange and broadcast domains in shaded blue. Caption asks "count them" (answer: 2 broadcast domains, 7 collision domains). *The authoring team must verify this count after fixing the exact topology.*
  - F3.1c: Stacked bar of the four delay components for a single packet.
- **Lab:** Packet Tracer. Build hub-vs-switch topologies, use Simulation mode to watch a ping flood every port on the hub but only one port on the switch, and screenshot the event list.

### 3.2 The OSI and TCP/IP models and encapsulation  `[MUST]`
- **Core idea:** Each layer adds its own header (and sometimes a trailer) so its peer layer at the far end can act on it. Data becomes segment, then packet, then frame, then bits.
- **Analogy:** The postal system.
  - The letter (data) goes into an envelope with the department name (port/L4), then a postal envelope with the city address (IP/L3), then a courier van labelled for the next depot (MAC/L2).
  - The van changes at every depot, but the postal address does not.
- **Content:**
  - Layers 7→1 and the mnemonic ("All People Seem To Need Data Processing").
  - TCP/IP 4-layer vs 5-layer models.
  - PDU names; where devices operate; where protocols sit (ARP's "2.5" ambiguity; ICMP at L3; TLS between L4 and L7).
  - SAPs and multiplexing via EtherType, IP protocol number and port.
- **Worked example:** Header overhead of an HTTP GET carrying 100 bytes of payload.
  - TCP 20 + IPv4 20 + Ethernet 14 + FCS 4 = 58 bytes, plus 8 bytes preamble/SFD and 12 bytes IFG on the wire.
  - Efficiency = 100/178 ≈ 56%.
  - Repeat for a 1,460-byte payload: 1460/1538 ≈ 94.9%.
- **Figures:**
  - F3.2a: Side-by-side OSI (7) vs TCP/IP (4) columns, with protocol chips in each row (HTTP, DNS, TLS, TCP, UDP, QUIC, IP, ICMP, ARP, Ethernet, 802.11) and device icons in the margin (hub L1, switch L2, router L3, LB/firewall L4–7).
  - F3.2b: An "Encapsulation Russian doll". Horizontal nested boxes [Eth hdr | IP hdr | TCP hdr | HTTP data | FCS], colour-coded per layer and reused consistently throughout the book: L2 teal, L3 indigo, L4 amber, L7 rose.
  - F3.2c: Two-host, one-router stack diagram. A U-shaped arrow goes down the sender's stack, up to L3 in the router, then down and up the receiver's stack.
- **Lab:** Wireshark. Open a capture of `curl http://example.com`, expand each layer in the packet-details pane, and colour-map it to F3.2b. Print an annotated frame table in the book (self-contained); the .pcapng in the companion repo is a convenience copy only.

### 3.3 Physical and data-link layers: Ethernet, framing, error control and ARQ  `[MUST: Ethernet/MAC/switching] [SHOULD: CRC/Hamming/ARQ, which is MUST for QCM/BRC/NOK]`
- **Core idea:** L2 delivers frames reliably across one link. Framing finds the boundaries, the MAC address picks the receiver, CRC detects damage, and ARQ (where used) repairs it.
- **Analogy:**
  - CSMA/CD is a polite dinner table: listen before speaking, and if two people start at once, both stop and wait a random time.
  - CRC is a checksum digit on a cheque.
- **Content:**
  - Cabling (UTP Cat5e/6/6a, fibre SMF/MMF, SFP/QSFP), duplex/auto-negotiation, and duplex mismatch symptoms.
  - Ethernet II frame layout, MAC address structure (OUI, I/G bit, U/L bit), unicast/multicast/broadcast.
  - CSMA/CD and the minimum frame size; CSMA/CA preview (wireless, P6).
  - Framing (byte/bit stuffing); parity, checksum, CRC, Hamming.
  - Stop-and-Wait, Go-Back-N and Selective Repeat, with window limits and efficiency.
  - Switch learning/flooding/forwarding/filtering; cut-through vs store-and-forward.
- **Worked examples:**
  1. **CRC:** Data 1101011011, generator 10011 (x⁴+x+1).
     - Append four 0s, then long-divide mod-2.
     - Remainder 1110, so the transmitted frame is 11010110111110.
     - Show the receiver check yielding remainder 0.
  2. **Minimum frame for CSMA/CD:** 10 Mb/s, 2,500 m, v = 2×10⁸ m/s.
     - Tp = 12.5 µs, so 2Tp = 25 µs.
     - Lmin = 25 µs × 10 Mb/s = 250 bits.
     - Link to the real-world 512-bit (64-byte) minimum, which includes repeater margins.
  3. **ARQ efficiency:** 1 Mb/s link, 1,000-bit frames, Tp = 20 ms.
     - Tt = 1 ms, so a = Tp/Tt = 20.
     - Stop-and-Wait η = 1/(1+2a) = 1/41 ≈ 2.4%.
     - A window of 41 frames is needed for 100%.
     - Minimum sequence bits: GBN needs window ≤ 2ⁿ−1, so n = 6. SR needs window ≤ 2ⁿ⁻¹, so n = 7.
  4. **Hamming(7,4):** Encode 1011, flip bit 5, and locate the error via the syndrome.
- **Figures:**
  - F3.3a: Byte-accurate Ethernet II frame bar: Preamble 7 | SFD 1 | Dst MAC 6 | Src MAC 6 | EtherType 2 | Payload 46–1500 | FCS 4. Under it is the 802.1Q variant with a 4-byte tag (TPID 0x8100 | PCP 3b | DEI 1b | VID 12b) inserted after Src MAC. Annotate the minimum of 64 B and the maximum of 1518/1522 B.
  - F3.3b: MAC address bit-diagram with the I/G and U/L bits highlighted in the first octet.
  - F3.3c: Three stacked timing diagrams (sender/receiver vertical time axes) for SW, GBN (window 4, frame 2 lost, frames 2–5 resent) and SR (window 4, only frame 2 resent).
  - F3.3d: Mod-2 long-division worked layout for the CRC example.
  - F3.3e: Switch MAC-learning storyboard in 4 frames (empty CAM → A sends → flood → B replies → learned).
- **Labs:**
  - Packet Tracer: `show mac address-table` before and after pings, and `clear mac address-table dynamic`.
  - Wireshark: filter `eth.dst == ff:ff:ff:ff:ff:ff`.
  - Python mini-exercise: compute CRC-32 of a byte string and compare with `zlib.crc32`.

### 3.4 IPv4 addressing, subnetting, VLSM and CIDR  `[MUST]`
- **Core idea:** An IPv4 address is 32 bits split by the mask into network and host parts. Subnetting moves that split to fit the number of hosts you need.
- **Analogy:**
  - The PIN code and house number. The mask decides how many digits are "PIN code".
  - VLSM is cutting a pizza into unequal slices, biggest slice first.
- **Content:**
  - Dotted-decimal/binary; classful history (A/B/C/D/E) and why it died.
  - Private ranges (RFC 1918); special addresses (0.0.0.0, 127/8, 169.254/16 APIPA, 100.64/10 CGNAT, 255.255.255.255).
  - Prefix length, magic number / block-size method, wildcard masks, /31 point-to-point (RFC 3021), /32 host routes.
  - Summarisation/supernetting; longest-prefix-match preview.
- **Worked examples:**
  1. **Quick subnet:** 172.16.45.200/21.
     - Mask 255.255.248.0, so the block is 8 in the 3rd octet, and 45 falls in the 40 block.
     - Network 172.16.40.0, broadcast 172.16.47.255, usable 172.16.40.1–172.16.47.254.
     - Hosts 2¹¹−2 = 2046. Wildcard 0.0.7.255.
  2. **VLSM:** Given 192.168.10.0/24, with LANs of 100, 50 and 25 hosts and two P2P WAN links.
     - 100 hosts → /25 192.168.10.0 (usable .1–.126, bcast .127).
     - 50 hosts → /26 192.168.10.128 (.129–.190, bcast .191).
     - 25 hosts → /27 192.168.10.192 (.193–.222, bcast .223).
     - WAN1 → /30 192.168.10.224 (.225–.226).
     - WAN2 → /30 192.168.10.228 (.229–.230).
     - Spare: 192.168.10.232/29 and 192.168.10.240/28.
  3. **Summarisation:** 10.1.4.0/24 … 10.1.7.0/24 → 10.1.4.0/22. Counter-example: 10.1.5.0–10.1.8.0 cannot be summarised as a single /22 without over-claiming.
  4. **"Same subnet?" check:** Are 10.10.10.130/26 and 10.10.10.190/26 on the same subnet? Yes, both are in .128/26. Is 10.10.10.193? No, it is in .192/26. Cisco reports a coding variant: write `in_subnet(ip, cidr)` with bitwise AND (cross-ref P2).
- **Figures:**
  - F3.4a: The 32-bit ruler. 4 octets in binary with a sliding "mask line" at /21, network bits shaded indigo, host bits white, and the network/broadcast derivation shown as AND/OR operations.
  - F3.4b: The **subnetting master table** (also the cheat sheet), with columns: prefix /8–/32, dotted mask, wildcard, block size and octet, addresses, usable hosts.
  - F3.4c: VLSM "address-space bar". A horizontal 0–255 bar for the last octet, cut into coloured segments for each allocated subnet and grey for spare.
  - F3.4d: Summarisation binary-alignment diagram. Four /24s stacked in binary, with common bits boxed to reveal /22.
- **Labs:**
  - Paper drills: 30 timed problems in a "Subnetting Sprint" appendix, target < 45 s each.
  - Packet Tracer: implement the VLSM plan above on 3 routers and verify reachability.
  - Python: a 30-line subnet calculator using `ipaddress`, then a version without it (bitwise only).

### 3.5 The IPv4 header, fragmentation, MTU and ICMP  `[MUST]`
- **Core idea:** The IP header carries what every router needs to forward a packet. When a packet is bigger than the next link's MTU, it is fragmented, or dropped if DF is set.
- **Analogy:**
  - Fragmentation is shipping a sofa in numbered flat-pack boxes ("box 2 of 3, starts at panel 185").
  - TTL is a "use-by" stamp decremented at every depot.
- **Content:**
  - Every IPv4 header field with bit widths.
  - TTL and why traceroute works; protocol numbers; header checksum recomputed per hop.
  - Identification/flags/fragment offset (8-byte units); reassembly only at the destination.
  - MTU vs MSS; PMTUD via ICMP Type 3 Code 4; black-hole routers; MSS clamping.
  - ICMP types (0, 3, 5, 8, 11); ping and traceroute on Windows (ICMP) vs Linux (UDP 33434+).
- **Worked examples:**
  1. **Fragmentation:** A 4,000-byte datagram (20 B header + 3,980 B data) crosses a link with MTU 1,500. Max data per fragment = 1,480 (a multiple of 8). The table shows Total Length, offset and MF for each fragment:

     | Frag | Data | Total Length | Offset (×8) | MF |
     |---|---|---|---|---|
     | 1 | 1480 | 1500 | 0 | 1 |
     | 2 | 1480 | 1500 | 185 | 1 |
     | 3 | 1020 | 1040 | 370 | 0 |

  2. **Hex decode:** Decode the hex dump `45 00 00 3c 1c 46 40 00 40 06 b1 e6 c0 a8 00 68 c0 a8 00 01`.
     - Version 4, IHL 5 (20 B), total length 60, ID 0x1c46, DF set, TTL 64, protocol 6 (TCP).
     - Src 192.168.0.104, dst 192.168.0.1. Verify the checksum by hand.
  3. **MSS:** With MTU 1500, MSS = 1500 − 20 − 20 = 1460. Over a PPPoE MTU of 1492, MSS is 1452. Explain why `ip tcp adjust-mss 1452` fixes "some websites won't load".
- **Figures:**
  - F3.5a: **IPv4 header bit-layout**, 32 bits wide × 5 rows (+ options), with exact field widths: Ver 4 | IHL 4 | DSCP 6 | ECN 2 | Total Length 16 / Identification 16 | Flags 3 | Fragment Offset 13 / TTL 8 | Protocol 8 | Header Checksum 16 / Source 32 / Destination 32. Bit numbers 0–31 run across the top, and the fields that change per hop (TTL, checksum, and fragmentation fields if fragmenting) are highlighted.
  - F3.5b: Fragmentation diagram. The original datagram bar is split into 3 coloured fragments with offset/MF labels.
  - F3.5c: Traceroute ladder. Source and 3 routers, with probes at TTL 1/2/3, each answered by an ICMP Time Exceeded from successive routers and a final Echo Reply / Port Unreachable.
  - F3.5d: PMTUD black-hole sequence. An ICMP "frag needed" is filtered by a firewall, so the connection hangs after the handshake.
- **Labs:**
  - Linux: `ping -M do -s 1472 8.8.8.8` succeeds; `-s 1473` fails, showing the 1500 MTU.
  - Wireshark: capture `traceroute` and `tracert`, then compare UDP vs ICMP probes.
  - GNS3/Containerlab: set a mid-path link to MTU 1400 and observe fragmentation vs DF drops.

### 3.6 ARP, DHCP and NAT: the glue protocols  `[MUST]`
- **Core idea:**
  - ARP maps a next-hop IP to a MAC.
  - DHCP hands out IP settings automatically.
  - NAT rewrites addresses so many private hosts share a few public ones.
- **Analogies:**
  - ARP: shouting in a hostel corridor "Who is room 10? Tell Ravi", and only room 10 answers.
  - DHCP: the hotel reception's four steps (Discover "anyone at reception?", Offer "room 204?", Request "yes, 204 please", Acknowledge "here is your key card valid 24 h").
  - NAT/PAT: an office switchboard. One public number with extensions.
- **Content:**
  - ARP request/reply format, ARP cache and timeouts, gratuitous ARP (duplicate detection, failover), proxy ARP, ARP spoofing (pointer to P9).
  - DHCP DORA with ports UDP 67/68, broadcast flag, lease/T1 (50%)/T2 (87.5%) renewals, relay (`ip helper-address`, giaddr), options 3/6/51/43/82.
  - Static NAT, dynamic NAT, PAT/overload; inside/outside local/global terminology; port forwarding; NAT traversal problems; CGNAT.
- **Worked example: the packet walk with MAC/IP at each hop.**
  - **Topology:**
    - PC-A 192.168.1.10/24, MAC AA:AA.
    - R1 G0/0 192.168.1.1 (MAC 11:11, inside) and G0/1 203.0.113.2 (MAC 12:12, outside, PAT).
    - ISP router 203.0.113.1 (MAC 21:21) and 198.51.100.1 (MAC 22:22).
    - Web server 198.51.100.80 (MAC BB:BB).
  - **Step 1, PC-A:** The destination is off-subnet, so PC-A ARPs for 192.168.1.1.
  - **Steps 2–4, the four legs:**

    | Leg | Src MAC | Dst MAC | Src IP:port | Dst IP:port |
    |---|---|---|---|---|
    | PC-A→R1 | AA:AA | 11:11 | 192.168.1.10:51000 | 198.51.100.80:80 |
    | R1→ISP | 12:12 | 21:21 | 203.0.113.2:51000 (or remapped port) | 198.51.100.80:80 |
    | ISP→Server | 22:22 | BB:BB | 203.0.113.2:51000 | 198.51.100.80:80 |
    | Return | reversed | reversed | — | R1 un-NATs back to 192.168.1.10:51000 |

  - **NAT table:** Show the `show ip nat translations` row: inside local 192.168.1.10:51000 · inside global 203.0.113.2:51000 · outside local/global 198.51.100.80:80.
  - **DHCP extra:** Put the DHCP server on a different subnet, with relay on R1 (giaddr 192.168.1.1). Show src/dst IPs for each of the 4 DORA messages: client 0.0.0.0→255.255.255.255, relay unicast to the server.
- **Figures:**
  - F3.6a: **Packet-walk strip.** Topology across the top, with under each link a "header card" showing L2 src/dst (changes, highlighted teal) and L3 src/dst (constant except at NAT, highlighted indigo).
  - F3.6b: ARP request/reply ladder, with frame fields (sender MAC/IP, target MAC/IP, opcode 1/2), the broadcast vs unicast destination MAC, and the cache entry created on both sides.
  - F3.6c: **DHCP DORA ladder** with relay: Client | Relay (R1) | Server columns, 4 arrows each labelled with src/dst IP, src/dst port and key options.
  - F3.6d: NAT four-quadrant diagram of inside/outside × local/global addresses.
- **Labs:**
  - Packet Tracer: configure a DHCP pool on a router, a relay on a second router and PAT overload. Use `debug ip nat` and `show ip dhcp binding`.
  - Wireshark: `arp || dhcp` while running `sudo dhclient -r && sudo dhclient`.
  - Linux: `ip neigh`, then `arping` a duplicate IP.

### 3.7 IPv6 essentials  `[SHOULD, MUST for QCM/NOK/JNP]`
- **Core idea:** IPv6 uses 128-bit addresses, a fixed 40-byte header, no broadcast, no router fragmentation, and NDP (built on ICMPv6) in place of ARP.
- **Analogy:** Moving from 10-digit phone numbers to a numbering plan so large that every grain of sand gets a number. "Neighbour discovery" is a neighbourhood WhatsApp group replacing shouting in the corridor.
- **Content:**
  - Notation and compression rules (leading zeros; a single `::`).
  - Address types: GUA 2000::/3, ULA FC00::/7, link-local FE80::/10, multicast FF00::/8, ::1, ::/128.
  - Anycast; prefix sizes (/48 site, /64 subnet).
  - EUI-64; SLAAC vs stateless DHCPv6 vs stateful DHCPv6 (RA M/O flags); privacy addresses.
  - NDP messages (RS 133, RA 134, NS 135, NA 136, Redirect 137); DAD; solicited-node multicast.
  - Header and extension headers; transition (dual stack, 6to4/tunnels, NAT64/DNS64).
- **Worked examples:**
  1. **Compression:** 2001:0DB8:0000:0000:0000:FF00:0042:8329 → 2001:db8::ff00:42:8329. Trap: 2001:db8:0:0:1:0:0:1 → 2001:db8::1:0:0:1, with `::` used only once, on the longest run, and on the leftmost run if tied.
  2. **EUI-64:** MAC 00:1A:2B:3C:4D:5E.
     - Split it and insert FFFE: 001A:2BFF:FE3C:4D5E.
     - Flip the 7th bit: 00→02.
     - Interface ID 021A:2BFF:FE3C:4D5E, giving link-local FE80::21A:2BFF:FE3C:4D5E.
  3. **Solicited-node:** For the address above, FF02::1:FF3C:4D5E (FF02::1:FF + last 24 bits). The multicast MAC is 33:33:FF:3C:4D:5E.
  4. **Subnetting:** Split 2001:db8:acad::/48 into /64s. There are 65,536 subnets; list the first 3 and the last one.
- **Figures:**
  - F3.7a: **IPv6 header bit-layout** (32-bit rows): Ver 4 | Traffic Class 8 | Flow Label 20 / Payload Length 16 | Next Header 8 | Hop Limit 8 / Source 128 / Destination 128. Beside it, a ghosted IPv4 header with "removed" fields struck through.
  - F3.7b: EUI-64 transformation flow (MAC → split → FFFE insert → bit-7 flip → interface ID), with the flipped bit circled.
  - F3.7c: SLAAC sequence ladder (host link-local + DAD NS → RS to FF02::2 → RA with prefix/flags → GUA formed → DAD).
  - F3.7d: Address-type "map" chart: prefix, scope ring (link/site/global), example.
- **Labs:**
  - Packet Tracer: dual-stack 2 routers, `ipv6 unicast-routing`, SLAAC on hosts, static IPv6 routes.
  - Wireshark: filter `icmpv6.type == 134`.
  - Linux: `ip -6 addr`, `ip -6 neigh`, `ping ff02::1%eth0`.

### 3.8 Routing concepts and algorithms (bridge to Pillar 4)  `[SHOULD]`
- **Core idea:** Routers forward by longest-prefix match against a routing table. The table is filled statically or by algorithms that are distance-vector (talk to neighbours) or link-state (map the whole network).
- **Analogy:**
  - Distance-vector is following road signs that only say "Delhi 200 km this way".
  - Link-state is every driver holding the full Google Map and computing their own shortest route.
- **Content:**
  - Forwarding vs routing; longest-prefix match; default route.
  - Bellman-Ford; count-to-infinity and its fixes (split horizon, poison reverse, hold-down, triggered updates); RIP basics.
  - Dijkstra and SPF; path-vector (BGP) preview.
  - Intra- vs inter-domain routing; AS numbers.
- **Worked examples:**
  1. **Dijkstra by table:** A 5-node graph A–E with edges A-B 4, A-C 2, B-C 1, B-D 5, C-D 8, C-E 10, D-E 2. Show the tentative/permanent table per iteration. Final distances: B 3 (via C), C 2, D 8 (A-C-B-D), E 10 (A-C-B-D-E, beating A-C-E = 12).
  2. **Count-to-infinity:** Three routers A–B–C and the C-network fails. Show B and A ping-ponging metrics 2, 3, 4 … 16 (RIP infinity), then re-run with split horizon.
  3. **Longest-prefix match:** The table holds 10.0.0.0/8 → R1, 10.1.0.0/16 → R2, 10.1.1.0/24 → R3, 0.0.0.0/0 → R4. Look up 10.1.1.5 (R3), 10.1.2.5 (R2), 10.2.0.1 (R1) and 11.0.0.1 (R4).
- **Figures:**
  - F3.8a: Dijkstra iteration panels (small multiples). The graph is redrawn 5 times with the permanent set shaded and the tentative distances in node badges.
  - F3.8b: Count-to-infinity table animation (rows = time, columns = A's and B's distance to net-C).
  - F3.8c: Binary trie for LPM with the four prefixes above and the lookup paths highlighted (cross-ref P1 trie).
- **Labs:**
  - Python: implement Dijkstra (heapq) and Bellman-Ford over the same graph, and print the routing tables (cross-ref P1).
  - Packet Tracer: RIPv2 on a triangle; break a link and watch convergence with `debug ip rip`.

### 3.9 Transport layer: UDP, TCP, flow control and congestion control (flagship section, ~30 pp)  `[MUST]`
- **Core idea:**
  - UDP is a thin, connectionless "ports + checksum" service.
  - TCP builds a reliable, ordered, flow- and congestion-controlled byte stream over unreliable IP, using sequence numbers, ACKs, timers and windows.
- **Analogies:**
  - UDP is a postcard; TCP is a registered parcel with signatures.
  - **Flow control** is the receiver saying "my bucket can take only 3 more litres" (rwnd).
  - **Congestion control** is a driver sensing traffic: speed up gently on empty roads, brake hard on a jam (AIMD).
  - BBR is a driver who measures the road's speed limit and length, then drives exactly at that pace.
- **Sub-sections and content:**
  1. Ports and sockets; the 4-tuple/5-tuple; well-known/registered/ephemeral ranges.
  2. UDP header (8 B); when UDP wins (DNS, VoIP, gaming, QUIC).
  3. TCP header and every field; flags (CWR ECE URG ACK PSH RST SYN FIN); options (MSS, WS, SACK-permitted, timestamps).
  4. 3-way handshake; ISN randomisation; simultaneous open; SYN flood and SYN cookies.
  5. 4-way teardown; half-close; TIME_WAIT (2×MSL) and why it exists; CLOSE_WAIT leaks (server bug symptom); RST cases.
  6. TCP state machine (all 11 states).
  7. Reliability: cumulative ACK, delayed ACK, RTO estimation (SRTT/RTTVAR, Jacobson/Karels, Karn's algorithm), fast retransmit (3 dup ACKs), SACK.
  8. Flow control: rwnd, sliding window, zero window and persist timer, silly window syndrome, Nagle, the Nagle + delayed-ACK interaction.
  9. Throughput limits: window/RTT, BDP, window scaling, the Mathis formula (intuition only).
  10. Congestion control: slow start, ssthresh, congestion avoidance (AIMD), Tahoe vs Reno vs NewReno, CUBIC (Linux default; cubic growth around W_max), BBR (models BtlBw and RTprop; pacing; v1 vs v2/v3 fairness concerns), ECN, an AQM pointer (RED/CoDel).
  11. TCP vs UDP vs QUIC comparison table.
- **Worked examples:**
  1. **Handshake numbers:** Client ISN = 1000, server ISN = 5000.
     - SYN (seq 1000), then SYN-ACK (seq 5000, ack 1001), then ACK (seq 1001, ack 5001).
     - The client sends 500 B (seq 1001), and the server ACKs 1501.
     - FIN from the client (seq 1501), ACK 1502.
  2. **cwnd trace (exam classic):** MSS = 1 segment unit, initial cwnd = 1, ssthresh = 16.
     - RTT 1–5: 1, 2, 4, 8, 16 (slow start).
     - RTT 6–9: 17, 18, 19, 20 (CA).
     - Timeout at 20 (Tahoe/any): ssthresh = 10, cwnd = 1, then 2, 4, 8, 10, 11 …
     - Alternatively, 3 dup ACKs at 20 under Reno: ssthresh = 10, cwnd = 10 (+3 inflation), then linear.
     - Plot both as a line chart.
  3. **Throughput ceiling:** rwnd 65,535 B, RTT 100 ms gives max ≈ 5.24 Mb/s. For a 1 Gb/s × 100 ms path, BDP = 12.5 MB, so a window-scale factor ≥ 8 (65,535 × 2⁸ ≈ 16.8 MB) is needed.
  4. **RTO computation:** α = 1/8, β = 1/4. Start with SRTT = 100 ms and RTTVAR = 25 ms, then feed samples 120 ms and 80 ms. Compute RTO = SRTT + 4·RTTVAR each step.
  5. **Sliding-window simulation (Google/Qualcomm coding variant):** Write pseudo-code for a sender with window N, a timer per oldest unacked segment, and handling of cumulative ACKs.
- **Figures:**
  - F3.9a: **TCP header bit-layout** (32-bit rows): Src Port 16 | Dst Port 16 / Sequence 32 / Acknowledgement 32 / Data Offset 4 | Rsvd 4 | Flags 8 | Window 16 / Checksum 16 | Urgent Ptr 16 / Options.
  - F3.9b: UDP header bit-layout (2 rows), placed next to F3.9a for scale.
  - F3.9c: **Ladder diagram of the 3-way handshake** with seq/ack numbers from worked example 1, client states (SYN_SENT → ESTABLISHED) and server states (LISTEN → SYN_RCVD → ESTABLISHED) on the timeline margins.
  - F3.9d: **4-way teardown ladder**, with FIN_WAIT_1/2, CLOSE_WAIT, LAST_ACK and TIME_WAIT labelled, and a 2MSL bracket.
  - F3.9e: **TCP state machine** (RFC 9293 style). Rounded-rectangle states; arrows labelled "event / action" (e.g. "rcv SYN / snd SYN,ACK"); client path in solid blue and server path in dashed green.
  - F3.9f: Sliding-window strip: a byte line with segments "sent & ACKed | sent not ACKed | usable window | cannot send yet" and the window edges moving after an ACK (two-row before/after).
  - F3.9g: **cwnd vs RTT line chart** for Tahoe and Reno on the same axes, with ssthresh as a dashed horizontal line and annotated events (timeout, 3-dup-ACK).
  - F3.9h: CUBIC growth curve: concave approach to W_max, plateau, convex probe. Beside it a BBR pacing-gain cycle diagram (1.25, 0.75, 1 × 6) with the "BtlBw × RTprop = BDP" operating point on a delivery-rate vs inflight plot (the Kleinrock optimal point vs the loss-based operating point).
  - F3.9i: Fast-retransmit ladder showing segment 3 lost, dup ACKs for 3 ×3, and retransmission before RTO.
- **Labs:**
  - Wireshark: open the handshake capture and enable Statistics → TCP Stream Graphs → Stevens; set relative vs absolute sequence numbers.
  - Linux, two network namespaces + `tc qdisc add dev veth0 root netem delay 50ms loss 1%`:
    - Run `iperf3` with `sysctl net.ipv4.tcp_congestion_control=cubic` and then `=bbr`.
    - Watch `ss -ti` cwnd/rtt fields and plot throughput.
  - Python sockets: an echo server that never calls `close()`; observe CLOSE_WAIT in `ss -tan` (cross-ref P7).
  - `hping3 -S` SYN to a closed port, then capture the RST.

### 3.10 Application layer: DNS, HTTP, TLS, QUIC and friends  `[SHOULD, MUST for GOO/MSF/AMZ]`
- **Core idea:** The application layer gives names (DNS), documents and APIs (HTTP), secrecy (TLS) and lower latency (HTTP/2 multiplexing, HTTP/3 over QUIC).
- **Analogy:**
  - DNS is the phone directory hierarchy: ask the national exchange (root) which state directory (.com) holds "google", then ask Google's own receptionist (authoritative).
  - A TLS handshake is exchanging sealed ID cards and agreeing a secret handshake before talking.
- **Content:**
  - DNS hierarchy; recursive vs iterative; stub/recursive/authoritative roles.
  - Record types (A, AAAA, CNAME, MX, NS, SOA, PTR, TXT, SRV, CAA); TTL and negative caching; UDP 53 and the TCP fallback (truncation, zone transfers).
  - DNSSEC overview, DoH/DoT, anycast DNS (8.8.8.8, 1.1.1.1).
  - HTTP methods, status codes and persistent connections; HTTP/2 binary framing, streams, HPACK, TCP head-of-line problem; HTTP/3/QUIC (UDP 443, connection IDs, 0-RTT).
  - TLS 1.2 vs 1.3 handshake (2-RTT vs 1-RTT), certificates/CA chain, SNI.
  - Others in a table: SMTP/POP3/IMAP, FTP active/passive, SSH, SNMP, NTP, Telnet.
- **Worked example:** `dig +trace www.google.com` walk-through. Annotate the root → `com.` NS (a.gtld-servers.net) → `google.com.` NS (ns1.google.com) → A record, with TTLs. Then `dig www.google.com @8.8.8.8` twice to show the cached TTL decreasing.
- **Figures:**
  - F3.10a: DNS resolution diagram. Client → recursive resolver, with numbered arrows to root, TLD and authoritative servers (iterative), and the reply path; recursion and iteration labelled distinctly.
  - F3.10b: TLS 1.3 handshake ladder (ClientHello+key_share → ServerHello+key_share, {EncryptedExtensions, Certificate, CertificateVerify, Finished} → {Finished} → application data), with the RTT bracket. Beside it, the TLS 1.2 ladder ghosted for comparison.
  - F3.10c: Protocol-stack comparison of HTTP/1.1 / HTTP/2 / HTTP/3 (HTTP/2 over TLS over TCP vs HTTP/3 over QUIC over UDP).
  - F3.10d: HoL-blocking illustration. 3 streams over one TCP connection with one lost packet stalling all, vs QUIC stalling only the affected stream.
- **Labs:**
  - Wireshark: capture `dns` and `tls.handshake`; decrypt TLS using `SSLKEYLOGFILE` with a browser.
  - `curl -v --http3 https://cloudflare.com` (if built with HTTP/3) vs `--http2`.
  - `nslookup -type=mx gmail.com`.

### 3.11 Capstone: "What happens when you type google.com and press Enter?"  `[MUST]`
- **Core idea:** Every concept in this pillar fires in sequence within roughly 100 ms. A strong answer is layered, ordered and quantified.
- **Analogy:** Ordering a pizza by phone. Find the number (DNS), dial and confirm the line (TCP + TLS), place the order (HTTP), the pizza is delivered in boxes over roads (IP routing, Ethernet hops), and you assemble the slices (rendering).
- **Structure: the "11-step answer" scaffold students memorise.**
  1. Browser parses the URL, checks HSTS and its caches (browser → OS → hosts file).
  2. DNS: the stub resolver sends a UDP 53 query to the configured resolver (from DHCP), which runs the recursive lookup.
  3. ARP for the default gateway (if not cached).
  4. TCP 3-way handshake to the IP on 443, or QUIC over UDP 443.
  5. TLS 1.3 handshake, SNI, certificate validation.
  6. HTTP GET; Google's anycast front end / load balancer; responses (301 redirect to www, 200).
  7. At each router hop: TTL decrement, LPM lookup, L2 rewrite; PAT at the home router.
  8. Inside Google: GFE, LB, backend (pointer to P5).
  9. Response returns; TCP congestion window grows.
  10. Browser renders: parse HTML, fetch subresources (more connections/streams).
  11. Connection reuse / teardown.
- **Three "depth dial" versions:** a 60-second fresher answer, a 5-minute standard answer, and a 15-minute "keep going deeper" answer with interviewer interrupts such as "what if DNS is cached?", "what if the gateway's MAC is unknown?", "what if the TLS certificate expired?" and "how does the reply find your laptop behind NAT?".
- **Figures:**
  - F3.11a: **Full-page hero illustration.** A horizontal swim-lane timeline with lanes Browser | OS / stub resolver | Home router (NAT) | ISP | DNS resolver | Google edge. Numbered events 1–11 have approximate ms timestamps (e.g. DNS 20 ms, TCP 15 ms, TLS 15 ms, first byte 40 ms).
  - F3.11b: Layer-by-layer packet "x-ray" of the first TLS ClientHello frame leaving the laptop, with every header field filled in using realistic values.
- **Lab:** Record the full sequence in one Wireshark capture after `ipconfig /flushdns` / `resolvectl flush-caches` and `arp -d`. A guided worksheet asks the student to find the frame numbers for each of the 11 steps.

## Pillar 3 labs summary table

| Section | Tool | Lab | Deliverable |
|---|---|---|---|
| 3.1 | Packet Tracer | Hub vs switch flooding | Screenshot + domain count |
| 3.2 | Wireshark | Layer colour-mapping of an HTTP GET | Annotated pcap |
| 3.3 | PT + Python | MAC learning; CRC-32 check | CAM table before/after; script |
| 3.4 | PT + Python | VLSM 3-router build; subnet calculator | Working pings; `subnet.py` |
| 3.5 | Linux + Containerlab | MTU/DF probing; mid-path MTU 1400 | ping output; pcap |
| 3.6 | PT + Wireshark | DHCP relay + PAT; DORA capture | `show ip nat translations` |
| 3.7 | PT + Linux | Dual-stack SLAAC | RA capture |
| 3.8 | Python + PT | Dijkstra/Bellman-Ford; RIP convergence | Routing tables |
| 3.9 | Linux netns + tc + iperf3 | CUBIC vs BBR under 50 ms / 1% loss | Throughput plot; `ss -ti` log |
| 3.10 | Wireshark + dig | DNS trace; TLS decrypt | Annotated trace |
| 3.11 | Wireshark | Full google.com walk | 11-step worksheet |

## Pillar 3 company-tag matrix
H = frequently reported / core to role, M = sometimes, L = rare. These are indicative only, based on aggregated self-reported interviews and role descriptions.

| Topic | CSC | QCM | GOO | MSF | AMZ NDE | JNP | ARI | NOK | BRC |
|---|---|---|---|---|---|---|---|---|---|
| OSI/TCP-IP + encapsulation | H | H | M | H | H | H | M | H | M |
| "Type google.com" walk | H | M | H | H | H | M | M | M | L |
| Subnetting/VLSM by hand | H | M | M | M | H | H | H | H | M |
| Ethernet / MAC / switching basics | H | M | L | M | M | H | H | H | H |
| CRC / ARQ / sliding window | M | H | M | M | L | M | L | H | H |
| IPv4 header / fragmentation / MTU-MSS | H | H | M | M | H | H | H | H | H |
| ARP / DHCP / NAT | H | M | M | H | H | H | M | M | M |
| IPv6 / NDP | M | H | M | M | M | H | M | H | M |
| TCP handshake / states / TIME_WAIT | H | H | H | H | H | H | H | M | M |
| TCP congestion (Reno/CUBIC/BBR) | M | H | H | H | H | M | M | M | M |
| DNS / HTTP / TLS / QUIC | M | L | H | H | H | L | L | L | L |
| Routing algorithms (Dijkstra/BF) | H | M | H | M | M | H | H | H | M |

Rationale notes for the authors:
- Qualcomm and Broadcom lean towards protocol-stack internals (ARQ, windows, headers, IPv6 for cellular).
- Google and Microsoft lean towards TCP behaviour and application performance.
- Amazon NDE leans towards MTU/MSS, TCP and DNS operations.
- Juniper, Arista and Nokia lean towards L2/L3 forwarding.

## Pillar 3 interview question bank (50). Every question has a full solution in the P3 end-of-chapter pack (§3.E4); each entry is also tagged MUST/SHOULD/OPTIONAL by its section

**Models and L2**
1. [E] Name the OSI layers and give one protocol and one device for each. (all)
2. [E] What is the difference between a hub, a switch and a router, in terms of collision and broadcast domains? (CSC, NOK)
3. [E] Which header fields change at each router hop, and which never change (absent NAT)? (CSC, AMZ, JNP)
4. [M] Why is the minimum Ethernet frame 64 bytes? Derive it from CSMA/CD. (QCM, BRC)
5. [M] Explain how a switch learns MAC addresses. What happens when the CAM table is full? (CSC, ARI, BRC)
6. [M] Compute the CRC for data 1101011011 with generator 10011. (QCM, NOK)
7. [M] With 3-bit sequence numbers, what are the maximum GBN and SR windows, and why? (QCM, BRC)
8. [M] Stop-and-Wait on a 1 Mb/s link with 1,000-bit frames and Tp = 20 ms: what is the efficiency, and what window gives 100%? (QCM)
9. [H] Cut-through vs store-and-forward: which has lower latency, which propagates errored frames, and why do data-centre switches (Arista) offer cut-through? (ARI, BRC)

**IPv4, subnetting, fragmentation**
10. [E] Give the network, broadcast and usable range for 172.16.45.200/21, without a calculator. (CSC, AMZ)
11. [E] How many usable hosts are on a /27? On a /31? Why is /31 allowed on point-to-point links? (CSC, JNP)
12. [M] Design a VLSM plan from 192.168.10.0/24 for 100, 50 and 25 hosts and two WAN links. (CSC, NOK)
13. [M] Summarise 10.1.4.0/24–10.1.7.0/24. Can you summarise 10.1.5.0–10.1.8.0 into one /22? (CSC, JNP)
14. [M] Write a function `in_subnet(ip, cidr)` using only bitwise operations. (CSC, GOO, ARI)
15. [M] Fragment a 4,000-byte datagram for MTU 1,500. Give the offsets and MF flags. (QCM, BRC, JNP)
16. [M] MTU vs MSS: what is the MSS over PPPoE? What does `ip tcp adjust-mss` do? (AMZ, CSC)
17. [H] *Scenario:* Users can ping a website and complete the TCP handshake, but the page never loads. Large transfers hang. What is happening, and how do you prove it? (PMTUD black hole) (AMZ, MSF, CSC)
18. [M] How does traceroute work on Linux vs Windows? Why do you sometimes see `* * *`? (AMZ, CSC)
19. [E] What is APIPA (169.254/16), and what does it tell you about DHCP? (MSF, CSC)

**ARP, DHCP, NAT**
20. [E] Explain DHCP DORA with ports and addresses. Why is Discover broadcast? (CSC, MSF)
21. [M] How does DHCP work when the server is on another subnet? What is giaddr? (CSC, JNP)
22. [M] What is gratuitous ARP, and where is it used? (FHRP failover, duplicate detection) (CSC, ARI)
23. [M] Walk a packet from PC-A to a web server through a PAT router. Give the MAC/IP/port at each hop. (CSC, AMZ, GOO)
24. [H] *Scenario:* Two hosts behind different NATs need peer-to-peer VoIP. Why does it fail, and how do STUN/TURN/ICE help? (QCM, MSF)
25. [M] Proxy ARP: what is it, and what problem can it hide? (CSC)

**IPv6**
26. [E] Compress 2001:0DB8:0000:0000:0000:FF00:0042:8329. (CSC, NOK)
27. [M] Derive the EUI-64 link-local address from MAC 00:1A:2B:3C:4D:5E. (CSC, JNP)
28. [M] How does IPv6 replace ARP? What is a solicited-node multicast address? (QCM, NOK, JNP)
29. [M] SLAAC vs DHCPv6. What do the RA M and O flags mean? (CSC, QCM)
30. [H] Why don't IPv6 routers fragment? What breaks if ICMPv6 is blocked? (AMZ, GOO)

**TCP/UDP**
31. [E] TCP vs UDP: give three applications for each and justify. (all)
32. [E] Draw the 3-way handshake with ISNs 1000 and 5000. (all)
33. [M] Why is the handshake 3-way and not 2-way? (GOO, MSF, QCM)
34. [M] Explain TIME_WAIT. Why 2×MSL? Which side enters it? What happens on a busy proxy with thousands of TIME_WAIT sockets? (GOO, AMZ, MSF)
35. [M] A server shows thousands of CLOSE_WAIT sockets. Whose bug is it? (MSF, AMZ)
36. [M] Flow control vs congestion control: which window is which, and what is the effective send window? (QCM, GOO, AMZ)
37. [M] Trace cwnd: initial 1, ssthresh 16, timeout at 20. What happens with Tahoe, and with Reno on 3 dup ACKs? (QCM, MSF)
38. [H] CUBIC vs BBR: what signal does each react to? Why can BBR v1 be unfair to CUBIC? (GOO, MSF, AMZ)
39. [H] Compute max throughput for rwnd 64 KB and RTT 100 ms. How do you fill a 1 Gb/s, 100 ms path? (GOO, AMZ)
40. [M] Explain fast retransmit and SACK. Why are 3 dup ACKs used, not 1? (QCM, GOO)
41. [H] Nagle + delayed ACK: why does an interactive app see 40–200 ms stalls, and how do you fix it? (GOO, MSF)
42. [M] What is a SYN flood? How do SYN cookies work? (CSC, AMZ, MSF)
43. [H] *Coding:* Simulate a sliding-window sender. Given an ACK stream and a timeout, output which segments are retransmitted. (GOO, QCM)
44. [M] When does a TCP stack send RST? (CSC, JNP)

**Application and capstone**
45. [E] What happens when you type google.com and press Enter? Start at the keyboard. (all; Google/Microsoft/Amazon expect depth)
46. [M] Recursive vs iterative DNS. What do TTL and negative caching do? When does DNS use TCP? (AMZ, GOO, MSF)
47. [M] CNAME vs A vs ALIAS. Why can't you CNAME a zone apex? (AMZ, MSF)
48. [M] TLS 1.2 vs 1.3: how many RTTs does each need, and what is SNI? (GOO, MSF)
49. [H] HTTP/2 vs HTTP/3: what is head-of-line blocking, and how does QUIC remove it? (GOO, MSF)
50. [H] *Scenario:* A website is slow only for users in one city. Give a step-by-step plan covering DNS geo-routing, anycast path, MTU and packet loss. (AMZ, GOO)

## Pillar 3 trap boxes ("Gotcha!" call-outs, red-bordered)
- The MAC changes at every hop but the IP does not, except through NAT. Students often say the opposite under pressure.
- "Usable hosts = 2ⁿ − 2" fails for /31 (2 usable on P2P per RFC 3021) and /32.
- Fragment offset is in **8-byte units**. Writing 1480 instead of 185 is the classic error.
- MSS excludes IP and TCP headers. MTU excludes the Ethernet header and FCS.
- `::` may appear only once in an IPv6 address.
- The EUI-64 bit flip is the 7th bit from the left of the first byte (U/L), not the last bit.
- A TCP SYN and FIN each consume one sequence number, but a pure ACK does not.
- TIME_WAIT sits on the side that **actively closes**, which is not necessarily the client.
- Flow control (rwnd) protects the receiver, while congestion control (cwnd) protects the network. Effective window = min(rwnd, cwnd).
- Slow start is exponential growth, not slow. It is "slow" only relative to blasting the whole window at once.
- Reno halves on 3 dup ACKs but resets to 1 on timeout. Do not conflate the two.
- DNS is not "UDP only". It uses TCP for responses > 512 B without EDNS0, for truncation and for zone transfers.
- Traceroute on Linux uses UDP by default, while Windows `tracert` uses ICMP. Firewalls treat them differently.
- A switch floods unknown unicast, but that is not the same as broadcasting.

## Pillar 3 one-page cheat sheet (contents). Printed as the one-page revision sheet §3.E2
1. OSI ↔ TCP/IP mapping with PDUs and devices.
2. **Subnetting table:** /16–/32, mask, wildcard, block size, hosts; "magic number" rule; powers of 2 up to 2¹⁶.
3. Private and special IPv4 ranges; IPv6 address-type prefixes; EUI-64 steps.
4. **Well-known ports:**
   - 20/21 FTP, 22 SSH, 23 Telnet, 25 SMTP, 53 DNS, 67/68 DHCP, 69 TFTP, 80 HTTP, 110 POP3, 123 NTP, 143 IMAP, 161/162 SNMP, 179 BGP, 389 LDAP, 443 HTTPS/QUIC, 514 syslog, 520 RIP, 646 LDP, 830 NETCONF, 3389 RDP, 4789 VXLAN, 6653 OpenFlow.
   - IP protocol numbers: 1 ICMP, 2 IGMP, 6 TCP, 17 UDP, 47 GRE, 50 ESP, 51 AH, 58 ICMPv6, 88 EIGRP, 89 OSPF, 103 PIM, 112 VRRP.
   - EtherTypes: 0x0800 IPv4, 0x0806 ARP, 0x86DD IPv6, 0x8100 802.1Q, 0x8847 MPLS.
5. Header sizes: Ethernet 14 + 4 FCS (+4 tag), IPv4 20–60, IPv6 40, TCP 20–60, UDP 8, VXLAN overhead 50.
6. ICMP type/code mini-table (0, 3/0–4, 5, 8, 11); ICMPv6 NDP types 133–137.
7. TCP flags; state list; handshake/teardown thumbnails; key timers (TIME_WAIT 2MSL; RTO min 200 ms on Linux / 1 s per RFC 6298).
8. Congestion-control cheat: slow start (cwnd += 1 MSS per ACK), CA (+1 MSS per RTT), 3 dup ACKs (Reno: ssthresh = cwnd/2, cwnd = ssthresh + 3), timeout (ssthresh = cwnd/2, cwnd = 1); one line each on CUBIC and BBR.
9. Formulas: transmission delay L/R; propagation d/v; SW efficiency 1/(1+2a); throughput ≤ W/RTT; BDP = R × RTT.
10. DHCP DORA ports/addresses; DNS record types.

## Pillar 3 mini-project — "PacketScope: a teaching packet dissector and subnet toolkit"
- **Brief:** Build a Python CLI with three tools.
  - `pscope subnet 172.16.45.200/21` prints network, broadcast, range, wildcard, and the binary ruler as ASCII art.
  - `pscope parse capture.pcap` uses raw `struct` unpacking (no Scapy for the core) to decode Ethernet/802.1Q/IPv4/IPv6/TCP/UDP/ICMP/ARP/DNS, flag TCP handshakes, and compute per-flow RTT from SYN→SYN-ACK.
  - `pscope cwnd log.txt` reads `ss -ti` samples taken during the 3.9 iperf3 lab and plots cwnd vs time for CUBIC vs BBR.
- **Stretch goal:** Detect the retransmissions and dup ACKs in a capture, reproducing Wireshark's "TCP Analysis Flags".
- **Interview value:** Hits bit manipulation (Cisco/Arista), protocol parsing (Qualcomm/Broadcom) and TCP performance (Google/Amazon). Include a 3-line résumé bullet template.

## Pillar 3 end-of-chapter pack (~50 pp)
- **§3.E1 Short notes (~11 pp):**
  - One page per section (3.1–3.11) in tight bullets: key definitions, numbers to memorise and one thumbnail figure. Each page ends with a "say this in an interview" one-liner.
  - Example items for 3.9: "cwnd vs rwnd; eff. window = min"; "3 dup ACK → ssthresh = cwnd/2"; "TIME_WAIT = active closer, 2MSL".
- **§3.E2 One-page revision sheet:** the cheat-sheet contents above, laid out as a single dense, colour-coded A4 page, with a perforated/tear-out style border in print.
- **§3.E3 Flashcards (~90 cards, 2-up per page, front/back, tagged MUST/SHOULD/OPTIONAL):**
  - Ports and protocol numbers (~20).
  - Header field widths (~10).
  - Subnet quick-fires (~15, e.g. "/27 → hosts? block?" = "30, 32").
  - IPv6 prefixes and EUI-64 (~8).
  - TCP states/flags and congestion rules (~15).
  - DNS record types and DHCP DORA ports (~8).
  - Definitions such as BDP, MSS, PMTUD, Nagle (~14).
- **§3.E4 Solved interview problems:**
  - (a) Full solutions to all 50 bank questions, in the template above.
  - (b) **10 long-form solved problems:**
    1. A VLSM design for a 6-department college campus from 10.20.0.0/22, with the full allocation table.
    2. A fragmentation chain over two links (MTU 1500 → 576).
    3. A hex-dump decode of a full Ethernet/IPv4/TCP SYN frame.
    4. A cwnd trace with mixed timeout and 3-dup-ACK events over 25 RTTs, with plot.
    5. A BDP/window-scaling sizing for a Mumbai–Virginia 1 Gb/s path (RTT ≈ 190 ms).
    6. The ARP + DHCP relay + PAT packet walk table (complete).
    7. IPv6 SLAAC + DAD sequence with all addresses computed.
    8. A Dijkstra + Bellman-Ford comparison on one graph.
    9. The PMTUD black-hole diagnosis scenario, written as a mock-interview dialogue.
    10. "Type google.com" model answers at 60 s, 5 min and 15 min, with interviewer interrupts and answers.
  - (c) All 30 subnetting-sprint drills and every lab task, with answers and expected outputs.

---

# PILLAR 4 — Routing & Switching (CCNA → CCNP Enterprise)

**Title:** *"Building the Network: Switching, Routing and the Protocols that Run the Internet"*
**One-line promise:** You will configure, verify and troubleshoot VLANs, STP, OSPF, EIGRP, BGP, FHRPs, MPLS, QoS and multicast on real CLIs, and explain every state machine and selection rule well enough to survive a CCIE-flavoured interview loop.

- **Prerequisites:** All of Pillar 3, especially 3.3, 3.4, 3.6 and 3.8. Basic Linux shell (P8). Packet Tracer installed; GNS3 or Containerlab with FRRouting / Arista cEOS / Nokia SR Linux images (free) for the later sections.
- **Estimated pages:** ~230, made up of 14 sections of ~15 pp, plus a 20 pp question bank, cheat sheet and mini-project.
- **Weeks to study:** 7 weeks at ~12–14 h/week. Weeks 1–4 cover the CCNA core (4.1–4.6); weeks 5–7 cover CCNP topics (4.7–4.14). A student targeting only the CCNA level can stop after week 4 + 4.8 FHRP.
- **Suggested week split:**
  - W1: 4.1 CLI and device internals, 4.2 VLANs/trunks.
  - W2: 4.3 STP/RSTP and EtherChannel.
  - W3: 4.4 static routing and the routing table, 4.5 OSPF part 1.
  - W4: 4.5 OSPF part 2 (multi-area, LSAs), 4.13 IP services and ACLs.
  - W5: 4.6 EIGRP, 4.8 FHRP, 4.9 redistribution/VRF/PBR.
  - W6: 4.7 BGP (double week).
  - W7: 4.10 MPLS, 4.11 QoS, 4.12 multicast, 4.14 overlays + mini-project.

## Learning objectives

1. Navigate Cisco IOS/IOS-XE (with Junos, EOS and SR Linux equivalence tables); configure, save, verify and recover devices.
2. Explain the RIB vs FIB vs adjacency table vs CAM/TCAM, and process vs fast vs CEF switching.
3. Configure and troubleshoot VLANs, access/trunk ports, 802.1Q, native VLAN, DTP/VTP risks, and inter-VLAN routing (ROAS and SVI).
4. Predict the STP root bridge, port roles and states for any topology. Compare 802.1D, RSTP, PVST+ and MST. Apply PortFast, BPDU Guard, Root Guard and Loop Guard correctly.
5. Bundle links with EtherChannel (LACP/PAgP/static) and troubleshoot mismatches.
6. Read a routing table and predict forwarding using longest-prefix match → AD → metric; build floating static and default routes.
7. Configure single- and multi-area OSPFv2/v3. Recite the neighbour states, DR/BDR election and LSA types 1/2/3/4/5/7, and the area types. Fix adjacency failures (MTU, timers, area, auth, network type).
8. Compute EIGRP composite metrics. Apply the DUAL feasibility condition. Explain stuck-in-active and stub routers.
9. Explain BGP FSM states, eBGP/iBGP rules (next-hop-self, full mesh, route reflectors, confederations), attributes and the complete path-selection order. Influence inbound and outbound traffic.
10. Configure HSRP/VRRP/GLBP with tracking and preemption; compare their timers, multicast addresses and virtual MACs.
11. Use route maps, prefix lists, redistribution (with loop-prevention tags), PBR and VRF-lite.
12. Explain the MPLS label stack, LDP, PHP and an L3VPN packet walk with RD/RT/VPNv4.
13. Design a QoS policy: classify/mark (DSCP/CoS), queue (LLQ/CBWFQ), police vs shape, WRED.
14. Explain IP multicast: addressing and MAC mapping, IGMPv2/v3 and snooping, PIM-DM/SM/SSM, RP, the RPF check, shared vs source trees.
15. Configure NAT, DHCP relay, NTP, SNMP, syslog and standard/extended ACLs on IOS; place ACLs correctly.
16. Explain GRE, the purpose of IPsec, and where VXLAN/EVPN and SD-WAN fit (handing off to P5/P9).

## Section-by-section outline

### 4.1 Inside the box: device architecture and the CLI  `[SHOULD, MUST for BRC/ARI/JNP]`
- **Core idea:** A router or switch has a control plane (protocols build the RIB), a data plane (the FIB/TCAM forwards at line rate) and a management plane (CLI/SSH/APIs). The CLI is how you talk to all three.
- **Analogy:**
  - The control plane is the city traffic-planning office drawing maps overnight.
  - The data plane is the traffic police at each junction, reading a printed cheat card (FIB) and waving cars through instantly.
- **Content:**
  - Boot sequence (ROM → IOS → startup-config), config register 0x2102/0x2142, password recovery.
  - CLI modes (user/privileged/global/interface/router); `show running-config` vs `startup-config`; `copy run start`; `do`; `?`; abbreviations; `show ip interface brief`.
  - SSH configuration; CDP/LLDP.
  - Process switching vs fast switching vs CEF; RIB vs FIB; adjacency table; TCAM/ASIC (Broadcom Trident/Tomahawk/Jericho context for BRC/ARI).
  - Multi-vendor CLI equivalence table: IOS vs Junos (commit model) vs Arista EOS vs Nokia SR Linux.
- **Worked example:** The first 15 minutes on a new router. Set hostname, enable secret, console/vty passwords, SSH (domain, RSA 2048, `transport input ssh`), interface IPs, banner, save. Then verify with `show ip int brief`, `show cdp neighbors detail` and `show ip ssh`.
- **Figures:**
  - F4.1a: Three-plane layered diagram (management / control / data) of a router chassis, with arrows showing an OSPF packet punted to the CPU vs a transit packet hitting the ASIC fast path.
  - F4.1b: CLI mode "staircase" (Router> → Router# → Router(config)# → Router(config-if)# / (config-router)#) with entry/exit commands on each step.
  - F4.1c: RIB → FIB → adjacency table flow diagram for one prefix.
- **Labs:**
  - Packet Tracer: base config and SSH on 2 routers and 1 switch.
  - Containerlab: `srl` + `ceos` nodes. Run the same "show interfaces" task on each vendor and complete the equivalence table.

### 4.2 Switching, VLANs, trunking and inter-VLAN routing  `[MUST]`
- **Core idea:** VLANs split one physical switch into many logical broadcast domains. Trunks carry many VLANs on one link via 802.1Q tags. A router or L3 switch is needed to move traffic between VLANs.
- **Analogy:**
  - VLANs are colour-coded floors in one office building, each with its own announcement system.
  - A trunk is the lift carrying people of all colours, each wearing a coloured badge (the tag).
  - The native VLAN is people who forgot their badge and get sent to a default floor.
- **Content:**
  - Access vs trunk; 802.1Q tag fields; VLAN ranges (1, 2–1001, 1002–1005 legacy, 1006–4094 extended); native VLAN and mismatch; allowed VLAN lists.
  - DTP modes (dynamic auto/desirable; `switchport nonegotiate`); VTP modes/versions and the "VTP bomb" risk.
  - Voice VLAN; ROAS (sub-interfaces, `encapsulation dot1Q`); SVIs on L3 switches; routed ports.
  - L2 security cross-ref (port security, DHCP snooping, DAI → P9).
- **Worked example:** Two VLANs, 10 SALES 192.168.10.0/24 and 20 ENG 192.168.20.0/24, across SW1–SW2 with a trunk; ROAS on R1 G0/0.10 and G0/0.20.
  - Walk a ping from a SALES PC to an ENG PC, showing the frame tagged VID 10 on the trunk, routed on R1, and returned tagged VID 20.
  - Then convert it to an L3-switch SVI design.
- **Figures:**
  - F4.2a: Physical vs logical view, side by side. One switch with coloured ports vs two separate "virtual switches".
  - F4.2b: 802.1Q tag insertion diagram showing original frame → tagged frame, with FCS recalculation noted, and tag field widths (TPID 16 | PCP 3 | DEI 1 | VID 12).
  - F4.2c: ROAS "hairpin" packet path with tag numbers on each segment.
  - F4.2d: DTP negotiation matrix (rows/cols: access, trunk, dynamic desirable, dynamic auto; cell = resulting mode).
  - F4.2e: VLAN-hopping double-tag attack diagram (pointer to P9).
- **Labs:**
  - Packet Tracer: build the worked example; break it by setting a native VLAN mismatch and removing VLAN 20 from the allowed list. Observe the CDP log messages.
  - Containerlab: the same on cEOS with SVIs.

### 4.3 Spanning Tree (802.1D/RSTP/PVST+/MST) and EtherChannel  `[MUST]`
- **Core idea:**
  - Redundant L2 links create loops, and Ethernet has no TTL, so STP elects a root and blocks just enough ports to form a loop-free tree.
  - EtherChannel bundles parallel links so STP sees them as one.
- **Analogy:**
  - STP is a group of villages electing a capital (root), then each village keeps only its single best road to the capital and barricades the redundant ones.
  - EtherChannel is merging four lanes into one motorway that STP treats as a single road.
- **Content:**
  - Broadcast storms, MAC-table instability, duplicate frames.
  - BPDU fields; Bridge ID = priority (4 bits, multiples of 4096) + extended system ID (VLAN, 12 bits) + MAC.
  - Election steps: root bridge → root port per non-root (lowest root path cost → lowest sender BID → lowest sender port ID) → designated port per segment → others blocked/alternate.
  - Port costs (short: 10M=100, 100M=19, 1G=4, 10G=2; long: 1G=20,000, 10G=2,000).
  - 802.1D states and timers (blocking 20 s max-age, listening 15, learning 15 → up to 50 s); RSTP roles (root, designated, alternate, backup) and states (discarding, learning, forwarding); proposal/agreement; edge ports.
  - PVST+/Rapid PVST+; MST regions/instances.
  - Features: PortFast, BPDU Guard, BPDU Filter, Root Guard, Loop Guard, UDLD.
  - EtherChannel: LACP (active/passive), PAgP (desirable/auto), `on`; load-balancing hashes; consistency (speed/duplex/VLANs); L3 EtherChannel; MLAG/vPC preview (→ P5).
- **Worked example:** A triangle of three switches, all priority 32769 (VLAN 1), with MACs SW1 0000.0000.0001, SW2 …0002 and SW3 …0003, all links 1 Gb/s (cost 4).
  - Root = SW1 (lowest MAC).
  - SW2 and SW3 root ports face SW1.
  - On the SW2–SW3 segment, both have root path cost 4. The tie-break is the lower BID, so SW2's port is designated and SW3's port is blocking/alternate.
  - Part 2: set SW3 priority 4096. Re-elect the root and recompute roles.
  - Part 3: SW1–SW2 is now two parallel links (Gi0/1, Gi0/2). Which one blocks? Answer: SW2 blocks the port that receives the higher sender port ID from SW1.
- **Figures:**
  - F4.3a: **STP election diagram.** A triangle topology with BIDs in each switch box, link costs on edges, port role badges (R/D/B) colour-coded (root port green, designated blue, blocked red ✕) and the root marked with a crown.
  - F4.3b: BPDU / Bridge ID bit-layout: priority 4 bits | ext-sys-ID 12 bits | MAC 48 bits, with "why priority must be a multiple of 4096" annotated.
  - F4.3c: 802.1D port-state timeline bar (Blocking 20 s → Listening 15 s → Learning 15 s → Forwarding) vs the RSTP proposal/agreement sync ladder (sub-second).
  - F4.3d: Feature-placement map. An access/distribution/core diagram showing where PortFast + BPDU Guard (access edge), Root Guard (distribution downlinks) and Loop Guard (non-designated uplinks) go.
  - F4.3e: LACP/PAgP mode compatibility matrix (✓/✕ cells).
- **Labs:**
  - Packet Tracer: build the triangle; `show spanning-tree`; change priorities; shut the root port and time convergence with 802.1D vs `spanning-tree mode rapid-pvst`.
  - Create a broadcast storm deliberately (disable STP) in simulation and watch it.
  - EtherChannel: LACP active/passive; break it with a speed mismatch and observe `show etherchannel summary` flags (SU/P/s/D).

### 4.4 IP routing fundamentals: routing table, static and default routes  `[MUST]`
- **Core idea:** A router picks a route by longest prefix first, then lowest administrative distance (between sources), then lowest metric (within a protocol). Static routes and default routes are the simplest way to fill the table.
- **Analogy:** AD is how much you trust the source of directions: your own eyes (connected, 0) > a printed signboard (static, 1) > a local's advice (OSPF 110) > a stranger's rumour (RIP 120).
- **Content:**
  - Reading `show ip route` (codes, [AD/metric], via, age); connected and local (/32) routes.
  - Recursive lookup; static to next-hop vs exit-interface vs fully specified; floating static (AD 5–254); default route; null0 discard routes.
  - IPv6 static routes; ECMP basics.
  - The full AD table.
- **Worked example:**
  - **Routing table puzzle:** R1 has OSPF 10.1.0.0/16 [110/20], EIGRP 10.1.0.0/16 [90/3072], static 10.1.1.0/24 [1/0] and RIP 10.0.0.0/8 [120/2]. Which entries are installed, and where does 10.1.1.9 go? (Static /24, by longest prefix.) Where does 10.1.5.5 go? (EIGRP, because AD 90 beats OSPF 110 for the same /16.) And 10.200.0.1? (RIP /8.)
  - **Floating static:** Primary via OSPF to an ISP, and `ip route 0.0.0.0 0.0.0.0 203.0.113.9 250` as backup. Show the table before and after the primary fails.
- **Figures:**
  - F4.4a: Annotated `show ip route` screenshot, with every token (code, prefix, [AD/metric], next hop, age, interface) called out by leader lines.
  - F4.4b: Decision flowchart: packet arrives → LPM → if multiple sources for the same prefix, AD (at install time) → metric → ECMP.
  - F4.4c: Floating static before/after diagram.
- **Lab:** Packet Tracer: 4 routers in a square, static routes only. Add a floating static, test failover with `shutdown`, and use `traceroute` to prove the path change. Then do an IPv6 version.

### 4.5 OSPF (single- and multi-area, OSPFv2 and v3)  `[MUST]`
- **Core idea:** OSPF is a link-state IGP. Routers form adjacencies, flood LSAs to build an identical LSDB per area, and each runs Dijkstra to compute the shortest paths by cost.
- **Analogy:**
  - Each router posts a "postcard about my links" (LSA) to every router in the area, and everyone pins the postcards to the same notice-board (LSDB) and computes their own map.
  - The DR is a class monitor who collects and redistributes notes so 30 students don't pass notes to each other.
- **Content:**
  - Packet types (Hello, DBD, LSR, LSU, LSAck); IP protocol 89; 224.0.0.5/6.
  - Hello/dead timers (10/40 broadcast; 30/120 NBMA).
  - Router-ID selection (manual → highest loopback → highest active interface IP).
  - **Neighbour states** (Down → Attempt (NBMA) → Init → 2-Way → ExStart → Exchange → Loading → Full); adjacency requirements (area, subnet/mask, hello/dead, auth, stub flags, MTU for DBD, unique RID, network type compatibility).
  - Network types (broadcast, point-to-point, NBMA, P2MP); DR/BDR election (priority → RID; non-preemptive; priority 0) and DROTHER 2-Way.
  - Cost = reference BW / interface BW (default 100 Mb/s, so 1G and 10G both = 1, hence `auto-cost reference-bandwidth`).
  - **LSA types 1, 2, 3, 4, 5, 7**; areas and backbone rule; ABR/ASBR.
  - Stub / totally stubby / NSSA / totally NSSA; virtual links; summarisation (`area range` on ABR, `summary-address` on ASBR).
  - Route types O, O IA, O E1/E2, N1/N2; E1 vs E2 metric behaviour.
  - Authentication (MD5/SHA); OSPFv3 differences (per-link, link-local next hops, LSA types 8 and 9); BFD for fast failure detection.
  - Minimising flaps: summarisation, stub areas, LSA throttling. This addresses the reported Cisco question about minimising routing updates when a set of routes flaps.
- **Worked examples:**
  1. **SPF cost:** R1-R2 10, R1-R3 5, R3-R2 3, R2-R4 1, R3-R4 10. R1→R4 = R1-R3-R2-R4 = 9, not R1-R2-R4 = 11. Show the R1 SPF tree and `show ip route ospf` output.
  2. **DR election:** Four routers on one LAN segment.
     - R1 (prio 1, RID 1.1.1.1), R2 (prio 1, RID 2.2.2.2), R3 (prio 0), R4 (prio 1, RID 4.4.4.4).
     - DR = R4, BDR = R2, and R3 can never be DR.
     - Then R5 joins with prio 255. Nothing changes (non-preemptive) until DR R4 fails, at which point BDR R2 becomes DR and R5 becomes BDR.
  3. **Adjacency fault-finding:** Two neighbours are stuck in EXSTART/EXCHANGE, caused by an MTU mismatch of 1500 vs 1400. Fix with matching MTU (or `ip ospf mtu-ignore`, plus a note on why that is a smell).
  4. **Multi-area LSA trace:** Area 1 (R1) – ABR R2 – Area 0 – ABR R3 – Area 2 (R4 ASBR redistributing static 172.16.0.0/16).
     - In area 1, R1 sees Type 3 for the area-2 prefixes, Type 4 for R4, and Type 5 for 172.16/16.
     - Convert area 1 to totally stubby. R1 then sees only Type 1/2 plus a Type 3 default.
- **Figures:**
  - F4.5a: **OSPF neighbour state machine.** States as rounded boxes left-to-right (Down, Init, 2-Way, ExStart, Exchange, Loading, Full); arrow labels show the triggering packets (Hello received, Hello seen with own RID, DBD master/slave negotiation, DBD exchange, LSR/LSU, LSAck). A side branch shows "2-Way is final between DROTHERs", and a red "stuck here" annotation shows common causes (Init: one-way hello/ACL; ExStart/Exchange: MTU; 2-Way: normal for DROTHERs).
  - F4.5b: **Adjacency ladder diagram** R1↔R2: Hello → Hello (2-Way) → DBD (I/M/MS bits) negotiation → DBD summaries → LSR → LSU → LSAck, with states in the margins.
  - F4.5c: **LSA flooding scope map.** A multi-area topology (area 1 – area 0 – area 2 + external cloud) with coloured arrows per LSA type showing how far each floods; Type 1/2 confined to the area, Type 3 crossing ABRs, Type 5 domain-wide except stubs, Type 7 converted to 5 at the NSSA ABR.
  - F4.5d: **Area-type matrix** (rows: normal, stub, totally stubby, NSSA, totally NSSA; columns: LSA 1/2, 3, 4, 5, 7, default route) with ✓/✕.
  - F4.5e: DR/BDR multicast flow: DROTHERs send to 224.0.0.6, and the DR re-floods to 224.0.0.5.
  - F4.5f: SPF tree drawn over worked example 1.
- **Labs:**
  - Packet Tracer: single-area OSPF on 4 routers; DR/BDR manipulation with `ip ospf priority`; reference bandwidth.
  - Containerlab with FRR (or SR Linux): multi-area plus stub/NSSA conversions; `show ip ospf database` before/after.
  - Fault injection script: a pre-built broken lab with 6 faults (hello mismatch, area mismatch, MTU, passive interface, duplicate RID, auth key), which students fix in 30 minutes.
  - Wireshark: capture `ospf` on a link while bringing up an adjacency and match packets to F4.5b.

### 4.6 EIGRP  `[OPTIONAL, SHOULD for CSC]`
- **Core idea:** EIGRP is Cisco's advanced distance-vector protocol. It uses DUAL to keep a loop-free backup path (the feasible successor) ready, so failover is near-instant.
- **Analogy:**
  - The feasibility condition is accepting a backup route from a friend only if the friend is *closer to the destination than you currently are*. That guarantees the friend isn't routing through you.
- **Content:**
  - Packets (Hello, Update, Query, Reply, ACK); RTP; protocol 88; 224.0.0.10; neighbour requirements (AS, K values, subnet, auth).
  - Topology table, successor, feasible distance (FD), reported/advertised distance (RD/AD), feasible successor; feasibility condition RD < FD.
  - Metric with default K values (K1 = K3 = 1): 256 × (10⁷ / min BW kb/s + Σ delay µs / 10); wide metrics (64-bit) overview.
  - Unequal-cost load balancing (`variance`); stub routers; query scoping and stuck-in-active (SIA); auto-summary history; named mode.
- **Worked examples:**
  1. **Metric:** A path over a T1 (1,544 kb/s, delay 20,000 µs) and a GigE (delay 10 µs).
     - 10⁷ / 1544 = 6476 (integer).
     - Delay = 20,010 / 10 = 2001.
     - Metric = 256 × (6476 + 2001) = 2,170,112.
  2. **Feasibility:** Paths to 10.9.9.0/24:
     - via R2: FD 3000 (RD 1000), which is the successor.
     - via R3: RD 2500 < 3000, so it is a feasible successor.
     - via R4: RD 3500, which is not feasible (possible loop).
     - With `variance 2`, which paths are used? R3 is used if its FD < 6000. R4 is never used, because unequal-cost load balancing requires feasibility.
- **Figures:**
  - F4.6a: **DUAL diagram.** The destination on the right, with three candidate neighbours and their RD/FD values on links; the successor in green, the FS in amber, the non-feasible path in grey with a ✕; FD drawn as a dashed threshold.
  - F4.6b: Query/reply propagation with and without stub routers (shows SIA risk).
  - F4.6c: OSPF vs EIGRP comparison table graphic.
- **Lab:** Packet Tracer: 5-router EIGRP with a deliberate FS; `show ip eigrp topology`. Shut the successor and observe zero queries (FS promoted). Repeat with no FS and observe queries (`debug eigrp packets query`).

### 4.7 BGP: the Internet's routing protocol (flagship section, ~30 pp)  `[MUST]`
- **Core idea:** BGP is a path-vector protocol between autonomous systems. It runs over TCP 179, carries policy-rich attributes, and picks one best path per prefix through a strict, ordered list of tie-breakers.
- **Analogy:**
  - BGP is diplomatic relations between countries (ASes). Each embassy tells its neighbours "you can reach these cities through me, via these countries" (AS_PATH).
  - Countries choose routes by policy (alliances = local preference) before distance.
  - Route reflectors are a regional embassy that relays news so every consulate doesn't need a direct line to every other.
- **Content:**
  1. AS numbers (2-byte/4-byte, private 64512–65534 and 4200000000+); eBGP vs iBGP; AD 20/200.
  2. **FSM:** Idle → Connect → Active → OpenSent → OpenConfirm → Established. Stuck-in-Active and Idle causes.
  3. Messages: OPEN (version, AS, hold time, BGP ID, capabilities), UPDATE (withdrawn routes, path attributes, NLRI), KEEPALIVE, NOTIFICATION, ROUTE-REFRESH. Timers 60/180 (Cisco).
  4. Neighbour configuration; `update-source loopback`; `ebgp-multihop`; `network` vs redistribution; the exact-match requirement for `network`.
  5. iBGP rules: no re-advertising of iBGP-learned routes to iBGP peers (full mesh n(n−1)/2); next hop unchanged into iBGP (`next-hop-self`); synchronisation history.
  6. Route reflectors (client/non-client rules, ORIGINATOR_ID, CLUSTER_LIST loop prevention, RR clusters); confederations.
  7. Attributes: well-known mandatory (ORIGIN, AS_PATH, NEXT_HOP), well-known discretionary (LOCAL_PREF, ATOMIC_AGGREGATE), optional transitive (COMMUNITY, AGGREGATOR), optional non-transitive (MED, ORIGINATOR_ID, CLUSTER_LIST); Cisco WEIGHT (local, not an attribute on the wire).
  8. **Path selection (Cisco order):**
     - 0. Next hop reachable (and synchronised if enabled).
     - 1. Highest Weight.
     - 2. Highest Local Pref (default 100).
     - 3. Locally originated (network/aggregate/redistribute).
     - 4. Shortest AS_PATH.
     - 5. Lowest Origin (IGP < EGP < incomplete).
     - 6. Lowest MED (same neighbour AS by default).
     - 7. eBGP over iBGP.
     - 8. Lowest IGP metric to the next hop.
     - 9. Multipath check.
     - 10. Oldest eBGP path.
     - 11. Lowest router ID.
     - 12. Shortest cluster-list.
     - 13. Lowest neighbour address.
     - **Mnemonic: "N WLLA OMNI"** (Next-hop, Weight, Local pref, Locally originated, AS path, Origin, MED, Neighbour type, IGP metric), then "Old Routers Clear Neighbours" (Oldest, RID, Cluster list, Neighbour IP).
  9. Traffic engineering:
     - **Outbound:** Weight, Local Pref.
     - **Inbound:** AS-path prepending, MED, more-specific prefixes, communities (no-export, no-advertise, provider TE communities).
  10. Filtering: prefix lists, AS-path access lists (regex `^$`, `_65001_`), route maps; soft reconfiguration / route refresh; maximum-prefix.
  11. BGP multipath / ECMP (`maximum-paths`, same-AS requirement, `bgp bestpath as-path multipath-relax`); BGP in the data centre (RFC 7938 eBGP spine-leaf, per-rack ASNs, allowas-in) as a pointer to P5; BFD.
  12. Security and operations: route leaks, hijacks (Pakistan/YouTube 2008, Facebook 2021 outage), RPKI/ROV overview, MD5/TCP-AO, GTSM.
- **Worked examples:**
  1. **Path selection race:** R1 in AS 65000 receives 203.0.113.0/24 three ways:
     - (a) from ISP-A, eBGP, AS_PATH 100 300, LP 100, MED 50
     - (b) from ISP-B, eBGP, AS_PATH 200 300, LP 100, MED 10
     - (c) via iBGP from R2, AS_PATH 100 300, LP 150
     - Step through the list: (c) wins on LP 150 at step 2.
     - Remove the LP setting: (a) and (b) tie on AS_PATH length and origin; MED is compared only for the same neighbour AS (100 ≠ 200), so it is not compared by default; both are eBGP; the IGP cost tie-breaks, then the oldest path.
     - Discuss `bgp always-compare-med`.
  2. **Dual-homed enterprise:**
     - **Primary/backup outbound:** Set LP 200 on routes from ISP-A via a route map.
     - **Inbound:** Prepend AS 65000 twice towards ISP-B.
     - Show `show ip bgp` output before and after, with the `>` best-path marker.
  3. **iBGP next-hop problem:** R3 (iBGP) installs no route because the next hop is the eBGP peer's address, which is unknown in the IGP. Fix with `next-hop-self` on the border router or by advertising the link in the IGP.
  4. **Full-mesh arithmetic:** 10 routers need 45 sessions. With 2 RRs and 8 clients, it is 2 × 8 + 1 = 17 sessions.
- **Figures:**
  - F4.7a: **BGP FSM diagram.** Six states in a ring/flow with transition labels (Start event, TCP connect success/fail, ConnectRetry timer expiry, OPEN sent/received, KEEPALIVE received, NOTIFICATION / hold-timer expiry back to Idle). Red notes mark "Active = trying to connect, NOT good".
  - F4.7b: BGP session ladder: TCP 3-way handshake on 179 → OPEN ↔ OPEN → KEEPALIVE ↔ KEEPALIVE → UPDATEs, with states in the margins.
  - F4.7c: **Path-selection staircase infographic.** 13 numbered steps descending, each with an icon and a "higher/lower wins" arrow; the N WLLA OMNI mnemonic letters set large on the left in brand colour.
  - F4.7d: Dual-homed enterprise topology, with arrows showing the inbound (prepend) vs outbound (LP) traffic-influence direction, colour-coded.
  - F4.7e: Route-reflector topology: RR in the centre, clients around it, a non-client peer; arrows show which advertisements are reflected (client → all; non-client → clients only), with ORIGINATOR_ID/CLUSTER_LIST tags on one route.
  - F4.7f: Attribute taxonomy tree (well-known mandatory/discretionary; optional transitive/non-transitive).
  - F4.7g: Annotated `show ip bgp` output with the status codes (`*`, `>`, `i`, `r`), Next Hop, Metric, LocPrf, Weight, Path and Origin code.
- **Labs:**
  - Containerlab with FRR (free, scriptable), 6 nodes across 2 ISPs, an enterprise AS (2 border routers + 1 internal) and a "content" AS.
    - Tasks: eBGP/iBGP; next-hop-self; LP outbound; prepend inbound; communities; prefix-list filtering; max-prefix.
    - Validate with `vtysh -c "show bgp ipv4 unicast"`.
  - A variant on Arista cEOS or Nokia SR Linux, for ARI/NOK candidates.
  - Wireshark: capture BGP OPEN/UPDATE and decode the attributes.
  - Stretch: a route-reflector lab with 1 RR and 4 clients; prove loop prevention via CLUSTER_LIST.

### 4.8 First-hop redundancy: HSRP, VRRP, GLBP  `[SHOULD]`
- **Core idea:** Hosts have one default gateway. FHRPs let two or more routers share a virtual IP/MAC so the gateway survives a router failure.
- **Analogy:** A shop with one public phone number answered by whichever staff member is on duty. If they go on break, a colleague picks up the same number.
- **Content:**
  - **HSRP:** v1/v2, states (Initial, Learn, Listen, Speak, Standby, Active), priority 100, preempt off by default, hello 3 s / hold 10 s, UDP 1985, multicast 224.0.0.2 (v1) / 224.0.0.102 (v2), virtual MAC 0000.0c07.acXX (v1) / 0000.0c9f.fXXX (v2).
  - **VRRP:** v2/v3, IP protocol 112, 224.0.0.18, MAC 0000.5e00.01XX, preempt on by default, can use the interface's real IP (owner = priority 255).
  - **GLBP:** AVG/AVF, load-balancing, MAC 0007.b400.XXYY.
  - Interface/object tracking with decrement; gratuitous ARP on failover; aligning the STP root with the HSRP active router.
- **Worked example:**
  - R1 priority 110 + preempt + track G0/1 decrement 20; R2 priority 100; VIP 192.168.1.254.
  - R1's uplink fails, so 110 − 20 = 90 < 100 and R2 becomes active.
  - The uplink returns, and R1 preempts back.
  - Show the `show standby brief` output at each stage.
- **Figures:**
  - F4.8a: FHRP topology: two routers, VIP/VMAC box floating between them, hosts pointing at the VIP; a failover arrow sequence (1 → 2 → 3) with gratuitous ARP.
  - F4.8b: HSRP vs VRRP vs GLBP comparison table graphic (standard, multicast, port/protocol, VMAC, preempt default, load-balancing).
  - F4.8c: Tracking timeline chart: priority vs time for R1 and R2 crossing at the failure.
- **Lab:** Packet Tracer: HSRPv2 with tracking. Continuous ping from a host while shutting the R1 uplink; count lost pings. Then convert to VRRP (IOS-XE in GNS3 or FRR `vrrpd`).

### 4.9 Route control: prefix lists, route maps, redistribution, PBR, VRF-lite  `[SHOULD]`
- **Core idea:** Policy tools let you select, filter and modify routes and packets. Redistribution connects routing domains but needs loop protection.
- **Analogy:**
  - A route map is an airport security queue with numbered lanes. Each lane has a match rule and an action, and anything not matched at the end is turned away (implicit deny).
  - A VRF is separate flats in one building with separate letterboxes.
- **Content:**
  - Prefix-list syntax (`ge`/`le`) and worked matches.
  - Route-map sequence, match/set, permit/deny semantics, implicit deny, the "continue" statement.
  - Redistribution between OSPF↔EIGRP↔BGP (seed metrics, `subnets` keyword in older IOS); two-way redistribution loops and tag-based prevention; AD manipulation.
  - PBR (`ip policy route-map`); VRF-lite (`vrf definition`, interface assignment, per-VRF routing tables, `ping vrf`).
- **Worked examples:**
  1. Which prefixes match `ip prefix-list X permit 10.0.0.0/8 ge 16 le 24`? Test 10.0.0.0/8 (no), 10.1.0.0/16 (yes), 10.1.1.0/24 (yes) and 10.1.1.0/25 (no).
  2. Two-way redistribution between OSPF and EIGRP at two points. Show the loop, then fix it by tagging (set tag 110 / deny tag 110).
- **Figures:**
  - F4.9a: Route-map flowchart: sequence 10 → 20 → implicit deny, with match/set boxes.
  - F4.9b: Two-way redistribution loop diagram with red loop arrows, then the tagged fix.
  - F4.9c: VRF "split router" illustration: one router box divided into coloured VRF slices, each with its own routing table.
- **Lab:** GNS3 (IOSv) or FRR: mutual redistribution loop creation and fix; PBR sending HTTP via ISP-B; VRF-lite with overlapping 10.0.0.0/24 in two VRFs.

### 4.10 MPLS and L3VPN  `[SHOULD, MUST for JNP/NOK/SP roles]`
- **Core idea:** MPLS forwards on short labels instead of IP lookups, which enables L3VPNs where a provider carries many customers' overlapping routes privately across one core.
- **Analogy:**
  - A courier's barcode sticker. Hubs scan the sticker (label) and never open the parcel (IP header).
  - The VPN label is a second sticker saying which customer's mailbox at the destination depot.
- **Content:**
  - Label shim (Label 20 | TC 3 | S 1 | TTL 8 = 32 bits); EtherType 0x8847.
  - Reserved labels (0 IPv4 explicit-null, 1 router alert, 2 IPv6 explicit-null, 3 implicit-null); LSR roles (CE/PE/P); push/swap/pop; PHP.
  - LDP (UDP 646 discovery / TCP 646 sessions); LIB vs LFIB.
  - L3VPN: VRF, RD (makes VPNv4 prefixes unique, 64-bit RD + 32-bit IPv4 = 96 bits), RT (import/export controls membership), MP-BGP VPNv4 between PEs, the two-label stack.
  - MPLS TE and Segment Routing (SR-MPLS/SRv6) as a short preview (relevant to JNP/NOK/CSC SP roles).
- **Worked example: the L3VPN packet walk.**
  - Customer A at site 1 (CE1, 10.1.1.0/24) to site 2 (CE2, 10.2.2.0/24) via PE1 – P1 – P2 – PE2.
  - **CE1→PE1:** plain IP.
  - **PE1:** VRF lookup, then push [VPN label 300 (inner), transport label 24 (outer)].
  - **P1:** swaps 24→35.
  - **P2** (penultimate): pops the transport label (PHP, implicit-null 3 advertised by PE2), so the packet now carries VPN label 300 only.
  - **PE2:** looks up label 300, maps it to VRF A, does an IP lookup and forwards to CE2.
  - Customer B, also using 10.1.1.0/24, stays separate via RD 65000:2 and RT 65000:2.
- **Figures:**
  - F4.10a: MPLS shim bit-layout and its position between the L2 and IP headers.
  - F4.10b: **L3VPN packet-walk strip:** 6 nodes in a row, with a "packet card" under each link showing the label stack (coloured blocks: transport label orange, VPN label purple) and the IP header.
  - F4.10c: RD vs RT explainer: two customers with identical prefixes become unique VPNv4 routes; RT import/export arrows into VRF tables.
  - F4.10d: Control-plane overlay: LDP sessions (hop-by-hop, dotted) vs MP-BGP VPNv4 session (PE-to-PE, solid arc).
- **Lab:** Containerlab with FRR (MPLS LDP + BGP VPNv4 supported on Linux kernel MPLS) or GNS3 with IOSv/CSR1000v.
  - Build a 4-node core with two customers using overlapping prefixes.
  - Verify with `show mpls forwarding-table` / `ip -f mpls route`, `show bgp vpnv4 unicast all`, and `traceroute` showing labels.

### 4.11 Quality of Service  `[SHOULD]`
- **Core idea:** When links congest, QoS decides who waits and who is dropped. Classify and mark at the edge, then queue, shape or police at congestion points.
- **Analogy:**
  - Airport check-in: business class (EF voice) has its own short queue with a hard cap.
  - Families get guaranteed counters (CBWFQ), and standby passengers are bumped first when it is full (WRED).
  - A policer is a toll gate that turns away excess cars. A shaper is a traffic light that holds them.
- **Content:**
  - QoS needs: voice one-way delay ≤ 150 ms, jitter ≤ 30 ms, loss ≤ 1%.
  - Models: best-effort, IntServ (RSVP), DiffServ.
  - Classification (ACL, NBAR); marking: CoS (802.1p 3 bits), IP Precedence, **DSCP** (6 bits: EF 46, AFxy = 8x + 2y, CS0–CS7), ECN bits; trust boundaries.
  - Queuing: FIFO, PQ, WFQ, CBWFQ, LLQ (priority with an implicit policer); congestion avoidance (tail drop, global synchronisation, RED/WRED).
  - Policing vs shaping (token bucket, CIR/Bc/Be, Tc = Bc/CIR); MQC (class-map, policy-map, service-policy).
  - The QoS angle on wireless/cellular (5QI pointer to P6).
- **Worked examples:**
  1. **DSCP decode:** ToS byte 0xB8 = 1011 1000, so DSCP 101110 = 46 = EF. AF31 = 8·3 + 2·1 = 26 (binary 011010).
  2. **Shaper:** CIR 10 Mb/s, Bc 100,000 bits, so Tc = 10 ms. Each 10 ms interval allows 100 kb.
  3. **Policy design:** A 10 Mb/s WAN with voice LLQ 10% priority, video 30%, business-critical 25%, scavenger 1%, default rest. Write the MQC config.
- **Figures:**
  - F4.11a: **DSCP/ToS byte bit-layout** (DSCP 6 | ECN 2) with the precedence overlay, plus a full DSCP table graphic (PHB, decimal, binary, typical traffic).
  - F4.11b: QoS toolkit pipeline: ingress classify/mark → trust boundary → egress queues (LLQ, CBWFQ classes, default) → scheduler → wire.
  - F4.11c: **Policing vs shaping graph:** two rate-vs-time charts of the same bursty input, with the policer chopping the peaks (dropped/re-marked) and the shaper smoothing them (delayed).
  - F4.11d: Token-bucket illustration (bucket of Bc tokens refilling at CIR).
  - F4.11e: WRED drop-probability curve (min threshold, max threshold, mark probability denominator) for AF11/12/13.
- **Labs:**
  - GNS3 (IOSv): MQC LLQ policy on a constrained link; generate traffic with iperf3 from Linux hosts with DSCP set (`iperf3 -S 0xB8`); `show policy-map interface`.
  - Linux `tc`: an HTB shaper plus a policer comparison and graphs.

### 4.12 IP Multicast  `[OPTIONAL, SHOULD for JNP/NOK/BRC]`
- **Core idea:** Multicast sends one stream to many receivers by replicating only where paths split. Receivers join via IGMP, and routers build distribution trees with PIM, guarded by RPF checks.
- **Analogy:**
  - A radio station: you tune in (IGMP join), and towers relay only to regions with listeners (PIM).
  - The RPF check is "only accept the broadcast from the tower that is on your shortest road back to the station".
- **Content:**
  - Addressing (224.0.0.0/4; 224.0.0.0/24 link-local; 232/8 SSM; 239/8 admin-scoped); MAC mapping 01:00:5E + low 23 bits (32:1 overlap).
  - IGMPv1/v2/v3 (joins, leaves, querier); IGMP snooping on switches.
  - PIM-DM (flood and prune) vs PIM-SM (RP, shared tree (*,G), SPT switchover (S,G), register/register-stop); RP discovery (static, Auto-RP, BSR); PIM-SSM with IGMPv3; Bidir-PIM; MSDP (inter-domain, overview).
  - The RPF check; ENCOR coverage (PIM-SM, IGMPv2/v3, SSM, Bidir, MSDP).
- **Worked example:**
  - **MAC mapping:** 239.1.1.1 → 01:00:5E:01:01:01. 224.129.1.1 maps to the *same* MAC, because the top bit of the 2nd octet (129 = 1000 0001) is dropped. So 32 IP groups share one MAC.
  - **PIM-SM join walk:** A receiver sends an IGMP join for 239.1.1.1 → the last-hop router sends a (*,G) join toward the RP → the source's first-hop router registers with the RP → traffic flows down the shared tree → the LHR switches to the SPT (S,G) → the RP prunes.
- **Figures:**
  - F4.12a: **IP-to-MAC mapping bit diagram:** 32-bit group address, top 4 bits (1110) fixed, next 5 bits dropped (shaded grey "lost"), low 23 bits copied into the MAC after 01:00:5E plus a 0 bit.
  - F4.12b: Unicast vs broadcast vs multicast replication comparison (three small network panels showing link usage counts).
  - F4.12c: **PIM-SM shared tree → SPT switchover** in two panels: panel 1 shows the RP-rooted (*,G) tree in blue; panel 2 shows the source-rooted (S,G) tree in green, with the prune toward the RP in red dashed.
  - F4.12d: RPF-check flowchart (packet arrives on interface X → unicast route back to the source via X? → accept/drop).
- **Lab:** GNS3 (IOSv): PIM-SM with a static RP, VLC/`iperf -u -B 239.1.1.1` as source and receivers; `show ip mroute`, `show ip igmp groups`; break RPF with a static route and watch drops.

### 4.13 IP services and access control on IOS (CCNA domain 4 and part of 5)  `[MUST]`
- **Core idea:** Routers also provide the everyday services a network depends on (NAT, DHCP, NTP, SNMP, syslog), and ACLs decide which packets are allowed.
- **Analogy:** An ACL is a guest list checked top-down. The first matching line decides, and anyone not on the list is refused (implicit deny).
- **Content:**
  - IOS NAT/PAT configuration (`ip nat inside source list 1 interface g0/1 overload`).
  - DHCP server/relay configuration; NTP (stratum, client/server, authentication); SNMPv2c vs v3; syslog severity levels 0–7 ("Every Awesome Cisco Engineer Will Need Ice cream Daily"); TFTP/FTP for images.
  - Standard (1–99, source only, place near the destination) vs extended (100–199, place near the source) ACLs; named ACLs; wildcard masks; sequence numbers; `established`; IPv6 ACLs (implicit permit for NDP before the deny).
  - L2 security hand-off to P9.
- **Worked examples:**
  - Write an extended ACL allowing only 192.168.10.0/24 to reach the web server 10.0.0.80 on TCP 443 and permit return traffic. Decide where to apply it and in which direction.
  - Convert "hosts 192.168.1.16–31" into wildcard 0.0.0.15.
- **Figures:**
  - F4.13a: ACL processing flowchart (top-down, first match, implicit deny).
  - F4.13b: ACL placement diagram (standard near the destination, extended near the source) with in/out direction arrows on interfaces.
  - F4.13c: Syslog severity ladder 0–7 with the mnemonic.
- **Lab:** Packet Tracer: CCNA-style integrated lab with PAT, a DHCP pool + relay, an NTP server, syslog to a server, SSH-only vty with an ACL, and an extended ACL on the web server.

### 4.14 Tunnels and enterprise architecture (bridge to Pillars 5, 9 and 10)  `[OPTIONAL]`
- **Core idea:** Tunnels (GRE, IPsec, VXLAN) wrap packets to cross networks that do not natively carry them. Modern enterprise design layers SD-WAN and SD-Access controllers over this.
- **Analogy:** Putting a sealed parcel inside another courier's bag. The outer courier knows only the bag's address.
- **Content:**
  - GRE (protocol 47, 24 B overhead, recursive-routing trap); GRE over IPsec (pointer to P9); DMVPN (concept).
  - Campus 2-tier/3-tier vs spine-leaf (pointer to P5); SD-WAN (vManage/vSmart/vBond/vEdge roles) and SD-Access (fabric, LISP control plane, VXLAN data plane) per ENCOR 1.0/2.0.
  - BFD; IP SLA tracking.
- **Worked example:** GRE tunnel between R1 (203.0.113.1) and R2 (198.51.100.1) with tunnel subnet 172.31.0.0/30 and OSPF over the tunnel. Show the outer/inner headers and the MTU reduction (1500 − 24 = 1476), then the recursive-routing failure when the tunnel destination is learnt via the tunnel itself.
- **Figures:**
  - F4.14a: GRE encapsulation header stack (outer IP | GRE | inner IP | payload) with byte counts.
  - F4.14b: Three-tier campus vs spine-leaf comparison diagram.
  - F4.14c: SD-WAN component diagram (orchestrator, controller, manager, edges; control vs data plane arrows).
- **Lab:** Packet Tracer / GNS3: GRE + OSPF over the tunnel; trigger recursive routing and observe the "line protocol down" flaps.

## Pillar 4 labs summary table

| Section | Primary tool | Lab | Free alternative |
|---|---|---|---|
| 4.1 | Packet Tracer / Containerlab | Base config + SSH; multi-vendor CLI | SR Linux, cEOS |
| 4.2 | Packet Tracer | VLANs, trunks, ROAS, SVIs; native mismatch | cEOS |
| 4.3 | Packet Tracer | STP election, Rapid-PVST timing, EtherChannel | — |
| 4.4 | Packet Tracer | Static, floating static, IPv6 static | FRR |
| 4.5 | PT → Containerlab FRR | OSPF multi-area, stub/NSSA, 6-fault challenge | SR Linux |
| 4.6 | Packet Tracer | EIGRP FS failover, queries | FRR `eigrpd` (limited) |
| 4.7 | Containerlab FRR | Dual-homed BGP, LP/prepend/communities, RR | cEOS, SR Linux |
| 4.8 | Packet Tracer | HSRP tracking, VRRP | FRR `vrrpd` |
| 4.9 | GNS3 IOSv / FRR | Redistribution loop and fix, PBR, VRF-lite | FRR |
| 4.10 | Containerlab FRR / GNS3 | MPLS LDP + L3VPN, overlapping customers | — |
| 4.11 | GNS3 IOSv + Linux tc | LLQ/CBWFQ, shaping vs policing | Linux tc |
| 4.12 | GNS3 IOSv | PIM-SM with RP, SPT switchover | FRR `pimd` |
| 4.13 | Packet Tracer | Integrated CCNA services + ACLs | — |
| 4.14 | PT / GNS3 | GRE + OSPF, recursive-routing fault | FRR |

Companion repo plan: a `labs/p4/<section>/topology.clab.yml` + `startup-configs/` + `verify.py` (pytest + Netmiko/`vtysh` checks) per lab, so P10 automation can reuse them.

## Pillar 4 company-tag matrix

| Topic | CSC | QCM | GOO | MSF | AMZ NDE | JNP | ARI | NOK | BRC |
|---|---|---|---|---|---|---|---|---|---|
| CLI / device architecture / CEF/TCAM | H | L | M | M | M | H | H | H | H |
| VLANs / trunking / inter-VLAN | H | L | L | M | M | H | H | H | M |
| STP / RSTP / MST scenarios | H | L | L | M | M | H | H | H | M |
| EtherChannel / LACP / MLAG | H | L | M | M | H | H | H | M | M |
| Static, routing table, AD, LPM | H | M | M | H | H | H | H | H | M |
| OSPF states / LSAs / areas | H | L | M | M | H | H | H | H | M |
| EIGRP / DUAL | H | L | L | L | M | L | L | L | L |
| BGP attributes / path selection / RR | H | L | H | H | H | H | H | H | M |
| HSRP / VRRP | H | L | L | M | M | M | M | M | L |
| Redistribution / route maps / VRF | H | L | M | M | H | H | H | H | L |
| MPLS / L3VPN / SR | M | L | M | M | M | H | M | H | M |
| QoS (DSCP, LLQ, policing/shaping) | H | M | M | M | M | H | M | H | H |
| Multicast (IGMP/PIM) | M | M | L | L | L | H | M | H | M |
| ACL / NAT / DHCP / NTP on IOS | H | L | L | M | M | M | M | M | L |

Notes:
- **Amazon NDE:** BGP path manipulation, MTU/MSS and "biggest outage" stories are consistently reported.
- **Meta-style / Arista / Juniper:** iBGP loop avoidance, RR clusters, BGP ECMP and spine-leaf are reported.
- **Cisco:** STP scenarios, OSPF LSA types and BGP attributes are reported.
- **Broadcom:** Data-plane depth (TCAM, LPM hardware, QoS queues) rather than protocol configuration.
- **Qualcomm:** L2/L3 mostly only for networking-software roles, so prioritise Pillars 3 and 6 for them.

## Pillar 4 interview question bank (55). Every question has a full solution in the P4 end-of-chapter pack (§4.E4); each entry is also tagged MUST/SHOULD/OPTIONAL by its section

**Switching and STP**
1. [E] Access vs trunk port. What is the native VLAN, and what happens on a native-VLAN mismatch? (CSC, JNP)
2. [E] How many VLANs does 802.1Q support, and why 4094? (CSC, ARI)
3. [M] Explain how inter-VLAN routing works with ROAS vs SVIs. Which scales better? (CSC)
4. [M] Why is DTP a security risk? How do you harden trunk ports? (CSC)
5. [M] Walk through the STP root election and port-role selection for this triangle (worked example). (CSC, JNP, ARI)
6. [M] Why must the STP priority be a multiple of 4096? (CSC)
7. [M] 802.1D vs RSTP: list the port states and roles. Why does RSTP converge in under a second? (CSC, NOK)
8. [M] PortFast + BPDU Guard vs Root Guard vs Loop Guard: where do you apply each? (CSC, ARI)
9. [H] *Scenario:* Users report the network "freezing" every few minutes, and switch CPU is at 100%. `show mac address-table` shows MACs flapping between ports. Diagnose it and fix it. (CSC, AMZ)
10. [M] LACP active/passive vs PAgP vs `on`: which combinations form a bundle? (CSC, ARI)
11. [H] An EtherChannel shows member ports in `(s)` suspended state. Give five causes. (CSC, JNP)
12. [H] How does MLAG/vPC avoid STP blocking? What is the peer-link for? (ARI, CSC, AMZ)

**Routing basics**
13. [E] What is administrative distance? Give the AD for connected, static, eBGP, EIGRP, OSPF, RIP and iBGP. (CSC, AMZ)
14. [M] Order the routing decision: longest prefix, AD, metric. Solve the routing-table puzzle from 4.4. (CSC, AMZ, JNP)
15. [M] What is a floating static route? Configure a backup default route. (CSC)
16. [H] Explain RIB vs FIB vs TCAM. How does a hardware switch perform LPM at line rate? (BRC, ARI, JNP)

**OSPF**
17. [E] List the OSPF neighbour states in order. (CSC, JNP, NOK)
18. [M] Two routers are stuck in EXSTART. Why? What about stuck in INIT, or 2-WAY? (CSC, AMZ, JNP)
19. [M] List all the parameters that must match for OSPF adjacency. (CSC, NOK)
20. [M] How is the DR elected? Is it pre-emptive? Why do we need a DR at all? (CSC, JNP)
21. [M] Explain LSA types 1, 2, 3, 4, 5 and 7, who generates each, and their flooding scope. (CSC, JNP, NOK, AMZ)
22. [M] Stub vs totally stubby vs NSSA: which LSAs are blocked in each? (CSC, JNP)
23. [M] Why must all areas connect to area 0? What is a virtual link? (CSC)
24. [M] Why do 1 Gb/s and 10 Gb/s links have the same OSPF cost by default? How do you fix it? (CSC, AMZ)
25. [H] E1 vs E2 external routes: which is preferred, and when does it matter? (CSC, JNP)
26. [H] *Scenario:* A set of 200 customer routes in area 3 flaps every few minutes, causing SPF runs network-wide. How do you contain it? (summarisation at the ABR, stub area, LSA throttling) (CSC — reported)
27. [H] OSPF vs IS-IS: why do many service providers and data centres prefer IS-IS? (JNP, NOK, GOO)

**EIGRP**
28. [M] Define successor, feasible successor, FD and RD. State the feasibility condition. (CSC)
29. [M] Compute the EIGRP metric for a T1 + GigE path. (CSC)
30. [H] What is stuck-in-active, and how do stub routers and summarisation prevent it? (CSC)
31. [M] OSPF vs EIGRP: give five differences. (CSC, MSF)

**BGP**
32. [E] Why does BGP use TCP? Which port? (all)
33. [E] List the BGP neighbour states. What does "Active" mean? (CSC, AMZ, JNP)
34. [M] eBGP vs iBGP: differences in AD, TTL, next-hop behaviour, AS_PATH. (AMZ, JNP, ARI)
35. [M] Recite the BGP best-path selection order. (CSC, AMZ, JNP, ARI, NOK — very frequently reported)
36. [M] Weight vs Local Preference vs MED: scope, direction influenced, and which is higher-better. (AMZ, CSC)
37. [M] Why does iBGP need a full mesh? How do route reflectors and confederations solve it? (GOO, ARI, JNP — reported in a Meta loop)
38. [H] How does a route reflector prevent loops? (ORIGINATOR_ID, CLUSTER_LIST) What is an RR cluster? (ARI, JNP)
39. [M] An iBGP router has the route in its BGP table but not in its RIB. Why? (next hop unreachable; RIB failure) (AMZ, CSC)
40. [H] *Scenario:* You are dual-homed to ISP-A and ISP-B. Make ISP-A primary for both inbound and outbound traffic. Write the policy. (AMZ — reported, CSC, MSF)
41. [H] How does BGP multipath/ECMP work? What conditions must match? What does `as-path multipath-relax` do? (ARI, GOO, AMZ)
42. [H] Why is eBGP used inside large data-centre fabrics instead of OSPF (RFC 7938)? (GOO, MSF, ARI, AMZ)
43. [M] What are BGP communities? Explain no-export vs no-advertise. (JNP, NOK)
44. [H] *Scenario:* A customer accidentally announces a more-specific prefix of a major content provider. What happens globally, and how do RPKI/ROV and max-prefix help? (AMZ, GOO, MSF)
45. [H] *Coding:* Given a list of BGP paths with attributes, implement best-path selection (steps 1–8) in Python. (GOO, ARI, AMZ)

**FHRP, policy, MPLS, QoS, multicast**
46. [E] HSRP vs VRRP: which is open-standard? What are the default preempt behaviours? (CSC)
47. [M] With HSRP tracking, R1's uplink fails but R1 stays active. Why? (preempt missing on R2? decrement too small?) (CSC)
48. [M] Prefix-list `10.0.0.0/8 ge 16 le 24`: which of four given prefixes match? (CSC, JNP)
49. [H] Explain the routing loop caused by two-way redistribution at two points, and how tags fix it. (CSC, JNP)
50. [M] What is an MPLS label stack? Explain PHP and why implicit-null exists. (JNP, NOK, CSC)
51. [H] Walk a packet through an MPLS L3VPN. What do RD and RT each do? (JNP, NOK, CSC)
52. [M] Policing vs shaping: give the effect on TCP flows of each. (CSC, NOK, BRC)
53. [M] Decode DSCP 46 and AF31. Why does voice use LLQ? (CSC, QCM, NOK)
54. [M] How does an IPv4 multicast address map to a MAC? Why is there 32:1 ambiguity? (CSC, JNP, BRC)
55. [H] Explain the PIM-SM shared tree vs the shortest-path tree and the RPF check. What happens if unicast routing is asymmetric? (JNP, NOK)

## Pillar 4 trap boxes
- An STP **root port** is on the non-root switch facing the root, and the root has none. **Designated ports** are per segment. Every port on the root is designated.
- Bridge priority is set in multiples of 4096. The displayed priority 32769 = 32768 + VLAN 1 (extended system ID).
- AD is compared only between **different sources for the same prefix length**. A /24 static always beats a /16 connected for matching traffic, because of LPM.
- An OSPF DR is not pre-emptive. Raising priority later does nothing until the DR fails.
- OSPF "2-Way" between DROTHERs is normal, not a fault.
- OSPF cost with the default reference bandwidth makes 1G = 10G = 1. Set the reference bandwidth consistently on *all* routers.
- "BGP neighbour Active" means it is *not* established, but trying.
- MED is compared only between paths from the **same neighbouring AS** by default. A lower MED wins, whereas a higher Weight/LP wins.
- iBGP does not change the next hop. Missing `next-hop-self` is the number-one lab failure.
- The `network` statement in BGP needs an **exact** prefix match in the RIB, unlike OSPF/EIGRP `network`.
- HSRP preempt is **off** by default, while VRRP preempt is **on**.
- EIGRP unequal-cost load balancing (`variance`) still only uses **feasible successors**.
- PortFast on a trunk/switch-facing port invites loops. Pair it with BPDU Guard on access ports.
- A standard ACL goes near the destination and an extended ACL near the source. Every ACL ends in an implicit `deny any`. IPv6 ACLs implicitly permit NDP before that.
- In multicast, 224.0.0.0/24 is link-local, and PIM never routes it.
- Policing re-marks or drops instantly (TCP sees loss and saw-tooths), while shaping buffers (adds delay). Do not police voice on ingress without understanding the consequences.

## Pillar 4 one-page cheat sheet (contents). Printed as the one-page revision sheet §4.E2
1. **AD table:** Connected 0 · Static 1 · EIGRP summary 5 · eBGP 20 · EIGRP internal 90 · IGRP 100 · OSPF 110 · IS-IS 115 · RIP 120 · EIGRP external 170 · iBGP 200 · DHCP default 254 · Unknown 255.
2. **BGP path-selection mnemonic:** "N WLLA OMNI + Old Routers Clear Neighbours" with the higher/lower-wins column; FSM states; timers 60/180; AD 20/200; attribute categories.
3. **OSPF:**
   - Neighbour states; LSA types 1–5, 7 with the generator and scope.
   - Area-type ✓/✕ grid.
   - Timers 10/40 and 30/120.
   - Multicast 224.0.0.5/6; protocol 89.
   - RID rules; DR election rules; cost formula.
4. **EIGRP:** Metric formula (K1 = K3 = 1); FC rule RD < FD; 224.0.0.10; protocol 88.
5. **STP:**
   - Election order (lowest BID → lowest root path cost → lowest sender BID → lowest sender port ID).
   - Cost tables (short/long).
   - 802.1D timers 2/15/20.
   - RSTP roles/states.
   - Guard features and placement.
6. **VLAN/trunk:** 802.1Q fields; VLAN ranges; DTP matrix; EtherChannel mode matrix.
7. **FHRP comparison table:** HSRP v1/v2, VRRP, GLBP (multicast, port/protocol, VMAC, default priority, preempt).
8. **MPLS:** Label field widths; reserved labels 0–3; LDP 646; RD vs RT one-liners.
9. **QoS:**
   - DSCP table: EF 46; AF11 10 · AF12 12 · AF13 14 · AF21 18 · AF22 20 · AF23 22 · AF31 26 · AF32 28 · AF33 30 · AF41 34 · AF42 36 · AF43 38; CS1–CS7 = 8, 16, … 56.
   - AFxy = 8x + 2y.
   - Voice targets 150 ms / 30 ms / 1%.
   - Tc = Bc/CIR.
10. **Multicast:** Address ranges; MAC mapping rule; IGMP versions; PIM modes; well-known groups (224.0.0.1 all hosts, .2 all routers, .5/.6 OSPF, .9 RIPv2, .10 EIGRP, .13 PIMv2, .18 VRRP, .102 HSRPv2/GLBP).
11. Syslog levels 0–7 + mnemonic; wildcard-mask quick rules.
12. **Top-25 IOS `show` commands** (e.g. `show ip route`, `show ip ospf neighbor`, `show ip bgp summary`, `show spanning-tree`, `show etherchannel summary`, `show standby brief`, `show interfaces trunk`, `show mpls forwarding-table`, `show policy-map interface`, `show ip mroute`) with Junos/EOS/FRR equivalents.

## Pillar 4 mini-project — "Campus-to-Internet: a dual-homed enterprise built and verified as code"
- **Topology** (Containerlab, all free images: FRR + Arista cEOS or Nokia SR Linux):
  - Two campus access switches (VLANs 10/20/99 voice) with an LACP uplink to a collapsed-core pair running VRRP/HSRP and Rapid-PVST (the STP root aligned to the FHRP active router).
  - Multi-area OSPF (area 0 core, area 10 branch as totally stubby).
  - Two border routers with eBGP to ISP-A (AS 100) and ISP-B (AS 200), iBGP between the borders with next-hop-self.
  - ISPs peer with a "content AS" 300.
- **Policy requirements:**
  - ISP-A primary both ways (LP 200 inbound to us; prepend ×2 towards ISP-B).
  - Advertise only 198.51.100.0/24 (prefix list + max-prefix).
  - Tag and filter customer routes with communities.
  - PAT at the borders; QoS LLQ for voice on the WAN.
  - A GRE tunnel to a branch carrying OSPF.
- **Deliverables:**
  1. Design document: IP plan using VLSM (tie to 3.4), diagram drawn in the book's figure style.
  2. `topology.clab.yml` + startup configs.
  3. A `verify.py` test suite (pytest) asserting OSPF neighbours FULL, BGP sessions Established, the best path via ISP-A, failover to ISP-B within N seconds when the ISP-A link is cut, and voice DSCP EF preserved end-to-end. This ties to P10.
  4. A failure-injection runbook of 5 faults, each with symptoms → diagnosis → fix, feeding P11.
  5. A 2-minute "explain your project" interview script and résumé bullets.
- **Stretch goals:** Add an MPLS L3VPN provider core between the HQ and the branch instead of GRE; enable BFD and measure the convergence improvement.

## Pillar 4 end-of-chapter pack (~65 pp)
- **§4.E1 Short notes (~14 pp):**
  - One page per section (4.1–4.14): state machines as thumbnails, selection rules, defaults/timers, and the top 5 `show` commands per topic with what to look for.
  - Each page ends with a "say this in an interview" one-liner.
- **§4.E2 One-page revision sheet:** the cheat-sheet contents above on one dense A4 page. AD table, BGP mnemonic, OSPF LSA/area grid, STP election order and DSCP table get the visual priority.
- **§4.E3 Flashcards (~110 cards, front/back, tagged MUST/SHOULD/OPTIONAL):**
  - AD values (~13).
  - BGP steps and attributes (~15).
  - OSPF states/LSAs/area types/timers (~18).
  - STP roles/states/timers/guards (~14).
  - VLAN/trunk/EtherChannel modes (~10).
  - FHRP facts (~8).
  - EIGRP terms and formula (~6).
  - MPLS labels/RD/RT (~8).
  - DSCP/QoS (~10).
  - Multicast ranges and MAC mapping (~8).
- **§4.E4 Solved interview problems:**
  - (a) Full solutions to all 55 bank questions, in the template above (with CLI snippets and expected output where relevant).
  - (b) **12 long-form solved problems:**
    1. STP on a 4-switch square + diagonal, roles for VLAN 10 and VLAN 20 under PVST+ with different roots.
    2. The routing-table puzzle with 8 entries and 6 lookups.
    3. An OSPF 6-fault adjacency challenge, with symptom → `show` evidence → fix for each fault.
    4. A multi-area LSA inventory per router before and after a stub/NSSA conversion.
    5. An EIGRP topology table and FS/variance analysis.
    6. A BGP path-selection race with 5 candidate paths, stepping through all 13 steps.
    7. Dual-homed BGP inbound/outbound policy, with complete config + verification.
    8. RR loop-prevention trace with ORIGINATOR_ID/CLUSTER_LIST.
    9. HSRP tracking failover timeline.
    10. Two-way redistribution loop and tag fix.
    11. MPLS L3VPN packet walk with label tables at every node.
    12. QoS policy design for a 10 Mb/s branch WAN, with the full MQC config and a bandwidth check.
  - (c) Solution configs and expected outputs for every lab in 4.1–4.14 and for the mini-project test suite.

---

## Sources

**Exam blueprints and changes**
- Cisco Learning Network, CCNA exam topics (official, verify weights): https://learningnetwork.cisco.com/s/ccna-exam-topics
- CCNA exam topics summaries (v1.1 domains, AI/ML/Terraform additions, v2.0 transition dates): https://computingforgeeks.com/ccna-exam-topics/ · https://open-exam-prep.com/blog/ccna-200-301-exam-topics-lab-blueprint-2026 · https://www.examcert.app/blog/ccna-exam-topics-2026/ · https://www.packettracernetwork.com/ccna-ccnp-preparation/ccna.html · https://www.ituonline.com/blogs/200-301-ccna-exam/
- CCNA Official Cert Guide exam-updates appendix (O'Reilly): https://www.oreilly.com/library/view/ccna-200-301-official/9780138229856/appb.xhtml
- CCNP ENCOR v1.2 changes and domains: https://ipcisco.com/what-is-new-in-ccnp-encor/ · https://www.nwkings.com/ccnp-encor-v1-2-updates · https://open-exam-prep.com/study-guides/cisco-350-401/intro/exam-logistics-overview · https://trainingcamp.com/ccnp-encor-practice-test/
- CCNP and CCIE Enterprise Core ENCOR 350-401 Official Cert Guide, 2nd ed. (Pearson): https://www.pearson.com/en-ca/subject-catalog/p/ccnp-and-ccie-enterprise-core-encor-350-401-official-cert-guide/P200000011247/9780138216764

**Interview experiences (self-reported)**
- Cisco (STP scenarios, BGP attributes/path selection, OSPF LSA types; subnetting without a calculator; bitwise subnet check): https://www.glassdoor.com/Interview/Cisco-Interview-E1425-RVW13977842.htm · https://www.glassdoor.ca/Interview/Cisco-Interview-E1425-RVW32382771.htm · https://www.glassdoor.sg/Interview/Cisco-Interview-E1425-RVW78049185.htm · https://www.naukri.com/code360/interview-experiences/cisco-tech/interview-experience-by-b-raju-software-engineer-jul-2022-exp-0-2-years · https://www.jointaro.com/interviews/companies/cisco/experiences/associate-software-engineer-bangalore-rural-september-1-2024-no-offer-negative-a6ce5b65 · https://www.techinterview.org/companies/cisco-interview/
- Amazon NDE (iBGP/eBGP path manipulation, attributes, MSS/MTU, TCP, Python, LPs): https://static-pc.glassdoor.de/Interview/Amazon-Network-Development-Engineer-Interview-Questions-EI_IE6036.0,6_KO7,35.htm · https://www.glassdoor.fr/Entretien/Amazon-Entretien-E6036-RVW32207866.htm
- Meta / Arista / Juniper-style (iBGP loop avoidance, route reflectors and clusters, BGP ECMP, spine-leaf/EVPN): https://www.glassdoor.com.mx/Entrevista/Meta-Entrevista-E40772-RVW37223219.htm · https://static.glassdoor.es/Interview/sr-network-engineer-interview-questions-SRCH_KO0,19_IP85.htm · https://www.glassdoor.co.in/Interview/Juniper-Networks-Interview-E7224-RVW87706309.htm · https://clear.glassdoor.nl/Interview/Juniper-Networks-Network-Engineer-Interview-Questions-EI_IE7224.0,16_KO17,33_IP2.htm
- Qualcomm (sliding window, flow/congestion control for data protocol stack roles): https://www.glassdoor.sg/Interview/Qualcomm-Interview-E640-RVW409559.htm · https://www.glassdoor.co.in/Interview/Qualcomm-Interview-E640-RVW2056586.htm · https://www.glassdoor.co.uk/Interview/Qualcomm-Interview-E640-RVW11326753.htm
- Google (sliding-window TCP simulation in phone screen): https://www.glassdoor.com.au/Interview/Google-Interview-E9079-RVW62860997.htm

**Technical references to cite in the book (standards; not fetched in this session, authors to verify sections)**
- RFC 9293 (TCP), RFC 5681 (TCP congestion control), RFC 6298 (RTO), RFC 7323 (window scaling/timestamps), RFC 2018 (SACK), RFC 9438 (CUBIC), BBR (Cardwell et al., ACM Queue 2016) and IETF CCWG BBR drafts
- RFC 791 (IPv4), RFC 8200 (IPv6), RFC 4861 (NDP), RFC 4862 (SLAAC), RFC 1918, RFC 3021 (/31), RFC 1191 (PMTUD), RFC 2131 (DHCP), RFC 1034/1035 (DNS), RFC 8446 (TLS 1.3), RFC 9000/9114 (QUIC, HTTP/3)
- RFC 2328 (OSPFv2), RFC 5340 (OSPFv3), RFC 7868 (EIGRP informational), RFC 4271 (BGP-4), RFC 4456 (route reflection), RFC 1997 (communities), RFC 7938 (BGP in large DCs), RFC 6811 (RPKI ROV)
- RFC 5798 (VRRPv3), RFC 2281 (HSRP), RFC 3031/3032 (MPLS), RFC 5036 (LDP), RFC 4364 (BGP/MPLS L3VPN), RFC 2474/2597/3246 (DSCP, AF, EF), RFC 7761 (PIM-SM), RFC 3376 (IGMPv3), IEEE 802.1Q (VLANs, RSTP/MSTP), IEEE 802.1AX (LACP)
- Tools: Cisco Packet Tracer (netacad.com), GNS3 (gns3.com), Containerlab (containerlab.dev), FRRouting (frrouting.org), Wireshark (wireshark.org)

> Research caveat for the editor: the official Cisco exam-topics PDF host (learningcontent.cisco.com) was not reachable from the research session's network. Domain weights above come from memory cross-checked against third-party summaries and must be verified against cisco.com before print. Interview reports are anonymous and self-reported (2012–2026), so the company-tag matrix is indicative, not definitive.
