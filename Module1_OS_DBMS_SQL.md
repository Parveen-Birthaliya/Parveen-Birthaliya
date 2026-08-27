# MODULE 1 — OS + DBMS + SQL | Final IBPS SO IT Revision
*Built from your 3 mocks (152 Qs). Priority = your errors + IBPS depth potential.*

---

# PART A — OPERATING SYSTEM

## A1. PROCESS STATES & TRANSITIONS — 🅰️ MUST KNOW
**CORE IDEA:** A process moves New→Ready→Running→(Waiting)→Terminated. CPU is given only from Ready.

**PROCESS STATE FLOWCHART**
```
        admit           dispatch (scheduler picks + dispatcher loads)
 NEW ─────────► READY ─────────────► RUNNING ─────────► TERMINATED
                  ▲                     │
                  │  I/O or event       │  I/O request /
                  │  completion         │  event wait
                  │                     ▼
                  └────────────── WAITING/BLOCKED
        (timer expiry / higher-priority process preempts)
 RUNNING ───────────────────────────► READY
```

**MUST REMEMBER**
- Running → Ready: only via **preemption** (timer interrupt / higher-priority arrival) — CPU is *taken away*, process didn't ask.
- Running → Waiting: process **itself** requests I/O or an event — voluntary.
- Waiting → Ready (never Waiting → Running directly): I/O/event completes, process re-joins the ready queue and must be scheduled again.
- Ready → Running: only the **scheduler + dispatcher** can do this.

**EXAM TRAP**
IBPS loves writing "Running → Waiting → Running" as a distractor. **There is no direct Waiting→Running edge.** It must pass through Ready.

**CONFUSION PAIR**

| Transition | Trigger | Voluntary? |
|---|---|---|
| Running → Waiting | I/O request / event wait | Yes (process asks) |
| Running → Ready | Timer expiry / preemption | No (forced) |
| Waiting → Ready | I/O/event completion | N/A (system-driven) |
| Ready → Running | Scheduler dispatch | N/A |

**DEEPER IBPS LEVEL:** A 5-state model may add **Suspended (Swapped)** states (Ready-Suspend, Blocked-Suspend) — memory-related, used by medium-term scheduler. Don't confuse "Suspended" with "Waiting" — Suspended = swapped out of main memory to disk.

**EXAMPLE (scenario):** A process reading a file: Running → (issues read()) → Waiting → (disk controller signals completion) → Ready → (scheduler picks it up later) → Running.

**MEMORY TRICK:** "You **choose** to wait, but you're **forced** to ready." (Waiting = self-initiated; Ready via preemption = system-initiated.)

**PYQ/MOCK CONNECTION:** Mock-1 Q1 — you answered "Running→Ready→Suspended→Waiting" ❌. Correct: **Running→Waiting→Ready→Running**.

**MCQs**
1. A process executing on CPU issues a `read()` system call. What is the immediate next state?
   A. Ready B. Waiting C. Terminated D. New E. Suspended
   **Ans: B** — self-initiated I/O request → Waiting (never Ready directly).
2. Which transition is caused *only* by an external scheduling decision, not the process's own action?
   A. Running→Waiting B. Waiting→Ready C. Running→Ready D. New→Ready
   **Ans: C** — preemption is forced onto the process.
3. After I/O completes, a process goes directly to:
   A. Running B. Ready C. Terminated D. New
   **Ans: B** — must re-compete for CPU via Ready queue.

---

## A2. PCB (Process Control Block) — 🅱️ HIGH PRIORITY
**CORE IDEA:** OS's per-process data structure — the "identity card" of a process, used during context switch.

**MUST REMEMBER**
- Contains: Process ID, State, Program Counter, CPU registers, scheduling info (priority), memory management info (page tables), accounting info, I/O status (open files).
- One PCB per process; stored in kernel space.

**EXAM TRAP:** IBPS may ask "what is saved/restored during a context switch?" → Answer: **PCB contents** (PC + registers + state), not the entire program.

**MEMORY TRICK:** PCB = process's "passport" — checked/stamped every time it crosses a state border.

---

## A3. CONTEXT SWITCHING — 🅱️ HIGH PRIORITY
**CORE IDEA:** Saving the PCB of the currently running process and loading the PCB of the next scheduled process — pure overhead, no useful work done during the switch itself.

**MUST REMEMBER**
- Pure overhead — CPU does zero useful computation while switching.
- Happens on: interrupt, timer expiry, I/O wait, priority preemption.
- Frequency ∝ overhead: too many switches (e.g., very small RR time quantum) → thrashing-like inefficiency.

**EXAM TRAP:** A tiny Round Robin time quantum is often shown as "good for responsiveness" — true, but IBPS may trap you into ignoring that it **increases context-switch overhead**, hurting throughput.

---

## A4. SCHEDULERS: LONG-TERM vs SHORT-TERM vs MEDIUM-TERM — 🅰️ MUST KNOW

| Scheduler | Also called | Selects from → to | Frequency | Controls |
|---|---|---|---|---|
| **Long-term** | Job scheduler | New → Ready (admits jobs) | Slowest (seconds/minutes) | Degree of multiprogramming |
| **Short-term** | CPU scheduler | Ready → Running | Fastest (milliseconds) | Which process gets CPU next |
| **Medium-term** | — | Swaps process out/in (Ready/Waiting ⇄ Suspended) | Moderate | Reduces multiprogramming, handles memory pressure |

**EXAM TRAP:** Question may describe *swapping* and expect "Medium-term scheduler," but options include "Long-term" as bait — Long-term is about **admission**, not swapping already-admitted processes.

**MEMORY TRICK:** Long = **L**ets in (admits). Short = **S**elects next to run. Medium = **M**oves to disk (swap).

---

## A5. SCHEDULER vs DISPATCHER — 🅰️ MUST KNOW (explicit table requested)

| Aspect | Scheduler (Short-term) | Dispatcher |
|---|---|---|
| Job | **Decides** which process runs next | **Performs** the actual switch |
| Actions | Selection based on algorithm (FCFS/SJF/RR...) | Context switch, mode switch (kernel→user), jump to program's location |
| Speed | Can be relatively slower (decision logic) | Must be extremely fast — this delay is called **Dispatch Latency** |
| Output | A decision (which PID) | Actual CPU handover |

**EXAM TRAP:** "Dispatcher decides priority order" — **false**. Dispatcher only *executes* what the scheduler already decided.

**MEMORY TRICK:** Scheduler = **brain** (decides), Dispatcher = **hands** (executes).

---

## A6. TIMER INTERRUPT & PREEMPTION — 🅱️ HIGH PRIORITY
**CORE IDEA:** Hardware timer generates periodic interrupts enabling preemptive scheduling (else a process could hog CPU forever).

