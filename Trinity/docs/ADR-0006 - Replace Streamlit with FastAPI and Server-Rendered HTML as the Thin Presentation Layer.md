# ADR-0006 - Replace Streamlit with FastAPI and Server-Rendered HTML as the Thin Presentation Layer

## Status
- Accepted
- Supersedes [ADR-0001](<ADR-0001 - Use a Thin Presentation Layer with Shared-Storage Deployment as the Near-Term Baseline.md>)

## Decision
Use FastAPI with server-rendered HTML as the accepted presentation layer, replacing Streamlit. The governing principle from ADR-0001 is unchanged: the renderer is a presentation surface only — it does not own workflow logic, persistence semantics, routing rules, review control, lock handling, or publish behavior. Shared-storage deployment remains the accepted near-term operating model.

## Context
ADR-0001 accepted Streamlit as the near-term renderer for Trinity-backed projects. In practice, builds on Streamlit (including Target RP Finder) approached its limits as the workflow-governed core grew — session-state handling and reactive rerun behavior began pulling toward the UI-owns-state failure mode ADR-0001 was explicitly trying to avoid. FastAPI plus server-rendered HTML was adopted instead, and is now running in production on Target RP Finder (`uvicorn target_rp_finder.main:app`, two-stage VBS launcher per `DEPLOYMENT.md`).

## Alternatives considered
- Keep Streamlit and work around its limits with custom session-state management:
  - Rejected because the workarounds themselves were drifting business/workflow logic into UI callback code — the exact pattern ADR-0001 was written to prevent.
- Adopt a heavier SPA framework (React/Vue) over a JSON API:
  - Rejected for the current phase — adds build tooling and frontend infrastructure not justified by current scope, and conflicts with the single-machine, launcher-based deployment model.
- FastAPI + server-rendered HTML (chosen):
  - Already proven in Target RP Finder; no new framework risk, no client-side build step, fits directly into the existing uvicorn/VBS launcher contract.

## Why chosen
FastAPI + server-rendered HTML preserves the actual boundary ADR-0001 protects — business rules live in service modules, the renderer reflects persisted workflow truth and contains no logic of its own — without requiring Streamlit's reactive session model. It also matches deployment that is already contracted and working (`DEPLOYMENT.md`), avoiding a rewrite for a problem that isn't the real risk.

## Consequences
- Easier: deployment stays on the already-stamped uvicorn/VBS launcher contract with no override needed going forward; no Streamlit session-state lifecycle to fight.
- Harder: server-rendered HTML requires more manual wiring for dynamic interactions (filters, partial updates) than Streamlit's reactive model provided for free.
- Requires: UI templates remain logic-free — routing derives from persisted workflow state, not from page/session variables; any partial-page interactivity (HTMX or plain JS) must call back into the service layer, never reimplement it client-side.
- Locks in: FastAPI as the renderer for projects already on this stack; does not retroactively change projects still running Streamlit unless they hit the same limits.

## Review trigger
Revisit if FastAPI + server-rendered HTML begins constraining workflow correctness or UI maintainability, or if a future project's interactivity needs exceed what server rendering can reasonably support.
