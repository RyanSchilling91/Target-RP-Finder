---
name: done-checker
description: "Defines and enforces the completion bar before any merge or release. Prevents work from being called done without evidence that quality gates have been met."
---

# done-checker — Quality Gate Enforcement

## Core rule
Work is not done until every applicable gate has evidence.
"It works on my machine" is not evidence.

## Gate checklist — run before every merge or release

### Always required
- [ ] Planning docs reflect the implementation
- [ ] Required tests pass — output captured, not assumed
- [ ] Workflow matches documented behavior
- [ ] Known blockers resolved or explicitly deferred with risk logged

### Required when persistence is touched
- [ ] State persists correctly across refresh, restart, reload
- [ ] Schema version is explicit
- [ ] Forward migration tested
- [ ] Partial or damaged state handling tested
- [ ] Rollback path defined

### Required when auth or permissions are touched
- [ ] Role and session edge cases tested
- [ ] Unauthorized access paths verified

### Required for every bug fix
- [ ] Root cause identified
- [ ] Regression test added or reason documented
- [ ] FAILURE_CATALOG.md updated
- [ ] Process or rule change proposed if pattern is systemic

## Completion statement — required output
Before closing any task, report:
- Tests run and results
- Docs updated
- Gates met — list which applied
- Known risks or deferrals — with explicit acknowledgment

## Blocking rule
If a required gate cannot be met, it must be explicitly deferred 
with documented risk. Silent skipping is never acceptable.
A deferred gate is not a failed gate — an unacknowledged gate is.