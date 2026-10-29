::: {.p4}

## [4.11]{.sec}Quality of Service [Should · ■■□]{.tag} {#s4-11}

::: bigidea
When a link is congested, QoS decides who waits and who is dropped, so it is applied where congestion happens, using markings made once at the edge of the network.
:::

Voice needs a one-way delay of no more than about 150 ms, jitter of at most 30 ms and loss below 1%; bulk transfers tolerate none of these constraints being met so strictly, since TCP retransmits. Three models exist: best effort (no distinction), IntServ (reserve per flow with RSVP, which does not scale) and *DiffServ*, in which packets carry a marking and each router applies a *per-hop behaviour* (PHB) by class. DiffServ is the model in use.

The marking is the *DSCP* (differentiated services code point), the top six bits of the IP ToS byte; the bottom two are ECN. Layer 2 has its own 3-bit field, CoS (802.1p), in the 802.1Q tag. Marking is trusted only inside a *trust boundary*, typically at the access switch where an IP phone is recognised; everything else is re-marked.

<figure>
<svg viewBox="0 0 480 90" width="480">
  <rect class="box" x="10" y="10" width="60" height="26"/><text class="lbl" x="40" y="27" text-anchor="middle">x</text>
  <rect class="box" x="70" y="10" width="60" height="26"/><text class="lbl" x="100" y="27" text-anchor="middle">x</text>
  <rect class="box" x="130" y="10" width="60" height="26"/><text class="lbl" x="160" y="27" text-anchor="middle">x</text>
  <rect class="fill" x="190" y="10" width="60" height="26"/><text class="lbl" x="220" y="27" text-anchor="middle">y</text>
  <rect class="fill" x="250" y="10" width="60" height="26"/><text class="lbl" x="280" y="27" text-anchor="middle">y</text>
  <rect class="box" x="310" y="10" width="60" height="26"/><text class="lbl" x="340" y="27" text-anchor="middle">0</text>
  <rect class="hl" x="370" y="10" width="100" height="26"/><text class="lbl" x="420" y="27" text-anchor="middle">ECN 2 bits</text>
  <path class="ln" d="M10,44 L10,48 L370,48 L370,44"/><text class="sm" x="190" y="60" text-anchor="middle">DSCP 6 bits = class xxx, drop precedence yy, 0</text>
  <text class="sm" x="10" y="78">AFxy = 8x + 2y (AF31 = 26 = 011010). EF = 46 = 101110, ToS byte 0xB8. CSn = 8n. The top three bits alone are IP precedence.</text>
</svg>
<figcaption><b>Figure 4.35</b> The ToS byte. Assured Forwarding classes AF1 to AF4 each have three drop precedences.</figcaption>
</figure>

| PHB | DSCP | Typical use |
|---|---|---|
| EF | 46 | voice |
| AF41 / AF31 / AF21 / AF11 | 34 / 26 / 18 / 10 | video, critical data, transactional, bulk |
| CS6 / CS3 | 48 / 24 | network control, signalling |
| CS1 | 8 | scavenger (below best effort) |
| default | 0 | best effort |

<figure>
<svg viewBox="0 0 480 140" width="480">
  <defs><marker id="q411" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="#1A1D23"/></marker></defs>
  <rect class="box" x="10" y="40" width="80" height="36" rx="2"/><text class="lbl" x="50" y="56" text-anchor="middle">Classify</text><text class="sm" x="50" y="68" text-anchor="middle">and mark</text>
  <rect class="box" x="120" y="40" width="64" height="36" rx="2"/><text class="lbl" x="152" y="56" text-anchor="middle">Police or</text><text class="sm" x="152" y="68" text-anchor="middle">shape</text>
  <rect class="hl" x="220" y="10" width="110" height="24" rx="2"/><text class="lbl" x="275" y="26" text-anchor="middle">LLQ (voice)</text>
  <rect class="box" x="220" y="44" width="110" height="24" rx="2"/><text class="lbl" x="275" y="60" text-anchor="middle">CBWFQ class A</text>
  <rect class="box" x="220" y="78" width="110" height="24" rx="2"/><text class="lbl" x="275" y="94" text-anchor="middle">CBWFQ class B</text>
  <rect class="fill" x="220" y="112" width="110" height="24" rx="2"/><text class="lbl" x="275" y="128" text-anchor="middle">class-default</text>
  <rect class="box" x="370" y="40" width="70" height="36" rx="2"/><text class="lbl" x="405" y="56" text-anchor="middle">Scheduler</text><text class="sm" x="405" y="68" text-anchor="middle">to the wire</text>
  <line class="ln" x1="90" y1="58" x2="120" y2="58" marker-end="url(#q411)"/><line class="ln" x1="184" y1="58" x2="220" y2="22" marker-end="url(#q411)"/><line class="ln" x1="184" y1="58" x2="220" y2="56" marker-end="url(#q411)"/><line class="ln" x1="184" y1="58" x2="220" y2="90" marker-end="url(#q411)"/><line class="ln" x1="184" y1="58" x2="220" y2="124" marker-end="url(#q411)"/>
  <line class="ln" x1="330" y1="22" x2="370" y2="52" marker-end="url(#q411)"/><line class="ln" x1="330" y1="56" x2="370" y2="58" marker-end="url(#q411)"/><line class="ln" x1="330" y1="90" x2="370" y2="64" marker-end="url(#q411)"/><line class="ln" x1="330" y1="124" x2="370" y2="70" marker-end="url(#q411)"/>
