::: {.p3}

## [3.3]{.sec}The data-link layer: Ethernet, switching, error control and ARQ [Must · ■■□]{.tag} {#s3-3}

The data-link layer delivers frames across a single link, between two devices that are directly connected. It must decide where one frame ends and the next begins (*framing*), which neighbour a frame is for (*addressing*), whether the frame was damaged (*error detection*) and, on some links, how to repair damage (*ARQ*, automatic repeat request). Ethernet, which dominates wired networks, answers the first three; the fourth is done mostly by higher layers, but it is the standard exam topic for sliding-window protocols and reappears in TCP.

::: bigidea
Layer 2 gets a frame across one link: the MAC address picks the receiver, the CRC detects damage, and a switch forwards by learning where each address lives.
:::

### The physical layer in one page

Bits travel as electrical signals over copper, as light over fibre or as radio waves. *Unshielded twisted pair* (UTP) is the cable in offices: Cat5e carries 1 Gb/s and Cat6a carries 10 Gb/s to 100 m. *Fibre* carries more over longer distances: *multimode* (MMF) reaches a few hundred metres inside a building, and *single-mode* (SMF) reaches tens of kilometres. Transceivers plug into the switch as SFP (1 Gb/s), SFP+ (10), SFP28 (25) and QSFP (40 to 400).

Two ends of a link must agree on speed and *duplex*. Full duplex means both ends transmit at once; half duplex means they take turns. Auto-negotiation normally settles both, but if one end is forced to full duplex and the other is left on auto, the auto end falls back to half duplex. This *duplex mismatch* is a classic fault: the link comes up and pings work, but throughput collapses under load, the half-duplex side reports late collisions and the full-duplex side reports CRC errors and runts.

### Ethernet frames and MAC addresses

[**Unicast, multicast, broadcast** — one receiver, a group of receivers, everyone on the segment. Broadcast is the all-ones address.]{.margin}Every Ethernet port has a 48-bit *MAC address*, written as six hexadecimal bytes. The first three bytes form the *OUI*, assigned to the manufacturer; the last three are chosen by the manufacturer. Two bits of the first byte carry meaning: the lowest bit (I/G) marks a group address, so any address with an odd first byte, including `ff:ff:ff:ff:ff:ff`, is multicast or broadcast; the next bit (U/L) marks an address that an administrator has set instead of the hardware default.

<figure>
<svg viewBox="0 0 480 156" width="480">
<text class="lbl" x="20" y="12" text-anchor="start" >A MAC address is 48 bits, written as six bytes in hexadecimal</text>
<rect class="fill" x="20" y="22" width="210" height="26" rx="0" />
<text class="lbl" x="125" y="39" text-anchor="middle" >OUI (24 bits): vendor</text>
<rect class="box" x="230" y="22" width="210" height="26" rx="0" />
<text class="lbl" x="335" y="39" text-anchor="middle" >NIC-specific (24 bits)</text>
<text class="sm" x="20" y="70" text-anchor="start" >First octet, most significant bit on the left</text>
<rect class="box" x="20" y="78" width="34" height="26" rx="0" />
<text class="mono" x="37" y="95" text-anchor="middle" >0</text>
<text class="sm" x="37" y="116" text-anchor="middle" >b7</text>
<rect class="box" x="54" y="78" width="34" height="26" rx="0" />
<text class="mono" x="71" y="95" text-anchor="middle" >0</text>
<text class="sm" x="71" y="116" text-anchor="middle" >b6</text>
<rect class="box" x="88" y="78" width="34" height="26" rx="0" />
<text class="mono" x="105" y="95" text-anchor="middle" >0</text>
<text class="sm" x="105" y="116" text-anchor="middle" >b5</text>
<rect class="box" x="122" y="78" width="34" height="26" rx="0" />
<text class="mono" x="139" y="95" text-anchor="middle" >0</text>
<text class="sm" x="139" y="116" text-anchor="middle" >b4</text>
<rect class="box" x="156" y="78" width="34" height="26" rx="0" />
<text class="mono" x="173" y="95" text-anchor="middle" >0</text>
<text class="sm" x="173" y="116" text-anchor="middle" >b3</text>
<rect class="box" x="190" y="78" width="34" height="26" rx="0" />
<text class="mono" x="207" y="95" text-anchor="middle" >0</text>
<text class="sm" x="207" y="116" text-anchor="middle" >b2</text>
<rect class="hl" x="224" y="78" width="34" height="26" rx="0" />
<rect class="ln" x="224" y="78" width="34" height="26" rx="0" fill="none"/>
<text class="mono" x="241" y="95" text-anchor="middle" >0</text>
<text class="sm" x="241" y="116" text-anchor="middle" >b1</text>
<rect class="hl" x="258" y="78" width="34" height="26" rx="0" />
<rect class="ln" x="258" y="78" width="34" height="26" rx="0" fill="none"/>
<text class="mono" x="275" y="95" text-anchor="middle" >0</text>
<text class="sm" x="275" y="116" text-anchor="middle" >b0</text>
<text class="acct" x="241" y="132" text-anchor="middle" style="font-weight:700;font-size:8px">U/L</text>
<text class="acct" x="275" y="132" text-anchor="middle" style="font-weight:700;font-size:8px">I/G</text>
<text class="lbl" x="300" y="92" text-anchor="start" >Example: 00:1A:2B:3C:4D:5E</text>
<text class="sm" x="300" y="104" text-anchor="start" >first octet 0x00 = 0000 0000</text>
<text class="sm" x="300" y="116" text-anchor="start" >I/G = 0: unicast; U/L = 0: global (burned in)</text>
<text class="sm" x="20" y="148" text-anchor="start" >I/G = 1 means group address (multicast; all ones is broadcast ff:ff:ff:ff:ff:ff). U/L = 1 means locally administered.</text>
</svg>
<figcaption><b>Figure 3.6</b> MAC address structure. The two low bits of the first octet are flags; the U/L bit is the one flipped when an IPv6 interface ID is built from a MAC (Section 3.7).</figcaption>
</figure>

