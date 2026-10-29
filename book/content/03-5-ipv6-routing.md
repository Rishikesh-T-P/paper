::: {.p3}

## [3.7]{.sec}IPv6 essentials [Should · ■■□]{.tag} {#s3-7}

IPv4 has about 4.3 billion addresses, and they ran out at the registries between 2011 and 2015. IPv6 widens the address to 128 bits, a space so large that every subnet can be given 2⁶⁴ addresses. Its designers also simplified the header and removed several IPv4 mechanisms: there is no broadcast, no header checksum and no fragmentation by routers, and ARP is replaced by a neighbour discovery protocol built on ICMPv6. For Qualcomm, Nokia and Juniper this section is a Must.

::: bigidea
IPv6 solves the shortage by making addresses 128 bits and solves the overhead by making the header fixed at 40 bytes, leaving everything else to extension headers and to ICMPv6.
:::

### Notation and address types

An IPv6 address is eight groups of four hexadecimal digits separated by colons. Two rules shorten it: leading zeros in a group may be dropped, and one run of consecutive all-zero groups may be replaced by `::`, once only, because two would make the address ambiguous. If two runs tie, compress the longest, and the leftmost if they are equal.

<figure>
<svg viewBox="0 0 480 216" width="480">
<text class="sm" x="26.9" y="17" text-anchor="middle" >0</text>
<text class="sm" x="123.1" y="17" text-anchor="middle" >7</text>
<text class="sm" x="136.9" y="17" text-anchor="middle" >8</text>
<text class="sm" x="233.1" y="17" text-anchor="middle" >15</text>
<text class="sm" x="246.9" y="17" text-anchor="middle" >16</text>
<text class="sm" x="343.1" y="17" text-anchor="middle" >23</text>
<text class="sm" x="356.9" y="17" text-anchor="middle" >24</text>
<text class="sm" x="453.1" y="17" text-anchor="middle" >31</text>
<rect class="box" x="20" y="22" width="55.0" height="16" rx="0" />
<text class="lbl" x="47.5" y="33.0" text-anchor="middle" >Version 6</text>
<rect class="box" x="75.0" y="22" width="110.0" height="16" rx="0" />
<text class="lbl" x="130.0" y="33.0" text-anchor="middle" >Traffic Class 8</text>
<rect class="box" x="185.0" y="22" width="275.0" height="16" rx="0" />
<text class="lbl" x="322.5" y="33.0" text-anchor="middle" >Flow Label 20</text>
<rect class="box" x="20" y="38" width="220.0" height="16" rx="0" />
<text class="lbl" x="130.0" y="49.0" text-anchor="middle" >Payload Length 16</text>
<rect class="box" x="240.0" y="38" width="110.0" height="16" rx="0" />
<text class="lbl" x="295.0" y="49.0" text-anchor="middle" >Next Header 8</text>
<rect class="hl" x="350.0" y="38" width="110.0" height="16" rx="0" />
<rect class="ln" x="350.0" y="38" width="110.0" height="16" rx="0" fill="none"/>
<text class="lbl" x="405.0" y="49.0" text-anchor="middle" >Hop Limit 8</text>
<rect class="box" x="20" y="54" width="440.0" height="16" rx="0" />
<text class="lbl" x="240.0" y="65.0" text-anchor="middle" >Source Address (128 bits)</text>
<rect class="box" x="20" y="70" width="440.0" height="16" rx="0" />
<text class="lbl" x="240.0" y="81.0" text-anchor="middle" ></text>
<rect class="box" x="20" y="86" width="440.0" height="16" rx="0" />
<text class="lbl" x="240.0" y="97.0" text-anchor="middle" ></text>
<rect class="box" x="20" y="102" width="440.0" height="16" rx="0" />
<text class="lbl" x="240.0" y="113.0" text-anchor="middle" ></text>
<rect class="box" x="20" y="118" width="440.0" height="16" rx="0" />
<text class="lbl" x="240.0" y="129.0" text-anchor="middle" >Destination Address (128 bits)</text>
<rect class="box" x="20" y="134" width="440.0" height="16" rx="0" />
<text class="lbl" x="240.0" y="145.0" text-anchor="middle" ></text>
<rect class="box" x="20" y="150" width="440.0" height="16" rx="0" />
<text class="lbl" x="240.0" y="161.0" text-anchor="middle" ></text>
<rect class="box" x="20" y="166" width="440.0" height="16" rx="0" />
<text class="lbl" x="240.0" y="177.0" text-anchor="middle" ></text>
<text class="sm" x="20" y="196" text-anchor="start" >Fixed 40 bytes. Hop Limit (yellow) is the IPv4 TTL. No header checksum, no fragmentation fields, no options:</text>
<text class="sm" x="20" y="207" text-anchor="start" >those moved to extension headers chained by Next Header (6 = TCP, 17 = UDP, 58 = ICMPv6, 44 = Fragment).</text>
</svg>
<figcaption><b>Figure 3.20</b> The IPv6 header. Compared with IPv4 (Figure 3.12), the checksum, the header length, the three fragmentation fields and the options are gone; the addresses are four times larger and a Flow Label is added.</figcaption>
</figure>

