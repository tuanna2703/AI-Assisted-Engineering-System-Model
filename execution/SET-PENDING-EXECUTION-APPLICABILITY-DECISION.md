# `set_pending_execution` Applicability Decision

**Date:** 2026-09-16  
**Status:** Decision Record — Authoritative  
**Scope:** Agent–Runtime Bridge applicability only  
**Implementation status:** No implementation change authorized by this record

---

## 1. Decision Question

Determine whether `Runtime.set_pending_execution()` is:

- **Outside Bridge Boundary — Intentional**;
- **Required Bridge Capability — Implementation Gap**; or
- **Applicability/Specification Decision Required**.

The specific question is:

> Is recording pending execution an Agent-facing engineering contribution that belongs on the Agent–Runtime Bridge, or is it Runtime-internal execution-state management?

This decision is intentionally separate from the already-established `reconsider` bridge implementation gap.

---

## 2. Governing Sources

The decision is based on the current repository semantics and the established bridge boundary, including:

- `docs/04-Execution-Model.md` — PEM execution semantics;
- `docs/05-Process-Instance-and-Execution-Context.md` — authoritative Execution Context and continuity state;
- `docs/06-Participants-and-Agent-Participation.md` — Agent capabilities and authority boundary;
- `docs/07-Runtime-and-Conformance.md` — Runtime responsibilities and mutation boundary;
- `docs/08-Continuity-Traceability-and-Reconsideration.md` — continuity and reconsideration semantics;
- `docs/13-Runtime-Implementer-Guide.md` — Runtime responsibility and Agent boundary;
- `execution/AGENT-RUNTIME-BRIDGE-CONTRACT.md` — accepted bridge responsibilities and non-responsibilities;
- `execution/BRIDGE-BOUNDARY-DECISION.md` — established bridge boundary and prior unresolved classification;
- `bridge/agent_runtime_bridge.py` — current bridge dispatch surface;
- `runtime/core/runtime.py` — concrete `set_pending_execution()` behavior.

---

## 3. Semantic Analysis

### 3.1 What `set_pending_execution` does

`Runtime.set_pending_execution(work)`:

1. requires an attached Process Instance;
2. requires an active Process Instance lifecycle;
3. requires the `implementation` Process State;
4. appends `work` to `ExecutionContext.pending_execution`;
5. persists the resulting context and a `pending_execution_recorded` history event.

It does not itself create an engineering artifact, recognize an Engineering Decision, perform verification, or change the EPM Process State.

The operation therefore mutates **authoritative continuation/execution state**.

### 3.2 Meaning of pending execution

The Execution Context specification defines `pending execution activity`, its status, and the next expected action as continuity state. It explicitly treats continuation information as authoritative state used by resumed execution, not as an imperative instruction to replay a previous Runtime operation.

PEM execution semantics likewise identify pending work as part of the authoritative operational state updated by execution.

Therefore, pending execution is primarily an **execution-state representation** rather than an independent engineering conclusion.

### 3.3 Runtime ownership

The Runtime is explicitly responsible for:

- maintaining and recovering authoritative Execution Context;
- evaluating the current executable situation;
- applying permitted state mutations;
- preserving pending work;
- preserving continuity information.

This establishes the Runtime as the semantic owner of the authoritative `pending_execution` state.

The Runtime also uses this state in execution governance. In the current implementation, `begin_verification()` rejects progression while `pending_execution` is non-empty. Consequently, creation of a pending-execution entry can affect whether the Runtime permits progression to verification.

That makes `set_pending_execution` more than passive record storage: it participates in execution control.

### 3.4 Agent contribution remains distinct

The Agent may:

- perform authorized engineering work;
- propose plans and actions;
- create or modify artifacts;
- report execution results;
- identify contradictions and uncertainty;
- challenge previous conclusions;
- identify conditions requiring reconsideration.

The Agent does not own the authoritative Execution Context and its output does not become authoritative state merely by being produced.

The semantic contribution path is explicitly Runtime-controlled:

```text
Agent / Participant
        ↓
Observation / Participant Input / Candidate Contribution
        ↓
Runtime-controlled recognition
        ↓
Applicable EPM / PEM conditions
        ↓
Permitted State Mutation
        ↓
Execution Context / Trace
```

Therefore, an Agent may provide information from which remaining work can be recognized, but this does not establish a requirement for the Agent to directly mutate `pending_execution`.

### 3.5 Bridge boundary test

The established bridge criterion is that a Runtime operation belongs on the bridge when it represents an **Agent-authorized engineering-participation activity**.

`set_pending_execution` does not satisfy that criterion.

It directly mutates Runtime-owned continuity/execution-governance state. The Agent's authorized engineering role does not include independent authority to decide that a particular entry must become authoritative pending execution state.

The Runtime may derive or record pending work from recognized Agent contributions, execution results, evaluation, or other applicable execution information. That remains a Runtime responsibility regardless of where the originating information came from.

### 3.6 Separation test

Exposing `set_pending_execution` directly to the Agent would weaken the established separation between:

- Agent engineering participation; and
- Runtime execution-state governance.

