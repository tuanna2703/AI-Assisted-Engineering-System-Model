# Runtime Consistency and Continuity Hardening

## Scope

This record captures implementation decisions and changes made under the Runtime Consistency and Continuity Hardening work unit.

## Persistence State Consistency

Runtime mutations that modify authoritative Execution Context before persistence now snapshot the prior Context and restore it when the authoritative write fails.

Covered mutation paths include:

- process-state transitions through the state-transition helper;
- pending execution recording;
- reconsideration;
- engineering completion recognition;
- implementation and verification entry operations whose pre-persistence preparation mutates Context.

Failure-path tests compare the live Runtime Context, history count, and freshly reloaded persisted Context.

## Persisted Schema

Persisted Process Instance and Execution Context records now carry schema_version = 1.

Compatibility contract:

- missing schema_version is treated as version 1 for existing repository state;
- unsupported versions are rejected with PersistenceError;
- no automatic transformation of unknown future versions is attempted.

This keeps repository-local .aesm state portable without silently interpreting an incompatible schema.

## Process Instance Concurrency

Process Instance writes now use optimistic concurrency based on the persisted updated_at value captured by the Runtime when the Process Instance was loaded.

A write is rejected when the persisted Process Instance has changed since load. This prevents one Runtime from overwriting another Runtime's newer Process Instance binding/lifecycle state.

Context writes retain their existing version-based stale-write guard.

## Lifecycle Resumption

Resumption from SUSPENDED -> ACTIVE no longer infers authority from words inside semantic_basis.

The authoritative determination is now structured:

~~~json
{
  "resumption_determination": {
    "status": "PERMITTED",
    "basis": "..."
  }
}
~~~

Only PERMITTED is accepted. Missing, REJECTED, ambiguous, malformed, or explicitly conflicting determinations are rejected. semantic_basis remains traceability text.

## Cross-Process Validation Artifacts

The independent-process validation scripts were migrated to the current repository-local persistence boundary:

~~~text
<temporary repository root>/.aesm/<process-instance-id>/
~~~

Both processes now construct ActiveRepositoryContext and Runtime through the current API. Observation contributions include explicit Runtime recognition.

The environment-mechanism probe was likewise migrated to ActiveRepositoryContext.

## Multi-File Recovery Boundary

process.json, context.json, and history.jsonl remain separately atomically written files. Existing rollback restores the affected files after ordinary persistence exceptions.

No generalized transaction layer was introduced.

An abrupt hard process crash between successful file replacements is not claimed to be transaction-atomic. Repository/Git history remains the recovery mechanism for committed .aesm state; unresolved or inconsistent local state must not be treated as automatically reconciled.

## Verification Status

Implementation changes are complete for the targeted hardening work.

Behavioral regression and the repaired cross-process experiment still require execution in an environment with the repository checkout and test dependencies available. The implementation record does not claim those runs passed until their evidence is available.
