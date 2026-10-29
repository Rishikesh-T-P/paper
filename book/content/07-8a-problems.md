::: {.p7}

::: pack
## Problem Set {#ps7}

Every interview question of this pillar is solved once, here, in the compact template: a 30-second answer first, then the approach, code, follow-ups and common mistakes where they apply. Tags give the companies and round where the question was reported, the difficulty (■□□ easy, ■■□ medium, ■■■ hard), and **S** when a specific question was reported by candidates or **T** when only the topic was reported and the wording is ours. Where another pillar already solves a question in full, the entry here gives the 30-second answer and a pointer, so that nothing is solved twice.

::: problems

::: q
### Q7.1 Process versus thread: what is shared and what is not?
[CISCO · JUNIPER · QUALCOMM · ARISTA · TECH-1 · ■□□ · S]{.meta}

[30-second answer: threads of one process share its address space (code, globals, heap) and open files; each thread has its own stack, registers and thread-local storage. Processes share nothing unless set up explicitly.]{.short}

**Answer.** A process is the unit of resource ownership (address space, descriptors, signal handlers); a thread is the unit of scheduling inside it. Thread creation and switching are cheaper, and communication is a plain memory write, but there is no isolation. **Follow-ups.** The 1:1 model in Linux; `clone()` flags. **Mistakes.** Saying threads have separate heaps ([7.3](#s7-3){.ref}).
:::

::: q
### Q7.2 What happens if one thread segfaults?
[CISCO · TECH-1 · ■□□ · S]{.meta}

[30-second answer: the whole process dies, because SIGSEGV is delivered to the process and its default action terminates it, taking every thread along.]{.short}

**Answer.** All threads share one address space, so a wild pointer in one may already have corrupted the others. A handler may catch the signal, but resuming is unsafe. **Follow-ups.** `exit()` from any thread ends the process, while `pthread_exit()` ends only the caller; one process per worker (as browsers and some routing daemons do) contains a crash.
:::

::: q
### Q7.3 How many times does `hi` print? `fork(); fork(); fork(); printf("hi\n");` Then `fork() && fork() || fork()`.
[CISCO · JUNIPER · QUALCOMM · TECH-1 · ■■□ · S]{.meta}

[30-second answer: 8, because each fork doubles the number of processes; the second expression creates 5 processes.]{.short}

**Approach.** Three forks give 2³ = 8 processes, each reaching the `printf`. For the expression, the parent gets a non-zero PID from both forks, so `&&` is true and `||` skips the third fork: 1 process. The first child gets 0, so `&&` is false and it runs the third fork: 2 processes. The second child gets 0 from its fork, so it also runs the third fork: 2 processes. Total 1 + 2 + 2 = 5 (Figure 7.4). **Mistakes.** Forgetting stdout buffering: with output redirected, an unflushed `printf("hi")` before the fork is copied and printed twice.
:::

::: q
### Q7.4 What is a zombie process? What is an orphan?
[CISCO · JUNIPER · TECH-1 · ■□□ · S]{.meta}

[30-second answer: a zombie is a child that has exited but whose parent has not yet called `wait()`, so its control block and exit status remain; an orphan is a running child whose parent has exited, adopted by PID 1.]{.short}

**Answer.** A zombie uses a PID slot and no other memory, shows state `Z` in `ps`, and cannot be killed; it disappears when the parent waits or dies. Reap with `waitpid(-1, NULL, WNOHANG)` in a SIGCHLD handler, or ignore SIGCHLD with `SA_NOCLDWAIT`. **Mistakes.** Calling an orphan a zombie ([7.2](#s7-2){.ref}).
:::

::: q
### Q7.5 What happens on a context switch? Why is a thread switch cheaper?
[CISCO · QUALCOMM · TECH-1 · ■■□ · S]{.meta}

[30-second answer: the kernel saves the running task's registers in its control block, picks the next task, and restores that task's registers; switching to a thread of the same process avoids changing the page tables and so keeps the TLB and caches warm.]{.short}

**Answer.** Steps: (i) a timer interrupt, a block or a yield enters the kernel; (ii) save registers and program counter; (iii) the scheduler chooses; (iv) if the address space differs, load the new page-table base (flushing or retagging the TLB); (v) restore registers and return. The indirect cost, refilling caches and TLB, often exceeds the direct few microseconds. **Mistakes.** Claiming a thread switch flushes the TLB.
:::

::: q
### Q7.6 Compute the average waiting time under round robin with q = 2 for P1 (arrival 0, burst 5), P2 (1, 3), P3 (2, 1), P4 (3, 2).
[QUALCOMM · CISCO · OA · ■■□ · S]{.meta}

[30-second answer: the average waiting time is 4.5 time units.]{.short}

**Approach.** Take the convention that a newly arrived process joins the ready queue before a pre-empted one. Gantt chart: P1 0–2, P2 2–4, P3 4–5, P1 5–7, P4 7–9, P2 9–10, P1 10–11. Completion times: P1 11, P2 10, P3 5, P4 9. Turnaround = completion − arrival: 11, 9, 3, 6. Waiting = turnaround − burst: 6, 6, 2, 4. **Answer.** (6 + 6 + 2 + 4)/4 = 4.5; average turnaround 29/4 = 7.25. **Mistakes.** Using the opposite arrival convention without saying so, which changes the order at t = 2 and the totals.
:::

::: q
### Q7.7 What is starvation? How does ageing fix it?
[QUALCOMM · TECH-1 · ■■□ · S]{.meta}

[30-second answer: starvation is a ready task that is never chosen, for example a low-priority task behind a steady stream of high-priority ones; ageing raises a task's priority the longer it waits, so it eventually runs.]{.short}

**Answer.** Starvation differs from deadlock: the system as a whole progresses. Sources are priority scheduling, SJF with a stream of short jobs, and reader-preferring locks. Cures are ageing, fair queueing, feedback queues with a periodic boost, and writer-preferring locks ([7.4](#s7-4){.ref}).
:::

::: q
### Q7.8 What is a race condition? What is a critical section?
[CISCO · JUNIPER · QUALCOMM · MICROSOFT · TECH-1 · ■□□ · S]{.meta}

[30-second answer: a race condition is a result that depends on the timing of unsynchronised accesses to shared data, at least one of them a write; a critical section is the code that touches the shared data and must run by one thread at a time.]{.short}

**Answer.** `counter++` is load, add, store, so two threads can both load 5 and both store 6 ([7.3](#s7-3){.ref}). A correct solution gives mutual exclusion, progress (a free section is granted to a waiter) and bounded waiting (no thread is overtaken for ever). **Follow-ups.** Detecting races with ThreadSanitizer; atomics for single-word updates.
:::

::: q
### Q7.9 Mutex versus binary semaphore: when would you use each?
[JUNIPER · CISCO · QUALCOMM · TECH-1 · ■■□ · S]{.meta}

[30-second answer: a mutex has an owner and only the locker may unlock it, so it protects shared data; a binary semaphore has no owner and any thread may post it, so it signals events between threads.]{.short}

**Answer.** Ownership gives the mutex priority inheritance, recursive and error-checking variants and misuse detection. Use a mutex around a critical section. Use a semaphore when one thread, or an interrupt handler, tells another that something has happened ("buffer ready"), or a counting semaphore to bound a pool. **Mistakes.** Using a semaphore as a lock and then suffering priority inversion with no inheritance available ([7.5](#s7-5){.ref}).
:::

::: q
### Q7.10 Mutex versus spinlock. Which is used in an interrupt handler, and why?
[QUALCOMM · BROADCOM · CISCO · TECH-1 · ■■□ · S]{.meta}

[30-second answer: a mutex puts a waiter to sleep, a spinlock busy-waits; an interrupt handler has no task context to sleep in, so it must use a spinlock, with interrupts disabled while it is held.]{.short}

**Answer.** Spin when the critical section is shorter than a context switch and the holder is running on another core. On one CPU a spinlock held by a pre-empted task would spin for ever, which is why the kernel disables pre-emption while one is held. Use `spin_lock_irqsave` if an ISR can also take the lock, otherwise the ISR could interrupt the holder on the same core and spin for ever. **Mistakes.** Sleeping or calling `kmalloc(GFP_KERNEL)` under a spinlock.
:::

::: q
### Q7.11 Implement a counting semaphore using a mutex and a condition variable.
[JUNIPER · ARISTA · TECH-2 · ■■■ · S]{.meta}

[30-second answer: keep a counter under a mutex; `wait` sleeps on the condition variable while the counter is zero, then decrements; `post` increments and signals.]{.short}

**Code.**

```c
#include <pthread.h>

typedef struct {
    int n;
    pthread_mutex_t m;
    pthread_cond_t c;
} sem_t2;

void s_init(sem_t2 *s, int n)
{
    s->n = n;
    pthread_mutex_init(&s->m, 0);
    pthread_cond_init(&s->c, 0);
}

void s_wait(sem_t2 *s)
{
    pthread_mutex_lock(&s->m);
    while (s->n == 0)
        pthread_cond_wait(&s->c, &s->m);
    s->n--;
    pthread_mutex_unlock(&s->m);
}

void s_post(sem_t2 *s)
{
    pthread_mutex_lock(&s->m);
    s->n++;
    pthread_cond_signal(&s->c);
    pthread_mutex_unlock(&s->m);
}
```

**Answer.** The loop in `s_wait` rechecks the counter because the wake-up may be spurious or stolen by another waiter that decremented first. One `signal` per `post` is enough, since one unit of the resource appeared. **Follow-ups.** Use `sem_timedwait`-style timeouts with `pthread_cond_timedwait`; this is how POSIX semaphores are built on some systems.
:::

::: q
### Q7.12 Implement producer–consumer with a bounded buffer. Why does the wait use a `while` loop?
[JUNIPER · CISCO · GOOGLE · TECH-2 · ■■■ · S]{.meta}

[30-second answer: a circular buffer with a mutex, a `not_full` and a `not_empty` condition variable; each side waits in a `while` on its predicate, because a woken thread must recheck that the condition still holds.]{.short}

**Approach.** The complete program with three producers and two consumers is in [7.5](#s7-5){.ref} (`bbuf.c`), with the semaphore version beside it. Producer: lock; `while (count == N) wait(not_full)`; store; `count++`; signal `not_empty`; unlock. Consumer: the mirror. **Answer.** `while`, not `if`, since the standard allows spurious wake-ups and another thread may consume the item between the signal and the waiter's re-acquisition of the mutex. **Mistakes.** Waiting on the semaphore after taking the mutex; forgetting to wake sleeping consumers at shutdown.
:::

::: q
### Q7.13 What are the four conditions for deadlock? How do you prevent each?
[CISCO · JUNIPER · TECH-1 · ■■□ · S]{.meta}

[30-second answer: mutual exclusion, hold and wait, no pre-emption and circular wait must all hold; break any one. In practice, impose a global lock order to break circular wait.]{.short}

**Answer.** Mutual exclusion: make the resource shareable. Hold and wait: request everything at once. No pre-emption: on a failed `trylock`, release all and retry. Circular wait: order the locks and acquire in order. Example: threads locking A,B and B,A deadlock; the fixed order A,B for both ([7.6](#s7-6){.ref}) cures it. **Mistakes.** Treating mutual exclusion as removable for locks that protect writes.
:::

::: q
### Q7.14 Run the banker's algorithm: totals (6, 3, 4); Allocation P0 (1,0,1), P1 (1,1,0), P2 (1,0,1), P3 (0,1,1); Max P0 (3,2,2), P1 (2,2,1), P2 (2,1,2), P3 (1,2,2). Is the state safe?
[QUALCOMM · CISCO · OA · ■■■ · S]{.meta}

[30-second answer: yes; the safe sequence is P1, P2, P3, P0.]{.short}

**Approach.** Available = (6, 3, 4) − (3, 2, 3) = (3, 1, 1). Need = Max − Allocation: P0 (2,2,1), P1 (1,1,1), P2 (1,1,1), P3 (1,1,1). Work = (3,1,1): P1 fits, Work = (4,2,1). P2 fits, Work = (5,2,2). P3 fits, Work = (5,3,3). P0 needs (2,2,1), fits, Work = (6,3,4), the totals. **Answer.** Safe, in the order ⟨P1, P2, P3, P0⟩. **Follow-ups.** If P0 asked for (2,0,0) now: it is within its need and within Available, and after the pretend grant Available is (1,1,1), still enough to run P1 and then everything else, so grant. **Mistakes.** Comparing Max (not Need) with Work.
:::

::: q
### Q7.15 What is priority inversion? Explain priority inheritance using the Mars Pathfinder case.
[QUALCOMM · CISCO · TECH-1 · ■■□ · S]{.meta}

[30-second answer: a high-priority task waits for a lock held by a low-priority task that a medium-priority task keeps pre-empting; priority inheritance lets the lock holder run at the waiter's priority until it unlocks.]{.short}

**Answer.** On Pathfinder (1997) a low-priority task held a bus lock, a medium task ran, and the high-priority bus manager missed its deadline and triggered a reset; the engineers enabled inheritance on the lock by remote patch. Alternatives: priority ceiling (the lock has a ceiling priority that its holder inherits), or avoiding the shared lock ([7.6](#s7-6){.ref}). **Mistakes.** Describing it as deadlock: the system is delayed, not stuck.
:::

::: q
### Q7.16 Readers–writers: give a writer-preferring solution.
[ARISTA · JUNIPER · TECH-2 · ■■■ · S]{.meta}

[30-second answer: count readers and waiting writers under a mutex; a reader enters only if no writer is active or waiting; a writer enters when no one is inside; on exit a writer prefers waking another writer.]{.short}

**Code.**

```c
#include <pthread.h>

typedef struct {
    pthread_mutex_t m;
    pthread_cond_t rd, wr;
    int readers, writer, wwait;
} rw_t;

void r_lock(rw_t *l)
{
    pthread_mutex_lock(&l->m);
    while (l->writer || l->wwait)
        pthread_cond_wait(&l->rd, &l->m);
    l->readers++;
    pthread_mutex_unlock(&l->m);
}

void r_unlock(rw_t *l)
{
    pthread_mutex_lock(&l->m);
    if (--l->readers == 0)
        pthread_cond_signal(&l->wr);
    pthread_mutex_unlock(&l->m);
}

void w_lock(rw_t *l)
{
    pthread_mutex_lock(&l->m);
    l->wwait++;
    while (l->writer || l->readers)
        pthread_cond_wait(&l->wr, &l->m);
    l->wwait--;
    l->writer = 1;
    pthread_mutex_unlock(&l->m);
}

void w_unlock(rw_t *l)
{
    pthread_mutex_lock(&l->m);
    l->writer = 0;
    if (l->wwait)
        pthread_cond_signal(&l->wr);
    else
        pthread_cond_broadcast(&l->rd);
    pthread_mutex_unlock(&l->m);
}
```

**Answer.** New readers yield to any waiting writer (`wwait`), so writers cannot starve; the cost is that readers can starve under a steady stream of writers, which is the dual problem. A fair alternative queues arrivals in order. **Follow-ups.** `pthread_rwlock_t` with `PTHREAD_RWLOCK_PREFER_WRITER_NONRECURSIVE_NP` provides the same policy.
:::

::: q
### Q7.17 What is virtual memory and why is it needed?
[CISCO · JUNIPER · TECH-1 · ■□□ · S]{.meta}

[30-second answer: each process sees a private, contiguous address space that the MMU maps to physical frames; it provides isolation, simple linking and loading, and lets pages be allocated on demand or swapped out.]{.short}

**Answer.** Benefits: protection (a process cannot name another's memory), relocation (every program may assume the same layout), sharing (libraries, copy-on-write), and over-commitment through demand paging. **Mistakes.** Describing it only as "disk used as RAM" ([7.7](#s7-7){.ref}).
:::

::: q
### Q7.18 Explain paging, the page table and the TLB. What happens on a TLB miss and on a page fault?
[CISCO · QUALCOMM · ARISTA · TECH-1 · ■■□ · S]{.meta}

[30-second answer: memory is split into fixed pages; the page table maps virtual pages to frames; the TLB caches recent translations. A TLB miss causes a table walk; a page fault, when the entry is absent or forbidden, enters the kernel to load the page or kill the process.]{.short}

**Approach.** Address = page number + offset. Worked check: 0x00403ABC with 4 KB pages maps page 0x00403 to frame 0x1A2, giving 0x1A2ABC. A TLB miss costs extra memory reads (one per level) and is handled by hardware or a short kernel routine; a page fault costs microseconds (minor) to milliseconds (major, disk). **Answer.** EAT = 0.95 × 101 + 0.05 × 201 = 106 ns for the figures in [7.7](#s7-7){.ref}. **Mistakes.** Confusing the two: a TLB miss is not an error.
:::

::: q
### Q7.19 Compute the page faults for LRU with three frames on the reference string 1 2 3 4 2 1 5 6 2 1 2 3 7 6 3 2 1 2 3 6.
[QUALCOMM · OA · ■■□ · S]{.meta}

[30-second answer: 15 faults in 20 references.]{.short}

**Approach.** Track the three most recently used pages; a reference is a hit if the page is among them, and otherwise evicts the least recently used. Outcome per reference (F fault, h hit): F F F F h F F F F F h F F F h F F h h F. Count the Fs: 15. **Check.** With four frames the same string gives 10 faults, so memory helps. **Mistakes.** Not moving a page to most-recent on a hit.
:::

::: q
### Q7.20 What is Bélády's anomaly?
[QUALCOMM · TECH-1 · ■■□ · S]{.meta}

[30-second answer: for FIFO replacement, giving a process more frames can increase its page faults; LRU and Optimal are immune because they are stack algorithms.]{.short}

**Answer.** On 1 2 3 4 1 2 5 1 2 3 4 5, FIFO takes 9 faults with three frames and 10 with four. The pages in memory under LRU with n frames are always a subset of those with n + 1 frames, which excludes the anomaly ([7.7](#s7-7){.ref}).
:::

::: q
### Q7.21 What is copy-on-write and how does `fork()` use it?
[CISCO · GOOGLE · TECH-1 · ■■□ · S]{.meta}

[30-second answer: parent and child share the same physical pages, marked read-only; the first write by either raises a fault and the kernel copies just that page for the writer.]{.short}

**Answer.** This makes `fork` fast and makes `fork` plus `exec` nearly free, since the child's pages are never copied. It also explains why a forked child's memory use grows only as it writes ([7.7](#s7-7){.ref}). **Follow-ups.** Redis snapshots rely on it; a parent writing heavily during a snapshot can double memory use.
:::

::: q
### Q7.22 Stack versus heap: which is faster to allocate, and why?
[ARISTA · QUALCOMM · TECH-1 · ■□□ · S]{.meta}

[30-second answer: the stack, because allocation is one adjustment of the stack pointer and the memory is likely in cache; the heap must search for a suitable block and may fragment.]{.short}

**Answer.** Solved in full once in [Q2.14](#ps2){.ref} of Pillar 2, with lifetime and size limits. The systems angle added here is that heap allocation may take a lock and, on first touch, a page fault ([7.7](#s7-7){.ref}).
:::

::: q
### Q7.23 What is `sizeof` this struct, and how do you reduce it?
[ARISTA · QUALCOMM · CISCO · TECH-1 · ■■□ · S]{.meta}

[30-second answer: add padding so each member sits at a multiple of its alignment and the total is a multiple of the largest alignment; order members by decreasing size to shrink it.]{.short}

**Answer.** Worked in [Q2.3](#ps2){.ref} and [Q2.2](#ps2){.ref} of Pillar 2 (for example `{char; int; char}` is 12 bytes and 8 when reordered). For wire formats, pack the structure (`__attribute__((packed))`) and accept the unaligned-access cost, or better, parse by offset.
:::

:::
:::

:::
