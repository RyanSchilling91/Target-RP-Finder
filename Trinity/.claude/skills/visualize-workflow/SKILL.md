---
name: visualize-workflow
description: "Use this skill to generate visual diagrams and workflow maps from any input — code repos, text documents, pasted content, or even a verbal description in chat. Triggers include: \"visualize this\", \"map this out\", \"show me the flow\", \"diagram this\", \"how does data move through\", \"draw the workflow\", or any time the user wants to see how a system, process, or idea connects visually. The skill is input agnostic — it works from code, docs, or conversation. It reads what it has, picks the best visual format (flowchart, node map, architecture diagram, etc.), and generates a clear visual showing how data or steps enter, move, transform, and exit the system. Auto-trigger when the user's intent is to understand or communicate structure, flow, or connections — even if they don't explicitly ask for a diagram."
---

# Visualize Workflow

## Core Behavior
- Work from ANY input: code repo, file, pasted text, or verbal description in chat
- Never ask for a specific format — read what you have and build from it
- Pick the visual format that best fits the input (see Format Guide below)
- Always explain the diagram AFTER generating it — briefly, in plain English

## Input Types
Handle all of these without special prompting:
- Code / repo → trace how data moves through functions, APIs, storage
- Text document → extract steps, decisions, and connections
- Verbal / chat description → ask 1-2 clarifying questions MAX then build it
- Mixed → combine all sources into one unified map

## Format Guide
Choose the best fit automatically:

| Input Type | Best Visual |
|---|---|
| Data moving through a system | Flowchart with labeled arrows |
| How components connect | Node / bubble map |
| Steps in a process | Linear flow with decision points |
| System architecture | Layered architecture diagram |
| Project or idea mapping | Mind map style |

## What to Show
Always try to capture:
- Entry points — where does data/input come in?
- Transformations — what happens to it along the way?
- Storage — where does it live and how?
- Decision points — where does logic branch?
- Outputs — what comes out and where does it go?
- Connections — how do the pieces talk to each other?

## After the Visual
Always follow the diagram with:
1. A 2-3 sentence plain English summary of what the diagram shows
2. Any flaws, tangles, or gaps spotted in the flow
3. A single question: "Want me to zoom into any part of this?"

## Auto-Trigger Signals
Invoke this skill automatically when the user:
- Shares code or a doc and asks "how does this work"
- Uses words like: flow, map, diagram, visualize, trace, architecture, structure
- Seems lost in complexity and a visual would clearly help
- Says something like "I need to see how this connects"

## Token Efficiency
- Never ask the user to re-explain what they already gave you
- Build first, ask questions after if needed
- One diagram beats three paragraphs every time

## Incremental Editing
- NEVER regenerate the full diagram just because one part changed
- When the user requests a change, identify ONLY the affected section and redraw that part
- Keep the rest of the diagram intact
- Briefly note what changed: "Updated: [section name]"
- Only do a full regeneration if the user explicitly says 
  "start over" or "rebuild from scratch"
- This saves tokens and keeps the session fast and focused