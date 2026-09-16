# AESM Execution Model

## Purpose

The Process Execution Model (PEM) defines **how an Engineering Process Model is executed**.

PEM is implementation-independent. A Runtime may use any suitable technology provided that it preserves the required execution semantics.

PEM does not redefine engineering validity. EPM remains authoritative for engineering meaning.

## Execution authority model

The AESM layers are not a simple command hierarchy. They define distinct semantic responsibilities:

```text
EPM
  engineering meaning and validity
        ↓
PEM
  execution semantics
        ↓
Runtime
  concrete execution and operational control
        ↓
Process Instance / Execution Context
  persistent operational identity and authoritative operational state
```

A Runtime implements PEM; it does not become an alternative source of EPM meaning.

## Execution cycle

Execution is continuous and adaptive rather than a predetermined list of actions.

```text
Observe
   ↓
Evaluate
   ↓
Plan
   ↓
Execute
   ↓
Verify
   ↓
Update Execution Context
   ↓
Repeat
```

### Observe

The Runtime observes the current Process Instance, Execution Context, Process State, Artifacts, Participant Input, Evidence, environment changes, and other applicable information.

Observation itself does not mutate authoritative state.

### Evaluate

The Runtime evaluates whether execution may continue, whether more information is needed, whether verification failed, whether assumptions require resolution, whether a transition is valid, and whether a Decision Gate applies.

Evaluation can produce an **Execution Determination**.

### Plan

The Runtime determines permissible next activities within the current Process State, EPM constraints, PEM semantics, and applicable execution conditions.

A Participant or Agent may propose a plan, but a proposal is not automatically an Execution Determination.

### Execute

Execution performs or coordinates permitted engineering activities, such as investigation, analysis, artifact production, modification, experimentation, stakeholder interaction, and verification activities.

### Verify

Execution outputs are evaluated against applicable requirements and conditions. Verification failure may require additional work or reconsideration.

### Update Execution Context

Results are incorporated into authoritative operational state, including artifact changes, evidence, decisions, assumptions, risks, state progression, pending work, unresolved questions, and next actions.

### Repeat

The Runtime begins another cycle using the updated state until applicable completion, suspension, or termination conditions are reached.

## Execution Determination

An Execution Determination is an execution-level determination of what action or condition is permissible next.

It is distinct from an Engineering Decision. Engineering Decisions belong to engineering meaning under EPM; Execution Determinations belong to execution control under PEM.

An Execution Determination must be traceable to the authoritative state, applicable EPM/PEM conditions, and the information recognized during evaluation. It does not itself create engineering validity that EPM does not establish.

## Recognition and mutation

A conforming execution system must distinguish:

```text
Receipt ≠ Recognition
Recognition ≠ Mutation
Proposal ≠ Engineering Decision
Execution Determination ≠ Engineering Decision
Execution Result ≠ Verification
Verification Result ≠ automatic State Mutation
```

Information must be recognized under applicable EPM/PEM conditions before it can affect authoritative state.

### Recognition semantics

**Recognition** is the Runtime-controlled determination that an input, observation, contribution, event, or reported result is sufficiently identified and applicable to be used under the governing semantics.

Recognition must be evaluated against, as applicable:

- the Process Instance identity;
- applicable EPM identity and version/revision;
- current Process State;
- applicable Requirements and Constraints;
- PEM execution conditions;
- authority and authorization conditions;
- required context and preconditions;
- validity and provenance information;
- applicable Decision Gates.

Recognition does not mean that the recognized information is true, sufficient for a Decision, or automatically permitted to mutate state. Verification and mutation remain separate semantic steps where applicable.

If required information for recognition is missing or contradictory, the Runtime must represent the uncertainty or recognition failure explicitly rather than silently choosing an interpretation.

## State execution

EPM defines Process States and their engineering validity. PEM governs execution within and between those states.

A Runtime's technical ability to move a state does not itself establish that the engineering transition is valid.

A state transition may be executed only when the applicable EPM transition conditions have been established and any applicable PEM execution conditions permit execution. The Runtime records the determination and resulting state change as authoritative traceable state.

Where several transitions are technically possible, selection must follow the applicable EPM/PEM conditions rather than implementation preference. A Runtime must not infer engineering validity from technical ordering, convenience, or capability.

## Decision Gates

The Runtime recognizes when a Decision Gate applies, evaluates the required conditions, prevents progression when mandatory conditions are absent, and records the applicable execution determination and traceability.

Gate handling must not bypass or redefine EPM semantics.

A gate's satisfaction is based on recognized information and the applicable EPM gate conditions. Gate satisfaction is authoritative process state and must remain reconstructable. A previously satisfied gate may become unsatisfied through reconsideration, invalidated evidence, changed requirements or constraints, failed verification, or other applicable EPM conditions; the current status must reflect the governing conditions while historical satisfaction remains reconstructable.

## Participants and execution

Participants contribute through the Runtime-controlled execution boundary. They may provide information, analysis, evidence, recommendations, proposed actions, engineering work, verification, and other permitted contributions.

Participation does not transfer Runtime authority to the Participant.

## External actions

Actions performed through Agents, Participants, Tools, or Environment-facing capabilities remain subject to Runtime execution semantics.

The system should distinguish:

```text
requested action
performed action
reported result
recognized result
verified result
state mutation
```

