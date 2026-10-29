::: {.p6}

## [6.11]{.sec}The Linux and firmware view [Should · ■■□]{.tag} {#s6-11}

Everything so far happens in a few microseconds: the acknowledgement of a frame must start 16 µs after the frame ends, the backoff counts in 9 µs slots, and a block-ack bitmap must be built before the sender's timeout. A general-purpose kernel, whose interrupt latency is of the order of hundreds of microseconds, cannot do this. Hence a Wi-Fi chip contains a small processor with its own *firmware*, and the part of the MAC that is time-critical lives there, while the host runs the policy. This division is the subject of Qualcomm and Broadcom WLAN roles, which combine this chapter with the interrupts, DMA rings and bit manipulation of [Pillar 7](#ch7){.ref}.

### The Linux wireless stack

Linux splits the work into layers, each with a defined interface (Figure 6.16).

<figure>
<svg viewBox="0 0 480 252" width="480"><defs><marker id="i8" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="a8" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><rect class="box" x="14" y="12" width="262" height="24" /><text class="lbl" x="145" y="27" text-anchor="middle" >wpa_supplicant, hostapd, iw, NetworkManager</text><line class="ln" x1="145" y1="36" x2="145" y2="46" marker-end="url(#i8)"/><rect class="box" x="14" y="46" width="262" height="24" /><text class="lbl" x="145" y="61" text-anchor="middle" >nl80211 (generic netlink)</text><line class="ln" x1="145" y1="70" x2="145" y2="80" marker-end="url(#i8)"/><rect class="box" x="14" y="80" width="262" height="24" /><text class="lbl" x="145" y="95" text-anchor="middle" >cfg80211: config API, scan, regulatory</text><line class="ln" x1="145" y1="104" x2="145" y2="114" marker-end="url(#i8)"/><rect class="box" x="14" y="114" width="262" height="24" /><text class="lbl" x="145" y="129" text-anchor="middle" >mac80211: SoftMAC (rate control, aggregation, PS)</text><line class="ln" x1="145" y1="138" x2="145" y2="148" marker-end="url(#i8)"/><rect class="box" x="14" y="148" width="262" height="24" /><text class="lbl" x="145" y="163" text-anchor="middle" >driver: ath11k / ath12k / iwlwifi / mt76</text><line class="ln" x1="145" y1="172" x2="145" y2="182" marker-end="url(#i8)"/><rect class="box" x="14" y="182" width="262" height="24" /><text class="lbl" x="145" y="197" text-anchor="middle" >bus: PCIe / SDIO / USB</text><line class="ln" x1="145" y1="206" x2="145" y2="216" marker-end="url(#i8)"/><rect class="fill" x="14" y="216" width="262" height="24" /><text class="lbl" x="145" y="231" text-anchor="middle" >firmware on the chip (WMI commands and events)</text><rect class="box" x="330" y="126" width="136" height="24" /><text class="lbl" x="398" y="141" text-anchor="middle" >brcmfmac (FullMAC)</text><path class="acc" d="M276,92 L398,92 L398,126" marker-end="url(#a8)"/><text class="sm" x="404" y="88" text-anchor="start" >bypasses mac80211</text><path class="ln dash" d="M398,150 L398,228 L278,228" marker-end="url(#i8)"/><text class="sm" x="404" y="188" text-anchor="start" >MAC runs in firmware</text></svg>
<figcaption><b>Figure 6.16</b> The Linux wireless stack, from user space down to the radio, with the FullMAC bypass.</figcaption>
</figure>

| Layer | Role |
|--------------------------|------------------------------------------------------------|
| `wpa_supplicant`, `hostapd`, `iw`, NetworkManager | user-space policy: supplicant and authenticator state machines, the key handshakes, configuration |
| **nl80211** | the user-space interface: a generic-netlink family through which user space issues commands (scan, connect, set channel, set type) and receives events |
| **cfg80211** | the kernel's configuration layer: validates requests, holds the regulatory domain (which channels and powers are allowed), runs scans and connection management |
| **mac80211** | a software MAC framework ("SoftMAC") used by drivers whose hardware leaves the MAC to the host: the state machine, rate control (Minstrel), aggregation sessions, power-save handling, mesh |
| Driver | `ath9k`, `ath10k`, `ath11k`, `ath12k` (Qualcomm), `iwlwifi` (Intel), `mt76` (MediaTek); programs the chip and moves frames through DMA rings |
| Bus and firmware | PCIe, SDIO or USB, to the firmware that runs on the chip |

