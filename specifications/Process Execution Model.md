# Process Execution Model

**Conceptual Version:** Concept Freeze v0.1  
**Specification Status:** Chapters 1–5 — Unified  
**Document Status:** Consolidated Specification

---

# Chapter 1 — Introduction

## 1.1 Purpose

The **Process Execution Model (PEM)** defines the execution semantics of the Engineering Process Model.

Where the Engineering Process Model defines **what engineering activities constitute a valid engineering process**, the Process Execution Model defines **how those activities are executed consistently by participating actors**.

The Process Execution Model exists to ensure that a single Engineering Process Model can be executed predictably across different execution environments, Runtime implementations, and combinations of Human Participants and AI Agents.

This specification intentionally separates execution semantics from process definition.

The Engineering Process Model remains the authoritative description of engineering work, while the Process Execution Model defines the rules governing its execution.

---

## 1.2 Scope

This specification defines:

- how an engineering Process Instance is executed;
- how execution state is established and maintained;
- how Participants collaborate during execution;
- how Process States are entered, executed, verified, and exited;
- how Artifacts are produced and evolved during execution;
- how execution continuity is maintained across interruptions;
- the requirements that Runtime implementations must satisfy.

This specification does not define:

- the engineering process itself;
- individual Process State definitions;
- engineering Artifact definitions;
- governance structures;
- organizational policies;
- implementation technologies;
- user-interface design.

Those concerns are defined elsewhere.

---

## 1.3 Objectives

The Process Execution Model has the following objectives.

### Consistency

Equivalent engineering tasks should follow equivalent execution behavior regardless of the Runtime implementation.

### Predictability

Participants should understand how execution progresses, why decisions are made, and what conditions govern execution and state transitions.

### Portability

Execution semantics shall remain independent of any particular AI model, software platform, programming language, or Execution Environment.

### Human–AI Collaboration

Execution shall support collaboration between Humans and AI Agents without making either participant type inherently authoritative merely because of its implementation.

Responsibilities and authority are determined by the applicable process and execution conditions.

### Knowledge Continuity

Execution shall preserve sufficient information to allow work to continue after interruptions, context switches, or Runtime replacement.

### Evidence-Based Execution

Execution shall favor observable evidence over unsupported assumptions.

Where material uncertainty exists, execution should seek sufficient additional evidence before progressing.

---

## 1.4 Relationship to the Engineering Process Model

The Engineering Process Model and the Process Execution Model define different aspects of the same system.

The Engineering Process Model specifies engineering-level concepts including:

- engineering principles;
- Process States;
- transition rules;
- Decision Gates;
- execution modes;
- Artifact definitions;
- cross-cutting engineering disciplines.

The Process Execution Model specifies:

- execution behavior;
- Participant interaction;
- execution lifecycle;
- state execution;
- Execution Context management;
- execution continuity;
- execution control;
- Runtime conformance.

Neither model replaces the other.

The Engineering Process Model defines the structure and semantics of engineering work.

The Process Execution Model defines how that structure is executed.

---

## 1.5 Intended Audience

This specification is intended for:

- Runtime implementers;
- AI Agent developers;
- engineering teams adopting the Engineering Process Model;
- tool builders;
- researchers studying AI-assisted engineering processes.

---

## 1.6 Conformance

A Runtime implementation claiming conformance to this specification shall execute an Engineering Process Model according to the execution semantics defined herein.

Conformance does not require a specific implementation technology.

A conforming implementation may be:

- a conversational AI system;
- an integrated development environment;
- a command-line application;
- a workflow orchestration platform;
- a collaborative web application;
- or any other system capable of implementing the Process Execution Model.

---

# Chapter 2 — Core Concepts

## 2.1 Purpose

This chapter defines the fundamental concepts of the Process Execution Model.

These concepts establish the conceptual model upon which the execution semantics are defined.

All subsequent chapters use the terminology and relationships established herein.

The concepts are implementation-independent and represent logical entities rather than specific software components.

---

## 2.2 Conceptual Architecture

The Process Execution Model consists of the following primary concepts:

```text
Engineering Process Model
        │
        │ defines
        ▼
Process Execution Model
        │
        │ implemented by
        ▼
Runtime
        │
        │ executes
        ▼
Process Instance
        │
        │ maintains
        ▼
Execution Context
```

Participants interact with execution through the Runtime:

```text
Human Participant ──┐
                    │
AI Agent ───────────┤
                    ▼
                  Runtime
                    │
                    ▼
              Process Instance
```

These concepts are independent but closely related.

The Engineering Process Model defines engineering behavior.

The Process Execution Model defines execution semantics.

Runtime implementations realize those semantics.

Process Instances represent individual executions.

Execution Context preserves the operational state of each execution.

Participants contribute to execution.

---

## 2.3 Engineering Process Model

### Definition

The **Engineering Process Model (EPM)** is the authoritative definition of the engineering process.

It specifies concepts such as:

- engineering principles;
- Process States;
- transition rules;
- Decision Gates;
- execution modes;
- Artifact definitions;
- cross-cutting engineering disciplines.

