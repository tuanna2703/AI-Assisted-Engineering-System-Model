# AESM Lifecycle Conformance Matrix

## Purpose

This matrix translates the Lifecycle Semantic Decision Record into observable conformance criteria for targeted behavioral validation.

It does not prescribe APIs, storage schemas, database technology, event sourcing, locking, or other implementation mechanisms.

## Evidence status

The prior lifecycle behavioral experiment established useful continuity and recovery evidence, but it did not demonstrate the complete semantic requirements for suspension, resumption, termination, or lifecycle traceability. Existing recovery evidence therefore remains limited to the semantics it actually demonstrates.

## Conformance criteria

| ID | Semantic requirement | Observable criterion | Existing evidence | Status |
|---|---|---|---|---|
| LC-01 | Canonical lifecycle state | Current Process Instance lifecycle state is explicitly recoverable and distinguishable from Process State and engineering completion. | Existing lifecycle/recovery evidence establishes separation conceptually; canonical state behavior not directly tested. | Pending validation |
| LC-02 | Lifecycle persistence | Lifecycle state survives supported Runtime/process interruption and is recovered from authoritative state. | Recovery experiment demonstrated authoritative continuity, but not all lifecycle states. | Partial evidence |
| LC-03 | Suspension semantics | A valid suspension trigger produces `ACTIVE → SUSPENDED` and preserves sufficient authoritative continuation state. | No complete behavioral demonstration. | Pending validation |
| LC-04 | Suspension authority | An unauthorized suspension request/event does not mutate authoritative lifecycle state. | Not demonstrated. | Pending validation |
| LC-05 | Suspension preservation | After suspension, current Process State, pending work, unresolved conditions, verification state, material failure/uncertainty, and relevant traceability remain sufficient for safe continuation. | Not demonstrated as a lifecycle-specific scenario. | Pending validation |
| LC-06 | Resumption is distinct from recovery | Recovering a `SUSPENDED` instance does not by itself return it to executable active lifecycle state. | Existing recovery evidence demonstrates recovery/continuation separation conceptually; suspended-state behavior not tested. | Pending validation |
| LC-07 | Resumption reevaluation | Recovered conditions are reevaluated against current authoritative state and applicable EPM/PEM conditions before continuation. | Existing cross-Runtime recovery test provides continuity/recovery evidence but not complete reevaluation evidence. | Pending validation |
| LC-08 | Resumption safety | Stale or invalid pending work is not blindly replayed after recovery. | Existing evidence supports the conceptual boundary; targeted stale-work scenario required. | Pending validation |
| LC-09 | Resumption outcome | Reevaluation can result in continuation, different permissible activity, continued suspension, another applicable condition, or authorized termination. | Not demonstrated. | Pending validation |
| LC-10 | Termination semantics | A valid termination condition produces `TERMINATED`. | Not demonstrated. | Pending validation |
| LC-11 | Termination authority | An unauthorized termination request/event does not mutate authoritative lifecycle state. | Not demonstrated. | Pending validation |
| LC-12 | Termination finality | A terminated Process Instance cannot resume as the same lifecycle instance. | Not demonstrated. | Pending validation |
| LC-13 | Completion separation | Engineering completion and Process Instance termination are independently observable. | Existing documentation establishes the distinction; behavioral separation not demonstrated. | Pending validation |
| LC-14 | Lifecycle transition consistency | A lifecycle transition is recovered as a semantically consistent authoritative mutation rather than a partial state. | General mutation consistency evidence exists; lifecycle-specific transition scenario not demonstrated. | Pending validation |
| LC-15 | Lifecycle traceability | Material lifecycle transitions can be reconstructed independently from current lifecycle state. | Existing traceability evidence does not demonstrate lifecycle transition reconstruction. | Pending validation |
| LC-16 | Transition attribution | Transition basis and authority/actor information are reconstructable where applicable. | Not demonstrated. | Pending validation |
| LC-17 | Lifecycle separation from Runtime | Runtime startup, restart, failure, replacement, or termination does not itself imply lifecycle termination or suspension unless applicable semantics explicitly establish it. | Existing continuity/restart evidence supports separation from Runtime lifetime. | Partial evidence |
| LC-18 | Lifecycle separation from Agent/Environment | Agent departure, conversation closure, IDE closure, or environment replacement does not itself imply lifecycle termination unless applicable semantics explicitly establish it. | Existing continuity evidence supports the boundary. | Partial evidence |
| LC-19 | Terminal transition graph | `TERMINATED → ACTIVE` and `TERMINATED → SUSPENDED` cannot occur for the same lifecycle instance. | Not demonstrated. | Pending validation |
| LC-20 | Implementation independence | Conformance evidence demonstrates semantic behavior without relying on a mandated lifecycle API or storage mechanism. | Specification-level requirement only. | Pending validation |

## Evidence classification

Use these classifications consistently:

- **Demonstrated** — direct behavioral evidence establishes the criterion.
- **Partial evidence** — related evidence supports part of the criterion but does not establish the complete requirement.
- **Not demonstrated** — the criterion is defined but no adequate behavioral evidence currently establishes it.
- **Failed** — direct behavioral evidence contradicts the criterion.
- **Not applicable** — the criterion is genuinely outside the applicable execution semantics for the tested scenario; the reason must be recorded.

Absence of evidence must not be classified as Runtime non-conformance without a defined applicable requirement and an adequate test.

## Targeted validation mapping

### Suspension validation

```text
Authorized trigger
      ↓
ACTIVE → SUSPENDED
      ↓
Preserve authoritative state
      ↓
Persist lifecycle transition
      ↓
Recover independently
      ↓
Verify suspended condition and preserved continuation state
      ↓
Reconstruct transition history
```

### Resumption validation

```text
SUSPENDED
      ↓
Recover authoritative state
      ↓
Remain non-executing until reevaluation
      ↓
Observe current situation
      ↓
Evaluate current EPM/PEM conditions
      ↓
Validate pending execution / next expected action
      ↓
Determine permissible continuation
      ↓
Resume ACTIVE execution only when permitted
```

At least one scenario should introduce a material change after suspension so that blind replay can be distinguished from genuine reevaluation.

### Termination validation

```text
ACTIVE or SUSPENDED
      ↓
Authorized termination condition
      ↓
TERMINATED
      ↓
Persist terminal state
      ↓
Recover historical state
      ↓
Verify no same-instance resumption
```

A separate unauthorized-request scenario should demonstrate that a termination request without applicable authority does not mutate lifecycle state.

### Lifecycle traceability validation

The validator should reconstruct lifecycle history using historical evidence rather than reading only the current lifecycle state.

The reconstructed history should establish, where applicable:

```text
prior state
    ↓
trigger/request/condition
    ↓
authority/actor
    ↓
semantic basis
    ↓
transition
    ↓
resulting state
    ↓
material consequence
```

The reconstruction must remain possible after subsequent lifecycle changes.

## Current conclusion

The lifecycle semantic baseline is now sufficiently explicit to define behavioral tests without prescribing Runtime APIs.

The next experiment should therefore target LC-03 through LC-19, with the existing cross-Runtime continuity experiment retained as supporting evidence for LC-02, LC-06, LC-07, LC-08, LC-17, and LC-18 only to the extent its actual observations support those criteria.

Runtime implementation changes remain out of scope until the targeted validation produces evidence of a confirmed conformance gap.
