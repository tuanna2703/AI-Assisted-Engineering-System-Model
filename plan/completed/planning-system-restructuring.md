# Planning System Restructuring

## Identity

Task ID:
planning-system-restructuring

Status:
complete

Created:
2026-09-22

Source:
Human instruction — AESM Planning System Restructuring prompt (2026-09-22).
Authorized to replace monolithic IMPLEMENTATION_PLAN.md with structured plan/ system.

---

## Objective

Establish a structured, deterministic, recoverable planning system under `plan/`
that replaces the current monolithic `IMPLEMENTATION_PLAN.md`, enabling a fresh
AI Agent to identify current work and next safe action without requiring historical
conversation context.

---

## Context

The repository's planning surface is a single 707-line `IMPLEMENTATION_PLAN.md`
that mixes completed historical work, active work, future direction, governing
constraints, and verification evidence. A fresh Agent must scan the entire file
to determine what is current, what is done, and what is next.

This task establishes `plan/` as an agent-navigable planning system with clear
navigation protocol, authority boundaries, and migration of existing plan content.

This task operates at the planning governance layer. It does not execute AESM
engineering work, does not create or attach a new AESM Process Instance, and
does not alter AESM lifecycle semantics or Runtime authority.

---

## Governing Constraints

1. Do not execute the Repository-Scoped DBP Continuation Validation experiment.
2. Do not perform unrelated AESM implementation work.
3. Do not introduce a second execution-state authority.
4. Do not change existing AESM lifecycle semantics.
5. Do not modify docs/, runtime/, bridge/, tests/, or .aesm/ except as required
   for verification commands (read-only).
6. Do not create or attach a new AESM Process Instance for this planning task.
7. Preserve the existing repository conventions documented in AGENTS.md and
   IMPLEMENTATION_BASELINE.md.
8. Completed tasks created during migration must not duplicate canonical docs/
   content or production code.

---

## Dependencies

- IMPLEMENTATION_PLAN.md (source for migration; must exist until verification passes)
- AGENTS.md (governs repository conventions that must be preserved)
- IMPLEMENTATION_BASELINE.md (governs repository boundary that must be preserved)

---

## Decisions Still in Effect

The following decisions from prior completed work remain active constraints:

1. **Runtime authority** — Runtime remains authoritative for AESM persisted state.
   Planning records are not Runtime evidence.

2. **docs/ is canonical** — AESM semantic definitions belong in docs/, not in
   planning files, implementation records, or task files.

3. **implementation/ boundary** — implementation/ contains only durable
   engineering evidence. Not plans, not state, not transcripts.

4. **No competing planning authority** — exactly one planning system must be
   active at any time. During migration, IMPLEMENTATION_PLAN.md carries an
   explicit supersession notice.

5. **No generalized Project entity** — no workspace-wide Process Instance index,
   second persistence store, or Agent-owned discovery mechanism is authorized.

6. **Schema version 1 explicit** — missing version defaults to v1; unsupported
   versions are rejected. (Runtime implementation detail, preserved as context.)

7. **Bridge is thin** — bridge/ does not own Runtime authority and is not a
   new persistence layer.

8. **Remote Git round trip** — not an authorized closure criterion for the
   Runtime Consistency and Continuity Hardening work; remains explicitly unclaimed.

---

## Work Units

---

### Repository and Planning Inspection

Status: complete

Objective:
Inspect all existing planning material, repository conventions, and Git state
before making any modifications.

Subtasks:
- [x] Inspect repository root — evidence: list_dir output recorded in session
- [x] Inspect docs/ directory — evidence: 13 files including canonical docs set
- [x] Inspect implementation/ directory — evidence: 11 files, durable evidence records
- [x] Read AGENTS.md — evidence: rules and working sequence confirmed
- [x] Read README.md — evidence: core model confirmed
- [x] Read IMPLEMENTATION_BASELINE.md — evidence: boundary confirmed
- [x] Read IMPLEMENTATION_PLAN.md in full — evidence: 707 lines classified
- [x] Read implementation/README.md — evidence: purpose and boundary confirmed
- [x] Read docs/README.md — evidence: canonical structure confirmed
- [x] Inspect .aesm/ — evidence: one PI directory f713278b-cb74-4a49-a6a1-b6713f058b56
- [x] Check Git state — evidence: branch verify/executable-project-scope-resolution, HEAD 04ae17b, clean working tree

