# AESM Operationalization Analysis

**Project:** AI-Assisted Engineering System Model (AESM)  
**Phase:** Operationalization — Phase 1  
**Status:** Initial Baseline  
**Normative Foundation:** Engineering Process Model (EPM), Concept Freeze v0.1; Process Execution Model (PEM), Concept Freeze v0.1 / Chapters 1–5 Unified

---

## 1. Purpose

This document is the Phase 1 operationalization analysis for the AI-Assisted Engineering System Model (AESM).

Its purpose is to determine what an implementation must be able to represent, evaluate, execute, persist, expose, and validate in order to execute the Engineering Process Model (EPM) according to the Process Execution Model (PEM).

This document does **not** define the final AESM Operational Model, machine-readable schemas, Agent Execution Contract, or Runtime implementation. It identifies the operational requirements that those later artifacts must satisfy.

The analysis preserves the established architectural boundary:

```text
EPM
= engineering meaning and validity

PEM
= execution semantics and control

Runtime
= implementation of PEM

Process Instance
= one execution of an EPM

Execution Context
= authoritative operational state required to continue execution

Agent
= Participant in execution; not the Runtime

Execution Environment
= environment in which the Runtime and/or Agent operate
```

---

## 2. Normative Foundation

The operationalization work is derived from the canonical EPM and PEM. The EPM remains authoritative for engineering semantics and validity. The PEM remains authoritative for execution semantics.

The EPM explicitly defines engineering concepts including Engineering Objective, Requirements, Constraints, Investigation, Evidence, Assumptions, Candidate Solutions, Evaluation, Engineering Decisions, Verification, Artifacts, Risks, Process States, Transition Rules, Progression Conditions, Decision Gates, Execution Modes, Traceability, Knowledge Continuity, Controlled Reconsideration, Process Integrity, Engineering Invariants, and Engineering Process Completion.

The PEM explicitly defines Runtime, Process Instance, Execution Context, Participants, AI Agents, Artifacts, Evidence, Assumptions, Engineering Decisions, Verification, execution lifecycle, execution cycle, execution control, continuity, and Runtime conformance.

The operational layer shall therefore be derived from these semantics rather than becoming an independent source of engineering meaning.

---

## 3. Operationalization Principle

A concept is operationally usable when an implementation can, where applicable:

1. identify it;
2. represent its relevant state;
3. relate it to other process entities;
4. inspect it during execution;
5. create or modify it under applicable rules;
6. validate changes to it;
7. persist it as part of execution continuity;
8. expose the information required to participating Agents or Humans;
9. reconstruct its relevant history and traceability.

Not every concept requires the same representation or operations. The operational model shall preserve the semantic distinction between concepts rather than collapsing them into a generic task or message structure.

---

## 4. Operational Entity Inventory

The following entities and concepts require operational treatment.

### 4.1 Process Identity and Control

- Process Instance
- Engineering Objective
- Process State
- Transition
- Transition Rule
- Decision Gate
- Progression Condition
- Execution Mode
- Execution Determination
- Execution Action
- Execution Result
- Process termination status

### 4.2 Engineering Knowledge

- Requirement
- Constraint
- Evidence
- Assumption
- Risk
- Candidate Solution
- Evaluation
- Engineering Decision
- Verification
- Artifact
- unresolved question / pending matter

### 4.3 Continuity and Traceability

- Execution Context
- Execution Trace
- state history
- Decision history
- Evidence provenance/context
- Artifact relationships
- reconsideration history
- interruption/resumption state

### 4.4 Participation

- Participant
- Human Participant
- AI Agent
- Participant Input
- Participant capability
- applicable Participant authority

These categories are an analysis inventory, not yet the final schema hierarchy.

---

## 5. Process Instance

### Normative basis

The PEM defines a Process Instance as a single execution of an Engineering Process Model for a specific engineering objective. Each Process Instance has its own lifecycle, execution state, Artifacts, Decisions, and Execution Context.

### Operational requirements

An implementation shall be able to:

- create or establish a Process Instance;
- identify the Process Instance uniquely within its execution scope;
- associate it with the applicable EPM and PEM versions or identities;
- associate it with an Engineering Objective;
- establish its initial engineering and execution state;
- maintain its evolving state;
- persist the state independently of transient conversational memory;
- load the Process Instance for later execution;
- distinguish concurrent Process Instances;
- suspend, resume, and terminate execution without confusing Runtime termination with Engineering Process Completion.

### Open design question

The operational model must define the minimum initialization data required to establish a valid Process Instance without inventing unknown Requirements, Evidence, Assumptions, or other engineering facts.

