# AESM Planning Authorization and Task-Transition Refinement

## Identity

Task ID:
aesm-planning-authorization-refinement

Status:
complete

Created:
2026-09-22

Source:
Human instruction — AESM Planning Authorization and Task-Transition Refinement prompt (2026-09-22).
Authorized to strengthen backlog-to-active authorization gate, refine CURRENT.md
forward navigation, and record a non-binding successor in planning-system-restructuring.md.

---

## Objective

Strengthen the AESM planning system's explicit authorization and recovery model:

1. Make backlog-to-active promotion operationally unambiguous in plan/README.md.
2. Make plan/CURRENT.md explicitly distinguish next candidate from authorized task.
3. Record the DBP continuation task as a non-binding successor suggestion in the
   completed planning-system-restructuring task file.

---

## Context

The previous planning-system-restructuring task established the plan/ architecture.
The completed system correctly defines backlog promotion and CURRENT.md authority,
but leaves a gap: a fresh Agent reading CURRENT.md sees "Next Authorized Work" pointing
to a backlog candidate with a prohibition ("must not be activated autonomously"), but
without an explicit unambiguous authorization protocol in README.md and without CURRENT.md
explicitly distinguishing "candidate" from "authorized." This task closes those gaps.

---

## Governing Constraints

1. Do not create plan/SEQUENCE.md, TASKS.md, a task queue, or an ordered backlog.
2. Do not introduce automatic backlog promotion.
3. Do not allow an Agent to choose a backlog item autonomously.
4. Do not treat CURRENT.md as authoritative task state.
5. Do not create a new planning authority.
6. Do not introduce a new planning status solely for authorization.
7. Do not define Task-to-Process-Instance lifecycle rules.
8. Do not modify AESM Runtime semantics.
9. Do not modify Process Instance persistence semantics.
10. Do not create a DBP Process Instance or execute DBP engineering work.
11. Preserve the existing plan/ architecture exactly.

---

## Dependencies

- planning-system-restructuring (COMPLETE — plan/ architecture is the foundation)

---

## Decisions Still in Effect

All decisions from prerequisite completed tasks apply. Key relevant ones:

1. Runtime authority — Runtime remains authoritative for AESM persisted state.
2. CURRENT.md is a navigation projection, not authoritative task state.
3. Task file in plan/active/ is authoritative for task planning state.
4. Backlog tasks require explicit human authorization to activate.
5. No new planning status values without updating definitions/STATUS.md and recording decision.

---

## Work Units

---

### Planning and Authorization Inspection

Status: complete

Objective:
Inspect all existing planning documents to understand current authorization model
before making any changes.

Subtasks:
- [x] Read plan/README.md — evidence: read in full; 190 lines
- [x] Read plan/CURRENT.md — evidence: read in full; 55 lines
- [x] Read plan/PRINCIPLES.md — evidence: read in full; 163 lines
- [x] Read plan/ROADMAP.md — evidence: read in full; 115 lines
- [x] Read plan/definitions/TASK.md — evidence: read in full; 110 lines
- [x] Read plan/definitions/STATUS.md — evidence: read in full; 76 lines
- [x] Read plan/backlog/repository-scoped-dbp-continuation-validation.md — evidence: read in full; 131 lines
- [x] Read plan/completed/planning-system-restructuring.md — evidence: read in full; 422 lines
- [x] Read plan/completed/INDEX.md — evidence: read in full; 52 lines
- [x] Read AGENTS.md — evidence: read in full; 70 lines
- [x] Confirm plan/active/ is empty — evidence: list_dir shows empty directory

Inspection Findings:

**Finding 1 — Backlog status defined.**
plan/README.md §Backlog Promotion (lines 121–134): "Tasks in plan/backlog/ are candidate
future work. An Agent must not autonomously select a backlog Task. Promotion from backlog
to active requires an explicit planning decision — a human instruction that authorizes the
Task."
plan/backlog/repository-scoped-dbp-continuation-validation.md §Authorization Status:
"Not authorized. Requires explicit human instruction to activate."

