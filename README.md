# agentic-sdlc

A skills-based Software Development Lifecycle framework for autonomous coding agents. Drop it into any project and your agent follows a structured, auditable process — from requirements through retrospective — instead of ad-hoc coding.

---

## Philosophy

**Systematic over ad-hoc.** Every project goes through the same stages: inception, design, architecture, planning, implementation, review, testing, and retrospective. The framework enforces this by making skills mandatory, not optional.

**Evidence over claims.** Every stage writes artifacts to disk. No stage relies on conversation memory alone. All decisions are documented — requirements in `brd.md`, architecture decisions in ADRs, test results in `test-plan.md`.

**Gates over momentum.** Each stage has an explicit exit checklist. If it fails, the agent loops within the stage. Proceeding with a failed gate is a process violation.

**Human in the loop at irreversible decisions.** Architecture approval, destructive operations, and ambiguous decisions require explicit human sign-off before the agent proceeds.

---

## ⚠️ The Prime Directive

**Check for a relevant skill BEFORE taking any action — including asking clarifying questions.**

If there is even a 1% chance a skill applies, invoke it. Skills override default behavior. User instructions override skills.

Instruction priority:
1. **User's explicit instructions** — highest
2. **Agentic SDLC skills** — override default agent behavior
3. **Default agent behavior** — lowest priority

---

## How It Works

Each stage is a **skill** — a `SKILL.md` file the agent reads and follows. Skills contain:
- A `description` (YAML frontmatter) that tells the agent *when* to invoke it
- Behavioral instructions, checklists, and output formats
- Anti-rationalization "Red Flags" tables that help agents resist skipping discipline

The agent loads `AGENTS.md` at session start, which instructs it to check for relevant skills before any action.

---

## Dashboard

The framework includes a built-in dashboard to monitor project progress.

```bash
# Start the local dashboard
asdlc serve .
```

---

## Installation
The framework is now installable via `pip`, or can be manually added as a submodule.

### Option A: Install via Pip (Recommended)
```bash
# From your project root, or globally
pip install agentic-sdlc
```

### Option B: Clone and Install Locally (for development)
```bash
git clone https://github.com/salauddin-ee/agentic-sdlc.git
cd agentic-sdlc
pip install -e ".[dev]"
```

This gives you both `asdlc` and `asdlc-dev` commands.

### Option C: Manual Git Submodule
```bash
git submodule add https://github.com/salauddin-ee/agentic-sdlc .agentic-sdlc-framework
```

### Initialize Project
No matter how you install it, use the `asdlc` CLI to bootstrap your project:
```bash
asdlc init
```

---

## Developer CLI

For contributors and CI, a separate `asdlc-dev` CLI exposes eval and validation tools. It is available when installed with dev extras (Option B above, or `pip install agentic-sdlc[dev]`):

```bash
# Validate all SKILL.md files for structural correctness
asdlc-dev validate-skills .

# Run deterministic scenario fixtures against skills
asdlc-dev eval-skills .

# Eval a single skill
asdlc-dev eval-skills . --skill implementation
```

`asdlc-dev` also includes all public commands (`init`, `serve`).

---

## Skills Catalog

### Workflow 1: Greenfield (new project from scratch)

| Skill | Stage | Trigger |
|---|---|---|
| `using-agentic-sdlc` | Meta | Starting any session |
| `inception` | 1 | New project with unclear requirements |
| `design-system` | 2 | Establishing visual/interaction language |
| `ui-mockups` | 2a | User-facing redesign, new landing page, or major visual contract change |
| `tech-architecture` | 3 | Making technology or architecture decisions |
| `coding-constitution` | 3a | Establishing coding standards |
| `implementation-planning` | 4 | Creating execution plan from approved architecture |
| `story-breakdown` | 5 | Decomposing plan into executable tasks |
| `implementation` | 6 | Writing production code |
| `critical-review` | 7 | Adversarial quality review of completed implementation |
| `testing` | 8 | Executing test plan and verifying end-to-end behavior |
| `code-review` | 9 | Final structured review before merge |
| `retrospective` | 10 | Closing a project or story cycle |

### Workflow 2: Brownfield (existing codebase)

| Skill | Stage | Trigger |
|---|---|---|
| `context-harvest` | 0 | Starting on an unfamiliar existing codebase |
| `brownfield-brainstorm` | 1 | Understanding business impact of a story |
| `brownfield-design` | 2 | Story introduces new UI |
| `ui-mockups` | 2a | UI redesign or major visual contract change needs approval |
| `brownfield-tech-plan` | 3 | Planning technical approach for a story |
| *(Stages 4–10 same as greenfield)* | | |

### Shared Infrastructure

| Skill | Trigger |
|---|---|
| `stage-gates` | Evaluating whether a stage's exit criteria are met |
| `hitl-protocol` | Irreversible action or ambiguous decision needing human input |
| `writing-skills` | Creating or editing skills |

---

## Directory Structure

```
agentic-sdlc/
├── src/agentic_sdlc/
│   ├── skills/               ← One directory per skill, each with SKILL.md
│   │   ├── using-agentic-sdlc/
│   │   ├── inception/
│   │   ├── implementation/
│   │   ├── brownfield-design/
│   │   ├── stage-gates/
│   │   ├── hitl-protocol/
│   │   └── ...
│   ├── templates/            ← Document templates for each stage
│   └── fixtures/             ← Packaged eval fixtures for developer workflows
└── docs/
    ├── getting-started.md
    ├── workflow-greenfield.md
    ├── workflow-brownfield.md
    ├── skill-reference.md
    └── future-platforms.md
```

### Context directory (in your project)

```
docs/
  architecture/domain-model.md, product/features/brd.md  ← inception
  product/design-system.md, product/accessibility.md      ← design-system
  product/mockups.md                                      ← ui-mockups
  architecture/tech-architecture.md, architecture/adrs/   ← tech-architecture
  architecture/coding-standards.md                        ← coding-constitution
  sdlc/epics/implementation-plan.md, architecture/data-domain.md ← implementation-planning
  sdlc/epics/task-graph.md                                ← story-breakdown
  sdlc/stories/STORY-*.md                                 ← story-breakdown
  sdlc/retrospectives/critical-review.md                  ← critical-review
  sdlc/test-plans/test-plan.md                            ← testing
  sdlc/retrospectives/retrospective.md                    ← retrospective
  architecture/existing-system.md                         ← context-harvest (brownfield)
  sdlc/workspaces/tech-plan-*.md                          ← brownfield-tech-plan (per story)
```

---

## Platform Support

| Platform | Status | Instructions |
|---|---|---|
| Codex | ✅ Available | [docs/platforms/codex.md](docs/platforms/codex.md) |
| Claude Code | ✅ Available | [CLAUDE.md](CLAUDE.md) |
| Gemini CLI | ✅ Available | [docs/platforms/gemini.md](docs/platforms/gemini.md) |
| Antigravity | ✅ Available | [docs/platforms/antigravity.md](docs/platforms/antigravity.md) |
| Amp | ✅ Available | [docs/platforms/amp.md](docs/platforms/amp.md) |
| Cursor | 🗺️ Planned | [docs/future-platforms.md](docs/future-platforms.md)|

---

## License

MIT
