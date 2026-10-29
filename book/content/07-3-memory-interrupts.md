::: {.p7}

## [7.7]{.sec}Memory management and virtual memory [Must · ■■□]{.tag} {#s7-7}

Each process addresses memory through *virtual addresses*, and a hardware unit, the *memory-management unit* (MMU), translates them to *physical addresses* using tables the kernel maintains. Memory is divided into fixed-size *pages* (4 KB on x86-64 and most ARM systems) in the virtual space and equal-sized *frames* in physical memory; a *page table* maps each virtual page number (VPN) to a physical frame number (PFN). Three benefits follow. Processes are isolated, since a process can name only the pages its table maps. Memory can be fragmented physically yet contiguous virtually. And the kernel can defer work: a page need not exist until it is first used.

::: bigidea
Virtual memory is chiefly a translation-and-protection mechanism; using disk as spare memory is a secondary benefit, and a process that never touches a page never owns a frame for it.
:::

### Translating an address

A virtual address splits into a page number and an *offset* within the page. With 4 KB pages the offset takes the low 12 bits (2¹² = 4096), and the translation replaces the page number by the frame number and keeps the offset.

::: example
**Translate 0x00403ABC in a 32-bit address space with 4 KB pages.** The page table maps VPN 0x00403 to PFN 0x1A2.

1. Offset = the low 12 bits = 0xABC. VPN = the address shifted right by 12 = 0x00403.
2. Look up VPN 0x00403: PFN = 0x1A2.
3. Physical address = PFN × 4096 + offset = 0x1A2000 + 0xABC.

[Result: physical address 0x1A2ABC.]{.result}
:::

A flat table for 2²⁰ pages with 4-byte entries needs 4 MB for every process, even a tiny one. A *multi-level* table avoids this by allocating the lower levels only where addresses are in use. With a 10 + 10 + 12 split the top 10 bits index a first-level table whose entries point to second-level tables, and the next 10 bits index the second-level table; Figure 7.10 follows 0x00403ABC through it (first index 1, second index 3).

<figure>
<svg viewBox="0 0 480 235" width="480"><defs><marker id="ixl" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="axl" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><text class="lbl" x="240" y="12" text-anchor="middle">Virtual address 0x00403ABC, 4 KB pages, two-level table (10 + 10 + 12 bits)</text><rect class="box" x="20" y="22" width="100" height="24" rx="0"/><text class="mono" x="70.0" y="37.0" text-anchor="middle">L1 index = 1</text><rect class="box" x="120" y="22" width="100" height="24" rx="0"/><text class="mono" x="170.0" y="37.0" text-anchor="middle">L2 index = 3</text><rect class="fill" x="220" y="22" width="120" height="24" rx="0"/><text class="mono" x="280.0" y="37.0" text-anchor="middle">offset = 0xABC</text><text class="sm" x="70" y="58" text-anchor="middle">10 bits</text><text class="sm" x="170" y="58" text-anchor="middle">10 bits</text><text class="sm" x="280" y="58" text-anchor="middle">12 bits</text><text class="sm" x="60" y="84" text-anchor="middle">L1 table (per process)</text><rect class="box" x="20" y="90" width="80" height="20" rx="0"/><text class="sm" x="60.0" y="103.0" text-anchor="middle">[0]  ...</text><rect class="box" x="20" y="110" width="80" height="20" rx="0" style="fill:#FFF4C2"/><text class="sm" x="60.0" y="123.0" text-anchor="middle">[1]  to L2 table</text><rect class="box" x="20" y="130" width="80" height="20" rx="0"/><text class="sm" x="60.0" y="143.0" text-anchor="middle">[2]  ...</text><rect class="box" x="20" y="150" width="80" height="20" rx="0"/><text class="sm" x="60.0" y="163.0" text-anchor="middle">[3]  ...</text><text class="sm" x="190" y="84" text-anchor="middle">L2 table</text><rect class="box" x="150" y="90" width="90" height="20" rx="0"/><text class="sm" x="195.0" y="103.0" text-anchor="middle">[0]  ...</text><rect class="box" x="150" y="110" width="90" height="20" rx="0"/><text class="sm" x="195.0" y="123.0" text-anchor="middle">[1]  ...</text><rect class="box" x="150" y="130" width="90" height="20" rx="0"/><text class="sm" x="195.0" y="143.0" text-anchor="middle">[2]  ...</text><rect class="box" x="150" y="150" width="90" height="20" rx="0" style="fill:#FFF4C2"/><text class="sm" x="195.0" y="163.0" text-anchor="middle">[3]  PFN 0x1A2</text><rect class="box" x="150" y="170" width="90" height="20" rx="0"/><text class="sm" x="195.0" y="183.0" text-anchor="middle">[4]  ...</text><path class="acc" d="M100,130 L150,110 " marker-end="url(#axl)" /><path class="acc" d="M240,150 L290,150 L290,196" marker-end="url(#axl)" /><rect class="box" x="250" y="196" width="120" height="24" rx="0" style="fill:#FFF4C2"/><text class="mono" x="310.0" y="211.0" text-anchor="middle">PA = 0x1A2ABC</text><text class="sm" x="300" y="140" text-anchor="start">PFN 0x1A2</text><text class="sm" x="300" y="232" text-anchor="middle"></text><path class="lg" d="M280,58 L330,58 L330,170 L330,196" marker-end="url(#ixl)" stroke-dasharray="3 2"/><text class="sm" x="336" y="130" text-anchor="start">offset copied</text><rect class="fill" x="380" y="70" width="90" height="54" rx="0"/><text class="sm" x="425.0" y="96.0" text-anchor="middle">TLB</text><text class="sm" x="425.0" y="105.0" text-anchor="middle">VPN 0x00403 to 0x1A2</text><text class="sm" x="425" y="138" text-anchor="middle">hit: skip both table reads</text><text class="sm" x="425" y="148" text-anchor="middle">miss: walk, then cache</text><text class="sm" x="20" y="205" text-anchor="start">Three memory reads</text><text class="sm" x="20" y="215" text-anchor="start">on a TLB miss (L1, L2,</text><text class="sm" x="20" y="225" text-anchor="start">the data), one on a hit.</text></svg>
<figcaption><b>Figure 7.10</b> Two-level translation of 0x00403ABC. The TLB caches finished translations so that a hit skips both table reads.</figcaption>
</figure>

