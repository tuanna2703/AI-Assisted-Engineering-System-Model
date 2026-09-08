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

The canonical lifecycle states are:

```text
ACTIVE
SUSPENDED
TERMINATED
```

The universal transition possibilities are:

```text
ACTIVE ──suspend──→ SUSPENDED
  ↑                    │
  └─────resume─────────┘

ACTIVE ───────────────→ TERMINATED
SUSPENDED ────────────→ TERMINATED
```

`TERMINATED` is terminal and cannot return to `ACTIVE` or `SUSPENDED` as the same lifecycle instance.

Lifecycle transitions occur only when applicable execution semantics authorize or require them. Runtime shutdown, Agent departure, conversation closure, IDE closure, or Environment replacement do not themselves constitute suspension or termination unless applicable execution semantics explicitly establish that transition.

Engineering completion remains distinct from lifecycle termination. Completion is governed by applicable EPM conditions; termination is governed by applicable lifecycle/execution semantics.

## Suspension and resumption

Suspension is the lifecycle transition `ACTIVE → SUSPENDED`. It pauses Process Instance execution while preserving sufficient authoritative state for possible continuation.

The preserved state should include, as applicable, pending work, unresolved conditions, current Process State, verification state, material failure and uncertainty information, lifecycle transition basis, and traceability required to reconstruct the executable situation.

Resumption is not merely recovery. Recovery reconstructs authoritative state; resumption returns a suspended Process Instance to active execution only after reevaluation establishes that continuation is permissible.

The semantic sequence is:

```text
Recover authoritative state
        ↓
Observe current situation
        ↓
Evaluate current conditions
        ↓
Determine permissible continuation
        ↓
Resume active execution when permitted
```

Persisted continuation information such as `next_action` is expected continuation information, not an imperative command. Stale or invalid pending work must not be blindly replayed.

Reevaluation may result in continuation, different permissible activity, continued suspension, another applicable execution condition, or authorized termination.

## Lifecycle traceability

Every material lifecycle transition must remain reconstructable from authoritative history independently from the current lifecycle state, subject to applicable retention rules.

The reconstructable history should establish, where applicable:

```text
prior lifecycle state
        ↓
trigger / request / condition
        ↓
authority / actor
        ↓
applicable semantic basis
        ↓
transition
        ↓
resulting lifecycle state
        ↓
material consequence
```

Current lifecycle state alone is insufficient evidence of lifecycle traceability. Later lifecycle changes must not silently erase material transition history.

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
