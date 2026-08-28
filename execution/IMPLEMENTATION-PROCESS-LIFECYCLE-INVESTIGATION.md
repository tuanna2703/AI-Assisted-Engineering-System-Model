# First-Vertical-Slice Process Lifecycle Investigation

## Purpose

This document records the implementation investigation required before adding process-state/lifecycle behavior to the first AESM Runtime vertical slice.

It is an execution-generated implementation document. It does not redefine the normative AESM model, EPM, PEM, Process Instance, or Execution Context semantics.

The objective is to determine the smallest lifecycle behavior that can be justified by the current AESM semantics and the existing first-vertical-slice implementation boundary, and to prevent current implementation assignments from becoming accidental lifecycle semantics.

## Evidence Reviewed

The investigation reviewed:

- `IMPLEMENTATION_PLAN.md`
- `execution/IMPLEMENTATION-MINIMAL-RUNTIME-INTERFACE.md`
- `docs/03-Engineering-Model.md`
- `docs/04-Execution-Model.md`
- `docs/05-Process-Instance-and-Execution-Context.md`
- `runtime/core/models.py`
- `runtime/core/runtime.py`
- `runtime/core/store.py`
- `runtime/README.md`
- `tests/continuity/test_runtime_recovery.py`

The current repository state contains no separate, implementation-independent state-machine definition for the first vertical slice.

## Authoritative Lifecycle Semantics

The current AESM documentation establishes several important constraints.

### Process State belongs to EPM semantics

The Engineering Model defines Process State as a representation of the current stage of engineering work. A state has engineering meaning, permitted activities, expected outputs, completion conditions, and transition constraints. Process States and transition rules belong to the applicable EPM; PEM governs how the Runtime evaluates, executes, records, and recovers transitions.

Therefore, a Runtime string such as `implementation` cannot become an authoritative AESM Process State merely because the implementation currently assigns it.

### Completion is not a generic state mutation

Engineering completion is an EPM engineering determination. It may only be established when applicable EPM completion conditions are satisfied. Successful execution of an action, successful verification, absence of pending technical work, or Runtime shutdown does not by itself establish engineering completion.

The Runtime may record completion after explicit recognition under the governing semantics, but it must not invent the completion conditions.

### Engineering completion, Process Instance termination, and Runtime termination are distinct

AESM explicitly separates:

- engineering completion;
- Process Instance termination; and
- Runtime termination.

Stopping or restarting the Runtime does not complete or terminate the Process Instance. A terminal Process Instance lifecycle state therefore requires explicit lifecycle semantics rather than being inferred from Runtime shutdown or Agent/session loss.

### Suspension and resumption are distinct from termination

Execution may be suspended when permitted. Suspension preserves authoritative state, pending work, unresolved conditions, traceability, and failure/uncertainty information for later resumption. Resumption begins from authoritative state and re-evaluates applicable conditions.

The current prototype already preserves pending execution information, but the current Runtime does not expose a separate suspension operation.

## Existing Implementation Behavior

`ExecutionContext` currently initializes with:

- `process_state = "initial"`;
- `execution_mode = "active"`;
- `engineering_completion = False`.

`ProcessInstance` currently initializes with:

- `lifecycle = "active"`.

The Runtime currently performs two process-state assignments:

1. `set_pending_execution()` sets `context.process_state = "implementation"`.
2. `recognize_engineering_completion()` sets `context.process_state = "engineering_complete"` and `context.engineering_completion = True`.

The existing continuity test consequently treats `engineering_complete` as a process-state value after recognized engineering completion.

These assignments are implementation behavior. The reviewed AESM documentation does not define `initial`, `implementation`, or `engineering_complete` as universal Process State identifiers.

## First-Vertical-Slice Requirements

The controlled implementation plan defines the first vertical slice as a real engineering request that connects Process Instance, Execution Context, Agent guidance, engineering work, evidence, decisions, artifacts, verification, persistence, resume, and valid completion.

