# Installation

> Installation differs by platform. Pick your agent below.
> `agentic-sdlc` is not published on PyPI as of 2026-04-25, so the supported paths start from a local clone.

## Prerequisites

- Python 3.9 or newer for CLI-based setup
- `git`
- A local clone of `https://github.com/salauddin-ee/agentic-sdlc`
- `pipx` (optional, for Flow C — global install)

## Flow A - Recommended: clone + editable install + `asdlc init`

Use this when you want the CLI to scaffold `docs/` and copy the packaged skills into your project.

```bash
git clone https://github.com/salauddin-ee/agentic-sdlc.git
cd agentic-sdlc
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
mkdir -p /path/to/your/project
asdlc init /path/to/your/project
```

What this gives you:

- `AGENTS.md` in the target project root, copied from `src/agentic_sdlc/core/AGENTS.md`
- `.agents/skills/<skill-name>/SKILL.md`
- the standard `docs/` stage directories and stub files

## Flow B - Without Python: manual copy

Use this if you only want the skills and entry-point docs, or if Python installation is not available on the target machine.

```bash
git clone https://github.com/salauddin-ee/agentic-sdlc.git
mkdir -p /path/to/your-project/.agents
cp -r agentic-sdlc/src/agentic_sdlc/skills /path/to/your-project/.agents/skills
cp agentic-sdlc/src/agentic_sdlc/core/AGENTS.md /path/to/your-project/AGENTS.md
mkdir -p /path/to/your-project/docs/architecture/adrs
mkdir -p /path/to/your-project/docs/product/features
mkdir -p /path/to/your-project/docs/sdlc/stories
mkdir -p /path/to/your-project/docs/sdlc/workspaces
mkdir -p /path/to/your-project/docs/sdlc/test-plans
mkdir -p /path/to/your-project/docs/sdlc/retrospectives
```

Flow B does not install the CLI. You create the required directories yourself and manage future updates manually.

The repo-root `AGENTS.md` in `agentic-sdlc/` is for contributors working on the framework itself. Do not copy that file into a target project.

## Flow C - Global install with pipx (recommended for Mac/Linux)

Use this when you want `asdlc` and `asdlc-dev` available in **every terminal session** without activating a virtual environment.

```bash
# Install pipx if you don't have it
brew install pipx
pipx ensurepath

# Install agentic-sdlc globally from your local clone
pipx install -e /path/to/agentic-sdlc
```

What this gives you:

- `asdlc` and `asdlc-dev` available in every terminal without any activation step
- The editable install means code changes in the repo take effect immediately
- No conflict with other Python packages on your system

If you add new dependencies to `pyproject.toml` later:

```bash
pipx reinstall agentic-sdlc
```

Then initialise your project as normal:

```bash
asdlc init /path/to/your/project
```

## Claude Code

Use Flow A, B, or C above, then start Claude Code in the target project.

Claude Code currently uses the same manual project-root install path as the other supported agents.

An older Claude plugin manifest was removed from the supported repo surface because its schema was not verified against the official Claude Code plugin spec. If plugin packaging is reintroduced later, it should happen as a separate, spec-verified release step.

## OpenAI Codex

Codex can fetch the platform-specific instructions directly:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/salauddin-ee/agentic-sdlc/main/.codex/INSTALL.md
```

For local setup, use Flow A, B, or C from [docs/installation.md](installation.md), then start Codex in the target project root.

## OpenCode

OpenCode can fetch the platform-specific instructions directly:

```text
Fetch and follow instructions from https://raw.githubusercontent.com/salauddin-ee/agentic-sdlc/main/.opencode/INSTALL.md
```

For local setup, use Flow A, B, or C from [docs/installation.md](installation.md), then start OpenCode in the target project root.

## Cursor

Cursor does not have a supported manifest path in this repository. Use Flow A, B, or C above, then add the project-level instructions from `AGENTS.md` to your normal Cursor workflow.

## Other agents

Use Flow A, B, or C above for:

- Amp
- Antigravity
- Gemini CLI
- GitHub Copilot CLI

## Local development

For contributor workflows and the `asdlc-dev` entrypoint:

```bash
git clone https://github.com/salauddin-ee/agentic-sdlc.git
cd agentic-sdlc
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Verify the install

CLI path:

```bash
asdlc --help
```

Contributor path:

```bash
asdlc-dev --help
```

## Troubleshooting

### `externally-managed-environment`

If your Python interpreter blocks system-wide installs under PEP 668, use a virtual environment as shown in Flow A, or use `pipx` as shown in Flow C.

### `pipx: command not found`

Install pipx via Homebrew:

```bash
brew install pipx
pipx ensurepath
```

Then open a new terminal window and retry the install.

### `asdlc: command not found` after pipx install

Run `pipx ensurepath` and then open a new terminal, or add the pipx bin directory to your shell manually:

```bash
export PATH="$PATH:$HOME/.local/bin"
```

Add that line to your `~/.zshrc` to make it permanent.

### Direct PyPI install fails

The one-line PyPI install path is expected to fail until the package is published. Use the clone-based flows above instead.

Post-publish installation guidance is tracked in `docs/future/release-plan.md`. Until the package is published, treat the clone-based flows above as the supported setup paths.
