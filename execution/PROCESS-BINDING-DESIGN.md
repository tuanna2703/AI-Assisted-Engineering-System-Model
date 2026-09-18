# Process Binding Design

**Status:** Design complete — pending gate review  
**Work unit:** Process Binding Design  
**Predecessor:** `execution/PROJECT-SCOPE-RESOLUTION-DESIGN.md`

## 1. Design Question

Define how AESM transforms a resolved Engineering Scope and Engineering Request into an authoritative Process Instance binding without collapsing:

- Engineering Scope Identity;
- Engineering Objective;
- Process Instance Identity;
- Process Instance discovery;
- Context recovery;
- continuation; and
- new Process Instance creation.

The conceptual sequence is:

```
Engineering Request
  → Resolved Engineering Scope
  → Process Instance Candidate Discovery
  → Candidate Evaluation
  → Binding Decision
  → Existing Process Instance + Context Recovery
       OR
     New Process Instance + Initial Context
```

This is a semantic/design artifact. It does not introduce a Runtime API, ProcessStore implementation, new persistence technology, Agent orchestration, or a first-class Project entity.

## 2. Semantic Prerequisites

The binding design depends on the established scope-resolution semantics:

- Engineering Scope Identity identifies the stable engineering boundary.
- Engineering Objective identifies intended engineering work.
- Process Instance Identity identifies one concrete engineering execution.
- Execution Context is authoritative operational state.
- Runtime owns authoritative Process Instance discovery and control.
- Agent participation does not transfer Runtime authority.
- Execution Environment supplies evidence and capabilities, not semantic authority.
- One scope may contain multiple Process Instances.
- A Process Instance has one authoritative scope binding at a given point in its authoritative history.
- Known Process Instance identity remains a valid direct recovery mechanism.
- Ambiguity and conflict must remain explicit.

Current implementation evidence is treated as evidence of existing behavior, not as the semantic source of truth. In particular, the current Runtime/bridge supports explicit Process Instance creation and known-ID attachment, while objective-based discovery is explicitly deferred.

## 3. Process Binding Terminology

**Candidate:** an existing Process Instance that may be applicable to the resolved Engineering Scope and request.

**Candidate discovery:** obtaining Process Instance identities and relevant authoritative metadata that could participate in binding evaluation.

**Candidate evaluation:** determining whether a discovered Process Instance is semantically applicable.

**Binding:** the authoritative association of the Engineering Request with one Process Instance for execution.

**Continuation:** execution of an already-established Process Instance after authoritative Context recovery.

**Direct recovery:** locating an explicitly identified Process Instance by its known identity and validating its authoritative state.

**Creation:** establishing a new Process Instance when no applicable existing Process Instance is resolved and creation conditions are satisfied.

**Reuse:** selecting an existing Process Instance for the current request. Reuse is not synonymous with continuation: an existing completed or otherwise non-continuable instance may be relevant evidence without being eligible for continuation.

**Distinguishing information:** authoritative or recognized information that can legitimately differentiate otherwise applicable Process Instance candidates.

The semantic sequence is therefore:

```
Request
→ resolved scope
→ candidate discovery
→ candidate evaluation
→ binding
→ recovery/continuation OR creation
```

## 4. Candidate Sources

Potential candidate sources are:

| Source | Role | Authority |
|---|---|---|
| Explicit known Process Instance ID | Direct execution identity | Authoritative subject to validation |
| Persisted scope bindings | Existing authoritative relationship | Authoritative |
| Process Instance metadata | Candidate identity/objective/state | Authoritative for persisted values |
| Request provenance | Candidate matching information | Supporting unless separately authoritative |
| Engineering Objective | Matching information | Insufficient by itself |
| Agent-provided Process Instance reference | Candidate/proposal or direct identity | Direct identity only when established as authoritative input |
| Execution Environment observations | Supporting evidence | Non-authoritative |
| Repository/workspace/artifact evidence | Supporting evidence | Non-authoritative for binding |

