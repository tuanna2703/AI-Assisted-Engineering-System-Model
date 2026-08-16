# Engineering Process Model

**Conceptual Version:** Concept Freeze v0.1  
**Specification Status:** Completeness Revision

---

## 1. Purpose

The **Engineering Process Model (EPM)** defines what constitutes valid engineering work and how the engineering process is structured.

It establishes engineering-level concepts, relationships, rules, and invariants that execution must respect.

The EPM is implementation-independent. It does not define how a particular Runtime implements or executes the process.

The EPM is authoritative for engineering semantics. The Process Execution Model (PEM) is authoritative for execution semantics.

---

## 2. Scope

The EPM defines:

- engineering objectives;
- Requirements and their resolution;
- Constraints;
- Investigation;
- Evidence;
- Assumptions;
- Candidate Solutions and Evaluation;
- Engineering Decisions;
- Verification;
- Artifacts;
- Risks;
- Process States and their schema;
- transition rules and progression conditions;
- Decision Gates;
- Execution Modes as engineering-level rigor classifications;
- traceability;
- controlled reconsideration;
- engineering completion conditions;
- engineering-level process integrity and invariants.

The EPM does not define:

- Runtime architecture;
- execution-cycle mechanics;
- Execution Context storage or serialization;
- Participant interaction mechanics;
- interruption or resumption mechanics;
- APIs, databases, interfaces, prompts, or other implementation technologies;
- organizational governance or access-control mechanisms except where an applicable engineering rule requires an authorized Decision.

Those concerns belong to the PEM or to implementation and governance layers as appropriate.

---

## 3. Core Principles

Engineering work is:

- objective-driven;
- iterative;
- evidence-based;
- requirement-directed;
- decision-traceable;
- verifiable;
- subject to applicable Constraints and risks;
- capable of controlled reconsideration.

The engineering process is not a rigid linear workflow. Its structure is determined by the current engineering state and the conditions governing valid progression.

---

## 4. Engineering Process

The EPM describes engineering through the following conceptual relationship:

```text
Engineering Objective
        │
        ▼
Requirements ─────── Constraints
        │                 │
        └──────┬──────────┘
               ▼
         Investigation
               │
        ┌──────┴──────┐
        ▼             ▼
     Evidence     Assumptions
        │             │
        └──────┬──────┘
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
        ┌──────┴──────┐
        ▼             ▼
     Progression   Reconsideration
        │             │
        └──────┬──────┘
               ▼
       Updated Engineering State
               │
               └──────────► Iterate
```

The diagram describes engineering semantics, not the execution cycle used by a Runtime.

---

## 5. Normative Language

The terms **shall**, **shall not**, **may**, and **should** are used with the following meaning:

- **shall** — mandatory requirement for conformance to the EPM;
- **shall not** — prohibited behavior;
- **may** — permitted behavior that is not required;
- **should** — recommended behavior that may be omitted only when a justified engineering reason exists.

Where the EPM uses descriptive language without a normative keyword, the statement describes a concept or relationship rather than imposing an independent conformance requirement.

---

## 6. Engineering Objective

### Definition

An **Engineering Objective** is the explicit engineering outcome or purpose toward which a Process Instance is directed.

An Engineering Objective shall be sufficiently clear to determine whether engineering work remains relevant to the intended outcome.

### Integrity

The Engineering Objective shall not be silently changed during engineering work.

A material change to the objective shall be explicitly recognized and shall cause the affected Requirements, Decisions, Solutions, and verification conditions to be reconsidered as necessary.

The EPM does not prescribe how a Runtime records an objective change.

---

## 7. Requirements

### Definition

A **Requirement** is an explicit condition, capability, property, or outcome that engineering work is required or intended to satisfy.

Requirements provide criteria against which Candidate Solutions, Decisions, Artifacts, and verification results may be evaluated.

### Resolution States

A Requirement shall have an explicit resolution state. The EPM recognizes:

