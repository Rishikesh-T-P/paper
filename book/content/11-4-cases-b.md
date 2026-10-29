::: {.p11}

### Case 7 · OSPF neighbour never appears [Must · ■□□]{.tag} {#c11-7}

[L3 · CISCO · JUNIPER · NOKIA]{.where}

**Prompt.** "R3 and R4 are directly connected and pingable, but no OSPF neighbour forms."

<figure>
<svg viewBox="0 0 480 110" width="480">
<line class="acc" x1="130" y1="40" x2="350" y2="40"/>
<text class="sm" x="179" y="36" text-anchor="middle">Gi0/0 10.0.34.1</text>
<text class="sm" x="315" y="36" text-anchor="middle">Gi0/0 .2</text>
<circle class="box" cx="130" cy="40" r="13"/><path class="ln" d="M123,40 L137,40 M130,33 L130,47 M125,35 L135,45 M125,45 L135,35"/>
<text class="lbl" x="130" y="66" text-anchor="middle">R3</text>
<text class="sm" x="130" y="75" text-anchor="middle">area 0, MD5</text>
<circle class="box" cx="350" cy="40" r="13"/><path class="ln" d="M343,40 L357,40 M350,33 L350,47 M345,35 L355,45 M345,45 L355,35"/><circle class="acc" cx="350" cy="40" r="16"/>
<text class="lbl" x="350" y="66" text-anchor="middle">R4</text>
<text class="sm" x="350" y="75" text-anchor="middle">area 1, passive</text>
<text class="sm" x="240" y="98" text-anchor="middle">pingable, but no neighbour state at all</text>
</svg>
<figcaption><b>Figure 11.15</b> Case 7. Three independent mismatches are stacked on one link.</figcaption>
</figure>

| We ask | The interviewer answers |
|----------------------|--------------------------------------------|
| Any neighbour state at all? | None; not even Init |
| What changed? | R4 is new |
| Authentication? | Yes, MD5 on R3 |

**Hypotheses, ranked.** The *adjacency must-match list* is the hypothesis list: same subnet and mask; same area ID; same hello and dead timers; same authentication type and key; same stub flags; compatible network types; unique router IDs; interface not passive; nothing blocking 224.0.0.5 and 224.0.0.6.

| Layer | Command | Decisive output | Inference |
|----|-----------------|----------------------------|--------------------------|
| L3 | `show ip ospf interface Gi0/0` on R4 | `No Hellos (Passive interface)`; `Area 1` | R4 sends no hellos, and is in the wrong area |
| L3 | the same on R3 | `Area 0`, `Hello 10, Dead 40`, MD5 | R3 expects area 0 with authentication |
| L3 | after `no passive-interface`: R3 log | `Received invalid packet: mismatch area ID` | Second fault exposed |
| L3 | after correcting the area: R3 log | `Mismatch Authentication type. Input packet specified type 0, we use type 2` | Third fault exposed |

The exact wording of these messages varies a little between releases; the pattern is the point.


**Root cause.** Three stacked faults: a passive interface, area 1 where area 0 is required, and no authentication on R4. The lesson is to fix one, re-test, and not to stop at the first finding.

**Fix.** `no passive-interface Gi0/0`; `network 10.0.34.0 0.0.0.255 area 0`; `ip ospf authentication message-digest` and `ip ospf message-digest-key 1 md5 <key>`.

**Verify.** `show ip ospf neighbor` shows Full; the remote prefixes are in the table.

**Prevent.** Generate both ends of every link from one source of truth.

| The interviewer asks | A strong answer |
|-------------------|--------------------------------------|
| Which parameters need not match? | Process ID, priority, cost and interface names. |
| Junos equivalent? | `show ospf interface detail` and `show ospf neighbor`. |
| Why do network types matter? | Defaults differ between broadcast (10 and 40 s) and non-broadcast (30 and 120 s), so a mismatch appears as a timer mismatch. |

**Variant.** The key identifier differs, although both ends use MD5: the log shows an authentication failure, not a type mismatch.

### Case 8 · BGP session stuck in Active [Must · ■■□]{.tag} {#c11-8}

