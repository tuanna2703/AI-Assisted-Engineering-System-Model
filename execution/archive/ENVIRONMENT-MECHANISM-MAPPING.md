# Environment Mechanism Mapping

## 1. Purpose and Scope

This artifact maps the AESM responsibilities required by the confirmed Agent–Runtime boundary to mechanisms already available in the selected Execution Environment.

This is an evidence and feasibility mapping task. It does **not** design or implement the Agent–Runtime bridge.

The governing boundary is the existing Runtime-owned boundary:

1. Process Instance access — create or discover the relevant persistent Process Instance.
2. Execution Context access — obtain the authoritative context and make its current state available to the Agent.
3. Runtime dispatch — dispatch already-supported Runtime operations.
4. Authoritative result/state return — return authoritative Runtime results and resulting state.

The mapping preserves Runtime ownership of Process Instance discovery and authoritative state.

## 2. Evidence Base

The mapping uses the completed Agent–Runtime Execution Bridge Inspection and the subsequent Bridge Boundary Reconciliation as primary evidence, with actual Runtime source and existing test evidence taking precedence over descriptive documentation.

Relevant established evidence includes:

- Repository file read/write is available to the Agent.
- Repository command and Python execution are available through the current environment.
- Repository-level Agent instructions exist through `.agents/rules/` in the selected engineering workspace.
- Global Agent skills are available, but no AESM-specific skill was found.
- MCP capability is available in the environment, but no AESM MCP server is configured.
- The Agent can invoke the existing AESM Runtime programmatically.
- The Runtime can create, persist, and recover Process Instances and Execution Contexts.
- Cross-process continuity has been demonstrated.
- No existing mechanism automatically creates or identifies a Process Instance from an ordinary engineering request.
- No existing mechanism automatically presents authoritative Execution Context to the Agent.
- No existing mechanism currently connects ordinary Agent engineering activity to Runtime recording operations.

The Runtime inspection additionally established that Process Instance discovery is a Runtime-owned concern and that the current Runtime exposes UUID-based attachment but no objective-to-instance search/index capability.

## 3. Mechanism Classification

### Persistent Agent instructions

**Suitable for:** stable behavioral guidance that applies to Agent participation generally within a repository/environment.

**Candidate responsibilities:**

- Tell the Agent that AESM participation is required when the environment is configured for it.
- Instruct the Agent to treat persisted Process Instance / Execution Context state as authoritative rather than conversation history.
- Instruct the Agent to use the available AESM access mechanism rather than inventing process state locally.
- State the distinction between Agent engineering work and Runtime-authoritative state mutation.

**Not suitable for:** authoritative Process Instance identity, authoritative Execution Context, or reliable enforcement of Runtime constraints.

**Evidence status:** Mechanism exists. AESM-specific configuration is not currently installed.

### Task/process-specific instructions

**Suitable for:** request-specific objective, scope, constraints, repository context, and operational instructions that are not themselves authoritative process state.

**Candidate responsibilities:**

- Convey the current engineering request to the Agent.
- Provide task-local information needed to initiate interaction with the Runtime.
- Identify environment-specific entry instructions when necessary.

**Not suitable for:** replacing the persisted Process Instance or becoming the authoritative continuity record.

**Evidence status:** General task instruction capability is available through the Agent environment; no AESM-specific task mechanism is currently configured.

### Agent skills

**Suitable for:** reusable procedural interaction patterns, such as invoking an established Runtime-access workflow or formatting information exchanged with the Runtime.

**Candidate responsibilities:**

- Encapsulate repeatable Agent-side interaction with an existing Runtime access mechanism.
- Reduce repeated procedural instructions while leaving authority in the Runtime.

**Not suitable for:** redefining AESM semantics, owning Process Instance state, or implementing independent lifecycle authority.

**Evidence status:** Global skills are available. No AESM-specific skill has been demonstrated.

### MCP or equivalent external capability mechanism

**Suitable for:** exposing existing Runtime operations to an Agent when such a mechanism is actually selected and justified.

**Candidate responsibilities:**

- Provide an Agent-callable adapter surface over already-supported Runtime operations.
- Return Runtime results and authoritative resulting state.

**Not suitable as a semantic requirement:** AESM does not require MCP specifically. The mechanism is an Execution Environment adapter choice.

**Evidence status:** MCP capability exists in the environment, but no AESM MCP server is configured or demonstrated.

### Repository files / persisted Process Instance and Execution Context

**Suitable for:** authoritative persistent process information.

**Responsibilities:**

- Persist Process Instance identity.
- Persist authoritative Execution Context.
- Preserve evidence, decisions, artifacts, verification, and continuation information according to the existing Runtime model.
- Support continuity across Agent/session loss.

**Authority:** Runtime/Process Store owns this state. The Agent may consume and contribute through Runtime operations but must not establish an independent authoritative copy.

**Evidence status:** Demonstrated. Cross-process recovery has been validated.

### CLI / Python execution

**Suitable for:** invoking the existing Runtime programmatically from the Agent's available execution capability.

**Candidate responsibilities:**

- Execute an already-existing Runtime access path.
- Support an adapter implementation without requiring a VS Code-specific extension.

**Not suitable as a semantic definition:** the use of CLI/Python is an environment mechanism, not an AESM architectural requirement.

**Evidence status:** Directly demonstrated by successful Runtime invocation through `run_command`.

## 4. Responsibility-to-Mechanism Mapping