- **Open** — the Requirement has not yet been sufficiently resolved for its current engineering purpose;
- **Contested** — the Requirement, its interpretation, applicability, or satisfaction is materially disputed or uncertain;
- **Resolved** — the Requirement has an accepted interpretation and sufficient basis for its current engineering use.

Resolution state does not by itself establish that a Requirement is satisfied.

### Integrity

Requirements shall not be silently reinterpreted merely to make a Candidate Solution appear viable.

A material change to a Requirement shall preserve traceability to its previous interpretation and may require affected Decisions, Solutions, and verification results to be reconsidered.

---

## 8. Constraints

### Definition

A **Constraint** is a condition that restricts the set of acceptable engineering Solutions, Decisions, activities, or outcomes.

Constraints may arise from technical conditions, resources, compatibility, interfaces, timing, safety, operational realities, or other applicable engineering circumstances.

A Constraint is not itself a Requirement, although a Constraint may influence whether a Requirement can be satisfied.

### Use

Applicable Constraints shall be considered when evaluating Candidate Solutions and determining whether progression is valid.

A Constraint that materially changes shall be traceable and shall trigger reconsideration of affected engineering conclusions where necessary.

---

## 9. Investigation

### Definition

**Investigation** is objective-driven engineering work performed to reduce material uncertainty or obtain knowledge necessary for evaluation, decision-making, execution, or verification.

Investigation is defined by its purpose rather than by a fixed list of activities.

### Outputs

Investigation may produce or identify:

- Evidence;
- Constraints;
- unresolved questions;
- Assumptions;
- risks;
- candidate approaches;
- other knowledge required for engineering progression.

Investigation shall continue when material uncertainty prevents a reliable engineering Decision or progression and sufficient additional investigation is reasonably available.

---

## 10. Evidence

### Definition

**Evidence** is information used to support or justify engineering conclusions, Decisions, evaluations, or verification results.

Evidence may originate from documentation, code, experiments, measurements, stakeholders, operational systems, or other observable sources.

### Evidence Integrity

Evidence shall remain distinguishable from Assumptions and unsupported claims.

Evidence should retain sufficient provenance or context to allow its relevance and reliability to be evaluated.

Evidence that is materially invalidated, superseded, or contradicted shall not continue to be treated as unqualified support for an affected conclusion.

---

## 11. Assumptions

### Definition

An **Assumption** is a proposition accepted for engineering purposes without sufficient Evidence to establish it as a supported conclusion.

Assumptions shall be explicitly identifiable.

### Management

Material Assumptions shall be monitored for resolution, invalidation, or continued acceptance.

Engineering work should replace material Assumptions with Evidence whenever practical.

An Assumption that becomes invalid or materially uncertain shall trigger reconsideration of affected Decisions, Solutions, or progression conditions.

---

## 12. Candidate Solutions and Evaluation

### Candidate Solution

A **Candidate Solution** is a proposed approach for satisfying applicable Requirements while respecting applicable Constraints and engineering conditions.

The existence of a Candidate Solution does not establish that it is acceptable or valid.

### Evaluation

**Evaluation** is the engineering activity of comparing Candidate Solutions or conclusions against applicable Requirements, Evidence, Constraints, risks, and other relevant conditions.

Evaluation shall identify the basis on which a material Solution is considered acceptable, unacceptable, or unresolved.

Where no Candidate Solution satisfies the applicable conditions, the engineering process shall permit additional investigation, revision of Candidate Solutions, or controlled reconsideration of affected assumptions and Requirements.

---

## 13. Engineering Decisions

### Definition

An **Engineering Decision** is an accepted engineering conclusion or commitment that establishes direction, resolves material uncertainty, selects or rejects a Solution, or authorizes progression within the engineering process.

### Decision Conditions

A material Decision shall be supported by sufficient applicable Evidence and shall account for relevant Requirements, Constraints, risks, and verification status.

