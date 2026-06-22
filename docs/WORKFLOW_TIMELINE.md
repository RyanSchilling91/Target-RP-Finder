# WORKFLOW_TIMELINE.md

## Step-by-step

| # | Actor | Action | Data touched | System response | State impact |
|---|---|---|---|---|---|
| 1 | User | Opens app, clicks Browse, selects a `.b` folder | `.b` folder path | UI passes path to `batch_discovery` | none yet (working) |
| 2 | System (`batch_discovery`) | Lists top-level `.d` subfolders, classifies each by name (cal/ccv/tpc/idl/blank/prep blank/surrogate/sample) | `.d` folder names | Filters to samples only, hands list to `rp_parser` | working |
| 3 | System (`rp_parser`) | Parses each sample's `Target.RP`, extracts rows with REVIEW CODE `Udel`/`Udelete`/`dubious` | `Target.RP` file contents | Missing file → skip + flag sample. Malformed file → skip + flag sample (user must investigate). Otherwise hands parsed rows to `flag_review` | derived |
| 4 | System (`flag_review`) | Aggregates flagged compounds by sample/batch, computes totals | Parsed compound rows | Renders results table directly — no pause before this point | derived (not yet persisted) |
| 5 | User | Reviews table, optionally filters | Displayed table | UI filters client-side; underlying data unchanged | derived (still editable) |
| 6 | User | Hits Submit | Reviewed table | `flag_review` writes to Trinity as a published working revision; archive entry becomes available on the home page | **freezes → evidence** |
| 7 | User | Returns later, browses archive on home page | Archive entries | `flag_review` reads from Trinity, no re-parse | evidence (read-only) |
| 8 | User | Fixes a missing/malformed `Target.RP` in the same `.b` folder, re-selects it | Same `.b` folder path | System re-parses **only** the previously skipped/flagged samples (step 3 logic, scoped) | working (new revision) |
| 9 | System | Re-entry into Trinity | New parsed rows + reference to prior published entry | Per Trinity ADR-0004: creates a **new working revision** derived from the published one; original published archive entry is never edited in place | evidence (old) stays frozen; new working revision created |
| 10 | User | Reviews/submits the new revision | New revision table | Same as step 6 — freezes into its own evidence entry, linked to the prior revision | freezes → evidence |

## Review and approval points
- Steps 4–5 (after parsing, before Submit): table is fully derived and freely re-filterable, nothing is frozen yet.
- Step 6 / Step 10 (Submit): the only freeze point. Before submit = mutable working state. After submit = immutable evidence, per Trinity ADR-0002/ADR-0004.

## Handoff points
- `batch_discovery` → `rp_parser`: filtered list of sample `.d` folders.
- `rp_parser` → `flag_review`: parsed flagged-compound rows per sample (or skip+flag signal).
- `flag_review` → Trinity: the only service with a persistence dependency; reads/writes the cached/archived results.

## Edge cases
- `Target.RP` missing from a sample `.d` folder → skip that sample, flag it in the results table, continue the run (does not stop the batch).
- `Target.RP` present but malformed/unparseable → same as missing: skip, flag, continue; user is told to investigate.
- `.d` folder name doesn't match any known prefix and isn't an 11-digit numeric ID → unclassified; flagged for the user rather than silently dropped (open item — see ASSUMPTIONS).
- Re-processing the same `.b` folder after a fix → targeted re-parse of only previously flagged/skipped samples, new working revision created, old published evidence untouched.
- Open item carried to state-classifier: whether re-entry (step 8–9) requires the ADR-0004 admin/project-lead auth challenge, given this is a single-user app with no team — flag this open before persistence is finalized.
