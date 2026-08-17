# Phase 3 Revision 1 — Semantic Reconstruction Matrices

**Project:** AI-Assisted Engineering System Model (AESM)  
**Phase:** Phase 3 Revision 1  
**Status:** Reconciled Working Baseline — Canonical Model Not Yet Regenerated  
**Version:** 0.1.1  
**Authority:** Phase 2 AESM Operational Model, with EPM and PEM semantic authority

## 1. Purpose

These matrices reconstruct the Phase 2 Operational Model into a machine-readable semantic inventory before regeneration of the canonical JSON model and structural schema.

```text
EPM / PEM
   ↓
AESM Operational Model
   ↓
Semantic inventory
   ↓
Reconciliation matrices
   ↓
Canonical machine-readable model
   ↓
Derived schemas
```

The matrices are intermediate semantic artifacts. They do not define an API, Agent protocol, Runtime architecture, database schema, or programming-language implementation.

---

# 2. Reconciliation Results

The first matrix draft exposed several issues that are corrected here.

| Finding | Resolution |
|---|---|
| ProcessInstance → EngineeringObjective was N:1 | **1:1 per Process Instance**; an objective may have history, but a Process Instance has one current objective at a time |
| `Decision` was used as an undefined generic entity | Replaced with **EngineeringDecision** except where `Decision State` is a logical state category |
| ExecutionTrace cardinality conflicted with the Operational Model | Canonical model uses **one ExecutionTrace per Process Instance**, containing ordered trace events; event-level traceability is represented by trace events |
| Condition was introduced as an entity without sufficient semantic basis | Retained as a **cross-layer semantic type**, not a new independent engineering entity |
| Observation/Input/Contribution/Validation/Mutation were treated as ordinary peer entities | Reclassified as **operational records/stages in the authority path**; they remain distinct but do not redefine the EPM entity inventory |
| StateMutation was treated as an independent engineering entity | Reclassified as an **authoritative state-change record** associated with Execution Context and traceability |
| ExecutionContext was represented too shallowly | Expanded into explicit Process, Engineering, Decision, Knowledge, and Continuity state references/collections |
| ProcessStateDefinition lacked required EPM/PEM semantics | Expanded to include purpose, inputs, activities, outputs, invariants, entry/progression/completion/exit conditions, gates, verification, and reconsideration |
| Transition and DecisionGate lacked sufficient basis/history | Added condition, gate, verification, decision, evaluation-history, and trace references |
| Operation list lacked semantic metadata | Operations now require subject, inputs, outputs, authority, mutation classification, preconditions, postconditions, and trace requirement |
| Controlled mutation existed only as an invariant | Explicit authority-path records are now required |
| Reconsideration was only a status | Reconsideration is now an explicit operational record/process preserving prior state and revised conclusions |

---

# 3. Matrix A — Entity Completeness

The canonical model MUST represent the Operational Model's primary entities and MUST NOT collapse distinct semantic concepts.

