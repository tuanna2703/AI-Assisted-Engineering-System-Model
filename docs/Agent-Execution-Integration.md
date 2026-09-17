# Agent Execution Integration

## Purpose

This document consolidates the durable architectural and operational conclusions produced while validating how an AI Agent participates in AESM through an Execution Environment.

It defines the relationship between Agent guidance, Process Instance access, the Agent–Runtime bridge, Runtime authority, persisted Execution Context, and the mechanisms available in an Execution Environment.

It does **not** introduce a new AESM semantic layer, prescribe a particular transport, or make MCP, a VS Code extension, a CLI, or any particular Agent vendor normative.

## Scope and authority

The semantic authorities remain:

- EPM defines engineering meaning and validity.
- PEM defines engineering execution semantics.
- Runtime implements PEM and owns authoritative Process Instance and Execution Context state.
- Process Instance is the persistent unit of engineering work.
- Execution Context is authoritative operational state for that Process Instance.
- Human and AI Agents are Participants, not Runtime authority.
- Execution Environment supplies interaction and tooling mechanisms; it does not own AESM semantics.

This document applies those established semantics to the concrete Agent/Execution Environment integration boundary.

## Agent guidance contract

Before a material contribution, the Agent should establish from authoritative state and applicable semantics:

1. Engineering Objective;
2. current Requirements and Constraints;
3. current Process State;
4. relevant Evidence and Assumptions;
5. accepted and pending Engineering Decisions;
6. applicable Decision Gates;
7. implementation and verification status;
8. unresolved questions, risks, contradictions, and failures;
9. pending work and expected next actions;
10. applicable authorization or execution conditions.

Missing authoritative information must be represented as missing rather than silently inferred from conversation memory.

The Agent's conversation history is working memory only. It is never a substitute for the authoritative Process Instance and Execution Context.

## Controlled Agent contribution

The semantic contribution path is:

```text
Agent
  ↓
Observation / Candidate Contribution / Request
  ↓
Runtime-controlled recognition and validation
  ↓
Permitted state mutation
  ↓
Authoritative Execution Context / history
```

The Agent may investigate, reason, propose decisions, create artifacts, perform verification work, report results, and request supported Runtime operations. It does not independently determine which output becomes authoritative state.

The following invariants remain mandatory:

```text
Agent ≠ Runtime
Agent capability ≠ authority
Agent output ≠ automatic authority
Proposal ≠ authorization
Observation ≠ mutation
Engineering Decision ≠ Execution Determination
Conversation ≠ authoritative state
```

## Agent–Runtime bridge

The Agent–Runtime bridge is a thin adapter/access boundary. It is not a new process authority or a second process state machine.

Its durable semantic responsibilities are:

1. Process Instance creation when a new instance is required;
2. recovery/access to an existing Process Instance when its authoritative identifier is known;
3. authoritative Execution Context access;
4. dispatch of Runtime operations that are explicitly within the accepted Agent-facing boundary;
5. return of authoritative Runtime results and resulting state.

The bridge must not:

- own Process Instance identity;
- own or duplicate Execution Context semantics;
- maintain competing authoritative persistence;
- replace ProcessStore;
- implement EPM or PEM semantics;
- independently implement lifecycle semantics;
- bypass Runtime guards;
- invent Runtime operations;
- perform generalized Agent orchestration;
- turn technical capability into semantic authority.

### Process Instance access

For a new engineering request, the Runtime creates the Process Instance and owns its identifier.

For continuation with a known identifier, the bridge delegates to Runtime recovery/attachment. The bridge must not reconstruct authoritative state from conversation history.

Objective-to-Process-Instance discovery remains a Runtime responsibility. The current Runtime does not provide objective-to-instance search/list capability. The bridge therefore must not search persisted files and declare a result authoritative on its own.

The discovery gap is an implementation dependency, not permission to move discovery authority into the bridge or Agent.

### Execution Context access

The bridge presents a snapshot of Runtime-owned Execution Context. It may serialize or transport the snapshot but does not become its owner.

At minimum, the Agent must be able to obtain the objective, Process State, lifecycle state, evidence, decisions, artifacts, verification information, unresolved matters, pending work, completion state, and other fields present in the authoritative Context.

### Runtime operation dispatch

The bridge may expose only operations accepted as part of the Agent-facing boundary. Dispatch means delegation to the existing Runtime implementation; it is not permission to reproduce Runtime guards or state transitions in the bridge.

The currently demonstrated bridge surface includes the supported engineering operations for investigation, observation, decision recognition, implementation, artifact recording, verification, reconsideration, and engineering completion, together with Process Instance creation, known-ID attachment, and Context access.