---

## 6. Execution Context

### Normative basis

The PEM defines Execution Context as the authoritative operational state required to continue execution of a Process Instance consistently at a specific point in time. It is logical rather than a storage mechanism and shall be complete, consistent, portable, persistent, and observable.

The PEM identifies logical components including Process Status, Engineering State, Decision State, Knowledge State, and Continuity State.

### Operational requirements

An implementation shall be able to:

- construct an Execution Context;
- identify its associated Process Instance;
- represent the active Process State;
- represent the Engineering Objective;
- represent the execution mode;
- represent relevant Artifacts and their status;
- represent completed and remaining work;
- represent accepted and pending Decisions;
- represent applicable Decision Gates;
- represent Evidence, Assumptions, Risks, and unresolved questions;
- represent interruption point, pending activities, and next expected action;
- validate context consistency;
- persist context;
- reload context without conversational history;
- expose context to an Agent in a controlled form;
- update context only through valid execution operations.

### Critical operational property

Execution Context is authoritative for operational state but cannot override EPM engineering validity. The implementation must therefore prevent an operational state representation from becoming an alternate source of engineering semantics.

---

## 7. Process State and Transition

### Normative basis

The EPM owns Process State semantics and schema. The PEM executes those states. A Transition is valid only when the applicable engineering conditions are satisfied.

### Operational requirements

An implementation shall be able to:

- identify the current Process State;
- load its applicable state definition;
- identify applicable inputs, permitted activities, expected outputs, invariants, entry conditions, progression conditions, completion conditions, exit conditions, Decision Gates, verification requirements, and reconsideration conditions;
- determine applicable Transition Rules;
- evaluate transition conditions using the available Process Instance state;
- identify conditions preventing progression;
- distinguish an invalid transition from an unavailable or incomplete execution action;
- record a state transition and its basis;
- preserve prior state history for traceability.

### Boundary requirement

The Runtime shall execute the EPM-defined state and transition semantics. It shall not create alternative engineering validity conditions merely because those conditions are convenient to implement.

---

## 8. Decision Gates and Progression Conditions

### Normative basis

The EPM defines Decision Gates and progression conditions as engineering validity conditions. The PEM governs how a Runtime evaluates and executes those conditions.

### Operational requirements

An implementation shall be able to:

- identify applicable gates;
- determine the inputs required to evaluate a gate;
- identify required Evidence, verification, Requirements, Constraints, Risks, and Assumptions;
- evaluate whether a gate is satisfied, unresolved, rejected, or otherwise applicable according to the model;
- distinguish insufficient information from a negative determination;
- prevent progression when a required gate is unsatisfied;
- record the evaluation result and relevant basis;
- reevaluate a gate when relevant state changes;
- expose unresolved gates to the Agent.

The same principle applies to progression conditions: the implementation must evaluate applicable engineering conditions rather than infer progression from completion of an arbitrary activity list.

---

## 9. Engineering Knowledge Entities

The EPM distinguishes several forms of engineering knowledge. The operational representation shall preserve those distinctions.

### Requirement

Must support identity, statement/content, resolution state, relevant relationships, status/history, and traceability to Evidence, Constraints, Solutions, Evaluation, Decisions, and verification where applicable.

### Constraint

Must support identification, applicability, relevant scope, status/history, and relationships to affected Solutions, Decisions, and progression conditions.

### Evidence

Must support content or reference, provenance/context where available, relevance, status, and relationships to the conclusions or verification results it supports.

### Assumption

Must support explicit identification, proposition/content, status, affected engineering conclusions, and invalidation/resolution history.

### Candidate Solution

Must support identification, description, applicable Requirements and Constraints, evaluation status, and relationship to Decisions.

### Evaluation

Must support the evaluated subject, criteria/basis, Evidence and Constraints considered, result, and relationship to the resulting Decision or unresolved conclusion.

### Engineering Decision

Must support an accepted conclusion or commitment, its basis, affected Requirements/Constraints/Solutions, supporting Evidence, relevant Risks/Assumptions, status, and reconsideration history.

### Verification

Must support the verification target, applicable criteria, method or activity, result, supporting Evidence, status, and effect on progression.

### Artifact

Must support identity, persistent representation/reference, status, relevant version/history, and traceability to the engineering basis where applicable.

### Risk

Must support identification, description, relevance, status, treatment, affected engineering elements, and change/reconsideration history.

These are semantic requirements; the concrete field names and serialization format belong to the later Operational Model and machine-readable Model.

