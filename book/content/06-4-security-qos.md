::: {.p6}

## [6.7]{.sec}Security: WPA2, WPA3 and PMF [Must · ■■■]{.tag} {#s6-7}

A radio signal can be received by anyone in range, so a wireless link needs encryption that the wired link does not. Three properties are wanted: only authorised stations may join, traffic must be unreadable to others, and frames must not be forged or replayed. The security of 802.11 has been rebuilt twice because the first two designs failed.

*Wired Equivalent Privacy* (WEP, 1997) used the RC4 stream cipher with a 24-bit initialisation vector (IV) sent in clear and a static shared key. The IV space is so small that it repeats within hours on a busy network, and weaknesses in the way RC4 consumed the IV let an attacker recover the key from a few tens of thousands of packets, in minutes. Its integrity check was a plain CRC-32, which is linear and cannot detect deliberate edits. WEP is broken and must not be deployed. *WPA* (2003) was a stop-gap that kept the old hardware by wrapping RC4 in TKIP, with a per-packet key and a message integrity code; TKIP is now also deprecated. The two designs that matter are WPA2 and WPA3.

### WPA2-Personal: from passphrase to session keys

WPA2 (the RSN of IEEE 802.11i, 2004) encrypts with *CCMP*, which is AES in counter mode for confidentiality and CBC-MAC for integrity. Keys are organised in a hierarchy, shown in Figure 6.10. At the top is the *pairwise master key* (PMK), a secret shared by the station and the AP. In WPA2-Personal the PMK is computed from the passphrase and the network name:

PMK = PBKDF2-HMAC-SHA1(passphrase, SSID, 4096 iterations, 256 bits).

The 4,096 iterations slow down a guesser, and including the SSID makes precomputed tables specific to one network name. The PMK is never transmitted. From it, each association derives a fresh *pairwise transient key* (PTK) by a pseudo-random function, the PRF built on HMAC-SHA1:

PTK = PRF(PMK, "Pairwise key expansion", min(AA, SPA) ‖ max(AA, SPA) ‖ min(ANonce, SNonce) ‖ max(ANonce, SNonce)),

where AA is the authenticator's (AP's) address, SPA the supplicant's (station's) address, and the two nonces are random 256-bit numbers chosen by each side for this attempt. For CCMP the output is 384 bits, split into three 128-bit keys: the *key confirmation key* (KCK), which authenticates the handshake messages with a MIC; the *key encryption key* (KEK), which wraps the group key; and the *temporal key* (TK), which encrypts and authenticates the unicast data.

