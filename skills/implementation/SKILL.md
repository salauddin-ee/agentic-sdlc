---
name: implementation
description: Use when writing production code for any task in the task graph — enforces TDD, security non-negotiables, and coding constitution compliance per story.
---

Write production-quality code following TDD, the coding constitution, and the task graph. One task at a time. No exceptions to the TDD cycle.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.
```

Write code before the test? Delete it. Start over. No exceptions:
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Delete means delete

## Per-Task Loop

For each task in `/.agentic-sdlc/task-graph.md`:

```
1. Load task from task-graph.md — read full story text, acceptance criteria, files owned
2. Read any relevant skill (language/platform-specific if available)
3. Write failing test(s) — unit first, integration if needed
4. Run tests — confirm RED (test fails for the right reason)
5. Write minimal implementation to pass tests — NOTHING more
6. Run tests — confirm GREEN (test passes, no regressions)
7. Refactor — apply coding-constitution.md, clean code principles
8. Run full test suite — confirm no regression across all tests
9. Mark task complete in task-graph.md
10. If any interface contract changed: update interface-contracts.md → triggers HITL
```

## Test Pyramid Targets

Adjust per project NFRs, but defaults:

| Layer | Target | Characteristics |
|---|---|---|
| Unit | 70% of tests | Fast, isolated, no I/O, no external calls |
| Integration | 20% of tests | Real DB/service, no UI layer |
| E2E / acceptance | 10% of tests | Full stack, Given/When/Then from story |

## Security Non-Negotiables (check per story before marking complete)

```
[ ] Every authenticated endpoint verifies token/session before processing
[ ] Every user input is validated and sanitized at the boundary
[ ] No secrets in source code, logs, or error responses
[ ] All external calls have timeouts and error handling
[ ] SQL/NoSQL queries use parameterization — never string concatenation
[ ] Dependencies checked against known vulnerability database
```

## RED — Write Failing Test

Write one minimal test showing what should happen:

- Clear name describing the behavior (not the method)
- Tests the behavior, not the implementation
- Tests real code — mocks only when unavoidable (I/O, time, third-party APIs)
- One behavior per test — "and" in a test name → split it

Run the test. Confirm it **fails for the right reason** (feature missing, not a typo or import error).

**Test passes immediately?** You're testing existing behavior. Fix the test.
**Test throws an error?** Fix the error, re-run until it fails correctly.

## GREEN — Write Minimal Implementation

Write the simplest code that makes the test pass.

- Do not add features the test doesn't require
- Do not refactor other code
- Do not "improve" beyond what the test demands

## REFACTOR — Clean Code

Only after GREEN:
- Remove duplication
- Improve naming for clarity
- Extract helpers where complexity grows
- Apply coding-constitution.md standards

Keep all tests green throughout. Do not add new behavior.

## Rollback Rule

If implementation reveals a Stage 3 architectural decision was wrong:

1. **Stop immediately** — do not work around it
2. Write a superseding ADR in `/.agentic-sdlc/adr/` documenting the conflict
3. Trigger HITL (read `skills/hitl-protocol/SKILL.md`)
4. Update `/.agentic-sdlc/tech-architecture.md`
5. Only resume implementation after HITL approval

## Common Rationalizations — STOP

| Thought | Reality |
|---|---|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll write tests after to verify it works" | Tests-after pass immediately and prove nothing. |
| "I already manually tested it" | Manual testing has no record, can't re-run, misses edge cases. |
| "Deleting X hours of work is wasteful" | Sunk cost fallacy. Keeping untested code is tech debt. |
| "TDD will slow me down" | TDD is faster than debugging in production. |
| "This is different because..." | If you're rationalizing, you're violating. Delete. Start over. |
| "I'll keep it as reference" | You'll adapt it. That's tests-after. Delete means delete. |

## Completing a Task

Before marking a task complete in task-graph.md:

```
[ ] Every new function/method has a test that was written first and watched fail
[ ] All tests pass (unit + integration + E2E relevant to this story)
[ ] Security non-negotiables checked
[ ] Coding constitution followed (naming, error handling, logging)
[ ] No TODO comments left in production code
[ ] interface-contracts.md updated if any contract changed
```

## Transition

After all tasks in a story are complete:
→ Invoke `critical-review` skill before committing the story to the main branch.
