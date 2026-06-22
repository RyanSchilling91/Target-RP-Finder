---
name: data-modeler
description: "Defines core entities, ownership boundaries, identifiers, lifecycle states, relationships, and forbidden states before any schema or persistence is designed. Output is a confirmed DATA_MODEL.md."
---

# data-modeler — Entity and Data Model Definition

## Before any schema or persistence design
Do not design tables, collections, or storage structures until 
the data model is mapped and confirmed.

## Intake sequence
Ask one question at a time. Wait for answer before continuing.

1. What are the core real-world objects in this system?
2. What uniquely identifies each one — business key or system key?
3. Who owns each entity — user or system?
4. What fields does each entity carry and do they change over time?
5. What are the relationships — what belongs to what?
6. What states can each entity be in across its lifecycle?
7. What must never happen to this data?

## Output — produce DATA_MODEL.md containing
- One section per entity with:
  - What it is
  - Identifier — business key and/or system key
  - Fields — name, type, required, owner, changes over time
  - Allowed states
  - Must never happen rules
- Derived values section — what is computed, never stored
- Entity relationship summary
- Forbidden state transitions table

## Rules
- Every entity needs an explicit identifier — no anonymous records
- Derived values must be called out and kept out of the entity model
- Must-never-happen rules are required for every entity
- Ownership must be explicit — system-owned vs user-owned fields

## Confirmation gate
After producing the model, ask:
"Does this capture every entity and its rules accurately — 
or are there missing objects, fields, or forbidden states?"

Do not proceed to state classification until confirmed.