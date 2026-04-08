# Agentic SDLC — Codex Installation

## Setup

Tell Codex to fetch and follow these instructions:

```
Fetch and follow instructions from https://raw.githubusercontent.com/salauddin-ee/agentic-sdlc/main/.codex/INSTALL.md
```

Or install it locally:

### Option A: Submodule

1. Add the framework as a submodule:
   ```bash
   git submodule add https://github.com/salauddin-ee/agentic-sdlc.git .agentic-sdlc-framework
   ```
2. Copy the entry point and link skills:
   ```bash
   cp .agentic-sdlc-framework/AGENTS.md ./AGENTS.md
   ln -s .agentic-sdlc-framework/skills ./skills
   ```
3. Initialize the context directory:
   ```bash
   bash .agentic-sdlc-framework/scripts/init-context.sh .
   ```

### Option B: Copy

1. Copy the needed files from a local clone:
   ```bash
   cp /path/to/agentic-sdlc/AGENTS.md ./AGENTS.md
   cp -r /path/to/agentic-sdlc/skills ./skills
   cp -r /path/to/agentic-sdlc/scripts ./scripts
   ```
2. Initialize the context directory:
   ```bash
   bash scripts/init-context.sh .
   ```

Codex should see `AGENTS.md` at the project root, and the `skills/` directory must also be reachable from the project root.

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

## Other Platforms

Claude Code, Gemini CLI, Antigravity, and Amp are also supported. See `docs/future-platforms.md` for details.
