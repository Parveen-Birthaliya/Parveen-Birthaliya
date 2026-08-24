# Operating Systems — Last Minute Revision Notes (IBPS SO IT)

---

## 1. Introduction to OS

- **Application software**: performs specific task for user. **System software**: operates/controls computer, platform for apps.
- **OS**: manages all resources (HW + SW), provides convenient/efficient execution environment, hides hardware complexity, acts as **resource manager**.
- **Without OS**: bulky/complex apps (HW code inside app), resource exploitation by 1 app, no memory protection.
- **OS = collection of system software.**
- **Functions of OS**: access to hardware; interface between user & hardware; **resource management (aka Arbitration)** — memory, device, file, security, process; **hides complexity (aka Abstraction)**; facilitates execution via isolation & protection.
- Layer stack (top→bottom): **User → Application programs → OS → Hardware**.
- **OS goals**: max CPU utilization, less process starvation, higher priority job execution.

### Types of OS (with example systems — often asked!)
| Type | Example |
|---|---|
| Single process OS | MS-DOS (1981) — **oldest** |
| Batch-processing OS | ATLAS, Manchester Univ. (late 1950s–early 1960s) |
| Multiprogramming OS | THE, Dijkstra (early 1960s) |
| Multitasking OS | CTSS, MIT (early 1960s) |
| Multi-processing OS | Windows NT |
| Distributed system | LOCUS |
| Real-time OS | ATCS |

- **Single process OS**: only 1 process executes at a time from ready queue (oldest).
- **Batch-processing OS**: punch cards → operator → sorts into batches → submits batch-wise → all jobs of a batch executed together. Cons: no priority setting, starvation possible, CPU idle during I/O.
- **Multiprogramming**: ↑CPU utilization by keeping multiple jobs in memory so CPU always has work; single CPU; context switching when process waits; reduces CPU idle time.
- **Multitasking**: logical extension of multiprogramming; single CPU; runs >1 task simultaneously; uses context switching + time sharing; ↑responsiveness; CPU idle further reduced.
- **Multi-processing OS**: >1 CPU in single computer; ↑reliability (1 CPU fails, other works), better throughput, less starvation.
- **Distributed OS**: manages many resource bunches (≥1 CPU/memory/GPU); loosely connected autonomous, interconnected, independent, networked, physically separate nodes.
- **RTOS**: real-time, error-free computation within **tight time boundaries**. Eg: Air Traffic Control, Robots.

---

## 2. Multitasking vs Multithreading

- **Program**: compiled, executable code ready to run; stored in **disk**.
- **Process**: program **under execution**; resides in **RAM**.
- **Thread**: single sequence stream within a process; independent execution path; **lightweight process**; achieves parallelism by dividing a process's independent tasks. Eg: browser tabs; text editor (typing + spell-check + formatting + saving concurrently).

| Multi-Tasking | Multi-Threading |
|---|---|
| >1 process context switched | >1 thread (of same process) context switched |
| No. of CPUs = 1 | No. of CPUs ≥ 1 (better with >1) |
| Isolation & memory protection exists (separate memory/resources per program) | **No** isolation/protection — threads share process's memory & resources |

- **Thread scheduling**: based on priority; threads get processor time slices too.

### Thread vs Process Context Switching
| Thread CS | Process CS |
|---|---|
| Saves thread state, switches to another thread of **same** process | Saves process state, restores another process's state |
| **No** switching of memory address space (PC, registers, stack switch though) | **Includes** switching of memory address space |
| **Fast** switching | **Slow** switching |
| CPU cache **preserved** | CPU cache **flushed** |

---

## 3. Components of OS

- **Kernel**: interacts directly with hardware, performs crucial tasks; **heart/core** of OS; **first part loaded** at startup.
- **User space**: where application software runs (no privileged HW access); interacts with kernel via GUI/CLI.
- **Shell** (command interpreter): receives user commands, gets them executed.

