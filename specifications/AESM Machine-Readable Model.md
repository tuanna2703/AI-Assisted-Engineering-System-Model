# AESM Machine-Readable Model

**Project:** AI-Assisted Engineering System Model (AESM)  
**Phase:** Phase 3 — Machine-Readable AESM Model  
**Status:** Candidate — Revision 1  
**Version:** 0.1.1  
**Derived from:** `specifications/AESM Operational Model.md`

---

## 1. Purpose

The AESM Machine-Readable Model defines the canonical software-consumable representation of the AESM Operational Model.

Its purpose is to make the operational semantics explicit to software without requiring software to interpret the Markdown specification directly.

The Machine-Readable Model is a **model definition**, not an engineering Process Instance. It represents the operational entity vocabulary, state, conditions, relationships, operation semantics, authority boundaries, controlled mutation path, continuity requirements, traceability requirements, and operational invariants from which later Runtime data schemas and interfaces can be derived.

It MUST preserve the semantic authority of the EPM and PEM and MUST NOT introduce implementation-specific Runtime, Agent, protocol, database, or environment semantics.

---

## 2. Scope

Phase 3 covers:

1. canonical machine-readable model identity and versioning;
2. JSON/UTF-8 serialization;
3. complete operational entity and record vocabulary;
4. entity identity strategy;
5. property and type representation;
6. explicit relationships and cardinality;
7. Process, Engineering, Decision, Knowledge, Execution, Continuity, Artifact, and Lifecycle state categories;
8. explicit condition categories and evaluation representation;
9. semantic operation representation without defining API transport;
10. EPM/PEM/Operational Model authority representation;
11. controlled mutation representation;
12. continuity and Execution Context representation;
13. traceability representation;
14. reconsideration and historical-state representation;
15. operational invariant representation;
16. structural validation of the machine-readable model itself;
17. extension boundaries;
18. repository artifact organization.

Phase 3 does **not** define:

- Agent request/response messages;
- Agent authority or execution contract details;
- protocol transport;
- Runtime API;
- environment capability API;
- physical Process Instance storage;
- conformance-test implementation;
- IDE integration.

Those belong to later phases.

---

## 3. Authority Chain

The authority chain is:

```text
EPM
  ↓
PEM
  ↓
AESM Operational Model
  ↓
AESM Machine-Readable Model
```

The Machine-Readable Model is a representation of the Operational Model. It is not a replacement for the Operational Model and MUST NOT redefine its semantics.

If a machine-readable artifact conflicts with the Operational Model, the artifact is non-conforming and MUST be corrected rather than used to redefine the Operational Model.

The Machine-Readable Model therefore has a **representation authority**, not an independent engineering authority.

---

## 4. Canonical Model Structure

The canonical model contains these semantic layers:

```text
Entity vocabulary
      +
State categories
      +
Condition categories
      +
Relationships
      +
Operation semantics
      +
Authority rules
      +
Controlled mutation
      +
Continuity
      +
Traceability
      +
Invariants
```

This is intentionally broader than an entity/field catalog. A machine-readable representation that omits state, conditions, authority, mutation, continuity, or traceability is semantically incomplete even if its JSON is structurally valid.

---

## 5. Normative Artifacts

### 5.1 Model Schema

`schemas/aesm-machine-readable-model.schema.json`

The schema uses JSON Schema Draft 2020-12 and validates the structure of the canonical model definition.

### 5.2 Canonical Model Definition

`model/aesm-operational-model.json`

The canonical model definition is the machine-readable representation of the current AESM Operational Model.

These artifacts have different responsibilities:

```text
Model Schema
= validates machine-readable model structure

Canonical Model Definition
= represents AESM operational semantics
```

---

## 6. One Canonical Semantic Model

AESM uses **one canonical operational model definition** rather than multiple competing model definitions.

The canonical model is decomposed into entity definitions internally, but all definitions remain members of one coherent model identified by:

```text
modelId = aesm.operational-model
modelVersion = MAJOR.MINOR.PATCH
```

Later Runtime data schemas MAY be split into multiple files for maintainability or implementation purposes. Such schemas MUST derive from this canonical model and MUST NOT become independent semantic authorities.

---

## 7. Serialization

The canonical serialization format is **JSON encoded as UTF-8**.

The normative schema dialect is:

`https://json-schema.org/draft/2020-12/schema`

Markdown remains the normative human-readable specification format. JSON is its machine-readable semantic representation.

---

## 8. Identity and Versioning

Operational entities MUST use stable opaque identities. The identity strategy MUST NOT require database-generated IDs, filesystem paths, IDE identifiers, or Runtime-local object addresses.

The model and schema use semantic versioning:

```text
MAJOR.MINOR.PATCH
```

A breaking semantic/compatibility change requires MAJOR; a backward-compatible addition requires MINOR; a non-semantic correction requires PATCH.

