# AESM Implementation Plan

## Purpose

This document is the controlled implementation plan for turning the currently agreed AESM model into a practical, executable implementation that can be used by an AI Agent in an existing Execution Environment.

The purpose of this plan is to prevent procedural drift, accidental implementation errors, and unauthorized expansion of AESM while implementation is underway.

The plan is implementation-oriented. It does not redefine AESM semantics. The canonical AESM documentation remains the governing conceptual baseline.

## Implementation Objective

Prove, through a real executable prototype, that an engineering request can be processed as a persistent AESM Process Instance and that an AI Agent can participate in that process using mechanisms already available in an Execution Environment.

The target end-to-end capability is:

```text
Human Request
      ↓
Create / identify Process Instance
      ↓
Load / establish Execution Context
      ↓
Provide AESM guidance to AI Agent
      ↓
Agent performs engineering work
      ├── Evidence
      ├── Decisions
      ├── Artifacts
      └── Verification
      ↓
Persist updated Process Instance / Execution Context
      ↓
Agent or environment stops
      ↓
Later resume
      ↓
Recover Process Instance + Execution Context
      ↓
Continue execution
      ↓
Complete / terminate Process Instance
```

## Governing Principles

1. **Implement before expanding.** Do not expand AESM concepts merely because implementation is difficult.
2. **Use the existing AESM model as the baseline.** The Architecture Model, Operational Flow, and unified documentation set are the conceptual authority.
3. **Build a vertical slice.** The first implementation must connect Process Instance, Execution Context, Runtime, Agent guidance, persistence, execution, verification, and resume rather than developing isolated subsystems in advance.
4. **Use existing Execution Environment mechanisms.** Investigate instructions, skills, MCP, files, CLI/IDE capabilities, and equivalent mechanisms before creating AESM-specific infrastructure.
5. **Do not make AESM a VS Code product.** VS Code may be one Execution Environment, but AESM must remain independent of it.
6. **Keep Runtime, Agent, and Execution Environment distinct.** The Runtime manages process execution; the Agent performs engineering work; the Execution Environment supplies interaction and tooling capabilities.
7. **Treat persistent Process Instance state as authoritative.** Conversation history must not become the authoritative continuity mechanism.
8. **Separate guidance from enforcement.** Agent instructions guide behavior; Runtime-controlled state and constraints are used where reliable enforcement is required.
9. **Use implementation findings to justify model changes.** A change to AESM semantics requires a concrete implementation finding, not speculation.
10. **Keep the implementation minimal.** Do not add production-scale infrastructure until the prototype demonstrates that the capability is necessary.

## Scope

### In scope

- Process Instance identity and persistence
- Execution Context creation, loading, mutation, and persistence
- Minimal Runtime core
- Agent/AESM guidance interface
- Mapping AESM responsibilities to existing Execution Environment mechanisms
- Evidence, decision, artifact, and verification recording
- Process continuation after Agent/session loss
- Feedback and reconsideration
- Initial Runtime-controlled transition/constraint experiments
- Validation in at least one real Execution Environment
- Investigation of environment independence

### Explicitly out of scope for the initial prototype

- A dedicated AESM IDE extension
- A complete AESM graphical application
- A general-purpose workflow designer
- Multi-agent orchestration
- Distributed execution
- Enterprise authentication/authorization
- Production-scale infrastructure
- A new programming language or DSL
- Automatic enforcement of every AESM rule
- Speculative expansion of EPM, PEM, or the conceptual model

## Work Status Legend

- `[ ]` Not started
- `[~]` In progress
- `[x]` Complete
- `[!]` Blocked or requires explicit decision

## Controlled Implementation Work Plan

### Baseline and Scope Control

- [x] Confirm the unified `docs/` set is the canonical AESM knowledge surface.
- [x] Confirm the implementation objective: make the existing AESM process executable rather than continuing conceptual expansion.
- [x] Establish this document as the controlled implementation plan.
- [ ] Record the exact baseline commit/ref used for the first implementation experiment.
- [ ] Record any implementation assumptions that are not explicitly specified by the canonical documentation.

**Exit condition:** The implementation team can identify what is authoritative, what is experimental, and what is explicitly outside the first prototype.

### Repository and Implementation Inventory

