# Minimal Runtime Interface for the First Vertical Slice

## Purpose

This document records the implementation-derived Runtime contract required by the first AESM vertical slice.

It is an execution-generated implementation document. It does not redefine the normative AESM model, EPM, PEM, or the architectural responsibilities of Runtime, Agent, Human Participant, or Execution Environment.

The purpose is to establish the smallest Runtime capability boundary before further Runtime implementation work begins.

## Evidence Reviewed

The interface was derived from the current implementation and the controlled implementation plan, including:

- `IMPLEMENTATION_PLAN.md`
- `runtime/core/models.py`
- `runtime/core/runtime.py`
- `runtime/core/store.py`
- `runtime/core/__init__.py`
- `runtime/README.md`
- `tests/continuity/test_runtime_recovery.py`
- the completed Execution Context verification evidence referenced by the implementation plan.

The implementation plan requires a Minimal Runtime Core covering Process Instance creation/loading, Context loading/saving, required process-state/lifecycle operations, evidence, decisions, artifacts, verification, and completion/termination, while preserving the distinction between Runtime and Agent responsibilities.

## Current Runtime Surface

The current `Runtime` exposes:

- `create_process(objective)`
- `attach(process_instance_id)`
- `observe(observation)`
- `recognize_decision(decision, recognition)`
- `set_pending_execution(work)`
- `record_verification(result)`
- `recognize_engineering_completion(completion)`
- `stop()`

The current `ProcessStore` provides:

- `create(instance, context)`
- `load_instance(process_instance_id)`
- `load_context(process_instance_id)`
- `save_context(context, event)`
- `history(process_instance_id)`

The current models provide persistent `ProcessInstance` identity and an authoritative `ExecutionContext` containing the operational state required for continuation.

## First Vertical Slice Runtime Boundary

The first vertical slice requires Runtime to maintain the operational process around Agent engineering work.

The Runtime must provide mechanisms to:

1. create and identify a Process Instance;
2. load an existing Process Instance and its authoritative Execution Context;
3. persist authoritative Execution Context changes;
4. record evidence supplied by the engineering process;
5. record an Engineering Decision only when that decision has been recognized under the governing execution semantics;
6. preserve pending execution and continuation information;
7. associate implementation artifacts with the Process Instance/Context;
8. record verification results;
9. apply the process-state/lifecycle changes required by the prototype;
10. recognize valid engineering completion under the governing execution semantics; and
11. terminate the Process Instance when the prototype's completion semantics require termination.

These are Runtime capabilities, not claims that every item must become a separate public method.

## Minimal Capability Contract

### Process Instance management

**Required capabilities:**

- Create a new Process Instance from the engineering objective.
- Load an existing Process Instance by stable identity.
- Establish or recover its associated authoritative Execution Context.

**Current coverage:** present through `create_process()` and `attach()`.

### Authoritative Context management

**Required capabilities:**

- Load the authoritative Execution Context for a Process Instance.
- Persist Context mutations and preserve continuity metadata/history.

**Current coverage:** present through `attach()` and `ProcessStore.save_context()`.

### Evidence recording

**Required capability:**

- Record evidence supplied by the engineering process into authoritative Context.

**Authority boundary:** Runtime records evidence; it does not decide whether the evidence is sufficient or valid for an engineering conclusion.

**Current coverage:** present through `observe()`.

### Decision recording

**Required capability:**

- Record a recognized Engineering Decision into authoritative Context.

**Authority boundary:** Runtime does not independently create, validate, or approve engineering decisions. Recognition must come from the governing execution semantics.

**Current coverage:** present through `recognize_decision()` and its explicit recognition check.

### Pending execution / continuation

**Required capability:**

- Preserve work that remains to be executed, including enough information to resume execution after Runtime/Agent/session replacement.

**Current coverage:** present through `set_pending_execution()` and the `pending_execution` Context field.

### Artifact association

**Required capability:**

- Associate implementation artifacts or artifact references with the Process Instance/Context as required for continuity and verification.

**Current coverage:** the Context model contains `artifacts`, but the Runtime has no explicit artifact-recording operation. The current embedding of an artifact reference inside pending work is not sufficient to treat artifact association as a completed Runtime capability.

**Decision:** artifact recording is a confirmed Runtime gap, but its exact API shape should be derived from the first real vertical slice rather than generalized now.

### Verification recording

**Required capability:**

