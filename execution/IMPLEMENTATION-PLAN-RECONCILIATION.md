# Implementation Plan Reconciliation — Agent–Runtime Bridge

## Status

Reconciliation review complete. The canonical implementation plan currently contains stale bridge-work status and has not yet been rewritten because its complete-file replacement is operationally unsafe through the available repository write path.

This record therefore establishes the intended reconciliation without falsely claiming that `IMPLEMENTATION_PLAN.md` itself has been updated.

## Evidence reconciled

- Agent–Runtime Execution Bridge Inspection: `execution/AGENT-RUNTIME-EXECUTION-BRIDGE-INSPECTION.md`, commit `6549b02df5fecec2e8e6bb94967bfe0b93441505`.
- Environment Mechanism Mapping: `execution/ENVIRONMENT-MECHANISM-MAPPING.md`, commit `d8305593ac96908f43ee863ef5e3a01a3f64761d`.
- Bridge Boundary Decision and Implementation Design: `execution/BRIDGE-BOUNDARY-DECISION-AND-IMPLEMENTATION-DESIGN.md`, commit `22cd6ed6d91cc9c70f2da0bb6c034bff8312de3`.

## Required plan-state reconciliation

The following existing plan entries should be treated as complete based on the recorded evidence:

### Agent Guidance Interface

Mark the existing Agent Guidance Interface work complete. The Environment Mechanism Mapping establishes the available persistent guidance, task/process context, skills, MCP/tool capability, filesystem/CLI execution, and the boundary between guidance and Runtime authority.

### Agent–Runtime Execution Bridge Inspection

Replace the current `Status: Not started. Next bounded work unit.` state with completed status. Mark its inspection targets complete and reference the inspection artifact. The inspection concluded that a thin Agent–Runtime bridge is justified and that normal Agent engineering execution currently lacks an operational bridge.

### Environment Mechanism Mapping

Mark this work complete and reference `execution/ENVIRONMENT-MECHANISM-MAPPING.md`.

### Bridge Boundary Decision and Implementation Design

Add a completed bounded work unit for the design record. The decision is that a thin environment-facing bridge is justified. The first implementation mechanism is the existing Python/CLI execution capability; MCP remains an alternative, not a normative choice.

## Implementation authorization boundary

The bridge design does **not** authorize implementation by itself. Before implementation begins, the repository must have an explicit authorization state reconciled with the canonical plan.

Once that authorization is recorded, the permitted implementation scope is limited to:

- a thin Agent-facing adapter;
- Process Instance create/discovery/attach;
- authoritative Context retrieval and presentation;
- dispatch of already-supported Runtime recording operations;
- return of authoritative Runtime results/state;
- explicit failure/ambiguity handling.

The following remain unauthorized by this reconciliation:

- Runtime semantic/lifecycle changes;
- a second authoritative state store;
- generalized orchestration;
- an MCP server as a prerequisite;
- a VS Code extension or VS Code-specific API;
- multi-agent coordination.

## Current decision

**Do not begin bridge implementation yet solely on the basis of this record.** The controlled `IMPLEMENTATION_PLAN.md` still needs its actual status text reconciled, or an explicit implementation authorization record must supersede the stale plan state through the repository's normal governance mechanism.

This preserves the evidence → reconciliation → authorization boundary and avoids treating an auxiliary record as though it silently replaced the controlled implementation plan.