### Functions of Kernel
1. **Process management**: scheduling processes/threads; create & delete user/system processes; suspend/resume; process sync/communication mechanisms.
2. **Memory management**: allocate/deallocate memory; track which part used by which process.
3. **File management**: create/delete files & directories; map files to secondary storage; backup support.
4. **I/O management**: buffering, caching, spooling.
   - **Spooling**: between two jobs of **differing speed** (eg print spooling, mail spooling).
   - **Buffering**: within **one job** (eg YouTube video buffering).
   - **Caching**: memory caching, web caching.

### Types of Kernels
| | Monolithic | Micro | Hybrid |
|---|---|---|---|
| Functions in kernel | **All** functions in kernel | Only **major** (memory + process mgmt); File/IO mgmt in **user-space** | File mgmt in user space, rest in kernel |
| Size | Bulky | Smaller | — |
| Memory req | High | Low | — |
| Reliability | **Less** (1 module crash → whole kernel down) | **More** reliable & stable | Combines both |
| Performance | **High** (fast comm, less US↔KS overhead) | **Slow** (overhead switching US↔KS) | Speed & design of mono + modularity/stability of micro |
| Examples | Linux, Unix, MS-DOS | L4 Linux, Symbian OS, **MINIX** | **MacOS, Windows NT/7/10** |

- Also: **Nano/Exo kernels**.
- **IPC (Inter-Process Communication)**: two independent processes (own memory space, protected) communicate via **shared memory** and **message passing**.

---

## 4. System Calls

- **System call**: mechanism for a user program to request kernel service it doesn't have permission to perform (I/O access, communicating with other programs).
- **System calls are the ONLY way** a process goes from **User Mode → Kernel Mode**.
- Transition US→KS done by **software interrupts**.
- System calls implemented in **C**.
- Stack: User App → Glibc → **System Call Interface (SCI)** → Kernel → Hardware.
- Example: `mkdir` is just a **wrapper** around actual system calls.

### 5 Types of System Calls
1. **Process Control**: end/abort, load/execute, create/terminate process, get/set process attributes, wait for time, wait/signal event, allocate/free memory.
2. **File Management**: create/delete file, open/close, read/write/reposition, get/set file attributes.
3. **Device Management**: request/release device, read/write/reposition, get/set device attributes, attach/detach.
4. **Information Maintenance**: get/set time/date, get/set system data, get/set process/file/device attributes.
5. **Communication Management**: create/delete connection, send/receive messages, transfer status info, attach/detach remote devices.

### Windows vs Unix System Calls (HIGH-YIELD TABLE)
| Category | Windows | Unix |
|---|---|---|
| Process Control | CreateProcess(), ExitProcess(), WaitForSingleObject() | fork(), exit(), wait() |
| File Mgmt | CreateFile(), ReadFile(), WriteFile(), CloseHandle() | open(), read(), write(), close() |
| Device Mgmt | SetConsoleMode(), ReadConsole(), WriteConsole() | ioctl(), read(), write() |
| Info Mgmt | GetCurrentProcessID(), SetTimer(), Sleep() | getpid(), alarm(), sleep() |
| Communication | CreatePipe(), CreateFileMapping(), MapViewOfFile() | pipe(), shmget(), mmap() |

---

## 5. Booting Process

1. PC On.
2. CPU looks for firmware (**BIOS**, a ROM chip on motherboard) — modern PCs load **UEFI** instead.
3. CPU runs BIOS → tests/initializes HW, loads config → error if missing HW → boot stops. This = **POST (Power On Self-Test)**.
   - UEFI is like a tiny OS; Intel CPUs have **Intel Management Engine** (powers Active Management Technology for remote mgmt).
4. BIOS hands off to OS's **bootloader** via **MBR (Master Boot Record)** — special boot sector at start of disk containing bootloader-loading code (or via EFI system partition for UEFI).
5. **Bootloader** boots rest of OS (Kernel first, then User space).
   - Windows: **Windows Boot Manager (Bootmgr.exe)**
   - Linux: **GRUB**
   - Mac: **boot.efi**

---

## 6. 32-bit vs 64-bit OS