| AESM responsibility | Preferred mechanism class | Authority | Current status | Boundary note |
|---|---|---|---|---|
| Stable general AESM participation guidance | Persistent Agent instructions | Guidance only | Available, not AESM-configured | Must not create authoritative state |
| Request-specific operational guidance | Task/process-specific instructions | Guidance only | Mechanism available | Must not replace Process Instance state |
| Repeatable Runtime interaction procedure | Agent skill or equivalent | Agent procedure | Available in principle, not AESM-configured | Skill remains an adapter/procedure |
| Process Instance creation | Existing Runtime operation invoked through environment capability | Runtime | Demonstrated | Environment triggers/invokes; Runtime creates and owns identity |
| Process Instance recovery by known ID | Existing Runtime `attach` capability | Runtime | Demonstrated | UUID remains Runtime-owned identity |
| Process Instance discovery without known ID | Runtime-owned discovery capability exposed through an environment adapter | Runtime | Not currently available | This is an identified implementation gap; mapping does not design it |
| Authoritative Execution Context retrieval | Existing Runtime context access | Runtime | Demonstrated in Runtime; not automatically presented to Agent | Environment may expose result, but authority remains Runtime |
| Runtime evidence/decision/artifact/verification operations | Existing Runtime operations through an environment capability | Runtime | Runtime operations demonstrated; Agent connection absent | No new Runtime semantics implied |
| Authoritative result/state return | Runtime operation result through environment capability | Runtime | Mechanism feasible; no AESM bridge currently exists | Returned state must remain Runtime-authoritative |
| Persistent continuity | Existing Process Store / persisted Context | Runtime | Demonstrated | Conversation history is not authoritative |
| Agent engineering work | Existing repository/IDE/CLI capabilities | Agent | Demonstrated | Agent remains responsible for engineering activity |
| Runtime enforcement/guards | Existing Runtime guards | Runtime | Demonstrated | Instructions do not replace executable authority |

## 5. Required Interaction Pattern Supported by the Mapping

The existing mechanisms support the following conceptual interaction without requiring a new AESM semantic layer:

```text
Human request
    ↓
Execution Environment provides request + AESM participation guidance
    ↓
Agent uses an environment capability to access Runtime
    ↓
Runtime creates or identifies the authoritative Process Instance
    ↓
Runtime provides authoritative Execution Context
    ↓
Agent performs engineering work using normal environment capabilities
    ↓
Agent submits applicable contributions through the Runtime access mechanism
    ↓
Runtime validates, persists, and returns authoritative resulting state
```

The mapping deliberately leaves the concrete adapter/bridge implementation unspecified.

## 6. Boundary Preservation Assessment

The mapping confirms the following ownership rules:

- **Execution Environment:** supplies interaction mechanisms and capabilities.
- **Agent:** interprets guidance, performs engineering work, investigates, reasons, edits artifacts, and requests Runtime operations.
- **Runtime:** owns authoritative process execution, Process Instance identity/state, Execution Context authority, persistence interactions, guards, and supported state mutation.
- **Process Store:** remains the persistence mechanism for Runtime-owned process state.
- **Conversation history:** remains non-authoritative continuity information.

In particular, an instruction file, skill, CLI wrapper, or MCP tool must not maintain a competing Process Instance identity or authoritative Execution Context.

## 7. Gaps Identified by the Mapping

The mapping identifies gaps but does not solve them:

1. **No request-to-Process-Instance initiation path** is currently active.
2. **No objective-to-existing-instance discovery path** is currently available without a known Process Instance identifier.
3. **No automatic Execution Context presentation path** is currently active.
4. **No operational Agent-to-Runtime contribution path** is currently active for ordinary engineering work.
5. **No AESM-specific persistent Agent guidance configuration** has been demonstrated as installed.
6. **No AESM-specific skill or MCP capability** has been demonstrated as installed.

These findings do not justify changes to Runtime semantics by themselves. They identify the capabilities that a subsequent bridge contract must address.

## 8. Mechanisms Explicitly Not Selected as Normative Requirements

The mapping does not select any of the following as an AESM semantic requirement:

- MCP specifically;
- VS Code specifically;
- a dedicated IDE extension;
- a particular CLI transport;
- a particular Agent vendor or host;
- conversation history as a state store;
- a new persistence store;
- a new generalized orchestration layer.

Any concrete choice among available environment mechanisms belongs to the subsequent bridge contract determination and implementation authorization work.

## 9. Mapping Conclusion

**Status: MAPPING COMPLETE — SUFFICIENT TO DETERMINE THE NEXT BRIDGE CONTRACT QUESTION.**

The current Execution Environment already provides the fundamental capabilities needed to host an Agent–Runtime adapter: persistent instructions, task instructions, reusable skill/tool mechanisms, repository access, command/Python execution, and durable Runtime-backed state. The existing Runtime can create, recover, mutate, and persist authoritative Process Instance / Execution Context state.

However, the environment currently provides no operational AESM path connecting an ordinary engineering request and Agent activity to those Runtime capabilities. The remaining problem is therefore an **adapter/bridge integration problem**, not a missing general-purpose Execution Environment capability and not a demonstrated need to redesign Runtime semantics.

The mapping is sufficient to move to the next controlled decision: determine the smallest concrete bridge contract that can be implemented using the mapped mechanisms while preserving Runtime ownership of Process Instance discovery and authoritative state.

No bridge implementation is authorized by this artifact.