**Finding 2 — Authorization not operationally defined.**
plan/README.md §Backlog Promotion says "a human instruction that authorizes the Task"
but does not define what that instruction looks like, what form it must take, or how
a fresh Agent recognizes that authorization has occurred from plan/ documents alone.
GAP: The protocol lacks an operational definition of explicit authorization.

**Finding 3 — Authorization not recorded in plan/ documents.**
Currently authorization is conveyed only through the human's prompt — not recorded
in any planning document. A fresh Agent reading only plan/ cannot determine whether
authorization has been given.
GAP: No recoverable authorization record exists between "backlog" and "moved to active."

**Finding 4 — Fresh Agent task-state distinction.**
- Backlog candidate: file in plan/backlog/; status: not-started.
- Active task: file in plan/active/; CURRENT.md references it.
- Completed task: file in plan/completed/; indexed in INDEX.md.
- "Authorized but not yet promoted": no distinct state — promotion IS the record.
  The authorization becomes visible only when the task file moves to plan/active/.

**Finding 5 — CURRENT.md heading "Next Authorized Work" is misleading.**
CURRENT.md §Next Authorized Work (lines 31–42): The section heading says "Authorized"
but the candidate is NOT authorized. This is an accidental implication of authorization.
ISSUE: Must be renamed to "Next Candidate" to remove the false authorization implication.

**Finding 6 — ROADMAP.md §Current Strategic Boundary is misleading.**
ROADMAP.md line 24–25: "The immediate next authorized work is the Repository-Scoped
DBP Continuation Validation."
ISSUE: "authorized" here means "next in strategic direction" not "explicitly authorized
for execution." This could mislead a fresh Agent. Must be rephrased.

**Finding 7 — CURRENT.md does not state authorization status explicitly.**
CURRENT.md says "This task must not be activated autonomously" but does not explicitly
state "NOT AUTHORIZED" as a discrete authorization status field.

**Finding 8 — Statements to preserve.**
- plan/README.md §Backlog Promotion: "An Agent must not autonomously select a backlog Task."
- plan/README.md §Backlog Promotion: "The backlog is a holding area, not a queue."
- plan/README.md §CURRENT.md Authority: CURRENT.md is a "recoverable navigation projection."
- plan/README.md §Governing Rules rule 6: "Backlog Tasks require explicit authorization before activation."
- plan/backlog/ file §Authorization Status: "Not authorized. Requires explicit human instruction."
- All "Task file wins" statements throughout the system.

Gaps to address:
A. plan/README.md §Backlog Promotion: no operational authorization protocol.
B. plan/CURRENT.md §Next Authorized Work heading: misleading authorization implication.
C. plan/CURRENT.md: no explicit Authorization Status field for the candidate.
D. plan/ROADMAP.md §Current Strategic Boundary: misleading "authorized" language.
E. plan/completed/planning-system-restructuring.md: no Suggested Successor entry.

Completion condition:
All existing planning documents are understood; all gaps are identified and recorded.

Status after completion: SATISFIED. Full inspection complete. Five gaps identified.

---

### Backlog Promotion Protocol Refinement

Status: complete

Objective:
Strengthen plan/README.md §Backlog Promotion so that the authorization gate is
operationally unambiguous and recoverable by a fresh Agent.
Also fix plan/ROADMAP.md misleading "authorized" language.

Subtasks:
- [x] Revise plan/README.md §Backlog Promotion with operational authorization protocol — evidence: §Backlog Promotion replaced with What Constitutes Authorization, What Does NOT Constitute Authorization, Authorization Record, No Autonomous Promotion subsections
- [x] Fix plan/ROADMAP.md §Current Strategic Boundary misleading language — evidence: "immediate next authorized work" replaced with "next candidate task" + NOT AUTHORIZED notice

Completion condition:
A fresh Agent reading only plan/README.md can determine what explicit authorization
means, what form it takes, what constitutes authorization vs. non-authorization, and
that backlog presence alone is not authorization.

Status after completion: SATISFIED. README.md §Backlog Promotion now defines authorization
protocol, enumerates non-authorization conditions, defines authorization record, and
prohibits autonomous promotion. ROADMAP.md no longer implies the candidate is authorized.

