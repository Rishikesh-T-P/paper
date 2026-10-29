::: {.p11}

### Case 13 · Traffic works one way through the firewalls [Should · ■■■]{.tag} {#c11-13}

[L3 · L4 · CISCO · JUNIPER · NOKIA · GOOGLE · AMAZON]{.where}

**Prompt.** "After adding a second internet link, some users' sessions to the cloud application break; it looks random."

<figure>
<svg viewBox="0 0 480 168" width="480">
<line class="ln" x1="30" y1="70" x2="95" y2="70"/>
<line class="ln" x1="95" y1="70" x2="180" y2="32"/>
<line class="ln" x1="180" y1="32" x2="260" y2="32"/>
<line class="ln" x1="260" y1="32" x2="345" y2="32"/>
<line class="ln" x1="345" y1="32" x2="445" y2="70"/>
<line class="acc dash" x1="95" y1="70" x2="180" y2="110"/>
<line class="acc dash" x1="180" y1="110" x2="260" y2="110"/>
<line class="acc dash" x1="260" y1="110" x2="345" y2="110"/>
<line class="acc dash" x1="345" y1="110" x2="445" y2="70"/>
<rect class="box" x="15" y="60" width="30" height="20" rx="1"/><path class="ln" d="M22,84 L38,84"/><rect class="fill" x="19" y="64" width="22" height="11"/>
<text class="lbl" x="30" y="96" text-anchor="middle">Users</text>
<rect class="box" x="73" y="59" width="44" height="22" rx="2"/><path class="ln" d="M82,67 L108,67 M104,64 L108,67 L104,70 M108,74 L82,74 M86,71 L82,74 L86,77"/>
<text class="lbl" x="95" y="94" text-anchor="middle">Core</text>
<text class="sm" x="95" y="103" text-anchor="middle">ECMP</text>
<rect class="box" x="160" y="20" width="40" height="24" rx="1"/><path class="ln" d="M160,32 L200,32 M173,20 L173,32 M187,20 L187,32 M180,32 L180,44 M166,32 L166,44 M194,32 L194,44"/>
<text class="lbl" x="180" y="57" text-anchor="middle">FW-A</text>
<rect class="box" x="160" y="98" width="40" height="24" rx="1"/><path class="ln" d="M160,110 L200,110 M173,98 L173,110 M187,98 L187,110 M180,110 L180,122 M166,110 L166,122 M194,110 L194,122"/><rect class="acc" x="157" y="95" width="46" height="30" rx="3"/>
<text class="lbl" x="180" y="135" text-anchor="middle">FW-B</text>
<text class="sm" x="180" y="144" text-anchor="middle">no state</text>
<circle class="box" cx="260" cy="32" r="13"/><path class="ln" d="M253,32 L267,32 M260,25 L260,39 M255,27 L265,37 M255,37 L265,27"/>
<text class="lbl" x="260" y="58" text-anchor="middle">Edge-A</text>
<circle class="box" cx="260" cy="110" r="13"/><path class="ln" d="M253,110 L267,110 M260,103 L260,117 M255,105 L265,115 M255,115 L265,105"/>
<text class="lbl" x="260" y="136" text-anchor="middle">Edge-B</text>
<path class="box" d="M317,43 C305,43 305,27 319,27 C319,13 343,9 351,21 C363,15 379,27 371,35 C383,37 379,43 369,43 Z"/>
<text class="lbl" x="345" y="58" text-anchor="middle">ISP-A</text>
<path class="box" d="M317,121 C305,121 305,105 319,105 C319,91 343,87 351,99 C363,93 379,105 371,113 C383,115 379,121 369,121 Z"/>
<text class="lbl" x="345" y="136" text-anchor="middle">ISP-B</text>
<rect class="box" x="431" y="55" width="28" height="30" rx="1"/><path class="ln" d="M431,65 L459,65 M431,75 L459,75"/><circle class="accf" cx="453" cy="60" r="1.2" style="fill:#1A1D23"/>
<text class="lbl" x="445" y="98" text-anchor="middle">Cloud app</text>
<text class="sm acct" x="300" y="160" text-anchor="middle">SYN-ACK returns through ISP-B (accent)</text>
</svg>
<figcaption><b>Figure 11.21</b> Case 13. The request leaves through ISP-A and FW-A; the reply returns through ISP-B and FW-B, which has no state for it.</figcaption>
</figure>

