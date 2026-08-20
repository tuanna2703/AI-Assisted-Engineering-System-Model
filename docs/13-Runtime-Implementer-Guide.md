# Runtime Implementer Guide

## Purpose

This guide translates the AESM Runtime model into an implementation-oriented understanding without prescribing a particular software architecture or technology.

A Runtime is an implementation of the Process Execution Model (PEM). It executes Process Instances while preserving EPM engineering meaning, PEM execution semantics, and authoritative operational state.

## What must remain separate

A Runtime implementation must preserve these conceptual boundaries:

```text
EPM
  engineering meaning and validity

PEM
  execution semantics

Runtime
  concrete execution and operational control

Process Instance
  persistent identity of one engineering execution

Execution Context
  authoritative current operational state required to continue it

Participants
  Human and AI contributions

Execution Environment
  interaction and tooling surface
```

These are semantic responsibilities, not a mandatory command hierarchy. A convenient internal software structure may differ, but it must not collapse these boundaries.

## EPM binding

Every Process Instance must have an explicit, recoverable binding to the applicable EPM definition. Where EPM definitions are versioned, the applicable version or revision must be recoverable.

The Runtime must use that binding when evaluating engineering state, transition validity, Decision Gates, completion conditions, and other EPM-governed semantics.

The Runtime must not silently substitute a different EPM definition during recovery or continuation. If the applicable EPM cannot be resolved, execution must represent the deficiency rather than invent engineering semantics.

## Runtime responsibilities

A conforming Runtime must provide the semantic capabilities necessary to:

1. establish, attach to, and recover Process Instances;
2. establish, access, maintain, and recover authoritative Execution Context;
3. preserve the applicable EPM binding;
4. observe the current executable situation;
5. evaluate execution conditions;
6. recognize relevant inputs and events under applicable semantics;
7. evaluate Process States and transition conditions;
8. recognize and handle Decision Gates;
9. make Execution Determinations;
10. plan and coordinate permitted actions;
11. execute or coordinate execution actions;
12. record Execution Results;
13. support verification;
14. apply only permitted state mutations;
15. preserve pending work and unresolved conditions;
16. preserve history and traceability;
17. support reconsideration without silently erasing history;
18. preserve material failure, uncertainty, and conflicts;
19. support suspension, resumption, recovery, and applicable termination semantics.

These are semantic obligations, not a required module or service decomposition.

## Execution cycle

A Runtime should be understandable in terms of the PEM cycle:

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

The implementation may combine, split, queue, retry, or otherwise realize these operations differently, provided the observable semantics remain conformant.

## Recognition boundary

The Runtime must distinguish receiving information from recognizing its semantic meaning.

```text
Receipt
  ≠
Recognition
  ≠
Permitted Mutation
```

Recognition should consider, as applicable:

- Process Instance identity;
- applicable EPM identity and version/revision;
- current Process State;
- Requirements and Constraints;
- PEM execution conditions;
- authority and authorization conditions;
- required context and preconditions;
- validity and provenance;
- applicable Decision Gates;
- traceability requirements.

Recognition is not equivalent to verification, authorization, or mutation. If material information required for recognition is missing, contradictory, stale, or ambiguous, the Runtime must preserve that condition explicitly rather than invent an interpretation.

## State transition boundary

EPM determines engineering transition validity. PEM determines how execution handles the transition.

Therefore:

```text
EPM transition validity
        ≠
Runtime technical ability to move state
```

A Runtime may execute a state transition only when the applicable EPM conditions have been established and PEM permits execution. The Runtime must record the transition, its basis, and its resulting authoritative state.

When several transitions are technically possible, the Runtime must evaluate the applicable conditions rather than using technical ordering or implementation preference as engineering authority.

## Decision Gate boundary

Decision Gates are EPM-defined conditions governing progression. The Runtime must identify when a gate applies, evaluate its conditions using recognized information, prevent prohibited progression, and preserve the gate outcome in authoritative state and traceability.

A recommendation, assertion, successful action, or technical state change does not by itself satisfy a gate.

A gate that was previously satisfied may become unsatisfied when applicable evidence, verification, Requirements, Constraints, Decisions, or other governing conditions change. The current status must reflect current semantics while the historical satisfaction remains reconstructable.

## Mutation boundary

A useful implementation model is:

```text
Input / Observation
       ↓
Interpretation
       ↓
Recognition
       ↓
Applicable EPM / PEM conditions
       ↓
Execution Determination where required
       ↓
Permitted State Mutation
       ↓
Updated Execution Context
       ↓
Traceability
```

Technical write access is not equivalent to semantic permission to mutate authoritative state.

A mutation must preserve semantic consistency. If the complete permitted mutation cannot be committed, the Runtime must not silently expose a partial authoritative state. The implementation may use transactions, versioned state, append-only records, event processing, or another mechanism; AESM specifies the semantic consistency requirement, not the technology.

## Engineering validity versus execution ability

EPM determines whether an engineering transition is valid.

PEM determines how execution handles that transition.

Therefore:

```text
Runtime can perform X
        ≠
AESM permits X
```

A Runtime must not infer engineering validity from technical capability.

## Agent boundary

Agents and other Participants operate through the applicable Runtime execution boundary.

The Runtime must preserve the distinction among:

- Participant input;
- Agent proposal;
- Engineering Decision;
- execution recommendation;
- Execution Determination;
- performed action;
- reported result;
- recognized result;
- verified result;
- authoritative state mutation.

Agent capability must not be treated as unrestricted Runtime authority.

## Concurrency and stale state

Multiple Agents, Participants, or Execution Environments may contribute to one Process Instance. The Runtime must therefore prevent stale or concurrent contributions from silently overwriting newer authoritative state or creating invalid combinations of facts.

The implementation may use locking, optimistic concurrency, serialization, queues, version checks, conflict detection, or another mechanism. The semantic requirements are:

1. authoritative state changes are ordered or otherwise conflict-safe;
2. a contribution evaluated against stale state cannot silently replace newer state;
3. detected conflicts are represented explicitly;
4. conflicting contributions are re-evaluated against current authoritative state before permitted mutation;
5. retries do not silently create duplicate authoritative effects where the applicable operation is intended to be idempotent;
6. material conflict and retry history remains traceable.

## Process Instance and continuity

The Process Instance is the persistent identity of engineering work.

The Execution Context is the authoritative operational state required for continuation.

Runtime-specific memory, process-local state, caches, Agent conversations, or environment state may support execution but must not become authoritative merely by being convenient.

A Runtime replacement must be able to continue from the authoritative state and records required by applicable semantics, including the EPM binding.

## Failure and uncertainty

The Runtime must represent material failure and uncertainty explicitly.

Examples include:

- failed verification;
- missing required information;
- contradictory inputs;
- unmet preconditions;
- blocked execution;
- unavailable external capability;
- recovery failure;
- uncertain recognition;
- stale-state or concurrency conflict;
- inability to resolve the applicable EPM.

Failure does not automatically mean Process Instance termination.

## Lifecycle separation

The implementation must preserve:

```text
Engineering completion
        ≠
Process Instance termination
        ≠
Runtime termination
```

Engineering completion requires applicable EPM completion conditions. Process Instance termination is a separate lifecycle condition governed by applicable execution semantics. Runtime restart, shutdown, replacement, or failure must not silently establish either condition.

Lifecycle status is authoritative operational state and must survive Runtime replacement when continuation is supported.

## Conformance evidence

A Runtime implementation should be able to demonstrate, through appropriate evidence, that it preserves:

- EPM binding and engineering validity;
- PEM execution semantics;
- authority separation;
- controlled recognition and mutation;
- Process State and transition semantics;
- Decision Gate handling and invalidation;
- Agent and Participant boundaries;
- concurrency and stale-state protection;
- traceability and history;
- continuity and recovery;
- failure and uncertainty;
- lifecycle separation;
- implementation independence.

Useful test/evidence categories include EPM binding reconstruction, recovery reconstruction, state-transition tests, gate enforcement and invalidation tests, stale-input/conflict tests, mutation-consistency tests, Agent-boundary tests, external-action traceability, failure handling, Runtime replacement, and completion/termination separation.

## Implementation independence

AESM does not require a specific:

- programming language;
- database;
- filesystem;
- API style;
- transport;
- serialization format;
- Agent framework;
- model provider;
- deployment topology;
- UI;
- process architecture.

Choose implementation mechanisms according to the system's needs. Demonstrate conformance at the semantic boundary.
