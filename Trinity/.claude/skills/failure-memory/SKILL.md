---
name: failure-memory
description: "Records known failure patterns before touching risky code and updates the catalog after every bug. Prevents repeated mistakes across sessions by treating the failure catalog as active engineering memory, not a post-mortem archive."
---

failure-memory — Failure Catalog Enforcement
Before touching risky behavior
Check FAILURE_CATALOG.md first.
Risky behavior includes: persistence changes, state mutations,
UI/session logic, concurrency, auth, migrations, publish/archive flows.
If the failure pattern already exists — treat it as a regression
landmine. Do not proceed without explicitly addressing it.
After every bug, defect, or unexpected behavior
A fix is incomplete until all four of these are done:

Root cause identified — not just the symptom
Regression test added — or reason documented why not
FAILURE_CATALOG.md updated with:

Symptom — what the user experienced
Root cause — what actually caused it
Detection gap — why existing tests or reasoning missed it
Prevention rule — what changes in process, tests, or architecture


If the pattern is systemic — propose a rule change in RETROSPECTIVE.md

Catalog entry format
[Failure title]
Symptom
Root cause
Detection gap
Prevention rule
Regression test / guardrail
Core rule
Never treat a bug fix as complete without a catalog entry.
A fix that leaves no memory is a fix that will be repeated.
Never do this

Fix the symptom without identifying root cause
Skip the catalog entry because the bug seemed minor
Proceed past a known failure pattern without acknowledging it