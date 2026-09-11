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
- [ ] Implement decision recording.
- [ ] Implement artifact association/recording.
- [ ] Implement verification recording.
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
  - [!] Behavioral validation is complete, but all 7 failing scenarios confirm one common caller-level rollback defect: `recognize_decision()`, `record_artifact()`, and `record_verification()` mutate the in-memory Context before `save_context()` and do not restore the mutation when persistence fails. The persistence layer itself rolls back persisted state correctly. See `execution/RUNTIME-CAPABILITY-BEHAVIORAL-VALIDATION.md`.
- [x] Reconcile test results against the first vertical slice and decide whether implementation changes are required.
  - Minimal implementation correction required: add caller-level rollback following the existing `observe()` pattern. No AESM semantic change involved.

**Exit condition:** Behavioral validation of decision, artifact, and verification recording is complete. The capability remains open until the confirmed caller-level rollback defect is corrected and the regression evidence demonstrates that failed persistence leaves both in-memory and persisted state unchanged.

**Current inspection finding:** Decision, artifact, and verification recording already exist in `runtime/core/runtime.py`; no new Runtime feature is justified. Behavioral validation produced 53 tests with 46 passing and 7 failing, all attributable to the same caller-level rollback defect in the three recording methods. The defect is an implementation correction, not an AESM semantic gap. The existing `observe()` rollback behavior is the implementation precedent.

#### Caller-Level Recording Rollback Correction

- [ ] Restore the affected in-memory Context mutations when persistence fails in `recognize_decision()`, `record_artifact()`, and `record_verification()`.
- [ ] Use the existing `observe()` rollback behavior as the implementation precedent rather than introducing a new transaction abstraction.
- [ ] Verify that rollback restores the complete affected pre-operation in-memory state, not merely the newly recorded list entry.
- [ ] Preserve the existing persisted-state rollback behavior; do not modify `save_context()` or the persistence architecture unless evidence proves it necessary.
- [ ] Keep the correction implementation-only; do not alter AESM/EPM/PEM semantics, lifecycle semantics, or structured/direct verification-path semantics.
- [ ] Treat the 7 currently failing behavioral scenarios as regression acceptance tests.

**Exit condition:** All seven regression scenarios pass, the complete recording test suite passes, and failed persistence leaves the Runtime's in-memory authoritative state and persisted state unchanged.

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

### Environment Mechanism Mapping

- [ ] Map each required AESM capability to a candidate Execution Environment mechanism.
- [ ] Determine what belongs in persistent instructions.
- [ ] Determine what belongs in skills.
- [ ] Determine what belongs in MCP/tools.
- [ ] Determine what belongs in persisted Process Instance/Execution Context state.
- [ ] Determine what must be controlled by the Runtime instead of merely instructed to the Agent.
- [ ] Record the mapping and its rationale.

**Exit condition:** The implementation has an explicit, testable mapping between AESM responsibilities and Execution Environment mechanisms.

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
- [ ] Persist verification results.
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

- [ ] A human can initiate a real engineering request.
- [ ] A persistent Process Instance is created.
- [ ] An authoritative Execution Context is established and persisted.
- [ ] An AI Agent receives AESM guidance through existing Execution Environment mechanisms.
- [ ] The Agent can perform investigation and engineering work.
- [ ] Evidence is persisted.
- [ ] Decisions are persisted.
- [ ] Implementation artifacts are associated with the process.
- [ ] Verification is performed and recorded.
- [ ] Feedback/reconsideration can occur.
- [ ] The process can survive Agent/session loss.
- [ ] A new Agent can resume from persisted state.
- [ ] The process can reach completion/termination.
- [ ] Runtime, Agent, and Execution Environment responsibilities remain distinct.
- [ ] No environment-specific mechanism has silently become an AESM semantic requirement.
- [ ] No AESM semantic expansion has been introduced without an implementation-based justification.

## Change Control

The following rules apply to this plan.

### No unauthorized expansion

