---
name: doc-router
description: "Routes the agent to the correct planning docs before any task begins. Prevents full-doc reads on every session by matching task type to the minimum required doc subset."
---

# doc-router — Task-Based Doc Navigation

## On every task, identify the type first
Do not read all docs. Read only the subset required for the task type.

## Task routing

### New feature or workflow implementation
- WORKFLOW_TIMELINE.md
- DATA_MODEL.md
- STATE_CLASSIFICATION.md

### Persistence, schema, or migration change
- ARCHITECTURE_SELECTION.md
- DATA_MODEL.md
- STATE_CLASSIFICATION.md
- FAILURE_CATALOG.md

### Bug fix or regression
- FAILURE_CATALOG.md
- TEST_STRATEGY.md
- QUALITY_GATES.md

### Auth, roles, or permissions change
- PROJECT_BRIEF.md
- DATA_MODEL.md
- TEST_STRATEGY.md

### New project or architecture decision
- PROJECT_BRIEF.md
- WORKFLOW_TIMELINE.md
- ARCHITECTURE_SELECTION.md
- DATA_MODEL.md
- STATE_CLASSIFICATION.md

### Release or merge readiness
- QUALITY_GATES.md
- TEST_STRATEGY.md
- ASSUMPTIONS_AND_OPEN_QUESTIONS.md

## Blocking rule
If a required doc for the task type is missing or blank — stop.
Surface the gap to the user before proceeding.

## Default rule
When task type is ambiguous, default to:
- PROJECT_BRIEF.md
- WORKFLOW_TIMELINE.md
- FAILURE_CATALOG.md