Candidate discovery must not turn an observation into an authoritative Process Instance merely because the observation is technically easy to obtain.

The current bridge does not independently search or index Process Instances. That boundary remains intentional until a later mechanism design authorizes a concrete discovery mechanism.

## 5. Candidate Eligibility

A discovered Process Instance is eligible for binding only if the applicable semantic conditions hold.

At minimum:

1. Its identity is valid and recoverable.
2. Its authoritative scope binding is compatible with the resolved Engineering Scope.
3. Its authoritative state can be recovered.
4. Its Engineering Objective is relevant to the current request according to defined matching semantics.
5. Its lifecycle/process state permits the intended operation, or a separate rule explicitly permits the requested relationship.
6. No authoritative conflict invalidates its use.
7. Selection can be justified by semantic distinguishing information rather than technical ordering.

A candidate is not eligible merely because it:

- exists in the same repository;
- is the newest or oldest;
- is closest to the current workspace;
- is easiest to access;
- has a similar text objective;
- appears first in storage;
- was created by the same Agent; or
- is the only candidate visible through a limited technical mechanism.

Incomplete discovery must not be represented as proof that no applicable Process Instance exists.

## 6. Matching Semantics

Process Instance matching requires more than textual objective similarity.

Potential matching dimensions include:

- Engineering Scope Identity;
- Engineering Objective;
- explicit Process Instance Identity;
- request provenance;
- established Process Instance state;
- recognized requirements or constraints;
- recognized work/artifact relationship;
- explicit continuation intent;
- other distinguishing information established by applicable semantics.

Objective matching may be:

- **exact:** the established objective corresponds directly;
- **related:** the objective is semantically related but does not establish identity;
- **insufficient:** objective information cannot distinguish candidates;
- **conflicting:** authoritative objective information is incompatible with the requested binding.

Similarity is evidence, not identity.

If two Process Instances have similar objectives within the same scope, additional distinguishing information is required. Without it, the result remains ambiguous.

No implementation-specific similarity algorithm is selected by this design.

## 7. Deterministic Selection

When multiple candidates exist, selection must be deterministic in the semantic sense.

A valid rule must:

1. use defined authoritative or recognized distinguishing information;
2. produce the same result for equivalent authoritative inputs;
3. be independent of storage order and filesystem order;
4. be independent of technical accessibility;
5. not rely on recency unless recency is explicitly established as semantically relevant;
6. preserve explicit Process Instance identity when supplied;
7. expose ambiguity when no rule uniquely distinguishes a candidate.

Invalid tie-breakers include:

- first returned candidate;
- first filesystem entry;
- newest Process Instance;
- oldest Process Instance;
- currently attached Runtime;
- current workspace proximity;
- arbitrary lexical ordering;
- technical availability.

If several candidates remain equally applicable, the Process Instance binding result is **AMBIGUOUS** and execution requiring a unique Process Instance must not proceed.

## 8. Existing Process Instance Continuation

Continuation requires more than successful discovery.

The conceptual preconditions are:

1. a Process Instance has been authoritatively bound to the resolved scope;
2. the Process Instance is recoverable;
3. its authoritative Execution Context is recoverable and valid;
4. the current request is applicable to that Process Instance;
5. its lifecycle/process state permits continuation;
6. no authoritative conflict blocks continuation;
7. the continuation basis is traceable.

Lifecycle and process-state semantics remain distinct. A Process Instance's lifecycle value and its Execution Context's process state must not be inferred to mean the same thing.

A completed Process Instance is not automatically continued merely because its objective is related. Continuation of a completed instance requires an explicit applicable semantic rule. Otherwise a new Process Instance may be required.

Suspended or otherwise paused work may be continued only when the applicable lifecycle semantics permit continuation and the required resumption conditions are satisfied.

Discovery, Context recovery, and continuation remain separate operations:

```
discover → recover → validate → continue
```

Successful attachment alone is not proof that continuation is authorized.

## 9. Direct Process Instance Recovery

A known Process Instance ID provides a direct recovery path:

