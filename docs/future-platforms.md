# Future Platforms & Integrations

## Cursor

**Entry point:** `.cursor-plugin/plugin.json`

Cursor supports plugins with a `plugin.json` manifest. Rules can be injected via `asdlc-rules` or `asdlc-context` fields.

**Plugin manifest:** `.cursor-plugin/plugin.json`

```json
{
  "name": "agentic-sdlc",
  "version": "1.0.0",
  "rules": [
    "Before any action, check if a skill in .agents/skills/ applies. Read the SKILL.md and follow it."
  ],
  "context": [".agents/skills/**/*.md"]
}
```

---

## Multi-Framework Composability (Roadmap)

### The Problem

Multiple agentic skill frameworks now exist (Agentic SDLC, [Superpowers](https://github.com/obra/superpowers), and others). Each hijacks the agent via `AGENTS.md` / `CLAUDE.md` with a prime directive: *"Check MY skills before any action."*

If a user installs both Superpowers and Agentic SDLC, the agent receives **two competing handbooks**:

- Both claim ownership of the agent's bootstrap sequence
- Both provide skills for overlapping stages (planning, code review, testing)
- The agent has no mechanism to resolve which skill takes precedence
- Result: confused agent, contradictory instructions, broken workflow

Even when folder names don't collide (e.g., Superpowers has `brainstorming/`, Agentic SDLC has `inception/`), the **triggers** still conflict — both say *"when the user wants to plan → use my skill."*

### Proposed Solution: Layered Namespace System

#### Level 1 — Skill Prefixing

Each framework prefixes its skills so they are unambiguous:

```
skills/
  asdlc--inception/SKILL.md
  asdlc--implementation/SKILL.md
  asdlc--code-review/SKILL.md
  sp--brainstorming/SKILL.md
  sp--test-driven-development/SKILL.md
  sp--systematic-debugging/SKILL.md
```

This solves naming collisions but does **not** resolve trigger conflicts.

#### Level 2 — Skill Manifest with Conflict Routing

A `skill-manifest.json` at the project root declares which framework owns each stage:

```json
{
  "frameworks": {
    "agentic-sdlc": { "prefix": "asdlc", "version": "1.0.0" },
    "superpowers": { "prefix": "sp", "version": "5.0.7" }
  },
  "routing": {
    "planning":     "asdlc",
    "execution":    "sp",
    "code-review":  "asdlc",
    "debugging":    "sp",
    "testing":      "asdlc",
    "session-start": "asdlc"
  },
  "conflicts": [
    {
      "stage": "code-review",
      "skills": { "asdlc": "code-review", "sp": "requesting-code-review" },
      "winner": "asdlc",
      "reason": "ASDLC includes critical-review stage that SP lacks"
    }
  ]
}
```

The agent reads this manifest **first** and knows: *"For planning, use Agentic SDLC skills. For debugging, use Superpowers skills."*

#### Level 3 — Skill Dependency Declarations

Each SKILL.md declares what it **provides**, what it **conflicts with**, and what it **depends on** via extended YAML frontmatter:

```yaml
---
name: inception
namespace: agentic-sdlc
provides: [requirements, design-spec]
conflicts-with: [sp/brainstorming]
depends-on: []
outputs: [docs/product/features/brd.md]
---
```

```yaml
---
name: brainstorming
namespace: superpowers
provides: [requirements, design-spec]
conflicts-with: [asdlc/inception]
depends-on: []
outputs: [design-doc.md]
---
```

The resolver sees both provide `asdlc-requirements` → checks `skill-manifest.json` for the winner → only activates one.

#### Level 4 — Complementary Skill Routing

Many skills **don't conflict** — they fill gaps in the other framework. For example:

- Superpowers' `asdlc-systematic-debugging` covers a stage Agentic SDLC doesn't address
- Agentic SDLC's `asdlc-stage-gates` adds governance Superpowers doesn't have

A smart resolver would:

1. For **conflicting** capabilities → pick one based on manifest routing rules
2. For **complementary** capabilities → activate both
3. If no manifest exists → fall back to `AGENTS.md` priority order

```
Resolver logic:
  1. Read skill-manifest.json (if present)
  2. For each task, find applicable skills from ALL installed frameworks
  3. If multiple skills provide the same capability → use routing rules
  4. If a skill provides a unique capability → always activate it
  5. If no manifest → honor AGENTS.md load order (last writer wins)
```

### Implementation Roadmap

| Component | Effort | Description |
|---|---|---|
| YAML frontmatter extension | Small | Add `asdlc-namespace`, `asdlc-provides`, `asdlc-conflicts-with` fields to SKILL.md schema |
| `skill-manifest.json` spec | Small | Define the routing/override JSON format |
| `asdlc resolve-skills` CLI | Medium | Reads all installed skills, detects conflicts, generates manifest |
| Bootstrap skill update | Medium | `asdlc-using-agentic-sdlc` reads manifest before dispatching to skills |
| Dashboard integration | Small | Show active vs overridden skills in `asdlc serve` |
| Validator extension | Small | `asdlc-dev validate-skills` checks for unresolved conflicts |

### Strategic Value

This makes Agentic SDLC the **first composable** agentic skill framework:

> *"Use our governance and brownfield workflow alongside Superpowers' execution engine. We handle the conflicts."*

Instead of forcing users to pick one or the other, the positioning becomes: **Agentic SDLC plays well with others.**

---

## Implementation Notes (for contributors)

When adding a new platform:
1. Create the platform entry point file (`CLAUDE.md`, `GEMINI.md`, etc.)
2. Create the platform plugin manifest if applicable
3. Map tool names from Claude Code equivalents
4. Update `README.md` installation section
5. Test by running the `asdlc-using-agentic-sdlc` skill on the new platform
6. Document any behavioral differences in this file

---

*See [README.md](../README.md) for full installation instructions.*
