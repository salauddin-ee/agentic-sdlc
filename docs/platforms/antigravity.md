# Platform Support: Antigravity

**Entry point:** `ANTIGRAVITY.md`

Antigravity operates within the Google DeepMind agentic framework. It reads `ANTIGRAVITY.md` at session start for initializing the Agentic SDLC framework.

**Tool mapping:**
- Read Skill: `view_file`
- Write Document: `write_to_file` or `replace_file_content`
- Task tracking: Internal `task.md` artifacts

**Key differences:**
- Antigravity uses a robust built-in "artifacts" system. Complex plans and UI outputs may be drafted in its internal brain directory, but all final SDLC artifacts MUST still be saved into the local `docs/` repository structure as the permanent system of record.
- Context loading requires explicit `view_file` calls to read `SKILL.md` instructions.
