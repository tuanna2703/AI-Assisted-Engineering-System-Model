# Agent Guidance Interface

> **Status:** Analysis complete. Implementation Decision: existing mechanisms satisfy the semantic contract for all governed-execution capabilities; two pre-existing deferred gaps remain (guidance delivery mechanism, objective-to-Process-Instance discovery); no new implementation is justified within this work unit.
>
> **Evidence basis:** Direct inspection of all referenced AESM documentation, runtime source, bridge source, test suite (137/137 passing), and execution artifacts recorded through 2026-09-17.

---

## 1. What the Existing AESM Model Requires from an Agent

The AESM model specifies Agent participation obligations across `docs/06-Participants-and-Agent-Participation.md`, `docs/04-Execution-Model.md`, `docs/05-Process-Instance-and-Execution-Context.md`, `docs/07-Runtime-and-Conformance.md`, and `docs/08-Continuity-Traceability-and-Reconsideration.md`.

### 1.1 Pre-action Situational Awareness

Before making a material contribution, the Agent must establish (doc-06, "What the Agent should establish before acting"):

1. Engineering Objective
2. Current Requirements and Constraints
3. Current Process State
4. Relevant Evidence and Assumptions
5. Accepted and pending Engineering Decisions
6. Applicable Decision Gates
7. Current implementation and verification status
8. Unresolved questions, risks, contradictions, and failures
9. Pending work and expected next actions
10. Applicable authorization or execution conditions

**Source:** `docs/06-Participants-and-Agent-Participation.md`
**Status:** Documentation only — no mechanism currently guarantees delivery of this information to an Agent starting a session.

### 1.2 Controlled Contribution Path

The Agent must contribute through the Runtime-controlled recognition path:

```
Agent output → Observation/Contribution → Runtime-controlled recognition → Permitted State Mutation → Execution Context/Trace
```

**Source:** `docs/06-Participants-and-Agent-Participation.md` "Controlled contribution"
**Status:** Executable — the bridge `dispatch()` method routes Agent-requested operations to Runtime guards without allowing the Agent to write state directly.

### 1.3 Continuity Obligation

The Agent must resume from authoritative Execution Context supplied by the AESM execution system. Its own conversational memory is explicitly not authoritative.

**Source:** `docs/06` "Continuity"; `docs/08` "Authoritative continuity"
**Status:** Partially executable — the bridge/Runtime can supply authoritative context when the Agent knows the Process Instance ID; no mechanism currently delivers the ID to a fresh Agent or prevents reliance on conversation memory.

### 1.4 Evidence and Traceability Requirements

Material Agent output must be distinguishable by semantic role. Recognition and mutation are separate steps. The Agent must not fabricate Evidence, verification, or authority.

**Source:** `docs/06` "Reporting contributions"; `docs/04` "Recognition and mutation"
**Status:** Executable at the Runtime enforcement layer (recognition guards in `runtime.py` lines 319–325 require `recognized: True` and `basis`). Documentation guidance for the Agent is present; no mechanism enforces correct role annotation before submission.

### 1.5 Authority-Preservation Invariants

```
Agent != Runtime
Agent capability != authority
Agent output != automatic authority
Proposal != authorization
Observation != mutation
Engineering Decision != Execution Determination
Conversation != authoritative state
```

**Source:** `docs/06` "Authority-preservation invariants"
**Status:** Executable — bridge architecture enforces these at code level; Runtime rejects unauthorized operations.

---

## 2. Responsibility Boundary

### 2.1 Authority Classification Table

