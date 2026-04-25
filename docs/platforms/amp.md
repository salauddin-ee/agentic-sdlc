# Platform Support: Amp

**Entry point:** `AGENTS.md`

**Installation:** Use the canonical instructions in [docs/installation.md](../installation.md). Once installed, Amp reads `AGENTS.md` at startup.

Amp uses the project-root `AGENTS.md` entry point and the standard `.agents/skills/` layout in the target project.

**Tool mapping:**
- Read Skill: `view_file`
- Write Document: `write_to_file` or `replace_file_content`

**Key differences:**
- Like Antigravity, Amp uses explicit file reading/writing tools rather than native framework skill activations.
- Features a strict requirement for explicit HITL (Human-in-the-Loop) pauses before proceeding past gates.
