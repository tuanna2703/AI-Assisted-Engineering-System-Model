# AESM Operational Model

**Project:** AI-Assisted Engineering System Model (AESM)  
**Phase:** Operationalization — Phase 2  
**Status:** Initial Normative Draft  
**Derived from:** Engineering Process Model (EPM) and Process Execution Model (PEM), together with `analysis/AESM Operationalization Analysis.md`

---

## 1. Purpose

The AESM Operational Model defines the implementation-independent operational structure required to execute the Engineering Process Model (EPM) according to the Process Execution Model (PEM).

It is the normative bridge between the semantic specifications and later machine-readable schemas, Agent Execution Contract, protocol, Runtime, and conformance artifacts.

It defines:

- operational entities;
- their required properties and relationships;
- lifecycle and state semantics;
- permitted classes of operations;
- validation responsibilities;
- persistence and continuity requirements;
- information that must be observable to participating Agents and Humans.

It does **not** define a programming language, database, API framework, Agent framework, IDE integration, or concrete Runtime architecture.

---

## 2. Authority and Layering

AESM is layered as follows:

```text
EPM
  ↓
PEM
  ↓
AESM Operational Model
  ↓
Machine-readable Model / Protocol
  ↓
Runtime Implementation
  ↓
Environment / Agent Adapter
```

The authority of the layers is preserved:

- **EPM** defines engineering meaning and validity.
- **PEM** defines execution semantics and control.
- **Operational Model** defines how those semantics are represented and operated upon.
- **Machine-readable artifacts** provide implementation-consumable representations of the operational model.
- **Runtime** implements PEM using the operational model.
- **Agent and Environment adapters** expose capabilities without redefining AESM semantics.

A lower layer MUST NOT silently redefine a higher layer.

---

## 3. Core Operational Principles

### 3.1 Semantic Preservation

Operational representations MUST preserve distinctions established by EPM and PEM.

### 3.2 Authoritative State

The Process Instance's Execution Context is the authoritative operational state required to continue execution.

### 3.3 Controlled Mutation

Authoritative state MUST NOT be modified by arbitrary Agent output. Changes MUST pass through applicable execution and validation rules.

### 3.4 Explicit Knowledge Status

Known information, Evidence, Assumptions, unresolved matters, contested information, and invalidated information MUST remain distinguishable.

### 3.5 Traceability

Material changes to engineering knowledge and execution state MUST remain traceable.

### 3.6 Environment Independence

The model MUST NOT require VS Code, a specific Agent framework, database, programming language, or tool protocol.

### 3.7 Continuity

Execution MUST be resumable from persisted operational state without dependence on a previous conversational context window.

### 3.8 Engineering Validity vs Execution Control

Engineering validity belongs to EPM. Execution control belongs to PEM. The operational layer MUST preserve that boundary.

---

## 4. Operational Entity Model

The operational model consists of the following primary entity classes.

```text
Process Instance
├── Engineering Objective
├── Execution Context
│   ├── Process State
│   ├── Engineering State
│   ├── Decision State
│   ├── Knowledge State
│   └── Continuity State
├── Engineering Knowledge
│   ├── Requirements
│   ├── Constraints
│   ├── Evidence
│   ├── Assumptions
│   ├── Risks
│   ├── Candidate Solutions
│   ├── Evaluations
│   ├── Engineering Decisions
│   ├── Verification Results
│   └── Artifacts
├── Execution Records
│   ├── Execution Determinations
│   ├── Execution Actions
│   ├── Execution Results
│   └── Execution Trace
└── Participants
    ├── Human Participants
    └── AI Agents
```

This hierarchy is logical. Physical storage MAY use a different structure provided semantic relationships and required behavior are preserved.

---

# 5. Process Instance

## 5.1 Definition

A Process Instance represents one execution of an EPM for a specific Engineering Objective.

## 5.2 Required Properties

A Process Instance MUST have, at minimum:

- unique identity;
- applicable EPM identity/version;
- applicable PEM identity/version;
- Engineering Objective;
- lifecycle status;
- current Execution Context reference or embedded representation;
- creation/initialization information;
- execution history or reference to it.

