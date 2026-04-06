# Getting Started with Agentic SDLC

This guide walks you through setting up and using the agentic-sdlc framework in your project.

## What is agentic-sdlc?

A skills-based SDLC framework that gives your coding agent a structured, disciplined process for building software — from requirements through retrospective. Inspired by [Superpowers](https://github.com/obra/superpowers).

Instead of ad-hoc coding, your agent follows a documented lifecycle:

```
Greenfield: inception → design → architecture → planning → stories → code → review → test → retro
Brownfield: context harvest → brainstorm → design → plan → stories → code → review → test → retro
```

Each stage has: explicit inputs, explicit outputs written to disk, a gate that must pass before proceeding, and HITL checkpoints at critical transitions.

## Prerequisites

- A Codex-compatible coding agent
- Git (recommended)

## Installation (Codex)

### Option A: Install into your project

Replace `<owner>` with the GitHub user or organization that hosts this repository.

```bash
# From your project root
git submodule add https://github.com/<owner>/agentic-sdlc .agentic-sdlc-framework

# Or just copy the files
cp -r /path/to/agentic-sdlc/skills ./skills
cp /path/to/agentic-sdlc/AGENTS.md ./AGENTS.md
```

Then tell Codex at the start of your session:
```
Read AGENTS.md and then read skills/using-agentic-sdlc/SKILL.md before doing anything else.
```

### Option B: Reference remotely

Tell Codex:
```
Fetch and follow instructions from https://raw.githubusercontent.com/<owner>/agentic-sdlc/main/.codex/INSTALL.md
```

## Initialize Context Directory

Run the init script in your project root to create the `/.agentic-sdlc/` directory:

```bash
bash scripts/init-context.sh /path/to/your-project
# or from within your project:
bash /path/to/agentic-sdlc/scripts/init-context.sh .
```

This creates stub files for every stage artifact. The agent will fill them in as it works through the lifecycle.

## Starting a Session

### New project (greenfield)
```
Tell your agent: "Start a new project. Read AGENTS.md first."
```

The agent should:
1. Read `AGENTS.md`
2. Read `skills/using-agentic-sdlc/SKILL.md`
3. Determine this is greenfield
4. Invoke `skills/inception/SKILL.md`
5. Begin asking clarifying questions before any code is written

### Existing project (brownfield)
```
Tell your agent: "We're adding a new feature to an existing codebase. Read AGENTS.md first."
```

The agent should:
1. Read `AGENTS.md`
2. Read `skills/using-agentic-sdlc/SKILL.md`
3. Determine this is brownfield
4. Invoke `skills/context-harvest/SKILL.md`
5. Analyze the codebase before proposing any changes

## Verify It's Working

Ask your agent: *"What workflow should we follow?"*

Expected response:
- References agentic-sdlc framework
- Asks greenfield vs brownfield
- Names the starting skill (`inception` or `context-harvest`)

If the agent starts writing code without going through these steps, it has not loaded the skills correctly.

## The Context Directory

```
/.agentic-sdlc/
  domain.md            — what the business domain is
  brd.md               — requirements (filled in at inception)
  design-system.md     — design tokens and components
  tech-architecture.md — architecture decisions
  adr/                 — one ADR per major decision
  coding-constitution.md — project coding standards
  implementation-plan.md — milestones and contracts
  task-graph.md        — stories and dependency graph
  test-plan.md         — test results
  critical-review.md   — adversarial review findings
  retrospective.md     — lessons learned
```

Never rely on conversation memory — every stage writes to these files.

## Next Steps

- [Workflow: Greenfield](workflow-greenfield.md)
- [Workflow: Brownfield](workflow-brownfield.md)
- [Skill Reference](skill-reference.md)
- [Future Platform Support](future-platforms.md) — Claude Code, Cursor, Gemini CLI
