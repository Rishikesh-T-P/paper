::: {.p8}

::: pack
## Problem Set, continued: DNS, firewalls, namespaces and walk-throughs {#ps8b}

::: problems

::: q
### Q8.16 Walk me through the output of `dig +trace google.com`.
[GOOGLE · AMAZON · CISCO · TECH-1 · ■■□ · T]{.meta}

[30-second answer: `+trace` makes dig do the iterative resolution itself: it takes the root servers from its hints, asks one for `google.com`, receives a referral to the `.com` servers, asks one of those, receives a referral to Google's authoritative servers, and finally receives the answer with the `aa` flag.]{.short}

**Answer.** Each stage prints an NS set (the referral) and the server that supplied it. The sequence is root `.` then TLD `com.` then the zone `google.com.` then the A record. The referral carries glue addresses in the additional section so that the next server can be reached without resolving its name. A resolver that serves clients does exactly this on a cache miss, then caches each answer for its TTL; the stub on the client just sends one recursive query. Reading the trace locates a fault: a stage that returns no referral or times out identifies a broken delegation or a dead authoritative server. The sequence is drawn in [3.10](#s3-10){.ref} and the output is annotated in [8.9](#s8-9){.ref}. **Follow-ups.** DNSSEC adds `DS` and `RRSIG` records and the `ad` flag; `+norecurse` mimics what a resolver sends. **Mistakes.** Expecting `+trace` to use the system resolver's cache; it ignores it.
:::

::: q
### Q8.17 What is the difference between NXDOMAIN and SERVFAIL? What would you check for each?
[GOOGLE · AMAZON · MICROSOFT · TECH-1 · ■■□ · T]{.meta}

[30-second answer: NXDOMAIN is a definitive answer that the name does not exist. SERVFAIL means the server could not produce an answer: a failure on the way. Check the name and zone for NXDOMAIN; check the authoritative servers and DNSSEC for SERVFAIL.]{.short}

**Answer.**

| | NXDOMAIN | SERVFAIL |
|---|---|---|
| Meaning | name does not exist (authoritative) | server could not resolve |
| Cached | yes, for the SOA's negative TTL | briefly |
| Typical causes | typo, record never created, wrong zone, search-suffix expansion | authoritative servers unreachable or lame, broken delegation, DNSSEC validation failure, resolver overload |
| First checks | `dig @authoritative name` shows the same? check zone file and the `search` list | query the authoritative servers directly; `dig +cd name` (succeeds if DNSSEC is the cause); `dig +trace` |

NOERROR with an empty answer is a third case: the name exists but not with that record type. **Follow-ups.** REFUSED means a policy denial; a timeout is neither. **Mistakes.** Flushing caches for SERVFAIL when the authoritative side is broken.
:::

::: q
### Q8.18 Explain iptables tables and chains. Which chain sees a packet routed through the box, and which a packet destined to it?
[CISCO · AMAZON · JUNIPER · TECH-1 · ■■□ · T]{.meta}

[30-second answer: tables group rules by purpose (`filter`, `nat`, `mangle`, `raw`); chains are the hook points (PREROUTING, INPUT, FORWARD, OUTPUT, POSTROUTING). A forwarded packet crosses PREROUTING, FORWARD and POSTROUTING; a packet for the host crosses PREROUTING and INPUT.]{.short}

**Answer.** Each table registers only in some chains: `filter` in INPUT, FORWARD, OUTPUT; `nat` in PREROUTING, OUTPUT, POSTROUTING (for the first packet of each flow only; the rest follow conntrack); `mangle` in all five; `raw` in PREROUTING and OUTPUT. Within a chain, rules run top to bottom and the first terminating target wins; a chain without a match uses its policy. Local packets leave through OUTPUT and POSTROUTING (Figure 8.9, [8.12](#s8-12){.ref}). **Follow-ups.** Where does DNAT happen (PREROUTING, before the routing decision) and SNAT (POSTROUTING, after it)? Why does a forwarding firewall need `ip_forward=1`? **Mistakes.** Putting a filtering rule for forwarded traffic in INPUT.
:::

::: q
### Q8.19 DROP versus REJECT: what does the client see in each case, and which is better for internal networks?
[CISCO · AMAZON · TECH-1 · ■■□ · T]{.meta}

[30-second answer: with DROP the client gets nothing and times out after retransmitting; with REJECT it gets an immediate TCP RST or ICMP port-unreachable and fails at once. Internally REJECT is usually better, because it makes failures fast and obvious; DROP suits untrusted edges.]{.short}

**Answer.** A dropped SYN is retried at about 1 s intervals before the connection attempt gives up after roughly two minutes, so applications appear to hang ([8.7](#s8-7){.ref}). REJECT lets a monitoring system or a developer see "connection refused" immediately. On the Internet, DROP withholds the information that a host exists and slows scanners, but a determined scanner learns the same from timing, so the security gain is small. **Follow-ups.** `REJECT --reject-with tcp-reset` or `icmp-port-unreachable`; rate-limit ICMP errors. **Mistakes.** Saying one of them is "more secure" without context.
:::

::: q
### Q8.20 How do you find which process is using port 8080 and kill it gracefully?
[AMAZON · GOOGLE · ARISTA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: `ss -tlnp 'sport = :8080'` or `lsof -nP -i :8080` gives the PID; `kill PID` sends SIGTERM; wait and confirm with `ss`; use `kill -9` only if it ignores SIGTERM.]{.short}

**Approach.** Identify first, because the owner may be a service manager that restarts it. If it is a unit, stop it properly with `systemctl stop name` instead of killing the PID. Otherwise:

```
$ lsof -nP -i :8080
python3 21426 root  3u  IPv4 125319  0t0  TCP 10.0.2.2:8080 (LISTEN)
$ kill 21426; sleep 2; ss -tlnp 'sport = :8080'     # SIGTERM first; the listener disappears
$ kill -9 21426                                     # only if still present
```

**Follow-ups.** `fuser -k 8080/tcp` does both steps; a restarted port may be held in TIME-WAIT and needs `SO_REUSEADDR` in the new server ([7.10](#s7-10){.ref}); signals are in [7.9](#s7-9){.ref}. **Mistakes.** `kill -9` as the first move, and killing the parent supervisor that respawns it.
:::

::: q
### Q8.21 What is in `/proc`? Name five files you would look at for networking.
[AMAZON · GOOGLE · ARISTA · TECH-1 · ■■□ · S]{.meta}

[30-second answer: `/proc` is a virtual file system in which the kernel exposes process and system state as files that are generated on read. For networking: `/proc/net/dev`, `/proc/net/tcp`, `/proc/net/arp`, `/proc/net/route` and `/proc/sys/net/ipv4/ip_forward`.]{.short}

**Answer.** `/proc/net/dev` holds per-interface byte, packet, error and drop counters; `/proc/net/tcp` is the socket table in hexadecimal (state `0A` is LISTEN, ports in hex: `1F90` = 8080); `/proc/net/arp` the neighbour cache; `/proc/net/route` the IPv4 routing table; `/proc/sys/net/*` the tunables, writable ([8.13](#s8-13){.ref}). Per process: `/proc/PID/fd` (open files and sockets), `/proc/PID/status`, `/proc/PID/limits`, `/proc/PID/net/`. `/proc/meminfo` and `/proc/loadavg` give system state. Nothing in `/proc` takes disk space; it is the kernel's own data. **Follow-ups.** `/sys` for devices and driver parameters (`/sys/class/net/eth0/speed`); `ss` and `ip` are friendlier readers of the same data. **Mistakes.** Saying that `/proc` contains logs or that its files are stored on disk.
:::

::: q
### Q8.22 How do you make a sysctl change persistent? Give an example.
[AMAZON · GOOGLE · TECH-1 · ■■□ · T]{.meta}

[30-second answer: `sysctl -w` changes only the running kernel. For persistence, put the setting in a file under `/etc/sysctl.d/`, for example `net.ipv4.ip_forward = 1` in `90-forward.conf`, and apply it with `sysctl --system`; it is also read at boot.]{.short}

**Answer.**

```
$ sudo sysctl -w net.ipv4.ip_forward=1                                   # now, until reboot
$ echo 'net.ipv4.ip_forward = 1' | sudo tee /etc/sysctl.d/90-forward.conf
$ sudo sysctl --system                                                  # reload every file
$ sysctl net.ipv4.ip_forward
net.ipv4.ip_forward = 1
```

Equivalent: write to `/proc/sys/net/ipv4/ip_forward` (also temporary). Files are read in lexical order, so a later name overrides an earlier one. **Follow-ups.** Per-interface keys such as `net.ipv4.conf.all.rp_filter`; some settings are applied by a network manager and overwritten; inside a container only namespaced keys can be changed. **Mistakes.** Editing `/etc/sysctl.conf` on a distribution that ships `sysctl.d`, or forgetting that a kernel module must be loaded before its keys exist.
:::

::: q
### Q8.23 A Linux host can ping its gateway but not 8.8.8.8, and the gateway can ping 8.8.8.8. Walk through your diagnosis.
[CISCO · GOOGLE · AMAZON · MICROSOFT · TECH-2 · ■■■ · T]{.meta}

[30-second answer: the host-to-gateway link works, so the fault is on the path through the gateway: the host's default route, the gateway forwarding or translating the host's packets, or the return path. Test with `ip route get 8.8.8.8`, then `tcpdump` on both gateway interfaces to see where the packet stops.]{.short}

**Approach.** Work outwards, one layer at a time, and decide which side the fault is on before touching anything.

1. **Host.** `ip route get 8.8.8.8` must say `via <gateway> dev eth0 src <own address>`. A missing default route gives "Network is unreachable" (a route problem on the host); a wrong source address or interface points to policy routing or a second NIC. `ping 8.8.8.8` fails with silence, not an error, so the packet leaves.
2. **Gateway receives?** On the gateway, `tcpdump -ni LAN icmp` shows the echo request arriving. If it does not, the host is sending to the wrong MAC (`ip neigh`, a stale entry) or the VLAN is wrong.
3. **Gateway forwards?** If the request arrives but `tcpdump -ni WAN icmp` shows nothing leaving, the gateway discards it: `sysctl net.ipv4.ip_forward` is 0, a FORWARD chain rule drops it (`iptables -L FORWARD -nv`), or reverse-path filtering (`rp_filter`) rejected the source. If a packet leaves with the host's private source address, NAT is missing, so the reply cannot come back: check `iptables -t nat -L POSTROUTING -nv` for MASQUERADE.
4. **Return path.** If the request leaves translated but no reply arrives, the fault is upstream (ISP route, filtering). If the reply arrives at the gateway but not at the host, check conntrack (`conntrack -L`) and the FORWARD rules for the reverse direction.
5. **Why the gateway can ping.** The gateway pings from its own public address, which needs no forwarding or translation. That the gateway works and the host does not is the clue that the missing step is exactly one of those two.

**Follow-ups.** If `ping 8.8.8.8` works but `ping google.com` does not, the fault moves to DNS ([8.9](#s8-9){.ref}); if small packets work and large ones hang, check the path MTU ([8.10](#s8-10){.ref}). The complete method, with the other layers, is in the cases of [11.8](#s11-8){.ref}; NAT is in [3.6](#s3-6){.ref} and static routes in [4.4](#s4-4){.ref}. **Mistakes.** Changing the gateway's configuration before capturing at both interfaces.
:::

::: q
### Q8.24 Throughput between two data centres on a 10 Gb/s link with 100 ms RTT is only 50 Mb/s per flow. Diagnose.
[GOOGLE · AMAZON · CISCO · ARISTA · TECH-2 · ■■■ · T]{.meta}

[30-second answer: the BDP is 125 MB, and 50 Mb/s means a window of about 625 KB, so either the window is capped (receive buffer, no window scaling) or loss is holding the congestion window down. `ss -ti` and a capture decide which.]{.short}

**Approach.** The full calculation is the worked example in [8.13](#s8-13){.ref}: BDP = 10¹⁰ × 0.1 / 8 = 125 MB; window in use = 50 × 10⁶ × 0.1 / 8 = 625 KB. Then:

| Evidence | Reading | Fix |
|---|---|---|
| `wscale` absent in the SYN, or `snd_wnd`/`rcv_space` near 64 KB | window scaling disabled by a middlebox or setting | enable `tcp_window_scaling`; find the device that strips the option |
| `rwnd_limited` or window-full flags; receive buffer maximum below BDP | buffer cap | raise `tcp_rmem`/`tcp_wmem` maxima and `rmem_max` towards 128 MB |
| `cwnd` small, `retrans` rising, duplicate ACKs | loss: by the Mathis relation 50 Mb/s at 100 ms needs p ≈ 8 × 10⁻⁶, one packet in 125 000 | locate the loss (errors on a port, microbursts, a policer); try BBR; fix the cause |
| `app_limited` | the application sends too little | application tuning, more streams |

**Follow-ups.** Parallel streams (`iperf3 -P 8`) show whether the limit is per-flow; a policer or shaper on the path produces a sawtooth; check `tc -s qdisc` on the sender. **Mistakes.** Upgrading the link, which does not change a window-limited flow.
:::

::: q
### Q8.25 Where does tcpdump capture relative to netfilter on ingress and egress? Why might you see a packet in tcpdump that the application never receives?
[CISCO · JUNIPER · ARISTA · QUALCOMM · TECH-2 · ■■■ · T]{.meta}

[30-second answer: on ingress the tap is before netfilter; on egress it is after. So a captured inbound packet may still be dropped by a firewall rule, by reverse-path filtering, by a full socket queue or because no socket matches.]{.short}

**Answer.** The capture point is `AF_PACKET`, in the receive path before PREROUTING and in the transmit path after POSTROUTING (Figure 8.7). Reasons a seen packet is not delivered: (i) an INPUT, FORWARD or PREROUTING rule drops it (the DROP counter rises in `iptables -L -nv`); (ii) `rp_filter` discards a source address that would not route back through that interface (`nstat -az | grep -i filter`, or `IPReversePathFilter`); (iii) no listening socket, so the kernel sends RST (visible in the capture) or ICMP unreachable; (iv) the accept queue or receive buffer is full (`ss -ltn` with `Recv-Q` equal to `Send-Q`, `TcpExtListenDrops` rising); (v) a bad checksum or conntrack `INVALID` state; (vi) the packet was for another namespace or MAC (promiscuous capture). Conversely an *outbound* packet missing from the capture was dropped before the tap, by the local OUTPUT chain or a routing failure. **Follow-ups.** `nft monitor trace` or `iptables -t raw -j TRACE` follows one packet through the rules; XDP programs run even earlier ([7.12](#s7-12){.ref}). **Mistakes.** Treating the capture as proof of delivery.
:::

::: q
### Q8.26 Design an nftables rule set for a bastion host. Explain conntrack and why ESTABLISHED,RELATED comes first.
[AMAZON · GOOGLE · ARISTA · TECH-2 · ■■■ · T]{.meta}

[30-second answer: default-drop input; accept established and related first, then loopback, SSH from the management network and any needed ICMP; log the rest at a limited rate; allow outbound by default. Conntrack remembers flows, so replies are accepted without opening inbound ports, and the check comes first because it matches almost every packet.]{.short}

**Answer.** The complete rule set is in [8.12](#s8-12){.ref} (table `inet campus_fw`). Design decisions: (i) `policy drop` on `input` so that anything forgotten is closed; (ii) `ct state established,related accept` first, for speed and so that the administrator's own SSH session survives a reload; (iii) `ct state invalid drop`; (iv) a named set `mgmt` for the permitted source ranges, changed without editing rules; (v) ICMP limited to echo-request, destination-unreachable and time-exceeded at a limited rate, since blocking all ICMP breaks path-MTU discovery; (vi) a counter and a rate-limited log at the end; (vii) a `forward` chain with `policy drop` so that the host cannot be used as a router unless intended; (viii) load atomically with `nft -f`, and test from a second session with `at now + 5 minutes` rolling the rules back. **Follow-ups.** SSH hardening is in [Pillar 9](#ch9){.ref}; the equivalent iptables rules differ only in syntax. **Mistakes.** Setting the policy to drop before adding the ESTABLISHED rule, which cuts off one's own session.
:::

::: q
### Q8.27 How do network namespaces work, and how does Docker give a container connectivity with veth, a bridge and NAT?
[GOOGLE · AMAZON · MICROSOFT · NOKIA · TECH-2 · ■■■ · T]{.meta}

[30-second answer: a network namespace is a private copy of interfaces, addresses, routes, ARP cache and firewall rules. Docker puts each container in its own namespace, connects it with a veth pair to a host bridge (`docker0`), and uses iptables MASQUERADE for outbound and DNAT for published ports.]{.short}

**Answer.** Namespaces are one of the kernel's isolation primitives (alongside PID, mount, UTS, IPC, user and cgroup). A process belongs to one namespace of each kind; the network one gives it a separate stack, starting with only a down `lo`. A veth pair is a virtual cable: Docker moves one end into the container as `eth0` and attaches the other to the bridge, which acts as a switch among containers and as their gateway (172.17.0.1). Outbound packets leave through the host's routing table; a MASQUERADE rule in `nat POSTROUTING` rewrites their source to the host's address, and conntrack translates the replies back ([8.12](#s8-12){.ref}). `-p 8080:80` adds a DNAT rule in PREROUTING from host port 8080 to the container's address. Figure 8.5 and the lab of [8.5](#s8-5){.ref} build the same structure by hand, with `rtr` as the bridge. **Follow-ups.** `nsenter -t PID -n` or `ip netns exec` to debug inside; host networking removes the namespace; Kubernetes pods share one namespace among containers; overlay networks encapsulate (VXLAN). **Mistakes.** Describing containers as lightweight VMs, which have their own kernel.
:::

::: q
### Q8.28 `strace` a `curl` that hangs. What do you expect to see, and how do you tell a DNS hang from a TCP connect hang?
[AMAZON · GOOGLE · ARISTA · TECH-2 · ■■■ · T]{.meta}

[30-second answer: `strace -f -tt -e trace=network,poll curl URL`. A DNS hang waits after a send to port 53 (or a connect to the resolver) and never reaches a connect to the target; a TCP hang shows `connect(…) = -1 EINPROGRESS` to the target followed by a poll that times out.]{.short}

**Answer.** `curl` first loads configuration and looks for the name-service cache (`connect` to `/var/run/nscd/socket` failing with `ENOENT` is harmless), then resolves the name by `sendto`/`recvfrom` or `connect` on a UDP socket to the resolver. After resolution it creates a non-blocking socket and calls `connect`, which returns `EINPROGRESS`, then waits in `poll`/`ppoll` for writability; success is signalled by `getsockopt(SO_ERROR) = 0`, failure by an error such as `ECONNREFUSED` (immediate RST) or by the timeout alone (dropped SYN). If the hang is in `poll` after a UDP send to port 53, check `resolvectl status` and `dig`; if it follows a `connect` to the target, switch to `tcpdump` to see whether a SYN-ACK returns ([8.7](#s8-7){.ref}). **Follow-ups.** `strace -c` for a profile; `-T` for time per call; `ltrace` for library calls; compare `curl -w` timings ([8.10](#s8-10){.ref}). **Mistakes.** Forgetting `-f` (misses child processes) and `-tt` (no timing).
:::

::: q
### Q8.29 Explain the `ip neigh` states. What does FAILED versus INCOMPLETE indicate?
[CISCO · ARISTA · JUNIPER · TECH-1 · ■■■ · T]{.meta}

[30-second answer: the states track whether a neighbour's MAC address is known and recently confirmed: INCOMPLETE (resolving, no reply yet), REACHABLE (confirmed), STALE (not recently confirmed), DELAY and PROBE (re-verifying), FAILED (resolution gave up). INCOMPLETE is in progress; FAILED is the verdict that nobody answered.]{.short}

**Answer.** The full table is in [8.5](#s8-5){.ref}. After an ARP request is broadcast, the entry sits in INCOMPLETE while up to three solicitations are sent (one a second by default); if none is answered it becomes FAILED, and packets for that address are discarded with "Destination Host Unreachable". For a gateway, FAILED or a long INCOMPLETE means a layer-2 problem: the gateway is down, in another VLAN, on a different subnet from what the mask implies, or filtering ARP. A REACHABLE entry ages to STALE after about 30 s, which is normal; on the next use the kernel goes DELAY (5 s) and PROBE (unicast ARP) to confirm. **Follow-ups.** Capture with `tcpdump -nn -e arp`; duplicate IP addresses show as an entry whose `lladdr` changes; `arping -D` detects duplicates; IPv6 uses neighbour discovery with the same states. **Mistakes.** Treating STALE as a fault.
:::

::: q
### Q8.30 How would you implement policy-based routing so that traffic from 10.1.0.0/16 uses ISP-B and everything else uses ISP-A?
[CISCO · JUNIPER · AMAZON · NOKIA · TECH-2 · ■■■ · T]{.meta}

[30-second answer: put ISP-B's default route in a separate table (`ip route add default via <B> table 100`) and select it with a rule (`ip rule add from 10.1.0.0/16 lookup 100`); the main table keeps ISP-A as default. Verify with `ip route get … from …`.]{.short}

**Answer.** The commands and a verified run are in [8.5](#s8-5){.ref}. A production design adds four items. (i) **NAT per uplink:** masquerade on each outgoing interface, since each ISP expects its own addresses (`-t nat -A POSTROUTING -o ispB0 -j MASQUERADE`). (ii) **Reverse-path filtering:** with asymmetric paths set `net.ipv4.conf.all.rp_filter=2` (loose) or the reply may be discarded. (iii) **Failover:** the rules do not notice a dead ISP; a script or routing daemon pings through each link and replaces the default route or removes the rule. (iv) **Marks instead of sources**, when the selector is not an address: mark the packet and select on the mark.

```
iptables -t mangle -A PREROUTING -p tcp --dport 443 -j MARK --set-mark 1
ip rule add fwmark 1 lookup 100 priority 1000
```

**Follow-ups.** Rules are checked in priority order and `main` is consulted last; routers do this with PBR or VRF route leaking ([4.9](#s4-9){.ref}). **Mistakes.** Forgetting that rules are lost on reboot unless written to the network configuration.
:::

:::
:::

:::
