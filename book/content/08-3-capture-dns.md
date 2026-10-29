::: {.p8}

## [8.7]{.sec}Packet capture I: tcpdump [Must · ■■□]{.tag} {#s8-7}

`tcpdump` copies packets from the kernel and prints one line per packet. It is the ground truth of a network investigation: logs and counters say what a program or device believes happened, while the capture shows what crossed the wire. Capture uses a packet tap (`AF_PACKET`) inside the driver path. On *ingress* the copy is taken before netfilter, so tcpdump sees packets that the firewall then drops; on *egress* the copy is taken after the firewall has accepted them ([8.12](#s8-12){.ref}, Figure 8.7). The analogy is a camera at the gate of the housing society: it records everyone who walks up, including those the guard turns away.

The commonest invocation is `tcpdump -i eth0 -nn -s 0 -w file.pcap 'filter'`.

| Option | Effect |
|---|---|
| `-i eth0` / `-i any` | interface; `any` captures all, but with a pseudo link header (no real MAC addresses) |
| `-nn` | no name or service resolution: faster and unambiguous |
| `-s 0` | capture whole packets (the default is 262144 bytes in current versions; older ones cut at 96) |
| `-w f.pcap` / `-r f.pcap` | write raw packets / read them back |
| `-c N` | stop after N packets |
| `-e` | print link-layer headers (MAC addresses, VLAN tag) |
| `-v` `-vv` | more decoding (TTL, IP id, checksums) |
| `-S` | absolute sequence numbers (default is relative) |
| `-X` / `-A` | hex-and-ASCII / ASCII payload |
| `-G secs -W n` | rotate output files: a ring buffer for long captures |
| `-ttt` | time since the previous packet, which makes delays visible |

**Filters.** The expression is compiled to *BPF* (Berkeley Packet Filter) bytecode that runs inside the kernel, so unwanted packets are never copied to user space. This is what makes capture on a busy link practical; `tcpdump -d 'expr'` prints the compiled program. The grammar is built from *primitives* joined by `and`, `or`, `not`, with parentheses quoted against the shell.

| Primitive | Matches |
|---|---|
| `host 10.0.1.2`, `src host`, `dst host` | IPv4/IPv6 address, either or one direction |
| `net 10.20.0.0/16` | any address in the prefix |
| `port 443`, `src port`, `dst port`, `portrange 8000-8100` | TCP or UDP port |
| `tcp`, `udp`, `icmp`, `arp`, `ip6` | protocol |
| `ether host aa:bb:cc:dd:ee:ff` | MAC address |
| `vlan 10` | frames tagged with VLAN 10 |
| `greater 1400`, `less 64` | frame length |
| <code>tcp[tcpflags] & (tcp-syn&#124;tcp-ack) == tcp-syn</code> | SYN set, ACK clear: a connection attempt, not the reply |
| `tcp[tcpflags] & (tcp-rst) != 0` | resets |
| `icmp[icmptype] == icmp-echo` | pings only |
| `ip[8] < 5` | TTL below 5 |

The expression `tcp[tcpflags]` reads the flag byte of the TCP header (byte 13). The mask-and-compare form is needed because several flags can be set in one packet: `& (tcp-syn|tcp-ack) == tcp-syn` keeps a SYN with ACK clear, a connection attempt, and rejects the SYN-ACK reply, whereas `& tcp-syn != 0` would match both.

```
$ tcpdump -i eth0 -nn 'tcp dst port 443 and tcp[tcpflags] & (tcp-syn|tcp-ack) == tcp-syn'   # new connections to HTTPS
$ tcpdump -i any -nn 'not port 22 and host 10.20.1.15' -w /tmp/h.pcap                    # one host, without our own SSH
$ tcpdump -nn -r /tmp/h.pcap 'tcp[tcpflags] & tcp-rst != 0'                              # filter a saved file
```

Quote the whole expression; otherwise the shell interprets parentheses, `&` and `|`. To capture on a busy interface for hours without filling the disk, use `-G 300 -W 12 -w 'cap-%H%M.pcap'`, which keeps the latest hour.

### Reading a line

A TCP line has the same shape in every capture (Figure 8.6). The flags field is the most useful: `[S]` is a SYN, `[S.]` a SYN-ACK (the dot stands for ACK), `[.]` a bare ACK, `[P.]` data with PSH and ACK, `[F.]` a FIN, `[R]` or `[R.]` a reset.

<figure>
<svg viewBox="0 0 480 130" width="480"><defs><marker id="a86" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs>
<text class="mono" x="2" y="56" font-size="6.6">13:32:10.765765 IP 10.0.1.2.48808 &gt; 10.0.2.2.8080: Flags [S], seq 1234482972, win 64240,</text>
<text class="mono" x="2" y="68" font-size="6.6">   options [mss 1460,sackOK,TS val 2431811996 ecr 0,nop,wscale 10], length 0</text>
<g class="sm">
<text x="2" y="26">time</text><path class="lg" d="M10 30 L10 46" fill="none"/>
<text x="76" y="26">source IP.port</text><path class="lg" d="M100 30 L100 46" fill="none"/>
<text x="150" y="14">destination IP.port</text><path class="lg" d="M170 18 L170 46" fill="none"/>
<text x="252" y="26">flags</text><path class="lg" d="M268 30 L268 46" fill="none"/>
<text x="318" y="14">seq (relative unless -S)</text><path class="lg" d="M350 18 L350 46" fill="none"/>
<text x="402" y="26">window offered</text><path class="lg" d="M424 30 L424 46" fill="none"/>
</g>
<g class="sm">
<text x="40" y="92">mss: largest segment</text><path class="lg" d="M62 72 L62 86" fill="none"/>
<text x="130" y="108">sackOK: selective ACK allowed</text><path class="lg" d="M148 72 L148 102" fill="none"/>
<text x="290" y="92">TS: timestamps (RTT)</text><path class="lg" d="M250 72 L290 86" fill="none"/>
<text x="330" y="108">wscale 10: window x 1024</text><path class="lg" d="M330 72 L340 102" fill="none"/>
<text x="400" y="92">length: payload bytes</text><path class="lg" d="M440 72 L440 86" fill="none"/>
</g>
<text class="sm" x="2" y="124">The ack field appears on every segment except the first SYN; ecr 0 means no timestamp echoed yet.</text>
</svg>
<figcaption><b>Figure 8.6</b> Anatomy of a tcpdump line for a SYN. Everything after the flags is TCP detail: the options carried only on SYNs fix the segment size, selective acknowledgements, timestamps and window scaling for the whole connection.</figcaption>
</figure>

::: example
**Reading a complete HTTP request.** The capture below is `curl http://10.0.2.2:8080/` taken on the router between the two end hosts, with `-ttt` (delta times) and repeated host names shortened to `C` (client, 10.0.1.2) and `S` (server, 10.0.2.2:8080). Sequence numbers are relative.

```
 delta      direction  flags    sequence / ack            note
 0.000000   C > S  Flags [S],   seq 0, win 64240, [mss 1460,sackOK,TS,nop,wscale 10]   1  SYN
 0.000041   S > C  Flags [S.],  seq 0, ack 1, win 65160, [mss 1460,sackOK,TS,wscale 10]  2  SYN-ACK
 0.000015   C > S  Flags [.],   ack 1, win 63                                           3  ACK: connected
 0.000083   C > S  Flags [P.],  seq 1:77, ack 1, length 76: HTTP: GET / HTTP/1.1       4  request
 0.000008   S > C  Flags [.],   ack 77                                                  5  request received
 0.002830   S > C  Flags [P.],  seq 1:158, ack 77, length 157: HTTP/1.0 200 OK          6  response headers
 0.000035   C > S  Flags [.],   ack 158                                                 7
 0.000048   S > C  Flags [P.],  seq 158:7033, ack 77, length 6875                       8  body
 0.000043   S > C  Flags [F.],  seq 7033, ack 77                                        10 server closes first
 0.000197   C > S  Flags [F.],  seq 77, ack 7034                                        11 client closes
 0.000033   S > C  Flags [.],   ack 78                                                  12 final ACK
```

1. Lines 1 to 3 are the three-way handshake ([3.9](#s3-9){.ref}). The SYN carries the options; `win 64240` is the offered window, and with `wscale 10` it is later read as the value times 1024 (line 3's `win 63` is 63 × 1024 bytes).
2. Line 4 carries 76 bytes of data: relative sequence 1 to 77, so the next byte expected is 77, which the ACK of line 5 confirms.
3. The 2.8 ms gap before line 6 is the server's *think time*, the gap between the request and the first response byte; it is the number to watch when a service is slow.
4. The server (HTTP/1.0) closes first with `[F.]`; the client answers, and the final ACK completes the four-way close. The server, as the first closer, is the side that holds `TIME-WAIT` ([8.6](#s8-6){.ref}).

[Result: a healthy connection shows the SYN, SYN-ACK, ACK within one round-trip time, data acknowledged promptly, and two FINs. Every departure from that is a symptom.]{.result}
:::

**A failing handshake.** The most informative failures have two forms. A closed port answers at once with a reset: the client sees `Connection refused` and the capture shows two lines.

```
$ tcpdump -i rt-eth0 -nn 'tcp port 9999'
IP 10.0.1.2.46782 > 10.0.2.2.9999: Flags [S], seq 654362669, win 64240, options [...]
IP 10.0.2.2.9999 > 10.0.1.2.46782: Flags [R.], seq 0, ack 654362670, win 0, length 0
```

A port silently dropped by a firewall (or a dead host) gives no reply at all, and the client retransmits the SYN on a timer until it gives up. With a DROP rule in the path ([8.12](#s8-12){.ref}) the capture on the *ingress* interface of the router shows the client retrying, while the capture on the egress interface shows nothing.

```
$ tcpdump -i rt-eth0 -nn -tt 'tcp port 8080'       # ingress: packets arrive and are dropped inside the router
1793280763.217828 IP 10.0.1.2.41010 > 10.0.2.2.8080: Flags [S], seq 1916356639, ...
1793280764.224517 IP 10.0.1.2.41010 > 10.0.2.2.8080: Flags [S], seq 1916356639, ...   (+1.007 s)
1793280765.248314 IP 10.0.1.2.41010 > 10.0.2.2.8080: Flags [S], seq 1916356639, ...   (+1.024 s)
1793280766.272388 IP 10.0.1.2.41010 > 10.0.2.2.8080: Flags [S], seq 1916356639, ...   (+1.024 s)
$ tcpdump -i rt-eth1 -nn 'tcp port 8080'           # egress: no packets leave
0 packets captured
```

Three points. The sequence number is the same on every line, which identifies these as retransmissions of one SYN. The curl timed out after its 8 s limit, with no error message from the network: "packets leave and nothing returns" is the signature of a drop or a dead path, whereas an RST or an ICMP error is a deliberate answer. And the spacing is 1 s, 1 s, 1 s here rather than the doubling 1, 2, 4 s that textbooks give: Linux 6.1 and later keep the first retries at the initial timeout (`net.ipv4.tcp_syn_linear_timeouts`, 4 on this machine) before backing off exponentially. Both patterns mean the same thing, so one reads the lack of an answer, not the exact spacing.

<figure>
<svg viewBox="0 0 480 190" width="480"><defs><marker id="a87" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="b87" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs>
<rect class="box" x="10" y="8" width="130" height="24" rx="2"/><text class="lbl" x="75" y="24" text-anchor="middle">NIC / driver</text>
<path class="ln" d="M75 32 L75 46" fill="none" marker-end="url(#a87)"/>
<rect class="hl" x="10" y="48" width="130" height="24" rx="2" stroke="#1A1D23" stroke-width="0.8"/><text class="lbl" x="75" y="64" text-anchor="middle">tcpdump tap (ingress)</text>
<path class="ln" d="M75 72 L75 86" fill="none" marker-end="url(#a87)"/>
<rect class="box" x="10" y="88" width="130" height="24" rx="2"/><text class="lbl" x="75" y="104" text-anchor="middle">netfilter PREROUTING / INPUT</text>
<path class="ln" d="M75 112 L75 126" fill="none" marker-end="url(#a87)"/>
<rect class="box" x="10" y="128" width="130" height="24" rx="2"/><text class="lbl" x="75" y="144" text-anchor="middle">TCP socket → application</text>
<text class="sm" x="150" y="104">firewall DROP happens here:</text><text class="sm" x="150" y="114">tcpdump has already copied it</text>
<rect class="box" x="300" y="128" width="170" height="24" rx="2"/><text class="lbl" x="385" y="144" text-anchor="middle">application sends</text>
<path class="ln" d="M385 128 L385 112" fill="none" marker-end="url(#a87)"/>
<rect class="box" x="300" y="88" width="170" height="24" rx="2"/><text class="lbl" x="385" y="104" text-anchor="middle">netfilter OUTPUT / POSTROUTING</text>
<path class="ln" d="M385 88 L385 72" fill="none" marker-end="url(#a87)"/>
<rect class="hl" x="300" y="48" width="170" height="24" rx="2" stroke="#1A1D23" stroke-width="0.8"/><text class="lbl" x="385" y="64" text-anchor="middle">tcpdump tap (egress)</text>
<path class="ln" d="M385 48 L385 32" fill="none" marker-end="url(#a87)"/>
<rect class="box" x="300" y="8" width="170" height="24" rx="2"/><text class="lbl" x="385" y="24" text-anchor="middle">driver / NIC</text>
<text class="sm" x="240" y="180" text-anchor="middle">ingress: capture, then filter.  egress: filter, then capture.</text>
</svg>
<figcaption><b>Figure 8.7</b> Where tcpdump sits relative to netfilter. A packet visible in a capture may still be discarded before the application sees it; a packet absent from an egress capture may have been dropped by the local firewall.</figcaption>
</figure>

::: trap
*Claim:* "tcpdump shows the packet, so the firewall allowed it." *Why it is wrong:* on ingress the tap is before netfilter. *Correct statement:* a packet seen on ingress has reached the NIC; whether it reaches the application is shown by `iptables -L -v` counters or the socket, not by tcpdump. Further, a capture on a VM or a router sees only its own interfaces.
:::

**Offloads and big packets.** Capture on the *sending* host and tcpdump may show segments of 30 000 or 64 000 bytes on a 1500-MTU link. This is not a bug: TCP segmentation offload (TSO) and generic segmentation offload (GSO) let the kernel hand one large buffer to the stack and have the NIC (or the last software stage) cut it into 1448-byte wire segments, and generic receive offload (GRO) merges them on receipt. The capture tap sees the buffer before it is cut ([8.11](#s8-11){.ref}). Likewise, checksums show as "incorrect" on locally generated packets because the NIC computes them after the tap.

::: lab
`LAB 8.4 · 30 MIN` Handshake forensics. In one terminal run `sudo tcpdump -i any -nn -s 0 -w /tmp/h.pcap 'port 8080 or port 9999 or port 53'`; in another, start `python3 -m http.server 8080` and run `curl localhost:8080`, `curl localhost:9999` (refused) and `dig @127.0.0.53 example.com`. Stop the capture and read it with `tcpdump -nn -r /tmp/h.pcap`.

**What you should notice:** the three-way handshake lines for 8080; an `[R.]` reply for 9999 within a microsecond; a UDP query and response for port 53 with the DNS transaction id. With `-i any` the packets appear once per interface they cross, and loopback traffic never has a real MAC address.
:::

::: check
1. Write a filter for packets leaving 10.0.1.2 to TCP port 443 that are not SYNs. [^c87-1]
2. In `[P.]`, what do P and the dot mean? [^c87-2]
:::

[^c87-1]: `src host 10.0.1.2 and dst port 443 and tcp and not (tcp[tcpflags] & tcp-syn != 0)`.
[^c87-2]: P is the PSH flag (deliver data now) and the dot represents the ACK flag.

## [8.8]{.sec}Packet capture II: Wireshark [Should · ■■□]{.tag} {#s8-8}

Wireshark decodes the same packets graphically and understands hundreds of protocols; `tshark` is its command-line form. Where tcpdump is the camera, Wireshark is the forensic laboratory. Its distinctive features are three. *Display filters* select what is shown after capture; *Follow TCP stream* reassembles a conversation into readable text; and the *Expert Information* window lists anomalies (retransmissions, resets, zero windows) found by the dissector.

The two kinds of filter use different languages and must not be confused. A *capture filter* is BPF, as in [8.7](#s8-7){.ref}, and decides what is recorded; a *display filter* is Wireshark's own field language (`protocol.field operator value`) and decides what is shown, with no loss of the underlying capture.

| Display filter | Shows |
|---|---|
| `ip.addr == 10.0.1.2` | traffic to or from the address |
| `ip.addr == 10.0.1.2 && !(tcp.port == 22)` | the host, excluding SSH |
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | connection attempts |
| `tcp.flags.reset == 1` | resets |
| `tcp.analysis.retransmission` | retransmitted segments |
| <code>tcp.analysis.fast_retransmission &#124;&#124; tcp.analysis.duplicate_ack</code> | loss recovery |
| `tcp.analysis.zero_window` | receiver buffer full |
| `tcp.stream == 3` | one TCP conversation |
| `dns.flags.rcode != 0` | DNS errors |
| `dns.qry.name contains "campus"` | queries by name |
| `http.response.code >= 400` | HTTP errors |
| `http.request.method == "POST"` | form submissions |
| `tls.handshake.type == 1` | TLS ClientHello (see the server name) |
| `icmp.type == 3` | destination unreachable |
| `frame.time_delta > 1` | gaps longer than a second |

**Analysis tools.** *Statistics → Conversations* and *Endpoints* rank hosts by bytes and packets, which finds the top talkers. *I/O Graph* plots throughput or packets per second over time, optionally with a display filter on a second line, so that "bytes" and "retransmissions" can be overlaid. *TCP Stream Graphs* include the *Stevens* time-sequence graph (sequence number against time): a steady straight line is healthy; flat steps are stalls; a jump back down is a retransmission. *Expert Info* groups findings by severity.

```
$ tshark -r cap.pcap -q -z conv,tcp                          # conversation table
10.0.1.2:45784 <-> 10.0.2.2:8080     6 7555 bytes   6 480 bytes   12 8035 bytes   0.000000   0.0040
$ tshark -r cap.pcap -Y http -T fields -e frame.number -e http.request.method -e http.response.code -e http.request.uri
4   GET        /
8          200
$ tshark -r cap.pcap -q -z expert                            # anomalies found
   Notes (2)   Sequence  TCP  This frame initiates the connection closing
   Chats (6)   Sequence  TCP  Connection establish request (SYN): server port 8080
```

**Reading a slow transfer.** The two signatures to separate are loss and receiver limits. Packet loss appears as clusters of *duplicate ACKs* (the receiver repeating the same acknowledgement number because a segment is missing) followed by a *fast retransmission*, and the Stevens graph shows a sawtooth where throughput drops after each loss event. A receiver bottleneck appears as *TCP Window Full* or *Zero Window* flags and a `win` value shrinking to 0 in the receiver's ACKs: the sender is healthy but has been told to stop, and the Stevens graph shows flat stalls without retransmission. The congestion-control reasoning behind these shapes is in [3.9](#s3-9){.ref}. The fix differs completely: loss means a network path investigation ([8.10](#s8-10){.ref}); a closing window means the application is slow to read, and the remedy is in the receiving program or its socket buffer ([8.13](#s8-13){.ref}).

**Decrypting TLS.** An HTTPS capture shows the TLS handshake in clear (ClientHello with the Server Name, certificates, the negotiated cipher; see [Pillar 9](#ch9){.ref}) and the data encrypted. Browsers and curl can write the session secrets to a file named by `SSLKEYLOGFILE`; pointing Wireshark at that file under *Preferences → Protocols → TLS → (Pre)-Master-Secret log filename* decrypts the capture for the owner of the client. It works for a test of one's own application and is a legitimate debugging method; it does not weaken TLS for anyone else, because it needs the secrets from the endpoint itself.

::: trap
*Claim:* "Wireshark's red and black lines mean the network is broken." *Why it is wrong:* the colouring and the Expert Info flag *protocol events*; a few retransmissions or one RST at connection close are common on healthy paths, and a capture taken on the sender can show checksum errors caused by offload ([8.7](#s8-7){.ref}). *Correct statement:* judge by rate and by pattern: many retransmissions on one stream, or resets at the start of connections, matter.
:::

::: check
1. Which filter language does the capture dialog use, and which the filter bar? [^c88-1]
2. What distinguishes a receiver-limited stall from packet loss? [^c88-2]
:::

[^c88-1]: The capture dialog takes BPF capture filters; the filter bar takes Wireshark display filters.
[^c88-2]: Receiver-limited stalls show zero-window or window-full flags and no retransmissions; loss shows duplicate ACKs and retransmissions.

## [8.9]{.sec}DNS from the command line: dig, nslookup, host [Must · ■■□]{.tag} {#s8-9}

`dig` (domain information groper) sends a DNS query and prints the whole reply, which makes it the standard instrument for DNS faults; `host` and `nslookup` give shorter answers. The protocol, caching and the resolver hierarchy are explained in [3.10](#s3-10){.ref}; this section teaches the output. The examples query an authoritative server for the zone `campus.example`, set up inside the lab namespace at 10.0.2.2.

```
$ dig @10.0.2.2 www.campus.example A
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 45184
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; QUESTION SECTION:
;www.campus.example.		IN	A

;; ANSWER SECTION:
www.campus.example.	300	IN	A	10.0.2.10

;; Query time: 4 msec
;; SERVER: 10.0.2.2#53(10.0.2.2) (UDP)
;; MSG SIZE  rcvd: 91
```

The header holds the verdict. `status` is the response code: **NOERROR** (the query worked; an empty answer with NOERROR means the name exists but has no record of that type), **NXDOMAIN** (the name does not exist), **SERVFAIL** (the server failed to obtain an answer: a broken upstream, unreachable authoritative servers or DNSSEC validation failure) and **REFUSED** (policy: the server will not answer this client or this zone). The *flags* describe the reply: `qr` (this is a response), `aa` (authoritative answer, from the zone's own server), `rd` (recursion desired, set by the client), `ra` (recursion available, set by a recursive resolver), `ad` (data authenticated by DNSSEC), `tc` (truncated: retry over TCP). The number after the name in the answer, `300`, is the *TTL*, the seconds for which a cache may keep the record; querying a caching resolver twice shows it counting down.

**Options that matter.**

| Command | Purpose |
|---|---|
| `dig +short www.campus.example` | only the answer data |
| `dig @10.0.2.2 name` | ask a specific server, bypassing `/etc/resolv.conf` |
| `dig campus.example MX` / `NS` / `TXT` / `SOA` / `AAAA` | other record types |
| `dig -x 10.0.2.10` | reverse lookup (PTR) |
| `dig +noall +answer name` | only the answer section, with TTL |
| `dig +trace name` | walk from the root: root, TLD, authoritative |
| `dig +norecurse @server name` | ask without recursion (what a resolver does to others) |
| `dig +cd name` | disable DNSSEC checking (distinguishes validation failure) |
| `dig +tcp name` | force TCP |
| `dig +tries=1 +time=1` | short timeout for scripts |

```
$ dig @10.0.2.2 +noall +answer portal.campus.example
portal.campus.example.	300	IN	CNAME	www.campus.example.
www.campus.example.	300	IN	A	10.0.2.10
$ dig @10.0.2.2 nosuch.campus.example | grep -E 'status|SOA'
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 9668
campus.example.		300	IN	SOA	ns1.campus.example. noc.campus.example. 2026102901 3600 600 86400 300
$ dig @10.0.2.2 www.other.example | grep status        # a zone this server does not hold
;; ->>HEADER<<- opcode: QUERY, status: REFUSED, id: 48082
$ dig @10.0.2.2 +tries=1 +time=1 www.campus.example     # server stopped
;; no servers could be reached
```

An NXDOMAIN reply carries the zone's SOA record in the *authority* section; its last field (here 300) is the negative-caching TTL, the time for which resolvers remember that the name does not exist. The CNAME in the first example shows the alias followed by the final address. The distinction between "no servers could be reached" (a timeout, with nothing heard) and a status (a server answered) is the first split in any DNS diagnosis.

**NXDOMAIN versus SERVFAIL.** For NXDOMAIN, check the spelling, the zone for a missing record, and a search-domain suffix appended by the resolver (`ndots`). For SERVFAIL, query the authoritative servers directly (`dig @ns1 name`); if they answer normally, the failure lies in the resolver's path or validation: `dig +cd name` succeeding where `dig name` fails means DNSSEC validation is rejecting the answer (expired signatures or a broken DS record at the parent).

**Tracing.** `dig +trace` performs the iterative resolution itself instead of asking a recursive resolver: it starts from the root servers, follows the referral to the top-level domain and then to the zone's authoritative servers. The shape of the output (abridged; addresses and signatures omitted) is a sequence of delegations.

```
$ dig +trace www.campus.example
.                    518400 IN NS   a.root-servers.net.  ...        <- the root zone's NS set (from the hints file)
example.              172800 IN NS   a.nic.example.  ...             <- referral from a root server to the TLD
campus.example.       86400  IN NS   ns1.campus.example.            <- referral from the TLD to the zone
www.campus.example.   300    IN A    10.0.2.10                       <- the answer, from the authoritative server
```

Each stage returns a *referral* (an NS set in the authority section, with glue addresses in the additional section) until a server answers with the `aa` flag. A trace that stops at one stage identifies the broken delegation.

**Where the host looks first.** A program calls `getaddrinfo()`, and the C library consults the sources listed in `/etc/nsswitch.conf`, normally `hosts: files dns`. `files` means `/etc/hosts`, so a line there overrides DNS. `dns` reads `/etc/resolv.conf`, which on a modern Ubuntu holds only the local stub `nameserver 127.0.0.53` run by `systemd-resolved`; `resolvectl status` shows the real upstream servers and `resolvectl query name` shows what the system resolver, as opposed to `dig`, would answer. Note that `dig` ignores `/etc/hosts` and `nsswitch.conf`: if `ping name` and `dig name` disagree, the cause is likely an `/etc/hosts` entry or a search-domain difference. `host` and `nslookup` are shorter forms:

```
$ host www.campus.example 10.0.2.2
www.campus.example has address 10.0.2.10
$ getent hosts www.campus.example              # what applications see: files, then DNS
```

::: lab
`LAB 8.5 · 30 MIN` DNS detective. Plant three faults and diagnose each with only `dig`, `getent hosts` and `cat`: (i) add `10.9.9.9 www.campus.example` to `/etc/hosts`; (ii) point `/etc/resolv.conf` at an address that does not run DNS; (iii) query a name that has no record.

**What you should notice:** `getent` returns the `/etc/hosts` address while `dig` returns the real one; a dead resolver gives timeouts ("no servers could be reached", about 2 s per try and attempt), not a status; and the missing name gives `NXDOMAIN` with an SOA in the authority section.
:::

::: check
1. `dig` shows `status: NOERROR` and an empty ANSWER section. What does that mean? [^c89-1]
2. Which two header flags show that the reply came from the zone's own server and that a resolver offered recursion? [^c89-2]
:::

[^c89-1]: The name exists but has no record of the type requested (for example an AAAA query for an IPv4-only host).
[^c89-2]: `aa` (authoritative answer) and `ra` (recursion available).

:::
