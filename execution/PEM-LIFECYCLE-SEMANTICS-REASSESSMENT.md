# PEM Lifecycle Semantics Reassessment

## Purpose

This document records a targeted reassessment of the current AESM Process Execution Model (PEM) lifecycle semantics following the Process Instance lifecycle validation experiment.

The purpose is to determine what lifecycle behavior is actually required by the current AESM model before classifying implementation observations as gaps or defects.

This is a specification/conformance investigation. It does not implement lifecycle behavior, modify Runtime code, modify tests, or redefine normative semantics.

## Scope

The reassessment is intentionally limited to:

- Process Instance lifecycle;
- lifecycle states and transition semantics;
- suspension;
- resumption;
- Runtime termination versus Process Instance termination;
- recovery;
- pending execution;
- pending-work continuation;
- engineering completion;
- the resulting implementation/conformance questions.

It is not a broad architecture review.

## Evidence Reviewed

The following current repository artifacts were reviewed:

- `docs/03-Engineering-Model.md`
- `docs/04-Execution-Model.md`
- `docs/05-Process-Instance-and-Execution-Context.md`
- `docs/07-Runtime-and-Conformance.md`
- `implementation/process_instance_lifecycle_validation_report.md`
- `execution/IMPLEMENTATION-PROCESS-LIFECYCLE-INVESTIGATION.md`

The lifecycle validation report records empirical behavior at commit `8c2dd09087e064a029d32452a006cbd2b786e5f2`. This reassessment evaluates that evidence against the current documented semantics; it does not retroactively change what the experiment demonstrated.

## Findings

### Process Instance lifecycle is a distinct semantic dimension

The current model explicitly distinguishes Process Instance lifecycle from Process State, engineering completion, and Runtime lifecycle.

A Process Instance is the persistent identity of one engineering execution. Its lifecycle describes the condition of that continuing engineering execution entity. Runtime startup, restart, failure, replacement, or termination does not itself imply Process Instance termination.

**Conclusion:** The lifecycle concept is required by the current model. It is not merely an implementation convenience.

### Lifecycle state vocabulary is not sufficiently specified

The current documentation establishes that lifecycle is distinct from ordinary Process State progression and that lifecycle transitions are governed by applicable execution semantics. However, it does not define a complete, implementation-independent lifecycle state vocabulary or a complete transition table.

In particular, the current documentation does not establish a universal set of literal values such as `active`, `suspended`, or `terminated`, nor does it define all legal transition conditions among such values.

**Conclusion:** A lifecycle state machine cannot yet be derived as a universal implementation contract from the current specification alone.

This is a specification precision issue, not yet an implementation defect.

### Suspension is a supported semantic possibility

PEM states that execution may be suspended when permitted by applicable execution semantics. Suspension preserves sufficient authoritative state for later continuation, including current Process State, pending execution, unresolved conditions, interruption information, traceability, and relevant failure or uncertainty information.

Suspension is explicitly distinct from termination.

**Conclusion:** Suspension is within the semantic scope of PEM. The current documentation does not, however, define a universal suspension trigger, mandatory API shape, or universal lifecycle state literal.

Therefore the absence of a `suspend()` Runtime method in the prototype is not by itself sufficient evidence of an implementation defect.

### Resumption is explicitly required when continuation occurs

PEM defines resumption as re-entering execution from recovered authoritative state. It is explicitly not replay of the last Runtime operation.

The required conceptual sequence is:

```text
Recover authoritative state
        ↓
Observe
        ↓
Evaluate
        ↓
Plan
        ↓
Execute
        ↓
Verify
        ↓
Update Execution Context
        ↓
Repeat
```

The Runtime must reevaluate applicable conditions using recovered state before continuing. Persisted `next_action` and `pending_execution` do not constitute permission to execute an action without reevaluation.

**Conclusion:** Resumption semantics are defined at the execution-semantic level. A specific `resume()` API is not required by name, but a conforming Runtime must support the semantic ability to continue a Process Instance from authoritative recovered state when continuation is applicable.

