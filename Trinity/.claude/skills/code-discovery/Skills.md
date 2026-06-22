---
name: code-discovery
description: "Strategic codebase analysis skill. Triggers on: /code-discovery, 'what does this repo do', 'map this codebase', 'understand this app', 'how does this code work', or any time the user points at a repo and wants to understand what it does and how without reading every file. Builds a skeletal structure from docs first, then fills it in with targeted code reads. Designed to minimize token consumption on large repos and avoid prompt-and-pray full reads."
---

# code-discovery

## Invoke
- `/code-discovery` — run on repo in current working directory or context
- `/code-discovery [path]` — target a specific repo path

---

## The Problem This Skill Solves

A raw "read this repo" on a large codebase burns tokens indiscriminately and produces low-quality output because the model is spending cognitive budget on navigation, not interpretation. This skill front-loads structure before content — build the skeleton from docs, then fill in only what the skeleton needs.

---

## Phase 1 — Skeleton from Docs

Read these in order. Stop each phase as soon as you have enough to move forward.

**Pass 1A — Top-level orientation (always read these if they exist):**
```
README.md / README.rst / README.txt
docs/ or documentation/ directory listing (listing only, not full read)
ARCHITECTURE.md / DESIGN.md / OVERVIEW.md
package.json / pyproject.toml / requirements.txt / Cargo.toml (deps only)
```

**Output after Pass 1A:**
Internally hold:
- App name and stated purpose (from README)
- Primary language and framework
- Key dependencies (what this thing leans on)
- Docs directory structure (do not read yet)

If README alone answers "what does this do and how" clearly → move to Phase 3 immediately.

**Pass 1B — Docs deep read (only if docs directory exists):**
Read docs in this priority order:
1. Architecture or design docs
2. API or interface docs
3. Setup / deployment docs
4. Skip: changelogs, license, contributing guides

After Pass 1B, you should have the skeletal structure: what the app does, its major components, and how they connect.

---

## Phase 2 — Entry Point Identification

If docs gave a clear picture of structure → skip to Phase 3.

If not, find the entry point:

**Check in this order:**
```
main.py / app.py / server.py / index.js / index.ts / main.rs / main.go
src/main.* / src/app.* / src/index.*
Scripts section of package.json (start / dev / run commands)
Dockerfile or docker-compose.yml (CMD or ENTRYPOINT)
Makefile (first target or "run" target)
```

If no entry point is evident → state assumption:
> "No clear entry point found. Assuming [file] based on [reason]. Proceeding."

Read the entry point file. Do not follow every import — identify only:
- What gets initialized
- What the main execution path is
- What major modules/components are called

---

## Phase 3 — Targeted Component Reads

From the skeleton built in Phase 1-2, identify the 3-5 most important components by asking:
- What does the core feature touch?
- What handles data in/out?
- What enforces the main business logic?

Read those files. For each file:
- Read the top ~30 lines (imports + class/function signatures)
- Read function bodies only if the signature doesn't answer the question
- Skip: test files, migration files, generated files, config boilerplate

**Token discipline:** If a file is over 500 lines, read the top and bottom 50 lines plus any function that matches the component's stated purpose. Do not read linearly.

---

## Phase 4 — Discovery Report

Output this structure in tight prose — no padding:

**Problem**
One to two sentences. What user need or operational problem does this app address?

**How it solves it**
Two to four sentences. Core workflow: what goes in, what happens, what comes out. Name the primary technical mechanism.

**Architecture map**
Three to six bullets. Major components, what each does, how they connect. Format:
- `ComponentName` — what it does → feeds into `NextComponent`

**Key process steps**
The sequence a user or the system follows to accomplish the core function. Numbered, tight.

**What this replaces or accelerates**
One to two sentences. Manual process, previous system, or inefficiency this eliminates.

**Confidence level**
One line. "High — full docs present" / "Medium — entry point traced, no architecture docs" / "Low — no docs, assumed entry point." Flag what was inferred vs. confirmed.

**Open questions**
What the code alone cannot answer. External dependencies, undocumented logic, missing context. Flag these — never invent answers.

---

## Rules

- Always build skeleton before reading code — never start with raw file reads
- Never read a file you don't have a reason to read
- Never read linearly through large files — sample top, bottom, targeted functions
- Never speculate on what code does — if uncertain, flag it
- If docs exist and answer the question — stop reading and report
- Confidence level is mandatory — distinguish confirmed from inferred
- Target total token spend: equivalent of reading 5-8 average files, not the whole repo

---

## Escalation

If after Phase 1-3 the picture is still unclear:
> "Discovery incomplete — [specific gap]. To go deeper I'd need to read [specific files]. Proceed?"

Do not silently burn more tokens. Surface the gap and get confirmation first.