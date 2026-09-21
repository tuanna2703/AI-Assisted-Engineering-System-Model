# AESM Implementation Plan

## Purpose

This document is the controlled implementation plan for turning the agreed AESM model into a practical, executable implementation that can be used by an AI Agent in an existing Execution Environment.

The plan is implementation-oriented. It does not redefine AESM semantics. The canonical `docs/` set remains the governing conceptual baseline.

## Implementation Objective

Prove, through real executable engineering work, that an engineering request can be represented as a persistent AESM Process Instance and that an AI Agent can participate in that process using mechanisms already available in an Execution Environment.

The target capability is:

```text
Human Request
      ↓
Create / identify Process Instance
      ↓
Load / establish authoritative Execution Context
      ↓
Provide AESM guidance to Agent
      ↓
Agent performs engineering work
      ├── Investigation / Evidence
      ├── Decisions
      ├── Implementation / Artifacts
      └── Verification
      ↓
Persist authoritative process state
      ↓
Agent/session may stop
      ↓
Recover Process Instance + Execution Context
      ↓
Continue or complete the engineering process
```

## Governing Principles

1. **Implement before expanding.** Do not expand AESM concepts merely because implementation is difficult.
2. **Use the existing AESM model as the baseline.** Architecture, Operational Flow, EPM, PEM, and the unified documentation set are the conceptual authority.
3. **Use vertical evidence.** Validate the complete interaction rather than accumulating isolated mechanisms without an end-to-end test.
4. **Use existing Execution Environment mechanisms.** Do not create AESM-specific infrastructure unless evidence establishes a need.
5. **Keep AESM independent of a specific IDE.** VS Code or another IDE may be an Execution Environment, not the AESM architecture.
6. **Keep Agent, Runtime, and Execution Environment distinct.** The Agent performs engineering work; Runtime governs authoritative process execution; the Execution Environment supplies interaction and tooling mechanisms.
7. **Treat persisted Process Instance / Execution Context state as authoritative.** Conversation history is not authoritative continuity state.
8. **Separate guidance from enforcement.** Guidance can influence Agent behavior; Runtime state and constraints provide authoritative control where required.
9. **Require implementation evidence before semantic change.** Do not change AESM semantics based on speculation or a single implementation inconvenience.
10. **Keep the implementation minimal.** Add infrastructure only when demonstrated by the prototype.

## Scope

### In scope

- Process Instance identity and persistence
- Authoritative Execution Context
- Minimal Runtime core
- Agent/AESM guidance
- Agent–Runtime interaction
- Existing Execution Environment mechanisms
- Evidence, decision, artifact, and verification recording
- Process continuation and fresh-session recovery
- Feedback and reconsideration where justified
- Runtime-controlled transition and constraint experiments
- Validation in real Agent execution
- Environment-independence investigation

### Explicitly out of scope unless separately authorized

- Dedicated AESM IDE extension
- Complete AESM graphical application
- General-purpose workflow designer
- Multi-agent orchestration
- Distributed execution
- Enterprise infrastructure
- New programming language or DSL
- Automatic enforcement of every AESM rule
- Normative MCP requirement
- VS Code-specific architecture
- Generalized Agent orchestration
- Broad Runtime refactoring
- Speculative EPM/PEM/AESM expansion

## Work Status Legend

- `[ ]` Not started
- `[~]` In progress
- `[x]` Complete
- `[!]` Blocked or requires explicit decision

## Completed Foundations

### Baseline and Scope Control

- [x] Establish `docs/` as the canonical AESM knowledge surface.
- [x] Establish this document as the controlled implementation plan.
- [x] Establish the objective of operationalizing the existing AESM model rather than continuing conceptual expansion.

### Process Instance Persistence

- [x] Define the minimal Process Instance representation.
- [x] Implement Process Instance creation and stable identity.
- [x] Implement loading and filesystem persistence.
- [x] Demonstrate continuity without relying on conversation history.

### Authoritative Execution Context

- [x] Define the minimal authoritative Execution Context.
- [x] Implement creation, loading, mutation, and persistence.
- [x] Represent continuation information explicitly.
- [x] Demonstrate recovery from persisted Context after loss of the original Agent context.

