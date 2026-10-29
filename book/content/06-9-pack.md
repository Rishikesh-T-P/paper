::: {.p6}

::: pack
## Revision Spread {#rv6}

::: revision
::: top
**Ten facts.** (1) +3 dB is ×2 and +10 dB is ×10; dBm is absolute (200 mW = 23 dBm); FSPL = 20 log d + 20 log f − 147.55 (m, Hz) and adds 6 dB per doubling of distance or frequency. (2) Shannon: C = B log₂(1 + SNR); doubling the width costs 3 dB of SNR. (3) Rate = data subcarriers × bits × coding × streams ÷ symbol time; 802.11ax at 80 MHz, 1024-QAM, 5/6 gives 600.5 Mb/s per stream. (4) Wi-Fi is CSMA/CA with ACKs; in 5 GHz slot 9, SIFS 16, DIFS 34 µs; CW doubles 15 → 1023 on failure and resets on success; SIFS < DIFS so responses win. (5) RTS/CTS and the NAV fix hidden nodes; exposed nodes remain. (6) Frame Control is little-endian; type 0/1/2 = management/control/data; Address 1 is the receiver, Address 3 depends on To DS/From DS. (7) Lifecycle: discovery, open auth (State 2), association (State 3, AID), 4-way handshake, DHCP; real authentication is PSK/SAE/802.1X. (8) PTK = PRF(PMK, AA, SPA, ANonce, SNonce) = KCK | KEK | TK; the PMK never crosses the air; the GTK travels encrypted in message 3. (9) WPA3 = SAE (no offline dictionary, forward secrecy) + mandatory PMF; transition mode can be downgraded. (10) OFDMA shares frequency (RUs, trigger frames), MU-MIMO shares space, BSS colour allows spatial reuse, TWT schedules sleep; Wi-Fi 7 adds 320 MHz, 4096-QAM, MLO, multi-RU and puncturing; 5G NR: spacing 15 × 2^µ kHz, slot 1 ms ÷ 2^µ, AMF = mobility, SMF = sessions, UPF = user plane.

**Three figures to redraw.** The DCF timeline with the frozen backoff (Figure 6.5), the 4-way handshake with its keys (Figure 6.11), and the OFDM versus OFDMA grid (Figure 6.12).
:::

### Standards at a glance

| Standard | Band · width | QAM · peak | Essence |
|---|---|---|---|
| 802.11b / a / g | 2.4 / 5 / 2.4 GHz · 22 / 20 / 20 MHz | CCK / 64 / 64 · 11 / 54 / 54 Mb/s | DSSS; OFDM |
| 802.11n (Wi-Fi 4) | 2.4, 5 GHz · 20, 40 | 64 · 600 Mb/s | MIMO, A-MPDU |
| 802.11ac (Wi-Fi 5) | 5 GHz · to 160 | 256 · 6.93 Gb/s | DL MU-MIMO |
| 802.11ax (Wi-Fi 6, 6E) | 2.4, 5, 6 GHz · to 160 | 1024 · 9.61 Gb/s | OFDMA, UL MU-MIMO, colour, TWT |
| 802.11be (Wi-Fi 7) | 2.4, 5, 6 GHz · to 320 | 4096 · 46.1 Gb/s | MLO, multi-RU, puncturing |
| LTE / 5G NR | licensed · 20 / 100 to 400 MHz | 256 / 1024 | scheduled OFDMA; EPC / 5GC |

### Timing, sizes and constants

| Item | Value |
|---|---|
| 5 GHz OFDM | slot 9 µs, SIFS 16, PIFS 25, DIFS 34; CWmin 15, CWmax 1023 |
| 2.4 GHz | OFDM short slot: 9, 10, 28; with 802.11b: 20, 10, 50; 802.11b CWmin 31 |
| Contention window | 15, 31, 63, 127, 255, 511, 1023; mean backoff 7.5 slots at CW 15 |
| EDCA (AIFSN, CWmin–CWmax) | VO 2, 3–7; VI 2, 7–15; BE 3, 15–1023; BK 7, 15–1023; AIFS = SIFS + AIFSN × slot |
| Beacon | 100 TU, 1 TU = 1,024 µs, so 102.4 ms; DTIM period 3 gives 307.2 ms |
| Frame sizes | ACK, CTS 14 B; RTS 20 B; header 24 B (30 with Addr4, +2 QoS, +4 HTC); FCS 4 B; CCMP +16 B |
| CCA thresholds | preamble detect about −82 dBm, energy detect about −62 dBm (20 MHz) |
| Sensitivity (HE, 20 MHz) | MCS 0 −82, MCS 7 −64, MCS 9 −57, MCS 11 −52 dBm |
| Wireshark codes | beacon 0x08, probe req/resp 0x04/0x05, assoc req/resp 0x00/0x01, auth 0x0b, deauth 0x0c, RTS/CTS/ACK 0x1b/0x1c/0x1d, BA 0x19, QoS data 0x28 |
| OFDM numerology | 312.5 kHz / 3.2 µs (a to ac); 78.125 kHz / 12.8 µs (ax, be); GI 0.8, 1.6, 3.2 µs |
| RUs in 80 MHz | 37 × 26, 16 × 52, 8 × 106, 4 × 242, 2 × 484, 1 × 996 |
| 6 GHz | 5,925 to 7,125 MHz; 59 × 20, 29 × 40, 14 × 80, 7 × 160 MHz; 3 × 320 MHz |
| Cellular ports | GTP-U 2152, GTP-C 2123, PFCP 8805 (UDP); S1AP 36412, NGAP 38412 (SCTP) |

