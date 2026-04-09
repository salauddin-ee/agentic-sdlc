# Multi-Agent Orchestration Skill (Draft)

*This is a draft of the proposed `agent-orchestration` skill, to be used when the `story-breakdown` DAG has parallel tracks.*

---
name: agent-orchestration
description: Governs how multiple agents (or sub-agents) execute parallel tracks from the dependency DAG simultaneously, including synchronization and conflict resolution.
version: 1.0.0
---

Governs how multiple agents (or sub-agents) execute parallel tracks from the dependency DAG.

## When to Use

- When the `story-breakdown` DAG has 2+ independent parallel tracks.
- When the agent platform supports sub-agent spawning (e.g., Antigravity `browser_subagent`, Claude parallel tool calls, Codex multi-task).

## Orchestration Protocol

1. **Read the DAG** from `docs/sdlc/epics/EPIC-[ID].md`.
2. **Identify parallelizable tracks** — tracks with no dependency on each other.
3. **Verify prerequisites:**
   - All interface contracts are locked in `docs/architecture/data-domain.md`.
   - File ownership is exclusive per track (no overlapping files).
   - Each track has its own feature branch naming: `feature/TRACK-[X]-STORY-[ID]`.
4. **Spawn sub-agents** — one per parallel track:
   - Each sub-agent receives: story file, workspace template, coding standards, `data-domain.md` (read-only).
   - Each sub-agent creates its own feature branch.
   - Each sub-agent follows the `implementation` skill independently.
5. **Synchronization points:**
   - **Merge point:** When tracks converge (DAG merge node), all upstream tracks must be merged to main before the downstream story begins.
   - **Contract change:** If any sub-agent needs to modify `data-domain.md`, it must STOP, raise HITL, and all other agents must pause until the change is approved and propagated.
   - **Conflict detection:** Before merging any track, run `git merge --no-commit --no-ff main` to detect conflicts. If conflicts exist → HITL.
6. **Completion protocol:**
   - Each sub-agent runs `critical-review` and `code-review` on its own track.
   - After all tracks merge, run a final integration `critical-review` on the combined result.
   - Run full test suite on `main` after all merges.

## Sub-Agent Context Template

Each sub-agent is spawned with this context:

```markdown
You are executing Track [X] of EPIC-[ID].

## Your stories (in order):
[list of STORY-IDs with acceptance criteria]

## Your file ownership:
[exclusive file list]

## Your branch:
feature/TRACK-[X]-STORY-[ID]

## Interface contracts (READ-ONLY):
[copy of data-domain.md — do NOT modify without HITL]

## Rules:
1. Follow `implementation` skill exactly (TDD, commits, workspace)
2. Only modify files in your ownership list
3. If you need to change a contract → STOP and report back
4. Commit after every RED/GREEN/REFACTOR cycle
5. After all stories complete → run critical-review → report back
```

## Constraints / Limitations

- **Maximum parallel tracks:** 3 (more than 3 increases merge conflict risk beyond manageable).
- Each track must be independently testable.
- No shared mutable state between tracks (contracts are read-only during parallel execution).
- If ANY track fails `critical-review` with P0/P1 → ALL tracks pause until resolved.

## Gate

```
[ ] DAG has 2+ independent parallel tracks
[ ] File ownership is exclusive across all tracks
[ ] Interface contracts are locked and copied to each sub-agent context
[ ] Each sub-agent has a dedicated feature branch
[ ] Merge points are identified and ordered
[ ] Conflict resolution strategy documented (HITL by default)
[ ] Platform supports sub-agent spawning (or manual multi-session protocol defined)
```