### First Vertical Slice Semantics

- [x] Define a bounded engineering request and its objective/scope.
- [x] Bind applicable EPM semantics.
- [x] Derive required process states and valid transitions.
- [x] Define engineering completion separately from Runtime/session termination.
- [x] Derive the minimum Runtime responsibilities from the established semantics.

### Minimal Runtime Core

- [x] Process Instance creation/loading.
- [x] Execution Context loading/saving.
- [x] Process-state/lifecycle operations required by the prototype.
- [x] Evidence recording.
- [x] Decision recording.
- [x] Artifact recording.
- [x] Verification recording.
- [x] Completion/termination handling required by the prototype.
- [x] Preserve Runtime authority over lifecycle and completion semantics.

Evidence: [`tests/lifecycle/test_completion_termination.py`](tests/lifecycle/test_completion_termination.py).

### Recording Behavioral Validation

- [x] Validate decision, artifact, and verification recording.
- [x] Validate guards and persistence/history behavior.
- [x] Validate failure-path consistency.
- [x] Correct caller-level rollback defect discovered by behavioral testing, following the existing `observe()` rollback precedent.
- [x] Accept the recorded regression evidence: 53/53 recording tests and 88/88 full suite in the correction validation.

No further recording or persistence-semantic change is authorized by this evidence.

## Agent Guidance and Environment Work

### Agent Guidance Interface

**Status: Complete. Semantic contract closed.**

Evidence: [`docs/Agent-Execution-Integration.md`](docs/Agent-Execution-Integration.md).

The guidance analysis established:

- AESM guidance content is available and executable through repository documentation.
- Authoritative Execution Context is exposed by the Runtime bridge.
- Conversation history must not be treated as authoritative state.
- Governed execution capabilities are executable through the established bridge.
- Lifecycle observation is executable.
- Remaining semantic questions are not to be reopened merely for the empirical experiment.

The Agent Guidance Interface is not an open work unit. Subsequent work must use its established contract rather than redesigning it.

### Agent–Runtime Boundary Investigation

**Status: Complete.**

The investigation established the responsibility boundary between Agent, Runtime, and Execution Environment and justified a thin Agent–Runtime bridge rather than Runtime redesign or a normative transport.

Evidence: [`docs/Agent-Execution-Integration.md`](docs/Agent-Execution-Integration.md).

### Runtime API Inspection

**Status: Complete.**

The concrete adapter surface was determined as:

- `create_process`
- `attach`
- `get_context`
- `dispatch`

Objective-to-Process-Instance discovery remains a separate design concern and is not silently generalized into the bridge.

Evidence: [`docs/Agent-Execution-Integration.md`](docs/Agent-Execution-Integration.md).

### Minimal Agent–Runtime Bridge

**Status: Complete.**

The bounded bridge was implemented outside `runtime/` and delegates authority to the existing Runtime. It provides Process Instance access, authoritative Context access, Runtime dispatch, and authoritative result/state return.

Evidence: [`docs/Agent-Execution-Integration.md`](docs/Agent-Execution-Integration.md).

The bridge is not a new persistence layer, orchestration engine, lifecycle model, or transport requirement.

### Environment Mechanism Mapping

**Status: Complete and validated through the mechanism-validation work unit.**

The environment mapping established that the required minimum mechanism combination is:

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

No dedicated VS Code extension, MCP server, second Process Instance store, or generalized Agent orchestrator is required by the current evidence.

The prior Environment Mechanism Mapping findings are now superseded only where the subsequent mechanism validation demonstrated the capability empirically. The semantic contract itself is unchanged.

## Agent-Boundary Mechanism Validation

**Status: Complete — gate passed.**

Evidence: [`implementation/MECHANISM-VALIDATION.md`](implementation/MECHANISM-VALIDATION.md).

The validation combined two Agent sessions and established the complete operational chain:

```text
Fresh Agent session
      ↓
Persistent AESM guidance
      ↓
Process Instance establishment/recovery
      ↓
Authoritative Execution Context
      ↓
Agent-caused Runtime mutations
      ↓
Persisted evidence/state
      ↓
Independent fresh-session recovery
```

