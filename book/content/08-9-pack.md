::: {.p8}

::: pack
## Revision Spread {#rv8}

::: revision
::: top
**Ten facts.** (1) Every tool is a window onto kernel state: `ip` and `ss` use netlink, `ethtool` the driver, `tcpdump` a packet tap, `/proc` the rest. (2) Pipes connect stdout to stdin; `2>&1` after `>file` sends both to the file; exit status 0 means success. (3) `sort | uniq -c | sort -rn | head` is the top-N idiom; `uniq` counts adjacent lines only. (4) Scripts begin `set -euo pipefail`, quote every `"$var"`, send errors to stderr and exit non-zero on failure. (5) `ip route get` shows the route actually chosen with its source address; `ip neigh` `FAILED` or `INCOMPLETE` is an ARP (layer 2) fault. (6) `ss -tlnp` shows who listens and on which address; many `CLOSE-WAIT` is an application bug; `TIME-WAIT` is normal on the side that closed first. (7) tcpdump captures before netfilter on ingress and after it on egress; `[S]` with no `[S.]` is a drop, `[R.]` is a closed port. (8) Loss at an mtr hop counts only if it persists to the last hop. (9) Counters are cumulative: take two readings and divide by the interval. (10) Throughput is at most window ÷ RTT; the window must reach bandwidth × RTT.

**Three figures to redraw.** The netfilter path (Figure 8.9), the three-namespace lab with its routing tables (Figure 8.5), and the anatomy of a tcpdump SYN line (Figure 8.6).
:::

### Is it the network? The command ladder

| Layer | Question | Command | Healthy result |
|---|---|---|---|
| L1 | Is there a link? | `ethtool eth0`, `ip -br link` | `Link detected: yes`, `LOWER_UP`, expected speed and full duplex |
| L1 | Errors now? | `ip -s link` twice, `ethtool -S` | error counters not increasing |
| L2 | Is the gateway's MAC known? | `ip neigh`, `arping -I eth0 GW` | `REACHABLE` or `STALE` with `lladdr` |
| L3 | Address, mask, route? | `ip -br a`, `ip r`, `ip route get X` | via the expected gateway, right `src` |
| L3 | Does the path work? | `ping -c3 X`, `mtr -rwnc 100 X`, `tracepath X` | loss ends at 0 % at the destination |
| L3 | MTU ok? | `ping -M do -s 1472 X` | reply; otherwise "Frag needed (mtu = N)" |
| L4 | Does the port answer? | `nc -zv X 443`, `ss -tan` | `succeeded`; `Connection refused` = closed, timeout = filtered |
| L4 | Who listens locally? | `ss -tlnp` | right address and port for the service |
| DNS | Does the name resolve? | `dig +short X`, `dig @ns X`, `getent hosts X` | expected address; `NXDOMAIN` / `SERVFAIL` otherwise |
| Firewall | Is it filtered? | `nft list ruleset`, `iptables -L -n -v --line-numbers`, `conntrack -L` | counters rise on the expected rule |
| L7 | Does the application answer? | `curl -sv -o /dev/null -w '%{time_connect} %{time_starttransfer}\n' URL` | 2xx/3xx; timings in range |
| Host | Process, disk, logs? | `systemctl status`, `journalctl -u`, `df -h`, `lsof -i`, `strace -p` | active, space free, no errors |

### Commands by task

| Task | Command |
|---|---|
| Listening ports with process | `ss -tulpn` |
| Connections to a port, by state | `ss -tan state established '( dport = :443 )'` |
| TCP internals (rtt, cwnd, retrans) | `ss -ti dst X` |
| Counts per state | <code>ss -tan &#124; awk 'NR&gt;1{c[$1]++} END{for(s in c) print s,c[s]}'</code> |
| Interface counters / rates | `ip -s link show eth0`, `cat /proc/net/dev`, `nstat -az` |
| Legacy to modern | `ifconfig`→`ip a`, `route -n`→`ip r`, `arp -n`→`ip n`, `netstat`→`ss`, `brctl`→`ip link … type bridge` |
| Add address / route / namespace | `ip addr add 10.0.1.2/24 dev eth0`, `ip route add 10.0.2.0/24 via 10.0.1.1`, `ip netns add red` |
| Run inside a namespace | `ip netns exec red CMD`, `ip -n red a` |
| Policy routing | `ip route add default via GW table 100`, `ip rule add from P lookup 100` |
| Capture to file, rotate | `tcpdump -i eth0 -nn -s 0 -w f.pcap 'filter'`, `-G 300 -W 12` |
| Packets by DNS / HTTP | `tcpdump -nn port 53`, `tcpdump -nn -A port 80` |
| Trace the path (TCP) | `traceroute -n -T -p 443 X`, `mtr -rwnc 100 X` |
| Time a request | `curl -w '%{time_namelookup} %{time_connect} %{time_appconnect} %{time_starttransfer} %{time_total}\n' -o /dev/null -s URL` |
| Throughput test | `iperf3 -s`; `iperf3 -c X -P 4 -t 30 -R`; UDP: `-u -b 200M` |
| Persistent sysctl | `/etc/sysctl.d/90-x.conf` then `sysctl --system` |
| Who owns port 8080 | `ss -tlnp 'sport = :8080'`, `lsof -nP -i :8080` |
| Trace system calls | `strace -f -tt -e trace=network,poll CMD`, `strace -c -p PID` |
| Logs of a service | `journalctl -u NAME --since "10 min ago" -f` |
| Disk | `df -h`, <code>du -xh --max-depth=1 / &#124; sort -h &#124; tail</code>, `lsof +L1` |

