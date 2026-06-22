---
name: state-classifier
description: "Classifies all data as working, derived, or evidence before any persistence is designed. Prevents derived data from becoming source truth and evidence from being silently overwritten."
---

# state-classifier — Data State Classification

## Before any persistence design
Do not design storage, schemas, or write paths until all 
data is classified and confirmed.

## The three classifications
- Working — mutable, pre-commit, discarded on cancel
- Derived — computed from source, never stored as canonical truth
- Evidence — immutable after commit, never overwritten in place

## Intake sequence
Ask one question at a time. Wait for answer before continuing.

1. What data exists only before the user confirms — and is 
   discarded on cancel?
2. What data is computed from other data and never entered directly?
3. What data is frozen after the user confirms an action?
4. What is the only mechanism to correct evidence state?
5. What derived values are displayed but must never be persisted?

## Output — produce STATE_CLASSIFICATION.md containing
- Classification table — every data element mapped to 
  working / derived / evidence
- Mutability rules — what can change before commit, 
  what freezes after
- Derived state rules — source, computed at, never stored as
- Versioning behavior — how corrections create new versions
- Forbidden state transitions table

## Rules
- Every data element must have exactly one classification
- Derived values must list their source and recomputation rule
- Evidence state must define its correction mechanism
- No persistence design proceeds until this doc is confirmed

## Confirmation gate
After producing the classification, ask:
"Does every piece of data have the right classification — 
or are there elements that are misclassified or missing?"

Do not proceed to architecture selection until confirmed.