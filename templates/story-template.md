---
story_id: STORY-NNN
status: TO_DO
# status options: TO_DO | IN_PROGRESS | BLOCKED | DONE | ARCHIVED
epic_id: EPIC-000
milestone: M1
track: A
depends_on: []
owner: ""
branch: ""
priority: medium
# priority: critical | high | medium | low
blocked_reason: ""
---

# STORY-NNN: [Title]

## Acceptance Criteria

- Given [the user/system is in a specific state]
- When [a specific action is taken]
- Then [the expected outcome occurs]

## Tasks

- [ ] Write failing test(s) — confirm RED
- [ ] Implement minimal code to make tests pass — confirm GREEN
- [ ] Refactor — apply `docs/architecture/coding-standards.md`
- [ ] Run full test suite — confirm no regression
- [ ] Update `docs/architecture/data-domain.md` if any contract changed (triggers HITL)

## Files Owned

`src/path/to/file.ts`, `src/path/to/file.test.ts`

## Merge Strategy

Feature branch `feature/STORY-NNN-short-description`, squash merge to main

## HITL Before Starting

No / Yes — [reason if Yes]
