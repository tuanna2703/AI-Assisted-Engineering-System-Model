# Agent Execution Integration — Implementation Record

## Record purpose

This record preserves implementation-specific findings, validation evidence, current gaps, and mechanism-specific guidance extracted from the Agent Execution Integration work.

It is an implementation record, not part of the canonical AESM semantic documentation.

## Documentation boundary decision

The repository baseline reserves `docs/` for descriptive AESM knowledge and `implementation/` for execution-generated implementation decisions, findings, and evidence. The cleanup therefore separates durable integration semantics from implementation status and validation evidence.

`docs/Agent-Execution-Integration.md` is retained only as an integration-level architectural view. Detailed Agent participation semantics remain governed by `docs/06-Participants-and-Agent-Participation.md`; Runtime responsibilities by `docs/07-Runtime-and-Conformance.md`; continuity by `docs/08-Continuity-Traceability-and-Reconsideration.md`; and lifecycle semantics by `docs/11-Applicable-Process-Instance-Lifecycle-Semantics.md`.

## Implementation findings retained

### Agent guidance delivery

The implementation work identified persistent Agent instructions as the minimum durable mechanism for delivering baseline AESM participation guidance before a specific Process Instance is known.

The concrete environment instruction surface is not an AESM semantic requirement. Its configuration remains an implementation concern.

### Runtime interaction mechanism

A callable bridge-capable mechanism is required for an Agent to move from guidance to Runtime interaction. The implementation mapping identified CLI/programmatic invocation, MCP-equivalent tooling, IDE-integrated tooling, and equivalent adapters as possible transport mechanisms. No particular transport was selected as an AESM requirement.

### Process Instance continuity

The Runtime and ProcessStore remain the authoritative source of Process Instance identity and Execution Context. Known-ID cross-process recovery has been demonstrated. A fresh Agent still needs an environment-level way to receive or obtain the authoritative Process Instance identifier.

Objective-to-Process-Instance discovery remains an implementation dependency under Runtime ownership. The Agent–Runtime bridge must not search persistence independently and declare its own result authoritative.

### Bridge capability boundary

The implemented bridge delegates accepted Agent-facing operations to Runtime rather than reproducing Runtime semantics. The demonstrated surface includes Process Instance creation, known-ID attachment, Context access, investigation, observation, decision recognition, implementation, artifact recording, verification, reconsideration, and engineering completion.

`set_pending_execution` remains outside the Agent-facing bridge boundary. Direct lifecycle mutation and Runtime `stop` are likewise not Agent capabilities merely because corresponding Runtime functionality exists.

The bridge must not own identity, duplicate Context semantics, maintain competing persistence, implement EPM/PEM semantics, independently implement lifecycle semantics, bypass Runtime guards, or turn technical capability into semantic authority.

### Environment mechanism mapping

The completed mapping established that the existing environment capabilities are sufficient to host a thin Agent–Runtime adapter. The mapping identified persistent Agent instructions, task/process-specific guidance, reusable skills/tools, repository file access, command/Python execution, Runtime invocation, Context access, mutation, result return, and durable Process Instance/Execution Context persistence.

The mapping did not authorize a new MCP server, VS Code extension, Runtime redesign, ProcessStore change, or DBP source change.

## Current implementation gaps

| Area | Status | Implementation implication |
|---|---|---|
| Durable Agent guidance delivery | Configuration/mechanism gap | Configure an existing environment instruction surface |
| Process Instance ID delivery to a fresh Agent | Mechanism gap | Establish an environment/bridge delivery path |
| Objective-to-instance discovery | Runtime capability gap | Resolve under Runtime ownership; do not move authority into the bridge |
| EPM binding population/delivery | Evidence incomplete | Verify explicit recoverable EPM binding where required |
| Agent-side recognition honesty | Enforcement limitation | Do not claim technical enforcement beyond Runtime recognition/validation |
| Lifecycle request exposure through bridge | Separate specification decision required | Do not expose merely because Runtime supports an operation |
| End-to-end Agent participation | Empirical gap | Validate through real engineering work, not deterministic bridge tests alone |

## Evidence interpretation

The implementation validation established the following evidence ladder:

```text
Documentation exists
    ≠ Agent received guidance
    ≠ Agent followed guidance
    ≠ Agent interacted with Runtime
    ≠ Runtime-authoritative state changed
    ≠ End-to-end AESM Agent participation was demonstrated
```

Deterministic Runtime/bridge tests establish implementation behavior. They do not prove that an actual AI Agent received and followed AESM guidance during engineering work.

A historical full-suite validation at the relevant implementation point reported 137/137 tests passing. This record preserves that result as historical evidence only; it is not a claim that the suite was executed during this documentation cleanup.

## Mechanism-readiness validation

The implementation work used `scripts/validate_environment_mechanisms.py` as a mechanical readiness probe. The probe checks common instruction/skill/tool surfaces, verifies the bridge import and minimum bridge surface, creates a Process Instance through the bridge in an isolated store, recreates the bridge, and recovers authoritative Context.

A successful readiness probe demonstrates mechanism availability and bridge/runtime usability. It does not demonstrate genuine AI-Agent participation.

## Empirical Agent participation gate

The first real Directories Builder Pro execution remains the empirical gate for end-to-end participation.

Required evidence should distinguish the actual Agent interaction from post-hoc fabrication and should include, as applicable:

- the persistent guidance surface actually loaded by the Agent;
- the authoritative Process Instance identifier;
- authoritative Context obtained by the Agent;
- at least one Runtime-mediated mutation caused by Agent work;
- resulting persisted Context/history;
- the actual engineering artifact;
- independent verification evidence;
- traceability separating Agent reasoning/conversation from Runtime-recognized authoritative state.

The following are insufficient by themselves: documentation existing in the repository, a deterministic bridge test, a Process Instance existing without Agent interaction, an Agent claim that AESM was followed, or manually fabricated Context/evidence after the work.

## Historical implementation evidence

The Environment Mechanism Mapping work recorded that the environment had sufficient general capabilities to host a thin Agent–Runtime adapter and that the remaining problem was concrete bridge implementation rather than Runtime semantic redesign.

The later bridge implementation and validation work established the bridge as a thin delegation boundary. The reconsideration capability was subsequently exposed explicitly while `set_pending_execution` remained intentionally outside the Agent-facing boundary.

Relevant historical commits include:

- `187ba9033a60ab0435c79afa72e29fb9fa86268f` — Environment Mechanism Mapping action log.
- `c2c07e1795acfa732c53feaafa608e87fd7f20cc` — Agent–Runtime bridge implementation and test suite.
- `15307e95878eca1e0c82277051f818c113f280fd` — reconsideration exposed through the bridge.
- `908b52a6bceaddbace80dbd8cfa0e51864c92a71` — documentation index update introducing the integration document.

These references are traceability aids; they do not become AESM semantic authority.

## Cleanup result

The former mixed integration document contained both durable architectural material and implementation-specific status/evidence. Implementation-specific material is retained here so that it remains available for implementation traceability without being mistaken for canonical AESM semantics.

The canonical integration document now avoids current test results, implementation gaps, scripts, historical validation claims, and environment-specific configuration details.