**MUST REMEMBER**
- No timer interrupt → cooperative/non-preemptive scheduling only.
- RR fundamentally depends on timer interrupts for time-quantum enforcement.

---

## A7–A11. CPU SCHEDULING ALGORITHMS — 🅰️ MUST KNOW

**CORE IDEA (all algorithms):** Decide *order* processes get CPU from the Ready queue to optimize WT/TAT/RT/throughput.

### Quick Reference Table

| Algorithm | Preemptive? | Selection basis | Weakness |
|---|---|---|---|
| **FCFS** | No | Arrival order | Convoy effect (short jobs stuck behind long ones) |
| **SJF (Non-preemptive)** | No | Smallest burst time, runs to completion once started | Starvation of long jobs; needs burst-time prediction |
| **SRTF** | Yes | Smallest *remaining* burst time; preempts on new shorter arrival | High context-switch overhead |
| **Priority** | Either | Highest priority value | Starvation of low priority → fixed by **Aging** |
| **Round Robin** | Yes | FCFS + fixed time quantum | Too small q → overhead; too large q → behaves like FCFS |

**EXAM TRAP (your actual mock error):** A question describing "select smallest burst time... let it complete before selecting another" = **Non-preemptive SJF**, NOT Priority. Read carefully — the phrase "before selecting another" = **no preemption**, which rules out SRTF and Preemptive Priority immediately.

### FORMULAS
```
Turnaround Time (TAT) = Completion Time (CT) − Arrival Time (AT)
Waiting Time (WT)     = Turnaround Time (TAT) − Burst Time (BT)
Response Time (RT)    = Time of FIRST CPU allocation − Arrival Time (AT)
```
- FCFS/SJF/Priority (non-preemptive): RT = WT for the first process's own metrics... but in general **RT ≠ WT** whenever a process starts, gets preempted, then resumes later. In non-preemptive algorithms, RT = time until *first and only* CPU burst starts = same moment WT ends → **RT and start of execution coincide.**

### WORKED EXAMPLE 1 — FCFS
Processes (AT, BT): P1(0,4), P2(1,3), P3(2,1)
```
Gantt: | P1(0-4) | P2(4-7) | P3(7-8) |
CT: P1=4, P2=7, P3=8
TAT: P1=4-0=4, P2=7-1=6, P3=8-2=6
WT:  P1=4-4=0, P2=6-3=3, P3=6-1=5
Avg WT = (0+3+5)/3 = 2.67
```

### WORKED EXAMPLE 2 — Non-preemptive SJF
Processes (AT, BT): P1(0,7), P2(1,4), P3(2,1), P4(3,4)
```
At t=0 only P1 available → run P1 (0-7) [can't preempt even though shorter jobs arrive later]
At t=7, Ready={P2,P3,P4} → shortest BT = P3(1) → run P3(7-8)
Next shortest = P2(4) or P4(4), tie → FCFS tiebreak → P2(8-12)
Then P4(12-16)
CT: P1=7, P3=8, P2=12, P4=16
TAT: P1=7, P3=6, P2=11, P4=13
WT:  P1=0, P3=5, P2=7, P4=9
```

### WORKED EXAMPLE 3 — Round Robin (Quantum=2)
Processes (AT,BT): P1(0,5), P2(1,3), P3(2,1)
```
Ready order handling with arrivals interleaved:
t0-2: P1 runs (rem P1=3), queue after: P2,P3,P1
t2-4: P2 runs (rem P2=1), queue: P3,P1,P2
t4-5: P3 runs (rem P3=0 → done at t5), queue: P1,P2
t5-7: P1 runs (rem P1=1), queue: P2,P1
t7-8: P2 runs (rem P2=0 → done at t8), queue: P1
t8-9: P1 runs (rem P1=0 → done at t9)
CT: P3=5, P2=8, P1=9
TAT: P3=5-2=3, P2=8-1=7, P1=9-0=9
WT: P3=3-1=2, P2=7-3=4, P1=9-5=4
```
**EXAM TRAP:** RR numericals are the #1 place students miscompute — always re-insert the arriving process into the queue **after** the currently running one is put back (if not finished), and **before** processes that arrive during the current process's execution window is a common ordering trap. Practice the "queue update" step carefully.

**MEMORY TRICK:** TAT = "Total time in system." WT = "TAT minus the time you *actually* got served."

**PYQ/MOCK CONNECTION:** Mock-2 Q42 — you answered "Preemptive Priority" ❌ for a description that was actually Non-preemptive SJF. Trap keyword: "allows selected process to complete before selecting another" = non-preemptive.

**MCQs**
1. Which algorithm suffers most from the "convoy effect"?
   A. SRTF B. RR C. FCFS D. Priority
   **Ans: C**
2. In SRTF, what causes preemption of the currently running process?
   A. Timer quantum expiry B. Arrival of a process with smaller remaining burst time C. Priority aging D. I/O completion of another process
   **Ans: B**
3. Starvation of long processes is a classic weakness of:
   A. FCFS B. Round Robin C. Non-preemptive SJF D. All of the above
   **Ans: C**

---

## A12–A14. WT, TAT, RT — 🅱️ HIGH PRIORITY (see formulas above)
**EXAM TRAP:** IBPS may swap the formula: give you TAT and BT, ask for WT (WT = TAT − BT) or ask for **Response Time** in a preemptive scenario where RT ≠ WT (RT only counts time to *first* CPU allocation, even if process gets preempted afterward and resumes later).

---

## A15. STARVATION & AGING — 🅱️ HIGH PRIORITY
**CORE IDEA:** Starvation = indefinite postponement of low-priority process because higher-priority ones keep arriving. Aging = fix by gradually **increasing** the priority of a waiting process over time.

**MUST REMEMBER**
- Occurs in: Priority scheduling, SJF (long jobs), NOT typically in RR (RR is fair by design).
- Aging guarantees eventual execution — priority increases with wait time until it becomes highest.

**PYQ/MOCK CONNECTION:** Mock-2 Q43 — you got this correct (Aging). Keep it as a "safe" fact, but expect scenario-wrapped versions.

---

## A16–A18. DEADLOCK — 🅰️ MUST KNOW (not directly tested yet, but IBPS staple — high probability)

**CORE IDEA:** A set of processes are all waiting for resources held by each other — none can proceed.

**FOUR NECESSARY CONDITIONS (Coffman conditions) — must ALL hold simultaneously:**
1. **Mutual Exclusion** — resource can't be shared, only one process at a time.
2. **Hold and Wait** — process holding ≥1 resource is waiting for more.
3. **No Preemption** — resource can't be forcibly taken; only voluntarily released.
4. **Circular Wait** — a closed chain of processes, each waiting for a resource held by the next.

**EXAM TRAP:** Breaking **ANY ONE** condition prevents deadlock — IBPS may ask "which condition is broken by X technique." E.g., **Banker's Algorithm** = avoidance (checks safe state), doesn't strictly break any one condition permanently but avoids unsafe allocation.

