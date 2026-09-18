# Engineering Scope Identity Semantics

**Status:** Semantic clarification complete
**Decision gate:** Engineering Scope Identity Semantics
**Repository:** tuanna2703/AI-Assisted-Engineering-System-Model
**Predecessor:** execution/PROJECT-SCOPE-SEMANTICS-INVESTIGATION.md

## 1. Decision Question

This work defines the semantic meaning of an Engineering Scope Identity and determines whether AESM requires a first-class Project entity.

The work is independent of implementation technology. Repository paths, workspace identifiers, IDE state, Git metadata, and persistence locations are possible evidence or implementation mechanisms, not semantic definitions.

## 2. Existing AESM Baseline

The current AESM model establishes:
- Engineering Objective gives a Process Instance its intended purpose.
- Process Instance is the persistent identity of one concrete engineering execution.
- Execution Context is authoritative operational state for that Process Instance.
- EPM defines engineering meaning and validity.
- PEM defines execution semantics.
- Runtime owns authoritative Process Instance discovery and operational control.
- Execution Environment provides interaction and tooling capabilities.
- Agent participation does not transfer Runtime authority to the Agent.

The current model does not define an independent identity for the engineering scope in which an objective is performed.

Therefore:
```text
Engineering Objective
    !=
Engineering Scope Identity
    !=
Process Instance Identity
```

These dimensions must remain distinct.

## 3. Engineering Scope Definition

Engineering Scope is the stable engineering boundary within which a set of related engineering objectives, artifacts, requirements, constraints, decisions, and execution activities are understood as belonging to the same engineering body of work.

Engineering Scope Identity is the persistent, distinguishable identity assigned to that engineering boundary.

The definition is independent of a chat conversation, Agent, Agent context window, IDE, CLI session, Runtime process, filesystem path, repository URL, or workspace configuration.

An environment can provide evidence about scope, but environment state does not become scope identity merely because it is observable.

## 4. Required Identity Properties

A valid Engineering Scope Identity must be stable, distinguishable, persistent, recoverable, environment-independent, explicit, and traceable.

Changing an IDE, Runtime process, Agent, workspace path, or local checkout location must not inherently create a new scope.

Different engineering scopes must remain distinguishable even when their objectives are identical or similar.

## 5. Scope Is Not Objective

Engineering Objective answers: What engineering work is intended?

Engineering Scope answers: Which engineering body does that work belong to?

Process Instance Identity answers: Which concrete execution of that engineering work exists?

The relationship is:
```text
Engineering Scope Identity
        |
        +-- provides engineering boundary for
                    |
                    v
           Engineering Objective
                    |
                    v
             Process Instance
                    |
                    v
           Execution Context
```

Multiple Process Instances may have similar objectives within one scope.

## 6. Scope-to-Process Instance Cardinality

The semantic model permits one Engineering Scope to contain multiple Process Instances.

Therefore scope identity must not be used as a Process Instance identifier.

Multiple Process Instances may exist concurrently within one scope when they represent distinct engineering executions.

## 7. Process Instance Scope Binding

A Process Instance may be bound to an Engineering Scope Identity.

The binding is part of the authoritative identity/context relationship and must be recoverable for continuation.

The binding should be established at Process Instance creation or explicit scope-assignment time and must not be silently replaced merely because the Agent changes environment.

A material scope change is not equivalent to changing Process State or Engineering Objective.

## 8. Multi-Repository and Multi-Workspace Semantics

A repository is not defined as an Engineering Scope. A workspace is not defined as an Engineering Scope.

One scope may contain multiple repositories.

One scope may be represented through multiple workspaces.

One repository may contain multiple engineering scopes.

One Process Instance may reference work across multiple repositories when its engineering objective legitimately spans them.

Repositories and workspaces are therefore scope evidence or artifact locations, not the universal definition of scope.

## 9. Scope Lifecycle

Engineering Scope Identity is not a Process State and is not a Process Instance lifecycle.

The scope concept does not introduce another execution state machine.

```text
Engineering Scope lifecycle
    !=
Process Instance lifecycle
    !=
Process State
    !=
Engineering completion
```

Future implementation may need explicit scope metadata changes, but those changes must not silently rewrite historical Process Instance bindings.

## 10. Environmental Evidence

Potential scope evidence includes repository identity, Git remote, repository metadata, workspace metadata, current working directory, project configuration, known artifact locations, explicit human-provided scope information, and previously persisted authoritative scope information.

None of these is automatically authoritative.

The intended path is:
```text
Execution Environment
        v
Environmental / Participant Evidence
        v
Runtime recognition and resolution
        v
Engineering Scope Identity
        v
Process Instance binding
```

The Agent may contribute evidence or a proposed scope, but cannot independently establish an authoritative binding.

## 11. Scope Resolution Authority

The Runtime remains the authority for resolving an existing Process Instance and applying authoritative binding state.

The Execution Environment provides capabilities and evidence.

The Agent may report observed scope evidence, propose a scope, request creation or continuation, and identify explicit human-provided scope information.