The Engineering Process Model defines **what engineering work shall occur**.

It does not define how execution is performed.

The Engineering Process Model is not redefined by the Runtime during execution.

---

## 2.4 Process Execution Model

### Definition

The **Process Execution Model (PEM)** defines the execution semantics required to perform an Engineering Process Model.

It specifies:

- execution behavior;
- Participant coordination;
- execution lifecycle;
- state execution;
- Execution Context management;
- execution continuity;
- execution control;
- Runtime conformance.

The Process Execution Model defines **how engineering work is executed**.

It does not redefine the Engineering Process Model.

---

## 2.5 Runtime

### Definition

A **Runtime** is an implementation of the Process Execution Model.

Its purpose is to execute one or more Process Instances in accordance with both the Engineering Process Model and the Process Execution Model.

A Runtime is an implementation concept rather than an independent source of engineering authority.

The Runtime shall conform to the Engineering Process Model and the Process Execution Model.

It shall not silently modify either specification.

### Responsibilities

A Runtime is responsible for:

- loading or otherwise making applicable the Engineering Process Model;
- establishing Process Instances;
- maintaining Execution Context;
- coordinating Participants;
- executing Process States;
- evaluating applicable transition conditions;
- producing and updating execution Artifacts;
- preserving execution continuity;
- controlling execution according to the PEM.

The Runtime is not responsible for independently defining engineering behavior.

---

## 2.6 Process Instance

### Definition

A **Process Instance** is a single execution of an Engineering Process Model for a specific engineering objective.

Each engineering effort represented by the execution model is represented by a Process Instance.

Examples include:

- implementing a feature;
- investigating a defect;
- performing an architectural evaluation;
- planning a release.

Each Process Instance possesses its own lifecycle, execution state, Artifacts, Decisions, and Execution Context.

Multiple Process Instances may execute concurrently.

---

## 2.7 Process State

### Definition

A **Process State** represents the current stage of engineering work within a Process Instance.

A Process State defines, through the Engineering Process Model:

- its objective;
- permitted activities;
- expected outputs;
- completion conditions.

The Engineering Process Model defines Process States.

The Process Execution Model governs how those states are executed.

---

## 2.8 Execution Context

### Definition

The **Execution Context** is the authoritative operational state required to continue execution of a Process Instance consistently at a specific point in time.

It represents the minimum authoritative information required for a conforming Runtime to resume execution without altering engineering intent or execution semantics.

Execution Context is a logical model rather than a storage mechanism.

### Characteristics

Execution Context shall be:

- complete;
- consistent;
- portable;
- persistent;
- observable.

Execution Context shall not depend upon conversational history or transient Runtime memory.

### Composition

Execution Context logically contains:

#### Process Status

- Process Instance identity;
- active Process State;
- execution objective;
- execution mode.

#### Engineering State

- Artifacts;
- Artifact status;
- completed work;
- remaining work.

#### Decision State

- accepted Decisions;
- pending Decisions;
- Decision Gates.

#### Knowledge State

- Evidence;
- Assumptions;
- risks;
- unresolved questions.

#### Continuity State

- interruption point;
- pending activities;
- next expected action.

The physical representation of Execution Context is implementation-dependent.

---

## 2.9 Participant

### Definition

A **Participant** is an entity that contributes to the execution of a Process Instance.

A Participant may contribute:

- information;
- Evidence;
- clarification;
- engineering work;
- analysis;
- judgment;
- Decisions;
- authorization;
- verification;
- challenges to existing conclusions.

Participation may occur at different points during execution and may vary according to the requirements of the Process Instance.

A Participant does not automatically possess unrestricted authority over the Process Instance merely by participating in it.

---

## 2.10 Participant Types

The Process Execution Model recognizes two primary forms of Participant:

- Human Participant;
- AI Agent.

These represent different forms of participation in engineering execution.

The PEM does not require Human Participants and AI Agents to have identical capabilities or authority.

Their participation is governed by the applicable process rules and execution conditions.

An AI Agent is not synonymous with the Runtime.

```text
Human Participant ──┐
                    │
AI Agent ───────────┤
                    ▼
                  Runtime
                    │
                    ▼
              Process Instance
```

The Runtime remains the mechanism responsible for executing the Process Execution Model.

---

## 2.11 Artifacts

### Definition

An **Artifact** is a persistent representation of engineering knowledge produced or consumed during execution.

Artifacts exist independently of Runtime implementations.

Artifacts are governed by the Engineering Process Model and manipulated through execution defined by the Process Execution Model.

---

## 2.12 Evidence

### Definition

**Evidence** is information used to support or justify engineering Decisions and conclusions.

Evidence may originate from documentation, code, experiments, measurements, stakeholders, or operational systems.

Evidence shall be distinguishable from Assumptions.

---

## 2.13 Assumptions

### Definition

An **Assumption** is a temporary proposition accepted without sufficient Evidence.

Assumptions shall be explicitly identifiable.

Execution should seek to replace Assumptions with Evidence whenever practical.

---

## 2.14 Decisions

### Definition

A **Decision** is an accepted engineering conclusion or commitment that affects Process Execution.