---

### Current Navigation Refinement

Status: complete

Objective:
Make plan/CURRENT.md explicitly distinguish current state from next candidate,
and record a non-binding successor suggestion in planning-system-restructuring.md.

Subtasks:
- [x] Rename §Next Authorized Work to §Next Candidate in CURRENT.md — evidence: section heading changed; Authorization Status: NOT AUTHORIZED and Required Action fields added
- [x] Add explicit Authorization Status: NOT AUTHORIZED field in CURRENT.md — evidence: CURRENT.md contains explicit NOT AUTHORIZED field under §Next Candidate
- [x] Add Required Action field in CURRENT.md — evidence: CURRENT.md contains Required Action stating explicit human authorization needed
- [x] Add Suggested Successor entry to plan/completed/planning-system-restructuring.md — evidence: §Suggested Successor appended with all five required disclaimer statements

Completion condition:
A fresh Agent reading only plan/CURRENT.md can distinguish: (a) no task is active,
(b) a candidate exists, (c) the candidate is NOT authorized, (d) what action is required.
planning-system-restructuring.md contains the non-binding Suggested Successor entry.

Status after completion: SATISFIED. CURRENT.md §Active Task now references the current
active task; §Next Candidate replaces §Next Authorized Work with explicit NOT AUTHORIZED
status and Required Action. planning-system-restructuring.md has §Suggested Successor
with all five required disclaimer statements.

---

### Planning Consistency Verification

Status: complete

Objective:
Verify the modified planning documents answer all 10 verification questions using
document-derived evidence only, and confirm the regression suite passes.

Subtasks:
- [x] Re-read all modified planning documents as verification source — evidence: plan/README.md, plan/CURRENT.md, plan/ROADMAP.md, plan/completed/planning-system-restructuring.md re-read in verification step
- [x] Answer all 10 questions with file/section evidence — evidence: all 10 questions answered below from plan/ documents alone
- [x] Verify no prohibited implications remain — evidence: all six prohibited implications checked; none found
- [x] Run .venv/bin/pytest tests/ -q and record actual result — evidence: 204 passed in 2.10s, exit code 0
- [x] Run git diff --check and record result — evidence: PASS, no whitespace errors
- [x] Run git status and review diff — evidence: 4 planning files modified (plan/CURRENT.md, plan/README.md, plan/ROADMAP.md, plan/completed/planning-system-restructuring.md); plan/active/ new untracked; no production code changes

10-Question Document-Derived Verification (Verification-Time Snapshot):

The answers below record the planning state observed during this Task's verification on 2026-09-22. They are historical verification evidence, not a statement of the repository's current planning state. For the live state, read `plan/CURRENT.md`.

1. At verification time, what task was active?
   aesm-planning-authorization-refinement
   Source: plan/CURRENT.md §Active Task — Task ID field

2. At verification time, was there an active task?
   Yes
   Source: plan/CURRENT.md §Active Task — Status: in-progress

3. What is the next candidate, if one exists?
   repository-scoped-dbp-continuation-validation
   Source: plan/CURRENT.md §Next Candidate — Task ID field

4. Is that candidate authorized?
   No
   Source: plan/CURRENT.md §Next Candidate — Authorization Status: NOT AUTHORIZED

5. Why is it not authorized?
   Authorization requires explicit human instruction; backlog presence alone is not
   authorization. Enumerated list of non-authorization conditions.
   Source: plan/README.md §Backlog Promotion §What Does NOT Constitute Authorization

6. What explicit human action is required to authorize it?
   An unambiguous human instruction identifying the Task by name and directing the
   Agent to activate it (e.g., "Activate repository-scoped-dbp-continuation-validation").
   Source: plan/README.md §Backlog Promotion §What Constitutes Authorization

7. Can the Agent activate it autonomously?
   No.
   Source: plan/README.md §Backlog Promotion §No Autonomous Promotion

8. Does CURRENT.md itself authorize anything?
   No. It is a recoverable navigation projection.
   Source: plan/CURRENT.md §Navigation Entry Point; plan/README.md §CURRENT.md Authority