---

## 10. Engineering Decision vs Execution Determination

This distinction is mandatory in the operational layer.

```text
Engineering Decision
= EPM-level engineering conclusion or commitment

Execution Determination
= PEM/Runtime-level determination of what execution action
  or condition is permissible/appropriate next
```

The operational representation shall prevent these from being conflated.

An Agent may contribute analysis or propose an Engineering Decision, but participant output does not become an Engineering Decision merely because it was produced. The applicable EPM conditions must recognize the Decision.

Likewise, an Execution Determination shall not be represented as an Engineering Decision unless the applicable engineering process explicitly establishes and recognizes one.

---

## 11. Participant and Agent Interaction

### Normative basis

The PEM defines Human Participants and AI Agents as Participants. It explicitly states that an AI Agent is not synonymous with the Runtime and that participation does not automatically confer unrestricted authority.

### Operational requirements

The operational layer shall represent, as needed:

- Participant identity;
- Participant type;
- Participant capability relevant to the action;
- Participant input;
- applicable authority;
- actions or contributions attributed to the Participant;
- resulting Evidence, analysis, artifacts, Decisions, or verification results.

The implementation shall preserve the distinctions:

```text
Participant capability ≠ Participant authority
Participant input ≠ Engineering Decision
AI Agent ≠ Runtime
```

An Agent interface therefore requires a controlled mechanism for providing the Agent with applicable process state and receiving structured contributions without allowing the Agent to silently redefine process semantics.

---

## 12. Execution Cycle

### Normative basis

The PEM defines the continuous execution cycle:

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

### Operational requirements

The Runtime must be able to represent or otherwise make observable the current cycle stage and its relevant input/output.

At minimum, execution must support:

1. observation of current context and relevant environment information;
2. evaluation of execution conditions;
3. production of an Execution Determination or identification of the blocking condition;
4. planning of permissible execution activities;
5. execution of selected activities;
6. verification of results;
7. update of authoritative Execution Context;
8. repetition or valid termination/suspension.

The cycle itself is execution semantics. It must not be mistaken for a rigid engineering workflow.

---

## 13. Execution Actions and Environment Capabilities

The operational layer must distinguish an engineering activity from a tool invocation.

For example:

```text
Engineering activity:
    Investigate the cause of a defect.

Environment capabilities:
    read file
    search code
    inspect logs
    run tests
```

The AESM operational model should define the execution-level abstraction without coupling it to VS Code, a particular Agent framework, programming language, or tool API.

An Environment Adapter may expose capabilities to an Agent, but the existence of a tool does not itself establish that using the tool is an engineering-valid progression.

This distinction is required for portability across execution environments.

---

## 14. Traceability and Execution Trace

The EPM requires material engineering traceability. The PEM requires execution continuity and authoritative context.

Therefore an implementation must preserve an execution trace sufficient to reconstruct, as applicable:

- Process State changes;
- Execution Determinations;
- execution actions;
- Participant contributions;
- Evidence introduced or invalidated;
- Assumptions introduced, resolved, or invalidated;
- Engineering Decisions;
- verification results;
- Artifact changes;
- progression determinations;
- reconsideration events;
- interruptions and resumptions.

The operational layer must distinguish the **current authoritative state** from the **historical trace**. Execution Context represents current operational state; the trace preserves how that state evolved.

---

## 15. Controlled Reconsideration

### Normative basis

The EPM requires controlled reconsideration when material new information invalidates or materially changes assumptions, requirements, risks, Decisions, Solutions, or other engineering conclusions.

### Operational requirements

An implementation shall be able to:

1. register the new or changed Evidence;
2. identify affected Assumptions, Requirements, Risks, Solutions, Decisions, or verification results;
3. identify affected prior conclusions;
4. mark affected conclusions as requiring reconsideration or otherwise represent their changed validity;
5. preserve the prior Decision/history;
6. return execution to the applicable earlier engineering work;
7. produce the new evaluation/Decision;
8. preserve traceability from the previous conclusion to the revised conclusion.

The old Decision must remain reconstructable; reconsideration is not silent replacement.

---

## 16. Verification Failure

A conforming implementation must be able to represent verification failure as an execution-relevant condition.

Where a failed verification condition is required for progression, the Runtime shall prevent invalid progression.

The implementation must support subsequent engineering work such as:

- additional investigation;
- revision of an Artifact;
- reconsideration of a Decision;
- additional verification.

Verification failure must not be represented merely as an informational message if it has a normative effect on progression.

---

## 17. Interruption and Resumption

