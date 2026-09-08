# Process Instance Lifecycle Semantics Decision

## Decision Status

**Decision:** Adopt a universal AESM/PEM semantic boundary for Process Instance lifecycle, while leaving concrete transition conditions and scenario-specific triggers to applicable execution semantics.

**Scope:** Model/specification decision only. No Runtime or test implementation changes are authorized by this decision.

## Decision

Process Instance lifecycle is a **universal semantic dimension of AESM/PEM** because it describes the lifecycle condition of the Process Instance itself. It must therefore remain distinct from:

- EPM Process State;
- engineering completion;
- Runtime lifetime;
- Agent or conversation lifetime;
- Execution Environment lifetime.

AESM/PEM should define the meaning and invariants of Process Instance lifecycle at the universal model level.

However, AESM/PEM should **not prescribe that every engineering process use one universal set of literal lifecycle transitions or triggers independent of applicable execution semantics**. Concrete transition conditions, authorization, and scenario-specific causes may be determined by the applicable EPM/PEM semantics.

This establishes the following boundary:

```text
Universal AESM/PEM semantics
    ↓
Process Instance lifecycle is a distinct lifecycle dimension
    ↓
Universal invariants and lifecycle concepts are defined
    ↓
Applicable execution semantics determine concrete transition conditions
    ↓
Runtime implements the resulting semantics
```

## Rationale

### Process Instance lifecycle is not EPM Process State

The current model assigns engineering meaning to Process State through EPM. Process State is defined by the applicable engineering process, including its objective, permitted activities, outputs, completion conditions, and transition constraints.

Process Instance lifecycle instead describes the condition of the persistent execution entity. Treating lifecycle as merely another EPM Process State would collapse two distinct semantic dimensions and would make lifecycle continuity depend unnecessarily on the particular engineering process.

Therefore lifecycle must remain universal and independent of EPM Process State identity.

### Runtime lifetime cannot define Process Instance lifecycle

The model explicitly separates Runtime startup, restart, failure, replacement, and termination from Process Instance lifecycle. A Runtime may stop while the Process Instance remains active and recoverable.

Therefore Runtime behavior cannot be the authoritative definition of Process Instance lifecycle.

### Engineering completion cannot define lifecycle termination

Engineering completion is an EPM determination established by applicable engineering completion conditions. It is not equivalent to Runtime termination and is independently distinguished from Process Instance termination.

Therefore recognizing engineering completion must not automatically be treated as Process Instance termination unless applicable lifecycle semantics explicitly require that relationship.

### Lifecycle needs universal semantics, but not necessarily universal triggers

The model already requires lifecycle to be observable as a concept and identifies suspension, resumption, recovery, and termination as distinct semantic concerns. At the same time, the current specification does not establish a complete universal literal state vocabulary or universal transition table.

The appropriate resolution is therefore neither:

1. leave lifecycle entirely to individual EPMs; nor
2. impose an unconditional universal state machine with fixed literal values and transitions.

Instead, AESM/PEM should define the universal lifecycle dimension, invariants, and semantic categories, while applicable execution semantics define when concrete lifecycle transitions are valid.

## Universal Lifecycle Semantics

The following should be treated as universal semantic requirements to clarify in the specification.

### Lifecycle identity

A Process Instance has a lifecycle condition independent of its current EPM Process State.

### Lifecycle continuity

The Process Instance remains the same persistent engineering execution entity across Runtime replacement, Agent replacement, conversation/context-window boundaries, and Execution Environment changes, unless applicable semantics explicitly terminate it.

### Lifecycle separation

Process Instance lifecycle must remain distinguishable from:

- Process State;
- engineering completion;
- Runtime lifetime;
- Agent/session lifetime;
- Execution Environment lifetime.

### Suspension and termination distinction

Suspension and termination are distinct lifecycle semantics. Suspension preserves the possibility of later continuation; termination establishes that the Process Instance is no longer continuing under the applicable lifecycle semantics.

### Recovery and resumption distinction

Recovery reconstructs authoritative Execution Context. Resumption re-enters PEM execution using that recovered state. Successful recovery does not by itself prove that resumption has occurred.

