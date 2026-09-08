# Process Instance Lifecycle Conformance Finding Reconciliation

## Purpose

This document reconciles the empirical findings of the controlled Process Instance lifecycle validation with the current AESM/PEM lifecycle semantics.

Its purpose is to determine which observed implementation absences are:

- validated semantic boundaries;
- specification precision gaps;
- evidence gaps;
- confirmed implementation/conformance gaps; or
- potential implementation gaps that remain conditional on applicable execution semantics.

This document does not authorize Runtime implementation changes.

## Baseline

The reconciliation uses the following evidence:

- lifecycle validation experiment at commit `7273f2e9535436310e0df22c01800e172d848bb4`;
- lifecycle semantics reassessment;
- Process Instance lifecycle semantics decision;
- current Runtime and Conformance specification;
- current lifecycle conformance matrix.

The governing model decision is:

> Process Instance lifecycle is a universal AESM/PEM semantic dimension, while concrete lifecycle transition conditions and scenario-specific triggers are established by applicable execution semantics.

The decision explicitly defers generalized lifecycle implementation until specification clarification establishes concrete required behavior.

## Reconciliation Principle

An implementation observation is not a conformance defect merely because a mechanism is absent.

The classification order is:

```text
Semantic requirement exists
        ↓
Requirement is sufficiently precise
        ↓
Expected implementation behavior is derivable
        ↓
Implementation is compared with that behavior
        ↓
Experiment establishes actual behavior
        ↓
Conformance finding
```

This prevents API presence from becoming an implicit source of AESM semantics.

## Finding Reconciliation

| Observed condition | Empirical status | Semantic interpretation | Final classification |
|---|---|---|---|
| `ProcessInstance.lifecycle` exists and is preserved independently of Process State | Demonstrated | Lifecycle must remain distinct from EPM Process State | **Validated semantic boundary / demonstrated conformance** |
| Lifecycle remains `active` while Process State progresses | Demonstrated | Process State progression does not inherently constitute lifecycle transition | **Validated semantic boundary** |
| Lifecycle remains `active` after engineering completion | Demonstrated | Engineering completion is distinct from lifecycle termination | **Validated semantic boundary / demonstrated conformance** |
| `Runtime.stop()` leaves Process Instance lifecycle unchanged | Demonstrated | Runtime lifetime is distinct from Process Instance lifecycle | **Validated semantic boundary / demonstrated conformance** |
| Lifecycle state is persisted and recovered at creation | Demonstrated | Lifecycle condition must be authoritative and recoverable | **Partial conformance evidence** |
| No `suspend()` or equivalent API | Established implementation fact | AESM does not prescribe an API; concrete suspension conditions remain applicable-semantics dependent | **Evidence gap / conditional implementation question** |
| No `resume()` or equivalent API | Established implementation fact | Resumption is a semantic capability, not a required method name; recovery alone does not demonstrate resumption | **Evidence gap** |
| No `terminate()` or equivalent API | Established implementation fact | Termination is a required semantic category, but concrete triggers and representation require applicable semantics | **Potential implementation gap pending specification clarification** |
| No lifecycle mutation path in Runtime | Established implementation fact | No concrete lifecycle transition can currently be exercised | **Evidence gap for transition behavior; not independently a defect** |
| No ProcessInstance update persistence mechanism | Established implementation fact | Required only if applicable lifecycle semantics require mutable lifecycle state in this implementation | **Structural implementation prerequisite, not yet a confirmed semantic defect** |
| No lifecycle-specific history events | Established implementation fact | Material lifecycle transitions require reconstructable history once transitions are applicable and occur | **Traceability implementation prerequisite; not yet an exercised-transition defect** |
| No general lifecycle authorization mechanism | Established implementation fact | Authorization rules depend on applicable execution semantics | **Specification-dependent / evidence gap** |
| Pending execution survives Runtime replacement | Demonstrated | Pending work is authoritative continuation information | **Demonstrated conformance for persistence** |
| Pending execution is not shown being reevaluated and resumed | Not demonstrated | Resumption requires reevaluation before continuation | **Evidence gap** |
| Cross-Runtime recovery succeeds | Demonstrated | Recovery is distinct from resumption and is required for continuity | **Demonstrated recovery / continuity** |
| Cross-process/environment replacement was not directly exercised | Not demonstrated | Full environment-independent continuity remains broader than the experiment | **Evidence limitation** |

## Confirmed Conformance Findings

The following conclusions are sufficiently established by both specification and evidence.

### Runtime lifetime is not Process Instance lifecycle

`Runtime.stop()` does not suspend, terminate, or complete the Process Instance. The experiment directly observed that persisted lifecycle and Process State remained unchanged after Runtime detachment.

This is a **validated conformance property**, not a defect.

### Lifecycle is distinct from Process State

The implementation maintains lifecycle separately from `ExecutionContext.process_state`, and process-state transitions did not mutate lifecycle.

This is a **demonstrated semantic separation**.

### Engineering completion is distinct from lifecycle termination

