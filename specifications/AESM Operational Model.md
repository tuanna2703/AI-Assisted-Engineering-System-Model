# AESM Operational Model

**Project:** AI-Assisted Engineering System Model (AESM)  
**Phase:** Operationalization — Phase 2  
**Status:** Revised Normative Draft — Review Revision 1  
**Derived from:** Engineering Process Model (EPM), Process Execution Model (PEM), and `analysis/AESM Operationalization Analysis.md`

---

## 1. Purpose

The AESM Operational Model defines the implementation-independent operational structure required to execute the Engineering Process Model (EPM) according to the Process Execution Model (PEM).

It is the normative bridge between the semantic specifications and later machine-readable schemas, Agent Execution Contract, protocol, Runtime, and conformance artifacts.

It defines:

- operational entities;
- required properties and relationships;
- lifecycle and state semantics;
- permitted classes of operations;
- validation responsibilities;
- persistence and continuity requirements;
- Agent and Human visibility requirements;
- boundaries between engineering meaning, execution control, and environment capabilities.

It does not prescribe a programming language, database, API framework, Agent framework, IDE integration, serialization technology, or concrete Runtime architecture.

---

## 2. Authority and Layering

```text
EPM
  ↓  engineering meaning and validity
PEM
  ↓  execution semantics and control
AESM Operational Model
  ↓  operational representation and operations
Machine-Readable Model / Protocol
  ↓
Runtime Implementation
  ↓
Environment / Agent Adapter
```

The authority of the layers is preserved:

- **EPM** defines engineering meaning and validity.
- **PEM** defines execution semantics and control.
- **Operational Model** defines how those semantics are represented and operated upon.
- **Machine-readable artifacts** provide implementation-consumable representations.
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

Authoritative state MUST NOT be modified by arbitrary Agent output, tool output, or environment events. Changes MUST pass through applicable validation and execution rules.

### 3.4 Explicit Knowledge Status

Known information, Evidence, Assumptions, unresolved matters, contested information, and invalidated information MUST remain distinguishable.

### 3.5 Traceability

Material engineering changes and execution-state changes MUST remain traceable.

### 3.6 Environment Independence

The model MUST NOT require VS Code, a specific Agent framework, database, programming language, operating system, or tool protocol.

### 3.7 Continuity

Execution MUST be resumable from persisted operational state without dependence on a previous conversational context window.

### 3.8 Engineering Validity vs Execution Control

Engineering validity belongs to EPM. Execution control belongs to PEM. The operational layer MUST preserve this boundary.

### 3.9 Condition-Driven Progression

Completion of an arbitrary activity list MUST NOT by itself establish engineering progression. Progression is determined by applicable EPM conditions, gates, verification, and other validity requirements.

### 3.10 Observation Integrity

Observation MUST NOT itself modify authoritative Process Instance state. Observed information becomes authoritative engineering knowledge only through the applicable validation and state-mutation rules.

---

## 4. Operational Entity Model

The operational model consists of the following primary entity classes.

```text
Process Instance
├── Engineering Objective
├── Execution Mode
├── Execution Context
│   ├── Process Status
│   ├── Engineering State
│   ├── Decision State
│   ├── Knowledge State
│   └── Continuity State
├── Process State Definitions
├── Engineering Knowledge
│   ├── Requirements
│   ├── Constraints
│   ├── Investigations
│   ├── Evidence
│   ├── Assumptions
│   ├── Risks
│   ├── Candidate Solutions
│   ├── Evaluations
│   ├── Engineering Decisions
│   ├── Verification Results
│   └── Artifacts
├── Execution Control
│   ├── Transition Rules
│   ├── Transitions
│   ├── Decision Gates
│   ├── Progression Conditions
│   ├── Execution Determinations
│   ├── Plans
│   ├── Execution Actions
│   ├── Execution Results
│   └── Execution Trace
└── Participants
    ├── Human Participants
    └── AI Agents
```

This hierarchy is logical. Physical storage MAY use another structure provided semantic relationships and required behavior are preserved.

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
- Execution Mode;
- lifecycle status;
- current Execution Context reference or embedded representation;
- initialization information;
- execution history or reference to it.

## 5.3 Initialization

Initialization MUST establish enough state to begin execution without inventing engineering facts.

At initialization:

