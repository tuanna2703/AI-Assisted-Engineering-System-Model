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

    model_text = json.dumps(model)
    if "EngineeringCompletion" not in model_text or "RuntimeTermination" not in model_text:
        collect_error(errors, "engineering completion/runtime termination distinction is not represented")

    for a, b in REQUIRED_DISTINCTIONS:
        if a not in by_kind or b not in by_kind:
            collect_error(errors, f"required distinction missing: {a} != {b}")

    relationships = semantic.get("relationships", [])
    rel_text = json.dumps(relationships)
    for token in ["ValidationAssessment", "StateMutation", "ExecutionTrace", "Reconsideration"]:
        if token not in rel_text:
            collect_error(errors, f"relationship coverage missing for {token}")

    # Operation semantics are represented by the top-level operationClasses
    # structure, not by a semanticModel.operations entity collection.
    operation_classes = model.get("operationClasses", [])
    operation_text = json.dumps(operation_classes)
    for token in ["observe", "evaluate", "contribution", "execution", "reconsideration"]:
        if token.lower() not in operation_text.lower():
            collect_error(errors, f"operation-class coverage missing for {token}")

    invariants = model.get("invariants", [])
    invariant_text = json.dumps(invariants)
    for token in ["arbitrary Agent output", "tool output", "authoritative state"]:
        if token.lower() not in invariant_text.lower():
            collect_error(errors, f"controlled-mutation invariant missing: {token}")

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