Additional properties MAY be implementation-specific when they do not affect semantic interoperability.

## 5.3 Relationships

A Process Instance MUST be able to reference or contain:

- its Engineering Objective;
- its current Execution Context;
- relevant Requirements and Constraints;
- Evidence and Assumptions;
- Engineering Decisions;
- Verification results;
- Artifacts;
- Risks;
- Participants;
- Execution Trace.

## 5.4 Lifecycle

A Process Instance MUST support at least these logical conditions:

```text
Initialized
   ↓
Active
   ↓
Suspended / Interrupted
   ↓
Resumed
   ↓
Active
   ↓
Completed OR Terminated
```

The exact status vocabulary is to be normalized by the later machine-readable model, but Runtime termination MUST remain distinct from Engineering Process Completion.

## 5.5 Initialization

Initialization MUST establish enough state to begin execution without inventing engineering facts.

At initialization:

- the Engineering Objective MUST be identified;
- the applicable EPM and PEM MUST be known;
- the initial Process State MUST be established according to EPM/PEM rules;
- unknown Requirements, Evidence, Assumptions, or other knowledge MUST NOT be represented as established facts merely because they are absent.

---

# 6. Execution Context

## 6.1 Definition

Execution Context is the authoritative operational state required to continue a Process Instance consistently from a specific point in execution.

It is a logical construct, not a prescribed storage mechanism.

## 6.2 Required Components

Execution Context MUST provide, directly or through authoritative references, the following logical components:

### Process Status

- Process Instance identity;
- current execution status;
- current Process State;
- execution mode;
- current lifecycle condition.

### Engineering State

- Engineering Objective;
- relevant Requirements;
- Constraints;
- Evidence;
- Assumptions;
- Risks;
- Candidate Solutions;
- Evaluations;
- unresolved engineering matters;
- relevant Artifacts.

### Decision State

- accepted Engineering Decisions;
- pending/proposed Decisions;
- affected Decisions requiring reconsideration;
- applicable Decision Gates;
- decisions relevant to current execution.

### Knowledge State

- relevant known Evidence;
- Evidence provenance/context where available;
- Assumptions and their status;
- unresolved or contested information;
- invalidated knowledge;
- verification results.

### Continuity State

- last authoritative update;
- pending execution condition/activity;
- relevant execution history/reference;
- interruption/resumption information;
- information required to continue without conversational memory.

## 6.3 Completeness

Execution Context MUST contain or reference all operational information necessary for a conforming Runtime to determine what execution state currently exists and to continue according to PEM rules.

## 6.4 Consistency

A Runtime MUST validate that the Execution Context is internally consistent before treating it as authoritative.

Examples of consistency conditions include:

- current Process State is valid for the Process Instance;
- referenced Decisions exist and have valid status;
- required relationships are resolvable;
- lifecycle status does not contradict completion state;
- invalidated knowledge is not simultaneously represented as accepted Evidence without an explicit later validity determination.

## 6.5 Portability

The logical Execution Context MUST be representable independently of a Runtime's transient memory or process.

A compatible Runtime MUST be able to reconstruct equivalent operational state from the persisted representation.

---

# 7. Process State

## 7.1 Ownership

Process State semantics are owned by EPM. PEM executes those semantics.

## 7.2 Operational Representation

The active Process State MUST identify:

- state identity;
- applicable state definition;
- entry condition status;
- current work/condition status;
- applicable progression conditions;
- applicable Decision Gates;
- applicable verification conditions;
- applicable reconsideration conditions;
- valid exit/transition conditions.

## 7.3 State Evaluation

The Runtime MUST be able to determine whether the current Process State permits progression, requires additional work, requires reconsideration, or is complete according to the applicable EPM semantics.

---

# 8. Transition

## 8.1 Definition

A Transition represents a movement between Process States that is permitted by the applicable EPM and executed under PEM control.

## 8.2 Required Properties

A Transition MUST identify:

- source state;
- target state;
- triggering/qualifying conditions;
- required Decision Gates, where applicable;
- required verification conditions, where applicable;
- transition result/status;
- basis/trace reference.

## 8.3 Validity

A Runtime MUST NOT perform a Transition that violates applicable EPM conditions.

