# AESM Lifecycle Conformance Matrix

## Purpose

This matrix translates the current Lifecycle Semantic Decision Record and Applicable Process Instance Lifecycle Semantics into observable conformance criteria for targeted behavioral validation.

It separates semantic requirements, applicability prerequisites, required behavior, existing evidence, and conformance classification.

## Governing assessment chain

```text
Lifecycle semantic
        ↓
Applicable condition
        ↓
Required behavior
        ↓
Existing Runtime behavior
        ↓
Existing evidence
        ↓
Classification
```

Absence of an API or mechanism is not itself an implementation gap. A Runtime gap is confirmed only when an applicable semantic requirement establishes concrete behavior and the Runtime cannot satisfy it.

## Classification vocabulary

- **Conformant — Demonstrated** — direct evidence establishes the required semantic behavior.
- **Conformant — Evidence Incomplete** — the requirement is applicable and available evidence supports it, but does not establish the complete criterion.
- **Implementation Gap — Semantically Required** — the applicable requirement is established and the current Runtime cannot satisfy it.
- **Not Applicable** — the criterion is outside the applicable execution semantics for the scenario; the reason must be recorded.
- **Specification/Applicability Decision Required** — the universal requirement is defined, but no concrete applicable condition currently makes the behavior testable.

Historical experiment labels such as `Pending validation`, `Partial evidence`, or `Not demonstrated` remain historical evidence descriptions, not final conformance classifications.

## Current conformance assessment

| ID | Semantic requirement | Applicability prerequisite | Required behavior | Existing evidence | Current classification |
|---|---|---|---|---|---|
| LC-01 | Canonical lifecycle state | Universal lifecycle semantics apply to every Process Instance. | Lifecycle state is explicitly represented, recoverable, and distinguishable from Process State and engineering completion. | Lifecycle is represented as `active` and preserved across recovery; separation from Process State and completion was demonstrated. | **Conformant — Demonstrated** |
| LC-02 | Lifecycle persistence | Supported interruption/recovery of an existing Process Instance. | Lifecycle state is recovered from authoritative state rather than Runtime memory alone. | Cross-Runtime continuity/recovery demonstrated preservation of the observed `ACTIVE` state. | **Conformant — Demonstrated** for the observed state |
| LC-03 | Suspension transition | A concrete authorized suspension condition established by applicable execution semantics. | `ACTIVE → SUSPENDED` with sufficient authoritative continuation state preserved. | No suspension transition was exercised. | **Specification/Applicability Decision Required** |
| LC-04 | Suspension authority | A concrete scenario defines authorized and unauthorized suspension requests. | Unauthorized request does not mutate authoritative lifecycle state. | No lifecycle authority scenario was exercised. | **Specification/Applicability Decision Required** |
| LC-05 | Suspension preservation | A valid suspension condition exists. | Required continuation state and suspension basis remain recoverable after suspension. | No lifecycle-specific suspension scenario exists. | **Specification/Applicability Decision Required** |
| LC-06 | Recovery is distinct from resumption | A suspended Process Instance exists and is recovered. | Recovery reconstructs state but does not itself establish `ACTIVE`. | Cross-Runtime recovery is demonstrated, but no suspended instance was recovered. | **Conformant — Evidence Incomplete** |
| LC-07 | Resumption reevaluation | A suspended instance plus a concrete resumption scenario. | Current conditions are reevaluated before `SUSPENDED → ACTIVE` and continuation. | Pending execution survived Runtime replacement, but reevaluation before resumption was not demonstrated. | **Conformant — Evidence Incomplete** |
| LC-08 | Resumption safety | Suspended instance has stale or materially changed pending work. | Stale/invalid pending work is not blindly replayed. | No stale-work scenario was exercised. | **Conformant — Evidence Incomplete** |
| LC-09 | Resumption outcome | Suspended instance plus concrete reevaluation condition. | Reevaluation may continue, choose another permissible activity, remain suspended, enter another applicable condition, or terminate when independently authorized. | No semantic resumption outcome was exercised. | **Conformant — Evidence Incomplete** |
| LC-10 | Termination transition | A concrete authorized termination condition established by applicable execution semantics. | `ACTIVE → TERMINATED` or `SUSPENDED → TERMINATED` as applicable. | No termination transition was exercised. | **Specification/Applicability Decision Required** |
| LC-11 | Termination authority | A concrete scenario defines authorized and unauthorized termination requests. | Unauthorized termination does not mutate authoritative lifecycle state. | No lifecycle authority scenario was exercised. | **Specification/Applicability Decision Required** |
| LC-12 | Termination finality | A valid termination transition exists. | `TERMINATED` cannot return to `ACTIVE` or `SUSPENDED` as the same lifecycle instance. | No terminated instance exists in the tested implementation. | **Specification/Applicability Decision Required** |
| LC-13 | Completion separation | Engineering completion and lifecycle termination are independent unless explicitly connected by applicable semantics. | Completion remains independently observable from lifecycle termination. | Completion/process-state progression while lifecycle remained `ACTIVE` was demonstrated. | **Conformant — Demonstrated** |
| LC-14 | Lifecycle transition consistency | A concrete lifecycle transition is executed. | Lifecycle state and required Execution Context recover as one semantically consistent authoritative mutation. | General mutation evidence exists, but no lifecycle transition was executed. | **Conformant — Evidence Incomplete** |
| LC-15 | Lifecycle traceability | A material lifecycle transition is executed. | History reconstructs prior/resulting state, transition identity, sequence, trigger/condition, basis, authority where applicable, and material consequence. | No lifecycle transition history exists because no lifecycle transition was executed. | **Conformant — Evidence Incomplete** |
| LC-16 | Transition attribution | A lifecycle transition is executed and attribution is meaningful. | Authority/actor and semantic basis are reconstructable where applicable. | No lifecycle transition was executed. | **Conformant — Evidence Incomplete** |
| LC-17 | Lifecycle separation from Runtime | Runtime interruption occurs without an independently established lifecycle transition. | Runtime lifetime changes do not themselves imply suspension or termination. | `Runtime.stop()` left lifecycle unchanged; cross-Runtime recovery succeeded. | **Conformant — Demonstrated** |
| LC-18 | Lifecycle separation from Agent/Environment | Agent/session/environment interruption occurs without an independently established lifecycle transition. | Interruption does not itself imply lifecycle suspension or termination. | Existing continuity evidence supports the boundary; full environment-loss semantics were not directly exercised. | **Conformant — Evidence Incomplete** |
| LC-19 | Terminal transition graph | A terminated lifecycle instance exists after an applicable termination transition. | No `TERMINATED → ACTIVE` or `TERMINATED → SUSPENDED` transition for the same instance. | No terminated instance was created. | **Conformant — Evidence Incomplete** |
| LC-20 | Implementation independence | Lifecycle behavior is assessed semantically rather than by mandated mechanism. | Conformance does not depend on a specific lifecycle API or persistence technology. | Current specification explicitly makes API/storage choices implementation-dependent. | **Conformant — Demonstrated** at specification level |

