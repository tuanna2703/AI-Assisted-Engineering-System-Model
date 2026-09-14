# Agent–Runtime Execution Bridge Inspection

## 1. Scope and Baseline

| Item | Value |
|---|---|
| **Repository** | `tuanna2703/AI-Assisted-Engineering-System-Model` |
| **Branch** | `main` |
| **Task character** | Bounded inspection and decision-boundary task — not an implementation task |
| **DBP repository** | `tuanna2703/directories-builder-pro` (accessible read-only in this session) |
| **DBP reference file** | `modules/reviews/forms/add-review-form.php` — `Add_Review_Form` class |
| **DBP reference commit** | `deaabeb175593ec2c607b816eb80b7d16f4f01c5` |
| **Inspection date** | 2026-09-14 |

### Files Inspected

**Runtime implementation:**
- [`runtime/core/models.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/models.py)
- [`runtime/core/store.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/store.py)
- [`runtime/core/runtime.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py)
- [`runtime/core/__init__.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/__init__.py)
- [`runtime/persistence/json_store.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/persistence/json_store.py)
- [`runtime/README.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/README.md)

**Documentation:**
- [`docs/04-Execution-Model.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/04-Execution-Model.md)
- [`docs/05-Process-Instance-and-Execution-Context.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/05-Process-Instance-and-Execution-Context.md)
- [`docs/06-Participants-and-Agent-Participation.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/06-Participants-and-Agent-Participation.md)
- [`docs/07-Runtime-and-Conformance.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/07-Runtime-and-Conformance.md)
- [`docs/08-Continuity-Traceability-and-Reconsideration.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/08-Continuity-Traceability-and-Reconsideration.md)
- [`docs/09-Operational-Guide.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/09-Operational-Guide.md)
- [`docs/12-AI-Agent-Guide.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/12-AI-Agent-Guide.md)
- [`docs/13-Runtime-Implementer-Guide.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/13-Runtime-Implementer-Guide.md)

**Tests:**
- [`tests/continuity/test_runtime_recovery.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/tests/continuity/test_runtime_recovery.py)
- [`tests/continuity/xprocess_orchestrator.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/tests/continuity/xprocess_orchestrator.py)
- [`tests/lifecycle/test_runtime_lifecycle.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/tests/lifecycle/test_runtime_lifecycle.py)
- [`tests/lifecycle/test_process_instance_lifecycle_control.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/tests/lifecycle/test_process_instance_lifecycle_control.py)
- [`tests/recording/test_runtime_recording.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/tests/recording/test_runtime_recording.py)

**Execution records:**
- [`execution/RUNTIME-CAPABILITY-BEHAVIORAL-VALIDATION.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/RUNTIME-CAPABILITY-BEHAVIORAL-VALIDATION.md)
- [`execution/NEXT-RUNTIME-CAPABILITY-REASSESSMENT.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/NEXT-RUNTIME-CAPABILITY-REASSESSMENT.md)
- [`execution/EVIDENCE-RECORDING-CLOSURE.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/EVIDENCE-RECORDING-CLOSURE.md)
- [`execution/POST-CORRECTION-RECONCILIATION-RECORDING-ROLLBACK.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/POST-CORRECTION-RECONCILIATION-RECORDING-ROLLBACK.md)

**Plan and baseline:**
- [`IMPLEMENTATION_PLAN.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/IMPLEMENTATION_PLAN.md)
- [`IMPLEMENTATION_BASELINE.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/IMPLEMENTATION_BASELINE.md)

**DBP source (read-only):**
- [`add-review-form.php`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/wp-content/plugins/directories-builder-pro/modules/reviews/forms/add-review-form.php)

**Environment configuration:**
- [`.agents/rules/start-here.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/.agents/rules/start-here.md)

### Test Execution Evidence

**Freshly executed** during this inspection:

```
88 passed in 0.87s (Python 3.13.5, pytest, macOS)
```

All 88 existing tests pass. No production code was modified.

### Runtime Invocability Evidence

**Freshly executed** during this inspection: the Agent successfully invoked the Runtime programmatically via `run_command`, creating a Process Instance, stopping the Runtime, and recovering it through a new Runtime instance. This confirms the Agent's current environment **does** provide code execution capability sufficient to invoke the AESM Runtime.

---

## 2. Decision Gate — Established Before Investigation

The inspection concludes with **Outcome B — Thin Agent–Runtime Bridge Justified**.

The reasoning and evidence supporting this conclusion are developed throughout the following sections.

---

## 3. Execution Environment Evidence

### Mechanisms Available to the Agent

