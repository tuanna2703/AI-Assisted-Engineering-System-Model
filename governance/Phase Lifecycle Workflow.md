# Phase Lifecycle Workflow

**Project:** AI-Assisted Engineering System Model (AESM)  
**Artifact Type:** Project / Specification Governance  
**Status:** Governance Baseline — Retrospective Audit Pending  
**Date:** 2026-08-18

---

## 1. Purpose

The **Phase Lifecycle Workflow** defines the standard governance lifecycle used to develop, review, validate, revise, canonicalize, and freeze phases of the AESM specification project.

It governs the specification-development project only. It does not define engineering-process semantics, execution semantics, Runtime behavior, or Agent behavior.

The workflow exists to make phase governance explicit, repeatable, traceable, and freeze-controlled.

---

## 2. Governance Boundary

This workflow belongs to the AESM project/specification governance layer.

```text
AESM Project / Specification Governance
              │
              ▼
       Phase Lifecycle Workflow
              │
              ▼
     Phase-specific work
              │
              ├── specifications
              ├── analyses
              ├── reviews
              ├── validations
              └── freeze artifacts
```

It shall not become part of EPM or PEM semantics.

EPM remains authoritative for engineering meaning and validity. PEM remains authoritative for process execution semantics. This workflow governs how AESM specification phases are developed and controlled.

---

## 3. Standard Lifecycle

Every governed phase shall follow this control lifecycle, with phase-specific work and validation methods determined by the phase.

```text
Phase Entry
    ↓
Phase Definition
    ↓
Construction / Work
    ↓
Completeness Review
    ↓
Consistency Review
    ↓
Boundary Review
    ↓
Validation
    ↓
Freeze Eligibility
    ↓
Freeze Review
    ↓
Canonicalization
    ↓
Freeze Decision
    ↓
Post-Freeze Baseline
```

A failed review or validation returns the phase to **Revision / Correction**. The affected validation or review result remains historical evidence.

```text
Review / Validation
        ↓
      PASS ───────────────→ next control stage
        │
       FAIL
        ↓
Revision / Correction
        ↓
Re-review / Re-validation
        └──────────────────→ applicable control stage
```

---

## 4. Phase Entry

Before substantive phase work begins, the phase shall have an explicit entry definition containing:

- phase identity and purpose;
- phase scope;
- required inputs;
- governing frozen baselines;
- dependencies on prior phases;
- expected phase artifacts;
- known constraints and boundaries;
- initial acceptance criteria.

Phase Entry establishes what the phase is authorized to address. It does not establish the final content of the phase.

A phase shall not silently change its governing scope during construction. Material scope changes shall be explicitly recognized and assessed for downstream impact.

---

## 5. Phase Definition

The phase shall define:

- objectives;
- artifact responsibilities;
- semantic and governance boundaries;
- required reviews;
- required validation methods;
- acceptance criteria;
- expected evidence of completion;
- freeze prerequisites.

Common governance requirements are mandatory, but validation techniques and artifacts may be phase-specific.

---

## 6. Construction / Work

The phase-specific work is performed within the defined scope and against the governing baselines.

Construction may be iterative. It may include analysis, specification drafting, modeling, implementation of validators, review preparation, or other work required by the phase.

Intermediate drafts are non-authoritative unless explicitly designated otherwise.

Material alternatives or competing drafts shall remain distinguishable until canonicalization.

---

## 7. Completeness Review

**Purpose:** determine whether the phase has defined everything required by its scope and acceptance criteria.

The review shall consider, as applicable:

- required concepts and artifacts;
- required relationships and rules;
- required boundaries;
- required validation coverage;
- required evidence;
- required traceability;
- required continuity information;
- known phase-specific acceptance criteria.

A completeness failure means the phase is insufficiently defined or constructed. The phase returns to Revision / Correction.

Completeness does not establish consistency or validity.

---

## 8. Consistency Review

**Purpose:** determine whether the phase is consistent with its governing baselines and with other authoritative AESM artifacts.

The review shall consider, as applicable:

- EPM consistency;
- PEM consistency;
- Operational Model consistency;
- consistency with previously frozen phase artifacts;
- terminology and vocabulary consistency;
- architectural-boundary consistency;
- dependency consistency;
- internal consistency.

A consistency failure returns the affected phase content to Revision / Correction.

