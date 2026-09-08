# Process Instance Lifecycle Conformance Finding Reconciliation

## Purpose

This document reconciles the empirical findings of the controlled Process Instance lifecycle validation with the **current** AESM/PEM lifecycle semantics.

Its purpose is to determine which observed implementation absences are:

- validated semantic boundaries;
- specification precision gaps;
- evidence gaps;
- confirmed implementation/conformance gaps; or
- conditional implementation questions whose obligations depend on applicable execution semantics.

This document does not authorize Runtime implementation changes.

## Baseline

The reconciliation uses the following evidence:

- lifecycle validation experiment at commit `7273f2e9535436310e0df22c01800e172d848bb4`;
- lifecycle semantics reassessment;
- Process Instance lifecycle semantics decision;
- current `docs/04-Execution-Model.md`;
- current `docs/05-Process-Instance-and-Execution-Context.md`;
- current `docs/07-Runtime-and-Conformance.md`;
- current lifecycle conformance matrix.

The governing model decision is:

> Process Instance lifecycle is a universal AESM/PEM semantic dimension, while concrete lifecycle transition conditions and scenario-specific triggers are established by applicable execution semantics.

The current normative documents now explicitly define the universal lifecycle vocabulary `ACTIVE`, `SUSPENDED`, and `TERMINATED`, their universal meaning and invariants, the legal universal transition structure, lifecycle separation, recovery/resumption distinction, and lifecycle traceability requirements. Concrete triggers, authority rules, and scenario-specific transition conditions remain applicable-semantics dependent. fileciteturn7file0L2-L2 fileciteturn8file0L2-L2

## Reconciliation Principle

An implementation observation is not a conformance defect merely because a mechanism or method name is absent.

The classification order is:

```text
Semantic requirement exists
        ↓
Requirement is sufficiently precise
        ↓
Expected semantic behavior is derivable
        ↓
Applicable transition conditions exist
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
| `ACTIVE` lifecycle state is persisted and recovered | Demonstrated | Lifecycle condition is authoritative recoverable operational state | **Demonstrated for observed state; transition persistence remains untested** |
| Universal lifecycle vocabulary is now specified | Specification clarified | Current normative documents define `ACTIVE`, `SUSPENDED`, and `TERMINATED` | **Specification requirement established** |
| No `suspend()` or equivalent API | Established implementation fact | AESM does not prescribe an API; suspension requires an applicable condition and authorized semantic transition | **Evidence gap / conditional implementation question** |
| No `resume()` or equivalent API | Established implementation fact | Resumption is a semantic capability, not a required method name; recovery alone does not demonstrate resumption | **Evidence gap** |
| No `terminate()` or equivalent API | Established implementation fact | Termination is semantically defined, but a concrete transition obligation requires an applicable termination condition | **Conditional implementation question** |
| No lifecycle mutation path in Runtime | Established implementation fact | No lifecycle transition can currently be exercised by the prototype | **Evidence gap for transition behavior; not independently a defect** |
| No ProcessInstance update persistence mechanism | Established implementation fact | A mutable lifecycle persistence path becomes necessary if an applicable lifecycle transition must be executed | **Structural implementation prerequisite** |
| No lifecycle-specific history events | Established implementation fact | Material lifecycle transitions require reconstructable history when such transitions occur | **Traceability implementation prerequisite** |
| No general lifecycle authorization mechanism | Established implementation fact | Concrete authority rules are applicable-semantics dependent | **Specification/application-dependent evidence gap** |
| Pending execution survives Runtime replacement | Demonstrated | Pending work is authoritative continuation information | **Demonstrated conformance for persistence** |
| Pending execution is not shown being reevaluated and resumed | Not demonstrated | Resumption requires reevaluation before continuation | **Evidence gap** |
| Cross-Runtime recovery succeeds | Demonstrated | Recovery is distinct from resumption and supports continuity | **Demonstrated recovery / continuity** |
| Cross-process/environment replacement was not directly exercised | Not demonstrated | The experiment does not fully establish environment-independent replacement behavior | **Evidence limitation** |

## Confirmed Semantic/Conformance Findings

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

### The universal lifecycle vocabulary is no longer a specification gap

The current normative documents explicitly define `ACTIVE`, `SUSPENDED`, and `TERMINATED`, including their meanings and universal transition structure. The earlier reassessment's conclusion that the vocabulary remained unspecified is therefore superseded by the later specification clarification. fileciteturn8file0L2-L2

The remaining semantic uncertainty concerns **when** concrete lifecycle transitions are applicable, not what the universal lifecycle categories mean.

## Current Specification Status

The lifecycle semantics decision has now been operationalized in the current specification set.

The specification establishes:

- Process Instance lifecycle as a universal semantic dimension;
- lifecycle distinction from Process State, engineering completion, Runtime lifetime, Agent/session lifetime, and Execution Environment lifetime;
- universal lifecycle states `ACTIVE`, `SUSPENDED`, and `TERMINATED`;
- universal transition structure and terminality;
- authoritative persistence and recovery of lifecycle state;
- suspension preservation requirements;
- resumption as reevaluation followed by permissible continuation;
- termination as distinct from Runtime termination and engineering completion;
- lifecycle transition traceability requirements;
- implementation independence of API/storage choices.

The specification leaves these items applicable-semantics dependent:

- concrete suspension triggers;
- concrete resumption conditions;
- concrete termination triggers;
- transition authority details for a particular execution scenario;
- scenario-specific consequences and preconditions.

Accordingly, the previous blanket label **"specification precision gap"** is no longer appropriate for the universal lifecycle model. The open work is now to identify or define applicable execution semantics that make concrete lifecycle transitions testable.

## Conditional Implementation Findings

### Suspension

The absence of a suspension mechanism cannot currently be classified as a confirmed defect in isolation.

A confirmed implementation gap requires an applicable execution scenario that establishes a valid suspension condition and therefore creates a concrete Runtime obligation.

Once such a condition exists, the Runtime must provide the semantic capability to preserve authoritative continuation state and establish `SUSPENDED` without conflating suspension with Runtime shutdown.

### Resumption

The Runtime must support semantic continuation where applicable, including recovery, reevaluation, and controlled continuation. A named `resume()` API is not required unless an applicable implementation contract prescribes one.

The current experiment does not demonstrate that complete semantic behavior.

This is currently an **evidence gap**, not a confirmed API-level defect.

### Termination

Process Instance termination is now a defined universal lifecycle category and is terminal. However, the concrete termination condition, authority, and scenario-specific trigger remain applicable-semantics dependent.

Therefore the absence of a termination API is a **conditional implementation question**, not a confirmed defect at the current abstraction level.

If an applicable scenario establishes a valid termination condition, the Runtime must then demonstrate the corresponding `TERMINATED` transition, persistence, traceability, authority handling, and prevention of reactivation as the same lifecycle instance.

## Lifecycle Persistence and History

The experiment established that the current implementation can persist and recover the observed `ACTIVE` lifecycle state. It also established that Process Instance persistence is effectively write-once and that current history contains Process State/execution events rather than lifecycle transition events.

These are valid implementation facts.

Their conformance interpretation is conditional on whether a lifecycle transition is actually required and executed:

- current `ACTIVE` preservation satisfies the evidence available for the observed state;
- a future lifecycle transition requires a durable mutation path for lifecycle state;
- a material lifecycle transition requires history sufficient to reconstruct prior and resulting lifecycle states, transition identity/equivalent reference, sequence/time, authority where applicable, semantic basis, relevant conditions/evidence, and material consequences.

Thus the lack of lifecycle history events is not a failed record of a transition that never occurred, but it is a **clear implementation prerequisite for any future material lifecycle transition**.

## Final Classification

The lifecycle experiment should now be summarized as follows:

```text
Validated semantic boundaries
    ├─ Runtime lifetime ≠ Process Instance lifecycle
    ├─ Process Instance lifecycle ≠ EPM Process State
    └─ engineering completion ≠ lifecycle termination

