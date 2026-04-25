---
name: asdlc-troubleshooting
description: Use when the agent is stuck during implementation — a test won't pass after multiple attempts, a build fails with unclear errors, dependencies conflict, or execution is blocked and the path forward is not clear.
version: 1.0.0
---

Stop thrashing. Diagnose before retrying. A structured diagnosis in 5 minutes beats 10 failed retry attempts.

<HARD-GATE>
Do NOT continue retrying the same approach more than 3 times without first running this troubleshooting protocol. Repeated failed attempts without diagnosis are a process violation.
</HARD-GATE>

## When to Use

- A test has been failing for more than 3 attempts and the root cause is unclear
- A build error is not obviously caused by your last change
- A dependency conflict blocks installation or compilation
- The implementation doesn't match the expected behavior and you're not sure why
- You are about to make a large, speculative change to "try something"
- Context window pressure is causing you to lose track of what you've tried

---

## The Troubleshooting Protocol

Run through these steps in order. Stop when you find the root cause.

### Step 1 — Stop and Document

Before doing anything else, write down:
```
STUCK LOG — [timestamp]
Story: [STORY-ID]
What I was trying to do: [one sentence]
What happened instead: [exact error message or behavior]
What I tried so far: [list of approaches, max 5]
Number of attempts: [N]
```

This prevents re-trying approaches you've already ruled out.

### Step 2 — Re-read the Acceptance Criteria

Read `docs/sdlc/stories/STORY-[ID].md` from scratch.

Ask:
- Am I actually solving what the acceptance criteria say?
- Is the test testing the right behavior, or did I write the test wrong?
- Did I misread a Given/When/Then clause?

**Test passes immediately?** You may be testing existing behavior — re-read the story and fix the test scope.
**Test fails for the wrong reason?** Fix the test setup, not the implementation.

### Step 3 — Check the Interface Contracts

Read `docs/architecture/data-domain.md`.

Ask:
- Is my implementation using the correct request/response shape?
- Did I assume a field name or type that isn't actually in the contract?
- Has the contract changed but the test hasn't been updated?

### Step 4 — Isolate the Failure

Narrow the problem to its smallest reproducible form:

```
[ ] Can I reproduce the failure in a single unit test? (if not: it's an integration/setup issue)
[ ] Does the failure disappear if I revert my last change? (if yes: my last change is the culprit)
[ ] Does the failure exist on a clean checkout? (if yes: it's a pre-existing issue — document and don't fix)
[ ] Does the failure happen with a minimal input? (reduce test data to the smallest case that still fails)
```

### Step 5 — Search for the Error

Search the internet for the exact error message, including:
- The error text (remove project-specific paths/names first)
- The library name and version
- The runtime/framework version

Look specifically for:
- Known bugs in this version
- Version incompatibilities
- Configuration requirements not in the default setup
- Community workarounds

Document what you found in the Stuck Log.

### Step 6 — Check Dependencies

```bash
# Node.js
npm ls [package-name]        # check installed version vs. expected
npm audit                    # check for vulnerabilities affecting this area
node --version               # check runtime version

# Python
pip show [package-name]
python --version

# Check lock file consistency
# (npm: package-lock.json vs package.json, pip: requirements.txt vs installed)
```

If a version mismatch is found: pin to a known-good version and document the decision.

### Step 7 — Escalate to HITL

If Steps 1-6 don't resolve the issue, invoke `asdlc-hitl-protocol` skill with:

```
HITL REQUIRED
Stage: implementation
Story: [STORY-ID]
Question: I am stuck after [N] attempts. I need human guidance to proceed.
Context: [Paste the Stuck Log from Step 1]
What I've tried: [List from Stuck Log]
Best current hypothesis: [Your best guess at root cause]
Options: [A] Try approach X — [describe]
         [B] Try approach Y — [describe]
         [C] Descope this part of the story and create a new story for it
Default if no response: Wait for explicit guidance
```

---

## Common Failure Patterns

| Symptom | Likely Cause | First Check |
|---|---|---|
| Test fails immediately with import error | Missing dependency or wrong import path | Check package.json / requirements.txt |
| Test fails with "expected X, got undefined" | Wrong field name or async timing issue | Log the actual object shape |
| Test was passing, now failing after unrelated change | Global state leak between tests | Add test isolation (beforeEach reset) |
| Build fails with peer dependency conflict | Package version mismatch | Run `npm ls` / check lock file |
| "Cannot find module" in test but not in app | Different module resolution (test vs runtime) | Check test framework config |
| Test times out | External call not mocked, or real async not awaited | Mock the external call; verify await |
| Works locally, fails in CI | Environment variable missing in CI | Check CI environment config |
| Implementation matches contract but test still fails | Test is asserting wrong thing | Re-read the acceptance criteria |

---

## Gate (for HITL escalation)

Before invoking HITL:

```
[ ] Stuck Log written with exact error, what I tried, number of attempts
[ ] Acceptance criteria re-read from scratch — confirmed I'm solving the right thing
[ ] Interface contracts checked — my implementation matches data-domain.md
[ ] Failure isolated to smallest reproducible case
[ ] Web search completed for the exact error message
[ ] Dependencies checked for version mismatches
[ ] At least 2 options proposed for the human to choose from
```

---

## Red Flags

| Thought | Reality |
|---|---|
| "Let me just try one more thing" | If you've tried 3 times without diagnosis, the next attempt won't work either. Stop and diagnose. |
| "The error message is clear — I don't need to search" | Many "clear" error messages have non-obvious root causes. Search anyway. |
| "I'll work around it with a try/catch" | Swallowing errors hides root causes. Never suppress to make a test pass. |
| "I'll rewrite the whole thing fresh" | Rewrites without diagnosis reproduce the same bug. Diagnose first. |
| "HITL will slow me down" | 10 failed retries are slower than 1 HITL checkpoint. |
| "The test was probably wrong" | Don't assume the test is wrong. Re-read the acceptance criteria first. |
| "I remember what the error was" | Write it down. The Stuck Log exists because memory under pressure is unreliable. |