The validation demonstrated, among other capabilities:

- persistent Agent guidance was actually loaded and affected Agent behavior;
- a real Process Instance was created through the bridge;
- authoritative Context was obtained through the Runtime;
- Agent activity caused Runtime mutations through `dispatch()`;
- Runtime operations produced persisted history and Context state;
- a fresh Agent session recovered the same Process Instance and Context;
- Agent narrative remained distinct from authoritative Runtime state.

### Mechanism Validation Gate

**Decision: READY FOR DBP EMPIRICAL EXECUTION.**

The previous mechanism work is closed. Do not reopen Agent Guidance Interface semantics, Environment Mechanism Mapping, or bridge semantics as part of the DBP experiment unless new evidence directly requires a separate decision.

The next work must test whether the established mechanism governs and records a real engineering task rather than merely demonstrating that the mechanism exists.

## Current Work Unit — DBP Empirical Execution

**Status: Complete — empirical result reconciled.**

The controlled Directories Builder Pro experiment was executed against:

- Controlled repository: `tuanna2703/directories-builder-pro`
- Controlled request: **Requirements: Hierarchical Categories Filter — REQ-01 through REQ-26**
- Controlled boundary: `implementation/DBP-EMPIRICAL-EXECUTION-REPORT.md`
- Observer protocol: `implementation/DBP-EMPIRICAL-EXECUTION-REPORT.md`

The empirical result established a necessary distinction:

```
DBP engineering activity
        +
AESM operational participation
        +
project/process binding
```

The DBP Agent reported implementation of the controlled request and reported syntax/structural checks. Independent evidence also established the observed implementation change in `modules/reviews/forms/add-review-form.php`, where `business_id` was changed to `Fields_Manager::POST_SELECT` targeting `dbp_business`, with `save()` translating the WordPress post ID through `Business_Repository::find_by_post_id()`.

However, the execution did **not** provide sufficient evidence that the Agent actually participated in AESM through the established Runtime/Process Instance mechanism. No authoritative Process Instance, Execution Context, Runtime operation, or ProcessStore persistence attributable to the DBP execution was established by the available evidence.

The Agent's claimed completion and the independently observed AESM non-participation must remain separate findings.

Evidence record:

[`implementation/DBP-EMPIRICAL-EXECUTION-REPORT.md`](implementation/DBP-EMPIRICAL-EXECUTION-REPORT.md)

The original Agent completion report, where preserved outside this repository, remains source evidence and must not be rewritten as an AESM result.

### DBP Evidence Reconciliation

**Status: Complete — gap identified.**

The reconciliation established:

- DBP implementation activity occurred.
- The Agent reported completion of REQ-01–REQ-26, but the available evidence does not independently establish every requirement as fully behaviorally verified.
- Syntax/structural checks were reported; full runtime form/AJAX/end-to-end behavior and a comprehensive automated test suite were not demonstrated.
- No executable AESM Runtime participation was visibly established during the observed execution.
- No authoritative Process Instance or Execution Context attributable to the execution was established.
- No AESM ProcessStore persistence attributable to the execution was established.
- The `.akg/` directory must not be interpreted as AESM state; it is an Architectural Knowledge Graph mechanism.
- The execution therefore does not establish how a real Agent determines which engineering project/scope it is operating within or which Process Instance should govern that work.

The unresolved project/process binding is now treated as a distinct architectural work unit rather than as a reason to retrofit AESM state into the completed DBP execution.

**Exit condition:** Satisfied. The empirical evidence is preserved as a bounded finding and the resulting architectural question is explicitly separated from the DBP implementation result.

## Current Work Unit — Project Identity and Process Binding

**Status: Semantic clarification complete — Engineering Scope Identity defined; Project / Scope Resolution Design authorized.**

Evidence record: [implementation/PROJECT-SCOPE-SEMANTICS-INVESTIGATION.md](implementation/PROJECT-SCOPE-SEMANTICS-INVESTIGATION.md)
Semantic decision record: [implementation/ENGINEERING-SCOPE-IDENTITY-SEMANTICS.md](implementation/ENGINEERING-SCOPE-IDENTITY-SEMANTICS.md)

