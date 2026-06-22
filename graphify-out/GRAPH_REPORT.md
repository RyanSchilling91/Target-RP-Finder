# Graph Report - .  (2026-06-22)

## Corpus Check
- Corpus is ~47,159 words - fits in a single context window. You may not need a graph.

## Summary
- 314 nodes · 556 edges · 17 communities (13 shown, 4 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 75 edges (avg confidence: 0.74)
- Token cost: 305,854 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Trinity DB Engine|Trinity DB Engine]]
- [[_COMMUNITY_ADR Concurrency & Evidence Rules|ADR Concurrency & Evidence Rules]]
- [[_COMMUNITY_Failure Catalog|Failure Catalog]]
- [[_COMMUNITY_RP Finder Planning Docs|RP Finder Planning Docs]]
- [[_COMMUNITY_Project Skill Conductors|Project Skill Conductors]]
- [[_COMMUNITY_Lock Manager Tests|Lock Manager Tests]]
- [[_COMMUNITY_Lock Manager Module|Lock Manager Module]]
- [[_COMMUNITY_Dev Workflow Skills|Dev Workflow Skills]]
- [[_COMMUNITY_Data Model & Audit Log|Data Model & Audit Log]]
- [[_COMMUNITY_Session Contracts|Session Contracts]]
- [[_COMMUNITY_Working State Contracts|Working State Contracts]]
- [[_COMMUNITY_Architecture ADRs & House Rules|Architecture ADRs & House Rules]]
- [[_COMMUNITY_Trinity Schema & Modules|Trinity Schema & Modules]]
- [[_COMMUNITY_Judgment Skills|Judgment Skills]]
- [[_COMMUNITY_RP Finder Sample Discovery|RP Finder Sample Discovery]]
- [[_COMMUNITY_Trinity Package Init|Trinity Package Init]]
- [[_COMMUNITY_Code Discovery Skill|Code Discovery Skill]]

## God Nodes (most connected - your core abstractions)
1. `TrinityDB` - 40 edges
2. `DBConfig` - 26 edges
3. `TRINITY.md (Target RP finder)` - 12 edges
4. `acquire_lock()` - 10 edges
5. `test_acquire_verify_release_lock()` - 10 edges
6. `Working Revision (entity)` - 10 edges
7. `LockManager` - 9 edges
8. `LockHeldError` - 9 edges
9. `TrinityDB` - 9 edges
10. `add-feature skill` - 9 edges

## Surprising Connections (you probably didn't know these)
- `Revision entity` --semantically_similar_to--> `WorkingStateRef`  [INFERRED] [semantically similar]
  CLAUDE.md → Trinity/trinity/working_state.py
- `Revision entity` --semantically_similar_to--> `AuditEvent`  [INFERRED] [semantically similar]
  CLAUDE.md → Trinity/trinity/audit_log.py
- `Trinity as single source of truth` --conceptually_related_to--> `TrinityDB`  [INFERRED]
  CLAUDE.md → Trinity/trinity/db.py
- `PROJECT_BRIEF.md (Target RP finder)` --semantically_similar_to--> `PROJECT_BRIEF.md (Trinity docs)`  [INFERRED] [semantically similar]
  docs/PROJECT_BRIEF.md → Trinity/docs/PROJECT_BRIEF.md
- `STATE_CLASSIFICATION.md (Trinity docs)` --semantically_similar_to--> `DATA_MODEL.md (Target RP finder)`  [INFERRED] [semantically similar]
  Trinity/docs/STATE_CLASSIFICATION.md → docs/DATA_MODEL.md

## Import Cycles
- 1-file cycle: `Trinity/trinity/tests/test_lock_manager.py -> Trinity/trinity/tests/test_lock_manager.py`
- 2-file cycle: `Trinity/trinity/db.py -> Trinity/trinity/tests/test_lock_manager.py -> Trinity/trinity/db.py`