<figure>
<svg viewBox="0 0 480 198" width="480"><defs><marker id="i7" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="a7" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><rect class="box" x="10" y="20" width="120" height="26" /><text class="lbl" x="70" y="31" text-anchor="middle" >Passphrase + SSID</text><text class="sm" x="70" y="41" text-anchor="middle" >PBKDF2, 4096 x HMAC-SHA1</text><rect class="box" x="10" y="56" width="120" height="26" /><text class="lbl" x="70" y="67" text-anchor="middle" >802.1X: EAP MSK</text><text class="sm" x="70" y="77" text-anchor="middle" >first 256 bits</text><rect class="box" x="10" y="92" width="120" height="26" /><text class="lbl" x="70" y="103" text-anchor="middle" >WPA3: SAE</text><text class="sm" x="70" y="113" text-anchor="middle" >commit / confirm</text><rect class="hl" x="170" y="52" width="80" height="34" stroke="#1A1D23" stroke-width=".9"/><text class="lbl" x="210" y="66" text-anchor="middle" >PMK</text><text class="sm" x="210" y="78" text-anchor="middle" >never sent</text><line class="ln" x1="130" y1="33" x2="168" y2="62" marker-end="url(#i7)"/><line class="ln" x1="130" y1="69" x2="168" y2="69" marker-end="url(#i7)"/><line class="ln" x1="130" y1="105" x2="168" y2="69" marker-end="url(#i7)"/><rect class="box" x="290" y="20" width="110" height="34" /><text class="lbl" x="345" y="34" text-anchor="middle" >PTK = PRF(PMK,</text><text class="sm" x="345" y="46" text-anchor="middle" >AA, SPA, ANonce, SNonce)</text><line class="acc" x1="250" y1="62" x2="288" y2="40" marker-end="url(#a7)"/><text class="sm" x="270" y="30" text-anchor="end" >nonces and MACs</text><rect class="fill" x="270" y="80" width="66" height="30" /><text class="lbl" x="303" y="93" text-anchor="middle" >KCK 128</text><text class="sm" x="303" y="104" text-anchor="middle" >MIC of EAPOL</text><line class="lg" x1="345" y1="54" x2="303" y2="80" /><rect class="fill" x="340" y="80" width="66" height="30" /><text class="lbl" x="373" y="93" text-anchor="middle" >KEK 128</text><text class="sm" x="373" y="104" text-anchor="middle" >encrypts GTK</text><line class="lg" x1="345" y1="54" x2="373" y2="80" /><rect class="fill" x="410" y="80" width="66" height="30" /><text class="lbl" x="443" y="93" text-anchor="middle" >TK 128</text><text class="sm" x="443" y="104" text-anchor="middle" >encrypts unicast</text><line class="lg" x1="345" y1="54" x2="443" y2="80" /><rect class="box" x="170" y="135" width="80" height="30" /><text class="lbl" x="210" y="148" text-anchor="middle" >GMK (AP)</text><text class="sm" x="210" y="159" text-anchor="middle" >random</text><rect class="box" x="290" y="135" width="80" height="30" /><text class="lbl" x="330" y="148" text-anchor="middle" >GTK</text><text class="sm" x="330" y="159" text-anchor="middle" >multicast</text><rect class="box" x="390" y="135" width="80" height="30" /><text class="lbl" x="430" y="148" text-anchor="middle" >IGTK (PMF)</text><text class="sm" x="430" y="159" text-anchor="middle" >mgmt multicast</text><line class="ln" x1="250" y1="150" x2="288" y2="150" marker-end="url(#i7)"/><line class="lg" x1="370" y1="150" x2="390" y2="150" /><text class="sm" x="240" y="190" text-anchor="middle" >Sent over the air: nonces, MICs, and the GTK encrypted under the KEK (in M3). The PMK and PTK never are.</text></svg>
<figcaption><b>Figure 6.10</b> The key hierarchy: three ways to obtain a PMK, one PTK per station, and group keys chosen by the AP.</figcaption>
</figure>

**Why both nonces and both addresses are inputs.** The nonces make the PTK fresh: each side contributes randomness, so neither the AP nor an attacker replaying an old message can force the reuse of an earlier key. The addresses bind the key to this pair of devices, so a PTK cannot be moved to another association. Taking the minimum and maximum of each pair is a convention that lets both sides concatenate in the same order without knowing who is who.

**The group key.** Broadcast and multicast frames go to many stations, so they need a key all share. The AP chooses a *group temporal key* (GTK), derives it from a random group master key and its address, and delivers it, encrypted under the KEK, inside message 3 of the handshake. The GTK is changed when a station leaves the network (so that it can no longer decrypt group traffic) and periodically, by a short two-message group-key handshake.

### The 4-way handshake

The handshake has two aims: to prove to each side that the other holds the PMK, and to install the PTK and GTK. It is carried in *EAPOL-Key* frames and runs after association (Figure 6.11).