- **32-bit**: 32-bit registers, 2³² addresses = **4 GB** physical memory.
- **64-bit**: 64-bit registers, 2⁶⁴ addresses = **17,179,869,184 GB**.
- 32-bit CPU processes 32 bits/cycle (4 bytes); 64-bit processes 64 bits/cycle (8 bytes).
- **Compatibility**: 64-bit CPU runs both 32 & 64-bit OS; 32-bit CPU runs **only** 32-bit OS.
- 64-bit advantages: more addressable memory, better resource usage w/ excess RAM, better performance (bigger registers → bigger calc/cycle), better graphics performance.

---

## 7. Storage / Memory Hierarchy

Order (fastest/costliest → slowest/cheapest): **Register → Cache → Main Memory (RAM) → Secondary memory (Electronic Disk → Magnetic Disk → Optical Disk → Magnetic Tapes)**

- **Register**: smallest storage unit, part of CPU itself; holds instruction/address/data; used for immediate CPU use.
- **Cache**: stores frequently used instructions/data for quicker processing.
- **Main Memory**: RAM.
- **Secondary Memory**: storage media for data & programs.

| Factor | Primary | Secondary |
|---|---|---|
| Cost | Costly (Registers most expensive) | Cheaper |
| Access speed | Higher (Register > Cache > Main memory) | Lower |
| Storage size | Smaller | More |
| Volatility | **Volatile** | **Non-volatile** |

---

## 8. Process — Introduction

- **Program** = compiled code, ready to execute. **Process** = program under execution.
- **OS creates process (steps)**: load program+static data into memory → allocate runtime stack → heap allocation → IO tasks → OS handoffs control to `main()`.
- **Process memory architecture (high→low)**:
  - **Stack**: local variables, function args, return values.
  - **Heap**: dynamically allocated variables.
  - **Data**: global & static data.
  - **Text**: compiled code (loaded from disk).
- **Process table**: OS tracks all processes; each entry = **PCB (Process Control Block)**.
- **PCB structure fields**: Process ID (unique), Program Counter (next instruction address), Process State, Priority (basis for CPU time), Registers, List of open files, List of open devices.
- **Registers in PCB**: when time slice expires, current register values saved to PCB & process swapped out; when rescheduled, values read back from PCB into CPU registers.

---

## 9. Process States & Queues

- **States**: **New** (about to be created) → **Ready** (in memory, waiting for CPU) → **Running** (CPU allocated) → **Waiting** (waiting for I/O) → **Terminated** (finished, PCB removed).
- Transitions: new→ready (admitted); ready→running (scheduler dispatch); running→ready (interrupt); running→waiting (I/O or event wait); waiting→ready (I/O or event completion); running→terminated (exit).

### Process Queues
- **Job Queue**: processes in **New** state, in **secondary memory**; **Job Scheduler / Long-Term Scheduler (LTS)** picks & loads into memory.
- **Ready Queue**: processes in **Ready** state, in **main memory**; **CPU Scheduler / Short-Term Scheduler (STS)** picks & dispatches to CPU.
- **Waiting Queue**: processes in **Wait** state.
- **Degree of multiprogramming** = no. of processes in memory; controlled by **LTS**.
- **Dispatcher**: gives CPU control to process selected by **STS**.

---

## 10. Swapping | Context Switching | Orphan | Zombie

- **Medium-Term Scheduler (MTS)**: does **swapping** — removes processes from memory (reduce degree of multiprogramming) → later reintroduced, execution continues where left off. Swap-out/swap-in done by MTS.
- **Context switching**: state save of current process + state restore of new process; kernel saves old context in PCB, loads new; **pure overhead** (no useful work during switch); speed depends on machine (memory speed, no. of registers).
- **Orphan process**: parent terminated but process still running; **adopted by init process** (first process of OS).
- **Zombie/Defunct process**: execution completed but still has process-table entry (parent hasn't read child's exit status via `wait()`); removing it = **reaping**.

---

## 11. CPU Scheduling — Basics, FCFS

