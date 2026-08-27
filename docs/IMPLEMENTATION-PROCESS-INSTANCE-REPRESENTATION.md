# Process Instance Implementation Representation

## Purpose

This document defines the minimal implementation representation of an AESM Process Instance for the initial prototype.

It translates existing AESM semantics into implementation requirements without introducing new AESM semantics.

## Semantic Baseline

The canonical documentation defines a Process Instance as one execution of the Engineering Process Model for a specific engineering objective and as the persistent identity of that engineering work. It is independent of Agent, conversation, Agent context window, IDE session, Runtime process lifetime, and Execution Environment.

A Process Instance must have a stable identity that remains unchanged across continuation, Agent replacement, Runtime restart, and Execution Environment replacement. It must also retain an explicit binding to the applicable EPM definition, including a recoverable version or revision where the EPM is versioned.

The Process Instance and Execution Context are semantically distinct. The Process Instance identifies which engineering execution exists; the Execution Context records the authoritative operational situation now.

## Minimal Required Representation

The prototype Process Instance representation therefore requires exactly these semantic elements:

| Field | Required | Semantic role |
|---|---|---|
| `process_instance_id` | Yes | Stable identity of the engineering execution. |
| `engineering_objective` | Yes | The specific engineering objective for which this Process Instance exists. |
| `epm` | Yes | Explicit binding to the applicable EPM definition; includes version/revision when applicable. |

The representation may contain additional implementation metadata, but additional fields must not be interpreted as new AESM semantic requirements unless separately justified and approved.

## Prototype Representation

The existing Python implementation represents the Process Instance as a dataclass with:

- `process_instance_id`
- `engineering_objective`
- `lifecycle`
- `execution_context_ref`
- `epm`
- `pem`
- `created_at`
- `updated_at`

This representation is therefore classified as **ADAPT**, not **REPLACE**.

### `process_instance_id`

**Keep.** It directly implements the stable Process Instance identity requirement.

The value must be generated once at creation and persisted. Loading, Runtime replacement, Agent replacement, and environment replacement must preserve the same value.

### `engineering_objective`

**Keep.** It directly represents the specific engineering objective of the Process Instance.

It is part of the Process Instance representation for prototype purposes and should remain recoverable independently of conversation state.

### `epm`

**Keep and constrain.** The field directly implements the required EPM binding.

The binding must be explicit and recoverable. Where applicable, the representation must be capable of carrying the EPM version or revision required to interpret the Process Instance correctly.

The implementation must not infer the binding solely from the current Runtime, Agent, or environment.

### `pem`

**Retain only as implementation metadata pending validation.**

The current field is not required by the Process Instance semantic definition itself. The execution documentation establishes that PEM governs execution semantics and that a Runtime implements PEM, but it does not establish that a Process Instance must carry a separate persistent PEM identity in the same manner as the EPM binding.

Therefore this field must not be treated as a normative Process Instance requirement. It may remain temporarily for compatibility with the existing prototype, but its necessity must be evaluated before it is relied upon by later implementation work.

### `lifecycle`

**Keep as authoritative process-state metadata, but do not conflate it with completion or Runtime lifetime.**

The execution model states that Process Instance lifecycle status is authoritative process state and that engineering completion, Process Instance termination, and Runtime termination remain distinct.

The current `lifecycle` field may therefore represent Process Instance lifecycle status, provided its allowed values and transitions are subsequently aligned with the applicable execution semantics.

### `execution_context_ref`

**Keep as an implementation reference, not as an AESM semantic requirement.**

AESM requires a persistent and recoverable Execution Context but does not prescribe a storage format or physical representation.

A reference from the Process Instance record to the physical Context representation is therefore a valid prototype storage choice. It must not be confused with the semantic definition of the Process Instance.

### `created_at` / `updated_at`

**Keep as implementation metadata.**

These timestamps support persistence and operational inspection but are not identified as Process Instance semantic requirements in the canonical documentation.

## Relationship to Execution Context

The prototype must preserve this distinction:

```text
ProcessInstance
    ├── stable identity
    ├── engineering objective
    └── EPM binding

ExecutionContext
    ├── current process state
    ├── requirements / constraints
    ├── evidence / assumptions / risks
    ├── decisions / gates
    ├── artifacts / verification
    ├── unresolved matters / pending work
    └── other authoritative continuation state
```

The current Runtime may persist these structures using separate files or another implementation mechanism. The storage arrangement does not alter their semantic distinction.

## Explicit Non-Requirements

The following must **not** be added to the minimal Process Instance representation merely for convenience:

- Agent identity as the Process Instance owner;
- conversation/session identifiers as continuity identity;
- IDE or Execution Environment identity as Process Instance identity;
- Runtime process identifier as Process Instance identity;
- a workflow-specific step list as a substitute for the EPM;
- engineering conclusions that belong in Execution Context;
- transient Agent memory;
- environment-specific configuration presented as AESM semantics.

## Implementation Decision

**Decision: ADAPT the existing `ProcessInstance` representation rather than create a new model.**

The existing representation already contains the three semantic essentials: stable identity, engineering objective, and EPM binding. Its remaining fields are implementation metadata or execution-state support and can be retained only with the boundaries described above.

No new AESM semantic concept is introduced by this decision.

## Verification Requirements for the Next Task

The next implementation work may now proceed to Process Instance creation and persistence, subject to these checks:

1. Creation produces a stable unique identity.
2. Creation requires an engineering objective.
3. Creation records an explicit EPM binding.
4. Persisted state can be loaded without conversation history.
5. Reloading does not change the Process Instance identity.
6. Runtime or Agent replacement does not change the Process Instance identity.
7. Process Instance identity remains distinct from Execution Context state.
8. No implementation field is allowed to silently become a new AESM semantic requirement.