| Type | Prefix | Notes |
|---|---|---|
| Global unicast (GUA) | 2000::/3 | Routable on the Internet; sites receive a /48 and subnets are /64 |
| Unique local (ULA) | fc00::/7 (in practice fd00::/8) | Private, like RFC 1918 |
| Link-local | fe80::/10 | Valid on one link only; every interface has one |
| Multicast | ff00::/8 | ff02::1 all nodes, ff02::2 all routers; replaces broadcast |
| Loopback, unspecified | ::1/128, ::/128 | Like 127.0.0.1 and 0.0.0.0 |
| Documentation | 2001:db8::/32 | Used in this book |

An *anycast* address is one assigned to several machines, and a packet goes to the nearest; it is how public DNS services and CDNs are reached.

::: example
**Compress `2001:0DB8:0000:0000:0000:FF00:0042:8329`, and `2001:db8:0:0:1:0:0:1`.**

1. Drop leading zeros: `2001:DB8:0:0:0:FF00:42:8329`. The longest run of zero groups is three groups; replace it with `::`.
2. Lower case is conventional: `2001:db8::ff00:42:8329`.
3. In `2001:db8:0:0:1:0:0:1` there are two runs of two zero groups. They tie, so the leftmost is compressed: `2001:db8::1:0:0:1`.

[Result: 2001:db8::ff00:42:8329 and 2001:db8::1:0:0:1. Compressing both runs, as in `2001:db8::1::1`, is illegal.]{.result}
:::

### Interface identifiers and SLAAC

Hosts in the same /64 need to choose the remaining 64 bits, the *interface identifier*. The older method, EUI-64, derives it from the MAC address: split the MAC in the middle, insert `FF:FE`, and invert the universal/local bit of the first byte.