A new implementation task must not be added merely because it appears useful, interesting, or architecturally elegant.

A proposed addition must identify:

1. the concrete implementation problem it solves;
2. why the existing plan cannot solve that problem;
3. whether the addition changes AESM semantics or only implementation;
4. the specific plan section affected.

### No silent semantic changes

Implementation convenience must not redefine EPM, PEM, Runtime, Process Instance, Execution Context, Agent, Human Participant, or Execution Environment semantics.

### No premature generalization

A mechanism demonstrated for one prototype scenario must not automatically become a general AESM requirement.

### Completion marking

A task may be marked `[x]` only when its stated exit condition has been satisfied with implementation evidence. Partial work uses `[~]`; blocked work uses `[!]` with the reason recorded nearby.

### Next-step rule

After each completed task, the next task is the first unchecked task whose prerequisites are satisfied. Do not skip ahead merely to build a preferred component.

### Dynamic task decomposition

During execution, if a task proves too broad to execute or verify as a single unit, it must be decomposed into semantically meaningful nested subtasks under the parent task rather than being tracked informally outside this plan. If execution reveals a genuinely necessary task that is not represented by the current plan, add it directly to the appropriate work-plan section. Any such addition must follow the change-control rules above and preserve the dependency order of the plan.

## Current Status

**Plan status:** Implementation in progress.

**Completed immediately before the current step:** Process Instance persistence, Execution Context implementation/verification, Minimal Runtime interface definition, Process lifecycle implementation/validation, Agent–Runtime boundary investigation, First Vertical Slice Definition, Evidence Recording implementation/validation/reconciliation, and behavioral validation of the existing decision, artifact, and verification recording capabilities.

**Current next step:** Execute the bounded Caller-Level Recording Rollback Correction. No recording capability should be marked complete until the seven regression scenarios and the complete recording validation pass with persisted and in-memory rollback consistency demonstrated.

**Selected first vertical slice:** `tuanna2703/directories-builder-pro` — Reviews module — `Add_Review_Form::business_id` conversion from `SELECT` to `POST_SELECT`, including WP post ID → `dbp_businesses.id` persistence translation.

**Important implementation boundary established:** The Agent–Runtime investigation does not justify a normative transport choice or a generalized orchestration layer. The first vertical slice establishes four derived engineering states — Investigation, Implementation, Verification, and Engineering Complete — plus a feedback path from failed Verification to Investigation/Implementation. These are slice-specific semantics, not universal AESM state identifiers.

**Termination boundary:** The first vertical slice establishes engineering completion conditions but does not justify inventing a separate Process Instance terminal state or generalized termination semantics. Engineering completion, Process Instance termination, Runtime termination, and Agent/session termination remain distinct.

## Evidence and Change Record

