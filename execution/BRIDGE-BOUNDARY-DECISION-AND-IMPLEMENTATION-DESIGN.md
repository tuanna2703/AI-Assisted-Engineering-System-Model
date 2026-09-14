# Bridge Boundary Decision and Implementation Design

## Status

Bounded design task complete. Bridge implementation is not authorized by this record.

## Decision

A thin Agent–Runtime bridge is justified. The bridge should be environment-facing and transport-specific only at its adapter boundary; it must not become a second process engine or state store.

## Required interaction

```text
Engineering request
  -> discover existing Process Instance or create one
  -> obtain authoritative Execution Context
  -> present context and stable AESM participation guidance to Agent
  -> Agent investigates / reasons / performs engineering work
  -> Agent submits material contributions through bridge
  -> Runtime recognizes, validates, mutates, persists, and returns authoritative state
  -> Agent continues from returned state
```

## Boundary responsibilities

### Agent

- Engineering investigation and reasoning.
- Candidate evidence, decisions, implementation actions, and verification activity.
- Reporting uncertainty, failure, and reconsideration needs.
- No direct ownership of authoritative Process Instance state.

### Bridge

- Translate the Execution Environment interaction into a small Runtime-facing contract.
- Create or discover a Process Instance.
- Retrieve authoritative Execution Context.
- Dispatch only permitted Runtime operations.
- Return Runtime results and authoritative state to the Agent.
- Report transport or invocation failure without claiming successful Runtime mutation.

### Runtime

- Own Process Instance identity and authoritative Execution Context.
- Recognize and validate state mutations.
- Persist state/history.
- Enforce existing lifecycle/process-state conditions.
- Remain authoritative for Runtime-controlled responsibilities.

## Process Instance discovery

The existing Runtime can attach by UUID, but a fresh Agent cannot reliably discover a UUID from the current environment. The first bridge therefore needs a small discovery mechanism that maps an engineering workspace/request identity to candidate Process Instances.

The discovery mechanism must not use conversation history as authoritative state. It should return either no candidate, one unambiguous candidate, or an explicit ambiguity requiring human/Agent resolution.

A second authoritative Process Instance registry is not justified yet. Prefer a minimal persisted index/marker only if the first vertical slice demonstrates that UUID discovery cannot otherwise be supplied by the Execution Environment.

## Create versus continue

Default rule for the first prototype:

- no unambiguous matching Process Instance -> create;
- exactly one valid matching Process Instance -> continue;
- multiple plausible matches -> do not guess; surface ambiguity.

Matching criteria must be derived from stable workspace/process identity and objective information, not conversation text alone.

## Context presentation

The Agent should receive a read-only representation derived from the authoritative Execution Context containing, at minimum:

- Process Instance identity;
- engineering objective;
- current process/execution state;
- requirements and constraints;
- relevant evidence and assumptions;
- accepted/pending decisions and gates;
- implementation and verification status;
- unresolved and pending work;
- applicable authorization/execution conditions.

The representation is a view of Runtime state, not a second state model. The Runtime remains the source of truth.

## Runtime operation surface

The first bridge should expose only operations demonstrated necessary by the existing Runtime and first vertical slice:

1. create process;
2. discover/attach process;
3. obtain current context;
4. submit observation/evidence where supported;
5. recognize engineering decision where supported;
6. record artifact where supported;
7. record verification where supported;
8. obtain updated context.

Lifecycle/process-state operations should not be exposed merely for completeness. Add them only when the first vertical slice proves the Agent must request them.

## Mechanism decision

For the first prototype, use the existing Python/CLI execution capability as the initial adapter boundary because it is already demonstrated and requires no new external service. Persistent Agent guidance supplies stable participation rules. A reusable skill may later package the interaction procedure if repeated execution shows that this is useful.

MCP is not selected for the first implementation solely because it exists. It remains an alternative adapter if empirical use shows that direct execution is insufficient for reliable Agent interaction.

No VS Code-specific API is required.

## Failure behavior

The bridge must distinguish:

- Runtime operation succeeded and authoritative state changed;
- Runtime operation was rejected and authoritative state did not change;
- transport/invocation failed and mutation status is unknown;
- discovery returned ambiguity or no candidate.

The Agent must never infer successful authoritative mutation from an unsuccessful or ambiguous bridge call.

## Concurrency

No generalized multi-agent coordination mechanism is justified yet. For the first vertical slice, detect obvious conflicting attachment/write conditions where the existing Runtime can support that distinction. If real concurrent use is demonstrated, treat coordination as a separate bounded capability task.

## Implementation authorization boundary

This design authorizes preparation of a minimal adapter implementation only after this record is reconciled with the canonical AESM model and implementation plan. It does not authorize Runtime semantic changes, a new state store, an MCP server, a VS Code extension, or generalized orchestration.

## Acceptance evidence for the future implementation

A future bridge implementation should be accepted only if a fresh Agent can:

1. receive a real engineering request;
2. create or unambiguously discover its Process Instance without conversation authority;
3. obtain authoritative Execution Context;
4. perform engineering work using that context;
5. submit at least one material contribution through the Runtime boundary;
6. observe the resulting authoritative persisted state;
7. lose the Agent session;
8. start a fresh session and recover the same Process Instance/context;
9. continue without reconstructing authoritative state from the old conversation.

No implementation should be considered AESM participation merely because the Agent read AESM documentation or invoked Runtime code manually outside the normal request path.