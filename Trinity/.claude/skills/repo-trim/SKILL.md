---
name: repo-trim
description: "Enforces the 800-word cap on every repo doc update. Strips planning docs to verification-relevant content only — the skeleton stays in skills, the muscle stays in docs. Invoked any time a repo doc is created or updated."
---

repo-trim — Repository Doc Enforcement
Core rule
Repo docs are verification layers, not tutorials.
Every doc must answer: "does the implementation match the plan?"
Nothing else earns a place in the doc.
Word cap
Hard limit: 800 words per doc.
If over 800 — cut, do not summarize.
What survives a trim
Keep:

Decisions and their rationale — one sentence each
Rules that constrain implementation behavior
Must-never-happen statements
Verification criteria — observable, measurable
Current state of entities, workflows, or gates

Cut:

Background context that restates what code already shows
Prose that explains what a skill already enforces
Historical narrative — move to RETROSPECTIVE.md or ADR
Any content that exists only to explain skill behavior

On every doc write or update

Write the content
Count the words
If over 800 — cut the lowest-value content first
Confirm what remains answers: "does this match the skeleton?"

Doc-specific trim rules

PROJECT_BRIEF.md — problem, users, scope, constraints, success criteria
WORKFLOW_TIMELINE.md — step table, edge cases, freeze points
DATA_MODEL.md — entities, identifiers, fields, forbidden states
STATE_CLASSIFICATION.md — classification table, mutability rules
FAILURE_CATALOG.md — symptom, root cause, prevention rule per entry
QUALITY_GATES.md — gate checklist and completion statement
ASSUMPTIONS — open items, risk, and decision trigger only

Never do this

Allow a doc past 800 words without trimming
Keep content that duplicates skill behavior
Treat length as thoroughness