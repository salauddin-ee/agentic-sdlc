# Greenfield Workflow

Use this workflow when building a **new project from scratch** with no existing codebase.

## Workflow Overview

```text
inception → [design-system] → [ui-mockups] → tech-architecture
         → implementation-planning → story-breakdown → implementation
         → critical-review → testing → code-review → retrospective
```

`asdlc-design-system` is required if the project has a UI. `asdlc-ui-mockups` is required for a redesign, new landing page, or major visual contract change. `asdlc-tech-architecture` can still run before or after `asdlc-design-system`, but `asdlc-ui-mockups` must happen after `asdlc-design-system` and before implementation-planning begins.

---

## Stage 1: Inception

**Skill:** `.agents/skills/asdlc-inception/SKILL.md`
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

**Skill:** `.agents/skills/asdlc-design-system/SKILL.md`

What happens:
- Design tokens defined (color, typography, spacing, motion, breakpoints)
- Component inventory produced
- Accessibility requirements documented (WCAG 2.2 AA)
- Output: `docs/product/design-system.md`, `docs/product/accessibility.md`

Skip if: purely backend/API project with no user-facing UI.

---

## Stage 2a: UI Mockup Gate (if major UI change)

**Skill:** `.agents/skills/asdlc-ui-mockups/SKILL.md`
**HITL:** Required before Stage 4

What happens:
- Agent asks whether to create a mockup or import existing mockups
- A reviewable artifact is produced as screenshots or a coded prototype
- Visual approval is recorded in `docs/product/mockups.md`

Skip if: the UI work is not a redesign, new landing page, or major visual contract change.

---

## Stage 3: Tech Architecture

**Skill:** `.agents/skills/asdlc-tech-architecture/SKILL.md`
**HITL:** Required before Stage 4

What happens:
- Tech stack selected with ADRs written for every major decision
- C4 Level 1 + Level 2 diagrams produced
- Key sequence diagrams for critical flows
- Coding constitution authored (`.agents/skills/asdlc-coding-constitution/SKILL.md`)
- Output: `docs/architecture/tech-architecture.md`, `docs/architecture/adrs/`, `docs/architecture/coding-standards.md`

Gate: ADRs written, diagrams present, directory structure defined, security approach documented.

---

## Stage 4: Implementation Planning

**Skill:** `.agents/skills/asdlc-implementation-planning/SKILL.md`

What happens:
- Milestones defined with exit criteria
- Interface contracts locked between all modules
- Merge strategy selected via HITL and recorded in `docs/architecture/coding-standards.md`
- Risk log populated
- Definition of done agreed
- Output: `docs/sdlc/epics/implementation-plan.md`, `docs/architecture/data-domain.md`

---

## Stage 5: Story Breakdown

**Skill:** `.agents/skills/asdlc-story-breakdown/SKILL.md`
**HITL:** Required before Stage 6

What happens:
- Each milestone decomposed into stories with Given/When/Then acceptance criteria
- Dependency DAG built
- Parallel tracks defined with file ownership rules
- Output: `docs/sdlc/epics/task-graph.md`

---

## Stage 6: Implementation

**Skill:** `.agents/skills/asdlc-implementation/SKILL.md`

What happens (per story):
1. Write failing test (RED)
2. Implement minimal code (GREEN)
3. Refactor (clean + coding constitution compliant)
4. Run full test suite (no regressions)
5. Security checklist verified
6. Transition to critical-review, testing, and code-review

---

## Stage 7: Critical Review

**Skill:** `.agents/skills/asdlc-critical-review/SKILL.md`

What happens:
- Adversarial review: requirements coverage, code quality, security, integration
- P0/P1 findings block Stage 8
- P2 findings logged as tech debt
- P0/P1 found → return to Stage 6 and fix

---

## Stage 8: Testing

**Skill:** `.agents/skills/asdlc-testing/SKILL.md`

What happens:
- Full automated test suite runs (zero failures required)
- Test pyramid targets verified
- HITL test cases sent to human
- Performance targets verified against NFRs
- Output: `docs/sdlc/test-plans/test-plan.md`

---

## Stage 9: Code Review

**Skill:** `.agents/skills/asdlc-code-review/SKILL.md`

What happens:
- Standards compliance check
- Test quality review
- Security audit (dependency scan + auth verification)
- Operability check (logging, health check, graceful shutdown)
- Documentation completeness
- Story merged according to the configured merge strategy

---

## Stage 10: Retrospective

**Skill:** `.agents/skills/asdlc-retrospective/SKILL.md`

What happens:
- Execution summary written
- Requirements fidelity table completed
- If using the default epic branch strategy, final regression and HITL approval are recorded before `feature/EPIC-{ID}` merges to `main`
- Lessons learned documented
- Skills library updates proposed
- Output: `docs/sdlc/retrospectives/retrospective.md`
