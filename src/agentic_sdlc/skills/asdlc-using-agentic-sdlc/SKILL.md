---
name: asdlc-using-agentic-sdlc
description: Use when starting any conversation or project session — establishes how to find and invoke skills, and selects the correct workflow (greenfield vs brownfield) before any action is taken.
version: 1.0.0
---

Stop. Read this before doing anything else.

<EXTREMELY-IMPORTANT>
If there is even a 1% chance a skill applies to what you are doing, you MUST invoke it.
Skills override default behavior. User instructions override skills.
This is not optional. You cannot rationalize your way out of it.
</EXTREMELY-IMPORTANT>

## Instruction Priority

1. **User's explicit instructions** (conversation, AGENTS.md, project docs) — highest
2. **Agentic SDLC skills** — override default agent behavior
3. **Default agent behavior** — lowest priority

## How to Use Skills

Skills are in `.agents/skills/asdlc-<name>/SKILL.md`. Each has YAML frontmatter with `name` and `description`.

**To invoke a skill:** Read `.agents/skills/asdlc-<name>/SKILL.md` and follow it exactly.

**Never** rely on conversation memory for skill content — always read the current file.

## Workflow Selection

Before any work, determine which workflow applies:

```
Is this a brand-new project with no existing codebase?
  YES → Workflow 1 (Greenfield)
        asdlc-inception → asdlc-design-system → asdlc-ui-mockups → asdlc-tech-architecture
        → asdlc-implementation-planning → asdlc-story-breakdown → asdlc-implementation
        → asdlc-critical-review → asdlc-testing → asdlc-code-review → asdlc-retrospective

  NO  → Is this a story/feature on an existing codebase?
        YES → Workflow 2 (Brownfield)
              asdlc-context-harvest → asdlc-brownfield-brainstorm → asdlc-brownfield-design
              → asdlc-ui-mockups → asdlc-brownfield-tech-plan → asdlc-implementation-planning
              → asdlc-story-breakdown → asdlc-implementation → asdlc-critical-review
              → asdlc-testing → asdlc-code-review → asdlc-retrospective
```

**When in doubt, ask the user one question:** "Is this a new project from scratch, or are we adding to an existing codebase?"

## Skills Catalog

| Skill | Trigger |
|---|---|
| `asdlc-using-agentic-sdlc` | Starting any project or session |
| `asdlc-inception` | New project with unclear requirements |
| `asdlc-design-system` | Establishing visual/interaction language |
| `asdlc-ui-mockups` | User-facing redesign, new landing page, or major visual contract change needs visual approval |
| `asdlc-tech-architecture` | Making technology or architecture decisions |
| `asdlc-implementation-planning` | Creating execution plan from approved architecture |
| `asdlc-story-breakdown` | Decomposing a plan into executable tasks |
| `asdlc-implementation` | Writing production code for any task |
| `asdlc-critical-review` | Adversarial quality review of completed implementation |
| `asdlc-testing` | Executing test plan and verifying end-to-end behavior |
| `asdlc-code-review` | Final structured review before merge or handoff |
| `asdlc-retrospective` | Closing a project or story cycle |
| `asdlc-context-harvest` | Starting work on an unfamiliar existing codebase |
| `asdlc-brownfield-design` | Story introduces new UI in existing system |
| `asdlc-brownfield-brainstorm` | Understanding business impact of a story |
| `asdlc-brownfield-tech-plan` | Planning technical approach for a story |
| `asdlc-coding-constitution` | Establishing or reviewing coding standards |
| `asdlc-stage-gates` | Evaluating whether a stage's exit criteria are met |
| `asdlc-hitl-protocol` | Irreversible action or ambiguous decision needing human input |
| `asdlc-git-discipline` | Any git operation — branch creation, commits, merges |
| `asdlc-writing-skills` | Creating new skills or editing existing ones |

## Skill Types

**Rigid** (asdlc-implementation, asdlc-stage-gates, asdlc-hitl-protocol, asdlc-git-discipline): Follow exactly. No adaptation.

**Flexible** (asdlc-inception, asdlc-design-system): Adapt the process to the scale of the project. A one-page app needs a shorter design than an enterprise platform — but both still go through the stage.

## Rule: When Multiple Skills Apply

1. **Process skills first** (asdlc-inception, asdlc-context-harvest, asdlc-critical-review) — these determine HOW to approach
2. **Implementation skills second** (asdlc-implementation, asdlc-testing) — these guide execution

"Let's build X" → asdlc-inception first, then subsequent stages.
"Fix this bug" → Read asdlc-implementation skill, apply TDD.
"Add a feature to existing code" → asdlc-context-harvest first (if not done), then asdlc-brownfield-brainstorm.

## Context Directory

All stage outputs are written to a distributed `docs/` structure at the project root. Every stage reads and writes specific files. Never rely on conversation memory alone.

```text
docs/
  architecture/domain-model.md           ← inception
  architecture/existing-system.md        ← context-harvest (brownfield only)
  product/features/brd.md                ← inception
  product/design-system.md               ← design-system
  product/accessibility.md               ← design-system
  product/mockups.md                     ← ui-mockups
  architecture/tech-architecture.md      ← tech-architecture
  architecture/adrs/                     ← tech-architecture
  architecture/coding-standards.md       ← tech-architecture
  architecture/data-domain.md            ← implementation-planning
  sdlc/epics/implementation-plan.md      ← implementation-planning
  sdlc/epics/task-graph.md               ← story-breakdown
  sdlc/stories/                          ← story-breakdown
  sdlc/workspaces/                       ← implementation, brownfield-tech-plan
  sdlc/test-plans/test-plan.md           ← testing
  sdlc/retrospectives/critical-review.md ← critical-review
  sdlc/retrospectives/retrospective.md   ← retrospective
```

Run `asdlc init` to create this structure in a new project.

## Red Flags — You Are Rationalizing

| Thought | Reality |
|---|---|
| "This is too simple to need a design" | All projects go through the process. Design can be short. |
| "I'll skip the gate this once" | Gates exist because skipping them causes regressions. |
| "I don't need HITL for this" | If it's in the mandatory HITL list, it requires human sign-off. |
| "I remember what the skill says" | Skills evolve. Read the current version. |
| "This doesn't need TDD" | If it's production code, it needs a failing test first. |
| "Let me write some code first to explore" | Exploration prototypes must be thrown away before TDD begins. |
| "I already know what to build" | Unexamined assumptions are where wasted work hides. Run inception. |
| "We can skip architecture, it's a small project" | Small projects grow. ADRs take 10 minutes. Tech debt lasts forever. |
| "I'll document later" | Later never comes. Write artifacts now. |
| "The status doesn't matter" | Documents must be 'Approved' to pass gates. Update the status. |
| "Just start coding, I'll explain requirements as we go" | Coding without inception produces the wrong thing. Run inception first — it's fast. |
| "Let's skip inception and go straight to coding" | Inception exists to prevent this. Every project, every time. Run it. |