Decisions may determine:

- selected Solutions;
- accepted trade-offs;
- approved progression;
- process direction;
- resolution of material uncertainty.

Decisions shall remain distinguishable from proposals or unaccepted alternatives.

---

## 2.15 Verification

### Definition

**Verification** is the activity of evaluating whether an engineering result, Artifact, Decision, or Process State satisfies applicable requirements and conditions.

Verification provides Evidence for determining whether execution may progress.

Verification may identify deficiencies requiring additional execution.

---

## 2.16 Concept Relationships

The principal relationships are:

```text
Engineering Process Model
    ├── defines Process States
    ├── defines Artifacts
    ├── defines Decision Gates
    └── defines Engineering Rules
                │
                ▼
Process Execution Model
    ├── defines Execution Semantics
    ├── defines Runtime Behavior
    ├── defines State Execution
    └── defines Knowledge Continuity
                │
                ▼
Runtime
    ├── executes Process Instances
    ├── coordinates Participants
    ├── maintains Execution Context
    └── produces and updates Artifacts
                │
                ▼
Process Instance
    ├── has Process State
    ├── has Execution Context
    ├── contains Decisions
    ├── contains Evidence
    └── evolves over time
```

---

# Chapter 3 — Execution Cycle

## 3.1 Purpose

This chapter defines the normative execution behavior of the Process Execution Model.

Execution is modeled as a continuous cycle rather than a fixed sequence of engineering activities.

A Runtime shall repeatedly evaluate the current Process Instance, determine an appropriate action, perform that action, update the Execution Context, and repeat until the Process Instance reaches completion, is intentionally suspended, or is otherwise terminated according to applicable process conditions.

---

## 3.2 Principle

Execution is continuous.

Execution progresses through repeated evaluation rather than predetermined sequences.

The Runtime continuously responds to:

- newly available Evidence;
- Participant interaction;
- Artifact evolution;
- state completion;
- interruption;
- external change.

Execution therefore behaves as an adaptive control process.

---

## 3.3 Execution Cycle

Every Process Instance shall progress through the following conceptual cycle:

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

This cycle continues until the Process Instance reaches an applicable termination condition.

---

## 3.3.1 Observe

The Runtime observes the current execution situation.

Observation includes examination of:

- Execution Context;
- current Process State;
- Artifacts;
- Participant Input;
- newly available Evidence;
- relevant changes in the Execution Environment.

Observation shall not itself modify the Process Instance.

Its purpose is situational awareness.

---

## 3.3.2 Evaluate

The Runtime evaluates the observed information.

Evaluation determines, as applicable:

- whether execution may continue;
- whether additional information is required;
- whether verification has failed;
- whether Assumptions require resolution;
- whether transition conditions have been satisfied;
- whether a Decision Gate must be addressed;
- whether Participant Input materially affects execution.

Evaluation produces an execution decision or identifies the condition preventing reliable progression.

---

## 3.3.3 Plan

The Runtime determines the next execution activities.

Planning may select:

- engineering activities;
- Participant interaction;
- verification activities;
- Artifact updates;
- investigation;
- clarification;
- other permissible execution actions.

Planning shall remain within the boundaries of the current Process State and applicable execution constraints.

Planning shall not redefine the Engineering Process Model.

---

## 3.3.4 Execute

Execution performs the selected engineering activities.

Execution may involve:

- investigation;
- analysis;
- Artifact production;
- Artifact modification;
- stakeholder interaction;
- reasoning;
- experimentation;
- verification activities.

Execution modifies the Process Instance.

---

## 3.3.5 Verify

Verification evaluates execution outputs.

Verification determines, as applicable:

- correctness;
- completeness;
- consistency;
- readiness for progression;
- whether Assumptions remain acceptable;
- whether applicable Decision Gate conditions have been satisfied.

Verification occurs continuously.

Failure to verify may require additional investigation, revision, or return to earlier execution activities.

---

## 3.3.6 Update Context

Execution results are incorporated into the Execution Context.

Updates may include:

- Artifact changes;
- Decision records;
- Evidence;
- Assumptions;
- risks;
- Process State progression;
- pending work;
- unresolved questions;
- next expected action.

Execution Context becomes the new authoritative operational state.

---

## 3.3.7 Repeat

The Runtime begins the cycle again using the updated Execution Context.

---

## 3.4 State Independence

The Execution Cycle is independent of individual Process States.

The same cycle applies whether the Process Instance is in:

- Investigation;
- Requirements;
- Design;
- Verification;
- or another state defined by the Engineering Process Model.

Process States define **what work is permissible**.

The Execution Cycle defines **how execution progresses**.

---

## 3.5 Interruptions

Execution may be interrupted at any point.

An interruption does not necessarily terminate the Process Instance.

Before suspension or loss of active execution, the Runtime shall preserve sufficient Execution Context to permit consistent resumption.

Resumption begins with the **Observe** phase.

---

## 3.6 Completion

Execution terminates when the applicable Engineering Process Model conditions indicate completion or when execution is explicitly terminated or abandoned according to applicable process conditions.

