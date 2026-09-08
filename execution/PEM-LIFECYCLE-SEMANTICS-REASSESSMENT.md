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

## Lifecycle Semantics Decision

A model-level decision has now been made to resolve the outstanding question identified by this reassessment.

### Decision

**Process Instance lifecycle is a universal AESM/PEM semantic dimension, while concrete lifecycle transition conditions and scenario-specific triggers are determined by applicable execution semantics.**

This means AESM/PEM must define the universal meaning, invariants, and separation of Process Instance lifecycle. It must not, however, impose an unconditional universal state machine with fixed literal values and triggers independent of applicable engineering/execution semantics.

This preserves the established boundary:

```text
EPM
  → defines engineering meaning, including Process State and engineering completion

PEM
  → governs execution and universal Process Instance lifecycle semantics

Applicable execution semantics
  → establish concrete lifecycle transition conditions and scenario-specific triggers

Runtime
  → implements those semantics
```

The full decision and its rationale are recorded in:

`execution/PROCESS-INSTANCE-LIFECYCLE-SEMANTICS-DECISION.md`

### Consequences

The previous open question is resolved. The correct next task is now **specification clarification**, not implementation.

The specification must make explicit:

- universal Process Instance lifecycle semantic categories;
- lifecycle invariants;
- lifecycle transition authority;
- how applicable execution semantics establish transition conditions;
- suspension semantics;
- resumption semantics;
- Process Instance termination semantics;
- lifecycle state representation, including whether canonical literals are required;
- lifecycle history/traceability requirements;
- recovery behavior involving lifecycle condition.

Until these are clarified, no generalized lifecycle state machine or mandatory `suspend()`, `resume()`, or `terminate()` API should be implemented.

## Lifecycle Conformance Interpretation

The current specification, interpreted through the decision above, supports the following conformance interpretation.

| Semantic | Specification status | What implementation must demonstrate | Current prototype evidence | Assessment |
|---|---|---|---|---|
| Process Instance lifecycle | Universal semantic dimension | Preserve lifecycle independently from Process State, completion, and Runtime lifetime | `active` preserved | Separation demonstrated; concrete transitions require clarification |
| Lifecycle state vocabulary | Requires specification clarification | Represent lifecycle according to clarified semantics | Only `active` exists | Specification precision gap |
| Suspension | Supported where applicable | Preserve authoritative continuation state and suspend according to applicable conditions | No explicit operation observed | Not demonstrated; implementation defect not established |
| Resumption | Required for applicable continuation | Recover, reevaluate, and continue under PEM | Recovery demonstrated; no explicit resume operation | Recovery demonstrated; semantic resumption not demonstrated |
| Runtime termination | Distinct lifecycle | Do not silently terminate Process Instance | `stop()` leaves persisted lifecycle active | Demonstrated |
| Process Instance termination | Distinct semantic category | Apply clarified termination conditions and preserve authoritative state/history | No operation observed | Not demonstrated; final requirement awaits specification clarification |
| Recovery | Required | Reconstruct authoritative state independently of transient Runtime memory | Cross-Runtime recovery passes | Demonstrated |
| Pending execution | Required as continuation information where applicable | Preserve unfinished work and relevant conditions | Persisted and recovered | Demonstrated |
| Pending-work resumption | Governed by PEM | Reevaluate recovered situation before execution | No explicit continuation operation observed | Not demonstrated |
| Engineering completion | EPM determination | Require applicable completion conditions; keep distinct from lifecycle termination | Explicit completion recognition works | Demonstrated at prototype level |

## Classification Rules

The lifecycle experiment should not automatically classify every absent Runtime operation as a Representation Gap or Implementation Defect.

Use this order:

1. Establish whether the semantic requirement exists in applicable EPM/PEM semantics.
2. Establish whether the requirement is sufficiently precise to identify expected behavior.
3. Compare implementation representation and behavior with that requirement.
4. Determine whether the experiment actually exercised the required behavior.
5. Classify the result only after those questions are answered.

The resulting classifications are:

### Validated semantic boundary

Runtime lifetime is distinct from Process Instance lifecycle and engineering completion.

### Specification precision gap

The current specification does not yet provide a complete universal Process Instance lifecycle state vocabulary and transition table.

### Evidence gap

The prototype does not demonstrate semantic resumption or suspension behavior merely because recovery and pending-state persistence work.

### Potential implementation gap, pending specification clarification

Explicit Process Instance termination and suspension support may require implementation when clarified applicable semantics establish concrete required behavior. The current prototype cannot be declared defective in the abstract solely from absent APIs.

## Consequences for the Lifecycle Experiment Report

The experiment record should preserve its empirical findings but revise interpretation where necessary:

- Do not state that the mere absence of lifecycle mutation proves a Representation Gap.
- Do not treat `engineering_complete` as a universal AESM Process State.
- Do not treat Runtime `stop()` as a failed Process Instance termination operation; the semantic model explicitly separates those lifetimes.
- Distinguish successful recovery from demonstrated semantic resumption.
- Treat suspension, resumption, and termination implementation requirements as dependent on clarified applicable semantics.
- Promote Runtime lifetime ≠ Process Instance lifetime as a primary validated finding.
- Keep empirical observations separate from conclusions derived from specification analysis.
- Use semantic names rather than numeric phase labels when describing investigative stages.

## Required Specification Work

The next work item is to update the appropriate normative/specification documents so that the decision above becomes explicit and operationally precise.

The specification work should not yet prescribe implementation APIs. It should establish semantics first, including the relationship among lifecycle categories, Process State, engineering completion, Runtime lifetime, recovery, suspension, resumption, and termination.

After the specification clarification, the implementation ↔ PEM conformance matrix should be rerun against the clarified requirements, followed by targeted validation where evidence is still missing.

## Final Assessment

The targeted reassessment established that the lifecycle experiment uncovered a real limitation in the prototype's demonstrated lifecycle behavior, but the experiment did not by itself establish the precise nature of every lifecycle gap.

The model-level decision now resolves the outstanding semantic boundary:

**Process Instance lifecycle is universal at the AESM/PEM semantic level; concrete lifecycle transition conditions and scenario-specific triggers are established by applicable execution semantics.**

The current model already requires:

- a Process Instance lifecycle distinct from Process State;
- separation of Runtime lifetime from Process Instance lifetime;
- suspension and resumption semantics when applicable;
- recovery from authoritative persistent state;
- pending execution as continuation information;
- reevaluation before resumed execution;
- explicit distinction between engineering completion and Process Instance termination.

The remaining deficiency is specification precision: the lifecycle categories, state representation, invariants, and transition conditions need to be made sufficiently explicit to support a definitive implementation conformance determination.

Therefore implementation changes remain deferred until that specification clarification is complete.
