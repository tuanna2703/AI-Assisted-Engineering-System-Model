# DBP Empirical Execution — Pre-Execution Baseline Record

**Status:** Prepared — final local execution-environment confirmation required.

This record captures the repository-side baseline established before the fresh-Agent DBP experiment. It does not itself authorize DBP implementation.

## Experiment Inputs

- Controlled DBP repository: `tuanna2703/directories-builder-pro`
- Controlled request: **Requirements: Hierarchical Categories Filter — REQ-01 through REQ-26**
- Experiment boundary: `execution/DBP-EMPIRICAL-EXECUTION-BOUNDARY.md`
- Observer protocol: `execution/DBP-EMPIRICAL-EXECUTION-OBSERVER-PROTOCOL.md`
- Controlled implementation plan: `IMPLEMENTATION_PLAN.md`
- Required Agent input: approved fresh-Agent engineering prompt
- Observer protocol must remain inaccessible to the Agent.

## Repository Baselines

### AESM

- Repository: `tuanna2703/AI-Assisted-Engineering-System-Model`
- Branch: `main`
- Preparation tip before this baseline record: `c57b5ac83762e83a0edd96e3282bb9aac6306cfe`
- The preparation tip contains the finalized Observer Protocol and reconciled implementation plan.
- The final repository commit created by this baseline record is the repository-side AESM baseline for the experiment.

### DBP

- Repository: `tuanna2703/directories-builder-pro`
- Branch: `main`
- Baseline commit: `deaabeb175593ec2c607b816eb80b7d16f4f01c5`
- This baseline contains the previously completed `business_id` change.
- No Hierarchical Categories Filter experiment changes are included in this baseline.

## Working-Tree Condition

GitHub branch state establishes the committed repository baseline but cannot establish whether the local clone used to launch the Agent contains uncommitted changes.

Therefore the following must be confirmed in the actual Execution Environment immediately before launch:

- [ ] DBP local working tree is clean.
- [ ] DBP local `HEAD` equals `deaabeb175593ec2c607b816eb80b7d16f4f01c5`.
- [ ] AESM local `HEAD` equals the final repository-side baseline commit recorded after this file is created.
- [ ] No DBP files have been modified for the new controlled request.
- [ ] Observer Protocol is not exposed to the Agent.

A local cleanliness claim must not be inferred from GitHub repository metadata.

## AESM Guidance Baseline

The AESM repository contains repository-level `AGENTS.md` as persistent Agent guidance.

The guidance establishes, among other things:

- separation of Human/Agent, Execution Environment, Runtime, Process Instance/Context;
- Runtime-mediated authoritative state mutation;
- recovery of an existing Process Instance for continuity;
- distinction between conversation history and authoritative state;
- evidence discipline;
- prohibition on fabricating Runtime-recognized state.

The experiment must observe whether and how this guidance is actually loaded and used. The presence of `AGENTS.md` alone is not evidence of operational participation.

## AESM Persistence Observation Point

The current Runtime implementation persists each Process Instance beneath the configured ProcessStore root:

```text
process-instance/<process_instance_id>/process.json
process-instance/<process_instance_id>/context.json
process-instance/<process_instance_id>/history.jsonl
```

The actual ProcessStore root is environment-configured. Before Agent launch, the observer must record:

- [ ] actual ProcessStore root;
- [ ] discovery method;
- [ ] accessible persistence files;
- [ ] independent search procedure for a Process Instance;
- [ ] procedure for comparing Runtime responses with persisted state.

No authoritative state is to be created or edited manually for experiment setup.

## Baseline Freeze Conditions

The experiment is ready to launch only after:

- Observer Protocol is finalized.
- Boundary contains REQ-01 through REQ-26.
- Implementation plan is reconciled with the current request.
- Approved Agent prompt is frozen.
- DBP local working tree is confirmed clean.
- DBP local `HEAD` matches the recorded baseline.
- AESM local `HEAD` matches the final repository-side preparation baseline.
- Actual AESM persistence root is established.
- Fresh Agent session identity and start time are recorded.
- Contamination controls are confirmed.

**Current repository-side state:** Prepared.

**Current experiment result:** Undetermined.

**Important:** This record does not replace the required live pre-launch checklist. Local Execution Environment facts must be recorded at the point of execution.