A consistency review shall not silently modify a frozen upstream artifact. If a genuine upstream inconsistency is discovered, it shall be recorded and handled through the applicable change-control mechanism.

---

## 9. Boundary Review

**Purpose:** determine whether the phase preserves authority, responsibility, and architectural boundaries.

Boundary review shall be applied where the phase can affect or describe relationships between layers, participants, authorities, or responsibilities.

It shall consider, as applicable:

- EPM / PEM separation;
- Runtime / Agent separation;
- engineering authority / execution authority separation;
- capability / authority separation;
- observation / mutation separation;
- participant input / observation / candidate contribution distinctions;
- semantic interaction / protocol independence;
- current state / historical trace separation.

Boundary Review may be not-applicable for phases where no material boundary is introduced or modified; that determination shall be explicit.

---

## 10. Validation

Validation establishes conformance with the applicable phase acceptance criteria and invariants.

Validation may include:

- schema validation;
- structural validation;
- semantic validation;
- executable validators;
- independent checks;
- reconstruction checks;
- vocabulary coverage;
- operation or relationship coverage;
- authority and mutation checks;
- traceability checks;
- continuity checks;
- phase-specific tests.

The validation method shall be appropriate to the artifact being validated.

A validator validates the applicable canonical candidate artifact; it does not become the semantic authority.

Validation results shall identify the artifact/version or repository state against which validation was performed.

---

## 11. Revision and Correction

A failed review or validation shall return the phase to revision.

Corrections shall be explicit and traceable. A correction shall not overwrite the existence of the earlier failed review or validation attempt.

If a correction affects content covered by an earlier review or validation result, the affected result shall be treated as invalidated for freeze purposes and the affected checks shall be repeated.

The correction loop is therefore:

```text
Attempt
  ↓
Result
  ↓
Correction
  ↓
New Attempt
```

Historical attempts remain preserved.

A validator defect shall be distinguished from an artifact defect. Correcting a validator does not by itself imply that the canonical artifact was incorrect.

---

## 12. Freeze Eligibility

A phase may be declared **Freeze Eligible** only when all applicable prerequisites are satisfied:

1. required phase artifacts exist;
2. phase scope and objectives are satisfied;
3. Completeness Review passed;
4. Consistency Review passed;
5. required Boundary Review passed or was explicitly determined not applicable;
6. required Validation passed;
7. outstanding material defects are resolved or explicitly dispositioned under approved change control;
8. canonical artifact candidates are identified;
9. historical review and validation evidence is preserved;
10. dependencies on previous frozen phases have been checked;
11. downstream impact of the frozen baseline is understood sufficiently for the next phase.

Freeze Eligibility is not itself a freeze decision.

---

## 13. Freeze Review

The Freeze Review is the final governance review before a phase becomes authoritative.

It shall verify:

- freeze eligibility;
- completeness of required evidence;
- consistency with frozen dependencies;
- absence of unresolved material defects;
- identification of the canonical artifact;
- absence of competing authoritative drafts;
- preservation of historical evidence;
- readiness for downstream use;
- explicit freeze decision authority.

The Freeze Review shall record either **PASS** or **FAIL**.

A failed Freeze Review returns the phase to the applicable revision or correction stage.

---

## 14. Canonicalization

Canonicalization is a required freeze gate.

Before a phase is frozen:

1. the canonical artifact shall be explicitly identified;
2. competing drafts shall be identified and classified as non-authoritative, superseded, or otherwise dispositioned;
3. the canonical artifact shall be synchronized with the reviewed content;
4. the freeze record shall identify the canonical artifact and version/repository state;
5. no alternative draft shall remain implicitly authoritative.

Canonicalization shall not erase historical drafts or evidence needed to reconstruct the phase's development.

---

## 15. Freeze Decision

A phase becomes **Frozen** only after:

```text
Freeze Eligibility
      ↓
Freeze Review = PASS
      ↓
Canonicalization complete
      ↓
Explicit Freeze Decision
      ↓
Frozen
```

The freeze decision shall identify:

- phase;
- canonical artifact(s);
- governing baseline(s);
- relevant review/validation evidence;
- freeze status;
- date or repository state sufficient to identify the frozen baseline.

A frozen artifact becomes authoritative for downstream phases unless subsequently changed through explicit change control.

---

## 16. Post-Freeze Baseline

