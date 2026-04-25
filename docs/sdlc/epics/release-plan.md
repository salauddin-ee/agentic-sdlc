# Release Plan

> **Status:** Draft
> **Owner:** TBD
> **Last updated:** 2026-04-25
> **Audience:** Maintainers preparing the first published package release

## Purpose

Document the release-preparation work that follows the completed installation-doc cleanup.

This plan covers:

- TestPyPI and PyPI publishing readiness
- versioning and release verification
- post-publish documentation updates

This plan does not cover:

- marketplace submissions for Claude Code, Cursor, or other agent ecosystems
- new runtime features unrelated to release readiness

## Relationship to prior work

The installation work is already documented in `docs/sdlc/epics/installation-plan.md`.

That artifact should be kept as project history. It explains how the repository moved from clone-only install guidance to a cleaner pre-publish state. It should not be deleted just because the implementation is complete.

### Deferred from the installation plan

**Phase 4 of the installation plan (Marketplace publishing — Claude Code, Codex, Cursor) was intentionally skipped** and is tracked here for visibility:

- Blocked on PyPI publish (covered by this plan).
- Each marketplace requires its own publisher account and external review cycle.
- Will be picked up as separate work after the first PyPI release lands and is stable.

This release plan does **not** execute those submissions — it only unblocks them.

## Current baseline

Already verified on this branch:

- `python -m build` passes
- `python -m twine check dist/*` passes
- install docs are centralized in `docs/installation.md`
- unsupported pre-publish install paths have been removed from the live docs
- package metadata now includes `requires-python`, SPDX license expression, and project URLs

## Goals

1. Publish a test release to TestPyPI successfully
2. Verify `pip install agentic-sdlc` from TestPyPI in a fresh environment
3. Update install docs so PyPI becomes the recommended path after real publish
4. Publish the first real release to PyPI with a repeatable checklist

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Package upload succeeds but install path fails | Medium | High | Test on TestPyPI in a fresh venv before PyPI |
| Docs drift after publish | High | Medium | Update `docs/installation.md`, README, and platform docs in the same release-prep cycle |
| Version/tag mismatch | Medium | Medium | Use one explicit version bump step and verify built artifacts match |
| Missing release credentials or account setup | Medium | High | Confirm TestPyPI/PyPI access before the release window |

## Phase 1 - TestPyPI dry run

### Tasks

1. Confirm maintainer credentials and package ownership on TestPyPI
2. Build fresh artifacts:
   ```bash
   python -m build
   python -m twine check dist/*
   ```
3. Upload to TestPyPI
4. In a fresh virtual environment, install from TestPyPI and verify:
   ```bash
   python3 -m venv /tmp/asdlc-testpypi
   source /tmp/asdlc-testpypi/bin/activate
   python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple agentic-sdlc
   asdlc --help
   asdlc-dev --help
   mkdir -p /tmp/asdlc-test-project
   asdlc init /tmp/asdlc-test-project
   ```

### Exit criteria

- TestPyPI upload succeeds
- fresh install from TestPyPI succeeds
- `asdlc` and `asdlc-dev` resolve
- `asdlc init` creates `AGENTS.md` and `.agents/skills/` correctly

## Phase 2 - Post-publish doc changes

### Tasks

1. Update `docs/installation.md`
   - make `pip install agentic-sdlc` the recommended path
   - keep clone/manual install as fallback paths
2. Update README install quick start
3. Update platform docs so they point at the PyPI-backed canonical flow
4. Remove pre-publish TODO wording that assumes PyPI is unavailable

### Exit criteria

- docs no longer describe local clone as the primary path
- fallback instructions still exist for offline/manual cases
- platform docs remain aligned with the canonical install guide

## Phase 3 - PyPI release

### Tasks

1. Decide the release version
2. Update `pyproject.toml`
3. Rebuild artifacts
4. Upload to PyPI
5. Verify fresh install from PyPI
6. Create release notes / tag

### Exit criteria

- package is installable from PyPI in a fresh environment
- docs match the published install path
- release version, tag, and built artifacts are consistent

## Verification checklist

- [ ] `python -m build`
- [ ] `python -m twine check dist/*`
- [ ] TestPyPI upload
- [ ] fresh TestPyPI install
- [ ] fresh PyPI install
- [ ] `asdlc --help`
- [ ] `asdlc-dev --help`
- [ ] `asdlc init /tmp/<test-project>`
- [ ] install docs updated after publish

## Definition of done

- [ ] TestPyPI dry run completed successfully
- [ ] publish steps are documented and repeatable
- [ ] docs are updated for the post-publish state
- [ ] first PyPI release is verified from a clean environment
