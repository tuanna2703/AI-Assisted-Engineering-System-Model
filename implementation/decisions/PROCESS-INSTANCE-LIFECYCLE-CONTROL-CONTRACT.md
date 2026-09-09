# Process Instance Lifecycle Control Contract

## Purpose

This document defines the minimum implementation contract required for a Runtime to satisfy the currently applicable Process Instance lifecycle semantics.

It translates established lifecycle semantics into implementation obligations without introducing new lifecycle meaning or prescribing a specific API, storage technology, transaction mechanism, or programming language.

This contract is the implementation boundary between the applicable lifecycle specification and targeted Runtime changes.

## Semantic Sources

The contract is derived from:

- the universal Process Instance lifecycle model;
- the applicable Process Instance lifecycle semantics;
- the existing Process Instance representation decision;
- the existing Execution Context representation decision; and
- the controlled applicable lifecycle scenarios and conformance assessment.

The applicable lifecycle specification remains authoritative for semantic meaning. This document specifies only the minimum implementation behavior needed to realize that meaning in the current Runtime.

## Lifecycle State Set

The Runtime must represent the canonical lifecycle states:

```text
ACTIVE
SUSPENDED
TERMINATED
```

A newly created Process Instance is `ACTIVE` unless an applicable execution rule explicitly establishes another initial condition.

Lifecycle state is distinct from:

- EPM Process State;
- engineering completion;
- Runtime lifetime;
- Agent or conversation lifetime; and
- Execution Environment lifetime.

## Authoritative Mutation Boundary

Lifecycle state must not be changed through arbitrary field assignment by unrelated Runtime operations.

A lifecycle transition is a controlled state mutation with the following conceptual boundary:

```text
Lifecycle determination
        ↓
Authority validation
        ↓
Semantic/precondition validation
        ↓
State transition validation
        ↓
Authoritative persistence
        ↓
Lifecycle trace recording
```

The contract does not require this exact call sequence to be implemented as separate functions. It requires the observable semantics represented by the sequence.

## Lifecycle Determination Input

A lifecycle mutation must be based on an explicit lifecycle determination rather than inferred solely from Runtime behavior.

A determination must be capable of expressing, as applicable:

- target Process Instance;
- requested lifecycle transition;
- semantic basis or applicable condition;
- authority context;
- actor or source attribution;
- relevant evidence or conditions;
- ordering or timestamp information.

A request or proposal is not itself authorization. Technical ability to mutate stored state is not itself authorization.

## Validation Rules

Before applying a lifecycle transition, the Runtime must establish:

1. the target Process Instance is the intended instance;
2. the requested transition is legal from the current lifecycle state;
3. the applicable lifecycle condition is established;
4. the required authority is present;
5. material conflicts are resolved or preserved as uncertainty rather than silently overridden;
6. termination finality is respected; and
7. the resulting authoritative state can be persisted consistently with its required traceability evidence.

Unauthorized or semantically invalid lifecycle determinations must not mutate authoritative lifecycle state.

## Legal Transitions

The minimum legal lifecycle transitions are:

```text
ACTIVE → SUSPENDED
SUSPENDED → ACTIVE
ACTIVE → TERMINATED
SUSPENDED → TERMINATED
```

The following are invalid:

```text
TERMINATED → ACTIVE
TERMINATED → SUSPENDED
```

Termination is therefore terminal for the same lifecycle instance.

No other lifecycle transition is required by this contract unless a later applicable semantic decision establishes one.

## Suspension Contract

A valid suspension requires an applicable condition establishing that continuation is presently impermissible while the Process Instance remains extant and termination has not been established.

On successful `ACTIVE → SUSPENDED`, the Runtime must:

- persist `SUSPENDED` as authoritative lifecycle state;
- preserve the Execution Context required for later reevaluation;
- preserve pending execution and interruption information where applicable;
- preserve the suspension basis, authority, and material evidence required to interpret the suspension;
- prevent further execution while the suspension remains authoritative; and
- record a reconstructable lifecycle transition.

Suspension must not automatically:

- change EPM Process State;
- mark engineering work complete;
- terminate the Runtime;
- terminate an Agent or conversation; or
- terminate the Execution Environment.

## Recovery and Resumption Contract

Recovery of a suspended Process Instance must reconstruct its authoritative state while leaving lifecycle state `SUSPENDED`.

Recovery is not resumption.

Before `SUSPENDED → ACTIVE`, the Runtime must reevaluate the current executable situation against current authoritative state and applicable conditions.

The reevaluation must consider, where applicable:

- the suspension condition;
- current Process State;
- pending execution;
- resumption conditions;
- requirements and constraints;
- verification state;
- failures and uncertainty;
- changes since suspension;
- authority; and
- Decision Gates.

The reevaluation may establish:

1. permissible continuation of the existing pending activity;
2. a different permissible activity;
3. continued suspension; or
4. another applicable condition, including authorized termination.

Persisted continuation information is an expected continuation point, not an imperative instruction to replay a previous Runtime operation.

The Runtime must not blindly replay stale, invalid, or contradictory pending work.

## Termination Contract

Termination requires an applicable termination condition and the required authority.

The Runtime must support both:

```text
ACTIVE → TERMINATED
SUSPENDED → TERMINATED
```

On successful termination, the Runtime must:

- persist `TERMINATED` as authoritative lifecycle state;
- record the termination basis, authority, and material evidence required to interpret it;
- record a reconstructable lifecycle transition; and
- prevent any subsequent transition of the same lifecycle instance back to `ACTIVE` or `SUSPENDED`.

Historical recovery remains permissible for audit, traceability, or other allowed purposes, but must never reactivate the terminated lifecycle instance.

## Persistence Contract

Lifecycle state must be durable and recoverable independently of transient Runtime memory, Agent memory, conversation history, IDE/session state, or Execution Environment state.

The current implementation stores lifecycle on the Process Instance representation. The implementation may retain that physical representation, but it must provide a durable update path for lifecycle transitions after Process Instance creation.

The lifecycle state and the material state required to interpret the transition must not be exposed as an impossible partial mutation after recovery.

The implementation must therefore establish a consistency boundary between:

- the authoritative lifecycle state;
- any material Execution Context changes required by the transition; and
- the lifecycle transition trace.

The exact mechanism for achieving that boundary is implementation-defined.

## Lifecycle and Execution Context Representation

The semantic specification treats lifecycle as part of the authoritative operational state. The current prototype physically represents `lifecycle` on `ProcessInstance` while the `ExecutionContext` contains the operational state associated with that instance.

This contract does not require an immediate data-model relocation.

For the current implementation, the minimum invariant is:

> A recovered Process Instance and its Execution Context must present one semantically consistent lifecycle state and sufficient associated context to interpret that state.

If later implementation evidence demonstrates that the current physical placement cannot maintain this invariant reliably, the representation may be adapted through a separate implementation decision. Such adaptation must not alter the established lifecycle semantics.

## Lifecycle Trace Contract

Every material lifecycle transition must be reconstructable independently from the current lifecycle field.

The recorded transition must establish, where applicable:

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

At minimum, the trace must permit reconstruction of:

- prior lifecycle state;
- resulting lifecycle state;
- unique transition identity or equivalent reference;
- ordering or timestamp;
- recognized trigger, request, or condition;
- authority or actor attribution where applicable;
- applicable EPM/PEM/execution basis;
- relevant evidence or conditions used for the determination; and
- material consequence for continuation or termination.

The implementation may use the existing history mechanism or another mechanism; event sourcing is not required.

## Runtime Lifetime Boundary

Runtime shutdown, `stop()`, replacement, process exit, IDE closure, conversation closure, Agent departure, or Execution Environment loss must not change Process Instance lifecycle by implication.

Only an explicit applicable lifecycle determination may establish suspension or termination.

Likewise, Runtime startup or recovery must not change `SUSPENDED` to `ACTIVE` merely because the Runtime can continue executing.

## Completion Boundary

Engineering completion does not imply lifecycle termination under this contract.

A separate applicable rule may establish termination after completion, but that relationship must be explicit and independently validated.

Therefore:

```text
engineering completion
        ≠
Process Instance termination
```

## Required Behavioral Verification

The Runtime implementation must eventually demonstrate at least the following behaviors:

### Suspension

- authorized `ACTIVE → SUSPENDED` succeeds;
- unauthorized suspension does not mutate lifecycle;
- suspension persists across Runtime replacement;
- suspended execution is not continued while suspension is authoritative.

### Recovery and resumption

- recovery of `SUSPENDED` leaves it suspended;
- reevaluation occurs before resumption;
- valid reevaluation can establish `SUSPENDED → ACTIVE`;
- failed or insufficient reevaluation leaves the instance suspended;
- changed conditions can establish a different valid continuation;
- stale pending execution is not blindly replayed.

### Termination

- authorized `ACTIVE → TERMINATED` succeeds;
- authorized `SUSPENDED → TERMINATED` succeeds;
- unauthorized termination does not mutate lifecycle;
- `TERMINATED` remains terminal across recovery;
- attempts to reactivate a terminated instance are rejected.

### Separation and traceability

- Runtime shutdown does not alter lifecycle;
- engineering completion does not automatically terminate lifecycle;
- lifecycle transitions remain reconstructable from authoritative history;
- lifecycle state and associated context remain semantically consistent after recovery.

## Implementation Constraints

This contract does not prescribe:

- method names such as `suspend()`, `resume()`, or `terminate()`;
- class or module structure;
- database technology;
- schema details;
- event sourcing;
- locking strategy;
- serialization format;
- programming language;
- user interface; or
- execution environment.

The implementation should add only the minimum machinery required to satisfy the established semantic obligations.

## Implementation Sequence

The recommended implementation sequence is:

```text
Lifecycle control contract
        ↓
Targeted behavioral tests
        ↓
Minimal Runtime/store changes
        ↓
Execute lifecycle validation
        ↓
Classify observed evidence
        ↓
Update conformance assessment
```

Tests should be written against semantic outcomes rather than against an arbitrary API shape wherever practical.

## Decision

**ADOPT this document as the minimum implementation contract for Process Instance lifecycle control.**

The next implementation work should establish the smallest Runtime and persistence changes capable of satisfying this contract, with targeted behavioral tests providing the evidence for each obligation.
