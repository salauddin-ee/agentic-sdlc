# Agentic SDLC — Codex Installation

## Setup

Tell Codex to fetch and follow these instructions:

```
Fetch and follow instructions from https://raw.githubusercontent.com/<owner>/agentic-sdlc/main/.codex/INSTALL.md
```

Or install it locally in one of these layouts:

```bash
# Layout 1: keep the framework as a submodule
git submodule add https://github.com/<owner>/agentic-sdlc.git .agentic-sdlc-framework
cp .agentic-sdlc-framework/AGENTS.md ./AGENTS.md
ln -s .agentic-sdlc-framework/skills ./skills

# Layout 2: copy the framework files into your repo root
cp /path/to/agentic-sdlc/AGENTS.md ./AGENTS.md
cp -r /path/to/agentic-sdlc/skills ./skills
cp -r /path/to/agentic-sdlc/scripts ./scripts
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

## Initialize Context Directory

Run this script to create the `docs/` context directory in your project:

```bash
# If scripts were copied into the repo root
bash scripts/init-context.sh .

# If the framework stays in a subdirectory
bash .agentic-sdlc-framework/scripts/init-context.sh .
```

## Other Platforms

Claude Code, Gemini CLI, Antigravity, and Amp are also supported. See `docs/future-platforms.md` for details.
