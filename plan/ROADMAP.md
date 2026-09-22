# AESM Engineering Roadmap

## Purpose

This document records the long-term strategic direction of AESM engineering
work. It is not a task list and does not authorize specific implementation.

Items here represent:
- Strategic objectives that guide future Task creation and prioritization
- Architectural directions that have been discussed or implied by completed work
- Scope boundaries that should inform future planning decisions

Items in this roadmap must be formally authorized and converted into Tasks in
`plan/backlog/` or `plan/active/` before any implementation occurs.

---

## Current Strategic Boundary

The core AESM system (Runtime, bridge, Process Instance, Execution Context,
scope resolution) is implemented and verified as of the Runtime Consistency and
Continuity Hardening completion (2026-09-21).

The immediate next authorized work is the Repository-Scoped DBP Continuation
Validation (see `plan/backlog/repository-scoped-dbp-continuation-validation.md`).

---

## Strategic Objectives

### 1. Cross-Repository Scope Resolution

**Direction:** The current scope resolution is repository-local. Future work
may investigate whether and how a Process Instance may span multiple repositories
when an engineering scope requires it.

**Constraint from completed work:** A Process Instance may span multiple repositories
when its engineering scope requires it — but no implementation exists. Any
implementation requires a new design gate.

**Status:** Not authorized. Requires demonstrated need.

---

### 2. Operational Scale Validation

**Direction:** Validate the AESM operational chain at a scale beyond the current
proof-of-concept. This includes:
- Multiple concurrent Process Instances
- Engineering work involving multiple Agent sessions over weeks
- Evidence traceability over longer project timelines

**Status:** Not authorized. Depends on DBP continuation validation results.

---

### 3. Agent Discovery of Process Instances

**Direction:** The current scope-resolution mechanism requires knowing the
repository root to enumerate Process Instances. Future work may address how an
Agent discovers which Process Instance is applicable when the scope is not
immediately obvious from the repository structure.

**Constraint from completed work:** Objective-to-Process-Instance discovery is
a separate design concern from bridge, scope resolution, or process binding.
Agent-owned discovery is not authorized.

**Status:** Not authorized. Remains a separate design concern.

---

### 4. Normative Documentation Reconciliation

**Direction:** Ensure all canonical docs/ material accurately reflects the
implementation architecture established through the completed foundational work.
The normative documentation reconciliation record (implementation/NORMATIVE-DOCUMENTATION-RECONCILIATION.md)
established a baseline, but subsequent implementation may have evolved.

**Status:** Not authorized as a separate task. Should be evaluated periodically
against docs/.

---

## Explicitly Out of Scope

The following have been explicitly excluded from the AESM implementation scope
in the governing implementation plan. They remain out of scope unless separately
and explicitly authorized:

- Dedicated AESM IDE extension
- Complete AESM graphical application
- General-purpose workflow designer
- Multi-agent orchestration
- Distributed execution
- Enterprise infrastructure
- New programming language or DSL
- Automatic enforcement of every AESM rule
- Normative MCP requirement
- VS Code-specific architecture
- Generalized Agent orchestration
- Broad Runtime refactoring
- Speculative EPM/PEM/AESM expansion

---

## Conventions

Roadmap items are not Tasks. They do not have status, acceptance criteria, or
Subtasks. When a roadmap item is authorized for implementation:

1. Create a Task file in `plan/backlog/`.
2. Reference the roadmap item as context.
3. Authorize the Task through explicit human instruction.
4. Move to `plan/active/` when execution begins.
