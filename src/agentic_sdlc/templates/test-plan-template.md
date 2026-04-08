# Test Plan

> **Project:** [Project name]
> **Cycle:** [Milestone / Story range]
> **Date:** YYYY-MM-DD

## Scope

[What is covered in this test cycle — which stories, which milestone, which features.]

## Environment

| Item | Details |
|---|---|
| Environment | Staging / Local |
| Test data | [How is it seeded? Fixtures, factory, manual?] |
| External services | [Real / Mocked — and for which ones] |
| Test runner | [Vitest / Jest / Pytest / etc.] |

## Automated test cases

| ID | Story | Type | Scenario | Pass/Fail |
|---|---|---|---|---|
| TC-001 | STORY-001 | Unit | [Given user exists, when getUser is called with valid ID, then returns user object] | |
| TC-002 | STORY-001 | Integration | [When POST /api/users with valid payload, then 201 and user returned] | |
| TC-003 | STORY-002 | E2E | [Given on login page, when submitting valid credentials, then redirects to dashboard] | |

## Regression scope

| Test file / suite | Coverage concern |
|---|---|
| `src/auth/*.test.ts` | Auth flows must not regress |
| `src/payments/*.test.ts` | Payment processing must not regress |

## Performance targets

| Metric | NFR target | Actual result | Pass/Fail |
|---|---|---|---|
| P95 API latency | < 200ms | | |
| Throughput | 1000 req/s | | |
| Memory under load | < 512MB RSS | | |

## HITL test cases

| ID | Scenario | Question | Expected outcome | Result |
|---|---|---|---|---|
| HTC-001 | Password reset email | Did you receive the reset email within 60 seconds? | Yes, received within 60s | |
| HTC-002 | OAuth login flow | Did the Google OAuth flow complete successfully? | Redirected to dashboard | |

## Results summary

> Fill in after test run

- **Total automated tests:** [N]
- **Passing:** [N]
- **Failing:** [N] — [list failing tests with IDs]
- **Test pyramid:**
  - Unit: [N]% (target: 70%)
  - Integration: [N]% (target: 20%)
  - E2E: [N]% (target: 10%)
- **Performance targets:** Pass / Fail (details above)
- **HITL test cases resolved:** [N/N]

## Outstanding items

[Any test cases that did not run, or require follow-up]

---
*Written by: agentic-sdlc testing skill*
*Next stage: code-review*
