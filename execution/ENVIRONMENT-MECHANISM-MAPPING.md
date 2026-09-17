# Environment Mechanism Mapping

> **Status:** Mapping complete. Minimum mechanism combination identified; an executable mechanism-readiness probe is added separately. This artifact does not establish a normative transport, redefine AESM semantics, or claim end-to-end AI-Agent participation.
>
> **Input contract:** `execution/AGENT-GUIDANCE-INTERFACE.md`
>
> **Validation boundary:** mechanism availability/readiness can be tested here; actual AESM participation remains an empirical gate for the later real Directories Builder Pro execution.

## 1. Purpose

This artifact maps the established Agent Guidance Interface capabilities to concrete Execution Environment mechanisms.

The purpose is operational rather than semantic:

- identify which mechanism delivers each capability;
- distinguish guidance delivery from authoritative Runtime operations;
- identify the minimum sufficient mechanism combination;
- identify mechanism gaps without moving Runtime authority into the Agent or Execution Environment;
- define a concrete validation path that can be executed before the real DBP Agent experiment.

The semantic contract is not reopened here.

## 2. Mechanism Classes

The mapping uses six mechanism classes already identified by the Agent Guidance Interface work:

1. **Persistent Agent instructions** — durable baseline instructions supplied by the Execution Environment to an Agent.
2. **Task/process-specific guidance** — information specific to the current engineering request or active Process Instance.
3. **Skills** — reusable procedural capabilities packaged for an Agent.
4. **Tools / MCP-equivalent mechanisms** — callable capabilities through which the Agent can interact with the Runtime or other authoritative systems.
5. **Persisted Process Instance / Execution Context** — authoritative process state surviving Agent/session loss.
6. **Runtime-mediated operations** — authoritative operations and guards that mutate or validate process state.

These classes are mechanisms, not AESM semantic layers. In particular, MCP, skills, repository instruction files, and CLI execution are transport or environment choices rather than additions to EPM or PEM.

## 3. Capability-to-Mechanism Mapping