The canonical model MUST identify the EPM, PEM, and AESM Operational Model from which it is derived.

---

## 9. Entity and Record Representation

Each entity definition MUST identify:

- entity kind;
- identity;
- fields and their semantic type;
- required/optional status;
- reference targets where applicable;
- controlled vocabularies where required.

Phase 3 Revision 1 explicitly represents the following primary operational concepts:

- ProcessInstance;
- EngineeringObjective;
- ExecutionContext;
- ProcessState and ProcessStateDefinition;
- TransitionRule and Transition;
- DecisionGate and ProgressionCondition;
- Condition;
- ExecutionMode;
- Requirement and Constraint;
- Investigation and Evidence;
- Assumption and Risk;
- CandidateSolution and Evaluation;
- EngineeringDecision;
- VerificationResult and Artifact;
- ExecutionDetermination, Plan, ExecutionAction, and ExecutionResult;
- Participant, ParticipantInput, ParticipantContribution, and Observation;
- ValidationAssessment and StateMutation;
- Reconsideration;
- ExecutionTrace.

The following MUST remain distinct:

```text
EngineeringDecision ≠ ExecutionDetermination
ParticipantInput ≠ ParticipantContribution
ParticipantContribution ≠ ValidationAssessment
ValidationAssessment ≠ StateMutation
TransitionRule ≠ Transition
Engineering Completion ≠ Runtime Termination
Requirement Resolution ≠ Requirement Satisfaction
```

`Condition`, `Observation`, `ParticipantInput`, `ParticipantContribution`, `ValidationAssessment`, and `StateMutation` are operationally necessary records/types. They MUST NOT replace or redefine EPM engineering entities.

---

## 10. Execution Context

Execution Context is the authoritative operational continuation state.

The machine-readable representation MUST be capable of representing:

- current Process State;
- current Execution Mode;
- current Engineering Objective;
- Requirement state;
- Constraint state;
- Investigation state;
- Evidence and provenance/status;
- Assumptions;
- Risks;
- Candidate Solutions;
- Evaluations;
- unresolved/contested matters;
- Artifacts;
- accepted/pending Engineering Decisions;
- Decision Gates and current evaluations;
- Verification Results;
- continuity state;
- pending execution condition/activity;
- current/pending Plan;
- last authoritative update;
- interruption/resumption information;
- continuation information.

The representation MUST contain enough authoritative state to resume execution without conversational memory.

---

## 11. State and Condition Representation

AESM distinguishes state from conditions used to evaluate state progression.

### State categories

- Process State
- Engineering State
- Decision State
- Knowledge State
- Execution State
- Continuity State
- Artifact State
- Lifecycle State

### Condition categories

- Entry
- Progression
- Completion
- Exit
- Decision Gate
- Verification
- Execution Precondition
- Execution Postcondition
- Reconsideration
- Objective Change
- Mode Change

A condition representation MUST support identity, statement/expression, subject/scope, evaluation status, evaluation result, evaluation basis, and material evaluation history.

Activity completion MUST NOT be treated as sufficient evidence that a progression condition is satisfied.

---

## 12. Relationship Representation

Relationships are explicit and include source, target, cardinality, and required/optional status.

The canonical model includes, among others:

```text
ProcessInstance → EngineeringObjective
ProcessInstance → ExecutionContext
ProcessInstance → ExecutionTrace
ExecutionContext → ProcessState
ExecutionContext → Requirement
ExecutionContext → EngineeringDecision
ProcessStateDefinition → TransitionRule
Transition → TransitionRule
Transition → ExecutionTrace
Requirement → Evidence
Requirement → EngineeringDecision
Investigation → Evidence
Evidence → EngineeringDecision
CandidateSolution → Evaluation
Evaluation → EngineeringDecision
Plan → ExecutionAction
ExecutionAction → ExecutionResult
Participant → ParticipantInput
Participant → ParticipantContribution
ParticipantContribution → ValidationAssessment
ValidationAssessment → StateMutation
StateMutation → ExecutionContext
StateMutation → ExecutionTrace
Reconsideration → EngineeringDecision
```

A Runtime MAY physically store relationships using references, embedded objects, database relations, or another mechanism, provided the semantic relationships remain recoverable.

---

## 13. Operation Semantics

Operations are semantic operations, not API endpoints.

Each operation MUST be representable with:

- identity;
- operation class;
- authority layer;
- mutation classification;
- semantic subject/inputs/outputs where applicable;
- preconditions/postconditions where applicable;
- trace requirement.

The canonical operation classes are:

1. Observation
2. Evaluation
3. Investigation
4. Contribution
5. Execution
6. Reconsideration

An evaluation operation MUST NOT silently mutate authoritative engineering state merely by producing an evaluation result.