<figure>
<svg viewBox="0 0 480 166" width="480">
<defs><marker id="eu" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z" style=""/></marker></defs>
<text class="lbl" x="14" y="26" text-anchor="start" >1  MAC address</text>
<rect class="box" x="150" y="10" width="40" height="22" rx="0" />
<text class="mono" x="170" y="25" text-anchor="middle" style="font-size:9px">00</text>
<rect class="box" x="192" y="10" width="40" height="22" rx="0" />
<text class="mono" x="212" y="25" text-anchor="middle" style="font-size:9px">1A</text>
<rect class="box" x="234" y="10" width="40" height="22" rx="0" />
<text class="mono" x="254" y="25" text-anchor="middle" style="font-size:9px">2B</text>
<rect class="box" x="276" y="10" width="40" height="22" rx="0" />
<text class="mono" x="296" y="25" text-anchor="middle" style="font-size:9px">3C</text>
<rect class="box" x="318" y="10" width="40" height="22" rx="0" />
<text class="mono" x="338" y="25" text-anchor="middle" style="font-size:9px">4D</text>
<rect class="box" x="360" y="10" width="40" height="22" rx="0" />
<text class="mono" x="380" y="25" text-anchor="middle" style="font-size:9px">5E</text>
<text class="lbl" x="14" y="66" text-anchor="start" >2  Insert FF:FE</text>
<rect class="box" x="150" y="50" width="40" height="22" rx="0" />
<text class="mono" x="170" y="65" text-anchor="middle" style="font-size:9px">00</text>
<rect class="box" x="192" y="50" width="40" height="22" rx="0" />
<text class="mono" x="212" y="65" text-anchor="middle" style="font-size:9px">1A</text>
<rect class="box" x="234" y="50" width="40" height="22" rx="0" />
<text class="mono" x="254" y="65" text-anchor="middle" style="font-size:9px">2B</text>
<rect class="fill" x="276" y="50" width="40" height="22" rx="0" />
<text class="mono" x="296" y="65" text-anchor="middle" style="font-size:9px">FF</text>
<rect class="fill" x="318" y="50" width="40" height="22" rx="0" />
<text class="mono" x="338" y="65" text-anchor="middle" style="font-size:9px">FE</text>
<rect class="box" x="360" y="50" width="40" height="22" rx="0" />
<text class="mono" x="380" y="65" text-anchor="middle" style="font-size:9px">3C</text>
<rect class="box" x="402" y="50" width="40" height="22" rx="0" />
<text class="mono" x="422" y="65" text-anchor="middle" style="font-size:9px">4D</text>
<rect class="box" x="444" y="50" width="40" height="22" rx="0" />
<text class="mono" x="464" y="65" text-anchor="middle" style="font-size:9px">5E</text>
<text class="lbl" x="14" y="106" text-anchor="start" >3  Flip U/L bit</text>
<rect class="hl" x="150" y="90" width="40" height="22" rx="0" />
<rect class="ln" x="150" y="90" width="40" height="22" rx="0" fill="none"/>
<text class="mono" x="170" y="105" text-anchor="middle" style="font-size:9px">02</text>
<rect class="box" x="192" y="90" width="40" height="22" rx="0" />
<text class="mono" x="212" y="105" text-anchor="middle" style="font-size:9px">1A</text>
<rect class="box" x="234" y="90" width="40" height="22" rx="0" />
<text class="mono" x="254" y="105" text-anchor="middle" style="font-size:9px">2B</text>
<rect class="box" x="276" y="90" width="40" height="22" rx="0" />
<text class="mono" x="296" y="105" text-anchor="middle" style="font-size:9px">FF</text>
<rect class="box" x="318" y="90" width="40" height="22" rx="0" />
<text class="mono" x="338" y="105" text-anchor="middle" style="font-size:9px">FE</text>
<rect class="box" x="360" y="90" width="40" height="22" rx="0" />
<text class="mono" x="380" y="105" text-anchor="middle" style="font-size:9px">3C</text>
<rect class="box" x="402" y="90" width="40" height="22" rx="0" />
<text class="mono" x="422" y="105" text-anchor="middle" style="font-size:9px">4D</text>
<rect class="box" x="444" y="90" width="40" height="22" rx="0" />
<text class="mono" x="464" y="105" text-anchor="middle" style="font-size:9px">5E</text>
<text class="lbl" x="14" y="138" text-anchor="start" >4  Link-local</text>
<text class="mono" x="150" y="138" text-anchor="start" style="font-size:10px">fe80::21a:2bff:fe3c:4d5e</text>
<text class="sm" x="150" y="156" text-anchor="start" >Bit 7 (value 0x02) of the first byte: 0x00 = 0000 0000 becomes 0000 0010 = 0x02.</text>
<text class="sm" x="14" y="60" text-anchor="middle" ></text>
</svg>
<figcaption><b>Figure 3.21</b> Building an EUI-64 interface identifier from a MAC address. The middle step splits the MAC between the vendor and device halves; the flip inverts the universal/local bit, so that a burned-in address is marked "universal" with a 1.</figcaption>
</figure>

