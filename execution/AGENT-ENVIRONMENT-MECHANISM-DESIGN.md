# Agent / Environment Mechanism Design

**Status:** Design complete — gate passed  
**Work unit:** Agent / Environment Mechanism Design  
**Predecessors:** Project / Scope Resolution Design; Process Binding Design; Persistence Scope Design

## 1. Design Question

Determine the minimum existing mechanism combination through which a real AI Agent can reach the established Engineering Scope, Process Instance binding, persistence, and Execution Context semantics without becoming a semantic authority and without introducing a new orchestration or environment architecture layer.

The key distinction is between:
- semantic capability required;
- mechanism currently available;
- mechanism demonstrated empirically;
- mechanism missing or insufficient.

## 2. Semantic Prerequisites

The closed semantic contracts establish that Engineering Scope Identity is distinct from repository, workspace, Engineering Objective, and Process Instance Identity; repository/workspace/Git information is supporting evidence unless explicitly promoted; one scope may contain multiple Process Instances; a Process Instance has one authoritative scope binding at a given point in authoritative history; scope resolution and PI resolution are distinct; ambiguity and conflict remain explicit; Runtime owns authoritative resolution, binding, recovery, continuation eligibility, and creation authority; ProcessStore remains the authoritative persistence boundary; conversation history and Agent narrative are not authoritative state.

## 3. Existing Mechanism Baseline

### Persistent Agent guidance

Repository-level `AGENTS.md` is the existing persistent guidance mechanism. It separates Human/Agent, Execution Environment, Runtime, and Process Instance/Context roles; requires authoritative state recovery through Runtime; prohibits fabricated state; and requires Runtime-mediated mutation.

**Assessment: Mechanism Demonstrated.**

### Agent–Runtime bridge

`bridge/agent_runtime_bridge.py` currently exposes `create_process(objective)`, `attach(process_instance_id)`, `get_context()`, and `dispatch(operation, params)`. It delegates authority to Runtime. `discover(objective)` is explicitly deferred and returns an unsupported-capability result.

**Assessment: Demonstrated for explicit creation, known-ID recovery, Context acquisition, and supported Runtime mutation. Not a scope-resolution or candidate-discovery mechanism.**

### Runtime and ProcessStore

Runtime currently governs Process Instance creation/attachment, Context recovery, process-state/lifecycle behavior, evidence/decision/artifact/verification recognition, and persistence. ProcessStore persists `process.json`, `context.json`, and `history.jsonl`, with demonstrated cross-process recovery.

**Assessment:** Existing Runtime/persistence mechanism demonstrated; scope/binding semantics are not yet implemented.

### Execution Environment

The demonstrated environment can load `AGENTS.md`, inspect repository/workspace files and Git metadata, execute the bridge/Runtime, present information to the human, and start a fresh Agent invocation.

**Assessment: Mechanism Demonstrated as a capability surface, not as semantic authority.**

## 4. Agent Mechanism Inventory

| Capability | Mechanism | Demonstrated? | Limitation |
|---|---|---:|---|
| Persistent AESM guidance | `AGENTS.md` | Yes | Guidance is behavioral, not enforcement. |
| Request interpretation | Agent + guidance | Yes | Agent interpretation does not establish scope authority. |
| Scope evidence submission | Agent/environment interaction | Partial | No dedicated authoritative scope-resolution request exists. |
| Runtime invocation | Agent–Runtime bridge | Yes | Limited to current bridge surface. |
| Known PI recovery | `attach()` | Yes | Requires known PI ID. |
| Context acquisition | `attach()` / `get_context()` | Yes | Requires selected/known PI. |
| State mutation | `dispatch()` | Yes | Only supported Runtime operations. |
| Scope resolution | No current operation | No | Required for scope-unknown requests. |
| PI candidate discovery | Explicitly deferred | No | No discovery/index/evaluation mechanism. |
| PI binding | No current operation | No | No authoritative binding mechanism. |
| Ambiguity handling | Semantic contract only | No | No executable result surface. |
| Conflict handling | Semantic contract only | No | No executable result surface. |
| Human clarification | Agent ↔ human interaction | Interaction demonstrated | No dedicated authority/provenance channel. |
| Fresh-session recovery | Guidance + bridge + ProcessStore | Yes for known PI | Scope-based recovery not demonstrated. |

