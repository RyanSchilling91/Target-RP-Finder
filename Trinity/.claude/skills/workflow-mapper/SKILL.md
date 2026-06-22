---
name: workflow-mapper
description: "Maps the real-world workflow before any feature is implemented. Forces chronological sequencing of human and system actions, identifies state impact at each step, and surfaces edge cases before they become bugs."
---

# workflow-mapper — Workflow Timeline Extraction

## Before any feature implementation
Do not design data models or write code until the workflow 
is mapped and confirmed.

## Intake sequence
Ask one question at a time. Wait for answer before continuing.

1. What triggers this workflow — what does the user do first?
2. What does the system do in response?
3. What does the user do next — and what can go wrong here?
4. Where does data get created, changed, or frozen?
5. Who hands off to whom — and what do they pass?
6. What are the edge cases — missing data, failures, cancellations?

## Output — produce WORKFLOW_TIMELINE.md containing
- Step-by-step table: step number, actor, action, 
  data touched, system response, state impact
- Review and approval points — what can still change vs. what freezes
- Handoff points — who passes what to whom
- Edge cases and alternate paths — one entry per failure mode

## Rules
- Every step must identify actor (human or system)
- Every step must identify state impact (working / derived / evidence)
- No step can be skipped because it seems obvious
- Edge cases are required — a workflow with no edge cases 
  is an incomplete workflow

## Confirmation gate
After producing the timeline, ask:
"Does this match how the workflow actually runs — 
or are there steps or edge cases we missed?"

Do not proceed to data modeling until confirmed.