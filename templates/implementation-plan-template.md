# Implementation Plan

> **Project:** [Project name]
> **Date:** YYYY-MM-DD

## Milestones

| ID | Name | Description | Exit criteria | Depends on |
|---|---|---|---|---|
| M1 | [e.g., Foundation] | [e.g., Project scaffold, CI, auth] | [e.g., All tests green, staging deploy] | — |
| M2 | [e.g., Core features] | [e.g., FR-001 through FR-005] | [e.g., Acceptance tests pass] | M1 |
| M3 | [e.g., Polish & NFRs] | [e.g., Performance, accessibility] | [e.g., NFR targets met] | M2 |

## Interface contracts summary

> Full contracts in `/.agentic-sdlc/interface-contracts.md`

Key module boundaries:

| From | To | Contract type | Notes |
|---|---|---|---|
| [Frontend] | [API] | REST | Endpoints defined in interface-contracts.md |
| [API] | [Database] | ORM | Schema defined in migrations |
| [Service A] | [Service B] | Event | Schemas in interface-contracts.md |

*All contracts must be locked before story-breakdown begins. No contract may be defined during implementation.*

## Risk log

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| [e.g., Third-party API rate limits] | M | H | [e.g., Mock in tests; retry with backoff] |
| [e.g., Performance targets missed] | L | H | [e.g., Load test at M2 gate] |
| [e.g., Key person unavailable] | L | M | [e.g., Document all decisions in ADRs] |

*(H = High, M = Medium, L = Low)*

## Assumptions

*If any assumption below is wrong, trigger HITL before continuing.*

- [Assumption 1]
- [Assumption 2]
- [Assumption 3]

## Definition of done (project level)

- [ ] All FRs implemented and verified with passing tests
- [ ] All NFRs verified with evidence (benchmarks, audit reports, screenshots)
- [ ] Test pyramid targets met (see coding-constitution.md)
- [ ] Security checklist passed (dependency audit, auth review, input validation)
- [ ] Documentation complete (README, API docs, ADRs, CHANGELOG)
- [ ] No P0/P1 open bugs (all P2 logged in retrospective.md)
- [ ] Deployed to production (or staging if production deploy is out of scope)

---
*Written by: agentic-sdlc implementation-planning skill*
*Next stage: story-breakdown*
