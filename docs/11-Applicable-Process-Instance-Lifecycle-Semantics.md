# Applicable Process Instance Lifecycle Semantics

> **Status:** Normative semantic specification
> **Scope:** Process Instance lifecycle applicability, suspension, resumption, termination, authority, preservation, conflict handling, and lifecycle traceability.

## Purpose

This specification defines the concrete, implementation-independent lifecycle semantics required to apply the universal Process Instance lifecycle model during execution.

It establishes the semantic obligations against which a Runtime may be evaluated. It does not prescribe APIs, classes, storage technologies, database schemas, event mechanisms, or other implementation techniques.

## Authority and scope boundary

This specification is subordinate to the AESM Architecture Model and AESM Operational Flow and operates within the Process Execution Model (PEM).

The semantic ownership boundary is:

```text
AESM universal lifecycle semantics
        ↓
Applicable execution semantics
        ↓
Runtime implementation
        ↓
Observable conformance evidence
```

The Runtime implements lifecycle semantics; it does not derive lifecycle meaning from technical capability or current prototype behavior.

Universal AESM/PEM semantics establish lifecycle meaning, canonical states, invariants, and mandatory distinctions. Applicable execution semantics establish concrete triggers, preconditions, authority rules, and scenario-specific conditions.

## Lifecycle dimension

Process Instance lifecycle is distinct from:

- EPM Process State;
- engineering completion;
- Runtime process lifetime;
- Agent or conversation lifetime;
- Execution Environment lifetime.

The canonical lifecycle states are:

```text
ACTIVE
SUSPENDED
TERMINATED
```

`ACTIVE` means the Process Instance remains an ongoing engineering execution entity and may execute when applicable conditions permit.

`SUSPENDED` means execution is intentionally prevented while the Process Instance remains extant and potentially resumable.

`TERMINATED` means the Process Instance lifecycle has ended and cannot continue as the same lifecycle instance.

A newly established Process Instance is `ACTIVE` unless applicable execution semantics explicitly establish another initial condition.

## Universal transition graph

```text
                 ┌──────────────┐
                 │    ACTIVE    │
                 └──────┬───────┘
                        │ suspend
                        ↓
                 ┌──────────────┐
                 │  SUSPENDED   │
                 └──────┬───────┘
                        │ resume
                        ↓
                 ┌──────────────┐
                 │    ACTIVE    │
                 └──────────────┘

ACTIVE ───────────────→ TERMINATED
SUSPENDED ────────────→ TERMINATED
```

The arrows establish permitted semantic paths, not unconditional triggers.

`TERMINATED` has no valid outgoing lifecycle transition to `ACTIVE` or `SUSPENDED` for the same lifecycle instance.

## Suspension semantics

### Applicability

Suspension applies when an applicable execution condition establishes that continued execution must not proceed at the present time while the Process Instance remains eligible for possible future continuation.

A suspension condition therefore establishes both:

1. continuation is presently impermissible or explicitly paused; and
2. termination has not been established.

Universal PEM semantics do not prescribe a single domain-specific suspension trigger.

### Suspension transition

A valid suspension establishes:

```text
ACTIVE → SUSPENDED
```

The transition requires:

- an applicable suspension condition;
- valid authority under the applicable execution semantics;
- the Process Instance remaining extant;
- termination not having been established.

A request, event, or technical mutation capability is not by itself an authoritative suspension transition.

### Preservation

Suspension must preserve sufficient authoritative state to reconstruct the executable situation and permit later reevaluation and, where allowed, continuation.

The preserved state includes, as applicable:

- Process Instance identity;
- applicable EPM identity and version/revision;
- current Process State;
- pending execution activity and status;
- unresolved conditions;
- interruption information;
- verification state;
- material failures and uncertainties;
- suspension basis and authority;
- traceability required to reconstruct the transition and executable situation.

Suspension does not imply engineering completion, Process State termination, Runtime termination, Agent termination, or Execution Environment termination.

## Resumption semantics

