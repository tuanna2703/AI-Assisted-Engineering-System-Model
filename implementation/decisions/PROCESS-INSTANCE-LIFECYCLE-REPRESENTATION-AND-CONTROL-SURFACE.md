# Process Instance Lifecycle Representation and Control Surface Decision

## Status

**ADOPTED**

## Purpose

This document records the implementation decision for representing Process Instance lifecycle state and exposing its authoritative Runtime control boundary in the current AESM prototype.

It translates the established lifecycle semantics and lifecycle control contract into a small implementation decision. It does not introduce new lifecycle meaning and does not modify the frozen normative AESM documents.

## Decision Summary

The current implementation will:

1. retain `lifecycle` on `ProcessInstance` as the physical representation of the current Process Instance lifecycle state;
2. use canonical lowercase strings for the persisted/code values:
   - `active`
   - `suspended`
   - `terminated`
3. treat the normative uppercase names `ACTIVE`, `SUSPENDED`, and `TERMINATED` as semantic identifiers, not as required serialized literals;
4. centralize lifecycle mutation behind one authoritative public Runtime control surface that accepts a lifecycle determination;
5. validate the determination against the current authoritative Process Instance and applicable lifecycle semantics before mutation;
6. persist the resulting lifecycle state together with the material Execution Context consequence and lifecycle trace through the authoritative persistence boundary; and
7. leave API names, internal helper decomposition, transaction technology, and storage schema details implementation-specific except where this decision explicitly constrains them.

## Semantic State Set

The semantic state set is fixed by the applicable lifecycle semantics:

```text
ACTIVE
SUSPENDED
TERMINATED
```

The implementation maps these semantic states to canonical persisted values:

| Semantic state | Canonical implementation value |
|---|---|
| `ACTIVE` | `active` |
| `SUSPENDED` | `suspended` |
| `TERMINATED` | `terminated` |

This mapping is deliberate. The semantic identifiers remain uppercase for clarity in specifications and decision records, while the existing Python prototype continues to use ordinary JSON-compatible string values in its model and persistence representation.

The implementation must not introduce additional lifecycle states merely for technical convenience.

## Representation Boundary

`ProcessInstance.lifecycle` remains the authoritative physical lifecycle field in the current prototype.

This is an implementation representation decision, not a claim that lifecycle is semantically owned by the `ProcessInstance` object independently of the authoritative operational state. The semantic model continues to require lifecycle state to be persistent and recoverable as part of the authoritative operational state.

The corresponding invariant is:

> A recovered Process Instance and its Execution Context must expose one semantically consistent lifecycle state and sufficient associated context to interpret that state.

The current physical separation of `process.json` and `context.json` may remain. The persistence implementation must ensure that lifecycle transitions cannot be recovered as an accepted lifecycle change while the material context or trace required to interpret that change is absent or contradictory.

## Canonical Representation Rules

The implementation must treat the three lowercase values as the only canonical persisted lifecycle values:

```text
active
suspended
terminated
```

Equivalent casing or alternate spellings must not become additional canonical states.

Existing data using the canonical values must remain readable. If normalization or compatibility handling is required for pre-existing data, it must preserve the same three semantic states and must not silently reinterpret an unknown value as a valid state.

A missing lifecycle value on a newly created Process Instance may continue to resolve to the canonical initial value `active` through the existing creation default. A persisted unknown lifecycle value must be treated as invalid authoritative state rather than inferred from Runtime availability.

## Authoritative Control Surface

Lifecycle mutation will be centralized behind a single public Runtime lifecycle-control operation whose semantic role is:

```text
apply lifecycle determination
```

The concrete method name is an implementation choice; the current implementation is expected to expose one public operation corresponding to this role rather than independent mutation paths for each lifecycle state.

The control surface accepts a lifecycle determination containing, as applicable:

```text
target Process Instance
requested transition
semantic basis / applicable condition
authority context
actor / source attribution
evidence / relevant conditions
ordering or timestamp information
```

