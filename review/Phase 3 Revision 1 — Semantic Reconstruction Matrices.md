# Phase 3 Revision 1 — Semantic Reconstruction Matrices

**Project:** AI-Assisted Engineering System Model (AESM)  
**Phase:** Phase 3 Revision 1  
**Status:** Working Reconstruction Baseline  
**Version:** 0.1.0  
**Source authority:** Phase 2 AESM Operational Model, EPM, PEM

---

## 1. Purpose

This document defines the intermediate semantic reconstruction matrices used to rebuild the AESM machine-readable model directly from the Phase 2 Operational Model.

It is intentionally an intermediate artifact. It is not a Runtime schema and does not define an Agent protocol.

The reconstruction rule is:

```text
EPM / PEM semantic authority
        ↓
AESM Operational Model
        ↓
Semantic inventory
        ↓
Reconstruction matrices
        ↓
Canonical machine-readable model
        ↓
Derived implementation schemas
```

The matrices exist to prevent semantic loss during serialization.

---

# 2. Matrix A — Entity Completeness

The canonical model MUST represent the following operational concepts without collapsing distinct concepts.

| Entity / Concept | Layer | Required | Primary role | Status |
|---|---|---:|---|---|
| ProcessInstance | Operational | Yes | One execution of an EPM | Required |
| ExecutionContext | Operational | Yes | Authoritative continuation state | Required |
| EngineeringObjective | EPM/Operational | Yes | Purpose of engineering process | Required |
| ProcessState | EPM/PEM | Yes | Current execution state | Required |
| ProcessStateDefinition | EPM/PEM | Yes | Semantic definition of state | Required |
| TransitionRule | EPM/PEM | Yes | Conditions governing progression | Required |
| Transition | PEM/Operational | Yes | Recorded state change | Required |
| DecisionGate | EPM/PEM | Yes | Condition controlling progression | Required |
| ProgressionCondition | EPM | Yes | Condition for progression | Required |
| ExecutionMode | Operational | Yes | Execution configuration | Required |
| Requirement | EPM | Yes | Engineering requirement | Required |
| Constraint | EPM | Yes | Engineering constraint | Required |
| Investigation | EPM | Yes | Evidence-gathering process | Required |
| Evidence | EPM | Yes | Support for engineering knowledge | Required |
| Assumption | EPM | Yes | Explicit uncertain proposition | Required |
| Risk | EPM | Yes | Potential adverse outcome | Required |
| CandidateSolution | EPM | Yes | Candidate engineering solution | Required |
| Evaluation | EPM | Yes | Assessment of an engineering subject | Required |
| EngineeringDecision | EPM | Yes | Authoritative engineering conclusion | Required |
| VerificationResult | EPM | Yes | Verification outcome | Required |
| Artifact | EPM/Operational | Yes | Engineering output/representation | Required |
| Plan | PEM | Yes | Planned execution | Required |
| ExecutionDetermination | PEM | Yes | Execution-specific determination | Required |
| ExecutionAction | PEM | Yes | Authorized execution activity | Required |
| ExecutionResult | PEM | Yes | Result of execution action | Required |
| Participant | Operational | Yes | Human/AI participant | Required |
| ParticipantInput | Operational | Yes | Input submitted by participant | Required |
| ParticipantContribution | Operational | Yes | Validated/contributory input | Required |
| ExecutionTrace | Operational | Yes | Reconstruction of execution | Required |
| Condition | Cross-layer | Yes | Explicit evaluable condition | Required |
| Observation | Operational | Yes | Non-authoritative observation | Required |
| Reconsideration | EPM/Operational | Yes | Controlled revision process | Required |
| ValidationAssessment | Cross-layer | Yes | Assessment preceding authoritative mutation | Required |
| StateMutation | Operational | Yes | Authoritative state change | Required |

### Rule

`Observation`, `ParticipantInput`, `ParticipantContribution`, `ValidationAssessment`, and `StateMutation` MUST remain distinguishable. They represent different stages of the authority path.

---

# 3. Matrix B — Property Completeness

## 3.1 ProcessInstance

Required semantic properties:

- identity
- EPM reference and version
- PEM reference and version
- Engineering Objective reference
- Execution Mode reference
- engineering lifecycle status
- Runtime lifecycle status
- Execution Context reference
- initialization information
- execution history reference

## 3.2 ExecutionContext

Required semantic properties:

- identity
- Process Instance reference
- current Process State
- Execution Mode
- current Engineering Objective
- Requirement state
- Constraint state
- Investigation state
- Evidence state
- Assumption state
- Risk state
- Candidate Solution state
- Evaluation state
- unresolved/contested matters
- Artifact state
- Decision state
- Decision Gate state
- knowledge state
- continuity state
- pending execution condition
- current/pending Plan
- last authoritative update
- interruption/resumption information
- continuation information

## 3.3 ProcessStateDefinition

Required semantic properties:

- identity
- name
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

## 3.4 TransitionRule

Required semantic properties:

- identity
- source state
- target state
- required conditions
- prohibited conditions
- required Decision Gates
- required verification
- reconsideration conditions

## 3.5 Transition

Required semantic properties:

- identity
- source state
- target state
- Transition Rule
- condition evaluation
- gate evaluation
- verification basis
- Decision basis
- transition result/status
- trace reference

## 3.6 DecisionGate

Required semantic properties:

- identity
- purpose
- conditions
- evaluation history
- current evaluation status
- supporting Evidence
- supporting Decisions
- result

## 3.7 EngineeringDecision

Required semantic properties:

- identity
- decision statement
- rationale
- supporting Evidence
- relevant Requirements
- relevant Constraints
- relevant Evaluations
- status
- supersession/reconsideration relationship
- historical predecessor where applicable

## 3.8 Requirement

Required semantic properties:

- identity
- statement
- source/context
- resolution state
- satisfaction state
- supporting Evidence
- related Decisions
- related Verification Results

## 3.9 Investigation

Required semantic properties:

- identity
- objective
- engineering question
- scope
- activities
- Evidence/results
- sufficiency assessment
- status
- closure basis

## 3.10 Evidence

Required semantic properties:

- identity
- content/reference
- provenance
- source
- acquisition context
- reliability/relevance assessment where applicable
- status
- relationships to conclusions

## 3.11 Plan

Required semantic properties:

- identity
- purpose
- basis
- actions
- dependencies
- status
- execution conditions
- resulting Execution Results

## 3.12 ExecutionAction

Required semantic properties:

- identity
- purpose
- authorization basis
- participant/actor
- preconditions
- action specification
- result reference
- trace reference

## 3.13 ExecutionResult

Required semantic properties:

- identity
- action reference
- outputs
- status
- observed effects
- validation status
- trace reference

## 3.14 Reconsideration

Required semantic properties:

- identity
- triggering condition
- affected conclusions
- affected state
- affected Requirements
- affected Decisions
- evaluation process
- revised conclusions
- preserved historical state
- status

---

# 4. Matrix C — Relationship Completeness

| Relationship | Cardinality | Purpose |
|---|---|---|
| ProcessInstance → ExecutionContext | 1:1 | Authoritative continuation state |
| ProcessInstance → EngineeringObjective | N:1 | Objective identity |
| ProcessInstance → ExecutionTrace | 1:N | Execution reconstruction |
| ExecutionContext → ProcessState | N:1 | Current state |
| ExecutionContext → EngineeringObjective | N:1 | Current objective |
| ExecutionContext → Requirement | 1:N | Requirement state |
| ExecutionContext → Decision | 1:N | Decision state |
| ExecutionContext → Plan | 1:N | Current/pending plan |
| ProcessStateDefinition → TransitionRule | 1:N | Valid progression paths |
| Transition → TransitionRule | N:1 | Rule used |
| Transition → Evidence | N:M | Evidence supporting transition |
| Transition → DecisionGate | N:M | Gate evaluation |
| Transition → VerificationResult | N:M | Verification basis |
| Requirement → Evidence | N:M | Requirement support |
| Requirement → EngineeringDecision | N:M | Decision relationship |
| Requirement → VerificationResult | N:M | Satisfaction verification |
| Investigation → Evidence | 1:N | Investigation results |
| Evidence → EngineeringDecision | N:M | Decision support |
| CandidateSolution → Evaluation | 1:N | Solution assessment |
| Evaluation → EngineeringDecision | N:M | Decision basis |
| EngineeringDecision → EngineeringDecision | N:1 | Supersession/reconsideration history |
| Plan → ExecutionAction | 1:N | Planned execution |
| ExecutionAction → ExecutionResult | 1:1 | Action outcome |
| Participant → ParticipantInput | 1:N | Submitted inputs |
| Participant → ParticipantContribution | 1:N | Contributions |
| ParticipantContribution → ValidationAssessment | 1:N | Contribution validation |
| ValidationAssessment → StateMutation | 1:N | Authorized mutation basis |
| StateMutation → ExecutionContext | N:1 | Authoritative update |
| ExecutionTrace → StateMutation | 1:N | Mutation trace |
| ExecutionTrace → ExecutionAction | 1:N | Action trace |
| Reconsideration → EngineeringDecision | N:M | Affected/revised decisions |
| Reconsideration → Evidence | N:M | Reconsideration evidence |
| Reconsideration → ExecutionContext | N:1 | State being reconsidered |

---

# 5. Matrix D — State and Condition Semantics

AESM MUST distinguish state from conditions used to evaluate progression.

### State categories

- Engineering state
- Process state
- Execution state
- Knowledge state
- Decision state
- Continuity state
- Artifact state

### Condition categories

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

A condition MUST have:

- identity;
- statement/expression;
- subject or scope;
- evaluation status;
- evaluation result;
- evaluation basis;
- evaluation history where material.

