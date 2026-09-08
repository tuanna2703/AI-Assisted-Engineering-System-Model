# Process Instance Lifecycle Conformance Matrix

## Purpose

This matrix reassesses the Process Instance lifecycle prototype against the **current clarified AESM/PEM lifecycle semantics**.

It separates:

- semantic requirement;
- specification status;
- implementation representation;
- observed behavior;
- experimental coverage;
- current conformance assessment.

This is a conformance analysis artifact. It does not authorize implementation changes.

## Baseline

The lifecycle validation experiment evaluated the Runtime at commit:

`7273f2e9535436310e0df22c01800e172d848bb4`

The governing lifecycle decision is recorded in:

`execution/PROCESS-INSTANCE-LIFECYCLE-SEMANTICS-DECISION.md`

The current normative lifecycle semantics are represented in:

- `docs/04-Execution-Model.md`
- `docs/05-Process-Instance-and-Execution-Context.md`
- `docs/07-Runtime-and-Conformance.md`

These documents now define the universal lifecycle vocabulary `ACTIVE`, `SUSPENDED`, and `TERMINATED`, universal separation/invariants, legal universal transition structure, recovery/resumption distinction, and lifecycle traceability requirements. Concrete triggers, authority rules, and scenario-specific conditions remain applicable-semantics dependent.

## Conformance Matrix

| Requirement | Semantic requirement | Implementation representation | Experimental evidence | Coverage | Assessment |
|---|---|---|---|---|---|
| Lifecycle identity | Process Instance lifecycle is distinct from Process State, completion, and Runtime lifetime | `ProcessInstance.lifecycle` exists separately from process state | Lifecycle remained `active` while Process State changed | Covered | **Demonstrated** |
| Lifecycle persistence | Lifecycle condition is authoritative and recoverable | Lifecycle is stored on Process Instance; Process Instance is currently write-once | Creation and recovery preserve `active` | Partial | **Basic persistence/recovery demonstrated; mutable transition persistence not demonstrated** |
| Lifecycle vocabulary | Universal lifecycle categories are `ACTIVE`, `SUSPENDED`, `TERMINATED` | Prototype represents `active`; no explicit suspended/terminated values exercised | No alternative lifecycle condition exercised | Partial | **Representation of ACTIVE demonstrated; SUSPENDED/TERMINATED behavior not demonstrated** |
| Lifecycle transition authority | Runtime applies lifecycle mutation only when applicable execution semantics permit/require it | No general lifecycle transition mechanism demonstrated | No lifecycle transition executed | Not covered | **Evidence gap** |
| Runtime separation | Runtime startup/restart/failure/replacement/termination does not itself terminate Process Instance | `Runtime.stop()` detaches Runtime references only | Persisted lifecycle remained `active` after stop | Covered | **Demonstrated** |
| Process State separation | Lifecycle must not be inferred from EPM Process State progression | Separate `process_state` and `lifecycle` representations | Process State progressed while lifecycle remained `active` | Covered | **Demonstrated** |
| Engineering completion separation | Engineering completion is distinct from Process Instance termination | Completion tracked independently | Completion became true while lifecycle remained `active` | Covered | **Demonstrated** |
| Suspension | Applicable suspension establishes `ACTIVE → SUSPENDED` and preserves continuation state | No suspension operation demonstrated | No applicable suspension condition was established | Not covered | **Conditional implementation question / evidence gap** |
| Resumption | Resumption recovers state, reevaluates, determines permissible continuation, then returns to active execution | Recovery/attachment exists; no semantic resumption path demonstrated | Cross-Runtime recovery succeeded | Partial | **Recovery demonstrated; semantic resumption not demonstrated** |
| Recovery | Authoritative lifecycle and operational state must be reconstructable independently of transient Runtime/Agent memory | Persistent Process Instance/Execution Context mechanism | Cross-Runtime recovery succeeded | Covered | **Demonstrated for tested state** |
| Pending execution | Pending work is continuation information, not an imperative command | `pending_execution`, `next_action`, and `resumption_conditions` persisted | Pending execution survived Runtime replacement/recovery | Covered | **Demonstrated for persistence** |
| Pending-work continuation | Recovered pending work must be reevaluated before execution | No explicit resumed execution path demonstrated | No reevaluation/continuation scenario executed | Not covered | **Evidence gap** |
| Process Instance termination | Termination is distinct from Runtime termination and engineering completion and is terminal | No concrete termination mechanism demonstrated | No applicable termination condition was established | Not covered | **Conditional implementation question / evidence gap** |
| Lifecycle traceability | Material lifecycle transitions must remain reconstructable with basis and consequences | History exists, but only Process State/execution events observed | No lifecycle transition occurred | Not covered | **Traceability prerequisite for future lifecycle transitions** |
| Recovery of lifecycle condition | Recovered state must contain sufficient lifecycle information to interpret continuation | Lifecycle is persisted with Process Instance | `active` recovered successfully | Partial | **Demonstrated for ACTIVE; broader lifecycle recovery untested** |
| Blind replay prevention | Resumption must not blindly replay persisted continuation information | General execution model contains reevaluation semantics | No targeted lifecycle blind-replay scenario executed | Not covered | **Evidence gap** |

