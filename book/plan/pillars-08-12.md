# Chapter Plan — Pillars 8 to 12

> Scope: Pillar 8 (Linux & Network Tools), Pillar 9 (Network Security), Pillar 10 (Network Automation), Pillar 11 (Troubleshooting Methodology), Pillar 12 (Supporting Subjects).
> Audience: Indian B.E./B.Tech student, 2nd to 4th year, assumed to have finished Pillars 1–7 (or to be reading them in parallel where noted).
> Spelling: British. Command output in figures is always shown as real-looking terminal text in a monospaced "terminal card" (dark slate background, green prompt) so the reader learns to *read output*, not just type commands.

## Book-wide conventions used in these pillars

| Element | Visual treatment | Purpose |
|---|---|---|
| **Analogy box** ("Think of it like…") | Soft saffron left rule, chai-cup icon | Beginner bridge using Indian everyday life (railway, dabbawalas, housing society, Aadhaar, post office, toll plaza) |
| **Terminal card** | Dark slate, monospaced, prompt `user@lab:~$` | Every command shown with *real* output and callout numbers ①②③ explaining fields |
| **Trap box** | Red border, warning-triangle icon | The exact wrong answer interviewers hear most often, and the correct one |
| **Interviewer's lens** | Indigo side panel, magnifier icon | What the interviewer is actually scoring |
| **Company tag chips** | Small pills: `CSCO` `QCOM` `GOOG` `MSFT` `AMZN-NDE` `JNPR` `ANET` `NOK` `AVGO` | Shows where a topic is most frequently probed |
| **Difficulty tags** | 🟢 Warm-up / 🟡 Core / 🔴 Stretch (rendered as coloured dots, not emoji, in the PDF) | Question banks |
| **Lab card** | Grey tile with time estimate, kit list, success criterion | Hands-on |

Company abbreviations in matrices: ● = frequently probed, ◐ = sometimes, ○ = rare. Matrices are built from candidate reports (Glassdoor, GfG, Code360, PrepInsta, FACE Prep) and job descriptions; the book must label them "observed patterns, not official syllabi".

Standard lab environment for all five pillars (introduced once in Pillar 8, reused): an Ubuntu 24.04 LTS VM (or WSL2) + **containerlab** with images that need **no registration** (FRRouting, Nokia SR Linux, Alpine/Ubuntu hosts). Arista cEOS-lab (free account), Cisco DevNet sandboxes and GNS3/EVE-NG are marked *optional alternatives* only. Laptop minimum: 8 GB RAM, 4 cores.

## Reader constraints that govern Pillars 8–12 (added per user brief)

### A. Comprehensive content; priority tags; optional 8-week study route
**The book is not trimmed to any time limit.** Every pillar keeps its full scope; the 8-week figure is one reader's personal timeline, so it appears only as an optional study route (a printed "8-Week Route" insert), never as a cap on content.

Every section carries a **priority tag** (navigation aid) and an **indicative study-day estimate** (fractions of a ~3-hour day):
- **MUST** — asked often enough that skipping it risks failing a round.
- **SHOULD** — common in at least two target companies.
- **OPTIONAL** — depth/differentiator for specific roles (the company chip shows who values it). Optional sections are complete and fully taught, not stubs.
Per pillar a **"MUST-only path"** is listed for time-pressed readers.

Optional **8-Week Route** (≈ 56 days × 3 h; coordinator to reconcile with Pillars 1–7). Under this route the reader covers MUST + most SHOULD sections; OPTIONAL sections are flagged "after placement season / role-specific":

| Pillar | Full-coverage days | 8-week route days | Placement in route |
|---|---|---|---|
| 1 DSA | — | 12 | Weeks 1–8, daily coding block |
| 2 Programming | — | 4 | Week 1 |
| 3 CN fundamentals | — | 5 | Weeks 1–2 |
| 4 Routing & Switching | — | 5 | Weeks 2–3 |
| 5 DC & cloud | — | 2 | Week 4 |
| 6 Wireless | — | 2 | Week 4 |
| 7 OS & sockets | — | 3 | Week 3 |
| **8 Linux & tools** | **4.5** | **3.5** | Week 4 |
| **9 Network security** | **4.5** | **3.5** | Week 5 |
| **10 Automation** | **3.0** | **2.5** | Week 6 |
| **11 Troubleshooting** | **5.0** | **4.0** | Weeks 6–7 (needs 3, 4, 8, 9) |
| **12 Supporting subjects** | **9.0** | **7.0** | 12A aptitude as a 30-min daily drill from Week 1; 12B–12G in Weeks 7–8; last 2 days = mock OA + mock interviews |

All labs and mini-projects stay in the book in full. A reader on the 8-week route is advised to build one flagship project (Pillar 10 *FabricOps* or Pillar 8 *netdoctor*); others remain available.

### B. Fully self-contained PDF
- Every command shown in the book is printed **with its full expected output**, so a reader without a lab can still learn from "paper labs".
- Every lab card contains: install commands, every file (topology YAML, scripts, configs) **printed in full** in a listing, expected output, a "what if it breaks" box, and a **paper-lab variant** (questions answered from printed output alone).
- Appendix "Lab Setup from Zero" (shared across pillars, ~8 pages): Ubuntu/WSL2 install, Docker, containerlab, FRR/SR Linux images, Python venv with pinned versions, Wireshark, all in numbered steps with screenshots.
- RFC/standard facts needed for interviews are **restated in the text**; the "Sources" list at each pillar end is relabelled **"Author verification sources — not required reading"**.
- All pcaps, logs and datasets used in labs are **printed as excerpts** in the book (and optionally provided as files), so no download is mandatory.

### C. Answer standard for every interview question
Every question in every bank gets a **full in-book solution** in the end-of-chapter pack, written to this template:
1. **30-second answer** (what you say first, 2–4 sentences).
2. **Full answer** (the 2–3 minute version) with diagram/command output where useful.
3. **Likely follow-ups** (2–3), each with its own short answer.
4. **Common wrong answer** and why it loses marks.
5. For coding/scripting questions: complete, runnable code, sample input/output, complexity, and edge cases.
6. For scenario/design questions: a structured walk-through (clarifying questions → approach → trade-offs → final answer).
Page budget: ~0.5 page per 🟢, ~0.75 per 🟡, ~1–1.5 per 🔴 question.

### D. End-of-chapter pack (identical structure for Pillars 8–12)
1. **Short notes** (3–5 pages): one boxed paragraph + 5–8 bullets per section, in section order, tagged MUST/SHOULD/OPTIONAL.
2. **One-page revision sheet**: the single page to read the night before the interview (the denser cheat-sheet contents listed per pillar are compressed onto this one page; overflow goes to a "command appendix").
3. **Flashcards** (40 per pillar; 60 for Pillar 12): printed 8 per page in a cut-out grid, front = prompt, back = answer on the following page aligned for double-sided printing; each card tagged with section and priority. Spaced-repetition schedule tied to the 8-week plan: review on Day +1, +3, +7, +14 after the pillar, printed as a tick-box table.
4. **Solved interview problems**: every question from the bank solved per standard C, ordered by difficulty, with company chips.
5. **Self-test**: 15-minute timed quiz (10 MCQs + 2 short answers) with answers, to decide whether to move on or revisit.

---

# PILLAR 8 — Linux & Network Tools

**Chapter title:** *The Engineer's Toolbox: Seeing the Network from a Linux Shell*
**One-line promise:** By the end you will diagnose any "it doesn't connect" complaint on a Linux box in under ten minutes using `ip`, `ss`, `tcpdump`, `dig`, `mtr` and friends, and explain every field of their output.

- **Prerequisites:** Pillar 3 (OSI/TCP-IP, ARP, TCP handshake, DNS basics); Pillar 7 (processes, file descriptors, sockets) helpful. Comfort typing in a terminal.
- **Estimated pages:** 90 (teaching 60 + end-of-chapter pack 30, of which solved questions ≈ 22)
- **Study days:** 4.5 (Week 4 of 8). MUST-only path: 3.1 days.

## Learning objectives
1. Navigate the Linux shell confidently: files, pipes, redirection, permissions, process control, and the "text-processing quartet" `grep`, `awk`, `sed`, `cut`/`sort`/`uniq`.
2. Write Bash scripts with variables, conditionals, loops, functions, exit codes and `set -euo pipefail`, and know when to switch to Python.
3. Inspect and modify interfaces, addresses, routes, neighbours, policy routing and namespaces with `iproute2` (`ip link/addr/route/neigh/rule/netns`), and map each to the legacy `ifconfig/route/arp/netstat` commands.
4. Read socket state with `ss` (listening ports, owning process, TCP internals such as `cwnd`, `rtt`, retransmits) and relate each TCP state to the state machine.
5. Capture and filter packets with `tcpdump` (BPF syntax) and analyse them in Wireshark (display filters, Follow TCP Stream, Expert Info, I/O graphs, TCP sequence graphs).
6. Resolve and debug DNS with `dig` (`+trace`, `+short`, `@server`, record types, TTL, flags), and explain recursive vs iterative resolution from output.
7. Diagnose path problems with `ping`, `traceroute` (UDP/ICMP/TCP modes), `mtr`, `tracepath` (PMTU), and recognise ICMP rate-limiting false alarms.
8. Diagnose NIC/link problems with `ethtool` (speed/duplex, `-S` counters, `-k` offloads, `-g` rings) and `/proc/net/dev`, `nstat`, `ip -s link`.
9. Build, read and debug packet-filter rule sets in `iptables` (tables, chains, hooks, conntrack) and `nftables`, including NAT and stateful filtering.
10. Measure performance with `iperf3`, `curl -w` timing, `sar`, and reason with bandwidth-delay product and kernel buffer `sysctl`s.
11. Use systems-debugging tools that NDE/SDE interviews love: `lsof`, `strace`, `/proc`, `journalctl`, `systemctl`, `top/htop`, `vmstat`, `df/du`, `free`.

## Priority tags & indicative study days
| § | Section | Tag | Days | Core lab |
|---|---|---|---|---|
| 8.1 | Why Linux | MUST | 0.10 | — |
| 8.2 | Shell survival kit | MUST | 0.30 | — |
| 8.3 | Text processing | MUST | 0.40 | L8.1 |
| 8.4 | Bash scripting | SHOULD (MUST for AMZN-NDE, ANET) | 0.25 | — |
| 8.5 | iproute2 | MUST | 0.50 | L8.2 |
| 8.6 | `ss` & TCP states | MUST | 0.40 | L8.3 (paper variant) |
| 8.7 | tcpdump | MUST | 0.50 | L8.4 (HTTP + RST parts) |
| 8.8 | Wireshark analysis | SHOULD | 0.25 | — |
| 8.9 | DNS with dig | MUST | 0.30 | L8.5 |
| 8.10 | Path tools / mtr | MUST | 0.35 | L8.6 (paper variant) |
| 8.11 | ethtool & NIC | SHOULD (MUST for QCOM, AVGO) | 0.15 | — |
| 8.12 | iptables/nftables | MUST | 0.35 | L8.7 (host-firewall half) |
| 8.13 | Performance & BDP | SHOULD | 0.10 | — |
| 8.14 | /proc, strace, systemd | SHOULD | 0.15 | — |
| — | End-of-chapter pack (notes, flashcards, solved Qs, self-test) | MUST | 0.40 | — |
| | **Total (full coverage)** | | **4.50** | MUST-only path = 3.10 |

Labs L8.4 (HTTPS decryption half), L8.7 (NAT half), L8.8 and the mini-project are tagged OPTIONAL (fully specified in the book, outside the day estimate).

## Section-by-section outline

### 8.1 Why a network engineer lives in Linux
- **Core idea:** Every major NOS is Linux underneath or beside (Arista EOS, Cisco NX-OS with Bash shell, Juniper Junos Evolved, Nokia SR Linux, SONiC at Microsoft/Google-style fleets, Cumulus). Servers, hypervisors and cloud VMs are Linux. Your first tool in every incident is a shell.
- **Analogy:** Linux is the "control room of Indian Railways": the dashboards (GUI) are optional; the signalling cabin (shell) is where real work happens.
- **Worked example:** Show the same "show interface" information three ways: Arista EOS `show interfaces Ethernet1`, then `bash ip -s link show et1` inside EOS, then a plain Ubuntu host — same counters, same kernel.
- **Figures:** *Fig 8.1* — Layer-cake diagram: hardware ASIC / NIC → Linux kernel (netdev, routing table, netfilter, sockets) → user space (FRR, sshd, NOS CLI). Arrows show where each tool in this chapter "taps in" (`ethtool` → driver; `ip` → netlink to kernel tables; `ss` → sock_diag; `tcpdump` → AF_PACKET before netfilter on ingress; `iptables/nft` → netfilter hooks).

### 8.2 Shell survival kit (files, pipes, permissions, processes)
- **Core idea:** Everything is a file; small tools composed with pipes; exit codes signal success. Permissions `rwx` for user/group/other; `chmod 750`; `sudo`.
- **Analogy:** Pipes are a dabbawala relay: each runner does one job and passes the tiffin on.
- **Worked example:** "Top 5 source IPs hitting nginx": `awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -5` — dissect each stage with intermediate output.
- **Figures:** *Fig 8.2* — Pipeline diagram with sample data shown between each stage (boxes connected by arrows labelled stdin/stdout, stderr branching off to a dustbin `2>/dev/null`). *Fig 8.3* — Permission bit map: `-rwxr-x---` broken into type/user/group/other with octal 7 5 0 underneath.

### 8.3 Text processing for log hunting: grep, awk, sed, cut, sort, uniq, jq
- **Core idea:** Interviews (Amazon NDE especially) ask you to parse logs live. `grep -E`, `-v`, `-c`, `-o`, `-A/-B`; `awk` fields and `NR`, `$NF`; `sed -n 's/…/…/p'`; `jq` for JSON from APIs.
- **Analogy:** `grep` is the sieve, `awk` is the spreadsheet, `sed` is find-and-replace.
- **Worked example:** From a syslog file, count `%LINEPROTO-5-UPDOWN` flaps per interface in the last hour and print interfaces that flapped more than 3 times.
- **Figures:** *Fig 8.4* — Annotated syslog line with field numbers `$1…$NF` above each token as `awk` sees them.

### 8.4 Bash scripting that survives production
- **Core idea:** Shebang, variables, quoting (`"$var"`), `if/case/for/while`, functions, `$?`, `trap`, `set -euo pipefail`, arguments `$1 $@`, `getopts`; cron. Rule of thumb: > 50 lines or any data structure → Python.
- **Analogy:** A script is a recipe a junior cook can follow at 3 a.m. without calling you.
- **Worked example:** `reach.sh hosts.txt` — pings each host with timeout, records up/down with timestamp to CSV, exits non-zero if any host is down (suitable for cron/monitoring).
- **Figures:** *Fig 8.5* — Flowchart of the script with exit-code branches; side table "common Bash bugs" (unquoted variables with spaces, `[ $x == y ]` with empty x, word splitting).

### 8.5 iproute2 deep dive: `ip link`, `ip addr`, `ip route`, `ip neigh`, `ip rule`, `ip netns`
- **Core idea:** Netlink-based single tool for L2/L3 state. Read `ip -br a`, `ip -s link`, `ip route get 8.8.8.8` (which route + source address the kernel would actually use), `ip neigh` states (REACHABLE, STALE, DELAY, PROBE, FAILED, INCOMPLETE), policy routing tables, VRFs, network namespaces, veth pairs, bridges, VLAN sub-interfaces (`ip link add link eth0 name eth0.10 type vlan id 10`).
- **Analogy:** The routing table is the railway timetable board; `ip route get` is asking the enquiry counter "which platform for *this* train?"
- **Worked example:** Build two namespaces `red` and `blue` joined by a veth pair, address them 10.0.0.1/24 and 10.0.0.2/24, ping, then add a third namespace as a router with `net.ipv4.ip_forward=1` and static routes. Show the moment ping fails because forwarding is off.
- **Figures:** *Fig 8.6* — Namespace topology drawing (three rounded boxes with veth "cables", IPs on each end, routing table snippets inside each box). *Fig 8.7* — `ip neigh` state-machine diagram (NUD states with transitions labelled "packet sent", "confirmation", "timeout"). *Fig 8.8* — Legacy→modern Rosetta table (`ifconfig`→`ip a`, `route -n`→`ip r`, `arp -n`→`ip n`, `netstat -tulpn`→`ss -tulpn`, `brctl`→`ip link … type bridge`).

### 8.6 Sockets on the wire: `ss` (and why `netstat` retired)
- **Core idea:** `ss -tulpn` (TCP/UDP, listening, process, numeric); `ss -tan state established`; `ss -ti` exposes kernel TCP_INFO: `rtt`, `cwnd`, `retrans`, `mss`, `send` rate; filters `ss -tn dst 10.0.0.5 dport = :443`. Relate to TCP states (LISTEN, SYN-SENT, SYN-RECV, ESTAB, FIN-WAIT-1/2, TIME-WAIT, CLOSE-WAIT, LAST-ACK).
- **Analogy:** `ss` is the hotel reception register: who is checked in (ESTAB), who booked but has not arrived (SYN-RECV), who checked out but the room is not cleaned (TIME-WAIT).
- **Worked example:** A Flask app "isn't reachable from outside": `ss -tlnp` shows `127.0.0.1:5000` → bound to loopback only. Fix: bind `0.0.0.0`. Second example: thousands of `CLOSE-WAIT` → application not calling `close()` (bug in app, not network).
- **Figures:** *Fig 8.9* — TCP state diagram with each state labelled by the `ss` keyword; heat colouring of states that signal trouble (many SYN-RECV = SYN flood or backlog; many CLOSE-WAIT = app leak; many TIME-WAIT = normal on client side of short connections). *Fig 8.10* — Annotated `ss -ti` output with callouts on `rtt:12.3/4.1`, `cwnd:10`, `retrans:0/3`.

### 8.7 Packet capture I: `tcpdump`
- **Core idea:** `tcpdump -i any -nn -s 0 -w file.pcap`; BPF filters (`host`, `net`, `port`, `tcp[tcpflags] & (tcp-syn|tcp-fin) != 0`, `icmp`, `vlan`, `ether host`); `-e` for MAC headers; `-c`, `-G/-W` ring buffers; reading flags `[S]`, `[S.]`, `[.]`, `[P.]`, `[F.]`, `[R]`. Where capture sits relative to netfilter (ingress capture *before* iptables drops; egress after).
- **Analogy:** A CCTV camera at the society gate: it records everyone who walks up, even those the guard (firewall) then turns away.
- **Worked example:** Capture a `curl http://example.com` and annotate the 3-way handshake, HTTP GET, response, FIN exchange; then a failing case showing SYN retransmits at 1 s, 3 s, 7 s (exponential backoff) with no SYN-ACK → "packets leave, nothing returns".
- **Figures:** *Fig 8.11* — Annotated tcpdump line decoded field by field (timestamp, interface, direction, src.port > dst.port, flags, seq, ack, win, options [mss, sackOK, TS, nop, wscale], length). *Fig 8.12* — Timeline ladder diagram of the capture with retransmission timer gaps drawn to scale.

### 8.8 Packet capture II: Wireshark for analysis
- **Core idea:** Capture filter (BPF) vs display filter (`tcp.analysis.retransmission`, `tcp.flags.reset==1`, `dns.flags.rcode != 0`, `http.response.code >= 400`, `tls.handshake.type == 1`, `ip.addr==x && !(tcp.port==22)`); Follow TCP Stream; Statistics → Conversations, Endpoints, I/O Graph; Expert Info; TCP Stream Graph (Stevens); decrypting TLS with `SSLKEYLOGFILE`.
- **Analogy:** tcpdump is the camera, Wireshark is the forensic lab.
- **Worked example:** Provided pcap of a slow download: use Expert Info to find "Duplicate ACK" and "Fast Retransmission" clusters, I/O graph shows throughput collapse coinciding with zero-window advertisements from the receiver → receiver-side bottleneck, not network loss.
- **Figures:** *Fig 8.13* — Wireshark three-pane screenshot style mock-up (packet list, details tree, bytes) with numbered callouts. *Fig 8.14* — Side-by-side: zero-window vs packet-loss signatures in a Stevens graph.

### 8.9 DNS from the command line: `dig`, `nslookup`, `host`, `resolvectl`
- **Core idea:** `dig example.com A`, `+short`, `@8.8.8.8`, `+trace` (walk from root → TLD → authoritative), `+norecurse`, `-x` (PTR), `MX/NS/TXT/AAAA/CNAME/SOA`; header flags `qr rd ra aa ad`; status `NOERROR/NXDOMAIN/SERVFAIL/REFUSED`; TTL counting down in caches; `/etc/resolv.conf`, `systemd-resolved` stub `127.0.0.53`, `/etc/hosts` and `nsswitch.conf` order.
- **Analogy:** DNS is directory enquiry: the local resolver is your housing-society secretary who either knows the answer (cache) or phones around (recursion).
- **Worked example:** `dig +trace www.iitb.ac.in` annotated hop by hop; then a SERVFAIL caused by broken DNSSEC (`dig +cd` succeeds → validation failure).
- **Figures:** *Fig 8.15* — Annotated `dig` output with sections HEADER / QUESTION / ANSWER / AUTHORITY / ADDITIONAL highlighted. *Fig 8.16* — Recursive vs iterative resolution sequence diagram (stub → recursive resolver → root → .in TLD → ac.in → authoritative).

### 8.10 Path and reachability: `ping`, `traceroute`, `tracepath`, `mtr`, `arping`, `nc`, `curl`
- **Core idea:** `ping -c -s -M do` (DF bit, MTU probing); traceroute TTL mechanism; UDP (Linux default) vs ICMP (`-I`) vs TCP (`-T -p 443`) modes; reading `* * *`; `mtr -rwzbc 100` report columns Loss%, Snt, Avg, StDev; rule "loss that does not persist to the final hop is ICMP rate-limiting / control-plane policing, not real loss"; `nc -zv host 443` port test; `curl -v` and `curl -w '%{time_namelookup} %{time_connect} %{time_appconnect} %{time_starttransfer}'`.
- **Analogy:** Traceroute is sending a series of letters with "return to sender after N post offices" stamped on them; each post office that returns one reveals itself.
- **Worked example:** mtr report where hop 4 shows 60 % loss but hops 5–9 show 0 % → explain CoPP rate limiting; contrast with a report where loss starts at hop 6 and persists to destination → real problem at/after hop 6.
- **Figures:** *Fig 8.17* — TTL-expiry diagram (packets with TTL=1,2,3 dying at successive routers, ICMP Time Exceeded arrows returning). *Fig 8.18* — Two mtr reports side by side, "false alarm" vs "real loss", with shaded columns. *Fig 8.19* — `curl -w` timing waterfall bar (DNS | TCP | TLS | server think time | transfer).

### 8.11 Link layer and NIC health: `ethtool`, `ip -s link`, `/proc/net/dev`, `nstat`
- **Core idea:** `ethtool eth0` (speed, duplex, autoneg, link detected); `ethtool -S` driver counters (rx_crc_errors, rx_missed, tx_dropped); `ethtool -k` offloads (TSO/GSO/GRO explain why tcpdump shows 64 KB "packets"); `ethtool -g` ring sizes; `ethtool -i` driver/firmware; `nstat -az | grep -i retrans`.
- **Analogy:** `ethtool` is the mechanic's diagnostic plug for the car (NIC); counters are the odometer.
- **Worked example:** Server at 100 Mb/s half-duplex after a cable change, late collisions & CRC errors rising → bad cable / autoneg mismatch; fix and verify counters stop incrementing (take two snapshots 10 s apart — counters are cumulative).
- **Figures:** *Fig 8.20* — "Counter delta" diagram: two snapshots, subtraction, rate per second. *Fig 8.21* — Offload illustration: one 64 KB super-segment in the kernel split into 45 × 1448-byte wire segments by NIC (TSO), and GRO doing the reverse on receive.

### 8.12 Netfilter: `iptables` and `nftables`
- **Core idea:** Hooks PREROUTING → (routing decision) → INPUT / FORWARD → OUTPUT → POSTROUTING; tables `raw`, `mangle`, `nat`, `filter`, `security`; targets ACCEPT/DROP/REJECT/LOG/DNAT/SNAT/MASQUERADE; first-match semantics; default policy; conntrack states NEW/ESTABLISHED/RELATED/INVALID; `iptables -L -n -v --line-numbers` packet counters as a debugging tool; `iptables-save`; nftables syntax (`nft list ruleset`, sets, maps, inet family); `conntrack -L`; ufw/firewalld as front-ends.
- **Analogy:** Netfilter is a toll plaza with lanes (chains) and booth operators (rules): the first booth that recognises your vehicle decides your fate.
- **Worked example:** Build a host firewall: allow established/related, allow SSH from 10.0.0.0/8, allow 443 from anywhere, drop everything else, log drops with rate limit; then build a NAT gateway (MASQUERADE out eth0, DNAT port 8080 → 192.168.1.10:80). Show the classic mistake: DROP placed above ACCEPT; show counters proving which rule matched. Same rules rewritten in nftables.
- **Figures:** *Fig 8.22* — Netfilter packet-flow diagram (the classic "packet flow in Netfilter" simplified: boxes for each hook, colour per table, routing decision diamonds, local process box). *Fig 8.23* — Side-by-side iptables vs nftables rule translation table.

