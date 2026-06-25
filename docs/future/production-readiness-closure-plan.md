# Production Readiness Closure Plan

> Date: 2026-06-25
> Scope: Stabilize and close the `agentic-sdlc` source repository for production readiness.
> Outcome target: READY verdict, or clear NOT READY verdict with exact remaining blockers.

## Short goal prompt

```text
Stabilize and close the agentic-sdlc repo for production readiness.

Known blockers:
- Dirty working tree on main.
- Installed `asdlc` / `asdlc-dev` fail with ModuleNotFoundError unless using PYTHONPATH=src.
- Missing closure docs: coding-standards.md, task-graph.md, test-plan.md, critical-review.md, retrospective.md.
- Existing code review says CHANGES REQUIRED.
- Dependency audit not passing / pip-audit unavailable.
- pyproject still marks package Beta.

Goal:
Make repo release-ready or produce clear NOT READY verdict with exact blockers.

Required work:
1. Follow relevant ASDLC skills: git-discipline, critical-review, testing, code-review, retrospective.
2. Audit repo state: git status, changed files, install state, docs state.
3. Fix installed CLI so `asdlc --help` and `asdlc-dev --help` work without PYTHONPATH.
4. Run fresh verification and record command, timestamp, exit code, summary:
   - full pytest suite
   - `asdlc-dev validate-skills .`
   - `asdlc-dev eval-skills .`
   - dependency audit using pip-audit or equivalent
   - installed CLI smoke tests
5. Create/update missing closure docs:
   - `docs/architecture/coding-standards.md`
   - `docs/sdlc/epics/task-graph.md`
   - `docs/sdlc/test-plans/test-plan.md`
   - `docs/sdlc/retrospectives/critical-review.md`
   - `docs/sdlc/retrospectives/retrospective.md`
6. Reconcile docs with repo truth. No artifact may claim green if current checks are red.
7. Fix all P0/P1 findings before final approval.
8. Run final testing and final code review.
9. Clean generated junk: pycache, egg-info, accidental build artifacts.
10. Commit cleanly with no AI/tool attribution trailers.

Definition of done:
- `pytest -q` passes.
- `asdlc-dev validate-skills .` passes.
- `asdlc-dev eval-skills .` passes.
- `asdlc --help` works.
- `asdlc-dev --help` works.
- dependency audit passes or accepted risk is documented.
- closure docs exist and match evidence.
- code review verdict is APPROVED.
- git status clean.
- final report states READY or NOT READY, with evidence and remaining risks.
```

## Execution plan

### Phase 1 — Repo truth audit

Commands:

```bash
git status --short --branch
git diff --stat
git diff
find docs -maxdepth 4 -type f | sort
```

Check:
- changed files are intentional
- no generated artifacts need cleanup
- closure docs exist or are missing as expected
- current branch strategy is clear

### Phase 2 — Fix installed CLI

Current symptom:

```text
asdlc --help -> ModuleNotFoundError: No module named 'agentic_sdlc'
asdlc-dev --help -> ModuleNotFoundError: No module named 'agentic_sdlc'
```

Likely cause:
- installed editable package points at an old path, not this repository
- or local Python version mismatch between script entrypoint and installed package

Verify:

```bash
python3.13 -m pip show agentic-sdlc
which asdlc
which asdlc-dev
head -1 $(which asdlc)
head -1 $(which asdlc-dev)
```

Fix path:

```bash
python3.13 -m pip uninstall -y agentic-sdlc
python3.13 -m pip install -e '.[dev]'
```

Then verify:

```bash
asdlc --help
asdlc-dev --help
```

### Phase 3 — Fresh verification

Run all checks from clean environment where possible:

```bash
pytest -q
asdlc-dev validate-skills .
asdlc-dev eval-skills .
python3.13 -m pip install pip-audit
python3.13 -m pip_audit
```

For each command record:
- timestamp
- command
- exit code
- output summary

### Phase 4 — Closure docs

Create or update:

- `docs/architecture/coding-standards.md`
- `docs/sdlc/epics/task-graph.md`
- `docs/sdlc/test-plans/test-plan.md`
- `docs/sdlc/retrospectives/critical-review.md`
- `docs/sdlc/retrospectives/retrospective.md`

Minimum required content:

#### coding-standards.md
- Python/package standards
- test command
- dependency audit command
- docs standards
- release criteria
- merge strategy

#### task-graph.md
- current epic/story list
- status per item
- acceptance criteria
- verification mapping

#### test-plan.md
- exact test commands
- results summary
- evidence table
- skipped/manual checks, if any

#### critical-review.md
- P0/P1/P2 findings
- verdict PASS only if no P0/P1 remain

#### retrospective.md
- what changed
- evidence table
- tech debt logged
- remaining risks
- final verdict

### Phase 5 — Critical review

Review against actual repo, not prior docs.

Blockers:
- broken installed CLI
- failing tests/evals/audit
- missing required docs
- stale green claims
- uncommitted release-critical changes

All P0/P1 must be fixed before continuing.

### Phase 6 — Final testing

Hard gate:
- no failing automated tests
- no stale evidence
- dependency audit passed or risk explicitly accepted
- installed CLI smoke test passed

### Phase 7 — Final code review

Pass sections:
- standards compliance
- test quality
- security audit
- operability
- documentation

Overall verdict must be `APPROVED` before READY claim.

### Phase 8 — Clean and commit

Before commit:

```bash
find . -type d -name __pycache__ -prune -exec rm -rf {} +
find . -type f -name '*.pyc' -delete
rm -rf src/agentic_sdlc.egg-info
pytest -q
asdlc-dev validate-skills .
asdlc-dev eval-skills .
git status --short
```

Commit message rules:
- use Conventional Commit format
- no AI/tool attribution trailers
- no session IDs
- no generated-by footers

Example:

```bash
git add .
git commit -m "chore(release): stabilize production readiness closure"
git log -1 --format=%B
```

Verify commit message has no unauthorized trailers.

## Final report template

```markdown
# Production readiness report — 2026-06-25

## Verdict
READY | NOT READY

## Evidence
| Check | Command | Exit | Timestamp | Summary |
|---|---|---:|---|---|
| Tests | `pytest -q` | 0 | ... | ... |
| Skill validation | `asdlc-dev validate-skills .` | 0 | ... | ... |
| Skill evals | `asdlc-dev eval-skills .` | 0 | ... | ... |
| CLI smoke | `asdlc --help && asdlc-dev --help` | 0 | ... | ... |
| Dependency audit | `python3.13 -m pip_audit` | 0 | ... | ... |

## Files changed
- ...

## Remaining risks
- None, or listed with owner and mitigation.

## Release notes
- ...
```