### Recovery is not resumption

Recovery reconstructs authoritative Process Instance and Execution Context state. It does not by itself make a suspended Process Instance active.

For a suspended instance:

```text
Recover
   ↓
Reevaluate
   ↓
Determine permissible continuation
   ↓
Resume only when permitted
```

### Reevaluation requirement

Before a `SUSPENDED → ACTIVE` transition and continuation, the Runtime must reevaluate the current executable situation against current authoritative state and applicable EPM/PEM conditions.

The reevaluation includes, where applicable:

- the suspension condition;
- current Process State;
- pending execution;
- resumption conditions;
- requirements and constraints;
- verification state;
- failures and uncertainty;
- changes since suspension;
- authority;
- Decision Gates;
- other conditions affecting permissible continuation.

Persisted `next_action` or equivalent continuation information represents expected continuation information. It is not an imperative command to replay a previous Runtime operation.

### Resumption outcomes

Reevaluation may establish:

- continuation of the pending activity;
- a different permissible activity;
- continued suspension;
- another applicable execution condition; or
- authorized termination where termination conditions are independently satisfied.

A Process Instance must remain `SUSPENDED` when continuation remains impermissible.

A recovered Process Instance must not blindly replay stale, invalid, or contradictory pending work.

## Termination semantics

### Meaning

Termination establishes that the Process Instance has reached a final lifecycle condition and is no longer an executable engineering entity.

Termination is distinct from:

- engineering completion;
- individual action failure;
- failed verification;
- Runtime shutdown;
- Agent departure;
- conversation closure;
- IDE closure;
- Execution Environment loss.

### `ACTIVE → TERMINATED`

An `ACTIVE → TERMINATED` transition is valid when an applicable execution semantic establishes a termination condition and the required authority is present.

### `SUSPENDED → TERMINATED`

A suspended Process Instance may transition directly to `TERMINATED` when an applicable termination condition is established.

Termination does not require an artificial intermediate resumption:

```text
SUSPENDED → ACTIVE → TERMINATED
```

### Finality

Once `TERMINATED` is established, the same lifecycle instance cannot return to `ACTIVE` or `SUSPENDED`.

Historical state may remain recoverable for audit, traceability, reconsideration, or other permitted purposes. Historical recovery does not reactivate the Process Instance.

If engineering work must continue after termination, applicable semantics must establish a new Process Instance or another explicit relationship rather than silently reactivating the terminated instance.

## Authority

Lifecycle authority is separate from technical mutation capability.

The distinction is:

```text
request/proposal
      ≠
authorization
      ≠
Runtime mutation
```

A Participant, Agent, external system, or other actor may request or propose a lifecycle transition where applicable semantics permit such a request. The Runtime must evaluate authority and conditions before applying the authoritative lifecycle mutation.

The applicable execution semantics determine who or what may establish suspension, resumption, or termination.

Unauthorized lifecycle requests must not mutate authoritative lifecycle state.

## Lifecycle and Process State

Lifecycle State does not replace EPM Process State.

A Process State change does not automatically constitute a lifecycle transition unless applicable execution semantics explicitly establish that relationship.

Likewise, a lifecycle transition does not automatically redefine Process State.

The following distinction is mandatory:

```text
Engineering completion
        ≠
Process Instance termination
```

Engineering completion is established by applicable EPM completion conditions. Lifecycle termination is established by applicable lifecycle/execution semantics.

An applicable execution model may explicitly require termination after completion, but that is an applicable rule rather than a universal equivalence.

## Conflict handling

Lifecycle conditions must be evaluated against current authoritative state and applicable execution semantics.

The following rules apply:

- Recovery cannot override an unresolved suspension condition.
- Resumption cannot override an established termination condition.
- A valid termination condition prevents later resumption of that lifecycle instance.
- Completion does not imply termination unless an applicable semantic explicitly connects them.
- Runtime shutdown or environment loss does not imply suspension or termination unless applicable semantics explicitly establish that transition.
- An invalid or unauthorized lifecycle request must not become authoritative merely because Runtime can technically represent it.

