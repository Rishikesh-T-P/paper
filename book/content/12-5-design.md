::: {.p12}

## [12.11]{.sec}Light system design for networking roles [Must · ■■□]{.tag} {#s12-11}

A design question gives a vague goal ("design the network for a new campus") and thirty-five minutes. Nobody expects a finished product. The panel watches whether the candidate asks before drawing, puts numbers on the problem, names failure modes and states trade-offs. All three designs below follow one six-step method, and each ends in a skeleton that can be redrawn from memory.

::: bigidea
A design answer is judged by its reasoning order (requirements, numbers, structure, failure), so a modest design reached in that order beats an elaborate one drawn first.
:::

### The six-step template

<figure>
<svg viewBox="0 0 480 78" width="480">
<defs><marker id="a1211" viewBox="0 0 6 6" refX="5" refY="3" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L6 3L0 6z" fill="#1A1D23"/></marker></defs>
<g class="lbl" text-anchor="middle">
<rect class="box" x="6" y="12" width="68" height="34"/><text x="40" y="27">1 Clarify</text><text class="sm" x="40" y="39">5 min</text>
<rect class="box" x="86" y="12" width="68" height="34"/><text x="120" y="27">2 Estimate</text><text class="sm" x="120" y="39">5 min</text>
<rect class="box" x="166" y="12" width="68" height="34"/><text x="200" y="27">3 Sketch</text><text class="sm" x="200" y="39">5 min</text>
<rect class="hl" x="246" y="12" width="68" height="34"/><rect class="box" x="246" y="12" width="68" height="34"/><text x="280" y="27">4 Deep-dive</text><text class="sm" x="280" y="39">10 min</text>
<rect class="box" x="326" y="12" width="68" height="34"/><text x="360" y="27">5 Failures</text><text class="sm" x="360" y="39">5 min</text>
<rect class="box" x="406" y="12" width="68" height="34"/><text x="440" y="27">6 Trade-offs</text><text class="sm" x="440" y="39">5 min</text>
</g>
<line class="ln" x1="74" y1="29" x2="86" y2="29" marker-end="url(#a1211)"/><line class="ln" x1="154" y1="29" x2="166" y2="29" marker-end="url(#a1211)"/><line class="ln" x1="234" y1="29" x2="246" y2="29" marker-end="url(#a1211)"/><line class="ln" x1="314" y1="29" x2="326" y2="29" marker-end="url(#a1211)"/><line class="ln" x1="394" y1="29" x2="406" y2="29" marker-end="url(#a1211)"/>
<text class="sm" x="240" y="68" text-anchor="middle">35 minutes in all; the deep-dive on two components is where marks are won</text>
</svg>
<figcaption><b>Figure 12.11</b> The six-step design template with a time budget.</figcaption>
</figure>

1. **Clarify.** Functional needs, then non-functional ones: scale, latency, availability, security, budget. Ask, then write the answers on the board.
2. **Estimate.** Users, requests per second, bandwidth, storage, with round numbers and stated assumptions.
3. **Sketch.** Five to eight boxes and the arrows between them.
4. **Deep-dive.** Choose the two components that carry the risk and go one level down.
5. **Failure and scale.** What breaks first, and what happens at ten times the load?
6. **Trade-offs.** Say what was given up, and what you would revisit with more time.

The numbers in step 2 are quick if a few conversions are fixed in memory.

| Quantity | Value | Use |
|---|---|---|
| 2<sup>10</sup>, 2<sup>20</sup>, 2<sup>30</sup>, 2<sup>40</sup> | about 10<sup>3</sup>, 10<sup>6</sup>, 10<sup>9</sup>, 10<sup>12</sup> | Sizes |
| Seconds in a day | 86,400 (about 10<sup>5</sup>) | Daily to per-second |
| 1 Gb/s sustained | 10.8 TB per day | Bandwidth to volume |
| Availability 99.9%, 99.99% | 8.76 hours, 52.6 minutes of downtime per year | Targets |
| Latency: same rack, same city, across India, across the world | 0.1 ms, 2 ms, 30 ms, 150 ms or more | Placement |

