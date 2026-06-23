# TRINITY.md

**Doc class: CONTRACT DOC** — house-standard persistence backend,
stamped and confirmed at project-init, not interviewed. Trinity is
the default persistence layer for every app unless a project
explicitly overrides it (override logged in
ASSUMPTIONS_AND_OPEN_QUESTIONS.md).

Verification layer for the persistence mechanism. Answers: "does
all persistence actually go through Trinity, the way the contract
says?" TRINITY.md owns the MECHANISM. It does NOT own the content —
which entities exist, and what is working vs derived vs evidence,
live in DATA_MODEL.md and STATE_CLASSIFICATION.md.

## What Trinity is
A plug-and-play SQLite backend. It is the SINGLE persistence path
for the app — every report and all long-term data is stored and
recalled through Trinity. No loose report folders on disk. No
SQLite calls scattered through services.

## Folder contract — what lives in Trinity/
- Access code — the modules services use to read and write
- Schema / migrations — table definitions and version history
- The .db file — the live SQLite database

Trinity/ is mounted on PYTHONPATH alongside src/
(`PYTHONPATH=src;Trinity` — must match DEPLOYMENT.md).

## Entry surface — FILLED
**Module:** `trinity.target_rp_finder.TargetRPFinderPersistence`

**Pattern:** Single client class with methods per workflow action:
- `create_batch(batch_path)` → run_id
- `create_revision(run_id, based_on_revision_id)` → revision_id  
- `store_samples_and_compounds(revision_id, samples_data)` — persists parsed results
- `load_revision(revision_id)` — retrieves cached results
- `get_revision_context(revision_id)` — looks up the parent run_id and source batch path for a revision
- `publish_revision(revision_id)` — freezes revision as evidence
- `get_batch_revisions(run_id)` — lists all revisions for a batch

**Rule:** `flag_review` service is the ONLY caller. It imports and uses
TargetRPFinderPersistence; no service touches SQLite directly. All entity
data (Batch → Revision → Sample → Flagged Compound) flows through these
methods, serialized as JSON in the revisions.state_json column.

**Lifecycle:**
1. Create batch (run record) when user selects .b folder
2. Create working revision for that run
3. Parse all samples, aggregate results
4. Store samples/compounds as JSON in revision state
5. On Submit: publish revision (status → 'published')
6. On re-entry: create new working revision (based_on_revision_id → prior published)

This is the single enforcement point for the persistence rule.
Mirror this open item in ASSUMPTIONS_AND_OPEN_QUESTIONS.md.

## Backup — ⚠️ OPEN, must settle before persistence work
No automatic backup exists today. This MUST be settled and added
when persistence work begins — it is not optional.

The .db lives INSIDE Trinity/, inside the project folder. That
means the live database shares a fate with the code: a redeploy,
folder copy, or repo reset can clobber live evidence data. A
backup mechanism (path, trigger, retention) must be defined before
the app holds any real data.

Decision trigger: before the app stores any production/evidence data.
Mirror this open item in ASSUMPTIONS_AND_OPEN_QUESTIONS.md.

## Must never happen
- A service reads or writes SQLite outside the Trinity entry surface
- Reports or long-term data persisted anywhere but Trinity
- The live .db overwritten by a redeploy, folder copy, or repo reset
- Trinity dropped from PYTHONPATH while the data model expects it
- Evidence-class data mutated in place (see STATE_CLASSIFICATION.md)

## Verification criteria
- [ ] Entry surface section filled — names the one persistence path
- [ ] Every service write/read routes through that surface, no exceptions
- [ ] PYTHONPATH=src;Trinity present in DEPLOYMENT.md
- [ ] Backup mechanism defined before any real data is stored
- [ ] DATA_MODEL.md / STATE_CLASSIFICATION.md name Trinity as source of truth