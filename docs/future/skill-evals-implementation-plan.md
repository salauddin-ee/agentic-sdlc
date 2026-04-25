# Future plan - skill eval tooling hardening

> **Status:** Deferred
> **Version:** 0.2.0
> **Last updated:** 2026-04-25

## Purpose

Track only the unfinished hardening work for the already-shipped eval tooling baseline.

The canonical Stage 4 artifact for the shipped baseline remains:

- `docs/sdlc/epics/implementation-plan.md`

This future plan is intentionally narrower. It should not duplicate implemented milestones or historical rollout notes.

## Current baseline

Already implemented in the repository:

- shared eval modules under `src/agentic_sdlc/eval/`
- developer CLI commands `asdlc-dev validate-skills` and `asdlc-dev eval-skills`
- packaged fixtures under `src/agentic_sdlc/fixtures/`
- dashboard `/evals` page backed by the same validator and harness modules
- contributor documentation in `README.md`

## Remaining work

### F1. Automated regression coverage

Add committed tests for:

- validator rule coverage
- consistency rule coverage
- fixture loading and harness assertion behavior
- CLI result formatting and exit behavior
- dashboard eval data collection

### F2. Final verification in a fresh dev environment

Run and record:

```bash
python3 -m pytest -q
asdlc-dev validate-skills .
asdlc-dev eval-skills .
asdlc-dev validate-skills . --json-output
asdlc-dev eval-skills . --json-output
```

### F3. Documentation drift cleanup

Confirm docs continue to match the implemented behavior:

- validator rule ids and examples
- JSON output examples
- dashboard eval behavior
- fixture and command counts where examples are intentionally concrete

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Future plan drifts into historical narrative again | M | M | Keep this file scoped to unfinished work only |
| Rule set becomes brittle and flags acceptable wording differences | M | M | Add focused tests for each new rule |
| Scenario evals overfit to current skill text instead of ideal behavior | M | H | Add failing fixtures first, then improve the skills |
| Environment gaps hide verification regressions | H | M | Re-run final verification in a fresh dev environment before closing this plan |

## Verification gate

- [ ] Committed tests exist for validator, consistency, harness, CLI, and dashboard eval data collection
- [ ] `python3 -m pytest -q` passes in a fresh dev environment
- [ ] `asdlc-dev validate-skills .` exits `0`, or any accepted findings are explicitly documented
- [ ] `asdlc-dev eval-skills .` passes with clear per-scenario output
- [ ] README and architecture docs match the implemented eval behavior