## Hyperedges (group relationships)
- **Duplicated _seed_run_revision test fixture pattern across Trinity test suite** — test_audit_log_seed_run_revision, test_lock_manager_seed_run_revision, test_working_state_seed_run_revision [INFERRED 0.85]
- **Trinity NotImplementedError contract-class design pattern (DB-backed interfaces awaiting implementation)** — audit_log_auditlog, lock_manager_lockmanager, session_sessionstore, working_state_workingstatestore [INFERRED 0.85]
- **add-feature conductor orchestrates worker skills selectively** — add_feature_skill, doc_router_skill, test_planner_skill, done_checker_skill [EXTRACTED 1.00]
- **Sequential Planning Doc Production Chain** — bootstrap_questionnaire, data_model, state_classifier_state_classification_doc, architecture_selection, assumptions_and_open_questions [INFERRED 0.85]
- **Immutable Evidence / Re-entry Governance Pattern** — adr_0002_persist_mutable_working_state_with_version_aware_rehydration_and_keep_published_evidence_separate, adr_0004_published_revision_reentry_policy, data_model_published_evidence_package, data_model_working_revision [INFERRED 0.90]
- **project-init Conductor Worker Chain** — project_init_project_init, workflow_mapper_workflow_mapper, state_classifier_state_classifier, test_planner_test_planner, uncertainty_log_uncertainty_log, repo_trim_repo_trim [EXTRACTED 1.00]
- **Target RP finder service pipeline (batch_discovery -> rp_parser -> flag_review -> Trinity)** — service_batch_discovery, service_rp_parser, service_flag_review, trinity_doc_target_rp [EXTRACTED 1.00]
- **Trinity working-to-evidence lifecycle (run/revision/lock/audit)** — trinity_table_runs, trinity_table_revisions, trinity_table_locks, trinity_table_audit_events [EXTRACTED 1.00]
- **Target RP finder entity chain (Batch -> Revision -> Sample -> Flagged Compound)** — entity_batch, entity_revision, entity_sample, entity_flagged_compound [EXTRACTED 1.00]

## Communities (17 total, 4 thin omitted)

### Community 0 - "Trinity DB Engine"
Cohesion: 0.06
Nodes (46): Connection, _extract_sql_blocks, SCHEMA.md schema source, _utc_now_iso, RuntimeError, append_event, list_for_run, _seed_run_revision (audit log test) (+38 more)

### Community 1 - "ADR Concurrency & Evidence Rules"
Cohesion: 0.09
Nodes (34): ADR-0002: Version-Aware Rehydration, Working State vs Published Evidence, Run (entity referenced in ADR-0002), Version-Aware Rehydration, Working Revision (entity referenced in ADR-0002), ADR-0003: Single-Editor Per Run Locking, 60s Heartbeat / 20min Stale Timeout Policy, Lock Record (concurrency control object), Reviewer Independence Rule (reviewer != primary_user) (+26 more)

### Community 2 - "Failure Catalog"
Cohesion: 0.12
Nodes (29): Bad raw rows can poison Sample Set Manager rebuilds mid-batch, Derived truth can become stale when persisted casually, Explicit draft-save checkpoints can drift from authoritative working snapshot, Duplicate LIMS ID creation can silently overwrite an existing run, Governed criteria and protected admin access can drift from operational needs, Home review queue can advertise self-review as available work, Merge-conflict artifacts can ship into code and docs, Parent/child state changes can fail when related records are still active (+21 more)

### Community 3 - "RP Finder Planning Docs"
Cohesion: 0.19
Nodes (22): ADR-0004 published revision re-entry policy, Run/Revision Artifact Folder Layout, DATA_MODEL.md (Target RP finder), Two-stage VBS launcher, Batch entity, Flagged Compound entity, Revision entity, Sample entity (+14 more)

### Community 4 - "Project Skill Conductors"
Cohesion: 0.10
Nodes (25): Canonical Architectural Boundaries (workflow truth/derived/evidence/UI), doc-router (loads docs in project-continue), project-continue skill, Intake Summary (Problem/Goals/Constraints/Unknowns), project-designer skill, Phased Execution Plan, project-executor skill, Generated CLAUDE.md (+17 more)