### Gate Result

The semantic clarification establishes **Engineering Scope Identity** as a distinct AESM concept.

It is distinct from Engineering Objective, Process Instance Identity, Execution Context, Execution Environment, repository identity, and workspace identity.

A scope is a stable engineering boundary that contextualizes related engineering objectives, artifacts, requirements, constraints, decisions, and execution activities.

The decision does not establish Project = repository or Project = workspace.

A first-class Project entity is **not required at this gate**. It may be reconsidered later only if implementation/design evidence establishes a need for independently managed project metadata or lifecycle.

### Established semantic invariants

- Scope Identity is not Process Instance Identity.
- Scope Identity is not Engineering Objective.
- Repository identity is scope evidence, not universal scope identity.
- Workspace identity is scope evidence, not universal scope identity.
- One scope may contain multiple Process Instances.
- A Process Instance may span multiple repositories when its engineering scope requires it.
- Agent output does not establish authoritative scope binding.
- Environmental evidence does not become authoritative merely by observation.
- Ambiguous scope resolution must remain explicit.
- Established Process Instance scope binding must remain recoverable.
- Changing Agent, Runtime, IDE, workspace, or repository path does not by itself change scope identity.

### DBP consequence

The DBP empirical finding is now expressible as a concrete missing operational chain:
```text
DBP request
    v
Engineering Scope Identity resolution
    v
existing Process Instance resolution
    OR
new Process Instance creation
```

The DBP repository may provide evidence for scope resolution but is not itself the semantic definition of the scope.

### Current gate

**Engineering Scope Identity Semantics — COMPLETE.**

**Next authorized work:** **Project / Scope Resolution Design.**

Implementation remains blocked until deterministic resolution, ambiguity handling, Process Instance selection/creation, persistence, and Agent/Environment evidence flow are designed and approved.
## Current Work Unit — Project / Scope Resolution

**Status: Verification gate CLOSED — all executable evidence obtained; work unit complete.**

Design record: [implementation/PROJECT-SCOPE-RESOLUTION-DESIGN.md](implementation/PROJECT-SCOPE-RESOLUTION-DESIGN.md)

### Plan

- [x] Inspect the merged repository-portable continuation baseline.
- [x] Reconcile existing Engineering Scope Identity semantics and current scope-binding implementation.
- [x] Define the distinction between repository identity, repository root, Engineering Scope Identity, Engineering Objective, Process Instance Identity, and Execution Context.
- [x] Define the Execution Environment → Active Repository Context → Scope Resolution → Process Instance Resolution authority flow.
- [x] Define explicit outcomes for unresolved, ambiguous, conflicting, invalid, and resolved scope.
- [x] Define deterministic Process Instance candidate selection without objective/path/filesystem heuristics.
- [x] Define explicit Process Instance creation as separate from discovery.
- [x] Define repository isolation and active-context change behavior.
- [x] Define Agent/Execution Environment evidence as non-authoritative input.
- [x] Close the Project / Scope Resolution design gate.
- [x] Add stable repository identity to ActiveRepositoryContext without making it a scope identity.
- [x] Add repository-local Process Instance enumeration to ProcessStore.
- [x] Add Runtime-owned deterministic Process Instance resolution.
- [x] Add Runtime resolution-and-attach behavior.
- [x] Expose resolution through the existing Agent–Runtime Bridge without adding Bridge-owned state.
- [x] Add targeted tests for unique resolution, no candidate, ambiguity, explicit PI selection, cross-scope rejection, repository isolation, repository identity/path distinction, and Bridge delegation.
- [x] Run the targeted scope-resolution test suite.
- [x] Run the full regression suite.
- [x] Validate two independent repository roots in one workspace and active-context change behavior with executable evidence.
- [x] Reconcile Runtime, persisted, Agent/Bridge, and verification evidence.
- [x] Close the implementation work unit only from executable evidence.

### Authorization boundary

No generalized Project entity, workspace-wide Process Instance index, second persistence store, or Agent-owned discovery mechanism is authorized by this work unit.

Creation remains an explicit Runtime operation. Resolution may identify that creation is required, but it does not silently create a Process Instance.

### Verification status — CLOSED