- [x] Inventory the current repository against the implementation objective.
- [x] Classify existing implementation-related components as `KEEP`, `ADAPT`, `REPLACE`, `DELETE`, or `CREATE`.
- [x] Identify whether existing `runtime`, `tests`, `schemas`, `scripts`, `model`, or related components can be reused without importing obsolete semantics.
- [x] Identify the smallest repository structure required for the prototype.
- [x] Remove or isolate components that would introduce obsolete architectural assumptions.
- [x] Record the resulting implementation boundary in the repository.

**Exit condition:** Every retained implementation component has a current purpose tied to the executable AESM objective.

### Process Instance Persistence

- [x] Define the minimal implementation representation of a Process Instance from existing AESM semantics.
- [x] Implement Process Instance creation.
- [x] Implement stable Process Instance identification.
- [x] Implement Process Instance loading.
- [x] Implement persistent storage.
- [x] Verify that Process Instance identity survives Agent/session termination.

**Exit condition:** A Process Instance can be created, persisted, closed, and loaded again without relying on conversation history.

### Execution Context

- [x] Define the minimal authoritative Execution Context representation from existing AESM semantics.
- [x] Implement Context creation.
- [x] Implement Context loading.
- [x] Implement Context mutation.
- [x] Implement Context persistence.
- [x] Represent unresolved continuation information explicitly.
- [x] Verify that a new Agent session can reconstruct the operational situation from persisted Context.

**Exit condition:** A Process Instance can be resumed from persisted Execution Context after loss of the original Agent context.

### First Vertical Slice Definition

- [x] Select one small but genuine engineering request in an existing repository.
  - [x] Confirm the request is concrete enough to execute and verify end-to-end.
  - [x] Confirm the request is sufficiently bounded to remain a practical first vertical slice.
  - [x] Record the selected repository, component, and request boundary.
- [x] Define the engineering objective and scope of the selected request.
  - [x] Record the intended engineering outcome explicitly.
  - [x] Identify relevant requirements.
  - [x] Identify relevant constraints.
  - [x] Identify explicit exclusions from the slice.
- [x] Identify and bind the applicable EPM semantics.
  - [x] Identify the applicable EPM definition and version/revision where applicable.
  - [x] Identify only the EPM concepts actually required by the selected request.
  - [x] Preserve the EPM binding as explicit and recoverable process information.
- [x] Derive the actual Process States required by the selected request.
  - [x] Define the engineering purpose of each required state.
  - [x] Define permitted activities and expected outputs for each state.
  - [x] Define completion conditions for each state.
  - [x] Do not promote existing Runtime state strings into EPM semantics without evidence.
- [x] Derive the valid Process State transitions.
  - [x] Define the source state, transition condition, and destination state for each required transition.
  - [x] Identify required evidence, decisions, verification, gates, or other conditions governing each transition.
  - [x] Identify feedback or reconsideration paths actually required by the slice.
  - [x] Distinguish EPM transition validity from Runtime state mutation.
- [x] Derive engineering completion semantics for the selected request.
  - [x] Define the conditions under which engineering completion is valid.
  - [x] Distinguish engineering completion from Runtime termination and Agent/session termination.
  - [x] Determine whether explicit Process Instance termination is required; no new termination semantics are justified by this slice.
- [x] Derive the minimal Runtime lifecycle responsibilities from the established EPM semantics.
  - [x] Identify which transitions Runtime must execute, record, validate, or reject.
  - [x] Identify which conditions remain engineering judgments rather than Runtime responsibilities.
  - [x] Compare the derived semantics with existing `initial`, `implementation`, and `engineering_complete` representations.
  - [x] Record implementation gaps without generalizing lifecycle infrastructure prematurely.

**Exit condition:** A concrete first vertical slice has an explicit objective, applicable EPM binding, derived state/transition semantics, completion/termination semantics, and a justified minimum Runtime lifecycle boundary.

### Agent–Runtime Boundary Investigation

- [x] Review the first real Agent execution as the control condition for AESM participation.
- [x] Confirm whether a Process Instance and authoritative Execution Context participated in the observed execution.
- [x] Identify the minimum information that must cross the Agent–Runtime boundary in both directions.
- [x] Establish the responsibility boundary between Agent, Runtime, and Execution Environment.
- [x] Determine whether a particular transport such as MCP or CLI is semantically required.
- [x] Identify the minimum Agent-facing interaction surface without generalizing the Runtime API.
- [x] Record the distinction between Agent guidance and Runtime-controlled authoritative mutation.
- [x] Record the resulting implementation boundary and deferred questions.

