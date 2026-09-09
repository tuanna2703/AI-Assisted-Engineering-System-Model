# Process Instance Lifecycle Control — Runtime/Store Implementation Mapping

## Status

**ADOPTED AS THE IMPLEMENTATION MAP FOR THE NEXT CONTROLLED CHANGE**

## Purpose

This document maps the adopted Process Instance lifecycle representation and control-surface decision onto the current Runtime and persistence implementation.

It identifies the smallest required implementation changes before production code is modified. It is an implementation mapping, not a new AESM semantic specification.

## Reviewed Baseline

The mapping was performed against the current `main` branch after adoption of:

- `implementation/decisions/PROCESS-INSTANCE-LIFECYCLE-CONTROL-CONTRACT.md`
- `implementation/decisions/PROCESS-INSTANCE-REPRESENTATION.md`
- `implementation/decisions/PROCESS-INSTANCE-LIFECYCLE-REPRESENTATION-AND-CONTROL-SURFACE.md`
- targeted lifecycle scenarios in `tests/lifecycle/test_process_instance_lifecycle_control.py`

The current Runtime is explicitly described as a small implementation experiment rather than a normative semantic layer. `runtime/core/runtime.py` currently provides Process Instance creation/attachment, Process State operations, evidence/decision/artifact/verification recording, completion recognition, and Runtime stop, but no lifecycle-control operation. fileciteturn31file0L2-L2

## Current Architecture Relevant to Lifecycle

### ProcessInstance model

`runtime/core/models.py` already contains:

- stable `process_instance_id`;
- `engineering_objective`;
- `lifecycle`, defaulting to `active`;
- `execution_context_ref`;
- EPM/PEM references; and
- timestamps.

Therefore no new lifecycle field is required. The existing physical representation is compatible with the adopted decision. fileciteturn35file0L2-L2

### ExecutionContext model

`ExecutionContext` contains Process State and continuation information, including `pending_execution`, verification, unresolved matters, failure/uncertainty, and engineering completion. It does not contain a second lifecycle field. This is desirable because lifecycle and Process State must remain distinct. fileciteturn35file0L2-L2

No lifecycle field should be added to `ExecutionContext` for this change.

### Runtime

`Runtime` owns the in-memory references to the current Process Instance and Execution Context and delegates persistence to `ProcessStore`. Existing Runtime operations mutate Context through `_set_state()` or direct Context mutation followed by `save_context()`. No existing operation provides an authoritative Process Instance lifecycle mutation boundary. fileciteturn31file0L2-L2

This is the primary implementation gap.

### ProcessStore

`ProcessStore.create()` writes `process.json`, `context.json`, and an initial `process_created` history event. `load_instance()` reads `process.json`; `load_context()` validates and reads `context.json`; `save_context()` persists Context and appends history. There is currently no `save_instance()` or lifecycle-specific persistence operation. fileciteturn39file0L2-L2

This is the secondary implementation gap.

### JSON persistence

`JsonStore.save()` already performs an atomic replacement of an individual JSON file using a temporary file and `os.replace()`. `JsonlStore.append()` flushes and fsyncs the history file. These primitives can be reused; replacing the persistence layer is not justified by the lifecycle requirement. fileciteturn15file0L2-L2

## Required Change Set

The minimum production change should be limited to four implementation areas.

### Runtime lifecycle-control boundary

Add one public Runtime operation whose semantic role is **apply lifecycle determination**.

The operation should:

1. require an attached Process Instance;
2. validate that the determination is a mapping with the required lifecycle-control fields;
3. validate that the determination targets the attached Process Instance;
4. derive the current lifecycle from the authoritative Process Instance representation;
5. validate authority;
6. validate the requested transition against the legal transition graph;
7. validate the applicable condition/semantic basis;
8. reject explicit material conflicts rather than silently choosing an outcome;
9. apply only the supported lifecycle consequence;
10. persist the lifecycle change through `ProcessStore`; and
11. update the in-memory Process Instance only after the authoritative persistence operation succeeds, or otherwise restore the pre-transition in-memory state on failure.

The public operation must be the only intended Runtime route for lifecycle mutation.

### ProcessStore lifecycle persistence

Add the smallest ProcessStore capability necessary to persist a changed `ProcessInstance` and lifecycle trace.

The operation should accept the Process Instance plus the transition event data and persist:

- the updated `process.json`;
- the lifecycle transition trace; and
- any required Context update through an explicitly defined path.

The operation should validate Process Instance identity and existence before mutation.

A generic ProcessStore redesign is not required.

### Lifecycle representation validation

Add validation at the model/store boundary so that persisted lifecycle values are limited to:

```text
active
suspended
terminated
```

Unknown persisted values must fail recovery rather than being inferred or silently normalized into a valid state.

This can be implemented as a small validation helper or equivalent model validation. A new enum abstraction is not required unless it materially reduces complexity without expanding the semantic surface.

### Lifecycle execution guard

Existing Runtime operations that can perform engineering work should not continue execution while lifecycle is `suspended` or `terminated`.

