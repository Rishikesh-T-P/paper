::: {.p11}

::: pack
## Problem Set {#ps11}

Each solution opens with the 30-second answer. Tags give the companies that report the topic, the round, the difficulty (■□□ to ■■■) and the evidence: S for a specific reported question, T for a reported topic with our wording. Cases referred to are in [§11.8](#s11-8){.ref}.

::: problems
::: q
### Q11.1 Describe your general approach to troubleshooting a network problem.
[CISCO · GOOGLE · AMAZON · TECH-1 · ■□□ · T]{.meta}

[30-second answer: restate the symptom, ask scope, timeline and change questions, rank hypotheses, test them layer by layer saying the expected output, name a root cause that explains everything, fix with a rollback, then verify and prevent.]{.short}

**Answer.** Name the method (SCALPEL, [§11.2](#s11-2){.ref}) and the strategy: divide and conquer from Layer 3 by default. **Mistakes.** Listing commands without a purpose; no closure.
:::

::: q
### Q11.2 A user cannot reach a website. What are the first three checks and why?
[CISCO · GOOGLE · TECH-1 · ■□□ · T]{.meta}

[30-second answer: (i) scope and error text, to know whether it is one user, one site or all; (ii) `ping` the gateway and then a public IP, which tests Layers 1 to 3 in two steps; (iii) `nslookup` or `dig` the name, to separate DNS from connectivity.]{.short}

**Answer.** Only then `curl -v` to see the TCP and HTTP layers. Each check discards a layer: a gateway ping proves the local link and VLAN, a public ping proves routing and NAT, and a successful IP with a failed name is [Case 1](#c11-1){.ref}.
:::

::: q
### Q11.3 What is the difference between a connection timeout and connection refused?
[CISCO · GOOGLE · AMAZON · TECH-1 · ■□□ · S]{.meta}

[30-second answer: a timeout means no answer, so the packet was dropped somewhere; a refusal is a RST from a reachable host with nothing listening, or a firewall REJECT.]{.short}

**Answer.** On the wire, a timeout is SYN retransmissions at 1 s, 3 s and 7 s; a refusal is a SYN followed within a millisecond by a RST ([Figure 11.6](#s11-6){.ref}). Hence a refusal proves the path works. **Follow-up.** For UDP, a closed port returns ICMP port unreachable.
:::

::: q
### Q11.4 Top-down, bottom-up and divide and conquer: when would you use each?
[CISCO · GOOGLE · TECH-1 · ■□□ · T]{.meta}

[30-second answer: bottom-up after a physical change, top-down when one application fails, and divide and conquer from Layer 3 when many hops are involved and there is no other clue.]{.short}

**Answer.** Divide and conquer halves the search with each test; in [Figure 11.5](#s11-4){.ref} two pings isolate one of five links. Add follow the packet for routing faults, compare with working when one of two similar things fails, and swap when counters implicate hardware. **Mistake.** Always starting at Layer 1.
:::

::: q
### Q11.5 What do "up/down" and "administratively down" mean on a Cisco interface?
[CISCO · JUNIPER · TECH-1 · ■□□ · T]{.meta}

[30-second answer: the first word is the physical state and the second the line protocol (Layer 2); "administratively down" means someone typed `shutdown`.]{.short}

| Status / protocol | Meaning |
|---|---------------------|
| up / up | Healthy |
| up / down | Carrier present, Layer 2 failing: encapsulation, keepalives, clocking; for an SVI, no active port in the VLAN |
| down / down | No signal: cable, remote shut, wrong optic |
| administratively down | Shut by configuration |
| err-disabled | A protection (BPDU Guard, port security) closed it |
:::

::: q
### Q11.6 A host gets a 169.254.x.x address. What does that tell you?
[CISCO · AMAZON · TECH-1 · ■□□ · T]{.meta}

[30-second answer: the host asked for DHCP and received no answer, so it assigned itself a link-local address (APIPA).]{.short}

**Answer.** Layer 2 may be fine; test with a static address. Then check the relay on the SVI, the scope, snooping trust and the server. See [Case 12](#c11-12){.ref}. **Mistake.** Assuming the DHCP server is down before checking the relay.
:::

::: q
### Q11.7 How do you check whether a switch has learned a host's MAC, and on which port?
[CISCO · JUNIPER · ARISTA · TECH-1 · ■□□ · T]{.meta}

[30-second answer: `show mac address-table address <mac>` on IOS, `show ethernet-switching table` on Junos, `bridge fdb show` on Linux; the host must have sent a frame recently.]{.short}

**Answer.** Find the MAC from the host (`ipconfig /all`) or from `show ip arp`. If absent, generate traffic (a ping) and look again; entries age out after 300 s. The port shown leads you one hop towards the host; repeat on that switch until you reach an access port.
:::

::: q
### Q11.8 Two hosts in the same VLAN on different switches cannot communicate. Walk through it.
[CISCO · JUNIPER · ARISTA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: the VLAN is missing somewhere between the two ports: check the trunk allowed list, that the VLAN exists on both switches, the native VLAN, and spanning-tree state for that VLAN.]{.short}

**Answer.** `show interfaces trunk` is the decisive command; compare the allowed, active and forwarding lists. The cause in [Case 2](#c11-2){.ref} was `allowed vlan 10` replacing the list. **Follow-up.** After the fix, check that both MACs are learnt.
:::

::: q
### Q11.9 OSPF neighbours are stuck in ExStart. Likely cause and fix?
[CISCO · JUNIPER · NOKIA · ARISTA · AMAZON · TECH-1 · ■■□ · T]{.meta}

[30-second answer: an interface MTU mismatch, because a router rejects database descriptions advertising a larger MTU than its own; make the MTUs equal.]{.short}

**Answer.** Prove it with `debug ip ospf adj` ("larger interface MTU") and `show interfaces | include MTU`. `ip ospf mtu-ignore` masks the problem. Other causes of a stall: duplicate router ID, unicast loss on non-broadcast networks. Full case: [Case 6](#c11-6){.ref}.
:::

::: q
### Q11.10 List everything that must match for two OSPF routers to become neighbours.
[CISCO · JUNIPER · NOKIA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: subnet and mask, area ID, hello and dead timers, authentication, stub flags, a compatible network type, a unique router ID, a non-passive interface, and nothing blocking 224.0.0.5 and 224.0.0.6.]{.short}

**Answer.** MTU must also match for the exchange to complete. These need not match: process ID, priority, cost, interface name. Use the list as the hypothesis list ([Case 7](#c11-7){.ref}).
:::

::: q
### Q11.11 BGP Active versus Idle: what does each mean, and how do you troubleshoot?
[AMAZON · GOOGLE · CISCO · JUNIPER · ARISTA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: Idle means the speaker is not attempting a connection (down, no route, or in back-off); Active means it is trying to open TCP and failing, so check the address, the path and TCP 179 filters.]{.short}

**Answer.** Ping and `telnet peer 179` from the same source the session uses; check the update-source, `ebgp-multihop` for loopbacks, and ACL hit counts. NOTIFICATION messages indicate AS, timer or MD5 faults. Full case: [Case 8](#c11-8){.ref}.
:::

::: q
### Q11.12 BGP is Established but a prefix is not advertised. Why?
[AMAZON · GOOGLE · ARISTA · JUNIPER · TECH-1 · ■■□ · T]{.meta}

[30-second answer: a `network` statement originates a prefix only if an exact match is in the routing table; otherwise check outbound policy, then the peer's inbound filters.]{.short}

**Answer.** `show ip route <prefix> <mask>`, `show ip bgp <prefix>`, `advertised-routes`. If an internal router learns it but does not use it, the next hop is unreachable: use `next-hop-self` ([Case 9](#c11-9){.ref}). **Follow-up.** RPKI and IRR filters at the provider.
:::

::: q
### Q11.13 Small packets work and large packets fail. Explain and fix.
[GOOGLE · AMAZON · CISCO · JUNIPER · TECH-1 · ■■□ · T]{.meta}

[30-second answer: the path MTU is smaller than the packet and the ICMP "fragmentation needed" message is lost, so a black hole forms; allow ICMP type 3 code 4 and clamp the MSS.]{.short}

**Answer.** Test with `ping -M do -s <size>`; find the largest passing size and add 28 for the MTU. Tunnels are the usual cause ([Case 5](#c11-5){.ref}). Clamp the MSS to MTU minus 40. For IPv6, Packet Too Big must not be filtered.
:::

::: q
### Q11.14 An interface shows increasing CRC errors. What causes it, and how do you prove which?
[CISCO · QUALCOMM · ARISTA · BROADCOM · TECH-1 · ■■□ · T]{.meta}

[30-second answer: corrupted frames from a bad cable, a weak optic, interference or a duplex mismatch; take two snapshots to prove the counter is rising, check duplex and optical power, then swap the cable.]{.short}

**Answer.** Duplex mismatch is shown by late collisions on the other side and a half-duplex entry. An optic fault is shown by `show interfaces transceiver` (Rx power below the threshold). Clean the fibre or swap the part after saving the counters.
:::

::: q
### Q11.15 Duplex mismatch: symptoms on each side?
[CISCO · QUALCOMM · BROADCOM · TECH-1 · ■■□ · T]{.meta}

[30-second answer: the half-duplex side shows late collisions and runts; the full-duplex side shows CRC and frame errors; bulk TCP is very slow while interactive traffic seems fine.]{.short}

**Answer.** Cause: one end forced and the other on auto. Fix both to auto. Full case: [Case 4](#c11-4){.ref}.
:::

::: q
### Q11.16 A server is intermittently unreachable for 30 seconds at a time. Causes?
[CISCO · AMAZON · GOOGLE · TECH-1 · ■■□ · T]{.meta}

[30-second answer: a duplicate IP address, a flapping link or a Layer 2 loop, ARP or lease expiry, a bad ECMP member, or a first-hop redundancy split-brain; correlate the outage times with logs.]{.short}

**Answer.** The decisive checks are `%IP-4-DUPADDR`, `show ip arp` flipping between two MACs, and MAC-flap messages ([Case 10](#c11-10){.ref}). Ask whether the pattern is periodic, because a period often equals a timer.
:::

::: q
### Q11.17 How would you detect and stop a broadcast storm?
[CISCO · JUNIPER · NOKIA · ARISTA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: detect by a broadcast-rate alarm, 100 per cent CPU and MAC-flap logs; stop it by shutting the offending port, then prevent with BPDU Guard, storm control and loop protection.]{.short}

**Answer.** Mitigate first by shutting the port that shows the highest broadcast input rate. Find the loop from the MAC flaps between two ports. See [Case 11](#c11-11){.ref}. Frames have no TTL, which is why the storm persists.
:::

::: q
### Q11.18 How would you use `tcpdump` to decide whether a firewall is dropping traffic?
[GOOGLE · AMAZON · ARISTA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: capture on both sides of the firewall with the same filter; if the SYN is seen on the inside interface and not on the outside, the firewall drops it, and if the SYN leaves but nothing returns, the fault is beyond.]{.short}

**Answer.** Use `tcpdump -ni <if> 'host X and port Y'` at each interface, in the same minute. A SYN seen at the server with no SYN-ACK leaving points at the host; a SYN-ACK seen leaving but not arriving back points at the return path or the firewall state ([Case 13](#c11-13){.ref}).
:::

::: q
### Q11.19 IPsec Phase 1 is up, Phase 2 is down. Diagnose.
[CISCO · JUNIPER · NOKIA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: Phase 1 only proves the peers authenticate; Phase 2 fails on mismatched traffic selectors or proxy IDs, transform sets, PFS groups, or lifetimes.]{.short}

**Answer.** Read the debug (`TS_UNACCEPTABLE` or `NO_PROPOSAL_CHOSEN`) and compare both configurations. Once the child SA is up, if encapsulation counts rise but decapsulation stays zero, check the NAT exemption and the return route ([Case 15](#c11-15){.ref}).
:::

::: q
### Q11.20 Traceroute shows `* * *` at hop 5 but the destination is reachable. Explain.
[GOOGLE · CISCO · AMAZON · TECH-1 · ■□□ · T]{.meta}

[30-second answer: that router does not answer TTL-exceeded probes (it filters or rate-limits ICMP) but still forwards transit traffic, so it is not a fault.]{.short}

**Answer.** Traceroute depends on the router's cooperation; forwarding does not. Confirm by observing that later hops answer and the destination is reached. See [Case 18](#c11-18){.ref}. **Mistake.** Reporting hop 5 as the break.
:::

::: q
### Q11.21 (Cisco style) Two networks are joined by routers and switches; PC-A cannot reach PC-B. Ask questions and solve it.
[CISCO · JUNIPER · TECH-2 · ■■■ · S]{.meta}

[30-second answer: restate the symptom; ask for addresses, what fails, what does work, whether it ever worked, the routing protocol, the change history and the access to outputs; state the scenario back in one sentence; then walk Layer 3 first by pinging gateways.]{.short}

**Answer.** The full transcript with timestamps is [Round 1](#m11-1){.ref} of [§11.9](#s11-9){.ref}, where two stacked faults (a trunk list and a missing relay) are found. The scoring turns on the clarification: eight questions defined the scenario in [Figure 11.3](#s11-3){.ref}. **Mistake.** Proposing a fix after the first finding.
:::

::: q
### Q11.22 (Google style) Users report "the internet is slow." Define slow, then troubleshoot end to end.
[GOOGLE · TECH-2 · ■■■ · S]{.meta}

[30-second answer: turn "slow" into latency, loss or throughput with a measurement and a scope; then compare a slow and a fast client with `curl -w` timings, `mtr` and counters, and follow the evidence along the path.]{.short}

**Answer.** The timing split (DNS, connect, first byte, transfer) shows which phase is slow. Transfer-phase slowness with equal setup times means loss or a window limit. The transcript is [Round 2](#m11-2){.ref}.
:::

::: q
### Q11.23 Some users are always slow and others never, in a leaf-spine fabric. How can ECMP cause that, and how do you find the bad link?
[GOOGLE · MICROSOFT · AMAZON · ARISTA · TECH-2 · ■■■ · T]{.meta}

[30-second answer: ECMP hashes each flow's five-tuple onto one of several equal paths, so a user whose flows hash to a lossy path is slow every time; find it by error counters and optics on each member.]{.short}

**Answer.** Consistency per user, with no pattern by floor, is the signature. Confirm with `mtr` from a slow client, then `show interfaces counters errors` and `show interfaces transceiver` on each uplink. Drain the member. See [Case 14](#c11-14){.ref}.
:::

::: q
### Q11.24 After adding a second ISP, some TCP sessions break. Why, and how do you fix it architecturally?
[CISCO · JUNIPER · NOKIA · GOOGLE · AMAZON · TECH-2 · ■■■ · T]{.meta}

[30-second answer: replies return through a different stateful firewall that has no state for the session and drops them; make the paths symmetric or share state.]{.short}

**Answer.** Options: source NAT per ISP, policy routing, an active-standby pair, or a cluster with state synchronisation. Avoid ECMP across independent stateful devices. Evidence: "no connection" drops on one firewall ([Case 13](#c11-13){.ref}).
:::

::: q
### Q11.25 A single TCP flow over a long link is slow, but parallel flows are fine. Diagnose.
[GOOGLE · MICROSOFT · AMAZON · BROADCOM · TECH-2 · ■■■ · T]{.meta}

[30-second answer: a single stream is window-limited: throughput cannot exceed window divided by round-trip time, so compare the bandwidth-delay product with the window and check scaling and buffers.]{.short}

**Answer.** 64 KB over 80 ms is about 6.5 Mb/s, against a BDP of 10 MB on 1 Gb/s. Check `wscale` in `ss -ti`, the SYN at both ends and `tcp_rmem`. Parallel streams each carry a window, hence they sum up. See [Case 17](#c11-17){.ref}.
:::

::: q
### Q11.26 Production is down for 2,000 users after a change you made ten minutes ago. What do you do, minute by minute?
[GOOGLE · AMAZON · MICROSOFT · TECH-2 · HM · ■■■ · S]{.meta}

[30-second answer: declare an incident, roll the change back, tell stakeholders, verify recovery, and only then find the cause and write a blameless post-mortem.]{.short}

| Minute | Action |
|---|-----------------------------|
| 0 | Confirm the outage from monitoring, not only the report; state the time of the change |
| 1 | Declare Sev 1; name a commander, an operator and a scribe |
| 2 | Save current state: `show running-config`, logs, counters, for the post-mortem |
| 3 | Roll back the change (`configure replace` or the saved configuration) |
| 5 | Post the first update: impact, action under way, next update time |
| 7 | Verify with the test that failed (pings, a user check, monitoring green) |
| 10 | If not restored, fail over or drain; keep updates every 30 minutes |
| After | Reproduce in a lab, find the root cause, hold the blameless review ([§11.7](#s11-7){.ref}) |

**Mistake.** Investigating before rolling back, or rolling back without saving the evidence.
:::

::: q
### Q11.27 How do you troubleshoot a problem you cannot reproduce?
[GOOGLE · AMAZON · TECH-2 · ■■■ · T]{.meta}

[30-second answer: make the fault observable: add monitoring and a rolling packet capture at the suspected point, correlate the reported times with logs and changes, and form hypotheses from the pattern.]{.short}

**Answer.** (i) Ask for exact timestamps and affected hosts. (ii) Keep a circular capture (`tcpdump -C ... -W ...`) or flow records at both ends. (iii) Look for periodicity, which suggests timers, lease expiry or scheduled jobs. (iv) Compare the affected with the unaffected. (v) Change one variable at a time and record it.
:::

::: q
### Q11.28 Write a script that detects interface-error increases across 100 devices and alerts.
[AMAZON · GOOGLE · ARISTA · TECH-2 · ■■■ · T]{.meta}

[30-second answer: poll `show interfaces` concurrently, parse the error counter per interface, compare it with the previous poll and alert on a delta above a threshold; handle counter resets.]{.short}

**Code (Python).** The fetch is mocked; in production replace it with a Netmiko `send_command`, or a gNMI subscription ([Pillar 10](#ch10){.ref}).

```python
import json, pathlib, re
from concurrent.futures import ThreadPoolExecutor
STATE, LIMIT = pathlib.Path("counters.json"), 50
MOCK = {"sw1": "GigabitEthernet1/0/10 is up, line protocol is up\n"
               "     2217 input errors, 2217 CRC, 0 frame\n",
        "sw2": "GigabitEthernet1/0/1 is up, line protocol is up\n"
               "     12 input errors, 12 CRC, 0 frame\n"}
def fetch(host):              # real: ConnectHandler(...).send_command(...)
    return MOCK[host]
def parse(text):
    counts, name = {}, None
    for line in text.splitlines():
        m = re.match(r"(\S+) is (?:up|down|administratively down)", line)
        if m: name = m.group(1)
        m = re.search(r"(\d+) input errors", line)
        if m and name: counts[name] = int(m.group(1))
    return counts
def alerts(now, before):
    for host, ifs in now.items():
        for ifn, n in ifs.items():
            p = before.get(host, {}).get(ifn, n)
            d = n - p if n >= p else n     # counter cleared
            if d > LIMIT: yield host, ifn, d
hosts = sorted(MOCK)
with ThreadPoolExecutor(20) as pool:
    now = dict(zip(hosts, map(parse, pool.map(fetch, hosts))))
before = json.loads(STATE.read_text()) if STATE.exists() else {}
for h, i, d in alerts(now, before):
    print(f"ALERT {h} {i}: +{d} input errors")
STATE.write_text(json.dumps(now))
```

With a previous state of 1,000 errors for `sw1` Gi1/0/10 and 10 for `sw2` Gi1/0/1, the output is `ALERT sw1 GigabitEthernet1/0/10: +1217 input errors`; `sw2` rose by 2 and is quiet. **Mistake.** Alerting on the absolute counter, which stays high for ever.
:::

::: q
### Q11.29 Describe a time you troubleshot a hard problem.
[AMAZON · GOOGLE · CISCO · HM · ■■■ · T]{.meta}

[30-second answer: use STAR with SCALPEL as the Action: situation and impact, your task, the clarifying questions and layer walk with evidence, and the result with prevention.]{.short}

**Answer.** Choose a case with a stacked fault, as in [Case 7](#c11-7){.ref} or [Case 16](#c11-16){.ref}: it shows that you re-tested after each fix. State numbers (users affected, minutes to mitigate) and the guard you added. Amazon's Dive Deep and Ownership principles are the target ([Pillar 12](#ch12){.ref}).
:::

::: q
### Q11.30 Design monitoring so that the last five cases would have been detected before users noticed.
[GOOGLE · AMAZON · MICROSOFT · TECH-2 · ■■■ · T]{.meta}

[30-second answer: monitor symptoms at the user layer (synthetic probes, DNS and DHCP success), plus state and rates at the device layer (neighbours, sessions, error and broadcast rates, optics).]{.short}

| Case | Signal that would have fired |
|---|----------------------------------|
| 14, ECMP optic | CRC delta and optical power threshold on every uplink |
| 15, VPN | Child SA and encaps/decaps rate per tunnel |
| 16, Linux | External synthetic probe on the port after each deploy |
| 17, window | Long-haul throughput baseline |
| 18, mtr | None needed; a runbook answers the customer |

**Answer.** Alert on rate and delta, not on absolute counters; route alerts by severity; test the monitors by injecting the fault ([Pillar 10](#ch10){.ref}).
:::
::: q
### Q11.31 Cold case A: "The branch OSPF neighbour flaps every few minutes."
[CISCO · JUNIPER · TECH-2 · ■■■ · T]{.meta}

[30-second answer: the neighbour reaches Full on small packets, then drops when large database updates are lost on a tunnel whose real MTU is lower than its configured one; match the tunnel MTU and clamp, and let ICMP through.]{.short}

**Hidden facts** (reveal only if asked). Ping works; `ping size 1500 df-bit` to the HQ tunnel address fails; the log shows `Neighbor Down: Dead timer expired` a few seconds after `Loading`; HQ is an IPsec peer; the tunnel interface has MTU 1500.

**Model solution.** (i) Clarify: since when, what changed (an IPsec tunnel replaced a leased line), scope (one branch). (ii) Hypotheses: MTU on the tunnel, timer mismatch, authentication. (iii) Layer walk: `show ip ospf neighbor` cycles between Loading and Down; small pings pass, `ping 10.9.9.1 size 1500 df-bit` fails and `size 1400` passes. Hello packets are small and survive, while full-size LSUs are lost, so the dead timer expires. (iv) Fix: `ip mtu 1400` on both tunnel ends and `ip tcp adjust-mss 1360`; never `mtu-ignore`. (v) Verify: Full for an hour, LSDB equal. (vi) Prevent: tunnel template with MTU, and a pre-check. Related: [Case 5](#c11-5){.ref}, [Case 6](#c11-6){.ref}.
:::

::: q
### Q11.32 Cold case B: "After enabling jumbo frames, NFS hangs for some hosts only."
[GOOGLE · AMAZON · ARISTA · TECH-2 · ■■■ · T]{.meta}

[30-second answer: one switch or trunk in the storage VLAN still has MTU 1500, so large frames are dropped silently at Layer 2 (no ICMP is generated), while small operations work; find the hop with `ping -M do -s 8972` and check each port's MTU.]{.short}

**Hidden facts.** `ls` works and `cp` of a large file hangs; affected hosts hang to the same server; the storage VLAN crosses three switches; one was replaced last week.

**Model solution.** (i) Clarify: which hosts, since when (jumbo enabled yesterday), what is common (the replaced switch). (ii) Hypotheses: an MTU gap in the path; NIC settings; NFS server. (iii) Walk: from a failing host `ping -M do -s 8972 <server>` has 100% loss and `-s 1472` passes. Bisect by pinging each switch's management address with the large size, or compare `show interfaces | include MTU` on each trunk; the replaced switch shows `MTU 1500`. A Layer 2 switch drops an oversize frame without sending ICMP, so the sender can never learn the limit. (iv) Fix: `system mtu jumbo 9216` or the platform equivalent, then reload if needed. (v) Verify: the 8972-byte ping passes and the copy completes. (vi) Prevent: a pre-change check that pings at the jumbo size across the VLAN. Related: [Case 5](#c11-5){.ref}.
:::
:::
:::

::: pack
## Revision Spread {#rv11}

::: revision
::: top
**SCALPEL.** **S**ymptom: restate it as a measurement. **C**larify: scope, timeline and change, precision, environment, evidence. **A**ssess: annotate the path, rank three hypotheses. **L**ayer walk: command, healthy output, inference; divide and conquer from Layer 3. **P**inpoint: a root cause that explains every symptom. **E**xecute: minimal fix with a rollback. **L**ock in: verify, prevent, communicate. A failed hypothesis returns you to A.

**Ten facts.** (1) Three first questions: how many, since when, what changed. (2) Timeout means a drop; refusal means a RST from a live host; reset mid-stream means a middlebox or crash. (3) Ping proves ICMP only. (4) Counters are cumulative: take deltas. (5) ExStart means MTU; Init means one-way hellos; BGP Active means TCP failing. (6) Small packets pass and large fail: MTU and blocked ICMP. (7) In a live outage, roll back before diagnosing. (8) `allowed vlan` without `add` replaces the list. (9) Only `mtr` loss that persists to the destination counts. (10) Fix one fault, re-test: stacked faults are common.

**Three figures to redraw.** The SCALPEL card with its loop (Figure 11.1); the three ladders, timeout, refusal, reset (Figure 11.6); the strategy chooser (Figure 11.4).
:::

### Command matrix, condensed

| Layer | IOS XE | Linux |
|---|--------------------|--------------------|
| L1 | `show interfaces`, `show interfaces status`, `... transceiver` | `ethtool eth0`, `ethtool -S eth0`, `ip -s link` |
| L2 | `show mac address-table`, `show interfaces trunk`, `show spanning-tree` | `ip neigh`, `bridge fdb show`, `bridge vlan` |
| L3 | `show ip route X`, `show ip ospf neighbor`, `ping X source Y` | `ip route get X`, `ping -M do -s N`, `mtr -rwzbc 100 X` |
| L4 | `show access-lists`, `show ip nat translations`, `show policy-map control-plane` | `ss -tlnp`, `ss -ti`, `nft list ruleset` |
| L7 | `show ip dhcp binding`, `show ip dhcp snooping` | `dig`, `curl -v`, `tcpdump -ni eth0` |

### Look-alikes

| Observed | Means | First test |
|---|------------------|----------------|
| Timeout | Drop on the path | Capture at both ends |
| Refused | RST from live host | `ss -tlnp` |
| Reset mid-stream | Idle timer or crash | Who sent the RST |
| By IP only | DNS | `dig @server` |
| One direction | Asymmetry, ACL, NAT | Captures both ends |
| Large fails, small works | MTU | `ping -M do -s` |
| Same users always slow | One ECMP member | Counters per member |
| Single flow slow | Window limit | `ss -ti`, BDP |
| Intermittent | Duplicate IP, flap | Correlate with logs |

### Protocol checklists

**OSPF must match.** Subnet and mask, area, hello and dead, authentication, stub flags, network type, unique router ID, not passive, MTU. **BGP stuck states.** Idle: down or no route. Active: TCP failing (address, path, port 179). OpenSent: no valid reply. Established with a number: healthy. **DHCP.** Discover, Offer, Request, Acknowledge; relay adds giaddr; 169.254.0.0/16 on failure. **TCP signatures.** SYN repeated: drop. SYN then RST: no listener. Zero window: receiver slow. Duplicate ACKs: loss. **Overheads (bytes).** 802.1Q 4, MPLS 4 per label, GRE 24, VXLAN 50, IPsec ESP about 50 to 73. MSS is the MTU minus 40.

**Incident checklist.** Mitigate, communicate (first update within 10 minutes), diagnose, fix, post-mortem. Roles: commander, operator, scribe, communications. Save the evidence before rolling back. Name the system gap, not the person.

### Recognition lines for the eighteen cases

| Case | Recognition line |
|--|----------------------------|
| 1 | By IP works, by name fails: DHCP option 6 or DNS |
| 2 | Same VLAN across a trunk fails: allowed list replaced |
| 3 | One VLAN cannot leave: SVI shut, VLAN missing on the core |
| 4 | Bulk slow after a swap: half and full duplex mismatch |
| 5 | Large packets hang over the VPN: ICMP blocked, no MSS clamp |
| 6 | ExStart and Exchange loop: MTU mismatch |
| 7 | No neighbour at all: passive, area, authentication |
| 8 | BGP Active: loopback source and ACL on port 179 |
| 9 | Established, prefix absent: no exact route, next hop unreachable |
| 10 | Server drops for a minute: duplicate IP |
| 11 | Floor down, LEDs flashing: loop with BPDU filter |
| 12 | 169.254 in a new VLAN: no relay, untrusted uplink |
| 13 | Random sessions break: asymmetric return through a stateless firewall |
| 14 | Same users slow: one ECMP member with a bad optic |
| 15 | Tunnel up, no data: selectors and NAT exemption |
| 16 | Refused, then timeout: loopback bind, host firewall, security group |
| 17 | One stream 6 Mb/s: window scaling stripped |
| 18 | Loss at one hop only: CoPP, not a fault |

::: flash
| Q | A |
|---|---|
| First SCALPEL step? | Symptom: restate it as a measurement |
| Which step does a failed hypothesis return to? | Assess |
| The three highest-yield questions? | How many, since when, what changed |
| Default strategy? | Divide and conquer from Layer 3 |
| What does a timeout mean? | A drop on the path |
| What does a refusal mean? | RST: host reached, nothing listening |
| Reset after exactly 5 minutes idle? | Middlebox idle timer |
| Does ping prove the application works? | No, only ICMP reachability |
| Are interface counters rates? | No, cumulative: take deltas |
| `late collision` points to? | Duplex mismatch, on the half-duplex side |
| CRC on the full-duplex side points to? | The same mismatch, or cable or optic |
| `up/down` on an SVI? | VLAN has no active port, or VLAN missing |
| OSPF stuck in ExStart? | MTU mismatch |
| OSPF stuck in Init? | One-way hellos (ACL, multicast, passive) |
| BGP Active? | TCP connection failing |
| BGP state column shows a number? | Established; the prefixes received |
| A `network` statement originates when? | The exact prefix is in the RIB |
| iBGP route "inaccessible"? | Next hop unreachable: `next-hop-self` |
| `169.254.x.x`? | No DHCP reply |
| Which log names a duplicate IP? | `%IP-4-DUPADDR` |
| `%SW_MATM-4-MACFLAP_NOTIF`? | A MAC moving between ports: a loop or a duplicate |
| Why does a loop never end? | Ethernet frames have no TTL |
| `bpdufilter` on an edge port? | Loop detection off; use BPDU Guard |
| PMTUD black hole needs? | ICMP type 3 code 4 dropped |
| MSS on a 1400-byte path? | 1360 |
| Asymmetric path and a stateful firewall? | Reply dropped: no session |
| Why are the same users always slow in ECMP? | The five-tuple hashes to one path |
| 64 KB window at 80 ms? | About 6.5 Mb/s |
| `mtr` loss at one middle hop only? | Rate-limited ICMP; not a fault |
| First action after a bad change in production? | Roll back, after saving the evidence |
:::
:::
:::

:::