After freeze, the phase establishes a downstream baseline.

The baseline shall make it possible to determine:

- what was frozen;
- which artifacts are authoritative;
- which reviews and validations support the freeze;
- which dependencies later phases may rely upon;
- what historical evidence exists;
- what changes would constitute a post-freeze modification.

Subsequent phases shall use the frozen baseline rather than an informal recollection of the phase.

---

## 17. Review Semantics

The following review types shall remain distinct:

| Control | Question answered |
|---|---|
| Completeness Review | Did we define and produce everything required? |
| Consistency Review | Does it agree with governing baselines and related artifacts? |
| Boundary Review | Did authority, responsibility, or architectural boundaries leak? |
| Validation | Does the artifact satisfy applicable structural and semantic invariants? |
| Freeze Review | Is the phase stable and controlled enough to become authoritative? |

A phase may use additional review types, but these controls shall not be silently conflated.

---

## 18. Evidence and Historical Preservation

Review and validation attempts are historical evidence.

The project shall preserve, where material:

- attempt identity;
- artifact/repository state evaluated;
- criteria or checks applied;
- result;
- detected defects;
- corrections;
- subsequent attempt;
- final disposition.

Failed attempts shall not be rewritten to appear successful after correction.

This preserves the distinction between the state that failed and the state that subsequently passed.

---

## 19. Phase-Specific Variation

The workflow defines governance controls, not identical work products.

For example:

```text
Phase 3
Operational Model
→ machine-readable representation
→ schema validation
→ semantic validator
→ independent checks
→ reconstruction / authority checks

Phase 4
Boundary Matrix
→ Agent Execution Contract
→ semantic contract review
→ authority / boundary verification
→ correction / post-correction review
→ canonicalization / freeze
```

A future phase may use different artifacts and validation techniques while retaining the same governance control structure.

---

## 20. Change Control After Freeze

A frozen phase shall not be modified implicitly.

A material post-freeze change shall:

1. identify the affected frozen artifact;
2. state the reason for change;
3. identify affected downstream dependencies;
4. determine whether re-review or re-validation is required;
5. preserve the previous frozen baseline;
6. produce a new revision and explicit freeze decision if the authoritative baseline changes.

The default assumption shall be that material changes invalidate affected downstream reliance until impact has been assessed.

---

## 21. Governance Invariants

The following invariants apply to the phase lifecycle:

1. **Phase completion shall not be equated with freeze.**
2. **Freeze eligibility shall not be equated with freeze.**
3. **Canonicalization shall precede the freeze decision.**
4. **Failed reviews and validations shall remain reconstructable.**
5. **Corrections affecting validated content shall trigger affected re-validation.**
6. **Frozen upstream artifacts shall not be silently rewritten to resolve downstream inconsistencies.**
7. **The validator shall not become the semantic authority.**
8. **Phase governance shall not redefine EPM or PEM semantics.**
9. **Phase-specific validation methods may vary.**
10. **Every frozen phase shall establish an identifiable downstream baseline.**
11. **Historical evidence shall remain distinguishable from current authoritative state.**
12. **No competing draft shall remain implicitly authoritative after freeze.**

---

## 22. Standard Phase Statuses

The governance lifecycle recognizes the following control statuses:

```text
Not Started
   ↓
Entered
   ↓
Defined
   ↓
In Progress
   ↓
Under Review / Validation
   ↓
Freeze Eligible
   ↓
Frozen
```

A phase may return from review or validation to **In Progress** through correction.

**Frozen** is terminal for that baseline. Any later modification creates a new revision subject to change control.

---

## 23. Relationship to the AESM Architecture

The governance relationship is:

```text
EPM
  = engineering meaning and validity

PEM
  = execution semantics and control

AESM Operational Model
  = authoritative operational representation

Agent Execution Contract
  = participant interaction boundary

Phase Lifecycle Workflow
  = governance of AESM specification development
```

The Phase Lifecycle Workflow does not execute an engineering Process Instance. It governs how the AESM specification itself is developed and controlled.

---

## 24. Baseline Intent

This document is established from the successful lifecycle demonstrated by Phases 3 and 4 and is intended to be retrospectively audited against Phases 1–4 before becoming the frozen project governance baseline.

The retrospective audit shall determine whether any control is missing, incorrectly generalized, or inconsistent with actual successful practice.
