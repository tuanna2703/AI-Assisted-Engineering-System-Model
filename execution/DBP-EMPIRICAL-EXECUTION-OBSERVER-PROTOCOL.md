# DBP Empirical Execution — Observer Protocol

**Status:** Finalized — pre-execution
**Purpose:** Observer-only protocol for collecting and classifying evidence during the controlled Directories Builder Pro empirical execution.
**Audience:** Experiment observer only. This protocol must not be supplied to the Agent or used as Agent task instructions.

## 1. Experiment Identity

Record before execution:

- Fresh Agent session identifier.
- Agent model.
- Execution Environment and relevant host/tooling mechanism.
- Start time (UTC).
- End time (UTC).
- DBP repository URL and baseline commit.
- DBP working-tree cleanliness at baseline.
- AESM repository URL and baseline commit.
- Approved fresh-Agent prompt revision/hash.
- Observer Protocol revision/hash.
- AESM persistent guidance available at baseline, including repository-level `AGENTS.md`.
- Other persistent Agent guidance files or mechanisms actually present.

The controlled DBP repository is `tuanna2703/directories-builder-pro`.

The AESM repository is `tuanna2703/AI-Assisted-Engineering-System-Model`.

## 2. Evidence Sources

Collect evidence from the following sources where available:

1. Agent conversation/output.
2. Observable Agent tool and command activity.
3. DBP repository status and final diff.
4. Independent DBP test or verification results.
5. AESM Process Instance persistence, including `process.json`, `context.json`, and `history.jsonl` where present.
6. Runtime responses and identifiers.
7. Persisted evidence, decisions, artifacts, verification, and process-state/history records.
8. Independent post-execution inspection performed before reading the Agent's final report.

Do not infer hidden reasoning. Only reasoning or decision content exposed through the Agent's observable conversation/output may be recorded.

## 3. Evidence Authority

Evidence levels describe what each source can establish; they do not automatically resolve contradictions.

| Level | Source | What it establishes |
|---|---|---|
| 1 | Agent said X | Agent narrative only |
| 2 | Agent performed X | Observable execution evidence where available |
| 3 | Runtime recognized X | Authoritative Runtime result |
| 4 | Persisted state contains X | Authoritative persisted evidence |
| 5 | Independent engineering verification shows X | Independent engineering result |

When evidence conflicts, preserve the conflict explicitly. Do not erase or silently resolve a discrepancy by assigning a higher level. Report which sources support each competing observation.

In particular, an Agent statement does not establish Process Instance state, decision, artifact, verification, lifecycle status, or completion unless Runtime and/or persisted state confirms it.

## 4. AESM Participation Determination

Assess each item independently.

### 4.1 Guidance availability

Determine:

- Which persistent AESM guidance mechanisms were available to the Agent.
- Whether the relevant guidance was accessible through the actual Execution Environment.
- Whether there is observable evidence that the Agent loaded or accessed applicable guidance.
- Whether observed behavior is consistent with that guidance.

Availability or behavioral consistency alone does not prove causal influence.

### 4.2 Process Instance

Determine whether:

- a real Process Instance was created or recovered;
- its identity is independently observable;
- its persistence can be located and inspected;
- the Agent interacted with it through an established mechanism.

Do not count a manually created, observer-created, or fabricated Process Instance as Agent participation.

### 4.3 Authoritative Execution Context

Determine whether:

- the Agent obtained the authoritative Context;
- the Context belongs to the observed Process Instance;
- the Runtime returned the Context;
- subsequent persisted state reflects Context changes where applicable.

### 4.4 Runtime participation

Determine whether Agent activity caused actual Runtime operations.

Record:

- operation;
- observable invocation evidence;
- Runtime response;
- resulting state;
- persistence evidence.

Do not infer Runtime participation solely from the Agent's description of what it intended or believed it did.

### 4.5 Persisted engineering evidence

Determine whether the Runtime/persistence layer contains evidence relevant to:

- investigation;
- findings;
- decisions;
- implementation artifacts;
- verification;
- reconsideration where applicable;
- process state;
- completion.

### 4.6 Agent boundary

Maintain a clear distinction between:

- what the Agent reported;
- what the Agent visibly executed;
- what Runtime recognized;
- what persisted state contains;
- what independent repository inspection establishes.

## 5. AESM Persistence Observation Procedure

The observer must independently establish the persistence location before or at the start of evidence collection.

Record:

- actual Process Instance store root;
- discovery method;
- files inspected;
- Process Instance identifier(s) searched;
- search scope if no Process Instance is found.

For the current Runtime implementation, a Process Instance is persisted beneath the configured ProcessStore root using:

- `process-instance/<process_instance_id>/process.json`
- `process-instance/<process_instance_id>/context.json`
- `process-instance/<process_instance_id>/history.jsonl`

The observer must determine the actual configured root for the experiment environment rather than assuming a fixed absolute filesystem path.

Do not ask the Agent to define or fabricate the persistence location for evidence purposes.

## 6. Engineering Trace Reconstruction

Reconstruct the real engineering work as far as authoritative evidence permits:

```
request
  → investigation
  → relevant finding
  → decision
  → implementation
  → verification
  → completion
```

For every stage, record:

- observed evidence;
- evidence level;
- whether the stage is represented in authoritative Runtime/persisted state;
- whether independent repository evidence corroborates it;
- whether the stage can only be reconstructed from Agent narrative.

