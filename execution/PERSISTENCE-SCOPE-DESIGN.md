# Persistence Scope Design

**Status:** Design complete — pending gate review  
**Work unit:** Persistence Scope Design  
**Predecessor:** `execution/PROCESS-BINDING-DESIGN.md`

## 1. Design Question

Define the minimum durable representation required for Engineering Scope Identity and Process Instance binding so AESM can recover authoritative scope and Process Instance relationships across Agent, conversation, Runtime, IDE, workspace, and path replacement.

The central persistence question is:

> What must AESM persist so that a future Runtime can recover the same engineering scope and correctly bind an Engineering Request to the appropriate Process Instance?

The conceptual relationship is:

```
Engineering Scope
      │
      ├── Process Instance A
      ├── Process Instance B
      └── Process Instance C
```

Persistence must preserve this distinction:

```
Scope Identity ≠ Process Instance Identity ≠ Engineering Objective
```

This artifact defines semantic persistence requirements. It does not implement them.

## 2. Semantic Prerequisites

This design depends on:

- `execution/PROJECT-SCOPE-RESOLUTION-DESIGN.md`
- `execution/PROCESS-BINDING-DESIGN.md`
- `execution/AGENT-GUIDANCE-INTERFACE.md`
- `execution/MECHANISM-VALIDATION.md`
- the normative AESM architecture and operational-flow documents.

Established semantics include:

- Engineering Scope Identity is distinct from repository, workspace, path, and Process Instance Identity.
- One scope may contain multiple Process Instances.
- A Process Instance has one authoritative scope binding at a given point in authoritative history.
- Existing authoritative Process Instance state survives Agent/session/Runtime replacement.
- Runtime owns authoritative Process Instance and binding state.
- Agent and Execution Environment can provide evidence but do not become persistence authorities.
- Ambiguity and conflict must remain explicit.
- Existing ProcessStore is the current authoritative persistence boundary for Process Instance and Execution Context state.
- No second persistence system is justified by current evidence.

## 3. Persistence Boundary

The existing persistence boundary is:

```
ProcessStore
├── process.json
├── context.json
└── history.jsonl
```

Current implementation evidence shows that this boundary already supports:

- Process Instance identity;
- Engineering Objective;
- lifecycle state;
- EPM/PEM references;
- Execution Context;
- Context versioning;
- history;
- cross-process recovery.

It does not currently persist:

- authoritative Engineering Scope Identity;
- Process Instance → Scope binding;
- binding provenance;
- candidate evaluation;
- binding decision basis;
- creation/continuation binding basis.

Therefore the semantic gap is not the absence of persistence in general. It is the absence of durable **scope/binding semantics** within the existing persistence boundary.

The preferred direction is to extend the existing authoritative boundary rather than introduce an independent scope store.

## 4. Engineering Scope Identity

Engineering Scope Identity must be a stable semantic identity, not a filesystem convenience.

It must:

- uniquely identify the engineering boundary within AESM;
- remain stable across Agent replacement;
- remain stable across conversation replacement;
- remain stable across Runtime replacement;
- remain stable across IDE replacement;
- normally remain stable across workspace recreation;
- normally remain stable across repository/path relocation;
- be recoverable without the original Agent conversation.

The following are not automatically scope identity:

- filesystem path;
- workspace identifier;
- IDE instance;
- Agent identity;
- conversation identifier;
- current checkout directory;
- Git branch;
- current Git commit.

Repository/Git metadata may contribute supporting evidence when applicable, but it must not silently become scope identity.

A future concrete representation may be opaque or structured, but the semantic contract should treat the identity as stable and authoritative once established.

## 5. Process Instance Binding Representation

Every authoritative Process Instance must be persistently associated with its current Engineering Scope Identity.

The minimum semantic information is:

```
Process Instance Identity
Engineering Scope Identity
Engineering Objective
Binding basis
Binding provenance
Creation/continuation basis
Authoritative Process Instance state
Authoritative Execution Context
```

The binding itself must be authoritative. A scope candidate observed by an Agent or environment is not equivalent to an established binding.

The representation may eventually live directly in Process Instance persistence or in another representation owned by the same ProcessStore authority. This design does not require a particular serialization shape.