::: example
**Link-local address and solicited-node multicast for MAC 00:1A:2B:3C:4D:5E.**

1. Split the MAC after 3 bytes and insert FFFE: 00:1A:2B:FF:FE:3C:4D:5E.
2. Invert bit 7 of the first byte: 0x00 becomes 0x02. Interface ID = 021A:2BFF:FE3C:4D5E.
3. Link-local: `fe80::21a:2bff:fe3c:4d5e` (leading zero of 021A dropped).
4. The *solicited-node multicast* address is `ff02::1:ff` followed by the last 24 bits of the unicast address: `ff02::1:ff3c:4d5e`.
5. Its Ethernet multicast MAC is `33:33` followed by the last 32 bits of the IPv6 address: `33:33:ff:3c:4d:5e`.

[Result: fe80::21a:2bff:fe3c:4d5e; solicited-node ff02::1:ff3c:4d5e; MAC 33:33:ff:3c:4d:5e.]{.result}
:::

Because EUI-64 exposes the hardware address and lets one be tracked between networks, modern systems use random, changing identifiers (*privacy extensions*) for global addresses. *Stateless address autoconfiguration* (SLAAC) lets a host build an address without a server: it forms a link-local address, checks for a duplicate (*DAD*, duplicate address detection), sends a Router Solicitation, receives a Router Advertisement carrying the prefix, and combines prefix and identifier. Two flags in the advertisement send the host to DHCPv6: M (managed) means "get the address by stateful DHCPv6", and O (other) means "build the address by SLAAC, but get DNS and other options by stateless DHCPv6". The prefix itself carries an A flag that permits SLAAC.

<figure>
<svg viewBox="0 0 480 164" width="480">
<defs><marker id="sla" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="inkf" d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="slb" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z" style=""/></marker></defs>
<text class="lbl" x="110" y="12" text-anchor="middle" >Host</text>
<line class="lg" x1="110" y1="18" x2="110" y2="152" stroke-dasharray="2 2"/>
<text class="lbl" x="370" y="12" text-anchor="middle" >Router</text>
<line class="lg" x1="370" y1="18" x2="370" y2="152" stroke-dasharray="2 2"/>
<line class="lg" x1="110" y1="48" x2="370" y2="56" marker-end="url(#sla)"/>
<line class="ln" x1="110" y1="84" x2="370" y2="92" marker-end="url(#sla)"/>
<text class="lbl" x="240.0" y="82.0" text-anchor="middle" style="font-size:7.6px;paint-order:stroke;stroke:#fff;stroke-width:3px">RS</text>
<line class="acc" x1="370" y1="112" x2="110" y2="120" marker-end="url(#slb)"/>
<text class="lbl" x="240.0" y="110.0" text-anchor="middle" style="font-size:7.6px;paint-order:stroke;stroke:#fff;stroke-width:3px">RA</text>
<text class="sm" x="8" y="28" text-anchor="start" >1  link-local fe80::21a:2bff:fe3c:4d5e</text>
<text class="sm" x="8" y="40" text-anchor="start" >   DAD: NS from :: to ff02::1:ff3c:4d5e (silence = unique)</text>
<text class="sm" x="112" y="70" text-anchor="start" >2  Router Solicitation to ff02::2</text>
<text class="sm" x="368" y="104" text-anchor="end" >3  Router Advertisement from fe80::1 to ff02::1</text>
<text class="sm" x="368" y="132" text-anchor="end" >   prefix 2001:db8:1::/64 (A=1), M=0, O=0, router lifetime</text>
<text class="sm" x="8" y="150" text-anchor="start" >4  host forms 2001:db8:1:0:21a:2bff:fe3c:4d5e (or a random privacy ID), repeats DAD</text>
</svg>
<figcaption><b>Figure 3.22</b> SLAAC. The host needs no server: it derives a link-local address, checks it for duplicates (DAD), asks for a router, and combines the advertised /64 prefix with its own interface identifier.</figcaption>
</figure>