[L3 · L4 · AMAZON · GOOGLE · CISCO · JUNIPER · ARISTA · NOKIA · MICROSOFT]{.where}

**Prompt.** "Our eBGP session to the ISP is stuck in Active."

<figure>
<svg viewBox="0 0 480 125" width="480">
<line class="acc" x1="120" y1="40" x2="360" y2="40"/>
<text class="sm" x="157" y="36" text-anchor="middle">192.0.2.2</text>
<text class="sm" x="323" y="36" text-anchor="middle">192.0.2.1</text>
<circle class="box" cx="120" cy="40" r="13"/><path class="ln" d="M113,40 L127,40 M120,33 L120,47 M115,35 L125,45 M115,45 L125,35"/><circle class="acc" cx="120" cy="40" r="16"/>
<text class="lbl" x="120" y="66" text-anchor="middle">BR1</text>
<text class="sm" x="120" y="75" text-anchor="middle">Lo0 172.16.255.1</text>
<circle class="box" cx="360" cy="40" r="13"/><path class="ln" d="M353,40 L367,40 M360,33 L360,47 M355,35 L365,45 M355,45 L365,35"/>
<text class="lbl" x="360" y="66" text-anchor="middle">ISP-A PE</text>
<text class="sm" x="360" y="75" text-anchor="middle">AS 100</text>
<text class="sm acct" x="120" y="100" text-anchor="middle">neighbor 192.0.2.1 update-source Lo0</text>
<text class="sm acct" x="120" y="111" text-anchor="middle">EDGE-IN: permit icmp, permit tcp established</text>
<text class="sm" x="360" y="100" text-anchor="middle">expects peer 192.0.2.2</text>
</svg>
<figcaption><b>Figure 11.16</b> Case 8. BR1 sources the session from its loopback while the provider expects the WAN address, and an edge ACL blocks inbound SYNs.</figcaption>
</figure>

| We ask | The interviewer answers |
|----------------------|--------------------------------------------|
| Did it ever work? | No, it is a new circuit |
| Which addresses do the two sides use? | We use Loopback0; the ISP expects 192.0.2.2 |
| Any filtering? | An edge ACL on the WAN interface |
| Who configured what? | Both sides are configured |

**Hypotheses, ranked.** (1) update-source or neighbour address mismatch; (2) TCP 179 blocked by an ACL; (3) eBGP TTL 1 with a loopback (needs `ebgp-multihop`); (4) AS or MD5 mismatch (these show NOTIFICATION messages, not Active).

| Layer | Command | Decisive output | Inference |
|----|-----------------|----------------------------|--------------------------|
| L4 | `show ip bgp summary` | `192.0.2.1  4  100  0  0  ...  never  Active` | TCP connection attempts are failing |
| L3 | `ping 192.0.2.1 source Loopback0` | `.....` | The ISP has no route back to our loopback |
| L3 | `ping 192.0.2.1` | `!!!!!` | The link itself works |
| L4 | `telnet 192.0.2.1 179 /source-interface Gi0/1` | `Open` | From the WAN address the port opens |
| L4 | `show access-lists EDGE-IN` | `30 deny ip any any (87 matches)` | The ISP's SYNs are hitting the deny |


