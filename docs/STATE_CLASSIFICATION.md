# STATE_CLASSIFICATION.md

## Classification table

| Data element | Classification | Notes |
|---|---|---|
| Batch (`.b` folder selection) | Working | exists only as a path reference until a Revision is created from it |
| Sample list + classification (cal/ccv/idl/blank/prep blank/surrogate/sample) | Working | recomputed on every scan, not stored standalone |
| Parsed Sample (`parse_status`) | Working → Evidence | mutable while its Revision is `working`; freezes when Revision publishes |
| Flagged Compound (compound name + comment) | Working → Evidence | same lifecycle as its parent Sample/Revision |
| Revision record | Working → Evidence | `working` until Submit, `published` (immutable) after |
| Per-sample flagged-compound count | Derived | computed from Flagged Compound rows, never stored |
| Per-batch/revision total count | Derived | computed from Sample/Flagged Compound rows, never stored |
| "Has comments" table filter | Derived | computed at display time, never stored as a negative record |
| Table filters (UI-side: by compound, by comment type) | Working (UI-local) | discarded on navigation away, never persisted |
| Revision lineage (`prior_revision_id`) | Evidence | set once at re-entry, never changes after |

## Mutability rules
- Before Submit: Batch scan results, Sample parse outcomes, and Flagged Compound rows are all mutable working state — re-running the scan/parse discards and replaces them, nothing is archived yet.
- Cancel (navigate away without Submit): all working state for that scan is discarded; no Trinity write occurs.
- After Submit: the Revision and everything under it (Samples, Flagged Compounds) freezes into evidence. No further edits.

## Derived state rules
- Per-sample count — source: Flagged Compound rows for that sample+revision; computed at: display time; never stored as canonical truth.
- Per-batch/revision total — source: all Flagged Compound rows for that revision; computed at: display time.
- "Has comments" filter — source: per-sample count > 0; computed at: display time; samples with zero flagged compounds are simply omitted from the rendered table, not written anywhere.

## Versioning behavior
- Corrections to evidence happen only by re-entry (Trinity ADR-0004 pattern): re-parsing previously missing/malformed samples creates a **new working Revision** with `prior_revision_id` pointing at the published one being corrected.
- No admin/auth challenge gates this re-entry — single-user app, no team to authenticate against (confirmed by user). A reason is still recorded on the new Revision for traceability, since Trinity's audit pattern expects it, but it's a free-text note, not a credential check.
- The original published Revision is never overwritten; it remains queryable in the archive alongside the new one.

## Forbidden state transitions
| From | To | Why forbidden |
|---|---|---|
| `published` Revision | mutated in place | breaks evidence immutability |
| Derived count/total | stored as a persisted field | would let stale derived data silently diverge from source rows |
| Working Sample/Flagged Compound (pre-submit) | written to Trinity | working state is discarded on cancel, not partially persisted |
| `published` Revision | `working` (same record) | correction must create a new linked Revision, not flip status back |
