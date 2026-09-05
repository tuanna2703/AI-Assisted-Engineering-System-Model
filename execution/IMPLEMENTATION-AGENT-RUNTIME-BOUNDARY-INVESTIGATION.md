# Agent–Runtime Boundary Investigation

## Purpose

Determine the minimum operational interaction required for an AI Agent execution to participate in an AESM Process Instance while preserving the semantic boundary between Agent, Runtime, and Execution Environment.

This is an implementation-derived investigation. It does not redefine EPM, PEM, Process Instance, Execution Context, Agent, Runtime, or Execution Environment semantics.

## Investigation Trigger

The first observed engineering execution successfully performed investigation, engineering decision-making, implementation, and verification, but no executable AESM mechanism participated. It relied on task/documentation guidance, Agent reasoning, Execution Environment tools, conversation continuity, and ordinary artifacts.

No AESM Process Instance was created, no authoritative AESM Execution Context was attached, and the existing Runtime was not invoked. This provides a control condition: disciplined engineering can occur without AESM participation, but that execution is not an AESM-controlled execution.

## Evidence Reviewed

- `IMPLEMENTATION_PLAN.md`
- `docs/04-Execution-Model.md`
- `docs/06-Participants-and-Agent-Participation.md`
- `docs/07-Runtime-and-Conformance.md`
- `docs/12-AI-Agent-Guide.md`
- `runtime/core/models.py`
- `runtime/core/runtime.py`
- `runtime/core/store.py`
- `runtime/README.md`
- `execution/IMPLEMENTATION-MINIMAL-RUNTIME-INTERFACE.md`
- the first Agent execution observation and analysis report.

## Established Boundary

The Agent is a Participant, not the Runtime. It may investigate, reason, propose decisions, modify artifacts when authorized, verify work, report results, and request intervention. It does not own authoritative Execution Context and does not independently convert its output into authoritative process state.

The Runtime executes PEM semantics, preserves authoritative operational state, recognizes relevant inputs, evaluates applicable execution conditions, applies permitted mutations, preserves traceability, and supports continuity/recovery.

Therefore the integration must not turn the Agent into the Runtime or make the Execution Environment authoritative.

## Current Runtime Capability

The existing Runtime already provides:

- `create_process(objective)`;
- `attach(process_instance_id)`;
- `observe(...)`;
- `recognize_decision(...)`;
- `set_pending_execution(...)`;
- `record_verification(...)`;
- `recognize_engineering_completion(...)`;
- ProcessStore persistence of `process.json`, `context.json`, and `history.jsonl`.

The existing persistence foundation is therefore sufficient for an Agent-participation experiment. Confirmed gaps remain artifact association and terminal Process Instance handling; lifecycle behavior remains dependent on the first vertical slice's derived semantics.

## Minimum Operational Interaction

The investigation identifies five necessary interaction categories.

### Establish or recover Process Instance

Before material work, the execution must establish or identify a Process Instance and its authoritative Context. On resume, the Agent receives the stable Process Instance identity and current Context rather than reconstructing identity from conversation history.

### Supply authoritative Context

The Agent must be able to inspect current authoritative Context before material action and after meaningful updates. It must be sufficient to establish objective, requirements/constraints, current process state, evidence, decisions/gates, implementation and verification status, pending/unresolved work, risks, failures, and uncertainty.

### Submit contributions through recognition

The Agent must submit material contributions/results through a Runtime-accessible boundary rather than directly mutating authoritative Context. Relevant categories include evidence candidates, proposed Engineering Decisions, pending work, artifact/result information, verification results, and completion information.

Receipt, recognition, verification, and mutation remain distinct. Agent output is input to the execution system, not automatic authoritative state.

### Receive updated execution situation

After recognition and permitted mutation, the Runtime must make the updated authoritative situation available to the Agent, including current Context/state, pending work, unresolved conditions, conflicts or recognition failures, verification status, and whether further action is required/permitted.

### Persist independently of the session

Meaningful process information must persist independently of the Agent session. Another Agent must be able to reconstruct objective, evidence, recognized decisions, implementation/artifact status, verification status, unresolved matters, pending work, applicable EPM/PEM binding, and material failure/uncertainty.

## Responsibility Allocation

