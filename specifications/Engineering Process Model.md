# Engineering Process Model

**Conceptual Version:** Concept Freeze v0.1

## 1. Purpose

The **Engineering Process Model (EPM)** defines what constitutes valid engineering work and how the engineering process is structured.

It establishes engineering-level concepts and rules that execution must respect.

The EPM is implementation-independent. It does not define how a particular Runtime implements or executes the process.

## 2. Core Principles

Engineering work is objective-driven, iterative, evidence-based, and subject to explicit requirements, decisions, verification, and controlled reconsideration.

## 3. Engineering Process

The EPM describes engineering through concepts including:

- engineering objectives;
- Requirements;
- Investigation;
- Evidence;
- Constraints;
- Candidate Solutions;
- Evaluation;
- Engineering Decisions;
- Execution;
- Verification;
- updated knowledge and Artifacts;
- controlled reconsideration.

The conceptual process is iterative rather than a rigid linear workflow.

```text
Engineering Objective
        │
        ▼
Requirements
        │
        ▼
Investigation
        │
        ├──────── Evidence
        └──────── Constraints
                 │
                 ▼
        Candidate Solutions
                 │
                 ▼
             Evaluation
                 │
                 ▼
        Engineering Decision
                 │
                 ▼
             Execution
                 │
                 ▼
            Verification
                 │
                 ▼
        Updated Knowledge
                 │
                 ▼
        Updated Artifacts
                 │
                 ▼
       Reconsider where required
                 │
                 └──────► Iterate
```

## 4. Requirements

Requirements may have multiple possible outcomes and may be:

- Resolved;
- Contested;
- Open.

Requirement resolution must remain explicit.

## 5. Investigation

Investigation exists to resolve questions necessary for the engineering objective rather than to satisfy arbitrary activity lists.

Investigation should produce or identify Evidence, Constraints, unresolved questions, and other knowledge needed for evaluation and decision-making.

## 6. Evidence

**Evidence** is information used to justify engineering Decisions and conclusions.

Evidence may originate from documentation, code, experiments, measurements, stakeholders, or operational systems.

Evidence must remain distinguishable from Assumptions.

## 7. Assumptions

An **Assumption** is a temporary proposition accepted without sufficient Evidence.

Assumptions shall be explicitly identifiable. Engineering execution should seek to replace material assumptions with Evidence whenever practical.

## 8. Solutions and Evaluation

Candidate Solutions are evaluated against applicable Requirements, Evidence, Constraints, risks, and other relevant engineering conditions.

The existence of a candidate Solution does not establish that it is valid.

## 9. Decisions

Engineering Decisions establish conclusions or commitments that affect engineering direction.

Material Decisions should remain understandable and traceable in proportion to their impact.

## 10. Verification

Verification is cross-cutting and applies throughout engineering execution.

Required verification must not be silently bypassed.

Verification results contribute to updated engineering knowledge and may trigger reconsideration when they reveal deficiencies or new information.

## 11. Execution Modes

The EPM recognizes execution modes that affect the rigor applied to engineering work.

### Direct Mode

Appropriate for straightforward, low-risk work where the solution path is sufficiently clear.

### Guided Mode

Appropriate where moderate uncertainty, complexity, or coordination requires additional investigation, documentation, or verification.

### Full Mode

Appropriate for work with substantial complexity, risk, uncertainty, or consequence. It provides the highest level of process rigor, including stronger investigation, documentation, Decision traceability, verification, review, and Evidence preservation.

Mode selection should reflect the characteristics and consequences of the engineering work. Execution mode affects rigor, not the fundamental validity of the engineering process.

## 12. Knowledge Continuity

Knowledge generated during engineering execution must remain available for subsequent execution.

Important engineering knowledge must not exist solely in transient participant memory or conversational context.

Continuity should preserve sufficient information to understand:

- the engineering objective;
- current Requirements and their resolution state;
- important Evidence;
- significant Assumptions;
- important Decisions;
- current Solutions;
- unresolved matters;
- relevant Artifacts;
- verification status.

The specific execution mechanism for preserving and transferring this state belongs to the Process Execution Model.

## 13. Engineering Progression

Engineering progression occurs when sufficient conditions have been established for work to move forward.

Progression should be based on:

- current Requirements;
- Evidence;
- Decisions;
- verification;
- applicable Constraints;
- current engineering state.

Progression must not be based solely on passage of time, completion of an activity list, or pressure to produce an output.

## 14. Controlled Reconsideration

Because engineering is iterative, previously established conclusions may become invalid.

When significant new Evidence appears, the process should permit controlled reconsideration of:

- Requirements;
- Solutions;
- Decisions;
- Artifacts;
- Assumptions;
- verification results.

Reconsideration should preserve traceability to the previous state so that the evolution of engineering reasoning remains understandable.

## 15. Process Integrity

The Engineering Process Model establishes the authoritative engineering semantics of the process.

Execution must therefore preserve:

### Objective Integrity

The engineering objective must not be silently changed.

### Requirement Integrity

Requirements must not be silently reinterpreted merely to make a Solution appear viable.

### Evidence Integrity

Unsupported information must not be represented as established Evidence.

### Decision Integrity

Material Decisions must remain understandable and traceable in proportion to their impact.

### Verification Integrity

Required verification must not be silently bypassed.

### Knowledge Integrity

Material engineering knowledge must remain available across execution boundaries.

### Iteration Integrity

New Evidence must be capable of causing legitimate reconsideration.

## 16. Process Model Boundaries

The EPM defines the engineering process but does not define its execution implementation.

The following belong to the Process Execution Model:

- Runtime behavior;
- execution cycle;
- execution control;
- Participant interaction;
- Execution Context management;
- interruption and resumption mechanics.

The following belong to implementation:

- APIs;
- software architecture;
- databases;
- user interfaces;
- AI model selection;
- prompt construction;
- communication protocols.

The EPM therefore remains independent of the mechanism used to execute it.

## 17. Core Invariants

The Engineering Process Model is governed by the following fundamental invariants:

1. **Objective-Driven Engineering** — engineering work remains directed toward an explicit engineering objective.
2. **Iterative Execution** — engineering conclusions may be revisited when material new Evidence becomes available.
3. **Investigation Is Objective-Driven** — investigation exists to resolve questions necessary for the engineering objective.
4. **Requirements May Have Multiple Outcomes** — a Requirement may have zero, one, or multiple viable Solutions.
5. **Requirement Resolution Is Explicit** — Requirements may be Resolved, Contested, or Open.
6. **Verification Is Cross-Cutting** — verification applies throughout engineering execution.