A contribution operation creates candidate information and does not automatically create authoritative state.

Execution mutations remain governed by PEM semantics.

Engineering-state reconsideration remains governed by EPM semantics.

---

## 14. Authority and Controlled Mutation

The canonical authority path is:

```text
Participant / Agent / Tool / Environment output
                 ↓
             Observation
                 ↓
       Candidate contribution
                 ↓
       Validation / evaluation
                 ↓
      Authorized state mutation
                 ↓
       Updated Execution Context
                 ↓
               Trace
```

The machine-readable model MUST preserve the distinctions between the stages in this path.

In particular:

- AI Agent output has no implicit authority to mutate engineering state;
- tool output has no implicit authority to mutate engineering state;
- environment events have no implicit authority to mutate engineering state;
- Participant input is not automatically a validated contribution;
- a contribution is not automatically authoritative state;
- validation is distinct from mutation;
- authoritative mutation MUST be attributable to an authority path and trace.

The Runtime may implement the mutation mechanism, but the semantic distinction belongs to the operational model.

---

## 15. Reconsideration and Historical State

Reconsideration is an explicit operational record/process.

It MUST be able to identify:

- trigger condition;
- affected conclusions;
- affected engineering state;
- affected Requirements/Constraints/Risks/Solutions where applicable;
- evaluation process;
- revised conclusions;
- preserved historical state;
- status;
- traceability.

Reconsideration MUST NOT silently overwrite historical engineering conclusions.

---

## 16. Traceability and Continuity

The canonical model MUST support reconstruction of the material engineering/execution chain:

```text
Requirement / Objective
       ↓
Investigation
       ↓
Evidence
       ↓
Evaluation
       ↓
Engineering Decision
       ↓
Verification
       ↓
Execution Determination / Plan
       ↓
Execution Action
       ↓
Execution Result
       ↓
Authoritative State Mutation
       ↓
Execution Context
       ↓
Execution Trace
```

Material changes MUST remain attributable to the Process Instance, ordering/timestamp, actor where relevant, source operation, affected entity, prior state where required, resulting state, supporting basis, and trace event.

---

## 17. Validation Separation

Phase 3 separates three concerns:

```text
JSON Schema
= structural validation

Operational Model
= semantic operational rules

PEM Runtime
= execution validation
```

JSON Schema MUST NOT be treated as sufficient to establish engineering validity.

A structurally valid machine-readable model can still be semantically non-conforming; semantic conformance must be reviewed against the Operational Model.

---

## 18. Operational Invariants

The canonical model explicitly represents the Phase 2 invariants, including:

- EPM engineering authority;
- PEM execution authority;
- Execution Context authority;
- Agent/Runtime separation;
- Engineering Decision/Execution Determination separation;
- Engineering Completion/Runtime Termination separation;
- knowledge-state distinctions;
- observation non-mutation;
- controlled mutation;
- traceability;
- continuity;
- reconsideration history;
- condition-driven progression;
- objective integrity;
- Requirement resolution versus satisfaction.

Each invariant has a stable identity, owner, statement, and enforcement classification.

---

## 19. Extension Rules

An extension MUST:

1. have a stable identifier;
2. declare its purpose;
3. use an identifiable namespace where appropriate;
4. avoid redefining a core entity, relationship, or invariant;
5. remain distinguishable from the canonical model;
6. preserve forward compatibility where possible.

Extensions MUST NOT change the meaning of a core AESM entity.

---

## 20. Repository Artifacts

```text
specifications/
└── AESM Machine-Readable Model.md

schemas/
└── aesm-machine-readable-model.schema.json

model/
└── aesm-operational-model.json
```

The separation is intentional:

```text
specifications/ = normative human-readable semantics
schemas/        = structural machine validation
model/          = canonical machine-readable semantic model
```

---

## 21. Phase 3 Revision 1 Conformance Gate

Revision 1 is ready for final conformance review when:

1. the canonical model is valid JSON;
2. the canonical model conforms to the Phase 3 structural schema;
3. all reconstruction-matrix entity classes are represented;
4. required semantic properties are represented;
5. required relationships are explicit;
6. state and condition categories are represented;
7. operation semantics are represented without becoming API definitions;
8. the authority/mutation path is represented;
9. continuity and traceability are represented;
10. reconsideration and historical state are represented;
11. EPM/PEM authority boundaries remain intact;
12. no core distinction has been collapsed;
13. the model remains implementation-independent.

Passing this gate permits a final Phase 3 freeze review. It does not itself authorize Phase 4.

---

## 22. Phase 3 Freeze Criteria

Phase 3 may be frozen only after the final conformance review confirms that the machine-readable model faithfully represents the frozen Operational Model and that later Runtime/Agent layers can derive their schemas without inventing or redefining core operational semantics.