## 5. Execution Environment Mechanism Inventory

The environment can provide repository/workspace/Git/artifact evidence and the capability to invoke Runtime. It can also provide human clarification and support fresh Agent sessions.

The boundary is:

```
Repository / Git / Workspace / Artifacts
             ↓
Execution Environment evidence
             ↓
Agent request / evidence submission
             ↓
Runtime evaluation
             ↓
Authoritative scope / binding decision
```

Environment observations are evidence/capabilities; they do not automatically become semantic authority.

## 6. Agent ↔ Runtime Boundary

The required conceptual interaction is:

```
Engineering Request
        ↓
Agent gathers available evidence
        ↓
Agent requests authoritative resolution
        ↓
Runtime resolves scope
        ↓
Runtime resolves existing PI or creation eligibility
        ↓
Authoritative result
        ↓
Context recovery
        ↓
Agent engineering work
        ↓
Runtime-mediated recognition/mutation
        ↓
Persisted authoritative state
```

The Agent may request scope resolution, PI discovery/evaluation, known-PI recovery, binding, creation, Context recovery, continuation, additional evidence evaluation, and human clarification.

Runtime remains authoritative for scope, candidate evaluation, binding, ambiguity/conflict, continuation eligibility, creation eligibility, and persisted state.

## 7. Scope-Evidence Delivery

Potentially authoritative inputs:
- explicit Engineering Scope Identity through an applicable authoritative mechanism;
- known Process Instance ID;
- persisted authoritative binding;
- human clarification through an applicable authority path.

Supporting evidence:
- repository/Git metadata;
- workspace metadata;
- artifact locations;
- Agent observations;
- environment metadata.

The existing environment can collect supporting evidence, but there is currently no dedicated Runtime scope-resolution operation to evaluate it.

**Conclusion:** evidence delivery exists as an environment/Agent capability, while the authoritative receiving/evaluation mechanism is not yet implemented.

## 8. Process Instance Recovery and Binding

### Known Process Instance

```
Agent → known PI ID → bridge.attach()
     → Runtime authoritative PI + Context
     → continuation decision
```

This path is demonstrated by fresh-session recovery.

### Known Scope, unknown PI

```
Agent → scope evidence → Runtime scope resolution
     → PI candidate discovery/evaluation
     → BOUND / AMBIGUOUS / NO_APPLICABLE_PROCESS
```

Current mechanisms cannot complete this path because scope resolution and PI discovery are not exposed.

### Neither known

```
Engineering Request → scope resolution → Process Binding
                     → existing PI recovery OR authorized creation
                     → Context
```

Current `create_process()` can create a PI but does not establish the newly designed scope binding, so it is not yet a complete implementation of this path.

## 9. Ambiguity and Conflict Handling

| Outcome | Agent behavior | Execution consequence |
|---|---|---|
| RESOLVED | Accept authoritative result | Continue |
| UNRESOLVED | Gather permissible evidence or request clarification | Do not invent scope |
| AMBIGUOUS | Present unresolved alternatives and seek evidence/clarification | Do not select arbitrarily |
| CONFLICTING | Preserve incompatible claims and seek applicable authority | Do not silently override binding |
| INVALID | Correct and resubmit input | Do not reinterpret it |
| BOUND | Recover selected PI and Context | Continue if eligible |
| NO_APPLICABLE_PROCESS | Use authorized creation path if preconditions hold | Do not create merely because lookup failed |
| RECOVERY_REQUIRED | Recover persisted authority | Do not reconstruct from conversation |
| CONTINUATION_NOT_PERMITTED | Surface Runtime result | Do not bypass guard |

The semantic rule is that ambiguity remains ambiguity until resolved by an applicable mechanism.

## 10. Human Clarification Boundary

The safe sequence is:

```
Runtime → ambiguity/conflict
        ↓
Agent explains what remains unresolved
        ↓
Human provides clarification
        ↓
Agent submits clarification through applicable authority path
        ↓
Runtime evaluates/accepts
        ↓
Authoritative result is persisted
```

