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

1. establish, attach to, or recover Process Instances;
2. establish, access, maintain, and recover Execution Context;
3. evaluate the current executable situation according to PEM;
4. receive and interpret relevant inputs, observations, contributions, results, verification, failures, and continuation information;
5. distinguish informational content from mutation-relevant content;
6. recognize information under EPM/PEM semantics;
7. evaluate Process States and transition conditions;
8. recognize and handle Decision Gates;
9. make Execution Determinations;
10. plan and coordinate permissible actions;
11. record Execution Results;
12. support verification;
13. apply only permitted state mutations;
14. preserve pending work;
15. preserve traceability and history;
16. support reconsideration without erasing history;
17. preserve continuity information;
18. represent material failure and uncertainty explicitly;
19. support suspension, resumption, recovery, and termination according to applicable semantics.

These are semantic obligations, not a required software decomposition.

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

Recognition must consider applicable Process State, execution conditions, operation semantics, authority conditions, required context, validity constraints, and traceability.

A Runtime must not silently convert an informational or candidate input into authoritative state.

## State transition boundary

EPM defines engineering transition validity. PEM defines execution handling.

Therefore:

```text
EPM transition validity
        ≠
Runtime technical ability to move state
```

The Runtime must not create, bypass, or redefine engineering transition validity.

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
Permitted mutation
 ↓
Updated Execution Context
 ↓
Traceability
```

## External actions

Actions performed through Agents, Participants, Tools, or environment-facing capabilities remain under applicable Runtime execution control.

The Runtime should preserve the distinction between requested action, performed action, reported result, recognized result, verified result, and state mutation.

## Continuity and Runtime replacement

A conforming Runtime must support continuation from authoritative Execution Context.

Runtime-specific transient memory is not authoritative merely because it is internal to the Runtime.

Where Runtime replacement is permitted, another conforming Runtime must be able to continue from the authoritative state and associated records required for continuation.

## Lifecycle separation

```text
Runtime startup / restart / recovery
        ≠
Process Instance lifecycle
        ≠
Engineering completion
```

Stopping or restarting the Runtime must not silently complete or terminate a Process Instance.

## Conformance

A Runtime claiming conformance must demonstrate preservation of at least:

1. EPM engineering validity;
2. PEM execution semantics;
3. AESM operational boundaries;
4. Agent interaction boundaries;
5. controlled state mutation;
6. authority separation;
7. traceability;
8. continuity;
9. failure and uncertainty;
10. lifecycle separation;
11. transition and Decision Gate semantics;
12. implementation independence.

## Conformance evidence

Useful evidence categories include:

- Execution Context reconstruction;
- execution-trace reconstruction;
- initialization and recovery tests;
- authority-boundary tests;
- operation-recognition tests;
- state-transition tests;
- Decision Gate blocking/progression tests;
- mutation-control tests;
- external action/result traceability tests;
- failure and uncertainty tests;
- continuity and Runtime replacement tests;
- completion/termination separation tests.

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