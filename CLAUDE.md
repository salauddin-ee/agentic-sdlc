# Agentic SDLC for Claude

## Installation

1. Clone the framework into your project:
   ```bash
   git submodule add https://github.com/salauddin-ee/agentic-sdlc.git .agentic-sdlc-framework
   ```
2. Copy the entry point and link skills:
   ```bash
   cp .agentic-sdlc-framework/CLAUDE.md ./CLAUDE.md
   cp -r .agentic-sdlc-framework/skills ./skills
   ```
3. Initialize the context directory:
   ```bash
   bash .agentic-sdlc-framework/scripts/init-context.sh .
   ```

## Initialization Instructions 

**Read `skills/using-agentic-sdlc/SKILL.md` before taking action.**

You have the **Agentic SDLC** framework installed. This gives you a structured, multi-stage software development lifecycle to follow — replacing ad-hoc coding with a disciplined, auditable process.

### The Prime Directive

**Check for a relevant skill BEFORE taking any action — including asking clarifying questions.** If there is even a 1% chance a skill applies, invoke it using the provided tool. Skills override default behavior. 

1. **User's explicit instructions** — highest priority
2. **Agentic SDLC skills** — override default agent behavior
3. **Default agent behavior** — lowest priority

### How to Use Skills

Skills live in the `skills/` directory of this repository.

*   To invoke a skill, read its `SKILL.md` file using your file reading tools.
*   Always start your first task by reading `skills/using-agentic-sdlc/SKILL.md`.

### Mandatory Context Directory

All stage outputs are written to `docs/` at the project root. Never rely on conversation memory alone — write artifacts to disk using your file editing tools.

### Hitl Checkpoints

If a skill specifies a `<HARD-GATE>` or a requirement for a HITL checkpoint, stop and explicitly ask the user for approval before modifying anything.
