::: {.p3}

## [3.5]{.sec}The IPv4 header, fragmentation, MTU and ICMP [Must · ■■□]{.tag} {#s3-5}

Every IPv4 packet starts with a header that holds what a router needs in order to forward it, and little else. Knowing the header field by field lets one read a hex dump, explain why traceroute works and diagnose the fault that makes some websites refuse to load.

::: bigidea
The IP header carries just enough for each router to forward the packet, and when a link is too small for the packet, the packet is cut into fragments or, if forbidden to fragment, dropped with an error message.
:::

### The header, field by field

<figure>
<svg viewBox="0 0 480 222" width="480">
<text class="sm" x="26.9" y="17" text-anchor="middle" >0</text>
<text class="sm" x="123.1" y="17" text-anchor="middle" >7</text>
<text class="sm" x="136.9" y="17" text-anchor="middle" >8</text>
<text class="sm" x="233.1" y="17" text-anchor="middle" >15</text>
<text class="sm" x="246.9" y="17" text-anchor="middle" >16</text>
<text class="sm" x="343.1" y="17" text-anchor="middle" >23</text>
<text class="sm" x="356.9" y="17" text-anchor="middle" >24</text>
<text class="sm" x="453.1" y="17" text-anchor="middle" >31</text>
<rect class="box" x="20" y="22" width="55.0" height="26" rx="0" />
<text class="lbl" x="47.5" y="38.0" text-anchor="middle" >Version 4</text>
<rect class="box" x="75.0" y="22" width="55.0" height="26" rx="0" />
<text class="lbl" x="102.5" y="38.0" text-anchor="middle" >IHL 4</text>
<rect class="box" x="130.0" y="22" width="82.5" height="26" rx="0" />
<text class="lbl" x="171.2" y="38.0" text-anchor="middle" >DSCP 6</text>
<rect class="box" x="212.5" y="22" width="27.5" height="26" rx="0" />
<text class="sm" x="226.2" y="37.5" text-anchor="middle" style="font-size:6px">ECN 2</text>
<rect class="box" x="240.0" y="22" width="220.0" height="26" rx="0" />
<text class="lbl" x="350.0" y="38.0" text-anchor="middle" >Total Length 16</text>
<rect class="fill" x="20" y="48" width="220.0" height="26" rx="0" />
<text class="lbl" x="130.0" y="64.0" text-anchor="middle" >Identification 16</text>
<rect class="fill" x="240.0" y="48" width="41.25" height="26" rx="0" />
<text class="lbl" x="260.6" y="64.0" text-anchor="middle" >Flags 3</text>
<rect class="fill" x="281.25" y="48" width="178.75" height="26" rx="0" />
<text class="lbl" x="370.6" y="64.0" text-anchor="middle" >Fragment Offset 13</text>
<rect class="hl" x="20" y="74" width="110.0" height="26" rx="0" />
<rect class="ln" x="20" y="74" width="110.0" height="26" rx="0" fill="none"/>
<text class="lbl" x="75.0" y="90.0" text-anchor="middle" >TTL 8</text>
<rect class="box" x="130.0" y="74" width="110.0" height="26" rx="0" />
<text class="lbl" x="185.0" y="90.0" text-anchor="middle" >Protocol 8</text>
<rect class="hl" x="240.0" y="74" width="220.0" height="26" rx="0" />
<rect class="ln" x="240.0" y="74" width="220.0" height="26" rx="0" fill="none"/>
<text class="lbl" x="350.0" y="90.0" text-anchor="middle" >Header Checksum 16</text>
<rect class="box" x="20" y="100" width="440.0" height="26" rx="0" />
<text class="lbl" x="240.0" y="116.0" text-anchor="middle" >Source Address 32</text>
<rect class="box" x="20" y="126" width="440.0" height="26" rx="0" />
<text class="lbl" x="240.0" y="142.0" text-anchor="middle" >Destination Address 32</text>
<rect class="fill" x="20" y="152" width="440.0" height="26" rx="0" />
<text class="lbl" x="240.0" y="168.0" text-anchor="middle" >Options (0 to 40 bytes) + padding</text>
<text class="sm" x="20" y="192" text-anchor="start" >Yellow: rewritten at every router hop (TTL, hence the checksum).</text>
<text class="sm" x="20" y="203" text-anchor="start" >Grey: fragmentation fields (set by the sender; changed only when a router fragments), and options.</text>
<text class="sm" x="20" y="214" text-anchor="start" >Flags: bit 0 reserved, DF = do not fragment, MF = more fragments. IHL counts 32-bit words, so 5 means 20 bytes.</text>
</svg>
<figcaption><b>Figure 3.12</b> The IPv4 header, 32 bits wide, as it appears on the wire. The minimum is 20 bytes (five rows); the Total Length covers header and data.</figcaption>
</figure>

*Version* is 4. *IHL* (header length) counts 32-bit words, so the usual value is 5. *DSCP* and *ECN* carry the traffic class and congestion marks (Pillar 4 and Section 3.9). *Total length* is the size of header plus data in bytes, so a packet is at most 65,535 bytes. *Identification*, *flags* and *fragment offset* support fragmentation, described below. *TTL* (time to live) is decremented by every router and the packet is discarded at zero, which stops packets circulating for ever in a routing loop. *Protocol* names the payload: 1 for ICMP, 6 for TCP, 17 for UDP, 89 for OSPF. The *header checksum* protects the header only; it is the 16-bit one's-complement sum of all header words, and because TTL changes, every router must recompute it. The two 32-bit addresses close the fixed part.

