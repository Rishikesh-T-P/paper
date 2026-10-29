::: {.p3}
::: pack
## Revision Spread {#rv3}

::: revision
::: top
**Ten facts.** (1) MAC changes at every hop; IP does not, except at NAT. (2) Block size = 256 − mask octet; hosts = 2<sup>h</sup> − 2, except /31 (2) and /32 (1). (3) Fragment offset counts 8-byte units; MSS = MTU − 40. (4) TTL and header checksum change at every hop. (5) SYN and FIN each use one sequence number; a pure ACK uses none. (6) TIME_WAIT is on the active closer; CLOSE_WAIT is an application bug. (7) Effective window = min(rwnd, cwnd); throughput ≤ window / RTT; BDP = rate × RTT. (8) Reno: 3 duplicate ACKs give ssthresh = cwnd / 2; a timeout gives cwnd = 1. (9) CUBIC and Reno react to loss; BBR models bandwidth and RTT. (10) DNS: recursive from the client, iterative from the resolver; TTL decides when a change is seen; TCP for truncation and zone transfers.

**Three figures to redraw from memory.** The three-way handshake and teardown ladders with sequence numbers (Figure 3.24, Figure 3.25); the cwnd sawtooth with ssthresh (Figure 3.29); the packet-walk strip with the L2 row changing and the L3 row constant (Figure 3.19).
:::

#### Models, devices, PDUs
- 7 Application, 6 Presentation, 5 Session, 4 Transport (segment), 3 Network (packet), 2 Data link (frame), 1 Physical (bits). Mnemonic: All People Seem To Need Data Processing.
- Hub: L1, one collision and one broadcast domain. Switch: L2, collision domain per port. Router: L3, a broadcast domain per interface. Firewall and load balancer: L4 to L7.
- Demultiplexing keys: EtherType, IP protocol, port. Say in an interview: "each layer's header tells its peer what to do."

#### Layer 2
- Ethernet II: dst 6, src 6, type 2, payload 46 to 1,500, FCS 4 (frame 64 to 1,518; +4 with an 802.1Q tag). Preamble 7 + SFD 1 and gap 12 are outside the frame.
- MAC: OUI 3 + device 3 bytes; I/G = low bit of the first byte (1 = group); U/L = next bit.
- Switch: learn source, forward or flood on destination, age after 300 s. Cut-through starts after the destination MAC; store-and-forward checks the FCS.
- Min frame: L ≥ 2T<sub>p</sub>R. CRC: append r zeros, divide mod 2, remainder replaces them. Hamming: syndrome = position of the error.
- ARQ: SW efficiency 1/(1 + 2a), a = T<sub>p</sub>/T<sub>t</sub>. GBN window ≤ 2<sup>n</sup> − 1; SR window ≤ 2<sup>n−1</sup>.

#### IPv4 and subnetting
- Header 20 to 60 bytes (IHL × 4); fields: ver, IHL, DSCP/ECN, length, ID, flags (DF, MF), offset, TTL, protocol, checksum, src, dst.
- Block-size method: network = largest multiple of the block not above the address; broadcast = next network − 1.
- Private: 10/8, 172.16/12, 192.168/16. Special: 127/8, 169.254/16, 100.64/10, 224/4, 0.0.0.0, 255.255.255.255.
- VLSM: largest first, each on a multiple of its block. Summary: common leading bits of aligned, contiguous blocks.

| Prefix | Mask | Block | Addresses | Usable |
|---|---|---|---|---|
| /24 | 255.255.255.0 | 1 | 256 | 254 |
| /25 | 255.255.255.128 | 128 | 128 | 126 |
| /26 | 255.255.255.192 | 64 | 64 | 62 |
| /27 | 255.255.255.224 | 32 | 32 | 30 |
| /28 | 255.255.255.240 | 16 | 16 | 14 |
| /29 | 255.255.255.248 | 8 | 8 | 6 |
| /30 | 255.255.255.252 | 4 | 4 | 2 |
| /31 | 255.255.255.254 | 2 | 2 | 2 (RFC 3021) |
| /32 | 255.255.255.255 | 1 | 1 | 1 |

