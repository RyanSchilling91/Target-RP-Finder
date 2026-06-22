# TEST_STRATEGY.md

## Test scope summary
Covers `.d` folder classification, `Target.RP` parsing/flag extraction, aggregation/display, and the working→evidence persistence lifecycle through Trinity.

## Unit test targets

| Rule | Why it matters | Minimum cases |
|---|---|---|
| `.d` name classification (cal/ccv/tpc/idl/blank/prep blank/surrogate/sample) | Wrong classification leaks non-samples into parsing or drops real samples | `cal`/`Cal`, `ccv`/`CCV`, `cstpc`/`tpc`, `idl`, `peb`/`Peb`, numeric ID with thousands digit 8, 9, and neither; unclassifiable garbage name |
| `Target.RP` flag extraction | Core deliverable — must catch exactly `Udel`/`Udelete`/`dubious`, nothing else | Real fixture with `dubious` only; real fixture with `Udel`+`dubious`; row with other markers (`M`,`Q`,`H`,`QM`) but no comment must be excluded; synthetic clean file with zero comments |
| Missing/malformed file handling | Must skip+flag, never crash the batch | Missing `Target.RP` in a sample folder; truncated/garbled `Target.RP` content |
| Per-sample / per-batch counts | Displayed totals must match underlying flagged rows exactly | Zero, one, many flagged compounds per sample; multi-sample batch totals |
| "Has comments" filter | Samples with zero flags must never appear in the table | Sample with zero flags is omitted, not shown as empty row |

## Integration targets

| Workflow | Modules involved | Expected result |
|---|---|---|
| Full batch scan → parse → display | `batch_discovery` → `rp_parser` → `flag_review` | Given a folder of real+synthetic `.d` folders (samples, qc types, missing, malformed, clean), table shows only samples with ≥1 flagged compound, correct comments, correct counts |
| Submit → Trinity → reload | `flag_review` ↔ Trinity | After Submit, archive entry is retrievable from the home page with identical data, no re-parse triggered |
| Re-entry on correction | `batch_discovery` → `rp_parser` → `flag_review` ↔ Trinity | Fixing a missing/malformed sample and re-running creates a new working Revision linked via `prior_revision_id`; only the previously flagged/skipped sample is re-parsed; the original published Revision is unchanged in Trinity |

## Regression scenarios
- No prior bugs exist yet (clean V2 build), but the V1 attempt stalled specifically on `Target.RP` parsing logic. Guardrail: the parser must be covered by fixture-based tests against **real** published data (the two confirmed fixtures), not assumptions about the format — any future parser change must keep both real fixtures passing.

## Required fixtures
- `Target.RP_Missing_udel` (real, dubious-only comments) — `input data/`
- `Target.RP_with_Udel` (real, `Udel` + `dubious` comments) — `input data/`
- Synthetic clean `Target.RP` (in-memory string, zero REVIEW CODE comments) — for the "omitted from display" case
- Synthetic malformed/truncated `Target.RP` (in-memory string) — no real malformed file is available or to be created by altering the real fixtures
- Synthetic `.d` folder name sets — for classification unit tests (no real folder structure needed)

## Correctness definition
For a given `.b` folder and Revision: the displayed table contains exactly the samples that have ≥1 compound flagged `Udel`/`Udelete`/`dubious` in their `Target.RP`, each compound listed once with its exact comment token, correct per-sample and per-batch totals, and samples that are missing/malformed/non-sample are excluded from the table but reflected as skip/flag notices.

## Manual validation
Before trusting the tool on a real work batch: open one real `.b`-style folder in the running app and hand-verify the table against manually opening 2–3 of its `Target.RP` files — supplements automated coverage, never replaces it for the parsing rule itself.
