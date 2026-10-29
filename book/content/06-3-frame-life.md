::: {.p6}

## [6.5]{.sec}The 802.11 frame, bit by bit [Must · ■■□]{.tag} {#s6-5}

An 802.11 frame has the same three-part shape as any link-layer frame, a header, a body and a trailer, but its header is more elaborate than Ethernet's. This is because a wireless frame must say what kind of frame it is (data, management or control), in which direction it is going relative to the wired network, and which of up to four stations are involved. Unlike IP, whose fields are in network (big-endian) byte order, 802.11 transmits multi-byte fields least-significant byte first. A hand decoder must therefore swap the two bytes of Frame Control before reading it.

<figure>
<svg viewBox="0 0 480 170" width="480"><rect class="box" x="15" y="24" width="34" height="24" /><text class="sm" x="32.0" y="40" text-anchor="middle" >FC</text><text class="sm" x="32.0" y="20" text-anchor="middle" >2 B</text><rect class="box" x="49" y="24" width="34" height="24" /><text class="sm" x="66.0" y="40" text-anchor="middle" >Dur/ID</text><text class="sm" x="66.0" y="20" text-anchor="middle" >2 B</text><rect class="box" x="83" y="24" width="54" height="24" /><text class="sm" x="110.0" y="40" text-anchor="middle" >Addr1</text><text class="sm" x="110.0" y="20" text-anchor="middle" >6 B</text><rect class="box" x="137" y="24" width="54" height="24" /><text class="sm" x="164.0" y="40" text-anchor="middle" >Addr2</text><text class="sm" x="164.0" y="20" text-anchor="middle" >6 B</text><rect class="box" x="191" y="24" width="54" height="24" /><text class="sm" x="218.0" y="40" text-anchor="middle" >Addr3</text><text class="sm" x="218.0" y="20" text-anchor="middle" >6 B</text><rect class="box" x="245" y="24" width="34" height="24" /><text class="sm" x="262.0" y="40" text-anchor="middle" >Seq</text><text class="sm" x="262.0" y="20" text-anchor="middle" >2 B</text><rect class="box" x="279" y="24" width="54" height="24" stroke-dasharray="3 2"/><text class="sm" x="306.0" y="40" text-anchor="middle" >Addr4</text><text class="sm" x="306.0" y="20" text-anchor="middle" >6 B</text><rect class="box" x="333" y="24" width="30" height="24" stroke-dasharray="3 2"/><text class="sm" x="348.0" y="40" text-anchor="middle" >QoS</text><text class="sm" x="348.0" y="20" text-anchor="middle" >2 B</text><rect class="box" x="363" y="24" width="30" height="24" stroke-dasharray="3 2"/><text class="sm" x="378.0" y="40" text-anchor="middle" >HTC</text><text class="sm" x="378.0" y="20" text-anchor="middle" >4 B</text><rect class="fill" x="393" y="24" width="44" height="24" /><text class="sm" x="415.0" y="40" text-anchor="middle" >Body</text><text class="sm" x="415.0" y="20" text-anchor="middle" >var.</text><rect class="box" x="437" y="24" width="28" height="24" /><text class="sm" x="451.0" y="40" text-anchor="middle" >FCS</text><text class="sm" x="451.0" y="20" text-anchor="middle" >4 B</text><text class="sm" x="15" y="62" text-anchor="start" >Dashed fields appear only in some frames: Addr4 (WDS/mesh), QoS Control (QoS data), HT Control (+HTC bit set).</text><text class="lbl" x="15" y="12" text-anchor="start" >MAC header 24 bytes (up to 36)</text><text class="lbl" x="15" y="82" text-anchor="start" >Frame Control (16 bits, bit 0 is sent first)</text><rect class="box" x="16" y="90" width="56" height="26" /><text class="sm" x="44.0" y="106" text-anchor="middle" >Version</text><text class="sm" x="44.0" y="128" text-anchor="middle" >b0-1</text><rect class="box" x="72" y="90" width="56" height="26" /><text class="sm" x="100.0" y="106" text-anchor="middle" >Type</text><text class="sm" x="100.0" y="128" text-anchor="middle" >b2-3</text><rect class="box" x="128" y="90" width="112" height="26" /><text class="sm" x="184.0" y="106" text-anchor="middle" >Subtype</text><text class="sm" x="184.0" y="128" text-anchor="middle" >b4-7</text><rect class="hl" x="240" y="90" width="28" height="26" stroke="#1A1D23" stroke-width=".9"/><text class="sm" x="254.0" y="106" text-anchor="middle" >To DS</text><text class="sm" x="254.0" y="128" text-anchor="middle" >b8</text><rect class="hl" x="268" y="90" width="28" height="26" stroke="#1A1D23" stroke-width=".9"/><text class="sm" x="282.0" y="106" text-anchor="middle" >Fr DS</text><text class="sm" x="282.0" y="128" text-anchor="middle" >b9</text><rect class="box" x="296" y="90" width="28" height="26" /><text class="sm" x="310.0" y="106" text-anchor="middle" >MF</text><text class="sm" x="310.0" y="128" text-anchor="middle" >b10</text><rect class="box" x="324" y="90" width="28" height="26" /><text class="sm" x="338.0" y="106" text-anchor="middle" >Retry</text><text class="sm" x="338.0" y="128" text-anchor="middle" >b11</text><rect class="box" x="352" y="90" width="28" height="26" /><text class="sm" x="366.0" y="106" text-anchor="middle" >PM</text><text class="sm" x="366.0" y="128" text-anchor="middle" >b12</text><rect class="box" x="380" y="90" width="28" height="26" /><text class="sm" x="394.0" y="106" text-anchor="middle" >MD</text><text class="sm" x="394.0" y="128" text-anchor="middle" >b13</text><rect class="box" x="408" y="90" width="28" height="26" /><text class="sm" x="422.0" y="106" text-anchor="middle" >Prot</text><text class="sm" x="422.0" y="128" text-anchor="middle" >b14</text><rect class="box" x="436" y="90" width="28" height="26" /><text class="sm" x="450.0" y="106" text-anchor="middle" >+HTC</text><text class="sm" x="450.0" y="128" text-anchor="middle" >b15</text><text class="sm" x="15" y="140" text-anchor="start" >MF more fragments, PM power management, MD more data, Prot protected frame.</text><text class="sm" x="15" y="152" text-anchor="start" >Example: bytes 08 41 on the air read as 0x4108: type 2 (data), subtype 0, To DS = 1, Protected = 1.</text></svg>
<figcaption><b>Figure 6.8</b> The 802.11 MAC header and the bit layout of its Frame Control field.</figcaption>
</figure>

