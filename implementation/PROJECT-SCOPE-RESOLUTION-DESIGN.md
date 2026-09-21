# Project / Scope Resolution Design

## Purpose

Define the deterministic contract used to establish which Engineering Scope and Process Instance govern an engineering request after repository-portable continuation has been demonstrated.

This design does not define a new Project entity. It operationalizes the already-closed Engineering Scope Identity semantics and preserves the Runtime authority boundary.

## Design Gate

**Status: CLOSED — implementation authorized.**

The design establishes the minimum resolution contract required for the next implementation and validation work.

## Governing distinction

The following are distinct:

| Concept | Meaning |
|---|---|
| Repository identity | Stable identity supplied by the Execution Environment for the active repository |
| Repository root | Current filesystem location of that repository |
| Workspace identity | Execution Environment workspace evidence; not authoritative scope identity |
| Engineering Scope Identity | Stable AESM boundary for related engineering work |
| Engineering Objective | The concrete work requested within a scope |
| Process Instance Identity | Identity of one governed engineering execution |
| Execution Context | Runtime-authoritative operational state for one Process Instance |

A repository may provide evidence for a scope without being the semantic definition of that scope. A scope may span repositories, and one scope may contain multiple Process Instances.

## Resolution contract

The authoritative ingress is:

```
Execution Environment
        |
        v
Active Repository Context
        |
        +-- repository identity
        +-- repository root
        +-- environment evidence
        +-- optional human-provided scope evidence
        |
        v
Scope Resolution
        |
        +-- UNRESOLVED
        +-- AMBIGUOUS
        +-- INVALID
        +-- CONFLICTING
        +-- RESOLVED(scope identity)
        |
        v
Process Instance Resolution
        |
        +-- existing uniquely applicable PI -> attach
        +-- no applicable PI -> explicitly authorized create
        +-- multiple applicable PIs -> explicit ambiguity unless
        |   an authoritative PI identity is supplied
        |
        v
Runtime-authoritative Process Instance + Execution Context
```

The Agent may submit evidence or a proposed resolution. It cannot establish the authoritative binding by narrative alone.

## Active Repository Context

An Active Repository Context is immutable for one Runtime session.

It contains:

- repository root;
- stable repository identity when available;
- execution-environment evidence associated with establishing that context.

The Execution Environment is responsible for establishing the context. AESM does not silently search the workspace for a repository and does not infer a repository from an arbitrary path.

A new repository context requires a new Runtime/session binding.

Changing the filesystem path used by a repository does not itself change repository identity or Engineering Scope Identity. A new session may establish a new path for the same stable repository identity. Existing Runtime state is never silently rebound to the new path.

## Candidate Process Instances

Process Instance discovery is repository-local and Runtime-mediated.

The Runtime may enumerate persisted Process Instances in the active repository's `.aesm/` boundary and evaluate their persisted Engineering Scope Identity.

A candidate is applicable only when its persisted scope identity is resolved and matches the resolved Engineering Scope Identity.

The objective is not used as an implicit identity key. Similar or identical objectives do not establish that two Process Instances are the same.

Selection rules:

1. **Exactly one applicable candidate** — resolve that Process Instance.
2. **No applicable candidate** — return `NO_APPLICABLE_PROCESS_INSTANCE`; creation requires an explicit authorized create decision.
3. **More than one applicable candidate** — return `AMBIGUOUS`; do not silently choose by creation time, filesystem order, objective similarity, or Agent preference.
4. **Explicit authoritative Process Instance identity** — attach only that identity after Runtime validation that it belongs to the active repository and its scope matches the resolved scope.
5. A terminated Process Instance is not automatically selected merely because its scope matches; lifecycle applicability must be evaluated by the Runtime's existing lifecycle semantics.

## Scope resolution outcomes

Resolution is explicit and machine-readable:

- `RESOLVED` — exactly one authoritative Engineering Scope Identity established.
- `UNRESOLVED` — available evidence is insufficient.
- `AMBIGUOUS` — multiple scope identities remain plausible.
- `CONFLICTING` — supplied evidence establishes incompatible identities.
- `INVALID` — supplied resolution is structurally or semantically invalid.

A non-`RESOLVED` outcome cannot create an implicit authoritative scope binding.

## Evidence boundary

The Agent/Execution Environment may provide:

- repository root;
- repository identity / Git remote evidence;
- workspace evidence;
- execution-environment identity;
- human-provided project or scope information;
- candidate Process Instance IDs discovered in the active repository.

These are evidence inputs only.

The Runtime:

- validates the repository context;
- evaluates candidate Process Instances;
- accepts or rejects a proposed scope resolution;
- persists the authoritative scope binding;
- selects or attaches the applicable Process Instance;
- provides the authoritative Execution Context.

The Bridge remains an adapter and does not own discovery, selection, persistence, or scope state.

## Repository isolation

Resolution must never:

- search another repository's `.aesm/` boundary;
- fall back to a workspace-level persistence store;
- select a Process Instance merely because it exists elsewhere in the workspace;
- use conversation history as authoritative identity;
- silently switch repositories during an active Runtime session.

If repository context is missing, invalid, or inconsistent, resolution fails explicitly.

## Context-change guard

An active Runtime is bound to one immutable Active Repository Context.

A repository context change therefore requires a new Runtime/session. Existing Runtime methods must not silently retarget their ProcessStore.

A new Runtime may use a different filesystem path for the same repository identity. This is an environment change, not an Engineering Scope change. Scope binding is recovered from persisted authoritative state and must remain stable unless an explicitly authorized scope-resolution operation establishes it for an unresolved Process Instance.

## Creation authorization

Scope resolution and Process Instance creation are separate decisions.

A resolved scope with no applicable Process Instance produces:

```
RESOLVED scope
      +
NO_APPLICABLE_PROCESS_INSTANCE
      |
      v
explicit create authorization required
      |
      v
Runtime.create_process(objective, scope identity)
```

The Agent cannot create merely because discovery found no candidate unless the governing interaction supplies an explicit creation authorization.

## Required validation matrix

The implementation is not considered demonstrated until the following are executable:

| Scenario | Required result |
|---|---|
| One repository, one applicable PI | Resolve and attach |
| One repository, no PI | Explicit authorized creation |
| Multiple applicable PIs | Explicit ambiguity unless authoritative PI ID resolves it |
| Unknown repository context | Explicit unresolved/invalid failure |
| Two repositories in one workspace | Each resolves only against its own repository boundary |
| Repository context changes mid-session | Existing Runtime rejects/survives without retargeting |
| Same repository identity, new repository path | New Runtime recovers same scope/PI from the new path |
| Fresh Agent in same repository | Recovers the established PI |
| Fresh Agent in another repository | Cannot recover the first repository's PI |

## Implementation boundary

The smallest implementation authorized by this design is:

1. represent stable repository identity in Active Repository Context;
2. enumerate repository-local Process Instances through ProcessStore;
3. introduce a Runtime-owned deterministic scope/process resolver;
4. distinguish candidate selection from explicit Process Instance creation;
5. expose resolution through the existing Agent–Runtime Bridge without moving authority into the Bridge;
6. add behavioral isolation and context-change tests.

No Project entity, workspace-wide index, generalized orchestration layer, or second persistence store is authorized by this design.