- **Process Instance persistence implementation:** The existing Runtime already provided `ProcessInstance.create()`, UUID-based identity, `ProcessStore.create()`, `ProcessStore.load_instance()`, and JSON persistence. No change to `runtime/core/models.py` was necessary for this task.
- **Creation test:** Added `test_process_instance_creation` to `tests/continuity/test_runtime_recovery.py`, covering generated identity, objective, active lifecycle, Execution Context reference, EPM/PEM references, and timestamps.
- **Persistence/recovery evidence:** Existing `test_process_and_context_survive_runtime_replacement` verifies that a Process Instance created by one Runtime can be loaded by another Runtime after the first Runtime stops, including recovery of the same Process Instance identity.
- **Implementation commit:** `3dacf70292a5aeee8edbca645a26000d3691d5d3`.
- **Execution Context verification:** `verification_report.md` confirms the current `ExecutionContext` implementation is substantially aligned with `EXECUTION-CONTEXT-REPRESENTATION.md` and that all seven specified verification requirements pass. The report records 8/8 continuity tests passing and no structural changes required.
- **Execution Context verification scope:** The verification demonstrated Context creation, minimum authoritative information, semantic round-trip preservation, Process Instance association, recovery by a replacement Runtime/Agent context, explicit continuation information through `pending_execution`, and independence from transient Runtime/Agent/session information.
- **Execution Context implementation decision:** No changes were made to `runtime/core/models.py`, `runtime/core/runtime.py`, `runtime/core/store.py`, or the continuity tests as a result of the verification.
- **Minimal Runtime interface definition:** `execution/IMPLEMENTATION-MINIMAL-RUNTIME-INTERFACE.md` records the smallest Runtime capability boundary justified by the first vertical slice, the Runtime/Agent authority boundary, current implementation coverage, and confirmed gaps.
- **Runtime interface verification:** Review of `runtime/core/runtime.py`, `runtime/core/models.py`, `runtime/core/store.py`, `runtime/core/__init__.py`, and `tests/continuity/test_runtime_recovery.py` confirms that Process Instance creation/loading and Context loading/persistence are already implemented and exercised by existing tests. No duplicate implementation was introduced.
- **Runtime interface verification finding:** The next implementation boundary is required process-state/lifecycle behavior. Artifact association and terminal Process Instance handling remain identified gaps; their concrete API and semantics should be derived from the first real vertical slice rather than generalized prematurely.
- **Process lifecycle investigation:** `execution/IMPLEMENTATION-PROCESS-LIFECYCLE-INVESTIGATION.md` records that Process State and transition validity are governed by the applicable EPM, while PEM governs Runtime execution of those transitions. The current `initial`, `implementation`, and `engineering_complete` values are implementation representations, not established universal AESM state identifiers. Engineering completion recognition is justified when explicitly recognized under governing semantics, but the `engineering_complete` state assignment must not be generalized without first-vertical-slice EPM evidence. Process Instance termination remains distinct from engineering completion and Runtime termination; no terminal lifecycle value should be invented before the vertical slice establishes its semantics.
- **Lifecycle investigation commit:** `f862480caf776d0c0eddc1ba3026b38bccb716b6`.
- **First vertical slice task decomposition:** The First Real Vertical Slice work was expanded into a dedicated definition task with nested subtasks covering request selection, objective/scope, applicable EPM binding, state semantics, transition semantics, completion/termination semantics, and derivation of the minimal Runtime lifecycle boundary. The plan also explicitly requires future task decomposition/addition to be recorded directly in this checklist.
- **First vertical slice definition:** `execution/FIRST-VERTICAL-SLICE-DEFINITION.md` binds the first slice to `tuanna2703/directories-builder-pro`, `Add_Review_Form::business_id`, and derives four slice-specific states: Investigation, Implementation, Verification, and Engineering Complete. It records the valid transitions, the prototype human-approval execution condition, the verification feedback path, completion semantics, the non-applicability of invented terminal Process Instance semantics, and the minimum Runtime lifecycle responsibilities.
- **First vertical slice definition commit:** `f90a6250b6b8890640b893e03f6c17005103f4cc`.
- **First Agent execution observation:** The observed Directories Builder Pro execution successfully demonstrated disciplined engineering behavior but did not create or invoke an AESM Process Instance, authoritative Execution Context, or AESM Runtime. The execution therefore serves as the control condition for AESM participation.
- **Agent–Runtime boundary investigation:** `execution/IMPLEMENTATION-AGENT-RUNTIME-BOUNDARY-INVESTIGATION.md` records that the minimum operational boundary is bidirectional: the Agent consumes authoritative Context and submits contributions/results; the Runtime recognizes them, applies permitted mutations, persists authoritative state, and returns the updated executable situation. The investigation found that an invocation path is required but did not justify MCP, CLI, or another transport as normative.
- **Agent–Runtime investigation finding:** A small Agent-facing adapter is preferable to exposing the entire Runtime API. The adapter should remain an implementation mechanism and must not silently become an AESM semantic requirement.
- **Agent–Runtime investigation conclusion:** No normative AESM change is justified by the first execution observation. The first vertical slice must establish lifecycle semantics before the Agent-facing adapter is implemented.
- **Evidence Recording implementation and validation:** Pull request #4 was merged as `9aff039efeac3e3c9c520452dd572e1195d33bab`. The post-merge reconciliation records PASS for semantic boundary, context persistence/rollback, lifecycle compatibility, and behavioral validation, with 35/35 tests passing and an explicitly documented coverage qualification for the persistence-failure regression. It also records that no implementation redesign or semantic change is justified.
- **Evidence Recording repository hygiene:** `.gitignore` was added and committed Python cache files were removed from `main`. The post-merge reconciliation records repository hygiene as corrected. Subsequent repository inspection found no `__pycache__` matches, and the previously present `feature/evidence-recording` branch is no longer returned by branch search.
- **Evidence Recording closure:** The implementation-plan entry for evidence recording is marked complete because the merged implementation, tests, behavioral validation, and post-merge reconciliation satisfy the completion-marking rule. Human closure is the accepted baseline for the next bounded capability inspection.
- **Next Runtime capability inspection:** `execution/RUNTIME-CAPABILITY-INSPECTION-DECISION-ARTIFACT-VERIFICATION.md` inspected the existing decision, artifact, and verification recording methods. It found that all three capabilities already exist, so no new feature is justified. It also identified a concrete consistency risk: unlike `observe()`, the decision/artifact/verification methods mutate the in-memory Context before persistence and do not restore that mutation if `save_context()` fails. The persistence layer restores files, but the live Runtime object can become inconsistent with authoritative persisted state after a failed write.
- **Capability testing limitation:** The connected GitHub interface does not expose an executable local pytest runner for this repository, and the inspected commit has no associated GitHub Actions workflow run. Therefore this round is a bounded implementation/capability inspection, not a claim of fresh test execution. The next executable validation is explicitly tracked under `Bounded Recording Capability Validation`.
- **Recording capability behavioral validation:** `execution/RUNTIME-CAPABILITY-BEHAVIORAL-VALIDATION.md` documents the bounded behavioral testing of decision, artifact, and verification recording. 53 tests were created in `tests/recording/test_runtime_recording.py`; 46 passed, 7 failed. All 7 failures confirm a single implementation defect: `recognize_decision()`, `record_artifact()`, and `record_verification()` mutate the in-memory Context before calling `save_context()` and do not restore the mutation when `save_context()` raises, leaving the live Runtime inconsistent with the authoritative persisted state. The persistence layer's own file-level rollback works correctly; only the caller-level rollback is missing. The recommendation is minimal implementation correction following the existing `observe()` pattern. No AESM semantic change is involved. The parent implementation-plan items for decision recording, artifact recording, and verification recording remain unchecked because the confirmed defect must be corrected before their behavioral evidence is sufficient for completion marking. Baseline commit: `87fcc2bba226fda7b66bab910190e23abd10f67a`.
- **Recording validation reconciliation:** The behavioral validation is accepted as evidence that the three recording capabilities exist and are behaviorally exercised, but not yet as sufficient completion evidence because the seven failure-path scenarios expose a common caller-level rollback defect. The defect is bounded to `recognize_decision()`, `record_artifact()`, and `record_verification()`; `observe()` provides the existing rollback precedent. The correction is explicitly implementation-only and does not authorize changes to AESM semantics, lifecycle behavior, verification-path semantics, or persistence architecture.
- **Caller-level rollback correction authorization:** The next bounded implementation task is to restore the affected in-memory Context state when persistence fails in the three recording callers, using the existing `observe()` rollback pattern. The seven currently failing behavioral scenarios are the regression acceptance tests. No broader recording redesign or generalized transaction abstraction is authorized by this plan update.

Implementation evidence, findings, and approved deviations should be recorded as work proceeds. This plan remains the single checklist for implementation progress; detailed technical evidence may live in dedicated implementation documents or test artifacts referenced from the relevant task.