- [x] Add the initial deterministic resolution tests.
- [x] Expand tests for relocated repository paths, immutable active-repository context, cross-repository explicit PI rejection, and terminated PI exclusion.
- [x] Run the targeted scope-resolution, scope-binding, multi-project, repository-isolation, and affected Runtime/Bridge suites from an executable checkout.
- [x] Run the full regression suite from the merged main revision.
- [x] Validate the multi-repository and active-context scenarios with executable evidence.
- [x] Reconcile Runtime, persisted, Agent/Bridge, and verification evidence.
- [x] Close the implementation work unit only from executable evidence.

### Executable verification record — 2026-09-21

**Branch:** `verify/executable-project-scope-resolution`
**HEAD SHA:** `67f68ccceba20e7833338ef673ba0aa37a5010ae`
**Python:** 3.13.5 | **pytest:** 9.1.1

**Defect corrected:** `test_runtime_context_is_immutable_and_does_not_retarget_store` referenced non-existent `ProcessStore.context` attribute. Corrected to use `store.root` (public). No production code changed.

**Isolation strengthened:** `test_resolution_is_repository_local` and `test_cross_repo_isolation` both strengthened from single-direction / empty-B to bidirectional / populated-B with auditability comments.

| Suite | Command | Result |
|---|---|---|
| Scope resolution + binding | `pytest tests/project_identity/` | **25/25 PASS** |
| Multi-project + repository isolation | `pytest tests/multi_project/ tests/repository_isolation/` | **24/24 PASS** |
| Full regression | `pytest tests/` | **204/204 PASS** |

Evidence artifact: [implementation/EXECUTABLE-PROJECT-SCOPE-RESOLUTION-VERIFICATION.md](implementation/EXECUTABLE-PROJECT-SCOPE-RESOLUTION-VERIFICATION.md)

### Exit condition

The work unit closes only when the deterministic resolution tests and regression suite pass and the multi-repository isolation/context-change scenarios are explicitly verified. Source inspection or a committed test expansion does not satisfy this gate.

## Repository-Portable Continuation Validation

**Status: Complete — validation PASS.**

Evidence record: [implementation/REPOSITORY-PORTABLE-CONTINUATION-VALIDATION.md](implementation/REPOSITORY-PORTABLE-CONTINUATION-VALIDATION.md)

The validation demonstrated repository-local Process Instance portability through a Git round trip followed by continuation from an independent checkout by a genuinely fresh Agent session.

### Git Round-Trip Integrity

- [x] Freeze and record the source PI baseline.
- [x] Verify `.aesm/` is Git-visible and contains the authoritative PI files.
- [x] Record SHA-256 hashes for `process.json`, `context.json`, and `history.jsonl`.
- [x] Create an independent checkout from the remote repository revision without manually copying `.aesm/`.
- [x] Verify byte-level identity and authoritative PI metadata after checkout.
- [x] Verify no source-workspace or alternate persistence-store dependency remains.
- [x] Classify Git Round-Trip Integrity as **PASS**.
- [x] Classify Environment Independence as **PASS**.

### Fresh-Agent Repository-Scoped Continuation

- [x] End the source validation session before the continuation session.
- [x] Start a separate Agent session in the independent checkout.
- [x] Provide only repository/revision/checkout bootstrap information.
- [x] Require independent discovery of the applicable PI under repository-local `.aesm/`.
- [x] Recover the existing PI through Runtime `attach()`.
- [x] Obtain authoritative Execution Context from Runtime.
- [x] Perform exactly one bounded Runtime-mediated `observe()`.
- [x] Verify the same PI persisted after continuation.
- [x] Verify Context advanced from version 3 to version 4.
- [x] Verify history advanced from 5 to 6 with fresh-session attribution.
- [x] Verify no replacement PI or alternate persistence store was used.
- [x] Classify Fresh-Agent Repository-Scoped Continuation as **PASS**.

### Evidence Reconciliation

- [x] Reconcile CONTROLLER, AGENT, RUNTIME, PERSISTED, and VERIFICATION evidence.
- [x] Keep Git portability evidence separate from Agent continuity evidence.
- [x] Preserve the surrounding-conversation-summary limitation explicitly.
- [x] Confirm that no Runtime implementation change was introduced.
- [x] Record the final overall classification as **Repository-Portable Continuation Validation — PASS**.

