# Implementation Plan: Skill Eval Tooling

> **Epic ID:** E-001
> **Date:** 2026-04-25
> **Status:** Approved
> **Version:** 0.3.0

## User Review Required

> [!IMPORTANT]
> This file is the canonical Stage 4 implementation-planning artifact for the source repository. It stays at `docs/sdlc/epics/implementation-plan.md` because the framework contract, CLI bootstrap, and skills all treat that path as required.
>
> Remaining follow-up work is tracked separately in `docs/future/skill-evals-implementation-plan.md`. That future plan does not replace this artifact.

## Proposed Changes

Retain the approved baseline architecture for the eval tooling that is already shipped in this repository:

- developer CLI commands: `asdlc-dev validate-skills` and `asdlc-dev eval-skills`
- shared eval modules under `src/agentic_sdlc/eval/`
- packaged fixtures under `src/agentic_sdlc/fixtures/`
- dashboard `/evals` surface backed by the same validator and harness modules
- interface contracts documented in `docs/architecture/data-domain.md`

### CLI Surface

- `src/agentic_sdlc/cli.py`
- public CLI remains `asdlc`
- developer-only eval commands remain on `asdlc-dev`

### Eval Modules

- `src/agentic_sdlc/eval/models.py`
- `src/agentic_sdlc/eval/validator.py`
- `src/agentic_sdlc/eval/consistency.py`
- `src/agentic_sdlc/eval/harness.py`
- `src/agentic_sdlc/eval/utils.py`

### Fixtures And Docs

- `src/agentic_sdlc/fixtures/`
- `docs/architecture/data-domain.md`
- `README.md`

## Open Questions

- [ ] No blocking questions for the shipped baseline. Future hardening work is tracked in `docs/future/skill-evals-implementation-plan.md`.

## Verification Plan

### Automated Tests

- [ ] `python3 -m pytest -q` in a dev environment with optional dependencies installed
- [ ] `asdlc-dev validate-skills .`
- [ ] `asdlc-dev eval-skills .`

### Manual Verification

- [ ] `asdlc serve .`
- [ ] open `/evals` and confirm validation and scenario results render from shared modules

---
*Written by: agentic-sdlc implementation-planning skill*
