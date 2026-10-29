::: {.p9}

::: pack
## Problem Set, continued {#ps9b}

::: problems

::: q
### Q9.17 What is NAT-T and which ports does IPsec use?
[CISCO · JUNIPER · NOKIA · TECH-1 · ■■□ · S]{.meta}

[30-second answer: IKE uses UDP 500; ESP is IP protocol 50 and has no ports; NAT traversal detects a NAT during IKE and moves IKE and ESP to UDP 4500, with ESP wrapped in a UDP header.]{.short}

**Answer.** IKE sends hashes of the addresses and ports in its first messages; if they differ from what the peer sees, a NAT lies between them. ESP packets then carry an 8-byte UDP header (RFC 3948), and keepalives hold the NAT mapping open. AH cannot work at all ([9.7](#s9-7){.ref}). **Mistakes.** Opening only UDP 500 on the firewall, so that Phase 1 succeeds and data fails.
:::

::: q
### Q9.18 Explain ARP spoofing and how DAI stops it. What does DAI depend on?
[CISCO · JUNIPER · NOKIA · TECH-1 · ■■□ · S]{.meta}

[30-second answer: the attacker sends forged ARP replies claiming the gateway's IP at his MAC (and the victim's IP at his MAC), becoming a man in the middle; DAI checks each ARP packet on untrusted ports against the DHCP snooping binding table and drops mismatches.]{.short}

**Answer.** ARP has no authentication and hosts accept gratuitous replies. DAI therefore depends on the snooping table (IP, MAC, VLAN, port) or on static ARP ACLs for fixed-address hosts; uplinks and the DHCP server port must be trusted, and a rate limit protects the CPU. Without snooping DAI drops everything, including valid ARP ([9.9](#s9-9){.ref}). **Mistakes.** Enabling DAI before snooping has built its table.
:::

::: q
### Q9.19 What is VLAN hopping? Explain both methods and their mitigations.
[CISCO · JUNIPER · NOKIA · TECH-1 · ■■□ · S]{.meta}

[30-second answer: reaching a VLAN one does not belong to: by switch spoofing (negotiating a trunk with DTP) or double tagging (an outer native-VLAN tag stripped by the first switch exposes an inner tag); disable DTP on access ports and use an unused native VLAN.]{.short}

**Answer.** Switch spoofing: the port is `dynamic auto` or `desirable`, so the attacker's host forms a trunk and sees all VLANs; use `switchport mode access` and `nonegotiate`. Double tagging: the attacker is in the native VLAN, the first switch strips the outer tag, the second delivers by the inner tag; one-way only. Use an unused native VLAN, shut unused ports, tag the native VLAN where supported ([9.9](#s9-9){.ref}). **Mistakes.** Believing that VLAN 1 is harmless because it is "default".
:::

::: q
### Q9.20 What is a SYN flood? How do SYN cookies work?
[GOOGLE · MICROSOFT · AMAZON · CISCO · TECH-1 · ■■□ · S]{.meta}

[30-second answer: a flood of SYNs from spoofed sources fills the server's half-open queue so that real clients are refused; with SYN cookies the server keeps no state and encodes a counter, an MSS index and a keyed hash of the 4-tuple in the SYN-ACK's sequence number, validating it when the ACK returns.]{.short}

**Answer.** The valid ACK (acknowledgement = cookie + 1) proves the client received the SYN-ACK, which a spoofed source cannot do. Cost: TCP options such as window scale must be encoded or lost, so the kernel enables cookies only when the queue overflows. Other defences: larger backlog, SYN proxy at a firewall, rate limits, upstream filtering ([9.10](#s9-10){.ref}, Lab 9.4). **Mistakes.** Saying cookies increase the queue.
:::

::: q
### Q9.21 What is DNS cache poisoning? Why did source-port randomisation help so much?
[GOOGLE · MICROSOFT · AMAZON · TECH-2 · ■■□ · S]{.meta}

[30-second answer: forged answers that match the query's name, 16-bit ID and port, arriving before the real one, are cached and served to all users; randomising the source port adds about 16 more unknown bits, multiplying the attacker's work by about 65,000.]{.short}

**Answer.** The worked probabilities in [9.11](#s9-11){.ref}: about 1.5 % per race with a fixed port against about 2 × 10⁻⁷ with a random one, for 1,000 forged packets. Kaminsky's random sub-domains defeated the cache's protection by making each attempt a new race. Further defences: 0x20 case randomisation, query rate limits, DNSSEC. **Mistakes.** Claiming that randomisation prevents poisoning; it only makes it expensive.
:::

::: q
### Q9.22 RADIUS versus TACACS+: which for device administration, and why?
[CISCO · JUNIPER · NOKIA · TECH-1 · ■■□ · S]{.meta}

[30-second answer: TACACS+ for device administration: it separates authentication, authorisation and accounting, authorises each command, runs over TCP 49 and encrypts the whole body; RADIUS (UDP 1812 and 1813) suits network access such as 802.1X and VPN.]{.short}

**Answer.** RADIUS combines authentication and authorisation and hides only the password attribute, but it is an open standard supported by every vendor and by Wi-Fi and VPN gear; TACACS+ was Cisco's, now widely supported. Keep a local fallback account for the day the server is unreachable ([9.12](#s9-12){.ref}). **Mistakes.** Using RADIUS where command authorisation is required.
:::

::: q
### Q9.23 Explain the 802.1X roles and the message flow.
[CISCO · MICROSOFT · NOKIA · TECH-2 · ■■□ · S]{.meta}

[30-second answer: the supplicant (client) and authenticator (switch) exchange EAPOL; the switch relays EAP to the authentication server (RADIUS), which accepts or rejects and may return a VLAN; only then is the port authorised.]{.short}

**Answer.** Figure 9.18: EAPOL-Start, identity request and response, Access-Request, an EAP method exchange (EAP-TLS or PEAP) relayed in Access-Challenges, Access-Accept with VLAN attributes, EAP-Success. Before that only EAPOL passes. Devices without a supplicant use MAB, which is weak ([9.12](#s9-12){.ref}). **Follow-ups.** Which method is strongest? (EAP-TLS.) **Mistakes.** Saying the switch checks the password.
:::

::: q
### Q9.24 What is uRPF? Strict versus loose mode, and where is loose required?
[CISCO · JUNIPER · AMAZON · TECH-2 · ■■□ · S]{.meta}

[30-second answer: uRPF drops a packet whose source address has no route back through the arrival interface (strict) or no route at all (loose), implementing BCP 38; loose is required on multihomed borders where return paths are asymmetric.]{.short}

**Answer.** Strict suits single-homed customer edges. On BR1 and BR2 with two providers, a valid packet from a remote network may arrive on the interface that is not the best path back, so strict mode would drop it; loose mode still drops unrouted (bogon or unallocated) sources ([9.10](#s9-10){.ref}). **Mistakes.** Applying strict mode where routing is asymmetric.
:::

::: q
### Q9.25 A 400 Gb/s amplification DDoS hits your customer's IP. Walk through mitigation from the first minute to steady state.
[GOOGLE · AMAZON · MICROSOFT · TECH-2 · ■■■ · S]{.meta}

[30-second answer: confirm and classify from flow data; protect capacity by diverting to a scrubbing centre (or black-holing the one target if it cannot be saved); filter the reflected protocol with Flowspec and ACLs; coordinate with upstreams; then harden and tune.]{.short}

**Structured answer.**

1. *Minute 0 to 5, detect and classify.* NetFlow or IPFIX and SNMP show a surge to one address, UDP from source port 53 or 123 or 11211, huge packets. Declare an incident and name an owner.
2. *Contain.* The link is saturated, so local filtering cannot help; only upstream capacity can. Advertise the victim prefix to the scrubbing provider (BGP diversion or anycast), or, if the customer is expendable for now, RTBH the single /32 (it completes the denial of service but saves everything else).
3. *Filter.* Ask upstreams to apply Flowspec or ACLs on UDP source port 11211 and 123, fragments and oversized packets; rate-limit the reflected services.
4. *Steady state.* Return clean traffic over a tunnel, confirm the customer's service, keep the diversion until the attack stops, then withdraw it.
5. *After.* Check BCP 38 and open resolvers on one's own network, publish the timeline, add always-on protection.

**Mistakes.** Relying on the customer's firewall, which sees the flood after the link is full. **Follow-ups.** Why not block at the origin? (Spoofing hides it.)
:::

::: q
### Q9.26 How does DNSSEC establish trust? What does it not protect against? How is DoH different?
[GOOGLE · MICROSOFT · AMAZON · TECH-2 · ■■■ · S]{.meta}

[30-second answer: a chain of signed DS and DNSKEY records from the root trust anchor down to the zone, so a validating resolver can verify the RRSIG on an answer; it does not encrypt queries, hide them from observers, or help against a compromised resolver or registrar. DoH encrypts the client-resolver hop and proves nothing about the data.]{.short}

**Answer.** Figure 9.17 shows the chain. Not covered: privacy, availability (signed answers make amplification worse), unsigned zones, and the last hop if the client does not validate. DoH and DoT give privacy and integrity on one hop; with a malicious resolver they offer no truth ([9.11](#s9-11){.ref}). **Mistakes.** Equating the two.
:::

::: q
### Q9.27 A stateful firewall pair in active/active drops 30 % of return traffic. Diagnose.
[CISCO · JUNIPER · AMAZON · NOKIA · TECH-2 · ■■■ · S]{.meta}

[30-second answer: asymmetric routing: some replies return through the unit that did not see the SYN and so has no session; fix with symmetric paths, state synchronisation, or a single logical firewall.]{.short}

**Approach.** The drop fraction (about a third) suggests that one of several equal paths or ECMP hash outcomes returns through the other unit. Check, in order: (i) drop counters and logs naming "no session" or "invalid state"; (ii) the session table of each unit for the failing flow; (iii) whether state sync is enabled and fast enough for the first packets (a reply can overtake the sync); (iv) the routing on both sides, whether ECMP or BGP policy sends return traffic via the second border. **Fix.** Make the paths symmetric (local preference and AS-path prepending, or a hash by source and destination that is symmetric); or active/standby; or session sync with a proper cluster ([9.6](#s9-6){.ref}, Figure 9.9). The corresponding case is [Case 13](#c11-13){.ref}. **Mistakes.** Disabling inspection to "make it work".
:::

::: q
### Q9.28 Design the network security for a new 2,000-student campus.
[CISCO · AMAZON · MICROSOFT · TECH-2 · ■■■ · T]{.meta}

[30-second answer: segment by role, authenticate every port and SSID with 802.1X, filter between segments with a firewall and ACLs, protect the edge, harden the switches, and log everything to a SIEM.]{.short}

**Structured answer.**

| Layer | Design |
|---|---|
| Segmentation | VLANs and subnets for staff, students, servers, guests, IoT, management; routing between them only through the firewall or filtered at the distribution layer |
| Access | 802.1X (EAP-TLS for staff, PEAP or a portal for students), MAB for printers, dynamic VLAN, guest Wi-Fi isolated and rate-limited |
| Switch hardening | DHCP snooping, DAI, port security, BPDU Guard, unused ports off, native VLAN unused ([9.9](#s9-9){.ref}) |
| Edge | active/standby NGFW pair with NAT, IPS, URL filtering, uRPF, BGP filters and RPKI, DDoS service |
| Remote access | TLS or IKEv2 VPN with MFA; or identity-aware proxy ([9.14](#s9-14){.ref}) |
| Management | TACACS+ with local fallback, SSH only, management VRF, SNMPv3, NTP, syslog to a SIEM |
| Data and apps | TLS everywhere, certificates by ACME, backups offline |

**Follow-ups.** How are students on personal devices handled? (Separate VLAN, posture check, no access to servers except by proxy.) **Mistakes.** Starting with products instead of assets and threats ([9.1](#s9-1){.ref}).
:::

::: q
### Q9.29 Explain BGP hijacking and how RPKI route-origin validation mitigates it. What are its limits?
[GOOGLE · AMAZON · JUNIPER · TECH-2 · ■■■ · S]{.meta}

[30-second answer: an AS announces a prefix it does not own (or a more specific one) and attracts traffic; with RPKI the owner signs a ROA naming the allowed origin AS and maximum length, and validating routers drop invalid announcements. ROV checks only the origin, so a forged origin or a path attack passes.]{.short}

**Answer.** Valid, invalid and not-found are the three states; coverage is incomplete, so not-found routes are still accepted. Limits: no path validation (ASPA and BGPsec address it), loose `maxLength` allows a more specific hijack inside the ROA, and route leaks are not hijacks. Add prefix lists from the IRR, max-prefix limits and monitoring ([9.10](#s9-10){.ref}, [4.7](#s4-7){.ref}). **Mistakes.** Thinking that RPKI encrypts or authenticates BGP sessions.
:::

::: q
### Q9.30 What is zero trust? How would you migrate a VPN-based company to it? Map it to NIST SP 800-207.
[GOOGLE · MICROSOFT · AMAZON · TECH-2 · ■■■ · S]{.meta}

[30-second answer: no implicit trust from network location; every request is authenticated, authorised and checked against device state, per session. Migrate application by application behind an identity-aware proxy, then retire the broad VPN.]{.short}

**Structured answer.**

1. *Inventory* users, devices, applications and flows.
2. *Identity first:* central identity provider with MFA; device certificates and an inventory with posture signals (the identity management and CDM feeds of the 800-207 model).
3. *Put a Policy Enforcement Point in front of the first, least critical applications:* an identity-aware proxy. The policy engine and administrator are its decision service; policy is written per application and group.
4. *Observe, then enforce:* log decisions in a SIEM first, then block.
5. *Move the rest*, micro-segment the data centre, and retire full-tunnel access.

**Follow-ups.** What stays? (Firewalls and segmentation remain; the change is that location does not grant trust.) **Mistakes.** Buying "a zero-trust product" and keeping flat internal access ([9.14](#s9-14){.ref}).
:::

::: q
### Q9.31 TLS inspection on an NGFW: how does it work, what breaks, and what are the privacy and legal considerations?
[CISCO · JUNIPER · MICROSOFT · TECH-2 · ■■■ · T]{.meta}

[30-second answer: the firewall terminates the client's TLS session with a certificate it forges on the fly under an enterprise CA the clients trust, inspects the plaintext, and opens a second TLS session to the server; pinning and mutual TLS break, and the firewall's CA key becomes a prize.]{.short}

**Answer.** Breaks: apps with certificate pinning, client-certificate (mTLS) services, and TLS 1.3 features such as ECH. Practice: exempt banking, health and other sensitive categories, keep the CA key in an HSM, tell users by policy, keep logs short, and verify server certificates on the outbound leg, since otherwise the firewall hides the server's errors from the user ([9.6](#s9-6){.ref}). Legal: consent and data-protection duties apply to employee and student traffic. **Mistakes.** Inspecting everything and storing plaintext.
:::

::: q
### Q9.32 Compare IPsec, WireGuard and TLS VPNs for 10,000 remote employees: performance, NAT traversal, management.
[CISCO · JUNIPER · AMAZON · TECH-2 · ■■■ · T]{.meta}

[30-second answer: for managed laptops at scale choose a TLS/DTLS or IKEv2 client with certificates and MFA and central policy; IPsec performs well and is hardware-accelerated; WireGuard is the fastest and simplest, but its static key model needs a management layer; TLS VPN passes the most firewalls.]{.short}

| | IPsec (IKEv2) | WireGuard | TLS/DTLS VPN |
|---|---|---|---|
| Throughput | high, hardware offload on gateways | very high, in-kernel, small code | good with DTLS, lower over TCP |
| NAT and firewall traversal | NAT-T on UDP 4500; may be blocked | UDP only, any port | TCP 443 passes nearly everywhere |
| Management at 10,000 users | mature: certificates, EAP, per-user policy | peers are keys, so provisioning, revocation and per-user logging need extra tooling | mature: SAML, MFA, posture, per-app policy |
| Failure modes | MTU, selector mismatches | no built-in identity beyond keys | TCP-over-TCP stalls |

**Answer.** Decide by what must be managed: identity and posture (TLS or IKEv2 products), performance and simplicity for site links (WireGuard), and reach through hostile networks (TLS on 443). **Follow-ups.** Why prefer an identity-aware proxy for individual apps? ([9.14](#s9-14){.ref}). **Mistakes.** Judging only by raw throughput.
:::

:::
:::

:::
