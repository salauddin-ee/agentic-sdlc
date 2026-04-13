# Skill Reference

Quick reference for all agentic-sdlc skills. For full instructions, read the `SKILL.md` file.

## Workflow 1: Greenfield

| Order | Skill | Trigger | Key Output |
|---|---|---|---|
| 0 | `asdlc-using-agentic-sdlc` | Starting any session | Workflow selection |
| 1 | `asdlc-inception` | New project from scratch | `docs/product/features/brd.md` |
| 2 | `asdlc-design-system` | UI project | `docs/product/design-system.md` |
| 2a | `asdlc-ui-mockups` | Redesign, landing page, or major visual contract change | `docs/product/mockups.md` |
| 3 | `asdlc-tech-architecture` | Before any code | `docs/architecture/tech-architecture.md`, ADRs |
| 3a | `asdlc-coding-constitution` | Within tech-architecture | `docs/architecture/coding-standards.md` |
| 4 | `asdlc-implementation-planning` | After architecture approved | `docs/sdlc/epics/implementation-plan.md` |
| 5 | `asdlc-story-breakdown` | Before implementation | `docs/sdlc/epics/task-graph.md` |
| 6 | `asdlc-implementation` | Writing code | Code + tests |
| 7 | `asdlc-critical-review` | After implementation, per story | `docs/sdlc/retrospectives/critical-review.md` |
| 8 | `asdlc-testing` | After review passes | `docs/sdlc/test-plans/test-plan.md` |
| 9 | `asdlc-code-review` | Before merge | Review checklist |
| 10 | `asdlc-retrospective` | Project complete | `docs/sdlc/retrospectives/retrospective.md` |

## Workflow 2: Brownfield

| Order | Skill | Trigger | Key Output |
|---|---|---|---|
| 0 | `asdlc-context-harvest` | Unfamiliar existing codebase | `docs/architecture/existing-system.md` |
| 1 | `asdlc-brownfield-brainstorm` | Story arrives | Story BRD appended to `brd.md` |
| 2 | `asdlc-brownfield-design` | Story has UI changes | Design delta appended to `design-system.md` |
| 2a | `asdlc-ui-mockups` | Major visible UI change needs approval | `docs/product/mockups.md` |
| 3 | `asdlc-brownfield-tech-plan` | Story needs tech plan | `docs/sdlc/workspaces/tech-plan-[STORY-ID].md` |
| 4–10 | Same as greenfield from `asdlc-implementation-planning` → `asdlc-retrospective` | | |

## Shared Infrastructure

| Skill | Trigger | Purpose |
|---|---|---|
| `asdlc-stage-gates` | At every stage boundary | Evaluate exit criteria, enforce no-proceed-on-fail |
| `asdlc-hitl-protocol` | Mandatory checkpoints, irreversible actions | Structured human approval |
| `asdlc-writing-skills` | Creating or editing skills | TDD-for-skills methodology |

## HITL Mandatory Checkpoints

1. After `asdlc-inception` — before design/architecture
2. After `asdlc-tech-architecture` — before any code
3. After `asdlc-ui-mockups` — before implementation-planning, brownfield-tech-plan, or production implementation continue for the affected UI
4. After `asdlc-story-breakdown` — before implementation
5. Before any destructive operation (DB migration, data deletion, production write)
6. When agent is blocked by ambiguity
7. When an interface contract changes mid-implementation
8. When a Stage 3 architectural decision is superseded

## Context Directory

All stage outputs are written here (at project root):

`asdlc-``text
docs/
  architecture/domain-model.md           ← asdlc-inception
  product/features/brd.md                ← asdlc-inception
  product/design-system.md               ← asdlc-design-system
  product/accessibility.md               ← asdlc-design-system
  product/mockups.md                     ← asdlc-ui-mockups
  architecture/tech-architecture.md      ← asdlc-tech-architecture
  architecture/coding-standards.md       ← asdlc-tech-architecture
  architecture/adrs/                     ← asdlc-tech-architecture (one file per decision)
  sdlc/epics/implementation-plan.md      ← asdlc-implementation-planning
  architecture/data-domain.md            ← asdlc-implementation-planning
  sdlc/epics/task-graph.md               ← asdlc-story-breakdown
  sdlc/retrospectives/critical-review.md ← asdlc-critical-review
  sdlc/test-plans/test-plan.md           ← asdlc-testing
  sdlc/retrospectives/retrospective.md   ← asdlc-retrospective
  architecture/existing-system.md        ← asdlc-context-harvest (brownfield only)
  sdlc/workspaces/tech-plan-*.md         ← asdlc-brownfield-tech-plan (one per story)
`asdlc-``
