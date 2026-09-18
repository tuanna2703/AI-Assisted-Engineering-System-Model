# Project / Scope Semantics Investigation

**Status:** Complete — semantic gap identified  
**Repository:** `tuanna2703/AI-Assisted-Engineering-System-Model`  
**Related empirical finding:** `execution/DBP-EMPIRICAL-EXECUTION-REPORT.md`

## 1. Investigation Question

The investigation asked:

> What existing AESM concept represents the engineering scope of a request, how is that scope related to Process Instance identity, and is a new project identity concept actually required?

The investigation was deliberately limited to semantics and existing implementation representation. It did not introduce a Project entity, project identifier, repository detector, workspace detector, persistence mechanism, Runtime API, or Agent guidance change.

## 2. Sources Inspected

The investigation reviewed:

- `docs/01-Overview.md`
- `docs/02-System-Model.md`
- `docs/03-Engineering-Model.md`
- `docs/04-Execution-Model.md`
- `docs/05-Process-Instance-and-Execution-Context.md`
- `docs/06-Participants-and-Agent-Participation.md`
- `docs/07-Runtime-and-Conformance.md`
- `docs/08-Continuity-Traceability-and-Reconsideration.md`
- `docs/09-Operational-Guide.md`
- `docs/10-Reference.md`
- `docs/Agent-Execution-Integration.md`
- `runtime/core/models.py`
- `runtime/core/runtime.py`
- `runtime/core/store.py`
- the completed Agent–Runtime bridge and mechanism-validation evidence
- the DBP empirical execution evidence

## 3. Existing Semantic Model

### Engineering Objective

The EPM defines Engineering Objective as the purpose from which engineering execution begins.

The current model states that:

- a Process Instance represents one execution of the EPM for a specific engineering objective;
- the objective remains explicit and traceable;
- the objective is not silently changed by an Agent or Runtime.

Therefore:

```
Engineering Objective
        ↓
Process Instance purpose
```

This is an important identity dimension, but it describes **what the execution is intended to accomplish**, not necessarily **which engineering scope it belongs to**.

### Process Instance

The Process Instance is the persistent identity of one engineering execution.

The current semantic model explicitly makes it independent of:

- Agent;
- conversation;
- Agent context window;
- IDE session;
- Runtime process lifetime;
- Execution Environment.

The concrete model currently contains:

- `process_instance_id`;
- `engineering_objective`;
- lifecycle;
- Execution Context reference;
- EPM metadata;
- PEM metadata;
- timestamps.

There is no project/scope identity field.

### Execution Context

Execution Context is authoritative operational state required to continue the Process Instance.

It contains the engineering objective, process state, requirements, constraints, evidence, decisions, artifacts, verification, continuity information, and related state.

It does not currently define an independent project/scope identity.

### EPM Binding

The EPM binding identifies the applicable engineering semantics for the Process Instance.

It does not identify which repository, workspace, product, project, or external engineering scope the objective concerns.

### Execution Environment

The Execution Environment is explicitly modeled as a replaceable interaction/tooling surface.

It may be an IDE, CLI, cloud/web development environment, or another surface.

It is not an AESM semantic authority and does not currently have a normative project identity role.

## 4. Existing Runtime Model

The concrete Runtime currently provides:

- `create_process(objective)`;
- `attach(process_instance_id)`;
- Context access;
- Runtime-mediated operations;
- ProcessStore-backed persistence.

The Runtime documentation explicitly makes Process Instance discovery a Runtime responsibility.

However, the current implementation does not provide an objective/scope-based discovery mechanism.

The practical distinction is:

```
Known Process Instance ID
        ↓
Runtime attach
        ↓
Process Instance
```

rather than:

```
Engineering request + scope
        ↓
Runtime resolution
        ↓
appropriate Process Instance
```

The second chain is not currently semantically or operationally defined.

## 5. Existing Agent / Environment Boundary

The Agent–Runtime integration correctly establishes that:

- the Agent is a Participant;
- the Execution Environment provides interaction/tooling capabilities;
- the bridge mediates access to Runtime;
- Runtime owns Process Instance identity and discovery;
- the Execution Environment must not independently search persistence and declare its own Process Instance association authoritative.

The missing capability is therefore not permission for the Agent to choose a Process Instance.

The missing capability is:

> **A deterministic way to establish which engineering scope a new request belongs to before Runtime-owned Process Instance discovery can occur.**

## 6. Repository and Workspace Findings

