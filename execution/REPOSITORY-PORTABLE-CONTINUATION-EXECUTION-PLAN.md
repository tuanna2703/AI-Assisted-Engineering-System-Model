# Repository-Portable Fresh-Agent Continuation — Execution Plan

## Purpose

Validate the repository-local AESM persistence migration empirically without modifying Runtime behavior.

The work is intentionally divided into two gates:

1. **Git Round-Trip Gate** — demonstrate that an existing DBP Process Instance stored under `<repo-root>/.aesm/` survives a Git commit/push/clone or equivalent checkout into a separate repository workspace.
2. **Fresh-Agent Repository-Scoped Continuation Gate** — demonstrate that a genuinely fresh Agent can recover and continue the same DBP Process Instance from the round-tripped repository-local state.

A final **Evidence Reconciliation** closes the work by comparing authoritative persisted state, Git state, Agent/session evidence, and DBP engineering artifacts.

## Guardrails

- Do not modify Runtime, ProcessStore, bridge semantics, or persistence layout during this validation.
- Do not create a second persistence store or a workspace-level fallback.
- Do not copy conversation transcripts or reconstructed Context into the target workspace.
- Do not treat Agent narrative as authoritative AESM state.
- Do not silently select another repository or Process Instance.
- Preserve the existing DBP Process Instance identity and authoritative history.
- Any failure is recorded first as evidence; implementation changes require a separate decision after reconciliation.
- The validation must distinguish repository portability from Agent continuity.

## Preconditions

### Repository-local persistence

The DBP source workspace must contain the authoritative PI under:

```
directories-builder-pro/.aesm/<process-instance-id>/
    process.json
    context.json
    history.jsonl
```

The three files must be parseable, internally consistent, and attributable to the same PI.

### Git visibility

Before the round-trip begins:

- `.aesm/` must not be ignored.
- The PI files must be tracked or explicitly staged.
- A clean baseline commit must be recorded.
- SHA-256 hashes of the three authoritative files must be captured.
- The DBP repository revision containing the PI must be recorded.

### Fresh-session capability

The Controller must be able to start a genuinely separate Agent session after the round trip.

## Git Round-Trip Gate

### Preparation

1. Freeze the current DBP PI state.
2. Record PI ID, scope identity, Context version, process state, history count, and relevant evidence.
3. Compute SHA-256 hashes for `process.json`, `context.json`, and `history.jsonl`.
4. Verify `.aesm/` is Git-visible.
5. Commit the repository-local PI state.
6. Record the resulting DBP commit SHA.

### Transfer

7. Create a separate checkout/clone/worktree from that commit.
8. Do not copy the original `.aesm/` directory outside Git.
9. Verify the three PI files exist in the new repository.
10. Recompute hashes and compare with the source snapshot.
11. Verify PI identity, scope identity, Context version/state, and history count are unchanged.

### Gate decision

**PASS** only if the repository-local authoritative state is reproduced through Git with matching integrity and no dependency on the source workspace.

**FAIL** if the PI is missing, ignored, altered, dependent on the old workspace, or requires manual reconstruction.

## Fresh-Agent Repository-Scoped Continuation Gate

### Bootstrap

1. End the source Agent session.
2. Start a genuinely fresh Agent session in the round-tripped repository.
3. Provide only the permitted repository/workspace context and the experiment bootstrap identifiers defined by the Controller protocol.
4. Do not provide the previous transcript, copied Context, or an implementation summary.

### Recovery

5. Require the fresh Agent to load persistent AESM guidance.
6. Require it to establish the active repository context for the round-tripped DBP repository.
7. Recover the existing PI through Runtime.
8. Acquire the authoritative Context from Runtime.
9. Verify the recovered PI ID and scope identity match the Git round-trip snapshot.
10. Verify prior history/evidence is observable from persisted state.

### Continuation

11. Perform one bounded, authorized Runtime-mediated continuation action.
12. Record a new authoritative history event attributable to the fresh session/runtime.
13. Verify Context version/state advances according to Runtime semantics.
14. Verify the new state persists to the repository-local `.aesm/`.
15. End the fresh session and independently re-read the persisted files.

### Negative controls

The experiment must also establish:

- A PI from another repository cannot be recovered through the DBP repository context.
- Missing/invalid active repository context does not silently fall back elsewhere.
- The fresh Agent cannot establish authoritative state from conversation text alone.
- The fresh Agent does not create a replacement PI merely because its session is new.

### Gate decision

**PASS** only if the fresh Agent recovers the same authoritative PI from the round-tripped repository and causes a new persisted Runtime-mediated event without prior-session narrative.

**FAIL** if recovery depends on transcript/bootstrap reconstruction, another persistence location, implicit repository selection, replacement PI creation, or non-authoritative Agent claims.

## Evidence Reconciliation

Reconcile five evidence classes:

| Evidence class | Required question |
|---|---|
| CONTROLLER | Were the gates executed under the registered protocol? |
| PERSISTED | Do the PI/context/history files prove continuity? |
| RUNTIME | Did Runtime recognize the fresh-session operation authoritatively? |
| AGENT | Did the fresh Agent actually interact with the established mechanism? |
| VERIFICATION | Can an independent read reproduce the claimed result? |

The reconciliation must preserve discrepancies rather than normalize them away.

## Completion Criteria

The work unit is complete when:

- Git Round-Trip Gate has a recorded PASS or an explicit failure classification.
- Fresh-Agent Repository-Scoped Continuation Gate has a recorded PASS or an explicit failure classification.
- Evidence is reconciled independently.
- No Runtime modification was introduced as part of the experiment.
- The final claim is limited to what the evidence demonstrates.

## Expected milestone

A successful result establishes:

> An AESM Process Instance stored inside a repository can be transferred through Git and recovered by a fresh Agent in another execution environment, where the fresh Agent can continue the engineering process through Runtime authority using the repository-local persisted state.

This claim must not be made unless both gates and reconciliation support it.