| Mechanism | Status | Evidence Type |
|---|---|---|
| Repository file read/write | Available | Directly observed in this session |
| Python code execution via `run_command` | Available | Directly observed in this session |
| Repository-level Agent instructions (`.agents/rules/`) | Available | Directly observed — `start-here.md` exists |
| Task/process-specific instructions | Not configured for AESM | Directly observed — no AESM-specific instructions exist |
| Agent skills | Available at global level | Documented in environment — built-in skills exist; no AESM skills |
| MCP tool mechanisms | Available at global level | `~/.gemini/config/mcp_config.json` exists; no AESM MCP server configured |
| CLI interaction | Available | Directly observed — `run_command` tool |
| IDE interaction (VS Code) | Available as current environment | Known capability of the current environment |
| Browser subagent | Available | Known capability of the current environment |
| Repository files as persistent state | Available | Directly observed — AESM persistence store uses JSON files |
| Presenting authoritative context to the Agent | Not implemented for AESM | Directly observed — no mechanism currently presents Execution Context |
| Persisting information across Agent sessions | Available via filesystem | Directly observed — persistence store files survive session loss |
| AESM Runtime invocation | Available via Python execution | **Freshly executed** — Agent can invoke `Runtime` class through `run_command` |

### Critical Environment Findings

1. **The Agent CAN execute the Runtime.** The current Execution Environment provides Python execution capability. The Agent successfully created a Process Instance, stopped the Runtime, and recovered it through a second Runtime instance — all via `run_command`.

2. **No mechanism currently DOES invoke the Runtime for AESM purposes.** No instructions, skills, MCP servers, or other configuration cause AESM Runtime operations to occur when an engineering request is received. The Runtime is available as a library but sits dormant.

3. **No mechanism currently presents Execution Context to the Agent.** The Agent can read AESM documentation, but there is no mechanism that identifies a relevant Process Instance, loads its Execution Context, and presents it to the Agent as the authoritative starting point for engineering work.

4. **Workspace Agent instructions are DBP-specific, not AESM-aware.** The `.agents/rules/start-here.md` file instructs the Agent to read DBP documentation and follow DBP workflow. It makes no reference to AESM, Process Instances, or Execution Context.

---

## 4. DBP Reference Scenario

### Source Accessibility

The DBP source is **directly accessible** in this session at `wp-content/plugins/directories-builder-pro/`. The reference file [`add-review-form.php`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/wp-content/plugins/directories-builder-pro/modules/reviews/forms/add-review-form.php) was inspected read-only.

### Current DBP Form State

The `Add_Review_Form` class (lines 27–161) currently:

- Uses `Fields_Manager::POST_SELECT` for the `business_id` field (line 113), selecting a WordPress post of type `dbp_business`.
- In `save()`, receives `$values['business_id']` as a WordPress post ID (line 49).
- Resolves the internal `business_id` through `Business_Repository::find_by_post_id()` (line 51).
- Validates that `$business_id !== 0` (line 62).

This appears to already reflect the described change (post-selection with `Business_Repository` resolution). The reference commit `deaabeb` may represent this change or an earlier state.

### What a Real Agent Currently Does (Observed)

When a human gives this Agent a DBP engineering request today, the actual execution path is:

```text
Human: "Change the business_id field to use post selection"
        ↓
Agent reads .agents/rules/start-here.md
        ↓
Agent reads DBP AI_START_HERE.md and AI_WORKFLOW.md
        ↓
Agent investigates the codebase
        ↓
Agent modifies add-review-form.php
        ↓
Agent reports changes
        ↓
Conversation ends
```

**No AESM Runtime is invoked.** No Process Instance is created. No Execution Context is established. No authoritative state is persisted. If the conversation ends mid-work, continuity depends entirely on conversation history or human re-instruction.

### AESM Participation Points (Scenario-Based Reasoning)

For AESM to participate operationally in this request, the following would need to happen:

| Step | What must happen | Current status |
|---|---|---|
| Receive request | Create or identify Process Instance | **No mechanism exists** |
| Establish context | Load or create authoritative Execution Context | **No mechanism exists** |
| Present to Agent | Agent receives objective, requirements, constraints, state | **No mechanism exists** |
| Investigation | Agent investigates DBP codebase | Agent can do this already |
| Evidence | Record investigation findings as authoritative evidence | **No mechanism connects Agent to Runtime** |
| Decision | Record engineering decision | **No mechanism connects Agent to Runtime** |
| Implementation | Agent modifies source files | Agent can do this already |
| Artifact recording | Record artifacts in Execution Context | **No mechanism connects Agent to Runtime** |
| Verification | Record verification results | **No mechanism connects Agent to Runtime** |
| Completion | Recognize engineering completion | **No mechanism connects Agent to Runtime** |
| Continuation | Resume from authoritative state | **No mechanism presents persisted state** |

**Classification: The engineering work itself is available. The AESM participation wrapper is entirely absent.**

---

## 5. Process Instance Investigation

### How is a Process Instance created?

**Runtime source evidence** ([`runtime.py` lines 41–46](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L41-L46)): `Runtime.create_process(objective)` creates a `ProcessInstance` with a UUID, creates its `ExecutionContext`, persists both through `ProcessStore`, and attaches the Runtime.

**Current operational status:** The Runtime CAN create Process Instances. The Agent CAN invoke the Runtime. But **nothing currently causes Process Instance creation when an engineering request is received.**

### What event causes creation?

**No evidence found.** There is no trigger, listener, instruction, or mechanism that observes an incoming engineering request and initiates Process Instance creation.

