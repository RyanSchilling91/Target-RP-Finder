# ARCHITECTURE_SELECTION.md

**Doc class: CONTRACT DOC** — confirmed at project-init, not interviewed.

## Architecture laws applied
- Services live one-subject-per-folder under `src/services/`.
- UI is presentation only — no business logic, no persistence, no routing decisions.
- Business rules live in service modules, never in UI.
- Persistence is a single path through Trinity (see [TRINITY.md](TRINITY.md)). No loose report folders, no scattered SQLite calls.
- Deployment is the two-stage VBS launcher (see [DEPLOYMENT.md](DEPLOYMENT.md)).
- Hard file limit 350 lines, soft 250.

## Service folders (derived from confirmed scope)
- `services/batch_discovery/` — browses a `.b` folder, lists top-level `.d` subfolders, classifies each by name into sample / qcs / cals / blanks / prep blanks, keeps samples only.
- `services/rp_parser/` — parses each sample's `Target.RP` fixed-width text export, extracts compound rows whose REVIEW CODE column carries `Udel`, `Udelete`, or `dubious`.
- `services/flag_review/` — aggregates parsed flagged compounds by sample and by batch, computes totals, applies filters, and is the only caller into Trinity for caching parsed results.

## Layer boundaries
- UI → calls service layer only (batch_discovery for folder browse/classify, flag_review for table data). UI never touches Trinity or parses files directly.
- batch_discovery → rp_parser: hands off the filtered list of sample `.d` folders.
- rp_parser → flag_review: hands off parsed flagged-compound records per sample.
- flag_review → Trinity: the only service with a persistence dependency. batch_discovery and rp_parser are stateless/pure and do not touch Trinity.

## Contract-doc references
- **Trinity** ([TRINITY.md](TRINITY.md)) — single persistence path for all parsed results.
  - ⚠ OPEN: entry surface (the exact module/function services import to read/write) — must be filled on first real contact with Trinity from `flag_review`.
  - ⚠ OPEN: backup mechanism for the `.db` file — must be settled before any real `.b` folder data is stored.
- **Deployment** ([DEPLOYMENT.md](DEPLOYMENT.md)) — two-stage VBS launcher, no overrides. `PYTHONPATH=src;Trinity` required.

## Why this shape
Each service maps to one stage of the user's manual workflow being automated — find samples, parse flags, then review/cache — so a failure traces to exactly one folder. Trinity is isolated behind `flag_review` so the single-persistence-path rule has one enforcement point instead of being scattered across services.