Where a Decision depends on an unresolved Requirement, material Assumption, or unresolved risk, that dependency shall remain explicit.

### Decision Integrity

Material Decisions shall remain understandable and traceable in proportion to their impact.

A Decision shall be distinguishable from a proposal, option, hypothesis, or unaccepted alternative.

A Decision that is invalidated by material new information shall be subject to controlled reconsideration rather than silently replaced.

---

## 14. Verification

### Definition

**Verification** is the activity of evaluating whether an engineering result, Artifact, Decision, Requirement outcome, or Process State satisfies applicable requirements and conditions.

Verification produces Evidence about engineering correctness, completeness, consistency, readiness, or other applicable criteria.

### Cross-Cutting Nature

Verification is cross-cutting and may occur throughout engineering work rather than only at the end.

Required verification shall not be silently bypassed.

Verification failure shall prevent progression where the failed condition is a required progression condition, unless the applicable engineering rules explicitly permit controlled deviation.

Verification results may trigger additional investigation, revision, or reconsideration.

---

## 15. Artifacts

### Definition

An **Artifact** is a persistent representation of engineering knowledge or an engineering result produced, consumed, or modified during the process.

Examples may include specifications, designs, source code, test results, analysis records, decision records, configuration, or other persistent engineering outputs.

### Artifact Status

An Artifact may have an engineering status appropriate to its purpose, including states such as proposed, active, superseded, verified, rejected, or obsolete.

The exact status vocabulary may vary by engineering domain, but the status of a material Artifact shall remain explicit enough to determine whether it may be relied upon for current engineering work.

### Artifact Integrity

Material Artifact changes shall preserve traceability to the relevant Decision, Requirement, or other engineering basis where such traceability is applicable.

An Artifact shall not be represented as verified merely because it exists or has been produced.

---

## 16. Risks

### Definition

A **Risk** is a recognized possibility of an undesirable condition or consequence that may affect engineering objectives, Requirements, Solutions, Decisions, execution, or verification.

### Risk Management

Material Risks shall be identifiable and shall be considered when evaluating Candidate Solutions and making material Decisions.

Risk treatment may include:

- acceptance;
- mitigation;
- avoidance;
- transfer to an appropriate authority or process;
- additional investigation;
- monitoring.

A material change in Risk shall be capable of triggering reconsideration of affected Decisions or progression conditions.

The EPM defines engineering risk semantics; organizational risk ownership and governance remain outside the EPM unless explicitly incorporated as an engineering Constraint or Requirement.

---

## 17. Process States

### Definition

A **Process State** represents a defined stage or condition of engineering work within a Process Instance.

A Process State does not prescribe Runtime behavior. It establishes the engineering conditions under which particular work is permissible, expected, complete, or incomplete.

### State Schema

Every formally defined Process State shall specify, as applicable:

- **Identity** — unique name or identifier;
- **Purpose** — engineering purpose of the state;
- **Objective Relationship** — how the state contributes to the Engineering Objective;
- **Applicable Inputs** — information or conditions required to perform the state;
- **Permitted Activities** — engineering work that may be performed within the state;
- **Expected Outputs** — results or knowledge expected from the state;
- **Invariants** — conditions that shall remain true while the state is active;
- **Entry Conditions** — conditions required before entering the state;
- **Progression Conditions** — conditions that permit advancement within or beyond the state;
- **Completion Conditions** — conditions establishing that the state's purpose has been achieved;
- **Exit Conditions** — conditions governing valid movement out of the state;
- **Applicable Decision Gates** — gates that must be satisfied before relevant progression;
- **Verification Requirements** — verification necessary for valid completion or exit;
- **Reconsideration Conditions** — conditions requiring return to earlier work or reassessment.

Not every state requires a unique value for every field, but a state definition shall explicitly identify fields that are not applicable where omission could create ambiguity.

### State Semantics

A Process State defines engineering meaning, not execution mechanics.

