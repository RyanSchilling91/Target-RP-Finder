---
name: add-feature-description
description: "Orchestrates adding a new capability to an existing app project. Unlike project-init, runs a SELECTIVE chain — only the worker skills the feature actually touches. Conductor only. Invoke with /add-feature or when the user describes new capability on an existing project."
---

add-feature — New Capability Conductor
What this skill is
A conductor for additive work. It does not run the full init
chain. It fires only the bones the feature actually needs.
Precondition
Existing project with planning docs in place. If none exist:
"This looks new — run /project-designer then /project-init."
Step 1 — route first
Fire doc-router to load only the docs this feature touches.
Read them before anything else.
Step 2 — fire only what applies
Run a worker skill ONLY if the feature triggers it:

workflow-mapper   → IF it adds a new user/system flow
data-modeler      → IF it adds or changes entities
state-classifier  → IF it touches persistence
test-planner      → ALWAYS (new capability = new coverage)
Gate between each skill that fires. Skip the rest.

Step 3 — before risky code
Fire failure-memory — check the catalog for known landmines
in this area before writing anything.
Step 4 — gate the merge
Fire done-checker before the feature is called complete.
Ambient — active throughout

dev-contract — baseline rules, always on
repo-trim — runs on every doc updated

Progress display
Show which skills will fire, then:
✅ Complete / ⚙️ Current / ⬜ Pending
Rules

Do not run the full init chain — this is selective
test-planner always fires; the rest are conditional
Update docs the feature touches — do not create new ones
unless the feature adds a genuinely new surface
No merge until done-checker passes

Exit condition
"Feature complete. Docs updated, tests pass, gates met."