| Concern | Agent | Runtime | Execution Environment |
|---|:---:|:---:|:---:|
| Engineering interpretation/investigation | Primary | Preserve process boundary | Provide tools/interface |
| Engineering judgment | Primary | Must not assume | Human interaction |
| Evidence/decision contributions | Produce/propose | Recognize/persist | Transport |
| Engineering implementation | Perform authorized work | Govern applicable execution conditions | Provide capabilities |
| Artifact association | Produce/modify | Persist association | Filesystem/tooling |
| Verification | Perform | Record/recognize | Execute tools |
| Authoritative state mutation | No independent authority | Apply permitted mutation | No semantic authority |
| Continuity | Consume authoritative state | Own authoritative persistence | Session continuity only |

## Minimum Interface Shape

No specific transport is justified. MCP, CLI, HTTP, RPC, or an IDE mechanism remain implementation choices.

Semantically, the Agent-facing boundary needs operations equivalent to:

```text
create_or_attach_process
get_current_context
submit_contribution
get_execution_result_or_status
```

Persistence remains behind the Runtime boundary. A future adapter should expose semantic process participation rather than mirror every internal Runtime method.

## Guidance vs Runtime Control

The first execution shows that guidance can encourage investigation-first behavior, explicit reasoning, verification, limited scope, and uncertainty reporting. Guidance alone cannot create authoritative process state or guarantee continuity.

The minimum division is:

```text
Guidance
    → tells the Agent how to participate

Runtime
    → recognizes contributions
    → controls authoritative mutation
    → preserves continuity
    → applies applicable execution conditions

Execution Environment
    → supplies interaction and engineering capabilities
```

Not every instruction requires enforcement. Runtime enforcement should be introduced only where a vertical-slice requirement demonstrates an authority or reliability need.

## Findings

### Finding A — An operational Agent–Runtime boundary is necessary

**Classification:** Implementation requirement derived from evidence.

Without an invocation path from the Agent's Execution Environment to the Runtime, the Runtime cannot participate in execution. Documentation does not instantiate a Process Instance or persist Context by itself.

### Finding B — The first integration should not expose the entire Runtime API

**Classification:** Minimality decision.

Directly exposing all current Runtime methods would couple the Agent to implementation structure. A small Agent-facing adapter is preferable.

### Finding C — MCP is not established as an AESM requirement

**Classification:** Not established as a semantic requirement.

The evidence establishes the need for an invocation path, not a particular transport. Choosing MCP as normative would conflict with implementation independence without further evidence.

### Finding D — The boundary must be bidirectional

**Classification:** Implementation requirement derived from continuity semantics.

The Agent needs authoritative Context as input, while the Runtime needs Agent contributions/results as input. A one-way guidance mechanism is insufficient.

### Finding E — Recognition is the critical authority boundary

**Classification:** Confirmed by normative documentation and current implementation.

The integration must preserve the distinction between Agent contribution and authoritative mutation; a shared writable state file would not be equivalent.

### Finding F — Process identity must outlive the Agent session

**Classification:** Confirmed by the first execution and continuity semantics.

A conversation/session can terminate while engineering work remains active. Process Instance identity must therefore remain independently persisted.

## Minimum Prototype Integration

The next implementation experiment should contain only:

1. an Agent-facing adapter for create/attach, Context retrieval, contribution submission, and execution-status retrieval;
2. one mechanism allowing the selected Execution Environment to invoke that adapter;
3. persistence of recognized contributions through the existing Runtime;
4. execution metadata identifying the Agent/session without making it Process Instance identity;
5. tests showing that the Agent-facing interaction survives Agent/session replacement.

No generalized orchestration framework, dedicated IDE extension, distributed service, or broad Runtime redesign is justified.

## Deferred Questions

The following remain unresolved until their prerequisites are reached:

- exact EPM state/transition semantics for the selected engineering task;
- exact Process Instance termination semantics;
- which transition/condition, if any, must be Runtime-blocked;
- exact artifact-association API;
- exact Execution Environment adapter mechanism;
- multi-Agent/concurrent participation.

## Conclusion

AESM now has a clear implementation boundary for Agent participation: the interaction must be bidirectional. The Agent consumes authoritative Context and submits contributions/results; the Runtime recognizes them, applies permitted mutations, persists authoritative state, and returns the updated executable situation.

The investigation does not justify a normative AESM change or a specific transport. The next implementation step is an Agent-facing adapter experiment, but only after the remaining first-vertical-slice state, transition, completion, and termination semantics have been derived.