Human interaction is available, but a dedicated authoritative clarification channel and clarification provenance persistence are not yet implemented.

The Agent must not silently convert a vague human answer into durable scope identity.

## 11. Agent / Session Continuity

Demonstrated continuity:

```
Agent A → Runtime mutation → ProcessStore persistence
       → Agent B / fresh session
       → persistent guidance → Runtime attach
       → authoritative PI + Context → continue
```

Fresh-session validation demonstrated recovery without the prior conversation. Cross-process evidence demonstrated persistence across Runtime process replacement.

For scope/binding, the same rule applies: recover authoritative persisted binding once implemented; do not infer replacement scope from a new workspace or conversation; preserve unresolved matters.

## 12. Capability / Mechanism Matrix

| Required capability | Existing mechanism | Empirical status | Classification |
|---|---|---|---|
| Persistent guidance | `AGENTS.md` | Demonstrated | Mechanism Demonstrated |
| Human request delivery | Agent/environment | Demonstrated | Mechanism Demonstrated |
| Environment evidence | Existing tooling | Demonstrated | Mechanism Demonstrated |
| Runtime invocation | Agent–Runtime bridge | Demonstrated | Mechanism Demonstrated |
| Known PI recovery | `attach()` | Demonstrated | Mechanism Demonstrated |
| Context acquisition | bridge | Demonstrated | Mechanism Demonstrated |
| Runtime mutation | `dispatch()` | Demonstrated | Mechanism Demonstrated |
| Persistence/recovery | ProcessStore | Demonstrated | Mechanism Demonstrated |
| Scope evidence submission | No dedicated resolver surface | Not demonstrated | Mechanism Available but Not Yet Demonstrated / deferred implementation |
| Scope resolution | No Runtime/bridge operation | Not demonstrated | Implementation Gap |
| PI candidate discovery/evaluation | Explicitly deferred | Not demonstrated | Implementation Gap |
| PI binding | No current operation | Not demonstrated | Implementation Gap |
| Ambiguity/conflict result surface | Semantic contract only | Not demonstrated | Implementation Gap |
| Human clarification authority | Conversation exists; authority path undefined | Not demonstrated | Mechanism Design Gap |
| Scope/binding persistence | ProcessStore fields absent | Not demonstrated | Persistence Implementation Gap |
| Fresh-session recovery | Known-PI path | Demonstrated | Mechanism Demonstrated; scope discovery deferred |

## 13. Minimum Sufficient Mechanism Set

The evidence supports this minimum foundation:

```
Persistent Agent guidance
        +
Human engineering request / clarification interaction
        +
Execution Environment evidence/tooling
        +
Agent-accessible Runtime / bridge
        +
Authoritative Process Instance + Context persistence
        +
Runtime-mediated authoritative operations
```

No new architecture layer is required.

This foundation is already sufficient for the demonstrated known-PI governed path. It is **not yet sufficient for new or scope-unknown requests** because authoritative scope resolution, PI discovery/binding, explicit ambiguity/conflict results, and scope/binding persistence are absent.

Those are downstream implementation requirements of already-approved semantics, not justification for MCP, skills, an IDE extension, or an orchestration layer.

## 14. Empirical Evidence Reconciliation

### Agent-Boundary Mechanism Validation

Demonstrated persistent `AGENTS.md` guidance, bridge-based PI creation, authoritative Context acquisition, Agent-caused Runtime mutation, persisted history/Context, fresh-session recovery, and separation of Agent narrative from Runtime state.

**Limit:** known-PI path; predates scope/binding implementation.

### Cross-process continuity

Demonstrated Process Instance/Context recovery across Runtime process replacement.

**Limit:** no scope/binding discovery.

### Lifecycle validation and targeted tests

Demonstrate current Runtime guards/state behavior and regression coverage.

**Limit:** do not establish scope resolution or PI discovery.

### DBP empirical execution

Demonstrated engineering activity but did not establish executable AESM participation, authoritative PI state, or project/process binding.

**Limit:** must not be retroactively treated as AESM-governed execution.

## 15. Genuine Mechanism Gaps

