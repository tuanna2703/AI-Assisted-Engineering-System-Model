#!/usr/bin/env python3
"""Phase 3 structural and semantic validation for AESM."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "model/aesm-operational-model.json"
SCHEMA = ROOT / "schemas/aesm-machine-readable-model.schema.json"

# Primary entity vocabulary derived from the reconciled Phase 3 Matrix A.
# OperationDefinition and TraceEvent are intentionally excluded: they are
# semantic/structural concepts, not top-level entity kinds.
REQUIRED_KINDS = {
    "ProcessInstance", "EngineeringObjective", "ExecutionContext", "ProcessState",
    "ProcessStateDefinition", "TransitionRule", "Transition", "DecisionGate",
    "ProgressionCondition", "Condition", "ExecutionMode", "Requirement", "Constraint",
    "Investigation", "Evidence", "Assumption", "Risk", "CandidateSolution", "Evaluation",
    "EngineeringDecision", "VerificationResult", "Artifact", "ExecutionDetermination",
    "Plan", "ExecutionAction", "ExecutionResult", "Participant", "ParticipantInput",
    "ParticipantContribution", "ValidationAssessment", "StateMutation", "ExecutionTrace",
    "Reconsideration", "Observation"
}

REQUIRED_PROCESS_FIELDS = {
    "id", "epmRef", "pemRef", "engineeringObjectiveRef", "executionModeRef",
    "engineeringCompletionStatus", "runtimeLifecycleStatus", "executionContextRef",
    "initialization", "executionTraceRef"
}

REQUIRED_CONTEXT_FIELDS = {
    "id", "processInstanceRef", "currentProcessStateRef", "executionModeRef",
    "engineeringObjectiveRef", "requirements", "constraints", "investigations", "evidence",
    "assumptions", "risks", "candidateSolutions", "evaluations", "unresolvedMatters",
    "artifacts", "engineeringDecisions", "decisionGates", "verificationResults", "continuity",
    "lastAuthoritativeUpdate", "continuation"
}

REQUIRED_DISTINCTIONS = {
    ("EngineeringDecision", "ExecutionDetermination"),
    ("ParticipantInput", "ParticipantContribution"),
    ("ParticipantContribution", "ValidationAssessment"),
    ("ValidationAssessment", "StateMutation"),
}


def collect_error(errors, message):
    errors.append(message)


def main():
    errors = []

    try:
        model = json.loads(MODEL.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"FAIL: JSON parsing failed: {exc}")

    if model.get("serialization", {}).get("format") != "JSON":
        collect_error(errors, "model serialization format is not JSON")
    if "2020-12" not in model.get("serialization", {}).get("schemaDialect", ""):
        collect_error(errors, "model does not declare JSON Schema Draft 2020-12")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        collect_error(errors, "schema is not Draft 2020-12")

    semantic = model.get("semanticModel", {})
    entities = semantic.get("entityTypes", [])
    by_kind = {e.get("kind"): e for e in entities}

    missing = REQUIRED_KINDS - set(by_kind)
    if missing:
        collect_error(errors, "missing entity kinds: " + ", ".join(sorted(missing)))

    for kind, required in [
        ("ProcessInstance", REQUIRED_PROCESS_FIELDS),
        ("ExecutionContext", REQUIRED_CONTEXT_FIELDS),
    ]:
        if kind in by_kind:
            fields = {f.get("name") for f in by_kind[kind].get("fields", [])}
            missing_fields = required - fields
            if missing_fields:
                collect_error(errors, f"{kind} missing fields: {', '.join(sorted(missing_fields))}")

    # --- Engineering Completion vs Runtime Termination (structured) ---
    # Validate via ProcessInstance field presence and the dedicated invariant,
    # NOT by serializing the model to a string and searching for tokens.
    pi = by_kind.get("ProcessInstance")
    if pi is not None:
        pi_fields = {f.get("name") for f in pi.get("fields", [])}
        if "engineeringCompletionStatus" not in pi_fields:
            collect_error(errors, "ProcessInstance missing structured field: engineeringCompletionStatus")
        if "runtimeLifecycleStatus" not in pi_fields:
            collect_error(errors, "ProcessInstance missing structured field: runtimeLifecycleStatus")
    else:
        collect_error(errors, "ProcessInstance entity not found — cannot verify completion/termination separation")

    invariants = model.get("invariants", [])
    invariant_by_id = {inv.get("id"): inv for inv in invariants}

    ct_inv = invariant_by_id.get("completion-termination-separation")
    if ct_inv is None:
        collect_error(errors, "missing invariant: completion-termination-separation")
    else:
        ct_stmt = ct_inv.get("statement", "").lower()
        if "completion" not in ct_stmt or "termination" not in ct_stmt:
            collect_error(errors, "completion-termination-separation invariant does not reference both completion and termination")

    for a, b in REQUIRED_DISTINCTIONS:
        if a not in by_kind or b not in by_kind:
            collect_error(errors, f"required distinction missing: {a} != {b}")

    relationships = semantic.get("relationships", [])
    rel_by_src_tgt = set()
    for r in relationships:
        rel_by_src_tgt.add(r.get("source", ""))
        rel_by_src_tgt.add(r.get("target", ""))
    for token in ["ValidationAssessment", "StateMutation", "ExecutionTrace", "Reconsideration"]:
        if token not in rel_by_src_tgt:
            collect_error(errors, f"relationship coverage missing for {token}")

    # Operation semantics are represented by the top-level operationClasses
    # structure, not by a semanticModel.operations entity collection.
    operation_classes = model.get("operationClasses", [])
    op_class_ids = {oc.get("id", "").lower() for oc in operation_classes}
    for token in ["observation", "evaluation", "contribution", "execution", "reconsideration"]:
        if token not in op_class_ids:
            collect_error(errors, f"operation-class coverage missing for {token}")

    # --- Controlled-mutation invariant (structured) ---
    # Validate by looking up the invariant by its structured `id` field and
    # checking that its statement covers the required semantic concepts.
    # Do NOT search for exact literal phrases like "arbitrary Agent output"
    # or "tool output" because punctuation and phrasing may vary.
    cm_inv = invariant_by_id.get("controlled-mutation")
    if cm_inv is None:
        collect_error(errors, "missing invariant: controlled-mutation")
    else:
        cm_stmt = cm_inv.get("statement", "").lower()
        # The controlled-mutation invariant must semantically cover:
        # Participant, Agent, tool, environment, and output.
        required_concepts = ["participant", "agent", "tool", "environment", "output"]
        missing_concepts = [c for c in required_concepts if c not in cm_stmt]
        if missing_concepts:
            collect_error(errors, f"controlled-mutation invariant missing concepts: {', '.join(missing_concepts)}")

    # Authoritative-state representation: validate via structured invariant lookup.
    ec_inv = invariant_by_id.get("execution-context-authority")
    if ec_inv is None:
        collect_error(errors, "missing invariant: execution-context-authority")
    else:
        ec_stmt = ec_inv.get("statement", "").lower()
        if "authoritative" not in ec_stmt:
            collect_error(errors, "execution-context-authority invariant does not reference authoritative state")

    # TraceEvent is a structural type contained by ExecutionTrace rather than
    # a primary entity kind. Validate that the ExecutionTrace definition has
    # an explicit event collection.
    trace = by_kind.get("ExecutionTrace")
    if trace is not None:
        trace_fields = {f.get("name") for f in trace.get("fields", [])}
        event_fields = {"events", "eventRefs", "traceEvents", "eventRecords"}
        if not trace_fields.intersection(event_fields):
            collect_error(
                errors,
                "ExecutionTrace does not expose an explicit ordered event collection "
                "(expected one of: events, eventRefs, traceEvents, eventRecords)",
            )

    if errors:
        print("FAIL: Phase 3 semantic validation")
        for error in errors:
            print(f"FAIL: {error}")
        raise SystemExit(1)

    print("PASS: Phase 3 JSON parsing")
    print("PASS: Schema dialect declaration")
    print("PASS: Required entity coverage")
    print("PASS: ProcessInstance completeness baseline")
    print("PASS: ExecutionContext completeness baseline")
    print("PASS: Critical semantic distinctions")
    print("PASS: Relationship coverage")
    print("PASS: Operation-class coverage")
    print("PASS: Controlled-mutation invariant coverage")
    print("PASS: ExecutionTrace event-collection coverage")
    print("PASS: Phase 3 semantic baseline validation")


if __name__ == "__main__":
    main()
