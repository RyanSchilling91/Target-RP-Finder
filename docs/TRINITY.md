# TRINITY.md

**Doc class: CONTRACT DOC** — house-standard persistence backend,
stamped and confirmed at project-init, not interviewed. Trinity is
the default persistence layer for every app unless a project
explicitly overrides it (override logged in
ASSUMPTIONS_AND_OPEN_QUESTIONS.md).

Verification layer for the persistence mechanism. Answers: "does
all persistence actually go through Trinity, the way the contract
says?" TRINITY.md owns the MECHANISM. It does NOT own the content —
which entities exist, and what is working vs derived vs evidence,
live in DATA_MODEL.md and STATE_CLASSIFICATION.md.

## What Trinity is
A plug-and-play SQLite backend. It is the SINGLE persistence path
for the app — every report and all long-term data is stored and
recalled through Trinity. No loose report folders on disk. No
SQLite calls scattered through services.

## Folder contract — what lives in Trinity/
- Access code — the modules services use to read and write
- Schema / migrations — table definitions and version history
- The .db file — the live SQLite database

Trinity/ is mounted on PYTHONPATH alongside src/
(`PYTHONPATH=src;Trinity` — must match DEPLOYMENT.md).

## Entry surface — ⚠️ OPEN, agent fills on first contact
How a service calls into Trinity is NOT yet defined. The agent
must fill this section from the real code the first time it
touches Trinity in a project, then confirm with the user.

This blank is LOAD-BEARING. The entry surface IS the enforcement
point for the single-persistence-path rule — until it is named,
"all writes go through Trinity" cannot be verified, because there
is no named thing to go through. When filling it, record:
- The exact module/class/function a service imports to persist
- Whether it is one client, per-entity repositories, or other
- The one rule: services NEVER touch SQLite except through this

Decision trigger: before any service writes or reads data.
Mirror this open item in ASSUMPTIONS_AND_OPEN_QUESTIONS.md.

## Backup — ⚠️ OPEN, must settle before persistence work
No automatic backup exists today. This MUST be settled and added
when persistence work begins — it is not optional.

The .db lives INSIDE Trinity/, inside the project folder. That
means the live database shares a fate with the code: a redeploy,
folder copy, or repo reset can clobber live evidence data. A
backup mechanism (path, trigger, retention) must be defined before
the app holds any real data.

Decision trigger: before the app stores any production/evidence data.
Mirror this open item in ASSUMPTIONS_AND_OPEN_QUESTIONS.md.

## Must never happen
- A service reads or writes SQLite outside the Trinity entry surface
- Reports or long-term data persisted anywhere but Trinity
- The live .db overwritten by a redeploy, folder copy, or repo reset
- Trinity dropped from PYTHONPATH while the data model expects it
- Evidence-class data mutated in place (see STATE_CLASSIFICATION.md)

## Verification criteria
- [ ] Entry surface section filled — names the one persistence path
- [ ] Every service write/read routes through that surface, no exceptions
- [ ] PYTHONPATH=src;Trinity present in DEPLOYMENT.md
- [ ] Backup mechanism defined before any real data is stored
- [ ] DATA_MODEL.md / STATE_CLASSIFICATION.md name Trinity as source of truth