- the Engineering Objective MUST be identified;
- applicable EPM and PEM MUST be known;
- the initial Process State MUST be established according to EPM/PEM rules;
- Execution Mode MUST be established according to applicable rules;
- unknown Requirements, Evidence, Assumptions, Risks, or other knowledge MUST NOT be represented as established facts merely because they are absent.

## 5.4 Lifecycle

A Process Instance MUST distinguish at least:

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
Engineering Complete
    OR
Runtime Terminated / Execution Abandoned
```

The exact machine-readable status vocabulary is deferred, but Runtime termination MUST remain distinct from Engineering Process Completion.

## 5.5 Objective Change

The Engineering Objective MUST NOT be silently changed.

A material objective change MUST be represented as an explicit event or operation and MUST trigger impact evaluation over affected Requirements, Constraints, Decisions, Candidate Solutions, verification conditions, Risks, and other relevant engineering state.

Where the EPM requires it, affected conclusions MUST enter controlled reconsideration before execution continues.

The prior objective and its history MUST remain traceable.

---

# 6. Execution Context

## 6.1 Definition

Execution Context is the authoritative operational state required to continue a Process Instance consistently from a specific point in execution.

It is a logical construct, not a prescribed storage mechanism.

## 6.2 Required Components

Execution Context MUST provide, directly or through authoritative references:

### Process Status

- Process Instance identity;
- current execution status;
- current Process State;
- Execution Mode;
- current lifecycle condition.

### Engineering State

- Engineering Objective;
- relevant Requirements and their resolution state;
- Constraints;
- Investigations and their current purpose/status;
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

- relevant Evidence and provenance/context where available;
- Assumptions and their status;
- unresolved, contested, or invalidated information;
- verification results;
- other knowledge necessary to interpret current engineering state.

### Continuity State

- last authoritative update;
- pending execution condition/activity;
- current or pending Plan where applicable;
- relevant execution history/reference;
- interruption/resumption information;
- information required to continue without conversational memory.

## 6.3 Completeness

Execution Context MUST contain or reference all operational information necessary for a conforming Runtime to determine the current execution state and continue according to PEM rules.

The `completed work` and `remaining work` aspects of continuity state describe execution continuity only. They MUST NOT be treated as an independent definition of engineering progression.

## 6.4 Consistency

A Runtime MUST validate that Execution Context is internally consistent before treating it as authoritative.

Consistency checks MUST include, where applicable:

- current Process State is valid for the Process Instance;
- lifecycle status is compatible with engineering completion status;
- referenced Decisions and knowledge entities exist and have valid status;
- required relationships are resolvable;
- invalidated information is not simultaneously represented as accepted Evidence without an explicit later validity determination;
- applicable gates and progression conditions are evaluated against the current state.

## 6.5 Portability

The logical Execution Context MUST be representable independently of Runtime transient memory or process state.

A compatible Runtime MUST be able to reconstruct equivalent operational state from persisted representation.

---

# 7. Process State

## 7.1 Ownership

Process State semantics are owned by EPM. PEM executes those semantics.

The Operational Model MUST represent Process State without redefining its engineering meaning.

## 7.2 Operational Representation

The active Process State MUST identify, directly or by reference:

- state identity;
- applicable state definition;
- entry condition status;
- current engineering/execution condition;
- applicable progression conditions;
- applicable Decision Gates;
- applicable verification conditions;
- applicable reconsideration conditions;
- valid Transition Rules.

## 7.3 State Evaluation

The Runtime MUST be able to determine whether the current Process State:

- permits progression;
- requires additional engineering work;
- requires additional execution work;
- requires reconsideration;
- is blocked by an unsatisfied condition;
- is complete according to EPM semantics.

---

# 8. Transition Rule

## 8.1 Definition

A Transition Rule defines the conditions under which movement from one Process State to another is valid.

Transition Rule semantics are derived from EPM and executed under PEM control.

## 8.2 Required Properties

A Transition Rule MUST identify:

- Rule identity;
- applicable source state;
- target state;
- required conditions;
- prohibited conditions where applicable;
- required Decision Gates where applicable;
- required verification conditions where applicable;
- reconsideration conditions where applicable.

## 8.3 Evaluation

A Transition Rule MUST be evaluated against the authoritative Process Instance state before the associated Transition is performed.

An Agent request or completion of an activity MUST NOT override an unsatisfied Transition Rule.

---

# 9. Transition

## 9.1 Definition

A Transition is an occurrence in which the Process Instance moves from one Process State to another under a valid Transition Rule.

## 9.2 Required Properties

A Transition MUST identify:

- source state;
- target state;
- applicable Transition Rule;
- evaluation result;
- transition result/status;
- relevant Evidence, verification, or Decision basis where applicable;
- execution trace reference.

## 9.3 Validity

A Runtime MUST NOT perform a Transition that violates applicable EPM conditions or PEM execution control.

## 9.4 Trace

A completed Transition MUST remain traceable to its prior state, resulting state, evaluated conditions, relevant engineering basis, and execution event.

---

# 10. Decision Gate

## 10.1 Definition

A Decision Gate is an EPM-defined condition that controls whether execution may progress beyond a particular point.

## 10.2 Operational Properties

A gate MUST identify:

- gate identity;
- applicable Process State/context;
- required inputs or conditions;
- evaluation status;
- result;
- supporting basis/references;
- evaluation history.

## 10.3 Evaluation Results

The operational model MUST distinguish at least:

```text
Satisfied
Not Satisfied
Not Yet Determinable
Not Applicable
```

## 10.4 Enforcement

If a required Decision Gate is not satisfied, the Runtime MUST prevent any dependent Transition.

---

# 11. Progression Condition

A Progression Condition represents an EPM-defined condition required for valid advancement.

It MUST be:

- identifiable;
- associated with the applicable state or Transition Rule;
- evaluable using authoritative operational state;
- associated with an evaluation result;
- traceable to supporting Evidence, Decisions, verification, or other relevant state.

Progression MUST be determined from applicable conditions rather than superficial activity completion.

---

# 12. Execution Mode

Execution Mode controls the intended level of engineering rigor without changing the fundamental validity requirements of the EPM.

The operational model MUST support the EPM-defined modes:

- **Direct Mode**;
- **Guided Mode**;
- **Full Mode**.

An Execution Mode representation MUST identify:

- current mode;
- basis for selection where required;
- applicable rigor expectations;
- mode-change history where a change occurs.

A mode change MUST NOT silently weaken an applicable engineering validity condition. Where the EPM requires explicit recognition or reconsideration, the mode change MUST be treated accordingly.

---

# 13. Engineering Knowledge Model

## 13.1 General Rule

Engineering knowledge entities MUST retain their semantic identity. They MUST NOT be collapsed into a generic `task`, `note`, or `message` representation when doing so loses EPM meaning.

## 13.2 Requirement

A Requirement MUST support:

- identity;
- statement/content;
- resolution state;
- satisfaction state where applicable and distinct from resolution;
- source/context;
- relationships to Constraints, Evidence, Investigations, Solutions, Evaluations, Decisions, and verification where applicable;
- history/traceability.

Requirement resolution MUST preserve the EPM distinction:

```text
Open
Contested
Resolved
```

Resolution MUST NOT be interpreted as satisfaction.

## 13.3 Constraint

A Constraint MUST support:

- identity;
- statement/content;
- scope/applicability;
- status;
- affected engineering entities;
- history/traceability.

## 13.4 Investigation

An Investigation is an objective-driven engineering activity intended to reduce material uncertainty.

It MUST NOT be operationalized as a rigid universal task list.

An Investigation MUST support:

- identity;
- objective/purpose;
- uncertainty or engineering question being addressed;
- relevant Process State/context;
- activities or evidence-gathering actions where applicable;
- resulting knowledge;
- status/sufficiency determination where applicable;
- relationships to Evidence, Requirements, Constraints, Assumptions, Risks, Candidate Solutions, Evaluations, Decisions, or verification.

Investigation completion MUST be determined by whether its objective has been sufficiently achieved, not merely by completion of a predetermined list of activities.

## 13.5 Evidence

Evidence MUST support:

- identity;
- content or reference;
- provenance/context where available;
- relevance;
- status;
- relationships to Investigations, Evaluations, Decisions, verification results, and other conclusions it supports.

Observation or Agent output MUST NOT automatically become accepted Evidence.

## 13.6 Assumption

An Assumption MUST support:

- identity;
- proposition/content;
- status;
- affected engineering entities;
- invalidation/resolution history.

## 13.7 Risk

A Risk MUST support:

- identity;
- description;
- affected engineering entities;
- status;
- treatment/response;
- history.

Risk treatment MAY include acceptance, mitigation, avoidance, transfer, investigation, or monitoring as applicable to the EPM context.

## 13.8 Candidate Solution

A Candidate Solution MUST support:

- identity;
- description;
- relevant Requirements;
- relevant Constraints;
- relevant Risks;
- evaluation status;
- relationship to resulting Engineering Decisions.

## 13.9 Evaluation

An Evaluation MUST support:

- evaluated subject;
- Requirements considered;
- Constraints considered;
- Risks considered;
- Evidence considered;
- applicable criteria/basis;
- result;
- relationship to conclusions or Decisions.

## 13.10 Engineering Decision

An Engineering Decision MUST support:

- identity;
- decision/conclusion;
- status;
- rationale/basis;
- supporting Evidence;
- affected Requirements, Constraints, Risks, Solutions, or Artifacts;
- reconsideration status/history.

An Engineering Decision MUST NOT be inferred solely from an Agent message, Participant Input, Execution Result, or Execution Determination.

## 13.11 Verification Result

A Verification Result MUST support:

- identity;
- verification target;
- applicable criteria;
- method/activity reference;
- result;
- status;
- supporting Evidence;
- effect on applicable progression conditions.

## 13.12 Artifact

An Artifact MUST support:

- identity;
- representation/reference;
- status;
- relevant version/history;
- relationships to the engineering work that produced or depends upon it.

---

# 14. Execution Model

## 14.1 Execution Cycle

A conforming Runtime SHALL implement the PEM execution cycle:

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

The operational model represents the information and state changes required by this cycle. It does not turn the cycle into a fixed engineering workflow.

## 14.2 Observe

Observation retrieves or receives relevant information about the Process Instance, engineering state, execution environment, or results.

Observation MUST NOT itself modify authoritative Process Instance state.

Observed information MUST enter authoritative state only through the applicable classification and validation process.

## 14.3 Evaluate

Evaluation determines the current execution condition using authoritative state and applicable EPM/PEM rules.

Evaluation MAY identify:

- satisfied conditions;
- unsatisfied conditions;
- information gaps;
- required investigation;
- required verification;
- required reconsideration;
- permissible transitions;
- prohibited transitions.

## 14.4 Plan

A Plan represents the selection or organization of next execution activities within the current Process State and applicable constraints.

A Plan MAY be transient or persistable depending on implementation and traceability requirements.

A Plan MUST NOT itself establish engineering validity or progression.

## 14.5 Execution Determination

An Execution Determination represents a Runtime-level determination of what execution condition/action is currently permissible, required, blocked, or pending.

It MUST remain distinct from Engineering Decision.

## 14.6 Execution Action

An Execution Action represents an operational activity undertaken as part of PEM execution.

It MUST be associated with:

- Process Instance;
- relevant Execution Context;
- purpose/basis;
- actor/Participant where applicable;
- resulting Execution Result.

An Execution Action is not itself proof of engineering validity.

## 14.7 Execution Result

An Execution Result records what resulted from an Execution Action.

It MAY produce or reference:

- observations;
- Evidence candidates;
- Artifact changes;
- verification results;
- execution errors;
- proposed state changes;
- requests for further work.

The Runtime MUST validate which results can affect authoritative state.

---

# 15. Participant Model

## 15.1 Participant

A Participant represents an entity contributing to execution.

## 15.2 Human Participant and AI Agent

Human Participants and AI Agents are Participants. An AI Agent is not the Runtime.

## 15.3 Participant Input

Participant Input is information supplied by a Participant to the process.

Participant Input MUST remain distinguishable from authoritative engineering knowledge and from an Engineering Decision.

## 15.4 Participant Contribution

A Participant Contribution is a classified contribution made by a Participant during execution.

It MAY include:

- observation;
- analysis;
- Evidence candidate;
- Assumption;
- Candidate Solution;
- Evaluation;
- proposed Engineering Decision;
- Artifact change;
- verification result;
- execution outcome;
- request for clarification.

A contribution becomes part of authoritative engineering or execution state only through applicable validation and execution rules.

## 15.5 Authority

Participant capability and Participant authority MUST remain separate properties.

An Agent having access to a tool does not automatically have authority to perform every engineering action or establish every Decision.

---

# 16. Agent Visibility Boundary

The Agent-facing representation MUST expose sufficient information for the Agent to participate meaningfully in current execution.

At minimum, the Agent MAY require access to:

- Process Instance identity;
- Engineering Objective;
- current Process State;
- Execution Mode;
- relevant Requirements and their resolution state;
- Constraints;
- relevant Investigations;
- relevant Evidence;
- Assumptions;
- Risks;
- Candidate Solutions and Evaluations where applicable;
- accepted/pending Engineering Decisions;
- verification status;
- applicable Decision Gates;
- applicable progression conditions;
- unresolved matters;
- relevant Artifacts;
- execution scope;
- current continuity state.

The exact message format is deferred to the Agent Execution Contract.

The Agent MUST NOT be required to reconstruct authoritative process state solely from conversational history.

---

# 17. Controlled State Mutation

All authoritative state mutation MUST follow this conceptual sequence:

```text
Participant Input / Candidate Contribution / Execution Result
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

