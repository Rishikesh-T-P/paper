::: {.p5}

::: pack
## Problem Set, continued: internals, load balancing and the cloud {#ps5b}

::: problems

::: q
### Q5.21 What is TCAM? Why is it used for LPM and ACLs, and what are its costs?
[BROADCOM · CISCO · JUNIPER · TECH-2 · ■■□ · T]{.meta}

[30-second answer: a memory that compares the search key with every stored entry at once and stores 0, 1 or "don't care" in each bit; one cycle finds the longest prefix or the first ACL match. It costs area, power and money per bit, so it is small and shared.]{.short}

**Answer.** Prefixes and ACL lines are masks over header bits, which is exactly what a ternary cell stores. Entries are kept in priority order and a priority encoder returns the lowest index (Figure 5.14). Costs: a ternary bit needs about twice the storage of an SRAM bit and more area, every row switches on every lookup (power grows with depth), entries must be ordered (an insertion can shift many), and ranges expand into several entries (1024 to 65535 needs six). Large FIBs therefore sit in algorithmic SRAM and TCAM holds ACLs and the rest. **Follow-up.** 144 bits × 512 K entries is about 72 Mbit. Design framing in Q12.33. **Mistake.** "TCAM holds the routing table."
:::

::: q
### Q5.22 Design a data structure for longest-prefix match supporting 1 million IPv4 prefixes. Discuss memory and lookups per packet.
[BROADCOM · ARISTA · JUNIPER · CISCO · TECH-2 · ■■■ · T]{.meta}

[30-second answer: a DIR-24-8 table: an array of 2²⁴ entries indexed by the top 24 bits of the address, plus 256-entry second-level blocks for the few prefixes longer than /24; a lookup is one memory access, or two, at a cost of about 32 MiB.]{.short}