Termination shall preserve the final Execution Context and required Artifacts.

---

# Chapter 4 — Execution Control

## 4.1 Purpose

This chapter defines how a Runtime determines and controls the execution of a Process Instance.

Execution Control establishes the rules by which the Runtime:

- determines what may happen next;
- selects an appropriate execution action;
- respects the Engineering Process Model and current Process State;
- uses the Execution Context as the authoritative operational state;
- responds to Decision Gates;
- incorporates Participant Input;
- handles insufficient information;
- prevents execution from proceeding on unsupported Assumptions.

Execution Control does not define the Engineering Process Model itself.

The Engineering Process Model remains the source of engineering process semantics.

The Process Execution Model defines how those semantics are applied during execution.

---

## 4.2 Execution Control Principle

A Runtime does not independently determine what constitutes valid engineering work.

Its execution decisions are constrained by the models and state governing the Process Instance.

The Runtime must therefore determine its next action according to the following authority sequence:

```text
Engineering Process Model
        ↓
Current Process State
        ↓
Execution Context
        ↓
Decision Gates
        ↓
Participant Input
        ↓
Runtime Heuristics
```

Each level constrains the levels below it.

Runtime heuristics may assist execution, but they must not override requirements established by the Engineering Process Model, current Process State, Execution Context, applicable Decision Gates, or valid Participant Input.

---

## 4.3 Engineering Process Model as the Highest Execution Constraint

The Engineering Process Model defines the engineering process that the Runtime is executing.

The Runtime must therefore execute according to the applicable process definition.

The Runtime must not:

- redefine the process;
- silently alter process rules;
- bypass required process conditions;
- replace process-defined requirements with implementation preferences;
- treat its own heuristics as authoritative process rules.

If the Runtime encounters a situation that cannot be resolved within the applicable process definition, it must not silently invent a new process rule.

The situation must instead be surfaced for appropriate resolution.

---

## 4.4 Current Process State

The Runtime must consider the current Process State when determining the next execution action.

The current Process State establishes the immediate process context within which execution occurs.

The Runtime must ensure that actions are appropriate to the current state and consistent with its applicable conditions and constraints.

The Runtime must not treat the Process Instance as an unconstrained collection of activities.

Execution remains governed by the current Process State.

---

## 4.5 Execution Context as Operational Authority

The Runtime must use the Execution Context when determining the current execution situation.

The Execution Context provides the authoritative operational state required to continue execution of the Process Instance consistently.

Relevant information includes:

- Process Instance identity;
- current Process State;
- execution objective;
- execution mode;
- completed work;
- remaining work;
- Artifacts and their status;
- accepted Decisions;
- pending Decisions;
- Decision Gates;
- Evidence;
- Assumptions;
- risks;
- unresolved questions;
- interruption information;
- pending activities;
- next expected action.

Where conflicting information exists, the Runtime must identify and resolve the inconsistency rather than silently choosing a value.

---

## 4.6 Decision Gates

Decision Gates constrain progression through the engineering process.

A Decision Gate represents a point at which execution must establish whether the conditions for a relevant Decision or progression have been satisfied.

The Runtime must recognize applicable Decision Gates when determining whether execution may continue or transition.

The Runtime must not bypass an applicable Decision Gate merely because it considers the expected outcome obvious.

Where a gate cannot be evaluated reliably, the Runtime must not fabricate a result.

It must instead take an appropriate controlled action, such as:

- request missing information;
- recommend investigation;
- identify an unresolved condition;
- record an explicit Assumption where permitted;
- suspend execution.

The detailed semantics of individual Decision Gates are defined by the Engineering Process Model and applicable execution rules.

---

## 4.7 Participant Input

Participant Input may affect execution when it provides information, Decisions, clarification, or another contribution relevant to the Process Instance.

Participant Input must be evaluated in the context of:

- the Engineering Process Model;
- the current Process State;
- the Execution Context;
- applicable Decision Gates.

Participant Input does not automatically override higher-level execution constraints.

The detailed interaction between Human Participants, AI Agents, and the Runtime is defined in Chapter 5.

---

## 4.8 Runtime Heuristics

A Runtime may use heuristics to determine how best to proceed when multiple permissible actions are available.

Examples include choosing whether to:

- investigate further;
- request clarification;
- perform verification;
- update an Artifact;
- continue an existing activity;
- address an unresolved Assumption.

Runtime heuristics are subordinate to the execution constraints established above.

They must not be used to:

- override process rules;
- bypass Decision Gates;
- alter authoritative Execution Context without justification;
- fabricate missing information;
- silently resolve unresolved engineering Decisions.

Heuristics determine **how to execute within permitted boundaries**, not **what those boundaries are**.

---

## 4.9 Runtime Actions

Subject to applicable constraints, a Runtime may perform or initiate actions including:

- continue the current activity;
- request information;
- request clarification;
- recommend investigation;
- produce an Artifact;
- update an Artifact;
- perform verification;
- resolve an Assumption where sufficient Evidence exists;
- record a Decision;
- initiate a process transition;
- suspend execution;
- resume execution;
- terminate execution.

