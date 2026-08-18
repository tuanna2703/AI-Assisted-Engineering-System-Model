# Phase 5 Contract-to-Protocol Traceability Matrix

**Phase:** Phase 5 — Machine-Readable Agent Protocol  
**Status:** DRAFT — Construction Review  
**Canonical Contract:** `specifications/Agent Execution Contract.md`  
**Protocol:** `specifications/Machine-Readable Agent Protocol.md`  
**Schema:** `schemas/machine-readable-agent-protocol.schema.json`  
**Date:** 2026-08-18

---

## 1. Purpose

This matrix verifies that the Machine-Readable Agent Protocol represents the material interaction semantics established by the frozen Agent Execution Contract without creating new authority.

The matrix is a review artifact. It does not replace either the Contract or the Protocol specification.

---

## 2. Traceability Rules

Each material Contract concept shall be classified as:

- **Direct** — represented explicitly by protocol structure or operation;
- **Indirect** — represented through references or shared governing semantics;
- **Non-Protocol** — intentionally remains outside the protocol because it is authoritative semantic state or implementation behavior;
- **Pending** — representation requires further Phase 5 construction.

A missing direct representation is not automatically a defect. The matrix must document why the concept does not belong directly in the protocol.

---

## 3. Matrix

| Contract Concept | Protocol Representation | Classification | Authority Preserved | Status |
|---|---|---|---|---|
| Agent as Participant | `sender` / `recipient` participant type | Direct | Agent remains distinct from Runtime | Covered |
| Agent ≠ Runtime | participant type enum and protocol invariants | Direct | Yes | Covered |
| Agent capability ≠ authority | operation classification + governing recognition boundary | Indirect | Protocol cannot grant authority | Covered |
| Agent output ≠ authoritative state | payload + recognition boundary | Indirect | Receipt does not mutate state | Covered |
| Observation | `observation_report` / payload kind `observation` | Direct | Observation is non-authoritative | Covered |
| Participant Input | `participant_input` | Direct | Not automatic mutation | Covered |
| Candidate Contribution | `candidate_contribution` | Direct | Remains candidate | Covered |
| Proposal | `proposal` | Direct | Proposal ≠ authorization/decision | Covered |
| Execution request | `execution_request` | Direct | Runtime applies PEM control | Covered |
| Execution Result | `execution_result` | Direct | Result ≠ determination | Covered |
| Verification Result | `verification_result` | Direct | Result does not self-authorize | Covered |
| Failure / Uncertainty | `failure_uncertainty` / `failure` | Direct | Material uncertainty preserved | Covered |
| Reconsideration | `reconsideration` | Direct | History preserved | Covered |
| Process Instance | `process_instance_ref` | Direct | Reference only | Covered |
| Execution Context | `execution_context_ref` | Indirect | Message does not become context | Covered |
| Execution Trace | `trace_ref` | Direct | Supports reconstruction | Covered |
| Recognition | Runtime-controlled interpretation/recognition boundary | Non-Protocol authority | Protocol cannot establish recognition | Covered |
| Authorized State Mutation | mutation-relevant classification and Runtime boundary | Non-Protocol authority | Mutation remains Runtime/PEM controlled | Covered |
| Engineering Decision | proposal may represent candidate material; authoritative decision remains outside protocol | Non-Protocol authority | Decision authority preserved | Covered |
| Execution Determination | execution interaction/result may carry related information; determination remains execution semantics | Non-Protocol authority | Preserved | Covered |
| Decision Gates | Not represented as protocol authority | Non-Protocol | Gate semantics remain governing-system responsibility | Covered |
| Runtime | participant type `runtime` and recipient/sender semantics | Indirect | Runtime remains execution authority | Covered |
| Contract boundary | protocol itself is defined as downstream representation | Direct | Contract remains normative | Covered |
| Transport | Deliberately unspecified | Non-Protocol | Transport cannot define semantics | Covered |
| API/message implementation | Deliberately unspecified | Non-Protocol | Implementation independence preserved | Covered |
| Continuity | continuation operation + context/trace references | Direct | Protocol continuation ≠ authoritative context | Covered |
| Historical reconstructability | trace/causation/context references | Indirect | History remains external authoritative state | Covered |

---

## 4. Authority Leakage Review

The following leakage paths were explicitly checked:

### Agent → Authority

**Result:** No direct authority field grants an Agent authoritative state.

### Message → Mutation

**Result:** Protocol classification may identify mutation relevance but cannot authorize mutation.

### Proposal → Decision

**Result:** Proposal is explicitly distinct from Engineering Decision.

### Execution Result → Execution Determination

**Result:** Execution Result remains an outcome representation and does not establish an Execution Determination.

### Verification Result → Recognition

**Result:** Verification reporting does not itself establish authoritative recognition.

### Protocol → Transport

**Result:** No transport mechanism is normative.

### Protocol → Runtime Architecture

**Result:** Runtime is represented semantically only; architecture remains outside scope.

---

## 5. Coverage Assessment

Current construction assessment:

```text
Material Contract concepts requiring protocol representation
                         ↓
                    Represented
                         ↓
                Authority boundaries
                    preserved
```

No material Contract concept is currently classified as Pending.

The matrix remains subject to revision if completeness or consistency review identifies a missing protocol representation.

---

## 6. Review Status

**Traceability Construction Result: PASS**  
**Boundary Preservation Result: PASS**  
**Final Phase 5 completeness/consistency status: PENDING FORMAL REVIEW**
