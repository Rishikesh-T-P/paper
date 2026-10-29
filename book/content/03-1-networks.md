::: {.chapter .p3}
::: opener
[Part I · Pillar 3]{.part-label}

[3]{.num}

# Computer Networks Fundamentals {#ch3}

[Every packet tells a story; we learn to read it, layer by layer.]{.promise}

1. [3.1 Networks, devices and delay]{} [MUST]{}
2. [3.2 The OSI and TCP/IP models, and encapsulation]{} [MUST]{}
3. [3.3 The data-link layer: Ethernet, switching, error control and ARQ]{} [MUST]{}
4. [3.4 IPv4 addressing, subnetting, VLSM and CIDR]{} [MUST]{}
5. [3.5 The IPv4 header, fragmentation, MTU and ICMP]{} [MUST]{}
6. [3.6 ARP, DHCP and NAT: the glue protocols]{} [MUST]{}
7. [3.7 IPv6 essentials]{} [SHOULD]{}
8. [3.8 Routing concepts in one page]{} [MUST]{}
9. [3.9 Transport: UDP, TCP, flow control and congestion control]{} [MUST]{}
10. [3.10 The application layer: DNS, HTTP, TLS and QUIC]{} [SHOULD]{}
11. [3.11 Capstone: what happens when you type google.com]{} [MUST]{}
:::

## [3.1]{.sec}Networks, devices and delay [Must · ■□□]{.tag} {#s3-1}

A computer network is a set of devices that exchange data over shared links so that they can share resources: files, printers, an internet connection, a database. Every network question in an interview reduces to two things, namely *where the bits go* and *how long they take*, and this section supplies the vocabulary for both.

::: bigidea
A network moves bits between devices, and splitting that job into independent layers is what allows each part to be replaced without disturbing the rest.
:::

### Sizes and shapes

Networks are named by their reach. A *LAN* (local area network) covers a room, a floor or a campus and is owned by one organisation. A *MAN* covers a city. A *WAN* (wide area network) joins sites across cities or countries and usually runs over links leased from a carrier. The *Internet* is the network of networks that joins all of them using one common protocol, IP.

The *topology* is the pattern in which devices are joined. In a *bus* all devices hang from one shared cable; in a *star* each hangs from a central device; in a *ring* each has two neighbours; in a *full mesh* every pair is joined directly. The last is robust but costs n(n − 1)/2 links for n devices, so ten sites already need 45 links and a hundred need 4,950. Hence real networks are stars of stars, with a few meshed links at the core.

