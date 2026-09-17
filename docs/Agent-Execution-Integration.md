# Agent Execution Integration

## Purpose

This document describes the architectural relationship between an AI Agent, the Execution Environment, the Agent–Runtime bridge, the Runtime, and persistent Process Instance state.

It is an integration view over established AESM concepts. It does not introduce a new semantic authority, prescribe a particular transport, or make MCP, a VS Code extension, a CLI, or any particular Agent vendor normative.

## Integration boundary

The established AESM authority relationship remains:

- EPM defines engineering meaning and validity.
- PEM defines engineering execution semantics.
- Runtime implements PEM and owns authoritative Process Instance and Execution Context state.
- Process Instance is the persistent unit of engineering work.
- Execution Context is authoritative operational state for that Process Instance.
- Human and AI Agents participate in engineering work but are not Runtime authority.
- Execution Environment supplies interaction and tooling mechanisms but does not own AESM semantics.

The detailed semantic definitions remain in their governing documents rather than being duplicated here.

## Agent–Runtime bridge

The Agent–Runtime bridge is a thin adapter/access boundary between Agent-facing environment mechanisms and the Runtime. It is not a new process authority or a second process state machine.

Its integration responsibilities are:

1. request Process Instance creation when a new instance is required;
2. access or recover an existing Process Instance through Runtime when its authoritative identifier is known;
3. provide access to Runtime-owned Execution Context;
4. dispatch only Runtime operations that have been explicitly admitted to the Agent-facing boundary;
5. return authoritative Runtime results and resulting state to the Agent-facing environment mechanism.

The bridge does not:

- own Process Instance identity;
- own or duplicate Execution Context semantics;
- maintain competing authoritative persistence;
- replace ProcessStore;
- implement EPM or PEM semantics;
- independently implement lifecycle semantics;
- bypass Runtime guards;
- invent Runtime operations;
- become a generalized Agent orchestrator;
- turn technical capability into semantic authority.

### Process Instance access

For a new engineering request, Runtime remains responsible for creating the Process Instance and owning its identifier.

For continuation with a known identifier, the bridge delegates recovery/access to Runtime. The bridge does not reconstruct authoritative state from conversation history.

If objective-to-Process-Instance discovery is needed, that capability remains a Runtime concern. An Execution Environment adapter must not search persistence independently and declare its own result authoritative.

### Execution Context access

The bridge exposes Runtime-owned Context to the Agent-facing environment mechanism. Transport or serialization does not transfer authority over the Context to the bridge or Agent.

The Agent participation boundary and required Context information are defined by `06-Participants-and-Agent-Participation.md` and `05-Process-Instance-and-Execution-Context.md`.

### Runtime operation dispatch

The bridge delegates accepted requests to Runtime rather than reproducing Runtime guards, transitions, or persistence rules.

The set of operations available through the bridge is an implementation boundary and may evolve through explicit decisions. Runtime capability alone does not make an operation an Agent capability.

## Execution Environment mechanisms

An Execution Environment may combine several mechanism classes to deliver the established Agent-facing contract. AESM specifies their roles and authority relationships, not a particular product or transport.

| Mechanism class | Integration role | Authority |
|---|---|---|
| Persistent Agent guidance | Makes durable participation expectations available to the Agent | Guidance only |
| Human engineering request | Supplies immediate engineering intent | Human participation/intent as applicable |
| Callable bridge/tool mechanism | Carries Agent requests to Runtime and returns results | No independent authority |
| Persisted Process Instance / Execution Context | Preserves process identity and state across Agent/session/environment loss | Runtime / ProcessStore |
| Runtime-mediated operations | Recognize, validate, mutate, persist, or reject according to execution semantics | Runtime |

### Guidance

Persistent Agent guidance is an Execution Environment mechanism for delivering established AESM participation expectations before a specific Process Instance is known. It should point the Agent toward authoritative Context and Runtime-mediated mutation paths rather than redefine EPM or PEM.

### Callable Runtime access

A callable mechanism is required for an Agent to move from guidance to Runtime interaction. The mechanism may be programmatic, CLI-based, IDE-integrated, MCP-based, or another equivalent adapter.

No particular transport is an AESM semantic requirement.

### Optional procedural packaging

Skills or equivalent reusable procedures may package repeatable interaction patterns. They remain environment mechanisms and must not become a second state machine, authoritative Context store, or substitute for Runtime guards.

## Continuity boundary

Continuity belongs to the persistent Process Instance and Runtime-owned Execution Context, not to the lifetime of an Agent session.

A later Agent can continue a Process Instance when it can obtain the authoritative Process Instance identifier and recover the Runtime-owned state. The mechanism by which a fresh Agent receives or obtains that identifier is an Execution Environment concern, while identity and state authority remain with Runtime and ProcessStore.

The following boundaries remain distinct:

```text
Agent/session loss
        ≠
Runtime interruption
        ≠
Process Instance suspension
        ≠
Process Instance termination
```

Recovery is not itself resumption, and Runtime shutdown is not itself Process Instance termination. Detailed continuity and recovery semantics are defined by `08-Continuity-Traceability-and-Reconsideration.md` and the applicable lifecycle semantics.

## Lifecycle and completion boundary

The integration must preserve the distinction between:

- EPM Process State and Process Instance lifecycle;
- engineering completion and lifecycle termination;
- Runtime lifetime and Process Instance lifetime;
- Agent/conversation lifetime and Process Instance lifetime;
- recovery and resumption.

The detailed lifecycle authority is `11-Applicable-Process-Instance-Lifecycle-Semantics.md`. This integration document does not redefine its states, transitions, authority rules, or conformance interpretation.

## Implementation independence

The AESM integration model does not require:

- a VS Code extension;
- MCP specifically;
- a particular IDE;
- a particular CLI;
- a particular Agent vendor;
- a specific IPC, HTTP, or RPC protocol;
- a second persistence layer;
- Agent-owned Process Instance discovery.

The implementation should use the smallest available Execution Environment mechanism combination that can deliver the established semantic contract while preserving Runtime and ProcessStore authority.

## Relationship to authoritative documents

- `05-Process-Instance-and-Execution-Context.md` — Process Instance and authoritative Context.
- `06-Participants-and-Agent-Participation.md` — Agent participation boundary.
- `07-Runtime-and-Conformance.md` — Runtime responsibilities and authority.
- `08-Continuity-Traceability-and-Reconsideration.md` — continuity, history, and reconsideration.
- `11-Applicable-Process-Instance-Lifecycle-Semantics.md` — detailed lifecycle authority.

Implementation findings, validation evidence, current gaps, mechanism-specific configuration, and empirical Agent-participation records are retained under `implementation/` rather than in this canonical integration document.
