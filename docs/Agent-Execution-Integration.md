# Agent Execution Integration

## Purpose

This document defines the architectural relationship between an AI Agent, the Execution Environment, the Agent–Runtime bridge, the Runtime, and persistent Process Instance state.

It is an integration view over established AESM concepts. It does not introduce a new semantic authority, redefine EPM or PEM, prescribe a transport, or make MCP, a VS Code extension, a CLI, or any particular Agent vendor normative.

The document answers one architectural question:

> How does an Agent participate in AESM-controlled engineering execution without becoming the owner of process semantics or authoritative process state?

Detailed semantics remain in the governing documents identified at the end of this document.

## Integration boundary

The established authority relationship is:

- EPM defines engineering meaning and validity.
- PEM defines engineering execution semantics.
- Runtime implements PEM and owns authoritative Process Instance and Execution Context state.
- Process Instance is the persistent unit of engineering work.
- Execution Context is authoritative operational state for that Process Instance.
- Human Participants and AI Agents participate in engineering work but are not Runtime authority.
- Execution Environment supplies interaction and tooling capabilities but does not own AESM semantics.

The integration architecture therefore has three distinct concerns:

```text
Agent participation
        │
        ▼
Execution Environment
        │
        │ Agent-facing interaction
        ▼
Agent–Runtime bridge
        │
        │ Runtime-mediated access / requests / results
        ▼
Runtime
        │
        ▼
Process Instance + authoritative Execution Context
```

The bridge connects these concerns; it does not collapse them.

## Agent–Runtime bridge

The Agent–Runtime bridge is a semantic architectural boundary between Agent-facing interaction and Runtime authority. An implementation may realize that boundary through one or more environment mechanisms, but the boundary itself is not a transport, API, process state machine, or persistence layer.

The bridge has four architectural responsibilities:

1. **Process access** — establish access to a new or existing Process Instance through Runtime, including creation when a new instance is required and recovery when authoritative identity is known.
2. **Context access** — expose Runtime-owned Execution Context to the Agent-facing side without transferring ownership or authority over that Context.
3. **Operation mediation** — carry accepted Agent requests to Runtime operations that are explicitly admitted to the Agent-facing boundary. Runtime remains responsible for recognition, authorization, execution semantics, guards, mutation, and persistence.
4. **Result propagation** — return authoritative Runtime results and resulting state to the Agent-facing environment so the Agent can continue from authoritative information rather than from an assumed local state.

These responsibilities define the architectural boundary; they do not prescribe a one-to-one software interface. Process creation, known-identifier recovery, Context access, operation dispatch, and result return are examples of behavior that may realize the four responsibilities.

The bridge does not:

- own Process Instance identity;
- own or duplicate Execution Context semantics;
- maintain competing authoritative persistence;
- replace ProcessStore;
- implement EPM or PEM semantics;
- independently implement lifecycle semantics;
- bypass Runtime guards or authorization;
- invent Runtime operations;
- become a generalized Agent orchestrator;
- turn technical capability into semantic authority.

### Process access and discovery

For a new engineering request, Runtime remains responsible for establishing the Process Instance and owning its identity.

For continuation with a known identifier, the bridge delegates access or recovery to Runtime. It does not reconstruct authoritative state from conversation history.

If objective-to-Process-Instance discovery is required, discovery remains a Runtime responsibility. An Execution Environment adapter must not search persistence independently and declare its own result authoritative. The environment may provide the technical capabilities used by Runtime discovery without acquiring semantic ownership of discovery.

### Context access

The bridge exposes Runtime-owned Context to the Agent-facing environment. Serialization, copying, or transport does not transfer authority over Context to the bridge or Agent.

The information an Agent should establish before material action is defined by `06-Participants-and-Agent-Participation.md`; the authoritative Context model is defined by `05-Process-Instance-and-Execution-Context.md`.

### Operation mediation

The bridge delegates accepted requests to Runtime rather than reproducing Runtime guards, transitions, recognition, authorization, or persistence rules.

Runtime capability alone does not make an operation an Agent capability. The Agent-facing operation surface is therefore an explicit integration boundary that may evolve through implementation evidence and explicit decisions.

### Result propagation

