# PROJECT_BRIEF.md

## Problem
Reviewing flagged compounds across a `.b` instrument batch folder currently requires manually opening every sample's `Target.RP` file by hand to find compounds commented `Udel`, `Udelete`, or `dubious` — slow and error-prone.

## Goals
- Browse to a `.b` folder, auto-discover top-level `.d` subfolders, classify each by name, and keep only samples.
- Parse each sample's `Target.RP` file, extract compounds whose REVIEW CODE column carries `Udel`, `Udelete`, or `dubious`, and display them tied to their sample and batch with totals and filters.
- Cache parsed results in Trinity so a previously parsed `.b` folder loads instantly without re-parsing.
- Clean V2 build on the current skill infrastructure — not a continuation of the prior (miscommunication-stalled) codebase.

## Constraints
- Windows desktop app, Python, single user (project owner), no folder-permission concerns on `.b` folders.
- Must persist through Trinity (existing plug-and-play SQLite backend, owned by the same user) — see [TRINITY.md](TRINITY.md).
- `Target.RP` is a fixed-width text export from the legacy Target application — parsing this format correctly is the primary risk area (root cause of the prior V1 stall).

## App-specific details (intake gaps)

### File format
`Target.RP` — fixed-width text report per `.d` injection folder. Header block (sample ID, dates, method, dilution factor) followed by one or more paged compound tables. Each compound row has a REVIEW CODE column; rows of interest carry `Udel`, `Udelete`, or `dubious` in that column. Confirmed against two real (published) USGS data-release files — see input-data classification in conversation history.

### `.d` folder classification rules
Folder names are case-inconsistent (tech-entered) — match case-insensitively:
- Starts with `cal` → Calibration
- Starts with `ccv` → CCV
- Starts with `cstpc` or `tpc` → Third-party calibration (TPC)
- Starts with `idl` → IDL
- Starts with `peb` → Blank
- Otherwise: 11-digit numeric ID, structured `YYYY` (4-digit year) + `DDD` (3-digit Julian day) + sequential run number (4 digits). Thousands digit of the sequential run number:
  - `9` → Prep blank
  - `8` → Surrogate
  - else → **Sample** (only type parsed/kept)

### Hosting / deployment
Local desktop app — standard house two-stage VBS launcher (see [DEPLOYMENT.md](DEPLOYMENT.md)). No remote hosting, no network exposure beyond `127.0.0.1`.

### Auth
None — single user, local machine, no folder permission boundary on `.b` folders today.

### Integrations
Trinity only (persistence/caching). No external APIs or services.

## Commands
TBD — filled once `src/` scaffold exists (test/lint/run commands).
