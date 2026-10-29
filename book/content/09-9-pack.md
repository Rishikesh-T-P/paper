::: {.p9}

::: pack
## Revision Spread {#rv9}

::: revision
::: top
**Ten facts.** (1) CIA plus AAA; STRIDE maps threats to properties; defence in depth means independent rings. (2) Symmetric for bulk (AES-GCM, ChaCha20), asymmetric to agree keys and sign, hash for integrity, HMAC for keyed integrity; ephemeral DH gives forward secrecy. (3) A certificate is a CA signature over a name and a key; the server must send leaf and intermediates; the client checks the SAN, the dates, the chain and revocation. (4) TLS 1.3: one round trip, encryption starts after ServerHello, certificate encrypted, 0-RTT can be replayed. (5) ACL: first match, implicit deny, extended near the source, standard near the destination, wildcard is the inverse of the mask. (6) Stateful firewalls need both directions of a flow through one device. (7) IPsec: ESP 50, AH 51, IKE UDP 500, NAT-T UDP 4500; IKEv2 is four messages; "phase 1 up" never means the VPN works. (8) Layer-2 controls: DHCP snooping feeds DAI; port security stops MAC flooding; `nonegotiate` and an unused native VLAN stop hopping. (9) SYN cookies keep no state; amplification is stopped at the source by BCP 38 and at the victim by upstream scrubbing; DNSSEC signs data, DoH hides the hop. (10) TACACS+ for admins, RADIUS for access, 802.1X relays EAP; zero trust decides per request.

**Three figures to redraw.** The TLS 1.3 ladder with the encrypted part shaded (Figure 9.5), the IKEv2 four-message ladder (Figure 9.11), and the ESP packet formats (Figure 9.10).
:::

### Attack, defence and command

| Attack and defence | Command |
|---|---|
| ARP spoofing: Dynamic ARP Inspection | `ip arp inspection vlan 10,20`; uplink `ip arp inspection trust` |
| Rogue DHCP, starvation: DHCP snooping | `ip dhcp snooping vlan 10,20`; uplink `ip dhcp snooping trust`; `limit rate 15` |
| MAC flooding: port security | `switchport port-security maximum 2`; `violation restrict`; `mac-address sticky` |
| Switch spoofing: no DTP | `switchport mode access`; `switchport nonegotiate` |
| Double tagging: unused native VLAN | `switchport trunk native vlan 999` |
| STP root takeover: BPDU Guard, Root Guard | `spanning-tree bpduguard enable`; `spanning-tree guard root` |
| Spoofed sources: uRPF, BCP 38, IP Source Guard | `ip verify unicast source reachable-via rx` (or `any`); `ip verify source` |
| SYN flood: SYN cookies | `sysctl -w net.ipv4.tcp_syncookies=1` |
| Amplification: BCP 38, closed resolvers, scrubbing, RTBH | upstream; Flowspec |
| BGP hijack: RPKI ROV, prefix filters, max-prefix | `neighbor ... maximum-prefix`; validating RPKI session |
| DNS poisoning: port randomisation, 0x20, DNSSEC | validating resolver; `dig +dnssec` |
| Telnet, clear passwords: SSH 2, secret type 8 or 9 | `transport input ssh`; `algorithm-type scrypt secret` |
| Weak SNMP: SNMPv3 with privacy | `snmp-server group MON v3 priv` |
| Rogue device on a port: 802.1X | `authentication port-control auto` |
| Lateral movement: segmentation, zero trust | firewall zones; identity-aware proxy |

### Ports and protocols for security services

| Service | Port or protocol |
|---|---|
| SSH · Telnet (clear) | TCP 22 · TCP 23 |
| DNS · DoT · DoH | 53 · TCP 853 · TCP 443 |
| HTTPS · QUIC | TCP 443 · UDP 443 |
| IKE · NAT-T | UDP 500 · UDP 4500; ESP is IP protocol 50, AH 51 |
| WireGuard | UDP 51820 (default) |
| RADIUS · TACACS+ | UDP 1812 and 1813 · TCP 49 |
| Syslog · SNMP · NTP | UDP 514 · UDP 161 and 162 · UDP 123 |
| LDAP · LDAPS · Kerberos | 389 · 636 · 88 |
| DHCP (watched by snooping) | UDP 67 and 68 |

### Cryptography at a glance

