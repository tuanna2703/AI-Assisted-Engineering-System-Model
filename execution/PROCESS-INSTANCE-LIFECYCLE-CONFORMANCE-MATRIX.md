# Process Instance Lifecycle Conformance Matrix

## Purpose

This matrix reassesses the Process Instance lifecycle prototype against the clarified AESM/PEM lifecycle semantics.

It separates:

- semantic requirement;
- specification precision;
- implementation representation;
- observed behavior;
- experimental coverage;
- current conformance assessment.

This is a conformance analysis artifact. It does not authorize implementation changes.

## Baseline

The lifecycle validation experiment evaluated the Runtime at commit:

`8c2dd09087e064a029d32452a006cbd2b786e5f2`

The lifecycle semantics decision is recorded in:

`execution/PROCESS-INSTANCE-LIFECYCLE-SEMANTICS-DECISION.md`

The clarified specification is represented in the current versions of:

- `docs/04-Execution-Model.md`
- `docs/05-Process-Instance-and-Execution-Context.md`
- `docs/07-Runtime-and-Conformance.md`

## Conformance Matrix

| Requirement | Semantic requirement | Implementation representation | Experimental evidence | Coverage | Assessment |
|---|---|---|---|---|---|
| Lifecycle identity | Process Instance lifecycle is distinct from Process State, completion, and Runtime lifetime | `ProcessInstance.lifecycle` exists separately from process state | Lifecycle remained `active` while Process State changed | Covered | **Conformant for demonstrated separation** |
| Lifecycle persistence | Lifecycle condition is authoritative recoverable operational state | Lifecycle is represented on Process Instance; persistence/update support is limited | Creation and recovery preserve observed `active` value | Partial | **Partially demonstrated; transition persistence not validated** |
| Lifecycle vocabulary | Representation must follow clarified applicable semantics; universal literals are not assumed without specification | Prototype exposes `active` | No alternative lifecycle condition exercised | Not covered | **Specification now sufficient in principle; scenario-specific vocabulary/transition requirements remain to be established** |
| Lifecycle transition authority | Runtime may apply lifecycle changes only when applicable execution semantics permit them | No general lifecycle transition mechanism demonstrated | No lifecycle transition test | Not covered | **Not demonstrated** |
| Runtime separation | Runtime startup/restart/failure/replacement/termination does not itself terminate Process Instance | `Runtime.stop()` detaches Runtime references | Persisted lifecycle remained `active` after stop | Covered | **Demonstrated** |
| Process State separation | Lifecycle must not be inferred from ordinary Process State progression | Separate `process_state` and `lifecycle` representations | `initial → investigation → implementation → verification → engineering_complete` while lifecycle stayed `active` | Covered | **Demonstrated** |
| Engineering completion separation | Engineering completion is distinct from Process Instance termination | Completion is tracked independently | Completion became true while lifecycle remained `active` | Covered | **Demonstrated** |
| Suspension | When applicable, suspension preserves authoritative continuation state and is distinct from termination | No explicit suspension operation demonstrated | No suspension scenario executed | Not covered | **Evidence gap; implementation defect not established** |
| Resumption | Applicable continuation must recover state, reevaluate, and continue under PEM rather than replay | Recovery/attachment mechanisms exist; no explicit semantic resumption path demonstrated | Cross-Runtime recovery succeeded | Partial | **Recovery demonstrated; semantic resumption not demonstrated** |
| Recovery | Authoritative lifecycle and operational state must be reconstructable independently of transient Runtime/Agent memory | Persistent Process Instance/Execution Context mechanism | Cross-Runtime recovery succeeded | Covered | **Demonstrated** |
| Pending execution | Pending work is authoritative continuation information, not an imperative command | `pending_execution`, `next_action`, and resumption information are persisted | Pending execution survived Runtime replacement/recovery | Covered | **Persistence demonstrated** |
| Pending-work continuation | Recovered pending work must be reevaluated before execution | No explicit resumed execution path demonstrated | No test showed reevaluation followed by continued execution | Not covered | **Evidence gap** |
| Process Instance termination | Termination is distinct from Runtime termination and engineering completion; concrete conditions come from applicable semantics | No concrete termination operation demonstrated | No termination scenario executed | Not covered | **Not demonstrated; final implementation requirement depends on applicable lifecycle semantics** |
| Lifecycle traceability | Material lifecycle changes must remain reconstructable with their basis | Existing history mechanisms exist, but lifecycle transition recording was not demonstrated | No lifecycle transition history tested | Not covered | **Evidence gap** |
| Recovery of lifecycle condition | Recovered Execution Context must contain sufficient lifecycle information to interpret continuation | Lifecycle is represented as Process Instance state | Recovery preserved observed lifecycle value | Partial | **Basic preservation demonstrated; broader lifecycle recovery not validated** |
| Blind replay prevention | Resumption must not blindly execute persisted `next_action` or prior Runtime operation | Execution cycle supports reevaluation semantics | No targeted blind-replay test in lifecycle experiment | Not covered | **Not demonstrated** |