### Neighbour discovery

*NDP* (neighbour discovery protocol) is a set of five ICMPv6 messages: router solicitation (type 133), router advertisement (134), neighbour solicitation (135), neighbour advertisement (136) and redirect (137). Address resolution is by 135 and 136: instead of a broadcast the host sends the neighbour solicitation to the *solicited-node multicast* address of the target, which only the few hosts sharing the last 24 bits listen to, and the target replies with its MAC in a neighbour advertisement. The network interrupts uninterested hosts far less than ARP does.

### Header, fragmentation and transition

The 40-byte header has a fixed layout, and everything optional is moved into *extension headers* chained by the Next Header field. Routers never fragment IPv6 packets: only the source may, using a Fragment extension header, so a router with a too-large packet drops it and returns ICMPv6 "packet too big" (type 2). Every IPv6 link must carry at least 1,280 bytes. Hence ICMPv6 must not be blocked wholesale: unlike IPv4, without "packet too big", path MTU discovery fails, and without NDP nothing works at all.

Networks migrate in three ways. *Dual stack* runs both protocols side by side and is the preferred approach. *Tunnels* carry IPv6 packets inside IPv4 packets across an IPv4-only stretch. *NAT64* with *DNS64* lets IPv6-only hosts reach IPv4-only servers: DNS64 synthesises an AAAA record from the server's A record using the prefix 64:ff9b::/96, and NAT64 translates the packet.

::: example
**Split 2001:db8:acad::/48 into /64 subnets.**

1. The prefix borrows 64 − 48 = 16 bits, so there are 2¹⁶ = 65,536 subnets.
2. The subnet ID is the fourth group. The first three subnets are 2001:db8:acad:0::/64, 2001:db8:acad:1::/64 and 2001:db8:acad:2::/64.
3. The last is when the subnet ID is all ones: 2001:db8:acad:ffff::/64.

[Result: 65,536 subnets, from 2001:db8:acad::/64 to 2001:db8:acad:ffff::/64. Subnetting IPv6 is easier than IPv4: it moves on hexadecimal digit boundaries (4 bits).]{.result}
:::

::: trap
*Claim:* "The EUI-64 transformation inverts the last bit of the MAC address." *Why it is wrong:* the bit flipped is the universal/local bit, bit 7 of the first byte (value 0x02), not the last bit of the address. *Correct statement:* 00:1A:… becomes 02:1A:…, and `::` may be used only once in an address.
:::

::: lens
[QUALCOMM · NOKIA · JUNIPER · CISCO · AMAZON · GOOGLE]{.co}

Q3.26 to Q3.29 are mechanical (compress, EUI-64, solicited-node, SLAAC versus DHCPv6), and each is solved in the Problem Set. Q3.30, "why don't IPv6 routers fragment, and what breaks if ICMPv6 is blocked?", rewards the candidate who links it back to PMTUD in Section 3.5.
:::

::: lab
`LAB 3.7 · 20 MIN` On Linux, inspect the addresses, neighbours and the router advertisement; in Wireshark use the filter `icmpv6.type == 134`.

```
$ ip -6 addr show dev eth0
    inet6 2001:db8:1:0:21a:2bff:fe3c:4d5e/64 scope global dynamic mngtmpaddr
    inet6 fe80::21a:2bff:fe3c:4d5e/64 scope link
$ ping -c1 ff02::1%eth0
```

**What you should notice:** the link-local address has the EUI-64 form derived above (some systems print a random identifier instead). The ping to ff02::1 is answered by every IPv6 host on the link, which is the multicast replacement for a broadcast ping.
:::

::: check
1. How many bits are in an IPv6 subnet ID if a site has a /48 and uses /64 subnets? [^c3-21]
2. Which multicast address does a router listen to for solicitations? [^c3-22]
3. Why does IPv6 need no ARP? [^c3-23]
:::

