::: {.p4}

::: pack
## Revision Spread {#rv4}

::: revision
::: top
**Ten facts.** (1) Routing decision: longest prefix, then AD, then metric. (2) STP: lowest bridge ID is root; root port = lowest path cost, then lowest sender BID, then lowest sender port ID; the root has no root port. (3) STP priority moves in steps of 4096; VLAN is added (32768 + 1 = 32769). (4) OSPF states: Down, Init, 2-Way, ExStart, Exchange, Loading, Full; stuck in ExStart means MTU. (5) OSPF DR: priority, then router ID; not pre-emptive; 224.0.0.5 and .6. (6) LSA 1 and 2 stay in the area, 3 and 4 cross ABRs, 5 is domain-wide, 7 is converted to 5. (7) BGP: TCP 179, AD 20 and 200, iBGP never re-advertises iBGP routes, next hop unchanged in iBGP. (8) Best path: **N WLLA OMNI**, then **Old Routers Clear Neighbours**. (9) HSRP preempt off, VRRP on; tracking needs preempt on the standby. (10) EF = 46, AFxy = 8x + 2y, multicast MAC = 01:00:5E + low 23 bits.

**Three figures to redraw.** The STP triangle with R, D and blocked ports (Figure 4.9); the OSPF state ladder with its stuck points (Figure 4.16); the dual-homed AS diagram with local preference outbound and prepending inbound (Figure 4.26).
:::

### Administrative distance

| Source | AD | Source | AD |
|---|---|---|---|
| Connected | 0 | RIP | 120 |
| Static | 1 | EIGRP external | 170 |
| EIGRP summary | 5 | iBGP | 200 |
| eBGP | 20 | DHCP default | 254 |
| EIGRP internal | 90 | Unusable | 255 |
| OSPF | 110 | IS-IS | 115 |

### OSPF states, LSAs and areas

| State | Meaning |
|---|---|
| Down / Init | no hello / hello heard, own ID absent |
| 2-Way | bidirectional; DR election; final for DROTHERs |
| ExStart / Exchange | master elected / DBD headers swapped (MTU) |
| Loading / Full | LSR and LSU / databases equal |

| LSA | Origin | Scope |
|---|---|---|
| 1 Router | each router | area |
| 2 Network | DR | area |
| 3 Summary | ABR | other areas |
| 4 ASBR summary | ABR | other areas |
| 5 External | ASBR | all but stub |
| 7 NSSA | ASBR in NSSA | NSSA, to 5 at ABR |

Stub: no 4, 5. Totally stubby: no 3, 4, 5. NSSA: no 4, 5; has 7. Timers 10 and 40 s (broadcast), 30 and 120 s (NBMA). Cost = reference / bandwidth, default reference 100 Mb/s. Route preference: O, O IA, E1, E2.

### BGP best path (Cisco)

0 next hop reachable. 1 weight, high. 2 local preference, high (100). 3 locally originated. 4 AS_PATH, short. 5 origin, i < e < ?. 6 MED, low, same neighbour AS. 7 eBGP over iBGP. 8 IGP metric, low. 9 multipath. 10 oldest eBGP. 11 router ID, low. 12 cluster list, short. 13 neighbour address, low.

Attributes: well-known mandatory (ORIGIN, AS_PATH, NEXT_HOP); well-known discretionary (LOCAL_PREF, ATOMIC_AGGREGATE); optional transitive (COMMUNITY, AGGREGATOR); optional non-transitive (MED, ORIGINATOR_ID, CLUSTER_LIST). Keepalive 60 s, hold 180 s. Sessions: full mesh n(n-1)/2.

### STP and EtherChannel

| 802.1D state | Time | RSTP state |
|---|---|---|
| Blocking | max age 20 s | Discarding |
| Listening | 15 s | Discarding |
| Learning | 15 s | Learning |
| Forwarding | | Forwarding |

