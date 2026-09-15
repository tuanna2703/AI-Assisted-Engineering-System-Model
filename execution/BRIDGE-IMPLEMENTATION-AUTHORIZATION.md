# Agent–Runtime Bridge Implementation Authorization

## 1. Purpose and Status

This artifact records the controlled decision on whether the Agent–Runtime bridge defined by `execution/AGENT-RUNTIME-BRIDGE-CONTRACT.md` is sufficiently determined and bounded for implementation.

**Status: CONDITIONALLY AUTHORIZED — BOUNDED FIRST IMPLEMENTATION SLICE.**

Authorization is limited to the existing Runtime capabilities that are already demonstrated and does not authorize Runtime redesign, discovery ownership transfer, or broader AESM expansion.

## 2. Decision Basis

The decision is based on the completed evidence chain:

1. Actual Runtime implementation and executable verification recorded in `execution/RUNTIME-API-INSPECTION.md`.
2. Agent–Runtime boundary reconciliation in `execution/BRIDGE-BOUNDARY-RECONCILIATION.md`.
3. Execution Environment feasibility mapping in `execution/ENVIRONMENT-MECHANISM-MAPPING.md`.
4. Determined bridge contract in `execution/AGENT-RUNTIME-BRIDGE-CONTRACT.md`.
5. Normative AESM architecture, Runtime/conformance, Process Instance/Execution Context, and continuity documents.
6. Existing behavioral and cross-process Runtime validation evidence.

The evidence establishes that the current Runtime directly supports Process Instance creation, known-ID recovery, authoritative Execution Context access, supported operation dispatch, persistence, and cross-process recovery. The evidence also establishes that objective-to-existing-Process-Instance discovery is not currently exposed by the Runtime.

## 3. Authorization Questions and Decisions

| Decision question | Determination |
|---|---|
| Is the bridge contract sufficiently determined? | **Yes**, for the create, known-ID recovery, Context access, dispatch, and authoritative result/state paths. |
| Can the first implementation slice use the existing Runtime API? | **Yes.** No Runtime semantic change is required for the authorized slice. |
| Does missing objective-to-Process-Instance discovery block all bridge implementation? | **No.** It blocks the complete ordinary no-ID continuation flow, but not the bounded supported paths. |
| Should discovery be implemented in the bridge? | **No.** Runtime remains the semantic owner of discovery. |
| Should a new Runtime discovery API be added as part of this authorization? | **No.** Any such capability requires separate evidence, design, and authorization. |
| Must a particular transport be normative? | **No.** The implementation may use the smallest available Execution Environment mechanism without turning that mechanism into AESM architecture. |
| Can implementation proceed without changing Runtime semantics or Process Store? | **Yes**, for the authorized slice. |
| Is generalized Agent orchestration authorized? | **No.** |

## 4. Authorized Implementation Scope

The following implementation is authorized:

### 4.1 Process Instance creation

Implement a thin bridge operation that accepts an engineering objective and delegates Process Instance creation to the existing Runtime capability.

Requirements:

- Runtime generates the authoritative Process Instance identity.
- The bridge does not create a competing identifier.
- The authoritative resulting state and Execution Context are returned to the Agent.

### 4.2 Known-ID Process Instance recovery

Implement a thin bridge operation that accepts an authoritative Process Instance identifier and delegates recovery to the existing `Runtime.attach(process_instance_id)` capability.

Requirements:

- The bridge treats the identifier as a reference, not as proof of state.
- Runtime/Process Store remain authoritative for recovered state.
- Unknown or invalid identifiers are returned as Runtime errors; the bridge must not silently create a replacement instance.

### 4.3 Authoritative Execution Context access

Implement bridge access to the current Runtime-owned Execution Context after creation or attachment.

Requirements:

- Return the Runtime's authoritative Context representation.
- Do not create a second Context model.
- Do not persist an independent bridge-owned Context.
- Do not treat Agent conversation history as authoritative state.

### 4.4 Supported Runtime operation dispatch

Implement a thin routing surface for operations already supported by the actual Runtime.

Requirements:

- The bridge may validate request shape and routing requirements.
- Runtime remains authoritative for semantic validation, guards, mutation, and persistence.
- Unsupported operations are rejected rather than emulated.
- Runtime results and resulting authoritative state are returned to the Agent.

### 4.5 Authoritative result/state return

Ensure every confirmed Runtime interaction returns sufficient authoritative information for the Agent to continue from current state.

Requirements:

- Do not infer successful mutation when Runtime confirmation was not received.
- Preserve Runtime errors and guard rejections.
- Preserve persistence/recovery failures.
- Refresh stale state before state-sensitive continuation where required by the integration.

