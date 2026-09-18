# Project / Scope Resolution Design

**Status:** Design complete — pending gate review  
**Work unit:** Project / Scope Resolution Design  
**Predecessor:** `execution/ENGINEERING-SCOPE-IDENTITY-SEMANTICS.md`

## 1. Design Question

Define how AESM resolves an Engineering Request to an Engineering Scope Identity and then to an applicable Process Instance without collapsing scope identification, Process Instance discovery, context recovery, and execution.

```
Engineering Request → Scope Resolution → Engineering Scope Identity
→ Process Instance Resolution → Context Recovery / Creation → Execution
```

This is a semantic/design artifact. It does not introduce a Project entity, Runtime API, repository detector, workspace detector, or persistence technology.

## 2. Semantic Prerequisites

Established semantics used here:
- Engineering Objective identifies intended engineering work.
- Engineering Scope Identity identifies the stable engineering boundary.
- Process Instance Identity identifies one concrete engineering execution.
- Execution Context is authoritative operational state.
- Runtime owns authoritative Process Instance discovery and control.
- Agent participation does not transfer Runtime authority.
- Execution Environment supplies capabilities/evidence, not semantic authority.
- Repository/workspace identity is evidence, not universal scope identity.
- One scope may contain multiple Process Instances.
- A Process Instance may span multiple repositories where its objective requires it.
- Known Process Instance identity remains a valid direct recovery mechanism.
- Ambiguity must remain explicit.

## 3. Resolution Terminology

**Engineering Request:** request presented for engineering work.  
**Scope Evidence:** information supporting recognition of an Engineering Scope.  
**Scope Resolution:** authoritative recognition of Engineering Scope Identity.  
**Process Instance Resolution:** selection or creation of the applicable Process Instance after scope resolution.  
**Context Recovery:** recovery of authoritative Execution Context for a selected Process Instance.  
**Continuation:** continuing an existing Process Instance after state recovery.  
**Process Instance Creation:** establishing a new Process Instance when creation conditions are satisfied.

These operations are distinct.

## 4. Inputs and Evidence Classes

| Input | Role | Authority |
|---|---|---|
| Explicit scope identity | Direct identity candidate | Authoritative when supplied through an authoritative channel |
| Known Process Instance ID | Direct execution identity | Authoritative for direct recovery, subject to validation |
| Engineering Objective | Matching/context information | Insufficient by itself |
| Persisted scope binding | Existing authoritative relationship | Authoritative |
| Repository/Git metadata | Scope evidence | Supporting |
| Workspace metadata | Scope evidence | Supporting |
| Artifact locations | Scope evidence | Supporting |
| Agent observation | Participant evidence | Non-authoritative |
| Environment metadata | Context/evidence | Non-authoritative unless explicitly promoted |
| Human clarification | Potential authoritative input | Authoritative through applicable mechanism |

Not every observable input participates in every resolution.

## 5. Evidence Authority

Evidence content and evidence authority are separate.

```
Agent / Environment → Evidence / Proposal → Runtime evaluation
→ Authoritative scope resolution → Process Instance binding
```

Existing authoritative Process Instance scope binding is not silently replaced by environmental evidence.

Evidence should be evaluated for provenance, specificity, freshness, consistency, applicability, and ability to distinguish candidates.

Contradictory authoritative evidence is a conflict, not a reason to silently select a candidate.

## 6. Resolution Algorithm / Model

Conceptual procedure:

1. Receive the Engineering Request.
2. Check for an explicit known Process Instance ID.
3. If present, recover it and validate its authoritative binding.
4. Otherwise identify explicit scope information.
5. Evaluate applicable persisted scope bindings.
6. Evaluate recognized environmental/participant evidence.
7. Determine whether exactly one authoritative scope can be established.
8. If none can be established, return unresolved.
9. If several remain, return ambiguous unless an established rule uniquely distinguishes one.
10. If authoritative evidence conflicts, return conflicting unless an applicable authority rule resolves it.
11. With one scope, resolve the applicable Process Instance.
12. Recover its Context, or create a new Process Instance when creation conditions are satisfied.

Equivalent authoritative inputs and relevant evidence must produce the same result.

Technical convenience, storage order, filesystem order, or first-match behavior is not a legitimate tie-breaker.

## 7. No-Match Behavior

No matching scope does not imply permission to create one.

Default outcome:

**UNRESOLVED**

Automatic scope creation requires a separately defined rule covering authority, creation basis, duplicate prevention, traceability, and Process Instance binding.

This prevents fragmentation caused by insufficient evidence.

## 8. Ambiguity Behavior

If evidence supports multiple scopes:

```
Evidence → Scope A
        → Scope B
```

AESM must not silently choose one.

Permitted resolution mechanisms are additional evidence, explicit human clarification, or an already established deterministic rule. Otherwise the result remains **AMBIGUOUS** and execution requiring authoritative scope binding must not proceed.

## 9. Conflict Behavior