## Reassessment conclusion

The universal lifecycle semantics are now sufficiently explicit. The remaining boundary is applicability and evidence, not universal lifecycle vocabulary.

### Demonstrated conformance

- lifecycle separation from Process State;
- lifecycle separation from engineering completion;
- lifecycle separation from Runtime lifetime;
- representation and recovery of the observed `ACTIVE` lifecycle state; and
- implementation independence at the specification level.

### Evidence incomplete

- recovery of a `SUSPENDED` instance without automatic resumption;
- reevaluation before resumption;
- stale-work protection during resumption;
- alternative resumption outcomes;
- lifecycle transition consistency;
- lifecycle transition trace reconstruction;
- transition attribution; and
- terminality after an actual termination transition.

These are evidence gaps, not confirmed Runtime defects.

### Applicability decisions still required

Concrete suspension and termination conditions, and their scenario-specific authority, must be established before the corresponding Runtime behavior can be classified as a confirmed implementation gap.

A controlled validation scenario may establish an applicable semantic condition for experimentation without making that scenario a universal AESM trigger.

## Targeted validation mapping

### Suspension

```text
Controlled applicable suspension condition
      ↓
Authorized lifecycle determination
      ↓
ACTIVE → SUSPENDED
      ↓
Preserve authoritative state
      ↓
Persist transition
      ↓
Recover independently
      ↓
Verify suspended condition and preserved continuation state
      ↓
Reconstruct transition history
```

Runtime shutdown, Agent departure, conversation closure, IDE closure, or environment replacement must not be used as a suspension trigger unless the test explicitly establishes that semantic relationship.

### Resumption

```text
SUSPENDED
      ↓
Recover authoritative state
      ↓
Remain non-executing
      ↓
Introduce or observe current conditions
      ↓
Reevaluate applicable EPM/PEM conditions
      ↓
Validate pending execution / next expected action
      ↓
Determine permissible continuation
      ↓
Resume ACTIVE execution only when permitted
```

At least one scenario must introduce a material change after suspension so that blind replay can be distinguished from genuine reevaluation.

### Termination

```text
ACTIVE or SUSPENDED
      ↓
Controlled applicable termination condition
      ↓
Authorized lifecycle determination
      ↓
TERMINATED
      ↓
Persist terminal state
      ↓
Recover historical state
      ↓
Verify no same-instance resumption
```

A separate unauthorized-request scenario should demonstrate that an unauthorized termination request does not mutate lifecycle state.

### Traceability

The validator must reconstruct lifecycle history from historical evidence rather than reading only the current lifecycle field. The reconstruction should establish, where applicable:

```text
prior state
    ↓
trigger/request/condition
    ↓
authority/actor
    ↓
semantic basis
    ↓
transition
    ↓
resulting state
    ↓
material consequence
```

The reconstruction must remain possible after subsequent lifecycle changes.

## Decision on Runtime implementation

No generalized Runtime lifecycle implementation is justified yet.

The next step is targeted behavioral validation using controlled, scenario-specific applicable lifecycle conditions. Only the resulting evidence may establish a confirmed Runtime implementation obligation.

## Next work

```text
Controlled applicable lifecycle scenarios
        ↓
Targeted behavioral validation
        ↓
Evidence classification
        ↓
Confirmed Runtime obligations
        ↓
Implementation only for confirmed gaps
        ↓
Re-validation
```
