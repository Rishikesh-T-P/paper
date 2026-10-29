::: {.p5}

::: pack
## Problem Set {#ps5}

Every interview question of this pillar is solved once, here, in the compact template: a 30-second answer first, then the approach, answer, follow-ups and common mistakes where they apply. The tags give the companies that report the topic, the round, the difficulty (■□□ easy, ■■□ medium, ■■■ hard) and the evidence: **S** if candidates report this specific question, **T** if the topic is reported and the wording is ours. The first twenty questions cover the fabric, the overlay, SDN and the first part of the internals; the rest follow on the next pages. Section numbers refer to this chapter.

::: problems

::: q
### Q5.1 What is spine-leaf? Why is every leaf-to-leaf path the same length?
[ARISTA · JUNIPER · GOOGLE · TECH-1 · ■□□ · S]{.meta}

[30-second answer: a two-tier fabric in which every leaf (rack) switch connects to every spine switch and nothing else; any leaf-to-leaf path is leaf, spine, leaf, so all paths have the same length and the same cost, and there are as many of them as there are spines.]{.short}

**Answer.** Servers attach to leaves; leaves have no links to each other, and spines have none either. A path between two leaves must therefore leave through one uplink to a spine and return through that spine's link to the destination: three switches and two links, whichever spine. Equal length makes the paths equal-cost, so ECMP (§5.3) can use all of them, and latency is the same for every pair of racks. **Follow-ups.** For more than one spine's port count of leaves, add a super-spine tier (five switches between racks, §5.2). **Mistake.** Linking spines to each other adds paths of different length and breaks the uniformity.
:::

::: q
### Q5.2 Define oversubscription. Compute it for 48 × 10G down and 6 × 40G up.
[ARISTA · MICROSOFT · TECH-1 · ■□□ · S]{.meta}

[30-second answer: oversubscription is the ratio of the bandwidth a switch offers to its servers to the bandwidth it has towards the rest of the fabric; here 480 ÷ 240 = 2 : 1.]{.short}

**Answer.** Down: 48 × 10 = 480 Gb/s. Up: 6 × 40 = 240 Gb/s. Ratio 480 ÷ 240 = 2 : 1, so if every server sends at once each receives half its line rate across the fabric. Traffic inside the rack never uses the uplinks. **Follow-up.** For 1 : 1 use 12 uplinks of 40G or reduce the server ports to 24. **Mistake.** Counting the uplinks of one spine only, or mixing gigabits with gigabytes.
:::

::: q
### Q5.3 What is east-west traffic, and what is north-south?
[ALL · TECH-1 · ■□□ · T]{.meta}

[30-second answer: north-south crosses the data-centre boundary (clients and the Internet); east-west runs between servers inside it. East-west dominates in modern data centres, which is why the fabric is built for uniform server-to-server bandwidth.]{.short}

**Answer.** One user request becomes many internal calls, and replication, storage and analytics add bulk transfers, so internal traffic is a multiple of external traffic (§5.1). Hence the design goals: equal paths, high bisection bandwidth and no blocked links. **Follow-up.** Name a north-south device (the border leaf, the firewall or the edge load balancer).
:::

::: q
### Q5.4 Why do large data centres prefer eBGP to OSPF in the underlay? Give three reasons.
[GOOGLE · MICROSOFT · ARISTA · TECH-2 · ■■□ · T]{.meta}

[30-second answer: eBGP limits the effect of a failure to the paths that used it (no network-wide flooding), gives per-neighbour policy for draining and traffic steering, and one protocol serves the fabric and the edge; the cost is an AS-number plan and the need for BFD.]{.short}