Ambiguity means multiple plausible candidates. Conflict means incompatible authoritative claims.

Example:

```
Persisted binding → Scope A
Authoritative explicit scope → Scope B
```

If no authority rule resolves the conflict:
- do not silently select;
- retain the conflicting evidence;
- block execution requiring the disputed binding;
- require clarification or an applicable resolution rule.

Non-authoritative environmental observations do not override established state.

## 10. Process Instance Selection

Scope resolution and Process Instance resolution remain separate.

After scope resolution, candidates are evaluated using applicable information such as:
- Engineering Scope Identity;
- Engineering Objective;
- explicit Process Instance ID;
- request provenance;
- established Process Instance state;
- other semantically defined distinguishing information.

Objective similarity alone is insufficient when multiple Process Instances may legitimately match.

Do not select by newest, oldest, storage order, accessibility, or workspace proximity.

If several candidates remain indistinguishable, Process Instance resolution is **AMBIGUOUS**.

A completed Process Instance is not automatically selected for a related new request; continuation must be semantically permitted.

## 11. Process Instance Creation

Creation is permitted only when:
1. scope is resolved;
2. objective is established;
3. no applicable existing Process Instance is resolved;
4. creation is permitted for the request;
5. the new Process Instance can be authoritatively bound to the scope.

Creation establishes at minimum:
- Process Instance Identity;
- Engineering Scope binding;
- Engineering Objective;
- applicable EPM binding;
- initial authoritative Context;
- scope-assignment provenance.

Creation is not an ambiguity escape hatch.

## 12. Direct Process Instance Continuation

Known Process Instance ID remains a direct path:

```
Known PI ID → Runtime attach → authoritative Process Instance → Context recovery
```

This may bypass ordinary scope discovery for locating the execution, but not consistency validation.

The Runtime should verify existence, recoverability, binding consistency, and operation compatibility.

Contradictory environmental evidence is traced rather than silently changing the known Process Instance.

## 13. Scope / Process Binding

Normative invariants:
1. Scope Identity ≠ Process Instance Identity.
2. Scope Identity ≠ Engineering Objective.
3. One scope may contain multiple Process Instances.
4. A Process Instance has one authoritative scope binding at a given point in its authoritative history.
5. Environment/Agent changes do not silently change that binding.
6. Binding must survive conversation/session replacement.
7. New Process Instance creation requires an established scope binding when scope is mandatory.
8. Scope ambiguity cannot be converted into arbitrary PI selection.
9. PI discovery cannot fabricate an execution.
10. Direct PI recovery remains valid.

Explicit reassignment, split, and merge mechanisms are future design questions.

## 14. Runtime Authority

Runtime owns the authoritative resolution boundary:
- evaluate applicable evidence;
- resolve scope;
- preserve authoritative bindings;
- resolve Process Instances;
- expose ambiguity/conflict;
- establish bindings for authorized creation;
- recover authoritative Process Instance and Context.

This does not require Runtime to inspect Git, filesystems, IDEs, or a particular environment directly.

## 15. Agent Boundary

The Agent may provide requests, explicit human scope information, observations, proposals, known Process Instance IDs, and requests for continuation/creation/evidence gathering.

The Agent may not independently declare authoritative scope, silently choose an ambiguous scope, rewrite established binding, treat heuristics as AESM identity, or act as the authoritative Process Instance registry.

## 16. Execution Environment Boundary

The environment may expose repository/Git metadata, workspace information, artifact locations, explicit human input, and Runtime access.

These remain evidence/capabilities, not semantic scope definitions.

The design is usable from VS Code, other IDEs, CLI, web environments, and other Agent hosts.

## 17. Persistence Requirements

No storage technology is selected here.

Authoritative persistence eventually needs to preserve, at minimum:

```
Engineering Scope Identity
Scope binding basis / provenance
Relevant resolution evidence
Process Instance Identity
Engineering Objective
```

The authoritative record must support reconstruction of established scope, Process Instance binding, resolution basis, and authorized changes.

A second AESM persistence system is not implied. A first-class persistent scope record is deferred to persistence design.

## 18. Recovery Requirements

Continuity must survive replacement of Agent, conversation, Runtime process, IDE, workspace, and local checkout path.

Recovery relies on authoritative persisted information, not prior conversation.

Repository relocation or workspace recreation changes environmental evidence but does not automatically change scope.

If evidence conflicts with authoritative state, expose the conflict rather than silently creating a new scope.

## 19. Scope-Change Semantics

| Event | Default interpretation |
|---|---|
| Repository moved | Changed evidence; same scope unless explicitly changed |
| Repository renamed | Changed evidence; same scope unless explicitly changed |
| Git remote changed | Changed evidence; no automatic scope change |
| Workspace recreated | Changed environment; same scope may be represented |
| Files reorganized | Changed artifact structure; no automatic scope change |
| Scope split | Explicit semantic decision required |
| Scope merge | Explicit semantic decision required |
| Objective moves to another scope | Explicit assignment/reassignment required |

