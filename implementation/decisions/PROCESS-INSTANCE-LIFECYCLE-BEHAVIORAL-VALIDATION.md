# Process Instance Lifecycle Behavioral Validation

## Purpose

This document defines the targeted behavioral validation required before implementing the Process Instance lifecycle control contract in Runtime.

It translates the established lifecycle semantics and implementation contract into observable validation scenarios. It does not prescribe implementation APIs, storage technologies, test-framework structure, or internal class design.

## Validation baseline

The validation is governed by:

- the universal Process Instance lifecycle semantics;
- the applicable lifecycle semantics;
- the Process Instance representation decision;
- the Execution Context representation decision; and
- the Process Instance lifecycle control contract.

The validation must distinguish semantic behavior from implementation mechanism.

## Preconditions

Unless a scenario explicitly states otherwise, each test begins with a newly established Process Instance whose lifecycle is `ACTIVE`.

The test harness must be able to establish an applicable lifecycle determination with, where relevant:

- target Process Instance;
- requested transition;
- semantic basis or condition;
- authority context;
- actor/source attribution;
- relevant evidence or conditions; and
- ordering/time information.

The harness must also be able to inspect persisted Process Instance state, persisted Execution Context state, and authoritative history.

## Scenario matrix

| ID | Scenario | Expected result | Purpose |
|---|---|---|---|
| LC-01 | Authorized suspension | `ACTIVE → SUSPENDED` | Establish the basic valid suspension transition. |
| LC-02 | Unauthorized suspension | Lifecycle remains `ACTIVE` | Prove technical mutation capability does not substitute for authority. |
| LC-03 | Suspension persistence | Reloaded instance remains `SUSPENDED` | Prove lifecycle state survives Runtime loss. |
| LC-04 | Suspension preserves continuation state | Context and pending execution remain reconstructable | Prove suspension preserves sufficient authoritative execution state. |
| LC-05 | Recovery does not resume | Recovered instance remains `SUSPENDED` | Prove recovery is distinct from resumption. |
| LC-06 | Resume after valid reevaluation | `SUSPENDED → ACTIVE`, then continuation is permitted | Prove resumption requires current-condition reevaluation. |
| LC-07 | Reevaluation keeps suspension | Lifecycle remains `SUSPENDED` | Prove continuation is blocked while suspension remains applicable. |
| LC-08 | Changed continuation after recovery | Old pending activity is invalidated/replaced when no longer valid | Prevent blind replay of stale work. |
| LC-09 | Active termination | `ACTIVE → TERMINATED` | Establish valid direct termination. |
| LC-10 | Suspended termination | `SUSPENDED → TERMINATED` | Prove termination does not require artificial resumption. |
| LC-11 | Terminality | No transition from `TERMINATED` to `ACTIVE`/`SUSPENDED` | Prove lifecycle finality. |
| LC-12 | Unauthorized termination | Lifecycle remains unchanged | Prove termination authority is enforced. |
| LC-13 | Lifecycle history reconstruction | Full material transition chain is reconstructable | Prove lifecycle traceability independent of current state. |
| LC-14 | Engineering completion separation | Completion does not itself change lifecycle | Preserve distinction between completion and termination. |
| LC-15 | Runtime interruption separation | Runtime stop/replacement does not itself change lifecycle | Preserve distinction between Runtime lifetime and lifecycle. |
| LC-16 | Conflicting conditions | Runtime preserves authoritative state/uncertainty rather than silently choosing an invalid transition | Validate conflict handling. |

## Detailed expected behavior

### Authorized suspension

Given an `ACTIVE` Process Instance and an authorized, applicable suspension determination:

1. the lifecycle transition is validated;
2. lifecycle becomes `SUSPENDED`;
3. authoritative continuation state remains recoverable;
4. further execution is prevented while suspension is authoritative; and
5. the transition is recorded in authoritative history.

### Unauthorized suspension

Given an `ACTIVE` Process Instance and a technically well-formed but unauthorized suspension request, the Runtime must reject or otherwise leave the determination non-authoritative. Lifecycle must remain `ACTIVE` and no false authoritative suspension transition may be recorded.

