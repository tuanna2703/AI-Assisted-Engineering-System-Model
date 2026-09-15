# Agent–Runtime Bridge Contract

## 1. Purpose and Status

This artifact determines the smallest concrete semantic contract required for an Agent–Runtime bridge using the capabilities identified by the completed Environment Mechanism Mapping.

**Status: CONTRACT DETERMINED — IMPLEMENTATION NOT AUTHORIZED BY THIS ARTIFACT.**

This is a contract-definition artifact. It does not implement the bridge, select a normative transport, modify Runtime behavior, add persistence, or change AESM semantics.

The contract preserves the established AESM separation:

- **EPM** defines what engineering work means.
- **PEM** governs how engineering execution is conducted.
- **Runtime** implements PEM and owns authoritative Process Instance / Execution Context state.
- **Execution Environment** supplies mechanisms through which the Agent can interact with the Runtime.
- **Agent** performs engineering work and requests Runtime-governed operations.
- **Process Instance / Execution Context** remain persistent Runtime-owned process state.

## 2. Evidence and Governing Sources

The contract is derived from the following evidence, in authority order:

1. Actual Runtime implementation and executable verification recorded in `execution/RUNTIME-API-INSPECTION.md`.
2. The established Agent–Runtime boundary and its reconciliation in `execution/BRIDGE-BOUNDARY-RECONCILIATION.md`.
3. The completed Execution Environment mapping in `execution/ENVIRONMENT-MECHANISM-MAPPING.md`.
4. Normative architecture and operational documents, especially `docs/07-Runtime-and-Conformance.md`, `docs/05-Process-Instance-and-Execution-Context.md`, and `docs/08-Continuity-Traceability-and-Reconsideration.md`.
5. `IMPLEMENTATION_PLAN.md` as the controlled implementation sequence.

The Runtime inspection establishes that the current Runtime supports creation, known-ID recovery, context access, and supported operation dispatch, but has no objective-to-instance discovery/search/list capability. The Environment Mechanism Mapping establishes that the current Execution Environment can host a thin adapter but currently has no active AESM Agent-to-Runtime path.

## 3. Contract Boundary

The bridge is an **adapter/access boundary**, not a new engineering-process authority.

Its complete semantic responsibility is:

1. **Process Instance access** — enable creation or Runtime-owned identification/recovery of the relevant persistent Process Instance.
2. **Execution Context access** — obtain the authoritative current Execution Context and make it available to the Agent.
3. **Runtime dispatch** — request already-supported Runtime operations on behalf of the Agent.
4. **Authoritative result/state return** — return Runtime-authoritative results and resulting state to the Agent.

The fourth responsibility is a return property of the first three interactions rather than a separate stateful operation.

The bridge must not own Process Instance identity, Execution Context semantics, persistence, lifecycle authority, engineering semantics, or generalized Agent orchestration.

## 4. Actors and Authority

| Actor | Contract role | Authority |
|---|---|---|
| Human | Supplies/approves engineering intent as applicable | Human engineering authority where PEM/EPM require it |
| Agent | Performs engineering work and requests Runtime operations | No independent authority over Runtime state |
| Bridge | Translates Agent requests to supported Runtime interactions and returns authoritative results | No independent process-state authority |
| Runtime | Executes governed operations and owns authoritative process state | Authoritative Runtime authority |
| Process Store | Persists Runtime-owned Process Instance / Execution Context state | Persistence authority under Runtime |
| Execution Environment | Hosts the Agent and bridge mechanism | Mechanism provider, not semantic owner |

## 5. Minimal Contract Surface

The smallest useful bridge-facing semantic surface is four capabilities. These names describe contract capabilities; they are not normative requirements for a particular class, CLI command, MCP tool, or transport.

### 5.1 Create Process Instance

**Capability:** create a new Runtime-owned Process Instance for an engineering objective.

**Input:**

- `objective: string`

**Runtime action:** delegate to the existing `Runtime.create_process(objective)` capability.