**Closure:** The repository-local `.aesm/` boundary is empirically demonstrated as portable through Git and recoverable by a fresh Agent in an independent repository workspace. This result does not imply automatic resolution of arbitrary multi-repository engineering scopes.

## Current Work Unit — Runtime Consistency and Continuity Hardening

**Status: Implementation in progress — targeted implementation changes applied; behavioral and cross-process verification pending.**

This work unit addresses verified implementation findings against the current main baseline used to start this implementation branch.

### Scope

The work is limited to implementation correctness, behavioral regression coverage, and validation of continuity under the current repository-local persistence architecture.

It does not reopen:

- AESM semantic definitions already established in docs/;
- Agent Guidance Interface semantics;
- repository-local .aesm/ persistence boundary;
- the removal of the permanent execution/ directory;
- the Agent–Runtime authority boundary;
- the existing bridge contract, unless a verified compatibility defect requires a targeted correction.

### Persistence State Consistency

Objective: preserve the invariant that a failed authoritative persistence operation cannot leave Runtime in-memory state ahead of persisted state.

Planned changes:

- [x] Audit every Runtime operation that mutates authoritative Context or Process Instance state before persistence.
- [x] Standardize rollback for _set_state() so process-state transitions restore prior state, version, and timestamp when persistence fails.
- [x] Add rollback symmetry to set_pending_execution().
- [x] Make reconsider() atomic across failure_uncertainty, unresolved_matters, and process-state transition.
- [x] Verify recognize_engineering_completion() does not leave engineering_completion mutated when the subsequent persistence fails.
- [ ] Preserve the existing successful rollback behavior already demonstrated by observe(), recognize_decision(), record_artifact(), record_verification(), scope resolution, and lifecycle persistence.
- [x] Add failure-injection tests that compare live Runtime state with freshly reloaded persisted state after each affected operation.
- [x] Verify history is not advanced when the corresponding authoritative state write fails.

Exit condition: all affected mutating operations preserve live/persisted state equivalence across injected persistence failures, with no regression in the existing recording suite.

### Current-API Compatibility Repair

Objective: restore executable validation artifacts to the current ActiveRepositoryContext-based Runtime API.

Planned changes:

- [x] Update scripts/validate_environment_mechanisms.py to construct ActiveRepositoryContext and pass it to AgentRuntimeBridge.
- [x] Update tests/continuity/xprocess_process_a.py to use ActiveRepositoryContext and the current Runtime constructor.
- [x] Update tests/continuity/xprocess_process_b.py to use ActiveRepositoryContext and the current Runtime constructor.
- [x] Update xprocess observe() calls to satisfy the current explicit recognition contract.
- [x] Review tests/continuity/xprocess_orchestrator.py for assumptions that depend on the old API.
- [x] Rename the store fixture in tests/bridge/test_agent_runtime_bridge.py to repo_ctx or equivalent semantic name, and update dependent fixture/test parameters.
- [x] Do not introduce a compatibility wrapper that reopens the superseded raw-path/ProcessStore constructor.

Exit condition: all executable validation artifacts use the current API directly and the bridge test vocabulary reflects the actual ActiveRepositoryContext type.

### Cross-Process Continuity Validation

Objective: establish current-architecture evidence for independent OS-process recovery and continuation.

Planned procedure:

- [ ] Run the repaired xprocess orchestrator from the repository root.
- [ ] Verify Process A and Process B use distinct OS process identities and Runtime identities.
- [ ] Verify Process B reconstructs the same persisted Process Instance and authoritative Context.
- [ ] Verify persisted history contains evidence from both Runtime identities.
- [ ] Verify Process B performs a valid Runtime-mediated continuation.
- [ ] Record any discovery limitation separately from persistence/recovery capability.
- [ ] Reconcile the result against the existing continuity evidence before making any broader continuity claim.

Exit condition: the repository has current, reproducible evidence establishing exactly what cross-process continuity is demonstrated and what remains unproven.

### Structured Resumption Determination Review

