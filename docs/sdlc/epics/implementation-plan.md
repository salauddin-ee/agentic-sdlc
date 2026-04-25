# Implementation plan - skill eval tooling

> **Status:** Ready for approval
> **Version:** 0.2.0
> **Last updated:** 2026-04-25

## Planning inputs and approval gate

This is a brownfield internal-tooling plan. The normal BRD, tech architecture, and coding standards files are not present in this checkout, so this plan uses the available approved inputs instead:

- `docs/architecture/existing-system.md`
- `docs/architecture/data-domain.md`
- `docs/skill-testing-plan.md`
- `docs/sdlc/workspaces/tech-plan-skills-evals.md`
- current source under `src/agentic_sdlc/`

Approval gate:
- This plan is ready for user approval.
- Implementation work should not proceed until the user explicitly approves this plan or approves the documented deviation from missing BRD / tech-architecture / coding-standards files.

## Current repo baseline

The repository already contains substantial eval tooling:

- Eval package: `src/agentic_sdlc/eval/{models,validator,consistency,harness,utils}.py`
- Developer CLI: `asdlc-dev validate-skills` and `asdlc-dev eval-skills`
- Packaged fixtures: `src/agentic_sdlc/fixtures/<skill-name>/*.yaml`
- Dashboard surface: `asdlc serve` exposes an evals page backed by the same validator and harness modules
- README contributor docs for `asdlc-dev validate-skills` and `asdlc-dev eval-skills`

Known remaining gap:
- No committed `tests/` tree exists.
- `python3 -m pytest -q` cannot run in the current environment because `pytest` is not installed.

## Eval-driven skill improvement principle

Evals are not just a quality gate. They actively drive skill quality, mirroring the TDD discipline the framework enforces for production code:

```text
NO SKILL CHANGE WITHOUT A FAILING EVAL FIRST.
```

The correct order is always:

1. Write the eval asserting ideal behavior.
2. Run it and confirm the current skill fails when behavior is missing.
3. Fix the skill until the eval passes.
4. Keep the eval as a permanent regression guard.

A milestone is not complete until:

- its eval layer passes
- any skill weakness surfaced by that eval has been fixed in the skill text
- verification evidence is recorded

## Milestones

| ID | Name | Current state | Remaining exit criteria | Depends on |
|---|---|---|---|---|
| M1 | Eval foundation | Implemented: shared eval package, result models, and developer CLI command skeletons exist | `asdlc-dev validate-skills --help` and `asdlc-dev eval-skills --help` resolve in a fresh editable install | - |
| M2 | Static validation | Implemented: validator checks frontmatter, metadata, placeholders, sections, skill references, and consistency hooks | Add focused pytest coverage for validator rules; `asdlc-dev validate-skills .` exits `0` or reports only accepted known drift | M1 |
| M3 | Consistency checks | Implemented: path, template, CLI stub, and skill path drift checks exist | Add focused pytest coverage for consistency rules; fix or explicitly document all current drift findings | M2 |
| M4 | Scenario eval harness | Implemented: file-based fixture loading and rule-based assertions exist | Add focused pytest coverage for fixture loading and assertion behavior; `asdlc-dev eval-skills .` runs packaged fixtures with clear failure reasons | M1 |
| M5 | Initial skill suite | Implemented: packaged fixtures cover high-risk skills including bootstrap, implementation, stage gates, HITL, git discipline, and UI mockups | Verify at least two scenarios per targeted high-risk skill pass, or improve skill text until they pass | M4 |
| M6 | Documentation and dashboard rollout | Partially implemented: README and dashboard eval surface exist | Confirm docs match current CLI behavior; confirm dashboard eval page renders validator and scenario results from shared modules | M2, M3, M5 |
| M7 | Automated regression coverage and final verification | Not implemented: no committed tests tree | Add `tests/` coverage for validator, harness, CLI result behavior, and dashboard data collection; run final verification commands | M2, M3, M4, M6 |

## Design decision: CLI + dashboard dual surface

