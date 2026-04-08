# Skill Reference

Quick reference for all agentic-sdlc skills. For full instructions, read the `SKILL.md` file.

## Workflow 1: Greenfield

| Order | Skill | Trigger | Key Output |
|---|---|---|---|
| 0 | `using-agentic-sdlc` | Starting any session | Workflow selection |
| 1 | `inception` | New project from scratch | `docs/product/features/brd.md` |
| 2 | `design-system` | UI project | `docs/product/design-system.md` |
| 3 | `tech-architecture` | Before any code | `docs/architecture/tech-architecture.md`, ADRs |
| 3a | `coding-constitution` | Within tech-architecture | `docs/architecture/coding-standards.md` |
| 4 | `implementation-planning` | After architecture approved | `docs/sdlc/epics/implementation-plan.md` |
| 5 | `story-breakdown` | Before implementation | `docs/sdlc/epics/task-graph.md` |
| 6 | `implementation` | Writing code | Code + tests |
| 7 | `critical-review` | After implementation, per story | `docs/sdlc/retrospectives/critical-review.md` |
| 8 | `testing` | After review passes | `docs/sdlc/test-plans/test-plan.md` |
| 9 | `code-review` | Before merge | Review checklist |
| 10 | `retrospective` | Project complete | `docs/sdlc/retrospectives/retrospective.md` |

## Workflow 2: Brownfield

| Order | Skill | Trigger | Key Output |
|---|---|---|---|
| 0 | `context-harvest` | Unfamiliar existing codebase | `docs/architecture/existing-system.md` |
| 1 | `brownfield-brainstorm` | Story arrives | Story BRD appended to `brd.md` |
| 2 | `brownfield-design` | Story has UI changes | Design delta appended to `design-system.md` |
| 3 | `brownfield-tech-plan` | Story needs tech plan | `docs/sdlc/workspaces/tech-plan-[STORY-ID].md` |
| 4–10 | Same as greenfield from `implementation-planning` → `retrospective` | | |

## Shared Infrastructure

| Skill | Trigger | Purpose |
|---|---|---|
| `stage-gates` | At every stage boundary | Evaluate exit criteria, enforce no-proceed-on-fail |
| `hitl-protocol` | Mandatory checkpoints, irreversible actions | Structured human approval |
| `writing-skills` | Creating or editing skills | TDD-for-skills methodology |

## HITL Mandatory Checkpoints

1. After `inception` — before design/architecture
2. After `tech-architecture` — before any code
3. After `story-breakdown` — before implementation
4. Before any destructive operation (DB migration, data deletion, production write)
5. When agent is blocked by ambiguity
6. When an interface contract changes mid-implementation
7. When a Stage 3 architectural decision is superseded

## Context Directory

All stage outputs are written here (at project root):

```
docs/sdlc/
  domain.md              ← inception
  brd.md                 ← inception
  design-system.md       ← design-system
  accessibility.md       ← design-system
  tech-architecture.md   ← tech-architecture
  coding-constitution.md ← tech-architecture
  adr/                   ← tech-architecture (one file per decision)
  implementation-plan.md ← implementation-planning
  interface-contracts.md ← implementation-planning
  task-graph.md          ← story-breakdown
  critical-review.md     ← critical-review
  test-plan.md           ← testing
  retrospective.md       ← retrospective
  existing-system.md     ← context-harvest (brownfield only)
  tech-plan-*.md         ← brownfield-tech-plan (one per story)
```