| Responsibility | Who Initiates | Who Has Authority | Who Performs | Authoritative State Location |
|---|---|---|---|---|
| Engineering-request interpretation | Human (request), Agent (interpretation) | Agent (interpretation); Human (intent) | Agent | Agent reasoning — not persisted until recognized |
| Process Instance creation | Agent (on behalf of human) | Runtime | Runtime via bridge | ProcessStore (filesystem JSON) |
| Process Instance discovery (objective to ID) | Agent | Runtime | Not implemented — deferred gap | Runtime/ProcessStore |
| Process Instance recovery (known ID) | Agent | Runtime | Runtime via bridge | ProcessStore |
| Execution Context access | Agent | Runtime | Runtime via bridge | Runtime in-memory + ProcessStore |
| AESM guidance acquisition | Agent | AESM docs (EPM/PEM) | Agent (reads docs) | `docs/` repository files |
| Process-specific guidance | Agent | Process Instance + Execution Context | Runtime via bridge | ExecutionContext fields |
| Engineering investigation | Agent | Agent (engineering work) | Agent | — (results submitted via `observe`) |
| Evidence recognition | Agent (submits), Runtime (recognizes) | Runtime | Runtime `observe` method | Execution Context `evidence` list |
| Decision recognition | Agent (proposes), Runtime (recognizes) | Runtime | Runtime `recognize_decision` | Execution Context `engineering_decisions` |
| Artifact recording | Agent (produces), Runtime (records) | Runtime | Runtime `record_artifact` | Execution Context `artifacts` |
| Verification | Agent (performs), Runtime (records) | Runtime | Runtime `record_verification` | Execution Context `verification` |
| Lifecycle transitions | Authorized actor | Runtime | Runtime `apply_lifecycle_determination` | ProcessInstance.lifecycle |
| Engineering completion | Agent (conditions), Runtime (recognizes) | Runtime | Runtime `recognize_engineering_completion` | ExecutionContext.engineering_completion |
| Reconsideration | Agent (proposes), Runtime (executes) | Runtime | Runtime `reconsider` | State rollback + `failure_uncertainty` |
| Continuity across sessions | Agent (uses ID) | Runtime | Runtime via bridge | ProcessStore |

### 2.2 Ambiguous / Specification Decision Required

**Objective-to-Process-Instance discovery:** Model assigns discovery authority to the Runtime (`docs/07` "Process Instance discovery"), but the current Runtime has no objective-to-instance search. Gap pre-recorded in `execution/AGENT-RUNTIME-BRIDGE-CONTRACT.md` section 6. Authority = Runtime; mechanism = unresolved.

**Lifecycle transition initiation by Agent:** Model permits Participant lifecycle requests where applicable semantics permit; bridge does not expose `apply_lifecycle_determination`. Whether Agent-initiated lifecycle requests should be bridged is Specification Decision Required; the underlying Runtime capability exists.

**Guidance transport mechanism:** AESM does not prescribe how guidance reaches the Agent (`docs/04` "Implementation independence"). Whether guidance uses repository instructions, skills, MCP, persisted context, or another mechanism is Specification Decision Required — assigned to Environment Mechanism Mapping.

---

## 3. Minimum Semantic Agent Guidance Interface Contract

### 3.1 Guidance Acquisition

| Capability | Minimum requirement | Normative vs Advisory |
|---|---|---|
| AESM model guidance | Agent must be able to read and apply EPM/PEM semantics | Normative — violation means Agent operates outside AESM |
| Process Instance-specific guidance | Agent must obtain current Execution Context from Runtime | Normative — must come from Runtime state, not conversation |
| Engineering Objective | Agent must know the objective bound to the Process Instance | Normative |
| Current process state | Agent must know `process_state` before state-affecting decisions | Normative |
| Operational checklists | Pre-action self-assessment (doc-06 checklist) | Advisory — guides behavior, not enforced by Runtime |

How the Agent obtains guidance currently: by reading `docs/` files directly. No automated delivery mechanism exists.

How the Agent knows which guidance applies: `ProcessInstance.epm` and `ProcessInstance.pem` fields are the designated carriers (`models.py` lines 23–24) but are populated as empty dicts by default. No structured mechanism communicates the applicable EPM to the Agent.

### 3.2 Process Instance Interaction

| Capability | Minimum requirement | Current mechanism | Gap |
|---|---|---|---|
| Discover existing Process Instance | Identify which instance corresponds to the current request | None — Runtime lacks objective-to-instance search | Pre-recorded deferred gap |
| Create Process Instance | Create a new instance when none is applicable | `bridge.create_process(objective)` | None — implemented |
| Attach to known Process Instance | Recover an instance by ID | `bridge.attach(process_instance_id)` | None — implemented |
| Establish correct instance | Confirm recovered instance matches expected objective | Read `context.engineering_objective` from returned state | None — implemented |

### 3.3 Execution Context

