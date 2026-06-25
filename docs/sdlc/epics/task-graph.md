# Task graph — production-readiness closure

> **Epic ID:** PRC-2026-06-25
> **Status:** APPROVED
> **Last verified:** 2026-06-25T02:43:03Z

## Canonical objective
Stabilize and close `agentic-sdlc` for production readiness using the plan in `docs/future/production-readiness-closure-plan.md`.

## Stories

| Story ID | Title | Status | Dependencies | Evidence |
|---|---|---|---|---|
| PRC-001 | Audit repo truth and installed CLI state | APPROVED | none | `git status --short --branch`; CLI smoke evidence in test plan |
| PRC-002 | Fix installed CLI entrypoints | APPROVED | PRC-001 | `pipx uninstall agentic-sdlc`; `pipx install -e ".[dev]"`; `asdlc --help`; `asdlc-dev --help` |
| PRC-003 | Create closure documentation | APPROVED | PRC-001 | `docs/architecture/coding-standards.md`, this task graph, `docs/sdlc/test-plans/test-plan.md`, `docs/sdlc/retrospectives/critical-review.md`, `docs/sdlc/retrospectives/retrospective.md` |
| PRC-004 | Reconcile historical review blockers | APPROVED | PRC-002, PRC-003 | Final critical review PASS and final code review APPROVED supersede stale CHANGES REQUIRED notes |
| PRC-005 | Run fresh verification and dependency audit | APPROVED | PRC-002, PRC-003 | `pytest -q`, `asdlc-dev validate-skills .`, `asdlc-dev eval-skills .`, CLI help, `pipx run pip-audit . --progress-spinner off` all exited 0 |
| PRC-006 | Clean generated artifacts and commit closure | APPROVED | PRC-005 | Git cleanup and final commit; final status verified clean after commit |

## Acceptance criteria and verification mapping

| Acceptance criterion | Story | Verification |
|---|---|---|
| `pytest -q` passes | PRC-005 | Exit 0 at 2026-06-25T02:43:03Z; `9 passed in 0.15s` |
| `asdlc-dev validate-skills .` passes | PRC-005 | Exit 0 at 2026-06-25T02:43:03Z; `PASS (308 checks, 0 errors, 0 warnings)` |
| `asdlc-dev eval-skills .` passes | PRC-005 | Exit 0 at 2026-06-25T02:43:03Z; `PASS (18 scenarios, 18 passed, 0 failed)` |
| `asdlc --help` works without `PYTHONPATH` | PRC-002 | Exit 0 at 2026-06-25T02:43:03Z; installed entrypoint prints public CLI commands |
| `asdlc-dev --help` works without `PYTHONPATH` | PRC-002 | Exit 0 at 2026-06-25T02:43:03Z; installed entrypoint prints developer commands |
| Dependency audit passes or accepted risk documented | PRC-005 | Exit 0 at 2026-06-25T02:43:03Z; `No known vulnerabilities found` |
| Closure docs exist and match evidence | PRC-003 | Required docs are present and reference the same verification commands/results |
| Final code review verdict is APPROVED | PRC-004 | `docs/sdlc/retrospectives/code-review-production-readiness-2026-06-25.md` |
| Git status is clean | PRC-006 | Verified after final commit before final report |

## Status reconciliation
- Historical code reviews dated 2026-04-11 and 2026-04-13 remain in the repository as stale historical records with `CHANGES REQUIRED` verdicts.
- Their blockers were: missing `coding-standards.md`, unavailable dependency audit, and unavailable pytest environment.
- Current closure artifacts supersede those blockers with fresh passing evidence recorded in the test plan, critical review, final code review, and retrospective.
- No artifact in this closure may claim READY if any required check later fails.
