---
name: debug
description: "Orchestrates disciplined bug fixing on an existing project. failure-memory bookends the work — check the catalog before touching anything, record the lesson after. Conductor only. Invoke with /debug or when behavior diverges from expected and an error or failure is described."
---

debug — Disciplined Bug Fixing Conductor
What this skill is
A conductor that wraps bug fixing in failure-catalog discipline.
Check memory first, fix at root cause, record the lesson so the
bug never repeats.
Step 1 — route
Fire doc-router to load FAILURE_CATALOG, TEST_STRATEGY, and the
planning docs for the affected area.
Step 2 — check memory BEFORE touching code
Fire failure-memory. Is this a known landmine?
If the pattern exists in the catalog — treat it as a regression.
Do not re-discover it the hard way.
Step 3 — root cause, not symptom
Reproduce. Isolate. Identify what actually caused it — not just
where it surfaced. Do not patch the symptom and move on.
Step 4 — fix, then record
After the fix, fire failure-memory to record:

Symptom — what the user experienced
Root cause — what actually caused it
Detection gap — why tests or reasoning missed it
Prevention rule — what changes so it cannot recur
Regression test — added, or reason documented why not

Step 5 — gate
Fire done-checker. A fix is not done until the regression test
passes and the catalog entry exists.
Ambient

dev-contract — baseline rules, always on

Rules

Never fix a symptom without finding root cause
Never close a fix without a catalog entry
Never skip the regression test without documenting why
If the bug reveals a process weakness, propose a rule change
in RETROSPECTIVE.md

Exit condition
"Fixed at root cause. Regression test passing. Catalog updated."