# Project Identity and Process Binding Implementation

## Status

**Implementation complete; execution validation pending.**

This work unit implements the smallest vertical slice for authoritative Engineering Scope Identity and Process Instance binding without introducing a second authority layer.

## Implemented scope

The implementation now provides:

- explicit Engineering Scope resolution state on the Process Instance;
- authoritative Engineering Scope Identity when resolution is RESOLVED;
- explicit UNRESOLVED, AMBIGUOUS, CONFLICTING, and INVALID outcomes;
- Runtime-mediated scope resolution and binding;
- persistent Process Instance binding through the existing ProcessStore;
- recovery of scope binding through the existing Runtime/ProcessStore path;
- historical traceability for scope-resolution mutations;
- Agent–Runtime Bridge access to the Runtime scope-resolution operation;
- rejection of silent rebinding after an authoritative scope has been established.

No new persistence store, discovery index, Agent orchestrator, IDE-specific mechanism, MCP dependency, or parallel authority was introduced.

## Implementation boundary

The vertical slice intentionally does not implement:

- objective-to-scope candidate discovery;
- repository/workspace heuristic matching;
- duplicate Process Instance detection;
- automatic scope selection;
- objective-to-Process-Instance discovery;
- multi-project orchestration;
- a first-class Project entity;
- Agent-owned scope authority.

Those remain later validation/design concerns established by the completed semantic and normative gates.

## Runtime state model

ProcessInstance now carries:

- engineering_scope_identity
- engineering_scope_resolution
- engineering_scope_evidence

Resolution status is one of:

- UNRESOLVED
- RESOLVED
- AMBIGUOUS
- CONFLICTING
- INVALID

A RESOLVED state requires a non-empty scope identity. Other states cannot carry an authoritative scope identity.

Once a scope is resolved, a different identity cannot replace it through the scope-resolution operation. This prevents repository, workspace, Agent, or Runtime-session observations from silently replacing an established binding.

## Persistence and recovery

Scope state is stored with the existing process.json representation.

The existing ProcessStore remains the persistence authority. Scope-binding mutation is persisted through a dedicated Process Instance persistence boundary that snapshots the affected Process Instance and history files before mutation and restores them on failure.

Scope-resolution history records include:

- prior resolution status and identity;
- resulting resolution status and identity;
- resolution basis;
- actor;
- evidence;
- Runtime identifier.

Recovery uses the existing Runtime.attach() -> ProcessStore.load_instance() path, so the recovered scope binding comes from authoritative persisted Process Instance state rather than conversation or environment reconstruction.

## Agent boundary

The Agent–Runtime Bridge now exposes apply_scope_resolution as a delegated Runtime operation.

The bridge does not resolve scope, persist scope, or maintain a competing binding. It forwards the request to Runtime, and Runtime performs validation and authoritative mutation.

## Validation

Added targeted tests cover:

1. new Process Instances start with explicit UNRESOLVED scope state;
2. resolved scope identity is persisted;
3. resolved scope survives Runtime replacement;
4. all non-resolved outcomes remain explicit;
5. non-resolved outcomes survive recovery;
6. established scope cannot be silently rebound;
7. malformed resolved outcomes do not mutate binding;
8. scope resolution requires explicit Runtime recognition;
9. the Agent–Runtime Bridge can submit a resolution without owning the binding;
10. corrupted persisted scope state is rejected.

The repository's available GitHub integration does not expose a direct workflow-dispatch or local test-execution capability in this environment, and the repository has no workflow run associated with the implementation test commit. Therefore the tests were added but not executed here. No test result is being inferred from static inspection.

## Gate interpretation

The implementation work itself is complete.

The implementation-validation gate remains open until the targeted test suite is executed in a repository execution environment.

## Next authorized work

After implementation validation, proceed to Multi-Project Empirical Validation. That work should use real Agent execution to test scope isolation, ambiguity handling, Process Instance selection/creation boundaries, and cross-session discovery without converting environmental evidence into independent authority.