Completion of an activity or Agent request alone MUST NOT establish Transition validity.

## 8.4 Transition Record

A completed Transition MUST be traceable to:

- the prior state;
- the resulting state;
- the conditions evaluated;
- the relevant Evidence/verification where applicable;
- the execution event that caused the transition.

---

# 9. Decision Gate

## 9.1 Definition

A Decision Gate is an EPM-defined condition that controls whether execution may progress beyond a particular point.

## 9.2 Operational Properties

A gate MUST identify:

- gate identity;
- applicable Process State/context;
- required inputs or conditions;
- evaluation status;
- result;
- basis or supporting references;
- evaluation history.

## 9.3 Evaluation Results

The operational model MUST distinguish at least:

```text
Satisfied
Not Satisfied
Not Yet Determinable
Not Applicable
```

The exact final vocabulary may be refined during machine-readable schema design.

## 9.4 Enforcement

If a required Decision Gate is not satisfied, the Runtime MUST prevent any Transition that depends on that gate.

---

# 10. Progression Condition

A Progression Condition represents an EPM-defined condition required for valid advancement.

A Progression Condition MUST be:

- identifiable;
- associated with the applicable state or transition;
- evaluable using available operational state;
- associated with an evaluation result;
- traceable to the Evidence, Decision, verification, or other state that supports the result.

Progression MUST be determined from applicable conditions rather than from superficial activity completion.

---

# 11. Engineering Knowledge Model

## 11.1 General Rule

Engineering knowledge entities MUST retain their semantic identity and MUST NOT be collapsed into a generic `task`, `note`, or `message` representation when doing so would lose EPM meaning.

## 11.2 Requirement

A Requirement MUST support:

- identity;
- statement/content;
- status;
- relevant source/context;
- relationships to Constraints, Evidence, Solutions, Decisions, and verification where applicable;
- history/traceability.

## 11.3 Constraint

A Constraint MUST support:

- identity;
- statement/content;
- scope/applicability;
- status;
- affected engineering entities;
- history/traceability.

## 11.4 Evidence

Evidence MUST support:

- identity;
- content or reference;
- provenance/context where available;
- relevance;
- status;
- relationships to the conclusions, evaluations, Decisions, or verification results it supports.

Evidence MUST NOT be silently replaced by an unsupported conclusion.

## 11.5 Assumption

An Assumption MUST support:

- identity;
- proposition/content;
- status;
- affected engineering entities;
- invalidation/resolution history.

## 11.6 Risk

A Risk MUST support:

- identity;
- description;
- affected engineering entities;
- status;
- treatment/response where applicable;
- history.

## 11.7 Candidate Solution

A Candidate Solution MUST support:

- identity;
- description;
- relevant Requirements;
- relevant Constraints;
- evaluation status;
- relationship to resulting Engineering Decisions.

## 11.8 Evaluation

An Evaluation MUST support:

- evaluated subject;
- applicable criteria/basis;
- Evidence and Constraints considered;
- result;
- relationship to resulting conclusions or Decisions.

## 11.9 Engineering Decision

An Engineering Decision MUST support:

- identity;
- decision/conclusion;
- status;
- rationale/basis;
- supporting Evidence;
- affected Requirements, Constraints, Risks, Solutions, or Artifacts;
- reconsideration status/history.

An Engineering Decision MUST NOT be inferred solely from an Agent message or Execution Determination.

## 11.10 Verification Result

A Verification Result MUST support:

- identity;
- verification target;
- applicable criteria;
- method/activity reference;
- result;
- status;
- supporting Evidence;
- effect on applicable progression conditions.

## 11.11 Artifact

An Artifact MUST support:

- identity;
- representation/reference;
- status;
- relevant version/history;
- relationships to the engineering work that produced or depends upon it.

---

# 12. Execution Model

## 12.1 Execution Cycle

A Runtime SHALL implement the PEM execution cycle:

```text
Observe
   ↓
Evaluate
   ↓
Plan
   ↓
Execute
   ↓
Verify
   ↓
Update Context
   ↓
Repeat
```

The operational model represents the information exchanged and state changes required by this cycle. It does not turn the cycle into a fixed engineering workflow.

