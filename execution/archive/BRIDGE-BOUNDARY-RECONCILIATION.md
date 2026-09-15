# Bridge Boundary Reconciliation

## 1. Purpose and Scope

This artifact reconciles the previously established Agent–Runtime bridge boundary ([`AGENT-RUNTIME-EXECUTION-BRIDGE-INSPECTION.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/AGENT-RUNTIME-EXECUTION-BRIDGE-INSPECTION.md)) with the latest Runtime API inspection evidence ([`RUNTIME-API-INSPECTION.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/RUNTIME-API-INSPECTION.md)).

The central question is whether the previously established bridge boundary remains semantically correct, with particular attention to Process Instance identification and discovery.

**Scope boundary:** This artifact produces analytical findings only. No source code, Runtime API, test, bridge implementation, or normative documentation is created or modified.

---

## 2. Evidence Base

### Primary sources inspected (in evidence hierarchy order)

**1. Actual Runtime source (highest authority):**

| File | Evidence |
|---|---|
| [`runtime/core/models.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/models.py) | `ProcessInstance` and `ExecutionContext` dataclasses — 21 total fields on EC |
| [`runtime/core/runtime.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py) | `Runtime` class — 14 public methods, `create_process`, `attach`, state transitions, recording, lifecycle, `stop` |
| [`runtime/core/store.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/store.py) | `ProcessStore` — persistence with rollback, no listing/discovery capability |
| [`runtime/persistence/json_store.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/persistence/json_store.py) | Atomic file persistence primitives |
| [`runtime/core/__init__.py`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/__init__.py) | Public API exports |

**Test suite:** 88/88 tests pass (freshly executed 2026-09-15, 0.97s).

**2. Existing inspection artifacts:**

| Artifact | Role |
|---|---|
| [`AGENT-RUNTIME-EXECUTION-BRIDGE-INSPECTION.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/AGENT-RUNTIME-EXECUTION-BRIDGE-INSPECTION.md) | Previously established bridge boundary |
| [`RUNTIME-API-INSPECTION.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/RUNTIME-API-INSPECTION.md) | Latest Runtime API evidence |

**3. Normative documentation:**

| Document | Relevance |
|---|---|
| [`docs/07-Runtime-and-Conformance.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/07-Runtime-and-Conformance.md) | Runtime responsibilities, Process Instance discovery ownership, conformance |
| [`docs/05-Process-Instance-and-Execution-Context.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/05-Process-Instance-and-Execution-Context.md) | Discovery/recovery/resumption distinction, continuity invariant |
| [`docs/08-Continuity-Traceability-and-Reconsideration.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/08-Continuity-Traceability-and-Reconsideration.md) | Continuity across Agents and Environments |
| [`IMPLEMENTATION_PLAN.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/IMPLEMENTATION_PLAN.md) | Controlled work sequence and canonical bridge boundary |

**Runtime source verification:** All claims about Runtime behavior in this artifact are derived from direct inspection of the source files listed above and freshly executed test evidence. No claim relies solely on inspection artifact summaries without source verification.

---

## 3. Previously Established Boundary

The bridge inspection ([`AGENT-RUNTIME-EXECUTION-BRIDGE-INSPECTION.md` §16](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/AGENT-RUNTIME-EXECUTION-BRIDGE-INSPECTION.md)) established a four-part **complete operational boundary**:

| # | Responsibility | Description |
|---|---|---|
| 1 | **Process Instance initiation / identification** | Create a Process Instance when appropriate; identify/discover an existing relevant Process Instance when appropriate |
| 2 | **Execution Context presentation** | Obtain and present the authoritative Execution Context to the Agent |
| 3 | **Runtime operation dispatch** | Submit Agent contributions or requests to the Runtime |
| 4 | **Runtime state/result return** | Return authoritative Runtime state/results to the Agent |

This was subsequently codified in [`IMPLEMENTATION_PLAN.md` §Canonical Agent–Runtime Bridge Boundary](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/IMPLEMENTATION_PLAN.md) using slightly different labels:

1. **Process Instance access** — Create or discover the relevant persistent Process Instance.
2. **Execution Context access** — Obtain the authoritative Execution Context and make its current state available to the Agent.
3. **Runtime dispatch** — Dispatch already-supported Runtime operations on behalf of the Agent.
4. **Authoritative result/state return** — Return the authoritative Runtime result and resulting state to the Agent.

**Observed Evidence:** Both formulations explicitly include Process Instance discovery as part of responsibility 1. The bridge inspection's §5 explicitly classified "Process Instance discovery without UUID" as **Implementation Gap — Semantically Required**.

---

## 4. Reconciliation Findings

### 4.1 Latest Runtime API Inspection Adapter Surface

The Runtime API Inspection ([`RUNTIME-API-INSPECTION.md` §9](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/RUNTIME-API-INSPECTION.md)) defined the adapter surface as four operations:

| # | Adapter Operation | Maps to Bridge Responsibility |
|---|---|---|
| 1 | `create_process(objective)` | Process Instance access (creation path) |
| 2 | `attach(process_instance_id)` | Process Instance access (recovery path) |
| 3 | `get_context()` | Execution Context access |
| 4 | `dispatch(operation, params)` | Runtime dispatch |

Result/state return was **eliminated as a separate operation** and integrated into the return values of operations 1–4.

### 4.2 Treatment of Discovery in the Runtime API Inspection

The Runtime API Inspection explicitly classified objective-to-Process-Instance discovery as:

- **Missing** from the current Runtime ([§3.C](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/RUNTIME-API-INSPECTION.md), [§11](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/RUNTIME-API-INSPECTION.md))
- A **separate architectural/design decision** that does not block bridge implementation design for the first vertical slice
- Architecturally **above or alongside** the adapter, not inside it

### 4.3 Nature of the Difference

**Established Conclusion:** The difference between the two artifacts is a legitimate distinction between **complete bridge responsibility** and **Runtime-facing adapter API**, not an unintended reduction of the bridge boundary.

**Evidence:**

1. The bridge inspection established what the *complete operational boundary* must accomplish. Its responsibility 1 explicitly includes both creation and discovery.

2. The Runtime API Inspection established what the *adapter's four operations map to in the current Runtime*. The current Runtime provides `create_process()` and `attach(pid)` but no discovery capability. The adapter surface necessarily reflects only what the Runtime can currently support.

3. The Runtime API Inspection did not claim that discovery is unnecessary. It classified discovery as **Missing / Unresolved** and stated it is a "separate architectural/design decision" ([§11](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/RUNTIME-API-INSPECTION.md)).

4. The bridge inspection's complete boundary (responsibility 1 = "create or discover") is not contradicted by the adapter surface (`create_process` + `attach`). Rather, `create_process` + `attach` are the currently implementable subset of responsibility 1. Discovery would be an additional mechanism that feeds into `attach` by resolving an identifier.

**Classification:** This is a **factual** difference — the two artifacts describe different levels of abstraction (complete boundary vs. current adapter contract). There is no semantic disagreement or architectural contradiction.

### 4.4 Source Agreement/Disagreement Table

| Claim | Bridge Inspection | Runtime API Inspection | Runtime Source | Normative Docs | Agreement |
|---|---|---|---|---|---|
| Bridge needs 4 responsibilities | Yes (§16) | Yes (§9, responsibility 5 eliminated) | N/A | Yes (IMPL_PLAN §Canonical) | **Agree** |
| Discovery is part of the complete boundary | Yes (§5, §16) | Yes (§11 — classified as Missing) | No discovery in source | Yes (docs/07 §PI discovery) | **Agree** |
| Discovery is absent from current Runtime | Yes (§5) | Yes (§3.C, §11) | Confirmed — no discover/list/search | N/A | **Agree** |
| Current adapter surface = 4 operations | N/A (not its scope) | Yes (§9) | Consistent with Runtime API | N/A | **Consistent** |
| Discovery is a separate design decision | Not explicit | Yes (§11) | N/A | Partially — see §6 | **Requires analysis** |

---

## 5. Process Instance Discovery

### 5.1 Known Process Instance Identity

**Situation:** The Agent already possesses a valid Process Instance ID (UUID).

**What the current Runtime supports (Observed Evidence):**