| Capability | Minimum requirement | Current mechanism | Gap |
|---|---|---|---|
| Retrieve authoritative context | Get all fields of ExecutionContext from Runtime | `bridge.get_context()` returns complete `context.to_dict()` | None — implemented |
| Consume context information | Agent may use any field as information for reasoning | All ExecutionContext fields are exposed | None — implemented |
| Runtime-authoritative fields | `process_state`, `lifecycle`, `engineering_completion`, `version` must not be mutated by Agent directly | Bridge has no direct-write path; all mutation goes through Runtime operations | None — implemented |

### 3.4 Governed Execution

| Capability | Minimum requirement | Current mechanism | Gap |
|---|---|---|---|
| Request evidence recording | Submit observation for Runtime recognition | `bridge.dispatch("observe", {"observation": {...}})` | None |
| Request decision recognition | Submit decision proposal | `bridge.dispatch("recognize_decision", {...})` | None |
| Request state transitions | Initiate investigation, implementation, verification | `bridge.dispatch("start_investigation" / "begin_implementation" / "begin_verification")` | None |
| Request artifact recording | Record implementation artifact | `bridge.dispatch("record_artifact", {"artifact": {...}})` | None |
| Request verification recording | Record verification result | `bridge.dispatch("record_verification", {"result": {...}})` | None |
| Request reconsideration | Initiate reconsideration with reason | `bridge.dispatch("reconsider", {"reason": {...}})` | None |
| Request engineering completion | Recognize completion after successful verification | `bridge.dispatch("recognize_engineering_completion", {"completion": {...}})` | None |
| Runtime authority boundary | Agent reasons and recommends; Runtime validates and mutates | All operations pass through Runtime guards before state change | None |

A Runtime-authorized operation is any operation dispatched through the bridge that passes all Runtime guards (`_require_attached`, `_require_active_lifecycle`, `_require_state`, `_require_recognition`) and results in a success response containing updated authoritative `context` and `process_instance`.

### 3.5 Lifecycle

| Capability | Minimum requirement | Current mechanism | Gap |
|---|---|---|---|
| Observe current lifecycle state | Know whether Process Instance is `active`, `suspended`, or `terminated` | Returned in `process_instance.lifecycle` from any bridge call | None |
| Request lifecycle transitions | Not currently bridged | Not exposed through `bridge.dispatch()` | Specification Decision Required — `apply_lifecycle_determination` exists in Runtime but is not routed through bridge |
| Lifecycle authority | Remains exclusively with Runtime | Bridge does not expose lifecycle mutation as dispatch operation | None |

Lifecycle invariants preserved:
- Engineering completion does not equal lifecycle termination (demonstrated by `test_lc14`, `test_engineering_completion_does_not_terminate_process_instance`)
- Runtime stop/restart does not terminate the Process Instance (`test_runtime_stop_does_not_terminate_process_instance`)
- Terminated instances reject further lifecycle transitions (`test_lc11`)

Minimum Agent obligation: observe lifecycle state; if `suspended` or `terminated`, do not continue engineering execution.

### 3.6 Evidence and Traceability

| Capability | Minimum requirement | Current mechanism | Gap |
|---|---|---|---|
| Record observations as evidence | Submit through `observe`; Runtime applies recognition guard | `bridge.dispatch("observe", {"observation": {..., "recognition": {"recognized": True, "basis": "..."}}})` | None for recording; Agent-side role annotation not enforced |
| Record decisions | Submit through `recognize_decision`; Runtime recognition guard required | `bridge.dispatch("recognize_decision", ...)` | Same — annotation is Agent's responsibility |
| Record verification results | Submit through `record_verification` or structured path | `bridge.dispatch("record_verification", ...)` | None |
| Distinguish Agent claim from authoritative evidence | Runtime guards require `recognized: True` and `basis` | `_require_recognition()` in `runtime.py` lines 319–325 | Agent must not fabricate recognition |
| Trace decisions to evidence | Agent-side responsibility | Evidence and decisions stored separately in context lists | No automated trace linkage |
| Persist history | Runtime records all mutations with event history | `ProcessStore.save_context()` appends events | None |

