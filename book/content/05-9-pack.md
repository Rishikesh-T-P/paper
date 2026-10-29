::: {.p5}

::: pack
## Revision Spread {#rv5}

::: revision
::: top
**Ten facts.** (1) A two-tier Clos: leaves ≤ spine ports, spines = uplinks per leaf, servers = leaves × server ports, oversubscription = down ÷ up; a three-tier fabric of k-port switches holds k³/4 servers at 1 : 1. (2) ECMP balances *flows* by a 5-tuple hash; polarisation comes from the same seed at every tier; resilient hashing moves only the failed member's share (1/N), mod-N moves about 75% when N goes from 4 to 3. (3) RFC 7938: eBGP everywhere, one AS for the spines and one per leaf, BFD 300 ms × 3 = 0.9 s, unnumbered links over IPv6 link-local; the 2-byte private range has only 1,023 numbers. (4) VXLAN is UDP 4789 with a 24-bit VNI and an 8-byte header; it adds 50 bytes over IPv4 (70 over IPv6), so the underlay IP MTU must be at least 1,550; the outer source port is a hash of the inner flow. (5) EVPN is BGP AFI 25 / SAFI 70: Type 2 host, Type 3 flood list, Type 5 prefix; a host move raises the MAC-mobility sequence; use the anycast gateway and symmetric IRB (L3VNI). (6) SDN splits controller from switch; an OpenFlow table miss is the priority-0 entry; P4 programs the parser, the tables and the deparser. (7) RIB on the CPU holds all routes, FIB in the ASIC holds winners with adjacencies; a TCAM stores prefixes longest first and returns the lowest index; the range 1024 to 65535 costs six entries; punts are limited by CoPP. (8) L4 balancers use the 5-tuple (NAT, DSR, tunnel); L7 terminate TLS and read HTTP; DSR needs the VIP on a loopback with ARP suppressed; Maglev uses a prime-sized table. (9) Anycast is BGP-nearest, not nearest in kilometres; expected CDN latency = h × e + (1 − h) × (e + o). (10) AWS: five reserved addresses, security groups stateful and allow-only, NACLs stateless and numbered, peering non-transitive, use a transit gateway; Azure: NSGs stateful with priority 100 to 4096 (lowest first), UDR next hop `VirtualAppliance`, ExpressRoute ASN 12076, one circuit is not site-redundant.

**Three figures to redraw.** The two-tier fabric with its port budget (Figure 5.2), the VXLAN encapsulation with byte counts (Figure 5.8), and the ASIC pipeline from ingress to egress (Figure 5.15).
:::

### Fabric, ECMP and underlay

| Item | Rule or value |
|---|---|
| Oversubscription | down bandwidth ÷ up bandwidth; 48 × 25G over 8 × 100G = 1.5 : 1 |
| Fabric size | spines = leaf uplinks (8); leaves = spine ports (64); servers = 64 × 48 = 3,072 |
| Bisection | half the leaves × their uplink capacity: 32 × 800G = 25.6 Tb/s |
| Pod and super-spine | 32 leaves, 4 spines; spine 32 down + 32 up; 64 pods = 98,304 servers |
| Hash inputs | src and dst IP, protocol, src and dst port; Linux policy 0/1/2 |
| Mod-N, 4 → 3 members | about 75% of flows change path; resilient: 25% (4 of 16 buckets) |
| ASN plan | spines 65100, leaves 65101 and up; unique per leaf; `allowas-in` or `as-override` if shared |
| Failure detection | BFD 300 ms × 3 = 0.9 s; BGP default hold 180 s |
| `multipath-relax` | needed when equal-length paths differ in AS content |

### Overlay comparison