Hello 2 s, forward delay 15 s, max age 20 s. Costs (short): 10M 100, 100M 19, 1G 4, 10G 2. Roles: root, designated, alternate, backup. PortFast and BPDU Guard on access; Root Guard on distribution downlinks; Loop Guard on non-designated uplinks. LACP active or passive, PAgP desirable or auto; passive-passive and auto-auto never form. Flags: SU in use, P bundled, s suspended, D down.

### Short notes by section

**4.1 CLI.** Three planes: management, control, data. Prompts show the mode. `copy run start` saves. Register 0x2142 skips the saved configuration (recovery). CEF = FIB + adjacency table. Say: "the control plane builds the tables; the data plane only reads them."

**4.2 VLANs.** Access untagged, trunk tagged; native untagged. Tag 4 bytes: TPID 0x8100, PCP 3, DEI 1, VID 12. ROAS hairpins; SVI routes in hardware and needs an active port. DTP: configure statically. VTP: transparent or off. Say: "a VLAN is a broadcast domain; routing is needed between them."

**4.3 STP.** Four-step election; costs 4 (1G), 2 (10G); Rapid PVST+ is the default choice; MST for many VLANs. BPDU Guard on edge, Root Guard down, Loop Guard on uplinks. EtherChannel: LACP, same speed, duplex, VLANs; one flow, one member. Say: "STP elects a root and blocks what is left."

**4.4 Routing table.** LPM, then AD, then metric. Floating static: AD above the primary. Null0 anchors summaries. Say: "the most specific route wins, whatever its source."

**4.5 OSPF.** Link-state, Dijkstra, protocol 89, 224.0.0.5 and .6. Adjacency checklist: area, subnet, timers, authentication, stub flag, MTU, unique RID. Summarise at ABRs; stub areas shrink the database. Say: "every router in an area holds the same database and runs its own SPF."

**4.6 EIGRP.** DUAL; FC: RD < FD; K1 = K3 = 1; variance only over feasible successors; stubs and summaries limit queries. Say: "a feasible successor is a loop-free backup chosen in advance."

**4.7 BGP.** Path vector over TCP 179. iBGP: next hop unchanged, no re-advertisement, full mesh or RR. LOCAL_PREF outbound; prepend, MED, communities inbound. `network` needs an exact RIB match. Say: "BGP chooses by policy first and distance second."

**4.8 FHRP.** Virtual IP and MAC; HSRP preempt off, VRRP on; track and preempt together; align with the STP root.

**4.9 Policy.** Prefix list `ge`/`le`; route-map first match, implicit deny; tag at redistribution, deny the tag back; PBR is per interface; VRF-lite = separate tables.

**4.10 MPLS.** 20 / 3 / 1 / 8; push, swap, pop; PHP; VPN label inner, transport label outer; RD unique, RT selects.

**4.11 QoS.** Mark at the edge; LLQ for voice; CBWFQ shares; WRED avoids synchronisation; policer drops, shaper delays; Tc = Bc / CIR.

**4.12 Multicast.** IGMP join; PIM-SM via RP, then SPT; RPF check; MAC 01:00:5E + 23 bits.

**4.13 Services.** NAT overload by ACL; relay with `ip helper-address`; NTP stratum; SNMPv3; syslog 0 to 7; ACL top-down, implicit deny, wildcard = inverse mask.

**4.14 Tunnels.** GRE 24 bytes, MTU 1476, recursive-routing fault; IP SLA with a tracked static route; SD-WAN separates control from edge.

### Top show commands

| Task | IOS command | What to look for |
|---|---|---|
| Interfaces | `show ip interface brief` | up/up |
| VLANs and trunks | `show vlan brief`, `show interfaces trunk` | allowed list, native VLAN |
| STP | `show spanning-tree vlan N` | root, role, state |
| EtherChannel | `show etherchannel summary` | SU, P, s |
| Routes | `show ip route`, `show ip cef N` | source, AD/metric, next hop |
| OSPF | `show ip ospf neighbor`, `... database`, `... interface` | state, LSAs, timers |
| BGP | `show ip bgp summary`, `show ip bgp N` | state/prefixes, `>`, attributes |
| FHRP | `show standby brief` | priority, state |
| MPLS | `show mpls forwarding-table`, `show bgp vpnv4 unicast all` | labels |
| QoS | `show policy-map interface` | per-class drops |
| Multicast | `show ip mroute`, `show ip igmp groups` | flags, RPF |
| Services | `show ip nat translations`, `show ntp status`, `show ip access-lists` | matches, sync |