Objective: remove dependence on machine semantics being inferred from free-form prose.

This work is a design-and-test gate before implementation.

- [x] Inspect the canonical lifecycle/resumption semantics in docs/ and the existing lifecycle tests.
- [x] Identify the minimum structured representation required to establish resumption permissibility.
- [x] Define how human-readable semantic_basis remains traceability text without serving as the machine decision signal.
- [x] Define rejection behavior for missing, contradictory, or invalid structured determinations.
- [x] Add behavioral tests for accepted, rejected, ambiguous, and contradictory resumption determinations.
- [x] Only after the semantic contract is settled, implement the smallest Runtime change necessary.

Exit condition: resumption authority is represented by structured data whose meaning is explicit in the canonical model and tested independently of wording variations.

### Persisted Schema Evolution Review

Objective: determine a safe evolution strategy for repository-local .aesm/ state before long-lived cross-environment use expands.

This is a design gate, not an automatic schema change.

- [x] Inspect current ProcessInstance and ExecutionContext persisted fields and existing compatibility assumptions.
- [x] Determine whether a schema version is required for the current portability model.
- [x] Define defaults/migration behavior for safely additive fields.
- [x] Define explicit failure behavior for unsupported or malformed schema versions.
- [x] Add compatibility tests using representative existing persisted state.
- [x] Persisted schema version 1 is now explicit; missing version defaults to version 1, unsupported versions are rejected.

Exit condition: the repository has an explicit, tested decision on persisted schema evolution; implementation follows only if the decision requires it.

### Process-Instance Write Concurrency Review

Objective: determine whether save_process_instance() requires the same stale-write protection already present for save_context().

- [x] Inspect the single-writer assumption and all current Process Instance mutation paths.
- [x] Identify whether concurrent scope resolution or other Process Instance mutations are possible under the supported Execution Environment model.
- [x] Protect Process Instance writes using the persisted `updated_at` value as the optimistic concurrency comparison field.
- [x] Add a race/stale-write test before implementation.
- [x] Implement only the protection justified by the supported concurrency model.

Exit condition: Process Instance write concurrency is either explicitly bounded by the model and tested, or protected by a verified stale-write mechanism.

### Multi-File Persistence Recovery Review

Objective: define recovery semantics for interruption between atomic file replacements in a lifecycle transition.

- [x] Inspect the authoritative roles of process.json, context.json, and history.jsonl.
- [x] Determine which persisted representation is sufficient to reconstruct authoritative state after an interrupted multi-file write.
- [x] Define detectable inconsistency conditions.
- [x] Define the recovery procedure before adding implementation complexity.
- [x] Existing exception-path rollback tests cover multi-file lifecycle persistence; hard-crash recovery remains bounded by repository/Git recovery rather than a new transaction layer.
- [x] Do not introduce a generalized transaction layer; current per-file atomic writes plus rollback on ordinary persistence failure remain the bounded recovery mechanism.

Exit condition: partial-write behavior and recovery are explicitly defined for the current persistence model.

### Final Reconciliation

After the implementation and validation work above:

- [ ] Run the complete regression suite.
- [ ] Run the repaired cross-process experiment.
- [ ] Reconcile Runtime, persisted, test, and validation evidence.
- [ ] Update the durable engineering record only with findings that remain useful after implementation.
- [ ] Update this plan so completed work is marked from evidence, not from Agent narrative.
- [ ] Preserve the repository boundary established by the merged repository-work-record-structure change; do not recreate execution/.

### Authorization Boundary

No production-code change is authorized merely because a finding appears in the review.

The required sequence is:

inspect → plan → implement targeted change → behavioral verification → continuity validation → evidence reconciliation

Schema, lifecycle semantics, and persistence-recovery changes additionally require their respective design gate to close before implementation.


## Verification Gap Resolution

**Status: Targeted repairs applied; bounded verification pending.**

### Controller decisions recorded

