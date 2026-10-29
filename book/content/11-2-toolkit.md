::: {.p11}

## [11.5]{.sec}Layer command matrix and reading outputs [Must · ■■□]{.tag} {#s11-5}

::: bigidea
A command is only evidence once you know what a healthy output looks like, because the same number can be normal on one link and a fault on another.
:::

[**Blood report** — the reference range matters more than the raw number; a CRC count of 40 means nothing until you know whether it was 40 a minute ago.]{.margin}The matrix lists, for each layer, the question to settle and the two or three commands that settle it on Cisco IOS XE, Junos and Linux. The mechanisms behind each command are in their home chapters ([switching](#s4-2){.ref}, [OSPF](#s4-5){.ref}, [BGP](#s4-7){.ref}), and the Linux tools are taught in [Pillar 8](#ch8){.ref}. Arista EOS and NX-OS accept the IOS forms used here with small differences.

| Layer | Cisco IOS XE | Junos | Linux |
|-----|------------------------------|-----------------------|------------------------------|
| **L1** Link up, clean, speed and duplex | `show interfaces`, `show interfaces status`, `show interfaces transceiver` | `show interfaces extensive`, `show interfaces diagnostics optics` | `ethtool eth0`, `ethtool -S eth0`, `ip -s link` |
| **L2** MAC, VLAN, trunk, loop | `show mac address-table`, `show vlan brief`, `show interfaces trunk`, `show spanning-tree`, `show etherchannel summary` | `show ethernet-switching table`, `show vlans`, `show spanning-tree bridge`, `show lacp interfaces` | `ip neigh`, `bridge fdb show`, `bridge vlan`, `ip -d link` |
| **L3** Address, neighbour, route, path | `show ip interface brief`, `show ip arp`, `show ip route X`, `show ip ospf neighbor`, `show ip bgp summary`, `ping X source Y`, `traceroute X` | `show interfaces terse`, `show arp`, `show route X`, `show ospf neighbor`, `show bgp summary`, `ping X source Y` | `ip addr`, `ip route get X`, `ip neigh`, `ping -I eth0 X`, `traceroute -n X`, `mtr -rwzbc 100 X` |
| **L4** Port, policy, state | `show access-lists`, `show ip nat translations`, `show policy-map control-plane` | `show firewall filter`, `show security flow session` | `ss -tulpn`, `ss -ti`, `conntrack -L`, `nft list ruleset`, `nc -zv X 443` |
| **L7** Name, handshake, service | `show ip dhcp binding`, `show ip dhcp snooping` | `show dhcp server binding` | `dig X`, `curl -v URL`, `openssl s_client -connect X:443`, `journalctl -u svc` |
| **Any** On the wire | `monitor capture` (embedded packet capture) | `monitor traffic interface ge-0/0/0` | `tcpdump -ni eth0 'host X and port Y'` |

### Reading interface counters

Counters on an interface are cumulative since the last clear, so a figure is meaningful only as a *delta*: take two snapshots ten seconds apart and subtract. The pair below contrasts a healthy port with a port on a bad cable; the lines to read are the speed and duplex, and the error counters.

```
Healthy
Gi1/0/10 is up, line protocol is up
  Full-duplex, 1000Mb/s
  0 input errors, 0 CRC, 0 frame
  0 output errors, 0 collisions

Faulty (cable or optic)
Gi1/0/10 is up, line protocol is up
  Full-duplex, 1000Mb/s
  2217 input errors, 2217 CRC, 0 frame
  0 output errors, 0 collisions
```

| Counter | Reads as | Usual cause |
|--------------|------------------------|------------------------------|
| CRC, input errors rising | Frames corrupted on the wire | Bad cable, dirty or weak optic, duplex mismatch (on the full-duplex side) |
| Runts | Frames under 64 bytes | Collisions, duplex mismatch |
| Giants | Frames above the interface MTU | MTU or jumbo mismatch, tag overhead |
| Late collisions | Collision after the 64th byte | Half-duplex port facing a full-duplex peer; cable too long |
| Output drops | Egress queue overflowed | Congestion, microbursts |
| Resets, carrier transitions | Link flapped | Cable, optic, remote reboot |

### Reading trunks, neighbours and sessions

On a trunk, `show interfaces trunk` prints three lists, and the *difference* between them is the diagnosis: a VLAN that is allowed but not active is missing from the VLAN database, and one that is active but not forwarding is blocked by spanning tree or pruning.

```
Vlans allowed on trunk              : 1,10,20          healthy, VLAN 20 present
Vlans allowed and active            : 1,10,20
Vlans in spanning tree forwarding   : 1,10,20

Vlans allowed on trunk              : 10               faulty: list was replaced
```

Two more pairs are worth memorising, since they are the commonest outputs shown in case rounds. The OSPF pair shows the state and the dead timer; the BGP pair shows that the last column is a *state* while the session is down and a *prefix count* once it is up.

```
R1# show ip ospf neighbor                  healthy
Neighbor ID  Pri  State      Dead Time  Address    Interface
2.2.2.2        1  FULL/DR    00:00:36   10.0.12.2  Gi0/2

R1# show ip ospf neighbor                  stuck
2.2.2.2        1  EXSTART/DR 00:00:34   10.0.12.2  Gi0/2

R1# show ip bgp summary                    healthy
Neighbor     V   AS  MsgRcvd MsgSent  Up/Down   State/PfxRcd
192.0.2.1    4  100     5120    4871  3d02h             812

R1# show ip bgp summary                    down
192.0.2.1    4  100        0       0  never          Active
```

The routing protocols have state machines, taught in [§4.5](#s4-5){.ref} and [§4.7](#s4-7){.ref}; what matters when troubleshooting is *where a session sticks*, since each stuck state points to a different class of fault.

| Protocol state | Stuck here means | First test |
|---------------|------------------------------|------------------------|
| OSPF Down or Init | Hellos do not arrive, or are one-way (ACL, multicast, passive interface) | `show ip ospf interface`, `debug ip ospf hello` |
| OSPF 2-Way | Normal between DROthers on a broadcast segment | none needed |
| OSPF ExStart or Exchange | DBD exchange fails, usually an MTU mismatch | `show interfaces`, MTU line, on both ends |
| OSPF Loading | LSRs not answered, packets lost | Check MTU, authentication, loss |
| BGP Idle | Administratively down, or no route to the peer | `show ip bgp neighbors`, `show ip route peer` |
| BGP Active | TCP connection attempts fail (not "active" in the usual sense) | Ping and `telnet peer 179` from the same source; ACL |
| BGP OpenSent | Open sent, no valid reply: AS or parameters mismatch | Logs: NOTIFICATION |
| BGP Established with a number | The number is the prefixes received; the session is healthy | `show ip bgp neighbors X advertised-routes` |

### Reading Linux evidence

On a Linux host, three outputs carry most of the diagnosis. The pair for `ss -ti` shows a healthy long-haul connection and the window-limited one of [Case 17](#c11-17){.ref}; the `ping` pair shows a path-MTU black hole ([Case 5](#c11-5){.ref}); the last block shows `ip -s link`, where errors and drops are deltas to be read twice.

```
ss -ti   healthy
 cubic wscale:7,7 rto:284 rtt:81/4 cwnd:640 bytes_retrans:0
ss -ti   window-limited, retransmitting
 cubic rto:284 rtt:81/4 cwnd:10 bytes_retrans:182520 retrans:0/127

ping -M do -s 1372 10.10.5.20    healthy at the path MTU
1380 bytes from 10.10.5.20: icmp_seq=1 ttl=62 time=21.4 ms
ping -M do -s 1472 10.10.5.20    black hole: no reply and no error
--- 10.10.5.20 ping statistics --- 3 packets transmitted, 0 received

ip -s link show eth0
    RX: bytes packets errors dropped  missed  mcast
    8812770112 6120331  2217      40       0   1203
```

### Reading ping, traceroute and Linux socket output

| Symbol or text | Meaning |
|---------------|--------------------------------------------------|
| IOS ping `!` | Reply received |
| IOS ping `.` | Timeout: dropped, or no return route |
| IOS ping `U` | ICMP unreachable received from a router on the path |
| IOS ping `M` | Packet needed fragmentation and DF was set |
| traceroute `*` | No reply for that probe (filtered, or rate-limited); not a fault by itself |
| traceroute `!H`, `!N`, `!A` | Host, network unreachable, or administratively prohibited |
| `ss -ti` field `retrans` | Retransmitted segments on that connection |
| `ss -ti` field `wscale` | Window-scale factors negotiated; absent means a 64 KB window limit |
| `ip -s link` `dropped`, `errors` | Interface-level loss, as deltas |

::: trap
*Claim:* "The counter shows 3,000 errors, so the link is bad." *Why it is wrong:* the counter is cumulative and may have grown a year ago; and `mtr` loss at a middle hop is often a router rate-limiting its own ICMP replies. *Correct statement:* take deltas, and count only loss that persists to the destination.
:::

::: trap
*Claim:* "`debug all` will show me the problem." *Why it is wrong:* on a busy router it can exhaust the CPU and cut the session. *Correct statement:* use a targeted debug (for example `debug ip ospf adj`) with a condition, or a filtered capture, inside a change window, and switch it off with `undebug all`.
:::

::: check
1. Which command shows whether a VLAN is blocked by spanning tree on a trunk? [^c11-5a]
2. What does an OSPF neighbour in 2-Way on a broadcast segment mean? [^c11-5b]
:::

[^c11-5a]: `show interfaces trunk`: compare "allowed and active" with "in spanning tree forwarding state".
[^c11-5b]: It is normal for two DROthers, which do not become fully adjacent with each other; only the DR and BDR form Full adjacencies.

## [11.6]{.sec}Symptom look-alikes [Must · ■■□]{.tag} {#s11-6}

::: bigidea
Precise words for the symptom point at different faults, because a timeout, a refusal and a reset are produced by different devices behaving in different ways.
:::

[**Phone calls** — "nobody picked up" is a timeout, "the number does not exist" is a refusal, and "the call dropped" is a reset.]{.margin}Interviewers often supply a loose word and wait to see whether the candidate sharpens it. The table fixes the vocabulary; the three ladders show what each of the first three looks like in a capture.

| Observed | On the wire | Means | First test |
|--------------|----------------------|------------------------------|-------------------|
| Timeout | SYN retransmitted, nothing returns | Packet dropped on the path: ACL, firewall DROP, no route, dead link | Capture at both ends; see where it stops |
| Connection refused | SYN answered by RST | Host reached; nothing listens, or a firewall REJECTs | `ss -tlnp` on the server |
| Reset mid-stream | Established, then RST | Idle timer in a middlebox, application crash, lost state | Who sent the RST (TTL, MAC) |
| ICMP unreachable | ICMP type 3, codes 0, 1, 3, 13 | No route, no ARP answer, UDP port closed, filtered | Read the code and the sender |
| Loss | Gaps, retransmissions | Errors, congestion, rate limiting | `mtr` to the destination, counters as deltas |
| Latency | Constant high RTT | Distance, queueing, a detour | `ping`, `mtr` per hop |
| Jitter | RTT varies | Queueing, ECMP members of unequal quality, wireless | `ping -i 0.2 -c 100` |
| Low throughput | Window or loss limited | Small window, loss, shaping | `iperf3`, `ss -ti` |
| By IP only | Name lookups fail | DNS server, DHCP option, filter on port 53 | `dig @server name` |
| One direction only | Request seen, reply absent | Asymmetric route, ACL, NAT, uRPF | Captures at both ends |
| Intermittent | Pattern in time | Duplicate IP, flapping link, one bad ECMP member, lease expiry | Correlate with logs |

<figure>
<svg viewBox="0 0 480 170" width="480"><defs><marker id="ld1" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="#1A1D23"/></marker><marker id="ld2" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" style="fill:var(--accent)"/></marker></defs>
<text class="lbl" x="75" y="12" text-anchor="middle">Timeout</text>
<line class="lg" x1="20" y1="26" x2="20" y2="160"/><line class="lg" x1="130" y1="26" x2="130" y2="160"/>
<text class="sm" x="20" y="23" text-anchor="middle">client</text><text class="sm" x="130" y="23" text-anchor="middle">server</text>
<line class="ln" x1="20" y1="40" x2="130" y2="50" marker-end="url(#ld1)"/><text class="sm" x="75" y="39" text-anchor="middle">SYN t=0</text>
<line class="ln" x1="20" y1="66" x2="130" y2="76" marker-end="url(#ld1)"/><text class="sm" x="75" y="65" text-anchor="middle">SYN t=1 s</text>
<line class="ln" x1="20" y1="92" x2="130" y2="102" marker-end="url(#ld1)"/><text class="sm" x="75" y="91" text-anchor="middle">SYN t=3 s</text>
<text class="sm" x="75" y="128" text-anchor="middle">no reply: drop on path</text>
<text class="lbl" x="235" y="12" text-anchor="middle">Refused</text>
<line class="lg" x1="180" y1="26" x2="180" y2="160"/><line class="lg" x1="290" y1="26" x2="290" y2="160"/>
<text class="sm" x="180" y="23" text-anchor="middle">client</text><text class="sm" x="290" y="23" text-anchor="middle">server</text>
<line class="ln" x1="180" y1="40" x2="290" y2="50" marker-end="url(#ld1)"/><text class="sm" x="235" y="39" text-anchor="middle">SYN</text>
<line class="acc" x1="290" y1="70" x2="180" y2="80" marker-end="url(#ld2)"/><text class="sm" x="235" y="69" text-anchor="middle">RST, ACK</text>
<text class="sm" x="235" y="113" text-anchor="middle">host reached,</text>
<text class="sm" x="235" y="125" text-anchor="middle">no listener or REJECT</text>
<text class="lbl" x="395" y="12" text-anchor="middle">Reset mid-stream</text>
<line class="lg" x1="340" y1="26" x2="340" y2="160"/><line class="lg" x1="450" y1="26" x2="450" y2="160"/>
<text class="sm" x="340" y="23" text-anchor="middle">client</text><text class="sm" x="450" y="23" text-anchor="middle">server</text>
<line class="ln" x1="340" y1="40" x2="450" y2="50" marker-end="url(#ld1)"/><text class="sm" x="395" y="39" text-anchor="middle">SYN</text>
<line class="ln" x1="450" y1="62" x2="340" y2="72" marker-end="url(#ld1)"/><text class="sm" x="395" y="61" text-anchor="middle">SYN, ACK</text>
<line class="ln" x1="340" y1="84" x2="450" y2="94" marker-end="url(#ld1)"/><text class="sm" x="395" y="83" text-anchor="middle">ACK, data</text>
<text class="sm" x="395" y="111" text-anchor="middle">idle 300 s</text>
<line class="ln" x1="340" y1="126" x2="450" y2="136" marker-end="url(#ld1)"/><text class="sm" x="395" y="125" text-anchor="middle">data</text>
<line class="acc" x1="450" y1="150" x2="340" y2="160" marker-end="url(#ld2)"/><text class="sm" x="395" y="149" text-anchor="middle">RST (middlebox)</text>
</svg>
<figcaption><b>Figure 11.7</b> Three ladders. In a timeout the sender hears nothing; in a refusal the server answers at once with a reset; in a mid-stream reset a device that lost the state answers later data with a reset.</figcaption>
</figure>

```
# 1 Timeout: SYN retransmitted at 1 s and 3 s, never answered
10:01:00.000 IP 10.0.1.5.51312 > 10.0.2.10.8080: Flags [S], seq 1001
10:01:01.003 IP 10.0.1.5.51312 > 10.0.2.10.8080: Flags [S], seq 1001
10:01:03.011 IP 10.0.1.5.51312 > 10.0.2.10.8080: Flags [S], seq 1001
# 2 Refused: reset within a millisecond
10:02:00.000 IP 10.0.1.5.51320 > 10.0.2.10.8080: Flags [S], seq 2001
10:02:00.001 IP 10.0.2.10.8080 > 10.0.1.5.51320: Flags [R.], ack 2002
# 3 Reset after 300 s of silence: a middlebox forgot the session
10:08:01.220 IP 10.0.2.10.443 > 10.0.1.5.51400: Flags [R.], seq 5102
```

The excerpts support three inferences. In the first, the server never sees the SYN or its answer never returns; moving the capture to the server's interface decides which. In the second, the server host is alive and reachable, and the question moves to the listener or a REJECT rule. In the third, the interval of exactly five minutes is the clue: it matches an idle timer, and keepalives shorter than that timer remove the symptom.

The table below pairs the commonest first sentences of a complaint with their first suspect and the case in this chapter that works it through.

| Symptom sentence | First suspect | Case |
|---------------------------|-----------------------------|------|
| Works by IP, not by name | DNS server or DHCP option 6 | [1](#c11-1){.ref} |
| Only large transfers hang | MTU, blocked ICMP | [5](#c11-5){.ref} |
| One direction only, random sessions | Asymmetric path through stateful firewalls | [13](#c11-13){.ref} |
| Blips every few minutes | Duplicate IP, flapping | [10](#c11-10){.ref} |
| Bulk transfer slow, interactive fine | Duplex mismatch, loss | [4](#c11-4){.ref} |
| Slow for some users, always the same ones | One ECMP or LAG member | [14](#c11-14){.ref} |
| Single flow slow, parallel flows fine | Window-limited | [17](#c11-17){.ref} |
| 169.254.x.x address | No DHCP reply | [12](#c11-12){.ref} |
| Whole floor, LEDs flashing | Layer 2 loop | [11](#c11-11){.ref} |
| Neighbour stuck in ExStart | MTU mismatch | [6](#c11-6){.ref} |
| BGP stuck in Active | TCP 179 cannot open | [8](#c11-8){.ref} |
| Tunnel up, no traffic | Selectors, NAT exemption | [15](#c11-15){.ref} |
| Refused then timeout | Listener, then filters | [16](#c11-16){.ref} |
| Loss at one traceroute hop only | Control-plane rate limit | [18](#c11-18){.ref} |

::: check
1. A TCP SYN is answered by an immediate RST. Is the firewall dropping it? [^c11-6a]
2. Why do reset-after-idle failures appear at exactly the same interval? [^c11-6b]
:::

[^c11-6a]: No. A drop produces silence; a RST means a host or a REJECT rule answered, so the path is intact.
[^c11-6b]: A stateful device removes idle sessions after a fixed timer, and the next packet is reset.

## [11.7]{.sec}Incident overlay and post-mortems [Should · ■■□]{.tag} {#s11-7}

::: bigidea
In a live outage, restoring service comes before finding the cause, because every minute of diagnosis with users down is a minute of avoidable impact.
:::

[**Fire brigade** — put out the fire first, then look for the short circuit.]{.margin}When the prompt says "production is down", the order changes from SCALPEL's: *mitigate, communicate, diagnose, fix, review*. Mitigation is any action that restores service without needing the root cause: roll back the last change, fail over to the standby, drain the faulty member, or disable the new feature. If a change was made ten minutes before the outage, rolling it back is faster and safer than reasoning about it, and the evidence is still available afterwards from logs and saved outputs.

<figure>
<svg viewBox="0 0 480 100" width="480"><defs><marker id="in1" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="#1A1D23"/></marker></defs>
<rect class="fill" x="8" y="10" width="80" height="34" rx="2"/><text class="lbl" x="48" y="25" text-anchor="middle">Detect</text><text class="sm" x="48" y="37" text-anchor="middle">alert or call</text>
<line class="ln" x1="88" y1="27" x2="102" y2="27" marker-end="url(#in1)"/>
<rect class="box" x="102" y="10" width="80" height="34" rx="2"/><rect class="acc" x="102" y="10" width="80" height="34" rx="2"/><text class="lbl" x="142" y="25" text-anchor="middle">Mitigate</text><text class="sm" x="142" y="37" text-anchor="middle">roll back, fail over, drain</text>
<line class="ln" x1="182" y1="27" x2="196" y2="27" marker-end="url(#in1)"/>
<rect class="fill" x="196" y="10" width="80" height="34" rx="2"/><text class="lbl" x="236" y="25" text-anchor="middle">Diagnose</text><text class="sm" x="236" y="37" text-anchor="middle">SCALPEL</text>
<line class="ln" x1="276" y1="27" x2="290" y2="27" marker-end="url(#in1)"/>
<rect class="fill" x="290" y="10" width="80" height="34" rx="2"/><text class="lbl" x="330" y="25" text-anchor="middle">Fix</text><text class="sm" x="330" y="37" text-anchor="middle">permanent change</text>
<line class="ln" x1="370" y1="27" x2="384" y2="27" marker-end="url(#in1)"/>
<rect class="fill" x="384" y="10" width="80" height="34" rx="2"/><text class="lbl" x="424" y="25" text-anchor="middle">Review</text><text class="sm" x="424" y="37" text-anchor="middle">blameless post-mortem</text>
<line class="ln" x1="8" y1="62" x2="472" y2="62"/><line class="ln" x1="8" y1="58" x2="8" y2="66"/><line class="ln" x1="472" y1="58" x2="472" y2="66"/>
<text class="sm" x="240" y="76" text-anchor="middle">Communicate throughout: first update within 10 minutes, then at a fixed cadence (every 30 minutes for Sev 1)</text>
<text class="sm" x="102" y="94" text-anchor="middle">minutes</text><text class="sm" x="290" y="94" text-anchor="middle">hours</text><text class="sm" x="430" y="94" text-anchor="middle">days</text></svg>
<figcaption><b>Figure 11.8</b> The incident overlay. Mitigation is the accent step; communication runs in parallel with every phase.</figcaption>
</figure>

| Mitigation | Use when | Evidence to save first |
|---------------|----------------------------|--------------------------|
| Roll back the change | An outage follows a change within minutes | Configuration, logs and counters before the rollback |
| Fail over to the standby | A redundant path or device is healthy | State of both devices |
| Drain or shut the faulty member | One link, optic or node harms a share of flows | Counters of the member |
| Disable the new feature | A feature, not the platform, is implicated | The feature's configuration |
| Rate-limit or shed load | Overload, not a fault | Utilisation graphs |

Severity sets how often stakeholders are updated and who is woken.

| Severity | Definition | Example | Update cadence |
|-----|----------------------------|-------------------------|------------|
| Sev 1 | Widespread loss of a critical service | Campus core down; every VLAN affected | Every 30 minutes |
| Sev 2 | Major degradation or one site down | A floor lost, ISP-A down with ISP-B carrying | Every hour |
| Sev 3 | Limited impact with a workaround | One VLAN slow | Daily |
| Sev 4 | Cosmetic or no user impact | Alarm threshold needs tuning | At closure |

Four roles are named at once in a serious incident: an *incident commander* who decides and does not type commands, an *operator* who runs them, a *scribe* who keeps the timeline, and a *communications lead* who updates stakeholders. In an interview, naming these roles scores as maturity; saying "I would do everything myself" does not.

::: example
**Three incident messages.** A good message states impact, action, and the time of the next update, and nothing speculative. The wording below is for the floor outage of Case 11.

| Message | Text |
|-------|----------------------------------------------------------|
| First update (10 minutes) | "11:12. The third floor has no network. About 180 users are affected. We suspect a Layer 2 loop and are isolating ports. Next update at 11:40." |
| Progress update | "11:30. The suspected ports are shut and traffic on the floor is recovering. We are verifying each VLAN. Next update at 12:00." |
| Resolution | "11:48. Service is restored since 11:31. The cause was a cable loop on edge ports. A review will be circulated within three working days." |
:::

::: example
**A blameless post-mortem for Case 11.** The template has seven parts; the filled version is below, abridged.

| Part | Content |
|------|----------------------------------------------------------|
| Summary | 11:05 to 11:31, the third floor (about 180 users) lost network. |
| Timeline | 11:05 loop forms after a desk move; 11:07 helpdesk calls; 11:09 broadcast alarm on SW3A; 11:12 incident declared Sev 1; 11:18 MAC-flap logs name Gi1/0/14 and Gi1/0/15; 11:20 both ports shut (mitigation); 11:31 all services normal. |
| Impact | About 26 minutes of no network on one floor; no data loss. |
| Root cause | A physical loop on edge ports where BPDU filter hid the loop from spanning tree. |
| Contributing factors | The access-port template had BPDU filter but no BPDU Guard or storm control; no alert on broadcast rate; desk moves without a ticket. |
| What went well | The MAC-flap log named the ports at once; the shut-down was quick. |
| Action items | Template change (network engineering, two weeks); storm control and broadcast alert (monitoring, one week); disable unused wall ports (facilities, one month). |
:::

The post-mortem names *systems*, not people. "A user plugged a cable in" is a trigger; the root cause is that the design allowed one cable to take down a floor, and that is what the action items fix. The same structure answers behavioural questions: the timeline is the situation, the mitigation your action, and the action items the result, which is how the incident stories of [Pillar 12](#ch12){.ref} are built for Amazon's Ownership, Dive Deep and Bias for Action principles.

::: trap
*Claim:* "The root cause was human error." *Why it is wrong:* people make errors at a steady rate, so a cause that stops at a person guarantees a repeat. *Correct statement:* the root cause is the missing guard that let an ordinary error become an outage.
:::

::: check
1. A change was made ten minutes before a Sev 1 outage. What is the first action? [^c11-7a]
2. Which role does the incident commander not perform? [^c11-7b]
:::

[^c11-7a]: Roll the change back, after saving the current state and logs for the post-mortem.
[^c11-7b]: Typing commands; the commander decides and coordinates while the operator acts.

:::
