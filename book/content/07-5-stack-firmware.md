::: {.p7}

## [7.12]{.sec}The Linux receive path: NIC to recv() [Must · ■■■]{.tag} {#s7-12}

Networking employers ask this section's question in many forms: "how does a packet get from the wire to the application?" The answer joins everything before it: DMA, interrupts, softirqs, the memory allocator, the protocol layers and the socket. We follow one TCP segment through a Linux host and then name where the common acceleration techniques attach.

::: bigidea
The Linux receive path is a pipeline in which the hardware fills memory by DMA, a single interrupt starts a batched polling loop, and each packet is carried through the stack as one metadata object, the `sk_buff`, so that no layer copies the payload until the application reads it.
:::

<figure>
<svg viewBox="0 0 480 190" width="480"><defs><marker id="inp" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="anp" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><text class="lbl" x="6" y="20" text-anchor="start">low load: interrupt per packet</text><line class="lg" x1="120" y1="44" x2="460" y2="44" /><text class="lbl" x="6" y="80" text-anchor="start">high load: interrupt per packet</text><line class="lg" x1="120" y1="104" x2="460" y2="104" /><text class="lbl" x="6" y="140" text-anchor="start">high load: NAPI</text><line class="lg" x1="120" y1="164" x2="460" y2="164" /><line class="ln" x1="150" y1="44" x2="150" y2="24" /><line class="ln" x1="250" y1="44" x2="250" y2="24" /><line class="ln" x1="370" y1="44" x2="370" y2="24" /><line class="ln" x1="430" y1="44" x2="430" y2="24" /><line class="ln" x1="120" y1="104" x2="120" y2="84" /><line class="ln" x1="129" y1="104" x2="129" y2="84" /><line class="ln" x1="138" y1="104" x2="138" y2="84" /><line class="ln" x1="147" y1="104" x2="147" y2="84" /><line class="ln" x1="156" y1="104" x2="156" y2="84" /><line class="ln" x1="165" y1="104" x2="165" y2="84" /><line class="ln" x1="174" y1="104" x2="174" y2="84" /><line class="ln" x1="183" y1="104" x2="183" y2="84" /><line class="ln" x1="192" y1="104" x2="192" y2="84" /><line class="ln" x1="201" y1="104" x2="201" y2="84" /><line class="ln" x1="210" y1="104" x2="210" y2="84" /><line class="ln" x1="219" y1="104" x2="219" y2="84" /><line class="ln" x1="228" y1="104" x2="228" y2="84" /><line class="ln" x1="237" y1="104" x2="237" y2="84" /><line class="ln" x1="246" y1="104" x2="246" y2="84" /><line class="ln" x1="255" y1="104" x2="255" y2="84" /><line class="ln" x1="264" y1="104" x2="264" y2="84" /><line class="ln" x1="273" y1="104" x2="273" y2="84" /><line class="ln" x1="282" y1="104" x2="282" y2="84" /><line class="ln" x1="291" y1="104" x2="291" y2="84" /><line class="ln" x1="300" y1="104" x2="300" y2="84" /><line class="ln" x1="309" y1="104" x2="309" y2="84" /><line class="ln" x1="318" y1="104" x2="318" y2="84" /><line class="ln" x1="327" y1="104" x2="327" y2="84" /><line class="ln" x1="336" y1="104" x2="336" y2="84" /><line class="ln" x1="345" y1="104" x2="345" y2="84" /><line class="ln" x1="354" y1="104" x2="354" y2="84" /><line class="ln" x1="363" y1="104" x2="363" y2="84" /><line class="ln" x1="372" y1="104" x2="372" y2="84" /><line class="ln" x1="381" y1="104" x2="381" y2="84" /><line class="ln" x1="390" y1="104" x2="390" y2="84" /><line class="ln" x1="399" y1="104" x2="399" y2="84" /><line class="ln" x1="408" y1="104" x2="408" y2="84" /><line class="ln" x1="417" y1="104" x2="417" y2="84" /><line class="ln" x1="426" y1="104" x2="426" y2="84" /><line class="ln" x1="435" y1="104" x2="435" y2="84" /><line class="ln" x1="444" y1="104" x2="444" y2="84" /><line class="ln" x1="453" y1="104" x2="453" y2="84" /><rect class="hl" x="140" y="138" width="255" height="16" rx="0" style="fill:#FFF4C2;stroke:#9AA0A6;stroke-width:.7"/><text class="lbl" x="267.5" y="149.0" text-anchor="middle"></text><text class="sm" x="268" y="150" text-anchor="middle">polling: IRQ masked, packets batched</text><line class="acc" x1="140" y1="164" x2="140" y2="134" marker-end="url(#anp)" /><line class="ln" x1="395" y1="164" x2="395" y2="134" marker-end="url(#inp)" /><text class="sm" x="140" y="178" text-anchor="middle">first IRQ</text><text class="sm" x="395" y="178" text-anchor="middle">queue empty: IRQ on</text><text class="sm" x="290" y="72" text-anchor="middle">one interrupt every packet: the CPU does nothing else</text></svg>
<figcaption><b>Figure 7.20</b> Interrupt per packet and NAPI. Under high load NAPI replaces thousands of interrupts with one interrupt and one polling window.</figcaption>
</figure>