The `_require_recognition()` guard requires `recognition["recognized"] is True` and a non-empty `basis`. The guard does not verify that the Agent actually established the factual basis; a compliant-shape dict satisfies the guard. The semantic protection is the documentation requirement that recognition must be honest, not a technical enforcement.

### 3.7 Continuity

| Capability | Minimum requirement | Current mechanism | Gap |
|---|---|---|---|
| Continue an existing Process Instance across sessions | Agent obtains Process Instance ID and calls `bridge.attach(id)` | Implemented — `bridge.attach()` delegates to `Runtime.attach()` | Agent must know the ID — no delivery mechanism exists |
| State survival across session boundary | All state persisted in ProcessStore (filesystem JSON) | Demonstrated by cross-process continuity tests | None |
| Continuity distinguished from new session | Agent must use `attach()` not `create_process()` | Bridge makes these distinct calls | Requires Agent to know the ID exists |

The continuity gap: a fresh Agent has no automatic mechanism to obtain an existing Process Instance ID. The Agent must be told the ID externally. This is the same deferred gap recorded in `execution/AGENT-RUNTIME-BRIDGE-CONTRACT.md` and `IMPLEMENTATION_PLAN.md`.

---

## 4. Existing Mechanisms Against Contract Capabilities

### 4.1 Evidence Distinction

```text
Documentation exists
        !=
Agent was instructed to use AESM
        !=
Agent actually used AESM guidance
        !=
Agent interacted with the Runtime
        !=
Runtime-authoritative state changed
        !=
End-to-end AESM participation was demonstrated
```

### 4.2 Mechanism-to-Capability Matrix

| Contract Capability | Implementation Status | Mechanism | Evidence Level |
|---|---|---|---|
| General AESM guidance (EPM/PEM) | Documentation only | `docs/` files, readable by Agent | Documentation exists |
| Process Instance-specific guidance | Partially executable | `bridge.get_context()` → ExecutionContext fields | Agent interacted with Runtime (smoke test) |
| EPM binding delivery | Evidence incomplete | `ProcessInstance.epm` field exists but is empty by default | Documentation exists; field not populated |
| Process Instance creation | Executable | `bridge.create_process()` | Runtime-authoritative state changed (smoke test + 34 bridge tests) |
| Process Instance discovery (objective→ID) | Missing | Explicitly deferred; `bridge.discover()` returns error | Not applicable — deferred gap |
| Process Instance recovery (known ID) | Executable | `bridge.attach()` | Runtime-authoritative state changed (smoke test + 34 bridge tests) |
| Execution Context retrieval | Executable | `bridge.get_context()` | Runtime-authoritative state changed |
| Evidence recording | Executable | `bridge.dispatch("observe", ...)` | Runtime-authoritative state changed (53 recording tests + smoke test) |
| Decision recognition | Executable | `bridge.dispatch("recognize_decision", ...)` | Runtime-authoritative state changed |
| State transitions (investigation / implementation / verification) | Executable | `bridge.dispatch(...)` for all three | Runtime-authoritative state changed |
| Artifact recording | Executable | `bridge.dispatch("record_artifact", ...)` | Runtime-authoritative state changed |
| Verification recording | Executable | `bridge.dispatch("record_verification", ...)` | Runtime-authoritative state changed |
| Reconsideration | Executable | `bridge.dispatch("reconsider", ...)` | Runtime-authoritative state changed (5 reconsider tests) |
| Engineering completion | Executable | `bridge.dispatch("recognize_engineering_completion", ...)` | Runtime-authoritative state changed |
| Lifecycle observation | Executable | `process_instance.lifecycle` returned in all bridge responses | Runtime-authoritative state accessed |
| Lifecycle transition request (bridged) | Specification Decision Required | `apply_lifecycle_determination` exists in Runtime; not routed through bridge | Documentation only |
| Continuity (known ID) | Executable | `bridge.attach()` | Runtime-authoritative state changed (continuity tests + smoke test) |
| Process Instance ID delivery to fresh Agent | Missing | No mechanism — deferred gap | Not demonstrated |
| Persistent AESM guidance delivery mechanism | Missing | No `.agents/` directory, skill, or MCP server in repository | Documentation only |

### 4.3 What the Smoke Test Actually Demonstrates

