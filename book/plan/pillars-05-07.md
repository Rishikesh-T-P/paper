# Chapter Plan: Pillars 5, 6 and 7

**Book:** *From Zero to Packet: A Placement Textbook for Network Engineering and Networking-Software Roles*
**Scope of this file:** Pillar 5 (Data Centre and Cloud Networking), Pillar 6 (Wireless and Cellular), Pillar 7 (Operating Systems and Socket Programming)
**Status:** Planning document only. It contains no chapter prose.
**Spelling:** British (centre, optimise, behaviour, colour, licence as a noun, programme for a schedule and program for code).

---

## 0. How these three pillars fit the book

| Pillar | Main hiring signal it serves | Strongest company pull | Depends on | Feeds into |
|---|---|---|---|---|
| 5 Data Centre and Cloud | "Can you reason about networks at hyperscale and in the public cloud?" | Google, Microsoft (Azure Networking), Amazon NDE, Arista, Juniper, Broadcom | Pillar 3 (CN), Pillar 4 (R&S: BGP, OSPF/IS-IS) | Pillar 10 (Automation), Pillar 11 (Troubleshooting) |
| 6 Wireless and Cellular | "Do you understand the air interface, the MAC and the security handshake well enough to write firmware or debug a radio?" | Qualcomm, Broadcom, Cisco (Meraki/Catalyst Wireless), Nokia, Juniper (Mist), Arista (Wi-Fi) | Pillar 3 (CN), Pillar 9 (Security basics), Pillar 12 (signals) | Pillar 11 (Troubleshooting) |
| 7 OS and Sockets | "Can you write correct concurrent C that talks to the network, and do you know what the kernel does underneath?" | Cisco, Juniper, Arista, Qualcomm, Broadcom, Nokia (SR Linux), Google | Pillar 2 (C), Pillar 1 (DSA) | Pillar 8 (Linux tools), Pillars 5 and 6 (router internals, firmware) |

### Shared design conventions for the three chapters

These conventions should match the rest of the book. If the master style guide differs, the master style guide wins.

- **Box types:**
  - *Analogy* (soft teal): one everyday analogy per section.
  - *Worked Example* (white card, numbered): a concrete calculation or walk-through.
  - *Trap* (amber with warning glyph): a common interview mistake.
  - *Company Lens* (small coloured chip): which companies ask this and how deeply.
  - *Lab* (dark terminal style): hands-on steps with expected output.
  - *Deep Dive* (grey, optional): skippable on a first read.
- **Figure styles:**
  - One consistent icon set: router = circle with four arrows; L3 switch = square with arrows; leaf/spine = rounded rectangle tagged L or S; host = monitor; AP = dome with arcs; UE = phone.
  - Colour key: data plane = blue, control plane = orange, management = grey, encapsulation headers = stacked coloured bars (outer = darker).
- **Difficulty tags for questions:** [E] easy (definition or recall), [M] medium (mechanism or comparison), [H] hard (design, edge case or debugging), [X] expert (spec-level or kernel-level).
- **Company tag codes:**
  - CSCO Cisco
  - QCOM Qualcomm
  - GOOG Google
  - MSFT Microsoft
  - AMZN Amazon NDE
  - JNPR Juniper
  - ANET Arista
  - NOK Nokia
  - AVGO Broadcom
- **Dependency marker:** each section opens with "You need: ..." and points to the earlier pillar or section.

---

## 0A. Book-wide requirements applied to Pillars 5–7

The book stays **fully comprehensive**. Nothing in this plan is trimmed to fit any reader's timetable. The four requirements below are layered on top of the full content.

### 0A.1 Navigation tags (Must / Should / Optional)

Every section, lab and question carries one tag, printed as a coloured chip next to the heading:

- green **MUST**: asked in most target interviews, and required for later sections;
- blue **SHOULD**: frequently asked by one or more target companies, or needed for the mini-project;
- grey **OPTIONAL**: depth for specialists (firmware, SDK, hyperscaler design rounds).

Each section also prints an indicative *Must-path* study-day estimate, so a reader with limited time (for example, 8 weeks for the whole book) can plan a fast route. These estimates are only a reading guide: Should and Optional sections stay in the book in full.

**Pillar 5 tag table**

| Section | Tag | Must-path days |
|---|---|---|
| 5.2.1 Why DCs broke the campus model | Must | 0.25 |
| 5.2.2 Clos and spine-leaf maths | Must | 0.5 |
| 5.2.3 ECMP | Must | 0.5 |
| 5.2.4 eBGP underlay, BFD, unnumbered | Must | 0.5 |
| 5.2.5 VXLAN | Must | 0.5 |
| 5.2.6 EVPN | Should | 0.5 |
| 5.2.7 SDN, OpenFlow, P4 | Should | 0.5 |
| 5.2.8 Router internals: RIB/FIB/TCAM/ASIC | Must | 0.75 |
| 5.2.9 Load balancers | Should | 0.25 |
| 5.2.10 Anycast and CDN | Should | 0.25 |
| 5.2.11 AWS VPC | Must | 0.5 |
| 5.2.12 Azure VNet | Should (Must for MSFT) | 0.25 |
| 5.2.13 Direct Connect / ExpressRoute / VPN | Should (Must for MSFT/AMZN) | 0.25 |
| 5.2.14 Life of a request | Optional | — |
| End-of-chapter pack | Must | 0.5 |
| **Must-only total** | | **≈ 4 days** (≈ 6.5 days including Should) |

**Pillar 6 tag table**

| Section | Tag | Must-path days |
|---|---|---|
| 6.2.1 RF, dB, link budget | Must | 0.25 |
| 6.2.2 OFDM, QAM, MIMO | Must | 0.5 |
| 6.2.3 802.11 architecture and generations | Must | 0.25 |
| 6.2.4 CSMA/CA and DCF timing | Must | 0.5 |
| 6.2.5 802.11 frame format | Must | 0.5 |
| 6.2.6 Connection lifecycle | Must | 0.5 |
| 6.2.7 WPA2/802.1X/WPA3/PMF | Must | 0.5 |
| 6.2.8 QoS, aggregation, power save | Should | 0.25 |
| 6.2.9 Wi-Fi 6/6E/7 | Must (QCOM/AVGO), Should (others) | 0.5 |
| 6.2.10 Roaming and enterprise design | Should | 0.25 |
| 6.2.11 Linux and firmware view | Should (Must for QCOM/AVGO) | 0.25 |
| 6.2.12 LTE and 5G | Should (Must for NOK/QCOM modem) | 0.5 |
| End-of-chapter pack | Must | 0.5 |
| **Must-only total** | | **≈ 4.5 days** (≈ 6 days including Should) |

**Pillar 7:** the tags are printed inline on each section heading in 7.2. The Must-only total is ≈ 5 days, or ≈ 6.25 days including Should.

**Fast route across the three pillars** (illustrative, for a reader planning by tags): about 13.5 study days for Must-only, 19 days including Should. The full-depth reading is the ~12 weeks given in the chapter headers.

### 0A.2 Fully self-contained PDF

- Every concept, table, formula, configuration file and code listing that a reader needs is printed in the book. Long listings go in per-chapter appendices: 5-A Containerlab topology files and FRR configs; 6-A hostapd/wpa_supplicant configs, the PTK script and the frame-parser source; 7-A complete C sources for every server, the load generator and the allocator.
- Labs include exact commands, expected output (as printed screenshots or terminal blocks) and a "what if it fails" table. Readers can follow along on paper even without running anything.
- Pcap-derived figures (Pillar 6) are reproduced as annotated frame tables, so no external capture file is needed to learn.
- The **Sources** lists are author-verification references only. They are printed in a small-type "Further reading (optional)" box. No reader task depends on them.
- Standards facts the authors must check before print (MCS tables, ExpressRoute limits, cloud free-tier terms, Indian 6 GHz status) are flagged `[VERIFY]` in drafts and must be resolved, not left as links.

### 0A.3 Every interview question gets a full in-book solution

- The question banks in 5.5, 6.5 and 7.5 (40, 42 and 45 questions) are each paired with a **Solutions** section at the end of the chapter, with the same numbering.
- Solution format for each question:
  1. a 1–2 sentence "say this first" answer;
  2. the full explanation, with a diagram reference where relevant;
  3. a worked calculation or code (complete and compilable for coding questions, with complexity stated);
  4. "Follow-ups the interviewer may ask", with short answers;
  5. "Common wrong answer".
- [E] solutions run about ⅓ page, [M] about ½ page, [H]/[X] 1–2 pages. Estimated solution pages per pillar: P5 ≈ 28, P6 ≈ 28, P7 ≈ 34, already included in the page estimates below. The headline page counts in the chapter headers rise accordingly: **P5 ≈ 140–155, P6 ≈ 125–140, P7 ≈ 155–170**.

### 0A.4 End-of-chapter pack (identical structure for every pillar)

| Component | Contents | Size |
|---|---|---|
| **Short notes** | Section-by-section bullet summary (5–10 bullets per section) with the key numbers and figure thumbnails | 6–8 pages |
| **One-page revision sheet** | The cheat-sheet contents listed in 5.7 / 6.7 / 7.7, condensed to one side of A4 (the double-sided "cheat sheet" becomes the revision sheet plus its reverse "formulae and numbers" side) | 1 page (+ reverse) |
| **Flashcards** | Printed cut-out cards, Q on front and A on back, 9 per page. P5: 60 cards, P6: 60 cards, P7: 70 cards. Each carries a tag (Must/Should/Optional) and company chips | 7–8 pages |
| **Solved interview problems** | Full solutions to every question in the bank (see 0A.3), plus 5 extended "whiteboard round" problems per pillar written as a dialogue between interviewer and candidate | 28–34 pages |
| **Self-test** | A 20-question mixed quiz with an answer key and a score band: "ready" / "revise Must sections" | 2 pages |

Example extended whiteboard problems:

- **P5:** size a fabric for 10K servers; debug ECMP imbalance; design hub-spoke with ExpressRoute plus VPN failover; design an LPM structure; design an L4 LB.
- **P6:** decode a hex 802.11 frame; derive a PTK from given values; troubleshoot slow Wi-Fi at −50 dBm; schedule RUs; walk the 5G registration.
- **P7:** fork-tree prediction; producer-consumer code; Banker's safety check; an epoll server design for 100K connections; the NIC-to-`recv()` trace.

---

# PILLAR 5: Data Centre and Cloud Networking

## 5.0 Chapter header

- **Title:** *Chapter 5: Inside the Hyperscale Fabric: Data Centres, Router Internals and the Public Cloud*
- **One-line promise:** By the end you can draw a spine-leaf fabric from memory, explain how a packet crosses a VXLAN/EVPN overlay, say where in the ASIC a route lookup happens, and design a two-region AWS/Azure network with on-premises connectivity.
- **Prerequisites:**
  - Pillar 3: IP addressing and subnetting, the TCP/UDP headers, ARP, MTU and fragmentation.
  - Pillar 4: VLANs and STP, OSPF/IS-IS adjacencies, BGP sessions, attributes and best-path selection.
  - Pillar 8 (light): `ip route`, `ip link`, Linux bridges.
  - Not required: any prior cloud experience.
- **Estimated pages:** 110–125, with about 45 figures.
- **Must-path estimate:** ≈ 4 study days for the Must sections only (see the tag table in 0A.1). The book keeps all sections in full.
- **Weeks (full read):** 4 weeks at about 10 hours per week.
  - Week 1: sections 5.1–5.4 (fabric, ECMP, BGP in the data centre).
  - Week 2: sections 5.5–5.7 (VXLAN/EVPN, SDN/P4).
  - Week 3: sections 5.8–5.10 (router internals, load balancers, anycast/CDN).
  - Week 4: sections 5.11–5.14 (cloud) plus the mini-project.

## 5.1 Learning objectives

1. Explain why tree topologies with STP fail at data-centre scale, and derive the properties of a 3-stage folded Clos (spine-leaf).
2. Compute the oversubscription ratio, the bisection bandwidth and the maximum server count for a given leaf/spine port budget.
3. Describe ECMP hashing (the 5-tuple), and explain polarisation, hash-bucket resilience and why per-packet spraying causes reordering.
4. Justify eBGP as the underlay routing protocol (RFC 7938): ASN plans, `allowas-in`, BFD and `maximum-paths`.
5. Draw the VXLAN header bit by bit, calculate the encapsulation overhead (50 bytes) and choose an underlay MTU.
6. Explain the EVPN route types 2, 3 and 5, and walk a packet through symmetric IRB with an anycast gateway.
7. Contrast traditional control planes with SDN (OpenFlow match-action) and programmable data planes (P4 parser, match-action pipeline, deparser).
8. Trace a packet through router internals: ports, MAC, parser, L2/L3 lookup in the FIB (LPM in TCAM or algorithmic), ACL TCAM, queues/VOQ, rewrite, egress. Distinguish the RIB from the FIB.
9. Compare L4 and L7 load balancers, DSR, consistent hashing (Maglev) and health checking.
10. Explain anycast with BGP, and how a CDN uses DNS, anycast and caching.
11. Design an AWS VPC (subnets, route tables, IGW, NAT GW, SGs vs NACLs, Transit Gateway, PrivateLink) and the equivalent Azure VNet (NSG, UDR, VNet peering, Virtual WAN).
12. Explain Direct Connect and ExpressRoute: private peering, Microsoft peering, BGP communities, redundancy and the 4-byte private ASN rules.
13. Troubleshoot five canonical cloud failures, such as an asymmetric route through a NAT, a blackholed MTU, or a missing SG return rule (it is stateful) versus a missing NACL ephemeral-port rule.

## 5.2 Section-by-section outline

### 5.2.1 Why data centres broke the campus model

- **Core idea:** East-west traffic, which runs server to server, now dominates. Three-tier trees with STP waste half their links and create choke points, so data centres moved to flat, routed, multipath fabrics.
- **Analogy:** A city with one flyover where every road meets (core) versus a grid of parallel streets (Clos). On a grid, any crossing is the same number of turns away and a closed street barely matters.
- **Worked example:** 40 racks with 2 uplinks each in a three-tier design. STP blocks one uplink per rack, so 50% of the uplink capacity sits idle. Then show the same racks on four spines with every link forwarding, giving a 2× capacity gain.
- **Figures:**
  - **Fig 5.1:** Side-by-side diagram.
    - Left panel: core, aggregation and access tiers, with STP-blocked links drawn as dashed red lines with an "X".
    - Right panel: four spines (S1–S4) above eight leaves (L1–L8), fully meshed, with all links solid blue.
    - Caption: "Same cables, double the usable bandwidth."
  - **Fig 5.2:** Stacked bar chart of traffic mix, "north-south vs east-west".
    - Two bars, "Enterprise campus" and "Hyperscale DC".
    - Label the values as indicative; cite the Google Jupiter paper for the qualitative trend.
- **Trap:** Saying "spine-leaf removes STP entirely." STP may still run on host-facing edge ports, as a guard; it is just not used for fabric loop prevention.

### 5.2.2 Clos networks and spine-leaf maths

- **Core idea:** A folded 3-stage Clos gives every leaf the same hop count (leaf → spine → leaf) to every other leaf. Capacity is added by adding spines; reach is added by adding leaves or a super-spine tier (5-stage).
- **Analogy:** Airline hubs. Every regional airport (leaf) has one flight to every hub (spine), so any trip is "fly to a hub, fly out". Adding a hub adds capacity on every route at once.
- **Worked example:** "Size my fabric."
  - Leaf: 48 × 25G server ports and 8 × 100G uplinks.
  - Spine: 64 × 100G ports.
  - Oversubscription = (48 × 25) / (8 × 100) = 1200/800 = 1.5:1.
  - Maximum leaves = 64 (spine ports), so maximum servers = 64 × 48 = 3,072.
  - Number of spines = 8 (one per uplink).
  - Then ask: "What changes for 1:1?" Answer: either 12 × 100G uplinks (and 12 spines), or fewer server ports.
  - Extension: a 5-stage design with super-spines. Show a pod of 32 leaves and 4 spines, with each spine having 32 down and 32 up ports.
- **Figures:**
  - **Fig 5.3:** Annotated 2-tier fabric.
    - Port counts written on the links (e.g. "8 × 100G").
    - A callout box carrying the oversubscription formula.
  - **Fig 5.4:** Three-tier Clos (super-spine planes, pods). Colour each "plane" differently to show the Facebook/Meta F16 or Google Jupiter style.
  - **Fig 5.5:** Bisection-bandwidth illustration. A vertical cut through the fabric, with the links crossing the cut highlighted.
- **Trap:** Confusing oversubscription (a ratio at the leaf) with blocking (the Clos property). Also, assuming a 1:1 leaf is "non-blocking" overall when the spines are under-provisioned.
- **Company Lens:** GOOG and MSFT ask sizing questions; ANET and JNPR ask "why not 3-tier?" and "what is a super-spine?".

### 5.2.3 ECMP: many equal paths, one flow per path

- **Core idea:**
  - The router keeps up to N equal-cost next hops. It hashes header fields (typically the 5-tuple) to pick one.
  - All packets of one flow take one path, which avoids reordering. Different flows spread across the paths.
- **Analogy:** A toll plaza with eight booths where your booth is decided by the last digit of your number plate. The same car always gets the same booth, and the cars overall spread evenly.
- **Worked example:**
  - Use a toy hash: (src_port + dst_port) mod 4, over 4 spines.
  - Hash six flows and show the per-spine load. Reveal the imbalance from two elephant flows.
  - Then remove spine 3:
    - Naive modulo re-hash moves about 75% of flows.
    - Resilient/consistent hashing moves only the flows that were on spine 3, about 25%.
- **Figures:**
  - **Fig 5.6:** Hash pipeline. 5-tuple fields → hash function block (CRC16/CRC32 labelled) → "mod N" → next-hop table with 4 rows → chosen egress port.
  - **Fig 5.7:** "Hash polarisation". Two tiers both using the same hash seed, so all flows from one leaf land on the same downstream subset. Fix: a per-device seed.
  - **Fig 5.8:** Resilient hashing bucket table before and after a member failure. 16 buckets, with the reassigned buckets shaded.
- **Sub-topics:**
  - Weighted ECMP (UCMP).
  - Flowlet switching (CONGA and similar).
  - Packet spraying versus RDMA/RoCE ordering needs (mention only).
  - Elephant and mice flows.
  - `maximum-paths` in BGP.
  - Linux `fib_multipath_hash_policy`.
- **Trap:** Saying "ECMP load-balances packets." It balances flows. Per-packet balancing reorders TCP segments and triggers spurious fast retransmits.

### 5.2.4 Routing the fabric: eBGP underlay, BFD and unnumbered links

- **Core idea:** RFC 7938 recommends eBGP everywhere in large DCs. It has a simple policy model, a well-understood failure scope, a per-hop ASN and fewer moving parts than an IGP plus iBGP with route reflectors.
- **Analogy:** Every rack is its own small country (an ASN) with a border post (an eBGP session) to each spine. Each country's passport stamp (the AS_PATH) prevents loops.
- **Worked example:** ASN plan.
  - All spines share AS 65000. Each leaf gets a unique ASN: 65001, 65002, and so on.
  - Show why a leaf-to-leaf path is AS_PATH {65000, 65002}.
  - Explain why spines in the same ASN do not need `allowas-in`, but leaves that share an ASN would.
  - Show BFD at 300 ms × 3 giving sub-second failover, versus the BGP hold timer of 180 s.
  - Configure on two virtual leaves in FRR: `neighbor swp1 interface remote-as external` (BGP unnumbered, using IPv6 link-local next hops per RFC 5549/8950).