**Exit condition:** The minimum operational Agent–Runtime interaction required for an AESM-participating Agent execution is documented without introducing a normative transport or changing AESM semantics.

### Minimal Runtime Core

- [x] Define the smallest Runtime interface required by the first vertical slice.
- [x] Implement Process Instance creation/loading operations.
- [x] Implement Context loading/saving operations.
- [x] Implement the required process-state/lifecycle operations derived from the selected vertical slice.
- [x] Implement evidence recording.
- [x] Implement decision recording.
- [x] Implement artifact association/recording.
- [x] Implement verification recording.
- [ ] Implement process completion/termination handling required by the prototype.
- [ ] Verify that Runtime responsibilities do not become Agent responsibilities.

#### Bounded Recording Capability Validation

- [x] Inspect existing decision, artifact, and verification recording implementations against the first vertical slice.
  - [x] Confirm whether each capability already exists in the current Runtime.
  - [x] Identify state and lifecycle guards.
  - [x] Identify persistence/history behavior.
  - [x] Identify differences between structured and legacy verification paths.
  - [x] Identify Runtime in-memory consistency behavior when persistence fails.
- [x] Add and execute focused behavioral tests for decision recording.
- [x] Add and execute focused behavioral tests for artifact association/recording.
- [x] Add and execute focused behavioral tests for verification recording and its preconditions.
- [x] Add and execute failure-path tests proving persisted and in-memory rollback consistency.
  - [x] The initial 53-scenario validation exposed one common caller-level rollback defect in `recognize_decision()`, `record_artifact()`, and `record_verification()`. The defect was corrected following the existing `observe()` rollback pattern. The seven affected regression scenarios passed after correction; the complete recording suite passed 53/53 and the full repository suite passed 88/88 in the recorded validation run. Commit: `009b8e2`.
- [x] Reconcile test results against the first vertical slice and decide whether implementation changes are required.
  - Minimal implementation correction required: add caller-level rollback following the existing `observe()` pattern. No AESM semantic change involved.

**Exit condition:** Behavioral validation of decision, artifact, and verification recording is complete, including failure-path consistency between live in-memory authoritative state and persisted state.

**Current status:** Complete. Decision, artifact, and verification recording are implemented and behaviorally validated. The caller-level rollback defect discovered during validation was corrected in `009b8e2` and merged into `main` through `48ad835`. The seven previously failing rollback scenarios, 53/53 recording tests, and 88/88 full-suite results are accepted as recorded execution evidence. No further recording or persistence-semantic change is authorized by the current evidence.

#### Caller-Level Recording Rollback Correction

**Status: Complete**

- [x] Restore the affected in-memory Context mutations when persistence fails in `recognize_decision()`, `record_artifact()`, and `record_verification()`.
- [x] Use the existing `observe()` rollback behavior as the implementation precedent rather than introducing a new transaction abstraction.
- [x] Verify that rollback restores the complete affected pre-operation in-memory state, including `process_state` where verification recording performs a state transition.
- [x] Preserve the existing persisted-state rollback behavior; no persistence-layer change was required.
- [x] Keep the correction implementation-only; no AESM/EPM/PEM semantic, lifecycle, or verification-path change was made.
- [x] Treat the seven previously failing behavioral scenarios as regression acceptance tests.

**Exit condition:** Satisfied. The corrected Runtime preserves consistency between in-memory authoritative state and persisted state when recording persistence fails.

### Agent Guidance Interface

- [ ] Identify the mechanisms available in the selected Execution Environment for persistent instructions.
- [ ] Identify mechanisms for task/process-specific instructions.
- [ ] Identify skill mechanisms and their appropriate scope.
- [ ] Identify MCP or equivalent external capability mechanisms.
- [ ] Define the minimum general AESM guidance supplied to the Agent.
- [ ] Define the minimum Process Instance-specific guidance supplied to the Agent.
- [ ] Define how current Execution Context is exposed to the Agent.
- [ ] Ensure guidance does not silently redefine AESM semantics.
- [ ] Ensure Agent guidance does not make conversation history authoritative.

**Exit condition:** A real Agent can receive sufficient AESM guidance to participate in the Process Instance using existing environment mechanisms.

