# Target RP Finder

## What this is
A Windows desktop app that scans a `.b` instrument batch folder, parses each sample's `Target.RP` file, and surfaces only the compounds flagged `Udel`, `Udelete`, or `dubious` — replacing manual file-by-file review.

## What it owns
Four entities (see [docs/DATA_MODEL.md](docs/DATA_MODEL.md)): `Batch` (the `.b` folder), `Revision` (one parse run, working until Submit then published/immutable), `Sample` (a qualifying `.d` folder), `Flagged Compound` (compound name + comment, tied to a sample+revision). Working state (scan/parse results before Submit) is discarded on cancel; published Revisions are evidence and are never edited in place — corrections re-enter via a new linked Revision (see [docs/STATE_CLASSIFICATION.md](docs/STATE_CLASSIFICATION.md)).

## What the caller provides
A `.b` folder path via the Browse UI. Nothing else — no auth, single user. See [docs/WORKFLOW_TIMELINE.md](docs/WORKFLOW_TIMELINE.md) for the full step sequence and edge cases (missing/malformed `Target.RP`, re-entry on correction).

## Architecture
Service-per-subject under `src/services/`: `batch_discovery` (lists/classifies `.d` folders, keeps samples only) → `rp_parser` (extracts flagged compound rows from `Target.RP`) → `flag_review` (aggregates, filters, is the only service that talks to Trinity). UI is presentation-only. Full detail: [docs/ARCHITECTURE_SELECTION.md](docs/ARCHITECTURE_SELECTION.md).

## Deployment
Two-stage VBS launcher — `RunSetup.vbs` builds a venv at `%LOCALAPPDATA%\TargetRPFinder\.venv`; `RunApp.vbs` sets `PYTHONPATH=src;Trinity` and launches `uvicorn target_rp_finder.main:app` on `127.0.0.1:8000`. See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).

## Persistence
Trinity is the single source of truth for all published Revisions, Samples, and Flagged Compounds — no loose report folders, no SQLite calls outside Trinity. Entry surface and backup mechanism are still OPEN (see [docs/ASSUMPTIONS_AND_OPEN_QUESTIONS.md](docs/ASSUMPTIONS_AND_OPEN_QUESTIONS.md)). See [docs/TRINITY.md](docs/TRINITY.md).

## Never do this
- Edit a published Revision (or its Samples/Flagged Compounds) in place — re-entry must create a new linked Revision.
- Treat a `.d` folder as a sample without running it through the full classification rule set (prefix matches first, then the 11-digit thousands-digit check).
- Persist derived values (counts, totals, the "has comments" filter) as stored fields — always recompute from Flagged Compound rows.
- Let a missing or malformed `Target.RP` stop the whole batch — skip and flag that sample only.
- Write to SQLite from anywhere except Trinity's named entry surface (to be filled on first real contact).

## Commands
TBD — filled once the `src/` scaffold and `requirements.txt` exist.