| AESM capability | Primary mechanism | Supporting mechanism | Authority | Current status | Evidence required |
|---|---|---|---|---|---|
| General AESM guidance | Persistent Agent instructions | `docs/` as source material | AESM documentation | **Partially available** — content exists; durable environment delivery is not yet established in the repository baseline | Agent session demonstrably receives the required guidance before acting |
| Pre-action situational awareness | Persistent Agent instructions | Process-specific Execution Context | Agent guidance + Runtime state | **Executable in combination** | Agent demonstrates use of objective, state, evidence, decisions, risks, pending work, and authorization conditions from authoritative sources |
| Task/process-specific guidance | Persisted Execution Context | Agent task request; bridge context response | Runtime for authoritative state | **Executable for current Context fields** | Agent receives current Context from `get_context()` and uses it rather than conversation memory |
| EPM/PEM applicability | Persistent Agent instructions | Process Instance EPM/PEM fields | AESM model / Runtime-owned process state | **Evidence incomplete** — fields exist, but EPM binding is not reliably populated by the current implementation | A real Process Instance carries an explicit applicable binding that the Agent can recover |
| Process Instance creation | Tool / bridge mechanism | Runtime | Runtime | **Executable** — `AgentRuntimeBridge.create_process()` delegates to Runtime | Runtime-authoritative ID and Context are returned |
| Process Instance recovery with known ID | Tool / bridge mechanism | Persisted Process Instance | Runtime | **Executable** — `attach()` delegates to Runtime | Fresh bridge/session recovers the same authoritative state |
| Objective-to-Process-Instance discovery | Runtime-mediated operation | Tool / bridge mechanism | Runtime | **Gap** — current Runtime has no objective-to-instance discovery; bridge intentionally does not own discovery | Separate Runtime-owned discovery decision/implementation; do not substitute Agent-owned search |
| Authoritative Execution Context access | Tool / bridge mechanism | Persisted Context | Runtime | **Executable** — `get_context()` returns Runtime-owned serialized Context | Agent receives complete authoritative Context snapshot |
| Evidence recording | Tool / bridge mechanism | Persistent Context/history | Runtime | **Executable** | Agent submission causes Runtime-recognized persistent evidence |
| Decision recognition | Tool / bridge mechanism | Persistent Context/history | Runtime | **Executable** | Runtime recognizes and persists the decision through the existing bridge path |
| Artifact recording | Tool / bridge mechanism | Persistent Context/history | Runtime | **Executable** | Artifact is persisted through Runtime authority |
| Verification recording | Tool / bridge mechanism | Persistent Context/history | Runtime | **Executable** | Verification is recorded only through Runtime-controlled path and required guards |
| Process-state transitions | Tool / bridge mechanism | Persistent Context | Runtime | **Executable** for the currently bridged transitions | Runtime accepts/rejects transition and returns resulting authoritative state |
| Reconsideration | Tool / bridge mechanism | Persistent Context/history | Runtime | **Executable** | Runtime performs reconsideration and persists resulting state/history |
| Engineering completion | Tool / bridge mechanism | Persistent Context/history | Runtime | **Executable** | Runtime recognizes completion after required conditions |
| Lifecycle observation | Tool / bridge mechanism | Process Instance state | Runtime | **Executable** | Agent receives authoritative lifecycle state and respects it |
| Lifecycle transition request | Tool / bridge mechanism | Runtime lifecycle semantics | Runtime | **Specification decision remains required** — Runtime capability exists but is not exposed through the current Agent bridge surface | Explicit decision before exposing any Agent-facing lifecycle request |
| Continuity across Agent/session loss | Persisted Process Instance / Execution Context | Tool / bridge mechanism | Runtime / ProcessStore | **Demonstrated** for known-ID recovery and cross-process persistence | Fresh bridge/session reconstructs state without conversation history |
| Authority preservation | Runtime-mediated operations | Persistent Agent instructions | Runtime | **Executable** | Agent cannot directly mutate authoritative state; Runtime guards remain decisive |
| Agent procedural consistency | Persistent Agent instructions | Skills | Agent guidance | **Guidance only** | Agent follows procedure; failure to follow must not be mistaken for Runtime-authoritative success |
| Repeatable AESM procedure packaging | Skills | Persistent instructions | Agent environment | **Optional** for minimum path; no skill is required to satisfy the current semantic contract | Skill is only justified if repeated empirical work shows procedural packaging is needed |

## 4. Mechanism Roles and Boundaries

### 4.1 Persistent Agent instructions

Persistent instructions are the correct mechanism for durable baseline behavior that should apply before a particular Process Instance is known.

They should communicate, at minimum:

- AESM participation expectations;
- Agent/Runtime/Execution Environment separation;
- authority-preservation invariants;
- requirement to obtain authoritative Context before material continuation;
- prohibition on treating conversation memory as authoritative;
- requirement to use Runtime-mediated operations for authoritative mutations;
- requirement to distinguish proposals/claims from Runtime-recognized evidence, decisions, artifacts, and verification.

They should **not** duplicate or redefine EPM/PEM semantics that already live in `docs/`.

Current repository evidence does not establish a committed persistent-instruction file in the `main` branch. Therefore the mechanism is identified as the required delivery surface, but its concrete environment configuration remains a validation/implementation concern rather than being inferred from documentation alone.

### 4.2 Task/process-specific guidance

Task-specific information should be divided between:

- the human engineering request, which supplies the immediate objective;
- the authoritative Process Instance / Execution Context, which supplies persistent process-specific state.

The bridge already returns the authoritative Process Instance and complete Execution Context after creation or attachment. This is therefore the preferred source for process-specific operational state.

A separate task-guidance file is not required for the minimum mechanism combination unless the real Agent experiment demonstrates that the request plus Context cannot convey the required task-specific information reliably.

### 4.3 Skills

Skills are **not required** for the minimum operational path.

A skill may package a repeatable procedure such as:

```text
obtain Context → assess current state → perform engineering work →
submit evidence/decision/artifact/verification through Runtime
```

However, a skill must remain procedural guidance. It must not become a second process state machine, a second authoritative Context store, or a substitute for Runtime guards.