The existing AESM model does not define either:

```
Repository = Project
```

or:

```
Workspace = Project
```

Neither repository identity nor workspace identity is currently an authoritative AESM semantic entity.

Therefore the investigation cannot justify selecting either as the project identity.

This also means that introducing repository detection or workspace detection at the Runtime layer now would reverse the intended decision order.

## 7. Scope Adequacy Assessment

| Existing concept | What it identifies | Can it uniquely establish engineering scope? |
|---|---|---|
| Engineering Objective | Intended engineering purpose | No |
| Process Instance ID | One concrete engineering execution | No; it is the result of identification, not scope resolution |
| Execution Context | Current authoritative operational state | No current scope identity |
| EPM binding | Applicable engineering semantics | No |
| Execution Environment | Interaction/tooling surface | No |
| Repository | Potential environmental evidence | Not currently an AESM identity |
| Workspace | Potential environmental evidence | Not currently an AESM identity |

## 8. Critical Distinction

The investigation found an important distinction:

> **Engineering Objective is not equivalent to Engineering Scope Identity.**

For example, two separate engineering requests may have materially similar objectives:

```
"Implement feature X"
```

while operating against different engineering scopes:

```
Scope A
Scope B
```

The objective alone therefore cannot safely establish:

```
request → correct Process Instance
```

when multiple plausible scopes exist.

## 9. Required Semantic Relationship

The current model establishes:

```
Engineering Objective
        ↓
Process Instance
        ↓
Execution Context
```

The empirical DBP finding exposes the need for an additional semantic relationship:

```
Engineering Objective
        ↓
Engineering Scope Identity
        ↓
Process Instance
        ↓
Execution Context
```

This does **not** yet imply that the new concept must be named `Project`.

The concept may ultimately represent:

- a project;
- a product/system boundary;
- a repository-independent engineering scope;
- another stable engineering identity;
- or a composition of stable identifiers.

That determination belongs to the next semantic gate.

## 10. Layer Responsibility

The investigation preserves the established AESM separation:

| Concern | Semantic owner |
|---|---|
| Engineering meaning | EPM |
| Execution semantics | PEM |
| Authoritative Process Instance discovery | Runtime |
| Authoritative operational state | Process Instance / Execution Context |
| Engineering contribution | Participant under applicable rules |
| Environmental evidence/capability | Execution Environment |

A new scope identity must therefore be defined semantically before Runtime mechanisms are implemented.

## 11. DBP Reconciliation

The DBP experiment demonstrated engineering activity without establishing an authoritative project-to-Process-Instance association.

The current AESM model explains why this gap exists:

- the Process Instance can be created when its objective is known;
- the Runtime can recover it when its identifier is known;
- but AESM currently does not define how a fresh request obtains a stable engineering scope identity from which the correct Process Instance can be resolved.

This is a semantic capability gap, not merely a missing convenience API.

## 12. Decision

**Finding: A new Engineering Scope Identity semantic concept is required.**

However:

**No decision has yet been made that the concept must be a named `Project` entity.**

The next work must define Engineering Scope Identity before deciding its concrete representation.

The authorized sequence is therefore:

```
Project/Scope Semantics Investigation
        ↓
Engineering Scope Identity definition
        ↓
Representation decision
        ↓
Project Resolution
        ↓
Process Binding
        ↓
Persistence
        ↓
Implementation
```

## 13. Explicit Non-Decisions

This investigation does **not** decide:

- Project = Git repository;
- Project = workspace;
- one Process Instance = one repository;
- one Process Instance may or may not span repositories;
- persistence is repository-local;
- persistence is external;
- Runtime should inspect Git;
- Agent should choose Process Instances;
- Execution Environment owns scope identity;
- a `project_id` field should be added to Process Instance.

Those questions remain for the next semantic gate.

## 14. Gate Decision

### **Project/Scope Semantics Investigation — COMPLETE**

The evidence is sufficient to establish:

1. the existing Engineering Objective is insufficient as a scope identity;
2. Process Instance identity is the identity of the execution, not the external engineering scope;
3. repository/workspace identity is not currently an AESM semantic authority;
4. Runtime remains authoritative for Process Instance discovery;
5. a stable Engineering Scope Identity concept must be defined before project resolution can be designed.

### Next authorized work

**Project/Scope Semantic Clarification**

The next work must define the semantics of Engineering Scope Identity and determine whether a named `Project` entity is required.