### Suspension persistence and recovery

After suspension, terminate the Runtime process without making another lifecycle determination. A replacement Runtime must recover the Process Instance as `SUSPENDED`, together with the authoritative Context and suspension basis needed for reevaluation.

Recovery itself must not produce `SUSPENDED → ACTIVE`.

### Valid resumption

After recovery, establish that the suspension condition has changed or ceased and that applicable resumption conditions and authority are satisfied. The Runtime must reevaluate the current situation before transitioning to `ACTIVE`.

Only after valid reevaluation may continuation proceed.

### Continued suspension

If reevaluation establishes that continuation remains impermissible, lifecycle remains `SUSPENDED`. Recovery and reevaluation must not force resumption.

### Changed continuation

If the previously pending activity is no longer valid after suspension, the Runtime must not blindly replay it. The resulting authoritative state must instead invalidate, replace, or otherwise supersede stale continuation information before executing a different permissible activity.

### Termination

For an authorized applicable termination determination:

- `ACTIVE → TERMINATED` is valid;
- `SUSPENDED → TERMINATED` is valid;
- lifecycle becomes persistent and terminal; and
- subsequent recovery may inspect the terminated instance but must not reactivate it.

### Terminality

Any attempted transition from `TERMINATED` to `ACTIVE` or `SUSPENDED` must be rejected or remain non-authoritative. Historical recovery must not be interpreted as lifecycle reactivation.

### Lifecycle history

For each material lifecycle transition, authoritative history must permit reconstruction of:

```text
prior lifecycle state
        ↓
trigger / request / condition
        ↓
authority / actor
        ↓
semantic basis
        ↓
transition identity
        ↓
resulting lifecycle state
        ↓
material consequence
```

A test must verify a multi-transition sequence such as:

```text
ACTIVE → SUSPENDED → ACTIVE → TERMINATED
```

and confirm that all material transitions remain distinguishable and ordered.

### Completion separation

Establish engineering completion while the Process Instance is `ACTIVE`. Unless a separate applicable lifecycle determination exists, lifecycle must remain `ACTIVE`.

### Runtime interruption separation

Call Runtime stop/detach or replace the Runtime without issuing a lifecycle determination. The Process Instance lifecycle must remain unchanged.

## Test oracle

A scenario passes only when the observable authoritative state satisfies all applicable expectations. The test must not infer semantic success from the existence of a method, field, or internal flag alone.

The primary oracle is:

```text
Persisted authoritative state
        +
Persisted authoritative history
        +
Observable execution behavior
        ↓
Expected semantic outcome
```

## Evidence classification

Each executed scenario must record:

- scenario identifier;
- initial authoritative state;
- lifecycle determination used;
- authority result;
- observed lifecycle before and after the operation;
- relevant Context state before and after;
- execution behavior observed;
- persisted state after Runtime restart where applicable;
- history entries observed;
- pass/fail result;
- evidence artifact or reproducible test reference.

A test that cannot execute because the Runtime lacks the required capability is evidence of an implementation gap only when the applicable semantic obligation is already established.

## Implementation boundary

This validation specification intentionally does not require particular method names such as `suspend()`, `resume()`, or `terminate()`. Tests should exercise the externally meaningful lifecycle determination/control behavior through the smallest interface the implementation provides.

If the current Runtime exposes no mechanism to perform a required scenario, the missing capability must first be recorded as the expected failure. The test specification must not be weakened merely to fit the existing prototype.

## Execution order

The validation should be executed in this order:

1. lifecycle representation and basic valid transitions;
2. authority rejection;
3. persistence and recovery;
4. reevaluation and resumption;
5. stale continuation protection;
6. termination and terminality;
7. trace reconstruction;
8. separation from completion and Runtime interruption;
9. conflict handling.

The ordering is for efficient evidence gathering only and does not define a semantic phase model.

## Decision

**ADOPT this scenario set as the targeted behavioral validation contract for Process Instance lifecycle control.**

No Runtime production implementation is changed by this document. The next implementation activity is to map each scenario to the existing test harness and identify the smallest test additions required to expose the currently expected failures before changing Runtime behavior.