<figure>
<svg viewBox="0 0 480 256" width="480"><defs><marker id="i6" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="a6" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><text class="lbl" x="70" y="12" text-anchor="middle" >Supplicant (STA)</text><text class="lbl" x="410" y="12" text-anchor="middle" >Authenticator (AP)</text><line class="lg" x1="70" y1="18" x2="70" y2="250" /><line class="lg" x1="410" y1="18" x2="410" y2="250" /><rect class="lg" x="130" y="20" width="220" height="0.1" /><rect class="fill" x="8" y="24" width="118" height="30" /><text class="sm" x="67" y="36" text-anchor="middle" >knows PMK, own MAC</text><text class="sm" x="67" y="47" text-anchor="middle" >picks SNonce</text><rect class="fill" x="354" y="24" width="118" height="30" /><text class="sm" x="413" y="36" text-anchor="middle" >knows PMK, own MAC</text><text class="sm" x="413" y="47" text-anchor="middle" >picks ANonce</text><line class="ln" x1="408" y1="66" x2="72" y2="78" marker-end="url(#i6)"/><text class="lbl" x="240" y="61" text-anchor="middle" >M1: ANonce, replay counter r</text><text class="sm" x="240" y="88" text-anchor="middle" >Key Info: Pairwise, Ack</text><line class="acc" x1="72" y1="112" x2="408" y2="124" marker-end="url(#a6)"/><text class="lbl" x="240" y="107" text-anchor="middle" >M2: SNonce, MIC, STA's RSN IE</text><text class="sm" x="240" y="134" text-anchor="middle" >Key Info: Pairwise, MIC</text><line class="acc" x1="408" y1="158" x2="72" y2="170" marker-end="url(#a6)"/><text class="lbl" x="240" y="153" text-anchor="middle" >M3: ANonce, MIC, AP's RSN IE, {GTK}</text><text class="sm" x="240" y="180" text-anchor="middle" >Key Info: Install, Ack, MIC, Secure, Encrypted</text><line class="acc" x1="72" y1="204" x2="408" y2="216" marker-end="url(#a6)"/><text class="lbl" x="240" y="199" text-anchor="middle" >M4: MIC (acknowledgement)</text><text class="sm" x="240" y="226" text-anchor="middle" >Key Info: Pairwise, MIC, Secure</text><rect class="hl" x="8" y="70" width="118" height="24" stroke="#1A1D23" stroke-width=".9"/><text class="sm" x="67" y="85" text-anchor="middle" >derives PTK</text><rect class="hl" x="354" y="116" width="118" height="24" stroke="#1A1D23" stroke-width=".9"/><text class="sm" x="413" y="131" text-anchor="middle" >derives PTK, checks MIC</text><rect class="hl" x="8" y="162" width="118" height="24" stroke="#1A1D23" stroke-width=".9"/><text class="sm" x="67" y="177" text-anchor="middle" >checks MIC, decrypts GTK</text><rect class="box" x="8" y="208" width="118" height="24" /><text class="sm" x="67" y="223" text-anchor="middle" >installs TK and GTK</text><rect class="box" x="354" y="208" width="118" height="24" /><text class="sm" x="413" y="223" text-anchor="middle" >installs TK on receipt</text><text class="sm" x="240" y="246" text-anchor="middle" >M2 to M4 repeat the replay counter of the message they answer; the AP increments it for each new message</text></svg>
<figcaption><b>Figure 6.11</b> The 4-way handshake, with the key-information flags and the moment each side can derive and install keys.</figcaption>
</figure>

1. **Message 1 (AP → station).** The AP sends its ANonce and a replay counter. The station can now compute the PTK, because it has the PMK, both addresses, its own SNonce and the ANonce.
2. **Message 2 (station → AP).** The station sends its SNonce, its RSN element and a MIC computed with the KCK over the whole message. The AP computes the PTK with the SNonce and verifies the MIC. A wrong passphrase gives a different PMK, hence a different KCK, hence a failed MIC, and the AP drops the exchange; this is the source of reason code 15.
3. **Message 3 (AP → station).** The AP sends the ANonce again, its own RSN element (which the station compares with the beacon, to catch tampering), the GTK encrypted with the KEK, and a MIC. The *Install* flag tells the station to install the TK.
4. **Message 4 (station → AP).** The station acknowledges with a MIC. Both sides now install the TK and the controlled port opens.

The *replay counter* is a number in every EAPOL-Key frame. The AP increases it for each new message, and the station answers with the counter of the message being answered; a receiver discards a frame whose counter is not higher than the last one accepted. It prevents an attacker from replaying captured handshake messages.