### Frame Control

The first two bytes, the *Frame Control* field, describe the frame. Reading bit 0 first (the first bit sent):

| Bits | Field | Meaning |
|------|--------------------|------------------------------------------------------------|
| 0–1 | Protocol version | always 0 |
| 2–3 | Type | 0 management, 1 control, 2 data |
| 4–7 | Subtype | the particular frame within the type |
| 8 | To DS | frame is going to the distribution system (client to AP) |
| 9 | From DS | frame is coming from the distribution system (AP to client) |
| 10 | More Fragments | more fragments of this MSDU follow |
| 11 | Retry | this is a retransmission; the sender sets it so the receiver may drop duplicates |
| 12 | Power Management | the sender will sleep after this frame ([§6.8](#s6-8){.ref}) |
| 13 | More Data | the AP holds more buffered frames for a sleeping STA |
| 14 | Protected Frame | the body is encrypted (CCMP, GCMP) |
| 15 | +HTC / Order | an HT/VHT/HE Control field is present |

::: example
**Decoding two Frame Controls.** The bytes on the air are `08 41` for a data frame and `80 00` for a beacon.

1. Swap the bytes of the first: 0x4108 = 0100 0001 0000 1000 in binary.
2. Bits 0–1 = 00 (version 0); bits 2–3 = 10 (type 2, data); bits 4–7 = 0000 (subtype 0, plain data).
3. Byte 1 is 0x41 = 0100 0001: bit 8 (To DS) = 1, bit 9 (From DS) = 0, bit 14 (Protected) = 1.
4. The beacon: 0x0080, bits 2–3 = 00 (management) and bits 4–7 = 1000 (subtype 8, beacon); no flags.

[Result: `08 41` is a protected data frame from a station to its AP; `80 00` is a beacon.]{.result}
:::

Wireshark and `tcpdump` combine type and subtype into one number, (type × 16) + subtype, which is the value used in the display filter `wlan.fc.type_subtype`. The ones worth memorising are in the next table.

| Type | Frame (subtype) | Code | Purpose |
|-----------|--------------------------------------|--------------|----------------------------------------|
| Management | Association Request / Response (0 / 1) | 0x00 / 0x01 | join the BSS; response carries status and AID |
| Management | Reassociation Request / Response (2 / 3) | 0x02 / 0x03 | move to another AP of the ESS |
| Management | Probe Request / Response (4 / 5) | 0x04 / 0x05 | active scan |
| Management | Beacon (8) | 0x08 | periodic advertisement of the BSS |
| Management | Disassociation (10), Authentication (11), Deauthentication (12) | 0x0a, 0x0b, 0x0c | end association, open or SAE exchange, end all |
| Management | Action (13) | 0x0d | block-ack setup, 802.11k/v/r, SA Query |
| Control | Trigger (2) | 0x12 | 802.11ax, schedules uplink OFDMA |
| Control | Block Ack Request / Block Ack (8 / 9) | 0x18 / 0x19 | selective acknowledgement of an aggregate |
| Control | PS-Poll (10) | 0x1a | a sleeping STA asks for a buffered frame |
| Control | RTS / CTS / ACK (11 / 12 / 13) | 0x1b / 0x1c / 0x1d | reservation and acknowledgement |
| Data | Data (0), Null (4) | 0x20, 0x24 | payload; Null carries only the power-management bit |
| Data | QoS Data (8), QoS Null (12) | 0x28, 0x2c | payload with a QoS Control field |

### The addresses: four fields, three meanings

A frame has up to four address fields, because a frame relayed by an AP involves up to four parties: the original source, the final destination, and the two radios that carry it across one hop. The *receiver address* (RA) and *transmitter address* (TA) are the radio-hop endpoints and are always Address 1 and Address 2. The *source address* (SA) and *destination address* (DA) are the end systems. The To DS and From DS bits tell which role each field plays.

| To DS | From DS | Address 1 | Address 2 | Address 3 | Address 4 | Typical case |
|------|-------|------------|------------|------------|------------|------------------------------|
| 0 | 0 | RA = DA | TA = SA | BSSID | not present | IBSS, management frames |
| 1 | 0 | RA = BSSID | TA = SA | DA | not present | station to AP |
| 0 | 1 | RA = DA | TA = BSSID | SA | not present | AP to station |
| 1 | 1 | RA | TA | DA | SA | AP to AP (WDS, mesh) |

Consider a laptop (SA) sending to a file server (DA) behind the AP. The frame to the AP has To DS = 1: Address 1 is the AP's BSSID (the receiver), Address 2 the laptop (the transmitter and source) and Address 3 the server (the destination). The AP, after checking the frame, transmits an Ethernet frame onto the wire; in the reverse direction the AP sends with From DS = 1, Address 1 the laptop, Address 2 its own BSSID and Address 3 the server as source. The fourth address appears only when a frame is relayed wirelessly from AP to AP, because then neither the transmitter nor the receiver is an end system.

### Remaining fields and the trailer

The *Duration/ID* field (2 bytes) holds the number of microseconds the exchange will occupy, from which listeners set their NAV ([§6.4](#s6-4){.ref}); in a PS-Poll it carries the association ID instead. The *Sequence Control* field is a 12-bit sequence number and a 4-bit fragment number, so that duplicates created by retransmissions can be discarded. The *QoS Control* field (2 bytes, present in QoS data frames) holds the traffic identifier (TID, 4 bits), the acknowledgement policy and whether the body is an A-MSDU ([§6.8](#s6-8){.ref}). The *HT/VHT/HE Control* field (4 bytes) carries link-adaptation feedback. The body is followed by a 4-byte *frame check sequence* (CRC-32) over the whole frame; a receiver silently drops a frame whose FCS is wrong, which is why no negative acknowledgement exists. When encryption is on, CCMP adds an 8-byte header (a 48-bit packet number and the key identifier) and an 8-byte integrity check, so an encrypted frame is 16 bytes longer than a clear one.

The short control frames show how compact the format can be: an ACK or CTS is only Frame Control, Duration, a receiver address and the FCS, 14 bytes; an RTS adds the transmitter address, 20 bytes. A management frame has a 24-byte header, a fixed part and a sequence of *information elements* (IEs), each coded as one byte of element ID, one byte of length and the value. A beacon's body is as follows.

| Field or IE | Size | Content in the example |
|--------------------------|--------|--------------------------------------------------|
| Timestamp | 8 B | the AP's microsecond clock, for synchronisation |
| Beacon interval | 2 B | 100 TU (1 TU = 1,024 µs, so 102.4 ms) |
| Capability information | 2 B | ESS bit, privacy bit, short preamble |
| SSID (ID 0) | 1 + 6 B | "IITLab" |
| Supported rates (ID 1), DS parameter set (ID 3) | variable | basic rates; channel 6 (2.4 GHz only) |
| TIM (ID 5) | variable | DTIM count and period, bitmap of stations with buffered data |
| RSN (ID 48) | variable | group cipher CCMP, pairwise CCMP, AKM PSK |
| HT, VHT, HE capabilities | variable | widths, streams, MCS sets, features supported |

::: example
**Decode a QoS data frame header.** The first 32 bytes of a captured frame are

`88 41 2c 00 | 02 11 22 33 44 aa | 02 11 22 33 44 bb | 02 00 5e 00 00 01 | 10 07 | 06 00 | 01 00 00 20 00 00 00 00`

1. `88 41`: type 2 (data), subtype 8 (QoS data), To DS = 1, Protected = 1. Because To DS = 1 and From DS = 0, the table gives Address 1 = BSSID, Address 2 = source, Address 3 = destination.
2. `2c 00` is 0x002c = 44 µs of duration, which covers a SIFS and the ACK.
3. Address 1 is `02:11:22:33:44:aa`, the AP; Address 2 is `02:11:22:33:44:bb`, the station; Address 3 is `02:00:5e:00:00:01`, the gateway.
4. `10 07` is 0x0710: fragment number = low 4 bits = 0, sequence number = 0x0710 ≫ 4 = 0x71 = 113.
5. `06 00` is the QoS Control: TID = 6, which maps to the voice access category.
6. The final 8 bytes are the CCMP header: packet number 1 (bytes `01 00` and `00 00 00 00`), and the byte `20`, whose bit 5 is the ExtIV flag, with key identifier 0. The body that follows is ciphertext.

[Result: a voice-priority frame from `…:bb` to the gateway `…:01`, relayed by AP `…:aa`, with packet number 1.]{.result}
:::

::: lab
`LAB 6.5 · 15 MIN` Write the Frame Control decoder in C and feed it the two examples above. In a real capture the radiotap header precedes the frame; it begins with a version byte, a pad byte and a 16-bit little-endian length, and that length must be skipped.

```c
#include <stdio.h>
#include <stdint.h>
int main(void) {
    uint8_t wire[2][2] = { {0x08, 0x41}, {0x80, 0x00} };
    for (int i = 0; i < 2; i++) {
        uint16_t fc = wire[i][0] | (wire[i][1] << 8);   /* little-endian */
        printf("fc=0x%04x ver=%u type=%u subtype=%u ", fc,
               fc & 3, (fc >> 2) & 3, (fc >> 4) & 15);
        printf("tods=%u fromds=%u retry=%u prot=%u\n",
               (fc >> 8) & 1, (fc >> 9) & 1, (fc >> 11) & 1, (fc >> 14) & 1);
    }
    return 0;
}
```

```
fc=0x4108 ver=0 type=2 subtype=0 tods=1 fromds=0 retry=0 prot=1
fc=0x0080 ver=0 type=0 subtype=8 tods=0 fromds=0 retry=0 prot=0
```

**What you should notice:** the byte order is the only trap. Declaring a `struct` with bit-fields would give a layout that depends on the compiler and the host's endianness, so shifts and masks on a `uint16_t` built from the bytes are the portable way. This is the same lesson as `htons` in [§7.10](#s7-10){.ref}, in the opposite direction.
:::

::: trap
*Claim:* "Address 3 is the destination", or "the first address is the destination." *Why it is wrong:* Address 1 is always the receiver of this radio hop, and the meaning of Address 3 depends on To DS and From DS (the destination when To DS = 1, the source when From DS = 1, the BSSID in management frames). *Correct statement:* read the two DS bits first, then the table.
:::

::: lens
[QUALCOMM · BROADCOM · JUNIPER]{.co}

"Explain To DS and From DS and the four addresses" is a standard WLAN question; so is "what is in a beacon". A strong answer gives the table, walks through one STA-to-server frame in both directions, and notes the little-endian byte order. Follow-ups: what the Retry bit is for, what the sequence number prevents, and why control frames have no sequence number.
:::

::: check
1. A frame has To DS = 0, From DS = 1. Which address is the source? [^c65-1]
2. What is the length of an ACK frame? [^c65-2]
3. Which Wireshark subtype codes are a beacon and a deauthentication? [^c65-3]
:::

[^c65-1]: Address 3 (Address 1 is the destination, Address 2 the BSSID).
[^c65-2]: 14 bytes: Frame Control 2, Duration 2, receiver address 6, FCS 4.
[^c65-3]: 0x08 and 0x0c.

## [6.6]{.sec}The connection lifecycle [Must · ■■□]{.tag} {#s6-6}

A station connects to a network in five phases: it discovers the AP, performs an initial 802.11 exchange, associates, establishes keys, and only then obtains an IP address. The order matters because each phase unlocks the next. Each is a state of a small state machine kept by the AP: in State 1 the station is unauthenticated and unassociated and may send only a few management frames; in State 2 it is authenticated but not associated; in State 3 it is authenticated and associated, which allows data frames. A *deauthentication* returns the station to State 1 and a *disassociation* to State 2. In a secured network a second gate, the 802.1X *controlled port*, stays blocked in State 3 until the keys are installed, and until then only the key-exchange frames pass.

<figure>
<svg viewBox="0 0 480 300" width="480"><defs><marker id="i5" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="a5" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><text class="lbl" x="120" y="12" text-anchor="middle" >STA</text><text class="lbl" x="360" y="12" text-anchor="middle" >AP</text><line class="lg" x1="120" y1="18" x2="120" y2="330" /><line class="lg" x1="360" y1="18" x2="360" y2="330" /><line class="ln" x1="358" y1="34" x2="122" y2="34" marker-end="url(#i5)"/><text class="sm" x="240" y="30" text-anchor="middle" >Beacon (periodic)</text><line class="ln" x1="122" y1="51" x2="358" y2="51" marker-end="url(#i5)"/><text class="sm" x="240" y="47" text-anchor="middle" >Probe Request (active scan)</text><line class="ln" x1="358" y1="68" x2="122" y2="68" marker-end="url(#i5)"/><text class="sm" x="240" y="64" text-anchor="middle" >Probe Response</text><rect class="fill" x="4" y="22" width="56" height="45" /><text class="sm" x="32" y="48.5" text-anchor="middle" >Discovery</text><line class="lg" x1="4" y1="77" x2="476" y2="77" stroke-dasharray="2 3"/><line class="ln" x1="122" y1="91" x2="358" y2="91" marker-end="url(#i5)"/><text class="sm" x="240" y="87" text-anchor="middle" >Authentication, seq 1 (open)</text><line class="ln" x1="358" y1="108" x2="122" y2="108" marker-end="url(#i5)"/><text class="sm" x="240" y="104" text-anchor="middle" >Authentication, seq 2</text><rect class="fill" x="4" y="79" width="56" height="28" /><text class="sm" x="32" y="97.0" text-anchor="middle" >802.11 auth</text><line class="lg" x1="4" y1="117" x2="476" y2="117" stroke-dasharray="2 3"/><line class="ln" x1="122" y1="131" x2="358" y2="131" marker-end="url(#i5)"/><text class="sm" x="240" y="127" text-anchor="middle" >Association Request (rates, HT/VHT/HE, RSN)</text><line class="ln" x1="358" y1="148" x2="122" y2="148" marker-end="url(#i5)"/><text class="sm" x="240" y="144" text-anchor="middle" >Association Response (status 0, AID)</text><rect class="fill" x="4" y="119" width="56" height="28" /><text class="sm" x="32" y="137.0" text-anchor="middle" >Association</text><line class="lg" x1="4" y1="157" x2="476" y2="157" stroke-dasharray="2 3"/><line class="acc" x1="358" y1="171" x2="122" y2="171" marker-end="url(#a5)"/><text class="sm" x="240" y="167" text-anchor="middle" >EAPOL-Key 1/4  ANonce</text><line class="acc" x1="122" y1="188" x2="358" y2="188" marker-end="url(#a5)"/><text class="sm" x="240" y="184" text-anchor="middle" >EAPOL-Key 2/4  SNonce, MIC</text><line class="acc" x1="358" y1="205" x2="122" y2="205" marker-end="url(#a5)"/><text class="sm" x="240" y="201" text-anchor="middle" >EAPOL-Key 3/4  GTK, MIC</text><line class="acc" x1="122" y1="222" x2="358" y2="222" marker-end="url(#a5)"/><text class="sm" x="240" y="218" text-anchor="middle" >EAPOL-Key 4/4  MIC</text><rect class="fill" x="4" y="159" width="56" height="62" /><text class="sm" x="32" y="194.0" text-anchor="middle" >4-way</text><line class="lg" x1="4" y1="231" x2="476" y2="231" stroke-dasharray="2 3"/><line class="ln" x1="122" y1="245" x2="358" y2="245" marker-end="url(#i5)"/><text class="sm" x="240" y="241" text-anchor="middle" >DHCP Discover / Request</text><line class="ln" x1="358" y1="262" x2="122" y2="262" marker-end="url(#i5)"/><text class="sm" x="240" y="258" text-anchor="middle" >DHCP Offer / Ack (encrypted)</text><line class="ln" x1="122" y1="279" x2="358" y2="279" marker-end="url(#i5)"/><text class="sm" x="240" y="275" text-anchor="middle" >Encrypted data (CCMP)</text><rect class="fill" x="4" y="233" width="56" height="45" /><text class="sm" x="32" y="259.5" text-anchor="middle" >IP</text><line class="lg" x1="4" y1="288" x2="476" y2="288" stroke-dasharray="2 3"/></svg>
<figcaption><b>Figure 6.9</b> The connection lifecycle of a WPA2-Personal station, in the order seen in a monitor-mode capture.</figcaption>
</figure>

**Discovery.** In *passive scanning* the station tunes to each channel in turn and listens for beacons, which each BSS sends every 102.4 ms; the dwell per channel must be at least one beacon interval, so a full scan is slow. In *active scanning* the station sends a *probe request* (with a wildcard SSID, or with the SSID of a known network) and every AP that hears it replies with a *probe response* carrying the same capabilities as a beacon; the dwell is only about 20 ms per channel. Phones mix both: active scans on channels where probing is allowed, passive on channels that need radar detection. In 6 GHz a station scans first the *preferred scanning channels*, one in four, and learns about the other channels from reports inside the 2.4 and 5 GHz beacons.

**Open authentication.** The station sends an *Authentication* frame (algorithm 0, sequence 1) and the AP answers (sequence 2, status 0). In modern networks this exchange is a formality that carries no secret; it survives for compatibility with the original state machine. WEP's shared-key authentication (algorithm 1) is obsolete, and WPA3 replaces the open exchange by the SAE commit and confirm frames (algorithm 3, [§6.7](#s6-7){.ref}).

**Association.** The *association request* states the SSID, the supported rates and the station's HT, VHT and HE capabilities (what it can do), a listen interval for power save, and its security choices in the RSN element. The AP answers with a status (0 means success) and an *association ID* (AID), a number from 1 to 2007 that identifies the station in the TIM bitmap. The AP checks that the RSN element matches its policy.

**Key establishment.** If the network uses a pre-shared key, the pairwise master key is already known to both sides and the *4-way handshake* follows at once ([§6.7](#s6-7){.ref}). In an enterprise network the station and a RADIUS server first run an EAP method through the AP, which relays the exchange (EAPOL between station and AP, RADIUS between AP and server); the generic exchange is explained in [§9.12](#s9-12){.ref}, and its Wi-Fi-specific output, the PMK delivered to the AP, is covered in [§6.7](#s6-7){.ref}.

**IP configuration.** With keys installed, the station sends DHCP and ARP ([§3.6](#s3-6){.ref}), encrypted like any other data. This explains why a monitor-mode capture shows DHCP only when the 4-way handshake has been captured and the passphrase is known to Wireshark.

The table gives a typical capture for a WPA2-Personal client, as a monitor-mode sniffer would see it. Times are indicative.

| # | Frame | From → to | Key fields | Why it matters |
|----|------------------|------------|------------------------------|------------------------------|
| 1 | Beacon | AP → broadcast | SSID, RSN (CCMP, PSK), TIM, capabilities | passive discovery; repeated every 102.4 ms |
| 2 | Probe Request | STA → broadcast | SSID (wildcard or named), rates | active scan; may use a random MAC |
| 3 | Probe Response | AP → STA | as beacon, without TIM | answers only the prober |
| 4–5 | Authentication ×2 | STA ⇄ AP | algorithm 0, sequence 1 then 2, status 0 | opens State 2 |
| 6–7 | Association Request, Response | STA ⇄ AP | rates, HT/VHT/HE, RSN; status 0, AID | opens State 3; the port is still blocked |
| 8 | EAPOL-Key 1 of 4 | AP → STA | ANonce, replay counter | STA can now derive the PTK |
| 9 | EAPOL-Key 2 of 4 | STA → AP | SNonce, MIC, RSN | proves the STA knows the PMK |
| 10 | EAPOL-Key 3 of 4 | AP → STA | MIC, encrypted GTK, Install | AP proves the same; keys to install |
| 11 | EAPOL-Key 4 of 4 | STA → AP | MIC | confirms; port opens |
| 12–15 | DHCP Discover, Offer, Request, Ack | STA ⇄ server | inside QoS Data, protected | visible only after decryption |
| 16 | ARP for the gateway | STA → broadcast | inside protected data | first data frames |

The filter `eapol || wlan.fc.type_subtype == 0x0b || wlan.fc.type_subtype == 0x00` isolates the authentication, association and handshake frames in Wireshark ([§8.8](#s8-8){.ref}). A deauthentication frame carries a *reason code* that says why the connection ended; the common ones are 1 (unspecified), 2 (previous authentication no longer valid), 3 (the station is leaving), 4 (inactivity), 15 (4-way handshake timeout, usually a wrong passphrase) and 23 (802.1X authentication failed).

::: trap
*Claim:* "802.11 authentication is the security step." *Why it is wrong:* the open exchange has no credentials. Since WPA2, the real authentication is the PSK or 802.1X outcome proved by the 4-way handshake; authentication and association are two state transitions, not two levels of security. *Correct statement:* authentication opens State 2 and association opens State 3; keys come afterwards.
:::

::: lens
[QUALCOMM · CISCO · JUNIPER]{.co}

"How does a station associate with an AP?" and "walk through a WPA2-Personal connection frame by frame" recur in Qualcomm Hyderabad and Bengaluru reports and in Cisco and Juniper wireless rounds. A strong answer lists the phases in order, names the frames, says which state each frame reaches, and distinguishes the 802.11 exchange from the key exchange. Follow-ups: a missing EAPOL message 4 (wrong passphrase or a lost frame), and what a station does if association fails with status 17 (the AP is full).
:::

::: check
1. In which state may a station first send a data frame? [^c66-1]
2. Why can a sniffer see a DHCP exchange only sometimes? [^c66-2]
3. What does the AP assign during association? [^c66-3]
:::

[^c66-1]: State 3 (authenticated and associated); in a secured network, user data flows only after the controlled port opens.
[^c66-2]: The DHCP packets are encrypted; Wireshark decrypts them only if it has captured the 4-way handshake and knows the passphrase.
[^c66-3]: An association ID (AID) from 1 to 2007.

:::