Eval results are exposed on two surfaces for different audiences:

| Surface | Command / route | Audience | Use case |
|---|---|---|---|
| CLI | `asdlc-dev validate-skills` / `asdlc-dev eval-skills` | CI pipelines, automation, agents | Non-zero exit on failure; optional machine-readable JSON |
| Dashboard | `asdlc serve` -> `/evals` | Human users, maintainers | Visual per-skill pass/fail without requiring terminal use |

Both surfaces must read from the same eval modules. The dashboard must call `validator.validate()` and `harness.run()` rather than maintaining separate eval logic.

## Scope traceability

| Requirement ID | Requirement | Milestones |
|---|---|---|
| R1 | Validate every `SKILL.md` for structural correctness | M2 |
| R2 | Catch drift across skills, docs, templates, and CLI bootstrap behavior | M3 |
| R3 | Run deterministic skill eval scenarios locally | M4 |
| R4 | Cover the highest-risk skills first | M5 |
| R5 | Keep the solution lightweight and maintainable | M1, M6 |
| R6 | Surface eval results in both CLI and dashboard without duplicate logic | M6 |
| R7 | Add automated regression coverage for eval behavior | M7 |

## Interface contracts summary

See `docs/architecture/data-domain.md` for full contracts.

Key boundaries:

- CLI -> validator: command parses flags and emits structured pass/fail validation results.
- CLI -> harness: command selects fixture scope and executes deterministic scenario assertions.
- Dashboard -> validator / harness: dashboard collects the same reports as the CLI and renders per-skill status.
- Harness -> fixture files: file-based scenarios define prompts, target skill, assertions, and pass criteria.
- Validator -> repository content: reads skills, docs, templates, and generated path expectations without mutating them.

## Risk log

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Plan remains stale while eval code evolves | M | M | Treat current repo baseline as the source of truth and update this plan when scope changes |
| Rule set becomes brittle and flags acceptable wording differences | M | M | Keep first-pass rules structural and path-based; require tests for each new semantic rule |
| Scenario evals overfit to current skill text instead of ideal behavior | M | H | Write fixtures from desired behavior first, then improve skills to pass |
| Repo path drift creates noisy validator output | H | M | Fix real drift first; document any accepted deviations with explicit rule IDs |
| Test harness setup slows delivery | M | M | Add small pytest tests for new eval modules before broad integration coverage |

## Assumptions

- Skill files under `src/agentic_sdlc/skills/` are the source of truth for validation in this repository.
- Installed projects may use `.agents/skills/`; validator and harness should continue resolving both layouts.
- Adding a committed `tests/` tree and using `pytest` as a dev dependency is acceptable.
- Initial scenario evals remain deterministic and rule-based; live-model scoring is deferred.
- CI integration can be added after local command behavior and JSON output shape are stable.

## Verification plan

Run these before marking the implementation complete:

```bash
python3 -m pytest -q
asdlc-dev validate-skills .
asdlc-dev eval-skills .
asdlc-dev validate-skills . --json-output
asdlc-dev eval-skills . --json-output
```

Dashboard verification:

```bash
asdlc serve .
```

Then open `/evals` and confirm:

- validation status is visible
- scenario status is visible
- per-skill result cards reflect the same modules used by the CLI

## Definition of done

- [ ] Focused tests exist for validator rules, consistency checks, harness assertions, CLI behavior, and dashboard eval data collection
- [ ] `python3 -m pytest -q` passes in a fresh dev environment
- [ ] `asdlc-dev validate-skills .` exits `0`, or every non-zero finding is intentionally accepted and documented
- [ ] `asdlc-dev eval-skills .` runs packaged fixtures and reports clear per-scenario pass/fail details
- [ ] JSON output for both commands is documented and stable enough for CI use
- [ ] Dashboard eval page renders results from the shared validator and harness modules
- [ ] Any skill weakness surfaced by evals has been fixed in the corresponding `SKILL.md`
- [ ] README and developer docs match the implemented commands and fixtures