**KRACK.** In 2017 a key reinstallation attack showed a flaw in the way implementations handled message 3. If message 4 is blocked, the AP resends message 3, with a new, higher replay counter and therefore valid. A station that follows the standard literally reinstalls the same TK on receiving it and resets its packet number (the CCMP nonce) to zero. A nonce is then used twice under one key, so an attacker can replay frames or, with a stream-style cipher, recover the keystream and decrypt. The counter does not help, because the retransmitted message is genuine. The remedy is a software change: install a key only once, and ignore the retransmission.

**Why WPA2-PSK is vulnerable to an offline dictionary attack.** An attacker who captures messages 1 and 2 knows the nonces and both addresses; to test a guessed passphrase he computes the PMK, the PTK and the KCK and checks whether the MIC in message 2 matches. That test requires no interaction with the network, so billions of guesses per second on graphics hardware are possible and weak passphrases fall in hours. A related shortcut reads the PMKID (an HMAC of the PMK and the two addresses) from the first message alone. The defence is a long random passphrase, or no passphrase at all, with 802.1X or SAE.

::: lab
`LAB 6.7 · 20 MIN` Derive a PMK and a PTK in Python and see which parts depend on the nonces. The nonces and addresses below are synthetic; in Lab 6-L5 they come from a capture.

```python
import hashlib, hmac
def prf(key, label, data, bits):
    out, i = b"", 0
    while len(out) * 8 < bits:
        msg = label + b"\x00" + data + bytes([i])
        out += hmac.new(key, msg, hashlib.sha1).digest()
        i += 1
    return out[:bits // 8]
pmk = hashlib.pbkdf2_hmac("sha1", b"packet123", b"IITLab", 4096, 32)
aa, spa = bytes.fromhex("0211223344aa"), bytes.fromhex("0211223344bb")
an, sn = bytes(range(0x00, 0x20)), bytes(range(0x80, 0xA0))
data = min(aa, spa) + max(aa, spa) + min(an, sn) + max(an, sn)
ptk = prf(pmk, b"Pairwise key expansion", data, 384)
print("PMK", pmk[:8].hex())
print("KCK", ptk[:16].hex())
print("TK ", ptk[32:48].hex())
```

```
PMK f475f5c28b6c9ae2
KCK 274c66d2edb317fe68a08d7c79f78756
TK  5f62b371f013c07535625e7a4e777879
```

**What you should notice:** change one nonce byte and the KCK and TK change completely, while the PMK stays the same, since it depends only on the passphrase and SSID. In a real capture the same KCK, applied with HMAC-SHA1 (truncated to 16 bytes) to the EAPOL frame of message 2 with its MIC field zeroed, reproduces the MIC in the frame; that match proves the passphrase.
:::

### WPA2-Enterprise

