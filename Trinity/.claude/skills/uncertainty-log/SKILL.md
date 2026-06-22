---
name: uncertainty-log
description: "Captures assumptions, open questions, and deferred decisions so the agent logs uncertainty instead of guessing behavior into code. Updated continuously throughout development — not a one-time artifact."
---

# uncertainty-log — Assumptions and Open Questions

## Core rule
Never silently resolve ambiguity in code. If something is uncertain,
log it here first. Ask for resolution or explicit deferral.

## When to update this doc
- When a requirement has multiple valid interpretations
- When an architecture choice depends on an unanswered question
- When a risk is identified but not yet mitigated
- When a decision is deferred — log why and what it blocks
- When an assumption is being carried forward unverified

## Log format per entry

### Assumptions
- Assumption — what is being assumed
- Why assumed — reason it was not verified
- Risk if wrong — what breaks
- Mitigation — how to verify or limit damage
- Decision trigger — when this must be resolved

### Open questions
- Question — what is unresolved
- Why it matters — what it affects
- Risk of deferring — what could go wrong
- Decision trigger — when this must be resolved

### Deferred decisions
- Decision — what was deferred
- Why deferred — reason
- Maximum delay — what work is blocked

## Blocking rule
If an unresolved item affects architecture, persistence, security, 
workflow correctness, or release behavior — treat it as blocking 
unless explicitly deferred with documented risk.

## Never do this
Do not answer open questions silently in code.
Do not proceed past a blocking unknown without explicit deferral.