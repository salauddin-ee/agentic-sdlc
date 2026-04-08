# Brownfield Workflow

Use this workflow when adding a **feature or fix to an existing codebase**.

## Workflow Overview

```
context-harvest → brownfield-brainstorm → [brownfield-design] → brownfield-tech-plan
               → implementation-planning → story-breakdown → implementation
               → critical-review → testing → code-review → retrospective
```

`brownfield-design` is only needed if the story introduces UI changes.

---

## Stage 0: Context Harvest

**Skill:** `skills/context-harvest/SKILL.md`

What happens (once per project, not per story):
- Tech stack and versions documented
- Existing test suite run — baseline coverage recorded
- Code patterns catalogued (error handling, logging, validation, directory structure)
- Integration points mapped
- Fragile / high-risk areas flagged
- Output: `docs/architecture/existing-system.md`

**Critical rule:** Coverage baseline recorded here must NOT decrease by the end of any story.

---

## Stage 1: Brownfield Brainstorm

**Skill:** `skills/brownfield-brainstorm/SKILL.md`

What happens:
- Job-to-be-done identified
- Business outcome made measurable
- Given/When/Then acceptance criteria written
- Scope risks identified
- Existing behavior checked (can we extend it?)
- Output: Story section appended to `docs/product/features/brd.md`

---

## Stage 2: Brownfield Design (if UI)

**Skill:** `skills/brownfield-design/SKILL.md`

What happens:
- Existing design system read first
- Delta design only — new tokens and components introduced only where nothing existing fits
- Output: Design delta appended to `docs/product/design-system.md`

Skip if: story has no UI impact.

---

## Stage 3: Brownfield Tech Plan

**Skill:** `skills/brownfield-tech-plan/SKILL.md`

What happens:
- Existing code in affected area read first
- DRY check: does similar code already exist?
- Approach planned: YAGNI / KISS / extend existing patterns
- Regression risk assessed (which existing tests could break?)
- Interface contract change detected → triggers HITL if any
- Feature flag decision made
- Output: `docs/sdlc/workspaces/tech-plan-[STORY-ID].md`

---

## Stages 4–10: Same as Greenfield

From this point, the brownfield workflow follows the same stages as greenfield:

| Stage | Skill |
|---|---|
| 4 | `implementation-planning` — scoped to this story |
| 5 | `story-breakdown` |
| 6 | `implementation` — TDD, security non-negotiables |
| 7 | `critical-review` |
| 8 | `testing` — regression suite must still pass |
| 9 | `code-review` |
| 10 | `retrospective` — story retrospective appended |

## Key Differences vs. Greenfield

| Concern | Greenfield | Brownfield |
|---|---|---|
| Architecture | Defined from scratch (Stages 1–3) | Inherited — extend only with justification |
| Design system | Defined from scratch | Inherited — delta design only |
| Tech decisions | ADR per decision | ADR only if architecture changes |
| Test baseline | Not set yet | Set in context-harvest — must not decrease |
| Patterns | Define conventions | Follow existing conventions |
| Risk | Unknown unknowns | Known fragile areas flagged in context-harvest |