- **Figures:**
  - **Fig 5.9:** Spine-leaf diagram with ASNs printed on each box and AS_PATHs shown as speech bubbles on two routes.
  - **Fig 5.10:** Failure timeline graph.
    - X-axis: time in ms.
    - Three lines: "BGP hold timer", "BFD", "link-down event".
    - Y-axis: "traffic lost".
- **Trap:** Forgetting that a private 2-byte ASN range gives only 1,023 ASNs (64512–65534). Large fabrics use the 4-byte private range (4200000000–4294967294).
- **Company Lens:** AMZN NDE and MSFT backbone roles expect IS-IS/BGP/MPLS knowledge. Mention Segment Routing as a pointer to Pillar 4.

### 5.2.5 Overlays: VXLAN

- **Core idea:** VXLAN carries a tenant's Ethernet frame inside UDP/IP, on destination port 4789. A 24-bit VNI gives about 16 million segments, against 4,094 VLANs. Tenants then get L2 adjacency over a routed L3 underlay.
- **Analogy:** Putting a sealed envelope (the original frame) inside a courier parcel (the outer IP/UDP) addressed from one office mailroom (VTEP) to another. The courier never opens the inner envelope.
- **Worked example:** Byte-by-byte encapsulation.
  - Inner frame: 1,500-byte IP payload + 14-byte Ethernet header.
  - Outer additions: IPv4 20 + UDP 8 + VXLAN 8 + outer Ethernet 14 = 50 bytes.
  - Underlay IP MTU must therefore be at least 1,550. The standard practice is jumbo 9,216 on fabric links.
  - Note that the outer UDP source port is a hash of the inner flow, so ECMP entropy is preserved.
- **Figures:**
  - **Fig 5.11:** Encapsulation "Russian doll" stacked bar.
    - Outer Eth | Outer IP | UDP (dst 4789, src = hash) | VXLAN (Flags 8b, Reserved 24b, VNI 24b, Reserved 8b) | Inner Eth | Inner IP | Payload | FCS.
    - Byte counts are written under each block.
  - **Fig 5.12:** Two leaves acting as VTEPs (loopbacks 10.0.0.1 and 10.0.0.2).
    - Hosts A (VNI 10010) and B (VNI 10010) on different racks.
    - The packet path is drawn as a "tunnel" tube across the spines.
- **Sub-topics:**
  - Flood-and-learn with multicast underlay versus ingress replication.
  - BUM traffic.
  - Comparison with Geneve and NVGRE (Azure historically used NVGRE, now uses VXLAN), in a table.
- **Trap:** Saying VXLAN "extends VLANs". It carries L2 frames over L3; the VNI is not a VLAN tag. Also: MTU problems show up as "ping works, SSH or HTTPS hangs".

### 5.2.6 EVPN: a control plane for the overlay

- **Core idea:** BGP EVPN (AFI 25 / SAFI 70) advertises MAC and IP reachability and VTEP membership, which replaces flood-and-learn. It also enables multihoming (ESI) and distributed anycast gateways.
- **Analogy:** Instead of shouting "Who has Ravi?" across the building (flooding), every receptionist publishes a shared directory (BGP), saying who sits at which desk and on which floor.
- **Worked example:** Host A (10.1.10.11, MAC aa:aa) moves from leaf L1 to L3.
  - Show the Type-2 route: RD, ESI, Ethernet Tag, MAC, IP, Label1 = L2VNI, Label2 = L3VNI, plus RT extended communities.
  - Show the MAC Mobility extended community sequence number incrementing from 0 to 1, so the old route is withdrawn.
  - Then compare symmetric and asymmetric IRB. In symmetric IRB, A on VLAN 10 reaches C on VLAN 20 through the L3VNI 50001, with routing at both ingress and egress leaves.
- **Figures:**
  - **Fig 5.13:** EVPN route-type table: types 1, 2, 3, 4, 5, with columns "Purpose", "Key fields", "When you see it".
  - **Fig 5.14:** Sequence diagram of the MAC move. Lanes for L1, Spine-RR, L3 and remote L5, with arrows for the BGP UPDATE and withdraw.
  - **Fig 5.15:** Anycast gateway. Every leaf owns 10.1.10.1 with the same virtual MAC. A host's ARP is answered locally, shown with a "first hop = local leaf" annotation.
- **Trap:** Using the same RT import/export across tenants by accident, which leaks VRFs. Also: Type-5 versus Type-2-with-IP confusion.
- **Company Lens:** ANET and JNPR interviews explicitly cover EVPN/VXLAN, as do NOK SR Linux and CSCO Nexus roles.

### 5.2.7 SDN, OpenFlow and P4

- **Core idea:**
  - SDN separates the control plane, logically centralised in a controller, from a simple data plane.
  - OpenFlow standardised match-action flow tables.
  - P4 goes further by letting you *program the parser and pipeline itself*.
- **Analogy:**
  - Traditional router: a chef who decides the menu and cooks.
  - SDN: a head chef (controller) sending recipes to line cooks (switches).
  - P4: you can also redesign the kitchen layout.
- **Worked example:**
  - Write three OpenFlow rules on Mininet `s1`:
    - priority 100: match `ip,nw_dst=10.0.0.2` → `output:2`
    - priority 50: match `arp` → `FLOOD`
    - priority 0: → `CONTROLLER`
  - Show `ovs-ofctl dump-flows s1` with packet counters rising during a ping.
  - Then sketch a P4_16 fragment: parser states for Ethernet → IPv4, a `table ipv4_lpm { key = { hdr.ipv4.dstAddr: lpm; } actions = { forward; drop; } }`, and decrementing TTL in an action.
- **Figures:**
  - **Fig 5.16:** Three-layer SDN stack.
    - Applications on top (northbound REST).
    - Controller in the middle (ONOS/Ryu/OpenDaylight).
    - Switches below (southbound OpenFlow/P4Runtime/gNMI).
  - **Fig 5.17:** PISA pipeline: Programmable Parser → Match-Action stages 1..N (each with a table and an ALU) → Deparser. The metadata bus is drawn underneath.
  - **Fig 5.18:** Google B4 or Andromeda as a real-world SDN callout, a simplified map with a controller cloud.
- **Trap:** "SDN means no distributed protocols." Most production fabrics still run BGP. SDN often means centralised *policy* or *TE*, as in B4 for WAN TE.

### 5.2.8 Router and switch internals: RIB, FIB, TCAM and the ASIC pipeline

- **Core idea:**
  - Control-plane software (the routing protocols) builds the RIB.
  - The best routes are downloaded to the FIB in hardware.
  - Line-rate forwarding happens in ASIC pipelines, using TCAM/SRAM lookup structures.
  - Exceptions are punted to the CPU, which is rate-limited by CoPP.
- **Analogy:**
  - RIB: the full atlas in the manager's office, with every road known.
  - FIB: the laminated card taped to each toll booth, with only the best exit per destination.
  - TCAM: a booth worker who checks every card simultaneously.
- **Worked example A (RIB to FIB):**
  - The prefix 10.1.0.0/16 is learned from OSPF (AD 110) and from eBGP (AD 20). The RIB keeps both, and the FIB installs only eBGP.
  - Show `show ip route` versus `show ip cef`, or the Linux equivalents `ip route show table all` versus the kernel FIB.
- **Worked example B (LPM in TCAM):**
  - Entries: 10.0.0.0/8 → A, 10.1.0.0/16 → B, 10.1.2.0/24 → C, 0.0.0.0/0 → D.
  - Show the ternary bit patterns (e.g. 00001010.00000001.xxxxxxxx.xxxxxxxx).
  - Look up 10.1.2.7; all match. Explain that entries are sorted by prefix length so the lowest index wins and C is chosen.
  - Compute the TCAM cost: a 144-bit wide entry × 512K entries. Explain why TCAM is power-hungry (parallel compare), with a rule of thumb.
- **Worked example C (pipeline walk):**
  - A packet goes through: ingress port → MAC/PCS → parser (extract L2/L3/L4) → ingress ACL (TCAM) → L2 lookup (MAC table, exact-match hash) → L3 lookup (LPM) → ECMP group resolution → next-hop/adjacency (rewrite MAC, decrement TTL) → traffic manager (VOQ, buffer, scheduler: SP/WRR/DWRR) → egress ACL → egress port.
- **Figures:**
  - **Fig 5.19:** Control plane versus data plane split.
    - Route processor (CPU, RAM, the BGP/OSPF/IS-IS processes, RIB) at top.
    - The arrow "FIB download (via the driver/SDK)" goes down to the line card or ASIC with the FIB/adjacency tables.
    - A punt path arrow goes up through "CoPP policer".
  - **Fig 5.20:** TCAM lookup.
    - Four rows of value/mask, the search key on top, and match lines lighting up.
    - The priority encoder picks the lowest index.
    - An adjacent SRAM holds the result.
  - **Fig 5.21:** Full ASIC pipeline flowchart, ingress to egress, with a buffer/traffic manager in the centre. Label typical Broadcom Trident/Tomahawk/Jericho concepts generically (shared buffer vs deep buffer with VOQ).
  - **Fig 5.22:** "Merchant silicon vs custom silicon" comparison table:
    - Merchant: Broadcom, Marvell, Cisco Silicon One sold as merchant, Nvidia Spectrum.
    - Custom: Juniper Trio/Express, Cisco ASR/QuantumFlow.
    - Columns: buffer depth, programmability, typical role.