The Agent may not declare a Process Instance authoritative by itself, silently select between ambiguous scopes, rewrite an existing Process Instance scope, or treat repository/workspace heuristics as AESM semantics.

## 12. Ambiguity Semantics

If no sufficient scope evidence exists, the system must not fabricate a scope.

If one scope is sufficiently supported and unambiguous under the applicable recognition conditions, the Runtime may resolve it.

If multiple scopes are plausible, ambiguity must remain explicit and additional evidence, explicit human clarification, or another applicable resolution rule is required.

If an existing Process Instance is known but its scope is uncertain, the Process Instance may be recovered by identity while the scope uncertainty remains explicit.

## 13. Scope Identity and Process Instance Discovery

The semantic sequence is:
```text
Request
   v
Establish / resolve Engineering Scope Identity
   v
Resolve applicable Process Instance(s)
   v
Recover authoritative Execution Context
   v
Evaluate executable situation
   v
Continue or create execution as permitted
```

This does not require a specific discover API.

It establishes that Process Instance discovery must have enough information to distinguish engineering scope before selecting among potentially competing executions.

Known Process Instance ID remains a valid direct discovery mechanism for continuation.

## 14. Is a First-Class Project Entity Required?

**Decision: No, not at this semantic gate.**

The investigation establishes that AESM needs the semantic concept of Engineering Scope Identity, but it does not establish that a named Project entity is necessary.

A first-class Project entity would add additional entity and lifecycle/ownership semantics that are not required merely to establish the missing identity dimension.

The semantic requirement can be expressed as Engineering Scope Identity without committing AESM to a richer Project object.

Such an object may be reconsidered later if implementation or further semantic analysis demonstrates a need for independently managed scope metadata. It must not be introduced preemptively.

## 15. Why Repository Identity Is Insufficient

Repository identity is useful implementation-level evidence but fails as the universal semantic definition because one scope may span multiple repositories, one repository may contain multiple scopes, repository location/hosting can change, and not all engineering scopes are necessarily repository-backed.

Therefore:
```text
Repository Identity
    -> possible scope evidence
    !=
Engineering Scope Identity
```

## 16. Why Workspace Identity Is Insufficient

Workspace identity is useful evidence but is not a stable semantic boundary because multiple workspaces may represent one scope, one workspace may expose multiple scopes, workspace configuration can change, and different environments may not have equivalent workspace concepts.

Therefore:
```text
Workspace Identity
    -> possible scope evidence
    !=
Engineering Scope Identity
```

## 17. Scope Binding Invariants

1. Scope Identity is not Process Instance Identity.
2. Scope Identity is not Engineering Objective.
3. Scope Identity is not Execution Environment Identity.
4. Repository Identity is not Scope Identity by default.
5. Workspace Identity is not Scope Identity by default.
6. One scope may contain multiple Process Instances.
7. A Process Instance may span multiple repositories when its engineering scope requires it.
8. Agent output does not establish authoritative scope binding.
9. Environmental evidence does not become authoritative merely because it is observed.
10. Ambiguous scope resolution must remain explicit.
11. Established Process Instance scope binding must remain recoverable.
12. Changing Agent, Runtime, IDE, workspace, or repository path does not by itself change scope identity.

## 18. DBP Reconciliation

The DBP empirical execution exposed a practical gap: a real engineering request could be executed, but the evidence did not establish an authoritative project/process binding.

Under the clarified semantics, the DBP request requires a scope-resolution step before selecting or creating the governing Process Instance:
```text
DBP engineering request
        v
DBP Engineering Scope Identity
        v
existing Process Instance resolution
        OR
new Process Instance creation
```

The DBP repository may provide strong evidence for resolving the scope, but it is not itself the semantic definition of that scope.

## 19. Consequences for Future Design

The next design work must define how Engineering Scope Identity is represented and resolved operationally.

It must address scope identity representation, authoritative scope metadata, scope registration/creation, deterministic resolution, matching evidence, ambiguity handling, Process Instance selection, new Process Instance creation, continuity and persistence, scope binding change rules, environment-specific evidence adapters, and multi-scope isolation.

Implementation should remain blocked until that design is complete.

## 20. Gate Decision

**Engineering Scope Identity Semantics — COMPLETE**

The semantic gate establishes:
- AESM requires an explicit Engineering Scope Identity concept.
- Engineering Scope Identity is distinct from Engineering Objective and Process Instance Identity.
- Repository and workspace are evidence sources, not universal scope identities.
- One scope may contain multiple Process Instances.
- A Process Instance may span multiple repositories when semantically justified.
- Runtime retains authoritative resolution and binding authority.
- Ambiguous resolution must remain explicit.
- A first-class Project entity is not yet required.

### Next authorized work

**Project / Scope Resolution Design**

The next work should define the deterministic operational mechanism by which request plus available scope evidence is resolved to Engineering Scope Identity and then to an existing Process Instance or a new Process Instance while preserving Runtime authority and explicit ambiguity handling.