::: {.p5}

## [5.5]{.sec}Overlays: VXLAN [Must · ■■□]{.tag} {#s5-5}

::: bigidea
VXLAN carries a tenant's Ethernet frame inside a UDP packet between two switches, so tenants obtain layer-2 networks over a routed fabric, with 16 million segment identifiers in place of 4,094 VLANs, at the price of 50 bytes of header per packet.
:::

A virtual machine keeps its IP address when it moves, which is easy only if the new host is in the same layer-2 segment; yet the fabric of §5.4 is routed, and routers do not extend layer-2 segments. The solution is an *overlay*: the endpoints of the virtual network wrap each tenant frame in an ordinary IP packet, the routed *underlay* delivers it, and the far endpoint unwraps it. *VXLAN* (Virtual eXtensible LAN, RFC 7348) is the dominant overlay. The device that wraps and unwraps is the *VTEP* (VXLAN tunnel endpoint); it may be a leaf switch or the virtual switch of a hypervisor, and it has an IP address, usually a loopback, that appears as the outer address. A 24-bit *VXLAN network identifier* (VNI) names the tenant segment, giving 2²⁴ = 16,777,216 segments. The outer packet is UDP with destination port 4789.

The encapsulation is shown in Figure 5.7. The VXLAN header itself is eight bytes: a flags byte whose "I" bit (0x08) says that the VNI is valid, three reserved bytes, the three-byte VNI, and one reserved byte. The *source* UDP port is not fixed: the VTEP computes it as a hash of the inner Ethernet, IP and transport headers, within the ephemeral range. This is deliberate. The underlay's ECMP hash (§5.3) sees only the outer 5-tuple, and all packets between two VTEPs would otherwise share one tuple and one path; with the inner flow hashed into the source port, different tenant flows take different spines, and each flow stays in order.

