# Repository-Portable Fresh-Agent Continuation — Execution Plan

## Purpose

Validate repository-local AESM persistence as a portable engineering record through a Git round trip and a genuinely fresh Agent continuation, without modifying Runtime behavior.

This is a validation work unit, not a Runtime implementation change.

## Scope

The work has three semantic workstreams:

### Git Round-Trip Integrity

Demonstrate that an existing repository-local Process Instance survives transfer through Git into an independent repository workspace.

Tasks:
- Freeze and record the source PI baseline.
- Verify `.aesm/` is not ignored and all authoritative PI files are Git-visible.
- Record SHA-256 hashes for `process.json`, `context.json`, and `history.jsonl`.
- Commit the repository-local PI state and record the source revision.
- Create an independent checkout from that revision without copying `.aesm/` outside Git.
- Recompute hashes and verify byte-level identity.
- Verify PI identity, scope identity, Context version/state, lifecycle, and history count are unchanged.
- Record PASS/FAIL/BLOCKED evidence for the Git gate.

Exit condition: authoritative PI state is reproduced solely through Git with matching integrity and no dependency on the source workspace.

### Fresh-Agent Repository-Scoped Continuation

Demonstrate that a genuinely fresh Agent can recover and continue the round-tripped PI.

Tasks:
- End the source Agent session before starting the continuation session.
- Start a separate Agent session in the round-tripped repository.
- Provide only repository/workspace bootstrap context; do not provide the prior transcript, PI identity, expected state, Context version, or history count.
- Require the Agent to inspect repository-local `.aesm/` and identify the applicable PI.
- Recover the PI through the supported Runtime/bridge mechanism.
- Obtain authoritative Execution Context from Runtime.
- Verify recovered state against the Git-round-trip snapshot.
- Perform exactly one bounded Runtime-mediated continuation.
- Verify Context advancement and a new persisted history event attributable to the fresh Runtime/session.
- Independently inspect `.aesm/` after continuation.
- Verify no replacement PI was created and no alternate persistence boundary was used.
- Record PASS/FAIL/BLOCKED/PARTIAL evidence.

Exit condition: fresh Agent recovery and continuation are demonstrated from round-tripped repository state without prior-session narrative.

### Evidence Reconciliation

Reconcile CONTROLLER, PERSISTED, RUNTIME, AGENT, and VERIFICATION evidence.

Tasks:
- Preserve discrepancies rather than normalizing them.
- Separate Git portability evidence from Agent continuity evidence.
- Do not claim remote Git portability from same-filesystem evidence.
- Do not claim fresh-Agent continuity from file existence alone.
- Record limitations and failed gates explicitly.
- Produce one final evidence-based work-unit classification.

Exit condition: every claimed capability has corresponding evidence, and unsupported claims remain explicitly unclaimed.

## Guardrails

- No Runtime, ProcessStore, bridge, schema, scope-resolution, or persistence-layout changes.
- No second persistence store.
- No workspace-level fallback.
- No manual copying of `.aesm/` into the target checkout.
- No conversation transcript transfer.
- No reconstruction of authoritative Context from narrative.
- No replacement PI solely because the Agent/session changed.
- No `AgentRuntimeBridge.discover()` use for objective-to-PI discovery.
- Filesystem inspection may identify candidate PIs, but Runtime `attach()` remains authoritative recovery.
- Any implementation defect discovered during validation becomes a separate work item; do not repair it opportunistically.

## Preconditions

- Source repository contains one applicable authoritative PI under `<repo-root>/.aesm/<pi-id>/`.
- `process.json`, `context.json`, and `history.jsonl` are parseable and internally consistent.
- `.aesm/` is Git-visible.
- Source working tree is understood and unrelated changes are excluded from the snapshot.
- An independent checkout mechanism is available.
- A genuinely fresh Agent session can be started in the target checkout.

## Gate Criteria

### Git Round-Trip Gate

**PASS** only when PI files are transferred through Git, all hashes match, authoritative identity/state match, and no source-workspace dependency remains.

**FAIL** when Git loses, alters, or cannot reproduce the authoritative PI state.

**BLOCKED** when independent Git transfer cannot be performed because of an external/environmental limitation.

### Fresh-Agent Continuation Gate

**PASS** only when a fresh Agent independently discovers the applicable PI, Runtime attaches to the existing PI, authoritative Context is recovered, exactly one qualifying continuation is Runtime-mediated, Context advances, new history persists with fresh-session attribution, and no replacement PI or alternate store is used.

**PARTIAL** when substantial continuity is demonstrated but one bounded protocol condition cannot be demonstrated.

**FAIL** when the completed experiment disproves required continuity.

**BLOCKED** when recovery/continuation cannot reach the required validation point.

## Completion

The work unit closes only after both gates have explicit classifications, evidence classes are reconciled, no Runtime implementation change was introduced, the final claim is limited to demonstrated behavior, and `IMPLEMENTATION_PLAN.md` is updated from observed evidence.

> Expected successful claim: an AESM Process Instance stored under repository-local `.aesm/` can be transferred through Git and recovered by a genuinely fresh Agent in an independent repository workspace, where the Agent can continue the same engineering process through Runtime authority.

This claim is made only if both gates and reconciliation support it.