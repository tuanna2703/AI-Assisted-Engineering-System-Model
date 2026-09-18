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

Evidence: [`execution/COMPLETION-TERMINATION-VALIDATION.md`](execution/COMPLETION-TERMINATION-VALIDATION.md).

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

Evidence: [`execution/AGENT-GUIDANCE-INTERFACE.md`](execution/AGENT-GUIDANCE-INTERFACE.md).

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

Evidence: [`execution/AGENT-RUNTIME-EXECUTION-BRIDGE-INSPECTION.md`](execution/AGENT-RUNTIME-EXECUTION-BRIDGE-INSPECTION.md).

### Runtime API Inspection

**Status: Complete.**

The concrete adapter surface was determined as:

- `create_process`
- `attach`
- `get_context`
- `dispatch`

Objective-to-Process-Instance discovery remains a separate design concern and is not silently generalized into the bridge.

Evidence: [`execution/RUNTIME-API-INSPECTION.md`](execution/RUNTIME-API-INSPECTION.md).

### Minimal Agent–Runtime Bridge

**Status: Complete.**

The bounded bridge was implemented outside `runtime/` and delegates authority to the existing Runtime. It provides Process Instance access, authoritative Context access, Runtime dispatch, and authoritative result/state return.

Evidence: [`execution/AGENT-RUNTIME-BRIDGE-IMPLEMENTATION.md`](execution/AGENT-RUNTIME-BRIDGE-IMPLEMENTATION.md).

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

Evidence: [`execution/MECHANISM-VALIDATION.md`](execution/MECHANISM-VALIDATION.md).

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
- Controlled boundary: `execution/DBP-EMPIRICAL-EXECUTION-BOUNDARY.md`
- Observer protocol: `execution/DBP-EMPIRICAL-EXECUTION-OBSERVER-PROTOCOL.md`

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

[`execution/DBP-EMPIRICAL-EXECUTION-REPORT.md`](execution/DBP-EMPIRICAL-EXECUTION-REPORT.md)

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

Evidence record: [execution/PROJECT-SCOPE-SEMANTICS-INVESTIGATION.md](execution/PROJECT-SCOPE-SEMANTICS-INVESTIGATION.md)
Semantic decision record: [execution/ENGINEERING-SCOPE-IDENTITY-SEMANTICS.md](execution/ENGINEERING-SCOPE-IDENTITY-SEMANTICS.md)

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
## Fresh-Agent Continuity Validation

**Status: Pending.**

This work is not to be conflated with the mechanism-validation fresh-session recovery that already passed. The later continuity work must determine whether a fresh Agent can continue a real DBP engineering process after meaningful work has already been persisted.

- [ ] Stop the original DBP Agent session after meaningful process state exists.
- [ ] Start a genuinely fresh Agent session.
- [ ] Recover the existing Process Instance and authoritative Context.
- [ ] Determine whether the fresh Agent can continue without relying on the old conversation.
- [ ] Complete or otherwise resolve the DBP process as appropriate.
- [ ] Verify continuity from persisted evidence rather than Agent narrative alone.

**Exit condition:** A real DBP process remains operationally continuous across Agent/session loss.

## Feedback and Reconsideration Validation

**Status: Pending.**

- [ ] Introduce a realistic verification failure or human feedback event.
- [ ] Persist the event as appropriate.
- [ ] Reconsider the affected decision or implementation.
- [ ] Re-implement where necessary.
- [ ] Re-verify.
- [ ] Confirm that prior process knowledge remains traceable.

**Exit condition:** The prototype demonstrates controlled iterative engineering rather than only a linear happy path.

## Runtime Control Experiment

**Status: Pending.**

- [ ] Identify one rule initially expressible as Agent guidance.
- [ ] Test guidance reliability.
- [ ] Identify one condition that may require Runtime control.
- [ ] Validate the smallest Runtime control justified by evidence.
- [ ] Preserve the distinction between guidance and authoritative Runtime enforcement.

**Exit condition:** Evidence identifies which responsibilities can remain guidance and which require executable Runtime control.

## Environment Independence Validation

**Status: Pending.**

- [ ] Exercise a second usable Execution Environment or execution mechanism.
- [ ] Verify persisted Process Instance and Execution Context remain meaningful outside the first environment.
- [ ] Confirm environment-specific mechanisms remain adapters/capabilities rather than AESM semantic definitions.
- [ ] Record genuine portability limitations.

**Exit condition:** AESM remains conceptually and operationally independent of a particular Agent host or IDE.

## Prototype Evaluation and Controlled Refinement

**Status: Pending.**