<figure>
<svg viewBox="0 0 480 190" width="480"><defs></defs><rect class="box" x="8" y="16" width="42" height="26" rx="0"/><text class="lbl" x="29.0" y="32" text-anchor="middle">Outer Eth</text><text class="sm" x="29.0" y="54" text-anchor="middle">14</text><rect class="box" x="50" y="16" width="60" height="26" rx="0"/><text class="lbl" x="80.0" y="32" text-anchor="middle">Outer IP</text><text class="sm" x="80.0" y="54" text-anchor="middle">20</text><rect class="box" x="110" y="16" width="24" height="26" rx="0"/><text class="sm" x="122.0" y="32" text-anchor="middle">UDP</text><text class="sm" x="122.0" y="54" text-anchor="middle">8</text><rect class="fill" x="134" y="16" width="24" height="26" rx="0"/><text class="sm" x="146.0" y="32" text-anchor="middle">VX</text><text class="sm" x="146.0" y="54" text-anchor="middle">8</text><rect class="fill" x="158" y="16" width="42" height="26" rx="0"/><text class="lbl" x="179.0" y="32" text-anchor="middle">Inner Eth</text><text class="sm" x="179.0" y="54" text-anchor="middle">14</text><rect class="fill" x="200" y="16" width="190" height="26" rx="0"/><text class="lbl" x="295.0" y="32" text-anchor="middle">Inner IP + payload (the tenant's packet)</text><rect class="box" x="390" y="16" width="14" height="26" rx="0"/><text class="sm" x="397.0" y="32" text-anchor="middle">FCS</text><text class="sm" x="397.0" y="54" text-anchor="middle">4</text><path class="acc" d="M8,60 L158,60"/><text class="acct" x="83.0" y="72" text-anchor="middle">50 bytes added by the VTEP</text><text class="sm" x="122" y="86" text-anchor="middle">dst port 4789</text><text class="sm" x="152" y="98" text-anchor="middle"></text><text class="lbl" x="8" y="108" text-anchor="start">VXLAN header (8 bytes), bit positions</text><text class="sm" x="40" y="122" text-anchor="middle">0</text><text class="sm" x="136" y="122" text-anchor="middle">8</text><text class="sm" x="232" y="122" text-anchor="middle">16</text><text class="sm" x="328" y="122" text-anchor="middle">24</text><text class="sm" x="418" y="122" text-anchor="middle">31</text><rect class="hl" x="40" y="126" width="96" height="24" rx="0"/><text class="sm" x="88.0" y="141" text-anchor="middle">Flags: R R R R I R R R</text><rect class="box" x="136" y="126" width="288" height="24" rx="0"/><text class="lbl" x="280.0" y="141" text-anchor="middle">Reserved</text><rect class="hl" x="40" y="150" width="288" height="24" rx="0"/><text class="lbl" x="184.0" y="165" text-anchor="middle">VNI (24 bits)</text><rect class="box" x="328" y="150" width="96" height="24" rx="0"/><text class="sm" x="376.0" y="165" text-anchor="middle">Reserved</text><text class="sm" x="34" y="141" text-anchor="end">0</text><text class="sm" x="34" y="165" text-anchor="end">4</text></svg>
<figcaption><b>Figure 5.7</b> VXLAN encapsulation. Byte counts are under each block. The I flag (value 0x08) says the VNI is valid; the 24-bit VNI allows 16,777,216 segments.</figcaption>
</figure>

::: example
**Overhead and MTU for a 1,500-byte tenant packet.** Campus Net's SALES servers (VLAN 10, 10.1.10.0/24) are given VNI 10010 and appear on two racks; a packet from Host A on L1 to Host B on L2 crosses the fabric (Figure 5.8).

1. The tenant frame is the inner Ethernet header (14 bytes) plus a 1,500-byte IP packet: 1,514 bytes.
2. The VTEP adds a VXLAN header (8), an outer UDP header (8), an outer IPv4 header (20) and an outer Ethernet header (14): 50 bytes in all.
3. The outer IP packet is 20 + 8 + 8 + 1,514 = 1,550 bytes, so the underlay IP MTU must be at least 1,550. On the wire the frame is 1,564 bytes (1,568 with the FCS).
4. If the outer header is IPv6 (40 bytes instead of 20), the overhead is 70 bytes and the minimum underlay MTU is 1,570.
5. Fabrics therefore set the underlay MTU to 9,216 (jumbo frames) and leave the tenant MTU at 1,500 or 9,000. If the underlay stays at 1,500, the usable tenant MTU is 1,500 − 50 = 1,450 for the IP packet, which Linux sets automatically on a VXLAN interface.

[Result: 50 bytes of encapsulation (70 over IPv6); underlay IP MTU at least 1,550; jumbo frames avoid the problem.]{.result}
:::

<figure>
<svg viewBox="0 0 480 210" width="480"><defs><marker id="a58" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accf"/></marker></defs><rect class="box" x="5" y="70" width="52" height="26" rx="0"/><text class="lbl" x="31" y="83" text-anchor="middle">Host A</text><text class="sm" x="31" y="92" text-anchor="middle">VNI 10010</text><rect class="box" x="80" y="64" width="88" height="38" rx="0"/><text class="lbl" x="124" y="79" text-anchor="middle">Leaf L1</text><text class="sm" x="124" y="90" text-anchor="middle">VTEP 10.0.0.1</text><rect class="box" x="210" y="16" width="60" height="22" rx="0"/><text class="lbl" x="240" y="30" text-anchor="middle">Spine S1</text><rect class="box" x="210" y="118" width="60" height="22" rx="0"/><text class="lbl" x="240" y="132" text-anchor="middle">Spine S2</text><rect class="box" x="312" y="64" width="88" height="38" rx="0"/><text class="lbl" x="356" y="79" text-anchor="middle">Leaf L2</text><text class="sm" x="356" y="90" text-anchor="middle">VTEP 10.0.0.2</text><rect class="box" x="423" y="70" width="52" height="26" rx="0"/><text class="lbl" x="449" y="83" text-anchor="middle">Host B</text><text class="sm" x="449" y="92" text-anchor="middle">VNI 10010</text><line class="ln" x1="57" y1="83" x2="80" y2="83"/><line class="ln" x1="400" y1="83" x2="423" y2="83"/><line class="lg" x1="168" y1="76" x2="210" y2="27"/><line class="lg" x1="168" y1="90" x2="210" y2="129"/><line class="lg" x1="270" y1="27" x2="312" y2="76"/><line class="lg" x1="270" y1="129" x2="312" y2="90"/><path class="acc" d="M168,76 L210,27 M270,27 L312,76" marker-end="url(#a58)"/><text class="sm" x="240" y="60" text-anchor="middle">underlay: routed IP</text><text class="sm" x="240" y="76" text-anchor="middle">(ECMP picks S1 or S2</text><text class="sm" x="240" y="86" text-anchor="middle">from the outer UDP port)</text><rect class="fill" x="8" y="158" width="464" height="20" rx="0"/><text class="mono" x="14" y="171" text-anchor="start">on the access links:  Eth(A→B) | IP | payload</text><rect class="hl" x="8" y="182" width="464" height="20" rx="0"/><text class="mono" x="14" y="195" text-anchor="start">in the fabric:  IP 10.0.0.1→10.0.0.2 | UDP →4789 | VXLAN VNI 10010 | Eth(A→B) | IP | payload</text></svg>
<figcaption><b>Figure 5.8</b> A frame from Host A to Host B across the overlay. L1 wraps the tenant frame in an outer IP and UDP packet addressed to L2's loopback; the spines forward it as ordinary IP and never see the inner Ethernet header.</figcaption>
</figure>

A VTEP must learn where each tenant MAC lives. The original design copies a switch: a VTEP that receives an encapsulated frame learns "inner source MAC X is behind outer source IP Y", and sends frames for unknown destinations, broadcasts and multicast (together termed *BUM* traffic) to every other VTEP of that VNI. The BUM copies are delivered either by an IP multicast group in the underlay (efficient but requires PIM, [§4.12](#s4-12){.ref}) or by *ingress replication*, where the source VTEP unicasts one copy to each peer. Flood-and-learn works but does not scale, and §5.6 replaces it with a BGP control plane.

Two other encapsulations appear in interviews. *Geneve* (RFC 8926) uses UDP port 6081 and a variable-length option field, which suits services that need to carry metadata; AWS Gateway Load Balancer ([§5.9](#s5-9){.ref}) uses it. *NVGRE* (RFC 7637) puts the tenant frame in GRE, which has no UDP port to hash, so it offers poor ECMP entropy. Neither has displaced VXLAN in switch hardware. The comparison table is in the Revision Spread.

::: lab
`LAB 5.5 · 90 MIN`  Two Linux hosts (or network namespaces) joined by a link with MTU 1500, carrying a point-to-point VXLAN tunnel on VNI 10010.

```
ip link add vxlan10 type vxlan id 10010 dstport 4789 local 10.0.0.1 remote 10.0.0.2
ip addr add 10.1.10.1/24 dev vxlan10 && ip link set vxlan10 up
ip -d link show vxlan10 | grep mtu
ping -M do -s 1472 10.1.10.2
ping -M do -s 1422 10.1.10.2
```

```
vxlan10: ... mtu 1450 ...
ping: local error: message too long, mtu=1450
64 bytes from 10.1.10.2: icmp_seq=1 ttl=64
```

**What you should notice:** a 1,472-byte payload makes a 1,500-byte packet (1,472 + 28), which the interface refuses; 1,422 makes 1,450 and passes. Raise the underlay to 9000 (`ip link set eth0 mtu 9000`) and the VXLAN interface to 8950, and the large ping succeeds. With the default 1,500 and a tenant that believes its MTU is 1,500, small packets (ping, the TCP handshake) work while large ones vanish: the classic symptom is "ping works, HTTPS hangs".
:::

::: trap
*Claim:* "VXLAN extends a VLAN across the data centre." *Why it is wrong:* the VNI is not a VLAN tag, and the tenant frame travels over a routed network; a VLAN on a leaf port is merely mapped to a VNI (Campus Net maps VLAN 10 to VNI 10010). Further, the inner and outer headers together exceed the link MTU unless it is raised. *Correct statement:* VXLAN carries layer-2 frames in UDP over layer 3, and the underlay MTU must be at least the tenant MTU plus 50.
:::

::: check
1. How many bytes does VXLAN add over an IPv4 underlay, and which UDP port does it use? [^c55-1]
2. Why is the outer UDP source port a hash of the inner headers? [^c55-2]
3. What is BUM traffic and how is it delivered without multicast? [^c55-3]
:::

[^c55-1]: 50 bytes (outer Ethernet 14, IP 20, UDP 8, VXLAN 8); destination port 4789.
[^c55-2]: It gives the underlay's ECMP hash entropy, so tenant flows spread over all paths.
[^c55-3]: Broadcast, unknown-unicast and multicast frames; the source VTEP sends a separate unicast copy to each peer (ingress replication).

## [5.6]{.sec}EVPN: a control plane for the overlay [Should · ■■■]{.tag} {#s5-6}

::: bigidea
EVPN lets the same BGP that routes the underlay also advertise which MAC and IP addresses live behind which VTEP, so switches no longer flood to discover hosts and a host move is a routing update.
:::

Flood-and-learn makes every VTEP discover hosts by seeing traffic. *BGP EVPN* (RFC 7432, with RFC 8365 for its use over VXLAN) replaces this with advertisements. It is a BGP address family (AFI 25, SAFI 70, see [§4.7](#s4-7){.ref}) whose routes are of several *types*, each distinguished by a number. Each leaf learns local MAC and IP addresses from its attached hosts and advertises them with its VTEP address as the next hop; every other leaf installs them. Reachability of all hosts is thus known before a packet is sent. The same sessions as the underlay can carry it, or the spines can act as route reflectors.

| Type | Name | Purpose | Key fields | You see it when |
|---|---|---|---|---|
| 1 | Ethernet auto-discovery | multihoming: fast withdrawal, aliasing | ESI, Ethernet tag | a server is attached to two leaves |
| 2 | MAC/IP advertisement | where a host MAC (and IP) lives | RD, ESI, MAC, IP, L2VNI (Label1), L3VNI (Label2) | a host appears or moves |
| 3 | Inclusive multicast | VTEP joins a VNI; builds the BUM list | VTEP address, VNI | a VNI is configured on a leaf |
| 4 | Ethernet segment | elects the designated forwarder per segment | ESI, VTEP address | multihoming |
| 5 | IP prefix | a whole subnet or external route | RD, prefix and length, gateway, L3VNI | a border leaf injects 0.0.0.0/0, or a subnet is advertised |

Types 2 and 5 carry most of the load. A Type-2 route says "this MAC, and optionally this IP, is behind me"; a Type-5 route says "this prefix is behind me" and is how a border leaf announces Campus Net's default route into a tenant. Types 1 and 4 support a server attached to two leaves (an *Ethernet segment identifier*, ESI) without a proprietary MLAG, and Type 3 builds the list of VTEPs to which BUM traffic is replicated. Routes also carry *route targets* (RT), extended communities that decide which VRF or VNI imports them. Note that with a different AS number on each leaf, automatically derived RTs would not match, so the fabric sets explicit RTs such as 65100:10010.

::: example
**A host moves from L1 to L3.** Host A (MAC aa:aa:aa:aa:aa:11, IP 10.1.10.11, VNI 10010, L3VNI 50001 in VRF CAMPUS) is a virtual machine that migrates.

1. Before the move L1 advertises a Type-2 route of the form shown below (without the mobility community); every leaf installs "MAC aa:aa:aa:aa:aa:11 is at VTEP 10.0.0.1".
2. After migration the VM sends a gratuitous ARP from its new host. L3 learns the MAC locally and finds that it already holds a *remote* route for it with no sequence number (treated as 0).
3. L3 advertises the same MAC, as shown below, with the *MAC-mobility* extended community and sequence number 1. The rule of RFC 7432 is that the highest sequence number wins.
4. Every leaf, including L1, prefers L3's route. L1 sees that its own local route has been superseded, deletes it and withdraws its advertisement (Figure 5.9).
5. Traffic from L5 reaches the VM through VTEP 10.0.0.3 as soon as the update is installed, typically within milliseconds, rather than after a flood or an aging timer.

```
Route type 2 (MAC/IP advertisement)
  RD            10.0.0.3:10010        ESI    0 (single-homed)
  MAC           aa:aa:aa:aa:aa:11     IP     10.1.10.11
  Label1        10010 (L2VNI)         Label2 50001 (L3VNI)
  Ext. comms    RT 65100:10010  RT 65100:50001  MAC-mobility seq 1  Router-MAC 00:aa:bb:00:00:03
```

[Result: the move is a single BGP update with a higher sequence number, and the old location is withdrawn.]{.result}
:::

<figure>
<svg viewBox="0 0 480 206" width="480"><defs><marker id="a59" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accf"/></marker><marker id="b59" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker></defs><text class="lbl" x="50" y="12" text-anchor="middle">L1</text><line class="lg" x1="50" y1="18" x2="50" y2="200"/><text class="lbl" x="170" y="12" text-anchor="middle">Spine RR</text><line class="lg" x1="170" y1="18" x2="170" y2="200"/><text class="lbl" x="290" y="12" text-anchor="middle">L3</text><line class="lg" x1="290" y1="18" x2="290" y2="200"/><text class="lbl" x="410" y="12" text-anchor="middle">L5</text><line class="lg" x1="410" y1="18" x2="410" y2="200"/><rect class="hl" x="240" y="26" width="100" height="18" rx="0"/><text class="sm" x="290" y="38" text-anchor="middle">host A appears (GARP)</text><line class="acc" x1="290" y1="62" x2="170" y2="62" marker-end="url(#a59)"/><text class="sm" x="230.0" y="59" text-anchor="middle">Type-2 MAC aa:aa, IP 10.1.10.11, seq 1</text><line class="ln" x1="170" y1="86" x2="50" y2="86" marker-end="url(#b59)"/><text class="sm" x="110.0" y="83" text-anchor="middle">reflect (seq 1 > seq 0)</text><line class="ln" x1="170" y1="100" x2="410" y2="100" marker-end="url(#b59)"/><text class="sm" x="290.0" y="97" text-anchor="middle">reflect</text><rect class="hl" x="10" y="108" width="80" height="18" rx="0"/><text class="sm" x="50" y="120" text-anchor="middle">L1 withdraws its</text><text class="sm" x="50" y="138" text-anchor="middle">local entry; installs</text><text class="sm" x="50" y="148" text-anchor="middle">remote via L3</text><line class="ln" x1="50" y1="166" x2="170" y2="166" marker-end="url(#b59)"/><text class="sm" x="110.0" y="163" text-anchor="middle">withdraw old Type-2</text><line class="ln" x1="170" y1="180" x2="410" y2="180" marker-end="url(#b59)"/><text class="sm" x="290.0" y="177" text-anchor="middle">reflect: L5 now sends to L3</text></svg>
<figcaption><b>Figure 5.9</b> A host moves from L1 to L3. The new advertisement carries a higher MAC-mobility sequence number, so every leaf prefers it at once; flood-and-learn would have waited for traffic or for aging.</figcaption>
</figure>

Three further mechanisms complete the design. *ARP suppression*: a leaf snoops the ARP requests of its local hosts and, because Type-2 routes already tell it the MAC of every known IP address, answers the request itself instead of flooding it across the fabric; only an unknown address is flooded. An *anycast gateway* gives every leaf the same gateway IP address (10.1.10.1) and the same virtual MAC, so a host always finds its default gateway on its own leaf and keeps it after a move; this is the fabric analogue of the first-hop redundancy of [§4.8](#s4-8){.ref}, with no active/standby pair. Finally, *integrated routing and bridging* (IRB, RFC 9135) decides how traffic crosses subnets. In the *symmetric* model, A on VLAN 10 at L1 sends to C on VLAN 20 at L3 like this: A forwards to the anycast gateway on L1; L1 routes the packet in VRF CAMPUS, looks up 10.1.20.31 and finds VTEP L3 with L3's *router MAC*; it encapsulates with the L3VNI 50001 and the inner destination MAC set to L3's router MAC; L3 decapsulates, looks the VRF up by L3VNI, routes into VLAN 20 and bridges to C. Both leaves route, and a leaf needs only the VNIs of its own hosts plus the L3VNI. In the *asymmetric* model the ingress leaf routes and then bridges directly in the destination's VNI, so every leaf must hold every VNI even where it has no hosts, which does not scale.

::: trap
*Claim:* "Type 5 and Type 2 with an IP address are interchangeable." *Why it is wrong:* a Type-2 route describes one host (a /32 or /128) learned from ARP or ND, and moves with the host; a Type-5 route describes a prefix learned from routing and carries no MAC. *Correct statement:* use Type 2 for hosts, Type 5 for subnets and external routes; importing the same RT into two tenants by accident also leaks their VRFs into each other.
:::

::: lens
[ARISTA · JUNIPER · NOKIA · CISCO · MICROSOFT]{.co}

Arista and Juniper interviews ask for the route types, with one example of each, and for the difference between symmetric and asymmetric IRB. A good answer begins with the motivation (no flooding, mobility, multihoming), draws the Type-2 fields from memory, and names the anycast gateway and ARP suppression as the two features that remove flooding for user traffic. A common scenario is "a VM moves and traffic blackholes for thirty seconds": the answer is the MAC-mobility sequence number, plus a gratuitous ARP from the VM.
:::

::: check
1. Which EVPN route type carries the L2VNI and L3VNI of a host? [^c56-1]
2. What makes the new location of a moved MAC win? [^c56-2]
3. What does ARP suppression avoid? [^c56-3]
:::

[^c56-1]: Type 2 (MAC/IP advertisement), in its Label1 and Label2 fields.
[^c56-2]: A higher MAC-mobility sequence number.
[^c56-3]: Flooding ARP requests across the fabric; the leaf answers from the bindings learnt through Type-2 routes.

## [5.7]{.sec}SDN, OpenFlow and P4 [Should · ■■□]{.tag} {#s5-7}

::: bigidea
Software-defined networking moves the decisions out of each switch into a logically central controller and leaves the switch with a fast table lookup; P4 goes one step further and lets the operator define what the table and the packet parser look like.
:::

In a traditional device the *control plane* (routing protocols that decide) and the *data plane* (hardware that forwards) share a box, and each device decides alone. *Software-defined networking* (SDN) separates them: a *controller* holds the network-wide view, computes the forwarding rules and installs them in switches through a *southbound* interface; applications ask the controller for services through a *northbound* interface, often REST or gRPC (Figure 5.10). Two motivations drive it. A central view allows global optimisation that a distributed protocol cannot do, and a programmable interface lets software, not command-line scripts, manage thousands of devices. Google's B4 wide-area network, whose controller computes traffic-engineering paths, is the standard example, and Google's data-centre controller does the same for the Jupiter fabric.

*OpenFlow* is the protocol that first standardised the southbound interface. A switch holds one or more *flow tables*. Each *flow entry* has a *match* (fields from the packet headers and the ingress port), a *priority*, *counters*, *instructions* (actions such as output to a port, drop, rewrite a field, or go to the next table) and *timeouts*. The switch compares a packet with the entries in priority order and applies the first match. A *table miss*, when no entry matches, is itself handled by a low-priority entry; commonly it sends the packet to the controller as a *packet-in*, and the controller reacts by installing a flow. Installing flows only on demand is *reactive*; installing them in advance is *proactive*. A reactive design stalls when the controller is unreachable, whereas a proactive one keeps forwarding.

::: example
**Three OpenFlow rules on Open vSwitch.** In Mininet, switch `s1` has host h1 on port 1 and host h2 (10.0.0.2) on port 2.

```
ovs-ofctl add-flow s1 "priority=100,ip,nw_dst=10.0.0.2,actions=output:2"
ovs-ofctl add-flow s1 "priority=50,arp,actions=FLOOD"
ovs-ofctl add-flow s1 "priority=0,actions=CONTROLLER:65535"
ovs-ofctl dump-flows s1
```

```
priority=100,ip,nw_dst=10.0.0.2 actions=output:2         n_packets=5, n_bytes=490
priority=50,arp actions=FLOOD                            n_packets=2, n_bytes=84
priority=0 actions=CONTROLLER:65535                      n_packets=1, n_bytes=98
```

1. The first ARP from h1 matches priority 50 and is flooded (2 packets).
2. The echo requests to 10.0.0.2 match priority 100 and go to port 2; the counters rise with each ping (5 here).
3. Anything else, such as a packet to an unknown address, falls to priority 0 and is sent to the controller (1 packet).

[Result: matching is by priority, counters show which rule fires, and the priority-0 entry is the table-miss rule.]{.result}
:::

<figure>
<svg viewBox="0 0 480 160" width="480"><defs><marker id="a510" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker></defs><text class="lbl" x="95" y="12" text-anchor="middle">SDN layers</text><rect class="box" x="25" y="22" width="140" height="28" rx="0"/><text class="lbl" x="95" y="34" text-anchor="middle">Applications</text><text class="sm" x="95" y="45" text-anchor="middle">routing · TE · policy · LB</text><rect class="box" x="25" y="76" width="140" height="28" rx="0"/><text class="lbl" x="95" y="88" text-anchor="middle">Controller</text><text class="sm" x="95" y="99" text-anchor="middle">ONOS · Ryu · in-house</text><rect class="box" x="10" y="130" width="52" height="24" rx="0"/><text class="sm" x="36" y="145" text-anchor="middle">Switch</text><line class="lg" x1="36" y1="130" x2="95" y2="104"/><rect class="box" x="72" y="130" width="52" height="24" rx="0"/><text class="sm" x="98" y="145" text-anchor="middle">Switch</text><line class="lg" x1="98" y1="130" x2="95" y2="104"/><rect class="box" x="134" y="130" width="52" height="24" rx="0"/><text class="sm" x="160" y="145" text-anchor="middle">Switch</text><line class="lg" x1="160" y1="130" x2="95" y2="104"/><line class="ln" x1="95" y1="50" x2="95" y2="76"/><text class="sm" x="100" y="66" text-anchor="start">northbound: REST, gRPC</text><text class="sm" x="100" y="121" text-anchor="start">southbound: OpenFlow, P4Runtime, gNMI</text><text class="lbl" x="350" y="12" text-anchor="middle">PISA pipeline (P4 target)</text><rect class="box" x="212" y="40" width="50" height="50" rx="0"/><text class="lbl" x="237.0" y="62" text-anchor="middle">Parser</text><rect class="box" x="274" y="40" width="44" height="50" rx="0"/><text class="sm" x="296.0" y="62" text-anchor="middle">Stage 1</text><rect class="box" x="330" y="40" width="44" height="50" rx="0"/><text class="sm" x="352.0" y="62" text-anchor="middle">Stage 2</text><rect class="box" x="386" y="40" width="44" height="50" rx="0"/><text class="sm" x="408.0" y="62" text-anchor="middle">Stage N</text><rect class="box" x="442" y="40" width="38" height="50" rx="0"/><text class="sm" x="461.0" y="62" text-anchor="middle">Deparser</text><text class="sm" x="296.0" y="76" text-anchor="middle">table</text><text class="sm" x="296.0" y="85" text-anchor="middle">+ ALU</text><text class="sm" x="352.0" y="76" text-anchor="middle">table</text><text class="sm" x="352.0" y="85" text-anchor="middle">+ ALU</text><text class="sm" x="408.0" y="76" text-anchor="middle">table</text><text class="sm" x="408.0" y="85" text-anchor="middle">+ ALU</text><line class="ln" x1="262" y1="65" x2="274" y2="65" marker-end="url(#a510)"/><line class="ln" x1="318" y1="65" x2="330" y2="65" marker-end="url(#a510)"/><line class="ln" x1="374" y1="65" x2="386" y2="65" marker-end="url(#a510)"/><line class="ln" x1="430" y1="65" x2="442" y2="65" marker-end="url(#a510)"/><line class="lg dash" x1="212" y1="104" x2="480" y2="104"/><text class="sm" x="346" y="118" text-anchor="middle">metadata bus (ingress port, next hop, user fields)</text><text class="sm" x="237" y="32" text-anchor="middle">bytes in</text><text class="sm" x="461" y="32" text-anchor="middle">bytes out</text><text class="sm" x="346" y="140" text-anchor="middle">The parser and each table are programmed in P4.</text></svg>
<figcaption><b>Figure 5.10</b> Left: the SDN split between applications, a logically central controller and simple switches. Right: the protocol-independent switch architecture that P4 targets, in which the parser, the tables and the deparser are all defined by the program.</figcaption>
</figure>

OpenFlow fixes the set of headers that a switch can match. *P4* (Programming Protocol-independent Packet Processors) removes that limit. A P4 program describes a *parser* (a state machine that extracts headers from the bytes), a sequence of *match-action tables* and a *deparser* that reassembles the packet; the hardware, a *protocol-independent switch architecture* (PISA) chip, executes it at line rate. The program therefore defines new protocols, for instance a custom telemetry header, without waiting for a silicon revision. The control plane then fills the tables through P4Runtime. The fragment below forwards IPv4 by longest prefix, which is the standard first exercise.

```
parser MyParser(packet_in pkt, out headers hdr, inout metadata meta,
                inout standard_metadata_t std) {
    state start {
        pkt.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            0x0800: parse_ipv4;
            default: accept;
        }
    }
    state parse_ipv4 { pkt.extract(hdr.ipv4); transition accept; }
}
control MyIngress(inout headers hdr, inout metadata meta,
                  inout standard_metadata_t std) {
    action drop() { mark_to_drop(std); }
    action forward(bit<48> dst, bit<9> port) {
        std.egress_spec = port;
        hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
        hdr.ethernet.dstAddr = dst;
        hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
    }
    table ipv4_lpm {
        key = { hdr.ipv4.dstAddr: lpm; }
        actions = { forward; drop; }
        default_action = drop();
    }
    apply { if (hdr.ipv4.isValid()) { ipv4_lpm.apply(); } }
}
```

The `lpm` key kind asks the hardware to do a longest-prefix match, which §5.8 shows to be a ternary or algorithmic lookup. The action `forward` is what a router does after a lookup: rewrite the MAC addresses, decrement the TTL ([§3.5](#s3-5){.ref}) and pick the port.

::: trap
*Claim:* "SDN means the end of distributed routing protocols." *Why it is wrong:* most production data centres still run BGP for the underlay (§5.4); a controller usually manages policy, traffic engineering or the virtual-network overlay on top. *Correct statement:* SDN centralises selected decisions, and a controller outage need not stop forwarding if the flows were installed proactively.
:::

::: check
1. What happens on an OpenFlow table miss? [^c57-1]
2. What can P4 do that OpenFlow cannot? [^c57-2]
3. Name the two interface directions of an SDN controller. [^c57-3]
:::

[^c57-1]: A low-priority table-miss entry decides; commonly the packet goes to the controller as a packet-in.
[^c57-2]: Define the parser and the headers themselves, so new protocols are supported without new silicon.
[^c57-3]: Northbound toward applications (REST, gRPC) and southbound toward switches (OpenFlow, P4Runtime, gNMI).

:::
