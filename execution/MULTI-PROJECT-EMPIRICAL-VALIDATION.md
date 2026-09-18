# Multi-Project Empirical Validation

## Status

**IMPLEMENTATION PREPARED — EXECUTION PENDING**

This artifact defines and records the executable multi-project validation boundary. The implementation adds only targeted validation coverage; it does not add a Project entity, project registry, discovery mechanism, multi-project orchestrator, or second authority store.

The experiment is intended to determine whether the existing Engineering Scope Identity, Process Instance, ProcessStore, Runtime, and Agent–Runtime Bridge contracts remain isolated when multiple engineering scopes coexist.

## Experimental objective

Demonstrate that the existing implementation can maintain independent authoritative scope state for multiple Process Instances without:

- silently rebinding an established Process Instance;
- confusing one project with another;
- leaking scope state between Process Instances;
- depending on Runtime session memory for recovery;
- turning unresolved scope into inferred scope;
- introducing a second authority mechanism.

## Participating scopes

The executable scenarios use stable test identities corresponding to the two existing engineering repositories:

- `project:tuanna2703/directories-builder-pro`
- `project:tuanna2703/AI-Assisted-Engineering-System-Model`

These strings are experimental Engineering Scope identities. The test does not assert that a repository is universally equivalent to an Engineering Scope.

## Existing mechanisms under test

No new multi-project mechanism is introduced.

The tests exercise:

- `ProcessInstance`
- `ProcessStore`
- `Runtime`
- `AgentRuntimeBridge`
- existing Engineering Scope resolution and binding persistence

The Agent–Runtime Bridge remains a delegating boundary. Authoritative scope state remains on the Process Instance and is persisted by ProcessStore.

## Experimental scenarios

### Independent projects

Create two Process Instances and bind them independently:

```
Process Instance A → Project A
Process Instance B → Project B
```

Verify both identity and persisted history.

### Multiple Process Instances within one scope

Create two Process Instances for Project A.

Verify that the Process Instances remain distinct even though they share the same Engineering Scope Identity.

### Project switching

Persist Process Instance A for Project A, create and persist Process Instance B for Project B, then recover A in a fresh Runtime.

Verify that A still resolves to Project A.

### Conflicting rebinding

Bind A to Project A, then submit Project B as a second resolution.

Expected result:

- Runtime rejects the operation;
- in-memory authoritative binding remains Project A;
- persisted binding remains Project A;
- no additional successful binding history entry is created.

### Independent unresolved state

Keep separate Process Instances in `UNRESOLVED` and `AMBIGUOUS` states.

Verify that each state remains independent and contains no authoritative scope identity.

### Cross-instance contamination

Bind one Process Instance to Project B while another remains unresolved.

Recover both independently and verify that the unresolved Process Instance does not acquire Project B.

### Agent → Bridge → Runtime authority

Submit scope resolutions through two independent Agent–Runtime Bridge instances.

Verify that each bridge operation mutates only its attached Process Instance and that authoritative state is still persisted by ProcessStore.

### Bridge-level conflicting binding

Submit a conflicting scope through the bridge after an established binding exists.

Verify that the bridge returns the Runtime rejection and exposes the unchanged authoritative state.

### Fresh Runtime recovery

Stop the Runtime that established Project A, work with Project B in a separate Runtime, then attach Process Instance A using a fresh Runtime.

Verify that the recovered scope comes from persisted Process Instance state rather than Runtime session memory.

## Evidence requirements

A scenario is not considered demonstrated from an exception alone.

For each isolation or rejection scenario, evidence must inspect:

1. Runtime outcome;
2. in-memory Process Instance state where applicable;
3. persisted Process Instance state;
4. relevant history where applicable;
5. Process Instance identity;
6. Engineering Scope Identity;
7. Engineering Scope resolution status.

## Evidence classification

Use the existing classifications:

- **Conformant — Demonstrated**
- **Conformant — Evidence Incomplete**
- **Implementation Gap — Semantically Required**
- **Not Applicable**
- **Specification / Applicability Decision Required**

Do not introduce a new classification for this experiment.

## Non-goals

This validation does not implement or validate:

- project discovery;
- automatic project selection;
- project registries;
- multi-project orchestration;
- automatic Process Instance discovery;
- workspace heuristics;
- IDE integration;
- MCP integration;
- Agent memory;
- a new Project entity;
- a second persistence or authority mechanism.

If the experiment reveals a missing semantic or mechanism contract, that finding must be separated from the experiment and treated as a subsequent design decision.

## Execution boundary

The targeted test suite is:

```
PYTHONPATH=. .venv/bin/pytest -v tests/multi_project/test_multi_project_scope_isolation.py
```

Regression coverage should include the already established project-binding and recovery tests:

```
PYTHONPATH=. .venv/bin/pytest -v \
  tests/project_identity/test_scope_binding.py \
  tests/lifecycle/test_runtime_lifecycle.py \
  tests/continuity/test_runtime_recovery.py \
  tests/multi_project/test_multi_project_scope_isolation.py
```

The repository integration environment available to this execution does not provide a local checkout or executable Python environment, so these commands are recorded as the required execution boundary rather than reported as executed results.

## Stop conditions

Stop the work unit if:

- an existing contract is insufficient to explain an observed result;
- a mechanism defect is exposed;
- a test requires a new authority mechanism;
- the experiment would require project discovery or orchestration to proceed.

Do not modify Runtime semantics merely to make the experiment pass.

## Expected result categories

### Existing contracts demonstrated

If all required scenarios pass, record the multi-project isolation behavior as demonstrated and close the validation gate.

### Evidence incomplete

If the implementation appears correct but execution evidence cannot be obtained, record the evidence gap without inferring conformance.

### Mechanism gap

If the semantic contract is clear but the implementation cannot satisfy it, stop and record a separate implementation/mechanism decision.

### Semantic gap

If existing semantics cannot determine the correct behavior, stop and create a separate semantic decision before changing implementation.

## Implementation boundary

The implementation for this work unit is intentionally limited to:

- executable multi-project behavioral tests;
- this empirical validation record;
- plan-status reconciliation after evidence is actually available.

No Runtime, ProcessStore, Bridge, schema, or semantic implementation change is authorized by this work unit unless the empirical evidence independently establishes a separate gap.
