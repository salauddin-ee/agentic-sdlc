# Platform Support: Gemini CLI

**Entry point:** `AGENTS.md`

**Installation:** Use the canonical instructions in [docs/installation.md](../installation.md). Once installed, Gemini CLI uses `AGENTS.md` from the project root.

Gemini CLI uses the project-root `AGENTS.md` entry point and the standard `.agents/skills/` layout in the target project.

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
