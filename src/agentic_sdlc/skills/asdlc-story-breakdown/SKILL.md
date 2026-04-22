---
name: asdlc-story-breakdown
description: Use when decomposing an implementation plan into atomic, independently executable tasks with a dependency graph — before implementation begins.
version: 1.0.0
---

Decompose the implementation plan into stories with Given/When/Then acceptance criteria, then build an explicit dependency DAG for parallel execution.

<HARD-GATE>
Do NOT begin implementation until the task graph is approved by the user via HITL. All interface contracts must be locked before parallel work begins — no interface to be defined during implementation.
</HARD-GATE>

## Checklist

1. **Read inputs**: `docs/sdlc/epics/implementation-plan.md`, `docs/architecture/data-domain.md`
2. **Break milestones into stories** — each story independently testable, < ~400 lines net new code
3. **Write acceptance criteria** — Given/When/Then for every story
4. **Build the dependency DAG** — identify which stories can run in parallel
5. **Define parallel track rules** — file ownership and merge strategy
6. **Flag HITL tasks** — any task that needs human input before starting (set `hitl_required: true`)
7. **Assess complexity & risk** — for each story set `complexity` (low|medium|high) for decomposition risk and `risk` (low|medium|high) for critical-path impact. These are independent dimensions.
8. **List files touched** — populate `files_touched` per story. Cross-check across parallel tracks for overlap; overlapping files require explicit merge strategy or track reassignment.
9. **Write an epic manifest** to `docs/sdlc/epics/EPIC-[ID].md` using the `task-graph-template.md` file in this skill's directory.
10. **Write `docs/sdlc/epics/task-graph.md`** — a summary of all epics and their dependency DAGs for cross-reference.
11. **Write story files** to `docs/sdlc/stories/STORY-[ID].md` for every individual ticket using the `story-template.md` file in this skill's directory.
12. **Self-review** — check DAG is acyclic, all interface contracts locked, all FRs covered, no `files_touched` overlap without merge strategy
13. **HITL checkpoint** — human reviews and approves epic breakdown before implementation


## Parallel Track Rules

For each parallel track, define:
- **Exclusive file ownership**: which files does this track own? (no overlap with other tracks)
- **Merge strategy**: feature branch per story, squash merge to main

## Gate

```
[ ] Every story has Given/When/Then acceptance criteria
[ ] Every FR from brd.md is covered by at least one story
[ ] DAG is acyclic — no circular dependencies
[ ] All parallel tracks have exclusive file ownership or explicit merge strategy
[ ] All interface contracts locked before parallel work begins
[ ] No story > ~400 lines net new code (split if larger)
[ ] Every story has complexity and risk assessed
[ ] Every story has files_touched populated
[ ] No files_touched overlap between parallel stories without explicit merge strategy
[ ] HITL checkpoint tasks marked (hitl_required: true where needed)
[ ] EPIC written to docs/sdlc/epics/, task-graph.md written to docs/sdlc/epics/, and STORY-*.md files written to docs/sdlc/stories/
```

## HITL Checkpoint

```
HITL REQUIRED
Stage: story-breakdown
Question: Does this story breakdown correctly decompose the implementation plan into distributed executable stories?
Context: Epic graph at docs/sdlc/epics/
Options: [A] Approved — begin implementation
         [B] Changes needed — specify which stories or dependencies to revise
Default if no response: Wait for explicit approval
```

## Red Flags

| Thought | Reality |
|---|---|
| "Acceptance criteria can be informal" | Informal = untestable. Use Given/When/Then, always. |
| "The dependency order is obvious" | Write the DAG anyway. Obvious orderings hide hidden dependencies. |
| "Parallel tracks sound complex" | Parallel tracks without file ownership rules cause merge conflicts. Define them now. |
| "Stories don't need HITL flags" | Some stories touch irreversible operations. Flag them before you forget. |
| "I'll split large stories later" | Large stories break TDD discipline. Split them now — set a hard limit. |