**Answer.** (i) *Scope.* A link-state protocol floods each change to every router and each recomputes the shortest-path tree; BGP sends updates only to neighbours that need them. (ii) *Policy.* Communities and route maps let an operator drain a switch, steer traffic or filter by tag; OSPF has little equivalent. (iii) *Simplicity.* One protocol runs from the server to the border, with AS-path loop prevention and no redistribution between an IGP and BGP. Also: it runs over TCP, with multipath and unnumbered links (§5.4). **Follow-up.** Fix its slow default timers with BFD at 300 ms × 3. **Mistake.** Claiming BGP converges faster by itself; it does not.
:::

::: q
### Q5.5 Two leaves share AS 65001. What breaks, and what are two fixes?
[ARISTA · JUNIPER · TECH-2 · ■■□ · T]{.meta}

[30-second answer: a route learnt from the other leaf carries 65001 in its AS_PATH, so the leaf discards it as a loop and the two racks cannot reach each other; fix with unique AS numbers, `allowas-in` on the leaves, or `as-override` on the spines.]{.short}

**Answer.** L1 and L2 (both 65001) exchange routes through spines in AS 65100. L2 receives L1's prefix with AS_PATH 65100 65001, sees its own AS and drops it. Fixes: (i) a unique private AS per leaf (4-byte range if the 1,023 two-byte numbers run out); (ii) `allowas-in` on the leaf, which accepts a bounded number of own-AS occurrences but weakens loop detection; (iii) `neighbor ... as-override` on the spine, which replaces the leaf's AS in the path by the spine's own. **Mistake.** Applying `allowas-in` on the spines, which are not the ones dropping the route.
:::

::: q
### Q5.6 What does ECMP hash on? Why not per packet?
[ALL · TECH-1 · ■■□ · S]{.meta}

[30-second answer: normally the 5-tuple (addresses, protocol, ports); every packet of a flow takes the same path, so a TCP stream stays in order. Per-packet balancing reorders segments and causes spurious fast retransmits.]{.short}

**Answer.** The hash is computed in hardware, with a per-device seed, and indexes the next-hop group. Some devices let you choose the fields; Linux has `fib_multipath_hash_policy` (0 addresses, 1 5-tuple, 2 inner headers). For tunnels the outer 5-tuple is the same for every packet, so the encapsulating device puts a hash of the inner flow in the outer UDP source port (§5.5). **Follow-up.** Packet spraying is acceptable only where the receiver tolerates reordering. **Mistake.** Saying ECMP "balances load"; it balances flows, statistically.
:::

::: q
### Q5.7 You see 80% of the traffic on one of four spines. List five possible causes.
[GOOGLE · AMAZON · TECH-2 · ■■■ · T]{.meta}

[30-second answer: elephant flows, hash polarisation, only one path installed (`maximum-paths`), unequal paths (different AS_PATH length or preference), or a tunnel or LAG with no entropy so that all traffic has one 5-tuple.]{.short}

**Answer.** Work from the router outward. (i) *Elephant flows:* a few large flows (backup, shuffle) land on one link; check per-flow telemetry. (ii) *Polarisation:* the same hash and seed at successive tiers (§5.3); change the seed or the fields. (iii) *Multipath not installed:* `show ip route` lists one next hop because `maximum-paths` is 1, or `multipath-relax` is missing where the neighbours' AS numbers differ (§5.4). (iv) *Not equal-cost:* a longer AS_PATH or a higher LOCAL_PREF through three spines leaves them unused. (v) *No entropy:* GRE, IPsec or VXLAN with a fixed source port gives one 5-tuple. Confirm with interface counters per spine, then with a `tcpdump` flow count. **Mistake.** Rebooting spines before reading next-hop counts.
:::

::: q
### Q5.8 Explain resilient or consistent hashing and why it matters when a spine fails.
[GOOGLE · BROADCOM · TECH-2 · ■■■ · T]{.meta}

[30-second answer: the hash selects one of many fixed buckets, and the buckets are assigned to next hops; when a next hop fails only its buckets are reassigned, so flows on healthy paths do not move.]{.short}