</svg>
<figcaption><b>Figure 4.36</b> The QoS pipeline. Marking happens once at the trust boundary; queuing happens at every congested egress.</figcaption>
</figure>

<figure>
<svg viewBox="0 0 480 130" width="480">
  <text class="sm" x="10" y="12">Input: a bursty flow above the committed rate</text>
  <path class="lg" d="M20,100 L20,24 M20,100 L220,100"/><path class="ln" d="M20,70 L50,70 L50,30 L90,30 L90,70 L130,70 L130,40 L170,40 L170,70 L210,70"/><line class="lg dash" x1="20" y1="60" x2="220" y2="60"/><text class="sm" x="22" y="112">time</text><text class="sm" x="190" y="56">CIR</text>
  <text class="sm" x="250" y="12">Policer: peaks cut (drop or re-mark)</text>
  <path class="lg" d="M250,100 L250,24 M250,100 L450,100"/><path class="ln" d="M250,70 L280,70 L280,60 L320,60 L320,70 L360,70 L360,60 L400,60 L400,70 L440,70"/><line class="lg dash" x1="250" y1="60" x2="450" y2="60"/>
  <text class="sm" x="250" y="124">Shaper: peaks delayed (smooth output)</text>
  <path class="acc" d="M250,106 L275,106 L275,106 L300,106"/>
</svg>
<figcaption><b>Figure 4.37</b> Policing against shaping for the same input (left). The policer clips the peaks at the committed rate; the shaper would instead hold the excess and send it later, so total volume is preserved but delay grows.</figcaption>
</figure>

Queuing then orders the packets. *CBWFQ* gives each class a guaranteed share of bandwidth; *LLQ* adds a strict-priority queue for voice, which has an implicit policer so that it cannot starve the other classes. *WRED* drops packets early and randomly as a queue fills, with a rising probability between a minimum and a maximum threshold, and with higher drop probability for higher drop-precedence markings; it prevents *global synchronisation*, in which tail drop makes all TCP flows back off together. *Policing* and *shaping* both use a token bucket (fills at the committed rate, CIR; capacity is the burst size Bc): a policer discards or re-marks packets that find no tokens, while a shaper delays them in a buffer. Shaping thus adds delay but loses less; policing adds none but TCP sees loss and its window oscillates. A shaper's time interval is Tc = Bc / CIR.

A token bucket works as follows. Tokens, each worth one bit, arrive at the committed rate (CIR) and accumulate up to a limit Bc (a second bucket with Be allows an excess burst). A packet of *n* bits may be sent only if *n* tokens are available; they are then removed. A policer tests the bucket on arrival and acts on the packet at once (transmit, re-mark or drop, giving conform, exceed and violate actions). A shaper keeps the packet in a queue until enough tokens exist. The *time interval* Tc = Bc / CIR is the granularity of the shaper: a smaller Bc means smoother output but more timer work.

<figure>
<svg viewBox="0 0 480 100" width="480">
  <text class="sm" x="10" y="12">drop probability</text>
  <line class="lg" x1="40" y1="20" x2="40" y2="84"/><line class="lg" x1="40" y1="84" x2="460" y2="84"/>
  <path class="ln" d="M40,84 L160,84 L300,40 L300,20 L460,20"/>
  <text class="sm" x="100" y="96" text-anchor="middle">no drops</text><text class="sm" x="230" y="96" text-anchor="middle">random early drops</text><text class="sm" x="380" y="96" text-anchor="middle">tail drop (full)</text>
  <line class="lg dash" x1="160" y1="30" x2="160" y2="84"/><text class="sm" x="164" y="32">minimum threshold</text>
  <line class="lg dash" x1="300" y1="50" x2="300" y2="84"/><text class="sm" x="304" y="58">maximum threshold</text>
  <text class="sm" x="44" y="38">1 / mark-probability denominator at the maximum</text>
  <text class="sm" x="10" y="12" dx="0"></text>
</svg>
<figcaption><b>Figure 4.38</b> The WRED curve. Higher drop-precedence classes (AF13 against AF11) use lower thresholds, so they are dropped first.</figcaption>
</figure>

::: example
**Three QoS calculations.**

