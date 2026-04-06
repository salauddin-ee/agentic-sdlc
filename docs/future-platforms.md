# Future Platform Support

The agentic-sdlc MVP targets **Codex** via `AGENTS.md`. The following platforms are planned for future releases.

---

## Claude Code

**Entry point:** `CLAUDE.md`

Claude Code loads `CLAUDE.md` from the project root automatically. The file should:
1. Tell Claude to read `skills/using-agentic-sdlc/SKILL.md` at session start
2. Reference the skills catalog

**Plugin manifest:** `.claude-plugin/plugin.json`

```json
{
  "name": "agentic-sdlc",
  "version": "1.0.0",
  "description": "Agentic SDLC skills framework",
  "skills": "./skills"
}
```

**Skill invocation in Claude Code:**
Claude Code supports a `Skill` tool. Skills can be invoked by name. The `CLAUDE.md` should instruct Claude to use `Skill` before every action.

---

## Gemini CLI

**Entry point:** `GEMINI.md`

Gemini CLI loads `GEMINI.md` from the project root. The file should map Claude Code tool names to Gemini CLI equivalents and reference the skills directory.

**Tool name mapping:**

| Claude Code | Gemini CLI |
|---|---|
| `Skill()` | `activate_skill()` |
| `Read()` | `view_file()` |
| `Write()` | `write_to_file()` |
| `TodoWrite()` | Task tracking (manual) |

**Key differences:**
- Gemini CLI loads skill metadata at session start from YAML frontmatter
- Full skill content is loaded on demand via `activate_skill`
- Checklist items become action items rather than TodoWrite entries

---

## Cursor

**Entry point:** `.cursor-plugin/plugin.json`

Cursor supports plugins with a `plugin.json` manifest. Rules can be injected via `rules` or `context` fields.

**Plugin manifest:** `.cursor-plugin/plugin.json`

```json
{
  "name": "agentic-sdlc",
  "version": "1.0.0",
  "rules": [
    "Before any action, check if a skill in ./skills/ applies. Read the SKILL.md and follow it."
  ],
  "context": ["./skills/**/*.md"]
}
```

---

## Implementation Notes (for contributors)

When adding a new platform:
1. Create the platform entry point file (`CLAUDE.md`, `GEMINI.md`, etc.)
2. Create the platform plugin manifest if applicable
3. Map tool names from Claude Code equivalents
4. Update `README.md` installation section
5. Test by running the `using-agentic-sdlc` skill on the new platform
6. Document any behavioral differences in this file

---

*See README.md for current installation instructions (Codex MVP).*
