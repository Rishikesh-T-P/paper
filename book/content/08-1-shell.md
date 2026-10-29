::: {.chapter .p8}
::: opener
[Part I · Pillar 8]{.part-label}

[8]{.num}

# Linux and Network Tools {#ch8}

[The engineer's toolbox: seeing the network from a Linux shell, and reading every field of what it prints.]{.promise}

1. [8.1 Why a network engineer lives in Linux]{} [MUST]{}
2. [8.2 Shell survival kit]{} [MUST]{}
3. [8.3 Text processing for log hunting]{} [MUST]{}
4. [8.4 Bash scripting that survives production]{} [SHOULD]{}
5. [8.5 iproute2 and network namespaces]{} [MUST]{}
6. [8.6 Sockets on the wire: ss]{} [MUST]{}
7. [8.7 Packet capture I: tcpdump]{} [MUST]{}
8. [8.8 Packet capture II: Wireshark]{} [SHOULD]{}
9. [8.9 DNS from the command line]{} [MUST]{}
10. [8.10 Path and reachability tools]{} [MUST]{}
11. [8.11 Link layer and NIC health]{} [SHOULD]{}
12. [8.12 Netfilter: iptables and nftables]{} [MUST]{}
13. [8.13 Performance: iperf3, BDP, buffers]{} [SHOULD]{}
14. [8.14 Systems debugging toolkit]{} [SHOULD]{}
:::

<style>.p8 pre{font-size:7pt;line-height:1.38}</style>

## [8.1]{.sec}Why a network engineer lives in Linux [Must · ■□□]{.tag} {#s8-1}

Almost every network device that is not a laptop runs Linux, or sits beside a Linux machine that does. Arista EOS, Nokia SR Linux, SONiC, Cumulus and Junos Evolved are Linux distributions with a routing stack on top; Cisco NX-OS offers a Bash shell; servers, hypervisors, containers and cloud instances are Linux throughout. Hence the first action in most incidents is to open a shell, and the interview for a network role usually asks the candidate to do so on a whiteboard. This pillar teaches that shell as a measuring instrument for the network.

The key fact is that every tool in this chapter is a *window onto kernel state*. The kernel holds the interface table, the routing table, the ARP cache, the socket table and the packet-filter rules; the tools merely ask for them over a few interfaces: netlink sockets (`ip`, `ss`), `ioctl` calls into the NIC driver (`ethtool`), a packet tap (`tcpdump`), and the `/proc` and `/sys` file systems. Once one knows which window shows which table, a symptom points directly to a command (Figure 8.1).

<figure>
<svg viewBox="0 0 480 210" width="480"><defs><marker id="a81" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs>
<rect class="box" x="150" y="8" width="170" height="40" rx="2"/><text class="lbl" x="235" y="24" text-anchor="middle">User space</text><text class="sm" x="235" y="38" text-anchor="middle">sshd · FRR · nginx · NOS CLI</text>
<rect class="fill" x="150" y="62" width="170" height="86" rx="2" stroke="#1A1D23" stroke-width="0.8"/><text class="lbl" x="235" y="76" text-anchor="middle">Linux kernel</text>
<text class="sm" x="235" y="92" text-anchor="middle">sockets (TCP, UDP)</text><text class="sm" x="235" y="106" text-anchor="middle">netfilter hooks · routing tables</text><text class="sm" x="235" y="120" text-anchor="middle">neighbour cache · net_device</text><text class="sm" x="235" y="134" text-anchor="middle">driver (ring buffers, offloads)</text>
<rect class="box" x="150" y="162" width="170" height="36" rx="2"/><text class="lbl" x="235" y="178" text-anchor="middle">NIC / ASIC</text><text class="sm" x="235" y="190" text-anchor="middle">PHY, MAC, DMA engine</text>
<text class="mono" x="10" y="30">ss</text><text class="sm" x="10" y="40">sock_diag</text><line class="acc" x1="48" y1="34" x2="148" y2="86" marker-end="url(#a81)"/>
<text class="mono" x="10" y="78">ip</text><text class="sm" x="10" y="88">netlink</text><line class="acc" x1="40" y1="100" x2="148" y2="112" marker-end="url(#a81)"/>
<text class="mono" x="10" y="132">nft / iptables</text><line class="acc" x1="72" y1="128" x2="148" y2="106" marker-end="url(#a81)"/>
<text class="mono" x="352" y="40">strace</text><text class="sm" x="352" y="50">system calls</text><line class="acc" x1="350" y1="44" x2="322" y2="32" marker-end="url(#a81)"/>
<text class="mono" x="352" y="100">tcpdump</text><text class="sm" x="352" y="110">AF_PACKET tap</text><line class="acc" x1="350" y1="104" x2="322" y2="130" marker-end="url(#a81)"/>
<text class="mono" x="352" y="168">ethtool</text><text class="sm" x="352" y="178">driver ioctl</text><line class="acc" x1="350" y1="172" x2="322" y2="176" marker-end="url(#a81)"/>
<text class="mono" x="352" y="140">/proc /sys</text><line class="lg" x1="350" y1="138" x2="322" y2="100"/>
</svg>
<figcaption><b>Figure 8.1</b> Where each tool of this chapter taps into the system. The commands are different faces of one kernel, which is why a Linux host, an Arista switch and a container give the same counters.</figcaption>
</figure>

Consider how little changes between platforms. On an Arista switch `show interfaces Ethernet1` prints counters from the same `net_device` structure that `ip -s link show et1` prints from the EOS Bash shell, and that `ip -s link show eth0` prints on an Ubuntu server. The legacy tools (`ifconfig`, `route`, `arp`, `netstat`) read the same data through older, slower interfaces and are deprecated; Table 8.1 gives the replacements that interviewers expect.

| Legacy (net-tools) | Modern | Notes |
|---|---|---|
| `ifconfig` | `ip addr`, `ip -s link` | `ip -br a` gives one line per interface |
| `route -n` | `ip route`, `ip route get` | `get` shows the route actually chosen |
| `arp -n` | `ip neigh` | shows NUD states, not only entries |
| `netstat -tulpn` | `ss -tulpn` | `ss` reads the kernel directly through netlink |
| `brctl`, `vconfig` | `ip link … type bridge`, `type vlan` | |
| `iptables` | `nft` | same netfilter hooks, one syntax ([8.12](#s8-12){.ref}) |

::: lens
[AMAZON · GOOGLE · ARISTA · JUNIPER · CISCO]{.co}

Interviewers rarely ask for the syntax of one command in isolation. They give a symptom ("the service is unreachable") and watch which command the candidate types first and what the candidate does with the output. A strong answer names the layer being tested before the command, uses the modern tool, and states what a good and a bad result look like. The command ladder of the Revision Spread at the end of this chapter is built for exactly this.
:::

## [8.2]{.sec}Shell survival kit [Must · ■□□]{.tag} {#s8-2}

Linux treats nearly everything as a *file*: a document, a terminal, a pipe, a device, even a running process (under `/proc`). Programs are small and do one job, and the shell joins them by connecting the output of one to the input of the next. Three streams are open in every process: *standard input* (descriptor 0), *standard output* (1) and *standard error* (2). Descriptors are explained in [7.9](#s7-9){.ref} and [7.10](#s7-10){.ref}; here they matter because redirection simply re-points them.

| Operator | Effect | Example |
|---|---|---|
| `>` / `>>` | send stdout to a file (truncate / append) | `ip -br a > addr.txt` |
| `<` | read stdin from a file | `sort < hosts.txt` |
| `2>` | send stderr to a file | `ping x 2> err.txt` |
| `2>&1` | make stderr follow stdout | `cmd > all.log 2>&1` |
| `2>/dev/null` | discard stderr | `find / -name x 2>/dev/null` |
| <code>&#124;</code> | stdout of left becomes stdin of right | <code>ss -tan &#124; wc -l</code> |
| `&&` / <code>&#124;&#124;</code> | run next only if previous succeeded / failed | `make && ./run` |
| `;` and `&` | run in sequence / run in background | `sleep 9 &` |

Every command returns an *exit status* in `$?`: 0 means success and anything else means failure, which is why `&&` and `||` work. The *pipeline* is the central idea. Consider the standard question "which five clients hit the web server most?", answered by `awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -5`. Each stage is a separate process; the kernel connects them with pipes (small in-memory buffers), and a slow reader makes the writer wait, so no stage needs the whole file in memory (Figure 8.2).

<figure>
<svg viewBox="0 0 480 120" width="480"><defs><marker id="a82" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker></defs>
<rect class="box" x="4" y="26" width="76" height="32" rx="2"/><text class="mono" x="42" y="40" text-anchor="middle">awk $1</text><text class="sm" x="42" y="51" text-anchor="middle">pick column 1</text>
<rect class="box" x="100" y="26" width="76" height="32" rx="2"/><text class="mono" x="138" y="40" text-anchor="middle">sort</text><text class="sm" x="138" y="51" text-anchor="middle">group equal lines</text>
<rect class="box" x="196" y="26" width="76" height="32" rx="2"/><text class="mono" x="234" y="40" text-anchor="middle">uniq -c</text><text class="sm" x="234" y="51" text-anchor="middle">count runs</text>
<rect class="box" x="292" y="26" width="76" height="32" rx="2"/><text class="mono" x="330" y="40" text-anchor="middle">sort -rn</text><text class="sm" x="330" y="51" text-anchor="middle">biggest first</text>
<rect class="box" x="388" y="26" width="76" height="32" rx="2"/><text class="mono" x="426" y="40" text-anchor="middle">head -5</text><text class="sm" x="426" y="51" text-anchor="middle">first five</text>
<line class="ln" x1="80" y1="42" x2="98" y2="42" marker-end="url(#a82)"/><line class="ln" x1="176" y1="42" x2="194" y2="42" marker-end="url(#a82)"/><line class="ln" x1="272" y1="42" x2="290" y2="42" marker-end="url(#a82)"/><line class="ln" x1="368" y1="42" x2="386" y2="42" marker-end="url(#a82)"/>
<text class="sm" x="42" y="14" text-anchor="middle">10.20.1.15</text><text class="sm" x="138" y="14" text-anchor="middle">10.20.1.15 ×3, …</text><text class="sm" x="234" y="14" text-anchor="middle">3 10.20.1.15</text><text class="sm" x="330" y="14" text-anchor="middle">3 10.20.7.9 first</text><text class="sm" x="426" y="14" text-anchor="middle">top rows</text>
<path class="dash lg" d="M42 58 L42 96 M138 58 L138 96 M234 58 L234 96 M330 58 L330 96 M426 58 L426 96" fill="none"/>
<text class="sm" x="240" y="110" text-anchor="middle">stderr (fd 2) bypasses the pipe and reaches the terminal unless sent to /dev/null</text>
<text class="sm" x="89" y="22" text-anchor="middle">stdout → stdin</text>
</svg>
<figcaption><b>Figure 8.2</b> A pipeline: five processes, four pipes. Data passes between stages as text lines; error messages travel on the separate stderr stream.</figcaption>
</figure>

**Files and directories.** The file system is one tree rooted at `/`. The directories worth knowing are `/etc` (configuration), `/var/log` (logs), `/proc` and `/sys` (kernel state, [8.14](#s8-14){.ref}), `/tmp` (scratch space) and `/home`. The commands used daily are few: `ls -lah`, `cd`, `pwd`, `cp`, `mv`, `rm`, `mkdir -p`, `cat`, `less`, `head`, `tail -f` (follow a growing log), `find / -name '*.conf' -mtime -1`, `wc -l`, and `df -h` and `du -sh * | sort -h` for disk space.

**Permissions.** Each file has an owner, a group and three permission triplets: read (4), write (2) and execute (1) for the *user*, the *group* and *others*. The first character of `ls -l` gives the type (`-` file, `d` directory, `l` link). For a directory, *execute* means "may enter" and *write* means "may create or delete entries". Octal digits add the bit values, so `-rwxr-x---` is 7 5 0 (Figure 8.3), set with `chmod 750 file`.

<figure>
<svg viewBox="0 0 480 100" width="480">
<text class="mono" x="40" y="22" font-size="14">-</text><text class="mono" x="110" y="22" font-size="14">r w x</text><text class="mono" x="210" y="22" font-size="14">r - x</text><text class="mono" x="310" y="22" font-size="14">- - -</text>
<text class="sm" x="40" y="38" text-anchor="start">type</text><text class="sm" x="108" y="38">user (owner)</text><text class="sm" x="208" y="38">group</text><text class="sm" x="308" y="38">others</text>
<text class="mono" x="110" y="62">4 + 2 + 1 = 7</text><text class="mono" x="210" y="62">4 + 0 + 1 = 5</text><text class="mono" x="310" y="62">0 + 0 + 0 = 0</text>
<rect class="hl" x="104" y="68" width="18" height="14"/><text class="mono" x="106" y="79">7</text><rect class="hl" x="204" y="68" width="18" height="14"/><text class="mono" x="206" y="79">5</text><rect class="hl" x="304" y="68" width="18" height="14"/><text class="mono" x="306" y="79">0</text>
<text class="sm" x="360" y="79">chmod 750 file</text>
</svg>
<figcaption><b>Figure 8.3</b> The mode string <span style="font-family:monospace">-rwxr-x---</span> decoded. Octal 750 means the owner may read, write and execute, the group may read and execute, and everyone else has no access.</figcaption>
</figure>

Three special bits exist. The *setuid* bit (4000) makes a program run with its owner's identity (`passwd` needs it); *setgid* (2000) does the same for the group and, on a directory, makes new files inherit the group; the *sticky* bit (1000) on a directory allows a user to delete only their own entries, which is why `/tmp` shows as `drwxrwxrwt`. A process that needs privilege runs through `sudo`, which logs the command.

**Processes and job control.** `ps aux` lists all processes and `top` or `htop` shows them live. A command started with `&` runs in the background; `Ctrl-Z` suspends the foreground job, `bg` resumes it in the background, `fg` brings it back, `jobs` lists them. `kill PID` sends SIGTERM, which the program may handle in order to exit cleanly; `kill -9` sends SIGKILL, which cannot be caught and leaves no chance to clean up, so it is a last resort ([7.9](#s7-9){.ref}). `nohup cmd &` or a `tmux` session keeps work alive after the terminal closes, which matters over a flaky SSH link.

::: trap
*Claim:* "`kill -9` is the proper way to stop a process." *Why it is wrong:* SIGKILL gives the process no chance to flush buffers, remove lock files or close connections cleanly. *Correct statement:* send SIGTERM first, wait, and use SIGKILL only if the process ignores it.
:::

::: check
1. What does `cmd > out.txt 2>&1` do, and why does `cmd 2>&1 > out.txt` differ? [^c82-1]
2. A file has mode 640. Who can read it? [^c82-2]
:::

[^c82-1]: The first sends stdout to the file and then points stderr at the same place; the second points stderr at the old stdout (the terminal) before stdout moves, so errors still reach the screen.
[^c82-2]: The owner (read and write) and the group (read); others have no access.

## [8.3]{.sec}Text processing for log hunting [Must · ■■□]{.tag} {#s8-3}

Logs are text, one event per line, so a few tools answer most operational questions. *grep* filters lines, *awk* treats each line as columns, *sed* edits streams, and *cut*, *sort*, *uniq* and *wc* slice and count. For structured data from an API, *jq* does the same for JSON. The analogy is a sieve, a spreadsheet and a find-and-replace; the skill is combining them in a pipeline.

The examples use two files from Campus Net: `access.log`, the combined-format log of the student portal's web server, and `syslog.txt`, the switch log of `sw-core1`. Each line of the web log is split by *awk* on whitespace into numbered fields (Figure 8.4): `$1` is the client, `$4` the timestamp, `$7` the path, `$9` the status and `$10` the bytes; `$NF` is always the last field.

<figure>
<svg viewBox="0 0 480 96" width="480">
<text class="mono" x="4" y="40">10.20.1.15 - - [29/Oct/2026:09:01:19 +0530] "GET /portal/grades HTTP/1.1" 500 311</text>
<g class="sm"><text x="4" y="22">$1</text><text x="180" y="22">$4</text><text x="230" y="22">$5</text><text x="262" y="22">$6</text><text x="300" y="22">$7</text><text x="388" y="22">$8</text><text x="424" y="22">$9</text><text x="448" y="22">$10</text></g>
<g class="sm"><text x="4" y="58">client</text><text x="176" y="58">time</text><text x="258" y="58">method</text><text x="300" y="58">path</text><text x="418" y="58">status</text><text x="446" y="58">bytes</text></g>
<path class="acc" d="M418 44 L418 30" fill="none"/><path class="acc" d="M4 44 L4 30" fill="none"/>
<text class="sm" x="4" y="84">awk -F'"' splits on the quote instead, so $2 is the whole request line; $NF is the last field (the byte count here).</text>
</svg>
<figcaption><b>Figure 8.4</b> A web-log line as awk sees it. Fields are separated by runs of blanks; the quoted request counts as three fields (<span style="font-family:monospace">$6 $7 $8</span>) unless the separator is changed with <span style="font-family:monospace">-F</span>.</figcaption>
</figure>

**grep** selects lines. The options worth memorising are `-E` (extended regular expressions), `-v` (invert), `-c` (count), `-o` (print only the match), `-i`, `-n`, `-r`, and `-A`/`-B`/`-C n` for context lines around a match, which is how one sees what happened *before* an error.

```
$ grep -c 'changed state to down' syslog.txt
5
$ grep -B1 -A1 'Gi1/0/7' syslog.txt            # context around one port
Oct 29 09:00:33 sw-core1 %LINEPROTO-5-UPDOWN: Line protocol on Interface Gi1/0/12, changed state to up
Oct 29 09:01:02 sw-core1 %LINEPROTO-5-UPDOWN: Line protocol on Interface Gi1/0/7, changed state to down
Oct 29 09:01:05 sw-core1 %LINEPROTO-5-UPDOWN: Line protocol on Interface Gi1/0/12, changed state to down
$ grep -oE 'Gi[0-9/]+' syslog.txt | sort | uniq -c
      8 Gi1/0/12
      1 Gi1/0/3
      1 Gi1/0/7
```

**awk** reads a line, splits it into fields, and runs `pattern { action }` for every line; `BEGIN` and `END` blocks run before and after. Variables need no declaration, arrays are associative, and `NR` is the line number. This is enough for a "group by" query.

```
$ awk '$9 >= 500 {print $1, $7, $9}' access.log        # server errors only
10.20.1.15 /portal/grades 500
10.20.4.31 /portal/grades 502
10.20.4.31 /portal/grades 502
$ awk '{c[$9]++} END {for (s in c) print s, c[s]}' access.log | sort    # status histogram
200 5
302 1
304 1
500 1
502 2
$ awk '{b[$1]+=$10} END {for (i in b) print b[i], i}' access.log | sort -rn | head -2   # bytes per client
10551 10.20.1.15
2736 10.20.7.9
```

::: example
**Which switch ports flapped more than three times?** The `%LINEPROTO-5-UPDOWN` message is logged each time a port changes state, so a flapping port produces many "down" lines.

1. Keep only the down events: `grep 'LINEPROTO.*to down' syslog.txt`.
2. The port is the tenth field, `Gi1/0/12,`, with a trailing comma, which `sub()` removes: `awk '{sub(/,/,"",$10); print $10}'`.
3. Count per port with an array, and print those over the threshold in the `END` block.

```
$ grep 'LINEPROTO.*to down' syslog.txt \
    | awk '{sub(/,/,"",$10); n[$10]++} END {for (p in n) if (n[p] > 3) print p, n[p]}'
Gi1/0/12 4
```

[Result: Gi1/0/12 went down four times in under two minutes; Gi1/0/7 went down once. For the last hour, add a time filter on `$3` before the count.]{.result}
:::

**sed** applies edit commands to a stream. The commonest is substitution, `s/old/new/`, with `g` to replace every match on a line; with `-n` and the `p` flag it prints only the lines that matched, and `-i` edits a file in place. **cut** extracts columns by delimiter (`cut -d: -f1 /etc/passwd`), **sort** orders lines (`-n` numeric, `-r` reverse, `-h` human sizes, `-u` unique, `-k2` by column), and **uniq -c** counts *adjacent* repeats, which is why it must follow a `sort`.

```
$ sed -n 's/.*Interface \([^,]*\),.*to \(up\|down\)$/\1 \2/p' syslog.txt | head -3
Gi1/0/12 down
Gi1/0/12 up
Gi1/0/3 up
$ sed 's/10\.20\.\([0-9]*\)\.[0-9]*/10.20.\1.x/g' access.log | head -1      # anonymise last octet
10.20.1.x - - [29/Oct/2026:09:01:12 +0530] "GET /portal/login HTTP/1.1" 200 5120 "-" "Mozilla/5.0"
```

**jq** filters JSON. A dot selects a key, `.[]` iterates an array, `select(...)` filters, `-r` removes quotes from strings, and `@csv` formats a row. Network APIs (controllers, cloud CLIs, `ip -j`) return JSON, so `jq` joins the same pipelines.

```
$ jq -r '.interfaces[] | select(.in_errors>0) | "\(.name) \(.in_errors)"' ifaces.json
Gi1/0/12 412
Gi1/0/3 3
$ ip -j -br a | jq -r '.[] | "\(.ifname) \(.addr_info[0].local)"'     # structured output from iproute2
```

::: trap
*Claim:* "`sort | uniq -c` counts the distinct values wherever they appear." *Why it is wrong:* `uniq` compares only neighbouring lines, so unsorted input yields several small counts for the same value. *Correct statement:* always `sort` first (or use an awk array, which needs no ordering). Further, `grep` with an unquoted pattern lets the shell expand `*` and `$` before grep sees them; quote patterns in single quotes.
:::

::: lab
`LAB 8.1 · 30 MIN` Log-hunting dojo. Save the two sample logs shown above (or any nginx log and switch syslog) and write one pipeline for each question.

```
1. Which client sent the most bytes?          (awk array, sort -rn)
2. What share of requests failed with 5xx?    (awk END with printf "%.0f%%")
3. Which port flapped, and at what times?     (grep, awk '{print $3}')
4. Which URLs returned 502, with counts?      (awk '$9==502', sort, uniq -c)
```

**What you should notice:** each answer is a filter (`grep` or an awk pattern), a grouping (array or `sort | uniq -c`) and a ranking (`sort -rn | head`). Once the three stages are familiar, a new question is a change of one stage, not a new program.
:::

::: check
1. Print the last field of every line of a file. [^c83-1]
2. Why does `grep -c` differ from `grep ... | wc -l` on a file with long lines? [^c83-2]
:::

[^c83-1]: `awk '{print $NF}' file`.
[^c83-2]: It does not: both count matching lines. They differ only for `grep -o`, where `-c` still counts lines, not matches.

## [8.4]{.sec}Bash scripting that survives production [Should · ■■□]{.tag} {#s8-4}

A script is a recipe that a junior colleague can follow at three in the morning. It begins with a *shebang*, `#!/usr/bin/env bash`, which names the interpreter, and runs after `chmod +x`. Bash is the right tool for gluing commands, files and exit codes; the rule of thumb is that a script of more than about fifty lines, or one that needs a real data structure, JSON handling or a network protocol, belongs in Python ([Pillar 10](#ch10){.ref}).

**Variables and quoting.** Assign without spaces (`host=10.0.1.2`) and read with `$host`. The most common production bug is the unquoted expansion: the shell splits an unquoted value on spaces and expands wildcards in it, so `rm -rf $dir/` with an empty `dir` deletes `/`. Always write `"$dir"`. Command output is captured with `$(cmd)`, and arithmetic uses `$(( a + b ))`.

**Conditionals and loops.** Use `[[ ... ]]` in Bash (it does not word-split and supports patterns and `&&`). Tests: `-f` file exists, `-d` directory, `-r` readable, `-s` non-empty, `-z` empty string, `==` string equality, `-eq -lt -gt` for integers.

```bash
if [[ -r "$file" && $count -gt 0 ]]; then echo ok; else echo "bad" >&2; fi

case $state in up) echo good ;; down|dead) echo bad ;; *) echo '?' ;; esac

for h in sw1 sw2 sw3; do ping -c1 -W1 "$h" >/dev/null && echo "$h up"; done
while IFS= read -r line; do echo "got: $line"; done < hosts.txt     # reads a file line by line
for i in {1..5}; do ...; done                                         # brace expansion
```

**Functions and arguments.** A function takes `$1`, `$2`, … like a script does; `$#` is the count, `"$@"` the list of all arguments with each one preserved as a word, and `${1:-default}` supplies a default. `getopts` parses `-c 3 -w 1` style options. A function returns an exit status (`return 1`) and prints its result for the caller to capture.

**Failing loudly.** By default Bash carries on after an error, so a script can report success after it broke. The preamble `set -euo pipefail` changes that: `-e` exits when a command fails, `-u` treats an unset variable as an error, and `-o pipefail` makes a pipeline fail if *any* stage fails (without it the pipeline's status is that of the last stage only). Further, `trap 'rm -f "$tmp"' EXIT` runs clean-up on any exit, and every error message goes to stderr (`>&2`) with a non-zero status, so that cron or a monitor can detect it.

| Bug | Symptom | Fix |
|---|---|---|
| Unquoted `$var` | breaks on spaces; dangerous with `rm` | `"$var"` |
| `[ $x == y ]` with empty `x` | "unary operator expected" | `[[ $x == y ]]` |
| <code>cmd &#124; grep x</code> hides `cmd` failure | script continues after failure | `set -o pipefail` |
| `cd dir; rm *` | deletes in the wrong place if `cd` fails | `cd dir && rm *`, or `set -e` |
| `for f in $(ls)` | splits on spaces | `for f in *` or `find -print0` |
| `while read` in a pipeline | variables lost (subshell) | redirect: `done < file` |
| Reading `$?` too late | wrong status | save it: `rc=$?` |

::: example
**`reach.sh`: report unreachable hosts and fail if any exist.** The script reads a file of hosts, pings each with a timeout, appends one CSV row per host, and exits non-zero if any host was down, so that cron or a monitoring agent can alert on the status alone.

```bash
#!/usr/bin/env bash
# reach.sh - ping every host in a file; log CSV; exit 1 if any is down.
# usage: reach.sh [-c count] [-w secs] [-o out.csv] hosts.txt
set -euo pipefail

count=2 wait=1 out=reach.csv
usage() { echo "usage: ${0##*/} [-c count] [-w secs] [-o out.csv] hosts.txt" >&2; exit 2; }

while getopts ":c:w:o:h" opt; do
  case $opt in
    c) count=$OPTARG ;;
    w) wait=$OPTARG ;;
    o) out=$OPTARG ;;
    *) usage ;;
  esac
done
shift $((OPTIND - 1))
[[ $# -eq 1 && -r $1 ]] || usage
hosts=$1

probe() {                       # probe HOST -> prints "up" or "down"
  if ping -c "$count" -W "$wait" -q "$1" >/dev/null 2>&1; then echo up; else echo down; fi
}

down=0
[[ -s $out ]] || echo "time,host,status" > "$out"
while IFS= read -r host || [[ -n $host ]]; do
  [[ -z $host || $host == \#* ]] && continue      # skip blanks and comments
  state=$(probe "$host")
  printf '%s,%s,%s\n' "$(date -Is)" "$host" "$state" >> "$out"
  if [[ $state == down ]]; then down=$((down + 1)); echo "DOWN  $host" >&2; fi
done < "$hosts"

echo "checked $(grep -cv '^\s*\(#\|$\)' "$hosts") hosts, $down down"
(( down == 0 ))                  # exit status: 0 only if nothing was down
```

```
$ cat hosts.txt
# campus
10.0.1.2
127.0.0.1
192.0.2.77
10.20.99.1
$ ./reach.sh -c1 -w1 hosts.txt; echo "exit=$?"
DOWN  192.0.2.77
DOWN  10.20.99.1
checked 4 hosts, 2 down
exit=1
$ cut -d, -f2,3 reach.csv | tail -4
10.0.1.2,up
127.0.0.1,up
192.0.2.77,down
10.20.99.1,down
```

[Result: the summary line goes to stdout, the failures to stderr, and the exit status carries the verdict. The `|| [[ -n $host ]]` clause keeps a final line that lacks a newline.]{.result}
:::

For a whole subnet the sweep is parallel instead of sequential. Pinging 254 addresses one at a time with a one-second timeout takes over four minutes when most addresses are empty; 32 at a time takes under ten seconds.

```bash
#!/usr/bin/env bash
# sweep.sh 10.20.1 - ping A.B.C.1-254, 32 at a time, print the live hosts
set -euo pipefail
prefix=${1:?usage: sweep.sh A.B.C}
seq 1 254 | xargs -P 32 -I{} sh -c \
  'ping -c1 -W1 -q '"$prefix"'.{} >/dev/null 2>&1 && echo '"$prefix"'.{} || true' | sort -V
```

```
$ ./sweep.sh 10.0.1
10.0.1.1
10.0.1.2
```

Note the `|| true`. Without it `xargs` returns 123 whenever one of the commands fails, and under `set -e` every dead address would abort the script; this fault was found while testing the version above. The second tool is a log summary, which reuses the awk idioms of [8.3](#s8-3){.ref}:

```bash
#!/usr/bin/env bash
# logsum.sh - summarise an nginx/Apache combined-format access log.
set -euo pipefail
top=5
while getopts ":n:" o; do [[ $o == n ]] && top=$OPTARG || { echo "usage: ${0##*/} [-n top] FILE" >&2; exit 2; }; done
shift $((OPTIND - 1))
log=${1:?usage: ${0##*/} [-n top] FILE}
[[ -r $log ]] || { echo "cannot read $log" >&2; exit 2; }

echo "== requests: $(wc -l < "$log")"
echo "== status classes"
awk '{c[substr($9,1,1) "xx"]++} END {for (k in c) printf "%s %d\n", k, c[k]}' "$log" | sort
echo "== top $top clients"
awk '{print $1}' "$log" | sort | uniq -c | sort -rn | head -n "$top"
echo "== paths with 5xx"
awk '$9 ~ /^5/ {print $9, $7}' "$log" | sort | uniq -c | sort -rn | head -n "$top"
```

```
$ ./logsum.sh -n 3 access.log
== requests: 10
== status classes
2xx 5
3xx 2
5xx 3
== top 3 clients
      3 10.20.7.9
      3 10.20.1.15
      2 10.20.4.31
== paths with 5xx
      2 502 /portal/grades
      1 500 /portal/grades
```

**Scheduling.** `cron` runs a command at fixed times. A line `*/5 * * * * /opt/netops/reach.sh /opt/netops/hosts.txt || logger -t reach "hosts down"` runs the check every five minutes and writes to the system log if it fails; note the five time fields (minute, hour, day of month, month, day of week). Cron has a minimal `PATH`, so scripts use absolute paths. The modern alternative is a systemd timer ([8.14](#s8-14){.ref}).

::: lens
[AMAZON NDE · ARISTA · JUNIPER · GOOGLE]{.co}

The usual live task is "read hostnames from a file and report which do not respond". A strong solution quotes every expansion, sets `-euo pipefail`, handles blank lines and comments, takes the file as an argument rather than hard-coding it, prints failures to stderr and returns a non-zero status. Follow-ups: how to make it parallel (`xargs -P`), how to avoid a flood of simultaneous pings, and when to switch to Python (data structures, JSON, retries). The solved version is Q8.8 in the Problem Set.
:::

::: check
1. What does `set -o pipefail` change? [^c84-1]
2. Why write `"$@"` rather than `$@`? [^c84-2]
:::

[^c84-1]: A pipeline returns a failure status if any command in it fails, not only the last.
[^c84-2]: `"$@"` passes each argument as one word, preserving embedded spaces; unquoted `$@` splits them again.

:::