## 5. Authorized Implementation Hosting Mechanism

The first implementation may use a **repository-local executable adapter/module invoked through the already demonstrated Agent Execution Environment command/Python capability**.

This is an implementation mechanism for the prototype only. It is **not** a normative AESM requirement and does not establish a mandatory CLI, MCP server, VS Code integration, or other transport.

The implementation should remain callable from the existing Agent environment without requiring a dedicated IDE extension or generalized orchestration framework.

## 6. Explicit Discovery Boundary

Objective-to-existing-Process-Instance discovery remains unresolved.

The current Runtime does not expose an objective/search/list capability. Therefore:

- the bridge must not scan persistence files and choose an instance;
- the bridge must not maintain a parallel Process Instance index;
- the bridge must not infer authoritative identity from conversation history;
- the bridge must not add a new Runtime discovery API under this authorization;
- the implementation may support new-request creation and known-ID continuation;
- no-ID continuation that requires discovery must report the capability as unavailable rather than fabricate discovery.

A separate Runtime-owned discovery design may be considered later if real vertical-slice evidence demonstrates that it is necessary.

## 7. Continuity and Authority Constraints

Implementation must preserve these existing semantics:

- Process Instance persistence remains Runtime/Process Store responsibility.
- Execution Context remains Runtime-owned authoritative state.
- Cross-process recovery must continue to work.
- Runtime guards remain authoritative.
- Agent/session loss must not invalidate persisted process state.
- The bridge may hold transient request/response data only as required by its execution mechanism.
- No bridge-owned authoritative persistence is permitted.

## 8. Explicitly Unauthorized Work

The following work is outside this authorization:

- Runtime lifecycle redesign;
- Process Store redesign or replacement;
- new Process Instance persistence semantics;
- bridge-owned Process Instance discovery;
- bridge-owned authoritative Context storage;
- a new Runtime discovery/search/list API;
- automatic no-ID Process Instance matching not provided by Runtime;
- generalized Agent orchestration;
- EPM changes;
- PEM changes;
- lifecycle semantic changes;
- a dedicated VS Code extension;
- mandatory MCP architecture;
- normative transport selection;
- production-scale infrastructure;
- unrelated Runtime refactoring;
- speculative AESM model expansion.

## 9. Implementation Acceptance Conditions

The bounded implementation may be considered complete only when executable evidence demonstrates:

1. a new engineering objective can create a persistent Process Instance through the bridge;
2. the bridge returns the authoritative Process Instance identity and Context;
3. a later interaction can recover the same Process Instance using its known identifier;
4. authoritative Context can be obtained after recovery;
5. at least the Runtime operations required by the selected first vertical slice can be dispatched through the bridge;
6. Runtime guards and failures remain authoritative and observable;
7. persistence and cross-process continuity remain intact;
8. no parallel authoritative Process Instance or Context state is introduced;
9. the bridge does not claim objective-to-instance discovery that the Runtime does not provide;
10. existing Runtime behavior outside the bridge remains regression-safe.

The implementation must include focused tests for both successful and failure paths appropriate to the supported bridge operations.

## 10. Required Evidence During Implementation

Implementation work must record:

- exact Runtime APIs invoked;
- exact bridge entry points and request/response shapes;
- mechanism used to invoke the bridge from the Execution Environment;
- Process Instance creation/recovery evidence;
- Context return evidence;
- Runtime dispatch evidence;
- failure/guard propagation evidence;
- persistence and cross-process continuity evidence;
- any newly discovered gap or semantic ambiguity.

If implementation evidence requires a Runtime semantic change, the implementation must stop at that boundary and produce a separate decision/authorization request rather than silently expanding this authorization.

## 11. Final Authorization Decision

**Decision: CONDITIONALLY AUTHORIZE.**

The Agent–Runtime bridge is sufficiently determined and bounded to authorize implementation of the following first slice:

> **Create Process Instance → recover by known ID → expose authoritative Execution Context → dispatch already-supported Runtime operations → return authoritative results/state.**

The implementation must remain thin, mechanism-neutral at the AESM architectural level, and Runtime-authority-preserving.

The missing objective-to-Process-Instance discovery capability is explicitly retained as a dependency/gap and is **not** authorized for implementation by this decision.

This authorization is therefore sufficient to begin the next controlled work unit: **Bridge Implementation**.

## 12. Completion Criterion

Bridge Implementation Authorization is complete because the repository now contains an explicit evidence-backed determination of:

- what implementation is authorized;
- what mechanism may host the prototype implementation;
- what Runtime capabilities may be used without semantic change;
- what discovery capability remains unresolved;
- what work is explicitly unauthorized; and
- what evidence must be produced before the implementation can be accepted.
