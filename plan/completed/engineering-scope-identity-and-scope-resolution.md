# Engineering Scope Identity and Project / Scope Resolution

## Identity

Task ID:
engineering-scope-identity-and-scope-resolution

Status:
complete

Completed:
2026-09-21 (per IMPLEMENTATION_PLAN.md verification record dated 2026-09-21)

Source:
IMPLEMENTATION_PLAN.md — "Project Identity and Process Binding" and
"Project / Scope Resolution" sections

Concern tags:
scope-identity, scope-resolution, process-instance-binding, repository-isolation,
multi-project

---

## Objective

Define Engineering Scope Identity as a distinct AESM concept, design and implement
deterministic Process Instance scope resolution, and validate through an executable
test suite covering unique resolution, ambiguity, multi-repository isolation, and
active-context change behavior.

---

## Context

The DBP empirical execution identified that the established mechanism did not
address how a real Agent determines which engineering project/scope it is
operating within or which Process Instance should govern that work. This task
addressed that architectural gap through semantic clarification, design, implementation,
and verified testing.

---

## Governing Constraints

The following constraints were established during this task and remain in effect.

---

## Dependencies

- aesm-implementation-foundations
- dbp-empirical-execution (gap identification)

---

## Decisions Still in Effect

1. **Engineering Scope Identity is a distinct AESM concept.** It is distinct from:
   Engineering Objective, Process Instance Identity, Execution Context,
   Execution Environment, repository identity, and workspace identity.

2. **A scope is a stable engineering boundary** that contextualizes related
   engineering objectives, artifacts, requirements, constraints, decisions, and
   execution activities.

3. **The decision does not establish Project = repository or Project = workspace.**
   Repository identity is scope evidence, not universal scope identity.
   Workspace identity is scope evidence, not universal scope identity.

4. **A first-class Project entity is not required.** It may be reconsidered later
   only if implementation/design evidence establishes a need for independently
   managed project metadata or lifecycle.

5. **Scope identity invariants (all active constraints):**
   - Scope Identity is not Process Instance Identity.
   - Scope Identity is not Engineering Objective.
   - One scope may contain multiple Process Instances.
   - A Process Instance may span multiple repositories when its engineering scope requires it.
   - Agent output does not establish authoritative scope binding.
   - Environmental evidence does not become authoritative merely by observation.
   - Ambiguous scope resolution must remain explicit.
   - Established Process Instance scope binding must remain recoverable.
   - Changing Agent, Runtime, IDE, workspace, or repository path does not by itself change scope identity.

6. **Scope resolution is Runtime-owned and deterministic.** The Agent must not
   own discovery or silently create a Process Instance during resolution.

7. **No generalized Project entity.** No workspace-wide Process Instance index,
   second persistence store, or Agent-owned discovery mechanism is authorized.

8. **Creation remains an explicit Runtime operation.** Resolution may identify
   that creation is required, but does not silently create.

9. **Repository isolation is enforced.** Cross-scope Process Instance access is rejected.

10. **Repository path and repository identity are distinct.** A relocated
    repository path does not change the repository identity or scope.

---

## Work Units

### Engineering Scope Identity Semantics

Status: complete

Defined Engineering Scope Identity as a distinct AESM concept with all invariants.
Design record: implementation/PROJECT-SCOPE-RESOLUTION-DESIGN.md.
Semantic decision record: implementation/ENGINEERING-SCOPE-IDENTITY-SEMANTICS.md
(referenced by IMPLEMENTATION_PLAN.md; file may have been superseded by
PROJECT-SCOPE-RESOLUTION-DESIGN.md — see implementation/ for current records).

### Project / Scope Resolution Design and Implementation

Status: complete

Designed and implemented:
- Added stable repository identity to ActiveRepositoryContext.
- Added repository-local Process Instance enumeration to ProcessStore.
- Added Runtime-owned deterministic Process Instance resolution.
- Added Runtime resolution-and-attach behavior.
- Exposed resolution through existing Agent–Runtime Bridge.
- Targeted tests: unique resolution, no candidate, ambiguity, explicit PI selection,
  cross-scope rejection, repository isolation, repository identity/path distinction,
  Bridge delegation.

---

## Acceptance Criteria

All satisfied. Verification gate CLOSED.

---

## Verification Requirements

Satisfied with executable test results:

**Branch:** `verify/executable-project-scope-resolution`
**HEAD SHA:** `67f68ccceba20e7833338ef673ba0aa37a5010ae`

| Suite | Command | Result |
|---|---|---|
| Scope resolution + binding | `pytest tests/project_identity/` | 25/25 PASS |
| Multi-project + repository isolation | `pytest tests/multi_project/ tests/repository_isolation/` | 24/24 PASS |
| Full regression | `pytest tests/` | 204/204 PASS |

---

## Evidence Record

- `implementation/EXECUTABLE-PROJECT-SCOPE-RESOLUTION-VERIFICATION.md` — complete verification record
- `implementation/PROJECT-SCOPE-RESOLUTION-DESIGN.md` — design record
- `implementation/MULTI-PROJECT-EMPIRICAL-VALIDATION.md` — multi-project validation
- `implementation/PROJECT-IDENTITY-AND-PROCESS-BINDING-VALIDATION.md` — binding validation
- Test suites: `tests/project_identity/`, `tests/multi_project/`, `tests/repository_isolation/`
