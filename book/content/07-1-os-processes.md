::: {.chapter .p7}
::: opener
[Part I · Pillar 7]{.part-label}

[7]{.num}

# Operating Systems and Socket Programming {#ch7}

[Beneath every packet is a machine that schedules, locks, maps and interrupts; we learn to follow the packet through it.]{.promise}

1. [7.1 What an operating system does]{} [MUST]{}
2. [7.2 Processes, fork and exec]{} [MUST]{}
3. [7.3 Threads and context switching]{} [MUST]{}
4. [7.4 CPU scheduling]{} [SHOULD]{}
5. [7.5 Synchronisation]{} [MUST]{}
6. [7.6 Deadlock, starvation, priority inversion]{} [MUST]{}
7. [7.7 Memory management and virtual memory]{} [MUST]{}
8. [7.8 Interrupts, system calls and DMA]{} [MUST]{}
9. [7.9 Inter-process communication and signals]{} [SHOULD]{}
10. [7.10 Sockets from first principles]{} [MUST]{}
11. [7.11 Server concurrency: threads, select, poll, epoll]{} [MUST]{}
12. [7.12 The Linux receive path: NIC to recv()]{} [MUST]{}
13. [7.13 Firmware and embedded essentials]{} [SHOULD]{}
14. [7.14 Debugging a slow server]{} [OPTIONAL]{}
15. [7.15 Mini-project: TinyRelay]{} [OPTIONAL]{}
:::

<style>.p7 pre{font-size:7pt;line-height:1.38}</style>

## [7.0]{.sec}Why this pillar matters, and how to read it {#s7-0}

Networking products are programs running on an operating system, and the questions asked about them are operating-system questions: how a process differs from a thread, why two threads corrupt a counter, what a lock is, what happens when memory runs out, and how a packet gets from the wire to `recv()`. Cisco, Juniper and Arista ask these for software roles; Qualcomm and Broadcom ask them again for firmware, with interrupts, DMA and `volatile` added.