- Record verification results in authoritative Context.

**Authority boundary:** Runtime records the verification result; it does not independently infer engineering correctness from the result.

**Current coverage:** present through `record_verification()`.

### Process state and lifecycle

**Required capability:**

- Apply only the process-state/lifecycle transitions demonstrated as necessary by the prototype.
- Preserve the distinction between engineering completion and Process Instance termination.

**Current coverage:** partially present. The Runtime currently changes `process_state` for pending implementation and recognized engineering completion, but there is no explicit termination operation and no generalized lifecycle state machine.

**Decision:** do not build a generalized lifecycle engine at this point. Add only transitions demonstrated to be required by the first vertical slice.

### Completion recognition

**Required capability:**

- Record engineering completion only when completion has been recognized under the governing execution semantics.

**Current coverage:** present through `recognize_engineering_completion()`.

### Process termination

**Required capability:**

- Persist the terminal Process Instance lifecycle state when the prototype's completion semantics require termination.

**Current coverage:** missing.

**Decision:** termination semantics must be established by the first vertical slice before implementation of a generalized termination mechanism.

## Authority Boundary

The Runtime is an implementation mechanism for process execution and continuity. It must not become the source of engineering judgment.

The Runtime must not independently:

- investigate engineering problems;
- determine evidence sufficiency;
- make Engineering Decisions;
- determine engineering correctness;
- perform engineering implementation work;
- determine completion solely from a generic signal such as successful verification;
- redefine EPM or PEM semantics.

The Runtime may enforce implementation-level conditions where the governing execution semantics require them, such as refusing to record an Engineering Decision or engineering completion without explicit recognition.

## Capability-to-Responsibility Mapping

| Capability | Runtime responsibility | Agent / participant responsibility | Current status |
|---|---|---|---|
| Process Instance creation/loading | Identity and persistence mechanism | Supply/use objective and request context | Present |
| Context loading/persistence | Authoritative state continuity | Consume and update process through allowed operations | Present |
| Evidence recording | Persist supplied evidence | Investigate and produce evidence | Present |
| Decision recording | Persist recognized decision | Reason and propose/establish decision under governing semantics | Present with recognition boundary |
| Pending execution | Preserve continuation state | Perform or plan engineering work | Present |
| Artifact association | Persist artifact/process association | Produce or modify artifacts | Missing |
| Verification recording | Persist verification result | Perform verification | Present |
| State/lifecycle transition | Apply required executable transition rules | Participate according to process guidance | Partial |
| Completion recognition | Persist recognized completion | Establish/recognize completion under governing semantics | Present |
| Termination | Persist terminal lifecycle state when required | Participate in completion | Missing |

## Minimality Decision

The first vertical slice does not justify:

- a generalized Runtime plugin architecture;
- distributed Runtime execution;
- multi-agent coordination;
- a generalized workflow/state-machine framework;
- automatic engineering judgment;
- an independent decision engine;
- environment-specific Runtime semantics;
- a broad artifact management subsystem.

The Runtime should remain a small control and persistence surface until an actual vertical-slice requirement demonstrates otherwise.

## Implementation Boundary for the Next Task

The next Runtime implementation task should be limited to capabilities that are demonstrated by the first vertical slice and this contract.

At minimum, the implementation work should address the confirmed missing artifact-association capability and the process termination behavior required by the selected prototype scenario. It should also make only the smallest process-state/lifecycle adjustments required by that scenario.

No generalized Runtime abstraction should be introduced solely because it appears architecturally attractive.

## Verification Criteria for This Interface Definition

This interface definition is considered complete when:

- every Runtime dependency of the first vertical slice has a named capability;
- each capability has an explicit responsibility boundary;
- existing Runtime coverage is distinguished from genuine gaps;
- no Agent responsibility has been moved into Runtime;
- no new AESM semantic requirement has been introduced;
- the remaining implementation work is sufficiently constrained to proceed without redesigning the Runtime during implementation.

## Conclusion

The existing Runtime already provides most of the continuity foundation required by the first vertical slice. The investigation does not justify replacing or broadly redesigning it.

The minimal Runtime boundary is a small mechanism for Process Instance identity, authoritative Context continuity, process records, controlled state progression, recognized outcomes, and persistence. The principal confirmed implementation gaps are artifact association and terminal Process Instance handling. Their concrete implementation should be driven by the first real vertical slice rather than by premature generalization.
