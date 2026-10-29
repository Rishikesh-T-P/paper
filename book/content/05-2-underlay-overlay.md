::: {.p5}

## [5.4]{.sec}The eBGP underlay, BFD and unnumbered links [Must · ■■□]{.tag} {#s5-4}

::: bigidea
In a large fabric each switch runs eBGP to its neighbours, because BGP offers simple per-link policy, bounded failure scope and no flooding, and fast failure detection is added with BFD.
:::

The *underlay* is the routed network that carries every packet between the fabric's switches; the *overlay* (§5.5) is the virtual network carried on top of it. Pillar 4 taught OSPF and IS-IS ([§4.5](#s4-5){.ref}), which would also work here, but RFC 7938 documents why the large operators chose BGP instead. A link-state protocol floods every change to every switch and every switch runs the shortest-path calculation, so thousands of devices produce heavy churn; BGP sends an update only to a neighbour, which limits the effect of a failure to the paths that used it. BGP has a rich policy model (communities, route maps) for draining a device for maintenance, it uses TCP and so needs no extra protocol, and one protocol covers both the fabric and the edge to the outside world. The cost is a more careful design: every switch needs an AS number, and the usual loop-prevention rule must work with it.

The standard plan gives all the spines one AS number and each leaf its own. Campus Net's fabric uses private numbers: spines in AS 65100, and leaves L1 to L4 in AS 65101 to 65104 (Campus Net's border routers remain in AS 65000, [§4.7](#s4-7){.ref}). When L1 advertises its server subnet 10.1.1.0/24, spine S1 receives it with AS_PATH 65101 and passes it on to L4 with AS_PATH 65100 65101 (Figure 5.7). The shared spine AS has two useful effects. A route can only go *up* to a spine and *down* to a leaf: if L4 tried to advertise it back up to S2, S2 would see its own AS number 65100 in the path and discard it, which prevents "valleys" and the path-hunting that would follow a failure. The leaves, conversely, must have *different* AS numbers; two leaves sharing an AS would reject each other's routes for the same reason, and the fix would be `allowas-in` on the leaves, which weakens the loop protection.

<figure>
<svg viewBox="0 0 480 204" width="480"><defs><marker id="a56" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accf"/></marker></defs><rect class="box" x="115" y="10" width="90" height="26" rx="0"/><text class="lbl" x="160" y="23" text-anchor="middle">S1</text><text class="sm" x="160" y="32" text-anchor="middle">AS 65100</text><rect class="box" x="275" y="10" width="90" height="26" rx="0"/><text class="lbl" x="320" y="23" text-anchor="middle">S2</text><text class="sm" x="320" y="32" text-anchor="middle">AS 65100</text><rect class="box" x="30" y="118" width="80" height="26" rx="0"/><text class="lbl" x="70" y="131" text-anchor="middle">L1</text><text class="sm" x="70" y="140" text-anchor="middle">AS 65101</text><line class="lg" x1="160" y1="36" x2="70" y2="118"/><line class="lg" x1="320" y1="36" x2="70" y2="118"/><rect class="box" x="150" y="118" width="80" height="26" rx="0"/><text class="lbl" x="190" y="131" text-anchor="middle">L2</text><text class="sm" x="190" y="140" text-anchor="middle">AS 65102</text><line class="lg" x1="160" y1="36" x2="190" y2="118"/><line class="lg" x1="320" y1="36" x2="190" y2="118"/><rect class="box" x="250" y="118" width="80" height="26" rx="0"/><text class="lbl" x="290" y="131" text-anchor="middle">L3</text><text class="sm" x="290" y="140" text-anchor="middle">AS 65103</text><line class="lg" x1="160" y1="36" x2="290" y2="118"/><line class="lg" x1="320" y1="36" x2="290" y2="118"/><rect class="box" x="370" y="118" width="80" height="26" rx="0"/><text class="lbl" x="410" y="131" text-anchor="middle">L4</text><text class="sm" x="410" y="140" text-anchor="middle">AS 65104</text><line class="lg" x1="160" y1="36" x2="410" y2="118"/><line class="lg" x1="320" y1="36" x2="410" y2="118"/><path class="acc" d="M70,118 L160,36 L410,118" marker-end="url(#a56)"/><text class="sm" x="70" y="158" text-anchor="middle">10.1.1.0/24</text><text class="sm" x="410" y="158" text-anchor="middle">10.1.4.0/24</text><rect class="hl" x="10" y="168" width="120" height="28" rx="0"/><text class="sm" x="70" y="180" text-anchor="middle">on S1, learnt from L1:</text><text class="mono" x="70" y="191" text-anchor="middle">AS_PATH 65101</text><rect class="hl" x="330" y="168" width="140" height="28" rx="0"/><text class="sm" x="400" y="180" text-anchor="middle">on L4, learnt from S1:</text><text class="mono" x="400" y="191" text-anchor="middle">AS_PATH 65100 65101</text></svg>
<figcaption><b>Figure 5.7</b> An eBGP fabric. Spines share one ASN and each leaf has its own. The route to L1's subnet reaches L4 with the path 65100 65101; S2 would refuse any path that already contains 65100, which keeps routes from bouncing back up.</figcaption>
</figure>

Two details make ECMP work. By default BGP installs several paths only if their AS_PATH attributes are identical in the relevant parts; with the plan above the two paths from L4 to L1 are both "65100 65101", so `maximum-paths 8` is enough. If the spines had different AS numbers the paths would differ in content though not in length, and the command `bestpath as-path multipath-relax` is needed. Secondly, private AS numbers are scarce: the 2-byte private range 64512 to 65534 holds only 1,023 numbers, which a large fabric exhausts, so big operators use the 4-byte private range 4200000000 to 4294967294.

Convergence is the other half of the design. A BGP hold timer is 180 s by default, so a neighbour that fails silently would be believed for three minutes. *Bidirectional Forwarding Detection* (BFD, RFC 5880) is a lightweight hello protocol, run in hardware, that tells BGP when a path is dead. With a transmit interval of 300 ms and a multiplier of 3 a failure is detected after 3 × 300 ms = 900 ms.

| Mechanism | Detection time | Notes |
|---|---|---|
| Interface goes down | milliseconds | only if the physical signal is lost |
| BFD, 300 ms × 3 | 0.9 s | independent of the physical layer |
| BGP keepalive and hold, tuned to 3 s / 9 s | up to 9 s | common data-centre setting |
| BGP default hold timer | up to 180 s | the default; far too slow |

The last refinement removes IP addresses from the links. In *BGP unnumbered* the two ends of a link do not carry IPv4 addresses; the session runs over the IPv6 link-local addresses, which every IPv6 interface has automatically, and IPv4 routes are carried with an IPv6 next hop (RFC 5549, now RFC 8950). A fabric of 64 leaves and 8 spines has 512 links; numbering each with a /31 would consume 1,024 addresses and make 512 subnets to track, whereas unnumbered links need only one loopback address per switch. In FRR the whole neighbour configuration is two lines.

```
router bgp 65101
 bgp router-id 10.0.0.1
 neighbor swp1 interface remote-as external
 neighbor swp2 interface remote-as external
 neighbor swp1 bfd
 neighbor swp2 bfd
 address-family ipv4 unicast
  redistribute connected
  maximum-paths 8
```

::: lab
`LAB 5.4 · 3 H`  Containerlab with FRR images: two spines (AS 65100) and four leaves (AS 65101 to 65104), loopbacks 10.0.0.1 to 10.0.0.4 on the leaves, one server subnet per leaf. Configure the block above on every leaf and the mirror image on the spines, then verify.

```
leaf4# show bgp summary
leaf4# show ip route 10.1.1.0/24
```

```
Neighbor   V   AS     State/PfxRcd
swp1(S1)   4   65100  6
swp2(S2)   4   65100  6

B>* 10.1.1.0/24 [20/0] via fe80::a8bb:ccff:fe00:100, swp1, weight 1
  *                    via fe80::a8bb:ccff:fe00:200, swp2, weight 1
```

**What you should notice:** each leaf has exactly two sessions, and the route to another leaf's subnet has two next hops (ECMP). Shut one spine-facing port and the route falls to one next hop within about a second when BFD is on; remove the `bfd` lines and the failure of a link whose carrier stays up takes the full hold time to notice.
:::

::: trap
*Claim:* "Two leaves in the same AS will simply peer through the spines." *Why it is wrong:* the receiving leaf sees its own AS in the AS_PATH and discards the update as a loop. *Correct statement:* give each leaf (or each rack pair) its own AS number, or enable `allowas-in` knowingly and accept the weaker protection.
:::

::: lens
[GOOGLE · MICROSOFT · AMAZON · ARISTA · JUNIPER]{.co}

"Why eBGP and not OSPF in the data centre?" wants three reasons from the text above (smaller failure scope, policy and drain control, one protocol to the edge), the ASN plan and the reason for the shared spine AS, and BFD for sub-second failover. Backbone roles at Amazon and Microsoft also ask about IS-IS and MPLS, taught in [§4.10](#s4-10){.ref}.
:::

::: check
1. Why do spines share one AS number? [^c54-1]
2. How long does BFD with 300 ms and a multiplier of 3 take to detect a failure? [^c54-2]
3. What does BGP unnumbered use in place of an IPv4 address on the link? [^c54-3]
:::

[^c54-1]: A route may then only travel up and down, because a spine rejects any path that already contains its own AS; this prevents valley paths.
[^c54-2]: 900 ms.
[^c54-3]: The IPv6 link-local address, with IPv4 prefixes advertised over an IPv6 next hop.

## [5.5]{.sec}Overlays: VXLAN [Must · ■■□]{.tag} {#s5-5}

::: bigidea
VXLAN carries a tenant's Ethernet frame inside a UDP packet between two switches, so tenants obtain layer-2 networks over a routed fabric, with 16 million segment identifiers in place of 4,094 VLANs, at the price of 50 bytes of header per packet.
:::

A virtual machine keeps its IP address when it moves, which is easy only if the new host is in the same layer-2 segment; yet the fabric of §5.4 is routed, and routers do not extend layer-2 segments. The solution is an *overlay*: the endpoints of the virtual network wrap each tenant frame in an ordinary IP packet, the routed *underlay* delivers it, and the far endpoint unwraps it. *VXLAN* (Virtual eXtensible LAN, RFC 7348) is the dominant overlay. The device that wraps and unwraps is the *VTEP* (VXLAN tunnel endpoint); it may be a leaf switch or the virtual switch of a hypervisor, and it has an IP address, usually a loopback, that appears as the outer address. A 24-bit *VXLAN network identifier* (VNI) names the tenant segment, giving 2²⁴ = 16,777,216 segments. The outer packet is UDP with destination port 4789.

The encapsulation is shown in Figure 5.8. The VXLAN header itself is eight bytes: a flags byte whose "I" bit (0x08) says that the VNI is valid, three reserved bytes, the three-byte VNI, and one reserved byte. The *source* UDP port is not fixed: the VTEP computes it as a hash of the inner Ethernet, IP and transport headers, within the ephemeral range. This is deliberate. The underlay's ECMP hash (§5.3) sees only the outer 5-tuple, and all packets between two VTEPs would otherwise share one tuple and one path; with the inner flow hashed into the source port, different tenant flows take different spines, and each flow stays in order.

<figure>
<svg viewBox="0 0 480 190" width="480"><defs></defs><rect class="box" x="8" y="16" width="42" height="26" rx="0"/><text class="lbl" x="29.0" y="32" text-anchor="middle">Outer Eth</text><text class="sm" x="29.0" y="54" text-anchor="middle">14</text><rect class="box" x="50" y="16" width="60" height="26" rx="0"/><text class="lbl" x="80.0" y="32" text-anchor="middle">Outer IP</text><text class="sm" x="80.0" y="54" text-anchor="middle">20</text><rect class="box" x="110" y="16" width="24" height="26" rx="0"/><text class="sm" x="122.0" y="32" text-anchor="middle">UDP</text><text class="sm" x="122.0" y="54" text-anchor="middle">8</text><rect class="fill" x="134" y="16" width="24" height="26" rx="0"/><text class="sm" x="146.0" y="32" text-anchor="middle">VX</text><text class="sm" x="146.0" y="54" text-anchor="middle">8</text><rect class="fill" x="158" y="16" width="42" height="26" rx="0"/><text class="lbl" x="179.0" y="32" text-anchor="middle">Inner Eth</text><text class="sm" x="179.0" y="54" text-anchor="middle">14</text><rect class="fill" x="200" y="16" width="190" height="26" rx="0"/><text class="lbl" x="295.0" y="32" text-anchor="middle">Inner IP + payload (the tenant's packet)</text><rect class="box" x="390" y="16" width="14" height="26" rx="0"/><text class="sm" x="397.0" y="32" text-anchor="middle">FCS</text><text class="sm" x="397.0" y="54" text-anchor="middle">4</text><path class="acc" d="M8,60 L158,60"/><text class="lbl acct" x="83.0" y="72" text-anchor="middle">50 bytes added by the VTEP</text><text class="sm" x="122" y="86" text-anchor="middle">dst port 4789</text><text class="sm" x="152" y="98" text-anchor="middle"></text><text class="lbl" x="8" y="108" text-anchor="start">VXLAN header (8 bytes), bit positions</text><text class="sm" x="40" y="122" text-anchor="middle">0</text><text class="sm" x="136" y="122" text-anchor="middle">8</text><text class="sm" x="232" y="122" text-anchor="middle">16</text><text class="sm" x="328" y="122" text-anchor="middle">24</text><text class="sm" x="418" y="122" text-anchor="middle">31</text><rect class="hl" x="40" y="126" width="96" height="24" rx="0"/><text class="sm" x="88.0" y="141" text-anchor="middle">Flags: R R R R I R R R</text><rect class="box" x="136" y="126" width="288" height="24" rx="0"/><text class="lbl" x="280.0" y="141" text-anchor="middle">Reserved</text><rect class="hl" x="40" y="150" width="288" height="24" rx="0"/><text class="lbl" x="184.0" y="165" text-anchor="middle">VNI (24 bits)</text><rect class="box" x="328" y="150" width="96" height="24" rx="0"/><text class="sm" x="376.0" y="165" text-anchor="middle">Reserved</text><text class="sm" x="34" y="141" text-anchor="end">0</text><text class="sm" x="34" y="165" text-anchor="end">4</text></svg>
<figcaption><b>Figure 5.8</b> VXLAN encapsulation. Byte counts are under each block. The I flag (value 0x08) says the VNI is valid; the 24-bit VNI allows 16,777,216 segments.</figcaption>
</figure>

::: example
**Overhead and MTU for a 1,500-byte tenant packet.** Campus Net's SALES servers (VLAN 10, 10.1.10.0/24) are given VNI 10010 and appear on two racks; a packet from Host A on L1 to Host B on L2 crosses the fabric (Figure 5.9).

1. The tenant frame is the inner Ethernet header (14 bytes) plus a 1,500-byte IP packet: 1,514 bytes.
2. The VTEP adds a VXLAN header (8), an outer UDP header (8), an outer IPv4 header (20) and an outer Ethernet header (14): 50 bytes in all.
3. The outer IP packet is 20 + 8 + 8 + 1,514 = 1,550 bytes, so the underlay IP MTU must be at least 1,550. On the wire the frame is 1,564 bytes (1,568 with the FCS).
4. If the outer header is IPv6 (40 bytes instead of 20), the overhead is 70 bytes and the minimum underlay MTU is 1,570.
5. Fabrics therefore set the underlay MTU to 9,216 (jumbo frames) and leave the tenant MTU at 1,500 or 9,000. If the underlay stays at 1,500, the usable tenant MTU is 1,500 − 50 = 1,450 for the IP packet, which Linux sets automatically on a VXLAN interface.

[Result: 50 bytes of encapsulation (70 over IPv6); underlay IP MTU at least 1,550; jumbo frames avoid the problem.]{.result}
:::

<figure>
<svg viewBox="0 0 480 210" width="480"><defs><marker id="a58" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accf"/></marker></defs><rect class="box" x="5" y="70" width="52" height="26" rx="0"/><text class="lbl" x="31" y="83" text-anchor="middle">Host A</text><text class="sm" x="31" y="92" text-anchor="middle">VNI 10010</text><rect class="box" x="80" y="64" width="88" height="38" rx="0"/><text class="lbl" x="124" y="79" text-anchor="middle">Leaf L1</text><text class="sm" x="124" y="90" text-anchor="middle">VTEP 10.0.0.1</text><rect class="box" x="210" y="16" width="60" height="22" rx="0"/><text class="lbl" x="240" y="30" text-anchor="middle">Spine S1</text><rect class="box" x="210" y="118" width="60" height="22" rx="0"/><text class="lbl" x="240" y="132" text-anchor="middle">Spine S2</text><rect class="box" x="312" y="64" width="88" height="38" rx="0"/><text class="lbl" x="356" y="79" text-anchor="middle">Leaf L2</text><text class="sm" x="356" y="90" text-anchor="middle">VTEP 10.0.0.2</text><rect class="box" x="423" y="70" width="52" height="26" rx="0"/><text class="lbl" x="449" y="83" text-anchor="middle">Host B</text><text class="sm" x="449" y="92" text-anchor="middle">VNI 10010</text><line class="ln" x1="57" y1="83" x2="80" y2="83"/><line class="ln" x1="400" y1="83" x2="423" y2="83"/><line class="lg" x1="168" y1="76" x2="210" y2="27"/><line class="lg" x1="168" y1="90" x2="210" y2="129"/><line class="lg" x1="270" y1="27" x2="312" y2="76"/><line class="lg" x1="270" y1="129" x2="312" y2="90"/><path class="acc" d="M168,76 L210,27 M270,27 L312,76" marker-end="url(#a58)"/><text class="sm" x="240" y="60" text-anchor="middle">underlay: routed IP</text><text class="sm" x="240" y="76" text-anchor="middle">(ECMP picks S1 or S2</text><text class="sm" x="240" y="86" text-anchor="middle">from the outer UDP port)</text><rect class="fill" x="8" y="158" width="464" height="20" rx="0"/><text class="mono" x="14" y="171" text-anchor="start">on the access links:  Eth(A→B) | IP | payload</text><rect class="hl" x="8" y="182" width="464" height="20" rx="0"/><text class="mono" x="14" y="195" text-anchor="start">in the fabric:  IP 10.0.0.1→10.0.0.2 | UDP →4789 | VXLAN VNI 10010 | Eth(A→B) | IP | payload</text></svg>
<figcaption><b>Figure 5.9</b> A frame from Host A to Host B across the overlay. L1 wraps the tenant frame in an outer IP and UDP packet addressed to L2's loopback; the spines forward it as ordinary IP and never see the inner Ethernet header.</figcaption>
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
4. Every leaf, including L1, prefers L3's route. L1 sees that its own local route has been superseded, deletes it and withdraws its advertisement (Figure 5.10).
5. Traffic from L5 reaches the VM through VTEP 10.0.0.3 as soon as the update is installed, typically within milliseconds, rather than after a flood or an aging timer.

```
Route type 2 (MAC/IP advertisement)
  RD            10.0.0.3:10010        ESI    0 (single-homed)
  MAC           aa:aa:aa:aa:aa:11     IP     10.1.10.11
  Label1        10010 (L2VNI)         Label2 50001 (L3VNI)
  Ext. comms    RT 65100:10010  RT 65100:50001
                MAC-mobility seq 1  Router-MAC 00:aa:bb:00:00:03
```

[Result: the move is a single BGP update with a higher sequence number, and the old location is withdrawn.]{.result}
:::

<figure>
<svg viewBox="0 0 480 204" width="480"><defs><marker id="a59" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accf"/></marker><marker id="b59" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker></defs><text class="lbl" x="50" y="12" text-anchor="middle">L1</text><line class="lg" x1="50" y1="18" x2="50" y2="196"/><text class="lbl" x="190" y="12" text-anchor="middle">Spine RR</text><line class="lg" x1="190" y1="18" x2="190" y2="196"/><text class="lbl" x="330" y="12" text-anchor="middle">L3</text><line class="lg" x1="330" y1="18" x2="330" y2="196"/><text class="lbl" x="450" y="12" text-anchor="middle">L5</text><line class="lg" x1="450" y1="18" x2="450" y2="196"/><rect class="hl" x="262" y="24" width="136" height="16" rx="0"/><text class="sm" x="330" y="35" text-anchor="middle">host A appears at L3 (GARP)</text><line class="acc" x1="330" y1="62" x2="190" y2="62" marker-end="url(#a59)"/><text class="sm" x="260.0" y="59" text-anchor="middle">Type-2 aa:aa, seq 1</text><line class="ln" x1="190" y1="86" x2="50" y2="86" marker-end="url(#b59)"/><text class="sm" x="120.0" y="83" text-anchor="middle">reflect (seq 1 beats 0)</text><line class="ln" x1="190" y1="104" x2="450" y2="104" marker-end="url(#b59)"/><text class="sm" x="320.0" y="101" text-anchor="middle">reflect</text><rect class="hl" x="58" y="114" width="126" height="16" rx="0"/><text class="sm" x="121" y="125" text-anchor="middle">L1 drops its local entry</text><line class="ln" x1="50" y1="152" x2="190" y2="152" marker-end="url(#b59)"/><text class="sm" x="120.0" y="149" text-anchor="middle">withdraw old Type-2</text><line class="ln" x1="190" y1="178" x2="450" y2="178" marker-end="url(#b59)"/><text class="sm" x="320.0" y="175" text-anchor="middle">reflect: L5 now sends to L3</text></svg>
<figcaption><b>Figure 5.10</b> A host moves from L1 to L3. The new advertisement carries a higher MAC-mobility sequence number, so every leaf prefers it at once; flood-and-learn would have waited for traffic or for aging.</figcaption>
</figure>

Three further mechanisms complete the design. *ARP suppression*: a leaf snoops the ARP requests of its local hosts and, because Type-2 routes already tell it the MAC of every known IP address, answers the request itself instead of flooding it across the fabric; only an unknown address is flooded. An *anycast gateway* gives every leaf the same gateway IP address (10.1.10.1) and the same virtual MAC, so a host always finds its default gateway on its own leaf and keeps it after a move; this is the fabric analogue of the first-hop redundancy of [§4.8](#s4-8){.ref}, with no active/standby pair. Finally, *integrated routing and bridging* (IRB, RFC 9135) decides how traffic crosses subnets. In the *symmetric* model, A on VLAN 10 at L1 sends to C on VLAN 20 at L3 like this: A forwards to the anycast gateway on L1; L1 routes the packet in VRF CAMPUS, looks up 10.1.20.31 and finds VTEP L3 with L3's *router MAC*; it encapsulates with the L3VNI 50001 and the inner destination MAC set to L3's router MAC; L3 decapsulates, looks the VRF up by L3VNI, routes into VLAN 20 and bridges to C. Both leaves route (Figure 5.11), and a leaf needs only the VNIs of its own hosts plus the L3VNI. In the *asymmetric* model the ingress leaf routes and then bridges directly in the destination's VNI, so every leaf must hold every VNI even where it has no hosts, which does not scale.

<figure>
<svg viewBox="0 0 480 194" width="480"><defs><marker id="a5i" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accf"/></marker><marker id="b5i" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker></defs><rect class="box" x="6" y="60" width="60" height="28" rx="0"/><text class="lbl" x="36" y="72" text-anchor="middle">Host A</text><text class="sm" x="36" y="83" text-anchor="middle">VLAN 10</text><rect class="box" x="86" y="50" width="92" height="48" rx="0"/><text class="lbl" x="132" y="64" text-anchor="middle">Leaf L1</text><text class="sm" x="132" y="75" text-anchor="middle">VTEP 10.0.0.1</text><text class="sm" x="132" y="86" text-anchor="middle">gw 10.1.10.1</text><rect class="box" x="206" y="6" width="68" height="22" rx="0"/><text class="lbl" x="240" y="20" text-anchor="middle">Spine</text><rect class="box" x="302" y="50" width="92" height="48" rx="0"/><text class="lbl" x="348" y="64" text-anchor="middle">Leaf L3</text><text class="sm" x="348" y="75" text-anchor="middle">VTEP 10.0.0.3</text><text class="sm" x="348" y="86" text-anchor="middle">gw 10.1.20.1</text><rect class="box" x="414" y="60" width="60" height="28" rx="0"/><text class="lbl" x="444" y="72" text-anchor="middle">Host C</text><text class="sm" x="444" y="83" text-anchor="middle">VLAN 20</text><line class="ln" x1="66" y1="74" x2="86" y2="74" marker-end="url(#b5i)"/><line class="ln" x1="394" y1="74" x2="414" y2="74" marker-end="url(#b5i)"/><path class="acc" d="M178,60 L206,22 M274,22 L302,60" marker-end="url(#a5i)"/><text class="lbl" x="76" y="50" text-anchor="middle">1</text><text class="lbl" x="240" y="58" text-anchor="middle">2</text><text class="lbl" x="352" y="112" text-anchor="middle">3</text><text class="lbl" x="404" y="52" text-anchor="middle">4</text><rect class="hl" x="10" y="120" width="460" height="16" rx="0"/><text class="mono" x="16" y="131" text-anchor="start">outer 10.0.0.1→10.0.0.3 | UDP 4789 | VNI 50001 | dst MAC = L3 router MAC | IP A→C</text><text class="sm" x="8" y="152" text-anchor="start">1  A sends to its gateway, the anycast address on L1 (same IP and MAC on every leaf)</text><text class="sm" x="8" y="163" text-anchor="start">2  L1 routes inside VRF CAMPUS, finds C behind VTEP L3, encapsulates in the L3VNI</text><text class="sm" x="8" y="174" text-anchor="start">3  L3 decapsulates, selects the VRF by the L3VNI, routes into VLAN 20</text><text class="sm" x="8" y="185" text-anchor="start">4  L3 bridges to Host C in VLAN 20</text></svg>
<figcaption><b>Figure 5.11</b> Symmetric IRB. Both leaves route, so the packet travels in the tenant's L3VNI and neither leaf needs the other's VLAN to exist locally.</figcaption>
</figure>

::: lab
`LAB 5.6 · 3 H`  Containerlab with FRR: the fabric of §5.4 with VNI 10010 on L1 and L3, and EVPN enabled on the same eBGP sessions (`address-family l2vpn evpn`, `advertise-all-vni`). Start a ping from a host on L1 to a host on L3 and read the routes.

```
leaf3# show bgp l2vpn evpn route type macip
leaf3# show evpn mac vni 10010
```

```
*> [2]:[0]:[48]:[aa:aa:aa:aa:aa:11]:[32]:[10.1.10.11]
   10.0.0.1  ... ET:8 RT:65100:10010
```

Now move the host: detach its interface from L1 and attach it to L3, then repeat the command on L5.

```
   10.0.0.3  ... ET:8 RT:65100:10010 MM:1
```

**What you should notice:** the next hop changes from 10.0.0.1 to 10.0.0.3 and the *MM:1* (MAC-mobility sequence 1) appears; the old route disappears once L1 withdraws it. With ARP suppression on, `tcpdump` on a spine shows no ARP request crossing the fabric.
:::

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

:::
