::: {.p7}

## [7.5]{.sec}Synchronisation [Must · ■■□]{.tag} {#s7-5}

A *critical section* is a stretch of code that touches shared data and must not be executed by two threads at once. Enforcing this is *mutual exclusion*, and the tools differ in who may release them, whether a waiter sleeps, and where they may be used. We meet five: the mutex, the semaphore, the spinlock, the condition variable and the read-write lock.

A *mutex* (mutual-exclusion lock) has two states and an owner. `pthread_mutex_lock` takes it, sleeping if another thread holds it; `pthread_mutex_unlock` releases it, and only the owner may do so. Figure 7.7 shows the second thread being put to sleep and woken. The race in [7.3](#s7-3){.ref} disappears when the increment is placed between the two calls, at the price of slower code. On the four-core test machine, two threads making two million increments in total took about 120 ms under a contended mutex and about 20 ms with `__atomic_fetch_add`, an *atomic* instruction that performs the single-word update without ever sleeping; the unprotected loop was faster still, and wrong. Only the ordering of these figures should be trusted, not their values.

<figure>
<svg viewBox="0 0 480 150" width="480"><defs><marker id="imx" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="amx" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><text class="lbl" x="8" y="38" text-anchor="start">Thread A</text><text class="lbl" x="8" y="98" text-anchor="start">Thread B</text><rect class="fill" x="60" y="24" width="72" height="26" rx="0"/><text class="sm" x="96.0" y="40.0" text-anchor="middle">work</text><rect class="box" x="132" y="24" width="144" height="26" rx="0" style="fill:#FFF4C2"/><text class="sm" x="204.0" y="40.0" text-anchor="middle">holds the mutex</text><rect class="fill" x="276" y="24" width="108" height="26" rx="0"/><text class="sm" x="330.0" y="40.0" text-anchor="middle">work</text><rect class="fill" x="60" y="84" width="108" height="26" rx="0"/><text class="sm" x="114.0" y="100.0" text-anchor="middle">work</text><rect class="box dash" x="168" y="84" width="108" height="26" rx="0" style="fill:#fafafa"/><text class="sm" x="222.0" y="100.0" text-anchor="middle">blocked: asleep</text><rect class="box" x="276" y="84" width="108" height="26" rx="0" style="fill:#FFF4C2"/><text class="sm" x="330.0" y="100.0" text-anchor="middle">holds the mutex</text><text class="mono" x="132" y="18" text-anchor="middle">lock</text><text class="mono" x="276" y="18" text-anchor="middle">unlock</text><text class="mono" x="168" y="78" text-anchor="middle">lock (fails)</text><line class="acc" x1="276" y1="52" x2="276" y2="80" marker-end="url(#amx)" /><text class="sm" x="280" y="70" text-anchor="start">wake</text><text class="sm" x="280" y="78" text-anchor="middle"></text><line class="ln" x1="60" y1="124" x2="384" y2="124" marker-end="url(#imx)" /><text class="sm" x="384" y="138" text-anchor="end">time</text><text class="sm" x="60" y="138" text-anchor="start">Only the holder may unlock; the mutex records its owner.</text></svg>
<figcaption><b>Figure 7.7</b> A mutex timeline. Thread B fails to lock, sleeps, and is woken when A unlocks.</figcaption>
</figure>

[**Semaphore** — a counter with two operations. A car park with a "spaces free: 5" board: `wait` takes a space, `post` returns one.]{.margin}A *semaphore* is a non-negative counter with two atomic operations: `wait` (also P or down) decrements it, sleeping while it is zero, and `post` (V or up) increments it and wakes a sleeper. It has no owner, so any thread may post. A *counting* semaphore initialised to N admits N threads at once, as a pool of N identical resources; a *binary* semaphore (N = 1) behaves like a lock but may be released by a different thread than the one that took it, which makes it a signalling device between threads.

A *spinlock* does not sleep: a waiter loops on an atomic test until the lock is free. This is wasteful on a single core and fine for very short critical sections on several. It is the only lock usable where sleeping is forbidden, such as an interrupt handler ([7.8](#s7-8){.ref}), because a sleeping task cannot be scheduled from interrupt context. A naive test-and-set loop writes to the lock's cache line on every attempt, so the line bounces between cores; the *test-and-test-and-set* refinement spins on an ordinary read, which hits the local cache, and attempts the atomic write only when the lock looks free.

```c
#include <pthread.h>
#include <stdio.h>

#if defined(__x86_64__)
#define cpu_relax() __builtin_ia32_pause()   /* be kind to the sibling hyper-thread */
#else
#define cpu_relax() ((void)0)
#endif

typedef struct { volatile char flag; } spinlock_t;

static void spin_lock(spinlock_t *l)
{
    for (;;) {
        /* test-and-set: atomically write 1 and return the old value */
        if (!__atomic_test_and_set(&l->flag, __ATOMIC_ACQUIRE))
            return;
        /* test-and-test-and-set: spin on a plain read, which stays in
           the local cache, and retry the atomic only when it looks free */
        while (__atomic_load_n(&l->flag, __ATOMIC_RELAXED))
            cpu_relax();
    }
}

static void spin_unlock(spinlock_t *l)
{
    __atomic_clear(&l->flag, __ATOMIC_RELEASE);
}

static spinlock_t lock;
static long counter;

static void *work(void *arg)
{
    (void)arg;
    for (int i = 0; i < 1000000; i++) {
        spin_lock(&lock);
        counter++;
        spin_unlock(&lock);
    }
    return NULL;
}

int main(void)
{
    pthread_t t[4];
    for (int i = 0; i < 4; i++) pthread_create(&t[i], NULL, work, NULL);
    for (int i = 0; i < 4; i++) pthread_join(t[i], NULL);
    printf("counter = %ld (expected 4000000)\n", counter);
    return 0;
}
```

The program prints `counter = 4000000 (expected 4000000)`. Note the acquire and release memory orders: acquire on lock and release on unlock ensure that the data protected by the lock is seen consistently by the next holder.

A *condition variable* lets a thread sleep until a predicate on shared data becomes true. It is always used with a mutex: `pthread_cond_wait(&c, &m)` atomically releases the mutex and sleeps, and re-acquires the mutex before returning. The waiter must recheck the predicate in a `while` loop, not an `if`, for two reasons: a wake-up may be *spurious* (the standard permits it), and a wake-up may be *stolen* (another thread takes the item between the signal and the waiter's re-acquisition of the mutex).

::: bigidea
A condition variable does not remember signals; the predicate on the shared data is the truth, and the loop around `cond_wait` is how a thread rechecks it.
:::

### Worked example: the bounded buffer

The *producer–consumer* problem asks for a fixed-size queue shared by threads that add items and threads that remove them: producers must wait when the queue is full, consumers when it is empty. The solution below uses one mutex and two condition variables. Three producers make 10,000 items between them, two consumers take them, and the program compares the sum put in with the sum taken out.

```c
#include <pthread.h>
#include <stdio.h>

#define SLOTS 8
#define ITEMS 10000
#define PRODUCERS 3
#define CONSUMERS 2

static int buf[SLOTS];
static int head, tail, count;
static int produced, consumed;          /* items handed out / taken so far */
static long sum_in, sum_out;
static pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t not_full = PTHREAD_COND_INITIALIZER;
static pthread_cond_t not_empty = PTHREAD_COND_INITIALIZER;

static void *producer(void *arg)
{
    (void)arg;
    for (;;) {
        pthread_mutex_lock(&m);
        if (produced == ITEMS) {        /* nothing left to make */
            pthread_mutex_unlock(&m);
            return NULL;
        }
        int item = ++produced;          /* claim item number under the lock */
        while (count == SLOTS)          /* while, not if */
            pthread_cond_wait(&not_full, &m);
        buf[tail] = item;
        tail = (tail + 1) % SLOTS;
        count++;
        sum_in += item;
        pthread_cond_signal(&not_empty);
        pthread_mutex_unlock(&m);
    }
}

static void *consumer(void *arg)
{
    (void)arg;
    for (;;) {
        pthread_mutex_lock(&m);
        while (count == 0 && consumed < ITEMS)
            pthread_cond_wait(&not_empty, &m);
        if (count == 0) {               /* all items consumed: finish */
            pthread_mutex_unlock(&m);
            return NULL;
        }
        int item = buf[head];
        head = (head + 1) % SLOTS;
        count--;
        consumed++;
        sum_out += item;
        pthread_cond_signal(&not_full);
        if (consumed == ITEMS)
            pthread_cond_broadcast(&not_empty);   /* release idle consumers */
        pthread_mutex_unlock(&m);
    }
}

int main(void)
{
    pthread_t p[PRODUCERS], c[CONSUMERS];
    for (int i = 0; i < PRODUCERS; i++) pthread_create(&p[i], NULL, producer, NULL);
    for (int i = 0; i < CONSUMERS; i++) pthread_create(&c[i], NULL, consumer, NULL);
    for (int i = 0; i < PRODUCERS; i++) pthread_join(p[i], NULL);
    for (int i = 0; i < CONSUMERS; i++) pthread_join(c[i], NULL);
    printf("sum in = %ld, sum out = %ld, %s\n", sum_in, sum_out,
           sum_in == sum_out ? "match" : "MISMATCH");
    return 0;
}
```

```
$ gcc -Wall -Wextra -O2 -pthread bbuf.c -o bbuf && ./bbuf
sum in = 50005000, sum out = 50005000, match
```

Four details deserve attention. First, `count` is read and written only with the mutex held, so it is consistent. Second, a producer waits on `not_full` and a consumer on `not_empty`, so each signal wakes only a thread that can make progress. Third, the consumers must be released at the end; the `broadcast` when the last item is taken does this, and without it a consumer sleeping on an empty buffer would never return. Fourth, the same problem with semaphores uses `empty` (initially the number of slots) and `full` (initially 0), plus a mutex around the buffer indices:

```c
#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>

#define SLOTS 4
#define ITEMS 1000

static int buf[SLOTS], in, out;
static sem_t empty, full;                  /* free slots, filled slots */
static pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;
static long sum;

static void *producer(void *arg)
{
    (void)arg;
    for (int i = 1; i <= ITEMS; i++) {
        sem_wait(&empty);                  /* first: reserve a slot ... */
        pthread_mutex_lock(&m);            /* ... then take the lock. Swap them and a  */
        buf[in] = i; in = (in + 1) % SLOTS;/* full buffer deadlocks: producer holds m   */
        pthread_mutex_unlock(&m);          /* while sleeping, so the consumer cannot    */
        sem_post(&full);                   /* take m to make room.                      */
    }
    return NULL;
}

static void *consumer(void *arg)
{
    (void)arg;
    for (int i = 1; i <= ITEMS; i++) {
        sem_wait(&full);
        pthread_mutex_lock(&m);
        sum += buf[out]; out = (out + 1) % SLOTS;
        pthread_mutex_unlock(&m);
        sem_post(&empty);
    }
    return NULL;
}

int main(void)
{
    pthread_t p, c;
    sem_init(&empty, 0, SLOTS);
    sem_init(&full, 0, 0);
    pthread_create(&p, NULL, producer, NULL);
    pthread_create(&c, NULL, consumer, NULL);
    pthread_join(p, NULL); pthread_join(c, NULL);
    printf("sum = %ld (expected %d)\n", sum, ITEMS * (ITEMS + 1) / 2);
    return 0;
}
```

The order of the two waits in the producer matters. If the producer took the mutex first and then waited on `empty`, a full buffer would leave it asleep holding the mutex; the consumer could then never take the mutex to remove an item and make room, and both would wait for ever. This is a deadlock ([7.6](#s7-6){.ref}).

### Choosing a primitive

| | Mutex | Binary semaphore | Counting semaphore | Spinlock | Condition variable |
|---|---|---|---|---|---|
| Owner | yes, the locker | no | no | yes, by convention | not a lock |
| Waiter sleeps? | yes | yes | yes | no, spins | yes |
| Usable in an interrupt handler? | no | `post` only | `post` only | yes | no |
| Typical use | protect shared data | signal an event | limit a pool of N | very short sections, kernel | wait for a predicate |
| Linux kernel API | `mutex_lock` | `down` / `up` | `down` / `up` | `spin_lock_irqsave` | `wait_event` |

A mutex and a binary semaphore are not interchangeable. Because a mutex has an owner, the system can lend the owner a higher priority when a more urgent thread waits (priority inheritance, [7.6](#s7-6){.ref}), can detect an unlock by the wrong thread, and can offer recursive and error-checking variants. A semaphore, lacking an owner, can be posted from an interrupt handler or from another thread, which is exactly what signalling needs.

### Read-write locks

When many threads read and few write, `pthread_rwlock` lets any number of readers hold the lock together but gives a writer exclusive access. A reader-preferring implementation can *starve* a writer that waits behind a steady stream of readers; a writer-preferring one blocks new readers once a writer is waiting, trading reader latency for freedom from starvation.

::: lens
[JUNIPER · CISCO · QUALCOMM · ARISTA]{.co}

"Implement a mutex or semaphore", "mutex versus semaphore" and "write a multithreaded program with a lock" are reported Juniper and Cisco questions, and Qualcomm asks which lock is safe inside an interrupt handler. A strong answer gives the table above in words, states the ownership difference, writes the bounded buffer with a `while` around the wait, and explains why a spinlock is correct in an interrupt handler (nothing may sleep there) but wasteful in user code. Follow-ups: how to build a semaphore from a mutex and a condition variable (Q7.11), and what happens if `unlock` is called by a thread that does not own a mutex (undefined for a default mutex, an error for an error-checking one).
:::

::: trap
*Claim:* "`volatile int flag` protects a critical section." *Why it is wrong:* `volatile` stops the compiler from caching the variable but does not make a read-modify-write atomic and does not order other memory accesses. *Correct statement:* use a lock or an atomic operation with the right memory order; `volatile` is for device registers ([7.13](#s7-13){.ref}).
:::

::: check
1. A consumer wakes from `cond_wait` and finds the queue empty. Why can this happen? [^c75-1]
2. Which of mutex and spinlock may be used in an interrupt handler? [^c75-2]
3. Can a thread unlock a mutex that another thread locked? [^c75-3]
:::

[^c75-1]: The wake-up was spurious, or another consumer took the item first; hence the `while` loop that rechecks the predicate.
[^c75-2]: The spinlock. A mutex may sleep, which is not allowed in interrupt context.
[^c75-3]: Not legitimately; a mutex has an owner. A semaphore has none, so any thread may post it.

## [7.6]{.sec}Deadlock, starvation and priority inversion [Must · ■■□]{.tag} {#s7-6}

A set of tasks is *deadlocked* when each waits for a resource that another task in the set holds, so none can proceed. Four conditions, the *Coffman conditions*, must hold together: (i) *mutual exclusion*, a resource is held by at most one task; (ii) *hold and wait*, a task holds one resource while requesting another; (iii) *no pre-emption*, a resource cannot be taken away; (iv) *circular wait*, a cycle of tasks each waits for the next. Hence preventing deadlock means breaking any one of them.

| Condition | Prevention | Cost |
|---|---|---|
| Mutual exclusion | make the resource shareable (read-only data, lock-free structures) | not possible for a printer or a write |
| Hold and wait | request all resources at once, or release before requesting | low utilisation, possible starvation |
| No pre-emption | if a request fails, release everything held and retry (`pthread_mutex_trylock`) | restart cost; livelock if both retry in step |
| Circular wait | impose a global order on locks and always acquire in that order | the standard practical answer |

A *resource-allocation graph* draws tasks as circles and resources as squares, with a request edge from a task to a resource and an assignment edge from a resource to a task. A cycle is the circular-wait condition made visible.

<figure>
<svg viewBox="0 0 480 200" width="480"><defs><marker id="irg" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="arg" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><text class="lbl" x="120" y="14" text-anchor="middle">single instances: deadlock</text><text class="lbl" x="360" y="14" text-anchor="middle">two instances of R1: no deadlock</text><circle class="box" cx="40" cy="60" r="16"/><text class="lbl" x="40" y="63" text-anchor="middle">P1</text><rect class="box" x="182" y="42" width="36" height="36" rx="0"/><text class="sm" x="200" y="37" text-anchor="middle">R2</text><circle class="accf" cx="200" cy="60" r="3.2"/><circle class="box" cx="200" cy="160" r="16"/><text class="lbl" x="200" y="163" text-anchor="middle">P2</text><rect class="box" x="22" y="142" width="36" height="36" rx="0"/><text class="sm" x="40" y="137" text-anchor="middle">R1</text><circle class="accf" cx="40" cy="160" r="3.2"/><line class="acc" x1="56" y1="60" x2="180" y2="60" marker-end="url(#arg)" /><text class="sm" x="118" y="54" text-anchor="middle">requests</text><line class="acc" x1="200" y1="80" x2="200" y2="142" marker-end="url(#arg)" /><text class="sm" x="206" y="114" text-anchor="start">held by</text><line class="acc" x1="184" y1="160" x2="60" y2="160" marker-end="url(#arg)" /><text class="sm" x="122" y="174" text-anchor="middle">requests</text><line class="acc" x1="40" y1="140" x2="40" y2="78" marker-end="url(#arg)" /><text class="sm" x="34" y="114" text-anchor="end">held by</text><circle class="box" cx="270" cy="60" r="16"/><text class="lbl" x="270" y="63" text-anchor="middle">P1</text><rect class="box" x="412" y="42" width="36" height="36" rx="0"/><text class="sm" x="430" y="37" text-anchor="middle">R1</text><circle class="accf" cx="423" cy="60" r="3.2"/><circle class="accf" cx="437" cy="60" r="3.2"/><circle class="box" cx="430" cy="160" r="16"/><text class="lbl" x="430" y="163" text-anchor="middle">P2</text><rect class="box" x="252" y="142" width="36" height="36" rx="0"/><text class="sm" x="270" y="137" text-anchor="middle">R2</text><circle class="accf" cx="270" cy="160" r="3.2"/><circle class="box" cx="350" cy="110" r="16"/><text class="lbl" x="350" y="113" text-anchor="middle">P3</text><line class="acc" x1="286" y1="60" x2="410" y2="60" marker-end="url(#arg)" /><line class="acc" x1="430" y1="80" x2="430" y2="142" marker-end="url(#arg)" /><line class="acc" x1="414" y1="160" x2="290" y2="160" marker-end="url(#arg)" /><line class="acc" x1="270" y1="140" x2="270" y2="78" marker-end="url(#arg)" /><line class="ln" x1="416" y1="76" x2="364" y2="99" marker-end="url(#irg)" /><text class="sm" x="350" y="134" text-anchor="middle">P3 is not waiting;</text><text class="sm" x="350" y="144" text-anchor="middle">it will release R1</text><text class="sm" x="240" y="194" text-anchor="middle">Arrow from a process: request. Arrow from a resource: assignment. Dots are instances.</text></svg>
<figcaption><b>Figure 7.8</b> Resource-allocation graphs. Left: a cycle with single-instance resources is a deadlock. Right: a cycle with a multi-instance resource is not, since P3 can finish and release R1.</figcaption>
</figure>

::: trap
*Claim:* "A cycle in the resource graph always means deadlock." *Why it is wrong:* with several instances of a resource, a task outside the cycle may release one and let the cycle dissolve. *Correct statement:* a cycle is necessary for deadlock; it is sufficient only when every resource has a single instance.
:::

### Worked example: lock ordering

Thread 1 locks A then B; thread 2 locks B then A. If each takes its first lock before either takes its second, both wait for ever. The program below does this deliberately, with a short sleep to make the bad interleaving certain.

```c
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

static pthread_mutex_t A = PTHREAD_MUTEX_INITIALIZER, B = PTHREAD_MUTEX_INITIALIZER;

static void *t1(void *x) { (void)x;
    pthread_mutex_lock(&A); usleep(100000); pthread_mutex_lock(&B);   /* A then B */
    puts("t1 done"); pthread_mutex_unlock(&B); pthread_mutex_unlock(&A); return NULL; }

static void *t2(void *x) { (void)x;
#ifdef FIXED
    pthread_mutex_lock(&A); usleep(100000); pthread_mutex_lock(&B);   /* same order */
#else
    pthread_mutex_lock(&B); usleep(100000); pthread_mutex_lock(&A);   /* B then A: cycle */
#endif
    puts("t2 done"); pthread_mutex_unlock(&A); pthread_mutex_unlock(&B); return NULL; }

int main(void)
{
    pthread_t a, b;
    pthread_create(&a, NULL, t1, NULL); pthread_create(&b, NULL, t2, NULL);
    pthread_join(a, NULL); pthread_join(b, NULL);
    return 0;
}
```

```
$ gcc -g -pthread dl.c -o dl && ./dl &
$ gdb -p $! -batch -ex "thread apply all bt 2"
Thread 3 ...  #1  __lll_lock_wait (futex=... <B>, private=0)
Thread 2 ...  #1  __lll_lock_wait (futex=... <A>, private=0)
Thread 1 ...  #0  __futex_abstimed_wait_common64 ... pthread_join
```

**What you should notice:** two threads are stuck inside `__lll_lock_wait`, one on lock `B` and one on lock `A`, while the main thread waits in `pthread_join`. Compiled with `-DFIXED`, the second thread takes A first, as the first does, and the program prints both "done" lines: a global lock order removes the cycle.

### Worked example: the banker's algorithm

*Deadlock avoidance* lets a system grant a request only if the resulting state is *safe*, meaning some order exists in which every task can obtain its maximum claim and finish. The banker's algorithm tests this. Take five tasks and three resource types with totals A = 10, B = 5, C = 7. Each task has declared a maximum claim; the *need* is the maximum minus what it holds now.

| Task | Allocation (A B C) | Max (A B C) | Need = Max − Alloc |
|---|---|---|---|
| P0 | 0 1 0 | 7 5 3 | 7 4 3 |
| P1 | 2 0 0 | 3 2 2 | 1 2 2 |
| P2 | 3 0 2 | 9 0 2 | 6 0 0 |
| P3 | 2 1 1 | 2 2 2 | 0 1 1 |
| P4 | 0 0 2 | 4 3 3 | 4 3 1 |

::: example
**Is the state safe?** Available = totals − the column sums of Allocation = (10, 5, 7) − (7, 2, 5) = (3, 3, 2).

1. Work = (3, 3, 2). P1's need (1, 2, 2) fits. Run it to completion and take back its allocation: Work = (3, 3, 2) + (2, 0, 0) = (5, 3, 2).
2. P3 needs (0, 1, 1), which fits. Work = (5, 3, 2) + (2, 1, 1) = (7, 4, 3).
3. P4 needs (4, 3, 1), which fits. Work = (7, 4, 3) + (0, 0, 2) = (7, 4, 5).
4. P0 needs (7, 4, 3), which fits. Work = (7, 4, 5) + (0, 1, 0) = (7, 5, 5).
5. P2 needs (6, 0, 0), which fits. Work = (7, 5, 5) + (3, 0, 2) = (10, 5, 7), the totals.

[Result: the sequence ⟨P1, P3, P4, P0, P2⟩ finishes everyone, so the state is safe.]{.result}
:::

*Request test.* Suppose P1 now requests (1, 0, 2). It is within its need (1, 2, 2) and within Available (3, 3, 2). Pretend to grant it: Available becomes (2, 3, 0), P1 holds (3, 0, 2) and needs (0, 2, 0). P1's need fits in (2, 3, 0), so it can finish and return its holdings, giving (5, 3, 2), after which the sequence above completes. The new state is safe, so the request is granted. By contrast, a request by P4 for (3, 3, 0) leaves Available at (0, 0, 2) with every need larger than that in some column; no task can proceed, the state is unsafe, and the request must wait even though resources are free at this moment.

*Detection and recovery* are the alternative when avoidance is too costly: build the wait-for graph, look for a cycle, and break it by terminating or rolling back a task. General-purpose systems mostly ignore deadlock and leave lock discipline to programmers; databases detect and abort a victim transaction.

### Starvation and priority inversion

*Starvation* is indefinite postponement of a task that is ready but never chosen: a long job under SJF, a low-priority task under a busy high-priority load, a writer behind endless readers. Unlike deadlock, the system as a whole keeps moving; ageing, fair queues and writer-preferring locks are the cures.

*Priority inversion* occurs when a high-priority task H waits for a lock held by a low-priority task L, and a medium-priority task M, needing neither, pre-empts L. H is then delayed by M although H has the higher priority. In 1997 this reset the Mars Pathfinder lander's computer repeatedly: a low-priority meteorological task held a shared bus lock, a medium task ran, and the high-priority bus-management task missed its deadline, triggering the watchdog. The remedy is *priority inheritance*: while L holds a lock that H wants, L runs at H's priority, so M cannot pre-empt it; the Pathfinder team enabled this option on the lock remotely.

<figure>
<svg viewBox="0 0 480 190" width="480"><defs><marker id="iiv" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="aiv" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><text class="lbl" x="139" y="12" text-anchor="middle">without inheritance</text><text class="lbl" x="32" y="39" text-anchor="end">H</text><line class="lg" x1="34" y1="50" x2="243" y2="50" /><text class="lbl" x="32" y="73" text-anchor="end">M</text><line class="lg" x1="34" y1="84" x2="243" y2="84" /><text class="lbl" x="32" y="107" text-anchor="end">L</text><line class="lg" x1="34" y1="118" x2="243" y2="118" /><rect class="box" x="34" y="96" width="38" height="20" rx="0" style="fill:#FFF4C2"/><text class="lbl" x="53.0" y="109.0" text-anchor="middle"></text><rect class="box dash" x="72" y="28" width="133" height="20" rx="0" style="fill:#fafafa"/><text class="lbl" x="138.5" y="41.0" text-anchor="middle"></text><rect class="box" x="91" y="62" width="76" height="20" rx="0" style="fill:#F1F2F3"/><text class="lbl" x="129.0" y="75.0" text-anchor="middle"></text><rect class="box" x="167" y="96" width="38" height="20" rx="0" style="fill:#FFF4C2"/><text class="lbl" x="186.0" y="109.0" text-anchor="middle"></text><rect class="box" x="205" y="28" width="38" height="20" rx="0" style="fill:#F1F2F3"/><text class="lbl" x="224.0" y="41.0" text-anchor="middle"></text><text class="sm" x="34" y="134" text-anchor="middle">0</text><line class="ln" x1="34" y1="126" x2="34" y2="129" /><text class="sm" x="72" y="134" text-anchor="middle">2</text><line class="ln" x1="72" y1="126" x2="72" y2="129" /><text class="sm" x="110" y="134" text-anchor="middle">4</text><line class="ln" x1="110" y1="126" x2="110" y2="129" /><text class="sm" x="148" y="134" text-anchor="middle">6</text><line class="ln" x1="148" y1="126" x2="148" y2="129" /><text class="sm" x="186" y="134" text-anchor="middle">8</text><line class="ln" x1="186" y1="126" x2="186" y2="129" /><text class="sm" x="224" y="134" text-anchor="middle">10</text><line class="ln" x1="224" y1="126" x2="224" y2="129" /><text class="sm" x="72" y="20" text-anchor="middle">H arrives</text><text class="sm" x="98.6" y="54" text-anchor="middle">M arrives</text><text class="sm" x="178.4" y="106" text-anchor="middle">unlock</text><text class="sm" x="148" y="150" text-anchor="middle">H waits 7 units; M ran first</text><text class="lbl" x="379" y="12" text-anchor="middle">with inheritance</text><text class="lbl" x="272" y="39" text-anchor="end">H</text><line class="lg" x1="274" y1="50" x2="483" y2="50" /><text class="lbl" x="272" y="73" text-anchor="end">M</text><line class="lg" x1="274" y1="84" x2="483" y2="84" /><text class="lbl" x="272" y="107" text-anchor="end">L</text><line class="lg" x1="274" y1="118" x2="483" y2="118" /><rect class="box" x="274" y="96" width="76" height="20" rx="0" style="fill:#FFF4C2"/><text class="lbl" x="312.0" y="109.0" text-anchor="middle"></text><rect class="box dash" x="312" y="28" width="38" height="20" rx="0" style="fill:#fafafa"/><text class="lbl" x="331.0" y="41.0" text-anchor="middle"></text><rect class="box" x="350" y="28" width="38" height="20" rx="0" style="fill:#F1F2F3"/><text class="lbl" x="369.0" y="41.0" text-anchor="middle"></text><rect class="box" x="388" y="62" width="57" height="20" rx="0" style="fill:#F1F2F3"/><text class="lbl" x="416.5" y="75.0" text-anchor="middle"></text><text class="sm" x="274" y="134" text-anchor="middle">0</text><line class="ln" x1="274" y1="126" x2="274" y2="129" /><text class="sm" x="312" y="134" text-anchor="middle">2</text><line class="ln" x1="312" y1="126" x2="312" y2="129" /><text class="sm" x="350" y="134" text-anchor="middle">4</text><line class="ln" x1="350" y1="126" x2="350" y2="129" /><text class="sm" x="388" y="134" text-anchor="middle">6</text><line class="ln" x1="388" y1="126" x2="388" y2="129" /><text class="sm" x="426" y="134" text-anchor="middle">8</text><line class="ln" x1="426" y1="126" x2="426" y2="129" /><text class="sm" x="464" y="134" text-anchor="middle">10</text><line class="ln" x1="464" y1="126" x2="464" y2="129" /><text class="sm" x="312" y="20" text-anchor="middle">H arrives</text><text class="sm" x="350" y="106" text-anchor="middle">unlock</text><text class="sm" x="388" y="150" text-anchor="middle">H waits 2 units; L ran at H priority</text><text class="sm" x="240" y="178" text-anchor="middle">Shaded yellow: L holds the lock. Dashed: waiting. H, M, L = high, medium, low priority.</text></svg>
<figcaption><b>Figure 7.9</b> Priority inversion. Without inheritance, H waits for M's whole run. With inheritance, L finishes its critical section at H's priority and H resumes after two units.</figcaption>
</figure>

::: lens
[QUALCOMM · CISCO · JUNIPER]{.co}

"Name the four conditions for deadlock" and "run the banker's algorithm on this matrix" are reported in written tests and technical rounds; "explain priority inversion" is common for firmware and RTOS roles. A strong answer lists the conditions, gives a lock-ordering example, and for the banker's algorithm shows the Work vector at every step. Follow-ups: deadlock versus livelock (tasks keep changing state but make no progress) and why Linux's `PTHREAD_PRIO_INHERIT` mutexes exist.
:::

::: check
1. Which Coffman condition does a global lock order break? [^c76-1]
2. Why is a safe state not the same as "no deadlock now"? [^c76-2]
:::

[^c76-1]: Circular wait: with a fixed order, no cycle of waiting tasks can form.
[^c76-2]: Safety is a guarantee about the future, that some order lets everyone finish; an unsafe state may not be deadlocked yet but may become so.

:::