| We ask | The interviewer answers |
|----------------------|--------------------------------------------|
| Which users? | About half, varying by session |
| Which protocols? | TCP mostly; pings are fine |
| What do the firewall logs say? | FW-B: "TCP packet without SYN, no connection" |
| What changed? | A second ISP, with ECMP to both firewalls |

**Hypotheses, ranked.** (1) asymmetric routing through two independent stateful firewalls; (2) a NAT pool mismatch; (3) MTU on the new link.

| Layer | Command | Decisive output | Inference |
|----|-----------------|----------------------------|--------------------------|
| L3 | `traceroute` from a user, and from the cloud server (looking glass) | The two paths use different ISPs | The path is asymmetric |
| L4 | FW-B log | `%ASA-6-106015: Deny TCP (no connection) from 203.0.113.50/443 to 198.51.100.77/51514 flags SYN ACK` | A SYN-ACK arrives for a session FW-B never saw |
| L4 | `show conn` on FW-A | The session, with its SYN | FW-A holds the state; FW-B does not |
| L3 | ICMP test | Passes | Echo replies are permitted without a session |


**Root cause.** The return path crosses a different stateful firewall that has no session state, so it discards the reply. Remote networks choose their own return path by BGP policy, so Campus Net cannot force symmetry with outbound routing alone ([§4.7](#s4-7){.ref}).

**Fix.** Make the paths symmetric: source-NAT per ISP so replies return to the address of the firewall that sent the request; or policy routing; or an HA pair with state synchronisation or clustering. Do not run ECMP across independent stateful devices.

**Verify.** Sessions are stable and the "no connection" drop counter falls to zero.

**Prevent.** A design rule that a stateful device must see both directions, and failover tests of each path.

| The interviewer asks | A strong answer |
|-------------------|--------------------------------------|
| What is TCP state bypass? | A firewall setting that skips state checks for chosen flows; it removes the symptom and some protection. |
| How does ECMP choose a path? | By hashing the five-tuple, so one flow stays on one path. |
| Would strict uRPF help? | No, it would also drop asymmetric traffic. |

**Variant.** *NAT pool exhaustion.* New connections fail while old ones work; `show ip nat statistics` shows misses. Enlarge the pool or use PAT.

::: lens
[GOOGLE · AMAZON · CISCO]{.co}

A design question disguised as a fault. A strong answer ends with a rule (stateful devices must see both directions) and offers two fixes with their trade-offs. Expect: "what would you do if you could not change the ISPs?"
:::

### Case 14 · Website slow for some users only [Should · ■■■]{.tag} {#c11-14}

[L1 · L2 · L3 · GOOGLE · MICROSOFT · AMAZON · ARISTA]{.where}

**Prompt.** "About a quarter of users say the internal portal is slow; the others are fine. Server CPU is low."

<figure>
<svg viewBox="0 0 480 190" width="480">
<line class="ln" x1="30" y1="85" x2="100" y2="85"/>
<line class="ln" x1="100" y1="85" x2="260" y2="18"/>
<line class="acc" x1="100" y1="85" x2="260" y2="62"/>
<line class="ln" x1="100" y1="85" x2="260" y2="106"/>
<line class="ln" x1="100" y1="85" x2="260" y2="150"/>
<line class="ln" x1="260" y1="18" x2="420" y2="85"/>
<line class="ln" x1="260" y1="62" x2="420" y2="85"/>
<line class="ln" x1="260" y1="106" x2="420" y2="85"/>
<line class="ln" x1="260" y1="150" x2="420" y2="85"/>
<text class="sm" x="136" y="76" text-anchor="middle">Et49</text>
<rect class="box" x="15" y="75" width="30" height="20" rx="1"/><path class="ln" d="M22,99 L38,99"/><rect class="fill" x="19" y="79" width="22" height="11"/>
<text class="lbl" x="30" y="111" text-anchor="middle">Users</text>
<rect class="box" x="78" y="74" width="44" height="22" rx="2"/><path class="ln" d="M87,82 L113,82 M109,79 L113,82 L109,85 M113,89 L87,89 M91,86 L87,89 L91,92"/>
<text class="lbl" x="100" y="109" text-anchor="middle">Leaf1</text>
<rect class="box" x="238" y="7" width="44" height="22" rx="2"/><path class="ln" d="M247,15 L273,15 M269,12 L273,15 L269,18 M273,22 L247,22 M251,19 L247,22 L251,25"/>
<text class="lbl" x="260" y="42" text-anchor="middle">Spine1</text>
<rect class="box" x="238" y="51" width="44" height="22" rx="2"/><path class="ln" d="M247,59 L273,59 M269,56 L273,59 L269,62 M273,66 L247,66 M251,63 L247,66 L251,69"/><rect class="acc" x="235" y="48" width="50" height="28" rx="3"/>
<text class="lbl" x="260" y="86" text-anchor="middle">Spine2</text>
<rect class="box" x="238" y="95" width="44" height="22" rx="2"/><path class="ln" d="M247,103 L273,103 M269,100 L273,103 L269,106 M273,110 L247,110 M251,107 L247,110 L251,113"/>
<text class="lbl" x="260" y="130" text-anchor="middle">Spine3</text>
<rect class="box" x="238" y="139" width="44" height="22" rx="2"/><path class="ln" d="M247,147 L273,147 M269,144 L273,147 L269,150 M273,154 L247,154 M251,151 L247,154 L251,157"/>
<text class="lbl" x="260" y="174" text-anchor="middle">Spine4</text>
<rect class="box" x="398" y="74" width="44" height="22" rx="2"/><path class="ln" d="M407,82 L433,82 M429,79 L433,82 L429,85 M433,89 L407,89 M411,86 L407,89 L411,92"/>
<text class="lbl" x="420" y="109" text-anchor="middle">Leaf2</text>
</svg>
<figcaption><b>Figure 11.22</b> Case 14. Flows from Leaf1 are hashed over four spine uplinks; one has a failing optic.</figcaption>
</figure>

| We ask | The interviewer answers |
|----------------------|--------------------------------------------|
| Which users? | No pattern by floor |
| Consistent per user? | Yes, the same users every time |
| Measured how? | `curl` shows a long time to first byte, with retransmissions |
| What is the topology? | A leaf-spine fabric with four equal-cost uplinks |

**Hypotheses, ranked.** (1) one bad ECMP or LAG member; (2) an optic or duplex error; (3) one overloaded pool member behind a load balancer; (4) DNS returning a far replica.

| Layer | Command | Decisive output | Inference |
|----|-----------------|----------------------------|--------------------------|
| L7 | `curl -w` with the timing variables (name lookup, connect, first byte), slow vs fast client | DNS and connect equal; transfer slow | Not DNS or setup; loss in the transfer |
| L3 | `mtr -rwzbc 100 portal` from a slow client | Loss from the leaf-to-spine hop, persisting to the end | Real forwarding loss on one path |
| L1 | `show interfaces counters errors` on Leaf1 | `Et49  FCS 18342` rising | CRC errors on one uplink |
| L1 | `show interfaces transceiver` | `Et49  Rx power -14.2 dBm` | The optic is weak |


**Root cause.** A faulty optic on one fabric uplink loses packets for exactly those flows whose five-tuple hashes to it. Hashing is consistent per flow, which explains "the same users, always" and the absence of a pattern by floor.

**Fix.** Drain or shut the member so flows rehash, then clean or replace the optic and check the fibre.

**Verify.** CRC deltas are zero, light levels normal, and the users' `curl` timings recover.

**Prevent.** Telemetry alerts on CRC rate and optical power thresholds ([Pillar 10](#ch10){.ref}), and an automated drain.

| The interviewer asks | A strong answer |
|-------------------|--------------------------------------|
| Which fields feed the ECMP hash? | Source and destination address, protocol and ports. |
| Why is per-packet balancing avoided? | It reorders packets and triggers duplicate ACKs. |
| What is a gray failure? | A partial fault that health checks miss; end-to-end probes over every path find it. |

**Variant.** A port channel member suspended for a mismatched configuration (flag `s` in `show etherchannel summary`) gives the same "some flows" pattern.

::: lens
[GOOGLE · MICROSOFT · ARISTA]{.co}

A gray-failure question. The marks are for linking "same users every time" to flow hashing, and for proposing telemetry on every member. Expect: "how would you find this across 500 leaves?"
:::

### Case 15 · VPN tunnel up, but no traffic [Should · ■■□]{.tag} {#c11-15}

[L3 · SECURITY · CISCO · JUNIPER · NOKIA]{.where}

**Prompt.** "The new site-to-site VPN to Hyderabad shows Phase 1 up, but users cannot reach HQ."

<figure>
<svg viewBox="0 0 480 125" width="480">
<line class="acc dash" x1="100" y1="45" x2="380" y2="45"/>
<line class="ln" x1="100" y1="45" x2="240" y2="45"/>
<line class="ln" x1="240" y1="45" x2="380" y2="45"/>
<circle class="box" cx="100" cy="45" r="13"/><path class="ln" d="M93,45 L107,45 M100,38 L100,52 M95,40 L105,50 M95,50 L105,40"/>
<text class="lbl" x="100" y="71" text-anchor="middle">HQ (BR1)</text>
<text class="sm" x="100" y="80" text-anchor="middle">10.10.0.0/16</text>
<path class="box" d="M212,56 C200,56 200,40 214,40 C214,26 238,22 246,34 C258,28 274,40 266,48 C278,50 274,56 264,56 Z"/>
<text class="lbl" x="240" y="71" text-anchor="middle">Internet</text>
<circle class="box" cx="380" cy="45" r="13"/><path class="ln" d="M373,45 L387,45 M380,38 L380,52 M375,40 L385,50 M375,50 L385,40"/><circle class="acc" cx="380" cy="45" r="16"/>
<text class="lbl" x="380" y="71" text-anchor="middle">Hyderabad</text>
<text class="sm" x="380" y="80" text-anchor="middle">10.20.0.0/16</text>
<text class="sm" x="100" y="100" text-anchor="middle">selector 10.20.0.0/16</text>
<text class="sm acct" x="380" y="100" text-anchor="middle">selector 10.20.1.0/24</text>
<text class="sm acct" x="100" y="111" text-anchor="middle">PAT before encryption</text>
</svg>
<figcaption><b>Figure 11.23</b> Case 15. The two sides disagree on the traffic selectors, and HQ translates VPN-bound traffic before encrypting it.</figcaption>
</figure>

| We ask | The interviewer answers |
|----------------------|--------------------------------------------|
| IKE version? | IKEv2 |
| Is the child SA up? | "Not sure" |
| What do the logs say? | `TS_UNACCEPTABLE` |
| Any NAT? | HQ does PAT for internet access |

**Hypotheses, ranked.** (1) traffic-selector or proxy-ID mismatch; (2) transform-set or PFS mismatch; (3) missing NAT exemption; (4) a missing route to the tunnel, if route-based.

| Layer | Command | Decisive output | Inference |
|----|-----------------|----------------------------|--------------------------|
| L3 | `show crypto ikev2 sa` | `Status: READY` | Phase 1 is healthy |
| L3 | `show crypto ipsec sa peer 203.0.113.9` | no child SA; debug: `TS_UNACCEPTABLE` | The selectors do not match |
| L3 | after mirroring the selectors: the same command | `#pkts encaps: 412 ... #pkts decaps: 0` | HQ sends; nothing returns |
| L3 | `show ip nat translations` | `icmp 192.0.2.2:5 10.10.4.7:5 10.20.1.9:5 10.20.1.9:5` | HQ translates traffic before encryption |


**Root cause.** Two faults: HQ defines 10.20.0.0/16 and the branch 10.20.1.0/24, so negotiation of the child SA fails; and the NAT rule translates VPN-bound traffic, so it no longer matches the selector.

**Fix.** Mirror the selectors on both peers; add a NAT exemption (a `deny` for 10.10.0.0/16 to 10.20.0.0/16 at the top of the NAT access list).

**Verify.** Both sides show encapsulation and decapsulation counts rising; users reach HQ applications.

**Prevent.** Generate both peers from one definition, and use the checklist of [§9.7](#s9-7){.ref}.

| The interviewer asks | A strong answer |
|-------------------|--------------------------------------|
| What causes Phase 1 to fail? | A wrong pre-shared key, mismatched proposals, or UDP 500 and 4500 blocked. |
| How do policy-based and route-based VPNs differ in debugging? | The first by comparing selectors, the second by checking the route into the tunnel. |
| What is NAT-T? | ESP encapsulated in UDP 4500 when a NAT is detected between the peers. |

**Variant.** The tunnel works for small packets only: the MTU problem of [Case 5](#c11-5){.ref} applies as well.

### Case 16 · Linux service: refused, then timeout [Should · ■□□]{.tag} {#c11-16}

[L4 · L7 · AMAZON · GOOGLE · MICROSOFT · ARISTA]{.where}

**Prompt.** "Our new API on port 8080 works with `curl` on the VM itself, but not from other machines."

<figure>
<svg viewBox="0 0 480 110" width="480">
<line class="ln" x1="40" y1="40" x2="150" y2="40"/>
<line class="ln" x1="150" y1="40" x2="265" y2="40"/>
<line class="ln" x1="265" y1="40" x2="390" y2="40"/>
<rect class="box" x="25" y="30" width="30" height="20" rx="1"/><path class="ln" d="M32,54 L48,54"/><rect class="fill" x="29" y="34" width="22" height="11"/>
<text class="lbl" x="40" y="66" text-anchor="middle">Client</text>
<text class="sm" x="40" y="75" text-anchor="middle">10.0.1.5</text>
<rect class="box" x="130" y="28" width="40" height="24" rx="1"/><path class="ln" d="M130,40 L170,40 M143,28 L143,40 M157,28 L157,40 M150,40 L150,52 M136,40 L136,52 M164,40 L164,52"/>
<text class="lbl" x="150" y="65" text-anchor="middle">Cloud SG</text>
<text class="sm" x="150" y="74" text-anchor="middle">timeout?</text>
<rect class="box" x="245" y="28" width="40" height="24" rx="1"/><path class="ln" d="M245,40 L285,40 M258,28 L258,40 M272,28 L272,40 M265,40 L265,52 M251,40 L251,52 M279,40 L279,52"/>
<text class="lbl" x="265" y="65" text-anchor="middle">nftables</text>
<text class="sm" x="265" y="74" text-anchor="middle">timeout?</text>
<rect class="box" x="376" y="25" width="28" height="30" rx="1"/><path class="ln" d="M376,35 L404,35 M376,45 L404,45"/><circle class="accf" cx="398" cy="30" r="1.2" style="fill:#1A1D23"/><rect class="acc" x="373" y="22" width="34" height="36" rx="3"/>
<text class="lbl" x="390" y="68" text-anchor="middle">App</text>
<text class="sm" x="390" y="77" text-anchor="middle">127.0.0.1:8080</text>
<text class="sm" x="240" y="100" text-anchor="middle">three barriers, three different symptoms</text>
</svg>
<figcaption><b>Figure 11.24</b> Case 16. Three barriers in a row, each with its own symptom; the loopback bind is the first.</figcaption>
</figure>

| We ask | The interviewer answers |
|----------------------|--------------------------------------------|
| What error does the client see? | "Connection refused" once; a timeout after the admin "opened" the firewall |
| Cloud or on premises? | Cloud, with a security group |
| Any change? | A new deployment |

**Hypotheses, ranked.** (1) the application binds to loopback; (2) the host firewall; (3) the cloud security group; (4) a wrong port.

| Layer | Command | Decisive output | Inference |
|----|-----------------|----------------------------|--------------------------|
| L4 | `ss -tlnp` on the VM, line for 8080 | `LISTEN 0 128 127.0.0.1:8080 ... users:(("python3",pid=2211,fd=3))` | Loopback only; the kernel answers other hosts with a RST |
| L4 | after rebinding to `0.0.0.0`: client `curl` | `curl: (28) Connection timed out after 5001 milliseconds` | A drop, not a refusal |
| L4 | `nft list ruleset` or `ufw status` | no rule for 8080; `policy drop` | The host firewall drops it; allow it |
| L4 | `tcpdump -ni eth0 port 8080` on the VM | nothing arrives | The packet dies outside the VM: the security group |


**Root cause.** Three layers in a stack: the loopback bind (refusal), the host firewall (timeout), and the cloud security group (timeout, with the packet never arriving). Placing the capture on the VM is what separates the last two.

**Fix.** Bind to the interface address, allow 8080 from the client CIDR in nftables and in the security group.

**Verify.** `curl -v http://10.0.2.10:8080/health` returns 200 from the client, and `ss` shows `0.0.0.0:8080`.

**Prevent.** A deployment health check run from outside the host, and the security groups held as infrastructure-as-code.

| The interviewer asks | A strong answer |
|-------------------|--------------------------------------|
| Refusal or ICMP unreachable? | TCP is refused with a RST; a closed UDP port returns ICMP port unreachable (type 3 code 3). |
| What does tcpdump placement prove? | A capture on the VM shows whether the packet arrives; if not, the drop is upstream. |
| How do `ufw` and nftables relate? | `ufw` is a front end that writes rules into the kernel's netfilter. |

**Variant.** The application binds only to an IPv6 wildcard, or to a Unix socket behind a proxy that is not running.

### Case 17 · Throughput between Mumbai and Frankfurt is terrible [Optional · ■■■]{.tag} {#c11-17}

[L4 · GOOGLE · MICROSOFT · AMAZON · BROADCOM]{.where}

**Prompt.** "We have a 1 Gb/s private link, but a single backup stream reaches about 6 Mb/s. Several streams in parallel sum to much more."

<figure>
<svg viewBox="0 0 480 115" width="480">
<line class="ln" x1="50" y1="40" x2="240" y2="40"/>
<line class="ln" x1="240" y1="40" x2="430" y2="40"/>
<rect class="box" x="36" y="25" width="28" height="30" rx="1"/><path class="ln" d="M36,35 L64,35 M36,45 L64,45"/><circle class="accf" cx="58" cy="30" r="1.2" style="fill:#1A1D23"/>
<text class="lbl" x="50" y="68" text-anchor="middle">Mumbai</text>
<text class="sm" x="50" y="77" text-anchor="middle">wscale 7</text>
<rect class="box" x="220" y="28" width="40" height="24" rx="1"/><path class="ln" d="M220,40 L260,40 M233,28 L233,40 M247,28 L247,40 M240,40 L240,52 M226,40 L226,52 M254,40 L254,52"/><rect class="acc" x="217" y="25" width="46" height="30" rx="3"/>
<text class="lbl" x="240" y="65" text-anchor="middle">Middlebox</text>
<text class="sm" x="240" y="74" text-anchor="middle">strips wscale</text>
<rect class="box" x="416" y="25" width="28" height="30" rx="1"/><path class="ln" d="M416,35 L444,35 M416,45 L444,45"/><circle class="accf" cx="438" cy="30" r="1.2" style="fill:#1A1D23"/>
<text class="lbl" x="430" y="68" text-anchor="middle">Frankfurt</text>
<text class="sm" x="430" y="77" text-anchor="middle">rmem max 64 KB</text>
<text class="sm" x="240" y="100" text-anchor="middle">1 Gb/s, RTT 80 ms, one stream about 6 Mb/s</text>
</svg>
<figcaption><b>Figure 11.25</b> Case 17. A middlebox strips the window-scale option and an old script caps the receive buffer; one stream is limited to 64 KB per round trip.</figcaption>
</figure>

| We ask | The interviewer answers |
|----------------------|--------------------------------------------|
| Loss on the link? | Nearly none |
| Do parallel streams help? | Yes |
| Round-trip time? | 80 ms |
| Any tuning of the hosts? | A hardening script from years ago |

**Hypotheses, ranked.** (1) a window limit (the bandwidth-delay product); (2) window scaling removed; (3) loss and congestion control; (4) CPU or disk.

| Layer | Command | Decisive output | Inference |
|----|-----------------|----------------------------|--------------------------|
| L4 | arithmetic | BDP = 1 Gb/s × 0.08 s = 10 MB; 64 KB / 80 ms is about 6.5 Mb/s | The observation equals a 64 KB window: window-limited |
| L4 | `ss -ti` | `wscale` field absent | Scaling was not negotiated |
| L4 | `tcpdump -ni eth0 'tcp[tcpflags] & tcp-syn != 0'` at both ends | `wscale 7` leaves Mumbai; the SYN arrives without it | A middlebox strips the option |
| L4 | `sysctl net.ipv4.tcp_rmem` | `4096 16384 65536` | The receive buffer maximum is 64 KB |
| L4 | `iperf3 -c host`, then `-P 8` | about 6 Mb/s, then several times more | Each stream is limited separately |


**Root cause.** Without window scaling, the window cannot exceed 64 KB, and the buffer cap enforces the same limit, so a stream carries at most one window per round trip. The relation is in [§3.9](#s3-9){.ref}.

**Fix.** Stop the option stripping (disable the middlebox's TCP normalisation); raise `tcp_rmem` and `tcp_wmem` maxima to at least 16 MB; consider BBR.

**Verify.** A single `iperf3` stream reaches about 900 Mb/s.

**Prevent.** Baseline long-haul throughput tests, and an audit for drift in `sysctl` settings.

| The interviewer asks | A strong answer |
|-------------------|--------------------------------------|
| Why do parallel streams help? | Each stream has its own window, so their sum approaches the link rate. |
| What if loss, not the window, is the limit? | `ss -ti` shows many retransmissions and a small `cwnd`; the Mathis estimate applies. |
| Would BBR help? | Yes under loss, since it paces to the measured rate and not to loss events. |

**Variant.** A single stream limited by the application, for example a disk or a single-threaded compressor.

### Case 18 · Traceroute shows a scary loss at hop 4 [Optional · ■□□]{.tag} {#c11-18}

[L3 · GOOGLE · CISCO · AMAZON]{.where}

**Prompt.** "A customer sends an `mtr` showing 70 per cent loss at your router, hop 4, and demands a fix."

<figure>
<svg viewBox="0 0 480 110" width="480">
<line class="ln" x1="30" y1="40" x2="120" y2="40"/>
<line class="ln" x1="120" y1="40" x2="250" y2="40"/>
<line class="ln" x1="250" y1="40" x2="350" y2="40"/>
<line class="ln" x1="350" y1="40" x2="445" y2="40"/>
<rect class="box" x="15" y="30" width="30" height="20" rx="1"/><path class="ln" d="M22,54 L38,54"/><rect class="fill" x="19" y="34" width="22" height="11"/>
<text class="lbl" x="30" y="66" text-anchor="middle">Customer</text>
<circle class="box" cx="120" cy="40" r="13"/><path class="ln" d="M113,40 L127,40 M120,33 L120,47 M115,35 L125,45 M115,45 L125,35"/>
<text class="lbl" x="120" y="66" text-anchor="middle">ISP edge</text>
<text class="sm" x="120" y="75" text-anchor="middle">hop 2-3</text>
<circle class="box" cx="250" cy="40" r="13"/><path class="ln" d="M243,40 L257,40 M250,33 L250,47 M245,35 L255,45 M245,45 L255,35"/><circle class="acc" cx="250" cy="40" r="16"/>
<text class="lbl" x="250" y="66" text-anchor="middle">Border</text>
<text class="sm" x="250" y="75" text-anchor="middle">hop 4, CoPP</text>
<circle class="box" cx="350" cy="40" r="13"/><path class="ln" d="M343,40 L357,40 M350,33 L350,47 M345,35 L355,45 M345,45 L355,35"/>
<text class="lbl" x="350" y="66" text-anchor="middle">Core</text>
<text class="sm" x="350" y="75" text-anchor="middle">hop 5</text>
<rect class="box" x="431" y="25" width="28" height="30" rx="1"/><path class="ln" d="M431,35 L459,35 M431,45 L459,45"/><circle class="accf" cx="453" cy="30" r="1.2" style="fill:#1A1D23"/>
<text class="lbl" x="445" y="68" text-anchor="middle">Destination</text>
<text class="sm" x="445" y="77" text-anchor="middle">0% loss</text>
<text class="sm acct" x="250" y="100" text-anchor="middle">mtr shows 70% loss at hop 4 only</text>
</svg>
<figcaption><b>Figure 11.26</b> Case 18. The border router rate-limits the ICMP it generates; the forwarding path is clean.</figcaption>
</figure>

| We ask | The interviewer answers |
|----------------------|--------------------------------------------|
| Loss at the destination? | 0 per cent |
| Impact the customer can see? | None measured; they "saw the report" |
| Which protocol? | `mtr` default, ICMP |

**Hypotheses, ranked.** (1) control-plane rate limiting of ICMP replies (benign); (2) real forwarding loss, which would persist at later hops; (3) a slow return path.

| Layer | Command | Decisive output | Inference |
|----|-----------------|----------------------------|--------------------------|
| L3 | `mtr -rwzbc 200 dest` | hop 4 `70.0%`, hops 5 and 6 `0.0%` | Loss that does not persist is not forwarding loss |
| L4 | `mtr -T -P 443 -rwzbc 200 dest` | same shape | The pattern is independent of the probe |
| L3 | `show policy-map control-plane` | `Class-map: ICMP-TTL ... exceeded 41230 packets` | CoPP limits the replies the router generates |
| L1 | interface counters on the border router | clean | The data plane is healthy |


**Root cause.** None: the router rate-limits the time-exceeded messages it generates, while it forwards the customer's traffic without loss. The skill tested is communication, since the answer is evidence and a courteous explanation.

**Fix.** None; explain with the traces. Consider a modestly higher ICMP rate limit.

**Verify.** The customer's application metrics are normal.

**Prevent.** A support runbook entry for this report.

| The interviewer asks | A strong answer |
|-------------------|--------------------------------------|
| Which latency pattern is real? | A jump at one hop that *persists* to later hops is queueing; one that appears only at that hop is slow-path ICMP. |
| How do you answer the customer? | Share the traces, explain that routers answer probes on a slow path, and offer an end-to-end application test. |
| What would real loss look like? | Loss at hop 4 and at every later hop. |

**Variant.** A different return path for the probe replies inflates the latency shown at one hop.

::: trap
*Claim:* "Any loss in `mtr` is a fault at that hop." *Why it is wrong:* loss at a middle hop that does not carry on to later hops is the router declining to answer probes. *Correct statement:* only loss persisting to the destination counts.
:::

:::