The implementation should add the smallest reusable Runtime guard and apply it to operations that actually advance or mutate engineering execution.

The guard must not be applied to:

- lifecycle determination itself;
- attachment/recovery;
- read-only state inspection; or
- operations necessary to record an allowed lifecycle determination.

The exact list of guarded operations should be established from the existing Runtime surface rather than by redesigning Runtime globally.

## Lifecycle Determination Structure

The targeted tests already supply a determination with:

```text
target_process_instance_id
requested_transition
semantic_basis
authority_context
actor
evidence
occurred_at
```

The implementation should consume this structure rather than changing the tests to fit an invented API. The tests deliberately discover a public lifecycle-control method rather than prescribing its name. fileciteturn38file0L2-L2

The implementation should preserve this semantic adapter boundary.

## Transition Mapping

The Runtime should recognize only these transitions:

| Current | Requested | Result |
|---|---|---|
| `active` | `ACTIVE -> SUSPENDED` | `suspended` |
| `suspended` | `SUSPENDED -> ACTIVE` | `active` |
| `active` | `ACTIVE -> TERMINATED` | `terminated` |
| `suspended` | `SUSPENDED -> TERMINATED` | `terminated` |

The following must be rejected:

| Current | Requested | Result |
|---|---|---|
| `terminated` | `TERMINATED -> ACTIVE` | reject |
| `terminated` | `TERMINATED -> SUSPENDED` | reject |

A mismatch between the requested source state and the actual current state must also be rejected.

## Authority Mapping

The current tests distinguish `authorized-controller` from `unauthorized-source`. fileciteturn36file0L1-L2

For this prototype, the implementation should use the lightweight authority distinction required by the existing scenarios. It must not introduce a generalized authorization subsystem or claim that the string values constitute a universal AESM authority model.

At minimum:

```text
authority_context == "authorized-controller"
    → eligible for further semantic validation

other explicit authority context
    → reject
```

This is implementation scaffolding for the current controlled experiment, not a new AESM authority hierarchy.

## Semantic Condition Mapping

The current targeted scenarios intentionally express conditions as textual semantic bases and evidence.

The implementation should therefore apply conservative prototype validation rather than attempting to interpret arbitrary natural language exhaustively.

Minimum expected behavior:

- a determination must provide a non-empty semantic basis;
- suspension must establish that continuation is presently impermissible;
- resumption must establish that the suspension condition ceased or continuation is otherwise permissible;
- termination must provide an applicable termination basis;
- explicit conflict evidence must cause rejection when the conflict cannot be resolved from the supplied determination.

The implementation should use the evidence structure to recognize the controlled scenarios without becoming a general natural-language reasoning engine.

## Resumption and Pending Execution

The current `pending_execution` representation already provides a suitable continuity location. The lifecycle implementation should preserve it across suspension. The targeted suspension test explicitly requires pending work and Process State to survive recovery unchanged. fileciteturn36file0L1-L2

For resumption, the implementation must distinguish valid continuation from stale work.

The current targeted stale-work scenario supplies explicit evidence identifying `W1` as stale and `W2` as replacement work. The minimal implementation consequence is:

```text
stale pending work identified
    → remove/invalidate stale work
    → do not replay it
    → retain valid replacement continuation if explicitly supplied
    → activate only after valid reevaluation
```

The implementation should not introduce a general workflow scheduler.

## Execution Context Consequences

For the current lifecycle scenarios:

### Suspension

Do not modify:

- `process_state`;
- `pending_execution`;
- engineering decisions;
- artifacts; or
- verification state

unless a separate lifecycle consequence explicitly requires it.

The targeted test requires Process State and pending continuation to remain unchanged after suspension. fileciteturn36file0L1-L2

### Resumption

Normally no Process State mutation is required merely to change lifecycle from `suspended` to `active`.

Only stale/invalid continuation information identified by the determination should be changed.

### Termination

No Context field needs to be invented solely to represent termination. The lifecycle field plus lifecycle trace is sufficient for the current representation.

Engineering completion must remain unchanged and independent of Process Instance termination.

## Persistence and History Mapping

The existing store has a useful split:

```text
process.json  → Process Instance identity + lifecycle metadata
context.json  → authoritative operational Context
history.jsonl → append-only execution trace
```

This split should be retained for the prototype. `ProcessStore` should become the single persistence boundary through which lifecycle transitions are committed rather than allowing Runtime to manipulate files directly.

A successful lifecycle transition should create a lifecycle event containing at least:

```text
type
process_instance_id
prior_lifecycle
requested_transition
authority_context
actor
semantic_basis
evidence
resulting_lifecycle
runtime_id
occurred_at
```

A unique transition identifier should be added if needed by the implementation to distinguish repeated transitions; the implementation should not introduce a separate event infrastructure merely for this field.

The targeted history test requires accepted lifecycle events to expose the semantic states needed to reconstruct the transition chain. fileciteturn37file0L1-L2

## Consistency Boundary — Prototype Interpretation