1. *DSCP decode.* ToS 0xB8 = 1011 1000. The top six bits are 101110 = 46 = EF. AF31 has class 3 and drop precedence 1: 8 × 3 + 2 × 1 = 26.
2. *Shaper.* CIR 10 Mb/s with Bc 100,000 bits gives Tc = 100,000 / 10,000,000 = 10 ms, so up to 100 kb may be sent each 10 ms.
3. *Branch WAN policy.* On a 10 Mb/s link: voice 10% priority, video 30%, business-critical 25%, scavenger 1%, the rest default. The reserved sum is 66%, below the default 75% reservation limit, so the policy is accepted.

```
class-map match-all VOICE
 match dscp ef
! VIDEO (af41), CRIT (af31) and SCAV (cs1) are defined in the same way
policy-map WAN-CHILD
 class VOICE
  priority percent 10
 class VIDEO
  bandwidth percent 30
 class CRIT
  bandwidth percent 25
 class SCAV
  bandwidth percent 1
 class class-default
  fair-queue
policy-map WAN-PARENT
 class class-default
  shape average 10000000
  service-policy WAN-CHILD
interface GigabitEthernet0/1
 service-policy output WAN-PARENT
```

[Result: the parent shaper makes the Ethernet port behave as a 10 Mb/s link, so the child queues engage; `show policy-map interface Gi0/1` shows per-class packets and drops.]{.result}
:::

::: trap
*Claim:* a policer and a shaper are two names for rate limiting. *Why it is wrong:* the policer has no queue, so excess traffic is dropped or re-marked at once; the shaper queues it. *Correct statement:* shape on egress toward a slower service, police to enforce a contract, and never police voice without understanding the consequences.
:::

::: lens
[CISCO · BROADCOM · NOKIA]{.co}

Policing against shaping and the DSCP decode are near-certain. Give the unit conversions without hesitation (ToS byte against DSCP, AFxy = 8x + 2y). Broadcom and Nokia candidates also draw the queue pipeline and say where the buffers and the drop decisions are in hardware.
:::

::: lab
`LAB 4.11 · 40 MIN`  GNS3 with IOSv and two Linux hosts. Apply the WAN-PARENT policy above to a 10 Mb/s link and mark traffic with iperf3.

```
host$ iperf3 -c 10.0.0.2 -u -b 8M -S 0xB8      ! EF-marked UDP, 8 Mb/s
host$ iperf3 -c 10.0.0.2 -b 50M                ! unmarked TCP
R1# show policy-map interface GigabitEthernet0/1
  Class-map: VOICE (match-all)    priority: 10% (1000 kbps)    drops 4120 <-- exceeds LLQ
```

**What you should notice:** the EF stream above 1 Mb/s is dropped by the implicit policer of LLQ; the TCP flow takes the rest. Try the same on Linux with `tc qdisc add dev eth0 root tbf rate 10mbit burst 32kbit latency 50ms` and compare the shaper with a policer (`tc filter ... police`).
:::

## [4.12]{.sec}IP multicast [Optional · ■■■]{.tag} {#s4-12}

::: bigidea
Multicast sends one copy of a stream towards many receivers and duplicates it only where paths diverge; receivers announce interest with IGMP, and routers build distribution trees with PIM, accepting packets only from the direction of the source.
:::

Unicast, broadcast and multicast differ in how many copies the network carries. A source sending a stream to ten receivers by unicast sends ten copies over its first link; by broadcast it would reach everyone, wanted or not; by multicast it sends one copy, and the network replicates it only at branch points. Hence video distribution, market-data feeds and routing protocols themselves use multicast.

IPv4 multicast addresses are 224.0.0.0/4. Within it, 224.0.0.0/24 is link-local (never routed; 224.0.0.5 and .6 are OSPF, .10 EIGRP, .13 PIM), 232.0.0.0/8 is source-specific multicast (SSM) and 239.0.0.0/8 is administratively scoped, the private multicast range. A group address maps to a MAC address by placing its low 23 bits after the prefix 01:00:5E; since a group has 28 variable bits, 32 groups share one MAC.

<figure>
<svg viewBox="0 0 480 110" width="480">
  <rect class="box" x="10" y="14" width="50" height="24"/><text class="lbl" x="35" y="30" text-anchor="middle">1110</text>
  <rect class="fill" x="60" y="14" width="90" height="24"/><text class="lbl" x="105" y="30" text-anchor="middle">5 bits: lost</text>
  <rect class="hl" x="150" y="14" width="300" height="24"/><text class="lbl" x="300" y="30" text-anchor="middle">23 bits: copied</text>
  <text class="sm" x="10" y="9">IPv4 group (32 bits)</text>
  <path class="acc" d="M150,38 L150,58 M450,38 L450,58"/>
  <rect class="box" x="10" y="62" width="100" height="24"/><text class="lbl" x="60" y="78" text-anchor="middle">01:00:5E</text>
  <rect class="fill" x="110" y="62" width="40" height="24"/><text class="lbl" x="130" y="78" text-anchor="middle">0</text>
  <rect class="hl" x="150" y="62" width="300" height="24"/><text class="lbl" x="300" y="78" text-anchor="middle">23 bits</text>
  <text class="sm" x="10" y="102">MAC (48 bits)</text>
