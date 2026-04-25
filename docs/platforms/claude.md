# Platform Support: Claude Code

**Entry point:** `AGENTS.md`

**Installation:** Use the canonical instructions in [docs/installation.md](../installation.md). Once installed, Claude Code reads `AGENTS.md` from the project root.

Claude Code uses the project-root `AGENTS.md` entry point and the standard `.agents/skills/` layout in the target project.

**Tool mapping:**
- Read Skill: file reading tools
- Write Document: file editing tools
- Task tracking: native task/todo workflow when available

**Key differences:**
- Claude Code currently uses the same manual project-root install path as the other supported agents.
- The repository does not ship a supported Claude plugin manifest; plugin packaging should only be added as a separate, spec-verified release step.