This sequence prevents raw Agent output, tool output, or environmental events from silently becoming authoritative engineering state.

A validation failure MUST leave authoritative state unchanged unless the applicable operation explicitly represents a valid failure state.

---

# 18. Controlled Reconsideration

When material new information affects prior engineering conclusions, the operational model MUST support controlled reconsideration.

The minimum sequence is:

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

A revised Decision MUST NOT silently erase the existence or basis of an earlier Decision.

---

# 19. Verification and Failure Handling

Verification results are operationally significant when they affect EPM progression conditions.

A failed verification MUST be representable as a state-affecting result.

Where verification is required for progression, a failed or unresolved verification MUST prevent invalid progression.

The Runtime MUST permit subsequent work required by the EPM, including investigation, Artifact modification, reconsideration, or re-verification where applicable.

---

# 20. Traceability and Execution Trace

## 20.1 Engineering Traceability

Engineering Traceability represents relationships explaining how engineering conclusions are supported and how they relate to Requirements, Evidence, Constraints, Risks, Solutions, Evaluations, Decisions, verification, and Artifacts.

For example:

```text
Requirement
   ↓
Evidence
   ↓
Evaluation
   ↓
Engineering Decision
```

## 20.2 Execution Trace

Execution Trace records material execution evolution, including:

- Process Instance initialization;
- observation/evaluation events where material;
- Plans where material;
- Transition Rule evaluations;
- Transitions;
- Decision Gate evaluations;
- progression-condition evaluations;
- Execution Determinations;
- Execution Actions;
- Execution Results;
- Participant contributions;
- Evidence/Assumption changes;
- Engineering Decisions;
- verification results;
- Artifact changes;
- reconsideration events;
- interruption/resumption;
- objective or mode changes;
- completion/termination.