</svg>
<figcaption><b>Figure 4.39</b> Multicast IP-to-MAC mapping. The five lost bits are why 32 groups collide.</figcaption>
</figure>

::: example
**MAC mapping and ambiguity.** Map 239.1.1.1, and find another group with the same MAC.

1. The low 23 bits of 239.1.1.1 are the last three octets with the top bit of the second octet dropped: 1 = 0000001, then 1, then 1. The MAC is 01:00:5E:01:01:01.
2. 224.129.1.1 has second octet 129 = 1000 0001. Dropping the top bit gives 0000001 = 1, so its MAC is also 01:00:5E:01:01:01.

[Result: 239.1.1.1 and 224.129.1.1 share a MAC; hosts filter again at IP, and 32 groups overlap by this rule.]{.result}
:::

<figure>
<svg viewBox="0 0 480 190" width="480">
  <text class="lbl" x="120" y="12" text-anchor="middle">1 Shared tree (*,G)</text><text class="lbl" x="360" y="12" text-anchor="middle">2 Shortest-path tree (S,G)</text>
  <circle class="hl" cx="120" cy="50" r="14"/><text class="sm" x="120" y="53" text-anchor="middle">RP</text>
  <rect class="box" x="20" y="100" width="40" height="22" rx="2"/><text class="sm" x="40" y="114" text-anchor="middle">Source</text>
  <circle class="box" cx="40" cy="150" r="10"/><text class="sm" x="40" y="153" text-anchor="middle">FHR</text>
  <circle class="box" cx="200" cy="100" r="10"/><text class="sm" x="200" y="103" text-anchor="middle">LHR</text>
  <rect class="box" x="180" y="150" width="50" height="22" rx="2"/><text class="sm" x="205" y="164" text-anchor="middle">Receiver</text>
  <line class="lg" x1="40" y1="122" x2="40" y2="140"/><line class="acc" x1="40" y1="140" x2="120" y2="64"/><line class="acc" x1="134" y1="54" x2="196" y2="92"/><line class="lg" x1="200" y1="110" x2="205" y2="150"/>
  <circle class="hl" cx="360" cy="50" r="14"/><text class="sm" x="360" y="53" text-anchor="middle">RP</text>
  <rect class="box" x="260" y="100" width="40" height="22" rx="2"/><text class="sm" x="280" y="114" text-anchor="middle">Source</text>
  <circle class="box" cx="280" cy="150" r="10"/><text class="sm" x="280" y="153" text-anchor="middle">FHR</text>
  <circle class="box" cx="440" cy="100" r="10"/><text class="sm" x="440" y="103" text-anchor="middle">LHR</text>
  <rect class="box" x="420" y="150" width="50" height="22" rx="2"/><text class="sm" x="445" y="164" text-anchor="middle">Receiver</text>
  <line class="lg" x1="280" y1="122" x2="280" y2="140"/><line class="lg dash" x1="280" y1="140" x2="360" y2="64"/><line class="lg dash" x1="374" y1="54" x2="436" y2="92"/>
  <line class="acc" x1="290" y1="150" x2="430" y2="108"/><line class="lg" x1="440" y1="110" x2="445" y2="150"/>
  <text class="sm" x="10" y="186">1: traffic goes via the RP. 2: the last-hop router (LHR) joins the source directly (accent); the RP-side path is pruned (dashed).</text>
</svg>
<figcaption><b>Figure 4.40</b> PIM sparse mode: shared tree, then switchover to the shortest-path tree. FHR = first-hop router.</figcaption>
</figure>

| Mechanism | Purpose | Notes |
|---|---|---|
| IGMPv2 | host to router group membership | report to the group; leave to 224.0.0.2; querier election |
| IGMPv3 | adds source filtering | reports to 224.0.0.22; required for SSM |
| IGMP snooping | switch limits flooding to joined ports | requires a querier in the VLAN |
| PIM-DM | flood and prune | small networks only |
| PIM-SM | RP and shared tree, then SPT | the common mode; RP by static, Auto-RP, BSR |
| PIM-SSM | (S,G) from the start, 232/8 | no RP, needs IGMPv3 |
| Bidir-PIM | (\*,G) only, traffic both ways | many-to-many applications |
| MSDP | shares sources between RPs | inter-domain; mostly replaced by anycast RP |