### Agent–Runtime Execution Bridge Inspection

**Status: Complete.**

Purpose: determine the smallest operational mechanism by which a real AI Agent can receive AESM guidance and authoritative Process Instance / Execution Context information, perform engineering work in an existing Execution Environment, and cause authoritative Runtime updates without collapsing Agent, Runtime, and Execution Environment responsibilities.

Inspection targets:

- [x] Identify the actual Agent interaction surface available in the selected Execution Environment.
- [x] Trace how a real engineering request can create or identify a Process Instance.
- [x] Trace how the Agent can obtain current authoritative Execution Context.
- [x] Determine how Agent actions can invoke or otherwise interact with the Runtime without making a specific transport normative.
- [x] Determine which Runtime mutations must be authoritative and which activities remain Agent responsibilities.
- [x] Determine the minimum guidance/context exchange required for continuity.
- [x] Use the Directories Builder Pro request as the empirical target where practical.
- [x] Produce an inspection record with concrete evidence, constraints, and the smallest justified implementation boundary.

**Exit condition:** The repository contains an evidence-based design boundary for operational Agent participation, with no speculative Runtime feature or transport introduced.

**Completion:** The inspection established that the current Agent environment can invoke the existing AESM Runtime programmatically and demonstrated Process Instance creation, persistence, and cross-process recovery. However, no operational Agent–Runtime bridge exists: no mechanism currently creates a Process Instance when an engineering request arrives, no mechanism presents authoritative Execution Context to the Agent, and no mechanism connects Agent engineering activity to Runtime operations. The inspection concluded with **Outcome B — Thin Agent–Runtime Bridge Justified**, identifying the bounded bridge boundary defined later in this plan. No Runtime, specification, or DBP changes were made or required. Evidence: [`execution/AGENT-RUNTIME-EXECUTION-BRIDGE-INSPECTION.md`](execution/AGENT-RUNTIME-EXECUTION-BRIDGE-INSPECTION.md). Bridge implementation itself has **not** been authorized; the inspection produced a justified implementation direction, not a completed integration.

### Environment Mechanism Mapping

- [ ] Map each required AESM capability to a candidate Execution Environment mechanism.
- [ ] Determine what belongs in persistent instructions.
- [ ] Determine what belongs in skills.
- [ ] Determine what belongs in MCP/tools.
- [ ] Determine what belongs in persisted Process Instance/Execution Context state.
- [ ] Determine what must be controlled by the Runtime instead of merely instructed to the Agent.
- [ ] Record the mapping and its rationale.

**Exit condition:** The implementation has an explicit, testable mapping between AESM responsibilities and Execution Environment mechanisms.

#### Demonstrated mechanisms (established by bridge inspection)

The Agent–Runtime Execution Bridge Inspection demonstrated that the current Agent environment can:

- Read and write repository files.
- Execute repository commands and Python code.
- Use repository-level Agent instructions (`.agents/rules/`).
- Invoke the AESM Runtime programmatically via `run_command`.
- Create a Process Instance through Runtime invocation.
- Persist and recover Process Instance / Execution Context state.
- Recover state across separate Runtime/process execution (cross-process continuity).

#### Not yet demonstrated mechanisms

The bridge inspection did **not** demonstrate:

- Automatic AESM Runtime participation when an engineering request arrives.
- Automatic creation or discovery of the relevant Process Instance from an ordinary engineering request.
- Automatic presentation of authoritative Execution Context to the Agent.
- A functioning Agent–Runtime bridge.
- End-to-end AESM participation in a real DBP engineering request.
- Fresh-Agent continuation through such a bridge.

These are implementation gaps identified by the inspection, not implementation defects in the existing Runtime. The existing Runtime correctly implements its responsibilities; the gap is the absence of a connecting mechanism between Agent activity and Runtime operations.

### First Real Vertical Slice

- [ ] Select one small but genuine engineering request in an existing repository.
- [ ] Create its Process Instance.
- [ ] Establish its initial Execution Context.
- [ ] Start the Agent with AESM guidance.
- [ ] Execute investigation.
- [ ] Persist relevant evidence.
- [ ] Establish and persist the resulting engineering decision.
- [ ] Implement the requested change.
- [ ] Persist implementation/artifact information required for continuity.
- [ ] Perform verification.
- [ ] Reach a valid completion state.