A lifecycle determination is an input to the control boundary. It is not automatically authoritative merely because it was supplied to Runtime.

## Control-Surface Responsibility

The authoritative lifecycle control surface is responsible for enforcing the lifecycle mutation contract at the Runtime boundary.

Conceptually it performs:

```text
Lifecycle determination
        ↓
Target validation
        ↓
Authority validation
        ↓
Semantic / precondition validation
        ↓
Current-state and transition validation
        ↓
Conflict validation
        ↓
Authoritative state mutation
        ↓
Persistence + lifecycle trace
```

These responsibilities may be implemented by multiple private helpers or persistence operations. They must nevertheless behave as one authoritative lifecycle-control boundary from the perspective of callers and observable behavior.

Unrelated Runtime operations must not mutate `ProcessInstance.lifecycle` directly.

## Transition Rules

The control surface must enforce exactly the currently established transition graph:

```text
ACTIVE → SUSPENDED
SUSPENDED → ACTIVE
ACTIVE → TERMINATED
SUSPENDED → TERMINATED
```

The following transitions are rejected:

```text
TERMINATED → ACTIVE
TERMINATED → SUSPENDED
```

A transition is not accepted solely because its target state is representable.

## Determination and Authority

The control surface must distinguish:

```text
request / proposal
        ≠
authorization
        ≠
Runtime mutation
```

For the current targeted implementation, the determination's authority context and applicable condition are therefore required inputs to lifecycle validation.

The implementation may use lightweight validation appropriate to the current prototype. It must not invent a universal domain-specific authority model that has not been established by applicable execution semantics.

At minimum, an explicitly unauthorized determination must be rejected without changing authoritative lifecycle state.

## Condition and Conflict Handling

The control surface must not infer suspension, resumption, or termination solely from a requested target state.

It must evaluate the determination's stated semantic basis and relevant evidence/conditions sufficiently to distinguish an applicable determination from an unsupported request.

Where material conflicting conditions are explicitly presented and cannot be resolved by the applicable semantics available to the current implementation, the lifecycle mutation must be rejected rather than silently selecting an implementation-preferred outcome.

This decision does not establish a general-purpose conflict-resolution engine.

## Suspension Consequence

On successful `ACTIVE → SUSPENDED`:

- `ProcessInstance.lifecycle` becomes `suspended`;
- the existing Execution Context remains preserved;
- pending execution and interruption information remain recoverable where applicable;
- the Process State is not changed merely because lifecycle is suspended;
- subsequent execution must be prevented while the authoritative lifecycle remains suspended; and
- the transition is recorded in lifecycle history.

Suspension does not terminate the Runtime, Agent, conversation, or Execution Environment.

## Resumption Consequence

On a requested `SUSPENDED → ACTIVE` transition, the control surface must treat the determination as a resumption determination, not as a direct field update.

The determination must establish that the suspension condition has ceased or that applicable semantics otherwise permit continuation. The current authoritative Execution Context and relevant continuation information must be considered before activation.

If changed conditions establish that previously pending work is no longer valid, the implementation must invalidate or replace that stale continuation information rather than blindly replay it.

A failed or insufficient reevaluation must leave the lifecycle value `suspended`.

## Termination Consequence

On successful termination from either `active` or `suspended`:

- `ProcessInstance.lifecycle` becomes `terminated`;
- the termination basis and authority are preserved in the trace;
- the transition is reconstructable from authoritative history; and
- the same lifecycle instance cannot later return to `active` or `suspended`.

Engineering completion remains independent from lifecycle termination.

## Persistence Boundary

The lifecycle control surface does not write the lifecycle field as an isolated mutation.

A successful lifecycle transition must establish a consistency boundary across:

1. the authoritative Process Instance lifecycle state;
2. any material Execution Context consequence required by the transition; and
3. the lifecycle transition trace.

