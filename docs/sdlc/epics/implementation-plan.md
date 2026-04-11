# Implementation plan

> **Status:** Draft
> **Version:** 0.1.0

## Preconditions / approval blockers
- A story section in `docs/product/features/brd.md` does not exist yet, so full brownfield traceability is not complete.
- `docs/architecture/tech-architecture.md` and `docs/architecture/coding-standards.md` are not present in this repo, so this plan currently relies on the user request plus `docs/architecture/existing-system.md`.
- This plan should remain `Draft` until the story intent is documented and the user explicitly approves moving into implementation.

## Eval-Driven Skill Improvement Principle

Evals are not just a quality gate — they **actively drive skill quality**. This mirrors the TDD discipline the framework enforces for production code:

```
NO SKILL CHANGE WITHOUT A FAILING EVAL FIRST.
```

The correct order is always:
1. Write the eval asserting ideal behavior
2. Run it — the current skill may fail (expected)
3. Fix the skill until the eval passes
4. The eval becomes a permanent regression guard

A milestone is **not complete** until:
- its eval layer passes, **AND**
- any skill weaknesses it surfaces have been fixed in the skill text

This means static validation (M2) and consistency checks (M3) each have a built-in **fix pass** before the next milestone begins. Scenario evals (M4/M5) are written to **ideal** behavior, not current behavior, so the skill must be improved to meet them.

## Milestones
| ID | Name | Description | Exit criteria | Depends on |
|---|---|---|---|---|
| M1 | Eval foundation | Add shared eval package, result models, and CLI command skeletons | `asdlc validate-skills --help` and `asdlc eval-skills --help` resolve; module layout is in place | — |
| M2 | Static validation | Validate every `SKILL.md` for frontmatter, required metadata, placeholders, and basic structure | Validator passes with zero errors; all skill issues it surfaces have been fixed in skill text; unit tests cover key rule paths | M1 |
| M3 | Consistency checks | Detect drift between skills, docs, templates, and CLI-created paths | All known path/reference inconsistencies are caught and **fixed**; false-positive rate is acceptable for local use | M2 |
| M4 | Scenario eval harness | Add file-based scenario loading and deterministic rule-based assertions | Fixtures run through `asdlc eval-skills`; results include failure reasons per scenario | M1 |
| M5 | Initial skill suite | Cover the five highest-risk skills with fixtures written to ideal behavior | At least 2 scenarios per skill pass; any skills that failed evals have been improved to meet the ideal | M4 |
| M6 | Documentation and rollout | Document usage, wire commands into the developer workflow, and surface eval results in the `asdlc serve` dashboard | README/docs updated; validation and eval results visible in dashboard per skill; eval-driven improvement loop documented as standard workflow | M2, M3, M5 |

## Design Decision: CLI + Dashboard (Dual Surface)

Eval results are exposed on **two surfaces** for different audiences:

| Surface | Command | Audience | Use case |
|---|---|---|---|
| CLI | `asdlc validate-skills` / `asdlc eval-skills` | CI pipelines, automation, agents | Non-zero exit on failure; machine-readable JSON |
| Dashboard | `asdlc serve` → Evals tab | Human users, maintainers | Visual per-skill pass/fail; no terminal required |

Both surfaces read from the same eval modules — the dashboard calls the same `validator.validate()` and `harness.run()` functions and renders the results visually. No separate eval logic for the dashboard.

## Scope traceability
| Requirement ID | Requirement | Milestones |
|---|---|---|
| R1 | Validate every `SKILL.md` for structural correctness | M2 |
| R2 | Catch drift across skills, docs, templates, and CLI bootstrap behavior | M3 |
| R3 | Run deterministic skill eval scenarios locally | M4 |
| R4 | Cover the five highest-risk skills first | M5 |
| R5 | Keep the solution lightweight and maintainable | M1, M6 |

## Interface contracts summary
See `docs/architecture/data-domain.md` for full specs.

Key boundaries:
- CLI -> validator: command parses flags and emits structured pass/fail results from validation checks.
- CLI -> harness: command selects fixture scope and executes scenario assertions.
- Harness -> fixture files: file-based scenarios define prompts, target skill, expected assertions, and pass criteria.
- Validator -> repository content: reads skills, docs, templates, and generated path expectations without mutating them.

## Risk log
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Rule set becomes brittle and flags too many acceptable wording differences | M | M | Start with structural and path-based checks before adding semantic assertions |
| Scenario evals require model behavior that cannot be reproduced deterministically offline | H | M | Keep initial suite rule-based and fixture-driven; defer live-model scoring |
| Repo path drift is deeper than expected, making validator output noisy at first | H | M | Ship focused checks first, then fix current drift and codify regressions |
| Lack of existing test harness slows delivery | M | M | Add small pytest-based unit tests only for new eval modules and CLI paths |

## Assumptions
- Skill files under `src/agentic_sdlc/skills/` are the source of truth for validation.
- Adding a `tests/` tree and `pytest` as a dev dependency is acceptable for this repository.
- Initial eval coverage should prioritize deterministic correctness checks over model scoring sophistication.
- The first release only needs local CLI execution; CI integration can be added once output shape stabilizes.

## Definition of done (project level)
- [ ] All targeted validation rules are implemented with automated tests
- [ ] All targeted scenario fixtures run through a single local harness
- [ ] CLI commands are documented and return clear non-zero exit behavior on failures
- [ ] Current known skill/doc/path drift is either fixed or explicitly reported by the validator
- [ ] At least the five highest-risk skills have repeatable regression coverage
- [ ] No external services or heavy infrastructure are required to run the suite