Completion condition:
The repository's existing planning information and relevant conventions are
understood sufficiently to design the new structure without guessing.

Status after completion: SATISFIED. Content classification complete. See
implementation_plan.md artifact for the full classification of IMPLEMENTATION_PLAN.md.

---

### Planning Directory Establishment

Status: complete

Objective:
Create the plan/ directory skeleton to establish the structural boundary before
populating definitions or migrated content.

Subtasks:
- [x] Create plan/definitions/ — evidence: mkdir executed, exit 0
- [x] Create plan/active/ — evidence: mkdir executed, exit 0
- [x] Create plan/backlog/ — evidence: mkdir executed, exit 0
- [x] Create plan/completed/ — evidence: mkdir executed, exit 0
- [x] Create plan/completed/INDEX.md skeleton — evidence: file created

Completion condition:
The complete planning directory structure exists and its intended responsibilities
are clear.

Status after completion: SATISFIED. All required directories and the INDEX.md
skeleton exist.

---

### Planning Information Model

Status: complete

Objective:
Define the planning hierarchy (Task → Work Unit → Subtask) and the status and
completion models that govern them.

Subtasks:
- [x] Create plan/definitions/TASK.md — evidence: file created
- [x] Create plan/definitions/WORK-UNIT.md — evidence: file created
- [x] Create plan/definitions/SUBTASK.md — evidence: file created
- [x] Create plan/definitions/STATUS.md — evidence: file created
- [x] Create plan/definitions/COMPLETION.md — evidence: file created

Completion condition:
The definitions are sufficiently precise that two Agents should interpret Task,
Work Unit, Subtask, status, and completion consistently.

Status after completion: SATISFIED. Five definition files establish the hierarchy,
status model, and four-level completion distinction.

---

### Planning Governance and Agent Navigation

Status: complete

Objective:
Create plan/README.md as the complete Agent entry point and navigation document.

Subtasks:
- [x] Design complete README structure before writing — evidence: structure determined in session
- [x] Write plan/README.md with all required sections — evidence: file created

Required sections satisfied:
- [x] Planning-system purpose
- [x] Agent entry protocol
- [x] Planning/AESM boundary table
- [x] CURRENT.md authority definition
- [x] Work-unit transition protocol (9 steps exact)
- [x] Recovery protocol (11 steps)
- [x] Backlog promotion rule
- [x] Historical navigation guide
- [x] Directory reference

Completion condition:
A fresh Agent can understand the planning model and navigation protocol by reading
README without relying on construction history or prior conversation.

Status after completion: SATISFIED. README is self-contained and complete.

---

### Planning Principles

Status: complete

Objective:
Create plan/PRINCIPLES.md establishing the governance relationship between plan/
and AESM, with explicit Runtime authority boundary.

Subtasks:
- [x] Write plan/PRINCIPLES.md with 10 governing principles — evidence: file created

Principles covered:
- [x] Runtime authority
- [x] Planning records definition
- [x] Planning versus execution
- [x] No implicit scope
- [x] No premature generalization
- [x] Evidence before engineering completion
- [x] One planning authority
- [x] Semantic names not numeric labels
- [x] Task file is source of truth
- [x] Completed tasks are permanent records

Completion condition:
The governance relationship between plan/ and AESM is explicit and contains no
competing execution authority.

Status after completion: SATISFIED. PRINCIPLES.md establishes all required
governance relationships.

---

### Active Planning Task Establishment

Status: complete

Objective:
Create this living task file as the authoritative record for the planning-system
restructuring effort and keep it updated as execution progresses.

Subtasks:
- [x] Create plan/active/planning-system-restructuring.md — evidence: this file
- [x] Update status after each work unit completion — evidence: this file updated continuously