The frame format that nearly all networks use is *Ethernet II*. The destination address comes first so that a switch can start forwarding before the rest has arrived. The 2-byte *type* field says what the payload is (0x0800 for IPv4, for example). The payload must be at least 46 bytes, and short payloads are padded, for a reason derived below. The trailer is the 4-byte FCS, a CRC-32 computed over the frame. The *maximum transmission unit* (MTU), the largest payload, is 1,500 bytes.

A *VLAN tag* of 4 bytes, defined in 802.1Q, may be inserted after the source address. It starts with the value 0x8100 (the tag protocol identifier), followed by a 3-bit priority, a drop-eligible bit and a 12-bit VLAN identifier, so up to 4,094 usable VLANs exist. VLANs themselves are treated in Pillar 4.

<figure>
<svg viewBox="0 0 480 250" width="480">
<text class="lbl" x="20" y="12" text-anchor="start" >Ethernet II frame</text>
<rect class="fill" x="20" y="30" width="52" height="26" rx="0" />
<text class="lbl" x="46.0" y="46" text-anchor="middle" style="font-size:7.8px">Preamble</text>
<text class="sm" x="46.0" y="26" text-anchor="middle" >7 B</text>
<rect class="fill" x="72" y="30" width="22" height="26" rx="0" />
<text class="lbl" x="83.0" y="46" text-anchor="middle" style="font-size:7.8px">SFD</text>
<text class="sm" x="83.0" y="26" text-anchor="middle" >1 B</text>
<rect class="box" x="94" y="30" width="48" height="26" rx="0" />
<text class="lbl" x="118.0" y="46" text-anchor="middle" style="font-size:7.8px">Dst MAC</text>
<text class="sm" x="118.0" y="26" text-anchor="middle" >6 B</text>
<rect class="box" x="142" y="30" width="48" height="26" rx="0" />
<text class="lbl" x="166.0" y="46" text-anchor="middle" style="font-size:7.8px">Src MAC</text>
<text class="sm" x="166.0" y="26" text-anchor="middle" >6 B</text>
<rect class="box" x="190" y="30" width="30" height="26" rx="0" />
<text class="lbl" x="205.0" y="46" text-anchor="middle" style="font-size:7.8px">Type</text>
<text class="sm" x="205.0" y="26" text-anchor="middle" >2 B</text>
<rect class="box" x="220" y="30" width="150" height="26" rx="0" />
<text class="lbl" x="295.0" y="46" text-anchor="middle" style="font-size:7.8px">Payload (46–1500 B)</text>
<rect class="box" x="370" y="30" width="38" height="26" rx="0" />
<text class="lbl" x="389.0" y="46" text-anchor="middle" style="font-size:7.8px">FCS</text>
<text class="sm" x="389.0" y="26" text-anchor="middle" >4 B</text>
<line class="lg" x1="94" y1="64" x2="94" y2="70" />
<line class="lg" x1="94" y1="70" x2="408" y2="70" />
<line class="lg" x1="408" y1="64" x2="408" y2="70" />
<text class="sm" x="251.0" y="81" text-anchor="middle" >frame = 64 to 1518 bytes (Dst MAC to FCS)</text>
<text class="sm" x="20" y="100" text-anchor="start" >Preamble and SFD are added by the hardware and are not counted in the frame size</text>
<text class="lbl" x="20" y="122" text-anchor="start" >With an 802.1Q VLAN tag</text>
<rect class="box" x="20" y="144" width="48" height="26" rx="0" />
<text class="lbl" x="44.0" y="160" text-anchor="middle" style="font-size:7.8px">Dst MAC</text>
<text class="sm" x="44.0" y="140" text-anchor="middle" >6 B</text>
<rect class="box" x="68" y="144" width="48" height="26" rx="0" />
<text class="lbl" x="92.0" y="160" text-anchor="middle" style="font-size:7.8px">Src MAC</text>
<text class="sm" x="92.0" y="140" text-anchor="middle" >6 B</text>
<rect class="hl" x="116" y="144" width="50" height="26" rx="0" />
<rect class="ln" x="116" y="144" width="50" height="26" rx="0" fill="none"/>
<text class="lbl" x="141.0" y="160" text-anchor="middle" style="font-size:7.8px">TPID 0x8100</text>
<text class="sm" x="141.0" y="140" text-anchor="middle" >2 B</text>
<rect class="hl" x="166" y="144" width="32" height="26" rx="0" />
<rect class="ln" x="166" y="144" width="32" height="26" rx="0" fill="none"/>
<text class="lbl" x="182.0" y="160" text-anchor="middle" style="font-size:7.8px">TCI</text>
<text class="sm" x="182.0" y="140" text-anchor="middle" >2 B</text>
<rect class="box" x="198" y="144" width="30" height="26" rx="0" />
<text class="lbl" x="213.0" y="160" text-anchor="middle" style="font-size:7.8px">Type</text>
<text class="sm" x="213.0" y="140" text-anchor="middle" >2 B</text>
<rect class="box" x="228" y="144" width="114" height="26" rx="0" />
<text class="lbl" x="285.0" y="160" text-anchor="middle" style="font-size:7.8px">Payload (46–1500 B)</text>
<rect class="box" x="342" y="144" width="38" height="26" rx="0" />
<text class="lbl" x="361.0" y="160" text-anchor="middle" style="font-size:7.8px">FCS</text>
<text class="sm" x="361.0" y="140" text-anchor="middle" >4 B</text>
<text class="sm" x="20" y="242" text-anchor="start" >Tag adds 4 bytes: maximum frame 1522 B. Type 0x0800 = IPv4, 0x0806 = ARP, 0x86DD = IPv6.</text>
<text class="sm" x="300" y="200" text-anchor="start" >TCI (16 bits)</text>
<rect class="box" x="300" y="204" width="44" height="20" rx="0" />
<text class="lbl" x="322.0" y="217" text-anchor="middle" style="font-size:7.4px">PCP 3</text>
<rect class="box" x="344" y="204" width="30" height="20" rx="0" />
<text class="lbl" x="359.0" y="217" text-anchor="middle" style="font-size:7.4px">DEI 1</text>
<rect class="box" x="374" y="204" width="104" height="20" rx="0" />
<text class="lbl" x="426.0" y="217" text-anchor="middle" style="font-size:7.4px">VLAN ID 12 bits</text>
<text class="sm" x="300" y="200" text-anchor="middle" ></text>
</svg>
<figcaption><b>Figure 3.7</b> Byte-accurate Ethernet II frame (top) and the same frame with an 802.1Q tag (below). The minimum of 64 bytes is the reason for padding short payloads up to 46 bytes.</figcaption>
</figure>

