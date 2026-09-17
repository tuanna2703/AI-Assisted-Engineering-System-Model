# DBP Empirical Execution — Experiment Boundary

**Status:** Prepared — execution not started.

**Purpose:** Define the controlled boundary and evidence contract for the first real engineering task used to determine whether AESM actually participates in Agent execution.

## Experiment Objective

Execute one real, narrowly scoped Directories Builder Pro engineering request through the established Agent / Execution Environment / AESM Runtime mechanism.

The experiment is testing **AESM participation**, not merely successful code modification.

The central question is:

> When a human gives an Agent a real engineering request, does the Agent actually use the AESM process, Runtime, Process Instance, and Execution Context to govern and record the work?

## Controlled Engineering Request

Repository: `tuanna2703/directories-builder-pro`

### Requirements: Hierarchical Categories Filter

#### REQ-01 — Data: Category Tree with Counts

The system must provide a structured category tree where each parent category includes its listing count and an array of child categories with their individual listing counts. Counts must reflect the **full directory** (all active businesses, regardless of the current search query). The tree must only include terms from the `dbp_business_category` taxonomy.

#### REQ-02 — Data: "All Categories" Aggregate Count

The "All Categories" row must display the **total count of all active businesses** in the directory. This is the sum across all parent categories and must be computed server-side.

#### REQ-03 — Backend: Repository Query

All database queries required to build the category tree and counts must be encapsulated inside a dedicated Repository class method. No inline `$wpdb` calls are permitted outside the Repository layer (ADR-0007). The method must use `$wpdb->prepare()` for all dynamic parameters.

#### REQ-04 — Backend: AJAX Endpoint

A new public AJAX action `dbp_get_category_tree` must be registered via `Ajax_Manager::register_action()` in `search-module.php`. It must be accessible to both authenticated and unauthenticated users (`wp_ajax_` and `wp_ajax_nopriv_`). It must validate a nonce before processing. It must return a JSON response containing the category tree array.

#### REQ-05 — Backend: Hot-Removability Compliance

If the `Business_Category_Module` is removed, the `dbp_get_category_tree` AJAX handler must degrade gracefully with zero PHP fatal errors. The Search Module must not directly import or instantiate any class from the Business Category Module (ADR-0004).

#### REQ-06 — Template: Panel Structure

`templates/search/results.php` must be updated to replace the existing flat category button list with the new hierarchical panel. The template must include a PHP docblock at the top declaring the `@args` contract, specifying `$category_tree` (array) and `$active_category_slug` (string) as its input variables.

#### REQ-07 — Template: Panel Header

The panel must render a header row containing the label "Category" and a chevron icon. The header must act as the collapse/expand toggle for the panel body. The chevron icon must be rendered via `Icon_Manager::render('chevron-down')`. No inline SVG is permitted.

#### REQ-08 — Template: "All Categories" Row

The first row of the list must be an "All Categories" item displaying the aggregate business count (REQ-02) on the right. It must carry the active state styling by default on initial page load. It must include `aria-selected="true"` when active.

#### REQ-09 — Template: Parent Category Rows

Each parent category must render as a list row displaying the category name on the left and its listing count on the right. Each row must carry a `data-category-slug` attribute set to the category's slug. Rows for categories that have children must additionally carry a `data-has-children="true"` attribute.

#### REQ-10 — Template: Child Category Sub-list

Each parent category that has children must have a corresponding child sub-list rendered in the DOM immediately beneath its parent row. The child sub-list must be hidden by default using the `.dbp-hidden` utility class. Each child row must carry its own `data-category-slug` attribute. The sub-list must carry a `data-parent-slug` attribute matching its parent's slug so JavaScript can target it.

#### REQ-11 — Template: "See More" Button

The panel must display a "See More" button below the category list. On initial render, only the first **12** parent category rows must be visible; all rows beyond index 12 must carry a class that hides them. The button must carry an `aria-expanded="false"` attribute on initial render.

#### REQ-12 — Template: BEM and Token Compliance

All HTML elements in the panel must use BEM class names prefixed with `dbp-` (e.g. `.dbp-category-filter`, `.dbp-category-filter__header`, `.dbp-category-filter__item`). No inline `style=""` attributes are permitted except for dynamically computed runtime values. All icons must be rendered via `Icon_Manager::render()`.

#### REQ-13 — Template: Accessibility

The category list must use `role="listbox"` and `aria-label="Filter by category"`. Each row item must use `role="option"`. The active row must carry `aria-selected="true"`; all others must carry `aria-selected="false"`. Each count span must carry an `aria-label` with the full readable value (e.g. `aria-label="12 listings"`). The "See More" button must update its `aria-expanded` attribute to reflect its current state.

#### REQ-14 — JavaScript: Panel Collapse/Expand