The PEM requires Knowledge Continuity and explicitly makes Execution Context independent of transient conversational history.

Therefore an implementation must support:

```text
Execution
   ↓
Interruption
   ↓
Persist authoritative state
   ↓
Runtime/session replacement
   ↓
Load Process Instance + Execution Context
   ↓
Resume consistently
```

The operational model must define the minimum persisted state required to resume without relying on the previous Agent's context window.

This requirement is central to AESM and is not an optional convenience feature.

---

## 18. Completion vs Runtime Termination

The EPM owns Engineering Process Completion semantics.

The PEM governs Runtime termination mechanics.

The operational layer shall therefore represent these separately.

At minimum it must be possible to represent:

```text
Engineering incomplete
+
Runtime terminated/suspended
```

and:

```text
Engineering complete
+
Runtime eligible for termination
```

A Runtime stopping execution must not automatically imply that engineering work is complete.

---

## 19. Persistence and Portability

Execution Context is defined as persistent and portable, while its physical storage is implementation-dependent.

The operational layer therefore needs a logical persistence contract without prescribing a database, file format, or platform.

An implementation must be able to:

- serialize the authoritative operational state into its chosen persistence mechanism;
- restore equivalent operational state;
- preserve identity and relationships;
- detect or reject materially inconsistent state;
- transfer state between compatible Runtime implementations where the conformance model permits it.

The later machine-readable model should provide a representation capable of supporting this portability requirement.

---

## 20. Unknown Information and Epistemic Integrity

The specifications distinguish Evidence, Assumptions, unresolved matters, and supported conclusions. Operationalization must preserve this distinction.

An implementation shall not silently convert missing information into asserted fact merely to make execution easier.

At initialization and throughout execution, the operational state must be capable of representing:

```text
Known / supported
Unknown
Assumed
Contested
Unresolved
Invalidated
```

The exact vocabulary must be derived and normalized during the Operational Model phase.

---

## 21. Operational Requirements for an Agent Interface

The operationalization analysis establishes that an AESM-capable Agent must eventually be able to consume, at minimum, the information needed to understand:

- the Process Instance identity;
- Engineering Objective;
- current Process State;
- relevant Requirements and resolution states;
- applicable Constraints;
- relevant Evidence;
- Assumptions;
- Risks;
- Candidate Solutions and evaluations where relevant;
- accepted and pending Engineering Decisions;
- verification status;
- applicable Decision Gates;
- applicable progression conditions;
- unresolved matters;
- relevant Artifacts;
- execution scope and current execution condition;
- information necessary to continue from the current Execution Context.

The Agent must eventually be able to return structured contributions that can be evaluated and incorporated into the Process Instance, including, where applicable:

- observations;
- analysis;
- Evidence;
- Assumptions;
- Candidate Solutions;
- evaluations;
- proposed Engineering Decisions;
- Artifact changes;
- verification results;
- execution results;
- requests for additional information or clarification.

This section establishes requirements for the later Agent Execution Contract; it does not yet define that contract.

---

## 22. Operational Gaps Identified

The current EPM and PEM provide strong semantic and execution definitions, but the following operational details are not yet specified at the level required for implementation.

### G1 — Canonical operational entity model

The specifications define concepts but do not yet provide a single machine-operable entity model with explicit identities, relationships, lifecycle/status semantics, and update boundaries.

**Required next artifact:** AESM Operational Model.

### G2 — Execution Context schema

The PEM defines the logical composition and properties of Execution Context but explicitly leaves physical representation implementation-dependent. A normative logical schema is still required for interoperability.

**Required next artifact:** Operational Model + machine-readable schema.

### G3 — Process Instance initialization contract

The specifications define what a Process Instance is but do not yet define the exact operational initialization procedure and minimum data required to establish one without inventing information.

**Required next artifact:** Operational Model; later Agent Execution Contract.

### G4 — Execution operation model

The PEM defines the execution cycle and control semantics, but the operational interface for expressing execution actions, results, determinations, state updates, and validation outcomes has not yet been formalized.

**Required next artifact:** Operational Model + Agent Execution Contract.

### G5 — Agent interaction contract

The PEM identifies AI Agents as Participants but does not yet define a machine-operable protocol for presenting execution context to an Agent and accepting structured Agent contributions.

**Required next artifact:** Agent Execution Contract + machine-readable protocol.

### G6 — Tool/environment boundary

The specifications are intentionally environment-independent. They therefore do not yet define how an execution environment exposes capabilities while preserving AESM's distinction between engineering activity and environment/tool invocation.

