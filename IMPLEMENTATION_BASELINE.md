# AESM Implementation Baseline

## Baseline Purpose

This document records the repository and implementation baseline established before continuing implementation of `IMPLEMENTATION_PLAN.md`.

It is an implementation record, not a new AESM semantic specification.

## Baseline Reference

- Repository: `tuanna2703/AI-Assisted-Engineering-System-Model`
- Branch: `main`
- Baseline commit: `055ed3db22066a991ee32c9c18d1518687e78e2b`
- Baseline commit message: `Add controlled AESM implementation plan with progress tracking and change-control rules`
- Baseline date: 2026-08-27
- Implementation plan: `IMPLEMENTATION_PLAN.md`

The baseline commit is the exact repository state against which the initial implementation inventory was performed.

## Repository Inventory

The repository currently contains these top-level implementation surfaces:

- `docs/` — unified AESM documentation set.
- `implementation/` — execution-generated implementation decisions, findings, and evidence.
- `runtime/` — existing first Runtime implementation experiment.
- `tests/` — existing automated continuity/recovery tests.
- `README.md` — repository-level orientation.
- `IMPLEMENTATION_PLAN.md` — controlled implementation checklist.
- `IMPLEMENTATION_BASELINE.md` — this implementation baseline record.

No `schemas/`, `scripts/`, or `model/` directories are present in the baseline repository.

## Documentation Surface

The unified documentation set contains the current AESM knowledge surface, including the system model, engineering model, execution model, Process Instance and Execution Context, participant/Agent participation, Runtime/conformance, continuity/traceability/reconsideration, operational guidance, reference material, source mapping, Agent guidance, and Runtime implementer guidance.

The documentation source map explicitly states that the unified set is the current destination of the former conceptual sources and that implementation-specific details remain non-normative unless required by AESM semantics.

`docs/` is reserved for descriptive AESM knowledge. Execution-generated implementation decisions, findings, and evidence are kept outside `docs/` so they cannot be mistaken for part of the descriptive AESM model.

## Existing Implementation Inventory

### `runtime/`

**Classification: ADAPT**

The Runtime is directly relevant to the implementation objective and is therefore retained as the starting implementation surface. It is not accepted as complete or semantically authoritative merely because it already exists.

Current components:

- `runtime/core/models.py` — representations of `ProcessInstance` and `ExecutionContext`.
- `runtime/core/store.py` — Process Instance and authoritative Context persistence boundary.
- `runtime/core/runtime.py` — small Runtime control surface for process creation/loading, evidence observation, decision recognition, pending execution, verification, completion recognition, and attachment/replacement.
- `runtime/persistence/json_store.py` — durable JSON and JSONL persistence primitives.

The existing Runtime README describes this as a first implementation experiment and explicitly identifies Agent/MRAP and workspace/tool adapters as not yet implemented.

### `tests/`

**Classification: ADAPT**

The existing continuity test is valuable implementation evidence and should be retained, but it must be expanded or adjusted as the implementation proceeds.

The current test suite verifies Runtime replacement/recovery, explicit decision recognition, explicit completion recognition, failure when authoritative Context is missing, and preservation of execution history.

### `docs/`

**Classification: KEEP**

The unified documentation set is retained as the conceptual authority. Implementation work must not silently redefine it.

### `implementation/`

**Classification: CREATE / KEEP**

This is the execution-generated implementation record surface. It contains implementation decisions, findings, and evidence that arise while carrying out the controlled implementation plan. These materials support implementation and traceability but are not part of the descriptive AESM documentation set unless a separately approved change promotes a finding into the AESM model.

### `README.md`

**Classification: KEEP**

Retained as repository-level orientation; update only if implementation changes make its current description inaccurate.

### `schemas/`, `scripts/`, `model/`

**Classification: ABSENT / no action**

These directories are not present in the baseline repository. No obsolete implementation components from these directories need to be removed or isolated at this point.

## Initial Implementation Boundary

For the prototype, the minimum repository boundary is:

```text
IMPLEMENTATION_PLAN.md
IMPLEMENTATION_BASELINE.md
docs/
implementation/
runtime/
tests/
README.md
```

The existing Runtime and tests are experimental implementation assets. They must be validated and adapted against the current documentation before being treated as the foundation for subsequent work.

No new dedicated IDE extension, graphical application, workflow designer, multi-agent subsystem, distributed infrastructure, enterprise security layer, DSL, or generalized enforcement framework is part of this boundary.

## Implementation Assumptions

The following assumptions are being made for implementation purposes because they are not fully specified as concrete implementation choices by the conceptual documentation:

1. The first executable Runtime experiment may use a local filesystem-backed store so persistence and recovery can be demonstrated without introducing production infrastructure.
2. JSON is an acceptable prototype serialization format for authoritative Process Instance and Execution Context state, provided the representation remains an implementation detail rather than an AESM semantic requirement.
3. JSONL is an acceptable prototype format for append-only execution history, subject to later validation against the required continuity and traceability behavior.
4. Python is the implementation language of the existing prototype and may remain the language for the first vertical slice; this does not make Python an AESM requirement.
5. Pytest is the current test runner used by the existing prototype and may be used for implementation verification; this does not make Pytest an AESM requirement.
6. The first real Execution Environment experiment may use an existing IDE/CLI environment with an AI Agent, while AESM semantics remain independent of that environment.

These are implementation assumptions only. They must not be promoted into AESM semantics without explicit evidence and approval.

## Inventory Findings

1. The repository is no longer an empty implementation starting point. A partial Runtime and continuity test foundation already exists.
2. The existing Runtime already covers part of the Process Instance, Execution Context, persistence, recognition, and recovery concerns described by the implementation plan.
3. Agent guidance and environment mechanism integration are not yet implemented in the repository.
4. The existing implementation therefore needs to be evaluated and adapted rather than discarded and rebuilt from zero.
5. The implementation record should remain outside `docs/` so execution-generated decisions and findings are not confused with descriptive AESM knowledge.
6. The next implementation work should proceed from the existing Runtime/persistence foundation, but only after validating the exact behavior required for the first Process Instance persistence and Execution Context tasks.

## Exit Assessment

The repository and implementation inventory is complete for the current baseline.

The implementation team can now distinguish:

- conceptual authority: `docs/`;
- controlled implementation plan: `IMPLEMENTATION_PLAN.md`;
- execution-generated implementation record: `implementation/`;
- experimental implementation: `runtime/`;
- implementation evidence: `tests/`;
- baseline assumptions: this document.
