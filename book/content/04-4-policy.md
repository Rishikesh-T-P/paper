::: {.p4}

## [4.8]{.sec}First-hop redundancy: HSRP, VRRP and GLBP [Should · ■■□]{.tag} {#s4-8}

::: bigidea
A host has one default gateway address, so two routers share a *virtual* IP address and MAC address, and whichever is active answers for it; when it fails the other takes over and the hosts notice nothing.
:::

In *HSRP* (Cisco's Hot Standby Router Protocol) one router is *Active* and forwards for the virtual IP, another is *Standby*, and the rest *Listen*. Routers exchange hellos every 3 s (hold time 10 s) and the highest priority (default 100) becomes active. HSRP *preemption* is **off** by default, so a recovered higher-priority router does not take back the role unless `standby preempt` is configured. *VRRP* (RFC 5798) is the open standard, with a *master* and *backups*; its preemption is **on** by default, and a router that owns the virtual IP as its real address has priority 255. *GLBP* adds load balancing: one *active virtual gateway* hands out different virtual MACs, and up to four *active virtual forwarders* each carry part of the load.

| | HSRP v1 | HSRP v2 | VRRP v2/v3 | GLBP |
|---|---|---|---|---|
| Standard | Cisco | Cisco | IETF | Cisco |
| Transport and group address | UDP 1985, 224.0.0.2 | UDP 1985, 224.0.0.102 | IP protocol 112, 224.0.0.18 | UDP 3222, 224.0.0.102 |
| Virtual MAC | 0000.0c07.acXX | 0000.0c9f.fXXX | 0000.5e00.01XX | 0007.b400.XXYY |
| Default priority / preempt | 100 / off | 100 / off | 100 / on | 100 / off |
| Load sharing | per group | per group | per group | per host (several forwarders) |

<figure>
<svg viewBox="0 0 480 170" width="480">
  <circle class="box" cx="110" cy="36" r="16"/><path class="ln" d="M102,28 L118,44 M118,28 L102,44"/><text class="lbl" x="110" y="68" text-anchor="middle">R1 active (110)</text>
  <circle class="box" cx="370" cy="36" r="16"/><path class="ln" d="M362,28 L378,44 M378,28 L362,44"/><text class="lbl" x="370" y="68" text-anchor="middle">R2 standby (100)</text>
  <rect class="hl" x="180" y="22" width="120" height="28" rx="2"/><rect class="acc" x="180" y="22" width="120" height="28" rx="2"/><text class="lbl" x="240" y="34" text-anchor="middle">VIP 192.168.1.254</text><text class="sm" x="240" y="45" text-anchor="middle">VMAC 0000.0c9f.f001</text>
  <rect class="box" x="195" y="104" width="90" height="26" rx="2"/><text class="lbl" x="240" y="121" text-anchor="middle">SW1</text>
  <rect class="box" x="205" y="146" width="70" height="20" rx="2"/><text class="lbl" x="240" y="160" text-anchor="middle">Host</text>
  <line class="lg" x1="122" y1="48" x2="205" y2="104"/><line class="lg" x1="358" y1="48" x2="275" y2="104"/><line class="lg" x1="240" y1="130" x2="240" y2="146"/>
  <text class="sm" x="10" y="150">default gateway = VIP</text>
  <text class="sm" x="330" y="140">after failure: R2 becomes active,</text><text class="sm" x="330" y="150">sends a gratuitous ARP</text>
</svg>
<figcaption><b>Figure 4.27</b> First-hop redundancy. Both routers know the VIP; only the active one answers ARP for it with the virtual MAC.</figcaption>
</figure>

HSRP routers move through states: *Initial* (starting), *Learn* (waiting to learn the virtual IP from the active router), *Listen* (knows the virtual IP, hears hellos, is neither active nor standby), *Speak* (takes part in the election, sending hellos), *Standby* (next in line) and *Active*. The router that becomes active sends a gratuitous ARP and, since the virtual MAC is learnt by the switches from the HSRP hellos themselves, forwarding resumes at once. Failure of the active router is detected after the hold time (10 s by default), and a recoverable improvement is to shorten hello and hold (`standby 1 timers msec 200 msec 750`) or to use BFD.

::: example
**HSRP with interface tracking.** R1 has priority 110 and tracks its uplink Gi0/1 with a decrement of 20; R2 has priority 100. Both use `preempt`. The VIP is 192.168.1.254.

```
R1(config-if)# standby version 2
R1(config-if)# standby 1 ip 192.168.1.254
R1(config-if)# standby 1 priority 110
R1(config-if)# standby 1 preempt
R1(config-if)# standby 1 track GigabitEthernet0/1 20
```

1. Normal state: R1 is active with priority 110.
2. R1's uplink fails. The tracking decrement lowers R1 to 110 - 20 = 90, which is below R2's 100. Because R2 has `preempt`, it takes over.
3. The uplink returns. R1 climbs back to 110 and, with `preempt`, takes the role again.

```
R1# show standby brief
Interface   Grp  Pri P State   Active    Standby      Virtual IP
Gi0/0       1    90  P Standby 192.168.1.3 local      192.168.1.254   <-- after failure
```

[Result: tracking changes priority only; the standby takes over only if it has `preempt`. A decrement smaller than the priority gap (here less than 10) would not cause a switch.]{.result}
:::

<figure>
<svg viewBox="0 0 480 150" width="480">
  <line class="ln" x1="40" y1="20" x2="40" y2="120"/><line class="ln" x1="40" y1="120" x2="460" y2="120"/>
  <text class="sm" x="6" y="30">priority</text><text class="sm" x="20" y="48">110</text><text class="sm" x="20" y="82">100</text><text class="sm" x="26" y="100">90</text><text class="sm" x="440" y="134">time</text>
  <line class="lg dash" x1="40" y1="78" x2="460" y2="78"/>
  <path class="acc" d="M40,44 L190,44 L190,98 L330,98 L330,44 L460,44"/><text class="sm" x="48" y="40">R1</text>
  <path class="ln" d="M40,80 L460,80"/><text class="sm" x="48" y="92">R2 (100, preempt)</text>
  <line class="lg" x1="190" y1="20" x2="190" y2="120"/><text class="sm" x="194" y="30">uplink fails: R1 = 90, R2 active</text>
  <line class="lg" x1="330" y1="20" x2="330" y2="120"/><text class="sm" x="334" y="30">uplink back: R1 = 110, preempts</text>
</svg>
<figcaption><b>Figure 4.28</b> Priority against time for the tracking example. The roles swap when the lines cross, provided the lower-priority router has preempt enabled.</figcaption>
</figure>

*VRRP* and *GLBP* are configured in the same way. The VRRP version on IOS-XE and on FRR/Linux (`vrrpd`) uses the group, priority and address; if the router's real interface address equals the virtual address it becomes the owner with priority 255. GLBP distributes different virtual MACs to different hosts, so both routers forward.

```
! VRRP (IOS-XE)                          ! GLBP
interface GigabitEthernet0/0             interface GigabitEthernet0/0
 vrrp 1 ip 192.168.1.254                  glbp 1 ip 192.168.1.254
 vrrp 1 priority 110                      glbp 1 priority 110
 vrrp 1 track 1 decrement 20              glbp 1 preempt
```

Align the Layer 2 and Layer 3 roles: make the HSRP active router also the spanning-tree root for the VLAN, so that traffic does not cross the inter-switch link to reach it. On failover the new active router sends a gratuitous ARP so that switches relearn the virtual MAC.

::: lab
`LAB 4.8 · 20 MIN`  Packet Tracer, two routers and a host, HSRPv2 with tracking as in the example. Start a continuous ping and shut R1's uplink.

```
C:\> ping -t 192.168.1.254
Request timed out.   <-- count the lost packets
R2# show standby brief
Gi0/0   1  100 P Active   local   192.168.1.2   192.168.1.254
```

**What you should notice:** with default timers up to ten seconds of loss when R1 is *disconnected*, but only a few pings when tracking lowers the priority and R2 has preempt, because the standby no longer waits for the hold timer. Convert to VRRP and compare the lost-ping counts.
:::

::: check
1. R1 loses its uplink but stays active. Name two causes. [^c4-11]
:::

[^c4-11]: The tracking decrement is too small to drop below the standby's priority, or R2 lacks `preempt` (or the track object is not applied).

## [4.9]{.sec}Route control: prefix lists, route maps, redistribution and VRF-lite [Should · ■■□]{.tag} {#s4-9}

::: bigidea
Policy tools decide which routes are accepted, which are modified and which packets are steered; redistribution joins routing domains but, without tagging, joins them into a loop.
:::

A *prefix list* matches prefixes by address and length. `ip prefix-list X permit 10.0.0.0/8 ge 16 le 24` matches any prefix inside 10.0.0.0/8 whose length is between 16 and 24. Thus 10.0.0.0/8 does not match (length 8 is below 16), 10.1.0.0/16 and 10.1.1.0/24 match, and 10.1.1.0/25 does not (length 25 is above 24). With no `ge` or `le` only the exact prefix matches. Lists end with an implicit deny.

<figure>
<svg viewBox="0 0 480 150" width="480">
  <defs><marker id="m49" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="#1A1D23"/></marker></defs>
  <text class="sm" x="10" y="14">route in</text>
  <line class="ln" x1="50" y1="12" x2="70" y2="12" marker-end="url(#m49)"/>
  <rect class="box" x="72" y="2" width="110" height="26" rx="2"/><text class="lbl" x="127" y="14" text-anchor="middle">seq 10 match?</text><text class="sm" x="127" y="24" text-anchor="middle">prefix-list CUST</text>
  <line class="ln" x1="127" y1="28" x2="127" y2="62" marker-end="url(#m49)"/><text class="sm" x="132" y="50">yes</text>
  <rect class="hl" x="72" y="64" width="110" height="26" rx="2"/><text class="lbl" x="127" y="76" text-anchor="middle">set LOCAL_PREF 200</text><text class="sm" x="127" y="86" text-anchor="middle">then permit</text>
  <line class="ln" x1="182" y1="12" x2="250" y2="12" marker-end="url(#m49)"/><text class="sm" x="198" y="8">no</text>
  <rect class="box" x="252" y="2" width="110" height="26" rx="2"/><text class="lbl" x="307" y="14" text-anchor="middle">seq 20 match?</text><text class="sm" x="307" y="24" text-anchor="middle">(no match line: all)</text>
  <line class="ln" x1="307" y1="28" x2="307" y2="62" marker-end="url(#m49)"/><text class="sm" x="312" y="50">yes</text>
  <rect class="box" x="252" y="64" width="110" height="26" rx="2"/><text class="lbl" x="307" y="81" text-anchor="middle">permit unchanged</text>
  <line class="ln" x1="362" y1="12" x2="420" y2="12" marker-end="url(#m49)"/><text class="sm" x="372" y="8">no</text>
  <rect class="fill" x="422" y="2" width="52" height="26" rx="2"/><text class="lbl" x="448" y="19" text-anchor="middle">deny</text>
  <text class="sm" x="10" y="120">The first matching clause decides. If none matches, the implicit deny at the end rejects the route.</text>
  <text class="sm" x="10" y="132">A deny clause with a matching condition removes the route; a permit clause without match lines matches everything.</text>
</svg>
<figcaption><b>Figure 4.29</b> How a route map is evaluated. Clauses are tried in sequence-number order.</figcaption>
</figure>

A *route map* is an ordered list of numbered clauses, each with `match` conditions and `set` actions, and a `permit` or `deny`. The first clause that matches decides; if a permit clause has no match line it matches everything; at the end there is an implicit deny. Route maps are used for BGP policy, for redistribution and for policy-based routing.

```
ip prefix-list CUST seq 5 permit 10.0.0.0/8 ge 16 le 24
route-map SET-LP permit 10
 match ip address prefix-list CUST
 set local-preference 200
route-map SET-LP permit 20          ! no match: everything else passes unchanged
```

*Redistribution* imports routes of one protocol into another (`redistribute eigrp 100 subnets route-map X` under OSPF). The importing protocol needs a *seed metric*, since the foreign metric means nothing: OSPF assigns cost 20 by default (E2), EIGRP and RIP need explicit values. Done in one direction at one router it is safe. Done in both directions at two routers it is not: a route that enters OSPF from EIGRP at R1 can leave OSPF back into EIGRP at R2 with a better AD or metric, and so on, forming a loop. The fix is to *tag* routes as they are redistributed and to deny the tag in the reverse direction.

<figure>
<svg viewBox="0 0 480 150" width="480">
  <defs><marker id="a49" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="#21705A"/></marker></defs>
  <ellipse class="fill" cx="70" cy="75" rx="56" ry="40"/><text class="lbl" x="70" y="72" text-anchor="middle">OSPF</text><text class="sm" x="70" y="84" text-anchor="middle">domain</text>
  <ellipse class="fill" cx="410" cy="75" rx="56" ry="40"/><text class="lbl" x="410" y="72" text-anchor="middle">EIGRP</text><text class="sm" x="410" y="84" text-anchor="middle">domain</text>
  <circle class="box" cx="240" cy="30" r="14"/><path class="ln" d="M232,22 L248,38 M248,22 L232,38"/><text class="lbl" x="264" y="34">R1</text>
  <circle class="box" cx="240" cy="120" r="14"/><path class="ln" d="M232,112 L248,128 M248,112 L232,128"/><text class="lbl" x="264" y="124">R2</text>
  <path class="acc" d="M368,50 L256,30" marker-end="url(#a49)"/><path class="acc" d="M226,32 L108,52" marker-end="url(#a49)"/><path class="acc" d="M108,98 L226,118" marker-end="url(#a49)"/><path class="acc" d="M256,120 L368,100" marker-end="url(#a49)"/>
  <text class="sm" x="240" y="78" text-anchor="middle">route X circulates</text><text class="sm" x="240" y="88" text-anchor="middle">without a tag to stop it</text>
</svg>
<figcaption><b>Figure 4.30</b> Two-way redistribution at two points. A route learnt from EIGRP re-enters EIGRP through OSPF at the other router.</figcaption>
</figure>

```
route-map EIGRP-TO-OSPF deny 10
 match tag 110                     ! came from OSPF originally: do not send back
route-map EIGRP-TO-OSPF permit 20
 set tag 90
route-map OSPF-TO-EIGRP deny 10
 match tag 90
route-map OSPF-TO-EIGRP permit 20
 set tag 110
router ospf 1
 redistribute eigrp 100 subnets route-map EIGRP-TO-OSPF
router eigrp CAMPUS
 address-family ipv4 unicast autonomous-system 100
  topology base
   redistribute ospf 1 metric 100000 10 255 1 1500 route-map OSPF-TO-EIGRP
```

A seed metric is needed because the receiving protocol cannot interpret the sender's metric. The defaults differ and are a frequent source of surprise.

| Redistributed into | Seed metric | Notes |
|---|---|---|
| OSPF | cost 20 (E2); 1 for BGP routes | `subnets` needed for classless prefixes on older IOS; `metric-type 1` for E1 |
| EIGRP | none; route not installed without it | `metric bandwidth delay reliability load mtu` or `default-metric` |
| RIP | none (infinite) | `metric` or `default-metric` |
| BGP | metric copied (MED) | `redistribute ospf` brings only internal routes unless `match` is used |

*Policy-based routing* (PBR) routes on something other than the destination: `ip policy route-map WEB-VIA-B` on an interface, with `match ip address` for the traffic and `set ip next-hop 192.0.2.5`. *VRF-lite* gives one router several independent routing tables, each with its own interfaces, so two customers can both use 10.0.0.0/24; commands accept a `vrf` keyword (`ping vrf A 10.0.0.1`).

::: example
**Policy-based routing.** Campus Net sends web traffic from SALES via ISP-B while everything else uses the default route toward ISP-A.

```
ip access-list extended WEB
 permit tcp 192.168.10.0 0.0.0.255 any eq 80
 permit tcp 192.168.10.0 0.0.0.255 any eq 443
route-map WEB-VIA-B permit 10
 match ip address WEB
 set ip next-hop 192.0.2.5
interface GigabitEthernet0/0.10
 ip policy route-map WEB-VIA-B
```

```
R1# show route-map WEB-VIA-B
route-map WEB-VIA-B, permit, sequence 10
  Policy routing matches: 412 packets, 307311 bytes
```

[Result: matching packets leave via 192.0.2.5 regardless of the routing table; unmatched packets follow normal routing. PBR is stateless, so the return path may differ; add tracking so that it stops when the next hop is dead.]{.result}
:::

<figure>
<svg viewBox="0 0 480 130" width="480">
  <rect class="box" x="140" y="10" width="200" height="110" rx="4"/><text class="sm" x="148" y="24">One physical router</text>
  <rect class="hl" x="152" y="34" width="86" height="76" rx="2"/><text class="lbl" x="195" y="50" text-anchor="middle">VRF CUST-A</text><text class="sm" x="195" y="66" text-anchor="middle">10.0.0.0/24</text><text class="sm" x="195" y="80" text-anchor="middle">own routing table</text><text class="sm" x="195" y="94" text-anchor="middle">Gi0/3</text>
  <rect class="fill" x="244" y="34" width="86" height="76" rx="2"/><text class="lbl" x="287" y="50" text-anchor="middle">VRF CUST-B</text><text class="sm" x="287" y="66" text-anchor="middle">10.0.0.0/24</text><text class="sm" x="287" y="80" text-anchor="middle">own routing table</text><text class="sm" x="287" y="94" text-anchor="middle">Gi0/4</text>
  <text class="sm" x="10" y="60">customer A</text><line class="lg" x1="60" y1="58" x2="152" y2="90"/>
  <text class="sm" x="400" y="60">customer B</text><line class="lg" x1="398" y1="58" x2="330" y2="90"/>
</svg>
<figcaption><b>Figure 4.31</b> VRF-lite. The same prefix lives in two tables; a packet is looked up in the table of the interface it arrived on.</figcaption>
</figure>

```
vrf definition CUST-A
 address-family ipv4
interface GigabitEthernet0/3
 vrf forwarding CUST-A
 ip address 10.0.0.1 255.255.255.0
R1# show ip route vrf CUST-A
```

::: trap
*Claim:* redistributing in both directions between two protocols is safe because AD stops loops. *Why it is wrong:* AD protects only routes for the same prefix learnt natively; a redistributed route is seen as a native one by the second protocol, with another AD. *Correct statement:* tag at the first redistribution and deny the tag at the second.
:::

::: lens
[CISCO · JUNIPER · AMAZON]{.co}

Asked as "two-way redistribution loop and how do you stop it" and as "what does this route map do". Show the sequence evaluation and the implicit deny, state that a permit clause with no match matches everything, and distinguish a deny clause in a route map (the route is not redistributed) from a deny in a prefix list.
:::

::: lab
`LAB 4.9 · 40 MIN`  GNS3 with IOSv or FRR: three routers, OSPF on one side and EIGRP on the other, mutual redistribution at two routers. Create the loop first, then fix it with tags; finally build VRF-lite with an overlapping 10.0.0.0/24 in two VRFs.

```
R1# show ip route 10.9.9.0
Routing entry for 10.9.9.0/24
  Known via "ospf 1", distance 110, metric 20, type extern 2, tag 110
```

**What you should notice:** a tag on the route proves where it entered. Without the deny-tag clause, the router prefers the redistributed copy of its own route learned from the other router (an effect of AD); `traceroute` to the prefix bounces between the two redistribution points.
:::

## [4.10]{.sec}MPLS and L3VPN [Should · ■■■]{.tag} {#s4-10}

::: bigidea
MPLS forwards packets on short labels instead of IP addresses, which lets a provider carry many customers' overlapping address spaces across one core: inner labels identify the customer, outer labels identify the path.
:::

A *label* is a 32-bit shim header inserted between the Layer 2 and IP headers (EtherType 0x8847): a 20-bit label, a 3-bit traffic class, a 1-bit bottom-of-stack flag and an 8-bit TTL. Labels are *pushed*, *swapped* and *popped*. The edge router (*PE*, provider edge) pushes labels; core routers (*P*) swap them using the *LFIB* and never look at the IP header; customer routers are *CE*s. Labels 0 to 15 are reserved: 0 (IPv4 explicit null), 1 (router alert), 2 (IPv6 explicit null), 3 (*implicit null*). Labels are distributed hop by hop by LDP (UDP 646 for discovery, TCP 646 for sessions), one per IGP prefix. With *penultimate-hop popping* (PHP) the router before the egress pops the transport label, because the egress PE advertises implicit null (3) for its own address: the egress then does a single lookup rather than two.

<figure>
<svg viewBox="0 0 480 60" width="480">
  <rect class="box" x="10" y="10" width="200" height="26"/><text class="lbl" x="110" y="27" text-anchor="middle">Label 20 bits</text>
  <rect class="box" x="210" y="10" width="60" height="26"/><text class="lbl" x="240" y="27" text-anchor="middle">TC 3</text>
  <rect class="hl" x="270" y="10" width="30" height="26"/><text class="lbl" x="285" y="27" text-anchor="middle">S 1</text>
  <rect class="box" x="300" y="10" width="80" height="26"/><text class="lbl" x="340" y="27" text-anchor="middle">TTL 8</text>
  <text class="sm" x="10" y="52">32 bits; S = 1 marks the last label of the stack, so a two-label VPN packet has S = 0 on the outer label.</text>
</svg>
<figcaption><b>Figure 4.32</b> The MPLS shim.</figcaption>
</figure>

Each router keeps two label tables. The *LIB* (label information base) holds every label it has learnt from neighbours; the *LFIB* (label forwarding information base) holds the one chosen for each prefix, according to the IGP's best next hop. Label *swap* replaces the top label by the one the next hop advertised; the TTL field is decremented as in IP (and the ingress copies the IP TTL into it, unless `no mpls ip propagate-ttl` hides the core from `traceroute`). On the control plane, LDP (label distribution protocol) runs in a hop-by-hop fashion: each router assigns a local label for every prefix in its IGP and advertises it to its LDP neighbours, so that a *label-switched path* follows the IGP's shortest path.

```
P1# show mpls ldp neighbor
    Peer LDP Ident: 10.255.0.3:0; Local LDP Ident 10.255.0.2:0
        TCP connection: 10.255.0.3.646 - 10.255.0.2.43211
        State: Oper; Msgs sent/rcvd: 40/39
P1# show mpls forwarding-table
Local  Outgoing   Prefix           Bytes Label   Outgoing   Next Hop
Label  Label      or Tunnel Id     Switched      interface
24     35         10.255.0.5/32    0             Gi0/2      10.1.23.3     <-- swap 24 to 35
```

<figure>
<svg viewBox="0 0 480 180" width="480">
  <rect class="box" x="10" y="10" width="210" height="64" rx="3"/><text class="sm" x="16" y="24">Customer A, PE1 VRF A (RD 65000:1)</text>
  <text class="mono" x="16" y="42">10.1.1.0/24 -&gt; 65000:1:10.1.1.0/24</text><text class="sm" x="16" y="58">export RT 65000:1</text>
  <rect class="box" x="10" y="100" width="210" height="64" rx="3"/><text class="sm" x="16" y="114">Customer B, PE1 VRF B (RD 65000:2)</text>
  <text class="mono" x="16" y="132">10.1.1.0/24 -&gt; 65000:2:10.1.1.0/24</text><text class="sm" x="16" y="148">export RT 65000:2</text>
  <rect class="hl" x="260" y="42" width="210" height="96" rx="3"/><text class="lbl" x="365" y="60" text-anchor="middle">MP-BGP VPNv4 table</text>
  <text class="sm" x="270" y="78">two distinct 96-bit prefixes,</text><text class="sm" x="270" y="90">same IPv4 address</text><text class="sm" x="270" y="108">PE2 imports a route only if its</text><text class="sm" x="270" y="120">import RT matches the export RT</text>
  <line class="acc" x1="220" y1="42" x2="260" y2="70"/><line class="ln" x1="220" y1="132" x2="260" y2="110"/>
</svg>
<figcaption><b>Figure 4.33</b> RD and RT. The RD only makes the prefixes distinct; the RT is the membership rule that decides which VRF receives each one.</figcaption>
</figure>

An *L3VPN* (RFC 4364) uses three ideas. Each customer has a *VRF* on the PE. A *route distinguisher* (RD, 64 bits) is prefixed to each customer IPv4 route to make a 96-bit *VPNv4* prefix, so that two customers' 10.1.1.0/24 stay distinct in BGP. A *route target* (RT, a BGP extended community) controls which VRFs import which routes: export RTs are attached when a route is advertised, import RTs select it at the far PE. PEs exchange VPNv4 routes over MP-BGP; the transport path between them is given by LDP labels.

| | RD | RT |
|---|---|---|
| Purpose | makes a prefix unique in the provider's BGP | decides which VRFs install the route |
| Where carried | prefix of the VPNv4 NLRI | extended community attribute |
| Typical value | 65000:1 | 65000:1 (import and export) |

::: example
**An L3VPN packet walk.** Customer A site 1 (CE1, 10.1.1.0/24) sends to site 2 (CE2, 10.2.2.0/24) through PE1, P1, P2, PE2. Customer B also uses 10.1.1.0/24 (RD and RT 65000:2).

1. CE1 to PE1: an ordinary IP packet. PE1 looks up the destination in VRF A, finds a VPNv4 route from PE2 with VPN label 300 and BGP next hop PE2's loopback.
2. PE1 pushes two labels: VPN label 300 (inner, bottom of stack) and the LDP label 24 for PE2's loopback (outer).
3. P1 swaps 24 for 35. P1 never reads label 300 or the IP header.
4. P2 is the penultimate hop. PE2 advertised implicit null, so P2 *pops* the transport label and forwards a packet carrying only label 300.
5. PE2 looks up 300, which belongs to VRF A, pops it, performs an IP lookup in VRF A and forwards the packet to CE2.

[Result: customer A and B never meet, because each VPN label points to a VRF and each VRF has its own table.]{.result}
:::

<figure>
<svg viewBox="0 0 480 140" width="480">
  <rect class="box" x="22" y="14" width="36" height="22" rx="2"/><text class="lbl" x="40" y="29" text-anchor="middle">CE1</text>
  <circle class="fill" cx="120" cy="25" r="14"/><text class="lbl" x="120" y="28" text-anchor="middle">PE1</text>
  <circle class="box" cx="200" cy="25" r="14"/><text class="lbl" x="200" y="28" text-anchor="middle">P1</text>
  <circle class="box" cx="280" cy="25" r="14"/><text class="lbl" x="280" y="28" text-anchor="middle">P2</text>
  <circle class="fill" cx="360" cy="25" r="14"/><text class="lbl" x="360" y="28" text-anchor="middle">PE2</text>
  <rect class="box" x="422" y="14" width="36" height="22" rx="2"/><text class="lbl" x="440" y="29" text-anchor="middle">CE2</text>
  <line class="ln" x1="58" y1="25" x2="106" y2="25"/><line class="ln" x1="134" y1="25" x2="186" y2="25"/><line class="ln" x1="214" y1="25" x2="266" y2="25"/><line class="ln" x1="294" y1="25" x2="346" y2="25"/><line class="ln" x1="374" y1="25" x2="422" y2="25"/>
  <g class="cards">
  <rect class="hl" x="134" y="52" width="52" height="16"/><rect class="box" x="134" y="52" width="52" height="16" fill="none"/><text class="sm" x="160" y="63" text-anchor="middle">24</text>
  <rect class="hl" x="214" y="52" width="52" height="16"/><rect class="box" x="214" y="52" width="52" height="16" fill="none"/><text class="sm" x="240" y="63" text-anchor="middle">35</text>
  <rect class="box" x="134" y="68" width="52" height="16"/><text class="sm" x="160" y="79" text-anchor="middle">VPN 300</text>
  <rect class="box" x="214" y="68" width="52" height="16"/><text class="sm" x="240" y="79" text-anchor="middle">VPN 300</text>
  <rect class="box" x="294" y="68" width="52" height="16"/><text class="sm" x="320" y="79" text-anchor="middle">VPN 300</text>
  <rect class="fill" x="64" y="84" width="40" height="16"/><text class="sm" x="84" y="95" text-anchor="middle">IP</text>
  <rect class="fill" x="134" y="84" width="52" height="16"/><text class="sm" x="160" y="95" text-anchor="middle">IP</text>
  <rect class="fill" x="214" y="84" width="52" height="16"/><text class="sm" x="240" y="95" text-anchor="middle">IP</text>
  <rect class="fill" x="294" y="84" width="52" height="16"/><text class="sm" x="320" y="95" text-anchor="middle">IP</text>
  <rect class="fill" x="376" y="84" width="40" height="16"/><text class="sm" x="396" y="95" text-anchor="middle">IP</text>
  </g>
  <text class="sm" x="10" y="118">Highlighted block: transport (LDP) label. Open block below it: VPN label. P2 pops the transport label (PHP).</text>
  <text class="sm" x="10" y="130">Control plane: LDP between neighbours; MP-BGP VPNv4 between PE1 and PE2.</text>
</svg>
<figcaption><b>Figure 4.34</b> The label stack at each link of the L3VPN walk.</figcaption>
</figure>

```
vrf definition CUST-A
 rd 65000:1
 address-family ipv4
  route-target both 65000:1
interface GigabitEthernet0/1
 vrf forwarding CUST-A
 ip address 10.1.1.1 255.255.255.0
router bgp 65000
 neighbor 10.255.0.5 remote-as 65000
 neighbor 10.255.0.5 update-source Loopback0
 address-family vpnv4
  neighbor 10.255.0.5 activate
  neighbor 10.255.0.5 send-community extended
```

Verification at the provider edge follows the control plane: first the VRF routing table at each PE, then the VPNv4 table, and finally the label path.

```
PE1# show ip route vrf CUST-A 10.2.2.0
B  10.2.2.0/24 [200/0] via 10.255.0.5, 00:12:30          <-- learnt by MP-BGP from PE2
PE1# show bgp vpnv4 unicast all 10.2.2.0/24
  Route Distinguisher: 65000:1 (default for vrf CUST-A)
  Local: 10.255.0.5 (metric 20); label 300; Extended Community: RT:65000:1
PE1# traceroute vrf CUST-A 10.2.2.1
  1 10.1.12.2 [MPLS: Labels 24/300 Exp 0] 4 msec         <-- the two-label stack
```

Beyond L3VPN, MPLS traffic engineering and Segment Routing (SR-MPLS, SRv6) steer traffic along explicit paths by stacking labels or segment identifiers at the ingress; they matter mainly for service-provider roles and are outside the ENCOR core.

::: lens
[JUNIPER · NOKIA · CISCO]{.co}

The L3VPN walk is the standard question. Answer with the two-label stack, who pushes, swaps and pops, and why PHP exists. A good answer separates control plane (LDP for transport, MP-BGP for VPN labels) from data plane, and states in one line what RD and RT each do.
:::

::: lab
`LAB 4.10 · 40 MIN`  FRR Containerlab (Linux MPLS) or GNS3: four-router core, two customers with overlapping 10.1.1.0/24.

```
vtysh -c "show mpls ldp binding"
vtysh -c "show bgp ipv4 vpn"
ip -f mpls route
```

**What you should notice:** the VPNv4 table shows the same prefix twice under different RDs; the `ip -f mpls route` output shows `swap` at P routers and `pop` at the penultimate hop.
:::

:::
