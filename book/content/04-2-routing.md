::: {.p4}

## [4.4]{.sec}The routing table, static and default routes [Must · ■□□]{.tag} {#s4-4}

::: bigidea
A router chooses among routes by three tests in a fixed order (the longest matching prefix, then the lowest administrative distance, then the lowest metric), because each test answers a different question: how specific, how trustworthy and how short.
:::

The *routing table* holds one best route per prefix. When a packet arrives, the router finds the entry with the longest prefix that contains the destination address (the algorithm and its trie implementation are in [§1.9](#s1-9){.ref}). Only if several *sources* offer the same prefix and mask does the *administrative distance* (AD) decide: it is a local trust rating from 0 to 255 assigned to each source of routes, and lower wins. Only if one protocol offers several paths to the same prefix does the *metric*, the protocol's own measure of path length, decide. Metrics from different protocols are never compared, since OSPF cost and RIP hop count measure different things.

| Source | AD | Source | AD |
|---|---|---|---|
| Connected interface | 0 | IS-IS | 115 |
| Static route (next hop or interface) | 1 | RIP | 120 |
| EIGRP summary route | 5 | EIGRP external | 170 |
| eBGP | 20 | iBGP | 200 |
| EIGRP internal | 90 | DHCP-learned default | 254 |
| OSPF | 110 | Unusable | 255 |

```
BR1# show ip route
Gateway of last resort is 192.0.2.1 to network 0.0.0.0
S*    0.0.0.0/0 [1/0] via 192.0.2.1
      10.0.0.0/8 is variably subnetted, 3 subnets, 2 masks
O        10.1.1.0/24 [110/20] via 10.1.12.2, 00:04:10, GigabitEthernet0/2
C        10.1.12.0/30 is directly connected, GigabitEthernet0/2
L        10.1.12.1/32 is directly connected, GigabitEthernet0/2
```

Read each line from the left. The code names the source (`C` connected, `L` local address of the router itself as a /32, `S` static, `O` OSPF, `B` BGP, `*` candidate default). Next come the prefix, then `[AD/metric]`, then the next hop, the age and the exit interface. The "gateway of last resort" is the default route.

<figure>
<svg viewBox="0 0 480 80" width="480">
  <defs><marker id="a44" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="#1A1D23"/></marker></defs>
  <rect class="box" x="8" y="20" width="100" height="38" rx="2"/><text class="lbl" x="58" y="36" text-anchor="middle">1 Longest prefix</text><text class="sm" x="58" y="50" text-anchor="middle">most specific mask</text>
  <rect class="box" x="132" y="20" width="100" height="38" rx="2"/><text class="lbl" x="182" y="36" text-anchor="middle">2 Lowest AD</text><text class="sm" x="182" y="50" text-anchor="middle">between sources</text>
  <rect class="box" x="256" y="20" width="100" height="38" rx="2"/><text class="lbl" x="306" y="36" text-anchor="middle">3 Lowest metric</text><text class="sm" x="306" y="50" text-anchor="middle">within one protocol</text>
  <rect class="hl" x="380" y="20" width="92" height="38" rx="2"/><text class="lbl" x="426" y="36" text-anchor="middle">4 Tie: ECMP</text><text class="sm" x="426" y="50" text-anchor="middle">share the load</text>
  <line class="ln" x1="108" y1="39" x2="132" y2="39" marker-end="url(#a44)"/><line class="ln" x1="232" y1="39" x2="256" y2="39" marker-end="url(#a44)"/><line class="ln" x1="356" y1="39" x2="380" y2="39" marker-end="url(#a44)"/>
  <text class="sm" x="8" y="12">the decision for one destination address</text>
</svg>
<figcaption><b>Figure 4.7</b> The route-selection order. Steps 2 and 3 matter only among candidates for the same prefix and mask.</figcaption>
</figure>

A *static route* is configured by hand. Pointing it at a next-hop address (`ip route 10.9.0.0 255.255.0.0 10.1.12.2`) needs a *recursive lookup* to find the exit interface; pointing it at an interface alone is acceptable only on point-to-point links, since on Ethernet the router would ARP for every destination. A *default route* is the prefix 0.0.0.0/0, which matches everything with the shortest possible prefix, so it is used only when nothing else matches. A static route to `Null0` discards traffic, and is used to anchor a summary. The IPv6 forms are `ipv6 route 2001:db8:9::/48 2001:db8:12::2` and `ipv6 route ::/0 ...`. Equal-cost paths are installed together (ECMP, four by default on many IOS releases) and the load is spread per flow.

::: example
**The routing-table puzzle.** R1 holds four candidates: OSPF 10.1.0.0/16 [110/20], EIGRP 10.1.0.0/16 [90/3072], static 10.1.1.0/24 [1/0] and RIP 10.0.0.0/8 [120/2]. Where do three packets go?

1. Installed routes. The OSPF and EIGRP /16 entries have the same prefix and mask, so AD decides: EIGRP (90) is installed and OSPF (110) is held back. The static /24 and the RIP /8 have different masks, so both are installed.
2. 10.1.1.9 matches the /24, /16 and /8. The longest prefix is the /24, so it goes by the static route; AD is not consulted at all, because the candidates differ in mask.
3. 10.1.5.5 fails the /24 and matches the /16 (EIGRP) and the /8. The /16 wins.
4. 10.200.0.1 matches only the /8, so it goes to RIP.

[Result: static /24, EIGRP /16, RIP /8; AD was used once, to choose between OSPF and EIGRP.]{.result}
:::

A *floating static route* is a static route given an AD higher than the dynamic protocol's, so it sits idle until the dynamic route disappears. For Campus Net's backup path to ISP-B, with the primary default learned by OSPF from the border at AD 110:

```
BR1(config)# ip route 0.0.0.0 0.0.0.0 203.0.113.9 250
```

```
BR1# show ip route 0.0.0.0                  ! primary present
O*E2  0.0.0.0/0 [110/1] via 192.0.2.1
BR1# show ip route 0.0.0.0                  ! after the primary link fails
S*    0.0.0.0/0 [250/0] via 203.0.113.9     <-- floating route installed
```

::: trap
*Claim:* a /16 connected route beats a /24 static route because connected has AD 0. *Why it is wrong:* AD is consulted only between routes for the same prefix and mask. *Correct statement:* the longest prefix is tested first, so a /24 static is used for traffic it matches whatever the AD of the shorter /16.
:::

::: lens
[CISCO · AMAZON · JUNIPER]{.co}

Asked as "order the routing decision" or as a puzzle like the one above. State the order, then say that AD is evaluated once at install time and metric only inside one protocol. Follow-ups: why a floating static can be unreliable when the primary link stays up but the path is broken (use IP SLA tracking, [§4.14](#s4-14){.ref}), and what a recursive lookup is.
:::

::: check
1. A router learns 172.16.0.0/16 by eBGP and by OSPF. Which is installed? [^c4-5]
2. Why is `ip route 10.9.0.0 255.255.0.0 Gi0/1` unwise on an Ethernet link? [^c4-6]
:::

[^c4-5]: eBGP (AD 20), because the prefix and mask are identical and 20 is below OSPF's 110.
[^c4-6]: The router treats 10.9.0.0/16 as directly connected and ARPs for every destination in it; this loads the segment and needs proxy ARP on the neighbour.

## [4.5]{.sec}OSPF [Must · ■■□]{.tag} {#s4-5}

::: bigidea
OSPF is a link-state protocol: every router floods a description of its own links to all routers in its area, so that each builds the same map and independently computes shortest paths, which makes convergence fast and loop-free inside an area.
:::

Each router describes itself in a *link-state advertisement* (LSA); the set of LSAs it holds is its *link-state database* (LSDB). Because every router in an area holds an identical LSDB, each runs the same shortest-path-first (SPF) computation, which is Dijkstra's algorithm ([§1.11](#s1-11){.ref}), with itself as the root. The link metric is the *cost*, the reference bandwidth divided by the interface bandwidth. Routers become *neighbours* by exchanging Hello packets; neighbours that go on to synchronise databases are *adjacent*. OSPF runs directly over IP (protocol 89, TTL 1), sending to the multicast groups 224.0.0.5 (all OSPF routers) and 224.0.0.6 (DR and BDR only). Five packet types exist: Hello, Database Description (DBD, a catalogue of LSA headers), Link-State Request (LSR), Link-State Update (LSU, carrying full LSAs) and Link-State Acknowledgement (LSAck).

Hello and dead timers are 10 s and 40 s on broadcast and point-to-point links, and 30 s and 120 s on non-broadcast multi-access links. The *router ID* (RID), a 32-bit identifier, is chosen in this order: the `router-id` command, else the highest loopback address, else the highest active interface address.

<figure>
<svg viewBox="0 0 480 150" width="480">
  <defs><marker id="a45" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="#1A1D23"/></marker></defs>
  <g>
  <rect class="box" x="10" y="26" width="56" height="26" rx="6"/><text class="lbl" x="38" y="43" text-anchor="middle">Down</text>
  <rect class="box" x="77" y="26" width="56" height="26" rx="6"/><text class="lbl" x="105" y="43" text-anchor="middle">Init</text>
  <rect class="box" x="144" y="26" width="56" height="26" rx="6"/><text class="lbl" x="172" y="43" text-anchor="middle">2-Way</text>
  <rect class="box" x="211" y="26" width="56" height="26" rx="6"/><text class="lbl" x="239" y="43" text-anchor="middle">ExStart</text>
  <rect class="box" x="278" y="26" width="56" height="26" rx="6"/><text class="lbl" x="306" y="43" text-anchor="middle">Exchange</text>
  <rect class="box" x="345" y="26" width="56" height="26" rx="6"/><text class="lbl" x="373" y="43" text-anchor="middle">Loading</text>
  <rect class="hl" x="412" y="26" width="56" height="26" rx="6"/><rect class="box" x="412" y="26" width="56" height="26" rx="6" fill="none"/><text class="lbl" x="440" y="43" text-anchor="middle">Full</text>
  </g>
  <line class="ln" x1="66" y1="39" x2="77" y2="39" marker-end="url(#a45)"/><line class="ln" x1="133" y1="39" x2="144" y2="39" marker-end="url(#a45)"/><line class="ln" x1="200" y1="39" x2="211" y2="39" marker-end="url(#a45)"/><line class="ln" x1="267" y1="39" x2="278" y2="39" marker-end="url(#a45)"/><line class="ln" x1="334" y1="39" x2="345" y2="39" marker-end="url(#a45)"/><line class="ln" x1="401" y1="39" x2="412" y2="39" marker-end="url(#a45)"/>
  <text class="sm" x="38" y="68" text-anchor="middle">no hello yet</text>
  <text class="sm" x="105" y="68" text-anchor="middle">hello heard,</text><text class="sm" x="105" y="77" text-anchor="middle">my RID absent</text>
  <text class="sm" x="172" y="68" text-anchor="middle">hello lists</text><text class="sm" x="172" y="77" text-anchor="middle">my RID</text>
  <text class="sm" x="239" y="68" text-anchor="middle">DBD: elect</text><text class="sm" x="239" y="77" text-anchor="middle">master</text>
  <text class="sm" x="306" y="68" text-anchor="middle">DBD: swap</text><text class="sm" x="306" y="77" text-anchor="middle">LSA headers</text>
  <text class="sm" x="373" y="68" text-anchor="middle">LSR, LSU,</text><text class="sm" x="373" y="77" text-anchor="middle">LSAck</text>
  <text class="sm" x="440" y="68" text-anchor="middle">LSDBs</text><text class="sm" x="440" y="77" text-anchor="middle">identical</text>
  <path class="ln" d="M144,90 L144,94 L200,94 L200,90"/><text class="sm" x="172" y="106" text-anchor="middle">final state between</text><text class="sm" x="172" y="115" text-anchor="middle">two DROTHERs</text>
  <path class="acc" d="M211,90 L211,94 L334,94 L334,90"/><text class="sm" x="272" y="106" text-anchor="middle">stuck here: MTU mismatch,</text><text class="sm" x="272" y="115" text-anchor="middle">duplicate RID, unicast blocked</text>
  <path class="ln" d="M77,90 L77,94 L133,94 L133,90"/><text class="sm" x="105" y="130" text-anchor="middle">stuck: one-way hellos,</text><text class="sm" x="105" y="139" text-anchor="middle">ACL, timer or area mismatch</text>
</svg>
<figcaption><b>Figure 4.8</b> The OSPF neighbour state machine. A neighbour is adjacent only at Full; on a multi-access segment, 2-Way is the normal final state between two routers that are neither DR nor BDR.</figcaption>
</figure>

States, in order: *Down*; *Attempt* (non-broadcast networks only); *Init* (a hello has been heard, but it does not yet list our RID); *2-Way* (hellos are bidirectional; DR and BDR are elected here); *ExStart* (the two choose a master and initial sequence number); *Exchange* (DBDs list the LSA headers each holds); *Loading* (missing LSAs are fetched with LSR and delivered by LSU); *Full*. For two routers to become neighbours, the following must match: area ID, subnet and mask, hello and dead timers, authentication, stub-area flags and network type compatibility; the router IDs must differ. To reach Full, the interface MTU must also agree, since the MTU is carried in the DBD.

::: example
**An adjacency stuck in EXSTART.** BR1's Gi0/1 has MTU 1500 and the ISP-side router's has MTU 1400.

1. In the DBD, each side advertises its interface MTU. A router that receives a DBD advertising a *larger* MTU than its own interface can carry discards it.
2. Thus the 1400-byte side rejects BR1's DBDs. BR1 accepts the smaller ones and may reach Exchange, but its DBDs are never acknowledged, so it retransmits until the neighbour is declared down.
3. The symptom is a neighbour that cycles EXSTART/EXCHANGE and drops with "too many retransmissions". Hellos work, so the neighbour appears briefly healthy.

```
BR1# show ip ospf neighbor
Neighbor ID  Pri State        Dead Time  Address    Interface
2.2.2.2      1   EXSTART/DR   00:00:36   10.1.12.2  Gi0/1      <-- stuck
BR1# debug ip ospf adj
OSPF-1 ADJ Gi0/1: Nbr 2.2.2.2 has smaller interface MTU
```

[Result: the fix is to make the MTUs equal (`ip mtu 1400` on both). `ip ospf mtu-ignore` removes the check but hides a real path-MTU problem, so treat it as a smell.]{.result}
:::

On a broadcast segment (Ethernet) with *n* routers, full adjacency among all would need n(n-1)/2 adjacencies and flood each LSA many times. OSPF therefore elects a *designated router* (DR) and a *backup* (BDR). Every other router (a *DROTHER*) becomes adjacent only with the DR and BDR: it sends updates to 224.0.0.6, and the DR re-floods them to 224.0.0.5. The election uses the interface *priority* (default 1; 0 means ineligible), then the highest RID. It is *non-preemptive*: a router joining later never displaces the current DR, whatever its priority. Point-to-point links need no election, and `ip ospf network point-to-point` on an Ethernet link between two routers avoids one.

::: example
**DR election.** R1 (priority 1, RID 1.1.1.1), R2 (1, 2.2.2.2), R3 (0), R4 (1, 4.4.4.4) boot together on one LAN.

1. R3 is excluded by priority 0. Among R1, R2 and R4 the priorities tie, so the highest RID wins: DR = R4, BDR = R2 (the next highest).
2. R5 joins with priority 255. Election is not preemptive, so nothing changes: R4 stays DR.
3. R4 fails. The BDR, R2, is promoted to DR, and a new BDR is elected among the rest, where R5's priority 255 beats R1's 1: BDR = R5.

[Result: DR R4 then R2; BDR R2 then R5; R3 is never DR or BDR.]{.result}
:::

The cost of an interface is the reference bandwidth divided by the interface bandwidth, with a minimum of 1. The default reference is 100 Mb/s, so Fast Ethernet is 1, and both Gigabit and 10 Gigabit Ethernet are also 1, because the quotient is truncated. The command `auto-cost reference-bandwidth 100000` (100 Gb/s) gives 1 Gb/s a cost of 100 and 10 Gb/s a cost of 10; it must be the same on every router in the domain.

::: example
**An SPF calculation.** Link costs: R1-R2 10, R1-R3 5, R3-R2 3, R2-R4 1, R3-R4 10. Which path does R1 use to reach R4, where a loopback 10.255.0.4/32 of cost 1 lives?

1. Candidate paths: R1-R2-R4 costs 10 + 1 = 11; R1-R3-R4 costs 5 + 10 = 15; R1-R3-R2-R4 costs 5 + 3 + 1 = 9.
2. Dijkstra settles R3 first (cost 5), then R2 via R3 (8, better than the direct 10), then R4 (9).
3. The loopback adds its own cost of 1.

```
R1# show ip route ospf
O   10.255.0.4/32 [110/10] via 10.1.13.3, 00:00:21, GigabitEthernet0/2
```

[Result: next hop is R3; the metric is 9 + 1 = 10. The longer-looking path wins because its links are cheaper.]{.result}
:::

<figure>
<svg viewBox="0 0 480 150" width="480">
  <circle class="box" cx="60" cy="75" r="16"/><path class="ln" d="M52,67 L68,83 M68,67 L52,83"/><text class="lbl" x="60" y="106" text-anchor="middle">R1</text>
  <circle class="box" cx="200" cy="28" r="16"/><path class="ln" d="M192,20 L208,36 M208,20 L192,36"/><text class="lbl" x="200" y="60" text-anchor="middle">R2</text>
  <circle class="box" cx="200" cy="125" r="16"/><path class="ln" d="M192,117 L208,133 M208,117 L192,133"/><text class="lbl" x="200" y="156" text-anchor="middle">R3</text>
  <circle class="box" cx="350" cy="75" r="16"/><path class="ln" d="M342,67 L358,83 M358,67 L342,83"/><text class="lbl" x="350" y="106" text-anchor="middle">R4</text>
  <line class="lg" x1="74" y1="66" x2="186" y2="34"/><text class="sm" x="120" y="42">10</text>
  <line class="lg" x1="200" y1="44" x2="200" y2="109"/><text class="sm" x="206" y="80">3</text>
  <line class="lg" x1="214" y1="116" x2="336" y2="84"/><text class="sm" x="290" y="112">10</text>
  <path class="acc" d="M75,83 L186,120"/><text class="sm" x="110" y="112">5</text>
  <path class="acc" d="M200,109 L200,44"/>
  <path class="acc" d="M214,34 L336,66"/><text class="sm" x="280" y="44">1</text>
  <text class="sm" x="390" y="66">best path: cost 9</text><text class="sm" x="390" y="78">(accent)</text>
</svg>
<figcaption><b>Figure 4.9</b> The shortest-path tree rooted at R1. The path R1-R3-R2-R4 costs 9; R1-R2-R4 would cost 11.</figcaption>
</figure>

Large domains are divided into *areas* to limit the size of each LSDB and to confine the effect of flapping links. Area 0, the *backbone*, must connect every other area, because inter-area routes travel as distance vectors through it. A router with interfaces in two areas is an *area border router* (ABR); a router that injects routes from outside OSPF is an *autonomous system boundary router* (ASBR). If an area cannot physically touch area 0, a *virtual link* through a transit area patches the gap.

| Type | Name | Originated by | Describes | Flooded |
|---|---|---|---|---|
| 1 | Router | every router | its own links and costs | within the area |
| 2 | Network | the DR | the routers on a multi-access segment | within the area |
| 3 | Summary | an ABR | a prefix from another area (with cost) | into adjacent areas |
| 4 | ASBR summary | an ABR | the *location* of an ASBR | into adjacent areas (not the ASBR's own) |
| 5 | AS external | an ASBR | a route from outside OSPF | whole domain except stub areas |
| 7 | NSSA external | an ASBR inside an NSSA | an external route | inside the NSSA; the ABR converts it to type 5 |

<figure>
<svg viewBox="0 0 480 200" width="480">
  <defs><marker id="b45" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="#1A1D23"/></marker><marker id="c45" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="#21705A"/></marker></defs>
  <rect class="lg dash" x="8" y="18" width="120" height="76" rx="6"/><text class="sm" x="14" y="30">Area 1</text>
  <rect class="lg dash" x="150" y="18" width="180" height="76" rx="6"/><text class="sm" x="156" y="30">Area 0 (backbone)</text>
  <rect class="lg dash" x="352" y="18" width="120" height="76" rx="6"/><text class="sm" x="358" y="30">Area 2</text>
  <line class="ln" x1="66" y1="62" x2="130" y2="62"/><line class="ln" x1="150" y1="62" x2="330" y2="62"/><line class="ln" x1="350" y1="62" x2="414" y2="62"/>
  <circle class="box" cx="60" cy="62" r="10"/><text class="lbl" x="60" y="86" text-anchor="middle">R1</text>
  <circle class="fill" cx="140" cy="62" r="10"/><text class="lbl" x="140" y="86" text-anchor="middle">R2 ABR</text>
  <circle class="fill" cx="340" cy="62" r="10"/><text class="lbl" x="340" y="86" text-anchor="middle">R3 ABR</text>
  <circle class="box" cx="420" cy="62" r="10"/><text class="lbl" x="420" y="86" text-anchor="middle">R4 ASBR</text>
  <rect class="box" x="388" y="102" width="86" height="18" rx="9"/><text class="sm" x="431" y="114" text-anchor="middle">172.16.0.0/16</text><line class="ln dash" x1="420" y1="72" x2="425" y2="102"/>
  <text class="sm" x="10" y="140">Type 1, 2 stay in their area (three short bars)</text>
  <line class="ln" x1="10" y1="146" x2="126" y2="146"/><line class="ln" x1="152" y1="146" x2="328" y2="146"/><line class="ln" x1="354" y1="146" x2="470" y2="146"/>
  <text class="sm" x="10" y="160">Type 3 prefixes cross each ABR</text>
  <line class="ln" x1="10" y1="165" x2="470" y2="165" marker-start="url(#b45)" marker-end="url(#b45)"/>
  <text class="sm" x="10" y="179">Type 4 locates R4 (R3 into area 0, R2 into area 1)</text>
  <line class="ln" x1="10" y1="183" x2="350" y2="183" marker-start="url(#b45)"/>
  <text class="sm" x="10" y="196">Type 5 reaches every non-stub area</text>
</svg>
<figcaption><b>Figure 4.10</b> Flooding scope of the LSA types in a three-area network. R1 in area 1 holds type 3 LSAs for area 2's prefixes, type 4 for R4 and type 5 for 172.16.0.0/16.</figcaption>
</figure>

The area types control which LSAs may enter, to shrink the LSDB of small routers. A *stub area* blocks types 4 and 5 and the ABR injects a default route as a type 3. A *totally stubby area* (Cisco: `stub no-summary`) also blocks types 3, leaving only intra-area LSAs and one default. A *not-so-stubby area* (NSSA) blocks types 4 and 5 but lets an ASBR inside the area originate type 7, which the ABR translates to type 5 on entering the backbone. A *totally NSSA* also blocks type 3, with a default from the ABR.

| Area type | LSA 1, 2 | LSA 3 | LSA 4, 5 | LSA 7 | Default route |
|---|---|---|---|---|---|
| Normal | yes | yes | yes | no | none (optional) |
| Stub | yes | yes | no | no | type 3, automatic |
| Totally stubby | yes | default only | no | no | type 3, automatic |
| NSSA | yes | yes | no | yes | type 7, if configured |
| Totally NSSA | yes | default only | no | yes | type 3, automatic |

::: example
**Converting area 1 to totally stubby.** In Figure 4.10, R1 holds type 1 (R1, R2), type 3 (prefixes of areas 0 and 2), type 4 (R4) and type 5 (172.16.0.0/16).

1. Configure `area 1 stub` on R1 and on the ABR R2. Hello packets carry a stub flag, so both must agree or the adjacency fails.
2. On R2 only, add `no-summary`. R2 stops flooding types 3, 4 and 5 into area 1 and injects a single type 3 default instead.

```
R2(config-router)# area 1 stub no-summary
R1# show ip route ospf
O*IA  0.0.0.0/0 [110/2] via 10.1.12.2, GigabitEthernet0/1
```

[Result: R1's database shrinks to type 1 and 2 LSAs plus one default; traffic to everything else leaves through the ABR.]{.result}
:::

Routes carry a code that shows how they were learnt: `O` (intra-area), `O IA` (inter-area, from a type 3), `O E1` and `O E2` (external, type 5) and `O N1`/`O N2` (NSSA). A path's preference is `O`, then `O IA`, then `E1`, then `E2`, regardless of cost. An E2 route carries only the external cost, which is the default and is what is compared by all routers; an E1 route adds the internal cost to the ASBR, and is preferred when there are several ASBRs at different distances.

Three techniques contain flapping. *Summarisation* at the ABR (`area 3 range 10.3.0.0 255.255.0.0`) or at the ASBR (`summary-address`) hides detail so that one flapping /24 inside the range does not trigger SPF elsewhere. A *stub area* removes external LSAs. *Throttling* (`timers throttle spf 50 200 5000`) delays repeated SPF runs, and BFD detects failures in milliseconds so that timers can stay conservative. OSPFv3 uses the same states and algorithm for IPv6, but runs per link rather than per subnet, uses link-local addresses as next hops, sends to ff02::5 and ff02::6, and moves addresses out of the router and network LSAs into new LSA types (8, the link LSA, and 9, the intra-area-prefix LSA).

```
BR1(config)# router ospf 1
BR1(config-router)# router-id 1.1.1.1
BR1(config-router)# auto-cost reference-bandwidth 100000
BR1(config-router)# passive-interface default
BR1(config-router)# no passive-interface GigabitEthernet0/2
BR1(config)# interface GigabitEthernet0/2
BR1(config-if)# ip ospf 1 area 0
BR1(config-if)# ip ospf network point-to-point
```

[**Junos and FRR** — Junos: `set protocols ospf area 0 interface ge-0/0/2.0`. FRR: `router ospf` then `network 10.1.12.0/30 area 0`, or `ip ospf area 0` on the interface.]{.margin}Verification uses three commands: `show ip ospf neighbor` (state and DR role), `show ip ospf database` (the LSAs by type, and their age) and `show ip ospf interface` (cost, timers, network type, DR). The commonest adjacency faults are, in order: mismatched hello or dead timers, mismatched area, mismatched MTU, a passive interface, duplicate router IDs and a wrong authentication key.

::: trap
*Claim:* a router with priority 255 becomes DR as soon as it is configured. *Why it is wrong:* the DR election is not preemptive, so the current DR stays until it fails or OSPF is cleared. *Correct statement:* priority matters at election time; to force a change, clear the process (`clear ip ospf process`) after setting priorities. Similarly, 2-Way between two DROTHERs is correct and not a fault.
:::

::: lens
[CISCO · JUNIPER · NOKIA · AMAZON]{.co}

The state list and the "stuck in EXSTART/INIT/2-WAY" question are asked at all of these. Strong answers give the cause for each (MTU, one-way hello or filter, normal for DROTHERs) and a command that proves it. The LSA-types table is a near certainty at Cisco and Juniper; learn who originates each and where it floods. The reported scenario "200 routes in one area flap and SPF runs everywhere" is solved by summarisation at the ABR, stub area and throttling.
:::

::: lab
`LAB 4.5 · 30 MIN`  FRR Containerlab, three routers R1, R2, R3 in areas 1, 0, 2.

```
vtysh -c "show ip ospf database"
vtysh -c "configure terminal" -c "router ospf" -c "area 1 stub no-summary"
vtysh -c "show ip ospf database"
```

```
Summary Link States (Area 1)        <-- before: many; after: only 0.0.0.0
Type-5 AS External Link States      <-- absent in area 1 after conversion
```

**What you should notice:** the database of the stub router shrinks, and a default route appears. Then capture with Wireshark (`ospf` display filter) while you bring up a link, and match the DBD, LSR, LSU and LSAck packets to Figure 4.8.
:::

::: check
1. With the default reference bandwidth, what is the cost of a 1 Gb/s link, and why does it matter? [^c4-7]
2. Which LSA type does R1 in a totally stubby area still see besides types 1 and 2? [^c4-8]
:::

[^c4-7]: It is 1, because 100 / 1000 is rounded up to the minimum of 1; hence 1 Gb/s, 10 Gb/s and 100 Mb/s links all look equal and OSPF cannot prefer the faster one.
[^c4-8]: One type 3 LSA, the default route from the ABR.

:::
