::: {.p9}

## [9.4]{.sec}The TLS 1.3 handshake, step by step [Must · ■■■]{.tag} {#s9-4}

::: bigidea
TLS 1.3 completes in one round trip because the client guesses the key-exchange group and sends its key share in the very first message, so the server can derive keys and start encrypting at once.
:::

*Transport Layer Security* (TLS) gives a TCP connection confidentiality, integrity and server authentication (RFC 8446). It runs above TCP, so the TCP handshake of [Pillar 3](#ch3){.ref} comes first. Think of booking a sealed conversation: in version 1.3 you bring your half of the room key in your first sentence, so the receptionist can lock the door at once. The handshake has four goals: agree on a cipher suite, agree on keys by ECDHE (Section 9.2), prove the server's identity with a certificate (Section 9.3), and confirm that nobody altered the negotiation.

<figure>
<svg viewBox="0 0 480 282" width="480"><defs><marker id="itl" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="atl" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><rect class="fill" x="80" y="90" width="320" height="132" rx="0" /><text class="lbl" x="90" y="14" text-anchor="middle">Client</text><line class="lg" x1="90" y1="20" x2="90" y2="270" /><text class="lbl" x="390" y="14" text-anchor="middle">Server</text><line class="lg" x1="390" y1="20" x2="390" y2="270" /><line class="ln" x1="92" y1="38" x2="388" y2="38" marker-end="url(#itl)"/><text class="sm" x="240.0" y="33" text-anchor="middle">ClientHello: versions, cipher suites, key_share (X25519), SNI, ALPN</text><line class="acc" x1="388" y1="60" x2="92" y2="60" marker-end="url(#atl)"/><text class="sm" x="240.0" y="55" text-anchor="middle">ServerHello: chosen suite, key_share</text><text class="sm" x="240.0" y="82" text-anchor="middle">both sides now derive handshake traffic keys from the ECDHE secret</text><line class="ln" x1="388" y1="104" x2="92" y2="104" marker-end="url(#itl)"/><text class="sm" x="240.0" y="99" text-anchor="middle">EncryptedExtensions</text><line class="ln" x1="388" y1="126" x2="92" y2="126" marker-end="url(#itl)"/><text class="sm" x="240.0" y="121" text-anchor="middle">Certificate (chain)</text><line class="ln" x1="388" y1="148" x2="92" y2="148" marker-end="url(#itl)"/><text class="sm" x="240.0" y="143" text-anchor="middle">CertificateVerify (signature over the transcript)</text><line class="ln" x1="388" y1="170" x2="92" y2="170" marker-end="url(#itl)"/><text class="sm" x="240.0" y="165" text-anchor="middle">Finished (MAC over the transcript)</text><text class="sm" x="240.0" y="192" text-anchor="middle">server may already send application data (0.5-RTT)</text><line class="ln" x1="92" y1="214" x2="388" y2="214" marker-end="url(#itl)"/><text class="sm" x="240.0" y="209" text-anchor="middle">Finished</text><line class="acc" x1="92" y1="236" x2="388" y2="236" marker-end="url(#atl)"/><text class="sm" x="240.0" y="231" text-anchor="middle">Application data (application traffic keys)</text><line class="acc" x1="388" y1="258" x2="92" y2="258" marker-end="url(#atl)"/><text class="sm" x="240.0" y="253" text-anchor="middle">Application data</text><text class="sm" x="470" y="52" text-anchor="middle"></text></svg>
<figcaption><b>Figure 9.5</b> The TLS 1.3 full handshake. The shaded part is encrypted; the application can send data after its own Finished.</figcaption>
</figure>

1. **ClientHello.** The client lists the versions it accepts (`supported_versions`), its cipher suites, the groups it supports and, as a guess, a *key share* for one of them, usually an X25519 public value. Further extensions carry the *server name indication* (SNI), the signature algorithms it accepts and ALPN, the application protocol wanted (`h2`, `http/1.1`). The message is in clear.
2. **ServerHello.** The server picks one suite and answers with its own key share. From this moment both sides hold the ECDHE shared secret and, through the key schedule (HKDF), derive the *handshake traffic keys*. Everything the server sends from now on is encrypted. A legacy ChangeCipherSpec record is also sent, only so that middleboxes that expect the TLS 1.2 shape do not drop the connection.
3. **EncryptedExtensions.** The remaining negotiated parameters, such as the chosen ALPN protocol, now travel encrypted.
4. **Certificate.** The server's leaf and intermediates, encrypted, so a passive observer no longer sees which certificate was presented.
5. **CertificateVerify.** A signature, made with the certificate's private key, over a hash of the whole handshake so far. This is the proof of identity: only the key holder can produce it, and it binds the key exchange to the certificate, which defeats a man in the middle who relays the ECDHE values.
6. **Finished (server).** A MAC over the transcript under a key from the handshake secret. It confirms that both sides saw the same messages, so a downgrade attempt would be detected. The server derives the *application traffic keys* and may send data immediately.
7. **Finished (client).** The client verifies items 5 and 6, then sends its own Finished and its first request under the application keys. One round trip has elapsed.

If the server does not support the group guessed in the key share, it replies with a *HelloRetryRequest* naming a group it accepts, and the client sends a new ClientHello: this costs one extra round trip. A client certificate (mutual TLS) is requested by a CertificateRequest message after EncryptedExtensions and answered by the client's Certificate and CertificateVerify before its Finished.

::: deep
**The key schedule in four lines.** TLS 1.3 chains HKDF extractions. (i) The *early secret* comes from the PSK (zeros if there is none). (ii) The *handshake secret* mixes in the ECDHE shared secret; from it, hashes of the transcript up to ServerHello give the client and server *handshake traffic secrets*. (iii) The *master secret* is extracted next; hashes of the transcript up to the server's Finished give the *application traffic secrets*. (iv) Each direction expands its traffic secret into a record key and IV, and into a *finished key* for the Finished MAC. Because every secret depends on the transcript, a tampered ClientHello changes all later keys and the Finished check fails.
:::

*Resumption* avoids the full handshake. After the first connection the server sends a *NewSessionTicket* that carries a pre-shared key (PSK) value. On a later connection the client offers it in the ClientHello; if accepted, no certificate is exchanged, and with a fresh ECDHE share forward secrecy is kept. With a PSK the client may also send *0-RTT early data* in its first flight, encrypted under a key from the PSK. This gives zero extra round trips, but early data has no forward secrecy and can be *replayed*: an attacker records the first flight and sends it again, and the server may process it twice. Hence servers should accept 0-RTT only for idempotent requests (a GET, never a payment).

<figure>
<svg viewBox="0 0 480 170" width="480"><defs><marker id="itv" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="atv" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><text class="lbl" x="115" y="12" text-anchor="middle">TLS 1.2</text><line class="lg" x1="4" y1="18" x2="4" y2="150" /><line class="lg" x1="226" y1="18" x2="226" y2="150" /><line class="ln" x1="6" y1="38" x2="224" y2="38" marker-end="url(#itv)"/><text class="sm" x="115" y="35" text-anchor="middle">ClientHello</text><line class="ln" x1="224" y1="58" x2="6" y2="58" marker-end="url(#itv)"/><text class="sm" x="115" y="55" text-anchor="middle">ServerHello, Certificate, KeyExchange, Done</text><line class="ln" x1="6" y1="78" x2="224" y2="78" marker-end="url(#itv)"/><text class="sm" x="115" y="75" text-anchor="middle">KeyExchange, ChangeCipherSpec, Finished</text><line class="ln" x1="224" y1="98" x2="6" y2="98" marker-end="url(#itv)"/><text class="sm" x="115" y="95" text-anchor="middle">ChangeCipherSpec, Finished</text><line class="acc" x1="6" y1="118" x2="224" y2="118" marker-end="url(#atv)"/><text class="sm" x="115" y="115" text-anchor="middle">request</text><line class="acc" x1="224" y1="138" x2="6" y2="138" marker-end="url(#atv)"/><text class="sm" x="115" y="135" text-anchor="middle">response</text><text class="lbl" x="115" y="164" text-anchor="middle">2 RTT; certificate in clear</text><text class="lbl" x="359" y="12" text-anchor="middle">TLS 1.3</text><line class="lg" x1="248" y1="18" x2="248" y2="150" /><line class="lg" x1="470" y1="18" x2="470" y2="150" /><line class="ln" x1="250" y1="38" x2="468" y2="38" marker-end="url(#itv)"/><text class="sm" x="359" y="35" text-anchor="middle">ClientHello + key_share</text><line class="ln" x1="468" y1="58" x2="250" y2="58" marker-end="url(#itv)"/><text class="sm" x="359" y="55" text-anchor="middle">ServerHello ... Finished (encrypted)</text><line class="acc" x1="250" y1="78" x2="468" y2="78" marker-end="url(#atv)"/><text class="sm" x="359" y="75" text-anchor="middle">Finished + request</text><line class="acc" x1="468" y1="98" x2="250" y2="98" marker-end="url(#atv)"/><text class="sm" x="359" y="95" text-anchor="middle">response</text><text class="lbl" x="359" y="164" text-anchor="middle">1 RTT; certificate encrypted</text></svg>
<figcaption><b>Figure 9.6</b> Round trips before the first request: two for TLS 1.2, one for TLS 1.3 (each after the TCP handshake).</figcaption>
</figure>

| | TLS 1.2 | TLS 1.3 |
|---|---|---|
| Round trips before the request | 2 | 1 (0 with PSK and early data) |
| Key exchange | RSA key transport or (EC)DHE | (EC)DHE or PSK only |
| Forward secrecy | only with DHE suites | always, for certificate-based handshakes |
| Certificate visible to observers | yes | no, it is encrypted |
| Cipher suites | many, including CBC, RC4, 3DES | five AEAD suites (AES-GCM, ChaCha20-Poly1305, AES-CCM) |
| Renegotiation, compression | present, and a source of attacks | removed |
| Signature over handshake | ServerKeyExchange only | CertificateVerify over the entire transcript |

::: trap
*Claim:* HTTPS hides which site a user visits. *Why it is wrong:* the SNI in the ClientHello is plaintext unless Encrypted Client Hello (ECH) is used, and the DNS lookup may also leak the name. *Correct statement:* TLS 1.3 hides the certificate and the content; it hides the destination name only with ECH and encrypted DNS (Section 9.11), and the destination address is always visible.
:::

::: lab
`LAB 9.2 · 20 MIN` Watch the messages of TLS 1.3 with `-msg`, using the server of Lab 9.1.

```
openssl s_client -connect 127.0.0.1:8446 -servername www.campus.example \
  -CAfile root.crt -tls1_3 -msg 2>&1 | grep 'Handshake \['
```

(Add `-tls1_2` for the TLS 1.2 contrast: the server's certificate then appears in clear, and a `ServerKeyExchange` message precedes `ServerHelloDone`.)

```
>>> TLS 1.3, Handshake [length 00f7], ClientHello
<<< TLS 1.3, Handshake [length 007a], ServerHello
<<< TLS 1.3, Handshake [length 0006], EncryptedExtensions
<<< TLS 1.3, Handshake [length 03cc], Certificate
<<< TLS 1.3, Handshake [length 004e], CertificateVerify
<<< TLS 1.3, Handshake [length 0034], Finished
>>> TLS 1.3, Handshake [length 0034], Finished
```

For a browser-style capture of an HTTPS request, set `SSLKEYLOGFILE=$HOME/keys.log`, run `curl https://www.campus.example/`, capture with `tcpdump -w tls.pcap port 443`, and give Wireshark the log under Preferences, Protocols, TLS, "(Pre)-Master-Secret log filename".

**What you should notice:** only ClientHello and ServerHello are readable on the wire; the other five messages sit in encrypted records, and OpenSSL prints them because it holds the keys. The `Certificate` is by far the longest (0x3cc = 972 bytes). With the key log, Wireshark shows the same list under each encrypted record, which is the paper variant of this lab.
:::

::: lens
[GOOGLE · MICROSOFT · AMAZON]{.co}

"Walk me through the TLS 1.3 handshake. Where does encryption start?" Give the seven steps above, say that encryption starts immediately after the ServerHello, and explain why this saves a round trip. Expect: "What was removed from 1.2?" (RSA key transport, renegotiation, weak ciphers), "What is 0-RTT's risk?" (replay) and "What if the certificate is expired or names another host?" (the client aborts at validation with a fatal alert).
:::

## [9.5]{.sec}ACLs: stateless packet filtering [Must · ■■□]{.tag} {#s9-5}

::: bigidea
An access control list judges every packet on its own header fields against an ordered list, so it is fast and simple, but it has no memory of conversations and therefore cannot know that a packet is a reply.
:::

An *access control list* (ACL) is an ordered list of permit and deny rules, applied to an interface in one direction. Think of a bouncer with a printed list: he reads it from the top, stops at the first line that names you, and if you are not on it you are out. Four rules govern every ACL. (i) The list is read top to bottom and the *first match* decides; later lines are never consulted. (ii) An invisible *implicit deny any* ends every list, so a list of denies alone blocks everything. (iii) An ACL examines only packets passing through the interface in the direction applied: an outbound ACL does not filter traffic that the router itself originates. (iv) One ACL may be applied per interface, per direction and per protocol (IPv4 and IPv6 separately). The syntax, numbering and verification commands are in [Section 4.13](#s4-13){.ref}; here we concentrate on design.

| | Standard ACL | Extended ACL |
|---|---|---|
| Matches | source address only | protocol, source, destination, ports, flags |
| Numbers (classic) | 1 to 99, 1300 to 1999 | 100 to 199, 2000 to 2699 |
| Placement | close to the **destination** | close to the **source** |
| Reason | it cannot name the destination, so near the source it would block the source's other traffic as well | it can name everything, so dropping early saves bandwidth on the path |

The placement rule follows from what each type can express. A standard ACL that denies ENG from reaching the servers, if placed on ENG's own interface, would also deny ENG access to the Internet, because it sees only the source. Placed on the server-facing port, it affects only what reaches the servers. An extended ACL has no such problem and is better near the source, where it saves the transit links and the core routers the work (Figure 9.7).

<figure>
<svg viewBox="0 0 480 150" width="480"><defs><marker id="iap" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="aap" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><rect class="box" x="10" y="20" width="100" height="30" rx="0" /><text class="lbl" x="60.0" y="34.0" text-anchor="middle">ENG VLAN 20</text><text class="sm" x="60.0" y="44.0" text-anchor="middle">192.168.20.0/24</text><rect class="box" x="10" y="90" width="100" height="30" rx="0" /><text class="lbl" x="60.0" y="104.0" text-anchor="middle">SALES VLAN 10</text><text class="sm" x="60.0" y="114.0" text-anchor="middle">192.168.10.0/24</text><circle class="box" cx="240" cy="70" r="22"/><path class="ln" d="M226,56 L254,84 M254,56 L226,84"/><text class="lbl" x="240" y="108" text-anchor="middle">R1</text><rect class="box" x="370" y="55" width="100" height="30" rx="0" /><text class="lbl" x="420.0" y="69.0" text-anchor="middle">Servers</text><text class="sm" x="420.0" y="79.0" text-anchor="middle">10.0.0.0/24</text><line class="ln" x1="110" y1="35" x2="220" y2="62" /><line class="ln" x1="110" y1="105" x2="220" y2="80" /><line class="ln" x1="262" y1="70" x2="370" y2="70" /><rect class="hl" x="138" y="36" width="66" height="14" rx="0" /><text class="sm" x="171" y="46" text-anchor="middle">extended, in</text><rect class="hl" x="138" y="93" width="66" height="14" rx="0" /><text class="sm" x="171" y="103" text-anchor="middle">extended, in</text><rect class="hl" x="290" y="56" width="62" height="14" rx="0" /><text class="sm" x="321" y="66" text-anchor="middle">standard, out</text><text class="sm" x="240" y="140" text-anchor="middle">Extended: close to the source, drops early. Standard (source only): close to the destination.</text></svg>
<figcaption><b>Figure 9.7</b> ACL placement at R1 in Campus Net: the extended ACL near the source, the standard ACL near the destination.</figcaption>
</figure>

A *wildcard mask* says which address bits must match: 0 means "must match", 1 means "ignore". It is the inverse of the subnet mask for a contiguous block, so one writes 255 minus each mask octet. Because it is an independent bit pattern, it can also be discontiguous, which a subnet mask cannot: `192.168.1.0 0.0.254.255` matches every address with an odd third octet and any fourth octet, a trick used to select odd-numbered VLAN subnets. Note that a wildcard mask is not a subnet mask; confusing the two gives a rule that matches a different set of addresses.

<figure>
<svg viewBox="0 0 480 160" width="480"><defs><marker id="iwc" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="awc" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><text class="sm" x="170" y="14" text-anchor="middle">octet 1</text><text class="sm" x="220" y="14" text-anchor="middle">octet 2</text><text class="sm" x="305" y="14" text-anchor="middle">octet 3 (bits)</text><text class="sm" x="390" y="14" text-anchor="middle">octet 4</text><text class="lbl" x="8" y="37" text-anchor="start">Address</text><rect class="box" x="150" y="22" width="40" height="22" rx="0" /><text class="lbl" x="170.0" y="36.0" text-anchor="middle">192</text><rect class="box" x="200" y="22" width="40" height="22" rx="0" /><text class="lbl" x="220.0" y="36.0" text-anchor="middle">168</text><rect class="box" x="250" y="22" width="14" height="22" rx="0" /><text class="mono" x="257" y="37" text-anchor="middle">0</text><rect class="box" x="264" y="22" width="14" height="22" rx="0" /><text class="mono" x="271" y="37" text-anchor="middle">0</text><rect class="box" x="278" y="22" width="14" height="22" rx="0" /><text class="mono" x="285" y="37" text-anchor="middle">0</text><rect class="box" x="292" y="22" width="14" height="22" rx="0" /><text class="mono" x="299" y="37" text-anchor="middle">0</text><rect class="box" x="306" y="22" width="14" height="22" rx="0" /><text class="mono" x="313" y="37" text-anchor="middle">1</text><rect class="box" x="320" y="22" width="14" height="22" rx="0" /><text class="mono" x="327" y="37" text-anchor="middle">0</text><rect class="box" x="334" y="22" width="14" height="22" rx="0" /><text class="mono" x="341" y="37" text-anchor="middle">0</text><rect class="box" x="348" y="22" width="14" height="22" rx="0" /><text class="mono" x="355" y="37" text-anchor="middle">0</text><rect class="box" x="370" y="22" width="40" height="22" rx="0" /><text class="lbl" x="390.0" y="36.0" text-anchor="middle">0</text><text class="lbl" x="8" y="65" text-anchor="start">Subnet mask</text><rect class="box" x="150" y="50" width="40" height="22" rx="0" /><text class="lbl" x="170.0" y="64.0" text-anchor="middle">255</text><rect class="box" x="200" y="50" width="40" height="22" rx="0" /><text class="lbl" x="220.0" y="64.0" text-anchor="middle">255</text><rect class="box" x="250" y="50" width="14" height="22" rx="0" /><text class="mono" x="257" y="65" text-anchor="middle">1</text><rect class="box" x="264" y="50" width="14" height="22" rx="0" /><text class="mono" x="271" y="65" text-anchor="middle">1</text><rect class="box" x="278" y="50" width="14" height="22" rx="0" /><text class="mono" x="285" y="65" text-anchor="middle">1</text><rect class="box" x="292" y="50" width="14" height="22" rx="0" /><text class="mono" x="299" y="65" text-anchor="middle">1</text><rect class="box" x="306" y="50" width="14" height="22" rx="0" /><text class="mono" x="313" y="65" text-anchor="middle">1</text><rect class="box" x="320" y="50" width="14" height="22" rx="0" /><text class="mono" x="327" y="65" text-anchor="middle">1</text><rect class="box" x="334" y="50" width="14" height="22" rx="0" /><text class="mono" x="341" y="65" text-anchor="middle">0</text><rect class="box" x="348" y="50" width="14" height="22" rx="0" /><text class="mono" x="355" y="65" text-anchor="middle">0</text><rect class="box" x="370" y="50" width="40" height="22" rx="0" /><text class="lbl" x="390.0" y="64.0" text-anchor="middle">0</text><text class="lbl" x="8" y="93" text-anchor="start">Wildcard (255 - mask)</text><rect class="fill" x="150" y="78" width="40" height="22" rx="0" /><text class="lbl" x="170.0" y="92.0" text-anchor="middle">0</text><rect class="fill" x="200" y="78" width="40" height="22" rx="0" /><text class="lbl" x="220.0" y="92.0" text-anchor="middle">0</text><rect class="box" x="250" y="78" width="14" height="22" rx="0" /><text class="mono" x="257" y="93" text-anchor="middle">0</text><rect class="box" x="264" y="78" width="14" height="22" rx="0" /><text class="mono" x="271" y="93" text-anchor="middle">0</text><rect class="box" x="278" y="78" width="14" height="22" rx="0" /><text class="mono" x="285" y="93" text-anchor="middle">0</text><rect class="box" x="292" y="78" width="14" height="22" rx="0" /><text class="mono" x="299" y="93" text-anchor="middle">0</text><rect class="box" x="306" y="78" width="14" height="22" rx="0" /><text class="mono" x="313" y="93" text-anchor="middle">0</text><rect class="box" x="320" y="78" width="14" height="22" rx="0" /><text class="mono" x="327" y="93" text-anchor="middle">0</text><rect class="hl" x="334" y="78" width="14" height="22" rx="0" /><text class="mono" x="341" y="93" text-anchor="middle">1</text><rect class="hl" x="348" y="78" width="14" height="22" rx="0" /><text class="mono" x="355" y="93" text-anchor="middle">1</text><rect class="fill" x="370" y="78" width="40" height="22" rx="0" /><text class="lbl" x="390.0" y="92.0" text-anchor="middle">255</text><rect class="accf" x="250" y="110" width="84" height="3" rx="0" /><text class="sm" x="292" y="124" text-anchor="middle">must match (6 bits)</text><text class="sm" x="240" y="136" text-anchor="middle">free: the last 2 bits (third octet 8 to 11) and all of octet 4</text><text class="lbl" x="240" y="152" text-anchor="middle">Result: 192.168.8.0 0.0.3.255</text></svg>
<figcaption><b>Figure 9.8</b> Wildcard mask for 192.168.8.0/22. Only the first 22 bits must match; the last 10 are free.</figcaption>
</figure>

::: example
**An ACL for ENG.** Policy: ENG (192.168.20.0/24) may use HTTP and HTTPS to the web server 10.0.0.80 and may ping it; everything else addressed to the server network 10.0.0.0/24 is denied; all other traffic is permitted.

1. Choose an extended ACL because the policy names protocols, ports and a destination. Place it *inbound* on R1's ENG-facing interface (close to the source). Replies from the server enter R1 on another interface and are never filtered by this list, so no `established` line is needed.
2. Order the lines from the most specific to the most general. The permits for the server come first; the deny for the whole server network follows; the permit for everything else is last.
3. Write the wildcard for 10.0.0.0/24 as 0.0.0.255 and for a single host as `host`.

```
ip access-list extended ENG-IN
 10 permit tcp 192.168.20.0 0.0.0.255 host 10.0.0.80 eq 80
 20 permit tcp 192.168.20.0 0.0.0.255 host 10.0.0.80 eq 443
 30 permit icmp 192.168.20.0 0.0.0.255 host 10.0.0.80 echo
 40 deny   ip any 10.0.0.0 0.0.0.255
 50 permit ip any any
```

4. Test it by tracing eight flows through the list, as in the table.

| Flow from ENG | First match | Result |
|---|---|---|
| TCP 443 to 10.0.0.80 | line 20 | permit |
| TCP 22 to 10.0.0.80 | line 40 | deny |
| ping 10.0.0.80 | line 30 | permit |
| ping 10.0.0.81 | line 40 | deny |
| TCP 443 to 10.0.0.81 | line 40 | deny |
| UDP 53 to 8.8.8.8 | line 50 | permit |
| TCP 443 to SALES host 192.168.10.5 | line 50 | permit (intended? the policy never mentioned SALES) |
| TCP 443 to 10.0.0.80 with source 192.168.99.9 | line 40 | deny (not in ENG's range) |

[Result: the list implements the policy; the seventh row shows that a final `permit ip any any` makes the list a deny-list, so every unlisted path is open.]{.result}
:::

::: trap
*Claim:* adding `permit ip any any` early "just in case" does no harm. *Why it is wrong:* the first match decides, so every line after it becomes dead code. *Correct statement:* place specific lines first, the general permit last, and check the hit counts (`show access-lists`), since a line with zero matches may be shadowed.
:::

Three limits follow from statelessness. First, return traffic must be allowed explicitly: an inbound ACL on an Internet-facing interface needs `permit tcp any any established` (which matches ACK or RST, and so is easily forged) or a stateful device. Second, an ACL cannot follow protocols that open dynamic ports, such as active FTP. Third, an ACL cannot see the application. On management lines it works well: `access-class 10 in` on the VTY lines with a standard list limits who may log in. IPv6 lists end with implicit permits for neighbour discovery before the final deny, since ND replaces ARP. ACLs are executed in hardware (TCAM) on switches and routers, at line rate, which is why they remain the first filter for DDoS traffic and for Layer-3 segmentation, while the firewall of Section 9.6 handles sessions.

::: lens
[CISCO · JUNIPER · AMAZON]{.co}

"Write an ACL that lets one VLAN reach a web server and nothing else" is asked at the whiteboard. A strong answer states the placement and direction first, orders the lines specific to general, writes the wildcard correctly, mentions the implicit deny, and says how to verify (hit counters). Expect: "Where would you put it if it were standard?" and "How do replies get back?"
:::

::: check
1. Where is a standard ACL placed, and why? [^c9-6]
2. An ACL consists of three `deny` lines for specific hosts. What does it permit? [^c9-7]
3. What is the wildcard mask for a single host? [^c9-8]
:::

[^c9-6]: Close to the destination, because it matches only the source and would otherwise block that source's traffic to every other destination.
[^c9-7]: Nothing: the implicit `deny any` blocks all other packets.
[^c9-8]: 0.0.0.0, written `host x.x.x.x`.

## [9.6]{.sec}Stateful firewalls, NGFW and NAT interplay [Must · ■■□]{.tag} {#s9-6}

::: bigidea
A stateful firewall remembers each connection in a session table, so it can allow replies automatically and drop everything that does not belong to a permitted conversation.
:::

A *stateful firewall* creates an entry when it permits the first packet of a flow and then admits packets that match it in either direction. The entry holds the *5-tuple* (protocol, source and destination address, source and destination port), the connection state, a timer and counters. For TCP the firewall follows the handshake and the sequence-number window, so that a forged RST or out-of-window segment is dropped; for UDP and ICMP, which have no state, it keeps a pseudo-session with a short idle timeout. The housing-society guard analogy applies: he remembers that you invited the delivery rider, so he lets him leave again without checking the list, whereas a stateless guard (the ACL) re-reads the list for every passage.

| Protocol | Inside address | Translated address | Destination | State | Idle timer |
|---|---|---|---|---|---|
| TCP | 192.168.20.15:51514 | 203.0.113.5:40001 | 198.51.100.7:443 | ESTABLISHED | 3600 s |
| UDP | 192.168.10.7:49152 | 203.0.113.5:40002 | 8.8.8.8:53 | replied | 30 s |
| ICMP | 192.168.20.15 id 77 | 203.0.113.5 id 77 | 198.51.100.7 | echo sent | 10 s |

Firewalls group interfaces into *zones* (Campus Net: inside, servers, outside) and write rules between zones. Traffic inside one zone is usually permitted, traffic between zones is denied unless a rule allows it, and the usual defaults are that inside may initiate towards servers and outside, servers may reply, and outside may reach only published services. Some vendors use numeric *security levels* instead (Cisco ASA: 100 for inside, 0 for outside), with traffic from high to low allowed by default.

A *next-generation firewall* (NGFW) adds visibility above Layer 4: *application identification* (recognising a protocol by its behaviour, not its port, so that a service on TCP 443 is told apart from another), *user identity* (rules by directory user or group, not by address), an *intrusion prevention* engine (Section 9.13), URL and category filtering, malware sandboxing, and *TLS inspection*. For the last, the firewall acts as a proxy: it terminates the client's TLS session using a certificate that it forges on the fly, signed by an enterprise CA that the client's devices are configured to trust, and opens a second session to the real server. Content can then be scanned, but it breaks certificate pinning and mutual TLS, concentrates risk in the firewall's CA key, and raises privacy and legal questions, so banking and health categories are normally bypassed and users are informed by policy.

::: example
**A packet walk through the edge firewall.** Campus Net translates 192.168.20.0/24 to 203.0.113.5. A laptop 192.168.20.15 opens a connection to 198.51.100.7:443.

1. The SYN arrives on the inside interface. The firewall finds no session, checks the policy (inside to outside, HTTPS permitted), translates the source to 203.0.113.5:40001 and creates the session of the first row above.
2. The SYN-ACK from 198.51.100.7 is addressed to 203.0.113.5:40001. It matches the session in reverse, so it bypasses the rule base; the destination is translated back to 192.168.20.15:51514.
3. An unsolicited SYN from the Internet to 203.0.113.5:22 matches no session, and no rule permits it. It is dropped (usually silently, so that a scanner learns nothing).
4. Suppose BGP now sends the reply of a *new* connection via the second border router, whose firewall has no session. That firewall sees a SYN-ACK with no SYN and drops it; the client's connection times out.

[Result: stateful inspection depends on seeing both directions of a flow through the same device.]{.result}
:::

<figure>
<svg viewBox="0 0 480 170" width="480"><defs><marker id="ias" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="aas" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><rect class="box" x="10" y="62" width="70" height="30" rx="0" /><text class="lbl" x="45.0" y="80.0" text-anchor="middle">Client</text><rect class="box" x="400" y="62" width="70" height="30" rx="0" /><text class="lbl" x="435.0" y="80.0" text-anchor="middle">Server</text><rect class="fill" x="165" y="12" width="80" height="30" rx="0" /><text class="lbl" x="205.0" y="26.0" text-anchor="middle">FW1</text><text class="sm" x="205.0" y="36.0" text-anchor="middle">ISP-A</text><rect class="fill" x="165" y="118" width="80" height="30" rx="0" /><text class="lbl" x="205.0" y="132.0" text-anchor="middle">FW2</text><text class="sm" x="205.0" y="142.0" text-anchor="middle">ISP-B</text><line class="ln" x1="80" y1="68" x2="163" y2="34" marker-end="url(#ias)"/><line class="ln" x1="247" y1="34" x2="398" y2="68" marker-end="url(#ias)"/><text class="sm" x="112" y="44" text-anchor="middle">1 SYN</text><text class="sm" x="345" y="44" text-anchor="middle">1 SYN</text><text class="sm" x="205" y="56" text-anchor="middle">session created</text><line class="acc" x1="398" y1="88" x2="247" y2="128" marker-end="url(#aas)"/><line class="acc" x1="163" y1="128" x2="82" y2="90" marker-end="url(#aas)" stroke-dasharray="3 2"/><text class="sm" x="350" y="122" text-anchor="middle">2 SYN-ACK</text><text class="sm" x="205" y="160" text-anchor="middle">no session: dropped</text><text class="sm" x="88" y="125" text-anchor="middle">never arrives</text></svg>
<figcaption><b>Figure 9.9</b> Asymmetric routing: the SYN opens a session on FW1; the SYN-ACK returns through FW2, which has no session and drops it.</figcaption>
</figure>

Step 4 is the *asymmetric routing* problem (Figure 9.9). It arises when load sharing or BGP policy (Pillar 4) sends the outgoing and returning packets over different paths. The cures are to force symmetry (prefer one border for both directions, as with AS-path prepending or local preference), to place the firewalls in a high-availability pair that synchronises its session table (active/standby, in which only one unit forwards; an active/active pair needs symmetric flows or state replication between the units), or to place a single firewall behind both borders. A pair that drops 30 % of replies (Q9.27) is the textbook symptom.

*NAT interplay.* Translation and filtering interact in an order that is vendor-specific, so one must know which addresses a rule sees. In Linux Netfilter, *destination* NAT happens in `prerouting`, before the forward filter, so rules match the translated (internal) address; *source* NAT happens in `postrouting`, after it, so rules match the original internal address. Hence a rule for a published server names 10.0.0.80, not the public address. The connection-tracking entry stores both directions, so replies are un-translated without a rule. A stateful firewall is also itself a target: its session table has a finite size, which is why a flood of new connections can exhaust it (Section 9.10), and why no firewall alone stops a volumetric attack. The NAT techniques themselves are in [Section 3.6](#s3-6){.ref}.

The rule base of the Campus Net edge firewall is best planned as a matrix of zones before any rule is typed. The default for every empty cell is deny.

| From \ to | Users | Servers | Outside |
|---|---|---|---|
| **Users** | permit (same zone) | TCP 80 and 443 | permit, source-translated to 203.0.113.5 |
| **Servers** | replies only | permit (same zone) | TCP 443 to package mirrors and DNS to the resolver |
| **Outside** | deny | TCP 443 to 10.0.0.80 only (after destination NAT) | not applicable |

For availability, two firewalls form a *high-availability pair*. In *active/standby* only one unit forwards; it sends its session table over a dedicated link, together with heartbeats, so that the standby takes over without dropping established connections. If the heartbeat link fails while both units are healthy, both become active (*split brain*), which is why the heartbeat uses two paths. In *active/active* both forward, which brings back the symmetry problem above.

::: lab
`LAB 9.3 · 25 MIN` A stateful edge firewall for Campus Net with nftables, in a Linux VM (or three network namespaces) with `eth0` outside, `eth1` users and `eth2` servers. Run only on a lab VM you own.

```
table inet campus {
  chain input { type filter hook input priority 0; policy drop;
    ct state established,related accept
    iif lo accept
    iifname "eth1" tcp dport 22 accept
  }
  chain forward { type filter hook forward priority 0; policy drop;
    ct state established,related accept
    ct state invalid drop
    iifname "eth1" oifname "eth0" accept
    iifname "eth1" oifname "eth2" tcp dport { 80, 443 } accept
    iifname "eth0" oifname "eth2" ip daddr 10.0.0.80 tcp dport 443 accept
  }
}
table ip nat {
  chain prerouting { type nat hook prerouting priority -100;
    iifname "eth0" tcp dport 443 dnat to 10.0.0.80
  }
  chain postrouting { type nat hook postrouting priority 100;
    oifname "eth0" snat to 203.0.113.5
  }
}
```

The three forward rules, in order, let users reach the Internet, let users reach the web ports of the server network, and let the Internet reach the published server only (after DNAT). Load it with `nft -f campus.nft`, make a connection from a user host, and list the session with `conntrack -L`.

```
tcp 3598 ESTABLISHED src=192.168.20.15 dst=198.51.100.7 sport=51514 dport=443
  src=198.51.100.7 dst=203.0.113.5 sport=443 dport=40001 [ASSURED]
```

**What you should notice:** the second half of the entry is the reply tuple: its destination is the translated address 203.0.113.5:40001, which is how the reply is matched and un-translated. No rule allows replies; `ct state established,related` does that for every flow. The forward rule for the published server names 10.0.0.80, the address after DNAT. From the outside, `nc -zv 203.0.113.5 22` gets no answer, since the default policy is drop.
:::

::: check
1. What does a stateful firewall check that an ACL does not? [^c9-9]
2. Why does an active/active firewall pair need symmetric routing? [^c9-10]
:::

[^c9-9]: Whether a packet belongs to an existing, permitted session (and for TCP, whether its state and sequence number are valid).
[^c9-10]: Each unit holds only the sessions it created unless state is synchronised, so a reply returning through the other unit matches no session and is dropped.

:::
