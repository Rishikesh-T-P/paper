::: {.p8}

## [8.5]{.sec}iproute2 and network namespaces [Must · ■■□]{.tag} {#s8-5}

*iproute2* is the single tool, `ip`, for layer-2 and layer-3 state on Linux. It talks to the kernel over *netlink* sockets and has one object per table: `ip link` (interfaces), `ip addr` (addresses), `ip route` (routing table), `ip neigh` (ARP and neighbour discovery cache), `ip rule` (policy routing), `ip netns` (network namespaces). Each object takes the verbs `show`, `add`, `del`, `set`; options `-br` (brief), `-s` (statistics), `-j` (JSON) and `-n NS` (act inside a namespace) go before the object. The protocols behind these tables are taught in [3.6](#s3-6){.ref} and [4.4](#s4-4){.ref}; this section teaches how to read and change them.

```
$ ip -br a                               # one line per interface: name, state, addresses
lo               UNKNOWN        127.0.0.1/8
r-eth0@if7       UP             10.0.1.2/24
$ ip route
default via 10.0.1.1 dev r-eth0
10.0.1.0/24 dev r-eth0 proto kernel scope link src 10.0.1.2
$ ip route get 10.0.2.2                  # what the kernel WOULD do for this destination
10.0.2.2 via 10.0.1.1 dev r-eth0 src 10.0.1.2 uid 0
```

`ip route show` lists the table, while **`ip route get`** asks the kernel to perform the lookup and reports the chosen next hop, output interface and *source address*. The difference matters because the table may hold several overlapping prefixes, policy rules and a default route; the lookup applies longest-prefix match ([1.9](#s1-9){.ref}) and returns the one that wins. The `proto kernel` line was added automatically when the address was configured, and `scope link` marks a directly connected network.

**Interface counters.** `ip -s link show eth0` prints receive and transmit counters (bytes, packets, errors, drops, overruns). Counters are cumulative since the interface came up, so one reads the *difference* between two snapshots ([8.11](#s8-11){.ref}). The flags in angle brackets matter: `UP` is the administrative state, `LOWER_UP` means the carrier is present, and a port that is `UP` without `LOWER_UP` has no cable or no peer.

```
$ ip -s link show r-eth0
8: r-eth0@if7: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP
    link/ether ee:da:da:f1:92:5d brd ff:ff:ff:ff:ff:ff link-netns rtr
    RX:  bytes packets errors dropped  missed   mcast
           238       3      0       0       0       0
    TX:  bytes packets errors dropped carrier collsns
           434       5      0       0       0       0
```

**The neighbour table.** Before sending to a next hop the host needs its MAC address, which it learns by ARP (IPv4) or Neighbour Discovery (IPv6) and keeps in the *neighbour cache*. Each entry has a state from the Neighbour Unreachability Detection (NUD) machine, and the state is the diagnostic.

| State | Meaning | What it tells you |
|---|---|---|
| `INCOMPLETE` | ARP request sent, no reply yet | resolution in progress; a long stay means no answer |
| `REACHABLE` | confirmed recently (about 30 s) | healthy |
| `STALE` | known but not confirmed lately | normal; used without delay, re-checked on next use |
| `DELAY` | stale entry just used; waiting 5 s for upper-layer proof | transient |
| `PROBE` | unicast ARP probes being sent | transient; reachability being tested |
| `FAILED` | probes unanswered; entry given up | L2 fault: host down, wrong VLAN or subnet, cable |
| `PERMANENT` | set by hand (`ip neigh add … nud permanent`) | static ARP |

```
$ ip neigh flush all; ping -c1 -W1 10.0.1.77       # an address nobody owns
$ ip neigh
10.0.1.77 dev r-eth0 INCOMPLETE                    # no lladdr yet: nobody answered the ARP
$ ping -c1 10.0.1.1 >/dev/null; sleep 40; ip neigh
10.0.1.1 dev r-eth0 lladdr 46:4f:48:75:38:92 STALE # confirmed once, aged out after ~30 s
```

Hence "Destination Host Unreachable" printed by `ping` *from the local address* is not an ICMP message from a router at all: the host itself gave up because ARP failed for an on-link destination. If the same words arrive *from a router's address*, the router had no route.

**Policy routing.** A packet normally consults one table, `main`. `ip rule` adds rules that choose a table by source address, incoming interface, mark or other fields, evaluated in priority order. To send traffic from 10.1.0.0/16 through ISP-B and everything else through ISP-A, one adds a second table with its own default route and a rule that selects it:

```
$ ip route add default via 192.0.2.1 dev p0                        # ISP-A, main table
$ ip route add default via 198.51.100.1 dev p1 table 100           # ISP-B, table 100
$ ip rule add from 10.1.0.0/16 lookup 100 priority 1000
$ ip rule show
0:      from all lookup local
1000:   from 10.1.0.0/16 lookup 100
32766:  from all lookup main
$ ip route get 8.8.8.8
8.8.8.8 via 192.0.2.1 dev p0 src 192.0.2.2
$ ip route get 8.8.8.8 from 10.1.5.5
8.8.8.8 from 10.1.5.5 via 198.51.100.1 dev p1 table 100
```

The rules are checked top to bottom, `local` first (addresses of the host itself), then ours, then `main`. The `ip route get … from` form is the quickest test of a policy. Persisting it across reboots belongs to the network manager (netplan, NetworkManager or `systemd-networkd`), not to the shell.

**Other link types.** The same `ip link add` creates virtual interfaces. A VLAN sub-interface carries one 802.1Q tag ([4.2](#s4-2){.ref}): `ip link add link eth0 name eth0.10 type vlan id 10`. A software bridge acts as a learning switch: `ip link add br0 type bridge` and `ip link set eth0 master br0`. A VRF (`type vrf table 10`) gives a separate routing table per tenant ([4.9](#s4-9){.ref}), and a `veth` pair is a virtual patch cable whose two ends may live in different namespaces.

### Network namespaces and veth

A *network namespace* is an independent copy of the network stack: its own interfaces, addresses, routing table, neighbour cache, firewall rules and `/proc/net`. A process in a namespace sees only those. Containers are built from this idea, and so is every lab in this book. A `veth` pair behaves like a cable with a plug at each end; whatever enters one end leaves the other, so putting the ends in two namespaces joins them. The lab below builds the topology of Figure 8.5, and Campus Net's student VLAN and server VLAN are the two end networks.

<figure>
<svg viewBox="0 0 480 190" width="480"><defs><marker id="a85" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs>
<rect class="box" x="6" y="30" width="130" height="110" rx="12"/><text class="lbl" x="71" y="48" text-anchor="middle">netns red</text>
<rect class="box" x="175" y="30" width="130" height="110" rx="12" style="fill:#F2F3F5"/><text class="lbl" x="240" y="48" text-anchor="middle">netns rtr</text>
<rect class="box" x="344" y="30" width="130" height="110" rx="12"/><text class="lbl" x="409" y="48" text-anchor="middle">netns blue</text>
<line class="ln" x1="136" y1="85" x2="175" y2="85"/><line class="ln" x1="305" y1="85" x2="344" y2="85"/>
<circle class="box" cx="155" cy="85" r="3"/><circle class="box" cx="320" cy="85" r="3"/>
<text class="mono" x="14" y="76">r-eth0</text><text class="mono" x="14" y="88">10.0.1.2/24</text>
<text class="sm" x="14" y="104">default via 10.0.1.1</text>
<text class="mono" x="182" y="70">rt-eth0 .1</text><text class="mono" x="182" y="82">10.0.1.1/24</text>
<text class="mono" x="182" y="100">rt-eth1 .1</text><text class="mono" x="182" y="112">10.0.2.1/24</text>
<text class="sm" x="182" y="128">ip_forward = 1</text>
<text class="mono" x="352" y="76">b-eth0</text><text class="mono" x="352" y="88">10.0.2.2/24</text>
<text class="sm" x="352" y="104">default via 10.0.2.1</text>
<text class="sm" x="155" y="70" text-anchor="middle">veth</text><text class="sm" x="320" y="70" text-anchor="middle">veth</text>
<path class="acc" d="M70 150 L70 170 L409 170 L409 150" fill="none" marker-end="url(#a85)"/><text class="sm" x="240" y="183" text-anchor="middle">ping 10.0.2.2 from red: forwarded by rtr, TTL 64 → 63</text>
</svg>
<figcaption><b>Figure 8.5</b> The three-namespace lab. Each rounded box has private interfaces and routing tables; the two veth pairs are the cables. Without forwarding enabled in <span style="font-family:monospace">rtr</span> the middle box drops transit packets.</figcaption>
</figure>

::: lab
`LAB 8.2 · 40 MIN` Two end hosts and a router, built with namespaces (run as root; nothing needs a hypervisor).

```
ip netns add red; ip netns add blue; ip netns add rtr
ip link add r-eth0 type veth peer name rt-eth0       # cable 1
ip link add b-eth0 type veth peer name rt-eth1       # cable 2
ip link set r-eth0 netns red;  ip link set rt-eth0 netns rtr
ip link set b-eth0 netns blue; ip link set rt-eth1 netns rtr
ip -n red  addr add 10.0.1.2/24 dev r-eth0; ip -n red  link set r-eth0 up
ip -n blue addr add 10.0.2.2/24 dev b-eth0; ip -n blue link set b-eth0 up
ip -n rtr  addr add 10.0.1.1/24 dev rt-eth0; ip -n rtr addr add 10.0.2.1/24 dev rt-eth1
ip -n rtr  link set rt-eth0 up;  ip -n rtr link set rt-eth1 up
ip -n red  route add default via 10.0.1.1
ip -n blue route add default via 10.0.2.1
```

Now test, then break and repair things one at a time.

```
$ ip netns exec rtr sysctl net.ipv4.ip_forward
net.ipv4.ip_forward = 0
$ ip netns exec red ping -c2 -W1 10.0.2.2
2 packets transmitted, 0 received, 100% packet loss
$ ip netns exec rtr sysctl -w net.ipv4.ip_forward=1
$ ip netns exec red ping -c2 -W1 10.0.2.2
64 bytes from 10.0.2.2: icmp_seq=1 ttl=63 time=0.556 ms
```

Breakages to try: (i) delete the default route in `red`; (ii) remove the address from `rt-eth1`; (iii) `ip -n red neigh add 10.0.1.1 lladdr 02:00:00:00:00:99 dev r-eth0 nud permanent` (a wrong static ARP entry); (iv) re-disable forwarding. For each, write down the symptom of `ping`, `ip route get 10.0.2.2` and `ip neigh`.

**What you should notice:** with forwarding off, `red` reaches the router (10.0.1.1 answers) but not `blue`, so the fault is in the router and not in `red`. TTL 63 in the reply confirms exactly one router hop. A wrong static ARP entry makes ping fail although every route is correct; `ip neigh` exposes it.
:::

**Containers.** Docker and Kubernetes use the same machinery. Each container gets its own namespace, one end of a veth pair is moved inside, the other end is attached to a host bridge (`docker0`, itself an `ip link … type bridge`), and an iptables MASQUERADE rule on the host rewrites container source addresses on the way out ([8.12](#s8-12){.ref}). Published ports (`-p 8080:80`) are DNAT rules in the same tables. Hence a container's "network problem" is diagnosed with `nsenter -t PID -n ip a`, `ip route`, `ss` and `tcpdump` on the veth, exactly as above.

::: trap
*Claim:* "`ip addr add` makes the address permanent." *Why it is wrong:* the command changes the running kernel only; a reboot, a link flap handled by a network manager, or a DHCP renewal discards it. *Correct statement:* test with `ip`, then write the setting in netplan, NetworkManager or `systemd-networkd`. The same applies to routes and to `sysctl -w` ([8.13](#s8-13){.ref}).
:::

::: check
1. A host's `ip neigh` shows the gateway as `FAILED`. Which layer is suspect? [^c85-1]
2. What does `ip route get 8.8.8.8` print that `ip route` does not? [^c85-2]
:::

[^c85-1]: Layer 2: ARP received no reply, so look at the cable, VLAN, subnet mask or whether the gateway is up.
[^c85-2]: The route actually selected after policy rules and longest-prefix match, with the output interface and the source address the kernel would use.

## [8.6]{.sec}Sockets on the wire: ss [Must · ■■□]{.tag} {#s8-6}

`ss` (socket statistics) lists the kernel's socket table through the `sock_diag` netlink interface; it replaced `netstat`, which parsed `/proc/net/tcp` and became slow with many connections. A socket is the endpoint of a conversation ([7.10](#s7-10){.ref}); `ss` shows its state, queues, addresses and, with options, the process that owns it and the internals of its TCP connection. The TCP state machine is drawn in [3.9](#s3-9){.ref}; here each state is a row in a table.

| Option | Meaning |
|---|---|
| `-t` `-u` `-x` | TCP, UDP, Unix sockets |
| `-l` / `-a` | listening only / all states |
| `-n` | numeric ports and addresses; without it every line causes a DNS or services lookup |
| `-p` | owning process (needs root for other users' sockets) |
| `-i` | TCP internals: rtt, cwnd, retransmissions |
| `-e` `-m` | extended info; socket memory |
| `-s` | summary counts by state |
| `state X` / `dport = :443` | filter expressions |

The first question on any host is *who is listening, on which address*. The mnemonic is `ss -tulpn` (TCP, UDP, listening, process, numeric).

```
$ ss -tlnp
State  Recv-Q Send-Q Local Address:Port Peer Address:Port Process
LISTEN 0      5           10.0.2.2:8080     0.0.0.0:*     users:(("python3",pid=21426,fd=3))
```

The local address is the diagnosis. `10.0.2.2:8080` accepts connections only to that address; `127.0.0.1:5000` accepts only local clients, so a Flask or Node server started in development mode "works on my machine and nowhere else" until it binds `0.0.0.0` (all IPv4 addresses) or `[::]`. For a listening socket `Recv-Q` is the current accept queue length and `Send-Q` its maximum (the `backlog`); a `Recv-Q` equal to `Send-Q` means the application is not calling `accept()` fast enough and new connections are being dropped. For an established socket `Recv-Q` is unread data and `Send-Q` is unacknowledged data.

**States as signals.** Each connection moves through the TCP states ([3.9](#s3-9){.ref}). Counting them with `ss -tan | awk 'NR>1{c[$1]++} END{for(s in c) print s,c[s]}'` summarises a host's health.

| State | Normal? | Signals |
|---|---|---|
| `LISTEN` | yes | server waiting; check bind address |
| `SYN-SENT` | brief | client waited for SYN-ACK; many for long means filtered port or dead peer |
| `SYN-RECV` | brief | half-open; a pile suggests SYN flood or a full accept queue |
| `ESTAB` | yes | data phase |
| `FIN-WAIT-2` | brief | we closed, waiting for the peer's FIN; the peer has not closed yet |
| `TIME-WAIT` | yes | on the side that closed first; lasts 60 s on Linux (2 × MSL), protecting against old segments |
| `CLOSE-WAIT` | **no** | peer closed, our application has not called `close()`: a program bug |
| `LAST-ACK` | brief | we sent our FIN after CLOSE-WAIT, waiting for the final ACK |

The two halves of a close show clearly in one experiment on a single host: the server side closes first, so it enters `FIN-WAIT-2` and then `TIME-WAIT`, while the other end stays in `CLOSE-WAIT` until its program closes.

```
$ ss -tan | grep :9                                   # server closed its end first
LISTEN     0      1           10.0.1.2:9          0.0.0.0:*
CLOSE-WAIT 1      0           10.0.1.2:43508     10.0.1.2:9           <- client has not called close()
FIN-WAIT-2 0      0           10.0.1.2:9         10.0.1.2:43508       <- server waits for client's FIN
$ ss -tan | grep :9                                   # after the client's close()
TIME-WAIT  0      0           10.0.1.2:9         10.0.1.2:43508       <- the first closer waits 60 s
```

`CLOSE-WAIT` entries never disappear by themselves, because the kernel is waiting for the application; thousands of them mean a descriptor leak (a missing `close()` on an error path), and the fix is in the code, not in the network. `TIME-WAIT` is not a leak: it is the price of reliable closing, paid by whichever side closes first. A busy HTTP/1.0 server, which closes after every response, therefore shows many `TIME-WAIT` entries on the *server*, and a client making many short connections shows them on the *client*, where they can exhaust ephemeral ports.

**Filtering.** `ss -tan state established '( dport = :443 or sport = :443 )'`, `ss -tn dst 10.0.2.0/24`, and `ss -tan state time-wait | wc -l` select by state, port or address. The summary `ss -s` prints totals, which is a quick check for a connection explosion.

**TCP internals.** With `-i`, `ss` prints the kernel's own measurements for each connection ([3.9](#s3-9){.ref} explains what they control).

```
$ ss -tin dst 10.0.2.2
State      Recv-Q Send-Q Local Address:Port  Peer Address:Port
CLOSE-WAIT 11118  0           10.0.1.2:48232     10.0.2.2:8080
	 bbr wscale:10,10 rto:204 rtt:0.066/0.036 ato:40 mss:1448 pmtu:1500 cwnd:11
	 bytes_sent:18 bytes_received:11118 segs_out:7 segs_in:12 send 1930666667bps
	 pacing_rate 4534978280bps delivery_rate 482666664bps app_limited minrtt:0.024
```

| Field | Reading |
|---|---|
| `bbr` / `cubic` | congestion-control algorithm in use |
| `rtt:0.066/0.036` | smoothed RTT / mean deviation, in milliseconds |
| `rto:204` | retransmission timeout, ms (minimum 200 ms on Linux) |
| `mss`, `pmtu` | segment size negotiated; path MTU known |
| `cwnd:11` | congestion window in segments; with `mss` gives bytes in flight allowed |
| `retrans:0/3` (when present) | retransmits in flight / total; rising total means loss |
| `send`, `delivery_rate` | window-limited rate / measured goodput |
| `app_limited` | the application, not the network, is the limit |
| `rwnd_limited`, `snd_wnd` | the receiver's window is the limit (zero-window problems) |

Reading it is a short argument. High `rtt` with small `cwnd` and repeated `retrans` points to loss; small `rtt`, large `cwnd` and `app_limited` points to a slow application; `rwnd_limited` points to the receiver. The same fields are drawn as a Stevens graph in Wireshark ([8.8](#s8-8){.ref}).

::: lab
`LAB 8.3 · 30 MIN` The socket safari. Write a short Python server and client (or reuse the echo programs of [7.10](#s7-10){.ref}), and make `ss` show each of the states LISTEN, ESTAB, FIN-WAIT-2, CLOSE-WAIT and TIME-WAIT.

```
$ python3 -m http.server 8080 --bind 127.0.0.1 &
$ ss -tlnp | grep 8080                 # LISTEN, and the bind address
$ curl -s localhost:8080 >/dev/null; ss -tan state time-wait    # HTTP/1.0 server closes first
```

Then open a connection from Python, read the reply but do not call `close()`, and run `ss -tan state close-wait`.

**What you should notice:** which side is in TIME-WAIT depends only on who closed first, and CLOSE-WAIT appears on the side that has *received* a FIN but not yet closed. Binding to `127.0.0.1` makes the same server unreachable from another host with no change of firewall.
:::

::: check
1. `ss -tlnp` shows `127.0.0.1:5000` for a web app. Can a remote client connect? [^c86-1]
2. Which state accumulates when an application forgets `close()`? [^c86-2]
:::

[^c86-1]: No. The socket accepts only connections addressed to the loopback address; bind `0.0.0.0` or the interface address.
[^c86-2]: `CLOSE-WAIT`, on the side that received the peer's FIN.

:::
