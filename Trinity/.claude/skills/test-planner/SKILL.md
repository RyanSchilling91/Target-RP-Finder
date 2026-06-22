---
name: test-planner
description: "Defines test targets, fixtures, edge cases, and correctness criteria before any feature is called complete. Ensures business rules have automated coverage and bugs produce regression tests."
---

# test-planner — Test Strategy Definition

## Before any feature is called complete
Do not mark work done until test targets are defined 
and core business rules have automated coverage.

## Intake sequence
Ask one question at a time. Wait for answer before continuing.

1. What are the core business rules that must never break?
2. What does correct behavior look like — in plain language?
3. What are the edge cases — missing data, failures, 
   boundary conditions?
4. What fixtures are needed — known good data, malformed data, 
   persisted state snapshots?
5. What workflows need end-to-end coverage?
6. What has broken before that must never break again?

## Output — produce TEST_STRATEGY.md containing
- Test scope summary
- Unit test targets — rule, why it matters, minimum cases
- Integration targets — workflow, modules involved, expected result
- Regression scenarios — historical failures, expected guardrail
- Required fixtures — good data, bad data, edge state snapshots
- Correctness definition — plain language statement of correct behavior
- Manual validation — what supplements but never replaces automation

## Rules
- Core business rules require automated tests — no exceptions
- Every bug fix requires a regression test or documented reason why not
- Happy path only is not sufficient — edge cases are required
- Manual testing alone never satisfies a core business rule
- Fixtures must include malformed and partial state — not just clean data

## Confirmation gate
After producing the strategy, ask:
"Does this cover every rule and failure mode that matters — 
or are there gaps in coverage or missing fixtures?"