## 12.2 Execution Determination

An Execution Determination represents the Runtime-level determination of what execution condition/action is currently permissible or required.

It MUST remain distinct from Engineering Decision.

It may identify, for example:

- an action that can proceed;
- an information gap blocking execution;
- a required verification;
- a required reconsideration;
- a prohibited transition;
- a completion condition.

## 12.3 Execution Action

An Execution Action represents an operational activity undertaken as part of PEM execution.

It MUST be associated with:

- the relevant Process Instance;
- current Execution Context;
- purpose/basis;
- actor or Agent where applicable;
- resulting Execution Result.

An Execution Action is not itself proof of engineering validity.

## 12.4 Execution Result

An Execution Result records what resulted from an Execution Action.

It MAY produce or reference:

- observations;
- Evidence;
- Artifact changes;
- verification results;
- execution errors;
- proposed state changes;
- requests for further work.

The Runtime MUST validate which results can affect authoritative state.

---

# 13. Participant Model

## 13.1 Participant

A Participant represents an entity contributing to execution.

## 13.2 AI Agent

An AI Agent is a Participant operating within the process. It is not the Runtime.

The operational model MUST preserve this distinction.

## 13.3 Participant Contribution

A Participant contribution MUST be attributable to its source and MUST be classifiable according to its semantic role.

Examples include:

- observation;
- analysis;
- Evidence;
- Assumption;
- Candidate Solution;
- Evaluation;
- proposed Decision;
- Artifact change;
- verification result;
- request for clarification.

A contribution becomes part of authoritative engineering state only through the applicable validation and execution rules.

## 13.4 Authority

Participant capability and Participant authority MUST remain separate properties.

An Agent having access to a tool does not automatically have authority to perform every engineering action or establish every Decision.

---

# 14. Agent Visibility Boundary

The Agent-facing representation MUST expose sufficient information for the Agent to participate meaningfully in current execution.

At minimum, an Agent may require access to:

- Process Instance identity;
- Engineering Objective;
- current Process State;
- relevant Requirements and Constraints;
- relevant Evidence;
- Assumptions;
- Risks;
- Candidate Solutions and evaluations where applicable;
- accepted/pending Engineering Decisions;
- verification status;
- Decision Gates;
- progression conditions;
- unresolved matters;
- relevant Artifacts;
- execution scope;
- current continuity state.

The exact message format is intentionally deferred to the Agent Execution Contract.

The Agent MUST NOT be required to reconstruct authoritative process state solely from conversational history.

---

# 15. Controlled State Mutation

All authoritative state mutation MUST follow this conceptual sequence:

```text
Candidate Contribution / Execution Result
                ↓
          Classification
                ↓
       Semantic Validation
                ↓
       Execution Validation
                ↓
        State Determination
                ↓
        Authoritative Update
                ↓
          Trace Recording
```

The exact implementation mechanism is not prescribed.

This sequence prevents raw Agent output, tool output, or environmental events from silently becoming authoritative engineering state.

---

# 16. Controlled Reconsideration

When material new information affects prior engineering conclusions, the operational model MUST support controlled reconsideration.

The minimum operational sequence is:

```text
New Evidence / Change
        ↓
Identify affected entities
        ↓
Evaluate impact
        ↓
Mark affected conclusions
        ↓
Return to applicable engineering work
        ↓
Re-evaluate
        ↓
Produce revised conclusion / Decision
        ↓
Preserve prior history
```

Prior Decisions MUST remain historically reconstructable.

A revised Decision MUST NOT erase the fact that an earlier Decision existed.

---

# 17. Verification and Failure Handling

Verification results are operationally significant when they affect EPM progression conditions.

A failed verification MUST be representable as a state-affecting result.

Where verification is required for progression, a failed or unresolved verification MUST prevent invalid progression.

The Runtime MUST permit subsequent work required by the EPM, which may include investigation, Artifact modification, reconsideration, or re-verification.

---

# 18. Execution Trace

## 18.1 Purpose

Execution Trace records material execution and engineering-state evolution so that the Process Instance remains auditable and recoverable.

## 18.2 Traceable Events

