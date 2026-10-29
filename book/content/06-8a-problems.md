::: {.p6}

::: pack
## Problem Set {#ps6}

Every interview question of this pillar is solved once, here, in the compact template: a 30-second answer first, then the approach, answer, follow-ups and common mistakes where they apply. Tags give the companies and round where the question was reported, the difficulty (■□□ easy, ■■□ medium, ■■■ hard), and **S** when a specific question was reported by candidates or **T** when only the topic was reported and the wording is ours. Section references point to the teaching text; the answers add the reasoning an interviewer wants to hear and do not repeat the whole section.

::: problems

::: q
### Q6.1 What is the difference between SSID, BSSID and ESSID?
[CISCO · QUALCOMM · TECH-1 · ■□□ · T]{.meta}

[30-second answer: the SSID is the network's name (up to 32 bytes); the BSSID is the 48-bit MAC address of one AP radio serving that name; the ESSID is the SSID of an extended service set, that is, the same name used by several BSSs joined by a distribution system.]{.short}

**Answer.** A frame carries the BSSID, not the name; the name appears only in beacons, probes and association frames. A dual-band AP with one name has one SSID and two BSSIDs, and a campus has one SSID for hundreds of BSSIDs. **Follow-ups.** A hidden SSID is a beacon with an empty name, not a security measure; one radio can broadcast several SSIDs by deriving a BSSID per SSID from its base address ([§6.3](#s6-3){.ref}). **Mistakes.** Saying that the BSSID is the name, or that the SSID is unique to one AP.
:::

::: q
### Q6.2 Why does Wi-Fi use CSMA/CA instead of CSMA/CD?
[QUALCOMM · BROADCOM · CISCO · TECH-1 · ■□□ · T]{.meta}

[30-second answer: a radio cannot listen while it transmits, because its own signal is some 90 dB stronger than a received one; and in a wireless cell the sender cannot see a collision at the receiver anyway (hidden nodes). So 802.11 avoids collisions with random backoff and confirms success with an ACK.]{.short}

**Answer.** Ethernet detects a collision as a voltage anomaly on the shared wire. A half-duplex radio has a transmitter at +20 dBm and a receiver expecting −70 dBm; even if it could listen, a collision occurs at the receiver, which the sender may not hear. Hence collisions are avoided (carrier sense, DIFS, random backoff, NAV) and detected only by the missing ACK ([§6.4](#s6-4){.ref}). **Follow-ups.** The cost: ACK airtime and backoff overhead; full-duplex radios with self-interference cancellation are a research topic. **Mistakes.** Writing "CSMA/CD" for Wi-Fi.
:::

::: q
### Q6.3 Explain DCF with SIFS, DIFS, slot time and backoff. Why is SIFS shorter than DIFS?
[QUALCOMM · BROADCOM · TECH-1 · ■■□ · T]{.meta}

[30-second answer: a station with a frame waits until the medium has been idle for DIFS = SIFS + 2 slots (34 µs in 5 GHz), then counts down a random backoff in [0, CW] in 9 µs slots, freezing when the medium is busy; at zero it sends and the receiver answers with an ACK after SIFS = 16 µs. SIFS is shorter so that a response always begins before any contender's DIFS expires.]{.short}

**Approach.** State the timing for one PHY, then the five steps. **Answer.** Initial CW is 15; a failed frame (no ACK) doubles it to 31, 63, ..., 1023; success resets it. SIFS-spaced frames form an atomic exchange (data and ACK, RTS and CTS, fragments), which is protected because no station can finish a DIFS wait in between. **Follow-ups.** PIFS, EIFS and AIFS; how the NAV protects the whole exchange; why the backoff is frozen and not redrawn (fairness: the loser keeps its progress). **Mistakes.** Using 2.4 GHz and 5 GHz values together: in 2.4 GHz with 802.11b present, slot 20 µs, SIFS 10 µs, DIFS 50 µs.
:::

::: q
### Q6.4 What is the hidden-node problem? How do RTS/CTS and the NAV solve it? What is the exposed-node problem?
[QUALCOMM · CISCO · TECH-1 · ■■□ · T]{.meta}

[30-second answer: two stations that both reach the AP but not each other cannot sense each other's transmissions and collide at the AP. A short RTS/CTS exchange makes the AP announce the reservation: stations that hear the CTS set their NAV (a countdown of the Duration field) and stay silent. The exposed node is the reverse: a station defers although its transmission would not interfere.]{.short}

**Answer.** The RTS Duration covers 3 SIFS + CTS + DATA + ACK and the CTS Duration covers 2 SIFS + DATA + ACK, so everyone within earshot of either frame is silenced. Collisions can then occur only on the 20-byte RTS. RTS/CTS costs airtime, so it is used only above an RTS threshold (default off). The exposed node (B sends to A, C hears B, C wants to send to D) is not solved inside a cell; across cells it is mitigated by BSS colouring and spatial reuse ([§6.9](#s6-9){.ref}). **Follow-ups.** CTS-to-self (used to protect OFDM frames from 802.11b stations); why NAV is "virtual" carrier sense. **Mistakes.** Saying RTS/CTS eliminates all collisions.
:::

::: q
### Q6.5 What happens to the contention window after a failed transmission and after a success?
[QUALCOMM · TECH-1 · ■■□ · T]{.meta}

[30-second answer: after each failure (no ACK) the contention window doubles, CW ← 2·CW + 1, from 15 up to 1023; after a success, or after the frame is dropped at the retry limit, it returns to CWmin.]{.short}

**Answer.** Binary exponential backoff adapts to load without anyone measuring it: with few stations a small window means little wasted time; with many stations collisions raise the window until two stations rarely draw the same slot. The mean wait grows from 7.5 slots (CW = 15) to 511 slots (CW = 1023) after six failures. **Follow-ups.** Why not reset to CWmin after a failure (it would keep colliding); the retry limits (7 short, 4 long); Bianchi's model of saturation throughput against the number of stations. **Mistakes.** Doubling the window on a success, or confusing "double" with "double plus one".
:::

::: q
### Q6.6 Name the three 802.11 frame types and give two subtypes of each.
[QUALCOMM · BROADCOM · TECH-1 · ■□□ · T]{.meta}

[30-second answer: management (beacon, probe request, authentication, association request, deauthentication), control (RTS, CTS, ACK, Block Ack, PS-Poll) and data (data, QoS data, null).]{.short}

**Answer.** The type is Frame Control bits 2–3 (0, 1, 2) and the subtype bits 4–7; Wireshark's combined code is type × 16 + subtype, for example beacon 0x08, ACK 0x1d, QoS data 0x28 ([§6.5](#s6-5){.ref}). Management frames set up and tear down the relationship; control frames help deliver data (reservation, acknowledgement); data frames carry payload. **Follow-ups.** Which frames carry four addresses (data with To DS = From DS = 1); which have no sequence number (control). **Mistakes.** Putting RTS or ACK among the management frames.
:::

::: q
### Q6.7 Explain the To DS and From DS bits and the meaning of the four address fields in each case.
[QUALCOMM · BROADCOM · TECH-1 · ■■□ · T]{.meta}

[30-second answer: Address 1 is always the receiver and Address 2 the transmitter of this hop; Address 3 and 4 complete the end-to-end picture. (0,0): DA, SA, BSSID. (1,0) station to AP: BSSID, SA, DA. (0,1) AP to station: DA, BSSID, SA. (1,1) AP to AP: RA, TA, DA, SA.]{.short}

**Answer.** To DS = 1 means the frame is addressed to the distribution system, so the receiver is the AP; From DS = 1 means it comes from the DS, so the transmitter is the AP. When both are 1 neither radio is an end system and a fourth address is needed ([§6.5](#s6-5){.ref}). A worked example: laptop to server via AP uses (1,0) with A1 = AP, A2 = laptop, A3 = server. **Follow-ups.** The frame header lengths (24, 30 with the fourth address, plus 2 for QoS, 4 for HT Control); WDS and mesh. **Mistakes.** Treating Address 3 as always the destination.
:::

::: q
### Q6.8 What information is in a beacon frame?
[QUALCOMM · CISCO · JUNIPER · TECH-1 · ■■□ · T]{.meta}

[30-second answer: a timestamp, the beacon interval (default 100 TU = 102.4 ms), capability bits, the SSID, supported rates, the channel and HT/VHT/HE operation, the TIM (power-save indications), the country, and the RSN element with the security suites.]{.short}

**Answer.** A beacon is a management frame with the broadcast address as receiver and the BSSID as transmitter. The *timestamp* synchronises the stations' timers (needed for TWT and power save); the TIM tells sleeping stations whether frames are buffered; the RSN element says which ciphers and key management (PSK, SAE, 802.1X) are offered; the HT/VHT/HE capability and operation elements advertise widths and features; vendor elements add WMM parameters and load. **Follow-ups.** Why beacons are sent at the lowest basic rate and the cost of many SSIDs; what a probe response adds (nothing but the TIM) ([§6.5](#s6-5){.ref}). **Mistakes.** Forgetting the TIM, or saying that the beacon carries the passphrase.
:::

::: q
### Q6.9 Walk through how a station connects to a WPA2-Personal AP, frame by frame.
[QUALCOMM · CISCO · JUNIPER · TECH-1 · ■■□ · S]{.meta}

[30-second answer: beacon or probe request/response (discovery); authentication seq 1 and 2 (open); association request and response (status 0, AID); EAPOL-Key messages 1 to 4 (ANonce, SNonce + MIC, GTK + MIC, MIC) which derive and install keys; then DHCP and ARP in encrypted data frames.]{.short}

**Answer.** After the beacon or probe the station is in State 1. The open authentication moves it to State 2 and the association to State 3, but the controlled port stays closed. The station already has the PMK from the passphrase; messages 1 and 2 exchange nonces so that both derive the PTK, message 2 proves the station's knowledge by its MIC, message 3 delivers the GTK, and message 4 confirms. Then both install the TK, the port opens, and DHCP follows ([§6.6](#s6-6){.ref}). **Follow-ups.** What a wrong passphrase looks like in the capture (message 2 rejected, then reason code 15 after retries); where 802.1X would insert itself; why DHCP is invisible without decryption. **Mistakes.** Putting DHCP before the 4-way handshake.
:::

::: q
### Q6.10 What is the 4-way handshake for, and what keys result from it?
[QUALCOMM · CISCO · BROADCOM · TECH-1 · ■■□ · S]{.meta}

[30-second answer: it proves that both sides hold the PMK without sending it, derives a fresh PTK (KCK, KEK, TK) from the PMK and two nonces, and delivers the GTK (and IGTK) encrypted, so that unicast and group traffic can be protected.]{.short}

**Answer.** The AP sends ANonce (1); the station replies with SNonce and a MIC under the KCK (2); the AP sends the encrypted GTK, its own RSN element and a MIC with the Install flag (3); the station acknowledges (4). Keys: KCK (authenticates EAPOL messages), KEK (encrypts the GTK), TK (encrypts unicast data), plus the GTK for group traffic ([§6.7](#s6-7){.ref}). **Follow-ups.** What message 3 repeats the RSN element for (detecting a downgrade by comparing it with the beacon); why four messages (mutual proof, plus the group key). **Mistakes.** Saying that the PSK is sent, or that the handshake negotiates the PMK.
:::

::: q
### Q6.11 How is the PTK derived? Why are both nonces and both MAC addresses included?
[QUALCOMM · TECH-2 · ■■■ · T]{.meta}

[30-second answer: PTK = PRF-384(PMK, "Pairwise key expansion", min(AA, SPA) ‖ max(AA, SPA) ‖ min(ANonce, SNonce) ‖ max(ANonce, SNonce)), split into KCK, KEK and TK of 128 bits each. The nonces make it fresh and the addresses bind it to this pair.]{.short}

**Approach.** Give the formula, then the role of each input. **Answer.** The PRF is HMAC-SHA1 iterated with a counter until 384 bits are produced. If only the AP chose the nonce, an attacker could replay an old message 1 and force the station to reuse an old PTK; because each side adds its own random value, neither alone controls the key. The two addresses prevent a PTK from being moved to another station or AP. Ordering by min and max lets both sides compute the same string without agreeing on roles ([§6.7](#s6-7){.ref}; Lab 6.7 computes one). **Follow-ups.** The PMK itself comes from PBKDF2 (4,096 iterations) or from the MSK; for SHA-256-based key management the PRF is HMAC-SHA256. **Mistakes.** Including the PMK in the message or the passphrase in the PRF input.
:::

::: q
### Q6.12 What is the replay counter in EAPOL-Key frames? What was KRACK?
[QUALCOMM · BROADCOM · TECH-2 · ■■■ · T]{.meta}

[30-second answer: the replay counter increases with every authenticator message and must be echoed by the reply, so that old messages are rejected. KRACK (2017) made a station reinstall an already-installed key when message 3 was retransmitted, which reset the packet number and so reused the encryption nonce.]{.short}

**Answer.** The attacker blocks message 4; the AP, getting no answer, resends message 3 with a higher counter, so it is valid. A client that installs the TK on every message 3 resets the CCMP packet number to zero; keystream is then reused, allowing replay of frames and, with other ciphers or implementations, decryption or forgery. The fix is on the client: install a key once and ignore later copies, or reinstall without resetting the counters. The replay counter could not help, since the retransmission was genuine. **Follow-ups.** Why it affected also the group-key and FT handshakes; why WPA3 does not remove the issue by itself (the same handshake). **Mistakes.** Claiming that the attacker learned the passphrase.
:::

::: q
### Q6.13 Difference between PMK, PTK and GTK. When is the GTK rotated?
[QUALCOMM · CISCO · TECH-1 · ■■□ · T]{.meta}

[30-second answer: the PMK is the long-lived shared secret (from the passphrase or EAP); the PTK is the per-station, per-association session key derived from it; the GTK is the AP's key for broadcast and multicast, shared by all stations. The GTK is rotated periodically and when a station leaves.]{.short}

**Answer.** The PMK is never used to encrypt data; it only seeds the PTK, which gives each station a separate key, so one station cannot read another's unicast traffic. The GTK must be common, so any associated station can decrypt group frames (and could forge them, which is why group traffic is the weaker part). The AP renews it with a two-message group-key handshake after the rekey interval, and when a station disassociates so that the departed station loses access. **Follow-ups.** The IGTK for management frames; PMKID caching of the PMK. **Mistakes.** Saying that all stations share one PTK.
:::

::: q
### Q6.14 Why is WPA2-PSK vulnerable to offline dictionary attacks, and how does SAE fix it?
[QUALCOMM · CISCO · JUNIPER · TECH-1 · ■■□ · T]{.meta}

[30-second answer: an eavesdropper who captures messages 1 and 2 can test passphrase guesses offline: guess, derive PMK, PTK and KCK, recompute the MIC and compare. SAE gives each exchange fresh random secrets, so the transcript contains nothing to check a guess against, and every guess needs an online attempt.]{.short}

**Answer.** PBKDF2 slows each guess by 4,096 HMACs, but a GPU does billions of hashes a second, so an 8-character passphrase of common words falls in hours. In SAE both parties map the password to a curve point, send a commit (a scalar and an element built from random values) and a confirm; without the password and a live peer one learns nothing, and the AP can rate-limit attempts. A bonus is forward secrecy: a later leak of the password does not decrypt old sessions ([§6.7](#s6-7){.ref}). **Follow-ups.** The PMKID attack; Dragonblood and hash-to-element; why transition mode is weaker. **Mistakes.** Saying that SAE makes weak passwords safe.
:::

::: q
### Q6.15 What is PMF (802.11w) and which attack does it stop?
[CISCO · QUALCOMM · TECH-1 · ■□□ · T]{.meta}

[30-second answer: protected management frames authenticate and encrypt robust management frames (deauthentication, disassociation, action frames), stopping forged deauthentication and disassociation attacks that disconnect clients.]{.short}

**Answer.** Before 802.11w anyone could spoof the AP's address in a deauthentication frame and eject a client at will, or force it to re-handshake for an offline attack. With PMF, unicast management frames are encrypted under the TK, and group-addressed ones carry an integrity check under the IGTK, so a spoofed frame fails verification. It is mandatory in WPA3 and in 6 GHz, and optional in WPA2. **Follow-ups.** The SA Query procedure for the case in which one side has lost its keys; what is not protected (beacons, radio-level jamming). **Mistakes.** Believing that PMF encrypts data frames or prevents jamming.
:::

::: q
### Q6.16 Explain 802.1X roles and name two EAP methods. Which needs client certificates?
[CISCO · JUNIPER · TECH-1 · ■■□ · T]{.meta}

[30-second answer: the supplicant (client) wants access, the authenticator (the AP or switch) controls a port, and the authentication server (RADIUS) decides. EAP-TLS needs a certificate on both sides; PEAP needs only a server certificate and uses a password inside the TLS tunnel.]{.short}

**Answer.** The AP relays EAP messages between EAPOL toward the client and RADIUS toward the server; the port is blocked except for EAPOL until Access-Accept arrives, which also carries the MSK from which the PMK comes. EAP-TLS is the strongest, because there is no password to steal, but needs a certificate infrastructure; PEAP-MSCHAPv2 is the commonest. The generic flow is in [§9.12](#s9-12){.ref}; the Wi-Fi-specific part is in [§6.7](#s6-7){.ref}. **Follow-ups.** Why a client that skips server-certificate validation is vulnerable to a rogue AP; eduroam as a federation of RADIUS servers. **Mistakes.** Saying that the AP authenticates the user.
:::

::: q
### Q6.17 What is the difference between authentication and association in 802.11?
[QUALCOMM · TECH-1 · ■□□ · T]{.meta}

[30-second answer: authentication (open system) is a two-frame formality that moves a station to State 2 and has no credentials; association negotiates the capabilities, assigns an association ID and moves it to State 3. Real security comes afterwards, with SAE or 802.1X and the 4-way handshake.]{.short}

**Answer.** The old state machine had to be preserved for compatibility, so every station still performs the open exchange. Association carries what matters for the data path: rates, HT/VHT/HE capabilities, the RSN selection and power-save parameters. Deauthentication returns the station to State 1 and disassociation to State 2 ([§6.6](#s6-6){.ref}). **Follow-ups.** SAE reuses the authentication frames (algorithm 3) for its commit and confirm; FT uses algorithm 2. **Mistakes.** Calling the open exchange "authentication" in the security sense.
:::

::: q
### Q6.18 Explain OFDM and why the subcarriers are orthogonal. What is the cyclic prefix for?
[QUALCOMM · NOKIA · TECH-1 · ■■□ · S]{.meta}

[30-second answer: OFDM sends many low-rate symbols on narrow subcarriers spaced exactly 1/T apart, where T is the symbol duration; each subcarrier's spectrum is zero at the centres of all others, so a receiver integrating over T separates them. The cyclic prefix, a copy of the symbol's tail placed in front, absorbs multipath echoes so symbols do not overlap.]{.short}

**Answer.** Long symbols make multipath echoes a small fraction of the symbol. Orthogonality is exact if the subcarrier spacing equals 1/T and the receiver samples over one useful symbol; the cyclic prefix keeps the block periodic so this still holds with echoes shorter than the prefix. The IFFT/FFT pair makes the transform cheap ([§6.2](#s6-2){.ref}). **Follow-ups.** The price of the prefix (0.8 µs in 12.8 µs is 6%); what breaks orthogonality (frequency offset and Doppler, which is why oscillator accuracy matters, and why NR uses wider spacing at mmWave); pilots. **Mistakes.** Saying that the subcarriers do not overlap in frequency: they do, but are orthogonal.
:::

::: q
### Q6.19 OFDM versus OFDMA.
[QUALCOMM · CISCO · JUNIPER · TECH-1 · ■■□ · T]{.meta}

[30-second answer: in OFDM, one transmission occupies all the subcarriers of the channel; in OFDMA (802.11ax) the AP divides them into resource units and gives different units to different stations within the same symbol.]{.short}

**Answer.** OFDMA wins when many stations have small amounts of data: nine 100-byte frames take about a quarter of the airtime and cause no collisions ([§6.9](#s6-9){.ref}). It needs scheduling by the AP (a trigger frame in the uplink), so it adds complexity, and it does not raise the single-user peak rate. **Follow-ups.** The RU sizes (26 to 996 tones) and number per width; how cellular networks have used OFDMA since LTE. **Mistakes.** Claiming that OFDMA increases peak throughput.
:::

::: q
### Q6.20 SU-MIMO versus MU-MIMO. What did 802.11ax add over 802.11ac for MU-MIMO?
[QUALCOMM · BROADCOM · TECH-1 · ■■□ · T]{.meta}

[30-second answer: SU-MIMO sends several spatial streams to one client; MU-MIMO sends different streams to different clients at once, separated by beamforming. 802.11ac had downlink MU-MIMO only; 802.11ax added uplink MU-MIMO, up to eight users, and combination with OFDMA resource units of 106 tones or more.]{.short}

**Answer.** MU-MIMO needs channel knowledge (sounding), so that the AP can place a null of each client's beam on the others; the sounding airtime and the quality of the feedback limit the gain, which appears with many clients and an AP with many antennas. Uplink MU-MIMO adds the need to synchronise the clients, which the trigger frame provides ([§6.2](#s6-2){.ref}, [§6.9](#s6-9){.ref}). **Follow-ups.** Why the number of streams is bounded by the AP's antennas; the stream count of a typical phone (1 or 2). **Mistakes.** Mixing up the roles: MU-MIMO shares space, OFDMA shares frequency.
:::

::: q
### Q6.21 What is a trigger frame? Describe an uplink OFDMA exchange.
[QUALCOMM · BROADCOM · TECH-2 · ■■■ · T]{.meta}

[30-second answer: a trigger frame is a control frame by which the AP solicits uplink transmissions: it lists, for each station, its RU, MCS, power target and length. After SIFS the stations send HE trigger-based PPDUs simultaneously, and the AP replies with one multi-station Block Ack.]{.short}

**Answer.** The AP first gathers buffer status (from earlier frames or a buffer-status poll), then sends the trigger. All responders must end together, so shorter ones pad. The AP controls the target receive power, which keeps the signals within a few decibels at its antenna and so makes the shared symbol decodable. Stations without a grant may use the random-access RUs (UORA). A trigger can also carry MU-BAR to solicit acknowledgements ([§6.9](#s6-9){.ref}). **Follow-ups.** The cost of the trigger and the padding; frequency and timing synchronisation (the stations align to the trigger within the guard interval). **Mistakes.** Forgetting that uplink OFDMA is scheduled, not contended.
:::

:::
:::

:::
