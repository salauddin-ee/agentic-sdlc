# Agentic SDLC — Codex Installation

## Setup

Tell Codex to fetch and follow these instructions:

```
Fetch and follow instructions from https://raw.githubusercontent.com/salauddin-ee/agentic-sdlc/main/.codex/INSTALL.md
```

Or install it locally:

### Option A: Clone + CLI bootstrap (recommended)

1. Clone and install the framework:
   ```bash
   git clone https://github.com/salauddin-ee/agentic-sdlc.git
   cd agentic-sdlc
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -e .
   mkdir -p /path/to/your/project
   ```
2. Bootstrap your target project:
   ```bash
   asdlc init /path/to/your/project
   ```

### Option B: Manual copy

1. Copy the required files from a local clone:
   ```bash
   mkdir -p /path/to/your-project/.agents
   cp /path/to/agentic-sdlc/AGENTS.md /path/to/your-project/AGENTS.md
   cp -r /path/to/agentic-sdlc/src/agentic_sdlc/skills /path/to/your-project/.agents/skills
   ```
2. Create the minimum docs structure:
   ```bash
   mkdir -p /path/to/your-project/docs/architecture/adrs
   mkdir -p /path/to/your-project/docs/product/features
   mkdir -p /path/to/your-project/docs/sdlc/stories
   mkdir -p /path/to/your-project/docs/sdlc/workspaces
   mkdir -p /path/to/your-project/docs/sdlc/test-plans
   mkdir -p /path/to/your-project/docs/sdlc/retrospectives
   ```

Codex should see `AGENTS.md` at the project root, and the `.agents/skills/` directory must also be reachable from the project root.

## Manual Setup

If automatic loading does not work, tell Codex at the start of each session:

```
Read AGENTS.md and then read .agents/skills/asdlc-using-agentic-sdlc/SKILL.md before doing anything else.
```

## Verify Installation

Start a new Codex session and ask: *"What workflow should we follow for a new project?"*

The agent should:
1. Mention the Agentic SDLC framework
2. Ask whether this is greenfield or brownfield
3. Reference the `asdlc-inception` or `asdlc-context-harvest` skill as the starting point

## Other Platforms

For the canonical multi-platform install guide, see `docs/installation.md`.
