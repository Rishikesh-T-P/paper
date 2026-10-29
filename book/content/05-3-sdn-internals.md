::: {.p5}

## [5.7]{.sec}SDN, OpenFlow and P4 [Should · ■■□]{.tag} {#s5-7}

::: bigidea
Software-defined networking moves the decisions out of each switch into a logically central controller and leaves the switch with a fast table lookup; P4 goes one step further and lets the operator define what the table and the packet parser look like.
:::

In a traditional device the *control plane* (routing protocols that decide) and the *data plane* (hardware that forwards) share a box, and each device decides alone. *Software-defined networking* (SDN) separates them: a *controller* holds the network-wide view, computes the forwarding rules and installs them in switches through a *southbound* interface; applications ask the controller for services through a *northbound* interface, often REST or gRPC (Figure 5.12). Two motivations drive it. A central view allows global optimisation that a distributed protocol cannot do, and a programmable interface lets software, not command-line scripts, manage thousands of devices. Google's B4 wide-area network, whose controller computes traffic-engineering paths, is the standard example, and Google's data-centre controller does the same for the Jupiter fabric.

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
priority=100,ip,nw_dst=10.0.0.2 actions=output:2        n_packets=5
priority=50,arp actions=FLOOD                           n_packets=2
priority=0 actions=CONTROLLER:65535                     n_packets=1
```

1. The first ARP from h1 matches priority 50 and is flooded (2 packets).
2. The echo requests to 10.0.0.2 match priority 100 and go to port 2; the counters rise with each ping (5 here).
3. Anything else, such as a packet to an unknown address, falls to priority 0 and is sent to the controller (1 packet).

[Result: matching is by priority, counters show which rule fires, and the priority-0 entry is the table-miss rule.]{.result}
:::

<figure>
<svg viewBox="0 0 480 192" width="480"><defs><marker id="a510" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker></defs><text class="lbl" x="95" y="12" text-anchor="middle">SDN layers</text><rect class="box" x="25" y="22" width="140" height="28" rx="0"/><text class="lbl" x="95" y="34" text-anchor="middle">Applications</text><text class="sm" x="95" y="45" text-anchor="middle">routing · TE · policy · LB</text><rect class="box" x="25" y="84" width="140" height="28" rx="0"/><text class="lbl" x="95" y="96" text-anchor="middle">Controller</text><text class="sm" x="95" y="107" text-anchor="middle">ONOS · Ryu · in-house</text><rect class="box" x="10" y="146" width="52" height="22" rx="0"/><text class="sm" x="36" y="160" text-anchor="middle">Switch</text><line class="lg" x1="36" y1="146" x2="95" y2="112"/><rect class="box" x="72" y="146" width="52" height="22" rx="0"/><text class="sm" x="98" y="160" text-anchor="middle">Switch</text><line class="lg" x1="98" y1="146" x2="95" y2="112"/><rect class="box" x="134" y="146" width="52" height="22" rx="0"/><text class="sm" x="160" y="160" text-anchor="middle">Switch</text><line class="lg" x1="160" y1="146" x2="95" y2="112"/><line class="ln" x1="95" y1="50" x2="95" y2="84"/><text class="sm" x="100" y="62" text-anchor="start">northbound:</text><text class="sm" x="100" y="72" text-anchor="start">REST, gRPC</text><text class="sm" x="95" y="182" text-anchor="middle">southbound: OpenFlow, P4Runtime, gNMI</text><text class="lbl" x="333" y="12" text-anchor="middle">PISA pipeline (P4 target)</text><rect class="box" x="206" y="40" width="46" height="50" rx="0"/><text class="sm" x="229.0" y="62" text-anchor="middle">Parser</text><rect class="box" x="262" y="40" width="40" height="50" rx="0"/><text class="sm" x="282.0" y="62" text-anchor="middle">Stage 1</text><rect class="box" x="312" y="40" width="40" height="50" rx="0"/><text class="sm" x="332.0" y="62" text-anchor="middle">Stage 2</text><rect class="box" x="362" y="40" width="40" height="50" rx="0"/><text class="sm" x="382.0" y="62" text-anchor="middle">Stage N</text><rect class="box" x="412" y="40" width="48" height="50" rx="0"/><text class="sm" x="436.0" y="62" text-anchor="middle">Deparser</text><text class="sm" x="282.0" y="76" text-anchor="middle">table</text><text class="sm" x="282.0" y="85" text-anchor="middle">+ ALU</text><text class="sm" x="332.0" y="76" text-anchor="middle">table</text><text class="sm" x="332.0" y="85" text-anchor="middle">+ ALU</text><text class="sm" x="382.0" y="76" text-anchor="middle">table</text><text class="sm" x="382.0" y="85" text-anchor="middle">+ ALU</text><line class="ln" x1="252" y1="65" x2="262" y2="65" marker-end="url(#a510)"/><line class="ln" x1="302" y1="65" x2="312" y2="65" marker-end="url(#a510)"/><line class="ln" x1="352" y1="65" x2="362" y2="65" marker-end="url(#a510)"/><line class="ln" x1="402" y1="65" x2="412" y2="65" marker-end="url(#a510)"/><line class="lg dash" x1="206" y1="106" x2="460" y2="106"/><text class="sm" x="333" y="120" text-anchor="middle">metadata bus (ingress port, next hop, user fields)</text><text class="sm" x="229" y="34" text-anchor="middle">bytes in</text><text class="sm" x="436" y="34" text-anchor="middle">bytes out</text><text class="sm" x="333" y="148" text-anchor="middle">The parser and every table are defined by the P4 program.</text></svg>
<figcaption><b>Figure 5.12</b> Left: the SDN split between applications, a logically central controller and simple switches. Right: the protocol-independent switch architecture that P4 targets, in which the parser, the tables and the deparser are all defined by the program.</figcaption>
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

## [5.8]{.sec}Router and switch internals: RIB, FIB, TCAM and the ASIC [Must · ■■■]{.tag} {#s5-8}

::: bigidea
A router is two machines in one box: a slow, general-purpose computer that decides routes, and a fast, fixed-function chip that forwards packets by looking up a compact copy of those decisions, so the two are joined by a download path and an exception path.
:::

Pillar 4 introduced the *management*, *control* and *data* planes at the command line ([§4.1](#s4-1){.ref}), and the routing table and administrative distance ([§4.4](#s4-4){.ref}). This section opens the box and is the canonical place for what happens inside. The *control plane* runs on the *route processor*, an ordinary CPU with DRAM and an operating system: the BGP, OSPF and IS-IS processes exchange messages with neighbours and build tables of routes. The *data plane* runs on one or more *forwarding ASICs* (application-specific integrated circuits) that examine every packet in a fixed, small number of clock cycles. The CPU handles thousands of packets per second; the ASIC handles billions. The structure is drawn in Figure 5.13.

<figure>
<svg viewBox="0 0 480 256" width="480"><defs><marker id="a511" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="b511" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accf"/></marker></defs><rect class="box" x="60" y="8" width="300" height="86" rx="0"/><text class="lbl" x="80" y="22" text-anchor="start">Route processor (CPU + DRAM): control plane</text><rect class="fill" x="72" y="32" width="100" height="24" rx="0"/><text class="sm" x="122" y="47" text-anchor="middle">BGP · OSPF · IS-IS</text><rect class="fill" x="190" y="32" width="64" height="24" rx="0"/><text class="lbl" x="222" y="47" text-anchor="middle">RIB</text><rect class="fill" x="272" y="32" width="76" height="24" rx="0"/><text class="sm" x="310" y="47" text-anchor="middle">SDK / driver</text><rect class="fill" x="72" y="64" width="100" height="22" rx="0"/><text class="sm" x="122" y="78" text-anchor="middle">ARP / ND · SSH · SNMP</text><line class="ln" x1="172" y1="44" x2="190" y2="44"/><line class="ln" x1="254" y1="44" x2="272" y2="44"/><rect class="box" x="60" y="150" width="300" height="70" rx="0"/><text class="lbl" x="80" y="164" text-anchor="start">Line card / ASIC: data plane</text><rect class="fill" x="72" y="174" width="80" height="36" rx="0"/><text class="sm" x="112" y="189" text-anchor="middle">FIB (LPM)</text><text class="sm" x="112" y="200" text-anchor="middle">adjacency</text><rect class="fill" x="162" y="174" width="80" height="36" rx="0"/><text class="sm" x="202" y="189" text-anchor="middle">ACL TCAM</text><text class="sm" x="202" y="200" text-anchor="middle">counters</text><rect class="fill" x="252" y="174" width="96" height="36" rx="0"/><text class="sm" x="300" y="189" text-anchor="middle">queues · buffers</text><text class="sm" x="300" y="200" text-anchor="middle">rewrite engine</text><line class="ln" x1="310" y1="56" x2="310" y2="150" marker-end="url(#a511)"/><text class="sm" x="316" y="128" text-anchor="start">FIB download</text><rect class="box" x="150" y="104" width="100" height="18" rx="0"/><text class="sm" x="200" y="116" text-anchor="middle">CoPP policer</text><path class="acc" d="M200,174 L200,160 L200,122 M200,104 L200,94" marker-end="url(#b511)"/><text class="sm acct" x="120" y="134" text-anchor="middle">punt path</text><line class="lg" x1="60" y1="236" x2="360" y2="236"/><text class="sm" x="210" y="248" text-anchor="middle">ports</text><line class="ln" x1="110" y1="236" x2="110" y2="222" marker-end="url(#a511)"/><line class="ln" x1="310" y1="222" x2="310" y2="236" marker-end="url(#a511)"/><text class="sm" x="372" y="80" text-anchor="start">slow path: ms,</text><text class="sm" x="372" y="90" text-anchor="start">kilo-packets per second</text><text class="sm" x="372" y="190" text-anchor="start">fast path: ns,</text><text class="sm" x="372" y="200" text-anchor="start">billions of packets/s</text></svg>
<figcaption><b>Figure 5.13</b> Control plane above, data plane below. Routes flow down as FIB entries; packets that the hardware cannot handle (the accent path) flow up, through a policer that protects the CPU.</figcaption>
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
3. All four rows match, because each prefix covers the key (Figure 5.14). The priority encoder returns index 0, and the SRAM returns next hop C.
4. Cost: a 144-bit-wide entry, 512 K entries deep, is 144 × 524,288 = 75,497,472 bits, about 72 Mbit. A TCAM bit needs roughly twice the storage (value and mask) and considerably more area than an SRAM bit, and *every row* switches on every lookup, so power rises in proportion to depth. This explains why TCAM is the scarcest resource on a switch, and why large tables use *algorithmic* LPM in SRAM and keep TCAM for ACLs.

[Result: next hop C (the /24), found in one cycle with the lowest-index rule.]{.result}
:::

<figure>
<svg viewBox="0 0 480 168" width="480"><defs><marker id="a512" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accf"/></marker></defs><text class="lbl" x="8" y="14" text-anchor="start">Search key 10.1.2.7</text><text class="mono" x="120" y="14" text-anchor="start">00001010.00000001.00000010.00000111</text><text class="sm" x="8" y="38" text-anchor="start">idx</text><text class="sm" x="34" y="38" text-anchor="start">value / mask (x = don't care)</text><text class="sm" x="224" y="38" text-anchor="start">match</text><text class="sm" x="335" y="38" text-anchor="start">SRAM: result</text><text class="mono" x="10" y="59" text-anchor="start">0</text><rect class="box" x="30" y="44" width="186" height="20" rx="0"/><text class="mono" x="34" y="58" text-anchor="start">00001010.00000001.00000010.xxxxxxxx</text><circle class="accf" cx="236" cy="54" r="4"/><line class="lg" x1="240" y1="54" x2="270" y2="54"/><rect class="hl" x="334" y="44" width="120" height="20" rx="0"/><text class="mono" x="342" y="58" text-anchor="start">/24  →  next hop C</text><text class="mono" x="10" y="83" text-anchor="start">1</text><rect class="box" x="30" y="68" width="186" height="20" rx="0"/><text class="mono" x="34" y="82" text-anchor="start">00001010.00000001.xxxxxxxx.xxxxxxxx</text><circle class="accf" cx="236" cy="78" r="4"/><line class="lg" x1="240" y1="78" x2="270" y2="78"/><rect class="box" x="334" y="68" width="120" height="20" rx="0"/><text class="mono" x="342" y="82" text-anchor="start">/16  →  next hop B</text><text class="mono" x="10" y="107" text-anchor="start">2</text><rect class="box" x="30" y="92" width="186" height="20" rx="0"/><text class="mono" x="34" y="106" text-anchor="start">00001010.xxxxxxxx.xxxxxxxx.xxxxxxxx</text><circle class="accf" cx="236" cy="102" r="4"/><line class="lg" x1="240" y1="102" x2="270" y2="102"/><rect class="box" x="334" y="92" width="120" height="20" rx="0"/><text class="mono" x="342" y="106" text-anchor="start">/8  →  next hop A</text><text class="mono" x="10" y="131" text-anchor="start">3</text><rect class="box" x="30" y="116" width="186" height="20" rx="0"/><text class="mono" x="34" y="130" text-anchor="start">xxxxxxxx.xxxxxxxx.xxxxxxxx.xxxxxxxx</text><circle class="accf" cx="236" cy="126" r="4"/><line class="lg" x1="240" y1="126" x2="270" y2="126"/><rect class="box" x="334" y="116" width="120" height="20" rx="0"/><text class="mono" x="342" y="130" text-anchor="start">/0  →  next hop D</text><rect class="fill" x="270" y="44" width="40" height="92" rx="0"/><text class="sm" x="290" y="84" text-anchor="middle">priority</text><text class="sm" x="290" y="94" text-anchor="middle">encoder</text><text class="sm" x="290" y="110" text-anchor="middle">lowest</text><text class="sm" x="290" y="119" text-anchor="middle">index</text><path class="acc" d="M310,54 L334,54" marker-end="url(#a512)"/><text class="sm" x="240" y="158" text-anchor="middle">All four rows match in one cycle; the encoder passes index 0 to the SRAM, which returns next hop C.</text></svg>
<figcaption><b>Figure 5.14</b> A ternary lookup. Every row compares itself with the key in parallel; rows are stored longest prefix first, so the lowest matching index is the longest match.</figcaption>
</figure>

TCAM serves the *access control lists* of [§9.5](#s9-5){.ref} for the same reason: an ACL line matches ranges of header bits in priority order. Ranges are awkward, because a ternary entry can only express a power-of-two-aligned block. The port range 1024 to 65535 decomposes into six blocks (1024 to 2047, 2048 to 4095, 4096 to 8191, 8192 to 16383, 16384 to 32767 and 32768 to 65535), so a single line "permit tcp any any range 1024 65535" consumes six entries; a range on both source and destination multiplies the counts. An exact-match table, such as the MAC table, needs no ternary memory and uses a hash in SRAM.

### The ASIC pipeline

Modern chips are *pipelines*: a packet passes through a fixed series of stages, each doing one job, and many packets are in flight at once (Figure 5.15). A walk of one packet follows.

1. *Ingress port.* The MAC and physical coding sublayer check the frame and the FCS.
2. *Parser.* It extracts the Ethernet, VLAN, IP and TCP or UDP fields into a *header vector*.
3. *Ingress ACL* (TCAM). Security and QoS classification, and the decision to punt.
4. *L2 lookup* (exact-match hash on VLAN and destination MAC). For a routed packet the destination MAC is the router's own, which sends the packet to the L3 stage.
5. *L3 lookup* (LPM in TCAM or algorithmic SRAM). The result is not a single next hop but an ECMP group.
6. *ECMP resolution and adjacency.* The hash of §5.3 selects a member; the adjacency supplies the new MAC header; the TTL is decremented and the IP checksum updated.
7. *Traffic manager.* The packet is queued, in a *virtual output queue* (VOQ) for its egress port and class, in the buffer; a scheduler (strict priority, weighted round robin or deficit weighted round robin) decides when it leaves; ECN marking happens here.
8. *Egress pipeline.* An egress ACL, VXLAN or MPLS encapsulation if needed, then the deparser rebuilds the headers and the egress MAC sends the frame.

<figure>
<svg viewBox="0 0 480 182" width="480"><defs><marker id="a513" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="b513" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accf"/></marker></defs><rect class="box" x="10" y="24" width="68" height="34" rx="0"/><text class="lbl" x="44" y="38" text-anchor="middle">MAC / PCS</text><text class="sm" x="44" y="50" text-anchor="middle">ports</text><rect class="box" x="88" y="24" width="68" height="34" rx="0"/><text class="lbl" x="122" y="38" text-anchor="middle">Parser</text><text class="sm" x="122" y="50" text-anchor="middle">L2 L3 L4 fields</text><line class="ln" x1="78" y1="41" x2="88" y2="41" marker-end="url(#a513)"/><rect class="box" x="166" y="24" width="68" height="34" rx="0"/><text class="lbl" x="200" y="38" text-anchor="middle">Ingress ACL</text><text class="sm" x="200" y="50" text-anchor="middle">TCAM</text><line class="ln" x1="156" y1="41" x2="166" y2="41" marker-end="url(#a513)"/><rect class="box" x="244" y="24" width="68" height="34" rx="0"/><text class="lbl" x="278" y="38" text-anchor="middle">L2 lookup</text><text class="sm" x="278" y="50" text-anchor="middle">MAC table</text><line class="ln" x1="234" y1="41" x2="244" y2="41" marker-end="url(#a513)"/><rect class="box" x="322" y="24" width="68" height="34" rx="0"/><text class="lbl" x="356" y="38" text-anchor="middle">L3 lookup</text><text class="sm" x="356" y="50" text-anchor="middle">FIB (LPM)</text><line class="ln" x1="312" y1="41" x2="322" y2="41" marker-end="url(#a513)"/><rect class="box" x="400" y="24" width="68" height="34" rx="0"/><text class="sm" x="434" y="38" text-anchor="middle">ECMP + rewrite</text><text class="sm" x="434" y="50" text-anchor="middle">adjacency</text><line class="ln" x1="390" y1="41" x2="400" y2="41" marker-end="url(#a513)"/><text class="lbl" x="10" y="14" text-anchor="start">ingress pipeline</text><rect class="fill" x="10" y="84" width="458" height="36" rx="0"/><text class="lbl" x="239" y="99" text-anchor="middle">Traffic manager</text><text class="sm" x="239" y="112" text-anchor="middle">virtual output queues · shared or deep buffer · scheduler (SP, WRR, DWRR) · ECN marking</text><line class="ln" x1="433" y1="58" x2="433" y2="84" marker-end="url(#a513)"/><rect class="box" x="322" y="144" width="68" height="26" rx="0"/><text class="sm" x="356" y="161" text-anchor="middle">Egress queue</text><rect class="box" x="244" y="144" width="68" height="26" rx="0"/><text class="sm" x="278" y="161" text-anchor="middle">Egress ACL</text><rect class="box" x="166" y="144" width="68" height="26" rx="0"/><text class="sm" x="200" y="161" text-anchor="middle">Deparser</text><rect class="box" x="88" y="144" width="68" height="26" rx="0"/><text class="sm" x="122" y="161" text-anchor="middle">MAC / PCS</text><line class="ln" x1="356" y1="120" x2="356" y2="144" marker-end="url(#a513)"/><line class="ln" x1="322" y1="157" x2="312" y2="157" marker-end="url(#a513)"/><line class="ln" x1="244" y1="157" x2="234" y2="157" marker-end="url(#a513)"/><line class="ln" x1="166" y1="157" x2="156" y2="157" marker-end="url(#a513)"/><line class="ln" x1="88" y1="157" x2="60" y2="157" marker-end="url(#a513)"/><text class="sm" x="40" y="160" text-anchor="middle">out</text><text class="lbl" x="10" y="138" text-anchor="start">egress pipeline</text><path class="acc" d="M278,24 L278,10 L330,10" marker-end="url(#b513)"/><text class="sm" x="334" y="13" text-anchor="start">punt to CPU</text></svg>
<figcaption><b>Figure 5.15</b> A switch ASIC from ingress to egress. Each box is a hardware stage that handles a packet in a fixed number of clock cycles; the traffic manager in the middle is the only place where packets wait.</figcaption>
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

::: lab
`LAB 5.8 · 2 H`  Implement the binary trie of [§1.9](#s1-9){.ref} and test it against a brute-force longest-prefix match, which is the specification the trie must agree with.

```
for _ in range(100000):
    ip = random.getrandbits(32)
    want = max((p for p in prefixes if matches(p, ip)), key=lambda p: p.len, default=None)
    assert trie.lookup(ip) == (want.nexthop if want else None)
```

**What you should notice:** with 10,000 random prefixes the two agree on every address (including the default-route and nested-prefix cases you add on purpose), and the trie answers in at most 32 steps while the scan reads every entry. Time both, then replace the trie's 1-bit stride by 8 bits and count the memory accesses per lookup.
:::

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

:::