**Exit condition:** One real engineering request has completed end-to-end under AESM process control.

### Context-Loss and Resume Validation

- [ ] Stop the original Agent session after meaningful process state has been established.
- [ ] Close or otherwise terminate the Execution Environment session.
- [ ] Start a fresh Agent session.
- [ ] Load the existing Process Instance.
- [ ] Recover the Execution Context.
- [ ] Confirm that the new Agent can determine the objective, established knowledge, decisions, completed work, unresolved issues, and required continuation without the old conversation.
- [ ] Continue and complete the process from the recovered state.

**Exit condition:** The process remains operationally continuous across Agent/session loss.

### Feedback and Reconsideration Validation

- [ ] Introduce a realistic verification failure or human feedback event.
- [ ] Persist the feedback/failure as part of process history/state as appropriate.
- [ ] Reconsider the affected decision or implementation.
- [ ] Produce an updated decision where required.
- [ ] Re-implement as necessary.
- [ ] Re-verify.
- [ ] Confirm that the process remains iterative rather than becoming a linear checklist.

**Exit condition:** The implementation demonstrates controlled feedback and reconsideration without losing prior process knowledge.

### Runtime Control Experiment

- [ ] Identify one rule that can initially be expressed as Agent guidance.
- [ ] Test whether guidance alone is sufficiently reliable.
- [ ] Identify one transition or condition that may require Runtime control.
- [ ] Implement the smallest Runtime validation needed for that condition.
- [ ] Verify the distinction between Agent guidance and Runtime enforcement.
- [ ] Do not generalize the control mechanism beyond demonstrated need.

**Exit condition:** The prototype provides evidence for which responsibilities require instructions and which require executable Runtime control.

### Environment Independence Validation

- [ ] Identify a second usable Execution Environment or execution mechanism.
- [ ] Verify that the persisted Process Instance and Execution Context remain understandable outside the first environment.
- [ ] Verify that environment-specific mechanisms are adapters/capabilities rather than AESM semantic definitions.
- [ ] Record any genuine portability limitations.

**Exit condition:** AESM remains conceptually and operationally independent of a particular Agent host or IDE.

### Prototype Evaluation and Controlled Refinement

- [ ] Review all implementation failures and unexpected behaviors.
- [ ] Classify each finding as implementation defect, environment limitation, documentation ambiguity, or genuine AESM semantic deficiency.
- [ ] Correct implementation defects without changing AESM semantics.
- [ ] Resolve environment limitations through appropriate adapters/mechanisms where justified.
- [ ] Clarify documentation only where the implementation exposed genuine ambiguity.
- [ ] Propose AESM semantic changes only for demonstrated deficiencies.
- [ ] Record every approved semantic change separately before applying it.

**Exit condition:** The prototype has produced a documented evidence-based assessment of whether the current AESM model is implementable as intended.

## Completion Criteria for the Initial Prototype

The initial prototype is complete only when all of the following are demonstrated:

- A real engineering request can be represented as a persistent Process Instance.
- The authoritative Execution Context survives Agent/session loss.
- The Agent receives sufficient AESM guidance to participate in the process.
- The Agent performs engineering work using the existing Execution Environment.
- Runtime-controlled state and constraints remain authoritative where required.
- Evidence, decisions, artifacts, and verification are persisted.
- Feedback and reconsideration can be handled without losing process knowledge.
- The process can continue after the original Agent/session ends.
- A valid engineering completion state can be reached and distinguished from Runtime/session termination.
- The implementation remains independent of a specific IDE or transport.

The prototype should be judged by demonstrated behavior and recorded evidence, not by the number of Runtime APIs or documentation pages created.

## Canonical Agent–Runtime Bridge Boundary

The following is the single canonical definition of the bounded bridge justified by the completed Agent–Runtime Execution Bridge Inspection. No alternative or expanded bridge definition is authorized elsewhere in this plan.

The bridge may provide only these responsibilities:

1. **Process Instance access** — Create or discover the relevant persistent Process Instance.
2. **Execution Context access** — Obtain the authoritative Execution Context associated with that Process Instance and make its current state available to the Agent.
3. **Runtime dispatch** — Dispatch already-supported Runtime operations on behalf of the Agent.
4. **Authoritative result/state return** — Return the authoritative Runtime result and resulting Process Instance / Execution Context state to the Agent.