**Answer.** With `hash mod N`, going from N = 4 to 3 changes the index of about 75% of the flows, each of which now takes a different path, arrives out of order or hits a stateful device (a firewall, a load balancer) that has no state for it. With 16 buckets and four members, a failure reassigns 4 of 16 = 25% of the buckets, the minimum possible (Figure 5.5). When the member returns, buckets can migrate back gradually, at an idle gap of the flow, to avoid disturbing flows. **Follow-up.** The same principle at the load balancer is Maglev hashing (§5.9). **Mistake.** Assuming resilient hashing prevents all loss; flows on the failed link still need rerouting.
:::

::: q
### Q5.9 What is VXLAN? Which UDP port does it use, and how many segment identifiers are there?
[ARISTA · CISCO · NOKIA · TECH-1 · ■□□ · S]{.meta}

[30-second answer: an overlay that carries Ethernet frames inside UDP/IP between tunnel endpoints (VTEPs), on destination port 4789, with a 24-bit VNI giving 16,777,216 segments.]{.short}

**Answer.** The VTEP adds VXLAN (8 bytes), UDP, IP and Ethernet headers (§5.5); the underlay routes the outer IP packet and never sees the tenant frame. A VLAN has 12 bits (4,094 usable), a VNI 24. **Follow-up.** Name Geneve (UDP 6081) as the extensible alternative. **Mistake.** "VXLAN extends a VLAN"; it maps one to a VNI.
:::

::: q
### Q5.10 Compute the VXLAN overhead and the minimum underlay MTU for a 1,500-byte inner MTU; then for a 9,000-byte tenant MTU over an IPv6 underlay.
[ARISTA · JUNIPER · TECH-1 · ■■□ · S]{.meta}

[30-second answer: 50 bytes over IPv4 (70 over IPv6); the underlay IP MTU must be at least 1,550 for a 1,500-byte tenant MTU, and 9,070 for 9,000 over IPv6.]{.short}

**Answer.** The 1,500 case is worked in §5.5 (inner Ethernet 14 + 1,500 + VXLAN 8 + UDP 8 + IPv4 20 = 1,550). For the second, the inner frame is 9,000 + 14 = 9,014; the outer IPv6 packet adds 40 + 8 + 8, giving 9,070, so a 9,216-byte fabric MTU has room to spare. A 4-byte VLAN tag on the underlay link enlarges the *frame* but not the IP MTU. **Follow-up.** What if you cannot raise the underlay? Lower the tenant MTU and clamp the TCP MSS (§3.5). **Mistake.** Counting the inner Ethernet header twice, or forgetting it.
:::

::: q
### Q5.11 Why is the outer UDP source port of VXLAN variable?
[ARISTA · BROADCOM · TECH-2 · ■■□ · T]{.meta}

[30-second answer: so that ECMP in the underlay, which hashes the outer 5-tuple, can spread different tenant flows over different paths; the VTEP sets it to a hash of the inner headers.]{.short}

**Answer.** All frames between two VTEPs share outer source and destination addresses, protocol and destination port 4789; a fixed source port would give them a single 5-tuple and one path. The VTEP computes the port from the inner Ethernet, IP and transport fields, typically within 49152 to 65535, so one inner flow keeps one source port (no reordering) and different flows differ. It carries no meaning for the receiver. **Mistake.** Filtering on a fixed source port at a firewall; filter on the destination port.
:::

::: q
### Q5.12 What does EVPN add over flood-and-learn VXLAN?
[ARISTA · JUNIPER · NOKIA · CISCO · TECH-1 · ■■□ · S]{.meta}

[30-second answer: a BGP control plane that advertises MAC and IP reachability, so hosts are learnt from routes and not by flooding; it adds mobility, ARP suppression, multihoming, anycast gateways and integrated routing.]{.short}