In an enterprise network each user has individual credentials, and the PMK comes from an authentication server instead of a passphrase. Three roles take part: the *supplicant* (the station), the *authenticator* (the AP, which blocks all traffic except EAPOL until told otherwise), and the *authentication server* (a RADIUS server). The generic IEEE 802.1X and EAP exchange is taught in [§9.12](#s9-12){.ref}; the Wi-Fi-specific parts are these. EAP messages travel between station and AP inside EAPOL frames, and between AP and server inside RADIUS Access-Request and Access-Challenge packets. On success the server sends Access-Accept together with the *master session key* (MSK); the first 256 bits of the MSK are the PMK, which the AP then uses in the same 4-way handshake as above. The AP never learns the user's credentials, and each user has a different PMK, so a leaked key exposes one session only.

Two EAP methods matter in interviews. *EAP-TLS* authenticates both ends with certificates, so every client needs one; it is the strongest and the costliest to deploy. *PEAP* builds a TLS tunnel authenticated by the server's certificate alone and runs a password method (MSCHAPv2) inside it; it needs only a server certificate. The common deployment mistake is a client that does not validate the server certificate, which lets a rogue AP harvest password hashes.

### WPA3

WPA3 (2018) changes the personal mode and tightens the rest. For the personal mode, *simultaneous authentication of equals* (SAE, a form of the Dragonfly exchange) replaces the PSK derivation. Both sides map the password to a point on an elliptic curve, each picks a random secret, and they swap a *commit* (a scalar and a curve element) and then a *confirm*, in authentication frames with algorithm 3. The result is a PMK that is unique to each session and does not follow from the transcript, with two benefits. A captured exchange offers an attacker no value to test a guess against, so each guess needs a live interaction with the network, which the AP can rate-limit; this ends the offline dictionary attack. And a later compromise of the password does not reveal earlier sessions, a property called *forward secrecy*. The 4-way handshake still follows, as before, to derive the PTK from the SAE-derived PMK. The *hash-to-element* variant avoids timing leaks found in the original password-mapping loop, which were published as the "Dragonblood" weaknesses.

WPA3 also makes *protected management frames* mandatory, offers a 192-bit enterprise suite (GCMP-256 with 384-bit hash functions), and adds *Opportunistic Wireless Encryption* (OWE) for open networks: a Diffie–Hellman exchange at association gives each client its own key with no password, which stops passive eavesdropping, though not an impostor AP.

**Transition mode.** A network that advertises both WPA2-PSK and WPA3-SAE with the same passphrase lets old devices connect, but also lets an attacker run a rogue WPA2-only AP and force a downgrade, so strong protection exists only when WPA3 alone is configured.

### Protected management frames (802.11w)

Before 802.11w the management frames, including deauthentication and disassociation, were unauthenticated. Anyone could forge a deauthentication frame from the AP and eject a station, and repeat it indefinitely. *Protected management frames* (PMF) authenticate robust management frames: unicast ones are encrypted with the TK, and group-addressed ones carry an integrity code made with a separate *integrity group temporal key* (IGTK) delivered in message 3. A station that receives a forged deauthentication simply discards it. If a station has lost its keys and the AP sends an unprotected disassociation, the SA Query exchange verifies that the request is genuine. PMF can be "capable" or "required" in the RSN element; WPA3 and 6 GHz operation require it. PMF does not protect beacons or the radio layer, so jamming remains possible.

| | WEP | WPA | WPA2 | WPA3 |
|---|---|---|---|---|
| Year | 1997 | 2003 | 2004 | 2018 |
| Cipher | RC4, 24-bit IV | RC4 with TKIP | AES-CCMP | AES-CCMP (GCMP-256 for 192-bit mode) |
| Integrity | CRC-32 | Michael MIC | CCM MIC (8 B) | CCM or GCM |
| Personal key setup | static key | PSK, PBKDF2 | PSK, PBKDF2 | SAE (Dragonfly) |
| Enterprise | none | 802.1X | 802.1X | 802.1X, 192-bit option |
| Management-frame protection | none | none | optional (802.11w) | mandatory |
| Offline dictionary attack | n/a | yes | yes | no |
| Forward secrecy | no | no | no | yes (SAE) |
| Status | broken | deprecated | baseline | current |

::: trap
*Claim:* "The PSK is sent during the 4-way handshake", or "WPA3 makes weak passwords safe." *Why it is wrong:* neither the PSK nor the PMK is ever sent; only nonces, MICs and the encrypted GTK are. SAE removes the offline attack but cannot prevent online guessing, which the AP must still limit. *Correct statement:* the handshake proves possession of the PMK without transmitting it; WPA3 raises the cost of a guess from computation to interaction.
:::

::: lens
[QUALCOMM · CISCO · JUNIPER · BROADCOM]{.co}

"What is the 4-way handshake for, and what keys result?" and "how is the PTK derived and why are the nonces included?" are Qualcomm staples, and the follow-ups on KRACK and SAE are common at Cisco and Juniper. A strong answer draws the key hierarchy, states what each of KCK, KEK and TK does, says what each message proves, and explains why the passphrase does not cross the air. Follow-ups: PMKID caching, what changes under 802.1X, and the downgrade in transition mode.
:::

::: check
1. Which key authenticates the handshake messages, and which encrypts the GTK? [^c67-1]
2. What stops a forged deauthentication frame under PMF? [^c67-2]
3. Under 802.1X, from what is the PMK derived? [^c67-3]
:::

[^c67-1]: The KCK authenticates (the MIC); the KEK encrypts the GTK in message 3.
[^c67-2]: The frame must carry a valid integrity check or be encrypted under keys the attacker lacks, so the station discards it.
[^c67-3]: The first 256 bits of the MSK, delivered to the AP by the RADIUS server.

## [6.8]{.sec}QoS, aggregation and power save [Should · ■■□]{.tag} {#s6-8}

The DCF of [§6.4](#s6-4){.ref} treats all frames alike, so a bulk download and a voice call compete equally. Three mechanisms refine it: priority access (EDCA), aggregation to cut overhead, and sleep scheduling.

### EDCA and access categories

*Enhanced distributed channel access* (EDCA), the QoS part of the *Wi-Fi Multimedia* (WMM) profile, keeps contention but changes the parameters. Each station has four queues, the *access categories* (AC), each running its own backoff with its own *arbitration interframe space* (AIFS = SIFS + AIFSN × slot), its own contention window and a transmission opportunity limit. A higher priority means a shorter wait and a smaller window, so voice wins the medium more often, though never with certainty. The default parameters for a non-AP station in 5 GHz are as follows.

| Access category | Typical use | AIFSN | CWmin | CWmax | TXOP limit | Mean first wait |
|---|---|---|---|---|---|---|
| AC_VO | voice | 2 | 3 | 7 | 1.504 ms | 47.5 µs |
| AC_VI | video | 2 | 7 | 15 | 3.008 ms | 65.5 µs |
| AC_BE | best effort | 3 | 15 | 1023 | none | 110.5 µs |
| AC_BK | background | 7 | 15 | 1023 | none | 146.5 µs |

The last column is SIFS + AIFSN × 9 µs + (CWmin ÷ 2) × 9 µs; for voice, 16 + 18 + 13.5 = 47.5 µs, and for best effort, 16 + 27 + 67.5 = 110.5 µs, so voice starts on average 63 µs earlier. A *TXOP* lets the winner send several frames back to back, separated by SIFS, for up to the limit. If two queues in the same station count down to zero in the same slot, the higher AC gets the medium and the lower one behaves as if it had collided: an *internal collision*.

A frame's category comes from its *user priority* (UP, 0 to 7), carried in the QoS Control field and taken from the IP header's DSCP. UP 1 and 2 map to background, 0 and 3 to best effort, 4 and 5 to video, and 6 and 7 to voice. A trap here is the mapping of Expedited Forwarding (DSCP 46): the older practice of copying the top three bits of the DSCP gives UP 5, which is video; the current recommendation (RFC 8325) maps it to UP 6, which is voice.

### Aggregation and the block acknowledgement

The per-frame overhead seen in the efficiency example of [§6.4](#s6-4){.ref} is independent of the data rate, so the solution is to send more data per access. *Aggregation* does it at two levels. An *A-MSDU* packs several packets into one MAC frame with one header and one FCS, saving header bytes. An *A-MPDU* packs several complete MAC frames, each with its own header, delimiter and FCS, into one PHY transmission.

| | A-MSDU | A-MPDU |
|---|---|---|
| What is aggregated | packets (MSDUs) in one MPDU | MAC frames (MPDUs) in one PPDU |
| Headers and FCS | one header, one FCS | one per subframe, plus a 4-byte delimiter |
| Maximum size | 3,839 or 7,935 B (HT), 11,454 B (VHT, HE) | 64 KB (HT), 1 MB (VHT), 4 MB (HE) |
| On a bit error | the whole A-MSDU is lost | only the damaged subframe is repeated |
| Acknowledgement | one ACK or part of a Block Ack | one Block Ack for all subframes |

An A-MPDU survives a noisy channel better, because each subframe has its own FCS and only the failed ones are retransmitted; an A-MSDU has a single FCS and is lost entirely. Practical systems put A-MSDUs inside an A-MPDU.

Acknowledging each subframe separately would defeat the purpose. The *Block Ack* is a single reply, with a bitmap of which subframes in a window arrived: 64 frames in 802.11n and ac, 256 in 802.11ax, 1,024 in 802.11be. The agreement is set up with an ADDBA action frame exchange for each traffic class, after which the sender transmits the aggregate and the receiver replies with a Block Ack, and the sender re-sends only the missing sequence numbers.

::: example
**Airtime saved by aggregation.** A station sends 64 packets of 1,500 B at 600 Mb/s PHY rate, with the overheads of [§6.4](#s6-4){.ref}: DIFS 34 µs, average backoff 67.5 µs, SIFS 16 µs, preamble 50 µs, ACK or Block Ack about 32 µs.

1. Separately: each packet needs 34 + 67.5 + (50 + 20.5) + 16 + 32 ≈ 220 µs, so 64 packets take 64 × 220 = 14.1 ms, a goodput of 64 × 12,000 bits ÷ 14.1 ms ≈ 55 Mb/s.
2. As one A-MPDU: contention 34 + 67.5, preamble 50, data 64 × 20.5 = 1,312 plus about 3 µs of delimiters, SIFS 16 and one Block Ack 32: total ≈ 1.5 ms.
3. Goodput = 768,000 bits ÷ 1.5 ms ≈ 507 Mb/s.

[Result: about 9 times the goodput from the same PHY rate. At high rates, aggregation is mandatory, not an option.]{.result}
:::

### Power save

A phone cannot keep its radio on all the time. A station tells the AP that it is about to sleep by setting the Power Management bit in the Frame Control of a frame (often a Null frame), and from then on the AP buffers its frames. The AP lists the stations with waiting frames in the *traffic indication map* (TIM) element of each beacon, one bit per association ID. A sleeping station wakes for selected beacons, in multiples of its listen interval, reads the TIM, and if its bit is set it fetches the data: in legacy mode it sends a PS-Poll and the AP replies with one frame, setting the More Data bit if more remain; with *U-APSD*, designed for voice, the station's own uplink frame triggers the delivery of all buffered frames at once. Broadcast and multicast frames are buffered until the *delivery TIM* (DTIM) beacon, which occurs every DTIM-period beacons; with a beacon interval of 102.4 ms and a DTIM period of 3, a station wishing to receive multicast wakes every 307 ms, and a longer period saves power at the cost of multicast latency.

*Target wake time* (TWT), introduced in 802.11ax and described in [§6.9](#s6-9){.ref}, replaces this polling with a negotiated schedule: the station and AP agree on when the station will wake, so that it need not listen to every beacon, and many stations can be told to wake at different times, reducing contention.

::: lens
[QUALCOMM · BROADCOM · CISCO]{.co}

"Explain EDCA access categories and how voice gets priority", "what are TIM and DTIM", and "A-MPDU versus A-MSDU" are reported for WLAN firmware roles. A strong answer gives AIFSN and CW for voice and best effort, computes the average first wait, and says priority is statistical. For aggregation, explain the single-FCS risk of A-MSDU; for power save, trace a buffered frame from the TIM bit to the PS-Poll. Follow-ups: how much latency a DTIM period of 3 adds, and what the TXOP limit prevents.
:::

::: check
1. Which AC does DSCP 46 reach under RFC 8325? [^c68-1]
2. Why does a single bit error cost more in an A-MSDU? [^c68-2]
3. What does a beacon with a set TIM bit mean for a sleeping station? [^c68-3]
:::

[^c68-1]: User priority 6, hence AC_VO.
[^c68-2]: One FCS covers the whole A-MSDU, so the whole aggregate must be repeated; in an A-MPDU only the damaged subframe is.
[^c68-3]: The AP has buffered unicast frames for it; it should stay awake and retrieve them (PS-Poll or U-APSD trigger).

:::
