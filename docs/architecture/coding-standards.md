# Coding constitution — agentic-sdlc

> **Status:** Current
> **Version:** 1.0.0
> **Last verified:** 2026-06-25T02:43:03Z

## Language and runtime
- Language: Python 3.9+.
- Packaging: setuptools with `pyproject.toml`, source layout under `src/`.
- CLI framework: Click.
- YAML parsing: PyYAML.
- Supported contributor install: editable install with dev extras, preferably via `pipx install -e ".[dev]"` for global CLI smoke tests or a virtual environment for local development.

## Project structure
- `src/agentic_sdlc/`: package code, CLI entrypoints, dashboard, packaged skills, core `AGENTS.md`, eval fixtures.
- `src/agentic_sdlc/skills/`: packaged ASDLC skills and templates.
- `src/agentic_sdlc/eval/`: static validator and deterministic skill-eval harness.
- `src/agentic_sdlc/fixtures/`: packaged eval scenarios.
- `tests/`: pytest suite for CLI and scaffold contracts.
- `docs/`: framework documentation, architecture contracts, SDLC closure artifacts, and future plans.

## Naming conventions
- Python modules and functions: `snake_case`.
- Classes: `PascalCase`.
- Constants: `UPPER_SNAKE_CASE`.
- Tests: `test_*.py` files with `test_...` functions that describe behavior.
- Skills: directory name and frontmatter `name` must match `asdlc-*` hyphen-case names.
- Fixture files: YAML scenarios grouped by skill directory.

## Error handling
- CLI commands must exit non-zero for validation, eval, or scaffold failures.
- Human-readable CLI errors should be emitted with Click and include enough context to fix the issue.
- Eval and validation modules should collect structured failures instead of throwing when a scenario or skill fails validation.

## Logging and output standards
- CLI output must be deterministic enough for tests and documentation evidence.
- Validation and eval commands must provide concise pass/fail summaries and detailed failure lines.
- JSON output modes must emit stable report dictionaries suitable for automation.
- Do not log secrets, tokens, or private user data.

## Test standards
- Framework: pytest.
- Required full-suite command: `pytest -q`.
- Required skill validation command: `asdlc-dev validate-skills .`.
- Required skill eval command: `asdlc-dev eval-skills .`.
- Required CLI smoke commands: `asdlc --help` and `asdlc-dev --help` from the installed entrypoints, without `PYTHONPATH`.
- Test pyramid target for this CLI/library repo: mostly unit/contract tests; integration smoke tests cover installed CLI and dependency audit during closure.
- Tests must validate behavior and user-facing contracts, not private implementation details.

## Security non-negotiables
- No secrets in source, docs, fixtures, or logs.
- Dependencies must be audited before release with `pipx run pip-audit . --progress-spinner off` or equivalent.
- No high or critical vulnerability may remain without explicit documented risk acceptance.
- Any future network-facing dashboard hardening must include dependency audit and review of exposed endpoints before release.

## Clean code principles
- Prefer small, deterministic functions in CLI/eval modules.
- Avoid hidden global state in validation and eval logic.
- Keep source-layout imports package-relative.
- Do not commit generated junk: `__pycache__/`, `*.pyc`, `.pytest_cache/`, or `*.egg-info/`.
- No TODO/FIXME comments in production code unless tied to a documented future plan.

## Documentation standards
- Repo-truth artifacts must not claim green status unless current commands back the claim.
- Verification evidence must include command, timestamp, exit code, and output summary.
- Future or speculative plans belong under `docs/future/` and must not replace canonical ASDLC artifacts.
- Closure reviews must supersede stale historical CHANGES REQUIRED notes only with fresh evidence.

## Release criteria
A production-readiness closure may state `READY` only when all are true:
- `pytest -q` exits 0.
- `asdlc-dev validate-skills .` exits 0.
- `asdlc-dev eval-skills .` exits 0.
- `asdlc --help` exits 0 from installed entrypoint without `PYTHONPATH`.
- `asdlc-dev --help` exits 0 from installed entrypoint without `PYTHONPATH`.
- Dependency audit passes, or accepted risk is documented.
- Closure docs exist and match current evidence.
- Final code review verdict is `APPROVED`.
- Git status is clean after commit.

## Dependency management
- Runtime dependencies live in `[project].dependencies`.
- Development dependencies live in `[project.optional-dependencies].dev`.
- Add new dependencies only with a clear package purpose and an audit-compatible version range.
- Re-run dependency audit after dependency changes.

## Merge strategy
- This repository uses direct-to-main local closure for production-readiness maintenance when the user explicitly requests end-to-end closure in the current worktree.
- Commit format: Conventional Commits with no AI/tool attribution trailers.
- Forbidden commit metadata: co-author trailers for agents, session/thread/run IDs, generated-by footers, or tool signatures.
- Before reporting completion, run `git log -1 --format=%B` and verify the message contains only the human-authored commit text.
