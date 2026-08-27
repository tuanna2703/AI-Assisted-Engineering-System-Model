# Execution Context Implementation Representation

## Purpose

This document records the implementation decision for representing the authoritative AESM Execution Context in the initial prototype. It translates existing AESM semantics into the smallest implementation contract required for continuation, without introducing new AESM concepts.

## Semantic Baseline

The Execution Context is the authoritative operational state required to continue a Process Instance consistently at a specific point in time. It is persistent, recoverable, portable, and sufficient for continuation. It is semantically distinct from Process Instance identity, Runtime state, Agent state, conversation history, and Execution Environment state.

The canonical documentation describes Context information in these existing categories:

- process status;
- engineering state;
- decision state;
- knowledge state;
- continuity state;
- material historical and traceability state.

The Process Instance remains the continuity boundary. Its persistent representation supplies stable identity and applicable EPM binding; the Context supplies the current authoritative operational situation.

## Minimal Required Representation

The minimum Context must make the following recoverable without the previous Agent conversation:

| Information | Existing representation | Required role |
|---|---|---|
| Process Instance reference | `process_instance_id` | Identifies which engineering execution this Context belongs to. |
| Engineering objective | `engineering_objective` | Establishes the objective governing the current execution. |
| Current process situation | `process_state`, `execution_mode`, `engineering_completion` | Establishes current authoritative execution/completion status. |
| Engineering state | `requirements`, `constraints`, `artifacts`, `verification` | Preserves material engineering state needed for continuation. |
| Decision state | `engineering_decisions`, `decision_gates` | Preserves recognized engineering conclusions and applicable gate state. |
| Knowledge state | `evidence`, `assumptions`, `risks`, `unresolved_matters` | Preserves recognized knowledge and explicit uncertainty/unresolved matters. |
| Continuation state | `pending_execution`, `execution_determination`, `failure_uncertainty` | Preserves unfinished work, execution-level determination, and material blocking/failure/uncertainty information. |
| Authoritative-state metadata | `version`, `updated_at` | Supports persistence and recovery of the authoritative representation; these are implementation metadata, not new AESM semantic concepts. |

No additional top-level Context field is required by the current canonical semantics at this point.

## Continuation Contract

The existing `pending_execution` representation is the designated implementation location for unfinished execution and continuation information. It must be capable of making the following recoverable:

1. the unfinished activity;
2. its current status;
3. the next expected action;
4. any conditions that must be satisfied before resumption.

This does not introduce a workflow engine or a new lifecycle concept. These are the existing continuity semantics already described by AESM.

`unresolved_matters` remains the representation of unresolved questions or matters. `failure_uncertainty` remains the representation of material failure, contradiction, missing information, blocked conditions, and uncertainty. `execution_determination` remains distinct from Engineering Decisions and records execution-level determination where one exists.

The Context must not depend on Agent/session metadata, conversation memory, Runtime process identity, IDE state, or Execution Environment state for continuation.

## Field Classification

### KEEP

The existing fields are retained because each represents information covered by current AESM semantics or necessary to preserve the authoritative representation:

`process_instance_id`, `engineering_objective`, `process_state`, `execution_mode`, `requirements`, `constraints`, `evidence`, `assumptions`, `risks`, `candidate_solutions`, `engineering_decisions`, `decision_gates`, `artifacts`, `verification`, `unresolved_matters`, `pending_execution`, `execution_determination`, `failure_uncertainty`, `engineering_completion`, `version`, and `updated_at`.

### ADAPT

`pending_execution` requires an explicit continuation contract. Its entries must carry enough information to reconstruct unfinished work and the expected resumption point. The existing field is retained; no separate generalized task/workflow model is introduced.

### REMOVE

None. No existing field has been shown to violate current AESM semantics.

### CREATE

No new top-level Context field is required by this definition.

## Process Instance Boundary

The Context must not duplicate Process Instance identity semantics beyond the stable `process_instance_id` reference. Applicable EPM binding remains part of the Process Instance representation and is recovered together with the Context. The Context therefore does not need a second EPM identity field merely to duplicate that binding.

## Recovery Invariant

If the original Agent session disappears completely, another Runtime/Agent must be able to load the Process Instance and Context and reconstruct:

- what engineering execution this is;
- what objective governs it;
- the current authoritative process situation;
- what material engineering knowledge and decisions have been recognized;
- what has been produced and verified;
- what remains unresolved or uncertain;
- what execution remains unfinished;
- what the expected continuation point is; and
- what conditions must be reconsidered or satisfied before continuing.

Recovery must use this persisted authoritative state rather than inventing missing history from conversation memory.

## Explicit Non-Requirements

Do not add:

- Agent/session identity;
- conversation identifiers or transcript state;
- Runtime process identity;
- IDE or Execution Environment metadata;
- a generalized workflow/task engine;
- event-sourcing infrastructure;
- new lifecycle concepts;
- speculative artifact or decision submodels;
- implementation-specific fields not justified by continuation semantics.

## Verification Requirements

The implementation must demonstrate that:

1. a Context can be created for a Process Instance;
2. the Context contains the minimum authoritative information defined above;
3. serialization and deserialization preserve its semantic state;
4. the Context remains associated with the correct Process Instance;
5. persisted Context contains sufficient information for a replacement Runtime/Agent to reconstruct the operational situation;
6. unfinished work can express its continuation point without relying on the previous conversation;
7. no transient Runtime/Agent/session information is required for recovery.

## Decision

**KEEP the current top-level `ExecutionContext` structure. ADAPT the contract of `pending_execution` to explicitly carry continuation information. Do not add a separate top-level continuation model or new AESM concept unless a concrete implementation finding later proves the existing representation insufficient.**
