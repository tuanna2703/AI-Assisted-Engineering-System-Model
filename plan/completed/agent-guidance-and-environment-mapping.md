# Agent Guidance and Environment Mechanism Mapping

## Identity

Task ID:
agent-guidance-and-environment-mapping

Status:
complete

Completed:
2026-09-19 (per IMPLEMENTATION_PLAN.md history; exact dates approximate)

Source:
IMPLEMENTATION_PLAN.md — "Agent Guidance and Environment Work" section

Concern tags:
agent-guidance, bridge, environment-mapping, runtime-api

---

## Objective

Establish the Agent Guidance Interface, Agent–Runtime boundary, Runtime API
surface, minimal Agent–Runtime bridge, and Environment Mechanism Mapping —
defining the complete operational chain that governs Agent participation in
AESM-governed engineering work.

---

## Context

After the AESM Implementation Foundations established the Runtime core, this
task determined how an AI Agent interacts with the Runtime through the existing
Execution Environment without requiring AESM-specific IDE extensions or
normative MCP.

---

## Governing Constraints

The following constraints were established and remain in effect.

---

## Dependencies

- aesm-implementation-foundations (Runtime core must exist)
- docs/ canonical set (Agent participation, Runtime, Execution Environment semantics)

---

## Decisions Still in Effect

1. **Agent Guidance Interface is closed.** The semantic contract is established
   and must not be reopened merely for the subsequent empirical experiment or
   for convenience. Subsequent work uses its established contract.

2. **Thin bridge.** The bridge is implemented outside runtime/ and delegates
   authority to the existing Runtime. It is not a new persistence layer,
   orchestration engine, lifecycle model, or transport requirement.

3. **Four adapter surfaces.** The concrete bridge API surface is:
   - `create_process`
   - `attach`
   - `get_context`
   - `dispatch`
   No additional bridge surface is authorized by this work unit.

4. **Objective-to-Process-Instance discovery is a separate design concern.**
   It is not silently generalized into the bridge.

5. **Minimum mechanism combination.** The required minimum is:
   - Persistent Agent guidance
   - Human task request
   - Agent-accessible Runtime/bridge mechanism
   - Persisted Process Instance / Execution Context
   - Runtime-mediated authoritative operations
   No dedicated VS Code extension, MCP server, second Process Instance store,
   or generalized Agent orchestrator is required by the evidence.

6. **Environment Mechanism Mapping findings superseded only where subsequently
   validated empirically.** The semantic contract itself is unchanged.

7. **No VS Code-specific architecture.** VS Code or another IDE may be an
   Execution Environment, not the AESM architecture.

8. **No normative MCP requirement.** MCP is not required for AESM participation.

---

## Work Units

### Agent Guidance Interface

Status: complete

Established: AESM guidance content is available through repository documentation;
authoritative Execution Context is exposed by the Runtime bridge; conversation
history must not be treated as authoritative state; governed execution capabilities
are executable through the established bridge; lifecycle observation is executable.

### Agent–Runtime Boundary Investigation

Status: complete

Established the responsibility boundary between Agent, Runtime, and Execution
Environment. Justified a thin Agent–Runtime bridge rather than Runtime redesign
or a normative transport.

### Runtime API Inspection

Status: complete

Determined the concrete adapter surface: create_process, attach, get_context,
dispatch. Established that objective-to-Process-Instance discovery is a separate
concern not silently generalized into the bridge.

### Minimal Agent–Runtime Bridge

Status: complete

Implemented bridge/ outside runtime/. Provides Process Instance access,
authoritative Context access, Runtime dispatch, and authoritative result/state
return. Is not a new persistence layer, orchestration engine, lifecycle model,
or transport requirement.

### Environment Mechanism Mapping

Status: complete

Established and validated the minimum mechanism combination through subsequent
mechanism-validation work. Found no requirement for a dedicated IDE extension,
MCP server, second PI store, or generalized Agent orchestrator.

---

## Acceptance Criteria

All satisfied:
- Agent Guidance Interface semantic contract established and closed.
- Agent–Runtime boundary documented.
- Runtime API surface determined (four adapter surfaces).
- bridge/ implemented and validated.
- Minimum mechanism combination established.

---

## Evidence Record

- `docs/Agent-Execution-Integration.md` — Agent Guidance Interface, boundary
  investigation, Runtime API inspection, bridge implementation, and environment
  mechanism mapping evidence.
- `bridge/` — minimal bridge implementation.
