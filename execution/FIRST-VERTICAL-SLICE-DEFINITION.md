# First Vertical Slice Definition

## Purpose

Define the first concrete engineering Process Instance used to derive the minimum EPM state, transition, completion, termination, and Runtime lifecycle semantics required by the implementation prototype.

This document derives implementation requirements from an existing real engineering execution. It does not redefine the normative AESM model.

## Selected Engineering Request

**Repository:** `tuanna2703/directories-builder-pro`

**Component:** Reviews module, `Add_Review_Form`

**Request:** Convert `Add_Review_Form::business_id` from `Fields_Manager::SELECT` to `Fields_Manager::POST_SELECT`, targeting `dbp_business` posts, while preserving correct review persistence.

### Why this request is suitable

The request is genuine, bounded, non-trivial because it crosses two identifier domains, verifiable, and representative of investigation, evidence gathering, engineering decision, implementation, and verification.

### Important target clarification

The observation report identified a mismatch between the broader investigation wording (`Edit_Review_Form`) and the task actually supplied to the Agent (`Add_Review_Form`). The Agent correctly executed the task it received. The first vertical slice is therefore explicitly bound to **`Add_Review_Form`**, not `Edit_Review_Form`. The `Edit_Review_Form` discrepancy is excluded from this slice and must not silently expand its scope.

## Engineering Objective

Change the `business_id` input in `Add_Review_Form` to use the repository's existing post-search selection mechanism while preserving the domain expected by the review persistence layer.

```text
User selects a dbp_business WordPress post
        ↓
POST_SELECT submits WP_Post::ID
        ↓
Add_Review_Form::save() translates WP post ID
        ↓
Business_Repository::find_by_post_id()
        ↓
dbp_businesses.id
        ↓
Review persistence continues using the custom-table business ID
```

## Requirements

1. `business_id` uses `Fields_Manager::POST_SELECT`.
2. The post type is `dbp_business`.
3. Selection remains single-valued.
4. A selected WordPress post ID is translated to the corresponding `dbp_businesses.id` before review persistence.
5. Existing invalid-selection validation remains effective.
6. Review persistence and downstream business lookup semantics remain unchanged.
7. Obsolete manual option construction is removed only where made unnecessary by the field conversion.
8. No unrelated form, repository, or review behavior is changed.

## Constraints

- `dbp_reviews.business_id` references the custom business-table identifier, not the WordPress post ID.
- Existing `POST_SELECT` behavior returns WordPress post IDs.
- `Business_Repository::find_by_post_id()` provides the required translation.
- Existing `POST_SELECT` configuration conventions should be followed.
- The implementation must remain limited to the selected request.

## Explicit Exclusions

- `Edit_Review_Form` changes.
- Changes to `POST_SELECT` infrastructure.
- Changes to the `dbp_business` data model.
- Changes to review schema or repository semantics.
- General Runtime/lifecycle redesign unrelated to this slice.
- Normative changes to AESM EPM/PEM semantics.

## Applicable EPM Binding

The applicable engineering semantics are the current AESM Engineering Model represented by `docs/03-Engineering-Model.md` at the baseline used for this derivation. The slice requires Engineering Objective, Requirements, Constraints, Investigation, Evidence, Engineering Decision, Implementation, Artifacts, Verification, Process State, Progress, and Completion.

Candidate Solutions and reconsideration are not required as independent process elements for the initial successful execution, although the process must remain capable of reconsideration if verification or feedback invalidates the current solution.

The EPM binding is process information and must be persisted with the Process Instance rather than inferred from the Agent session.

## Derived Process States

The observed execution supports four semantically meaningful states for this slice.

### Investigation

**Purpose:** Establish sufficient evidence to make a confident implementation decision.

**Activities:** Inspect the target form, field types, existing conventions, persistence/repository behavior, identifier domains, and relevant supporting code.

**Outputs:** Requirements/constraints understood, relevant evidence recorded, material risks/uncertainties identified, and an Engineering Decision ready to guide implementation.

**Completion:** Sufficient recognized evidence exists to justify the selected implementation approach and no material unresolved issue prevents the decision.

### Implementation

**Purpose:** Apply the accepted engineering decision to the target artifact without exceeding scope.

**Activities:** Modify the target source file and perform implementation-oriented checks needed to establish the intended artifact change.

**Outputs:** Requested artifact modification and required implementation result information.

**Completion:** The intended implementation change has been applied and the resulting artifact is available for verification.

### Verification

**Purpose:** Establish whether the implemented artifact satisfies applicable requirements and conditions.

**Activities:** Syntax checks, structural checks, tests, runtime checks, and other appropriate evidence-producing verification.

**Outputs:** Verification evidence, pass/fail determination, and remaining risks or limitations.

**Completion:** Required verification has produced sufficient evidence to determine whether the engineering objective is satisfied.

### Engineering Complete

**Purpose:** Represent that the engineering objective has been established as satisfied under the applicable EPM completion conditions.

**Activities:** No further implementation is required unless new evidence or feedback causes reconsideration.

**Outputs:** Recognized completion and preserved verification/decision traceability.

**Completion:** Objective, requirements, implementation result, and applicable verification conditions are satisfied, with no unresolved material issue blocking completion.

