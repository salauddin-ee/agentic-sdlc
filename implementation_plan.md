# Agentic SDLC — Skills Framework Implementation Plan

Build an installable, Superpowers-style agentic skills framework from the Agentic SDLC Framework document. Users drop this into their project (or install as a plugin) and their coding agent automatically follows the full SDLC lifecycle — brainstorming → design → architecture → implementation → review → retro.

**Framework name:** `agentic-sdlc`
**Cross-references:** `agentic-sdlc:<skill-name>`
**Context directory:** `/.agentic-sdlc` (at project root)
**MVP Platform:** Codex (other platforms documented in `docs/future-platforms.md`)

---

## Directory Structure

```
agentic-sdlc/
├── README.md                          # Project overview, installation, usage
├── package.json                       # Minimal manifest (name, version)
├── LICENSE                            # MIT
├── AGENTS.md                          # Codex/generic agent entry point
│
├── .codex/                            # Codex plugin instructions
│   └── INSTALL.md
│
├── skills/                            # All skills (flat namespace)
│   ├── using-agentic-sdlc/           # Meta: How to use this framework
│   │   └── SKILL.md
│   │
│   │── # ── WORKFLOW 1: Greenfield ──
│   ├── inception/                     # Stage 1: Brainstorm + BRD
│   │   └── SKILL.md
│   ├── design-system/                 # Stage 2: Visual/interaction design
│   │   └── SKILL.md
│   ├── tech-architecture/             # Stage 3: Architecture + ADRs
│   │   ├── SKILL.md
│   │   └── adr-template.md
│   ├── implementation-planning/       # Stage 4: Implementation plan
│   │   └── SKILL.md
│   ├── story-breakdown/               # Stage 5: Task DAG + stories
│   │   └── SKILL.md
│   ├── implementation/                # Stage 6: TDD implementation loop
│   │   └── SKILL.md
│   ├── critical-review/               # Stage 7: Adversarial review
│   │   └── SKILL.md
│   ├── testing/                       # Stage 8: Test plan execution
│   │   └── SKILL.md
│   ├── code-review/                   # Stage 9: Final review
│   │   └── SKILL.md
│   ├── retrospective/                 # Stage 10: Retro + skills update
│   │   └── SKILL.md
│   │
│   │── # ── WORKFLOW 2: Brownfield ──
│   ├── context-harvest/               # Stage 0: Existing system analysis
│   │   └── SKILL.md
│   ├── brownfield-design/             # Stage 1 (lite): Delta design
│   │   └── SKILL.md
│   ├── brownfield-brainstorm/         # Stage 2 (lite): Story-level BRD
│   │   └── SKILL.md
│   ├── brownfield-tech-plan/          # Stage 3 (lite): Story tech plan
│   │   └── SKILL.md
│   │
│   │── # ── SHARED INFRASTRUCTURE ──
│   ├── coding-constitution/           # Coding standards authoring
│   │   └── SKILL.md
│   ├── stage-gates/                   # Gate evaluation protocol
│   │   └── SKILL.md
│   ├── hitl-protocol/                 # Human-in-the-loop protocol
│   │   └── SKILL.md
│   └── writing-skills/                # Meta: How to create new skills
│       └── SKILL.md
│
├── templates/                         # Reusable document templates
│   ├── brd-template.md
│   ├── adr-template.md
│   ├── design-system-template.md
│   ├── implementation-plan-template.md
│   ├── task-graph-template.md
│   ├── test-plan-template.md
│   ├── retrospective-template.md
│   └── story-template.md
│
├── scripts/                           # Helper scripts
│   └── init-context.sh                # Initialize /.agentic-sdlc directory
│
└── docs/                              # Extended documentation
    ├── getting-started.md
    ├── workflow-greenfield.md
    ├── workflow-brownfield.md
    ├── skill-reference.md
    └── future-platforms.md            # Claude Code, Cursor, Gemini CLI plans
```

---

## Components

### Component 1: Entry Points & Manifests (Codex MVP)