```
Known Process Instance ID
→ Runtime attach
→ authoritative Process Instance
→ authoritative Context recovery
→ binding validation
→ continuation decision
```

An explicit Process Instance ID has precedence as an execution identity input over ordinary candidate discovery, subject to validation.

It does not authorize the Agent to bypass authoritative state validation.

If non-authoritative environment evidence appears inconsistent with the known Process Instance, the Runtime should recover the known Process Instance and preserve the contradiction as traceable evidence rather than silently changing the binding.

If authoritative scope information contradicts the Process Instance's established binding, the result is **CONFLICTING** unless an explicit authority rule resolves the contradiction.

## 10. New Process Instance Creation

New Process Instance creation is permitted only when:

1. Engineering Scope Identity is resolved;
2. Engineering Objective is established;
3. candidate discovery/evaluation does not resolve an applicable existing Process Instance;
4. creation is permitted for the request;
5. the new Process Instance can be authoritatively bound to the resolved scope;
6. the initial Execution Context can be established;
7. the creation basis is traceable.

Creation must not be used as an escape from:

- scope ambiguity;
- Process Instance ambiguity;
- authoritative conflict;
- insufficient candidate discovery;
- missing required objective information.

The new Process Instance must initially establish, at minimum:

- Process Instance Identity;
- Engineering Scope binding;
- Engineering Objective;
- applicable EPM/PEM references;
- initial authoritative Execution Context;
- creation/binding provenance.

The existing Runtime's `create_process(objective)` behavior demonstrates the current creation mechanism, but it does not yet demonstrate semantic scope binding. That missing binding is a design requirement, not evidence to be fabricated into the historical Runtime behavior.

## 11. Duplicate-Creation Semantics

Repeated or concurrent requests can represent the same engineering work without implying that they should create independent Process Instances.

The semantic requirement is:

> Where an applicable existing Process Instance is authoritatively established, a repeated request must not create a replacement merely because the Agent, conversation, Runtime process, IDE, or workspace changed.

When two creation attempts occur without an already-established binding, duplicate prevention requires a separately defined authoritative mechanism capable of distinguishing equivalent requests and/or serializing creation decisions. This design does not select locking, transactions, distributed coordination, or a particular persistence technology.

A replayed request must therefore be evaluated through the same candidate and binding semantics rather than assuming that every invocation creates a new Process Instance.

Creation idempotency is a persistence/mechanism concern built on this semantic requirement.

## 12. Scope / Process Binding Invariants

The following invariants are normative for binding:

1. **Scope Identity ≠ Process Instance Identity.**
2. **Scope Identity ≠ Engineering Objective.**
3. One Engineering Scope may contain multiple Process Instances.
4. Each Process Instance has one authoritative scope binding at a given point in authoritative history.
5. Process Instance binding is not silently changed by Agent/session replacement.
6. Process Instance binding is not silently changed by workspace, repository, or path changes.
7. A Process Instance cannot be selected solely from objective similarity when multiple applicable candidates remain.
8. Ambiguous scope cannot become arbitrary Process Instance selection.
9. A discovered candidate cannot become authoritative without Runtime evaluation.
10. Direct Process Instance recovery remains valid.
11. Creation cannot be used to bypass unresolved or conflicting binding.
12. Binding decisions must remain reconstructable independently of the original Agent conversation.

## 13. Objective / Process Binding

Engineering Objective is a primary matching dimension but not a unique Process Instance identity.

The same objective may legitimately occur:

- in multiple scopes;
- multiple times within one scope;
- as separate executions with different provenance;
- as a continuation/reconsideration of an existing execution.

Therefore:

```
same objective ≠ same Process Instance
```

A Process Instance's objective should not be silently rewritten merely to make a new request match it.

If the work represented by an existing Process Instance materially changes objective, the applicable semantics must determine whether:

- the objective is legitimately mutable within that Process Instance;
- the change constitutes reconsideration of the same engineering work; or
- a new Process Instance is required.