The first empirical DBP execution should therefore avoid adding a skill merely to make the experiment look more AESM-specific. A skill becomes justified only if the environment demonstrates a real repeatability or guidance-delivery need.

### 4.4 Tools / MCP-equivalent mechanisms

A callable tool mechanism is required for the Agent to move from guidance to authoritative Runtime interaction.

The current bridge already provides the minimum semantic surface:

- `create_process(objective)`;
- `attach(process_instance_id)`;
- `get_context()`;
- `dispatch(operation, params)`.

The mechanism used to expose those calls may be CLI/programmatic invocation, MCP, an IDE-integrated tool, or another equivalent adapter. None is semantically required by AESM.

The minimum requirement is observable invocation of the existing bridge and return of authoritative Runtime results/state.

### 4.5 Persisted Process Instance / Execution Context

Persisted state is the continuity mechanism, not the Agent's conversation history.

The persisted state must remain owned by Runtime/ProcessStore. The Agent and environment may read it through the supported access path but must not establish a parallel authoritative copy.

This mechanism is already demonstrated by the Runtime/ProcessStore implementation and cross-process continuity evidence.

### 4.6 Runtime-mediated operations

Runtime-mediated operations are the enforcement mechanism for capabilities that must be authoritative.

The Agent may:

- reason;
- investigate;
- propose decisions;
- produce implementation artifacts;
- perform verification work;
- request supported state-affecting operations.

The Runtime remains responsible for:

- validating supported operations;
- applying guards;
- mutating authoritative state;
- persisting state/history;
- returning authoritative results;
- rejecting unsupported or invalid operations.

This boundary must not be reproduced as a second authoritative implementation in skills or instructions.

## 5. Minimum Sufficient Mechanism Combination

The evidence supports the following minimum combination for the first real Agent execution:

```text
Persistent Agent instructions
        +
Human task request
        +
Bridge-capable tool/programmatic access
        +
Persisted Process Instance / Execution Context
        +
Runtime-mediated operations
```

### Not required for the minimum path

- a dedicated VS Code extension;
- MCP specifically;
- a skill specifically;
- a second Process Instance store;
- a separate task-guidance database;
- Agent-owned Process Instance discovery;
- a new AESM-specific IDE.

The first DBP experiment should use the smallest environment mechanism combination that is already available, rather than adding infrastructure solely for the experiment.

## 6. Mechanism Gaps

| Gap | Classification | Consequence | Resolution boundary |
|---|---|---|---|
| Durable persistent guidance delivery is not established in the repository baseline | Implementation/configuration gap | Agent may not reliably receive AESM participation rules before acting | Configure an existing environment instruction mechanism; do not change AESM semantics |
| Process Instance ID delivery to a fresh Agent | Mechanism gap | Known-ID continuation works, but a fresh Agent has no automatic identifier source | Deliver authoritative ID through the environment/bridge; do not use conversation memory as authority |
| Objective-to-instance discovery | Runtime capability gap | Ordinary no-ID continuation cannot be fully automated | Separate Runtime-owned discovery decision; bridge must not assume discovery authority |
| EPM binding population/delivery | Evidence-incomplete gap | Agent may know generic AESM semantics but not the exact EPM binding for a Process Instance | Populate/persist binding only if required by the selected vertical slice and authorized by existing semantics |
| Agent-side role/recognition honesty | Enforcement limitation | Runtime validates recognition shape, not factual truth of Agent's basis | Preserve as Agent responsibility; do not claim technical enforcement where none exists |
| Automated end-to-end Agent participation | Empirical gap | Existing tests prove bridge/runtime behavior, not AI-Agent participation | Real DBP Agent execution |

## 7. Executable Mechanism-Readiness Probe

The repository now contains:

`scripts/validate_environment_mechanisms.py`

The probe is deliberately narrower than an end-to-end Agent test. It validates the prerequisites that can be established mechanically:

1. detect common persistent-instruction surfaces;
2. detect optional skill surfaces;
3. detect repository MCP/tool configuration;
4. import the Agent–Runtime bridge;
5. verify the minimum bridge surface (`create_process`, `attach`, `get_context`, `dispatch`);
6. create a Process Instance through the bridge in an isolated temporary store;
7. recover that Process Instance through a fresh bridge instance;
8. retrieve the authoritative Execution Context.

