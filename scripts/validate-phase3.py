#!/usr/bin/env python3
"""Phase 3 structural and semantic validation for AESM."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "model/aesm-operational-model.json"
SCHEMA = ROOT / "schemas/aesm-machine-readable-model.schema.json"

REQUIRED_KINDS = {
    "ProcessInstance", "EngineeringObjective", "ExecutionContext", "ProcessState",
    "ProcessStateDefinition", "TransitionRule", "Transition", "DecisionGate",
    "ProgressionCondition", "Condition", "ExecutionMode", "Requirement", "Constraint",
    "Investigation", "Evidence", "Assumption", "Risk", "CandidateSolution", "Evaluation",
    "EngineeringDecision", "VerificationResult", "Artifact", "ExecutionDetermination",
    "Plan", "ExecutionAction", "ExecutionResult", "Participant", "ParticipantInput",
    "ParticipantContribution", "ValidationAssessment", "StateMutation", "ExecutionTrace",
    "TraceEvent", "Reconsideration", "OperationDefinition"
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


def fail(message):
    raise SystemExit(f"FAIL: {message}")


def main():
    try:
        model = json.loads(MODEL.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"JSON parsing failed: {exc}")

    if model.get("serialization", {}).get("format") != "JSON":
        fail("model serialization format is not JSON")
    if "2020-12" not in model.get("serialization", {}).get("schemaDialect", ""):
        fail("model does not declare JSON Schema Draft 2020-12")
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        fail("schema is not Draft 2020-12")

    semantic = model.get("semanticModel", {})
    entities = semantic.get("entityTypes", [])
    by_kind = {e.get("kind"): e for e in entities}
    missing = REQUIRED_KINDS - set(by_kind)
    if missing:
        fail("missing entity kinds: " + ", ".join(sorted(missing)))

    for kind, required in [("ProcessInstance", REQUIRED_PROCESS_FIELDS), ("ExecutionContext", REQUIRED_CONTEXT_FIELDS)]:
        fields = {f.get("name") for f in by_kind[kind].get("fields", [])}
        missing_fields = required - fields
        if missing_fields:
            fail(f"{kind} missing fields: {', '.join(sorted(missing_fields))}")

    if "EngineeringCompletion" not in json.dumps(model) or "RuntimeTermination" not in json.dumps(model):
        fail("engineering completion/runtime termination distinction is not represented")

    for a, b in REQUIRED_DISTINCTIONS:
        if a not in by_kind or b not in by_kind:
            fail(f"required distinction missing: {a} != {b}")

    relationships = semantic.get("relationships", [])
    rel_text = json.dumps(relationships)
    for token in ["ValidationAssessment", "StateMutation", "ExecutionTrace", "Reconsideration"]:
        if token not in rel_text:
            fail(f"relationship coverage missing for {token}")

    operations = semantic.get("operations", [])
    operation_text = json.dumps(operations)
    for token in ["observe", "evaluate", "contribution", "execution", "reconsideration"]:
        if token.lower() not in operation_text.lower():
            fail(f"operation-class coverage missing for {token}")

    invariants = semantic.get("invariants", [])
    invariant_text = json.dumps(invariants)
    for token in ["arbitrary Agent output", "tool output", "authoritative state"]:
        if token.lower() not in invariant_text.lower():
            fail(f"controlled-mutation invariant missing: {token}")

    print("PASS: Phase 3 JSON parsing")
    print("PASS: Schema dialect declaration")
    print("PASS: Required entity coverage")
    print("PASS: ProcessInstance completeness baseline")
    print("PASS: ExecutionContext completeness baseline")
    print("PASS: Critical semantic distinctions")
    print("PASS: Relationship coverage")
    print("PASS: Operation-class coverage")
    print("PASS: Controlled-mutation invariant coverage")
    print("PASS: Phase 3 semantic baseline validation")


if __name__ == "__main__":
    main()