The EPM does not prescribe a universal fixed set of Process States. Different engineering processes may define different state structures provided they conform to the EPM's semantic rules.

---

## 18. Transition Rules and Progression

### Definition

A **Transition** is a valid change from one Process State to another, or from one defined engineering condition to another, within a Process Instance.

A **Transition Rule** defines the engineering conditions under which a transition is valid.

### Transition Conditions

A Transition Rule shall identify, as applicable:

- source state or condition;
- target state or condition;
- required Requirements and their resolution state;
- required Evidence;
- required Decisions;
- applicable Constraints;
- required verification;
- applicable Decision Gates;
- conditions that prohibit transition;
- conditions requiring reconsideration instead.

A transition shall not be considered valid solely because its target state appears desirable or because the expected activities have been performed.

### Progression

**Engineering Progression** occurs when the conditions required to move engineering work forward have been sufficiently established.

Progression shall be based on the applicable engineering conditions rather than solely on passage of time, completion of an activity list, or pressure to produce an output.

The PEM governs how a Runtime evaluates and executes transitions; the EPM defines the engineering validity conditions of those transitions.

---

## 19. Decision Gates

### Definition

A **Decision Gate** is an explicit engineering condition at which progression or a material Decision requires establishment of specified criteria before it may be accepted.

A Decision Gate shall identify, as applicable:

- the Decision or progression it governs;
- required inputs;
- required Evidence;
- required verification;
- applicable Requirements and Constraints;
- relevant Risks or Assumptions;
- acceptance conditions;
- rejection or deferral conditions;
- reconsideration conditions.

### Gate Semantics

A Decision Gate does not itself prescribe who or what performs the evaluation. Authority and interaction mechanics belong to the applicable execution and governance layers.

An applicable Decision Gate shall not be treated as satisfied merely because its expected outcome appears obvious.

If a gate cannot be evaluated reliably from the available engineering information, the gate shall remain unresolved and the process shall not represent it as satisfied.

---

## 20. Execution Modes

The EPM recognizes execution modes that affect the rigor applied to engineering work.

### Direct Mode

Appropriate for straightforward, low-risk work where the solution path is sufficiently clear.

### Guided Mode

Appropriate where moderate uncertainty, complexity, or coordination requires additional investigation, documentation, or verification.

### Full Mode

Appropriate for work with substantial complexity, risk, uncertainty, or consequence. It provides the highest level of process rigor, including stronger investigation, documentation, Decision traceability, verification, review, and Evidence preservation.

Mode selection should reflect the characteristics and consequences of the engineering work.

Execution mode affects the rigor applied to engineering work; it does not alter the fundamental validity conditions defined by the EPM.

The PEM defines how an execution mode is operationally applied by a Runtime.

---

## 21. Traceability

### Definition

**Traceability** is the persistent relationship between engineering elements that allows the basis, evolution, and verification of material engineering reasoning to be reconstructed.

### Required Relationships

For material engineering work, traceability shall support the following relationships where applicable:

```text
Requirement
   │
   ├── supported / clarified by → Evidence
   ├── constrained by → Constraint
   ├── addressed by → Candidate Solution
   └── evaluated by → Evaluation

Decision
   │
   ├── addresses → Requirement
   ├── based on → Evidence
   ├── selects / rejects → Candidate Solution
   └── verified by → Verification

Artifact
   │
   ├── implements / represents → Decision
   ├── addresses → Requirement
   └── evaluated by → Verification
```

The exact representation of these relationships is implementation-dependent, but the semantic relationships shall remain reconstructable for material engineering decisions.

Traceability shall preserve sufficient linkage across controlled reconsideration so that the evolution from prior to current engineering conclusions remains understandable.

---

## 22. Knowledge Continuity

Knowledge generated during engineering execution must remain available for subsequent execution.

Important engineering knowledge shall not exist solely in transient participant memory or conversational context.

Continuity shall preserve sufficient information to understand:

- the Engineering Objective;
- current Requirements and their resolution state;
- applicable Constraints;
- important Evidence;
- significant Assumptions;
- important Decisions;
- current Candidate Solutions and relevant evaluations;
- material Risks;
- current Process State;
- unresolved matters;
- relevant Artifacts and their status;
- verification status;
- applicable progression and gate conditions.

The specific mechanism for preserving and transferring this state belongs to the Process Execution Model.

---

## 23. Controlled Reconsideration

Because engineering is iterative, previously established conclusions may become invalid.

**Controlled Reconsideration** is the explicit process of reassessing affected engineering elements when material new information, changed conditions, failed verification, invalidated assumptions, or other significant events undermine a prior conclusion.

Reconsideration may affect:

- Requirements;
- Constraints;
- Evidence;
- Assumptions;
- Candidate Solutions;
- Decisions;
- Risks;
- Artifacts;
- verification results;
- Process State progression.

Reconsideration shall preserve traceability to the previous engineering state.

A reconsidered element shall not be silently overwritten when doing so would obscure the evolution of material engineering reasoning.

---

## 24. Process Completion

### Definition

**Engineering Process Completion** is the engineering condition in which the Process Instance has satisfied the applicable final Requirements, required verification, required Decision Gates, and other completion conditions established by its governing Process definition.

Completion is an engineering validity condition. It does not define how a Runtime terminates or records the Process Instance.

### Completion Conditions

A process definition shall identify its completion conditions sufficiently to determine when the Engineering Objective has been adequately addressed.

Where applicable, completion conditions shall account for:

- resolved and satisfied material Requirements;
- applicable Constraints;
- required Decisions;
- required verification results;
- material Risks and accepted residual conditions;
- required Artifacts and their status;
- unresolved matters that prevent valid completion;
- applicable final Decision Gates.

A Process Instance shall not be considered engineering-complete merely because planned activities have been performed or an expected Artifact has been produced.

### Relationship to Termination

Engineering completion establishes eligibility for execution termination; the PEM defines the execution semantics for recognizing and performing that termination.

A Process Instance may also be suspended or terminated without engineering completion when the applicable execution or governance conditions permit it. Such termination shall not be represented as Engineering Process Completion unless the EPM completion conditions are satisfied.

---

## 25. Process Integrity

The Engineering Process Model establishes the authoritative engineering semantics of the process.

Execution shall therefore preserve:

### Objective Integrity

The Engineering Objective shall not be silently changed.

### Requirement Integrity

Requirements shall not be silently reinterpreted merely to make a Solution appear viable.

### Evidence Integrity

Unsupported information shall not be represented as established Evidence.

### Assumption Integrity

Material Assumptions shall remain identifiable and shall not silently acquire the status of Evidence.

### Decision Integrity

Material Decisions shall remain understandable and traceable in proportion to their impact.

### Verification Integrity

Required verification shall not be silently bypassed or represented as successful without sufficient basis.

### Artifact Integrity

Material Artifacts shall retain sufficient status and traceability to determine whether they may be relied upon.

### Risk Integrity

Material Risks shall remain visible to the engineering decisions and progression conditions they affect.

### Transition Integrity

Engineering progression shall occur only when applicable Transition Rules and Decision Gates permit it.

### Knowledge Integrity

Material engineering knowledge shall remain available across execution boundaries.

### Iteration Integrity

New Evidence or materially changed conditions shall be capable of causing legitimate reconsideration.

---

## 26. Engineering Invariants

The Engineering Process Model is governed by the following fundamental invariants:

1. **Objective-Driven Engineering** — engineering work remains directed toward an explicit Engineering Objective.
2. **Requirement Integrity** — material Requirements remain explicit and shall not be silently reinterpreted.
3. **Evidence Distinction** — Evidence remains distinguishable from Assumptions and unsupported claims.
4. **Explicit Requirement Resolution** — Requirements have an explicit resolution state.
5. **Decision Traceability** — material Decisions remain traceable to their engineering basis.
6. **Verification Integrity** — required verification cannot be silently bypassed.
7. **Progression Validity** — engineering progression requires satisfaction of applicable progression conditions.
8. **Gate Integrity** — applicable Decision Gates cannot be silently bypassed.
9. **Artifact Integrity** — material engineering outputs remain identifiable and their relevant status remains explicit.
10. **Risk Visibility** — material Risks remain visible to affected engineering Decisions and progression conditions.
11. **Knowledge Continuity** — material engineering knowledge remains available across execution boundaries.
12. **Completion Integrity** — Engineering Process Completion is determined by explicit engineering completion conditions, not merely activity completion.
13. **Iteration** — material new Evidence or changed conditions can cause controlled reconsideration.
14. **Implementation Independence** — engineering semantics do not depend on a particular Runtime, software architecture, AI model, or storage mechanism.

---

## 27. Process Model Boundaries

The EPM defines the engineering process but does not define its execution implementation.

The following belong to the Process Execution Model:

- Runtime behavior;
- execution cycle;
- execution control;
- Participant interaction mechanics;
- Execution Context management and persistence mechanics;
- interruption and resumption mechanics;
- Runtime conformance mechanisms;
- execution termination mechanics.

The following belong to implementation:

- APIs;
- software architecture;
- databases and storage formats;
- user interfaces;
- AI model selection;
- prompt construction;
- communication protocols.

The following may belong to governance or organizational policy rather than the EPM:

- organizational authority structures;
- access-control systems;
- personnel roles;
- approval workflows that are not intrinsic to engineering validity.

The EPM therefore remains independent of the mechanism used to execute it.

---

## 28. Relationship to the Process Execution Model

The EPM and PEM define different aspects of the same system.

The EPM defines:

- engineering concepts;
- engineering state;
- engineering validity conditions;
- Process State definitions;
- Transition Rules;
- Decision Gates;
- engineering progression;
- Engineering Process Completion;
- engineering integrity and invariants.

The PEM defines:

- execution behavior;
- execution cycle;
- Participant interaction;
- execution control;
- Execution Context management;
- interruption and resumption;
- execution termination;
- Runtime conformance.

The boundary is therefore:

```text
Engineering Process Model
        │
        │ defines engineering meaning and validity
        ▼
Process Execution Model
        │
        │ defines execution semantics
        ▼
Runtime
        │
        │ implements PEM
        ▼
Process Instance
```

The PEM shall not redefine engineering validity conditions established by the EPM, and the EPM shall not prescribe Runtime execution mechanics.

---

## 29. Conformance-Oriented Requirements

A process definition conforms to the EPM when its material engineering semantics are explicitly defined sufficiently to determine:

- the Engineering Objective;
- applicable Requirements and their resolution;
- applicable Constraints;
- relevant Evidence and Assumptions;
- Candidate Solutions and their evaluation;
- material Decisions;
- verification conditions;
- material Artifacts and their status;
- material Risks;
- Process States and their required schema;
- valid Transition Rules;
- applicable Decision Gates;
- progression and completion conditions;
- traceability relationships;
- controlled reconsideration conditions.

Conformance does not require a specific document structure, storage format, software implementation, or Runtime architecture.

The PEM defines the additional requirements for a Runtime claiming execution conformance.

---

## 30. Core Invariants Summary

The EPM can be summarized by the following invariant chain:

```text
Objective
   ↓
Requirements + Constraints
   ↓
Investigation
   ↓
Evidence + Assumptions + Risks
   ↓
Candidate Solutions
   ↓
Evaluation
   ↓
Decision
   ↓
State / Progression Conditions
   ↓
Execution
   ↓
Verification
   ↓
Updated Engineering State
   ↓
Traceability
   ↓
Reconsider when material conditions change
   ↺
```

The chain is not a mandatory linear activity sequence. It represents the dependencies that must remain semantically coherent as engineering work evolves.
