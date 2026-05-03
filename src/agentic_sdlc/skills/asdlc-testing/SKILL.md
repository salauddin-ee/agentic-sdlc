---
name: asdlc-testing
description: Use when executing the test plan and verifying the application works end-to-end after implementation and critical review are complete.
version: 1.0.0
---

Execute the test plan. Verify the application works end-to-end — including paths that were not directly implemented by the agent. All automated tests must be green before this stage completes.

<HARD-GATE>
Do NOT proceed to asdlc-code-review until all automated tests pass, test pyramid targets are met, and all HITL test cases are resolved. A single failing test is a blocker.
</HARD-GATE>

## Checklist

1. **Bootstrap test plan if absent** — check whether `docs/sdlc/test-plans/test-plan.md` exists.
   - If it **does not exist**: create it now from the `test-plan-template.md` in this skill's directory. Populate the header (project name, date, version) and derive initial test cases from `docs/product/features/brd.md` acceptance criteria and `docs/sdlc/epics/implementation-plan.md` definition of done. Set `Status: Draft`.
   - If it **exists**: read it in full before proceeding.
2. **Run full automated test suite** — every test, zero failures
3. **Verify test pyramid targets** — from `docs/architecture/coding-standards.md`
4. **Run HITL test cases** — scenarios the agent cannot verify alone
5. **Run load/performance tests** if NFRs specify targets
6. **Document results in `docs/sdlc/test-plans/test-plan.md`** — fill Results Summary, mark each test case Passed/Failed/Skipped
7. **Gate evaluation** — all criteria must pass before proceeding


## Running Tests

1. **Run the full suite first** — never run only the new tests
2. **Any failure = blocker** — fix before continuing, even if unrelated to current story
3. **Record actual vs. expected** for every failing test
4. **Do not modify existing tests to make them pass** — unless the behavior change is explicitly in scope
5. **Mandatory Evidence:** For every run, record the exact command, exit code, timestamp, and a summary output snippet.

## HITL Test Cases

For each scenario the agent cannot verify alone:

```
HITL REQUIRED
Stage: testing
Scenario: [HTC-ID] — [Scenario description]
Question: [Specific question for the human]
Context: [What to look for, where to look]
Expected outcome: [What "pass" looks like]
```

Wait for human response before marking the HITL test case resolved.

## Performance Testing

If NFRs specify latency, throughput, or load targets:
- Run load test against staging environment
- Record results in test-plan.md
- If targets are missed: document deviation and trigger HITL before proceeding

## Gate

```
[ ] docs/sdlc/test-plans/test-plan.md physically exists (created this stage if absent)
[ ] Test execution evidence provided in test-plan.md (command, exit code, timestamp, output snippet)
[ ] All automated tests passing — 0 failures, 0 errors
[ ] Test pyramid targets met (or deviation documented with justification)
[ ] All HITL test cases resolved with human sign-off
[ ] Performance targets met (or deviation accepted via HITL)
[ ] No P0 or P1 findings from critical-review remain open
[ ] test-plan.md Results Summary section updated with actual pass/fail counts
```

## Red Flags

| Thought | Reality |
|---|---|
| "Tests mostly pass — close enough" | Zero tolerance. One failure is a blocker. |
| "I'll skip the regression suite — only changed one file" | One file change can break unrelated behavior. Run everything. |
| "HITL test cases can be inferred" | HITL exists because the agent cannot verify it alone. Ask the human. |
| "Performance targets are aspirational" | NFRs are requirements. Missed targets need HITL sign-off, not silence. |
