# AESM Implementation Foundations

## Identity

Task ID:
aesm-implementation-foundations

Status:
complete

Completed:
2026-09-19 (per IMPLEMENTATION_PLAN.md history; exact dates approximate)

Source:
IMPLEMENTATION_PLAN.md — "Completed Foundations" section

Concern tags:
foundation, process-instance, execution-context, runtime-core, recording

---

## Objective

Establish the minimal, executable AESM implementation: Process Instance identity
and persistence, authoritative Execution Context, first vertical slice semantics,
minimal Runtime core, and validated recording behavior.

---

## Context

This was the first engineering work that turned the agreed AESM conceptual model
into a practical, executable implementation. Prior to this work, AESM existed
only as conceptual documentation in docs/. This effort produced the Runtime,
bridge, and test infrastructure that all subsequent work depends on.

---

## Governing Constraints

The following constraints were established and remain in effect:

1. docs/ is the canonical AESM knowledge surface. Do not replace it with
   implementation records.
2. The objective is to operationalize the existing AESM model, not to continue
   conceptual expansion.
3. Runtime authority over lifecycle and completion semantics must be preserved.
4. No further recording or persistence-semantic change is authorized by the
   recording behavioral validation evidence.

---

## Dependencies

- Canonical docs/ set (EPM, PEM, Process Instance, Execution Context semantics)

---

## Decisions Still in Effect

1. **Process Instance is the continuity boundary.** Conversation history is not
   authoritative Process Instance state. A fresh Agent must recover the existing
   PI rather than creating a replacement because the session changed.

2. **Runtime authority.** Runtime governs authoritative process execution and
   state mutation. Agents perform engineering work but are not authoritative
   over persisted AESM state.

3. **Separate guidance from enforcement.** Guidance can influence Agent behavior;
   Runtime state and constraints provide authoritative control where required.

4. **Require implementation evidence before semantic change.** Do not change
   AESM semantics based on speculation or a single implementation inconvenience.

5. **Keep the implementation minimal.** Add infrastructure only when demonstrated
   by the prototype. No speculative EPM/PEM/AESM expansion.

6. **Recording behavioral validation closes the recording contract.** No further
   recording or persistence-semantic change is authorized by this evidence.
   This decision requires a new explicit authorization to reopen.

---

## Work Units

### Baseline and Scope Control

Status: complete

Established docs/ as canonical AESM knowledge surface, the implementation plan
as controlled work record, and the objective of operationalizing the existing
model rather than continuing conceptual expansion.

### Process Instance Persistence

Status: complete

Defined minimal Process Instance representation. Implemented creation, stable
identity, filesystem persistence. Demonstrated continuity without conversation
history.

### Authoritative Execution Context

Status: complete

Defined minimal authoritative Execution Context. Implemented creation, loading,
mutation, persistence, and continuation information. Demonstrated recovery from
persisted Context after loss of original Agent context.

### First Vertical Slice Semantics

Status: complete

Defined a bounded engineering request and its objective/scope. Bound applicable
EPM semantics. Derived required process states and valid transitions. Defined
engineering completion separately from Runtime/session termination. Derived
minimum Runtime responsibilities.

### Minimal Runtime Core

Status: complete

Implemented: Process Instance creation/loading, Execution Context loading/saving,
process-state/lifecycle operations, evidence recording, decision recording,
artifact recording, verification recording, completion/termination handling,
Runtime authority preservation.

### Recording Behavioral Validation

Status: complete

Validated decision, artifact, and verification recording; guards and
persistence/history behavior; failure-path consistency. Corrected caller-level
rollback defect following existing observe() rollback precedent.

---

## Acceptance Criteria

All satisfied:
- Process Instance creation, identity, persistence, and recovery demonstrated.
- Execution Context creation, loading, mutation, persistence demonstrated.
- First vertical slice semantics derived and implemented.
- Minimal Runtime core implemented.
- Recording behavioral validation: 53/53 recording tests, 88/88 full suite.

---

## Verification Requirements

Satisfied: executable test suite passing at closure.

---

## Evidence Record

- `tests/lifecycle/test_completion_termination.py` — lifecycle/completion evidence
- 53/53 recording tests passing at closure
- 88/88 full suite passing at closure
- Implementation: `runtime/`, `bridge/`, `tests/`