At minimum, the trace SHOULD support records for:

- Process Instance initialization;
- state evaluation;
- state transitions;
- Decision Gate evaluations;
- progression-condition evaluations;
- Execution Determinations;
- Execution Actions;
- Execution Results;
- Participant contributions;
- Evidence additions/changes;
- Assumption changes;
- Engineering Decisions;
- verification results;
- Artifact changes;
- reconsideration events;
- interruption/resumption;
- completion/termination.

## 18.3 State vs History

Execution Context represents current authoritative operational state.

Execution Trace represents material historical evolution.

They MUST NOT be treated as interchangeable.

---

# 19. Persistence and Recovery

## 19.1 Logical Requirement

A conforming implementation MUST be able to persist sufficient Process Instance state and restore it later.

## 19.2 Recovery

After interruption, the Runtime MUST be able to reconstruct the authoritative Execution Context without depending on the prior Agent's transient memory.

## 19.3 Equivalence

A successful restoration MUST preserve operationally significant identity, relationships, state, and traceability.

## 19.4 Physical Storage

The operational model does not prescribe:

- filesystem layout;
- database technology;
- serialization library;
- cloud service;
- IDE storage mechanism.

These belong to implementations and environment adapters.

---

# 20. Completion, Suspension, and Termination

The operational model MUST represent separately:

```text
Engineering Process Completion
Runtime Suspension / Interruption
Runtime Termination
```

A Runtime MAY terminate while engineering remains incomplete.

Engineering Process Completion MUST be established according to EPM completion semantics.

Only then may Runtime termination be interpreted as termination after successful completion rather than simple execution cessation.

---

# 21. Environment Boundary

The Execution Environment provides capabilities used during execution.

The operational model MUST NOT encode VS Code-specific or tool-specific assumptions.

An environment may expose capabilities such as:

```text
read file
write file
search repository
run command
run test
inspect version control
```

but these capabilities are environment-level mechanisms, not EPM entities.

An environment adapter MUST map available capabilities into the execution interface without changing EPM/PEM validity semantics.

---

# 22. Validation Responsibilities

Validation occurs at multiple levels.

## 22.1 Structural Validation

Determines whether an operational representation satisfies its required structure and relationships.

## 22.2 Semantic Validation

Determines whether a proposed state or knowledge update is consistent with EPM semantics.

## 22.3 Execution Validation

Determines whether the proposed action or transition is permitted under PEM control.

## 22.4 Persistence Validation

Determines whether stored state can be safely restored as authoritative operational state.

## 22.5 Conformance Validation

Determines whether an implementation satisfies the normative EPM/PEM/Operational Model requirements.

These validation levels MUST remain conceptually distinct even if a Runtime combines them in one implementation component.

---

# 23. Operation Classes

The operational model defines operation classes rather than implementation-specific APIs.

### Lifecycle Operations

- initialize Process Instance;
- load Process Instance;
- suspend execution;
- resume execution;
- complete Process Instance;
- terminate Runtime execution.

### Observation Operations

- inspect current Execution Context;
- inspect applicable Process State;
- inspect relevant engineering knowledge;
- inspect applicable gates and progression conditions.

### Evaluation Operations

- evaluate Process State;
- evaluate Decision Gate;
- evaluate progression condition;
- evaluate verification result;
- evaluate impact of new Evidence.

### Contribution Operations

- submit observation;
- submit Evidence;
- submit Assumption;
- submit analysis;
- submit Candidate Solution;
- submit Evaluation;
- propose Engineering Decision;
- submit verification result;
- submit Artifact result.

### Execution Operations

- establish Execution Determination;
- authorize/perform applicable Execution Action;
- record Execution Result;
- update Execution Context;
- record trace event.

### Reconsideration Operations

- identify affected conclusions;
- initiate reconsideration;
- revise applicable engineering state;
- record revised Decision;
- preserve historical state.

These operation classes will become concrete interface operations only in later artifacts.

---

# 24. Required Invariants

A conforming operational implementation MUST preserve at least these invariants:

1. **EPM authority invariant** — engineering validity cannot be redefined by Runtime convenience or Agent output.
2. **PEM execution invariant** — execution follows PEM semantics.
3. **Context authority invariant** — authoritative operational continuation state is represented by Execution Context.
4. **Agent boundary invariant** — Agent is not synonymous with Runtime.
5. **Decision distinction invariant** — Engineering Decision and Execution Determination remain distinct.
6. **Completion distinction invariant** — Engineering Completion and Runtime Termination remain distinct.
7. **Knowledge distinction invariant** — Evidence, Assumptions, unknowns, and conclusions remain distinguishable.
8. **Traceability invariant** — material changes remain reconstructable.
9. **Continuity invariant** — execution can resume without conversational memory.
10. **Environment independence invariant** — execution semantics do not depend on a specific IDE or tool environment.
11. **Controlled mutation invariant** — raw participant or environment output does not silently become authoritative state.
12. **Reconsideration invariant** — revised conclusions preserve prior history.

---

# 25. Machine-Readable Derivation Requirements

The later machine-readable model MUST faithfully represent the concepts defined here.

It MUST provide, where applicable:

- stable entity identities;
- typed relationships;
- explicit lifecycle/status representation;
- references between current state and historical trace;
- validation constraints;
- representation of unknown/unresolved state;
- representation of gate/progression evaluation;
- representation of Agent-visible execution context;
- persistence-compatible serialization;
- versioning sufficient to identify the applicable AESM model.

Concrete serialization format is intentionally deferred until the machine-readable design phase.

---

# 26. Agent Execution Contract Derivation Requirements

The later Agent Execution Contract MUST be derived from this model.

At minimum it must specify:

### AESM → Agent

- current execution context;
- relevant engineering state;
- applicable execution conditions;
- permitted scope/capabilities;
- required outputs or pending decisions;
- continuity information needed for the current execution step.

### Agent → AESM

- structured observations and analysis;
- Evidence and provenance/context where available;
- explicit Assumptions;
- Candidate Solutions;
- Evaluations;
- proposed Engineering Decisions;
- Artifact changes/results;
- verification results;
- execution outcomes;
- requests for information or clarification.

The Agent Contract MUST define how these contributions are distinguished from authoritative state changes.

---

# 27. Implementation Independence

This model intentionally does not prescribe:

- LLM provider;
- Agent framework;
- IDE;
- operating system;
- programming language;
- database;
- filesystem layout;
- API transport;
- message broker;
- cloud platform.

A conforming implementation may choose any of these while preserving the operational semantics.

---

# 28. Repository Boundary

AESM model artifacts and individual engineering execution data are separate concerns.

The AESM repository stores the model, specifications, schemas, protocols, and conformance artifacts.

An engineering project's execution environment stores its Process Instances, Execution Contexts, traces, and project-specific engineering artifacts according to the chosen Runtime implementation.

Conceptually:

```text
AESM Repository
    = system definition

Engineering Project Workspace / State Store
    = execution governed by that system
```

The operational model MUST preserve this distinction.

---

# 29. Open Items for Subsequent Phases

The following items remain intentionally unresolved because they belong to later artifacts:

1. exact field-level schema for every entity;
2. canonical machine-readable serialization format;
3. exact Agent message/request/response structures;
4. concrete protocol transport;
5. Runtime API surface;
6. environment capability interface;
7. conformance test format;
8. physical Process Instance storage layout.

These are not omissions from the operational model. They are deliberate implementation-level deferrals.

---

# 30. Phase 2 Completion Criteria

The AESM Operational Model is considered complete when:

- all operational requirement classes from the Phase 1 analysis have corresponding model treatment;
- Process Instance and Execution Context are operationally defined;
- state and transition semantics are operationally represented without redefining EPM;
- engineering knowledge entities retain their semantic distinctions;
- Agent/Participant and Runtime boundaries are explicit;
- controlled state mutation is defined;
- traceability, persistence, interruption, resumption, and reconsideration are operationally represented;
- environment independence is preserved;
- invariants are explicit;
- the model provides sufficient normative detail to derive machine-readable schemas and the Agent Execution Contract without inventing core semantics.

Upon satisfaction of these criteria, the next phase is **Phase 3 — Machine-Readable AESM Model**.
