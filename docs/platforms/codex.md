# Platform Support: Codex

To use the Agentic SDLC framework with Codex, follow these steps:

## Installation

### Option A: Reference via URL
Tell Codex at the start of a session:
```
Fetch and follow instructions from https://raw.githubusercontent.com/<owner>/agentic-sdlc/main/.codex/INSTALL.md
```

### Option B: Local Clone
Clone this repository into your project and point Codex at the `AGENTS.md` file.

```bash
git clone https://github.com/<owner>/agentic-sdlc.git
cp agentic-sdlc/AGENTS.md ./AGENTS.md
cp -r agentic-sdlc/skills ./skills
```

## Initializing Context
Run the initialization script to create the `docs/sdlc/` directory:
```bash
bash scripts/init-context.sh .
```