#### ARP, DHCP, NAT
- ARP: broadcast request (opcode 1), unicast reply (2). Gratuitous ARP: duplicate check and cache refresh. Proxy ARP: router answers for others.
- DHCP: Discover, Offer, Request, Ack; UDP 68 to 67; T1 50%, T2 87.5%; relay sets giaddr; options 1, 3, 6, 51, 54, 82.
- NAT: static 1:1; dynamic pool; PAT many:1 by port. Inside local, inside global, outside local, outside global. Port forwarding for servers; STUN, TURN and ICE for peer-to-peer.

#### IPv6
- 128 bits; header 40 bytes; no checksum, no router fragmentation; minimum MTU 1,280. Compress: drop leading zeros, one `::` on the longest run.
- 2000::/3 global, fc00::/7 unique local, fe80::/10 link-local, ff00::/8 multicast, ::1 loopback, 2001:db8::/32 documentation.
- EUI-64: insert FF:FE, flip bit 7. Solicited-node: ff02::1:ff + last 24 bits; MAC 33:33 + last 32 bits.
- NDP (ICMPv6): RS 133, RA 134, NS 135, NA 136, Redirect 137; PTB is type 2. RA flags: M (stateful DHCPv6), O (other options).

#### TCP and UDP
- UDP header 8 bytes: ports, length, checksum. TCP header 20 to 60 bytes: ports, seq, ack, offset, flags CWR ECE URG ACK PSH RST SYN FIN, window, checksum, urgent pointer, options (MSS, window scale, SACK, timestamps).
- Handshake: SYN, SYN-ACK, ACK. Teardown: FIN, ACK, FIN, ACK; active closer waits 2 MSL (60 s on Linux). RTO = SRTT + 4 RTTVAR, minimum 200 ms on Linux (1 s in RFC 6298), doubled on each timeout.
- Fast retransmit after 3 duplicate ACKs. Slow start doubles per RTT up to ssthresh, then +1 MSS per RTT. Initial window 10 MSS.
- Window scale shift s multiplies 65,535 by 2<sup>s</sup>. Mathis: rate ≈ (MSS / RTT) × 1.22 / √p.

| State | Who | Meaning |
|---|---|---|
| LISTEN | server | waiting for a SYN |
| SYN_SENT, SYN_RCVD | client, server | handshake in progress |
| ESTABLISHED | both | data flows |
| FIN_WAIT_1, FIN_WAIT_2 | active closer | FIN sent; ACK received |
| CLOSE_WAIT, LAST_ACK | passive closer | FIN received; waiting for the application to close |
| CLOSING | both closing | simultaneous close |
| TIME_WAIT | active closer | 2 MSL before CLOSED |

#### Ports, protocol numbers, EtherTypes
| Port | Service | Port | Service |
|---|---|---|---|
| 20/21 | FTP data/control | 123 | NTP (UDP) |
| 22 | SSH | 143 | IMAP |
| 23 | Telnet | 161/162 | SNMP |
| 25 | SMTP | 179 | BGP |
| 53 | DNS (UDP/TCP) | 389 | LDAP |
| 67/68 | DHCP server/client | 443 | HTTPS, QUIC |
| 69 | TFTP | 514 | syslog |
| 80 | HTTP | 520 | RIP |
| 110 | POP3 | 3389 | RDP |

IP protocol numbers: 1 ICMP, 2 IGMP, 6 TCP, 17 UDP, 47 GRE, 50 ESP, 51 AH, 58 ICMPv6, 89 OSPF. EtherTypes: 0x0800 IPv4, 0x0806 ARP, 0x86DD IPv6, 0x8100 802.1Q. ICMP: 0 echo reply, 3 unreachable (code 4 fragmentation needed), 5 redirect, 8 echo request, 11 time exceeded.

