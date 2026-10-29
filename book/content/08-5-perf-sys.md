::: {.p8}

## [8.13]{.sec}Performance: iperf3, BDP, socket buffers, sysctl [Should · ■■□]{.tag} {#s8-13}

Throughput questions need a measurement before a theory. `iperf3` generates traffic between two hosts and reports the achieved rate, which separates "the network is slow" from "the application is slow". The theory of windows and congestion control is in [3.9](#s3-9){.ref}; this section covers the tools and the Linux settings that decide whether the theory is reached.

```
server$ iperf3 -s                                      # listen on TCP/UDP 5201
client$ iperf3 -c 10.0.2.2 -t 30                       # one TCP stream for 30 s
client$ iperf3 -c 10.0.2.2 -P 4                        # four parallel streams
client$ iperf3 -c 10.0.2.2 -R                          # reverse: server sends (tests the other direction)
client$ iperf3 -c 10.0.2.2 -u -b 200M                  # UDP at a fixed rate: reports loss and jitter
client$ iperf3 -c 10.0.2.2 -w 64K                      # fix the socket buffer size
```

```
$ iperf3 -c 10.0.2.2 -t 3 -u -b 200M
[  5]   0.00-3.00   sec  71.5 MBytes   200 Mbits/sec  0.000 ms  0/55626 (0%)    sender
[  5]   0.00-3.00   sec  71.5 MBytes   200 Mbits/sec  0.011 ms  20/55626 (0.036%)  receiver
```

The TCP line shows bitrate and `Retr`, the retransmission count. The UDP line shows `Jitter` and `Lost/Total datagrams` at the receiver: loss in UDP is measured, not hidden. (Lab figures such as 16 Gb/s with two streams, over a virtual link with a round-trip time under 0.1 ms, show only the host's speed; they say nothing about a wide-area path.)

**Bandwidth-delay product.** A TCP sender may have at most one window of unacknowledged data in flight, so its throughput is at most *window ÷ RTT*. To fill a link the window must reach the *bandwidth-delay product* (BDP), the amount of data in the pipe: *BDP = bandwidth × RTT*. The analogy is a long pipe: the longer and wider it is, the more water must be poured in before the first drop comes out. For a 1 Gb/s path with an 80 ms RTT (a Mumbai to Frankfurt circuit), BDP = 10⁹ × 0.08 / 8 = 10 MB. A window of 64 KB, the largest without window scaling, allows 65 536 × 8 / 0.08 ≈ 6.5 Mb/s, under 1 % of the link.

<figure>
<svg viewBox="0 0 480 120" width="480">
<rect class="box" x="10" y="20" width="460" height="36" rx="18"/>
<rect class="hl" x="12" y="22" width="220" height="32" rx="16"/>
<text class="lbl" x="122" y="43" text-anchor="middle">window (data in flight)</text>
<text class="lbl" x="350" y="43" text-anchor="middle">empty pipe: link idle</text>
<path class="acc" d="M10 70 L470 70" fill="none"/><path class="acc" d="M10 64 L10 76 M470 64 L470 76" fill="none"/>
<text class="sm" x="240" y="86" text-anchor="middle">BDP = bandwidth × RTT = 10 MB (1 Gb/s × 80 ms)</text>
<text class="sm" x="240" y="104" text-anchor="middle">throughput = window / RTT: half the BDP in flight gives half the link rate</text>
</svg>
<figcaption><b>Figure 8.10</b> The pipe model. The link is full only when the data in flight equals the bandwidth-delay product; a window smaller than that leaves part of the pipe empty.</figcaption>
</figure>

| Link | RTT | BDP | Throughput with a 64 KB window |
|---|---|---|---|
| 100 Mb/s LAN | 1 ms | 12.5 KB | 100 Mb/s (window is larger than BDP) |
| 1 Gb/s campus WAN | 10 ms | 1.25 MB | 52 Mb/s |
| 1 Gb/s Mumbai to Frankfurt | 80 ms | 10 MB | 6.5 Mb/s |
| 10 Gb/s data-centre interconnect | 100 ms | 125 MB | 5.2 Mb/s |

**What decides the window.** The sender's window is limited by the smaller of the congestion window and the *receiver's advertised window*, which is bounded by the receive buffer. Linux sizes it automatically between the limits of `net.ipv4.tcp_rmem` (minimum, default, maximum, in bytes) for reading and `net.ipv4.tcp_wmem` for writing; `net.core.rmem_max` and `wmem_max` cap what an application may request with `SO_RCVBUF` ([7.10](#s7-10){.ref}). Window scaling (`net.ipv4.tcp_window_scaling=1`, on by default) multiplies the 16-bit window field by up to 2¹⁴, so windows above 64 KB are possible only if both ends negotiated it in the SYN (the `wscale` option seen in [8.7](#s8-7){.ref}). On a long fat pipe, check that the maximum of `tcp_rmem` and `tcp_wmem` is at least the BDP; the lab VM used for this chapter has a maximum of 32 MB, enough for about 2.7 Gb/s at 100 ms.

```
$ sysctl net.ipv4.tcp_rmem net.ipv4.tcp_wmem net.core.rmem_max net.ipv4.tcp_congestion_control
net.ipv4.tcp_rmem = 4096	131072	33554432
net.ipv4.tcp_wmem = 4096	16384	4194304
net.core.rmem_max = 4194304
net.ipv4.tcp_congestion_control = bbr
$ sysctl net.ipv4.tcp_available_congestion_control
net.ipv4.tcp_available_congestion_control = reno bbr cubic
```

**sysctl.** The kernel's tunable parameters appear as files under `/proc/sys`, and `sysctl` reads and writes them: `sysctl -w net.ipv4.ip_forward=1` changes the running kernel immediately and is lost at reboot. To make a change permanent one writes it into a file such as `/etc/sysctl.d/90-campus.conf` (`net.ipv4.ip_forward = 1`) and loads it with `sysctl --system`. The settings met most often are `ip_forward` (route between interfaces), `net.core.somaxconn` and `tcp_max_syn_backlog` (accept and SYN queues), `tcp_congestion_control` (cubic or bbr), `ip_local_port_range` (ephemeral ports; 32768 to 60999 here, about 28 000 simultaneous connections to one destination) and `tcp_tw_reuse`.

**Congestion control and queues.** `cubic` is the long-standing default and `bbr` estimates bandwidth and RTT directly rather than reacting to loss; `sysctl -w net.ipv4.tcp_congestion_control=bbr` switches new connections, and `ss -ti` shows which one a given connection uses. To reproduce a long path in a laboratory one adds delay and loss with the `netem` queueing discipline, `tc qdisc add dev eth0 root netem delay 40ms loss 0.1%`, and removes it with `tc qdisc del dev eth0 root`. (The kernel of the book's test VM lacked `netem`, so no measurement is printed; a laptop with Ubuntu 24.04 has it.)

::: example
**100 ms, 10 Gb/s, but 50 Mb/s per flow.** Compute the window the transfer actually uses and compare it with the BDP.

1. BDP = 10¹⁰ × 0.1 / 8 = 125 MB.
2. The window in use: 50 × 10⁶ × 0.1 / 8 = 625 KB, only 0.5 % of the BDP.
3. Two explanations give this size. (i) A buffer cap: a maximum receive buffer of about 625 KB, or window scaling absent (which would give 64 KB and 5 Mb/s, so scaling is present but the cap is low). (ii) Loss: by the Mathis relation, rate ≈ 1.22 × MSS / (RTT × √p), loss p = (1.22 × 1448 × 8 / (0.1 × 50 × 10⁶))² ≈ 8 × 10⁻⁶, one packet in 125 000.
4. Distinguish them with `ss -ti` during the transfer: `cwnd` small with `retrans` rising means loss, `rwnd_limited` or `snd_wnd` pinned means a buffer cap, and a capture shows window-full or zero-window flags ([8.8](#s8-8){.ref}).

[Result: raise `tcp_rmem`/`tcp_wmem` maxima towards 128 MB if buffer-limited; find and remove the loss otherwise, or try bbr, which tolerates random loss better than cubic. Several parallel streams (`-P`) also work around either limit.]{.result}
:::

::: check
1. A 622 Mb/s link has an RTT of 40 ms. What is the BDP? [^c813-1]
2. Why does `sysctl -w` not survive a reboot? [^c813-2]
:::

[^c813-1]: 622 × 10⁶ × 0.04 / 8 ≈ 3.1 MB.
[^c813-2]: It changes only the running kernel's value; the persistent source is a file in `/etc/sysctl.d/` loaded at boot.

## [8.14]{.sec}Systems debugging toolkit: /proc, lsof, strace, systemd [Should · ■■□]{.tag} {#s8-14}

When the network looks clean the fault is on the host: a process that died, a disk that filled, a service that never bound its port, a limit on open files. The tools in this section answer "what is this process doing" and "what does the system believe". Process, descriptor and system-call concepts are taught in [7.2](#s7-2){.ref} and [7.8](#s7-8){.ref}.

**/proc.** The `/proc` file system is a window onto the kernel, presented as files that are generated when read. `/proc/<pid>/` describes a process: `cmdline`, `status` (state, memory, threads), `fd/` (one symbolic link per open descriptor), `limits`, `net/`. System-wide files include `/proc/meminfo`, `/proc/loadavg`, `/proc/net/dev` (interface counters), `/proc/net/tcp` (the socket table in hexadecimal, from which `ss` once read), `/proc/net/route`, `/proc/net/arp` and `/proc/sys/net/*` (the tunables of [8.13](#s8-13){.ref}). Five worth remembering for networking are `/proc/net/dev`, `/proc/net/tcp`, `/proc/net/arp`, `/proc/sys/net/ipv4/ip_forward` and `/proc/<pid>/fd`.

```
$ ls -l /proc/21426/fd                       # the web server of the lab
lr-x------ 1 root root 64 0 -> /dev/null
l-wx------ 1 root root 64 1 -> /dev/null
lrwx------ 1 root root 64 3 -> socket:[125319]       <- descriptor 3 is the listening socket
$ grep -E 'Name|State|VmRSS|Threads' /proc/21426/status
Name:	python3
State:	S (sleeping)
VmRSS:	   19784 kB
Threads:	1
$ cat /proc/sys/net/ipv4/ip_forward
0
```

**lsof** ("list open files") shows which process holds which file or socket. Because sockets are files, it answers "who is using port 8080": `lsof -nP -i :8080`, and `lsof -nP -iTCP -sTCP:LISTEN` lists all listeners. `ss -tlnp` gives the same for sockets alone; `lsof +L1` finds deleted files that still occupy disk, a common cause of a "full" disk with no large file visible.

```
$ lsof -nP -i :8080
COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 21426 root    3u  IPv4 125319      0t0  TCP 10.0.2.2:8080 (LISTEN)
$ kill 21426                                  # SIGTERM first: lets the program close its connections
```

**strace** prints the system calls a process makes, with arguments and return values, which turns "it hangs" into a specific call. `strace -f -tt -e trace=network,connect,poll curl …` follows children (`-f`), adds timestamps (`-tt`) and filters to the network calls. For a hanging `curl`, two patterns separate the causes. A DNS hang shows `connect` to the resolver's address on port 53 (or `sendto` on a UDP socket) followed by a long `poll` with no reply before any `connect` to the target. A TCP hang shows the name resolved, then `connect(5, {sin_port=htons(8080), sin_addr=inet_addr("10.0.2.2")}, 16) = -1 EINPROGRESS` followed by a `poll` that waits until the timeout, the signature of a dropped SYN. A refused port instead returns the error at once (`ECONNREFUSED`).

```
$ strace -f -tt -e trace=connect,ppoll curl -s -m2 http://10.0.2.2:8080/ -o /dev/null
13:35:39.483272 connect(3, {sa_family=AF_UNIX, sun_path="/var/run/nscd/socket"}, 110) = -1 ENOENT
13:35:39.484290 connect(5, {sa_family=AF_INET, sin_port=htons(8080), sin_addr=inet_addr("10.0.2.2")}, 16) = -1 EINPROGRESS
```

(The first line is the C library looking for a name-service cache daemon that is not installed, a harmless failure; the second, in a run with the port blocked by a firewall, is followed by a wait with no answer.) Attaching to a running process uses `strace -p PID`; `strace -c` prints a table of calls and time, which finds the slow call.

**systemd and the journal.** Most distributions start services with *systemd*. `systemctl status nginx` shows whether a unit is active, its main process, the last log lines and why it stopped; `systemctl restart|reload|enable --now nginx`, `systemctl list-units --failed` and `systemctl list-timers` are the others in daily use. Service logs go to the *journal*, read with `journalctl`: `journalctl -u nginx --since "10 min ago"`, `-f` (follow), `-p err` (priority error and above), `-b` (since the last boot) and `-k` (kernel messages, the equivalent of `dmesg`). (The lab container ran without systemd as its first process, so these commands cannot be shown with real output here; they behave as described on any standard Ubuntu host.)

**Resource tools.** `top` or `htop` shows CPU and memory per process; `vmstat 1` prints one line per second with run-queue length (`r`), swap (`si`, `so`), blocked I/O (`b`) and CPU split (`us sy id wa`); `free -m` shows memory (the `available` column is what applications can use, not `free`); `df -h` shows file systems and `du -sh /var/log/*` finds what fills one; `iostat -x 1` shows disk utilisation; `uptime` or `/proc/loadavg` show load averages. Two limits cause strange failures. The *open files* limit, `ulimit -n` (20 000 in the lab shell, often 1024 by default), caps descriptors and therefore connections: "too many open files" in a server log is this. A *full disk* makes services fail to write logs, sockets or temporary files, and the symptom can be a 502 from the proxy in front.

::: example
**A website returns 502 Bad Gateway.** The reverse proxy is up, so it cannot reach the application behind it.

1. `systemctl status app` shows the unit `failed`; the last lines show it exited.
2. `journalctl -u app --since "10 min ago"` shows `OSError: [Errno 28] No space left on device`.
3. `df -h` shows `/var` at 100 %; `du -sh /var/log/* | sort -h | tail -3` finds a 40 GB log file written by a debug option left on.
4. Truncate the file (`: > /var/log/app/debug.log`; deleting it while the process runs would not free space until the process exits, which `lsof +L1` would reveal), restart the unit, and configure `logrotate` with size limits.

[Result: the 502 was the symptom of a disk problem two layers away; none of the network tools would have found it, which is why the host checks are part of the method in [Pillar 11](#ch11){.ref}.]{.result}
:::

<figure>
<svg viewBox="0 0 480 150" width="480"><defs><marker id="a814" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker></defs>
<g class="box"><rect x="4" y="10" width="86" height="34" rx="2"/><rect x="104" y="10" width="86" height="34" rx="2"/><rect x="204" y="10" width="86" height="34" rx="2"/><rect x="304" y="10" width="86" height="34" rx="2"/><rect x="404" y="10" width="72" height="34" rx="2"/></g>
<g class="lbl" text-anchor="middle"><text x="47" y="25">Process alive?</text><text x="147" y="25">Listening, right</text><text x="247" y="25">Local firewall</text><text x="347" y="25">Reachable from</text><text x="440" y="25">App logs</text></g>
<g class="sm" text-anchor="middle"><text x="47" y="37">systemctl, ps</text><text x="147" y="37">IP and port? ss -tlnp</text><text x="247" y="37">allows it? nft/ipt</text><text x="347" y="37">peer? nc, curl, tcpdump</text><text x="440" y="37">journalctl</text></g>
<path class="ln" d="M90 27 L104 27 M190 27 L204 27 M290 27 L304 27 M390 27 L404 27" fill="none" marker-end="url(#a814)"/>
<g class="sm" text-anchor="middle"><text x="47" y="66">no: journalctl -u, disk,</text><text x="47" y="76">memory, ulimit</text><text x="147" y="66">127.0.0.1 only, or wrong</text><text x="147" y="76">port: fix the bind</text><text x="247" y="66">counters on DROP rule</text><text x="247" y="76">rising: add ACCEPT</text><text x="347" y="66">SYN seen, no SYN-ACK:</text><text x="347" y="76">drop or path; RST: closed</text><text x="440" y="66">5xx, auth, config,</text><text x="440" y="76">upstream timeouts</text></g>
<path class="lg dash" d="M47 46 L47 58 M147 46 L147 58 M247 46 L247 58 M347 46 L347 58 M440 46 L440 58" fill="none"/>
<text class="sm" x="240" y="108" text-anchor="middle">Work left to right; stop at the first rung that fails, and fix that before testing the next.</text>
<text class="sm" x="240" y="122" text-anchor="middle">Host checks come first because a process that is not running cannot be fixed by any network change.</text>
</svg>
<figcaption><b>Figure 8.11</b> A decision ladder for "service unreachable on Linux". Each rung has one command and one typical finding.</figcaption>
</figure>

::: lens
[AMAZON SYSDE · GOOGLE SRE · ARISTA · JUNIPER]{.co}

"What is in /proc", "find the process on port 8080 and stop it", "strace a hanging curl" and "disk is full, service is down" are standard live-shell questions. A strong answer uses the specific file or command, explains what it reads (kernel state, not stored files), names the signal sequence (TERM, then KILL) and checks the cause afterwards (the 40 GB log, the missing `close()`). Follow-ups: `ulimit -n` and `/proc/<pid>/limits`, zombie processes, and `strace -c` for a profile. Solved forms are Q8.20, Q8.21, Q8.22 and Q8.28.
:::

::: check
1. How does `strace` distinguish a DNS hang from a TCP connect hang? [^c814-1]
2. A deleted 10 GB log is still filling the disk. Which command finds the holder? [^c814-2]
:::

[^c814-1]: A DNS hang waits on port 53 before any connect to the target; a TCP hang shows `connect` to the target returning `EINPROGRESS` and then waiting.
[^c814-2]: `lsof +L1` (files with a link count below one) shows the process holding the deleted file open.

:::