Clicking the panel header must toggle the panel between collapsed and expanded states. The chevron icon must rotate 180° when the panel is expanded. The transition must respect the `--dbp-transition-duration` and `--dbp-transition-ease` tokens. The panel initial state must be expanded across all screen sizes.

#### REQ-15 — JavaScript: "See More" Expansion

Clicking "See More" must reveal all hidden parent category rows beyond the initial 12. The button label must change to "See Less". Clicking "See Less" must re-hide those rows and restore the label. The `aria-expanded` attribute on the button must be updated to reflect the current state after each click.

#### REQ-16 — JavaScript: Parent Category Selection

Clicking a parent category row must remove the active state from all other rows and apply it to the clicked row. If the clicked row carries `data-has-children="true"`, the matching child sub-list must be revealed inline beneath the row. Any previously expanded child sub-list must be collapsed before the new one is revealed. The active state must also be cleared from any previously selected child row.

#### REQ-17 — JavaScript: Child Category Selection

Clicking a child category row must remove the active state from all other rows and apply it to the clicked child row. The parent row of the selected child must retain a visual indicator that it is the active parent context (a distinct style separate from the fully active state, to be defined in CSS). Clicking a different parent must collapse the current child sub-list.

#### REQ-18 — JavaScript: "All Categories" Selection

Clicking the "All Categories" row must clear the active state from all other rows, apply the active state to "All Categories", and collapse any open child sub-list. The search results must refresh to show all listings with no category filter applied.

#### REQ-19 — JavaScript: Search Integration

Selecting any category row (parent, child, or "All Categories") must trigger the existing `dbp_search` AJAX action, passing the selected `category_slug` as a query parameter (or an empty value for "All Categories"). The results grid must display the loading skeleton during the request, following the existing 200ms delay rule. Focus must be moved to the search results header node after results load (per Interaction Guidelines).

#### REQ-20 — JavaScript: URL State

Selecting a category must update the browser URL query string (e.g. `?category=arts-humanities`) without triggering a full page reload, using the History API (`pushState`). On page load, if a `category` query parameter is present in the URL, the matching category row must be pre-selected and its child sub-list expanded if applicable.

#### REQ-21 — Styling: New BEM Block

A new BEM block `.dbp-category-filter` must be added to `assets/css/frontend.css`. All color, spacing, typography, border radius, shadow, and transition values must reference CSS custom properties from `variables.css`. No hardcoded hex values, pixel sizes, or raw color names are permitted.

#### REQ-22 — Styling: Active and Hover States

The active category row name must render in bold (`font-weight: 700`) with an underline, matching the visual shown in the reference image. Hover states on non-active rows must provide a subtle background shift using `--dbp-color-neutral-100`. The active state and hover state must each be achievable without JavaScript class toggling (CSS `:hover` for hover; JS-toggled `.is-active` class for selection).

#### REQ-23 — Styling: Child Row Indentation

Child category rows must be visually indented relative to parent rows using `padding-left: var(--dbp-space-6)` to communicate hierarchy without additional icons or decorators.

#### REQ-24 — Styling: Count Column Alignment

Listing counts must be right-aligned in each row. The layout must use `display: flex; justify-content: space-between` on each row item so the name and count columns remain consistently aligned regardless of name length. Count text must use `--dbp-color-neutral-600` and `--dbp-text-sm`.

#### REQ-25 — Styling: "See More" Button Appearance

The "See More" / "See Less" button must be centered horizontally at the bottom of the panel, styled using the existing `.dbp-button--ghost` variant with `--dbp-color-primary` text color and `font-weight: 600`, matching the visual in the reference image.

#### REQ-26 — Documentation Updates

The following documentation files must be updated upon completion:

- `docs/modules/search.md` — new AJAX endpoint `dbp_get_category_tree` added to Core API Surfaces; template change noted in Templates section
- `docs/api/hooks.md` — new AJAX action added to the Action Hooks table
- `docs/ui/frontend-components.md` — Search Filters section updated to describe the hierarchical category panel
- `docs/ui/css-architecture.md` — new `.dbp-category-filter` block noted under `frontend.css`
- `CHANGELOG.md` — factual entry added under the current version block

The Agent may investigate the repository and determine the appropriate implementation and verification details, but the requirements above are the complete controlled engineering request for this experiment.

## Experiment Constraints

The fresh Agent must not be instructed to follow a prescribed AESM Runtime call sequence. In particular, the request must not prescribe calls such as `attach()`, `start_investigation()`, `record_artifact()`, or `begin_verification()`.

The experiment must not preload the Agent with:

- expected Process Instance state;
- expected Runtime operations;
- expected history entries;
- expected implementation details beyond the controlled request;
- an expected evidence classification;
- conclusions from prior validation sessions.