### 8.13 Performance measurement: `iperf3`, BDP, socket buffers, `sysctl`
- **Core idea:** `iperf3 -s` / `-c -P 4 -t 30 -R`; UDP mode jitter/loss; BDP = bandwidth × RTT; `net.core.rmem_max`, `net.ipv4.tcp_rmem`, window scaling; congestion control (`sysctl net.ipv4.tcp_congestion_control` cubic vs bbr); `tc qdisc` and `netem` to inject delay/loss for labs.
- **Analogy:** BDP is the number of litres of water inside a pipe: long, wide pipe → you must pour a lot before the first litre comes out.
- **Worked example:** 1 Gb/s link with 80 ms RTT Mumbai→Frankfurt: BDP = 10⁹ × 0.08 / 8 = 10 MB; a 64 KB window gives max 64 KB/0.08 s ≈ 6.5 Mb/s. Use netem to reproduce in lab and show iperf3 improving after raising buffers.
- **Figures:** *Fig 8.24* — Pipe-filling diagram with window size vs BDP. *Fig 8.25* — Bar chart: iperf3 throughput vs buffer size (lab results, captioned as illustrative).

### 8.14 Systems debugging toolkit: `/proc`, `lsof`, `strace`, `systemctl`, `journalctl`, resource tools
- **Core idea:** `/proc/<pid>/fd`, `/proc/net/tcp`, `/proc/sys/net/*`, `/proc/meminfo`; `lsof -i :443`; `strace -f -e trace=network`; `systemctl status`, `journalctl -u nginx --since "10 min ago"`; `top`, `vmstat 1`, `iostat`, `df -h`, `du -sh`, `free -m`; "disk full → service crash" and "too many open files" (`ulimit -n`) stories.
- **Analogy:** `/proc` is the X-ray of a running system.
- **Worked example:** "Website returns 502": `systemctl status app` shows crashed; `journalctl` shows `No space left on device`; `df -h` 100 %; `du -sh /var/log/*` finds a 40 GB log; fix with logrotate.
- **Figures:** *Fig 8.26* — Decision tree "service unreachable on Linux": process running? → listening on right IP/port? → local firewall? → reachable from peer? → app logs.

## Hands-on labs
| Lab | Title | Time | Success criterion |
|---|---|---|---|
| L8.1 | Log-hunting dojo: 10 graded one-liners on a provided 50k-line nginx log and Cisco syslog | 90 min | All 10 answers match key |
| L8.2 | Namespaces & veth: build 3-namespace routed lab, then break forwarding/route/ARP and fix | 2 h | Ping across; written explanation of each breakage |
| L8.3 | `ss` safari: run a toy server/client in Python, observe every TCP state including TIME-WAIT and CLOSE-WAIT (deliberately skip `close()`) | 75 min | Screenshot of each state with explanation |
| L8.4 | Handshake forensics: capture HTTP, HTTPS (with SSLKEYLOGFILE decryption), DNS, and a refused connection (RST) | 2 h | Annotated pcap exported as PDF |
| L8.5 | DNS detective: `dig +trace` five domains, a deliberately broken local `resolv.conf`, `/etc/hosts` override | 60 min | Correct diagnosis of three planted faults |
| L8.6 | Path doctor: containerlab FRR chain of 5 routers, introduce CoPP-like ICMP rate limit on R3 vs real loss with netem on R4; interpret mtr | 90 min | Correct attribution of both |
| L8.7 | Firewall builder: host firewall + NAT gateway in iptables then nftables; prove with counters and tcpdump | 2 h | Test matrix of 8 flows all behave as specified |
| L8.8 | Long fat pipe: netem 80 ms delay, iperf3 before/after buffer tuning, cubic vs bbr | 75 min | Graph + BDP calculation |

## Company-tag matrix
| Topic | CSCO | QCOM | GOOG | MSFT | AMZN-NDE | JNPR | ANET | NOK | AVGO |
|---|---|---|---|---|---|---|---|---|---|
| Shell & text processing | ◐ | ◐ | ● | ◐ | ● | ◐ | ● | ◐ | ◐ |
| Bash scripting live | ◐ | ○ | ◐ | ◐ | ● | ◐ | ● | ◐ | ○ |
| `ip`/routing table/namespaces | ◐ | ◐ | ● | ● | ● | ● | ● | ● | ◐ |
| `ss`/TCP states | ◐ | ◐ | ● | ● | ● | ◐ | ● | ◐ | ◐ |
| tcpdump/Wireshark reading | ● | ● | ● | ◐ | ● | ● | ● | ● | ◐ |
| DNS with dig | ◐ | ○ | ● | ● | ● | ◐ | ◐ | ◐ | ○ |
| traceroute/mtr interpretation | ● | ○ | ● | ◐ | ● | ● | ● | ◐ | ○ |
| ethtool/NIC/offloads | ○ | ● | ◐ | ◐ | ◐ | ◐ | ● | ◐ | ● |
| iptables/nftables | ◐ | ○ | ◐ | ◐ | ● | ◐ | ◐ | ◐ | ○ |
| /proc, strace, lsof, systemd | ◐ | ◐ | ● | ◐ | ● | ◐ | ● | ◐ | ◐ |

(QCOM/AVGO weight toward driver/NIC/offload and embedded Linux; AMZN-NDE and ANET weight toward live Linux + scripting; GOOG toward "explain what happens" depth.)

## Interview question bank (30) — every question fully solved in the end-of-chapter pack
1. 🟢 How do you list all listening TCP and UDP ports and the owning process? (`ss -tulpn`; why `-n` matters.)
2. 🟢 Difference between `ip addr` and `ifconfig`; why was net-tools deprecated?
3. 🟢 How do you check disk usage and find the biggest directory? (`df -h`, `du -sh * | sort -h`.)
4. 🟢 What is in `/etc/resolv.conf`, `/etc/hosts`, `/etc/nsswitch.conf`, and in what order are they consulted?
5. 🟢 What does `ping` actually send, and what does "Destination Host Unreachable" from your own IP mean? (ARP failed on local segment.)
6. 🟢 Explain file permissions `754` and the meaning of the sticky bit on `/tmp`.
7. 🟡 Write a one-liner to print the top 10 IPs by request count from an access log. *(AMZN-NDE classic)*
8. 🟡 Write a Bash script that reads a file of hostnames and reports which are unreachable, exiting non-zero if any fail.
9. 🟡 `ip route get 1.1.1.1` — what does it tell you that `ip route show` doesn't?
10. 🟡 How does traceroute work? Why does Linux traceroute use UDP and Windows `tracert` use ICMP? How do you traceroute through a firewall that allows only 443?
11. 🟡 mtr shows 50 % loss at hop 3 but 0 % at the destination. Is there a problem? Explain.
12. 🟡 A server has thousands of sockets in TIME-WAIT. Is that a problem? Which side ends up in TIME-WAIT and why does it last 2×MSL?
13. 🟡 Many sockets in CLOSE-WAIT — what is the cause and whose fault is it?
14. 🟡 Write a tcpdump filter to capture only SYN packets (not SYN-ACK) to port 443.
15. 🟡 You see 64 KB TCP segments in tcpdump on a 1500-MTU link. Bug? (TSO/GSO/GRO.)
16. 🟡 Walk me through `dig +trace google.com` output.
17. 🟡 What is the difference between NXDOMAIN and SERVFAIL? What would you check for each?
18. 🟡 Explain iptables tables and chains. Which chain sees a packet routed through the box? Which sees a packet destined to the box?
19. 🟡 DROP vs REJECT — what does the client see in each case? Which is better for internal networks and why?
20. 🟡 How would you find which process is using port 8080 and kill it gracefully?
21. 🟡 What is in `/proc`? Name five files you'd look at for networking. *(Reported in Amazon SysDE loops.)*
22. 🟡 How do you make a sysctl change persistent? Give an example (`net.ipv4.ip_forward`).
23. 🔴 A Linux host can ping its gateway but not 8.8.8.8, and the gateway can ping 8.8.8.8. Walk through your diagnosis.
24. 🔴 Throughput between two DCs on a 10 Gb/s link with 100 ms RTT is only 50 Mb/s per flow. Diagnose (BDP, windows, loss, congestion control).
25. 🔴 Explain where tcpdump captures relative to netfilter on ingress and egress. Why might you see a packet in tcpdump that the application never receives?
26. 🔴 Design an nftables rule set for a bastion host; explain conntrack and why you allow ESTABLISHED,RELATED first.
27. 🔴 How do network namespaces work and how do containers (Docker) use veth + bridge + NAT to give connectivity?
28. 🔴 `strace` a `curl` that hangs; what syscalls would you expect to see, and how would you tell DNS hang from TCP connect hang?
29. 🔴 Explain the `ip neigh` states. What does FAILED vs INCOMPLETE indicate during troubleshooting?
30. 🔴 How would you implement policy-based routing on Linux so that traffic from 10.1.0.0/16 uses ISP-B while everything else uses ISP-A? (`ip rule`, separate table, `ip route add default via … table 100`.)

## Trap boxes
- **"netstat is the command"** — still works on many boxes but deprecated; say `ss` first and mention netstat as legacy.
- **"Loss in the middle of traceroute = broken router"** — only loss that persists to the final hop matters; intermediate hops de-prioritise ICMP generation.
- **"`* * *` means the router is down"** — it usually means it doesn't send ICMP Time Exceeded or a firewall drops it.
- **"tcpdump shows the packet, so the firewall allowed it"** — ingress capture happens before netfilter.
- **"TIME-WAIT is a leak"** — normal; CLOSE-WAIT is the suspicious one.
- **"REJECT is more secure than DROP"** — neither is "more secure"; DROP slows scanners, REJECT speeds legitimate failure. Context.
- **"Counters say 5,000 CRC errors, so the link is bad now"** — counters are cumulative since boot/clear; always take a delta.
- **"`ping` works so the service works"** — ICMP reachability ≠ TCP port reachability ≠ application health.
- **Quoting in Bash** — `rm -rf $DIR/` with empty `$DIR`. Always quote and use `set -u`.
- **"/etc/hosts doesn't matter, DNS is configured"** — hosts file usually wins per nsswitch order.

## Cheat-sheet contents (2-page spread, laminate-style)
- Page A "Is it the network?" grid: `ip -br a`, `ip r`, `ip route get`, `ip n`, `ss -tulpn`, `ss -ti`, `ping -M do -s 1472`, `tracepath`, `mtr -rwc 100`, `dig +short / +trace`, `curl -vw`, `nc -zv`, `ethtool / -S / -k`, `nstat -az`, `conntrack -L`, `iptables -L -n -v --line-numbers`, `nft list ruleset`, `journalctl -u`, `lsof -i`.
- Page B: tcpdump filter recipes (15), Wireshark display filters (15), TCP state meanings, DNS rcodes, ICMP type/code table (0, 3/0-3-4-13, 5, 8, 11), netfilter hook diagram thumbnail, legacy→modern Rosetta, BDP formula, awk/sed/grep top-10 idioms.

## End-of-chapter pack (Pillar 8)
- **Short notes (4 pp):** one box per §8.1–8.14; e.g. §8.6 box: "`ss -tulpn` = who listens; `ss -ti` = TCP health (rtt, cwnd, retrans); TIME-WAIT normal on active closer; CLOSE-WAIT = app forgot `close()`; SYN-RECV pile-up = SYN flood or full accept queue."
- **One-page revision sheet:** the "Is it the network?" command ladder (L1 `ethtool` → L2 `ip n` → L3 `ip r`/`ip route get`/`ping`/`tracepath` → L4 `ss`/`nc` → DNS `dig` → L7 `curl -w`), 10 tcpdump filters, TCP-state traffic-light table, ICMP type table, netfilter hook thumbnail, BDP formula. Rest of the cheat-sheet content above moves to the command appendix.
- **Flashcards (40):** samples — "Front: `ip neigh` shows FAILED for the gateway. Back: ARP got no reply → L2 problem (VLAN, cable, gateway down, wrong subnet)." · "Front: Which netfilter chain sees forwarded traffic? Back: FORWARD (after PREROUTING, before POSTROUTING)." · "Front: tcpdump filter for pure SYN (not SYN-ACK)? Back: `'tcp[tcpflags] & (tcp-syn|tcp-ack) == tcp-syn'`." · "Front: mtr loss at a middle hop only? Back: ICMP rate-limiting/CoPP; ignore unless it persists to the destination."
- **Solved interview problems:** all 30 questions above, per answer standard C; scripting questions (Q7, Q8, Q30) include runnable code with sample input/output; Q23/Q24 solved as full layer-by-layer walk-throughs cross-referenced to Pillar 11 cases.
- **Self-test:** 10 MCQs (e.g. "Which shows the source IP the kernel would use? a) `ip a` b) `ip route get` c) `ss -s` d) `arp -n`") + 2 short answers (decode a printed tcpdump snippet; write an awk one-liner).

## Mini-project (OPTIONAL; flagship candidate): `netdoctor` — a one-command Linux connectivity diagnoser
- Bash front-end + Python core. Given a target (`netdoctor example.com:443`), it runs in order: interface & address check → default route & `ip route get` → gateway ARP/ping → DNS (resolver, answer, TTL, latency) → TCP connect timing → TLS handshake (via `openssl s_client`) → HTTP status; prints a coloured layer-by-layer verdict (PASS/WARN/FAIL with evidence) and saves a JSON report.
- Stretch: `--capture` flag that runs tcpdump in parallel and attaches a pcap; `--mtu` flag that binary-searches path MTU with DF pings.
- Deliverables: GitHub repo with README, demo GIF, three recorded "fault injection" runs (wrong DNS, blocked port, MTU 1400 path). Directly reusable as a résumé project for Pillar 12G.

## Sources (author verification sources — not required reading)
- iproute2 man pages: https://man7.org/linux/man-pages/man8/ip.8.html ; https://man7.org/linux/man-pages/man8/ss.8.html
- tcpdump & pcap-filter: https://www.tcpdump.org/manpages/tcpdump.1.html ; https://www.tcpdump.org/manpages/pcap-filter.7.html
- Wireshark User's Guide & display filter reference: https://www.wireshark.org/docs/wsug_html_chunked/ ; https://www.wireshark.org/docs/dfref/
- nftables wiki: https://wiki.nftables.org/
- Netfilter packet flow: https://wiki.nftables.org/wiki-nftables/index.php/Netfilter_hooks
- ethtool man page: https://man7.org/linux/man-pages/man8/ethtool.8.html
- mtr: https://github.com/traviscross/mtr
- iperf3: https://software.es.net/iperf/
- containerlab: https://containerlab.dev/
- Amazon NDE/SysDE/AWS candidate reports (anecdotal): https://static-pc.glassdoor.de/Interview/Amazon-Interview-E6036-RVW45180501.htm ; https://www.glassdoor.ca/Interview/Amazon-Web-Services-Interview-E7470741-RVW91508348.htm ; https://static.glassdoor.at/Interview/Amazon-System-Development-Engineer-Interview-Questions-EI_IE6036.0,6_KO7,34_IP5.htm ; https://dataford.io/interview-guides/amazon/systems-engineer
- Arista/Juniper Linux + Python interview reports: https://www.interviewquery.com/guides/arista-networks-software-engineer ; https://www.geeksforgeeks.org/juniper-networks-interview-experience-3/ ; https://dataford.io/interview-guides/arista/networks-software-engineer

---

# PILLAR 9 — Network Security

**Chapter title:** *Locks, Keys and Liars: Securing the Network Layer by Layer*
**One-line promise:** You will be able to explain every major network attack from L2 to L7, the control that stops it, and walk an interviewer packet-by-packet through TLS 1.3 and IPsec IKEv2.

- **Prerequisites:** Pillar 3 (TCP/IP, ARP, DNS, DHCP), Pillar 4 (VLANs, STP, ACL placement basics, routing), Pillar 8 (tcpdump, iptables). Basic modular arithmetic helpful but not required — the crypto section is conceptual.
- **Estimated pages:** 100 (teaching 68 + end-of-chapter pack 32, of which solved questions ≈ 25)
- **Study days:** 4.5 (Week 5 of 8). MUST-only path: 3.45 days.

## Learning objectives
1. State the CIA triad plus authentication, authorisation, accounting (AAA) and non-repudiation, and map threats (STRIDE) to them.
2. Explain symmetric vs asymmetric cryptography, hashing, MACs/HMAC, digital signatures, Diffie–Hellman (incl. ECDHE) and forward secrecy at a conceptual, interview-ready level.
3. Describe PKI: X.509 certificates, chain of trust, root/intermediate CAs, CSR, revocation (CRL, OCSP, OCSP stapling), certificate pinning, and Certificate Transparency.
4. Walk through the TLS 1.3 handshake message by message (1-RTT, 0-RTT, resumption with PSK) and contrast with TLS 1.2 (2-RTT, RSA key transport removed in 1.3).
5. Configure and reason about stateless ACLs (standard/extended, wildcard masks, implicit deny, placement rules) and stateful firewalls (zones, sessions, NAT interplay, asymmetric-routing pitfalls), plus next-generation firewall features.
6. Explain IPsec (AH vs ESP, transport vs tunnel, SA/SPI, IKEv1 main/aggressive/quick mode vs IKEv2 IKE_SA_INIT/IKE_AUTH/CREATE_CHILD_SA, NAT-T on UDP 4500) and compare site-to-site, remote-access, SSL/TLS VPN and WireGuard.
7. Explain and mitigate L2 attacks: ARP spoofing (DAI + DHCP snooping), MAC flooding (port security), DHCP starvation/rogue DHCP (DHCP snooping), VLAN hopping via switch spoofing (disable DTP) and double tagging (unused native VLAN), STP manipulation (BPDU Guard, Root Guard).
8. Explain and mitigate L3/L4 attacks: IP spoofing (uRPF, BCP 38), SYN flood (SYN cookies, backlog), UDP/ICMP floods, amplification/reflection (DNS, NTP, memcached), BGP hijacking (RPKI, prefix filters), and volumetric vs protocol vs application-layer DDoS.
9. Explain DNS attacks (cache poisoning incl. Kaminsky-style, spoofing, tunnelling, amplification) and defences (source-port randomisation, 0x20, DNSSEC, DoT/DoH).
10. Describe AAA (RADIUS vs TACACS+), 802.1X/EAP, NAC; IDS vs IPS (signature vs anomaly); SIEM basics; and device hardening (SSH v2 only, disable telnet/HTTP, CoPP, management plane protection, logging/NTP).
11. Explain zero-trust architecture (NIST SP 800-207: policy engine/administrator/enforcement point; "never trust, always verify"; micro-segmentation; identity-aware proxies e.g. Google BeyondCorp) and contrast with perimeter security.

## Priority tags & indicative study days
| § | Section | Tag | Days | Core lab |
|---|---|---|---|---|
| 9.1 | Security mindset | SHOULD | 0.15 | — |
| 9.2 | Cryptography essentials | MUST | 0.40 | — |
| 9.3 | PKI & certificates | MUST | 0.30 | L9.1 (paper variant acceptable) |
| 9.4 | TLS 1.3 handshake | MUST | 0.50 | L9.2 (paper variant: printed decrypted capture) |
| 9.5 | ACLs | MUST | 0.40 | L9.3 |
| 9.6 | Stateful firewall / NAT | MUST | 0.35 | — |
| 9.7 | IPsec & IKE | MUST | 0.50 | L9.4 (paper variant: printed `show crypto` outputs) |
| 9.8 | VPN families | SHOULD | 0.20 | — |
| 9.9 | L2 attacks & hardening | MUST (CSCO, JNPR, NOK) | 0.40 | L9.6 paper variant |
| 9.10 | L3/L4 attacks & DDoS | MUST | 0.35 | L9.7 |
| 9.11 | DNS security | SHOULD (MUST for GOOG, MSFT, AMZN) | 0.25 | — |
| 9.12 | AAA / 802.1X | SHOULD (MUST for CSCO) | 0.20 | — |
| 9.13 | IDS/IPS & hardening | OPTIONAL | 0.10 | — |
| 9.14 | Zero trust | SHOULD | 0.15 | — |
| — | End-of-chapter pack | MUST | 0.25 | — |
| | **Total (full coverage)** | | **4.50** | MUST-only path = 3.45 |

L9.5, L9.8, the hands-on half of L9.6 and the mini-project are tagged OPTIONAL (fully specified in the book).

## Section-by-section outline

### 9.1 Security mindset: CIA, AAA, STRIDE, defence in depth
- **Core idea:** Security is risk management; threats are classified (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege); defence in depth stacks independent controls.
- **Analogy:** A bank branch in Pune — guard at the door (firewall), CCTV (IDS), locker keys (encryption), visitor register (logging), two-person rule for the vault (authorisation).
- **Worked example:** Threat-model a college Wi-Fi + lab network: list assets, entry points, one threat per STRIDE letter, and one control each.
- **Figures:** *Fig 9.1* — Concentric "onion" diagram (physical → perimeter → network segment → host → application → data) with control examples on each ring. *Fig 9.2* — STRIDE × CIA/AAA mapping table.

### 9.2 Cryptography you must be able to explain
- **Core idea:** Symmetric (AES-GCM, ChaCha20-Poly1305) for bulk; asymmetric (RSA, ECC) for key exchange/signatures; hashes (SHA-256) for integrity; HMAC for authenticity; AEAD combines confidentiality + integrity; DH/ECDHE for shared secret over public channel; ephemeral keys → forward secrecy.
- **Analogy:** DH as the "paint-mixing" analogy reskinned with *rangoli colours*: both mix a public base colour with a secret colour, swap, then add their own secret again → same final colour that an eavesdropper cannot un-mix.
- **Worked example:** Toy DH with p = 23, g = 5, a = 6, b = 15 → A = 8, B = 19, shared = 2. Then show why a 2048-bit p or curve25519 makes this infeasible to reverse.
- **Figures:** *Fig 9.3* — Paint-mixing DH diagram. *Fig 9.4* — Signature vs encryption with public/private key direction arrows (encrypt to public key; sign with private key). *Fig 9.5* — Comparison table: primitive / purpose / example / what breaks if misused.

### 9.3 PKI and certificates
- **Core idea:** A certificate binds a public key to an identity, signed by a CA; browsers/OSes ship root stores; servers send leaf + intermediates; validation checks signature chain, validity dates, name (SAN), key usage, revocation. Let's Encrypt/ACME automation; mutual TLS for service-to-service and device identity.
- **Analogy:** Aadhaar-style identity: UIDAI (root CA) authorises enrolment agencies (intermediate CAs) that issue cards (leaf certs); a verifier checks the hologram chain, not your face alone.
- **Worked example:** `openssl s_client -connect www.google.com:443 -showcerts` annotated: chain depth, issuer/subject, SAN list, expiry; then a broken chain (missing intermediate) and how it fails on some clients but not browsers that cache intermediates.
- **Figures:** *Fig 9.6* — Chain-of-trust ladder (Root CA self-signed → Intermediate → Leaf) with signature arrows. *Fig 9.7* — Anatomy of an X.509 certificate (fields as a labelled card).

### 9.4 TLS 1.3 handshake, step by step
- **Core idea:** 1-RTT: ClientHello (supported_versions, cipher_suites, key_share with ECDHE public value, signature_algorithms, SNI, ALPN) → ServerHello (chosen suite + key_share) → from here encrypted: EncryptedExtensions, Certificate, CertificateVerify, Finished → client Finished → application data. HelloRetryRequest when key_share guess wrong. PSK resumption; 0-RTT early data and its replay risk. TLS 1.2 contrast: 2-RTT, static RSA key exchange (no forward secrecy) removed in 1.3, renegotiation removed, cipher suite list slimmed to 5 AEAD suites.
- **Analogy:** Booking a sealed conversation at a hotel: in 1.3 you bring your half of the room key in your first sentence, so the receptionist can lock the door immediately.
- **Worked example:** Decrypted Wireshark capture (via SSLKEYLOGFILE) of `curl https://example.com` with each record numbered and mapped to the RFC 8446 message.
- **Figures:** *Fig 9.8* — Ladder diagram TLS 1.3 full handshake, colour-shaded where encryption begins (handshake traffic keys vs application traffic keys). *Fig 9.9* — Side-by-side TLS 1.2 vs 1.3 ladders with RTT count. *Fig 9.10* — 0-RTT flow with replay-attack callout.

### 9.5 ACLs: stateless packet filtering on routers and switches
- **Core idea:** Standard ACL (source only, place near destination) vs extended (src/dst/protocol/port, place near source); numbered/named; wildcard masks (inverse of subnet mask, 0 = must match); top-down first match; implicit `deny any`; inbound vs outbound on interface; one ACL per interface/direction/protocol; ACLs on VTY lines; object-groups; IPv6 ACL implicit permits for ND.
- **Analogy:** Bouncer with a printed list at the door — checks names top to bottom; if not on the list, you are out (implicit deny).
- **Worked example:** "Allow the 10.1.10.0/24 student VLAN HTTP/HTTPS to the web server 10.1.50.10, allow ICMP echo, deny everything else to the server VLAN, allow all else." Write the extended ACL, choose interface + direction, and compute wildcard for 10.1.8.0/22 (0.0.3.255).
- **Figures:** *Fig 9.11* — Topology with router, three VLANs, arrows showing ACL placement in/out and the traffic it affects. *Fig 9.12* — Wildcard-mask binary worked grid.

### 9.6 Stateful firewalls, NGFW, NAT interplay
- **Core idea:** Session table (5-tuple + state), return traffic auto-permitted; zones and security levels; inspection; NGFW = application identification (App-ID), user identity, IPS, URL filtering, TLS inspection; order of NAT vs policy evaluation (vendor-specific); asymmetric routing breaks stateful inspection; high availability (active/standby state sync).
- **Analogy:** A housing-society guard who remembers that *you* invited the Swiggy rider, so lets him back out without re-checking (stateful), versus one who checks the list both ways (stateless).
- **Worked example:** Packet walk through an edge firewall doing source NAT for 192.168.1.0/24 to 203.0.113.5: outbound SYN creates session; inbound SYN-ACK matches session; an unsolicited inbound SYN dropped; then show how asymmetric return via second ISP is dropped as "no session".
- **Figures:** *Fig 9.13* — Session table snapshot with columns. *Fig 9.14* — Asymmetric routing diagram with two firewalls and the dropped return path in red.

