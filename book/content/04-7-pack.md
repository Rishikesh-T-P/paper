::: {.p4}

::: pack
## Problem Set {#ps4}

Each solution opens with the 30-second answer. Tags give the companies that report the topic, the round, the difficulty (■□□ to ■■■) and the evidence: S for a specific reported question, T for a reported topic with our wording.

::: problems
::: q
### Q4.1 Access vs trunk port. What is the native VLAN, and what happens on a mismatch?
[CISCO · JUNIPER · TECH-1 · ■□□ · T]{.meta}

[30-second answer: an access port carries one VLAN untagged; a trunk carries many VLANs with 802.1Q tags; the native VLAN is the one VLAN sent untagged on a trunk, and if the two ends disagree, frames cross from one VLAN into another.]{.short}

**Answer.** A frame of VLAN 1 sent untagged by a switch whose native VLAN is 1 is read by a neighbour with native VLAN 99 as VLAN 99. Hence traffic leaks between VLANs and spanning tree on that VLAN may block the port as inconsistent. CDP prints a mismatch message. **Mistakes.** Treating the message as harmless; leaving the native VLAN as VLAN 1 (set an unused VLAN on both ends).
:::

::: q
### Q4.2 How many VLANs does 802.1Q support, and why 4094?
[CISCO · ARISTA · TECH-1 · ■□□ · T]{.meta}

[30-second answer: the VLAN ID is 12 bits, giving 4096 values; 0 (priority tag, no VLAN) and 4095 (reserved) are unusable, leaving 4094.]{.short}

**Answer.** On Cisco, 1002 to 1005 are legacy and 1006 to 4094 need extended-range support. Beyond 4094 VLANs, VXLAN's 24-bit VNI is used ([§5.5](#s5-5){.ref}).
:::

::: q
### Q4.3 Explain inter-VLAN routing with ROAS and with SVIs. Which scales better?
[CISCO · TECH-1 · ■■□ · T]{.meta}

[30-second answer: router-on-a-stick uses one trunk and a sub-interface per VLAN on a router, with each packet crossing the link twice; an SVI is a virtual Layer 3 interface on a Layer 3 switch, routed in hardware; SVIs scale better.]{.short}

**Answer.** ROAS is bounded by one link and the router's forwarding rate; it suits small branches. SVIs need `ip routing`, one `interface Vlan N` per VLAN, and the VLAN must exist and have an active port for the SVI to come up. The packet walk is in §4.2 ([Figure 4.6](#s4-2){.ref}). **Follow-up.** Routed ports (`no switchport`) are used on links between Layer 3 switches.
:::

::: q
### Q4.4 Why is DTP a security risk? How do you harden trunk ports?
[CISCO · TECH-1 · ■■□ · T]{.meta}

[30-second answer: DTP lets a port become a trunk by negotiation, so an attacker who sends DTP frames can obtain a trunk and see all VLANs; configure every port statically and disable negotiation.]{.short}

