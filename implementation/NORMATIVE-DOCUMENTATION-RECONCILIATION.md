# Normative Documentation Reconciliation

**Status:** Complete — gate passed
**Work unit:** Normative Documentation Reconciliation

## 1. Reconciliation question

Determine whether the canonical AESM documentation accurately preserves the completed Engineering Scope, Process Binding, persistence, and Agent/Environment mechanism decisions without introducing a second authority or implementation-specific requirement.

## 2. Baseline reviewed

- docs/README.md
- docs/02-System-Model.md
- docs/04-Execution-Model.md
- docs/05-Process-Instance-and-Execution-Context.md
- docs/06-Participants-and-Agent-Participation.md
- docs/07-Runtime-and-Conformance.md
- docs/08-Continuity-Traceability-and-Reconsideration.md
- docs/09-Operational-Guide.md
- docs/Agent-Execution-Integration.md
- Completed execution artifacts for scope resolution, Process Binding, persistence scope, and Agent/Environment mechanism design.

## 3. Reconciliation findings

### Already consistent

The canonical documentation already establishes EPM as the source of engineering meaning, PEM as the source of execution semantics, Runtime as execution authority, Process Instance and Execution Context as distinct concepts, Execution Environment as a capability surface rather than semantic authority, Agent participation without Runtime authority transfer, Runtime responsibility for Process Instance discovery, explicit recoverable EPM binding, persistent/recoverable state, traceability, uncertainty, conflict handling, and implementation independence.

No change was required to the System Model, Execution Model, Runtime and Conformance, or Continuity/Traceability documents.

### Canonical gaps reconciled

The newer semantic work made Engineering Scope Identity and scope-to-Process-Instance binding explicit, but those relationships were not sufficiently visible in the canonical Process Instance, Agent, operational, and integration documentation.

The reconciliation therefore added only these normative clarifications:

1. Process Instance documentation now requires an explicit, recoverable Engineering Scope Identity binding and preserves its distinction from Process Instance Identity, Engineering Objective, repository, workspace, and environment.
2. Agent documentation now states that environment observations are supporting evidence unless an applicable authority path establishes otherwise, and that the Agent must not independently declare scope, select ambiguous candidates, or rewrite an established binding.
3. Operational guidance now separates scope resolution from Process Instance discovery/binding and Context recovery.
4. Agent integration documentation now explicitly shows evidence flowing to Runtime scope resolution and then Process Instance binding/recovery/creation, without prescribing transport or tooling.

## 4. Authority reconciliation

The resulting semantic responsibility remains:

Engineering Process Model
  -> engineering meaning and validity
Process Execution Model
  -> execution semantics
Runtime
  -> authoritative scope resolution, Process Instance binding, and execution control
Process Instance + Execution Context
  -> persistent operational state
Human / AI Agent
  -> participation and contributions
Execution Environment
  -> evidence and interaction capabilities

Repository identity, workspace identity, Agent reasoning, environment mechanisms, and bridge behavior do not become semantic authority by observation or capability.

## 5. Persistence reconciliation

The persistence design requires authoritative reconstruction of Engineering Scope Identity, scope binding basis/provenance, relevant resolution evidence, Process Instance Identity, Engineering Objective, and applicable EPM binding and execution state.

The canonical documentation already requires persistent and recoverable Process Instance state and traceability. No schema or storage mechanism was prescribed and no scope persistence was implemented.

## 6. Agent / Environment reconciliation

The existing mechanism foundation remains mechanism-neutral: persistent Agent guidance, Execution Environment capabilities/evidence, Agent–Runtime bridge, Runtime authority, and ProcessStore persistence.

This is sufficient for the demonstrated known-Process-Instance path. Scope-unknown execution still requires executable capabilities for scope resolution, Process Instance discovery/evaluation, binding, explicit ambiguity/conflict outcomes, and scope/binding persistence.

## 7. Lifecycle and continuity reconciliation

No lifecycle semantics changed. Process Instance lifecycle remains distinct from Process State and Runtime lifecycle; recovery remains distinct from resumption; Agent/session loss and environment replacement do not imply Process Instance termination or scope reassignment.

## 8. DBP evidence reconciliation

The historical DBP experiment remains bounded as previously established. It demonstrates DBP engineering activity but does not retroactively establish AESM Process Instance binding, Runtime participation, or authoritative scope resolution.

The missing operational chain is:

DBP request -> scope evidence -> authoritative scope resolution -> Process Instance binding -> Context recovery or creation -> AESM-governed execution

Historical evidence was not rewritten.

## 9. Changes deliberately not made

- Runtime was not modified.
- ProcessStore was not modified.
- No Scope Python classes or scope persistence were added.
- Candidate discovery, matching, or duplicate detection were not implemented.
- No MCP, Agent skills, VS Code extension, IDE-specific architecture, or orchestration layer was introduced.
- DBP was not modified.
- Historical empirical evidence was not rewritten.
- EPM, PEM, or lifecycle semantics were not changed.
- No transport, API, database, or environment product was made normative.

## 10. Gate decision

### Normative Documentation Reconciliation — COMPLETE

The canonical documentation now reflects the completed scope, Process Binding, persistence, and Agent/Environment mechanism decisions without introducing a competing authority or implementation-specific architecture.

The reconciliation found no contradiction requiring reopening the established semantic decisions.

Implementation may now proceed against the reconciled semantics.

## 11. Next authorized work

**Project Identity and Process Binding Implementation**

Implementation should begin with the smallest vertical slice that establishes authoritative Engineering Scope Identity, Process Instance binding, persistence, and recovery, while preserving explicit unresolved, ambiguous, conflicting, and invalid outcomes.