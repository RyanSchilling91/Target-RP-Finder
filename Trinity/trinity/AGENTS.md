# Trinity — Agent Orientation

## What this is

Trinity is a drop-in SQLite persistence layer for workflow-governed applications.
Drop the `trinity/` folder into your project root to get:

- Database setup and schema initialization
- Working-state save/load/delete for mutable run/revision data
- Single-editor lock acquisition, heartbeat, release, and forced override
- Append-only audit event logging
- Session context and identity contracts

## What Trinity owns

| Module | Responsibility |
|---|---|
| `db.py` | Database bootstrap, schema initialization, metadata |
| `working_state.py` | Save/load/delete mutable working state per revision |
| `lock_manager.py` | Acquire, renew, release, and force-release editor locks |
| `audit_log.py` | Append-only audit event recording and querying |
| `session.py` | Session context creation and resolution |

## What Trinity does NOT own

Trinity is infrastructure only. These belong to your application's service layer:

- Workflow state transitions and lifecycle rules
- Review independence and authorization policy
- Publish and reopen policy
- Domain-specific validation logic
- Any UI framework coupling

## Integration rules

- Initialize via `TrinityDB(DBConfig(...)).initialize()` — see `db.py`
- Implement each contract class in your service layer; every method raises `NotImplementedError` until implemented
- Workflow policy (valid status values, review rules, publish/reopen logic) belongs in the caller — never inside Trinity
- Run status and revision status are unconstrained TEXT — the caller enforces valid values

## Schema

`SCHEMA.md` — full table definitions, constraints, and executable SQL.

## Tests

`pytest trinity/tests/` from project root.