**Required next artifact:** Operational Model; later environment/Agent adapter contract.

### G7 — Execution trace schema

Traceability semantics are defined, but a complete operational representation of execution history has not yet been standardized.

**Required next artifact:** Operational Model + machine-readable trace schema.

### G8 — Persistence/interchange contract

Execution Context is required to be persistent and portable, but the interoperable logical representation and validation rules for persistence/transfer remain unspecified.

**Required next artifact:** Operational Model + machine-readable schemas.

### G9 — Reconsideration operation

Controlled reconsideration is semantically defined, but its executable sequence, affected-object identification, state update behavior, and historical preservation requirements need operational formalization.

**Required next artifact:** Operational Model + Agent Execution Contract.

### G10 — Conformance criteria at the implementation boundary

PEM conformance is defined at a normative level, but a testable operational conformance model has not yet been produced.

**Required next artifact:** Conformance Model.

### G11 — Runtime/Agent responsibility boundary

The conceptual distinction between Runtime and Agent is established, but the operational boundary—what the Runtime controls versus what the Agent proposes or performs—needs explicit interface semantics.

**Required next artifact:** Agent Execution Contract + Conformance Model.

### G12 — Completion/termination representation

The semantic distinction is established, but an interoperable operational representation of Engineering Process Completion versus Runtime suspension/termination remains to be defined.

**Required next artifact:** Operational Model.

---

## 23. Derived Operational Requirement Classes

The gaps above can be grouped into seven implementation-facing requirement classes.

### OR-1 — State Representation

The implementation must represent authoritative Process Instance and Execution Context state.

### OR-2 — State Evaluation

The implementation must evaluate applicable engineering and execution conditions without redefining them.

### OR-3 — Controlled Mutation

The implementation must provide controlled operations for incorporating valid execution results into authoritative state.

### OR-4 — Participant Interaction

The implementation must expose relevant context to Participants and incorporate Participant contributions according to applicable authority and validation rules.

### OR-5 — Continuity

The implementation must persist and restore sufficient state for interruption and resumption without conversational memory.

### OR-6 — Traceability

The implementation must preserve sufficient relationships and history to reconstruct material engineering reasoning and execution evolution.

### OR-7 — Conformance

The implementation must be testable against the semantic and execution requirements of EPM and PEM.

---

## 24. Required Transformation to the Next Phase

The next phase shall transform this analysis into a normative **AESM Operational Model**.

The transformation should proceed in the following order:

```text
Operational Requirement
        ↓
Operational Concept / Entity
        ↓
Properties and Relationships
        ↓
Lifecycle / State Semantics
        ↓
Permitted Operations
        ↓
Validation Rules
        ↓
Persistence Requirements
        ↓
Agent Visibility / Interaction
```

Only after this transformation should concrete JSON/YAML schemas, protocol messages, APIs, or Runtime code be designed.

---

## 25. Constraints on Subsequent Design

The following constraints are established for all later operational artifacts:

1. EPM remains authoritative for engineering meaning and validity.
2. PEM remains authoritative for execution semantics.
3. Runtime implementation details shall not be promoted into EPM semantics.
4. Machine-readable representations shall be derived from normative specifications.
5. Agent behavior shall not become an implicit source of engineering authority.
6. Execution Context shall remain authoritative for operational state but shall not override EPM validity.
7. Process State semantics shall remain owned by EPM.
8. Engineering Decision shall remain distinct from Execution Determination.
9. Runtime termination shall remain distinct from Engineering Process Completion.
10. Tool invocations shall remain distinct from engineering activities.
11. Unknown information shall remain distinguishable from Evidence and accepted conclusions.
12. Operational representations shall support interruption and resumption without conversational memory.
13. Repository artifacts describing AESM shall remain distinct from Process Instance data belonging to an individual engineering project.

---

## 26. Phase 1 Completion Criteria

Phase 1 is considered complete when:

- the operationally significant EPM and PEM concepts have been inventoried;
- each concept has been analyzed for representation, operation, persistence, validation, and interaction needs where applicable;
- the Process Instance and Execution Context requirements are explicit;
- the Agent-facing requirements are explicit;
- the Runtime/Agent/Environment boundary is explicit;
- operational gaps are identified and classified;
- the requirements for the next Operational Model phase are traceable to this analysis;
- no unresolved operational gap is silently treated as an implementation detail when it may affect EPM/PEM semantics.

This document satisfies the initial Phase 1 artifact requirement. The next phase is the formal construction of the **AESM Operational Model** from these derived requirements.