The minimal Runtime interface investigation already established that the Runtime needs controlled process-state/lifecycle behavior, but explicitly rejected a generalized lifecycle engine. It also identified artifact association and terminal Process Instance handling as gaps whose concrete semantics should be derived from the actual vertical slice.

At the current point in the implementation, the repository has not yet selected the specific real engineering request that will serve as the first vertical slice. Consequently, the exact EPM-defined state vocabulary and completion/termination conditions of that scenario are not yet available.

This is a material limitation: the Runtime cannot legitimately derive a general state machine from the current prototype assignments without introducing implementation-defined engineering semantics.

## Minimal State Model Justified Now

The investigation supports only the following implementation-level conclusions.

| Representation | Current value/meaning | Justification | Action |
|---|---|---|---|
| `ProcessInstance.lifecycle = "active"` | Process Instance exists and remains operational | Consistent with the current prototype's non-terminal creation state | Retain for now |
| `ExecutionContext.process_state = "initial"` | Initial implementation representation before process progression | Useful implementation representation, but not established as a universal EPM state | Retain as current prototype representation; do not generalize |
| `ExecutionContext.process_state = "implementation"` | Current Runtime marks pending implementation work | Consistent with the prototype's implementation activity, but not defined as a universal AESM state | May remain temporarily, but transition must be treated as prototype-specific |
| `ExecutionContext.engineering_completion = True` | Explicitly recognized engineering completion | Directly supported by EPM/PEM separation when completion has been recognized under applicable conditions | Retain |
| `ExecutionContext.process_state = "engineering_complete"` | Current implementation couples completion recognition to a state string | Not defined by the normative model and risks conflating engineering completion with Process State semantics | Do not expand this into a generalized state model without vertical-slice evidence |
| Process Instance terminal lifecycle state | Not currently represented | Termination is distinct and requires applicable lifecycle semantics | Do not invent a terminal value yet |

The strongest conclusion is therefore that **engineering completion is already a justified operational fact when explicitly recognized, but `engineering_complete` is not yet justified as a universal Process State identifier**.

## Required Transition Candidates

### Initial → implementation

The current implementation performs this transition when pending execution is recorded.

This is a plausible transition for the selected prototype, because the first vertical slice includes actual engineering implementation work. However, the investigation cannot establish it as a universal AESM transition because the applicable EPM state definition has not yet been selected for the real engineering request.

**Current decision:** retain the behavior as prototype implementation scaffolding, but do not generalize or expose it as a universal lifecycle rule yet.

### implementation → engineering completion

The current implementation changes the Process State to `engineering_complete` when engineering completion is explicitly recognized.

The recognition boundary is justified: the Runtime must not infer completion merely from verification or technical inactivity. The existing test correctly verifies that explicit recognition is required before `engineering_completion` becomes true.

The state assignment itself is not yet justified as a universal transition because the canonical model defines completion as an EPM engineering determination rather than defining `engineering_complete` as a universal state identifier.

**Current decision:** preserve explicit completion recognition, but defer the generalized state-transition interpretation until the first vertical slice supplies the applicable EPM state semantics.

### active → terminal lifecycle state

No concrete terminal state is currently defined by the implementation or the reviewed AESM documentation set.

Termination is explicitly distinct from engineering completion, and Runtime shutdown does not imply termination.

**Current decision:** do not implement a guessed terminal lifecycle value. The selected vertical slice must first establish whether and when Process Instance termination is required.

### active → suspended / suspended → active

The normative model permits suspension and resumption when applicable, but the first vertical slice has not demonstrated a need for an explicit suspension operation yet. Persisted `pending_execution`, unresolved matters, and failure/uncertainty already provide continuation information.

**Current decision:** do not add suspension transitions to the Runtime solely because the model permits them. Add them only if the selected vertical slice requires explicit suspension semantics.

## Transition Conditions

The investigation establishes the following authority rules for any future Runtime transition:

1. The Runtime must not invent EPM state meaning.
2. A transition must be grounded in the applicable EPM transition conditions.
3. PEM execution conditions must permit the transition.
4. Required recognition must occur before authoritative mutation.
5. Engineering completion must not be inferred from successful verification alone.
6. Runtime shutdown, replacement, or restart must not mutate Process Instance lifecycle state.
7. A terminal lifecycle transition must remain distinct from engineering completion.
8. Failed verification or uncertainty must remain representable without automatic termination.
9. Historical state changes must remain reconstructable through authoritative history.

## Current Implementation Gaps and Deviations

### Confirmed gap: explicit lifecycle control

The Runtime has no explicit operation for Process Instance termination. This remains a real gap, but its target lifecycle value and triggering conditions cannot yet be specified without the first vertical slice's concrete completion/termination semantics.

### Confirmed gap: generalized state validation

The Runtime currently assigns state strings directly. It does not validate a transition against an EPM-defined state graph or transition conditions.

A generalized transition engine is **not** justified at this stage. Building one would introduce a semantic abstraction before the applicable first-vertical-slice state model is known.

### Existing behavior requiring caution: `engineering_complete`

The current Runtime couples recognized engineering completion to `process_state = "engineering_complete"`. The completion recognition itself is correctly protected by explicit recognition, but the state value should not be treated as a normative AESM state until supported by the selected EPM semantics.

### Existing behavior requiring caution: `implementation`

The current Runtime changes state whenever pending execution is recorded. This is reasonable prototype scaffolding, but recording pending work does not universally establish that the EPM state has changed. A future implementation should make the transition only when the applicable EPM/PEM conditions establish it.

## Minimal Implementation Boundary

Before the first real vertical slice is selected, the Runtime should **not** acquire a generalized lifecycle/state-machine abstraction.

The next implementation work may safely preserve the existing explicit recognition behavior and the current prototype state representations, but should not add new universal state names or transition rules.

Once the first vertical slice is selected, its applicable EPM state semantics should be used to define only the transitions actually exercised by that scenario. Those transitions should then be implemented and tested as Runtime-controlled operations.

In particular:

- retain explicit recognition before engineering-completion mutation;
- do not infer completion from verification automatically;
- do not infer termination from completion or Runtime shutdown;
- do not add suspension lifecycle operations unless the slice requires them;
- do not build a generalized state-machine framework;
- do not treat implementation strings as frozen AESM semantics.

## Verification Implications

The lifecycle implementation tests should ultimately prove, for the selected vertical slice, that:

- invalid or unrecognized transitions are rejected;
- required transition conditions are enforced;
- valid transitions persist in authoritative Context;
- transition history is reconstructable;
- engineering completion is distinct from Process Instance termination;
- Runtime stop/replacement does not alter Process Instance lifecycle;
- failed verification does not automatically establish completion or termination;
- resume recovers the current state and pending conditions correctly.

The existing tests already provide partial evidence for explicit engineering-completion recognition and Runtime replacement continuity, but they do not yet establish a complete lifecycle contract.

## Conclusion

The investigation does **not** justify implementing a generalized process lifecycle/state machine at this point.

The current Runtime contains useful prototype behavior, but its state strings are implementation representations rather than established universal AESM Process States. The authoritative model places Process State and transition validity under the applicable EPM, with PEM governing Runtime execution of those transitions.

The most important finding is that **engineering completion recognition is justified, while the current `engineering_complete` Process State assignment is not yet justified as a general AESM state**. Likewise, `implementation` is a plausible prototype state but cannot be generalized without the selected EPM state semantics.

Therefore, the next implementation boundary should remain narrow: preserve the recognition boundary, avoid adding a generalized lifecycle mechanism, and derive concrete state/lifecycle transitions from the first real vertical slice before introducing new Runtime-controlled transition behavior.

## Recommended Next Task

**Select and define the first real vertical slice's applicable process-state/lifecycle semantics.**

That task should identify the concrete engineering request, determine the applicable EPM states and completion/termination conditions exercised by it, and produce the evidence needed to turn the prototype's current state assignments into explicit, testable Runtime transitions.