That decision is not delegated to textual similarity or Agent convenience.

## 14. Rebinding and Mutation

Default binding rule:

> A Process Instance's authoritative scope binding is stable unless an explicit reassignment mechanism is defined.

No implicit rebinding occurs because:

- a repository moved;
- a repository was renamed;
- a Git remote changed;
- a workspace was recreated;
- files moved;
- the Agent changed;
- the conversation changed;
- the Runtime process changed.

Scope reassignment, split, and merge remain explicit future semantic operations.

If reassignment is eventually permitted, it must define:

- authority;
- preconditions;
- affected historical bindings;
- effective time/version;
- traceability;
- conflict handling;
- impact on existing Context and pending work.

The same principle applies to material objective mutation.

## 15. Runtime Authority

Runtime owns the authoritative Process Instance binding boundary.

Runtime responsibilities include:

- evaluate candidate information;
- validate explicit Process Instance identity;
- determine candidate applicability;
- resolve Process Instance ambiguity/conflict;
- preserve authoritative binding;
- establish binding during authorized creation;
- validate Context recovery;
- determine whether continuation is permitted;
- expose binding outcomes and uncertainty;
- persist or delegate persistence of authoritative binding information.

The Runtime does not have to directly inspect Git, filesystems, IDEs, or Agent internals. Those can remain evidence providers through an applicable mechanism.

The bridge remains an adapter, not a second authority.

## 16. Agent Boundary

The Agent may:

- submit the Engineering Request;
- provide an explicit Process Instance ID;
- provide scope information;
- provide candidate observations;
- request candidate discovery;
- request continuation;
- request creation;
- gather additional evidence;
- present human clarification.

The Agent may not:

- declare a candidate authoritative;
- silently choose among ambiguous Process Instances;
- rewrite authoritative scope binding;
- treat a repository/workspace as Process Instance identity;
- fabricate Process Instance state;
- create a replacement solely because the session changed;
- act as the authoritative Process Instance registry.

Agent guidance should direct the Agent toward Runtime-mediated binding and recovery rather than embedding a competing registry or matching algorithm.

## 17. Execution Environment Boundary

The Execution Environment contributes capabilities and evidence such as:

- current repository/workspace information;
- Git metadata;
- artifact locations;
- human-provided identity;
- available Runtime/bridge access;
- Agent invocation context.

These are evidence inputs unless an explicit semantic rule promotes a particular input to authoritative identity.

The design remains independent of a specific host. VS Code, other IDEs, CLI, web environments, and other Agent hosts can provide the necessary evidence and Runtime access through different mechanisms.

## 18. Persistence Requirements

No persistence technology is selected here.

The authoritative persistent representation must eventually preserve enough information to answer:

> Which Process Instance was bound to this request, within which scope, on what basis, and with what authoritative state?

At minimum, the semantic data requirements are:

```
Engineering Scope Identity
Process Instance Identity
Engineering Objective
Binding basis / provenance
Creation or continuation basis
Relevant candidate-evaluation evidence
Binding history where mutation is permitted
Authoritative Process Instance state
Authoritative Execution Context reference/state
```

Persistence must survive Agent, conversation, Runtime-process, IDE, workspace, and checkout-path replacement.

This does not require a second AESM persistence system. Integration with the existing ProcessStore remains the preferred design direction unless later evidence establishes a semantic need for a separate store.

## 19. Recovery Requirements

### Known Process Instance

```
Known PI ID
→ recover authoritative PI
→ recover Context
→ validate scope binding
→ evaluate continuation
```

### Resolved Scope without Known Process Instance

```
Resolved scope
→ discover candidates
→ evaluate candidates
→ bind existing PI OR create new PI
→ recover/create Context
```

### Neither Scope nor Process Instance Known

```
Engineering Request
→ Scope Resolution
→ Process Binding
→ Context recovery/creation
```

Recovery must not depend on the original Agent conversation.

Changing the Agent or Execution Environment must not create a new Process Instance when an applicable authoritative Process Instance already exists.

