# Implementation Plan: [Name]

> **Epic ID:** [E-NNN]
> **Date:** YYYY-MM-DD
> **Status:** Draft | Ready for HITL | Approved
> **Version:** 0.1.0
>
> **Merge-strategy HITL (asked early, before story-breakdown):**
> **merge_strategy_hitl_prompt:** [Exact merge-strategy HITL prompt or artifact-local reference]
> **merge_strategy_hitl_response:** [Exact user response after HITL, blank before response]
> **merge_strategy_hitl_decision:** [approved | changes_requested | rejected, blank before response]
> **merge_strategy_hitl_approved_by:** [user/person, blank before response]
> **merge_strategy_hitl_approved_at:** [timestamp/date, blank before response]
>
> **Plan approval HITL (final stage gate):**
> **plan_approval_hitl_prompt:** [Exact plan-approval HITL prompt or artifact-local reference]
> **plan_approval_hitl_response:** [Exact user response after HITL, blank before response]
> **plan_approval_hitl_decision:** [approved | changes_requested | rejected, blank before response]
> **plan_approval_hitl_approved_by:** [user/person, blank before response]
> **plan_approval_hitl_approved_at:** [timestamp/date, blank before response]

## User Review Required

> [!IMPORTANT]
> [Critical decisions or breaking changes requiring human sign-off]

## Merge Strategy

> **Selected strategy:** Epic branch | Direct to main | PR-based
> **Recorded in:** `docs/architecture/coding-standards.md#merge-strategy`

- [ ] HITL merge strategy decision completed
- [ ] `docs/architecture/coding-standards.md` updated with the decision
- [ ] Branch targets are clear before story-breakdown begins

## Milestones

| Milestone | Exit Criteria |
|---|---|
| M1: [Name] | - [Criteria 1]<br>- [Criteria 2] |
| M2: [Name] | - [Criteria 1] |

## Risk Log

*Identify technical or delivery risks (at least 1, or 3+ per Scale Guide).*

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| [e.g., Third-party API rate limits] | High | High | Implement exponential backoff and caching |

## Proposed Changes

[Summary of technical approach]

### [Component A]

[File-level changes]

---

## Open Questions

- [ ] [Question 1]

## Verification Plan

### Automated Tests
- [ ] [Test command]

### Manual Verification
- [ ] [Manual step]

## Definition of Done

- [ ] All milestones completed
- [ ] [Project-specific DoD item]

---
*Written by: agentic-sdlc implementation-planning skill*