9. Where does authoritative Task state live?
   In the active Task file: plan/active/aesm-planning-authorization-refinement.md
   Source: plan/README.md §CURRENT.md Authority; plan/PRINCIPLES.md §9; plan/definitions/TASK.md §Authority

10. What is the relationship between planning state and AESM Runtime state?
    Planning state records intent. AESM Runtime state records authoritative execution
    evidence. Neither substitutes for the other.
    Source: plan/README.md §Planning / AESM Boundary table; plan/PRINCIPLES.md §1 and §2

Prohibited Implications Check:
- Automatic backlog promotion: NONE — plan/README.md §No Autonomous Promotion prohibits it
- Ordered execution commitment: NONE — "backlog is a holding area, not a queue"
- Agent-controlled task selection: NONE — §No Autonomous Promotion prohibits it
- Hidden task queue: NONE — no ordering structure exists
- New planning authority: NONE — exactly one planning system (plan/) exists
- Process Instance lifecycle relationship: NONE — no PI semantics added to any planning document

Completion condition:
All 10 verification questions answered with document-derived evidence; no prohibited
implications found; regression suite result recorded; diff verified clean.

Status after completion: SATISFIED. All 10 questions answerable from plan/ documents alone;
all six prohibited implications checked and found absent; 204/204 regression PASS;
git diff --check PASS; diff shows only planning documentation changes.

---

## Acceptance Criteria

1. plan/README.md clearly defines backlog candidate status. — [x] PASS
2. Explicit human authorization is operationally defined in plan/README.md. — [x] PASS
3. The Agent cannot interpret backlog presence as authorization. — [x] PASS
4. The Agent cannot autonomously promote a backlog Task. — [x] PASS
5. Authorization can be recognized from repository documentation. — [x] PASS
6. plan/CURRENT.md explicitly distinguishes current state from next candidate. — [x] PASS
7. A Next Candidate is clearly non-authorizing. — [x] PASS (Authorization Status: NOT AUTHORIZED)
8. planning-system-restructuring.md contains the specified non-binding Suggested Successor. — [x] PASS
9. No new sequencing artifact has been introduced. — [x] PASS
10. No new planning authority has been introduced. — [x] PASS
11. No new status value has been introduced. — [x] PASS
12. No Process Instance lifecycle semantics have been invented. — [x] PASS
13. The DBP continuation validation remains inactive. — [x] PASS
14. The planning/AESM authority boundary remains intact. — [x] PASS
15. All ten verification questions have document/section evidence. — [x] PASS
16. .venv/bin/pytest tests/ -q executed and actual result recorded. — [x] PASS (204 passed)
17. git diff --check passes. — [x] PASS
18. No unrelated repository changes were made. — [x] PASS

---

## Verification Requirements

1. Re-read all modified planning documents without construction context. — [x] DONE
2. Answer all 10 navigation questions from plan/ alone. — [x] DONE (see Work Unit 4)
3. Verify no prohibited implications remain. — [x] DONE (all six checked; none found)
4. Run .venv/bin/pytest tests/ -q and record actual result. — [x] DONE (204 passed in 2.10s)
5. Run git diff --check. — [x] DONE (PASS)
6. Run git status and review complete diff. — [x] DONE

---

## Completion Record

Completed: 2026-09-22

Evidence:
- plan/README.md: §Backlog Promotion expanded with operational authorization protocol
- plan/CURRENT.md: §Next Authorized Work replaced by §Next Candidate with explicit NOT AUTHORIZED status
- plan/ROADMAP.md: misleading "authorized" language corrected to "candidate"
- plan/completed/planning-system-restructuring.md: §Suggested Successor appended
- plan/active/aesm-planning-authorization-refinement.md: this task file (new)
- 204/204 regression tests PASS (.venv/bin/pytest tests/ -q, exit code 0)
- git diff --check: PASS
- No production code changes; no AESM Runtime semantics modified

Verification result:
- All 10 navigation questions answerable from plan/ documents alone without construction knowledge
- All six prohibited implications checked and found absent
- Regression suite: 204 PASS
- Changed files: planning documentation only (4 modified, 1 new)