Completion condition:
The restructuring task exists as a living task record whose state reflects actual execution.

Status after completion: SATISFIED. This file is updated after every work unit.

---

### Historical Plan Decomposition

Status: complete

Objective:
Analyze IMPLEMENTATION_PLAN.md and classify all content into the correct
destination categories without blind copying.

Subtasks:
- [x] Classify all content using the four-level precedence — evidence: implementation_plan.md artifact records full classification
- [x] Identify all completed engineering efforts — evidence: 7 completed task files created
- [x] Identify all future work items for backlog/ — evidence: repository-scoped-dbp-continuation-validation.md
- [x] Identify all strategic direction items for ROADMAP.md — evidence: ROADMAP.md created
- [x] Information deliberately retired: none — all substantive content migrated to plan/

Completion condition:
Every substantive part of the existing implementation plan has a deliberate
destination or an explicitly documented reason for retirement.

Status after completion: SATISFIED. All content classified and migrated.

---

### Planning Migration

Status: complete

Objective:
Migrate classified content into plan/active/, plan/backlog/, and plan/completed/
at the correct granularity.

Subtasks:
- [x] Create completed task file: aesm-implementation-foundations.md — evidence: file created
- [x] Create completed task file: agent-guidance-and-environment-mapping.md — evidence: file created
- [x] Create completed task file: agent-boundary-mechanism-validation.md — evidence: file created
- [x] Create completed task file: dbp-empirical-execution.md — evidence: file created
- [x] Create completed task file: engineering-scope-identity-and-scope-resolution.md — evidence: file created
- [x] Create completed task file: repository-portable-continuation-validation.md — evidence: file created
- [x] Create completed task file: runtime-consistency-and-continuity-hardening.md — evidence: file created
- [x] Create backlog task file: repository-scoped-dbp-continuation-validation.md — evidence: file created
- [x] Create plan/ROADMAP.md with strategic direction — evidence: file created
- [x] Update plan/completed/INDEX.md with all completed tasks — evidence: INDEX.md populated with 7 tasks and decisions quick-reference
- [x] Verify each completed task contains applicable sections — evidence: all 7 task files contain Identity, Objective, Context, Decisions Still in Effect, Work Units, Evidence Record

Completion condition:
The new planning structure contains the information required to understand
current work, future work, historical work, continuing decisions, and
verification history without relying on the old monolithic plan.

Status after completion: SATISFIED. All content migrated; index populated.

---

### Legacy Plan Transition

Status: complete

Objective:
Update IMPLEMENTATION_PLAN.md with an explicit supersession notice so that
exactly one planning authority exists.

Subtasks:
- [x] Add SUPERSEDED notice to IMPLEMENTATION_PLAN.md header — evidence: IMPLEMENTATION_PLAN.md lines 1-21
- [x] Update AGENTS.md to reference plan/ as planning surface — evidence: AGENTS.md line 64
- [x] Update IMPLEMENTATION_BASELINE.md to reference plan/ — evidence: IMPLEMENTATION_BASELINE.md lines 14-15

Completion condition:
There is one clearly authoritative planning system.

Status after completion: SATISFIED. IMPLEMENTATION_PLAN.md carries explicit SUPERSEDED notice;
AGENTS.md and IMPLEMENTATION_BASELINE.md updated to reference plan/.

---

### Planning-System Verification

Status: complete

Objective:
Verify the resulting system as though genuinely fresh, using only what is
readable from plan/ without construction memory.

