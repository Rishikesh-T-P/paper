::: {.p11}

## [11.9]{.sec}Mock rounds [Should · ■■■]{.tag} {#s11-9}

Three timed rounds follow, for practice with a friend. The partner reads the *interviewer lines* and the *hidden facts*, revealing a fact only when asked for it; the candidate covers the model transcript and attempts the round aloud, then compares. Each round lasts twenty to twenty-five minutes. The same ten-point rubric scores all three.

| Criterion | Points | Full marks when |
|------------------|----|----------------------------------------------|
| Symptom restated and measurable | 1 | The vague word is replaced by a test |
| Clarifying questions (scope, change, precision) | 2 | At least three, and assumptions stated |
| Structure and strategy named | 2 | A method is named and the layer under test stated each time |
| Technical accuracy | 2 | Commands, healthy outputs and inferences are right |
| Evidence for the root cause | 1 | It explains every symptom, including the unaffected cases |
| Fix with rollback and verification | 1 | The same test now passes |
| Prevention and communication | 1 | A guard, a monitor or a template is proposed |

### Round 1 · The Cisco vague-diagram round (cases 2 and 12) {#m11-1}

**Setting.** The diagram is [Figure 11.4](#s11-3){.ref}, and the eight clarifying answers there are already known. The prompt is "PC-A cannot reach PC-B." Time: 25 minutes.

| Hidden fact | Reveal only if asked |
|----------------------|--------------------------------------------|
| PC-B shows `169.254.37.8` | For PC-B's IP configuration |
| Static address 192.168.60.20 on PC-B cannot ping its gateway | After the candidate sets one |
| On SW2, `show interfaces trunk` toward R2 lists allowed VLANs `1,50` | For the trunk on SW2 |
| R2 has `interface Gi0/1.60` with 192.168.60.1/24 and no helper; the DHCP server is 192.168.50.10 | For R2's sub-interface |

::: example
**Model transcript.**

**C (0:30).** "Restating: the ping from PC-A to PC-B times out. The file server behind R2 answers, so the provider circuit, OSPF and R2's routing work. PC-B is new, in VLAN 60. My first suspect is PC-B itself. May I see its IP configuration?"

**I.** "It shows 169.254.37.8."

**C (3:00).** "That is an automatic address, so PC-B has no lease and is not in 192.168.60.0/24; the ping fails before routing matters. Two things could cause it: its frames do not reach R2, or the DHCP request is not answered. I test Layer 2 first, with a static address, because it removes DHCP from the picture. I would set 192.168.60.20 and ping the gateway .1."

**I.** "It times out."

**C (6:00).** "So Layer 2 or the sub-interface. On SW2 I want `show vlan brief` and `show interfaces trunk`."

**I.** "VLAN 60 exists and Gi0/7 is in it. The trunk to R2 lists allowed VLANs 1 and 50."

**C (8:00).** "VLAN 60 is not carried to R2, so its frames never arrive. I would add it with `switchport trunk allowed vlan add 60`, noting that without `add` the list is replaced. Rollback is `remove 60`."

**I.** "Done. The static address now pings .1. Put PC-B back on DHCP: still 169.254."

**C (11:00).** "Layer 2 is now proven, so the broadcast Discover reaches R2 but nobody forwards it, because the server is in another VLAN. I would look at R2's sub-interface for a relay."

**I.** "No `ip helper-address`."

**C (13:00).** "Add `ip helper-address 192.168.50.10` under Gi0/1.60 and renew. Verification: PC-B holds a lease, pings its gateway, and PC-A pings PC-B. I would also check that Windows Firewall on PC-B permits ICMP, since that is the next cause if the ping still fails. Prevention: the VLAN playbook creates the VLAN, trunk entry, sub-interface and relay together, and finishes by testing a lease."
:::

**Watch for.** Two stacked faults: a candidate who stops after the trunk fix has not re-tested. See [Case 2](#c11-2){.ref} and [Case 12](#c11-12){.ref}.

### Round 2 · The Google round (cases 14 and 17) {#m11-2}

**Setting.** A spoken scenario with no diagram. Prompt: "Users say the internet is slow. Define slow, then troubleshoot end to end." Time: 25 minutes.

| Hidden fact | Reveal only if asked |
|----------------------|--------------------------------------------|
| About a quarter of users, no pattern by floor, same users each time | Scope |
| `curl` timings: DNS and connect equal, first byte slow | Measurements |
| Fabric: leaf-spine, four equal-cost uplinks | Environment |
| Leaf1 `Et49` shows rising FCS errors and Rx power -14.2 dBm | Counters, optics |
| Second complaint: a nightly backup to Frankfurt reaches 6 Mb/s on a 1 Gb/s link, RTT 80 ms | After the first fault is closed |

::: example
**Model transcript.**

**C (0:30).** "'Slow' needs a number. I would separate latency, loss and throughput, and ask: how many users, which sites, measured how, and since when?"

**I.** "A quarter of users, always the same ones, no pattern by floor. `curl` shows a long time to first byte."

**C (3:00).** "Consistent per user and per flow points at something that depends on the flow's identity, which in a fabric is ECMP hashing: one of four equal paths is bad, and flows hashed to it suffer. DNS and connect times are equal, so the problem is loss during transfer, not setup. I would run `mtr` from a slow client to see where loss starts, then read error counters on the uplinks."

**I.** "Loss starts at the leaf-to-spine hop. Et49 shows FCS errors."

**C (7:00).** "A failing optic or fibre. I would check the optical power, drain the member so flows rehash (service recovers at once), then replace the optic. Verification is a delta of the counters and the users' timings. Prevention: alert on error rate and optical power, with an automated drain."

**I.** "Fine. A different team says their backup to Frankfurt reaches only 6 Mb/s on a 1 Gb/s link. Parallel streams are faster."

**C (12:00).** "The round-trip is 80 ms, so the bandwidth-delay product is 10 MB. Six megabits per second at 80 ms is about 64 KB per round trip, exactly an unscaled window. I would check whether window scaling was negotiated, with `ss -ti` and a SYN capture at both ends, and the receive buffer with `sysctl net.ipv4.tcp_rmem`."

**I.** "The SYN leaves with a scale of 7 and arrives without it."

**C (15:00).** "A middlebox is stripping the option. Fix it, raise the buffer maxima to 16 MB, and verify a single stream approaches the line rate. Prevention: periodic long-haul throughput baselines."
:::

**Watch for.** Defining "slow" before acting, and linking *consistent per user* to hashing. See [Case 14](#c11-14){.ref} and [Case 17](#c11-17){.ref}.

### Round 3 · The Amazon network-development round (cases 8 and 16) {#m11-3}

**Setting.** A mixed discussion. Prompt: "Our data centre's eBGP session to a cloud edge router is stuck, and separately a new API on a Linux VM is unreachable." Time: 25 minutes.

| Hidden fact | Reveal only if asked |
|----------------------|--------------------------------------------|
| `show ip bgp summary` shows `Active`, new circuit | The session state |
| Our side peers from Loopback0; the cloud side expects the WAN address | The peering addresses |
| An edge ACL permits only ICMP and established TCP | Filtering |
| The API answers on `127.0.0.1:8080` only; nftables has no rule for 8080; the security group lacks 8080 | Part two, in sequence |

::: example
**Model transcript.**

**I.** "What does Active mean in BGP?"

**C (1:00).** "Despite its name, Active means the speaker is trying to open the TCP connection and failing. Idle means it is not trying, because it is down or has no route to the peer. OpenSent means TCP succeeded and an Open was sent but no valid answer has come. So Active is a TCP problem: address, path or filter."

**I.** "It has been Active since turn-up."

**C (3:00).** "Three questions: which address does each side use, is anything filtering port 179, and is it eBGP between directly connected peers? I would ping the peer from the *same source* the session uses, and test port 179 with `telnet peer 179 /source-interface`."

**I.** "Our side uses Loopback0; the ping from it fails, the ping from the WAN interface works. The edge ACL permits ICMP and established TCP."

**C (6:00).** "Then there are two faults. The cloud side has no route to our loopback, and it expects the WAN address; and its SYN to us is dropped by an ACL that allows only established traffic. I would remove `update-source` and permit TCP 179 in both directions, then expect the summary to show a prefix count. Hit counts on the ACL deny line would confirm it first."

**I.** "Good. Second problem: a new API on a Linux VM works locally and not remotely."

**C (10:00).** "Locally works, so the service is up. First, `ss -tlnp | grep 8080` to see the bind address. If it is 127.0.0.1, remote clients get a refusal; the fix is to bind to the interface address. After that, a timeout rather than a refusal means a drop, so I would read `nft list ruleset`, then run `tcpdump -ni eth0 port 8080` on the VM. If nothing arrives even with the host rule open, the packet is dying in the cloud, at the security group."

**I.** "How would you detect both before users did?"

**C (15:00).** "A synthetic probe from outside the host that opens port 8080 after each deployment; BGP session state and prefix-count alerts; and the ACL and security-group rules held in code, so that peers and ports are reviewed together."
:::

**Watch for.** Precise state definitions, and an explanation that distinguishes refusal from timeout. See [Case 8](#c11-8){.ref} and [Case 16](#c11-16){.ref}.

### Labs and the fault injector {#lab11}

The cases are rehearsed best on a network that can be broken on demand. The lab below needs only Containerlab with FRR routers and Linux hosts; the Cisco switching cases (2, 3, 4, 11, 12) are reproduced in Packet Tracer or CML from the table.

::: lab
`LAB 11.1 · 40 MIN PER FAULT`  The break-fix arena. Build six FRR routers (R1 to R4, BR1, BR2), four Linux hosts and one nftables firewall in Containerlab, with OSPF in the core. A partner runs `breakit.sh N` without telling you which fault was injected; you restore service with SCALPEL and then run `check.sh`.

```
#!/bin/sh
# breakit.sh N : inject fault N (the numbers are the cases of 11.8)
case "$1" in
 5)  docker exec clab-campus-fw iptables -I FORWARD -p icmp -j DROP
     docker exec clab-campus-br1 ip link set dev tun0 mtu 1500 ;;
 6)  docker exec clab-campus-r2 ip link set dev eth2 mtu 9000 ;;
 7)  docker exec clab-campus-r4 vtysh -c 'conf t' -c 'router ospf' \
         -c 'passive-interface eth1' ;;
 10) docker exec clab-campus-h2 ip addr add 10.1.50.20/24 dev eth1 ;;
 16) docker exec clab-campus-h3 sh -c 'pkill -f http.server; \
         python3 -m http.server 8080 --bind 127.0.0.1 &' ;;
esac
```

```
#!/bin/sh
# check.sh : the grader; exits non-zero on the first unhealthy item
docker exec clab-campus-h1 ping -c2 -W1 10.1.2.10 >/dev/null || exit 1
docker exec clab-campus-r1 vtysh -c 'show ip ospf neighbor' | grep -q Full || exit 2
docker exec clab-campus-h1 curl -s -m3 http://10.1.2.10:8080/health || exit 3
echo healthy
```

Key output after fault 6: `show ip ospf neighbor` on R1 prints `ExStart/DR`; after the fix, `Full/DR`. **What you should notice:** each fault leaves one decisive line, and `check.sh` passes only when every layer is healthy, so it also catches a stacked second fault.
:::

| Lab | Task | Time |
|-------|-------------------------------------------|----------|
| L11.2 | Packet Tracer or CML. Inject, then solve: case 2 (`switchport trunk allowed vlan 10`), case 3 (`shutdown` on `interface vlan 30`), case 4 (hard-code 100/full on one end), case 11 (`spanning-tree bpdufilter enable` on two ports and a patch cable between them), case 12 (remove `ip helper-address`) | 30 min each |
| L11.3 | Partner mock rounds using the three scripts above, scored with the rubric | 3 × 25 min |
| L11.4 | Write a blameless post-mortem for one injected fault, using the template of [§11.7](#s11-7){.ref} | 45 min |

*Mini-project (optional).* Extend `breakit.sh` and `fixit.sh` to ten faults with an automatic grader that checks a ping matrix, OSPF and BGP state and an HTTP probe, and write one runbook per fault in SCALPEL format. A line for a résumé: "Built a fault-injection lab with ten reproducible network failures and SCALPEL runbooks."

:::
