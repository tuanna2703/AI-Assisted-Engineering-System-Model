# AESM Lifecycle Semantic Decision Record

## Purpose

This record resolves the semantic questions exposed by the targeted lifecycle behavioral validation before normative specification changes, conformance-matrix changes, or Runtime implementation.

The semantic ownership boundary is:

```text
Universal AESM/PEM lifecycle semantics
        ↓
Applicable execution semantics
        ↓
Runtime implementation
        ↓
Observable conformance evidence
```

A Runtime mechanism or API is not normative merely because it is convenient to implement.

## Decision status

**Status:** Decision baseline for normative specification update

**Scope:** Process Instance lifecycle state, suspension, resumption, termination, engineering completion separation, persistence, authority, and traceability.

**Implementation consequence:** None directly. Runtime changes remain subject to subsequent conformance validation.

## Semantic ownership

### Decision L-01 — Two-level lifecycle semantics

Lifecycle semantics have two levels:

1. **Universal AESM/PEM semantics** define lifecycle meaning, invariants, canonical lifecycle categories, and mandatory distinctions applicable to every Process Instance.
2. **Applicable execution semantics** define concrete triggers, preconditions, authority rules, and scenario-specific transition conditions.

The Runtime implements these semantics; it does not derive lifecycle meaning from technical behavior.

**Rationale:** AESM needs sufficient universal semantics for conformance while avoiding domain-specific lifecycle policy in the universal model.

## Canonical lifecycle states

### Decision L-02 — Universal lifecycle state vocabulary

The universal Process Instance lifecycle has three canonical states:

```text
ACTIVE
SUSPENDED
TERMINATED
```

- **ACTIVE** — the Process Instance remains an ongoing engineering execution entity and may execute when applicable conditions permit.
- **SUSPENDED** — execution is paused while the Process Instance remains extant and potentially resumable; sufficient authoritative state must be preserved for safe continuation.
- **TERMINATED** — the Process Instance lifecycle has ended and cannot continue as the same lifecycle instance.

A newly established Process Instance is `ACTIVE` unless applicable execution semantics explicitly establish another initial condition.

`TERMINATED` is terminal. `SUSPENDED` is non-terminal and may return to `ACTIVE` only through valid resumption semantics.

These states remain distinct from Process State, engineering completion, Runtime lifetime, Agent/conversation lifetime, and Execution Environment lifetime.

**Rationale:** This is the minimum universal vocabulary needed to make suspension and termination observable without turning domain-specific conditions such as completed, failed, cancelled, or blocked into universal lifecycle states.

## Suspension

### Decision L-03 — Meaning of suspension

Suspension is the lifecycle transition `ACTIVE → SUSPENDED` in which continued execution is paused while the Process Instance remains persistent and potentially resumable.

Sufficient authoritative state must be preserved to reconstruct the executable situation, including as applicable current Process State, pending execution and status, unresolved conditions, interruption information, verification state, material failure/uncertainty, lifecycle transition basis, and required traceability.

Suspension does not imply engineering completion, Process State termination, Process Instance termination, Runtime termination, Agent termination, or Execution Environment termination.

### Decision L-04 — Suspension triggers

Universal PEM semantics do not prescribe one suspension trigger. Suspension may occur only when applicable execution semantics authorize or require it.

Runtime shutdown, Agent departure, conversation closure, IDE closure, or Execution Environment replacement do not themselves constitute semantic suspension unless applicable execution semantics explicitly establish that transition.

### Decision L-05 — Suspension authority

A Participant, Agent, external system, or other actor may request or propose suspension where applicable semantics permit. The Runtime recognizes the request, evaluates authority and applicable conditions, and mutates authoritative lifecycle state only when permitted.

Technical write capability is not lifecycle authority.

## Resumption

### Decision L-06 — Meaning of resumption

Resumption is the transition `SUSPENDED → ACTIVE` followed by re-entry into PEM execution using recovered authoritative state.

Conceptually:

```text
Recovery
   ↓
Reevaluation
   ↓
Permitted continuation
```

Recovery alone is not resumption. A recovered Process Instance remains `SUSPENDED` until applicable resumption conditions are satisfied and execution is validly resumed.

### Decision L-07 — Resumption requires reevaluation

Before continuation, the Runtime must re-evaluate the recovered executable situation against current authoritative state and applicable EPM/PEM conditions.

Where applicable this includes lifecycle state, Process State, pending execution, resumption conditions, unresolved conditions, requirements and constraints, verification state, material failures and uncertainty, changes since suspension, authority, and Decision Gates.

Persisted `next_action` or equivalent continuation information identifies expected continuation; it is not an imperative command.

### Decision L-08 — Resumption is not guaranteed continuation

Reevaluation may result in:

- continuation of the pending activity;
- different permissible activity;
- remaining suspended;
- another applicable execution condition; or
- termination when termination conditions are independently satisfied.

Material outcomes must remain traceable.

## Termination

### Decision L-09 — Meaning of termination

Termination is the transition from a non-terminal lifecycle state to `TERMINATED`, ending the Process Instance as an executable engineering entity.

Termination is distinct from engineering completion, individual action failure, failed verification, Runtime shutdown, Agent departure, and Execution Environment loss.

### Decision L-10 — Termination triggers