## 20.3 Current State vs History

Execution Context represents current authoritative operational state.

Engineering Traceability represents current and historical engineering relationships.

Execution Trace represents historical execution evolution.

These concepts MUST NOT be treated as interchangeable.

---

# 21. Persistence and Recovery

## 21.1 Logical Requirement

A conforming implementation MUST persist sufficient Process Instance state and restore it later.

## 21.2 Recovery

After interruption, the Runtime MUST reconstruct authoritative Execution Context without depending on the prior Agent's transient memory.

## 21.3 Equivalence

Successful restoration MUST preserve operationally significant identity, relationships, state, knowledge status, and traceability.

## 21.4 Physical Storage

The model does not prescribe filesystem layout, database technology, serialization library, cloud service, or IDE storage mechanism.

---

# 22. Completion, Suspension, and Termination

The operational model MUST represent separately:

```text
Engineering Process Completion
Runtime Suspension / Interruption
Runtime Termination
```

A Runtime MAY terminate while engineering remains incomplete.

Engineering Process Completion MUST be established according to EPM completion semantics.

Runtime termination MUST NOT automatically imply Engineering Process Completion.

---

# 23. Environment Boundary

The Execution Environment provides capabilities used during execution.

The operational model MUST NOT encode VS Code-specific or tool-specific assumptions.