The availability and conditions of these actions are determined by the applicable Engineering Process Model and Process Execution Model semantics.

---

## 4.10 Insufficient Information

A Runtime must recognize when available information is insufficient to proceed reliably.

Insufficient information may occur when:

- required information is missing;
- Evidence is inadequate;
- an Assumption has become invalid;
- conflicting information exists;
- a Decision Gate cannot be evaluated;
- the Execution Context is incomplete or inconsistent;
- the next permissible action cannot be determined reliably.

When execution cannot proceed reliably, the Runtime must not fabricate information merely to maintain forward progress.

Instead, it may:

1. request clarification;
2. request additional information;
3. recommend or initiate appropriate investigation;
4. record an explicit Assumption where the process permits this;
5. suspend execution.

---

## 4.11 Controlled Progression

Execution progress must be based on sufficient Evidence and valid process conditions rather than on the desire to maintain forward movement.

An action may be technically possible while still being inappropriate because required conditions have not been established.

The Runtime must favor process correctness and execution integrity over artificial progression.

---

## 4.12 Execution Control and the Execution Cycle

Execution Control operates within the execution cycle defined in Chapter 3:

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

Execution Control determines how the Runtime moves through this cycle.

Conceptually:

```text
Observe
   ↓
Evaluate current state and context
   ↓
Determine applicable constraints
   ↓
Evaluate Decision Gates
   ↓
Consider Participant Input
   ↓
Select permissible action
   ↓
Execute
   ↓
Verify result
   ↓
Update Execution Context
   ↓
Repeat
```

---

## 4.13 Context Update

Execution Control is not complete when an action has been performed.

The Runtime must update the Execution Context when execution changes the operational state of the Process Instance.

Relevant changes may include:

- completed work;
- newly produced or modified Artifacts;
- new Evidence;
- changed Assumptions;
- newly identified risks;
- Decisions;
- changed Decision Gate status;
- changed Process State;
- newly identified unresolved questions;
- changed pending activities;
- changed next expected action.

The resulting Execution Context must remain sufficiently consistent to support continued execution.

---

## 4.14 Suspension

The Runtime may suspend execution when continued execution cannot proceed reliably or appropriately.

Suspension may be appropriate when:

- required information is unavailable;
- a required Decision cannot be obtained;
- a Decision Gate cannot be satisfied;
- conflicting information cannot yet be resolved;
- the Execution Context is insufficient or inconsistent;
- continued execution would require unsupported Assumptions.

Suspension is a controlled execution outcome.

It is not equivalent to failure.

A suspended Process Instance retains its Execution Context so that execution may be resumed when the blocking condition has been resolved.

---

## 4.15 Termination

The Runtime may terminate execution when termination is permitted by the applicable process conditions.

Termination must not be used merely as a substitute for handling uncertainty.

Where continued execution is possible but temporarily blocked, suspension is distinct from termination.

---

## 4.16 Execution Control Invariants

### Invariant 1 — Process Integrity

The Runtime must execute the Engineering Process Model rather than silently redefine it.

### Invariant 2 — Context Integrity

The Runtime must preserve the consistency and authority of the Execution Context.

### Invariant 3 — Gate Integrity

The Runtime must not bypass applicable Decision Gates.

### Invariant 4 — Evidence Integrity

The Runtime must not represent unsupported information as established knowledge.

### Invariant 5 — Uncertainty Integrity

The Runtime must not conceal material uncertainty merely to continue execution.

### Invariant 6 — Heuristic Subordination

Runtime heuristics must remain subordinate to higher-level execution constraints.

### Invariant 7 — Controlled Progression

Execution must progress only when the conditions for progression have been sufficiently established.

### Invariant 8 — Context Continuity

Changes to execution must be reflected in the Execution Context sufficiently for subsequent execution to remain consistent.

---

## 4.17 Execution Control Decision Model

The Runtime's control decision can be represented conceptually as:

```text
                  Observe
                     ↓
        ┌────────────────────────┐
        │ Engineering Process    │
        │ Model constraints      │
        └────────────┬───────────┘
                     ↓
        ┌────────────────────────┐
        │ Current Process State  │
        └────────────┬───────────┘
                     ↓
        ┌────────────────────────┐
        │ Execution Context      │
        └────────────┬───────────┘
                     ↓
        ┌────────────────────────┐
        │ Applicable Decision    │
        │ Gates                  │
        └────────────┬───────────┘
                     ↓
        ┌────────────────────────┐
        │ Participant Input      │
        └────────────┬───────────┘
                     ↓
        ┌────────────────────────┐
        │ Runtime Heuristics     │
        └────────────┬───────────┘
                     ↓
             Permissible Action
                     ↓
                  Execute
                     ↓
                  Verify
                     ↓
             Update Context
                     ↓
                   Repeat
```

If no reliable permissible action can be determined, the Runtime must not fabricate one.

It must instead enter an appropriate controlled condition, such as requesting information, recommending investigation, recording an explicit permitted Assumption, or suspending execution.

---

## 4.18 Scope Boundary

This chapter defines execution control, not all execution semantics.

