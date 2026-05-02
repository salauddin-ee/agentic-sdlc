# Existing system analysis

> **Status:** Draft
> **Version:** 0.1.0
> **Last updated:** 2026-05-02

## Tech stack
| Component | Technology | Version | Notes |
|---|---|---|---|
| Language | Python | >=3.9 | Package source under `src/agentic_sdlc/` |
| Runtime | Python | 3.13.12 observed locally | Current local test run used Python 3.13.12 |
| Package manager/build | setuptools | >=77.0.0 | Configured in `pyproject.toml` |
| CLI framework | Click | >=8.1.0 | Public `asdlc`; developer `asdlc-dev` |
| YAML support | PyYAML | >=6.0.0 | Used by skill eval/validation tooling |
| Test runner | pytest | >=7.0.0 | Optional dev dependency |
| Coverage | pytest-cov | >=4.0.0 | Optional dev dependency |

## Test coverage baseline
- Command: `pytest --cov=agentic_sdlc -q`
- Exit code: 0
- Total tests: 9
- Passing: 9
- Failing: 0
- Coverage: 15% total lines
- Last run: 2026-05-02

**This baseline must not decrease. Any change that drops coverage requires HITL approval.**

## Existing patterns
- Error handling: CLI commands use Click output plus `click.exceptions.Exit(code=1)` for user-facing failures.
- Logging/output: CLI prints concise human-readable status lines with `click.echo`.
- Input validation: Click argument and option types validate command inputs.
- Directory structure: package code lives under `src/agentic_sdlc/`; skills under `src/agentic_sdlc/skills/asdlc-*`; fixtures under `src/agentic_sdlc/fixtures/`; tests under `tests/`.
- Tests: `tests/test_cli.py` uses `click.testing.CliRunner` and temporary directories to validate scaffold behavior.

## Known tech debt
- Skill process safety gaps are tracked in `NEED-TO-FOCUS.md`.
- `docs/architecture/existing-system.md` previously described an unrelated TrainAssist app and has been refreshed for this repository.
- Overall coverage is low because dashboard and eval modules have little or no test coverage.

## Integration points
| Integration | Direction | Protocol | Notes |
|---|---|---|---|
| Local filesystem | read/write | POSIX paths via `pathlib`/`shutil` | `asdlc init` scaffolds docs, `.agents/skills`, and `AGENTS.md` into target projects |
| Python packaging | outbound | setuptools entry points | Publishes `asdlc` and `asdlc-dev` console scripts |
| Browser dashboard | local service | HTTP | `asdlc serve` delegates to `dashboard.serve` |
| Skill fixtures | local read | YAML files | `asdlc-dev eval-skills` reads deterministic scenario fixtures |

## Fragile / high-risk areas
- `src/agentic_sdlc/skills/`: Skill wording is the product contract; small instruction changes can alter agent behavior across all initialized projects.
- `src/agentic_sdlc/core/AGENTS.md`: Copied into user projects by `asdlc init`; changes affect bootstrapping and agent instruction priority.
- `src/agentic_sdlc/cli.py`: `init` currently owns scaffold creation and skill copying; changes can overwrite user project files if not carefully tested.
- `docs/workflow-greenfield.md` and `docs/workflow-brownfield.md`: Must stay aligned with skill transition rules.
- `tests/test_cli.py`: Current tests mainly cover init/update-agents scaffolding; process behavior is mostly guarded by fixtures and validation tooling.

## Constraints
- Commit messages in this repository must not contain agent/tool attribution metadata.
- Packaged skills live in `src/agentic_sdlc/skills/`; initialized projects receive copies under `.agents/skills/`.
- Stage artifacts should be written to `docs/` and should not rely on conversation memory.
- User approval is required for irreversible decisions and mandatory HITL checkpoints.
