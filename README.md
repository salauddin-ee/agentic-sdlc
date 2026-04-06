# agentic-sdlc

A skills-based Software Development Lifecycle framework for autonomous coding agents. Drop it into any project and your agent follows a structured, auditable process — from requirements through retrospective — instead of ad-hoc coding.

Inspired by [Superpowers](https://github.com/obra/superpowers).

---

## Philosophy

**Systematic over ad-hoc.** Every project goes through the same stages: inception, design, architecture, planning, implementation, review, testing, and retrospective. The framework enforces this by making skills mandatory, not optional.

**Evidence over claims.** Every stage writes artifacts to disk. No stage relies on conversation memory alone. All decisions are documented — requirements in `brd.md`, architecture decisions in ADRs, test results in `test-plan.md`.

**Gates over momentum.** Each stage has an explicit exit checklist. If it fails, the agent loops within the stage. Proceeding with a failed gate is a process violation.

**Human in the loop at irreversible decisions.** Architecture approval, destructive operations, and ambiguous decisions require explicit human sign-off before the agent proceeds.

---

## How It Works

Each stage is a **skill** — a `SKILL.md` file the agent reads and follows. Skills contain:
- A `description` (YAML frontmatter) that tells the agent *when* to invoke it
- Behavioral instructions, checklists, and output formats
- Anti-rationalization "Red Flags" tables that help agents resist skipping discipline

The agent loads `AGENTS.md` at session start, which instructs it to check for relevant skills before any action.

---

## Installation (Codex — MVP)

### Option A: Reference via URL

Replace `<owner>` with the GitHub user or organization that hosts this repository.

Tell Codex at the start of a session:
```
Fetch and follow instructions from https://raw.githubusercontent.com/<owner>/agentic-sdlc/main/.codex/INSTALL.md
```

### Option B: Clone into your project

```bash
git clone https://github.com/<owner>/agentic-sdlc.git
cp agentic-sdlc/AGENTS.md ./AGENTS.md
cp -r agentic-sdlc/skills ./skills
```

Then initialize the context directory:
```bash
bash agentic-sdlc/scripts/init-context.sh .
```

### Verify

Start a Codex session and ask: *"What workflow should we follow for a new project?"*

The agent should mention the Agentic SDLC framework, ask greenfield vs. brownfield, and name the starting skill.

---

## Skills Catalog

### Workflow 1: Greenfield (new project from scratch)

| Skill | Stage | Trigger |
|---|---|---|
| `using-agentic-sdlc` | Meta | Starting any session |
| `inception` | 1 | New project with unclear requirements |
| `design-system` | 2 | Establishing visual/interaction language |
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
├── AGENTS.md                 ← Codex entry point (copy to your project)
├── skills/                   ← All skills (flat namespace)
│   ├── using-agentic-sdlc/
│   ├── inception/
│   ├── design-system/
│   ├── tech-architecture/
│   ├── implementation-planning/
│   ├── story-breakdown/
│   ├── implementation/
│   ├── critical-review/
│   ├── testing/
│   ├── code-review/
│   ├── retrospective/
│   ├── context-harvest/
│   ├── brownfield-brainstorm/
│   ├── brownfield-design/
│   ├── brownfield-tech-plan/
│   ├── coding-constitution/
│   ├── stage-gates/
│   ├── hitl-protocol/
│   └── writing-skills/
├── templates/                ← Document templates for each stage
├── scripts/
│   └── init-context.sh       ← Creates /.agentic-sdlc/ in your project
└── docs/
    ├── getting-started.md
    ├── workflow-greenfield.md
    ├── workflow-brownfield.md
    ├── skill-reference.md
    └── future-platforms.md   ← Claude Code, Cursor, Gemini CLI roadmap
```

### Context directory (in your project)

```
/.agentic-sdlc/
  domain.md, brd.md               ← inception
  design-system.md, accessibility.md  ← design-system
  tech-architecture.md, adr/       ← tech-architecture
  coding-constitution.md           ← coding-constitution
  implementation-plan.md, interface-contracts.md  ← implementation-planning
  task-graph.md                    ← story-breakdown
  critical-review.md               ← critical-review
  test-plan.md                     ← testing
  retrospective.md                 ← retrospective
  existing-system.md               ← context-harvest (brownfield)
  tech-plan-*.md                   ← brownfield-tech-plan (per story)
```

---

## Platform Support

| Platform | Status |
|---|---|
| Codex | ✅ Available — see `AGENTS.md` |
| Claude Code | ✅ Available — see `CLAUDE.md` and `.claude-plugin/plugin.json` |
| Gemini CLI | ✅ Available — see `GEMINI.md` |
| Antigravity | ✅ Available — see `ANTIGRAVITY.md` |
| Amp (ampcode.com) | ✅ Available — Amp natively reads `.agents/skills/` (see `AMP.md`) |
| Cursor | 🗺️ Planned |

---

## License

MIT