### CSMA/CD and the 64-byte minimum

On the original shared cable, any station could transmit when it heard silence, and two stations could start together. *CSMA/CD* (carrier sense multiple access with collision detection) handles this: a station listens first, transmits if the cable is idle, keeps listening while transmitting, and on hearing a collision stops, sends a short jam signal and waits a random time that grows after each repeated collision (*binary exponential backoff*). For the sender to detect a collision it must still be transmitting when the damaged signal returns from the far end, which sets a lower limit on the frame length.

::: example
**Why is the minimum frame 64 bytes?** A 10 Mb/s Ethernet spans at most 2,500 m, and signals travel at 2 × 10⁸ m/s.

1. One-way propagation: T<sub>p</sub> = 2,500 / (2 × 10⁸) = 12.5 µs.
2. In the worst case, the colliding signal from the far station reaches the sender after one more trip: the sender must still transmit for 2T<sub>p</sub> = 25 µs.
3. Bits transmitted in 25 µs at 10 Mb/s: 25 × 10⁻⁶ × 10 × 10⁶ = 250 bits.
4. The standard rounds up to 512 bits (64 bytes, a 51.2 µs slot time) to allow for repeater delays, the jam signal and a safety margin.

[Result: the minimum frame must satisfy L ≥ 2T<sub>p</sub> × R, giving 250 bits here and 512 bits in the standard. At 1 Gb/s the same rule would demand a much longer frame, so gigabit half-duplex uses carrier extension; full-duplex links have no collisions at all.]{.result}
:::

### Switching

A *switch* builds a *MAC address table* (also called the CAM table, after the content-addressable memory that stores it) by learning. For each arriving frame it does three things. It reads the source address and records "this address is behind this port". It then looks up the destination: if the destination is known, the frame is *forwarded* to that port only; if the destination port is the arrival port, it is *filtered* (dropped); if the destination is broadcast, multicast or unknown, the frame is *flooded* out of every port except the arrival port. Entries are removed after an *ageing time* (300 s on Cisco switches), so a device that is moved is relearned.

