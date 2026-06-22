---
name: project-init
description: "Orchestrates new app project setup after /project-designer confirms the scope is an app. Fires the planning worker skills in dependency order, enforces a confirmation gate between each, and refuses to allow code until all planning docs exist. Conductor only — does not do intake or planning work itself. Invoke with /project-init or when /project-designer hands off a confirmed app scope."
---

project-init — New App Project Conductor
What this skill is
A conductor. It does not ask intake questions or write docs.
It fires worker skills in order and enforces the gate between each.
Precondition
Requires confirmed /project-designer output (Problem / Goals /
Constraints). If missing, say:
"I need a confirmed project scope first — run /project-designer."
Pass that scope to project-intake. Do not re-ask what the
designer already captured.
The chain — fire one at a time, gate between each

project-intake    → PROJECT_BRIEF.md
(feed designer scope; ask ONLY app-specific gaps:
file formats, hosting, auth, integrations)
workflow-mapper   → WORKFLOW_TIMELINE.md
data-modeler      → DATA_MODEL.md
state-classifier  → STATE_CLASSIFICATION.md
test-planner      → TEST_STRATEGY.md
uncertainty-log   → ASSUMPTIONS_AND_OPEN_QUESTIONS.md

Ambient — active throughout

dev-contract — baseline rules, always on
repo-trim — runs on every doc, enforce 800-word cap

Progress display
Show at each step: ✅ Complete / ⚙️ Current / ⬜ Pending
Rules

Never run two steps without a confirmation between them
Never skip a step because it seems obvious
No code until all six docs exist and are confirmed
If the user pushes to code early, surface what is missing
Fire the worker skills — never write their docs yourself

Step 7 — generate CLAUDE.md
After all six docs are confirmed, produce CLAUDE.md at the repo root:

# [Project Name]

## What this is
[one line from PROJECT_BRIEF]

## What it owns
[from DATA_MODEL and STATE_CLASSIFICATION]

## What the caller provides
[from WORKFLOW_TIMELINE and ASSUMPTIONS]

## Architecture
[from ARCHITECTURE_SELECTION]

## Never do this
[must-never-happen rules from DATA_MODEL and STATE_CLASSIFICATION]

## Commands
[test, lint, run commands from PROJECT_BRIEF]

Exit condition
When all six docs and CLAUDE.md are confirmed:
"Planning complete. CLAUDE.md and all six docs confirmed. Ready for code."
Hand off to build work or /add-feature for the first capability.