### Authoritative state

Lifecycle status and other continuation information must be recoverable from authoritative persistent state rather than transient Runtime memory or Agent context.

## What Remains Applicable-Semantics Dependent

The following should not be declared as universal literal behavior without further specification work:

- exact lifecycle state names;
- mandatory lifecycle state enumeration;
- exact suspension triggers;
- exact resumption triggers;
- exact termination triggers;
- whether particular engineering processes expose explicit lifecycle operations;
- whether engineering completion permits, requires, or is independent of a lifecycle transition;
- authorization rules for lifecycle transitions.

These require explicit specification where they are needed for a concrete execution scenario.

## Required Specification Clarifications

The next specification revision should explicitly define at least:

1. **Lifecycle semantic categories** — what kinds of lifecycle conditions AESM recognizes universally.
2. **Lifecycle invariants** — relationships that must remain true regardless of EPM.
3. **Lifecycle transition authority** — which layer determines whether a transition is permitted.
4. **Lifecycle transition conditions** — how applicable EPM/PEM semantics establish concrete transition conditions.
5. **Suspension semantics** — what must be preserved and what suspension means operationally.
6. **Resumption semantics** — how a suspended/recovered Process Instance re-enters execution.
7. **Termination semantics** — what Process Instance termination means and how it differs from completion and Runtime termination.
8. **Lifecycle state representation** — whether canonical literals are required and, if so, which ones.
9. **History/traceability requirements** — what lifecycle transitions must record.
10. **Recovery behavior** — how lifecycle condition participates in authoritative Execution Context recovery.

This clarification should be made in the appropriate normative/specification documents rather than inferred from the current prototype.

## Conformance Consequences

This decision changes the interpretation of the lifecycle validation experiment as follows.

| Observation | Interpretation after this decision |
|---|---|
| `ProcessInstance.lifecycle` remains `active` while Process State changes | Consistent with lifecycle/Process State separation; does not prove lifecycle implementation completeness |
| Engineering completion leaves lifecycle unchanged | Not a defect by itself; completion and lifecycle termination are distinct |
| `Runtime.stop()` leaves Process Instance lifecycle unchanged | Correctly demonstrates Runtime lifetime separation |
| Cross-Runtime recovery succeeds | Evidence of continuity and recovery |
| No explicit `resume()` operation observed | Evidence gap for semantic resumption, not proof that a named API is required |
| No explicit `suspend()` operation observed | Not a defect until applicable suspension semantics establish a concrete required behavior |
| No explicit Process Instance termination operation observed | Conformance remains conditional on clarified applicable termination semantics |
| No universal lifecycle state vocabulary exists | Specification precision gap requiring clarification |

## Decision on the Current Prototype

No Runtime lifecycle state machine should be implemented yet.

No generalized `suspend()`, `resume()`, or `terminate()` API should be added solely because the experiment exposed their absence.

The prototype should first be evaluated against the clarified lifecycle semantics. Only after the specification establishes concrete required behavior should implementation work be classified as an implementation/representation task.

## Follow-up Work

The immediate follow-up is specification clarification, followed by a revised conformance matrix and targeted validation requirements.

The intended sequence is:

```text
Lifecycle semantics decision
        ↓
Normative/specification clarification
        ↓
Implementation ↔ PEM conformance reassessment
        ↓
Targeted validation requirements
        ↓
Implementation work, if required
```

This sequence prevents the validation experiment from becoming an implicit source of new semantics and preserves the separation between observation, specification, and implementation.

## Final Decision

**AESM shall treat Process Instance lifecycle as a universal semantic dimension of the Process Instance and PEM, distinct from EPM Process State, engineering completion, Runtime lifetime, Agent/session lifetime, and Execution Environment lifetime. Universal lifecycle concepts and invariants must be specified by AESM/PEM. Concrete lifecycle transition conditions and scenario-specific triggers may be established by applicable EPM/PEM execution semantics.**

Until the corresponding specification clarification is completed, lifecycle implementation changes remain deferred.