Environmental change does not itself constitute semantic scope change.

## 20. Failure / Uncertainty Semantics

Required conceptual outcomes:

| Outcome | Meaning |
|---|---|
| **RESOLVED** | One authoritative scope established |
| **UNRESOLVED** | Insufficient information |
| **AMBIGUOUS** | Multiple plausible scopes remain |
| **CONFLICTING** | Authoritative evidence makes incompatible claims |
| **INVALID** | Supplied identity/evidence violates applicable constraints |

These are semantic categories, not yet a mandatory enum/API.

## 21. Traceability Requirements

Authoritative resolution must be reconstructable from persisted state.

The trace should preserve, as applicable:
- request;
- explicit scope;
- candidates;
- evidence and provenance;
- evidence freshness/version where meaningful;
- authority applied;
- resolution result and basis;
- conflicts/ambiguity;
- clarification;
- selected Process Instance;
- creation versus continuation;
- relevant authoritative state/version.

The reconstruction question is:

> Why did AESM resolve this request to this scope and this Process Instance?

The answer must not depend on the original Agent conversation.

## 22. Resolution Decision Matrix

| Scope situation | PI situation | Result |
|---|---|---|
| Explicit authoritative scope, unique | Existing applicable PI | Resolve + recover |
| Explicit authoritative scope, unique | None | Create PI with binding |
| Established persisted binding | Bound PI exists | Preserve + recover |
| No sufficient scope evidence | Any | UNRESOLVED |
| Multiple plausible scopes | Any | AMBIGUOUS unless valid deterministic rule |
| Conflicting authoritative evidence | Any | CONFLICTING unless authority rule |
| Known valid PI ID | PI exists | Direct recovery + validation |
| Known PI + non-authoritative contradiction | PI exists | Recover PI + trace contradiction |
| Known PI + authoritative contradictory scope | PI exists | CONFLICTING unless authority rule |
| Resolved scope + multiple equally applicable PIs | Several | PI ambiguity |
| Resolved scope + no applicable PI | None | Create if preconditions hold |
| Stale/insufficient evidence | Any | UNRESOLVED or gather evidence |
| Completed PI appears related | One | Continue only if semantics permit |

Technical ordering/accessibility never authorizes selection.

## 23. DBP Reconciliation

The historical DBP experiment demonstrated engineering activity but did not establish authoritative AESM scope or Process Instance binding.

The missing chain is:

```
DBP request → scope evidence → scope resolution
→ existing PI resolution OR new PI creation
→ authoritative Context → AESM-governed execution
```

The DBP repository is evidence, not the semantic definition of scope.

The historical `.akg/` mechanism is not AESM Process Instance persistence.

The historical experiment remains unchanged; its missing binding evidence is not retroactively fabricated.

## 24. Alternatives Considered

### Repository = Scope
Rejected as a universal semantic definition because scopes may span repositories, repositories may contain multiple scopes, and repository identity may change.

### Workspace = Scope
Rejected because workspaces are environment-specific and mutable.

### Objective = Scope
Rejected because similar objectives may exist across scopes and one scope may contain multiple objectives.

### Agent-selected scope
Rejected as authoritative resolution.

### Automatic first match
Rejected because technical ordering/accessibility is not semantic authority.

### Automatic new scope on no match
Not adopted; it risks fragmentation and requires a separate creation rule.

### First-class Project entity now
Not required; Engineering Scope Identity expresses the current semantic need without adding unnecessary lifecycle/ownership semantics.

### Direct PI identity only
Insufficient for new requests; it solves continuation, not initial request-to-scope resolution.

## 25. Open Questions

Deferred to subsequent design:
1. Concrete persistent representation of scope identity.
2. Whether an independently managed scope record is eventually required.
3. Initial evidence providers.
4. Evidence-composition rules.
5. Human clarification mechanism.
6. Scope reassignment/split/merge mechanism.
7. Exact PI matching data.
8. Integration with ProcessStore without a second persistence system.
9. Agent/Environment mechanism exposing minimum evidence.
10. Multi-project empirical validation cases.

## 26. Gate Decision

### Project / Scope Resolution Design — COMPLETE

This design establishes the resolution operation, evidence/authority model, deterministic behavior, no-match/ambiguity/conflict semantics, PI selection and creation boundaries, direct recovery, binding invariants, authority boundaries, persistence/recovery requirements, scope-change semantics, traceability, decision matrix, and DBP reconciliation.

No implementation mechanism has been introduced.

A first-class Project entity is not required by this gate.

## 27. Next Authorized Work

> **Process Binding Design**

The next work must define how a resolved Engineering Scope and Engineering Request bind to an existing or newly created Process Instance, including candidate selection, binding invariants, creation/continuation conditions, and authoritative state relationships.

Authorized progression:

```
Project / Scope Resolution Design ✓
        ↓
Process Binding Design
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

Implementation of scope resolution is not authorized by this gate.