## Classification

### Demonstrated

The prototype provides evidence for:

- separation of Process Instance lifecycle from Process State;
- separation of Process Instance lifecycle from engineering completion;
- separation of Runtime lifetime from Process Instance lifecycle;
- persistence/recovery of observed Process Instance state;
- persistence and recovery of pending execution information.

### Evidence gaps

The lifecycle experiment did not demonstrate:

- an actual suspension transition;
- semantic resumption after recovery;
- reevaluation followed by pending-work execution;
- lifecycle transition authority in a concrete transition;
- lifecycle transition history;
- Process Instance termination behavior;
- prevention of blind replay in a targeted lifecycle scenario.

These are evidence gaps, not automatic implementation defects.

### Specification clarification remaining

The clarified specification establishes the universal lifecycle boundary and invariants, but concrete transition conditions remain applicable-semantics dependent. A definitive implementation classification for suspension or termination therefore requires a concrete engineering scenario or an explicit applicable execution specification that establishes those conditions.

## Key Finding

The strongest validated lifecycle property remains:

```text
Runtime lifetime
        ≠
Process Instance lifecycle
        ≠
Engineering completion
```

The prototype's unchanged `active` lifecycle across normal Process State progression and Runtime termination is therefore not, by itself, evidence that lifecycle behavior is missing or incorrect.

The remaining question is behavioral completeness against concrete lifecycle semantics, especially suspension, semantic resumption, lifecycle transitions, and termination.

## Recommended Validation Work

The next validation should use explicit semantic scenarios rather than API-presence checks.

### Suspension scenario

Establish an applicable condition that permits suspension, then verify that:

1. execution becomes suspended according to the applicable semantics;
2. authoritative lifecycle/continuation state is persisted;
3. pending execution and unresolved conditions remain reconstructable;
4. Runtime termination does not accidentally become the suspension mechanism;
5. later continuation is possible.

### Resumption scenario

Starting from an authoritative suspended/interrupted state, verify that:

1. the existing Process Instance is discovered;
2. authoritative state is recovered;
3. the executable situation is reevaluated;
4. stale `next_action` or pending information cannot bypass evaluation;
5. permissible execution continues;
6. resulting state and traceability are updated.

### Termination scenario

Only after applicable termination semantics are established, verify that:

1. the required termination condition is recognized;
2. Process Instance lifecycle changes appropriately;
3. termination is distinct from Runtime termination;
4. termination is distinct from engineering completion unless the applicable semantics explicitly relate them;
5. authoritative state and history preserve the transition.

## Final Assessment

The clarified semantics allow a more precise conformance judgment than the original lifecycle experiment could provide.

The prototype has demonstrated important lifecycle boundaries and continuity behavior, but it has not demonstrated the complete lifecycle transition behavior that may be required in applicable scenarios.

No implementation defect should be declared solely from the absence of named lifecycle APIs. The next engineering evidence should be scenario-based validation of concrete suspension, resumption, and termination semantics after those semantics are explicitly applicable.
