# Graph Report - Target RP finder  (2026-06-22)

## Corpus Check
- 75 files · ~47,899 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 390 nodes · 595 edges · 32 communities (26 shown, 6 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 64 edges (avg confidence: 0.74)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7f0a65c8`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

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
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]

## God Nodes (most connected - your core abstractions)
1. `TrinityDB` - 39 edges
2. `DBConfig` - 26 edges
3. `acquire_lock()` - 10 edges
4. `test_acquire_verify_release_lock()` - 10 edges
5. `Working Revision (entity)` - 10 edges
6. `Target RP Finder` - 9 edges
7. `LockManager` - 9 edges
8. `LockHeldError` - 9 edges
9. `TrinityDB` - 9 edges
10. `add-feature skill` - 9 edges

## Surprising Connections (you probably didn't know these)
- `TRINITY.md (Target RP finder)` --semantically_similar_to--> `README.md (Trinity module)`  [INFERRED] [semantically similar]
  docs/TRINITY.md → Trinity/trinity/README.md
- `WORKFLOW_TIMELINE.md (Trinity docs)` --conceptually_related_to--> `ADR-0004 published revision re-entry policy`  [INFERRED]
  Trinity/docs/WORKFLOW_TIMELINE.md → docs/TRINITY.md
- `LockRecord` --semantically_similar_to--> `LockToken`  [INFERRED] [semantically similar]
  Trinity/trinity/tests/test_lock_manager.py → Trinity/trinity/lock_manager.py
- `New Working Revision on Re-entry` --conceptually_related_to--> `Working Revision (entity)`  [INFERRED]
  Trinity/docs/ADR-0004-published-revision-reentry-policy.md → Trinity/docs/DATA_MODEL.md
- `Run Status Lifecycle (Draft->...->Published)` --conceptually_related_to--> `Run (entity)`  [INFERRED]
  Trinity/docs/ASSUMPTIONS_AND_OPEN_QUESTIONS.md → Trinity/docs/DATA_MODEL.md

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

## Communities (32 total, 6 thin omitted)

### Community 0 - "Trinity DB Engine"
Cohesion: 0.07
Nodes (61): datetime, _extract_sql_blocks, SCHEMA.md schema source, _utc_now_iso, append_event, list_for_run, _seed_run_revision (audit log test), test_audit_append_and_ordered_retrieval (+53 more)

### Community 1 - "ADR Concurrency & Evidence Rules"
Cohesion: 0.21
Nodes (16): ADR-0002: Version-Aware Rehydration, Working State vs Published Evidence, Run (entity referenced in ADR-0002), Version-Aware Rehydration, Working Revision (entity referenced in ADR-0002), Audit Event (entity), Criteria Configuration (entity), Derived Result Set (entity), Match Mapping (entity) (+8 more)

### Community 2 - "Failure Catalog"
Cohesion: 0.12
Nodes (29): Bad raw rows can poison Sample Set Manager rebuilds mid-batch, Derived truth can become stale when persisted casually, Explicit draft-save checkpoints can drift from authoritative working snapshot, Duplicate LIMS ID creation can silently overwrite an existing run, Governed criteria and protected admin access can drift from operational needs, Home review queue can advertise self-review as available work, Merge-conflict artifacts can ship into code and docs, Parent/child state changes can fail when related records are still active (+21 more)

### Community 3 - "RP Finder Planning Docs"
Cohesion: 0.17
Nodes (10): App-specific details (intake gaps), Auth, Commands, Constraints, `.d` folder classification rules, File format, Goals, Hosting / deployment (+2 more)

### Community 4 - "Project Skill Conductors"
Cohesion: 0.11
Nodes (24): Canonical Architectural Boundaries (workflow truth/derived/evidence/UI), doc-router (loads docs in project-continue), project-continue skill, project-designer skill, Phased Execution Plan, project-executor skill, Generated CLAUDE.md, project-init skill (+16 more)

### Community 5 - "Lock Manager Tests"
Cohesion: 0.18
Nodes (15): RP parser service - extracts flagged compounds from Target.RP files., _extract_sample_id(), FlaggedCompound, _is_known_code_or_anomaly(), _is_numeric_token(), _parse_compound_row(), parse_target_rp(), Parse Target.RP fixed-width text files and extract flagged compounds. (+7 more)

### Community 6 - "Lock Manager Module"
Cohesion: 0.16
Nodes (11): LockManager, LockToken, Single-editor locking contracts for Trinity., Represents an acquired lock for a run revision., Contract for lock acquisition, heartbeat, release, and override., Acquire single-editor lock or fail if unavailable., Renew lock lifetime for the token owner., Return currently active lock, if any. (+3 more)

### Community 7 - "Dev Workflow Skills"
Cohesion: 0.25
Nodes (11): add-feature skill, data-modeler skill, debug (debugcheck) skill, dev-contract skill, doc-router skill, done-checker skill, failure-memory skill, repo-trim skill (+3 more)

### Community 8 - "Data Model & Audit Log"
Cohesion: 0.23
Nodes (8): AuditEvent, AuditLog, Audit logging contracts for governed workflow actions., Append-only event record., Contract for writing and querying durable audit events., Append an immutable event., List audit events for a run in chronological order., List audit events for a specific revision in chronological order.

### Community 9 - "Session Contracts"
Cohesion: 0.17
Nodes (9): test_session_contract_types_exist, Session contracts for user/workstation context and guarded transitions., Identity and launch context for a client session., Contract for creating and resolving active user sessions., Create a new session context., Look up a session context by ID., Terminate an active session context., SessionContext (+1 more)

### Community 10 - "Working State Contracts"
Cohesion: 0.20
Nodes (11): Any, Working-state contracts for Trinity run revisions., Identity for mutable workflow truth., Result metadata for an explicit save boundary., Contract for loading/saving canonical mutable working state., Return canonical working-state payload for a run revision., Persist canonical working-state payload for a run revision., Delete mutable working-state payload for a run revision. (+3 more)

### Community 11 - "Architecture ADRs & House Rules"
Cohesion: 0.17
Nodes (11): Shared-Storage Deployment Model, Streamlit as Renderer, Not Architecture Owner, ADR-0001: Thin Presentation Layer with Shared-Storage Deployment, Thin UI Layer Rule, Run/Revision Artifact Folder Layout, Workflow-Governed Python Application Core, Architecture laws applied, Contract-doc references (+3 more)

### Community 12 - "Trinity Schema & Modules"
Cohesion: 0.24
Nodes (12): AGENTS.md (Trinity), audit_log.py, db.py, lock_manager.py, SCHEMA.md (Trinity module), session.py, audit_events table (Trinity), locks table (Trinity) (+4 more)

### Community 14 - "RP Finder Sample Discovery"
Cohesion: 0.20
Nodes (9): Architecture, Commands, Deployment, Never do this, Persistence, Target RP Finder, What it owns, What the caller provides (+1 more)

### Community 17 - "Community 17"
Cohesion: 0.20
Nodes (9): Batch, Derived values (computed, never stored), Entities, Entity relationship summary, Flagged Compound, Forbidden state transitions, Persistence, Revision (+1 more)

### Community 18 - "Community 18"
Cohesion: 0.22
Nodes (7): Correctness definition, Integration targets, Manual validation, Regression scenarios, Required fixtures, Test scope summary, Unit test targets

### Community 19 - "Community 19"
Cohesion: 0.29
Nodes (5): Classification table, Derived state rules, Forbidden state transitions, Mutability rules, Versioning behavior

### Community 20 - "Community 20"
Cohesion: 0.33
Nodes (4): Edge cases, Handoff points, Review and approval points, Step-by-step

### Community 21 - "Community 21"
Cohesion: 0.21
Nodes (7): Connection, RuntimeError, Create required tables/metadata if not present., Load durable metadata (schema/app/storage versions, timestamps)., Persist durable metadata., _utc_now_iso(), Any

### Community 22 - "Community 22"
Cohesion: 0.23
Nodes (10): ClassifiedFolder, classify_folder(), discover_samples(), Discover and classify .d folders in a .b batch folder., Result of classifying a .d folder., Classify a .d folder by name using case-insensitive prefix matching and numeric, Scan a .b batch folder, classify all .d subfolders, return only samples.      Re, Batch discovery service - scans .b folders and classifies .d subfolders. (+2 more)

### Community 23 - "Community 23"
Cohesion: 0.22
Nodes (6): Required Document Set, LIMS ID Canonical Identifier Assumption, Run Status Lifecycle (Draft->...->Published), Assumptions, Deferred decisions, Open questions

### Community 24 - "Community 24"
Cohesion: 0.25
Nodes (8): ADR-0003: Single-Editor Per Run Locking, 60s Heartbeat / 20min Stale Timeout Policy, Lock Record (concurrency control object), Reviewer Independence Rule (reviewer != primary_user), Bootstrap Fallback Credential, ADR-0005: Password-Only Admin Challenges Bootstrap, Workstation Identity as Actor Attribution, Lock Record (entity)

### Community 25 - "Community 25"
Cohesion: 0.25
Nodes (7): Architecture Rules (file size, split-first), Docs-First Rule, Failure Documentation Rule, Persistence Design Rules, Failure Catalog Entry Format, Failure Catalog Check Before Risky Behavior, failure-memory skill

### Community 26 - "Community 26"
Cohesion: 0.29
Nodes (6): ADR-0004 published revision re-entry policy, Two-stage VBS launcher, Trinity backup mechanism (open item), TRINITY.md (Target RP finder), Trinity entry surface (open item), README.md (Trinity module)

### Community 27 - "Community 27"
Cohesion: 0.40
Nodes (4): ADR Candidates List, Planned Sample Set Enters First, Planned Sample Set Line (entity), Intake Summary (Problem/Goals/Constraints/Unknowns)

### Community 28 - "Community 28"
Cohesion: 0.50
Nodes (4): Immutable Published Revision Principle, New Working Revision on Re-entry, ADR-0004: Published Revision Re-entry Policy, Anti-Failure Rules

## Knowledge Gaps
- **86 isolated node(s):** `FolderType`, `Path`, `Path`, `What this is`, `What it owns` (+81 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `datetime` connect `Trinity DB Engine` to `Data Model & Audit Log`, `Session Contracts`, `Working State Contracts`, `Lock Manager Module`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Why does `TrinityDB` connect `Trinity DB Engine` to `Community 21`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `TRINITY.md (Target RP finder)` connect `Community 26` to `Architecture ADRs & House Rules`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `TrinityDB` (e.g. with `datetime` and `LockHeldError`) actually correct?**
  _`TrinityDB` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `DBConfig` (e.g. with `datetime` and `LockHeldError`) actually correct?**
  _`DBConfig` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `datetime` (e.g. with `DBConfig` and `TrinityDB`) actually correct?**
  _`datetime` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Services for Target RP Finder.`, `Batch discovery service - scans .b folders and classifies .d subfolders.`, `FolderType` to the rest of the system?**
  _161 weakly-connected nodes found - possible documentation gaps or missing edges._