`tests/bridge/test_agent_invocation_smoke.py::TestAgentInvocationSmokeTest::test_agent_invocation_lifecycle` (PASSED):

Demonstrated: Agent-facing invocation through bridge → Runtime → persistence → cross-bridge recovery → full engineering lifecycle (investigation → implementation → verification → completion).

Evidence level: Agent interacted with Runtime; Runtime-authoritative state changed; Process Instance survived bridge/session boundary.

Not demonstrated: An actual AI Agent received AESM guidance and made decisions. The test is a deterministic Python script, not an AI Agent session. End-to-end AESM participation by an AI Agent has not been demonstrated.

---

## 5. Separation of Semantic Contract from Transport

The semantic Agent Guidance Interface contract is:

> The Agent must be able to: (a) receive AESM guidance, (b) obtain an authoritative Process Instance and Execution Context, (c) perform engineering work and request governed operations through the Runtime, and (d) resume from persistent authoritative state.

This contract is mechanism-neutral. Assessment against candidate mechanisms:

| Mechanism | Contract portion it could satisfy | Current status |
|---|---|---|
| Repository `docs/` files | AESM guidance (normative EPM/PEM) | Available — readable by Agent |
| `.agents/rules/` Agent instructions | AESM operational guidance delivery | No `.agents/` directory in AESM repository — not implemented |
| Agent skills/instructions | Process Instance-specific guidance delivery | Not implemented |
| `bridge/agent_runtime_bridge.py` (Python) | Process Instance access, Context access, dispatch, result return | Implemented — executable via `run_command` or programmatic import |
| MCP server | Same four bridge responsibilities via MCP protocol | Not implemented — not normatively required |
| CLI wrapper around bridge | Same four bridge responsibilities via CLI | Not implemented |
| IDE extension | Same four bridge responsibilities via IDE integration | Not implemented — explicitly excluded from scope |
| Project-level file (e.g., `.aesm-state`) | Process Instance ID delivery for continuity | Not implemented |
| `pending_execution` field in Execution Context | Continuity hint for resumed Agent | Implemented — readable from context |

The existing `bridge/agent_runtime_bridge.py` satisfies the process access, context access, dispatch, and result-return portions of the contract. The guidance delivery portion is not satisfied by any existing mechanism — the `docs/` files are present but are not automatically delivered.

---

## 6. Concrete DBP Engineering Request Trace

**Request:** Convert `Edit_Review_Form::business_id` from `Fields_Manager::SELECT` to `Fields_Manager::POST_SELECT` for `dbp_business`.

The DBP change is not implemented. This trace covers the semantic interface only.

### Step 1: Human Request

| Attribute | Value |
|---|---|
| Actor | Human |
| Action | Delivers engineering request |
| Interface capability | Human authority to initiate engineering work |
| Existing mechanism | Conversation / IDE / any channel |
| Gap | None |

### Step 2: Agent Interpretation

| Attribute | Value |
|---|---|
| Actor | Agent |
| Action | Interprets: identifies Edit_Review_Form, business_id, SELECT→POST_SELECT, dbp_business as engineering scope |
| Interface capability | Engineering-request interpretation |
| Existing mechanism | Agent reasoning (no AESM mechanism required) |
| Gap | None — this is Agent responsibility |

### Step 3: Guidance Acquisition

| Attribute | Value |
|---|---|
| Actor | Agent |
| Action | Reads AESM guidance: must create/recover Process Instance, obtain Execution Context, operate through Runtime, not treat output as automatic authority |
| Interface capability | AESM guidance acquisition |
| Existing mechanism | `docs/` files in repository — readable by Agent via file tools |
| Evidence status | Documentation exists; Agent not automatically delivered guidance |
| Gap | No persistent instruction mechanism delivers AESM guidance to the Agent automatically |

### Step 4: Process Instance Discovery or Creation

| Attribute | Value |
|---|---|
| Actor | Agent (initiates); Runtime (authority) |
| Action | No known Process Instance ID → `bridge.create_process("Convert Edit_Review_Form::business_id from SELECT to POST_SELECT for dbp_business")` |
| Interface capability | Process Instance creation |
| Existing mechanism | `bridge.create_process()` → `Runtime.create_process()` → `ProcessStore.create()` |
| Evidence status | Executable — demonstrated by smoke test with equivalent objective |
| Gap | If a prior Process Instance exists for this request, the Agent has no way to discover it by objective. Pre-recorded deferred gap. |