Hosts join a group with *IGMP*: v2 uses general queries (to 224.0.0.1), reports sent to the group address and Leave messages (to 224.0.0.2); v3 adds source filtering and is what SSM needs. A switch that does *IGMP snooping* forwards a group only to ports that joined. Between routers, *PIM* in *dense mode* floods and prunes. *PIM sparse mode* (PIM-SM, the standard) uses a *rendezvous point* (RP). A receiver's last-hop router sends a (\*,G) join towards the RP, building a shared tree; the source's first-hop router registers with the RP; once traffic flows, the last-hop router switches to a source-rooted shortest-path tree (S,G) and the RP prunes itself off. The RP is found by static configuration, Auto-RP or BSR. Every multicast packet is subject to the *RPF check*: it is accepted only if it arrives on the interface that unicast routing would use to reach the source, which prevents loops. If unicast routing is asymmetric, the RPF interface may differ from the interface the stream uses, and the stream is dropped until a static multicast route corrects it. Bidirectional PIM suits many-to-many traffic, and MSDP connects RPs between domains.

```
R1(config)# ip multicast-routing
R1(config)# ip pim rp-address 10.255.0.1
R1(config-if)# ip pim sparse-mode
R1# show ip mroute 239.1.1.1
(*, 239.1.1.1), 00:03:12/00:02:48, RP 10.255.0.1, flags: S
(10.2.2.5, 239.1.1.1), 00:01:07/00:02:53, flags: T    <-- T: SPT switchover
```

::: lab
`LAB 4.12 · 35 MIN`  GNS3 with IOSv: PIM-SM with a static RP on the middle router, a source and a receiver on each side.

```
R2# show ip igmp groups
239.1.1.1   GigabitEthernet0/1   00:02:10   00:02:49   10.2.2.9      <-- the receiver's join
R2# show ip mroute 239.1.1.1 count
Group: 239.1.1.1, Source count: 1, Packets forwarded: 5420, Packets received: 5420
```

**What you should notice:** at first the flag is S (sparse, shared tree) and later T (SPT); break the reverse path with a static route to the source via the wrong interface and `show ip mroute count` reports RPF drops.
:::

::: check
1. Why does a multicast packet fail the RPF check? [^c4-15]
:::

[^c4-15]: It arrived on an interface that the unicast routing table would not use to reach the source.

## [4.13]{.sec}IP services and access lists on IOS [Must · ■■□]{.tag} {#s4-13}

::: bigidea
A router supplies the services a network depends on (address translation, addressing, time, monitoring, logging) and filters packets with access lists, which are read from the top and stop at the first match.
:::

