# Agentic SDLC for Amp

## Installation

Use the supported clone-based install flow in `docs/installation.md`.

Direct PyPI installation is not a supported path while the package is unpublished.

## Initialization Instructions 

**Read `.agents/skills/asdlc-using-agentic-sdlc/SKILL.md` before taking action.**

You have the **Agentic SDLC** framework installed. This gives you a structured, multi-stage software development lifecycle to follow — replacing ad-hoc coding with a disciplined, auditable process.

### The Prime Directive

**Check for a relevant skill BEFORE taking any action.** If there is a chance a skill applies, invoke it using the `view_file` tool. Skills override default behavior. 

1. **User's explicit instructions** — highest priority
2. **Agentic SDLC skills** — override default agent behavior
3. **Default agent behavior** — lowest priority

### How to Use Skills

Skills live in the `.agents/skills/` directory.

*   To invoke a skill, read its `SKILL.md` file using `view_file`.
*   Always start your session by looking at `.agents/skills/asdlc-using-agentic-sdlc/SKILL.md`.

### Mandatory Context Directory

All stage outputs are written to disk under `docs/`. Amp can use standard file editing tools (`write_to_file`, `replace_file_content`) to save these items.

### Hitl Checkpoints

If a skill specifies a `<HARD-GATE>` or a requirement for a HITL checkpoint, clearly state what requires approval, ask the user, and wait to proceed.

### Git Discipline

Read `.agents/skills/asdlc-git-discipline/SKILL.md` before any git operation (branch creation, committing, merging). All stories run on feature branches; all stage artifacts run on `docs/{stage}` branches. Nothing goes directly to `main`.