An environment MAY expose capabilities such as:

```text
read file
write file
search repository
run command
run test
inspect version control
```

These capabilities are environment-level mechanisms, not EPM entities.

An Environment Adapter MUST map available capabilities into the execution interface without changing EPM or PEM validity semantics.

An environment event or tool result MUST enter authoritative state only through controlled mutation.

---

# 24. Runtime Operational Responsibilities

A conforming Runtime is responsible, as applicable, for:

- loading the applicable EPM and PEM;
- establishing Process Instances;
- establishing and maintaining Execution Context;
- coordinating Participants;
- presenting relevant state to Participants;
- evaluating Process State conditions;
- evaluating Transition Rules, Decision Gates, and progression conditions;
- executing valid Transitions;
- managing the execution cycle;
- controlling Execution Actions;
- receiving and classifying Execution Results;
- maintaining authoritative state;
- preserving continuity;
- recording execution trace;
- supporting controlled reconsideration;
- distinguishing engineering completion from Runtime termination.

The Runtime MUST perform these responsibilities without redefining EPM engineering semantics.

---

# 25. Validation Responsibilities

Validation occurs at multiple conceptual levels.

## 25.1 Structural Validation

Determines whether an operational representation satisfies required structure and relationships.

## 25.2 Semantic Validation

Determines whether a proposed engineering-state update is consistent with EPM semantics.

