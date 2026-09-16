# Continuity, Traceability, and Reconsideration

## Why continuity matters

AESM treats engineering work as persistent state rather than transient interaction.

Continuity means that work can continue after an interruption, Agent change, Runtime restart, IDE closure, or Execution Environment change without requiring the previous conversation to be authoritative.

## Authoritative continuity

```text
Conversation history        ┐
Agent internal memory       ├─ not authoritative by themselves
Transient Runtime state     ┘

Execution Context
        ↓
authoritative operational state
        ↓
Process Instance continuation
```

A conforming system must preserve sufficient information to reconstruct the operational situation and continue execution consistently when the Process Instance remains eligible for continuation.

## Traceability

Traceability makes material engineering and execution history reconstructable.

A useful conceptual chain is:

```text
Requirement / Objective
        ↓
Evidence / Investigation
        ↓
Evaluation
        ↓
Engineering Decision
        ↓
Implementation / Artifact
        ↓
Verification
        ↓
Progress / State
```

The execution layer adds:

```text
Observation / Input
        ↓
Recognition
        ↓
Execution Determination
        ↓
Execution Action
        ↓
Execution Result
        ↓
Verification
        ↓
State Mutation
```

The two chains are related but not interchangeable. Engineering Decisions belong to engineering meaning; Execution Determinations belong to execution control.

## Historical state

Material historical state should remain reconstructable. A new conclusion does not erase the existence of an earlier conclusion.

Historical preservation supports:

- auditing;
- reconsideration;
- debugging;
- understanding why a Decision was made;
- Runtime replacement;
- recovery after interruption;
- reconstruction of material Process Instance lifecycle transitions.

## Reconsideration

Reconsideration occurs when new Evidence, failed verification, changed Constraints, contradictions, identified errors, or other material information warrants revisiting earlier conclusions.

A reconsideration should:

1. identify what is being reconsidered;
2. identify the reason;
3. preserve the previous conclusion and its basis;
4. evaluate the new information;
5. establish a new conclusion through applicable EPM semantics;
6. apply controlled state changes;
7. preserve traceability between previous and current state.

## Continuity across Agents

An Agent may stop participating while the Process Instance remains active or suspended.

```text
Agent A
  ↓
work persisted
  ↓
Agent A unavailable
  ↓
Agent B
  ↓
restore authoritative context
  ↓
reevaluate applicable conditions
  ↓
continue when permitted
```

Agent B should not need Agent A's private conversational memory to establish the authoritative process state.

## Continuity across Environments

The same Process Instance may move between IDE, CLI, cloud, web, or other Execution Environments.

The environment provides access; it does not become the source of truth.

## Process Instance lifecycle

Process Instance lifecycle is a universal AESM/PEM semantic dimension distinct from Process State, engineering completion, Runtime lifetime, Agent/conversation lifetime, and Execution Environment lifetime.

Lifecycle state and lifecycle transitions affect whether a Process Instance may continue, while remaining distinct from engineering completion and Process State. Detailed lifecycle states, transition rules, suspension and resumption semantics, termination semantics, authority, preservation, and lifecycle traceability are defined by [Applicable Process Instance Lifecycle Semantics](11-Applicable-Process-Instance-Lifecycle-Semantics.md).

For continuity purposes, lifecycle state is authoritative Process Instance state rather than a property of the current Agent, conversation, Runtime session, or Execution Environment. Lifecycle history therefore contributes to reconstructing the operational situation across interruptions and changes of participation or environment.

## Suspension and resumption

Continuity depends on distinguishing recovery from resumption. Recovery reconstructs authoritative Process Instance and Execution Context state; it does not by itself establish that execution may continue. A recovered Process Instance must be reevaluated against applicable conditions before continuation is permitted.

```text
Recover authoritative state
        ↓
Reevaluate applicable conditions
        ↓
Continue when permitted
```

Persisted continuation information such as `next_action` is expected continuation information rather than an imperative command to replay a previous Runtime operation. Detailed suspension, resumption, preservation, and reevaluation semantics are defined by [Applicable Process Instance Lifecycle Semantics](11-Applicable-Process-Instance-Lifecycle-Semantics.md).

## Lifecycle traceability

Material lifecycle history contributes to the reconstructability required for continuity and traceability. Current lifecycle state alone is not sufficient to reconstruct the history of material lifecycle transitions.

The detailed requirements for lifecycle transition traceability, including the information required to reconstruct a material transition, are defined by [Applicable Process Instance Lifecycle Semantics](11-Applicable-Process-Instance-Lifecycle-Semantics.md).

## Failure and uncertainty

Continuity also requires preserving what is not known.

Material uncertainty, failed verification, unavailable information, contradictions, blocked conditions, and inability to continue should remain explicit. A system must not manufacture certainty merely to maintain forward motion.

## Core continuity invariants

```text
Process Instance survives Agent changes while not terminated
Process Instance survives Environment changes while not terminated
Process Instance survives Runtime restart when recovery is supported
Execution Context is authoritative operational state
Conversation is not authoritative state
Historical state is not silently erased
Material lifecycle history remains reconstructable
Reconsideration preserves reconstructability
Failure and uncertainty remain explicit
Recovery does not itself imply resumption
Termination does not imply Runtime termination
```