**Output:**

- authoritative `process_instance_id`;
- authoritative `ProcessInstance` state as available from the Runtime;
- authoritative `ExecutionContext` state associated with the created instance;
- operation outcome/error information.

**Authority rule:** the Runtime generates and owns the Process Instance identity. The bridge must not generate a competing identifier.

### 5.2 Access Existing Process Instance

**Capability:** recover an existing Runtime-owned Process Instance when its authoritative identifier is already known.

**Input:**

- `process_instance_id: string`

**Runtime action:** delegate to existing `Runtime.attach(process_instance_id)`.

**Output:**

- authoritative recovered `ProcessInstance` state;
- authoritative `ExecutionContext` state;
- operation outcome/error information.

**Authority rule:** the supplied identifier is only a reference. The Runtime validates and resolves it. The bridge must not reconstruct state from conversation history or maintain a parallel authoritative copy.

### 5.3 Access Execution Context

**Capability:** obtain the authoritative current Execution Context for the attached Process Instance.

**Input:**

- active Process Instance reference within the Runtime interaction; no independent context identifier is required.

**Runtime action:** read the Runtime's authoritative context (`runtime.context`) after creation or attachment.

**Output:**

- complete authoritative Execution Context snapshot, represented without introducing a second AESM context model;
- associated Process Instance identity;
- operation outcome/error information.

**Authority rule:** returned context is a snapshot of Runtime-owned state. The bridge may serialize/present it, but must not become its owner.

### 5.4 Dispatch Supported Runtime Operation

**Capability:** request an already-supported Runtime operation without expanding Runtime semantics.

**Input:**

- `operation: string` identifying an existing supported Runtime operation;
- `params: object` containing that operation's required parameters;
- active Process Instance association where required by the Runtime.

**Runtime action:** validate the requested operation against the actual Runtime surface and delegate directly to the corresponding existing operation.

**Output:**

- operation result;
- authoritative resulting `ProcessInstance` / `ExecutionContext` state when applicable;
- Runtime validation/guard rejection where applicable;
- persistence failure or other Runtime error information where applicable.

**Authority rule:** the bridge must not simulate, bypass, reinterpret, or replace Runtime guards.

## 6. Process Instance Discovery Boundary

Process Instance discovery requires special treatment because the complete bridge boundary includes discovery while the current Runtime does not expose an objective-to-instance search operation.

### 6.1 Normative ownership

**Semantic ownership remains with the Runtime.** The bridge must not search arbitrary persisted state and declare an instance authoritative merely because it finds a matching file or objective string.

The normative model permits the Execution Environment to provide capabilities used by Runtime discovery, but those capabilities do not transfer semantic ownership of discovery away from the Runtime.

### 6.2 Current implementation dependency

The current Runtime provides:

- `create_process(objective)`;
- `attach(process_instance_id)`;
- no objective/repository/context search or list operation.

Therefore the current contract can fully specify the **creation** and **known-ID recovery** paths, but cannot claim that ordinary no-ID continuation is fully implementable today.

### 6.3 Contract treatment of no-ID requests

For an ordinary request with no Process Instance ID, the bridge contract is:

1. obtain the request objective/context from the Agent/Execution Environment;
2. invoke or rely on a **Runtime-owned discovery capability if one exists in the implementation being integrated**;
3. if Runtime discovery identifies an existing authoritative Process Instance, recover it through Runtime-owned access;
4. if Runtime discovery establishes that no relevant instance exists, create a new Process Instance through `create_process(objective)`;
5. return the authoritative identity and Context to the Agent.

The current Runtime does not satisfy step 2. This is recorded as an **implementation dependency/gap**, not as permission for the bridge to assume discovery ownership.

No new `discover()` Runtime API is mandated by this contract. The semantic requirement is Runtime ownership of discovery; its eventual mechanism remains an implementation/design decision subject to separate authorization.

## 7. Agent-to-Runtime Interaction Flows