- **Non-preemptive**: once CPU allocated, process keeps it till termination/wait-state. → starvation (long BT process starves short ones), low CPU utilization.
- **Preemptive**: CPU taken away after time quantum expiry/termination/wait. → less starvation, high CPU utilization.
- **Goals**: max CPU utilization, min turnaround time (TAT), min wait time, min response time, max throughput.
- **Key terms**:
  - **Throughput** = processes completed per unit time.
  - **Arrival Time (AT)**: when process arrives at ready queue.
  - **Burst Time (BT)**: execution time required.
  - **Turnaround Time (TAT)** = CT − AT.
  - **Wait Time (WT)** = TAT − BT.
  - **Response Time**: time between ready-queue entry & first CPU allocation.
  - **Completion Time (CT)**: time till termination.
- **FCFS**: process arriving first in ready queue gets CPU first. → **Convoy Effect**: one long-BT process blocks many short processes needing the resource briefly → poor resource management.

---

## 12. CPU Scheduling Algorithms — SJF | Priority | RR

- **SJF (Non-preemptive)**: least BT dispatched first; needs BT estimation (impossible ideally); suffers convoy effect if first process has large BT; starvation possible. Criteria: **AT + BT**.
- **SJF (Preemptive)** aka **SRTF**: less starvation, no convoy effect; gives lower average WT (short job before long decreases short's WT more than it increases long's WT).
- **Priority Scheduling (Non-preemptive)**: priority assigned at creation; **SJF = special case of priority scheduling** (priority ∝ 1/BT).
- **Priority Scheduling (Preemptive)**: current job preempted if new job has higher priority; may cause **indefinite waiting/starvation** for low priority (true for both preemptive & non-preemptive) → solved by **Ageing** (gradually ↑ priority of long-waiting process, eg +1 every 15 min).
- **Round Robin (RR)**: most popular; like FCFS but preemptive; designed for time-sharing; criteria = **AT + Time Quantum (TQ)** (not BT-dependent); very low starvation (no convoy effect); easy to implement; **small TQ → more context switches (more overhead)**.

---

## 13. MLQ | MLFQ

- **Multi-Level Queue (MLQ)**: ready queue divided into multiple queues by priority; process **permanently** assigned to one queue (inflexible) based on property (memory size, priority, type). Each queue has own algorithm — eg System Process(SP)→RR, Interactive Process(IP)→RR, Batch Process(BP)→FCFS.
  - Priority order: System process (highest) > Interactive (foreground, needs I/O) > Batch (background, silent).
  - Scheduling between sub-queues = **fixed priority preemptive** (foreground preempts background).
  - **Problem**: lower queues scheduled only after higher ones fully complete → starvation for low priority; **convoy effect present**.
- **Multi-Level Feedback Queue (MLFQ)**: multiple sub-queues; processes **can move between queues** based on BT behavior — CPU-heavy process moved to lower priority queue (keeps I/O-bound/interactive in higher queue); process waiting too long in lower queue can move up (**ageing** — prevents starvation). Less starvation than MLQ; flexible; configurable.

### Comparison Table (VERY high-yield)
| | FCFS | SJF | PSJF | Priority | P-Priority | RR | MLQ | MLFQ |
|---|---|---|---|---|---|---|---|---|
| Design | Simple | Complex | Complex | Complex | Complex | Simple | Complex | Complex |
| Preemption | No | No | Yes | No | Yes | Yes | Yes | Yes |
| Convoy effect | Yes | Yes | No | Yes | Yes | No | Yes | Yes |
| Overhead | No | No | Yes | No | Yes | Yes | Yes | Yes |

---

## 14. Concurrency & Multithreading Details

- **Concurrency**: execution of multiple instruction sequences at the same time (multiple threads running in parallel).
- **TCB (Thread Control Block)**: like PCB, for thread state storage during context switching.
- **Single CPU + multithreading = NO gain** (threads still context switch on that one CPU).
- **Benefits of multithreading**: responsiveness; efficient resource sharing; **economy** (cheaper to create/switch threads than processes — process creation needs costly memory/resource allocation); better utilization of multiprocessor architecture.