### Recovery is distinct from resumption

The Process Instance and Execution Context specification distinguishes:

```text
Discovery = identify an existing Process Instance
Recovery  = reconstruct authoritative Execution Context
Resumption = re-enter PEM execution using recovered authoritative state
```

Recovery must not depend on transient Runtime memory, Agent context, or conversation history.

**Conclusion:** The existing experiment's successful cross-Runtime recovery is evidence for recovery/continuity. It is not, by itself, evidence that the Runtime implements full semantic resumption.

### Pending execution is continuation information, not an execution command

The current model explicitly defines `pending_execution` as unfinished execution activity relevant to continuation, `next_action` as expected continuation activity, and `resumption_conditions` as conditions to consider before continuation.

The presence of pending work does not establish that execution is currently permissible.

**Conclusion:** Persistence of pending execution is required continuity behavior, but persistence alone does not demonstrate pending-work resumption.

### Runtime termination is explicitly separate from Process Instance termination

The current model states that Runtime startup, restart, failure, replacement, and termination do not themselves imply Process State transition, Process Instance termination, or engineering completion.

The lifecycle validation experiment observed that `Runtime.stop()` only detached the Runtime in memory and left the persisted Process Instance lifecycle unchanged.

**Conclusion:** The experiment's observation that Runtime termination did not terminate the Process Instance is consistent with the documented semantic boundary.

This is a validated separation, not a lifecycle failure.

### Process Instance termination is a distinct semantic condition

The current documentation explicitly distinguishes Process Instance termination from engineering completion and Runtime termination. Runtime conformance documentation also identifies termination as a lifecycle responsibility according to applicable semantics.

However, the current model does not provide a complete universal terminal-state vocabulary or universal termination transition conditions.

**Conclusion:** The semantic category of Process Instance termination exists and must remain distinct, but its concrete trigger/state representation cannot yet be inferred universally from the current documentation.

The absence of a concrete terminal lifecycle operation in the prototype therefore remains a conformance question whose final classification depends on the applicable EPM/PEM lifecycle semantics of the engineering scenario.

### Engineering completion is not Process Instance termination

EPM defines engineering completion as an engineering determination established when applicable EPM completion conditions are satisfied. It explicitly states that completion is distinct from Runtime termination and Agent/session stopping.

The lifecycle model independently distinguishes Process Instance termination from engineering completion.

The experiment observed:

```text
engineering_completion: False → True
process_state: verification → engineering_complete
ProcessInstance.lifecycle: active → active
```

**Conclusion:** Keeping lifecycle unchanged when engineering completion is recognized is not evidence of a defect. The model requires these concepts to remain distinct.

The separate question is whether `engineering_complete` is a valid universal Process State identifier. The current EPM documentation does not establish that literal value as universal; Process State identity belongs to the applicable EPM.

## Lifecycle Conformance Interpretation

The current specification supports the following conformance interpretation.

| Semantic | Specification status | What implementation must demonstrate | Current prototype evidence | Preliminary assessment |
|---|---|---|---|---|
| Process Instance lifecycle | Required conceptually | Preserve lifecycle independently from Process State, completion, and Runtime lifetime | `active` preserved | Demonstrated separation; lifecycle transition semantics remain under-specified |
| Lifecycle state vocabulary | Incomplete | Use states defined by applicable semantics | Only `active` exists | Specification precision gap |
| Suspension | Required when applicable | Preserve authoritative continuation state and suspend execution according to applicable conditions | No explicit operation observed | Not demonstrated; not yet an implementation defect solely from absence of API |
| Resumption | Required for applicable continuation | Recover state, reevaluate, and continue under PEM | Recovery demonstrated; no explicit resume operation | Recovery demonstrated; semantic resumption not demonstrated |
| Runtime termination | Distinct lifecycle | Do not silently terminate Process Instance | `stop()` leaves persisted lifecycle active | Demonstrated |
| Process Instance termination | Required as distinct semantic category where applicable | Apply defined lifecycle termination conditions and preserve authoritative state/history | No operation observed | Not demonstrated; concrete requirement remains scenario/specification dependent |
| Recovery | Required | Reconstruct authoritative state independently of transient Runtime memory | Cross-Runtime recovery passes | Demonstrated |
| Pending execution | Required as continuation information where applicable | Preserve unfinished work and relevant conditions | Persisted and recovered | Demonstrated |
| Pending-work resumption | Governed by PEM | Reevaluate recovered situation before execution | No explicit continuation operation observed | Not demonstrated |
| Engineering completion | EPM determination | Require applicable completion conditions; keep distinct from lifecycle termination | Explicit completion recognition works | Demonstrated at prototype level |

