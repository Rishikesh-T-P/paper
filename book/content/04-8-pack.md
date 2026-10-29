::: {.p4}

::: problems
::: q
### Q4.28 Define successor, feasible successor, FD and RD. State the feasibility condition.
[CISCO · TECH-1 · ■■□ · T]{.meta}

[30-second answer: the successor is the next hop of the best path; FD is our best total metric; RD is the neighbour's own metric to the destination; a neighbour is a feasible successor if its RD is lower than our FD.]{.short}

**Answer.** The condition guarantees the neighbour's path does not pass through us, so the backup is loop-free without computation. Example in §4.6.
:::

::: q
### Q4.29 Compute the EIGRP metric for a T1 plus GigE path.
[CISCO · TECH-1 · ■■□ · S]{.meta}

[30-second answer: 256 × (10^7 / 1544 + (20,000 + 10) / 10) = 256 × (6476 + 2001) = 2,170,112.]{.short}

**Answer.** Slowest bandwidth in kb/s, sum of delays in tens of microseconds, integer division at each step, K1 = K3 = 1.
:::

::: q
### Q4.30 What is stuck-in-active, and how do stubs and summarisation prevent it?
[CISCO · TECH-2 · ■■■ · T]{.meta}

[30-second answer: a route with no feasible successor goes active and queries neighbours, who query theirs; if a reply does not return within three minutes the route is stuck in active and the neighbour is reset.]{.short}

**Answer.** Stub routers are not queried at all; a summary lets a router answer a query for a covered prefix at once, so queries stop at the summarising boundary. Also: reliable links, and feasible successors by design.
:::

::: q
### Q4.31 OSPF vs EIGRP: five differences.
[CISCO · MICROSOFT · TECH-1 · ■■□ · T]{.meta}

[30-second answer: link-state against DUAL; open against Cisco-origin; cost against bandwidth-and-delay; equal-cost only against unequal-cost balancing; areas against summarisation anywhere.]{.short}

**Answer.** A fifth point is the AD (110 against 90 and 170) and a sixth the packet transport (IP 89 against 88 with reliable delivery). The comparison table is in §4.6.
:::

::: q
### Q4.32 Why does BGP use TCP? Which port?
[ALL · TECH-1 · ■□□ · T]{.meta}

[30-second answer: BGP needs reliable, ordered delivery of large tables; TCP provides it so BGP does not need its own retransmission; the port is 179.]{.short}

**Answer.** A BGP session is long-lived and incremental: after the initial table only changes are sent, which relies on a reliable stream. The drawback is that TCP failure detection is slow, so keepalives and BFD supplement it.
:::

::: q
### Q4.33 List the BGP states. What does Active mean?
[CISCO · AMAZON · JUNIPER · TECH-1 · ■□□ · S]{.meta}

[30-second answer: Idle, Connect, Active, OpenSent, OpenConfirm, Established; Active means the router is trying to open the TCP connection and has failed, not that the session is up.]{.short}

**Answer.** Troubleshoot Idle and Active with reachability (`ping` from the update source), ACLs on TCP 179, the AS number, the update source and `ebgp-multihop`. `show ip bgp summary` prints the state in the last column.
:::

::: q
### Q4.34 eBGP vs iBGP: AD, TTL, next hop, AS_PATH.
[AMAZON · JUNIPER · ARISTA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: eBGP AD 20, TTL 1, next hop set to self, own AS prepended; iBGP AD 200, TTL 255, next hop unchanged, AS_PATH unchanged, and no re-advertisement to other iBGP peers.]{.short}

**Answer.** The unchanged next hop is why iBGP needs `next-hop-self` or an IGP route to the external link. Table in §4.7.
:::

::: q
### Q4.35 Recite the BGP best-path selection order.
[CISCO · AMAZON · JUNIPER · ARISTA · NOKIA · TECH-1 · ■■□ · S]{.meta}

[30-second answer: N WLLA OMNI: next hop reachable, weight (high), local preference (high), locally originated, AS_PATH (short), origin (low), MED (low, same neighbour AS), eBGP over iBGP, lowest IGP metric; then oldest, lowest router ID, shortest cluster list, lowest neighbour address.]{.short}

**Answer.** Walk the table of §4.7 aloud, then volunteer two reasons: weight and local preference come first because they are local policy; MED is compared only for one neighbour AS because the values of different ASes are not comparable. This is the single most reported BGP question. **Mistake.** Placing AS_PATH above local preference.
:::

::: q
### Q4.36 Weight vs local preference vs MED: scope, direction and higher or lower wins.
[AMAZON · CISCO · TECH-1 · ■■□ · T]{.meta}

[30-second answer: weight is local to one Cisco router, steers outbound, higher wins; local preference is shared in the AS by iBGP, steers outbound, higher wins; MED is sent to a neighbouring AS, hints inbound, lower wins.]{.short}

| | Scope | Steers | Wins |
|---|---|---|---|
| Weight | one router | outbound | highest |
| Local preference | whole AS | outbound | highest |
| MED | neighbour AS | inbound | lowest |
:::

::: q
### Q4.37 Why does iBGP need a full mesh? How do route reflectors and confederations solve it?
[GOOGLE · ARISTA · JUNIPER · TECH-2 · ■■□ · S]{.meta}

[30-second answer: an iBGP router does not pass iBGP-learned routes to other iBGP peers (the AS_PATH does not change inside the AS, so it cannot detect loops), so all must peer directly; a route reflector is permitted to reflect, and a confederation turns sub-ASes into eBGP.]{.short}

**Answer.** Ten routers need 45 sessions; two RRs and eight clients need 17. Clients peer only with the RR, which reflects client routes to all and non-client routes to clients. A confederation splits the AS into private sub-ASes with eBGP-like rules between them and a single public AS outward. RRs are more common.
:::

::: q
### Q4.38 How does a route reflector prevent loops? What is a cluster?
[ARISTA · JUNIPER · TECH-2 · ■■■ · T]{.meta}

[30-second answer: the RR adds ORIGINATOR_ID (the router that first injected the route) and prepends its CLUSTER_ID to CLUSTER_LIST; a router that sees its own ID, or an RR that sees its own cluster ID, discards the route.]{.short}

**Answer.** A cluster is an RR with its clients; the cluster ID defaults to the RR's router ID. If two RRs serve one cluster, give them the same cluster ID so that they ignore each other's reflections; use distinct IDs for more redundancy at the price of more state.
:::

::: q
### Q4.39 An iBGP router has the route in its BGP table but not in its RIB. Why?
[AMAZON · CISCO · TECH-1 · ■■□ · T]{.meta}

[30-second answer: usually the BGP next hop is not reachable through the IGP, so the route is not valid for installation; else a better-AD route for the same prefix exists (RIB failure).]{.short}

**Answer.** Check `show ip bgp <prefix>` (no `>`; "inaccessible"), `show ip route <next hop>`. Fix with `next-hop-self` on the border router or by carrying the link in the IGP. Also `show ip bgp rib-failure`.
:::

::: q
### Q4.40 Scenario: dual-homed to ISP-A and ISP-B. Make ISP-A primary for inbound and outbound traffic. Write the policy.
[AMAZON · CISCO · MICROSOFT · TECH-2 · ■■■ · S]{.meta}

[30-second answer: outbound, set local preference 200 on routes from ISP-A; inbound, prepend our AS two or three times on advertisements to ISP-B (and tag with the provider's low-preference community if offered).]{.short}

**Answer.** The configuration and the `show ip bgp` output are in the dual-homing example of §4.7 ([Figure 4.13](#s4-7){.ref}). **Follow-ups.** Prepending is a hint, because a remote AS with higher local preference ignores it; communities to the provider are stronger. More-specific prefixes (/25s) attract traffic strongly but are filtered by many networks beyond /24. Verify from a looking glass.
:::

::: q
### Q4.41 How does BGP multipath work? Which conditions must match? What does `multipath-relax` do?
[ARISTA · GOOGLE · AMAZON · TECH-2 · ■■■ · T]{.meta}

[30-second answer: `maximum-paths N` installs up to N paths that tie through the IGP-metric step; weight, local preference, AS_PATH length, origin, MED and the neighbouring AS must match; `as-path multipath-relax` drops the identical-AS requirement.]{.short}

**Answer.** In spine-leaf fabrics each leaf may have its own AS, so equal paths have different AS numbers; relax allows ECMP across them as long as the path lengths are equal.
:::

::: q
### Q4.42 Why is eBGP used inside large data-centre fabrics instead of OSPF (RFC 7938)?
[GOOGLE · MICROSOFT · ARISTA · AMAZON · TECH-2 · ■■■ · T]{.meta}

[30-second answer: eBGP has per-neighbour policy, no flooding of the whole topology to every router, scales to very large fabrics, and its failures are easy to reason about; one session per link needs no IGP underneath.]{.short}

**Answer.** Typical design: one AS per rack or per leaf pair, one AS for the spines, `allowas-in` or unique private ASNs, ECMP with multipath-relax, BFD for fast failure. Link-state flooding in a fabric of thousands of nodes produces churn that BGP's path-vector updates avoid. See [§5.4](#s5-4){.ref}.
:::

::: q
### Q4.43 What are BGP communities? Explain no-export and no-advertise.
[JUNIPER · NOKIA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: a community is a 32-bit tag attached to a route to signal policy; `no-export` keeps a route inside the AS (or confederation); `no-advertise` keeps it from every peer.]{.short}

**Answer.** Communities are optional transitive and are only sent if `send-community` is configured. Providers publish communities to set local preference or to blackhole.
:::

::: q
### Q4.44 Scenario: a customer announces a more-specific prefix of a major content provider. What happens globally? How do RPKI/ROV and max-prefix help?
[AMAZON · GOOGLE · MICROSOFT · TECH-2 · ■■■ · S]{.meta}

[30-second answer: routers prefer the longest prefix, so traffic for that range is drawn to the hijacker; RPKI origin validation marks the route invalid and filters it; a maximum-prefix limit stops a flood of leaked routes.]{.short}

**Answer.** Longest-prefix match, not BGP preference, decides, so the more-specific wins everywhere it is accepted. ROV compares the origin AS and maximum length against signed ROAs. Providers filter customers by prefix list and IRR data, and a max-prefix on each customer session. The 2008 YouTube incident is the textbook case.
:::

::: q
### Q4.45 Coding: given BGP paths with attributes, implement best-path selection (steps 1 to 8).
[GOOGLE · ARISTA · AMAZON · TECH-2 · ■■■ · S]{.meta}

[30-second answer: filter the candidate list step by step, keeping only the paths that are best on each attribute, and stop as soon as one remains.]{.short}

**Approach.** Eight ordered filters, each a keep-the-best on a key. MED is compared only within one neighbouring AS unless always-compare is set.

```python
from dataclasses import dataclass
ORIGIN = {"i": 0, "e": 1, "?": 2}

@dataclass
class Path:
    nh_ok: bool; weight: int; lp: int; local: bool
    as_path: list; origin: str; med: int
    ebgp: bool; igp: int; peer_as: int; rid: str

def keep(c, key, best=min):
    v = best(key(p) for p in c)
    return [p for p in c if key(p) == v]

def med_step(c, always):
    if always: return keep(c, lambda p: p.med)
    low = {}
    for p in c: low[p.peer_as] = min(low.get(p.peer_as, p.med), p.med)
    return [p for p in c if p.med == low[p.peer_as]]

def best_path(paths, always_med=False):
    c = [p for p in paths if p.nh_ok]
    steps = [lambda c: keep(c, lambda p: p.weight, max),
             lambda c: keep(c, lambda p: p.lp, max),
             lambda c: keep(c, lambda p: p.local, max),
             lambda c: keep(c, lambda p: len(p.as_path)),
             lambda c: keep(c, lambda p: ORIGIN[p.origin]),
             lambda c: med_step(c, always_med),
             lambda c: keep(c, lambda p: p.ebgp, max),
             lambda c: keep(c, lambda p: p.igp)]
    for s in steps:
        if len(c) <= 1: break
        c = s(c)
    rid = lambda p: tuple(map(int, p.rid.split(".")))
    return min(c, key=rid) if c else None
```

**Complexity.** O(8n) time, O(n) space. **Mistakes.** Comparing MED across neighbour ASes; treating higher MED as better; forgetting step 0 (unreachable next hop). Real implementations also add the age and cluster-list tie-breaks.
:::

::: q
### Q4.46 HSRP vs VRRP: which is the open standard? Default preempt?
[CISCO · TECH-1 · ■□□ · T]{.meta}

[30-second answer: VRRP is the IETF standard; HSRP is Cisco's; HSRP preempt is off by default and VRRP preempt is on.]{.short}

**Answer.** Other differences: groups addresses (224.0.0.2 or .102 against 224.0.0.18), virtual MACs and protocol (UDP 1985 against IP 112), VRRP's owner priority 255. Table in §4.8.
:::

::: q
### Q4.47 With HSRP tracking, R1's uplink fails but R1 stays active. Why?
[CISCO · TECH-1 · ■■□ · T]{.meta}

[30-second answer: tracking only lowers R1's priority; R2 takes over only if R2 has `preempt` and the new priority is below R2's, so check preempt on R2, the size of the decrement, and the track object.]{.short}

**Answer.** `show standby` displays the current priority and the tracked object's state. R1: 110 with decrement 20 becomes 90; with R2 at 100 and preempt, R2 becomes active. A decrement below the gap of 10 leaves R1 active.
:::

::: q
### Q4.48 Prefix list `10.0.0.0/8 ge 16 le 24`: which of four prefixes match?
[CISCO · JUNIPER · TECH-1 · ■■□ · S]{.meta}

[30-second answer: 10.0.0.0/8 no, 10.1.0.0/16 yes, 10.1.1.0/24 yes, 10.1.1.0/25 no.]{.short}

**Answer.** The prefix must lie inside 10.0.0.0/8 and its length must be between 16 and 24 inclusive.
:::

::: q
### Q4.49 Explain the loop from two-way redistribution at two points. How do tags fix it?
[CISCO · JUNIPER · TECH-2 · ■■■ · T]{.meta}

[30-second answer: a route redistributed from protocol A into B at one router is seen as native B by the second router, which redistributes it back into A; tags mark routes at the first redistribution, and the reverse route map denies that tag.]{.short}

**Answer.** Configuration in §4.9 ([Figure 4.15](#s4-9){.ref}). Alternatives: filter by prefix list, or raise the AD of the redistributed routes.
:::

::: q
### Q4.50 What is an MPLS label stack? Explain PHP and why implicit null exists.
[JUNIPER · NOKIA · CISCO · TECH-1 · ■■□ · T]{.meta}

[30-second answer: a stack is a sequence of 32-bit shim headers, the top one used for forwarding; the penultimate router pops the top label so that the egress router does one lookup instead of two, and the egress signals this by advertising implicit null (3).]{.short}

**Answer.** The bottom-of-stack bit marks the last label. Without PHP the egress router would pop the label and then perform an IP lookup, two lookups in a hot spot.
:::

::: q
### Q4.51 Walk a packet through an MPLS L3VPN. What do RD and RT do?
[JUNIPER · NOKIA · CISCO · TECH-2 · ■■■ · T]{.meta}

[30-second answer: the ingress PE looks up the customer's VRF and pushes a VPN label (inner) and a transport label (outer); P routers swap the transport label; the penultimate router pops it; the egress PE uses the VPN label to select the VRF and forwards by IP. RD makes prefixes unique; RT selects which VRFs import them.]{.short}

**Answer.** Walk and figure in §4.10 ([Figure 4.17](#s4-10){.ref}). Control plane: LDP for transport labels, MP-BGP VPNv4 for VPN labels.
:::

::: q
### Q4.52 Policing vs shaping: the effect on TCP flows.
[CISCO · NOKIA · BROADCOM · TECH-1 · ■■□ · T]{.meta}

[30-second answer: a policer drops or re-marks excess packets, so TCP sees loss and its window oscillates; a shaper queues them, so TCP sees extra delay but fewer losses.]{.short}

**Answer.** Shape on egress towards a slower circuit; police on ingress to enforce a contract. A shaper adds jitter, so voice goes to a priority queue ahead of it.
:::

::: q
### Q4.53 Decode DSCP 46 and AF31. Why does voice use LLQ?
[CISCO · QUALCOMM · NOKIA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: DSCP 46 is EF (101110, ToS 0xB8); AF31 is class 3, drop precedence 1: 8 × 3 + 2 × 1 = 26; voice needs low delay and jitter, which a strict-priority queue provides.]{.short}

**Answer.** LLQ is CBWFQ plus a priority queue with an implicit policer to stop starvation. Voice targets: delay 150 ms, jitter 30 ms, loss 1%.
:::

::: q
### Q4.54 How does an IPv4 multicast address map to a MAC address? Why the 32:1 ambiguity?
[CISCO · JUNIPER · BROADCOM · TECH-1 · ■■□ · T]{.meta}

[30-second answer: the low 23 bits of the group address follow the prefix 01:00:5E; a group has 28 variable bits, so 5 are lost and 32 groups share a MAC.]{.short}

**Answer.** 239.1.1.1 and 224.129.1.1 both map to 01:00:5E:01:01:01 (§4.12). The host filters again at IP level; the cost is a little CPU.
:::

::: q
### Q4.55 Explain the PIM-SM shared tree vs the shortest-path tree and the RPF check. What if unicast routing is asymmetric?
[JUNIPER · NOKIA · TECH-2 · ■■■ · T]{.meta}

[30-second answer: receivers first join a tree rooted at the RP, (\*,G); the last-hop router then switches to a tree rooted at the source, (S,G), which is shorter; the RPF check accepts a packet only on the interface the unicast table would use to reach the source.]{.short}

**Answer.** With asymmetric routing the interface that carries the stream differs from the RPF interface, so the stream is dropped. Fix with a static `ip mroute`, a multicast-specific routing table (MP-BGP), or by making the routing symmetric.
:::
:::
:::