The chapter has three movements. Sections 7.1–7.9 are the classical core: processes, threads, synchronisation, deadlock, memory, interrupts. Sections 7.10–7.11 teach the Berkeley sockets API and the server architectures built on it; this is the canonical home of the API in the book. Sections 7.12–7.14 follow a packet through the Linux kernel, and 7.15 is a mini-project that joins the chapter. Two boundaries keep the book free of repetition. C memory, pointers and byte order belong to [Pillar 2](#ch2){.ref}, and we use them here without re-teaching them. The behaviour of the TCP protocol itself, its state machine and congestion control, belongs to [Pillar 3](#ch3){.ref}; here we meet TCP only as the thing a socket call triggers.

Every program in this chapter was compiled with `gcc -Wall -Wextra` on 64-bit Linux and run, and every printed output is from that run. Compile threaded programs with `-pthread`. Exact timings and counts vary between machines; where a number varies, the text gives its range and not a promise.

::: bigidea
An operating system multiplexes one CPU, one memory and a set of devices among many programs, and it can do so safely only because the hardware gives it a privileged mode that programs do not have.
:::

## [7.1]{.sec}What an operating system does [Must · ■□□]{.tag} {#s7-1}

An *operating system* is a resource manager and a protection boundary. As a manager it divides the CPU among runnable tasks (scheduling), gives each program its own view of memory (virtual memory), and shares disks and network cards through uniform abstractions (files, sockets). As a boundary it prevents a faulty or hostile program from reading another program's memory or taking over a device. The mechanism is a *mode bit* in the processor: in *user mode* the CPU refuses privileged instructions and accesses to kernel memory; in *kernel mode* it allows them. The *kernel* is the part of the operating system that runs in kernel mode.

[**Mode bit** — one bit of CPU state. Think of a hostel warden's master key: residents (user mode) cannot copy it.]{.margin}A program asks the kernel for service through a *system call*. The C library wrapper (`read()`, `send()`, `fork()`) loads the call number and arguments into registers and executes a special instruction (`syscall` on x86-64). The processor switches to kernel mode, jumps to a fixed entry point, switches to a kernel stack, and the kernel indexes a table of handlers by the call number. The result returns in a register, and a return instruction (`sysret`) restores user mode. Figure 7.1 shows the layers and the boundary.

<figure>
<svg viewBox="0 0 480 215" width="480"><defs><marker id="ily" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="aly" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><rect class="box" x="40" y="8" width="400" height="30" rx="0"/><text class="lbl" x="240.0" y="26.0" text-anchor="middle">Applications: browser, routing daemon, your server</text><rect class="fill" x="40" y="44" width="400" height="26" rx="0"/><text class="lbl" x="240.0" y="60.0" text-anchor="middle">libc: wrappers such as read(), send(), fork()</text><line class="acc" x1="20" y1="84" x2="460" y2="84" stroke-dasharray="6 3" stroke-width="2.2"/><text class="sm" x="24" y="79" text-anchor="start">user mode</text><text class="sm" x="24" y="96" text-anchor="start">kernel mode</text><text class="sm" x="456" y="79" text-anchor="end">system-call interface</text><rect class="box" x="40" y="104" width="76" height="28" rx="0"/><text class="lbl" x="78.0" y="121.0" text-anchor="middle">scheduler</text><rect class="box" x="121" y="104" width="76" height="28" rx="0"/><text class="lbl" x="159.0" y="121.0" text-anchor="middle">memory</text><rect class="box" x="202" y="104" width="76" height="28" rx="0"/><text class="lbl" x="240.0" y="121.0" text-anchor="middle">file systems</text><rect class="box" x="283" y="104" width="76" height="28" rx="0"/><text class="lbl" x="321.0" y="121.0" text-anchor="middle">network stack</text><rect class="box" x="364" y="104" width="76" height="28" rx="0"/><text class="lbl" x="402.0" y="121.0" text-anchor="middle">drivers</text><rect class="fill" x="40" y="140" width="400" height="24" rx="0"/><text class="lbl" x="240.0" y="155.0" text-anchor="middle">Hardware: CPU and MMU, RAM, NIC, disk, timer, interrupt controller</text><line class="ln" x1="240" y1="70" x2="240" y2="100" marker-end="url(#ily)" /><text class="mono" x="250" y="92" text-anchor="start">syscall</text><text class="sm" x="240" y="186" text-anchor="middle">A call crosses the dashed line twice: into the kernel by the syscall instruction, and back by sysret</text><text class="sm" x="240" y="198" text-anchor="middle">with the result in a register. Interrupts cross it from below, without a request from the program.</text></svg>
<figcaption><b>Figure 7.1</b> The user/kernel boundary. System calls cross it on request; interrupts cross it from below without a request.</figcaption>
</figure>

::: lab
`LAB 7.1 · 10 MIN` Count the system calls a trivial program makes.

```
$ strace -c ls /usr > /dev/null
% time     seconds  usecs/call     calls    errors syscall
 18.61    0.000190          27         7           read
 17.34    0.000177          35         5           mprotect
 11.75    0.000120          13         9           close
 10.19    0.000104          14         7           openat
  5.78    0.000059          29         2           getdents64
```

**What you should notice:** `ls` is a few lines of logic, yet it makes dozens of calls: `openat` to open the directory, `getdents64` to read its entries, `write` to print (not shown), `mprotect` and `mmap` from the dynamic loader. Every line of the table is a mode switch.
:::

::: trap
*Claim:* "A system call is just a function call." *Why it is wrong:* it changes privilege level, switches stacks, and with the speculative-execution mitigations in current kernels costs from about a hundred nanoseconds to over a microsecond, against a few nanoseconds for an ordinary call. *Correct statement:* a system call is a controlled, expensive entry into the kernel; high-performance I/O designs (batching, `epoll`, `io_uring`, kernel bypass) exist to make fewer of them.
:::

::: check
1. Why can a user program not simply execute the instruction that disables interrupts? [^c71-1]
2. Name two things that move execution from user mode to kernel mode other than a system call. [^c71-2]
:::

[^c71-1]: It is a privileged instruction; in user mode the CPU raises a fault and the kernel decides what happens, normally terminating the program.
[^c71-2]: A hardware interrupt (timer, NIC) and an exception such as a page fault or a divide by zero.

## [7.2]{.sec}Processes, fork and exec [Must · ■■□]{.tag} {#s7-2}

A *process* is a program in execution. The kernel represents it by a *process control block*, called `task_struct` in Linux, which records the identifier (PID), the scheduling state, the saved registers, a pointer to the memory map, the open files and the signal settings. Each process owns a private *virtual address space* (the memory model, segment by segment, is in [Pillar 2](#s2-1){.ref}); Figure 7.2 shows how the control block points to it.

<figure>
<svg viewBox="0 0 480 235" width="480"><defs><marker id="ipc" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="apc" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><text class="lbl" x="75" y="12" text-anchor="middle">PCB (task_struct)</text><rect class="box" x="10" y="20" width="130" height="22" rx="0"/><text class="sm" x="75.0" y="34" text-anchor="middle">pid, parent pid</text><rect class="fill" x="10" y="42" width="130" height="22" rx="0"/><text class="sm" x="75.0" y="56" text-anchor="middle">state</text><rect class="box" x="10" y="64" width="130" height="22" rx="0"/><text class="sm" x="75.0" y="78" text-anchor="middle">saved PC and registers</text><rect class="fill" x="10" y="86" width="130" height="22" rx="0"/><text class="sm" x="75.0" y="100" text-anchor="middle">priority, scheduling data</text><rect class="box" x="10" y="108" width="130" height="22" rx="0"/><text class="sm" x="75.0" y="122" text-anchor="middle">mm_struct pointer</text><rect class="fill" x="10" y="130" width="130" height="22" rx="0"/><text class="sm" x="75.0" y="144" text-anchor="middle">open-file table</text><rect class="box" x="10" y="152" width="130" height="22" rx="0"/><text class="sm" x="75.0" y="166" text-anchor="middle">signal handlers and masks</text><rect class="fill" x="10" y="174" width="130" height="22" rx="0"/><text class="sm" x="75.0" y="188" text-anchor="middle">kernel stack pointer</text><line class="acc" x1="140" y1="119" x2="213" y2="125" marker-end="url(#apc)" /><text class="lbl" x="285" y="12" text-anchor="middle">virtual address space (x86-64)</text><rect class="fill" x="215" y="20" width="165" height="28" rx="0"/><text class="sm" x="297.5" y="37.0" text-anchor="middle">kernel (shared by all processes)</text><rect class="box dash" x="215" y="48" width="165" height="22" rx="0" style="fill:#fafafa"/><text class="sm" x="297.5" y="62.0" text-anchor="middle">unmapped canonical hole</text><rect class="box" x="215" y="70" width="165" height="30" rx="0"/><text class="sm" x="297.5" y="88.0" text-anchor="middle">stack (grows down)</text><rect class="box" x="215" y="100" width="165" height="34" rx="0"/><text class="sm" x="297.5" y="120.0" text-anchor="middle">mmap: libraries, files, big blocks</text><rect class="box" x="215" y="134" width="165" height="30" rx="0"/><text class="sm" x="297.5" y="152.0" text-anchor="middle">heap (grows up)</text><rect class="fill" x="215" y="164" width="165" height="24" rx="0"/><text class="sm" x="297.5" y="179.0" text-anchor="middle">.bss  .data  .rodata</text><rect class="box" x="215" y="188" width="165" height="24" rx="0"/><text class="sm" x="297.5" y="203.0" text-anchor="middle">.text (program code)</text><text class="mono" x="386" y="36" text-anchor="start">0xffff 8000...</text><text class="mono" x="386" y="208" text-anchor="start">0x0000 0000 4000</text><text class="mono" x="386" y="62" text-anchor="start">0x7ffd...</text><text class="sm" x="386" y="220" text-anchor="start">low addresses</text><text class="sm" x="386" y="20" text-anchor="start">high addresses</text><text class="sm" x="10" y="232" text-anchor="start">Segment details: Chapter 2. ASLR moves every user region at each run.</text></svg>
<figcaption><b>Figure 7.2</b> The PCB (left) and the address space it describes (right). The kernel half is the same in every process; the user half is private.</figcaption>
</figure>

A process is always in one of five states, shown in Figure 7.3. It is *ready* when it could run but is waiting for a CPU, *running* when it holds one, and *waiting* (or blocked) when it needs an event such as disk or network data. Only the scheduler moves a task between ready and running; only an event moves it from waiting to ready.

<figure>
<svg viewBox="0 0 480 175" width="480"><defs><marker id="ist" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="ast" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><rect class="box" x="7" y="65" width="76" height="30" rx="14"/><text class="lbl" x="45.0" y="83.0" text-anchor="middle">New</text><rect class="box" x="132" y="65" width="76" height="30" rx="14"/><text class="lbl" x="170.0" y="83.0" text-anchor="middle">Ready</text><rect class="box" x="282" y="65" width="76" height="30" rx="14" style="fill:#FFF4C2"/><text class="lbl" x="320.0" y="83.0" text-anchor="middle">Running</text><rect class="box" x="402" y="65" width="76" height="30" rx="14"/><text class="lbl" x="440.0" y="83.0" text-anchor="middle">Terminated</text><rect class="box" x="207" y="135" width="76" height="30" rx="14"/><text class="lbl" x="245.0" y="153.0" text-anchor="middle">Waiting</text><line class="ln" x1="83" y1="80" x2="132" y2="80" marker-end="url(#ist)" /><text class="sm" x="108" y="72" text-anchor="middle">admit</text><path class="ln" d="M208,70 Q245,52 282,70" marker-end="url(#ist)" /><text class="sm" x="245" y="52" text-anchor="middle">dispatch</text><path class="acc" d="M282,90 Q245,108 208,90" marker-end="url(#ast)" /><text class="sm" x="245" y="112" text-anchor="middle">timeout / pre-empt</text><line class="ln" x1="358" y1="80" x2="402" y2="80" marker-end="url(#ist)" /><text class="sm" x="380" y="72" text-anchor="middle">exit</text><path class="ln" d="M305,95 Q290,140 283,140" marker-end="url(#ist)" /><text class="sm" x="335" y="128" text-anchor="middle">I/O or event wait</text><path class="ln" d="M207,140 Q175,135 170,96" marker-end="url(#ist)" /><text class="sm" x="100" y="128" text-anchor="middle">I/O done, event</text></svg>
<figcaption><b>Figure 7.3</b> Process states. Only the accent-coloured transition, pre-emption, is forced on the running process.</figcaption>
</figure>

### Creating processes: fork, exec, wait

Linux creates a process by duplication. `fork()` returns twice: in the parent it returns the child's PID, and in the child it returns 0. The child receives a copy of the parent's address space, made cheap by *copy-on-write* ([7.7](#s7-7){.ref}): both processes share the same physical pages, marked read-only, until one writes. `exec()` replaces the calling process's program with a new one while keeping its PID and open files. A shell runs a command as `fork`, then `exec` in the child, then `wait` in the parent. `wait()` returns the child's exit status and lets the kernel discard its control block.

The program below is the core of a shell: it forks, the child becomes the requested command through `execvp`, and the parent waits and reports how the child ended.

```c
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char **argv)          /* usage: ./run command [args...] */
{
    if (argc < 2) {
        fprintf(stderr, "usage: run command [args]\n");
        return 2;
    }
    pid_t pid = fork();
    if (pid < 0) {
        perror("fork");
        return 1;
    }
    if (pid == 0) {                      /* child: become the command */
        execvp(argv[1], argv + 1);
        perror("execvp");                /* reached only if exec failed */
        _exit(127);
    }
    int st;
    waitpid(pid, &st, 0);                /* parent: wait, read the status */
    if (WIFEXITED(st))
        printf("pid %d exited with status %d\n", (int)pid, WEXITSTATUS(st));
    else if (WIFSIGNALED(st))
        printf("pid %d killed by signal %d\n", (int)pid, WTERMSIG(st));
    return 0;
}
```

```
$ ./run sh -c 'exit 3'
pid 17619 exited with status 3
$ ./run nosuchcmd
execvp: No such file or directory
pid 17620 exited with status 127
$ ./run sh -c 'kill -9 $$'
pid 17623 killed by signal 9
```

Note that the line `perror("execvp")` runs only when `exec` fails, since a successful `exec` never returns; the child then uses `_exit`, which skips the duplicated stdio buffers.

Fork puzzles ask how many lines a program prints. The rule is that each `fork()` doubles the number of processes that execute the code after it. Hence a loop of three forks yields 2³ = 8 processes, each printing the line below the loop.

```c
#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void)
{
    for (int i = 0; i < 3; i++)
        fork();
    printf("hi\n");
    while (wait(NULL) > 0)      /* reap children so output is complete */
        ;
    return 0;
}
```

The output is eight lines (`./fork3 | wc -l` prints 8). The variant `fork() && fork() || fork()` is subtler, because `&&` and `||` short-circuit and the child sees a different return value from the parent. The parent gets a non-zero PID from both forks, so the `||` is skipped. The first child gets 0 from its fork, skips the `&&` branch and evaluates the third fork; the second child gets 0 from its own fork and does the same. Counting the survivors gives five processes (Figure 7.4).

<figure>
<svg viewBox="0 0 480 200" width="480"><defs><marker id="ift" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="aft" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><text class="lbl" x="30" y="33" text-anchor="end">P</text><line class="ln" x1="40" y1="30" x2="380" y2="30" /><rect class="box" x="380" y="22" width="70" height="16" rx="0" style="fill:#FFF4C2"/><text class="sm" x="415.0" y="33.0" text-anchor="middle">prints</text><text class="lbl" x="30" y="69" text-anchor="end">C1</text><line class="ln" x1="100" y1="66" x2="380" y2="66" /><rect class="box" x="380" y="58" width="70" height="16" rx="0" style="fill:#FFF4C2"/><text class="sm" x="415.0" y="69.0" text-anchor="middle">prints</text><text class="lbl" x="30" y="105" text-anchor="end">C4</text><line class="ln" x1="290" y1="102" x2="380" y2="102" /><rect class="box" x="380" y="94" width="70" height="16" rx="0" style="fill:#FFF4C2"/><text class="sm" x="415.0" y="105.0" text-anchor="middle">prints</text><text class="lbl" x="30" y="141" text-anchor="end">C2</text><line class="ln" x1="190" y1="138" x2="380" y2="138" /><rect class="box" x="380" y="130" width="70" height="16" rx="0" style="fill:#FFF4C2"/><text class="sm" x="415.0" y="141.0" text-anchor="middle">prints</text><text class="lbl" x="30" y="177" text-anchor="end">C3</text><line class="ln" x1="290" y1="174" x2="380" y2="174" /><rect class="box" x="380" y="166" width="70" height="16" rx="0" style="fill:#FFF4C2"/><text class="sm" x="415.0" y="177.0" text-anchor="middle">prints</text><line class="acc" x1="100" y1="30" x2="100" y2="65" marker-end="url(#aft)" /><text class="sm" x="105" y="42" text-anchor="start">fork 1</text><line class="acc" x1="190" y1="30" x2="190" y2="137" marker-end="url(#aft)" /><text class="sm" x="195" y="42" text-anchor="start">fork 2</text><line class="acc" x1="290" y1="66" x2="290" y2="101" marker-end="url(#aft)" /><text class="sm" x="295" y="78" text-anchor="start">fork 3</text><line class="acc" x1="290" y1="138" x2="290" y2="173" marker-end="url(#aft)" /><text class="sm" x="295" y="150" text-anchor="start">fork 3</text><text class="sm" x="200" y="22" text-anchor="start">both forks true; || skips fork 3</text><text class="sm" x="106" y="60" text-anchor="start">gave 0: skip fork 2</text><text class="sm" x="196" y="132" text-anchor="start">gave 0</text><text class="sm" x="240" y="192" text-anchor="middle">P runs forks 1 and 2 only; C1 and C2 each continue to fork 3, which creates C4 and C3.</text></svg>
<figcaption><b>Figure 7.4</b> Process tree for fork() && fork() || fork(). Each process that finishes the expression prints once; there are five.</figcaption>
</figure>

::: trap
*Claim:* "`printf("hi")` before a `fork` prints once." *Why it is wrong:* when standard output is a pipe or file it is fully buffered, so the unflushed text sits in the process's memory and is copied into the child. Both processes flush it at exit. *Correct statement:* the text is printed twice; end the line with `\n` on a terminal, or call `fflush(stdout)` before forking.
:::

### Zombies and orphans

When a child exits, the kernel keeps its control block until the parent calls `wait()`, so the parent can still read the exit status. Between exit and `wait()` the child is a *zombie*: it uses no memory beyond the block, but it occupies a PID, and a parent that never waits eventually exhausts them. An *orphan* is the opposite case, a child whose parent has exited first. The kernel re-parents it to PID 1 (or to a designated subreaper), which calls `wait()` for it.

```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

int main(void)
{
    pid_t pid = fork();
    if (pid == 0)
        _exit(7);                       /* child exits at once */
    printf("child %d is a zombie for 5 s\n", (int)pid);
    fflush(stdout);
    sleep(5);                           /* run: ps -o pid,ppid,stat,cmd */
    int st;
    waitpid(pid, &st, 0);               /* reaping removes the zombie */
    printf("exit status %d\n", WEXITSTATUS(st));
    return 0;
}
```

::: lab
`LAB 7.2 · 10 MIN` Create and reap a zombie. Run `./zombie &`, then in the same second:

```
$ ps -o pid,ppid,stat,cmd --ppid $(pgrep zombie)
  PID  PPID STAT CMD
 8935  8933 Z    [zombie] <defunct>
exit status 7
```

**What you should notice:** state `Z` and the label `<defunct>` mark the zombie. It cannot be killed, because it is already dead; only its parent's `wait()` (or the parent's death) removes it.
:::

::: lens
[CISCO · JUNIPER · QUALCOMM]{.co}

"How many times does this print?" with `fork` in a loop, and "what is a zombie?", are reported in Cisco, Juniper and Qualcomm technical rounds. A strong answer states the doubling rule, draws the process tree, mentions stdout buffering if the output is redirected, and gives both the zombie definition and its cause (the parent did not wait). Follow-ups: how `exec` differs from `fork`, and what the shell does between them.
:::

::: check
1. How many processes exist after `fork(); fork(); fork();` executed once by one process? [^c72-1]
2. What does `fork()` return in the child? [^c72-2]
3. Does `exec()` create a new process? [^c72-3]
:::

[^c72-1]: Eight, counting the original: each fork doubles the count.
[^c72-2]: Zero. In the parent it returns the child's PID; on failure it returns -1 and no child exists.
[^c72-3]: No. It replaces the program image of the calling process; the PID and open descriptors survive.

## [7.3]{.sec}Threads and context switching [Must · ■■□]{.tag} {#s7-3}

A *thread* is an execution context inside a process. All threads of a process share the code, the global data, the heap and the open files; each has its own stack, its own saved registers and its own *thread-local storage*, including `errno`. Because the address space is shared, creating a thread needs no new page tables and communicating between threads needs no kernel call: a write by one thread is visible to the others. The same sharing is the hazard.

<figure>
<svg viewBox="0 0 480 190" width="480"><defs><marker id="ith" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="ath" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><text class="lbl" x="105" y="12" text-anchor="middle">one thread per process</text><text class="lbl" x="360" y="12" text-anchor="middle">three threads in one process</text><rect class="fill" x="15" y="20" width="180" height="100" rx="0"/><text class="lbl" x="105.0" y="73.0" text-anchor="middle"></text><rect class="box" x="25" y="30" width="160" height="20" rx="0"/><text class="sm" x="105.0" y="43.0" text-anchor="middle">code, data, heap</text><rect class="box" x="25" y="54" width="160" height="20" rx="0"/><text class="sm" x="105.0" y="67.0" text-anchor="middle">open files, signal handlers</text><rect class="box" x="25" y="82" width="70" height="30" rx="0"/><text class="sm" x="60.0" y="96.0" text-anchor="middle">registers</text><text class="sm" x="60.0" y="105.0" text-anchor="middle">PC, SP</text><rect class="box" x="105" y="82" width="80" height="30" rx="0"/><text class="sm" x="145.0" y="96.0" text-anchor="middle">stack</text><text class="sm" x="145.0" y="105.0" text-anchor="middle">private</text><rect class="fill" x="245" y="20" width="230" height="130" rx="0"/><text class="lbl" x="360.0" y="88.0" text-anchor="middle"></text><rect class="box" x="255" y="30" width="210" height="20" rx="0"/><text class="sm" x="360.0" y="43.0" text-anchor="middle">code, data, heap (shared)</text><rect class="box" x="255" y="54" width="210" height="20" rx="0"/><text class="sm" x="360.0" y="67.0" text-anchor="middle">open files, signal handlers (shared)</text><rect class="box" x="255" y="82" width="66" height="22" rx="0"/><text class="sm" x="288.0" y="96.0" text-anchor="middle">stack 1</text><rect class="box" x="255" y="108" width="66" height="22" rx="0"/><text class="sm" x="288.0" y="122.0" text-anchor="middle">registers</text><rect class="box" x="327" y="82" width="66" height="22" rx="0"/><text class="sm" x="360.0" y="96.0" text-anchor="middle">stack 2</text><rect class="box" x="327" y="108" width="66" height="22" rx="0" style="fill:#FFF4C2"/><text class="sm" x="360.0" y="122.0" text-anchor="middle">registers</text><rect class="box" x="399" y="82" width="66" height="22" rx="0"/><text class="sm" x="432.0" y="96.0" text-anchor="middle">stack 3</text><rect class="box" x="399" y="108" width="66" height="22" rx="0"/><text class="sm" x="432.0" y="122.0" text-anchor="middle">registers</text><text class="sm" x="360" y="144" text-anchor="middle">private: stack, registers, TLS, errno</text><text class="sm" x="105" y="140" text-anchor="middle">A second process would repeat the whole block.</text><text class="sm" x="105" y="152" text-anchor="middle">Its page tables are separate; a thread's are not.</text><text class="sm" x="240" y="178" text-anchor="middle">A thread that corrupts the shared heap damages every other thread; a crash ends the process.</text></svg>
<figcaption><b>Figure 7.5</b> Process versus threads. Threads share everything except stack, registers and thread-local storage.</figcaption>
</figure>

Linux implements a thread as a task that shares its parent's address space (the `clone()` system call with the sharing flags set), which is the *1:1* model: one kernel-scheduled task per user thread, so threads run in parallel on different cores. Runtimes such as Go multiplex many lightweight tasks onto few kernel threads (*M:N*), gaining cheap creation at the cost of a second scheduler.

::: bigidea
Sharing memory makes threads cheap to create and to switch, and it is also why a bug in one thread can corrupt, or terminate, every other thread in the process.
:::

### The race condition

Two threads that each increment a shared counter one million times should produce two million. They do not, because `counter++` compiles to three steps (load, add, store), and the threads interleave between them. the table below shows how one update is lost.

| Step | Thread A | Thread B | counter in memory |
|---|---|---|---|
| 1 | load counter (5) | | 5 |
| 2 | | load counter (5) | 5 |
| 3 | add 1 (6) | | 5 |
| 4 | | add 1 (6) | 5 |
| 5 | store 6 | | 6 |
| 6 | | store 6 | 6 |

Both threads read 5 and both store 6, so one increment vanishes.

```c
#include <pthread.h>
#include <stdio.h>

#define N 1000000
static volatile long counter;   /* volatile: keep it out of a register */
static pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;

static void *plain(void *arg)
{
    (void)arg;
    for (int i = 0; i < N; i++)
        counter++;                      /* load, add, store: not atomic */
    return NULL;
}

static void *locked(void *arg)
{
    (void)arg;
    for (int i = 0; i < N; i++) {
        pthread_mutex_lock(&m);
        counter++;
        pthread_mutex_unlock(&m);
    }
    return NULL;
}

static void run(void *(*fn)(void *), const char *name)
{
    pthread_t a, b;
    counter = 0;
    pthread_create(&a, NULL, fn, NULL);
    pthread_create(&b, NULL, fn, NULL);
    pthread_join(a, NULL);
    pthread_join(b, NULL);
    printf("%-8s counter = %ld (expected %d)\n", name, counter, 2 * N);
}

int main(void)
{
    run(plain, "plain");
    run(locked, "mutex");
    return 0;
}
```

```
$ gcc -O1 -pthread race.c -o race && ./race
plain    counter = 1092934 (expected 2000000)
mutex    counter = 2000000 (expected 2000000)
```

The unprotected total falls anywhere between about one and two million, and differs on each run. The `volatile` qualifier is present only to stop the optimiser from keeping the counter in a register, which would hide the race on some compilers; it does not fix it ([7.13](#s7-13){.ref}). The ThreadSanitizer (`gcc -fsanitize=thread -g`) reports it directly: `WARNING: ThreadSanitizer: data race`, with the two source lines involved.

### What a context switch does

A *context switch* stops one task and starts another. The kernel (i) saves the running task's registers and program counter into its control block, (ii) lets the scheduler choose the next task, (iii) if the next task belongs to a different process, loads its page-table base register, which invalidates or retags the TLB entries ([7.7](#s7-7){.ref}), and (iv) restores the next task's registers. Step (iii) is the reason that switching between threads of the same process is cheaper than switching between processes: the address space does not change, so the cached translations and, to a lesser degree, the data caches stay useful. The direct cost of a switch is a few microseconds; the indirect cost, the cold caches afterwards, is often larger.

<figure>
<svg viewBox="0 0 480 120" width="480"><defs><marker id="ics" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="acs" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><rect class="fill" x="8" y="30" width="62" height="40" rx="0"/><text class="lbl" x="39.0" y="53.0" text-anchor="middle"></text><text class="sm" x="39.0" y="46" text-anchor="middle">A runs</text><text class="sm" x="39.0" y="86" text-anchor="middle">user mode</text><line class="ln" x1="70" y1="50" x2="74" y2="50" marker-end="url(#ics)" /><rect class="box" x="74" y="30" width="62" height="40" rx="0"/><text class="lbl" x="105.0" y="53.0" text-anchor="middle"></text><text class="sm" x="105.0" y="46" text-anchor="middle">interrupt</text><text class="sm" x="105.0" y="55" text-anchor="middle">or block</text><text class="sm" x="105.0" y="86" text-anchor="middle">enter kernel</text><line class="ln" x1="136" y1="50" x2="140" y2="50" marker-end="url(#ics)" /><rect class="box" x="140" y="30" width="62" height="40" rx="0"/><text class="lbl" x="171.0" y="53.0" text-anchor="middle"></text><text class="sm" x="171.0" y="46" text-anchor="middle">save A</text><text class="sm" x="171.0" y="86" text-anchor="middle">regs to PCB</text><line class="ln" x1="202" y1="50" x2="206" y2="50" marker-end="url(#ics)" /><rect class="box" x="206" y="30" width="62" height="40" rx="0"/><text class="lbl" x="237.0" y="53.0" text-anchor="middle"></text><text class="sm" x="237.0" y="46" text-anchor="middle">scheduler</text><text class="sm" x="237.0" y="86" text-anchor="middle">picks B</text><line class="ln" x1="268" y1="50" x2="272" y2="50" marker-end="url(#ics)" /><rect class="box dash" x="272" y="30" width="62" height="40" rx="0" style="fill:#FFF4C2"/><text class="lbl" x="303.0" y="53.0" text-anchor="middle"></text><text class="sm" x="303.0" y="46" text-anchor="middle">load</text><text class="sm" x="303.0" y="55" text-anchor="middle">B tables</text><text class="sm" x="303.0" y="86" text-anchor="middle">new process only</text><line class="ln" x1="334" y1="50" x2="338" y2="50" marker-end="url(#ics)" /><rect class="box" x="338" y="30" width="62" height="40" rx="0"/><text class="lbl" x="369.0" y="53.0" text-anchor="middle"></text><text class="sm" x="369.0" y="46" text-anchor="middle">restore B</text><text class="sm" x="369.0" y="86" text-anchor="middle">regs from PCB</text><line class="ln" x1="400" y1="50" x2="404" y2="50" marker-end="url(#ics)" /><rect class="fill" x="404" y="30" width="62" height="40" rx="0"/><text class="lbl" x="435.0" y="53.0" text-anchor="middle"></text><text class="sm" x="435.0" y="46" text-anchor="middle">B runs</text><text class="sm" x="435.0" y="86" text-anchor="middle">user mode</text><text class="lbl" x="240" y="14" text-anchor="middle">A thread switch inside one process skips the shaded step, so the TLB and caches stay useful.</text><text class="sm" x="240" y="108" text-anchor="middle">The direct cost is microseconds; the indirect cost, cold caches and TLB after the switch, is often larger.</text></svg>
<figcaption><b>Figure 7.6</b> The steps of a context switch. The shaded step is skipped when both tasks are threads of one process.</figcaption>
</figure>

::: lab
`LAB 7.3 · 10 MIN` Let ThreadSanitizer find the race, then confirm the fix.

```
$ gcc -fsanitize=thread -g -O1 race.c -o racet -pthread && ./racet
WARNING: ThreadSanitizer: data race
  Read of size 8 ... by thread T2:
    #0 plain race.c:12
SUMMARY: ThreadSanitizer: data race race.c:12 in plain
```

**What you should notice:** every report names a line in `plain` (line 12, the unprotected increment) and none names `locked`. The sanitizer finds races that did not happen to corrupt the output on this run, which is why it belongs in every threaded project's test build.
:::

::: trap
*Claim:* "Threads have their own heaps" or "a thread switch flushes the TLB." *Why it is wrong:* the heap belongs to the process, and a switch inside one process keeps the same page tables. *Correct statement:* threads share the heap; only the stack, registers and thread-local storage are private, and a TLB flush happens only when the address space changes.
:::

::: lens
[CISCO · QUALCOMM · JUNIPER · ARISTA]{.co}

"Process versus thread" is asked at nearly every networking employer, usually followed by "what happens if one thread crashes?". A strong answer gives the shared and private lists, states that a fault such as SIGSEGV is delivered to the process and ends all threads, and compares the switch cost with a reason (no address-space change). Follow-ups: thread safety and reentrancy (`strtok` keeps a hidden static pointer, so it is unsafe; `strtok_r` takes the state as an argument), and why a server prefers a pool of threads to one thread per request.
:::

::: check
1. Which segments are private to a thread? [^c73-1]
2. Why is the unprotected counter result different on each run? [^c73-2]
:::

[^c73-1]: The stack, the registers (including the program counter) and thread-local storage.
[^c73-2]: The interleaving depends on when the scheduler pre-empts each thread, which varies with load and timing; the lost updates vary with it.

## [7.4]{.sec}CPU scheduling [Should · ■■□]{.tag} {#s7-4}

The *scheduler* chooses which ready task runs next, balancing throughput (work finished per second), latency (time to first response) and fairness. A *non-pre-emptive* algorithm lets a task run until it blocks or finishes; a *pre-emptive* one can interrupt it, normally on a timer tick. For one task we define the *turnaround time* TAT = completion − arrival and the *waiting time* WT = TAT − burst, where the burst is the CPU time needed.

We compare four algorithms on five processes: P1 arrives at 0 with burst 8, P2 at 1 with 4, P3 at 2 with 9, P4 at 3 with 5, P5 at 4 with 2.

<figure>
<svg viewBox="0 0 480 232" width="480"><defs><marker id="igt" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="agt" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><text class="lbl" x="6" y="25" text-anchor="start">FCFS</text><rect class="box" x="62.0" y="12" width="112.0" height="20" rx="0"/><text class="sm" x="118.0" y="25.0" text-anchor="middle">P1</text><rect class="fill" x="174.0" y="12" width="56.0" height="20" rx="0"/><text class="sm" x="202.0" y="25.0" text-anchor="middle">P2</text><rect class="box" x="230.0" y="12" width="126.0" height="20" rx="0"/><text class="sm" x="293.0" y="25.0" text-anchor="middle">P3</text><rect class="fill" x="356.0" y="12" width="70.0" height="20" rx="0"/><text class="sm" x="391.0" y="25.0" text-anchor="middle">P4</text><rect class="box" x="426.0" y="12" width="28.0" height="20" rx="0"/><text class="sm" x="440.0" y="25.0" text-anchor="middle">P5</text><text class="lbl" x="6" y="63" text-anchor="start">SJF</text><rect class="box" x="62.0" y="50" width="112.0" height="20" rx="0"/><text class="sm" x="118.0" y="63.0" text-anchor="middle">P1</text><rect class="box" x="174.0" y="50" width="28.0" height="20" rx="0"/><text class="sm" x="188.0" y="63.0" text-anchor="middle">P5</text><rect class="fill" x="202.0" y="50" width="56.0" height="20" rx="0"/><text class="sm" x="230.0" y="63.0" text-anchor="middle">P2</text><rect class="fill" x="258.0" y="50" width="70.0" height="20" rx="0"/><text class="sm" x="293.0" y="63.0" text-anchor="middle">P4</text><rect class="box" x="328.0" y="50" width="126.0" height="20" rx="0"/><text class="sm" x="391.0" y="63.0" text-anchor="middle">P3</text><text class="lbl" x="6" y="101" text-anchor="start">SRTF</text><rect class="box" x="62.0" y="88" width="14.0" height="20" rx="0"/><text class="sm" x="69.0" y="101.0" text-anchor="middle"></text><rect class="fill" x="76.0" y="88" width="56.0" height="20" rx="0"/><text class="sm" x="104.0" y="101.0" text-anchor="middle">P2</text><rect class="box" x="132.0" y="88" width="28.0" height="20" rx="0"/><text class="sm" x="146.0" y="101.0" text-anchor="middle">P5</text><rect class="fill" x="160.0" y="88" width="70.0" height="20" rx="0"/><text class="sm" x="195.0" y="101.0" text-anchor="middle">P4</text><rect class="box" x="230.0" y="88" width="98.0" height="20" rx="0"/><text class="sm" x="279.0" y="101.0" text-anchor="middle">P1</text><rect class="box" x="328.0" y="88" width="126.0" height="20" rx="0"/><text class="sm" x="391.0" y="101.0" text-anchor="middle">P3</text><text class="lbl" x="6" y="139" text-anchor="start">RR q=2</text><rect class="box" x="62.0" y="126" width="28.0" height="20" rx="0"/><text class="sm" x="76.0" y="139.0" text-anchor="middle">P1</text><rect class="fill" x="90.0" y="126" width="28.0" height="20" rx="0"/><text class="sm" x="104.0" y="139.0" text-anchor="middle">P2</text><rect class="box" x="118.0" y="126" width="28.0" height="20" rx="0"/><text class="sm" x="132.0" y="139.0" text-anchor="middle">P3</text><rect class="box" x="146.0" y="126" width="28.0" height="20" rx="0"/><text class="sm" x="160.0" y="139.0" text-anchor="middle">P1</text><rect class="fill" x="174.0" y="126" width="28.0" height="20" rx="0"/><text class="sm" x="188.0" y="139.0" text-anchor="middle">P4</text><rect class="box" x="202.0" y="126" width="28.0" height="20" rx="0"/><text class="sm" x="216.0" y="139.0" text-anchor="middle">P5</text><rect class="fill" x="230.0" y="126" width="28.0" height="20" rx="0"/><text class="sm" x="244.0" y="139.0" text-anchor="middle">P2</text><rect class="box" x="258.0" y="126" width="28.0" height="20" rx="0"/><text class="sm" x="272.0" y="139.0" text-anchor="middle">P3</text><rect class="box" x="286.0" y="126" width="28.0" height="20" rx="0"/><text class="sm" x="300.0" y="139.0" text-anchor="middle">P1</text><rect class="fill" x="314.0" y="126" width="28.0" height="20" rx="0"/><text class="sm" x="328.0" y="139.0" text-anchor="middle">P4</text><rect class="box" x="342.0" y="126" width="28.0" height="20" rx="0"/><text class="sm" x="356.0" y="139.0" text-anchor="middle">P3</text><rect class="box" x="370.0" y="126" width="28.0" height="20" rx="0"/><text class="sm" x="384.0" y="139.0" text-anchor="middle">P1</text><rect class="fill" x="398.0" y="126" width="14.0" height="20" rx="0"/><text class="sm" x="405.0" y="139.0" text-anchor="middle"></text><rect class="box" x="412.0" y="126" width="28.0" height="20" rx="0"/><text class="sm" x="426.0" y="139.0" text-anchor="middle">P3</text><rect class="box" x="440.0" y="126" width="14.0" height="20" rx="0"/><text class="sm" x="447.0" y="139.0" text-anchor="middle"></text><text class="sm" x="460.0" y="22" text-anchor="middle"></text><line class="ln" x1="62.0" y1="158" x2="62.0" y2="162" /><text class="sm" x="62.0" y="172" text-anchor="middle">0</text><line class="ln" x1="90.0" y1="158" x2="90.0" y2="162" /><text class="sm" x="90.0" y="172" text-anchor="middle">2</text><line class="ln" x1="118.0" y1="158" x2="118.0" y2="162" /><text class="sm" x="118.0" y="172" text-anchor="middle">4</text><line class="ln" x1="146.0" y1="158" x2="146.0" y2="162" /><text class="sm" x="146.0" y="172" text-anchor="middle">6</text><line class="ln" x1="174.0" y1="158" x2="174.0" y2="162" /><text class="sm" x="174.0" y="172" text-anchor="middle">8</text><line class="ln" x1="202.0" y1="158" x2="202.0" y2="162" /><text class="sm" x="202.0" y="172" text-anchor="middle">10</text><line class="ln" x1="230.0" y1="158" x2="230.0" y2="162" /><text class="sm" x="230.0" y="172" text-anchor="middle">12</text><line class="ln" x1="258.0" y1="158" x2="258.0" y2="162" /><text class="sm" x="258.0" y="172" text-anchor="middle">14</text><line class="ln" x1="286.0" y1="158" x2="286.0" y2="162" /><text class="sm" x="286.0" y="172" text-anchor="middle">16</text><line class="ln" x1="314.0" y1="158" x2="314.0" y2="162" /><text class="sm" x="314.0" y="172" text-anchor="middle">18</text><line class="ln" x1="342.0" y1="158" x2="342.0" y2="162" /><text class="sm" x="342.0" y="172" text-anchor="middle">20</text><line class="ln" x1="370.0" y1="158" x2="370.0" y2="162" /><text class="sm" x="370.0" y="172" text-anchor="middle">22</text><line class="ln" x1="398.0" y1="158" x2="398.0" y2="162" /><text class="sm" x="398.0" y="172" text-anchor="middle">24</text><line class="ln" x1="426.0" y1="158" x2="426.0" y2="162" /><text class="sm" x="426.0" y="172" text-anchor="middle">26</text><line class="ln" x1="454.0" y1="158" x2="454.0" y2="162" /><text class="sm" x="454.0" y="172" text-anchor="middle">28</text><line class="ln" x1="62" y1="160" x2="454.0" y2="160" /><text class="sm" x="454.0" y="184" text-anchor="end">time</text><text class="sm" x="6" y="184" text-anchor="start">Arrivals: P1 at 0, P2 at 1, P3 at 2, P4 at 3, P5 at 4. Bursts 8, 4, 9, 5, 2.</text></svg>
<figcaption><b>Figure 7.7</b> Gantt charts for the five processes. Shorter jobs first (SJF, SRTF) cut the average wait; round robin raises it here but bounds the response time.</figcaption>
</figure>

::: example
**Average waiting time under FCFS.** First-come-first-served runs in arrival order, so P1 runs 0–8, P2 8–12, P3 12–21, P4 21–26, P5 26–28.

1. Waiting time = start − arrival for a task that runs without interruption: P1 0, P2 8 − 1 = 7, P3 12 − 2 = 10, P4 21 − 3 = 18, P5 26 − 4 = 22.
2. Sum = 57, average = 57/5.

[Result: average waiting time 11.4, average turnaround 17.0. The short P5 waits behind the long P3, the *convoy effect*.]{.result}
:::

| Algorithm | Pre-emptive? | Avg waiting | Avg turnaround | Property |
|---|---|---|---|---|
| FCFS | no | 11.4 | 17.0 | simple; convoy effect |
| SJF (shortest job first) | no | 8.2 | 13.8 | optimal waiting among non-pre-emptive; needs burst lengths; starves long jobs |
| SRTF (shortest remaining time first) | yes | 6.6 | 12.2 | optimal average waiting overall; many switches |
| Round robin, q = 2 | yes | 13.0 | 18.6 | fair; response bounded by (n − 1)q; q too small wastes time in switches |

Round robin lets each task run for at most a *quantum* q and then moves it to the back of the queue. Its numbers above assume that a task arriving at the instant a quantum ends joins the queue before the pre-empted task; the opposite convention changes the order and the totals slightly, so a question should state it. *Priority scheduling* runs the highest-priority ready task; low-priority tasks may *starve*, and *ageing*, which slowly raises the priority of waiting tasks, cures it. A *multilevel feedback queue* (MLFQ) combines these ideas: new tasks enter the top queue with a short quantum, a task that uses its whole quantum is demoted, and a periodic boost lifts everything back so that nothing starves.

<figure>
<svg viewBox="0 0 480 150" width="480"><defs><marker id="iml" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L8,4 L0,8 z" style="fill:#1A1D23"/></marker><marker id="aml" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto"><path class="accf" d="M0,0 L8,4 L0,8 z"/></marker></defs><text class="lbl" x="10" y="40" text-anchor="start">Queue 0</text><text class="sm" x="10" y="50" text-anchor="start">quantum 8</text><rect class="box" x="100" y="22" width="230" height="34" rx="0"/><text class="lbl" x="215.0" y="42.0" text-anchor="middle"></text><rect class="fill" x="106" y="28" width="46" height="22" rx="0"/><text class="sm" x="129.0" y="42.0" text-anchor="middle">job 1</text><rect class="fill" x="160" y="28" width="46" height="22" rx="0"/><text class="sm" x="183.0" y="42.0" text-anchor="middle">job 2</text><rect class="fill" x="214" y="28" width="46" height="22" rx="0"/><text class="sm" x="237.0" y="42.0" text-anchor="middle">job 3</text><rect class="fill" x="268" y="28" width="46" height="22" rx="0"/><text class="sm" x="291.0" y="42.0" text-anchor="middle">job 4</text><text class="lbl" x="10" y="80" text-anchor="start">Queue 1</text><text class="sm" x="10" y="90" text-anchor="start">quantum 16</text><rect class="box" x="100" y="62" width="230" height="34" rx="0"/><text class="lbl" x="215.0" y="82.0" text-anchor="middle"></text><rect class="fill" x="106" y="68" width="46" height="22" rx="0"/><text class="sm" x="129.0" y="82.0" text-anchor="middle"></text><rect class="fill" x="160" y="68" width="46" height="22" rx="0"/><text class="sm" x="183.0" y="82.0" text-anchor="middle"></text><rect class="fill" x="214" y="68" width="46" height="22" rx="0"/><text class="sm" x="237.0" y="82.0" text-anchor="middle"></text><rect class="fill" x="268" y="68" width="46" height="22" rx="0"/><text class="sm" x="291.0" y="82.0" text-anchor="middle"></text><text class="lbl" x="10" y="120" text-anchor="start">Queue 2</text><text class="sm" x="10" y="130" text-anchor="start">FCFS until done</text><rect class="box" x="100" y="102" width="230" height="34" rx="0"/><text class="lbl" x="215.0" y="122.0" text-anchor="middle"></text><rect class="fill" x="106" y="108" width="46" height="22" rx="0"/><text class="sm" x="129.0" y="122.0" text-anchor="middle"></text><rect class="fill" x="160" y="108" width="46" height="22" rx="0"/><text class="sm" x="183.0" y="122.0" text-anchor="middle"></text><rect class="fill" x="214" y="108" width="46" height="22" rx="0"/><text class="sm" x="237.0" y="122.0" text-anchor="middle"></text><rect class="fill" x="268" y="108" width="46" height="22" rx="0"/><text class="sm" x="291.0" y="122.0" text-anchor="middle"></text><line class="acc" x1="215" y1="56" x2="215" y2="62" marker-end="url(#aml)" /><line class="acc" x1="215" y1="96" x2="215" y2="102" marker-end="url(#aml)" /><text class="sm" x="222" y="60" text-anchor="start">full quantum used: demote</text><text class="sm" x="222" y="100" text-anchor="start">demote again</text><path class="ln" d="M340,119 L370,119 L370,39 L334,39" marker-end="url(#iml)" stroke-dasharray="3 2"/><text class="sm" x="376" y="82" text-anchor="start">periodic boost:</text><text class="sm" x="376" y="92" text-anchor="start">everything back to</text><text class="sm" x="376" y="102" text-anchor="start">queue 0</text><text class="sm" x="240" y="144" text-anchor="middle">New and interactive tasks stay near the top and run first; long CPU hogs sink, and the boost prevents starvation.</text></svg>
<figcaption><b>Figure 7.8</b> A multilevel feedback queue with three levels.</figcaption>
</figure>

Linux does not use a fixed quantum. The Completely Fair Scheduler kept a *virtual runtime* for each task, advanced more slowly for tasks of higher weight, and always ran the task with the smallest value; two tasks with weights 2 : 1 therefore receive CPU in the ratio 2 : 1. From Linux 6.6 the pick logic is EEVDF (earliest eligible virtual deadline first), which keeps the weighted-fair accounting but also lets latency-sensitive tasks ask for shorter slices. The interview-level statement is that Linux gives each runnable task a weighted fair share and picks the one that has had the least.

::: trap
*Claim:* "SJF is the best algorithm." *Why it is wrong:* it is optimal for average waiting time only if burst lengths are known in advance, which they are not, and it starves long jobs when short ones keep arriving. *Correct statement:* real schedulers estimate the next burst from history (exponential averaging) and use ageing or feedback to prevent starvation.
:::

::: check
1. In FCFS, which of TAT and WT is larger for a task, and by how much? [^c74-1]
2. What does ageing prevent? [^c74-2]
:::

[^c74-1]: TAT is larger, by exactly the burst time, since WT = TAT − burst.
[^c74-2]: Starvation of low-priority tasks, by raising a task's priority the longer it waits.

:::
