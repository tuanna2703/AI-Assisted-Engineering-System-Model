# Runtime and Conformance

## Runtime definition

A **Runtime** is an implementation of the Process Execution Model.

Its purpose is to execute Process Instances according to EPM and PEM while preserving authoritative operational state.

A Runtime is not:

- the EPM;
- the PEM;
- an AI Agent;
- a Participant;
- the Execution Context;
- an Engineering Decision;
- an independent source of engineering authority.

## Runtime responsibilities

A conforming Runtime provides semantic capabilities necessary to:

1. discover, establish, attach to, or recover Process Instances;
2. establish, access, maintain, and recover Execution Context;
3. establish and preserve the applicable EPM binding;
4. evaluate the current executable situation according to PEM;
5. receive and interpret relevant inputs, observations, contributions, results, verification, failures, and continuation information;
6. distinguish informational content from mutation-relevant content;
7. recognize information under EPM/PEM semantics;
8. evaluate Process States and transition conditions;
9. recognize and handle Decision Gates;
10. make Execution Determinations;
11. plan and coordinate permissible actions;
12. record Execution Results;
13. support verification;
14. apply only permitted state mutations;
15. preserve pending work;
16. preserve traceability and history;
17. support reconsideration without erasing history;
18. preserve continuity information;
19. represent material failure, uncertainty, conflicts, and recovery failures explicitly;
20. support Process Instance suspension, resumption, recovery, and termination according to applicable semantics.

These are semantic obligations, not a required software decomposition or API surface.

## Process Instance discovery

Process Instance discovery is a Runtime responsibility.

The Runtime is responsible for resolving an existing Process Instance when sufficient identification or discovery information is available. The Execution Environment may provide access, storage, filesystem, network, API, or other capabilities used to perform discovery, but those capabilities do not make the Execution Environment the semantic owner of Process Instance discovery.

Conceptually:

```text
Execution Environment
    provides access/capabilities
             ↓
Runtime
    discovers / resolves Process Instance
             ↓
Process Instance
             ↓
Execution Context
```

Discovery is an implementation responsibility of the Runtime and does not require a particular storage mechanism, search strategy, identifier, or API shape.

AESM does not require a specific `discover()` API.

A Runtime may implement discovery through files, databases, services, indexes, identifiers, registries, or other suitable mechanisms, provided that the resulting Process Instance identity and authoritative state remain consistent with AESM semantics.

## Runtime control boundary

```text
External information / action
        ↓
Runtime interpretation
        ↓
Recognition under EPM / PEM
        ↓
Execution Determination
        ↓
Execution Action
        ↓
Execution Result
        ↓
Verification
        ↓
Permitted State Mutation
        ↓
Execution Context / Trace
```

Receipt does not itself cause mutation.

## Recognition

Recognition is the Runtime-controlled determination that an observed representation or event corresponds to a semantically meaningful input under applicable EPM/PEM rules.

Recognition must consider applicable Process State, execution conditions, operation semantics, authority conditions, required context, validity constraints, provenance, the applicable EPM binding, and traceability.

A Runtime must not silently convert an informational or candidate input into authoritative state.

Recognition does not imply truth, sufficiency, verification, authorization, or mutation. Those are separate determinations where applicable.

If the information required for recognition is missing, contradictory, stale, or ambiguous in a material way, the Runtime must preserve that condition explicitly and must not invent an interpretation solely to enable progress.

## State transition boundary

EPM defines engineering transition validity. PEM defines execution handling.

Therefore:

```text
EPM transition validity
        ≠
Runtime technical ability to move state
```

The Runtime must not create, bypass, or redefine engineering transition validity.

A conforming Runtime may execute a transition only after the applicable EPM conditions have been established and the PEM execution conditions permit it. The resulting state change and its basis must be represented in authoritative state and traceability.

## Controlled state mutation

State Mutation occurs only when applicable EPM/PEM semantics permit it and the Runtime has sufficient recognized information and execution conditions.

```text
Input / Observation
 ↓
Interpretation
 ↓
Recognition
 ↓
Applicable conditions
 ↓
Execution Determination where required
 ↓
Permitted mutation
 ↓
Updated Execution Context
 ↓
Traceability
```