| Primitive | Gives, and the pitfall |
|---|---|
| Symmetric AEAD (AES-GCM, ChaCha20) | confidentiality and integrity; nonce reuse, ECB |
| Hash (SHA-256) | fingerprint; not authentication, not for passwords |
| HMAC | keyed integrity; short or reused key |
| Signature (ECDSA, Ed25519, RSA-PSS) | origin, non-repudiation; not "encrypt with the private key" |
| (EC)DH (X25519, P-256) | shared secret; no authentication alone |
| RSA key transport | secret to a public key; no forward secrecy, gone from TLS 1.3 |
| Equal strength | 256-bit EC, 3072-bit RSA, 128-bit AES (RSA-2048 is about 112 bits) |

### TLS, IKE, ACL, VPN quick facts

| Topic | Facts |
|---|---|
| TLS 1.3 against 1.2 | 1 RTT against 2; no RSA key transport, renegotiation, compression or CBC; certificate encrypted; five AEAD suites |
| TLS 1.3 messages | ClientHello, ServerHello, then encrypted EncryptedExtensions, Certificate, CertificateVerify, Finished, client Finished |
| IKEv1 against IKEv2 | 6 (main) or 3 (aggressive) plus 3 quick; IKEv2 is 4: IKE_SA_INIT ×2, IKE_AUTH ×2; CREATE_CHILD_SA rekeys |
| IPsec mismatch checklist | encryption, hash or PRF, DH group, authentication and PSK, lifetime, selectors (proxy-IDs), PFS, NAT exemption, routing |
| ESP tunnel overhead (IPv4, GCM) | 54 to 57 bytes, plus 8 for NAT-T; MSS about 1395 on a 1500 link, commonly 1360 |
| ACL placement | extended near the source, standard near the destination; inbound drops before routing |
| Wildcard masks | /8 0.255.255.255 · /16 0.0.255.255 · /20 0.0.15.255 · /22 0.0.3.255 · /24 0.0.0.255 · /25 0.0.0.127 · /26 0.0.0.63 · /27 0.0.0.31 · /28 0.0.0.15 · /29 0.0.0.7 · /30 0.0.0.3 · host 0.0.0.0 |
| VPN choice | site link: IPsec or WireGuard; managed laptops: IKEv2 or TLS; hostile networks: TLS on 443 |
| DDoS classes | volumetric (scrubbing, RTBH), protocol (cookies, proxies), application (CDN, WAF) |

**Zero-trust tenets (NIST SP 800-207).** (1) All data sources and computing services are resources. (2) All communication is secured regardless of network location. (3) Access is granted per session. (4) Access is decided by dynamic policy (identity, device, behaviour). (5) The enterprise monitors the integrity and posture of all assets. (6) Authentication and authorisation are strictly enforced before access. (7) The enterprise collects as much information as it can about the state of assets and traffic to improve policy.

### Flashcards

| Q | A |
|---|---|
| CIA? | Confidentiality, integrity, availability |
| STRIDE? | Spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege |
| Sign or encrypt with which key? | Sign with the private key; encrypt with the public key |
| Why HMAC, not H(K‖m)? | Length-extension attack on SHA-2 |
| Toy DH: p 23, g 5, a 6, b 15? | A = 8, B = 19, K = 2 |
| Forward secrecy? | Ephemeral DH keys; a stolen long-term key opens no past session |
| Chain of trust? | Leaf, intermediate, root in the trust store |
| Missing intermediate? | `unable to verify the first certificate`; send the full chain |
| Revocation methods? | CRL, OCSP, OCSP stapling (must-staple) |
| Certificate Transparency? | Public logs of every certificate; SCTs in the certificate |
| Where does TLS 1.3 encryption start? | After ServerHello |
| What is in the TLS 1.3 ClientHello? | Versions, suites, key share, SNI, ALPN |
| 0-RTT risk? | Replay of early data |
| What does SNI leak? | The site name, unless ECH is used |
| Implicit ACL rule? | `deny any` |
| Standard ACL placement? | Near the destination |
| Wildcard of /20? | 0.0.15.255 |
| Stateless versus stateful? | Per-packet against session table |
| Asymmetric routing and firewalls? | The reply meets a unit with no session; dropped |
| Order of NAT and filter in Linux? | DNAT in prerouting before the filter; SNAT in postrouting after |
| ESP versus AH? | Encrypts and authenticates (50) versus authenticates only, NAT-hostile (51) |
| IKE and NAT-T ports? | UDP 500 and UDP 4500 |
| IKEv2 messages? | Four |
| Phase 1 up, no traffic? | Selectors, transform and PFS, routing, NAT exemption |
| DAI depends on? | DHCP snooping binding table |
| Port security violation modes? | Protect, restrict, shutdown |
| Two VLAN-hopping methods? | DTP switch spoofing; double tagging |
| What does BPDU Guard do? | Err-disables an edge port that receives a BPDU |
| SYN cookie contents? | Counter, MSS index, keyed hash of the 4-tuple |
| uRPF strict versus loose? | Same interface versus any route; loose for multihoming |
| Kaminsky attack? | Random sub-domains give unlimited poisoning races |
| DNSSEC records? | DNSKEY, RRSIG, DS (plus NSEC or NSEC3) |
| DoH is not? | DNSSEC; it protects one hop only |
| RADIUS versus TACACS+? | UDP 1812 combined AAA, password-only encryption, versus TCP 49 separated AAA, full encryption |
| 802.1X roles? | Supplicant, authenticator, authentication server |
| ROV limit? | Checks only the origin AS, not the path |
| Type 7 password? | Reversible; use type 8 or 9 secrets |
| Zero trust in a line? | No implicit trust from location; decide each request with PEP and PDP |