It would allow the Agent-facing surface to directly create authoritative execution state that affects progression guards, without establishing that the Agent owns that execution-governance authority.

The fact that the method has Runtime guards does not change the semantic ownership of the resulting state.

The bridge should not expose a Runtime capability merely because the Runtime already implements it.

### 3.7 Continuity does not imply Agent control

Pending execution must survive applicable interruptions and support continuation. That requirement establishes the importance and persistence of the state; it does not establish who should directly mutate it.

Similarly, the fact that an Agent can identify unfinished engineering work does not mean that the Agent must directly write the corresponding continuation-state representation.

The semantic distinction is:

```text
Agent identifies / reports remaining work
        ≠
Agent owns pending-execution state

Runtime recognizes and records authoritative continuation state
        =
Runtime execution-state responsibility
```

### 3.8 Specification sufficiency

The prior boundary record correctly identified an ambiguity because the bridge contract did not explicitly name `set_pending_execution`.

The broader governing semantics now provide the missing distinction:

- Execution Context is Runtime-authoritative operational state;
- pending execution is explicitly continuity/execution state;
- Runtime responsibility includes preserving pending work and applying permitted state mutations;
- Agent output does not automatically become authoritative state;
- bridge membership is limited to Agent-authorized engineering-participation activities.

The specification therefore provides sufficient semantic basis for classification without requiring a new Runtime API or a change to the normative model.

The remaining implementation question is not whether pending execution exists—it clearly does—but whether direct Agent authority to mutate that state is required. The current semantics do not establish such Agent authority.

---

## 4. Decision

### **Outside Bridge Boundary — Intentional**

`set_pending_execution` is **not an Agent-facing bridge capability**.

It is a Runtime-owned execution-state management operation that records authoritative continuation work in the Execution Context and participates in execution governance.

The Agent may identify, propose, or report remaining work through the normal controlled contribution path. The Runtime remains responsible for recognizing applicable information and recording authoritative pending execution state.

No direct Agent-to-`set_pending_execution` bridge operation is required by the current AESM semantics.

---

## 5. Decision Rationale

The classification follows four independent findings:

1. **State ownership** — `pending_execution` is part of authoritative Execution Context continuity state.
2. **Execution authority** — the Runtime owns authoritative state mutation and preservation of pending work.
3. **Agent boundary** — Agent participation permits engineering contributions and reporting, but does not transfer ownership of the authoritative Execution Context.
4. **Bridge criterion** — the bridge exposes Agent-authorized engineering-participation activities, not Runtime-internal execution-state management.

The operation is therefore excluded for semantic reasons, not merely because the current bridge implementation happens not to expose it.

---

## 6. Consequences

### Bridge

No `set_pending_execution` dispatch entry should be added to `bridge/agent_runtime_bridge.py`.

Its continued absence is intentional and should not be reported as an implementation gap.

### Runtime

No Runtime change is required by this decision.

The existing Runtime responsibility to preserve and manage pending execution remains unchanged.

### Agent participation

The Agent may still communicate unfinished work or execution results through the supported Agent contribution path. Such information remains subject to Runtime recognition and applicable EPM/PEM conditions before authoritative state mutation.

This decision does **not** prohibit an Agent from reporting remaining work. It only establishes that direct mutation of `ExecutionContext.pending_execution` is not an Agent bridge capability.

### Reconsideration

The `reconsider` finding remains unchanged:

> `reconsider` is a **Required Bridge Capability — Implementation Gap**.

That capability must be handled by its own subsequent implementation work unit.

---

## 7. Non-Actions

This decision work unit makes no implementation changes.

Specifically:

- no bridge code was changed;
- no Runtime code was changed;
- no bridge tests were changed;
- no Runtime tests were changed;
- no lifecycle semantics were changed;
- no `reconsider` implementation was performed;
- no Agent/Execution Environment Participation Validation was performed;
- no DBP execution was performed.

---

## 8. Final Boundary State

The relevant bridge boundary is now:

| Runtime operation | Classification |
|---|---|
| `apply_lifecycle_determination` | Outside Bridge Boundary — Intentional |
| `set_pending_execution` | **Outside Bridge Boundary — Intentional** |
| `reconsider` | Required Bridge Capability — Implementation Gap |
| `stop` | Outside Bridge Boundary — Intentional |

The previously unresolved `set_pending_execution` applicability question is therefore closed.

The next controlled work unit may proceed to the separately established **`reconsider` Bridge Implementation** without bundling any `set_pending_execution` implementation work.

---

## 9. Completion Gate

- [x] Execution Context semantics inspected.
- [x] Continuity semantics inspected.
- [x] Agent contribution and authority semantics inspected.
- [x] Runtime ownership and mutation semantics inspected.
- [x] Established bridge boundary inspected.
- [x] Concrete Runtime behavior inspected.
- [x] `set_pending_execution` ownership determined.
- [x] Bridge applicability determined.
- [x] Specification sufficiency assessed.
- [x] Decision recorded explicitly.
- [x] No implementation change made.
- [x] `reconsider` remains a separate implementation work unit.
- [x] DBP execution remains deferred.
