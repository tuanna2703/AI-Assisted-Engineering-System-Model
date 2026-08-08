# AI-Assisted Engineering System Model

The AI-Assisted Engineering System Model is the umbrella conceptual model for the project.

Its central structure is:

> **EPM defines the engineering process. PEM defines how that process is executed. A Runtime implements the PEM and executes Process Instances within an Execution Environment. Execution Context represents the authoritative operational state of a Process Instance. Humans and AI Agents participate in that execution.**

The model therefore provides a stable conceptual map without requiring the project to prematurely define implementation architecture.

The current engineering objective is to complete and validate the Engineering Process Model and Process Execution Model specifications before expanding the system model further.

## 1. Model Scope

The AI-Assisted Engineering System Model describes the overall conceptual structure of an AI-assisted engineering system.

It provides the conceptual relationship between:

- Engineering Process Model (EPM);
- Process Execution Model (PEM);
- Runtime;
- Process Instance;
- Execution Context;
- Participants;
- Artifacts, Evidence, Decisions, and Assumptions;
- Execution Environment.

## 2. Central Relationship

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

Participants contribute to the execution of Process Instances through the Runtime, while the Runtime operates within an Execution Environment.

## 3. Engineering Process Model

The **Engineering Process Model (EPM)** defines what constitutes valid engineering work and how the engineering process is structured.

It establishes engineering-level concepts and rules such as:

- Principles;
- Process States;
- State Schema;
- Transition Rules;
- Trigger Conditions;
- Decision Gates;
- Execution Modes;
- Verification;
- Traceability;
- Risk Management;
- Assumption Management;
- Knowledge Continuity;
- Artifacts.

The EPM is implementation-independent and represents the engineering semantics of the system.

## 4. Process Execution Model

The **Process Execution Model (PEM)** defines how the Engineering Process Model is executed.

It is implementation-independent and specifies execution semantics rather than a particular software implementation.

The PEM establishes an iterative execution model:

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

The PEM also defines execution control. The current conceptual authority sequence is:

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

## 5. Runtime

A **Runtime** is an implementation of the Process Execution Model.

The Runtime executes Process Instances according to the execution semantics defined by the PEM and the engineering semantics defined by the EPM.

The Runtime is distinct from both the PEM and the Execution Environment and is not an independent source of engineering authority.

The AESM does not prescribe a particular Runtime architecture.

## 6. Process Instance

A **Process Instance** represents one execution of the Engineering Process Model for a specific engineering objective.

It has an evolving operational state including, among other things:

- current Process State;
- execution objective;
- execution mode;
- engineering progress;
- Decisions;
- Evidence;
- Assumptions;
- risks;
- unresolved questions;
- Artifacts;
- pending actions.

The Process Instance is the object of execution for the Runtime.

## 7. Execution Context

**Execution Context** is the authoritative operational state required to execute a Process Instance consistently at a specific point in time.

It represents the minimum authoritative information necessary for a conforming Runtime to continue execution without altering engineering intent, execution semantics, or current progress.

Execution Context is a logical concept rather than a particular document or storage format.

It logically contains:

### Process Status

- Process Instance identity;
- active Process State;
- execution objective;
- execution mode.

### Engineering State

- artifacts;
- artifact status;
- completed work;
- remaining work.

### Decision State

- accepted decisions;
- pending decisions;
- Decision Gates.

### Knowledge State

- Evidence;
- Assumptions;
- risks;
- unresolved questions.

### Continuity State

- interruption point;
- pending activities;
- next expected action.

Conversation history is not itself Execution Context.

## 8. Participants

A **Participant** is an entity that contributes to the execution of a Process Instance.

Participants may contribute:

- information;
- Evidence;
- engineering work;
- analysis;
- judgment;
- Decisions;
- authorization;
- clarification;
- verification;
- challenges to existing conclusions.

Two primary participant forms are recognized:

- Human Participant;
- AI Agent.

An AI Agent is not synonymous with the Runtime.

Participation does not automatically imply unrestricted authority. Participant authority is governed by the applicable process and execution conditions.

## 9. Artifacts and Engineering Knowledge

Important supporting concepts include:

- **Artifacts** — persistent representations of engineering knowledge produced or consumed during execution.
- **Evidence** — information used to support engineering conclusions and Decisions.
- **Assumptions** — propositions accepted temporarily or conditionally when sufficient Evidence is not available.
- **Decisions** — conclusions or commitments that affect engineering direction.
- **Verification** — activities used to establish whether a result, Decision, or state satisfies applicable requirements.

## 10. Knowledge Continuity

Knowledge generated during engineering execution must remain available for subsequent execution.

Important engineering knowledge must not exist solely in transient participant memory or conversational context.

Execution Context provides the authoritative operational state needed for continuation across interruptions, context switches, or Runtime replacement.

Session Collapse is a mechanism for preserving or transferring the information required to reconstruct or continue Execution Context; it is not itself the Execution Context.

## 11. Execution Environment

The **Execution Environment** is the environment in which a Runtime operates.

Examples may include:

- a conversational AI environment;
- an IDE;
- a CLI;
- a web application.

The Execution Environment should not be confused with the Runtime.

```text
Execution Environment
        │
        │ hosts / supports
        ▼
     Runtime
        │
        │ executes
        ▼
Process Instance
```

## 12. What the AESM Does Not Define

The AI-Assisted Engineering System Model does not currently define:

- a software architecture;
- a Runtime implementation;
- an AI-agent architecture;
- APIs;
- communication protocols;
- data schemas;
- storage formats;
- user interfaces;
- permission systems;
- orchestration mechanisms;
- Session Collapse implementation;
- a specific execution environment.

These may become subjects of future work if required. They are not prerequisites for defining the EPM and PEM.

## 13. Relationship to the Specifications

The AESM provides the conceptual map.

The **EPM Specification** defines the Engineering Process Model in detail.

The **PEM Specification** defines the Process Execution Model in detail.

```text
AI-Assisted Engineering System Model
                │
        ┌───────┴────────┐
        ▼                ▼
 EPM Specification   PEM Specification
        │                │
        │                │
 What engineering       How engineering
 work means             execution occurs
```

The specifications should not be replaced by this document.

## 14. Current Development Principle

The AI-Assisted Engineering System Model is intentionally broader than the specifications currently being developed.

The project should proceed by documenting and validating what currently exists before designing what does not yet exist.

The current development sequence is:

```text
AI-Assisted Engineering System Model
              │
              ▼
     Complete EPM Specification
              │
              ▼
     Complete PEM Specification
              │
              ▼
       Practical Validation
              │
              ▼
 Identify genuine deficiencies
              │
              ▼
 Refine the model where evidence
       demonstrates a need
```