### Step 5: Execution Context Retrieval

| Attribute | Value |
|---|---|
| Actor | Agent (requests); Runtime (authoritative) |
| Action | `bridge.get_context()` → receives ExecutionContext with `process_state="initial"`, empty evidence/decisions/artifacts |
| Interface capability | Authoritative Execution Context retrieval |
| Existing mechanism | `bridge.get_context()` → `runtime.context.to_dict()` |
| Evidence status | Executable |
| Gap | None |

### Step 6: Engineering Investigation

| Attribute | Value |
|---|---|
| Actor | Agent |
| Action | `bridge.dispatch("start_investigation")`; inspects DBP repository files; finds Edit_Review_Form class; locates business_id field definition using Fields_Manager::SELECT |
| Interface capability | State transition (investigation); Agent-side investigation tooling |
| Existing mechanism | `bridge.dispatch("start_investigation")` for AESM state; Agent's file-reading tools for engineering work |
| Evidence status | State transition executable; investigation tooling available to Agent |
| Gap | None |

### Step 7: Requirements, Evidence, and Decision Handling

| Attribute | Value |
|---|---|
| Actor | Agent (proposes); Runtime (recognizes) |
| Action | Records findings as evidence: `bridge.dispatch("observe", {"observation": {"fact": "Edit_Review_Form::business_id uses SELECT", "source": "code_inspection", "recognition": {"recognized": True, "basis": "direct code inspection of Edit_Review_Form.php"}}})`. Proposes decision: `bridge.dispatch("recognize_decision", {"decision": {"description": "Change business_id from SELECT to POST_SELECT"}, "recognition": {"recognized": True, "basis": "POST_SELECT required for post-submission data access pattern"}})` |
| Interface capability | Evidence recording, decision recognition |
| Existing mechanism | `bridge.dispatch("observe", ...)`, `bridge.dispatch("recognize_decision", ...)` |
| Evidence status | Executable — demonstrated by smoke test with equivalent objective |
| Gap | Recognition guard requires `recognized: True` and `basis` but cannot verify the Agent actually inspected code rather than fabricating the observation |

### Step 8: Governed Execution Request

| Attribute | Value |
|---|---|
| Actor | Agent (requests); Runtime (authorizes) |
| Action | `bridge.dispatch("begin_implementation")` — Runtime checks: attached? active lifecycle? state=investigation? decisions exist? — all pass → state transitions to `implementation` |
| Interface capability | Runtime dispatch; lifecycle guard enforcement |
| Existing mechanism | `bridge.dispatch("begin_implementation")` → `Runtime.begin_implementation()` |
| Evidence status | Executable |
| Gap | None |

### Step 9: Runtime Execution

| Attribute | Value |
|---|---|
| Actor | Agent (performs work); Runtime (records) |
| Action | Agent modifies Edit_Review_Form.php in DBP repository; records artifact: `bridge.dispatch("record_artifact", {"artifact": {"type": "code_change", "path": "includes/Edit_Review_Form.php", "change": "business_id: SELECT → POST_SELECT"}})` |
| Interface capability | Artifact recording |
| Existing mechanism | `bridge.dispatch("record_artifact", ...)` → `Runtime.record_artifact()` |
| Evidence status | Executable |
| Gap | None for recording. DBP file change is Agent action outside Runtime scope — appropriate. |

### Step 10: Result and Evidence Recording

| Attribute | Value |
|---|---|
| Actor | Agent (reports result); Runtime (records) |
| Action | `bridge.dispatch("begin_verification")`; Agent performs DBP form testing; `bridge.dispatch("record_verification", {"result": {"passed": True, "method": "functional_test", "details": "Edit_Review_Form::business_id now uses POST_SELECT correctly"}})` |
| Interface capability | Verification recording |
| Existing mechanism | `bridge.dispatch("begin_verification")`, `bridge.dispatch("record_verification", ...)` |
| Evidence status | Executable |
| Gap | None |

### Step 11: Engineering Completion