::: example
**Page-table memory for a process using 8 MB.** Each second-level table (1024 entries × 4 bytes = 4 KB) maps 1024 pages = 4 MB.

1. 8 MB needs two second-level tables if the region is contiguous and aligned: 2 × 4 KB.
2. One first-level table: 4 KB.

[Result: 12 KB of page tables, against 4 MB for the flat table.]{.result}
:::

On x86-64 with 48-bit virtual addresses, the same idea uses four levels of 9 bits each (512 eight-byte entries per table) plus the 12-bit offset: 4 × 9 + 12 = 48 bits.

### The TLB and effective access time

Walking the table costs memory reads, so the MMU caches recent translations in the *translation lookaside buffer* (TLB), a small associative cache. A *hit* gives the frame at once; a *miss* triggers a table walk, after which the entry is cached. Because a process switch changes the page tables, the TLB entries are flushed or tagged with an address-space identifier, which is the hidden cost of switching processes ([7.3](#s7-3){.ref}).

::: example
**Effective access time (EAT).** TLB lookup 1 ns, memory access 100 ns, TLB hit ratio 95 %, single-level table.

1. A hit costs the lookup and one memory access: 1 + 100 = 101 ns.
2. A miss costs the lookup, one table read and one data read: 1 + 100 + 100 = 201 ns.
3. EAT = 0.95 × 101 + 0.05 × 201 = 95.95 + 10.05.

[Result: EAT = 106 ns, 6 % above the raw memory time. At a 50 % hit ratio it would be 151 ns.]{.result}
:::

### Page faults

A *page fault* is the exception raised when the MMU cannot translate an address. The kernel's handler decides what kind it is. A *minor* fault finds the page already in memory or needing only a zeroed frame (first touch of `malloc`'d memory, a copy-on-write copy); it costs microseconds. A *major* fault must read the page from disk (a file mapping, or swap), costing milliseconds. An *invalid* fault is an access to an unmapped address or one that violates permissions, and the kernel delivers SIGSEGV.

::: lab
`LAB 7.7 · 10 MIN` Watch first-touch page faults. The program reads `getrusage` before and after a 100 MB `malloc` and a `memset`.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/resource.h>

static long faults(void)
{
    struct rusage r;
    getrusage(RUSAGE_SELF, &r);
    return r.ru_minflt;                    /* minor faults: no disk I/O needed */
}

int main(void)
{
    size_t n = 100u << 20;                 /* 100 MB */
    long f0 = faults();
    char *p = malloc(n);                   /* reserves address space only */
    long f1 = faults();
    memset(p, 1, n);                       /* first touch of every page */
    long f2 = faults();
    printf("after malloc: +%ld faults\n", f1 - f0);
    printf("after touching 100 MB: +%ld faults (%zu pages of 4 KB)\n", f2 - f1, n / 4096);
    printf("last byte = %d\n", p[n - 1]);    /* use the data so the optimiser keeps it */
    free(p);
    return 0;
}
```

```
$ gcc -O1 pf.c -o pf && ./pf
after malloc: +3 faults
after touching 100 MB: +25600 faults (25600 pages of 4 KB)
```

**What you should notice:** `malloc` of 100 MB costs almost nothing; the 25,600 faults arrive only when the pages are first written, one per 4 KB page. With transparent huge pages enabled the count is lower, since one fault then maps 2 MB.
:::

### Copy-on-write, mmap and thrashing

After `fork()` the child's page table points at the parent's frames, and both sets of entries are marked read-only. The first write by either process raises a fault; the kernel copies that one frame, maps the copy writable for the writer, and resumes. Hence `fork` followed by `exec` copies almost nothing. `mmap` maps a file, or anonymous zeroed memory, into the address space, and pages are loaded on demand; `malloc` uses it for large blocks. When the total of the processes' actively used pages (their *working sets*) exceeds physical memory, pages are evicted just before they are needed again and the system spends its time faulting: this is *thrashing*.

### Page replacement

When no frame is free, the kernel must evict a page. *FIFO* evicts the oldest-loaded page; *LRU* (least recently used) evicts the page unused for longest; *Optimal* evicts the page whose next use is furthest in the future, which needs knowledge of the future and serves as a bound. Real kernels approximate LRU with the *clock* algorithm: frames sit on a circle, each with a reference bit set by the hardware on use; a hand sweeps, clearing set bits and evicting the first frame whose bit is already clear.

Take the reference string 7 0 1 2 0 3 0 4 2 3 0 3 2 with three frames. The table shows the resident pages after each reference (oldest first for FIFO and LRU; slot order for Optimal), and F marks a fault.

| Ref | FIFO | | LRU | | Optimal | |
|---|---|---|---|---|---|---|
| 7 | 7 | F | 7 | F | 7 | F |
| 0 | 7 0 | F | 7 0 | F | 7 0 | F |
| 1 | 7 0 1 | F | 7 0 1 | F | 7 0 1 | F |
| 2 | 0 1 2 | F | 0 1 2 | F | 2 0 1 | F |
| 0 | 0 1 2 | | 1 2 0 | | 2 0 1 | |
| 3 | 1 2 3 | F | 2 0 3 | F | 2 0 3 | F |
| 0 | 2 3 0 | F | 2 3 0 | | 2 0 3 | |
| 4 | 3 0 4 | F | 3 0 4 | F | 2 4 3 | F |
| 2 | 0 4 2 | F | 0 4 2 | F | 2 4 3 | |
| 3 | 4 2 3 | F | 4 2 3 | F | 2 4 3 | |
| 0 | 2 3 0 | F | 2 3 0 | F | 2 0 3 | F |
| 3 | 2 3 0 | | 2 0 3 | | 2 0 3 | |
| 2 | 2 3 0 | | 0 3 2 | | 2 0 3 | |
| **Faults** | | **10** | | **9** | | **7** |

*Bélády's anomaly* is the surprising fact that for FIFO more frames can cause more faults. On the string 1 2 3 4 1 2 5 1 2 3 4 5, FIFO has 9 faults with three frames and 10 with four. LRU and Optimal are *stack algorithms*: the pages held with n frames are always a subset of those held with n + 1, so they cannot show the anomaly.

### Stack, heap and a small allocator

The stack is fast to allocate because allocation is moving one register, the stack pointer, and freeing is moving it back; memory is reused immediately and is likely to be in cache. The heap must find a block of the right size among live and freed ones, which costs a search and risks fragmentation. *Internal fragmentation* is waste inside an allocated block (rounding up to 16 bytes); *external fragmentation* is free memory scattered in pieces too small to use. Structure padding and alignment, the other memory-layout question asked with these, are taught in [Pillar 2](#s2-7){.ref}.

Embedded targets often have no `malloc`, and Arista and Qualcomm ask candidates to design one. The usual answer is a *free list* over a fixed arena: each block begins with a header holding its size and a free flag; `malloc` takes the first block that fits (first fit) and splits off the remainder; `free` marks the block free and merges it with free neighbours (*coalescing*) so that fragments do not accumulate.

```c
#include <stddef.h>
#include <stdio.h>

#define ARENA 4096
struct hdr { size_t size; int free; struct hdr *next; };   /* 24 bytes on LP64 */

static _Alignas(16) unsigned char arena[ARENA];
static struct hdr *first;

static size_t round16(size_t n) { return (n + 15) & ~(size_t)15; }

void *a_malloc(size_t n)
{
    if (!first) {                               /* one big free block */
        first = (struct hdr *)arena;
        *first = (struct hdr){ ARENA - sizeof *first, 1, NULL };
    }
    n = round16(n);
    for (struct hdr *h = first; h; h = h->next) {
        if (!h->free || h->size < n) continue;  /* first fit */
        if (h->size >= n + sizeof *h + 16) {    /* split the remainder */
            struct hdr *r = (struct hdr *)((unsigned char *)(h + 1) + n);
            *r = (struct hdr){ h->size - n - sizeof *h, 1, h->next };
            h->size = n;
            h->next = r;
        }
        h->free = 0;
        return h + 1;
    }
    return NULL;
}

void a_free(void *p)
{
    if (!p) return;
    ((struct hdr *)p - 1)->free = 1;
    for (struct hdr *h = first; h && h->next; ) {   /* coalesce neighbours */
        if (h->free && h->next->free) {
            h->size += sizeof *h + h->next->size;
            h->next = h->next->next;
        } else h = h->next;
    }
}

int main(void)
{
    void *a = a_malloc(100), *b = a_malloc(200), *c = a_malloc(50);
    a_free(b); a_free(a);                       /* a and b merge into one hole */
    void *d = a_malloc(300);                    /* fits only in the merged hole */
    printf("a=%p d=%p same start: %s\n", a, d, a == d ? "yes" : "no");
    a_free(c); a_free(d);
    size_t total = 0; int blocks = 0;
    for (struct hdr *h = first; h; h = h->next) { total += h->size; blocks++; }
    printf("blocks=%d, free bytes=%zu\n", blocks, total);
    return 0;
}
```

```
$ gcc -Wall -Wextra alloc.c -o alloc && ./alloc
a=0x55afdad11038 d=0x55afdad11038 same start: yes
blocks=1, free bytes=4072
```

Freeing `a` and `b` creates one merged hole that the 300-byte request then fits; freeing everything coalesces the arena into a single block of 4096 − 24 bytes. A production allocator adds size classes, thread-local caches and a boundary tag at the block's end so that coalescing needs no list walk; the kernel's *slab allocator* keeps per-type caches of equal-sized objects, which is why `sk_buff` allocation is quick ([7.12](#s7-12){.ref}).

::: trap
*Claim:* "`malloc(100 MB)` gives me 100 MB of physical memory." *Why it is wrong:* it reserves virtual address space; frames are assigned at the first write of each page, as the lab shows, and the kernel may overcommit. *Correct statement:* `malloc` returns virtual memory, and physical frames arrive on first touch.
:::

::: lens
[CISCO · JUNIPER · QUALCOMM · ARISTA]{.co}

"What is virtual memory and why is it needed?" is asked almost everywhere, with "what happens on a TLB miss, and on a page fault?" as the follow-up. A strong answer names isolation and translation first, draws the VPN and offset split, and separates the TLB-miss path (hardware or kernel walks the table) from the page-fault path (the kernel loads or creates the page, or kills the process). Qualcomm and Arista add "design `malloc` for a system without an OS", which expects a header format, first-fit with splitting, and coalescing on free. Follow-ups: copy-on-write after `fork`, and why a TLB flush hurts.
:::

::: check
1. How many bits of a 32-bit virtual address are the offset with 16 KB pages? [^c77-1]
2. Which page-replacement algorithm shows Bélády's anomaly? [^c77-2]
3. Why does `fork` followed by `exec` cost little? [^c77-3]
:::

[^c77-1]: 14, since 2¹⁴ = 16384; the remaining 18 bits are the page number.
[^c77-2]: FIFO. Stack algorithms such as LRU and Optimal cannot show it.
[^c77-3]: Copy-on-write: the pages are shared and not copied, and `exec` discards the child's address space almost at once.

## [7.8]{.sec}Interrupts, system calls and DMA [Must · ■■□]{.tag} {#s7-8}

A device signals that it needs attention by raising an *interrupt*. The interrupt controller (the APIC on x86, the GIC on ARM) selects a CPU; the CPU finishes the current instruction, saves enough state to resume, switches to kernel mode and jumps through a *vector table* to the handler registered for that interrupt line, the *interrupt service routine* (ISR). When the ISR ends, a special return instruction (`iret` or `eret`) restores the interrupted code. *Exceptions* (page fault, divide by zero) use the same mechanism but arise from the running instruction, and a *system call* is a deliberate software-triggered entry.

<figure>
<svg viewBox="0 0 480 120" width="480"><defs><marker id="iir" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="air" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><rect class="box" x="6" y="30" width="72" height="52" rx="0"/><text class="lbl" x="42.0" y="59.0" text-anchor="middle"></text><text class="sm" x="42" y="46" text-anchor="middle">device</text><text class="sm" x="42" y="56" text-anchor="middle">raises line</text><line class="ln" x1="78" y1="56" x2="84" y2="56" marker-end="url(#iir)" /><rect class="box" x="84" y="30" width="72" height="52" rx="0"/><text class="lbl" x="120.0" y="59.0" text-anchor="middle"></text><text class="sm" x="120" y="46" text-anchor="middle">controller</text><text class="sm" x="120" y="56" text-anchor="middle">(APIC, GIC)</text><text class="sm" x="120" y="66" text-anchor="middle">picks CPU</text><line class="ln" x1="156" y1="56" x2="162" y2="56" marker-end="url(#iir)" /><rect class="box" x="162" y="30" width="72" height="52" rx="0"/><text class="lbl" x="198.0" y="59.0" text-anchor="middle"></text><text class="sm" x="198" y="46" text-anchor="middle">CPU saves</text><text class="sm" x="198" y="56" text-anchor="middle">state, reads</text><text class="sm" x="198" y="66" text-anchor="middle">vector</text><line class="ln" x1="234" y1="56" x2="240" y2="56" marker-end="url(#iir)" /><rect class="box" x="240" y="30" width="72" height="52" rx="0" style="fill:#FFF4C2"/><text class="lbl" x="276.0" y="59.0" text-anchor="middle"></text><text class="sm" x="276" y="46" text-anchor="middle">ISR (top</text><text class="sm" x="276" y="56" text-anchor="middle">half):</text><text class="sm" x="276" y="66" text-anchor="middle">acknowledge,</text><text class="sm" x="276" y="76" text-anchor="middle">queue work</text><line class="ln" x1="312" y1="56" x2="318" y2="56" marker-end="url(#iir)" /><rect class="box" x="318" y="30" width="72" height="52" rx="0"/><text class="lbl" x="354.0" y="59.0" text-anchor="middle"></text><text class="sm" x="354" y="46" text-anchor="middle">bottom half</text><text class="sm" x="354" y="56" text-anchor="middle">runs later</text><line class="ln" x1="390" y1="56" x2="396" y2="56" marker-end="url(#iir)" /><rect class="box" x="396" y="30" width="72" height="52" rx="0"/><text class="lbl" x="432.0" y="59.0" text-anchor="middle"></text><text class="sm" x="432" y="46" text-anchor="middle">iret / eret:</text><text class="sm" x="432" y="56" text-anchor="middle">resume</text><text class="sm" x="240" y="104" text-anchor="middle">Steps 1 to 4 and 6 are fast and run with the interrupt masked; step 5 is ordinary scheduled kernel work.</text></svg>
<figcaption><b>Figure 7.11</b> The life of an interrupt. Only the shaded step, the ISR, is time-critical; the heavy work is deferred.</figcaption>
</figure>

An ISR runs while other interrupts may be masked, so it must be short. It acknowledges the device, grabs what cannot wait (reads a status register, notes the packet's buffer) and schedules the rest as a *bottom half*. Linux offers softirqs, tasklets and workqueues for this. The ISR itself, the *top half*, runs in *interrupt context*, where there is no process to put to sleep: it may not block, take a mutex, or call `kmalloc(GFP_KERNEL)`, which can sleep; it uses spinlocks and `GFP_ATOMIC`.

| | Top half (ISR) | Softirq / tasklet | Workqueue |
|---|---|---|---|
| Context | interrupt | softirq (interrupt-like) | process (a kernel thread) |
| May sleep? | no | no | yes |
| May be interrupted by another interrupt? | by higher-priority ones only | yes | yes, and pre-empted by the scheduler |
| Example in a NIC driver | acknowledge, `napi_schedule()` | NAPI poll, protocol processing | reset after a hardware error |

*Direct memory access* (DMA) lets a device read and write main memory without the CPU copying each word. The driver prepares a *descriptor ring*, a circular array of descriptors each holding the address and length of a buffer; it programs the NIC with the ring's base address. The NIC fills buffers and advances its position, the driver follows behind, cleans completed descriptors and hands fresh buffers back (Figure 7.12). On a CPU with caches the driver must also keep the cache consistent with the device's writes, which the kernel's DMA-mapping API arranges.

<figure>
<svg viewBox="0 0 480 150" width="480"><defs><marker id="idr" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="adr" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><rect class="box" x="20" y="40" width="52" height="30" rx="0"/><text class="mono" x="46.0" y="58.0" text-anchor="middle">d0</text><rect class="fill" x="28" y="96" width="36" height="20" rx="0"/><text class="sm" x="46.0" y="109.0" text-anchor="middle">buf</text><line class="lg" x1="46.0" y1="70" x2="46.0" y2="96" /><rect class="box" x="72" y="40" width="52" height="30" rx="0"/><text class="mono" x="98.0" y="58.0" text-anchor="middle">d1</text><rect class="fill" x="80" y="96" width="36" height="20" rx="0"/><text class="sm" x="98.0" y="109.0" text-anchor="middle">buf</text><line class="lg" x1="98.0" y1="70" x2="98.0" y2="96" /><rect class="box" x="124" y="40" width="52" height="30" rx="0" style="fill:#FFF4C2"/><text class="mono" x="150.0" y="58.0" text-anchor="middle">d2</text><rect class="fill" x="132" y="96" width="36" height="20" rx="0"/><text class="sm" x="150.0" y="109.0" text-anchor="middle">buf</text><line class="lg" x1="150.0" y1="70" x2="150.0" y2="96" /><rect class="box" x="176" y="40" width="52" height="30" rx="0" style="fill:#FFF4C2"/><text class="mono" x="202.0" y="58.0" text-anchor="middle">d3</text><rect class="fill" x="184" y="96" width="36" height="20" rx="0"/><text class="sm" x="202.0" y="109.0" text-anchor="middle">buf</text><line class="lg" x1="202.0" y1="70" x2="202.0" y2="96" /><rect class="box" x="228" y="40" width="52" height="30" rx="0" style="fill:#FFF4C2"/><text class="mono" x="254.0" y="58.0" text-anchor="middle">d4</text><rect class="fill" x="236" y="96" width="36" height="20" rx="0"/><text class="sm" x="254.0" y="109.0" text-anchor="middle">buf</text><line class="lg" x1="254.0" y1="70" x2="254.0" y2="96" /><rect class="box" x="280" y="40" width="52" height="30" rx="0"/><text class="mono" x="306.0" y="58.0" text-anchor="middle">d5</text><rect class="fill" x="288" y="96" width="36" height="20" rx="0"/><text class="sm" x="306.0" y="109.0" text-anchor="middle">buf</text><line class="lg" x1="306.0" y1="70" x2="306.0" y2="96" /><rect class="box" x="332" y="40" width="52" height="30" rx="0"/><text class="mono" x="358.0" y="58.0" text-anchor="middle">d6</text><rect class="fill" x="340" y="96" width="36" height="20" rx="0"/><text class="sm" x="358.0" y="109.0" text-anchor="middle">buf</text><line class="lg" x1="358.0" y1="70" x2="358.0" y2="96" /><rect class="box" x="384" y="40" width="52" height="30" rx="0"/><text class="mono" x="410.0" y="58.0" text-anchor="middle">d7</text><rect class="fill" x="392" y="96" width="36" height="20" rx="0"/><text class="sm" x="410.0" y="109.0" text-anchor="middle">buf</text><line class="lg" x1="410.0" y1="70" x2="410.0" y2="96" /><text class="lbl" x="240" y="14" text-anchor="middle">RX descriptor ring (power-of-two size), each descriptor points at a packet buffer</text><line class="acc" x1="124" y1="30" x2="124" y2="40" marker-end="url(#adr)" /><text class="sm" x="124" y="24" text-anchor="middle">driver next to clean</text><line class="acc" x1="280" y1="30" x2="280" y2="40" marker-end="url(#adr)" /><text class="sm" x="280" y="24" text-anchor="middle">NIC next to fill</text><text class="sm" x="240" y="134" text-anchor="middle">Shaded: filled by the NIC, waiting for the driver. Unshaded: free buffers the driver has given to the NIC. Indices wrap.</text><text class="sm" x="240" y="144" text-anchor="middle"></text></svg>
<figcaption><b>Figure 7.12</b> An RX descriptor ring. The NIC fills descriptors up to its pointer; the driver processes behind it and refills. Both indices wrap.</figcaption>
</figure>

### Why one interrupt per packet fails

A 10 Gb/s link carrying minimum-size frames moves 64 bytes plus 20 bytes of preamble and inter-frame gap per packet: 84 bytes = 672 bits, hence 10 × 10⁹ / 672 ≈ 14.88 million packets per second, one every 67 ns. An interrupt costs more than that, so a CPU taking one interrupt per packet would do nothing else; at the worst it would be *livelocked*, spending all its time entering and leaving ISRs. The cures are *interrupt coalescing* (the NIC raises one interrupt per batch or per timeout) and *NAPI* ([7.12](#s7-12){.ref}), which switches the device to polling under load.

| | Interrupts | Polling |
|---|---|---|
| Latency at low load | best: reacts at once | up to one polling interval |
| CPU use at low load | none while idle | wasted: the poller runs regardless |
| Behaviour at high load | overhead per event; livelock risk | efficient: events are batched |
| Used by | NICs at low rate, keyboards | NAPI under load, DPDK, busy-polling drivers |

::: lab
`LAB 7.8 · 10 MIN` Look at the machine's interrupt and receive-processing counters.

```
$ head -4 /proc/interrupts
           CPU0       CPU1       CPU2       CPU3
 26:          0          0          2          0  IO-APIC   4-edge      ttyS0
 32:          0        972          0          0  PCI-MSIX-0000:00:01.0   3-edge      virtio0-stats
$ head -1 /proc/net/softnet_stat
00039a92 00000000 00000019 ...
```

**What you should notice:** each row of `/proc/interrupts` is one interrupt line with a count per CPU; a multi-queue NIC shows one line per queue, each bound to a core, and the counts climb during an `iperf3` run. In `softnet_stat` the first three hexadecimal columns are packets processed, packets dropped, and `time_squeeze`, the number of times the receive poll ran out of budget with work left; here 0x39a92 packets, 0 drops, 0x19 = 25 squeezes.
:::

::: trap
*Claim:* "An ISR can call a function that takes a mutex, provided the mutex is rarely contended." *Why it is wrong:* if the mutex is held, the ISR would sleep, but an interrupt handler has no task context to sleep in, and the kernel panics or deadlocks. *Correct statement:* in interrupt context use spinlocks (with interrupts disabled while the lock is held, to avoid self-deadlock) and atomic allocations.
:::

::: lens
[QUALCOMM · BROADCOM · CISCO · JUNIPER]{.co}

"Describe what happens from the device signal to the end of the ISR" and "why can't you sleep in an ISR?" are reported firmware and driver questions, and "polling or interrupts?" was reported for a Cisco internship. A strong answer lists the steps in the figure, states the top-half rule, mentions deferral and DMA, and gives the polling trade-off with the packet-rate arithmetic above. Follow-ups: what NAPI is, and what `volatile` and memory barriers do for device registers ([7.13](#s7-13){.ref}).
:::

::: check
1. Why must an ISR be short? [^c78-1]
2. What does DMA save the CPU from? [^c78-2]
:::

[^c78-1]: Interrupts of equal or lower priority are held off while it runs, so a long ISR delays other devices and the scheduler's timer.
[^c78-2]: Copying every word between the device and memory; the CPU only sets up descriptors and handles the completion interrupt.

## [7.9]{.sec}Inter-process communication and signals [Should · ■■□]{.tag} {#s7-9}

Processes cannot touch each other's memory, so they communicate through the kernel or through memory the kernel maps into both. A *pipe* is a one-way byte channel between related processes; a *FIFO* (named pipe) is a pipe with a name in the file system, so unrelated processes may open it; a *message queue* preserves message boundaries; *shared memory* maps the same frames into two address spaces; and a *socket* ([7.10](#s7-10){.ref}) also works across machines.

| Mechanism | Direction | Unrelated processes? | Kernel copies per message | Needs synchronisation? |
|---|---|---|---|---|
| Pipe | one way | no (shared ancestor) | 2 | no, the kernel blocks |
| FIFO | one way | yes | 2 | no |
| Message queue | any | yes | 2 | no |
| Shared memory | any | yes | 0 | yes, e.g. a process-shared mutex |
| Unix-domain socket | both | yes (same host) | 2 | no |
| Signal | notification only | yes | none, carries a number | n/a |

Shared memory is fastest because after setup no kernel call is on the data path; its price is that the processes must synchronise themselves, as threads do.

The shell pipeline `ls | wc -l` shows how the pieces combine. The parent creates a pipe, forks twice, and each child uses `dup2` to make the pipe's end its standard output or input before `exec`.

```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void)                          /* equivalent of: ls | wc -l */
{
    int fd[2];
    if (pipe(fd) < 0) { perror("pipe"); exit(1); }

    if (fork() == 0) {                  /* writer: ls */
        dup2(fd[1], STDOUT_FILENO);     /* stdout now feeds the pipe */
        close(fd[0]); close(fd[1]);     /* close the originals */
        execlp("ls", "ls", (char *)NULL);
        perror("execlp"); _exit(127);
    }
    if (fork() == 0) {                  /* reader: wc -l */
        dup2(fd[0], STDIN_FILENO);
        close(fd[0]); close(fd[1]);
        execlp("wc", "wc", "-l", (char *)NULL);
        perror("execlp"); _exit(127);
    }
    close(fd[0]); close(fd[1]);         /* parent must close, or wc never sees EOF */
    while (wait(NULL) > 0)
        ;
    return 0;
}
```

In each child, `dup2(fd[1], STDOUT_FILENO)` makes descriptor 1 refer to the pipe's write end, and the original two descriptors are closed. The parent must also close both ends: a pipe delivers end-of-file to the reader only when every write end is closed, so a forgotten copy in the parent leaves `wc` waiting for ever.

A *signal* is an asynchronous notification delivered to a process: SIGINT (Ctrl-C), SIGTERM (polite termination), SIGKILL (cannot be caught), SIGSEGV (invalid memory access), SIGCHLD (a child changed state; the standard place to reap zombies with `waitpid(-1, NULL, WNOHANG)`), and SIGPIPE (a write to a pipe or socket whose reader has gone). Because a handler can interrupt the program at any point, it may call only *async-signal-safe* functions: `write` is on the list, `printf` and `malloc` are not, since they may hold internal locks that the interrupted code already owns. The common practice is to set a flag in the handler and act on it in the main loop. A network server normally ignores SIGPIPE (`signal(SIGPIPE, SIG_IGN)`, or `MSG_NOSIGNAL` on `send`) and handles the `EPIPE` error instead.

::: check
1. Which IPC mechanism avoids kernel copies of the data? [^c79-1]
2. Why can a signal handler not safely call `printf`? [^c79-2]
:::

[^c79-1]: Shared memory, after the one-off setup; it needs explicit synchronisation.
[^c79-2]: `printf` takes an internal lock; if the signal interrupted code holding it, the handler would deadlock.

:::