::: example
**Decode `45 00 00 3c 1c 46 40 00 40 06 9c bc c0 a8 00 68 c0 a8 00 01`.**

1. `45`: version 4, IHL 5, so the header is 20 bytes. `00`: DSCP 0, ECN 0.
2. `00 3c`: total length 60 bytes. `1c 46`: identification 0x1c46.
3. `40 00`: flags and offset. 0x4000 is 0100 0000 0000 0000 in binary, so DF = 1, MF = 0, offset 0.
4. `40`: TTL 64. `06`: protocol 6 (TCP). `9c bc`: header checksum.
5. `c0 a8 00 68` is 192.168.0.104 and `c0 a8 00 01` is 192.168.0.1, the source and destination.
6. Verify the checksum: add the ten 16-bit words, 0x4500 + 0x003c + 0x1c46 + 0x4000 + 0x4006 + 0x9cbc + 0xc0a8 + 0x0068 + 0xc0a8 + 0x0001 = 0x2FFFD. Fold the carry back in: 0xFFFD + 0x2 = 0xFFFF.

[Result: a 60-byte TCP packet from 192.168.0.104 to 192.168.0.1, TTL 64, DF set; the one's-complement sum is 0xFFFF, so the header is intact.]{.result}
:::

A receiver verifies the checksum by summing all words including the checksum; an undamaged header gives 0xFFFF. To compute it, set the field to zero, sum, fold the carries and complement: here the sum without the checksum is 0x6343 and its complement is 0x9cbc.

### Fragmentation, MTU and MSS

Every link has a *maximum transmission unit* (MTU), the largest IP packet it carries: 1,500 bytes on Ethernet and 1,492 on PPPoE. If a packet is larger, a router may *fragment* it, cutting the data into pieces that each carry a copy of the IP header. The Identification field is the same in all fragments, and the *fragment offset* gives the position of each piece in units of 8 bytes, so every piece but the last must have a data size that is a multiple of 8. The *MF* (more fragments) flag is 1 on all but the last. Only the destination reassembles, because routers on the path may take different routes for different fragments.

::: example
**Fragment a 4,000-byte datagram (20-byte header, 3,980 bytes of data) for a link with MTU 1,500.**

1. Room for data per fragment: 1,500 − 20 = 1,480 bytes. That is a multiple of 8 (1,480 = 185 × 8), so it can be used as is.
2. Number of fragments: 3,980 / 1,480 = 2.69, so three: 1,480 + 1,480 + 1,020 = 3,980 bytes.
3. Offsets in 8-byte units: 0, 1,480 / 8 = 185, 2,960 / 8 = 370.

| Fragment | Data | Total Length | Offset field | MF |
|---|---|---|---|---|
| 1 | 1,480 | 1,500 | 0 | 1 |
| 2 | 1,480 | 1,500 | 185 | 1 |
| 3 | 1,020 | 1,040 | 370 | 0 |

[Result: three fragments with offsets 0, 185, 370; the last has MF = 0 and a Total Length of 1,040. If a later link has a smaller MTU, each fragment is fragmented again, with offsets relative to the original.]{.result}
:::

<figure>
<svg viewBox="0 0 480 160" width="480">
<text class="lbl" x="14" y="26" text-anchor="start" >Original</text>
<rect class="hl" x="70" y="10" width="14" height="24" rx="0" />
<rect class="ln" x="70" y="10" width="14" height="24" rx="0" fill="none"/>
<rect class="box" x="84" y="10" width="360.0" height="24" rx="0" />
<text class="lbl" x="264.0" y="25" text-anchor="middle" >3980 B data</text>
<text class="sm" x="450.0" y="20" text-anchor="start" >Total Length 4000</text>
<text class="sm" x="450.0" y="30" text-anchor="start" >ID 0x1c46</text>
<text class="lbl" x="14" y="70" text-anchor="start" >Fragment 1</text>
<rect class="hl" x="70" y="54" width="14" height="24" rx="0" />
<rect class="ln" x="70" y="54" width="14" height="24" rx="0" fill="none"/>
<rect class="box" x="84" y="54" width="133.9" height="24" rx="0" />
<text class="lbl" x="150.9" y="69" text-anchor="middle" >1480 B data</text>
<text class="sm" x="223.9" y="64" text-anchor="start" >TL 1500</text>
<text class="sm" x="223.9" y="74" text-anchor="start" >offset 0, MF 1</text>
<text class="lbl" x="14" y="102" text-anchor="start" >Fragment 2</text>
<rect class="hl" x="70" y="86" width="14" height="24" rx="0" />
<rect class="ln" x="70" y="86" width="14" height="24" rx="0" fill="none"/>
<rect class="box" x="84" y="86" width="133.9" height="24" rx="0" />
<text class="lbl" x="150.9" y="101" text-anchor="middle" >1480 B data</text>
<text class="sm" x="223.9" y="96" text-anchor="start" >TL 1500</text>
<text class="sm" x="223.9" y="106" text-anchor="start" >offset 185, MF 1</text>
<text class="lbl" x="14" y="134" text-anchor="start" >Fragment 3</text>
<rect class="hl" x="70" y="118" width="14" height="24" rx="0" />
<rect class="ln" x="70" y="118" width="14" height="24" rx="0" fill="none"/>
<rect class="box" x="84" y="118" width="92.3" height="24" rx="0" />
<text class="lbl" x="130.1" y="133" text-anchor="middle" >1020 B data</text>
<text class="sm" x="182.3" y="128" text-anchor="start" >TL 1040</text>
<text class="sm" x="182.3" y="138" text-anchor="start" >offset 370, MF 0</text>
<text class="sm" x="70" y="152" text-anchor="start" >Yellow cell = 20-byte IP header. All fragments carry the same Identification; offsets count 8-byte units (1480 / 8 = 185).</text>
<line class="lg" x1="217.9" y1="34" x2="217.9" y2="54" stroke-dasharray="2 2"/>
<line class="lg" x1="351.7" y1="34" x2="351.7" y2="54" stroke-dasharray="2 2"/>
</svg>
<figcaption><b>Figure 3.13</b> Fragmenting a 4,000-byte datagram for a link with MTU 1,500. Only the destination reassembles; routers on the way treat each fragment as a separate packet.</figcaption>
</figure>

Fragmentation is costly: one lost fragment forces the loss of the whole datagram, and routers and firewalls dislike fragments. Hence modern hosts avoid it. They set the *DF* (don't fragment) flag and use *path MTU discovery* (PMTUD): a router that cannot forward a DF packet drops it and returns ICMP type 3 code 4, "fragmentation needed", with the next-hop MTU, and the sender then shrinks its packets. TCP expresses the result as the *maximum segment size* (MSS), the largest amount of TCP data in one segment, which excludes the IP and TCP headers: MSS = MTU − 20 − 20 = 1,460 on Ethernet. MTU and MSS are different: MTU includes the IP header and excludes the Ethernet header and FCS; MSS excludes both IP and TCP headers.

PMTUD fails when something blocks the ICMP message. The symptom is characteristic: the TCP handshake completes, small requests succeed, but large responses hang, because only full-size segments exceed the MTU. A common cause is a PPPoE or tunnel link with an MTU of 1,492 or less behind a firewall that drops all ICMP. The standard remedy is *MSS clamping*: the router rewrites the MSS option in passing SYN packets so that the endpoints never send oversize segments, for instance `ip tcp adjust-mss 1452` on a PPPoE interface (1,492 − 40).

<figure>
<svg viewBox="0 0 480 164" width="480">
<defs><marker id="pma" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="inkf" d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="pmb" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z" style=""/></marker></defs>
<text class="lbl" x="50" y="12" text-anchor="middle" >Client</text>
<line class="lg" x1="50" y1="18" x2="50" y2="152" stroke-dasharray="2 2"/>
<text class="lbl" x="170" y="12" text-anchor="middle" >Firewall</text>
<line class="lg" x1="170" y1="18" x2="170" y2="152" stroke-dasharray="2 2"/>
<text class="lbl" x="300" y="12" text-anchor="middle" >Router (MTU 1400 ahead)</text>
<line class="lg" x1="300" y1="18" x2="300" y2="152" stroke-dasharray="2 2"/>
<text class="lbl" x="440" y="12" text-anchor="middle" >Server</text>
<line class="lg" x1="440" y1="18" x2="440" y2="152" stroke-dasharray="2 2"/>
<line class="ln" x1="50" y1="52" x2="300" y2="72" marker-end="url(#pma)"/>
<text class="lbl" x="175.0" y="58.5" text-anchor="middle" style="font-size:7.6px">1500 B, DF=1</text>
<line class="lg" x1="300" y1="72" x2="170" y2="92" marker-end="url(#pma)"/>
<text class="sm" x="235.0" y="78.5" text-anchor="middle" style="font-size:7.6px">ICMP 3/4: MTU 1400</text>
<text class="sm" x="14" y="34" text-anchor="start" >Handshake of small packets succeeds. The first full-size segment then goes out:</text>
<text class="acct" x="170" y="108" text-anchor="middle" >firewall drops the ICMP</text>
<text class="sm" x="14" y="150" text-anchor="start" >The client times out and resends 1500 B with DF=1: the transfer hangs.</text>
<path class="acc" d="M168,88 l8,8 m0,-8 l-8,8"/><line class="acc" x1="50" y1="124" x2="300" y2="136" marker-end="url(#pmb)"/>
</svg>
<figcaption><b>Figure 3.14</b> Path-MTU black hole. The router cannot forward a 1,500-byte packet with DF set onto its MTU-1,400 link, so it sends ICMP type 3 code 4; a firewall that blocks all ICMP discards it, and the client never learns to send smaller segments.</figcaption>
</figure>

### ICMP, ping and traceroute

The *Internet Control Message Protocol* (ICMP) carries errors and diagnostics, inside IP packets with protocol number 1. The types to know are: 0 echo reply and 8 echo request (ping); 3 destination unreachable, whose code says which kind (0 network, 1 host, 3 port, 4 fragmentation needed with DF set); 5 redirect; and 11 time exceeded.

*Traceroute* exploits the TTL. It sends probes with TTL 1, 2, 3 and so on. The first router decrements TTL 1 to zero, discards the probe and returns ICMP time exceeded, whose source address names that router; the next probe reaches the second router, and so forth until a probe reaches the destination, which answers differently. Linux sends UDP probes to ports from 33434 upwards, and the destination replies ICMP port unreachable (type 3 code 3); Windows `tracert` sends ICMP echo requests and the destination replies with an echo reply. A line of `* * *` means no answer arrived in time: the router may not generate time exceeded, rate-limit it or sit behind a firewall that drops the probe or its reply; it does not by itself mean that the path is broken.

<figure>
<svg viewBox="0 0 480 184" width="480">
<defs><marker id="tra" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="inkf" d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="trb" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z" style=""/></marker></defs>
<text class="lbl" x="40" y="12" text-anchor="middle" >Source</text>
<line class="lg" x1="40" y1="18" x2="40" y2="176" stroke-dasharray="2 2"/>
<text class="lbl" x="145" y="12" text-anchor="middle" >R1</text>
<line class="lg" x1="145" y1="18" x2="145" y2="176" stroke-dasharray="2 2"/>
<text class="lbl" x="250" y="12" text-anchor="middle" >R2</text>
<line class="lg" x1="250" y1="18" x2="250" y2="176" stroke-dasharray="2 2"/>
<text class="lbl" x="355" y="12" text-anchor="middle" >R3</text>
<line class="lg" x1="355" y1="18" x2="355" y2="176" stroke-dasharray="2 2"/>
<text class="lbl" x="450" y="12" text-anchor="middle" >Dest</text>
<line class="lg" x1="450" y1="18" x2="450" y2="176" stroke-dasharray="2 2"/>
<line class="ln" x1="40" y1="34" x2="145" y2="40" marker-end="url(#tra)"/>
<text class="lbl" x="92.5" y="33.5" text-anchor="middle" style="font-size:7.6px">TTL 1</text>
<line class="lg" x1="145" y1="40" x2="40" y2="46" marker-end="url(#tra)"/>
<text class="sm" x="92.5" y="39.5" text-anchor="middle" style="font-size:7.6px">ICMP 11 from R1</text>
<line class="ln" x1="40" y1="66" x2="250" y2="76" marker-end="url(#tra)"/>
<text class="lbl" x="145.0" y="67.5" text-anchor="middle" style="font-size:7.6px">TTL 2</text>
<line class="lg" x1="250" y1="76" x2="40" y2="86" marker-end="url(#tra)"/>
<text class="sm" x="145.0" y="77.5" text-anchor="middle" style="font-size:7.6px">ICMP 11 from R2</text>
<line class="ln" x1="40" y1="98" x2="355" y2="110" marker-end="url(#tra)"/>
<text class="lbl" x="197.5" y="100.5" text-anchor="middle" style="font-size:7.6px">TTL 3</text>
<line class="lg" x1="355" y1="110" x2="40" y2="122" marker-end="url(#tra)"/>
<text class="sm" x="197.5" y="112.5" text-anchor="middle" style="font-size:7.6px">ICMP 11 from R3</text>
<line class="ln" x1="40" y1="134" x2="450" y2="148" marker-end="url(#tra)"/>
<text class="lbl" x="245.0" y="137.5" text-anchor="middle" style="font-size:7.6px">TTL 4</text>
<line class="acc" x1="450" y1="148" x2="40" y2="162" marker-end="url(#trb)"/>
<text class="lbl" x="245.0" y="151.5" text-anchor="middle" style="font-size:7.6px">Port unreach. / Echo reply</text>
<text class="sm" x="14" y="175" text-anchor="start" >ICMP 11 = Time Exceeded (TTL reached 0). Each probe has TTL one higher; the sender learns one router per probe.</text>
</svg>
<figcaption><b>Figure 3.15</b> How traceroute works. A router that decrements TTL to zero discards the packet and returns an ICMP Time Exceeded message, revealing its own address. The last hop answers with a different message, because the probe finally arrives.</figcaption>
</figure>

::: trap
*Claim:* "Fragment offset 1480 means the second fragment starts at byte 1480." *Why it is wrong:* the field counts 8-byte units, so a value of 1480 would mean byte 11,840. *Correct statement:* the second fragment of the example above has offset field 185, which is byte 1,480.
:::

::: lens
[AMAZON · MICROSOFT · CISCO · QUALCOMM · BROADCOM · JUNIPER]{.co}

Q3.15 (fragmentation arithmetic) and Q3.16 (MTU versus MSS) are routine. Q3.17 is the scenario "ping works, the TCP handshake completes, the page never loads". A strong answer names PMTUD, says what to look for (ICMP 3/4 absent; retransmissions of the same large segment; a successful `ping -M do -s 1372`), and gives both fixes (allow ICMP type 3 code 4; clamp the MSS).
:::

::: lab
`LAB 3.5 · 20 MIN` On Linux, probe the path MTU with DF set. The ICMP header adds 8 bytes and the IP header 20, so a 1,472-byte payload is exactly a 1,500-byte packet.

```
$ ping -c1 -M do -s 1472 8.8.8.8
1480 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=9.8 ms
$ ping -c1 -M do -s 1473 8.8.8.8
ping: local error: message too long, mtu=1500
$ traceroute -n 8.8.8.8          # then: traceroute -I -n 8.8.8.8
 1  192.168.1.1  0.9 ms
 2  * * *
```

**What you should notice:** the largest unfragmented payload is 1,472 bytes, confirming the 1,500-byte MTU. In the traceroute, the `-I` (ICMP) option may succeed where the default UDP probes give `* * *` at a firewall; capture both in Wireshark with `ip.ttl == 1` to see the probes and the type-11 replies.
:::

::: check
1. A 1,500-byte packet (20-byte header) must cross a link with MTU 576. How many fragments, and what are their data sizes? [^c3-15]
2. Why is the header checksum recomputed at every hop? [^c3-16]
3. Which ICMP message makes PMTUD work, and what does it contain? [^c3-17]
:::

[^c3-15]: Data = 1,480; room per fragment = 576 − 20 = 556, rounded down to a multiple of 8 = 552. 1,480 / 552 = 2.68, so three fragments: 552, 552, 376.
[^c3-16]: Because TTL, which is inside the header, changes at every hop.
[^c3-17]: ICMP type 3 code 4 (fragmentation needed and DF set); it carries the next-hop MTU and the start of the original packet.

## [3.6]{.sec}ARP, DHCP and NAT: the glue protocols [Must · ■■□]{.tag} {#s3-6}

Three small protocols turn a plugged-in laptop into a working Internet host. ARP finds the MAC address of the next hop, DHCP supplies the laptop's address, mask, gateway and DNS server, and NAT lets a private network share one public address. They are tested together because a single "packet walk" question exercises all three.

::: bigidea
IP addresses say where a packet is going, MAC addresses say who gets it on the next link, and ARP, DHCP and NAT are the three devices that keep those two worlds consistent.
:::

### ARP

[**Mnemonic** — ARP asks "Who has this IP?" by broadcast and is answered by unicast; DHCP's first message, Discover, is also a broadcast, because the sender has nothing else to use.]{.margin}A host that wants to send an IP packet knows the destination IP address but needs a destination MAC address for the frame. If the destination is on the same subnet it needs the destination's MAC; otherwise it needs the MAC of the *default gateway*, the router that leads off the subnet. The *Address Resolution Protocol* (ARP) finds it: the host broadcasts "who has 192.168.1.1? tell 192.168.1.10" (opcode 1, destination MAC `ff:ff:ff:ff:ff:ff`), and only the owner replies by unicast (opcode 2) with its MAC. Both sides record the mapping in an *ARP cache*, which expires after a time that ranges from seconds on Linux to four hours on Cisco IOS.

<figure>
<svg viewBox="0 0 480 152" width="480">
<defs><marker id="ara" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="inkf" d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="arb" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z" style=""/></marker></defs>
<text class="lbl" x="70" y="12" text-anchor="middle" >Host A</text>
<line class="lg" x1="70" y1="18" x2="70" y2="144" stroke-dasharray="2 2"/>
<text class="lbl" x="250" y="12" text-anchor="middle" >Host B (target)</text>
<line class="lg" x1="250" y1="18" x2="250" y2="144" stroke-dasharray="2 2"/>
<text class="lbl" x="410" y="12" text-anchor="middle" >Host C</text>
<line class="lg" x1="410" y1="18" x2="410" y2="144" stroke-dasharray="2 2"/>
<line class="ln" x1="70" y1="40" x2="250" y2="52" marker-end="url(#ara)"/>
<text class="lbl" x="160.0" y="42.5" text-anchor="middle" style="font-size:7.6px">ARP request (broadcast)</text>
<line class="ln" x1="70" y1="44" x2="410" y2="56" marker-end="url(#ara)"/>
<line class="acc" x1="250" y1="92" x2="70" y2="104" marker-end="url(#arb)"/>
<text class="lbl" x="160.0" y="94.5" text-anchor="middle" style="font-size:7.6px">ARP reply (unicast)</text>
<text class="sm" x="70" y="26" text-anchor="middle" >192.168.1.10 / AA:AA</text>
<text class="sm" x="250" y="26" text-anchor="middle" >192.168.1.1 / 11:11</text>
<text class="sm" x="410" y="26" text-anchor="middle" >192.168.1.77 / CC:CC</text>
<text class="sm" x="254" y="64" text-anchor="start" >Dst MAC ff:ff:ff:ff:ff:ff, opcode 1</text>
<text class="sm" x="254" y="74" text-anchor="start" >"Who has 192.168.1.1? Tell 192.168.1.10"</text>
<text class="sm" x="410" y="70" text-anchor="middle" >C ignores it</text>
<text class="sm" x="254" y="114" text-anchor="start" >Dst MAC AA:AA, opcode 2</text>
<text class="sm" x="254" y="124" text-anchor="start" >"192.168.1.1 is at 11:11"</text>
<text class="acct" x="8" y="140" text-anchor="start" >A caches 192.168.1.1 → 11:11</text>
<text class="sm" x="300" y="140" text-anchor="start" >B caches 192.168.1.10 → AA:AA (from the request)</text>
</svg>
<figcaption><b>Figure 3.16</b> ARP resolves a next-hop IP address to a MAC address. The request is broadcast; only the owner of the target address replies, by unicast. MAC addresses are abbreviated to two bytes.</figcaption>
</figure>

A *gratuitous ARP* is an ARP message in which the sender asks for its own address. A host sends it after configuring an address to detect a duplicate (if anyone replies, the address is taken) and to update other hosts' caches; a router in a first-hop redundancy group sends it on failover so that the switch and hosts learn that the virtual address has moved. *Proxy ARP* is a router answering ARP requests for addresses it can reach on behalf of the real owner. It lets a host with a wrong mask work, and so hides misconfiguration; it enlarges ARP tables and is normally disabled. *ARP spoofing*, the forging of replies, is treated in Pillar 9.

### DHCP

*DHCP* (Dynamic Host Configuration Protocol) hands out addresses on lease. A new host has no address and does not know where the server is, so it must use broadcasts, and the exchange has four messages, remembered as DORA. The client broadcasts a **D**iscover (UDP source port 68, destination 67, source IP 0.0.0.0, destination 255.255.255.255). Every server replies with an **O**ffer holding an address and lease time. The client broadcasts a **R**equest naming the server it chose (option 54) and the address wanted (option 50), which also tells the other servers to withdraw. The chosen server confirms with an **A**cknowledgement, which carries the options: 1 subnet mask, 3 default gateway, 6 DNS servers, 51 lease time. If no server answers, the client may give itself a link-local 169.254.x.y address, which signals a DHCP failure to anyone reading `ipconfig`.

The lease is renewed in stages. At T1, 50% of the lease, the client unicasts a Request to its server; if that fails, at T2, 87.5%, it broadcasts to any server; if the lease runs out, it starts again with Discover.

Broadcasts do not cross routers, but a company seldom has one DHCP server per subnet. A *relay agent*, configured on the router with `ip helper-address`, receives the broadcast, stores its own interface address in the *giaddr* field, and forwards the message by unicast to the server. The server uses giaddr to choose the right pool and sends its reply to that address, and the relay delivers it to the client.

<figure>
<svg viewBox="0 0 480 192" width="480">
<defs><marker id="dha" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="inkf" d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="dhb" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z" style=""/></marker></defs>
<text class="lbl" x="50" y="12" text-anchor="middle" >Client</text>
<line class="lg" x1="50" y1="18" x2="50" y2="184" stroke-dasharray="2 2"/>
<text class="lbl" x="240" y="12" text-anchor="middle" >Relay R1 (giaddr 192.168.1.1)</text>
<line class="lg" x1="240" y1="18" x2="240" y2="184" stroke-dasharray="2 2"/>
<text class="lbl" x="430" y="12" text-anchor="middle" >DHCP server 10.0.0.5</text>
<line class="lg" x1="430" y1="18" x2="430" y2="184" stroke-dasharray="2 2"/>
<line class="ln" x1="50" y1="34" x2="240" y2="40" marker-end="url(#dha)"/>
<line class="ln" x1="240" y1="40" x2="430" y2="46" marker-end="url(#dha)"/>
<line class="ln" x1="430" y1="76" x2="240" y2="82" marker-end="url(#dha)"/>
<line class="ln" x1="240" y1="82" x2="50" y2="88" marker-end="url(#dha)"/>
<line class="ln" x1="50" y1="118" x2="240" y2="124" marker-end="url(#dha)"/>
<line class="ln" x1="240" y1="124" x2="430" y2="130" marker-end="url(#dha)"/>
<line class="ln" x1="430" y1="160" x2="240" y2="166" marker-end="url(#dha)"/>
<line class="ln" x1="240" y1="166" x2="50" y2="172" marker-end="url(#dha)"/>
<text class="sm" x="52" y="31" text-anchor="start" >1 DISCOVER  0.0.0.0:68 → 255.255.255.255:67</text>
<text class="sm" x="245" y="38" text-anchor="start" >10.0.0.1 → 10.0.0.5  (giaddr set)</text>
<text class="sm" x="430" y="73" text-anchor="end" >2 OFFER yiaddr 192.168.1.50, lease 86400 s</text>
<text class="sm" x="238" y="80" text-anchor="end" >to client (L2 broadcast or unicast)</text>
<text class="sm" x="52" y="115" text-anchor="start" >3 REQUEST  0.0.0.0:68 → 255.255.255.255:67</text>
<text class="sm" x="245" y="122" text-anchor="start" >opt 50 = .50, opt 54 = 10.0.0.5</text>
<text class="sm" x="430" y="157" text-anchor="end" >4 ACK  yiaddr 192.168.1.50, opt 3 gw, opt 6 DNS</text>
<text class="sm" x="238" y="164" text-anchor="end" >to client</text>
</svg>
<figcaption><b>Figure 3.17</b> DHCP DORA through a relay. The client has no address and no idea where the server is, so Discover and Request are broadcasts (UDP 68 to 67). The relay turns them into unicasts, stamping its own interface address in the giaddr field so the server can pick a pool and reply.</figcaption>
</figure>

### NAT and PAT

*Network address translation* lets private addresses (Section 3.4) reach the Internet by rewriting the headers at a border device. In *static NAT* one private address is mapped to one public address permanently, which suits a server. In *dynamic NAT* the router maps hosts to addresses from a pool, one-to-one, for as long as they are in use. In *port address translation* (PAT, also *NAT overload*), by far the most common form, thousands of hosts share one public address, and the router tells their connections apart by the source port; it records each mapping in a *translation table*.

Cisco names the four addresses by two questions: is the host inside or outside, and is the address viewed as local (from inside) or global (from outside).

<figure>
<svg viewBox="0 0 480 158" width="480">
<defs><marker id="nq" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z" style=""/></marker></defs>
<text class="sm" x="250" y="12" text-anchor="middle" >Local = as seen on the inside</text>
<rect class="box" x="20" y="24" width="210" height="52" rx="0" />
<text class="lbl" x="28" y="38" text-anchor="start" style="font-weight:700">Inside local</text>
<text class="mono" x="28" y="54" text-anchor="start" >192.168.1.10:51000</text>
<text class="sm" x="28" y="68" text-anchor="start" >the private host, as the LAN sees it</text>
<rect class="box" x="250" y="24" width="210" height="52" rx="0" />
<text class="lbl" x="258" y="38" text-anchor="start" style="font-weight:700">Inside global</text>
<text class="mono" x="258" y="54" text-anchor="start" >203.0.113.2:51000</text>
<text class="sm" x="258" y="68" text-anchor="start" >the same host, as the Internet sees it</text>
<rect class="box" x="20" y="84" width="210" height="52" rx="0" />
<text class="lbl" x="28" y="98" text-anchor="start" style="font-weight:700">Outside local</text>
<text class="mono" x="28" y="114" text-anchor="start" >198.51.100.80:80</text>
<text class="sm" x="28" y="128" text-anchor="start" >the server, as the LAN sees it</text>
<rect class="box" x="250" y="84" width="210" height="52" rx="0" />
<text class="lbl" x="258" y="98" text-anchor="start" style="font-weight:700">Outside global</text>
<text class="mono" x="258" y="114" text-anchor="start" >198.51.100.80:80</text>
<text class="sm" x="258" y="128" text-anchor="start" >the server, as the Internet sees it</text>
<path class="acc" d="M232,50 H248" marker-end="url(#nq)"/>
<text class="sm" x="240" y="150" text-anchor="middle" >NAT rewrites the top row (inside local to inside global); the bottom row is normally identical.</text>
</svg>
<figcaption><b>Figure 3.18</b> The four NAT address names. "Inside" and "outside" say where the host lives; "local" and "global" say from which side the address is viewed.</figcaption>
</figure>

NAT has costs. A host behind it cannot be reached from outside unless a mapping exists, and so *port forwarding* (a static entry for one port) is needed to publish a server. Protocols that carry addresses in their payload, such as active FTP and SIP, break unless the router rewrites the payload too (an *application-level gateway*). Two hosts behind different NATs cannot open a connection to each other without help (see Q3.24). *Carrier-grade NAT* (CGNAT), which uses 100.64.0.0/10, adds a second NAT inside the provider. IPv6 (Section 3.7) removes the shortage that made all this necessary.

### The packet walk

The following worked example is the canonical "show me every hop" question. PC-A (192.168.1.10/24, MAC AA:AA) sends an HTTP request to a web server at 198.51.100.80. R1 has an inside interface 192.168.1.1 (MAC 11:11) and an outside interface 203.0.113.2 (MAC 12:12) with PAT. The ISP router has 203.0.113.1 (MAC 21:21) towards R1 and 198.51.100.1 (MAC 22:22) towards the server, whose MAC is BB:BB. MAC addresses are abbreviated to two bytes.

<figure>
<svg viewBox="0 0 480 166" width="480">
<defs><marker id="wk" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="inkf" d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker></defs>
<rect class="box" x="32" y="24" width="28" height="14" rx="1" />
<text class="lbl" x="46" y="12" text-anchor="middle" >PC-A</text>
<text class="sm" x="46" y="54" text-anchor="middle" >192.168.1.10/24</text>
<text class="sm" x="46" y="63" text-anchor="middle" > MAC AA:AA</text>
<circle class="box" cx="176" cy="30" r="12"/><line class="ln" x1="170" y1="24" x2="182" y2="36" /><line class="ln" x1="182" y1="24" x2="170" y2="36" />
<text class="lbl" x="176" y="12" text-anchor="middle" >R1 (PAT)</text>
<text class="sm" x="176" y="54" text-anchor="middle" >in .1 / 11:11</text>
<text class="sm" x="176" y="63" text-anchor="middle" >out 203.0.113.2 / 12:12</text>
<circle class="box" cx="314" cy="30" r="12"/><line class="ln" x1="308" y1="24" x2="320" y2="36" /><line class="ln" x1="320" y1="24" x2="308" y2="36" />
<text class="lbl" x="314" y="12" text-anchor="middle" >ISP router</text>
<text class="sm" x="314" y="54" text-anchor="middle" >203.0.113.1 / 21:21</text>
<text class="sm" x="314" y="63" text-anchor="middle" >198.51.100.1 / 22:22</text>
<rect class="box" x="426" y="24" width="28" height="14" rx="1" />
<text class="lbl" x="440" y="12" text-anchor="middle" >Server</text>
<text class="sm" x="440" y="54" text-anchor="middle" >198.51.100.80</text>
<text class="sm" x="440" y="63" text-anchor="middle" >MAC BB:BB</text>
<line class="ln" x1="60" y1="30" x2="164" y2="30" />
<line class="ln" x1="188" y1="30" x2="302" y2="30" />
<line class="ln" x1="326" y1="30" x2="426" y2="30" />
<text class="lbl" x="80" y="86" text-anchor="middle" >Leg 1</text>
<rect class="hl" x="10" y="92" width="146" height="18" rx="0" />
<rect class="ln" x="10" y="92" width="146" height="18" rx="0" fill="none"/>
<text class="mono" x="83" y="104" text-anchor="middle" style="font-size:7.6px">L2  AA:AA → 11:11</text>
<rect class="fill" x="10" y="110" width="146" height="30" rx="0" />
<text class="mono" x="83" y="122" text-anchor="middle" style="font-size:7.6px">L3  192.168.1.10:51000</text>
<text class="mono" x="83" y="134" text-anchor="middle" style="font-size:7.6px">→ 198.51.100.80:80</text>
<text class="lbl" x="236" y="86" text-anchor="middle" >Leg 2 (after NAT)</text>
<rect class="hl" x="166" y="92" width="146" height="18" rx="0" />
<rect class="ln" x="166" y="92" width="146" height="18" rx="0" fill="none"/>
<text class="mono" x="239" y="104" text-anchor="middle" style="font-size:7.6px">L2  12:12 → 21:21</text>
<rect class="fill" x="166" y="110" width="146" height="30" rx="0" />
<text class="mono" x="239" y="122" text-anchor="middle" style="font-size:7.6px">L3  203.0.113.2:51000</text>
<text class="mono" x="239" y="134" text-anchor="middle" style="font-size:7.6px">→ 198.51.100.80:80</text>
<text class="lbl" x="392" y="86" text-anchor="middle" >Leg 3</text>
<rect class="hl" x="322" y="92" width="146" height="18" rx="0" />
<rect class="ln" x="322" y="92" width="146" height="18" rx="0" fill="none"/>
<text class="mono" x="395" y="104" text-anchor="middle" style="font-size:7.6px">L2  22:22 → BB:BB</text>
<rect class="fill" x="322" y="110" width="146" height="30" rx="0" />
<text class="mono" x="395" y="122" text-anchor="middle" style="font-size:7.6px">L3  203.0.113.2:51000</text>
<text class="mono" x="395" y="134" text-anchor="middle" style="font-size:7.6px">→ 198.51.100.80:80</text>
<text class="sm" x="240" y="158" text-anchor="middle" >The L2 row changes on every link; the L3 row changes only at the NAT router (source address, and port if it clashes).</text>
</svg>
<figcaption><b>Figure 3.19</b> The packet walk of Section 3.6. The yellow row (MAC addresses) is rewritten at every hop; the grey row (IP address and port) is rewritten only where the NAT sits. The return packets use the same cards with source and destination swapped, and R1 translates the destination back.</figcaption>
</figure>

::: example
**Follow a TCP SYN from PC-A, source port 51000, to the server, port 80.**

1. PC-A compares 198.51.100.80 with its own subnet 192.168.1.0/24. The destination is outside, so the frame must go to the default gateway, 192.168.1.1. PC-A has no cache entry and sends an ARP request; R1 replies "192.168.1.1 is at 11:11".
2. **Leg 1.** Frame: source MAC AA:AA, destination 11:11. Packet: 192.168.1.10:51000 to 198.51.100.80:80.
3. R1 decapsulates, decrements the TTL, looks up the route (default via 203.0.113.1) and applies PAT: the source 192.168.1.10:51000 becomes 203.0.113.2:51000, and the mapping is stored. R1 resolves 203.0.113.1 by ARP (21:21) if necessary.
4. **Leg 2.** Frame: 12:12 to 21:21. Packet: 203.0.113.2:51000 to 198.51.100.80:80.
5. The ISP router decrements TTL, finds 198.51.100.0/24 connected, and ARPs for the server (BB:BB).
6. **Leg 3.** Frame: 22:22 to BB:BB. Packet: unchanged, 203.0.113.2:51000 to 198.51.100.80:80.
7. The reply reverses the cards: server to 203.0.113.2:51000, then at R1 the table is consulted and the destination is rewritten to 192.168.1.10:51000, and the frame goes to AA:AA.

```
R1# show ip nat translations
Pro Inside global        Inside local         Outside local        Outside global
tcp 203.0.113.2:51000    192.168.1.10:51000   198.51.100.80:80     198.51.100.80:80
```

[Result: the MAC addresses change on every leg; the IP addresses are constant except at R1, which rewrites only the source address and port outward and the destination address and port inward. The TTL falls by one at each of the two routers.]{.result}
:::

::: trap
*Claim:* "The destination MAC stays the same from PC-A to the server, and the IP addresses change at every router." *Why it is wrong:* it is the other way round; a MAC address has meaning only on one link. *Correct statement:* L2 addresses are rewritten at every hop, L3 addresses end to end, except where NAT rewrites them.
:::

::: lens
[CISCO · AMAZON · GOOGLE · MICROSOFT · JUNIPER]{.co}

Q3.23 is the walk above, usually with PAT. Interviewers push with "what if PC-A has no ARP entry for the gateway?", "what if the server is on the same subnet?" (no gateway: ARP for the server itself) and "what if two hosts use source port 51000?" (R1 picks another global port). Q3.20 and Q3.21 test DHCP with and without a relay.
:::

::: lab
`LAB 3.6 · 30 MIN` In Packet Tracer, configure R1 as DHCP server for 192.168.1.0/24 and PAT on its outside interface, then use `debug ip nat`. In Wireshark, filter `arp || dhcp` while renewing a lease with `sudo dhclient -r && sudo dhclient`; on Linux, view the cache with `ip neigh` and provoke a conflict with `arping`.

```
$ ip neigh show 192.168.1.1
192.168.1.1 dev eth0 lladdr 00:11:22:33:44:55 REACHABLE
 1 DHCP Discover - Transaction ID 0x3a7c1e02
 2 DHCP Offer    - Your (client) IP address: 192.168.1.50
 3 DHCP Request  - Requested IP Address: 192.168.1.50; Server Identifier: 192.168.1.1
 4 DHCP ACK      - IP Address Lease Time: 86400 s; Router: 192.168.1.1; DNS: 192.168.1.1
```

**What you should notice:** the first two packets use the Ethernet broadcast, and the DHCP transaction ID ties all four together. After the ACK, the client sends a gratuitous ARP; `show ip nat translations` fills only when traffic leaves the inside.
:::

::: check
1. Which MAC address does PC-A put as destination when it pings 8.8.8.8? [^c3-18]
2. A lease is 8 hours. When does the client first try to renew, and when does it start broadcasting? [^c3-19]
3. Why does a DHCP relay need to set giaddr? [^c3-20]
:::

[^c3-18]: The MAC address of its default gateway, learned by ARP, not any address for 8.8.8.8.
[^c3-19]: T1 = 50%, so after 4 hours it unicasts to the server; T2 = 87.5%, so after 7 hours it broadcasts to any server.
[^c3-20]: It tells the server which subnet the client is on, so that the right pool is used, and where to send the reply.

:::