| Attribute | Value |
|---|---|
| Actor | Agent (proposes); Runtime (recognizes) |
| Action | `bridge.dispatch("recognize_engineering_completion", {"completion": {"recognized": True, "basis": "Verification passed; business_id change confirmed functional"}})` — Runtime checks: active? state=verification? verification passed? — all pass → `engineering_completion=True`, state=`engineering_complete` |
| Interface capability | Engineering completion recognition |
| Existing mechanism | `bridge.dispatch("recognize_engineering_completion", ...)` |
| Evidence status | Executable |
| Gap | None |

### Step 12: Continuity, Reconsideration, or Completion

| Attribute | Value |
|---|---|
| Actor | Agent + Runtime |
| Action | If verification failed: `bridge.dispatch("reconsider", {"reason": {"description": "Verification failed: POST_SELECT not supported in current DBP version"}})` — Runtime rolls back to investigation state. If complete: Process Instance remains `active` unless explicit termination is requested. |
| Interface capability | Reconsideration, continuity |
| Existing mechanism | `bridge.dispatch("reconsider", ...)` — demonstrated; termination requires `apply_lifecycle_determination` (not bridged) |
| Gap | Agent-initiated termination path not currently bridged — Specification Decision Required |

### Trace Summary

The DBP request can be processed end-to-end through the existing bridge and Runtime mechanisms. All twelve steps have existing executable mechanisms or are appropriately Agent responsibilities. The two material gaps exposed by the trace:

1. Guidance delivery to Agent (Step 3): no automatic mechanism; Agent must find and read docs.
2. Objective-to-Process-Instance discovery (Step 4): pre-recorded deferred gap; Agent must create a new instance if ID is unknown.

---

## 7. Evidence Required to Demonstrate Actual AESM Participation

| Claim | Evidence required | Current evidence level |
|---|---|---|
| AESM documentation exists | `docs/` files inspectable | Satisfied |
| Agent was instructed to use AESM | Agent instruction mechanism exists and references AESM | Not satisfied — no `.agents/rules/` or equivalent in AESM repository |
| Agent actually used AESM guidance | Recording of Agent session showing AESM-guided behavior | Not demonstrated — no such recorded session |
| Agent interacted with the Runtime | Agent session called bridge/Runtime methods | Not demonstrated — smoke test is a Python script, not an AI Agent session |
| Runtime-authoritative state changed | ProcessStore files show Runtime-owned state mutations | Demonstrated by test suite (137/137 passing) |
| End-to-end AESM participation was demonstrated | AI Agent session: received guidance → created/attached Process Instance → performed work → dispatched Runtime operations → authoritative state persisted → fresh Agent resumed | Not demonstrated |

The current repository demonstrates through tests that:
- Runtime correctly implements PEM semantics.
- Bridge correctly delegates to Runtime.
- Continuity across bridge instances works.
- All recording, lifecycle, and verification operations function correctly.

The repository does not demonstrate an actual AI Agent participating in an AESM-governed engineering process. That demonstration requires the First Real Vertical Slice work unit.

---

## 8. Implementation Decision

### Assessment

The existing mechanisms — `docs/` files (AESM guidance), `bridge/agent_runtime_bridge.py` (process access, context access, dispatch, result return), `runtime/core/runtime.py` (authoritative state), `runtime/persistence/json_store.py` (persistence) — collectively satisfy the semantic minimum contract for all governed-execution capabilities. Three items are not satisfied:

1. **AESM guidance delivery mechanism.** Guidance content exists in `docs/` but is not automatically delivered to the Agent. This is a mechanism gap, not a semantic gap. The guidance content is complete; the issue is absence of a delivery channel (rules, skills, MCP, etc.).

2. **Objective-to-Process-Instance discovery.** Pre-recorded deferred gap. Not introduced by this work unit.

3. **Agent-initiated lifecycle transitions through the bridge.** Not bridged. Specification Decision Required before implementation.

### Decision: No Implementation Justified in This Work Unit

**Rationale:** The implementation rule gates are applied:

1. Requirement is established by the existing AESM model.
2. The existing `docs/` files and bridge together satisfy the semantic contract for governed-execution capabilities; the guidance delivery gap is a mechanism mapping question.
3. The Environment Mechanism Mapping work unit, not the Agent Guidance Interface work unit, is the correct scope for resolving which mechanism delivers guidance.
4. The smallest implementation is identifiable (creating `.agents/rules/` or equivalent).
5. Such implementation would not change AESM semantics.

