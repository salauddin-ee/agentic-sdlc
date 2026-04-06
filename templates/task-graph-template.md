# Task Graph

> **Project:** [Project name]
> **Date:** YYYY-MM-DD

## Stories

---

### STORY-001: [Title]

**Milestone:** M1
**Track:** A
**Depends on:** —

**Acceptance criteria:**
- Given [context]
- When [action]
- Then [outcome]

**Tasks:**
- [ ] Write failing test(s)
- [ ] Implement to make tests pass
- [ ] Refactor
- [ ] Update interface-contracts.md if any contract changed

**Files owned:** `src/...`
**Merge strategy:** Feature branch, squash merge to main
**HITL before starting:** No

---

### STORY-002: [Title]

**Milestone:** M1
**Track:** B (parallel with STORY-003)
**Depends on:** STORY-001

**Acceptance criteria:**
- Given [context]
- When [action]
- Then [outcome]

**Tasks:**
- [ ] Write failing test(s)
- [ ] Implement to make tests pass
- [ ] Refactor

**Files owned:** `src/...`
**Merge strategy:** Feature branch, squash merge to main
**HITL before starting:** No

---

*[Add all stories here]*

---

## Dependency graph

```
STORY-001 (Foundation)
  ├── STORY-002 (Module A)    ← depends on STORY-001
  └── STORY-003 (Module B)    ← depends on STORY-001
        └── STORY-004 (Integration) ← merge point: depends on STORY-002 + STORY-003
```

## Parallel tracks

| Track | Stories | Files owned | Merge strategy |
|---|---|---|---|
| A | STORY-002 | `src/module-a/` | Feature branch per story |
| B | STORY-003 | `src/module-b/` | Feature branch per story |
| Merge | STORY-004 | `src/integration/` | Feature branch, merge after A + B |

## HITL tasks

| Story | Reason | When |
|---|---|---|
| [STORY-NNN] | [e.g., DB migration — destructive] | Before story starts |

---
*Written by: agentic-sdlc story-breakdown skill*
*Next stage: implementation*