## 20. Failure and Uncertainty Semantics

The binding process requires explicit conceptual outcomes:

| Outcome | Meaning |
|---|---|
| **BOUND** | One applicable Process Instance has been authoritatively selected |
| **NO_APPLICABLE_PROCESS** | Scope is resolved but no existing Process Instance applies |
| **AMBIGUOUS** | Multiple Process Instances remain equally applicable |
| **CONFLICTING** | Authoritative information makes incompatible binding claims |
| **INVALID** | Supplied identity or binding information violates applicable constraints |
| **RECOVERY_REQUIRED** | A candidate is identified but authoritative Context/state must be recovered before continuation |
| **CONTINUATION_NOT_PERMITTED** | Existing Process Instance is known but current operation cannot continue it |

These are semantic categories, not yet mandatory Runtime enums or API values.

A no-applicable-process result may lead to creation only when creation preconditions are independently satisfied.

## 21. Traceability

A binding decision must be reconstructable without the original Agent conversation.

The trace should preserve, as applicable:

- Engineering Request;
- resolved Engineering Scope Identity;
- explicit Process Instance Identity, if supplied;
- discovered candidates;
- candidate provenance;
- candidate evaluation basis;
- rejected/excluded candidates and reasons;
- matching evidence;
- authority applied;
- ambiguity/conflict;
- clarification;
- binding result;
- continuation versus creation decision;
- creation basis;
- authoritative Process Instance state/version.

The reconstruction question is:

> Why did AESM bind this Engineering Request to this Process Instance rather than another candidate or a new Process Instance?

Technical lookup order must never be the only answer.

## 22. Process Binding Decision Matrix

| Resolved scope | PI evidence | Applicability | Binding result |
|---|---|---|---|
| Unique authoritative scope | One applicable existing PI | Continuable | Bind + recover Context + continue |
| Unique authoritative scope | One applicable existing PI | Non-continuable | Do not continue; evaluate creation only if permitted |
| Unique authoritative scope | Multiple candidates | One uniquely distinguished | Bind distinguished candidate |
| Unique authoritative scope | Multiple candidates | Equally applicable | **AMBIGUOUS** |
| Unique authoritative scope | No applicable PI | Creation permitted | Create + bind + initialize Context |
| Unique authoritative scope | No applicable PI | Creation not permitted | **NO_APPLICABLE_PROCESS** |
| Explicit valid PI ID | Matching PI exists | Binding valid | Direct recovery + validate + continue if permitted |
| Explicit PI ID | PI missing/invalid | — | **INVALID** / recovery failure |
| Explicit PI ID | Authoritative scope contradicts PI binding | — | **CONFLICTING** unless authority rule |
| Known PI | Non-authoritative environmental contradiction | PI otherwise valid | Recover known PI + trace contradiction |
| Unresolved scope | Any PI evidence | — | No Process Instance binding |
| Conflicting scope | Any PI evidence | — | No Process Instance binding |
| Resolved scope | Completed related PI | Continuation not explicitly permitted | Do not continue; evaluate new execution |
| Resolved scope | Candidate state requires recovery | Candidate otherwise applicable | **RECOVERY_REQUIRED** |
| Resolved scope | Existing PI known but operation disallowed | — | **CONTINUATION_NOT_PERMITTED** |

No row authorizes selection by storage order, recency, accessibility, or workspace proximity.

## 23. Empirical Evidence Reconciliation

Existing evidence constrains the design but does not replace it.

### Cross-process continuity

The cross-process experiment demonstrated that a Process Instance can be discovered and recovered across Runtime processes using persistent state. It supports the requirement that Process Instance identity and Context survive Runtime replacement.

It did not demonstrate scope-based Process Instance discovery or semantic candidate selection.

### Lifecycle behavioral validation

Lifecycle validation demonstrated that current Process Instance lifecycle state and Execution Context process state are distinct implementation concepts. It supports keeping binding/continuation decisions separate from lifecycle semantics.