<figure>
<svg viewBox="0 0 480 136" width="480">
<text class="lbl" x="60" y="14" text-anchor="middle" >Bus</text>
<text class="sm" x="60" y="128" text-anchor="middle" >one shared cable</text>
<text class="lbl" x="178" y="14" text-anchor="middle" >Star</text>
<text class="sm" x="178" y="128" text-anchor="middle" >n links to the centre</text>
<text class="lbl" x="296" y="14" text-anchor="middle" >Ring</text>
<text class="sm" x="296" y="128" text-anchor="middle" >n links in a loop</text>
<text class="lbl" x="414" y="14" text-anchor="middle" >Full mesh</text>
<text class="sm" x="414" y="128" text-anchor="middle" >n(n − 1)/2 links</text>
<line class="acc" x1="15" y1="60" x2="105" y2="60" />
<line class="ln" x1="24" y1="60" x2="24" y2="78" />
<rect class="box" x="18" y="78" width="12" height="10" rx="1" />
<line class="ln" x1="48" y1="60" x2="48" y2="78" />
<rect class="box" x="42" y="78" width="12" height="10" rx="1" />
<line class="ln" x1="72" y1="60" x2="72" y2="78" />
<rect class="box" x="66" y="78" width="12" height="10" rx="1" />
<line class="ln" x1="96" y1="60" x2="96" y2="78" />
<rect class="box" x="90" y="78" width="12" height="10" rx="1" />
<text class="sm" x="60" y="108" text-anchor="middle" >n = 4: 4 drops</text>
<rect class="fill" x="169" y="52" width="18" height="12" rx="1" />
<line class="ln" x1="173" y1="58" x2="183" y2="58" />
<line class="ln" x1="178" y1="58" x2="178.0" y2="22.0" />
<rect class="box" x="173.0" y="18.0" width="10" height="8" rx="1" />
<line class="ln" x1="178" y1="58" x2="212.2" y2="46.9" />
<rect class="box" x="207.2" y="42.9" width="10" height="8" rx="1" />
<line class="ln" x1="178" y1="58" x2="199.2" y2="87.1" />
<rect class="box" x="194.2" y="83.1" width="10" height="8" rx="1" />
<line class="ln" x1="178" y1="58" x2="156.8" y2="87.1" />
<rect class="box" x="151.8" y="83.1" width="10" height="8" rx="1" />
<line class="ln" x1="178" y1="58" x2="143.8" y2="46.9" />
<rect class="box" x="138.8" y="42.9" width="10" height="8" rx="1" />
<text class="sm" x="178" y="108" text-anchor="middle" >n = 5: 5 links</text>
<line class="ln" x1="296.0" y1="26.0" x2="328.3" y2="49.5" />
<line class="ln" x1="328.3" y1="49.5" x2="316.0" y2="87.5" />
<line class="ln" x1="316.0" y1="87.5" x2="276.0" y2="87.5" />
<line class="ln" x1="276.0" y1="87.5" x2="263.7" y2="49.5" />
<line class="ln" x1="263.7" y1="49.5" x2="296.0" y2="26.0" />
<rect class="box" x="291.0" y="22.0" width="10" height="8" rx="1" />
<rect class="box" x="323.3" y="45.5" width="10" height="8" rx="1" />
<rect class="box" x="311.0" y="83.5" width="10" height="8" rx="1" />
<rect class="box" x="271.0" y="83.5" width="10" height="8" rx="1" />
<rect class="box" x="258.7" y="45.5" width="10" height="8" rx="1" />
<text class="sm" x="296" y="108" text-anchor="middle" >n = 5: 5 links</text>
<line class="lg" x1="414.0" y1="26.0" x2="446.3" y2="49.5" />
<line class="lg" x1="414.0" y1="26.0" x2="434.0" y2="87.5" />
<line class="lg" x1="414.0" y1="26.0" x2="394.0" y2="87.5" />
<line class="lg" x1="414.0" y1="26.0" x2="381.7" y2="49.5" />
<line class="lg" x1="446.3" y1="49.5" x2="434.0" y2="87.5" />
<line class="lg" x1="446.3" y1="49.5" x2="394.0" y2="87.5" />
<line class="lg" x1="446.3" y1="49.5" x2="381.7" y2="49.5" />
<line class="lg" x1="434.0" y1="87.5" x2="394.0" y2="87.5" />
<line class="lg" x1="434.0" y1="87.5" x2="381.7" y2="49.5" />
<line class="lg" x1="394.0" y1="87.5" x2="381.7" y2="49.5" />
<rect class="box" x="409.0" y="22.0" width="10" height="8" rx="1" />
<rect class="box" x="441.3" y="45.5" width="10" height="8" rx="1" />
<rect class="box" x="429.0" y="83.5" width="10" height="8" rx="1" />
<rect class="box" x="389.0" y="83.5" width="10" height="8" rx="1" />
<rect class="box" x="376.7" y="45.5" width="10" height="8" rx="1" />
<text class="sm" x="414" y="108" text-anchor="middle" >n = 5: 10 links</text>
</svg>
<figcaption><b>Figure 3.1</b> Four physical topologies and their link counts. A full mesh grows quadratically, which is why large networks are built as stars of stars.</figcaption>
</figure>

### Devices

Five boxes appear in almost every diagram, and an interviewer expects one sentence on each. A *hub* is a layer-1 repeater: every bit that enters a port leaves all the other ports, so all attached devices share one wire. A *switch* learns which device sits behind which port and forwards a frame only to the port concerned. A *router* joins different networks and forwards packets by their IP destination. A *layer-3 switch* is a switch with routing built into its hardware, which is how campus networks route between VLANs at line rate. A *firewall* permits or drops traffic according to rules, and an *access point* (AP) bridges Wi-Fi radio to the wired network.

Two terms follow from these devices. A *collision domain* is the set of ports whose transmissions can collide on a shared medium; a hub extends it, and every switch port ends it. A *broadcast domain* is the set of devices that receive a frame sent to the broadcast address; a switch extends it, and only a router ends it. Note that modern switched Ethernet is full-duplex, so collisions no longer occur in practice, yet the counting question remains a standard interview exercise.

