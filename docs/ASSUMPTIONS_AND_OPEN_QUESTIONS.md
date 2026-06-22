# ASSUMPTIONS_AND_OPEN_QUESTIONS.md

## Assumptions

- **Assumption**: The only REVIEW CODE comment tokens that matter are `Udel`, `Udelete`, and `dubious`.
  - Why assumed: only tokens observed in the two real fixtures.
  - Risk if wrong: a real future batch using a different comment word (e.g. a typo variant or new lab convention) would be silently excluded from results.
  - Mitigation: log any REVIEW CODE token encountered that isn't blank and isn't one of the three known tokens, surfaced to the user rather than silently dropped.
  - Decision trigger: before relying on this tool for a production batch with comment tokens not yet seen.

- **Assumption**: `.d` folder name prefixes (`cal`, `ccv`, `cstpc`/`tpc`, `idl`, `peb`) and the 11-digit numeric sample/prep-blank/surrogate pattern cover all folder types that will appear.
  - Why assumed: based on user's description of current lab naming conventions; no exhaustive folder listing reviewed.
  - Risk if wrong: an unrecognized folder name could be misclassified as a sample (false positive) or silently dropped.
  - Mitigation: per WORKFLOW_TIMELINE edge cases — any `.d` name that matches neither a known prefix nor the 11-digit pattern is flagged as unclassified, never silently treated as a sample.
  - Decision trigger: first real `.b` folder run — confirm no unclassified folders appear unexpectedly.

- **Assumption**: ADR-0004's admin/project-lead re-entry auth challenge does not apply to this app.
  - Why assumed: confirmed by user — single-user app, no team.
  - Risk if wrong: N/A unless a second user is ever added.
  - Mitigation: a free-text reason is still recorded on re-entry for traceability, without a credential gate.
  - Decision trigger: if this app is ever shared with another user.

## Open questions

- **Question**: What is Trinity's entry surface — the exact module/function `flag_review` calls to read/write?
  - Why it matters: it's the single enforcement point for "all persistence goes through Trinity."
  - Risk of deferring: services could end up touching SQLite directly if this isn't named before `flag_review` is built.
  - Decision trigger: before any service writes or reads data (per TRINITY.md).

- **Question**: What is the backup mechanism for the Trinity `.db` file?
  - Why it matters: the live `.db` lives inside the project folder and can be clobbered by a redeploy or repo reset.
  - Risk of deferring: a redeploy could destroy all archived batch evidence with no recovery path.
  - Decision trigger: before the app stores any real `.b` folder data (per TRINITY.md).

## Deferred decisions

- **Decision**: Exact UI/db schema for storing Revision lineage and reason text.
  - Why deferred: schema design belongs to implementation, not planning docs.
  - Maximum delay: must be settled once Trinity's entry surface is filled and before `flag_review` is implemented.
