::: {.p7}

::: pack
## Revision Spread {#rv7}

::: revision
::: top
**Ten facts.** (1) User mode versus kernel mode is a CPU mode bit; a system call crosses it by the `syscall` instruction and costs far more than a function call. (2) `fork` doubles the processes (n forks give 2ⁿ); a zombie is an exited child not yet waited for, and an orphan is adopted by PID 1. (3) Threads share code, data, heap and descriptors, and own stack, registers and TLS; one thread's SIGSEGV kills the process. (4) A mutex has an owner; a semaphore does not; a spinlock never sleeps and is the only lock usable in an ISR; wait on a condition variable in a `while`. (5) Deadlock needs mutual exclusion, hold and wait, no pre-emption and circular wait; a global lock order breaks the cycle; a cycle in a resource graph is sufficient only for single-instance resources. (6) 4 KB pages: offset 12 bits; PA = frame × 4096 + offset; EAT = h(t + m) + (1 − h)(t + 2m). (7) FIFO can fault more with more frames (Bélády); LRU and Optimal cannot. (8) An ISR is short, cannot sleep, and defers work to a bottom half; DMA moves data with no CPU copy; NAPI polls under load. (9) TCP is a byte stream: loop on `recv`, frame with a length prefix, `htons` the port, set `SO_REUSEADDR`, ignore SIGPIPE. (10) `epoll` costs O(ready); edge-triggered needs non-blocking sockets read to `EAGAIN`; the receive path is NIC, DMA ring, IRQ, NAPI, `sk_buff`, IP, TCP, socket queue, `recv`.

**Three figures to redraw.** The receive path with XDP and the tcpdump tap (Figure 7.21), the socket call ladder against the TCP handshake (Figure 7.16), and the epoll interest and ready lists (Figure 7.18).
:::

### Synchronisation primitives

| | Owner | Sleeps? | In ISR? | Use |
|---|---|---|---|---|
| Mutex | yes | yes | no | protect shared data; priority inheritance |
| Binary semaphore | no | yes | post only | signal an event |
| Counting semaphore | no | yes | post only | bound a pool of N |
| Spinlock | yes | no | yes | very short sections, kernel |
| Condition variable | no (needs a mutex) | yes | no | wait for a predicate, in a `while` |
| Read-write lock | yes | yes | no | many readers, few writers |
| Atomic | none | no | yes | one word, no lock |

### Deadlock, memory and scheduling formulae

| Item | Rule |
|---|---|
| Coffman conditions | mutual exclusion, hold and wait, no pre-emption, circular wait |
| Prevention | share, request all at once, release and retry, order the locks |
| Banker's | Need = Max − Alloc; run any task with Need ≤ Work; Work += its Alloc; safe if all finish |
| Turnaround, waiting | TAT = completion − arrival; WT = TAT − burst |
| Response time (RR) | at most (n − 1) × q for a new task |
| Optimal for average waiting | SJF (non-pre-emptive), SRTF (pre-emptive) |
| Page split | offset = log₂(page size); VPN = VA ≫ offset bits |
| Flat table size | 2^(VA bits − offset bits) × entry size |
| Two-level, 10 + 10 + 12 | 4 KB per table; 8 MB mapped needs 3 tables (12 KB) |
| x86-64 | 4 levels × 9 bits + 12 bits = 48-bit addresses |
| EAT | h × (t + m) + (1 − h) × (t + 2m) |
| 10 Gb/s, 64-byte frames | 84 bytes on the wire = 672 bits; 14.88 Mpps |

### Page replacement on 7 0 1 2 0 3 0 4 2 3 0 3 2, three frames

| Policy | Faults | Idea |
|---|---|---|
| FIFO | 10 | evict the oldest loaded |
| LRU | 9 | evict the least recently used |
| Optimal | 7 | evict the page used furthest ahead |
| Clock | n/a | LRU approximation with a reference bit and a sweeping hand |

### Socket calls and what they trigger

| Side | Call | Effect |
|---|---|---|
| Server | `socket` | create descriptor |
| Server | `bind` | local address and port (`htons`) |
| Server | `listen(n)` | passive; accept queue of about n; SYN queue behind it |
| Server | `accept` | returns a new descriptor after the handshake completed |
| Client | `connect` | sends SYN; returns on SYN-ACK; `ECONNREFUSED` on RST |
| Both | `send` / `recv` | partial counts; loop; `EINTR`, `EAGAIN` |
| Both | `close` | FIN; the first closer enters TIME_WAIT (2 × MSL) |
| UDP | `sendto` / `recvfrom` | one datagram per call; sender address returned |

