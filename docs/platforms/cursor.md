# Platform Support: Cursor

Cursor does not have a supported plugin or manifest path in this repository.

## Installation

Use the canonical instructions in [docs/installation.md](../installation.md).

Recommended path:

```bash
git clone https://github.com/salauddin-ee/agentic-sdlc.git
cd agentic-sdlc
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
mkdir -p /path/to/your/project
asdlc init /path/to/your/project
```

After setup, keep `AGENTS.md` in the target project root so Cursor can use the same project instructions as other agents.
