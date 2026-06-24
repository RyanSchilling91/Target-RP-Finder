# DATA_MODEL.md

## Persistence
All entities below are persisted exclusively through Trinity (see [TRINITY.md](TRINITY.md)) once their parent Revision is published — Trinity is the single source of truth for archived batch/revision data.

## Entities

### Batch
- What it is: a `.b` instrument folder containing all injections for a run.
- Identifier: folder name/path (business key), unique on disk.
- Fields: name/path (system, static).
- Owner: system-derived from the folder the user browses to.
- Allowed states: none of its own — state lives on its Revisions.
- Must never happen: a Batch persisted with zero Revisions after a Submit action.

### Revision
- What it is: one full parse run of a Batch — the unit that goes from working to published.
- Identifier: system-generated revision ID; carries `prior_revision_id` (nullable) when re-entered from a published revision.
- Fields: `batch_id` (system), `status` (`working`/`published`, system, set by user action), `created_at` (system), `published_at` (system, set on Submit).
- Owner: system-created; the working→published transition is a user action (Submit).
- Allowed states: `working` → `published` (one-way). Re-entry creates a new `working` revision linked via `prior_revision_id`; the published one is untouched.
- Must never happen: a `published` revision mutated in place; two `working` revisions open at once for the same `batch_id`.

### Sample
- What it is: a `.d` folder classified as a sample (11-digit numeric ID, not a 9xxx prep blank or 8xxx surrogate, not a prefix-matched QC type).
- Identifier: 11-digit sample ID, unique within its parent Batch/Revision.
- Fields: `sample_id` (system), `revision_id` (system), `parse_status` (`parsed`/`missing`/`malformed`, system, fixed once the revision is created).
- Owner: system-derived from folder name and parse outcome.
- Allowed states: `parsed`, `missing`, `malformed` — fixed per revision, not mutable after parse.
- Must never happen: a `missing`/`malformed` Sample carrying any Flagged Compound rows; a Sample existing without a parent Revision.

### Flagged Compound
- What it is: one compound row from a sample's `Target.RP` whose REVIEW CODE carried `Udel`, `Udelete`, `dubious`, `E-Code`, or `Quad Erronious` (non-numerical ON-COLUMN).
- Identifier: no standalone business key — identity is (`sample_id`, `revision_id`, `compound_name`).
- Fields: `compound_name` (system), `comment` (system, one of `Udel`/`Udelete`/`dubious`/`E-Code`/`Quad Erronious`), `sample_id` (system), `revision_id` (system), `has_quad_error` (system, boolean, True if ON-COLUMN contains non-numerical value).
- Owner: fully system-derived from parsing; never user-edited.
- Allowed states: none — exists or doesn't, immutable once parsed into a revision.
- Must never happen: a Flagged Compound without a parent Sample and Revision; a comment value outside the allowed tokens; `has_quad_error` set to True if comment is not `Quad Erronious`.

## Derived values (computed, never stored)
- Per-sample flagged-compound count.
- Per-batch/per-revision total flagged-compound count.
- "Has comments" filter — a Sample with zero Flagged Compounds is simply omitted from display, not stored as a negative record.

## Entity relationship summary
`Batch` 1—* `Revision` 1—* `Sample` 1—* `Flagged Compound`
`Revision.prior_revision_id` → `Revision.id` (self-referencing lineage, nullable)

## Forbidden state transitions
| From | To | Why forbidden |
|---|---|---|
| `published` Revision | edited in place | breaks evidence immutability (Trinity ADR-0004) |
| `published` Revision | `working` (same record) | re-entry must create a NEW revision, not flip status back |
| `missing`/`malformed` Sample | has Flagged Compound rows | contradicts parse outcome — nothing was parsed |
| any Batch | two simultaneous `working` Revisions | ambiguous which is the active re-entry |
