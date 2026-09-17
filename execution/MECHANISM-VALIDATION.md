# Mechanism Configuration & Validation

**Status:** Configuration implemented; empirical Agent validation pending.

**Purpose:** Establish the minimum Execution Environment mechanism combination required for an AI Agent to participate in an AESM Process Instance, then record what is actually demonstrated versus what still requires an Agent-boundary experiment.

## Scope

This work unit does not redefine AESM semantics. The established semantic contract from the Agent Guidance Interface and Environment Mechanism Mapping work remains the authority.

The minimum mechanism combination is:

```text
Persistent Agent guidance
        +
Human task request
        +
Agent-accessible Runtime / bridge mechanism
        +
Persisted Process Instance / Execution Context
        +
Runtime-mediated authoritative operations
```

No dedicated VS Code extension, MCP server, skill, second Process Instance store, or generalized Agent orchestrator is required by the current evidence.

## Mechanism Configuration

### Persistent Agent guidance

A repository-level `AGENTS.md` has been added as the first concrete persistent-guidance mechanism.

Its role is intentionally narrow. It tells the Agent to:

- preserve the Agent / Runtime / Execution Environment boundary;
- treat persisted Process Instance / Execution Context state as authoritative;
- obtain authoritative Context before continuing governed work;
- use Runtime-mediated operations for authoritative mutations;
- distinguish engineering actions from Runtime-recognized process state;
- preserve continuity across Agent/session changes;
- avoid fabricating process evidence or claiming AESM participation without observable evidence.

The file does not redefine EPM or PEM semantics and points semantic questions back to the canonical `docs/` set.

### Task/process-specific guidance

No second persistent task-guidance system is introduced.

For a concrete task, the Human request supplies the engineering objective and the authoritative Process Instance / Execution Context supplies process-specific state after the Agent obtains it through the Runtime boundary.

### Skills

No skill mechanism is introduced by this work unit. Current evidence does not require one for the minimum path.

### Tools / MCP-equivalent mechanism

The existing Agent–Runtime bridge remains the intended authoritative execution boundary. This work unit does not add a new transport.

The empirical validation must use the actual bridge-access mechanism available in the selected Execution Environment rather than treating a repository unit test as Agent participation.

### Persisted Process Instance / Execution Context

Existing Runtime persistence remains the authoritative continuity mechanism. The Agent must recover and read this state through the supported Runtime/bridge path rather than reconstructing it from conversation history.

## Validation Status

| Capability | Repository-side status | Agent-boundary evidence required |
|---|---|---|
| Persistent guidance artifact exists | Demonstrated | Agent must demonstrably load it |
| Agent / Runtime responsibility boundary | Demonstrated by guidance and existing implementation evidence | Observe it during real execution |
| Runtime-mediated operations exist | Demonstrated by existing implementation/test evidence | Agent must invoke one through the environment |
| Process Instance persistence | Demonstrated by existing runtime validation evidence | Agent-mediated create/recover must be observed |
| Authoritative Context acquisition | Demonstrated by existing bridge/runtime evidence | Agent must obtain and use Context |
| Runtime-authoritative mutation | Demonstrated by existing runtime/bridge evidence | Agent must cause a mutation |
| Cross-session continuity | Demonstrated at Runtime/process level | Fresh Agent session must recover the same instance |
| Actual Agent participation | **Not demonstrated** | Required before DBP empirical gate |

## Required Agent-Boundary Experiment

The next validation must be performed from a fresh Agent interaction in the selected Execution Environment.

The experiment must use an ordinary engineering request rather than an AESM-specific scripted request.

The Agent must be able to demonstrate the following sequence:

```text
ordinary engineering request
        ↓
Agent receives persistent AESM guidance
        ↓
Agent establishes or recovers Process Instance
        ↓
Agent obtains authoritative Execution Context
        ↓
Agent performs genuine engineering investigation
        ↓
Agent invokes Runtime-mediated operation
        ↓
Runtime validates and persists the mutation
        ↓
Agent receives authoritative resulting state
        ↓
Agent continues engineering work
        ↓
engineering artifact + verification are produced
```

## Evidence Requirements

Capture independently observable evidence for:

1. the persistent guidance surface actually loaded by the Agent;
2. the Process Instance identifier returned or recovered through the Runtime boundary;
3. the authoritative Execution Context returned to the Agent;
4. at least one Runtime-mediated mutation caused by the Agent's work;
5. the resulting persisted Context and history;
6. the engineering artifact produced by the task;
7. verification of the engineering result;
8. continuity when the original Agent/session context is removed, if the experiment includes a second session.

Do not count the following as sufficient evidence:

- this document or `AGENTS.md` merely existing;
- documentation being read without Runtime interaction;
- bridge unit tests executed without Agent participation;
- an Agent's unverified claim that AESM was followed;
- a Process Instance created independently of the Agent and later attached to the report;
- manually fabricated Context, evidence, decisions, or history.

## Authority Checks

The experiment should include at least one observation that distinguishes Runtime authority from Agent claims. For example:

- compare Agent-visible Context with persisted Runtime state;
- verify that a Runtime mutation creates corresponding persisted history;
- verify that an unsupported direct state mutation is not treated as authoritative;
- verify that a fresh session can recover the state without relying on the previous conversation.

Only behavior actually observed in the selected environment should be recorded as demonstrated.

## DBP Readiness Gate

The repository is **not yet marked READY FOR DBP EMPIRICAL EXECUTION by this artifact alone**.

The decisive gate is a fresh real Agent execution of the selected Directories Builder Pro request:

```text
modules/reviews/forms/add-review-form.php
Add_Review_Form::business_id
Fields_Manager::SELECT → Fields_Manager::POST_SELECT
```

The DBP experiment should occur only after the Agent-boundary experiment establishes that persistent guidance delivery and Agent-to-Runtime interaction are observable in the selected environment.

## Classification Rules

- **Demonstrated:** independently observable evidence exists.
- **Evidence Incomplete:** implementation exists but the required observation is missing.
- **Implementation Gap:** a required mechanism does not exist.
- **Specification/Applicability Decision Required:** semantics or applicability cannot be resolved from existing authority.
- **Not Applicable:** the capability is not required for the selected execution path.

## Current Gate Result

**Mechanism configuration:** established at repository level.

**Mechanism validation:** evidence incomplete at the Agent boundary.

**Next gate:** execute the controlled fresh-Agent experiment in the actual Execution Environment, then decide whether the environment is ready for the real DBP vertical slice.