It did not establish Process Instance binding rules.

### Targeted lifecycle tests

The targeted lifecycle scenarios provide regression evidence for current Runtime behavior. They do not establish objective matching, candidate selection, or creation idempotency.

### Agent-boundary mechanism validation

The mechanism validation demonstrated:

```
fresh Agent
→ persistent guidance
→ Process Instance
→ authoritative Context
→ Agent-caused Runtime mutations
→ persisted evidence
→ fresh-session recovery
```

This supports the authority boundary and continuity requirements.

It does not demonstrate semantic scope resolution or Process Instance candidate binding for a new request.

### DBP empirical history

The historical DBP experiment demonstrated engineering activity but did not establish authoritative AESM scope or Process Instance binding.

The historical `.akg/` mechanism must not be retroactively treated as AESM Process Instance persistence.

Historical evidence remains unchanged.

## 24. Alternatives Considered

### Repository = Process Instance

Rejected. A repository is environment/evidence context and does not uniquely identify one engineering execution.

### Repository + objective = Process Instance

Rejected as insufficient. The same objective may recur within one repository/scope and may span multiple repositories.

### Objective-only matching

Rejected as insufficient when multiple Process Instances can legitimately share similar objectives.

### Agent-selected Process Instance

Rejected as authoritative binding. The Agent can propose or identify but cannot become the Process Instance registry.

### First matching candidate

Rejected because technical ordering is not semantic authority.

### New Process Instance whenever uncertain

Rejected because creation cannot be an ambiguity escape hatch and would fragment continuity.

### Completed Process Instance always reused

Rejected. Completion does not by itself establish permission to continue.

### New first-class Project/Binding entity immediately

Not required by this design. The semantic requirements can be expressed through authoritative scope binding and Process Instance state; persistence design will determine the minimum durable representation.

### Separate Process Instance store

Not adopted. Existing ProcessStore is the current persistence boundary; a second store would require independent authority and synchronization semantics.

## 25. Open Questions

Deferred to subsequent design work:

1. Concrete persistent representation of Engineering Scope Identity.
2. Exact Process Instance binding fields in the existing ProcessStore.
3. Whether an independent persistent scope record is required.
4. Candidate discovery mechanism and evidence providers.
5. Exact objective matching semantics/algorithm.
6. Human clarification mechanism for ambiguity/conflict.
7. Duplicate-creation/idempotency mechanism.
8. Scope reassignment, split, and merge semantics.
9. Objective mutation semantics.
10. Exact lifecycle-to-continuation eligibility rules.
11. Agent/Environment mechanism for supplying binding evidence.
12. Multi-project empirical validation.

## 26. Gate Decision

### Process Binding Design — COMPLETE

This design establishes:

- Process Instance binding terminology;
- candidate sources and eligibility;
- matching semantics;
- deterministic selection requirements;
- existing Process Instance continuation;
- direct Process Instance recovery;
- new Process Instance creation;
- duplicate-creation semantics;
- scope/Process Instance invariants;
- objective relationship;
- rebinding/mutation boundaries;
- Runtime authority;
- Agent and Execution Environment boundaries;
- persistence/recovery requirements;
- explicit failure/uncertainty semantics;
- traceability;
- decision matrix;
- reconciliation with existing empirical evidence;
- alternatives and deferred questions.

No Runtime API, ProcessStore schema, matching implementation, Agent bridge change, or new persistence mechanism is introduced by this gate.

## 27. Next Authorized Work

> **Persistence Scope Design**

The next work must define the minimum durable representation required for Engineering Scope Identity and Process Instance binding, how it integrates with the existing ProcessStore, what information must survive process/environment replacement, and how binding traceability is persisted.

Authorized progression:

```
Project / Scope Resolution Design ✓
        ↓
Process Binding Design ✓
        ↓
Persistence Scope Design
        ↓
Agent / Environment Mechanism Design
        ↓
Normative Documentation Reconciliation
        ↓
Implementation
        ↓
Multi-Project Validation
```