## 25.3 Execution Validation

Determines whether a proposed execution action, Transition, or state mutation is permitted under PEM control.

## 25.4 Persistence Validation

Determines whether stored state can be safely restored as authoritative operational state.

## 25.5 Conformance Validation

Determines whether an implementation satisfies normative EPM, PEM, and Operational Model requirements.

These validation levels MUST remain conceptually distinct even if an implementation combines them.

---

# 26. Operation Classes

The operational model defines operation classes rather than implementation-specific APIs.

### Lifecycle Operations

- initialize Process Instance;
- load Process Instance;
- change Engineering Objective through the controlled objective-change operation;
- change Execution Mode where permitted;
- suspend execution;
- resume execution;
- establish Engineering Process Completion;
- terminate Runtime execution.

### Observation Operations

- inspect current Execution Context;
- inspect applicable Process State;
- inspect relevant engineering knowledge;
- inspect applicable gates and progression conditions;
- observe environment information.

### Evaluation Operations

- evaluate Process State;
- evaluate Transition Rule;
- evaluate Decision Gate;
- evaluate progression condition;
- evaluate verification result;
- evaluate impact of new Evidence;
- evaluate objective or mode changes.

### Investigation Operations

- establish Investigation objective;
- perform investigation activities;
- record resulting Evidence/knowledge;
- evaluate Investigation sufficiency;
- close or continue Investigation according to its objective.

### Contribution Operations

- submit Participant Input;
- submit observation/analysis;
- submit Evidence candidate;
- submit Assumption;
- submit Candidate Solution;
- submit Evaluation;
- propose Engineering Decision;
- submit verification result;
- submit Artifact result.

### Execution Operations

- establish Execution Determination;
- create/update Plan where applicable;
- authorize/perform applicable Execution Action;
- record Execution Result;
- update Execution Context;
- perform valid Transition;
- record trace event.

### Reconsideration Operations

- identify affected conclusions;
- initiate reconsideration;
- revise applicable engineering state;
- record revised Decision;
- preserve historical state.

These operation classes become concrete interfaces only in later artifacts.

---

# 27. Engineering and Operational Invariants

## 27.1 Engineering Invariants

Engineering Invariants are owned by EPM. The Operational Model MUST preserve and enforce them operationally but MUST NOT redefine them.

## 27.2 Operational Invariants

A conforming operational implementation MUST preserve at least:

1. **EPM authority invariant** — engineering validity cannot be redefined by Runtime convenience or Agent output.
2. **PEM execution invariant** — execution follows PEM semantics.
3. **Context authority invariant** — authoritative operational continuation state is represented by Execution Context.
4. **Agent boundary invariant** — Agent is not synonymous with Runtime.
5. **Decision distinction invariant** — Engineering Decision and Execution Determination remain distinct.
6. **Completion distinction invariant** — Engineering Completion and Runtime Termination remain distinct.
7. **Knowledge distinction invariant** — Evidence, Assumptions, unknowns, contested information, and conclusions remain distinguishable.
8. **Observation invariant** — observation does not itself mutate authoritative Process Instance state.
9. **Traceability invariant** — material changes remain reconstructable.
10. **Continuity invariant** — execution can resume without conversational memory.
11. **Environment independence invariant** — execution semantics do not depend on a specific IDE or tool environment.
12. **Controlled mutation invariant** — raw Participant, Agent, tool, or environment output does not silently become authoritative state.
13. **Reconsideration invariant** — revised conclusions preserve prior history.
14. **Condition-driven progression invariant** — activity completion alone does not establish engineering progression.
15. **Objective integrity invariant** — Engineering Objective changes are explicit and traceable.
16. **Requirement-resolution invariant** — Requirement resolution remains distinct from Requirement satisfaction.

---

# 28. Machine-Readable Derivation Requirements