The following constraints remain binding:

- Do not modify DBP before the controlled Agent execution begins.
- Do not treat Agent statements as authoritative AESM state.
- Do not fabricate missing Runtime participation or persisted evidence.
- Do not broaden the DBP change beyond the agreed target.
- Do not modify AESM Runtime or semantics merely to make the experiment succeed.
- Do not count documentation reading alone as AESM operational participation.
- Do not declare the experiment successful merely because the DBP code change or tests succeed.

## Evidence Contract

The experiment must collect evidence sufficient to assess the following independently:

| Evidence area | Required question |
|---|---|
| Persistent guidance | Did the Agent actually receive applicable AESM guidance? |
| Process Instance | Was a real AESM Process Instance established or recovered for this task? |
| Execution Context | Did the Agent obtain authoritative context through the Runtime? |
| Engineering investigation | Did the Agent investigate the actual DBP implementation before changing it? |
| Runtime participation | Did Agent activity cause actual AESM Runtime operations? |
| State/evidence recording | Did Runtime operations produce authoritative persisted state? |
| Implementation | Was the requested DBP change actually made? |
| Verification | Was the resulting implementation independently or operationally verified? |
| Traceability | Can the engineering work be reconstructed from authoritative AESM state? |
| Agent boundary | Can Agent narrative be distinguished from Runtime/persisted evidence? |

## Authority Model for Evidence

Evidence must distinguish at least these layers:

1. **Agent said X** — narrative evidence only.
2. **Agent performed X** — observable execution evidence where available.
3. **Runtime recognized X** — authoritative Runtime result.
4. **Persisted state contains X** — authoritative persisted evidence.
5. **Independent repository verification shows X** — independently verified engineering result.

A statement in Agent conversation does not establish a Process Instance state, decision, artifact, verification, lifecycle status, or completion state unless the Runtime and/or persisted state confirms it.

## Expected Observation Sequence

The experiment should observe, without prescribing, whether the following relationship occurs:

```text
Human engineering request
        ↓
Persistent AESM guidance available to Agent
        ↓
Process Instance established/recovered
        ↓
Authoritative Execution Context obtained
        ↓
Agent investigates DBP
        ↓
AESM Runtime participates in the engineering process
        ↓
Evidence / decisions / artifacts / verification are persisted
        ↓
DBP implementation is performed
        ↓
Implementation is verified
        ↓
Authoritative process state reflects the actual work
```

This is an observation model, not a required Agent script.

## Independent DBP Verification

After Agent execution, inspect the DBP repository independently of the Agent's final narrative.

Verify at minimum:

- the implementation addresses the Hierarchical Categories Filter requirements REQ-01 through REQ-26;
- the required backend, template, JavaScript, styling, and documentation changes are present;
- no unrelated DBP modifications were introduced by the experiment;
- the resulting code is structurally/syntactically valid;
- relevant tests or verification procedures were run where applicable.

## Independent AESM Persistence Verification

Inspect the actual AESM persistence mechanism independently of the Agent's explanation.

Verify where available:

- Process Instance identity;
- Process Instance lifecycle;
- current process state;
- Execution Context contents;
- evidence;
- decisions;
- artifacts;
- verification;
- history entries;
- state/version changes;
- Runtime identifiers;
- consistency between Runtime responses and persisted files.

## Engineering Trace Assessment

Determine whether the authoritative AESM state provides a meaningful correspondence to the real DBP work.

The target trace is conceptually:

```text
request
  → investigation
  → relevant finding
  → decision
  → implementation
  → verification
  → completion
```

The experiment must determine whether this trace is actually represented by authoritative AESM state, rather than reconstructed solely from the Agent conversation.

## Result Classification

Use the established evidence categories where applicable:

- **Demonstrated** — independently observable evidence establishes the capability.
- **Evidence Incomplete** — implementation or behavior exists, but required evidence is missing.
- **Implementation Gap** — a required mechanism does not exist.
- **Specification/Applicability Decision Required** — existing authority does not determine the required behavior.
- **Not Applicable** — the capability is not applicable to this experiment.

The overall result must be evidence-based. A successful DBP implementation does not by itself establish successful AESM participation.

## Fresh-Agent Requirement

The actual DBP execution must begin from a genuinely fresh Agent invocation. The fresh Agent may receive only the information legitimately supplied through the established Execution Environment mechanism plus the controlled engineering request and any process-specific information required by that mechanism.

Prior mechanism-validation conclusions must not be injected as expected execution outcomes.

## Completion Condition

This boundary artifact is complete when the experiment has been executed and a dedicated empirical execution report records the actual observations, independently verified DBP result, independently verified AESM persistence, discrepancies, limitations, classifications, and final conclusion.

Until then, the DBP empirical result remains **undetermined**.
