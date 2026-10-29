::: {.p8}

::: pack
## Problem Set {#ps8}

Every interview question of this pillar is solved once, here, in the compact template: a 30-second answer first, then the approach, code, follow-ups and common mistakes where they apply. Tags give the companies and round where the topic was reported, the difficulty (■□□ easy, ■■□ medium, ■■■ hard), and **S** when a specific question was reported by candidates or **T** when only the topic was reported and the wording is ours. Output shown comes from the Campus Net lab of this chapter. Where a section already teaches the full reasoning, the entry gives the answer and a pointer, so that nothing is explained twice.

::: problems

::: q
### Q8.1 How do you list all listening TCP and UDP ports and the owning process?
[CISCO · AMAZON · ARISTA · TECH-1 · ■□□ · T]{.meta}

[30-second answer: `ss -tulpn`, which prints TCP and UDP (`-t -u`), listening sockets (`-l`), the owning process (`-p`) and numeric ports and addresses (`-n`). Run it as root to see other users' processes.]{.short}

**Answer.** `-n` matters because without it `ss` resolves addresses and port numbers to names, which is slow and may hide the port number being searched for. Read the *Local Address* column: `0.0.0.0:22` or `*:22` accepts on every IPv4 address, `127.0.0.1:5000` only on loopback, `[::]:80` on every IPv6 (and usually IPv4) address. Filter with `ss -tlnp 'sport = :8080'`. **Follow-ups.** `lsof -i -P -n` gives the same through the file table; `netstat -tulpn` is the legacy form ([8.6](#s8-6){.ref}). **Mistakes.** Forgetting `sudo` and concluding that no process owns the port.
:::

::: q
### Q8.2 What is the difference between `ip addr` and `ifconfig`? Why was net-tools deprecated?
[CISCO · QUALCOMM · MICROSOFT · TECH-1 · ■□□ · T]{.meta}

[30-second answer: `ifconfig` belongs to the unmaintained net-tools package and reads `/proc` and uses old `ioctl` calls; `ip` (iproute2) uses netlink and covers everything the kernel supports: several addresses per interface, policy routing, VRFs, namespaces, tunnels and modern IPv6.]{.short}

**Answer.** net-tools has seen no significant development since the early 2000s. Its `ifconfig` shows only one address per alias label, cannot show or set many link types or the neighbour states, and has no equivalent of `ip rule`, `ip netns` or `ip route get`. `ip` reads and writes through netlink, which is faster on hosts with many routes or sockets and returns consistent snapshots. The replacements are listed in [8.1](#s8-1){.ref}. **Follow-ups.** `ip -br a`, `ip -j` for JSON, `ip -s link` for counters. **Mistakes.** Saying `ifconfig` is "removed": it still runs where installed, but is not installed by default on current Debian and Ubuntu.
:::

::: q
### Q8.3 How do you check disk usage and find the biggest directory?
[AMAZON · MICROSOFT · TECH-1 · ■□□ · T]{.meta}

[30-second answer: `df -h` shows file-system usage; `du -sh * | sort -h` (or `du -xh --max-depth=1 / | sort -h | tail`) shows which directory is biggest. Run the second from the top and descend into the largest.]{.short}

**Approach.** `df -h` first, because it names the full file system; then `du -xh --max-depth=1 /var | sort -h | tail -5`, with `-x` to stay on that file system, repeated one level down. **Follow-ups.** If `df` says 100 % but `du` finds less, deleted files held open by a process (`lsof +L1`) or inode exhaustion (`df -i`) are the usual causes; `ncdu` gives an interactive view. **Mistakes.** Running `du` on `/` without `-x`, which counts `/proc` and mounted volumes.
:::

::: q
### Q8.4 What do `/etc/resolv.conf`, `/etc/hosts` and `/etc/nsswitch.conf` contain, and in what order are they consulted?
[GOOGLE · AMAZON · MICROSOFT · TECH-1 · ■□□ · T]{.meta}

[30-second answer: `nsswitch.conf` sets the order of name sources, normally `hosts: files dns`; so `/etc/hosts` is read first, then DNS using the servers named in `/etc/resolv.conf`.]{.short}

**Answer.** `/etc/hosts` maps names to addresses locally. `/etc/resolv.conf` lists `nameserver` addresses, a `search` list of suffixes to try on short names and `options` (`timeout`, `attempts`, `ndots`); on current Ubuntu it holds the stub `127.0.0.53` of `systemd-resolved`, and `resolvectl status` shows the real upstreams. Applications call `getaddrinfo()`, which follows `nsswitch.conf`. **Follow-ups.** `dig` bypasses hosts and nsswitch, so `getent hosts name` is the right test of what applications see ([8.9](#s8-9){.ref}). **Mistakes.** Editing `resolv.conf` on a system where it is regenerated, so the change vanishes.
:::

::: q
### Q8.5 What does `ping` actually send? What does "Destination Host Unreachable" from your own IP mean?
[CISCO · QUALCOMM · MICROSOFT · TECH-1 · ■□□ · T]{.meta}

[30-second answer: ICMP Echo Request (type 8, code 0) with an identifier, a sequence number and a payload, answered by Echo Reply (type 0). "Destination Host Unreachable" whose source is the sender's own address means ARP found no owner for an on-link destination.]{.short}

**Answer.** The default payload is 56 bytes, so with an 8-byte ICMP header and 20-byte IP header the packet is 84 bytes. If the destination is on the local subnet the host must ARP for it; when there is no reply, the host's own IP layer reports the failure. `ip neigh` shows the entry as `INCOMPLETE` and then `FAILED` ([8.5](#s8-5){.ref}). The same words from a *router's* address mean that router had no route. **Follow-ups.** A reply of "Request timeout" or no reply is silence (drop or dead host); TTL in the reply estimates the hop count. **Mistakes.** Treating a successful ping as proof that the service works.
:::

::: q
### Q8.6 Explain permissions `754` and the sticky bit on `/tmp`.
[CISCO · AMAZON · TECH-1 · ■□□ · T]{.meta}

[30-second answer: 754 is rwx for the owner (7), r-x for the group (5) and r-- for others (4). The sticky bit on a directory lets only a file's owner (or root) delete or rename it, which is why world-writable `/tmp` shows `drwxrwxrwt`.]{.short}

**Answer.** Read is 4, write 2, execute 1, summed per class (Figure 8.3 in [8.2](#s8-2){.ref}). On a directory, execute means permission to enter and use names inside, and write permission to create or delete entries there. Without the sticky bit, anyone with write access to a directory could remove other users' files in it. **Follow-ups.** `chmod 1777 dir` sets the sticky bit; setuid (4000) runs a program as its owner (`passwd`), setgid (2000) on a directory makes new files inherit its group. `umask 022` gives new files 644. **Mistakes.** Using `chmod 777` to "fix" a permission problem.
:::

::: q
### Q8.7 Write a one-liner to print the top 10 IPs by request count from an access log.
[AMAZON · ARISTA · GOOGLE · TECH-1 · ■■□ · S]{.meta}

[30-second answer: `awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10`. The first field is the client address; `sort` groups equal lines so that `uniq -c` can count them; `sort -rn` ranks by count.]{.short}

**Answer.**

```
$ awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -3
      3 10.20.7.9
      3 10.20.1.15
      2 10.20.4.31
$ awk '{c[$1]++} END {for (i in c) print c[i], i}' access.log | sort -rn | head -10     # no initial sort
```

**Complexity.** The pipeline sorts the whole input, O(n log n) in time, spilling to disk when memory is short (`sort -S 1G`); the awk array version is O(n) and holds only one entry per distinct address, so it is better for a very large log. **Follow-ups.** Requests per URL (`$7`), per status (`$9`), per minute (cut the timestamp with `cut -c14-18`); only errors (`awk '$9>=500'`); behind a proxy the client is in `X-Forwarded-For`, not `$1`. **Mistakes.** Omitting the first `sort` (`uniq` counts only adjacent lines) and sorting counts as text (`sort -n`, not `sort`).
:::

::: q
### Q8.8 Write a Bash script that reads a file of hostnames and reports which are unreachable, exiting non-zero if any fail.
[AMAZON · ARISTA · JUNIPER · TECH-1 · ■■□ · T]{.meta}

[30-second answer: loop over the file with `while read`, ping each host once with a timeout, print the failures to stderr, and `exit 1` at the end if any failed. The version with options, CSV output and a log is `reach.sh` in [8.4](#s8-4){.ref}.]{.short}

**Code.**

```bash
#!/usr/bin/env bash
set -uo pipefail                      # no -e: a failing ping is expected, not fatal
fail=0
while IFS= read -r h || [[ -n $h ]]; do
  [[ -z $h || $h == \#* ]] && continue
  ping -c1 -W1 "$h" >/dev/null 2>&1 || { echo "UNREACHABLE $h" >&2; fail=1; }
done < "${1:?usage: ${0##*/} hostsfile}"
exit "$fail"
```

```
$ ./q8.sh hosts.txt; echo rc=$?
UNREACHABLE 192.0.2.77
UNREACHABLE 10.20.99.1
rc=1
```

**Follow-ups.** For hundreds of hosts use `xargs -P 32` (parallel), as in `sweep.sh`; separate DNS failure from ping failure with `getent hosts`; above fifty lines or with retries, JSON output or threads, use Python. **Mistakes.** `for h in $(cat file)` (word splitting), no quoting of `"$h"`, and `set -e` that aborts at the first dead host.
:::

::: q
### Q8.9 What does `ip route get 1.1.1.1` tell you that `ip route show` does not?
[GOOGLE · MICROSOFT · AMAZON · TECH-1 · ■■□ · T]{.meta}

[30-second answer: it performs the actual lookup and prints the route the kernel would use, with the next hop, the output interface and the source address, after policy rules and longest-prefix match. `show` only lists table contents.]{.short}

**Answer.** `ip route show` lists the main table. The real decision also depends on `ip rule` (other tables), marks, the input interface and the best-matching prefix. `get` applies all of these:

```
$ ip route get 10.0.2.2
10.0.2.2 via 10.0.1.1 dev r-eth0 src 10.0.1.2 uid 0
$ ip route get 8.8.8.8 from 10.1.5.5            # test a policy rule
8.8.8.8 from 10.1.5.5 via 198.51.100.1 dev p1 table 100
```

The `src` field answers "which address will the packet carry", which is what a remote firewall will see and which ACLs and NAT rules match. **Follow-ups.** `iif eth0` simulates a forwarded packet; an error "Network is unreachable" means no route at all. **Mistakes.** Reading the default route in `show` and assuming it is used for every destination.
:::

::: q
### Q8.10 How does traceroute work? Why does Linux use UDP and Windows ICMP? How do you trace through a firewall that allows only 443?
[CISCO · JUNIPER · ARISTA · GOOGLE · TECH-1 · ■■□ · T]{.meta}

[30-second answer: it sends probes with TTL 1, 2, 3, …; each router that decrements the TTL to zero returns ICMP Time Exceeded, revealing its address, until a probe reaches the destination. The UDP or ICMP choice is historical; for a firewall that allows only 443, use TCP probes: `traceroute -T -p 443 host`.]{.short}

**Answer.** Figure 8.8 shows the exchange ([8.10](#s8-10){.ref}). The destination answers UDP probes (sent to unlikely high ports) with ICMP port unreachable, ICMP echo probes with an echo reply, and TCP SYN probes with SYN-ACK or RST; any of these ends the trace. Both UDP and ICMP work; Unix tradition used UDP and Windows' `tracert` ICMP echo, and either may be filtered. A TCP SYN to the permitted port passes the filter and reveals each hop until the firewall. **Follow-ups.** ECMP makes successive probes take different paths, so Paris traceroute keeps the flow tuple constant; `* * *` is a missing reply, not a failure; MPLS can hide hops. **Mistakes.** Reading the latency of a middle hop as the latency of the path.
:::

::: q
### Q8.11 `mtr` shows 50 % loss at hop 3 but 0 % at the destination. Is there a problem?
[CISCO · JUNIPER · AMAZON · GOOGLE · TECH-1 · ■■□ · T]{.meta}

[30-second answer: no. Loss at an intermediate hop that does not continue to later hops is the router rate-limiting its own ICMP replies (control-plane policing), not dropping forwarded traffic. Only loss that persists to the final hop is real.]{.short}

**Answer.** Hop 3 is probed by the packets whose TTL expires there, and the router must generate the reply on its slow path. Forwarded traffic uses the fast path and is untouched; if it had been dropped at hop 3, hops 4 onwards would show at least the same loss. Confirm with a different protocol (`mtr -T -P 443`) or by testing the real application. **Follow-ups.** The mirror case: loss that begins at hop 6 and stays through the destination is real, located at or just after hop 6; loss only at the last hop may be the destination rate-limiting ICMP, so test with TCP. **Mistakes.** Sending a ticket to the owner of hop 3.
:::

::: q
### Q8.12 A server has thousands of sockets in TIME-WAIT. Is that a problem? Which side ends up there, and why does it last 2 × MSL?
[GOOGLE · AMAZON · CISCO · TECH-1 · ■■□ · T]{.meta}

[30-second answer: usually not a problem. TIME-WAIT is held by whichever side closed first, for 60 s on Linux (2 × MSL), so that a lost final ACK can be answered with a repeated FIN and old segments of the connection expire before the port pair is reused.]{.short}

**Answer.** The active closer sends the first FIN, receives the peer's FIN and sends the last ACK; it must keep the connection tuple for 2 × MSL in case that ACK was lost, and so that delayed duplicates from the old connection die in the network. Thousands of entries cost a few hundred bytes each. They matter only to a *client* opening many short connections to one destination: the tuple space is limited by ephemeral ports (28 232 by default), so about 470 new connections per second to one server address and port exhaust it. Remedies: reuse connections (keep-alive, pooling), widen `ip_local_port_range`, enable `net.ipv4.tcp_tw_reuse` for outgoing connections, spread over more server addresses. **Follow-ups.** `tcp_tw_recycle` was removed from the kernel because it broke clients behind NAT; `SO_REUSEADDR` lets a restarted server bind while old connections wait ([7.10](#s7-10){.ref}). **Mistakes.** Calling TIME-WAIT a leak, or lowering it by recompiling.
:::

::: q
### Q8.13 Many sockets are in CLOSE-WAIT. What is the cause and whose fault is it?
[GOOGLE · AMAZON · ARISTA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: the peer has closed (sent FIN) and the local application has not called `close()`. It is an application bug, a descriptor leak, not a network problem; the kernel waits for the program indefinitely.]{.short}

**Answer.** CLOSE-WAIT is the state after receiving a FIN and before the local FIN; only the application can move the socket on, by `close()`. Find the process with `ss -tanp state close-wait`, then count descriptors in `/proc/PID/fd` and read the code for error paths where `close()` is skipped (a `return` before cleanup, an exception, a connection pool that never evicts). The growth eventually hits the open-files limit and the service fails with "too many open files". **Follow-ups.** Stopgap: restart the process; permanent: close in a `finally` or use RAII; contrast with FIN-WAIT-2, which is the *other* side of the same half-close. **Mistakes.** Tuning TCP timers, which have no effect on CLOSE-WAIT.
:::

::: q
### Q8.14 Write a tcpdump filter to capture only SYN packets (not SYN-ACK) to port 443.
[CISCO · JUNIPER · QUALCOMM · TECH-1 · ■■□ · T]{.meta}

[30-second answer: `tcpdump -nn 'tcp dst port 443 and tcp[tcpflags] & (tcp-syn|tcp-ack) == tcp-syn'`. The mask keeps the SYN and ACK bits, and the comparison requires SYN set and ACK clear.]{.short}

**Answer.** A SYN-ACK has both bits set, so testing `tcp-syn` alone would match it too; masking with `(tcp-syn|tcp-ack)` and comparing with `tcp-syn` selects only the first packet of a handshake. The filter runs in the kernel as BPF ([8.7](#s8-7){.ref}). **Follow-ups.** Resets: `tcp[tcpflags] & tcp-rst != 0`; SYN-ACKs: `== (tcp-syn|tcp-ack)`; the older form is `tcp[13] & 18 == 2`. **Mistakes.** Writing `tcp[tcpflags] == tcp-syn` for a pure SYN (it works, but breaks with ECN flags set), and forgetting to quote the expression.
:::

::: q
### Q8.15 You see 64 KB TCP segments in tcpdump on a 1500-MTU link. Is it a bug?
[QUALCOMM · BROADCOM · ARISTA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: no. TCP segmentation offload (TSO) and generic segmentation offload (GSO) let the stack hand one large buffer to the driver, which is cut into MSS-sized frames later; the capture tap sees the buffer. On receive, GRO merges frames before the tap.]{.short}

**Answer.** The wire frames are 1500 bytes or fewer; the 64 KB figure is a software view that saves per-packet CPU cost. Check with `ethtool -k eth0 | grep -E 'tcp-seg|generic'`; disable temporarily with `ethtool -K eth0 tso off gso off gro off` to see real frames, or capture on another machine or a mirror port. A 64 KB buffer becomes about 45 segments of 1448 bytes ([8.11](#s8-11){.ref}). **Follow-ups.** Checksums appear wrong on the sender because the NIC fills them in after the tap; a packet of 64 KB never crosses the wire, so path-MTU reasoning is unaffected. **Mistakes.** Filing a bug, or concluding that the MTU is 64 KB.
:::

:::
:::

:::