Results returned through the bridge distinguish authoritative Runtime state from Agent-local interpretation. The Agent may reason over returned state and produce further contributions, but those contributions re-enter the Runtime-controlled recognition and mutation boundary before becoming authoritative.

## Execution Environment role

The Execution Environment is the realization surface through which a Human or Agent interacts with the engineering system. It can provide mechanisms for delivering guidance, presenting Context, invoking the bridge, handling returned results, and performing engineering work on external artifacts.

AESM does not require a fixed inventory of environment mechanisms. Different environments may realize the same architectural roles through different combinations of instructions, task configuration, reusable procedures, tools, command execution, programmatic interfaces, IDE integration, or equivalent capabilities.

The architectural requirement is functional rather than product-specific:

```text
Guidance and authoritative Context
              ↓
      Agent understanding
              ↓
       Agent contribution
              ↓
       Bridge interaction
              ↓
      Runtime recognition
              ↓
  Permitted authoritative mutation
              ↓
       Runtime result / state
              ↓
     Environment returns state
              ↓
       Agent continues work
```

### Guidance

Guidance is an environment-level means of making established AESM participation expectations available to an Agent. It should direct the Agent toward authoritative Process Instance / Execution Context information and Runtime-mediated mutation paths.

Guidance does not itself establish authority, create authoritative state, or redefine EPM/PEM semantics. The particular mechanism used to deliver it is an implementation choice.

### Runtime access

An Agent must have some callable path from the Execution Environment to the Agent–Runtime bridge if it is to participate in Runtime-mediated execution. That path may be programmatic, command-based, IDE-integrated, service-based, or another equivalent realization.

The transport and interface technology are not AESM semantics. What matters architecturally is that the path preserves the bridge boundary and returns authoritative Runtime results rather than creating a competing local authority.

### Procedural packaging

Reusable procedures or skills may package repeatable interaction patterns. They remain Execution Environment mechanisms and must not become a second process state machine, authoritative Context store, or substitute for Runtime guards and semantic decisions.

## Continuity integration consequence

Continuity is provided by the persistent Process Instance and Runtime-owned Execution Context, not by the lifetime of an Agent session or conversation.

A later Agent can participate in the same Process Instance when the environment provides a way to obtain the authoritative Process Instance identity and the bridge/Runtime can recover authoritative state. The delivery or discovery mechanism for that identity is an environment/implementation concern; identity and state authority remain with Runtime and ProcessStore.

The integration must preserve these distinctions:

```text
Agent/session loss
        ≠
Runtime interruption
        ≠
Process Instance suspension
        ≠
Process Instance termination
```

Recovery is not itself resumption, and Runtime shutdown is not itself termination. Detailed continuity and recovery semantics remain governed by `08-Continuity-Traceability-and-Reconsideration.md`; lifecycle semantics remain governed by `11-Applicable-Process-Instance-Lifecycle-Semantics.md`.

## Lifecycle integration consequence

The integration boundary must preserve the distinction between:

- EPM Process State and Process Instance lifecycle;
- engineering completion and lifecycle termination;
- Runtime lifetime and Process Instance lifetime;
- Agent/conversation lifetime and Process Instance lifetime;
- recovery and resumption.

The integration architecture does not define lifecycle states, transitions, triggers, authority, preservation, or conformance rules. It only requires that bridge and environment mechanisms do not bypass or silently reinterpret those semantics. Detailed lifecycle authority is `11-Applicable-Process-Instance-Lifecycle-Semantics.md`.

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

An implementation should use the smallest available Execution Environment mechanism combination that can realize the architectural roles described here while preserving Runtime and ProcessStore authority.

Implementation findings, validation evidence, current gaps, mechanism-specific configuration, and empirical Agent-participation records belong under `implementation/` rather than in this canonical integration document.

## Relationship to authoritative documents

- `05-Process-Instance-and-Execution-Context.md` — Process Instance and authoritative Context.
- `06-Participants-and-Agent-Participation.md` — Agent participation semantics and authority boundary.
- `07-Runtime-and-Conformance.md` — Runtime responsibilities, recognition, mutation, continuity, and conformance.
- `08-Continuity-Traceability-and-Reconsideration.md` — continuity, history, and reconsideration.
- `11-Applicable-Process-Instance-Lifecycle-Semantics.md` — detailed lifecycle authority.

This document supplies the integration architecture between those authorities; it does not replace them.