## Classification

### Demonstrated

The prototype provides evidence for:

- separation of Process Instance lifecycle from Process State;
- separation of Process Instance lifecycle from engineering completion;
- separation of Runtime lifetime from Process Instance lifecycle;
- persistence/recovery of the observed `ACTIVE` lifecycle condition;
- persistence/recovery of pending execution information;
- Runtime replacement continuity for the tested state.

### Evidence gaps

The lifecycle experiment did not demonstrate:

- an actual `ACTIVE → SUSPENDED` transition;
- semantic resumption after a suspended state;
- reevaluation followed by permissible pending-work continuation;
- lifecycle transition authority in an executed transition;
- an actual lifecycle transition history record;
- `ACTIVE → TERMINATED` behavior;
- `SUSPENDED → TERMINATED` behavior;
- prevention of blind replay in a targeted lifecycle scenario.

These remain evidence gaps unless and until applicable execution semantics establish concrete scenarios that make the behaviors required and testable.

### Applicable-semantics dependency

The current specification deliberately defines universal lifecycle meaning and invariants while leaving concrete suspension, resumption, and termination triggers to applicable execution semantics.

Therefore the next conformance question is not whether the Runtime happens to expose lifecycle API names. It is whether a concrete applicable execution scenario establishes a lifecycle transition obligation and, if so, whether the Runtime satisfies it.

## Key Finding

The strongest validated lifecycle property remains:

```text
Runtime lifetime
        ≠
Process Instance lifecycle
        ≠
Engineering completion
```

The prototype's unchanged `active` lifecycle across normal Process State progression, engineering completion, and Runtime termination is therefore consistent with the current semantic boundary and is not itself evidence of a lifecycle defect.

## Required Next Validation

The next validation should use explicit applicable semantic scenarios rather than API-presence checks.

### Suspension

First establish a concrete applicable condition that authorizes or requires suspension. Then verify:

1. `ACTIVE → SUSPENDED` occurs only when permitted;
2. authoritative lifecycle and continuation state are persisted;
3. pending execution and unresolved conditions remain reconstructable;
4. Runtime shutdown is not incorrectly treated as suspension;
5. lifecycle history preserves the transition basis.

### Resumption

Starting from an authoritative `SUSPENDED` state, verify:

1. the existing Process Instance is discovered;
2. authoritative state is recovered;
3. the current executable situation is reevaluated;
4. stale `next_action` or pending information cannot bypass evaluation;
5. permissible continuation returns the lifecycle to `ACTIVE`;
6. resulting state and traceability are updated.

### Termination

Only after a concrete applicable termination condition is established, verify:

1. the termination condition is recognized and authorized;
2. the lifecycle reaches `TERMINATED`;
3. termination is distinct from Runtime termination;
4. termination is distinct from engineering completion unless applicable semantics explicitly relate them;
5. terminated state is persistent and recoverable for permitted historical purposes;
6. the terminated lifecycle instance cannot resume as the same lifecycle instance;
7. lifecycle history preserves the transition basis and consequences.

## Final Assessment

The clarified semantics support a precise conclusion:

- the universal lifecycle model is now sufficiently specified;
- the experiment demonstrated important lifecycle boundaries and basic ACTIVE-state continuity;
- suspension, semantic resumption, and termination remain behaviorally unproven;
- absence of named APIs is not, by itself, a conformance defect;
- concrete implementation obligations must be derived from applicable lifecycle scenarios.

No Runtime lifecycle implementation should be added solely from the original experiment. The next engineering task is to establish concrete applicable lifecycle semantics, then reassess conformance and implement only confirmed obligations.