### Text-processing idioms

| Need | Idiom |
|---|---|
| Top 10 clients | <code>awk '{print $1}' f &#124; sort &#124; uniq -c &#124; sort -rn &#124; head -10</code> |
| Group by field | `awk '{c[$9]++} END{for(k in c) print k,c[k]}' f` |
| Filter on a number | `awk '$9>=500 {print $1,$7,$9}' f` |
| Last field | `awk '{print $NF}' f` |
| Replace | `sed 's/old/new/g' f`, in place `sed -i` |
| Print matching part | `grep -oE 'Gi[0-9/]+' f`; context `grep -B2 -A2 PATTERN f` |
| Columns | `cut -d: -f1,3 /etc/passwd` |
| JSON | <code>jq -r '.items[] &#124; select(.up==false) &#124; .name'</code> |
| Count lines / uniques | `wc -l`; <code>sort -u &#124; wc -l</code> |

### tcpdump (BPF) and Wireshark display filters

| Goal | tcpdump (capture filter) | Wireshark (display filter) |
|---|---|---|
| One host | `host 10.0.1.2` | `ip.addr == 10.0.1.2` |
| One port | `port 443` | `tcp.port == 443` |
| Network | `net 10.20.0.0/16` | `ip.addr == 10.20.0.0/16` |
| Exclude SSH | `not port 22` | `!(tcp.port == 22)` |
| New connections | <code>tcp[tcpflags] & (tcp-syn&#124;tcp-ack) == tcp-syn</code> | `tcp.flags.syn==1 && tcp.flags.ack==0` |
| Resets | `tcp[tcpflags] & tcp-rst != 0` | `tcp.flags.reset == 1` |
| Retransmissions | (not available) | `tcp.analysis.retransmission` |
| Zero window | (not available) | `tcp.analysis.zero_window` |
| Pings | `icmp[icmptype] == icmp-echo` | `icmp.type == 8` |
| DNS | `udp port 53` | `dns`; errors `dns.flags.rcode != 0` |
| HTTP errors | `tcp port 80` then read | `http.response.code >= 400` |
| TLS ClientHello | `tcp port 443` | `tls.handshake.type == 1` |
| VLAN 10 | `vlan 10` | `vlan.id == 10` |
| One conversation | `host A and host B and port P` | `tcp.stream == N` |
| Slow gaps | `-ttt` option | `frame.time_delta > 1` |

### TCP states as traffic lights, and ICMP types

| State | Light | Meaning |
|---|---|---|
| `LISTEN`, `ESTAB` | green | normal |
| `TIME-WAIT` | green | first closer waits 60 s; many = short connections |
| `SYN-SENT` | amber | waiting for SYN-ACK; many for long = filtered or dead peer |
| `SYN-RECV` | amber / red | many = SYN flood or full accept queue |
| `FIN-WAIT-2` | amber | peer has not closed its side |
| `CLOSE-WAIT` | red | application did not `close()` |
| `LAST-ACK` | amber | final ACK pending |

| ICMP type / code | Meaning | Seen when |
|---|---|---|
| 0 | echo reply | ping answered |
| 3 / 0, 1 | network, host unreachable | no route, ARP failure at a router |
| 3 / 3 | port unreachable | UDP to a closed port; ends a UDP traceroute |
| 3 / 4 | fragmentation needed, DF set | path MTU smaller than the packet |
| 3 / 13 | administratively prohibited | firewall reject |
| 5 | redirect | a better gateway exists |
| 8 | echo request | ping |
| 11 / 0 | time exceeded in transit | TTL reached zero (traceroute hop) |

### Netfilter, BDP and DNS in one place

| Item | Rule |
|---|---|
| Forwarded packet | PREROUTING → FORWARD → POSTROUTING |
| Packet for the host | PREROUTING → INPUT; local output: OUTPUT → POSTROUTING |
| DNAT / SNAT | PREROUTING (before routing) / POSTROUTING (after) |
| Conntrack states | NEW, ESTABLISHED, RELATED, INVALID |
| First rule of a stateful firewall | `ct state established,related accept` |
| DROP / REJECT | silence and retries / immediate RST or ICMP error |
| BDP | bandwidth (bit/s) × RTT (s) ÷ 8 bytes |
| Window-limited rate | window × 8 ÷ RTT; 64 KB at 80 ms = 6.5 Mb/s |
| Mathis (loss-limited) | rate ≈ 1.22 × MSS ÷ (RTT × √p) |
| DNS status | NOERROR (empty = no such type), NXDOMAIN (no name), SERVFAIL (failed), REFUSED (policy) |
| DNS header flags | `qr` response, `aa` authoritative, `rd` / `ra` recursion desired / available, `ad` DNSSEC valid, `tc` truncated |
| Resolution order | `nsswitch.conf` `hosts: files dns` → `/etc/hosts`, then `resolv.conf` |
| Neighbour states | INCOMPLETE → REACHABLE → STALE → DELAY → PROBE → FAILED |
| Ephemeral ports | 32768-60999 (28 232) |

### Flashcards

| Q | A |
|---|---|
| `ip neigh` shows FAILED for the gateway | ARP got no reply: layer-2 problem (VLAN, cable, gateway down, wrong mask) |
| Which chain sees forwarded traffic? | FORWARD, after PREROUTING and before POSTROUTING |
| Filter for a pure SYN | <code>tcp[tcpflags] & (tcp-syn&#124;tcp-ack) == tcp-syn</code> |
| mtr loss at a middle hop only | ICMP rate limit; ignore unless it persists to the destination |
| What does `ip route get X` add to `ip route`? | The chosen route, output interface and source address |
| `ss` option for listening sockets with PID | `-lp` (usually `ss -tulpn`) |
| Why `-n` in ss, tcpdump, traceroute | skips name lookups: faster, no hidden port numbers |
| Thousands of CLOSE-WAIT | the application is not closing sockets: a code bug |
| Which side holds TIME-WAIT? | The side that closed first, 60 s on Linux |
| Pipe versus redirect | pipe joins two commands; redirect connects a stream to a file |
| `cmd 2>&1 > f` versus `cmd > f 2>&1` | the first leaves stderr on the terminal; the second sends both to the file |
| Why quote `"$var"` | to stop word splitting and globbing; empty `$var` in `rm -rf $var/` |
| `set -euo pipefail` | exit on error, error on unset variable, fail a pipeline if any stage fails |
| Permissions 750 | owner rwx, group r-x, others none |
| Sticky bit on /tmp | only the owner can delete their files in a shared directory |
| `kill` default signal | SIGTERM (15), catchable; SIGKILL (9) cannot be caught |
| `uniq -c` needs what first? | `sort`, because it counts adjacent duplicates only |
| Linux traceroute default probe | UDP to high ports; `-I` ICMP, `-T` TCP |
| Why does `* * *` appear? | no ICMP reply: filtered, rate-limited or not sent; not proof of a dead hop |
| ICMP 3/4 | fragmentation needed with DF set: path MTU discovery |
| Ping with DF to test MTU | `ping -M do -s 1472 X` (payload + 28 = packet size) |
| DNS: NXDOMAIN vs SERVFAIL | name absent vs failed lookup |
| `dig +cd` succeeds, plain `dig` fails | DNSSEC validation failure |
| `dig +trace` shows | root, TLD and authoritative referrals walked iteratively |
| Does `dig` read /etc/hosts? | No; use `getent hosts` for what applications see |
| tcpdump on ingress is before or after the firewall? | before; on egress, after |
| 64 KB packet seen on a 1500-MTU host | TSO/GSO: the tap sees the buffer before it is split |
| `ethtool -S` counters | cumulative since boot: take a delta |
| Duplex mismatch symptom | late collisions, CRC errors, speed falls under load |
| REJECT vs DROP | immediate error vs silence |
| `MASQUERADE` vs `SNAT` | masquerade uses the outgoing interface's current address |
| Why ESTABLISHED,RELATED first | matches most packets and lets replies in without open inbound ports |
| BDP of 1 Gb/s, 80 ms | 10 MB |
| `sysctl -w` persistence | none; write `/etc/sysctl.d/*.conf` and `sysctl --system` |
| Find the process on port 8080 | `ss -tlnp 'sport = :8080'` or `lsof -nP -i :8080` |
| DNS hang vs TCP hang in strace | wait after UDP send to :53 vs `connect` to target returning EINPROGRESS then a long poll |
| Policy routing in two lines | `ip route add default via B table 100`; `ip rule add from P lookup 100` |
:::
:::

:::