- [ ] Review implementation failures and unexpected behavior.
- [ ] Classify each finding as implementation defect, environment limitation, documentation ambiguity, or genuine AESM semantic deficiency.
- [ ] Correct implementation defects without changing AESM semantics.
- [ ] Resolve environment limitations through justified mechanisms.
- [ ] Clarify documentation only where implementation exposes genuine ambiguity.
- [ ] Propose semantic changes only for demonstrated deficiencies.
- [ ] Record any approved semantic change as a separate decision before applying it.

**Exit condition:** The prototype provides an evidence-based assessment of whether the current AESM model is implementable as intended.

## Completion Criteria for the Initial Prototype

The initial prototype is complete only when the following are demonstrated by recorded evidence:

- A real engineering request is represented as a persistent Process Instance.
- Authoritative Execution Context survives Agent/session loss.
- The Agent receives sufficient AESM guidance to participate.
- The Agent performs real engineering work using an existing Execution Environment.
- Runtime-controlled state and constraints remain authoritative where required.
- Evidence, decisions, artifacts, and verification are persisted.
- Feedback/reconsideration can be handled without losing process knowledge.
- The process can continue after the original Agent/session ends.
- Engineering completion is distinguishable from Runtime/session termination.
- The implementation remains independent of a specific IDE or transport.

The prototype is judged by demonstrated behavior and recorded evidence, not by the number of Runtime APIs or documentation pages created.

## Controlled Forward Work Sequence

The authorized sequence is now:

- [x] **Plan Reconciliation and Mechanism Gate Closure** — reconcile this plan with the completed Agent-boundary mechanism validation and establish the DBP gate.
- [x] **DBP Experiment Boundary Definition** — establish the controlled DBP request, evidence contract, authority model, and experiment constraints.
- [x] **DBP Empirical Execution** — execute the controlled DBP request and record the observed engineering and AESM participation results.
- [x] **DBP Evidence Reconciliation** — independently reconcile DBP implementation evidence, AESM participation evidence, and project/process binding findings.
- [x] **Project/Scope Semantics Investigation** — inspect the existing AESM model and determine whether the current semantic concepts are sufficient to identify engineering scope.
- [x] **Project/Scope Semantic Clarification** — define Engineering Scope Identity; establish scope invariants; determine that a first-class Project entity is not yet semantically required.
- [x] **Project / Scope Resolution Design** — deterministic scope resolution, ambiguity handling, Process Instance selection/creation, and authority boundaries established. Gate complete.
- [x] **Process Binding Design** — normative scope-to-Process-Instance relationship and discovery model established. Gate complete.
- [x] **Persistence Scope Design** — authoritative scope/process persistence requirements established. Gate complete.
- [x] **Agent / Environment Mechanism Design** — scope evidence, Agent/Runtime authority boundaries, and minimum mechanism combination established. Gate complete. Evidence: `execution/AGENT-ENVIRONMENT-MECHANISM-DESIGN.md`.
- [x] **Normative Documentation Reconciliation** — canonical Process Instance, Agent, operational, and Agent-integration documentation reconciled with the completed scope/binding/persistence/mechanism decisions. Evidence: `execution/NORMATIVE-DOCUMENTATION-RECONCILIATION.md`. No implementation mechanism or new authority layer introduced.
- [ ] **Project Identity and Process Binding Implementation** — implement the approved mechanism after all semantic gates pass.
- [ ] **Multi-Project Empirical Validation** — validate continuity, isolation, ambiguity handling, and cross-session discovery through real Agent execution.
- [ ] **Fresh-Agent DBP Continuation** — validate continuation of a real DBP process after project binding is available.
- [ ] **Feedback and Reconsideration Validation** — validate controlled iteration where justified.
- [ ] **Environment Independence Validation** — test portability beyond the first Agent environment.
- [ ] **Prototype Evaluation and Controlled Refinement** — reconcile findings and authorize only evidence-based changes.

### Current Progress Position

The repository has completed the foundational Runtime, persistence, Context, recording, lifecycle, Agent guidance, Agent–Runtime bridge, environment mechanism mapping, Agent-boundary mechanism validation, and DBP empirical investigation.

The Project/Scope Semantics Investigation established that the current AESM model identifies engineering execution by objective and Process Instance identity, but does not yet define a stable identity for the engineering scope in which that objective is performed.

**Current gate:** Project/Scope Semantic Clarification.

**Next action:** Define Engineering Scope Identity before deciding whether AESM requires a named Project entity, repository identity, workspace identity, or another scope representation.

No Runtime, schema, persistence, Agent guidance, or environment mechanism implementation should proceed until the scope semantics are resolved.
