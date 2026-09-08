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

Execution may be suspended when permitted by applicable execution semantics.

Suspension preserves sufficient authoritative state for later continuation, including as applicable:

- current Process State;
- pending execution activity;
- unresolved conditions;
- interruption information;
- traceability;
- failure and uncertainty information;
- verification state;
- other information required to reconstruct the executable situation.

Resumption is not equivalent to replaying the last Runtime operation.

Persisted continuation information is interpreted as authoritative input to resumed execution. In particular, a persisted `next_action` identifies expected continuation activity; it is not, by itself, an imperative command that must be executed without reevaluation.

Resumption follows the execution semantics:

```text
Recover authoritative Process Instance state
              ↓
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

The Runtime must re-evaluate applicable conditions using the recovered authoritative state before continuing execution. It must not silently rely on stale Runtime memory, Agent memory, conversation history, or assumptions from the previous execution session.

## Continuation state

The Execution Context may preserve explicit continuation information.

The following concepts have distinct roles:

```text
pending_execution
    = unfinished execution activity that remains relevant to continuation

next_action
    = expected continuation activity associated with the pending execution

resumption_conditions
    = conditions that must be considered before continuation
```

These fields are continuity information, not an instruction to bypass PEM execution semantics.

The presence of `next_action` does not establish that the action is currently permissible. The Runtime must evaluate the recovered situation and applicable EPM/PEM conditions before executing it.

Similarly, the presence of `pending_execution` does not by itself establish whether verification, state transition, completion, suspension, or another execution activity is currently permissible. Those relationships remain governed by the applicable execution conditions.

## Process Instance lifecycle semantics

Process Instance lifecycle is a universal AESM/PEM semantic dimension. It describes the lifecycle condition of the Process Instance as the persistent engineering execution entity.

It is not an EPM Process State and must remain distinct from:

- Process State;
- engineering completion;
- Runtime lifecycle;
- Agent or conversation lifetime;
- Execution Environment lifetime.

AESM/PEM defines the universal lifecycle meaning, invariants, and semantic distinctions. Applicable execution semantics determine concrete lifecycle transition conditions and scenario-specific triggers. A Runtime implements those semantics but must not invent lifecycle meaning from technical behavior alone.

Universal lifecycle invariants include:

- Runtime startup, restart, failure, replacement, or termination does not by itself terminate a Process Instance.
- Engineering completion does not by itself mean Process Instance termination.
- Suspension, when applicable, is distinct from termination and preserves sufficient authoritative state for possible continuation.
- Recovery reconstructs authoritative state; resumption re-enters PEM execution using that state.
- Process Instance lifecycle condition must be recoverable from authoritative state rather than transient Runtime or Agent memory.

AESM/PEM does not require a particular API such as `suspend()`, `resume()`, or `terminate()`. Nor does this section establish a universal literal lifecycle-state enumeration. Where concrete lifecycle states or transitions are required, they must be defined by the applicable specification and execution semantics.

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

**Process Instance lifecycle** describes the lifecycle condition of the Process Instance as a continuing engineering execution entity.

**Process State** describes the current engineering execution state governed by applicable EPM semantics and executed under PEM.

**Engineering completion** is established when applicable EPM completion conditions are satisfied.

**Runtime lifecycle** describes the lifetime of a concrete Runtime process.

Therefore:

```text
Runtime startup
Runtime restart
Runtime failure
Runtime replacement
Runtime termination

        do not themselves imply

Process State transition
Process Instance termination
Engineering completion
```

A Process Instance may remain active while its Process State changes repeatedly during normal engineering execution.

The exact lifecycle transition vocabulary and transition conditions are governed by applicable execution semantics and must remain distinguishable from ordinary Process State progression.