`set_pending_execution`, direct lifecycle determination, and Runtime `stop` remain outside the Agent-facing bridge boundary unless a separate explicit decision changes that boundary. Their existence as Runtime methods does not automatically make them Agent capabilities.

Lifecycle authority remains with applicable execution semantics and Runtime. The Agent may request or propose lifecycle action where the applicable semantics permit such a request, but technical access to a lifecycle mutation operation is not itself authority to perform it.

## Execution Environment mechanism model

The Execution Environment can deliver the Agent-facing contract through combinations of existing mechanisms. AESM does not prescribe one transport.

### Required mechanism classes

The minimum sufficient combination for the first real Agent execution is:

```text
Persistent Agent instructions
        +
Human engineering request
        +
Bridge-capable tool/programmatic access
        +
Persisted Process Instance / Execution Context
        +
Runtime-mediated operations
```

Their roles are distinct:

| Mechanism | Role | Authority |
|---|---|---|
| Persistent Agent instructions | Deliver durable AESM participation guidance before a specific Process Instance is known | Guidance only |
| Human task request | Supply immediate engineering intent | Human intent as applicable |
| Bridge-capable tool/programmatic access | Carry Agent requests to Runtime and return authoritative results | No independent authority |
| Persisted Process Instance / Execution Context | Preserve process identity and state across Agent/session/environment loss | Runtime / ProcessStore |
| Runtime-mediated operations | Validate, mutate, persist, and reject according to PEM and Runtime rules | Runtime |

### Persistent Agent instructions

Persistent instructions are the preferred mechanism for baseline guidance that must be available before the Agent knows a Process Instance.

They should communicate participation expectations, authority boundaries, the requirement to obtain authoritative Context, the prohibition on treating conversation history as authoritative, and the requirement to use Runtime-mediated paths for authoritative mutation.

They should not duplicate or redefine the detailed EPM/PEM specifications.

Repository evidence does not establish a committed persistent-instruction surface in the AESM repository baseline. Therefore the requirement is established, but its concrete environment configuration remains an implementation/configuration concern.

### Task-specific guidance

Task-specific operational information should normally come from two sources:

- the human engineering request for immediate objective and intent;
- the authoritative Process Instance / Execution Context for persistent process-specific state.

A separate task-guidance database is not required for the minimum path.

### Skills

Skills are optional procedural packaging. They are not required for the minimum Agent execution path.

A skill may package a repeatable procedure such as obtaining Context, assessing the current state, doing engineering work, and submitting recognized results through Runtime. A skill must never become a second state machine, second authoritative Context store, or substitute for Runtime guards.

### Tools and MCP-equivalent mechanisms

A callable mechanism is required for the Agent to move from guidance to Runtime interaction. The bridge can be exposed through CLI/programmatic invocation, MCP, IDE-integrated tooling, or another equivalent adapter.

No one of these mechanisms is semantically required by AESM.

## Continuity

Continuity belongs to the persistent Process Instance and Runtime-owned Execution Context, not to the Agent session.

A later Agent can continue a Process Instance when it can obtain the authoritative Process Instance identifier and recover the Runtime-owned state. Known-ID cross-process recovery has been behaviorally demonstrated.

The remaining delivery problem is therefore not persistence itself but how a fresh Agent receives or obtains the authoritative Process Instance identifier. That mechanism must not elevate conversation history into an authoritative registry.

The lifecycle distinction must also remain explicit:

```text
Agent/session loss
        ≠
Runtime interruption
        ≠
Process Instance suspension
        ≠
Process Instance termination
```

Recovery does not itself imply resumption, and Runtime shutdown does not itself terminate the Process Instance.

## Lifecycle and completion boundaries

The validated implementation distinguishes:

- EPM Process State from Process Instance lifecycle;
- engineering completion from lifecycle termination;
- Runtime lifetime from Process Instance lifetime;
- Agent/conversation lifetime from Process Instance lifetime;
- recovery from resumption.

The authoritative detailed lifecycle semantics are defined by `11-Applicable-Process-Instance-Lifecycle-Semantics.md`.

The implementation evidence recorded that:

- engineering completion requires successful verification;
- engineering completion does not by itself terminate the Process Instance;
- Runtime interruption does not terminate the Process Instance;
- authorized termination persists and survives recovery;
- terminated Process Instances reject further lifecycle transitions;
- lifecycle state and history remain Runtime-authoritative.

These are implementation/conformance observations, not new lifecycle semantics.