### Other facts

| Topic | Facts |
|---|---|
| FHRP | HSRP 224.0.0.2/.102, UDP 1985, 3 s / 10 s; VRRP 224.0.0.18, proto 112; GLBP 224.0.0.102 |
| MPLS | label 20, TC 3, S 1, TTL 8; labels 0 to 3 reserved; LDP 646; RD unique, RT selects |
| QoS | EF 46, AF11 10, AF21 18, AF31 26, AF41 34, CS1 8; voice 150 ms, 30 ms, 1%; Tc = Bc / CIR |
| Multicast | 224/4, 232/8 SSM, 239/8 private; IGMPv2, v3; PIM-SM; RPF |
| Services | syslog 0 to 7: EACCEWNID; NTP stratum, UDP 123; SNMPv3 authPriv; GRE 24 bytes |

::: flash
| Q | A |
|---|---|
| Access vs trunk? | One VLAN untagged; many VLANs tagged |
| Usable VLAN IDs? | 4094 (12 bits, 0 and 4095 reserved) |
| 802.1Q tag size? | 4 bytes; frame 1522 |
| `auto` + `auto` DTP? | Access |
| ROAS drawback? | One link carries each packet twice |
| STP root? | Lowest bridge ID |
| STP priority step? | 4096 |
| Root port? | Lowest root path cost, on non-root only |
| 802.1D worst convergence? | 50 s |
| RSTP port states? | Discarding, learning, forwarding |
| Where Root Guard? | Distribution downlinks |
| LACP passive + passive? | No bundle |
| `(s)` in channel summary? | Suspended member |
| AD of OSPF, eBGP, iBGP? | 110, 20, 200 |
| Floating static? | AD above the primary route |
| /24 static vs /16 connected? | /24: longest prefix |
| OSPF protocol number? | 89 |
| Stuck in ExStart? | MTU mismatch |
| 2-Way between DROTHERs? | Normal |
| Is the DR pre-emptive? | No |
| Default OSPF reference? | 100 Mb/s: 1G = 10G = 1 |
| LSA 3 originator? | ABR |
| LSA 5 blocked in? | Stub, NSSA |
| Totally stubby gets? | Type 1, 2 and one type 3 default |
| E1 vs E2? | E1 adds internal cost; E1 preferred |
| EIGRP FC? | RD < FD |
| EIGRP K defaults? | K1 = K3 = 1 |
| EIGRP AD? | 90, 170 external |
| BGP port? | TCP 179 |
| BGP Active? | Trying to connect, not up |
| iBGP next hop? | Unchanged |
| Full mesh count? | n(n-1)/2 |
| RR loop attributes? | ORIGINATOR_ID, CLUSTER_LIST |
| Highest wins? | Weight and local preference |
| MED compared? | Same neighbour AS only |
| Inbound TE tools? | Prepend, MED, more specifics, communities |
| `network` in BGP needs? | Exact RIB match |
| `no-export`? | Not outside the AS |
| HSRP default preempt? | Off |
| VRRP owner priority? | 255 |
| `ge 16 le 24`? | Length 16 to 24 inclusive |
| Redistribution loop fix? | Tag and deny the tag |
| MPLS shim fields? | 20, 3, 1, 8 bits |
| PHP? | Penultimate router pops the label |
| RD vs RT? | Uniqueness vs import and export |
| DSCP EF? | 46, ToS 0xB8 |
| AF31? | 26 |
| Policer vs shaper? | Drops vs delays |
| Multicast MAC? | 01:00:5E + low 23 bits |
| RPF check? | Accept only from the unicast path to the source |
| GRE overhead? | 24 bytes; MTU 1476 |
:::
:::
:::

:::