<figure>
<svg viewBox="0 0 480 180" width="480">
<rect class="lg" x="6" y="4" width="116" height="168" rx="2" fill="none"/>
<text class="lbl" x="64.0" y="16" text-anchor="middle" >1. Empty table</text>
<rect class="box" x="40" y="50" width="48" height="22" rx="1" />
<text class="sm" x="64" y="64" text-anchor="middle" >Switch</text>
<rect class="box" x="15" y="110" width="18" height="12" rx="1" />
<text class="lbl" x="24" y="119.5" text-anchor="middle" >A</text>
<line class="ln" x1="48" y1="72" x2="24" y2="110" />
<text class="sm" x="40" y="84" text-anchor="middle" >p1</text>
<rect class="box" x="55" y="110" width="18" height="12" rx="1" />
<text class="lbl" x="64" y="119.5" text-anchor="middle" >B</text>
<line class="ln" x1="64" y1="72" x2="64" y2="110" />
<text class="sm" x="64" y="84" text-anchor="middle" >p2</text>
<rect class="box" x="95" y="110" width="18" height="12" rx="1" />
<text class="lbl" x="104" y="119.5" text-anchor="middle" >C</text>
<line class="ln" x1="80" y1="72" x2="104" y2="110" />
<text class="sm" x="88" y="84" text-anchor="middle" >p3</text>
<line class="acc" x1="48" y1="72" x2="24" y2="110" />
<text class="sm" x="64.0" y="34" text-anchor="middle" >A sends to B</text>
<text class="sm" x="64.0" y="44" text-anchor="middle" ></text>
<text class="sm" x="64.0" y="136" text-anchor="middle" style="font-size:6.6px">frame enters port 1</text>
<text class="sm" x="14" y="152" text-anchor="start" >MAC table:</text>
<text class="lbl" x="58" y="152" text-anchor="start" style="font-size:7.4px">(empty)</text>
<rect class="lg" x="126" y="4" width="116" height="168" rx="2" fill="none"/>
<text class="lbl" x="184.0" y="16" text-anchor="middle" >2. Learn A, flood</text>
<rect class="box" x="160" y="50" width="48" height="22" rx="1" />
<text class="sm" x="184" y="64" text-anchor="middle" >Switch</text>
<rect class="box" x="135" y="110" width="18" height="12" rx="1" />
<text class="lbl" x="144" y="119.5" text-anchor="middle" >A</text>
<line class="ln" x1="168" y1="72" x2="144" y2="110" />
<text class="sm" x="160" y="84" text-anchor="middle" >p1</text>
<rect class="box" x="175" y="110" width="18" height="12" rx="1" />
<text class="lbl" x="184" y="119.5" text-anchor="middle" >B</text>
<line class="ln" x1="184" y1="72" x2="184" y2="110" />
<text class="sm" x="184" y="84" text-anchor="middle" >p2</text>
<rect class="box" x="215" y="110" width="18" height="12" rx="1" />
<text class="lbl" x="224" y="119.5" text-anchor="middle" >C</text>
<line class="ln" x1="200" y1="72" x2="224" y2="110" />
<text class="sm" x="208" y="84" text-anchor="middle" >p3</text>
<line class="acc" x1="168" y1="72" x2="144" y2="110" />
<line class="acc" x1="184" y1="72" x2="184" y2="110" stroke-dasharray="3 2"/>
<line class="acc" x1="200" y1="72" x2="224" y2="110" stroke-dasharray="3 2"/>
<text class="sm" x="184.0" y="34" text-anchor="middle" >B unknown: flood</text>
<text class="sm" x="184.0" y="44" text-anchor="middle" ></text>
<text class="sm" x="184.0" y="136" text-anchor="middle" style="font-size:6.6px">copies leave ports 2 and 3</text>
<text class="sm" x="134" y="152" text-anchor="start" >MAC table:</text>
<text class="lbl" x="178" y="152" text-anchor="start" style="font-size:7.4px">A→p1</text>
<rect class="lg" x="246" y="4" width="116" height="168" rx="2" fill="none"/>
<text class="lbl" x="304.0" y="16" text-anchor="middle" >3. B replies</text>
<rect class="box" x="280" y="50" width="48" height="22" rx="1" />
<text class="sm" x="304" y="64" text-anchor="middle" >Switch</text>
<rect class="box" x="255" y="110" width="18" height="12" rx="1" />
<text class="lbl" x="264" y="119.5" text-anchor="middle" >A</text>
<line class="ln" x1="288" y1="72" x2="264" y2="110" />
<text class="sm" x="280" y="84" text-anchor="middle" >p1</text>
<rect class="box" x="295" y="110" width="18" height="12" rx="1" />
<text class="lbl" x="304" y="119.5" text-anchor="middle" >B</text>
<line class="ln" x1="304" y1="72" x2="304" y2="110" />
<text class="sm" x="304" y="84" text-anchor="middle" >p2</text>
<rect class="box" x="335" y="110" width="18" height="12" rx="1" />
<text class="lbl" x="344" y="119.5" text-anchor="middle" >C</text>
<line class="ln" x1="320" y1="72" x2="344" y2="110" />
<text class="sm" x="328" y="84" text-anchor="middle" >p3</text>
<line class="acc" x1="304" y1="72" x2="304" y2="110" />
<line class="acc" x1="288" y1="72" x2="264" y2="110" stroke-dasharray="3 2"/>
<text class="sm" x="304.0" y="34" text-anchor="middle" >dst A known</text>
<text class="sm" x="304.0" y="44" text-anchor="middle" ></text>
<text class="sm" x="304.0" y="136" text-anchor="middle" style="font-size:6.6px">forwarded to port 1 only</text>
<text class="sm" x="254" y="152" text-anchor="start" >MAC table:</text>
<text class="lbl" x="298" y="152" text-anchor="start" style="font-size:7.4px">A→p1, B→p2</text>
<rect class="lg" x="366" y="4" width="116" height="168" rx="2" fill="none"/>
<text class="lbl" x="424.0" y="16" text-anchor="middle" >4. A to B again</text>
<rect class="box" x="400" y="50" width="48" height="22" rx="1" />
<text class="sm" x="424" y="64" text-anchor="middle" >Switch</text>
<rect class="box" x="375" y="110" width="18" height="12" rx="1" />
<text class="lbl" x="384" y="119.5" text-anchor="middle" >A</text>
<line class="ln" x1="408" y1="72" x2="384" y2="110" />
<text class="sm" x="400" y="84" text-anchor="middle" >p1</text>
<rect class="box" x="415" y="110" width="18" height="12" rx="1" />
<text class="lbl" x="424" y="119.5" text-anchor="middle" >B</text>
<line class="ln" x1="424" y1="72" x2="424" y2="110" />
<text class="sm" x="424" y="84" text-anchor="middle" >p2</text>
<rect class="box" x="455" y="110" width="18" height="12" rx="1" />
<text class="lbl" x="464" y="119.5" text-anchor="middle" >C</text>
<line class="ln" x1="440" y1="72" x2="464" y2="110" />
<text class="sm" x="448" y="84" text-anchor="middle" >p3</text>
<line class="acc" x1="408" y1="72" x2="384" y2="110" />
<line class="acc" x1="424" y1="72" x2="424" y2="110" stroke-dasharray="3 2"/>
<text class="sm" x="424.0" y="34" text-anchor="middle" >dst B known</text>
<text class="sm" x="424.0" y="44" text-anchor="middle" ></text>
<text class="sm" x="424.0" y="136" text-anchor="middle" style="font-size:6.6px">forwarded to port 2 only</text>
<text class="sm" x="374" y="152" text-anchor="start" >MAC table:</text>
<text class="lbl" x="418" y="152" text-anchor="start" style="font-size:7.4px">A→p1, B→p2</text>
</svg>
<figcaption><b>Figure 3.8</b> A switch learns by reading the source address of every frame and forwards by looking up the destination. Solid accent lines: the frame entering; dashed accent lines: where it leaves.</figcaption>
</figure>