## Evidence levels

The repository's validation work established an important evidence distinction:

```text
Documentation exists
        ≠
Agent received guidance
        ≠
Agent followed guidance
        ≠
Agent interacted with Runtime
        ≠
Runtime-authoritative state changed
        ≠
End-to-end AESM Agent participation was demonstrated
```

The deterministic bridge and Runtime tests demonstrate Runtime/bridge behavior. They do not, by themselves, demonstrate that an actual AI Agent received and followed AESM guidance during real engineering work.

The first real Directories Builder Pro execution remains the empirical gate for end-to-end participation.

## Mechanism-readiness validation

The repository contains `scripts/validate_environment_mechanisms.py`. Its purpose is limited to mechanical readiness. It checks for common instruction/skill/tool surfaces, verifies the bridge import and minimum bridge surface, creates a Process Instance through the bridge in an isolated store, recreates the bridge, and recovers authoritative Context.

A successful readiness probe means that the mechanisms are available and the bridge/runtime path is usable. It does not prove AI-Agent participation.

## Empirical Agent participation gate

The real Agent validation should observe the following chain:

```text
Ordinary engineering request
        ↓
Persistent AESM guidance delivered to Agent
        ↓
Process Instance established/recovered
        ↓
Authoritative Context obtained
        ↓
Real engineering work performed
        ↓
Runtime-mediated operation invoked by Agent
        ↓
Runtime validates + persists
        ↓
Agent receives authoritative resulting state
        ↓
Engineering result independently verified
```

Minimum evidence should include:

- the actual persistent guidance surface loaded by the Agent;
- the authoritative Process Instance ID;
- the authoritative Context obtained by the Agent;
- at least one Runtime-mediated mutation caused by Agent work;
- resulting persisted Context/history;
- the actual engineering artifact;
- verification evidence;
- enough traceability to distinguish Agent reasoning from Runtime-recognized state.

The following are insufficient by themselves:

- AESM documentation merely existing in the repository;
- a successful deterministic Python bridge test;
- a Process Instance existing without Agent interaction;
- an Agent statement that AESM was followed;
- manually fabricated Context or evidence after the work.

## Current gaps and decisions

| Area | Current status | Required boundary |
|---|---|---|
| Durable Agent guidance delivery | Mechanism/configuration gap | Configure an existing environment instruction surface; do not alter AESM semantics |
| Process Instance ID delivery to a fresh Agent | Mechanism gap | Deliver authoritative identity through the environment/bridge |
| Objective-to-instance discovery | Runtime capability gap | Resolve separately under Runtime ownership |
| EPM binding population/delivery | Evidence incomplete | Ensure explicit recoverable EPM binding where required by the applicable model |
| Agent-side recognition honesty | Enforcement limitation | Remains an Agent responsibility; do not claim technical enforcement beyond Runtime validation |
| Lifecycle request exposure through bridge | Specification decision required | Do not expose lifecycle mutation merely because Runtime supports it |
| End-to-end AI-Agent participation | Empirical gap | Validate through the real DBP execution |

## Validation evidence retained from the implementation work

The consolidated execution artifacts recorded successful deterministic validation of the bridge/runtime prototype, including Process Instance creation, known-ID recovery, Context access, Runtime operation dispatch, persistence, continuity, reconsideration, lifecycle boundaries, and completion/termination separation.

A recorded full-suite validation at the relevant implementation point reported **137/137 tests passing**. This is historical evidence tied to that validation run, not a claim that those tests were executed in the current documentation-cleanup operation.

The validation artifacts also established that no successful bridge test should be interpreted as proof of genuine AI-Agent participation.

## Implementation independence

Nothing in this document requires:

- a VS Code extension;
- MCP specifically;
- a particular IDE;
- a particular CLI;
- a particular Agent vendor;
- a specific IPC/HTTP/RPC protocol;
- a second persistence layer;
- Agent-owned Process Instance discovery.

The correct implementation is the smallest environment mechanism combination that can deliver the established semantic contract while keeping Runtime and ProcessStore authoritative.

## Relationship to other AESM documents

- `06-Participants-and-Agent-Participation.md` defines the Agent's semantic participation boundary.
- `07-Runtime-and-Conformance.md` defines Runtime responsibilities and authority.
- `08-Continuity-Traceability-and-Reconsideration.md` defines continuity, history, and reconsideration relationships.
- `11-Applicable-Process-Instance-Lifecycle-Semantics.md` is the detailed lifecycle semantic authority.
- This document defines the durable Agent/Execution Environment integration view without replacing those authorities.
