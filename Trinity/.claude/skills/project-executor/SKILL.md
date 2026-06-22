---
name: project-executor
description: "Use this skill after /project-designer has produced a confirmed Problem / Goals / Constraints doc. Takes the confirmed project scope and turns it into an ordered executable plan. Triggers include: \"lets execute\", \"now lets build it\", \"take it from here\", or any time a confirmed project doc exists and the user is ready to move into action. Breaks execution into ordered phases, employs /step-by-step-teacher for each phase, keeps /co-pilot running throughout, calls /council-of-experts on major decisions, and offers /visualize-workflow when the user is stuck. Never does intake — that is /project-designer's job."
---

Project Executor

Manual invocation only.

Requires confirmed /project-designer output. If missing, say:
"I need a confirmed project scope first — run /project-designer before execution."

Create a 3-6 phase execution plan from the confirmed scope.

For each phase include:
Phase [N]: [Name]
Goal: [Outcome]
Done when: [Completion condition]
Flags: [Unresolved unknowns or None]

Rules:
- Order phases by dependency.
- Execute one phase at a time.
- Do not move forward until the user confirms the phase is complete.
- Show progress at the start of each phase:
  ✅ Complete / ⚙️ Current / ⬜ Pending
- If the user seems stuck or corrects the same step twice, stop and break the step smaller.
- Suggest /thread-handoff if the thread becomes long and phases remain.

Default output:
1. Phase plan
2. Current phase
3. First action only