The later machine-readable model MUST faithfully represent this model and MUST provide, where applicable:

- stable entity identities;
- typed relationships;
- explicit lifecycle/status representation;
- Requirement resolution distinct from satisfaction;
- Investigation representation;
- Execution Mode representation;
- Transition Rule and Transition distinction;
- references between current state and historical trace;
- validation constraints;
- unknown/unresolved/contested/invalidated state;
- gate/progression evaluation;
- Agent-visible execution context;
- persistence-compatible serialization;
- model version identification.

Concrete serialization format remains intentionally deferred.

---

# 29. Agent Execution Contract Derivation Requirements

The later Agent Execution Contract MUST be derived from this model.

### AESM → Agent

It MUST be capable of providing, according to visibility and authority rules:

- current Execution Context;
- relevant engineering state;
- applicable Process State;
- Execution Mode;
- applicable execution conditions;
- permitted scope/capabilities;
- required outputs or pending decisions;
- continuity information required for the current execution step.

### Agent → AESM

It MUST support structured contributions including, where applicable:

- Participant Input;
- observations and analysis;
- Evidence candidates and provenance/context;
- explicit Assumptions;
- Investigation results;
- Candidate Solutions;
- Evaluations;
- proposed Engineering Decisions;
- Artifact changes/results;
- verification results;
- execution outcomes;
- requests for information or clarification.

The Agent Contract MUST define how these contributions are distinguished from authoritative state changes.

---

# 30. Implementation Independence

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

A conforming implementation MAY choose any of these while preserving operational semantics.

---

# 31. Repository Boundary

AESM model artifacts and individual engineering execution data are separate concerns.

The AESM repository stores system specifications, operational models, schemas, protocols, and conformance artifacts.

An engineering project's execution environment stores Process Instances, Execution Contexts, traces, and project-specific engineering artifacts according to the Runtime implementation.

```text
AESM Repository
    = system definition

Engineering Project Workspace / State Store
    = execution governed by that system
```

The operational model MUST preserve this distinction.

---

# 32. Phase 2 Revision Scope

This revision explicitly closes the following findings from the Phase 2 consistency review:

- Investigation is now a first-class operational concept.
- Transition Rule is separated from Transition.
- Execution Mode is operationally defined.
- Requirement resolution is explicitly distinguished from satisfaction.
- Engineering Objective change is explicitly controlled and traceable.
- Participant Input is distinguished from Participant Contribution and authoritative state.
- Engineering Invariants are separated conceptually from Operational Invariants.
- Evaluation explicitly includes Requirements and Risks.
- Observation is explicitly non-mutating.
- Planning is operationally represented without becoming a mandatory fixed workflow.
- Runtime responsibilities are explicitly mapped.
- `completed work` and `remaining work` are explicitly defined as continuity information rather than progression criteria.
- Engineering Traceability is explicitly distinguished from Execution Trace.

---

# 33. Open Items for Subsequent Phases

The following remain intentionally unresolved because they belong to later artifacts:

1. exact field-level schema for every entity;
2. canonical machine-readable serialization format;
3. exact Agent request/response structures;
4. concrete protocol transport;
5. Runtime API surface;
6. environment capability interface;
7. conformance test format;
8. physical Process Instance storage layout;
9. exact versioning and migration mechanism for operational state.

These are deliberate implementation-level deferrals, not unresolved semantic gaps in the Operational Model.

---

# 34. Phase 2 Completion Criteria

The AESM Operational Model may be frozen when a final review confirms that:

- all Phase 1 operational requirement classes have corresponding treatment;
- EPM concepts required for execution have not been omitted;
- PEM execution semantics are represented without semantic drift;
- Process Instance and Execution Context are operationally defined;
- Process State, Transition Rule, Transition, Decision Gate, and Progression Condition are distinct and usable;
- Investigation and Execution Mode are operationally represented;
- engineering knowledge entities retain their semantic distinctions;
- Agent/Participant and Runtime boundaries are explicit;
- controlled state mutation is defined;
- observation, planning, execution, verification, and context update have clear operational boundaries;
- engineering traceability and execution trace are both supported;
- persistence, interruption, resumption, reconsideration, objective changes, and termination are represented;
- environment independence is preserved;
- invariants are explicit;
- the model provides sufficient normative detail to derive machine-readable schemas and the Agent Execution Contract without inventing core semantics.

If these criteria are satisfied, the next phase is **Phase 3 — Machine-Readable AESM Model**.