*Address translation.* The theory of NAT and PAT is in [§3.6](#s3-6){.ref}; here is the IOS form. Interfaces are marked inside or outside, an ACL selects the inside addresses, and `overload` turns NAT into PAT by multiplexing on port numbers.

```
interface GigabitEthernet0/0.10
 ip nat inside
interface GigabitEthernet0/1
 ip nat outside
access-list 1 permit 192.168.10.0 0.0.0.255
ip nat inside source list 1 interface GigabitEthernet0/1 overload
ip nat inside source static 192.168.10.80 198.51.100.80      ! one-to-one for a server
```

```
BR1# show ip nat translations
Pro Inside global        Inside local       Outside local      Outside global
tcp 192.0.2.2:1025       192.168.10.5:49152 203.0.113.10:443   203.0.113.10:443
```

*DHCP.* A router can be a server. A host broadcast does not cross a router, so a router on the client's subnet can *relay* it as a unicast to the real server with `ip helper-address`, filling in the `giaddr` field so that the server chooses the right pool. The helper also forwards some other UDP broadcasts (TFTP, DNS, TACACS, time, NetBIOS) by default.

```
ip dhcp excluded-address 192.168.10.1 192.168.10.20
ip dhcp pool SALES
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 dns-server 10.0.0.53
interface GigabitEthernet0/0.20
 ip helper-address 10.0.0.5          ! relay to a central server
```

*NTP* keeps clocks aligned, which makes logs comparable. A server is given a *stratum*, its distance from a reference clock: stratum 1 has the clock attached, each hop adds one, and 16 means unsynchronised. NTP uses UDP 123. *Syslog* (UDP 514) sends log messages to a server, each with a severity from 0 to 7. *SNMP* (UDP 161 for polling, 162 for traps) lets a manager read and set device variables. Version 2c authenticates by a clear-text community string; version 3 adds authentication and encryption (`authPriv`) and should be used.

```
ntp server 10.0.0.5
ntp authentication-key 1 md5 N7pKey
ntp authenticate
ntp trusted-key 1
logging host 10.0.0.6
logging trap warnings
service timestamps log datetime msec
snmp-server group NMS v3 priv
snmp-server user nms NMS v3 auth sha AuthPass priv aes 128 PrivPass
```

```
BR1# show ntp status
Clock is synchronized, stratum 3, reference is 10.0.0.5
```

| Level | Name | Level | Name |
|---|---|---|---|
| 0 | Emergency | 4 | Warning |
| 1 | Alert | 5 | Notice |
| 2 | Critical | 6 | Informational |
| 3 | Error | 7 | Debugging |

[**Mnemonic** — "Every Awesome Cisco Engineer Will Need Ice cream Daily": Emergency, Alert, Critical, Error, Warning, Notice, Informational, Debugging. `logging trap warnings` sends levels 0 to 4.]{.margin}*Access control lists.* The theory and placement of ACLs belong to [§9.5](#s9-5){.ref}; the IOS syntax is below. An ACL is a list of permit and deny lines examined top to bottom; the first match decides, and an invisible `deny ip any any` ends every list. Standard ACLs (1 to 99) match the source address only and are applied close to the destination; extended ACLs (100 to 199) match protocol, source, destination and ports and are applied close to the source. Named ACLs allow sequence numbers, so that lines can be inserted. Masks are *wildcards*: a 0 bit must match, a 1 bit is ignored, so the wildcard is the inverted subnet mask. IPv6 ACLs end with implicit permits for neighbour discovery before the final deny.

::: example
**An ACL that protects a server.** Only SALES (192.168.10.0/24) may reach the web server 10.0.0.80 on TCP 443; other networks must not reach it at all.

1. Place it as close as possible to the destination for a *single* protected host, as an outbound ACL on R1's server-facing port; alternatively, place an extended ACL inbound on each user-facing interface so that denied packets are discarded at the first router.
2. Permit the allowed flow, deny everything else addressed to the server, and permit the rest.
3. Return traffic needs nothing here, since an outbound ACL on the server's port inspects only packets *toward* the server. If the ACL were applied inbound on the server port (filtering replies), add `permit tcp host 10.0.0.80 eq 443 192.168.10.0 0.0.0.255 established`.

```
ip access-list extended TO-WEB
 10 permit tcp 192.168.10.0 0.0.0.255 host 10.0.0.80 eq 443
 20 deny   ip any host 10.0.0.80 log
 30 permit ip any any
interface GigabitEthernet0/2
 ip access-group TO-WEB out
```

```
R1# show ip access-lists TO-WEB
    10 permit tcp 192.168.10.0 0.0.0.255 host 10.0.0.80 eq 443 (153 matches)
    20 deny ip any host 10.0.0.80 log (7 matches)
```

[Result: line 10 matches the permitted flow, line 20 catches everything else for the server, and line 30 stops the implicit deny from blocking unrelated traffic.]{.result}
:::

::: example
**A wildcard mask.** Match hosts 192.168.1.16 to 192.168.1.31. The block holds 16 addresses starting at a multiple of 16, so the mask is 16 - 1 = 15 in the last octet: `192.168.1.16 0.0.0.15`. Quick rule: wildcard = 255 minus the subnet-mask octet, so /24 is 0.0.0.255 and a single host is `0.0.0.0` (written `host x`).
:::

::: trap
*Claim:* an ACL with only `deny` lines blocks those packets and passes the rest. *Why it is wrong:* every ACL ends in an implicit `deny any`, so a list of denies blocks everything. *Correct statement:* finish with `permit ip any any` when the intent is to filter selected traffic only.
:::

::: lens
[CISCO · AMAZON · MICROSOFT]{.co}

Expected at Cisco as a configuration or "what is wrong with this ACL" exercise (order of lines, implicit deny, direction on the interface, wildcard arithmetic). Be able to write the NAT overload line, a DHCP relay and an SNMPv3 user from memory, and to name the verification command for each.
:::

Address translation and filtering are most often debugged with a short routine, which is worth memorising.

| Symptom | First check | Likely cause |
|---|---|---|
| Inside hosts cannot reach the Internet | `show ip nat translations`, `show ip nat statistics` | no `ip nat inside` or `outside` marking; ACL does not match the inside subnet |
| Some translations fail, then all | `show ip nat statistics` (misses, pool exhaustion) | too few ports or addresses; missing `overload` |
| Server unreachable from outside | `show ip nat translations` | no static entry, or ACL blocks the *inside local* address |
| DHCP clients get no address | `debug ip dhcp server packet` | missing `ip helper-address`; pool exhausted; wrong `giaddr` subnet |
| ACL seems ignored | `show ip access-lists`, `show ip interface Gi0/2 \| include access list` | applied in the wrong direction or on the wrong interface; line order |
| Clock drifts, logs disagree | `show ntp associations` | NTP unreachable; wrong key; stratum too high |

::: lab
`LAB 4.13 · 45 MIN`  Packet Tracer, integrated: PAT at BR1, a DHCP pool and relay, an NTP server, syslog and an SSH-only vty line, then TO-WEB.

```
BR1(config)# access-list 10 permit 10.0.0.0 0.0.0.255
BR1(config)# line vty 0 4
BR1(config-line)# access-class 10 in
```

**What you should notice:** `show ip nat translations` fills as hosts browse; a Telnet attempt from outside the admin subnet is refused; the match counters of TO-WEB rise on the permit line only for SALES.
:::

::: check
1. What does `ip nat inside source list 1 interface Gi0/1 overload` do? [^c4-12]
2. A standard ACL is applied near the source and blocks too much. Why? [^c4-13]
:::

[^c4-12]: It translates addresses matched by ACL 1 to the address of Gi0/1, using port numbers to distinguish hosts (PAT).
[^c4-13]: A standard ACL sees only the source address, so near the source it blocks that source's traffic to every destination.

## [4.14]{.sec}Tunnels and enterprise architecture [Optional · ■■□]{.tag} {#s4-14}

::: bigidea
A tunnel wraps a packet inside another to cross a network that would not otherwise carry it, at the price of a header and a smaller usable MTU.
:::

*GRE* (IP protocol 47) adds a 4-byte header and a new 20-byte IP header, 24 bytes in all, so a 1500-byte link leaves 1476 for the inner packet. GRE does not encrypt; IPsec does ([§9.7](#s9-7){.ref}), and GRE over IPsec is the standard way to carry routing protocols securely. DMVPN adds dynamic spoke-to-spoke tunnels.

<figure>
<svg viewBox="0 0 480 60" width="480">
  <rect class="box" x="10" y="12" width="110" height="26"/><text class="lbl" x="65" y="29" text-anchor="middle">Outer IP 20 bytes</text>
  <rect class="hl" x="120" y="12" width="70" height="26"/><text class="lbl" x="155" y="29" text-anchor="middle">GRE 4</text>
  <rect class="box" x="190" y="12" width="110" height="26"/><text class="lbl" x="245" y="29" text-anchor="middle">Inner IP 20</text>
  <rect class="fill" x="300" y="12" width="170" height="26"/><text class="lbl" x="385" y="29" text-anchor="middle">Payload up to 1456 bytes</text>
  <text class="sm" x="10" y="54">Outer IP protocol = 47. Inner packet limit 1476 bytes on a 1500-byte link.</text>
</svg>
<figcaption><b>Figure 4.41</b> GRE encapsulation.</figcaption>
</figure>

::: example
**GRE with OSPF, and the recursive-routing fault.** HQ-R (203.0.113.1) and Branch-R (198.51.100.1) are joined by a tunnel on 172.31.0.0/30, with OSPF running over it.

```
interface Tunnel0
 ip address 172.31.0.1 255.255.255.252
 tunnel source 203.0.113.1
 tunnel destination 198.51.100.1
 ip mtu 1476
 ip tcp adjust-mss 1436
router ospf 1
 network 172.31.0.0 0.0.0.3 area 0
```

1. The tunnel destination 198.51.100.1 must be reachable over the *underlay* (the real ISP path).
2. If OSPF learns 198.51.100.0/24 *through the tunnel itself*, the router tries to reach the tunnel endpoint through the tunnel. The tunnel then collapses and flaps:

```
%TUN-5-RECURDOWN: Tunnel0 temporarily disabled due to recursive routing
%LINEPROTO-5-UPDOWN: Line protocol on Interface Tunnel0, changed state to down
```

[Result: keep the underlay route to the tunnel destination more specific or of lower AD than anything learnt via the tunnel, for example by running OSPF over the tunnel in a separate process and filtering the underlay prefixes.]{.result}
:::

Failure detection beyond link state uses *BFD* (millisecond hellos) and *IP SLA* probes that feed a *track* object, for example a floating default route that is withdrawn when a probe to the ISP's gateway fails, not only when the link drops:

```
ip sla 1
 icmp-echo 192.0.2.1 source-interface GigabitEthernet0/1
 frequency 5
ip sla schedule 1 life forever start-time now
track 1 ip sla 1 reachability
ip route 0.0.0.0 0.0.0.0 192.0.2.1 track 1
```

<figure>
<svg viewBox="0 0 480 170" width="480">
  <text class="lbl" x="110" y="12" text-anchor="middle">Three-tier campus</text><text class="lbl" x="370" y="12" text-anchor="middle">Spine-leaf (see Pillar 5)</text>
  <rect class="box" x="60" y="22" width="100" height="22" rx="2"/><text class="lbl" x="110" y="37" text-anchor="middle">Core</text>
  <rect class="box" x="20" y="72" width="80" height="22" rx="2"/><text class="lbl" x="60" y="87" text-anchor="middle">Distribution</text>
  <rect class="box" x="120" y="72" width="80" height="22" rx="2"/><text class="lbl" x="160" y="87" text-anchor="middle">Distribution</text>
  <rect class="box" x="10" y="124" width="55" height="22" rx="2"/><text class="lbl" x="37" y="139" text-anchor="middle">Access</text>
  <rect class="box" x="80" y="124" width="55" height="22" rx="2"/><text class="lbl" x="107" y="139" text-anchor="middle">Access</text>
  <rect class="box" x="150" y="124" width="55" height="22" rx="2"/><text class="lbl" x="177" y="139" text-anchor="middle">Access</text>
  <line class="lg" x1="90" y1="44" x2="60" y2="72"/><line class="lg" x1="130" y1="44" x2="160" y2="72"/><line class="lg" x1="100" y1="83" x2="120" y2="83"/>
  <line class="lg" x1="50" y1="94" x2="37" y2="124"/><line class="lg" x1="70" y1="94" x2="107" y2="124"/><line class="lg" x1="150" y1="94" x2="107" y2="124"/><line class="lg" x1="170" y1="94" x2="177" y2="124"/>
  <rect class="box" x="290" y="28" width="70" height="22" rx="2"/><text class="lbl" x="325" y="43" text-anchor="middle">Spine 1</text>
  <rect class="box" x="390" y="28" width="70" height="22" rx="2"/><text class="lbl" x="425" y="43" text-anchor="middle">Spine 2</text>
  <rect class="box" x="270" y="110" width="50" height="22" rx="2"/><text class="lbl" x="295" y="125" text-anchor="middle">Leaf</text>
  <rect class="box" x="335" y="110" width="50" height="22" rx="2"/><text class="lbl" x="360" y="125" text-anchor="middle">Leaf</text>
  <rect class="box" x="400" y="110" width="50" height="22" rx="2"/><text class="lbl" x="425" y="125" text-anchor="middle">Leaf</text>
  <g class="lg"><line class="lg" x1="325" y1="50" x2="295" y2="110"/><line class="lg" x1="325" y1="50" x2="360" y2="110"/><line class="lg" x1="325" y1="50" x2="425" y2="110"/><line class="lg" x1="425" y1="50" x2="295" y2="110"/><line class="lg" x1="425" y1="50" x2="360" y2="110"/><line class="lg" x1="425" y1="50" x2="425" y2="110"/></g>
  <text class="sm" x="10" y="164">North-south traffic dominates; STP or routing at the distribution layer. Every leaf reaches every other leaf in two hops with equal-cost paths.</text>
</svg>
<figcaption><b>Figure 4.42</b> The two shapes. The campus hierarchy suits hosts that talk to services outside; the fabric suits servers that talk to each other.</figcaption>
</figure>

<figure>
<svg viewBox="0 0 480 150" width="480">
  <rect class="box" x="150" y="10" width="180" height="30" rx="2"/><text class="lbl" x="240" y="29" text-anchor="middle">Orchestration and management</text>
  <rect class="box" x="30" y="60" width="120" height="26" rx="2"/><text class="lbl" x="90" y="77" text-anchor="middle">Controller (policy, routes)</text>
  <rect class="box" x="330" y="60" width="120" height="26" rx="2"/><text class="lbl" x="390" y="77" text-anchor="middle">Authenticator (admission)</text>
  <rect class="fill" x="20" y="118" width="70" height="24" rx="2"/><text class="lbl" x="55" y="134" text-anchor="middle">Edge router</text>
  <rect class="fill" x="130" y="118" width="70" height="24" rx="2"/><text class="lbl" x="165" y="134" text-anchor="middle">Edge router</text>
  <rect class="fill" x="280" y="118" width="70" height="24" rx="2"/><text class="lbl" x="315" y="134" text-anchor="middle">Edge router</text>
  <rect class="fill" x="390" y="118" width="70" height="24" rx="2"/><text class="lbl" x="425" y="134" text-anchor="middle">Edge router</text>
  <line class="lg" x1="210" y1="40" x2="90" y2="60"/><line class="lg" x1="270" y1="40" x2="390" y2="60"/>
  <line class="lg dash" x1="90" y1="86" x2="55" y2="118"/><line class="lg dash" x1="90" y1="86" x2="165" y2="118"/><line class="lg dash" x1="390" y1="86" x2="315" y2="118"/><line class="lg dash" x1="390" y1="86" x2="425" y2="118"/>
  <path class="acc" d="M90,130 L130,130 M200,130 L280,130 M350,130 L390,130"/>
  <text class="sm" x="215" y="112" text-anchor="middle">data plane: encrypted overlay tunnels over any transport</text>
</svg>
<figcaption><b>Figure 4.43</b> The SD-WAN idea: a central control plane (dashed) programs edge devices, which build the data-plane overlay (accent) between themselves.</figcaption>
</figure>

Enterprise designs have two common shapes. A *three-tier campus* has access, distribution and core layers: access switches terminate hosts (PortFast, BPDU Guard), distribution pairs run the inter-VLAN routing and FHRP, and the core carries traffic between them. A *two-tier (collapsed-core)* design merges the last two; a *spine-leaf* fabric (see [§5.1](#s5-1){.ref}) replaces both in data centres. *SD-WAN* (for example Cisco's vManage, vSmart, vBond and edge routers) separates a central control plane and orchestration from the edge forwarding devices and builds overlay tunnels over any transport. *SD-Access* builds a campus *fabric* with a LISP control plane and a VXLAN data plane. These overlays are taught in [§5.5](#s5-5){.ref}; the point here is that they rest on the routing and tunnelling in this chapter.

::: check
1. What MTU should the GRE tunnel use over a 1500-byte link, and why? [^c4-14]
:::

[^c4-14]: 1476, because the 24-byte GRE overhead (20 outer IP, 4 GRE) is subtracted.

:::