Do not convert a narrative-only trace into authoritative AESM evidence.

## 7. Requirement Reconciliation

Perform independent DBP inspection before reading the Agent's final assessment.

For each requirement REQ-01 through REQ-26, assign one status:

- **Present** — independently verified as satisfied.
- **Partial** — some required behavior is present, but the requirement is incomplete.
- **Absent** — required behavior is not present.
- **Unverifiable** — available evidence is insufficient to establish the requirement.
- **Conflicted** — evidence sources disagree materially.

Use the controlled request in `execution/DBP-EMPIRICAL-EXECUTION-BOUNDARY.md` as the requirement authority.

After the independent inspection, compare the result with the Agent's own final assessment and preserve discrepancies.

## 8. Classification

Apply the established classification to each applicable AESM participation question, trace stage, and requirement where relevant:

- **Demonstrated** — independently observable evidence establishes the capability or result.
- **Evidence Incomplete** — implementation or behavior exists, but required evidence is missing.
- **Implementation Gap** — a required mechanism does not exist.
- **Specification/Applicability Decision Required** — existing authority does not determine the required behavior.
- **Not Applicable** — the capability is not applicable to this experiment.

Do not produce an overall score, ranking, or pass/fail rating.

## 9. Pre-Execution Checklist

Before launching the fresh Agent, verify and record:

- [ ] DBP baseline commit recorded.
- [ ] DBP working tree confirmed clean in the actual execution environment.
- [ ] AESM baseline commit recorded.
- [ ] Applicable persistent AESM guidance identified.
- [ ] Actual AESM Process Instance store root independently established.
- [ ] Approved Agent prompt revision recorded.
- [ ] Observer Protocol revision recorded.
- [ ] Fresh Agent session identity available.
- [ ] Observer Protocol is inaccessible to the Agent.
- [ ] Observer has not communicated experimental expectations, evidence criteria, or classifications to the Agent.
- [ ] No expected Process Instance state was supplied to the Agent.
- [ ] No expected Runtime operation sequence was supplied to the Agent.
- [ ] No DBP modification has occurred before controlled execution.
- [ ] Independent DBP test/verification capability is available.
- [ ] Baseline timestamps recorded.

If any required precondition is not satisfied, record it explicitly before execution.

## 10. Post-Execution Checklist

After the Agent ends:

- [ ] Record end time (UTC).
- [ ] Preserve the Agent conversation/output available through the environment.
- [ ] Preserve observable tool/command activity.
- [ ] Inspect DBP status and diff before reading the Agent's final report.
- [ ] Inspect AESM persistence independently.
- [ ] Run independent DBP tests or verification.
- [ ] Record Runtime responses/identifiers where available.
- [ ] Reconcile REQ-01 through REQ-26 independently.
- [ ] Read the Agent's final report after independent inspection.
- [ ] Record discrepancies between Agent claims and independent evidence.
- [ ] Reconstruct the engineering trace.
- [ ] Classify AESM participation and engineering outcomes.
- [ ] Produce the empirical execution report.

The observer must not modify DBP or authoritative AESM persistence between execution and evidence collection.

## 11. Final Empirical Report

The dedicated report under `execution/` must contain:

1. Experiment identity and baselines.
2. Evidence collected by source and authority level.
3. AESM guidance findings.
4. Process Instance findings.
5. Execution Context findings.
6. Runtime participation findings.
7. Persisted state/evidence findings.
8. Independent DBP implementation verification.
9. Requirement reconciliation for REQ-01 through REQ-26.
10. Engineering trace reconstruction.
11. Classification results.
12. Agent-vs-authoritative discrepancies.
13. Limitations and unverifiable areas.
14. Evidence-based conclusion about actual AESM participation.

The report must distinguish demonstrated facts, incomplete evidence, implementation gaps, specification/applicability questions, and non-applicable capabilities.

## 12. Contamination and Scope Controls

The observer must not:

- tell the Agent that the experiment is testing AESM participation;
- prescribe AESM Runtime calls or a required execution sequence;
- preload an expected Process Instance;
- preload expected Context contents;
- supply expected evidence, history, decisions, artifacts, or verification;
- reveal this Observer Protocol;
- steer the Agent toward producing evidence;
- alter DBP implementation to improve the experiment;
- alter AESM Runtime or semantics merely to make the experiment succeed;
- backfill or fabricate AESM evidence after engineering work;
- treat documentation reading alone as operational participation.

The controlled engineering request remains the sole DBP task authority.

## 13. Observation Model

The following is an observation model, not an Agent script:

```
Human engineering request
        ↓
Persistent AESM guidance available
        ↓
Process Instance established/recovered
        ↓
Authoritative Execution Context obtained
        ↓
Agent investigates DBP
        ↓
AESM Runtime participates
        ↓
Evidence / decisions / artifacts / verification persist
        ↓
DBP implementation occurs
        ↓
Implementation is verified
        ↓
Authoritative process state reflects the work
```

The experiment determines which parts of this relationship actually occur and what evidence supports each part.

## 14. Completion State

Before execution, the empirical result is **undetermined**.

The experiment is complete only when the dedicated empirical report records actual observations, independent DBP verification, independent AESM persistence verification, discrepancies, limitations, classifications, and the evidence-based conclusion.

**Protocol status:** Ready for pre-execution baseline and fresh-Agent execution.