### 7.1 New request with no known Process Instance

```text
Human request
  ↓
Agent receives objective and applicable environment guidance
  ↓
Bridge receives request context
  ↓
Runtime-owned discovery is attempted when available
  ├─ matching instance → Runtime access/recovery
  └─ no matching instance → Runtime create_process(objective)
  ↓
Bridge returns authoritative Process Instance + Execution Context
  ↓
Agent performs engineering work
  ↓
Agent requests supported Runtime operations through bridge
  ↓
Runtime validates, persists, and returns authoritative result/state
```

**Current limitation:** the existing Runtime lacks the discovery capability shown in the first branch. The creation path remains directly implementable.

### 7.2 Continuation with known Process Instance

```text
Agent has Process Instance ID
  ↓
Bridge access-existing-process
  ↓
Runtime.attach(process_instance_id)
  ↓
Runtime loads authoritative Process Instance + Execution Context
  ↓
Bridge returns state to Agent
  ↓
Agent continues engineering work
```

This flow is directly supported by the current Runtime.

### 7.3 Context access during execution

```text
Bridge request
  ↓
Runtime authoritative context access
  ↓
Context snapshot
  ↓
Bridge
  ↓
Agent
```

The bridge does not cache or mutate an independent authoritative context.

### 7.4 Runtime operation dispatch

```text
Agent requests supported operation + parameters
  ↓
Bridge validates only contract shape / routing needs
  ↓
Runtime operation
  ↓
Runtime guard + mutation + persistence
  ↓
Authoritative result/state
  ↓
Bridge
  ↓
Agent
```

The bridge is not permitted to reproduce Runtime guards in a way that creates a second authority. It may perform transport/input-shape validation, while Runtime remains authoritative for semantic validation.

## 8. Request and Response Semantics

A bridge interaction must preserve the following information categories.

### Agent → Bridge

- engineering objective/request where applicable;
- known Process Instance reference when available;
- requested capability/Runtime operation;
- operation parameters;
- sufficient request context for the selected environment mechanism.

### Bridge → Runtime

- create request with objective; or
- known Process Instance identifier for access; or
- Runtime context request; or
- supported Runtime operation plus parameters.

### Runtime → Bridge

- authoritative Process Instance identity;
- authoritative Process Instance state;
- authoritative Execution Context snapshot;
- operation result;
- guard/validation rejection;
- persistence or recovery error;
- other Runtime-defined failure information.

### Bridge → Agent

- authoritative Process Instance identity/state;
- authoritative current Execution Context;
- Runtime operation result;
- actionable Runtime failure/rejection information;
- explicit indication when a capability is unavailable rather than fabricated success.

## 9. Error and Authority Semantics

The bridge must preserve, not reinterpret away, the following cases:

| Condition | Required bridge behavior | Authority |
|---|---|---|
| Unknown Process Instance ID | Return Runtime recovery error; do not create silently | Runtime |
| Invalid/corrupt persisted state | Return Runtime persistence/recovery failure | Runtime/Process Store |
| Discovery unavailable | Report capability unavailable; do not substitute Agent-owned search as authoritative discovery | Runtime contract |
| Ambiguous discovery result | Do not arbitrarily select an instance; require a Runtime-authoritative resolution mechanism or explicit Agent/Human decision as permitted by the governing model | Runtime/Human as applicable |
| Unsupported Runtime operation | Reject as unsupported; do not emulate it | Bridge contract + Runtime surface |
| Invalid operation parameters | Return validation failure; Runtime remains semantic authority | Runtime |
| Runtime guard rejection | Return the rejection and relevant Runtime state; do not bypass/rewrite it | Runtime |
| Persistence failure | Return failure and authoritative state/error as provided by Runtime | Runtime/Process Store |
| Stale Agent context | Treat persisted Runtime state as authoritative; refresh before state-sensitive continuation | Runtime |
| Bridge transport/mechanism failure | Report that the Runtime interaction was not confirmed; do not claim successful state mutation | Bridge mechanism |

