::: {.p9}

::: pack
## Problem Set {#ps9}

Every interview question of this pillar is solved once, here, in the compact template: a 30-second answer first, then approach, answer, follow-ups and mistakes where they apply. The tags give the companies and round where the topic was reported, the difficulty (■□□ easy, ■■□ medium, ■■■ hard), and **S** when candidates reported the specific question or **T** when only the topic was reported and the wording is ours. The Campus Net examples are those of the chapter. Q9.1 to Q9.16 follow; Q9.17 to Q9.32 are in the continuation.

::: problems

::: q
### Q9.1 What is the CIA triad? Give a network example of a breach of each.
[CISCO · AMAZON · MICROSOFT · OA · ■□□ · S]{.meta}

[30-second answer: confidentiality (only authorised readers), integrity (no undetected change), availability (reachable when needed); a sniffed Telnet password, a rewritten download, and a SYN flood breach them in that order.]{.short}

**Answer.** Add authentication, authorisation, accounting and non-repudiation for who is acting; STRIDE maps each threat to the property it breaks ([9.1](#s9-1){.ref}). **Follow-ups.** Which property does encryption raise and which may it lower? (Confidentiality up; the ability of an IDS to inspect down.) **Mistakes.** Treating availability as an operations matter only: DoS is a security attack.
:::

::: q
### Q9.2 Symmetric versus asymmetric encryption: why does TLS use both?
[GOOGLE · CISCO · MICROSOFT · OA · ■□□ · S]{.meta}

[30-second answer: symmetric is fast but needs a shared key; asymmetric needs no shared secret but is about a thousand times slower, so TLS uses asymmetric methods (ECDHE, signatures) once to agree keys and prove identity, then AES-GCM or ChaCha20 for the data.]{.short}

**Answer.** Symmetric: one key, bulk data, AEAD modes give integrity too. Asymmetric: key pair, used for key agreement, signatures and certificates; RSA by factoring, ECC by discrete logarithm on curves, with smaller keys ([9.2](#s9-2){.ref}). **Mistakes.** Saying that TLS encrypts the data with RSA.
:::

::: q
### Q9.3 What is a hash? Why is a hash alone not enough to authenticate a message?
[AMAZON · CISCO · TECH-1 · ■□□ · S]{.meta}

[30-second answer: a hash maps any input to a fixed-size digest that is one-way and collision-resistant; but anyone can recompute it after altering the message, so authentication needs a key: HMAC.]{.short}

**Answer.** HMAC(K, m) = H((K ⊕ opad) ‖ H((K ⊕ ipad) ‖ m)) gives integrity and origin authentication to holders of K, and avoids the length-extension weakness of H(K ‖ m). A signature does the same without a shared key and adds non-repudiation. **Follow-ups.** Password storage needs a salted slow hash (Argon2, bcrypt), not HMAC. **Mistakes.** Using MD5 or SHA-1 for security.
:::

::: q
### Q9.4 What is a digital certificate and who signs it?
[CISCO · GOOGLE · TECH-1 · ■□□ · S]{.meta}

[30-second answer: an X.509 certificate binds a public key to a name (the SAN), and is signed by a certificate authority whose own certificate chains to a root in the client's trust store.]{.short}

**Answer.** Fields: subject, SAN, issuer, validity, public key, key usage, Basic Constraints, revocation pointers, SCTs, signature. The leaf is signed by an intermediate CA; the intermediate by the root ([9.3](#s9-3){.ref}). **Follow-ups.** How is a certificate obtained? (CSR, domain validation, ACME.) **Mistakes.** Thinking that a self-signed certificate is weaker in cryptography; it is simply untrusted by third parties.
:::

::: q
### Q9.5 What is the implicit rule at the end of every ACL? Where are standard and extended ACLs placed?
[CISCO · JUNIPER · AMAZON · OA · ■□□ · S]{.meta}

[30-second answer: an implicit `deny any`; standard ACLs (source only) go close to the destination, extended ACLs close to the source.]{.short}

**Answer.** The list is read top to bottom, the first match decides, and nothing matching means deny. A standard ACL near the source would block that source's traffic to every destination, whereas an extended ACL can name the destination, so dropping early saves bandwidth ([9.5](#s9-5){.ref}). The IOS syntax is in [4.13](#s4-13){.ref}. **Follow-ups.** Inbound versus outbound; an outbound ACL does not filter router-originated packets. **Mistakes.** A list of denies with no final permit.
:::

::: q
### Q9.6 Compute the wildcard mask for 172.16.32.0/20.
[CISCO · JUNIPER · OA · ■□□ · S]{.meta}

[30-second answer: 0.0.15.255, matching 172.16.32.0 to 172.16.47.255.]{.short}

**Approach.** The wildcard is 255 minus each subnet-mask octet. /20 is 255.255.240.0, so the wildcard is 0.0.(255 − 240).255 = 0.0.15.255. **Check.** The block size in the third octet is 256 − 240 = 16, starting at 32 (a multiple of 16), so the third octet runs 32 to 47. The method is that of Figure 9.8. **Mistakes.** Writing the subnet mask in the ACL, or choosing a network address that is not on a block boundary.
:::

::: q
### Q9.7 Stateless versus stateful firewall.
[CISCO · JUNIPER · AMAZON · NOKIA · TECH-1 · ■□□ · S]{.meta}

[30-second answer: a stateless filter judges each packet alone by header fields; a stateful firewall keeps a session table and automatically admits packets that belong to a permitted flow, in particular the replies.]{.short}

**Answer.** The session entry holds the 5-tuple, state, timers; for TCP it checks the handshake and sequence window. Stateful gives safer defaults and simpler rules but costs memory per flow and breaks under asymmetric routing; the ACL is fast and hardware-based but cannot recognise replies ([9.6](#s9-6){.ref}). **Mistakes.** Calling `established` in an ACL stateful; it matches only the ACK or RST flag.
:::

::: q
### Q9.8 IDS versus IPS.
[CISCO · NOKIA · TECH-1 · ■□□ · T]{.meta}

[30-second answer: an IDS watches a copy of the traffic and alerts; an IPS sits inline and can drop or reset flows, at the price that a false positive or a failure interrupts traffic.]{.short}

**Answer.** Detection by signature (known patterns, few false positives) or by anomaly (baseline, finds novel attacks, more noise). Placement: SPAN or TAP for the IDS, in the path for the IPS, with fail-open or fail-closed decided in advance ([9.13](#s9-13){.ref}). **Mistakes.** Putting an IPS in the path without a bypass.
:::

::: q
### Q9.9 Walk me through the TLS 1.3 handshake. Where does encryption start?
[GOOGLE · MICROSOFT · AMAZON · TECH-1 · ■■□ · S]{.meta}

[30-second answer: ClientHello with a key share; ServerHello with its key share, after which everything is encrypted (EncryptedExtensions, Certificate, CertificateVerify, Finished); client Finished; application data. One round trip.]{.short}

**Answer.** (i) ClientHello: versions, suites, key share, SNI, ALPN. (ii) ServerHello: chosen suite and share; both derive handshake keys by ECDHE and HKDF. (iii) Server sends EncryptedExtensions, the certificate chain, a CertificateVerify signature over the transcript and a Finished MAC. (iv) The client verifies and sends Finished with the first request under application keys ([9.4](#s9-4){.ref}, Figure 9.5). **Follow-ups.** HelloRetryRequest when the guessed group is wrong; mutual TLS adds CertificateRequest. **Mistakes.** Saying that encryption starts after Finished; it starts after ServerHello.
:::

::: q
### Q9.10 Why is TLS 1.3 one round trip instead of two? What was removed from 1.2, and why?
[GOOGLE · MICROSOFT · AMAZON · TECH-1 · ■■□ · S]{.meta}

[30-second answer: the client sends its key share in the first message, so the server can finish key agreement in its first reply. Removed: static RSA key exchange (no forward secrecy), renegotiation, compression and weak ciphers (CBC, RC4, 3DES).]{.short}

**Answer.** In 1.2 the client had to wait for the server's chosen parameters before sending its key exchange, which cost the second round trip. Version 1.3 allows only (EC)DHE or PSK, five AEAD suites, and encrypts the certificate. The table in [9.4](#s9-4){.ref} lists the differences. **Mistakes.** Forgetting that TCP's handshake comes first: total time to first byte is still 2 RTT before the request is answered.
:::

::: q
### Q9.11 What is forward secrecy and how does ECDHE provide it?
[GOOGLE · MICROSOFT · AMAZON · TECH-2 · ■■□ · S]{.meta}

[30-second answer: past sessions stay secret even if the server's long-term key is stolen later, because the session keys come from ephemeral Diffie-Hellman values that are deleted after use.]{.short}

**Answer.** With RSA key transport the client encrypts the secret to the server's certificate key, so one stolen key decrypts every recorded session. With ECDHE both sides generate a fresh key pair per session; the certificate key only signs the handshake, and never protects a secret. A recorded session cannot be decrypted without the discarded ephemeral values ([9.2](#s9-2){.ref}). **Follow-ups.** Session tickets can weaken it if their keys are long-lived. **Mistakes.** Thinking forward secrecy stops a live man in the middle; authentication does that.
:::

::: q
### Q9.12 What is 0-RTT and why is it dangerous for non-idempotent requests?
[GOOGLE · AMAZON · TECH-2 · ■■□ · S]{.meta}

[30-second answer: on resumption the client sends application data in its first flight under a key from the earlier PSK, saving a round trip; an attacker can replay that flight, so a server may process it twice.]{.short}

**Answer.** Early data has no replay protection and no forward secrecy of its own. A replayed GET is harmless; a replayed "transfer 1,000 rupees" is not. Mitigations: accept 0-RTT only for idempotent methods, one-time tickets, a strike register in the server, and an `Early-Data` header so that the application can reject with 425 ([9.4](#s9-4){.ref}). **Mistakes.** Enabling it on a payments endpoint.
:::

::: q
### Q9.13 How does a browser validate a certificate? What happens if the intermediate is missing?
[GOOGLE · MICROSOFT · CISCO · TECH-1 · ■■□ · S]{.meta}

[30-second answer: it builds a chain from the leaf to a trusted root, checking signatures, validity dates, name against the SAN, key usage and revocation; with a missing intermediate the path cannot be built and strict clients fail.]{.short}

**Answer.** The six checks of Figure 9.4. Some browsers cache intermediates or fetch them through the AIA extension, so the site appears fine in a browser and fails in `curl`, Java or a mobile library with `unable to verify the first certificate`. The fix is to serve the full chain, leaf first ([9.3](#s9-3){.ref}, Lab 9.1). **Follow-ups.** An expired leaf and a hostname mismatch give different errors; the client aborts with a fatal alert. **Mistakes.** Installing the root on the server instead of the intermediate.
:::

::: q
### Q9.14 Explain IPsec tunnel versus transport mode and AH versus ESP. Why does AH not work through NAT?
[CISCO · JUNIPER · NOKIA · TECH-1 · ■■□ · S]{.meta}

[30-second answer: transport mode protects the payload and keeps the original IP header (host to host); tunnel mode encrypts the whole packet inside a new IP header (gateway to gateway). ESP (protocol 50) encrypts and authenticates; AH (51) authenticates only, and its integrity check covers the outer IP header, so NAT rewriting the address breaks it.]{.short}

**Answer.** Figure 9.10 shows the formats. ESP in tunnel mode is the norm; NAT traversal wraps ESP in UDP 4500 because ESP has no ports for a NAT to translate ([9.7](#s9-7){.ref}). **Mistakes.** Calling AH "more secure" for authenticating more of the header.
:::

::: q
### Q9.15 Explain IKEv1 Phase 1 and Phase 2. How does IKEv2 differ? How many messages does each use?
[CISCO · JUNIPER · NOKIA · TECH-2 · ■■□ · S]{.meta}

[30-second answer: IKEv1 Phase 1 builds the IKE SA (6 messages in main mode, 3 in aggressive) and Phase 2 quick mode builds the IPsec SAs (3 messages); IKEv2 does both in 4 messages, IKE_SA_INIT and IKE_AUTH, with CREATE_CHILD_SA for rekeying.]{.short}

**Answer.** Aggressive mode is faster but sends identities in clear and exposes a hash for offline PSK guessing. IKEv2 adds built-in liveness, NAT-T and EAP, and a simpler state machine (Figure 9.11, [9.7](#s9-7){.ref}). **Follow-ups.** What does PFS add? (A fresh DH exchange per Child SA.) **Mistakes.** Stating nine messages for IKEv2.
:::

::: q
### Q9.16 A site-to-site VPN shows Phase 1 up, but no traffic passes. What do you check?
[CISCO · JUNIPER · NOKIA · TECH-2 · ■■□ · S]{.meta}

[30-second answer: Phase 1 only proves that the peers authenticated; check the Child SA (selectors or crypto ACL mirroring, transform set, PFS group), the routing into the tunnel, NAT exemption, and the encaps/decaps counters.]{.short}

**Approach.** (i) `show crypto ikev2 sa` then `show crypto ipsec sa`: are there inbound and outbound SPIs, and do both counters rise? Encaps rising with zero decaps means the far end does not return. (ii) Selectors: 172.16.50.0/24 on one side and /25 on the other gives `TS_UNACCEPTABLE`. (iii) Transform and PFS mismatches show as `NO_PROPOSAL_CHOSEN`. (iv) A route or interface-bound policy must send the traffic into the tunnel. (v) A NAT rule must exempt VPN traffic, so that it is not translated before encryption. (vi) Reduce MSS if large packets die while pings work ([9.8](#s9-8){.ref}). The full case is [Case 15](#c11-15){.ref}. **Mistakes.** Concluding "the tunnel is up" from Phase 1.
:::

:::
:::

:::
