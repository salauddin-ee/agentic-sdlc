# Platform Support: Gemini CLI

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