## 6. Scope / Process Instance Cardinality

The persistence model must support:

```
one scope → zero or many Process Instances
one Process Instance → one authoritative scope binding
```

It must not assume:

```
one repository → one Process Instance
one objective → one Process Instance
one workspace → one Process Instance
```

A scope may have no Process Instances before the first authorized creation.

A Process Instance without a valid authoritative scope binding must not be treated as a normally bound Process Instance once scope binding becomes mandatory for the applicable execution model.

## 7. Binding Provenance

Persistence must preserve why a binding became authoritative.

Relevant provenance categories include:

- explicit authoritative scope supplied through an applicable mechanism;
- existing persisted authoritative binding;
- Runtime-established binding during authorized Process Instance creation;
- human clarification accepted through an applicable authority mechanism;
- recognized evidence subsequently evaluated by Runtime.

Supporting evidence must remain distinguishable from authority.

At minimum, provenance must identify:

- the basis of the binding;
- the authority under which it became authoritative;
- when it became effective;
- the associated Process Instance;
- the relevant scope identity.

The Agent's original conversation is not an acceptable sole source of binding provenance.

## 8. Binding History and Mutation

Default semantic rule:

> An authoritative Process Instance → Scope binding is stable unless an explicit reassignment mechanism is defined.

No persistence model may silently reinterpret historical binding because:

- a repository moved;
- a repository was renamed;
- a Git remote changed;
- a workspace was recreated;
- files moved;
- the Agent changed;
- the conversation changed;
- the Runtime process changed.

Future explicit reassignment, split, or merge semantics would require historical traceability. At minimum, such a history would need:

- previous scope identity;
- new scope identity;
- authority;
- basis;
- effective version/time;
- affected Process Instance;
- reason;
- impact on Context/pending work.

Reassignment is deferred and therefore no implementation representation is mandated for it now. The persistence design must simply avoid making historical reconstruction impossible.

## 9. Process Instance Creation Persistence

Creation must establish the following conceptual consistency boundary:

```
Process Instance Identity
+
Engineering Scope Identity
+
Engineering Objective
+
Initial Execution Context
+
Creation/binding provenance
```

A successfully persisted Process Instance must not appear authoritative while its required scope binding is missing or contradictory.

Creation history should distinguish:

- Process Instance creation;
- scope binding establishment;
- creation basis.

Whether these are represented as one atomic persistence operation or several internally coordinated operations is an implementation decision deferred to implementation design. The semantic result must be consistent and recoverable.

## 10. Continuation and Recovery Persistence

For known Process Instance recovery, persistence must allow:

```
Known PI ID
→ recover Process Instance
→ recover scope binding
→ recover Context
→ validate applicability
→ evaluate continuation
```

For scope-based recovery:

```
Scope Identity
→ identify persisted Process Instance candidates
→ evaluate candidates
→ bind existing PI OR authorize creation
```

Recovery must survive:

- Agent replacement;
- conversation replacement;
- Runtime process replacement;
- IDE replacement;
- workspace recreation;
- checkout/path replacement.

Cross-process continuity evidence already demonstrates that Process Instance and Context persistence can survive Runtime replacement. The new persistence requirement is to preserve the scope/binding relationship alongside that state.

## 11. Duplicate-Creation Semantics

Persistence must support the semantic requirement that repeated requests do not create replacement Process Instances when an applicable authoritative Process Instance already exists.

The semantic distinction is:

```
same request replay
≠
automatically new execution
```

However:

```
same objective
≠
automatically same Process Instance
```

The persistence model therefore needs enough durable information to:

- discover existing bindings;
- evaluate candidate applicability;
- preserve creation provenance;
- distinguish legitimate separate executions.

Concurrency control, locking, transactions, idempotency keys, or distributed coordination are not selected here. They belong to later implementation design after the semantic requirement is established.

## 12. Consistency Requirements

The persistence boundary must prevent authoritative contradictions such as:

- Process Instance references scope A while binding history establishes scope B as current;
- Process Instance exists but required Context is absent;
- Context references a different Process Instance;
- binding is persisted without enough provenance to determine its authority;
- creation is recorded without a recoverable scope binding when scope is mandatory.

At recovery time, inconsistent persisted data must result in explicit recovery/error handling rather than silent repair.