Technical write access is not equivalent to semantic permission to mutate authoritative state.

A mutation must preserve semantic consistency. If a requested change cannot be applied as a valid authoritative update, the Runtime must reject, defer, or otherwise represent the condition explicitly rather than partially applying an invalid state.

The implementation may use transactions, versioning, append-only records, event processing, or other mechanisms. AESM requires the semantic result: recovery must not silently expose partial authoritative mutation or lose the traceability of accepted changes.

## External actions

Actions performed through Agents, Participants, Tools, or environment-facing capabilities remain under applicable Runtime execution control.

The Runtime should preserve the distinction between requested action, performed action, reported result, recognized result, verified result, and state mutation.

An external action may succeed technically without establishing a verified or authoritative engineering result.

## Concurrent participation

Multiple Participants, Agents, or Execution Environments may contribute to the same Process Instance. A conforming Runtime must preserve consistency when contributions are concurrent or were produced from stale Execution Context.

A stale contribution must not silently overwrite newer authoritative state or create an invalid combination of facts. The Runtime must detect or otherwise prevent such semantic conflicts and re-evaluate the contribution against current authoritative state before applying a permitted mutation.

AESM does not prescribe locking, optimistic concurrency, serialization, queues, or another implementation mechanism. The semantic requirement is authoritative conflict detection and controlled resolution.

Retries or duplicate delivery must not silently produce duplicate authoritative effects where the applicable operation is intended to be idempotent. Retry and conflict history must remain traceable where material.

## Continuity and Runtime replacement

A conforming Runtime must support continuation from authoritative Execution Context.

Runtime-specific transient memory is not authoritative merely because it is internal to the Runtime.

Where Runtime replacement is permitted, another conforming Runtime must be able to:

1. discover or otherwise resolve the existing Process Instance;
2. recover its authoritative Execution Context;
3. re-establish the applicable EPM binding;
4. reconstruct the executable situation;
5. continue execution according to PEM semantics.

Discovery, recovery, and resumption are distinct:

```text
Discover
   ↓
Recover
   ↓
Observe
   ↓
Evaluate
   ↓
Plan
   ↓
Continue
```

The Runtime must not treat persisted continuation information as permission to bypass evaluation.

If authoritative state is insufficient to establish a valid continuation situation, the Runtime must represent the recovery deficiency rather than fabricate missing state.

## Process Instance lifecycle semantics

Process Instance lifecycle is a universal AESM/PEM semantic dimension describing the lifecycle condition of the persistent Process Instance itself.

The Runtime must preserve this distinction from:

- EPM Process State;
- engineering completion;
- Runtime lifetime;
- Agent or conversation lifetime;
- Execution Environment lifetime.

The Runtime implements lifecycle semantics; it does not define them from implementation behavior. In particular, a Runtime must not infer Process Instance termination merely from its own shutdown, restart, replacement, or loss of transient state.

A conforming Runtime must preserve lifecycle condition as authoritative recoverable state and must apply lifecycle transitions only when the applicable execution semantics permit them. Where a lifecycle transition occurs, its basis and material consequences must remain traceable.

AESM/PEM does not require a particular lifecycle API or implementation mechanism. The absence of a method named `suspend()`, `resume()`, or `terminate()` is not itself evidence of non-conformance. Conformance is determined by semantic behavior against the applicable lifecycle requirements.

## Lifecycle separation

```text
Runtime startup / restart / recovery
        ≠
Process Instance lifecycle
        ≠
Engineering completion
```

Stopping or restarting the Runtime must not silently complete or terminate a Process Instance.

Process Instance lifecycle status is authoritative operational state. Engineering completion is established by applicable EPM completion conditions. Process Instance termination is a distinct lifecycle condition governed by applicable execution semantics.

Suspension, when applicable, preserves sufficient authoritative state for later continuation. Resumption requires recovery and reevaluation under PEM rather than blind replay of a previous Runtime operation.

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
- suspension/resumption behavior where applicable;
- Process Instance termination behavior where applicable;
- completion/termination separation tests;
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
