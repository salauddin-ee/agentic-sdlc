# Agentic SDLC — OpenCode Installation

## Setup

Tell OpenCode to fetch and follow these instructions:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/salauddin-ee/agentic-sdlc/main/.opencode/INSTALL.md
```

Or install it locally.

### Option A: Clone + CLI bootstrap (recommended)

```bash
git clone https://github.com/salauddin-ee/agentic-sdlc.git
cd agentic-sdlc
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
mkdir -p /path/to/your/project
asdlc init /path/to/your/project
```

### Option B: Manual copy

```bash
mkdir -p /path/to/your-project/.agents
cp /path/to/agentic-sdlc/AGENTS.md /path/to/your-project/AGENTS.md
cp -r /path/to/agentic-sdlc/src/agentic_sdlc/skills /path/to/your-project/.agents/skills
mkdir -p /path/to/your-project/docs/architecture/adrs
mkdir -p /path/to/your-project/docs/product/features
mkdir -p /path/to/your-project/docs/sdlc/stories
mkdir -p /path/to/your-project/docs/sdlc/workspaces
mkdir -p /path/to/your-project/docs/sdlc/test-plans
mkdir -p /path/to/your-project/docs/sdlc/retrospectives
```

## Verify Installation

Start a new OpenCode session in the target project and ask:

```text
What workflow should we follow for a new project?
```

The agent should reference Agentic SDLC, ask whether the work is greenfield or brownfield, and name the correct first skill.