**Answer.** Access ports: `switchport mode access`, `switchport nonegotiate`, an unused native VLAN, `spanning-tree portfast` with BPDU guard, and shut unused ports into a parking VLAN. Trunks: `switchport mode trunk`, `nonegotiate`, an explicit allowed list, native VLAN not 1. Double-tagging and its defence are in [§9.5](#s9-5){.ref}.
:::

::: q
### Q4.5 Walk through the STP root election and port roles for the triangle.
[CISCO · JUNIPER · ARISTA · TECH-1 · ■■□ · S]{.meta}

[30-second answer: lowest bridge ID wins root (SW1, lowest MAC at equal priority); each other switch takes its lowest-cost port to the root as the root port; per segment the lowest-cost, then lowest-BID sender is designated; the remaining port on SW3 blocks.]{.short}

**Answer.** The full three-part trace (default priorities, SW3 at 4096, parallel links) is the worked example of §4.3 ([Figure 4.9](#s4-3){.ref}); learn the four-step order rather than the answer. **Mistake.** Giving the root bridge a root port.
:::

::: q
### Q4.6 Why must the STP priority be a multiple of 4096?
[CISCO · TECH-1 · ■■□ · T]{.meta}

[30-second answer: the 16-bit priority field is split into a 4-bit priority and a 12-bit VLAN ID (the extended system ID), so only the top four bits can be set.]{.short}

**Answer.** The configurable values are 0, 4096, ..., 61440. The VLAN ID is added to the configured value, hence VLAN 10 at default priority displays 32778.
:::

::: q
### Q4.7 802.1D vs RSTP: port states and roles. Why does RSTP converge in under a second?
[CISCO · NOKIA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: 802.1D has five states (blocking, listening, learning, forwarding, disabled) and timers of up to 50 s; RSTP has three (discarding, learning, forwarding) and negotiates with proposal and agreement instead of waiting for timers.]{.short}

**Answer.** Roles in RSTP are root, designated, alternate and backup. An alternate port is a precomputed path to the root and takes over immediately; a new link is handled by a sync handshake, and edge ports forward at once. Failure is detected after three missed hellos (6 s), or at once on loss of link. **Mistake.** Saying RSTP removes the need for the root election; it keeps it.
:::

::: q
### Q4.8 PortFast and BPDU Guard, Root Guard, Loop Guard: where does each go?
[CISCO · ARISTA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: PortFast with BPDU Guard on access ports facing hosts; Root Guard on distribution ports facing access switches that must never be root; Loop Guard on non-designated uplinks.]{.short}

**Answer.** BPDU Guard shuts an edge port if a BPDU arrives. Root Guard puts a port in root-inconsistent state if it hears a superior BPDU and recovers when they stop. Loop Guard stops a blocking port from forwarding when BPDUs vanish (a unidirectional link). UDLD detects the unidirectional fibre itself. **Mistake.** PortFast on a switch-facing port invites loops.
:::

::: q
### Q4.9 Scenario: the network freezes every few minutes, switch CPU is at 100% and MACs flap between ports. Diagnose and fix.
[CISCO · AMAZON · TECH-2 · ■■■ · S]{.meta}

[30-second answer: a Layer 2 loop or storm; find the loop port from the flapping MAC and the interface counters, shut it, then fix the cause (a missing or broken spanning tree) and add guards.]{.short}

**Approach.** (i) `show processes cpu` confirms the load; (ii) `show mac address-table | include <mac>` repeated shows the same MAC on alternating ports; (iii) `show interfaces | include broadcasts` or `show spanning-tree detail | include occurr|from` shows the port with the highest broadcast rate and the topology-change source. **Fix.** Shut that port. Common causes: an unmanaged switch looped by a patch cable, STP disabled or a BPDU filter, an unexpected PortFast, an EtherChannel mismatch. Then enable BPDU Guard, `storm-control broadcast level 1`, Loop Guard, and errdisable auto-recovery.
:::

::: q
### Q4.10 LACP active/passive vs PAgP vs `on`: which combinations form a bundle?
[CISCO · ARISTA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: LACP forms with active-active and active-passive, but not passive-passive; PAgP with desirable-desirable and desirable-auto; `on` only with `on`; the protocols do not mix.]{.short}

**Answer.** See the matrix in §4.3. `on` does not negotiate, so a mismatch can form a one-sided bundle and a loop. Prefer LACP: it is the open standard and detects a failed partner.
:::

::: q
### Q4.11 An EtherChannel shows member ports as suspended (s). Give five causes.
[CISCO · JUNIPER · TECH-2 · ■■■ · T]{.meta}

[30-second answer: the member's settings disagree with the bundle or the partner: speed or duplex, trunk or VLAN configuration, channel mode or protocol, no LACP reply, and differing spanning-tree settings.]{.short}

**Answer.** (i) Speed or duplex mismatch; (ii) trunk mode, allowed list or native VLAN differs between members; (iii) LACP partner silent, or both sides passive, or `on` against LACP; (iv) different LACP system or port priority limits (more than eight members); (v) different STP port cost or PortFast settings. Check with `show etherchannel summary` and `show etherchannel detail`. LACP suspends a member that hears no PDUs so that a loop cannot form.
:::

::: q
### Q4.12 How does MLAG or vPC avoid STP blocking? What is the peer link for?
[ARISTA · CISCO · AMAZON · TECH-2 · ■■■ · T]{.meta}

[30-second answer: two physical switches present one logical switch to the downstream device, which bundles its uplinks across both; with no loop in the logical topology nothing blocks; the peer link synchronises state and carries traffic when needed.]{.short}

**Answer.** The peers share MAC and ARP tables over the peer link, and a keepalive on a separate path detects a split-brain. Orphan ports (single-attached) use the peer link if the other peer holds the path. Internals in [§5.3](#s5-3){.ref}.
:::

::: q
### Q4.13 What is administrative distance? Give the values for connected, static, eBGP, EIGRP, OSPF, RIP and iBGP.
[CISCO · AMAZON · TECH-1 · ■□□ · S]{.meta}

[30-second answer: AD is a local trust rating of a routing source, from 0 to 255, used to choose between sources of the same prefix; connected 0, static 1, eBGP 20, EIGRP 90, OSPF 110, RIP 120, iBGP 200.]{.short}

**Answer.** Full table in §4.4. AD is not carried in any protocol; it is configurable per route or per protocol (`distance`).
:::

::: q
### Q4.14 Order the routing decision. Solve the routing-table puzzle.
[CISCO · AMAZON · JUNIPER · TECH-1 · ■■□ · S]{.meta}

[30-second answer: longest prefix first, then lowest AD, then lowest metric, then equal-cost sharing.]{.short}

**Answer.** The puzzle is solved in §4.4: 10.1.1.9 goes to the static /24, 10.1.5.5 to the EIGRP /16 and 10.200.0.1 to the RIP /8. **Twist.** Add a static 10.1.0.0/16 [1/0]: it replaces the EIGRP route (AD 1 against 90) and 10.1.5.5 follows it.
:::

::: q
### Q4.15 What is a floating static route? Configure a backup default route.
[CISCO · TECH-1 · ■■□ · T]{.meta}

[30-second answer: a static route with an AD higher than the primary's, which enters the table only when the primary route disappears.]{.short}

**Answer.** `ip route 0.0.0.0 0.0.0.0 203.0.113.9 250` as backup to an OSPF default (AD 110). **Mistake.** It reacts to the route vanishing, not to a broken path behind an up link; tie it to an IP SLA track object (§4.14).
:::

::: q
### Q4.16 Explain RIB, FIB and TCAM. How does a hardware switch do longest-prefix match at line rate?
[BROADCOM · ARISTA · JUNIPER · TECH-2 · ■■■ · T]{.meta}

[30-second answer: the RIB holds all routes the protocols offer; the FIB is the best-route set compiled for forwarding; hardware stores it in TCAM, which matches all entries in parallel, ordered so the longest prefix wins.]{.short}

**Answer.** Detail is in [§5.2](#s5-2){.ref}. A ternary CAM stores each prefix with a mask, so a lookup is a single cycle; entries are sorted by prefix length. Large tables use algorithmic LPM in SRAM (tries) because TCAM is costly and power-hungry. The algorithm is in [§1.9](#s1-9){.ref}.
:::

::: q
### Q4.17 List the OSPF neighbour states in order.
[CISCO · JUNIPER · NOKIA · TECH-1 · ■□□ · S]{.meta}

[30-second answer: Down, (Attempt), Init, 2-Way, ExStart, Exchange, Loading, Full.]{.short}

**Answer.** Figure 4.16 shows the packet that causes each step: Hello (Init), a Hello listing our ID (2-Way), DBD master election (ExStart), DBD summaries (Exchange), LSR and LSU (Loading). Attempt applies only to non-broadcast networks.
:::

::: q
### Q4.18 Two routers are stuck in EXSTART. Why? And in INIT, or 2-WAY?
[CISCO · AMAZON · JUNIPER · TECH-1 · ■■□ · S]{.meta}

[30-second answer: EXSTART/EXCHANGE: MTU mismatch, or a duplicate router ID or blocked unicast; INIT: hellos are heard in one direction only; 2-WAY: normal between two DROTHERs, a fault otherwise.]{.short}

**Answer.** Evidence: `show ip interface` for MTU, `debug ip ospf adj` ("smaller interface MTU"). INIT: an ACL or a multicast filter blocks one direction, or one side's hello lacks our ID. 2-Way on a point-to-point link points at a network-type mismatch.
:::

::: q
### Q4.19 List the parameters that must match for an OSPF adjacency.
[CISCO · NOKIA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: area ID, subnet and mask, hello and dead timers, authentication, stub-area flags, MTU, compatible network type; router IDs must differ.]{.short}
:::

::: q
### Q4.20 How is the DR elected? Is it pre-emptive? Why have a DR?
[CISCO · JUNIPER · TECH-1 · ■■□ · T]{.meta}

[30-second answer: highest interface priority, then highest router ID; priority 0 is ineligible; it is not pre-emptive; the DR limits adjacencies to n-1 and floods each LSA once.]{.short}

**Answer.** Without a DR, a segment of n routers needs n(n-1)/2 adjacencies. Worked example in §4.5. Force a change by setting priorities and clearing the process.
:::

::: q
### Q4.21 Explain LSA types 1, 2, 3, 4, 5, 7: who generates each and its scope.
[CISCO · JUNIPER · NOKIA · AMAZON · TECH-1 · ■■□ · S]{.meta}

[30-second answer: 1 router (every router, area); 2 network (DR, area); 3 summary (ABR, other areas); 4 ASBR summary (ABR, other areas); 5 external (ASBR, domain-wide except stubs); 7 NSSA external (ASBR in NSSA, converted to 5 by the ABR).]{.short}

**Answer.** Table and scope map in §4.5. Mention that type 3 is distance-vector-like (prefix and cost only), which is why every area must hang off area 0.
:::

::: q
### Q4.22 Stub vs totally stubby vs NSSA: which LSAs are blocked?
[CISCO · JUNIPER · TECH-1 · ■■□ · T]{.meta}

[30-second answer: stub blocks 4 and 5; totally stubby blocks 3, 4 and 5 (one default type 3); NSSA blocks 4 and 5 but allows 7; totally NSSA also blocks 3.]{.short}

**Answer.** Use a stub area where no ASBR exists in the area and routers are small; an NSSA where a local ASBR must exist, for example a branch connected to a partner network.
:::

::: q
### Q4.23 Why must all areas connect to area 0? What is a virtual link?
[CISCO · TECH-1 · ■■□ · T]{.meta}

[30-second answer: inter-area routing passes through the backbone as prefix-and-cost summaries, so a non-backbone path could loop; a virtual link tunnels area 0 connectivity across a transit area.]{.short}

**Answer.** `area 1 virtual-link <ABR RID>` on both ABRs. It is a repair, not a design; a discontiguous backbone is better fixed physically.
:::

::: q
### Q4.24 Why do 1 Gb/s and 10 Gb/s links have the same OSPF cost by default? How do you fix it?
[CISCO · AMAZON · TECH-1 · ■■□ · T]{.meta}

[30-second answer: cost = 100 Mb/s divided by bandwidth, with a minimum of 1, so both are 1; set `auto-cost reference-bandwidth` to a higher value on every router.]{.short}

**Answer.** With 100000 (100 Gb/s), 1G costs 100 and 10G costs 10. Alternatively set `ip ospf cost` per link. **Mistake.** Changing it on only some routers, which produces inconsistent metrics.
:::

::: q
### Q4.25 E1 vs E2 external routes: which is preferred, and when does it matter?
[CISCO · JUNIPER · TECH-2 · ■■■ · T]{.meta}

[30-second answer: E2 (default) keeps the external cost unchanged; E1 adds the internal cost to the ASBR; an E1 route is preferred over E2 for the same prefix, and E1 matters when several ASBRs advertise the same prefix.]{.short}

**Answer.** With E2, the nearest exit is chosen only as a tie-break (the lowest internal cost to the ASBR, the forwarding address). With E1 total cost is compared, so the closer ASBR wins unless the external costs differ enough.
:::

::: q
### Q4.26 Scenario: 200 customer routes in area 3 flap every few minutes and SPF runs network-wide. How do you contain it?
[CISCO · TECH-2 · ■■■ · S]{.meta}

[30-second answer: summarise at the ABR so the flaps never leave area 3, make area 3 stub or totally stubby, throttle SPF and LSA generation, and fix the root cause.]{.short}

**Approach.** Type 1 and 2 LSAs flood within the area, so only area 3's routers recompute; but each flapping prefix also generates a type 3 into area 0 and beyond. `area 3 range 10.3.0.0 255.255.0.0` hides detail: while any prefix inside is up, the summary stays. Then `timers throttle spf 50 200 5000`, `timers throttle lsa all 50 200 5000`, BFD for failure detection and interface dampening (`dampening` on the interface) on the unstable links. **Mistake.** Summarising a range that has holes, which attracts traffic for addresses that do not exist; add a Null0 route.
:::

::: q
### Q4.27 OSPF vs IS-IS: why do many providers and data centres prefer IS-IS?
[JUNIPER · NOKIA · GOOGLE · TECH-2 · ■■■ · T]{.meta}

[30-second answer: IS-IS runs directly over Layer 2 rather than IP, uses TLVs that extend easily (IPv4, IPv6, segment routing) with one protocol, and scales through a simple two-level hierarchy.]{.short}

**Answer.** Differences: OSPF has areas that attach to a backbone through ABRs, IS-IS has areas per router and a contiguous Level 2 backbone; OSPFv2 and v3 are separate protocols, IS-IS carries both families. Both are link-state and use Dijkstra, so say which one you have configured and why.
:::
:::
:::

:::