A condition MUST NOT be inferred solely from an activity having been performed.

---

# 6. Matrix E — Operation Semantics

Operations are semantic operation classes, not API endpoints.

Each operation definition MUST be able to identify:

- operation identity;
- operation class;
- subject entity;
- required inputs;
- expected outputs;
- authority layer;
- whether the operation observes or mutates authoritative state;
- preconditions;
- postconditions;
- trace requirement.

## Operation classes

### Observation

Examples:

- inspectExecutionContext
- inspectProcessState
- inspectEngineeringKnowledge
- inspectConditions
- observeEnvironment

Mutation: **No**

### Evaluation

Examples:

- evaluateProcessState
- evaluateTransitionRule
- evaluateDecisionGate
- evaluateProgressionCondition
- evaluateVerificationResult
- evaluateImpact

Mutation: **normally no direct authoritative mutation**

### Investigation

Examples:

- establishInvestigationObjective
- performInvestigationActivity
- recordInvestigationResult
- evaluateInvestigationSufficiency
- continueInvestigation
- closeInvestigation

Mutation: **controlled**, subject to validation and authority rules

### Contribution

Examples:

- submitParticipantInput
- submitObservation
- submitEvidenceCandidate
- submitAssumption
- submitCandidateSolution
- submitEvaluation
- proposeEngineeringDecision
- submitVerificationResult
- submitArtifactResult

Mutation: **candidate contribution only** unless separately validated and authorized

### Execution

Examples:

- establishExecutionDetermination
- createPlan
- updatePlan
- authorizeExecutionAction
- performExecutionAction
- recordExecutionResult
- updateExecutionContext
- performTransition
- recordTraceEvent

Mutation: **controlled authoritative execution mutation**

### Reconsideration

Examples:

- identifyAffectedConclusions
- initiateReconsideration
- reviseEngineeringState
- recordRevisedDecision
- preserveHistoricalState

Mutation: **controlled authoritative engineering mutation**

---

# 7. Matrix F — Authority and Mutation

The authority path is normative:

```text
External / participant / Agent / tool / environment output
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

| Source | May observe | May propose | May directly establish authoritative state |
|---|---:|---:|---:|
| Human Participant | Yes | Yes | Only through defined authority path |
| AI Agent | Yes | Yes | No implicit authority |
| Tool | Yes | Yes | No implicit authority |
| Environment | Yes | No | No |
| Runtime | Yes | No independent engineering authority | Only according to PEM-controlled execution semantics |
| EPM | N/A | N/A | Owns engineering semantics |
| PEM | N/A | N/A | Owns execution semantics |

### Required distinctions

```text
ParticipantInput
≠ ParticipantContribution

ParticipantContribution
≠ ValidationAssessment

ValidationAssessment
≠ StateMutation

EngineeringDecision
≠ ExecutionDetermination

EngineeringCompletion
≠ RuntimeTermination
```

---

# 8. Matrix G — Traceability

The machine-readable model MUST support reconstruction of the engineering chain:

```text
User Request
    ↓
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
Plan / Execution Determination
    ↓
Execution Action
    ↓
Execution Result
    ↓
Authoritative State Update
    ↓
Trace
```

At minimum, material changes MUST be attributable to:

- process instance;
- timestamp/ordering information;
- actor/participant where relevant;
- source operation;
- affected entity;
- prior state where required;
- resulting state;
- supporting basis;
- trace event.

Historical state MUST remain reconstructable when reconsideration changes a conclusion.

---

# 9. Reconstruction Rules

The revised canonical model MUST satisfy these rules:

1. No Phase 2 core entity may disappear during serialization.
2. No Phase 2 semantic distinction may be collapsed for convenience.
3. Required operational relationships MUST be explicit.
4. Authoritative state MUST be distinguishable from candidate information.
5. Observation MUST remain non-mutating.
6. Operations MUST have semantic meaning without becoming API definitions.
7. EPM authority and PEM authority MUST remain distinct.
8. Engineering Completion and Runtime Termination MUST remain distinct.
9. Engineering Decision and Execution Determination MUST remain distinct.
10. Requirement resolution and satisfaction MUST remain distinct.
11. Reconsideration MUST preserve historical state.
12. Execution Context MUST contain enough authoritative state to support continuation.
13. Traceability MUST be reconstructable.
14. JSON Schema MUST remain structural validation, not a substitute for EPM/PEM semantics.
15. Runtime implementation details MUST remain outside the canonical model.

---

# 10. Exit Criteria for Reconstruction

The reconstruction stage is complete only when:

- Entity Completeness = Pass
- Property Completeness = Pass
- Relationship Completeness = Pass
- State/Condition Completeness = Pass
- Operation Semantics = Pass
- Authority/Mutation = Pass
- Traceability = Pass

Only then should the revised JSON Schema and canonical JSON model be generated.