**DEADLOCK vs STARVATION — CONFUSION PAIR**

| Aspect | Deadlock | Starvation |
|---|---|---|
| Processes involved | ≥2, circularly blocked | Can be a single process, indefinitely delayed |
| Will it ever resolve on its own? | No — needs OS intervention | Possibly, if scheduling changes (e.g., no more high-priority arrivals) |
| Fix | Detection+Recovery / Prevention / Avoidance (Banker's) | Aging |
| State | All involved processes are stuck (Waiting) | Process is Ready but never selected |

**MEMORY TRICK:** Deadlock = circular traffic jam (nobody moves). Starvation = one car always losing at the signal (unfair, not stuck-stuck).

**MCQs**
1. Which condition, if removed, means a resource CAN be forcibly taken from a process?
   A. Mutual Exclusion B. Hold and Wait C. No Preemption D. Circular Wait
   **Ans: C**
2. Banker's Algorithm is an example of deadlock:
   A. Prevention B. Avoidance C. Detection D. Recovery
   **Ans: B**
3. Which is true of starvation but NOT necessarily deadlock?
   A. Involves circular waiting B. Can involve just one unlucky process C. Requires ≥2 processes D. Resources never get released
   **Ans: B**

---

## A19–A24. PAGING, VIRTUAL MEMORY, SEGMENTATION — 🅰️ MUST KNOW

**CORE IDEA:** Paging = divide logical memory into fixed-size **pages** and physical memory into equal-size **frames**; non-contiguous allocation eliminates external fragmentation (but causes internal fragmentation).

**PAGE vs FRAME vs PAGE TABLE — comparison**

| Term | Belongs to | Size | Purpose |
|---|---|---|---|
| **Page** | Logical/Virtual memory (process address space) | Fixed size | Chunk of a process |
| **Frame** | Physical memory (RAM) | Same fixed size as page | Physical slot that holds a page |
| **Page Table** | Per-process, kernel-maintained | Rows = pages | Maps page number → frame number |

**Address breakdown:** Logical Address = **Page Number** + **Offset**.
```
Logical Address → [ Page Number | Offset ] 
Page Number → looked up in Page Table → Frame Number
Physical Address = [ Frame Number | Offset ]   (offset unchanged)
```

**MUST REMEMBER**
- Paging → **Internal fragmentation** (last page rarely fully used).
- Variable partitioning (no paging) → **External fragmentation**.
- **Page Fault**: referenced page not in main memory → trap → OS loads it from disk.

### PAGE FAULT HANDLING SEQUENCE (exact order — you got this wrong in mock)
```
1. Trap to OS
2. Validate the memory reference (valid page vs illegal access)
3. Locate the required page on secondary storage (disk)
4. Obtain a free frame (or select a victim via page-replacement algorithm)
5. Load the required page into the selected frame (disk I/O)
6. Update the page table (valid bit=1, frame number set)
7. Restart the interrupted instruction
```
**EXAM TRAP:** IBPS may shuffle steps 2/3 or 4/5 — memorize the sequence: **Trap → Validate → Locate → Get Frame → Load → Update Table → Restart.**
**MEMORY TRICK:** "**T-V-L-G-L-U-R**" — Try Very Large Games, Look Up, Retry.

**Virtual Memory:** Illusion of a memory space larger than physical RAM, implemented via demand paging (pages loaded only when referenced).

**Segmentation:** Logical division of a program into variable-sized meaningful units (code, data, stack) — closer to programmer's view, but causes external fragmentation (variable-size blocks).

**Combined Segmentation + Paging (your mock error, Q41):** Program divided into logical **segments** first (programmer view), then each segment is internally divided into fixed-size **pages** for physical allocation. This is neither "pure segmentation" nor "pure paging" nor "fixed partitioning" — it's a **hybrid**, used in x86 architecture.

**FRAGMENTATION — CONFUSION PAIR**

| Type | Occurs in | Cause |
|---|---|---|
| **Internal** | Fixed partitioning, Paging | Allocated block bigger than needed — leftover space wasted *inside* |
| **External** | Variable/dynamic partitioning | Enough total free memory exists, but scattered in small non-contiguous holes |

**PYQ/MOCK CONNECTION:** Mock-2 Q23 (page fault sequence) ❌, Q40 (fragmentation) ✅ but Q41 (segmentation+paging) ❌.

**MCQs**
1. What causes internal fragmentation?
   A. Non-contiguous allocation B. Fixed-size allocation bigger than the process's need C. Too many small holes D. Disk swapping
   **Ans: B**
2. In the page fault sequence, which step happens immediately after locating the page on disk?
   A. Update page table B. Restart instruction C. Obtain a free frame (or select victim) D. Trap to OS
   **Ans: C**
3. A program logically split into Code/Data/Stack, each further split into fixed blocks — this is:
   A. Pure paging B. Pure segmentation C. Fixed partitioning D. Combined segmentation with paging
   **Ans: D**

---

## A25–A26. INTERRUPTS & HARDWARE INTERRUPT SEQUENCE — 🅱️ HIGH PRIORITY (your mock error)

**CORE IDEA:** Interrupt = signal that diverts CPU from normal execution to handle an event.

**MUST REMEMBER**
- **Hardware interrupt (asynchronous):** CPU finishes the **current instruction completely** before servicing it (not mid-instruction).
- **Trap/Exception (synchronous):** handled immediately upon detection (e.g., divide-by-zero, invalid opcode, page fault) since it's caused BY the current instruction.
- Sequence: Fetch → Decode → Execute → **check for interrupt** → if pending, save PC+registers (into PCB) → jump to ISR (Interrupt Service Routine) → after ISR, restore state → resume.

**EXAM TRAP:** "CPU processes IRQ immediately when raised" — **False**, it waits till current instruction finishes. This exact trap caught you in mock-2 Q16.

**CONFUSION PAIR**

| | Hardware Interrupt | Trap/Exception |
|---|---|---|
| Sync/Async | Asynchronous (external device) | Synchronous (caused by current instruction) |
| Timing | Serviced after current instruction completes | Serviced immediately/during instruction |
| Example | Keyboard press, timer | Divide by zero, page fault, illegal opcode |

**MCQs**
1. An I/O device raises an IRQ mid-instruction. When does the CPU service it?
   A. Immediately B. After completing the current instruction C. Never, it's ignored D. Before the current instruction starts
   **Ans: B**
2. A page fault is classified as:
   A. Hardware interrupt B. Synchronous trap/exception C. I/O interrupt D. Software crash only
   **Ans: B**

---

## OS — CONSOLIDATED CONFUSION PAIRS TABLE

| Pair | Key distinguishing test |
|---|---|
| Scheduler vs Dispatcher | Decides vs Executes |
| Long-term vs Short-term vs Medium-term | Admits vs Selects-to-run vs Swaps |
| SJF vs SRTF | Non-preemptive vs Preemptive on shorter-arrival |
| Priority vs SJF | Priority value vs Burst time as criterion |
| Deadlock vs Starvation | Circular block (≥2) vs Indefinite unfair delay (≥1) |
| Internal vs External fragmentation | Wasted space inside block vs scattered free holes |
| Paging vs Segmentation | Fixed-size, physical view vs Variable-size, logical/programmer view |
| Hardware Interrupt vs Trap | Waits for instruction to finish vs Immediate (caused by instruction itself) |
| WT vs TAT vs RT | Wait-only vs Total system time vs Time to FIRST CPU burst |

---

## PART A — OS: 10 THINGS I ABSOLUTELY CANNOT FORGET
1. Waiting → Ready → Running (never Waiting → Running directly).
2. Running → Ready = forced/preemption; Running → Waiting = voluntary.
3. Scheduler decides, Dispatcher executes (dispatch latency = dispatcher's delay).
4. Long-term=admits, Short-term=picks next CPU job, Medium-term=swaps.
5. "Runs to completion once started, picks smallest burst" = Non-preemptive SJF (not Priority).
6. Page fault order: Trap→Validate→Locate→Get Frame→Load→Update Table→Restart.
7. Fixed-size allocation (paging) → internal fragmentation; variable-size → external fragmentation.
8. Segments split into pages = Combined Segmentation+Paging (x86-style hybrid).
9. Hardware interrupts wait for current instruction to finish; traps/exceptions are immediate.
10. Deadlock needs ALL 4 Coffman conditions; breaking any ONE prevents it. Aging fixes starvation, not deadlock.

## PART A — OS: 5 MOST DANGEROUS TRAPS
1. Writing "Running→Waiting→Running" — missing the mandatory Ready stop.
2. Confusing SJF (burst-time based) with Priority scheduling (priority-value based) when the question describes burst-time selection.
3. Assuming IRQ is handled the instant it's raised.
4. Mixing up internal (fixed-size waste) vs external (scattered holes) fragmentation.
5. Treating "swap out to disk" as Long-term scheduler's job (it's Medium-term).

## PART A — OS: 60-SECOND RECALL
New→Ready→Running→(Waiting⇄Ready loop)→Terminated. Scheduler decides/Dispatcher executes. 3 schedulers: Long(admit)/Short(pick)/Medium(swap). FCFS(simple,convoy)/SJF(non-preemptive,starves long jobs)/SRTF(preemptive SJF)/Priority(+Aging fixes starvation)/RR(preemptive, quantum). TAT=CT−AT, WT=TAT−BT, RT=first burst start−AT. Deadlock=4 Coffman conditions all true+circular wait; break any one to prevent. Paging=fixed pages/frames, page table maps them, internal fragmentation. Segmentation=variable logical units, external fragmentation. Page fault sequence: Trap-Validate-Locate-Frame-Load-Update-Restart. Hardware interrupts wait for instruction completion; traps are immediate.

## PART A — OS: 10-QUESTION MINI TEST
1. Which scheduler controls the degree of multiprogramming? *(Long-term)*
2. What does the Dispatcher do that the Scheduler doesn't? *(Performs actual context switch/CPU handover)*
3. In SRTF, what triggers preemption? *(Arrival of process with smaller remaining burst)*
4. Formula for Waiting Time? *(TAT − BT)*
5. What fixes starvation in priority scheduling? *(Aging)*
6. Name all 4 necessary conditions for deadlock. *(Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait)*
7. Fixed-size allocation causes which fragmentation? *(Internal)*
8. First step when a page fault occurs? *(Trap to OS)*
9. Logical address in paging = ? *(Page Number + Offset)*
10. Is a divide-by-zero error a hardware interrupt or a trap? *(Trap/exception — synchronous)*

---
---

# PART B — DBMS

## B1. SUPER KEY vs CANDIDATE KEY vs PRIMARY KEY — 🅰️ MUST KNOW

**CORE IDEA:** Super key = any attribute set that uniquely identifies a tuple (may have extra/redundant attributes). Candidate key = **minimal** super key (no redundant attribute can be removed). Primary key = the one candidate key chosen by the designer.

**MUST REMEMBER**
- Every Candidate Key is a Super Key, but not vice versa.
- A relation can have multiple Candidate Keys but only ONE Primary Key.
- Attributes in candidate keys but not chosen as primary = **Alternate Keys**.
- Composite Key = a key made of 2+ attributes together (could be a candidate/primary key).

**EXAM TRAP:** IBPS gives a big attribute set (e.g., {A,B,C,D}) that is a super key, then asks "is this a candidate key?" — check if you can **remove any attribute and still uniquely identify** the tuple. If yes → NOT minimal → NOT a candidate key, just a super key.

**CONFUSION PAIR**

| | Super Key | Candidate Key |
|---|---|---|
| Uniqueness | Yes | Yes |
| Minimality | Not required (can have extra attrs) | Required (no attribute can be dropped) |
| Count per relation | Many | Fewer (subset of super keys) |
| Relationship | Candidate Key ⊂ Super Key (every CK is SK) | — |

**MEMORY TRICK:** "All candidates are super, but not all supers make the cut (aren't minimal)."

---

## B2. ATTRIBUTE CLOSURE & CANDIDATE KEY IDENTIFICATION — 🅰️ MUST KNOW (your biggest DBMS miss)

**CORE IDEA:** Closure of attribute set X (written X⁺) = all attributes functionally determined by X, computed by repeatedly applying FDs. Used to test candidate keys: if X⁺ = all attributes of R, X is a super key.

**ALGORITHM**
```
Start: X⁺ = X
Repeat: for each FD (α→β) in F, if α ⊆ X⁺, add β to X⁺
Stop when no more attributes can be added.
If X⁺ = all attributes of R → X is a Super Key.
X is a Candidate Key if X⁺ = R AND no proper subset of X has this property.
```

**WORKED EXAMPLE (your mock Q44 — you got this wrong):**
R(A,B,C,D,E), F = {A→BC, CD→E, B→D, E→A}
```
Try {A}⁺: A→BC gives {A,B,C}; B→D gives {A,B,C,D}; CD→E gives {A,B,C,D,E} = ALL.
→ {A}⁺ = R → A is a super key, and since it's a single attribute, it's minimal → CANDIDATE KEY.

Try {E}⁺: E→A gives {E,A}; A→BC gives {E,A,B,C}; B→D gives {E,A,B,C,D} = ALL.
→ E is also a Candidate Key.

Try {CD}⁺: CD→E gives {C,D,E}; E→A gives {C,D,E,A}; A→BC gives {C,D,E,A,B} = ALL.
→ CD is a Candidate Key (and minimal — dropping C or D alone doesn't reach all attributes).

Try {BC}⁺: B→D gives {B,C,D}; CD→E gives {B,C,D,E}; E→A gives {B,C,D,E,A} = ALL.
→ BC is also a Candidate Key.

Total Candidate Keys = {A}, {E}, {CD}, {BC} → 4 candidate keys.
```
**EXAM TRAP:** Students stop after finding ONE candidate key and pick that as the answer count (you answered "2" ❌, correct was **4**). Always systematically test **every** attribute/combination that could be minimal, especially attributes that appear only on the LHS of some FD or nowhere on the RHS (strong candidates to start with — they can NEVER be derived from other attributes).

**MEMORY TRICK:** An attribute that never appears on the right side of any FD (or on the left side of a determining chain) MUST be part of every candidate key — start closure testing there.

---

## B3. PARTIAL vs TRANSITIVE DEPENDENCY (2NF/3NF) — 🅰️ MUST KNOW

**CORE IDEA:** Partial Dependency = a non-prime attribute depends on only **part** of a composite candidate key (violates 2NF). Transitive Dependency = a non-prime attribute depends on another non-prime attribute, not directly on the key (violates 3NF).

**CONFUSION PAIR**

| | Partial Dependency | Transitive Dependency |
|---|---|---|
| Violates | 2NF | 3NF |
| Requires | Composite (multi-attribute) primary key | Any key size |
| Pattern | Non-prime attr depends on **part** of the key | Non-prime attr depends on **another non-prime attr** (Key→A→B chain) |
| Example | (StudentID, CourseID)→Grade; StudentID→StudentName [StudentName depends only on part of key] | RollNo→DeptID→DeptName [DeptName depends on DeptID, not RollNo directly] |

**MEMORY TRICK:** Partial = "key acting alone" (part of composite key does the job). Transitive = "a chain reaction" (Key → X → Y, Y is dependent on X, not Key).

## NORMAL FORMS — QUICK TABLE

| NF | Requirement | Removes |
|---|---|---|
| 1NF | Atomic values, no repeating groups | Multi-valued columns |
| 2NF | 1NF + no partial dependency | Partial dependency (only relevant if composite key) |
| 3NF | 2NF + no transitive dependency | Transitive dependency |
| BCNF | For every FD X→Y, X must be a super key | Anomalies 3NF misses (when overlapping composite candidate keys exist) |

**EXAM TRAP (your mock Q20):** R(A,B,C,D,E), F={A→B, BC→D, E→C}. Only A→B is a "full" single-attribute FD on part of nothing (no composite key given/no multi-attribute determinant issue directly shown) — with only single-attribute LHS dependency and no composite candidate key explicitly forcing partial dependency, such a relation may still sit at **1NF** if candidate key isn't {A} alone (need to check closure!). Always **compute the actual candidate key first** before assuming NF level — don't guess from FD shape alone.

---

## B4. INTEGRITY CONSTRAINTS — 🅰️ MUST KNOW

| Constraint | Rule | Trap |
|---|---|---|
| **Entity Integrity** | No primary key (or its component) can be NULL | Applies to PK only, not all keys |
| **Referential Integrity** | Foreign key must either be NULL (if allowed) or match an existing PK value in referenced table | Governs FK-PK relationship |
| **Domain Integrity** | Column value must respect its defined data type/domain/range | e.g., age column can't store text |

### REFERENTIAL INTEGRITY — ACTIONS (deep dive, your mock error Mock-1 Q1)
When a parent-table row is **updated/deleted**, and child rows reference it via FK:
- **CASCADE** — change propagates to child (update/delete child rows too).
- **SET NULL** — child FK set to NULL (only if FK allows NULL).
- **SET DEFAULT** — child FK set to a default value.
- **RESTRICT / NO ACTION** — operation is **rejected** if matching child rows exist.

**EXAM TRAP (exact mock scenario):** "Modifying a PK value in parent table R2 when matching FK values exist in R1, **without cascading**" → **violates referential integrity** (this was the correct answer, Mock-1 Q1 — you picked "deleting a child tuple," which is always SAFE and never violates integrity). 
**Key rule: Deleting/updating a CHILD row is always safe. Deleting/updating a PARENT row that has matching children (without cascade/proper handling) is what breaks referential integrity.**

**MEMORY TRICK:** "Children can leave home anytime (delete child = safe). Parents can't just disappear/change identity while kids still list that address (update/delete parent with active children = violation, unless cascade)."

**MCQs**
1. Deleting a row from the child table (FK side) — does this ever violate referential integrity?
   A. Yes, always B. No, never C. Only if PK is NULL D. Only with CASCADE
   **Ans: B**
2. A parent PK is updated with no cascade, and child FK rows reference the old value. This:
   A. Is always safe B. Violates referential integrity C. Violates entity integrity D. Violates domain integrity
   **Ans: B**
3. Entity Integrity constraint specifically restricts:
   A. Foreign key values B. Primary key from being NULL C. Data types D. Unique constraint duplicates
   **Ans: B**

---

## B5. NULL BEHAVIOR WITH AGGREGATE FUNCTIONS — 🅰️ MUST KNOW

**CORE IDEA:** `COUNT(*)` counts ALL rows including NULLs. `COUNT(column)` skips NULLs in that column. `AVG`, `SUM`, `MAX`, `MIN` all **ignore NULLs** automatically.

**WORKED EXAMPLE (your mock Q23 — you got this right, but memorize the mechanism):**
Employees(dept_id, salary): (10,1000), (20,2000), (30,NULL), (40,3000), (NULL,4000)
```
COUNT(dept_id) → counts non-NULL dept_id values → 4 (excludes the row where dept_id=NULL)
AVG(salary) → averages non-NULL salary values → (1000+2000+3000+4000)/4 = 2500
  (the row with salary=NULL is excluded entirely from AVG's count AND sum)
Answer: 4 and 2500
```

**EXAM TRAP:** `COUNT(*)` here would give **5** (all rows), NOT 4 — that's the classic trap swap between `COUNT(*)` and `COUNT(column)`.

**MEMORY TRICK:** `COUNT(*)` = "count heads in the room" (everyone, NULL or not). `COUNT(col)`/`AVG`/`SUM` = "count/average only those who answered" (skip NULLs).

---

## B6. WHERE vs HAVING — 🅰️ MUST KNOW

| Aspect | WHERE | HAVING |
|---|---|---|
| Applies to | Individual rows, BEFORE grouping | Groups, AFTER GROUP BY aggregation |
| Can use aggregate functions? | **No** (SUM, AVG, COUNT not allowed directly) | **Yes** — that's its main purpose |
| Execution order | Filters rows first | Filters groups after aggregation |
| Works without GROUP BY? | Yes | Yes (treats whole table as one group) |

**EXAM TRAP:** `SELECT dept_id, AVG(salary) FROM Emp WHERE AVG(salary)>5000 GROUP BY dept_id` → **syntax error** — aggregate functions cannot be used in WHERE. Must use HAVING instead.

**SQL LOGICAL EXECUTION ORDER (deeper level, often tested indirectly):**
```
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
```

**MEMORY TRICK:** WHERE = "gatekeeper before the party starts (before grouping)." HAVING = "bouncer checking groups after they've formed."

**MCQs**
1. Which clause filters rows BEFORE aggregation occurs?
   A. HAVING B. WHERE C. ORDER BY D. GROUP BY
   **Ans: B**
2. `SELECT dept_id, COUNT(*) FROM Emp GROUP BY dept_id HAVING COUNT(*)>5` — is this valid?
   A. Yes B. No, HAVING can't use COUNT C. No, GROUP BY missing WHERE D. No, syntax error
   **Ans: A — perfectly valid**

---

## B7. JOINS — 🅱️ HIGH PRIORITY

**MUST REMEMBER**
- **INNER JOIN**: only matching rows from both tables.
- **LEFT JOIN**: all rows from left + matched right (unmatched right columns = NULL).
- **RIGHT JOIN**: all rows from right + matched left.
- **FULL OUTER JOIN**: all rows from both, unmatched side filled with NULL.
- **Cardinality formula:** `Rows in FULL OUTER JOIN = |A| + |B| − (Matching Rows)`

**EXAM TRAP (deep, your mock Q6, correct but conceptually tricky):**
`SELECT * FROM Emp LEFT JOIN Dept ON Emp.dept_id=Dept.dept_id WHERE Dept.dept_name='IT'`
→ Adding a WHERE filter on the RIGHT table's column **functionally converts LEFT JOIN behavior into INNER JOIN** for that query — because unmatched rows have Dept.dept_name = NULL, and `NULL = 'IT'` is never true, so those rows get filtered out anyway. **The LEFT JOIN syntax remains, but the WHERE clause defeats its purpose.**

**WORKED EXAMPLE (cardinality, your mock Q26):**
Table A=5 rows, Table B=3 rows, 2 rows match.
```
FULL OUTER JOIN rows = |A| + |B| − matches = 5+3−2 = 6
```

**MEMORY TRICK:** "WHERE on the OUTER side's column silently turns your OUTER JOIN into an INNER JOIN." Always filter the outer-joined table's NULL-able column using the ON clause (not WHERE) if you want true outer-join behavior.

---

## B8. B-TREE vs B+ TREE (Indexing) — 🅱️ HIGH PRIORITY (your mock error)

**CORE IDEA:** Both are balanced multi-way search trees used for indexing. B+ Tree is the DB-industry standard because it's optimized for **range queries**.

**CONFUSION PAIR**

| | B-Tree | B+ Tree |
|---|---|---|
| Data pointers | Stored in **both** internal AND leaf nodes | Stored **only in leaf nodes** |
| Leaf node linking | Not linked | **Linked sequentially** (linked list of leaves) |
| Range query efficiency | Slower — must traverse tree repeatedly | **Fast — traverse leaf linked list directly** |
| Internal nodes | Hold actual data | Hold only keys (guide/index values), no data |
| Used in | Some file systems | **Almost all RDBMS indexes** (MySQL InnoDB, Oracle, etc.) |

**EXAM TRAP (your mock Q47 — you answered "fewer key comparisons for point queries" ❌):** The real structural advantage of B+ Tree over B Tree for **range queries** is that **leaf nodes are linked sequentially**, allowing efficient **linear traversal** across a range — NOT fewer comparisons for point (single-value) lookups.

**MEMORY TRICK:** B+ Tree leaves = "a linked chain of drawers" — once you find the starting drawer, slide along the chain for a range scan. B-Tree has no such chain.

**Indexing types (light touch — MEDIUM priority):**

| Index type | When formed |
|---|---|
| Primary Index (Dense) | Ordered data, unique key, entry for every record |
| Primary Index (Sparse) | Ordered data, entry only for some records (block pointer) |
| Clustering Index | Data physically ordered by a non-key (duplicate-allowing) column |
| Secondary Index (Dense) | Unordered data / non-key column with duplicates — must index every record |

**MCQs**
1. What is the main structural advantage of B+ Tree over B Tree for range queries?
   A. Fewer comparisons for point lookups B. Leaf nodes linked sequentially for linear traversal C. No balancing required D. Data pointers in internal nodes
   **Ans: B**
2. In a B+ Tree, where are the actual data pointers stored?
   A. Internal nodes only B. Both internal and leaf nodes C. Leaf nodes only D. Root node only
   **Ans: C**

---

## DBMS — CONSOLIDATED CONFUSION PAIRS

| Pair | Distinguishing test |
|---|---|
| Super Key vs Candidate Key | Minimality (can an attribute be dropped and still work?) |
| Partial vs Transitive Dependency | Depends on part of composite key vs depends on another non-prime attribute |
| Entity vs Referential vs Domain Integrity | PK-not-null vs FK-matches-PK vs value-fits-datatype |
| COUNT(*) vs COUNT(column) | Includes NULLs vs excludes NULLs |
| WHERE vs HAVING | Before grouping/no aggregates vs after grouping/allows aggregates |
| B-Tree vs B+ Tree | Data in all nodes, unlinked vs data only in linked leaves |
| Delete child row vs Update/Delete parent row | Always safe vs can violate referential integrity |

## PART B — DBMS: 10 THINGS I ABSOLUTELY CANNOT FORGET
1. Every Candidate Key is minimal — test by removing an attribute and re-checking closure.
2. Compute X⁺ systematically; don't stop at the first candidate key found (there can be several).
3. An attribute never appearing on any FD's RHS MUST be in every candidate key — start there.
4. Partial dependency needs a composite key; transitive dependency doesn't.
5. Deleting a CHILD row never violates referential integrity; updating/deleting a PARENT with active children (without cascade) does.
6. `COUNT(*)` includes NULLs; `COUNT(col)`, `AVG`, `SUM` exclude NULLs.
7. WHERE can't use aggregate functions; HAVING can.
8. Filtering the outer-joined table's column in WHERE silently converts LEFT/RIGHT JOIN behavior toward INNER JOIN.
9. FULL OUTER JOIN row count = |A| + |B| − matching rows.
10. B+ Tree's edge over B-Tree = linked leaf nodes for range scans, not fewer comparisons.

## PART B — DBMS: 5 MOST DANGEROUS TRAPS
1. Stopping candidate-key search after finding just one.
2. Assuming "deleting a row" always risks referential integrity (only PARENT-side deletes/updates do).
3. Using COUNT(*) and COUNT(column) interchangeably.
4. Believing WHERE can filter on an aggregate result.
5. Thinking B+ Tree wins on point-query speed rather than range-query traversal.

## PART B — DBMS: 60-SECOND RECALL
SuperKey ⊇ CandidateKey (minimal) → PrimaryKey (chosen one). Closure X⁺: expand via FDs until no growth; X⁺=R → super key; minimal → candidate key. Partial dep = part of composite key determines non-prime attr (breaks 2NF); Transitive = non-prime→non-prime chain (breaks 3NF). Entity Integrity=PK not NULL; Referential Integrity=FK matches parent PK or NULL; deleting child=safe, changing parent with active children=violation unless CASCADE/SET NULL/SET DEFAULT/RESTRICT. COUNT(*)=all rows; COUNT(col)/AVG/SUM=skip NULLs. WHERE before grouping, no aggregates; HAVING after grouping, aggregates allowed. FULL OUTER JOIN rows=|A|+|B|−matches. B+ Tree: leaves linked sequentially → fast range queries; B-Tree: data in all nodes, no leaf linking.

## PART B — DBMS: 10-QUESTION MINI TEST
1. Is every Super Key also a Candidate Key? *(No — only if minimal)*
2. How do you test if attribute set X is a super key? *(Compute X⁺; if it equals all attributes of R, yes)*
3. Partial dependency requires what kind of primary key? *(Composite/multi-attribute)*
4. Deleting a tuple from the child table — does it violate referential integrity? *(No, never)*
5. `COUNT(*)` vs `COUNT(col)` — which includes NULL rows? *(COUNT(*))*
6. Can WHERE filter using `AVG(salary)>5000`? *(No — must use HAVING)*
7. Formula for FULL OUTER JOIN cardinality? *(|A|+|B|−matches)*
8. Which join type does `WHERE` on the right table's column silently convert LEFT JOIN into? *(INNER JOIN behavior)*
9. What's the key structural feature that makes B+ Tree good for range queries? *(Linked leaf nodes)*
10. Which NF removes transitive dependency? *(3NF)*

---
---

# PART C — SQL

## SQL COMMAND → CATEGORY TABLE — 🅰️ MUST KNOW (your mock error, Mock-1 Q5, Q46)

| Command | Category | Full Form |
|---|---|---|
| CREATE, ALTER, DROP, **TRUNCATE** | **DDL** | Data Definition Language |
| INSERT, UPDATE, DELETE | **DML** | Data Manipulation Language |
| **GRANT**, REVOKE | **DCL** | Data Control Language |
| COMMIT, ROLLBACK, SAVEPOINT | **TCL** | Transaction Control Language |
| SELECT | **DQL** | Data Query Language |

**EXAM TRAP #1 (your exact mock error):** TRUNCATE is **DDL**, not DML — even though it removes data (feels like DML), because it also resets the table structure/auto-increment and can't be rolled back (implicit commit) like DDL. 
**EXAM TRAP #2 (your exact mock error):** GRANT/REVOKE are **DCL**, not DDL and not TCL — don't confuse "control" in DCL with "control" in TCL. DCL = permissions; TCL = transaction commit/rollback.

**MEMORY TRICK:** "**T**RUNCATE **T**ags along with DDL, not DML — it's structural, not row-by-row." **G**RANT = **G**ate-keeping (DCL, permissions) — different from TCL's transaction commits.

---

## TRUNCATE vs DELETE vs DROP — 🅰️ MUST KNOW (explicit table requested, your mock error)

| Aspect | DELETE | TRUNCATE | DROP |
|---|---|---|---|
| Category | DML | DDL | DDL |
| Removes | Specific rows (WHERE optional) | ALL rows | Entire table + structure/schema |
| WHERE clause? | Yes | No | N/A |
| Rollback possible? | Yes (logged row-by-row) | Generally No (minimal logging, auto-commit in most RDBMS) | No |
| Table structure after? | Retained | **Retained** (empty table) | **Destroyed** (table gone entirely) |
| Speed | Slower (row-by-row logging) | Faster (deallocates data pages) | N/A |
| Resets identity/auto-increment? | No | **Yes** (typically) | N/A (table gone) |

**EXAM TRAP (your mock Q48 — you answered DROP ❌):** "Remove all rows... while retaining table's structural definition... without writing individual row deletions to transaction log" = **TRUNCATE**, not DROP. DROP destroys the table definition entirely — it doesn't "retain structure."

**MEMORY TRICK:** DELETE = surgical (row by row, can undo). TRUNCATE = empty the box, keep the box. DROP = destroy the box itself.

---

## WHERE vs HAVING — 🅰️ MUST KNOW *(also see DBMS section B6 — same concept, repeated intentionally as memory aid)*

| | WHERE | HAVING |
|---|---|---|
| Filters | Rows (before grouping) | Groups (after GROUP BY + aggregation) |
| Aggregate functions allowed | No | Yes |
| Mandatory with GROUP BY? | No | No |

---

## GRANT/REVOKE vs COMMIT/ROLLBACK/SAVEPOINT — 🅰️ MUST KNOW (explicit table requested)

| | GRANT / REVOKE (DCL) | COMMIT / ROLLBACK / SAVEPOINT (TCL) |
|---|---|---|
| Purpose | **Permissions** — who can access/modify what | **Transaction management** — making changes permanent or undoing them |
| GRANT | Gives a privilege (e.g., SELECT, INSERT) to a user/role | — |
| REVOKE | Removes a previously granted privilege | — |
| COMMIT | — | Permanently saves all changes since last COMMIT/start of transaction |
| ROLLBACK | — | Undoes changes since last COMMIT (or to a SAVEPOINT) |
| SAVEPOINT | — | Marks a point within a transaction to which you can later ROLLBACK partially |

**EXAM TRAP:** `GRANT SELECT ON emp TO user1;` — students sometimes call this TCL because it "controls" something — it's **DCL** (controls access/permission, not transaction state).

**MEMORY TRICK:** DCL = "**D**oor keys" (who gets in). TCL = "**T**ime machine" (undo/redo/checkpoint within a transaction).

---

## DDL / DML SYNTAX QUICK REFERENCE — 🅱️/🅲 (light touch — you didn't miss these)

| Command | Use |
|---|---|
| `CREATE TABLE t (...)` | Define new table |
| `ALTER TABLE t ADD/MODIFY/DROP COLUMN` | Change table structure |
| `DROP TABLE t` | Delete table entirely |
| `TRUNCATE TABLE t` | Empty table, keep structure |
| `INSERT INTO t VALUES (...)` | Add row(s) |
| `UPDATE t SET col=val WHERE cond` | Modify existing rows |
| `DELETE FROM t WHERE cond` | Remove specific rows |

**EXAM TRAP:** `DELETE * FROM t` is **invalid syntax** — correct is `DELETE FROM t` (no `*` after DELETE, unlike SELECT *).

---

## CONSTRAINTS — 🅱️ HIGH PRIORITY (your mock error, CHECK constraint)

| Constraint | Enforces |
|---|---|
| **CHECK** | Column value must satisfy a **boolean expression** (e.g., `age > 18`) |
| NOT NULL | Column cannot store NULL |
| UNIQUE | No duplicate values (NULL allowed, usually only once depending on RDBMS) |
| PRIMARY KEY | UNIQUE + NOT NULL, one per table |
| FOREIGN KEY | Value must match a PK in referenced table (or be NULL) |
| DEFAULT | Auto-fills a value if none is provided |

**EXAM TRAP (your mock Q3 — you answered NOT NULL ❌):** "Enforces values satisfy a specific boolean logical expression" = **CHECK constraint**. NOT NULL only blocks NULLs — it can't evaluate arbitrary conditions like `salary > 0`.

---

## AGGREGATE FUNCTIONS, GROUP BY, SUBQUERIES, JOINS — 🅱️ HIGH PRIORITY (recap; see DBMS Part B for deep dive on WHERE/HAVING/NULL)

**MUST REMEMBER**
- Aggregate functions: `COUNT, SUM, AVG, MAX, MIN` — all ignore NULLs except `COUNT(*)`.
- `GROUP BY` groups rows sharing the same value(s) in specified column(s); typically paired with an aggregate in SELECT.
- **Subqueries**: nested SELECT; can appear in WHERE, FROM, or SELECT clause. Correlated subquery references outer query's columns (re-evaluated per outer row); non-correlated runs once independently.

**EXAM TRAP:** A `SELECT` with a non-aggregated column NOT included in `GROUP BY` is invalid in strict SQL mode (e.g., `SELECT dept_id, name, MAX(salary) FROM Emp GROUP BY dept_id` — `name` is neither grouped nor aggregated → **syntax/semantic error** — this was your mock Q27 answer, correctly identified).

---

## SQL — 20 ULTRA-HIGH-YIELD FACTS
1. TRUNCATE is DDL, not DML.
2. GRANT/REVOKE are DCL, not DDL or TCL.
3. TRUNCATE retains table structure; DROP destroys it entirely.
4. DELETE can use WHERE + can be rolled back; TRUNCATE generally cannot be rolled back.
5. CHECK constraint enforces boolean expressions; NOT NULL only blocks NULL.
6. `COUNT(*)` counts all rows including NULLs; `COUNT(col)` skips NULLs in that column.
7. AVG/SUM/MAX/MIN all ignore NULL values automatically.
8. WHERE filters rows before grouping; cannot use aggregate functions.
9. HAVING filters groups after aggregation; CAN use aggregate functions.
10. SQL logical execution order: FROM→WHERE→GROUP BY→HAVING→SELECT→ORDER BY.
11. Every non-aggregated SELECT column must appear in GROUP BY (strict SQL mode).
12. FULL OUTER JOIN row count = |A| + |B| − matching rows.
13. Filtering the right/outer table's column in WHERE (not ON) converts an OUTER JOIN's effective behavior toward INNER JOIN.
14. `DELETE * FROM t` is invalid syntax; correct is `DELETE FROM t`.
15. SAVEPOINT allows partial rollback within a transaction (TCL).
16. Referential Integrity: deleting a child row is always safe; updating/deleting a parent row with matching children (w/o cascade) violates it.
17. Entity Integrity = Primary Key can never be NULL.
18. B+ Tree leaf nodes are linked sequentially — enables efficient range queries.
19. Data pointers exist only in leaf nodes in B+ Tree (not internal nodes).
20. Candidate Key = minimal Super Key; test minimality by attribute-closure after removing one attribute.

## SQL — 10 DANGEROUS TRAPS
1. Calling TRUNCATE a DML command.
2. Calling GRANT/REVOKE a TCL command.
3. Confusing TRUNCATE ("keeps structure") with DROP ("destroys structure").
4. Using aggregate functions inside WHERE instead of HAVING.
5. Assuming COUNT(*) = COUNT(column) when NULLs exist.
6. Assuming CHECK and NOT NULL are interchangeable.
7. Believing WHERE filtering an outer-joined table's column preserves true OUTER JOIN semantics.
8. Writing `DELETE * FROM t` (invalid syntax).
9. Selecting a non-aggregated, non-grouped column alongside an aggregate function.
10. Assuming deleting from the FK-side (child) table can break referential integrity.

## SQL — 15 IBPS-LEVEL MCQs
1. `TRUNCATE TABLE Logs;` belongs to which category? **A. DDL**
2. Which command removes a previously granted privilege? **A. REVOKE**
3. Which constraint enforces `salary > 0`? **A. CHECK**
4. `SELECT COUNT(dept_id) FROM Employees` where one row has dept_id=NULL out of 5 rows returns: **A. 4**
5. Which clause can legally contain `HAVING AVG(salary) > 5000`? **A. HAVING itself, correctly placed after GROUP BY**
6. `DROP TABLE Logs;` — is table structure retained? **A. No**
7. Which TCL command lets you undo only part of a transaction? **A. SAVEPOINT (with ROLLBACK TO)**
8. `SELECT dept_id FROM Employees GROUP BY dept_id;` (no aggregate used) — valid? **A. Yes, valid**
9. Table A (5 rows), Table B (3 rows), 2 matches — FULL OUTER JOIN row count? **A. 6**
10. Which SQL sub-language does COMMIT belong to? **A. TCL**
11. `GRANT SELECT, INSERT ON customer TO teller_role;` belongs to: **A. DCL**
12. B+ Tree's biggest advantage for range queries comes from: **A. Sequentially linked leaf nodes**
13. Which of these best distinguishes DELETE from TRUNCATE? **A. DELETE supports WHERE and is typically rollback-able; TRUNCATE is not**
14. `SELECT dept_id, name, MAX(salary) FROM Employees GROUP BY dept_id;` — valid? **A. No — `name` is neither aggregated nor grouped**
15. Entity Integrity constraint mandates: **A. No primary key value can be NULL**

## SQL — 10-QUESTION RAPID RECALL TEST
1. TRUNCATE = DDL or DML? *(DDL)*
2. GRANT/REVOKE = which category? *(DCL)*
3. Which is faster and generally non-rollback-able: DELETE or TRUNCATE? *(TRUNCATE)*
4. Which constraint checks a boolean expression? *(CHECK)*
5. Does COUNT(*) include NULL rows? *(Yes)*
6. Can WHERE use AVG()? *(No)*
7. SQL logical execution order — what comes right after WHERE? *(GROUP BY)*
8. FULL OUTER JOIN formula? *(|A|+|B|−matches)*
9. Which TCL command allows partial rollback? *(SAVEPOINT)*
10. Is `DELETE * FROM t` valid SQL? *(No)*