> `Engineering Complete` is a derived state name for this slice, not a claim that `engineering_complete` is a universal AESM state identifier. The existing Runtime string remains an implementation detail until validated against this slice.

## Derived Transitions

| Source | Condition | Destination | Runtime responsibility |
|---|---|---|---|
| Investigation | Sufficient evidence, understood constraints, and established Engineering Decision | Implementation | Recognize applicable information and permit/record transition; do not make the engineering decision |
| Implementation | Intended artifact change applied and ready for evaluation | Verification | Record execution result and establish verification as the required next activity |
| Verification | Required verification passed and completion conditions satisfied | Engineering Complete | Recognize completion conditions and apply permitted state mutation |
| Verification | Verification failed or material uncertainty remains | Investigation or Implementation, according to current engineering conditions | Preserve failure/uncertainty and support reconsideration; do not infer destination from technical convenience |

### Investigation → Implementation execution condition

The observed workflow included human approval of the implementation plan before code modification. This is recorded as a **prototype execution condition**, not as evidence that the EPM universally requires a plan-approval Decision Gate.

### Implementation → Verification

This transition is based on the existence of the intended artifact change, not on the Agent's assertion that the implementation is correct.

### Verification → Engineering Complete

Verification success is necessary but, for this slice, completion also requires that the objective and requirements remain satisfied and no material unresolved matter blocks completion.

## Feedback and Reconsideration

A failed verification or material new evidence must not be represented as successful completion.

```text
Verification
    ↓ failure / material new evidence
Investigation
    ↓ reconsider decision if necessary
Implementation
    ↓
Verification
```

Historical evidence, decisions, and failed verification results remain reconstructable. Reconsideration does not erase prior conclusions.

## Engineering Completion Semantics

Engineering completion for this slice requires:

1. the requested `Add_Review_Form::business_id` conversion is implemented;
2. the field targets `dbp_business` posts and remains single-valued;
3. submitted WP post IDs are translated to the custom business-table ID domain before persistence;
4. invalid selections remain rejected;
5. relevant verification evidence passes;
6. no material unresolved issue prevents the intended behavior.

Engineering completion is distinct from Agent response termination, IDE/session closing, Runtime stopping, and Process Instance termination.

## Process Instance Termination

This slice does **not** establish a separate engineering requirement for explicit Process Instance termination semantics. Termination remains distinct from engineering completion, and no new terminal lifecycle value is introduced.

The Process Instance may therefore reach engineering completion while its lifecycle remains active until an explicit termination condition is established by the execution model. The evidence from this slice is insufficient to invent general termination semantics.

## Minimal Runtime Lifecycle Boundary

The slice justifies these Runtime responsibilities:

- establish/attach the Process Instance;
- maintain authoritative Execution Context;
- recognize relevant evidence contributions;
- recognize the Engineering Decision before authoritative recording;
- record implementation/pending execution information;
- record verification results;
- evaluate derived transition conditions;
- recognize engineering completion when its conditions are established;
- persist state changes and traceability;
- preserve failure/uncertainty and permit reconsideration.

The Runtime must not decide which repository files require investigation, choose the implementation solution, substitute its own engineering judgment, or equate a successful shell command with engineering completion.

## Comparison With Existing Runtime States

Current implementation representations include `initial`, `implementation`, and `engineering_complete` in `ExecutionContext`, while `set_pending_execution()` currently assigns `implementation`.

The slice does not justify treating these strings as universal EPM states. Its derived semantics map approximately as follows:

```text
initial implementation representation
    → Investigation semantics required before implementation

implementation
    → Implementation semantics

(no current explicit verification state)
    → Verification semantics required by the slice

engineering_complete
    → Engineering Complete semantics, but only after derived completion conditions
```

This establishes a concrete Runtime gap: the current implementation does not represent the full derived lifecycle, particularly the distinction between Investigation and Verification.

## Runtime Gaps Established by the Slice

1. Lifecycle representation must support the derived states without promoting arbitrary strings into universal EPM semantics.
2. Runtime transition operations must evaluate explicit conditions rather than assign state strings as side effects.
3. Verification must participate in transition evaluation rather than merely clear pending execution.
4. Engineering completion must require recognized completion conditions rather than only a caller-provided recognition flag and basis.
5. Process termination remains unresolved and should not be generalized here.
6. Artifact association remains required for continuity, but its exact schema/API should be derived only as far as this slice requires.

## Required Runtime Experiment

The next Runtime implementation should test only:

- start in Investigation;
- record recognized evidence;
- recognize an Engineering Decision and permit transition to Implementation;
- record implementation artifact/result and permit transition to Verification;
- record verification result;
- permit transition to Engineering Complete only when completion conditions are satisfied;
- preserve failed Verification as failure/uncertainty and support return to Investigation or Implementation;
- persist each recognized state change and relevant evidence.

The experiment must not introduce a universal workflow engine.

## Conclusion

This request is sufficiently small to serve as the first real EPM/Runtime lifecycle slice. It exposes meaningful distinctions that the current Runtime does not yet enforce while remaining narrow enough to avoid premature generalization.

The next implementation task is to implement and test the minimum lifecycle behavior derived here, not to build the Agent-facing adapter yet.