[^c3-21]: 64 − 48 = 16 bits.
[^c3-22]: ff02::2, the all-routers address.
[^c3-23]: Neighbour discovery (ICMPv6 types 135 and 136, sent to the solicited-node multicast address) resolves IPv6 addresses to MAC addresses.

## [3.8]{.sec}Routing concepts in one page [Must · ■■□]{.tag} {#s3-8}

*Forwarding* is the per-packet action of a router: look up the destination and send the packet out of one interface. *Routing* is the process that fills the table used for the lookup, either by hand (static routes) or by protocols that exchange information. The routing table is searched by *longest-prefix match*: of all entries whose prefix matches the destination, the router chooses the one with the longest mask, and the default route 0.0.0.0/0 matches everything with length zero, so it is chosen last. The data structure for a fast lookup is the trie of Pillar 1; this section needs only the rule.

::: example
**Look up four destinations in a table with 10.0.0.0/8 to R1, 10.1.0.0/16 to R2, 10.1.1.0/24 to R3 and 0.0.0.0/0 to R4.**

1. 10.1.1.5 matches /8, /16 and /24, and the longest is /24: next hop R3.
2. 10.1.2.5 matches /8 and /16 only (the third octet is not 1): R2.
3. 10.2.0.1 matches only /8: R1.
4. 11.0.0.1 matches nothing but the default: R4.

[Result: R3, R2, R1, R4.]{.result}
:::

Routing protocols divide into two families by what they tell their neighbours. A *distance-vector* protocol sends its neighbours a list of destinations with a distance to each, and every router computes shortest paths by the Bellman-Ford rule; a *link-state* protocol floods the description of every router's links to all routers, and each runs Dijkstra's algorithm on the full map. The algorithms themselves are solved in Pillar 1 (shortest paths) and the protocols are configured in Pillar 4 (RIP, OSPF, EIGRP, BGP).

| | Distance-vector (RIP) | Link-state (OSPF, IS-IS) |
|---|---|---|
| Knowledge | Neighbours' distances only | Complete topology map |
| Algorithm | Bellman-Ford | Dijkstra (SPF) |
| Traffic | Periodic table to neighbours | Flooded updates on change |
| Convergence | Slow; count-to-infinity risk | Fast |
| Memory, CPU | Low | Higher |

BGP, the protocol between organisations, is a third kind, *path-vector*: each route carries the list of autonomous systems it crossed, which prevents loops. An *autonomous system* (AS) is a network under one administration with an AS number; routing inside an AS uses an *interior* protocol and routing between ASes uses BGP.

The weakness of distance-vector is the *count to infinity*. A router believes a neighbour's claim that a network is reachable, and when the real route breaks, two routers may each point to the other for a route that no longer exists, adding one to the metric at each exchange.

::: example
**Network N hangs off router C in the chain A, B, C; the link to N fails.**

1. Before failure the metrics to N are C = 1, B = 2, A = 3.
2. C loses N but, before it announces anything, B's regular update says "N is 2 away". C accepts: N = 3 via B.
3. B hears from C that N is 3 and updates to 4; C then hears 4 and takes 5; the values grow 5, 6, 7 and so on until RIP's infinity of 16, when all three declare N unreachable.
4. With *split horizon*, B does not advertise N back to C, because B learned it from C; C hears nothing and N expires at once. *Poison reverse* sends N with metric 16 back instead. *Triggered updates* spread the bad news immediately, and *hold-down timers* ignore worse news for a while.

[Result: without safeguards the metric climbs one step per exchange up to 16; split horizon removes the loop between two neighbours. Larger loops still need hold-down and triggered updates, one reason why link-state protocols replaced RIP.]{.result}
:::

::: check
1. A table holds 192.168.0.0/16 and 192.168.4.0/22. Which entry forwards 192.168.5.9? [^c3-24]
2. Which family floods the topology, and which algorithm does each router run? [^c3-25]
:::

[^c3-24]: 192.168.4.0/22 covers 192.168.4.0 to 192.168.7.255, so it is the longest match.
[^c3-25]: Link-state; Dijkstra's shortest-path-first.

:::