#### DNS, HTTP, TLS
- Records: A, AAAA, CNAME, NS, MX, PTR, TXT, SOA, SRV, CAA. UDP 53; TCP for truncation and zone transfer; DoT 853; DoH 443.
- Status classes: 2xx success, 3xx redirect (301, 302, 304), 4xx client (401, 403, 404, 429), 5xx server (500, 502, 503).
- TLS 1.3: 1 RTT; TLS 1.2: 2 RTT; SNI names the host. HTTP/2: streams over TCP, blocked by one loss. HTTP/3: QUIC over UDP 443, per-stream recovery.

#### Formulas
Transmission L / R. Propagation d / v (v ≈ 2 × 10⁸ m/s). Total delay = processing + queueing + transmission + propagation. Throughput ≤ W / RTT. BDP = R × RTT. Hosts = 2<sup>h</sup> − 2. Subnets = 2<sup>b</sup>. Frame efficiency = payload / (payload + headers + 20).
:::

::: break
#### Flashcards

::: flash
| Q | A | Q | A |
|---|---|---|---|
| Layer of a router; of a switch? | 3; 2 | Compress 2001:0db8:0000:0000:0000:0000:0000:0001 | 2001:db8::1 |
| PDU names, layer 4 down to 1 | Segment, packet, frame, bits | EUI-64 steps | Insert FF:FE; flip bit 7 |
| Fields that change per hop | TTL, header checksum, MAC addresses | Solicited-node multicast | ff02::1:ff + last 24 bits |
| Minimum and maximum Ethernet frame | 64 and 1,518 bytes (1,522 tagged) | RA flags M and O | Stateful DHCPv6; other options by DHCPv6 |
| Why 64 bytes? | Sender must still transmit when a collision returns: L ≥ 2T<sub>p</sub>R | ICMPv6 NDP types | 133 to 137 |
| Switch, unknown destination | Flood out of all ports except the arrival port | UDP header size; TCP minimum | 8; 20 bytes |
| CRC remainder bits for generator 10011 | 4 | What does a SYN consume? | One sequence number |
| Stop-and-Wait efficiency | 1 / (1 + 2a) | Which side has TIME_WAIT? | The active closer |
| GBN and SR window, n-bit numbers | 2<sup>n</sup> − 1; 2<sup>n−1</sup> | Many CLOSE_WAIT sockets mean | Application does not call close() |
| /27: block, hosts | 32; 30 | Effective window | min(rwnd, cwnd) |
| /30: hosts; /31: hosts | 2; 2 (RFC 3021) | Slow start growth | Doubles each RTT |
| /22 mask | 255.255.252.0 | Reno on 3 duplicate ACKs | ssthresh = cwnd / 2; cwnd = ssthresh (+3 inflation) |
| Wildcard of /21 | 0.0.7.255 | Reno on timeout | cwnd = 1 |
| Private IPv4 ranges | 10/8, 172.16/12, 192.168/16 | CUBIC reacts to | Loss; cubic growth about W<sub>max</sub> |
| APIPA range | 169.254.0.0/16 | BBR models | Bottleneck bandwidth and minimum RTT |
| CGNAT range | 100.64.0.0/10 | 64 KB window, 100 ms RTT | 5.24 Mb/s |
| Fragment offset unit | 8 bytes | BDP of 1 Gb/s, 100 ms | 12.5 MB |
| MSS on Ethernet; on PPPoE | 1,460; 1,452 | Why Nagle plus delayed ACK stalls | Each waits for the other; use TCP_NODELAY |
| ICMP for PMTUD | Type 3 code 4 | SYN cookie holds | Hash of 4-tuple, secret and time in the ISN |
| Traceroute probes, Linux; Windows | UDP from port 33434; ICMP echo | TLS 1.3 handshake | 1 RTT |
| ARP request destination MAC | ff:ff:ff:ff:ff:ff | DNS over TCP when | Truncation, zone transfer |
| DHCP ports | 67 server, 68 client | CNAME at the apex | Not allowed (SOA and NS there) |
| DHCP T1; T2 | 50%; 87.5% of the lease | HTTP/3 transport | QUIC over UDP 443 |
| Role of giaddr | Identifies the client subnet to the server | First step of the google.com walk | Browser caches and HSTS, then DNS |
| PAT distinguishes hosts by | Source port |  |  |
:::
:::
:::
:::