---

## 15. Critical Section & Race Conditions

- **Critical Section**: code segment where processes/threads access shared resources (variables, files) & write to them.
- **Race Condition**: ≥2 threads access & try to change shared data simultaneously; result depends on scheduling order (unpredictable) — both threads "racing" to access/change data.
- **Solutions to race condition**: atomic operations (executed in 1 CPU cycle), Mutual Exclusion (locks), Semaphores.
- **Simple flag variable does NOT solve** race condition.
- **Peterson's Solution**: avoids race condition but works for **only 2 processes/threads**.
- **Mutex/Locks**: implement mutual exclusion (1 thread/process accesses CS at a time). Disadvantages: **contention** (busy waiting; if lock-holder dies → others wait infinitely), **deadlocks**, debugging difficulty, starvation of high-priority threads.

### Conditional Variable vs Semaphore
- **Conditional Variable**: synchronization primitive; thread waits for a condition; **works with a lock**; thread can wait only after acquiring lock — on wait, releases lock, waits for notify, then reacquires lock. Used to **avoid busy waiting**. **No contention** here.
- **Semaphore**: integer = number of resources available; multiple threads can execute CS concurrently (up to resource count).
  - **Binary semaphore** (0/1) = aka **mutex lock**.
  - **Counting semaphore**: unrestricted range; controls access to finite-instance resources.
  - To avoid busy waiting: `wait()` blocks process into a waiting queue (state→Waiting) instead of spinning; `signal()`/wakeup() moves it back to Ready queue.

---

## 16. Dining Philosophers Problem

- 5 philosophers, 2 states: **Thinking**, **Eating**; circular table, 5 forks (1 between each pair).
- Eating: needs both adjacent forks (left+right), picks one at a time; can't pick a taken fork; eats without releasing once both held.
- **Solution**: each fork = binary semaphore; `wait()` to acquire, `signal()` to release. `Semaphore fork[5]{1};`
- **Problem**: semaphore solution alone can still **Deadlock** — if all 5 pick up left fork simultaneously, all semaphores = 0, everyone waits forever for right fork.
- **Deadlock avoidance methods**:
  a. Allow max **4 philosophers** to sit simultaneously.
  b. Pick up fork only if **both** available, and do so **atomically** (in critical section).
  c. **Odd-even rule**: odd philosopher picks left-then-right fork; even philosopher picks right-then-left.
- **Conclusion**: semaphores alone insufficient — need enhancement rules for deadlock-free solution.

---

## 17. Deadlock — Part 1 (Conditions & Prevention)

- **Deadlock (DL)**: processes waiting on a resource that will never be free (also held by a waiting process) — indefinite wait.
- DL = bug in process/thread synchronization; processes never finish; resources tied up.
- Resource utilization: **Request → Use → Release**.

### 4 Necessary Conditions (must hold SIMULTANEOUSLY) — MUST MEMORIZE
1. **Mutual Exclusion**: only 1 process uses resource at a time; others must wait.
2. **Hold & Wait**: process holds ≥1 resource while waiting to acquire more (held by others).
3. **No Preemption**: resource can only be released voluntarily by holding process.
4. **Circular Wait**: set {P0,P1,...,Pn} where P0 waits for resource held by P1, P1 for P2's, ... forming a cycle.

### Methods to handle Deadlock
a. **Prevent/Avoid** — ensure system never enters DL state.
b. **Detect & Recover** — allow DL, then detect & recover.
c. **Ignore** (Ostrich algorithm) — aka **Deadlock ignorance**.

### Deadlock Prevention (deny 1 necessary condition)
- **Mutual Exclusion**: use locks only for **non-sharable** resources (sharable eg read-only files can be accessed by multiple); can't fully deny this condition (some resources intrinsically non-sharable).
- **Hold & Wait**: Protocol A — request & get ALL resources before execution starts. Protocol B — request resources only when holding none (release all before requesting more).
- **No Preemption**: if process holding resources requests one that can't be allocated, **preempt all its current resources**; it restarts only after regaining old + new resource (may cause **Live Lock**). Alternative: check if wanted resource is held by another waiting process — if so, preempt from that process.
- **Circular Wait**: impose **proper ordering** of resource allocation (eg both P1,P2 must lock R1 before R2 — whoever locks R1 first gets R2).

