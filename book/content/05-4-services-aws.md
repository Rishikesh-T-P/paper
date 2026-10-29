::: {.p5}

## [5.9]{.sec}Load balancers [Must · ■■□]{.tag} {#s5-9}

::: bigidea
A load balancer presents one virtual address and spreads connections over many servers; a layer-4 balancer decides from the 5-tuple and is fast, a layer-7 balancer reads the request and is flexible, and hyperscalers build the first kind from ECMP and consistent hashing in software.
:::

A *load balancer* (LB) answers on a *virtual IP address* (VIP), chooses a *backend* server for each new connection and keeps all packets of that connection going to the same backend. A *layer-4* balancer works on addresses and ports: it never reads the payload and sees no URL. A *layer-7* balancer terminates the TCP connection (and usually TLS, [§9.4](#s9-4){.ref}), parses the HTTP request and opens a second connection to the backend, so it can route by host name or path, rewrite headers, cache and retry. The difference in cost is large, because layer 7 must hold two connections and decrypt each request.

| | Layer 4 | Layer 7 |
|---|---|---|
| Decides on | 5-tuple | URL, host, headers, cookies |
| Connection | passes packets (NAT, DSR, tunnel) | terminates and re-opens |
| TLS | passthrough | terminated here |
| Speed | millions of packets per second per node | much lower; CPU bound |
| AWS | Network Load Balancer (NLB), Gateway Load Balancer (GWLB, Geneve to appliances) | Application Load Balancer (ALB) |
| Azure | Load Balancer | Application Gateway (regional), Front Door (global) |

There are three ways for a layer-4 balancer to forward (Figure 5.16). In *NAT* (proxy) mode the balancer rewrites the destination to the backend and the reply returns through it, which also allows it to rewrite the source (SNAT). In *direct server return* (DSR) the balancer rewrites only the destination MAC (same layer-2 segment) or wraps the packet in a tunnel (IP-in-IP or GRE, any distance), and the backend replies *directly* to the client with the VIP as its source address. For the reply to be accepted by the client, the backend must own the VIP, and it is therefore configured on its loopback interface, with ARP for it suppressed (`arp_ignore=1`, `arp_announce=2` on Linux) so that the backend does not compete with the balancer for the VIP. DSR suits web traffic because responses are far larger than requests: the balancer sees only the small inbound half.

<figure>
<svg viewBox="0 0 480 232" width="480"><defs><marker id="a514" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="b514" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accf"/></marker></defs><text class="lbl" x="80" y="12" text-anchor="middle">NAT / proxy</text><rect class="box" x="54" y="22" width="52" height="18" rx="0"/><text class="lbl" x="80" y="34" text-anchor="middle">Client</text><rect class="box" x="54" y="86" width="52" height="18" rx="0"/><text class="lbl" x="80" y="98" text-anchor="middle">LB (VIP)</text><rect class="box" x="54" y="150" width="52" height="18" rx="0"/><text class="lbl" x="80" y="162" text-anchor="middle">Backend</text><text class="lbl" x="240" y="12" text-anchor="middle">DSR (direct return)</text><rect class="box" x="214" y="22" width="52" height="18" rx="0"/><text class="lbl" x="240" y="34" text-anchor="middle">Client</text><rect class="box" x="214" y="86" width="52" height="18" rx="0"/><text class="lbl" x="240" y="98" text-anchor="middle">LB (VIP)</text><rect class="box" x="214" y="150" width="52" height="18" rx="0"/><text class="lbl" x="240" y="162" text-anchor="middle">Backend</text><text class="lbl" x="400" y="12" text-anchor="middle">Tunnel (IP-in-IP / GRE)</text><rect class="box" x="374" y="22" width="52" height="18" rx="0"/><text class="lbl" x="400" y="34" text-anchor="middle">Client</text><rect class="box" x="374" y="86" width="52" height="18" rx="0"/><text class="lbl" x="400" y="98" text-anchor="middle">LB (VIP)</text><rect class="box" x="374" y="150" width="52" height="18" rx="0"/><text class="lbl" x="400" y="162" text-anchor="middle">Backend</text><line class="ln" x1="72" y1="40" x2="72" y2="86" marker-end="url(#a514)"/><text class="lbl" x="68" y="66" text-anchor="end">1</text><line class="ln" x1="72" y1="104" x2="72" y2="150" marker-end="url(#a514)"/><text class="lbl" x="68" y="130" text-anchor="end">2</text><line class="ln" x1="88" y1="150" x2="88" y2="104" marker-end="url(#a514)"/><text class="lbl" x="92" y="130" text-anchor="start">3</text><line class="ln" x1="88" y1="86" x2="88" y2="40" marker-end="url(#a514)"/><text class="lbl" x="92" y="66" text-anchor="start">4</text><line class="ln" x1="240" y1="40" x2="240" y2="86" marker-end="url(#a514)"/><text class="lbl" x="234" y="66" text-anchor="end">1</text><line class="ln" x1="240" y1="104" x2="240" y2="150" marker-end="url(#a514)"/><text class="lbl" x="234" y="130" text-anchor="end">2</text><path class="acc" d="M266,159 L290,159 L290,31 L266,31" marker-end="url(#b514)"/><text class="lbl" x="294" y="95" text-anchor="start">3</text><line class="ln" x1="400" y1="40" x2="400" y2="86" marker-end="url(#a514)"/><text class="lbl" x="394" y="66" text-anchor="end">1</text><line class="ln" x1="400" y1="104" x2="400" y2="150" marker-end="url(#a514)"/><text class="lbl" x="394" y="130" text-anchor="end">2</text><path class="acc" d="M426,159 L450,159 L450,31 L426,31" marker-end="url(#b514)"/><text class="lbl" x="454" y="95" text-anchor="start">3</text><text class="sm" x="8" y="184" text-anchor="start">1 dst = VIP</text><text class="sm" x="8" y="194" text-anchor="start">2 dst = backend, src = LB</text><text class="sm" x="8" y="204" text-anchor="start">3 reply to LB</text><text class="sm" x="8" y="214" text-anchor="start">4 src = VIP</text><text class="sm" x="170" y="184" text-anchor="start">1 dst = VIP</text><text class="sm" x="170" y="194" text-anchor="start">2 dst MAC rewritten only</text><text class="sm" x="170" y="204" text-anchor="start">3 src = VIP, direct to client</text><text class="sm" x="330" y="184" text-anchor="start">1 dst = VIP</text><text class="sm" x="330" y="194" text-anchor="start">2 outer IP to backend</text><text class="sm" x="330" y="204" text-anchor="start">3 inner src = VIP, direct</text></svg>
<figcaption><b>Figure 5.16</b> Three ways to forward to a backend. In the first the balancer sits on both directions; in the other two the reply bypasses it, so it handles only the (usually much smaller) request traffic.</figcaption>
</figure>

The balancer must also choose a backend. The common algorithms are in the table; *consistent hashing* is the one that matters at scale, because it keeps most connections on the same backend when the pool changes.

| Algorithm | Rule | Weakness |
|---|---|---|
| Round robin | next backend in turn | ignores load and request size |
| Weighted round robin | turns in proportion to weight | static weights |
| Least connections | fewest open connections | needs shared state |
| Power of two choices | pick two at random, take the less loaded | none serious; common default |
| Source or 5-tuple hash | hash of the flow | pool change reshuffles unless consistent |
| Consistent hash (Maglev) | lookup table built from per-backend permutations | table must be rebuilt on change |

::: example
**A Maglev lookup table.** Google's software balancer, Maglev (NSDI 2016), builds a table of M entries, with M prime and much larger than the number of backends; a connection is sent to `table[hash(5-tuple) mod M]`. Take M = 7 and three backends B0, B1 and B2. Each backend hashes its name into an *offset* and a *skip*, which defines a permutation of the table positions, `(offset + j × skip) mod 7`. The values are B0: offset 3, skip 4; B1: offset 0, skip 2; B2: offset 3, skip 1.

1. Permutations: B0 = 3, 0, 4, 1, 5, 2, 6; B1 = 0, 2, 4, 6, 1, 3, 5; B2 = 3, 4, 5, 6, 0, 1, 2.
2. The backends take turns, each claiming its most preferred position that is still free. Round 1: B0 takes 3, B1 takes 0, B2 wants 3 (taken) and takes 4. Round 2: B0 takes 1 (0 and 4 taken), B1 takes 2, B2 takes 5. Round 3: B0 takes 6.
3. The table is [B1, B0, B1, B0, B2, B2, B0] for positions 0 to 6: B0 has 3 entries and B1, B2 have 2 each.
4. Remove B1 and refill with B0 and B2 only. Round 1: B0 takes 3, B2 takes 4. Round 2: B0 takes 0, B2 takes 5. Round 3: B0 takes 1, B2 takes 6. Round 4: B0 takes 2. The table becomes [B0, B0, B0, B0, B2, B2, B2].
5. Compare the tables: positions 0, 2 and 6 changed, 3 of 7. Two of the changes are unavoidable (B1's own entries); the third is a side effect. A plain `hash mod N`, going from 3 backends to 2, would keep a flow only when h mod 6 is 0 or 1, so about 67% of connections move.

[Result: the new table differs in 3 of 7 entries, near the minimum of 2; a hash mod N would have moved about two thirds of the connections.]{.result}
:::

In production M is large (65,537 in the paper) so that each backend gets nearly the same number of entries, and a *connection-tracking table* on each balancer pins existing connections, so the lookup table matters only for new ones. Maglev machines are stateless peers: the edge routers spread packets over them with ECMP (§5.3), any one of them can fail, and because they all build the same table from the same backend list, a connection that lands on a different Maglev machine after a failure still reaches the same backend.

*Health checks* decide which backends are in the pool. The balancer probes each backend (a TCP connect, or an HTTP request for a given URL) at an interval and applies hysteresis: a backend moves from Up to Down after, say, three consecutive failures, and from Down back to Up only after two consecutive successes, which prevents flapping. *Session persistence* (sticky sessions) maps one client to one backend by cookie or source address, which is needed only when the application keeps per-user state in memory. A last pitfall concerns NAT mode and outbound connections: a balancer or NAT gateway has one public address and so about 64,000 source ports per destination address and port; many short connections to the same destination exhaust them, and new connections fail. This is *SNAT port exhaustion*, met again in §5.12.

::: lab
`LAB 5.9 · 2 H`  Linux IPVS in direct-routing mode, with a balancer and two backends in network namespaces on one bridge (VIP 10.1.10.100, backends 10.1.10.21 and .22).

```
ipvsadm -A -t 10.1.10.100:80 -s rr
ipvsadm -a -t 10.1.10.100:80 -r 10.1.10.21 -g
ipvsadm -a -t 10.1.10.100:80 -r 10.1.10.22 -g
ip addr add 10.1.10.100/32 dev lo          # on each backend
sysctl -w net.ipv4.conf.all.arp_ignore=1 net.ipv4.conf.all.arp_announce=2
for i in 1 2 3 4; do curl -s 10.1.10.100/id; done
ipvsadm -E -t 10.1.10.100:80 -s sh
```

```
backend1 backend2 backend1 backend2        (round robin)
backend1 backend1 backend1 backend1        (source hashing)
```

**What you should notice:** replies carry the VIP as source and never pass through the balancer (`tcpdump` on it shows only requests). Remove the `arp_ignore` setting and the backends answer ARP for the VIP, so requests sometimes skip the balancer altogether.
:::

::: trap
*Claim:* "An L4 load balancer can route /api and /images to different pools." *Why it is wrong:* it never reads the HTTP request, and with TLS passthrough it could not even decrypt it. *Correct statement:* path-based routing needs a layer-7 balancer (ALB, Application Gateway); a layer-4 balancer routes by address and port.
:::

::: check
1. Why must a DSR backend carry the VIP on its loopback? [^c59-1]
2. What advantage does DSR give the balancer? [^c59-2]
3. Why is the Maglev table size a prime much larger than the number of backends? [^c59-3]
:::

[^c59-1]: The reply leaves with the VIP as its source, and the client only accepts replies from the address it contacted.
[^c59-2]: It carries only the (small) request half of the traffic.
[^c59-3]: A prime keeps every permutation complete, and a large table gives each backend almost the same share.

## [5.10]{.sec}Anycast and content delivery networks [Should · ■■□]{.tag} {#s5-10}

::: bigidea
Announcing one prefix from many sites lets BGP deliver every user to the nearest site in routing terms, and a content delivery network adds caches at those sites so that most requests never travel to the origin.
:::

In *anycast* the same IP address is announced from several places, and the Internet's routing sends each packet to whichever announcement is best from the sender's position ([§4.7](#s4-7){.ref}). Nothing in the protocol is special; the routers simply see several paths to one prefix and choose by the usual BGP rules, usually the shortest AS_PATH, then the closest exit by IGP cost. The root name servers, public resolvers and CDNs all use it. It gives short paths, automatic failover (a site that stops announcing is removed from the table) and absorption of attacks, since flood traffic is divided among the sites by where it originates.

::: example
**Anycast from three sites.** The prefix 192.0.2.0/24 (origin AS 64496) is announced from Mumbai, Singapore and Frankfurt. A user in Chennai is behind ISP AS 64510 (Figure 5.17).

1. ISP 64510 learns three paths: AS_PATH 64496 from Mumbai, 64520 64496 from Singapore, 64530 64496 from Frankfurt.
2. BGP prefers the shortest AS_PATH, so Chennai traffic goes to Mumbai.
3. Mumbai is taken down for maintenance and withdraws the prefix. The ISP removes that path, and the best remaining path (a tie in length, broken by IGP cost) takes the traffic to Singapore within the BGP convergence time.
4. A TCP connection that was open to Mumbai now sends its segments to Singapore, which has no state for it and answers with a reset. Anycast therefore suits short exchanges (DNS, short HTTP requests) and long connections only if routing is stable.

[Result: the user lands on the BGP-nearest site, and failover is a routing withdrawal.]{.result}
:::

<figure>
<svg viewBox="0 0 480 200" width="480"><defs><marker id="a515" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accf"/></marker></defs><rect class="box" x="25" y="10" width="110" height="30" rx="0"/><text class="lbl" x="80" y="23" text-anchor="middle">Mumbai PoP</text><text class="sm" x="80" y="34" text-anchor="middle">192.0.2.0/24, AS 64496</text><rect class="box" x="185" y="10" width="110" height="30" rx="0"/><text class="lbl" x="240" y="23" text-anchor="middle">Singapore PoP</text><text class="sm" x="240" y="34" text-anchor="middle">192.0.2.0/24, AS 64496</text><rect class="box" x="345" y="10" width="110" height="30" rx="0"/><text class="lbl" x="400" y="23" text-anchor="middle">Frankfurt PoP</text><text class="sm" x="400" y="34" text-anchor="middle">192.0.2.0/24, AS 64496</text><rect class="box" x="190" y="100" width="100" height="26" rx="0"/><text class="lbl" x="240" y="113" text-anchor="middle">ISP, Chennai side</text><text class="sm" x="240" y="122" text-anchor="middle">AS 64510</text><line class="lg" x1="80" y1="40" x2="240" y2="100"/><line class="lg" x1="240" y1="40" x2="240" y2="100"/><line class="lg" x1="400" y1="40" x2="240" y2="100"/><path class="acc" d="M80,40 L225,100"/><text class="sm" x="100" y="76" text-anchor="end">AS_PATH 64496</text><text class="sm" x="250" y="64" text-anchor="start">64520 64496</text><text class="sm" x="390" y="76" text-anchor="end">64530 64496</text><rect class="fill" x="205" y="150" width="70" height="22" rx="0"/><text class="lbl" x="240" y="164" text-anchor="middle">User, Chennai</text><line class="ln" x1="240" y1="126" x2="240" y2="150"/><text class="sm" x="240" y="190" text-anchor="middle">Shortest AS_PATH wins; if Mumbai withdraws, the next-best path (Singapore) takes over.</text></svg>
<figcaption><b>Figure 5.17</b> One prefix announced from three sites. The ISP's router picks one path by ordinary BGP rules, so each user lands on the site that is nearest in routing terms, not necessarily in kilometres.</figcaption>
</figure>

A *CDN* places *edge* caches at such sites. A request first needs the CDN's address: the site's name is a CNAME to the CDN's domain, and the CDN's DNS server either returns an anycast address or, in *DNS-based global server load balancing*, returns the address of the edge it judges best for the client's resolver. DNS-based steering can use measured latency and load but sees only the *resolver's* address, so the extension *EDNS Client Subnet* passes a prefix of the client's address to the authoritative server. An edge that holds the object (a *hit*) replies at once; on a *miss* it fetches the object from a mid-tier cache or the origin, stores it according to the `Cache-Control` and TTL headers, and replies.

::: example
**What a CDN saves.** The origin is 220 ms away, the edge 15 ms away, and 90% of requests hit.

1. A hit costs the edge round trip: 15 ms.
2. A miss costs the edge plus the origin trip: 15 + 220 = 235 ms.
3. The expected time is 0.9 × 15 + 0.1 × 235 = 13.5 + 23.5 = 37 ms, against 235 ms with no cache.
4. Raising the hit ratio to 99% gives 0.99 × 15 + 0.01 × 235 = 17.2 ms. Each point of hit ratio is worth about 2.2 ms here.

[Result: 37 ms expected, about six times faster than going to the origin every time.]{.result}
:::

| | DNS-based steering | Anycast |
|---|---|---|
| Decision made by | the CDN's DNS server, from the resolver's address | BGP, from the user's network position |
| Failover speed | bounded by DNS TTL and client caching | BGP convergence (seconds) |
| Granularity | per resolver or client subnet; can use load and latency | coarse; by path length |
| Weakness | the resolver may be far from the client | route changes break long connections |

::: lab
`LAB 5.10 · 90 MIN`  Containerlab: three "PoP" nodes (FRR) each announce 192.0.2.1/32 by eBGP to one transit router, with a client behind it. Give the PoPs different AS_PATH lengths by prepending.

```
client# traceroute -n 192.0.2.1
vtysh -c 'clear bgp *'   # after shutting the PoP that answered
```

```
 2  10.9.0.2     (transit)
 3  192.0.2.1    pop1
 3  192.0.2.1    pop2        (after pop1 is shut down)
```

**What you should notice:** all three PoPs hold the same address, and the traceroute shows the one with the shortest path; when it fails the answer moves after BGP converges, and a TCP connection opened before the failure is reset.
:::

::: trap
*Claim:* "Anycast sends a user to the geographically nearest site." *Why it is wrong:* BGP knows paths, not kilometres; a user may be served from another continent when their ISP peers with the CDN there. *Correct statement:* anycast selects the BGP-nearest site, and operators influence this by choosing where to announce and by prepending.
:::

::: check
1. What does BGP use to choose between anycast sites? [^c510-1]
2. What happens to an open TCP connection when the route changes to another site? [^c510-2]
3. Compute the expected latency for a 95% hit ratio, edge 20 ms and origin 180 ms. [^c510-3]
:::

[^c510-1]: The ordinary best-path rules: usually shortest AS_PATH, then lowest IGP cost to the exit.
[^c510-2]: The new site has no state for it and resets it (unless the sites share connection state).
[^c510-3]: 0.95 × 20 + 0.05 × 200 = 19 + 10 = 29 ms.

## [5.11]{.sec}AWS: the Virtual Private Cloud [Must · ■■□]{.tag} {#s5-11}

::: bigidea
A VPC is a private network that the provider simulates in software, scoped to one region, in which routing is explicit (route tables decide what is public) and filtering is done at two levels, a stateful security group at each interface and a stateless network ACL at each subnet.
:::

The fabric of the preceding sections is invisible to a cloud customer; what the customer sees is a virtual network that behaves like the campus network of Pillar 4. In Amazon Web Services this is the *Virtual Private Cloud* (VPC). A VPC is created in one region with an address block between /16 and /28, for example 10.0.0.0/16. It is divided into *subnets*, and each subnet lives in exactly one *availability zone* (AZ), a physically separate data-centre group within the region, so that high availability means placing one subnet in each of two or more AZs. Within the VPC every subnet can reach every other through an implicit router; the *route table* attached to a subnet decides where all other traffic goes. A VPC has a ready-made route "local" for its own block and nothing else; every other route is added by the customer.

A subnet is *public* if its route table contains a default route (0.0.0.0/0) to an *internet gateway* (IGW), a horizontally scaled, redundant gateway that translates between private addresses and public ones. It is *private* if the default route instead points to a *NAT gateway*, which sits in a public subnet and lets instances start outbound connections while blocking unsolicited inbound ones ([§3.6](#s3-6){.ref}), or if there is no default route at all. Being public also requires the instance to hold a public or Elastic IP address; the route alone is not enough. Note that AWS reserves five addresses in every subnet: the network address (.0), the VPC router (.1), the DNS resolver (.2), one held for future use (.3) and the broadcast address (the last), so a /24 offers 251 usable addresses, not 254.

::: example
**A three-tier web application across two AZs.** The VPC is 10.0.0.0/16 (Figure 5.18).

1. Subnets: public 10.0.1.0/24 (AZ a) and 10.0.2.0/24 (AZ b); private application 10.0.11.0/24 and 10.0.12.0/24; database 10.0.21.0/24 and 10.0.22.0/24. Each has 256 − 5 = 251 usable addresses.
2. Route tables: *public* has 10.0.0.0/16 local and 0.0.0.0/0 to the IGW. Each *application* table has 10.0.0.0/16 local and 0.0.0.0/0 to the NAT gateway in the same AZ (a gateway in a single AZ would be a shared failure point). The *database* table has only the local route, so the database cannot reach the Internet at all.
3. Security groups: ALB-SG allows TCP 443 from 0.0.0.0/0. App-SG allows TCP 8080 *from ALB-SG* (a rule that names a group, not an address range, so it follows instances as they scale). DB-SG allows TCP 5432 from App-SG. No other inbound rule exists.
4. Network ACL on the public subnets: inbound allow TCP 443 from 0.0.0.0/0; outbound allow TCP 1024 to 65535 to 0.0.0.0/0. The outbound rule is the *ephemeral-port* rule: the client's source port is chosen from a high range, and since a network ACL remembers nothing, the reply must be explicitly allowed. Omitting it makes an otherwise correct design hang.
5. Return traffic through the security groups needs no rule, because they are stateful.

[Result: only the load balancer is exposed; each tier admits only the tier above it; the database has no route out.]{.result}
:::

<figure>
<svg viewBox="0 0 480 258" width="480"><defs></defs><rect class="lg dash" x="4" y="4" width="472" height="248" rx="6"/><text class="sm" x="14" y="16" text-anchor="start">Region (for example ap-south-1)</text><rect class="box" x="10" y="34" width="322" height="212" rx="3"/><text class="lbl" x="18" y="46" text-anchor="start">VPC 10.0.0.0/16</text><rect class="box" x="124" y="22" width="64" height="18" rx="0"/><text class="lbl" x="156" y="34" text-anchor="middle">IGW</text><line class="ln" x1="156" y1="40" x2="156" y2="64"/><text class="sm" x="90" y="60" text-anchor="middle">AZ a</text><rect class="fill" x="18" y="66" width="148" height="60" rx="2"/><text class="sm" x="22" y="76" text-anchor="start">public 10.0.1.0/24</text><rect class="box" x="108" y="98" width="52" height="20" rx="0"/><text class="sm" x="134" y="111" text-anchor="middle">NAT GW</text><rect class="fill" x="18" y="132" width="148" height="48" rx="2"/><text class="sm" x="22" y="142" text-anchor="start">private app 10.0.11.0/24</text><rect class="box" x="108" y="150" width="52" height="22" rx="0"/><text class="lbl" x="134" y="164" text-anchor="middle">EC2</text><rect class="fill" x="18" y="186" width="148" height="52" rx="2"/><text class="sm" x="22" y="196" text-anchor="start">private db 10.0.21.0/24</text><rect class="box" x="108" y="206" width="52" height="22" rx="0"/><text class="lbl" x="134" y="220" text-anchor="middle">RDS</text><line class="lg" x1="134" y1="118" x2="134" y2="150"/><text class="sm" x="246" y="60" text-anchor="middle">AZ b</text><rect class="fill" x="174" y="66" width="148" height="60" rx="2"/><text class="sm" x="178" y="76" text-anchor="start">public 10.0.2.0/24</text><rect class="box" x="264" y="98" width="52" height="20" rx="0"/><text class="sm" x="290" y="111" text-anchor="middle">NAT GW</text><rect class="fill" x="174" y="132" width="148" height="48" rx="2"/><text class="sm" x="178" y="142" text-anchor="start">private app 10.0.12.0/24</text><rect class="box" x="264" y="150" width="52" height="22" rx="0"/><text class="lbl" x="290" y="164" text-anchor="middle">EC2</text><rect class="fill" x="174" y="186" width="148" height="52" rx="2"/><text class="sm" x="178" y="196" text-anchor="start">private db 10.0.22.0/24</text><rect class="box" x="264" y="206" width="52" height="22" rx="0"/><text class="lbl" x="290" y="220" text-anchor="middle">RDS</text><line class="lg" x1="290" y1="118" x2="290" y2="150"/><rect class="box" x="20" y="80" width="296" height="14" rx="2"/><text class="sm" x="168" y="90" text-anchor="middle">Application Load Balancer (spans both public subnets)</text><path class="acc" d="M156,64 L156,80"/><text class="lbl" x="342" y="44" text-anchor="start">Public route table</text><text class="mono" x="342" y="55" text-anchor="start">10.0.0.0/16  local</text><text class="mono" x="342" y="65" text-anchor="start">0.0.0.0/0  igw-…</text><text class="lbl" x="342" y="96" text-anchor="start">App route table (per AZ)</text><text class="mono" x="342" y="107" text-anchor="start">10.0.0.0/16  local</text><text class="mono" x="342" y="117" text-anchor="start">0.0.0.0/0  nat-… (same AZ)</text><text class="lbl" x="342" y="148" text-anchor="start">Database route table</text><text class="mono" x="342" y="159" text-anchor="start">10.0.0.0/16  local</text></svg>
<figcaption><b>Figure 5.18</b> The three-tier VPC of the worked example. A subnet is public only because its route table points at the internet gateway; the private subnets reach the internet through the NAT gateway in their own AZ.</figcaption>
</figure>

| | Security group | Network ACL |
|---|---|---|
| Attached to | network interface (ENI) | subnet |
| State | stateful: replies allowed automatically | stateless: both directions need rules |
| Rule types | allow only | allow and deny |
| Evaluation | all rules together, no order | by rule number, lowest first, first match wins; final deny |
| Default | deny inbound, allow outbound | default ACL allows all; a new custom ACL denies all |
| Can reference | other security groups | address ranges only |

Connecting VPCs is the next question. *VPC peering* joins two VPCs with a private link; it needs non-overlapping address blocks and a route in each VPC's tables. Peering is *not transitive*: if A peers with B and B with C, then A cannot reach C through B, and neither can A use B's internet gateway or VPN. Connecting n VPCs in a full mesh needs n(n − 1)/2 peerings: for 50 VPCs that is 1,225. A *transit gateway* (TGW) is a regional hub-and-spoke router: each VPC, VPN and Direct Connect (§5.13) is an *attachment*, and TGW route tables, with *association* and *propagation*, decide which attachment can reach which, so 50 VPCs need 50 attachments and segmentation is expressed in the route tables. *PrivateLink* exposes one *service* (behind a network load balancer) to another VPC through an *interface endpoint*, a network interface with a private address in the consumer's subnet. It is one-way and works even when the address blocks overlap. *Gateway endpoints* reach S3 and DynamoDB through a route-table entry rather than the Internet.

AWS builds these networks by host-based software: the Nitro cards of each server encapsulate packets in a VPC-aware tunnel, apply security groups and answer ARP requests from a mapping service, which is why a VPC has no broadcast and why the underlying switches stay a plain routed fabric (§5.5). *VPC Flow Logs* record accepted and rejected connections per interface and are the first tool for the diagnoses of [Pillar 11](#ch11){.ref}.

::: lab
`LAB 5.11 · 3 H`  An AWS free-tier account, console or CLI. Create a VPC 10.0.0.0/16 with a public and a private subnet, an IGW, a bastion in the public subnet and an instance in the private subnet, and enable Flow Logs. Then add a network ACL to the public subnet that allows inbound TCP 22 but no outbound ephemeral ports.

```
aws ec2 create-vpc --cidr-block 10.0.0.0/16
aws ec2 create-route --route-table-id rtb-... --destination-cidr-block 0.0.0.0/0 --gateway-id igw-...
ssh -o ConnectTimeout=5 ec2-user@<bastion-public-ip>
```

**What you should notice:** with the ephemeral rule missing, SSH hangs at the connect stage while the security group looks correct; Flow Logs show an ACCEPT for the inbound packet and no reply, because the NACL silently drops the response. Adding outbound TCP 1024 to 65535 repairs it. **Cost:** a NAT gateway is billed hourly, so use a NAT instance or skip it, and delete everything afterwards.
:::

::: trap
*Claim:* "VPC peering is transitive, and I can add a deny to a security group." *Why it is wrong:* peering joins exactly two VPCs, and security groups contain only allow rules. *Correct statement:* use a transit gateway for many VPCs, a network ACL for an explicit deny, and remember that peered VPCs cannot have overlapping blocks.
:::

::: lens
[AMAZON · MICROSOFT · GOOGLE]{.co}

Amazon's network development engineer loops ask "security group versus network ACL" and the scenario "an instance in a private subnet cannot reach the Internet; list the checks in order" (route table, NAT gateway state and placement, the NAT's own route to the IGW, outbound rules, DNS, then the instance's own firewall). Start from the route and finish at the host.
:::

::: check
1. Why does a /24 subnet in AWS have 251 usable addresses? [^c511-1]
2. Which of the two filters needs an ephemeral-port rule, and why? [^c511-2]
3. How many peerings does a full mesh of 10 VPCs need? [^c511-3]
:::

[^c511-1]: Five addresses are reserved: network, router, DNS, future use and broadcast.
[^c511-2]: The network ACL, because it is stateless and the reply goes to a high source port.
[^c511-3]: 10 × 9 ÷ 2 = 45.

:::