**Answer.** Flood-and-learn sends unknown-unicast and broadcast to every VTEP and learns from traffic, which does not scale and converges by aging. With EVPN each leaf advertises the MACs and IPs it learnt locally (Type 2), its VNIs (Type 3) and prefixes (Type 5); other leaves install them. Consequences: (i) no flooding for known hosts, and ARP answered locally; (ii) a host move is an update with a higher sequence number; (iii) a server can attach to two leaves (Types 1 and 4); (iv) route targets give multi-tenancy. See §5.6.
:::

::: q
### Q5.13 Explain EVPN route types 2, 3 and 5, with an example of when each is sent.
[JUNIPER · NOKIA · ARISTA · TECH-2 · ■■■ · T]{.meta}

[30-second answer: Type 2 advertises a host (MAC, optionally IP) with its L2 and L3 VNIs; Type 3 advertises that a VTEP belongs to a VNI, building the flood list; Type 5 advertises an IP prefix, used for subnets and external routes.]{.short}

**Answer.** *Type 2:* host 10.1.10.11 with MAC aa:aa:aa:aa:aa:11 appears on L1; L1 sends RD, ESI, MAC, IP, Label1 = 10010 (L2VNI), Label2 = 50001 (L3VNI) and RTs. *Type 3:* VNI 10010 is configured on L3; L3 sends its VTEP address with that VNI, so L1 adds L3 to the replication list for BUM frames of 10010. *Type 5:* the border leaf learns 0.0.0.0/0 from BR1 and sends it into VRF CAMPUS with the L3VNI 50001 and its router MAC. A Type-2 route follows its host; a Type-5 route carries no MAC. **Mistake.** Mixing the two RTs of Type 2 (L2 and L3) or importing one RT in two tenants.
:::

::: q
### Q5.14 Symmetric versus asymmetric IRB: trade-offs in scale and configuration.
[ARISTA · CISCO · TECH-2 · ■■■ · T]{.meta}

[30-second answer: in symmetric IRB both leaves route and the packet crosses the fabric in a shared L3VNI, so a leaf needs only its own subnets; in asymmetric IRB only the ingress leaf routes and every leaf needs every VNI, which does not scale.]{.short}

**Answer.**

| | Symmetric | Asymmetric |
|---|---|---|
| Who routes | ingress and egress leaf | ingress leaf only |
| VNI on the wire | L3VNI of the VRF, both directions | destination's L2VNI, return uses the source's |
| State per leaf | local subnets plus the L3VNI | every VNI, even without hosts |
| Configuration | one L3VNI per VRF, router MAC | simple, but a VNI on every leaf |
| Path | the same both ways | different VNIs each way |

Production fabrics use symmetric IRB. **Mistake.** Saying the packet is routed "twice" as if it were a drawback; it is the cheaper design.
:::

::: q
### Q5.15 A VM moves between racks and traffic blackholes for 30 seconds. Which EVPN mechanisms should have prevented that?
[ARISTA · MICROSOFT · TECH-2 · ■■■ · T]{.meta}

[30-second answer: the new leaf must learn the MAC quickly (a gratuitous ARP or RARP from the hypervisor), advertise it with a higher MAC-mobility sequence number, and the old leaf must withdraw; a 30-second gap points to a missing announcement or stale caches.]{.short}

**Answer.** Check in order. (i) Did the hypervisor send the GARP/RARP on arrival? Without it the leaf learns only from the first data packet. (ii) Does the new leaf's Type-2 route carry sequence 1 (`show bgp l2vpn evpn route type macip`)? (iii) Has the old leaf deleted its local entry and withdrawn it? (iv) Are remote leaves holding a stale ARP or ND entry, or is ARP suppression answering with the old binding? (v) Is *duplicate-MAC detection* freezing the address after several moves in a short window? Thirty seconds suggests an aging or detection timer; flood-and-learn would show the same gap. **Mistake.** Blaming the underlay before reading the Type-2 route.
:::

::: q
### Q5.16 What is an anycast gateway?
[ARISTA · CISCO · TECH-1 · ■□□ · T]{.meta}

