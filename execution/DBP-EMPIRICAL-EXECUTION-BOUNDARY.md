# DBP Empirical Execution — Experiment Boundary

**Status:** Prepared — execution not started.

**Purpose:** Define the controlled boundary and evidence contract for the first real engineering task used to determine whether AESM actually participates in Agent execution.

## Experiment Objective

Execute one real, narrowly scoped Directories Builder Pro engineering request through the established Agent / Execution Environment / AESM Runtime mechanism.

The experiment is testing **AESM participation**, not merely successful code modification.

The central question is:

> When a human gives an Agent a real engineering request, does the Agent actually use the AESM process, Runtime, Process Instance, and Execution Context to govern and record the work?

## Controlled Engineering Request

Repository: `tuanna2703/directories-builder-pro`

Target file:

`modules/reviews/forms/add-review-form.php`

Target class:

`Add_Review_Form`

Target member:

`$business_id`

Required change:

```text
Fields_Manager::SELECT
→
Fields_Manager::POST_SELECT
```

The requested implementation scope is limited to this change. The Agent may investigate the repository and determine the appropriate implementation and verification details.

## Experiment Constraints

The fresh Agent must not be instructed to follow a prescribed AESM Runtime call sequence. In particular, the request must not prescribe calls such as `attach()`, `start_investigation()`, `record_artifact()`, or `begin_verification()`.

The experiment must not preload the Agent with:

- expected Process Instance state;
- expected Runtime operations;
- expected history entries;
- expected implementation details beyond the controlled request;
- an expected evidence classification;
- conclusions from prior validation sessions.

The following constraints remain binding:

- Do not modify DBP before the controlled Agent execution begins.
- Do not treat Agent statements as authoritative AESM state.
- Do not fabricate missing Runtime participation or persisted evidence.
- Do not broaden the DBP change beyond the agreed target.
- Do not modify AESM Runtime or semantics merely to make the experiment succeed.
- Do not count documentation reading alone as AESM operational participation.
- Do not declare the experiment successful merely because the DBP code change or tests succeed.

## Evidence Contract

The experiment must collect evidence sufficient to assess the following independently:

| Evidence area | Required question |
|---|---|
| Persistent guidance | Did the Agent actually receive applicable AESM guidance? |
| Process Instance | Was a real AESM Process Instance established or recovered for this task? |
| Execution Context | Did the Agent obtain authoritative context through the Runtime? |
| Engineering investigation | Did the Agent investigate the actual DBP implementation before changing it? |
| Runtime participation | Did Agent activity cause actual AESM Runtime operations? |
| State/evidence recording | Did Runtime operations produce authoritative persisted state? |
| Implementation | Was the requested DBP change actually made? |
| Verification | Was the resulting implementation independently or operationally verified? |
| Traceability | Can the engineering work be reconstructed from authoritative AESM state? |
| Agent boundary | Can Agent narrative be distinguished from Runtime/persisted evidence? |

## Authority Model for Evidence

Evidence must distinguish at least these layers:

1. **Agent said X** — narrative evidence only.
2. **Agent performed X** — observable execution evidence where available.
3. **Runtime recognized X** — authoritative Runtime result.
4. **Persisted state contains X** — authoritative persisted evidence.
5. **Independent repository verification shows X** — independently verified engineering result.

A statement in Agent conversation does not establish a Process Instance state, decision, artifact, verification, lifecycle status, or completion state unless the Runtime and/or persisted state confirms it.

## Expected Observation Sequence

The experiment should observe, without prescribing, whether the following relationship occurs:

```text
Human engineering request
        ↓
Persistent AESM guidance available to Agent
        ↓
Process Instance established/recovered
        ↓
Authoritative Execution Context obtained
        ↓
Agent investigates DBP
        ↓
AESM Runtime participates in the engineering process
        ↓
Evidence / decisions / artifacts / verification are persisted
        ↓
DBP implementation is performed
        ↓
Implementation is verified
        ↓
Authoritative process state reflects the actual work
```

This is an observation model, not a required Agent script.

## Independent DBP Verification

After Agent execution, inspect the DBP repository independently of the Agent's final narrative.

Verify at minimum:

- the target file changed;
- the target class/member is the subject of the change;
- `Fields_Manager::SELECT` became `Fields_Manager::POST_SELECT` as requested;
- no unrelated DBP modifications were introduced by the experiment;
- the resulting code is structurally/syntactically valid;
- relevant tests or verification procedures were run where applicable.

## Independent AESM Persistence Verification

Inspect the actual AESM persistence mechanism independently of the Agent's explanation.

Verify where available:

- Process Instance identity;
- Process Instance lifecycle;
- current process state;
- Execution Context contents;
- evidence;
- decisions;
- artifacts;
- verification;
- history entries;
- state/version changes;
- Runtime identifiers;
- consistency between Runtime responses and persisted files.

## Engineering Trace Assessment

Determine whether the authoritative AESM state provides a meaningful correspondence to the real DBP work.

The target trace is conceptually:

```text
request
  → investigation
  → relevant finding
  → decision
  → implementation
  → verification
  → completion
```

The experiment must determine whether this trace is actually represented by authoritative AESM state, rather than reconstructed solely from the Agent conversation.

## Result Classification

Use the established evidence categories where applicable:

- **Demonstrated** — independently observable evidence establishes the capability.
- **Evidence Incomplete** — implementation or behavior exists, but required evidence is missing.
- **Implementation Gap** — a required mechanism does not exist.
- **Specification/Applicability Decision Required** — existing authority does not determine the required behavior.
- **Not Applicable** — the capability is not applicable to this experiment.

The overall result must be evidence-based. A successful DBP code change does not by itself establish successful AESM participation.

## Fresh-Agent Requirement

The actual DBP execution must begin from a genuinely fresh Agent invocation. The fresh Agent may receive only the information legitimately supplied through the established Execution Environment mechanism plus the controlled engineering request and any process-specific information required by that mechanism.

Prior mechanism-validation conclusions must not be injected as expected execution outcomes.

## Completion Condition

This boundary artifact is complete when the experiment has been executed and a dedicated empirical execution report records the actual observations, independently verified DBP result, independently verified AESM persistence, discrepancies, limitations, classifications, and final conclusion.

Until then, the DBP empirical result remains **undetermined**.
