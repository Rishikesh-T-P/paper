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
<figcaption><b>Figure 4.18</b> The ToS byte. Assured Forwarding classes AF1 to AF4 each have three drop precedences.</figcaption>
</figure>

| PHB | DSCP | Typical use |
|---|---|---|
| EF | 46 | voice |
| AF41 / AF31 / AF21 / AF11 | 34 / 26 / 18 / 10 | video, critical data, transactional, bulk |
| CS6 / CS3 | 48 / 24 | network control, signalling |
| CS1 | 8 | scavenger (below best effort) |
| default | 0 | best effort |

Queuing then orders the packets. *CBWFQ* gives each class a guaranteed share of bandwidth; *LLQ* adds a strict-priority queue for voice, which has an implicit policer so that it cannot starve the other classes. *WRED* drops packets early and randomly as a queue fills, with a rising probability between a minimum and a maximum threshold, and with higher drop probability for higher drop-precedence markings; it prevents *global synchronisation*, in which tail drop makes all TCP flows back off together. *Policing* and *shaping* both use a token bucket (fills at the committed rate, CIR; capacity is the burst size Bc): a policer discards or re-marks packets that find no tokens, while a shaper delays them in a buffer. Shaping thus adds delay but loses less; policing adds none but TCP sees loss and its window oscillates. A shaper's time interval is Tc = Bc / CIR.

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

## [4.12]{.sec}IP multicast [Optional · ■■■]{.tag} {#s4-12}

::: bigidea
Multicast sends one copy of a stream towards many receivers and duplicates it only where paths diverge; receivers announce interest with IGMP, and routers build distribution trees with PIM, accepting packets only from the direction of the source.
:::

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
<figcaption><b>Figure 4.19</b> Multicast IP-to-MAC mapping. The five lost bits are why 32 groups collide.</figcaption>
</figure>

::: example
**MAC mapping and ambiguity.** Map 239.1.1.1, and find another group with the same MAC.

1. The low 23 bits of 239.1.1.1 are the last three octets with the top bit of the second octet dropped: 1 = 0000001, then 1, then 1. The MAC is 01:00:5E:01:01:01.
2. 224.129.1.1 has second octet 129 = 1000 0001. Dropping the top bit gives 0000001 = 1, so its MAC is also 01:00:5E:01:01:01.

[Result: 239.1.1.1 and 224.129.1.1 share a MAC; hosts filter again at IP, and 32 groups overlap by this rule.]{.result}
:::

Hosts join a group with *IGMP*: v2 uses general queries (to 224.0.0.1), reports sent to the group address and Leave messages (to 224.0.0.2); v3 adds source filtering and is what SSM needs. A switch that does *IGMP snooping* forwards a group only to ports that joined. Between routers, *PIM* in *dense mode* floods and prunes. *PIM sparse mode* (PIM-SM, the standard) uses a *rendezvous point* (RP). A receiver's last-hop router sends a (\*,G) join towards the RP, building a shared tree; the source's first-hop router registers with the RP; once traffic flows, the last-hop router switches to a source-rooted shortest-path tree (S,G) and the RP prunes itself off. The RP is found by static configuration, Auto-RP or BSR. Every multicast packet is subject to the *RPF check*: it is accepted only if it arrives on the interface that unicast routing would use to reach the source, which prevents loops. If unicast routing is asymmetric, the RPF interface may differ from the interface the stream uses, and the stream is dropped until a static multicast route corrects it. Bidirectional PIM suits many-to-many traffic, and MSDP connects RPs between domains.

```
R1(config)# ip multicast-routing
R1(config)# ip pim rp-address 10.255.0.1
R1(config-if)# ip pim sparse-mode
R1# show ip mroute 239.1.1.1
(*, 239.1.1.1), 00:03:12/00:02:48, RP 10.255.0.1, flags: S
(10.2.2.5, 239.1.1.1), 00:01:07/00:02:53, flags: T    <-- T: SPT switchover
```

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
<figcaption><b>Figure 4.20</b> GRE encapsulation.</figcaption>
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

Enterprise designs have two common shapes. A *three-tier campus* has access, distribution and core layers: access switches terminate hosts (PortFast, BPDU Guard), distribution pairs run the inter-VLAN routing and FHRP, and the core carries traffic between them. A *two-tier (collapsed-core)* design merges the last two; a *spine-leaf* fabric (see [§5.1](#s5-1){.ref}) replaces both in data centres. *SD-WAN* (for example Cisco's vManage, vSmart, vBond and edge routers) separates a central control plane and orchestration from the edge forwarding devices and builds overlay tunnels over any transport. *SD-Access* builds a campus *fabric* with a LISP control plane and a VXLAN data plane. These overlays are taught in [§5.5](#s5-5){.ref}; the point here is that they rest on the routing and tunnelling in this chapter.

::: check
1. What MTU should the GRE tunnel use over a 1500-byte link, and why? [^c4-14]
:::

[^c4-14]: 1476, because the 24-byte GRE overhead (20 outer IP, 4 GRE) is subtracted.

:::
