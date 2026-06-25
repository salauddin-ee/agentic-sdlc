# Test plan — production-readiness closure

> **Project:** agentic-sdlc
> **Status:** PASS
> **Date:** 2026-06-25
> **Evidence timestamp:** 2026-06-25T02:43:03Z

## Scope
This test plan covers the production-readiness closure objective in `docs/future/production-readiness-closure-plan.md`.

## Results summary

| Category | Total | Passed | Failed | Skipped |
|---|---:|---:|---:|---:|
| Automated pytest suite | 1 | 1 | 0 | 0 |
| Skill validation | 1 | 1 | 0 | 0 |
| Skill scenario evals | 1 | 1 | 0 | 0 |
| Installed CLI smoke tests | 2 | 2 | 0 | 0 |
| Dependency audit | 1 | 1 | 0 | 0 |
| **Total** | **6** | **6** | **0** | **0** |

## Evidence table

| ID | Check | Command | Exit | Timestamp | Output summary |
|---|---|---|---:|---|---|
| TP-001 | Full automated test suite | `pytest -q` | 0 | 2026-06-25T02:43:03Z | `9 passed in 0.15s` |
| TP-002 | Static skill validation | `asdlc-dev validate-skills .` | 0 | 2026-06-25T02:43:03Z | `validate-skills: PASS (308 checks, 0 errors, 0 warnings)` |
| TP-003 | Deterministic skill evals | `asdlc-dev eval-skills .` | 0 | 2026-06-25T02:43:03Z | `eval-skills: PASS (18 scenarios, 18 passed, 0 failed)` |
| TP-004 | Public CLI smoke test | `asdlc --help` | 0 | 2026-06-25T02:43:03Z | Help printed `init`, `serve`, and `update-agents` commands |
| TP-005 | Developer CLI smoke test | `asdlc-dev --help` | 0 | 2026-06-25T02:43:03Z | Help printed `eval-skills`, `validate-skills`, and public commands |
| TP-006 | Dependency audit | `pipx run pip-audit . --progress-spinner off` | 0 | 2026-06-25T02:43:03Z | `No known vulnerabilities found` |

## Installed CLI remediation evidence
Initial installed entrypoints failed with `ModuleNotFoundError: No module named 'agentic_sdlc'` because the pipx entrypoints pointed at an environment that could not import the package. The fix was to reinstall the editable package from this repository:

```bash
pipx uninstall agentic-sdlc
pipx install -e ".[dev]"
```

Post-fix smoke tests TP-004 and TP-005 passed without setting `PYTHONPATH`.

## Test pyramid assessment
This repository is a CLI/library package. The current pyramid is appropriate for its surface:
- Unit/contract tests: pytest checks scaffold and CLI behavior.
- Integration smoke tests: installed `asdlc` and `asdlc-dev` entrypoints execute outside `PYTHONPATH`.
- Process evals: deterministic ASDLC skill fixtures validate process behavior.

## Manual / HITL checks
No manual product UI checks are required for this closure because the affected surfaces are CLI entrypoints, package metadata, skills, docs, and validation/eval tooling. The user explicitly requested autonomous end-to-end completion in goal mode.

## Gate result
PASS. All automated checks, installed CLI smoke tests, and the dependency audit exited 0. No skipped checks remain for the production-readiness definition of done.