Flooding an unknown unicast frame is not the same as a broadcast: the frame is still addressed to one MAC, and the receivers other than that one discard it at layer 2. A switch does, however, treat both the same way.

If the table fills, a switch cannot learn and floods every frame for unknown addresses, so it behaves like a hub. An attacker who sends frames with thousands of invented source addresses exploits exactly this to see other people's traffic (*MAC flooding*; mitigation in Pillar 9).

Switches also differ in when they start forwarding. A *store-and-forward* switch receives the whole frame, checks the FCS and then forwards; it adds a delay of one frame time (1,500 bytes take 12 µs at 1 Gb/s and 1.2 µs at 10 Gb/s) but never forwards a corrupted frame. A *cut-through* switch begins forwarding as soon as it has read the destination address, after the 6-byte destination address, so its latency is tens of nanoseconds and independent of frame size, at the price of forwarding damaged frames, which the receiver then discards. Data-centre switches offer cut-through because latency, not error filtering, matters most there.

### Framing and error detection

The bits of a frame must be delimited. Ethernet uses a preamble and start delimiter; serial links often use a flag byte. If the flag could appear inside the data, it must be hidden by *stuffing*. In *bit stuffing* (HDLC) the flag is `01111110`, and the sender inserts a 0 after every run of five 1s in the data, which the receiver removes; the data `01111110` is sent as `011111010`. In *byte stuffing* an escape byte is inserted before any flag or escape byte inside the data.

Errors are detected by adding redundancy. A *parity bit* makes the number of 1s even (or odd) and detects any odd number of flipped bits, but misses even numbers. A *checksum* adds the data in words, as the IP header checksum does (Section 3.5). A *cyclic redundancy check* (CRC) treats the data as a polynomial over arithmetic modulo 2 and divides it by a fixed *generator* polynomial; the remainder is the check value. It detects all burst errors no longer than the degree of the generator and almost all longer ones, which is why Ethernet uses the 32-bit generator of CRC-32.

::: example
**CRC for data 1101011011 with generator 10011 (x⁴ + x + 1).**

1. The generator has 5 bits, so its degree is 4: append four zeros to the data, giving 11010110110000.
2. Divide modulo 2. Wherever the leading bit is 1, XOR the generator under it, aligned to that bit; there is no borrowing. The register after each XOR is shown below.
3. The last four bits are the remainder: 1110. Replace the appended zeros with it and transmit 11010110111110.
4. The receiver divides the whole received word by the same generator. If no bit is damaged the remainder is 0000.

```
start       11010110110000
xor at  0   10011000000000
result      01001110110000
xor at  1   01001100000000
result      00000010110000
xor at  6   00000010011000
result      00000000101000
xor at  8   00000000100110
result      00000000001110      remainder = 1110
```

