# Getting Started with Agentic SDLC

This guide walks you through setting up and using the agentic-sdlc framework in your project.

## What is agentic-sdlc?

A skills-based SDLC framework that gives your coding agent a structured, disciplined process for building software — from requirements through retrospective.

Instead of ad-hoc coding, your agent follows a documented lifecycle:

```text
Greenfield: inception → design → mockup gate → architecture → planning → stories → code → review → test → retro
Brownfield: context harvest → brainstorm → design → mockup gate → plan → stories → code → review → test → retro
```

Each stage has: explicit inputs, explicit outputs written to disk, a gate that must pass before proceeding, and HITL checkpoints at critical transitions.

## Prerequisites

- A supported coding agent (Codex, Claude Code, OpenCode, Cursor, Gemini CLI, Antigravity, or Amp)
- Git (recommended)

## Installation

See [Installation](installation.md) for the supported install paths, verification commands, and troubleshooting notes.

## Initialize Your Project

From within your project root, run:

```bash
asdlc init
```

This command will:
1. Create the `docs/sdlc/` directory structure.
2. Copy the necessary `.agents/skills/` and `templates/` into your project.
3. Copy `AGENTS.md` and platform-specific instructions to your root.

This creates stub files for every stage artifact. The agent will fill them in as it works through the lifecycle.

## Starting a Session

### New project (greenfield)
```
Tell your agent: "Start a new project. Read AGENTS.md first."
```

The agent should:
1. Read `AGENTS.md`
2. Read `.agents/skills/asdlc-using-agentic-sdlc/SKILL.md`
3. Determine this is greenfield
4. Invoke `.agents/skills/asdlc-inception/SKILL.md`
5. Begin asking clarifying questions before any code is written

### Existing project (brownfield)
```
Tell your agent: "We're adding a new feature to an existing codebase. Read AGENTS.md first."
```

The agent should:
1. Read `AGENTS.md`
2. Read `.agents/skills/asdlc-using-agentic-sdlc/SKILL.md`
3. Determine this is brownfield
4. Invoke `.agents/skills/asdlc-context-harvest/SKILL.md`
5. Analyze the codebase before proposing any changes

## Verify It's Working

Ask your agent: *"What workflow should we follow?"*

Expected response:
- References agentic-sdlc framework
- Asks greenfield vs brownfield
- Names the starting skill (`asdlc-inception` or `asdlc-context-harvest`)

If the agent starts writing code without going through these steps, it has not loaded the skills correctly.

## The Context Directory

```
docs/
  architecture/
    domain-model.md        — domain knowledge (inception)
    tech-architecture.md   — architecture decisions
    coding-standards.md    — coding standards
    data-domain.md         — interface contracts
    adrs/                  — one ADR per major decision
  product/
    features/brd.md        — business requirements (inception)
    design-system.md       — design tokens and components
    accessibility.md       — accessibility requirements
    mockups.md             — reviewed UI direction for major visual changes
  sdlc/
    epics/
      implementation-plan.md — milestones and contracts
      task-graph.md          — stories and dependency graph
    stories/               — individual story files
    test-plans/            — test results
    retrospectives/        — critical review and retrospective
```

Never rely on conversation memory — every stage writes to these files.

## Next Steps

- [Workflow: Greenfield](workflow-greenfield.md)
- [Workflow: Brownfield](workflow-brownfield.md)
- [Skill Reference](skill-reference.md)
- [Installation](installation.md)
