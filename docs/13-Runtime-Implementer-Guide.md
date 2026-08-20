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

Process Instance / Execution Context
  persistent operational state

Participants
  Human and AI contributions

Execution Environment
  interaction and tooling surface
```

A convenient internal software structure may differ, but it must not collapse these semantic boundaries.

## Runtime responsibilities

A conforming Runtime must provide the semantic capabilities necessary to:

1. establish, attach to, and recover Process Instances;
2. establish, access, maintain, and recover authoritative Execution Context;
3. observe the current executable situation;
4. evaluate execution conditions;
5. recognize relevant inputs and events under applicable semantics;
6. evaluate Process States and transition conditions;
7. recognize and handle Decision Gates;
8. make Execution Determinations;
9. plan and coordinate permitted actions;
10. execute or coordinate execution actions;
11. record Execution Results;
12. support verification;
13. apply only permitted state mutations;
14. preserve pending work and unresolved conditions;
15. preserve history and traceability;
16. support reconsideration without silently erasing history;
17. preserve material failure and uncertainty;
18. support suspension, resumption, recovery, and applicable termination semantics.

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

- current Process State;
- EPM conditions;
- PEM execution conditions;
- authority conditions;
- required context;
- validity constraints;
- provenance and traceability;
- applicable Decision Gates.

An implementation must not silently convert arbitrary input into authoritative state.

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

## Process Instance and continuity

The Process Instance is the persistent identity of engineering work.

The Execution Context is the authoritative operational state required for continuation.

Runtime-specific memory, process-local state, caches, Agent conversations, or environment state may support execution but must not become authoritative merely by being convenient.

A Runtime replacement must be able to continue from the authoritative state and records required by applicable semantics.

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
- uncertain recognition.

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

Runtime restart, shutdown, replacement, or failure must not silently change the engineering lifecycle state.

## Conformance evidence

A Runtime implementation should be able to demonstrate, through appropriate evidence, that it preserves:

- EPM engineering validity;
- PEM execution semantics;
- authority separation;
- controlled recognition and mutation;
- Process State and Decision Gate handling;
- Agent and Participant boundaries;
- traceability and history;
- continuity and recovery;
- failure and uncertainty;
- lifecycle separation;
- implementation independence.

Useful test/evidence categories include recovery reconstruction, state-transition tests, gate enforcement, mutation-control tests, Agent-boundary tests, external-action traceability, failure handling, Runtime replacement, and completion/termination separation.

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