### Community 5 - "Lock Manager Tests"
Cohesion: 0.22
Nodes (22): datetime, acquire_lock, get_active_lock, release_lock, _seed_run_revision (lock manager test), test_acquire_raises_lock_held_error_for_fresh_competing_lock, test_acquire_verify_release_lock, test_stale_lock_can_be_taken_over_after_expiry_threshold (+14 more)

### Community 6 - "Lock Manager Module"
Cohesion: 0.16
Nodes (11): LockManager, LockToken, Single-editor locking contracts for Trinity., Represents an acquired lock for a run revision., Contract for lock acquisition, heartbeat, release, and override., Acquire single-editor lock or fail if unavailable., Renew lock lifetime for the token owner., Return currently active lock, if any. (+3 more)

### Community 7 - "Dev Workflow Skills"
Cohesion: 0.17
Nodes (15): add-feature skill, debug (debugcheck) skill, dev-contract skill, doc-router skill, done-checker skill, failure-memory skill, repo-trim skill, state-classifier skill (+7 more)

### Community 8 - "Data Model & Audit Log"
Cohesion: 0.17
Nodes (11): data-modeler skill, Batch entity (.b folder), Revision entity, AuditEvent, AuditLog, Audit logging contracts for governed workflow actions., Append-only event record., Contract for writing and querying durable audit events. (+3 more)

### Community 9 - "Session Contracts"
Cohesion: 0.17
Nodes (9): test_session_contract_types_exist, Session contracts for user/workstation context and guarded transitions., Identity and launch context for a client session., Contract for creating and resolving active user sessions., Create a new session context., Look up a session context by ID., Terminate an active session context., SessionContext (+1 more)

### Community 10 - "Working State Contracts"
Cohesion: 0.20
Nodes (11): Any, Working-state contracts for Trinity run revisions., Identity for mutable workflow truth., Result metadata for an explicit save boundary., Contract for loading/saving canonical mutable working state., Return canonical working-state payload for a run revision., Persist canonical working-state payload for a run revision., Delete mutable working-state payload for a run revision. (+3 more)

### Community 11 - "Architecture ADRs & House Rules"
Cohesion: 0.15
Nodes (12): Shared-Storage Deployment Model, Streamlit as Renderer, Not Architecture Owner, ADR-0001: Thin Presentation Layer with Shared-Storage Deployment, Architecture Rules (file size, split-first), Docs-First Rule, Failure Documentation Rule, Persistence Design Rules, Thin UI Layer Rule (+4 more)

### Community 12 - "Trinity Schema & Modules"
Cohesion: 0.24
Nodes (12): AGENTS.md (Trinity), audit_log.py, db.py, lock_manager.py, SCHEMA.md (Trinity module), session.py, audit_events table (Trinity), locks table (Trinity) (+4 more)

## Knowledge Gaps
- **35 isolated node(s):** `_utc_now_iso`, `SCHEMA.md schema source`, `test_initialize_creates_schema_and_version_marker`, `test_initialize_rejects_schema_mismatch`, `test_duplicate_lims_id_rejected_by_unique_display_id_constraint` (+30 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TrinityDB` connect `Trinity DB Engine` to `Lock Manager Tests`, `Dev Workflow Skills`?**
  _High betweenness centrality (0.131) - this node is a cross-community bridge._
- **Why does `datetime` connect `Lock Manager Tests` to `Trinity DB Engine`, `Lock Manager Module`, `Data Model & Audit Log`, `Session Contracts`, `Working State Contracts`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `TrinityDB` (e.g. with `datetime` and `Trinity as single source of truth`) actually correct?**
  _`TrinityDB` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `DBConfig` (e.g. with `datetime` and `LockHeldError`) actually correct?**
  _`DBConfig` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `datetime` (e.g. with `DBConfig` and `TrinityDB`) actually correct?**
  _`datetime` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Trinity contracts package.`, `Audit logging contracts for governed workflow actions.`, `Append-only event record.` to the rest of the system?**
  _94 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Trinity DB Engine` be split into smaller, more focused modules?**
  _Cohesion score 0.062146892655367235 - nodes in this community are weakly interconnected._