The bridge is an **adapter/access boundary between the Agent and the existing Runtime**. It is not a replacement for the Runtime, Process Store, Execution Context, PEM, EPM, or Execution Environment. It must not become a generalized orchestration layer.

## Explicit Bridge Exclusions

The bounded bridge work does **not** authorize:

- A new persistence store.
- Replacement of the existing Process Store.
- Changes to Process Instance persistence semantics.
- Changes to Runtime lifecycle semantics.
- Changes to EPM semantics.
- Changes to PEM semantics.
- Changes to Execution Context semantics.
- Creation of a new lifecycle model.
- An MCP server as a normative AESM requirement.
- A VS Code extension.
- VS Code-specific architecture.
- Generalized Agent orchestration.
- Broad Runtime refactoring.
- Speculative AESM model expansion.
- Automatic behavior not justified by the inspection evidence.

If a future implementation appears to require any excluded capability, that requirement must become a separate design/authorization decision rather than being silently incorporated into the bridge.

## Forward Work Sequence

The completed inspection leads to the following bounded sequence of work units:

- [x] **Controlled Plan Reconciliation** — Reconcile the implementation plan with the completed bridge inspection evidence. Establish the bounded bridge direction and authorization gate in the plan.
- [!] **Bridge Implementation Authorization** — Explicit decision gate. See below.
- [ ] **Runtime API Inspection** — Inspect the actual existing Runtime API to determine the smallest concrete adapter contract.
- [ ] **Minimal Agent–Runtime Bridge Implementation** — Implement the bounded bridge per the canonical boundary above.
- [ ] **Bridge Behavioral Validation** — Validate that the bridge correctly connects Agent activity to Runtime operations.
- [ ] **DBP Real-Request Execution** — Execute a real DBP engineering request end-to-end under AESM process control.
- [ ] **Context-Loss / Fresh-Agent Validation** — Validate that a fresh Agent can resume from authoritative persisted state.
- [ ] **Reconciliation and Decision Gate** — Evaluate results and determine next steps.

### Bridge Implementation Authorization

**Status: Not yet passed. Explicit decision gate.**

Bridge implementation is not authorized merely because the inspection concluded that a thin bridge is justified. The authorization gate is satisfied only when the bounded bridge boundary (defined in "Canonical Agent–Runtime Bridge Boundary" above) is explicitly accepted as the implementation scope and the next Runtime API Inspection is authorized to determine the concrete adapter contract.

Until this gate is passed:

- No bridge implementation.
- No bridge tests.
- No new adapter.
- No Runtime modifications.
- No Execution Environment integration.

The gate therefore establishes authorization for **design/implementation work**, not implementation itself during this reconciliation task.

### Runtime API Inspection

**Status: Not started. Next technical investigation after authorization.**

Purpose: inspect the actual existing Runtime API and determine the smallest concrete adapter contract capable of implementing the already-authorized bridge boundary.

The Runtime API Inspection must determine, from actual code and tests:

- How Process Instances are created.
- How Process Instances are discovered or attached.
- How Execution Context is obtained.
- Which Runtime operations are already available.
- What inputs those operations require.
- What authoritative state/results they return.
- What persistence behavior already exists.
- Which operations can be exposed without changing Runtime semantics.

This inspection is not authorized to begin until the Bridge Implementation Authorization gate is passed.

## Current Progress Position

The current implementation has established the persistent Process Instance, authoritative Execution Context, minimal Runtime boundary, lifecycle control, and recording foundation. Recording rollback consistency has been corrected and behaviorally validated.

The Agent–Runtime Execution Bridge Inspection has been completed. It established that the current Agent environment can invoke the Runtime programmatically and demonstrated Process Instance persistence and recovery, but found no existing Agent–Runtime bridge or automatic AESM participation path. The inspection concluded with Outcome B — Thin Agent–Runtime Bridge Justified — identifying a bounded four-part adapter boundary.

The next objective is therefore **operational Agent participation** through the bounded bridge, not another isolated Runtime feature. The next work unit is `Bridge Implementation Authorization`, an explicit decision gate that must be passed before any bridge design or implementation work begins. After authorization, `Runtime API Inspection` determines the concrete adapter contract.

No bridge implementation, bridge tests, adapter, Runtime modification, or Execution Environment integration is authorized until the Bridge Implementation Authorization gate is explicitly passed.