The exact transaction or storage mechanism is deliberately deferred to the implementation-mapping work. The current JSON persistence mechanism may be adapted rather than replaced.

The control surface must not report a successful lifecycle transition when authoritative recovery can expose an impossible partial result.

## History Representation

Each accepted material lifecycle transition must produce a reconstructable history record containing, at minimum where applicable:

```text
prior lifecycle state
requested transition / recognized trigger
authority / actor
semantic basis
relevant evidence or conditions
transition identity or equivalent reference
resulting lifecycle state
material consequence
ordering / timestamp
```

The existing append-only `history.jsonl` mechanism may be retained and extended. Event sourcing is neither required nor implied by this decision.

Rejected lifecycle determinations should not mutate authoritative lifecycle state. Recording rejected attempts may be useful for diagnostics, but such records must remain distinguishable from accepted lifecycle transitions and must never be interpreted as state changes.

## Process State Separation

Lifecycle control must not reuse `ExecutionContext.process_state` as a substitute for lifecycle state.

The implementation therefore retains the existing separation:

```text
ProcessInstance.lifecycle
        ≠
ExecutionContext.process_state
```

A lifecycle transition may preserve the current Process State unchanged. Any Process State change associated with a lifecycle transition requires an independently established applicable rule.

## Runtime Lifetime Separation

`Runtime.stop()` and equivalent Runtime replacement/recovery operations must not mutate Process Instance lifecycle implicitly.

Likewise, attaching to a suspended Process Instance must not reactivate it merely because the Runtime is capable of continuing execution.

Lifecycle state changes only through the authoritative lifecycle-control boundary.

## API Design Constraint

The implementation should expose the semantic control boundary rather than a collection of state-specific convenience methods whose existence would become an accidental semantic contract.

Therefore this decision does **not** require:

```text
suspend()
resume()
terminate()
```

as separate public Runtime APIs.

A separate convenience API may exist later only if it delegates to the same authoritative lifecycle-control boundary and does not bypass determination, authority, semantic validation, persistence, or trace recording.

## Non-Goals

This decision does not:

- redesign the Runtime architecture;
- redesign `ProcessStore` as a whole;
- relocate lifecycle state into `ExecutionContext` as a physical model change;
- introduce event sourcing;
- define a universal authority hierarchy;
- define domain-specific suspension or termination triggers beyond the established applicable semantics;
- prescribe a database or transaction technology;
- prescribe locking or concurrency strategy;
- define a UI;
- modify the frozen normative AESM documents; or
- weaken or rewrite the LC-01–LC-16 behavioral scenarios.

## Implementation Consequences

The next implementation-mapping work should inspect the existing Runtime and persistence code specifically for the smallest changes required to satisfy this decision.

The expected implementation areas are limited to:

- canonical lifecycle representation/validation;
- one authoritative Runtime lifecycle-control boundary;
- lifecycle-aware persistence of `ProcessInstance`;
- consistency of material Execution Context consequences;
- lifecycle history records; and
- protection of execution against authoritative `suspended` or `terminated` lifecycle state.

No broader Runtime redesign is implied.

## Validation Relationship

The targeted lifecycle scenarios remain the behavioral oracle. They must be interpreted as semantic scenarios, not as a prescription for arbitrary API names.

The implementation should be judged by whether the control boundary produces the required observable outcomes:

```text
valid determination
    → accepted transition
    → durable consistent state
    → reconstructable trace

invalid / unauthorized / conflicting determination
    → rejected transition
    → authoritative state unchanged
```

The existing tests' lowercase assertions are therefore compatible with the uppercase semantic state identifiers once the representation mapping recorded in this decision is applied.

## Decision

**ADOPT.**

This decision establishes the canonical implementation representation and the authoritative lifecycle control boundary for the current Runtime prototype.

Implementation work may now proceed to Runtime/Store mapping without reopening the lifecycle semantic model or inventing an API shape during coding.