<figure>
<svg viewBox="0 0 480 236" width="480">
<defs><marker id="dm" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="inkf" d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker></defs>
<rect class="lg" x="8" y="62" width="222" height="166" rx="4" fill="#EEF3F5" fill-opacity=".7" stroke-dasharray="4 2"/>
<rect class="lg" x="250" y="62" width="222" height="166" rx="4" fill="#EEF3F5" fill-opacity=".7" stroke-dasharray="4 2"/>
<text class="sm" x="16" y="222" text-anchor="start" >Broadcast domain 1</text>
<text class="sm" x="464" y="222" text-anchor="end" >Broadcast domain 2</text>
<circle class="box" cx="240" cy="24" r="13"/><line class="ln" x1="232" y1="16" x2="248" y2="32" /><line class="ln" x1="248" y1="16" x2="232" y2="32" />
<text class="sm" x="268" y="28" text-anchor="start" >Router</text>
<line class="ln" x1="233" y1="35" x2="128" y2="92" />
<line class="ln" x1="120" y1="109" x2="40" y2="150" />
<line class="ln" x1="120" y1="109" x2="100" y2="150" />
<line class="ln" x1="120" y1="109" x2="160" y2="150" />
<line class="ln" x1="247" y1="35" x2="352" y2="92" />
<line class="ln" x1="360" y1="109" x2="290" y2="150" />
<line class="ln" x1="360" y1="109" x2="350" y2="150" />
<line class="ln" x1="375" y1="109" x2="430" y2="134" />
<rect class="box" x="100" y="91" width="40" height="18" rx="1" /><line class="ln" x1="108" y1="97" x2="132" y2="97" marker-end="url(#dm)"/><line class="ln" x1="132" y1="104" x2="108" y2="104" marker-end="url(#dm)"/><text class="sm" x="120" y="123" text-anchor="middle" >Switch S1</text>
<rect class="box" x="340" y="91" width="40" height="18" rx="1" /><line class="ln" x1="348" y1="97" x2="372" y2="97" marker-end="url(#dm)"/><line class="ln" x1="372" y1="104" x2="348" y2="104" marker-end="url(#dm)"/><text class="sm" x="360" y="123" text-anchor="middle" >Switch S2</text>
<rect class="box" x="29" y="150" width="22" height="12" rx="1" /><text class="sm" x="40" y="173" text-anchor="middle" >PC1</text>
<rect class="box" x="89" y="150" width="22" height="12" rx="1" /><text class="sm" x="100" y="173" text-anchor="middle" >PC2</text>
<rect class="box" x="149" y="150" width="22" height="12" rx="1" /><text class="sm" x="160" y="173" text-anchor="middle" >PC3</text>
<rect class="box" x="279" y="150" width="22" height="12" rx="1" /><text class="sm" x="290" y="173" text-anchor="middle" >PC4</text>
<rect class="box" x="339" y="150" width="22" height="12" rx="1" /><text class="sm" x="350" y="173" text-anchor="middle" >PC5</text>
<rect class="fill" x="412" y="134" width="36" height="14" rx="1" />
<text class="sm" x="430" y="144" text-anchor="middle" >Hub</text>
<line class="ln" x1="430" y1="148" x2="405" y2="184" />
<rect class="box" x="394" y="184" width="22" height="12" rx="1" /><text class="sm" x="405" y="207" text-anchor="middle" >PC6</text>
<line class="ln" x1="430" y1="148" x2="430" y2="184" />
<rect class="box" x="419" y="184" width="22" height="12" rx="1" /><text class="sm" x="430" y="207" text-anchor="middle" >PC7</text>
<line class="ln" x1="430" y1="148" x2="455" y2="184" />
<rect class="box" x="444" y="184" width="22" height="12" rx="1" /><text class="sm" x="455" y="207" text-anchor="middle" >PC8</text>
<circle cx="180" cy="64" r="5.5" style="fill:#fff;stroke:var(--accent);stroke-width:1"/><text class="sm" x="180" y="66" text-anchor="middle" style="fill:var(--accent);font-weight:700;font-size:7px">1</text>
<circle cx="80" cy="130" r="5.5" style="fill:#fff;stroke:var(--accent);stroke-width:1"/><text class="sm" x="80" y="132" text-anchor="middle" style="fill:var(--accent);font-weight:700;font-size:7px">2</text>
<circle cx="110" cy="130" r="5.5" style="fill:#fff;stroke:var(--accent);stroke-width:1"/><text class="sm" x="110" y="132" text-anchor="middle" style="fill:var(--accent);font-weight:700;font-size:7px">3</text>
<circle cx="140" cy="130" r="5.5" style="fill:#fff;stroke:var(--accent);stroke-width:1"/><text class="sm" x="140" y="132" text-anchor="middle" style="fill:var(--accent);font-weight:700;font-size:7px">4</text>
<circle cx="300" cy="64" r="5.5" style="fill:#fff;stroke:var(--accent);stroke-width:1"/><text class="sm" x="300" y="66" text-anchor="middle" style="fill:var(--accent);font-weight:700;font-size:7px">5</text>
<circle cx="325" cy="130" r="5.5" style="fill:#fff;stroke:var(--accent);stroke-width:1"/><text class="sm" x="325" y="132" text-anchor="middle" style="fill:var(--accent);font-weight:700;font-size:7px">6</text>
<circle cx="355" cy="130" r="5.5" style="fill:#fff;stroke:var(--accent);stroke-width:1"/><text class="sm" x="355" y="132" text-anchor="middle" style="fill:var(--accent);font-weight:700;font-size:7px">7</text>
<circle cx="402" cy="122" r="5.5" style="fill:#fff;stroke:var(--accent);stroke-width:1"/><text class="sm" x="402" y="124" text-anchor="middle" style="fill:var(--accent);font-weight:700;font-size:7px">8</text>
</svg>
<figcaption><b>Figure 3.2</b> Counting domains. The router does not forward broadcasts, so there are two broadcast domains (dashed). Every switch port is its own collision domain, while the hub and PC6 to PC8 share one wire. Link 8 is therefore one domain, and the total is 8 collision domains, numbered on the links.</figcaption>
</figure>