Universal PEM semantics do not prescribe one termination trigger. Termination may occur only when applicable execution semantics establish a valid termination condition, which must be sufficiently defined to make the transition testable.

### Decision L-11 — Termination authority

Termination must be authorized by applicable execution semantics. An actor may request termination, but the request becomes authoritative only when authority and execution conditions permit it.

The Runtime is responsible for recognition, authority/condition evaluation, authoritative mutation, and recording the basis.

### Decision L-12 — Termination is terminal

`TERMINATED` cannot transition to `ACTIVE` or `SUSPENDED` as the same lifecycle instance.

Historical state may remain discoverable and recoverable for audit, traceability, reconsideration, or other permitted purposes; historical recovery does not reactivate the Process Instance.

If engineering work continues after termination, applicable semantics must establish a new Process Instance or another explicit relationship rather than silently reactivating the terminated instance.

## Engineering completion

### Decision L-13 — Completion and termination are independent

Engineering completion is established by applicable EPM completion conditions. Process Instance termination is established by applicable lifecycle/execution semantics.

Therefore, unless applicable semantics prohibit a combination, the following are distinct possibilities:

```text
Engineering incomplete + ACTIVE
Engineering incomplete + SUSPENDED
Engineering complete   + ACTIVE
Engineering complete   + SUSPENDED
Engineering complete   + TERMINATED
```

An applicable execution model may require termination after completion, but that is an explicit applicable rule, not a universal AESM equivalence.

## Persistence and authority

### Decision L-14 — Lifecycle state is authoritative operational state

Current lifecycle state is part of the authoritative Execution Context and must be persistent and recoverable. It must not depend solely on Runtime memory, Agent memory, conversation history, IDE/session state, or Execution Environment state.

Recovery must reconstruct lifecycle state together with the operational state required to interpret it.

### Decision L-15 — Lifecycle transitions are consistent authoritative mutations

A lifecycle transition must be represented as a semantically consistent authoritative mutation. Recovery must not expose an accepted lifecycle transition while omitting material state required to interpret it or expose an impossible partial transition.

No particular transaction, event, database, or storage mechanism is required.

## Lifecycle traceability

### Decision L-16 — Material lifecycle transitions are reconstructable

Every material lifecycle transition must be reconstructable from authoritative history.

At minimum, the history must permit reconstruction of:

1. prior lifecycle state;
2. resulting lifecycle state;
3. transition identity or equivalent unique reference;
4. time or ordering information sufficient to establish sequence;
5. recognized triggering event, request, or condition;
6. authority/actor attribution where applicable;
7. applicable EPM/PEM/execution basis;
8. relevant conditions or evidence used for the transition determination;
9. material consequences for continuation or termination.

The storage schema is implementation-dependent.

### Decision L-17 — Current state alone is insufficient

Current lifecycle state alone is not sufficient evidence of lifecycle traceability. Material lifecycle history must remain independently reconstructable, subject to applicable retention rules, and must not be silently overwritten by later state changes.

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

The arrows establish semantic possibilities, not unconditional triggers. Applicable execution semantics determine when transitions are permitted or required.

Universal lifecycle transitions from `TERMINATED` to `ACTIVE` or `SUSPENDED` are prohibited.

## Conformance implications

| Requirement | Observable criterion |
|---|---|
| Canonical lifecycle state | Lifecycle state is explicitly recoverable and distinguishable from Process State and engineering completion. |
| Suspension | A valid trigger produces `ACTIVE → SUSPENDED` while preserving sufficient continuation state. |
| Suspension authority | Unauthorized suspension does not mutate lifecycle state. |
| Resumption | Recovery alone does not make a suspended instance executable. |
| Resumption reevaluation | Recovered conditions are evaluated before continuation. |
| Resumption safety | Stale or invalid pending work is not blindly replayed. |
| Termination | A valid termination condition produces a terminal lifecycle state. |
| Termination authority | Unauthorized termination does not mutate lifecycle state. |
| Termination finality | A terminated instance cannot resume as the same lifecycle instance. |
| Completion separation | Engineering completion and lifecycle termination remain independently observable. |
| Persistence | Lifecycle state survives supported interruption and is recoverable from authoritative state. |
| Transition consistency | Lifecycle mutations recover as semantically consistent authoritative state. |
| Lifecycle traceability | Material transitions can be reconstructed independently from current state. |
| Attribution | Transition basis and authority/actor information are reconstructable where applicable. |

These criteria define what must be demonstrated, not how it must be implemented.

## Explicit non-decisions

This record does not establish:

- a required `suspend()`, `resume()`, or `terminate()` API;
- a particular persistence technology or event/audit schema;
- universal domain-specific suspension or termination triggers;
- a universal rule that engineering completion causes termination;
- additional universal lifecycle states such as `COMPLETED`, `FAILED`, `CANCELLED`, or `BLOCKED`;
- a requirement that Participants or Agents directly control lifecycle state.

## Next work

```text
Lifecycle Semantic Decision Record
        ↓
Normative specification update
        ↓
Conformance matrix update
        ↓
Targeted behavioral validation
        ↓
Runtime gap determination
        ↓
Implementation only for confirmed gaps
        ↓
Verification
```

The existing continuity/recovery experiment remains evidence for continuity and recovery. It is not retroactively promoted to complete semantic resumption evidence.
