# AESM Execution Model

## Purpose

The Process Execution Model (PEM) defines **how an Engineering Process Model is executed**.

PEM is implementation-independent. A Runtime may use any suitable technology provided that it preserves the required execution semantics.

PEM does not redefine engineering validity. EPM remains authoritative for engineering meaning.

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

## State execution

EPM defines Process States and their engineering validity. PEM governs execution within and between those states.

A Runtime's technical ability to move a state does not itself establish that the engineering transition is valid.

## Decision Gates

The Runtime recognizes when a Decision Gate applies, evaluates the required conditions, prevents progression when mandatory conditions are absent, and records the applicable execution determination and traceability.

Gate handling must not bypass or redefine EPM semantics.

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

## Failure and uncertainty

Material failure, contradiction, missing information, failed verification, unmet preconditions, and uncertainty must remain explicit.

Failure does not automatically terminate a Process Instance. Uncertainty does not become Evidence merely because execution needs an answer.

## Suspension and resumption

Execution may be suspended when permitted. Suspension preserves sufficient authoritative state, pending work, unresolved conditions, traceability, and failure/uncertainty information for later resumption.

Resumption starts from authoritative state and re-evaluates applicable execution conditions rather than blindly replaying stale assumptions.

## Lifecycle separation

The following remain distinct:

```text
Engineering completion
        ≠
Process Instance termination
        ≠
Runtime termination
```

Stopping or restarting a Runtime must not silently complete or terminate the Process Instance.