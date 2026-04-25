## If You Are an AI Agent — Read This First

This file governs work inside the `agentic-sdlc` source repository itself.

If you are using Agentic SDLC inside some other project, the project-root `AGENTS.md` for that target project comes from `src/agentic_sdlc/core/AGENTS.md`, not from this repo-root file.

You have the **Agentic SDLC** framework installed. This gives you a structured, multi-stage software development lifecycle to follow — replacing ad-hoc coding with a disciplined, auditable process.

### The Prime Directive

**Check for a relevant skill BEFORE taking any action — including asking clarifying questions.**

If there is even a 1% chance a skill applies, invoke it. Skills override default behavior. User instructions override skills.

Instruction priority:
1. **User's explicit instructions** (in conversation, AGENTS.md, project docs) — highest
2. **Agentic SDLC skills** — override default agent behavior
3. **Default agent behavior** — lowest priority

---

### How to Use Skills

In this source repository, packaged skills live in `src/agentic_sdlc/skills/`. In an initialized user project, those same skills are copied to `.agents/skills/`.

Each skill is a `SKILL.md` file with:
- A `name` and `description` (YAML frontmatter) — tells you WHEN to invoke it
- Detailed instructions for HOW to execute the stage or activity

**To use a skill in this repo:** Read the relevant `src/agentic_sdlc/skills/asdlc-<name>/SKILL.md` file at the start of any task that matches its trigger. Follow it exactly.

**Start here:** Always read `src/agentic_sdlc/skills/asdlc-using-agentic-sdlc/SKILL.md` at the beginning of a new project or conversation.

---

### Workflow Selection

```
Starting a new project from scratch?
  → Use Workflow 1 (Greenfield): asdlc-inception → asdlc-design-system → asdlc-ui-mockups
    → asdlc-tech-architecture
    → asdlc-implementation-planning → asdlc-story-breakdown → asdlc-implementation
    → asdlc-critical-review → asdlc-testing → asdlc-code-review → asdlc-retrospective

Working on an existing codebase?
  → Use Workflow 2 (Brownfield): asdlc-context-harvest → asdlc-brownfield-brainstorm
    → asdlc-brownfield-design → asdlc-ui-mockups → asdlc-brownfield-tech-plan
    → asdlc-implementation-planning
    → asdlc-story-breakdown → asdlc-implementation → asdlc-critical-review → asdlc-testing
    → asdlc-code-review → asdlc-retrospective
```

---

### Skills Catalog

| Skill | Trigger |
|---|---|
| `asdlc-using-agentic-sdlc` | Starting any project or session |
| `asdlc-inception` | New project with unclear requirements |
| `asdlc-design-system` | Establishing visual/interaction language |
| `asdlc-ui-mockups` | User-facing redesign, new landing page, or major visual contract change needing visual approval |
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

---

### Context Directory

All stage outputs are written to a distributed `docs/` structure at the project root. Never rely on conversation memory alone — write artifacts to disk.

```
docs/
  architecture/domain-model.md
  architecture/existing-system.md
  product/features/brd.md
  product/design-system.md
  product/accessibility.md
  product/mockups.md
  architecture/tech-architecture.md
  architecture/adrs/
  architecture/coding-standards.md
  architecture/data-domain.md
  sdlc/epics/implementation-plan.md
  sdlc/epics/task-graph.md
  sdlc/stories/
  sdlc/workspaces/
  sdlc/test-plans/test-plan.md
  sdlc/retrospectives/critical-review.md
  sdlc/retrospectives/retrospective.md
```

Run `asdlc init` to create this structure in a new project.

---

The Agentic SDLC framework is platform-agnostic. Platform documentation for framework users lives in the README and `docs/platforms/`:

- [Codex](docs/platforms/codex.md)
- [Claude Code](docs/platforms/claude.md)
- [Gemini CLI](docs/platforms/gemini.md)
- [Antigravity](docs/platforms/antigravity.md)
- [Amp](docs/platforms/amp.md)

### Red Flags — You Are Rationalizing

| Thought | Reality |
|---|---|
| "This is too simple to need a design" | All projects go through the process. Design can be short. |
| "I'll skip the gate this once" | Gates exist because skipping them causes regressions. |
| "I don't need HITL for this" | If it's in the mandatory HITL list, it requires human sign-off. |
| "I remember what the skill says" | Skills evolve. Read the current version. |
| "This doesn't need TDD" | If it's production code, it needs a failing test first. |
| "Let me write some code first to explore" | Exploration prototypes must be thrown away before TDD begins. |
