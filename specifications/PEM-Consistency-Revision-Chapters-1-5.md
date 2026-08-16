# PEM Chapters 1-5 — Targeted Consistency Revision

This document records the normative amendments identified by the formal EPM/PEM consistency review. It is intended to be merged into the consolidated Process Execution Model.

## 1. Authority boundary

The Engineering Process Model (EPM) is authoritative for engineering meaning and validity. The Process Execution Model (PEM) is authoritative for execution semantics. A conforming Runtime shall satisfy both. The PEM defines how EPM-defined engineering conditions are executed and shall not redefine those conditions.

The Runtime is not an independent source of engineering authority.

## 2. Engineering Decision vs Execution Determination

The PEM shall use **Execution Determination** for a Runtime-level determination of the permissible or appropriate next execution action.

An **Engineering Decision** remains the EPM-defined accepted engineering conclusion or commitment. A Runtime selection of a next execution action is not an Engineering Decision unless the applicable EPM conditions explicitly establish that Decision.

The phrase **execution decision** shall not be used as a generic synonym for Execution Determination.

## 3. Process State

Process State semantics originate in the EPM. The PEM shall not maintain an independent or abbreviated state definition that changes their meaning.

A Runtime shall interpret each Process State according to the EPM Process State Schema, including applicable inputs, permitted activities, invariants, entry conditions, progression conditions, completion conditions, exit conditions, Decision Gates, verification requirements, and reconsideration conditions.

The PEM governs how the Runtime enters, operates within, verifies, progresses, suspends, resumes, and exits an EPM-defined Process State.

## 4. Execution Context

Execution Context is authoritative for the operational state of a Process Instance. It is not an independent source of engineering validity.

The current Execution Context shall remain consistent with applicable EPM-defined engineering conditions. If the Context and EPM appear inconsistent, the Runtime shall identify and resolve the inconsistency according to applicable rules rather than silently allowing Context to override EPM semantics.

The canonical term in Execution Context shall be **Engineering Objective**, not execution objective.

## 5. Progression

Execution progression shall occur only when the applicable EPM-defined progression conditions and PEM execution conditions are satisfied.

Where EPM conditions require Evidence, the Runtime shall ensure that sufficient applicable Evidence is established. Evidence is therefore a conditional progression requirement, not an unconditional requirement that every transition contain new Evidence.

A technically possible action is not necessarily a permissible action.

## 6. Decision Gates

The EPM defines the engineering validity criteria of a Decision Gate. The PEM defines when and how the Runtime evaluates and enforces that gate.

A Runtime shall not invent, weaken, or silently bypass an EPM-defined gate.

## 7. Verification

The EPM defines the engineering meaning and validity of Verification. The PEM defines how Verification participates in execution.

Verification may be performed by a Runtime, Participant, external system, or other permitted mechanism. The Runtime shall not assume that every verification requires new Evidence; it shall satisfy whatever Evidence and verification conditions the applicable EPM state or gate requires.

## 8. Completion vs termination

**Engineering Process Completion** is an EPM-defined engineering condition.

**Termination** is a PEM execution event.

A Runtime shall not declare engineering completion merely because no immediate action is available. A Process Instance may be suspended or otherwise terminated when PEM conditions permit this without satisfying Engineering Process Completion, but such termination shall not be represented as engineering completion.

## 9. Artifact authority

Artifact engineering semantics, material status, and validity originate in the EPM. The PEM defines how the Runtime creates, updates, verifies, persists, and carries Artifacts during execution.

## 10. Participant authority

Participant Input does not automatically constitute an Engineering Decision or authoritative state change.

The Runtime shall evaluate Participant authority, applicable EPM conditions, Process State, Decision Gates, and Execution Context before treating Participant Input as an authoritative engineering contribution.

Participant unavailability shall not be interpreted as approval or as satisfaction of an EPM-defined Requirement, Decision Gate, verification condition, or completion condition unless the applicable process explicitly defines such behavior.

Participant Input may change engineering state when accepted under applicable EPM conditions, but neither Participant Input nor Runtime interpretation may silently redefine the EPM.

## 11. Runtime heuristics

Runtime heuristics may select among execution actions that are permissible under the EPM and PEM. They shall not make an otherwise invalid engineering transition, Decision, gate outcome, verification result, or completion condition valid.

## 12. Cross-specification authority model

```text
EPM
  -> defines engineering meaning and validity

PEM
  -> defines execution semantics and control

Runtime
  -> implements PEM and has no independent engineering authority

Execution Context
  -> records authoritative operational state but cannot override EPM validity

Participants
  -> contribute according to applicable authority and process conditions
```

## 13. Cross-specification invariants

1. Runtime shall not redefine EPM engineering semantics.
2. Runtime shall execute according to PEM semantics.
3. Execution Context shall remain consistent with applicable EPM conditions.
4. Engineering Decisions shall remain distinct from Execution Determinations.
5. Process State semantics originate in EPM; PEM governs their execution.
6. EPM Decision Gates shall not be weakened or bypassed by Runtime heuristics.
7. Progression requires applicable EPM and PEM conditions to be satisfied.
8. Engineering Process Completion remains distinct from Runtime termination.
9. Artifact engineering validity is determined by EPM semantics; Runtime determines execution handling.
10. Participant contribution does not automatically constitute an authoritative engineering state change.
11. Engineering Decision and Execution Determination shall not be used interchangeably.
12. These semantics remain implementation-independent.

## 14. Integration status

These amendments resolve the targeted consistency findings from the formal EPM/PEM review. They are to be merged into the consolidated PEM Chapters 1–5, followed by a final cross-specification verification pass.