## Classification Rules Resulting from the Reassessment

The lifecycle experiment should not automatically classify every absent Runtime operation as a Representation Gap or Implementation Defect.

Use the following order:

1. Establish whether the semantic requirement exists in the applicable EPM/PEM semantics.
2. Establish whether the requirement is sufficiently precise to identify the expected behavior.
3. Compare the implementation representation and behavior with that requirement.
4. Determine whether the experiment actually exercised the required behavior.
5. Classify the result only after those questions are answered.

This yields the following preliminary categories:

### Validated semantic boundary

Runtime lifetime is distinct from Process Instance lifecycle and engineering completion.

### Specification precision gap

The current documentation does not provide a complete universal Process Instance lifecycle state vocabulary and transition table.

### Evidence gap

The prototype does not demonstrate semantic resumption or suspension behavior merely because recovery and pending-state persistence work.

### Potential implementation gap, pending applicable semantics

Explicit Process Instance termination and explicit suspension may require implementation support when an applicable EPM/PEM scenario establishes their concrete conditions. The current documentation is insufficient to declare the prototype defective in the abstract.

## Consequences for the Lifecycle Experiment Report

The authoritative experiment record should preserve its empirical findings but revise interpretation where necessary:

- Do not state that the mere absence of lifecycle mutation proves a Representation Gap.
- Do not treat `engineering_complete` as a universal AESM Process State.
- Do not treat Runtime `stop()` as a failed Process Instance termination operation; the semantic model explicitly separates those lifetimes.
- Distinguish successful recovery from demonstrated semantic resumption.
- Treat suspension, resumption, and termination requirements as specification-dependent until concrete lifecycle transition semantics are established.
- Promote Runtime lifetime ≠ Process Instance lifetime as a primary validated finding.
- Keep empirical observations separate from conclusions derived from specification analysis.
- Use semantic names rather than numeric phase labels when describing investigative stages.

## Required Decision Before Implementation

The next substantive model-level question is not whether to add `suspend()`, `resume()`, or `terminate()` methods.

The required question is:

> Does AESM need a fully specified Process Instance lifecycle state model independent of any particular EPM, or should lifecycle states and transition conditions be defined only by the applicable EPM/PEM execution semantics of each engineering process?

The current documents strongly support the second principle for Process State: EPM defines engineering state meaning while PEM governs execution. The same distinction should be resolved explicitly for Process Instance lifecycle semantics before implementation work begins.

Until that decision is made, no generalized lifecycle state machine should be implemented.

## Final Assessment

The targeted reassessment establishes that the lifecycle experiment uncovered a real implementation limitation but did not, by itself, establish the precise nature of every lifecycle gap.

The current AESM model already requires:

- a Process Instance lifecycle distinct from Process State;
- separation of Runtime lifetime from Process Instance lifetime;
- suspension and resumption semantics when applicable;
- recovery from authoritative persistent state;
- pending execution as continuation information;
- reevaluation before resumed execution;
- explicit distinction between engineering completion and Process Instance termination.

What remains insufficiently specified is the concrete lifecycle state vocabulary and universal transition conditions.

Therefore the correct next step is **specification clarification of Process Instance lifecycle semantics**, followed by a conformance determination against those clarified semantics. Implementation changes should remain deferred until that clarification is complete.
