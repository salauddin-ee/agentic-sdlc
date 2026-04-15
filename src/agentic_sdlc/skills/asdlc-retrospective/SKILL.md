---
name: asdlc-retrospective
description: Use when a project or story cycle is complete — to capture what happened, extract lessons, and feed knowledge back into the skills library for future runs.
version: 1.0.0
---

Close the loop. Account for what happened, extract reusable knowledge into the skills library, and make the next project or story run smarter.

## When to Use

- After a greenfield project completes (full retrospective)
- After a brownfield story cycle closes (story retrospective appended to existing file)
- After any significant HITL intervention or rollback that deserves analysis

## Checklist

1. **Read the full context**: `docs/product/features/brd.md`, `docs/sdlc/epics/task-graph.md`, `docs/sdlc/retrospectives/critical-review.md`, `docs/sdlc/test-plans/test-plan.md`
2. **Write the retrospective** — using the `retrospective-template.md` file in this skill's directory
3. **Identify skills library updates** — new patterns worth capturing, existing skills to improve
4. **Propose process improvements** — changes to the framework that would improve future runs
5. **Write / append to `docs/sdlc/retrospectives/retrospective.md`**
6. **If skills library updates are proposed**: invoke `asdlc-writing-skills` skill

## Retrospective Format

In `docs/sdlc/retrospectives/retrospective.md`:

For full project or story cycles, use the `retrospective-template.md` file in this skill's directory. Append Story retrospectives to the existing file if it already exists.

## Skills Library Updates

If you identify a pattern worth capturing as a reusable skill:

1. Note it in the retrospective under "Skills library updates"
2. Answer: would this benefit someone working on a completely different project? If yes → create a skill
3. Invoke `asdlc-writing-skills` skill to create or update the skill file

## Gate

```
[ ] retrospective.md written (or appended) to docs/sdlc/retrospectives/
[ ] All P2 tech debt from critical-review logged under 'Tech debt logged'
[ ] Requirements fidelity table completed for all FRs
[ ] Skills library updates section completed (even if empty — 'none this cycle' is valid)
[ ] Process improvements section completed
[ ] If skills updates proposed: writing-skills skill invoked
```

## Red Flags

| Thought | Reality |
|---|---|
| "Nothing went wrong — no retro needed" | Something always went differently from plan. Write it down. |
| "Tech debt can skip the retro" | P2 findings not logged are P2 findings forgotten and repeated. |
| "Skills library updates are optional" | Patterns not captured are patterns repeated from scratch next time. |
| "The retro is just paperwork" | The retro is how the framework gets better. Skipping it penalizes future runs. |
