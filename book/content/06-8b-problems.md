::: {.p6}

::: pack
## Problem Set, continued: Wi-Fi 6 and 7, power, roaming and cellular {#ps6b}

::: problems

::: q
### Q6.22 What is BSS colouring?
[QUALCOMM · CISCO · TECH-1 · ■■□ · T]{.meta}

[30-second answer: every HE frame carries a 6-bit colour identifying its BSS. A station that hears a frame of another colour below the OBSS packet-detect threshold may ignore it and transmit, with reduced power; this is spatial reuse and it cuts needless deferral between overlapping cells.]{.short}

**Answer.** Without colours, any frame above the −82 dBm preamble-detect level makes the medium busy, even if it comes from a distant neighbour on the same channel. With colours, the station sees that the frame is inter-BSS; if its level is below the threshold (the default −82 dBm, adjustable up to −62 dBm), it treats the medium as idle and may transmit at a power lowered by the amount that the threshold was raised. Two NAVs (intra-BSS and basic) keep own-cell reservations intact ([§6.9](#s6-9){.ref}). **Follow-ups.** Colour collisions between neighbouring APs, and the AP's ability to change colour; why gains are largest in dense, same-channel deployments. **Mistakes.** Saying that colouring avoids interference; it only avoids unnecessary deferral.
:::

::: q
### Q6.23 What is TWT and which devices benefit?
[QUALCOMM · BROADCOM · TECH-1 · ■■□ · T]{.meta}

[30-second answer: target wake time is a negotiated schedule in which the AP and a station agree when the station will wake; it sleeps in between without listening to beacons. Battery devices (IoT sensors, phones, wearables) benefit, and contention falls because stations wake in separate slots.]{.short}

**Answer.** The agreement fixes the first wake time, the interval (mantissa × 2^exponent µs) and the minimum wake duration; it may be individual or, in broadcast TWT, announced by the AP for a group, and it may be trigger-enabled so that the AP polls the station inside its window. Compared with legacy power save, the station avoids waking for every beacon or DTIM, and the AP knows when to buffer. Wi-Fi 7 adds restricted TWT to protect latency-sensitive flows ([§6.8](#s6-8){.ref}, [§6.9](#s6-9){.ref}). **Follow-ups.** The firmware challenge of honouring many agreements at once; clock drift between AP and station. **Mistakes.** Describing TWT as a faster beacon.
:::

::: q
### Q6.24 List four Wi-Fi 7 features and the benefit of each.
[QUALCOMM · CISCO · BROADCOM · TECH-1 · ■■□ · T]{.meta}

[30-second answer: 320 MHz channels (double the bandwidth, in 6 GHz); 4096-QAM (20% more bits per symbol at high SNR); multi-link operation (aggregate rate, lower latency and better reliability across bands); multi-RU and preamble puncturing (use of fragmented or partly occupied spectrum).]{.short}

**Answer.** The factors 2 (320 MHz), 1.2 (4096-QAM) and 2 (16 streams) take the peak from 9.6 to 46.1 Gb/s. Realistically a 2-stream 320 MHz client has 5.8 Gb/s. 4096-QAM needs an even better SNR than 1024-QAM (and a low error-vector magnitude in the transmitter), so it benefits clients near the AP only. Restricted TWT and multi-AP coordination target latency ([§6.9](#s6-9){.ref}). **Follow-ups.** The PHY rate for 2 streams (2 × 2,882 Mb/s); which of the features need new hardware in the AP. **Mistakes.** Quoting 46 Gb/s as a user-visible rate.
:::

::: q
### Q6.25 Explain MLO modes (STR, NSTR, EMLSR) and a firmware challenge each introduces.
[QUALCOMM · BROADCOM · TECH-2 · ■■■ · T]{.meta}

[30-second answer: in STR a multi-link device transmits on one link while receiving on another; in NSTR the links are too close, so it cannot; in EMLSR a single full radio listens on several links and switches to the one that receives an initial control frame. Challenges: independent per-link state (STR), aligned end times (NSTR), switching delay (EMLSR).]{.short}

**Answer.** STR needs radio isolation, and its firmware must keep a separate EDCA, NAV and backoff state for each link yet share one sequence-number space and a block-ack scoreboard. NSTR must align PPDU ends on both links, otherwise transmitting on one deafens the other and the acknowledgements are lost. EMLSR saves power and cost; the AP must know the transition delay and not send to the station until it has switched, and frames during the switch are lost. Common tasks: TID-to-link mapping, link recovery and the single MLD address ([§6.9](#s6-9){.ref}). **Follow-ups.** Where in the stack the link choice is made; effect on rate adaptation. **Mistakes.** Treating MLO as band steering: the same flow uses several links at once.
:::

::: q
### Q6.26 What is A-MPDU versus A-MSDU? Which survives better on a noisy channel, and why?
[QUALCOMM · BROADCOM · TECH-1 · ■□□ · T]{.meta}

[30-second answer: an A-MSDU puts several packets in one MAC frame with one header and one FCS; an A-MPDU sends several complete MAC frames, each with its own FCS, in one PHY burst. The A-MPDU survives better: a bit error costs only its subframe, while an A-MSDU is lost entirely.]{.short}

**Answer.** An A-MSDU saves header bytes but its single FCS makes it all-or-nothing; its maximum size is 3,839 or 7,935 bytes for HT and 11,454 for VHT and HE. An A-MPDU subframe has a 4-byte delimiter and is padded to 4 bytes, but is acknowledged selectively by Block Ack and can reach 64 KB (HT), 1 MB (VHT) or 4 MB (HE). Systems use both: A-MSDUs inside an A-MPDU ([§6.8](#s6-8){.ref}). **Follow-ups.** The efficiency effect of aggregation (the 9× goodput example); the latency cost of waiting to fill an aggregate. **Mistakes.** Reversing the two, or saying that A-MSDU needs a Block Ack per packet.
:::

::: q
### Q6.27 What is Block Ack?
[QUALCOMM · BROADCOM · TECH-1 · ■■□ · T]{.meta}

[30-second answer: a single acknowledgement frame with a bitmap that reports which MPDUs of a window arrived, so that an aggregate needs one reply and only the missing MPDUs are resent.]{.short}

**Answer.** The agreement is set up per traffic identifier by ADDBA request and response action frames, fixing the window size (64 in 802.11n and ac, 256 in 802.11ax, 1,024 in 802.11be) and the starting sequence number. The sender transmits an A-MPDU, the receiver replies with a Block Ack after SIFS (or the sender solicits it with a Block Ack Request), and the sender slides the window past acknowledged frames. The receiver reorders frames, so that the upper layers still see order ([§6.8](#s6-8){.ref}). **Follow-ups.** Immediate versus delayed; the multi-STA Block Ack in OFDMA; the reorder-buffer memory on a chip. **Mistakes.** Saying that Block Ack replaces the ACK for single frames.
:::

::: q
### Q6.28 Explain EDCA access categories and how voice gets priority.
[QUALCOMM · CISCO · TECH-1 · ■■□ · T]{.meta}

[30-second answer: four queues (voice, video, best effort, background), each with its own AIFSN, CWmin and CWmax and TXOP limit; voice has AIFSN 2 and CW 3 to 7, best effort AIFSN 3 and CW 15 to 1023. A shorter wait and a smaller window make voice win more often, and its TXOP allows a short burst.]{.short}

**Answer.** The average first wait is SIFS + AIFSN × 9 µs + (CWmin/2) × 9 µs: 47.5 µs for voice against 110.5 µs for best effort. Priority is therefore statistical, not guaranteed; if two queues in one station expire together, the higher one wins (internal collision). The user priority is carried in the QoS Control field and derived from the DSCP; EF should map to UP 6 (voice) under RFC 8325, not to UP 5 ([§6.8](#s6-8){.ref}). **Follow-ups.** Why high-priority traffic can still starve others (admission control, TXOP limits); WMM certification. **Mistakes.** Quoting wired-network strict priority.
:::

::: q
### Q6.29 What are TIM and DTIM? How does a sleeping station get buffered unicast frames?
[QUALCOMM · BROADCOM · TECH-1 · ■■□ · T]{.meta}

[30-second answer: the TIM in each beacon has one bit per association ID marking stations with buffered unicast frames; every DTIM-period-th beacon is a DTIM, after which buffered broadcast and multicast are sent. A sleeping station wakes for the beacon, sees its bit, and fetches its frames with a PS-Poll (or a U-APSD trigger).]{.short}

**Answer.** The station tells the AP that it will sleep by setting the power-management bit; the AP buffers. After a PS-Poll the AP sends one frame, with More Data set if more are queued; with U-APSD, one uplink frame releases all. With a 102.4 ms beacon and DTIM period 3 a station that wants multicast wakes every 307 ms ([§6.8](#s6-8){.ref}). **Follow-ups.** Listen interval; the latency and power trade-off of a long DTIM; why phones set a DTIM of 1 to 3. **Mistakes.** Thinking that the DTIM concerns unicast.
:::

::: q
### Q6.30 How does 802.11r speed up roaming? What do 802.11k and 802.11v add?
[CISCO · JUNIPER · QUALCOMM · TECH-1 · ■■□ · T]{.meta}

[30-second answer: 802.11r (fast transition) derives the keys for the next AP in advance from a key hierarchy (PMK-R0, PMK-R1), so a roam costs two authentication and two reassociation frames, about 20 ms, with no 802.1X re-authentication. 802.11k gives the client a neighbour list; 802.11v lets the AP suggest a better AP.]{.short}

**Answer.** The client decides; k and v only help. k shortens the scan by naming the candidate channels; v moves sticky clients and balances load with BSS transition requests; r removes the long part, the key exchange ([§6.10](#s6-10){.ref}). **Follow-ups.** Over-the-air versus over-the-DS; opportunistic key caching as the vendor alternative; clients that fail when 802.11r is enabled. **Mistakes.** Believing that the AP can force a client to roam.
:::

::: q
### Q6.31 Users complain that voice calls drop while walking down a corridor. How do you troubleshoot?
[CISCO · JUNIPER · TECH-2 · ■■■ · T]{.meta}

[30-second answer: reproduce on a walk test with a client log and a capture; find whether the call drops at the roam (gap, sticky client, key exchange time), or from poor signal (hole, high retries), or from the channel (interference, DFS evacuation); fix coverage, power, minimum rate, 802.11k/v/r and QoS in that order, and verify again.]{.short}

**Approach.** Follow the method of [Pillar 11](#ch11){.ref}: scope, measure, hypothesise, change one thing, verify. **Answer.** (i) Scope: one floor, one phone model or all? Time-dependent? (ii) Walk with the phone, record RSSI and SNR, the BSSID and the time of each roam, and capture on the channel. (iii) Read the evidence. A long gap at the roam suggests 802.1X re-authentication or no 802.11r; a late roam at −80 dBm suggests a sticky client (raise the minimum RSSI, enable 802.11v); a hole between APs shows as falling SNR and rising retries; an AP that disappears on a DFS channel points to radar events; one-way audio points to an AP that is louder than the client (reduce transmit power). (iv) Check that voice is marked UP 6 end to end, and that rates below 12 Mb/s are disabled. **Follow-ups.** Target values: −67 dBm, SNR 25 dB, retries under 10%, roam under 50 ms. **Mistakes.** Changing power and channels before looking at the roam events.
:::

::: q
### Q6.32 Convert 200 mW to dBm. What does −3 dB mean?
[QUALCOMM · NOKIA · TECH-1 · ■□□ · T]{.meta}

[30-second answer: 200 mW is 23 dBm (100 mW is 20 dBm and doubling adds 3 dB). −3 dB is a factor of one half in power.]{.short}

**Answer.** dBm = 10 log₁₀(mW), so 10 log₁₀(200) = 23.0. A decibel is a ratio: +3 dB is ×2, +10 dB is ×10, −3 dB is ×0.5, −10 dB is ×0.1; a −3 dB loss halves the power, so 23 dBm becomes 20 dBm. In amplitude (voltage) terms the factors are the square roots ([§6.1](#s6-1){.ref}). **Follow-ups.** Add 17 dBm and 20 dBm (that is 50 mW + 100 mW = 150 mW = 21.8 dBm); the FSPL change for twice the distance (+6 dB). **Mistakes.** Adding dBm values, or reading −3 dB as "minus three watts".
:::

::: q
### Q6.33 Why are only channels 1, 6 and 11 recommended in 2.4 GHz?
[CISCO · TECH-1 · ■■□ · T]{.meta}

[30-second answer: the 2.4 GHz channels are 5 MHz apart but each is about 20 MHz wide, so two channels are free of overlap only if their numbers differ by 5 or more; 1, 6 and 11 are the only three such channels in the 1 to 11 range that all regions allow.]{.short}

**Answer.** Co-channel neighbours hear each other's preambles and share airtime by CSMA/CA; partly overlapping neighbours do not decode each other and merely raise noise, so frames are corrupted and retried. Hence one plans three non-overlapping channels and repeats them. In some regions the plan 1, 5, 9, 13 is used for OFDM-only networks, accepting a little overlap; the general recommendation stays 1, 6, 11. 40 MHz channels in 2.4 GHz leave room for no more than one cell ([§6.10](#s6-10){.ref}). **Follow-ups.** Why 5 GHz relieves this; how the interference from microwave ovens and Bluetooth enters. **Mistakes.** Choosing channels 3 and 8 "to avoid the crowd".
:::

::: q
### Q6.34 Throughput is low even though RSSI is −50 dBm. List causes.
[CISCO · QUALCOMM · TECH-2 · ■■■ · T]{.meta}

[30-second answer: RSSI measures only the signal; throughput also depends on SNR (noise and interference), contention (airtime shared with neighbours and slow clients), retries, the negotiated MCS, channel width and streams, legacy-client protection, and the wired side.]{.short}

**Answer.** Check, in order: (i) noise floor and SNR: a −50 dBm signal with a −60 dBm interferer is a 10 dB SNR, which gives a low MCS; (ii) channel utilisation and co-channel APs (each shares the airtime); (iii) retry rate and the MCS in `iw station dump`; (iv) slow legacy stations (an 802.11b client at 1 Mb/s occupies the channel for ages, and protection modes add overhead); (v) a width mismatch (80 MHz on a congested band, 40 MHz in 2.4 GHz) or a single-stream client; (vi) power-save or TXOP behaviour; (vii) the backhaul or the server. **Follow-ups.** The expected goodput (about 60% of the PHY rate at best). **Mistakes.** Treating RSSI as quality.
:::

::: q
### Q6.35 What is rate adaptation? Describe one algorithm.
[QUALCOMM · BROADCOM · TECH-2 · ■■■ · T]{.meta}

[30-second answer: the transmitter does not know which MCS the channel supports, so it picks one per frame from the outcome of earlier frames. Minstrel keeps, for every rate, a smoothed delivery probability, estimates throughput as rate × probability, uses the best, and probes other rates for about 10% of frames.]{.short}

**Approach.** Rates are an ordered set; a high rate has more throughput if it succeeds and none if it fails, so the algorithm explores and exploits. **Answer.** Each interval (100 ms in Minstrel) the success statistics update the probability with an exponentially weighted average (75% old, 25% new); the retry chain falls back to lower rates when the first choice fails, and a probe is only sent at a rate not obviously worse. Firmware versions add SNR feedback and aggregation length.

```c
#include <stdlib.h>
#define NR 8
struct rate { int kbps; double p; };

int pick(const struct rate *t,
         unsigned sent)
{
  if (sent % 10 == 9)   /* probe */
    return rand() % NR;
  int best = 0;
  for (int i = 1; i < NR; i++)
    if (t[i].kbps * t[i].p >
        t[best].kbps * t[best].p)
      best = i;
  return best;
}

void update(struct rate *r,
            int ok, int tries)
{
  double s = (double)ok / tries;
  r->p = 0.75 * r->p + 0.25 * s;
}
```

**Follow-ups.** Why not use the highest rate always (the loss collapses throughput); the effect of aggregation (a loss costs a whole burst); how OFDMA and MU-MIMO complicate it (per-RU rates). **Mistakes.** Judging a rate on one frame, or never probing upwards.
:::

::: q
### Q6.36 In firmware, how would you schedule RUs across 20 stations with mixed QoS? State the inputs, the constraints and a greedy heuristic.
[QUALCOMM · TECH-2 · ■■■ · T]{.meta}

[30-second answer: inputs are each station's queue per access category, its rate per tone and its age; constraints are the RU tree of the channel (26 to 996 tones), the PPDU length limit and the number of users per PPDU. Greedy: sort by priority, then queue; give each the smallest RU that drains its queue, keeping a minimum RU for those not yet served; carry unserved stations over with a growing age.]{.short}

**Approach.** Pick the metric, then the allocation, then fairness. **Answer.** With 80 MHz there are 37 26-tone RUs, so 20 stations all fit; the problem is how big each RU is. Time is bounded by the TXOP, so a station needs queue ÷ bpt tones, where bpt is the number of bytes one tone carries in the PPDU duration at the station's MCS, rounded up to an allowed size (26, 52, 106, 242, 484, 996). Reserving 26 tones per later station prevents a large voice or video queue from starving the rest.

```c
struct sta { int id, prio, bytes, bpt; };

static int cmp(const void *a,
               const void *b)
{
  const struct sta *x = a, *y = b;
  if (x->prio != y->prio)
    return y->prio - x->prio;
  return y->bytes - x->bytes;
}

void schedule(struct sta *s, int n,
              int *ru)
{
  static const int sz[] =
    {26, 52, 106, 242, 484, 996};
  int left = 996;  /* 80 MHz */
  qsort(s, n, sizeof *s, cmp);
  for (int i = 0; i < n; i++) {
    ru[i] = 0;
    if (left < 26) continue;
    /* keep 26 per later STA */
    int room = left - 26 * (n-i-1);
    if (room < 26) room = 26;
    int need = s[i].bytes/s[i].bpt + 1;
    int k = 0;
    while (k < 5 && sz[k] < need) k++;
    while (k > 0 && sz[k] > room) k--;
    ru[i] = sz[k];
    left -= sz[k];
  }
}
```

The function returns sizes; a second step places them in the RU tree (largest first, so that no 26-tone gap is stranded) and chooses an MCS per RU from the station's recent SNR. **Complexity.** O(n log n). **Follow-ups.** Uplink needs buffer-status reports; deadline-aware (earliest-deadline-first) scheduling for voice; deficit counters for long-term fairness; when to prefer MU-MIMO or a single wide RU. **Mistakes.** Ignoring the trigger and acknowledgement overhead, which makes tiny RUs wasteful.
:::

::: q
### Q6.37 Describe the LTE architecture (MME, S-GW, P-GW, HSS).
[NOKIA · QUALCOMM · TECH-1 · ■■□ · T]{.meta}

[30-second answer: the UE connects over the radio to an eNodeB; the eNB talks to the MME for signalling (S1-MME) and to the S-GW for user data (S1-U). The MME handles attach, security and mobility using subscriber data from the HSS (S6a); the S-GW anchors user data during handover; the P-GW assigns the IP address and connects to the Internet (SGi). PCRF supplies policy.]{.short}

**Answer.** Control and user planes are separate: MME and HSS carry signalling, S-GW and P-GW carry packets in GTP-U tunnels (S1-U, S5). The user's session is an EPS bearer: the default one has QCI 9, and a dedicated bearer (QCI 1 for voice) adds guaranteed rate ([§6.12](#s6-12){.ref}). **Follow-ups.** X2 handover between eNBs; tracking areas and paging; EPS-AKA. **Mistakes.** Putting the IP address allocation in the MME.
:::

::: q
### Q6.38 What are AMF, SMF and UPF in 5G? What is a service-based architecture?
[NOKIA · QUALCOMM · TECH-1 · ■■□ · T]{.meta}

[30-second answer: the AMF handles registration, NAS security and mobility; the SMF manages PDU sessions and allocates the IP address and programs the UPF; the UPF forwards user packets. In a service-based architecture the control functions expose services to each other over HTTP/2 and register in a repository (NRF), instead of using fixed point-to-point interfaces.]{.short}

**Answer.** The 4G MME was split: its mobility half is the AMF and its session half the SMF, and the user-plane parts of S-GW and P-GW became the UPF, controlled over N4 (PFCP). The service-based design allows each function to scale and update on its own, as cloud software does; discovery is by the NRF. Other functions: AUSF and UDM (authentication and subscriber data), PCF (policy), NSSF (slice selection) ([§6.12](#s6-12){.ref}). **Follow-ups.** Why CUPS lets the UPF sit near the edge; what a slice is. **Mistakes.** Saying that the AMF is a renamed MME.
:::

::: q
### Q6.39 Walk through the UE attach or registration procedure and PDU session establishment.
[QUALCOMM · NOKIA · TECH-2 · ■■■ · S]{.meta}

[30-second answer: RRC connection; Attach (LTE) or Registration (5G) request to the MME or AMF; authentication with the HSS or AUSF/UDM; security mode; accept; then session set-up: in LTE the default bearer through S-GW and P-GW, in 5G a PDU session through the SMF and UPF. At the end the UE has an IP address and a GTP-U tunnel to the core.]{.short}

**Answer for LTE.** (1) Random access and RRC connection setup; the attach request with a PDN connectivity request travels to the MME in the S1AP initial UE message. (2) The MME fetches the authentication vector from the HSS over S6a and runs EPS-AKA with the UE. (3) NAS security mode command. (4) The MME updates the HSS with its location and receives the subscription. (5) The MME sends a Create Session Request to the S-GW and then the P-GW (GTP-C), which allocates the UE's IP address and the default bearer (QCI 9). (6) The MME sends an initial context setup request to the eNB, carrying the attach accept; the eNB reconfigures the radio bearer. (7) The UE replies attach complete; the MME gives the eNB's tunnel endpoint to the S-GW (Modify Bearer), and downlink data can flow. **5G.** The steps are the ten of [§6.12](#s6-12){.ref}: registration with SUCI, 5G-AKA through AUSF and UDM, security, accept with 5G-GUTI, then the PDU session through the SMF, an N4 session at the UPF and an N3 tunnel to the gNB. **Follow-ups.** NAS against AS; what changes at re-registration or handover; why SUCI hides the permanent identity. **Mistakes.** Forgetting that the core, not the eNB, authenticates.
:::

::: q
### Q6.40 What is GTP-U? Why tunnel user data between gNB and UPF?
[NOKIA · QUALCOMM · TECH-1 · ■■□ · T]{.meta}

[30-second answer: the GPRS tunnelling protocol, user plane, carries the user's IP packets inside UDP (port 2152), with an 8-byte header whose TEID identifies the bearer or session. Tunnelling hides the UE's address from the transport network and keeps it constant while the UE moves.]{.short}

**Answer.** The UE's IP address belongs to the core (the P-GW or UPF), not to the topology of the radio network. A tunnel from the base station to the anchor lets the transport network route on outer addresses only, so a handover merely changes the tunnel end; it also gives per-session accounting and QoS marking. Overhead is 20 + 8 + 8 = 36 bytes with IPv4, which reduces the effective MTU of the UE to avoid fragmentation ([§6.12](#s6-12){.ref}). **Follow-ups.** The TEID allocation (each end assigns the ID its peer must use); GTP-C on port 2123; the similarity to VXLAN. **Mistakes.** Thinking that GTP encrypts: it does not, and IPsec or the radio security does.
:::

::: q
### Q6.41 Compare 5G NR numerology with LTE. What does µ = 3 mean for slot duration?
[QUALCOMM · NOKIA · TECH-2 · ■■■ · T]{.meta}

[30-second answer: LTE has a fixed 15 kHz subcarrier spacing and 1 ms subframe; NR's spacing is 15 × 2^µ kHz, and the slot of 14 symbols lasts 1 ms ÷ 2^µ. For µ = 3 the spacing is 120 kHz and the slot is 125 µs.]{.short}

**Answer.** Wider spacing means shorter symbols (8.33 µs useful for 120 kHz), so lower latency and more tolerance of the phase noise and Doppler at mmWave, at the cost of a shorter cyclic prefix and so less delay spread tolerated. There are 8 slots in a 1 ms subframe at µ = 3 and 80 in a 10 ms frame. Different numerologies can coexist on one carrier, for example eMBB and URLLC services ([§6.12](#s6-12){.ref}). **Follow-ups.** The PRB width (12 × the spacing: 1.44 MHz at 120 kHz); the maximum carrier bandwidth (100 MHz in FR1, 400 MHz in FR2); mini-slots. **Mistakes.** Taking the slot as 7 symbols (LTE) or as a fixed 1 ms.
:::

::: q
### Q6.42 In Linux, what are cfg80211, mac80211 and nl80211?
[QUALCOMM · BROADCOM · TECH-1 · ■□□ · T]{.meta}

[30-second answer: nl80211 is the netlink interface through which user space (iw, wpa_supplicant, hostapd) configures wireless devices; cfg80211 is the kernel configuration layer, with regulatory rules and scanning; mac80211 is the SoftMAC framework that implements the MAC state machine, rate control and aggregation for drivers that need it.]{.short}

**Answer.** A command such as `iw dev wlan0 scan` goes through nl80211 to cfg80211, which validates it and calls the driver (directly for FullMAC chips like brcmfmac, or through mac80211 for SoftMAC drivers like ath9k and, in part, ath11k). The firmware on modern chips does the time-critical work; the host and firmware exchange WMI commands and events ([§6.11](#s6-11){.ref}). **Follow-ups.** FullMAC versus SoftMAC; monitor mode and radiotap; `mac80211_hwsim` for simulation. **Mistakes.** Describing mac80211 as a driver, or placing the regulatory database in user space only.
:::

:::

**Questions solved in other pillars.** The generic 802.1X and EAP exchange behind Q6.16 is in [Pillar 9](#ch9){.ref}; the troubleshooting method behind Q6.31 is [Pillar 11](#ch11){.ref}; the interrupt, DMA and receive-path questions that WLAN firmware interviews add are solved in [Pillar 7](#ch7){.ref}.
:::

:::
