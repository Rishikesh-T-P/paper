::: {.p3}
::: pack
## Problem Set {#ps3}

::: problems
::: q
### Q3.1 Name the OSI layers and give one protocol and one device for each.
[ALL · TECH-1 · ■□□ · S]{.meta}

[30-second answer: 7 Application (HTTP; gateway), 6 Presentation (TLS), 5 Session (RPC), 4 Transport (TCP; firewall, L4 load balancer), 3 Network (IP; router), 2 Data link (Ethernet; switch, AP), 1 Physical (cable, 802.3 PHY; hub, repeater). PDUs: data, segment, packet, frame, bits.]{.short}

**Follow-ups.** Where is ARP (between 2 and 3, carried in Ethernet)? Which layers does TCP/IP merge (5 to 7, and 1 to 2)? **Mistakes.** Calling a switch a layer-3 device (only an L3 switch is); placing TLS in the TCP/IP model without saying it sits between transport and application. Details: [§3.2](#s3-2){.ref}.
:::

::: q
### Q3.2 Hub, switch, router: collision and broadcast domains?
[CISCO · NOKIA · TECH-1 · ■□□ · S]{.meta}

[30-second answer: a hub is one collision domain and one broadcast domain for all its ports; a switch gives one collision domain per port but keeps one broadcast domain (per VLAN); a router gives each interface its own collision and broadcast domain.]{.short}

**Approach.** Collision domain: who can collide on a shared medium. Broadcast domain: who hears a broadcast. **Answer.** Hub repeats bits to all ports, so everything shares one wire. Switch forwards per port by MAC, so full-duplex ports never collide, but floods broadcasts everywhere in the VLAN. Router does not forward broadcasts, so it ends the domain. For the counting exercise (2 broadcast, 8 collision domains) see Figure 3.2 in [§3.1](#s3-1){.ref}. **Mistake.** Saying a switch splits broadcast domains; VLANs do, not the switch itself.
:::

::: q
### Q3.3 Which IP header fields change at each router hop, and which never change?
[CISCO · AMAZON · JUNIPER · TECH-1 · ■□□ · S]{.meta}

[30-second answer: at every hop the TTL falls by one and the header checksum is recomputed, and the Ethernet source and destination MAC are rewritten. Source and destination IP, protocol and the TCP or UDP ports never change, unless NAT rewrites them.]{.short}

**Answer.** Constant end to end: IP source and destination, protocol, identification, data. Changing per hop: TTL, checksum, and the layer-2 header and FCS. Changing only when something special happens: fragment fields (a router fragments), DSCP and ECN (a router re-marks or signals congestion), addresses and ports (NAT). **Mistake.** Saying the IP address changes and the MAC does not; the correct statement is the reverse ([§3.6](#s3-6){.ref}).
:::

::: q
### Q3.4 Why is the minimum Ethernet frame 64 bytes? Derive it from CSMA/CD.
[QUALCOMM · BROADCOM · TECH-1 · ■■□ · S]{.meta}

[30-second answer: a sender must still be transmitting when a collision signal returns from the far end, so frame time must be at least twice the one-way delay: L ≥ 2T<sub>p</sub>R. For 10 Mb/s and 2,500 m, 2T<sub>p</sub> = 25 µs gives 250 bits; the standard uses 512 bits (64 bytes, 51.2 µs) to allow for repeaters and jam signal.]{.short}

**Approach and answer.** T<sub>p</sub> = 2,500 / (2 × 10⁸) = 12.5 µs; 2T<sub>p</sub> × 10 Mb/s = 250 bits; round up to 512 bits. Payload is padded to 46 bytes, so that 14 + 46 + 4 = 64. **Follow-ups.** What changes at 1 Gb/s (carrier extension; full duplex has no collisions)? **Mistake.** Dividing by T<sub>p</sub>, not 2T<sub>p</sub>. See [§3.3](#s3-3){.ref}.
:::

::: q
### Q3.5 How does a switch learn MAC addresses? What happens when the CAM table is full?
[CISCO · ARISTA · BROADCOM · TECH-1 · ■■□ · S]{.meta}

[30-second answer: it records the source MAC of every frame against the arrival port, forwards by the destination MAC, and floods broadcast, multicast and unknown unicast. When the table is full it cannot learn, so unknown destinations are flooded and the switch behaves like a hub, which an attacker exploits with MAC flooding.]{.short}

**Answer.** Entries age out (300 s on Cisco) and are refreshed by traffic, so moves are relearned; a frame whose destination is on its arrival port is filtered. A full table does not drop traffic; it degrades to flooding, so the attacker sees other hosts' frames. **Mitigation.** Port security with a MAC limit per port, sticky addresses, and storm control (Pillar 9). **Mistake.** Saying that a full table drops frames. See [§3.3](#s3-3){.ref}.
:::

::: q
### Q3.6 Compute the CRC for data 1101011011 with generator 10011.
[QUALCOMM · NOKIA · OA · ■■□ · S]{.meta}

[30-second answer: append four zeros (the generator's degree), divide modulo 2, and the remainder is 1110; the transmitted word is 11010110111110, and the receiver's division gives remainder 0.]{.short}

**Approach.** The register after each XOR, and the check, are worked out in the CRC example of [§3.3](#s3-3){.ref}. **Check.** 11010110111110 divided by 10011 leaves 0000, as verified by running the same loop on the full word. **Mistake.** Forgetting to append the zeros first, or using subtraction with borrows instead of XOR.
:::

::: q
### Q3.7 With 3-bit sequence numbers, what are the maximum Go-Back-N and Selective Repeat windows?
[QUALCOMM · BROADCOM · TECH-1 · ■■□ · S]{.meta}

[30-second answer: Go-Back-N 2³ − 1 = 7; Selective Repeat 2³⁻¹ = 4.]{.short}

**Reason.** In GBN the receiver window is 1, so the sender window may use all but one of the numbers: if all 8 were outstanding, an ACK of 0 could mean "all 8 received" or "none received". In SR both windows have size W and must not overlap modulo 2ⁿ, so 2W ≤ 2ⁿ. **Mistake.** Quoting 2ⁿ for both.
:::

::: q
### Q3.8 Stop-and-Wait, 1 Mb/s, 1,000-bit frames, T<sub>p</sub> = 20 ms: efficiency, and the window for 100%?
[QUALCOMM · TECH-1 · ■■□ · S]{.meta}

[30-second answer: T<sub>t</sub> = 1 ms, a = 20, η = 1/(1 + 2a) = 1/41 ≈ 2.4%; a window of 41 frames gives 100%.]{.short}

**Follow-ups.** Sequence bits: GBN needs 6, SR needs 7 (the full working is in [§3.3](#s3-3){.ref}). If the frame error rate is p, Stop-and-Wait efficiency becomes (1 − p)/(1 + 2a). **Mistake.** Using the round-trip time as T<sub>p</sub>.
:::

::: q
### Q3.9 Cut-through versus store-and-forward: which is faster, which propagates errors, and why do data-centre switches offer cut-through?
[ARISTA · BROADCOM · TECH-2 · ■■■ · T]{.meta}

[30-second answer: cut-through is faster, because it starts forwarding after the destination MAC (latency of tens of nanoseconds, independent of frame size) whereas store-and-forward waits for the whole frame and its FCS (1,500 bytes cost 1.2 µs at 10 Gb/s per hop). The price is that cut-through forwards corrupted frames, which the receiver then drops. Data-centre switches use it because small latencies add up over several hops and matter to storage and HPC traffic.]{.short}

**Answer.** Store-and-forward checks the FCS, can convert speeds and queue-shape, and never forwards a bad frame. Cut-through needs equal ingress and egress speed and an uncongested egress; otherwise the switch must buffer, and falls back. Many switches count FCS errors per port and fall back to store-and-forward above a threshold. **Mistake.** Saying cut-through checks the FCS.
:::

::: q
### Q3.10 Network, broadcast and usable range for 172.16.45.200/21, without a calculator.
[CISCO · AMAZON · TECH-1 · ■□□ · S]{.meta}

[30-second answer: block size 8 in the third octet, 45 lies in 40 to 47: network 172.16.40.0, broadcast 172.16.47.255, usable 172.16.40.1 to 172.16.47.254, 2,046 hosts.]{.short}

**Approach.** Mask 255.255.248.0, block = 256 − 248 = 8; the full working and the wildcard (0.0.7.255) are in [§3.4](#s3-4){.ref}. **Mistake.** Writing 172.16.45.0 as the network address.
:::

::: q
### Q3.11 How many usable hosts on a /27 and a /31? Why is /31 allowed?
[CISCO · JUNIPER · TECH-1 · ■□□ · S]{.meta}

[30-second answer: /27 has 5 host bits, 2⁵ − 2 = 30 usable. A /31 has 2 addresses and both are usable, because RFC 3021 allows a point-to-point link to dispense with the network and broadcast addresses.]{.short}

**Answer.** A /32 holds one address and names a host. The saving matters: a /31 per link uses half the addresses of a /30. Not all equipment supports /31 on all interface types, so verify before deploying. **Mistake.** Saying that /31 has zero hosts.
:::

::: q
### Q3.12 VLSM plan from 192.168.10.0/24 for LANs of 100, 50 and 25 hosts and two WAN links.
[CISCO · NOKIA · TECH-1 · ■■□ · S]{.meta}

[30-second answer: /25 at .0, /26 at .128, /27 at .192, then /30 at .224 and /30 at .228, leaving .232/29 and .240/28 spare.]{.short}

**Approach.** Largest first, each on a multiple of its block size. The usable range of each is in [§3.4](#s3-4){.ref}: .1 to .126, .129 to .190, .193 to .222, .225 and .226, .229 and .230. **Mistake.** Starting with the small subnets, which leaves no aligned room for the /25.
:::

::: q
### Q3.13 Summarise 10.1.4.0/24 to 10.1.7.0/24. Can 10.1.5.0 to 10.1.8.0 become one /22?
[CISCO · JUNIPER · TECH-1 · ■■□ · T]{.meta}

[30-second answer: 10.1.4.0/22. No: the third octets 5 to 8 share only four bits, so one summary would be 10.1.0.0/20, which over-claims 12 other /24s; use 10.1.5.0/24, 10.1.6.0/23 and 10.1.8.0/24.]{.short}

**Approach.** Binary alignment: the block must start at a multiple of its size, and contain only the required networks. 4 to 7 is a four-block range starting at a multiple of 4; 5 to 8 is not. See [§3.4](#s3-4){.ref}.
:::

::: q
### Q3.14 Write `in_subnet(ip, cidr)` using only bitwise operations.
[CISCO · GOOGLE · ARISTA · TECH-1 · ■■□ · S]{.meta}

[30-second answer: build the mask by shifting, and compare the two addresses under the mask: `(ip & mask) == (net & mask)`. Guard the prefix 0 case, because shifting a 32-bit value by 32 is undefined in C.]{.short}

```c
#include <stdint.h>
#include <stdio.h>
int parse(const char *s, uint32_t *o) {
  unsigned a, b, c, d;
  if (sscanf(s, "%u.%u.%u.%u",
             &a, &b, &c, &d) != 4
      || (a|b|c|d) > 255) return -1;
  *o = a << 24 | b << 16 | c << 8 | d;
  return 0;
}
int in_subnet(uint32_t ip,
              uint32_t net, int p) {
  uint32_t m = p ? ~0u << (32 - p) : 0;
  return (ip & m) == (net & m);
}
```

**Complexity.** O(1). **Follow-ups.** Return the network and broadcast: `net & mask` and `net | ~mask`. Support IPv6 by comparing 16 bytes with a partial last byte. **Mistake.** Using signed integers (right shifts then sign-extend), or string comparison.
:::

::: q
### Q3.15 Fragment a 4,000-byte datagram for MTU 1,500: offsets and MF flags.
[QUALCOMM · BROADCOM · JUNIPER · TECH-1 · ■■□ · S]{.meta}

[30-second answer: three fragments with data 1,480, 1,480 and 1,020 bytes, Total Length 1,500, 1,500 and 1,040, offset field 0, 185 and 370 (in 8-byte units), MF 1, 1 and 0.]{.short}

**Approach.** Data per fragment = 1,500 − 20 = 1,480, a multiple of 8. The table and the second-link variant (MTU 576) are in [§3.5](#s3-5){.ref}. **Mistake.** Writing 1,480 in the offset field.
:::

::: q
### Q3.16 MTU versus MSS: what is the MSS over PPPoE, and what does `ip tcp adjust-mss` do?
[AMAZON · CISCO · TECH-1 · ■■□ · S]{.meta}

[30-second answer: MTU is the largest IP packet on a link; MSS is the largest TCP payload, MTU − 40 for IPv4. PPPoE has MTU 1,492, so MSS = 1,452. `ip tcp adjust-mss 1452` makes the router rewrite the MSS option in transit SYNs, so that endpoints never send segments that exceed the link, which avoids the stalls of a broken PMTUD.]{.short}

**Answer.** Each endpoint advertises an MSS from its own interface MTU and cannot know of a smaller link in the middle; clamping fixes that without relying on ICMP. IPv6 subtracts 60 (40 + 20). **Mistake.** Including the Ethernet header in the MTU.
:::

::: q
### Q3.17 Scenario: pages do not load, though ping and the TCP handshake work. What is happening, and how do you prove it?
[AMAZON · MICROSOFT · CISCO · TECH-2 · ■■■ · T]{.meta}

[30-second answer: a path-MTU black hole. Small packets pass, but a full-size packet with DF set is too big for a link in the path, and the ICMP "fragmentation needed" message is blocked, so the sender keeps resending the same large segment. Prove it with DF-set pings of decreasing size, and a capture that shows repeated retransmissions and no ICMP type 3 code 4.]{.short}

**Approach.** (i) `ping -M do -s 1472 host` fails but `-s 1372` succeeds: bisect for the largest working size. (ii) Capture at the client: SYN, SYN-ACK and the request succeed; the response's large segments never arrive or arrive after retransmissions; no ICMP 3/4. (iii) Locate it with `tracepath` or by pinging each hop with DF. (iv) Fix: permit ICMP 3/4 at firewalls; clamp MSS at the tunnel or PPPoE edge; lower the interface MTU. **Mistakes.** Blaming DNS or the server; leaving ICMP blocked "for security". See Figure 3.14 and [§3.5](#s3-5){.ref}.
:::

::: q
### Q3.18 How does traceroute work on Linux and on Windows? Why `* * *`?
[AMAZON · CISCO · TECH-1 · ■■□ · S]{.meta}

[30-second answer: it sends probes with TTL 1, 2, 3 and so on, and each router that decrements the TTL to zero returns ICMP time exceeded, revealing itself. Linux sends UDP probes to ports from 33434 and the destination answers ICMP port unreachable; Windows `tracert` sends ICMP echo requests and the destination answers echo reply. `* * *` means no reply arrived in time.]{.short}

**Answer.** Reasons for stars: the router rate-limits or suppresses ICMP, a firewall drops probes of this type (try `traceroute -I` or `-T -p 443`), the return path differs, or the destination ignores the probe. A star in the middle with replies afterwards is harmless. **Mistake.** Reading a star as an outage. See [§3.5](#s3-5){.ref}.
:::

::: q
### Q3.19 What is APIPA (169.254.0.0/16), and what does it tell you about DHCP?
[MICROSOFT · CISCO · TECH-1 · ■□□ · S]{.meta}

[30-second answer: a host that gets no DHCP reply gives itself a link-local 169.254.x.y address, after probing with ARP that it is unused. Seeing it means the host could not reach a DHCP server: check the cable and VLAN, the relay (`ip helper-address`), the pool (exhausted?) and the server.]{.short}

**Mistake.** Treating it as a working configuration: such a host can talk only to others on its own link.
:::

::: q
### Q3.20 Explain DHCP DORA with ports and addresses. Why is Discover a broadcast?
[CISCO · MICROSOFT · TECH-1 · ■□□ · S]{.meta}

[30-second answer: Discover (client 0.0.0.0:68 to 255.255.255.255:67), Offer, Request (broadcast, names the chosen server and the address wanted), Acknowledgement (carries mask, gateway, DNS, lease). Discover is a broadcast because the client has no address and does not know any server.]{.short}

**Answer.** Offer and Ack may be unicast to the client MAC or broadcast, depending on the broadcast flag. The Request is broadcast too, so that losing servers learn that their offer was declined. Renewal: unicast at T1 (50%), broadcast at T2 (87.5%). The relay case is in [§3.6](#s3-6){.ref}.
:::

::: q
### Q3.21 DHCP server on another subnet: how does it work, and what is giaddr?
[CISCO · JUNIPER · TECH-2 · ■■□ · S]{.meta}

[30-second answer: a relay agent on the client's router (`ip helper-address`) turns the broadcast into a unicast to the server and fills giaddr with the address of the interface the request arrived on. The server uses giaddr to select the pool for that subnet and replies to giaddr; the relay delivers the reply to the client.]{.short}

**Answer.** Addresses: Discover 0.0.0.0 to 255.255.255.255; relayed copy relay-IP to server-IP, UDP 67 to 67. Option 82 can add circuit identifiers. **Mistake.** Forgetting that without giaddr the server cannot know which subnet to allocate from. See Figure 3.17.
:::

::: q
### Q3.22 What is gratuitous ARP, and where is it used?
[CISCO · ARISTA · TECH-2 · ■■□ · T]{.meta}

[30-second answer: an ARP message in which a host announces its own address (sender and target IP equal). It detects duplicate addresses, refreshes neighbours' caches after a change, and is sent by a new active router in first-hop redundancy protocols (HSRP, VRRP) or by a failed-over server so that switches and hosts relearn the virtual address.]{.short}

**Mistake.** Thinking it requests anything; no reply is expected. If one arrives, the address is a duplicate. Security: it is also the tool of ARP spoofing (Pillar 9).
:::

::: q
### Q3.23 Walk a packet from PC-A to a web server through a PAT router. Give MAC, IP and port at each hop.
[CISCO · AMAZON · GOOGLE · TECH-1 · ■■□ · S]{.meta}

[30-second answer: PC-A ARPs for its gateway; the frame goes AA:AA to 11:11 with 192.168.1.10:51000 to 198.51.100.80:80. R1 applies PAT, so the second leg is 12:12 to 21:21 with 203.0.113.2:51000 to the same destination; the third is 22:22 to BB:BB with the same IPs. MACs change at every link, IPs only at the NAT.]{.short}

**Answer.** The complete walk, the NAT table row and the return path are in [§3.6](#s3-6){.ref}. **Follow-ups.** Server on the same subnet: no gateway, ARP for the server. Two hosts with the same source port: R1 assigns another global port. **Mistake.** Reversing the roles of MAC and IP.
:::

::: q
### Q3.24 Scenario: two hosts behind different NATs need peer-to-peer VoIP. Why does it fail, and how do STUN, TURN and ICE help?
[QUALCOMM · MICROSOFT · TECH-2 · ■■■ · T]{.meta}

[30-second answer: each NAT drops unsolicited inbound packets, since it has no mapping for them, and each host knows only its private address. STUN lets a host learn its public mapping from a server; both sides exchange these and send simultaneously (hole punching), which works for most NATs. TURN relays media through a server when punching fails (symmetric NATs). ICE gathers all candidates, tests the pairs and picks the best.]{.short}

**Answer.** Candidate types: host (private), server-reflexive (from STUN), relayed (TURN). A signalling channel (SIP, WebRTC) carries the candidates. Carrier-grade NAT often forces TURN. IPv6 removes NAT but not firewalls. **Mistake.** Forgetting that TURN costs bandwidth, which is why it is the last resort.
:::

::: q
### Q3.25 Proxy ARP: what is it, and what can it hide?
[CISCO · TECH-2 · ■■□ · T]{.meta}

[30-second answer: a router answers ARP requests for addresses it can route to, with its own MAC, so a host that believes a remote address is local still reaches it. It hides wrong masks and missing default gateways, inflates ARP tables, and breaks when the router fails; it is usually disabled (`no ip proxy-arp`).]{.short}
:::

:::
:::
:::