### The nine steps

1. **DMA.** The NIC receives a frame, checks its CRC, and writes it by DMA into a buffer that a descriptor in the RX ring ([7.8](#s7-8){.ref}) points at, then marks the descriptor complete.
2. **Interrupt.** The NIC raises an MSI-X interrupt, normally one per RX queue, each bound to a core. The driver's ISR does almost nothing: it calls `napi_schedule()` and *masks* further interrupts from that queue.
3. **Softirq.** On return from the interrupt, the kernel runs the `NET_RX` softirq, whose handler `net_rx_action()` calls the driver's `poll()` function.
4. **Poll with a budget.** `poll()` takes completed descriptors from the ring, up to its *budget* (64 packets per call by default; `net.core.netdev_budget`, default 300, bounds one softirq run across devices). For each packet it builds an `sk_buff` and sets its protocol. If fewer packets than the budget were waiting, the ring is empty: the driver calls `napi_complete_done()` and re-enables the interrupt. If the budget was used up, polling continues without any new interrupt.
5. **GRO.** `napi_gro_receive()` merges consecutive segments of the same flow into one larger `sk_buff`, so that the upper layers run once for many packets.
6. **Link layer to IP.** `__netif_receive_skb_core()` hands the packet first to taps (`AF_PACKET` sockets; this is where `tcpdump` sees it), then to the protocol handler for its EtherType: `ip_rcv()`.
7. **IP.** The netfilter `PREROUTING` hook runs; a route lookup finds the destination local; `ip_local_deliver()` runs the `INPUT` hook and passes the packet to the transport protocol.
8. **TCP.** `tcp_v4_rcv()` finds the socket from the four-tuple, `tcp_rcv_established()` handles sequence numbers, ACKs and the window ([Pillar 3](#ch3){.ref} covers what these do), and the data is appended to the socket's receive queue. A process sleeping in `recv()`, or in `epoll_wait()` on this socket, is made runnable.
9. **User copy.** When the process runs, `recv()` enters `tcp_recvmsg()`, which copies the bytes from the `sk_buff`s into the user's buffer (`copy_to_user`) and frees them. This is the one copy of the payload on the receive path.

<figure>
<svg viewBox="0 0 480 372" width="480"><defs><marker id="irx" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="arx" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><rect class="fill" x="6" y="4" width="468" height="62" rx="0"/><text class="lbl" x="240.0" y="38.0" text-anchor="middle"></text><text class="sm" x="12" y="14" text-anchor="start">HARDWARE</text><rect class="fill" x="6" y="70" width="468" height="44" rx="0"/><text class="lbl" x="240.0" y="95.0" text-anchor="middle"></text><text class="sm" x="12" y="80" text-anchor="start">HARD IRQ</text><rect class="fill" x="6" y="118" width="468" height="128" rx="0"/><text class="lbl" x="240.0" y="185.0" text-anchor="middle"></text><text class="sm" x="12" y="128" text-anchor="start">SOFTIRQ (NET_RX), BUDGET 64 PER POLL</text><rect class="fill" x="6" y="250" width="468" height="54" rx="0"/><text class="lbl" x="240.0" y="280.0" text-anchor="middle"></text><text class="sm" x="12" y="260" text-anchor="start">SOCKET</text><rect class="fill" x="6" y="308" width="468" height="56" rx="0"/><text class="lbl" x="240.0" y="339.0" text-anchor="middle"></text><text class="sm" x="12" y="318" text-anchor="start">USER SPACE</text><rect class="box" x="16" y="18" width="90" height="40" rx="0"/><text class="lbl" x="61.0" y="37.0" text-anchor="middle">NIC</text><text class="sm" x="61.0" y="46.0" text-anchor="middle">frame to RX FIFO</text><rect class="box" x="140" y="18" width="150" height="40" rx="0"/><text class="lbl" x="215.0" y="37.0" text-anchor="middle">RX descriptor ring</text><text class="sm" x="215.0" y="46.0" text-anchor="middle">DMA writes into buffers</text><line class="ln" x1="106" y1="38" x2="138" y2="38" marker-end="url(#irx)" /><text class="sm" x="122" y="33" text-anchor="middle">DMA</text><rect class="box dash" x="330" y="18" width="130" height="40" rx="0" style="fill:#FFF4C2"/><text class="lbl" x="395.0" y="37.0" text-anchor="middle">XDP (native)</text><text class="sm" x="395.0" y="46.0" text-anchor="middle">in the driver, before sk_buff</text><line class="lg" x1="290" y1="38" x2="328" y2="38" /><rect class="box" x="16" y="84" width="130" height="24" rx="0"/><text class="lbl" x="81.0" y="99.0" text-anchor="middle">MSI-X interrupt</text><rect class="box" x="176" y="84" width="280" height="24" rx="0"/><text class="mono" x="316.0" y="99.0" text-anchor="middle">driver ISR: napi_schedule(), mask the IRQ</text><line class="ln" x1="146" y1="96" x2="174" y2="96" marker-end="url(#irx)" /><line class="ln" x1="60" y1="58" x2="60" y2="82" marker-end="url(#irx)" /><rect class="box" x="16" y="130" width="130" height="26" rx="0"/><text class="mono" x="81.0" y="146.0" text-anchor="middle">net_rx_action()</text><rect class="box" x="176" y="130" width="130" height="26" rx="0"/><text class="mono" x="241.0" y="146.0" text-anchor="middle">driver poll()</text><rect class="box" x="336" y="130" width="130" height="26" rx="0"/><text class="mono" x="401.0" y="146.0" text-anchor="middle">build sk_buff</text><line class="ln" x1="146" y1="143" x2="174" y2="143" marker-end="url(#irx)" /><line class="ln" x1="306" y1="143" x2="334" y2="143" marker-end="url(#irx)" /><rect class="box" x="16" y="172" width="130" height="26" rx="0"/><text class="mono" x="81.0" y="188.0" text-anchor="middle">napi_gro_receive()</text><rect class="box" x="176" y="172" width="130" height="26" rx="0"/><text class="mono" x="241.0" y="188.0" text-anchor="middle">netif_receive_skb</text><rect class="box" x="336" y="172" width="130" height="26" rx="0" style="fill:#FFF4C2"/><text class="mono" x="401.0" y="184.0" text-anchor="middle">AF_PACKET taps</text><text class="sm" x="401.0" y="193.0" text-anchor="middle">tcpdump sees it here</text><path class="ln" d="M400,156 L400,164 L80,164 L80,170" marker-end="url(#irx)" /><line class="ln" x1="146" y1="185" x2="174" y2="185" marker-end="url(#irx)" /><line class="lg" x1="306" y1="185" x2="334" y2="185" /><rect class="box" x="16" y="212" width="90" height="26" rx="0"/><text class="mono" x="61.0" y="228.0" text-anchor="middle">ip_rcv()</text><rect class="box" x="120" y="212" width="110" height="26" rx="0" style="fill:#FFF4C2"/><text class="mono" x="175.0" y="228.0" text-anchor="middle">netfilter hooks</text><rect class="box" x="244" y="212" width="110" height="26" rx="0"/><text class="mono" x="299.0" y="228.0" text-anchor="middle">route: local</text><rect class="box" x="368" y="212" width="98" height="26" rx="0"/><text class="mono" x="417.0" y="228.0" text-anchor="middle">tcp_v4_rcv()</text><path class="ln" d="M240,198 L240,204 L60,204 L60,210" marker-end="url(#irx)" /><line class="ln" x1="106" y1="225" x2="118" y2="225" marker-end="url(#irx)" /><line class="ln" x1="230" y1="225" x2="242" y2="225" marker-end="url(#irx)" /><line class="ln" x1="354" y1="225" x2="366" y2="225" marker-end="url(#irx)" /><rect class="box" x="16" y="266" width="200" height="30" rx="0"/><text class="mono" x="116.0" y="284.0" text-anchor="middle">socket lookup, tcp_rcv_established()</text><rect class="box" x="260" y="266" width="206" height="30" rx="0" style="fill:#FFF4C2"/><text class="mono" x="363.0" y="284.0" text-anchor="middle">sk_receive_queue; wake waiter</text><path class="ln" d="M416,238 L416,252 L116,252 L116,264" marker-end="url(#irx)" /><line class="acc" x1="216" y1="281" x2="258" y2="281" marker-end="url(#arx)" /><rect class="box" x="16" y="324" width="150" height="30" rx="0"/><text class="mono" x="91.0" y="342.0" text-anchor="middle">recv() / epoll_wait()</text><rect class="box" x="210" y="324" width="256" height="30" rx="0"/><text class="mono" x="338.0" y="342.0" text-anchor="middle">tcp_recvmsg(): copy_to_user()</text><path class="acc" d="M363,296 L363,318 L88,318 L88,322" marker-end="url(#arx)" /><line class="ln" x1="210" y1="339" x2="168" y2="339" marker-end="url(#irx)" /></svg>
<figcaption><b>Figure 7.21</b> The receive path. Yellow marks where an observer can see or alter the packet: native XDP (before any sk_buff exists), the AF_PACKET taps, the netfilter hooks, and the socket queue.</figcaption>
</figure>

### The sk_buff

An `sk_buff` (*socket buffer*, "skb") is the kernel's packet descriptor. It does not hold the packet; it points into a linear data buffer by four pointers, `head` (start of the allocation), `data` (start of the current packet header), `tail` (end of the data) and `end` (end of the allocation), and keeps the lengths, protocol, device, timestamps and the owning socket. Each layer then moves the `data` pointer instead of copying bytes: `skb_pull(n)` advances `data` by n to strip a header as the packet climbs, `skb_push(n)` moves it back to prepend one as the packet descends, `skb_put(n)` extends `tail` to append, and `skb_reserve(n)` leaves headroom at the start so that headers can be pushed later without reallocation. Pulling the 14-byte Ethernet header, as `ip_rcv` expects, is exactly `skb_pull(skb, 14)` ( Figure 7.22 ). Large payloads sit outside the linear area in fragment pages described by `skb_shared_info` at `end`, which is how GRO and scatter-gather avoid copying.

<figure>
<svg viewBox="0 0 480 200" width="480"><defs><marker id="isk" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="ask" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><text class="lbl" x="240" y="8" text-anchor="middle">sk_buff: one linear buffer, four pointers</text><text class="lbl" x="8" y="66" text-anchor="start">a</text><rect class="box" x="40" y="46" width="400" height="28" rx="0"/><text class="lbl" x="240.0" y="63.0" text-anchor="middle"></text><rect class="fill" x="40" y="46" width="60" height="28" rx="0"/><text class="sm" x="70.0" y="63.0" text-anchor="middle">headroom</text><rect class="box" x="100" y="46" width="240" height="28" rx="0" style="fill:#FFF4C2"/><text class="sm" x="220.0" y="63.0" text-anchor="middle">packet data</text><rect class="fill" x="340" y="46" width="100" height="28" rx="0"/><text class="sm" x="390.0" y="63.0" text-anchor="middle">tailroom</text><line class="ln" x1="40" y1="44" x2="40" y2="32" marker-end="url(#isk)" /><text class="mono" x="40" y="29" text-anchor="middle">head</text><line class="ln" x1="100" y1="44" x2="100" y2="32" marker-end="url(#isk)" /><text class="mono" x="100" y="29" text-anchor="middle">data</text><line class="ln" x1="340" y1="44" x2="340" y2="32" marker-end="url(#isk)" /><text class="mono" x="340" y="29" text-anchor="middle">tail</text><line class="ln" x1="440" y1="44" x2="440" y2="32" marker-end="url(#isk)" /><text class="mono" x="440" y="29" text-anchor="middle">end</text><text class="sm" x="280" y="88" text-anchor="middle">driver reserved 60 bytes; frame of 240 bytes starts with the Ethernet header</text><text class="lbl" x="8" y="66" text-anchor="start">a</text><text class="lbl" x="8" y="150" text-anchor="start">b</text><rect class="box" x="40" y="130" width="400" height="28" rx="0"/><text class="lbl" x="240.0" y="147.0" text-anchor="middle"></text><rect class="fill" x="40" y="130" width="74" height="28" rx="0"/><text class="sm" x="77.0" y="147.0" text-anchor="middle">headroom</text><rect class="box" x="114" y="130" width="226" height="28" rx="0" style="fill:#FFF4C2"/><text class="sm" x="227.0" y="147.0" text-anchor="middle">packet data</text><rect class="fill" x="340" y="130" width="100" height="28" rx="0"/><text class="sm" x="390.0" y="147.0" text-anchor="middle">tailroom</text><line class="ln" x1="40" y1="128" x2="40" y2="116" marker-end="url(#isk)" /><text class="mono" x="40" y="113" text-anchor="middle">head</text><line class="ln" x1="114" y1="128" x2="114" y2="116" marker-end="url(#isk)" /><text class="mono" x="114" y="113" text-anchor="middle">data</text><line class="ln" x1="340" y1="128" x2="340" y2="116" marker-end="url(#isk)" /><text class="mono" x="340" y="113" text-anchor="middle">tail</text><line class="ln" x1="440" y1="128" x2="440" y2="116" marker-end="url(#isk)" /><text class="mono" x="440" y="113" text-anchor="middle">end</text><text class="sm" x="280" y="172" text-anchor="middle">after skb_pull(skb, 14): data moves right; the 14-byte Ethernet header is now headroom</text><text class="lbl" x="8" y="150" text-anchor="start">b</text><text class="sm" x="240" y="192" text-anchor="middle">skb_push(n) moves data left to prepend a header; skb_put(n) moves tail right; skb_reserve(n) sets the headroom.</text></svg>
<figcaption><b>Figure 7.22</b> The four sk_buff pointers, before (a) and after (b) skb_pull(skb, 14). Only the pointer moves; no bytes are copied.</figcaption>
</figure>

The kernel allocates `sk_buff` structures from a slab cache ([7.7](#s7-7){.ref}), which is why allocation is cheap enough for millions of packets per second.

### Transmit, and where acceleration attaches

The transmit path is the mirror image: `send()` enters `tcp_sendmsg()`, which copies the data into `sk_buff`s and builds segments; `ip_queue_xmit()` adds the IP header and routes the packet; the queueing discipline (`qdisc`) schedules it; `dev_queue_xmit()` hands it to the driver's `ndo_start_xmit()`, which places a descriptor in the TX ring and tells the NIC; and a completion interrupt, again batched, lets the driver free the `sk_buff`.

Several mechanisms exist because one core cannot keep up with a fast link. *RSS* (receive-side scaling) has the NIC hash each flow's addresses and ports to one of several RX queues, each with its own interrupt, so different flows are processed on different cores while the packets of one flow stay in order. *RPS* and *RFS* do the same steering in software, for NICs without enough queues, and RFS prefers the core on which the consuming application runs. *XDP* runs a small verified program, written in restricted C and loaded into the kernel, in the driver before any `sk_buff` is allocated; it can drop, redirect or pass the packet, which is the fastest place to discard unwanted traffic. Because it acts before the `AF_PACKET` tap, a packet dropped by native XDP is invisible to `tcpdump`. *DPDK* leaves the kernel path altogether: a user-space poll-mode driver reads the NIC's rings directly from huge-page memory, with no interrupts, no system calls and no `sk_buff`, at the cost of dedicating cores and reimplementing the protocol stack above it.

| | Kernel stack | XDP | DPDK |
|---|---|---|---|
| Where packets are handled | kernel, full stack | kernel driver, before sk_buff | user space, kernel bypassed |
| Interrupts | yes, with NAPI polling | yes, same driver | none: polling cores |
| Copies and system calls | one copy; one call per `recv` | none for dropped or redirected | none |
| Protocol stack | Linux's own | Linux's, for passed packets | application supplied |
| Typical use | servers, routers | filtering, load balancing, DDoS drop | forwarding and virtual-switch data planes |

::: lab
`LAB 7.12 · 20 MIN` Observe the stack's knobs and counters (outputs depend on the NIC and driver, so none is reproduced here).

```
$ ethtool -l eth0                       # RX/TX queue counts (RSS)
$ ethtool -C eth0 rx-usecs 50           # interrupt coalescing: one interrupt per 50 us
$ ethtool -S eth0 | grep -i -E 'drop|miss|rx_queue'
$ cat /proc/net/softnet_stat            # per-CPU: processed, dropped, time_squeeze
$ sudo bpftrace -e 'kprobe:tcp_v4_rcv { @[comm] = count(); }'
```

**What you should notice:** during an `iperf3` run the packets are spread over the queues listed by `ethtool -l`; a rising third column of `softnet_stat` (`time_squeeze`) means the poll budget ran out and the receive path is falling behind; and the `bpftrace` count attributes `tcp_v4_rcv` calls to whichever process happened to be on the CPU when the softirq ran, a reminder that softirq work is charged to no one in particular.
:::

::: trap
*Claim:* "`tcpdump` sees every packet the NIC received, and it sees them before the firewall." *Why it is wrong:* `tcpdump` taps at `AF_PACKET`, which is after the driver and any native XDP program (so XDP drops are invisible) and, on ingress, before netfilter (so firewall drops are visible as received). *Correct statement:* ingress capture sits between XDP and netfilter. Further, "NAPI means no interrupts" is also wrong: it means interrupts are masked during polling and re-enabled when the queue empties.
:::

::: lens
[CISCO · JUNIPER · ARISTA · NOKIA · BROADCOM · QUALCOMM]{.co}

"How does a packet travel from the NIC to a user-space application?" and "what is `sk_buff`?" are standard at platform and SDK roles; Qualcomm data-path interviews ask about NAPI and DMA rings, and Cisco and Nokia add XDP versus DPDK. A strong answer walks the nine steps with function names, states why polling replaces per-packet interrupts (the arithmetic in [7.8](#s7-8){.ref}), explains that `sk_buff` moves pointers and not bytes, and distinguishes where XDP and DPDK intercept. Follow-ups: where `tcpdump` sees the packet, what RSS does, and how the transmit path differs.
:::

::: check
1. What does the driver do with the RX interrupt when NAPI starts polling? [^c712-1]
2. How does `skb_pull(skb, 14)` remove the Ethernet header without copying? [^c712-2]
3. Where does native XDP run relative to `sk_buff` allocation? [^c712-3]
:::

[^c712-1]: It masks the queue's interrupt, and re-enables it when polling finds the ring empty.
[^c712-2]: It advances the `data` pointer by 14 bytes and reduces `len`; the header bytes remain in memory as headroom.
[^c712-3]: Before it, in the driver, which is why XDP is cheaper than any stage that follows.

## [7.13]{.sec}Firmware and embedded essentials [Should · ■■□]{.tag} {#s7-13}

Network firmware runs on small cores, often under a real-time operating system (RTOS) or on bare metal, close to the hardware this chapter has described. Correctness there rests on a handful of habits: telling the compiler that a location can change without its knowledge, ordering memory accesses, doing little in an ISR, and passing data between interrupt and main code without locks.

### volatile and device registers

A *memory-mapped* device register is read or written like memory, but a read may return a different value each time and a write has an effect. The compiler, which assumes memory changes only when the program changes it, may then optimise the access away. `volatile` forbids that: every source-level access to the object becomes a real access, in program order with respect to other volatile accesses. The qualifier combinations follow from this: `const volatile uint32_t *status` is a read-only register that the hardware may change; `volatile uint32_t *data` is a register the program may write.

```c
#include <stdint.h>

/* read-only device register */
#define UART_STATUS (*(const volatile uint32_t *)0x40001004u)
/* read/write device register */
#define UART_DATA   (*(volatile uint32_t *)0x40001000u)
#define TX_READY    (1u << 5)

void uart_putc(char c)
{
    while (!(UART_STATUS & TX_READY))  /* volatile: re-read each pass */
        ;  /* without it the compiler may read once and spin for ever */
    UART_DATA = (uint32_t)c;  /* volatile: this store must really happen */
}

/* ISR-to-main hand-over: a flag set in the handler and polled by the main loop */
static volatile uint32_t rx_flag;

void uart_isr(void)
{
    rx_flag = 1;  /* do little here; leave the work to main */
}

int main_loop_step(void)
{
    if (rx_flag) {                      /* volatile: re-read on each call */
        rx_flag = 0;
        return 1;
    }
    return 0;
}
```

Compiling this with `-O2` and reading the assembly shows the load of the status register *inside* the loop; remove `volatile` and the compiler is entitled to load once and spin for ever. Two limits must be stated. `volatile` does not make an access atomic, and it does not order the access against *non-volatile* accesses or against another core; the flag in the example is safe only because one interrupt handler and one main loop share a single core. Between cores one uses C11 atomics with acquire and release ordering, or memory barriers, which stop the CPU and compiler reordering accesses across them. Storage classes (`static`, `extern`) and the full qualifier rules are in [Pillar 2](#s2-6){.ref}.

### Lock-free ring buffers between an ISR and the main loop, or between two cores

The standard hand-over structure is the *single-producer single-consumer* (SPSC) ring. Because each index has exactly one writer, no lock is needed: the producer writes the slot and then publishes it by advancing `tail` with *release* ordering; the consumer reads `tail` with *acquire* ordering, which guarantees that it sees the slot's contents, reads the slot, and frees it by advancing `head`. With a power-of-two size, `index & (size - 1)` replaces the modulo. The same layout, one side owning each index, is the descriptor ring that a NIC and its driver share ([7.8](#s7-8){.ref}).

<figure>
<svg viewBox="0 0 480 120" width="480"><defs><marker id="isp" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="asp" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><rect class="box" x="40" y="40" width="50" height="28" rx="0"/><text class="lbl" x="65.0" y="57.0" text-anchor="middle"></text><text class="mono" x="65.0" y="58" text-anchor="middle">0</text><rect class="box" x="90" y="40" width="50" height="28" rx="0"/><text class="lbl" x="115.0" y="57.0" text-anchor="middle"></text><text class="mono" x="115.0" y="58" text-anchor="middle">1</text><rect class="box" x="140" y="40" width="50" height="28" rx="0" style="fill:#FFF4C2"/><text class="lbl" x="165.0" y="57.0" text-anchor="middle"></text><text class="mono" x="165.0" y="58" text-anchor="middle">2</text><rect class="box" x="190" y="40" width="50" height="28" rx="0" style="fill:#FFF4C2"/><text class="lbl" x="215.0" y="57.0" text-anchor="middle"></text><text class="mono" x="215.0" y="58" text-anchor="middle">3</text><rect class="box" x="240" y="40" width="50" height="28" rx="0" style="fill:#FFF4C2"/><text class="lbl" x="265.0" y="57.0" text-anchor="middle"></text><text class="mono" x="265.0" y="58" text-anchor="middle">4</text><rect class="box" x="290" y="40" width="50" height="28" rx="0"/><text class="lbl" x="315.0" y="57.0" text-anchor="middle"></text><text class="mono" x="315.0" y="58" text-anchor="middle">5</text><rect class="box" x="340" y="40" width="50" height="28" rx="0"/><text class="lbl" x="365.0" y="57.0" text-anchor="middle"></text><text class="mono" x="365.0" y="58" text-anchor="middle">6</text><rect class="box" x="390" y="40" width="50" height="28" rx="0"/><text class="lbl" x="415.0" y="57.0" text-anchor="middle"></text><text class="mono" x="415.0" y="58" text-anchor="middle">7</text><line class="ln" x1="165.0" y1="24" x2="165.0" y2="40" marker-end="url(#isp)" /><text class="sm" x="165.0" y="18" text-anchor="middle">head (consumer writes)</text><line class="acc" x1="315.0" y1="24" x2="315.0" y2="40" marker-end="url(#asp)" /><text class="sm" x="315.0" y="18" text-anchor="middle">tail (producer writes)</text><text class="sm" x="240" y="90" text-anchor="middle">slot = index &amp; (size - 1); empty when head == tail; full when tail - head == size.</text><text class="sm" x="240" y="104" text-anchor="middle">Each index has one writer, so no lock is needed: release when publishing, acquire when reading the other index.</text></svg>
<figcaption><b>Figure 7.23</b> An SPSC ring. The consumer owns head, the producer owns tail; full is tail - head = size, empty is head = tail.</figcaption>
</figure>

```c
#include <pthread.h>
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>

#define RING 1024                        /* power of two: mask replaces modulo */
#define MASK (RING - 1)

struct ring {
    uint32_t slot[RING];
    _Atomic uint32_t head;               /* written only by the consumer */
    _Atomic uint32_t tail;               /* written only by the producer */
};

static int ring_put(struct ring *r, uint32_t v)       /* producer only */
{
    uint32_t t = atomic_load_explicit(&r->tail, memory_order_relaxed);
    uint32_t h = atomic_load_explicit(&r->head, memory_order_acquire);
    if (t - h == RING)
        return 0;                        /* full */
    r->slot[t & MASK] = v;
    atomic_store_explicit(&r->tail, t + 1, memory_order_release);  /* publish */
    return 1;
}

static int ring_get(struct ring *r, uint32_t *v)      /* consumer only */
{
    uint32_t h = atomic_load_explicit(&r->head, memory_order_relaxed);
    uint32_t t = atomic_load_explicit(&r->tail, memory_order_acquire);
    if (h == t)
        return 0;                        /* empty */
    *v = r->slot[h & MASK];
    atomic_store_explicit(&r->head, h + 1, memory_order_release);  /* free slot */
    return 1;
}

static struct ring q;
#define COUNT 1000000u

static void *prod(void *arg)
{
    (void)arg;
    for (uint32_t i = 1; i <= COUNT; i++)
        while (!ring_put(&q, i))
            ;                            /* spin while full */
    return NULL;
}

int main(void)
{
    pthread_t p;
    uint64_t sum = 0;
    uint32_t v, got = 0;
    pthread_create(&p, NULL, prod, NULL);
    while (got < COUNT)
        if (ring_get(&q, &v)) { sum += v; got++; }
    pthread_join(p, NULL);
    printf("received %u items, sum %llu (expected %llu)\n", got,
           (unsigned long long)sum, (unsigned long long)COUNT * (COUNT + 1) / 2);
    return 0;
}
```

The program prints `received 1000000 items, sum 500000500000 (expected 500000500000)`. The indices are free-running 32-bit counters that wrap harmlessly, because the difference `t - h` stays correct in unsigned arithmetic; the slot is found by masking. A full ring is reported by `ring_put` returning 0, and the caller decides whether to drop, retry or back-pressure.

Byte order and bit manipulation are the other firmware staples. Whether a header field is big-endian (IP, TCP) or little-endian (802.11 Frame Control) decides whether `ntohs` or a plain read is correct; the endianness test, `__builtin_bswap32`, mask-and-shift field extraction and the set, clear and toggle idioms are all in [Pillar 2](#s2-9){.ref}.

::: trap
*Claim:* "Declaring the shared variable `volatile` makes the code thread-safe." *Why it is wrong:* `volatile` neither makes read-modify-write atomic nor orders memory accesses between cores. *Correct statement:* it prevents the compiler from removing or caching accesses, which suits device registers and ISR flags on one core; for threads and cores use atomics, barriers or locks.
:::

::: lens
[QUALCOMM · BROADCOM · ARISTA]{.co}

"What does `volatile` do, and is it enough for sharing data between an ISR and a thread?" and "implement a lock-free ring buffer" are reported for firmware and platform roles. A strong answer gives the register example and its assembly consequence, names the single-writer-per-index rule, and chooses acquire and release ordering over a lock. Follow-ups: why a mutex cannot be used inside an ISR, what happens when the producer is faster than the consumer, and why the indices may be free-running.
:::

::: check
1. What does `const volatile uint32_t *p` declare? [^c713-1]
2. Why does the SPSC ring need no lock? [^c713-2]
:::

[^c713-1]: A pointer to a 32-bit value that the program may not write through but that may change on its own, such as a hardware status register.
[^c713-2]: Each index is written by one side only; release and acquire ordering make the slot contents visible before the index that publishes them.

## [7.14]{.sec}Debugging a slow server [Optional · ■■■]{.tag} {#s7-14}

Consider a TCP service whose latency rises under load although CPU use is low. The method is that of [Pillar 11](#ch11){.ref}: a symptom, a hypothesis that this chapter makes specific, a command that tests it, and the evidence that confirms or rejects it.

| Symptom | Hypothesis | Command | Evidence | Fix |
|---|---|---|---|---|
| New connections wait, then time out | the accept queue is full: the server does not call `accept` fast enough | `ss -ltn` | `Recv-Q` on the listener near the backlog | find why the loop is blocked; raise backlog and `somaxconn` only after that |
| One thread at 100 % of a core, others idle | a single-threaded loop does blocking disk work | `top -H`, `strace -p` | the thread sits in `read` on a file, not in `epoll_wait` | keep the event loop non-blocking; push slow work to a thread pool and return results through an `eventfd` |
| Packets arrive but the application sees gaps | receive processing falls behind | `cat /proc/net/softnet_stat` | third column (`time_squeeze`) or second (dropped) rising | spread flows over queues (RSS), set IRQ affinity, raise `netdev_budget` |
| Many sockets in TIME_WAIT, `EADDRNOTAVAIL` on connect | a client opens and closes connections faster than ports recycle | `ss -tan state time-wait \| wc -l` | tens of thousands of entries | reuse connections (keep-alive), widen the ephemeral port range |
| Throughput stops while `Send-Q` is high | the peer reads slowly; the send buffer is full | `ss -tin` | `Send-Q` large, small advertised window | add per-connection output buffering and `EPOLLOUT`; look at the receiver |

A full accept queue with one busy thread is the classic first finding. The cause is in the application, the cheap fix is the event loop of [7.11](#s7-11){.ref} with a worker pool, and only then does tuning `softnet_stat` and the NIC queues pay off, because kernel tuning cannot rescue a loop that is not calling `accept`.

## [7.15]{.sec}Mini-project: TinyRelay, an epoll chat and relay server [Optional · ■■■]{.tag} {#s7-15}

The project joins the sections of this chapter into one program that can be shown at an interview. It is a single-threaded C server first, then a multi-threaded one, built in the milestones below; each milestone is small enough to finish in an evening.

| Milestone | Build | Section |
|---|---|---|
| 1 | an edge-triggered `epoll` loop with non-blocking sockets and length-prefixed frames | [7.10](#s7-10){.ref}, [7.11](#s7-11){.ref} |
| 2 | chat rooms: `JOIN`, `MSG` and `LEAVE` commands, with fan-out to every member of a room | 7.11 |
| 3 | a per-client output buffer; register `EPOLLOUT` only while it is non-empty (back-pressure) | 7.11 |
| 4 | a thread pool for slow commands, fed by a mutex and condition-variable queue; results return to the loop through an `eventfd` | [7.5](#s7-5){.ref} |
| 5 | a UDP statistics port reporting connected clients, messages per second, bytes in and out | 7.10 |
| 6 | graceful shutdown on SIGINT through `signalfd` | [7.9](#s7-9){.ref} |
| 7 | load test with `loadgen` at 1,000 and 5,000 connections; report latency percentiles | 7.11 |
| 8 | builds clean under ThreadSanitizer and AddressSanitizer, with a Makefile | [7.3](#s7-3){.ref} |

Stretch goals: IPv6 through `getaddrinfo`; `SO_REUSEPORT` sharding across worker processes; an XDP program that drops packets from a blocklisted address before they reach the server ([7.12](#s7-12){.ref}). The pay-off is a defensible answer to "design a scalable server", "explain epoll" and "how did you test the concurrency?"

:::
