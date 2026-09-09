# Controlled Applicable Process Instance Lifecycle Scenarios

## Purpose

This document defines controlled, scenario-specific lifecycle conditions that make the universal Process Instance lifecycle semantics behaviorally testable without turning a test trigger into a universal AESM lifecycle policy.

It bridges the current semantic specification and targeted Runtime validation.

The scenarios are validation semantics, not new universal lifecycle rules.

## Governing boundary

```text
Universal AESM/PEM lifecycle semantics
        ↓
Controlled applicable validation semantics
        ↓
Expected Runtime behavior
        ↓
Behavioral evidence
```

The controlled scenarios establish an applicable condition for the purpose of validation. They do not prescribe that every AESM deployment must use the same external trigger, actor, interface, or operational policy.

No lifecycle API name is required by these scenarios.

## Applicability model

For validation, an external **lifecycle determination** is treated as an input to the execution semantics. The determination contains:

- target Process Instance identity;
- requested lifecycle transition;
- semantic basis/condition;
- authority context;
- actor or source attribution where applicable;
- relevant evidence/conditions;
- ordering/time information.

The Runtime must not treat technical receipt of the determination as sufficient authority. It must apply the applicable authority and lifecycle rules before authoritative mutation.

This permits validation of lifecycle semantics without assuming that a production Runtime must expose `suspend()`, `resume()`, or `terminate()` methods.

## Controlled suspension scenario

### Applicability condition

The test establishes an authorized condition stating:

> Continued execution of the selected Process Instance is presently impermissible, while the Process Instance remains extant and eligible for possible future continuation.

The test explicitly establishes that termination has not been determined.

### Required transition

```text
ACTIVE → SUSPENDED
```

### Required behavior

The Runtime must:

1. recognize the applicable suspension determination;
2. validate its authority and conditions;
3. preserve the authoritative Execution Context required for later reevaluation;
4. persist the lifecycle state as `SUSPENDED`;
5. preserve the suspension basis and material transition evidence; and
6. prevent continued execution while the suspension condition remains authoritative.

Runtime shutdown is not used as the semantic suspension trigger.

### Negative control

A lifecycle determination lacking the required authority must not mutate `ACTIVE` to `SUSPENDED`.

## Controlled recovery/resumption scenario

### Starting condition

The controlled suspension scenario has established a persisted `SUSPENDED` Process Instance with:

- pending execution information;
- current Process State;
- suspension basis;
- relevant requirements/constraints;
- sufficient traceability.

### Recovery condition

A new Runtime instance reconstructs the Process Instance and Execution Context.

Recovery alone must leave the lifecycle state `SUSPENDED` and must not begin execution.

### Material change

Before resumption is authorized, the test changes at least one material condition relevant to continuation. Examples include:

- a requirement or constraint changes;
- pending work becomes invalid;
- a Decision Gate outcome changes;
- verification information changes; or
- an unresolved condition is resolved or newly introduced.

The particular changed condition is test-defined; the requirement is that it materially affects whether the previously expected continuation remains permissible.

### Reevaluation

The Runtime must reevaluate the recovered executable situation against current authoritative state and applicable EPM/PEM conditions.

Persisted continuation information is evidence about expected continuation, not an imperative command to replay stale work.

### Required outcomes

The test must establish at least these outcomes across controlled cases:

1. **Resume:** reevaluation permits continuation, producing `SUSPENDED → ACTIVE` and valid continuation.
2. **Remain suspended:** reevaluation determines that continuation is still impermissible, leaving the instance `SUSPENDED`.
3. **Changed continuation:** reevaluation invalidates the old pending activity but establishes another permissible activity; the Runtime must not blindly replay the old activity.

A termination outcome may be tested separately under the termination scenario below.

## Controlled termination scenario

### Applicability condition

The test establishes an authorized condition stating:

> The Process Instance must no longer continue as the same lifecycle instance.

The condition is explicit enough to distinguish termination from temporary suspension, Runtime shutdown, action failure, verification failure, and engineering completion.

### Required transitions

Two starting states are validated independently:

```text
ACTIVE   → TERMINATED
SUSPENDED → TERMINATED
```

The suspended case must not require an artificial intermediate resumption.

### Required behavior

The Runtime must:

1. recognize the applicable termination determination;
2. validate authority and conditions;
3. establish `TERMINATED` as authoritative lifecycle state;
4. persist the terminal state consistently with the required Execution Context;
5. record sufficient transition history; and
6. prevent the same lifecycle instance from returning to `ACTIVE` or `SUSPENDED`.

Historical recovery remains permitted for audit, traceability, reconsideration, or other applicable purposes, but historical recovery must not reactivate the lifecycle instance.

### Negative control

A termination determination lacking required authority must not mutate the lifecycle state.

## Completion-separation scenario

Engineering completion is intentionally exercised independently from lifecycle termination.

The test must demonstrate at least one case in which engineering completion is established while the lifecycle remains `ACTIVE` or `SUSPENDED`, unless a separate applicable execution rule explicitly requires immediate termination.

This scenario preserves the mandatory distinction:

```text
Engineering completion ≠ Process Instance termination
```

## Runtime interruption scenario

Runtime interruption is deliberately kept separate from lifecycle control.

The test performs Runtime stop, replacement, or equivalent interruption without supplying a lifecycle determination.

Expected result:

- Runtime lifetime changes;
- Process Instance lifecycle does not change merely because Runtime stopped;
- supported authoritative state remains recoverable; and
- recovery does not become semantic resumption unless a valid resumption determination and reevaluation occur.

This scenario extends the already demonstrated lifecycle/Runtime separation evidence rather than redefining suspension.

## Lifecycle traceability scenario

After executing lifecycle transitions, the validator must reconstruct history without relying solely on the current lifecycle field.

For each material transition, the reconstruction must establish, where applicable:

```text
prior lifecycle state
        ↓
trigger / request / condition
        ↓
authority / actor
        ↓
applicable semantic basis
        ↓
transition identity
        ↓
resulting lifecycle state
        ↓
material consequence
```

The history must remain reconstructable after a later transition. For example:

```text
ACTIVE
  ↓ suspend
SUSPENDED
  ↓ resume
ACTIVE
  ↓ terminate
TERMINATED
```

must retain evidence of the earlier suspension and resumption rather than only the final `TERMINATED` state.

## Scenario independence

These controlled scenarios intentionally do not establish:

- a universal human-only lifecycle controller;
- a universal Agent-only lifecycle controller;
- a particular UI;
- a particular protocol;
- a particular API;
- a particular persistence technology;
- a universal production suspension trigger;
- a universal production termination trigger; or
- a universal rule connecting engineering completion to termination.

A concrete deployment may realize the applicable conditions through different mechanisms while remaining semantically conformant.

## Expected conformance consequences

Once these controlled scenarios are accepted as applicable validation semantics:

- suspension and termination become testable semantic obligations;
- absence of a lifecycle API can no longer be used as a reason to defer the behavioral test;
- the Runtime can be evaluated for an actual implementation gap;
- lifecycle mutation/persistence becomes a concrete implementation concern if the Runtime cannot realize the required transitions;
- lifecycle history becomes a concrete implementation concern when a material transition is executed; and
- resumption can be tested for reevaluation and blind-replay prevention.

A failed scenario must be classified only after the Runtime behavior and evidence are compared with the required semantic behavior.

## Validation sequence

```text
Controlled applicable condition
        ↓
Lifecycle determination
        ↓
Authority/condition evaluation
        ↓
Authoritative lifecycle mutation
        ↓
Persistence and recovery
        ↓
Behavioral observation
        ↓
Trace reconstruction
        ↓
Conformance classification
```

## Decision

> **The universal lifecycle semantics remain implementation-independent, while controlled applicable validation semantics now provide concrete, testable suspension, resumption, and termination conditions. These scenarios are sufficient to proceed to targeted behavioral validation without prematurely imposing domain-specific lifecycle policy on AESM.**

## Next work

The next work item is targeted behavioral validation using these controlled scenarios. Runtime implementation changes must wait for the resulting evidence and conformance classification.