| Entity / Record | Classification | Authority | Required |
|---|---|---|---:|
| ProcessInstance | Primary operational entity | Operational | Yes |
| EngineeringObjective | Primary entity | EPM | Yes |
| ExecutionContext | Primary operational entity | Operational/PEM | Yes |
| ProcessState | Runtime/current-state record | EPM/PEM | Yes |
| ProcessStateDefinition | State definition | EPM/PEM | Yes |
| TransitionRule | Execution-control entity | EPM/PEM | Yes |
| Transition | Execution occurrence | PEM/Operational | Yes |
| DecisionGate | Progression-control entity | EPM/PEM | Yes |
| ProgressionCondition | Condition record | EPM | Yes |
| ExecutionMode | Operational entity | EPM/Operational | Yes |
| Requirement | Engineering knowledge entity | EPM | Yes |
| Constraint | Engineering knowledge entity | EPM | Yes |
| Investigation | Engineering activity/entity | EPM | Yes |
| Evidence | Engineering knowledge entity | EPM | Yes |
| Assumption | Engineering knowledge entity | EPM | Yes |
| Risk | Engineering knowledge entity | EPM | Yes |
| CandidateSolution | Engineering knowledge entity | EPM | Yes |
| Evaluation | Engineering knowledge entity | EPM | Yes |
| EngineeringDecision | Engineering conclusion | EPM | Yes |
| VerificationResult | Verification record | EPM/PEM | Yes |
| Artifact | Engineering output | EPM | Yes |
| ExecutionDetermination | Execution-control record | PEM | Yes |
| Plan | Execution-control entity | PEM | Yes |
| ExecutionAction | Execution occurrence | PEM | Yes |
| ExecutionResult | Execution result | PEM | Yes |
| ExecutionTrace | One trace for a Process Instance | PEM/Operational | Yes |
| Participant | Human/AI participant | Operational | Yes |
| ParticipantInput | Participant-originated input record | Operational | Yes |
| ParticipantContribution | Candidate/validated contribution record | Operational | Yes |
| Observation | Non-authoritative observation record | Operational | Yes |
| ValidationAssessment | Assessment record | Cross-layer | Yes |
| StateMutation | Authoritative state-change record | PEM/Operational | Yes |
| Reconsideration | Controlled reconsideration record/process | EPM/Operational | Yes |
| Condition | Cross-layer semantic type | EPM/PEM | Yes |

**Important:** `Condition`, `Observation`, `ParticipantInput`, `ParticipantContribution`, `ValidationAssessment`, and `StateMutation` are operationally necessary records/types but MUST NOT be allowed to replace or redefine the EPM's engineering entities.

---

# 4. Matrix B — Property Completeness

## 4.1 ProcessInstance

- identity
- EPM identity/version
- PEM identity/version
- current Engineering Objective
- Execution Mode
- engineering completion status
- Runtime lifecycle status
- Execution Context reference
- initialization information
- ExecutionTrace reference
- objective-change history

Engineering completion and Runtime termination MUST remain separate dimensions.

## 4.2 ExecutionContext

- identity
- Process Instance reference
- current Process State
- Execution Mode
- current Engineering Objective
- Requirements and resolution/satisfaction state
- Constraints
- Investigations and status
- Evidence and provenance/status
- Assumptions and status
- Risks and status
- Candidate Solutions and evaluation status
- Evaluations
- unresolved/contested/invalidated matters
- Artifacts
- accepted/pending/affected Engineering Decisions
- applicable Decision Gates and current evaluations
- Verification Results
- continuity state
- pending execution condition/activity
- current/pending Plan
- last authoritative update
- interruption/resumption information
- continuation information

## 4.3 ProcessStateDefinition

- identity/name
- purpose
- objective relationship
- applicable inputs
- permitted activities
- expected outputs
- invariants
- entry conditions
- progression conditions
- completion conditions
- exit conditions
- Decision Gates
- verification requirements
- reconsideration conditions
- valid Transition Rules

## 4.4 ProcessState

- identity
- definition reference
- entry-condition status
- current condition status
- progression-condition evaluations
- applicable gates and gate evaluations
- verification-condition evaluations
- reconsideration-condition status
- applicable Transition Rules

## 4.5 TransitionRule

- identity
- source state
- target state
- required conditions
- prohibited conditions
- required Decision Gates
- required verification
- reconsideration conditions

## 4.6 Transition

- identity
- source state
- target state
- Transition Rule reference
- condition evaluation
- gate evaluation
- verification basis
- Decision basis
- transition result/status
- trace reference

## 4.7 DecisionGate

- identity
- purpose
- applicable state/context
- conditions
- current evaluation status
- evaluation result
- evaluation history
- supporting Evidence
- supporting Engineering Decisions

## 4.8 Requirement

- identity
- statement
- source/context
- resolution state
- satisfaction state, when applicable
- supporting Evidence
- related Constraints
- related Evaluations
- related Engineering Decisions
- related Verification Results
- history

Resolution and satisfaction MUST remain distinct.

## 4.9 Investigation

- identity
- objective/purpose
- engineering question/uncertainty
- scope/context
- activities/evidence-gathering actions
- results/Evidence
- sufficiency assessment
- status
- closure basis

Investigation completion is objective/sufficiency-driven, not task-list-driven.