**Root cause.** Two faults: BR1 originates the session from Loopback0 although the provider peers with the WAN address, and the edge ACL permits only established TCP and ICMP, so the ISP's SYN to port 179 is dropped. BGP's session rules are in [§4.7](#s4-7){.ref}.

**Fix.** Remove `update-source Loopback0`, or agree loopback peering with the ISP (plus `ebgp-multihop` and a static route). Insert `permit tcp host 192.0.2.1 host 192.0.2.2 eq bgp` and the reverse before the deny.

**Verify.** `show ip bgp summary` shows a number in the last column; `show ip bgp neighbors 192.0.2.1 | include state` shows Established; routes enter the table.

**Prevent.** An edge-ACL template with a BGP peer object group, and a pre-turn-up checklist.

| The interviewer asks | A strong answer |
|-------------------|--------------------------------------|
| Name the BGP states. | Idle, Connect, Active, OpenSent, OpenConfirm, Established. |
| How does Idle (admin) differ from Active? | Idle (admin) is shut down by configuration; Active is an attempt that fails. |
| What does eBGP to a loopback need? | TTL above 1 (`ebgp-multihop 2` or `disable-connected-check`) and a route to both loopbacks. |

**Variant.** The state flaps between Active and Idle with "bad AS" in the log: a `remote-as` mismatch, shown as a NOTIFICATION.

::: lens
[AMAZON · GOOGLE · JUNIPER]{.co}

Candidates report BGP state definitions being probed directly. Answer Active precisely (connect failing), then give the three checks: address, filter, TTL. Expect: "what would you see if the AS number were wrong?"
:::

### Case 9 · BGP up, but a prefix is not advertised or installed [Must · ■■□]{.tag} {#c11-9}

[L3 · AMAZON · GOOGLE · ARISTA · JUNIPER · NOKIA · MICROSOFT]{.where}

**Prompt.** "BGP is up, but the ISP says it does not receive our 198.51.100.0/24, and internally R5 learns a route but does not use it."

<figure>
<svg viewBox="0 0 480 120" width="480">
<line class="ln" x1="90" y1="40" x2="250" y2="40"/>
<line class="ln" x1="250" y1="40" x2="410" y2="40"/>
<text class="sm" x="287" y="36" text-anchor="middle">192.0.2.2</text>
<text class="sm" x="373" y="36" text-anchor="middle">192.0.2.1</text>
<circle class="box" cx="90" cy="40" r="13"/><path class="ln" d="M83,40 L97,40 M90,33 L90,47 M85,35 L95,45 M85,45 L95,35"/>
<text class="lbl" x="90" y="66" text-anchor="middle">R5</text>
<text class="sm" x="90" y="75" text-anchor="middle">iBGP</text>
<circle class="box" cx="250" cy="40" r="13"/><path class="ln" d="M243,40 L257,40 M250,33 L250,47 M245,35 L255,45 M245,45 L255,35"/><circle class="acc" cx="250" cy="40" r="16"/>
<text class="lbl" x="250" y="66" text-anchor="middle">BR1</text>
<text class="sm" x="250" y="75" text-anchor="middle">AS 65000</text>
<circle class="box" cx="410" cy="40" r="13"/><path class="ln" d="M403,40 L417,40 M410,33 L410,47 M405,35 L415,45 M405,45 L415,35"/>
<text class="lbl" x="410" y="66" text-anchor="middle">ISP-A PE</text>
<text class="sm" x="410" y="75" text-anchor="middle">AS 100</text>
<text class="sm acct" x="250" y="98" text-anchor="middle">RIB holds 198.51.100.0/25 and /26, no /24</text>
<text class="sm" x="90" y="98" text-anchor="middle">next hop 192.0.2.1 unknown</text>
</svg>
<figcaption><b>Figure 11.17</b> Case 9. BR1 owns only two subnets of the /24, and R5 cannot reach the eBGP next hop.</figcaption>
</figure>

| We ask | The interviewer answers |
|----------------------|--------------------------------------------|
| Is the prefix in our table exactly? | "We have subnets of it" |
| Any outbound policy? | A route map, TO-ISP |
| iBGP design? | Full mesh, no `next-hop-self` |

**Hypotheses, ranked.** (1) a `network` statement needs an *exact* match in the routing table; (2) outbound policy filters the route; (3) the iBGP next hop is unreachable; (4) the ISP filters by IRR or RPKI.

| Layer | Command | Decisive output | Inference |
|----|-----------------|----------------------------|--------------------------|
| L3 | `show ip route 198.51.100.0 255.255.255.0` | `% Network not in table` | No exact /24 to originate |
| L3 | `show ip bgp neighbors 192.0.2.1 advertised-routes` | empty | Nothing is sent |
| L3 | `show ip bgp 8.8.8.0` on R5 | `192.0.2.1 (inaccessible) from 10.255.0.1` | The next hop is unusable |
| L3 | `show ip route 192.0.2.1` on R5 | `% Network not in table` | The IGP does not carry the WAN link |


**Root cause.** Two faults: the `network` statement needs the exact /24 in the routing table but only the /25 and /26 exist; and iBGP passes the eBGP next hop unchanged, which R5 cannot reach ([§4.7](#s4-7){.ref}).

**Fix.** `ip route 198.51.100.0 255.255.255.0 Null0` (an anchor route) or `aggregate-address`; then `neighbor <R5> next-hop-self` on BR1.

**Verify.** The /24 appears in `advertised-routes`, the ISP confirms, and the R5 route shows the best-path marker `>`.

**Prevent.** An origination checklist, and a registered RPKI route origin authorisation for the /24.

| The interviewer asks | A strong answer |
|-------------------|--------------------------------------|
| What is the best-path order? | Weight, local preference, locally originated, AS-path length, origin, MED, eBGP over iBGP, IGP metric to the next hop, then tie-breakers ([§4.7](#s4-7){.ref}). |
| How do you resend routes without dropping the session? | `clear ip bgp <peer> soft out`. |
| Why might the ISP drop a /25? | Providers commonly filter prefixes longer than /24. |

**Variant.** The prefix is advertised but the provider marks it RPKI-invalid because no route origin authorisation exists.

### Case 10 · One server drops for a minute, several times an hour [Must · ■■□]{.tag} {#c11-10}

[L2 · L3 · CISCO · AMAZON · GOOGLE]{.where}

**Prompt.** "The finance server randomly becomes unreachable for 30 to 60 seconds, several times an hour."

<figure>
<svg viewBox="0 0 480 135" width="480">
<line class="ln" x1="45" y1="55" x2="170" y2="55"/>
<line class="ln" x1="170" y1="55" x2="320" y2="25"/>
<line class="acc" x1="170" y1="55" x2="320" y2="100"/>
<text class="sm" x="284" y="28" text-anchor="middle">Gi1/0/12</text>
<text class="sm" x="284" y="85" text-anchor="middle">Gi1/0/33</text>
<rect class="box" x="30" y="45" width="30" height="20" rx="1"/><path class="ln" d="M37,69 L53,69"/><rect class="fill" x="34" y="49" width="22" height="11"/>
<text class="lbl" x="45" y="81" text-anchor="middle">Clients</text>
<rect class="box" x="148" y="44" width="44" height="22" rx="2"/><path class="ln" d="M157,52 L183,52 M179,49 L183,52 L179,55 M183,59 L157,59 M161,56 L157,59 L161,62"/>
<text class="lbl" x="170" y="79" text-anchor="middle">SW1</text>
<rect class="box" x="306" y="10" width="28" height="30" rx="1"/><path class="ln" d="M306,20 L334,20 M306,30 L334,30"/><circle class="accf" cx="328" cy="15" r="1.2" style="fill:#1A1D23"/>
<text class="lbl" x="320" y="53" text-anchor="middle">Finance server</text>
<text class="sm" x="320" y="62" text-anchor="middle">10.1.50.20</text>
<rect class="box" x="305" y="90" width="30" height="20" rx="1"/><path class="ln" d="M312,114 L328,114"/><rect class="fill" x="309" y="94" width="22" height="11"/><rect class="acc" x="302" y="87" width="36" height="26" rx="3"/>
<text class="lbl" x="320" y="126" text-anchor="middle">Lab VM</text>
<text class="sm" x="320" y="135" text-anchor="middle">10.1.50.20 static</text>
<text class="sm" x="430" y="60" text-anchor="middle">VLAN 50</text>
<text class="sm" x="430" y="70" text-anchor="middle">10.1.50.0/24</text>
</svg>
<figcaption><b>Figure 11.18</b> Case 10. A lab VM was given the finance server's static address.</figcaption>
</figure>

| We ask | The interviewer answers |
|----------------------|--------------------------------------------|
| All clients or some? | Some at a time |
| Pattern? | Random |
| What does the server log? | Nothing |
| Any change? | New VMs in VLAN 50 last week |

**Hypotheses, ranked.** (1) duplicate IP address; (2) MAC flapping from a loop; (3) NIC-teaming misconfiguration; (4) ARP cache problems.

| Layer | Command | Decisive output | Inference |
|----|-----------------|----------------------------|--------------------------|
| L3 | switch log | `%IP-4-DUPADDR: Duplicate address 10.1.50.20 on Vlan50, sourced by 0050.56aa.bbbb` | Another device uses the address |
| L2 | `show ip arp 10.1.50.20`, repeated | The MAC alternates between two values | Clients' caches flip |
| L2 | `show mac address-table address 0050.56aa.bbbb` | `Gi1/0/33` | The intruder is on the hypervisor port |
| L2 | `arping -D -I eth0 10.1.50.20` | `Unicast reply from 10.1.50.20 [00:50:56:AA:BB:BB]` | A second MAC answers for the address |


**Root cause.** A duplicate IP address: ARP caches on clients alternate between the two MACs, so the server is reachable only while a client holds the right entry (ARP is in [§3.6](#s3-6){.ref}).

**Fix.** Re-address the VM, `clear arp-cache`, and reserve the address in IPAM and the DHCP exclusion list.

**Verify.** ARP stays stable and no `DUPADDR` message appears for an hour.

**Prevent.** IPAM, DHCP snooping with IP source guard, dynamic ARP inspection, and gratuitous-ARP conflict detection on servers.

| The interviewer asks | A strong answer |
|-------------------|--------------------------------------|
| How does a MAC flap differ from an ARP flap? | A MAC flap is one MAC seen on two ports (loop, mis-teamed NIC); an ARP flap is one IP resolving to two MACs (duplicate). |
| What else looks the same? | An HSRP split-brain, where both routers are active; `show standby` shows it. |
| How do you find the intruder? | The OUI identifies the vendor; `show mac address-table address <mac>` names the port. |

**Variant.** A NIC team configured active-active without a LAG makes the server's own MAC flap between ports.

### Case 11 · A whole floor went down when someone plugged in a switch [Must · ■■□]{.tag} {#c11-11}

[L2 · CISCO · JUNIPER · NOKIA · ARISTA]{.where}

**Prompt.** "At 11:05 the entire third floor lost network; the switch CPUs are at 100 per cent and the LEDs flash wildly."

<figure>
<svg viewBox="0 0 480 168" width="480">
<line class="ln" x1="240" y1="32" x2="130" y2="100"/>
<line class="ln" x1="240" y1="32" x2="40" y2="100"/>
<rect class="box" x="218" y="21" width="44" height="22" rx="2"/><path class="ln" d="M227,29 L253,29 M249,26 L253,29 L249,32 M253,36 L227,36 M231,33 L227,36 L231,39"/>
<text class="lbl" x="240" y="13" text-anchor="middle">Distribution</text>
<rect class="box" x="108" y="89" width="44" height="22" rx="2"/><path class="ln" d="M117,97 L143,97 M139,94 L143,97 L139,100 M143,104 L117,104 M121,101 L117,104 L121,107"/>
<text class="lbl" x="130" y="124" text-anchor="middle">SW3A</text>
<text class="sm" x="130" y="133" text-anchor="middle">Rapid PVST+</text>
<rect class="box" x="18" y="89" width="44" height="22" rx="2"/><path class="ln" d="M27,97 L53,97 M49,94 L53,97 L49,100 M53,104 L27,104 M31,101 L27,104 L31,107"/>
<text class="lbl" x="40" y="124" text-anchor="middle">SW3B</text>
<rect class="box" x="328" y="89" width="44" height="22" rx="2"/><path class="ln" d="M337,97 L363,97 M359,94 L363,97 L359,100 M363,104 L337,104 M341,101 L337,104 L341,107"/><rect class="acc" x="325" y="86" width="50" height="28" rx="3"/>
<text class="lbl" x="350" y="124" text-anchor="middle">Cheap switch</text>
<text class="sm" x="350" y="133" text-anchor="middle">unmanaged</text>
<text class="sm acct" x="240" y="160" text-anchor="middle">both cable ends in SW3A wall ports; BPDU filter on</text>
<line class="acc" x1="152" y1="95" x2="328" y2="95"/><line class="acc" x1="152" y1="106" x2="328" y2="106"/><text class="sm" x="240" y="90" text-anchor="middle">Gi1/0/14</text><text class="sm" x="240" y="118" text-anchor="middle">Gi1/0/15</text>
</svg>
<figcaption><b>Figure 11.19</b> Case 11. A cheap switch has a cable looped between two wall ports of SW3A; BPDU filter makes spanning tree blind.</figcaption>
</figure>

| We ask | The interviewer answers |
|----------------------|--------------------------------------------|
| Whole floor or building? | Floor |
| Any change? | "Nothing", then, when asked about desk moves: a desk move this morning |
| What does monitoring show? | Broadcast at 100 per cent of the link |
| Is spanning tree on? | Yes, Rapid PVST+, with PortFast on edge ports |

**Hypotheses, ranked.** (1) a Layer 2 loop and broadcast storm; (2) spanning tree disabled or bypassed on the ports; (3) root-bridge change; (4) a unidirectional link.

| Layer | Command | Decisive output | Inference |
|----|-----------------|----------------------------|--------------------------|
| L2 | `show interfaces Gi1/0/14`, rate lines | `5 minute input rate 912345000 bits/sec` | A storm on these ports |
| L2 | switch log | `%SW_MATM-4-MACFLAP_NOTIF: Host 0050.7966.6801 in vlan 10 is flapping between port Gi1/0/14 and port Gi1/0/15` | The same MACs appear on both ports: a loop |
| L2 | `show spanning-tree interface Gi1/0/14 detail` | `Bpdu filter is enabled`; `BPDU: sent 0, received 0` | Spanning tree is blind on these ports |
| L1 | `show processes cpu sorted` | `CPU utilization for five seconds: 99%` | The control plane is saturated |


**Mitigate first.** `shutdown` on Gi1/0/14, then confirm the rates fall.

**Root cause.** A physical loop on edge ports where BPDU filter disabled loop detection; with PortFast alone, the port would receive its own BPDUs and block within about two seconds ([§4.3](#s4-3){.ref}). No BPDU Guard or storm control existed as a backstop, and Ethernet frames have no TTL, so they circulate indefinitely.

**Fix.** Remove the loop and the BPDU filter from access ports; `spanning-tree portfast bpduguard default`; `storm-control broadcast level 1.00`; an errdisable recovery policy; Loop Guard on uplinks.

**Verify.** Broadcast rates and CPU return to normal and MAC flaps stop.

**Prevent.** An access-port template with BPDU Guard and storm control, broadcast-rate alerts, physical security of wall ports, 802.1X. The post-mortem for this case is in [§11.7](#s11-7){.ref}.

| The interviewer asks | A strong answer |
|-------------------|--------------------------------------|
| Why do Ethernet frames loop for ever? | The Ethernet header has no TTL, so nothing removes a frame from a loop. |
| What does Root Guard do? | It stops a port from accepting a superior BPDU, so an edge switch cannot take over as root. |
| How does RSTP converge? | A proposal and agreement handshake on point-to-point links, in under a second. |

**Variant.** The *global* `spanning-tree portfast bpdufilter default` is safer than the per-port form, because ports lose the filter when a BPDU arrives.

::: lens
[CISCO · JUNIPER · ARISTA]{.co}

A mitigation test: the interviewer waits to see whether the candidate shuts the port before explaining the theory. Say the mitigation first, then the cause, then the template change. Expect: "why did spanning tree not stop it?"
:::

### Case 12 · New VLAN's clients get 169.254 addresses [Must · ■□□]{.tag} {#c11-12}

[L2 · L3 · L7 · CISCO · AMAZON · JUNIPER]{.where}

**Prompt.** "Laptops in the new lab VLAN 60 get 169.254 addresses."

<figure>
<svg viewBox="0 0 480 125" width="480">
<line class="ln" x1="40" y1="45" x2="140" y2="45"/>
<line class="acc" x1="140" y1="45" x2="270" y2="45"/>
<line class="ln" x1="270" y1="45" x2="410" y2="45"/>
<text class="sm" x="226" y="41" text-anchor="middle">Gi1/0/48</text>
<rect class="box" x="25" y="35" width="30" height="20" rx="1"/><path class="ln" d="M32,59 L48,59"/><rect class="fill" x="29" y="39" width="22" height="11"/>
<text class="lbl" x="40" y="71" text-anchor="middle">Laptop</text>
<text class="sm" x="40" y="80" text-anchor="middle">VLAN 60</text>
<rect class="box" x="118" y="34" width="44" height="22" rx="2"/><path class="ln" d="M127,42 L153,42 M149,39 L153,42 L149,45 M153,49 L127,49 M131,46 L127,49 L131,52"/>
<text class="lbl" x="140" y="69" text-anchor="middle">ASW</text>
<text class="sm" x="140" y="78" text-anchor="middle">DHCP snooping</text>
<rect class="box" x="248" y="34" width="44" height="22" rx="2"/><path class="ln" d="M257,42 L283,42 M279,39 L283,42 L279,45 M283,49 L257,49 M261,46 L257,49 L261,52"/><rect class="acc" x="245" y="31" width="50" height="28" rx="3"/>
<text class="lbl" x="270" y="69" text-anchor="middle">Core</text>
<text class="sm" x="270" y="78" text-anchor="middle">Vlan60 10.1.60.1</text>
<rect class="box" x="396" y="30" width="28" height="30" rx="1"/><path class="ln" d="M396,40 L424,40 M396,50 L424,50"/><circle class="accf" cx="418" cy="35" r="1.2" style="fill:#1A1D23"/>
<text class="lbl" x="410" y="73" text-anchor="middle">DHCP server</text>
<text class="sm" x="410" y="82" text-anchor="middle">10.1.99.10</text>
<text class="sm acct" x="270" y="108" text-anchor="middle">no ip helper-address; uplink untrusted</text>
</svg>
<figcaption><b>Figure 11.20</b> Case 12. The SVI has no relay, and the access switch distrusts the uplink on which offers return.</figcaption>
</figure>

| We ask | The interviewer answers |
|----------------------|--------------------------------------------|
| Only VLAN 60? | Yes |
| Does a static address work? | Yes, so Layers 2 and 3 are fine |
| Does a scope exist for VLAN 60? | Yes |
| Is DHCP snooping on? | Yes, on the access layer |

**Hypotheses, ranked.** (1) no relay on the SVI; (2) the scope is missing or exhausted; (3) snooping drops server replies on an untrusted uplink; (4) option 82 trouble.

| Layer | Command | Decisive output | Inference |
|----|-----------------|----------------------------|--------------------------|
| L7 | `ipconfig` on a laptop | `Autoconfiguration IPv4 Address: 169.254.37.8` | No lease was obtained |
| L7 | `tcpdump -ni eth0 port 67 or port 68` | Only `BOOTP/DHCP, Request from ...` | Discovers are sent; no offer returns |
| L3 | `show running-config interface vlan 60` | no `ip helper-address` | Nothing forwards the broadcast to the server |
| L2 | after the helper is added: `show ip dhcp snooping statistics` | `Packets Dropped From untrusted ports = 14` | Offers are discarded at the uplink |
| L2 | `show ip dhcp snooping` | `Gi1/0/48  no` (trust) | The uplink is untrusted |


**Root cause.** Two faults: the SVI has no DHCP relay, and the access switch treats its uplink as untrusted, so the offers that return from the server are dropped. A client without a lease assigns itself an address in 169.254.0.0/16 ([§3.6](#s3-6){.ref}).

**Fix.** `ip helper-address 10.1.99.10` on Vlan60; `ip dhcp snooping trust` on the uplink; check the server scope for 10.1.60.0/24.

**Verify.** The four steps of DHCP (Discover, Offer, Request, Acknowledge) appear in a capture, the client holds a lease, and `show ip dhcp snooping binding` lists it.

**Prevent.** The VLAN provisioning playbook includes the relay and ends with a check that a test client obtains a lease.

| The interviewer asks | A strong answer |
|-------------------|--------------------------------------|
| How does the server pick the scope? | From the relay address (giaddr) in the request. |
| Which DHCP steps are broadcast? | Discover and, before the address is held, Request; the relay converts them to unicast. |
| What is the option 82 risk? | Snooping inserts it; some servers drop requests that carry it with giaddr zero. |

**Variant.** *Exhaustion.* A late arrival gets 169.254 while others work: `show ip dhcp pool` shows no free addresses. Shorten the lease, enlarge the scope and reclaim stale bindings.

:::
