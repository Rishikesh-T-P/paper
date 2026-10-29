::: {.p7}

::: pack
## Problem Set, continued: firmware, sockets and the stack {#ps7b}

::: problems

::: q
### Q7.24 Design a memory allocator (malloc and free) for an embedded system with no OS.
[ARISTA · QUALCOMM · BROADCOM · TECH-2 · ■■■ · S]{.meta}

[30-second answer: carve blocks from a static arena, each with a header (size, free flag); `malloc` takes the first free block that fits and splits it; `free` marks the block free and merges it with free neighbours.]{.short}

**Approach.** The tested first-fit implementation is in [7.7](#s7-7){.ref} (`alloc.c`). State the design choices: alignment (round sizes to 16), the fit policy (first fit is fast, best fit wastes less), splitting only when the remainder can hold a header, coalescing on free, and what happens when the arena is exhausted (return NULL, never block). **Answer.** For hard real-time firmware prefer *fixed-size pools*: one free list per size class, O(1) allocate and free, no external fragmentation ([Q2.59](#ps2){.ref} builds one). Make the allocator thread- and ISR-safe with a spinlock or by disabling interrupts for the few instructions of list surgery. **Mistakes.** Forgetting alignment, and coalescing only forwards.
:::

::: q
### Q7.25 What is an interrupt? Describe the steps from device signal to the return from the ISR.
[QUALCOMM · CISCO · JUNIPER · TECH-1 · ■■□ · S]{.meta}

[30-second answer: a device asserts an interrupt line; the controller selects a CPU, which saves its state, switches to kernel mode, jumps through the vector table to the ISR; the ISR acknowledges the device and defers work, then an `iret` restores the interrupted code.]{.short}

**Answer.** Steps: (i) device raises the line; (ii) controller (APIC or GIC) prioritises and delivers; (iii) the CPU finishes its instruction, pushes state, loads the handler address from the vector; (iv) the ISR runs, reads status, acknowledges the device, queues a bottom half; (v) `iret` or `eret` resumes. The ISR runs in interrupt context and must not sleep ([7.8](#s7-8){.ref}). **Follow-ups.** Maskable versus non-maskable; interrupt latency and nesting.
:::

::: q
### Q7.26 Top half versus bottom half. Why can't you sleep in an ISR?
[QUALCOMM · BROADCOM · TECH-1 · ■■□ · S]{.meta}

[30-second answer: the top half is the urgent, short ISR that acknowledges the device; the bottom half (softirq, tasklet, workqueue) does the rest later. An ISR runs on whatever task was interrupted and has no context of its own, so sleeping would block an unrelated task or the scheduler.]{.short}

**Answer.** Softirqs and tasklets also cannot sleep; workqueue items run in a kernel thread and can. In an ISR use spinlocks and `GFP_ATOMIC`, never a mutex or `GFP_KERNEL` ([7.8](#s7-8){.ref}). **Mistakes.** Calling a function that may sleep indirectly, such as `copy_to_user`.
:::

::: q
### Q7.27 Polling versus interrupts: when is polling better?
[CISCO · QUALCOMM · TECH-1 · ■■□ · S]{.meta}

[30-second answer: interrupts suit rare events because they cost nothing while idle; polling suits frequent events because it batches them and avoids per-event overhead and interrupt livelock.]{.short}

**Answer.** At 14.88 million minimum-size packets per second on a 10 Gb/s link, one interrupt per packet leaves no CPU for work. Hybrid designs interrupt when idle and poll when busy: NAPI. DPDK polls always, trading a burning core for latency. A poll interval bounds the latency of a polled event ([7.8](#s7-8){.ref}).
:::

::: q
### Q7.28 What is DMA?
[QUALCOMM · BROADCOM · TECH-1 · ■□□ · S]{.meta}

[30-second answer: direct memory access lets a device move data to or from main memory itself, so the CPU only sets up a descriptor and handles the completion interrupt.]{.short}

**Answer.** A NIC DMAs received frames into buffers named by an RX descriptor ring and the driver processes behind it; the buffers must be physically contiguous or described by a scatter-gather list, and cache coherency with the device must be arranged by the kernel's DMA-mapping calls. **Follow-up.** An IOMMU translates device addresses and limits what a device can reach.
:::

::: q
### Q7.29 Name the IPC mechanisms. Which is fastest, and why?
[CISCO · JUNIPER · TECH-1 · ■■□ · S]{.meta}

[30-second answer: pipes, FIFOs, message queues, shared memory, sockets and signals; shared memory is fastest because, after setup, data moves with no system call and no copy.]{.short}

**Answer.** The price of shared memory is synchronisation: use a process-shared mutex or a semaphore. Pipes and sockets are simpler and copy twice; signals carry only a number. See the table in [7.9](#s7-9){.ref}.
:::

::: q
### Q7.30 What is `volatile`? Give a firmware example. Does it make code thread-safe?
[QUALCOMM · ARISTA · TECH-1 · ■□□ · S]{.meta}

[30-second answer: `volatile` tells the compiler that every access to the object must really happen, in order, because it may change outside the program, as with a device register; it does not make code thread-safe.]{.short}

**Answer.** Worked in [Q2.7](#ps2){.ref} and [Q2.9](#ps2){.ref} of Pillar 2; the polled UART register and its assembly are in [7.13](#s7-13){.ref}. It gives neither atomicity nor ordering between cores.
:::

::: q
### Q7.31 Write a function that detects the machine's endianness.
[QUALCOMM · ARISTA · CISCO · TECH-1 · ■□□ · S]{.meta}

[30-second answer: store 1 in a 16-bit integer and look at its first byte; if it is 1, the machine is little-endian.]{.short}

**Code.**

```c
#include <stdint.h>

int is_little_endian(void)
{
    uint16_t x = 1;
    return *(uint8_t *)&x == 1;
}
```

**Answer.** Accessing an object through `uint8_t *` (a character type) is always permitted, so this is defined behaviour. A fuller treatment, with a union and `htonl`, is in [Q2.10](#ps2){.ref}.
:::

::: q
### Q7.32 Explain the TCP server socket call sequence. What does `listen()`'s backlog mean?
[CISCO · JUNIPER · ARISTA · GOOGLE · TECH-1 · ■□□ · S]{.meta}

[30-second answer: `socket`, `bind`, `listen`, then `accept` in a loop, with `read`/`write` on the descriptor it returns, and `close`; the backlog sizes the queue of completed connections waiting for `accept`.]{.short}

**Answer.** The client mirrors with `socket`, `connect`, `send`/`recv`, `close`. The kernel finishes the three-way handshake itself, parking half-open connections in the SYN queue and completed ones in the accept queue; `accept()` takes the oldest. Linux caps the backlog at `net.core.somaxconn`. When the queue is full, new connection attempts are delayed or dropped ([7.10](#s7-10){.ref}). **Mistakes.** Reading the backlog as a limit on total connections.
:::

::: q
### Q7.33 Why do we need `htons` and `htonl`?
[CISCO · JUNIPER · TECH-1 · ■■□ · S]{.meta}

[30-second answer: the network uses big-endian byte order and most hosts are little-endian, so multi-byte integers in headers and `sockaddr` fields must be converted; forgetting `htons` on a port makes the program use the wrong port.]{.short}

**Answer.** 8080 is 0x1F90; without `htons` a little-endian host sends `90 1F`, which the network reads as 0x901F = 36895. Solved in full in [Q2.11](#ps2){.ref} of Pillar 2; the lab in [7.10](#s7-10){.ref} shows `1F95` in `/proc/net/tcp`.
:::

::: q
### Q7.34 Why can `recv()` return fewer bytes than were sent? How do you frame messages over TCP?
[GOOGLE · ARISTA · CISCO · TECH-1 · ■■□ · S]{.meta}

[30-second answer: TCP is a byte stream with no message boundaries, so the kernel may split or merge sends; the receiver loops until it has a whole message, which the sender marks with a length prefix or a delimiter.]{.short}

**Approach.** Send a 4-byte length in network order, then the payload; receive with `readn(4)` and then `readn(len)`; `readn` loops over `recv` and retries on `EINTR`. The tested helpers are in [7.10](#s7-10){.ref} (`frame.c`), and `coalesce.c` there shows a 25-byte read spanning two messages. **Mistakes.** Trusting the peer's length (cap it), and sending the length in host order.
:::

::: q
### Q7.35 What is TIME_WAIT, who enters it, and why does `bind` fail with `EADDRINUSE` after a restart?
[CISCO · GOOGLE · ARISTA · TECH-1 · ■■□ · S]{.meta}

[30-second answer: TIME_WAIT is the state of the side that closes first, lasting 2 × MSL (60 s on Linux); it absorbs delayed segments and lets a lost final ACK be re-sent. A restarted server's `bind` fails because old connections on the port are still in it, unless `SO_REUSEADDR` is set.]{.short}

**Answer.** It is intentional protocol behaviour, not a bug; the protocol detail is in [Pillar 3](#ch3){.ref}. A server that closes connections itself accumulates TIME_WAIT entries; setting `SO_REUSEADDR` before `bind` fixes the restart problem. **Follow-ups.** A client that opens and closes many connections can exhaust ephemeral ports; reuse connections. **Mistakes.** Confusing `SO_REUSEADDR` with `SO_REUSEPORT`.
:::

::: q
### Q7.36 `select` versus `poll` versus `epoll`.
[CISCO · JUNIPER · ARISTA · GOOGLE · TECH-1 · ■■□ · S]{.meta}

[30-second answer: all three wait for readiness on many descriptors; `select` and `poll` rescan every descriptor on each call (O(n)), `select` is capped at 1024, and `epoll` keeps the interest list in the kernel and returns only ready descriptors (O(ready)).]{.short}

**Answer.** Use the table in [7.11](#s7-11){.ref}: limit, cost, who holds the set, edge-trigger support, portability. `epoll` is Linux-only; BSD has `kqueue`. For a few descriptors `poll` is as fast and simpler. **Follow-ups.** `io_uring` as a completion-based alternative.
:::

::: q
### Q7.37 Level-triggered versus edge-triggered epoll. What bug do you get with edge-triggered mode on a blocking socket?
[ARISTA · GOOGLE · TECH-2 · ■■■ · S]{.meta}

[30-second answer: level-triggered reports a descriptor as long as it is ready; edge-triggered reports only the transition, so you must drain the socket until `EAGAIN`. On a blocking socket the final read blocks for ever and the loop hangs.]{.short}

**Answer.** Edge-triggered code: set `O_NONBLOCK`, and on each event loop `read` until it returns `EAGAIN`. If you stop early, the leftover bytes produce no further event until new data arrives, so the connection stalls. Edge-triggered needs fewer system calls; level-triggered is more forgiving ([7.11](#s7-11){.ref}). **Mistakes.** One read per event.
:::

::: q
### Q7.38 Design a server handling 100,000 concurrent connections: the threading model, the I/O model and the kernel tuning.
[GOOGLE · CISCO · AMAZON · TECH-2 · ■■■ · T]{.meta}

[30-second answer: one event loop per core using `epoll` with non-blocking sockets and `SO_REUSEPORT` listeners, a worker pool for blocking work, per-connection state kept small, and raised descriptor and queue limits.]{.short}

**Approach.** (i) Model: a thread per core, each with its own epoll instance and listener sharing the port through `SO_REUSEPORT`, so the kernel balances new connections and there is no thundering herd. (ii) I/O: edge-triggered reads drained to `EAGAIN`; per-connection output buffers and `EPOLLOUT` for back-pressure; blocking or CPU-heavy work moved to a pool and returned through an `eventfd`. (iii) Memory: at 100,000 connections, 4 KB of user state and a few KB of socket buffer each is hundreds of megabytes, so bound buffers and use timeouts to reap idle clients. (iv) Limits: `ulimit -n` above 100,000, `net.core.somaxconn` and `tcp_max_syn_backlog` raised, `fs.file-max`. (v) NIC: RSS queues matched to cores with interrupt affinity. **Follow-ups.** What breaks first (descriptors, memory, the accept queue), and how to test (a load generator on several machines). **Mistakes.** Thread per connection; ignoring slow readers.
:::

::: q
### Q7.39 How does a packet travel from the NIC to a user-space application in Linux?
[CISCO · JUNIPER · ARISTA · NOKIA · BROADCOM · TECH-2 · ■■■ · S]{.meta}

[30-second answer: the NIC DMAs the frame into an RX ring buffer and interrupts; the driver schedules NAPI, which polls the ring in softirq, builds an `sk_buff`, and passes it through GRO, IP, netfilter and TCP into the socket's receive queue; `recv()` then copies it to user space.]{.short}

**Answer.** The chain: NIC → DMA ring → MSI-X IRQ → `napi_schedule` (IRQ masked) → `net_rx_action` → driver `poll` (budget 64) → `sk_buff` → `napi_gro_receive` → `__netif_receive_skb_core` (taps) → `ip_rcv` → netfilter PREROUTING → route (local) → `ip_local_deliver` → INPUT → `tcp_v4_rcv` → socket queue → wake the process → `tcp_recvmsg` → `copy_to_user`. Draw Figure 7.21 of [7.12](#s7-12){.ref} from memory and mark XDP and the `tcpdump` tap. **Follow-ups.** The transmit path; RSS; where firewall rules apply.
:::

::: q
### Q7.40 What is an `sk_buff`? Explain `skb_push` and `skb_pull`.
[JUNIPER · ARISTA · BROADCOM · TECH-1 · ■■□ · S]{.meta}

[30-second answer: `sk_buff` is the kernel's per-packet descriptor, pointing into a data buffer with `head`, `data`, `tail` and `end`; `skb_pull(n)` moves `data` forward to strip a header, `skb_push(n)` moves it back to prepend one, with no copying.]{.short}

**Answer.** As a packet climbs the stack each layer pulls its own header; going down, each pushes its own into headroom reserved by `skb_reserve`. For a received frame, `skb_pull(skb, 14)` exposes the IP header. `skb_put(n)` extends `tail` to append data; large payloads live in fragments after `end` ([7.12](#s7-12){.ref}). **Mistakes.** Calling `skb_push` without enough headroom, which triggers a panic or a costly reallocation.
:::

::: q
### Q7.41 What is NAPI and why was it introduced?
[QUALCOMM · CISCO · BROADCOM · TECH-1 · ■■□ · S]{.meta}

[30-second answer: NAPI is Linux's hybrid receive model: the first packet interrupts, the driver masks the interrupt and polls the ring in softirq up to a budget, then re-enables the interrupt when the ring is empty; it stops interrupt storms at high packet rates.]{.short}

**Answer.** Before NAPI one interrupt per packet could livelock a host at line rate (the arithmetic is in [7.8](#s7-8){.ref}). With NAPI the cost per packet falls as load rises. Related knobs: interrupt coalescing (`ethtool -C`), the per-poll budget (64) and `netdev_budget` (300). **Mistakes.** "NAPI removes interrupts": it only suppresses them while polling.
:::

::: q
### Q7.42 What are XDP and DPDK, and how do they differ from the normal kernel path?
[CISCO · NOKIA · GOOGLE · TECH-2 · ■■■ · S]{.meta}

[30-second answer: XDP runs a small in-kernel program in the driver before an `sk_buff` exists, to drop, redirect or pass packets; DPDK bypasses the kernel with user-space poll-mode drivers that read the NIC rings directly.]{.short}

**Answer.** XDP stays inside Linux (the kernel still owns the NIC and the stack handles whatever is passed), so it suits filtering and load balancing; DPDK takes the NIC away from the kernel, dedicates polling cores and huge pages, and the application supplies its own stack, which suits forwarding planes. See the comparison table in [7.12](#s7-12){.ref}. **Mistakes.** Saying `tcpdump` can see XDP-dropped packets.
:::

::: q
### Q7.43 Implement a lock-free single-producer single-consumer ring buffer.
[ARISTA · BROADCOM · QUALCOMM · TECH-2 · ■■■ · S]{.meta}

[30-second answer: a power-of-two array with two free-running indices, each written by exactly one side; the producer stores the slot and then publishes the tail with release ordering, the consumer reads the tail with acquire ordering.]{.short}

**Approach.** The compiled C11 program, with a million-item test between two threads, is in [7.13](#s7-13){.ref} (`spsc.c`). Key points: empty is `head == tail`; full is `tail - head == size`; the slot is `index & (size - 1)`; unsigned wrap-around keeps the differences right. **Answer.** Only acquire/release is needed because each index has a single writer, and the data written before the release is visible after the matching acquire. Multiple producers or consumers need compare-and-swap loops or locks. **Mistakes.** `volatile` indices without ordering; a non-power-of-two size with free-running counters.
:::

::: q
### Q7.44 What happens when a client calls `connect()` to a port with no listener? And when the server's accept queue is full?
[GOOGLE · CISCO · TECH-1 · ■■□ · S]{.meta}

[30-second answer: with no listener the server's kernel answers the SYN with an RST and `connect` fails at once with `ECONNREFUSED`; with a full accept queue the SYN (or the final ACK) is dropped, so the client sees retransmissions and a timeout.]{.short}

**Answer.** Refusal is quick and unambiguous. A full queue gives a slow, ambiguous failure: SYN retransmits at roughly 1, 3, 7 seconds and so on, and the symptom resembles packet loss. Diagnose with `ss -ltn` (listener `Recv-Q` at the backlog) and fix the loop that is not calling `accept` ([7.14](#s7-14){.ref}). **Follow-ups.** A firewall that silently drops gives the same timeout as a full queue, while a firewall that rejects gives a refusal or an ICMP error.
:::

::: q
### Q7.45 Explain the thundering-herd problem with `accept()` and `epoll`, and its mitigations.
[GOOGLE · ARISTA · TECH-2 · ■■■ · T]{.meta}

[30-second answer: when several processes or threads wait on one listening socket, a single new connection wakes all of them and all but one go back to sleep, wasting CPU; mitigate with `EPOLLEXCLUSIVE` or by giving each worker its own listener with `SO_REUSEPORT`.]{.short}

**Answer.** Modern `accept()` wakes one waiter, but several epoll instances watching the same listener all wake. `EPOLLEXCLUSIVE` asks the kernel to wake one or a few; `SO_REUSEPORT` lets N sockets bind the same port and the kernel hashes connections among them, which also balances load across cores. The trade-off of `SO_REUSEPORT` is that a hashed connection is stuck with its worker even if that worker is busy ([7.11](#s7-11){.ref}).
:::

**Questions solved in other pillars.** The TCP state machine and TIME_WAIT timers behind Q7.35 and Q7.44, and congestion control, belong to [Pillar 3](#ch3){.ref}. The troubleshooting framework behind the slow-server case belongs to [Pillar 11](#ch11){.ref}. Shell tools such as `ss`, `strace` and `perf` are taught in [Pillar 8](#ch8){.ref}.
:::

:::
:::