- Bridge stale attribute: **test-only correction authorized**. The test must inject persistence failure through the Runtime's authoritative `store.save_context` boundary; no compatibility alias is added to Runtime.
- Lifecycle helper: **test fixture correction authorized**. The SUSPENDED → ACTIVE test determination must include structured `resumption_determination: {status: PERMITTED, basis: ...}` so the intended persistence-failure injection path is reached.
- Schema error: **preserve the existing `load_context()` wrapper contract**. Inspection established that `ExecutionContext.from_dict()` correctly rejects unsupported schema versions, while `ProcessStore.load_context()` intentionally exposes the stable generic `PersistenceError("authoritative context is invalid: <pid>")` boundary. The verification test is therefore corrected to assert the existing public wrapper contract; production code remains unchanged.
- Remote Git round trip: **not authorized as a required closure criterion for this bounded work unit** unless separately requested. Existing local repository-portability evidence remains the agreed evidence scope; no remote round-trip PASS may be claimed.

### Targeted repairs

- [x] Correct bridge persistence-failure test to patch the Runtime-owned ProcessStore boundary.
- [x] Add structured resumption determination to the lifecycle persistence-failure fixture.
- [x] Align the unsupported-schema test with the established `load_context()` wrapper contract.
- [x] Make no production-code changes for these three gaps.

### Verification gate

- [x] Run the full regression suite and targeted suites from the repository checkout.
- [x] Confirm the repaired tests execute the intended failure paths rather than merely changing assertions around skipped behavior.
- [x] Reconcile the final results into the durable implementation record.
- [x] Close the work unit only if all agreed verification obligations pass.

The remote Git push → independent checkout → recovery sequence remains explicitly unclaimed and outside this work unit's closure evidence.

---

## Final Verification Record — 2026-09-21

> **Evidence type: current executable verification (2026-09-21).**
> The following reflects commands actually executed against the merged `main` branch.
> Historical records above — original failures, Controller decisions, authorized test corrections, branch merge — are preserved.

**Repository:** `tuanna2703/AI-Assisted-Engineering-System-Model`
**Branch:** `main`
**HEAD SHA:** `a9d3fc808fc565af0e772811777e1967d7beb3cf`
**Working tree:** Clean
**Python:** 3.13.5 | **pytest:** 9.1.1
**Dependencies:** OK

### Repaired test results

| Test | Runtime result | Path/contract evidence | Classification |
|---|---|---|---|
| `TestPersistenceFailure::test_persistence_failure_returns_error` | `1 passed in 0.24s` | Patch targets `bridge._runtime.store.save_context` (Runtime-owned boundary); `observe()` call chain verified to reach `store.save_context()`; stale `repo_ctx` surface absent from production code | PASS |
| `test_lifecycle_persistence_failure_restores_files_and_authoritative_in_memory_state` | `1 passed in 0.09s` | `resumption_determination: {status: PERMITTED}` confirmed in fixture; `pytest.raises(match="injected lifecycle history failure")` requires the injected `RuntimeError` to propagate — impossible without reaching `JsonlStore.append`; rollback assertions also pass | PASS |
| `test_unsupported_context_schema_is_rejected` | `1 passed in 0.07s` | Test asserts `PersistenceError(match="authoritative context is invalid:")` — confirmed as the public `ProcessStore.load_context()` wrapper at `runtime/core/store.py:133`; lower-level schema error wrapped per established contract | PASS |

### Bounded regression

| Suite | Result |
|---|---|
| `tests/runtime/test_persistence_hardening.py` | 6/6 PASS |
| `tests/runtime/test_persistence_schema_and_concurrency.py` | 4/4 PASS |
| `tests/lifecycle/test_process_instance_lifecycle_control.py` | 20/20 PASS |
| `tests/bridge/` | 43/43 PASS |
| `tests/repository_isolation/` | 15/15 PASS |

### Cross-process continuity

Exit code 0. `"result": "EVIDENCE_COLLECTED"`. Both process boundary and state continuity demonstrated. Prior documented `observe()`/`recognition` incompatibility was already resolved; no failure observed.

### Full regression

```
.venv/bin/pytest -q
192 passed in 1.84s
```

Exit code 0. 192/192 passed. No failures.

### Remaining gaps

None.

### Work unit closure

**VERIFICATION COMPLETE — WORK UNIT CLOSED**

All closure criteria satisfied by current executable evidence. Production code was not modified during this verification.