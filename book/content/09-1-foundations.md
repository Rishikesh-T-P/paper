::: {.chapter .p9}
::: opener
[Part I · Pillar 9]{.part-label}

[9]{.num}

# Network Security {#ch9}

[Locks, keys and liars: we name every major attack from Layer 2 to Layer 7, the control that stops it, and walk through TLS 1.3 and IKEv2 packet by packet.]{.promise}

1. [9.1 Security mindset: CIA, AAA, STRIDE, defence in depth]{} [SHOULD]{}
2. [9.2 Cryptography you must be able to explain]{} [MUST]{}
3. [9.3 PKI and certificates]{} [MUST]{}
4. [9.4 The TLS 1.3 handshake, step by step]{} [MUST]{}
5. [9.5 ACLs: stateless packet filtering]{} [MUST]{}
6. [9.6 Stateful firewalls, NGFW and NAT interplay]{} [MUST]{}
7. [9.7 IPsec and IKE]{} [MUST]{}
8. [9.8 VPN families and remote access]{} [SHOULD]{}
9. [9.9 Layer-2 attacks and switch hardening]{} [MUST]{}
10. [9.10 Layer-3 and Layer-4 attacks, and DDoS]{} [MUST]{}
11. [9.11 DNS security]{} [SHOULD]{}
12. [9.12 AAA, RADIUS, TACACS+ and 802.1X]{} [SHOULD]{}
13. [9.13 Detection and device hardening]{} [OPTIONAL]{}
14. [9.14 Zero trust]{} [SHOULD]{}
:::