The persistence model must not silently infer a new scope or Process Instance to compensate for missing authoritative data.

## 13. Traceability Requirements

Persistence must support reconstruction of:

> Why did this request bind to this Process Instance within this Engineering Scope?

The minimum traceable information is:

- Engineering Request or sufficient request reference;
- resolved Engineering Scope Identity;
- explicit Process Instance Identity, if supplied;
- candidate Process Instances considered, where candidate discovery is persisted;
- relevant candidate evaluation evidence;
- selected Process Instance;
- rejected/excluded candidates and basis, where required for reconstruction;
- ambiguity/conflict;
- clarification;
- binding result;
- creation or continuation basis;
- authoritative state/version.

Not every transient observation must become permanent state. The design requirement is that authoritative binding decisions remain reconstructable without the original Agent conversation.

## 14. Current ProcessStore Reconciliation

Current implementation provides:

| Semantic requirement | Current implementation | Assessment |
|---|---|---|
| Process Instance identity | `process.json` | Demonstrated |
| Engineering Objective | `process.json` and Context | Demonstrated |
| Lifecycle state | `process.json` | Demonstrated |
| Execution Context identity | `context.json` | Demonstrated |
| Context persistence/version | `context.json` | Demonstrated |
| History | `history.jsonl` | Demonstrated |
| Cross-process recovery | Runtime attach + ProcessStore | Demonstrated |
| Scope identity | None | Semantic gap |
| PI → Scope binding | None | Semantic gap |
| Binding provenance | General history exists, binding-specific semantics absent | Semantic gap |
| Candidate evaluation | None | Deferred mechanism gap |
| Creation basis | Generic process creation history exists | Binding-specific gap |
| Continuation basis | Runtime/history evidence exists, binding-specific basis absent | Binding-specific gap |
| Binding decision traceability | None | Semantic gap |

This distinction is important: the current implementation already provides a viable persistence boundary. The missing capability is the authoritative persistence of scope/binding semantics, not persistence itself.

## 15. Minimum Durable Representation

The minimum conceptual durable representation is:

```
Engineering Scope
├── scope_identity
├── identity_basis
└── scope_provenance

Process Instance
├── process_instance_id
├── engineering_objective
├── authoritative_scope_binding
├── binding_basis
├── binding_provenance
├── creation_basis
├── continuation_basis (when applicable)
└── authoritative execution state/context

Binding Trace
├── request/reference
├── candidates considered (when applicable)
├── evaluation basis
├── selected/rejected result
├── ambiguity/conflict
└── authority/clarification
```

This is a semantic representation, not a required JSON schema.

The minimum representation should not require a first-class independent Scope database if the existing ProcessStore can authoritatively persist the relationship and trace.

## 16. Recovery Matrix

| Starting information | Required persisted information | Recovery result |
|---|---|---|
| Known PI ID | PI identity + scope binding + Context | Direct PI recovery |
| Scope Identity | Scope identity + PI bindings + PI state | Candidate discovery |
| Scope + explicit PI | Both identity and binding | Validate direct recovery |
| Neither scope nor PI | Scope-resolution result + binding information | Continue after resolution |
| Environment evidence only | Persisted authoritative binding | Evidence evaluated against authority |
| Conflicting authoritative data | Binding history/provenance | Conflict, not silent repair |
| Existing completed PI | PI state + binding + objective/history | Continuation only if explicitly permitted |
| Agent/session replaced | Durable PI/binding/Context | Continue from persistent state |
| Runtime replaced | Durable PI/binding/Context/history | Recover authoritative state |
| Workspace/path changed | Stable scope identity + binding | Preserve binding |

## 17. Persistence Decision Matrix