Demonstrated capabilities
    ├─ ACTIVE lifecycle representation at creation
    ├─ ACTIVE lifecycle persistence/recovery
    ├─ Process Instance continuity across Runtime replacement
    └─ pending execution persistence/recovery

Evidence gaps
    ├─ actual suspension transition
    ├─ semantic resumption and reevaluation
    ├─ lifecycle transition authority in an executed transition
    ├─ lifecycle transition trace reconstruction
    └─ targeted blind-replay prevention

Applicable-semantics work
    ├─ identify concrete suspension conditions
    ├─ identify concrete resumption conditions
    └─ identify concrete termination conditions

Conditional implementation questions
    ├─ lifecycle mutation/persistence support when a transition is required
    ├─ suspension support when a suspension condition is applicable
    └─ termination support when a termination condition is applicable
```

## Consequences

No generalized Runtime lifecycle implementation should be added solely from the original experiment.

No mandatory `suspend()`, `resume()`, or `terminate()` API should be introduced solely because those method names are absent.

The next engineering work is now **applicable lifecycle semantics and conformance reassessment**, not another broad lifecycle implementation experiment.

The intended sequence is:

```text
Current lifecycle specification
        ↓
Identify concrete applicable lifecycle semantics
        ↓
Rerun implementation ↔ PEM conformance matrix
        ↓
Define targeted behavioral scenarios
        ↓
Classify confirmed implementation obligations
        ↓
Implement only confirmed obligations
        ↓
Re-validate behavior and traceability
```

## Final Decision

> **Process Instance lifecycle is semantically required and its universal categories and invariants are now specified. The experiment demonstrates correct separation from Process State, engineering completion, and Runtime lifetime, as well as basic lifecycle persistence/recovery. Suspension, resumption, and termination remain unproven behaviorally because the experiment did not establish concrete applicable transition conditions. Specific implementation defects must therefore be determined only after applicable lifecycle semantics make those transitions testable.**
