# Tech plan — SKILL-EVALS: Skill Evaluation Harness — 2026-04-11

> **Status:** Draft
> **Version:** 0.1.0

## Approach summary
Add a small, file-based evaluation system for Agentic SDLC skills that first catches repository drift and malformed skill metadata, then grows into scenario-based regression coverage for the highest-risk skills. The implementation should extend the existing Click CLI and markdown-driven project structure rather than introducing a separate service, database, or benchmark platform.

## DRY check
Existing code already provides the right foundations for a minimal solution:

- Reuse the Click CLI in `src/agentic_sdlc/cli.py` for `asdlc-dev validate-skills` and `asdlc-dev eval-skills`.
- Reuse the existing `src/agentic_sdlc/skills/` directory as the source of truth for static validation.
- Reuse repo documentation and generated artifact paths as the comparison targets for consistency checks.
- Introduce only a small evaluator module plus fixtures instead of inventing a generalized scoring platform.

## Files to change
| File | Change type | Description |
|---|---|---|
| `src/agentic_sdlc/cli.py` | Modify | Add CLI entry points for validation and eval execution |
| `pyproject.toml` | Modify | Add any required test dependency and test configuration for the new eval modules |
| `README.md` | Modify | Document local usage of validation and eval commands |
| `docs/getting-started.md` | Modify | Add contributor workflow guidance for running the new checks |
| `docs/architecture/existing-system.md` | Reference only | Baseline repo constraints and risks |

## New files required
| File | Purpose |
|---|---|
| `src/agentic_sdlc/eval/__init__.py` | Package for eval-related logic |
| `src/agentic_sdlc/eval/validator.py` | Static and cross-file validation rules |
| `src/agentic_sdlc/eval/harness.py` | Scenario loading and pass/fail execution |
| `src/agentic_sdlc/eval/models.py` | Shared dataclasses or typed structures for results and fixtures |
| `tests/test_skill_validator.py` | Unit coverage for validation behavior |
| `tests/test_skill_eval_harness.py` | Unit coverage for scenario harness behavior |
| `src/agentic_sdlc/fixtures/<skill-name>/*.yaml` | Scenario fixtures for targeted skills |

## Interface contract changes
New local CLI surface only:

- `asdlc-dev validate-skills`
- `asdlc-dev eval-skills`
- optional follow-up: `asdlc-dev eval-skills --skill <name>`

No external API, packaging, or generated-project contract changes are required for the first implementation.

## Regression risk assessment
```
[x] Which existing tests could break? None currently committed; new tests will establish baseline coverage.
[x] Which integration points does this change touch? Local CLI behavior, repository file layout, packaged skill/docs consistency.
[x] Is a feature flag needed to deploy safely? No; this is additive developer tooling.
[x] Are there DB migrations? Are they reversible? No database is involved.
```

## Feature flag
Not needed. The work is additive and can be safely shipped behind new non-default CLI commands.

## Definition of done (story technical)
- [ ] `asdlc-dev validate-skills` reports malformed frontmatter, placeholder content, and path/reference drift
- [ ] `asdlc-dev eval-skills` runs a small scenario suite with deterministic pass/fail output
- [ ] Initial fixtures cover `using-agentic-sdlc`, `implementation`, `stage-gates`, `hitl-protocol`, and `git-discipline`
- [ ] Automated tests cover validator rules and harness behavior
- [ ] CLI help text and docs explain how to run the checks locally
- [ ] No unrelated architecture or workflow changes are introduced
