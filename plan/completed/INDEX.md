# Completed Task Index

This index lists all Tasks in `plan/completed/`. For full context, decisions,
and verification evidence, read the referenced task file.

---

## Index

| Task ID | Completed | Status | Purpose | Task File |
|---------|-----------|--------|---------|-----------|
| aesm-implementation-foundations | ~2026-09-19 | complete | Establish Process Instance persistence, Execution Context, first vertical slice semantics, minimal Runtime core, and recording behavioral validation | [→](aesm-implementation-foundations.md) |
| agent-guidance-and-environment-mapping | ~2026-09-19 | complete | Establish Agent Guidance Interface, Agent–Runtime boundary, Runtime API surface (four adapter surfaces), minimal bridge, and environment mechanism mapping | [→](agent-guidance-and-environment-mapping.md) |
| agent-boundary-mechanism-validation | ~2026-09-19 | complete | Validate the complete operational chain from fresh Agent session through Runtime mutations, persisted state, and fresh-session recovery | [→](agent-boundary-mechanism-validation.md) |
| dbp-empirical-execution | ~2026-09-19 | complete | Execute controlled DBP engineering request under AESM; reconcile evidence; identify AESM participation gap; establish project/process binding as separate concern | [→](dbp-empirical-execution.md) |
| engineering-scope-identity-and-scope-resolution | 2026-09-21 | complete | Define Engineering Scope Identity as distinct AESM concept; design and implement deterministic Runtime-owned scope resolution; validate 204/204 tests | [→](engineering-scope-identity-and-scope-resolution.md) |
| repository-portable-continuation-validation | 2026-09-21 | complete | Demonstrate Git-portable .aesm/ and fresh-Agent continuation from independent checkout; validate PASS for Git round trip and fresh-session continuation | [→](repository-portable-continuation-validation.md) |
| runtime-consistency-and-continuity-hardening | 2026-09-21 | complete | Harden Runtime persistence (rollback symmetry, schema evolution, concurrency, recovery); repair API compatibility; validate cross-process continuity; 192/192 regression PASS | [→](runtime-consistency-and-continuity-hardening.md) |
| planning-system-restructuring | 2026-09-22 | complete | Establish structured, deterministic, recoverable plan/ planning system replacing monolithic IMPLEMENTATION_PLAN.md; enable fresh Agent navigation without prior context | [→](planning-system-restructuring.md) |
| aesm-planning-authorization-refinement | 2026-09-22 | complete | Strengthen backlog-to-active authorization gate in README.md; make CURRENT.md explicitly distinguish candidate from authorized task; add non-binding Suggested Successor to planning-system-restructuring | [→](aesm-planning-authorization-refinement.md) |
| planning-verification-time-boundary-correction | 2026-09-22 | complete | Correct the historical verification record temporal boundary; reconcile Work Unit structural state; resolve blocked test subtasks (204/204 PASS); implement planning-system refinement (authorization, blocked-recovery, projection-reconciliation, decision-lifecycle, runtime-boundary, fresh-agent review) | [→](planning-verification-time-boundary-correction.md) |
| resolve-dbp-active-process-instance-disposition | 2026-09-23 | complete | Inspect active DBP PI, obtain and record human termination authorization, execute Runtime-mediated ACTIVE→TERMINATED lifecycle transition, independently verify persisted state, record resolution evidence for blocked continuation Task | [→](resolve-dbp-active-process-instance-disposition.md) |
| plan-execution-boundary-governance-resolution | 2026-09-23 | complete | Establish, implement, and validate the AESM planning/execution boundary: normative boundary model, scope control, blocked-lifecycle integration, conformance tests (9/9 pass, 213/213 regression) | [→](plan-execution-boundary-governance-resolution.md) |

---

## Decisions Still in Effect (Quick Reference)

Key decisions from completed tasks that remain active constraints for all future work.
For full context, read the referenced task file.

| Decision | Source Task |
|----------|------------|
| Runtime is the sole authority for persisted AESM state | aesm-implementation-foundations |
| Planning records ≠ Runtime evidence | aesm-implementation-foundations |
| Recording behavioral validation closes the recording contract | aesm-implementation-foundations |
| Agent Guidance Interface semantic contract is closed | agent-guidance-and-environment-mapping |
| Bridge is thin; four adapter surfaces only | agent-guidance-and-environment-mapping |
| Minimum mechanism: no VS Code extension, MCP, or second PI store required | agent-guidance-and-environment-mapping |
| Mechanism validation gate is closed | agent-boundary-mechanism-validation |
| DBP engineering activity and AESM non-participation are separate findings | dbp-empirical-execution |
| No retroactive AESM evidence for original DBP execution | dbp-empirical-execution |
| Engineering Scope Identity is distinct from PI identity, repository identity, workspace identity | engineering-scope-identity-and-scope-resolution |
| No first-class Project entity; no workspace-wide PI index | engineering-scope-identity-and-scope-resolution |
| Repository isolation enforced; scope resolution is Runtime-owned | engineering-scope-identity-and-scope-resolution |
| Git-portable .aesm/; result does not imply multi-repository auto-resolution | repository-portable-continuation-validation |
| Remote Git round trip is explicitly unclaimed from prior validations | repository-portable-continuation-validation |
| Rollback symmetry required for all authoritative state mutations | runtime-consistency-and-continuity-hardening |
| Schema version 1 explicit; missing defaults to v1; unsupported rejected | runtime-consistency-and-continuity-hardening |
| Single-writer assumption; PI writes use optimistic concurrency (updated_at) | runtime-consistency-and-continuity-hardening |
| Per-file atomic writes + rollback = bounded recovery; no generalized transaction layer | runtime-consistency-and-continuity-hardening |
| execution/ directory permanently absent; do not recreate | runtime-consistency-and-continuity-hardening |
| Execution discovery does not create authorization; a Finding is classified evidence, not authorization | plan-execution-boundary-governance-resolution |
| Work Candidate is record-only; only explicit planning authorization creates executable work | plan-execution-boundary-governance-resolution |
| Scope decision is deterministic: in scope / out of scope / blocking | plan-execution-boundary-governance-resolution |
| Out-of-scope blocking condition requires the existing blocked lifecycle | plan-execution-boundary-governance-resolution |
| Blocker resolution does not authorize or auto-reactivate a blocked Task | plan-execution-boundary-governance-resolution |
| Completion is acceptance-based; future-work candidates do not prevent completion | plan-execution-boundary-governance-resolution |

---

## Strategic Notes

Transferred from the former `plan/ROADMAP.md`. These are directional items,
not authorized work. Each requires explicit human authorization and a formal
Task before any implementation occurs.

| Item | Status | Notes |
|------|--------|-------|
| Cross-Repository Scope Resolution | Not authorized | Current scope resolution is repository-local. Requires demonstrated need and a new design gate. |
| Operational Scale Validation | Not authorized | Multiple concurrent PIs, multi-session work over weeks, longer-timeline evidence traceability. Depends on DBP continuation validation. |
| Agent Discovery of Process Instances | Not authorized | How an Agent discovers the applicable PI when the scope is not obvious from repository structure. Separate design concern from bridge/scope-resolution. |
| Normative Documentation Reconciliation | Not authorized | Ensure docs/ accurately reflects implementation architecture. Evaluate periodically. |
