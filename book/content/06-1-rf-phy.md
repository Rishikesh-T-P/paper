::: {.chapter .p6}
::: opener
[Part I · Pillar 6]{.part-label}

[6]{.num}

# Wireless and Cellular Networks {#ch6}

[A radio link is a wire with noise, a shared medium and a rulebook; we learn the rulebook frame by frame.]{.promise}

1. [6.1 RF in one sitting]{} [MUST]{}
2. [6.2 PHY essentials: OFDM, QAM and MIMO]{} [MUST]{}
3. [6.3 802.11 architecture and the family tree]{} [MUST]{}
4. [6.4 The MAC: CSMA/CA and DCF timing]{} [MUST]{}
5. [6.5 The 802.11 frame, bit by bit]{} [MUST]{}
6. [6.6 The connection lifecycle]{} [MUST]{}
7. [6.7 Security: WPA2, WPA3 and PMF]{} [MUST]{}
8. [6.8 QoS, aggregation and power save]{} [SHOULD]{}
9. [6.9 Wi-Fi 6, 6E and Wi-Fi 7]{} [MUST]{}
10. [6.10 Roaming and enterprise design]{} [SHOULD]{}
11. [6.11 The Linux and firmware view]{} [SHOULD]{}
12. [6.12 Cellular from LTE to 5G]{} [SHOULD]{}
:::

