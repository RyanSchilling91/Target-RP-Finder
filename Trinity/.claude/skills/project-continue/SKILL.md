---
name: project-continue
description: "Resumes work on an existing app project. Loads the planning docs, reports current state and open unknowns, then routes to the right next conductor based on what the user is doing this session. Conductor only. Invoke with /project-continue at the start of a working session on an existing project."
---

project-continue — Resume Session Conductor
What this skill is
The front door for an existing project. It does not build or fix
anything itself. It orients, then routes to the right conductor.
Precondition
Existing project with planning docs in place. If none exist:
"No planning docs found — run /project-designer then /project-init."
Step 1 — load and orient
Fire doc-router to load PROJECT_BRIEF, ASSUMPTIONS_AND_OPEN_QUESTIONS,
and the most recent RETROSPECTIVE entry.
Step 2 — report current state
Tell the user, briefly:

What the project is (one line from the brief)
What open unknowns or deferred decisions are still live
What was last worked on, if the retrospective shows it

Step 3 — ask what this session is for
Ask one question:
"What are we working on this session?"
Step 4 — route to the right conductor
Based on the answer:

New capability        → hand off to /add-feature
Something is broken    → hand off to /debug
More planning needed   → fire the specific worker skill needed
Architecture change    → load ARCHITECTURE_SELECTION + relevant ADRs

Ambient

dev-contract — baseline rules, always on

Rules

Do not start building or fixing from this skill — route first
Always report open unknowns before new work begins
If open unknowns block the session's goal, surface that before
routing — a live blocker is addressed before new work starts

Exit condition
Hand off cleanly to the chosen conductor with context loaded.