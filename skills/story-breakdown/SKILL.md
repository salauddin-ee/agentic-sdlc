---
name: story-breakdown
description: Use when decomposing an implementation plan into atomic, independently executable tasks with a dependency graph — before implementation begins.
---

Decompose the implementation plan into stories with Given/When/Then acceptance criteria, then build an explicit dependency DAG for parallel execution.

<HARD-GATE>
Do NOT begin implementation until the task graph is approved by the user via HITL. All interface contracts must be locked before parallel work begins — no interface to be defined during implementation.
</HARD-GATE>

## Checklist

1. **Read inputs**: `/.agentic-sdlc/implementation-plan.md`, `/.agentic-sdlc/interface-contracts.md`
2. **Break milestones into stories** — each story independently testable, < ~400 lines net new code
3. **Write acceptance criteria** — Given/When/Then for every story
4. **Build the dependency DAG** — identify which stories can run in parallel
5. **Define parallel track rules** — file ownership and merge strategy
6. **Flag HITL tasks** — any task that needs human input before starting
7. **Write `/.agentic-sdlc/task-graph.md`** — using format below
8. **Self-review** — check DAG is acyclic, all interface contracts locked, all FRs covered
9. **HITL checkpoint** — human reviews and approves task graph before implementation

## Story Format

```markdown
### STORY-NNN: [Title]

**Milestone:** M1
**Track:** A (parallel with B, C)
**Depends on:** STORY-NNN-1

**Acceptance criteria:**
- Given [context]
- When [action]
- Then [outcome]
- And [additional outcome if needed]

**Tasks:**
- [ ] Write failing test(s)
- [ ] Implement to make tests pass
- [ ] Refactor
- [ ] Update interface-contracts.md if any contract changed (triggers HITL)

**Files owned:** src/module/foo.ts, src/module/foo.test.ts
**Merge strategy:** Feature branch, squash merge to main
**HITL before starting:** [Yes/No — reason if Yes]
```

## Dependency Graph Format

In `/.agentic-sdlc/task-graph.md`:

```markdown
## Task dependency graph

STORY-001 (Foundation scaffold)
  └── STORY-002 (Auth module)      ← depends on STORY-001
  └── STORY-003 (Database layer)   ← depends on STORY-001
        └── STORY-005 (User CRUD)  ← depends on STORY-003
  └── STORY-004 (API gateway)      ← depends on STORY-001 + STORY-002
        └── STORY-006 (E2E tests)  ← merge point: depends on STORY-004 + STORY-005

Parallel tracks:
- Track A: STORY-002 → STORY-004
- Track B: STORY-003 → STORY-005
- Merge point: STORY-006 (waits for Track A and B)
```

## Parallel Track Rules

For each parallel track, define:
- **Exclusive file ownership**: which files does this track own? (no overlap with other tracks)
- **Merge strategy**: feature branch per story, squash merge to main
- **Conflict resolution**: if two tracks touch the same file, one must wait (make explicit in DAG)

## Task-Graph Document Structure

`/.agentic-sdlc/task-graph.md`:

```markdown
# Task graph

## Stories

[All stories in STORY-NNN format above]

## Dependency graph

[ASCII or Mermaid graph]

## Parallel tracks

| Track | Stories | Files owned | Merge strategy |
|---|---|---|---|

## HITL tasks

| Story | Reason for HITL |
|---|---|
```

## Gate

```
[ ] Every story has Given/When/Then acceptance criteria
[ ] Every FR from brd.md is covered by at least one story
[ ] DAG is acyclic — no circular dependencies
[ ] All parallel tracks have exclusive file ownership or explicit merge strategy
[ ] All interface contracts locked before parallel work begins
[ ] No story > ~400 lines net new code (split if larger)
[ ] HITL checkpoint tasks marked
[ ] task-graph.md written to /.agentic-sdlc/
```

## HITL Checkpoint

```
HITL REQUIRED
Stage: story-breakdown
Question: Does this task graph correctly decompose the implementation plan into executable stories?
Context: Task graph at /.agentic-sdlc/task-graph.md
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
