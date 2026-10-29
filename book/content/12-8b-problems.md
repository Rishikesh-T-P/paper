::: {.p12}
::: problems
::: q
### Q12.19 Primary key, unique key and foreign key.
[CISCO · NOKIA · TECH-1 · ■□□ · T]{.meta}

[30-second answer: a primary key identifies each row and can be neither null nor repeated (one per table); a unique key forbids repeats but may allow a null (several per table); a foreign key is a column that must match a primary or unique key in another table, which enforces referential integrity.]{.short}

**Example.** `device.name` is the primary key, `device.serial` unique, `device.site_id` a foreign key to `site`. Deleting a site that devices still reference is refused, or cascades if declared `ON DELETE CASCADE`. Table in [§12.9](#s12-9){.ref}.
:::

::: q
### Q12.20 What is normalisation? Explain 1NF, 2NF and 3NF.
[CISCO · NOKIA · MICROSOFT · TECH-1 · ■□□ · T]{.meta}

[30-second answer: normalisation splits tables so that each fact is stored once, removing insertion, update and deletion anomalies. 1NF: atomic cells. 2NF: no non-key attribute depends on part of a composite key. 3NF: no non-key attribute depends on another non-key attribute. Mnemonic: every attribute depends on the key (1NF), the whole key (2NF) and nothing but the key (3NF).]{.short}

**Example.** The four-table decomposition of the interface log is worked in [§12.9](#s12-9){.ref}. **Mistake.** Stating that normalisation always improves speed; it reduces redundancy but adds joins.
:::

::: q
### Q12.21 Write SQL for the second-highest salary, with and without window functions.
[MICROSOFT · NOKIA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: `SELECT MAX(salary) FROM emp WHERE salary < (SELECT MAX(salary) FROM emp);` returns the second-highest distinct salary.]{.short}

**Data.** `emp(name, salary)`: Asha 50,000; Ravi 70,000; Meena 70,000; Kiran 60,000; Dev 40,000. **Three forms, each returning 60,000.**

```sql
SELECT DISTINCT salary FROM emp ORDER BY salary DESC LIMIT 1 OFFSET 1;
SELECT DISTINCT salary FROM
  (SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) r FROM emp) t
WHERE r = 2;
```

**Ties.** Ravi and Meena tie at 70,000, so `DENSE_RANK` and `DISTINCT` are needed; `ROW_NUMBER` would return 70,000. **Follow-up.** If there is no second salary, the first form returns null and the `LIMIT` form returns no row; wrap it in a subquery to force null.
:::

::: q
### Q12.22 INNER versus LEFT JOIN, with sample tables and output.
[CISCO · MICROSOFT · TECH-1 · ■■□ · T]{.meta}

[30-second answer: `INNER JOIN` keeps only rows that match on both sides; `LEFT JOIN` keeps every left row and fills the right columns with null when nothing matches.]{.short}

**Data.** `dept`: 10 NOC, 20 Dev, 30 QA. `emp(ename, did)`: Asha 10, Ravi 10, Meena 20.

| Query on `dept d ... emp e ON e.did = d.did` | Rows returned |
|---|---|
| `INNER JOIN` | (Dev, Meena), (NOC, Asha), (NOC, Ravi) |
| `LEFT JOIN` | the same three, plus (QA, null) |

**Use.** Add `WHERE e.ename IS NULL` to a left join to find departments with no employees: QA. **Mistake.** Putting a filter on a right-table column in `WHERE`, which turns a left join into an inner join; put it in `ON`.
:::

::: q
### Q12.23 What is an index? Why a B+ tree? When does an index hurt?
[CISCO · NOKIA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: an index is a sorted auxiliary structure that avoids scanning the table. A B+ tree is used because it is balanced and shallow (high fan-out means three or four page reads for a million rows) and its linked leaves give cheap range scans. It hurts when it slows writes, costs space, or is ignored.]{.short}

**When ignored.** Low selectivity (a column with two values), a function applied to the column, a leading wildcard (`LIKE '%x'`), or a composite index whose leftmost column is not in the query. **Follow-up.** Clustered versus non-clustered ([§12.9](#s12-9){.ref}).
:::

::: q
### Q12.24 Explain ACID with a bank-transfer example.
[MICROSOFT · AMAZON · TECH-1 · ■■□ · T]{.meta}

[30-second answer: moving ₹500 from account 1 to 2 must debit and credit together (atomicity), keep the balance rule intact (consistency), not be seen half-done by others (isolation) and survive a crash after commit (durability).]{.short}

```sql
BEGIN;
UPDATE acct SET bal = bal - 500 WHERE id = 1 AND bal >= 500;
UPDATE acct SET bal = bal + 500 WHERE id = 2;
COMMIT;
```

**Mechanisms.** Atomicity by an undo log; consistency by constraints (`CHECK (bal >= 0)`); isolation by locks or MVCC; durability by flushing the write-ahead log before commit. **Mistake.** Ignoring the check of the first update's row count: if the balance is short, zero rows change and the transaction must roll back.
:::

::: q
### Q12.25 Isolation levels and the anomalies each prevents.
[MICROSOFT · NOKIA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: read uncommitted allows dirty reads; read committed forbids them; repeatable read also forbids non-repeatable reads; serializable also forbids phantoms.]{.short}

**Answer.** Each level adds one prevention, in the order dirty read, non-repeatable read, phantom (matrix in [§12.9](#s12-9){.ref}). **Defaults.** PostgreSQL and Oracle read committed; MySQL InnoDB repeatable read. **Follow-up.** Why not always serializable? Throughput falls through blocking or retry on conflicts. **Mistake.** Quoting the standard table for PostgreSQL's repeatable read, which also blocks phantoms.
:::

::: q
### Q12.26 Two engineers allocate "the next free IP" at once and get the same address. Why, and how do you fix it?
[AMAZON · CISCO · TECH-2 · ■■■ · T]{.meta}

[30-second answer: each transaction reads the same free row before the other writes (a check-then-act race), so both claim it. Fix by making the claim atomic: a conditional update, a lock on the row with `FOR UPDATE SKIP LOCKED`, or a unique constraint that makes the second insert fail.]{.short}

**Interleaving.** T1 and T2 both run `SELECT ip FROM ip_pool WHERE owner IS NULL ORDER BY ip LIMIT 1` and see 10.0.0.2; both then `UPDATE ... SET owner = ...` for it. Under read committed both succeed.

**Fixes.**

1. Conditional update, checking the row count: `UPDATE ip_pool SET owner = :me WHERE ip = :ip AND owner IS NULL;` One row changed means success; zero means retry. We ran this on a pool whose first free address was 10.0.0.2: exactly one row changed.
2. Lock while choosing (PostgreSQL, MySQL 8): `SELECT ip FROM ip_pool WHERE owner IS NULL ORDER BY ip LIMIT 1 FOR UPDATE SKIP LOCKED;` so each transaction takes a different free row.
3. A table `allocation(ip PRIMARY KEY, owner)`: the second insert of the same `ip` violates the key and is retried.

**Mistake.** Fixing it in application code with a Python lock, which fails with more than one application server; the database is the single point of agreement.
:::

::: q
### Q12.27 Represent −18 in 8-bit two's complement.
[QUALCOMM · BROADCOM · TECH-1 · ■□□ · T]{.meta}

[30-second answer: 1110 1110, which is 0xEE.]{.short}

**Steps.** 18 = 0001 0010; invert: 1110 1101; add one: 1110 1110. **Check.** 256 − 18 = 238 = 0xEE. **Range.** −128 to 127; the pattern 1000 0000 has no positive counterpart.
:::

::: q
### Q12.28 What is endianness? What is network byte order, and why do we need `htons`?
[QUALCOMM · ARISTA · BROADCOM · TECH-1 · ■■□ · S]{.meta}

[30-second answer: endianness is the order in which a multi-byte value's bytes are stored. Little-endian puts the least significant byte first (x86, most ARM); big-endian puts the most significant first. Network byte order is big-endian, so `htons` and `htonl` convert from host order before sending and `ntohs` and `ntohl` convert back.]{.short}

**Example.** 10.0.0.1 is 0x0A000001: on the wire the bytes are 0A 00 00 01; in memory on a little-endian host they are 01 00 00 0A. `htons(0x1234)` on such a host gives 0x3412. **Mistake.** Calling network byte order "little-endian". Details in [§2.9](#s2-9){.ref}.
:::

::: q
### Q12.29 Write a C function to check whether the machine is little-endian.
[QUALCOMM · BROADCOM · TECH-1 · ■■□ · S]{.meta}

[30-second answer: store 1 in a 16-bit integer and read its first byte through a byte pointer; if it is 1, the least significant byte is first.]{.short}

```c
#include <stdint.h>
int is_little_endian(void) {
    uint16_t x = 1;
    return *(uint8_t *)&x == 1;
}
```

**Output.** On x86 the function returns 1. Reading through `uint8_t *` (a character type) is permitted by the aliasing rules, whereas a cast between `int *` types would not be. **Follow-up.** A `union` also works in C.
:::

::: q
### Q12.30 Count the set bits of an integer (Kernighan's method). Complexity?
[QUALCOMM · BROADCOM · ARISTA · TECH-1 · ■■□ · S]{.meta}

[30-second answer: repeat `x &= x - 1`, which clears the lowest set bit, and count the iterations; the time is O(*k*) for *k* set bits.]{.short}

```c
int popcount(unsigned x) {
    int c = 0;
    while (x) { x &= x - 1; c++; }
    return c;
}
```

**Trace.** For 0xF0F0 (eight set bits) the loop runs 8 times; for 0 it runs 0 times, so `popcount(0xF0F0)` is 8 and `popcount(0)` is 0 (compiled and run). **Why it works.** Subtracting 1 flips the lowest set bit and every zero below it, so the AND clears exactly that bit. **Alternatives.** A 256-entry table, or `__builtin_popcount` (hardware instruction).
:::

::: q
### Q12.31 Find the tag, index and offset bits for a 16 KB direct-mapped cache with 16-byte blocks and 32-bit addresses.
[QUALCOMM · BROADCOM · TECH-1 · ■■□ · T]{.meta}

[30-second answer: offset 4 bits, index 10 bits, tag 18 bits.]{.short}

**Steps.** Offset = log<sub>2</sub> 16 = 4. Blocks = 16,384/16 = 1,024, and direct-mapped means one block per set, so index = log<sub>2</sub> 1,024 = 10. Tag = 32 − 10 − 4 = 18. **Variant.** A 4-way cache of the same size has 256 sets: index 8, tag 20. Method and a hit-count example in [§12.10](#s12-10){.ref}.
:::

::: q
### Q12.32 Interrupts versus polling versus NAPI. Why do high-speed NICs poll?
[ARISTA · BROADCOM · AMAZON · TECH-2 · ■■□ · T]{.meta}

[30-second answer: an interrupt per packet costs a context switch, which at millions of packets a second consumes the CPU (receive livelock); polling wastes cycles when idle. NAPI combines them: the first packet interrupts, interrupts are then masked and the kernel polls in batches until the ring is empty.]{.short}

**Detail.** The NIC places packets in a ring by DMA; interrupt coalescing delays the signal until several packets accumulate, trading latency for efficiency. Multi-queue NICs spread flows over cores (RSS). `ethtool -c` shows coalescing and `ethtool -S` shows drops. See [§7.8](#s7-8){.ref}.
:::

::: q
### Q12.33 Why do routers use TCAM for lookups? Trade-offs against SRAM-based algorithmic lookup.
[CISCO · JUNIPER · ARISTA · TECH-2 · ■■■ · T]{.meta}

[30-second answer: a TCAM compares the key with every entry at once and stores a "don't care" bit per cell, so a longest-prefix or ACL lookup finishes in one cycle regardless of table size. The price is area, power and cost per bit, and limited capacity; algorithmic lookup in SRAM or DRAM (multibit tries) is cheaper and larger but needs several memory accesses.]{.short}

**Detail.** Entries are ordered so that longer prefixes win, which makes incremental updates costly. TCAM is also the natural store for ACLs because it matches ranges of header bits. High-end ASICs combine both. See [Pillar 5](#ch5){.ref} and [§1.9](#s1-9){.ref}.
:::

::: q
### Q12.34 Design the network for a new five-building campus with 8,000 users.
[CISCO · JUNIPER · NOKIA · TECH-2 · ■■□ · T]{.meta}

[30-second answer: a hierarchical design with dual cores, a distribution pair per building and dual uplinks everywhere; one /16 per building summarised in an OSPF stub area; HSRP or VRRP gateways, a wireless controller with 802.1X and a guest portal, segmentation by ACL, and dual edge firewalls to two providers. Peak internet demand is 8,000 × 0.4 × 2 Mb/s = 6.4 Gb/s, so two 10 Gb/s uplinks.]{.short}

**Skeleton to redraw.** Clarify; estimate; core, distribution, access; addressing; redundancy; wireless; security; failure; trade-offs. **Full solution** with figure and IP plan: [§12.11](#s12-11){.ref}.
:::

::: q
### Q12.35 Design a rate limiter for an API used by 10 million users.
[AMAZON · GOOGLE · MICROSOFT · TECH-2 · ■■□ · T]{.meta}

[30-second answer: a token bucket per API key at the gateway, with counters in a sharded in-memory store updated atomically; 10<sup>6</sup> active users at 0.5 requests per second need 500,000 checks per second, hence at least 5 shards of 100,000 operations per second; refused clients receive 429 and `Retry-After`.]{.short}

**Skeleton.** Requirements; algorithm choice (token bucket for bursts); placement at the gateway; distributed state; response; failure policy (open for reads, closed for payments). **Full solution:** [§12.11](#s12-11){.ref}. Code: [§1.15](#s1-15){.ref}.
:::

::: q
### Q12.36 Token bucket versus leaky bucket, and how they relate to policing and shaping.
[CISCO · JUNIPER · ARISTA · TECH-1 · ■■□ · T]{.meta}

[30-second answer: a token bucket of capacity *b* refilled at rate *r* lets a quiet sender burst up to *b* and then sends at *r*; a leaky bucket queues arrivals and releases them at constant rate, so its output is smooth. A policer is a token bucket that drops or re-marks excess; a shaper queues the excess and so behaves like a leaky bucket.]{.short}

**Numbers.** With *r* = 10 per second and *b* = 20, a full bucket allows 20 + 10 × 5 = 70 packets in the first 5 seconds; a leaky bucket at 10 per second allows only 50. **Consequence.** Policing adds no delay but can cause TCP loss; shaping adds delay and needs buffer ([§4.11](#s4-11){.ref}).
:::

::: q
### Q12.37 Design a CDN for an Indian video-streaming start-up.
[GOOGLE · AMAZON · MICROSOFT · TECH-2 · ■■■ · T]{.meta}

[30-second answer: assume 2 million daily viewers watching one hour at 2 Mb/s: 900 MB each, 1.8 PB a day, 167 Gb/s on average and about 500 Gb/s at three times the mean. Serve adaptive-bitrate segments from edge caches in Mumbai, Delhi, Chennai and Kolkata and inside ISP networks, with a shield tier, so that at a 95% hit ratio the origin carries 25 Gb/s at peak.]{.short}

**Components.** Request routing by DNS or anycast; segments of 2 to 6 seconds cached under the URL; popular titles in memory, the long tail on disk; versioned manifests; token-signed URLs; TLS at the edge; popular new releases pre-positioned before launch. **Arithmetic.** 2 × 10<sup>6</sup> × 0.9 GB = 1.8 PB; 1.8 × 10<sup>15</sup> × 8/86,400 = 167 Gb/s; × 3 = 500; × 5% = 25. **Trade-off.** Pre-positioning spends bandwidth to save latency. Template: [§12.11](#s12-11){.ref}.
:::

::: q
### Q12.38 Anycast versus GeoDNS for request routing.
[GOOGLE · AMAZON · CISCO · TECH-2 · ■■■ · T]{.meta}

[30-second answer: GeoDNS answers each lookup with a nearby server's address, chosen from the resolver's location; anycast announces one address from many sites and lets BGP deliver each packet to the topologically nearest. GeoDNS is controllable but coarse and slow to fail over; anycast fails over at BGP speed but gives less control over load.]{.short}

| | GeoDNS | Anycast |
|---|---|---|
| Choice made by | DNS server, by resolver address | BGP, by AS path |
| Failover | Waits for TTL and health checks | Withdraw the route: seconds |
| Accuracy | Wrong when the resolver is far from the user | Nearest by network path, not by distance |
| Load control | Fine (weights per region) | Coarse (prepending, communities) |
| Risk | Stale caches | A route flap can move live TCP sessions |

**Practice.** Many CDNs combine them: anycast for DNS and TCP entry, DNS steering for capacity.
:::

::: q
### Q12.39 Design an L4 load balancer for 1 million new connections per second.
[AMAZON · GOOGLE · ARISTA · TECH-2 · ■■■ · T]{.meta}

[30-second answer: announce one virtual IP from several balancer nodes; routers spread flows over them by ECMP on the five-tuple; each node picks a backend by consistent hashing so that most flows survive a change, forwards by direct server return, and health-checks backends.]{.short}

**Estimate (assumptions stated).** About 10 inbound packets per connection gives 10 million packets per second; at 5 million per second per software node (XDP or DPDK on 25 GbE), 2 nodes suffice and 4 give N+2. With 60-second connections, 60 × 10<sup>6</sup> = 60 million live connections; at 64 bytes of state each that is 3.84 GB spread over the nodes. **Design points.** Direct server return lets replies bypass the balancer; consistent hashing (Maglev) limits remapping when a backend or a node fails; connection draining before removal; SYN-flood protection at the edge. **Follow-up.** L7 balancing terminates TLS and routes by URL, at lower throughput. See [Pillar 5](#ch5){.ref}.
:::

::: q
### Q12.40 How would you make the campus network survive a core switch failure without users noticing?
[CISCO · JUNIPER · NOKIA · TECH-2 · ■■■ · T]{.meta}

[30-second answer: remove every single point of failure above the access layer and make detection fast: dual cores, dual uplinks from each distribution pair, routed links with equal-cost paths, BFD for failure detection in about 300 ms, and a first-hop redundancy protocol with tuned timers. Traffic then reroutes in well under a second, which TCP sessions survive.]{.short}

**Timeline.** BFD with a 100 ms interval and multiplier 3 detects the loss in 300 ms; OSPF recomputes in tens of milliseconds; ECMP already holds the alternate path, so only flows on the dead switch move; the gateway moves to its standby within the tuned hold time (for example 750 ms). A TCP sender sees a retransmission delay, not a reset, because the minimum retransmission timeout is about 200 ms and a connection fails only after many. **Also.** Stateful firewall pair with synchronised sessions; dual power feeds; spanning-tree root placed on the active gateway; a tested maintenance procedure. **Mistake.** Relying on default spanning-tree timers, which take seconds. See [§12.11](#s12-11){.ref} and [§4.8](#s4-8){.ref}.
:::
:::
:::