The first question is who does the MAC work. In a *SoftMAC* design, the driver implements a thin interface, and mac80211 does most of the MAC, with only timing-critical parts in hardware (older `ath9k`). In a *FullMAC* design the chip's firmware does nearly all of it, and the driver (`brcmfmac`, for Broadcom FullMAC chips) talks to cfg80211 directly, bypassing mac80211. Modern high-rate chips are in between: `ath11k` and `ath12k` register with mac80211 but the firmware does the scheduling, aggregation, retries, rate control and OFDMA, because those decisions must follow each frame by microseconds.

The host and firmware exchange messages through shared-memory rings. Host commands go to the firmware as *WMI* messages (configuration, scan requests, key installation); the firmware answers with events (scan results, connection state, TX completion). The data path uses separate descriptor rings: the host posts empty receive buffers, the firmware writes received frames into them by DMA and raises an interrupt, which a NAPI poll loop services ([§7.12](#s7-12){.ref}); for transmission the host queues frames and the firmware aggregates, schedules and sends them, then reports completion. The generic firmware concepts, ISRs, bottom halves and DMA, are in [§7.13](#s7-13){.ref}.

**What the firmware does.** The microsecond tasks are ACK and block-ack generation, backoff and EDCA, aggregation and retry, rate control, OFDMA and MU-MIMO scheduling, beacon generation and the TIM bitmap, hardware encryption, power-save handling and the calibration of the radio. It also performs *offloads* that let the host sleep: answering ARP and neighbour requests, keeping connections alive, filtering packets, scanning for a better AP, and waking the host on a magic packet or a pattern (Wake on WLAN).

**Rate adaptation.** The transmitter does not know the best MCS; it infers it from acknowledgements. Minstrel, the algorithm in mac80211, keeps for each rate an exponentially weighted success probability and estimates throughput as that probability multiplied by the rate; it sends most frames at the best estimate and about 10% as probes at other rates, and falls back along a retry chain of lower rates when a frame fails. Firmware implementations use richer inputs, such as per-frame SNR feedback.

::: lab
`LAB 6.11 · 20 MIN` Inspect a wireless interface. The output is typical and abridged; yours will differ.

```
$ iw dev wlan0 link
Connected to 02:11:22:33:44:aa (on wlan0)
        SSID: IITLab
        freq: 5180
        signal: -58 dBm
        rx bitrate: 866.7 MBit/s VHT-MCS 9 80MHz short GI VHT-NSS 2
        tx bitrate: 780.0 MBit/s VHT-MCS 8 80MHz short GI VHT-NSS 2
$ iw dev wlan0 station dump | grep -E 'signal|retries|failed'
        signal:         -58 dBm
        tx retries:     1042
        tx failed:      3
$ iw phy phy0 info | grep -E 'monitor|HE Iftypes|VHT Capabilities'
```

**What you should notice:** the bit rate is the formula of [§6.2](#s6-2){.ref} applied in reverse: VHT-MCS 9 on 80 MHz with 2 streams and the short guard interval is 2 × 234 × 8 × 5/6 ÷ 3.6 µs = 866.7 Mb/s. The two directions differ because each side runs its own rate adaptation. A high count of `tx retries` against a good signal points to interference or hidden nodes, not to range. The third command tells whether the card supports monitor mode and HE.
:::

### Monitor mode

A normal ("managed") interface hands the host only the frames addressed to it, converted to Ethernet. To see the frames of [§6.6](#s6-6){.ref} one needs *monitor mode*, in which the radio on one channel passes up every 802.11 frame it can decode, management and control frames included, with a *radiotap* header carrying the signal strength, channel and rate. The interface cannot associate while in this mode.

```
$ sudo ip link set wlan0 down
$ sudo iw dev wlan0 set type monitor
$ sudo ip link set wlan0 up
$ sudo iw dev wlan0 set channel 36 80MHz
$ sudo tcpdump -i wlan0 -y IEEE802_11_RADIO -w cap.pcap
```

Wireshark reads the capture and offers the filters in [§6.6](#s6-6){.ref} ([§8.8](#s8-8){.ref}); to decrypt the data frames it needs the passphrase and the capture of the station's 4-way handshake. Only networks one owns or is authorised to test may be captured. Without a monitor-capable adapter, the kernel module `mac80211_hwsim` creates virtual radios (`modprobe mac80211_hwsim radios=3`) on which `hostapd` and `wpa_supplicant` can run a complete WPA2 or WPA3 session inside network namespaces, with a capture interface `hwsim0` that shows every frame.

::: trap
*Claim:* "Monitor mode is the same as promiscuous mode." *Why it is wrong:* promiscuous mode on a managed interface only lifts the filter on destination addresses of frames that the station is already allowed to receive, after decryption and conversion to Ethernet, so other stations' 802.11 frames never reach it. *Correct statement:* monitor mode delivers raw 802.11 frames of all stations on the channel, with radiotap; promiscuous mode does not.
:::

::: lens
[QUALCOMM · BROADCOM]{.co}

WLAN firmware roles at Qualcomm and Broadcom join this section with the C and kernel material of Pillar 7. Reported questions are "what are cfg80211, mac80211 and nl80211", "explain rate adaptation" and, at the low level, bit manipulation, memory management and interrupt handling. A strong answer places each layer on the diagram, explains why the MAC cannot live on the host (the 16 µs SIFS), and names what the firmware offloads. Follow-ups: the difference between FullMAC and SoftMAC, how a host command reaches the firmware, and how a frame travels from the air to a socket.
:::

::: check
1. What do cfg80211 and mac80211 each do? [^c611-1]
2. Why is the ACK generated in hardware or firmware? [^c611-2]
3. Which command puts a card on channel 36 in monitor mode? [^c611-3]
:::

[^c611-1]: cfg80211 holds configuration, regulatory rules and scanning and is the kernel side of nl80211; mac80211 is the SoftMAC implementation used by drivers that leave the MAC to the host.
[^c611-2]: It must start 16 µs after the frame ends, which a general-purpose kernel's interrupt latency cannot guarantee.
[^c611-3]: `iw dev wlan0 set type monitor`, then, with the interface up, `iw dev wlan0 set channel 36`.

## [6.12]{.sec}Cellular from LTE to 5G [Should · ■■□]{.tag} {#s6-12}

A cellular network has the same two halves in every generation. The *radio access network* (RAN), a set of base stations, serves the *user equipment* (UE) over a licensed radio channel; the *core network* authenticates the subscriber, assigns an IP address, keeps track of the location, and connects to the Internet. Two planes cross both halves: the *control plane* (signalling about attachment, mobility and sessions) and the *user plane* (the IP packets). The UE and the core exchange *non-access stratum* (NAS) messages, which the base station relays without reading; the UE and base station exchange *access stratum* (AS) messages, the radio resource control (RRC), which set up radio bearers. Unlike Wi-Fi, the base station schedules every transmission, uplink as well as downlink, so there is no contention among UEs.

### LTE: the evolved packet system

The LTE architecture, the *evolved packet system* (EPS), has a RAN made of one kind of node and a core, the *evolved packet core* (EPC), made of a few boxes (Figure 6.17).

<figure>
<svg viewBox="0 0 480 160" width="480"><defs><marker id="i9" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="a9" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><rect class="box" x="8" y="56" width="36" height="24" /><text class="lbl" x="26.0" y="71" text-anchor="middle" >UE</text><rect class="box" x="76" y="56" width="46" height="24" /><text class="lbl" x="99.0" y="71" text-anchor="middle" >eNB</text><rect class="box" x="180" y="12" width="50" height="24" /><text class="lbl" x="205.0" y="27" text-anchor="middle" >MME</text><rect class="box" x="290" y="12" width="50" height="24" /><text class="lbl" x="315.0" y="27" text-anchor="middle" >HSS</text><rect class="box" x="180" y="100" width="56" height="24" /><text class="lbl" x="208.0" y="115" text-anchor="middle" >S-GW</text><rect class="box" x="280" y="100" width="56" height="24" /><text class="lbl" x="308.0" y="115" text-anchor="middle" >P-GW</text><rect class="box" x="380" y="100" width="70" height="24" /><text class="lbl" x="415.0" y="115" text-anchor="middle" >Internet</text><rect class="box" x="380" y="12" width="60" height="24" /><text class="lbl" x="410.0" y="27" text-anchor="middle" >PCRF</text><line class="lg" x1="44" y1="68" x2="76" y2="68" stroke-dasharray="2 2"/><text class="sm" x="60" y="62" text-anchor="middle" >Uu</text><line class="ln" x1="122" y1="62" x2="180" y2="30" stroke-dasharray="4 3"/><text class="sm" x="138" y="40" text-anchor="middle" >S1-MME</text><line class="ln" x1="230" y1="24" x2="290" y2="24" stroke-dasharray="4 3"/><text class="sm" x="260" y="20" text-anchor="middle" >S6a</text><line class="acc" x1="122" y1="74" x2="180" y2="108" /><text class="acct" x="138" y="98" text-anchor="middle" >S1-U</text><line class="acc" x1="236" y1="112" x2="280" y2="112" /><text class="acct" x="258" y="106" text-anchor="middle" >S5</text><line class="acc" x1="336" y1="112" x2="380" y2="112" /><text class="acct" x="358" y="106" text-anchor="middle" >SGi</text><line class="ln" x1="208" y1="36" x2="208" y2="100" stroke-dasharray="4 3"/><text class="sm" x="220" y="70" text-anchor="start" >S11</text><line class="ln" x1="308" y1="100" x2="308" y2="90" stroke-dasharray="4 3"/><line class="ln" x1="308" y1="90" x2="410" y2="90" stroke-dasharray="4 3"/><line class="ln" x1="410" y1="90" x2="410" y2="36" stroke-dasharray="4 3"/><text class="sm" x="350" y="86" text-anchor="middle" >Gx</text><text class="sm" x="10" y="150" text-anchor="start" >Dashed: control plane.  Solid accent: user plane (GTP-U tunnels on S1-U and S5).</text></svg>
<figcaption><b>Figure 6.17</b> The LTE Evolved Packet System: MME and HSS handle signalling, while S-GW and P-GW carry the user plane.</figcaption>
</figure>

| Node | Plane | Function |
|------------------------|--------|------------------------------------------------------------|
| eNodeB (eNB) | both | the base station: radio scheduling, header compression, ciphering, handover decisions; connects to the MME (S1-MME) and the S-GW (S1-U) |
| MME (mobility management entity) | control | NAS signalling: attach, authentication, tracking-area updates, paging, bearer set-up; selects the S-GW and P-GW |
| S-GW (serving gateway) | user | the anchor for the user plane while the UE moves between eNBs |
| P-GW (PDN gateway) | user | assigns the UE's IP address, applies policy and charging, and links to the Internet (SGi) |
| HSS (home subscriber server) | control | the subscriber database and the keys; used in authentication (S6a) |
| PCRF | control | policy and charging rules for the bearers (Gx) |

The user's traffic is carried in *bearers*, logical channels with a defined treatment. At attach the network creates a *default EPS bearer*, with best-effort quality (QCI 9) and the UE's IP address, which remains for as long as the UE is attached. A *dedicated bearer* adds a guaranteed bit rate and a low delay for a service such as voice over LTE (QCI 1). An EPS bearer is a chain of three pieces: a radio bearer between UE and eNB, an S1 bearer between eNB and S-GW and an S5 bearer between S-GW and P-GW.

**GTP-U.** Between the nodes the user's IP packets are carried inside the *GPRS tunnelling protocol, user plane*, a UDP-based tunnel (port 2152). Each packet gets an outer IP header, a UDP header and an 8-byte GTP header whose *tunnel endpoint identifier* (TEID) tells the receiver which bearer the packet belongs to. The reason for tunnelling is mobility: the UE's IP address is anchored in the P-GW, and when the UE moves from one eNB to another only the tunnel's far end changes, while the UE's address stays the same and the routers in between need not know the UE exists. The overhead is 20 + 8 + 8 = 36 bytes with IPv4 (more with extension headers), an instance of the encapsulation theme that returns with VXLAN in [Pillar 5](#ch5){.ref}.

### 5G: the new core and radio

5G's *standalone* (SA) architecture replaces the EPC by the *5G core* (5GC) and the eNB by the *gNodeB* (gNB). The design changes in two ways. The control and user planes are fully separated: all user-plane forwarding is in one function, the *UPF*, and the rest is control. And the control-plane functions form a *service-based architecture* (SBA) in which each function offers services to the others over an HTTP/2 interface with JSON bodies and registers itself with a repository, the NRF; this is how cloud-native software is built, and it lets operators scale and replace the functions independently (Figure 6.18).

<figure>
<svg viewBox="0 0 480 198" width="480"><rect class="fill" x="8" y="10" width="464" height="28" /><text class="sm" x="240" y="22" text-anchor="middle" >service-based bus (HTTP/2 JSON): Namf, Nsmf, Nausf, Nudm, Npcf, Nnrf, Nnssf, Nnef</text><rect class="box" x="14.0" y="50" width="50" height="22" /><text class="lbl" x="39.0" y="64" text-anchor="middle" >AMF</text><line class="ln" x1="39.0" y1="38" x2="39.0" y2="50" /><rect class="box" x="71.5" y="50" width="50" height="22" /><text class="lbl" x="96.5" y="64" text-anchor="middle" >SMF</text><line class="ln" x1="96.5" y1="38" x2="96.5" y2="50" /><rect class="box" x="129.0" y="50" width="50" height="22" /><text class="lbl" x="154.0" y="64" text-anchor="middle" >AUSF</text><line class="ln" x1="154.0" y1="38" x2="154.0" y2="50" /><rect class="box" x="186.5" y="50" width="50" height="22" /><text class="lbl" x="211.5" y="64" text-anchor="middle" >UDM</text><line class="ln" x1="211.5" y1="38" x2="211.5" y2="50" /><rect class="box" x="244.0" y="50" width="50" height="22" /><text class="lbl" x="269.0" y="64" text-anchor="middle" >PCF</text><line class="ln" x1="269.0" y1="38" x2="269.0" y2="50" /><rect class="box" x="301.5" y="50" width="50" height="22" /><text class="lbl" x="326.5" y="64" text-anchor="middle" >NRF</text><line class="ln" x1="326.5" y1="38" x2="326.5" y2="50" /><rect class="box" x="359.0" y="50" width="50" height="22" /><text class="lbl" x="384.0" y="64" text-anchor="middle" >NSSF</text><line class="ln" x1="384.0" y1="38" x2="384.0" y2="50" /><rect class="box" x="416.5" y="50" width="50" height="22" /><text class="lbl" x="441.5" y="64" text-anchor="middle" >NEF</text><line class="ln" x1="441.5" y1="38" x2="441.5" y2="50" /><rect class="box" x="14" y="120" width="50" height="24" /><text class="lbl" x="39" y="135" text-anchor="middle" >gNB</text><rect class="box" x="14" y="168" width="50" height="22" /><text class="lbl" x="39" y="182" text-anchor="middle" >UE</text><rect class="box" x="130" y="120" width="56" height="24" /><text class="lbl" x="158" y="135" text-anchor="middle" >UPF</text><rect class="box" x="250" y="120" width="70" height="24" /><text class="lbl" x="285" y="135" text-anchor="middle" >Data network</text><path class="ln dash" d="M30,120 L30,86 L39,86 L39,72"/><text class="sm" x="46" y="100" text-anchor="start" >N2 (NGAP)</text><line class="lg" x1="39" y1="168" x2="39" y2="144" stroke-dasharray="2 2"/><text class="sm" x="46" y="160" text-anchor="start" >Uu / N1 (NAS to AMF)</text><line class="acc" x1="64" y1="132" x2="130" y2="132" /><text class="acct" x="97" y="126" text-anchor="middle" >N3</text><line class="acc" x1="186" y1="132" x2="250" y2="132" /><text class="acct" x="218" y="126" text-anchor="middle" >N6</text><path class="ln dash" d="M158,120 L158,90 L88,90 L88,72"/><text class="sm" x="168" y="108" text-anchor="start" >N4 (PFCP) from SMF</text><text class="sm" x="380" y="150" text-anchor="middle" >Solid: user plane</text><text class="sm" x="380" y="162" text-anchor="middle" >Dashed: control plane</text></svg>
<figcaption><b>Figure 6.18</b> The 5G core: control-plane functions on a service bus, and a single user-plane function, the UPF.</figcaption>
</figure>

| 5G function | What it does | Closest LTE counterpart |
|------------------------|--------------------------------------------|--------------------------|
| AMF (access and mobility management) | registration, NAS security, mobility, paging; the UE's single point of contact | MME (the mobility half) |
| SMF (session management) | allocates the UE's IP address, selects and programs the UPF over N4 | MME (session half) with the control parts of S-GW and P-GW |
| UPF (user-plane function) | forwards packets, applies QoS and usage rules, connects to the data network (N6) | S-GW-U and P-GW-U |
| AUSF and UDM (with UDR) | authentication server and subscriber data | HSS |
| PCF | policy | PCRF |
| NRF, NSSF, NEF | service registry and discovery; slice selection; exposure of capabilities to third parties | none |

Control-plane interfaces get names such as N1 (UE to AMF, NAS), N2 (gNB to AMF, NGAP), N3 (gNB to UPF, GTP-U), N4 (SMF to UPF, PFCP), N6 (UPF to the data network) and N11 (AMF to SMF). The 5G user plane carries IP in *PDU sessions*, and each session is divided into *QoS flows* that carry a QoS flow identifier (QFI), which the SMF maps to radio bearers; the default flow has the best-effort profile, 5QI 9. An operator can offer *network slices*, separate logical networks identified by a *single network slice selection assistance information* (S-NSSAI), on the same infrastructure.

::: example
**Registration and PDU session in ten steps (5G SA).**

1. The UE finds a cell, performs random access and opens an RRC connection with the gNB; its first NAS message rides along.
2. The NAS *Registration Request* carries the SUCI, the subscriber identity concealed with the home network's public key so that the permanent identity is never sent in clear. The gNB forwards it to an AMF over N2.
3. The AMF asks the AUSF, which asks the UDM, to authenticate the UE (5G-AKA): the network sends a random challenge and an authentication token, and the UE, using the key in its SIM, checks the token (so that it knows the network is genuine) and returns a response.
4. The AMF and UE agree on NAS ciphering and integrity (Security Mode Command); the gNB does the same for the radio (AS security).
5. The AMF sends the *Registration Accept* with a temporary identity (5G-GUTI) and the permitted slices; the UE answers Registration Complete.
6. The UE sends a *PDU Session Establishment Request* (data network name and slice); the AMF forwards it to an SMF.
7. The SMF obtains the subscription from the UDM and policy from the PCF, selects a UPF, and opens an N4 session with it (PFCP rules).
8. The UPF's N3 tunnel endpoint (an address and a TEID) is passed through the AMF to the gNB, which configures the radio bearer and returns its own TEID, so both ends of the N3 GTP-U tunnel are known.
9. The UE receives the *PDU Session Establishment Accept* with its IP address and the QoS rules.
10. User data now flows UE, gNB, N3 tunnel, UPF, N6, on the default QoS flow.

[Result: control-plane steps 1 to 9 involve AMF, AUSF/UDM, SMF and PCF; the user plane is touched only by gNB and UPF. The LTE attach has the same shape with the MME, HSS, S-GW and P-GW and ends with the default bearer (QCI 9).]{.result}
:::

### The radio: numerology

LTE used a fixed subcarrier spacing of 15 kHz, with OFDMA in the downlink and SC-FDMA (a power-efficient variant of OFDM) in the uplink, a slot of 0.5 ms and a subframe (the scheduling unit) of 1 ms. 5G NR keeps OFDM but makes the spacing a parameter, the *numerology* µ: the spacing is 15 × 2^µ kHz, and the slot, which always has 14 OFDM symbols, shortens in proportion.

| µ | Subcarrier spacing | Slot duration | Slots per 1 ms subframe | Typical use |
|----|--------------|--------------|----------------|------------------------------|
| 0 | 15 kHz | 1 ms | 1 | sub-1 GHz coverage, as in LTE |
| 1 | 30 kHz | 0.5 ms | 2 | mid-band (3.5 GHz), the main 5G band |
| 2 | 60 kHz | 0.25 ms | 4 | mid-band, mmWave |
| 3 | 120 kHz | 0.125 ms | 8 | mmWave (24 to 52 GHz) |

For µ = 3 the slot is 1 ms ÷ 2³ = 125 µs, and the useful symbol is 1/120 kHz = 8.33 µs. A wider spacing means shorter symbols, hence lower latency and more tolerance of the phase noise and Doppler of high frequencies, at the cost of a shorter cyclic prefix. The two frequency ranges differ in the channel width: FR1 (410 MHz to 7.125 GHz) carriers go up to 100 MHz, and FR2 (24.25 to 52.6 GHz) up to 400 MHz, compared with LTE's 20 MHz.

| | LTE | 5G NR |
|---|---|---|
| Waveform | OFDMA downlink, SC-FDMA uplink | CP-OFDM both ways (optionally DFT-s-OFDM in uplink) |
| Subcarrier spacing | 15 kHz | 15 × 2^µ kHz |
| Carrier bandwidth | up to 20 MHz | up to 100 MHz (FR1), 400 MHz (FR2) |
| Core | EPC | 5GC, service-based |
| Slicing | no | yes (S-NSSAI) |
| Latency targets | tens of ms | URLLC down to about 1 ms |

Two more points complete the picture. In *non-standalone* (NSA) deployment (option 3x) the 5G radio is added to an LTE network, with the LTE eNB as anchor and the EPC as core; *standalone* (option 2) uses the gNB with the 5GC. A *handover* moves the UE between base stations: with X2 in LTE or Xn in 5G the eNBs or gNBs coordinate directly, and with S1 or N2 the core is involved. Finally, operators split a gNB into a *central unit* (CU), a *distributed unit* (DU) and a *radio unit* (RU), the O-RAN architecture, so that the real-time radio functions can sit at the antenna and the rest in a data centre; the CU and DU talk over the F1 interface.

::: trap
*Claim:* "The AMF is the MME in 5G", or "5G is just faster LTE." *Why it is wrong:* the MME's session functions moved to the SMF, so the AMF handles access and mobility only; and 5G changes the core (service-based, split user plane), the radio (flexible numerology, mmWave) and the service model (slices). *Correct statement:* the AMF is the mobility half of the MME; session management and user-plane control belong to the SMF.
:::

::: lens
[NOKIA · QUALCOMM · CISCO]{.co}

Nokia (RAN and core software) and Qualcomm (modem) examine this section in depth; Cisco (private 5G) and Microsoft (operator cloud) ask for the architecture only. A Qualcomm candidate was asked for the UE network attach procedure. A strong answer names the nodes and interfaces, goes through registration in order, distinguishes NAS from AS and control from user plane, and says what the GTP-U tunnel is for. Follow-ups: the LTE counterpart of each 5G function, µ = 3 slot length, and NSA against SA.
:::

::: check
1. Which 5G function replaces the S-GW and P-GW user-plane parts? [^c612-1]
2. What is the slot duration for µ = 1? [^c612-2]
3. What is carried over N3, and by which protocol? [^c612-3]
:::

[^c612-1]: The UPF.
[^c612-2]: 1 ms ÷ 2 = 0.5 ms, with a 30 kHz subcarrier spacing.
[^c612-3]: The user's IP packets between gNB and UPF, in GTP-U tunnels (UDP port 2152).

:::