## 4.10 Evidence

- identity
- content/reference
- provenance
- source
- acquisition/context information
- relevance/reliability assessment where applicable
- status
- relationships to Investigations, Evaluations, Decisions, Verification Results, and conclusions

## 4.11 EngineeringDecision

- identity
- decision/conclusion
- rationale/basis
- status
- supporting Evidence
- relevant Requirements
- relevant Constraints
- relevant Risks
- relevant Candidate Solutions
- relevant Evaluations
- reconsideration status
- predecessor/supersession history

## 4.12 VerificationResult

- identity
- verification target
- criteria
- method/activity reference
- result
- status
- supporting Evidence
- effect on applicable conditions/gates

## 4.13 Plan

- identity
- purpose
- basis
- actions
- dependencies
- status
- execution conditions
- resulting Execution Results

## 4.14 ExecutionAction

- identity
- purpose
- authorization basis
- participant/actor reference
- preconditions
- action specification
- result reference
- trace reference

## 4.15 ExecutionResult

- identity
- action reference
- outputs
- status
- observed effects
- validation status
- trace reference

## 4.16 ExecutionDetermination

- identity
- execution determination
- basis
- status
- applicable authority/conditions
- trace reference

It MUST remain distinct from EngineeringDecision.

## 4.17 Participant / Input / Contribution

### Participant
- identity
- participant type: Human or AIAgent
- capabilities
- authority

### ParticipantInput
- identity
- participant reference
- content
- provenance/time/context

### ParticipantContribution
- identity
- participant reference
- contribution type
- content/reference
- validation status
- validation assessment reference

## 4.18 Observation

- identity
- source/observer
- observation content/reference
- context
- timestamp/order
- status
- resulting candidate contribution references

Observation MUST NOT directly mutate authoritative state.

## 4.19 ValidationAssessment

- identity
- subject/contribution reference(s)
- validation criteria
- evaluator/authority
- result/status
- supporting basis
- permitted mutation reference where applicable

## 4.20 StateMutation

- identity
- affected Process Instance/Execution Context
- source operation
- actor/authority
- prior state reference where required
- proposed/resulting state
- validation basis
- timestamp/order
- trace reference

## 4.21 Reconsideration

- identity
- trigger condition
- affected conclusions
- affected Requirements/Constraints/Risks/Solutions where applicable
- affected Process/Decision/Knowledge state
- evaluation process
- revised conclusions
- preserved historical state
- status
- trace

## 4.22 ExecutionTrace

One ExecutionTrace belongs to one Process Instance and contains ordered trace events.

The trace MUST support reconstruction of:

- material engineering changes
- Process State transitions
- Decision/Gate evaluations
- execution determinations
- plans/actions/results
- authoritative state mutations
- reconsideration and historical revisions
- participant contributions where material

---

# 5. Matrix C — Relationship Completeness