Where conditions conflict or remain materially ambiguous, the Runtime must preserve the uncertainty and evaluate the applicable semantics rather than silently selecting an implementation-preferred interpretation.

## Lifecycle state as authoritative operational state

Current lifecycle state is part of the authoritative Execution Context and must be persistent and recoverable.

It must not depend solely on:

- transient Runtime memory;
- Agent memory;
- conversation history;
- IDE/session state;
- Execution Environment state.

Recovery must reconstruct lifecycle state together with the operational information required to interpret it correctly.

A lifecycle mutation must be represented as a semantically consistent authoritative mutation. Recovery must not expose an accepted lifecycle transition while omitting material state required to interpret it or expose an impossible partial transition.

No particular transaction, event, database, or storage mechanism is required.

## Lifecycle traceability

Every material lifecycle transition must remain reconstructable from authoritative history, independently from the current lifecycle state and subject to applicable retention rules.

The history must establish, where applicable:

```text
prior lifecycle state
        ↓
trigger / request / condition
        ↓
authority / actor
        ↓
applicable semantic basis
        ↓
transition
        ↓
resulting lifecycle state
        ↓
material consequence
```

At minimum, reconstruction must permit determination of:

1. the prior lifecycle state;
2. the resulting lifecycle state;
3. transition identity or equivalent unique reference;
4. time or ordering sufficient to establish sequence;
5. recognized trigger, request, or condition;
6. authority or actor attribution where applicable;
7. applicable EPM/PEM/execution basis;
8. relevant conditions or evidence used for the transition determination;
9. material consequences for continuation or termination.

Current lifecycle state alone is insufficient evidence of lifecycle traceability.

## Runtime obligations

Where applicable execution semantics require lifecycle behavior, a conforming Runtime must be capable of:

1. representing lifecycle state explicitly;
2. validating applicable lifecycle preconditions;
3. enforcing termination finality;
4. preserving sufficient Execution Context during suspension;
5. recovering suspended Process Instances without automatically resuming them;
6. reevaluating before resumption;
7. preventing continuation when reevaluation does not permit it;
8. terminating from both `ACTIVE` and `SUSPENDED`;
9. preserving lifecycle transition evidence;
10. reconstructing material lifecycle history.

These are semantic obligations, not implementation prescriptions.

## Conformance interpretation

Lifecycle conformance must be assessed through the following chain:

```text
Applicable lifecycle requirement
        ↓
Concrete applicable condition
        ↓
Expected observable behavior
        ↓
Current Runtime capability
        ↓
Existing evidence
        ↓
Conformance determination
```

The following classifications should be used:

- **Conformant — Demonstrated**
- **Conformant — Evidence Incomplete**
- **Implementation Gap — Semantically Required**
- **Not Applicable**
- **Specification/Applicability Decision Required**

Absence of an API or other technical capability is not itself an implementation defect. A confirmed implementation gap exists only when an applicable semantic requirement is established and Runtime cannot satisfy it.

## Implementation independence

This specification does not prescribe:

- `suspend()`, `resume()`, or `terminate()` APIs;
- class or module names;
- database or persistence technology;
- event sourcing;
- locking or concurrency mechanisms;
- serialization format;
- programming language;
- framework;
- user interface;
- deployment architecture.

An implementation choice becomes normative only where explicitly required by applicable AESM/PEM semantics.

## Relationship to validation

The semantic specification establishes the expected behavior before targeted behavioral validation.

The validation sequence is:

```text
Applicable lifecycle semantics
        ↓
Conformance matrix
        ↓
Targeted behavioral validation
        ↓
Evidence classification
        ↓
Confirmed implementation obligations
        ↓
Runtime changes, if required
        ↓
Re-validation
```

Existing experiments remain evidence only for the behaviors they actually demonstrated. They must not be retroactively treated as evidence of semantic behavior that was not tested.
