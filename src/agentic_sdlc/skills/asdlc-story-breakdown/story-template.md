---
story_id: STORY-NNN
status: TO_DO
# status options: TO_DO | IN_PROGRESS | BLOCKED | DONE | ARCHIVED
epic_id: EPIC-000
milestone: M1
track: A
depends_on: []
owner: ""
branch: feature/STORY-NNN-short-description
priority: medium
# priority: critical | high | medium | low
complexity: medium
# complexity: low | medium | high — risk signal for decomposition/HITL, NOT time estimation
risk: low
# risk: low | medium | high — impact on critical path; distinct from complexity
hitl_required: false
# hitl_required: true | false — does this story need human approval before/during execution?
files_touched: []
# files_touched: list of files this story modifies — used to detect conflicts between parallel stories
blocked_reason: ""
---

# Story: [Name]

> **Story ID:** [S-NNN]
> **Date:** YYYY-MM-DD
> **Status:** Draft | In Progress | Approved
> **Version:** 0.1.0

## Description

[User story format: As a... I want to... so that...]

## Acceptance Criteria

- [ ] [AC-1]
- [ ] [AC-2]

## Implementation Notes

> **Git operations**: Follow `asdlc-git-discipline` skill for all branching, commits, and merges. Do not run git commands outside that protocol.

- [ ] Create feature branch per `asdlc-git-discipline` → Story Implementation Protocol
- [ ] Write failing test(s) — confirm RED
- [ ] Implement minimal code to make tests pass — confirm GREEN
- [ ] Refactor — apply `docs/architecture/coding-standards.md`
- [ ] Run full test suite — confirm no regression
- [ ] Update `docs/architecture/data-domain.md` if any contract changed (triggers HITL)
- [ ] Commit story per `asdlc-git-discipline` — only stage files listed in `files_touched` + test files
- [ ] After code-review PASS: squash merge to main, delete feature branch per `asdlc-git-discipline`

---
*Written by: agentic-sdlc story-breakdown skill*
