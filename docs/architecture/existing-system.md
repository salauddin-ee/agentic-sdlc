# Existing system analysis

> **Status:** Approved
> **Version:** 0.2.0

## Tech stack
| Component | Technology | Version | Notes |
|---|---|---|---|
| Language | Python | 3.14.4 | Verified via `python3 --version` in the local environment |
| Packaging | setuptools build backend | n/a | Declared in `pyproject.toml` |
| CLI framework | Click | >=8.1.0 | Used in `src/agentic_sdlc/cli.py` |
| Markdown/YAML parsing | PyYAML | >=6.0.0 | Used in `src/agentic_sdlc/dashboard.py` |
| Runtime surface | Python package + stdlib HTTP server | n/a | Dashboard serves via `http.server` |
| Test runner | pytest | not installed in current environment | `python3 -m pytest -q` failed with `No module named pytest` |

## Test coverage baseline
- Total tests discovered in repo: 1 test file (`tests/test_cli.py`, 4 tests)
- Passing: 4 (verified via `python3 -m pytest -q` with pytest installed)
- Failing: 0
- Coverage: not measured; no coverage tooling configured
- Last run: 2026-04-25

**Baseline note:** `tests/test_cli.py` covers `asdlc init` behavior, platform doc entry-point checks, and unsupported-entrypoint guards. Run `python3 -m pytest -q` in a venv with dev dependencies installed.

## Existing patterns
- Error handling: broad exception swallowing in utility paths; `dashboard.parse_markdown_file()` catches broad exceptions and prints parsing failures instead of raising typed errors.
- Logging: ad hoc `print()` for parsing failures and `click.echo()` for CLI progress output; no structured logger.
- Input validation: Click argument and option validation at CLI boundaries; otherwise lightweight manual assumptions inside helper functions.
- Directory structure: packaged Python source under `src/agentic_sdlc/`, human-facing docs at repo root `docs/`, templates in `src/agentic_sdlc/skills/`, evaluation code in `src/agentic_sdlc/eval/`.
- Naming: snake_case Python modules and functions, kebab-case skill/template directories, markdown-driven configuration with YAML frontmatter.

## Known tech debt
- Test infrastructure absent: no committed automated test suite or coverage reporting.
- Documentation drift risk: repo-root agent docs and the packaged `src/agentic_sdlc/core/AGENTS.md` file can diverge if they are edited independently.
- Packaging/install drift risk: `pyproject.toml` uses PEP 517 build isolation, which currently fails in a clean offline venv because build dependencies are fetched from the index.
- Dashboard/frontend polish is bundled inline in `dashboard.py`, which makes larger UI changes harder to review and test.

## Integration points
| Integration | Direction | Protocol | Notes |
|---|---|---|---|
| Filesystem project root | inbound/outbound | local file I/O | CLI initializes docs, skills, templates, and core markdown files into target repos |
| Python packaging toolchain | outbound | PEP 517 build backend | `setuptools.build_meta` is used for packaging and installation |
| Local HTTP clients/browsers | outbound | HTTP | Dashboard serves HTML via stdlib `HTTPServer` |

## Fragile / high-risk areas
- `src/agentic_sdlc/cli.py`: installer behavior copies generated artifacts into user repos; doc/path mistakes here propagate into every initialized project.
- `src/agentic_sdlc/core/AGENTS.md`: this is the packaged source of truth for initialized projects and can silently drift from the repo-root `AGENTS.md`.
- `src/agentic_sdlc/skills/*.md`: process contradictions create systemic agent behavior regressions even without Python code changes.
- Packaging entrypoints: any change to build metadata affects `pip install` behavior across the whole project.

## Constraints
- The framework relies on markdown skill files as executable process guidance; textual inconsistencies are product defects, not merely editorial issues.
- Repo currently lacks a verified automated test baseline, so review conclusions rely primarily on diff inspection plus targeted command verification.
- Plain `pip install` on externally-managed Python (Homebrew, Debian/Ubuntu system Python) is blocked by PEP 668 unless the user is in a virtual environment or explicitly opts out with `--break-system-packages`.