The following remain outside the scope of this chapter:

- detailed Participant Interaction;
- complete Process State execution semantics;
- complete Artifact lifecycle semantics;
- detailed Decision Gate evaluation procedures;
- Knowledge Continuity operational protocols;
- interruption and recovery protocols;
- Execution Mode selection criteria;
- error and exception handling;
- Runtime conformance criteria;
- implementation-specific Runtime architecture.

These subjects are addressed only where required by the present specification.

---

## 4.19 Chapter Summary

Execution Control defines how a Runtime determines and governs its next action during Process Execution.

The Runtime operates under a hierarchy of constraints:

```text
Engineering Process Model
        ↓
Current Process State
        ↓
Execution Context
        ↓
Decision Gates
        ↓
Participant Input
        ↓
Runtime Heuristics
```

The Runtime may use heuristics to select among permissible actions, but heuristics cannot override higher-level process constraints.

When sufficient information exists, the Runtime executes an appropriate action, verifies its result, and updates the Execution Context.

When reliable execution is not possible, the Runtime must not fabricate information or silently bypass constraints.

The fundamental principle of Execution Control is:

> **The Runtime is responsible for controlling execution, but it is not free to redefine what valid execution means.**

---

# Chapter 5 — Participant Interaction

## 5.1 Purpose

This chapter defines how Participants interact with the execution of a Process Instance.

Participant Interaction establishes how information, judgment, Decisions, authorization, and other legitimate contributions from Participants become part of Process Execution.

The purpose of this chapter is not to define a general human–AI interaction architecture.

It defines only the participation semantics required by the Process Execution Model.

---

## 5.2 Participant

A **Participant** is an entity that contributes to the execution of a Process Instance.

A Participant may contribute:

- information;
- Evidence;
- clarification;
- engineering work;
- analysis;
- judgment;
- Decisions;
- authorization;
- verification;
- challenges to existing conclusions.

Participation may occur at different points during execution and may vary according to the requirements of the Process Instance.

A Participant does not automatically possess unrestricted authority over the Process Instance merely by participating in it.

---

## 5.3 Participant Types

The Process Execution Model recognizes two primary forms of Participant:

- Human Participant;
- AI Agent.

These represent different forms of participation in engineering execution.

The PEM does not require Human Participants and AI Agents to have identical capabilities or authority.

Their participation is governed by the applicable process rules and execution conditions.

An AI Agent is not synonymous with the Runtime.

```text
Human Participant ──┐
                    │
AI Agent ───────────┤
                    ▼
                  Runtime
                    │
                    ▼
              Process Instance
```

The Runtime remains the mechanism responsible for executing the Process Execution Model.

---

## 5.4 Participant Capability and Authority

Participant capability and participant authority are distinct concepts.

**Capability** concerns what a Participant can perform or contribute.

**Authority** concerns what a Participant is permitted to establish, approve, authorize, or cause within the Process Instance.

A Participant may therefore have the capability to perform an activity without possessing the authority to determine its process-level outcome.

The PEM therefore does not assume:

> Capability implies authority.

Nor does it assume:

> Participation implies unrestricted authority.

Specific authority remains governed by the applicable process conditions and Execution Context.

---

## 5.5 Participant Input

**Participant Input** is information or action supplied by a Participant that may affect Process Execution.

Participant Input may include:

- information;
- Evidence;
- clarification;
- proposed actions;
- engineering analysis;
- proposed Decisions;
- approval or rejection;
- challenges to existing conclusions;
- requests for investigation or review.

Participant Input becomes relevant to execution when it affects the current Process Instance.

The Runtime must evaluate Participant Input in the context of the applicable process and execution state.

Participant Input must not be treated as authoritative merely because it originates from a Participant.

---

## 5.6 Runtime and Participants

The Runtime and Participants have different responsibilities.

The Runtime implements the Process Execution Model and controls execution according to its rules.

Participants contribute to that execution.

Conceptually:

```text
Participant
     │
     │ contributes
     ▼
Participant Input
     │
     ▼
Runtime
     │
     │ evaluates and applies
     ▼
Process Instance
```

The Runtime may:

- request Participant Input;
- present execution information requiring participant response;
- evaluate Participant Input;
- incorporate valid Participant Input into execution;
- determine that Participant Input is insufficient;
- continue execution where participant involvement is not required;
- suspend execution when required Participant Input is unavailable.

The Runtime must not silently convert participant suggestions into authoritative process Decisions when the applicable process requires further validation or authorization.

---

## 5.7 Participant-Initiated Interaction

Participants may initiate interaction with the Runtime when they have relevant information, Decisions, corrections, concerns, or other contributions.

Examples include:

- providing missing requirements;
- correcting an inaccurate Assumption;
- supplying new Evidence;
- challenging an Artifact;
- requesting investigation;
- proposing an alternative;
- approving or rejecting a Decision when authorized;
- indicating that the current execution objective has changed.

The Runtime must evaluate such input against the current Process Instance and Execution Context.

Participant-initiated interaction does not automatically cause a process transition.

The Runtime must determine whether the input:

1. changes the Execution Context;
2. requires verification;
3. requires a new Decision;
4. invalidates an existing Assumption;
5. affects a Decision Gate;
6. requires a Process State transition;
7. has no material effect on execution.

---

## 5.8 Runtime-Initiated Interaction

The Runtime may request Participant Input when execution requires information, judgment, authorization, or another contribution that cannot reliably be obtained otherwise.

The Runtime may request participation when:

- required information is missing;
- clarification is required;
- a Decision Gate requires participant involvement;
- a Decision requires authorization;
- conflicting Evidence requires resolution;
- an engineering judgment cannot be established reliably from available information;
- the Runtime identifies material uncertainty;
- continued execution would otherwise require an unsupported Assumption.

The Runtime should request only the participation necessary to continue execution appropriately.

Participant interaction should remain proportional to the needs of the Process Instance.

---

## 5.9 Participant Decisions

Participants may contribute Decisions to Process Execution.

A participant Decision may include:

- accepting a proposed conclusion;
- rejecting a proposed conclusion;
- selecting among permissible alternatives;
- approving progression;
- declining progression;
- resolving an issue within the Participant's authority.

A participant Decision becomes part of the authoritative execution state only when the applicable process conditions for recognizing that Decision have been satisfied.

The Runtime is responsible for incorporating recognized Decisions into the Execution Context.

The Runtime must not treat an informal statement as a formal process Decision when the process requires a defined Decision or approval condition.

---

## 5.10 Participant Challenges

Participants may challenge:

- Assumptions;
- Evidence;
- Decisions;
- Artifacts;
- verification results;
- proposed transitions;
- Runtime conclusions;
- AI-generated conclusions.

A challenge is legitimate Participant Input.

The existence of a challenge does not automatically invalidate the challenged result.

The Runtime must determine the appropriate response according to the current Process State and Execution Context.

Possible responses include:

- evaluate the challenge;
- request additional Evidence;
- perform verification;
- initiate investigation;
- revise an Artifact;
- reconsider a Decision;
- invoke a Decision Gate;
- suspend execution.

---

## 5.11 AI Agent Participation

An **AI Agent** is a Participant that performs engineering work or provides engineering contributions through AI-based capabilities.

An AI Agent may:

- analyze information;
- propose Solutions;
- generate or modify Artifacts;
- identify risks;
- propose Decisions;
- perform investigation;
- perform verification activities;
- identify contradictions;
- request information;
- recommend actions.

AI-generated output is Participant Input unless and until it satisfies the applicable conditions for becoming authoritative process information, a recognized Decision, or another authoritative element of the Execution Context.

Conceptually:

```text
AI Agent output
       ↓
Participant Input
       ↓
Evaluation / Verification
       ↓
Recognized execution information
```

The AI Agent does not acquire Runtime authority merely by performing engineering work.

---

## 5.12 Human Participant Participation

A Human Participant may provide engineering information, judgment, Decisions, authorization, or other contributions required by the Process Instance.

Human participation may be required when:

- the process explicitly requires human involvement;
- an authorized Decision is required;
- information exists only with the Participant;
- an engineering judgment cannot be established reliably through available execution resources;
- the Participant identifies a material issue requiring review.

Human participation does not require that the Human Participant directly control the Runtime.

The Runtime remains responsible for applying the Process Execution Model.

---

## 5.13 Participant Input and Execution Context

Participant Input that materially changes the Process Instance must be reflected in the Execution Context.

Examples include:

- newly established Requirements;
- newly supplied Evidence;
- accepted Decisions;
- changed Assumptions;
- identified risks;
- rejected conclusions;
- changed objectives;
- new unresolved questions;
- participant-approved progression.

The Runtime must ensure that recognized Participant contributions are incorporated consistently.

Conversation history or an unstructured interaction transcript is not, by itself, an authoritative update to Execution Context.

---

## 5.14 Participant Input and Decision Gates

Participant Input may be required for a Decision Gate.

Where a Decision Gate requires participant approval, the Runtime must not treat the gate as satisfied merely because the Runtime or an AI Agent considers the outcome appropriate.

Where participant approval is required and has not been obtained, the Runtime must not represent the gate as satisfied.

If required Participant Input cannot be obtained, the Runtime may:

- request the required input;
- suspend execution;
- record the pending condition.

It must not fabricate participant approval.

---

## 5.15 Conflicting Participant Input

Different Participants may provide conflicting information, judgments, or Decisions.

Conflicting Participant Input must not be silently reconciled when the conflict could materially affect Process Execution.

The Runtime must identify the conflict and determine an appropriate response according to the applicable process conditions.

Possible responses include:

- request clarification;
- obtain additional Evidence;
- initiate investigation;
- invoke a Decision Gate;
- defer the Decision;
- suspend execution.

The Runtime must not arbitrarily select one conflicting input merely to maintain execution progress.

---

## 5.16 Participant Input That Conflicts with Process Constraints

Participant Input does not override the Engineering Process Model or applicable execution constraints merely because a Participant requests a particular action.

Where Participant Input conflicts with a higher-level process constraint, the Runtime must preserve the applicable constraint.

