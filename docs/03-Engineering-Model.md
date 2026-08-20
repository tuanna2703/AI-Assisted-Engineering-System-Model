# AESM Engineering Model

## Purpose

The Engineering Process Model (EPM) defines **what engineering work is** and the conditions under which engineering progress is valid.

EPM is independent of Runtime technology, Agents, IDEs, programming languages, storage systems, and other implementation choices.

## Engineering objective

Engineering execution begins from an objective that gives the Process Instance its intended purpose. The objective must remain explicit and traceable. It is not silently changed by an Agent or Runtime.

## Core engineering concepts

The engineering model includes, as applicable:

- Requirements
- Constraints
- Investigation
- Evidence
- Assumptions
- Risks
- Candidate Solutions
- Evaluation
- Engineering Decisions
- Implementation
- Artifacts
- Verification
- Process States
- Decision Gates
- Progress
- Reconsideration
- Completion

## Requirements

Requirements express what the engineering result must satisfy. They may be clarified, challenged, refined, or changed as evidence develops, but material changes remain explicit and traceable.

Requirement interpretation and satisfaction are distinct concepts. A requirement can be understood without yet being satisfied, and proposed satisfaction must be supported by applicable evidence and verification.

## Constraints

Constraints limit permissible engineering choices or execution. They may arise from technical, operational, organizational, environmental, compatibility, or other applicable conditions.

A Participant or Runtime must not silently override a constraint merely because an alternative action is technically possible.

## Investigation

Investigation is objective-driven. Its purpose is to gather sufficient evidence to support confident engineering decisions or conclusions.

Investigation is not defined by a fixed universal checklist. The required investigation depends on the uncertainty, objective, constraints, and evidence needed for the current engineering situation.

## Evidence

Evidence is information used to support engineering conclusions and Decisions. Evidence may originate from documentation, source code, experiments, measurements, stakeholders, operational systems, or other appropriate sources.

Evidence must remain distinguishable from assumptions and unsupported claims.

## Assumptions

An Assumption is a proposition accepted without sufficient Evidence. Material assumptions should be explicitly identified and, where practical, replaced or validated through investigation.

## Candidate Solutions

Candidate Solutions are possible approaches to an engineering problem. They can be generated, compared, evaluated, challenged, and revised.

A candidate is not an Engineering Decision merely because an Agent or Participant proposes it.

## Engineering Decisions

An Engineering Decision is an accepted engineering conclusion or commitment that affects engineering direction or outcome.

Decisions should remain traceable to the Evidence, Requirements, Constraints, evaluation, and other reasoning that support them.

Engineering Decision is distinct from **Execution Determination**. The former concerns engineering meaning; the latter concerns what execution may or should do next under PEM.

## Artifacts

Artifacts are persistent representations of engineering knowledge produced or consumed during execution. Examples include source code, designs, specifications, tests, configuration, reports, and other engineering outputs.

Artifact existence alone does not establish engineering validity.

## Verification

Verification evaluates whether an Artifact, Decision, result, or Process State satisfies applicable requirements and conditions.

Verification produces Evidence for progression decisions. Failed verification may require additional investigation, revision, reconsideration, or return to an earlier engineering concern.

## Process States

A Process State represents the current stage of engineering work within a Process Instance.

A state is defined by its engineering objective, permitted activities, expected outputs, completion conditions, and applicable transition constraints.

EPM defines the engineering meaning and validity of states. PEM governs how those states are executed.

## Decision Gates

Decision Gates are explicit conditions that govern whether progression is permitted. A gate may require particular evidence, verification, decisions, approvals, or other conditions.

A gate must not be bypassed or treated as satisfied merely because a Participant or Runtime wants execution to continue.

## Progress

Engineering progress is not equivalent to elapsed time, number of actions, number of Agent responses, or amount of generated content.

Progress is established through the applicable engineering conditions, including required outputs, evidence, decisions, verification, and state progression.

## Reconsideration

AESM supports controlled reconsideration. New Evidence, failed verification, changed constraints, discovered errors, or other material information may justify revisiting earlier Requirements, Solutions, Decisions, or implementation choices.

Reconsideration changes current engineering state without erasing the historical fact that earlier conclusions existed.

## Completion

Engineering completion is an engineering determination under EPM. It is distinct from Runtime termination and from the technical stopping of an Agent session.

## Engineering flow

A useful conceptual view is:

```text
Objective
   ↓
Requirements / Constraints
   ↓
Investigation
   ↓
Evidence
   ↓
Candidate Solutions
   ↓
Evaluation
   ↓
Engineering Decision
   ↓
Implementation / Artifacts
   ↓
Verification
   ↓
Progress evaluation
   ├── continue
   ├── reconsider
   ├── block
   └── complete
```

The flow is iterative rather than waterfall.