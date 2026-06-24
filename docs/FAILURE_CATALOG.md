# FAILURE_CATALOG.md

## Target.RP Parsing Logic Risk

**Symptom:**
V1 build stalled specifically on `Target.RP` parsing — format assumptions didn't match real lab output, leading to missed compounds or false positives.

**Root Cause:**
Fixed-width column format is fragile. Assumptions about column positions or token boundaries can silently fail when real-world files vary slightly in spacing, multi-line wrapping, or header alignment. Whitespace-based token splitting loses positional information, making ON-COLUMN extraction unreliable.

**Detection Gap:**
- V1 had no fixture-based tests against real published data
- Synthetic test data can mask format mismatches
- Position-dependent extraction logic not validated against actual files

**Prevention Rule:**
1. Parser must remain covered by tests against both real USGS published fixtures (`Target.RP_with_Udel`, `Target.RP_Missing_udel`)
2. Any parser change must keep all existing fixture tests passing (regression gate)
3. New flag types (E-Code, Quad Erronious) must have synthetic test cases to isolate behavior
4. ON-COLUMN extraction by position (not token split) is the current approach — if format assumptions change, re-validate against real files immediately

**Regression Test / Guardrail:**
- `test_parse_with_udel`: must always pass (7 flagged, 6 dubious)
- `test_flagged_compound_structure`: validates extracted fields
- New: `test_e_code_recognition`, `test_quad_erronious_on_column_non_numerical`, `test_on_column_numerical_no_flag`

**Core Rule:**
Before accepting any parser change: confirm that ALL existing fixture tests still pass. If a real USGS fixture fails, stop and investigate root cause before proceeding.

## Known Risks (Open)

### Risk: ON-COLUMN Position Detection
**Status:** Open
- ON-COLUMN position is extracted from header line via regex search for "ON-COLUMN"
- Relies on header format consistency
- If USGS changes header structure, position detection could fail silently
- **Mitigation:** If on_column_start is None, skip ON-COLUMN checking (graceful degradation)

### Risk: Fixed-Width Column Extraction
**Status:** Open
- ON-COLUMN is extracted by taking a fixed 15-character window from on_column_start
- Real data may have different width or padding
- **Mitigation:** Current tests pass; validate against real data with non-numerical ON-COLUMN values before production use

### Risk: "Okay" Exclusion
**Status:** Closed (test coverage)
- "Okay" is case-sensitive in the exclusion list
- Real lab output might use "OKAY" or other variants
- **Mitigation:** Add case-insensitive matching if lab data shows variants
- **Test:** `test_okay_excluded_from_unknown_tokens` covers lowercase "Okay"

## Decision Log

### Decision: Store has_quad_error as boolean, not raw on_column_value
- **Why:** The user's requirement is binary: flag or don't flag. Raw value adds storage overhead with no downstream use.
- **Addressed by:** Council of Experts review; confirmed with user
- **Impact:** If future audit trail of raw values becomes needed, would require schema change; current binary flag is sufficient for current requirements
