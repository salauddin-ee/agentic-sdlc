# Template Placement Analysis — Three Options

## The Core Question

Where should templates live: centralized or distributed inside skills?

---

## Option A: `.agents/templates/` (centralized under .agents)

```
.agents/
  skills/
    asdlc-inception/SKILL.md
    asdlc-implementation/SKILL.md
    ...
  templates/                    ← centralized
    brd-template.md
    workspace-template.md
    story-template.md
    ...
```

| Pro | Con |
|---|---|
| Easy to find — one directory | Disconnects templates from their owning skills |
| Clean project root | Skills reference external files — coupling |
| Simple CLI copy logic | Template updates require knowing which skill owns it |

---

## Option B: `asdlc-templates` skill (pseudo-skill)

```
.agents/skills/
  asdlc-templates/
    SKILL.md                    ← "Use when you need a template"
    brd-template.md
    workspace-template.md
    ...
```

| Pro | Con |
|---|---|
| Follows skill naming convention | **Not actually a skill** — it's a bucket |
| Discoverable via skill catalog | Violates what skills are ("behavioral instructions for specific situations") |
| | Agent would need to read asdlc-templates AND the real skill |
| | `asdlc-writing-skills` explicitly says "don't create a skill for standard practices" |

> [!CAUTION]
> **Option B violates the skill definition.** Skills are "reusable behavioral instructions for specific, repeating situations." A template bucket is a reference resource, not a behavioral skill.

---

## Option C: Templates as supporting files inside each skill ✅ RECOMMENDED

```
.agents/skills/
  asdlc-inception/
    SKILL.md
    brd-template.md             ← used only by this skill
  asdlc-design-system/
    SKILL.md
    design-system-template.md   ← used only by this skill
  asdlc-tech-architecture/
    SKILL.md
    adr-template.md             ← used only by this skill
  asdlc-implementation/
    SKILL.md
    workspace-template.md       ← used only by this skill
  asdlc-story-breakdown/
    SKILL.md
    story-template.md           ← used only by this skill
    task-graph-template.md      ← used only by this skill
  asdlc-implementation-planning/
    SKILL.md
    implementation-plan-template.md  ← used only by this skill
  asdlc-testing/
    SKILL.md
    test-plan-template.md       ← used only by this skill
  asdlc-retrospective/
    SKILL.md
    retrospective-template.md   ← used only by this skill
  asdlc-ui-mockups/
    SKILL.md
    mockups-template.md         ← used only by this skill
```

| Pro | Con |
|---|---|
| **Follows `asdlc-writing-skills` guidance exactly** | Need to know which skill owns which template |
| Skills are fully self-contained | |
| No separate directory to get out of sync | |
| Agent reads one skill → has everything it needs | |
| Template updates happen where the skill is maintained | |

---

## Why Option C Is Right

### 1. The framework's own rules say so