### I/O models and the receive path

| Model | Cost per wait | Limit |
|---|---|---|
| thread per connection | scheduler and memory per thread | thousands |
| `select` | O(n) | fd below 1024 |
| `poll` | O(n) | none |
| `epoll` | O(ready) | descriptors, memory |

| Item | Value |
|---|---|
| NAPI poll budget | 64 per poll; `netdev_budget` 300 |
| `sk_buff` pointers | head, data, tail, end; `skb_pull` strips, `skb_push` prepends |
| Hooks in order | native XDP, tcpdump tap, netfilter PREROUTING, INPUT, socket |
| Tuning knobs | `somaxconn`, `tcp_max_syn_backlog`, `netdev_budget`, `ulimit -n`, RSS queues, IRQ affinity |
| Errors | `EAGAIN` retry later; `EINTR` retry; `ECONNRESET` close; `EPIPE` close and ignore SIGPIPE |

### Flashcards

| Q | A |
|---|---|
| Mode bit? | Separates user and kernel mode; privileged instructions fault in user mode |
| `fork` return values? | Child PID in parent, 0 in child, -1 on error |
| Processes after `fork(); fork();`? | 4 |
| `fork() && fork() \|\| fork()`? | 5 processes |
| Zombie? | Exited child not yet waited for |
| Orphan? | Running child whose parent exited; adopted by PID 1 |
| Thread-private state? | Stack, registers, TLS (`errno`) |
| Why is a thread switch cheaper? | Same page tables; TLB and caches stay warm |
| `counter++` is? | Load, add, store: not atomic |
| Mutex versus binary semaphore? | Owner and priority inheritance versus signalling |
| Why a `while` around `cond_wait`? | Spurious and stolen wake-ups |
| Spinlock in an ISR? | Yes; sleeping is impossible there |
| Producer–consumer wait order? | Semaphore `empty`, then the mutex; never the reverse |
| Four deadlock conditions? | Mutual exclusion, hold and wait, no pre-emption, circular wait |
| Cure for lock-order deadlock? | A global order |
| Safe state? | Some order lets every task finish |
| RAG cycle, multi-instance? | Necessary, not sufficient |
| Priority inversion fix? | Priority inheritance (or ceiling) |
| Starvation fix? | Ageing |
| SJF weakness? | Needs burst lengths; starves long jobs |
| RR quantum too small? | Time lost in context switches |
| Page, frame? | Virtual block, physical block of the same size |
| TLB? | Cache of recent translations |
| Page fault kinds? | Minor (no disk), major (disk), invalid (SIGSEGV) |
| Copy-on-write? | Shared read-only pages, copied on the first write |
| Bélády's anomaly? | More frames, more faults, in FIFO |
| `malloc` returns? | Virtual memory; frames arrive on first touch |
| Internal versus external fragmentation? | Waste inside a block versus unusable free gaps |
| ISR rules? | Short, no sleeping, spinlock and `GFP_ATOMIC`, defer the rest |
| Top and bottom half? | Urgent acknowledge versus deferred work |
| DMA? | Device reads or writes memory without the CPU |
| Fastest IPC? | Shared memory, with its own synchronisation |
| `volatile`? | Forces real accesses; not atomic, not ordered across cores |
| SIGPIPE? | Write to a closed peer; ignore it and handle `EPIPE` |
| `listen` backlog? | Size of the accept queue |
| Why `htons`? | Network order is big-endian |
| `recv` returned less? | Stream, no boundaries; loop and frame |
| TIME_WAIT side? | The first closer, 2 × MSL |
| `SO_REUSEADDR`? | Bind despite TIME_WAIT entries |
| `epoll` versus `poll`? | Kernel interest list; O(ready) |
| Edge-triggered rules? | Non-blocking, read until `EAGAIN` |
| Thundering herd cure? | `EPOLLEXCLUSIVE` or `SO_REUSEPORT` |
| NAPI? | Interrupt, then poll with a budget, then re-enable |
| `sk_buff`? | Packet descriptor with head, data, tail, end pointers |
| XDP versus DPDK? | In-driver kernel program versus kernel bypass |
| `connect` to a closed port? | RST then `ECONNREFUSED` |
:::
:::

:::
