::: {.p6}

## [6.9]{.sec}Wi-Fi 6, 6E and Wi-Fi 7 [Must · ■■■]{.tag} {#s6-9}

Earlier generations raised the peak rate of one client. By 2015 the limit was no longer the peak but the crowd: an apartment block or a stadium has hundreds of devices, each sending small packets, and each packet pays the contention overhead of [§6.4](#s6-4){.ref}. IEEE 802.11ax turns Wi-Fi from "one talker at a time" into scheduled access in which the AP can orchestrate many stations in one transmission. 802.11be adds more bandwidth and the ability to use several links at once.

### OFDMA and resource units

In *OFDMA* the subcarriers of a channel are divided into *resource units* (RUs) of 26, 52, 106, 242, 484 or 996 tones (a tone is one subcarrier, data or pilot), and each RU is assigned to a different station within one transmission (Figure 6.12). Previously a station occupying the channel for 100 bytes wasted the other 99% of the subcarriers' capacity for that symbol; now several stations share them. The number of RUs by width is as follows.

<figure>
<svg viewBox="0 0 480 154" width="480"><text class="lbl" x="126" y="12" text-anchor="middle" >OFDM: one user per symbol</text><line class="lg" x1="26" y1="20" x2="26" y2="136" /><line class="lg" x1="26" y1="136" x2="236" y2="136" /><text class="sm" x="22" y="78" text-anchor="end" >freq</text><text class="sm" x="236" y="148" text-anchor="end" >time</text><rect class="box" x="30" y="24" width="48" height="108" style="fill:#F1F2F3"/><text class="sm" x="54" y="82" text-anchor="middle" >STA1</text><rect class="box" x="82" y="24" width="48" height="108" style="fill:#D9DCDF"/><text class="sm" x="106" y="82" text-anchor="middle" >STA2</text><rect class="box" x="134" y="24" width="48" height="108" style="fill:#BFC3C7"/><text class="sm" x="158" y="82" text-anchor="middle" >STA3</text><rect class="box" x="186" y="24" width="48" height="108" style="fill:#A6ABB0"/><text class="sm" x="210" y="82" text-anchor="middle" >STA4</text><text class="lbl" x="366" y="12" text-anchor="middle" >OFDMA: one PPDU, many users</text><line class="lg" x1="266" y1="20" x2="266" y2="136" /><line class="lg" x1="266" y1="136" x2="476" y2="136" /><text class="sm" x="262" y="78" text-anchor="end" >freq</text><text class="sm" x="476" y="148" text-anchor="end" >time</text><rect class="box" x="270" y="24" width="200" height="108" style="fill:#FFFFFF"/><rect class="box" x="270" y="24" width="200" height="40" style="fill:#F1F2F3"/><rect class="box" x="270" y="64" width="200" height="20" style="fill:#D9DCDF"/><rect class="box" x="270" y="84" width="200" height="20" style="fill:#BFC3C7"/><rect class="box" x="270" y="104" width="200" height="28" style="fill:#A6ABB0"/><text class="sm" x="370" y="49" text-anchor="middle" >STA1 (106 tones)</text><text class="sm" x="370" y="77" text-anchor="middle" >STA2 (52)</text><text class="sm" x="370" y="97" text-anchor="middle" >STA3 (52)</text><text class="sm" x="370" y="121" text-anchor="middle" >STA4 (106)</text><line class="lg" x1="236" y1="20" x2="236" y2="140" stroke-dasharray="2 3"/></svg>
<figcaption><b>Figure 6.12</b> Time-frequency grid: OFDM gives the whole channel to one station at a time; OFDMA splits it into resource units shared within a single transmission.</figcaption>
</figure>

| Channel | 26-tone | 52-tone | 106-tone | 242-tone | 484-tone | 996-tone |
|---|---|---|---|---|---|---|
| 20 MHz | 9 | 4 | 2 | 1 | | |
| 40 MHz | 18 | 8 | 4 | 2 | 1 | |
| 80 MHz | 37 | 16 | 8 | 4 | 2 | 1 |
| 160 MHz | 74 | 32 | 16 | 8 | 4 | 2 |

The AP decides the allocation. For the downlink it sends one PPDU with the allocation in its preamble. For the uplink, which needs the stations to start together and to end together, it first sends a *trigger frame* that lists, for each station, the RU, the MCS, the power target and the length. After a SIFS the stations send their *HE trigger-based PPDUs* simultaneously, padded to equal duration, and the AP answers with one *multi-station Block Ack*. A station without an assignment may use *uplink OFDMA random access* (UORA), a backoff over RUs reserved for contention.

<figure>
<svg viewBox="0 0 480 150" width="480"><defs><marker id="i10" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="a10" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><text class="lbl" x="90" y="12" text-anchor="middle" >AP</text><line class="lg" x1="90" y1="18" x2="90" y2="140" /><text class="lbl" x="190" y="12" text-anchor="middle" >STA1</text><line class="lg" x1="190" y1="18" x2="190" y2="140" /><text class="lbl" x="290" y="12" text-anchor="middle" >STA2</text><line class="lg" x1="290" y1="18" x2="290" y2="140" /><text class="lbl" x="390" y="12" text-anchor="middle" >STA3</text><line class="lg" x1="390" y1="18" x2="390" y2="140" /><line class="acc" x1="90" y1="30" x2="188" y2="36" marker-end="url(#a10)"/><line class="acc" x1="90" y1="30" x2="288" y2="36" marker-end="url(#a10)"/><line class="acc" x1="90" y1="30" x2="388" y2="36" marker-end="url(#a10)"/><text class="acct" x="40" y="28" text-anchor="middle" >Trigger</text><text class="sm" x="240" y="24" text-anchor="middle" >RU, MCS, power, length per station</text><rect class="hl" x="150" y="62" width="80" height="14" stroke="#1A1D23" stroke-width=".9"/><text class="sm" x="190" y="72" text-anchor="middle" >RU 1</text><rect class="hl" x="250" y="62" width="80" height="14" stroke="#1A1D23" stroke-width=".9"/><text class="sm" x="290" y="72" text-anchor="middle" >RU 2</text><rect class="hl" x="350" y="62" width="80" height="14" stroke="#1A1D23" stroke-width=".9"/><text class="sm" x="390" y="72" text-anchor="middle" >RU 3</text><text class="sm" x="290" y="90" text-anchor="middle" >HE trigger-based PPDUs, sent together after SIFS</text><text class="sm" x="240" y="112" text-anchor="middle" >Multi-STA Block Ack from the AP after SIFS</text><line class="ln" x1="92" y1="118" x2="186" y2="124" marker-end="url(#i10)"/><line class="ln" x1="92" y1="118" x2="286" y2="124" marker-end="url(#i10)"/><line class="ln" x1="92" y1="118" x2="386" y2="124" marker-end="url(#i10)"/></svg>
<figcaption><b>Figure 6.13</b> Uplink OFDMA: the AP schedules, the stations answer in parallel on their own resource units, and one acknowledgement closes the exchange.</figcaption>
</figure>

::: example
**Nine sensors in one 20 MHz channel.** Nine IoT sensors each have 100 bytes to send. Compare nine separate accesses with one trigger-based OFDMA exchange, with the 5 GHz timings of [§6.4](#s6-4){.ref} (DIFS 34 µs, average backoff 67.5 µs, SIFS 16 µs) and these assumptions: a single-user transmission uses a 44 µs preamble and MCS 7, one data symbol (13.6 µs); the ACK takes 32 µs; the trigger frame takes 70 µs; each sensor uses a 26-tone RU (24 data tones) at MCS 5 (64-QAM, 2/3), whose rate is 24 × 6 × 2/3 ÷ 13.6 µs ≈ 7 Mb/s; and the multi-station Block Ack takes 60 µs.

1. Separate accesses: 34 + 67.5 + 44 + 13.6 + 16 + 32 ≈ 207 µs each, so nine take about 1.86 ms, ignoring the collisions that nine contenders would cause.
2. OFDMA: one contention (34 + 67.5), the trigger (70), SIFS (16), the uplink PPDU with 56 µs of preamble and (816 + 22 bits) ÷ 96 bits per symbol = 9 symbols = 122 µs of data, SIFS (16) and the Block Ack (60): about 0.44 ms.

[Result: about four times less airtime for the same nine packets, plus no collisions among the nine. The gain is airtime and latency for many small flows; the single-client peak rate does not change.]{.result}
:::

### MU-MIMO, 1024-QAM, BSS colouring and TWT

802.11ac had downlink MU-MIMO only. 802.11ax adds *uplink* MU-MIMO, in which several stations transmit on the same RU and the AP separates them with its antennas, and allows MU-MIMO inside RUs of 106 tones or more, so OFDMA and MU-MIMO can be combined. 1024-QAM (10 bits per symbol) gives 25% more than 256-QAM, but only at a SNR above about 35 dB.

*BSS colouring* addresses the exposed-node problem between neighbouring cells. Every HE frame carries a 6-bit *colour* of its BSS in the PHY header. A station that detects a frame with a different colour knows that it belongs to an overlapping BSS (OBSS). If the frame is weaker than the *OBSS packet-detect threshold* (the default is −82 dBm and it may be raised up to −62 dBm), the station may ignore that frame, regard the medium as idle and transmit, with its power reduced by as many decibels as the threshold was raised. This is *spatial reuse*. In an example, a frame from another BSS arrives at −78 dBm with a threshold of −72 dBm: the station continues its backoff as though the frame were absent. A frame of the same colour must be respected, which is why a colour collision with a neighbour disables the benefit. The standard keeps two NAVs, one for frames of the own BSS and one for others, so that ignoring a foreign reservation does not affect the own cell.

*Target wake time* (TWT), mentioned in [§6.8](#s6-8){.ref}, is a negotiated agreement: the station and AP exchange TWT elements that fix a first wake time, a wake interval (a mantissa multiplied by a power of two, in microseconds) and a minimum wake duration. Between its service periods the station can turn its radio off, which suits battery-powered sensors and phones. Because stations wake in separate service periods, contention is also lower. In *broadcast TWT* the AP announces schedules to groups of stations, so no individual negotiation is needed.

### Wi-Fi 6E and the 6 GHz band

*Wi-Fi 6E* is 802.11ax in the 6 GHz band (5,925 to 7,125 MHz in the United States), which adds 1,200 MHz of spectrum, almost twice as much as the 2.4 and 5 GHz bands together. The band holds 59 channels of 20 MHz, 29 of 40, 14 of 80 and 7 of 160 MHz, which make wide channels practical; Wi-Fi 7 gets 3 channels of 320 MHz (Figure 6.15). Since no legacy device uses the band, there are no 802.11a/b/g/n/ac clients, no beacons at old rates and no need for protection. Access requires WPA3 or OWE. Indoor low-power access points work without coordination; standard-power outdoor use depends on an automated frequency coordination database that protects incumbent microwave links. Regulators differ by country; India has opened its lower 6 GHz range for indoor low-power use, and the current rules should be checked at the time of reading.

### Wi-Fi 7 (802.11be)

802.11be, "Extremely High Throughput", combines four multipliers: 320 MHz channels (2× over 160 MHz), 4096-QAM (12 bits, 1.2× over 1024-QAM), 16 spatial streams in the standard (2× over 8) and *multi-link operation*, giving the peak rate of 46.1 Gb/s computed in [§6.2](#s6-2){.ref}. Two more features matter in dense networks. *Multi-RU* allows a station to be given several RUs at once, which avoids wasting capacity when the channel is partly occupied. *Preamble puncturing* lets an 80, 160 or 320 MHz transmission skip a 20 MHz subchannel that is busy or occupied by radar, so a single interferer no longer cuts the channel to the width of its clean part.

**Multi-link operation (MLO)** lets one device use several radios, for example on 5 and 6 GHz, as a single logical device. A *multi-link device* (MLD) has one MAC address that upper layers see and one affiliated station per link, each with its own link address; the stations share one sequence-number space and a Block Ack scoreboard, so frames of one flow may travel on any link. The result is higher throughput (the links add) and lower latency (a frame can use whichever link wins contention first). The mode depends on how well the radios isolate each other.

| Mode | Behaviour | Hardware cost | A firmware challenge |
|---|---|---|---|
| STR (simultaneous transmit and receive) | links work independently, one may send while another receives | filters and enough frequency separation; most demanding | in-device interference and independent EDCA and NAV state on each link |
| NSTR (non-simultaneous) | links are close, so transmitting on one blocks receiving on the other | lower | aligning the end of transmissions on both links, otherwise the sender's own signal deafens its other link |
| EMLSR (enhanced multi-link single radio) | one full radio listens on several links with minimal circuits, then switches to the link that receives an initial control frame | lowest; a single radio chain | the switching delay, which must be known to the AP, and the frames lost during it |

Another firmware task is the mapping of traffic identifiers to links (for example, voice on the less loaded link), and recovery when a link is lost.

| Feature | Wi-Fi 5 (ac) | Wi-Fi 6 (ax) | Wi-Fi 6E | Wi-Fi 7 (be) |
|---|---|---|---|---|
| Bands | 5 GHz | 2.4, 5 | adds 6 GHz | 2.4, 5, 6 |
| Widest channel | 160 MHz | 160 MHz | 160 MHz | 320 MHz |
| QAM | 256 | 1024 | 1024 | 4096 |
| OFDMA | no | yes | yes | yes, with multi-RU |
| MU-MIMO | DL | DL, UL | DL, UL | DL, UL |
| BSS colour, TWT | no | yes | yes | yes, plus restricted TWT |
| Multi-link, puncturing | no | no | no | yes |

::: trap
*Claim:* "OFDMA increases the peak speed", or "Wi-Fi 6E is a new standard." *Why it is wrong:* the peak rate of one client comes from width, QAM order and streams; OFDMA improves efficiency and latency when many clients have small amounts of data. 6E is a regulatory and band extension of 802.11ax, with no new PHY. *Correct statement:* OFDMA is about sharing, and 6E is ax in 6 GHz.
:::

::: lens
[QUALCOMM · BROADCOM · CISCO · JUNIPER]{.co}

Qualcomm WLAN postings list MU-MIMO, OFDMA, TWT and rate control, and the reported questions are "OFDM versus OFDMA", "what is a trigger frame", "what is BSS colouring", "list four Wi-Fi 7 features" and "explain MLO modes and a firmware challenge of each". Expect also "how would the firmware schedule RUs across 20 stations with mixed QoS?" (solved in the Problem Set). A strong answer says what is shared (frequency for OFDMA, space for MU-MIMO), draws the trigger sequence, and links each feature to its benefit: airtime, latency, power or throughput.
:::

::: check
1. How many 26-tone RUs fit in 80 MHz? [^c69-1]
2. What does a station do with a frame of another BSS received below the OBSS threshold? [^c69-2]
3. By what factors do 320 MHz, 4096-QAM and 16 streams raise the Wi-Fi 6 peak? [^c69-3]
:::

[^c69-1]: 37.
[^c69-2]: It ignores the frame for carrier sensing and may transmit, at reduced power (spatial reuse).
[^c69-3]: 2, 1.2 and 2, a total of 4.8 (9.6 to 46.1 Gb/s).

## [6.10]{.sec}Roaming and enterprise design [Should · ■■□]{.tag} {#s6-10}

A station that walks from one AP's coverage into another's must change its association without dropping the call. Three facts shape the problem. The *client* decides when and where to roam; the network can only advise, and many clients roam late, remaining attached to a distant AP while a closer one is available (the *sticky client* problem). Roaming consists of a scan, a re-authentication and a (re)association, and each step takes time. And a voice call tolerates a gap of about 50 ms, whereas a full 802.1X authentication takes several round trips to a RADIUS server.

Three amendments help, each aiming at one of these steps.

- **802.11k (radio resource measurement)** supplies information. The AP gives the client a *neighbour report*, a list of nearby APs with their channels, so the client scans only those channels instead of all of them, and can also request beacon reports and load measurements.
- **802.11v (wireless network management)** supplies a suggestion. The AP can send a *BSS transition management request* to a client, naming better candidate APs, or warning that it will disassociate soon; the client may decline.
- **802.11r (fast BSS transition, FT)** supplies speed. It adds a key level, so that the keys for the next AP can be prepared in advance. The first association derives a PMK-R0 from the master key and the mobility domain; each AP of the domain holds a PMK-R1 derived from it; when the client roams, it derives a fresh PTK for the new AP from the PMK-R1 with new nonces, in the reassociation exchange itself, without a new 802.1X authentication and without a separate 4-way handshake. FT can run *over the air* (two authentication frames, then reassociation) or *over the DS* (the messages are relayed through the old AP).

<figure>
<svg viewBox="0 0 480 120" width="480"><text class="sm" x="10" y="20" text-anchor="start" >Full 802.1X re-authentication</text><rect class="fill" x="14" y="24" width="190.0" height="14" /><text class="sm" x="210.0" y="35" text-anchor="start" >200 to 400 ms</text><text class="sm" x="10" y="50" text-anchor="start" >PMK caching (OKC, PMKID)</text><rect class="fill" x="14" y="54" width="57.0" height="14" /><text class="sm" x="77.0" y="65" text-anchor="start" >about 60 to 100 ms</text><text class="sm" x="10" y="80" text-anchor="start" >802.11r fast transition</text><rect class="hl" x="14" y="84" width="19.0" height="14" stroke="#1A1D23" stroke-width=".9"/><text class="sm" x="39.0" y="95" text-anchor="start" >about 20 ms</text><line class="acc" x1="61.5" y1="14" x2="61.5" y2="112" stroke-dasharray="3 2"/><text class="acct" x="65.5" y="112" text-anchor="start" >50 ms voice budget</text></svg>
<figcaption><b>Figure 6.14</b> Illustrative time to move between access points under three key-management schemes.</figcaption>
</figure>

::: example
**Why 802.11r meets the voice budget.** Full re-authentication needs about four RADIUS round trips at 20 ms each plus server processing, and a four-message handshake: roughly 200 to 400 ms, well beyond the 50 ms budget. With FT over the air, the exchange is two authentication frames and two reassociation frames, at 1 to 5 ms each including contention, that is about 20 ms. Key caching without 802.11r (PMKID or opportunistic key caching) skips the RADIUS exchange but not the handshake: about 60 to 100 ms.

[Result: only 802.11r reliably meets the voice budget. The figures are illustrative; the shape of the comparison is what an interview expects.]{.result}
:::

A network design must also decide *where* the clients roam. Practical rules follow from the earlier sections.

**Channel planning in 2.4 GHz.** The band has channels 1 to 13 (14 in Japan only), spaced 5 MHz apart but each about 20 MHz wide. Two channels do not overlap if they are at least 25 MHz apart, so only 1, 6 and 11 can be used together (Figure 6.15). Using channel 3 or 8 overlaps two others partially; the overlapped signal looks like noise rather than a decodable frame, so carrier sense reacts to it unreliably and frames are corrupted, whereas co-channel neighbours at least defer to one another and merely share the airtime. Hence the rule "1, 6, 11 or nothing".

<figure>
<svg viewBox="0 0 480 232" width="480"><text class="lbl" x="10" y="12" text-anchor="start" >2.4 GHz: 20 MHz channels 1 to 13 (5 MHz apart); 1, 6 and 11 do not overlap</text><line class="lg" x1="14" y1="74" x2="470" y2="74" /><path class="acc" d="M25.9,74 C52.9,22 112.9,22 139.9,74"/><text class="lbl" x="82.9" y="84" text-anchor="middle" >1</text><path class="lg" d="M52.1,74 C79.1,22 139.1,22 166.1,74"/><text class="sm" x="109.1" y="84" text-anchor="middle" >2</text><path class="lg" d="M78.3,74 C105.3,22 165.3,22 192.3,74"/><text class="sm" x="135.3" y="84" text-anchor="middle" >3</text><path class="lg" d="M104.5,74 C131.5,22 191.5,22 218.5,74"/><text class="sm" x="161.5" y="84" text-anchor="middle" >4</text><path class="lg" d="M130.7,74 C157.7,22 217.7,22 244.7,74"/><text class="sm" x="187.7" y="84" text-anchor="middle" >5</text><path class="acc" d="M156.9,74 C183.9,22 243.9,22 270.9,74"/><text class="lbl" x="213.9" y="84" text-anchor="middle" >6</text><path class="lg" d="M183.1,74 C210.1,22 270.1,22 297.1,74"/><text class="sm" x="240.1" y="84" text-anchor="middle" >7</text><path class="lg" d="M209.3,74 C236.3,22 296.3,22 323.3,74"/><text class="sm" x="266.3" y="84" text-anchor="middle" >8</text><path class="lg" d="M235.5,74 C262.5,22 322.5,22 349.5,74"/><text class="sm" x="292.5" y="84" text-anchor="middle" >9</text><path class="lg" d="M261.7,74 C288.7,22 348.7,22 375.7,74"/><text class="sm" x="318.7" y="84" text-anchor="middle" >10</text><path class="acc" d="M287.9,74 C314.9,22 374.9,22 401.9,74"/><text class="lbl" x="344.9" y="84" text-anchor="middle" >11</text><path class="lg" d="M314.1,74 C341.1,22 401.1,22 428.1,74"/><text class="sm" x="371.1" y="84" text-anchor="middle" >12</text><path class="lg" d="M340.3,74 C367.3,22 427.3,22 454.3,74"/><text class="sm" x="397.3" y="84" text-anchor="middle" >13</text><text class="lbl" x="10" y="108" text-anchor="start" >5 GHz: 20 MHz channels; hatched groups need DFS (radar detection)</text><defs><pattern id="hat7" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="4" stroke="#9AA0A6" stroke-width="1"/></pattern></defs><rect class="box" x="14" y="116" width="68.0" height="20" /><text class="sm" x="48.0" y="130" text-anchor="middle" >36-48</text><text class="sm" x="48.0" y="148" text-anchor="middle" >UNII-1</text><rect class="box" x="86.0" y="116" width="68.0" height="20" style="fill:url(#hat7)"/><text class="sm" x="120.0" y="130" text-anchor="middle" style="fill:#1A1D23">52-64</text><text class="sm" x="120.0" y="148" text-anchor="middle" >UNII-2A</text><rect class="box" x="158.0" y="116" width="208.0" height="20" style="fill:url(#hat7)"/><text class="sm" x="262.0" y="130" text-anchor="middle" style="fill:#1A1D23">100-144</text><text class="sm" x="262.0" y="148" text-anchor="middle" >UNII-2C</text><rect class="box" x="370.0" y="116" width="85.5" height="20" /><text class="sm" x="412.75" y="130" text-anchor="middle" >149-165</text><text class="sm" x="412.75" y="148" text-anchor="middle" >UNII-3</text><text class="lbl" x="10" y="172" text-anchor="start" >6 GHz: 5925 to 7125 MHz, 59 channels of 20 MHz</text><rect class="fill" x="14.0" y="180" width="6.8" height="14" /><rect class="fill" x="21.4" y="180" width="6.8" height="14" /><rect class="fill" x="28.8" y="180" width="6.8" height="14" /><rect class="fill" x="36.2" y="180" width="6.8" height="14" /><rect class="fill" x="43.6" y="180" width="6.8" height="14" /><rect class="fill" x="51.0" y="180" width="6.8" height="14" /><rect class="fill" x="58.4" y="180" width="6.8" height="14" /><rect class="fill" x="65.8" y="180" width="6.8" height="14" /><rect class="fill" x="73.2" y="180" width="6.8" height="14" /><rect class="fill" x="80.6" y="180" width="6.8" height="14" /><rect class="fill" x="88.0" y="180" width="6.8" height="14" /><rect class="fill" x="95.4" y="180" width="6.8" height="14" /><rect class="fill" x="102.8" y="180" width="6.8" height="14" /><rect class="fill" x="110.2" y="180" width="6.8" height="14" /><rect class="fill" x="117.6" y="180" width="6.8" height="14" /><rect class="fill" x="125.0" y="180" width="6.8" height="14" /><rect class="fill" x="132.4" y="180" width="6.8" height="14" /><rect class="fill" x="139.8" y="180" width="6.8" height="14" /><rect class="fill" x="147.2" y="180" width="6.8" height="14" /><rect class="fill" x="154.6" y="180" width="6.8" height="14" /><rect class="fill" x="162.0" y="180" width="6.8" height="14" /><rect class="fill" x="169.4" y="180" width="6.8" height="14" /><rect class="fill" x="176.8" y="180" width="6.8" height="14" /><rect class="fill" x="184.2" y="180" width="6.8" height="14" /><rect class="fill" x="191.6" y="180" width="6.8" height="14" /><rect class="fill" x="199.0" y="180" width="6.8" height="14" /><rect class="fill" x="206.4" y="180" width="6.8" height="14" /><rect class="fill" x="213.8" y="180" width="6.8" height="14" /><rect class="fill" x="221.2" y="180" width="6.8" height="14" /><rect class="fill" x="228.6" y="180" width="6.8" height="14" /><rect class="fill" x="236.0" y="180" width="6.8" height="14" /><rect class="fill" x="243.4" y="180" width="6.8" height="14" /><rect class="fill" x="250.8" y="180" width="6.8" height="14" /><rect class="fill" x="258.2" y="180" width="6.8" height="14" /><rect class="fill" x="265.6" y="180" width="6.8" height="14" /><rect class="fill" x="273.0" y="180" width="6.8" height="14" /><rect class="fill" x="280.4" y="180" width="6.8" height="14" /><rect class="fill" x="287.8" y="180" width="6.8" height="14" /><rect class="fill" x="295.2" y="180" width="6.8" height="14" /><rect class="fill" x="302.6" y="180" width="6.8" height="14" /><rect class="fill" x="310.0" y="180" width="6.8" height="14" /><rect class="fill" x="317.4" y="180" width="6.8" height="14" /><rect class="fill" x="324.8" y="180" width="6.8" height="14" /><rect class="fill" x="332.2" y="180" width="6.8" height="14" /><rect class="fill" x="339.6" y="180" width="6.8" height="14" /><rect class="fill" x="347.0" y="180" width="6.8" height="14" /><rect class="fill" x="354.4" y="180" width="6.8" height="14" /><rect class="fill" x="361.8" y="180" width="6.8" height="14" /><rect class="fill" x="369.2" y="180" width="6.8" height="14" /><rect class="fill" x="376.6" y="180" width="6.8" height="14" /><rect class="fill" x="384.0" y="180" width="6.8" height="14" /><rect class="fill" x="391.4" y="180" width="6.8" height="14" /><rect class="fill" x="398.8" y="180" width="6.8" height="14" /><rect class="fill" x="406.2" y="180" width="6.8" height="14" /><rect class="fill" x="413.6" y="180" width="6.8" height="14" /><rect class="fill" x="421.0" y="180" width="6.8" height="14" /><rect class="fill" x="428.4" y="180" width="6.8" height="14" /><rect class="fill" x="435.8" y="180" width="6.8" height="14" /><rect class="fill" x="443.2" y="180" width="6.8" height="14" /><rect class="box" x="14.0" y="200" width="58.2" height="10" /><rect class="box" x="73.2" y="200" width="58.2" height="10" /><rect class="box" x="132.4" y="200" width="58.2" height="10" /><rect class="box" x="191.6" y="200" width="58.2" height="10" /><rect class="box" x="250.8" y="200" width="58.2" height="10" /><rect class="box" x="310.0" y="200" width="58.2" height="10" /><rect class="box" x="369.2" y="200" width="58.2" height="10" /><text class="sm" x="221.20000000000002" y="220" text-anchor="middle" >7 non-overlapping 160 MHz channels (3 of 320 MHz in Wi-Fi 7)</text></svg>
<figcaption><b>Figure 6.15</b> Channel maps for the three Wi-Fi bands (US-style numbering; regulatory limits differ by country).</figcaption>
</figure>

**Channel planning in 5 and 6 GHz.** There are about 25 channels of 20 MHz in 5 GHz, of which those in the UNII-2A and 2C ranges require *dynamic frequency selection* (DFS): the AP listens for radar for about a minute before using the channel, and must leave within seconds if it detects any, avoiding it for 30 minutes. With 80 MHz channels only five or six exist, which in a dense deployment forces neighbouring APs onto the same channel. A good design uses 20 or 40 MHz channels, a reuse pattern that places the same channel at least two cells apart in every direction, including the floors above and below, and spreads transmit power so that cells overlap by about 15 to 20% for roaming.

**Cell size and data rates.** An AP can transmit at 20 dBm but a phone only at about 14 dBm, so if the AP's power is not lowered the client hears the AP but cannot answer. Setting the AP power close to the client's, and disabling the lowest data rates (1, 2, 5.5 and 11 Mb/s), makes the beacons shorter, removes slow clients that hold the channel for ages, and shrinks the cell so that the client roams sooner. Typical targets are a signal of −67 dBm or better and an SNR of 25 dB for voice and video.

**Controllers.** In the *split-MAC* design a *lightweight AP* handles the radio and real-time frames, and a *wireless LAN controller* (WLC) handles management, policy and roaming state. The tunnel between them is CAPWAP (UDP ports 5246 for control and 5247 for data). The controller runs *radio resource management*, which selects channels and powers automatically, detects rogue APs, and keeps the keys that make fast roaming possible. In *local switching* (FlexConnect) the AP puts client traffic directly on the local VLAN so a WAN failure does not stop a branch. Cloud-managed systems (Meraki, Mist) move the controller into a cloud service and keep the data plane local.

::: example
**Channel plan for a three-floor hostel.** Each floor has four APs along the corridor, P1 to P4. Use the eight non-DFS 20 MHz channels of 5 GHz (36, 40, 44, 48, 149, 153, 157, 161), keeping four in reserve.

| Floor | P1 | P2 | P3 | P4 |
|---|---|---|---|---|
| 3 | 149 | 157 | 36 | 44 |
| 2 | 44 | 36 | 157 | 149 |
| 1 | 36 | 44 | 149 | 157 |

1. Along every floor the four neighbours use four different channels.
2. Directly above or below, no cell repeats the channel of the cell next to it (compare floors 1 and 2, then 2 and 3, position by position).
3. Keep power at 14 to 17 dBm and the lowest rate at 12 Mb/s, so the floor slabs and walls finish the job of isolating the reuse.

[Result: no two adjacent cells, horizontal or vertical, share a channel. With 80 MHz channels the same building has only two non-DFS channels (36 to 48 and 149 to 161), and the plan is impossible.]{.result}
:::

::: lens
[CISCO · JUNIPER · QUALCOMM]{.co}

Roaming and design questions come from the enterprise vendors, in the form "how does 802.11r speed up roaming and what do k and v add" and "users complain voice calls drop while walking down a corridor; how do you troubleshoot?". A strong answer separates the client's decision from the network's help, and for the second question works through the layers: signal and SNR at the roam point, AP power versus client power, channel overlap, DFS events, sticky clients, 802.11r compatibility and RADIUS delay. Troubleshooting method in general is the subject of [Pillar 11](#ch11){.ref}.
:::

::: check
1. Which amendment supplies a neighbour list? [^c610-1]
2. Why must 2.4 GHz plans use 1, 6 and 11? [^c610-2]
3. What does DFS require an AP to do? [^c610-3]
:::

[^c610-1]: 802.11k (the neighbour report).
[^c610-2]: They are the only three 20 MHz channels at least 25 MHz apart, so they do not overlap.
[^c610-3]: Listen for radar before using a channel, and vacate it, for 30 minutes, if radar is detected.

:::