### Design a campus network

**Clarify.** Campus Net: five buildings, 8,000 users, wired and Wi-Fi, laboratories, hostels, guest access, CCTV and IoT, availability 99.9%, two internet providers. Ask about budget, existing cabling, and whether a data-centre room exists.

**Estimate.** Peak concurrency 40% and 2 Mb/s each gives 8,000 × 0.4 × 2 = 6,400 Mb/s = 6.4 Gb/s of internet demand. Two 10 Gb/s uplinks in active-active use give N+1 protection: after one fails, the survivor still carries 6.4 Gb/s. The 99.9% target allows 8.76 hours of downtime a year, which rules out any single-box core. With two devices per user there are about 16,000 endpoints.

**Sketch.** A hierarchical design, as in [Figure 12.12](#s12-11){.ref}: access switches in each building, a pair of distribution switches per building, a pair of core switches, and a pair of edge firewalls to the two providers.

<figure>
<svg viewBox="0 0 480 190" width="480">
<g class="lbl" text-anchor="middle">
<path class="box" d="M200 10 q20 -10 40 0 q20 -4 40 4 q8 10 -4 16 h-76 q-14 -8 0 -20z"/><text x="240" y="24">ISP 1 and ISP 2</text>
<rect class="box" x="170" y="42" width="60" height="20"/><text x="200" y="56">Firewall A</text>
<rect class="box" x="250" y="42" width="60" height="20"/><text x="280" y="56">Firewall B</text>
<rect class="box" x="170" y="82" width="60" height="20"/><text x="200" y="96">Core 1</text>
<rect class="box" x="250" y="82" width="60" height="20"/><text x="280" y="96">Core 2</text>
</g>
<line class="ln" x1="200" y1="62" x2="200" y2="82"/><line class="ln" x1="280" y1="62" x2="280" y2="82"/><line class="ln" x1="200" y1="62" x2="280" y2="82"/><line class="ln" x1="280" y1="62" x2="200" y2="82"/>
<line class="acc" x1="230" y1="92" x2="250" y2="92"/>
<line class="ln" x1="220" y1="26" x2="200" y2="42"/><line class="ln" x1="260" y1="26" x2="280" y2="42"/>
<g class="lbl" text-anchor="middle">
<rect class="fill" x="10" y="140" width="80" height="22"/><text x="50" y="154">B1 Academic</text>
<rect class="fill" x="104" y="140" width="80" height="22"/><text x="144" y="154">B2 Labs</text>
<rect class="fill" x="198" y="140" width="80" height="22"/><text x="238" y="154">B3 Library</text>
<rect class="fill" x="292" y="140" width="80" height="22"/><text x="332" y="154">B4 Hostel</text>
<rect class="fill" x="386" y="140" width="84" height="22"/><text x="428" y="154">B5 Auditorium</text>
</g>
<g class="lg">
<line x1="190" y1="102" x2="50" y2="140"/><line x1="290" y1="102" x2="50" y2="140"/>
<line x1="195" y1="102" x2="144" y2="140"/><line x1="285" y1="102" x2="144" y2="140"/>
<line x1="200" y1="102" x2="238" y2="140"/><line x1="280" y1="102" x2="238" y2="140"/>
<line x1="205" y1="102" x2="332" y2="140"/><line x1="275" y1="102" x2="332" y2="140"/>
<line x1="210" y1="102" x2="428" y2="140"/><line x1="270" y1="102" x2="428" y2="140"/>
</g>
<text class="sm" x="240" y="182" text-anchor="middle">OSPF area 0 on core links; one stub area per building summarising 10.b.0.0/16</text>
</svg>
<figcaption><b>Figure 12.12</b> Campus Net, collapsed to one line per building: dual cores, dual firewalls and dual uplinks from each building (each box contains its own distribution pair and access layer), so that no single device failure isolates a building.</figcaption>
</figure>

**Deep-dive 1: addressing and VLANs.** One /16 per building gives each distribution pair one summary route. The second octet is the building, and the third octet is the VLAN, grouped by role.

| Building | Users | Prefix | Third octet by role |
|---|---|---|---|
| B1 Academic and administration | 1,500 | 10.1.0.0/16 | 10 to 19 staff; 30 to 59 Wi-Fi |
| B2 Laboratories | 1,500 | 10.2.0.0/16 | 20 to 29 lab wired; 30 to 59 Wi-Fi |
| B3 Library and seminar halls | 1,000 | 10.3.0.0/16 | 30 to 59 Wi-Fi; 60 to 69 CCTV and IoT |
| B4 Hostels | 3,000 | 10.4.0.0/16 | 30 to 59 Wi-Fi (24 /24 subnets for 6,000 devices) |
| B5 Auditorium and sports | 1,000 | 10.5.0.0/16 | 30 to 59 Wi-Fi |
| Infrastructure | n/a | 10.250.0.0/16 | Loopbacks and /31 point-to-point links |
| Guest, data room | n/a | 10.251.0.0/16, 10.100.0.0/16 | Guest isolated; servers behind the firewall |

The hostel plan is checked by arithmetic: 3,000 users × 2 devices = 6,000 addresses, and at 254 hosts per /24 that needs 24 subnets, which fits in the 30 slots (30 to 59) reserved for Wi-Fi. Subnetting method is in [§3.4](#s3-4){.ref}.

**Deep-dive 2: resilience.** Each distribution pair runs a first-hop redundancy protocol (HSRP or VRRP, [§4.8](#s4-8){.ref}) or an anycast gateway, with the active gateway matched to the spanning-tree root. Links between layers are routed (OSPF, with BFD for sub-second failure detection), so that spanning tree is confined to one closet and equal-cost paths are used in parallel. Loss of one core switch then costs a reconvergence of a few hundred milliseconds, which TCP sessions survive; [Q12.40](#ps12){.ref} walks through it.

**Wi-Fi and security.** A wireless controller (or cloud-managed access points) maps each SSID to a VLAN: staff with WPA3-Enterprise and 802.1X, students with 802.1X or a passphrase per user, guests with a captive portal and internet-only access. CCTV and IoT sit in their own VLANs behind ACLs that allow only the recording server. DHCP snooping, dynamic ARP inspection and port security protect access ports, and the firewalls enforce zones, NAT and logging ([Pillar 9](#ch9){.ref}).

**Failure and scale.** The single points that remain are the building closet itself and the provider pair if both enter by one duct; one answer is two physical paths. At ten times the load the first limit is the firewall's throughput, not the links, so we size it by inspected Gb/s.

**Trade-offs.** A collapsed core (distribution and core on the same pair) saves cost for five buildings; the separate core is chosen here because six or more buildings would make the cabling mesh unmanageable.

### Design a rate limiter

A *rate limiter* caps how many requests a client may make in a time window, to protect a service from overload and abuse.

**Clarify.** Limit per user, per IP and per API key? A limit of, say, 100 requests per minute, with some burst allowed? Enforced on many gateway servers? Fail open (allow when the limiter is down) or fail closed? What should the client see when refused?

**Estimate.** Ten million registered users, 10% active at peak, 0.5 requests per second each: 10<sup>6</sup> × 0.5 = 500,000 checks per second. One in-memory store handles about 100,000 operations per second, so we need at least 5 shards; 8 allow headroom. State per active user is a counter and a timestamp, roughly 64 bytes, so 10<sup>6</sup> × 64 B = 64 MB in all.

| Algorithm | How it works | Strength | Weakness |
|---|---|---|---|
| Token bucket | A bucket of capacity *b* refills at rate *r*; a request takes a token | Allows bursts up to *b*; two numbers per key | Burst can be unwelcome |
| Leaky bucket | Requests join a queue drained at constant rate | Smooth output | Delays; no burst |
| Fixed window | Counter per clock minute | One counter | Up to 2 × limit around a boundary |
| Sliding-window log | Store every timestamp | Exact | Memory per request |
| Sliding-window counter | Weight the previous window by the overlap | Cheap and close to exact | Approximate |

::: example
**Limit 100 per minute with the sliding-window counter. The previous minute saw 80 requests; the current minute has 30 so far and is 15 seconds old. Allow the next request?**

1. Overlap of the sliding window with the previous minute: (60 − 15)/60 = 0.75.
2. Estimate = 80 × 0.75 + 30 = 60 + 30 = 90.
3. 90 is below 100, so the request is allowed and the counter becomes 31.

[Result: allowed; a token bucket with *r* = 10/s and *b* = 20 would likewise pass 20 requests at once, then 10 per second, i.e. 70 in the first 5 seconds.]{.result}
:::

<figure>
<svg viewBox="0 0 480 110" width="480">
<defs><marker id="a1213" viewBox="0 0 6 6" refX="5" refY="3" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L6 3L0 6z" fill="#1A1D23"/></marker></defs>
<g class="lbl" text-anchor="middle">
<rect class="box" x="10" y="36" width="64" height="30"/><text x="42" y="55">Client</text>
<rect class="box" x="120" y="36" width="80" height="30"/><text x="160" y="55">API gateway</text>
<rect class="hl" x="250" y="12" width="90" height="30"/><rect class="box" x="250" y="12" width="90" height="30"/><text x="295" y="31">Limiter shard</text>
<rect class="box" x="250" y="62" width="90" height="30"/><text x="295" y="81">Service</text>
</g>
<line class="ln" x1="74" y1="51" x2="120" y2="51" marker-end="url(#a1213)"/>
<line class="ln" x1="200" y1="44" x2="250" y2="27" marker-end="url(#a1213)"/>
<line class="ln" x1="200" y1="58" x2="250" y2="77" marker-end="url(#a1213)"/>
<line class="acc" x1="120" y1="58" x2="74" y2="58" marker-end="url(#a1213)"/>
<text class="sm" x="360" y="20">atomic check and decrement in one step</text>
<text class="sm" x="360" y="34">key = user id, hashed to a shard</text>
<text class="sm" x="360" y="84">only allowed requests reach it</text>
<text class="sm" x="97" y="80" text-anchor="middle">429 + Retry-After</text>
</svg>
<figcaption><b>Figure 12.13</b> The limiter sits at the gateway; each user maps to one shard, so a check is one network round trip.</figcaption>
</figure>

**Deep-dive.** With many gateways the counters must be shared. A store such as Redis does the check atomically with a short script or `INCR` plus `EXPIRE`, because a read followed by a write from two gateways would let both pass. A local cache of tokens at each gateway, refilled in batches, trades a small over-admission for fewer round trips. Refused clients receive HTTP 429 with a `Retry-After` header.

**Failure.** If the store is down, public read endpoints fail open and money-moving endpoints fail closed. A hot key (one abusive client) lives on one shard, which is acceptable since its traffic is mostly refused. The router analogue is the interface policer, which drops excess traffic, versus the shaper, which queues it ([§4.11](#s4-11){.ref}); the coding version is in [§1.15](#s1-15){.ref}.

### Design a CDN

A *content delivery network* stores copies of content in many *points of presence* (PoPs) near users, so that most requests never reach the origin.

**Clarify.** Static files and video; users across India and a smaller share abroad; a target hit ratio of 95%; TLS everywhere; purge within a minute.

**Estimate.** Ten million daily users at 50 MB each: 10<sup>7</sup> × 50 MB = 500 TB a day. Dividing by 86,400 s and multiplying by 8: 500 × 10<sup>12</sup> × 8 / 86,400 ≈ 46 Gb/s average, and about 140 Gb/s at three times the mean for the evening peak. With a 95% hit ratio the origin supplies only 5%: about 2.3 Gb/s average and 7 Gb/s at peak, which one origin cluster can serve.

<figure>
<svg viewBox="0 0 480 100" width="480">
<defs><marker id="a1214" viewBox="0 0 6 6" refX="5" refY="3" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L6 3L0 6z" fill="#1A1D23"/></marker></defs>
<g class="lbl" text-anchor="middle">
<rect class="box" x="6" y="34" width="60" height="30"/><text x="36" y="53">Client</text>
<rect class="box" x="96" y="6" width="80" height="26"/><text x="136" y="23">GeoDNS or anycast</text>
<rect class="hl" x="96" y="50" width="80" height="30"/><rect class="box" x="96" y="50" width="80" height="30"/><text x="136" y="69">Edge PoP</text>
<rect class="box" x="226" y="50" width="86" height="30"/><text x="269" y="69">Shield cache</text>
<rect class="box" x="362" y="50" width="76" height="30"/><text x="400" y="69">Origin</text>
</g>
<line class="ln" x1="66" y1="44" x2="96" y2="22" marker-end="url(#a1214)"/>
<line class="ln" x1="66" y1="54" x2="96" y2="62" marker-end="url(#a1214)"/>
<line class="ln" x1="176" y1="65" x2="226" y2="65" marker-end="url(#a1214)"/>
<line class="ln" x1="312" y1="65" x2="362" y2="65" marker-end="url(#a1214)"/>
<text class="sm" x="201" y="60" text-anchor="middle">miss</text><text class="sm" x="337" y="60" text-anchor="middle">miss</text>
<text class="sm" x="240" y="96" text-anchor="middle">a hit at the edge ends the journey; two miss tiers shield the origin</text>
</svg>
<figcaption><b>Figure 12.14</b> Request path in a two-tier CDN: the first hit wins, and every miss goes one tier closer to the origin.</figcaption>
</figure>

**Deep-dive 1: request routing and caching.** The client's DNS lookup for `cdn.example.com` returns the address of a nearby PoP, chosen by GeoDNS (by the resolver's location) or by anycast (the same address announced from every PoP, so BGP delivers the nearest); the comparison is in [Q12.38](#ps12){.ref}. The cache key is the URL plus the headers that change the response; the time to live comes from `Cache-Control: max-age`. Inside a PoP, consistent hashing of the key across cache servers avoids storing every object everywhere and keeps most keys in place when a server joins or leaves.

**Deep-dive 2: freshness.** Purge by key or tag through a control plane that fans out to every PoP; use versioned file names (`app.3f9a.js`) so that most files never need purging. Popular items are served from memory, long-tail items from disk, and the shield tier collapses simultaneous misses for one object into a single origin request.

**Failure and scale.** A failed PoP is withdrawn from anycast or DNS and traffic moves to the next nearest, so spare capacity of about 30% is kept. Volumetric attacks are absorbed because capacity is spread over many PoPs. The origin is protected by the shield and by serving stale content while revalidating.

**Trade-offs.** A longer TTL raises the hit ratio but delays updates; more PoPs reduce latency but increase purge cost and the number of certificates to manage.

### Variants

A layer-4 load balancer spreads connections by the five-tuple using ECMP and consistent hashing, and answers on a virtual IP; a layer-7 balancer terminates TLS and routes by URL. Global traffic management combines health-checked DNS with anycast. Details and the 1-million-connections-per-second design are in [Q12.39](#ps12){.ref} and [Pillar 5](#ch5){.ref}.

::: lens
[CISCO · JUNIPER · AMAZON · GOOGLE · NOKIA]{.co}

For networking roles the campus design is the likeliest question, then a limiter or load balancer. A strong answer opens with requirements and one calculation, draws no more than eight boxes, names a redundancy mechanism at each layer, and closes with failure modes. Expect "what if a core switch dies?", "how does this scale to ten campuses?" and "where does security sit?".
:::

::: check
1. A campus of 12,000 users, 35% concurrency at 1.5 Mb/s. Peak demand? [^c12g-1]
2. Hit ratio drops from 95% to 90% on 140 Gb/s of peak traffic. Origin load at peak before and after? [^c12g-2]
3. Which rate-limit algorithm permits a burst of *b* requests? [^c12g-3]
:::

[^c12g-1]: 12,000 × 0.35 × 1.5 = 6,300 Mb/s = 6.3 Gb/s.
[^c12g-2]: 5% of 140 = 7 Gb/s before; 10% of 140 = 14 Gb/s after, so the origin load doubles.
[^c12g-3]: The token bucket, with capacity *b*.

:::