Engineering completion changes the applicable EPM Process State and completion indication without implying Process Instance lifecycle termination.

This is a **validated semantic boundary**.

### Recovery is distinct from resumption

The Runtime can recover a Process Instance and Execution Context through a fresh Runtime instance. The experiment did not demonstrate a semantic resumed execution path with reevaluation.

Therefore recovery is demonstrated, while resumption remains an **evidence gap**.

## Specification Precision Finding

The remaining specification work is to make the universal lifecycle semantics sufficiently operationally precise.

The specification should explicitly define:

- universal lifecycle semantic categories;
- lifecycle invariants;
- transition authority;
- how applicable execution semantics establish transition conditions;
- suspension preservation requirements;
- resumption and reevaluation requirements;
- termination semantics and finality;
- lifecycle state representation requirements;
- lifecycle history requirements;
- recovery treatment of lifecycle condition.

The existing lifecycle semantics decision already establishes that these questions must be resolved at the specification level before generalized implementation.

This is a **specification clarification task**, not a Runtime defect.

## Conditional Implementation Findings

### Suspension

The absence of a suspension mechanism cannot currently be classified as a confirmed defect in isolation.

A confirmed implementation gap requires an applicable execution scenario that establishes a valid suspension condition and therefore creates a concrete Runtime obligation.

Once such a condition exists, the Runtime must provide the semantic capability to preserve authoritative continuation state and establish the suspended lifecycle condition without conflating suspension with Runtime shutdown.

### Resumption

The Runtime must support semantic continuation where applicable, including recovery, reevaluation, and controlled continuation. A named `resume()` API is not required unless applicable implementation semantics prescribe one.

The current experiment does not demonstrate that complete semantic behavior.

This is currently an **evidence gap**, not a confirmed API-level defect.

### Termination

Process Instance termination is a universal lifecycle category distinct from engineering completion and Runtime termination. However, the concrete termination condition, authority, and representation remain applicable-semantics dependent.

Therefore the absence of a termination API is a **potential implementation gap pending specification clarification**, not a confirmed defect at the current abstraction level.

## Lifecycle History

The experiment established that current history records Process State and execution events but contains no lifecycle transition events.

This observation is valid and should not be discarded. Its conformance interpretation is conditional:

- if no lifecycle transition is applicable or occurs, absence of a lifecycle transition event does not demonstrate a failed transition record;
- when a material lifecycle transition is established and executed, the clarified semantics require enough history to reconstruct the transition basis, resulting state, timing/sequence, authority where applicable, relevant conditions/evidence, and material consequences.

Therefore the current state is a **traceability implementation prerequisite**, not a confirmed failure of an exercised lifecycle transition.

## Final Classification

The lifecycle experiment should no longer be summarized as proving that the Runtime has a generic "lifecycle implementation gap" merely because lifecycle mutation APIs are absent.

The corrected classification is:

```text
Validated semantic boundaries
    ├─ Runtime lifetime ≠ Process Instance lifecycle
    ├─ Process Instance lifecycle ≠ EPM Process State
    └─ engineering completion ≠ lifecycle termination

Demonstrated capabilities
    ├─ lifecycle representation at creation
    ├─ lifecycle persistence/recovery for observed state
    ├─ Process Instance continuity across Runtime replacement
    └─ pending execution persistence/recovery

Evidence gaps
    ├─ suspension behavior
    ├─ semantic resumption and reevaluation
    ├─ lifecycle transition authority in an executed transition
    ├─ lifecycle transition trace reconstruction
    └─ targeted blind-replay prevention

Specification clarification
    ├─ universal lifecycle categories and representation
    ├─ lifecycle invariants
    ├─ applicable transition conditions
    ├─ transition authority
    └─ lifecycle history requirements

Conditional implementation questions
    ├─ suspension support when applicable semantics establish a transition
    └─ termination support when applicable semantics establish a transition
```

## Consequences

No generalized Runtime lifecycle state machine should be implemented solely from the current experiment.

No mandatory `suspend()`, `resume()`, or `terminate()` API should be introduced solely because those method names are absent.

The next engineering task is specification clarification. After that clarification:

1. rerun the implementation ↔ PEM conformance matrix against the clarified requirements;
2. identify concrete applicable lifecycle scenarios;
3. define targeted behavioral validation for those scenarios;
4. classify resulting implementation obligations;
5. implement only confirmed obligations;
6. rerun behavioral validation and preserve the decision/evidence trace.

## Final Decision

The lifecycle experiment establishes a meaningful implementation limitation in demonstrated behavior, but it does **not** justify a blanket confirmed-conformance-gap classification for suspension, resumption, or termination.

The current authoritative conclusion is:

> **Process Instance lifecycle is semantically required and demonstrably separated from Process State, engineering completion, and Runtime lifetime. Concrete lifecycle transition behavior remains dependent on clarified applicable execution semantics. The present prototype therefore contains evidence gaps and implementation prerequisites, with specific implementation defects to be determined only after specification clarification and scenario-based validation.**