### 9.7 IPsec and IKE
- **Core idea:** ESP (IP protocol 50; confidentiality + integrity) vs AH (51; integrity only, breaks with NAT); transport vs tunnel mode; Security Association, SPI, SAD/SPD; IKE on UDP 500, NAT-T on UDP 4500. IKEv1: Phase 1 main mode (6 messages) or aggressive mode (3, leaks identity), Phase 2 quick mode (3). IKEv2: IKE_SA_INIT (2 messages: crypto proposals, DH, nonces) + IKE_AUTH (2 messages: identities, auth, first CHILD_SA) = 4 messages; CREATE_CHILD_SA for rekeys/extra SAs; built-in DPD/liveness, EAP support. Proposal matching: encryption, integrity/PRF, DH group, lifetime; traffic selectors / proxy-IDs / crypto ACL must mirror; PFS. Route-based (VTI) vs policy-based VPN.
- **Analogy:** Phase 1 is two embassies agreeing on a secure diplomatic pouch; Phase 2 is the individual sealed letters (one pouch per pair of departments) sent using that agreement.
- **Worked example:** Site-to-site VPN Bengaluru HQ (10.10.0.0/16) ↔ Hyderabad branch (10.20.0.0/16) over the internet: full IKEv2 config on IOS XE (proposal, policy, keyring, profile, IPsec profile, tunnel interface), then `show crypto ikev2 sa`, `show crypto ipsec sa` reading encaps/decaps counters; a mismatch case (branch selector 10.20.1.0/24) showing phase 1 up, phase 2 failing (TS_UNACCEPTABLE).
- **Figures:** *Fig 9.15* — Packet format comparison: original IP packet; ESP transport; ESP tunnel; ESP with NAT-T UDP header (field widths drawn proportionally). *Fig 9.16* — IKEv2 4-message ladder with payloads labelled (SA, KE, Ni/Nr, IDi/IDr, AUTH, SAi2/SAr2, TSi/TSr). *Fig 9.17* — IKEv1 main+quick vs IKEv2 message-count comparison.

### 9.8 VPN families and remote access
- **Core idea:** Site-to-site IPsec; DMVPN/GETVPN (name-check only); remote-access IPsec vs SSL/TLS VPN (AnyConnect/Cisco Secure Client); WireGuard (Noise protocol, UDP, simple key model); split tunnelling trade-offs; MTU/MSS implications of encapsulation overhead (links to Pillar 11 case).
- **Analogy:** Private tunnel through a public highway — the tunnel walls are encryption, the toll is overhead bytes.
- **Worked example:** Compute ESP tunnel overhead for AES-GCM over a 1500-byte link (new IP 20 + ESP header 8 + IV 8 + padding/trailer 2–17 + ICV 16 ≈ 54–70 bytes; with NAT-T +8) → why `ip tcp adjust-mss 1360` is common.
- **Figures:** *Fig 9.18* — Comparison matrix (IPsec S2S, RA IPsec, SSL VPN, WireGuard: layer, transport, NAT traversal, client, typical use). *Fig 9.19* — Overhead stack bar showing bytes consumed.

### 9.9 Layer-2 attacks and switch hardening
- **Core idea:** ARP spoofing/poisoning (gratuitous ARP lie → MITM) → DHCP snooping binding table + Dynamic ARP Inspection; MAC flooding (CAM exhaustion → switch floods like a hub) → port security max MAC/sticky/violation modes; rogue DHCP & starvation → DHCP snooping trusted ports + rate limit; VLAN hopping via (a) switch spoofing — attacker negotiates trunk with DTP → `switchport mode access`, `switchport nonegotiate`; (b) double tagging — outer tag = native VLAN stripped at first switch, inner tag delivered one-way into victim VLAN → change native VLAN to an unused one / tag native VLAN; STP attacks → BPDU Guard on access ports, Root Guard on distribution; IP source guard; 802.1X port authentication; private VLANs.
- **Analogy:** ARP spoofing is someone at a wedding shouting "I am the caterer!" and receiving every dish.
- **Worked example:** Lab: attacker runs `arpspoof`/`ettercap` against a victim and gateway; show victim ARP table before/after, Wireshark duplicate-IP warning; enable DHCP snooping + DAI on the switch; show `%SW_DAI-4-DHCP_SNOOPING_DENY` log and attack failure.
- **Figures:** *Fig 9.20* — ARP-spoofing MITM triangle (victim, gateway, attacker) with ARP tables before/after. *Fig 9.21* — Double-tagging frame diagram: 802.1Q outer tag (VLAN 1 native) + inner tag (VLAN 20) → first switch strips outer → second switch reads inner. *Fig 9.22* — Attack → mitigation → command table.

### 9.10 Layer-3/4 attacks and DDoS
- **Core idea:** IP spoofing → ingress filtering BCP 38, uRPF strict/loose; SYN flood exhausts half-open backlog → SYN cookies (encode state in ISN), backlog increase, SYN proxies; ICMP/UDP floods; smurf (historic); amplification (DNS ~50×, NTP monlist ~500×, memcached up to ~50,000×) via spoofed source; application-layer (HTTP floods, Slowloris); BGP hijack & route leaks → RPKI ROV, IRR filters, max-prefix; DDoS mitigation stack: anycast scrubbing, RTBH, Flowspec, rate limiting, CDN/WAF, autoscaling.
- **Analogy:** SYN flood is a prankster booking every table at a restaurant by phone and never arriving.
- **Worked example:** `hping3 -S --flood` against a lab VM; watch `ss -s` / `netstat -s | grep -i listen` overflow and SYN-RECV explosion; enable `net.ipv4.tcp_syncookies=1`; show legit `curl` succeeding again; explain how a SYN cookie ISN is constructed (timestamp, MSS index, hash of 4-tuple + secret).
- **Figures:** *Fig 9.23* — SYN flood ladder showing backlog slots filling. *Fig 9.24* — Amplification diagram (attacker spoofs victim IP → open resolvers → huge replies to victim), with amplification factors as bar chart. *Fig 9.25* — DDoS defence layers diagram (edge, ISP, scrubbing centre, CDN, origin).

### 9.11 DNS security
- **Core idea:** Cache poisoning: attacker races forged responses matching TXID (16-bit) + port; Kaminsky 2008 made it practical with random subdomains; defences: source-port randomisation (~32 bits combined), 0x20 case randomisation, DNSSEC (RRSIG, DNSKEY, DS chain, AD bit), DoT (853) / DoH (443) for privacy (not integrity of the data origin); DNS tunnelling detection; open-resolver abuse.
- **Analogy:** Poisoning is slipping a fake entry into the society phone directory before the real one arrives.
- **Worked example:** Probability calc: one guess vs 65,536 TXIDs vs 65,536 × ~60,000 ports; `dig +dnssec cloudflare.com` showing RRSIG and `ad` flag.
- **Figures:** *Fig 9.26* — Race-condition timeline (resolver query, attacker flood, real answer arriving too late). *Fig 9.27* — DNSSEC chain of trust (root KSK → .com DS → example.com DNSKEY → RRSIG over A).

### 9.12 Identity and access: AAA, RADIUS, TACACS+, 802.1X, NAC
- **Core idea:** RADIUS (UDP 1812/1813, combines authN+authZ, encrypts only password) vs TACACS+ (TCP 49, separates AAA, encrypts whole body, per-command authorisation — preferred for device admin); 802.1X roles (supplicant, authenticator, authentication server), EAP methods (EAP-TLS, PEAP); MAB fallback; dynamic VLAN assignment; Cisco ISE as example NAC.
- **Analogy:** 802.1X is the college gate: student (supplicant) shows ID to the guard (switch), who phones the admin office (RADIUS) before opening.
- **Worked example:** 802.1X flow on a switch port with EAPOL-Start → identity → RADIUS Access-Request/Challenge/Accept with VLAN attribute → port authorised.
- **Figures:** *Fig 9.28* — Three-party 802.1X ladder. *Fig 9.29* — RADIUS vs TACACS+ comparison table.

### 9.13 Detection and device hardening
- **Core idea:** IDS (passive, SPAN/TAP) vs IPS (inline); signature vs anomaly; false positive/negative trade-off; Snort/Suricata/Zeek; NetFlow/IPFIX for detection; SIEM correlation; device hardening checklist (SSH v2, strong local fallback account, `service password-encryption` is weak — use `secret` type 8/9, disable unused services, CDP/LLDP on edge off, CoPP, logging to syslog, NTP authentication, SNMPv3 authPriv, banner, management VRF).
- **Analogy:** IDS is CCTV that alerts; IPS is the guard who physically blocks.
- **Worked example:** Hardening diff: insecure IOS config → hardened config with a line-by-line rationale table.
- **Figures:** *Fig 9.30* — IDS (SPAN) vs IPS (inline) placement diagram. *Fig 9.31* — Hardening checklist infographic grouped by management/control/data plane.

### 9.14 Zero trust and modern architectures
- **Core idea:** NIST SP 800-207 components: Policy Engine, Policy Administrator, Policy Enforcement Point; per-request decisions based on identity, device posture, context; micro-segmentation; identity-aware proxies (BeyondCorp); SASE/SSE name-check; mTLS service mesh in DCs; contrast with castle-and-moat VPN.
- **Analogy:** Instead of one gate to the IT park, every office door has a badge reader that checks who you are *and* whether your laptop is patched — every time.
- **Worked example:** Re-architect "contractor needs access to one internal wiki" from full VPN to an identity-aware proxy with device posture check; list the policy decision inputs.
- **Figures:** *Fig 9.32* — NIST 800-207 logical components diagram (subject → PEP ↔ PDP (PE+PA) with feeds: CDM, threat intel, ID management, logs). *Fig 9.33* — Perimeter vs zero-trust side-by-side.

## Hands-on labs
| Lab | Title | Time | Success criterion |
|---|---|---|---|
| L9.1 | OpenSSL playground: generate CA, intermediate, leaf; run `openssl s_server`/`s_client` with mTLS; break chain deliberately | 2 h | Valid chain verifies; broken one fails with the right error |
| L9.2 | TLS 1.3 decryption in Wireshark via SSLKEYLOGFILE; label every handshake message | 75 min | Annotated capture |
| L9.3 | ACL builder on Cisco CML/Packet Tracer or containerlab cEOS: implement the 9.5 policy, test 8 flows | 90 min | Test matrix passes; `show access-lists` hit counts match |
| L9.4 | Site-to-site IKEv2 VPN: two FRR/strongSwan Linux routers (or IOS XE sandbox); then planted proxy-ID mismatch | 2.5 h | Tunnel up, encaps/decaps increment; mismatch diagnosed from logs |
| L9.5 | WireGuard in 15 minutes between two namespaces; compare overhead with tcpdump | 60 min | Ping and measured MTU |
| L9.6 | L2 attack range (isolated lab only): ARP spoof, MAC flood (macof), DHCP rogue; then DAI, port security, snooping | 2.5 h | Each attack shown working then blocked |
| L9.7 | SYN flood vs SYN cookies on lab VMs | 60 min | Before/after `ss -s` and curl latency |
| L9.8 | DNSSEC & DoH: validate with `dig +dnssec`, observe DoH with Wireshark | 45 min | Explain AD bit and why DoH is opaque |

Ethics box (mandatory, on the first page of labs): only attack lab networks you own; Indian IT Act 2000 s.43/66 exposure for unauthorised access; never run L9.6/L9.7 on college Wi-Fi.

## Company-tag matrix
| Topic | CSCO | QCOM | GOOG | MSFT | AMZN-NDE | JNPR | ANET | NOK | AVGO |
|---|---|---|---|---|---|---|---|---|---|
| Crypto basics / PKI | ◐ | ● | ● | ● | ◐ | ◐ | ○ | ◐ | ◐ |
| TLS 1.3 handshake | ◐ | ◐ | ● | ● | ● | ◐ | ◐ | ◐ | ○ |
| ACLs & wildcard masks | ● | ○ | ◐ | ◐ | ● | ● | ◐ | ◐ | ○ |
| Stateful firewall / NAT | ● | ○ | ◐ | ◐ | ● | ● | ◐ | ● | ○ |
| IPsec/IKE | ● | ◐ | ◐ | ◐ | ◐ | ● | ◐ | ● | ◐ |
| L2 attacks & switch hardening | ● | ○ | ○ | ○ | ◐ | ◐ | ◐ | ◐ | ○ |
| SYN flood / DDoS | ◐ | ○ | ● | ● | ● | ◐ | ◐ | ◐ | ○ |
| DNS security | ◐ | ○ | ● | ● | ● | ○ | ○ | ○ | ○ |
| AAA / 802.1X | ● | ◐ (Wi-Fi) | ○ | ◐ | ○ | ◐ | ○ | ◐ | ○ |
| Zero trust | ◐ | ○ | ● | ● | ◐ | ◐ | ○ | ◐ | ○ |
| Wireless security (WPA3) — cross-ref Pillar 6 | ◐ | ● | ○ | ○ | ○ | ○ | ○ | ◐ | ◐ |

## Interview question bank (32) — every question fully solved in the end-of-chapter pack
1. 🟢 What is the CIA triad? Give a network example of a breach of each.
2. 🟢 Symmetric vs asymmetric encryption — why does TLS use both?
3. 🟢 What is a hash? Why is a hash alone not enough to authenticate a message? (HMAC.)
4. 🟢 What is a digital certificate and who signs it?
5. 🟢 What is the implicit rule at the end of every ACL? Where do you place standard vs extended ACLs?
6. 🟢 Compute the wildcard mask for 172.16.32.0/20. (0.0.15.255.)
7. 🟢 Stateless vs stateful firewall.
8. 🟢 IDS vs IPS.
9. 🟡 Walk me through the TLS 1.3 handshake. Where does encryption start? *(GOOG/MSFT/AMZN favourite)*
10. 🟡 Why is TLS 1.3 one round trip instead of two? What was removed from 1.2 and why?
11. 🟡 What is forward secrecy and how does ECDHE provide it?
12. 🟡 What is 0-RTT and why is it dangerous for non-idempotent requests?
13. 🟡 How does a browser validate a certificate? What happens if the intermediate is missing?
14. 🟡 Explain IPsec tunnel vs transport mode, AH vs ESP. Why doesn't AH work through NAT?
15. 🟡 Explain IKEv1 Phase 1 and Phase 2. How does IKEv2 differ? How many messages each?
16. 🟡 A site-to-site VPN shows phase 1 up but no traffic passes. What do you check? (Proxy-ID/crypto ACL, transform set, PFS group, routing, NAT exemption.)
17. 🟡 What is NAT-T and which ports does IPsec use?
18. 🟡 Explain ARP spoofing and how DAI stops it. What does DAI depend on?
19. 🟡 What is VLAN hopping? Explain both methods and their mitigations.
20. 🟡 What is a SYN flood? How do SYN cookies work?
21. 🟡 What is DNS cache poisoning? Why did source-port randomisation help so much?
22. 🟡 RADIUS vs TACACS+ — which for device administration and why?
23. 🟡 Explain the 802.1X roles and message flow.
24. 🟡 What is uRPF? Strict vs loose mode and where loose is required (multihoming).
25. 🔴 An amplification DDoS of 400 Gb/s is hitting your customer's IP. Walk through mitigation from the first minute to steady state (RTBH, Flowspec, scrubbing, anycast, upstream coordination).
26. 🔴 How does DNSSEC establish trust? What does it *not* protect against? How is DoH different?
27. 🔴 A stateful firewall pair in active/active drops 30 % of return traffic. Diagnose. (Asymmetric routing / session sync.)
28. 🔴 Design network security for a new 2,000-student campus (segmentation, NAC, guest Wi-Fi, ACLs, logging, edge firewall).
29. 🔴 Explain BGP hijacking and how RPKI route-origin validation mitigates it. Limits of ROV?
30. 🔴 What is zero trust? How would you migrate a VPN-based company to it? Map to NIST 800-207 components.
31. 🔴 TLS inspection on an NGFW: how does it work, what breaks (pinning, mTLS), and what are the privacy/legal considerations?
32. 🔴 Compare IPsec, WireGuard and TLS VPNs for 10,000 remote employees — performance, NAT traversal, management.