[30-second answer: every leaf has the same gateway IP address and virtual MAC for a subnet, so a host's default gateway is always on its own leaf, and it keeps working unchanged when the host moves.]{.short}

**Answer.** The gateway 10.1.10.1 and one virtual MAC are configured on all leaves; ARP for the gateway is answered locally. There is no active/standby election, no hairpin to a distant gateway, and no gateway change on a VM migration. Compare HSRP and VRRP ([§4.8](#s4-8){.ref}), which keep one active router per subnet. **Mistake.** Giving each leaf a different physical gateway address for the same subnet.
:::

::: q
### Q5.17 What is SDN? Name the northbound and southbound interfaces.
[CISCO · GOOGLE · TECH-1 · ■□□ · T]{.meta}

[30-second answer: separating the control plane (a logically central controller) from the data plane (switches that apply installed rules); applications use the northbound interface (REST, gRPC) and switches the southbound one (OpenFlow, P4Runtime, gNMI, NETCONF).]{.short}

**Answer.** The controller has the global topology and computes paths or policies; it programs switches through the southbound protocol. Benefits: global optimisation (Google's B4 traffic engineering) and software-driven operation. Costs: the controller is a critical dependency, so production systems keep forwarding with the last installed state and often keep BGP underneath (§5.7). **Mistake.** "SDN replaces routing protocols."
:::

::: q
### Q5.18 Describe an OpenFlow flow-table entry and what happens on a table miss.
[CISCO · GOOGLE · TECH-2 · ■■□ · T]{.meta}

[30-second answer: an entry has a match, a priority, counters, instructions and timeouts; the highest-priority matching entry wins, and on a miss the table-miss entry (priority 0) decides, usually sending a packet-in to the controller.]{.short}

**Answer.** Fields: match (ingress port, Ethernet, VLAN, IP, ports), priority, counters, instructions (apply actions such as output or set-field, or goto-table), idle and hard timeouts, a cookie. A packet is matched table by table; if no entry matches and there is no table-miss entry, it is dropped (OpenFlow 1.3). The controller then installs a flow and returns the packet. **Follow-up.** Proactive installation avoids the controller round trip and the outage sensitivity of reactive designs. **Mistake.** Assuming a miss floods by default.
:::

::: q
### Q5.19 What does P4 let you do that OpenFlow does not?
[GOOGLE · BROADCOM · TECH-2 · ■■□ · T]{.meta}

[30-second answer: define the parser, the headers, the tables and the actions themselves, so the switch can process a protocol that did not exist when the chip was made; OpenFlow only fills tables over a fixed set of fields.]{.short}

**Answer.** A P4 program has a parser (state machine), match-action tables with chosen keys (exact, ternary, lpm) and a deparser; the compiler maps it onto a PISA target. Uses: custom telemetry headers, new tunnels, load-balancing in the switch, in-network aggregation. The control plane (P4Runtime) fills the entries. **Follow-up.** Limits: no loops, a fixed number of stages, and a target-specific architecture. **Mistake.** Treating P4 as a replacement for the controller; it programs the data plane only.
:::

::: q
### Q5.20 RIB versus FIB: what is the difference?
[CISCO · JUNIPER · ARISTA · TECH-1 · ■□□ · S]{.meta}

[30-second answer: the RIB holds every route learnt by every source on the control-plane CPU; the FIB is the compact copy of the winning routes, with adjacency data, that the forwarding hardware searches for each packet.]{.short}

**Answer.** Several protocols may offer one prefix; the lowest administrative distance (then metric) wins in the RIB, and only the winner is installed in the FIB (§5.8). The FIB also resolves recursive next hops down to an interface and rewrite string. The RIB changes at protocol speed; the FIB is downloaded to the ASIC. Check the two with `show ip route` and `show ip cef` (or `ip route` and the kernel FIB). **Mistake.** Saying the FIB contains backup routes; it normally holds the best path or paths only.
:::

:::
:::

:::