| Relationship | Cardinality | Status |
|---|---|---|
| ProcessInstance → EngineeringObjective | 1:1 current objective | Required |
| ProcessInstance → ExecutionContext | 1:1 | Required |
| ProcessInstance → ExecutionTrace | 1:1 | Required |
| ExecutionContext → ProcessState | N:1 current state | Required |
| ExecutionContext → EngineeringObjective | N:1 current objective | Required |
| ExecutionContext → Requirement | 1:N | Required |
| ExecutionContext → Constraint | 1:N | Required |
| ExecutionContext → Investigation | 1:N | Required |
| ExecutionContext → Evidence | 1:N | Required |
| ExecutionContext → Assumption | 1:N | Required |
| ExecutionContext → Risk | 1:N | Required |
| ExecutionContext → CandidateSolution | 1:N | Required |
| ExecutionContext → Evaluation | 1:N | Required |
| ExecutionContext → EngineeringDecision | 1:N | Required |
| ExecutionContext → VerificationResult | 1:N | Required |
| ExecutionContext → Artifact | 1:N | Required |
| ExecutionContext → DecisionGate | 1:N | Required |
| ExecutionContext → Plan | 1:N | Required |
| ProcessStateDefinition → TransitionRule | 1:N | Required |
| Transition → TransitionRule | N:1 | Required |
| Transition → Evidence | N:M | Applicable |
| Transition → DecisionGate | N:M | Applicable |
| Transition → VerificationResult | N:M | Applicable |
| Requirement → Evidence | N:M | Applicable |
| Requirement → Constraint | N:M | Applicable |
| Requirement → EngineeringDecision | N:M | Applicable |
| Requirement → VerificationResult | N:M | Applicable |
| Investigation → Evidence | 1:N | Required |
| Evidence → EngineeringDecision | N:M | Applicable |
| CandidateSolution → Evaluation | 1:N | Required |
| Evaluation → EngineeringDecision | N:M | Applicable |
| EngineeringDecision → EngineeringDecision | N:1 predecessor/supersession | Applicable |
| Reconsideration → EngineeringDecision | N:M | Required |
| Reconsideration → ExecutionContext | N:1 | Required |
| Reconsideration → Evidence | N:M | Applicable |
| Plan → ExecutionAction | 1:N | Required |
| ExecutionAction → ExecutionResult | 1:1 | Required |
| Participant → ParticipantInput | 1:N | Required |
| Participant → ParticipantContribution | 1:N | Required |
| ParticipantContribution → ValidationAssessment | N:M | Applicable |
| ValidationAssessment → StateMutation | 1:N | Applicable |
| StateMutation → ExecutionContext | N:1 | Required |
| StateMutation → ExecutionTrace | N:1 | Required |
| ExecutionAction → ExecutionTrace | N:1 | Required |
| Transition → ExecutionTrace | N:1 | Required |

**Cardinality rule:** `N:1` means many records may reference one authoritative/current object; it does not imply that the target is shared as an independent engineering fact across unrelated Process Instances.

---

# 6. Matrix D — State and Condition Semantics

## State categories

- Process State
- Engineering State
- Decision State
- Knowledge State
- Execution State
- Continuity State
- Artifact state
- lifecycle/completion state

## Condition categories

- Entry condition
- Progression condition
- Completion condition
- Exit condition
- Decision Gate condition
- Verification condition
- Execution precondition
- Execution postcondition
- Reconsideration condition
- Objective-change condition
- Mode-change condition

Every operational Condition representation MUST support:

- identity
- statement/expression
- subject/scope
- evaluation status
- evaluation result
- evaluation basis
- evaluation history where material

A condition MUST NOT be inferred solely from activity completion.

---

# 7. Matrix E — Operation Semantics

Operations are semantic operations, not API endpoints. Every operation definition MUST identify:

- operation identity
- operation class
- subject
- required inputs
- expected outputs
- authority layer
- observation/mutation classification
- preconditions
- postconditions
- trace requirement

| Class | Examples | Mutation classification |
|---|---|---|
| Observation | inspectExecutionContext, inspectProcessState, inspectEngineeringKnowledge, inspectConditions, observeEnvironment | Non-mutating |
| Evaluation | evaluateProcessState, evaluateTransitionRule, evaluateDecisionGate, evaluateProgressionCondition, evaluateVerificationResult, evaluateImpact | Non-mutating assessment unless explicitly coupled to a permitted record operation |
| Investigation | establishInvestigationObjective, performInvestigationActivity, recordInvestigationResult, evaluateInvestigationSufficiency, continueInvestigation, closeInvestigation | Controlled record mutation |
| Contribution | submitParticipantInput, submitObservation, submitEvidenceCandidate, submitAssumption, submitCandidateSolution, submitEvaluation, proposeEngineeringDecision, submitVerificationResult, submitArtifactResult | Candidate contribution; not automatically authoritative |
| Execution | establishExecutionDetermination, createPlan, updatePlan, authorizeExecutionAction, performExecutionAction, recordExecutionResult, updateExecutionContext, performTransition, recordTraceEvent | Controlled PEM-governed mutation |
| Reconsideration | identifyAffectedConclusions, initiateReconsideration, reviseEngineeringState, recordRevisedDecision, preserveHistoricalState | Controlled engineering-state mutation |

`evaluateX` MUST NOT silently mutate authoritative engineering state merely by producing an evaluation result.