| Decision | Semantic requirement | Design decision |
|---|---|---|
| Scope identity | Stable authoritative identity | Persist as durable scope identity |
| PI binding | One authoritative scope per PI | Persist within existing authority boundary |
| Multiple PIs per scope | Required | Supported |
| Multiple scopes per PI | Not established | Not permitted by default |
| Repository as identity | Insufficient | Supporting evidence only |
| Workspace as identity | Insufficient | Supporting evidence only |
| Objective as identity | Insufficient | Matching evidence only |
| Binding provenance | Required | Persist |
| Binding history | Required for future mutation | Preserve extensibility; mutation deferred |
| Creation basis | Required | Persist binding-specific basis |
| Continuation basis | Required when continuation occurs | Persist/reconstruct |
| Candidate trace | Required where needed for reconstruction | Persist relevant decision evidence |
| Separate scope store | Not semantically required | Do not introduce now |
| Database technology | Not semantically required | Deferred |
| Concurrency mechanism | Required eventually for duplicate-creation safety | Deferred |
| Scope reassignment | Not currently defined | Deferred |

## 18. Alternatives Considered

### Repository metadata as the durable scope identity

Rejected as insufficiently stable and semantically under-defined.

### Workspace as durable scope identity

Rejected because workspace recreation and relocation must not silently change engineering scope.

### Process Instance ID as scope identity

Rejected because one scope may contain multiple Process Instances.

### Engineering Objective as scope identity

Rejected because the same objective can recur across scopes and executions.

### Separate Scope database

Not adopted. Current evidence does not establish a semantic need for a second persistence authority.

### Only persist the final PI → Scope relationship

Insufficient because binding traceability and provenance would be lost.

### Reconstruct scope from environment during recovery

Rejected as an authoritative recovery mechanism. Environment observations can support resolution but must not silently replace persisted authority.

## 19. Implementation Constraints

The eventual implementation must:

- preserve Runtime authority;
- use the existing ProcessStore boundary unless later evidence establishes otherwise;
- avoid a second competing persistence system;
- keep Scope Identity separate from PI Identity;
- preserve existing cross-process continuity;
- preserve existing Execution Context semantics;
- avoid silently repairing contradictory persisted state;
- make authoritative binding recoverable independently of conversation history;
- support multiple Process Instances within one scope;
- avoid treating repository/workspace/path metadata as authoritative scope without an explicit semantic rule.

The implementation must not prematurely introduce:

- a Project entity;
- a generalized scope registry;
- objective similarity algorithms;
- Agent-owned persistence;
- IDE-specific persistence;
- Git-specific identity semantics.

## 20. Open Questions

Deferred to subsequent work:

1. Exact concrete representation of Engineering Scope Identity.
2. Exact fields and serialization shape in ProcessStore.
3. Whether a separate persisted scope record becomes necessary when multiple scopes exist.
4. Candidate indexing/discovery mechanism.
5. Objective matching mechanism.
6. Duplicate-creation concurrency mechanism.
7. Human clarification persistence mechanism.
8. Scope reassignment/split/merge history representation.
9. Material objective mutation semantics.
10. Exact lifecycle eligibility for continuation.
11. Agent/Execution Environment mechanism for supplying authoritative scope candidates.
12. Multi-project empirical validation.

## 21. Gate Decision

### Persistence Scope Design — COMPLETE

This design establishes:

- the persistence boundary;
- durable Engineering Scope Identity requirements;
- Process Instance → Scope binding requirements;
- cardinality;
- provenance;
- mutation/history requirements;
- creation consistency;
- recovery requirements;
- duplicate-creation persistence semantics;
- consistency requirements;
- traceability;
- current ProcessStore reconciliation;
- minimum durable representation;
- recovery and decision matrices;
- alternatives and implementation constraints.

No Runtime API, ProcessStore schema, scope class, persistence technology, Agent mechanism, or discovery implementation is introduced by this gate.

## 22. Next Authorized Work

> **Agent / Environment Mechanism Design**

The next work must define how the established scope and binding semantics are delivered through the real Agent and Execution Environment boundary.

It should determine:

- which existing Agent guidance mechanisms can supply scope/binding inputs;
- which Execution Environment mechanisms can expose relevant evidence;
- how authoritative Runtime interaction is reached;
- how the Agent requests scope resolution/binding without becoming authoritative;
- how ambiguity/conflict is surfaced to the human;
- the minimum mechanism combination required for real execution.

The progression is:

```
Project / Scope Resolution Design ✓
        ↓
Process Binding Design ✓
        ↓
Persistence Scope Design ✓
        ↓
Agent / Environment Mechanism Design
        ↓
Normative Documentation Reconciliation
        ↓
Implementation
        ↓
Multi-Project Validation
```