::: example
**Count the domains in the figure.**

1. A router interface never forwards broadcasts, so each of its two sides is a separate broadcast domain: S1 with PC1–PC3, and S2 with PC4–PC5, the hub and PC6–PC8. That gives 2.
2. Each switch port is a separate collision domain. S1 has four ports in use (router, PC1, PC2, PC3), giving 4.
3. S2 has four ports in use (router, PC4, PC5, hub). The hub and PC6–PC8 share one wire and so form a single domain behind S2's hub port, giving 4.

[Result: 2 broadcast domains and 8 collision domains.]{.result}
:::

### Circuit and packet switching

A telephone network of the old kind used *circuit switching*: a path was reserved from end to end for the whole call, whether or not anyone was speaking. The Internet uses *packet switching*: the data is cut into packets, each carrying its destination address, and routers forward them independently. Packet switching wastes nothing on silence and shares links statistically, at the price that packets can queue, be delayed or be lost. Every later topic in this pillar is a mechanism for living with that price.

### Four kinds of delay

[**Bandwidth vs throughput** — bandwidth is what the link could carry, in bits per second; throughput is what you actually got. A motorway has six lanes (bandwidth) but you still arrive late in a jam.]{.margin}A packet travelling from host to host accumulates delay at every hop from four sources. *Processing delay* is the time a router takes to read the header and choose the output port; it is microseconds. *Queueing delay* is the time spent waiting for the output link to become free, and it varies with load; it is the cause of jitter, the variation of delay from one packet to the next. *Transmission delay* is the time to push all the bits of the packet onto the link, L/R for a packet of L bits on a link of R bit/s. *Propagation delay* is the time a bit takes to travel the length of the link, d/v, where v is about 2 × 10⁸ m/s in copper or fibre, two-thirds of the speed of light in vacuum.

Transmission delay depends on packet size and link speed; propagation delay depends only on distance. Confusing the two is the commonest error in this topic.

::: example
**Send a 1 MB file over a 2,000 km link.** Take 1 MB as 8 × 10⁶ bits and ignore queueing and headers.

1. At 10 Mb/s: transmission = 8 × 10⁶ / 10⁷ = 0.8 s.
2. Propagation = 2 × 10⁶ m / 2 × 10⁸ m/s = 0.010 s = 10 ms, whatever the speed of the link.
3. At 10 Mb/s the total is 0.8 + 0.01 ≈ 0.81 s.
4. At 1 Gb/s: transmission = 8 × 10⁶ / 10⁹ = 8 ms, so the total is 8 + 10 = 18 ms.

[Result: 0.81 s and 18 ms. Once the link is fast, distance, not bandwidth, sets the floor on latency; no upgrade can beat 10 ms for these 2,000 km.]{.result}
:::

::: trap
*Claim:* "A faster link makes every transfer faster by the same factor." *Why it is wrong:* only transmission delay shrinks with bandwidth; propagation delay is fixed by distance and the speed of light in the medium. *Correct statement:* a hundred-fold faster link cuts a large transfer a hundred-fold, but a small request across an ocean barely improves.
:::

::: lens
[CISCO · NOKIA]{.co}