An external action may be performed successfully without its result being recognized or verified. Likewise, a recognized or verified result does not automatically authorize every possible state mutation.

## Failure and uncertainty

Material failure, contradiction, missing information, failed verification, unmet preconditions, and uncertainty must remain explicit.

Failure does not automatically terminate a Process Instance. Uncertainty does not become Evidence merely because execution needs an answer.

## Concurrency and stale state

A Process Instance may be accessed by multiple Participants, Agents, or Execution Environments. The Runtime must therefore preserve authoritative ordering and consistency when concurrent or stale contributions occur.

The semantic requirement is not a particular locking or transaction mechanism. The Runtime must ensure that a contribution evaluated against stale authoritative state cannot silently overwrite newer authoritative state or create an invalid combination of facts.

A Runtime may use serialization, version checks, conflict detection, transactional mechanisms, or other suitable techniques. When a conflict is detected, the Runtime must represent it explicitly and re-evaluate the contribution against current authoritative state before applying a permitted mutation.

Repeated delivery or retry of the same contribution or external result must not silently create duplicate authoritative effects where the applicable operation is intended to be idempotent. The implementation must preserve traceability of retries and conflicts.

## Suspension and resumption

Execution may be suspended only when permitted or required by applicable execution semantics. Suspension pauses Process Instance execution without terminating the Process Instance.

Recovery alone is not resumption. Before resuming a suspended Process Instance, the Runtime must reevaluate the current executable situation against current authoritative state and applicable conditions. Persisted continuation information is not an imperative command.

The detailed semantics of suspension authority, preservation requirements, resumption reevaluation, resumption outcomes, and their relationship to applicable execution conditions are specified in [Applicable Process Instance Lifecycle Semantics](11-Applicable-Process-Instance-Lifecycle-Semantics.md).

## Process Instance lifecycle semantics

Process Instance lifecycle is a universal AESM/PEM semantic dimension describing the lifecycle condition of the persistent Process Instance. The canonical lifecycle states are `ACTIVE`, `SUSPENDED`, and `TERMINATED`.

Lifecycle state is distinct from EPM Process State, engineering completion, Runtime lifetime, Agent/conversation lifetime, and Execution Environment lifetime.

Engineering completion remains independent of lifecycle termination. Completion is established by applicable EPM completion conditions; termination is established by applicable lifecycle/execution semantics. An applicable execution model may explicitly require termination after completion, but that is not a universal equivalence.

The detailed lifecycle semantics — including transition graphs, suspension/resumption/termination authority, preservation requirements, conflict handling, traceability, Runtime obligations, and conformance interpretation — are specified in [Applicable Process Instance Lifecycle Semantics](11-Applicable-Process-Instance-Lifecycle-Semantics.md).

AESM/PEM does not prescribe a lifecycle API such as `suspend()`, `resume()`, or `terminate()`, nor a storage mechanism for lifecycle state or history.

## Lifecycle separation

The following concepts remain distinct:

```text
Process Instance lifecycle
        ≠
Process State
        ≠
Engineering completion
        ≠
Runtime lifecycle
```

Runtime startup, restart, failure, replacement, or termination do not themselves imply Process State transition, Process Instance termination, or engineering completion.

A lifecycle transition is an authoritative state mutation and must be semantically consistent with the recovered Execution Context. Current lifecycle state alone is insufficient for lifecycle traceability; material lifecycle history must remain reconstructable independently from current state, subject to applicable retention rules.

## Conformance

A Runtime claiming conformance must demonstrate preservation of at least:

1. EPM engineering validity;
2. PEM execution semantics;
3. applicable EPM binding;
4. AESM operational boundaries;
5. Agent interaction boundaries;
6. controlled recognition and state mutation;
7. authority separation;
8. Process State and transition semantics;
9. Decision Gate semantics;
10. concurrency and stale-state protection;
11. traceability and history;
12. continuity and recovery;
13. failure, uncertainty, and conflict handling;
14. Process Instance lifecycle semantics and separation;
15. implementation independence.

## Conformance evidence

Useful evidence categories include:

- Process Instance discovery and attachment;
- Process Instance identity preservation across discovery;
- Execution Context reconstruction;
- EPM binding reconstruction;
- execution-trace reconstruction;
- initialization and recovery tests;
- authority-boundary tests;
- operation-recognition tests;
- stale-input and conflict tests;
- state-transition tests;
- Decision Gate blocking/progression/invalidation tests;
- mutation-control and atomicity/consistency tests;
- external action/result traceability tests;
- failure, uncertainty, and recovery-deficiency tests;
- continuity and Runtime replacement tests;
- continuation from recovered authoritative state;
- prevention of blind replay of stale continuation information;
- lifecycle state persistence and reconstruction;
- authorized suspension and unauthorized-suspension rejection;
- resumption reevaluation and stale-pending-work handling;
- authorized termination and unauthorized-termination rejection;
- termination finality;
- completion/termination separation;
- lifecycle transition-history reconstruction;
- lifecycle separation across Runtime restart and replacement.

These are evidence categories rather than mandatory implementation mechanisms.

## Implementation independence

Conformance does not prescribe:

- transport;
- APIs;
- serialization;
- databases;
- filesystems;
- programming languages;
- frameworks;
- model providers;
- network topology;
- deployment architecture;
- UI behavior.

An implementation choice becomes normative only when explicitly required by the applicable AESM semantics.
