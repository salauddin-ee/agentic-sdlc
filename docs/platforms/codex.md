# Platform Support: Codex

To use the Agentic SDLC framework with Codex, follow these steps:

## Installation

### Option A: Reference via URL
Tell Codex at the start of a session:
```
Fetch and follow instructions from https://raw.githubusercontent.com/<owner>/agentic-sdlc/main/.codex/INSTALL.md
```

### Option B: Local Install
You can install the framework locally in either of these verified layouts.

```bash
# Layout 1: keep the framework as a submodule
git submodule add https://github.com/<owner>/agentic-sdlc.git .agentic-sdlc-framework
cp .agentic-sdlc-framework/AGENTS.md ./AGENTS.md
ln -s .agentic-sdlc-framework/skills ./skills

# Layout 2: copy the needed files into your repo root
cp /path/to/agentic-sdlc/AGENTS.md ./AGENTS.md
cp -r /path/to/agentic-sdlc/skills ./skills
cp -r /path/to/agentic-sdlc/scripts ./scripts
```

## Initializing Context
Run the initialization script to create the `docs/` context directory:
```bash
# If you copied scripts into the repo root
bash scripts/init-context.sh .

# If the framework stays in a subdirectory
bash .agentic-sdlc-framework/scripts/init-context.sh .
```