For example:

```text
Process requires verification
        ↓
Participant requests immediate transition
        ↓
Verification not completed
        ↓
Runtime cannot bypass the requirement
```

The Runtime should instead surface the blocking condition and identify what must occur before the requested action becomes permissible.

---

## 5.17 Required Participant Input

Some execution conditions may require Participant Input before execution can continue.

When required input is unavailable, the Runtime must distinguish between:

- not yet received;
- not obtainable;
- not required;
- insufficient or ambiguous.

The Runtime must not silently treat missing required input as approval, agreement, or completion.

Where execution cannot continue without required input, the Process Instance may be suspended.

---

## 5.18 Participant Interaction Within the Execution Cycle

Participant Interaction occurs within the execution cycle established by Chapter 3.

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

Participant Input may enter the cycle at multiple points.

For example:

```text
Observe
   ↓
Participant provides new Evidence
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

Participant Interaction is therefore not a separate phase of engineering execution.

It is a cross-cutting interaction mechanism within the execution cycle.

---

## 5.19 Participant Interaction and Execution Control

Participant Interaction extends the Execution Control model established in Chapter 4.

The Runtime considers Participant Input after applying the higher-level constraints of the execution model:

```text
Engineering Process Model
        ↓
Current Process State
        ↓
Execution Context
        ↓
Decision Gates
        ↓
Participant Input
        ↓
Runtime Heuristics
```

Participant Input therefore has an important role in execution without becoming an unrestricted source of execution authority.

The Runtime remains responsible for determining the permissible execution action.

---

## 5.20 Participant Availability

A Process Instance may encounter situations in which a required Participant is temporarily unavailable.

Participant unavailability must not be interpreted as participant approval or consent.

Where required Participant Input is necessary for continued execution, the Runtime may:

- wait for the Participant;
- request the Participant again;
- identify alternative permissible participation where the process allows it;
- suspend execution.

The Runtime must not fabricate the missing contribution.

---

## 5.21 Participant Interaction and Verification

Participant contributions may themselves require verification.

For example:

- newly supplied information may require corroboration;
- AI-generated analysis may require verification;
- a proposed Decision may require Evidence;
- an Artifact modification may require review;
- a participant claim may conflict with existing Evidence.

Participant status alone does not determine factual validity.

The Runtime must apply applicable verification requirements before treating a contribution as established engineering knowledge where verification is required.

---

## 5.22 Participant Interaction Invariants

### Invariant 1 — Participation Is Not Runtime

A Participant is not the Runtime merely because the Participant performs engineering work or interacts directly with execution.

### Invariant 2 — Participation Does Not Imply Unlimited Authority

A Participant's ability to contribute does not automatically grant authority to change every aspect of the Process Instance.

### Invariant 3 — Missing Input Is Not Approval

The absence of Participant Input must not be interpreted as agreement, approval, or completion.

### Invariant 4 — Participant Input Must Respect Process Constraints

Participant Input must be evaluated within the applicable Engineering Process Model, Process State, Execution Context, and Decision Gates.

### Invariant 5 — Material Contributions Must Be Preserved

Participant Input that materially changes execution must be reflected in the authoritative Execution Context.

### Invariant 6 — Conflicts Must Not Be Hidden

Material conflicts between Participants or between Participant Input and established execution knowledge must not be silently discarded.

### Invariant 7 — AI Agent Is Not Runtime

An AI Agent may participate in execution but does not thereby become the Runtime.

### Invariant 8 — Uncertainty Must Remain Visible

The Runtime must not convert uncertain or unverified Participant Input into established knowledge merely to enable continued execution.

---

## 5.23 Scope Boundary

This chapter defines the conceptual semantics of Participant Interaction.

It does not define:

- APIs;
- message formats;
- communication protocols;
- user interfaces;
- agent frameworks;
- identity systems;
- authentication;
- authorization software;
- permission schemas;
- implementation-specific Human–AI interaction patterns;
- Runtime software architecture.

It also does not define a comprehensive organizational authority system.

Where a specific Process Instance requires different Participant roles or authorities, those requirements belong to the applicable Engineering Process Model and Execution Context.

---

## 5.24 Chapter Summary

Participants contribute to Process Execution through information, engineering work, judgment, Decisions, authorization, verification, and other legitimate forms of input.

The Runtime coordinates and evaluates this participation while continuing to enforce the execution constraints established by the Engineering Process Model and Process Execution Model.

Human Participants and AI Agents are both capable of participating in execution, but neither is synonymous with the Runtime.

The fundamental relationship is:

```text
Participant
     │
     │ contributes
     ▼
Participant Input
     │
     │ evaluated within
     ▼
Execution Control
     │
     ▼
Runtime
     │
     ▼
Process Instance
     │
     ▼
Execution Context
```

Participant Interaction is therefore not an independent workflow phase.

It is a cross-cutting mechanism through which Humans and AI Agents contribute to the iterative execution of a Process Instance.

The fundamental principle of Participant Interaction is:

> **Participants contribute to engineering execution; the Runtime governs execution according to the Process Execution Model.**
