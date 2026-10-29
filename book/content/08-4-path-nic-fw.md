::: {.p8}

## [8.10]{.sec}Path and reachability tools [Must · ■■□]{.tag} {#s8-10}

A connectivity complaint is answered by a ladder of probes that each test one more layer than the last: ARP, ICMP, a TCP handshake, an application request. The tools below are the rungs. Their protocols (ICMP, TTL, path MTU, ARP) are in [3.5](#s3-5){.ref} and [3.6](#s3-6){.ref}.

**ping** sends ICMP echo requests and reports the round-trip time and loss. Useful options are `-c N` (count), `-i` (interval), `-W` (reply timeout), `-s` (payload size), and `-M do` (set the Don't-Fragment bit). Replies show `ttl`, which reveals the hop count when the sender's initial value is known (64 on Linux: a reply with ttl 63 crossed one router). `ping` proves that ICMP works on the path, nothing more: a server can answer ping with its web service down, or drop ICMP while serving traffic.

**Path MTU** is found with DF pings. The payload plus 28 bytes of IP and ICMP header must fit the MTU, so `-s 1472` fills a 1500-byte packet. With a smaller link in the path (the lab set the link towards `blue` to 1400), the router answers with ICMP "fragmentation needed", naming the limit:

```
$ ping -c1 -M do -s 1472 10.0.2.2
From 10.0.1.1 icmp_seq=1 Frag needed and DF set (mtu = 1400)
$ ping -c1 -M do -s 1372 10.0.2.2                 # 1372 + 28 = 1400
1380 bytes from 10.0.2.2: icmp_seq=1 ttl=63 time=0.046 ms
$ tracepath -n 10.0.2.2                           # discovers the same limit hop by hop
 1:  10.0.1.1                                              0.067ms
 2:  10.0.1.1                                              0.012ms pmtu 1400
 2:  10.0.2.2                                              0.027ms reached
     Resume: pmtu 1400 hops 2 back 2
```

Ordinary packets are small and work, but large transfers hang when the ICMP message is filtered: the "black hole" symptom, where a login works and a large file stalls. `tracepath` needs no root and reports `pmtu` as it learns it.

**traceroute** reveals the routers on the path by exploiting the TTL field: it sends probes with TTL 1, 2, 3, …; each router that decrements the TTL to zero discards the probe and returns ICMP *Time Exceeded*, whose source address names that hop (Figure 8.8). The last probe reaches the destination, which answers differently (an ICMP port-unreachable for UDP probes, an echo reply for ICMP probes, a SYN-ACK or RST for TCP probes), ending the trace.

<figure>
<svg viewBox="0 0 480 140" width="480"><defs><marker id="a88" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="b88" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs>
<rect class="box" x="6" y="52" width="50" height="26" rx="2"/><text class="lbl" x="31" y="69" text-anchor="middle">Host</text>
<circle class="box" cx="170" cy="65" r="14"/><path class="ln" d="M160 55 L180 75 M180 55 L160 75"/><text class="sm" x="170" y="92" text-anchor="middle">R1 10.0.1.1</text>
<circle class="box" cx="290" cy="65" r="14"/><path class="ln" d="M280 55 L300 75 M300 55 L280 75"/><text class="sm" x="290" y="92" text-anchor="middle">R2 10.0.9.1</text>
<rect class="box" x="410" y="52" width="64" height="26" rx="2"/><text class="lbl" x="442" y="69" text-anchor="middle">Destination</text>
<line class="lg" x1="56" y1="65" x2="156" y2="65"/><line class="lg" x1="184" y1="65" x2="276" y2="65"/><line class="lg" x1="304" y1="65" x2="410" y2="65"/>
<path class="ln" d="M58 14 L154 14" fill="none" marker-end="url(#a88)"/><text class="sm" x="106" y="10" text-anchor="middle">probe TTL=1</text>
<path class="ln" d="M58 26 L274 26" fill="none" marker-end="url(#a88)"/><text class="sm" x="166" y="22" text-anchor="middle">probe TTL=2</text>
<path class="ln" d="M58 38 L408 38" fill="none" marker-end="url(#a88)"/><text class="sm" x="233" y="34" text-anchor="middle">probe TTL=3</text>
<path class="acc dash" d="M156 59 L60 59" fill="none" marker-end="url(#b88)"/>
<text class="sm" x="106" y="116" text-anchor="middle">Time Exceeded from R1</text>
<text class="sm" x="290" y="116" text-anchor="middle">Time Exceeded from R2</text>
<text class="sm" x="442" y="96" text-anchor="middle">port unreachable,</text><text class="sm" x="442" y="106" text-anchor="middle">echo reply or SYN-ACK</text>
<text class="sm" x="240" y="132" text-anchor="middle">TTL reaches 0 at the router; the destination answers instead of forwarding</text>
</svg>
<figcaption><b>Figure 8.8</b> Traceroute. Each probe lives one router longer than the last; the source address of each Time Exceeded message names the hop. Reverse paths may differ from forward paths, and each hop may rate-limit its replies.</figcaption>
</figure>

Linux `traceroute` sends UDP datagrams to high, unlikely ports by default (so that the destination answers port-unreachable), while Windows `tracert` uses ICMP echo; the choice is historical, and either may be filtered. Options switch the probe type: `-I` (ICMP), `-T -p 443` (TCP SYN to port 443, which passes a firewall that allows only HTTPS), `-n` (no reverse DNS, much faster) and `-q 1` (one probe per hop). A line of `* * *` means no reply came within the timeout: the router may be configured not to send Time Exceeded, a firewall may drop the probes or the replies, or the router rate-limits ICMP. It does not mean the router is down, because traffic that is not addressed to the router itself passes through it normally.

```
$ traceroute -n -q1 10.0.2.2
 1  10.0.1.1  0.059 ms
 2  10.0.2.2  0.036 ms
```

**mtr** combines ping and traceroute: it probes every hop continuously and reports loss and latency statistics per hop, which exposes intermittent problems that one traceroute misses. The report mode is `mtr -rwnc 100 host` (report, wide, numeric, 100 cycles).

```
$ mtr -rwnc 5 10.0.2.2
HOST: vm            Loss%   Snt   Last   Avg  Best  Wrst StDev
  1.|-- 10.0.1.1     0.0%     5    1.1   0.3   0.1   1.1   0.5
  2.|-- 10.0.2.2     0.0%     5    0.1   0.1   0.1   0.2   0.0
```

The rule for reading it is that *loss counts only if it persists to the last hop*. Routers prioritise forwarding over generating ICMP, and many apply control-plane policing (CoPP) to the CPU path that builds Time Exceeded messages. A hop that shows 50 % loss while later hops show none is merely slow to answer *its own* probes; the forwarded traffic is unaffected. Real loss at hop *k* appears at hop *k* and every hop after it. The two reports below (typical shapes, not captured from the lab) show the contrast.

```
False alarm (rate limit)          Real loss from hop 3
 1 10.20.0.1    0.0%               1 10.20.0.1    0.0%
 2 10.30.0.1    0.0%               2 10.30.0.1    0.0%
 3 10.30.4.1   50.0%  <- ignore     3 10.30.4.1   12.0%  <- real
 4 10.40.1.1    0.0%               4 10.40.1.1   11.0%
 5 10.40.9.9    0.0%  <- last hop   5 10.40.9.9   12.0%  <- last hop
```

Two further cautions. Latency that jumps at a hop and stays high thereafter is real queueing or a long link (for example a sea cable); a spike at one hop only is again the router's slow ICMP path. And the forward and return paths can differ, so loss on the return path shows at the hops that carry the replies; `mtr` from both ends settles it.

**arping** tests layer 2 directly with ARP, bypassing IP routing and any ICMP filter: `arping -I eth0 10.0.1.1` prints the gateway's MAC address if it is alive on the segment. It is also the tool for detecting duplicate addresses (two replies with different MACs).

**nc (netcat)** tests a TCP or UDP port, and `curl` tests the application. `nc -zv host 443` completes a handshake and exits (`-z` no data, `-v` verbose, `-w 2` timeout); the message distinguishes the failure kinds, as the earlier capture showed.

```
$ nc -zv -w2 10.0.2.2 8080
Connection to 10.0.2.2 8080 port [tcp/http-alt] succeeded!
$ nc -zv -w2 10.0.2.2 9999
nc: connect to 10.0.2.2 port 9999 (tcp) failed: Connection refused      <- RST: host up, nothing listening
```

"Connection refused" means a reset came back (host reachable, port closed); "timed out" means silence (drop, dead host or path). `curl -v` prints the request and response headers and the connection steps, and `curl -w` prints timings that split a slow request into stages:

```
$ curl -s -o /dev/null -w 'dns=%{time_namelookup} connect=%{time_connect} tls=%{time_appconnect} start=%{time_starttransfer} total=%{time_total} code=%{http_code}\n' http://10.0.2.2:8080/
dns=0.000033 connect=0.000235 tls=0.000000 start=0.003609 total=0.004089 code=200
```

The timings are cumulative from the start: DNS finished at 0.03 ms, the TCP handshake at 0.24 ms, the first response byte at 3.6 ms (the server's think time is `start − connect`), the whole body at 4.1 ms. A large `dns` points to the resolver, a large `connect − dns` to the network round trip or a SYN drop, a large `tls − connect` to certificate or handshake costs, a large `start − tls` to the application, and a large `total − start` to the transfer.

::: trap
*Claim:* "Loss shown in the middle of an mtr report means a router is dropping my traffic." *Why it is wrong:* the percentage counts only unanswered probes to that router's own control plane, which is rate limited. *Correct statement:* trust loss only if it continues to the final hop. Likewise `* * *` in traceroute is a missing reply, not a dead router, and `ping` working does not show that TCP port 443 or the application works.
:::

::: lens
[CISCO · JUNIPER · ARISTA · AMAZON · GOOGLE]{.co}

"Explain traceroute", "mtr shows loss at hop 3 but not at the end" and "traceroute through a firewall that only allows 443" are near-universal. A strong answer states the TTL and Time Exceeded mechanism, the UDP, ICMP and TCP probe types and why `-T -p 443` passes a port-443 filter, the rate-limiting rule for intermediate hops, and asymmetric paths. Follow-ups: ECMP making different probes take different paths (Paris traceroute keeps the flow tuple fixed), and MPLS hops that hide or reveal labels. The solved forms are Q8.10 and Q8.11.
:::

::: check
1. A DF ping of 1472 bytes fails and 1372 succeeds. What is the path MTU? [^c810-1]
2. Which message does `nc` print for a closed port, and which for a filtered one? [^c810-2]
:::

[^c810-1]: Between 1400 and 1499 bytes: a packet of 1372 + 28 = 1400 fits and one of 1500 does not. The router's "mtu = 1400" message gives the exact value.
[^c810-2]: Closed: "Connection refused" (a RST). Filtered or dead: a timeout, with no message from the network.

## [8.11]{.sec}Link layer and NIC health: ethtool, ip -s link, nstat [Should · ■□□]{.tag} {#s8-11}

A large share of "network" problems are physical: a bad cable, a speed or duplex mismatch, a failing transceiver, a full receive ring. `ethtool` talks to the NIC driver and reports what the hardware negotiated and counted. The analogy is a mechanic's diagnostic plug: the counters are the odometer, cumulative since the device came up, so one reads a *rate*, not a total.

| Command | Reports |
|---|---|
| `ethtool eth0` | link detected, speed, duplex, auto-negotiation, supported modes |
| `ethtool -S eth0` | driver counters: `rx_crc_errors`, `rx_missed`, `tx_dropped`, per-queue statistics |
| `ethtool -i eth0` | driver name, version, firmware, bus address |
| `ethtool -k eth0` | offload features on or off (TSO, GSO, GRO, checksums) |
| `ethtool -g eth0` | ring buffer sizes, current and maximum |
| `ethtool -a eth0` | pause-frame (flow-control) settings |
| `ethtool -m eth0` | transceiver (SFP) optical power and temperature, if supported |
| `ip -s link show eth0` | generic RX/TX packets, errors, drops, overruns |
| `cat /proc/net/dev` | the same counters for every interface, plain text |
| `nstat -az` | protocol counters: `TcpRetransSegs`, `IpInDiscards`, `TcpExtListenDrops` |

```
$ ethtool eth0 | grep -E 'Speed|Duplex|Auto|Link'
	Speed: 1000Mb/s
	Duplex: Full
	Auto-negotiation: on
	Link detected: yes
$ ethtool -g eth0 | sed -n 2,13p
Pre-set maximums:
RX:			256
TX:			256
Current hardware settings:
RX:			256
TX:			256
$ ethtool -k eth0 | grep -E '^(tcp-seg|generic-seg|generic-rec)'
tcp-segmentation-offload: on
generic-segmentation-offload: on
generic-receive-offload: on
```

(The 1000 Mb/s block is the usual output of a physical NIC; the virtual NIC of the book's lab VM reports `Speed: Unknown!` because it has no medium. The ring and offload lines above are real output from it.) The first line to check on a suspect port is the negotiated speed and duplex: a link that negotiates 100 Mb/s half-duplex on a gigabit port points to a damaged cable or an auto-negotiation mismatch (one side forced, the other automatic: the automatic side falls back to half-duplex), and half-duplex produces *late collisions* and CRC errors under load. In that case the repair is a new cable or both ends set to auto.

**Counters need two snapshots.** A counter such as `rx_crc_errors 5000` says nothing alone; it may have grown during a fault last month. The method is to read twice and divide the difference by the interval (rate = Δcounter / Δtime).

```
$ ip -s link show eth0 | awk '/RX:/{getline; a=$3} END{print a}'; sleep 10; ip -s link show eth0 | awk '/RX:/{getline; b=$3} END{print b}'
311919
312190
```

Here 271 packets arrived in 10 s, 27 packets per second. The same two-snapshot approach applied to `rx_crc_errors` or to the `errors` column separates "errors since boot" from "errors now". In the generic counters, `errors` are damaged frames (CRC, length, alignment: physical), `dropped` means the host discarded frames (ring full, no buffer, filter), and `overruns` or `missed` mean the NIC had no free descriptor: the CPU did not drain the ring fast enough. A rising `rx_missed` with a small ring is the case for `ethtool -G eth0 rx 4096` or for spreading interrupts across queues ([7.12](#s7-12){.ref}).

**Offloads and capture.** TSO lets the kernel pass a large TCP buffer (up to 64 KB) to the NIC, which cuts it into MSS-sized segments with correct headers and checksums; GSO does the same in software when the NIC cannot; GRO merges consecutive received segments of one flow before the stack sees them, saving per-packet cost. One 64 KB buffer becomes about 45 wire segments of 1448 bytes (65 536 / 1448 ≈ 45). These features explain why a capture taken *on the host* shows super-sized packets and unverified checksums, whereas a capture on a mirror port or another machine shows the real wire frames. For protocol debugging one turns them off temporarily: `ethtool -K eth0 tso off gso off gro off`.

::: trap
*Claim:* "5,000 CRC errors, so the link is bad." *Why it is wrong:* counters are cumulative since the device started or was cleared. *Correct statement:* take two readings and compare the rate; a link is bad if errors increase while traffic flows, and the cure is confirmed when the rate falls to zero.
:::

::: check
1. A gigabit port negotiated 100 Mb/s half-duplex and shows late collisions. Likely cause? [^c811-1]
2. Why does tcpdump on a sender show a 64 KB segment on a 1500-MTU link? [^c811-2]
:::

[^c811-1]: A damaged cable (only two pairs working) or a duplex mismatch from forced settings on one side.
[^c811-2]: The tap sees the buffer before TSO/GSO splits it; the wire carries 1448-byte segments.

## [8.12]{.sec}Netfilter: iptables and nftables [Must · ■■□]{.tag} {#s8-12}

*Netfilter* is the packet-filtering framework inside the Linux kernel. It defines *hooks*, fixed points on a packet's path, at which registered rules may accept, drop, modify or redirect it. `iptables` and `nftables` are two user-space front-ends to the same hooks; `ufw` and `firewalld` are friendlier front-ends over them. Connection-tracking state, address translation and filtering all live here, which is why the framework underlies host firewalls, NAT gateways, Docker and Kubernetes networking. The concepts of NAT and ACLs are taught in [3.6](#s3-6){.ref} and [Pillar 9](#ch9){.ref}; this section teaches the Linux mechanism.

A packet entering the host passes **PREROUTING**; the routing decision then decides whether it is for this host (**INPUT**, then the local process) or for forwarding (**FORWARD**). A locally generated packet passes **OUTPUT**. Everything leaving the host passes **POSTROUTING** (Figure 8.9). Hence the answers to the standard questions: a packet *routed through* the box traverses PREROUTING, FORWARD, POSTROUTING; a packet *for* the box traverses PREROUTING and INPUT.

<figure>
<svg viewBox="0 0 480 190" width="480"><defs><marker id="a89" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="b89" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs>
<text class="sm" x="2" y="14">packet in</text>
<rect class="box" x="10" y="20" width="100" height="50" rx="2"/><text class="lbl" x="60" y="36" text-anchor="middle">PREROUTING</text><text class="sm" x="60" y="48" text-anchor="middle">raw · mangle · nat</text><text class="sm" x="60" y="60" text-anchor="middle">(DNAT, conntrack)</text>
<path class="acc" d="M110 45 L128 45" fill="none" marker-end="url(#b89)"/>
<path class="box" d="M128 45 L168 25 L208 45 L168 65 Z"/><text class="sm" x="168" y="43" text-anchor="middle">routing</text><text class="sm" x="168" y="52" text-anchor="middle">decision</text>
<path class="acc" d="M208 45 L236 45" fill="none" marker-end="url(#b89)"/><text class="sm" x="222" y="38" text-anchor="middle">transit</text>
<rect class="box" x="236" y="20" width="96" height="50" rx="2"/><text class="lbl" x="284" y="40" text-anchor="middle">FORWARD</text><text class="sm" x="284" y="54" text-anchor="middle">mangle · filter</text>
<path class="acc" d="M332 45 L350 45" fill="none" marker-end="url(#b89)"/>
<rect class="box" x="350" y="20" width="96" height="50" rx="2"/><text class="lbl" x="398" y="36" text-anchor="middle">POSTROUTING</text><text class="sm" x="398" y="48" text-anchor="middle">mangle · nat</text><text class="sm" x="398" y="60" text-anchor="middle">(SNAT, MASQ)</text>
<path class="ln" d="M446 45 L474 45" fill="none" marker-end="url(#a89)"/><text class="sm" x="458" y="38" text-anchor="middle">out</text>
<path class="ln" d="M168 65 L168 100" fill="none" marker-end="url(#a89)"/><text class="sm" x="174" y="86">for this host</text>
<rect class="box" x="118" y="100" width="100" height="50" rx="2"/><text class="lbl" x="168" y="120" text-anchor="middle">INPUT</text><text class="sm" x="168" y="134" text-anchor="middle">mangle · filter</text>
<path class="ln" d="M218 125 L246 125" fill="none" marker-end="url(#a89)"/>
<rect class="fill" x="246" y="100" width="86" height="50" rx="2" stroke="#1A1D23" stroke-width="0.8"/><text class="lbl" x="289" y="128" text-anchor="middle">local process</text>
<path class="ln" d="M332 125 L350 125" fill="none" marker-end="url(#a89)"/>
<rect class="box" x="350" y="100" width="96" height="50" rx="2"/><text class="lbl" x="398" y="116" text-anchor="middle">OUTPUT</text><text class="sm" x="398" y="128" text-anchor="middle">raw · mangle</text><text class="sm" x="398" y="140" text-anchor="middle">nat · filter</text>
<path class="ln" d="M398 100 L398 72" fill="none" marker-end="url(#a89)"/>
<text class="sm" x="240" y="176" text-anchor="middle">table order within a hook: raw, mangle, nat, filter. Highlighted path: a packet routed through the box.</text>
</svg>
<figcaption><b>Figure 8.9</b> The netfilter path, simplified. Boxes are hooks with the tables registered there; the diamond is the routing decision. Transit traffic crosses PREROUTING, FORWARD and POSTROUTING; local traffic enters through INPUT and leaves through OUTPUT and POSTROUTING.</figcaption>
</figure>

**Tables and targets.** In iptables, rules live in *tables* by purpose: `filter` (accept or drop: the default), `nat` (address translation), `mangle` (header changes, marks), `raw` (exempt from connection tracking). Each table has some of the *chains* above. A chain is an ordered list of rules; a packet is compared with the rules *in order*, the first match decides, and if none matches the chain's *policy* (ACCEPT or DROP) applies. A rule's target is `ACCEPT`, `DROP` (discard silently), `REJECT` (discard and send an error), `LOG` (write a log line and continue), `DNAT`, `SNAT` and `MASQUERADE` (translation), or a jump to another chain.

**Connection tracking.** The kernel's *conntrack* module records each flow, and rules can match its state: `NEW` (first packet), `ESTABLISHED` (traffic in both directions seen), `RELATED` (new flow tied to an existing one: an ICMP error, an FTP data channel) and `INVALID`. This allows a *stateful* firewall: accept replies to connections the host started, and judge only new connections. The rule `-m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT` is placed first, for two reasons: nearly all packets match it, so it is also the fastest path, and it permits return traffic without opening any inbound port.

::: example
**A host firewall for a Campus Net server.** Policy: replies are allowed; SSH only from the campus range 10.0.0.0/8; HTTPS from anywhere; everything else dropped, with a rate-limited log.

1. Set the default policy to DROP on INPUT, after making sure that the SSH session will survive: the ESTABLISHED rule comes first.
2. Accept loopback, so that local services can talk to each other.
3. Add the SSH and HTTPS rules, then the logging rule, which sits last so that only unmatched packets are logged.

```
iptables -P INPUT DROP
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -p tcp -s 10.0.0.0/8 --dport 22  -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
iptables -A INPUT -m limit --limit 5/min -j LOG --log-prefix "campus-fw drop: "
```

```
$ iptables -L INPUT -n -v --line-numbers          # after one ping and one SSH-port attempt from 10.0.1.2
Chain INPUT (policy DROP 1 packets, 84 bytes)
num   pkts bytes target     prot opt in     out     source               destination
1        0     0 ACCEPT     0    --  *      *       0.0.0.0/0            0.0.0.0/0            ctstate RELATED,ESTABLISHED
2        0     0 ACCEPT     0    --  lo     *       0.0.0.0/0            0.0.0.0/0
3        1    60 ACCEPT     6    --  *      *       10.0.0.0/8           0.0.0.0/0            tcp dpt:22
4        0     0 ACCEPT     6    --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:443
5        1    84 LOG        0    --  *      *       0.0.0.0/0            0.0.0.0/0            limit: avg 5/min burst 5 LOG
```

[Result: the packet counters prove which rule matched: the SSH SYN (60 bytes) hit rule 3, and the ping (84 bytes) fell through to the LOG rule and then to the DROP policy. If a rule has zero hits when traffic should match it, an earlier rule is taking the packets.]{.result}
:::

The usual mistakes are all about order. A broad `DROP` placed above a specific `ACCEPT` makes the later rule dead; the counters then stay at zero, which is how one finds it. Rules are inserted at a position with `-I INPUT 3`, deleted with `-D INPUT 3`, and the whole set is dumped or restored with `iptables-save` and `iptables-restore`. A change made at the shell is lost at reboot until saved by the distribution's mechanism (`netfilter-persistent`).

**DROP versus REJECT.** With `DROP` the sender receives nothing and retransmits until its timeout (the SYN retries seen in [8.7](#s8-7){.ref}), so a legitimate client waits a long time for the failure while a scanner is slowed down. With `REJECT` the sender at once receives a TCP RST (or ICMP port-unreachable for UDP) and fails fast, "connection refused". Neither is "more secure": inside a trusted network REJECT gives faster diagnosis and avoids hanging applications; on an Internet-facing interface DROP gives away less to scanners.

**NAT.** Source NAT rewrites the source of outgoing packets; `MASQUERADE` is SNAT that takes the address of the outgoing interface, the right choice when that address is dynamic. Destination NAT rewrites the destination of incoming packets to expose an internal service. Conntrack remembers the translation, so replies are translated back automatically. The theory of PAT is in [3.6](#s3-6){.ref}.

```
iptables -t nat -A POSTROUTING -s 10.0.1.0/24 -o rt-eth1 -j MASQUERADE
iptables -t nat -A PREROUTING -i rt-eth0 -p tcp --dport 8081 -j DNAT --to-destination 10.0.2.2:8080
```

```
$ conntrack -L                                    # the translation is stored with both directions
tcp 6 116 SYN_SENT src=10.0.1.2 dst=10.0.1.1 sport=58188 dport=8081 [UNREPLIED] src=10.0.2.2 dst=10.0.2.1 sport=8080 dport=58188
```

In that line the first tuple is the original packet (client to the router's port 8081) and the second is the expected reply (server 10.0.2.2:8080 to the translated source). The flow stayed `[UNREPLIED]` in the experiment because the destination host had a firewall that accepted port 8080 only from 10.0.1.0/24, and MASQUERADE had changed the client's apparent address to the router's 10.0.2.1: a NAT gateway changes the source seen by every firewall behind it, so those rules must be written for the translated address. Forwarding also requires `net.ipv4.ip_forward=1` ([8.5](#s8-5){.ref}).

### nftables

*nftables* is the successor to iptables, with one tool (`nft`), one syntax for IPv4, IPv6 and other families (`inet` covers both), sets and maps that match many addresses in a single rule, and atomic loading of a whole ruleset. A rule set has *tables* containing *chains*, which are attached to a hook with a `type`, `hook` and `priority`. The bastion-host rule set below does what the iptables example did, with the campus range held in a set, and loads in one step.

```
table inet campus_fw {
  set mgmt { type ipv4_addr; flags interval; elements = { 10.0.1.0/24 } }
  chain input {
    type filter hook input priority 0; policy drop;
    ct state established,related accept
    ct state invalid drop
    iif "lo" accept
    ip protocol icmp icmp type { echo-request, destination-unreachable, time-exceeded } limit rate 10/second accept
    ip saddr @mgmt tcp dport 8080 accept          # management service from the set only
    tcp dport 443 accept
    counter limit rate 5/minute log prefix "campus-fw drop: "
  }
}
```

```
$ nft -f bastion.nft && nft list chain inet campus_fw input | tail -3     # after a probe to the closed port 9999
		tcp dport 443 accept
		counter packets 3 bytes 180 limit rate 5/minute burst 5 packets log prefix "campus-fw drop: "
```

The counter before the `limit` counts every packet that reaches the end of the chain (here three SYN retries to port 9999), while the log is limited to five a minute and the policy drops them. The ruleset is shown by `nft list ruleset`, and the iptables-to-nftables translation is mechanical:

| Task | iptables | nftables |
|---|---|---|
| Allow replies | `-m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT` | `ct state established,related accept` |
| Allow SSH from a range | `-p tcp -s 10.0.0.0/8 --dport 22 -j ACCEPT` | `ip saddr 10.0.0.0/8 tcp dport 22 accept` |
| Several ports | `-m multiport --dports 80,443 -j ACCEPT` | `tcp dport { 80, 443 } accept` |
| Default drop | `iptables -P INPUT DROP` | `policy drop;` in the chain definition |
| Masquerade | `-t nat -A POSTROUTING -o eth0 -j MASQUERADE` | `oifname "eth0" masquerade` in a `nat` chain |
| DNAT | `-t nat -A PREROUTING -p tcp --dport 8081 -j DNAT --to 10.0.2.2:8080` | `tcp dport 8081 dnat to 10.0.2.2:8080` |
| List with counters | `iptables -L -n -v --line-numbers` | `nft list ruleset` (counters if declared) |
| Save / load | `iptables-save` / `iptables-restore` | `nft list ruleset > f` / `nft -f f` |

A bastion rule set follows from this pattern: default-drop INPUT, ESTABLISHED/RELATED first, loopback, SSH from the management set, ICMP limited to the types needed for path MTU discovery and diagnostics, and a rate-limited log. The ICMP types matter: dropping all ICMP breaks path MTU discovery ([8.10](#s8-10){.ref}).

::: trap
*Claim:* "I added the ACCEPT rule, so it works." *Why it is wrong:* rules are evaluated top to bottom and the first match wins; an earlier DROP, or the packet counters showing zero, proves the rule is never reached. *Correct statement:* check order with `--line-numbers` and the pkts column, and test with the real traffic. Further, mixing `iptables` and `nft` on the same host can leave two rule sets competing at the same hook.
:::

::: lab
`LAB 8.7 · 40 MIN` Firewall builder. In the three-namespace lab of [8.5](#s8-5){.ref}, run a web server in `blue` on port 8080 and apply the bastion rule set to `blue`. Test a matrix of flows from `red`: TCP 8080, TCP 9999, ping, and the same after `iptables -t nat -A POSTROUTING -o rt-eth1 -j MASQUERADE` in `rtr`.

**What you should notice:** 8080 succeeds from the management range and fails once masquerading changes the source; 9999 hangs (silent drop) and the counter rises; ping is allowed by the ICMP rule. Capture with `tcpdump` on both sides of `rtr` to watch the translated source address appear.
:::

::: check
1. Which chains does a packet forwarded through a Linux router traverse? [^c812-1]
2. Why is the ESTABLISHED,RELATED rule first? [^c812-2]
:::

[^c812-1]: PREROUTING, FORWARD and POSTROUTING.
[^c812-2]: Most packets belong to existing flows, so it is the fastest path, and it allows replies without opening inbound ports.

:::
