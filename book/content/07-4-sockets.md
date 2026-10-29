::: {.p7}

## [7.10]{.sec}Sockets from first principles [Must · ■■□]{.tag} {#s7-10}

A *socket* is a file descriptor that names one end of a communication channel. The *Berkeley sockets API* is the set of system calls, standard on Linux, macOS and Windows (with small differences), by which a program creates such endpoints, attaches them to addresses, and moves bytes through them. A stream socket (`SOCK_STREAM`, TCP) delivers a reliable, ordered byte stream between two connected endpoints; a datagram socket (`SOCK_DGRAM`, UDP) sends independent messages with no connection and no delivery guarantee. The protocols themselves are taught in [Pillar 3](#ch3){.ref}; this section teaches the calls that drive them.

A TCP server prepares a *listening socket* and then serves connections one by one: `socket` creates the endpoint, `bind` gives it a local address, `listen` marks it passive, and `accept` waits for a client and returns a *new* descriptor for that client while the listening descriptor remains available for the next. A client calls `socket` and then `connect`. After that both sides use `send`/`recv` (or `write`/`read`) and finally `close`.

| Call | What it does | Notes |
|---|---|---|
| `socket(domain, type, proto)` | creates an endpoint, returns a descriptor | `AF_INET`/`AF_INET6`; `SOCK_STREAM`/`SOCK_DGRAM` |
| `bind(fd, addr, len)` | assigns a local address and port | port in network byte order; `EADDRINUSE` if taken |
| `listen(fd, backlog)` | makes the socket passive, sizes the accept queue | capped by `net.core.somaxconn` |
| `accept(fd, addr, len)` | takes one completed connection from the queue | returns a new descriptor; blocks if none |
| `connect(fd, addr, len)` | starts the TCP handshake | returns when established or failed |
| `send` / `recv` | move bytes | may transfer fewer bytes than asked |
| `sendto` / `recvfrom` | UDP: with a peer address per datagram | `recvfrom` reports who sent it |
| `close(fd)` | releases the descriptor, sends FIN | `shutdown(fd, SHUT_WR)` closes one direction only |
| `setsockopt` | changes behaviour | `SO_REUSEADDR`, `TCP_NODELAY`, `SO_KEEPALIVE` |

<figure>
<svg viewBox="0 0 480 300" width="480"><defs><marker id="ild" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="ald" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><text class="lbl" x="95" y="12" text-anchor="middle">Server</text><text class="lbl" x="385" y="12" text-anchor="middle">Client</text><line class="lg" x1="95" y1="18" x2="95" y2="292" /><line class="lg" x1="385" y1="18" x2="385" y2="292" /><rect class="box" x="20" y="25" width="150" height="18" rx="0"/><text class="mono" x="95.0" y="37" text-anchor="middle">socket()</text><rect class="box" x="20" y="47" width="150" height="18" rx="0"/><text class="mono" x="95.0" y="59" text-anchor="middle">bind(port)</text><rect class="box" x="20" y="69" width="150" height="18" rx="0"/><text class="mono" x="95.0" y="81" text-anchor="middle">listen(backlog)</text><rect class="box" x="20" y="91" width="150" height="18" rx="0"/><text class="mono" x="95.0" y="103" text-anchor="middle">accept()  blocks</text><rect class="box" x="20" y="205" width="150" height="18" rx="0"/><text class="mono" x="95.0" y="217" text-anchor="middle">recv()  blocks</text><rect class="box" x="20" y="229" width="150" height="18" rx="0"/><text class="mono" x="95.0" y="241" text-anchor="middle">send(reply)</text><rect class="box" x="20" y="253" width="150" height="18" rx="0"/><text class="mono" x="95.0" y="265" text-anchor="middle">recv() returns 0</text><rect class="box" x="20" y="273" width="150" height="18" rx="0"/><text class="mono" x="95.0" y="285" text-anchor="middle">close()</text><rect class="box" x="310" y="111" width="150" height="18" rx="0"/><text class="mono" x="385.0" y="123" text-anchor="middle">socket()</text><rect class="box" x="310" y="133" width="150" height="18" rx="0"/><text class="mono" x="385.0" y="145" text-anchor="middle">connect()  blocks</text><rect class="box" x="310" y="173" width="150" height="18" rx="0"/><text class="mono" x="385.0" y="185" text-anchor="middle">connect() returns</text><rect class="box" x="310" y="205" width="150" height="18" rx="0"/><text class="mono" x="385.0" y="217" text-anchor="middle">send(request)</text><rect class="box" x="310" y="241" width="150" height="18" rx="0"/><text class="mono" x="385.0" y="253" text-anchor="middle">recv() blocks</text><rect class="box" x="310" y="261" width="150" height="18" rx="0"/><text class="mono" x="385.0" y="273" text-anchor="middle">close()</text><rect class="box" x="20" y="91" width="150" height="18" rx="0" style="fill:#FFF4C2"/><text class="mono" x="95.0" y="103.0" text-anchor="middle">accept()  blocks</text><line class="acc" x1="310" y1="148" x2="170" y2="160" marker-end="url(#ald)" /><text class="sm" x="240" y="150" text-anchor="middle">SYN</text><line class="acc" x1="170" y1="162" x2="310" y2="172" marker-end="url(#ald)" /><text class="sm" x="240" y="172" text-anchor="middle">SYN-ACK</text><line class="acc" x1="310" y1="182" x2="170" y2="192" marker-end="url(#ald)" /><text class="sm" x="240" y="186" text-anchor="middle">ACK</text><text class="sm" x="240" y="202" text-anchor="middle">accept() returns a new descriptor</text><line class="ln" x1="310" y1="220" x2="170" y2="226" marker-end="url(#ild)" /><text class="sm" x="240" y="222" text-anchor="middle">data</text><line class="ln" x1="170" y1="240" x2="310" y2="246" marker-end="url(#ild)" /><text class="sm" x="240" y="238" text-anchor="middle">data</text><line class="ln" x1="310" y1="274" x2="170" y2="268" marker-end="url(#ild)" /><text class="sm" x="240" y="266" text-anchor="middle">FIN</text></svg>
<figcaption><b>Figure 7.16</b> The call sequence of a TCP exchange. The kernel completes the three-way handshake without the server's process; accept() merely collects the finished connection.</figcaption>
</figure>

The mapping to the wire is worth fixing in mind. `connect()` sends a SYN and returns when the SYN-ACK arrives and the final ACK has been sent. On the server the kernel answers SYNs by itself: it keeps half-open connections in a *SYN queue*, moves each to the *accept queue* when its handshake completes, and `accept()` simply removes the oldest entry (Figure 7.17). The `backlog` argument sizes the accept queue, limited by the system maximum; when it is full the kernel drops or ignores further handshake completions, so clients see delays or retransmitted SYNs.

<figure>
<svg viewBox="0 0 480 130" width="480"><defs><marker id="iaq" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="aaq" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><rect class="box" x="10" y="40" width="90" height="50" rx="0"/><text class="sm" x="55.0" y="68.0" text-anchor="middle">incoming SYN</text><rect class="fill" x="140" y="30" width="120" height="70" rx="0"/><text class="lbl" x="200.0" y="64.0" text-anchor="middle">SYN queue</text><text class="sm" x="200.0" y="73.0" text-anchor="middle">half-open: SYN received</text><rect class="fill" x="300" y="30" width="120" height="70" rx="0"/><text class="lbl" x="360.0" y="64.0" text-anchor="middle">accept queue</text><text class="sm" x="360.0" y="73.0" text-anchor="middle">handshake complete</text><line class="ln" x1="100" y1="65" x2="138" y2="65" marker-end="url(#iaq)" /><text class="sm" x="120" y="58" text-anchor="middle">SYN-ACK</text><line class="acc" x1="260" y1="65" x2="298" y2="65" marker-end="url(#aaq)" /><text class="sm" x="280" y="58" text-anchor="middle">ACK</text><line class="ln" x1="420" y1="65" x2="465" y2="65" marker-end="url(#iaq)" /><text class="mono" x="446" y="58" text-anchor="middle">accept()</text><text class="sm" x="360" y="116" text-anchor="middle">length capped by min(backlog, somaxconn); when full, new ACKs are dropped or ignored</text><text class="sm" x="200" y="116" text-anchor="middle"></text></svg>
<figcaption><b>Figure 7.17</b> The two kernel queues behind a listening socket.</figcaption>
</figure>

### Addresses and byte order

An IPv4 endpoint is a `struct sockaddr_in` holding the family, a 16-bit port and a 32-bit address, both in *network byte order* (big-endian). A PC stores integers little-endian, so a port must be converted with `htons` ("host to network short") and an address with `htonl`; the reverse conversions are `ntohs` and `ntohl`. For port 8080 = 0x1F90, a little-endian host holds the bytes `90 1F` in memory, and the wire needs `1F 90`; `htons(8080)` performs the swap, and on a big-endian host it does nothing. The byte-order rules themselves are in [Pillar 2](#s2-9){.ref}. `INADDR_ANY` (0.0.0.0) binds to every local address, and `inet_pton`/`inet_ntop` convert between text and binary addresses.

### A TCP echo server and client

The server below accepts one client at a time and sends back every byte it receives. It shows the three habits that separate a working server from a fragile one: it sets `SO_REUSEADDR` before `bind`, it checks every return value, and it loops on `send` because a call may transfer fewer bytes than requested.

```c
#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

static void die(const char *what) { perror(what); exit(1); }

int main(int argc, char **argv)
{
    int port = argc > 1 ? atoi(argv[1]) : 8080;
    signal(SIGPIPE, SIG_IGN);  /* write to a closed peer gives EPIPE */

    int ls = socket(AF_INET, SOCK_STREAM, 0);
    if (ls < 0) die("socket");
    int on = 1;
    setsockopt(ls, SOL_SOCKET, SO_REUSEADDR, &on, sizeof on);

    struct sockaddr_in a = { .sin_family = AF_INET,
                             .sin_port = htons(port),  /* host to network order */
                             .sin_addr.s_addr = htonl(INADDR_ANY) };
    if (bind(ls, (struct sockaddr *)&a, sizeof a) < 0) die("bind");
    if (listen(ls, 128) < 0) die("listen");
    printf("listening on port %d\n", port);

    for (;;) {
        struct sockaddr_in peer;
        socklen_t len = sizeof peer;
        int c = accept(ls, (struct sockaddr *)&peer, &len);
        if (c < 0) {
            if (errno == EINTR) continue;
            die("accept");
        }
        char ip[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &peer.sin_addr, ip, sizeof ip);
        printf("client %s:%d\n", ip, ntohs(peer.sin_port));

        char buf[4096];
        ssize_t n;
        while ((n = recv(c, buf, sizeof buf, 0)) > 0) {
            for (ssize_t off = 0; off < n; ) {   /* send may be partial */
                ssize_t w = send(c, buf + off, n - off, 0);
                if (w < 0) { if (errno == EINTR) continue; goto done; }
                off += w;
            }
        }
    done:
        close(c);  /* sends FIN; the next client is accepted */
    }
}
```

`SO_REUSEADDR` lets `bind` succeed on a port whose previous connections are still in `TIME_WAIT`; without it a restarted server fails with `EADDRINUSE` for up to a minute. It does not allow two live servers to share a port, which is a different option, `SO_REUSEPORT` ([7.11](#s7-11){.ref}). The client is shorter:

```c
#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    const char *ip = argc > 1 ? argv[1] : "127.0.0.1";
    int port = argc > 2 ? atoi(argv[2]) : 8080;

    int s = socket(AF_INET, SOCK_STREAM, 0);
    if (s < 0) { perror("socket"); return 1; }
    struct sockaddr_in a = { .sin_family = AF_INET, .sin_port = htons(port) };
    if (inet_pton(AF_INET, ip, &a.sin_addr) != 1) {
        fprintf(stderr, "bad address\n");
        return 1;
    }
    if (connect(s, (struct sockaddr *)&a, sizeof a) < 0) {
        perror("connect");
        return 1;
    }

    const char *msg = "hello, socket\n";
    send(s, msg, strlen(msg), 0);
    char buf[128];
    ssize_t n = recv(s, buf, sizeof buf - 1, 0);   /* may be partial */
    if (n < 0) { perror("recv"); return 1; }
    buf[n] = '\0';
    printf("echo: %s", buf);
    close(s);
    return 0;
}
```

::: lab
`LAB 7.10 · 15 MIN` Run both, then look at the sockets afterwards.

```
$ gcc -Wall -Wextra echosrv.c -o echosrv && gcc -Wall -Wextra echocli.c -o echocli
$ ./echosrv 8085 &
listening on port 8085
$ ./echocli 127.0.0.1 8085
echo: hello, socket
client 127.0.0.1:43614
$ awk 'NR>1 { print $2, $3, $4 }' /proc/net/tcp | grep 1F95
00000000:1F95 00000000:0000 0A
0100007F:AA5E 0100007F:1F95 06
```

**What you should notice:** `ss -tan` shows the same table in words, but `/proc/net/tcp` is always present. Port 8085 appears as `1F95`, the network-order hexadecimal that `htons` produced. State `0A` is LISTEN. State `06` is TIME_WAIT, and it sits on the *client's* side (local port `AA5E` = 43614): the client called `close()` first, so it is the one that waits, 2 × MSL (60 s on Linux), in case its final ACK was lost. This is deliberate behaviour, not a leak.
:::

### The stream has no message boundaries

TCP delivers a byte stream, so one `send()` is not one `recv()`. Three sends of 10, 20 and 5 bytes may arrive as one read of 35 bytes, two reads of 25 and 10, or any other split; likewise a single large `send` may need several `recv` calls. The program below sends three messages, lets them all arrive, and then reads.

```c
#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

int main(void)
{
    int ls = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in a = { .sin_family = AF_INET,
                             .sin_addr.s_addr = htonl(INADDR_LOOPBACK) };
    socklen_t len = sizeof a;
    bind(ls, (struct sockaddr *)&a, sizeof a);  /* port 0: kernel picks one */
    listen(ls, 1);
    getsockname(ls, (struct sockaddr *)&a, &len);

    int c = socket(AF_INET, SOCK_STREAM, 0);
    connect(c, (struct sockaddr *)&a, sizeof a);   /* completes at once */
    int s = accept(ls, NULL, NULL);

    char msg[20];
    memset(msg, 'x', sizeof msg);
    send(c, msg, 10, 0);  /* three separate sends */
    send(c, msg, 20, 0);
    send(c, msg, 5, 0);
    usleep(200000);  /* let all three arrive first */

    char buf[100];
    ssize_t n;
    n = recv(s, buf, 25, 0);  printf("first recv(25):  %zd bytes\n", n);
    n = recv(s, buf, 100, 0); printf("second recv(100): %zd bytes\n", n);
    close(c); close(s); close(ls);
    return 0;
}
```

```
first recv(25):  25 bytes
second recv(100): 10 bytes
```

The first read returned 25 bytes spanning two messages, and the second the remaining 10 bytes, spanning the third and the tail of the second. The receiver must therefore *frame* the messages: delimit them with a terminator (a newline, as HTTP/1 headers do) or prefix each with its length. A length prefix with two helpers, `readn` and `writen`, which loop until the whole count is transferred, is the standard pattern:

```c
#include <arpa/inet.h>
#include <errno.h>
#include <stdint.h>
#include <sys/socket.h>
#include <sys/types.h>

/* Read exactly n bytes; return n, 0 on clean EOF before any byte, -1 on error. */
ssize_t readn(int fd, void *buf, size_t n)
{
    size_t got = 0;
    while (got < n) {
        ssize_t r = recv(fd, (char *)buf + got, n - got, 0);
        if (r == 0) return got == 0 ? 0 : -1;   /* EOF mid-message: error */
        if (r < 0) { if (errno == EINTR) continue; return -1; }
        got += r;
    }
    return got;
}

/* Write exactly n bytes; return n or -1. */
ssize_t writen(int fd, const void *buf, size_t n)
{
    size_t sent = 0;
    while (sent < n) {
        ssize_t w = send(fd, (const char *)buf + sent, n - sent, MSG_NOSIGNAL);
        if (w < 0) { if (errno == EINTR) continue; return -1; }
        sent += w;
    }
    return n;
}

/* Frame = 4-byte big-endian length, then payload. */
int send_msg(int fd, const void *p, uint32_t len)
{
    uint32_t be = htonl(len);
    if (writen(fd, &be, 4) < 0) return -1;
    return writen(fd, p, len) < 0 ? -1 : 0;
}

ssize_t recv_msg(int fd, void *p, uint32_t cap)    /* returns payload length */
{
    uint32_t be;
    ssize_t r = readn(fd, &be, 4);
    if (r <= 0) return r;
    uint32_t len = ntohl(be);
    if (len > cap) return -1;  /* never trust a peer's length */
    return readn(fd, p, len) < 0 ? -1 : (ssize_t)len;
}
```

Three details matter. `readn` retries on `EINTR` (a signal interrupted the call) and treats end-of-file inside a message as an error. `writen` uses `MSG_NOSIGNAL` so that a closed peer produces `EPIPE` and not a fatal SIGPIPE. And `recv_msg` refuses a length larger than its buffer, because a peer's length field is untrusted input.

::: bigidea
A TCP socket promises the bytes, in order, and nothing about how they are grouped; every protocol on top of it must supply its own message boundaries.
:::

### UDP and address-family-neutral code

A UDP socket needs no `listen`, `accept` or `connect`: one `bind`, then `recvfrom` returns each datagram together with the sender's address, and `sendto` replies to it. Each call moves exactly one datagram, so there is no framing problem, but datagrams may be lost, duplicated or reordered, and one that exceeds the buffer given to `recvfrom` is truncated.

```c
#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    int port = argc > 1 ? atoi(argv[1]) : 9090;
    int s = socket(AF_INET, SOCK_DGRAM, 0);
    struct sockaddr_in a = { .sin_family = AF_INET, .sin_port = htons(port),
                             .sin_addr.s_addr = htonl(INADDR_ANY) };
    if (s < 0 || bind(s, (struct sockaddr *)&a, sizeof a) < 0) {
        perror("udp");
        return 1;
    }
    for (;;) {
        char buf[1500];
        struct sockaddr_in from;
        socklen_t len = sizeof from;
        ssize_t n = recvfrom(s, buf, sizeof buf, 0,
                             (struct sockaddr *)&from, &len);
        if (n < 0) { perror("recvfrom"); continue; }
        sendto(s, buf, n, 0, (struct sockaddr *)&from, len);   /* reply */
    }
}
```

To test it, `printf dgram | nc -u -w1 127.0.0.1 9090` should print `dgram`. To keep a client independent of IPv4 or IPv6, resolve names with `getaddrinfo`, which returns a list of candidate addresses, and try each:

```c
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

/* Connect to host:port over IPv4 or IPv6, whichever works first. */
int dial(const char *host, const char *port)
{
    struct addrinfo hints, *res, *p;
    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_UNSPEC;                 /* IPv4 or IPv6 */
    hints.ai_socktype = SOCK_STREAM;
    if (getaddrinfo(host, port, &hints, &res) != 0)
        return -1;
    int fd = -1;
    for (p = res; p; p = p->ai_next) {           /* try each address in turn */
        fd = socket(p->ai_family, p->ai_socktype, p->ai_protocol);
        if (fd < 0) continue;
        if (connect(fd, p->ai_addr, p->ai_addrlen) == 0) break;
        close(fd); fd = -1;
    }
    freeaddrinfo(res);
    return fd;
}

int main(void)
{
    int fd = dial("localhost", "8083");
    printf("dial returned %s\n",
           fd >= 0 ? "a connected socket" : "-1 (connection refused)");
    return 0;
}
```

With nothing listening on port 8083 the program prints `dial returned -1 (connection refused)`: the kernel answered the SYN with an RST, which `connect` reports as `ECONNREFUSED`. If the server's accept queue is full instead, the SYN is silently dropped and the client keeps retransmitting, so the symptom is a *timeout*, not a refusal.

### Errors and options worth knowing

| `errno` | Meaning | Usual response |
|---|---|---|
| `EINTR` | a signal interrupted the call | retry |
| `EAGAIN` / `EWOULDBLOCK` | non-blocking call has nothing to do | wait for readiness |
| `ECONNREFUSED` | no listener; RST received | report, maybe retry later |
| `ECONNRESET` | peer sent RST | close the socket |
| `EPIPE` | write after the peer closed | close; ignore SIGPIPE |
| `EADDRINUSE` | port in use or in TIME_WAIT without `SO_REUSEADDR` | set the option, or pick another port |

| Option | Effect |
|---|---|
| `SO_REUSEADDR` | allow `bind` while old connections linger in TIME_WAIT |
| `SO_REUSEPORT` | several sockets may bind one port; the kernel spreads connections among them |
| `TCP_NODELAY` | send small writes at once instead of waiting to coalesce (disables Nagle) |
| `SO_KEEPALIVE` | probe an idle connection to detect a dead peer |
| `SO_RCVBUF` / `SO_SNDBUF` | size the kernel buffers, which bounds the window the connection can advertise |

::: trap
*Claim:* "If I `send(fd, buf, 1000, 0)` and it returns 1000, the peer has received 1000 bytes." *Why it is wrong:* a successful `send` means only that the kernel accepted the bytes into its send buffer; they may still be in flight, lost and awaiting retransmission, or unread by the application. Likewise one `recv` is not one message. *Correct statement:* `send` returning n means n bytes were queued; delivery is confirmed only by an application-level reply.
:::

::: lens
[CISCO · JUNIPER · ARISTA · GOOGLE]{.co}

"Write a TCP client and server in C" and "explain `listen()`'s backlog" are reported at Cisco, Juniper and Arista, with Google asking the follow-ups on framing and errors. A strong answer writes the call sequence from memory, applies `htons`, checks return values, explains `SO_REUSEADDR` and TIME_WAIT, and volunteers that `recv` returns a partial count. Follow-ups: what `connect` returns when no process listens (`ECONNREFUSED` after an RST) and when the accept queue is full (a timeout), and how a server serves many clients at once ([7.11](#s7-11){.ref}).
:::

::: check
1. What does `accept()` return, and what happens to the listening socket? [^c710-1]
2. Which side of a connection enters TIME_WAIT? [^c710-2]
3. Why must a `recv`-based protocol parser loop? [^c710-3]
:::

[^c710-1]: A new descriptor for the connected client; the listening socket stays open and queues further connections.
[^c710-2]: The side that closes first (the active closer), for 2 × MSL.
[^c710-3]: A byte stream may split or merge messages at any point, so a single `recv` can return part of a message or parts of several.

## [7.11]{.sec}Server concurrency: threads, select, poll, epoll [Must · ■■■]{.tag} {#s7-11}

The echo server above serves one client at a time; while it waits for client A's data it cannot even accept client B. A real server must handle many connections at once, and there are two families of design. The first gives each connection its own thread or process; the second lets one thread wait on many sockets and act on whichever is ready, termed *I/O multiplexing*.

### Thread per connection

The simplest change is to hand each accepted descriptor to a new thread:

```c
#include <arpa/inet.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>

static void *serve(void *arg)
{
    int c = (int)(long)arg;
    char buf[4096];
    ssize_t n;
    while ((n = recv(c, buf, sizeof buf, 0)) > 0)
        send(c, buf, n, MSG_NOSIGNAL);  /* short writes ignored for brevity */
    close(c);
    return NULL;
}

int main(void)
{
    int ls = socket(AF_INET, SOCK_STREAM, 0), on = 1;
    setsockopt(ls, SOL_SOCKET, SO_REUSEADDR, &on, sizeof on);
    struct sockaddr_in a = { .sin_family = AF_INET, .sin_port = htons(8084),
                             .sin_addr.s_addr = htonl(INADDR_ANY) };
    if (bind(ls, (struct sockaddr *)&a, sizeof a) < 0 ||
        listen(ls, 128) < 0) {
        perror("bind/listen");
        return 1;
    }
    for (;;) {
        int c = accept(ls, NULL, NULL);
        if (c < 0) continue;
        pthread_t t;                              /* one thread per connection */
        pthread_attr_t at; pthread_attr_init(&at);
        pthread_attr_setdetachstate(&at, PTHREAD_CREATE_DETACHED);
        pthread_create(&t, &at, serve, (void *)(long)c);
    }
}
```

The program is correct and the logic stays linear, since each thread blocks in `recv` as the single-client server did. Its cost is memory and scheduling: every thread has a stack (8 MB of virtual space by default, though only the touched pages are resident) and a kernel task, and with thousands of mostly idle connections the scheduler and the caches spend their time on switching. This limit gave rise to the *C10K problem*, serving ten thousand concurrent connections on one machine, and its answer, the event loop.

### select, poll and epoll

`select` takes three bit sets of descriptors (read, write, exceptional), blocks until one is ready, and returns with the sets modified to show which; the caller rebuilds the sets on every call. The sets have a fixed size, `FD_SETSIZE`, normally 1024, so a descriptor numbered 1024 or more cannot be watched at all. `poll` takes an array of `struct pollfd`, which removes the size limit and the rebuilding of bit sets. Both are O(n) per call: the kernel scans every watched descriptor, and so does the program to find the ready ones.

`epoll` stores the interest list *inside the kernel*. `epoll_ctl` adds, modifies or removes a descriptor once; `epoll_wait` returns only the descriptors that are ready. The kernel keeps the interest list as a red-black tree and attaches a callback to each socket's wait queue; when data arrives, the callback moves that descriptor onto a *ready list* (Figure 7.18). The cost of a wait is therefore proportional to the number of ready descriptors, not the number watched.

<figure>
<svg viewBox="0 0 480 215" width="480"><defs><marker id="iep" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="aep" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><rect class="fill" x="10" y="20" width="120" height="160" rx="0"/><text class="lbl" x="70.0" y="103.0" text-anchor="middle"></text><text class="lbl" x="70" y="14" text-anchor="middle">your process</text><rect class="box" x="20" y="34" width="100" height="36" rx="0"/><text class="mono" x="70.0" y="51.0" text-anchor="middle">epoll_ctl</text><text class="sm" x="70.0" y="60.0" text-anchor="middle">ADD / MOD / DEL</text><rect class="box" x="20" y="132" width="100" height="36" rx="0"/><text class="mono" x="70.0" y="149.0" text-anchor="middle">epoll_wait</text><text class="sm" x="70.0" y="158.0" text-anchor="middle">returns ready fds</text><rect class="fill" x="165" y="20" width="150" height="160" rx="0"/><text class="lbl" x="240.0" y="103.0" text-anchor="middle"></text><text class="lbl" x="240" y="14" text-anchor="middle">epoll instance (kernel)</text><rect class="box" x="175" y="34" width="130" height="60" rx="0"/><text class="lbl" x="240.0" y="63.0" text-anchor="middle">interest list</text><text class="sm" x="240.0" y="72.0" text-anchor="middle">red-black tree keyed by fd</text><rect class="box" x="175" y="118" width="130" height="50" rx="0" style="fill:#FFF4C2"/><text class="lbl" x="240.0" y="142.0" text-anchor="middle">ready list</text><text class="sm" x="240.0" y="151.0" text-anchor="middle">linked list, filled by callbacks</text><line class="ln" x1="120" y1="52" x2="173" y2="52" marker-end="url(#iep)" /><line class="acc" x1="173" y1="143" x2="122" y2="150" marker-end="url(#aep)" /><rect class="box" x="360" y="20" width="110" height="36" rx="0"/><text class="sm" x="415.0" y="37.0" text-anchor="middle">socket A</text><text class="sm" x="415.0" y="46.0" text-anchor="middle">wait queue</text><rect class="box" x="360" y="66" width="110" height="36" rx="0"/><text class="sm" x="415.0" y="83.0" text-anchor="middle">socket B</text><text class="sm" x="415.0" y="92.0" text-anchor="middle">wait queue</text><rect class="box" x="360" y="112" width="110" height="36" rx="0" style="fill:#FFF4C2"/><text class="sm" x="415.0" y="129.0" text-anchor="middle">socket C</text><text class="sm" x="415.0" y="138.0" text-anchor="middle">wait queue</text><path class="acc" d="M360,130 Q330,130 305,143" marker-end="url(#aep)" /><text class="sm" x="335" y="160" text-anchor="middle">data arrives: callback</text><text class="sm" x="335" y="170" text-anchor="middle">adds C to the ready list</text><line class="lg" x1="305" y1="52" x2="358" y2="38" /><line class="lg" x1="305" y1="60" x2="358" y2="84" /><line class="lg" x1="305" y1="70" x2="358" y2="128" /><text class="sm" x="240" y="200" text-anchor="middle">Each wait costs O(ready descriptors), not O(watched descriptors).</text></svg>
<figcaption><b>Figure 7.18</b> Inside epoll. The interest list is built once by epoll_ctl; the socket callbacks fill the ready list; epoll_wait only drains it.</figcaption>
</figure>

| | `select` | `poll` | `epoll` |
|---|---|---|---|
| Descriptor limit | `FD_SETSIZE` (1024) | none | none (resource limit) |
| Cost per wait | O(n) scan, O(n) copy in | O(n) scan, O(n) copy in | O(ready) |
| Interest set kept by | caller, rebuilt each call | caller, array each call | kernel, changed by `epoll_ctl` |
| Edge-triggered mode | no | no | yes |
| Portability | POSIX everywhere | POSIX | Linux only (BSD: `kqueue`) |

### Level-triggered and edge-triggered

[**Level or edge** — level-triggered is a doorbell that rings while the visitor stands there; edge-triggered rings once on arrival, and you must let everyone in.]{.margin}By default `epoll` is *level-triggered*: `epoll_wait` reports a descriptor on every call for as long as it is ready, that is, while unread data remains. In *edge-triggered* mode (`EPOLLET`) it reports a descriptor only when its state *changes* from not ready to ready: once per arrival of new data. The two behaviours are drawn in Figure 7.19.

<figure>
<svg viewBox="0 0 480 175" width="480"><defs><marker id="ilt" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="alt" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><text class="sm" x="8" y="40" text-anchor="start">data in socket</text><text class="sm" x="8" y="100" text-anchor="start">level-triggered</text><text class="sm" x="8" y="148" text-anchor="start">edge-triggered</text><path class="ln" d="M90,50 L120,50 L120,26 L300,26 L300,50 L360,50" /><text class="sm" x="210" y="20" text-anchor="middle">unread bytes remain</text><line class="ln" x1="150" y1="108" x2="150" y2="84" marker-end="url(#ilt)" /><line class="ln" x1="180" y1="108" x2="180" y2="84" marker-end="url(#ilt)" /><line class="ln" x1="210" y1="108" x2="210" y2="84" marker-end="url(#ilt)" /><line class="ln" x1="240" y1="108" x2="240" y2="84" marker-end="url(#ilt)" /><line class="ln" x1="270" y1="108" x2="270" y2="84" marker-end="url(#ilt)" /><line class="ln" x1="120" y1="108" x2="120" y2="84" marker-end="url(#ilt)" /><line class="acc" x1="120" y1="156" x2="120" y2="124" marker-end="url(#alt)" /><line class="lg" x1="90" y1="110" x2="360" y2="110" /><line class="lg" x1="90" y1="158" x2="360" y2="158" /><text class="sm" x="210" y="78" text-anchor="middle">every epoll_wait reports it while data remains</text><text class="sm" x="210" y="122" text-anchor="middle">reported once, on the rising edge: read until EAGAIN</text><text class="sm" x="210" y="172" text-anchor="middle">epoll_wait calls at t = 1 ... 6</text></svg>
<figcaption><b>Figure 7.19</b> Level-triggered reports every wait while data remains. Edge-triggered reports once, at the rising edge.</figcaption>
</figure>

Edge-triggered mode demands two disciplines. The sockets must be *non-blocking* (`O_NONBLOCK`), and on each notification the program must read until `read` returns `EAGAIN`, because an event is not repeated if data is left behind. Using ET with a blocking socket hangs the server at the last read, and not draining loses the rest of the data until the peer sends more. In return ET needs fewer `epoll_wait` calls.

### The epoll server

The listing is a complete echo server serving every client from one thread. The listening socket is level-triggered; each client is registered edge-triggered.

```c
#define _GNU_SOURCE
#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/epoll.h>
#include <sys/socket.h>
#include <unistd.h>

#define MAX_EVENTS 256

static void die(const char *what) { perror(what); exit(1); }

static void set_nonblock(int fd)
{
    int fl = fcntl(fd, F_GETFL, 0);
    if (fl < 0 || fcntl(fd, F_SETFL, fl | O_NONBLOCK) < 0) die("fcntl");
}

static void add(int ep, int fd, uint32_t events)
{
    struct epoll_event ev = { .events = events, .data.fd = fd };
    if (epoll_ctl(ep, EPOLL_CTL_ADD, fd, &ev) < 0) die("epoll_ctl add");
}

int main(int argc, char **argv)
{
    int port = argc > 1 ? atoi(argv[1]) : 8080;
    signal(SIGPIPE, SIG_IGN);

    int ls = socket(AF_INET, SOCK_STREAM, 0);
    if (ls < 0) die("socket");
    int on = 1;
    setsockopt(ls, SOL_SOCKET, SO_REUSEADDR, &on, sizeof on);
    struct sockaddr_in a = { .sin_family = AF_INET, .sin_port = htons(port),
                             .sin_addr.s_addr = htonl(INADDR_ANY) };
    if (bind(ls, (struct sockaddr *)&a, sizeof a) < 0) die("bind");
    if (listen(ls, SOMAXCONN) < 0) die("listen");
    set_nonblock(ls);

    int ep = epoll_create1(0);
    if (ep < 0) die("epoll_create1");
    add(ep, ls, EPOLLIN);                         /* listener: level-triggered */
    printf("epoll server on port %d\n", port);

```

The event loop follows.

```c
    struct epoll_event evs[MAX_EVENTS];
    for (;;) {
        int n = epoll_wait(ep, evs, MAX_EVENTS, -1);
        if (n < 0) { if (errno == EINTR) continue; die("epoll_wait"); }
        for (int i = 0; i < n; i++) {
            int fd = evs[i].data.fd;

            if (fd == ls) {                       /* new connections */
                for (;;) {
                    int c = accept(ls, NULL, NULL);
                    if (c < 0) {
                        if (errno == EAGAIN || errno == EWOULDBLOCK) break;
                        if (errno == EINTR) continue;
                        perror("accept"); break;
                    }
                    set_nonblock(c);
                    add(ep, c, EPOLLIN | EPOLLRDHUP | EPOLLET);   /* ET */
                }
                continue;
            }

            if (evs[i].events & (EPOLLERR | EPOLLHUP)) { close(fd); continue; }

            int closed = 0;
            char buf[4096];
            for (;;) {                            /* ET: drain until EAGAIN */
                ssize_t r = read(fd, buf, sizeof buf);
                if (r > 0) {
                    ssize_t off = 0;
                    while (off < r) {
                        ssize_t w = write(fd, buf + off, r - off);
                        if (w > 0) { off += w; continue; }
                        if (w < 0 && errno == EINTR) continue;
                        /* EAGAIN: the send buffer is full; a real server would
                           queue the rest and register EPOLLOUT. We drop it. */
                        break;
                    }
                } else if (r == 0) { closed = 1; break; }  /* peer closed */
                else if (errno == EAGAIN || errno == EWOULDBLOCK) break;
                else if (errno == EINTR) continue;
                else { closed = 1; break; }
            }
            if (closed || (evs[i].events & EPOLLRDHUP))
                close(fd);  /* close() also removes it from epoll */
        }
    }
}
```

Read it in four steps. The setup is `socket`, `bind`, `listen` and `set_nonblock`. `epoll_create1` makes the instance and `add` registers the listener. The loop calls `epoll_wait`; if the event is on the listener, a loop accepts every pending connection until `EAGAIN`, switching each new socket to non-blocking and registering it with `EPOLLIN | EPOLLRDHUP | EPOLLET`. Otherwise the event is on a client, and the program reads until `EAGAIN`, writing each chunk back, and closes the socket on end-of-file or error; `close` also removes it from the epoll set, provided the descriptor has not been duplicated. One simplification remains: if `write` returns `EAGAIN` because the peer is not reading, the remaining bytes are dropped. A production server queues them in a per-connection buffer and registers `EPOLLOUT` until it drains, which is the back-pressure mechanism.

::: lab
`LAB 7.11 · 20 MIN` Hold thousands of connections open. The load generator `loadgen.c` below opens N connections to the server and sends one echo on each.

```c
#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    if (argc < 3) {
        fprintf(stderr, "usage: loadgen port connections\n");
        return 1;
    }
    int port = atoi(argv[1]), conns = atoi(argv[2]);
    int *fd = malloc(conns * sizeof *fd);
    struct sockaddr_in a = { .sin_family = AF_INET, .sin_port = htons(port) };
    inet_pton(AF_INET, "127.0.0.1", &a.sin_addr);
    int ok = 0;
    for (int i = 0; i < conns; i++) {
        fd[i] = socket(AF_INET, SOCK_STREAM, 0);
        if (connect(fd[i], (struct sockaddr *)&a, sizeof a) < 0) {
            perror("connect");
            break;
        }
        ok++;
    }
    for (int i = 0; i < ok; i++) {  /* one round trip on every connection */
        char b[16];
        send(fd[i], "ping", 4, 0);
        if (recv(fd[i], b, sizeof b, 0) != 4) {
            fprintf(stderr, "bad echo on %d\n", i);
            break;
        }
    }
    printf("%d of %d connections echoed\n", ok, conns);
    return 0;
}
```

```
$ gcc -O2 epollsrv.c -o epollsrv && gcc loadgen.c -o loadgen
$ ulimit -n 20000
$ ./epollsrv 8082 &
$ ./loadgen 8082 3000
3000 of 3000 connections echoed
```

**What you should notice:** one thread serves 3,000 simultaneous connections. Raise the count until `connect` fails with `EMFILE` or `ECONNREFUSED`; the first is the per-process descriptor limit (`ulimit -n`), the second a full accept queue (`net.core.somaxconn`). Repeat with `tpc` and compare the memory in `ps -o rss,nlwp`, then fill the table below on your own machine.
:::

| Connections | Thread per connection | `select` | `epoll` |
|---|---|---|---|
| 10 | | | |
| 100 | | | |
| 1,000 | | | |
| 10,000 | | n/a (over 1024 descriptors) | |

*Fill in resident memory and the time to echo all connections; the shape of the curve, not the values, is the lesson.*

### Further models and pitfalls

An event loop uses one core. To use several, run one loop per core: each worker has its own epoll instance and its own listening socket bound to the same port with `SO_REUSEPORT`, and the kernel hashes incoming connections among them. Sharing a *single* listening socket among several waiters causes the *thundering herd*, where every sleeper wakes for one new connection and all but one go back to sleep; `EPOLLEXCLUSIVE` or the sharded listeners avoid it. Libraries such as libevent and the structure of nginx implement this *reactor* pattern. `io_uring` goes one step further: the application submits operations on a shared ring and collects *completions*, so a burst of I/O needs few system calls, and the model is closer to asynchronous I/O than to readiness notification.

::: trap
*Claim:* "With `EPOLLET` I can read once per event." *Why it is wrong:* edge-triggered mode does not repeat the notification for data left in the buffer. *Correct statement:* read until `EAGAIN`, on a non-blocking socket. Further, `select` cannot watch a descriptor numbered 1024 or above.
:::

::: lens
[CISCO · JUNIPER · ARISTA · GOOGLE · NOKIA]{.co}

"`select` versus `poll` versus `epoll`" is among the most reported systems questions at these employers, and Google SRE and networking interviews raise the C10K problem directly. A strong answer gives the cost model (O(n) per call against O(ready)), the descriptor limit, the interest list kept in the kernel, then level versus edge and the non-blocking requirement. Follow-ups: how to scale a server to several cores (`SO_REUSEPORT`, one loop per core), what the thundering herd is, and why a slow client needs an output buffer and `EPOLLOUT`.
:::

::: check
1. Why does `epoll_wait` scale better than `poll`? [^c711-1]
2. What happens if an edge-triggered server stops reading before `EAGAIN`? [^c711-2]
:::

[^c711-1]: The interest list lives in the kernel and only ready descriptors are returned, so the cost depends on the number of ready descriptors, not the number watched.
[^c711-2]: The remaining data stays in the socket buffer with no further notification until new data arrives, so the connection stalls.

:::