The current JSON implementation provides atomic replacement per file, but not a multi-file transaction spanning `process.json`, `context.json`, and `history.jsonl`. fileciteturn15file0L2-L2

This is a real implementation limitation and should not be hidden.

For the current lifecycle implementation, the minimum acceptable boundary is:

- no successful Runtime result before required state persistence succeeds;
- no lifecycle mutation in memory when authoritative persistence fails;
- lifecycle history is written as part of the lifecycle persistence operation;
- recovery after normal successful operations yields mutually consistent state.

Crash-atomic multi-file transactions are **deferred**. They are not justified by the current behavioral evidence and should become a separate implementation task only if an experiment demonstrates that the prototype's persistence boundary is insufficient.

This explicitly avoids introducing event sourcing or a new transactional storage subsystem prematurely.

## Attach and Recovery

`Runtime.attach()` already loads Process Instance and Context from `ProcessStore`. fileciteturn31file0L2-L2

No new recovery mechanism is required.

The lifecycle implementation must ensure:

```text
stored suspended → attach → suspended
stored terminated → attach → terminated
```

It must not infer `active` from Runtime startup or attachment.

The existing recovery tests already establish the general Process Instance/Context replacement pattern. fileciteturn41file0L2-L2

## Runtime Stop

`Runtime.stop()` currently only clears Runtime-local references and does not mutate persisted state. This is already compatible with the lifecycle requirement. fileciteturn31file0L2-L2

No change to `stop()` is required unless lifecycle execution guards reveal an indirect path that currently mutates lifecycle.

## Test Mapping

The implementation should be evaluated against the existing LC-01–LC-16 scenarios without changing their semantic oracles.

| Scenario group | Primary implementation area |
|---|---|
| LC-01, LC-02 | Runtime determination validation + ProcessStore lifecycle persistence |
| LC-03, LC-05 | ProcessStore persistence + Runtime attach |
| LC-04 | preservation of Context/pending execution |
| LC-06, LC-07 | resumption determination validation |
| LC-08 | stale continuation invalidation |
| LC-09, LC-10 | termination transition handling |
| LC-11 | terminal-state guard |
| LC-12 | authority validation |
| LC-13 | lifecycle history |
| LC-14 | completion/lifecycle separation |
| LC-15 | Runtime stop/recovery separation |
| LC-16 | conflict detection |

The targeted tests currently fail explicitly when no public lifecycle-control mechanism exists, which is the intended implementation gap. fileciteturn20file0L2-L2

## Regression Protection

The implementation must preserve the existing continuity behavior:

- Process Instance creation still yields `active`;
- Context remains independently recoverable;
- Runtime replacement still recovers objective, evidence, decisions, and pending execution;
- explicit decision recognition remains unchanged;
- explicit completion recognition remains unchanged; and
- history ordering for existing non-lifecycle operations remains valid.

The existing continuity suite establishes these behaviors and should not be weakened to accommodate lifecycle implementation. fileciteturn24file0L2-L2

## Files Expected to Change

Expected production changes:

```text
runtime/core/runtime.py
runtime/core/store.py
runtime/core/models.py        # only if lifecycle validation cannot remain local to store/runtime
```

Expected test changes:

```text
tests/lifecycle/test_process_instance_lifecycle_control.py
```

Potentially add a focused lifecycle persistence/model test file only if doing so improves coverage without duplicating LC-01–LC-16.

No changes are currently justified to:

```text
runtime/persistence/json_store.py
runtime/core/__init__.py
normative AESM documents
```

`json_store.py` already provides the necessary individual-file durability primitive. fileciteturn15file0L2-L2

## Implementation Order

The production change should be made in this order:

1. Add lifecycle value validation.
2. Add ProcessStore lifecycle persistence operation and trace construction.
3. Add Runtime lifecycle determination validation and transition application.
4. Add execution guards for suspended/terminated lifecycle where required.
5. Run LC-01–LC-16.
6. Correct only behavioral defects demonstrated by those tests.
7. Run the existing continuity/recovery suite.
8. Record the resulting validation evidence and conformance impact.

Do not introduce convenience APIs, broad authorization infrastructure, new lifecycle states, or a new persistence architecture during these changes.

## Exit Condition

This implementation-mapping task is complete when the next engineer/agent can modify the Runtime without needing to rediscover:

- where lifecycle is represented;
- where lifecycle mutation belongs;
- what ProcessStore must provide;
- what Context must and must not change;
- what history must contain;
- what current limitations remain; and
- which files are expected to change.

## Conclusion

The current implementation does **not** require a Runtime redesign.

The lifecycle gap is localized:

```text
ProcessInstance.lifecycle
        ↑
ProcessStore lifecycle persistence
        ↑
Authoritative Runtime lifecycle determination
        ↓
Lifecycle-aware execution guard
        ↓
Existing ExecutionContext + history mechanisms
```

The existing representation, persistence primitives, Runtime attachment model, and continuity tests can be retained and adapted. The next task is therefore controlled Runtime implementation, not further semantic or architectural design.

**Mapping status: COMPLETE.**
