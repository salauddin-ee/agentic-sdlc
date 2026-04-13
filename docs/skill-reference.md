# Skill Reference

Quick reference for all agentic-sdlc skills. For full instructions, read the `SKILL.md` file.

## Workflow 1: Greenfield

| Order | Skill | Trigger | Key Output |
|---|---|---|---|
| 0 | `using-agentic-sdlc` | Starting any session | Workflow selection |
| 1 | `inception` | New project from scratch | `docs/product/features/brd.md` |
| 2 | `design-system` | UI project | `docs/product/design-system.md` |
| 2a | `ui-mockups` | Redesign, landing page, or major visual contract change | `docs/product/mockups.md` |
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
| 2a | `ui-mockups` | Major visible UI change needs approval | `docs/product/mockups.md` |
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
3. After `ui-mockups` — before implementation-planning, brownfield-tech-plan, or production implementation continue for the affected UI
4. After `story-breakdown` — before implementation
5. Before any destructive operation (DB migration, data deletion, production write)
6. When agent is blocked by ambiguity
7. When an interface contract changes mid-implementation
8. When a Stage 3 architectural decision is superseded

## Context Directory

All stage outputs are written here (at project root):

```text
docs/
  architecture/domain-model.md           ← inception
  product/features/brd.md                ← inception
  product/design-system.md               ← design-system
  product/accessibility.md               ← design-system
  product/mockups.md                     ← ui-mockups
  architecture/tech-architecture.md      ← tech-architecture
  architecture/coding-standards.md       ← tech-architecture
  architecture/adrs/                     ← tech-architecture (one file per decision)
  sdlc/epics/implementation-plan.md      ← implementation-planning
  architecture/data-domain.md            ← implementation-planning
  sdlc/epics/task-graph.md               ← story-breakdown
  sdlc/retrospectives/critical-review.md ← critical-review
  sdlc/test-plans/test-plan.md           ← testing
  sdlc/retrospectives/retrospective.md   ← retrospective
  architecture/existing-system.md        ← context-harvest (brownfield only)
  sdlc/workspaces/tech-plan-*.md         ← brownfield-tech-plan (one per story)
```