- **Sub-topics:**
  - Adjacency table and ARP/ND glean.
  - Recursive next-hop resolution.
  - FIB compression.
  - Hash-based exact match versus LPM algorithms (tries, DIR-24-8, as a forward reference to Pillar 1's trie chapter).
  - CoPP.
  - NSF/GR and NSR (keeping forwarding during control-plane restart).
  - Store-and-forward versus cut-through.
  - Shallow versus deep buffers (the incast problem).
- **Trap:** "TCAM stores the routing table." It stores the FIB, often in algorithmic SRAM plus TCAM. Also: ACL explosion when port ranges expand into many TCAM entries. Worked: the port range 1024–65535 requires 6 ternary entries.
- **Company Lens:** AVGO, ANET, JNPR and CSCO platform and SDK roles probe this deeply. Expect "design a longest-prefix-match data structure" as a coding question.

### 5.2.9 Load balancers

- **Core idea:**
  - Load balancers spread connections over backends.
  - L4 LBs work on the 5-tuple, via NAT or DSR. L7 LBs terminate TCP/TLS and route on HTTP content.
  - Hyperscalers build L4 LBs in software, using ECMP and consistent hashing (Google Maglev, the Azure Ananta design).
- **Analogy:** A restaurant host (VIP) who seats you at a table (backend).
  - L4 only looks at your party size.
  - L7 reads your reservation note ("vegetarian, window seat").
  - DSR means the waiter brings food straight to you without going back through the host.
- **Worked example:**
  - Consistent hashing with a Maglev lookup table of size M = 7 and 3 backends.
  - Compute the permutation tables using offset and skip, then fill the table. Remove one backend and count the changed entries.
  - Contrast with a plain modulo approach.
  - Also cover DSR: the backend has the VIP on its loopback, ARP is suppressed, and reply packets bypass the LB. Show why this lets the LB handle only inbound traffic.
- **Figures:**
  - **Fig 5.23:** Three LB modes side by side: NAT/proxy, DSR, and tunnel (IP-in-IP/GRE to backends). Arrows are numbered 1–4 for request and response.
  - **Fig 5.24:** Maglev architecture. Router → ECMP → Maglev instances (stateless consistent hashing plus a connection-tracking table) → backends.
  - **Fig 5.25:** Health-check state machine: Up → Suspect (after N fails) → Down → probing → Up.
- **Sub-topics:**
  - Algorithms: round robin, least connections, weighted.
  - Session persistence (sticky sessions).
  - SNAT port exhaustion (a link to Azure SNAT).
  - TLS termination versus passthrough.
  - AWS ALB, NLB and GWLB; Azure Load Balancer versus Application Gateway versus Front Door.
- **Trap:** Assuming an L4 LB "sees the URL". Also: SNAT port exhaustion under many short connections to one destination.

### 5.2.10 Anycast and Content Delivery Networks

- **Core idea:** Anycast announces the same prefix from many sites so BGP delivers each user to the nearest one, in AS-path or IGP terms. CDNs combine anycast or DNS steering with edge caches, bringing content close to users.
- **Analogy:** Every city has a branch of the same bank with the same phone number. The telephone exchange connects you to the branch nearest you.
- **Worked example:**
  - 1.1.1.0/24 is announced from Mumbai, Singapore and Frankfurt.
  - A user in Chennai has an ISP whose best path, by shortest AS_PATH, reaches Mumbai.
  - Mumbai withdraws for maintenance, and BGP converges to Singapore.
  - Discuss why TCP over anycast mostly works (routes are stable) and when it breaks: a mid-session path change sends packets to a site with no TCP state.
  - Then compute a CDN cache-hit benefit: origin RTT 220 ms, edge RTT 15 ms, hit ratio 90%, so expected RTT = 0.9 × 15 + 0.1 × (15 + 220) = 37 ms.
- **Figures:**
  - **Fig 5.26:** World map schematic with three anycast PoPs sharing one prefix. Coloured catchment regions and user arrows.
  - **Fig 5.27:** CDN request flow.
    - Steps: DNS resolution (CNAME → CDN) → edge PoP → cache hit/miss → mid-tier → origin.
    - Labels: TTLs, cache-control headers.
- **Sub-topics:**
  - DNS-based GSLB versus anycast.
  - EDNS Client Subnet.
  - Anycast DNS (root servers).
  - DDoS absorption.
  - Google Cloud CDN, Azure Front Door, CloudFront (names only).
- **Trap:** "Anycast picks the geographically nearest site." It picks the BGP-nearest one, which can be on another continent.

### 5.2.11 The public cloud, part 1: AWS VPC

- **Core idea:**
  - A VPC is a software-defined, region-scoped private network.
  - Subnets are per-AZ. Route tables decide whether a subnet is "public" (a route to the IGW) or "private" (a route to a NAT GW).
  - Security groups are stateful and attach to ENIs. NACLs are stateless and attach to subnets.
- **Analogy:**
  - VPC: a gated campus.
  - Subnets: buildings.
  - Route table: signposts.
  - IGW: the main gate.
  - NAT GW: a one-way turnstile, so you can go out but strangers cannot come in.
  - SG: the guard at each room door, who remembers who left.
  - NACL: the guard at the building entrance, who checks everyone both ways and remembers nothing.
- **Worked example:** A three-tier web app in 10.0.0.0/16 across 2 AZs.
  - Public 10.0.1.0/24 and 10.0.2.0/24. Private app 10.0.11.0/24 and 10.0.12.0/24. DB 10.0.21.0/24 and 10.0.22.0/24.
  - Route tables written out:
    - Public: 10.0.0.0/16 local; 0.0.0.0/0 igw-xxx.
    - Private: 0.0.0.0/0 nat-xxx.
  - Show the reserved 5 IPs per subnet (.0, .1 router, .2 DNS, .3 future, .255), so a /24 gives 251 usable addresses.
  - SG rules: ALB-SG allows 443 from 0.0.0.0/0. App-SG allows 8080 from ALB-SG (an SG reference). DB-SG allows 5432 from App-SG.
  - NACL trap: the return traffic needs the ephemeral ports 1024–65535 outbound.
- **Figures:**
  - **Fig 5.28:** Standard AWS architecture diagram.
    - Region box → VPC box → two AZ columns → three subnet rows.
    - IGW at the top, a NAT GW in each public subnet, the ALB spanning both public subnets.
    - Route-table callouts.
  - **Fig 5.29:** SG versus NACL comparison table with these rows: level, stateful?, allow/deny, rule evaluation, default.
  - **Fig 5.30:** Connectivity options.
    - VPC peering (non-transitive, drawn as a triangle with an "X" on the transitive leg).
    - Transit Gateway (hub-spoke).
    - PrivateLink (an interface endpoint pointing to an NLB in another VPC).
    - Gateway endpoints (S3/DynamoDB).
- **Sub-topics:**
  - Elastic IPs.
  - Egress-only IGW for IPv6.
  - VPC Flow Logs (link to Pillar 11).
  - Route 53 Resolver.
  - The Nitro/Hyperplane mention: AWS virtual networking is implemented on Nitro cards, not in the guest. This is why ARP inside a VPC is answered by the hypervisor layer.
- **Trap:**
  - "VPC peering is transitive." It is not.
  - "Adding a deny in a SG." SGs have allow rules only.
  - Overlapping CIDRs block peering.

### 5.2.12 The public cloud, part 2: Azure VNet

- **Core idea:**
  - Azure VNets are region-scoped. Subnets span AZs (unlike AWS).
  - NSGs can attach to a subnet or a NIC.
  - UDRs override system routes, for example to force traffic through an NVA or firewall.
  - VNet peering and Virtual WAN provide hub-and-spoke.
- **Analogy:** The same campus as AWS, but each building spans every zone, and the "signpost overrides" (UDRs) let you force all visitors past the security desk (Azure Firewall).
- **Worked example:** Hub-spoke.
  - Hub 10.100.0.0/16 with AzureFirewallSubnet 10.100.1.0/26 and GatewaySubnet 10.100.255.0/27.
  - Spokes 10.1.0.0/16 and 10.2.0.0/16.
  - UDR on the spoke subnets: 0.0.0.0/0 → next hop VirtualAppliance 10.100.1.4. Show why spoke-to-spoke traffic now crosses the firewall.
  - Explain "Use remote gateway" and "Allow gateway transit" on the peering.
  - Azure reserves 5 IPs per subnet: .0, .1, .2, .3 and the last.
- **Figures:**
  - **Fig 5.31:** Hub-spoke diagram with peering lines, firewall icon and UDR labels.
  - **Fig 5.32:** AWS↔Azure term-mapping table:
    - VPC↔VNet
    - SG↔NSG/ASG
    - NACL↔(NSG at subnet)
    - Route table↔UDR
    - TGW↔Virtual WAN hub
    - Direct Connect↔ExpressRoute
    - PrivateLink↔Private Link/Private Endpoint
    - NAT GW↔NAT Gateway
    - ALB↔Application Gateway
    - NLB↔Azure Load Balancer
- **Sub-topics:**
  - Service tags.
  - Private DNS zones.
  - Accelerated Networking (SR-IOV, FPGA-based SmartNIC, AccelNet) as a link back to router internals.
  - SNAT port exhaustion on Azure Load Balancer.
- **Trap:** Assuming NSG rules are evaluated in order of creation. They are evaluated by priority number; a lower number wins.

### 5.2.13 Hybrid connectivity: Direct Connect, ExpressRoute and VPN

- **Core idea:**
  - Private circuits (AWS Direct Connect, Azure ExpressRoute) connect on-premises to the cloud with BGP, bypassing the internet. IPsec VPN is the cheaper and slower alternative, or the backup.
  - Redundancy, BGP path preference and route limits are the design levers.
- **Analogy:** A private toll-free expressway from your office to the cloud campus, versus an armoured van (IPsec) on public roads.
- **Worked example:** ExpressRoute private peering.
  - Two /30s, primary 192.168.10.0/30 and secondary 192.168.10.4/30. Microsoft uses ASN 12076 (cite the docs).
  - Customer ASN 65010 advertises 172.16.0.0/16.
  - Show AS_PATH prepending on the secondary to make primary preferred inbound. Show local preference on-premises for outbound preference.
  - Discuss BFD on ExpressRoute and the route-advertisement limits per peering (cite current docs; do not hard-code numbers without checking).
  - Contrast with an AWS Direct Connect private VIF to a Virtual Private Gateway or Direct Connect Gateway, plus a Site-to-Site VPN backup (two tunnels per connection).
- **Figures:**
  - **Fig 5.33:** ExpressRoute topology.
    - Customer edge routers (CE1, CE2) → provider → Microsoft Enterprise Edge (MSEE) pair → VNet gateway.
    - Private peering and Microsoft peering shown as two coloured BGP sessions.
  - **Fig 5.34:** Decision flowchart: "VPN vs Direct Connect/ExpressRoute vs SD-WAN", with nodes on bandwidth, latency SLA, cost and compliance.
- **Trap:** Assuming one ExpressRoute circuit is redundant on its own. It has two links, but both may terminate in one peering location. Also: asymmetric routing when the VPN backup and ExpressRoute both advertise the same prefixes with no preference set.
- **Company Lens:** MSFT Cloud Network Engineer postings explicitly list VNet, ExpressRoute, Private Link, UDRs, VPN and NSGs, plus ISIS/BGP/MPLS for backbone roles. AMZN NDE asks VPC/Direct Connect and BGP troubleshooting scenarios.

### 5.2.14 Putting it together: the life of a request in the cloud

- **Core idea:** One narrative traces a user's HTTPS request end to end. It goes from DNS to anycast front door, edge LB, region backbone, spine-leaf fabric, VXLAN host overlay and hypervisor vSwitch to the VM socket, then back again.
- **Analogy:** A courier tracking page showing every hand-off.
- **Worked example:** A timeline table with about 12 rows, each listing hop, device, the header added or removed, and the lookup performed.
- **Figures:**
  - **Fig 5.35:** A two-page spread.
    - A horizontal journey from the phone (left) to the VM (right).
    - Each hop has an icon and a mini header-stack bar showing encapsulation growing and shrinking.
    - This is the signature figure of the chapter.

## 5.3 Hands-on labs

Lab tags: Must = 5-L1, 5-L3, 5-L8, 5-L9. Should = 5-L2, 5-L4, 5-L5, 5-L10, 5-L12. Optional = 5-L6, 5-L7, 5-L11. Full configs are in Appendix 5-A.

| # | Lab | Tooling | Time | Outcome / checkpoint |
|---|---|---|---|---|
| 5-L1 | **Build a 2-spine, 4-leaf eBGP fabric** | Containerlab + FRR images (or Arista cEOS / Nokia SR Linux free images) | 3 h | `show bgp summary` shows 2 sessions per leaf. `ip route` on a leaf shows `nexthop via ... weight 1` twice (ECMP). |
| 5-L2 | **Watch ECMP spread flows** | Same lab + `iperf3 -P 8` + `tcpdump` on spine interfaces | 1 h | The per-spine packet counts differ by flow. Then set `net.ipv4.fib_multipath_hash_policy=1` and observe the change. |
| 5-L3 | **Break the MTU** | Add VXLAN with Linux `ip link add vxlan10 type vxlan id 10 dstport 4789 local ... remote ...` | 1.5 h | `ping -M do -s 1472` fails across the overlay, and `-s 1422` works. Then fix it by raising the underlay MTU to 9000. |
| 5-L4 | **EVPN-VXLAN with FRR or SR Linux** | Containerlab topology file provided in the appendix | 3 h | `show bgp l2vpn evpn route type macip` shows Type-2 routes. Move a host and observe the MAC Mobility sequence number increment. |
| 5-L5 | **OpenFlow by hand** | Mininet `sudo mn --topo linear,3 --controller none --switch ovsk` + `ovs-ofctl` | 1.5 h | Students write the flows that make `pingall` succeed, then drop ICMP to h3 only. |
| 5-L6 | **Ryu L2 learning switch** | Mininet + Ryu `simple_switch_13.py`, modified | 2 h | Add a rule that mirrors h1's traffic to h3. Count the packet-ins before and after flows are installed. |
| 5-L7 | **P4 basic forwarding** | P4 tutorials VM (BMv2 `simple_switch_grpc`) `exercises/basic` | 3 h | Complete the `ipv4_lpm` table and actions; `h1 ping h2` works. Stretch: the `ecmp` exercise. |
| 5-L8 | **LPM in code** | C or Python | 2 h | Implement a binary trie with insert/lookup and test it against 10K random prefixes. Compare with a linear scan. Links to Pillar 1. |
| 5-L9 | **AWS free-tier VPC** | AWS Console + CLI (`aws ec2 create-vpc ...`), t2.micro/t3.micro within the free tier | 3 h | Public + private subnet, bastion, and VPC Flow Logs to CloudWatch. Break the NACL ephemeral rule and see the SSH hang. **Cost warning box:** NAT Gateway is NOT free; use a NAT instance or skip it, and delete everything after. |
| 5-L10 | **Azure VNet peering (free account credit)** | Azure CLI `az network vnet peering create` | 2 h | Hub-spoke with a UDR to a Linux VM acting as an NVA (`ip_forward=1`). Use `traceroute` to prove the path. |
| 5-L11 | **Anycast in a lab** | Containerlab: 3 "PoP" nodes announcing 192.0.2.1/32 via BGP to a 'transit' router | 1.5 h | Shut one PoP and observe client traceroutes switch. |
| 5-L12 | **Toy L4 load balancer** | Linux IPVS (`ipvsadm`) in DR mode with 2 backends in network namespaces | 2 h | Round-robin is seen with `curl` in a loop. Switch to `sh` (source hashing) and observe stickiness. |

## 5.4 Company-tag matrix (Pillar 5)

Depth: ● core / frequently asked, ◐ sometimes, ○ rarely or only for specific teams.

| Topic | CSCO | QCOM | GOOG | MSFT | AMZN | JNPR | ANET | NOK | AVGO |
|---|---|---|---|---|---|---|---|---|---|
| Spine-leaf / Clos sizing | ● | ○ | ● | ● | ● | ● | ● | ● | ◐ |
| ECMP and hashing | ● | ○ | ● | ● | ● | ● | ● | ● | ● |
| eBGP underlay / RFC 7938 | ◐ | ○ | ● | ● | ● | ● | ● | ● | ○ |
| VXLAN / EVPN | ● | ○ | ◐ | ● | ◐ | ● | ● | ● | ◐ |
| SDN / OpenFlow / P4 | ◐ | ○ | ● | ◐ | ◐ | ◐ | ◐ | ◐ | ● |
| RIB/FIB, TCAM, ASIC pipeline | ● | ◐ | ◐ | ◐ | ◐ | ● | ● | ● | ● |
| Load balancers / Maglev | ○ | ○ | ● | ● | ● | ○ | ○ | ○ | ○ |
| Anycast / CDN | ○ | ○ | ● | ● | ● | ○ | ○ | ○ | ○ |
| AWS VPC | ○ | ○ | ◐ (GCP VPC) | ◐ | ● | ○ | ◐ (CloudVision/cloud) | ○ | ○ |
| Azure VNet / ExpressRoute | ○ | ○ | ○ | ● | ○ | ○ | ○ | ○ | ○ |

Notes for the authors:

- Google network-engineer candidates on Reddit repeatedly recommend the *Jupiter Rising* paper. Include a "how to read this paper in 45 minutes" sidebar.
- Arista candidate reports mention EVPN/VXLAN with C and OS questions.
- MSFT postings explicitly list ExpressRoute, VNet, Private Link, UDR, NSG, with ISIS/BGP/MPLS.

## 5.5 Interview question bank (Pillar 5): 40 questions, each with a full in-book solution (see 0A.3)

1. [E] What is spine-leaf? Why is every leaf-to-leaf path the same length? (ANET, JNPR, GOOG)
2. [E] Define oversubscription. Compute it for 48 × 10G down and 6 × 40G up. *(Answer: 2:1.)* (ANET, MSFT)
3. [E] What is east-west versus north-south traffic? (all)
4. [M] Why do large data centres prefer eBGP over OSPF in the underlay? Give three reasons. (GOOG, MSFT, ANET)
5. [M] Two leaves share ASN 65001. What breaks, and what are two fixes? *(`allowas-in` or unique ASNs.)* (ANET, JNPR)
6. [M] What does ECMP hash on? Why not hash per packet? (all)
7. [H] You see 80% of traffic on one of four spines. List five possible causes. *(Elephant flow, polarisation, a missing `maximum-paths`, unequal AS_PATH, an LACP hash on a single-flow tunnel without UDP-source entropy.)* (GOOG, AMZN)
8. [H] Explain resilient or consistent hashing and why it matters when a spine fails. (GOOG, AVGO)
9. [E] What is VXLAN? Which UDP port does it use, and how many VNIs are there? (ANET, CSCO, NOK)
10. [M] Calculate the VXLAN overhead and the minimum underlay MTU for a 1,500-byte inner MTU. (ANET, JNPR)
11. [M] Why is the VXLAN outer UDP source port variable? (ANET, AVGO)
12. [M] What does EVPN add over flood-and-learn VXLAN? (ANET, JNPR, NOK, CSCO)
13. [H] Explain EVPN Route Types 2, 3 and 5 with an example of when each is sent. (JNPR, NOK, ANET)
14. [H] Symmetric versus asymmetric IRB: trade-offs in scale and configuration. (ANET, CSCO)
15. [H] A VM moves between racks and traffic blackholes for 30 seconds. What EVPN mechanisms should have prevented that? (ANET, MSFT)
16. [E] What is an anycast gateway? (ANET, CSCO)
17. [E] What is SDN? Name the northbound and southbound interfaces. (CSCO, GOOG)
18. [M] Describe an OpenFlow flow-table entry and what happens on a table miss. (CSCO, GOOG)
19. [M] What does P4 let you do that OpenFlow does not? (GOOG, AVGO)
20. [E] RIB versus FIB: what is the difference? (CSCO, JNPR, ANET)
21. [M] What is TCAM? Why is it used for LPM and ACLs, and what are its costs? (AVGO, CSCO, JNPR)
22. [H] Design a data structure for longest-prefix match supporting 1M IPv4 prefixes. Discuss memory and lookups per packet. (AVGO, ANET, JNPR, CSCO)
23. [H] Walk a packet through a switch ASIC from ingress port to egress. (AVGO, ANET, JNPR)
24. [M] What is a punt? What is CoPP and why is it needed? (CSCO, JNPR)
25. [M] Cut-through versus store-and-forward switching. When does cut-through fall back? (ANET, AVGO)
26. [H] What is TCP incast? How do deep buffers, ECN/DCTCP or pacing help? (GOOG, ANET)
27. [M] What are NSF/Graceful Restart and NSR? (JNPR, CSCO, NOK)
28. [E] L4 versus L7 load balancer. (AMZN, MSFT, GOOG)
29. [M] Explain DSR. Why does the backend need the VIP on its loopback? (GOOG, AMZN)
30. [H] Design a software L4 load balancer handling 10 Mpps that survives instance failure without breaking connections. *(ECMP, consistent hashing, connection table, Maglev.)* (GOOG, MSFT)
31. [M] How does anycast work? What happens to TCP if routing changes mid-flow? (GOOG, AMZN)
32. [M] How does a CDN choose which edge serves you? (GOOG, AMZN, MSFT)
33. [E] SG versus NACL in AWS. (AMZN)
34. [M] A private-subnet EC2 instance cannot reach the internet. List the checks in order. (AMZN)
35. [M] Is VPC peering transitive? How do you connect 50 VPCs? (AMZN, MSFT)
36. [M] Azure: what is a UDR? Give a scenario that needs one. (MSFT)
37. [H] Design ExpressRoute with VPN failover. How do you ensure symmetric routing? (MSFT)
38. [H] On-premises advertises 10.0.0.0/8 over ExpressRoute while an Azure VNet uses 10.1.0.0/16. What happens and how do you fix it? (MSFT)
39. [X] Explain how Azure or AWS implement the VPC data plane: host-based SDN, SmartNICs, encapsulation. (MSFT, AMZN)
40. [X] Compare the Google Jupiter approach (centralised control, merchant silicon, Clos, later optical circuit switches) with a traditional chassis-based DC. (GOOG)

## 5.6 Trap boxes (Pillar 5 consolidated)

1. ECMP balances *flows*, not packets.
2. VXLAN MTU: "ping works, HTTPS hangs" is the classic symptom.
3. VPC peering is non-transitive, and overlapping CIDRs cannot peer.
4. SGs are stateful, allow-only and attach to ENIs. NACLs are stateless, ordered, use allow/deny and attach to subnets.
5. Anycast is BGP-nearest, not geographically nearest.
6. TCAM holds FIB and ACL entries. A port-range ACL may consume many entries.
7. The RIB may contain several routes to a prefix; the FIB holds the winner(s) only.
8. An ExpressRoute circuit is not geo-redundant on its own.
9. Hash polarisation happens when the same hash seed is used at every tier.
10. The AWS subnet reservation is 5 IPs, not 2.
11. NSG priority: lower number = higher priority.
12. In SDN, a controller outage need not stop forwarding (flows installed proactively), but reactive designs will stall.

## 5.7 Cheat-sheet contents (one double-sided A4 page)

- **Side A (fabric):**
  - Clos formula box: max servers = spine_ports × leaf_down_ports; oversubscription = down_bw / up_bw.
  - ECMP hash inputs.
  - RFC 7938 ASN plan.
  - BFD timers.
  - VXLAN header diagram (8 bytes, VNI 24 bits, UDP 4789); overhead 50 bytes (IPv4) / 70 bytes (IPv6).
  - EVPN route types 1–5 table.
  - RIB→FIB→adjacency flow.
  - TCAM versus SRAM.
  - ASIC pipeline in 10 boxes.
- **Side B (cloud):**
  - AWS/Azure term-mapping table.
  - VPC reserved IPs.
  - SG/NACL table.
  - Public versus private subnet rule.
  - Peering versus TGW versus PrivateLink.
  - ExpressRoute peering types.
  - Direct Connect VIF types (private, public, transit).
  - Anycast/CDN formula.
  - The LB family (ALB, NLB, GWLB; App Gateway, Azure LB, Front Door).
  - "First five checks when the cloud VM cannot connect".

## 5.8 Mini-project (Pillar 5): "Pocket Hyperscaler"

- **Brief:** Build, document and break a small EVPN-VXLAN data centre with a cloud-like edge.
  1. Containerlab topology: 2 spines, 4 leaves (FRR or SR Linux), 8 Linux hosts in 2 tenants (VRF-A, VRF-B).
  2. eBGP unnumbered underlay, EVPN overlay with symmetric IRB and an anycast gateway.
  3. An IPVS DSR load balancer in front of 3 web backends in tenant A. The VIP is announced by anycast from two border leaves.
  4. A Python script (forward reference to Pillar 10) that pulls `show bgp evpn` JSON and draws the MAC-to-VTEP table.
  5. **Chaos test:** fail a spine, a border leaf and a backend. Measure the loss with `ping -i 0.01` and report recovery times in a table.
- **Deliverables:** GitHub repo, topology diagram, a 2-page write-up and a 3-minute demo video. A rubric is given in the appendix.
- **Interview pay-off:** It gives students a concrete "tell me about a project" story for ANET, JNPR, NOK, MSFT and GOOG.

## 5.9 Sources (Pillar 5)

Researched during planning:

- Microsoft Senior Cloud Network Engineer posting (repost): https://jobs.anitab.org/companies/microsoft-2/jobs/92973050-senior-cloud-network-engineer
- Microsoft Cloud Network Engineer II posting (repost): https://jobs.anitab.org/companies/microsoft/jobs/60499379-cloud-network-engineer-ii
- Microsoft Cloud Network Engineer (careers site): https://jobs.careers.microsoft.com/us/en/job/1809940/Cloud-Network-Engineer
- Microsoft Senior Cloud Network Engineer (Taro): https://jointaro.com/jobs/microsoft/senior-cloud-network-engineer-c14e7b0d
- Amazon NDE interview questions (Glassdoor): https://static.glassdoor.de/Interview/Amazon-Network-Development-Engineer-Interview-Questions-EI_IE6036.0,6_KO7,35_IP3.htm
- Amazon NDE experiences (Taro):
  - https://www.jointaro.com/interviews/companies/amazon/work-experiences/network-development-engineer-dublin-dublin-may-18-2025-4-91d2d903/
  - https://www.jointaro.com/interviews/companies/amazon/experiences/network-development-engineer-austin-tx-february-1-2025-no-offer-positive-67408af9
- Google Network Engineer interview reports (Glassdoor): https://www.glassdoor.co.in/Interview/Google-Network-Engineer-Interview-Questions-EI_IE9079.0,6_KO7,23.htm
- Reddit r/networking thread on the Google Network Implementation Engineer role (mirror): https://redlib.hyperreal.coffee/r/networking/comments/1kihmrn/google_network_implementation_engineer
- Google Jupiter coverage:
  - https://www.datacenterknowledge.com/networking/custom-google-data-center-network-pushes-1-petabit-per-second
  - https://techcrunch.com/2015/06/17/google-pulls-back-curtain-on-its-data-center-networking-setup/amp/
- Arista interview guides and experiences:
  - https://www.interviewquery.com/interview-guides/arista-networks-software-engineer
  - https://leetcode.com/discuss/interview-experience/6078309/Arista-Networks-or-SWE-1-or-India-or-Accepted/
  - https://medium.com/@omnikam0404/arista-networks-on-campus-interview-experience-pict-pune-57a4d7f79c27

Primary references for authors to cite in the chapter (standards and papers; verify current versions before print):

- RFC 7938 (BGP in large-scale data centres): https://www.rfc-editor.org/rfc/rfc7938
- RFC 7348 (VXLAN): https://www.rfc-editor.org/rfc/rfc7348
- RFC 7432 (BGP MPLS-based EVPN): https://www.rfc-editor.org/rfc/rfc7432
- RFC 8365 (EVPN as an NVO solution): https://www.rfc-editor.org/rfc/rfc8365
- RFC 9135 (integrated routing and bridging in EVPN): https://www.rfc-editor.org/rfc/rfc9135
- RFC 8950 (IPv4 NLRI with an IPv6 next hop): https://www.rfc-editor.org/rfc/rfc8950
- Singh et al., "Jupiter Rising", SIGCOMM 2015: https://research.google/pubs/jupiter-rising-a-decade-of-clos-topologies-and-centralized-control-in-googles-datacenter-network/
- Eisenbud et al., "Maglev", NSDI 2016: https://research.google/pubs/maglev-a-fast-and-reliable-software-network-load-balancer/
- P4 language specification and tutorials: https://p4.org/specs/ and https://github.com/p4lang/tutorials
- OpenFlow switch specification (ONF): https://opennetworking.org/software-defined-standards/specifications/
- AWS VPC documentation: https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html
- AWS Direct Connect documentation: https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html
- Azure Virtual Network documentation: https://learn.microsoft.com/azure/virtual-network/virtual-networks-overview
- Azure ExpressRoute documentation: https://learn.microsoft.com/azure/expressroute/expressroute-introduction
- Containerlab: https://containerlab.dev/
- Mininet: http://mininet.org/
- FRRouting documentation: https://docs.frrouting.org/

## 5.10 End-of-chapter pack (per 0A.4)

- Short notes, ordered as section 5.2.x.
- One-page revision sheet, built from 5.7.
- 60 flashcards.
- Solutions to all 40 questions in 5.5, in the five-part format.
- Five extended whiteboard problems (listed in 0A.4).
- A 20-question self-test with an answer key.

---


# PILLAR 6: Wireless and Cellular Networking

## 6.0 Chapter header

- **Title:** *Chapter 6: Talking Through Air: Wi-Fi from Radio to Handshake, and the Road from LTE to 5G*
- **One-line promise:** By the end you can read a Wi-Fi packet capture frame by frame (beacon → probe → auth → assoc → EAPOL 1–4 → data), explain CSMA/CA timing with numbers, say what OFDMA, MU-MIMO and MLO change in Wi-Fi 6/7, and sketch the LTE/5G architecture and attach procedure.
- **Prerequisites:**
  - Pillar 3: the layers, Ethernet framing, ARP/DHCP.
  - Pillar 9: symmetric keys, HMAC and AES basics.
  - Pillar 12: decibels, frequency and bandwidth, the Shannon formula, modulation basics (a quick recap box is included).
  - Pillar 2 for the C bit-field parsing lab.
- **Estimated pages:** 95–110, with about 40 figures.
- **Must-path estimate:** ≈ 4.5 study days for the Must sections only (see the tag table in 0A.1). The book keeps all sections in full.
- **Weeks (full read):** 3.5 weeks at about 10 hours per week.
  - Week 1: RF and PHY basics, plus 802.11 architecture.
  - Week 2: the MAC (CSMA/CA, frames, power save) and the connection lifecycle.
  - Week 3: security (WPA2/WPA3), Wi-Fi 6/6E/7, roaming.
  - Half week: LTE/5G.

## 6.1 Learning objectives

1. Convert between mW and dBm, compute the free-space path loss and a link budget, and explain SNR versus data rate (MCS).
2. Explain OFDM (subcarriers, orthogonality, cyclic prefix, guard interval), QAM orders (BPSK up to 4096-QAM) and spatial streams/MIMO.
3. Describe the 802.11 architecture: STA, AP, BSS, ESS, BSSID, SSID, the DS, and infrastructure versus IBSS versus mesh (802.11s).
4. Explain DCF/CSMA-CA with timing (SIFS, DIFS, slot time, contention window, binary exponential back-off), and RTS/CTS and the NAV for the hidden-node problem. Contrast this with CSMA/CD.
5. Decode the 802.11 MAC header: Frame Control bits, Duration/ID, the four address fields and the To DS/From DS truth table, Sequence Control, QoS Control, and the FCS.
6. List the management, control and data frame subtypes, and trace the full connection lifecycle in Wireshark.
7. Explain EDCA access categories (AC_VO, AC_VI, AC_BE, AC_BK) with AIFSN/CWmin/CWmax/TXOP; block ack; A-MSDU and A-MPDU aggregation.
8. Derive the PTK in the WPA2 4-way handshake (PMK, ANonce, SNonce, MACs → PTK = KCK | KEK | TK), deliver the GTK and explain the replay counter. Explain what KRACK exploited, and what WPA3-SAE, PMF (802.11w) and OWE fix.
9. Compare 802.1X/EAP (EAP-TLS, PEAP) with PSK. Name the roles of supplicant, authenticator and authentication server (RADIUS).
10. Explain Wi-Fi 6/6E (802.11ax) features: OFDMA resource units, UL/DL MU-MIMO, trigger frames, BSS colouring, TWT, 1024-QAM, and 6 GHz. Explain Wi-Fi 7 (802.11be) features: 320 MHz, 4096-QAM, MLO, multi-RU and puncturing.
11. Explain roaming and fast transition (802.11r FT, 802.11k neighbour reports, 802.11v BSS transition), and power save (PS-Poll, TIM/DTIM, U-APSD, TWT).
12. Sketch the LTE EPS architecture (UE, eNodeB, MME, S-GW, P-GW, HSS, PCRF) and the 5G SA architecture (gNB, AMF, SMF, UPF, AUSF, UDM, NRF; service-based). Walk the attach/registration and PDU session setup at block level. Explain bearers/QoS flows, and handover at a high level.
13. Relate firmware concepts (host-firmware split, FullMAC versus SoftMAC, mac80211/cfg80211/nl80211) to what Qualcomm and Broadcom WLAN teams build.

## 6.2 Section-by-section outline

### 6.2.1 RF in one sitting: decibels, link budgets and Shannon

- **Core idea:** Radio links are governed by power ratios measured in dB, by loss over distance, and by noise. Shannon's limit C = B log2(1 + SNR) explains why wider channels and better SNR both raise throughput.
- **Analogy:** Shouting across a hall. Louder speech (Tx power), a quieter room (low noise floor) and a shorter distance (less path loss) all help. A wider "vocal range" (bandwidth) lets you say more per second.
- **Worked example:** Link budget.
  - Tx 20 dBm (100 mW) + antenna gain 3 dBi.
  - FSPL at 5.5 GHz over 30 m: FSPL(dB) = 20log10(d) + 20log10(f) − 147.55 with d in metres and f in Hz, which gives ≈ 76.8 dB.
  - Wall loss 12 dB. Rx antenna 3 dBi.
  - Received power: 20 + 3 − 76.8 − 12 + 3 ≈ −62.8 dBm.
  - With a noise floor of −92 dBm, SNR ≈ 29 dB.
  - Look up the MCS table (illustrative values; cite the standard table): roughly 256-QAM 3/4 territory. Explain why 1024-QAM (≈35 dB) needs to be closer.
- **Figures:**
  - **Fig 6.1:** dBm ruler. A horizontal log scale from −100 dBm to +30 dBm with landmarks: "noise floor", "good Wi-Fi −65", "AP Tx 20", "1 W = 30 dBm".
  - **Fig 6.2:** Link-budget waterfall chart. Bars going up and down for Tx, gains and losses, ending at Rx power, with a dashed line for sensitivity.
  - **Fig 6.3:** Channel maps.
    - 2.4 GHz: channels 1, 6 and 11 non-overlapping, drawn as overlapping humps.
    - 5 GHz: UNII bands with DFS highlighted.
    - 6 GHz: 59 × 20 MHz channels, showing 14 × 80 MHz and 7 × 160 MHz blocks, and 320 MHz for Wi-Fi 7.
    - Note that Indian 6 GHz regulation status should be checked at print time.
- **Trap:** "+3 dB means 3× the power." It means 2×; +10 dB = 10×. Also: dBm is absolute, while dB and dBi are relative.

### 6.2.2 PHY essentials: OFDM, QAM and MIMO

- **Core idea:**
  - OFDM splits a wide channel into many narrow orthogonal subcarriers. The peaks of each fall on the nulls of the others, so they don't interfere.
  - A cyclic prefix (guard interval) absorbs multipath echoes.
  - QAM packs bits per symbol.
  - MIMO uses multiple antennas for spatial streams.
- **Analogy:** A multi-lane motorway (subcarriers) with lanes spaced exactly so the cars never sideswipe. QAM is how many passengers fit per car; MIMO is building a second, stacked motorway.
- **Worked example:** Compute an 802.11ax data rate.
  - 80 MHz has 980 data subcarriers (996-tone RU minus pilots; cite the exact figure from the spec).
  - 1024-QAM = 10 bits per subcarrier, coding rate 5/6.
  - Symbol duration 12.8 µs + GI 0.8 µs = 13.6 µs.
  - Per stream: 980 × 10 × 5/6 / 13.6 µs ≈ 600.5 Mb/s. Two spatial streams give ≈ 1201 Mb/s, matching the familiar "1.2 Gb/s" figure.
  - Then repeat with 4096-QAM and 320 MHz for Wi-Fi 7 to show where the marketing numbers come from.
- **Figures:**
  - **Fig 6.4:** Overlapping sinc-shaped subcarrier spectra, with the orthogonality points marked by dots on the zero crossings.
  - **Fig 6.5:** Constellation diagrams for BPSK, QPSK, 16-QAM and 64-QAM, plus a 1024-QAM thumbnail. "Bits/symbol" is written below each.
  - **Fig 6.6:** 2×2 MIMO diagram: two Tx antennas and two Rx antennas with four channel paths h11, h12, h21, h22 and the matrix H.
  - **Fig 6.7:** Cyclic prefix. A symbol whose tail is copied to its front, with a delayed echo landing inside the CP.
- **Trap:** Confusing SU-MIMO (multiple streams to one client) with MU-MIMO (streams to different clients at once). Confusing OFDM (one user per symbol, before ax) with OFDMA (multiple users share one symbol via RUs).
- **Company Lens:** QCOM interviewers have asked "explain OFDMA and how subcarrier orthogonality is maintained" (Glassdoor report).

### 6.2.3 802.11 architecture and the family tree

- **Core idea:** Wi-Fi organises stations into BSSs around an AP. Multiple BSSs on one distribution system form an ESS with one SSID. The standard has evolved through amendments, from b/a/g to n (Wi-Fi 4), ac (5), ax (6/6E) and be (7).
- **Analogy:** An AP is a classroom teacher (BSS). The school (ESS) shares a name (SSID). Each classroom has a room number (the BSSID, the AP radio's MAC).
- **Worked example:**
  - A home with a dual-band AP broadcasting "Sharma_Home" has two BSSIDs (2.4 and 5 GHz), one SSID and one ESS.
  - A campus with 200 APs × 3 radios × 2 SSIDs has 1,200 BSSIDs.
  - Explain why beacon overhead grows with SSID count. A rule of thumb: keep it to 3 SSIDs or fewer.
- **Figures:**
  - **Fig 6.8:** Architecture diagram. Two BSS bubbles (AP1, AP2) joined by a wired DS (switch), with STAs inside, labelled ESS "CampusNet".
  - **Fig 6.9:** Timeline table (the generations table): Wi-Fi 4/5/6/6E/7 against IEEE name, year, bands, maximum width, maximum QAM, maximum streams, key MAC/PHY feature, and the theoretical maximum rate.
  - **Fig 6.10:** Split-MAC architecture. AP to WLC over CAPWAP/control channel, versus cloud-managed (Mist/Meraki) as a simple diagram.

### 6.2.4 The MAC: CSMA/CA and DCF timing

- **Core idea:**
  - Radios cannot detect collisions while transmitting (half-duplex; their own signal drowns the receiver). So 802.11 *avoids* collisions instead.
  - A station senses the medium, waits DIFS plus a random back-off, then transmits. Every unicast frame needs an ACK after SIFS. On failure the contention window doubles.
- **Analogy:** A polite group conversation. Wait until it's quiet, count to a random number, then speak. If two people start together, nobody hears an "OK", so each picks a bigger random number next time.
- **Worked example:** 802.11a/g/n/ac OFDM timing in 5 GHz.
  - Slot 9 µs, SIFS 16 µs, DIFS = SIFS + 2 × slot = 34 µs.
  - CWmin = 15, CWmax = 1023.
  - Station A draws back-off 7 and station B draws 4. B's counter hits 0 first after 4 × 9 = 36 µs. B transmits; A freezes at 3.
  - After B's frame, SIFS, and the ACK, A waits DIFS and counts the remaining 3 slots, then transmits.
  - Now a collision: both draw 5. There is no ACK, so CW doubles to 31 and they redraw.
  - Finally compute the efficiency of a single 1,500-byte frame at 54 Mb/s, including the preamble (20 µs), DIFS, average back-off (7.5 × 9), SIFS and the ACK. This gives ≈ 60–70%. It motivates aggregation in 802.11n and later.
- **Figures:**
  - **Fig 6.11:** Timing diagram (the hero figure).
    - Horizontal time axis with lanes for STA A, STA B and the medium.
    - Blocks for DIFS, back-off slots (numbered countdown), DATA, SIFS and ACK.
    - Frozen back-off is drawn with a hatched pattern.
  - **Fig 6.12:** Hidden-node problem. A and C both in range of the AP but not of each other, with range circles drawn. Then the RTS/CTS solution, with the NAV bars set on A and C.
  - **Fig 6.13:** Exposed-node problem, as a small inset.
  - **Fig 6.14:** CW growth staircase graph. Retry 0..6 on the x-axis, CW = 15, 31, 63 ... 1023 on the y-axis.
- **Sub-topics:**
  - Physical carrier sense (CCA) versus virtual carrier sense (NAV, set from the Duration field).
  - PCF (legacy) and HCF.
  - Why the ACK is needed: no collision detection, and a lossy medium.
  - EIFS.
- **Trap:** "Wi-Fi uses CSMA/CD." It uses CSMA/CA. Also: "RTS/CTS is always on." It is threshold-based, usually off by default for small frames.
- **Company Lens:** CSMA/CA versus CD and DCF are core QCOM/AVGO WLAN screening questions.

### 6.2.5 The 802.11 frame, bit by bit

- **Core idea:**
  - The 802.11 MAC header is up to 4 addresses long. Frame Control says what the frame is and which direction it travels relative to the DS.
  - The To DS/From DS bits decide what Address 1–4 mean.
- **Analogy:** An envelope with four address lines: final recipient, sender, the relay that received it, and the relay that will forward it. Two tick-boxes on the envelope say which lines are relays.
- **Worked example:**
  - Decode a real hex dump from a capture (supplied in the book's companion files). Frame Control `0x0841`, read little-endian:
    - Protocol version 0, type 2 (Data), subtype 0.
    - Flags: To DS = 1, Protected = 1.
  - Fill in: Addr1 = BSSID (receiver), Addr2 = STA (transmitter), Addr3 = destination MAC.
  - Then decode a beacon (`0x8000`): Type 0, Subtype 8. Parse its tagged parameters: SSID (tag 0), Supported Rates (1), DS Parameter (3), TIM (5), RSN IE (48), HT/VHT/HE capabilities.
- **Figures:**
  - **Fig 6.15:** MAC header layout.
    - Frame Control (2) | Duration/ID (2) | Addr1 (6) | Addr2 (6) | Addr3 (6) | Seq Ctrl (2) | Addr4 (6) | QoS Ctrl (2) | HT Ctrl (4) | Body | FCS (4).
    - Field widths in bytes, and an exploded view of Frame Control's 16 bits: version, type, subtype, ToDS, FromDS, MoreFrag, Retry, PwrMgt, MoreData, Protected, +HTC/Order.
  - **Fig 6.16:** To DS/From DS truth table (00, 01, 10, 11) with the meaning of Addr1–Addr4 in each case and a scenario icon (IBSS, from AP, to AP, WDS/mesh).
  - **Fig 6.17:** Frame-type tree:
    - Management: beacon, probe req/resp, auth, deauth, assoc req/resp, reassoc, disassoc, action.
    - Control: RTS, CTS, ACK, Block Ack/BAR, PS-Poll, Trigger (ax).
    - Data: Data, QoS Data, Null, QoS Null.
- **Lab tie-in:** Students write a C parser for the radiotap header and the 802.11 header, using bit-fields and masks (see Lab 6-L4).
- **Trap:** Forgetting that Frame Control is little-endian on air, and that the type/subtype bit ordering trips up hand-decoding. Also: "Addr3 is always the destination." It depends on the DS bits.

### 6.2.6 The connection lifecycle: scan, authenticate, associate, 4-way, DHCP

- **Core idea:**
  - A client discovers networks: passive scanning listens for beacons; active scanning sends probes.
  - It then performs 802.11 Open System "authentication" (a formality in WPA2), then association, which negotiates capabilities and assigns an AID.
  - In RSN networks the 802.1X/EAP stage (enterprise) or the PMK from PSK (personal) comes next, followed by the 4-way handshake to derive keys.
  - Only then do DHCP and ARP run.
- **Analogy:** Arriving at a hotel. You read the signboards (beacons) or ask at reception (probe). You show you're a guest (auth), get a room number (association ID), collect a key card (4-way handshake), and only then go to the restaurant (DHCP/IP).
- **Worked example:** Annotated Wireshark trace of about 15 frames, with a numbered table: time, source, destination, frame, key fields, and "why it matters".
  - Beacon (SSID, RSN IE: AKM = PSK, cipher = CCMP)
  - Probe Request/Response
  - Auth (seq 1, 2; algorithm 0 = open)
  - Assoc Req (listen interval, supported rates, HT/VHT/HE capabilities, RSN IE)
  - Assoc Resp (status 0, AID 1)
  - EAPOL 1/4 (ANonce)
  - EAPOL 2/4 (SNonce + MIC)
  - EAPOL 3/4 (GTK encrypted, MIC, install flag)
  - EAPOL 4/4 (ACK)
  - First QoS Data (protected)
  - DHCP Discover/Offer/Request/ACK (inside encrypted frames, visible only when decrypted with the PSK in Wireshark)
  - ARP for the gateway
- **Figures:**
  - **Fig 6.18:** Swim-lane sequence diagram STA ↔ AP (↔ RADIUS for enterprise). Phases are colour-banded: Discovery, 802.11 Auth, Association, 802.1X/EAP (optional), 4-Way Handshake, IP Configuration.
  - **Fig 6.19:** The 802.11 state machine. State 1 (unauth, unassoc) → State 2 (auth, unassoc) → State 3 (auth, assoc, 802.1X port blocked) → State 4 (port authorised). Deauth and disassoc arrows go back.
- **Trap:** Calling 802.11 open "authentication" a security step. In RSN it is a legacy formality; the real authentication is 802.1X/SAE plus the 4-way handshake. Also: Shared Key auth (WEP) is deprecated and leaks keystream.
- **Company Lens:** "How does a STA associate with an AP?" and "What is the 4-way handshake?" recur in QCOM Hyderabad and Bengaluru reports.

### 6.2.7 Security: WPA2, 802.1X, WPA3, PMF

- **Core idea:**
  - WPA2 derives a per-session PTK from the PMK and two nonces without ever sending the PMK over the air.
  - The GTK protects broadcast and multicast.
  - WPA3 replaces PSK's offline-dictionary-attackable handshake with SAE (Dragonfly), gaining forward secrecy, and makes PMF mandatory.
- **Analogy:** Two people who share a secret recipe (PMK). Each brings a fresh random spice (nonce). They mix the recipe with both spices to make today's dish (PTK). An eavesdropper who sees the spices but not the recipe cannot make the dish.
- **Worked example:**
  - **(A) Key hierarchy.**
    - For PSK: PMK = PBKDF2-HMAC-SHA1(passphrase, SSID, 4096 iterations, 256 bits).
    - PTK = PRF(PMK, "Pairwise key expansion", min(AA, SPA) ‖ max(AA, SPA) ‖ min(ANonce, SNonce) ‖ max(ANonce, SNonce)).
    - For CCMP, split the 384-bit PTK into KCK (128) | KEK (128) | TK (128).
    - Compute with Python `hashlib.pbkdf2_hmac` for SSID "IITLab" and passphrase "packet123". Show the first 8 bytes of the PMK.
    - Then show the MIC is computed with the KCK over EAPOL message 2.
  - **(B) Why the attacker can brute-force WPA2-PSK.** Capture messages 1 and 2, then guess passphrases offline and check the MIC. Show why SAE prevents this: each guess requires an online interaction.
  - **(C) KRACK in one paragraph.** Retransmitted message 3 causes reinstallation of the TK with a reset nonce/packet number, which leads to keystream reuse.
- **Figures:**
  - **Fig 6.20:** Key hierarchy tree. Passphrase/EAP → PMK → PTK (KCK, KEK, TK) and GMK → GTK. Colours mark what is sent over the air (nonces, encrypted GTK) and what is never sent (PMK).
  - **Fig 6.21:** 4-way handshake ladder diagram. Fields shown on each message: ANonce, SNonce, MIC, Replay Counter, RSN IE, encrypted GTK, Install bit, Ack bit.
  - **Fig 6.22:** 802.1X triad: supplicant (laptop) ↔ authenticator (AP, controlled/uncontrolled port) ↔ authentication server (RADIUS), with EAPOL on the left leg and RADIUS on the right leg.
  - **Fig 6.23:** Comparison table WEP | WPA | WPA2 | WPA3 with rows: cipher (RC4/TKIP/CCMP/GCMP-256), key management, PMF, forward secrecy, status.
- **Sub-topics:**
  - PMKID caching.
  - OWE (Enhanced Open).
  - WPA3 transition mode and its downgrade risk.
  - The deauth attack and how PMF (802.11w) protects management frames.
- **Trap:** "The PSK is sent during the handshake." It never is. Also: "WPA3 makes weak passwords safe." It stops offline dictionary attacks, but online guessing is still possible.

### 6.2.8 QoS, aggregation and power save

- **Core idea:**
  - EDCA gives voice and video shorter waits and smaller windows, so they statistically win the medium.
  - A-MPDU/A-MSDU aggregation and Block Ack amortise overhead.
  - Power save lets clients sleep, with the AP buffering frames and advertising them in the TIM.
- **Analogy:**
  - EDCA: priority boarding at the airport.
  - Aggregation: a bus instead of many cars.
  - Power save: a hotel that holds your mail and puts a flag on the noticeboard.
- **Worked example:**
  - EDCA table: AC_VO AIFSN 2, CWmin 3, CWmax 7; AC_BE AIFSN 3, CWmin 15, CWmax 1023 (default STA parameters; cite the standard).
  - Compute the average initial wait: SIFS + AIFSN × slot + CWmin/2 × slot.
    - VO: 16 + 18 + 13.5 = 47.5 µs.
    - BE: 16 + 27 + 67.5 = 110.5 µs.
  - DSCP → UP → AC mapping example: DSCP 46 (EF) → UP 6 → AC_VO.
  - Then aggregation: 64 MPDUs in one A-MPDU with one Block Ack, against 64 individual ACKs. Compute the airtime saved.
  - DTIM example: beacon interval 102.4 ms, DTIM period 3, so clients wake every ≈307 ms for multicast.
- **Figures:**
  - **Fig 6.24:** Four AC queues inside one STA, each with its own back-off timer and AIFS bar, plus an "internal collision" resolution arrow.
  - **Fig 6.25:** A-MSDU versus A-MPDU structure diagram, showing where the MAC header and FCS sit in each.
  - **Fig 6.26:** Power-save timeline with beacons and TIM bits, the client waking, PS-Poll and data. TWT is drawn as scheduled wake windows.

### 6.2.9 Wi-Fi 6/6E and Wi-Fi 7

- **Core idea:**
  - 802.11ax turns Wi-Fi from "one talker at a time" into scheduled multi-user access. OFDMA resource units are allocated via trigger frames; UL MU-MIMO; BSS colouring cuts needless deferral; TWT saves power; 6 GHz adds clean spectrum.
  - 802.11be adds 320 MHz, 4096-QAM, puncturing and Multi-Link Operation across bands.
- **Analogy:**
  - OFDMA: a lorry (one transmission) with many small compartments for different customers, instead of one parcel per lorry.
  - BSS colouring: a coloured shirt that tells you whether chatter is from your own classroom or next door's.
  - MLO: a delivery van allowed to use the motorway, the expressway and the service road at the same time.
- **Worked example:**
  - **(A) RU allocation in 20 MHz (802.11ax).** Possible RUs are 9 × 26-tone, or 4 × 52-tone (plus a 26), or 2 × 106-tone (plus a 26), or 1 × 242. With nine IoT sensors each sending 100-byte frames, OFDMA serves all nine in one PPDU versus nine separate contentions. Do a rough airtime comparison with stated assumptions.
  - **(B) Trigger-based uplink sequence.** AP sends a Trigger frame → STAs send HE TB PPDUs on their assigned RUs → AP sends a Multi-STA Block Ack.
  - **(C) BSS colouring.** An OBSS frame arrives with a different colour and an RSSI of −78 dBm, below the OBSS-PD threshold of −72. The STA ignores it and continues back-off (spatial reuse).
  - **(D) MLO.** An MLD with links on 5 GHz and 6 GHz. Contrast STR, NSTR and EMLSR modes in one table. State the trade-off: throughput and latency against hardware complexity.
- **Figures:**
  - **Fig 6.27:** Time-frequency grid ("Tetris" figure). Left: OFDM, with one colour per transmission across the full width. Right: OFDMA, with coloured RU blocks for STA1–4 inside one PPDU.
  - **Fig 6.28:** 20/40/80 MHz RU tree. A hierarchical breakdown of 26/52/106/242/484/996-tone RUs.
  - **Fig 6.29:** Trigger-frame sequence ladder: AP, STA1, STA2, STA3.
  - **Fig 6.30:** BSS colouring. Two overlapping cells coloured blue and green, with the threshold explanation.
  - **Fig 6.31:** MLO diagram. AP MLD and non-AP MLD with three affiliated links (2.4/5/6), with one MAC address (MLD MAC) above and per-link MACs below.
  - **Fig 6.32:** Wi-Fi 6 versus 6E versus 7 feature checklist table.
- **Trap:** "OFDMA increases peak throughput." It mainly improves *efficiency and latency* for many small flows; peak single-client rate comes from width, QAM and streams. Also: "Wi-Fi 6E is a new standard." It is 802.11ax extended to 6 GHz.
- **Company Lens:** Qualcomm WLAN postings list MU-MIMO, OFDMA, TWT and rate control. Expect "how would firmware schedule RUs?" and "what is rate adaptation (Minstrel-style)?"

### 6.2.10 Roaming, mobility and enterprise design

- **Core idea:** The client decides when to roam; the AP and network can only assist. 802.11k provides neighbour lists, 802.11v suggests a move, and 802.11r pre-derives keys so the roam skips the full 802.1X exchange and stays under about 50 ms for voice.
- **Analogy:** Changing trains at a junction. 802.11k is the platform map, 802.11v is the station master suggesting a platform, and 802.11r is a through-ticket so you don't queue at the ticket counter again.
- **Worked example:**
  - Full 802.1X re-authentication (≈ 4 RADIUS round trips at 20 ms plus processing) is about 200–400 ms.
  - FT over-the-air: FT Auth (2 frames) + Reassoc (2 frames), about 20 ms. Present these as illustrative and cite them as such.
  - Also: the sticky-client problem, and setting the minimum RSSI / BSS transition threshold.
  - Channel planning for a 3-floor hostel, as a 3D grid exercise: 5 GHz on 36/40/44/48/149/153/157/161 at 20 MHz, and why 80 MHz is a poor choice in dense deployments.
- **Figures:**
  - **Fig 6.33:** Roaming timeline comparison. Three horizontal bars: "full EAP", "PMK caching (OKC)" and "802.11r FT", with millisecond annotations.
  - **Fig 6.34:** Floor-plan heat map, a stylised RSSI gradient with AP icons and a "roam boundary" contour at −67 dBm.

### 6.2.11 Linux and firmware view of Wi-Fi

- **Core idea:**
  - In Linux, user space talks nl80211 to cfg80211.
  - mac80211 implements the SoftMAC; drivers such as ath10k, ath11k, ath12k (Qualcomm) and brcmfmac (Broadcom FullMAC) talk to the chip firmware.
  - Firmware handles time-critical MAC functions such as ACK timing, retries, rate control and OFDMA scheduling.
- **Analogy:** A restaurant. The owner (hostapd/wpa_supplicant) writes policy, the manager (cfg80211/mac80211) runs the floor, and the kitchen (firmware) cooks in real time.
- **Worked example:**
  - Run `iw dev`, `iw phy phy0 info` (supported bands, HE capabilities) and `iw dev wlan0 station dump` (tx bitrate, MCS, signal).
  - Map each output line to concepts from this chapter.
  - Put the card in monitor mode with `iw dev wlan0 set type monitor` / `airmon-ng`, after checking that the card supports it.
- **Figures:**
  - **Fig 6.35:** Linux wireless stack.
    - User space: wpa_supplicant, hostapd, iw, NetworkManager.
    - nl80211 → cfg80211 → mac80211 → driver (ath11k) → bus (PCIe/SDIO/USB) → firmware on the SoC → radio.
    - A side branch for FullMAC (brcmfmac), which bypasses mac80211.
  - **Fig 6.36:** Host-firmware message flow: host command (WMI) → firmware event → host. Labelled generically, with a note that Qualcomm's interface is called WMI in open-source ath drivers.
- **Company Lens:**
  - QCOM and AVGO WLAN firmware roles combine this chapter with Pillar 7: interrupts, ISRs versus bottom halves, DMA rings, memory constraints, C bit manipulation.
  - Glassdoor reports stress "bit manipulation and memory management" and C storage classes.

### 6.2.12 Cellular in a chapter: from LTE to 5G

- **Core idea:**
  - Cellular networks separate the radio access network from the core.
  - LTE's EPC (MME for control; S-GW/P-GW for user plane, with GTP-U tunnels) evolved into the 5G Core, a service-based architecture of cloud-native functions (AMF, SMF, UPF and others).
  - Full control and user plane separation (CUPS).
- **Analogy:**
  - The tower (eNB/gNB) is a post office counter.
  - The core is the sorting headquarters: AMF is the front desk that checks your ID, SMF is the clerk who opens your delivery account, UPF is the conveyor belt that actually moves the parcels, and UDM/HSS is the citizens' register.
- **Worked example:** 5G registration and PDU session in 10 steps.
  1. UE → gNB RRC setup.
  2. Registration Request (SUCI, the concealed SUPI) → AMF.
  3. AMF → AUSF → UDM: authentication with 5G-AKA. RAND, AUTN and RES* are explained at the level of "challenge/response with a SIM-held key".
  4. NAS Security Mode Command.
  5. Registration Accept (5G-GUTI).
  6. PDU Session Establishment Request → SMF.
  7. SMF selects a UPF and establishes the N4 (PFCP) session.
  8. The N3 GTP-U tunnel (TEIDs) is set up between gNB and UPF.
  9. The UE gets an IP address.
  10. Data flows with QoS Flow ID 9 (default).
  - Compare with the LTE attach (MME, HSS, S-GW/P-GW, default EPS bearer, QCI 9).
  - Also give a GTP-U overhead calculation: outer IPv4 20 + UDP 8 (port 2152) + GTP-U 8 (+ extension headers) = 36+ bytes. This links to VXLAN in Pillar 5: "everything is a tunnel".
- **Figures:**
  - **Fig 6.37:** LTE EPS block diagram. UE—(Uu)—eNB—(S1-MME)—MME—(S6a)—HSS; eNB—(S1-U)—S-GW—(S5)—P-GW—(SGi)—Internet; PCRF on Gx. Control lines dashed orange, user plane solid blue.
  - **Fig 6.38:** 5G SA service-based architecture. A bus labelled SBI (HTTP/2) connecting AMF, SMF, AUSF, UDM, PCF, NRF, NSSF and NEF. UPF below, connected by N4; gNB via N2/N3; DN via N6.
  - **Fig 6.39:** Protocol-stack comparison for the user plane: UE IP → PDCP → RLC → MAC → PHY ‖ gNB relays to GTP-U/UDP/IP → UPF.
  - **Fig 6.40:** Registration + PDU session sequence diagram with lanes UE, gNB, AMF, AUSF/UDM, SMF, UPF.
  - **Fig 6.41:** 4G versus 5G comparison table: waveform (OFDMA DL / SC-FDMA UL vs CP-OFDM both ways), numerology (15 kHz fixed vs 15·2^µ kHz), bands (sub-6 / mmWave), core (EPC vs 5GC), slicing (no/yes), latency targets (URLLC).
- **Sub-topics:**
  - NSA versus SA deployment (option 3x versus option 2).
  - Network slicing (S-NSSAI).
  - Handover: X2/Xn versus S1/N2.
  - O-RAN split (CU/DU/RU) in one paragraph, relevant to Nokia.
  - Wi-Fi/5G convergence (N3IWF), mentioned only.
- **Trap:** "5G is just faster LTE." Its core architecture, numerology and slicing are new. Also: confusing the AMF (mobility and access) with the SMF (sessions).
- **Company Lens:**
  - NOK (RAN/core software) and QCOM (modem) go deep.
  - A Qualcomm candidate was asked about the UE network attach procedure (Glassdoor).
  - CSCO (Private 5G) and MSFT (Azure Operator Nexus) are lighter.

## 6.3 Hands-on labs

Lab tags: Must = 6-L1, 6-L2, 6-L3. Should = 6-L4, 6-L5, 6-L6, 6-L9. Optional = 6-L7, 6-L8. Full configs and code are in Appendix 6-A. For readers without a monitor-mode adapter, every capture used is reproduced as an annotated frame table in the book.

| # | Lab | Tooling | Time | Outcome / checkpoint |
|---|---|---|---|---|
| 6-L1 | **Survey your hostel Wi-Fi** | `iw dev wlan0 scan` / `nmcli dev wifi` / WiFi Analyzer app | 1 h | A table of SSID, BSSID, channel, width, RSSI and security for 10+ networks. Identify channel overlap in 2.4 GHz. |
| 6-L2 | **Monitor-mode capture of your own connection** | USB adapter with monitor support (e.g. a MediaTek MT7612U or MT7921AU based card; check current compatibility lists) + `airmon-ng start wlan0` + Wireshark | 2 h | Capture beacon → auth → assoc → EAPOL 1–4 for *your own* AP. Use the Wireshark filter `eapol || wlan.fc.type_subtype == 0x0b || wlan.fc.type_subtype == 0x00`. **Ethics box:** only capture networks you own or are authorised to test. Indian law (IT Act 2000, sections 43/66) applies. |
| 6-L3 | **Decrypt your own WPA2 traffic** | Wireshark → Preferences → Protocols → IEEE 802.11 → Decryption keys (wpa-pwd) | 1 h | DHCP and ARP become visible after the 4-way handshake is captured. Explain why a capture missing EAPOL 1–2 cannot be decrypted. |
| 6-L4 | **Write an 802.11 frame parser in C** | C + libpcap reading a pcap file (provided), radiotap length parsing | 3 h | Output: `type=Mgmt subtype=Beacon BSSID=.. SSID=..` for every frame, plus counts per subtype. Uses bit masks on Frame Control. |
| 6-L5 | **Compute the PTK yourself** | Python (`hashlib`, `hmac`) using nonces extracted from the 6-L2 capture | 2 h | The computed MIC matches the MIC in EAPOL message 2, proving understanding of the key hierarchy. |
| 6-L6 | **Simulated Wi-Fi with mac80211_hwsim** | `modprobe mac80211_hwsim radios=3`, hostapd + wpa_supplicant configs (WPA2 and WPA3-SAE), all in network namespaces | 3 h | Build a full WPA3 AP and client on a laptop without real radios. Capture on `hwsim0` and compare SAE commit/confirm frames with WPA2. |
| 6-L7 | **Mininet-WiFi roaming** | Mininet-WiFi with 2 APs and a mobile STA along a path | 2 h | Plot RSSI over time and identify the roam point. Enable 802.11r in the hostapd config and compare the gap in `ping`. |
| 6-L8 | **CSMA/CA simulator** | Python (simpy or a hand-written discrete-event loop) | 3 h | Simulate N = 1..50 stations and plot throughput and collision probability against N. Compare with Bianchi's model curve (cite the paper). |
| 6-L9 | **5G core in a box** | Open5GS + UERANSIM in Docker | 3 h | `nr-ue` registers and gets an IP on `uesimtun0`. Capture NGAP/NAS and GTP-U on the N3 interface in Wireshark, and identify TEIDs. |

## 6.4 Company-tag matrix (Pillar 6)

| Topic | CSCO | QCOM | GOOG | MSFT | AMZN | JNPR | ANET | NOK | AVGO |
|---|---|---|---|---|---|---|---|---|---|
| RF basics, dB, link budget | ◐ | ● | ○ | ○ | ○ | ◐ (Mist) | ◐ | ● | ● |
| OFDM/QAM/MIMO | ◐ | ● | ○ | ○ | ○ | ◐ | ◐ | ● | ● |
| CSMA/CA, DCF, hidden node | ● | ● | ◐ | ○ | ◐ | ◐ | ◐ | ◐ | ● |
| 802.11 frame format and types | ◐ | ● | ○ | ○ | ○ | ◐ | ◐ | ○ | ● |
| Association + 4-way handshake | ● | ● | ◐ | ◐ | ◐ | ● | ◐ | ◐ | ● |
| WPA3/SAE/PMF, 802.1X | ● | ● | ◐ | ◐ | ◐ | ● | ◐ | ○ | ● |
| Wi-Fi 6/7 (OFDMA, MU-MIMO, MLO, TWT) | ● | ● | ○ | ○ | ○ | ● | ◐ | ◐ | ● |
| Roaming 802.11k/v/r | ● | ● | ○ | ○ | ○ | ● | ◐ | ○ | ◐ |
| Linux wireless stack / firmware | ◐ | ● | ◐ (Android/Nest) | ○ | ◐ (Kindle/Eero devices) | ○ | ○ | ○ | ● |
| LTE/5G architecture and attach | ◐ | ● | ○ | ◐ | ○ | ◐ | ○ | ● | ◐ |

## 6.5 Interview question bank (Pillar 6): 42 questions, each with a full in-book solution (see 0A.3)

1. [E] What is the difference between SSID, BSSID and ESSID? (CSCO, QCOM)
2. [E] Why does Wi-Fi use CSMA/CA instead of CSMA/CD? (QCOM, AVGO, CSCO)
3. [M] Explain DCF with SIFS, DIFS, slot time and back-off. Why is SIFS shorter than DIFS? (QCOM, AVGO)
4. [M] What is the hidden-node problem? How do RTS/CTS and the NAV solve it? What is the exposed-node problem? (QCOM, CSCO)
5. [M] What happens to the contention window after a failed transmission and after a success? (QCOM)
6. [E] Name the three 802.11 frame types and give two subtypes of each. (QCOM, AVGO)
7. [M] Explain the To DS/From DS bits and the meaning of the four address fields in each case. (QCOM, AVGO)
8. [M] What information is in a beacon frame? (QCOM, CSCO, JNPR)
9. [M] Walk through how a STA connects to a WPA2-Personal AP, frame by frame. (QCOM, CSCO, JNPR)
10. [M] What is the 4-way handshake for, and what keys result from it? (QCOM, CSCO, AVGO)
11. [H] How is the PTK derived? Why are both nonces and both MAC addresses included? (QCOM)
12. [H] What is the replay counter in EAPOL-Key frames? What was KRACK? (QCOM, AVGO)
13. [M] Difference between PMK, PTK and GTK. When is the GTK rotated? (QCOM, CSCO)
14. [M] Why is WPA2-PSK vulnerable to offline dictionary attacks, and how does SAE fix it? (QCOM, CSCO, JNPR)
15. [E] What is PMF (802.11w) and which attack does it stop? (CSCO, QCOM)
16. [M] Explain 802.1X roles and name two EAP methods. Which needs client certificates? (CSCO, JNPR)
17. [E] What is the difference between authentication and association in 802.11? (QCOM)
18. [M] Explain OFDM and why subcarriers are orthogonal. What is the cyclic prefix for? (QCOM, NOK)
19. [M] OFDM versus OFDMA. (QCOM, CSCO, JNPR)
20. [M] SU-MIMO versus MU-MIMO. What did 802.11ax add over 802.11ac for MU-MIMO? (QCOM, AVGO)
21. [H] What is a trigger frame? Describe an uplink OFDMA exchange. (QCOM, AVGO)
22. [M] What is BSS colouring? (QCOM, CSCO)
23. [M] What is TWT and which devices benefit? (QCOM, AVGO)
24. [M] List four Wi-Fi 7 features and the benefit of each. (QCOM, CSCO, AVGO)
25. [H] Explain MLO modes (STR, NSTR, EMLSR) and a firmware challenge each introduces. (QCOM, AVGO)
26. [E] What is A-MPDU versus A-MSDU? Which survives better on a noisy channel, and why? (QCOM)
27. [M] What is Block Ack? (QCOM, AVGO)
28. [M] Explain EDCA access categories and how voice gets priority. (QCOM, CSCO)
29. [M] What are TIM and DTIM? How does a sleeping STA get buffered unicast frames? (QCOM, AVGO)
30. [M] How does 802.11r speed up roaming? What do 802.11k and 802.11v add? (CSCO, JNPR, QCOM)
31. [H] Users complain voice calls drop while walking down a corridor. How do you troubleshoot? (CSCO, JNPR)
32. [E] Convert 200 mW to dBm. What does −3 dB mean? (QCOM, NOK)
33. [M] Why are only channels 1, 6 and 11 recommended in 2.4 GHz? (CSCO)
34. [H] Throughput is low even though RSSI is −50 dBm. List causes. *(Interference, co-channel contention, low MCS from a high noise floor, retries, legacy clients forcing protection, a channel-width mismatch.)* (CSCO, QCOM)
35. [H] What is rate adaptation? Describe one algorithm. (QCOM, AVGO)
36. [X] In firmware, how would you schedule RUs across 20 STAs with mixed QoS? State the inputs, the constraints and a greedy heuristic. (QCOM)
37. [M] Describe the LTE architecture (MME, S-GW, P-GW, HSS). (NOK, QCOM)
38. [M] What are AMF, SMF and UPF in 5G? What is a service-based architecture? (NOK, QCOM)
39. [H] Walk through the UE attach or registration procedure and PDU session establishment. (QCOM, NOK)
40. [M] What is GTP-U? Why tunnel user data between gNB and UPF? (NOK, QCOM)
41. [X] Compare 5G NR numerology with LTE. What does µ = 3 mean for slot duration? (QCOM, NOK)
42. [E] In Linux, what are cfg80211, mac80211 and nl80211? (QCOM, AVGO)

## 6.6 Trap boxes (Pillar 6 consolidated)

1. CSMA/**CA**, not CD. There is no collision detection on half-duplex radios.
2. +3 dB = 2×, +10 dB = 10×. dBm is absolute, dBi is antenna gain relative to isotropic.
3. 802.11 "open authentication" is not security.
4. The PMK and PSK are never transmitted.
5. OFDMA is about efficiency for many users, not peak single-user speed.
6. Wi-Fi 6E = 802.11ax in 6 GHz, not a new PHY.
7. The client decides to roam; the AP only suggests.
8. Address 3 meaning depends on the To DS/From DS bits.
9. WPA3 transition mode can be downgraded.
10. The 802.11 frame is little-endian on the wire, unlike network byte order in IP.
11. AMF ≠ MME clone: the MME's session functions moved to the SMF.
12. Monitor mode ≠ promiscuous mode. Promiscuous mode on a managed interface does not show other stations' 802.11 frames.

## 6.7 Cheat-sheet contents (one double-sided A4 page)

- **Side A (Wi-Fi):**
  - dB table (0, 3, 6, 10, 20, 30 dB).
  - FSPL formula.
  - Channel plan sketch.
  - Generations table (4/5/6/6E/7).
  - DCF timing numbers (5 GHz: slot 9, SIFS 16, DIFS 34; 2.4 GHz long/short slot).
  - CW sequence.
  - MAC header layout.
  - DS-bit table.
  - Frame subtype codes most often filtered in Wireshark (beacon 0x08, probe req 0x04, resp 0x05, auth 0x0b, assoc req 0x00, resp 0x01, deauth 0x0c, ACK 0x1d, RTS 0x1b, CTS 0x1c, BA 0x19, QoS data 0x28).
  - Wireshark filter strings.
- **Side B (security and cellular):**
  - Connection lifecycle strip.
  - Key hierarchy.
  - The four EAPOL messages with their contents.
  - WPA2 versus WPA3.
  - EDCA table.
  - 802.11k/v/r one-liners.
  - Wi-Fi 6/7 features against their benefits.
  - LTE versus 5G node-name map (MME→AMF + part of SMF; S-GW/P-GW-U→UPF; HSS→UDM/AUSF; PCRF→PCF).
  - GTP-U port 2152.
  - Registration steps in 10 words each.

## 6.8 Mini-project (Pillar 6): "Air Sniffer: a Wi-Fi Connection Doctor"

- **Brief:** A command-line tool, in C for the parsing core and Python for reports.
  - It reads a monitor-mode pcap or attaches live to a monitor interface.
  - For each client, it reconstructs the connection timeline: probe → auth → assoc → EAPOL 1–4 → first data.
  - It flags problems: missing EAPOL 4 (wrong PSK likely), repeated EAPOL 3 (retransmission, link quality), deauth reason codes (decoded to text), high retry-bit ratio (> 10%), the MCS distribution, and channel utilisation estimated from frame durations.
- **Stretch goals:**
  - Support WPA3-SAE frames.
  - Show an 802.11r roam timeline.
  - Output an HTML report with a per-client swim-lane, reusing figure styles from the chapter.
- **Testing:** Use mac80211_hwsim captures (Lab 6-L6) so every student can create known-good and known-bad cases. For example, configure a wrong PSK and confirm the tool says "EAPOL 2 MIC failure likely, wrong passphrase".
- **Interview pay-off:** It speaks directly to QCOM and AVGO WLAN firmware and CSCO/JNPR wireless roles. It demonstrates C bit-manipulation, protocol knowledge and debugging.

## 6.9 Sources (Pillar 6)

Researched during planning:

- Qualcomm interview reports (Glassdoor), including the OFDMA-orthogonality and UE-attach questions:
  - https://www.glassdoor.com.ar/Entrevista/Qualcomm-Entrevista-E640-RVW88920767.htm
  - https://www.glassdoor.com/Interview/Qualcomm-Interview-E640-RVW24929658.htm
  - https://static.glassdoor.com.ar/Interview/Qualcomm-Interview-E640-RVW98552849.htm
- Qualcomm Firmware Engineer interview questions, India (Glassdoor): https://www.glassdoor.co.in/Interview/Qualcomm-Firmware-Engineer-Interview-Questions-EI_IE640.0,8_KO9,26.htm
- Qualcomm Software Engineer – WLAN posting (MU-MIMO, OFDMA, TWT, rate control): https://www.tealhq.com/job/software-engineer-wlan_7ea1ab46ddb59028caa4087869fd75c61ce7a
- WLAN interview Q&A collections:
  - https://www.rfwireless-world.com/jobs/WLAN-interview-questions-answers.html
  - https://wifibysandeep.blogspot.com/2022/10/wlan-qa_28.html
- 4-way handshake overview: https://itwissen.info/en/4-way-handshake-127297.html
- Wi-Fi 7 explainer (vendor; MLO, 320 MHz, 4096-QAM): https://www.purple.ai/en-gb/guides/wi-fi-7-802-11be-explained-what-changes-for-enterprise-wifi

Primary references for authors (verify editions):

- IEEE 802.11-2020 standard and the 802.11ax-2021 and 802.11be amendments: https://standards.ieee.org/ieee/802.11/7028/
- Wi-Fi Alliance, WPA3 specification and Wi-Fi 7 overview: https://www.wi-fi.org/discover-wi-fi/security and https://www.wi-fi.org/discover-wi-fi/wi-fi-certified-7
- Vanhoef and Piessens, "Key Reinstallation Attacks" (CCS 2017): https://www.krackattacks.com/
- Bianchi, "Performance Analysis of the IEEE 802.11 DCF", IEEE JSAC 2000 (DOI 10.1109/49.840210)
- Linux wireless documentation (cfg80211, mac80211, nl80211, mac80211_hwsim): https://wireless.docs.kernel.org/
- Matthew Gast, *802.11 Wireless Networks: The Definitive Guide* (O'Reilly), and *802.11ac: A Survival Guide*.
- 3GPP TS 23.501 (5G system architecture) and TS 23.502 (procedures): https://www.3gpp.org/specifications-technologies
- Open5GS: https://open5gs.org/ and UERANSIM: https://github.com/aligungr/UERANSIM
- Mininet-WiFi: https://mininet-wifi.github.io/

## 6.10 End-of-chapter pack (per 0A.4)

- Short notes, ordered as section 6.2.x.
- One-page revision sheet, built from 6.7.
- 60 flashcards.
- Solutions to all 42 questions in 6.5, in the five-part format.
- Five extended whiteboard problems (listed in 0A.4).
- A 20-question self-test with an answer key.

---


# PILLAR 7: Operating Systems and Socket Programming

## 7.0 Chapter header

- **Title:** *Chapter 7: The Machine Under the Packet: Processes, Concurrency, Memory, Interrupts and Sockets*
- **One-line promise:** By the end you can answer every "process vs thread / mutex vs semaphore / deadlock / virtual memory / interrupt" question that Cisco, Juniper and Qualcomm ask. You will also have written a working epoll-based TCP server in C, and you can trace a packet from the NIC through NAPI and sk_buff to `recv()`.
- **Prerequisites:**
  - Pillar 2: C pointers, structs, bit operations, `malloc`/`free`, compiling with `gcc -Wall -g`, and gdb basics.
  - Pillar 3: TCP state machine and UDP.
  - Pillar 8 (light): shell, `ps`, `top`, `strace`.
- **Estimated pages:** 120–135, with about 45 figures and about 25 code listings.
- **Weeks (full, comprehensive read):** 4.5 weeks at about 10 hours per week.
  - Week 1: sections 7.2.1–7.2.4 (OS, processes, threads, scheduling).
  - Week 2: sections 7.2.5–7.2.6 (synchronisation, deadlock).
  - Week 3: sections 7.2.7–7.2.9 (memory, interrupts, IPC).
  - Week 4: sections 7.2.10–7.2.12 (sockets, epoll, the Linux stack).
  - Half week: section 7.2.13 and the mini-project.
- **Must-path estimate:** about 5 study days for the Must sections only (see the tag table in section 0). This is a navigation aid for time-pressed readers, not a cut. All content stays in the book.

## 7.1 Learning objectives

1. Define a process, its address-space layout (text, data, BSS, heap, stack, mmap) and its PCB. Trace `fork()`, `exec()`, `wait()` and zombie/orphan behaviour, including predicting the output of fork puzzles.
2. Distinguish processes from threads: what is shared and what is private, user-level versus kernel threads, and the cost of a context switch.
3. Compare the CPU-scheduling algorithms (FCFS, SJF, RR, priority, MLFQ, Linux CFS/EEVDF) and compute waiting and turnaround times by hand.
4. Explain race conditions and critical sections. Use and compare mutexes, spinlocks, semaphores (counting and binary), condition variables and read-write locks. Implement producer-consumer with a bounded buffer.
5. Name the four Coffman conditions, then prevent, avoid (the Banker's algorithm, worked) and detect deadlock. Explain priority inversion and priority inheritance.
6. Explain virtual memory: paging, page tables (multi-level), the TLB, page faults, the replacement algorithms (FIFO, LRU, Optimal, Clock, with Bélády's anomaly), thrashing, copy-on-write and `mmap`.
7. Explain stack versus heap, memory alignment and struct padding, memory leaks, and the basics of allocator design (free lists, a slab allocator).
8. Explain interrupts: hardware versus software, ISR top-half/bottom-half (softirq, tasklet, workqueue), interrupt context restrictions, polling versus interrupts, DMA, and system calls.
9. Use IPC: pipes, FIFOs, message queues, shared memory and signals, and compare them.
10. Write TCP and UDP client/server programs in C with the Berkeley sockets API, handling byte order, partial reads and writes, `SO_REUSEADDR`, `TIME_WAIT` and errors.
11. Compare I/O models: blocking, non-blocking, `select`, `poll`, `epoll` (level-triggered versus edge-triggered), and io_uring (overview). Build a C10K-style epoll server.
12. Trace the Linux receive and transmit paths: NIC → DMA ring → IRQ → NAPI poll → `sk_buff` → GRO → `netif_receive_skb` → `ip_rcv` → netfilter → routing → `tcp_v4_rcv` → socket receive queue → `recv()`. Know where XDP, tc and RSS/RPS fit, and what DPDK bypasses.
13. Explain the basics of embedded and RTOS work relevant to Qualcomm, Cisco and Broadcom firmware: volatile, memory barriers, endianness, atomic operations, and lock-free ring buffers.

## 7.2 Section-by-section outline

Each section heading carries its navigation tag and an indicative Must-path study-day estimate: **[Must | x d]**, **[Should | x d]** or **[Optional]**. Tags guide reading order; they never remove content.

### 7.2.1 What an operating system really does **[Must | 0.25 d]**

- **Core idea:** An OS is a resource manager and a protection boundary. It multiplexes CPU, memory and devices among programs, and isolates them via user mode and kernel mode.
- **Analogy:** A hostel warden who allocates rooms (memory), sets the bathroom timetable (CPU scheduling), keeps the master keys (kernel mode) and handles complaints (system calls and interrupts).
- **Worked example:** `strace -c ls`.
  - List the system calls made (openat, read, write, mmap, close) and count them.
  - Explain the user→kernel transition per call (syscall instruction, mode bit, kernel stack).
- **Figures:**
  - **Fig 7.1:** Layered ring diagram: hardware → kernel (scheduler, memory manager, VFS, network stack, drivers) → system-call interface → libc → applications. The user/kernel boundary is a thick dashed line.
  - **Fig 7.2:** System-call sequence: user code → libc wrapper → `syscall` instruction → syscall table lookup → handler → return value in a register.
- **Trap:** "A system call is a function call." It involves a privilege-level switch, and with mitigations it costs about 100 ns or more.

### 7.2.2 Processes, `fork`/`exec` and the address space **[Must | 0.5 d]**

- **Core idea:**
  - A process is a program in execution. It has its own virtual address space, a PCB (task_struct in Linux) and a state: new, ready, running, waiting or terminated.
  - `fork()` duplicates the process using copy-on-write; `exec()` replaces its image.
- **Analogy:** `fork` is photocopying a filled-in form (identical at first; edits diverge). `exec` is erasing the form and filling in a completely different one under the same file number (PID).
- **Worked example:**
  - **(A)** `for (i = 0; i < 3; i++) fork(); printf("hi\n");` prints 8 times. Draw the process tree. Then the variant `fork() && fork() || fork();` gives 5 processes; show the short-circuit tree.
  - **(B)** Zombie and orphan.
    - The child exits but the parent never calls `wait()`, so `ps` shows `<defunct>`.
    - The parent dies first, so the child is re-parented to init/systemd (PID 1, or a subreaper).
  - **(C)** Address layout. Print the addresses of a global, a static, a local, a malloc'd pointer and a function. Run twice and observe ASLR.
- **Figures:**
  - **Fig 7.3:** Virtual address space, vertical from low to high: text | data | BSS | heap ↑ | (mmap/shared libs) | stack ↓ | kernel space. Arrows show growth directions; sample addresses come from the worked example.
  - **Fig 7.4:** Process state diagram: five states and the transitions admit, dispatch, timeout/preempt, I/O wait, I/O done and exit.
  - **Fig 7.5:** fork tree for example A, as a binary tree with PIDs at the nodes and the printf leaves highlighted.
  - **Fig 7.6:** PCB contents box: PID, state, PC, registers, memory map pointer (mm_struct), open file table, priority, signal masks.
- **Trap:** In fork puzzles, forgetting stdout buffering. `printf("hi")` without `\n` before a fork, with output redirected to a file, prints duplicates.

### 7.2.3 Threads and context switching **[Must | 0.5 d]**

- **Core idea:**
  - Threads are execution contexts inside one process. They share code, heap, globals and file descriptors, but each has a private stack, registers and thread-local storage.
  - Switching threads is cheaper than switching processes because there is no address-space (page table / TLB) change.
- **Analogy:** A process is a flat; threads are flatmates. They share the kitchen and fridge (heap and globals) but each has their own bed (stack). A fire (a crash) burns the whole flat.
- **Worked example:**
  - Two pthreads each increment a shared `counter` 1,000,000 times without a lock. The result is around 1.2–1.9 M, not 2 M.
  - Show the assembly (`load, add, store`) and an interleaving table that loses one increment.
  - Measure the context switch with a pipe ping-pong between two processes against two threads. Report the method and indicative results without promising numbers.
- **Figures:**
  - **Fig 7.7:** Single-threaded versus multithreaded process diagram (the classic shared code/data/files with three separate stacks and register sets).
  - **Fig 7.8:** Interleaving table: time steps T1–T6 with columns Thread A, Thread B and the counter value, showing the lost update.
  - **Fig 7.9:** Context-switch steps: save registers → update PCB → scheduler picks → (switch page table, flush/tag TLB if a process switch) → restore registers.
- **Sub-topics:**
  - User threads versus kernel threads (1:1 in Linux NPTL; M:N in Go).
  - `clone()` flags.
  - Thread-safety and reentrancy (strtok versus strtok_r).
  - Does one thread crashing kill the process? Yes, from SIGSEGV; this is a Cisco question.
- **Trap:** "Threads have separate heaps." They share the heap. Also: "A context switch between threads flushes the TLB." It does not within one process.

### 7.2.4 CPU scheduling **[Should | 0.5 d]**

- **Core idea:** The scheduler picks which ready task runs next, balancing throughput, latency and fairness.
  - Pre-emptive algorithms (RR, priority, MLFQ, CFS) interrupt running tasks.
  - Non-pre-emptive ones (FCFS, SJF) do not.
- **Analogy:** A canteen queue. FCFS is plain queueing, SJF lets "just a tea" people go first, and round robin gives everyone 2 minutes at the counter before rejoining the queue.
- **Worked example:** Five processes with arrival and burst times (P1 0/8, P2 1/4, P3 2/9, P4 3/5, P5 4/2).
  - Draw Gantt charts for FCFS, SJF (non-pre-emptive), SRTF and RR with q = 2.
  - Compute the average waiting time and turnaround for each, in a results table.
  - Then explain CFS vruntime with two tasks of weight ratio 2:1, and note that EEVDF replaced CFS's pick logic from Linux 6.6.
- **Figures:**
  - **Fig 7.10:** Four stacked Gantt charts with a common time axis and coloured process blocks.
  - **Fig 7.11:** MLFQ diagram: three queues (q = 8, 16, FCFS), with demotion and periodic boost arrows.
  - **Fig 7.12:** CFS red-black tree keyed by vruntime, with the leftmost node highlighted as "next to run".
- **Trap:** SJF is optimal for average waiting time, but it needs future knowledge and can starve long jobs. Also: priority inversion is introduced here and revisited in 7.2.6.

### 7.2.5 Synchronisation primitives **[Must | 0.75 d]**

- **Core idea:**
  - Races are prevented by mutual exclusion around critical sections.
  - A *mutex* is a lock with ownership.
  - A *semaphore* is a counter with wait/signal.
  - A *spinlock* busy-waits and suits short sections where sleeping is not allowed (interrupt context).
  - *Condition variables* let threads sleep until a predicate holds.
- **Analogy:**
  - Mutex: the single key to the lab; whoever takes it must return it.
  - Counting semaphore: a car park with a "spaces free: 5" display.
  - Spinlock: standing at the door rattling the handle rather than going for a nap.
  - Condition variable: a "wake me when the parcel arrives" note at the reception desk.
- **Worked examples:**
  - **(A)** Fix the counter from 7.2.3 with `pthread_mutex_lock`, and show the cost. Then with `__atomic_fetch_add` and compare.
  - **(B)** Bounded-buffer producer-consumer, done twice:
    - Semaphores `empty = N`, `full = 0` and a mutex. Explain why the order of `wait(empty)` before `wait(mutex)` matters; reversing it deadlocks.
    - Condition variables with `while (count == N) pthread_cond_wait(&not_full, &m);`. Explain why `while`, not `if`: spurious wake-ups and stolen wake-ups.
  - **(C)** Readers-writers with `pthread_rwlock`, and writer starvation.
  - **(D)** Implement a spinlock with test-and-set (`__atomic_test_and_set`), then test-and-test-and-set. Explain cache-line bouncing.
  - **(E)** Dining philosophers: the deadlock version, then the ordered-forks fix.
- **Figures:**
  - **Fig 7.13:** Comparison table of mutex, binary semaphore, counting semaphore, spinlock and condition variable. Columns: ownership, can sleep?, usable in ISR?, typical use, Linux kernel API (`mutex_lock`, `down`/`up`, `spin_lock_irqsave`, `wait_event`).
  - **Fig 7.14:** Bounded-buffer ring with head/tail pointers, producer and consumer arrows, and semaphore counters shown as gauges.
  - **Fig 7.15:** Timeline of a condition-variable wait: lock held → `cond_wait` atomically releases and sleeps → signal → re-acquire → re-check predicate.
  - **Fig 7.16:** Dining philosophers round table with 5 forks, showing the deadlock cycle in red and the fix in green.
- **Trap:**
  - "A binary semaphore is the same as a mutex." It is not. A mutex has an owner, so only the locker unlocks; that enables priority inheritance and recursive or error-checking types. A semaphore can be signalled by any thread, which makes it usable for signalling between threads.
  - Juniper and Cisco reports ask exactly this.
- **Company Lens:** Juniper candidates were asked to implement mutexes and semaphores, and to write multithreaded programs that use them. Cisco asks "when to use a mutex over a semaphore". Qualcomm asks about ISR-safe locking.

### 7.2.6 Deadlock, starvation and priority inversion **[Must | 0.5 d]**

- **Core idea:**
  - Deadlock requires all four Coffman conditions: mutual exclusion, hold-and-wait, no pre-emption and circular wait.
  - Break any one to prevent it. Avoid it dynamically with the Banker's algorithm. Detect it with wait-for graphs.
- **Analogy:** Four cars at a four-way junction, each waiting for the car on its right. All four conditions hold, so nobody moves.
- **Worked examples:**
  - **(A) Banker's algorithm.**
    - Five processes and three resource types (A = 10, B = 5, C = 7). Use the classic Allocation/Max matrices, stated in full in the book.
    - Compute Need = Max − Allocation.
    - Find the safe sequence step by step (e.g. P1, P3, P4, P0, P2), showing the Work vector at each step.
    - Then test the request P1 = (1, 0, 2).
  - **(B) Lock ordering.** Thread 1 does lock(A) then lock(B); thread 2 does lock(B) then lock(A). Draw the wait-for graph and fix it with a global ordering.
  - **(C) Mars Pathfinder priority inversion.** Low, medium and high-priority tasks, and how priority inheritance resolves it.
- **Figures:**
  - **Fig 7.17:** Resource-allocation graph with a cycle, and a variant without a cycle.
  - **Fig 7.18:** Banker's worked table, with rows per iteration and the Work vector column highlighted.
  - **Fig 7.19:** Priority inversion timeline with three lanes (H, M, L): before and after inheritance.
- **Trap:** "A cycle in a resource graph always means deadlock." That holds only with single-instance resources. With multiple instances, a cycle is necessary but not sufficient.

### 7.2.7 Memory management and virtual memory **[Must | 0.75 d]**

- **Core idea:**
  - Each process sees a private virtual address space. The MMU translates virtual pages to physical frames via page tables, cached in the TLB.
  - Missing pages cause page faults that the kernel resolves, from disk, by zero-fill or by copy-on-write.
- **Analogy:** A virtual address is a "seat number on your ticket". The page table is the usher's chart mapping seat numbers to real chairs. The TLB is the usher's memory of the last few lookups.
- **Worked examples:**
  - **(A) Address split.**
    - 32-bit VA with 4 KB pages: offset 12 bits, VPN 20 bits.
    - Translate 0x00403ABC given the page-table entry VPN 0x00403 → PFN 0x1A2. The PA is 0x1A2ABC.
    - Then a two-level table (10 + 10 + 12): compute the memory needed for the page tables of a process using 8 MB.
  - **(B) Effective access time.**
    - TLB hit 95%, TLB 1 ns, memory 100 ns.
    - EAT = 0.95 × (1 + 100) + 0.05 × (1 + 100 + 100) ≈ 106 ns.
  - **(C) Page replacement.**
    - Reference string 7 0 1 2 0 3 0 4 2 3 0 3 2 with 3 frames.
    - Count the faults under FIFO, LRU and Optimal, with a table of frame contents at each step.
    - Then show Bélády's anomaly with FIFO on 1 2 3 4 1 2 5 1 2 3 4 5 (3 frames give 9 faults; 4 frames give 10).
  - **(D) Struct padding.**
    - `struct { char a; int b; char c; }` is 12 bytes. Reordering to `{int b; char a; char c;}` gives 8 bytes.
    - Show `offsetof`, and `__attribute__((packed))` with its unaligned-access cost on ARM. This is Arista's struct-padding question.
  - **(E) A tiny allocator.** A first-fit free list over a 4 KB static arena, with split and coalesce. This is for Arista's "design a memory allocation library" question; full code is in Appendix 7-A.
- **Figures:**
  - **Fig 7.20:** Address translation pipeline: VA → [VPN | offset] → TLB lookup (hit → PA) / (miss → page-table walk) → PA → cache/memory. Fault branch → kernel.
  - **Fig 7.21:** Two-level (and x86-64 four-level) page table tree diagram.
  - **Fig 7.22:** Page-replacement tables for the three algorithms, side by side, with fault cells shaded.
  - **Fig 7.23:** Copy-on-write after fork: two page tables pointing at the same frames marked read-only. After a write, the frame is duplicated.
  - **Fig 7.24:** Struct memory layout grid in bytes, with padding cells hatched.
  - **Fig 7.25:** Free-list allocator heap diagram: blocks with headers (size, free flag), before and after malloc/free/coalesce.
- **Sub-topics:**
  - Internal versus external fragmentation.
  - Segmentation (brief).
  - Thrashing and the working set.
  - `mmap` for files and anonymous memory.
  - Huge pages (relevant to DPDK).
  - The slab allocator (kmem_cache; `sk_buff` uses one).
  - Stack overflow and recursion depth.
  - Memory-mapped I/O registers in firmware.
- **Trap:**
  - "Virtual memory means using disk as RAM." That is only swapping; VM is primarily about isolation and translation.
  - "malloc returns physical memory." It returns virtual memory, and pages are allocated on first touch.

### 7.2.8 Interrupts, system calls, DMA and kernel context **[Must | 0.5 d]**

- **Core idea:**
  - Devices signal the CPU via interrupts. The CPU saves state, jumps through the vector table to an ISR (the top half), which must be fast and must not sleep.
  - Heavier work is deferred to bottom halves (softirqs, tasklets, workqueues).
  - DMA lets devices move data to memory without the CPU.
- **Analogy:** The doorbell (interrupt). You open the door and sign for the parcel (top half: quick), then unpack it later (bottom half). DMA is a courier who has a key and puts the parcel straight in your cupboard.
- **Worked example:**
  - Read `/proc/interrupts` on a laptop.
  - Identify per-CPU counts for the NIC queues (e.g. `iwlwifi` or `enp0s3-rx-0`).
  - Watch the counts climb during an `iperf3` run.
  - Then compute: at 10 Gb/s with 64-byte frames (≈14.88 Mpps), one interrupt per packet is impossible. This motivates interrupt coalescing and NAPI.
  - Polling versus interrupts trade-off table (the Cisco internship question).
- **Figures:**
  - **Fig 7.26:** Interrupt flow: device → interrupt controller (APIC/GIC) → CPU → save context → IDT/vector table → ISR → ack device → schedule bottom half → return (iret/eret).
  - **Fig 7.27:** Top-half versus bottom-half table, with columns: context, can sleep?, can be pre-empted?, example in a NIC driver.
  - **Fig 7.28:** DMA descriptor ring. The circular buffer of descriptors with head (written by the NIC) and tail (refilled by the driver), and pointers to packet buffers.
- **Trap:**
  - Calling `kmalloc(GFP_KERNEL)` or taking a mutex inside an ISR. Neither may sleep; use `GFP_ATOMIC` and spinlocks.
  - Forgetting `volatile` and memory barriers for device registers.

### 7.2.9 Inter-process communication and signals **[Should | 0.25 d]**

- **Core idea:** Processes communicate via the kernel, using pipes, FIFOs, message queues and sockets. They can also share memory (fastest, but synchronisation is needed). Signals are asynchronous notifications.
- **Analogy:**
  - Pipe: a one-way speaking tube.
  - Message queue: a pigeonhole system.
  - Shared memory: a shared whiteboard.
  - Signal: a tap on the shoulder.
- **Worked example:**
  - Implement `ls | wc -l` in C with `pipe()`, `fork()`, `dup2()` and `execlp()`.
  - Then a shared-memory counter between two processes using `shm_open` + `mmap` + a process-shared mutex.
  - Signals: handle SIGINT and explain async-signal-safe functions (why `printf` in a handler is wrong). SIGCHLD for zombie reaping. SIGPIPE when writing to a closed socket, and how to handle it with `MSG_NOSIGNAL` or by ignoring the signal.
- **Figures:**
  - **Fig 7.29:** IPC comparison table with these columns: mechanism, direction, related processes only?, kernel copies, speed, synchronisation needed.
  - **Fig 7.30:** Pipe + fork + dup2 file-descriptor table diagram, before and after the dup2 calls.

### 7.2.10 Sockets from first principles **[Must | 0.75 d]**

- **Core idea:**
  - A socket is a file descriptor bound to a protocol endpoint.
  - TCP servers follow `socket → bind → listen → accept → read/write → close`; clients follow `socket → connect → write/read → close`.
  - UDP uses `sendto`/`recvfrom` without a connection.
- **Analogy:** A shop phone line.
  - `socket` buys a phone and `bind` assigns its number.
  - `listen` switches the ringer on and sets how many callers can wait on hold.
  - `accept` picks up a call, giving a new line per caller while the main number keeps ringing.
- **Worked examples:**
  - **(A)** A minimal TCP echo server and client, full code of about 60 lines each, with error checking.
    - Explain `htons`/`htonl` (an endianness worked example: 0x1F90 = 8080 stored as 90 1F on x86).
    - `INADDR_ANY`, `SO_REUSEADDR`, and the listen backlog (SYN queue versus accept queue).
  - **(B) Partial reads and writes.**
    - The `writen()` / `readn()` loop.
    - Message framing with a 4-byte length prefix. TCP is a byte stream; "one send ≠ one recv" is demonstrated by sending 3 messages and receiving them coalesced.
  - **(C) Map socket calls to TCP states.**
    - `connect()` sends a SYN. `accept()` returns after the 3-way handshake completes in the kernel.
    - `close()` sends a FIN. The side that closes first enters `TIME_WAIT` for 2 × MSL (60 s on Linux).
    - Use `ss -tanp` to watch the states.
  - **(D)** UDP echo, and why `recvfrom` gives you the peer address.
  - **(E)** `getaddrinfo` for IPv4/IPv6-agnostic code.
- **Figures:**
  - **Fig 7.31:** Client/server call-sequence diagram. Two columns (server, client) of API boxes, with arrows mapped to SYN, SYN-ACK, ACK, data and FIN packets in the middle.
  - **Fig 7.32:** Kernel queues: the listen socket with a SYN queue (half-open) and an accept queue (fully established). `accept()` pops from the accept queue. The backlog is annotated.
  - **Fig 7.33:** TCP state diagram, simplified, with the socket call that triggers each transition overlaid.
  - **Fig 7.34:** Byte-stream illustration: three `send()` calls (10, 20, 5 bytes) arriving as two `recv()` calls (25, 10).
- **Trap:**
  - Assuming one `recv()` equals one message.
  - Forgetting `htons` on the port.
  - Ignoring the `EINTR` and `EAGAIN` return values.
  - Not handling SIGPIPE.
  - Confusing `SO_REUSEADDR` with `SO_REUSEPORT`.
  - Thinking `TIME_WAIT` is a bug. It protects against delayed segments.

### 7.2.11 Concurrency models for servers: threads, select, poll, epoll **[Must | 0.75 d]**

- **Core idea:**
  - Thread-per-connection is simple but scales poorly.
  - I/O multiplexing lets one thread watch many sockets. `select` and `poll` are O(n) per call. `epoll` keeps an interest list in the kernel and returns only the ready descriptors, O(ready).
  - Edge-triggered mode requires non-blocking sockets and draining until `EAGAIN`.
- **Analogy:**
  - Thread-per-connection: hiring one waiter per table.
  - `select`/`poll`: one waiter walking past every table asking "ready?".
  - `epoll`: tables have call buttons, and the waiter only visits tables whose light is on.
  - Edge-triggered: the light blinks once. If you don't finish serving that table, it won't blink again.
- **Worked example:** An epoll echo/chat server in C (full listing of about 150 lines, annotated line by line).
  - `epoll_create1(0)`; `fcntl(fd, F_SETFL, O_NONBLOCK)`; `epoll_ctl(ADD, listen_fd, EPOLLIN)`.
  - Loop over `epoll_wait`:
    - If the listen fd is ready, accept in a loop until `EAGAIN` and add each client fd with `EPOLLIN | EPOLLET`.
    - Otherwise, read until `EAGAIN` and write back.
    - Handle `EPOLLRDHUP`/`EPOLLHUP`.
  - Then measure with a provided load generator (or `wrk` / a small C client): 10, 100, 1,000 and 10,000 concurrent connections. Compare a thread-per-connection version, a `select` version (FD_SETSIZE limit of 1024) and the epoll version. Present the results as a template table; students fill it in.
  - Discuss the thundering herd (`EPOLLEXCLUSIVE`, `SO_REUSEPORT` sharding), and the reactor pattern (libevent, nginx).
  - io_uring as the next step: a completion-based model, overview only.
- **Figures:**
  - **Fig 7.35:** Four-panel comparison: blocking, non-blocking busy loop, multiplexed (`select`/`poll`/`epoll`) and async (io_uring). Time on the x-axis shows where the app waits and where the kernel copies.
  - **Fig 7.36:** epoll internals: the interest list (red-black tree of fds), the ready list (linked list), and wakeup callbacks from socket wait queues.
  - **Fig 7.37:** LT versus ET waveform diagram. A data-available signal over time, with LT notifying on every `epoll_wait` while data remains and ET notifying only on the rising edge.
  - **Fig 7.38:** Scaling chart template (line chart): connections (log x) against requests/s, with three lines for threads, select and epoll. Leave axes and labels in place for the student's own data.
- **Trap:**
  - With ET mode on a blocking socket, the server hangs.
  - Not draining in ET mode loses events.
  - `select` cannot watch fd ≥ 1024.
  - Forgetting to `epoll_ctl(DEL)` before `close()` is harmless (close removes it), *unless* the fd was `dup`ed. That is an expert nuance.
- **Company Lens:** Cisco, Juniper and Arista ask "select vs poll vs epoll". Google SRE/networking asks the C10K problem. Qualcomm and Broadcom may ask event loops in firmware contexts.

### 7.2.12 The Linux network stack: from NIC to `recv()` **[Must | 0.5 d]**

- **Core idea:**
  - Packets arrive by DMA into ring buffers. A hardware IRQ schedules NAPI, which disables further IRQs and polls up to a budget of packets in softirq context.
  - Each packet is wrapped in an `sk_buff`, passed up through GRO, `netif_receive_skb`, IP, netfilter, routing and TCP, then queued on the socket. The application's `recv()` copies it to user space.
- **Analogy:** An airport baggage system.
  - DMA is the conveyor dropping bags into bins (the ring).
  - The IRQ is the bell. NAPI is a handler who, once rung, keeps unloading bags until the belt is empty or their shift budget ends, rather than responding to a bell per bag.
  - The `sk_buff` is the bag tag that accumulates routing stickers.
  - The socket queue is the carousel at your gate.
- **Worked example:** Trace one TCP segment.
  1. The NIC DMAs a frame into an RX descriptor buffer.
  2. MSI-X IRQ → the driver's ISR calls `napi_schedule()` and masks the IRQ.
  3. `NET_RX_SOFTIRQ` → `net_rx_action()` → the driver's `poll()` (budget 64, overall `netdev_budget` 300).
  4. The driver builds an `sk_buff` (`napi_alloc_skb`/`build_skb`) and sets `skb->protocol`.
  5. `napi_gro_receive()` merges segments.
  6. `__netif_receive_skb_core()` → taps (AF_PACKET; tcpdump sees it here) → `ip_rcv()`.
  7. `NF_INET_PRE_ROUTING` → route lookup (local) → `ip_local_deliver()` → `NF_INET_LOCAL_IN`.
  8. `tcp_v4_rcv()` → socket lookup → `tcp_rcv_established()` → queued on `sk->sk_receive_queue` → the process waiting in `recv()` or epoll is woken.
  9. `recv()` → `tcp_recvmsg()` → `copy_to_user`.

  - Show the `sk_buff` pointers `head`, `data`, `tail` and `end`, and `skb_push`/`skb_pull`/`skb_put`/`skb_reserve` with byte offsets, e.g. pulling 14 bytes for the Ethernet header.
  - Then the transmit path in brief: `send()` → `tcp_sendmsg` → `ip_queue_xmit` → qdisc → `dev_queue_xmit` → driver `ndo_start_xmit` → TX ring → completion IRQ.
  - Where XDP runs: in the driver, before `sk_buff` allocation, for native XDP. This resolves the conflicting secondary sources noted in research; cite kernel documentation.
  - RSS, RPS and RFS. DPDK as kernel bypass (PMD polling, huge pages). Cisco VPP and Nokia/Juniper user-space data planes as context.
- **Figures:**
  - **Fig 7.39:** Full receive-path flowchart (a hero figure across two pages). Hardware zone (NIC, DMA, ring), hard-IRQ zone, softirq zone (NAPI poll, GRO, protocol handlers, netfilter hooks as small diamonds), socket zone, user zone. Each arrow is labelled with a kernel function name. The XDP and tc hook points are marked as coloured pins.
  - **Fig 7.40:** `sk_buff` anatomy: the linear buffer with headroom, data and tailroom. Four pointer arrows, and before/after diagrams of `skb_pull(skb, 14)` and `skb_push(skb, 20)`. `skb_shared_info` frags are shown at the end.
  - **Fig 7.41:** Interrupt-per-packet versus NAPI. A timeline showing interrupts (spikes) against a polling window (shaded) under low and high load.
  - **Fig 7.42:** Kernel stack versus DPDK bypass, side by side, showing where the copies and context switches are removed.
- **Lab tie-ins:**
  - `ethtool -S`, `ethtool -l/-L` (queues), `ethtool -C` (coalescing).
  - `/proc/net/softnet_stat` columns (processed, dropped, time_squeeze).
  - `perf trace` or `bpftrace -e 'kprobe:tcp_v4_rcv { @[comm] = count(); }'`.
- **Trap:**
  - "tcpdump sees packets before the firewall." True on ingress (the AF_PACKET tap is before netfilter), but XDP drops happen before tcpdump.
  - "NAPI means no interrupts." It means interrupts are disabled while polling, then re-enabled.
- **Company Lens:** Cisco, Juniper, Arista, Nokia and Broadcom platform/SDK roles ask "how does a packet reach user space?" and "what is sk_buff?". Qualcomm data-path roles ask about NAPI and DMA rings.

### 7.2.13 Firmware and embedded essentials for networking chips **[Should | 0.25 d]**

- **Core idea:**
  - Networking firmware runs on constrained cores, often with an RTOS or bare metal.
  - Correctness depends on `volatile`, memory barriers, atomic operations, careful endianness handling and lock-free single-producer/single-consumer rings between host and device.
- **Analogy:** Working in a tiny ship's galley. Every utensil has a fixed place (static allocation), you can't wait for anything (no blocking in ISRs), and you shout "behind!" (barriers) before moving.
- **Worked examples:**
  - **(A)** An SPSC lock-free ring buffer in C11 atomics with a power-of-two size (head and tail masks). Explain why it needs only acquire/release ordering.
  - **(B)** Endianness.
    - Write `is_little_endian()`.
    - Swap with `__builtin_bswap32`.
    - Parse a big-endian IPv4 header and a little-endian 802.11 Frame Control from the same buffer, linking to Pillar 6.
  - **(C)** Bit manipulation set: count set bits, set/clear/toggle a bit, extract a field with mask and shift, check whether n is a power of two, reverse bits. These are Qualcomm/Arista favourites.
  - **(D)** C storage classes (auto, static, extern, register) and `const`/`volatile` combinations, e.g. `const volatile uint32_t *status_reg`. Asked at Qualcomm.
- **Figures:**
  - **Fig 7.43:** SPSC ring with head and tail indices, masks and an "owned by producer/consumer" colouring.
  - **Fig 7.44:** Endianness memory diagram: 0x12345678 laid out in big-endian and little-endian byte order across four addresses.
  - **Fig 7.45:** A memory-ordering hazard: two cores' store/load timeline without a barrier versus with release/acquire.
- **Trap:**
  - "`volatile` makes code thread-safe." It does not; it only prevents the compiler optimising accesses away.
  - Using `sizeof` on a pointer parameter instead of the array.

### 7.2.14 Putting it together: debugging a slow server **[Optional]**

- **Core idea:** Apply the chapter to a realistic incident: a TCP service with rising latency under load.
- **Worked example:** A story-led investigation.
  - `ss -s` shows a full accept queue (Recv-Q = backlog). The cause is the app's single thread blocking on disk I/O.
  - The fix is epoll plus a worker pool.
  - Then `softnet_stat` shows time_squeeze, so RSS queues and IRQ affinity are tuned.
  - This links to Pillar 11's troubleshooting method.
- **Figures:**
  - **Fig 7.46:** Investigation flowchart: symptom → hypothesis → command → evidence → fix.

## 7.3 Hands-on labs (all instructions fully in-book; code listings in Appendix 7-A)

| # | Lab | Tag | Days | Tooling | Outcome / checkpoint |
|---|---|---|---|---|---|
| 7-L1 | **fork puzzles and zombies** | Must | 0.1 | gcc, `ps -o pid,ppid,stat,cmd` | Predict, then verify, the output of five fork programs. Create a zombie (`Z` state) and reap it. |
| 7-L2 | **Race condition and fix** | Must | 0.15 | pthreads, `-fsanitize=thread` | The unsynchronised counter fails, and TSan reports the race. Fixed with a mutex and with atomics, with timing compared. |
| 7-L3 | **Bounded buffer** | Must | 0.2 | pthreads (semaphores and condvars) | 3 producers and 2 consumers, 10K items, the checksum matches, no deadlock under `stress`. |
| 7-L4 | **Deadlock on purpose** | Should | 0.1 | pthreads + gdb `thread apply all bt` | Students see two threads blocked in `__lll_lock_wait`, then fix it by lock ordering. |
| 7-L5 | **Page faults and COW** | Should | 0.1 | `/usr/bin/time -v`, `perf stat -e page-faults` | Minor faults rise with first-touch of a 100 MB malloc. Observe COW after fork with a write loop. |
| 7-L6 | **TCP echo client/server in C** | Must | 0.25 | gcc, `nc`, `ss -tanp`, Wireshark on `lo` | Echo works. The 3-way handshake, FIN exchange and TIME_WAIT are seen in `ss` and Wireshark. |
| 7-L7 | **Message framing** | Must | 0.1 | Extend 7-L6 with a length prefix | Three messages are sent and three are received intact, even when the network coalesces them (test with `tc qdisc add dev lo root netem delay 50ms`). |
| 7-L8 | **epoll TCP server (flagship lab)** | Must | 0.5 | gcc, `epoll`, the book's load-generator source | Handles 5,000+ concurrent connections on a laptop (raise `ulimit -n`). Students fill in the comparison table against thread-per-connection and `select`. ET mode with correct `EAGAIN` draining. |
| 7-L9 | **UDP and broadcast** | Optional | — | C | UDP echo, then `SO_BROADCAST` discovery on the LAN. |
| 7-L10 | **Watch the stack** | Should | 0.15 | `/proc/interrupts`, `/proc/net/softnet_stat`, `ethtool -S`, `bpftrace` | A table of IRQ counts before and after `iperf3`. A bpftrace one-liner counts `tcp_v4_rcv` calls per process. |
| 7-L11 | **Network namespaces + veth** | Should | 0.1 | `ip netns`, `ip link add veth` | Run the epoll server in ns1 and the client in ns2, showing that sockets cross a virtual link. Links to Pillar 5 overlays. |
| 7-L12 | **Mini allocator** | Optional | — | C | First-fit malloc/free with coalescing over a static arena, validated by a randomised test harness. |

## 7.4 Company-tag matrix (Pillar 7)

| Topic | CSCO | QCOM | GOOG | MSFT | AMZN | JNPR | ANET | NOK | AVGO |
|---|---|---|---|---|---|---|---|---|---|
| Process vs thread, fork | ● | ● | ● | ● | ◐ | ● | ● | ● | ● |
| Scheduling | ◐ | ● | ◐ | ◐ | ○ | ◐ | ◐ | ◐ | ◐ |
| Mutex/semaphore/spinlock/condvar | ● | ● | ● | ● | ◐ | ● | ● | ● | ● |
| Deadlock / Coffman / Banker's | ● | ● | ◐ | ◐ | ○ | ● | ◐ | ◐ | ◐ |
| Virtual memory, paging, TLB | ● | ● | ● | ● | ○ | ● | ● | ◐ | ● |
| Stack/heap, padding, allocator design | ● | ● | ◐ | ◐ | ○ | ● | ● | ◐ | ● |
| Interrupts, ISR, polling, DMA | ● | ● | ○ | ◐ | ○ | ● | ● | ● | ● |
| IPC and signals | ● | ◐ | ◐ | ◐ | ○ | ● | ◐ | ◐ | ◐ |
| Socket API (TCP/UDP) | ● | ◐ | ● | ● | ● | ● | ● | ● | ◐ |
| select/poll/epoll | ● | ◐ | ● | ◐ | ◐ | ● | ● | ● | ◐ |
| Linux stack: sk_buff, NAPI, XDP | ● | ● | ◐ | ◐ | ◐ | ● | ● | ● | ● |
| Embedded C: volatile, endianness, bits, lock-free | ● | ● | ○ | ○ | ○ | ● | ● | ◐ | ● |

## 7.5 Interview question bank (Pillar 7): 45 questions, each with a full in-book solution

1. [E] Process versus thread: what is shared and what is not? (CSCO, JNPR, QCOM, ANET)
2. [E] What happens if one thread segfaults? (CSCO)
3. [M] How many times does `hi` print? `fork(); fork(); fork(); printf("hi\n");` Then the `fork() && fork() || fork()` variant. (CSCO, JNPR, QCOM)
4. [E] What is a zombie process? What is an orphan? (CSCO, JNPR)
5. [M] What happens on a context switch? Why is a thread switch cheaper? (CSCO, QCOM)
6. [M] Compute the average waiting time under RR with q = 2 for a given set of processes. (QCOM, CSCO campus tests)
7. [M] What is starvation? How does ageing fix it? (QCOM)
8. [E] What is a race condition and a critical section? (all)
9. [M] Mutex versus binary semaphore. When would you use each? (JNPR, CSCO, QCOM)
10. [M] Mutex versus spinlock. Which is used in an interrupt handler, and why? (QCOM, AVGO, CSCO)
11. [H] Implement a counting semaphore using a mutex and a condition variable. (JNPR, ANET)
12. [H] Implement producer-consumer with a bounded buffer. Explain why the wait uses a `while` loop. (JNPR, CSCO, GOOG)
13. [M] What are the four conditions for deadlock? How do you prevent each? (CSCO, JNPR)
14. [H] Run the Banker's algorithm on a given matrix. Is the state safe? (QCOM, CSCO written tests)
15. [M] What is priority inversion? Explain priority inheritance using the Mars Pathfinder case. (QCOM, CSCO)
16. [M] Readers-writers problem: give a writer-preferring solution. (ANET, JNPR)
17. [E] What is virtual memory and why is it needed? (CSCO, JNPR)
18. [M] Explain paging, the page table and the TLB. What happens on a TLB miss and on a page fault? (CSCO, QCOM, ANET)
19. [M] Compute the page-fault count for LRU with 3 frames on a given reference string. (QCOM)
20. [M] What is Bélády's anomaly? (QCOM)
21. [M] What is copy-on-write and how does `fork()` use it? (CSCO, GOOG)
22. [E] Stack versus heap: which is faster to allocate, and why? (ANET, QCOM)
23. [M] What is `sizeof` this struct, and how do you reduce it? (ANET, QCOM, CSCO)
24. [H] Design a memory allocator (malloc/free) for an embedded system with no OS. (ANET, QCOM, AVGO)
25. [M] What is an interrupt? Describe the steps from device signal to ISR return. (QCOM, CSCO, JNPR)
26. [M] Top half versus bottom half. Why can't you sleep in an ISR? (QCOM, AVGO)
27. [M] Polling versus interrupts: when is polling better? (CSCO, QCOM)
28. [E] What is DMA? (QCOM, AVGO)
29. [M] Name the IPC mechanisms. Which is fastest and why? (CSCO, JNPR)
30. [M] What is `volatile`? Give a firmware example. Does it make code thread-safe? (QCOM, ANET)
31. [E] Write a function that detects the machine's endianness. (QCOM, ANET, CSCO)
32. [E] Explain the TCP server socket call sequence. What does `listen()`'s backlog mean? (CSCO, JNPR, ANET, GOOG)
33. [M] Why do we need `htons` and `htonl`? (CSCO, JNPR)
34. [M] Why can `recv()` return fewer bytes than were sent? How do you frame messages over TCP? (GOOG, ANET, CSCO)
35. [M] What is `TIME_WAIT`, who enters it, and why does `bind` fail with `EADDRINUSE` after a restart? (CSCO, GOOG, ANET)
36. [M] `select` versus `poll` versus `epoll`. (CSCO, JNPR, ANET, GOOG)
37. [H] Level-triggered versus edge-triggered epoll. What bug do you get with ET on a blocking socket? (ANET, GOOG)
38. [H] Design a server handling 100K concurrent connections: the threading model, I/O model and kernel tuning. (GOOG, CSCO, AMZN)
39. [H] How does a packet travel from the NIC to a user-space application in Linux? (CSCO, JNPR, ANET, NOK, AVGO)
40. [M] What is an `sk_buff`? Explain `skb_push` and `skb_pull`. (JNPR, ANET, AVGO)
41. [M] What is NAPI and why was it introduced? (QCOM, CSCO, AVGO)
42. [H] What are XDP and DPDK, and how do they differ from the normal kernel path? (CSCO, NOK, GOOG)
43. [H] Implement a lock-free single-producer single-consumer ring buffer. (ANET, AVGO, QCOM)
44. [M] What happens when a client calls `connect()` to a port with no listener? *(RST, then ECONNREFUSED.)* And when the server's accept queue is full? (GOOG, CSCO)
45. [X] Explain the thundering-herd problem with `accept()` and epoll, and its mitigations (`EPOLLEXCLUSIVE`, `SO_REUSEPORT`). (GOOG, ANET)

## 7.6 Trap boxes (Pillar 7 consolidated)

1. A binary semaphore is not a mutex. The difference is ownership.
2. Use `while`, not `if`, around `pthread_cond_wait`.
3. Never sleep in an ISR. Use spinlocks and `GFP_ATOMIC`.
4. `volatile` is not a synchronisation primitive.
5. One `send` is not one `recv`. TCP is a byte stream.
6. Edge-triggered epoll needs non-blocking sockets and draining to `EAGAIN`.
7. `select` is limited to fd < 1024 (FD_SETSIZE).
8. `TIME_WAIT` is on the side that closes actively, and it is intentional.
9. A thread crash kills the whole process.
10. stdio buffering duplicates output across `fork()`.
11. A cycle in the RAG implies deadlock only for single-instance resources.
12. NAPI still uses interrupts, just not one per packet.
13. Writing to a closed socket raises SIGPIPE, which by default kills the process.
14. `malloc` returns virtual memory; physical pages come on first touch.

## 7.7 Cheat-sheet contents (one double-sided A4 page)

- **Side A (OS):**
  - Process states diagram.
  - fork rule (2ⁿ).
  - Thread shared/private table.
  - Scheduling formulae (TAT = CT − AT; WT = TAT − BT).
  - Primitive comparison table.
  - The four Coffman conditions with one prevention each.
  - Banker's steps.
  - VA split formula.
  - EAT formula.
  - Replacement algorithms one-liners.
  - Struct alignment rules.
  - Top/bottom half table.
  - IPC table.
- **Side B (sockets and the stack):**
  - TCP server/client call sequence with matching TCP states.
  - `sockaddr_in` fields.
  - The `htons` family.
  - The `readn`/`writen` idiom.
  - Common errno values (EAGAIN, EINTR, ECONNREFUSED, ECONNRESET, EADDRINUSE, EPIPE).
  - Socket options (SO_REUSEADDR, SO_REUSEPORT, TCP_NODELAY, SO_KEEPALIVE, SO_RCVBUF).
  - The epoll skeleton in 12 lines.
  - LT/ET rules.
  - The receive path in 9 boxes.
  - The `sk_buff` pointer diagram.
  - Tuning knobs (`somaxconn`, `tcp_max_syn_backlog`, `netdev_budget`, `ulimit -n`).

## 7.8 Mini-project (Pillar 7): "TinyRelay: an epoll chat and packet-relay server"

- **Brief:** A single-threaded, then multi-threaded, C server.
  1. epoll edge-triggered loop with non-blocking sockets and length-prefixed framing.
  2. Chat rooms: `JOIN`, `MSG` and `LEAVE` commands, with fan-out to members.
  3. A per-client output buffer with back-pressure: register `EPOLLOUT` only when the buffer is non-empty.
  4. A thread pool for "slow" commands, using a mutex/condvar work queue, with results handed back to the event loop via an `eventfd`.
  5. Stats endpoint over UDP: connected clients, messages per second, bytes in and out.
  6. Graceful shutdown on SIGINT using `signalfd`.
  7. Load test with the book's client generator at 1,000 and 5,000 connections, reporting latency percentiles.
  8. TSan- and ASan-clean builds and a Makefile.
- **Stretch:** IPv6 support via `getaddrinfo`. `SO_REUSEPORT` sharding across N worker processes. An XDP program (in C, loaded with `ip link set dev ... xdp obj`) that drops packets from a blocklisted IP before they reach the server.
- **Interview pay-off:** A complete, defensible answer to "design a scalable server", "explain epoll" and "how did you test concurrency?" at CSCO, JNPR, ANET, GOOG and NOK.

## 7.9 Sources (Pillar 7) (author research only; readers never need them)

Researched during planning:

- Juniper interview experiences (mutex, semaphore, threads, sockets):
  - https://www.glassdoor.co.in/Interview/Juniper-Networks-Interview-E7224-RVW40275047.htm
  - https://www.glassdoor.co.uk/Interview/Juniper-Networks-Interview-E7224-RVW1682205.htm
  - https://www.geeksforgeeks.org/juniper-interview-experience-set-3-campus/
- Cisco interview experiences (process vs thread, deadlock, interrupts, polling):
  - https://www.geeksforgeeks.org/?p=131791
  - https://www.jointaro.com/interviews/companies/cisco/experiences/software-engineer-ottawa-on-april-1-2022-accepted-offer-positive-6f4afa8e/
  - https://www.glassdoor.co.in/Interview/Cisco-Interview-E1425-RVW503316.htm
- Arista interview experiences (C, OS, struct padding, memory allocator):
  - https://www.interviewquery.com/interview-guides/arista-networks-software-engineer
  - https://leetcode.com/discuss/interview-experience/6078309/Arista-Networks-or-SWE-1-or-India-or-Accepted/
  - https://www.glassdoor.com/Interview/Arista-Networks-Interview-E295128-RVW33699587.htm
- Qualcomm (C storage classes, bit manipulation, memory management): https://www.glassdoor.co.in/Interview/Qualcomm-Firmware-Engineer-Interview-Questions-EI_IE640.0,8_KO9,26.htm
- Linux receive path overviews (secondary; cross-check against kernel documentation):
  - https://www.socallinuxexpo.org/sites/default/files/presentations/A%20deep%20dive%20into%20Linux%20Networking%20%282%29_0.pdf
  - https://site-aer.pages.dev/blog/received-packet-journey-nic-to-recv
  - https://besthub.dev/articles/how-linux-receives-network-packets-from-nic-interrupts-to-recvfrom-4625974bb34d
  - https://people.cs.nycu.edu.tw/~ttyeh/course/2024_Spring/IOC5226/slide/lecture-22.pdf

Primary references for authors (to verify facts):

- Linux kernel networking documentation (NAPI, sk_buff, XDP): https://docs.kernel.org/networking/napi.html, https://docs.kernel.org/networking/skbuff.html, https://docs.kernel.org/networking/scaling.html
- `epoll(7)`, `socket(7)`, `tcp(7)` man pages: https://man7.org/linux/man-pages/man7/epoll.7.html
- Arpaci-Dusseau, *Operating Systems: Three Easy Pieces* (free online): https://pages.cs.wisc.edu/~remzi/OSTEP/
- Silberschatz, Galvin and Gagne, *Operating System Concepts* (for the Banker's and scheduling conventions used in Indian university syllabi).
- W. Richard Stevens, *UNIX Network Programming, Vol. 1*.
- Beej's Guide to Network Programming: https://beej.us/guide/bgnet/
- Dan Kegel, "The C10K problem": http://www.kegel.com/c10k.html
- DPDK documentation: https://doc.dpdk.org/guides/

## 7.10 End-of-chapter pack (per 0A.4)

- Short notes, ordered as section 7.2.x.
- One-page revision sheet, built from 7.7.
- 70 flashcards.
- Solutions to all 45 questions in 7.5, in the five-part format.
- Five extended whiteboard problems (listed in 0A.4).
- A 20-question self-test with an answer key.

---

*End of plan for Pillars 5–7.*