Asked as "hub versus switch versus router", the interviewer wants collision and broadcast domains stated per device, then one scenario, such as why a loop of hubs is harmless but a loop of switches is not (a topic for Pillar 4). A strong answer draws the figure above and counts, without being asked. See Q3.2 in the [Problem Set](#ps3){.ref}.
:::

::: lab
`LAB 3.1 · 15 MIN` Cisco Packet Tracer. Build two small networks: four PCs on a hub, and four PCs on a switch. Switch to *Simulation* mode, filter on ICMP, and send one ping from PC0 to PC1 in each network.

**What you should notice:** on the hub, the event list shows the echo request copied to every other port and the request is seen by PC2 and PC3, which discard it. On the switch, the first request is flooded (the switch has not yet learned PC1), but the reply, and every later ping, travels only between the two ports concerned.
:::

::: check
1. How many links does a full mesh of 12 routers need? [^c3-1]
2. A frame is sent from a PC to another PC in the same VLAN through two switches. How many collision domains does it cross? [^c3-2]
3. Which of the four delays grows when the network is congested? [^c3-3]
:::

[^c3-1]: 12 × 11 / 2 = 66.
[^c3-2]: Three: PC to switch 1, switch 1 to switch 2, switch 2 to PC. Each link is its own domain.
[^c3-3]: Queueing delay, because packets wait for the output link; it is also the source of jitter.

## [3.2]{.sec}The OSI and TCP/IP models, and encapsulation [Must · ■□□]{.tag} {#s3-2}

Sending a web page involves cables, addresses, reliability, encryption and a document format, and no single protocol does all of this. The standard answer is to divide the work into *layers*, each offering a service to the layer above and using the service of the layer below. A layer on one machine is concerned only with its *peer* layer on the other machine, which it talks to through a header that it adds to the data.

::: bigidea
Each layer wraps the data from above in its own header so that its peer layer at the far end can act on it, and this wrapping is why a change at one layer does not disturb the others.
:::

### Two models

[**OSI mnemonic** — layers 7 to 1: *All People Seem To Need Data Processing* (Application, Presentation, Session, Transport, Network, Data link, Physical). Reverse it for 1 to 7: *Please Do Not Throw Sausage Pizza Away*.]{.margin}The *OSI model* (Open Systems Interconnection) has seven layers and is used as vocabulary: engineers say "a layer-2 problem" or "a layer-7 load balancer". The *TCP/IP model* describes what is actually deployed and has four layers, in which the top three OSI layers merge into one application layer and the bottom two into one link layer. Textbooks that prefer five layers split the link layer again, giving the five-layer model used in this book from now on.

<figure>
<svg viewBox="0 0 480 192" width="480">
<text class="sm" x="18" y="12" text-anchor="start" >OSI model</text>
<text class="sm" x="122" y="12" text-anchor="start" >TCP/IP model</text>
<text class="sm" x="216" y="12" text-anchor="start" >Typical protocols</text>
<text class="sm" x="362" y="12" text-anchor="start" >PDU · device</text>
<rect class="box" x="16" y="18" width="100" height="22" rx="0" />
<text class="lbl" x="66" y="32" text-anchor="middle" >7 Application</text>
<rect class="fill" x="214" y="18" width="142" height="22" rx="0" />
<text class="lbl" x="285" y="32" text-anchor="middle" style="font-size:7.4px">HTTP · DNS · SMTP · SSH</text>
<text class="lbl" x="362" y="28" text-anchor="start" style="font-size:7.6px">Data</text>
<rect class="box" x="16" y="42" width="100" height="22" rx="0" />
<text class="lbl" x="66" y="56" text-anchor="middle" >6 Presentation</text>
<rect class="fill" x="214" y="42" width="142" height="22" rx="0" />
<text class="lbl" x="285" y="56" text-anchor="middle" style="font-size:7.4px">TLS · encodings (UTF-8, JSON)</text>
<text class="lbl" x="362" y="52" text-anchor="start" style="font-size:7.6px">Data</text>
<rect class="box" x="16" y="66" width="100" height="22" rx="0" />
<text class="lbl" x="66" y="80" text-anchor="middle" >5 Session</text>
<rect class="fill" x="214" y="66" width="142" height="22" rx="0" />
<text class="lbl" x="285" y="80" text-anchor="middle" style="font-size:7.4px">sockets, RPC sessions</text>
<text class="lbl" x="362" y="76" text-anchor="start" style="font-size:7.6px">Data</text>
<rect class="box" x="16" y="90" width="100" height="22" rx="0" />
<text class="lbl" x="66" y="104" text-anchor="middle" >4 Transport</text>
<rect class="fill" x="214" y="90" width="142" height="22" rx="0" />
<text class="lbl" x="285" y="104" text-anchor="middle" style="font-size:7.4px">TCP · UDP · QUIC (over UDP)</text>
<text class="lbl" x="362" y="100" text-anchor="start" style="font-size:7.6px">Segment / datagram</text>
<text class="sm" x="362" y="109" text-anchor="start" >firewall, load balancer</text>
<rect class="box" x="16" y="114" width="100" height="22" rx="0" />
<text class="lbl" x="66" y="128" text-anchor="middle" >3 Network</text>
<rect class="fill" x="214" y="114" width="142" height="22" rx="0" />
<text class="lbl" x="285" y="128" text-anchor="middle" style="font-size:7.4px">IP · ICMP · OSPF (over IP)</text>
<text class="lbl" x="362" y="124" text-anchor="start" style="font-size:7.6px">Packet</text>
<text class="sm" x="362" y="133" text-anchor="start" >router, L3 switch</text>
<rect class="box" x="16" y="138" width="100" height="22" rx="0" />
<text class="lbl" x="66" y="152" text-anchor="middle" >2 Data link</text>
<rect class="fill" x="214" y="138" width="142" height="22" rx="0" />
<text class="lbl" x="285" y="152" text-anchor="middle" style="font-size:7.4px">Ethernet · 802.11 · ARP · PPP</text>
<text class="lbl" x="362" y="148" text-anchor="start" style="font-size:7.6px">Frame</text>
<text class="sm" x="362" y="157" text-anchor="start" >switch, bridge, AP</text>
<rect class="box" x="16" y="162" width="100" height="22" rx="0" />
<text class="lbl" x="66" y="176" text-anchor="middle" >1 Physical</text>
<rect class="fill" x="214" y="162" width="142" height="22" rx="0" />
<text class="lbl" x="285" y="176" text-anchor="middle" style="font-size:7.4px">UTP · fibre · radio</text>
<text class="lbl" x="362" y="172" text-anchor="start" style="font-size:7.6px">Bits</text>
<text class="sm" x="362" y="181" text-anchor="start" >hub, repeater</text>
<rect class="box" x="120" y="18" width="90" height="70" rx="0" />
<text class="lbl" x="165" y="50" text-anchor="middle" >Application</text>
<text class="sm" x="165" y="62" text-anchor="middle" >(layers 5–7)</text>
<rect class="box" x="120" y="90" width="90" height="22" rx="0" />
<text class="lbl" x="165" y="104" text-anchor="middle" >Transport</text>
<rect class="box" x="120" y="114" width="90" height="22" rx="0" />
<text class="lbl" x="165" y="128" text-anchor="middle" >Internet</text>
<rect class="box" x="120" y="138" width="90" height="46" rx="0" />
<text class="lbl" x="165" y="158" text-anchor="middle" >Link</text>
<text class="sm" x="165" y="170" text-anchor="middle" >(layers 1–2)</text>
<rect class="acc" x="214" y="90" width="142" height="22" fill="none"/>
</svg>
<figcaption><b>Figure 3.3</b> The seven-layer OSI model beside the four-layer TCP/IP model. The highlighted row is where TCP and UDP live; the stack below it is the network, the stack above it is the application.</figcaption>
</figure>

Each layer has a name for its unit of data, the *protocol data unit* (PDU): data at the application layer, a *segment* (TCP) or *datagram* (UDP) at the transport layer, a *packet* at the network layer, a *frame* at the data-link layer, and *bits* on the wire. Interviewers notice when these names are used loosely.

Protocols do not always sit tidily. ARP is carried directly in Ethernet frames yet resolves IP addresses, so it is often called a "layer 2.5" protocol. ICMP is a layer-3 protocol, even though it travels inside IP packets. TLS lives between the transport and application layers and has no home in the TCP/IP model. QUIC runs over UDP but provides what TCP provides, plus encryption. Hence the question "which layer is X?" is best answered with "it is carried in Y and serves Z".

### Encapsulation

When an application writes data to a socket, the transport layer prepends a TCP header, giving a segment; the network layer prepends an IP header, giving a packet; the link layer prepends an Ethernet header and appends a trailer, the *frame check sequence* (FCS), giving a frame. This is *encapsulation*; the receiver strips the headers in reverse order, termed *decapsulation*. A layer knows which protocol is above it through a *demultiplexing key* in its header: the EtherType field in Ethernet (0x0800 for IPv4, 0x86DD for IPv6, 0x0806 for ARP), the protocol field in IP (6 for TCP, 17 for UDP, 1 for ICMP), and the destination port in TCP and UDP.

<figure>
<svg viewBox="0 0 480 170" width="480">
<text class="sm" x="20" y="10" text-anchor="start" >Layer</text>
<text class="sm" x="430" y="10" text-anchor="start" >PDU</text>
<text class="lbl" x="20" y="33" text-anchor="start" >Application</text>
<rect class="box" x="110" y="14" width="300" height="26" rx="0" />
<text class="lbl" x="260" y="30" text-anchor="middle" >HTTP request (data)</text>
<text class="lbl" x="430" y="31" text-anchor="start" >Data</text>
<text class="lbl" x="20" y="69" text-anchor="start" >Transport</text>
<rect class="hl" x="110" y="50" width="69.2" height="26" rx="0" />
<rect class="ln" x="110" y="50" width="69.2" height="26" rx="0" fill="none"/>
<text class="lbl" x="144.6" y="66" text-anchor="middle" style="font-size:7.8px">TCP hdr 20 B</text>
<rect class="box" x="179.2" y="50" width="230.8" height="26" rx="0" />
<text class="lbl" x="294.6" y="66" text-anchor="middle" style="font-size:7.8px">data</text>
<text class="lbl" x="430" y="67" text-anchor="start" >Segment</text>
<text class="lbl" x="20" y="105" text-anchor="start" >Network</text>
<rect class="hl" x="110" y="86" width="56.2" height="26" rx="0" />
<rect class="ln" x="110" y="86" width="56.2" height="26" rx="0" fill="none"/>
<text class="lbl" x="138.1" y="102" text-anchor="middle" style="font-size:7.8px">IP hdr 20 B</text>
<rect class="fill" x="166.2" y="86" width="56.2" height="26" rx="0" />
<text class="lbl" x="194.4" y="102" text-anchor="middle" style="font-size:7.8px">TCP hdr</text>
<rect class="box" x="222.5" y="86" width="187.5" height="26" rx="0" />
<text class="lbl" x="316.2" y="102" text-anchor="middle" style="font-size:7.8px">data</text>
<text class="lbl" x="430" y="103" text-anchor="start" >Packet</text>
<text class="lbl" x="20" y="141" text-anchor="start" >Data link</text>
<rect class="hl" x="110" y="122" width="43.9" height="26" rx="0" />
<rect class="ln" x="110" y="122" width="43.9" height="26" rx="0" fill="none"/>
<text class="lbl" x="132.0" y="138" text-anchor="middle" style="font-size:7.8px">Eth 14 B</text>
<rect class="fill" x="153.9" y="122" width="43.9" height="26" rx="0" />
<text class="lbl" x="175.9" y="138" text-anchor="middle" style="font-size:7.8px">IP hdr</text>
<rect class="fill" x="197.8" y="122" width="43.9" height="26" rx="0" />
<text class="lbl" x="219.8" y="138" text-anchor="middle" style="font-size:7.8px">TCP hdr</text>
<rect class="box" x="241.7" y="122" width="137.2" height="26" rx="0" />
<text class="lbl" x="310.3" y="138" text-anchor="middle" style="font-size:7.8px">data</text>
<rect class="hl" x="378.9" y="122" width="31.1" height="26" rx="0" />
<rect class="ln" x="378.9" y="122" width="31.1" height="26" rx="0" fill="none"/>
<text class="lbl" x="394.5" y="138" text-anchor="middle" style="font-size:7.8px">FCS 4</text>
<text class="lbl" x="430" y="139" text-anchor="start" >Frame</text>
</svg>
<figcaption><b>Figure 3.4</b> Encapsulation. Each layer wraps the data it receives from above in its own header (highlighted). Only the data-link layer also adds a trailer, the frame check sequence (FCS). The receiver reverses the process, which is termed decapsulation.</figcaption>
</figure>

The headers cost bandwidth, and an interviewer may ask by how much. We measure it below.

::: example
**Overhead of an HTTP request carrying 100 bytes of data, and of a full-size segment.**

1. Header bytes: TCP 20 + IPv4 20 + Ethernet 14 + FCS 4 = 58 bytes.
2. On the wire there is also an 8-byte preamble and start delimiter and a 12-byte inter-frame gap, which together occupy the medium for 20 bytes. The total per frame is 100 + 58 + 20 = 178 byte-times.
3. Efficiency = 100 / 178 ≈ 56%.
4. With 1,460 bytes of data (the largest that fits a 1,500-byte IP packet), the total is 1,460 + 78 = 1,538 byte-times, and the efficiency is 1,460 / 1,538 ≈ 94.9%.

[Result: 56% for the small request and 94.9% for the full-size segment. Small packets waste capacity, which is why bulk transfers use the largest segment the path allows.]{.result}
:::

### What changes where

The stack diagram below shows a packet crossing one router. The hosts build and read all layers, but the router climbs only to layer 3: it removes the incoming frame, decrements the IP time-to-live, looks up the destination, and builds a new frame for the next link. The layer-4 segment inside is never read. Hence the rule that interviewers love, which is stated in Section 3.6 with numbers: *the MAC addresses change at every hop, whereas the IP addresses do not (unless NAT intervenes).*

<figure>
<svg viewBox="0 0 480 180" width="480">
<defs><marker id="sk" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z" style=""/></marker></defs>
<text class="lbl" x="70" y="14" text-anchor="middle" >Host A</text>
<rect class="box" x="30" y="22" width="80" height="26" rx="0" />
<text class="lbl" x="36" y="34" text-anchor="start" >Application</text>
<rect class="box" x="30" y="52" width="80" height="26" rx="0" />
<text class="lbl" x="36" y="64" text-anchor="start" >Transport</text>
<rect class="box" x="30" y="82" width="80" height="26" rx="0" />
<text class="lbl" x="36" y="94" text-anchor="start" >Network</text>
<rect class="box" x="30" y="112" width="80" height="26" rx="0" />
<text class="lbl" x="36" y="124" text-anchor="start" >Link</text>
<text class="lbl" x="240" y="14" text-anchor="middle" >Router</text>
<rect class="box" x="200" y="82" width="80" height="26" rx="0" />
<text class="lbl" x="206" y="94" text-anchor="start" >Network</text>
<rect class="box" x="200" y="112" width="80" height="26" rx="0" />
<text class="lbl" x="206" y="124" text-anchor="start" >Link</text>
<text class="lbl" x="410" y="14" text-anchor="middle" >Host B</text>
<rect class="box" x="370" y="22" width="80" height="26" rx="0" />
<text class="lbl" x="376" y="34" text-anchor="start" >Application</text>
<rect class="box" x="370" y="52" width="80" height="26" rx="0" />
<text class="lbl" x="376" y="64" text-anchor="start" >Transport</text>
<rect class="box" x="370" y="82" width="80" height="26" rx="0" />
<text class="lbl" x="376" y="94" text-anchor="start" >Network</text>
<rect class="box" x="370" y="112" width="80" height="26" rx="0" />
<text class="lbl" x="376" y="124" text-anchor="start" >Link</text>
<line class="lg" x1="110" y1="135" x2="200" y2="135" />
<line class="lg" x1="280" y1="135" x2="370" y2="135" />
<path class="acc" d="M100,38 V135 H255 V104 H268 V135 H440 V40" marker-end="url(#sk)"/>
<text class="sm" x="155" y="150" text-anchor="middle" >frame 1: A to router</text>
<text class="sm" x="325" y="150" text-anchor="middle" >frame 2: router to B</text>
<text class="sm" x="240" y="172" text-anchor="middle" >segment: end to end    packet: end to end (TTL changes)    frame: one link only</text>
</svg>
<figcaption><b>Figure 3.5</b> A packet crossing one router. The segment is built and read only at the two hosts; the router climbs just to layer 3, then rewrites the frame for the next link.</figcaption>
</figure>

::: trap
*Claim:* "A router decrypts and reads the TCP header, which is how it knows the port." *Why it is wrong:* an ordinary router forwards on the IP destination alone and never touches the segment. *Correct statement:* firewalls, NAT devices and load balancers do read layer 4, and are therefore described as layer-4 devices; a plain router is a layer-3 device.
:::

::: lens
[CISCO · NOKIA · AMAZON · MICROSOFT · JUNIPER]{.co}

The question is "name the layers with a protocol and a device each" (Q3.1) or, harder, "which layer does a load balancer work at?". A strong answer gives both L4 (TCP connections, as for a network load balancer) and L7 (HTTP headers, as for an application load balancer), and notes the cost of each.
:::

::: lab
`LAB 3.2 · 20 MIN` Wireshark. Run `curl -s http://example.com -o /dev/null` while capturing, stop, and apply the display filter `http`. Select the request and expand the packet-details pane.

```
Frame 14: 142 bytes on wire
Ethernet II, Src: 52:54:00:12:34:56, Dst: 52:54:00:12:35:02   (type 0x0800)
Internet Protocol Version 4, Src: 10.0.2.15, Dst: 93.184.216.34  (proto 6)
Transmission Control Protocol, Src Port: 49822, Dst Port: 80, Len: 76
Hypertext Transfer Protocol: GET / HTTP/1.1
```

**What you should notice:** the four headings are the four layers of Figure 3.4 from the bottom upward; the EtherType, the IP protocol number and the destination port are the three demultiplexing keys. The headers total 66 bytes of the 142 captured: 14 (Ethernet), 20 (IPv4) and 32 (TCP, 20 plus 12 bytes of timestamp options), leaving 76 bytes of HTTP.
:::

::: check
1. At which layer does a switch operate, and which address does it read? [^c3-4]
2. Why is ARP called "layer 2.5"? [^c3-5]
3. A frame carries 14 + 20 + 20 header bytes and 1,000 bytes of data. What fraction of the frame (ignoring FCS and preamble) is data? [^c3-6]
:::

[^c3-4]: Layer 2; the destination MAC address.
[^c3-5]: It is carried in an Ethernet frame (layer 2) but it maps layer-3 addresses to layer-2 addresses.
[^c3-6]: 1,000 / 1,054 ≈ 94.9%.

:::
