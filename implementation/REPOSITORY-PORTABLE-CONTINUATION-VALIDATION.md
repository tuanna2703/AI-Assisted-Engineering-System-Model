# AESM Repository-Portable Continuation Validation — Final Evidence Record

## Purpose

Record the completed repository-portable continuation validation as durable engineering evidence. This validation evaluates repository-local `.aesm/` persistence through a Git round trip and a genuinely fresh Agent continuation without modifying Runtime behavior.

## Validation Identity

| Field | Value |
|---|---|
| Repository | `tuanna2703/AI-Assisted-Engineering-System-Model` |
| Source revision | `2a6625a00b49764c575a5784616fc35087843bc7` |
| Process Instance | `f713278b-cb74-4a49-a6a1-b6713f058b56` |
| Scope Identity | `AESM-Repository-Portability-and-Cross-Session-Continuity-Validation` |
| Source state | `investigation` |
| Source Context version | `3` |
| Source history count | `5` |
| Independent checkout | `/tmp/aesm-session-a-validation-1789978403` |

## Session A — Git Round-Trip Integrity

Session A completed the source snapshot and independent-checkout transfer.

### Preflight

All required capabilities were available:

- shell execution;
- filesystem read/write;
- Git CLI;
- repository state inspection;
- SHA-256 calculation;
- independent Git checkout;
- Runtime/bridge access;
- remote cloning.

### Source persistence snapshot

The applicable PI was independently identified under repository-local `.aesm/`.

| File | SHA-256 |
|---|---|
| `process.json` | `7d498030586c6fcf1965db07c6610077f9cedd4fb953cb580824a0b87f589b79` |
| `context.json` | `144f5a986cfa6178691501a882405ac4ef0b40113d2075abb1b52b6036fe9d0c` |
| `history.jsonl` | `be5b12205709582b24361aa1330444b30d25d960770acb3eada00654e48d9863` |

The source working tree was clean. `.aesm/` was Git-visible, and no workspace `.aesm-process-store` or alternate persistence store was present.

### Independent checkout

A fresh remote `git clone` was created from GitHub at the same revision. The checkout obtained `.aesm/` through Git rather than manual copying or a worktree.

All three PI-file hashes matched the source snapshot exactly. PI identity, scope identity, lifecycle, state, Context version, history count, and Git revision also matched.

**Git Round-Trip Integrity: PASS**

**Environment Independence: PASS**

## Session B — Fresh-Agent Repository-Scoped Continuation

Session B was conducted as a separate Agent conversation in the independent checkout.

Only bootstrap information was supplied:

- repository URL;
- exact Git revision;
- independent checkout path.

The Session B Agent was not supplied with the PI ID, source Context version, source history count, source hashes, prior transcript, or expected operation.

### Independent discovery

Session B inspected repository-local `.aesm/` and independently discovered:

- PI `f713278b-cb74-4a49-a6a1-b6713f058b56`;
- scope `AESM-Repository-Portability-and-Cross-Session-Continuity-Validation`;
- lifecycle `active`;
- state `investigation`;
- Context version `3`;
- history count `5`.

The pre-operation hashes matched Session A exactly.

### Runtime recovery

Session B established ActiveRepositoryContext against the independent checkout and used the existing Runtime/bridge:

`bridge.attach("f713278b-cb74-4a49-a6a1-b6713f058b56")`

Runtime recovery returned the existing PI and Context version 3. Runtime `aesm_root()` resolved to the checkout-local `.aesm/`.

No workspace persistence store or alternate repository was used.

### Bounded continuation

Session B declared continuation intent before execution and performed exactly one Runtime-mediated `observe()`.

Expected transition:

`Context 3 → 4`

`history 5 → 6`

Observed transition:

- same PI identity;
- Context version advanced from 3 to 4;
- history count advanced from 5 to 6;
- one new `evidence_recorded` history event;
- event attributed to Runtime ID `session-b-fresh-agent`;
- process state remained `investigation`.

### Persisted verification

After continuation:

- `process.json` hash remained unchanged;
- `context.json` hash changed as expected;
- `history.jsonl` hash changed as expected;
- persisted Context version was 4;
- persisted history count was 6;
- Git diff contained only the expected Context/history changes;
- no replacement PI was created;
- no alternate persistence store was introduced.

**Fresh-Agent Repository-Scoped Continuation: PASS**

## Evidence Reconciliation

| Evidence class | Demonstrated evidence |
|---|---|
| CONTROLLER | Only repository/revision/checkout bootstrap was supplied to Session B |
| AGENT | Fresh session independently discovered the applicable PI |
| RUNTIME | Runtime attach and exactly one observe returned authoritative state |
| PERSISTED | Direct `.aesm/` inspection, hashes, Context version, and history event |
| VERIFICATION | Recovery checks, pre/post identity checks, Git diff, and persistence checks |

The validation therefore separates Agent discovery from Runtime authority and persisted evidence. Agent narrative was not used as the authoritative continuity state.

## Boundaries and Limitations

The experiment does not claim that a surrounding host conversation could never leak contextual information. Session B correctly recorded that limitation because the experiment cannot independently prove what external conversation-summary machinery may have exposed beyond the explicitly supplied bootstrap facts.

This limitation does not alter the demonstrated repository transfer, Runtime recovery, persisted continuity, or fresh-session attribution results.

The validation also does not claim that arbitrary multi-repository engineering scopes are automatically resolved. It demonstrates repository-scoped recovery for the controlled PI in the independent checkout.

## Final Classification

| Gate / capability | Result |
|---|---|
| Git Round-Trip Integrity | **PASS** |
| Environment Independence | **PASS** |
| Fresh-Agent Repository-Scoped Continuation | **PASS** |
| Runtime Authority | **PASS** |
| Repository Persistence Boundary | **PASS** |
| Overall Repository-Portable Continuation Validation | **PASS** |

## Implementation Impact

No Runtime, ProcessStore, bridge, schema, scope-resolution, or persistence-layout implementation changes were made for this validation.

The repository-local `.aesm/` persistence boundary remains the demonstrated continuity mechanism.

This record closes the validation work unit. Future work should use these results as evidence and should not reopen the validated mechanism merely to repeat the experiment.
