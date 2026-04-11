# Platform Support: Amp

**Entry point:** `AMP.md`

Amp works similarly to Antigravity and reads `AMP.md` at startup to apply the SDLC framework constraints.

**Tool mapping:**
- Read Skill: `view_file`
- Write Document: `write_to_file` or `replace_file_content`

**Key differences:**
- Like Antigravity, Amp uses explicit file reading/writing tools rather than native framework skill activations.
- Features a strict requirement for explicit HITL (Human-in-the-Loop) pauses before proceeding past gates.
