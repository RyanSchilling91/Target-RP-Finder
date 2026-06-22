---
name: dev-contract
description: "Baseline operating rules for every coding session. Enforces architecture boundaries, state classification, persistence safety, testing requirements, and end-of-task reporting. Applies to every task — not invoked manually."
---

# dev-contract — Agent Operating Rules

## Before any code
- If planning docs are missing or weak, surface the gap — do not invent requirements
- If uncertainty affects architecture, persistence, security, or workflow 
  correctness, log it in ASSUMPTIONS_AND_OPEN_QUESTIONS.md before proceeding

## Architecture rules
- UI files are presentation only — no business logic, no persistence, 
  no routing decisions
- Business rules live in domain/service modules
- Persistence logic lives in persistence modules
- The UI framework must be replaceable without rewriting the core
- Hard file limit: 350 lines. Soft limit: 250. Prefer small focused modules.

## State rules
- Classify all data as working, derived, or evidence before designing persistence
- Working state is mutable and pre-commit only
- Derived state is recomputable — never promote it to source truth
- Evidence state is immutable after commit — never overwrite in place
- Rework creates a new version, never mutates existing evidence

## Persistence rules
- Before any schema change, locate all save, load, and rehydrate paths
- Wrap all writes in transactions — never allow partial commits
- Document source of truth, versioning, and recovery expectations

## Testing rules
- New business rules require automated tests
- Bug fixes require regression tests
- Core logic cannot rely on manual testing alone

## End of every task
Report:
- Files changed and why
- Tests run and results
- Docs updated
- Known risks or deferrals
- Whether quality gates are met