---

## 18. Deadlock — Part 2 (Avoidance, Detection, Recovery)

- **Deadlock Avoidance**: kernel given advance info on resources a process will use in its lifetime; decides per-request whether process should wait, considering currently available/allocated resources + future requests/releases.
- **Safe State**: system can allocate resources to each process (up to max) in **some order** & still avoid DL — i.e., a **safe sequence** exists.
- **Unsafe State**: OS cannot guarantee avoiding DL; NOT necessarily a deadlock itself, but may lead to one.
- Key rule: approve a resource request **only if** resulting state is **safe**.
- **Banker's Algorithm**: scheduling algorithm to find safe state / avoid deadlock; on request, checks if allocating leaves system safe — if yes, allocate; if no, process waits.

### Deadlock Detection
- **Single instance per resource type** → **Wait-for graph** method: DL exists **iff there's a cycle** in wait-for graph; system periodically checks for cycles.
- **Multiple instances per resource type** → **Banker's Algorithm** (detection variant).

### Recovery from Deadlock
a. **Process termination**: abort all DL processes, OR abort one at a time until cycle breaks.
b. **Resource preemption**: successively preempt resources from processes, give to others, until cycle breaks.

---

## 19. Memory Management — Address Spaces & Contiguous Allocation

- **Logical (Virtual) Address**: generated by CPU; address of instruction/data used by process; user **can** access; range 0 to max; doesn't exist physically.
- **Physical Address**: loaded into memory-address register; actual location in main memory; user **cannot** access directly (only indirectly); range (R+0) to (R+max) for base R.
- **MMU (Memory Management Unit)**: hardware device that maps logical→physical address at runtime; adds **relocation register** value to logical address.
- **Relocation register** = base address (smallest physical addr); **Limit register** = range of logical addresses. Each logical address must be < limit register (checked before mapping).
- On context switch, dispatcher loads correct relocation & limit register values → protects OS & other processes' memory.
- Illegal access attempt by user program → **trap** to OS, treated as fatal error.

### Contiguous Memory Allocation
- Each process in a **single contiguous block**.
- **Fixed Partitioning**: memory divided into equal/different-sized partitions (declared beforehand).
  - Limitations: **Internal fragmentation** (process < partition size → wasted space); **External fragmentation** (total free space across partitions unusable if non-contiguous); process size limited to largest partition size; **low degree of multiprogramming** (fixed partition sizes).
- **Dynamic Partitioning**: partition size declared at process-load time (= process size).
  - Advantages over fixed: no internal fragmentation, no process size limit, better multiprogramming degree.
  - Limitation: **External fragmentation** still occurs.

---

## 20. Free Space Management

- **Compaction/Defragmentation**: minimizes external fragmentation by making all free partitions contiguous (merging loaded partitions together) → allows storing bigger processes. Downside: ↓system efficiency (moving many free spaces to one place is costly).
- **Free space representation**: **Linked list (free list)** of holes.
- **Allocation algorithms** for a request of size n:
  - **First Fit**: first big-enough hole; simple, fast, less time complexity.
  - **Next Fit**: like First Fit but always starts search from **last allocated hole**.
  - **Best Fit**: **smallest** big-enough hole; less internal fragmentation but may create many small holes → major external fragmentation; **slow** (iterates whole list).
  - **Worst Fit**: **largest** available hole; slow (iterates whole list); leaves larger holes for future processes.

---

## 21. Paging (Non-Contiguous Allocation)