Run from the repository root with:

```bash
python scripts/validate_environment_mechanisms.py
```

A successful run establishes **mechanism readiness**, not AESM participation.

The probe must not be interpreted as proof that an AI Agent received or followed AESM guidance.

## 8. Actual Agent Mechanism-Validation Path

After the readiness probe, the next validation is an Agent-observable experiment, not another documentation review.

### Preparation

1. Establish the selected persistent Agent instruction mechanism.
2. Start an Agent in the existing Execution Environment with no AESM-specific conversational explanation beyond the ordinary task request and the configured persistent guidance.
3. Make the bridge invocation mechanism available to that Agent.
4. Use a fresh Process Instance or an explicitly supplied authoritative Process Instance ID; do not rely on conversation memory.

### Probe sequence

```text
ordinary engineering request
        ↓
Agent receives persistent AESM guidance
        ↓
Agent establishes/obtains Process Instance identity
        ↓
Agent obtains authoritative Execution Context
        ↓
Agent performs real engineering investigation
        ↓
Agent invokes Runtime-mediated operation(s)
        ↓
Runtime validates + persists
        ↓
Agent receives authoritative resulting state
        ↓
Agent continues engineering work
```

At each boundary, record evidence of the actual mechanism used. A statement by the Agent that it "used AESM" is insufficient evidence by itself.

### Minimum observable evidence

The experiment should capture at least:

- the persistent instruction surface actually loaded by the Agent;
- the Process Instance ID returned by Runtime;
- the authoritative Context obtained by the Agent;
- at least one Runtime-mediated state mutation caused by Agent work;
- the resulting persisted Context/history;
- the engineering artifact produced in the target repository;
- verification evidence;
- enough information to distinguish Agent reasoning from Runtime-recognized state.

## 9. DBP Empirical Gate

The first real DBP execution remains the decisive empirical validation boundary.

Target request:

> Implement the selected Directories Builder Pro change under the current AESM model.

The DBP experiment should answer:

> **Did the Agent actually participate in an AESM Process Instance using the mapped Execution Environment mechanisms?**

Evidence must demonstrate a chain such as:

```text
Agent guidance delivery
        ↓
Process Instance establishment
        ↓
Authoritative Context acquisition
        ↓
Real DBP engineering work
        ↓
Runtime-mediated recognition/state mutation
        ↓
Persisted AESM process evidence
        ↓
Independent verification of DBP result
```

The experiment must reject these as sufficient on their own:

- documentation being present;
- a successful Python bridge test;
- a Process Instance existing without Agent interaction;
- Agent claims that AESM was followed;
- manually fabricated Context/evidence after the engineering work.

## 10. Validation Outcome Categories

Use these categories when assessing mechanism validation:

- **Mechanism Demonstrated** — the environment mechanism was actually invoked and observable evidence confirms its delivery/function.
- **Mechanism Available, Delivery Unproven** — the environment supports the mechanism, but no execution evidence proves that the Agent received/used it.
- **Runtime Capability Demonstrated, Agent Participation Unproven** — Runtime/bridge behavior is confirmed independently of AI-Agent execution.
- **Implementation Gap** — a required mechanism is absent and must be implemented/configured.
- **Specification/Applicability Decision Required** — the capability exists but exposing it to the Agent changes a boundary that requires an explicit decision.
- **Empirical AESM Participation Demonstrated** — reserved for the real Agent execution where the complete evidence chain is observed.

## 11. Gate for the Next Work Unit

Environment Mechanism Mapping is complete when:

- the required capabilities have a concrete mechanism mapping;
- the minimum sufficient mechanism combination is identified;
- optional mechanisms are explicitly separated from required ones;
- mechanism gaps are recorded without moving Runtime authority into the Agent/environment;
- an executable readiness probe exists;
- an actual Agent validation path is defined with observable evidence requirements;
- the DBP empirical gate remains separate from mechanism readiness.

The next work should therefore move toward **mechanism configuration/validation and the first real DBP Agent execution**, rather than reopening the Agent Guidance Interface semantics.