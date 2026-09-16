# Bridge Boundary Decision

**Date:** 2026-09-15
**Status:** Decision Record — Authoritative
**Origin:** [BRIDGE-BEHAVIORAL-VALIDATION.md](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/BRIDGE-BEHAVIORAL-VALIDATION.md), Finding #40 — **Decision Required** on dispatch table completeness

---

## 1. Decision Context

The Bridge Behavioral Validation (Section 12.5, Finding #40) identified one genuine **Decision Required** finding:

> Whether the current Agent–Runtime Bridge dispatch surface is intentionally limited to the eight currently exposed Runtime operations, or whether additional Runtime operations must be exposed through the bridge.

The four Runtime operations currently absent from the bridge dispatch table are:

| # | Operation | Runtime Source Location |
|---|---|---|
| 1 | `apply_lifecycle_determination` | [`runtime.py:200–296`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L200-L296) |
| 2 | `set_pending_execution` | [`runtime.py:118–124`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L118-L124) |
| 3 | `reconsider` | [`runtime.py:175–185`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L175-L185) |
| 4 | `stop` | [`runtime.py:300–303`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L300-L303) |

This decision record resolves whether each operation belongs inside the accepted Agent–Runtime Bridge boundary.

---

## 2. Boundary Evidence Summary

### 2.1 Current Accepted Bridge Purpose

Source: [AGENT-RUNTIME-BRIDGE-CONTRACT.md §3](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/AGENT-RUNTIME-BRIDGE-CONTRACT.md) and [BRIDGE-IMPLEMENTATION-AUTHORIZATION-DECISION.md](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/BRIDGE-IMPLEMENTATION-AUTHORIZATION-DECISION.md).

> The Agent–Runtime Bridge is a thin, mechanism-neutral adapter between the Agent/Execution Environment and AESM Runtime capabilities. Its accepted purpose is to expose Process Instance creation, known-ID Process Instance recovery, authoritative Execution Context access, and dispatch of Runtime operations that have already been accepted as part of the bridge surface. The bridge does not independently define engineering semantics, replace PEM governance, or grant the Agent unrestricted access to Runtime internals. Runtime capabilities existing in the implementation are not automatically bridge capabilities.

**Verification against repository:** The bridge contract (§3) defines bridge responsibility as: (1) Process Instance access, (2) Execution Context access, (3) Runtime dispatch, (4) authoritative result/state return. The contract states the bridge "must not own Process Instance identity, Execution Context semantics, persistence, lifecycle authority, engineering semantics, or generalized Agent orchestration" (§3). The authorization decision confirms "the accepted bridge remains limited to" these four responsibilities (§2). The bridge contract §5.4 describes dispatch as routing to "an existing supported Runtime operation" — it does not enumerate specific dispatch operations; it describes the dispatch mechanism generically.

**Contradiction check:** The contract §5.4 describes dispatch of "already-supported Runtime operations" without qualifying which Runtime operations are in scope and which are excluded. The authorization decision lists "Runtime dispatch of already-supported Runtime operations" similarly without an explicit inclusion/exclusion list. Neither document independently resolves which of the 12 Runtime operations constitute the bridge dispatch surface. This is the ambiguity that produced the validation finding.

However, the contract §12 states the bridge does not "implement lifecycle semantics independently." This is a boundary constraint relevant to `apply_lifecycle_determination`. The contract §3 states the bridge does not "own ... lifecycle authority."

### 2.2 Currently Exposed Bridge Capabilities

Source: [agent_runtime_bridge.py](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/bridge/agent_runtime_bridge.py) `_DISPATCH_TABLE` (lines 33–45).

| # | Bridge Operation | Runtime Method |
|---|---|---|
| 1 | `start_investigation` | `Runtime.start_investigation()` |
| 2 | `observe` | `Runtime.observe(observation)` |
| 3 | `recognize_decision` | `Runtime.recognize_decision(decision, recognition)` |
| 4 | `begin_implementation` | `Runtime.begin_implementation()` |
| 5 | `record_artifact` | `Runtime.record_artifact(artifact)` |
| 6 | `begin_verification` | `Runtime.begin_verification()` |
| 7 | `record_verification` | `Runtime.record_verification(result)` |
| 8 | `recognize_engineering_completion` | `Runtime.recognize_engineering_completion(completion)` |

Plus the non-dispatch bridge operations: `create_process`, `attach`, `get_context`, `discover` (deferred).

### 2.3 Agent Responsibilities Relevant to the Bridge

Source: [06-Participants-and-Agent-Participation.md](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/06-Participants-and-Agent-Participation.md).

The Agent may: inspect Execution Context; perform investigation; contribute evidence candidates; propose engineering decisions; create/modify artifacts; perform verification; report execution results; challenge earlier conclusions; request clarification; identify conditions requiring reconsideration.

The Agent may **not**: redefine EPM/PEM semantics; bypass Decision Gates; convert proposals into authoritative decisions by assertion; own authoritative Execution Context; fabricate evidence; erase material history; directly control lifecycle state.

Key invariants: `Agent ≠ Runtime`, `Agent capability ≠ authority`, `Agent output ≠ automatic authority`.

### 2.4 Runtime Responsibilities Relevant to the Bridge

Source: [07-Runtime-and-Conformance.md](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/07-Runtime-and-Conformance.md).

The Runtime: discovers/establishes/recovers Process Instances; maintains authoritative Execution Context; evaluates the executable situation; recognizes information under EPM/PEM semantics; evaluates Process State transitions; handles Decision Gates; makes Execution Determinations; applies permitted state mutations; preserves pending work; supports reconsideration; supports suspension, resumption, recovery, and termination.

### 2.5 Execution Environment Responsibilities

Source: [AGENT-RUNTIME-BRIDGE-CONTRACT.md §4](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/AGENT-RUNTIME-BRIDGE-CONTRACT.md).

The Execution Environment: hosts the Agent and bridge mechanism; provides access/capabilities used by the Runtime; is a mechanism provider, not a semantic owner.

### 2.6 Relevant EPM/PEM Semantics

Source: [03-Engineering-Model.md](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/03-Engineering-Model.md), [04-Execution-Model.md](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/04-Execution-Model.md), [08-Continuity-Traceability-and-Reconsideration.md](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/08-Continuity-Traceability-and-Reconsideration.md), [11-Applicable-Process-Instance-Lifecycle-Semantics.md](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/11-Applicable-Process-Instance-Lifecycle-Semantics.md), [14-Lifecycle-Semantic-Decision-Record.md](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/archive/14-Lifecycle-Semantic-Decision-Record.md).

- **Lifecycle authority** is separate from technical mutation capability (Decision L-05, L-11). Lifecycle transitions require authorization by applicable execution semantics.
- **Reconsideration** is an AESM engineering concept (EPM §Reconsideration, PEM §Verification) triggered by new evidence, failed verification, changed constraints. It is part of the iterative engineering flow.
- **Pending execution** is continuity state (`pending_execution` in Execution Context). It records continuation work — not an Agent-facing engineering action but operational state management.
- **Suspension and termination** are governed by applicable execution semantics, not Agent request alone (Decision L-04, L-05, L-10, L-11).
- **AESM does not prescribe lifecycle APIs** (`suspend()`, `resume()`, `terminate()`) — Decision L-explicit non-decisions. The Lifecycle Semantic Decision Record §Explicit non-decisions states: "This record does not establish... a requirement that Participants or Agents directly control lifecycle state."

### 2.7 Authoritative Sources

| Source | Type | Relevance |
|---|---|---|
| [`AGENT-RUNTIME-BRIDGE-CONTRACT.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/AGENT-RUNTIME-BRIDGE-CONTRACT.md) | Accepted decision (contract) | Bridge boundary, responsibilities, non-responsibilities |
| [`BRIDGE-IMPLEMENTATION-AUTHORIZATION-DECISION.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/archive/BRIDGE-IMPLEMENTATION-AUTHORIZATION-DECISION.md) | Accepted decision (authorization) | What was authorized/accepted for the bridge |
| [`BRIDGE-BEHAVIORAL-VALIDATION.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/archive/BRIDGE-BEHAVIORAL-VALIDATION.md) | Validation evidence | Current bridge dispatch table, the finding under analysis |
| [`agent_runtime_bridge.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/bridge/agent_runtime_bridge.py) | Implementation evidence | Current bridge dispatch table |
| [`runtime.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py) | Implementation evidence | Runtime operations under analysis |
| [`04-Execution-Model.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/04-Execution-Model.md) | Normative specification | PEM lifecycle, reconsideration, suspension/resumption semantics |
| [`05-Process-Instance-and-Execution-Context.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/05-Process-Instance-and-Execution-Context.md) | Normative specification | Process Instance identity, Execution Context authority |
| [`06-Participants-and-Agent-Participation.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/06-Participants-and-Agent-Participation.md) | Normative specification | Agent boundary, capabilities, non-authorities |
| [`07-Runtime-and-Conformance.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/07-Runtime-and-Conformance.md) | Normative specification | Runtime responsibilities, lifecycle, conformance |
| [`08-Continuity-Traceability-and-Reconsideration.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/08-Continuity-Traceability-and-Reconsideration.md) | Normative specification | Reconsideration semantics, suspension/resumption |
| [`14-Lifecycle-Semantic-Decision-Record.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/archive/14-Lifecycle-Semantic-Decision-Record.md) | Accepted decision | Lifecycle semantic decisions L-01 through L-17 |
| [`11-Applicable-Process-Instance-Lifecycle-Semantics.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/11-Applicable-Process-Instance-Lifecycle-Semantics.md) | Normative specification | Applicable lifecycle semantics, authority, conformance |
| [`03-Engineering-Model.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/03-Engineering-Model.md) | Normative specification | EPM reconsideration, verification, completion |

### 2.8 Contradictions and Unresolved Boundary Statements

**Identified contradiction:** The bridge contract §5.4 describes dispatch of "already-supported Runtime operations" without qualification. Read literally, this could include all 12 Runtime operations. However, the contract §12 explicitly states the bridge does not "implement lifecycle semantics independently" and §3 denies "lifecycle authority." These constraints would exclude operations that transfer lifecycle authority to the Agent.

**Resolution approach:** The contract §5.4 cannot be read in isolation. The bridge's non-responsibilities in §12 and the Actor/Authority table in §4 constrain which "already-supported Runtime operations" are within the dispatch boundary. The dispatch boundary is not "all Runtime methods" but rather "Runtime operations whose dispatch through the bridge is consistent with the bridge's role as an adapter that does not assume lifecycle authority, engineering semantics ownership, or Runtime control."

---

## 3. Operation-by-Operation Analysis

### 3.1 `apply_lifecycle_determination`

#### Semantic Responsibility

This operation applies an authoritative lifecycle-state transition (ACTIVE↔SUSPENDED, ACTIVE/SUSPENDED→TERMINATED) to a Process Instance. Inspecting the implementation ([runtime.py:200–296](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L200-L296)):

- Requires a `determination` dict with: `target_process_instance_id`, `requested_transition`, `semantic_basis`, `authority_context`, `actor`, `evidence`, `occurred_at`.
- Validates that `authority_context == "authorized-controller"`.
- Validates the transition against the lifecycle transition graph.
- Validates resumption preconditions (suspension condition cessation).
- Applies stale-work invalidation during resumption.
- Persists the lifecycle event via `store.save_lifecycle()`.

This is the **authoritative lifecycle-control operation** — the mechanism by which Process Instance lifecycle state (ACTIVE, SUSPENDED, TERMINATED) is authoritatively mutated.

#### Authority

**Lifecycle authority belongs to applicable execution semantics, not to the Agent.**

- Decision L-05: "A Participant, Agent, external system, or other actor may **request or propose** suspension where applicable semantics permit. The Runtime recognizes the request, evaluates authority and applicable conditions, and mutates authoritative lifecycle state only when permitted."
- Decision L-11: "Termination must be authorized by applicable execution semantics. An actor may **request** termination, but the request becomes authoritative only when authority and execution conditions permit it."
- Lifecycle Specification §Authority: "A Participant, Agent, external system, or other actor may request or propose a lifecycle transition where applicable semantics permit such a request. The Runtime must evaluate authority and conditions before applying the authoritative lifecycle mutation."
- Decision L-explicit non-decisions: "This record does not establish... a requirement that Participants or Agents directly control lifecycle state."

The operation itself requires `authority_context == "authorized-controller"`. This authority gate is not Agent authority — it represents an authorized controller of lifecycle state, which is a distinct authority from Agent participation.

**Owning actor/layer:** Runtime / applicable execution semantics. The Agent may *request* lifecycle transitions, but the determination and application of lifecycle state is a Runtime/governance responsibility.

#### Existing AESM Meaning

- [04-Execution-Model.md §Process Instance lifecycle semantics](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/04-Execution-Model.md): Lifecycle transitions are governed by applicable execution semantics; AESM does not prescribe lifecycle APIs.
- [11-Applicable-Process-Instance-Lifecycle-Semantics.md §Authority](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/11-Applicable-Process-Instance-Lifecycle-Semantics.md): Lifecycle authority is separate from technical mutation capability. Request ≠ authorization ≠ Runtime mutation.
- [14-Lifecycle-Semantic-Decision-Record.md §L-05, L-11](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/archive/14-Lifecycle-Semantic-Decision-Record.md): Agents may request but do not directly control lifecycle state.

#### Bridge Boundary Test

> Does the Agent need this capability through the bridge in order to exercise an AESM responsibility that the Agent is actually authorized to perform?

**No.** The Agent is not authorized to directly apply lifecycle determinations. The Agent may *request* a lifecycle transition, but the authoritative determination and application is a Runtime/governance function requiring `authorized-controller` authority. The eight currently exposed operations cover the Agent's authorized engineering participation activities (investigation, observation, decision recognition, implementation, artifact recording, verification, completion recognition). Lifecycle control is a separate semantic dimension from engineering participation.

#### Separation Test

Exposing `apply_lifecycle_determination` through the bridge would **collapse** the AESM separation between Agent participation and lifecycle governance. It would give the Agent direct mutation authority over Process Instance lifecycle state — precisely the authority that Decisions L-05 and L-11 deny to Agents as Agents.

Even though the operation has an `authority_context` guard, routing it through the Agent bridge implies that the Agent is the expected caller with lifecycle control authority. This conflates the Agent's engineering participation role with lifecycle governance authority.

#### Absence Test

The current absence is **intentionally outside the bridge boundary**. The bridge contract §12 states the bridge does not "implement lifecycle semantics independently." The bridge contract §3 denies lifecycle authority to the bridge. The lifecycle semantic decisions explicitly do not establish Agent lifecycle control. The bridge's dispatch table correctly excludes lifecycle governance operations from the Agent-facing surface.

#### Classification: **Outside Bridge Boundary — Intentional**

---

### 3.2 `set_pending_execution`

#### Semantic Responsibility

This operation records continuation work in the `pending_execution` list without changing Process State. Inspecting the implementation ([runtime.py:118–124](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L118-L124)):

- Requires attachment, active lifecycle, and `implementation` process state.
- Appends a `work` dict to `context.pending_execution`.
- Persists the context with a `pending_execution_recorded` history event.

Semantically, pending execution represents **continuation work** — a record of what execution activity remains to be performed. It is part of the Execution Context continuity state.

#### Authority

Pending execution is described in the Execution Context specification ([05-Process-Instance-and-Execution-Context.md §Continuity state](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/05-Process-Instance-and-Execution-Context.md)):

> - pending execution activity
> - status of pending execution
> - next expected action

And:

> Continuation information is authoritative state used by resumed execution. It is not an imperative instruction to replay a previous Runtime operation.

The Runtime is the entity responsible for recording and managing execution state ([07-Runtime-and-Conformance.md](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/07-Runtime-and-Conformance.md) responsibility #15: "preserve pending work"). 

The Agent's role during implementation is to perform engineering work (create artifacts, perform verification). The Agent does not independently manage the Runtime's continuation state — that is an execution-governance function.

However, there is an important nuance: the Agent, during implementation, may identify work that remains to be done. Whether this identification constitutes a direct `set_pending_execution` call through the bridge, or whether it should be reported as an engineering observation that the Runtime then records, depends on where the semantic boundary is drawn.

**Owning actor/layer:** The `pending_execution` field is Execution Context state owned by the Runtime. The Agent contributes engineering work; the Runtime records the execution state. The operation is closer to Runtime execution-state management than Agent engineering participation.

#### Existing AESM Meaning

- [04-Execution-Model.md §Update Execution Context](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/04-Execution-Model.md): "Results are incorporated into authoritative operational state, including ... pending work."
- [05-Process-Instance-and-Execution-Context.md §Continuity state](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/05-Process-Instance-and-Execution-Context.md): Pending execution is continuity state, not an imperative instruction.
- [07-Runtime-and-Conformance.md](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/07-Runtime-and-Conformance.md): The Runtime preserves pending work (#15).

#### Bridge Boundary Test

> Does the Agent need this capability through the bridge in order to exercise an AESM responsibility that the Agent is actually authorized to perform?

The Agent is authorized to perform engineering work during implementation and to report results. Whether recording pending execution entries is an Agent responsibility or a Runtime-internal state-management function is not clearly established.

The eight currently exposed operations include `record_artifact` (recording implementation outputs) and all state transitions. There is no currently exposed operation for recording pending/continuation work. The Agent's bridge participation currently covers the engineering contribution path (observe → decide → implement → record → verify → complete) but not the execution-state management path (pending execution, continuation state).

The Agent may need to communicate that implementation work remains to be done, but the AESM documentation does not clearly establish whether this should be a direct bridge-dispatched operation or whether it should flow through another mechanism (e.g., the Agent's engineering output being interpreted by the Runtime).

#### Separation Test

Exposing `set_pending_execution` would be **neutral to marginally concerning** for AESM separation. The operation modifies Execution Context continuity state, which is Runtime-owned. However, the operation is guarded by the same preconditions as `record_artifact` (attached, active lifecycle, implementation state), and it records execution-relevant information without changing Process State. It does not grant lifecycle authority or engineering semantics control.

The concern is whether direct Agent mutation of the `pending_execution` list conflates the Agent's engineering role with the Runtime's execution-state management role. In the current implementation, `begin_verification` checks `if self.context.pending_execution` and rejects verification when pending work remains. This means `set_pending_execution` affects the Agent's ability to proceed to verification — it is an execution-governance mechanism, not merely a record-keeping function.

#### Absence Test

The current absence is **not clearly determined** by existing specification. The bridge contract does not explicitly include or exclude pending-execution recording. No accepted decision addresses whether the Agent should directly manage the pending-execution list.

#### Classification: **Applicability/Specification Decision Required**

---

### 3.3 `reconsider`

#### Semantic Responsibility

This operation transitions a Process Instance from `verification` back to `investigation` when verification has failed, recording the reconsideration reason. Inspecting the implementation ([runtime.py:175–185](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L175-L185)):

- Requires attachment, active lifecycle, `verification` process state.
- Requires that verification has not passed (`verification.get("passed") is True` causes rejection).
- Requires a descriptive reason.
- Appends the reason to `failure_uncertainty` and `unresolved_matters`.
- Transitions process state to `investigation` via `_set_state`.

This is an **engineering-process state transition** — the return from failed verification to investigation for reconsideration. It is part of the iterative engineering flow.

#### Authority

Reconsideration is described in EPM ([03-Engineering-Model.md §Reconsideration](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/03-Engineering-Model.md)):

> AESM supports controlled reconsideration. New Evidence, failed verification, changed constraints, discovered errors, or other material information may justify revisiting earlier Requirements, Solutions, Decisions, or implementation choices.

And in the reconsideration specification ([08-Continuity-Traceability-and-Reconsideration.md §Reconsideration](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/08-Continuity-Traceability-and-Reconsideration.md)):

> A reconsideration should: (1) identify what is being reconsidered; (2) identify the reason; (3) preserve the previous conclusion and its basis; (4) evaluate the new information; (5) establish a new conclusion through applicable EPM semantics; (6) apply controlled state changes; (7) preserve traceability.

The Agent is explicitly permitted to "challenge earlier conclusions" and to "identify conditions requiring reconsideration" ([06-Participants-and-Agent-Participation.md §What an Agent may do](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/06-Participants-and-Agent-Participation.md)).

**Owning actor/layer:** Reconsideration is part of the engineering flow. The Agent participates in the engineering flow — the Agent identifies conditions requiring reconsideration. The Runtime applies the controlled state change. The `reconsider` operation is a **process-state transition** (verification → investigation), which is analogous to the currently exposed transitions (`start_investigation`, `begin_implementation`, `begin_verification`).

#### Existing AESM Meaning

- [03-Engineering-Model.md §Reconsideration](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/03-Engineering-Model.md): Reconsideration is an explicit EPM concept.
- [08-Continuity-Traceability-and-Reconsideration.md §Reconsideration](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/08-Continuity-Traceability-and-Reconsideration.md): Detailed reconsideration semantics.
- [04-Execution-Model.md §Verification](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/04-Execution-Model.md): "Verification failure may require additional work or reconsideration."
- [03-Engineering-Model.md §Engineering flow](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/03-Engineering-Model.md): The engineering flow explicitly includes "reconsider" as a branch from progress evaluation.
- [09-Operational-Guide.md §Example](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/09-Operational-Guide.md): The operational example includes "Reconsider Solution / Decision" as part of the engineering flow after verification failure.

#### Bridge Boundary Test

> Does the Agent need this capability through the bridge in order to exercise an AESM responsibility that the Agent is actually authorized to perform?

**Yes.** The Agent is authorized to identify conditions requiring reconsideration. Reconsideration after failed verification is an integral part of the engineering flow that the Agent participates in. The bridge currently exposes all other process-state transitions in the engineering cycle: initial→investigation, investigation→implementation, implementation→verification, verification→engineering_complete. The reconsideration transition (verification→investigation after failure) is the missing return path in this cycle.

Without `reconsider` in the dispatch table, the Agent cannot complete a full engineering cycle through the bridge when verification fails. The bridge currently supports only the forward path. The backward/iterative path — which AESM explicitly supports — is absent.

#### Separation Test

Exposing `reconsider` would **preserve** AESM separation. The operation is a process-state transition analogous to the other process-state transitions already in the dispatch table. It requires Runtime guards (attached, active lifecycle, verification state, failed verification), does not grant lifecycle authority, and does not transfer engineering semantics ownership. It enables the Agent to participate in the iterative engineering flow — which is the Agent's authorized role.

#### Absence Test

The current absence is **an actual required capability missing from the implementation of the bridge dispatch table**. The Agent is authorized to participate in reconsideration. The engineering flow requires the reconsideration path. The bridge currently supports all other process-state transitions. The reconsideration transition is the only engineering-process-state transition absent from the dispatch table.

#### Classification: **Required Bridge Capability — Implementation Gap**

---

### 3.4 `stop`

#### Semantic Responsibility

This operation detaches the Runtime from the current Process Instance. Inspecting the implementation ([runtime.py:300–303](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L300-L303)):

```python
def stop(self) -> None:
    self.attached = False
    self.process_instance = None
    self.context = None
```

This is a **Runtime-internal detach operation**. It:
- Sets `attached = False`.
- Releases the in-memory references to ProcessInstance and ExecutionContext.
- Does **not** persist anything.
- Does **not** change Process Instance lifecycle state.
- Does **not** change process state.
- Does **not** constitute suspension or termination.

This is semantically equivalent to the Runtime "putting down" its in-memory reference to the Process Instance. The Process Instance continues to exist in persistent state.

#### Authority

This is a Runtime execution-control mechanism. It governs the Runtime's in-memory attachment state.

**Owning actor/layer:** Runtime internal state management. This is not a Process Instance operation, not a lifecycle operation, not an engineering operation, and not an Execution Context mutation. It is a Runtime session-management function.

#### Existing AESM Meaning

The AESM documentation establishes that:

- Runtime shutdown, restart, Agent departure, and conversation closure do not themselves constitute Process Instance suspension or termination ([04-Execution-Model.md §Lifecycle separation](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/04-Execution-Model.md)).
- Process Instance continuity survives Agent changes and Runtime restarts ([05-Process-Instance-and-Execution-Context.md §Process continuity invariant](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/05-Process-Instance-and-Execution-Context.md)).

The `stop` operation implements the transient-layer detachment. It is a Runtime operational convenience, not an AESM semantic operation.

#### Bridge Boundary Test

> Does the Agent need this capability through the bridge in order to exercise an AESM responsibility that the Agent is actually authorized to perform?

**No.** The Agent does not have an AESM responsibility that requires explicitly detaching the Runtime from a Process Instance. When the Agent stops participating:
- The bridge can be destroyed (which releases the `_runtime` reference).
- The Process Instance persists independently.
- A new bridge can reattach via `attach()`.

The bridge is explicitly "intentionally disposable" ([agent_runtime_bridge.py docstring](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/bridge/agent_runtime_bridge.py)). The behavioral validation demonstrated that bridge destruction and recreation preserves continuity (Section 8.1–8.2). The `stop` operation is a Runtime-internal convenience that the bridge does not need to expose because bridge disposal achieves the same effect.

#### Separation Test

Exposing `stop` would be **neutral** to AESM separation. The operation does not change any authoritative state. However, exposing it would add an unnecessary operation to the bridge surface — the bridge already achieves detachment through its disposable lifecycle.

#### Absence Test

The current absence is **intentionally outside the bridge boundary**. The bridge achieves detachment through its own disposable lifecycle. The `stop` operation is a Runtime-internal mechanism not needed at the Agent-facing bridge surface. Its absence does not prevent any Agent-authorized AESM activity.

#### Classification: **Outside Bridge Boundary — Intentional**

---

## 4. Decision Matrix

| Runtime operation | Semantic concern | Owning actor/layer | Agent-accessible? | Bridge boundary requires exposure? | Separation effect | Classification | Supporting evidence |
|---|---|---|---|---|---|---|---|
| `apply_lifecycle_determination` | Process Instance lifecycle-state mutation (suspend/resume/terminate) | Runtime / applicable execution semantics | Request only, not direct control | No — lifecycle authority is not an Agent bridge capability | Would collapse Agent/lifecycle-governance separation | **Outside Bridge Boundary — Intentional** | Contract §3, §12; Decisions L-05, L-11; Lifecycle spec §Authority; agent_runtime_bridge.py dispatch table |
| `set_pending_execution` | Continuation-work recording in Execution Context | Runtime / Execution Context management | Not clearly established | Not determinable from current specification | Neutral to marginally concerning — Agent would directly manage execution-governance state | **Applicability/Specification Decision Required** | EC spec §Continuity state; Runtime responsibilities #15; no explicit bridge inclusion/exclusion |
| `reconsider` | Process-state transition: verification → investigation after failed verification | Engineering flow / Agent participation + Runtime governance | Yes — Agent identifies reconsideration conditions | Yes — completes the iterative engineering cycle through the bridge | Preserves separation — analogous to existing process-state transitions | **Required Bridge Capability — Implementation Gap** | EPM §Reconsideration; PEM §Verification; Agent Guide; Operational flow; all other process-state transitions exposed |
| `stop` | Runtime in-memory detachment from Process Instance | Runtime internal state management | Not an Agent AESM responsibility | No — bridge disposal achieves the same effect | Neutral — no authoritative state change | **Outside Bridge Boundary — Intentional** | Bridge contract (disposable bridge); behavioral validation §8.1–8.2 (continuity across bridge destruction) |

---

## 5. Evidence Reconciliation

| Operation | Classification | Supporting semantic evidence | Supporting boundary/authorization evidence | Implementation consistency | Documentation consistency | Reconciliation result |
|---|---|---|---|---|---|---|
| `apply_lifecycle_determination` | Outside Bridge Boundary — Intentional | Decisions L-05, L-11: Agents request, do not control lifecycle. Lifecycle spec §Authority: request ≠ authorization ≠ mutation. Lifecycle non-decisions: no requirement for Agent lifecycle control. | Contract §3: bridge does not own lifecycle authority. Contract §12: bridge does not implement lifecycle semantics independently. | **Consistent** — implementation excludes this operation from dispatch table. | **Consistent** — bridge behavioral validation §9.1 notes "No lifecycle-related methods in bridge." Contract and authorization do not list lifecycle control as a bridge capability. | Fully reconciled — no contradictions |
| `set_pending_execution` | Applicability/Specification Decision Required | EC spec §Continuity state describes pending execution as continuation information. Runtime responsibilities #15: preserve pending work. Agent participation docs do not explicitly address pending-execution recording. | Contract §5.4 describes dispatch generically. No explicit inclusion or exclusion of `set_pending_execution`. | **Consistent with exclusion** — implementation excludes this operation. | **Consistent with ambiguity** — no document explicitly requires or excludes this operation from the bridge. | Reconciled with acknowledged ambiguity — evidence insufficient to determine bridge membership |
| `reconsider` | Required Bridge Capability — Implementation Gap | EPM §Reconsideration; PEM §Verification ("failure may require reconsideration"); Agent docs: Agent may "challenge earlier conclusions" and "identify conditions requiring reconsideration"; Operational flow includes reconsideration path. | Contract §5.4: dispatch of "already-supported Runtime operations." The operation is a supported Runtime operation. Contract does not exclude process-state transitions from dispatch. | **Inconsistent** — the implementation excludes `reconsider` while all other process-state transitions (start_investigation, begin_implementation, begin_verification, recognize_engineering_completion) are included. | **Inconsistent** — no documentation explains why reconsider is excluded while all other process-state transitions are included. | Implementation gap confirmed — engineering-cycle process-state transition missing from dispatch table |
| `stop` | Outside Bridge Boundary — Intentional | AESM: Runtime/Agent departure does not constitute lifecycle transition. Process Instance persists independently. | Bridge is explicitly disposable (docstring, behavioral validation §8). Bridge disposal releases Runtime reference without explicit `stop`. | **Consistent** — implementation excludes this operation. Bridge disposal achieves detachment. | **Consistent** — behavioral validation confirms continuity across bridge destruction. | Fully reconciled — no contradictions |

---

## 6. Uncertainty Characterization: `set_pending_execution`

### Specific Ambiguity

The precise question that cannot currently be answered:

> Is recording pending execution entries an Agent-facing engineering contribution that should be dispatched through the bridge, or is it a Runtime-internal execution-state management function that the Agent should not directly invoke?

### Conflicting Interpretations

**Interpretation A — Agent-accessible:** The Agent, during implementation, identifies work that remains to be done. Recording this work is analogous to recording artifacts (`record_artifact`) — both are engineering contributions during implementation. The Agent should be able to record pending work through the bridge, and the Runtime records it as authoritative continuation state.

**Interpretation B — Runtime-internal:** Pending execution is execution-governance state. The `pending_execution` list affects whether the Runtime permits the transition to verification (`begin_verification` rejects when `pending_execution` is non-empty). Recording pending execution is not an engineering contribution — it is execution-state management that the Runtime should perform based on its evaluation of the engineering situation, not based on direct Agent instruction.

**Interpretation C — Hybrid:** The Agent may communicate that work remains, but this communication should flow through an engineering observation or reporting mechanism, not through direct mutation of the `pending_execution` list. The Runtime would then evaluate and record the pending execution based on the Agent's report.

### Missing Evidence

To resolve this ambiguity, the following would be required:

1. A specification decision on whether `pending_execution` recording is an Agent-facing capability or a Runtime-internal function.
2. Clarification of whether the `begin_verification` guard against non-empty `pending_execution` is an execution-governance mechanism that should be managed by the Runtime alone, or whether the Agent has explicit authority over when pending execution entries are created and cleared.

### Consequences

- **If Interpretation A is adopted:** `set_pending_execution` would be added to the bridge dispatch table. The Agent would have direct authority to create entries that block verification progression.
- **If Interpretation B is adopted:** `set_pending_execution` remains outside the bridge. The Agent's engineering contributions during implementation would not directly manage continuation state.
- **If Interpretation C is adopted:** A new mechanism for Agent-to-Runtime communication of remaining work would need to be specified, distinct from direct `pending_execution` mutation.

---

## 7. AESM Separation Review

### EPM/PEM Separation

The proposed boundary preserves EPM/PEM separation:
- The bridge does not define engineering meaning (EPM responsibility).
- The bridge dispatches engineering-participation operations (process-state transitions, evidence recording, decision recognition, artifact recording, verification, completion recognition, and — once implemented — reconsideration) through PEM-governed Runtime operations.
- Lifecycle governance remains outside the bridge.

### Runtime/Execution Environment Separation

The proposed boundary preserves Runtime/Execution Environment separation:
- The bridge remains a mechanism adapter, not a semantic authority.
- The Execution Environment provides the hosting mechanism; the Runtime owns all authoritative state.
- Runtime-internal operations (`stop`) are not exposed through the Execution Environment bridge.

### Process Instance Authority

Process Instance authority is preserved:
- The bridge does not own Process Instance identity (creation via Runtime).
- Lifecycle state is not mutable through the bridge.
- All state mutations flow through Runtime guards.

### Agent/Runtime Control

The proposed boundary avoids granting the Agent unrestricted Runtime control:
- Lifecycle governance (`apply_lifecycle_determination`) is excluded.
- Runtime session management (`stop`) is excluded.
- The Agent accesses only engineering-participation operations through the bridge.
- The `set_pending_execution` ambiguity is explicitly recorded rather than silently resolved.

### Remaining Bridge Capabilities

With `reconsider` added (as a follow-up implementation), the Agent would have all bridge capabilities required for the complete iterative engineering cycle:

```
initial → investigation → implementation → verification ──→ engineering_complete
                    ↑                            │
                    └──── reconsider (gap) ───────┘
```

Plus: evidence recording, decision recognition, artifact recording, verification recording, Execution Context access, Process Instance creation and recovery.

The only unresolved question is `set_pending_execution`, which is explicitly deferred to a specification decision.

### Separation Conclusions

1. **EPM/PEM separation:** Preserved.
2. **Runtime/Execution Environment separation:** Preserved.
3. **Process Instance authority:** Preserved.
4. **Agent/unrestricted Runtime control:** Avoided.
5. **Agent bridge capabilities:** Complete for the engineering cycle, with one specification question deferred (`set_pending_execution`).

---

## 8. Accepted Boundary Statement

The accepted Agent–Runtime Bridge boundary after this analysis is:

> The Agent–Runtime Bridge is a thin, mechanism-neutral adapter between the Agent/Execution Environment and AESM Runtime capabilities. Its accepted purpose is to expose Process Instance creation, known-ID Process Instance recovery, authoritative Execution Context access, and dispatch of Runtime operations that represent the Agent's authorized engineering-participation activities. The bridge dispatch surface encompasses the complete iterative engineering-cycle process-state transitions (including reconsideration), engineering-contribution recording operations (evidence, decisions, artifacts, verification, completion), and their associated Runtime guards. The bridge does not expose lifecycle-governance operations, Runtime-internal session management, or operations whose authority belongs to actors or layers other than the Agent's engineering-participation role. Runtime capabilities existing in the implementation are not automatically bridge capabilities; inclusion in the bridge dispatch table requires that the operation represents an Agent-authorized AESM engineering-participation activity.

**Qualification against the canonical starting statement:** The starting statement is confirmed and qualified. The qualification is that "dispatch of Runtime operations that have already been accepted as part of the bridge surface" is now clarified to mean "Runtime operations that represent the Agent's authorized engineering-participation activities." This clarification resolves the contract §5.4 ambiguity by establishing the selection criterion for dispatch table membership.

---

## 9. Consequences

### Implementation Implications

- **`reconsider`**: Must be added to the bridge dispatch table as a follow-up implementation activity. This is recorded as a finding, not performed in this work unit.
- **`set_pending_execution`**: Requires a specification decision before any implementation change.
- **`apply_lifecycle_determination`** and **`stop`**: No implementation change required.

### Documentation Implications

- The bridge contract §5.4 could be clarified to specify the dispatch-inclusion criterion (Agent-authorized engineering-participation operations), but this is not required for the boundary decision to be effective.
- The behavioral validation §12.5 finding is resolved by this decision record.

### Evidence Implications

- The `reconsider` implementation gap should be tracked as a follow-up validation item after implementation.

### Unresolved Specification Implications

- `set_pending_execution` requires a specification/applicability decision on whether pending-execution recording is an Agent-facing capability or Runtime-internal function.

---

## 10. Decision Gate

**Boundary Resolved — Proceed to Resulting Implications**

Three of four operations are fully resolved:
- `apply_lifecycle_determination`: Outside Bridge Boundary — Intentional.
- `reconsider`: Required Bridge Capability — Implementation Gap.
- `stop`: Outside Bridge Boundary — Intentional.

One operation requires a follow-up specification decision:
- `set_pending_execution`: Applicability/Specification Decision Required.

The bridge boundary is sufficiently resolved to proceed to the next controlled work unit. The `set_pending_execution` specification question does not block resolution of the bridge boundary for the three resolved operations.

---

## 11. Non-Actions Confirmed

- No bridge capability was added.
- No Runtime behavior was changed.
- No DBP execution occurred.
- No Agent/Execution Environment Participation Validation was performed.
- No bridge operation was removed.
- No implementation files were modified.

---

## Completion Gate Verification

- [x] Boundary context reconstruction was completed first.
- [x] A Boundary Evidence Summary was produced (§2).
- [x] The accepted bridge boundary was explicitly established (§8).
- [x] All four operations were analyzed using the same reasoning framework (§3).
- [x] Each operation has exactly one classification (§4).
- [x] Each classification has specific supporting evidence (§4, §5).
- [x] Evidence reconciliation was performed separately from the initial analysis (§5).
- [x] Uncertainty has been explicitly characterized (§6).
- [x] AESM separation was explicitly evaluated (§7).
- [x] The final decision matrix is internally consistent (§4).
- [x] The decision record matches the final matrix (§4, §8, §9, §10).
- [x] No bridge operation was added or removed (§11).
- [x] No Runtime behavior was changed (§11).
- [x] No DBP execution occurred (§11).
- [x] No Agent/Execution Environment Participation Validation occurred (§11).