Subtasks:
- [x] Re-read plan/README.md fresh — evidence: read in verification step; all sections readable and self-contained
- [x] Re-read plan/CURRENT.md fresh — evidence: read in verification step
- [x] Stale CURRENT.md defect identified (pointed to Historical Plan Decomposition instead of Planning-System Verification) — evidence: defect documented in task file
- [x] Task file updated to reflect actual completed state — evidence: this file
- [x] CURRENT.md repaired to Planning-System Verification — evidence: CURRENT.md updated
- [x] Answer all 10 navigation questions from plan/ alone — evidence: all 10 questions answered in session; all discoverable from plan/ without construction knowledge
- [x] Verify recovery scenario — evidence: stale CURRENT.md correctly recovered from task file authority; repair protocol demonstrated
- [x] Verify consistency checklist:
      - [x] Exactly one active task in plan/active/ — PASS
      - [x] CURRENT.md points to existing active task file — PASS
      - [x] Current work unit exists in task file — PASS
      - [x] Task file state agrees with work-unit state — PASS (after repair)
      - [x] No competing planning authority — PASS (IMPLEMENTATION_PLAN.md carries SUPERSEDED notice)
      - [x] Semantic names used throughout — PASS
      - [x] All completed tasks indexed in INDEX.md — PASS (7 tasks)
      - [x] Continuing decisions discoverable from completed task files — PASS
      - [x] Planning records not represented as AESM evidence — PASS
- [x] Regression suite: 204/204 PASS — evidence: .venv/bin/pytest tests/ -q, exit code 0
- [x] No production code modified by this task — evidence: git diff --name-only HEAD shows only AGENTS.md, IMPLEMENTATION_BASELINE.md, IMPLEMENTATION_PLAN.md (all documentation)

Completion condition:
A genuinely fresh Agent can discover and reconstruct current planning state
without relying on prior conversation or construction knowledge.

Status after completion: SATISFIED. All 10 navigation questions answerable from plan/;
recovery scenario demonstrated; consistency checklist passes; regression suite PASS.

---

## Acceptance Criteria

1. `plan/` directory exists with all required files. — [x] PASS
2. A fresh Agent following `README → CURRENT → Task file` can identify the next
   executable Subtask without requiring conversation history. — [x] PASS (verified)
3. Exactly one active planning authority exists; IMPLEMENTATION_PLAN.md carries
   a supersession notice. — [x] PASS
4. All substantive IMPLEMENTATION_PLAN.md content has a deliberate destination. — [x] PASS
5. Completed tasks are indexed in plan/completed/INDEX.md. — [x] PASS (7 tasks)
6. Continuing decisions are discoverable from completed task files. — [x] PASS
7. Planning records are not represented as AESM evidence. — [x] PASS (PRINCIPLES.md, COMPLETION.md)
8. Repository conventions from AGENTS.md and IMPLEMENTATION_BASELINE.md are preserved. — [x] PASS

---

## Verification Requirements

1. Re-read plan/README.md and plan/CURRENT.md without construction context and
   answer all 10 navigation questions explicitly. — [x] DONE
2. Verify CURRENT.md points to an existing active task. — [x] DONE
3. Verify the current work unit in CURRENT.md matches the Task file state. — [x] DONE
4. Verify plan/completed/INDEX.md lists all completed tasks. — [x] DONE (7 tasks listed)
5. Verify exactly one active task exists in plan/active/. — [x] DONE
6. Verify no production code or AESM semantics were modified (git diff). — [x] DONE
   Only AGENTS.md, IMPLEMENTATION_BASELINE.md, IMPLEMENTATION_PLAN.md modified
   (documentation only, not production code).

---

## Completion Record

Completed: 2026-09-22

Evidence:
- plan/ directory: 19 files across 5 subdirectories
- 204/204 regression tests PASS (.venv/bin/pytest tests/ -q, exit code 0)
- Git branch: verify/executable-project-scope-resolution
- HEAD: 04ae17b (unchanged; plan/ is untracked, not yet committed)
- Working tree: modified AGENTS.md, IMPLEMENTATION_BASELINE.md, IMPLEMENTATION_PLAN.md
  (documentation only); plan/ is new untracked directory
- No production code changes

Verification result:
- All 10 navigation questions answerable from plan/ without construction knowledge
- Recovery scenario demonstrated: stale CURRENT.md corrected from task file authority
- Consistency checklist: all items PASS
- One active planning authority (plan/); IMPLEMENTATION_PLAN.md marked SUPERSEDED
