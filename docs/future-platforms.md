# Platform Support

## Supported Platforms

| Platform | Entry Point | Status |
|---|---|---|
| Codex | `AGENTS.md` | ✅ Available |
| Claude Code | `CLAUDE.md` | ✅ Available |
| Gemini CLI | `GEMINI.md` | ✅ Available |
| Antigravity | `ANTIGRAVITY.md` | ✅ Available |
| Amp | `AMP.md` | ✅ Available |
| Cursor | `.cursor-plugin/plugin.json` | 🗺️ Planned |


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

*See [README.md](../README.md) for full installation instructions.*
