<!--
Sync Impact Report
- Version change: (none) -> 1.0.0
- Modified principles: N/A (initial adoption)
- Added sections: Core Principles; Additional Constraints; Development Workflow; Governance
- Removed sections: None
- Templates requiring updates: 
	* .specify/templates/plan-template.md ✅ (added Constitution gates)
	* .specify/templates/tasks-template.md ✅ (testing + clarity references)
	* .specify/templates/spec-template.md ⚠ (pending UX style guide reference)
- Deferred TODOs: TODO(UX_STYLE_GUIDE): Create initial UX style guide for messages & errors
-->

# CSC299 Project Constitution

## Core Principles

### I. Code Clarity & Simplicity
Rules:
- Code MUST prioritize readability over cleverness; prefer explicit over implicit constructs.
- Each function MUST have a single, clear responsibility; nesting depth SHOULD NOT exceed 3 levels.
- Public APIs MUST use descriptive names and minimal, well-typed parameters.
- Dead or commented-out code MUST be removed in the same PR it is identified.
- Refactoring for clarity MUST NOT change behavior without corresponding tests proving equivalence.
Rationale: Clear, simple code reduces defect rates, accelerates onboarding, and lowers long‑term maintenance cost.

### II. Code Quality & Maintainability
Rules:
- All commits MUST pass linting and formatting checks; PRs failing automation MUST NOT be merged.
- Cyclomatic complexity per function MUST NOT exceed 10 unless a documented justification is added to the PR description.
- Dependencies MUST be audited quarterly; unused or stale libraries MUST be removed or upgraded.
- Non‑trivial modules (≥150 LOC or central to a feature) MUST include a top‑level doc comment stating purpose, invariants, and constraints.
- Configuration, environment flags, and feature toggles MUST be documented in a single source (e.g., `docs/config.md`).
Rationale: Consistent quality and intentional structure enable predictable evolution and safer change.

### III. Testing Standards & Coverage
Rules:
- New logic MUST include unit tests; externally visible behavior MUST include contract or integration tests.
- Global line coverage MUST be ≥80%; core/business‑critical modules MUST be ≥90%; coverage reductions REQUIRE explicit justification.
- Tests MUST be deterministic, isolated, and free of undeclared external network calls (mock or fixture required).
- Critical P1 user stories SHOULD follow a test‑first (Red‑Green‑Refactor) workflow; regressions MUST add or strengthen tests.
- Flaky tests MUST be fixed or quarantined within 48 hours; quarantined tests block release after 7 days.
Rationale: Strong, reliable tests provide change safety, enable refactoring, and expose regressions early.

### IV. User Experience Consistency
Rules:
- User‑facing messages, errors, and CLI output MUST follow a shared style (TODO(UX_STYLE_GUIDE)).
- Similar interactions (validation, error codes, retries) MUST behave consistently across modules.
- Breaking UX changes (altering workflows, semantics, or required flags) REQUIRE a MINOR or MAJOR version bump depending on impact scope.
- Defaults MUST be safe, predictable, and documented; implicit side effects are prohibited.
- CLI/help output MUST remain scriptable (stable flags) unless a deprecation notice with migration guidance is published.
Rationale: Consistent experiences build trust, reduce support burden, and improve adoption.

## Additional Constraints

- Favor standard library and well‑maintained dependencies over custom abstractions (YAGNI principle enforced).
- Performance optimizations MUST follow measurable bottleneck evidence (profiling or metrics) before complexity is introduced.
- Security baseline: input validation mandatory for all external data; secrets MUST NOT be hard‑coded.
- Naming conventions: clear, intention‑revealing names; avoid abbreviations except widely recognized (e.g., `id`, `url`).
- Cross‑cutting changes impacting multiple principles MUST include an Impact section in the PR description citing affected rules.

## Development Workflow

- PR Description MUST map changes to principle rules when non‑trivial (≥50 LOC or new feature).
- Code Review Checklist MUST include: Clarity, Complexity Justification (if >10), Tests Added/Updated, UX Consistency.
- Complexity Justification Table (if any variances) MUST follow: Reason, Simpler Alternative Rejected, Future Simplification Path.
- Decision Records (ADR) REQUIRED for architectural changes (new service/module, data store, protocol) and MUST reference principles.
- Merge Gate: all principle violations resolved OR explicitly justified with time‑boxed remediation task.

## Governance

Authority & Scope:
- This constitution supersedes ad hoc practices; conflicting conventions MUST be aligned or retired.

Amendments:
- Proposal submitted via PR labeled `constitution-change` including: diff, rationale, impact analysis, version bump reasoning.
- Requires ≥2 maintainer approvals OR 1 maintainer + documented community review (meeting notes or async summary).
- Migration plan REQUIRED for removals or redefinitions affecting active workstreams.

Versioning Policy (Semantic):
- MAJOR: Removal/redefinition of principles or governance altering enforcement scope.
- MINOR: Addition of new principle or substantial expansion of rules.
- PATCH: Clarifications, wording improvements, non‑semantic refinements.

Compliance & Review:
- Quarterly compliance audit: sample PRs checked for adherence; findings logged in `docs/governance-audit.md`.
- Violations tracked with remediation tasks; unresolved critical violations escalate to maintainers within 7 days.

Runtime Guidance:
- Developers MUST reference this file when drafting plan or spec documents (see Constitution Check section in `plan-template.md`).
- Style guide TODO(UX_STYLE_GUIDE) MUST be created before first public release milestone.

Enforcement:
- Automated CI gates (lint, tests, coverage) MUST block merges failing quality or coverage thresholds.
- Manual review enforces clarity, UX, complexity rules until automation extended.

**Version**: 1.0.0 | **Ratified**: 2025-11-19 | **Last Amended**: 2025-11-19
