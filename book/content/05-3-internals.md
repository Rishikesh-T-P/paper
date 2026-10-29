::: {.p5}

## [5.8]{.sec}Router and switch internals: RIB, FIB, TCAM and the ASIC [Must · ■■■]{.tag} {#s5-8}

::: bigidea
A router is two machines in one box: a slow, general-purpose computer that decides routes, and a fast, fixed-function chip that forwards packets by looking up a compact copy of those decisions, so the two are joined by a download path and an exception path.
:::

Pillar 4 introduced the *management*, *control* and *data* planes at the command line ([§4.1](#s4-1){.ref}), and the routing table and administrative distance ([§4.4](#s4-4){.ref}). This section opens the box and is the canonical place for what happens inside. The *control plane* runs on the *route processor*, an ordinary CPU with DRAM and an operating system: the BGP, OSPF and IS-IS processes exchange messages with neighbours and build tables of routes. The *data plane* runs on one or more *forwarding ASICs* (application-specific integrated circuits) that examine every packet in a fixed, small number of clock cycles. The CPU handles thousands of packets per second; the ASIC handles billions. The structure is drawn in Figure 5.11.

<figure>
<svg viewBox="0 0 480 256" width="480"><defs><marker id="a511" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="b511" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accf"/></marker></defs><rect class="box" x="60" y="8" width="300" height="86" rx="0"/><text class="lbl" x="80" y="22" text-anchor="start">Route processor (CPU + DRAM): control plane</text><rect class="fill" x="72" y="32" width="100" height="24" rx="0"/><text class="sm" x="122" y="47" text-anchor="middle">BGP · OSPF · IS-IS</text><rect class="fill" x="190" y="32" width="64" height="24" rx="0"/><text class="lbl" x="222" y="47" text-anchor="middle">RIB</text><rect class="fill" x="272" y="32" width="76" height="24" rx="0"/><text class="sm" x="310" y="47" text-anchor="middle">SDK / driver</text><rect class="fill" x="72" y="64" width="100" height="22" rx="0"/><text class="sm" x="122" y="78" text-anchor="middle">ARP / ND · SSH · SNMP</text><line class="ln" x1="172" y1="44" x2="190" y2="44"/><line class="ln" x1="254" y1="44" x2="272" y2="44"/><rect class="box" x="60" y="150" width="300" height="70" rx="0"/><text class="lbl" x="80" y="164" text-anchor="start">Line card / ASIC: data plane</text><rect class="fill" x="72" y="174" width="80" height="36" rx="0"/><text class="sm" x="112" y="189" text-anchor="middle">FIB (LPM)</text><text class="sm" x="112" y="200" text-anchor="middle">adjacency</text><rect class="fill" x="162" y="174" width="80" height="36" rx="0"/><text class="sm" x="202" y="189" text-anchor="middle">ACL TCAM</text><text class="sm" x="202" y="200" text-anchor="middle">counters</text><rect class="fill" x="252" y="174" width="96" height="36" rx="0"/><text class="sm" x="300" y="189" text-anchor="middle">queues · buffers</text><text class="sm" x="300" y="200" text-anchor="middle">rewrite engine</text><line class="ln" x1="310" y1="56" x2="310" y2="150" marker-end="url(#a511)"/><text class="sm" x="318" y="104" text-anchor="start">FIB download</text><rect class="box" x="150" y="104" width="100" height="18" rx="0"/><text class="sm" x="200" y="116" text-anchor="middle">CoPP policer</text><path class="acc" d="M200,174 L200,160 L200,122 M200,104 L200,94" marker-end="url(#b511)"/><text class="acct" x="120" y="134" text-anchor="middle">punt path</text><line class="lg" x1="60" y1="236" x2="360" y2="236"/><text class="sm" x="210" y="248" text-anchor="middle">ports</text><line class="ln" x1="110" y1="236" x2="110" y2="222" marker-end="url(#a511)"/><line class="ln" x1="310" y1="222" x2="310" y2="236" marker-end="url(#a511)"/><text class="sm" x="385" y="80" text-anchor="start">slow path: milliseconds,</text><text class="sm" x="385" y="90" text-anchor="start">kilo-packets per second</text><text class="sm" x="385" y="190" text-anchor="start">fast path: nanoseconds,</text><text class="sm" x="385" y="200" text-anchor="start">billions of packets per second</text></svg>
<figcaption><b>Figure 5.11</b> Control plane above, data plane below. Routes flow down as FIB entries; packets that the hardware cannot handle (the accent path) flow up, through a policer that protects the CPU.</figcaption>
</figure>

### RIB, FIB and adjacency

The *routing information base* (RIB) is the control plane's table. It holds every route from every source, and when several sources offer the same prefix, the lowest administrative distance chooses the winner. The *forwarding information base* (FIB) is the data plane's table, a compressed copy that contains only the winning routes, in a form the hardware can search quickly. Cisco calls the mechanism *CEF* (Cisco Express Forwarding); it keeps two structures. The FIB maps a destination prefix to a next hop. The *adjacency table* maps that next hop to the egress interface and to the complete layer-2 header to prepend (the *rewrite string*), so that forwarding is one lookup and one copy of precomputed bytes, with no ARP request on the fast path. If the next hop's MAC address is not yet known, the adjacency is a *glean* entry: the first packet is punted to the CPU, which sends the ARP request ([§3.6](#s3-6){.ref}) and completes the entry.

::: example
**From RIB to FIB.** BR1 learns Campus Net's data-centre aggregate 10.1.0.0/16 twice: from OSPF (AD 110, redistributed by the border leaf) and from eBGP (AD 20, [§4.7](#s4-7){.ref}), next hop 172.16.255.2.

1. The RIB keeps both candidates. The route-selection rule prefers the lower distance, so the eBGP route is *installed* in the routing table and the OSPF route waits as a backup.
2. The FIB is built from installed routes only: one entry, 10.1.0.0/16 via 172.16.255.2.
3. The next hop 172.16.255.2 is reached over a connected route on Gi0/0/1. *Recursive resolution* (when a route's next hop is itself reached through another route) is flattened in CEF, so the FIB entry points directly to the adjacency for 172.16.255.2 on Gi0/0/1, which holds the neighbour's MAC address and the rewrite string.
4. If the eBGP route is withdrawn, the OSPF route is promoted in the RIB, the FIB entry is replaced, and the hardware table is updated by the driver.

```
BR1# show ip route 10.1.0.0 255.255.0.0
  Known via "bgp 65000", distance 20, metric 0
    * 172.16.255.2, from 172.16.255.2
BR1# show ip cef 10.1.0.0/16 detail
10.1.0.0/16
  nexthop 172.16.255.2 GigabitEthernet0/0/1
```

[Result: the RIB holds two routes, the FIB one; Linux shows the same split with `ip route show table all` (the routes) and the kernel's FIB.]{.result}
:::

### Ternary memory and longest-prefix match

Looking up an address in a table of 1,000,000 prefixes by software would take dozens of memory reads ([§1.9](#s1-9){.ref} gives the trie algorithms). A *ternary content-addressable memory* (TCAM) does it in one cycle by comparing the key with every stored entry at once. Each entry stores a *value* and a *mask*, and a bit position can be 0, 1 or "don't care" (x), which is why the memory is ternary. A prefix such as 10.1.0.0/16 is stored as its 16 significant bits followed by 16 don't-cares. The match lines of all rows go to a *priority encoder*, which returns the index of the lowest matching row, and that index addresses an ordinary SRAM holding the result (the next hop). Since the lowest index wins, entries are stored in order of decreasing prefix length, which makes the first match the longest.

::: example
**Longest-prefix match in a TCAM.** The table has four entries: 10.0.0.0/8 to A, 10.1.0.0/16 to B, 10.1.2.0/24 to C and 0.0.0.0/0 to D. Look up 10.1.2.7.

1. Sort by prefix length, longest first: index 0 is the /24 (C), 1 the /16 (B), 2 the /8 (A), 3 the /0 (D).
2. The /24 is stored as 00001010.00000001.00000010.xxxxxxxx; the key is 00001010.00000001.00000010.00000111.
3. All four rows match, because each prefix covers the key (Figure 5.12). The priority encoder returns index 0, and the SRAM returns next hop C.
4. Cost: a 144-bit-wide entry, 512 K entries deep, is 144 × 524,288 = 75,497,472 bits, about 72 Mbit. A TCAM bit needs roughly twice the storage (value and mask) and considerably more area than an SRAM bit, and *every row* switches on every lookup, so power rises in proportion to depth. This explains why TCAM is the scarcest resource on a switch, and why large tables use *algorithmic* LPM in SRAM and keep TCAM for ACLs.

[Result: next hop C (the /24), found in one cycle with the lowest-index rule.]{.result}
:::

<figure>
<svg viewBox="0 0 480 168" width="480"><defs><marker id="a512" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accf"/></marker></defs><text class="lbl" x="8" y="14" text-anchor="start">Search key 10.1.2.7</text><text class="mono" x="120" y="14" text-anchor="start">00001010.00000001.00000010.00000111</text><text class="sm" x="8" y="38" text-anchor="start">idx</text><text class="sm" x="34" y="38" text-anchor="start">value / mask (x = don't care)</text><text class="sm" x="224" y="38" text-anchor="start">match</text><text class="sm" x="335" y="38" text-anchor="start">SRAM: result</text><text class="mono" x="10" y="59" text-anchor="start">0</text><rect class="box" x="30" y="44" width="186" height="20" rx="0"/><text class="mono" x="34" y="58" text-anchor="start">00001010.00000001.00000010.xxxxxxxx</text><circle class="accf" cx="236" cy="54" r="4"/><line class="lg" x1="240" y1="54" x2="270" y2="54"/><rect class="hl" x="334" y="44" width="120" height="20" rx="0"/><text class="mono" x="342" y="58" text-anchor="start">/24  →  next hop C</text><text class="mono" x="10" y="83" text-anchor="start">1</text><rect class="box" x="30" y="68" width="186" height="20" rx="0"/><text class="mono" x="34" y="82" text-anchor="start">00001010.00000001.xxxxxxxx.xxxxxxxx</text><circle class="accf" cx="236" cy="78" r="4"/><line class="lg" x1="240" y1="78" x2="270" y2="78"/><rect class="box" x="334" y="68" width="120" height="20" rx="0"/><text class="mono" x="342" y="82" text-anchor="start">/16  →  next hop B</text><text class="mono" x="10" y="107" text-anchor="start">2</text><rect class="box" x="30" y="92" width="186" height="20" rx="0"/><text class="mono" x="34" y="106" text-anchor="start">00001010.xxxxxxxx.xxxxxxxx.xxxxxxxx</text><circle class="accf" cx="236" cy="102" r="4"/><line class="lg" x1="240" y1="102" x2="270" y2="102"/><rect class="box" x="334" y="92" width="120" height="20" rx="0"/><text class="mono" x="342" y="106" text-anchor="start">/8  →  next hop A</text><text class="mono" x="10" y="131" text-anchor="start">3</text><rect class="box" x="30" y="116" width="186" height="20" rx="0"/><text class="mono" x="34" y="130" text-anchor="start">xxxxxxxx.xxxxxxxx.xxxxxxxx.xxxxxxxx</text><circle class="accf" cx="236" cy="126" r="4"/><line class="lg" x1="240" y1="126" x2="270" y2="126"/><rect class="box" x="334" y="116" width="120" height="20" rx="0"/><text class="mono" x="342" y="130" text-anchor="start">/0  →  next hop D</text><rect class="fill" x="270" y="44" width="40" height="92" rx="0"/><text class="sm" x="290" y="84" text-anchor="middle">priority</text><text class="sm" x="290" y="94" text-anchor="middle">encoder</text><text class="sm" x="290" y="110" text-anchor="middle">lowest</text><text class="sm" x="290" y="119" text-anchor="middle">index</text><path class="acc" d="M310,54 L334,54" marker-end="url(#a512)"/><text class="sm" x="240" y="158" text-anchor="middle">All four rows match in one cycle; the encoder passes index 0 to the SRAM, which returns next hop C.</text></svg>
<figcaption><b>Figure 5.12</b> A ternary lookup. Every row compares itself with the key in parallel; rows are stored longest prefix first, so the lowest matching index is the longest match.</figcaption>
</figure>

TCAM serves the *access control lists* of [§9.5](#s9-5){.ref} for the same reason: an ACL line matches ranges of header bits in priority order. Ranges are awkward, because a ternary entry can only express a power-of-two-aligned block. The port range 1024 to 65535 decomposes into six blocks (1024 to 2047, 2048 to 4095, 4096 to 8191, 8192 to 16383, 16384 to 32767 and 32768 to 65535), so a single line "permit tcp any any range 1024 65535" consumes six entries; a range on both source and destination multiplies the counts. An exact-match table, such as the MAC table, needs no ternary memory and uses a hash in SRAM.

### The ASIC pipeline

Modern chips are *pipelines*: a packet passes through a fixed series of stages, each doing one job, and many packets are in flight at once (Figure 5.13). A walk of one packet follows.

1. *Ingress port.* The MAC and physical coding sublayer check the frame and the FCS.
2. *Parser.* It extracts the Ethernet, VLAN, IP and TCP or UDP fields into a *header vector*.
3. *Ingress ACL* (TCAM). Security and QoS classification, and the decision to punt.
4. *L2 lookup* (exact-match hash on VLAN and destination MAC). For a routed packet the destination MAC is the router's own, which sends the packet to the L3 stage.
5. *L3 lookup* (LPM in TCAM or algorithmic SRAM). The result is not a single next hop but an ECMP group.
6. *ECMP resolution and adjacency.* The hash of §5.3 selects a member; the adjacency supplies the new MAC header; the TTL is decremented and the IP checksum updated.
7. *Traffic manager.* The packet is queued, in a *virtual output queue* (VOQ) for its egress port and class, in the buffer; a scheduler (strict priority, weighted round robin or deficit weighted round robin) decides when it leaves; ECN marking happens here.
8. *Egress pipeline.* An egress ACL, VXLAN or MPLS encapsulation if needed, then the deparser rebuilds the headers and the egress MAC sends the frame.

<figure>
<svg viewBox="0 0 480 182" width="480"><defs><marker id="a513" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="b513" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accf"/></marker></defs><rect class="box" x="10" y="24" width="68" height="34" rx="0"/><text class="lbl" x="44" y="38" text-anchor="middle">MAC / PCS</text><text class="sm" x="44" y="50" text-anchor="middle">ports</text><rect class="box" x="88" y="24" width="68" height="34" rx="0"/><text class="lbl" x="122" y="38" text-anchor="middle">Parser</text><text class="sm" x="122" y="50" text-anchor="middle">L2 L3 L4 fields</text><line class="ln" x1="78" y1="41" x2="88" y2="41" marker-end="url(#a513)"/><rect class="box" x="166" y="24" width="68" height="34" rx="0"/><text class="lbl" x="200" y="38" text-anchor="middle">Ingress ACL</text><text class="sm" x="200" y="50" text-anchor="middle">TCAM</text><line class="ln" x1="156" y1="41" x2="166" y2="41" marker-end="url(#a513)"/><rect class="box" x="244" y="24" width="68" height="34" rx="0"/><text class="lbl" x="278" y="38" text-anchor="middle">L2 lookup</text><text class="sm" x="278" y="50" text-anchor="middle">MAC table</text><line class="ln" x1="234" y1="41" x2="244" y2="41" marker-end="url(#a513)"/><rect class="box" x="322" y="24" width="68" height="34" rx="0"/><text class="lbl" x="356" y="38" text-anchor="middle">L3 lookup</text><text class="sm" x="356" y="50" text-anchor="middle">FIB (LPM)</text><line class="ln" x1="312" y1="41" x2="322" y2="41" marker-end="url(#a513)"/><rect class="box" x="400" y="24" width="68" height="34" rx="0"/><text class="sm" x="434" y="38" text-anchor="middle">ECMP + rewrite</text><text class="sm" x="434" y="50" text-anchor="middle">adjacency</text><line class="ln" x1="390" y1="41" x2="400" y2="41" marker-end="url(#a513)"/><text class="lbl" x="10" y="14" text-anchor="start">ingress pipeline</text><rect class="fill" x="10" y="84" width="458" height="36" rx="0"/><text class="lbl" x="239" y="99" text-anchor="middle">Traffic manager</text><text class="sm" x="239" y="112" text-anchor="middle">virtual output queues · shared or deep buffer · scheduler (SP, WRR, DWRR) · ECN marking</text><line class="ln" x1="433" y1="58" x2="433" y2="84" marker-end="url(#a513)"/><rect class="box" x="322" y="144" width="68" height="26" rx="0"/><text class="sm" x="356" y="161" text-anchor="middle">Egress queue</text><rect class="box" x="244" y="144" width="68" height="26" rx="0"/><text class="sm" x="278" y="161" text-anchor="middle">Egress ACL</text><rect class="box" x="166" y="144" width="68" height="26" rx="0"/><text class="sm" x="200" y="161" text-anchor="middle">Deparser</text><rect class="box" x="88" y="144" width="68" height="26" rx="0"/><text class="sm" x="122" y="161" text-anchor="middle">MAC / PCS</text><line class="ln" x1="356" y1="120" x2="356" y2="144" marker-end="url(#a513)"/><line class="ln" x1="322" y1="157" x2="312" y2="157" marker-end="url(#a513)"/><line class="ln" x1="244" y1="157" x2="234" y2="157" marker-end="url(#a513)"/><line class="ln" x1="166" y1="157" x2="156" y2="157" marker-end="url(#a513)"/><line class="ln" x1="88" y1="157" x2="60" y2="157" marker-end="url(#a513)"/><text class="sm" x="40" y="160" text-anchor="middle">out</text><text class="lbl" x="10" y="138" text-anchor="start">egress pipeline</text><path class="acc" d="M278,24 L278,10 L330,10" marker-end="url(#b513)"/><text class="sm" x="334" y="13" text-anchor="start">punt to CPU (TTL expiry, glean, local traffic)</text></svg>
<figcaption><b>Figure 5.13</b> A switch ASIC from ingress to egress. Each box is a hardware stage that handles a packet in a fixed number of clock cycles; the traffic manager in the middle is the only place where packets wait.</figcaption>
</figure>

Two properties of this design matter in practice. *Cut-through* switching starts to transmit a frame as soon as the header has been read, before the rest has arrived, instead of the *store-and-forward* method that waits for the whole frame. For a 1,500-byte frame the saving is the serialisation time: 12,000 bits at 10 Gb/s take 1.2 µs, at 100 Gb/s 0.12 µs. Cut-through needs the egress port to be idle and at least as fast as the ingress port; if the egress is busy or slower (10G in, 100G out would starve), the switch falls back to store-and-forward, and a frame with a bad FCS is already on its way when the error is found. Secondly, the *buffer* absorbs bursts. Shallow shared buffers (tens of megabytes for a whole chip) suit a leaf; deep buffers (gigabytes, with VOQs) suit a router at the edge of a long path. The failure mode of shallow buffers is *incast*: many servers answer one request at the same instant, say 40 senders each returning 64 KiB to one client on a 10 Gb/s port. The burst is 40 × 64 KiB = 2.5 MiB, arriving far faster than the port drains, so a buffer of 1 MiB per port overflows, the tail packets are dropped and the senders wait for the TCP retransmission timer, typically 200 ms, which is a hundred times longer than the transfer itself. Cures are ECN marking with a DCTCP-style sender ([§3.9](#s3-9){.ref}), a smaller minimum retransmission timeout, deeper buffers, or application-level staggering of the replies.

### Punts, CoPP and surviving a restart

Packets that the ASIC cannot or should not forward are *punted*, that is, handed to the route processor: packets addressed to the router itself (BGP, OSPF, SSH), packets whose TTL expires, packets that need an ARP or ND resolution (glean), packets with IP options, and ACL entries marked "log". Since the CPU is orders of magnitude slower than the ASIC, an unprotected punt path is a denial-of-service target. *Control-plane policing* (CoPP) places a rate limiter on each class of punted traffic, in hardware, before it reaches the CPU.

```
class-map match-any ROUTING
 match access-group name ROUTING-PROTOCOLS
policy-map COPP
 class ROUTING
  police rate 2000 pps conform-action transmit exceed-action drop
 class class-default
  police rate 500 pps conform-action transmit exceed-action drop
control-plane
 service-policy input COPP
```

The control plane may restart (software upgrade or crash) while the data plane keeps working. *Non-stop forwarding* (NSF) with *graceful restart* (GR) does this by cooperation: the ASIC keeps forwarding with the stale FIB, and the neighbours, acting as helpers, keep the restarting router's routes for an agreed restart time instead of withdrawing them (RFC 4724 for BGP). *Non-stop routing* (NSR) needs no help from neighbours: a standby route processor mirrors the protocol state, including the TCP sessions, and takes over invisibly.

Chips come from two sources. *Merchant silicon* is sold to any vendor and powers most data-centre switches; *custom silicon* is designed by the vendor for its own routers. The classification below is generic and approximate.

| Family | Examples | Buffer | Programmability | Typical role |
|---|---|---|---|---|
| Merchant, shallow shared buffer | Broadcom Trident and Tomahawk, Nvidia Spectrum, Marvell | tens of MB per chip | fixed pipeline, some flexible tables | leaf and spine switches |
| Merchant, deep buffer | Broadcom Jericho | gigabytes with VOQ | fixed pipeline, large FIB | WAN and aggregation routers |
| Merchant, programmable | Cisco Silicon One, Tofino (P4) | varies | programmable pipeline | fabric and edge, telemetry |
| Custom | Juniper Trio and Express, Cisco QuantumFlow | deep | programmable microcode | service-provider routers |

::: trap
*Claim:* "The TCAM stores the routing table." *Why it is wrong:* it stores the FIB (the winning routes), usually together with algorithmic SRAM for the bulk of a large table, and in the same TCAM the ACL entries compete for space, with a range line taking several entries. *Correct statement:* the RIB lives in the CPU's DRAM; the FIB, ACLs and adjacency live in the ASIC's memories.
:::

::: lens
[BROADCOM · ARISTA · JUNIPER · CISCO · NOKIA]{.co}

Platform and SDK roles probe this section deeply. Expect "RIB versus FIB", "what is TCAM and why is it expensive?", "walk a packet through the ASIC" and, as a coding question, "design a longest-prefix-match structure for one million routes" (the trie and DIR-24-8 answers are in [§1.9](#s1-9){.ref} and Q5.22). A strong answer names each stage, says where the ECMP hash sits, and explains punt and CoPP unprompted.
:::

::: check
1. Which table does the ASIC consult, the RIB or the FIB? [^c58-1]
2. Why are TCAM entries stored longest prefix first? [^c58-2]
3. How many ternary entries does the range 1024 to 65535 need? [^c58-3]
:::

[^c58-1]: The FIB (with the adjacency table); the RIB lives on the route processor.
[^c58-2]: The priority encoder returns the lowest matching index, so the longest prefix then wins.
[^c58-3]: Six.

## [5.9]{.sec}Load balancers [Must · ■■□]{.tag} {#s5-9}

::: bigidea
A load balancer presents one virtual address and spreads connections over many servers; a layer-4 balancer decides from the 5-tuple and is fast, a layer-7 balancer reads the request and is flexible, and hyperscalers build the first kind from ECMP and consistent hashing in software.
:::

A *load balancer* (LB) answers on a *virtual IP address* (VIP), chooses a *backend* server for each new connection and keeps all packets of that connection going to the same backend. A *layer-4* balancer works on addresses and ports: it never reads the payload and sees no URL. A *layer-7* balancer terminates the TCP connection (and usually TLS, [§9.4](#s9-4){.ref}), parses the HTTP request and opens a second connection to the backend, so it can route by host name or path, rewrite headers, cache and retry. The difference in cost is large, because layer 7 must hold two connections and decrypt each request.

| | Layer 4 | Layer 7 |
|---|---|---|
| Decides on | 5-tuple | URL, host, headers, cookies |
| Connection | passes packets (NAT, DSR, tunnel) | terminates and re-opens |
| TLS | passthrough | terminated here |
| Speed | millions of packets per second per node | much lower; CPU bound |
| AWS | Network Load Balancer (NLB), Gateway Load Balancer (GWLB, Geneve to appliances) | Application Load Balancer (ALB) |
| Azure | Load Balancer | Application Gateway (regional), Front Door (global) |

There are three ways for a layer-4 balancer to forward (Figure 5.14). In *NAT* (proxy) mode the balancer rewrites the destination to the backend and the reply returns through it, which also allows it to rewrite the source (SNAT). In *direct server return* (DSR) the balancer rewrites only the destination MAC (same layer-2 segment) or wraps the packet in a tunnel (IP-in-IP or GRE, any distance), and the backend replies *directly* to the client with the VIP as its source address. For the reply to be accepted by the client, the backend must own the VIP, and it is therefore configured on its loopback interface, with ARP for it suppressed (`arp_ignore=1`, `arp_announce=2` on Linux) so that the backend does not compete with the balancer for the VIP. DSR suits web traffic because responses are far larger than requests: the balancer sees only the small inbound half.

<figure>
<svg viewBox="0 0 480 232" width="480"><defs><marker id="a514" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="b514" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accf"/></marker></defs><text class="lbl" x="80" y="12" text-anchor="middle">NAT / proxy</text><rect class="box" x="54" y="22" width="52" height="18" rx="0"/><text class="lbl" x="80" y="34" text-anchor="middle">Client</text><rect class="box" x="54" y="86" width="52" height="18" rx="0"/><text class="lbl" x="80" y="98" text-anchor="middle">LB (VIP)</text><rect class="box" x="54" y="150" width="52" height="18" rx="0"/><text class="lbl" x="80" y="162" text-anchor="middle">Backend</text><text class="lbl" x="240" y="12" text-anchor="middle">DSR (direct return)</text><rect class="box" x="214" y="22" width="52" height="18" rx="0"/><text class="lbl" x="240" y="34" text-anchor="middle">Client</text><rect class="box" x="214" y="86" width="52" height="18" rx="0"/><text class="lbl" x="240" y="98" text-anchor="middle">LB (VIP)</text><rect class="box" x="214" y="150" width="52" height="18" rx="0"/><text class="lbl" x="240" y="162" text-anchor="middle">Backend</text><text class="lbl" x="400" y="12" text-anchor="middle">Tunnel (IP-in-IP / GRE)</text><rect class="box" x="374" y="22" width="52" height="18" rx="0"/><text class="lbl" x="400" y="34" text-anchor="middle">Client</text><rect class="box" x="374" y="86" width="52" height="18" rx="0"/><text class="lbl" x="400" y="98" text-anchor="middle">LB (VIP)</text><rect class="box" x="374" y="150" width="52" height="18" rx="0"/><text class="lbl" x="400" y="162" text-anchor="middle">Backend</text><line class="ln" x1="72" y1="40" x2="72" y2="86" marker-end="url(#a514)"/><text class="lbl" x="68" y="66" text-anchor="end">1</text><line class="ln" x1="72" y1="104" x2="72" y2="150" marker-end="url(#a514)"/><text class="lbl" x="68" y="130" text-anchor="end">2</text><line class="ln" x1="88" y1="150" x2="88" y2="104" marker-end="url(#a514)"/><text class="lbl" x="92" y="130" text-anchor="start">3</text><line class="ln" x1="88" y1="86" x2="88" y2="40" marker-end="url(#a514)"/><text class="lbl" x="92" y="66" text-anchor="start">4</text><line class="ln" x1="240" y1="40" x2="240" y2="86" marker-end="url(#a514)"/><text class="lbl" x="234" y="66" text-anchor="end">1</text><line class="ln" x1="240" y1="104" x2="240" y2="150" marker-end="url(#a514)"/><text class="lbl" x="234" y="130" text-anchor="end">2</text><path class="acc" d="M266,159 L290,159 L290,31 L266,31" marker-end="url(#b514)"/><text class="lbl" x="294" y="95" text-anchor="start">3</text><line class="ln" x1="400" y1="40" x2="400" y2="86" marker-end="url(#a514)"/><text class="lbl" x="394" y="66" text-anchor="end">1</text><line class="ln" x1="400" y1="104" x2="400" y2="150" marker-end="url(#a514)"/><text class="lbl" x="394" y="130" text-anchor="end">2</text><path class="acc" d="M426,159 L450,159 L450,31 L426,31" marker-end="url(#b514)"/><text class="lbl" x="454" y="95" text-anchor="start">3</text><text class="sm" x="8" y="184" text-anchor="start">1 dst = VIP</text><text class="sm" x="8" y="194" text-anchor="start">2 dst = backend, src = LB</text><text class="sm" x="8" y="204" text-anchor="start">3 reply to LB</text><text class="sm" x="8" y="214" text-anchor="start">4 src = VIP</text><text class="sm" x="170" y="184" text-anchor="start">1 dst = VIP</text><text class="sm" x="170" y="194" text-anchor="start">2 dst MAC rewritten only</text><text class="sm" x="170" y="204" text-anchor="start">3 src = VIP, direct to client</text><text class="sm" x="330" y="184" text-anchor="start">1 dst = VIP</text><text class="sm" x="330" y="194" text-anchor="start">2 outer IP to backend</text><text class="sm" x="330" y="204" text-anchor="start">3 inner src = VIP, direct</text></svg>
<figcaption><b>Figure 5.14</b> Three ways to forward to a backend. In the first the balancer sits on both directions; in the other two the reply bypasses it, so it handles only the (usually much smaller) request traffic.</figcaption>
</figure>

The balancer must also choose a backend. The common algorithms are in the table; *consistent hashing* is the one that matters at scale, because it keeps most connections on the same backend when the pool changes.

| Algorithm | Rule | Weakness |
|---|---|---|
| Round robin | next backend in turn | ignores load and request size |
| Weighted round robin | turns in proportion to weight | static weights |
| Least connections | fewest open connections | needs shared state |
| Power of two choices | pick two at random, take the less loaded | none serious; common default |
| Source or 5-tuple hash | hash of the flow | pool change reshuffles unless consistent |
| Consistent hash (Maglev) | lookup table built from per-backend permutations | table must be rebuilt on change |

::: example
**A Maglev lookup table.** Google's software balancer, Maglev (NSDI 2016), builds a table of M entries, with M prime and much larger than the number of backends; a connection is sent to `table[hash(5-tuple) mod M]`. Take M = 7 and three backends B0, B1 and B2. Each backend hashes its name into an *offset* and a *skip*, which defines a permutation of the table positions, `(offset + j × skip) mod 7`. The values are B0: offset 3, skip 4; B1: offset 0, skip 2; B2: offset 3, skip 1.

1. Permutations: B0 = 3, 0, 4, 1, 5, 2, 6; B1 = 0, 2, 4, 6, 1, 3, 5; B2 = 3, 4, 5, 6, 0, 1, 2.
2. The backends take turns, each claiming its most preferred position that is still free. Round 1: B0 takes 3, B1 takes 0, B2 wants 3 (taken) and takes 4. Round 2: B0 takes 1 (0 and 4 taken), B1 takes 2, B2 takes 5. Round 3: B0 takes 6.
3. The table is [B1, B0, B1, B0, B2, B2, B0] for positions 0 to 6: B0 has 3 entries and B1, B2 have 2 each.
4. Remove B1 and refill with B0 and B2 only. Round 1: B0 takes 3, B2 takes 4. Round 2: B0 takes 0, B2 takes 5. Round 3: B0 takes 1, B2 takes 6. Round 4: B0 takes 2. The table becomes [B0, B0, B0, B0, B2, B2, B2].
5. Compare the tables: positions 0, 2 and 6 changed, 3 of 7. Two of the changes are unavoidable (B1's own entries); the third is a side effect. A plain `hash mod N`, going from 3 backends to 2, would keep a flow only when h mod 6 is 0 or 1, so about 67% of connections move.

[Result: the new table differs in 3 of 7 entries, near the minimum of 2; a hash mod N would have moved about two thirds of the connections.]{.result}
:::

In production M is large (65,537 in the paper) so that each backend gets nearly the same number of entries, and a *connection-tracking table* on each balancer pins existing connections, so the lookup table matters only for new ones. Maglev machines are stateless peers: the edge routers spread packets over them with ECMP (§5.3), any one of them can fail, and because they all build the same table from the same backend list, a connection that lands on a different Maglev machine after a failure still reaches the same backend.

*Health checks* decide which backends are in the pool. The balancer probes each backend (a TCP connect, or an HTTP request for a given URL) at an interval and applies hysteresis: a backend moves from Up to Down after, say, three consecutive failures, and from Down back to Up only after two consecutive successes, which prevents flapping. *Session persistence* (sticky sessions) maps one client to one backend by cookie or source address, which is needed only when the application keeps per-user state in memory. A last pitfall concerns NAT mode and outbound connections: a balancer or NAT gateway has one public address and so about 64,000 source ports per destination address and port; many short connections to the same destination exhaust them, and new connections fail. This is *SNAT port exhaustion*, met again in §5.12.

::: trap
*Claim:* "An L4 load balancer can route /api and /images to different pools." *Why it is wrong:* it never reads the HTTP request, and with TLS passthrough it could not even decrypt it. *Correct statement:* path-based routing needs a layer-7 balancer (ALB, Application Gateway); a layer-4 balancer routes by address and port.
:::

::: check
1. Why must a DSR backend carry the VIP on its loopback? [^c59-1]
2. What advantage does DSR give the balancer? [^c59-2]
3. Why is the Maglev table size a prime much larger than the number of backends? [^c59-3]
:::

[^c59-1]: The reply leaves with the VIP as its source, and the client only accepts replies from the address it contacted.
[^c59-2]: It carries only the (small) request half of the traffic.
[^c59-3]: A prime keeps every permutation complete, and a large table gives each backend almost the same share.

## [5.10]{.sec}Anycast and content delivery networks [Should · ■■□]{.tag} {#s5-10}

::: bigidea
Announcing one prefix from many sites lets BGP deliver every user to the nearest site in routing terms, and a content delivery network adds caches at those sites so that most requests never travel to the origin.
:::

In *anycast* the same IP address is announced from several places, and the Internet's routing sends each packet to whichever announcement is best from the sender's position ([§4.7](#s4-7){.ref}). Nothing in the protocol is special; the routers simply see several paths to one prefix and choose by the usual BGP rules, usually the shortest AS_PATH, then the closest exit by IGP cost. The root name servers, public resolvers and CDNs all use it. It gives short paths, automatic failover (a site that stops announcing is removed from the table) and absorption of attacks, since flood traffic is divided among the sites by where it originates.

::: example
**Anycast from three sites.** The prefix 192.0.2.0/24 (origin AS 64496) is announced from Mumbai, Singapore and Frankfurt. A user in Chennai is behind ISP AS 64510 (Figure 5.15).

1. ISP 64510 learns three paths: AS_PATH 64496 from Mumbai, 64520 64496 from Singapore, 64530 64496 from Frankfurt.
2. BGP prefers the shortest AS_PATH, so Chennai traffic goes to Mumbai.
3. Mumbai is taken down for maintenance and withdraws the prefix. The ISP removes that path, and the best remaining path (a tie in length, broken by IGP cost) takes the traffic to Singapore within the BGP convergence time.
4. A TCP connection that was open to Mumbai now sends its segments to Singapore, which has no state for it and answers with a reset. Anycast therefore suits short exchanges (DNS, short HTTP requests) and long connections only if routing is stable.

[Result: the user lands on the BGP-nearest site, and failover is a routing withdrawal.]{.result}
:::

<figure>
<svg viewBox="0 0 480 200" width="480"><defs><marker id="a515" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accf"/></marker></defs><rect class="box" x="30" y="10" width="100" height="30" rx="0"/><text class="lbl" x="80" y="23" text-anchor="middle">Mumbai PoP</text><text class="sm" x="80" y="34" text-anchor="middle">192.0.2.0/24 origin AS 64496</text><rect class="box" x="190" y="10" width="100" height="30" rx="0"/><text class="lbl" x="240" y="23" text-anchor="middle">Singapore PoP</text><text class="sm" x="240" y="34" text-anchor="middle">192.0.2.0/24 origin AS 64496</text><rect class="box" x="350" y="10" width="100" height="30" rx="0"/><text class="lbl" x="400" y="23" text-anchor="middle">Frankfurt PoP</text><text class="sm" x="400" y="34" text-anchor="middle">192.0.2.0/24 origin AS 64496</text><rect class="box" x="190" y="100" width="100" height="26" rx="0"/><text class="lbl" x="240" y="113" text-anchor="middle">ISP, Chennai side</text><text class="sm" x="240" y="122" text-anchor="middle">AS 64510</text><line class="lg" x1="80" y1="40" x2="240" y2="100"/><line class="lg" x1="240" y1="40" x2="240" y2="100"/><line class="lg" x1="400" y1="40" x2="240" y2="100"/><path class="acc" d="M80,40 L225,100"/><text class="sm" x="100" y="76" text-anchor="end">AS_PATH 64496</text><text class="sm" x="250" y="64" text-anchor="start">64520 64496</text><text class="sm" x="390" y="76" text-anchor="end">64530 64496</text><rect class="fill" x="205" y="150" width="70" height="22" rx="0"/><text class="lbl" x="240" y="164" text-anchor="middle">User, Chennai</text><line class="ln" x1="240" y1="126" x2="240" y2="150"/><text class="sm" x="240" y="190" text-anchor="middle">Shortest AS_PATH wins; if Mumbai withdraws, the next-best path (Singapore) takes over.</text></svg>
<figcaption><b>Figure 5.15</b> One prefix announced from three sites. The ISP's router picks one path by ordinary BGP rules, so each user lands on the site that is nearest in routing terms, not necessarily in kilometres.</figcaption>
</figure>

A *CDN* places *edge* caches at such sites. A request first needs the CDN's address: the site's name is a CNAME to the CDN's domain, and the CDN's DNS server either returns an anycast address or, in *DNS-based global server load balancing*, returns the address of the edge it judges best for the client's resolver. DNS-based steering can use measured latency and load but sees only the *resolver's* address, so the extension *EDNS Client Subnet* passes a prefix of the client's address to the authoritative server. An edge that holds the object (a *hit*) replies at once; on a *miss* it fetches the object from a mid-tier cache or the origin, stores it according to the `Cache-Control` and TTL headers, and replies.

::: example
**What a CDN saves.** The origin is 220 ms away, the edge 15 ms away, and 90% of requests hit.

1. A hit costs the edge round trip: 15 ms.
2. A miss costs the edge plus the origin trip: 15 + 220 = 235 ms.
3. The expected time is 0.9 × 15 + 0.1 × 235 = 13.5 + 23.5 = 37 ms, against 235 ms with no cache.
4. Raising the hit ratio to 99% gives 0.99 × 15 + 0.01 × 235 = 17.2 ms. Each point of hit ratio is worth about 2.2 ms here.

[Result: 37 ms expected, about six times faster than going to the origin every time.]{.result}
:::

| | DNS-based steering | Anycast |
|---|---|---|
| Decision made by | the CDN's DNS server, from the resolver's address | BGP, from the user's network position |
| Failover speed | bounded by DNS TTL and client caching | BGP convergence (seconds) |
| Granularity | per resolver or client subnet; can use load and latency | coarse; by path length |
| Weakness | the resolver may be far from the client | route changes break long connections |

::: trap
*Claim:* "Anycast sends a user to the geographically nearest site." *Why it is wrong:* BGP knows paths, not kilometres; a user may be served from another continent when their ISP peers with the CDN there. *Correct statement:* anycast selects the BGP-nearest site, and operators influence this by choosing where to announce and by prepending.
:::

::: check
1. What does BGP use to choose between anycast sites? [^c510-1]
2. What happens to an open TCP connection when the route changes to another site? [^c510-2]
3. Compute the expected latency for a 95% hit ratio, edge 20 ms and origin 180 ms. [^c510-3]
:::

[^c510-1]: The ordinary best-path rules: usually shortest AS_PATH, then lowest IGP cost to the exit.
[^c510-2]: The new site has no state for it and resets it (unless the sites share connection state).
[^c510-3]: 0.95 × 20 + 0.05 × 200 = 19 + 10 = 29 ms.

:::