`Runtime.attach(process_instance_id)` ([`runtime.py:48–51`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/runtime.py#L48-L51)) loads the `ProcessInstance` and `ExecutionContext` from the `ProcessStore` by UUID. This path is fully implemented, tested, and demonstrated across Runtime instances.

**Established Conclusion:** Known-ID recovery is fully supported. The bridge adapter can serve this case through `attach(process_instance_id)` without any additional mechanism.

### 5.2 Ordinary Engineering Request (No Initial Process Instance ID)

**Situation:** A human gives the Agent a request such as "Implement feature X." The Agent does not initially possess a Process Instance ID.

**What must conceptually happen (Architectural Interpretation):**

1. **Determine whether an appropriate Process Instance already exists.** This requires searching or querying against some criterion (engineering objective, repository context, or other identifying information). The current Runtime and ProcessStore provide no mechanism for this. The persistence store uses UUID-based directories (`process-instance/<uuid>/`) with no index, registry, or search capability.

2. **If found: identify the relevant Process Instance.** This means resolving the search result to a specific UUID. Once a UUID is obtained, `attach(pid)` can be used.

3. **Recover its authoritative Execution Context.** `attach(pid)` loads both `ProcessInstance` and `ExecutionContext` from persistent state. This is supported.

4. **If not found: determine that a new Process Instance must be created.** This is a decision that follows from the discovery result (no match found). `create_process(objective)` then creates the new instance.

**Established Conclusion:** The gap is specifically in step 1 — there is no mechanism to search for or match against existing Process Instances. Steps 2–4 are all supported by existing Runtime capabilities once the UUID is known or a creation decision is made.

### 5.3 No Matching Process Instance

**Situation:** Discovery determines that no suitable existing Process Instance exists.

**What the bridge must conceptually do (Architectural Interpretation):**

The bridge (or the mechanism feeding it) must determine that creation is appropriate and invoke `create_process(objective)`. The Runtime itself does not make this determination — `create_process` always creates a new instance without checking for existing ones.

**Established Conclusion:** The creation path is fully supported. The decision of *when* to create vs. *when* to attach is a bridge-level or pre-bridge-level concern, not a Runtime concern. The Runtime correctly provides both `create_process` and `attach` as separate, independent operations.

---

## 6. Discovery Ownership

### 6.1 Normative Assignment

**Observed Evidence — Canonical Documentation:**

[`docs/07-Runtime-and-Conformance.md` lines 46–70](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/07-Runtime-and-Conformance.md#L46-L70) explicitly states:

> "Process Instance discovery is a Runtime responsibility."

> "The Runtime is responsible for resolving an existing Process Instance when sufficient identification or discovery information is available. The Execution Environment may provide access, storage, filesystem, network, API, or other capabilities used to perform discovery, but those capabilities do not make the Execution Environment the semantic owner of Process Instance discovery."

> "Discovery is an implementation responsibility of the Runtime and does not require a particular storage mechanism, search strategy, identifier, or API shape."

> "AESM does not require a specific `discover()` API."

**Established Conclusion:** The normative AESM documentation unambiguously assigns **semantic ownership** of Process Instance discovery to the Runtime. This is not a recommendation — it is a conformance requirement.

### 6.2 Distinction: Semantic Ownership vs. Mechanism Location vs. Adapter Exposure

| Dimension | Definition | Normative Assignment |
|---|---|---|
| **Semantic ownership** | Which layer is responsible for the meaning and authority of discovery | **Runtime** — explicitly assigned by docs/07 |
| **Mechanism location** | Where code or integration logic may physically perform the lookup | **Flexible** — Runtime may use files, databases, indexes, registries, etc. The Execution Environment may provide access capabilities. |
| **Adapter exposure** | Whether the bridge needs to expose discovery as an operation | **Not prescribed** — AESM does not require a specific `discover()` API |

**Architectural Interpretation:** The Runtime API Inspection's treatment of discovery as "above or alongside the adapter" is compatible with the normative model *only if* semantic ownership remains with the Runtime. A mechanism physically located outside the Runtime (e.g., an index file maintained by the adapter) does not automatically move semantic ownership outside the Runtime — provided that the Runtime remains the authority for resolving the discovered identity.

### 6.3 Candidate Ownership Arrangements

#### A. Runtime-owned discovery (via new Runtime/ProcessStore API)

| Criterion | Assessment |
|---|---|
| Consistency with AESM authority model | **Fully consistent** — directly satisfies docs/07 |
| Process Instance authority | Runtime retains authority over identity |
| Persistence authority | ProcessStore retains authority over persistence |
| Continuity | Discovery result is authoritative |
| Risk of duplicate state | Low — single authority |
| Risk of bypassing Runtime governance | None |
| EPM/PEM/Runtime/EE separation | Preserved |
| Whether new Runtime API is justified | Requires analysis — see §9 |

#### B. Bridge-adapter-owned discovery (adapter maintains an index)

| Criterion | Assessment |
|---|---|
| Consistency with AESM authority model | **Conditionally consistent** — only if semantic authority is delegated back to Runtime for resolution. The adapter would perform lookup; the Runtime would validate the discovered identity via `attach()`. |
| Process Instance authority | Runtime retains authority via `attach()` |
| Persistence authority | **Risk** — the adapter index is a second persistence location for Process Instance metadata (at minimum, objective-to-UUID mapping). This metadata must remain consistent with ProcessStore state. |
| Continuity | Depends on index durability and consistency |
| Risk of duplicate state | **Moderate** — the index duplicates information already present in `process.json` files |
| Risk of bypassing Runtime governance | Low if adapter only reads the index and always resolves through `attach()` |
| EPM/PEM/Runtime/EE separation | **Requires care** — the adapter must not become a semantic authority for Process Instance identity |
| Whether new Runtime API is justified | No — uses existing `attach()` |

#### C. Execution-Environment-owned discovery

| Criterion | Assessment |
|---|---|
| Consistency with AESM authority model | **Inconsistent** — docs/07 explicitly states that EE capabilities "do not make the Execution Environment the semantic owner of Process Instance discovery" |
| All other criteria | Not evaluated — arrangement is excluded by normative constraint |

#### D. Split responsibility (Runtime owns semantics; adapter/EE provides access mechanism)

| Criterion | Assessment |
|---|---|
| Consistency with AESM authority model | **Consistent** — this is explicitly contemplated by docs/07: "The Execution Environment may provide access, storage, filesystem, network, API, or other capabilities used to perform discovery" while the Runtime remains semantically responsible |
| Process Instance authority | Runtime retains via `attach()` |
| Persistence authority | Depends on whether the access mechanism introduces new persistence |
| Continuity | Depends on mechanism durability |
| Risk of duplicate state | Lower than B if the mechanism reads existing ProcessStore state rather than maintaining a separate index |
| Risk of bypassing Runtime governance | Low if mechanism only provides discovery information and resolution goes through Runtime |
| EPM/PEM/Runtime/EE separation | Preserved if semantic ownership remains with Runtime |
| Whether new Runtime API is justified | Depends — a `ProcessStore.list()` or similar read-only capability could serve the access mechanism without changing Runtime semantics |

### 6.4 Discovery Ownership Determination

**Established Conclusion:** Semantic ownership of Process Instance discovery belongs to the Runtime per the normative AESM model. This is not overridden by the current implementation's absence of a discovery mechanism.

**Architectural Interpretation:** The most AESM-consistent arrangements are A (Runtime-owned via new API) or D (split responsibility with Runtime retaining semantic ownership). Arrangement B (adapter-maintained index) is conditionally acceptable but introduces duplicate-state risk. Arrangement C (EE-owned) is excluded by the normative model.

**Recommendation:** The specific arrangement (A vs. D) is an implementation design decision that should be resolved during Environment Mechanism Mapping or Bridge Implementation Design. Both are architecturally valid. The constraint is: **semantic ownership must remain with the Runtime regardless of mechanism location.**

---

## 7. Continuity Implications

### 7.1 Conversational Dependency

**Situation:** The Agent can continue only because the previous conversation remembers or supplies the Process Instance ID.

**Assessment (Established Conclusion):** This is a **continuity weakness** per the AESM specification. [`docs/05` line 157](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/05-Process-Instance-and-Execution-Context.md#L157): "authoritative continuation information must not depend on transient conversation memory." [`docs/08` line 115](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/docs/08-Continuity-Traceability-and-Reconsideration.md#L115): "Agent B should not need Agent A's private conversational memory to establish the authoritative process state."

If the only way to obtain the Process Instance UUID is from the previous conversation, then continuity depends on conversation history. This violates the AESM continuity invariant.

### 7.2 Persistent Non-Conversational Identification

**Situation:** An identifier is supplied through a persistent mechanism — for example, a repository artifact, persistent mapping, index, or other durable mechanism.

**Assessment (Architectural Interpretation):** A persistent, non-conversational mechanism *can* satisfy the continuity objective, provided:

1. **Reliability:** The mechanism reliably identifies the *correct* Process Instance, not merely any Process Instance. If multiple Process Instances exist, the mechanism must resolve to the appropriate one.
2. **Durability:** The mechanism survives the same events that Process Instance state survives (Agent session loss, IDE closure, Environment replacement).
3. **Consistency:** The identifier in the mechanism corresponds to a valid, existing Process Instance in the ProcessStore.
4. **Non-dependency on conversation:** The mechanism must be discoverable by a fresh Agent without prior conversational context.

A simple file containing a UUID (e.g., `.aesm/current-process-instance`) satisfies criteria 2–4 but may fail criterion 1 in scenarios with multiple concurrent Process Instances for different objectives.

**Established Conclusion:** Persistent non-conversational identification is *necessary but may not be sufficient* without additional matching logic (e.g., objective matching, repository-context matching). Its sufficiency depends on the operational scenario:

- **Single active Process Instance per repository context:** A persistent pointer is likely sufficient.
- **Multiple concurrent Process Instances:** A persistent pointer alone is insufficient; some form of objective/context matching is needed.

### 7.3 Objective/Context-Based Discovery

**Situation:** The Agent identifies the relevant Process Instance from the engineering objective or other persistent context without conversational memory or manually supplied UUID.

**Assessment (Architectural Interpretation):** This is the strongest continuity posture. It means that when a human says "Continue working on feature X," a fresh Agent can:

1. Inspect the engineering objective or repository context.
2. Search for Process Instances whose objective matches.
3. Identify the correct one.
4. Attach and recover authoritative state.

This capability is **not strictly required** for every operational scenario. It is required when:

- The human does not explicitly provide a UUID.
- Multiple Process Instances may exist.
- The Agent has no prior conversational context.

For the first vertical slice, the Runtime API Inspection correctly noted that explicit UUID provision or new creation suffices. However, for the general operational flow described in the implementation objective (where a human gives an ordinary engineering request), objective-based discovery is the mechanism that prevents conversational dependency.

**Established Conclusion:** Objective/context-based discovery is not required for the first vertical slice's happy path, but it *is* required for the general AESM continuity objective. The complete operational boundary must include it even if the first adapter implementation defers it.

### 7.4 Core Continuity Question

> **Can a later Agent reliably enter or recover the correct AESM Process Instance through a persistent mechanism while preserving Process Instance and Execution Context authority?**

**Current answer (Established Conclusion):** **Not fully.** The Runtime provides the *recovery* mechanism (`attach(pid)`), and Process Instance state is durable. However, no *discovery* mechanism exists to help a fresh Agent identify the correct Process Instance without prior conversational context or an externally provided UUID. The gap is specifically in the identification/discovery step, not in the recovery or authority preservation steps.

---

## 8. Complete Boundary Minimality Test

The omission test is applied to the **complete Agent–Runtime operational boundary**, not merely to the four adapter operations.

### 8.1 Process Instance Creation

> **If omitted:** No new engineering process can begin. The Agent cannot create a Process Instance for a new engineering request.

**Verdict:** **Cannot be omitted.** No other capability provides creation. `attach` requires an existing PI.

### 8.2 Process Instance Identification/Discovery

> **If omitted:** When the Agent does not already possess a UUID, it cannot determine which existing Process Instance (if any) corresponds to the current engineering request. Consequences:
>
> - Every new Agent session for the same objective creates a duplicate Process Instance.
> - Continuity across sessions depends on conversational memory or manually supplied UUIDs.
> - The AESM continuity invariant is violated in the general case.

**Verdict:** **Cannot be omitted from the complete operational boundary.** Even if the first vertical slice can operate without it, the boundary is incomplete without this capability.

**Can discovery be implemented through a mechanism outside the Runtime-facing adapter?** Yes — the normative model explicitly permits discovery through files, indexes, or other mechanisms. However, even when physically located outside the adapter, discovery remains *semantically part of the complete operational boundary* because:

1. Without it, the boundary cannot fulfill responsibility 1 (Process Instance access) in the general case.
2. Without it, the continuity invariant is not satisfied in the general case.
3. The normative model assigns discovery to the Runtime's *semantic* responsibility regardless of mechanism location.

### 8.3 Known-ID Recovery

> **If omitted:** The Agent cannot resume an existing Process Instance. Continuation after session loss is impossible even with a known UUID.

**Verdict:** **Cannot be omitted.** No other capability provides recovery. `create_process` creates new PIs, not recovers existing ones.

### 8.4 Execution Context Retrieval/Presentation

> **If omitted:** The Agent has no way to obtain the current authoritative state. It cannot determine process state, evidence, decisions, pending work, or any other operational information.

**Verdict:** **Cannot be omitted.** `create_process` and `attach` establish context internally but the Agent must be able to read it.

### 8.5 Runtime Operation Dispatch

> **If omitted:** Agent contributions (evidence, decisions, artifacts, verification) cannot reach authoritative state. The Agent performs engineering work but none of it becomes authoritative.

**Verdict:** **Cannot be omitted.** No other capability provides dispatch.

### 8.6 Runtime State/Result Return

> **If omitted:** The Agent has no feedback from the Runtime. It cannot determine whether an operation succeeded or what the resulting state is.

**Verdict:** **Cannot be omitted.** The Runtime API Inspection correctly integrated this into the return values of operations 1–4 rather than making it a separate operation, but the *capability* must exist.

### 8.7 Minimality Summary

| Capability | Omission Result | In Adapter Surface? | In Complete Boundary? |
|---|---|---|---|
| Process Instance creation | Fails — no new PI | Yes (`create_process`) | Yes |
| Process Instance discovery | Fails continuity in general case | **No** (deferred) | **Yes** |
| Known-ID recovery | Fails continuation | Yes (`attach`) | Yes |
| Execution Context retrieval | Fails state visibility | Yes (`get_context`) | Yes |
| Runtime operation dispatch | Fails authoritativeness | Yes (`dispatch`) | Yes |
| Runtime state/result return | Fails feedback | Yes (integrated) | Yes |

**Established Conclusion:** The complete operational boundary requires all six capabilities. The adapter surface currently covers five (with state/result return integrated). Discovery is the one capability that is in the complete boundary but absent from the adapter surface and the current Runtime.

---

## 9. Runtime API Implications

> **Does this reconciliation justify adding a Process Instance discovery API to the Runtime?**

### Analysis

**Evidence hierarchy evaluation:**

1. **Actual Runtime source:** The Runtime and ProcessStore provide no discovery mechanism. No `list()`, `search()`, `find()`, `discover()`, or index capability exists. ProcessStore directories are named by UUID with no cross-referencing. This is confirmed by grep search of the entire `runtime/` directory — zero results for "discover", "search", "find", "lookup", or "index" in Python source files.

2. **Normative documentation:** Discovery is a Runtime *semantic* responsibility (docs/07 line 48). However, "AESM does not require a specific `discover()` API" (docs/07 line 68). The Runtime may implement discovery "through files, databases, services, indexes, identifiers, registries, or other suitable mechanisms" (docs/07 line 70).

3. **Continuity requirement:** The complete boundary minimality test (§8.2) establishes that discovery cannot be omitted from the operational boundary without violating the continuity invariant in the general case.

4. **Complete-boundary omission test:** Discovery is required. But the normative model explicitly permits non-API implementations.

### Possible Conclusions Evaluated

**A. Discovery requires a new Runtime API (e.g., `Runtime.discover(objective)`).**

Not necessarily justified. The normative model explicitly does not require a specific `discover()` API. A `ProcessStore.list()` that returns existing Process Instance summaries would be a smaller, more defensible addition that provides the *access mechanism* for discovery without embedding discovery *logic* in the Runtime.

**B. Discovery requires a Runtime *capability* (not necessarily a `discover()` API).**

Justified. The Runtime is semantically responsible for discovery. The current Runtime provides no capability — not even a read-only listing — that could support discovery. Some form of Runtime-layer capability is needed, even if it is as minimal as a read-only listing of existing Process Instances and their objectives.

**C. Discovery can be exposed through an adapter while semantic authority remains with Runtime.**

Compatible with the normative model. The adapter could maintain an index or scan the ProcessStore directory structure, then resolve through `Runtime.attach()`. Semantic authority remains with the Runtime because `attach()` validates the discovered identity. However, this arrangement introduces duplicate-state risk if the adapter maintains its own index (see §6.3 arrangement B).

**D. Further architectural evidence/decision is required.**

Yes. The specific mechanism (Runtime API vs. ProcessStore listing vs. adapter-level scanning vs. persistent index) is an implementation design decision that affects:

- Whether the Runtime source needs modification (adding a `list()` or equivalent).
- Whether the adapter introduces duplicate persistence.
- Whether the mechanism is environment-dependent.

This decision is appropriately made during Environment Mechanism Mapping or Bridge Implementation Design, not during this reconciliation.

### Runtime API Implication Determination

**Established Conclusion:** This reconciliation establishes that:

1. **Discovery is semantically required** by the complete operational boundary and the AESM continuity invariant.
2. **Semantic ownership** of discovery belongs to the Runtime per the normative model.
3. **A new `discover()` API is not necessarily required** — the normative model explicitly permits other mechanisms.
4. **Some form of Runtime-layer or ProcessStore-layer capability** is likely needed to support discovery without introducing duplicate state, but the specific form is an implementation decision.
5. **The decision of which mechanism to use** should be made during Environment Mechanism Mapping or Bridge Implementation Design with explicit consideration of the constraints identified in §6.

---

## 10. Minor Verification: Execution Context Field Count

**Claim in [`RUNTIME-API-INSPECTION.md` §4 line 181](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/RUNTIME-API-INSPECTION.md):** "It contains all 18 semantic fields."

**Actual `ExecutionContext` definition** ([`models.py:38–74`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/runtime/core/models.py#L38-L74)):

- **Total declared dataclass fields:** 21
- **Freshly verified** by programmatic inspection of `dataclasses.fields(ExecutionContext)`.

**Field classification:**

| Category | Fields | Count |
|---|---|---|
| **Identity/objective** | `process_instance_id`, `engineering_objective` | 2 |
| **Process/execution state** | `process_state`, `execution_mode` | 2 |
| **Engineering state** | `requirements`, `constraints`, `evidence`, `assumptions`, `risks`, `candidate_solutions`, `engineering_decisions`, `decision_gates`, `artifacts`, `verification`, `unresolved_matters`, `pending_execution`, `execution_determination`, `failure_uncertainty`, `engineering_completion` | 15 |
| **Metadata** | `version`, `updated_at` | 2 |
| **Total** | | **21** |

**Discrepancy:** The inspection's table (§4) actually lists 20 rows (it omits `updated_at`). The text claims "18 semantic fields." If "semantic fields" excludes `version` and `updated_at` (metadata), the count is 19, not 18.

**Assessment:** Minor counting discrepancy. The table in RUNTIME-API-INSPECTION.md is substantively accurate (it lists all fields used for engineering and process semantics). The "18 semantic fields" text appears to be an off-by-one relative to the 19 non-metadata fields, and the table omits `updated_at`.

**Follow-up item:** Record this discrepancy for correction in a future update to `RUNTIME-API-INSPECTION.md`. This discrepancy does not affect any architectural determination.

---

## 11. Impact on Implementation Plan

### Current Forward Work Sequence

[`IMPLEMENTATION_PLAN.md` §Forward Work Sequence](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/IMPLEMENTATION_PLAN.md):

```
[x] Controlled Plan Reconciliation
[x] Bridge Implementation Authorization (PASSED)
[ ] Runtime API Inspection       ← current position
[ ] Minimal Agent–Runtime Bridge Implementation
[ ] Bridge Behavioral Validation
[ ] DBP Real-Request Execution
[ ] Context-Loss / Fresh-Agent Validation
[ ] Reconciliation and Decision Gate
```

**Note:** The `IMPLEMENTATION_PLAN.md` still shows Runtime API Inspection as `[ ]` (not started). The Runtime API Inspection has actually been completed (artifact exists at [`execution/RUNTIME-API-INSPECTION.md`](file:///Volumes/DATA/Workspace/Development/MAMP/htdocs/wordpress-plugins/AI-Assisted-Engineering-System-Model/execution/RUNTIME-API-INSPECTION.md)). This Bridge Boundary Reconciliation is a step that was not explicitly listed in the forward work sequence but logically follows from the Runtime API Inspection.

### Impact Assessment

**Does the reconciliation affect the planned sequence?**

The reconciliation establishes that:

1. The four-part adapter surface (`create_process`, `attach`, `get_context`, `dispatch`) is correct and sufficient for the first vertical slice.
2. Process Instance discovery is absent from both the adapter surface and the Runtime, but is part of the complete operational boundary.
3. Discovery's semantic ownership belongs to the Runtime per the normative model.
4. A decision about the discovery mechanism is required before or during bridge implementation.

**Sequence assessment (Architectural Interpretation):**

The sequence **Runtime API Inspection → Bridge Boundary Reconciliation → Environment Mechanism Mapping → Bridge Implementation Design → Explicit Implementation Authorization → Bridge Implementation → End-to-End DBP Validation** remains appropriate, with one addition:

- **Environment Mechanism Mapping** should include evaluation of discovery mechanism candidates (ProcessStore listing, adapter index, directory scanning, persistent pointer, etc.) alongside the transport/integration mechanism evaluation.
- The discovery mechanism decision does **not** need to be resolved before Environment Mechanism Mapping begins. It is appropriately part of that work.

**No sequence change is required.** Environment Mechanism Mapping is the correct next step after this reconciliation. The discovery question should be explicitly included as a mapping concern.

### What This Reconciliation Does NOT Authorize

- Bridge implementation
- Discovery mechanism implementation
- Runtime API additions
- ProcessStore modifications
- Environment Mechanism Mapping execution

---

## 12. Follow-up Decisions / Evidence

### Required before Bridge Implementation Design

| Item | Type | Description |
|---|---|---|
| **Discovery mechanism selection** | Architectural Decision | Choose between: (a) ProcessStore listing capability, (b) adapter-level directory scanning, (c) adapter-maintained index, (d) persistent pointer file, (e) other mechanism. Must preserve Runtime semantic ownership of discovery per docs/07. |

### Follow-up items (not blocking)

| Item | Type | Description |
|---|---|---|
| **RUNTIME-API-INSPECTION.md field count correction** | Minor Factual | The text claims "18 semantic fields"; actual count is 19 non-metadata fields (21 total). The table omits `updated_at`. Record for future correction. |
| **IMPLEMENTATION_PLAN.md status update** | Plan Maintenance | The forward work sequence should reflect completed Runtime API Inspection and this reconciliation. Not modified during this task per scope constraint. |

---

## 13. Final Determination

The previously established four-part Agent–Runtime bridge boundary remains **semantically correct**. The adapter surface defined by the Runtime API Inspection (`create_process`, `attach`, `get_context`, `dispatch`) is a correct and sufficient implementation of the boundary for the first vertical slice.

Process Instance discovery is confirmed as part of the **complete operational boundary** (responsibility 1) and is semantically owned by the Runtime per normative documentation. It is absent from both the current Runtime implementation and the adapter surface. This absence does not invalidate the boundary — it identifies a capability that must be addressed before the bridge can satisfy the complete boundary in the general case.

The discovery mechanism is an architectural decision that should be resolved during Environment Mechanism Mapping or Bridge Implementation Design, with the constraint that semantic ownership must remain with the Runtime.

No unresolved architectural contradiction, boundary reduction, or normative violation was identified.

`BOUNDARY CONFIRMED`
