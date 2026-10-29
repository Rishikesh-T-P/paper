::: {.p12}

## [12.10]{.sec}Computer organisation for network engineers [Should · ■■□]{.tag} {#s12-10}

Computer organisation describes how a processor represents numbers, reaches memory and overlaps instructions. Qualcomm, Broadcom and Arista ask about it because a packet processor is a small computer whose speed depends on exactly these three things. Endianness and the memory layout of a process are taught in [§2.9](#s2-9){.ref} and [§7.7](#s7-7){.ref}; we do not repeat them, and keep to number representation, caches, pipelines and the memory hierarchy.

::: bigidea
Memory is slow and the processor is fast, so almost every design in this section is a way of hiding that gap: caches by remembering, pipelines by overlapping.
:::

### Number representation

A computer stores *n*-bit integers in *two's complement*: the top bit has weight −2<sup>*n*−1</sup>, so the range is −2<sup>*n*−1</sup> to 2<sup>*n*−1</sup> − 1 (−128 to 127 for 8 bits). To negate a number, invert all bits and add one; the same adder then handles signed and unsigned values. Overflow occurs when two operands of the same sign give a result of the opposite sign.

::: example
**(a) Write −45 in 8-bit two's complement. (b) What does 100 + 50 give in 8 bits? (c) Encode 10.75 as an IEEE 754 single-precision number.**

1. (a) 45 = 0010 1101; inverted 1101 0010; plus one 1101 0011 = 0xD3. Check: 0xD3 = 211 = 256 − 45.
2. (b) 100 + 50 = 150 = 1001 0110, which read as signed is 150 − 256 = −106. Two positives gave a negative, so signed overflow occurred.
3. (c) 10.75 = 1010.11<sub>2</sub> = 1.01011 × 2<sup>3</sup>. The sign is 0; the exponent is 3 + 127 = 130 = 1000 0010; the fraction is 0101 1000 … (23 bits). Grouped: 0 10000010 01011000000000000000000.

[Result: 0xD3; −106 with overflow; 0x412C0000.]{.result}
:::

<figure>
<svg viewBox="0 0 480 80" width="480">
<rect class="fill" x="20" y="20" width="20" height="26"/>
<rect class="box" x="40" y="20" width="140" height="26"/>
<rect class="box" x="180" y="20" width="280" height="26"/>
<text class="lbl" x="30" y="37" text-anchor="middle">S</text>
<text class="lbl" x="110" y="37" text-anchor="middle">exponent, 8 bits, bias 127</text>
<text class="lbl" x="320" y="37" text-anchor="middle">fraction, 23 bits (leading 1 implied)</text>
<text class="sm" x="30" y="60" text-anchor="middle">bit 31</text>
<text class="sm" x="110" y="60" text-anchor="middle">bits 30 to 23</text>
<text class="sm" x="320" y="60" text-anchor="middle">bits 22 to 0</text>
<text class="sm" x="240" y="76" text-anchor="middle">value = (−1)^S × 1.fraction × 2^(exponent − 127)</text>
</svg>
<figcaption><b>Figure 12.8</b> IEEE 754 single precision. Double precision uses 11 exponent bits (bias 1,023) and 52 fraction bits.</figcaption>
</figure>

Two consequences matter in interviews. Floating-point numbers are approximations (0.1 has no exact binary form), so equality tests on them are unsafe. Further, a 32-bit float holds integers exactly only up to 2<sup>24</sup>, so counters and byte totals must be integers. Conversions between binary, hex and dotted decimal are taught with subnetting in [§3.4](#s3-4){.ref}: for example 0xC0A80101 is 192.168.1.1.

### Memory hierarchy

No memory is both large and fast, so computers stack several. Each level holds a subset of the one below it, and a program that reuses nearby data (*locality*) sees mostly the fast levels. Temporal locality means recently used items are used again; spatial locality means neighbours of a used item are used soon.

| Level | Typical size | Typical latency | Note |
|---|---|---|---|
| Registers | under 1 KB | about 0.3 ns | Inside the core |
| L1 cache | 32 to 64 KB | about 1 ns | Per core, split instruction and data |
| L2 cache | 256 KB to 2 MB | about 4 ns | Per core |
| L3 cache | 8 to 64 MB | 10 to 40 ns | Shared |
| DRAM | 8 to 512 GB | 80 to 100 ns | Main memory |
| NVMe SSD | 0.5 to 8 TB | 10 to 100 µs | About 1,000 times slower than DRAM |
| Network, same data centre | n/a | about 0.5 ms round trip | See [Pillar 5](#ch5){.ref} |

These are orders of magnitude, not specifications; what an interviewer wants is the ratios, namely that each level costs about ten to a hundred times more than the one above.

### Cache organisation

A cache holds *blocks* (lines) of, typically, 64 bytes. An address is split into three fields. The *offset* selects the byte within a block: log<sub>2</sub>(block size) bits. The *index* selects the set: log<sub>2</sub>(number of sets) bits. The *tag*, the remaining high bits, is stored with the block and compared to confirm a hit.

| Mapping | Where a block may go | Strength | Weakness |
|---|---|---|---|
| Direct-mapped | Exactly one line (index = block mod lines) | Fast, simple | Conflict misses |
| *k*-way set-associative | Any of *k* lines in one set | Balanced; common | Comparators in parallel |
| Fully associative | Any line | No conflict misses | Costly; used in TLBs and TCAM-like structures |

<figure>
<svg viewBox="0 0 480 84" width="480">
<rect class="box" x="20" y="14" width="190" height="28"/>
<rect class="fill" x="210" y="14" width="140" height="28"/>
<rect class="box" x="350" y="14" width="110" height="28"/>
<text class="lbl" x="115" y="32" text-anchor="middle">tag: 19 bits</text>
<text class="lbl" x="280" y="32" text-anchor="middle">index: 7 bits</text>
<text class="lbl" x="405" y="32" text-anchor="middle">offset: 6 bits</text>
<text class="sm" x="20" y="58">bit 31</text><text class="sm" x="460" y="58" text-anchor="end">bit 0</text>
<text class="sm" x="240" y="76" text-anchor="middle">32 KB, 4-way, 64 B blocks, 32-bit address</text>
</svg>
<figcaption><b>Figure 12.9</b> The address split of the worked example below; the index picks one of 128 sets, and four tags are compared at once.</figcaption>
</figure>

::: example
**A 32 KB, 4-way set-associative cache has 64-byte blocks and a 32-bit address. Find the three fields.**

1. Offset: 64 = 2<sup>6</sup>, so 6 bits.
2. Number of blocks = 32,768 / 64 = 512; sets = 512 / 4 = 128 = 2<sup>7</sup>, so 7 index bits.
3. Tag = 32 − 7 − 6 = 19 bits.

[Result: tag 19, index 7, offset 6.]{.result}
:::

::: example
**Block addresses 3, 11, 3, 19, 11 are accessed in an 8-block cache that starts empty. Count the hits for direct-mapped, 2-way (LRU) and fully associative (LRU).**

1. Direct-mapped: index = address mod 8. All of 3, 11 and 19 map to line 3, so each access evicts the previous block: 0 hits.
2. 2-way: 4 sets, index = address mod 4, so all map to set 3, which holds two blocks. Sequence: 3 miss, 11 miss, 3 hit, 19 miss (evicts 11, the least recently used), 11 miss (evicts 3): 1 hit.
3. Fully associative: all eight lines are free to hold them, so only 3 distinct misses occur: 3, 11, 19 miss; the second 3 and the second 11 hit: 2 hits.

[Result: 0, 1 and 2 hits. More associativity removes conflict misses.]{.result}
:::

Performance is summarised by the *average memory access time*: AMAT = hit time + miss rate × miss penalty. With a 1 ns hit, a 5% miss rate and a 100 ns penalty, AMAT = 1 + 0.05 × 100 = 6 ns, so the cache hides most but not all of the DRAM delay. On a write, a *write-through* cache updates memory at once (simple, high traffic); a *write-back* cache marks the line dirty and writes it on eviction (less traffic, more complexity). Routers use content-addressable memory (TCAM) for longest-prefix match because it compares a key against every entry in one cycle, at much higher cost and power per bit than SRAM; the trade-off is solved in [Q12.33](#ps12){.ref}.

### Pipelining

A pipeline overlaps the stages of consecutive instructions, as a car factory overlaps its assembly stations. The classic five-stage RISC pipeline has *fetch*, *decode*, *execute*, *memory* and *write-back*. With *k* stages and *n* instructions the pipeline takes *k* + (*n* − 1) cycles instead of *kn*, so the speedup is *kn*/(*k* + *n* − 1). For 100 instructions on five stages: 500/104 ≈ 4.8, approaching *k* as *n* grows. Switch ASICs use the same idea: a packet flows through parser and match-action stages, and one packet completes per clock.

| Hazard | Cause | Remedy |
|---|---|---|
| Structural | Two instructions need the same hardware in one cycle | Duplicate the unit (separate instruction and data caches) |
| Data (read after write) | An instruction needs a result not yet written | Forwarding; stall one cycle for a load followed by a use |
| Control | A branch changes the next instruction | Branch prediction; flush on a wrong guess |

<figure>
<svg viewBox="0 0 480 120" width="480">
<text class="sm" x="62" y="12" text-anchor="end">cycle</text>
<text class="sm" x="82" y="12" text-anchor="middle">1</text><text class="sm" x="122" y="12" text-anchor="middle">2</text><text class="sm" x="162" y="12" text-anchor="middle">3</text><text class="sm" x="202" y="12" text-anchor="middle">4</text><text class="sm" x="242" y="12" text-anchor="middle">5</text><text class="sm" x="282" y="12" text-anchor="middle">6</text><text class="sm" x="322" y="12" text-anchor="middle">7</text><text class="sm" x="362" y="12" text-anchor="middle">8</text>
<text class="mono" x="62" y="38" text-anchor="end">lw  R1,0(R2)</text>
<text class="mono" x="62" y="68" text-anchor="end">add R3,R1,R4</text>
<text class="mono" x="62" y="98" text-anchor="end">sub R5,R6,R7</text>
<g class="lbl" text-anchor="middle">
<rect class="box" x="64" y="24" width="36" height="20"/><text x="82" y="38">IF</text>
<rect class="box" x="104" y="24" width="36" height="20"/><text x="122" y="38">ID</text>
<rect class="box" x="144" y="24" width="36" height="20"/><text x="162" y="38">EX</text>
<rect class="box" x="184" y="24" width="36" height="20"/><text x="202" y="38">MEM</text>
<rect class="box" x="224" y="24" width="36" height="20"/><text x="242" y="38">WB</text>
<rect class="box" x="104" y="54" width="36" height="20"/><text x="122" y="68">IF</text>
<rect class="box" x="144" y="54" width="36" height="20"/><text x="162" y="68">ID</text>
<rect class="hl" x="184" y="54" width="36" height="20"/><text x="202" y="68" class="sm">stall</text>
<rect class="box" x="224" y="54" width="36" height="20"/><text x="242" y="68">EX</text>
<rect class="box" x="264" y="54" width="36" height="20"/><text x="282" y="68">MEM</text>
<rect class="box" x="304" y="54" width="36" height="20"/><text x="322" y="68">WB</text>
<rect class="box" x="144" y="84" width="36" height="20"/><text x="162" y="98">IF</text>
<rect class="hl" x="184" y="84" width="36" height="20"/><text x="202" y="98" class="sm">stall</text>
<rect class="box" x="224" y="84" width="36" height="20"/><text x="242" y="98">ID</text>
<rect class="box" x="264" y="84" width="36" height="20"/><text x="282" y="98">EX</text>
<rect class="box" x="304" y="84" width="36" height="20"/><text x="322" y="98">MEM</text>
<rect class="box" x="344" y="84" width="36" height="20"/><text x="362" y="98">WB</text>
</g>
<path class="acc" d="M220 44 L238 54" />
</svg>
<figcaption><b>Figure 12.10</b> A load followed at once by a use of its result: even with forwarding, the add must wait one cycle for the memory stage, so one bubble delays every later instruction.</figcaption>
</figure>

### Interrupts, polling and the NIC

When a packet arrives, the NIC copies it into memory by *DMA* (direct memory access) through a ring of descriptors and then signals the CPU. Signalling by *interrupt* costs a context switch per packet, which is ruinous at millions of packets a second, whereas *polling* wastes cycles when idle. Linux therefore uses NAPI: the first packet raises an interrupt, further interrupts are masked, and the kernel polls in batches until the ring is empty. The mechanism is taught in [§7.8](#s7-8){.ref}; the questions are in [Q12.32](#ps12){.ref}.

::: lens
[QUALCOMM · BROADCOM · ARISTA · CISCO]{.co}

Typical asks are two's complement conversions, the tag/index/offset split, and why a cache helps. A strong answer shows the arithmetic in one line and states the assumption (byte-addressed, block size in bytes). Expect "what happens on a cache miss?" as a follow-up: the line is fetched, an old line is evicted, and the pipeline stalls for the miss penalty.
:::

::: check
1. Range of a 12-bit two's complement integer. [^c12f-1]
2. A 16 KB direct-mapped cache with 32-byte blocks and 32-bit addresses: how many index bits? [^c12f-2]
3. A 6-stage pipeline runs 200 instructions with no stalls. Speedup over no pipelining? [^c12f-3]
4. AMAT with a 2 ns hit, 4% miss rate and 60 ns penalty. [^c12f-4]
:::

[^c12f-1]: −2048 to 2047.
[^c12f-2]: 16,384 / 32 = 512 blocks = 2<sup>9</sup>, so 9 bits.
[^c12f-3]: 6 × 200/(6 + 199) = 1,200/205 ≈ 5.85.
[^c12f-4]: 2 + 0.04 × 60 = 4.4 ns.

:::
