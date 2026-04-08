# Platform Support: Codex

To use the Agentic SDLC framework with Codex, follow these steps:

## Installation

### Option A: Reference via URL
Tell Codex at the start of a session:
```
Fetch and follow instructions from https://raw.githubusercontent.com/salauddin-ee/agentic-sdlc/main/.codex/INSTALL.md
```

### Option B: Local Install (submodule)

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

### Option C: Local Install (copy)

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