| Finding | Classification |
|---|---|
| Persistent guidance | Mechanism Demonstrated |
| Known-PI attach/context | Mechanism Demonstrated |
| Agent Runtime mutation | Mechanism Demonstrated |
| Scope evidence collection | Mechanism Available but Not Yet Demonstrated |
| Scope resolution | Implementation Gap |
| PI discovery/evaluation | Implementation Gap |
| PI binding | Implementation Gap |
| Ambiguity/conflict transport | Implementation Gap |
| Human clarification authority | Mechanism Design Gap |
| Scope/binding persistence | Persistence Implementation Gap |
| New transport/orchestration | Deferred; not justified by current evidence |

## 16. Operational Interaction Model

### New request

```
Human
  ↓
Agent
  ↓
Persistent AESM guidance
  ↓
Execution Environment evidence
  ↓
Authoritative Runtime request
  ↓
Scope Resolution
  ↓
Process Binding
  ↓
Authoritative Process Instance / Context
  ↓
Agent engineering work
  ↓
Runtime-mediated state mutation
  ↓
Persisted evidence/state
  ↓
Verification
```

The guidance, environment, bridge, and persistence mechanisms are already demonstrated. Scope resolution and binding are semantically defined but await implementation.

### Fresh-session recovery

```
Fresh Agent → persistent guidance → Runtime / bridge
            → persisted scope + PI + Context
            → authoritative recovery → continue
```

The known-PI form is demonstrated; scope-based recovery is deferred.

## 17. Alternatives Considered

- **MCP as required transport:** not justified; existing bridge already reaches Runtime.
- **Agent skills as required mechanism:** not justified; persistent guidance and existing tooling demonstrate the current behavioral boundary.
- **VS Code/IDE extension:** rejected as unnecessary and environment-specific.
- **Generalized orchestration layer:** rejected because Runtime is the authoritative execution boundary.
- **Agent inference from repository identity:** rejected; repository is supporting evidence.
- **Environment-selected PI:** rejected; binding remains Runtime-authoritative.
- **New persistence store:** rejected; ProcessStore is the existing authority boundary.

## 18. Non-Goals

This design does not modify Runtime or ProcessStore; add Scope classes or scope persistence; implement candidate discovery/matching/duplicate detection; add MCP/skills/IDE extensions; create an orchestration layer; modify DBP; rewrite historical evidence; or change normative Architecture Model/Operational Flow documents.

## 19. Open Questions

Deferred to implementation/reconciliation:
1. Runtime operation shape for scope resolution.
2. Evidence envelope supplied by Agent/environment.
3. Concrete scope identity representation.
4. Candidate discovery/evaluation mechanism.
5. ProcessStore representation for scope/binding/provenance.
6. Human clarification authority and persistence format.
7. Duplicate-creation/concurrency controls.
8. Scope reassignment/split/merge semantics.
9. Exact continuation eligibility after binding recovery.
10. Multi-project empirical validation.
11. Whether existing environment adapters need configuration rather than new infrastructure.

## 20. Gate Decision

### Agent / Environment Mechanism Design — COMPLETE

The gate is satisfied. The design establishes the existing Agent guidance mechanism, Execution Environment evidence/tooling surface, Agent ↔ Runtime boundary, evidence/authority distinction, known-PI recovery, scope-based interaction path, ambiguity/conflict behavior, human clarification boundary, session continuity, empirical reconciliation, minimum sufficient mechanism combination, and genuine mechanism gaps.

**Key conclusion:** the existing Agent guidance + Execution Environment + Agent–Runtime bridge + ProcessStore combination is the minimum mechanism foundation. It is already sufficient for known-Process-Instance governed execution, but not yet sufficient for new/scope-unknown requests because authoritative scope resolution, PI discovery/binding, ambiguity/conflict result handling, and scope/binding persistence are not implemented.

No new transport, orchestration layer, or IDE-specific mechanism is required by this gate.

## 21. Next Authorized Work

> **Normative Documentation Reconciliation**

Reconcile the completed scope, Process Binding, persistence, and Agent/Environment mechanism decisions with the normative AESM Architecture Model and Operational Flow before implementation begins.

Implementation remains blocked until that reconciliation gate is complete.