Gates 2 and 3 fail: the guidance delivery mechanism question belongs to Environment Mechanism Mapping, which is explicitly prohibited from being started in this work unit.

The delivery mechanism gap is recorded as an explicit finding and passed to Environment Mechanism Mapping as its first input.

---

## 9. Gap Analysis: Complete Summary

| Capability | Status | Finding |
|---|---|---|
| AESM guidance content | Executable | `docs/` complete; all EPM/PEM/Agent semantics specified |
| AESM guidance delivery mechanism | Documentation only | No `.agents/rules/`, skill, or MCP server delivers guidance; belongs to Environment Mechanism Mapping |
| EPM binding in Process Instance | Evidence incomplete | `ProcessInstance.epm` field exists; populated as empty dict by default; no mechanism fills it |
| Process Instance creation | Executable | `bridge.create_process()` demonstrated |
| Process Instance recovery (known ID) | Executable | `bridge.attach()` demonstrated |
| Process Instance discovery (objective to ID) | Missing | Pre-recorded deferred gap |
| Execution Context retrieval | Executable | `bridge.get_context()` returns complete ExecutionContext |
| Evidence recording | Executable | `bridge.dispatch("observe", ...)` with recognition guard |
| Decision recognition | Executable | `bridge.dispatch("recognize_decision", ...)` with recognition guard |
| Investigation / implementation / verification state transitions | Executable | `bridge.dispatch(...)` for all three |
| Artifact recording | Executable | `bridge.dispatch("record_artifact", ...)` |
| Verification recording | Executable | `bridge.dispatch("record_verification", ...)` |
| Reconsideration | Executable | `bridge.dispatch("reconsider", ...)` |
| Engineering completion | Executable | `bridge.dispatch("recognize_engineering_completion", ...)` |
| Lifecycle observation | Executable | All bridge responses include `process_instance.lifecycle` |
| Lifecycle transition (bridged) | Specification Decision Required | `apply_lifecycle_determination` not routed through bridge; separate authorization required |
| Continuity (known ID) | Executable | `bridge.attach()` across bridge instances — demonstrated |
| Process Instance ID delivery to fresh Agent | Missing | No delivery mechanism; deferred gap |
| End-to-end AI Agent participation | Missing | Not demonstrated; requires First Real Vertical Slice |

---

## 10. What Remains Outside This Work Unit

The following were not started and remain out of scope:

- Environment Mechanism Mapping — determining which Execution Environment mechanisms satisfy each contract capability
- First Real Vertical Slice — an actual AI Agent end-to-end execution
- DBP implementation — the Edit_Review_Form change was traced but not implemented
- Agent-initiated lifecycle bridge extension — specification decision required first
- Process Instance discovery mechanism design — separately authorized decision required
- Runtime changes — none required or made
- AESM semantic changes — none required or made

---

## 11. Next Gate

The next authorized work unit is **Environment Mechanism Mapping** — map each contract capability established here to a candidate Execution Environment mechanism, with explicit rationale for what belongs in persistent instructions, skills, MCP/tools, persisted context, or Runtime control.

Primary inputs to Environment Mechanism Mapping from this work unit:

1. The complete capability matrix in section 9 above.
2. The specific gap: AESM guidance delivery to the Agent has no current mechanism.
3. The specific gap: Process Instance ID delivery to a fresh Agent has no current mechanism.
4. The established contract: bridge satisfies process access, context access, dispatch, and result return.
5. The deferred question: EPM binding should be explicitly populated in Process Instance creation.
6. The specification decision required: Agent-initiated lifecycle bridge extension scope.

---

## 12. Repository Integrity

```
git status --short:  (clean — no output)
git diff --check:    (clean — no output)
```

Files modified by this work unit:
- `execution/AGENT-GUIDANCE-INTERFACE.md` — created (this file)
- `IMPLEMENTATION_PLAN.md` — updated (plan reconciliation only)

No Runtime, bridge, test, or other source files were modified.
No downstream work was started.
No commits were made.
