# Agentic SDLC — Codex Installation

## Setup

Tell Codex to fetch and follow these instructions:

```
Fetch and follow instructions from https://raw.githubusercontent.com/<owner>/agentic-sdlc/main/.codex/INSTALL.md
```

Or, if you've cloned this repository into your project:

1. Ensure `AGENTS.md` is at the root of your project (or this repo is cloned there)
2. Codex will automatically load `AGENTS.md` at session start
3. The agent will be instructed to read `skills/using-agentic-sdlc/SKILL.md` before any work begins

## Manual Setup

If automatic loading does not work, tell Codex at the start of each session:

```
Read AGENTS.md and then read skills/using-agentic-sdlc/SKILL.md before doing anything else.
```

## Verify Installation

Start a new Codex session and ask: *"What workflow should we follow for a new project?"*

The agent should:
1. Mention the Agentic SDLC framework
2. Ask whether this is greenfield or brownfield
3. Reference the `inception` or `context-harvest` skill as the starting point

## Initialize Context Directory

Run this script to create the `/.agentic-sdlc/` context directory in your project:

```bash
bash scripts/init-context.sh /path/to/your/project
```

## Future Platforms

Claude Code, Cursor, and Gemini CLI support is planned. See `docs/future-platforms.md`.