## Trap boxes
- **"Encrypt with private key = signature"** — conceptually only for textbook RSA; modern signature schemes (ECDSA, EdDSA) are not "encryption with the private key". Say "sign with private key, verify with public key".
- **"HTTPS hides which site I visit"** — SNI is plaintext unless ECH is used; DNS may leak too.
- **"TLS 1.3 = no handshake overhead"** — still 1 RTT (plus TCP's 1 RTT); 0-RTT has replay caveats.
- **"Wildcard mask = subnet mask"** — it's the inverse; and wildcard masks can be discontiguous.
- **"AH is more secure than ESP"** — AH gives no confidentiality and breaks with NAT; ESP with integrity is the norm.
- **"Phase 1 up means VPN is fine"** — phase 2 / CHILD_SA and counters must be checked.
- **"VLANs are a security boundary on their own"** — only with hardened trunks, native VLAN hygiene and L3 filtering.
- **"Firewall blocks DDoS"** — a stateful firewall's session table is itself a DDoS target; volumetric attacks must be stopped upstream.
- **"DoH = DNSSEC"** — DoH secures the transport hop; DNSSEC authenticates the data origin.
- **"`service password-encryption` secures passwords"** — type 7 is reversible.

## Cheat-sheet contents
- Port/protocol table: SSH 22, Telnet 23, DNS 53, HTTPS 443, IKE UDP 500, NAT-T UDP 4500, ESP proto 50, AH proto 51, RADIUS 1812/1813, TACACS+ TCP 49, DoT 853, Syslog 514, SNMP 161/162, NTP 123, LDAP(S) 389/636, Kerberos 88.
- TLS 1.3 ladder thumbnail + TLS 1.2 diff list.
- IKEv1 vs IKEv2 message-count table; IPsec mismatch checklist (encryption, hash, DH group, auth, lifetime, PSK, proxy-ID, PFS, NAT exemption).
- Attack → mitigation → IOS/NX-OS command grid (ARP spoof → `ip arp inspection vlan`, rogue DHCP → `ip dhcp snooping`, MAC flood → `switchport port-security maximum`, VLAN hop → `switchport nonegotiate` + native VLAN change, STP → `spanning-tree bpduguard enable`, spoofing → `ip verify unicast source reachable-via rx`).
- ACL placement rules and wildcard quick table (/8–/30).
- DDoS taxonomy: volumetric / protocol / application with example + defence.
- Zero-trust principles in 7 bullets (from NIST 800-207 tenets).

## End-of-chapter pack (Pillar 9)
- **Short notes (4 pp):** one box per §9.1–9.14; e.g. §9.7 box: "ESP = proto 50 (encrypts + authenticates), AH = 51 (no encryption, NAT-hostile). IKE UDP 500, NAT-T UDP 4500. IKEv1 = 6 (main) or 3 (aggressive) + 3 (quick); IKEv2 = 4 (IKE_SA_INIT ×2 + IKE_AUTH ×2). Phase 1 up / phase 2 down → proxy-IDs, transform set, PFS."
- **One-page revision sheet:** TLS 1.3 ladder, IKEv2 ladder, port/protocol table, attack→mitigation→command grid, ACL placement rules + wildcard table, DDoS taxonomy, 7 zero-trust tenets.
- **Flashcards (40):** samples — "Front: Two VLAN-hopping methods? Back: switch spoofing (DTP trunk) → `switchport mode access` + `nonegotiate`; double tagging (native VLAN) → unused/tagged native VLAN." · "Front: What does DAI rely on? Back: DHCP-snooping binding table (or static ARP ACLs)." · "Front: Where does TLS 1.3 encryption start? Back: Immediately after ServerHello (EncryptedExtensions onward)." · "Front: SYN cookie encodes what in the ISN? Back: time counter, MSS index, keyed hash of 4-tuple."
- **Solved interview problems:** all 32 questions per answer standard C; Q25, Q28, Q30, Q32 solved as structured design answers with diagrams; Q16 cross-referenced to Pillar 11 Case 15.
- **Self-test:** 10 MCQs + compute a wildcard mask + label a blank TLS 1.3 ladder.

## Mini-project (OPTIONAL): "Campus Shield" — secure-by-design lab network with an attack-and-defend report
- Build in containerlab/GNS3: edge firewall (nftables or pfSense/OPNsense VM), core L3 switch, three VLANs (staff, students, servers), RADIUS server (FreeRADIUS) for SSH device admin, strongSwan site-to-site VPN to a "branch".
- Phase A: implement policy (ACLs/firewall rules, DHCP snooping/DAI where the platform supports it, SSH-only management, syslog to a Linux collector).
- Phase B: run four attacks from a Kali container (ARP spoof, port scan, SYN flood, rogue DHCP) and document detection (Suricata alert or logs) and mitigation.
- Deliverables: topology diagram, policy matrix, config repo, 6-page "pentest-style" report with before/after evidence. Great résumé and project-deep-dive material.

## Sources (author verification sources — not required reading)
- RFC 8446 TLS 1.3: https://datatracker.ietf.org/doc/html/rfc8446
- RFC 7296 IKEv2: https://datatracker.ietf.org/doc/html/rfc7296
- RFC 4303 ESP: https://datatracker.ietf.org/doc/html/rfc4303 ; RFC 3948 NAT-T: https://datatracker.ietf.org/doc/html/rfc3948
- RFC 4987 TCP SYN flooding attacks and mitigations: https://datatracker.ietf.org/doc/html/rfc4987
- BCP 38 / RFC 2827 ingress filtering: https://datatracker.ietf.org/doc/html/rfc2827
- RFC 4033 DNSSEC intro: https://datatracker.ietf.org/doc/html/rfc4033 ; RFC 8484 DoH: https://datatracker.ietf.org/doc/html/rfc8484
- RFC 6811 BGP prefix origin validation (RPKI): https://datatracker.ietf.org/doc/html/rfc6811
- NIST SP 800-207 Zero Trust Architecture: https://csrc.nist.gov/pubs/sp/800/207/final
- Google BeyondCorp papers: https://research.google/pubs/beyondcorp-a-new-approach-to-enterprise-security/
- CISA DDoS guidance / amplification factors: https://www.cisa.gov/news-events/alerts/2014/01/17/udp-based-amplification-attacks
- Cisco Catalyst DHCP snooping/DAI configuration guides: https://www.cisco.com/c/en/us/support/switches/catalyst-9300-series-switches/products-installation-and-configuration-guides-list.html
- WireGuard whitepaper: https://www.wireguard.com/papers/wireguard.pdf
- Cisco/NCE interview reports listing ACL/VPN/security topics (anecdotal): https://www.glassdoor.co.uk/Interview/Cisco-Interview-E1425-RVW56475813.htm
- Indian IT Act 2000 (ethics box): https://www.indiacode.nic.in/handle/123456789/1999

---

# PILLAR 10 — Network Automation & Programmability

**Chapter title:** *Teach the Network to Configure Itself: From SSH Scripts to Model-Driven Telemetry*
**One-line promise:** You will move from typing CLI on one router to safely pushing, validating and rolling back configuration on fifty devices from Git, and you will be able to defend every design choice in an interview.

- **Prerequisites:** Pillar 2 (Python: functions, dicts/lists, exceptions, classes, virtualenv, pip), Pillar 4 (IOS-style CLI for VLANs, interfaces, OSPF/BGP basics), Pillar 8 (shell, SSH, `jq`). JSON/YAML basics are taught here.
- **Estimated pages:** 95 (teaching 65 incl. full code listings + end-of-chapter pack 30, of which solved questions ≈ 24)
- **Study days (indicative, full coverage):** 3.0. MUST-only path: 1.95 days.
- **Self-containment note:** all labs default to **Nokia SR Linux + FRR** in containerlab (no registration needed; SR Linux supports gNMI, NETCONF and JSON-RPC); IOS XE sandbox and cEOS steps are given as optional alternatives. Every script is printed in full with expected output.

## Learning objectives
1. Explain why automate (consistency, speed, auditability, fewer outages) and the maturity ladder: CLI scripts → templated config → declarative intent → closed-loop (telemetry-driven) automation.
2. Read and write JSON, YAML and XML; convert between them in Python; validate with JSON Schema/pydantic.
3. Use Paramiko for raw SSH/SFTP and explain channels, `exec_command` vs interactive shell, host-key policy.
4. Use Netmiko to connect to multi-vendor devices (`ConnectHandler`, `send_command`, `send_config_set`, `save_config`, `use_textfsm=True` / TTP / Genie parsing) with error handling and concurrency.
5. Generate configuration from data with Jinja2 templates (loops, conditionals, filters, inheritance) and a YAML "source of truth".
6. Use NAPALM's vendor-neutral getters (`get_facts`, `get_interfaces`, `get_bgp_neighbors`, `get_lldp_neighbors`) and its candidate-config workflow (`load_merge_candidate`/`load_replace_candidate` → `compare_config` → `commit_config` / `discard_config` → `rollback`).
7. Run inventory-driven automation in Nornir and Ansible (inventory, playbooks, `network_cli`/`netconf`/`httpapi` connections, `cisco.ios.ios_config`, `*_facts`, idempotency, check/diff mode, roles, vault).
8. Explain YANG modelling (module, container, list, leaf, key, augment, deviation; IETF vs OpenConfig vs native models), NETCONF (SSH port 830, RPCs `get`, `get-config`, `edit-config`, `commit`, `lock`; datastores running/candidate/startup), and RESTCONF (HTTPS, RFC 8040 URIs, JSON/XML encodings, HTTP verb mapping).
9. Explain gNMI (gRPC over HTTP/2, protobuf, `Capabilities/Get/Set/Subscribe`, subscription modes STREAM [sample/on_change], ONCE, POLL) and streaming telemetry vs SNMP polling; use `gnmic`.
10. Use Git for network configs (branching, pull requests, review, tags, `.gitignore` for secrets) and build a CI pipeline (GitHub Actions/GitLab CI) that lints YAML, renders templates, runs a containerlab-based test, and produces a diff for review.
11. Apply safety practices: dry-run/diff, staged rollout (canary), pre/post checks, automatic rollback, idempotency, secrets management, rate limiting connections, and logging.
12. Recognise API-first platforms (Cisco DNA Center/Catalyst Center, Meraki Dashboard API, Arista CloudVision, Juniper PyEZ, NX-API) and SDN concepts (control/data-plane separation, OpenFlow history, P4 name-check).

## Priority tags & indicative study days
| § | Section | Tag | Days | Core lab |
|---|---|---|---|---|
| 10.1 | Why automate | MUST | 0.10 | — |
| 10.2 | Data formats | MUST | 0.20 | L10.1 |
| 10.3 | Paramiko | OPTIONAL | 0.05 | — |
| 10.4 | Netmiko | MUST | 0.35 | L10.2 |
| 10.5 | Parsing CLI | SHOULD | 0.20 | L10.3 |
| 10.6 | Jinja2 & source of truth | MUST | 0.30 | L10.4 (render-only half) |
| 10.7 | NAPALM | SHOULD | 0.20 | — |
| 10.8 | Nornir | OPTIONAL | 0.05 | — |
| 10.9 | Ansible | SHOULD (MUST for CSCO, JNPR, NOK) | 0.25 | L10.6 |
| 10.10 | YANG | MUST | 0.25 | — |
| 10.11 | NETCONF/RESTCONF | MUST | 0.30 | L10.7 |
| 10.12 | gNMI & telemetry | SHOULD (MUST for GOOG, MSFT, ANET, JNPR) | 0.20 | — |
| 10.13 | Git | MUST | 0.15 | — |
| 10.14 | CI/CD & testing | SHOULD | 0.15 | — |
| 10.15 | Safety, scale, platforms, SDN | OPTIONAL (MUST-read story box) | 0.05 | — |
| — | End-of-chapter pack | MUST | 0.20 | — |
| | **Total (full coverage)** | | **3.00** | MUST-only path = 1.95 |

L10.5, L10.8, L10.9, the deploy half of L10.4 and the mini-project are tagged OPTIONAL (fully specified in the book).

## Section-by-section outline

### 10.1 Why automate, and the maturity ladder
- **Core idea:** Human CLI typing doesn't scale and causes most outages; automation gives repeatability and evidence. Ladder: L0 manual → L1 scripted → L2 templated/source of truth → L3 declarative intent with validation → L4 closed loop.
- **Analogy:** A *thali* kitchen at a wedding for 2,000 guests: you need recipes (templates), an ingredient list (source of truth), a tasting step (validation) and a head chef (CI) — not 2,000 improvisations.
- **Worked example:** Time-and-error comparison of adding VLAN 30 to 40 access switches by hand (estimate 4 h, ~3 % typo rate) vs a Netmiko loop (6 min, zero typos, logged).
- **Figures:** *Fig 10.1* — Maturity staircase with tools placed on each step. *Fig 10.2* — Reference architecture: source of truth (NetBox/YAML in Git) → CI → renderer → transport (SSH/NETCONF/gNMI) → devices → telemetry → collector → alerting, loop back.

### 10.2 Data formats: JSON, YAML, XML; and why structure beats screen-scraping
- **Core idea:** Structured data vs CLI text; JSON maps to Python dict/list; YAML indentation & anchors; XML namespaces (needed for NETCONF); conversion with `json`, `yaml` (PyYAML), `xmltodict`.
- **Analogy:** CLI output is a handwritten letter; JSON is a filled-in railway reservation form — every field in its box.
- **Worked example:** The same interface data represented as CLI text, JSON, YAML, XML; Python snippet to load YAML of 3 interfaces and print those with `enabled: false`.
- **Figures:** *Fig 10.3* — Four-panel comparison with matching colour per field across formats. *Fig 10.4* — YAML indentation pitfall illustration (tab vs spaces, list vs dict).

### 10.3 Paramiko: SSH from first principles
- **Core idea:** `SSHClient`, `set_missing_host_key_policy` (AutoAddPolicy risks), `connect`, `exec_command` vs `invoke_shell` (many network devices need interactive shell), reading buffers, SFTP; why you rarely use Paramiko directly on network gear.
- **Analogy:** Paramiko is driving a manual car — full control, more chances to stall.
- **Worked example:** Script that runs `show version` on an IOS XE sandbox through `invoke_shell`, handles the `--More--` pager by sending `terminal length 0`, and saves output.
- **Figures:** *Fig 10.5* — SSH layers (TCP 22 → transport, key exchange → user auth → channels: exec/shell/sftp).

### 10.4 Netmiko: multi-vendor SSH made sane
- **Core idea:** `ConnectHandler(device_type='cisco_ios', host, username, password)`; prompt detection; `send_command` (with `expect_string`, `read_timeout`), `send_command_timing`, `send_config_set`, `send_config_from_file`, `save_config`, `enable`; `use_textfsm=True` (ntc-templates) / `use_ttp` / `use_genie` for structured output; exceptions `NetmikoTimeoutException`, `NetmikoAuthenticationException`; concurrency with `concurrent.futures.ThreadPoolExecutor`.
- **Analogy:** Netmiko is an automatic gearbox fitted to Paramiko.
- **Worked example:** Back up running-configs of 20 devices in parallel (thread pool of 8), file-per-device with timestamp, summary table of success/failure, retries for timeouts.
- **Figures:** *Fig 10.6* — Sequence diagram: script → Netmiko → device (login, disable paging, command, prompt match, return). *Fig 10.7* — Serial vs threaded timeline bars (20 × 6 s serial = 120 s vs ≈ 18 s with 8 workers).

### 10.5 Parsing CLI output: TextFSM, TTP, Genie, regex
- **Core idea:** When APIs aren't available you parse text; TextFSM templates (ntc-templates library), TTP, Cisco Genie/pyATS parsers; regex fallback and its brittleness.
- **Analogy:** Turning a handwritten letter into a form by a trained clerk (template).
- **Worked example:** Parse `show ip interface brief` into a list of dicts with TextFSM; flag interfaces where Status=up but Protocol=down.
- **Figures:** *Fig 10.8* — Text table with a template overlay mapping columns to variables.

### 10.6 Jinja2 templating and the source of truth
- **Core idea:** Separate data (YAML/NetBox) from logic (template) from transport; loops, conditionals, filters (`ipaddr` via netaddr/ansible.utils), macros, `{% include %}`; whitespace control `{%-`; NetBox as SoT (name-check: Nautobot, Infrahub).
- **Analogy:** A wedding-card template: names and dates change; layout stays.
- **Worked example:** `vlans.yml` + `access_switch.j2` → rendered configs for three switches with per-port VLAN assignment and description; show how a typo in YAML is caught by schema validation before rendering.
- **Figures:** *Fig 10.9* — Data + template → renderer → config files flow. *Fig 10.10* — Before/after of rendered config with highlighted substitutions.

### 10.7 NAPALM: vendor-neutral getters and safe config replace
- **Core idea:** Drivers (ios, iosxr, nxos/nxos_ssh, eos, junos) behind one API; getters return normalised dicts; config workflow with candidate, diff, commit, rollback; `validate` against a YAML compliance file; underlying mechanisms differ (IOS uses SCP + `configure replace`; Junos/EOS native candidate/sessions).
- **Analogy:** A universal remote control for TVs of different brands.
- **Worked example:** Compare BGP neighbour state across an EOS and a Junos device with `get_bgp_neighbors()`; then `load_merge_candidate(config="ntp server 10.0.0.1")` → print `compare_config()` → commit → verify → rollback.
- **Figures:** *Fig 10.11* — Candidate workflow state diagram (running → load → candidate → compare → commit/discard → rollback). *Fig 10.12* — Driver abstraction diagram.

### 10.8 Nornir: Python-native inventory and concurrency
- **Core idea:** Inventory (hosts/groups/defaults YAML), tasks, plugins (nornir_netmiko, nornir_napalm, nornir_jinja2), filtering (`F(role="leaf")`), result objects, built-in threading — "Ansible-like inventory, pure Python control".
- **Analogy:** A conductor who hands sheet music to every musician at once and collects how each performed.
- **Worked example:** Nornir task: render template per host, push with NAPALM merge in dry-run, print diffs for all leaves, then commit only if all diffs are non-empty and approved.
- **Figures:** *Fig 10.13* — Inventory inheritance (defaults → groups → hosts) tree.

### 10.9 Ansible for networks
- **Core idea:** Agentless, YAML playbooks, inventory, `connection: ansible.netcommon.network_cli` / `netconf` / `httpapi`; collections (`cisco.ios`, `arista.eos`, `junipernetworks.junos`); resource modules (`ios_vlans`, `ios_interfaces`, state merged/replaced/overridden/deleted/gathered); `--check --diff`; idempotency; roles; `ansible-vault`; when to choose Ansible vs Python (team skills, declarative tasks vs complex logic).
- **Analogy:** Ansible is a printed SOP checklist every shift follows — readable by non-programmers.
- **Worked example:** Playbook that ensures VLANs 10/20/30 exist with names on all access switches using `cisco.ios.ios_vlans` with `state: merged`; run twice to demonstrate idempotency (`changed=0` on second run).
- **Figures:** *Fig 10.14* — Playbook anatomy (play → hosts → tasks → modules → handlers) annotated. *Fig 10.15* — First-run vs second-run output panels.

### 10.10 YANG data models
- **Core idea:** YANG (RFC 7950) defines schema: module, namespace, container, list (with key), leaf, leaf-list, typedef, grouping/uses, augment, deviation, config true/false; models from IETF (e.g. ietf-interfaces), OpenConfig (vendor-neutral, ops-driven), and vendor native (Cisco-IOS-XE-native); tools `pyang -f tree`, YANG Suite, yangcatalog.org.
- **Analogy:** YANG is the building plan approved by the municipal authority; NETCONF/RESTCONF/gNMI are different lorries delivering the furniture that must fit the plan.
- **Worked example:** `pyang -f tree ietf-interfaces.yang` output dissected; map `/interfaces/interface[name='GigabitEthernet2']/description` to the CLI `description` line.
- **Figures:** *Fig 10.16* — YANG tree with symbols legend (`rw`, `ro`, `*` list, `?` optional, `[name]` key). *Fig 10.17* — Model families Venn/stack (IETF, OpenConfig, native).

### 10.11 NETCONF and RESTCONF
- **Core idea:** NETCONF (RFC 6241) over SSH subsystem on port 830; `<hello>` capabilities exchange; RPCs `get`, `get-config`, `edit-config` (operations merge/replace/create/delete/remove), `lock/unlock`, `commit`, `validate`, `copy-config`, `discard-changes`; datastores running/candidate/startup; confirmed-commit; transactional, all-or-nothing. Python `ncclient`. RESTCONF (RFC 8040) over HTTPS: `/restconf/data/<module>:<path>`, GET/POST/PUT/PATCH/DELETE ↔ read/create/replace/merge/delete; `application/yang-data+json`. Comparison with CLI scraping.
- **Analogy:** NETCONF is a registered-post legal transaction (everything or nothing, with receipts); RESTCONF is the same paperwork via a web portal.
- **Worked example:** `ncclient` script: connect to IOS XE sandbox, list capabilities, `get-config` filtered to interfaces, `edit-config` to set a description on the candidate/running, verify; then the RESTCONF equivalent with `requests` and `curl -k -u … -H "Accept: application/yang-data+json"`.
- **Figures:** *Fig 10.18* — NETCONF protocol stack (content/operations/messages/secure transport layers per RFC 6241). *Fig 10.19* — RESTCONF verb ↔ NETCONF operation mapping table. *Fig 10.20* — Transaction diagram: lock → edit candidate → validate → commit → unlock; failure path rolls back.

### 10.12 gNMI and streaming telemetry
- **Core idea:** gRPC (HTTP/2, protobuf) RPCs `Capabilities`, `Get`, `Set`, `Subscribe`; paths in OpenConfig form; encodings JSON_IETF/PROTO; subscription modes STREAM (SAMPLE with interval, ON_CHANGE, TARGET_DEFINED), ONCE, POLL; dial-in vs dial-out; push vs SNMP pull; pipelines `gnmic` → Kafka/Prometheus/InfluxDB → Grafana; gNOI/gRIBI name-check.
- **Analogy:** SNMP polling is calling the plumber every five minutes to ask if there's a leak; streaming telemetry is a smart water meter that pings you the moment flow changes.
- **Worked example:** `gnmic -a leaf1:6030 --insecure subscribe --path /interfaces/interface[name=Ethernet1]/state/counters --mode stream --stream-mode sample --sample-interval 10s` against cEOS in containerlab; push to Prometheus; Grafana panel of in-octets rate; flap the interface and watch ON_CHANGE oper-status update.
- **Figures:** *Fig 10.21* — Telemetry pipeline diagram (device → collector → TSDB → dashboard → alert). *Fig 10.22* — SNMP poll vs gNMI stream timeline showing missed micro-burst in 5-min polling.

### 10.13 Git for network engineers
- **Core idea:** Repos, commits, branches, `diff`, merge vs rebase (conceptual), pull requests and code review, tags for releases, `.gitignore` and never committing secrets (`git-secrets`, pre-commit hooks), GitOps idea: Git is the source of truth, pipeline reconciles devices.
- **Analogy:** Git is the registrar's office for every config change — who, when, why, with the old version always retrievable.
- **Worked example:** Branch `feature/vlan-40`, edit YAML, commit, open PR, reviewer comments on rendered diff, merge, tag `v2026.10.29-1`.
- **Figures:** *Fig 10.23* — Branch graph (main, feature branch, merge commit). *Fig 10.24* — GitOps loop.

### 10.14 CI/CD and testing for networks
- **Core idea:** Pipeline stages: lint (yamllint, ansible-lint, `pylint`/ruff), unit tests (pytest for template rendering), schema validation, render, spin up containerlab topology, push, post-checks (pyATS/NAPALM validate/Batfish analysis), produce diff artifact, manual approval gate, deploy canary → rest, automatic rollback on failed post-check. Batfish for pre-change reachability/ACL analysis.
- **Analogy:** A mock exam before the board exam — fail cheaply in the lab, not in production.
- **Worked example:** GitHub Actions YAML with jobs `lint → render → lab-test → approve → deploy`; show a failing PR where a template change removes `no shutdown` and the lab ping test catches it.
- **Figures:** *Fig 10.25* — Pipeline swim-lane diagram with gates. *Fig 10.26* — Pre/post-check comparison table (BGP neighbours, routes count, interface status) with diff highlighting.

### 10.15 Safety, scale and the platforms you'll meet at work
- **Core idea:** Idempotency, dry run, canary, blast-radius limits, concurrency caps (don't SSH-storm AAA servers), secrets (Vault, env vars), audit logs; controllers & APIs (Catalyst Center, Meraki, CloudVision, Junos PyEZ, NX-API, SONiC at hyperscalers); SDN concept, OpenFlow history, P4 programmable data planes (for AVGO/Intel-style roles).
- **Analogy:** Never test a new pressure cooker recipe on the whole family's dinner first.
- **Worked example:** Post-mortem style story: a script with no concurrency limit and a wrong template wiped `ip route 0.0.0.0` on 120 branch routers — derive the five controls that would have prevented it.
- **Figures:** *Fig 10.27* — Canary rollout waves diagram. *Fig 10.28* — Controller/API landscape map by vendor.

## Hands-on labs
| Lab | Title | Time | Success criterion |
|---|---|---|---|
| L10.1 | Data-format kata: convert, validate and query JSON/YAML/XML in Python | 60 min | 8 exercises pass pytest |
| L10.2 | Netmiko backup bot against containerlab SR Linux/FRR ×4 (DevNet sandbox optional) with threading and retries | 2 h | All backups + CSV summary |
| L10.3 | TextFSM parsing of `show ip int brief`, `show cdp/lldp neighbors` → topology JSON → draw with graphviz | 90 min | Auto-generated diagram |
| L10.4 | Jinja2 + YAML source of truth for a 2-spine 4-leaf BGP fabric (FRR or cEOS) | 2.5 h | Fabric converges from generated config |
| L10.5 | NAPALM merge/compare/commit/rollback on cEOS and vJunos/vSRX (or cRPD) | 90 min | Diff shown; rollback restores |
| L10.6 | Ansible resource modules + idempotency + `--check --diff` | 90 min | Second run `changed=0` |
| L10.7 | NETCONF (ncclient) on SR Linux and RESTCONF via printed IOS XE transcripts (live IOS XE sandbox optional) | 2 h | Description changed via both; verified via CLI |
| L10.8 | gNMI telemetry stack: containerlab SR Linux (cEOS optional) + gnmic + Prometheus + Grafana | 2.5 h | Live dashboard; ON_CHANGE event captured |
| L10.9 | Git + GitHub Actions pipeline with containerlab test stage | 3 h | Broken PR fails; good PR passes |

## Company-tag matrix
| Topic | CSCO | QCOM | GOOG | MSFT | AMZN-NDE | JNPR | ANET | NOK | AVGO |
|---|---|---|---|---|---|---|---|---|---|
| Python scripting for network tasks | ● | ◐ | ● | ● | ● | ● | ● | ● | ◐ |
| Netmiko/Paramiko | ● | ○ | ◐ | ◐ | ● | ◐ | ◐ | ◐ | ○ |
| Jinja2 / SoT | ◐ | ○ | ● | ● | ● | ◐ | ● | ◐ | ○ |
| NAPALM / Nornir | ◐ | ○ | ◐ | ◐ | ◐ | ◐ | ◐ | ◐ | ○ |
| Ansible | ● | ○ | ◐ | ◐ | ◐ | ● | ◐ | ● | ○ |
| YANG / NETCONF / RESTCONF | ● | ○ | ● | ◐ | ◐ | ● | ◐ | ● | ◐ |
| gNMI / streaming telemetry | ◐ | ○ | ● | ● | ◐ | ● | ● | ● | ◐ |
| Git & CI/CD | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| SDN / P4 / programmable data plane | ◐ | ◐ | ● | ● | ○ | ◐ | ◐ | ◐ | ● |

## Interview question bank (30) — every question fully solved in the end-of-chapter pack
1. 🟢 Why automate networks? Give three concrete benefits and one risk.
2. 🟢 JSON vs YAML vs XML — which would you use for a human-edited inventory and why?
3. 🟢 Paramiko vs Netmiko — what problem does Netmiko solve?
4. 🟢 What does `send_config_set` do differently from `send_command`?
5. 🟢 What is idempotency? Why does it matter for Ansible playbooks?
6. 🟢 What is Git? Difference between `git fetch` and `git pull`; between a commit and a push.
7. 🟡 Write a Python function that takes a list of device dicts and returns those whose `show version` uptime is under 1 day (parsing provided text). *(AMZN-NDE-style live scripting)*
8. 🟡 Write a script that logs into 100 devices and backs up configs. How do you make it fast and robust? (Threads, timeouts, retries, logging, credential handling.)
9. 🟡 How would you parse unstructured CLI output? Compare regex, TextFSM, Genie.
10. 🟡 Explain Jinja2 templating with an example of a loop over interfaces.
11. 🟡 What is a source of truth? Why should it not be the devices' running config?
12. 🟡 Explain NAPALM's `load_merge_candidate` vs `load_replace_candidate`. What are the risks of replace?
13. 🟡 What is YANG? Explain container, list, leaf and key with an interface example.
14. 🟡 NETCONF vs RESTCONF vs gNMI: transport, encoding, use cases.
15. 🟡 Which port does NETCONF use? What happens in the `<hello>` exchange?
16. 🟡 What are NETCONF datastores? Why is a candidate datastore valuable?
17. 🟡 Map RESTCONF HTTP methods to NETCONF operations.
18. 🟡 Streaming telemetry vs SNMP polling — why did hyperscalers move to telemetry?
19. 🟡 Explain gNMI subscription modes. When would you use ON_CHANGE vs SAMPLE?
20. 🟡 Ansible vs Python scripts — when would you pick each?
21. 🟡 What would you put in a CI pipeline for network config changes?
22. 🔴 Design an automation system to roll out a new NTP/AAA config to 5,000 devices across three vendors with zero downtime and automatic rollback.
23. 🔴 Your automation pushed a bad ACL that isolated 30 sites. Walk through the incident response and the process changes afterwards (blameless post-mortem).
24. 🔴 How would you test a config change before production? (containerlab digital twin, Batfish, pre/post checks, canary.)
25. 🔴 Design a telemetry pipeline that detects micro-bursts on 10,000 ports and alerts within 30 seconds; estimate data volume.
26. 🔴 Write (whiteboard) a Python class `Device` with methods `connect`, `get_interfaces`, `push_config(dry_run=True)` and explain how you'd unit-test it without real devices (mocks).
27. 🔴 How do you handle secrets in automation repos and CI?
28. 🔴 Explain GitOps for networks and the concept of drift detection/reconciliation.
29. 🔴 What is SDN? Separate control and data planes; where do OpenFlow and P4 fit; what do hyperscalers actually run?
30. 🔴 You must automate a vendor with no API and a quirky CLI pager that sometimes prints prompts mid-output. How do you build a robust driver? (expect patterns, timing, prompt regex, retries, Netmiko custom class.)

## Trap boxes
- **"AutoAddPolicy is fine"** — disables host-key verification; man-in-the-middle risk. Use known_hosts or a managed key store.
- **"Ansible is idempotent by magic"** — `ios_command` or raw `ios_config` lines with `parents` mismatches can show `changed` every run; resource modules are idempotent, command modules are not.
- **"RESTCONF is just REST on the device"** — it is YANG-driven with specific URI and media types; not arbitrary REST.
- **"NETCONF on port 22"** — NETCONF's IANA port is 830 (SSH subsystem); some devices also allow 22.
- **"Telemetry replaces SNMP everywhere"** — traps/legacy NMS integration still exist; describe coexistence.
- **"replace is just a bigger merge"** — replace removes anything not in the candidate, including the management ACL if you forgot it.
- **Committing passwords** — once in Git history, rotating the secret is the only fix.
- **Unlimited concurrency** — can overload TACACS+/RADIUS and trip CoPP on devices.

## Cheat-sheet contents
- Netmiko snippet card (connect/command/config/save/disconnect with try/except), `device_type` list for IOS, IOS XR, NX-OS, EOS, Junos, Linux.
- NAPALM workflow card + top 10 getters.
- Ansible: inventory format, `ansible-playbook -i inv site.yml --check --diff -l leaf1`, resource-module states table.
- YANG tree symbol legend; NETCONF RPC list; RESTCONF URI pattern & verb mapping; content types.
- gNMI RPCs, subscription modes, `gnmic` commands (capabilities/get/set/subscribe).
- Ports: SSH 22, NETCONF 830, RESTCONF 443, gNMI (IANA) 9339 — plus common vendor defaults stated in-book (Arista EOS 6030, Nokia SR Linux 57400), with the advice to confirm on the target platform.
- Git essentials (clone, branch, add, commit, push, PR, revert); CI stage template.
- Safety checklist: dry-run, diff, approval, canary, pre/post checks, rollback, logging, rate-limit, secrets.

## End-of-chapter pack (Pillar 10)
- **Short notes (4 pp):** one box per §10.1–10.15; e.g. §10.11 box: "NETCONF = SSH port 830, XML, RPCs get/get-config/edit-config/commit/lock, datastores running/candidate/startup, transactional. RESTCONF = HTTPS, `/restconf/data/module:path`, GET/POST/PUT/PATCH/DELETE, JSON or XML, same YANG models."
- **One-page revision sheet:** Netmiko snippet, NAPALM workflow, Ansible command line + resource-module states, YANG tree legend, NETCONF/RESTCONF/gNMI comparison table (transport, port, encoding, RPCs, best for), gNMI subscription modes, Git six commands, safety checklist.
- **Flashcards (40):** samples — "Front: `load_replace_candidate` risk? Back: removes anything not in the file — can delete management access." · "Front: gNMI four RPCs? Back: Capabilities, Get, Set, Subscribe." · "Front: Ansible resource-module state that removes unlisted items? Back: `overridden` (device-wide) / `replaced` (per resource)." · "Front: YANG `list` must have? Back: a `key` (for config lists)."
- **Solved interview problems:** all 30 questions per answer standard C; Q7, Q8, Q26, Q30 include complete runnable Python with mock-device tests; Q22, Q25 solved as design answers with capacity estimates.
- **Self-test:** 10 MCQs + "fix this broken Jinja2 template" + "write the RESTCONF URL for interface description".

## Mini-project (OPTIONAL; flagship candidate): "FabricOps" — GitOps for a containerlab leaf-spine
- Topology: 2 spines + 4 leaves (SR Linux/FRR by default; Arista cEOS optional) + 4 Linux hosts in containerlab.
- Source of truth: `inventory.yml` + `fabric.yml` (ASNs, loopbacks, P2P /31s, VLANs/VNIs optional).
- Code: Nornir + Jinja2 renderer; NAPALM (or Netmiko) deploy with dry-run diffs; pytest unit tests; pre/post checks (BGP sessions Established, host-to-host ping matrix).
- Telemetry: gnmic → Prometheus → Grafana dashboard of interface rates and BGP state.
- CI: GitHub Actions runs lint → render → spin lab → deploy → test → upload diffs as artefacts; PR comment shows the diff.
- Deliverables: repo, README with architecture diagram, 3-minute demo video, "design decisions" doc (why Nornir over Ansible, why gNMI) — perfect for Pillar 12G deep-dive.

## Sources (author verification sources — not required reading)
- Netmiko: https://github.com/ktbyers/netmiko ; https://ktbyers.github.io/netmiko/
- Paramiko docs: https://docs.paramiko.org/
- NAPALM docs: https://napalm.readthedocs.io/
- Nornir: https://nornir.readthedocs.io/
- Ansible network docs: https://docs.ansible.com/ansible/latest/network/index.html ; Cisco IOS collection: https://docs.ansible.com/ansible/latest/collections/cisco/ios/index.html
- ntc-templates (TextFSM): https://github.com/networktocode/ntc-templates ; TTP: https://ttp.readthedocs.io/
- Jinja2: https://jinja.palletsprojects.com/
- RFC 6241 NETCONF: https://datatracker.ietf.org/doc/html/rfc6241 ; RFC 6242 NETCONF over SSH: https://datatracker.ietf.org/doc/html/rfc6242
- RFC 8040 RESTCONF: https://datatracker.ietf.org/doc/html/rfc8040 ; RFC 7950 YANG 1.1: https://datatracker.ietf.org/doc/html/rfc7950
- gNMI specification: https://github.com/openconfig/reference/blob/master/rpc/gnmi/gnmi-specification.md ; https://www.openconfig.net/docs/gnmi/gnmi-specification ; gnmic: https://gnmic.openconfig.net/
- Cisco Nexus gNMI/OpenConfig telemetry white paper: https://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/white-paper-c11-744191.html
- Juniper gNMI subscribe docs: https://www.juniper.net/documentation/us/en/software/junos/interfaces-telemetry/topics/concept/subscribe-rpc.html
- Cisco DevNet sandboxes: https://developer.cisco.com/site/sandbox/
- Batfish: https://batfish.org/ ; containerlab: https://containerlab.dev/
- YANG catalog: https://yangcatalog.org/
- Juniper/Arista interview reports referencing Python, Ansible, Linux (anecdotal): https://www.glassdoor.ca/Interview/About-Current-project-Linux-database-shell-scripting-python-kubernetes-ansible-various-networking-concepts-and-prot-QTN_5737114.htm

---

# PILLAR 11 — Troubleshooting Methodology

**Chapter title:** *The Network Detective: A Repeatable Method for Any Outage, Any Whiteboard*
**One-line promise:** Given a vague diagram and a one-line complaint, you will ask the right questions, walk the layers aloud, name the commands and expected outputs, reach the root cause, and close with fix, verification and prevention — the exact behaviour that Cisco case rounds, Google troubleshooting rounds and Amazon NDE loops score.

- **Prerequisites:** Pillars 3 and 4 (mandatory), 8 (mandatory), 9 (§9.5–9.7 for firewall/VPN cases), 5 (for the DC/ECMP case), 7 (for the Linux socket case). This pillar is deliberately placed late: it *integrates* everything.
- **Estimated pages:** 120 (framework 20 + 18 cases × ~4.5 pp ≈ 80 + end-of-chapter pack 20)
- **Study days (indicative, full coverage):** 5.0. MUST-only path: 3.3 days.
- **Interview reality this chapter is built on (from candidate reports):** Cisco network/consulting-engineer case rounds present *a deliberately vague diagram* — e.g. two LANs joined through routers and switches where "PC-A cannot reach PC-B" — and score whether you *ask questions to define the scenario* before proposing a fix; some Cisco NCE rounds hand over documentation (configs/outputs) to troubleshoot from; Google network-engineering screens and onsites include "thought process and approach to network troubleshooting problems" and troubleshooting on a diagram; Amazon NDE loops mix BGP/OSPF/TCP fundamentals with Linux troubleshooting. The chapter states these as *observed patterns*, not official formats.

## Learning objectives
1. Apply the **SCALPEL** framework (below) to any troubleshooting prompt and narrate it in a structured, time-boxed way (≈ 2 min clarify, 10–15 min diagnose, 3 min close).
2. Ask high-yield clarifying questions in five families: *scope, timeline/change, symptom precision, environment, evidence available*.
3. Choose and justify a strategy: **top-down**, **bottom-up**, **divide-and-conquer (start at L3 with ping)**, **follow-the-path**, **compare-with-working (spot the difference)**, **swap/isolate component**.
4. Know, for each OSI layer, the 3–5 most diagnostic commands on Cisco IOS/IOS XE, NX-OS/EOS-style CLI, Junos (key equivalents) and Linux, and what *healthy* vs *unhealthy* output looks like.
5. Distinguish look-alike symptoms: timeout vs refused vs reset; loss vs latency vs jitter; "can't resolve" vs "can't connect"; intermittent vs persistent; one user vs many; one direction vs both.
6. Diagnose the 18 canonical failure patterns in this chapter end-to-end and recognise them from the first symptom sentence.
7. Close every case like a senior engineer: **fix with minimal blast radius, verify with evidence, prevent recurrence** (monitoring, automation, guard rails), and communicate status (incident comms).
8. Work under incident conditions: severity, mitigation before root cause, change freeze, rollback, blameless post-mortem.

## The SCALPEL framework (the chapter's signature, printed on the inside back cover)

| Step | Name | What you do aloud | Time in an interview |
|---|---|---|---|
| **S** | **Symptom** — restate precisely | "So the user on PC-A gets a timeout when browsing to the intranet server; let me confirm exactly what 'can't reach' means." Convert vague words ("slow", "down", "can't connect") into a measurable symptom. | 30 s |
| **C** | **Clarify** — ask the five question families | *Scope:* one user/VLAN/site/all? *Timeline:* since when, constant or intermittent, any change (config, cable, upgrade, new device)? *Precision:* which app/port, error text, ping vs app? *Environment:* topology, IPs, VLANs, routing protocol, firewalls/NAT/VPN in path? *Evidence:* what logs/outputs/monitoring exist; can I run commands on both ends? | 1–2 min |
| **A** | **Assess & hypothesise** — draw/annotate the path, list top 3 hypotheses ranked by likelihood × ease of test | Annotate the diagram with every hop and every L2/L3 boundary; "Most likely, given only VLAN 20 is affected after yesterday's change: trunk allowed-list, SVI, or DHCP relay." | 1 min |
| **L** | **Layer walk** — test hypotheses with the chosen strategy, one layer at a time, saying the command *and the expected healthy output* | Default: divide-and-conquer from L3 (`ping` gateway → remote gateway → host), then go down (ARP/MAC/interface) or up (TCP port/DNS/app) depending on result. | 8–12 min |
| **P** | **Pinpoint root cause** — state it with evidence, and explain why it causes *every* observed symptom (and why the unaffected cases are unaffected) | "Root cause: VLAN 20 missing from the allowed list on trunk Gi1/0/24 after the change; it explains why only VLAN 20 hosts on SW2 fail and why SW1 hosts are fine." | 1 min |
| **E** | **Execute fix** — minimal, reversible, in a change window if needed; mitigate first if users are down | Command-level fix + rollback plan. | 1 min |
| **L** | **Lock in** — verify (same test that failed now passes, counters stable), prevent (monitoring, template/automation, guard rail, doc), communicate | "Add the VLAN via `switchport trunk allowed vlan add 20` (not without `add`!), verify, then put trunk config in the Jinja2 template with a CI check." | 1 min |

Supporting tools in the framework section:
- **Question bank card** — 25 reusable clarifying questions, grouped by the five families (printed as a tear-out card).
- **Symptom → first-suspect table** (e.g. "only large transfers hang" → MTU/PMTUD; "works by IP, not by name" → DNS; "one direction only" → asymmetric routing / ACL / NAT; "every ~30 s blips" → STP/flapping/ARP conflict; "Connection refused" → host reached, nothing listening/firewall REJECT; "timeout" → path/filter drop; "slow only for some users" → one ECMP/LAG member or duplex).
- **Layer command matrix** — rows L1…L7, columns Cisco IOS XE / NX-OS / Junos / Linux, cells = top commands. Examples: L1 `show interfaces` (CRC, input errors, late collisions, duplex) / `show interface counters errors` / `show interfaces extensive` / `ethtool -S`; L2 `show mac address-table`, `show vlan brief`, `show interfaces trunk`, `show spanning-tree`, `show etherchannel summary` / Junos `show ethernet-switching table` / Linux `ip n`, `bridge fdb`; L3 `show ip interface brief`, `show ip route x.x.x.x`, `show ip arp`, `show ip ospf neighbor`, `show ip bgp summary`, `ping`/`traceroute` with source / Junos `show route`, `show ospf neighbor`, `show bgp summary` / Linux `ip r`, `ip route get`; L4 `show access-lists` (hit counts), `show ip nat translations`, firewall session table / Linux `ss`, `conntrack -L`, `nc -zv`; L7 `dig`, `curl -v`, `openssl s_client`, application logs.
- **Strategy chooser flowchart** — "Do you have access to both ends? Is the symptom one-way? Is there a known-good comparison?" → strategy.
- **Narration script** — a sample 15-minute transcript showing pacing, thinking aloud, and how to recover when a hypothesis fails ("That rules out L2 on SW1; next I'd …").
- **Incident overlay** — when the prompt says "production is down": Mitigate → Communicate → Diagnose → Fix → Post-mortem; severity levels; why rollback-first beats root-cause-first at 2 a.m.

## Priority tags & indicative study days
| § | Section | Tag | Days |
|---|---|---|---|
| 11.1 | Why method beats memory; how interviewers score | MUST | 0.10 |
| 11.2 | SCALPEL framework + narration script | MUST | 0.40 |
| 11.3 | Clarifying-question families & card | MUST | 0.20 |
| 11.4 | Strategies (top-down, bottom-up, divide-and-conquer, follow-path, compare, swap) | MUST | 0.20 |
| 11.5 | Layer command matrix (multi-vendor + Linux) & healthy/unhealthy outputs | MUST | 0.40 |
| 11.6 | Symptom look-alikes (timeout/refused/reset, loss/latency/jitter …) | MUST | 0.20 |
| 11.7 | Incident overlay & post-mortems | SHOULD | 0.15 |
| 11.8 | Case file: Cases 1–18 (each case ≈ 0.15 days) | Cases 1–12 MUST; 13–16 SHOULD; 17–18 OPTIONAL | 2.70 |
| 11.9 | Mock rounds (3 timed, interviewer-script + scoring rubric) | SHOULD | 0.30 |
| — | End-of-chapter pack | MUST | 0.35 |
| | **Total (full coverage)** | | **5.00** (MUST-only path ≈ 3.3) |

## Section-by-section outline

### 11.1 Why method beats memory
- **Core idea:** Interviewers score structure, communication and hypothesis discipline as much as the final answer; jumping to a fix without clarifying is the #1 failure mode in case rounds.
- **Analogy:** A good doctor at a government hospital OPD: asks history, examines, orders the *cheapest decisive test first*, then prescribes — never prescribes antibiotics for "I feel unwell".
- **Worked example:** Two transcripts of the same prompt ("Users can't access the web server"): candidate A lists 12 random commands; candidate B runs SCALPEL. Rubric scores shown side by side.
- **Figures:** *Fig 11.1* — Interviewer's scoring rubric radar (clarification, structure, technical depth, evidence, communication, closure). *Fig 11.2* — Two-transcript comparison panel.

### 11.2 SCALPEL in detail
- **Core idea:** As in the table above, each step with do/don't lists and stock phrases.
- **Analogy:** Surgical checklist (WHO safe-surgery checklist) — the scalpel is used only after the checks.
- **Worked example:** Full annotated walk-through of Case 1 using every step, with timestamps.
- **Figures:** *Fig 11.3* — SCALPEL wheel with the loop back from P to A when a hypothesis fails. *Fig 11.4* — Time-budget bar for a 20-minute round.

### 11.3 Clarifying questions
- **Core idea:** Five families; ask the 3–5 highest-information questions first; state assumptions if the interviewer refuses to answer ("I'll assume a single OSPF area and no firewall; tell me if that's wrong").
- **Analogy:** Railway enquiry: "Which train, which date, which class?" before "Is there a seat?"
- **Worked example:** The vague Cisco-style diagram (two LANs, two routers, a switch each, a cloud in the middle labelled "WAN") turned into a fully specified scenario through 8 questions and answers.
- **Figures:** *Fig 11.5* — Vague diagram before/after: left as given, right annotated with answers (IPs, VLANs, protocol, link types). *Fig 11.6* — Question card.

### 11.4 Strategies
- **Core idea:** When to use which: divide-and-conquer at L3 as default; bottom-up after physical changes; top-down for app-specific complaints; follow-the-path for multi-hop; compare-with-working when one user/site is affected; swap for hardware suspicion.
- **Analogy:** Finding a fused bulb in a long serial string of Diwali lights — test the middle first (binary search).
- **Worked example:** Same fault solved with three strategies; count of steps each.
- **Figures:** *Fig 11.7* — Strategy chooser flowchart. *Fig 11.8* — Binary-search on a 6-hop path diagram.

### 11.5 Layer command matrix and reading outputs
- **Core idea:** For each layer: what to check, commands, *healthy* sample output, *unhealthy* sample output, and the inference.
- **Analogy:** Reading a blood report: reference ranges matter more than raw numbers.
- **Worked example:** `show interfaces Gi0/1` healthy vs with CRC and late collisions; `show ip ospf neighbor` FULL vs EXSTART; `show ip bgp summary` Established (prefix count) vs Active; `show interfaces trunk` allowed vs active VLAN lists.
- **Figures:** *Fig 11.9* — Matrix spread (two pages). *Fig 11.10–11.13* — Healthy/unhealthy output pairs with highlighted fields.

### 11.6 Symptom look-alikes
- **Core idea:** Precise symptom vocabulary: *timeout* (no response: drop/path) vs *connection refused* (RST: host reachable, port closed or REJECT) vs *reset mid-stream* (middlebox/idle timer/app crash); *loss* vs *latency* vs *jitter* vs *throughput*; one-way vs two-way; deterministic vs intermittent; by-name vs by-IP.
- **Analogy:** "No one picked up" vs "number does not exist" vs "call dropped" on a phone.
- **Worked example:** Three tcpdump excerpts (SYN retransmits only; SYN → RST; established then RST after 300 s idle) mapped to causes.
- **Figures:** *Fig 11.14* — Look-alike decision table. *Fig 11.15* — Three ladder diagrams.

### 11.7 Incident overlay and post-mortems
- **Core idea:** Mitigate first (roll back, fail over, drain), comms cadence, roles (incident commander, scribe), then RCA; blameless post-mortem template (timeline, impact, root cause, contributing factors, what went well, action items with owners). Links to Amazon "Ownership", "Dive Deep" and "Bias for Action" stories (Pillar 12F).
- **Analogy:** Fire brigade puts out the fire before investigating the short circuit.
- **Worked example:** Post-mortem for Case 11 (STP loop) written in the template.
- **Figures:** *Fig 11.16* — Incident timeline graphic. *Fig 11.17* — Post-mortem template page.

### 11.8 The Case File (18 fully specified scenarios)
Each case occupies a 4–5-page spread with fixed layout: **(a) case card** (title, company chips, difficulty, layers involved, priority tag); **(b) prompt as the interviewer says it**; **(c) topology figure**; **(d) clarifying questions with the interviewer's answers**; **(e) hypotheses ranked**; **(f) layer-by-layer diagnosis table** (layer | test | command | observed output (printed) | inference); **(g) root cause** and why it explains all symptoms; **(h) fix** (commands) + rollback; **(i) verification**; **(j) prevention**; **(k) interviewer follow-ups with answers**; **(l) "variant" box** (how the same case is twisted in other interviews).

Topology figure standard for all cases: icons (PC, switch, L3 switch, router, firewall, server, cloud), interface labels (Gi0/1 etc.), IPs/VLANs in grey text, the fault marked with a red lightning bolt in the *solution* page only (the prompt page shows the clean diagram, so the reader can attempt first).

---

#### Case 1 — "Internet works by IP but not by name" (MUST · 🟢 · L3/L7 · AMZN-NDE GOOG MSFT CSCO)
- **Prompt:** "A user says the internet is down."
- **Topology:** PC 192.168.10.25/24 → access switch → L3 switch/gateway 192.168.10.1 → edge router with NAT → ISP. Internal DNS server 192.168.50.53 in server VLAN.
- **Clarifying Qs & answers:** Everyone or one user? → whole VLAN 10. What exactly fails — browser error text? → "DNS_PROBE_FINISHED_NXDOMAIN"/"server not found". Does `ping 8.8.8.8` work? → yes. Any change? → DHCP scope edited yesterday. Other VLANs fine? → yes.
- **Hypotheses:** (1) wrong DNS server handed out by DHCP; (2) DNS server down; (3) ACL blocking UDP/TCP 53 from VLAN 10.
- **Layer walk:** L1–L3 proven by successful `ping 8.8.8.8` (skip down-layers explicitly and say why). L7/DNS: `ipconfig /all` or `resolvectl status` → DNS server 192.168.10.53 (non-existent). `nslookup google.com 192.168.50.53` → answers → DNS server healthy. `dig @192.168.10.53 google.com` → timeout.
- **Root cause:** DHCP option 6 typo (192.168.10.53 instead of 192.168.50.53) in VLAN 10 scope; explains why only VLAN 10 fails and IP connectivity works.
- **Fix:** Correct option 6 (`ip dhcp pool VLAN10` → `dns-server 192.168.50.53`); clients `ipconfig /renew`; interim: tell users to renew/flush (`ipconfig /flushdns`).
- **Verify:** `nslookup` from two clients; browsing works.
- **Prevent:** DHCP scope from template/IPAM; post-change test "resolve a name from each scope".
- **Follow-ups:** "If only some names failed?" → split-horizon/conditional forwarder/negative caching (SOA minimum TTL). "Why does ping by IP prove so much?" → L1–L3 and NAT both work.

#### Case 2 — "Same VLAN, different switches, can't talk" (MUST · 🟢 · L2 · CSCO JNPR ANET NOK)
- **Prompt:** "PC-A and PC-B are both in VLAN 20 but cannot ping each other."
- **Topology:** PC-A on SW1 Gi1/0/5 (VLAN 20), PC-B on SW2 Gi1/0/7 (VLAN 20), SW1 Gi1/0/24 ↔ SW2 Gi1/0/24 trunk; VLAN 10 hosts across the same trunk work.
- **Clarifying Qs:** Same subnet? → 10.20.0.0/24 both. Do VLAN 10 hosts across the trunk work? → yes. Change? → trunk re-provisioned last night. Same-switch VLAN 20 pings? → work.
- **Hypotheses:** trunk allowed-list missing VLAN 20; VLAN 20 not created on SW2; native VLAN mismatch; STP blocking VLAN 20 only (per-VLAN STP).
- **Layer walk:** L1 `show interfaces Gi1/0/24` up/up, no errors. L2 `show interfaces trunk` on SW1: "Vlans allowed on trunk: 1,10" (printed) ← evidence; `show vlan brief` on SW2 confirms VLAN 20 exists; `show mac address-table vlan 20` on SW1 lacks PC-B's MAC. PC-A `arp -a` shows incomplete for PC-B.
- **Root cause:** Re-provisioning used `switchport trunk allowed vlan 10` (replacing list) instead of `add`.
- **Fix:** `switchport trunk allowed vlan add 20` on both ends.
- **Verify:** `show interfaces trunk` lists 20 in "allowed and active" and "forwarding"; MAC learned; ping works.
- **Prevent:** Trunk config from template; trap box "`allowed vlan` without `add` replaces the list".
- **Follow-ups:** native VLAN mismatch symptoms (CDP log `%CDP-4-NATIVE_VLAN_MISMATCH`, cross-VLAN leakage); VTP pruning; how would you see it on Junos (`show ethernet-switching interface`).

#### Case 3 — "Inter-VLAN routing broken for one VLAN" (MUST · 🟢 · L2/L3 · CSCO AMZN-NDE JNPR)
- **Prompt:** "Hosts in VLAN 30 can ping each other but not anything outside their VLAN."
- **Topology:** L3 core switch with SVIs Vlan10/20/30 (10.30.0.1/24 for VLAN 30), access switches trunked to it.
- **Clarifying Qs:** Can they ping their gateway 10.30.0.1? → no. Other VLANs route fine? → yes. New VLAN? → yes, created this week.
- **Hypotheses:** SVI administratively down / no VLAN 30 in core's VLAN database (SVI down/down); hosts have wrong gateway/mask; VLAN not on uplink trunk; `ip routing` disabled (would break all VLANs → ruled out).
- **Layer walk:** Host `ipconfig` → gateway 10.30.0.1 correct. Core `show ip interface brief | inc Vlan30` → "Vlan30 10.30.0.1 YES manual administratively down down". Then after `no shut` → "up down" → `show vlan brief` lacks VLAN 30 on core (VLAN only created on access switch) → SVI line protocol needs an active VLAN with at least one up forwarding port.
- **Root cause:** Two faults — SVI shut and VLAN 30 not defined on the core / not allowed on the uplink trunk.
- **Fix:** `vlan 30` on core; add to trunk; `interface vlan 30` / `no shutdown`.
- **Verify:** `show ip int brief` up/up; host pings gateway and beyond; `show ip route connected` includes 10.30.0.0/24.
- **Prevent:** VLAN provisioning playbook that creates VLAN, trunk membership and SVI atomically with post-check.
- **Follow-ups:** Router-on-a-stick variant (`encapsulation dot1Q 30` missing/wrong); "SVI up/down — what conditions make it up/up?"; `autostate`.

#### Case 4 — "Slow file transfers after a cable swap" (MUST · 🟡 · L1/L2 · CSCO QCOM AVGO ANET)
- **Prompt:** "Since yesterday, copying files to the file server is painfully slow; web browsing seems okay."
- **Topology:** Server NIC ↔ access switch Gi1/0/10; server team hard-coded 100/full on NIC; switch left on auto.
- **Clarifying Qs:** All users or traffic to one server? → one server. Any change? → cable/NIC replaced and "tuned". Error messages? → none. Throughput measured? → ~2 Mb/s versus normal ~900 Mb/s.
- **Hypotheses:** duplex mismatch; bad cable (CRC); NIC offload/driver issue; congestion on uplink.
- **Layer walk:** Switch `show interfaces Gi1/0/10` → "Half-duplex, 100Mb/s", rising "late collision" and "runts"; server `ethtool eth0` → "Speed: 100Mb/s Duplex: Full Auto-negotiation: off". Explain: auto side falls back to half-duplex when the peer doesn't negotiate; full-duplex side sends while half side detects collisions → late collisions on the half side, CRC/FCS errors on the full side. Take two counter snapshots 10 s apart to prove increase. Interactive web traffic tolerates it; bulk TCP collapses due to loss → retransmits (confirm with `nstat`/`ss -ti` retrans).
- **Root cause:** Duplex mismatch from hard-coding one side only.
- **Fix:** Set both sides to auto (preferred) or both hard-coded identical; `ethtool -s eth0 autoneg on`.
- **Verify:** 1000/full both sides; counters stop incrementing; iperf3 ≈ 940 Mb/s.
- **Prevent:** Standard "auto/auto" policy; monitoring alert on late collisions/CRC rate.
- **Follow-ups:** "Which side shows late collisions vs CRC?"; "what if CRC errors but duplex matches?" → cable, SFP, optics (`show interfaces transceiver` light levels), EMI.

#### Case 5 — "SSH works, but big transfers over the VPN hang" (MUST · 🟡 · L3/L4 · GOOG AMZN-NDE CSCO JNPR MSFT)
- **Prompt:** "Branch users can open the intranet login page over the site-to-site VPN, but large pages and file downloads hang forever. SSH works fine."
- **Topology:** Branch LAN → branch router (IPsec tunnel, MTU 1500 physical) → internet → HQ firewall that drops all ICMP → HQ servers.
- **Clarifying Qs:** Small vs large? → small fine. Over VPN only? → yes. Recent changes? → HQ firewall "hardening: block ICMP". Which direction is the big data? → server → client.
- **Hypotheses:** PMTUD black hole (ICMP "fragmentation needed" type 3 code 4 blocked) ; MSS not clamped; DF bit set by servers.
- **Layer walk:** `ping -M do -s 1472 <server>` fails, `-s 1372` succeeds → effective path MTU ≈ 1400 (1500 minus ESP/NAT-T overhead). `tracepath` shows pmtu reduction. tcpdump on client: handshake OK (small packets), first full-size data segments never arrive, server retransmits; on HQ firewall logs: ICMP type 3 code 4 from branch router dropped.
- **Root cause:** Encapsulation reduces MTU; the router sends ICMP Frag-Needed for DF packets, the HQ firewall drops it, so the server never lowers its segment size — PMTUD black hole.
- **Fix:** Allow ICMP type 3 code 4 (and ICMPv6 Packet Too Big — mandatory in IPv6); and clamp MSS on tunnel (`ip tcp adjust-mss 1360` on tunnel interface / `iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu`).
- **Verify:** Large download succeeds; tcpdump shows MSS 1360 in SYN; DF pings at 1372 succeed.
- **Prevent:** Security policy exception list for essential ICMP (RFC 4890 for v6); tunnel template includes MSS clamp.
- **Follow-ups:** Compute overhead (see §9.8); why SSH works (small packets/interactive); why UDP apps differ (no MSS → need fragmentation or app-level sizing).

#### Case 6 — "OSPF neighbours stuck in EXSTART/EXCHANGE" (MUST · 🟡 · L3 · CSCO JNPR NOK ANET AMZN-NDE)
- **Prompt:** "We added a new link between R1 and R2 and OSPF won't come up — `show ip ospf neighbor` keeps showing EXSTART."
- **Topology:** R1 Gi0/2 (10.0.12.1/30, MTU 1500) ↔ R2 Gi0/2 (10.0.12.2/30, MTU 9000 jumbo configured on interface/ip mtu), area 0.
- **Clarifying Qs:** Which state exactly? → EXSTART/EXCHANGE, flapping. Hello/dead visible? → yes, 2-WAY reached. Interface MTUs? → "not sure". Vendors? → mixed.
- **Hypotheses:** MTU mismatch (DBD packets rejected); duplicate router ID; unicast reachability problem for DBD on NBMA.
- **Layer walk:** `show ip ospf neighbor` → EXSTART; `debug ip ospf adj` → "Nbr 2.2.2.2 has larger interface MTU"; `show ip ospf interface Gi0/2` on both → MTU 1500 vs 9000; `show interfaces Gi0/2 | inc MTU`.
- **Root cause:** Interface MTU mismatch; OSPF DBD packets carry the interface MTU and a router rejects DBDs advertising an MTU larger than its own, so the exchange never completes.
- **Fix:** Match MTUs (preferred) or `ip ospf mtu-ignore` as a stop-gap (explain risk: large LSUs may then be dropped).
- **Verify:** Neighbour FULL; `show ip route ospf` shows remote prefixes; LSDB synchronised (`show ip ospf database` same on both).
- **Prevent:** Link templates set MTU on both ends; pre-check in automation compares MTUs.
- **Follow-ups:** OSPF state machine (Down → Init → 2-Way → ExStart → Exchange → Loading → Full); what keeps neighbours at INIT (one-way hellos: ACL, multicast issue); 2-WAY normal on broadcast between DROTHERs; duplicate router ID symptoms.

#### Case 7 — "OSPF neighbour never appears" (MUST · 🟢 · L3 · CSCO JNPR NOK)
- **Prompt:** "R3 and R4 are directly connected and pingable, but no OSPF neighbour forms."
- **Topology:** R3 Gi0/0 10.0.34.1/24 ↔ R4 Gi0/0 10.0.34.2/24; R3 interface in area 0, R4 configured `network 10.0.34.0 0.0.0.255 area 1`; R4 also has `passive-interface default`.
- **Clarifying Qs:** Any neighbour state at all? → none. Recent change? → R4 is new. Authentication used? → yes on R3.
- **Hypotheses (checklist printed as "OSPF adjacency must match"):** same subnet/mask, area ID, hello/dead timers, authentication type/key, stub flags, network type compatibility, unique RIDs, interface not passive, ACL not blocking 224.0.0.5/6.
- **Layer walk:** `show ip ospf interface Gi0/0` on R4 → "No Hellos (Passive interface)", area 1; on R3 → area 0, Hello 10 Dead 40, MD5 auth. `debug ip ospf hello` on R3 → "mismatched area ID". Fix iteratively: remove passive → next debug shows "authentication type mismatch" → configure auth.
- **Root cause:** Three stacked mismatches (passive interface, area ID, authentication) — teaches "fix one, re-test, don't stop at the first finding".
- **Fix:** `no passive-interface Gi0/0`; correct area; `ip ospf authentication message-digest` + key.
- **Verify:** FULL; routes present.
- **Prevent:** Peer config generated from a single source of truth per link.
- **Follow-ups:** Which parameters must match vs needn't (process ID, priority, cost need not); Junos equivalent `show ospf interface detail`.

#### Case 8 — "BGP session stuck in Active" (MUST · 🟡 · L3/L4 · AMZN-NDE GOOG CSCO JNPR ANET NOK MSFT)
- **Prompt:** "Our eBGP session to the ISP is stuck in Active."
- **Topology:** CE router loopback 192.0.2.1 used as `update-source`, ISP PE 198.51.100.1 configured to peer with CE's physical IP 203.0.113.2; edge ACL inbound on CE WAN interface permits only established TCP + ICMP.
- **Clarifying Qs:** Ever worked? → new circuit. Which side initiates? → both configured. Peering addresses on each side? → CE uses loopback, ISP expects physical. ACLs/firewalls? → CE has edge ACL.
- **Hypotheses:** TCP 179 blocked; wrong neighbour address / update-source mismatch; eBGP TTL=1 with loopback (needs `ebgp-multihop`/`disable-connected-check`); AS number mismatch (would show NOTIFICATION, typically Idle/Active flaps with "bad AS" logs); MD5 mismatch.
- **Layer walk:** `show ip bgp summary` → State "Active" (means TCP connect attempts failing). `ping 198.51.100.1 source Loopback0` → fails (ISP lacks route to loopback) vs `ping 198.51.100.1` from WAN interface → OK. `telnet 198.51.100.1 179 /source-interface Gi0/0` → refused/timeout. `show access-lists EDGE-IN` → deny hit count rising for TCP 179 SYN from ISP. `debug ip bgp` → "connection timed out".
- **Root cause:** (a) update-source loopback while the ISP expects the physical address; (b) edge ACL blocks ISP-initiated SYNs to 179.
- **Fix:** Remove `update-source` (peer from physical interface) or agree loopback peering with ISP + multihop + static route; permit `tcp host 198.51.100.1 host 203.0.113.2 eq bgp` and the reverse.
- **Verify:** State becomes a prefix count (e.g. "1" for default route); `show ip bgp neighbors … | inc state` Established; routes in RIB.
- **Prevent:** Edge-ACL template with BGP peer object-group; pre-turn-up checklist.
- **Follow-ups:** BGP FSM (Idle → Connect → Active → OpenSent → OpenConfirm → Established) and what each stuck state means; Idle (admin) vs Active; "BGP path hunting" (reported in an NDE loop) briefly explained in answer.

#### Case 9 — "BGP Established, but the prefix isn't advertised/installed" (MUST · 🟡 · L3 · AMZN-NDE GOOG ANET JNPR NOK MSFT)
- **Prompt:** "BGP is up, but the ISP says they don't receive our 203.0.113.0/24, and internally R5 learns a route but doesn't use it."
- **Topology:** CE with `network 203.0.113.0 mask 255.255.255.0` but RIB only has 203.0.113.0/25 and /26 subnets; iBGP R5 receives routes with next-hop of the eBGP peer (not reachable in IGP, no `next-hop-self`).
- **Clarifying Qs:** Is the prefix in our routing table exactly? → "we have subnets". Any outbound route-map/prefix-list? → yes "TO-ISP". iBGP design? → full mesh, no next-hop-self.
- **Hypotheses:** `network` statement requires an *exact* RIB match; outbound policy filtering; iBGP next-hop unreachable; synchronisation (historic); RPKI/IRR filtering at ISP.
- **Layer walk:** `show ip route 203.0.113.0 255.255.255.0` → "% Network not in table". `show ip bgp 203.0.113.0/24` → not in BGP table. `show ip bgp neighbors 198.51.100.1 advertised-routes` → empty. On R5: `show ip bgp 8.8.8.0` → "Inaccessible" next hop 198.51.100.1; `show ip route 198.51.100.1` → no route.
- **Root cause:** (1) no exact /24 in RIB so `network` doesn't originate it; (2) iBGP next-hop unreachable → route not best/installed.
- **Fix:** `ip route 203.0.113.0 255.255.255.0 Null0` (anchor route) or `aggregate-address`; `neighbor R5 next-hop-self` on edge (or advertise the WAN link into IGP).
- **Verify:** `advertised-routes` shows /24; ISP confirms; R5 best path `>` installed.
- **Prevent:** Route origination checklist; RPKI ROA created for the /24.
- **Follow-ups:** BGP best-path order (weight, local-pref, locally originated, AS-path, origin, MED, eBGP over iBGP, IGP metric to next hop, …); soft reset; why /25 more-specifics might be filtered by ISPs (> /24 commonly dropped).

#### Case 10 — "Intermittent drops for one server every few minutes" (MUST · 🟡 · L2/L3 · CSCO AMZN-NDE GOOG)
- **Prompt:** "The finance server randomly becomes unreachable for 30–60 seconds, several times an hour."
- **Topology:** Server 10.1.50.20 on VLAN 50; a newly imaged lab VM accidentally configured with static 10.1.50.20.
- **Clarifying Qs:** All clients or some? → some at a time. Pattern? → random. Logs? → server sees nothing. Change? → new VMs in VLAN 50 last week.
- **Hypotheses:** duplicate IP (ARP flapping); MAC flapping from a loop; NIC teaming misconfig; ARP-cache timeout issues.
- **Layer walk:** Switch log `%IP-4-DUPADDR: Duplicate address 10.1.50.20 on Vlan50, sourced by 0050.56aa.bbbb`; `show ip arp 10.1.50.20` changes MAC between two values over time; `show mac address-table address 0050.56aa.bbbb` → port Gi1/0/33 (hypervisor); Linux `arping -D -I eth0 10.1.50.20` detects a reply from another MAC; Wireshark "duplicate use of IP detected".
- **Root cause:** Duplicate IP address; clients' ARP caches alternate between the two MACs.
- **Fix:** Re-address the VM; clear ARP (`clear arp-cache`); reserve the address in IPAM/DHCP exclusion.
- **Verify:** ARP stable; no DUPADDR logs over an hour.
- **Prevent:** IPAM, DHCP snooping + IP source guard, DAI, gratuitous-ARP conflict detection on servers.
- **Follow-ups:** Distinguish from MAC flap (`%SW_MATM-4-MACFLAP_NOTIF`) caused by loops or misconfigured NIC teaming.

#### Case 11 — "The whole floor went down when someone plugged in a switch" (MUST · 🟡 · L2 · CSCO JNPR NOK ANET)
- **Prompt:** "At 11:05 the entire 3rd floor lost network; switch CPUs at 100 %, LEDs flashing wildly."
- **Topology:** Access SW3A/SW3B uplinked to distribution; a user connected a cheap unmanaged switch with a cable looped back into two wall ports (both on SW3A). The access-port template (legacy "quiet ports") has PortFast **and `spanning-tree bpdufilter enable`** but no BPDU Guard or storm control, so the loop is never detected by STP.
- **Clarifying Qs:** Whole floor or building? → floor. Change? → "nothing" (ask about desk moves → yes, a desk move). Monitoring? → interface utilisation 100 % broadcast. Is STP enabled? → yes, Rapid PVST+, PortFast on edge ports.
- **Hypotheses:** L2 loop/broadcast storm; STP disabled or bypassed; root-bridge change; unidirectional link.
- **Layer walk:** `show interfaces | inc broadcast|rate` → huge broadcast input rates on Gi1/0/14 and Gi1/0/15; `show mac address-table` + `%SW_MATM-4-MACFLAP_NOTIF` logs: same MACs flapping between Gi1/0/14 and Gi1/0/15; `show spanning-tree interface Gi1/0/14 detail` → "The port is in the portfast mode… Bpdu filter is enabled… BPDU: sent 0, received 0" (STP is blind on these ports, so it never blocks the loop; contrast: with PortFast alone the port would receive its own BPDUs and STP would block within ~2 s); `show processes cpu sorted`. **Mitigate first:** shut Gi1/0/14.
- **Root cause:** Physical loop on edge ports where BPDU filter disabled STP's loop detection, with no BPDU Guard or storm control as a backstop.
- **Fix:** Remove loop; remove BPDU filter from access ports; enable `spanning-tree portfast bpduguard default` (or per-port), `storm-control broadcast level 1.00`, errdisable recovery policy; consider loop guard on uplinks.
- **Verify:** Broadcast rates normal, CPU normal, MAC flaps stop.
- **Prevent:** Access-port template with BPDU Guard + storm control; alerting on broadcast rate; physical security of wall ports; 802.1X.
- **Follow-ups:** Why Ethernet frames loop forever (no TTL at L2); root bridge election and root guard; how RSTP converges.

#### Case 12 — "New VLAN's clients get 169.254.x.x" (MUST · 🟢 · L2/L3/L7 · CSCO AMZN-NDE JNPR)
- **Prompt:** "Laptops in the new lab VLAN 60 get 169.254 addresses."
- **Topology:** DHCP server 10.1.99.10 in server VLAN; core L3 switch SVI Vlan60 10.1.60.1/24 without `ip helper-address`; DHCP snooping enabled on access switch with uplink not trusted.
- **Clarifying Qs:** Only VLAN 60? → yes. Static IP works? → yes (proves L2/L3). DHCP scope exists? → yes. Snooping? → enabled on access layer.
- **Hypotheses:** missing relay; scope missing/exhausted; DHCP snooping dropping server replies (untrusted uplink); option 82 issues; VLAN not on trunk (ruled out by static IP).
- **Layer walk:** Client APIPA 169.254/16 → no DHCPOFFER received. tcpdump/Wireshark on client: DISCOVER broadcasts, no OFFER. Core `show run interface vlan 60` → no helper. After adding helper, still failing → access switch `show ip dhcp snooping statistics` drops "untrusted port" for OFFER on uplink; `show ip dhcp snooping` → uplink Gi1/0/48 untrusted. (Also mention option 82 insertion causing some servers to drop if giaddr = 0.)
- **Root cause:** Missing DHCP relay on SVI + uplink not trusted for DHCP snooping.
- **Fix:** `ip helper-address 10.1.99.10` on Vlan60; `ip dhcp snooping trust` on uplink; check server scope for 10.1.60.0/24.
- **Verify:** DORA seen; client lease; `show ip dhcp snooping binding` entries.
- **Prevent:** VLAN provisioning playbook includes relay; post-check "a test client obtains a lease".
- **Follow-ups:** DORA steps and broadcast vs unicast; how the server picks the scope (giaddr); why APIPA appears.

#### Case 13 — "Traffic works one way through the firewalls" (SHOULD · 🔴 · L3/L4 · CSCO JNPR NOK GOOG AMZN-NDE)
- **Prompt:** "After adding a second internet link, some users' sessions to the cloud app break; it looks random."
- **Topology:** Two edge routers to ISP-A/ISP-B, two independent stateful firewalls (FW-A, FW-B, *no* state sync), internal core doing ECMP to both; return traffic sometimes enters via the other ISP/firewall.
- **Clarifying Qs:** Which users? → ~half, varies. Which protocols? → TCP mostly; pings fine. Firewall logs? → "TCP packet without SYN, no session — dropped" on FW-B. Change? → second ISP + ECMP.
- **Hypotheses:** asymmetric routing through stateful devices; NAT pool mismatch; MTU on new link.
- **Layer walk:** `traceroute` from user vs return path from cloud (looking glass/`traceroute` from server) differ; FW-B logs "no session"/"first packet not SYN"; `show conn` on FW-A shows SYN, FW-B gets SYN-ACK. ICMP works because both FWs permit ICMP statelessly / create sessions for echo replies in some configs.
- **Root cause:** Asymmetric return path through a different stateful firewall that has no session state.
- **Fix:** Make paths symmetric (source NAT per ISP so returns come back via same edge; or policy routing; or HA pair with state sync / clustering); disable ECMP across stateful boundaries.
- **Verify:** Sessions stable; drop counters for "no session" fall to zero.
- **Prevent:** Design rule "stateful devices must see both directions"; testing of failover paths.
- **Follow-ups:** TCP state bypass (and why it's a security trade-off); how ECMP hashing decides; uRPF strict would also drop asymmetric traffic.

#### Case 14 — "Website slow for some users only" (SHOULD · 🔴 · L1/L2/L3 · GOOG MSFT AMZN-NDE ANET)
- **Prompt:** "About a quarter of users say the internal portal is slow; others are fine. Server CPU is low."
- **Topology:** Leaf-spine: users' traffic hashed across 4 ECMP uplinks / a 4-member LAG; one member has a dirty optic with CRC errors.
- **Clarifying Qs:** Which users — any pattern? → no obvious pattern by floor. Consistent per user? → yes, same users. Measured? → curl shows long `time_starttransfer` and retransmits.
- **Hypotheses:** one bad ECMP/LAG member (hash-polarised subset); duplex/optic error; overloaded server in a load-balancer pool; DNS returning a far replica for some resolvers.
- **Layer walk:** `curl -w` timing from a slow vs fast client: DNS same, connect same, transfer slow → loss. `mtr` from slow client shows loss starting at leaf-to-spine hop and persisting. `show interfaces counters errors` on the LAG/ECMP members → Eth49 rx CRC rising; `show interfaces transceiver` low Rx power (-14 dBm). Hash explains "same users always" (5-tuple consistent).
- **Root cause:** Faulty optic on one fabric uplink causing loss for flows hashed onto it.
- **Fix:** Drain/shut the member (traffic rehashes), clean/replace optic; check fibre.
- **Verify:** CRC deltas zero, light levels normal, users' curl timings normal.
- **Prevent:** Telemetry alert on CRC rate and optic DOM thresholds (Pillar 10 gNMI pipeline); automated drain.
- **Follow-ups:** ECMP hashing inputs; why per-packet load balancing causes reordering; detecting gray failures at scale.

#### Case 15 — "VPN tunnel up, but no traffic" (SHOULD · 🟡 · L3/security · CSCO JNPR NOK)
- **Prompt:** "The new site-to-site VPN to Hyderabad shows Phase 1 up but users can't reach HQ."
- **Topology:** HQ ASA/IOS XE 10.10.0.0/16 ↔ branch 10.20.0.0/16; branch crypto ACL defines 10.20.1.0/24 ↔ 10.10.0.0/16; HQ defines 10.20.0.0/16 ↔ 10.10.0.0/16; HQ also NATs branch-bound traffic (no NAT exemption).
- **Clarifying Qs:** IKE version? → IKEv2. Phase 2 SA? → "not sure". Errors? → logs mention TS_UNACCEPTABLE. NAT on either side? → HQ PAT for internet.
- **Hypotheses:** traffic-selector/proxy-ID mismatch; transform set/PFS mismatch; NAT exemption missing; routing to tunnel missing (route-based).
- **Layer walk:** `show crypto ikev2 sa` → READY; `show crypto ipsec sa` → no SA or encaps 0/decaps 0; debug → TS_UNACCEPTABLE; compare selectors; after fixing selectors: encaps increasing at HQ but decaps 0 at branch → `show ip nat translations` shows HQ translating 10.10.x → public before encryption → NAT exemption missing.
- **Root cause:** Mismatched traffic selectors + missing NAT exemption.
- **Fix:** Mirror selectors (10.20.0.0/16 ↔ 10.10.0.0/16); add NAT exemption (`no-nat`/deny in NAT ACL) for VPN traffic.
- **Verify:** Both sides encaps/decaps incrementing; users reach HQ apps.
- **Prevent:** VPN templates generated from a single definition for both peers; checklist from §9.7.
- **Follow-ups:** Phase 1 failure causes (PSK, proposal, NAT-T ports 500/4500 blocked); policy-based vs route-based VPN debugging.

#### Case 16 — "Linux service unreachable: refused vs timeout" (SHOULD · 🟢 · L4/L7 · AMZN-NDE GOOG MSFT ANET)
- **Prompt:** "Our new API on port 8080 on a Linux VM works with curl on the VM itself but not from other machines."
- **Topology:** Client 10.0.1.5 → VM 10.0.2.10 (Ubuntu, nftables/ufw enabled, app bound to 127.0.0.1:8080); cloud security group also in path.
- **Clarifying Qs:** Error from client? → "Connection refused" on one attempt, timeout after the admin "opened" the firewall. Cloud? → yes, security group. Any change? → new deployment.
- **Hypotheses:** app bound to loopback; host firewall; cloud SG; wrong port.
- **Layer walk:** On VM `ss -tlnp | grep 8080` → `127.0.0.1:8080` users:(("python3",pid=…)) → explains refused (kernel RST for no listener on 10.0.2.10:8080). Fix bind to 0.0.0.0 → client now times out → `nft list ruleset`/`ufw status` → 8080 not allowed (DROP → timeout); allow → still timeout → `tcpdump -ni eth0 port 8080` on VM shows nothing arriving → cloud SG blocking (outside the VM). Add SG rule → works.
- **Root cause:** Three-layer stack: loopback bind (refused), host firewall DROP (timeout), cloud SG (timeout, packet never arrives).
- **Fix:** Bind correctly; allow 8080 from client CIDR in nftables and SG.
- **Verify:** `curl -v http://10.0.2.10:8080/health` from client returns 200; `ss` shows 0.0.0.0:8080.
- **Prevent:** Deployment health check from outside the host; infrastructure-as-code for SG rules.
- **Follow-ups:** RST vs ICMP port unreachable (TCP vs UDP); how tcpdump placement proves where a packet dies.

#### Case 17 — "Throughput between Mumbai and Frankfurt is terrible" (OPTIONAL · 🔴 · L4 · GOOG MSFT AMZN-NDE AVGO)
- **Prompt:** "We have a 1 Gb/s private link, but a single backup stream only reaches ~6 Mb/s. Multiple parallel streams sum up much higher."
- **Topology:** Two Linux servers, RTT 80 ms; one server's `net.ipv4.tcp_rmem` max set to 65536 by an old hardening script; a middlebox strips the window-scale option.
- **Clarifying Qs:** Loss on link? → near zero. Parallel helps? → yes. RTT? → 80 ms. OS tuning? → legacy script.
- **Hypotheses:** window-limited (BDP); window scaling stripped; loss/congestion control; CPU/disk bottleneck.
- **Layer walk:** BDP = 1 Gb/s × 0.08 s = 10 MB; observed ≈ 64 KB / 80 ms ≈ 6.5 Mb/s → window-limited signature. `ss -ti` → `rcv_space`, `wscale:` absent; tcpdump SYN on sender side shows `wscale 7`, on receiver side the option missing → middlebox stripping. `sysctl net.ipv4.tcp_rmem` shows 65536 max. iperf3 single vs `-P 8` confirms.
- **Root cause:** Window scaling removed by a middlebox plus a small receive buffer → max window 64 KB.
- **Fix:** Fix the middlebox (disable TCP normalisation option-stripping); raise `tcp_rmem/tcp_wmem` max to ≥ 16 MB; consider BBR.
- **Verify:** iperf3 single stream ≈ 900+ Mb/s.
- **Prevent:** Baseline long-haul throughput tests; config audit of sysctl drift.
- **Follow-ups:** Throughput ≈ MSS/(RTT·√loss) (Mathis) intuition; why parallel streams help.

#### Case 18 — "Traceroute shows a scary loss at hop 4" (OPTIONAL · 🟢 · L3 · GOOG CSCO AMZN-NDE)
- **Prompt:** "A customer sends an mtr showing 70 % loss at your router (hop 4) and demands a fix."
- **Topology:** Customer → ISP edge → your border router (hop 4, CoPP rate-limits ICMP TTL-exceeded generation) → … → destination (0 % loss).
- **Clarifying Qs:** Loss at the destination? → 0 %. User-visible impact? → none measured, they "saw the report". Protocol? → mtr default ICMP.
- **Hypotheses:** control-plane ICMP rate limiting (benign); real forwarding loss (would persist to later hops); asymmetric return path latency.
- **Layer walk:** Re-run `mtr -rwzbc 200 dest` and `mtr -T -P 443` — hop 4 loss but subsequent hops 0 %; on router `show policy-map control-plane` shows drops in ICMP class; data-plane interface counters clean.
- **Root cause:** No problem — ICMP generation rate-limited by CoPP; forwarding is healthy.
- **Fix:** None; explain to customer with evidence (communication skill is the point).
- **Verify:** Application metrics normal.
- **Prevent:** FAQ/runbook for customer support; consider modestly higher ICMP rate limits.
- **Follow-ups:** Latency that jumps at one hop and persists vs latency that only appears at one hop (slow-path ICMP vs real queueing).

*(Additional case stubs for the variant boxes, fully covered inside the above cases: EtherChannel suspended due to mismatched member configuration — in Case 14 variant; HSRP/VRRP split-brain — in Case 10 variant; NAT pool exhaustion — in Case 13 variant; DNS negative caching — in Case 1 variant; wireless "connected, no internet" captive-portal/DHCP — cross-referenced to Pillar 6.)*

### 11.9 Mock rounds
- **Core idea:** Three timed simulations with an "interviewer script" (what to reveal only if asked) so readers can practise with a friend: (1) Cisco-style vague diagram (combines Cases 2 + 12), (2) Google-style "a user reports slowness" (Cases 14 + 17), (3) Amazon NDE-style mixed Linux/BGP (Cases 8 + 16). Each with a 10-point scoring rubric and a model transcript.
- **Analogy:** Net practice before the match.
- **Figures:** *Fig 11.18* — Interviewer-script card layout (hidden facts under fold). *Fig 11.19* — Rubric table.

## Hands-on labs
| Lab | Title | Time | Tag |
|---|---|---|---|
| L11.1 | "Break-fix arena": a containerlab topology (6 FRR routers, 4 Linux hosts, 1 nftables firewall) with a script `breakit.sh N` that injects the fault for Cases 1, 2*, 5, 6, 7, 8, 9, 10, 12*, 13, 16, 17 (*using Linux bridges/VLANs to emulate switching) | 30–45 min per fault | MUST (pick ≥ 4 faults) — fully printed scripts, paper variant via printed outputs |
| L11.2 | Packet Tracer/CML pack for Cisco-switching cases (2, 3, 4-simulated, 11, 12) — `.pkt` files optional; all configs and outputs printed | 30 min each | SHOULD |
| L11.3 | Partner mock rounds using 11.9 scripts | 3 × 25 min | SHOULD |
| L11.4 | Write a blameless post-mortem for one injected fault | 45 min | OPTIONAL |

## Company-tag matrix
| Item | CSCO | QCOM | GOOG | MSFT | AMZN-NDE | JNPR | ANET | NOK | AVGO |
|---|---|---|---|---|---|---|---|---|---|
| Vague-diagram case with clarifying questions | ● | ○ | ● | ◐ | ◐ | ◐ | ◐ | ◐ | ○ |
| Documentation/output-based troubleshooting | ● | ○ | ◐ | ◐ | ● | ◐ | ◐ | ● | ○ |
| L2 (VLAN/STP/trunk/EtherChannel) cases | ● | ○ | ◐ | ○ | ◐ | ● | ● | ● | ○ |
| Routing protocol cases (OSPF/BGP) | ● | ○ | ● | ◐ | ● | ● | ● | ● | ○ |
| Linux host / sockets cases | ◐ | ◐ | ● | ● | ● | ◐ | ● | ◐ | ◐ |
| Performance (BDP, loss, ECMP gray failure) | ○ | ◐ | ● | ● | ● | ◐ | ● | ◐ | ◐ |
| Incident response / post-mortem behaviour | ◐ | ○ | ● | ● | ● | ◐ | ◐ | ◐ | ○ |

## Interview question bank (30) — every question fully solved in the end-of-chapter pack
1. 🟢 Describe your general approach to troubleshooting a network problem.
2. 🟢 A user can't reach a website. What are the first three things you check and why?
3. 🟢 What's the difference between a connection timeout and connection refused?
4. 🟢 Top-down vs bottom-up vs divide-and-conquer — when would you use each?
5. 🟢 What does "up/down" mean on a Cisco interface? "administratively down"?
6. 🟢 A host gets a 169.254.x.x address. What does that tell you?
7. 🟢 How do you check whether a switch has learned a host's MAC address and on which port?
8. 🟡 Two hosts in the same VLAN on different switches can't communicate. Walk me through it.
9. 🟡 OSPF neighbours stuck in EXSTART — likely cause and fix.
10. 🟡 List everything that must match for two OSPF routers to become neighbours.
11. 🟡 BGP stuck in Active vs Idle — what does each mean and how do you troubleshoot?
12. 🟡 BGP is Established but a prefix isn't advertised. Why might that be?
13. 🟡 Small packets work, large packets fail. Explain and fix.
14. 🟡 Interface shows increasing CRC errors. What could cause it and how do you prove which?
15. 🟡 Duplex mismatch: symptoms on each side.
16. 🟡 A server is intermittently unreachable for 30 seconds at a time. Causes?
17. 🟡 How would you detect and stop a broadcast storm?
18. 🟡 Explain how you'd use tcpdump to decide whether a firewall is dropping traffic.
19. 🟡 Phase 1 up, phase 2 down on an IPsec VPN. Diagnose.
20. 🟡 Traceroute shows `* * *` at hop 5 but the destination is reachable — explain.
21. 🔴 (Cisco-style) Here is a diagram of two networks connected by routers and switches; PC-A can't reach PC-B. Ask me questions and solve it. *(Model answer = full SCALPEL transcript.)*
22. 🔴 (Google-style) Users report "the internet is slow". Define slow, then troubleshoot end to end.
23. 🔴 Some users experience slowness consistently, others never, in a leaf-spine fabric. Explain how ECMP could cause this and how you'd find the bad link.
24. 🔴 After adding a second ISP, some TCP sessions break. Why, and how do you fix it architecturally?
25. 🔴 A single TCP flow across a long-distance link is slow, parallel flows are fine. Diagnose.
26. 🔴 Production is down for 2,000 users after a change you made 10 minutes ago. What do you do, minute by minute?
27. 🔴 How do you troubleshoot a problem you cannot reproduce?
28. 🔴 Write a script that detects interface error increases across 100 devices and alerts. *(Bridges to Pillar 10.)*
29. 🔴 Explain a time you troubleshot a hard problem (behavioural + technical; STAR + SCALPEL).
30. 🔴 How would you design monitoring so that the last five cases would have been detected before users noticed?

## Trap boxes
- **Jumping to the fix** — never propose a command before restating the symptom and asking at least three questions.
- **"Ping works, so the network is fine"** — ICMP ≠ TCP port ≠ application; ICMP may even take a different path/policy.
- **Stopping at the first finding** — many real cases (Cases 3, 7, 8, 12, 15, 16) have stacked faults; re-test after each fix.
- **Reading cumulative counters as rates** — take deltas.
- **Trusting mtr middle-hop loss** — only persistent loss to the destination counts.
- **`switchport trunk allowed vlan X` without `add`** — replaces the list and causes outages.
- **`ip ospf mtu-ignore` as the "fix"** — it masks the mismatch; match MTUs.
- **"Root cause = human error"** — post-mortems look for the system gap that allowed the error.
- **Not stating assumptions** when the interviewer is deliberately vague — say them aloud.
- **Debugging in production without care** — `debug all` can crash a busy router; use conditional debugs, captures with filters, and change windows.

## Cheat-sheet contents
- SCALPEL wheel; 25-question clarify card; symptom → first-suspect table (20 rows).
- Layer command matrix (IOS XE / NX-OS·EOS / Junos / Linux), compressed.
- OSPF "must-match" list and neighbour-state meanings; BGP FSM stuck-state meanings; DHCP DORA; TCP failure signatures (SYN-retrans, RST, zero-window, dup-ACK).
- MTU/MSS overhead numbers (GRE 24, IPsec ESP ~50–73, VXLAN 50, 802.1Q 4, MPLS 4 per label).
- Incident overlay checklist (mitigate, communicate, diagnose, fix, post-mortem).

## End-of-chapter pack (Pillar 11)
- **Short notes (4 pp):** one box per §11.1–11.7 plus a one-paragraph "recognition line" for each of the 18 cases (e.g. "EXSTART/EXCHANGE loop → MTU mismatch").
- **One-page revision sheet:** SCALPEL wheel + 10 best clarifying questions + symptom → first-suspect table + layer command matrix (top 3 commands per layer for IOS XE and Linux).
- **Flashcards (40):** 18 "case recognition" cards (front = symptom sentence, back = top hypothesis + decisive command), 10 state-machine cards (OSPF/BGP/TCP/DHCP), 12 command-output cards (front = printed output snippet, back = inference).
- **Solved interview problems:** all 30 questions per answer standard C; Q21, Q22 and Q26 written as full model transcripts with timestamps; Q28 includes runnable Python (Netmiko/TextFSM or SR Linux gNMI) with mocked output.
- **Self-test:** two "cold" cases (no hints) with interviewer scripts and model solutions on the reverse page.

## Mini-project (OPTIONAL): "Fault Injector & Runbook Library"
- Extend L11.1: `breakit.sh` / `fixit.sh` pairs for ≥ 10 faults + automatic grader that checks whether the network is healthy (ping matrix, OSPF/BGP state, HTTP checks).
- Write one runbook per fault in SCALPEL format; publish as a static site (MkDocs) inside the repo.
- Résumé line: "Built a fault-injection lab with 10+ reproducible network failures and SCALPEL runbooks; used by N peers for interview practice."

## Sources (author verification sources — not required reading)
- Cisco case-round reports (vague diagram, ask clarifying questions; two-network diagram; documentation-based NCE troubleshooting; NCE topics OSPF/BGP/MPLS/QoS/DHCP/EtherChannel/STP): https://www.glassdoor.com.au/Interview/Cisco-Interview-E1425-RVW1095631.htm ; https://www.glassdoor.fr/Entretien/Cisco-Entretien-E1425-RVW81744712.htm ; https://www.glassdoor.co.uk/Interview/Cisco-Interview-E1425-RVW56475813.htm ; https://static-pc.glassdoor.de/Interview/Cisco-Network-Engineer-Interview-Questions-EI_IE1425.0,5_KO6,22_IP15.htm ; https://static.glassdoor.com.mx/Interview/consulting-engineer-interview-questions-SRCH_KO0,19_IP68.htm
- Google network-engineering troubleshooting reports and prep guides: https://www.glassdoor.co.in/Interview/Google-Interview-E9079-RVW87986882.htm ; https://www.glassdoor.com/Interview/Google-Cloud-Interview-E3162960-RVW99972889.htm ; https://www.jointaro.com/interviews/companies/google/experiences/network-production-engineer-dublin-leinster-october-28-2025-no-offer-positive-5c437f29 ; https://dataford.io/interview-guides/google/network-engineer ; https://www.interviewstack.io/preparation-guide/google/network_engineer/entry
- Amazon NDE reports (BGP/OSPF/Linux/troubleshooting, BGP path hunting): https://static-pc.glassdoor.de/Interview/Amazon-Interview-E6036-RVW45180501.htm ; https://static.glassdoor.ch/Interview/Amazon-Interview-E6036-RVW70079136.htm ; https://www.glassdoor.it/Colloquio/Amazon-Colloquio-E6036-RVW33876925.htm
- RFC 2328 OSPFv2 (neighbour state machine, DBD MTU check): https://datatracker.ietf.org/doc/html/rfc2328
- RFC 4271 BGP-4 (FSM): https://datatracker.ietf.org/doc/html/rfc4271
- RFC 1191 Path MTU Discovery; RFC 4821 PLPMTUD; RFC 4890 ICMPv6 filtering: https://datatracker.ietf.org/doc/html/rfc1191 ; https://datatracker.ietf.org/doc/html/rfc4821 ; https://datatracker.ietf.org/doc/html/rfc4890
- RFC 2131 DHCP: https://datatracker.ietf.org/doc/html/rfc2131
- Cisco "Troubleshooting Ethernet" / duplex & CRC guidance: https://www.cisco.com/c/en/us/support/docs/interfaces-modules/port-adapters/12768-eth-collisions.html
- Google SRE book, Effective Troubleshooting & Postmortem Culture chapters: https://sre.google/sre-book/effective-troubleshooting/ ; https://sre.google/sre-book/postmortem-culture/
- Mathis et al., "The macroscopic behavior of the TCP congestion avoidance algorithm" (throughput formula): https://dl.acm.org/doi/10.1145/263932.264023

---

# PILLAR 12 — Supporting Subjects

**Chapter title:** *Everything Else That Decides the Offer: Aptitude, CS Core, Design, Behaviour and Your Story*
**One-line promise:** You will clear Indian campus online assessments, answer core-CS viva questions in OOP, DBMS and computer organisation, design a campus network / rate limiter / CDN on a whiteboard, and tell STAR stories mapped to Amazon's Leadership Principles — with a résumé and project deep-dive that survive 45 minutes of probing.

- **Prerequisites:** none for 12A (start on Day 1 of study); 12B needs Pillar 2; 12C needs basic SQL from 12C itself; 12D needs nothing; 12E needs Pillars 3, 4, 5, 9; 12F/12G need one or more projects (Pillars 8–11 mini-projects).
- **Estimated pages:** 190 (12A 50 · 12B 22 · 12C 26 · 12D 20 · 12E 30 · 12F 22 · 12G 20) of which end-of-chapter packs ≈ 50.
- **Study days (indicative, full coverage):** 9.0 (12A 2.5 as a daily 30-min drill · 12B 1.0 · 12C 1.25 · 12D 0.75 · 12E 1.5 · 12F 1.0 · 12G 1.0). MUST-only path: 6.0 days.
- **Structure:** seven sub-chapters, each with its own objectives, outline, labs/drills, question bank and end-of-chapter pack; one combined company matrix, trap list and source list.

## Learning objectives (pillar level)
1. Solve campus-OA quantitative, logical and verbal questions at target speed (≈ 60–75 s per question) using named shortcut methods; manage time, guessing and negative marking.
2. Answer CS-MCQ sections (C/C++ output prediction, OS, DBMS, CN, DSA) typical of HackerRank/AMCAT/Mettl-style tests.
3. Explain OOP's four pillars, SOLID, and five design patterns with code in C++ and Python; model a network domain (Device, Interface, Route) in classes.
4. Write correct SQL (joins, GROUP BY/HAVING, subqueries, window functions basics), normalise to 3NF/BCNF, explain indexes (B+ tree), ACID, isolation levels and SQL vs NoSQL.
5. Explain computer-organisation topics that networking interviews love: number systems, two's complement, bit manipulation, endianness and network byte order, memory hierarchy and caches, pipelining, interrupts vs polling, DMA and NIC ring buffers.
6. Run a light system-design interview with a 6-step template and solve: campus network, rate limiter, CDN (plus load balancer and DNS-based global traffic management as variants), with capacity estimates.
7. Build 8–10 STAR stories, map them to all 16 Amazon Leadership Principles and to Google/Microsoft/Cisco behavioural themes; answer "Tell me about yourself", "Why networking?", "Why this company?".
8. Produce a one-page ATS-friendly résumé and survive a project deep-dive (architecture, trade-offs, failures, metrics, "what would you change").

## Priority tags & indicative study days (all sub-chapters)
| § | Section | Tag | Days |
|---|---|---|---|
| 12A.1 | OA landscape & test-taking strategy | MUST | 0.10 |
| 12A.2 | Quantitative aptitude (12 topics) | MUST | 1.00 |
| 12A.3 | Logical reasoning (9 topics) | MUST | 0.60 |
| 12A.4 | Verbal ability | SHOULD | 0.30 |
| 12A.5 | Data interpretation | SHOULD | 0.20 |
| 12A.6 | CS-MCQ section (C output, OS, DBMS, CN, DSA) | MUST | 0.30 |
| 12B.1–12B.3 | OOP pillars, C++/Python mechanics | MUST | 0.50 |
| 12B.4 | SOLID & design patterns | SHOULD | 0.35 |
| 12B.5 | Modelling a network domain | OPTIONAL | 0.15 |
| 12C.1–12C.3 | Relational model, SQL, normalisation | MUST | 0.70 |
| 12C.4 | Indexes, transactions, isolation | MUST | 0.35 |
| 12C.5 | NoSQL, time-series DBs for telemetry | OPTIONAL | 0.20 |
| 12D.1–12D.2 | Number systems, bits, endianness | MUST | 0.35 |
| 12D.3–12D.4 | Memory hierarchy, caches, pipelining | SHOULD (MUST for QCOM, AVGO) | 0.25 |
| 12D.5 | Interrupts, DMA, NIC data path | SHOULD | 0.15 |
| 12E.1 | Design-interview template & estimation | MUST | 0.25 |
| 12E.2 | Design a campus network | MUST (CSCO, JNPR, NOK, ANET) | 0.40 |
| 12E.3 | Design a rate limiter | MUST | 0.35 |
| 12E.4 | Design a CDN | SHOULD | 0.35 |
| 12E.5 | Variants: L4/L7 load balancer, GSLB/anycast DNS | OPTIONAL | 0.15 |
| 12F.1–12F.3 | STAR, story bank, Amazon LPs | MUST | 0.70 |
| 12F.4 | Other companies' behavioural themes, HR questions | SHOULD | 0.30 |
| 12G.1–12G.2 | Résumé | MUST | 0.40 |
| 12G.3 | Project deep-dive drill | MUST | 0.40 |
| 12G.4 | Mock day (mock OA + 3 mock interviews) | SHOULD | 0.20 |
| | **Total (full coverage)** | | **9.0** (MUST-only ≈ 6.0) |

---

## 12A — Aptitude & Online Assessments (Indian campus)

**Promise:** Walk into any campus OA knowing the format, the 40 shortcut methods, and your personal pacing plan.

**OA landscape (as reported; label "observed patterns, verify with your placement cell"):** Cisco campus tests have historically been ~50 MCQs in 60 min across aptitude and technical sections (DSA, DBMS, OS, networking) with no negative marking; recent drills report coding-heavy formats (e.g. 2–3 coding problems, or a 90-minute AI-proctored test combining technical MCQs with DSA coding). Platforms seen across target companies: HackerRank, HackerEarth, Mettl/Mercer, AMCAT, SHL, Codility. Amazon OAs for new grads typically combine coding with work-style/behavioural components. Qualcomm/Broadcom tests lean on aptitude + C + digital electronics/computer organisation MCQs. The book shows one illustrative **format table** per company with a dated "last observed" column and the advice to confirm per drive.

### Sections
- **12A.1 OA strategy** — *Core:* time per question, two-pass method (easy first, flag hard), elimination, guessing maths under negative marking (guess if you can eliminate ≥ 1 of 4 when penalty is −1/4: expected value (1/3)(+1) + (2/3)(−0.25) = +0.17 > 0), proctoring rules (webcam, tab switching). *Analogy:* a cricket chase — rotate strike (easy questions), don't go for every six. *Worked example:* simulate a 50-Q/60-min paper with a pacing chart. *Figure:* Fig 12A.1 pacing timeline with checkpoints at Q15/30 min etc.
- **12A.2 Quantitative aptitude** — topics, each with formula box, 2 shortcut methods, 3 solved examples (easy/medium/hard), 15 practice questions with full solutions in the pack: (1) number system (divisibility, HCF/LCM, remainders, unit digit cyclicity), (2) percentages, (3) profit & loss/discount, (4) simple & compound interest, (5) ratio, proportion & partnership, (6) averages & mixtures/alligation, (7) time & work / pipes & cisterns, (8) time-speed-distance, trains, boats & streams, (9) permutations & combinations, (10) probability, (11) ages & simple equations, (12) mensuration basics & clocks/calendars. *Analogy for alligation:* mixing chai with milk at two strengths. *Worked example (TSD):* "Two trains 150 m and 100 m long at 54 km/h and 36 km/h in opposite directions; time to cross" → relative speed 90 km/h = 25 m/s → 250/25 = 10 s. *Worked example (P&C):* arrangements of "ROUTER" = 6!/2! = 360. *Figures:* Fig 12A.2 alligation cross diagram; Fig 12A.3 relative-speed train diagram; Fig 12A.4 unit-digit cyclicity table (2, 3, 7, 8 cycle 4).
- **12A.3 Logical reasoning** — number/letter series, coding-decoding, blood relations (family-tree drawing method), direction sense (compass grid), seating arrangement (linear/circular), syllogisms (Venn method), puzzles (grid method), data sufficiency, clocks/calendars logic. *Worked example:* circular seating of 8 with 6 clues solved step by step on a drawn circle. *Figures:* Fig 12A.5 family-tree notation legend (□ male, ○ female, = married, | child); Fig 12A.6 syllogism Venn cases ("All A are B; Some B are C" → no definite conclusion).
- **12A.4 Verbal ability** — reading comprehension (skim-question-scan), sentence correction (subject-verb, tense, articles, prepositions), para-jumbles (opening sentence, pronoun links), fill-in-the-blanks, synonyms/antonyms in context. *Worked example:* a 250-word RC on BGP outages with 4 questions and why each wrong option is wrong. *Figure:* Fig 12A.7 para-jumble link-word map.
- **12A.5 Data interpretation** — tables, bar, line, pie, caselets; approximation tricks (percentage-change estimation, 1/7 ≈ 14.28 %). *Worked example:* bandwidth-usage bar chart of 5 campuses → growth % and ratio questions. *Figure:* Fig 12A.8 the DI chart itself.
- **12A.6 CS-MCQ section** — C output prediction (operator precedence, pre/post increment, pointer arithmetic, `sizeof`, integer overflow, `static`), OS (scheduling calc: FCFS/SJF/RR waiting time, page replacement FIFO/LRU/Optimal faults, deadlock conditions, semaphores), DBMS (keys, normal forms, SQL output), CN (subnetting, OSI layer of a protocol, port numbers, TCP vs UDP), DSA (complexity, tree traversals, stack/queue output). *Worked example:* RR with quantum 2 on 4 processes → Gantt chart and average waiting time. *Figure:* Fig 12A.9 Gantt chart; Fig 12A.10 LRU page-frame trace table.

**Drills (in place of labs):** D12A.1–D12A.12 — twelve timed 20-question drills (one per topic group), two full-length mock OAs (60 min, 50 Q; 90 min with 2 coding + 20 MCQ), and a personal error log template (topic, error type: concept/careless/speed). Daily 30-minute drill schedule printed as a tick-box calendar.

---

## 12B — Object-Oriented Programming

**Promise:** Explain OOP in viva-ready language and show it in code — including why a network-automation library is designed the way it is.

### Sections
- **12B.1 Classes, objects, encapsulation, abstraction** — access specifiers; getters/setters; abstract classes and interfaces. *Analogy:* a TV remote (interface) hides the circuitry (implementation). *Worked example:* `class Interface { name, ip, mtu, set_mtu() with validation }` in C++ and Python. *Figure:* Fig 12B.1 UML class box.
- **12B.2 Inheritance & polymorphism** — single/multiple/multilevel; diamond problem and virtual inheritance; compile-time (overloading, templates) vs run-time (virtual functions); vtable/vptr mechanism; Python MRO and duck typing. *Analogy:* "Vehicle → Car/Bike": every vehicle can `start()`, each differently. *Worked example:* `Device` base with `get_config()` overridden by `CiscoIOS`, `JunosDevice`, `EOSDevice` — exactly NAPALM's driver pattern (link to §10.7). *Figures:* Fig 12B.2 vtable diagram (object → vptr → table of function pointers); Fig 12B.3 diamond inheritance graph.
- **12B.3 Language mechanics viva** — constructors/destructors, copy vs move, shallow vs deep copy, rule of three/five, `static` members, `friend`, operator overloading, RAII, smart pointers (`unique_ptr`, `shared_ptr`); Python `__init__`, `__repr__`, `@property`, `@classmethod/@staticmethod`, dataclasses. *Worked example:* shallow-copy bug with a pointer member, then fixed with copy constructor. *Figure:* Fig 12B.4 shallow vs deep copy memory diagram.
- **12B.4 SOLID & design patterns** — S, O, L, I, D each with a bad/good code pair; patterns: Singleton (logger/connection pool, and its testability cost), Factory (device driver by `device_type` — Netmiko's `ConnectHandler` is a factory), Strategy (pluggable routing-metric calculators), Observer (telemetry subscribers), Adapter (wrapping vendor APIs). *Analogy:* Factory = a dosa counter that makes masala/plain/onion based on your token. *Worked example:* refactor an `if vendor == ...` chain into a factory + strategy. *Figure:* Fig 12B.5 pattern cards (intent, UML mini-diagram, network example).
- **12B.5 Modelling a network domain** — classes `Device`, `Interface`, `Link`, `Route`, `RoutingTable` with longest-prefix-match method; composition vs inheritance choices. *Worked example:* implement `RoutingTable.lookup(ip)` using Python `ipaddress` with sorted prefixes (and note trie for scale, link to Pillar 1). *Figure:* Fig 12B.6 class diagram.

**Labs:** L12B.1 implement the driver factory with two mock vendors and pytest; L12B.2 C++ vtable exploration with `sizeof` and a debugger printout (printed output provided).

---

## 12C — Database Management Systems

**Promise:** Write the SQL an interviewer asks for on paper, and explain what the database does underneath.

### Sections
- **12C.1 Relational model & keys** — relation, tuple, attribute; super/candidate/primary/foreign/composite keys; ER diagrams; relational algebra basics (σ, π, ⋈). *Analogy:* a college admission register with roll number as primary key. *Worked example:* ER model of a network inventory (Site, Device, Interface, IPAddress, Circuit). *Figure:* Fig 12C.1 ER diagram with crow's-foot notation.
- **12C.2 SQL** — DDL/DML; SELECT/WHERE/ORDER BY; joins (INNER, LEFT, RIGHT, FULL, SELF, CROSS) with Venn and row-level illustrations; GROUP BY/HAVING; subqueries (correlated); `EXISTS` vs `IN`; window functions (`ROW_NUMBER`, `RANK`, `LAG`); classic questions: Nth highest salary, duplicates, employees earning more than their managers. *Worked example (network flavour):* "List sites with more than 3 devices whose software version is older than the site's newest version" — solved with GROUP BY + window function. *Figures:* Fig 12C.2 join row-matching illustration (not just Venn); Fig 12C.3 query execution order (FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT).
- **12C.3 Normalisation** — anomalies; functional dependencies; 1NF, 2NF, 3NF, BCNF with one evolving table; denormalisation trade-offs. *Worked example:* `DeviceInterfaceLog(device, site, site_city, interface, ip, vendor, vendor_support_phone)` normalised to BCNF step by step. *Figure:* Fig 12C.4 decomposition tree.
- **12C.4 Indexes, transactions, concurrency** — B-tree/B+ tree index, clustered vs non-clustered, composite index leftmost-prefix rule, hash index; ACID; isolation levels and anomalies (dirty read, non-repeatable read, phantom) table; locking vs MVCC; deadlocks; write-ahead logging. *Analogy:* index = book index; transaction = UPI payment (either both debit and credit happen or neither). *Worked example:* two concurrent "allocate next free IP" transactions causing a duplicate allocation under READ COMMITTED; fixed with `SELECT … FOR UPDATE` or a unique constraint. *Figures:* Fig 12C.5 B+ tree with leaf linkage; Fig 12C.6 isolation-level anomaly matrix.
- **12C.5 NoSQL & telemetry stores** — key-value, document, wide-column, graph; CAP (and PACELC mention); time-series DBs (Prometheus, InfluxDB) for interface counters; when to use which. *Worked example:* schema for storing per-second interface counters for 10,000 ports — row estimate and retention. *Figure:* Fig 12C.7 CAP triangle with example systems.

**Labs:** L12C.1 SQLite inventory database with 15 graded queries (all data printed in the book); L12C.2 concurrency demo with two SQLite/PostgreSQL sessions (printed transcripts provided).

---

## 12D — Computer Organisation (for network engineers)

**Promise:** Answer the "bits, bytes and buses" questions that Qualcomm, Broadcom and Arista ask, and connect them to how packets move through a NIC.

### Sections
- **12D.1 Number systems & arithmetic** — binary/octal/hex conversions; two's complement; overflow; IEEE 754 single-precision layout; fast subnet maths in binary (link to Pillar 3). *Worked example:* −18 in 8-bit two's complement = 11101110; 0xC0A80101 = 192.168.1.1. *Figure:* Fig 12D.1 IEEE 754 bit-field diagram.
- **12D.2 Bit manipulation & endianness** — AND/OR/XOR/shifts, set/clear/toggle bit, count set bits, power-of-two check; big- vs little-endian; network byte order = big-endian; `htons/htonl/ntohs/ntohl`; checksum calculation (ones'-complement sum, the IPv4 header checksum worked by hand). *Analogy:* writing dates DD/MM/YYYY vs YYYY/MM/DD — same data, different order. *Worked example:* hex dump of an IPv4 header in memory on x86 vs on the wire; compute its checksum. *Figure:* Fig 12D.2 byte-order diagram for 0x0A000001 on little-endian memory vs wire.
- **12D.3 Memory hierarchy & caches** — registers → L1/L2/L3 → DRAM → SSD; latency numbers table (order of magnitude); locality; direct-mapped vs set-associative vs fully associative; tag/index/offset split; hit ratio/AMAT; write-through vs write-back; TCAM in routers vs RAM (why LPM in hardware uses TCAM). *Worked example:* 32 KB 4-way cache, 64 B lines, 32-bit addresses → offset 6 bits, sets = 32768/(64×4) = 128 → index 7 bits, tag 19 bits. *Figures:* Fig 12D.3 pyramid with latencies; Fig 12D.4 address split diagram; Fig 12D.5 TCAM vs SRAM lookup comparison.
- **12D.4 Pipelining** — 5-stage RISC pipeline, hazards (structural, data, control), forwarding, stalls, branch prediction; speedup formula; analogy to packet-processing pipelines in switch ASICs (parser → match-action stages, link to P4 in §10.15). *Worked example:* speedup for 100 instructions on 5-stage pipeline = 500/(5+99) ≈ 4.8. *Figure:* Fig 12D.6 pipeline space-time diagram with a stall bubble.
- **12D.5 I/O: interrupts, polling, DMA, the NIC data path** — interrupt vs polling; NAPI hybrid; DMA and descriptor rings; RSS multi-queue; interrupt coalescing; how a packet travels NIC → ring → DMA → sk_buff → stack → socket (bridging Pillars 7–8, `ethtool -g/-S`). *Analogy:* a courier leaving parcels in the society's parcel room (ring) and ringing the bell only every few parcels (coalescing). *Figure:* Fig 12D.7 receive path diagram with ring buffer.

**Labs:** L12D.1 C programs for endianness detection, checksum, bit tricks (code + output printed); L12D.2 cache-friendly vs unfriendly loop timing (row vs column traversal) with printed results.

---

## 12E — Light System Design for Networking Roles

**Promise:** A repeatable 6-step design method and three complete, whiteboard-ready designs with numbers.

### Sections
- **12E.1 Template & estimation** — 6 steps: (1) clarify requirements (functional, non-functional: scale, latency, availability, security, budget); (2) estimate (users, rps, bandwidth, storage); (3) high-level diagram; (4) deep-dive 2 components; (5) failure modes & scaling; (6) trade-offs & summary. Powers of two and latency cheat table. *Analogy:* planning a wedding for 1,500 guests: headcount first, venue second. *Worked example:* estimate peak campus internet bandwidth for 8,000 users (concurrency 40 %, 2 Mb/s average → 6.4 Gb/s peak → 2 × 10 Gb/s uplinks with N+1). *Figure:* Fig 12E.1 template flow.
- **12E.2 Design a campus network** — requirements (5 buildings, 8,000 users, wired + Wi-Fi, labs, hostels, guest, CCTV/IoT, 99.9 % availability); hierarchical core/distribution/access vs collapsed core; L2 vs L3 access (routed access to shrink STP domains); VLAN/subnet plan per building and role (with a full IP plan table using 10.0.0.0/8 hierarchy); redundancy (dual uplinks, MLAG/StackWise, first-hop redundancy HSRP/VRRP or anycast gateway), routing (OSPF areas per building or single area, default from edge), Wi-Fi (controller vs cloud-managed, SSIDs mapped to VLANs, 802.1X/WPA3-Enterprise for staff, captive portal for guest), security (segmentation, ACLs, NAC, firewall at edge, DHCP snooping/DAI), services (DHCP, DNS, NTP, AAA, syslog/SNMP/telemetry), internet edge (dual ISP, BGP or static with SLA tracking, NAT), PoE budget for APs/cameras, cabling (fibre between buildings, Cat6A to access), QoS for voice/video, monitoring, capacity growth. *Worked example:* full design with oversubscription calc (48 × 1 Gb/s access ports, 2 × 10 Gb/s uplinks → 2.4:1). *Figures:* Fig 12E.2 three-tier campus diagram; Fig 12E.3 IP/VLAN plan table; Fig 12E.4 failure-domain shading (what breaks if core-1 fails).
- **12E.3 Design a rate limiter** — requirements (per user/IP/API key, limit e.g. 100 req/min, distributed across N gateways, low latency, fail-open vs fail-closed); algorithms: token bucket (rate r, burst b), leaky bucket (smooth output), fixed window (boundary burst problem), sliding-window log (memory heavy), sliding-window counter (approximation formula); placement (client, edge/API gateway, service, network device policer/shaper — link to QoS `police` vs `shape`); distributed state (Redis with atomic INCR + EXPIRE or Lua script, consistency vs latency, local + global hybrid); response (HTTP 429, `Retry-After`, headers); network-device analogue: CoPP and interface policers using token buckets (CIR, Bc, Be). *Analogy:* toll-plaza FASTag tokens refilled at a fixed rate. *Worked example:* token bucket pseudocode + Python implementation; trace of 12 requests with r = 5/s, b = 10; Redis-based sliding window counter calc for 1,000 rps per key. *Figures:* Fig 12E.5 token bucket diagram; Fig 12E.6 fixed vs sliding window boundary-burst timeline; Fig 12E.7 distributed limiter architecture.
- **12E.4 Design a CDN** — requirements (static + video, global users with India focus, cache hit ratio target, TLS, purge); components: origin, edge PoPs, mid-tier/shield caches, request routing (GeoDNS vs anycast), cache key/TTL/`Cache-Control`, purge/invalidation, consistent hashing within a PoP, TLS termination & certificate management, DDoS absorption, logging/analytics; capacity estimate (e.g. 10 M daily users × 50 MB = 500 TB/day egress → ~46 Gb/s average, ×3 peak ≈ 140 Gb/s, distributed across PoPs). *Analogy:* regional warehouses of an e-commerce company (Flipkart/Amazon) so deliveries don't come from one central depot. *Worked example:* request lifecycle for `https://cdn.example.in/video/seg42.ts` from a user in Chennai: DNS/anycast → nearest PoP → cache miss → shield → origin → fill. *Figures:* Fig 12E.8 CDN tiered architecture; Fig 12E.9 anycast vs GeoDNS routing comparison; Fig 12E.10 consistent-hash ring.
- **12E.5 Variants** — L4 vs L7 load balancer (DSR, health checks, connection draining, ECMP + consistent hashing à la Maglev); GSLB/anycast DNS; brief "design a DHCP/IPAM service" and "design a network monitoring system" outlines. *Figure:* Fig 12E.11 L4 LB with ECMP and DSR.

**Labs/drills:** D12E.1 three timed 35-minute design mocks with interviewer prompts and rubric; L12E.1 implement and unit-test token bucket + sliding-window counter in Python (code printed); L12E.2 Packet Tracer/containerlab mini-campus (optional).

---

## 12F — Behavioural Interviews, STAR & Amazon Leadership Principles

**Promise:** Eight polished stories that answer 50 behavioural questions — and no more freezing at "Tell me about a time…".

### Sections
- **12F.1 STAR (and STAR-L)** — Situation (2 lines), Task (your responsibility), Action (60 % of time, "I" not "we", specific steps), Result (quantified), + Learning. Length 2–3 min. *Analogy:* a cricket commentary highlight — situation of the match, your role, the shots you played, final score. *Worked example:* a weak vs strong STAR answer for "a time you solved a hard technical problem" (college lab network outage), annotated. *Figure:* Fig 12F.1 STAR time-split bar.
- **12F.2 Building a story bank** — sources for freshers: projects, internships, hackathons, college fests/tech clubs, team assignments, part-time work, sports/NSS/NCC; story-mining worksheet; one story can serve 3–4 principles; quantification tips (latency cut, users served, hours saved). *Worked example:* one internship story re-angled for Ownership, Dive Deep, Deliver Results. *Figure:* Fig 12F.2 story × principle matrix template (8 stories × 16 LPs).
- **12F.3 Amazon Leadership Principles (all 16)** — Customer Obsession; Ownership; Invent and Simplify; Are Right, A Lot; Learn and Be Curious; Hire and Develop the Best; Insist on the Highest Standards; Think Big; Bias for Action; Frugality; Earn Trust; Dive Deep; Have Backbone; Disagree and Commit; Deliver Results; Strive to be Earth's Best Employer; Success and Scale Bring Broad Responsibility. For each: plain-English meaning, what a fresher's evidence looks like, 2 typical questions, red flags, and a model fresher answer (in the pack). Note Bar Raiser role and that NDE loops blend LPs into every technical round. The book reproduces each principle's name and paraphrases its meaning (no need to look up the official page). *Figure:* Fig 12F.3 LP wheel grouped (customer, ownership/results, thinking, people, standards/responsibility).
- **12F.4 Other companies and HR rounds** — Google ("Googleyness", general cognitive ability, leadership, role-related knowledge), Microsoft (growth mindset, collaboration), Cisco (conscious culture, teamwork, customer focus, managerial round on projects/relocation/flexibility), Juniper/Arista/Nokia/Qualcomm/Broadcom (team fit, depth, learning). HR staples: tell me about yourself (present-past-future 90-second formula), why networking, why this company, strengths/weaknesses, where in 5 years, relocation/bond/shift questions typical in Indian campus offers, salary expectations for freshers, questions to ask the interviewer. *Worked example:* 90-second "Tell me about yourself" for a networking-focused ECE student. *Figure:* Fig 12F.4 present-past-future timeline.

**Drills:** D12F.1 story-mining worksheet; D12F.2 record yourself answering 10 LP questions, self-score with rubric (structure, specificity, "I", result, learning, time); D12F.3 peer mock with 3 follow-up probes per story ("what would you do differently?", "what was the data?", "who disagreed?").

---

## 12G — Résumé & Project Deep-Dives

**Promise:** A one-page résumé that gets shortlisted and a project you can defend for 45 minutes.

### Sections
- **12G.1 Résumé anatomy** — one page; sections (header, education with CGPA, skills grouped: Languages / Networking / Tools / Automation, projects ×3, experience/internships, certifications (CCNA/JNCIA/AWS CCP as optional), achievements); ATS-friendly formatting (single column, standard headings, no tables/graphics for text, PDF); XYZ bullet formula ("Accomplished X as measured by Y by doing Z"); keyword alignment with JDs for NDE/NCE/SDE-networking roles; honesty rule — everything on the résumé is fair game. *Worked example:* before/after résumé of a fictional student (Ananya, ECE, tier-2 college) with every change annotated. *Figures:* Fig 12G.1 annotated résumé; Fig 12G.2 bullet rewrite table (weak → strong).
- **12G.2 Choosing and presenting projects** — what impresses networking interviewers: measurable, network-relevant, your own code; recommended set from this book (netdoctor, Campus Shield, FabricOps, Fault Injector) plus DSA-flavoured networking projects (LPM trie, packet parser, mini-TCP over UDP); GitHub hygiene (README with diagram, how-to-run, results, tests, licence). *Figure:* Fig 12G.3 ideal README skeleton.
- **12G.3 Project deep-dive drill** — the 10 questions every deep-dive asks: problem & why; architecture (draw it); your contribution vs team; hardest bug and how found; key trade-off and alternatives rejected; how you tested; numbers/results; failure modes/scaling to 10×/1000×; security considerations; what you would change. Prepare a 2-minute and a 10-minute version. *Worked example:* complete deep-dive transcript on *FabricOps* (Pillar 10) with interviewer probes ("why Nornir not Ansible?", "how do you roll back?", "what if two PRs merge at once?"). *Figure:* Fig 12G.4 deep-dive preparation canvas (one page: problem, diagram, numbers, trade-offs, failures, next).
- **12G.4 Mock day & offer stage** — schedule for a full mock (OA in the morning, technical + troubleshooting + behavioural in the afternoon); offer comparison basics for freshers (CTC vs in-hand, joining bonus, bond, location, role/team); pre-placement-talk questions.

**Labs/drills:** D12G.1 résumé rewrite with checklist (20 checks); D12G.2 fill the deep-dive canvas for your flagship project; D12G.3 two recorded deep-dive mocks.

---

## Hands-on labs & drills (summary)
| ID | Title | Time | Tag |
|---|---|---|---|
| D12A.1–12 | Topic drills (20 Q each) | 25 min each | MUST |
| D12A.M1–M2 | Full mock OAs | 60 / 90 min | MUST |
| L12B.1 | Driver factory with pytest | 60 min | SHOULD |
| L12C.1 | SQLite inventory queries | 90 min | MUST |
| L12C.2 | Concurrency/isolation demo | 45 min | OPTIONAL |
| L12D.1 | Endianness, checksum, bit tricks in C | 60 min | SHOULD |
| L12E.1 | Token bucket + sliding window implementation | 60 min | SHOULD |
| D12E.1 | Three design mocks | 3 × 35 min | MUST |
| D12F.1–3 | Story bank & LP mocks | 3 h total | MUST |
| D12G.1–3 | Résumé & deep-dive | 2.5 h total | MUST |

## Company-tag matrix
| Topic | CSCO | QCOM | GOOG | MSFT | AMZN-NDE | JNPR | ANET | NOK | AVGO |
|---|---|---|---|---|---|---|---|---|---|
| Quant/logical/verbal aptitude in OA | ● | ● | ○ | ○ | ◐ | ● | ◐ | ● | ● |
| CS MCQs (C, OS, DBMS, CN) in OA | ● | ● | ○ | ◐ | ◐ | ● | ◐ | ● | ● |
| OOP viva | ● | ● | ◐ | ● | ◐ | ● | ● | ● | ● |
| DBMS/SQL | ● | ◐ | ◐ | ● | ◐ | ◐ | ◐ | ● | ◐ |
| Computer organisation / bits / endianness | ◐ | ● | ◐ | ◐ | ○ | ◐ | ● | ◐ | ● |
| Light system design (campus/rate limiter/CDN) | ● | ○ | ● | ● | ● | ◐ | ◐ | ◐ | ○ |
| Behavioural (STAR) | ● | ◐ | ● | ● | ● (LPs in every round) | ◐ | ◐ | ◐ | ◐ |
| Résumé/project deep-dive | ● | ● | ● | ● | ● | ● | ● | ● | ● |

## Interview question bank (54) — every question fully solved in the end-of-chapter packs
**12A Aptitude & CS-MCQ (10)**
1. 🟢 A sum doubles in 8 years at simple interest. In how many years does it triple? (16.)
2. 🟢 Unit digit of 7^95. (Cycle 7, 9, 3, 1; 95 mod 4 = 3 → 3.)
3. 🟢 A can finish a job in 12 days, B in 18. Together? (7.2 days.)
4. 🟡 Two trains 150 m and 100 m at 54 and 36 km/h, opposite directions — crossing time. (10 s.)
5. 🟡 How many ways to arrange the letters of "NETWORK" so that vowels are together? (6! × 2! = 1,440.)
6. 🟡 Probability that two cards drawn without replacement are both aces. (1/221.)
7. 🟡 Syllogism: All routers are devices; some devices are switches. Conclusion "Some routers are switches" — valid? (No.)
8. 🟡 Round-robin (q = 2) on P1–P4 with given bursts: average waiting time.
9. 🟡 C output: `int i = 5; printf("%d %d", i++, ++i);` — answer: undefined behaviour (unsequenced modifications) — explain why OA keys sometimes list a number and what to choose.
10. 🔴 Circular seating puzzle (8 people, 6 clues) — full solution.
**12B OOP (8)**
11. 🟢 Explain the four pillars of OOP with a networking example.
12. 🟢 Overloading vs overriding.
13. 🟡 How do virtual functions work internally (vptr/vtable)? Cost?
14. 🟡 Abstract class vs interface (C++ pure virtual vs Java/Python ABC).
15. 🟡 Shallow vs deep copy; rule of three/five.
16. 🟡 Explain SOLID with one example per letter.
17. 🟡 Implement a thread-safe Singleton in C++/Python; why might you avoid Singletons?
18. 🔴 Design classes for a router's routing table supporting add/delete/longest-prefix lookup; discuss data structure choice (trie).
**12C DBMS (8)**
19. 🟢 Primary key vs unique key vs foreign key.
20. 🟢 What is normalisation? Explain 1NF, 2NF, 3NF.
21. 🟡 Write SQL for the second-highest salary (with and without window functions).
22. 🟡 INNER vs LEFT JOIN with sample tables and output.
23. 🟡 What is an index? Why B+ tree? When does an index hurt?
24. 🟡 Explain ACID with a bank-transfer example.
25. 🟡 Isolation levels and the anomalies each prevents.
26. 🔴 Two engineers allocate the "next free IP" simultaneously and get the same address. Explain and fix at the DB level.
**12D Computer organisation (7)**
27. 🟢 Represent −18 in 8-bit two's complement.
28. 🟢 What is endianness? What is network byte order and why do we need `htons`?
29. 🟡 Write a C function to check if a machine is little-endian.
30. 🟡 Count set bits in an integer (Brian Kernighan's method) — complexity.
31. 🟡 Compute tag/index/offset bits for a given cache configuration.
32. 🟡 Interrupts vs polling vs NAPI; why high-speed NICs poll.
33. 🔴 Why do routers use TCAM for lookups? Trade-offs vs SRAM-based algorithmic lookup.
**12E System design (7)**
34. 🟡 Design the network for a new 5-building campus with 8,000 users. *(CSCO/JNPR/NOK)*
35. 🟡 Design a rate limiter for an API used by 10 M users.
36. 🟡 Token bucket vs leaky bucket — explain and relate to router policing/shaping.
37. 🔴 Design a CDN for an Indian video-streaming start-up.
38. 🔴 Anycast vs GeoDNS for request routing — pros/cons.
39. 🔴 Design an L4 load balancer for 1 M connections/s (ECMP, consistent hashing, DSR, health checks).
40. 🔴 How would you make the campus network survive a core switch failure without users noticing?
**12F Behavioural (10)**
41. 🟢 Tell me about yourself.
42. 🟢 Why networking? Why this company?
43. 🟡 (Customer Obsession) Tell me about a time you went beyond what was asked for a user.
44. 🟡 (Ownership) A time you took responsibility for something outside your role.
45. 🟡 (Dive Deep) A time you found the root cause of a difficult problem.
46. 🟡 (Have Backbone; Disagree and Commit) A time you disagreed with a teammate or professor.
47. 🟡 (Bias for Action) A time you made a decision with incomplete information.
48. 🟡 (Deliver Results) A time you met a tough deadline.
49. 🟡 (Learn and Be Curious) Something you learnt recently on your own.
50. 🔴 Tell me about a failure. What did you learn? (Earn Trust / Insist on the Highest Standards.)
**12G Résumé & projects (4)**
51. 🟡 Walk me through your best project. Draw the architecture.
52. 🟡 What was the hardest bug in your project and how did you find it?
53. 🔴 If your project had to serve 1,000× the load, what breaks first?
54. 🔴 What would you do differently if you started the project again?

## Trap boxes
- **OA:** spending 5 minutes on one hard puzzle; ignoring negative-marking maths; trusting the "expected" answer for undefined-behaviour C questions without understanding why.
- **OOP:** saying "polymorphism means many forms" and stopping — give the mechanism (virtual dispatch) and an example.
- **DBMS:** "Index always speeds things up" — slows writes, costs storage, unused for low-selectivity columns or functions on the column.
- **CompOrg:** confusing network byte order with "little-endian"; network byte order is big-endian.
- **Design:** drawing boxes before asking requirements and doing estimates; forgetting failure modes and security; no numbers.
- **Behavioural:** "we" instead of "I"; no quantified result; the "fake weakness" ("I work too hard"); stories with no conflict; one story reused identically for everything.
- **Résumé:** listing technologies you can't answer three questions about; two-page résumé for a fresher; graphics that break ATS; inflated CGPA or titles.
- **Deep-dive:** not knowing why you picked a tool; claiming team work as yours.

## Cheat-sheet contents
- Aptitude formula sheet (percent ↔ fraction table, SI/CI, TSD relative speed, work-rate, alligation, P&C/probability rules, unit-digit cycles, divisibility rules).
- CS-MCQ quick facts (scheduling formulas, page-replacement rules, deadlock conditions, normal-form definitions, port numbers, subnet table).
- OOP: pillars, SOLID one-liners, five pattern cards.
- SQL: join types, query order, window functions syntax, isolation anomaly matrix.
- CompOrg: two's complement steps, bit-trick table, endianness diagram, cache address split formula, pipeline speedup.
- Design template + estimation numbers (powers of 2, latency table, bandwidth conversions).
- STAR template + 16 LPs with one-line meanings + "Tell me about yourself" formula.
- Résumé checklist (20 items) + deep-dive canvas.

## End-of-chapter pack (Pillar 12 — one pack per sub-chapter, same five parts)
- **Short notes (≈ 2 pp per sub-chapter, 14 pp total):** e.g. 12E box: "Rate limiter: token bucket (r, b) allows bursts up to b; leaky bucket smooths; fixed window has boundary bursts; sliding-window counter ≈ prev × overlap + current; distributed via Redis atomic ops; return 429 + Retry-After."
- **One-page revision sheet per sub-chapter (7 pages):** 12A formula sheet; 12B OOP/SOLID/patterns; 12C SQL & isolation; 12D bits & caches; 12E design template + three design skeletons; 12F STAR + LP list + story matrix; 12G résumé checklist + deep-dive canvas.
- **Flashcards (60):** 20 aptitude formula cards, 8 OOP, 8 DBMS, 8 CompOrg, 6 design, 10 LP-meaning cards (front = principle, back = meaning + fresher evidence example).
- **Solved interview problems:** all 54 questions per answer standard C; aptitude solutions show the fastest method *and* the conventional method; SQL questions show sample tables and exact output; coding questions (Q17, Q18, Q29, Q30) include runnable code; design questions (Q34–Q40) include diagrams and estimates; behavioural questions (Q41–Q50) include a complete model STAR answer from a fresher's perspective *plus* a "make it yours" template and the follow-up probes with guidance.
- **Practice bank (beyond the interview bank):** 300 aptitude questions (25 per topic) and 100 CS-MCQs, all with full solutions; 2 full mock OAs with answer keys and explanations.
- **Self-test per sub-chapter:** 10 MCQs + 1 short task (e.g. write one SQL query; draft one STAR story; sketch one design).

## Mini-project (OPTIONAL): "Placement Readiness Portfolio"
- Deliverables: final one-page résumé; GitHub profile with 2–3 polished repos from Pillars 8–11 projects; a story bank document (8 STAR stories mapped to LPs); one design write-up (campus network for your own college, using real building names and a plausible IP plan); a 2-minute and a 10-minute deep-dive recording of your flagship project; personal OA error log trend.

## Sources (author verification sources — not required reading)
- Cisco campus OA formats (anecdotal, varying by year): https://www.faceprep.in/article/cisco-placement-papers-a-complete-guide-to-crack-the-online-test/ ; https://faceprep.in/article/cisco-hiring-process-for-freshers-2026/ ; https://prepinsta.com/cisco/ ; https://www.geeksforgeeks.org/cisco-interview-experience-on-campus-2018/ ; https://www.geeksforgeeks.org/cisco-interview-experience-for-internship-on-campus-2020/ ; https://cpt.hitbullseye.com/Cisco-Test-Pattern.php ; https://www.naukri.com/code360/library/ways-to-get-into-cisco ; https://www.designgurus.io/answers/detail/what-is-the-cisco-interview-process-like-round-by-round
- Juniper/Arista interview reports (OOP, Python, Linux, networking): https://www.geeksforgeeks.org/juniper-networks-interview-experience-3/ ; https://www.interviewquery.com/guides/juniper-networks-software-engineer ; https://www.interviewquery.com/guides/arista-networks-software-engineer
- Amazon Leadership Principles (official): https://www.aboutamazon.com/working-at-amazon/our-leadership-principles ; 2021 expansion to 16: https://www.carrus.io/blog/amazon-newprinciples
- Amazon behavioural emphasis in SysDE/NDE loops (anecdotal): https://static.glassdoor.at/Interview/Amazon-System-Development-Engineer-Interview-Questions-EI_IE6036.0,6_KO7,34_IP5.htm
- Google behavioural/STAR in network-engineer loops (anecdotal): https://www.glassdoor.co.uk/Interview/Google-Network-Implementation-Engineer-Interview-Questions-EI_IE9079.0,6_KO7,38.htm
- Google "How we hire": https://www.google.com/about/careers/applications/how-we-hire/
- Token bucket / policing: RFC 2697 (srTCM), RFC 2698 (trTCM): https://datatracker.ietf.org/doc/html/rfc2697 ; https://datatracker.ietf.org/doc/html/rfc2698
- Maglev load balancer (Google, NSDI 2016): https://research.google/pubs/maglev-a-fast-and-reliable-software-network-load-balancer/
- Cisco Campus LAN design guides (Cisco Validated Design): https://www.cisco.com/c/en/us/solutions/design-zone/networking-design-guides/campus-wired-wireless.html
- Database isolation anomalies: "A Critique of ANSI SQL Isolation Levels" (Berenson et al., 1995): https://www.microsoft.com/en-us/research/publication/a-critique-of-ansi-sql-isolation-levels/
- RFC 1071 Internet checksum computation: https://datatracker.ietf.org/doc/html/rfc1071

---

## Cross-pillar notes for the coordinator
- **Dependencies:** P11 cases cite P3 (ARP/DHCP/TCP), P4 (VLAN/STP/OSPF/BGP), P5 (ECMP/leaf-spine), P8 (tools), P9 (IPsec/firewalls). P12B–D overlap with P2 (Programming) and P7 (OS) — recommend P12 owns *viva-style* coverage and cross-references the deep treatment in P2/P7 to avoid duplication.
- **Shared assets to build once:** the containerlab "Lab Setup from Zero" appendix; the icon set and terminal-card style; a single fictional company/campus ("Sahyadri Institute of Technology", 5 buildings) reused across P8 labs, P9 Campus Shield, P11 cases and P12E campus design, so readers see one coherent network grow through the book.
- **Answer volume estimate (Pillars 8–12):** 176 interview questions + 18 cases + 400 practice aptitude/CS-MCQ items — budget ≈ 160 pages of solutions across the five packs (already included in the page estimates above).
- **Pages (Pillars 8–12):** 90 + 100 + 95 + 120 + 190 = **595 pages**.
