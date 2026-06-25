# Changelog

All notable changes to this project are documented here.

## v1.0.0 — 2026-06-25

### Release scope
- Source release for local clone, editable install, and manual installation workflows.
- PyPI/TestPyPI publishing is intentionally deferred and tracked in `docs/future/release-plan.md`.

### Production-readiness evidence
- `pytest -q` passes.
- `asdlc-dev validate-skills .` passes.
- `asdlc-dev eval-skills .` passes.
- `asdlc --help` and `asdlc-dev --help` work from installed entrypoints.
- Dependency audit passes with no known vulnerabilities.
- Closure docs and final APPROVED code review are recorded under `docs/sdlc/`.