### Self-test

1. Which TLS 1.3 message is the first to be encrypted? (a) ClientHello (b) ServerHello (c) EncryptedExtensions (d) client Finished.
2. The wildcard mask for 10.8.0.0/13 is (a) 0.7.255.255 (b) 0.8.0.0 (c) 0.0.7.255 (d) 0.255.255.255.
3. Which feature stops ARP spoofing on an access switch? (a) port security (b) BPDU Guard (c) Dynamic ARP Inspection (d) uRPF.
4. A VPN shows IKE SA READY but no traffic. The first thing to compare is (a) the DH group of IKE_SA_INIT (b) the traffic selectors of the Child SA (c) the NTP time (d) the VLAN.
5. TACACS+ runs over (a) UDP 49 (b) TCP 49 (c) UDP 1812 (d) TCP 1812.
6. SYN cookies store the connection state in (a) a hash table (b) the SYN queue (c) the initial sequence number (d) a DNS record.
7. A standard ACL goes (a) near the source (b) near the destination (c) on the VTY only (d) outbound on any port.
8. DNSSEC gives (a) privacy of queries (b) authenticity of the data (c) protection of the client-resolver hop (d) availability.
9. AH fails through NAT because (a) it uses UDP (b) its check covers the outer IP header (c) it has no SPI (d) it encrypts ports.
10. ROV validates (a) the AS path (b) the origin AS of a prefix (c) the BGP session (d) the next hop.

**Answers.** 1 c; 2 a (/13 gives 255.248 in the second octet, so 255 − 248 = 7); 3 c; 4 b; 5 b; 6 c; 7 b; 8 b; 9 b; 10 b.

<figure>
<svg viewBox="0 0 480 190" width="480"><defs><marker id="ibk" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="abk" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><text class="lbl" x="90" y="14" text-anchor="middle">Client</text><text class="lbl" x="390" y="14" text-anchor="middle">Server</text><line class="lg" x1="90" y1="20" x2="90" y2="180" /><line class="lg" x1="390" y1="20" x2="390" y2="180" /><line class="ln" x1="92" y1="34" x2="388" y2="34" marker-end="url(#ibk)"/><text class="sm" x="240" y="31" text-anchor="middle">1  ..........................................</text><line class="ln" x1="388" y1="54" x2="92" y2="54" marker-end="url(#ibk)"/><text class="sm" x="240" y="51" text-anchor="middle">2  ..........................................</text><line class="ln" x1="388" y1="74" x2="92" y2="74" marker-end="url(#ibk)"/><text class="sm" x="240" y="71" text-anchor="middle">3  ..........................................</text><line class="ln" x1="388" y1="94" x2="92" y2="94" marker-end="url(#ibk)"/><text class="sm" x="240" y="91" text-anchor="middle">4  ..........................................</text><line class="ln" x1="388" y1="114" x2="92" y2="114" marker-end="url(#ibk)"/><text class="sm" x="240" y="111" text-anchor="middle">5  ..........................................</text><line class="ln" x1="388" y1="134" x2="92" y2="134" marker-end="url(#ibk)"/><text class="sm" x="240" y="131" text-anchor="middle">6  ..........................................</text><line class="ln" x1="92" y1="154" x2="388" y2="154" marker-end="url(#ibk)"/><text class="sm" x="240" y="151" text-anchor="middle">7  ..........................................</text></svg>
<figcaption><b>Figure 9.21</b> Self-test: name the seven numbered messages and mark where encryption begins. The answer is in the TLS 1.3 ladder of this chapter.</figcaption>
</figure>

**Answer to the figure.** 1 ClientHello; 2 ServerHello (encryption begins after it); 3 EncryptedExtensions; 4 Certificate; 5 CertificateVerify; 6 server Finished; 7 client Finished.
:::
:::

:::