From [asdlc-writing-skills SKILL.md lines 113-122](file:///Users/salauddin/Projects/learning/sdd/agentic-sdlc/src/agentic_sdlc/skills/asdlc-writing-skills/SKILL.md#L113-L122):

```
.agents/skills/
  skill-name/
    SKILL.md              # Required — main skill file
    supporting-file.*     # Only if needed (templates, scripts, heavy reference)
```

> "Keep inline if it fits. Separate files only for: >100 lines of reference material, reusable scripts, or **templates that users fill in**."

Templates are explicitly mentioned as supporting files that belong inside skill directories.

### 2. Every template has exactly ONE owning skill

| Template | Lines | Owning Skill | Shared? |
|---|---|---|---|
| `brd-template.md` | 67 | `asdlc-inception` | No |
| `design-system-template.md` | 109 | `asdlc-design-system` | No |
| `adr-template.md` | 39 | `asdlc-tech-architecture` | No |
| `workspace-template.md` | 72 | `asdlc-implementation` | No |
| `story-template.md` | 45 | `asdlc-story-breakdown` | No |
| `task-graph-template.md` | 14 | `asdlc-story-breakdown` | No |
| `implementation-plan-template.md` | 18 | `asdlc-implementation-planning` | No |
| `test-plan-template.md` | 16 | `asdlc-testing` | No |
| `retrospective-template.md` | 13 | `asdlc-retrospective` | No |
| `mockups-template.md` | 30 | `asdlc-ui-mockups` | No |

**No template is shared across skills.** Every template belongs to exactly one skill. There's zero reason to centralize them.

### 3. Most skills already have the format INLINE — the template files are richer copies

This is a **duplication problem**:

| Skill | Has inline format? | Template file adds... |
|---|---|---|
| `asdlc-inception` | ✅ BRD format at lines 48-81 | Richer: adds `How measured` column, examples, explicit guidance notes |
| `asdlc-design-system` | ✅ Design tokens at lines 44-75 | Richer: adds breakpoints, more token rows, component variants |
| `asdlc-tech-architecture` | ✅ ADR format at lines 33-54 | Same — minimal difference |
| `asdlc-implementation` | ✅ Workspace format in steps | Richer: adds YAML frontmatter for dashboard, git tracking, tasks checklist |
| `asdlc-story-breakdown` | ✅ Story format at lines 50-73 | Richer: adds YAML frontmatter with track, depends_on, priority |
| `asdlc-testing` | ✅ Test plan at lines 27-65 | Minimal — nearly identical |
| `asdlc-retrospective` | ✅ Retro format at lines 28-64 | Minimal — nearly identical |
| `asdlc-implementation-planning` | ✅ Plan format at lines 30-67 | Minimal — nearly identical |

> [!WARNING]
> **The template files are often RICHER than the inline formats in the skills.** The BRD template has a `How measured` column and examples. The story template has YAML frontmatter for tracking. If the agent follows the inline format, it produces a simpler document than the template file. This drift is a bug.

---

## Proposed Change

### What to do:

1. **Move each template into its owning skill directory** as a supporting file
2. **Update each skill's SKILL.md** to reference the template as a local file:
   ```
   Copy `brd-template.md` (in this skill's directory) to `docs/product/features/brd.md`
   ```
3. **Remove the root `templates/` directory** from `asdlc init`
4. **Reconcile inline formats vs template files** — pick ONE source of truth per skill:
   - Option: keep the inline format SHORT (structure only) and point to the template for the full version
   - Or: remove inline formats entirely and tell agents to read the template file
5. **Update `consistency.py`** to check templates inside `.agents/skills/` instead of root `templates/`
6. **Update `cli.py`** to stop copying templates separately (they come with the skills copy)

### What this eliminates:

- ~~Root `templates/` directory~~ → gone
- ~~Separate template copy step in CLI~~ → templates ship with skills automatically
- ~~Template ↔ skill drift~~ → one location, one owner
- ~~Agent confusion~~ → skill says "use the template in this directory"

---

## Impact on the CLI

**Before:**
```python
# cli.py does THREE separate copies:
shutil.copytree(package_root / "skills", target_path / ".agents" / "skills")  # 1
shutil.copytree(package_root / "templates", target_path / "templates")         # 2
for core_file in (package_root / "core").glob("*.md"): ...                     # 3
```

**After:**
```python
# cli.py does TWO copies:
shutil.copytree(package_root / "skills", target_path / ".agents" / "skills")  # 1 (includes templates!)
shutil.copy(package_root / "core" / "AGENTS.md", target_path / "AGENTS.md")   # 2 (only AGENTS.md)
```

---

## Summary of All `asdlc init` Changes

| # | Change | Rationale |
|---|---|---|
| 1 | **Move templates into skill directories** in source | Follows `asdlc-writing-skills` spec |
| 2 | **Remove `templates/` copy** from CLI init | Templates ship with skills |
| 3 | **Only copy `AGENTS.md`**, not platform files | Platform files are framework docs |
| 4 | **Remove platform links** from AGENTS.md template | Broken links after removing platform files |
| 5 | **Add AGENTS.md Phase 2 update** to tech-architecture skill | AGENTS.md should grow with the project |
| 6 | **Update consistency.py** to check templates inside skills | New template location |
| 7 | **Reconcile inline formats vs template files** | Eliminate duplication/drift |

Shall I create the implementation plan to execute these changes?
