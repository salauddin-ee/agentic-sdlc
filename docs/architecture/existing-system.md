# Existing system analysis

## Tech stack
| Component | Technology | Version | Notes |
|---|---|---|---|
| Language | Python | 3.9.6 | Verified via `python3 --version` in local environment |
| Packaging | setuptools | n/a | Defined in `pyproject.toml` build backend |
| CLI framework | Click | >=8.1.0 | Used in `src/agentic_sdlc/cli.py` |
| Markdown/YAML parsing | PyYAML | >=6.0.0 | Used in dashboard metadata parsing |
| Runtime surface | Python package + stdlib HTTP server | n/a | `dashboard.py` serves via `http.server` |
| Test runner | pytest | not configured in environment | `python3 -m pytest -q` failed: `No module named pytest` |

## Test coverage baseline
- Total tests discovered in repo: 0 dedicated test files
- Passing: 0
- Failing: 0
- Coverage: unavailable; no coverage report or test harness is configured in this checkout
- Last run: 2026-04-09 local time

**Baseline note:** repository-wide search found no `tests/` tree or `test_*.py` / `*_test.py` files. Attempting `python3 -m pytest -q` failed because `pytest` is not installed in the current environment.

## Existing patterns
- Error handling: best-effort exception swallowing in utility paths; `dashboard.parse_markdown_file()` catches broad exceptions and logs to stdout rather than surfacing typed errors.
- Logging: ad hoc `print()` for parsing failures and `click.echo()` for CLI progress output; no structured logger.
- Input validation: Click argument and option validation at CLI boundaries; otherwise lightweight manual assumptions inside helper functions.
- Directory structure: packaged Python source under `src/agentic_sdlc/`, human-facing docs at repo root `docs/`, templates in `src/agentic_sdlc/templates/`, skills in `src/agentic_sdlc/skills/`.
- Naming: snake_case Python modules and functions, kebab-case skill/template directories, markdown-driven configuration with YAML frontmatter.

## Known tech debt
- Test infrastructure absent: no committed automated test suite or coverage reporting.
- Documentation drift risk: repo-root agent docs and packaged `src/agentic_sdlc/core/*.md` files can diverge because both exist and are maintained separately.
- Dashboard/frontend polish is bundled inline in `dashboard.py`, which makes larger UI changes harder to review and test.

## Integration points
| Integration | Direction | Protocol | Notes |
|---|---|---|---|
| Filesystem project root | inbound/outbound | local file I/O | CLI initializes docs, skills, templates, and core markdown files into target repos |
| Python packaging toolchain | outbound | PEP 517 build backend | `setuptools.build_meta` used for packaging and installation |
| Local HTTP clients/browsers | outbound | HTTP | Dashboard serves HTML via stdlib `HTTPServer` |

## Fragile / high-risk areas
- `src/agentic_sdlc/cli.py`: installer behavior copies generated artifacts into user repos; doc/path mistakes here propagate into every initialized project.
- `src/agentic_sdlc/core/*.md`: these files are the packaged source of truth for initialized projects and can silently drift from repo-root copies.
- `src/agentic_sdlc/skills/*.md`: process contradictions create systemic agent behavior regressions even without Python code changes.

## Constraints
- The framework relies on markdown skill files as executable process guidance; textual inconsistencies are product defects, not merely editorial issues.
- Repo currently lacks a verified automated test baseline, so review conclusions rely primarily on diff inspection plus targeted command verification.