## 10. Persistence and Continuity Contract

The bridge is intentionally stateless with respect to authoritative Process Instance persistence.

It may hold transient request/response data required by the selected Execution Environment mechanism, but it must not create a second persistent Process Instance registry or authoritative Execution Context store.

Continuity is provided by the Runtime and Process Store. Agent/session loss must not make conversation history the source of truth. A later Agent can continue by obtaining the authoritative Process Instance identifier and recovering the Runtime-owned state.

If a bridge interaction fails before Runtime confirmation, the bridge must report the operation as unconfirmed rather than infer mutation from the Agent's intent.

## 11. Mechanism Neutrality

This contract is intentionally independent of:

- MCP;
- a VS Code extension;
- a particular IDE;
- a particular CLI;
- a particular Agent vendor;
- a specific IPC/HTTP/RPC protocol;
- conversation history as storage.

The mapped environment mechanisms establish feasibility, not a normative transport choice. A later implementation may choose the smallest suitable mechanism while preserving this semantic contract.

## 12. Minimality and Explicit Non-Responsibilities

The bridge does **not**:

- define EPM semantics;
- define or redesign PEM;
- own Process Instance identity;
- own Execution Context semantics;
- persist a competing process state;
- replace `ProcessStore`;
- implement lifecycle semantics independently;
- invent Runtime operations that do not exist;
- bypass Runtime guards;
- perform generalized Agent orchestration;
- decide engineering content that belongs to the Agent/human;
- require MCP or a VS Code extension;
- require a new Runtime discovery API by name;
- change Runtime semantics as part of contract determination.

## 13. Implementation Readiness Assessment

### Contractually determined

The following are sufficiently precise for a subsequent implementation authorization decision:

- bridge purpose and boundary;
- four bridge responsibilities;
- create path;
- known-ID recovery path;
- authoritative Context access;
- supported-operation dispatch;
- authoritative result/state return semantics;
- persistence/continuity authority;
- error and guard propagation rules;
- transport/mechanism neutrality;
- explicit non-responsibilities.

### Remaining implementation dependency

The only material unresolved capability for the complete ordinary-request flow is **Runtime-owned Process Instance discovery when no Process Instance ID is initially known**.

This is not resolved by the contract because the current Runtime demonstrably has no such capability. The contract therefore records it as a dependency/gap rather than silently moving discovery into the bridge.

### Readiness conclusion

**The bridge contract is sufficiently determined to evaluate implementation authorization for the currently supported create/known-ID/context/dispatch paths.**

**The complete no-ID continuation flow is not fully implementable until the Runtime-owned discovery question is separately resolved.**

## 14. Explicit Authorization Decision

This artifact does **not** authorize bridge implementation.

The next decision should explicitly determine whether to authorize a minimal bridge implementation against this contract, and if so, whether the first implementation slice is restricted to:

1. create a Process Instance for a new request;
2. recover a Process Instance by known ID;
3. expose authoritative Execution Context;
4. dispatch already-supported Runtime operations;
5. return authoritative results/state;
6. preserve the discovery gap without inventing a bridge-owned discovery mechanism.

Any Runtime discovery design, Runtime API change, transport selection, or broader orchestration should remain separately authorized work.

## 15. Completion Criterion

Bridge Contract Determination is complete when the engineering team can answer:

> **What is the smallest concrete Agent–Runtime bridge contract that can be implemented using mapped Execution Environment mechanisms while preserving Runtime ownership of Process Instance discovery and authoritative state?**

The answer established by this artifact is:

> **A thin, mechanism-neutral adapter exposing Process Instance creation, known-ID recovery, authoritative Execution Context access, and dispatch of already-supported Runtime operations, with authoritative Runtime results/state returned on every confirmed interaction; Runtime remains the semantic owner of Process Instance discovery, and the current absence of a discovery mechanism is retained as an explicit implementation dependency rather than transferred to the bridge.**
