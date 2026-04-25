# Platform Support: OpenCode

OpenCode should read the same project-root `AGENTS.md` and `.agents/skills/` layout as Codex.

## Installation

Use the canonical instructions in [docs/installation.md](../installation.md), or fetch the OpenCode-specific bootstrap doc:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/salauddin-ee/agentic-sdlc/main/.opencode/INSTALL.md
```

The supported local install flow is:

```bash
git clone https://github.com/salauddin-ee/agentic-sdlc.git
cd agentic-sdlc
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
mkdir -p /path/to/your/project
asdlc init /path/to/your/project
```