| File | Purpose |
|---|---|
| `README.md` | Project overview, philosophy, Codex installation, skills catalog |
| `AGENTS.md` | Generic agent entry point — instructs agent to check skills first |
| `package.json` | `{ "name": "agentic-sdlc", "version": "1.0.0" }` |
| `.codex/INSTALL.md` | Codex-specific installation instructions |
| `LICENSE` | MIT |

---

### Component 2: Greenfield Workflow Skills (Stages 1–10)

Each skill uses YAML frontmatter + behavioral instructions + checklists + anti-patterns + red flags. All context artifacts write to `/.agentic-sdlc/`.

| Skill | Stage | Key Outputs |
|---|---|---|
| `using-agentic-sdlc` | Meta | — |
| `inception` | Stage 1 | `/.agentic-sdlc/domain.md`, `/.agentic-sdlc/brd.md` |
| `design-system` | Stage 2 | `/.agentic-sdlc/design-system.md`, `/.agentic-sdlc/accessibility.md` |
| `tech-architecture` | Stage 3 | `/.agentic-sdlc/tech-architecture.md`, `/.agentic-sdlc/adr/`, `/.agentic-sdlc/coding-constitution.md` |
| `implementation-planning` | Stage 4 | `/.agentic-sdlc/implementation-plan.md` |
| `story-breakdown` | Stage 5 | `/.agentic-sdlc/task-graph.md` |
| `implementation` | Stage 6 | Code + tests (TDD loop) |
| `critical-review` | Stage 7 | `/.agentic-sdlc/critical-review.md` |
| `testing` | Stage 8 | `/.agentic-sdlc/test-plan.md` |
| `code-review` | Stage 9 | Review checklist output |
| `retrospective` | Stage 10 | `/.agentic-sdlc/retrospective.md` |

HITL checkpoints: after Stage 1, after Stage 3, after Stage 5, and before any destructive operation.

---

### Component 3: Brownfield Workflow Skills

| Skill | Stage | Purpose |
|---|---|---|
| `context-harvest` | Stage 0 | Codebase fingerprinting → `/.agentic-sdlc/existing-system.md` |
| `brownfield-design` | Stage 1 lite | Delta design, inherit existing system |
| `brownfield-brainstorm` | Stage 2 lite | Job-to-be-done, acceptance criteria |
| `brownfield-tech-plan` | Stage 3 lite | YAGNI/KISS approach + regression risk |

---

### Component 4: Shared Infrastructure Skills

| Skill | Purpose |
|---|---|
| `coding-constitution` | Author / evaluate coding standards |
| `stage-gates` | Gate format, self-evaluation, loop-on-failure |
| `hitl-protocol` | HITL prompt format, mandatory checkpoints, timeout/defaults |
| `writing-skills` | TDD-for-skills, SKILL.md structure, testing methodology |

---

### Component 5: Templates (8 files)

Pre-filled, structured templates matching the formats defined in the framework document:

`brd-template.md` · `adr-template.md` · `design-system-template.md` · `implementation-plan-template.md` · `task-graph-template.md` · `test-plan-template.md` · `retrospective-template.md` · `story-template.md`

---

### Component 6: Scripts & Docs

| File | Purpose |
|---|---|
| `scripts/init-context.sh` | Creates `/.agentic-sdlc/` directory structure in user's project |
| `docs/getting-started.md` | First-time setup walkthrough |
| `docs/workflow-greenfield.md` | Visual guide to Workflow 1 |
| `docs/workflow-brownfield.md` | Visual guide to Workflow 2 |
| `docs/skill-reference.md` | Quick reference table for all skills |
| `docs/future-platforms.md` | Claude Code, Cursor, Gemini CLI implementation notes |

---

## Verification Plan

### Automated
- All SKILL.md files have valid YAML frontmatter (`name` + `description`)
- All cross-references between skills resolve to existing files
- All templates referenced in skills exist
- Markdown linted for formatting consistency

### Manual
- Install into a test project, verify skills load via Codex
- Walk through greenfield workflow (Stages 1→10)
- Walk through brownfield workflow (Stages 0→10)
- Verify gate evaluation halts progression on failure