Wireless engineering is asked in three registers: arithmetic (decibels, timing, data rates), protocol (frames, handshakes, state machines) and system (firmware, scheduling, cellular cores). The sections follow that order. The Must path is about 4.5 days; the Qualcomm and Broadcom WLAN roles expect the whole chapter, and the Nokia and Qualcomm modem roles add §6.12. Ethernet and CSMA/CD are taught in [§3.3](#s3-3){.ref}, the generic 802.1X and EAP exchange in [§9.12](#s9-12){.ref}, and the Linux capture tools in [§8.7](#s8-7){.ref}; this chapter adds only what is specific to the air.

## [6.1]{.sec}RF in one sitting [Must · ■□□]{.tag} {#s6-1}

A radio link is governed by three quantities: how much power leaves the transmitter, how much of it survives the journey, and how much noise the receiver must compete with. Engineers compare these on a logarithmic scale because the numbers span many orders of magnitude: a transmitter radiates 100 milliwatts, while a receiver can still decode a signal of a hundred-billionth of a milliwatt.

### Decibels and dBm

The *decibel* (dB) expresses a ratio of two powers as ten times the base-10 logarithm of that ratio. It is relative: it says "twice as much", never "so many watts". Because logarithms turn multiplication into addition, a chain of gains and losses is simply summed. The *dBm* is the same scale with a fixed reference of one milliwatt, and so it is an absolute power. Antenna gain is quoted in *dBi*, relative to an ideal isotropic radiator that sends equally in all directions.

| Change in dB | Power ratio | Remember as |
|---|---|---|
| 0 | ×1 | unchanged |
| +3 | ×2 | double (exactly 1.995) |
| +6 | ×4 | double twice |
| +10 | ×10 | one decade |
| +20 | ×100 | two decades |
| +30 | ×1000 | three decades |
| −3 | ×½ | half |
| −10 | ×0.1 | one tenth |

To convert, use P(dBm) = 10 log₁₀(P in mW). Thus 1 mW is 0 dBm, 100 mW is 20 dBm, 1 W is 30 dBm, and 200 mW is 100 mW doubled, that is 20 + 3 = 23 dBm. A mixed number such as 40 mW is found by splitting it into factors of 10 and 2: 40 = 10 × 2 × 2, so 0 + 10 + 3 + 3 = 16 dBm.

::: trap
*Claim:* "+3 dB means three times the power." *Why it is wrong:* the decibel is logarithmic; +3 dB is a factor of two and +10 dB a factor of ten. A related slip is to add dBm values: two 20 dBm sources do not make 40 dBm. *Correct statement:* ratios in dB add, absolute levels in dBm combine as powers, so two equal sources give +3 dB (here 23 dBm), and a dBm value plus a dB gain gives a dBm value.
:::

### Path loss and the link budget

A signal spreads as it travels, and its power density falls with the square of the distance. For a free-space path, the *free-space path loss* (FSPL) between isotropic antennas is

FSPL (dB) = 20 log₁₀(d) + 20 log₁₀(f) − 147.55, with d in metres and f in hertz.

Two consequences follow. Doubling the distance adds 6 dB, and doubling the frequency also adds 6 dB; hence a 5 GHz signal is about 7 dB weaker than a 2.4 GHz signal at the same distance, which is one reason 5 GHz cells are smaller. Real buildings are worse than free space: walls, floors and people add loss, and indoors the loss grows as 10·n·log₁₀(d) with an exponent n between 3 and 4 rather than 2.

The *link budget* is the bookkeeping of this journey. We start from the transmit power, add every gain, subtract every loss, and compare the received level with what the receiver needs.

::: example
**Link budget of a 5 GHz link.** An AP transmits 20 dBm (100 mW) through a 3 dBi antenna to a laptop 30 m away, with one internal wall of 12 dB and a 3 dBi receive antenna; the channel is 20 MHz wide and the receiver noise floor is −92 dBm.

1. FSPL at 5.5 GHz over 30 m: 20 log₁₀(30) = 29.5, 20 log₁₀(5.5×10⁹) = 194.8, so 29.5 + 194.8 − 147.55 = 76.8 dB.
2. Received power = 20 + 3 − 76.8 − 12 + 3 = −62.8 dBm (Figure 6.1).
3. SNR = −62.8 − (−92) = 29.2 dB.
4. Shannon's bound C = B log₂(1 + SNR) with SNR = 10^2.92 ≈ 832 gives 20 MHz × log₂(833) ≈ 20 × 9.7 = 194 Mb/s for one spatial stream.
5. Compare with the minimum receiver sensitivities of 802.11ax at 20 MHz: MCS 7 (64-QAM 5/6) needs −64 dBm, MCS 8 (256-QAM 3/4) needs −59 dBm, MCS 11 (1024-QAM 5/6) needs −52 dBm. A level of −62.8 dBm therefore guarantees MCS 7, about 86 Mb/s; a good receiver at 29 dB SNR may manage MCS 8, about 103 Mb/s, roughly half of Shannon's bound.

[Result: −62.8 dBm received, 29 dB SNR, MCS 7 to 8. To reach 1024-QAM one needs roughly 35 dB SNR, which means being closer or in the same room.]{.result}
:::

<figure>
<svg viewBox="0 0 480 176" width="480"><line class="lg" x1="30" y1="14" x2="30" y2="156" /><line class="lg" x1="30" y1="156" x2="470" y2="156" /><line class="lg" x1="27" y1="25.5" x2="30" y2="25.5" /><text class="sm" x="24" y="28.0" text-anchor="end" >20</text><line class="lg" x1="27" y1="47.5" x2="30" y2="47.5" /><text class="sm" x="24" y="50.0" text-anchor="end" >0</text><line class="lg" x1="27" y1="69.5" x2="30" y2="69.5" /><text class="sm" x="24" y="72.0" text-anchor="end" >-20</text><line class="lg" x1="27" y1="91.5" x2="30" y2="91.5" /><text class="sm" x="24" y="94.0" text-anchor="end" >-40</text><line class="lg" x1="27" y1="113.5" x2="30" y2="113.5" /><text class="sm" x="24" y="116.0" text-anchor="end" >-60</text><line class="lg" x1="27" y1="135.5" x2="30" y2="135.5" /><text class="sm" x="24" y="138.0" text-anchor="end" >-80</text><text class="sm" x="30" y="10" text-anchor="middle" >dBm</text><rect class="fill" x="50" y="25.5" width="44" height="130.5" /><text class="lbl" x="72" y="21.5" text-anchor="middle" >+20 dBm</text><text class="sm" x="72" y="168" text-anchor="middle" >Tx power</text><rect class="box" x="120" y="22.2" width="44" height="3.3000000000000007" /><text class="lbl" x="142" y="18.2" text-anchor="middle" >+3 dB</text><text class="sm" x="142" y="168" text-anchor="middle" >Tx antenna</text><rect class="box" x="190" y="22.2" width="44" height="84.5" style="fill:#FFF4C2"/><text class="lbl" x="212" y="116.7" text-anchor="middle" >-76.8 dB</text><text class="sm" x="212" y="168" text-anchor="middle" >Path loss</text><rect class="box" x="260" y="106.7" width="44" height="13.200000000000003" /><text class="lbl" x="282" y="102.7" text-anchor="middle" >-12 dB</text><text class="sm" x="282" y="168" text-anchor="middle" >Wall</text><rect class="box" x="330" y="116.6" width="44" height="3.3000000000000114" /><text class="lbl" x="352" y="112.6" text-anchor="middle" >+3 dB</text><text class="sm" x="352" y="168" text-anchor="middle" >Rx antenna</text><rect class="fill" x="400" y="116.6" width="44" height="39.400000000000006" /><text class="lbl" x="422" y="112.6" text-anchor="middle" >-62.8 dBm</text><text class="sm" x="422" y="168" text-anchor="middle" >Received</text><line class="acc" x1="30" y1="148.7" x2="470" y2="148.7" stroke-dasharray="4 3"/><text class="sm" x="468" y="145.7" text-anchor="end" >noise floor -92 dBm</text><line class="ln" x1="446" y1="116.6" x2="446" y2="148.7" /><text class="lbl" x="440" y="135.64999999999998" text-anchor="end" >SNR 29 dB</text></svg>
<figcaption><b>Figure 6.1</b> Link budget of the worked example: gains raise the level, losses lower it, and the SNR is the gap between the received level and the noise floor.</figcaption>
</figure>

The noise floor itself has a cause. Thermal noise power is −174 dBm per hertz plus 10 log₁₀(B); for a 20 MHz channel that is −174 + 73 = −101 dBm, and a receiver's electronics add a *noise figure* of several decibels, which is why −92 dBm is a realistic floor. Doubling the channel width doubles the noise power, so an 80 MHz channel has a floor 6 dB higher than a 20 MHz one. This is the first of many trade-offs between speed and robustness.

### Shannon and SNR

*Shannon's capacity theorem* states that the error-free rate of a channel with bandwidth B hertz and signal-to-noise ratio SNR (as a plain ratio, not in dB) cannot exceed B log₂(1 + SNR). Two readings matter. At high SNR each additional 3 dB of SNR adds about one bit per hertz, because log₂ gains 1 when SNR doubles; at low SNR capacity is nearly linear in power. Capacity is linear in bandwidth. Thus wider channels and cleaner signals both help, but bandwidth pays more, which is why every Wi-Fi generation widened the channel while only slowly raising the QAM order.

Wi-Fi turns this into a table. The transmitter chooses a *modulation and coding scheme* (MCS) from the measured SNR: a low SNR demands a sparse constellation and heavy error coding, a high SNR allows a dense one. The choice of MCS for each frame is called *rate adaptation* and is taught in [§6.11](#s6-11){.ref}.

::: lens
[QUALCOMM · NOKIA · BROADCOM]{.co}

"Convert 200 mW to dBm" and "what does −3 dB mean" are warm-up questions in WLAN and modem screens, usually followed by a link-budget calculation such as the one above. A strong answer states the formula, writes the chain of additions on the board, and finishes by relating SNR to a modulation order. Follow-ups: why 5 GHz cells are smaller than 2.4 GHz cells, and what a 3 dB change in transmit power does to range (about 41% more distance in free space, since the loss grows with the square).
:::

::: check
1. Convert 25 mW to dBm. [^c61-1]
2. A receiver has a −90 dBm noise floor and gets −61 dBm. What is the SNR? [^c61-2]
3. By how much does FSPL change when the distance triples? [^c61-3]
:::

[^c61-1]: 25 mW is 100 mW divided by four, so 20 − 6 = 14 dBm.
[^c61-2]: SNR = −61 − (−90) = 29 dB.
[^c61-3]: 20 log₁₀(3) = 9.5 dB more.

## [6.2]{.sec}PHY essentials: OFDM, QAM and MIMO [Must · ■■□]{.tag} {#s6-2}

The physical layer (PHY) turns bits into radio waves. Modern Wi-Fi, LTE and 5G share one idea at this layer: split the channel into many narrow subcarriers, put a few bits on each, and send them all at once. The reasoning is as follows. A single fast stream of symbols is short in time, and an echo of one symbol arrives while the next is being received; this *multipath* smears the symbols together. Many slow parallel streams have long symbols, and an echo of a few hundred nanoseconds is a small fraction of a long symbol.

### OFDM, subcarriers and the cyclic prefix

*Orthogonal frequency-division multiplexing* (OFDM) places subcarriers at a spacing of exactly 1/T hertz, where T is the useful symbol duration. The spectrum of each subcarrier has the shape sin(x)/x, which is zero at every multiple of 1/T from its centre. Hence at the centre of any one subcarrier all the others contribute exactly zero, and a receiver that integrates over one symbol period separates them perfectly. This is what *orthogonal* means, and it is the answer to the common interview question about how the subcarriers do not interfere (Figure 6.2).

<figure>
<svg viewBox="0 0 480 136" width="480"><defs><marker id="i1" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="a1" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><line class="lg" x1="20" y1="95" x2="280" y2="95" /><polyline class="ln" points="20,95.0 22,91.9 24,88.4 26,84.8 28,81.0 30,77.0 32,72.9 34,68.8 36,64.7 38,60.7 40,56.8 42,53.1 44,49.6 46,46.4 48,43.5 50,41.0 52,38.9 54,37.2 56,36.0 58,35.2 60,35.0 62,35.2 64,36.0 66,37.2 68,38.9 70,41.0 72,43.5 74,46.4 76,49.6 78,53.1 80,56.8 82,60.7 84,64.7 86,68.8 88,72.9 90,77.0 92,81.0 94,84.8 96,88.4 98,91.9 100,95.0 102,97.8 104,100.4 106,102.5 108,104.4 110,105.8 112,106.9 114,107.6 116,108.0 118,108.0 120,107.7 122,107.2 124,106.4 126,105.3 128,104.1 130,102.7 132,101.2 134,99.7 136,98.1 138,96.5 140,95.0 142,93.5 144,92.2 146,91.0 148,89.9 150,89.0 152,88.3 154,87.8 156,87.4 158,87.3 160,87.4 162,87.6 164,88.0 166,88.6 168,89.3 170,90.1 172,91.0 174,92.0 176,93.0 178,94.0 180,95.0 182,96.0 184,96.9 186,97.8 188,98.5 190,99.2 192,99.7 194,100.1 196,100.3 198,100.5 200,100.5 202,100.3 204,100.0 206,99.7 208,99.2 210,98.6 212,98.0 214,97.3 216,96.5 218,95.8 220,95.0 222,94.3 224,93.6 226,92.9 228,92.3 230,91.8 232,91.4 234,91.1 236,90.9 238,90.8 240,90.8 242,90.9 244,91.1 246,91.3 248,91.7 250,92.2 252,92.7 254,93.2 256,93.8 258,94.4 260,95.0 262,95.6 264,96.2 266,96.7 268,97.2 270,97.6 272,97.9 274,98.2 276,98.4 278,98.5 280,98.5"/><polyline class="ln" points="20,95.0 22,96.5 24,98.1 26,99.7 28,101.2 30,102.7 32,104.1 34,105.3 36,106.4 38,107.2 40,107.7 42,108.0 44,108.0 46,107.6 48,106.9 50,105.8 52,104.4 54,102.5 56,100.4 58,97.8 60,95.0 62,91.9 64,88.4 66,84.8 68,81.0 70,77.0 72,72.9 74,68.8 76,64.7 78,60.7 80,56.8 82,53.1 84,49.6 86,46.4 88,43.5 90,41.0 92,38.9 94,37.2 96,36.0 98,35.2 100,35.0 102,35.2 104,36.0 106,37.2 108,38.9 110,41.0 112,43.5 114,46.4 116,49.6 118,53.1 120,56.8 122,60.7 124,64.7 126,68.8 128,72.9 130,77.0 132,81.0 134,84.8 136,88.4 138,91.9 140,95.0 142,97.8 144,100.4 146,102.5 148,104.4 150,105.8 152,106.9 154,107.6 156,108.0 158,108.0 160,107.7 162,107.2 164,106.4 166,105.3 168,104.1 170,102.7 172,101.2 174,99.7 176,98.1 178,96.5 180,95.0 182,93.5 184,92.2 186,91.0 188,89.9 190,89.0 192,88.3 194,87.8 196,87.4 198,87.3 200,87.4 202,87.6 204,88.0 206,88.6 208,89.3 210,90.1 212,91.0 214,92.0 216,93.0 218,94.0 220,95.0 222,96.0 224,96.9 226,97.8 228,98.5 230,99.2 232,99.7 234,100.1 236,100.3 238,100.5 240,100.5 242,100.3 244,100.0 246,99.7 248,99.2 250,98.6 252,98.0 254,97.3 256,96.5 258,95.8 260,95.0 262,94.3 264,93.6 266,92.9 268,92.3 270,91.8 272,91.4 274,91.1 276,90.9 278,90.8 280,90.8"/><polyline class="acc" points="20,95.0 22,94.0 24,93.0 26,92.0 28,91.0 30,90.1 32,89.3 34,88.6 36,88.0 38,87.6 40,87.4 42,87.3 44,87.4 46,87.8 48,88.3 50,89.0 52,89.9 54,91.0 56,92.2 58,93.5 60,95.0 62,96.5 64,98.1 66,99.7 68,101.2 70,102.7 72,104.1 74,105.3 76,106.4 78,107.2 80,107.7 82,108.0 84,108.0 86,107.6 88,106.9 90,105.8 92,104.4 94,102.5 96,100.4 98,97.8 100,95.0 102,91.9 104,88.4 106,84.8 108,81.0 110,77.0 112,72.9 114,68.8 116,64.7 118,60.7 120,56.8 122,53.1 124,49.6 126,46.4 128,43.5 130,41.0 132,38.9 134,37.2 136,36.0 138,35.2 140,35.0 142,35.2 144,36.0 146,37.2 148,38.9 150,41.0 152,43.5 154,46.4 156,49.6 158,53.1 160,56.8 162,60.7 164,64.7 166,68.8 168,72.9 170,77.0 172,81.0 174,84.8 176,88.4 178,91.9 180,95.0 182,97.8 184,100.4 186,102.5 188,104.4 190,105.8 192,106.9 194,107.6 196,108.0 198,108.0 200,107.7 202,107.2 204,106.4 206,105.3 208,104.1 210,102.7 212,101.2 214,99.7 216,98.1 218,96.5 220,95.0 222,93.5 224,92.2 226,91.0 228,89.9 230,89.0 232,88.3 234,87.8 236,87.4 238,87.3 240,87.4 242,87.6 244,88.0 246,88.6 248,89.3 250,90.1 252,91.0 254,92.0 256,93.0 258,94.0 260,95.0 262,96.0 264,96.9 266,97.8 268,98.5 270,99.2 272,99.7 274,100.1 276,100.3 278,100.5 280,100.5"/><polyline class="ln" points="20,95.0 22,95.8 24,96.5 26,97.3 28,98.0 30,98.6 32,99.2 34,99.7 36,100.0 38,100.3 40,100.5 42,100.5 44,100.3 46,100.1 48,99.7 50,99.2 52,98.5 54,97.8 56,96.9 58,96.0 60,95.0 62,94.0 64,93.0 66,92.0 68,91.0 70,90.1 72,89.3 74,88.6 76,88.0 78,87.6 80,87.4 82,87.3 84,87.4 86,87.8 88,88.3 90,89.0 92,89.9 94,91.0 96,92.2 98,93.5 100,95.0 102,96.5 104,98.1 106,99.7 108,101.2 110,102.7 112,104.1 114,105.3 116,106.4 118,107.2 120,107.7 122,108.0 124,108.0 126,107.6 128,106.9 130,105.8 132,104.4 134,102.5 136,100.4 138,97.8 140,95.0 142,91.9 144,88.4 146,84.8 148,81.0 150,77.0 152,72.9 154,68.8 156,64.7 158,60.7 160,56.8 162,53.1 164,49.6 166,46.4 168,43.5 170,41.0 172,38.9 174,37.2 176,36.0 178,35.2 180,35.0 182,35.2 184,36.0 186,37.2 188,38.9 190,41.0 192,43.5 194,46.4 196,49.6 198,53.1 200,56.8 202,60.7 204,64.7 206,68.8 208,72.9 210,77.0 212,81.0 214,84.8 216,88.4 218,91.9 220,95.0 222,97.8 224,100.4 226,102.5 228,104.4 230,105.8 232,106.9 234,107.6 236,108.0 238,108.0 240,107.7 242,107.2 244,106.4 246,105.3 248,104.1 250,102.7 252,101.2 254,99.7 256,98.1 258,96.5 260,95.0 262,93.5 264,92.2 266,91.0 268,89.9 270,89.0 272,88.3 274,87.8 276,87.4 278,87.3 280,87.4"/><polyline class="ln" points="20,95.0 22,94.4 24,93.8 26,93.2 28,92.7 30,92.2 32,91.7 34,91.3 36,91.1 38,90.9 40,90.8 42,90.8 44,90.9 46,91.1 48,91.4 50,91.8 52,92.3 54,92.9 56,93.6 58,94.3 60,95.0 62,95.8 64,96.5 66,97.3 68,98.0 70,98.6 72,99.2 74,99.7 76,100.0 78,100.3 80,100.5 82,100.5 84,100.3 86,100.1 88,99.7 90,99.2 92,98.5 94,97.8 96,96.9 98,96.0 100,95.0 102,94.0 104,93.0 106,92.0 108,91.0 110,90.1 112,89.3 114,88.6 116,88.0 118,87.6 120,87.4 122,87.3 124,87.4 126,87.8 128,88.3 130,89.0 132,89.9 134,91.0 136,92.2 138,93.5 140,95.0 142,96.5 144,98.1 146,99.7 148,101.2 150,102.7 152,104.1 154,105.3 156,106.4 158,107.2 160,107.7 162,108.0 164,108.0 166,107.6 168,106.9 170,105.8 172,104.4 174,102.5 176,100.4 178,97.8 180,95.0 182,91.9 184,88.4 186,84.8 188,81.0 190,77.0 192,72.9 194,68.8 196,64.7 198,60.7 200,56.8 202,53.1 204,49.6 206,46.4 208,43.5 210,41.0 212,38.9 214,37.2 216,36.0 218,35.2 220,35.0 222,35.2 224,36.0 226,37.2 228,38.9 230,41.0 232,43.5 234,46.4 236,49.6 238,53.1 240,56.8 242,60.7 244,64.7 246,68.8 248,72.9 250,77.0 252,81.0 254,84.8 256,88.4 258,91.9 260,95.0 262,97.8 264,100.4 266,102.5 268,104.4 270,105.8 272,106.9 274,107.6 276,108.0 278,108.0 280,107.7"/><circle cx="60" cy="95" r="1.8" style="fill:#1A1D23"/><circle cx="100" cy="95" r="1.8" style="fill:#1A1D23"/><circle cx="140" cy="95" r="1.8" style="fill:#1A1D23"/><circle cx="180" cy="95" r="1.8" style="fill:#1A1D23"/><circle cx="220" cy="95" r="1.8" style="fill:#1A1D23"/><text class="sm" x="150" y="112" text-anchor="middle" >frequency</text><text class="sm" x="150" y="12" text-anchor="middle" >Subcarrier spectra: each peak sits on the zeros of the others</text><text class="sm" x="150" y="124" text-anchor="middle" >Spacing 1/T (78.125 kHz in 802.11ax)</text><text class="sm" x="380" y="12" text-anchor="middle" >Cyclic prefix</text><rect class="fill" x="310" y="30" width="130" height="22" /><rect class="hl" x="310" y="30" width="30" height="22" stroke="#1A1D23" stroke-width=".9"/><rect class="hl" x="440" y="30" width="30" height="22" stroke="#1A1D23" stroke-width=".9"/><text class="lbl" x="325" y="44" text-anchor="middle" >CP</text><text class="sm" x="455" y="44" text-anchor="middle" >tail</text><text class="lbl" x="375" y="44" text-anchor="middle" >useful symbol</text><line class="lg" x1="447" y1="52" x2="447" y2="58" /><path class="lg" d="M455,52 C455,66 325,66 325,52" fill="none" marker-end="url(#i1)"/><text class="sm" x="390" y="78" text-anchor="middle" >tail copied in front</text><rect class="fill" x="310" y="90" width="130" height="14" /><rect class="hl" x="323" y="90" width="30" height="14" stroke="#1A1D23" stroke-width=".9"/><text class="sm" x="375" y="101" text-anchor="middle" >delayed echo</text><line class="lg" x1="340" y1="84" x2="340" y2="90" /><text class="sm" x="390" y="122" text-anchor="middle" >Echo shorter than CP: no inter-symbol interference</text></svg>
<figcaption><b>Figure 6.2</b> Orthogonal subcarriers (left) and the cyclic prefix that absorbs multipath echoes (right).</figcaption>
</figure>

To keep the symbols apart in time, the transmitter copies the last part of each symbol to its front, the *cyclic prefix* (in 802.11, the *guard interval*, GI). An echo that arrives later than the direct path by less than the prefix falls inside the copy and does not corrupt the next symbol. Because the prefix is a cyclic copy, the received block still looks periodic, so orthogonality survives. The price is time: a 0.8 µs guard interval on a 12.8 µs symbol costs 6%.

The table below lists the numerology of the Wi-Fi generations. The 802.11a/g/n/ac OFDM symbol is 3.2 µs plus a 0.8 µs guard (0.4 µs in the short-GI option) on 312.5 kHz subcarriers, while 802.11ax made the symbol four times longer (12.8 µs, 78.125 kHz spacing) to tolerate outdoor echoes and to make resource units finer.

| Generation | Subcarrier spacing | Useful symbol | Guard intervals | Data subcarriers in 20 MHz |
|---|---|---|---|---|
| 802.11a/g | 312.5 kHz | 3.2 µs | 0.8 µs | 48 (plus 4 pilots) |
| 802.11n | 312.5 kHz | 3.2 µs | 0.8 or 0.4 µs | 52 |
| 802.11ac | 312.5 kHz | 3.2 µs | 0.8 or 0.4 µs | 52 |
| 802.11ax, be | 78.125 kHz | 12.8 µs | 0.8, 1.6 or 3.2 µs | 234 |

*Pilot* subcarriers carry known symbols; the receiver uses them to track phase and frequency drift.

### QAM and the modulation and coding scheme

*Quadrature amplitude modulation* (QAM) sends a symbol as a point on a two-dimensional grid, by varying the amplitude of two carriers 90° apart. A grid of M points carries log₂(M) bits per symbol: 4 points (QPSK) carry 2 bits, 16-QAM 4 bits, 64-QAM 6 bits, 256-QAM 8 bits, 1024-QAM 10 bits and 4096-QAM 12 bits (Figure 6.3). A denser grid packs more bits but brings the points closer, so the same noise makes more errors; this is why a high QAM order needs a high SNR. *Forward error correction* adds redundancy, and the *coding rate* (1/2, 2/3, 3/4 or 5/6) is the fraction of bits that are data. 802.11n and earlier use convolutional codes; LDPC codes, which are stronger at high rates, are optional in 802.11n/ac and mandatory in 802.11ax for resource units larger than 242 tones.

<figure>
<svg viewBox="0 0 480 158" width="480"><line class="lg" x1="12" y1="62" x2="108" y2="62" /><line class="lg" x1="60" y1="14" x2="60" y2="110" /><circle cx="36" cy="62" r="2.6" style="fill:#1A1D23"/><circle cx="84" cy="62" r="2.6" style="fill:#1A1D23"/><text class="lbl" x="60" y="124" text-anchor="middle" >BPSK</text><text class="sm" x="60" y="135" text-anchor="middle" >1 bit per symbol</text><line class="lg" x1="132" y1="62" x2="228" y2="62" /><line class="lg" x1="180" y1="14" x2="180" y2="110" /><circle cx="159.0" cy="83.0" r="2.4" style="fill:#1A1D23"/><circle cx="159.0" cy="41.0" r="2.4" style="fill:#1A1D23"/><circle cx="201.0" cy="83.0" r="2.4" style="fill:#1A1D23"/><circle cx="201.0" cy="41.0" r="2.4" style="fill:#1A1D23"/><text class="lbl" x="180" y="124" text-anchor="middle" >QPSK</text><text class="sm" x="180" y="135" text-anchor="middle" >2 bits per symbol</text><line class="lg" x1="252" y1="62" x2="348" y2="62" /><line class="lg" x1="300" y1="14" x2="300" y2="110" /><circle cx="268.5" cy="93.5" r="2.4" style="fill:#1A1D23"/><circle cx="268.5" cy="72.5" r="2.4" style="fill:#1A1D23"/><circle cx="268.5" cy="51.5" r="2.4" style="fill:#1A1D23"/><circle cx="268.5" cy="30.5" r="2.4" style="fill:#1A1D23"/><circle cx="289.5" cy="93.5" r="2.4" style="fill:#1A1D23"/><circle cx="289.5" cy="72.5" r="2.4" style="fill:#1A1D23"/><circle cx="289.5" cy="51.5" r="2.4" style="fill:#1A1D23"/><circle cx="289.5" cy="30.5" r="2.4" style="fill:#1A1D23"/><circle cx="310.5" cy="93.5" r="2.4" style="fill:#1A1D23"/><circle cx="310.5" cy="72.5" r="2.4" style="fill:#1A1D23"/><circle cx="310.5" cy="51.5" r="2.4" style="fill:#1A1D23"/><circle cx="310.5" cy="30.5" r="2.4" style="fill:#1A1D23"/><circle cx="331.5" cy="93.5" r="2.4" style="fill:#1A1D23"/><circle cx="331.5" cy="72.5" r="2.4" style="fill:#1A1D23"/><circle cx="331.5" cy="51.5" r="2.4" style="fill:#1A1D23"/><circle cx="331.5" cy="30.5" r="2.4" style="fill:#1A1D23"/><text class="lbl" x="300" y="124" text-anchor="middle" >16-QAM</text><text class="sm" x="300" y="135" text-anchor="middle" >4 bits per symbol</text><line class="lg" x1="372" y1="62" x2="468" y2="62" /><line class="lg" x1="420" y1="14" x2="420" y2="110" /><circle cx="383.2" cy="98.8" r="1.9" style="fill:#1A1D23"/><circle cx="383.2" cy="88.2" r="1.9" style="fill:#1A1D23"/><circle cx="383.2" cy="77.8" r="1.9" style="fill:#1A1D23"/><circle cx="383.2" cy="67.2" r="1.9" style="fill:#1A1D23"/><circle cx="383.2" cy="56.8" r="1.9" style="fill:#1A1D23"/><circle cx="383.2" cy="46.2" r="1.9" style="fill:#1A1D23"/><circle cx="383.2" cy="35.8" r="1.9" style="fill:#1A1D23"/><circle cx="383.2" cy="25.2" r="1.9" style="fill:#1A1D23"/><circle cx="393.8" cy="98.8" r="1.9" style="fill:#1A1D23"/><circle cx="393.8" cy="88.2" r="1.9" style="fill:#1A1D23"/><circle cx="393.8" cy="77.8" r="1.9" style="fill:#1A1D23"/><circle cx="393.8" cy="67.2" r="1.9" style="fill:#1A1D23"/><circle cx="393.8" cy="56.8" r="1.9" style="fill:#1A1D23"/><circle cx="393.8" cy="46.2" r="1.9" style="fill:#1A1D23"/><circle cx="393.8" cy="35.8" r="1.9" style="fill:#1A1D23"/><circle cx="393.8" cy="25.2" r="1.9" style="fill:#1A1D23"/><circle cx="404.2" cy="98.8" r="1.9" style="fill:#1A1D23"/><circle cx="404.2" cy="88.2" r="1.9" style="fill:#1A1D23"/><circle cx="404.2" cy="77.8" r="1.9" style="fill:#1A1D23"/><circle cx="404.2" cy="67.2" r="1.9" style="fill:#1A1D23"/><circle cx="404.2" cy="56.8" r="1.9" style="fill:#1A1D23"/><circle cx="404.2" cy="46.2" r="1.9" style="fill:#1A1D23"/><circle cx="404.2" cy="35.8" r="1.9" style="fill:#1A1D23"/><circle cx="404.2" cy="25.2" r="1.9" style="fill:#1A1D23"/><circle cx="414.8" cy="98.8" r="1.9" style="fill:#1A1D23"/><circle cx="414.8" cy="88.2" r="1.9" style="fill:#1A1D23"/><circle cx="414.8" cy="77.8" r="1.9" style="fill:#1A1D23"/><circle cx="414.8" cy="67.2" r="1.9" style="fill:#1A1D23"/><circle cx="414.8" cy="56.8" r="1.9" style="fill:#1A1D23"/><circle cx="414.8" cy="46.2" r="1.9" style="fill:#1A1D23"/><circle cx="414.8" cy="35.8" r="1.9" style="fill:#1A1D23"/><circle cx="414.8" cy="25.2" r="1.9" style="fill:#1A1D23"/><circle cx="425.2" cy="98.8" r="1.9" style="fill:#1A1D23"/><circle cx="425.2" cy="88.2" r="1.9" style="fill:#1A1D23"/><circle cx="425.2" cy="77.8" r="1.9" style="fill:#1A1D23"/><circle cx="425.2" cy="67.2" r="1.9" style="fill:#1A1D23"/><circle cx="425.2" cy="56.8" r="1.9" style="fill:#1A1D23"/><circle cx="425.2" cy="46.2" r="1.9" style="fill:#1A1D23"/><circle cx="425.2" cy="35.8" r="1.9" style="fill:#1A1D23"/><circle cx="425.2" cy="25.2" r="1.9" style="fill:#1A1D23"/><circle cx="435.8" cy="98.8" r="1.9" style="fill:#1A1D23"/><circle cx="435.8" cy="88.2" r="1.9" style="fill:#1A1D23"/><circle cx="435.8" cy="77.8" r="1.9" style="fill:#1A1D23"/><circle cx="435.8" cy="67.2" r="1.9" style="fill:#1A1D23"/><circle cx="435.8" cy="56.8" r="1.9" style="fill:#1A1D23"/><circle cx="435.8" cy="46.2" r="1.9" style="fill:#1A1D23"/><circle cx="435.8" cy="35.8" r="1.9" style="fill:#1A1D23"/><circle cx="435.8" cy="25.2" r="1.9" style="fill:#1A1D23"/><circle cx="446.2" cy="98.8" r="1.9" style="fill:#1A1D23"/><circle cx="446.2" cy="88.2" r="1.9" style="fill:#1A1D23"/><circle cx="446.2" cy="77.8" r="1.9" style="fill:#1A1D23"/><circle cx="446.2" cy="67.2" r="1.9" style="fill:#1A1D23"/><circle cx="446.2" cy="56.8" r="1.9" style="fill:#1A1D23"/><circle cx="446.2" cy="46.2" r="1.9" style="fill:#1A1D23"/><circle cx="446.2" cy="35.8" r="1.9" style="fill:#1A1D23"/><circle cx="446.2" cy="25.2" r="1.9" style="fill:#1A1D23"/><circle cx="456.8" cy="98.8" r="1.9" style="fill:#1A1D23"/><circle cx="456.8" cy="88.2" r="1.9" style="fill:#1A1D23"/><circle cx="456.8" cy="77.8" r="1.9" style="fill:#1A1D23"/><circle cx="456.8" cy="67.2" r="1.9" style="fill:#1A1D23"/><circle cx="456.8" cy="56.8" r="1.9" style="fill:#1A1D23"/><circle cx="456.8" cy="46.2" r="1.9" style="fill:#1A1D23"/><circle cx="456.8" cy="35.8" r="1.9" style="fill:#1A1D23"/><circle cx="456.8" cy="25.2" r="1.9" style="fill:#1A1D23"/><text class="lbl" x="420" y="124" text-anchor="middle" >64-QAM</text><text class="sm" x="420" y="135" text-anchor="middle" >6 bits per symbol</text><text class="sm" x="240" y="150" text-anchor="middle" >256-QAM: 8 bits   1024-QAM: 10 bits   4096-QAM: 12 bits (same layout, 16, 32 and 64 points per axis)</text></svg>
<figcaption><b>Figure 6.3</b> Constellations: each dot is one symbol, and a denser grid carries more bits but leaves less distance between neighbours.</figcaption>
</figure>

Each combination of modulation and coding rate is an MCS index. For a given width, the rate follows from one formula.

**Rate = (data subcarriers × bits per subcarrier × coding rate × spatial streams) ÷ (symbol + guard duration).**

::: example
**Data rate of an 802.11ax link.** An 80 MHz channel with one 996-tone resource unit has 980 data subcarriers (16 of the 996 are pilots). Use 1024-QAM (10 bits), coding rate 5/6, symbol 12.8 µs plus a 0.8 µs guard interval.

1. Bits per OFDM symbol per stream = 980 × 10 × 5/6 = 8,167.
2. Symbol time = 12.8 + 0.8 = 13.6 µs.
3. Rate per stream = 8,167 ÷ 13.6 µs = 600.5 Mb/s.
4. Two spatial streams give 1,201 Mb/s, the familiar "1.2 Gb/s" label; four streams on 160 MHz (1,960 subcarriers) give 4 × 1,201 = 4,804 Mb/s.
5. For Wi-Fi 7 take 320 MHz (3,920 data subcarriers) and 4096-QAM (12 bits): 3,920 × 12 × 5/6 ÷ 13.6 µs = 2,882 Mb/s per stream; sixteen streams, the standard's ceiling, give 46.1 Gb/s.

[Result: 600.5 Mb/s per stream at 80 MHz; 2,882 Mb/s per stream at 320 MHz with 4096-QAM. Marketing figures are these formulas at the best MCS and the shortest guard interval.]{.result}
:::

| MCS | Modulation | Coding | 20 MHz, 1 stream | 80 MHz, 1 stream | Typical SNR needed |
|---|---|---|---|---|---|
| 0 | BPSK | 1/2 | 8.6 Mb/s | 36.0 Mb/s | 5 dB |
| 2 | QPSK | 3/4 | 25.8 | 108.1 | 12 dB |
| 4 | 16-QAM | 3/4 | 51.6 | 216.2 | 18 dB |
| 7 | 64-QAM | 5/6 | 86.0 | 360.3 | 25 dB |
| 9 | 256-QAM | 5/6 | 114.7 | 480.4 | 31 dB |
| 11 | 1024-QAM | 5/6 | 143.4 | 600.5 | 35 dB |

The rates are for 802.11ax with the 0.8 µs guard interval; the SNR column is an engineering rule of thumb, not a standard value, because it depends on the receiver. Wi-Fi 7 adds MCS 12 and 13 (4096-QAM at 3/4 and 5/6).

### Spatial streams, MIMO and beamforming

With several antennas at each end a radio can exploit *multiple-input multiple-output* (MIMO) operation. If the transmitter has N_t antennas and the receiver N_r, the channel is a matrix **H** of N_r × N_t complex gains, one per antenna pair. In a scattering environment these paths differ, so the receiver can solve the linear equations y = **H**x and recover up to min(N_t, N_r) independent *spatial streams* sent at the same time on the same frequency. The rate scales with the number of streams, at the cost of needing high SNR on every stream. A "2×2:2" radio has two transmit and two receive antennas and two streams.

*Beamforming* uses the same antennas differently. The transmitter weights each antenna's phase so that the waves add constructively at the receiver, which raises the SNR by up to 10 log₁₀(N_t) dB (about 3 dB for two antennas, 6 dB for four). The transmitter learns the channel through *explicit sounding*: it sends a null data packet, and the receiver returns a compressed feedback matrix. In *single-user* MIMO (SU-MIMO) all streams go to one client; in *multi-user* MIMO (MU-MIMO) the AP steers different streams to different clients at once, placing the nulls of one client's beam on the other. MU-MIMO needs accurate sounding, which costs airtime, so it pays only with many clients and many AP antennas. The 802.11 generations and their abilities are in [§6.3](#s6-3){.ref}.

**Channel width** is the last lever. Wi-Fi channels are 20 MHz building blocks that bond to 40, 80, 160 and (Wi-Fi 7) 320 MHz. Each doubling roughly doubles the rate and lowers the SNR by 3 dB, because the noise bandwidth doubles. A wide channel also requires every 20 MHz piece to be idle before transmission, so in a crowded band it is rarely available. The primary 20 MHz channel carries the beacons and the control frames of legacy clients.

::: trap
*Claim:* "OFDM and OFDMA are the same thing with a different name", or "MU-MIMO and OFDMA are alternatives." *Why it is wrong:* OFDM is the modulation, used by every generation since 802.11a, in which one user occupies all subcarriers of a symbol. OFDMA, new in 802.11ax, divides the subcarriers among several users within one symbol ([§6.9](#s6-9){.ref}). MU-MIMO separates users in space on the same subcarriers. *Correct statement:* OFDMA shares frequency, MU-MIMO shares space; both can be used together.
:::

::: lens
[QUALCOMM · BROADCOM · NOKIA]{.co}

A Qualcomm candidate was asked to "explain OFDMA and how subcarrier orthogonality is maintained". A strong answer gives the 1/T spacing and the zero-crossing argument, adds the cyclic prefix as the protection against multipath, and only then moves to resource units. Follow-ups: why 802.11ax lengthened the symbol fourfold, and how pilots are used.
:::

::: check
1. How many bits does a 256-QAM symbol carry, and what happens to the required SNR if 64-QAM is replaced by 256-QAM at the same coding rate? [^c62-1]
2. Why does doubling the channel width not double the range? [^c62-2]
3. What limits the number of spatial streams? [^c62-3]
:::

[^c62-1]: 8 bits; the points are closer, so roughly 6 dB more SNR is needed.
[^c62-2]: The noise bandwidth doubles, so the SNR falls by 3 dB and the best MCS is lower at the same distance.
[^c62-3]: The smaller of the transmit and receive antenna counts, and the rank of the channel matrix, which depends on scattering.

:::
