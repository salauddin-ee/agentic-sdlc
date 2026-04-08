# Greenfield Workflow

Use this workflow when building a **new project from scratch** with no existing codebase.

## Workflow Overview

```
inception → [design-system] → tech-architecture → implementation-planning
         → story-breakdown → implementation → critical-review
         → testing → code-review → retrospective
```

`design-system` is required if the project has a UI. It can run before or after `tech-architecture` depending on whether UI is the primary driver.

---

## Stage 1: Inception

**Skill:** `skills/inception/SKILL.md`
**HITL:** Required before Stage 2

What happens:
- Agent asks clarifying questions (one at a time) to understand requirements
- Domain knowledge documented in `docs/architecture/domain-model.md`
- Business requirements documented in `docs/product/features/brd.md`
- User reviews and approves the BRD before proceeding

Gate (must pass):
- Business objective measurable
- User personas defined
- Success metrics quantified
- NFRs captured
- Out-of-scope explicit

---

## Stage 2: Design System (if UI)

**Skill:** `skills/design-system/SKILL.md`

What happens:
- Design tokens defined (color, typography, spacing, motion, breakpoints)
- Component inventory produced
- Accessibility requirements documented (WCAG 2.2 AA)
- Output: `docs/product/design-system.md`, `docs/product/accessibility.md`

Skip if: purely backend/API project with no user-facing UI.

---

## Stage 3: Tech Architecture

**Skill:** `skills/tech-architecture/SKILL.md`
**HITL:** Required before Stage 4

What happens:
- Tech stack selected with ADRs written for every major decision
- C4 Level 1 + Level 2 diagrams produced
- Key sequence diagrams for critical flows
- Coding constitution authored (`skills/coding-constitution/SKILL.md`)
- Output: `docs/architecture/tech-architecture.md`, `docs/architecture/adrs/`, `docs/architecture/coding-standards.md`

Gate: ADRs written, diagrams present, directory structure defined, security approach documented.

---

## Stage 4: Implementation Planning

**Skill:** `skills/implementation-planning/SKILL.md`

What happens:
- Milestones defined with exit criteria
- Interface contracts locked between all modules
- Risk log populated
- Definition of done agreed
- Output: `docs/sdlc/epics/implementation-plan.md`, `docs/architecture/data-domain.md`

---

## Stage 5: Story Breakdown

**Skill:** `skills/story-breakdown/SKILL.md`
**HITL:** Required before Stage 6

What happens:
- Each milestone decomposed into stories with Given/When/Then acceptance criteria
- Dependency DAG built
- Parallel tracks defined with file ownership rules
- Output: `docs/sdlc/epics/task-graph.md`

---

## Stage 6: Implementation

**Skill:** `skills/implementation/SKILL.md`

What happens (per story):
1. Write failing test (RED)
2. Implement minimal code (GREEN)
3. Refactor (clean + coding constitution compliant)
4. Run full test suite (no regressions)
5. Security checklist verified
6. Story marked complete in task-graph

---

## Stage 7: Critical Review

**Skill:** `skills/critical-review/SKILL.md`

What happens:
- Adversarial review: requirements coverage, code quality, security, integration
- P0/P1 findings block Stage 8
- P2 findings logged as tech debt
- P0/P1 found → return to Stage 6 and fix

---

## Stage 8: Testing

**Skill:** `skills/testing/SKILL.md`

What happens:
- Full automated test suite runs (zero failures required)
- Test pyramid targets verified
- HITL test cases sent to human
- Performance targets verified against NFRs
- Output: `docs/sdlc/test-plans/test-plan.md`

---

## Stage 9: Code Review

**Skill:** `skills/code-review/SKILL.md`

What happens:
- Standards compliance check
- Test quality review
- Security audit (dependency scan + auth verification)
- Operability check (logging, health check, graceful shutdown)
- Documentation completeness

---

## Stage 10: Retrospective

**Skill:** `skills/retrospective/SKILL.md`

What happens:
- Execution summary written
- Requirements fidelity table completed
- Lessons learned documented
- Skills library updates proposed
- Output: `docs/sdlc/retrospectives/retrospective.md`