| Encapsulation | Transport | Header and identifier | Notes |
|---|---|---|---|
| VXLAN (RFC 7348) | UDP 4789 | 8 bytes; 24-bit VNI | fixed header; source port = inner hash; dominant in switches |
| Geneve (RFC 8926) | UDP 6081 | 8 bytes + options; 24-bit VNI | extensible metadata; OVN, NSX, AWS Gateway LB |
| NVGRE (RFC 7637) | GRE, protocol 47 | 8 bytes; 24-bit VSID + 8-bit flow ID | no UDP port, so weak ECMP entropy; older Hyper-V |
| GRE | protocol 47 | 4 bytes (8 with key) | point-to-point tunnels; carries anything |
| MPLS L3VPN | labels | 4 bytes per label | provider core ([§4.10](#s4-10){.ref}); label stack, no IP overlay |

Overhead over IPv4: VXLAN 50 bytes (14 + 20 + 8 + 8), Geneve 50 plus options, GRE 24 (20 + 4) with no outer Ethernet counted.

### EVPN

| Type | Name | Use |
|---|---|---|
| 1 | Ethernet auto-discovery | multihoming, fast withdrawal |
| 2 | MAC/IP advertisement | host; L2VNI and L3VNI; mobility sequence |
| 3 | Inclusive multicast | VNI membership, BUM flood list |
| 4 | Ethernet segment | designated forwarder election |
| 5 | IP prefix | subnets, default route, external routes |

Symmetric IRB: ingress leaf routes into the L3VNI, egress leaf routes out. Asymmetric: every VNI on every leaf. ARP suppression: answered from Type-2 bindings.

### Router internals

| Item | Fact |
|---|---|
| RIB | all routes, all sources; control-plane CPU and DRAM |
| FIB + adjacency | winners and rewrite strings; ASIC memories |
| Punt reasons | to the router itself, TTL expiry, glean (ARP), IP options, ACL log |
| TCAM | ternary 0/1/x; priority encoder; 144 bits × 512 K ≈ 72 Mbit; high power |
| Pipeline | MAC, parser, ingress ACL, L2, L3 (LPM), ECMP and rewrite, traffic manager, egress ACL, deparser, MAC |
| Cut-through | needs idle egress and ingress speed ≥ egress speed; else store-and-forward |
| Incast | many senders, shallow buffer, 200 ms RTO; fix with ECN/DCTCP, buffers, fewer or paced senders |
| GR versus NSR | helper neighbours keep routes; standby processor mirrors state |

### Load balancers, anycast and CDN

| Item | Fact |
|---|---|
| L4 | 5-tuple; NAT, DSR or tunnel; no URL |
| L7 | terminates TLS; routes on host, path, header |
| DSR | VIP on loopback; `arp_ignore=1`, `arp_announce=2`; reply bypasses the balancer |
| Maglev | table of M entries (M prime); offset and skip per backend; round-robin fill |
| Health check | up after 2 successes, down after 3 failures (typical) |
| SNAT limit | about 64,000 ports per source address and destination address and port |
| Anycast | one prefix, many origins; failover by withdrawal; long TCP flows at risk |
| CDN hit | 0.9 × 15 + 0.1 × 235 = 37 ms (edge 15, origin 220) |

### AWS versus Azure

| Concept | AWS | Azure | Remember |
|---|---|---|---|
| Virtual network | VPC (region) | VNet (region) | both regional |
| Subnet | one AZ | spans zones | AWS: subnet per AZ |
| Instance filter | security group (stateful, allow) | NSG on NIC (stateful, allow/deny, priority) | NSG lowest number first |
| Subnet filter | network ACL (stateless) | NSG on subnet | Azure has no stateless filter |
| Routes | route table | route table with UDRs | UDR > BGP > system |
| Internet | internet gateway | default outbound / system route | AWS needs IGW and public IP |
| NAT | NAT gateway (per AZ) | NAT Gateway | cure for SNAT exhaustion |
| Join two networks | peering (non-transitive) | VNet peering (non-transitive) | overlap is not allowed |
| Hub | transit gateway | Virtual WAN hub, or hub VNet + firewall | many VPCs: 50 attachments, not 1,225 peerings |
| Private service access | PrivateLink (interface endpoint) | Private Link (private endpoint) | one-way, overlap allowed |
| Service by route | gateway endpoint (S3, DynamoDB) | service endpoint | no Internet transit |
| L4 / L7 balancer | NLB, GWLB / ALB | Load Balancer / Application Gateway | GWLB uses Geneve |
| Global front door | CloudFront, Global Accelerator | Front Door | anycast edge |
| Private circuit | Direct Connect (VIFs: private, public, transit) | ExpressRoute (private, Microsoft peering) | circuit is not site-redundant |
| VPN | Site-to-Site VPN, 2 tunnels | VPN Gateway | up to 1.25 Gb/s per AWS tunnel |
| Dynamic routes with an NVA | (transit gateway Connect) | Route Server (AS 65515) | BGP into the VNet |
| Flow records | VPC Flow Logs | NSG flow logs | first diagnostic tool |
| Reserved addresses | 5 per subnet | 5 per subnet | .0, .1, .2, .3, last |

### First five checks when a cloud VM cannot connect

(i) Route table of the subnet (and the NAT or gateway state). (ii) Security group or NSG, both directions, by priority. (iii) Network ACL, including the ephemeral ports (AWS). (iv) MTU through the overlay, VPN or peering: `ping -M do -s 1422`. (v) Return path and overlap: is the reply routed back the same way, and do the address ranges overlap?

### Flashcards

| Q | A |
|---|---|
| Spine-leaf path length? | leaf, spine, leaf; equal for all pairs |
| Servers in a two-tier fabric? | leaves (= spine ports) × server ports per leaf |
| Oversubscription? | down ÷ up bandwidth at the leaf |
| 5-stage Clos adds? | super-spine tier, pods and planes |
| What does ECMP balance? | flows, not packets |
| Polarisation cause and cure? | same hash and seed at all tiers; per-device seed |
| Resilient hashing? | fixed buckets; only the failed member's buckets move |
| Why eBGP in the DC? | small failure scope, policy, one protocol, simple loop control |
| Shared leaf ASN breaks? | AS_PATH loop check drops routes; unique AS, `allowas-in` or `as-override` |
| BFD 300 ms × 3? | 0.9 s detection |
| BGP unnumbered? | IPv6 link-local sessions; IPv4 routes via IPv6 next hop |
| Private ASN ranges? | 64512–65534 (2-byte), 4200000000–4294967294 (4-byte) |
| VXLAN port and ID? | UDP 4789; 24-bit VNI, 16,777,216 values |
| VXLAN overhead? | 50 bytes IPv4, 70 IPv6; underlay MTU ≥ 1,550 |
| Outer source port? | hash of the inner flow, for ECMP entropy |
| BUM delivery? | multicast underlay or ingress replication |
| EVPN address family? | AFI 25, SAFI 70 |
| Type 2, 3, 5? | host MAC/IP; VNI flood list; IP prefix |
| MAC mobility? | higher sequence number wins; old leaf withdraws |
| Anycast gateway? | same IP and MAC on every leaf |
| Symmetric IRB? | both leaves route, shared L3VNI |
| ARP suppression? | leaf answers from EVPN bindings |
| OpenFlow table miss? | priority-0 entry, often packet-in |
| P4 programs what? | parser, match-action tables, deparser |
| RIB or FIB in the ASIC? | FIB with adjacency |
| TCAM order? | longest prefix first; lowest index wins |
| Entries for ports 1024–65535? | six |
| CoPP? | rate-limits punted traffic per class |
| Cut-through falls back when? | egress busy or faster than ingress |
| Incast fix? | ECN/DCTCP, buffers, shorter RTO, paced replies |
| L4 versus L7? | 5-tuple and packets; TLS terminated and HTTP routing |
| DSR backend needs? | the VIP on a loopback, ARP suppressed |
| Maglev table size? | prime M much larger than the backends |
| Anycast picks? | the BGP-nearest site |
| SG versus NACL? | stateful allow-only on the interface; stateless numbered on the subnet |
| Is peering transitive? | no; use a transit gateway |
| NSG rule order? | lowest priority number first |
| ExpressRoute redundancy? | two links, one location; add a second circuit |
| VPN over ExpressRoute with a /24? | more specific prefix wins; keep lengths equal |
:::
:::

:::