[Result: frame 11010110111110; the receiver's check gives remainder 0. Addition and subtraction are both XOR, which is why the sender can simply replace the zeros with the remainder.]{.result}
:::

CRC only detects errors. *Hamming codes* correct them. In a Hamming(7,4) code, four data bits are protected by three parity bits placed at positions 1, 2 and 4 of a 7-bit word, each covering the positions whose binary index contains its bit: p1 covers 1, 3, 5, 7; p2 covers 2, 3, 6, 7; p4 covers 4, 5, 6, 7. After a single-bit error the three parity checks, read as a binary number (the *syndrome*), name the position of the faulty bit.

::: example
**Hamming(7,4) with even parity for data 1011.**

1. Place the data at positions 3, 5, 6, 7: d3 = 1, d5 = 0, d6 = 1, d7 = 1.
2. p1 = d3 xor d5 xor d7 = 1 xor 0 xor 1 = 0. p2 = d3 xor d6 xor d7 = 1 xor 1 xor 1 = 1. p4 = d5 xor d6 xor d7 = 0 xor 1 xor 1 = 0.
3. The codeword, positions 1 to 7, is 0110011.
4. Suppose position 5 flips in transit, giving 0110111. The p1 group (1, 3, 5, 7) now sums to an odd number, so c1 = 1; the p2 group (2, 3, 6, 7) is even, so c2 = 0; the p4 group (4, 5, 6, 7) is odd, so c4 = 1.
5. The syndrome c4c2c1 = 101 = 5, so flip position 5 back.

[Result: syndrome 5 locates the error, and the corrected word is 0110011.]{.result}
:::

### Reliable delivery on a link: ARQ

Some links, such as Wi-Fi or satellite, must repair losses themselves; the same ideas reappear in TCP (Section 3.9). In *Stop-and-Wait* the sender transmits one frame and waits for its acknowledgement; a timer expires if none arrives, and the frame is resent. It is simple but wasteful on long links. *Go-Back-N* (GBN) lets the sender have a *window* of N unacknowledged frames; the receiver accepts only the next expected frame, discards the rest and repeats the last acknowledgement, and on timeout the sender resends the lost frame and everything after it. *Selective Repeat* (SR) has the receiver buffer out-of-order frames and acknowledge each, so that only the lost frame is resent, at the price of buffers and more complex bookkeeping.

<figure>
<svg viewBox="0 0 480 246" width="480">
<defs><marker id="aq" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="inkf" d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker></defs>
<text class="lbl" x="78" y="12" text-anchor="middle" >Stop-and-Wait</text>
<text class="sm" x="38" y="19" text-anchor="middle" >Sender</text>
<text class="sm" x="118" y="19" text-anchor="middle" >Receiver</text>
<line class="lg" x1="38" y1="30" x2="38" y2="230" stroke-dasharray="2 2"/>
<line class="lg" x1="118" y1="30" x2="118" y2="230" stroke-dasharray="2 2"/>
<line class="ln" x1="38" y1="28" x2="118" y2="53" marker-end="url(#aq)"/>
<text class="lbl" x="35" y="31" text-anchor="end" style="font-size:6.8px">F0</text>
<line class="lg" x1="118" y1="53" x2="38" y2="78" marker-end="url(#aq)"/>
<text class="sm" x="121" y="56" text-anchor="start" style="font-size:6.8px">A1</text>
<line class="ln" x1="38" y1="78" x2="86.0" y2="93.0" stroke-dasharray="3 2"/>
<path class="acc" d="M82.5,89.5 l7,7 m0,-7 l-7,7"/>
<text class="lbl" x="35" y="81" text-anchor="end" style="font-size:6.8px">F1</text>
<line class="ln" x1="38" y1="128" x2="118" y2="153" marker-end="url(#aq)"/>
<text class="lbl" x="35" y="131" text-anchor="end" style="font-size:6.8px">F1</text>
<line class="lg" x1="118" y1="153" x2="38" y2="178" marker-end="url(#aq)"/>
<text class="sm" x="121" y="156" text-anchor="start" style="font-size:6.8px">A0</text>
<line class="acc" x1="28" y1="118" x2="126" y2="118" stroke-dasharray="2 2"/>
<text class="acct" x="52" y="115" text-anchor="start" style="font-size:7px">timeout</text>
<text class="sm" x="78" y="240" text-anchor="middle" >one frame per round trip</text>
<text class="lbl" x="238" y="12" text-anchor="middle" >Go-Back-N (window 4)</text>
<text class="sm" x="198" y="19" text-anchor="middle" >Sender</text>
<text class="sm" x="278" y="19" text-anchor="middle" >Receiver</text>
<line class="lg" x1="198" y1="30" x2="198" y2="230" stroke-dasharray="2 2"/>
<line class="lg" x1="278" y1="30" x2="278" y2="230" stroke-dasharray="2 2"/>
<line class="ln" x1="198" y1="28" x2="278" y2="53" marker-end="url(#aq)"/>
<text class="lbl" x="195" y="31" text-anchor="end" style="font-size:6.8px">F0</text>
<line class="ln" x1="198" y1="38" x2="278" y2="63" marker-end="url(#aq)"/>
<text class="lbl" x="195" y="41" text-anchor="end" style="font-size:6.8px">F1</text>
<line class="ln" x1="198" y1="48" x2="246.0" y2="63.0" stroke-dasharray="3 2"/>
<path class="acc" d="M242.5,59.5 l7,7 m0,-7 l-7,7"/>
<text class="lbl" x="195" y="51" text-anchor="end" style="font-size:6.8px">F2</text>
<line class="ln" x1="198" y1="58" x2="278" y2="83" marker-end="url(#aq)"/>
<text class="lbl" x="195" y="61" text-anchor="end" style="font-size:6.8px">F3</text>
<line class="lg" x1="278" y1="53" x2="198" y2="78" marker-end="url(#aq)"/>
<text class="sm" x="281" y="56" text-anchor="start" style="font-size:6.8px">A1</text>
<line class="lg" x1="278" y1="63" x2="198" y2="88" marker-end="url(#aq)"/>
<text class="sm" x="281" y="66" text-anchor="start" style="font-size:6.8px">A2</text>
<line class="ln" x1="198" y1="78" x2="278" y2="103" marker-end="url(#aq)"/>
<text class="lbl" x="195" y="81" text-anchor="end" style="font-size:6.8px">F4</text>
<line class="ln" x1="198" y1="88" x2="278" y2="113" marker-end="url(#aq)"/>
<text class="lbl" x="195" y="91" text-anchor="end" style="font-size:6.8px">F5</text>
<line class="lg" x1="278" y1="83" x2="198" y2="108" marker-end="url(#aq)"/>
<text class="sm" x="281" y="86" text-anchor="start" style="font-size:6.8px">A2</text>
<line class="lg" x1="278" y1="103" x2="198" y2="128" marker-end="url(#aq)"/>
<text class="sm" x="281" y="106" text-anchor="start" style="font-size:6.8px">A2</text>
<line class="lg" x1="278" y1="113" x2="198" y2="138" marker-end="url(#aq)"/>
<text class="sm" x="281" y="116" text-anchor="start" style="font-size:6.8px">A2</text>
<line class="ln" x1="198" y1="150" x2="278" y2="175" marker-end="url(#aq)"/>
<text class="lbl" x="195" y="153" text-anchor="end" style="font-size:6.8px">F2</text>
<line class="ln" x1="198" y1="160" x2="278" y2="185" marker-end="url(#aq)"/>
<text class="lbl" x="195" y="163" text-anchor="end" style="font-size:6.8px">F3</text>
<line class="ln" x1="198" y1="170" x2="278" y2="195" marker-end="url(#aq)"/>
<text class="lbl" x="195" y="173" text-anchor="end" style="font-size:6.8px">F4</text>
<line class="ln" x1="198" y1="180" x2="278" y2="205" marker-end="url(#aq)"/>
<text class="lbl" x="195" y="183" text-anchor="end" style="font-size:6.8px">F5</text>
<line class="lg" x1="278" y1="175" x2="198" y2="200" marker-end="url(#aq)"/>
<text class="sm" x="281" y="178" text-anchor="start" style="font-size:6.8px">A3</text>
<line class="lg" x1="278" y1="185" x2="198" y2="210" marker-end="url(#aq)"/>
<text class="sm" x="281" y="188" text-anchor="start" style="font-size:6.8px">A4</text>
<line class="lg" x1="278" y1="195" x2="198" y2="220" marker-end="url(#aq)"/>
<text class="sm" x="281" y="198" text-anchor="start" style="font-size:6.8px">A5</text>
<line class="lg" x1="278" y1="205" x2="198" y2="230" marker-end="url(#aq)"/>
<text class="sm" x="281" y="208" text-anchor="start" style="font-size:6.8px">A6</text>
<line class="acc" x1="188" y1="140" x2="286" y2="140" stroke-dasharray="2 2"/>
<text class="acct" x="212" y="137" text-anchor="start" style="font-size:7px">timeout</text>
<text class="sm" x="238" y="240" text-anchor="middle" >F2 lost: F2 to F5 all resent</text>
<text class="lbl" x="398" y="12" text-anchor="middle" >Selective Repeat (window 4)</text>
<text class="sm" x="358" y="19" text-anchor="middle" >Sender</text>
<text class="sm" x="438" y="19" text-anchor="middle" >Receiver</text>
<line class="lg" x1="358" y1="30" x2="358" y2="230" stroke-dasharray="2 2"/>
<line class="lg" x1="438" y1="30" x2="438" y2="230" stroke-dasharray="2 2"/>
<line class="ln" x1="358" y1="28" x2="438" y2="53" marker-end="url(#aq)"/>
<text class="lbl" x="355" y="31" text-anchor="end" style="font-size:6.8px">F0</text>
<line class="ln" x1="358" y1="38" x2="438" y2="63" marker-end="url(#aq)"/>
<text class="lbl" x="355" y="41" text-anchor="end" style="font-size:6.8px">F1</text>
<line class="ln" x1="358" y1="48" x2="406.0" y2="63.0" stroke-dasharray="3 2"/>
<path class="acc" d="M402.5,59.5 l7,7 m0,-7 l-7,7"/>
<text class="lbl" x="355" y="51" text-anchor="end" style="font-size:6.8px">F2</text>
<line class="ln" x1="358" y1="58" x2="438" y2="83" marker-end="url(#aq)"/>
<text class="lbl" x="355" y="61" text-anchor="end" style="font-size:6.8px">F3</text>
<line class="lg" x1="438" y1="53" x2="358" y2="78" marker-end="url(#aq)"/>
<text class="sm" x="441" y="56" text-anchor="start" style="font-size:6.8px">A0</text>
<line class="lg" x1="438" y1="63" x2="358" y2="88" marker-end="url(#aq)"/>
<text class="sm" x="441" y="66" text-anchor="start" style="font-size:6.8px">A1</text>
<line class="ln" x1="358" y1="78" x2="438" y2="103" marker-end="url(#aq)"/>
<text class="lbl" x="355" y="81" text-anchor="end" style="font-size:6.8px">F4</text>
<line class="ln" x1="358" y1="88" x2="438" y2="113" marker-end="url(#aq)"/>
<text class="lbl" x="355" y="91" text-anchor="end" style="font-size:6.8px">F5</text>
<line class="lg" x1="438" y1="83" x2="358" y2="108" marker-end="url(#aq)"/>
<text class="sm" x="441" y="86" text-anchor="start" style="font-size:6.8px">A3</text>
<line class="lg" x1="438" y1="103" x2="358" y2="128" marker-end="url(#aq)"/>
<text class="sm" x="441" y="106" text-anchor="start" style="font-size:6.8px">A4</text>
<line class="lg" x1="438" y1="113" x2="358" y2="138" marker-end="url(#aq)"/>
<text class="sm" x="441" y="116" text-anchor="start" style="font-size:6.8px">A5</text>
<line class="ln" x1="358" y1="150" x2="438" y2="175" marker-end="url(#aq)"/>
<text class="lbl" x="355" y="153" text-anchor="end" style="font-size:6.8px">F2</text>
<line class="lg" x1="438" y1="175" x2="358" y2="200" marker-end="url(#aq)"/>
<text class="sm" x="441" y="178" text-anchor="start" style="font-size:6.8px">A2</text>
<line class="acc" x1="348" y1="140" x2="446" y2="140" stroke-dasharray="2 2"/>
<text class="acct" x="372" y="137" text-anchor="start" style="font-size:7px">timeout</text>
<text class="sm" x="398" y="240" text-anchor="middle" >only F2 resent; 3, 4, 5 buffered</text>
</svg>
<figcaption><b>Figure 3.9</b> Three ARQ schemes after the loss of frame 2. Acknowledgements are shown by the next frame expected (cumulative) in Stop-and-Wait and Go-Back-N, and per frame (A3 means frame 3 received) in Selective Repeat. Go-Back-N discards out-of-order frames and repeats A2; Selective Repeat buffers them.</figcaption>
</figure>

Let a = T<sub>p</sub> / T<sub>t</sub> be the ratio of the one-way propagation time to the frame transmission time. The sender can send for T<sub>t</sub>, then idles for a round trip of 2T<sub>p</sub>; a window that covers the whole 1 + 2a frame times keeps the link busy. Sequence numbers are written in n bits, so they wrap modulo 2<sup>n</sup>, and the window must be small enough that an old frame is never mistaken for a new one: in GBN the window may be at most 2<sup>n</sup> − 1, whereas in SR it may be at most 2<sup>n−1</sup>, because the sender's and receiver's windows must not overlap.

::: example
**A 1 Mb/s link carries 1,000-bit frames, and the one-way propagation delay is 20 ms.**

1. T<sub>t</sub> = 1,000 / 10⁶ = 1 ms, so a = 20 ms / 1 ms = 20.
2. Stop-and-Wait efficiency: η = 1 / (1 + 2a) = 1 / 41 ≈ 2.4%. The link carries one frame in every 41 ms.
3. A window of 1 + 2a = 41 frames gives 100% (and any window W < 41 gives η = W / 41).
4. Sequence numbers for W = 41: GBN needs 2<sup>n</sup> − 1 ≥ 41, so 2<sup>n</sup> ≥ 42 and n = 6. SR needs 2<sup>n−1</sup> ≥ 41, so n − 1 ≥ 6 and n = 7.

[Result: 2.4%; a window of 41 gives full utilisation; 6 bits for GBN and 7 bits for SR.]{.result}
:::

::: trap
*Claim:* "A CRC corrects errors, and a longer CRC corrects more." *Why it is wrong:* a CRC is a detection code; the receiver can only tell that a frame is bad. *Correct statement:* Ethernet drops a frame whose FCS fails and leaves recovery to the higher layers (TCP resends); correction is the job of codes such as Hamming or the forward error correction in Wi-Fi and cellular.
:::

::: lens
[QUALCOMM · BROADCOM · NOKIA · ARISTA · CISCO]{.co}

Qualcomm, Broadcom and Nokia interviews like the numerical problems: the CRC, the window limits and Stop-and-Wait efficiency (Q3.6 to Q3.8). Cisco and Arista ask about learning, flooding and the full CAM table (Q3.5), and Arista adds cut-through (Q3.9). A strong answer states the formula before the arithmetic and checks the units.
:::

::: lab
`LAB 3.3 · 25 MIN` Three small tasks. (i) In Packet Tracer, connect three PCs to one switch, run `show mac address-table` before and after a ping from PC0 to PC1, then `clear mac address-table dynamic`. (ii) In Wireshark, apply `eth.dst == ff:ff:ff:ff:ff:ff` and list the protocols that appear. (iii) In Python, check CRC-32.

```
Switch# show mac address-table dynamic
 Vlan    Mac Address       Type        Ports
    1    0001.6446.e5a2    DYNAMIC     Fa0/1
    1    0003.e4a1.b3c4    DYNAMIC     Fa0/2
```

```python
import zlib
print(hex(zlib.crc32(b"123456789")))   # 0xcbf43926, the standard check value
```

**What you should notice:** before the ping the table is empty, and after it holds exactly the source addresses seen, one per port. The broadcast filter shows ARP and DHCP; broadcast frames are never sources, so they never appear in the table.
:::

::: check
1. A host sends a frame to an address that is not in the switch's table. What does the switch do, and what does it learn? [^c3-7]
2. Which Ethernet field makes the receiver pass the payload to IPv4 rather than ARP? [^c3-8]
3. For Stop-and-Wait, what happens to the efficiency if the propagation delay is doubled? [^c3-9]
:::

[^c3-7]: It floods the frame out of every port except the arrival port, and it learns the *source* address on the arrival port.
[^c3-8]: The EtherType field: 0x0800 for IPv4, 0x0806 for ARP.
[^c3-9]: a doubles, so η = 1 / (1 + 2a) roughly halves when a is large (1/41 becomes 1/81).

:::