This chapter assumes the protocols of [Pillar 3](#ch3){.ref} (ARP, DHCP, TCP, DNS) and the switching and routing of [Pillar 4](#ch4){.ref}; it adds the adversary. The examples belong to **Campus Net**, the fictional university network of Pillar 4: SALES (VLAN 10, 192.168.10.0/24) and ENG (VLAN 20, 192.168.20.0/24) on the office floor, a server network 10.0.0.0/24 holding the web server 10.0.0.80, two border routers BR1 and BR2, and the public address 203.0.113.5 used for translation. NAT itself is taught in [Section 3.6](#s3-6){.ref} and IOS access-list syntax in [Section 4.13](#s4-13){.ref}; here we teach the reasoning behind them. Candidate reports show that Cisco, Juniper and Nokia ask about ACLs, IPsec and Layer-2 hardening, whereas Google, Microsoft and Amazon ask about TLS, DNS and DDoS; these are patterns reported by candidates, not official syllabi.

## [9.1]{.sec}Security mindset: CIA, AAA, STRIDE, defence in depth [Should · ■□□]{.tag} {#s9-1}

::: bigidea
Security is the management of risk, not the removal of it, because every control costs money or convenience and every asset has a finite value; we therefore stack independent controls so that one failure is not fatal.
:::

Three properties define what is being protected. *Confidentiality* means that only authorised parties can read the data; *integrity* means that it cannot be altered undetected; *availability* means that it can be reached when needed. Together they form the *CIA triad*. Three further services answer who is asking: *authentication* proves identity, *authorisation* decides what that identity may do, and *accounting* records what it did; the three are called *AAA* (Section 9.12). *Non-repudiation* adds that the sender cannot later deny having sent a message, which only a digital signature gives (Section 9.2).

A breach of each property has a network example. A packet capture on shared Wi-Fi breaks confidentiality; a router that rewrites a downloaded file breaks integrity; a SYN flood against the web server breaks availability. Note that the three can conflict: encrypting everything raises confidentiality but blinds the intrusion-detection system, and replicating data raises availability but multiplies the places it can leak.

[**Bank branch** — guard at the door (firewall), CCTV (IDS), locker keys (encryption), visitor register (logging), two keys for the vault (separation of duty).]{.margin}To reason about attackers systematically we use *STRIDE*, a threat classification from Microsoft. Each letter is a way of violating one security property, and each has a standard family of controls.

| Threat | Violates | Campus Net example | Typical control |
|---|---|---|---|
| **S**poofing | authentication | forged ARP reply for the gateway | DAI, 802.1X, certificates |
| **T**ampering | integrity | modified packet on an unencrypted link | TLS, IPsec, HMAC |
| **R**epudiation | non-repudiation | an admin denies deleting a VLAN | AAA accounting, signed logs |
| **I**nformation disclosure | confidentiality | Telnet password sniffed on a trunk | SSH, TLS, encryption at rest |
| **D**enial of service | availability | SYN flood on 10.0.0.80 | SYN cookies, rate limits, scrubbing |
| **E**levation of privilege | authorisation | a student account gains enable access | least privilege, TACACS+ command sets |

A *threat model* lists the assets, the entry points to them and one threat per STRIDE letter with its control. It is the first step of any design, because a control without a named threat cannot be justified or tested.

<figure>
<svg viewBox="0 0 480 226" width="480"><defs><marker id="ion" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="aon" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><rect class="fill" x="6" y="4" width="468" height="218" rx="0" /><text class="lbl" x="14" y="17" text-anchor="start">Physical</text><text class="sm" x="64.8" y="17" text-anchor="start">locked wiring closets, badge readers</text><rect class="box" x="18" y="24" width="444" height="178" rx="0" /><text class="lbl" x="26" y="37" text-anchor="start">Perimeter</text><text class="sm" x="82.4" y="37" text-anchor="start">edge firewall, DDoS scrubbing, IPS</text><rect class="fill" x="30" y="44" width="420" height="138" rx="0" /><text class="lbl" x="38" y="57" text-anchor="start">Network</text><text class="sm" x="83.19999999999999" y="57" text-anchor="start">VLANs, ACLs, 802.1X, snooping, DAI</text><rect class="box" x="42" y="64" width="396" height="98" rx="0" /><text class="lbl" x="50" y="77" text-anchor="start">Host</text><text class="sm" x="78.4" y="77" text-anchor="start">patching, endpoint detection</text><rect class="fill" x="54" y="84" width="372" height="58" rx="0" /><text class="lbl" x="62" y="97" text-anchor="start">Application</text><text class="sm" x="129.6" y="97" text-anchor="start">TLS, input validation, login</text><rect class="box" x="66" y="104" width="348" height="18" rx="0" /><text class="lbl" x="74" y="117" text-anchor="start">Data</text><text class="sm" x="102.4" y="117" text-anchor="start">encryption at rest, backups, keys</text></svg>
<figcaption><b>Figure 9.1</b> Defence in depth for Campus Net: independent controls on every ring, so that the failure of one does not expose the data.</figcaption>
</figure>

*Defence in depth* places controls on several rings (Figure 9.1), each assumed to fail some day. The rings should be independent, meaning that one flaw (a stolen password, say) does not defeat two rings at once. Further, each ring should fail closed where possible and should log, so that the next ring and the operators learn of the failure.

::: example
**A threat model for the Campus Net Wi-Fi and lab network.** Assets: student records on 10.0.0.0/24, the lab switches, and the guest Wi-Fi's reputation. Entry points: the Wi-Fi, the lab sockets, the VPN and the public web server.

1. Spoofing: someone joins the staff SSID with a shared password. Control: WPA3-Enterprise with 802.1X, so that identity is per user (Section 9.12).
2. Tampering: a rogue DHCP server hands out a malicious gateway. Control: DHCP snooping on access ports (Section 9.9).
3. Repudiation: a technician changes an ACL and denies it. Control: TACACS+ accounting to a syslog server.
4. Information disclosure: the lab's HTTP management page sends passwords in clear. Control: HTTPS only, HTTP disabled (Section 9.13).
5. Denial of service: a student floods the DHCP pool. Control: DHCP rate limiting and port security.
6. Elevation of privilege: a guest laptop reaches the server VLAN. Control: guest VLAN with an ACL or firewall rule denying 10.0.0.0/24.

[Result: six threats, six controls, each with an owner and a test; the table is the audit trail.]{.result}
:::

::: lens
[CISCO · AMAZON · MICROSOFT]{.co}

"Name the CIA triad and give a network breach of each" is a warm-up; "How would you secure a campus?" is the real question. A strong answer names the assets first, then the rings of Figure 9.1, then one control per threat, and ends with logging and a way to test each control.
:::

## [9.2]{.sec}Cryptography you must be able to explain [Must · ■■□]{.tag} {#s9-2}

::: bigidea
Every secure protocol in this chapter is built from five primitives (symmetric ciphers, hashes, MACs, signatures and key exchange), because each solves exactly one problem that the others cannot.
:::

**Symmetric encryption** uses one secret key for both directions. It is fast (AES runs at many gigabits per second, helped by hardware instructions), so it carries all bulk data. Its problem is distribution: both parties must already share the key. A *block cipher* such as AES transforms 128-bit blocks; a *mode of operation* says how to handle longer messages. ECB encrypts each block alone, so equal plaintext blocks give equal ciphertext blocks and patterns survive; it must never be used. CBC chains blocks through an initialisation vector (IV) but gives no integrity. CTR turns the cipher into a stream. GCM is CTR with an authentication tag, termed *authenticated encryption with associated data* (AEAD): one operation gives confidentiality and integrity. ChaCha20-Poly1305 is the other AEAD in common use, faster than AES where hardware support is missing. Note that GCM fails badly if a key and nonce pair is ever reused, so protocols derive nonces from counters.

**Hash functions** map any input to a fixed-size digest (SHA-256 gives 256 bits). Three properties matter: given a digest one cannot find an input (*pre-image resistance*), cannot find a second input with the same digest, and cannot find any colliding pair. MD5 and SHA-1 are broken for collisions and are not used for security. A hash alone does not authenticate a message, because an attacker who alters the message can recompute the hash. For stored passwords a fast hash is also wrong; one uses a salted, deliberately slow function such as bcrypt or Argon2.

**HMAC** fixes this by mixing a shared key into the hash: HMAC(K, m) = H((K ⊕ opad) ‖ H((K ⊕ ipad) ‖ m)). Only holders of K can produce the tag, so it gives integrity and origin authentication. The nested form is used because the naive H(K ‖ m) is open to *length-extension* attacks on SHA-2. HMAC is how IPsec (older suites), TLS 1.2 non-AEAD suites and many API signatures work.

**Asymmetric cryptography** gives each party a *key pair*: a public key that may be published and a private key that is never shared. RSA rests on the difficulty of factoring large numbers; elliptic-curve cryptography (ECC) rests on the discrete logarithm on a curve and reaches the same strength with much smaller keys (a 256-bit curve matches about 3072-bit RSA). Asymmetric operations are around a thousand times slower than AES, hence the standard design: use them briefly to agree on keys or prove identity, then switch to symmetric encryption.

A **digital signature** proves who produced a message. The signer hashes the message and signs the digest with the private key; anyone verifies it with the public key (Figure 9.2). Encryption and signing use the pair in opposite directions: to send a secret to Bob one encrypts with Bob's public key, and to sign one uses one's own private key.

<figure>
<svg viewBox="0 0 480 150" width="480"><defs><marker id="ise" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="ase" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><text class="lbl" x="8" y="14" text-anchor="start">Confidentiality</text><rect class="box" x="8" y="22" width="70" height="26" rx="0" /><text class="lbl" x="43.0" y="38.0" text-anchor="middle">plaintext</text><rect class="box" x="130" y="22" width="100" height="26" rx="0" /><text class="lbl" x="180.0" y="34.0" text-anchor="middle">encrypt</text><text class="sm" x="180.0" y="44.0" text-anchor="middle">with Bob's public key</text><rect class="box" x="282" y="22" width="70" height="26" rx="0" /><text class="lbl" x="317.0" y="38.0" text-anchor="middle">ciphertext</text><rect class="box" x="404" y="22" width="70" height="26" rx="0" /><text class="lbl" x="439.0" y="34.0" text-anchor="middle">decrypt</text><text class="sm" x="439.0" y="44.0" text-anchor="middle">Bob's private</text><line class="ln" x1="78" y1="35" x2="130" y2="35" marker-end="url(#ise)"/><line class="ln" x1="230" y1="35" x2="282" y2="35" marker-end="url(#ise)"/><line class="ln" x1="352" y1="35" x2="404" y2="35" marker-end="url(#ise)"/><text class="lbl" x="8" y="84" text-anchor="start">Authenticity and integrity</text><rect class="box" x="8" y="92" width="70" height="26" rx="0" /><text class="lbl" x="43.0" y="108.0" text-anchor="middle">message</text><rect class="box" x="110" y="92" width="60" height="26" rx="0" /><text class="lbl" x="140.0" y="108.0" text-anchor="middle">hash</text><rect class="box" x="212" y="92" width="110" height="26" rx="0" /><text class="lbl" x="267.0" y="104.0" text-anchor="middle">sign</text><text class="sm" x="267.0" y="114.0" text-anchor="middle">with Alice's private key</text><rect class="box" x="364" y="92" width="110" height="26" rx="0" /><text class="lbl" x="419.0" y="104.0" text-anchor="middle">verify</text><text class="sm" x="419.0" y="114.0" text-anchor="middle">with Alice's public key</text><line class="ln" x1="78" y1="105" x2="110" y2="105" marker-end="url(#ise)"/><line class="ln" x1="170" y1="105" x2="212" y2="105" marker-end="url(#ise)"/><line class="acc" x1="322" y1="105" x2="364" y2="105" marker-end="url(#ase)"/><text class="sm" x="343" y="134" text-anchor="middle">signature + message; verifier hashes the message again</text><text class="sm" x="343" y="100" text-anchor="middle"></text></svg>
<figcaption><b>Figure 9.2</b> Encryption and signature use the key pair in opposite directions: encrypt to the public key, sign with the private key.</figcaption>
</figure>

::: trap
*Claim:* a signature is "encryption with the private key". *Why it is wrong:* this holds only for textbook RSA; ECDSA and EdDSA are not encryption at all, and real RSA signatures add padding (PSS). *Correct statement:* one signs with the private key and verifies with the public key; one encrypts with the public key and decrypts with the private key.
:::

**Diffie-Hellman (DH)** lets two parties create a shared secret over a public channel. Both agree on public numbers: a prime p and a generator g. Each picks a secret, publishes g raised to it modulo p, and raises the other's value to its own secret. Since (gᵃ)ᵇ = (gᵇ)ᵃ, both reach the same number, while an eavesdropper who sees only the published values must solve the *discrete logarithm problem*, which is infeasible for large p. In the paint-mixing analogy, each side mixes a public colour with a private one, swaps the mixtures, and adds the private colour again; nobody can un-mix the shared result.

::: example
**Toy Diffie-Hellman.** Take p = 23, g = 5. The client chooses a = 6 and the server b = 15.

1. Client publishes A = 5⁶ mod 23. Now 5² = 25 ≡ 2, so 5⁶ ≡ 2³ = 8. A = 8.
2. Server publishes B = 5¹⁵ mod 23. Using 5² ≡ 2, 5⁴ ≡ 4, 5⁸ ≡ 16: 5¹⁵ = 5⁸ · 5⁴ · 5² · 5 ≡ 16 · 4 · 2 · 5 = 640 ≡ 19. B = 19.
3. Client computes Bᵃ = 19⁶ mod 23. Since 19 ≡ −4, (−4)⁶ = 4096 ≡ 2.
4. Server computes Aᵇ = 8¹⁵ mod 23. Since 8 = 2³ and 2¹¹ ≡ 1 (mod 23), 8¹⁵ = 2⁴⁵ ≡ 2¹ = 2.

[Result: shared secret K = 2 on both sides; Eve sees only 23, 5, 8 and 19.]{.result}
:::

<figure>
<svg viewBox="0 0 480 190" width="480"><defs><marker id="idh" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="adh" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><rect class="fill" x="150" y="6" width="180" height="24" rx="0" /><text class="lbl" x="240.0" y="21.0" text-anchor="middle">public: p = 23, g = 5</text><text class="lbl" x="80" y="52" text-anchor="middle">Campus Net client</text><text class="lbl" x="400" y="52" text-anchor="middle">Campus Net server</text><line class="lg" x1="80" y1="58" x2="80" y2="182" /><line class="lg" x1="400" y1="58" x2="400" y2="182" /><rect class="box" x="20" y="62" width="120" height="22" rx="0" /><text class="lbl" x="80.0" y="76.0" text-anchor="middle">secret a = 6</text><rect class="box" x="340" y="62" width="120" height="22" rx="0" /><text class="lbl" x="400.0" y="76.0" text-anchor="middle">secret b = 15</text><text class="mono" x="80" y="104" text-anchor="middle">A = 5^6 mod 23 = 8</text><text class="mono" x="400" y="104" text-anchor="middle">B = 5^15 mod 23 = 19</text><line class="ln" x1="130" y1="114" x2="350" y2="114" marker-end="url(#idh)"/><text class="lbl" x="240" y="110" text-anchor="middle">A = 8</text><line class="ln" x1="350" y1="132" x2="130" y2="132" marker-end="url(#idh)"/><text class="lbl" x="240" y="128" text-anchor="middle">B = 19</text><text class="mono" x="80" y="156" text-anchor="middle">K = 19^6 mod 23 = 2</text><text class="mono" x="400" y="156" text-anchor="middle">K = 8^15 mod 23 = 2</text><rect class="hl" x="150" y="142" width="180" height="38" rx="0" /><text class="sm" x="240" y="156" text-anchor="middle">Eve sees 23, 5, 8, 19</text><text class="sm" x="240" y="168" text-anchor="middle">finding a or b is the discrete logarithm</text><rect class="acc" x="20" y="142" width="120" height="22" rx="0"/><rect class="acc" x="340" y="142" width="120" height="22" rx="0"/></svg>
<figcaption><b>Figure 9.3</b> Diffie-Hellman with p = 23 and g = 5. The eavesdropper sees p, g, 8 and 19 only; both ends compute 2.</figcaption>
</figure>

With p = 23 an attacker simply tries all exponents. With a 2048-bit prime, or an elliptic curve such as X25519, the search space is far beyond reach. The shared number is never used directly as a key; a *key derivation function* (HKDF in TLS 1.3) expands it into the keys needed. In *ephemeral* DH (DHE, or ECDHE on curves) fresh secrets are generated for every session and discarded afterwards. This gives *forward secrecy*: if the server's long-term private key is stolen later, recorded sessions still cannot be decrypted, because the session secrets no longer exist. DH alone does not authenticate, so an active attacker can sit in the middle; the signature on the handshake (Section 9.4) closes that gap.

| Primitive | Purpose | Example | What breaks if misused |
|---|---|---|---|
| Symmetric cipher | confidentiality | AES-GCM, ChaCha20-Poly1305 | ECB leaks patterns; nonce reuse in GCM leaks the key stream |
| Hash | integrity fingerprint | SHA-256 | MD5, SHA-1 collisions; fast hashes for passwords |
| HMAC | integrity and origin | HMAC-SHA256 | a short or reused key; H(K ‖ m) instead of HMAC |
| Signature | origin, non-repudiation | ECDSA, Ed25519, RSA-PSS | reused nonce in ECDSA reveals the key |
| Key exchange | shared secret | ECDHE (X25519) | no authentication: man in the middle; static keys: no forward secrecy |
| Key pair encryption | key transport | RSA-OAEP | RSA key transport has no forward secrecy; removed from TLS 1.3 |

Quantum computers running Shor's algorithm would break RSA, DH and ECC; hybrid key exchanges that combine X25519 with a lattice scheme (ML-KEM) are already deployed in browsers. Symmetric ciphers and hashes are weakened only by doubling the key length.

::: check
1. Why does TLS use both symmetric and asymmetric cryptography? [^c9-1]
2. Why is HMAC preferred to H(K ‖ m)? [^c9-2]
3. What does ephemeral DH give that static RSA key transport does not? [^c9-3]
:::

[^c9-1]: Asymmetric operations are slow but need no shared secret; symmetric ones are fast but need one. TLS uses the first to agree a key and the second for the data.
[^c9-2]: H(K ‖ m) allows length extension on SHA-2: an attacker who knows the tag for m can compute a valid tag for m ‖ padding ‖ x without K.
[^c9-3]: Forward secrecy: the session keys are never derived from a long-term key, so stealing that key later does not expose recorded traffic.

## [9.3]{.sec}PKI and certificates [Must · ■■□]{.tag} {#s9-3}

::: bigidea
A certificate binds a public key to a name by a signature from a party the verifier already trusts, so that trust in one root key extends to millions of servers it has never met.
:::

Public-key encryption has a gap: when the client receives "my public key is K", how does it know that K belongs to the site and not to an attacker? The answer is a *public key infrastructure* (PKI). A *certificate authority* (CA) checks that the applicant controls the name and signs a document that lists the name and the key. That document is an *X.509 certificate*. The Aadhaar analogy fits: a central authority (the root CA) authorises enrolment agencies (intermediate CAs), who issue the cards (leaf certificates), and a verifier checks the chain of authority and not only the face.

| X.509 field | Meaning |
|---|---|
| Subject, Subject Alternative Name (SAN) | the identity; browsers check the SAN list (DNS names) and ignore the old Common Name |
| Issuer | the CA that signed it |
| Validity (notBefore, notAfter) | the dates; public certificates now last at most about 13 months and the maximum is falling |
| Public key | the key being certified (RSA or ECDSA) |
| Basic Constraints | CA:TRUE for authorities, with an optional path length limit |
| Key Usage, Extended Key Usage | permitted uses, such as digitalSignature and serverAuth |
| CRL and OCSP locations, SCTs | where revocation is checked; proof of logging in Certificate Transparency |
| Signature | the issuer's signature over all the above |

<figure>
<svg viewBox="0 0 480 170" width="480"><defs><marker id="ich" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="ach" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><rect class="fill" x="20" y="10" width="190" height="36" rx="0" /><text class="lbl" x="115.0" y="27.0" text-anchor="middle">Campus Net Root CA</text><text class="sm" x="115.0" y="37.0" text-anchor="middle">self-signed; in the trust store</text><rect class="box" x="20" y="62" width="190" height="36" rx="0" /><text class="lbl" x="115.0" y="79.0" text-anchor="middle">Campus Net Issuing CA</text><text class="sm" x="115.0" y="89.0" text-anchor="middle">CA:TRUE, pathlen 0; sent by the server</text><rect class="box" x="20" y="114" width="190" height="36" rx="0" /><text class="lbl" x="115.0" y="131.0" text-anchor="middle">www.campus.example</text><text class="sm" x="115.0" y="141.0" text-anchor="middle">CA:FALSE, SAN, serverAuth; sent by the server</text><line class="acc" x1="115" y1="46" x2="115" y2="62" marker-end="url(#ach)"/><line class="acc" x1="115" y1="98" x2="115" y2="114" marker-end="url(#ach)"/><text class="sm" x="122" y="56" text-anchor="middle"></text><text class="sm" x="232" y="58" text-anchor="start">signs</text><text class="sm" x="232" y="110" text-anchor="start">signs</text><text class="sm" x="290" y="30" text-anchor="start">1. leaf name matches the SAN</text><text class="sm" x="290" y="50" text-anchor="start">2. dates valid today</text><text class="sm" x="290" y="70" text-anchor="start">3. leaf signature verifies with the issuer key</text><text class="sm" x="290" y="90" text-anchor="start">4. issuer signature verifies with the root key</text><text class="sm" x="290" y="110" text-anchor="start">5. root is trusted; CA flags and key usage allow it</text><text class="sm" x="290" y="130" text-anchor="start">6. not revoked (OCSP, stapling, CRL)</text><text class="lbl" x="290" y="14" text-anchor="start">Client validation, in order</text></svg>
<figcaption><b>Figure 9.4</b> The chain of trust. The browser holds only the root; the server sends the leaf and the intermediate.</figcaption>
</figure>

Browsers and operating systems ship a *trust store* of root certificates. A root is self-signed, so its authority comes from being in the store and not from any signature. Roots are kept offline and sign only a few *intermediate* CAs; the intermediates issue the leaf certificates. This limits the damage of a compromise, because an intermediate can be revoked without replacing the root in every device. The server sends its leaf and the intermediates, and the client builds the path to a root it holds (Figure 9.4).

Validation checks the six conditions in the figure. *Revocation* handles keys that leak before expiry. A *certificate revocation list* (CRL) is a signed list of serial numbers, large and slow to fetch. The *Online Certificate Status Protocol* (OCSP) asks the CA about one certificate, but leaks browsing to the CA and adds a round trip; hence *OCSP stapling*, in which the server fetches a signed, time-stamped response and attaches it to the handshake. The *must-staple* flag makes stapling mandatory. *Certificate Transparency* requires CAs to log every certificate in public append-only logs, whose signed timestamps (SCTs) appear in the certificate, so that a mis-issued certificate for campus.example can be detected by its owner. *Pinning*, in which an application accepts only a specific key, defends against rogue CAs but breaks easily when keys rotate; browsers have abandoned it for CT. *ACME*, the protocol of Let's Encrypt, automates issuance: the applicant proves control of a domain by serving a token over HTTP or by publishing a DNS record, receives a certificate valid for 90 days, and renews it by script. In *mutual TLS* (mTLS) the client also presents a certificate, which is how service-to-service traffic and managed devices authenticate.

::: lab
`LAB 9.1 · 30 MIN` Build a two-level CA for Campus Net and verify a server certificate. **Use only machines you own; unauthorised access to a computer system is an offence under sections 43 and 66 of the Indian IT Act 2000, and the attack labs of this chapter must never be run on a college or public network.**

```
openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -nodes \
  -keyout root.key -out root.crt -days 365 -subj "/O=Campus Net/CN=Campus Net Root CA"
# intermediate: CSR, then sign with the root using basicConstraints CA:TRUE,pathlen:0
# leaf: CSR for www.campus.example, sign with the intermediate, SAN in the extension file
openssl verify -CAfile root.crt leaf.crt
openssl verify -CAfile root.crt -untrusted int.crt leaf.crt
openssl s_server -accept 8446 -cert leaf.crt -cert_chain int.crt -key leaf.key -www &
openssl s_client -connect 127.0.0.1:8446 -servername www.campus.example \
  -CAfile root.crt -verify_hostname www.campus.example
```

```
error 20 at 0 depth lookup: unable to get local issuer certificate     (first verify)
leaf.crt: OK                                                            (with -untrusted int.crt)
 0 s:CN = www.campus.example        i:O = Campus Net, CN = Campus Net Issuing CA
 1 s:O = Campus Net, CN = Campus Net Issuing CA   i:O = Campus Net, CN = Campus Net Root CA
Verification: OK
```

Now start the server with `-cert leaf.crt` only (no `-cert_chain`): the client reports `verify error:num=21:unable to verify the first certificate`.

**What you should notice:** the leaf alone cannot be validated, because the client has the root but not the intermediate. Many browsers cache intermediates or fetch them from the AIA extension, so the same site works in a browser and fails in `curl` or a Java client; the fix is to send the full chain. Against a public site, `-showcerts` prints the same structure, with `s:` the subject and `i:` the issuer of each certificate.
:::

::: check
1. Why does a browser trust a root certificate that is self-signed? [^c9-4]
2. What does OCSP stapling remove? [^c9-5]
:::

[^c9-4]: It does not trust the signature; it trusts the root's presence in its trust store, which the vendor curates.
[^c9-5]: The client's separate query to the CA, which saves a round trip and stops the CA learning which sites the client visits.

:::