- **Paging**: permits process's physical address space to be **non-contiguous**; avoids external fragmentation & need for compaction.
- Physical memory divided into fixed blocks = **Frames**; logical memory divided into same-size blocks = **Pages** (page size = frame size).
- **Page size** determined by processor architecture; traditionally uniform, eg **4096 bytes**; modern CPUs may support multiple page sizes.
- **Page Table**: data structure mapping page→frame; stores **base address of each page** in physical memory.
- Logical address = **Page number (p) + Page offset (d)**; p indexes page table to get frame's base address.
- Page table stored in main memory at process creation; base address stored in **PCB**.
- **PTBR (Page Table Base Register)**: points to current page table; only this register changes on context switch.
- **Why paging is slow**: too many memory references needed to get physical address.
- **TLB (Translation Look-aside Buffer)**: hardware cache (high-speed) to speed up paging; has key-value pairs (page#→frame#).
  - **TLB hit**: mapping found in TLB directly (fast).
  - **TLB miss**: must reference actual page table; then entry added to TLB for future.
  - **ASID (Address Space Identifier)**: stored per TLB entry; uniquely identifies process; provides address-space protection; allows TLB entries for multiple processes simultaneously — if current process's ASID ≠ entry's ASID → treated as TLB miss.

---

## 22. Segmentation (Non-Contiguous Allocation)

- **Segmentation**: memory management technique supporting the **user's view** of memory (unlike paging which is OS-centric).
- Logical address space = collection of **segments** based on user view; each segment defined by **<segment-number, offset> = {s, d}**.
- Process divided into **variable-sized segments** (eg main function = 1 segment, library functions = another).
- **Paging vs Segmentation**: paging may split a single function across multiple pages (loaded/not loaded independently) → reduces efficiency; segmentation keeps related functions together in one segment.
- **Segmentation hardware**: uses **Segment Table** with **limit** & **base** per segment; logical address (s,d) checked: if d < limit → physical addr = base+d, else trap (addressing error).

### Advantages / Disadvantages
| Advantages | Disadvantages |
|---|---|
| No internal fragmentation | External fragmentation |
| Contiguous within a segment → efficient | Variable segment sizes bad for swapping time |
| Segment table smaller than page table | |
| More efficient (compiler groups same-type functions in one segment) | |

- **Modern systems**: hybrid of segmentation + paging.

---

## 23. Virtual Memory & Demand Paging

- **Virtual Memory**: allows executing processes not completely in memory; illusion of large main memory by treating part of secondary memory as main memory (**swap space**).
- **Advantage**: programs can be **larger than physical memory**; more programs run simultaneously → ↑CPU utilization & throughput; benefits both system and user.
- **Demand Paging**: popular VM management method; least-used pages stored in secondary memory; page copied to main memory only **on demand** (or **page fault**).
- **Lazy Swapper**: never swaps a page into memory unless needed. (Technically called **Pager**, not swapper, since it deals with individual pages not entire processes.)
- **Valid-Invalid bit** (in page table):
  - **1** = page is legal **and** in memory.
  - **0** = page either invalid (not in process's logical address space) OR valid but currently on disk.
- If process never accesses an invalid-bit page → executes fine without that page ever entering memory.
- **Page Fault**: accessing a page marked invalid → causes trap to OS.

### Page Fault Handling Procedure
1. Check internal table (in PCB) — was reference valid or invalid?
2. If invalid → throw exception. If valid → pager swaps in the page.
3. Find a free frame (from free-frame list).
4. Schedule disk operation to read desired page into the newly allocated frame.
5. On completion, update page table — page now marked in memory.
6. Restart the interrupted instruction — process continues as if page was always in memory.

- **Pure Demand Paging**: can start executing process with **zero pages** in memory — first instruction itself faults, page brought in. Never brings a page in until required.
- **Locality of reference**: exploited to get reasonable demand paging performance.

### Advantages / Disadvantages of Virtual Memory
| Advantages | Disadvantages |
|---|---|
| ↑ Degree of multiprogramming | System can become slower (swapping takes time) |
| Run large apps with less physical memory | **Thrashing** may occur |

---

## 24. Page Replacement Algorithms

- Needed when: page fault occurs, all frames busy/high utilization → must replace an existing page. **Aim: minimum page faults.**

| Algorithm | Key points |
|---|---|
| **FIFO** | Replaces **oldest** page in memory; easy to implement; performance not always good (may evict either a good candidate or a heavily-reused page); suffers **Belady's Anomaly**. |
| **Belady's Anomaly** | For LRU & Optimal, ↑frames → ↓page faults (expected). But **FIFO** can show ↑page faults with ↑frames — strange/anomalous behavior only seen in FIFO (in some cases). |
| **Optimal** | Replace page **never referenced again** (if exists) OR page **referenced farthest in future**; gives **lowest page fault rate of any algorithm**; **impossible to implement** in practice — needs future knowledge of reference string (similar issue to SJF scheduling). |
| **LRU (Least Recently Used)** | Replace page unused for **longest period** (uses recent past to approximate future). Implementation: (1) **Counters** — time field per page table entry, replace smallest time; (2) **Stack** — page number pushed to top on reference; MRU always on top, LRU at bottom; doubly linked list used since entries may be removed from middle. |
| **Counting-based** | Keep reference counter per page. **LFU (Least Frequently Used)**: replace smallest count (assumes actively-used pages have large count). **MFU (Most Frequently Used)**: replace largest count (argues smallest-count page was just brought in, not yet used). Neither LFU nor MFU is common in practice. |

---

## 25. Thrashing

- **Thrashing**: process lacks frames needed for its active pages → repeatedly page-faults, must evict pages still in active use → faults again immediately → high paging activity.
- System is **thrashing** when it **spends more time servicing page faults than executing processes**.
- CPU utilization vs degree of multiprogramming graph: rises then **sharply drops** after a point — that drop-off zone = thrashing.

### Techniques to Handle Thrashing
1. **Working Set Model**: based on **Locality Model**. If enough frames allocated to cover process's current locality → faults only when moving to a new locality. If allocated frames < current locality size → **process bound to thrash**.
2. **Page Fault Frequency (PFF)**: thrashing shows high page-fault rate; establish upper & lower bounds on desired PF rate:
   - PF-rate **> upper limit** → allocate **another frame** to process.
   - PF-rate **< lower limit** → **remove a frame** from process.
   - Controlling PF-rate this way **prevents thrashing**.

---

## ⚡ Quick-Fire Facts (Rapid Recall)

- OS = resource manager + abstraction layer.
- Kernel = first thing loaded at boot; heart of OS.
- Only system calls take a process from User Mode → Kernel Mode.
- Program (disk) → Process (RAM) → Thread (lightweight, within process).
- Thread context switch: fast, no address-space switch, cache preserved.
- Process context switch: slow, address-space switch, cache flushed.
- LTS (Job Scheduler) — controls degree of multiprogramming, works from secondary memory (Job Queue).
- STS (CPU Scheduler) — picks from Ready Queue (main memory), works with Dispatcher.
- MTS — does swapping.
- Convoy effect present in: FCFS, SJF (non-preemptive), Priority (non-preemptive), MLQ, MLFQ.
- Convoy effect absent in: PSJF, RR.
- Starvation solution (priority scheduling) = Ageing.
- 4 deadlock conditions: Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait — ALL must hold together.
- Deadlock avoidance = Banker's Algorithm; needs "safe state"/"safe sequence".
- Wait-for graph → single-instance resource deadlock detection (cycle = deadlock).
- Paging → OS-centric, fixed-size pages/frames, avoids external fragmentation, but has internal fragmentation potential (last page).
- Segmentation → User-centric, variable-size, avoids internal fragmentation, but external fragmentation exists.
- TLB = cache for page table entries; ASID differentiates entries per process.
- Belady's Anomaly = unique to FIFO (more frames → more faults, sometimes).
- Optimal page replacement = theoretical best, needs future knowledge (impossible practically).
- Thrashing = more time faulting than executing; handled via Working Set Model or Page Fault Frequency method.
- Register > Cache > RAM (Main memory) > Secondary storage — in both speed & cost (descending), and ascending in size/volatility-non-volatility.