**Approach.** Compare the options by accesses per lookup and memory. A *binary trie* needs up to 32 reads and 1 M prefixes make millions of nodes. A *multibit trie* with stride 8 needs four reads and more memory (prefixes expand to the stride). A *compressed* trie (Linux's LC-trie, a poptrie) uses less memory with a few reads. A TCAM does it in one cycle at high power. DIR-24-8 trades memory for speed: the tables are sized for all /24 blocks, and updates are the price.

**Answer.**

```c
#include <stdint.h>
static uint16_t tbl24[1u << 24];        /* 32 MiB; bit 15 set: index of a tbl8 block */
static uint16_t tbl8[4096][256];        /* 512 bytes per extended /24 block */
uint16_t lookup(uint32_t ip) {          /* returns a next-hop index */
    uint16_t e = tbl24[ip >> 8];
    if (e & 0x8000) e = tbl8[e & 0x7FFF][ip & 0xFF];
    return e;
}
```

Insert a prefix of length ≤ 24 by filling 2^(24 − len) entries of `tbl24` (a /8 writes 65,536 entries, a /24 one); keep the longer prefix on collision by inserting in increasing length order or by storing the length. A prefix longer than /24 allocates a `tbl8` block for its /24 and fills the 2^(32 − len) entries. **Complexity.** Lookup O(1): one access (two for long prefixes); memory 32 MiB + 512 B per extended block (4,096 blocks add 2 MiB). With 1 M prefixes, nearly all are ≤ /24, so the table is dense. At about 80 ns per DRAM miss, a core does roughly 12 M lookups per second unprefetched, and far more when it batches lookups and prefetches. **Follow-ups.** IPv6 needs a different structure (a trie on 64-bit prefixes or hashing). Updates of a /8 are slow, so routers batch them. **Mistake.** Forgetting that the 32 MiB array is sparse in use but not in memory.
:::

::: q
### Q5.23 Walk a packet through a switch ASIC from ingress port to egress.
[BROADCOM · ARISTA · JUNIPER · TECH-2 · ■■■ · T]{.meta}

[30-second answer: ingress MAC, parser, ingress ACL, L2 lookup, L3 lookup, ECMP resolution and adjacency rewrite, then the traffic manager (queues, buffer, scheduler), egress ACL, deparser and egress MAC.]{.short}

**Answer.** The parser builds a header vector; the ACL TCAM can drop, mark or punt; the L2 table (exact match on MAC) finds a routed packet by the router MAC; the L3 LPM returns a next-hop group, a hash picks a member, and the adjacency rewrites the MAC header and the TTL; the traffic manager queues the packet by egress port and class and the scheduler releases it; the egress stages add encapsulation and the checksum. Details and diagram: §5.8. **Follow-ups.** Where is the ECMP hash (after L3)? Where is ECN marked (traffic manager)? Where are punts decided (ACL, L3 or exceptions)? **Mistake.** Putting the queue in front of the lookups; the destination port is needed to choose the queue.
:::

::: q
### Q5.24 What is a punt? What is CoPP and why is it needed?
[CISCO · JUNIPER · TECH-1 · ■■□ · T]{.meta}

[30-second answer: a punt hands a packet the ASIC cannot forward alone (for the router itself, TTL expiry, an ARP glean) to the CPU; CoPP rate-limits each class of punted traffic so that a flood cannot starve the control plane.]{.short}

**Answer.** The CPU handles thousands of packets per second, the ASIC billions, so unprotected punts are a denial-of-service path that can break routing sessions. CoPP applies a hardware policer per class (routing protocols, management, ARP, everything else) before the CPU queue, with generous rates for BGP and OSPF and low ones for the rest (§5.8). **Follow-up.** The data plane also can be protected from the control plane with a router-address ACL. **Mistake.** Applying CoPP to transit traffic; it polices only traffic destined to, or punted to, the router.
:::

::: q
### Q5.25 Cut-through versus store-and-forward switching. When does cut-through fall back?
[ARISTA · BROADCOM · TECH-2 · ■■□ · T]{.meta}

[30-second answer: cut-through forwards a frame as soon as the header is read; store-and-forward waits for the whole frame and checks the FCS. Cut-through falls back when the egress port is busy or faster than the ingress port.]{.short}

**Answer.** Serialisation time of a 1,500-byte frame is 12,000 bits ÷ 25 Gb/s = 480 ns at 25G (1.2 µs at 10G); cut-through saves most of it per hop. The switch must be able to supply bits to the egress at least as fast as it sends them, so it needs ingress speed ≥ egress speed and an idle port; otherwise the frame is buffered, and the switch is store-and-forward for that frame. Frames with a bad FCS have already left when the error is found; the switch counts them and may poison the frame. **Mistake.** Quoting cut-through latency as if queueing delay vanished.
:::

::: q
### Q5.26 What is TCP incast? How do deep buffers, ECN/DCTCP or pacing help?
[GOOGLE · ARISTA · TECH-2 · ■■■ · T]{.meta}

[30-second answer: many servers reply to one client at once, overflowing the shallow buffer of the client's port; tail drops cause retransmission timeouts of about 200 ms and throughput collapses. Larger buffers, early ECN marking with DCTCP, shorter timers or paced replies cure it.]{.short}

**Approach.** Quantify the burst against the port buffer. **Answer.** 50 servers each return 20 KB (1 MB in total) to one client on a 10 Gb/s port with 256 KB of buffer. The data needs 1 MB ÷ 1.25 GB/s = 0.8 ms to drain, but the burst arrives almost simultaneously, so about 750 KB is lost. The lost senders wait for a 200 ms timeout, and goodput is 8 Mb ÷ 0.2008 s = about 40 Mb/s, 0.4% of the port. Remedies: (i) *buffers:* deeper or dynamically shared buffers absorb the burst (and cost latency); (ii) *ECN and DCTCP* ([§3.9](#s3-9){.ref}) mark above a low threshold so senders shrink windows before loss; (iii) *timers:* a retransmission timeout of a few milliseconds; (iv) *application:* limit fan-out, stagger or pace replies; (v) *network:* a priority queue or per-flow fair queueing. **Mistake.** Only adding bandwidth: the port was idle 99% of the time.
:::

::: q
### Q5.27 What are NSF/Graceful Restart and NSR?
[JUNIPER · CISCO · NOKIA · TECH-2 · ■■□ · T]{.meta}

[30-second answer: both keep traffic flowing while the control plane restarts. Graceful restart relies on neighbours to keep the router's routes during a restart window; non-stop routing mirrors protocol state on a standby processor, with no help from neighbours.]{.short}

**Answer.** *NSF with GR:* the forwarding hardware keeps the stale FIB; the restarting router signals a restart time, and helper neighbours retain its routes and re-learn them (RFC 4724 for BGP, RFC 3623 for OSPF). It needs two route processors or a software restart, and capable neighbours. *NSR:* the standby processor holds a synchronised copy of the protocol state, including TCP sessions for BGP, and takes over unnoticed. GR is cooperative and can be unsafe if the data plane is also broken (traffic is blackholed to a dead next hop for the window); NSR is internal and costs memory and complexity. **Mistake.** Using GR with an aggressive BFD that tears the session down anyway.
:::

::: q
### Q5.28 L4 versus L7 load balancer.
[AMAZON · MICROSOFT · GOOGLE · TECH-1 · ■□□ · S]{.meta}

[30-second answer: layer 4 decides from addresses and ports and forwards packets without reading them (fast, no TLS); layer 7 terminates TCP and TLS, reads the HTTP request and routes by host, path or header (flexible, costlier).]{.short}

**Answer.** Use the comparison in §5.9: NLB and Azure Load Balancer are layer 4, ALB and Application Gateway layer 7. Choose layer 4 for raw throughput, non-HTTP protocols, source-IP preservation and static addresses; choose layer 7 for path routing, header rewriting, WAF, sticky cookies and retries. Often both are used: a layer-4 tier in front of a layer-7 tier. **Mistake.** Expecting URL routing from a layer-4 balancer.
:::

::: q
### Q5.29 Explain direct server return. Why does the backend need the VIP on its loopback?
[GOOGLE · AMAZON · TECH-2 · ■■□ · T]{.meta}

[30-second answer: the balancer forwards the request to the backend without rewriting the destination IP, and the backend replies straight to the client with the VIP as source; the backend must hold the VIP locally to accept the packet, on a loopback with ARP suppressed so that it does not answer for the VIP.]{.short}

**Answer.** In layer-2 DSR the balancer rewrites only the destination MAC, so the packet still carries the VIP as destination and the backend's stack drops it unless it owns that address. The loopback holds the VIP; `arp_ignore=1` and `arp_announce=2` stop the backend from advertising it. Over a layer-3 tunnel (IP-in-IP or GRE) the backend decapsulates and sees the same inner packet. The reply source is the VIP, so the client accepts it. Benefits: the balancer handles only requests; limits: no port translation, backends in the same layer-2 domain or tunnelled, and the balancer cannot see the reply to track state. **Mistake.** Putting the VIP on the physical interface, so that the backend answers ARP and steals the VIP.
:::

::: q
### Q5.30 Design a software L4 load balancer handling 10 Mpps that survives instance failure without breaking connections.
[GOOGLE · MICROSOFT · TECH-2 · ■■■ · T]{.meta}

[30-second answer: announce the VIP from several stateless balancer nodes; routers spread flows by ECMP; every node uses the same consistent-hash table and a connection table to choose a backend, so a flow that lands on another node after a failure still reaches the same backend.]{.short}

**Approach.** Size first, then make failure invisible. **Answer.** *Capacity:* at about 5 Mpps per node (XDP or DPDK on 25 GbE), 10 Mpps needs 2 nodes; with N+2 spare and headroom, 4 to 5. *Flow path:* the border routers hold the VIP route from each node (BGP), ECMP hashes the 5-tuple, ideally with resilient hashing. Each node computes `table[hash(5-tuple) mod M]` with a Maglev table (§5.9), checks its connection table, and forwards by DSR or GRE. *Failure:* BFD removes the dead node's route in about a second; the router re-hashes some flows to other nodes, which hash to the same backend because the tables are identical, so the connections survive. *Backend change:* new connections use the new table; existing ones stay pinned in the connection table until idle. *Health checks* drive the pool; connections drain before removal. **Follow-ups.** SYN floods (SYN cookies at the edge), connection-table size (about 64 bytes per connection), and what breaks (a backend change at the same time as a node failure). **Mistake.** Per-node state that cannot be rebuilt.
:::

::: q
### Q5.31 How does anycast work? What happens to TCP if routing changes mid-flow?
[GOOGLE · AMAZON · TECH-2 · ■■□ · T]{.meta}

[30-second answer: the same prefix is announced from many sites and BGP delivers each user to the best (BGP-nearest) one; if the route changes during a connection the packets reach a site with no state for it, which resets the connection.]{.short}

**Answer.** Nothing in the protocol is special; the routers see several paths and apply the usual rules (§5.10). A site withdraws its route to leave. Routes are usually stable for the length of a short HTTP or DNS exchange, so TCP works; long flows are exposed to a change of the best path. Mitigations: keep long flows on a unicast address after the handshake, share connection state between sites, use QUIC with connection IDs, and avoid flapping by announcing from stable locations. **Mistake.** Claiming that anycast needs a special protocol, or that it finds the geographically nearest site.
:::

::: q
### Q5.32 How does a CDN choose which edge serves you?
[GOOGLE · AMAZON · MICROSOFT · TECH-1 · ■■□ · T]{.meta}

[30-second answer: either DNS returns the address of an edge chosen from the resolver's (or client subnet's) location and measured load, or the CDN announces one anycast address and BGP picks the edge; both aim for the lowest latency with healthy capacity.]{.short}

**Answer.** (i) *DNS steering:* the site name is a CNAME to the CDN, whose authoritative server uses the resolver's address or the EDNS Client Subnet, measured latency and load to answer with an edge; TTLs of 20 to 60 s keep it adaptive. (ii) *Anycast:* routing decides, with failover by withdrawal. (iii) Operators combine them, and mid-tier caches shield the origin (§5.10). **Follow-up.** A resolver far from its users causes poor choices; EDNS Client Subnet reduces this at a privacy cost. **Mistake.** Forgetting that a cache miss still pays the origin round trip.
:::

::: q
### Q5.33 Security group versus network ACL in AWS.
[AMAZON · TECH-1 · ■□□ · S]{.meta}

[30-second answer: a security group is stateful, allow-only, attached to an interface and evaluated as a whole; a network ACL is stateless, has allow and deny rules in numbered order, and is attached to a subnet.]{.short}

**Answer.** Use the table in §5.11. Scenario: a web server accepts TCP 443. The security group needs one inbound rule; the reply is allowed automatically. The network ACL needs an inbound rule for 443 and an outbound rule for the ephemeral ports 1024 to 65535, because it forgets the request. Use security groups for tier-to-tier rules (by group reference) and NACLs for subnet-wide denies, such as blocking an address range. **Mistake.** Writing a deny in a security group.
:::

::: q
### Q5.34 A private-subnet EC2 instance cannot reach the Internet. List the checks in order.
[AMAZON · TECH-1 · ■■□ · S]{.meta}

[30-second answer: the subnet's route table (default route to a NAT gateway), the NAT gateway (available, in a public subnet, with an Elastic IP), that subnet's route to the IGW, security group and network ACL rules both ways, DNS, and finally the instance's own firewall.]{.short}

**Answer.** (i) Route table of the private subnet: is there `0.0.0.0/0` to a NAT gateway (not a missing or blackholed target)? (ii) NAT gateway: state *available*, an Elastic IP attached, placed in a *public* subnet. (iii) The public subnet's route table: `0.0.0.0/0` to the IGW. (iv) Security group egress of the instance (the default allows all) and the NAT's inbound handling. (v) Network ACLs on both subnets: outbound 443 and inbound ephemeral 1024 to 65535 for the reply. (vi) DNS: `enableDnsSupport`, the resolver at the VPC base + 2. (vii) The host: its default gateway, firewall and proxy settings. Use Flow Logs to see where the packet stops. **Mistake.** Putting the NAT gateway in the private subnet.
:::

::: q
### Q5.35 Is VPC peering transitive? How do you connect 50 VPCs?
[AMAZON · MICROSOFT · TECH-2 · ■■□ · T]{.meta}

[30-second answer: no: peering joins exactly two VPCs and does not pass traffic through one to another; for 50 VPCs use a transit gateway, which needs 50 attachments where a full mesh of peerings would need 1,225.]{.short}

**Answer.** Peering also needs non-overlapping CIDRs and routes on both sides, and does not allow use of the peer's IGW, NAT or VPN. A transit gateway gives transitive routing, with attachment route tables expressing which VPC reaches which (shared services, isolated tenants). For service-only access use PrivateLink, which tolerates overlapping ranges. Across regions, peer transit gateways. **Follow-up.** Costs: per-attachment and per-GB charges on a TGW, against free peering within an AZ. **Mistake.** Assuming a route through the middle VPC will work if the route tables allow it.
:::

::: q
### Q5.36 Azure: what is a UDR? Give a scenario that needs one.
[MICROSOFT · TECH-1 · ■■□ · T]{.meta}

[30-second answer: a user-defined route overrides Azure's system routes for a subnet; for example 0.0.0.0/0 with next hop `VirtualAppliance` to force all spoke traffic through a firewall in a hub.]{.short}

**Answer.** A UDR lives in a route table attached to subnets and names a prefix and a next hop type (virtual appliance, virtual network gateway, internet, none). In hub and spoke (§5.12) the spoke default route makes spoke-to-spoke traffic cross the firewall, since peering is non-transitive. Also used to blackhole a prefix (next hop `None`) or to steer traffic to an NVA. Precedence among equal prefixes: UDR, then BGP, then system. **Mistake.** Forgetting *Allow forwarded traffic* on the peering, so that the firewall's forwarded packets are dropped.
:::

::: q
### Q5.37 Design ExpressRoute with VPN failover. How do you ensure symmetric routing?
[MICROSOFT · TECH-2 · ■■■ · T]{.meta}

[30-second answer: advertise the same prefixes over both paths with the same length, make ExpressRoute preferred in both directions (higher LOCAL_PREF on-premises, shorter AS_PATH towards Azure) and leave the VPN as a last resort; never advertise a more specific prefix over the VPN.]{.short}

**Approach.** Decide preference for each direction separately, then test. **Answer.** The two links of the circuit run to two MSEEs and each is a BGP session (§5.13). *Outbound* (campus to Azure): LOCAL_PREF 200 on routes from the primary CE, 150 from the secondary, 100 from the VPN. *Inbound* (Azure to campus): prepend towards the secondary and more towards the VPN, so the primary has the shortest path. Keep prefix lengths identical on every path, since the longest prefix beats all attributes. Azure prefers ExpressRoute over VPN for the same prefix by default. Add BFD, summarise to stay below the peering route limit, and place a second circuit in another peering location if the facility matters. Rehearse by shutting each link and checking both directions with `traceroute`. **Mistake.** Prepending on only one side, which leaves a path asymmetric through a stateful firewall.
:::

::: q
### Q5.38 On-premises advertises 10.0.0.0/8 over ExpressRoute while an Azure VNet uses 10.1.0.0/16. What happens and how do you fix it?
[MICROSOFT · TECH-2 · ■■■ · T]{.meta}

[30-second answer: inside the VNet the more specific local route wins, so VNet traffic stays local, but any on-premises hosts in 10.1.0.0/16 become unreachable from Azure; fix by renumbering, by advertising only the real on-premises prefixes, or by translating one side.]{.short}

**Answer.** The VNet has a system route for 10.1.0.0/16 and learns 10.0.0.0/8 through the gateway; longest prefix means 10.1.x.x stays in the VNet and the other 10.x.x.x reaches on-premises. If a campus subnet shares an address with the VNet, say 10.1.5.0/24, traffic to it is delivered inside the VNet to the wrong host or to nothing. In the opposite direction the VNet's 10.1.0.0/16 advertised to the campus competes with the on-premises routes. A VNet cannot be peered with another that overlaps. Fixes, in order of preference: (i) renumber the cloud ranges out of the on-premises space (plan from one IPAM list); (ii) replace the /8 with the prefixes actually in use; (iii) NAT at a firewall for the overlapping part. **Mistake.** Relying on a summary route to "cover" overlapping space.
:::

::: q
### Q5.39 Explain how Azure or AWS implement the virtual-network data plane: host-based SDN, SmartNICs, encapsulation.
[MICROSOFT · AMAZON · TECH-3 · ■■■ · T]{.meta}

[30-second answer: the physical network is a plain routed fabric; each host (or its SmartNIC) holds the tenant's flow and mapping tables, encapsulates a tenant packet toward the destination host's physical address, and applies security rules, so the virtual network exists only in the hosts' tables.]{.short}

**Answer.** *Publicly described design:* a controller computes a tenant's policy and pushes it to every host; the host's virtual switch (Azure's Virtual Filtering Platform, AWS's Nitro-based software and hardware) holds match-action layers for routing, security-group or NSG rules and NAT. A mapping service translates a virtual address into the physical address of the destination host; the packet is encapsulated (VXLAN-like) and carried by the underlay (§5.5), then decapsulated and filtered at the destination. First packets of a flow take a slower path that builds a flow entry; later packets hit the entry, and with *Accelerated Networking* or Nitro cards the whole fast path is offloaded to the NIC (SR-IOV, FPGA or custom silicon), freeing the CPUs. Stateful rules need a connection tracker. **Follow-up.** Why no broadcast: ARP is answered by the host. **Mistake.** Describing VPCs as VLANs on a switch.
:::

::: q
### Q5.40 Compare the Google Jupiter approach with a traditional chassis-based data centre.
[GOOGLE · TECH-3 · ■■■ · T]{.meta}

[30-second answer: Jupiter builds a Clos fabric of many small merchant-silicon switches under centralised control, so capacity scales by adding identical blocks and software is updated centrally; a chassis design buys large proprietary boxes with distributed protocols, which scale less, cost more and fail in bigger domains.]{.short}

**Answer.** Per the *Jupiter Rising* paper and its successor: (i) *Topology:* a multi-stage Clos from commodity chips, with later generations adding optical circuit switches in place of part of the spine layer so that capacity can be re-balanced without recabling; a chassis tree has a few large aggregation boxes and spanning tree or MLAG. (ii) *Control:* centralised, software-defined routing (Orion) with a logically central view; a chassis network relies on distributed protocols on each device. (iii) *Scale and cost:* many small failures are tolerated and the cost per port is lower; a chassis failure removes a large share of capacity. (iv) *Operations:* incremental upgrade, standard blocks, automation. Limits: the centralised design needs resilient controllers and a fallback. **Mistake.** Saying Jupiter is "just a bigger spine-leaf"; the control plane and the optical layer are the new parts.
:::

**Questions solved in other pillars.** The congestion-control mechanisms behind Q5.26 are taught in [Pillar 3](#ch3){.ref}; the ARP, MTU and NAT mechanisms in Q5.10 and Q5.34 are in [Pillar 3](#ch3){.ref}; BGP attributes in Q5.5, Q5.37 and Q5.38 are in [Pillar 4](#ch4){.ref}. System-design framings of Q5.21 and Q5.30 (Q12.33, Q12.39) and the slow-user ECMP case (Q11.23) appear in their own pillars and cite this chapter.
:::

:::

:::
