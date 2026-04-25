# Platform Support: Codex

Codex uses `AGENTS.md` at the project root and reads `.agents/skills/` relative to that root.

## Installation

Use the canonical instructions in [docs/installation.md](../installation.md), or fetch the Codex-specific bootstrap doc:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/salauddin-ee/agentic-sdlc/main/.codex/INSTALL.md
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

Manual fallback:

```bash
mkdir -p /path/to/your-project/.agents
cp /path/to/agentic-sdlc/AGENTS.md /path/to/your-project/AGENTS.md
cp -r /path/to/agentic-sdlc/src/agentic_sdlc/skills /path/to/your-project/.agents/skills
```

## Notes

- The legacy shell bootstrap script is deprecated and not part of the supported setup path.
- The installed skill layout is `.agents/skills/<skill-name>/SKILL.md`.
- `docs/installation.md` is the source of truth for multi-platform install guidance.