### How is an existing Process Instance identified?

**Runtime source evidence** ([`runtime.py` lines 48–51](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L48-L51)): `Runtime.attach(process_instance_id)` loads a Process Instance and its Execution Context from the store by UUID.

**Current operational status:** Attachment requires knowing the UUID. No discovery mechanism exists that maps a human-readable engineering objective or repository context to an existing Process Instance.

### Can the Agent discover an existing instance without relying on conversation history?

**No.** The persistence store uses UUID-based directory naming (`process-instance/<uuid>/`). There is no index, registry, or search capability. An Agent in a fresh session would need the UUID from either:
- Conversation history (explicitly prohibited as authoritative by AESM)
- An external record or instruction containing the UUID
- A discovery mechanism that does not yet exist

### Where is Process Instance identity persisted?

**Runtime source evidence** ([`store.py` lines 18–22](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/store.py#L18-L22)): Persisted as `process.json` and `context.json` under `<store_root>/process-instance/<uuid>/`.

### Who owns that identity?

**The Runtime through ProcessStore.** Identity is a UUID generated at creation time and persisted to filesystem.

### Can multiple Agent sessions access the same Process Instance?

**Yes, in principle.** The `attach()` method loads from persistent storage. The cross-process continuity tests (`xprocess_orchestrator.py` and related scripts) demonstrate this across OS processes. **Freshly confirmed** in this inspection: two Runtime instances with different `runtime_id` values successfully accessed the same Process Instance.

### What happens when an Agent session disappears?

**The Process Instance persists.** Filesystem state is durable. However, the in-memory Runtime state (including the `attached` flag and context reference) is lost. A new session must create a new Runtime and call `attach()` with the UUID.

### Classification

| Concern | Classification |
|---|---|
| Process Instance creation capability | **Conformant — Demonstrated** |
| Process Instance creation from engineering request | **Implementation Gap — Semantically Required** |
| Process Instance identity persistence | **Conformant — Demonstrated** |
| Process Instance discovery by UUID | **Conformant — Demonstrated** |
| Process Instance discovery without UUID | **Implementation Gap — Semantically Required** |
| Process Instance survival across sessions | **Conformant — Demonstrated** |
| Agent-initiated Process Instance creation | **Implementation Gap — Semantically Required** |

---

## 6. Execution Context Investigation

### What the Context contains

**Runtime source evidence** ([`models.py` lines 38–74](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/models.py#L38-L74)):

| Context element | Implemented | Field |
|---|---|---|
| Process Instance identity | Yes | `process_instance_id` |
| Engineering objective | Yes | `engineering_objective` |
| Current process state | Yes | `process_state` |
| Execution mode | Yes | `execution_mode` |
| Requirements | Yes | `requirements` |
| Constraints | Yes | `constraints` |
| Evidence | Yes | `evidence` |
| Assumptions | Yes | `assumptions` |
| Risks | Yes | `risks` |
| Candidate solutions | Yes | `candidate_solutions` |
| Engineering decisions | Yes | `engineering_decisions` |
| Decision gates | Yes | `decision_gates` |
| Artifacts | Yes | `artifacts` |
| Verification | Yes | `verification` |
| Unresolved matters | Yes | `unresolved_matters` |
| Pending execution | Yes | `pending_execution` |
| Execution determination | Yes | `execution_determination` |
| Failure/uncertainty | Yes | `failure_uncertainty` |
| Engineering completion | Yes | `engineering_completion` |
| Version | Yes | `version` |

### Where is this information stored?

**ProcessStore** persists it as `context.json` with atomic file replacement via `json_store.py`. History is appended to `history.jsonl`.

### How is it retrieved?

**`Runtime.attach(pid)`** loads both `ProcessInstance` and `ExecutionContext` from the store. The Agent can then access `runtime.context` and `runtime.process_instance`.

### Does the Agent actually receive it?

**No.** In the current execution path, no mechanism:
1. Identifies which Process Instance is relevant to the current task.
2. Loads its Execution Context.
3. Presents the context to the Agent in a form it can use for engineering work.

The Runtime can load and provide this information, but nothing orchestrates the connection between the Agent and the Runtime.

### Is the information authoritative?

**Yes.** The Execution Context stored in `context.json` is the authoritative operational state. The Runtime controls mutations through recognized operations with guards, versioning, and rollback. This is confirmed by:
- 88 passing tests
- Cross-process continuity experiments
- Persistence-failure rollback validation

### Is conversation history being treated as the continuity mechanism?

**In effect, yes.** Because no bridge exists, the Agent currently has no way to resume from authoritative AESM state. If a session ends and a new session begins, the Agent would rely on:
- Conversation history (if available)
- Human re-instruction
- Reading the repository (without knowing which Process Instance applies)

The AESM specification explicitly prohibits this: "A conforming system must not substitute conversation memory for missing authoritative state" ([`docs/05`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/05-Process-Instance-and-Execution-Context.md), line 157).

### Key answer

> **Can the current Agent resume meaningful engineering work from authoritative AESM state rather than from prior conversation context?**

**No.** The Execution Context exists and is authoritative, but no mechanism presents it to the Agent.

### Classification

| Concern | Classification |
|---|---|
| Execution Context data model | **Conformant — Demonstrated** |
| Execution Context persistence | **Conformant — Demonstrated** |
| Execution Context recovery (Runtime side) | **Conformant — Demonstrated** |
| Execution Context delivery to Agent | **Implementation Gap — Semantically Required** |
| Continuity without conversation history | **Implementation Gap — Semantically Required** |

---

## 7. Agent → Runtime Boundary

### Which situation describes reality?

The actual current situation is:

```text
Human request
        ↓
AI Agent
        ↓
Agent guidance / repository instructions
        ↓
Engineering work
        ↓
Repository changes
```

Not:

```text
Human / AI Agent
        ↓
Execution Environment
        ↓
AESM Runtime
```

**Evidence:**

1. **No Runtime invocation occurs** during normal Agent engineering work. The Agent reads `.agents/rules/start-here.md`, reads DBP documentation, and performs work. The AESM Runtime is never instantiated.

2. **The Agent CAN invoke the Runtime** (freshly demonstrated) but **nothing currently causes it to do so.** The capability exists but is unconnected.

3. **Agent contributions do not reach the Runtime.** When the Agent produces evidence, decisions, artifacts, or verification results during DBP work, none of these are submitted to the Runtime through `observe()`, `recognize_decision()`, `record_artifact()`, or `record_verification()`.

4. **No transport/interface exists.** There is no MCP server, CLI adapter, HTTP API, Agent skill, or instruction that bridges Agent activity to Runtime operations.

5. **The Agent cannot mutate authoritative state directly.** The Agent does not have filesystem-level access to `process-instance/` directories in a way that would bypass Runtime controls. However, this is an implementation detail of the current environment rather than an architectural guarantee — the Agent does have general filesystem access.

### Does a transport already exist?

**No.** The Runtime README explicitly identifies this: "Agent/MRAP and workspace/tool adapters are not yet implemented" (line 44).

### Is the current mechanism merely procedural guidance?

**Yes.** The AESM documentation provides guidance on how an Agent *should* participate (`docs/12-AI-Agent-Guide.md`), but this is descriptive documentation, not an operational mechanism. An Agent reading this guide gains understanding but does not thereby participate in an AESM Process Instance.

**Reading AESM documentation is not evidence of AESM execution participation.**

### Classification

| Concern | Classification |
|---|---|
| Agent → Runtime operational boundary | **Implementation Gap — Semantically Required** |
| Agent contribution reaching Runtime | **Implementation Gap — Semantically Required** |
| Runtime recognition of Agent contributions | **Conformant — Demonstrated** (when contributions reach it) |
| Transport/interface | **Implementation Gap — Semantically Required** |

---

## 8. Runtime Authority Investigation

### Current authoritative operations

| Operation | Method | Authority demonstrated |
|---|---|---|
| Process Instance creation | `create_process()` | Creates UUID, persists, attaches |
| Process Instance attachment/recovery | `attach()` | Loads from store, validates |
| Start investigation | `start_investigation()` | Guards: attached, active lifecycle, initial state |
| Evidence recording | `observe()` | Recognition required; rollback on failure |
| Decision recognition | `recognize_decision()` | Recognition required; state guard; rollback on failure |
| Begin implementation | `begin_implementation()` | Requires recognized decision; state guard |
| Pending execution | `set_pending_execution()` | Guards: attached, active, implementation state |
| Artifact recording | `record_artifact()` | Guards: attached, active, implementation state; rollback |
| Begin verification | `begin_verification()` | Guards: artifacts required, no pending execution |
| Verification recording | `record_verification()` | State guard; rollback on failure |
| Reconsideration | `reconsider()` | Requires failed verification; records reason |
| Engineering completion | `recognize_engineering_completion()` | Recognition required; verification must pass |
| Lifecycle determination | `apply_lifecycle_determination()` | Full authority: validated transitions, semantic basis, conflict detection |
| Detachment | `stop()` | Clears in-memory state |
| Persistence | `ProcessStore.*` | Atomic writes, version control, rollback |
| History/traceability | `history.jsonl` | Append-only event log |

### What the Agent can request (with bridge)

The Agent would need to invoke the following Runtime operations:

1. `create_process(objective)` — create a new Process Instance
2. `attach(pid)` — recover an existing Process Instance
3. `start_investigation()` — begin investigation
4. `observe(observation)` — submit recognized evidence
5. `recognize_decision(decision, recognition)` — submit engineering decision
6. `begin_implementation()` — transition to implementation
7. `set_pending_execution(work)` — record continuation work
8. `record_artifact(artifact)` — record implementation artifact
9. `begin_verification()` — begin verification phase
10. `record_verification(result)` — record verification result
11. `reconsider(reason)` — request reconsideration
12. `recognize_engineering_completion(completion)` — complete engineering

### What the Agent can perform independently

- Investigation and analysis of source code
- Reading and understanding requirements
- Producing candidate solutions
- Writing and modifying source files
- Running tests and other verification commands
- Proposing decisions, evidence, and artifacts

### What Runtime validates

Every mutation operation validates:
- Attachment state (Process Instance loaded)
- Active lifecycle (not suspended/terminated)
- Correct process state for the operation
- Recognition records where applicable (evidence, decisions, completion)
- Required preconditions (e.g., artifacts before verification, decisions before implementation)

### What becomes authoritative only after Runtime mutation

Information produced by the Agent becomes authoritative **only** when the Runtime has:
1. Received it through a recognized operation
2. Validated its preconditions
3. Persisted it to the authoritative store
4. Recorded it in the history log

Agent-produced content that exists only in conversation memory, agent files, or other transient state is not authoritative AESM state.

---

## 9. Guidance vs. Enforcement Analysis

| Concern | Guidance | Runtime Enforcement | Evidence |
|---|---|---|---|
| Process Instance identity | Partial | Yes | `docs/12-AI-Agent-Guide.md` instructs Agent to treat PI as persistent unit; `Runtime.create_process()` and `attach()` enforce identity through UUID and store |
| Execution Context retrieval | Yes | Yes | `docs/12-AI-Agent-Guide.md` instructs Agent to reconstruct from authoritative Context; `Runtime.attach()` enforces Context loading with integrity validation |
| Evidence recognition | Yes | Yes | `docs/06-Participants-and-Agent-Participation.md` describes contribution path; `Runtime.observe()` enforces recognition requirement and persists |
| Decision recognition | Yes | Yes | `docs/12-AI-Agent-Guide.md` describes proposals vs decisions; `Runtime.recognize_decision()` enforces recognition and state guard |
| Artifact recording | Partial | Yes | Limited guidance in docs; `Runtime.record_artifact()` enforces implementation state and active lifecycle |
| Verification recognition | Yes | Yes | `docs/04-Execution-Model.md` distinguishes execution result from verification; `Runtime.record_verification()` enforces state guards |
| State transition control | Yes | Yes | `docs/04-Execution-Model.md` describes transition semantics; Runtime methods enforce state preconditions |
| Persistence | No | Yes | No agent guidance describes how to persist; `ProcessStore` provides atomic persistence with rollback |
| Continuity | Yes | Partial | `docs/05-Process-Instance-and-Execution-Context.md` describes continuity invariant; Runtime provides recovery (`attach`) but **no mechanism presents Context to Agent** |

### Analysis

Guidance and enforcement are both present but **disconnected**. The documentation describes how an Agent *should* participate, and the Runtime enforces semantic correctness for operations that reach it. The gap is between these two layers:

- Guidance tells the Agent what it should do.
- Runtime enforces correctness for operations it receives.
- **Nothing connects the Agent's actions to the Runtime's enforcement.**

This is the operational gap.

---

## 10. Responsibility Boundary

### Human

| Responsibility | Current placement | Evidence |
|---|---|---|
| Engineering intent | Human | Human provides the engineering request |
| Authorization | Human | No explicit authorization mechanism; implicit in request |
| Review | Human | Human reviews Agent output |
| Acceptance | Human | Human accepts or rejects work |
| Decisions requiring human authority | Human | No mechanism routes these through Runtime |

### AI Agent

| Responsibility | Current placement | Evidence |
|---|---|---|
| Investigation | Agent | Agent reads and analyzes source code |
| Analysis | Agent | Agent evaluates solutions |
| Proposing decisions | Agent | Agent can propose changes |
| Performing engineering work | Agent | Agent modifies source files |
| Interacting with tools | Agent via Execution Environment | Agent uses `run_command`, file tools |
| Producing candidate artifacts | Agent | Agent creates and modifies files |
| Performing verification | Agent | Agent can run tests |
| Reporting results | Agent | Agent reports to human in conversation |

### Runtime

| Responsibility | Current placement | Evidence |
|---|---|---|
| Process Instance authority | Runtime (but unreachable) | `Runtime.create_process()`, `attach()` |
| Execution Context authority | Runtime (but unreachable) | `ProcessStore` with atomic persistence |
| Recognition | Runtime (but unreachable) | `_require_recognition()` guards |
| Validation | Runtime (but unreachable) | State and lifecycle guards on every operation |
| Permitted state mutation | Runtime (but unreachable) | All mutation goes through Runtime methods |
| Persistence | Runtime (but unreachable) | `ProcessStore` with atomic write + rollback |
| Traceability | Runtime (but unreachable) | `history.jsonl` append-only log |
| Execution governance | Runtime (but unreachable) | State machine with enforced transitions |

### Execution Environment

| Responsibility | Current placement | Evidence |
|---|---|---|
| Presenting Agent interaction | Execution Environment | IDE provides chat, files, terminal |
| Providing tools | Execution Environment | `run_command`, file tools, browser |
| Transporting requests/results | **NOT IMPLEMENTED** | No bridge exists |
| Exposing persistent instructions | Execution Environment | `.agents/rules/start-here.md` exists |
| Providing skills/MCP mechanisms | Execution Environment | Available but no AESM skills/MCP configured |

### Key finding

The Runtime has the correct responsibilities and enforces them correctly. The Agent has the correct capabilities. The Execution Environment provides sufficient tools. **The missing piece is the connection between them.**

---

## 11. Minimum Information Crossing the Boundary

### Agent → Runtime

| Information | Justified | Evidence |
|---|---|---|
| Process Instance identity | Yes | Required to identify/create the Process Instance |
| Requested operation | Yes | Agent must indicate what Runtime operation to perform |
| Semantic contribution type | Partial | Implicit in the operation (observe, record_artifact, etc.) |
| Evidence/result data | Yes | The substance of the contribution |
| Recognition information | Yes | Required by `_require_recognition()` for evidence, decisions, completion |
| Provenance/actor | Yes | Runtime records `runtime_id`; could also record agent identity |

### Runtime → Agent

| Information | Justified | Evidence |
|---|---|---|
| Process Instance identity | Yes | Agent needs to know which PI it's working on |
| Engineering objective | Yes | Agent needs the objective to guide work |
| Current process state | Yes | Agent needs to know what operations are permissible |
| Lifecycle state | Yes | Agent needs to know if PI is active |
| Requirements and constraints | Yes | Agent needs these for engineering work |
| Evidence | Yes | Agent needs to build on established evidence |
| Engineering decisions | Yes | Agent needs to know accepted decisions |
| Artifacts | Yes | Agent needs to know what has been implemented |
| Verification state | Yes | Agent needs to know verification status |
| Unresolved matters | Yes | Agent needs to address these |
| Pending execution | Yes | Agent needs to know continuation work |
| Failure/uncertainty | Yes | Agent needs to address failures |
| Completion state | Yes | Agent needs to know if engineering is complete |

### What is NOT justified

- Transport-specific metadata (HTTP headers, MCP framing, etc.)
- Agent-internal reasoning state
- Execution Environment configuration
- Runtime-internal versioning details (version number may be informational but is not required for Agent decisions)

---

## 12. Continuity and Session Loss

### Current support for cross-session continuity

```text
Agent session A
      ↓
authoritative persisted AESM state    ← EXISTS (process.json, context.json, history.jsonl)
      ↓
Agent session B
      ↓
continued engineering work             ← NO MECHANISM TO LOAD AND PRESENT STATE
```

### Evidence

**Previously recorded evidence:**
- Cross-process continuity tests exist (`xprocess_orchestrator.py`, `xprocess_process_a.py`, `xprocess_process_b.py`). These demonstrate that separate OS processes can create, persist, and recover Process Instances.
- `test_process_and_context_survive_runtime_replacement` (freshly executed, PASSED) demonstrates Runtime replacement within a single process.

**Freshly executed evidence:**
- This inspection confirmed that the Agent can invoke `Runtime.create_process()` and `Runtime.attach()` programmatically.

**Gap:**
- The Agent in session B would need to know the Process Instance UUID to call `attach()`.
- No discovery mechanism maps "I'm working on the DBP Add_Review_Form change" to a specific UUID.
- Without the UUID, the Agent must rely on conversation history or external human provision — which violates the continuity invariant.

### Classification

| Concern | Classification |
|---|---|
| Persisted state survives session loss | **Conformant — Demonstrated** |
| New Runtime can recover from persisted state | **Conformant — Demonstrated** |
| Agent can programmatically invoke recovery | **Conformant — Demonstrated** |
| Agent can discover relevant Process Instance | **Implementation Gap — Semantically Required** |
| Agent receives authoritative Context on session start | **Implementation Gap — Semantically Required** |

---

## 13. Environment Independence

### Assessment

The minimum Agent–Runtime boundary does **not** depend on a particular Execution Environment.

| Environment | Could the boundary operate? | Reason |
|---|---|---|
| VS Code (current) | Yes | Agent has `run_command`, file access, Python execution |
| Another IDE with Agent | Yes | Requires Python execution and file access |
| CLI | Yes | Python execution directly available |
| Another Agent environment | Yes | Requires: invoke Python, read/write files |
| Another tool transport | Yes | Runtime is a Python library; transport is not prescribed |

### Key finding

The Runtime is a Python library with no environment-specific dependencies. It operates on filesystem persistence. Any environment that can:
1. Execute Python code
2. Read/write files

can invoke the Runtime.

The current environment (VS Code with Antigravity agent) happens to provide these capabilities, but AESM does not require VS Code. The architecture achieves the required environment independence.

### Implementation convenience vs. architectural requirement

If an MCP server or CLI adapter is eventually built, it would be an **implementation convenience** within a particular environment, not an architectural requirement. The Runtime semantics do not change regardless of transport.

---

## 14. Constraints and Non-Goals Verification

| Constraint | Preserved? | Evidence |
|---|---|---|
| AESM independent of VS Code | Yes | Runtime is a Python library with filesystem persistence |
| Distinct components (EPM, PEM, Runtime, etc.) | Yes | Architecture separates these; this inspection does not collapse them |
| Runtime authoritative for state mutation | Yes | All mutations through Runtime methods with guards |
| Agent is not a second Runtime | Yes | Agent does not control authoritative state |
| Execution Environment not authoritative state owner | Yes | Filesystem is a persistence mechanism, not the state owner |
| Conversation history not continuity authority | Yes (design) / No (practice) | Specification prohibits it; in practice it's the only mechanism today |
| No second authoritative state model | Yes | This inspection does not introduce one |
| Guidance not confused with enforcement | Yes | Section 9 explicitly distinguishes them |
| Transport not normative | Yes | This inspection does not select a transport |
| No lifecycle/governance semantics invented | Yes | This inspection uses existing semantics only |

---

## 15. Open Questions

No material open questions remain for the inspection decision.

The evidence clearly establishes:
1. The Runtime exists and functions correctly.
2. The Agent has the capability to invoke it.
3. No operational connection currently exists between them.
4. The gap is precisely identifiable and bounded.

The inspection outcome (Outcome B) can be selected with confidence.

---

## 16. Smallest Justified Operational Boundary

The evidence justifies the following conceptual boundary:

```text
AI Agent / Execution Environment
             │
             │ request / contribution / result
             ▼
     Agent–Runtime Adapter
             │
             ├── identify/create Process Instance
             ├── obtain authoritative Execution Context
             ├── expose current authoritative situation
             ├── submit permitted contributions/results
             └── request permitted Runtime operations
             │
             ▼
          Runtime
             │
             ├── recognize
             ├── validate
             ├── mutate authoritative state
             ├── persist
             └── trace
```

### What the bridge must minimally provide

1. **Process Instance initiation:** Given an engineering objective (and optionally a repository/context), create a Process Instance through the Runtime, or discover and attach to an existing one.

2. **Execution Context presentation:** After attachment, present the authoritative Execution Context to the Agent in a form it can use for engineering decisions.

3. **Operation dispatch:** Allow the Agent to invoke Runtime operations (observe, recognize_decision, record_artifact, record_verification, begin_implementation, begin_verification, etc.) without the Agent needing to manage Python Runtime instantiation manually.

4. **Process Instance discovery:** Provide a mechanism to find an existing Process Instance by objective, repository context, or other identifying information — beyond raw UUID lookup.

### What the bridge must explicitly NOT provide

- A second state model or duplicate authoritative store
- Engineering reasoning or decision-making capability
- Transport-specific framing or protocol
- VS Code-specific integration
- Multi-agent orchestration
- Authentication or authorization beyond what AESM already specifies
- EPM, PEM, or lifecycle semantic interpretation

### Which Runtime capabilities it would expose

All current Runtime public methods are candidates:
- `create_process()`, `attach()`, `stop()`
- `start_investigation()`, `observe()`, `recognize_decision()`
- `begin_implementation()`, `set_pending_execution()`, `record_artifact()`
- `begin_verification()`, `record_verification()`, `reconsider()`
- `recognize_engineering_completion()`
- `apply_lifecycle_determination()`

Plus read access to:
- `runtime.context` (Execution Context)
- `runtime.process_instance` (Process Instance)
- `store.history(pid)` (execution history)

### Responsibilities that remain unchanged

| Component | Unchanged responsibilities |
|---|---|
| **Agent** | Investigation, analysis, engineering work, proposing decisions, producing artifacts, running verification, reporting results |
| **Runtime** | Recognition, validation, state mutation, persistence, traceability, lifecycle control, execution governance |
| **Execution Environment** | Tool provision, file access, Python execution, user interaction, session management |
| **Human** | Engineering intent, authorization, acceptance, decisions requiring human authority |

---

## 17. Implementation Decision Boundary

### Exact operational gap

The AESM Runtime exists as a functional Python library with correct authoritative state management, but **no mechanism connects Agent engineering activity to Runtime operations.** The Agent and Runtime are two disconnected components in the same repository.

### Minimum bridge capability justified

A thin, transport-independent adapter that:
1. Creates or discovers Process Instances
2. Loads and presents authoritative Execution Context to the Agent
3. Dispatches Agent contributions to Runtime operations
4. Returns Runtime state to the Agent

### Capabilities explicitly outside the bridge

- Engineering reasoning (Agent responsibility)
- State management beyond Runtime delegation (Runtime responsibility)
- Transport selection (implementation convenience, not architecture)
- EPM/PEM semantic interpretation (specification responsibility)

### Runtime responsibilities unchanged

All Runtime methods, guards, recognition requirements, persistence behavior, rollback behavior, lifecycle control, and traceability remain exactly as implemented. The bridge does not modify, extend, or duplicate any Runtime capability.

### Agent responsibilities unchanged

The Agent continues to perform investigation, analysis, engineering work, and verification. The bridge allows the Agent to submit its contributions to the Runtime rather than leaving them in conversation memory.

### Execution Environment responsibilities unchanged

The Execution Environment continues to provide tools, file access, and user interaction. The bridge may use Execution Environment capabilities (e.g., Python execution, MCP, skills, instructions) but does not redefine what the Execution Environment provides.

### What evidence authorizes a future implementation task

1. **Freshly demonstrated:** The Agent can invoke the Runtime programmatically (Process Instance creation, attachment, recovery).
2. **Freshly demonstrated:** All 88 Runtime tests pass, confirming the Runtime is a stable foundation.
3. **Freshly observed:** No operational connection exists between Agent activity and Runtime operations.
4. **Established by specification:** AESM requires Process Instance authority and Execution Context authority to be operational, not merely documented.
5. **Established by specification:** Conversation history must not be the continuity authority.

### Implementation questions deliberately unresolved

1. **Transport mechanism.** Whether the bridge is delivered as an MCP server, CLI adapter, Agent skill, instruction set, or Python script is not determined by this inspection. The next task (Environment Mechanism Mapping) should determine this.

2. **Discovery mechanism.** How Process Instance discovery maps engineering objectives to UUIDs is not designed here. Options include a simple index file, a metadata store, or repository-level markers.

3. **Context presentation format.** Whether the Execution Context is presented as structured JSON, markdown, or another format depends on the Agent environment and is not determined here.

4. **Automation level.** Whether Process Instance creation is automatic (triggered by instructions) or explicit (Agent invokes a tool) is a design decision for the implementation task.

---

## 18. Conclusion

### Status

`Complete`

### AESM participation today

**Not Demonstrated**

The AESM Runtime exists and functions correctly. The Agent can read AESM documentation. But when a human gives this Agent a real engineering request (e.g., the DBP `Add_Review_Form` change), no Process Instance is created, no Execution Context is established, no Agent contribution reaches the Runtime, and continuity depends on conversation history. Reading AESM documentation is not AESM execution participation.

### Strongest evidence

1. **Positive:** The Agent freshly demonstrated programmatic Runtime invocation — Process Instance creation, detachment, and recovery through a new Runtime instance all succeeded.
2. **Negative:** No mechanism currently causes this to happen during real engineering work. The Runtime sits dormant while the Agent performs engineering tasks following only repository instructions.

### Current gap

The smallest operational gap: **no mechanism connects Agent engineering activity to AESM Runtime operations.** The Runtime is a functioning library that the Agent can invoke but does not invoke.

### Minimum boundary

A thin, transport-independent Agent–Runtime adapter that:
1. Creates or discovers Process Instances
2. Presents authoritative Execution Context to the Agent
3. Dispatches Agent contributions to Runtime operations
4. Returns updated state to the Agent

### Transport decision

`No transport selected`

The inspection does not make any transport mechanism normative. The bridge must be conceptually transport-independent. The Environment Mechanism Mapping task should evaluate available mechanisms (MCP, skills, CLI, instructions) against the bridge requirements.

### Runtime changes

`None`

### DBP changes

`None`

### Semantic/model changes

`None`

No AESM, EPM, or PEM specification inconsistency was discovered during this inspection.

### Inspection outcome

**Outcome B — Thin Agent–Runtime Bridge Justified**

### Next authorized work

The next authorized work is **Environment Mechanism Mapping**, followed by a separately authorized bridge implementation-design task. Do not implement the bridge as part of this inspection.

---

## Appendix A: Test Execution Record

**Freshly executed** during this inspection on 2026-09-14:

```
$ .venv/bin/python -m pytest -v --tb=short
88 passed in 0.87s
Python 3.13.5, pytest, macOS (darwin)
```

All 88 tests across all test directories passed:
- `tests/continuity/test_runtime_recovery.py` — 12 passed
- `tests/lifecycle/test_process_instance_lifecycle_control.py` — 16 passed
- `tests/lifecycle/test_runtime_lifecycle.py` — 7 passed
- `tests/recording/test_runtime_recording.py` — 53 passed

**Freshly executed** Runtime invocability test:

```
$ .venv/bin/python -c "from runtime.core import ProcessStore, Runtime; ..."
Process Instance created: 0726e527-4def-434e-ba47-f4f832f24f39
Context state: initial
Lifecycle: active
Recovered objective: Inspection test objective
Recovered state: initial
Agent CAN invoke Runtime programmatically in this environment.
```

## Appendix B: Evidence Classification Summary

| Finding | Classification |
|---|---|
| Runtime implementation correctness | **Conformant — Demonstrated** |
| Process Instance persistence and recovery | **Conformant — Demonstrated** |
| Execution Context persistence and recovery | **Conformant — Demonstrated** |
| Lifecycle control | **Conformant — Demonstrated** |
| Recording operations with rollback | **Conformant — Demonstrated** |
| Cross-process continuity | **Conformant — Demonstrated** |
| Agent code execution capability | **Conformant — Demonstrated** |
| Agent → Runtime operational connection | **Implementation Gap — Semantically Required** |
| Process Instance creation from engineering request | **Implementation Gap — Semantically Required** |
| Process Instance discovery (non-UUID) | **Implementation Gap — Semantically Required** |
| Execution Context presentation to Agent | **Implementation Gap — Semantically Required** |
| Continuity without conversation history | **Implementation Gap — Semantically Required** |
| Environment independence | **Conformant — Demonstrated** |