---

# 8. Matrix F — Authority and Controlled Mutation

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

| Source | Observe | Propose | Direct authoritative mutation |
|---|---:|---:|---:|
| Human Participant | Yes | Yes | Only through defined authority path |
| AI Agent | Yes | Yes | No implicit authority |
| Tool | Yes | Yes | No implicit authority |
| Environment | Yes | No | No |
| Runtime | Yes | No independent engineering authority | Only PEM-controlled execution mutations |
| EPM | N/A | N/A | Defines engineering meaning/validity |
| PEM | N/A | N/A | Defines execution semantics/control |

Required distinctions:

```text
ParticipantInput ≠ ParticipantContribution
ParticipantContribution ≠ ValidationAssessment
ValidationAssessment ≠ StateMutation
EngineeringDecision ≠ ExecutionDetermination
Engineering Completion ≠ Runtime Termination
Observation ≠ Authoritative Knowledge
```

---

# 9. Matrix G — Traceability

The machine-readable model MUST support reconstruction of:

```text
User Request
  ↓
Engineering Objective / Requirement
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
Execution Trace
```

Material changes MUST be attributable, where applicable, to:

- Process Instance
- timestamp/order
- actor/participant
- source operation
- affected entity/state
- prior state
- resulting state
- supporting basis
- trace event

Reconsideration MUST preserve enough history to reconstruct the superseded state and the basis for the revision.

---

# 10. Reconciliation Rules

1. No Phase 2 primary engineering entity may disappear during serialization.
2. No EPM/PEM semantic distinction may be collapsed for implementation convenience.
3. `EngineeringDecision` is the canonical engineering conclusion entity; generic `Decision` is not a separate entity.
4. A Process Instance has one current Engineering Objective at a time; objective history is retained separately.
5. A Process Instance has one authoritative Execution Context and one logical Execution Trace; trace events provide event-level reconstruction.
6. `Condition` is a cross-layer semantic type, not a replacement for Process State or Decision Gate.
7. Observation, Participant Input, Participant Contribution, Validation Assessment, and State Mutation remain distinct operational records.
8. Authoritative state is distinguishable from candidate information.
9. Observation is non-mutating.
10. Engineering validity belongs to EPM; execution control belongs to PEM.
11. Engineering Completion and Runtime Termination remain separate state dimensions.
12. Engineering Decision and Execution Determination remain separate entities.
13. Requirement resolution and satisfaction remain separate properties.
14. Investigation sufficiency is objective-driven, not activity-list-driven.
15. Reconsideration preserves historical state.
16. Execution Context is sufficient to determine current execution state and resume without conversational memory.
17. JSON Schema validates structure; it does not replace EPM/PEM semantic rules.
18. Runtime, Agent, IDE, database, API, and tool-specific implementation details remain outside the canonical semantic model.

---

# 11. Matrix Review Result

| Matrix | Result | Notes |
|---|---|---|
| Entity Completeness | **PASS — reconciled** | Primary entities and operational records are distinguished |
| Property Completeness | **PASS — baseline** | Required Operational Model properties represented |
| Relationship Completeness | **PASS — baseline** | Cardinalities reconciled with one trace/context per Process Instance |
| State & Condition | **PASS — baseline** | State categories separated from condition evaluation |
| Operation Semantics | **PASS — baseline** | Operations now carry semantic metadata requirements |
| Authority & Mutation | **PASS — baseline** | Controlled mutation path explicitly represented |
| Traceability | **PASS — baseline** | Engineering/execution chain reconstructable in principle |

**Overall:** `RECONSTRUCTION MATRICES — READY FOR CANONICAL MODEL REGENERATION`

This does **not** mean Phase 3 is complete. It means the intermediate reconstruction stage has reached the threshold for rebuilding the canonical machine-readable model.

---

# 12. Next Derivation

The next artifacts SHALL be regenerated from these reconciled matrices:

1. canonical machine-readable model;
2. JSON Schema;
3. semantic validation rules / conformance checks.

No further conceptual expansion is required before that derivation unless regeneration exposes a direct contradiction with the Phase 2 Operational Model.