### Security comparison

| | WEP | WPA | WPA2 | WPA3 |
|---|---|---|---|---|
| Cipher | RC4 | TKIP | CCMP | CCMP, GCMP-256 |
| Personal | static | PSK | PSK | SAE |
| Offline guess | n/a | yes | yes | no |
| PMF | no | no | optional | required |
| Fwd secrecy | no | no | no | yes |

### Key chain and lifecycle in one line each

- **Keys.** Passphrase + SSID → PBKDF2 → PMK (or EAP MSK[0:256], or SAE); PMK + AA + SPA + ANonce + SNonce → PTK = KCK 128 | KEK 128 | TK 128; GMK → GTK, delivered encrypted under the KEK; IGTK protects management multicast.
- **Handshake.** M1 ANonce; M2 SNonce + MIC; M3 GTK + MIC + Install; M4 MIC. The replay counter rises with each new message; a wrong passphrase fails the MIC in M2.
- **Lifecycle.** Beacon or probe, authentication (algorithm 0, SAE 3, FT 2), association (status 0, AID 1 to 2007), EAPOL 1 to 4, DHCP, ARP.
- **Roaming.** k = neighbour report, v = BSS transition request, r = FT with PMK-R0 and PMK-R1; about 20 ms against 200 to 400 ms for full 802.1X.
- **LTE to 5G.** MME → AMF (mobility) + SMF (sessions); S-GW/P-GW user plane → UPF; HSS → UDM + AUSF; PCRF → PCF; S1-U → N3; S1-MME → N2; X2 → Xn; QCI 9 → 5QI 9.
- **Numerology.** µ = 0, 1, 2, 3 gives 15, 30, 60, 120 kHz and slots of 1, 0.5, 0.25, 0.125 ms.

### Flashcards

::: flash
| Q | A | Q | A |
|---|---|---|---|
| 200 mW in dBm | 23 dBm | Why CSMA/CA, not CD | Radio is deaf while sending |
| −3 dB | Half power | DIFS, 5 GHz | 34 µs |
| FSPL, double distance | +6 dB | CW after 3 failures | 127 |
| Thermal floor, 20 MHz | −101 dBm | What sets the NAV | Duration field |
| Bits in 1024-QAM | 10 | RTS/CTS solves | Hidden nodes |
| Wider channel, SNR | −3 dB per doubling | Frame Control order | Little-endian |
| Subcarrier spacing | 1/T | To DS = 1, From DS = 0 | STA to AP: BSSID, SA, DA |
| Cyclic prefix | Absorbs echoes | ACK length | 14 bytes |
| SU- vs MU-MIMO | One vs many clients | Message 1 holds | ANonce, counter |
| ax 80 MHz, 1024-QAM | 600.5 Mb/s per stream | Key that wraps GTK | KEK |
| Beacon interval | 102.4 ms | PMKID | HMAC of PMK, AA, SPA |
| SSID vs BSSID | Name vs radio MAC | KRACK reinstalls | TK, nonce reset |
| Open auth gives | State 2 only | SAE gives | No offline guessing |
| AID range | 1 to 2007 | PMF stops | Forged deauth |
| Voice AIFSN, CW | 2, 3 to 7 | Needs client certs | EAP-TLS |
| A-MPDU vs A-MSDU | FCS per subframe vs one | OFDMA shares | Frequency (RUs) |
| Block Ack, ax | 256 MPDUs | Trigger frame has | RU, MCS, power, length |
| DTIM 3 | 307 ms multicast | BSS colour | 6 bits, HE preamble |
| 2.4 GHz plan | 1, 6, 11 | Wi-Fi 7 factors | 2 × 1.2 × 2 |
| NR slot, µ = 3 | 125 µs | AMF vs SMF | Mobility vs sessions |
:::

:::
:::

:::
