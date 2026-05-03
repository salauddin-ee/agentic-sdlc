# Need to Focus

Prioritized improvements for the Agentic SDLC skills framework.
Discovered via a full Greenfield + Brownfield exercise against a dummy Zen Quotes app (2026-05-01).

> **Rule:** Fix everything in Tier 1 before touching Tier 2. Fix Tier 2 before Tier 3.

## Current review summary — 2026-05-01

This file was re-reviewed against the current repository and the `dummy-zen-app`
exercise artifacts on 2026-05-01.

- Original findings about direct merges, merge-strategy selection, orphaned testing, workspace files, domain-model templates, brownfield BRD appends, domain-model drift, and story YAML enforcement are still valid.
- Original findings about HITL proof, `data-domain.md`, BRD approval status, review history, and UI mockup skip guidance are partially fixed or partially valid, but still need tightening.
- Original findings about `task-graph.md`, ADR files, and `accessibility.md` are now mostly covered by current skill gates, but the dummy exercise still shows agents can miss them if gates are not evidence-backed.
- Additional Tier 1 and Tier 2 items were added below from the current repo review and dummy-zen audit.

---

## Tier 1 — Critical (Framework safety broken)

### 1. Stories merge directly to `main` — unsafe by default

**Status:** ✅ DONE (2026-05-02, commit `91d5f35`) — Epic integration branch is now the default. `asdlc-git-discipline` defines three strategies (Epic branch / Direct to main / PR-based), with Epic branch as the missing-config default. New **Epic Finalization Protocol** requires full regression on `feature/EPIC-{ID}` and explicit HITL approval before merging to `main`. `asdlc-implementation`, `asdlc-code-review`, and `asdlc-retrospective` all defer to the configured strategy.

**Problem:** The framework currently squash-merges each story directly to `main` after code review. This has three compounding risks:
- **No integration testing** — stories that work individually can break each other on `main`.
- **No PR flow** — bypasses CI, team review, and remote branch protection.
- **User loses control** — the agent decides when `main` changes; the user is never asked.

**Root cause:** The framework assumes a solo-dev, local-only workflow and makes that the *only* workflow.

**Affected Files:**
- `src/agentic_sdlc/skills/asdlc-git-discipline/SKILL.md` (Branch Strategy, Story Implementation Protocol)
- `src/agentic_sdlc/skills/asdlc-code-review/SKILL.md` (Merge Protocol)
- `src/agentic_sdlc/skills/asdlc-implementation/SKILL.md` (Transition section)
- `src/agentic_sdlc/skills/asdlc-retrospective/SKILL.md` (no final regression step)

**Fix — Epic Integration Branch as default:**

Replace the current "story → main" pattern with an **epic integration branch** where stories accumulate before hitting `main`:

```
Default (safe):
  feature/EPIC-001 ← feature/STORY-001  (squash merge after code-review)
  feature/EPIC-001 ← feature/STORY-002  (squash merge after code-review)
  feature/EPIC-001 ← feature/STORY-003  (squash merge after code-review)
  → Run full regression on feature/EPIC-001
  → HITL: "All stories merged. Approve merge to main?"
  main ← feature/EPIC-001               (only on explicit user approval)

Fallback (solo-dev, if user opts in):
  main ← STORY-001  (squash, current behavior)
```

This means:
- `main` is **always stable** — only user-approved, fully-regressed code lands there.
- Stories integrate with each other on the epic branch first — cross-story regressions are caught before `main` is touched.
- The user explicitly controls when `main` changes.

---

### 2. Ask the user for merge strategy during planning — not after

**Status:** ✅ DONE (2026-05-02, commit `91d5f35`) — `asdlc-implementation-planning` now includes a mandatory **Merge Strategy HITL** step (steps 6–7) with the exact prompt template and three options (Epic / Direct / PR), defaulting to Epic branch if no response. Decision is recorded in `docs/architecture/coding-standards.md` under `## Merge strategy`. `asdlc-git-discipline`, `asdlc-implementation`, `asdlc-story-breakdown`, `asdlc-code-review`, and `asdlc-retrospective` all read this section. Eval fixtures `merge-strategy-hitl-001.yaml` and `epic-branch-default-001.yaml` cover both behaviors.

**Problem:** The current framework hard-codes the merge strategy (squash to main). The user is never asked how they want to handle branching. This decision should happen during the **implementation-planning** phase, before any branches are created.

**Affected Files:**
- `src/agentic_sdlc/skills/asdlc-implementation-planning/SKILL.md` (Checklist — add a new step)
- `src/agentic_sdlc/skills/asdlc-git-discipline/SKILL.md` (Branch Strategy — make configurable)

**Fix:** Add a HITL question to `asdlc-implementation-planning` before story-breakdown begins:

```
HITL REQUIRED
Stage: implementation-planning
Question: How should completed stories be merged?
Context: Stories will be broken down and implemented on feature branches.
Options: [A] Epic branch (recommended) — stories merge into feature/EPIC-{ID},
             then epic branch merges to main after full regression + your approval.
         [B] Direct to main — each story squash-merges to main after code-review
             (solo-dev workflow, no integration branch).
         [C] PR-based — stories push to remote and open PRs against main
             (team workflow with CI and remote review).
Default if no response: [A] Epic branch
```

Record the decision in `docs/architecture/coding-standards.md` under a new `## Merge strategy` section. The `asdlc-git-discipline` skill reads this section to determine which protocol to follow.

---

### 3. HITL is never actually invoked — agents self-approve

**Status:** ✅ DONE (2026-05-02) — `asdlc-stage-gates` now requires durable HITL evidence (`hitl_prompt`, `hitl_response`, `hitl_decision`, `hitl_approved_by`, `hitl_approved_at`) before `Status: Approved` is valid. `asdlc-hitl-protocol` now defines the artifact evidence lifecycle: `Ready for HITL` before prompting, then `Approved` only after the user response is recorded. Added stage-gate eval coverage for approved-without-HITL-evidence.

**Current status:** Partially fixed in text, still unsafe. `asdlc-stage-gates` now says user approval is not assumed, but there is no artifact-level proof of the actual prompt and user response. There is also a gate-ordering conflict: stage-gates require `Status: Approved` before the gate passes, while stage skills often set `Approved` only after HITL.

**Problem:** Despite HITL being mandatory at the end of inception, tech-architecture, and story-breakdown, the dummy exercise passed through ALL stages without a single HITL prompt being presented to the user. The agent self-approved everything. This is the most critical process deviation — HITL is the framework's primary safety mechanism.

**Affected Files:**
- `src/agentic_sdlc/skills/asdlc-stage-gates/SKILL.md`
- `src/agentic_sdlc/skills/asdlc-hitl-protocol/SKILL.md`

**Fix:** Add a **mandatory HITL verification** to `asdlc-stage-gates`:
```
[ ] HITL checkpoint invoked for this stage (reference the HITL prompt and user response)
```
Consider adding a `hitl_response` field to artifact frontmatter so the gate can verify HITL was triggered, not just that the artifact exists.

---

### 4. `asdlc-testing` is orphaned — no prior skill creates its input

**Status:** ✅ DONE (2026-05-03) — `asdlc-testing` now owns its own bootstrap: Step 1 checks whether `docs/sdlc/test-plans/test-plan.md` exists and creates it from `test-plan-template.md` if absent, deriving initial test cases from BRD acceptance criteria and the implementation-plan definition of done. A new gate item explicitly requires the file to physically exist. `asdlc-using-agentic-sdlc` context directory comment updated to clarify this stage creates + fills the file.

**Problem:** The testing skill reads `docs/sdlc/test-plans/test-plan.md` as its primary input. But **no earlier skill creates this file**. The implementation skill doesn't mention it. The critical-review transitions to "proceed to testing" but the input doesn't exist. During the exercise, the entire testing stage was silently skipped.

**Affected Files:**
- `src/agentic_sdlc/skills/asdlc-testing/SKILL.md`
- `src/agentic_sdlc/skills/asdlc-implementation-planning/SKILL.md` (or `asdlc-story-breakdown`)

**Fix:** Either (a) add a step to `asdlc-implementation-planning` or `asdlc-story-breakdown` to produce a test plan skeleton, or (b) have `asdlc-testing` create the test plan itself as step 1. Update the Context Directory in `asdlc-using-agentic-sdlc` to clarify which stage produces `test-plan.md`.

---

### 5. Stage gate approval order is internally inconsistent

**Status:** ✅ DONE (2026-05-02) — mandatory HITL stages now use `Draft -> Ready for HITL -> Approved`. Pre-HITL gates stop after prompting and waiting; post-HITL gates require recorded prompt and user response evidence before proceeding.

**Problem:** `asdlc-stage-gates` requires primary artifacts to have `Status: Approved` before a gate passes, then says to proceed to HITL after the gate passes. Stage skills such as `asdlc-inception` say artifacts become `Approved` only after HITL. This creates two bad outcomes:
- **Deadlock** — an agent cannot pass the gate because HITL has not happened yet.
- **Premature self-approval** — an agent marks the artifact `Approved` before user approval just to satisfy the gate.

**Affected Files:**
- `src/agentic_sdlc/skills/asdlc-stage-gates/SKILL.md`
- `src/agentic_sdlc/skills/asdlc-inception/SKILL.md`
- `src/agentic_sdlc/skills/asdlc-tech-architecture/SKILL.md`
- `src/agentic_sdlc/skills/asdlc-story-breakdown/SKILL.md`

**Fix:** Split every approval gate into two explicit states:
1. **Pre-HITL gate:** artifact is complete and reviewable, with `Status: Draft` or `Ready for Review`.
2. **Post-HITL approval gate:** user response is recorded, `hitl_response` is present, and artifact status is updated to `Approved`.

The stage-gates skill should never require `Status: Approved` before the mandatory HITL checkpoint has happened.

---

### 6. Implementation flow skips testing before code-review

**Status:** ✅ DONE (2026-05-03) — The transition sequence in `asdlc-implementation` now explicitly includes `asdlc-testing` before `asdlc-code-review`. `asdlc-code-review` requires evidence that testing was completed before allowing the review to proceed. `workflow-greenfield.md` and `workflow-brownfield.md` were also updated to move the "merge" step out of Stage 6 and into Stage 9, reflecting the true flow.

**Problem:** The global workflow says `implementation → critical-review → testing → code-review`, and `asdlc-code-review` says it runs after testing is complete. But `asdlc-implementation` transitions directly from critical-review to code-review and then merge. This contradiction lets agents bypass the testing stage even if `asdlc-testing` exists.

**Affected Files:**
- `src/agentic_sdlc/skills/asdlc-implementation/SKILL.md`
- `src/agentic_sdlc/skills/asdlc-code-review/SKILL.md`
- `src/agentic_sdlc/skills/asdlc-testing/SKILL.md`
- `docs/workflow-greenfield.md`
- `docs/workflow-brownfield.md`

---

### 7. Test and coverage claims can be fabricated

**Problem:** The dummy app records test pass counts and coverage, but the repo lacks runnable Android build files (`gradlew`, `build.gradle`, `settings.gradle`). A written claim like "1 passing test, 100% coverage" is not enough. Gate checks currently trust handwritten results too much.

**Affected Files:**
- `src/agentic_sdlc/skills/asdlc-context-harvest/SKILL.md`
- `src/agentic_sdlc/skills/asdlc-testing/SKILL.md`
- `src/agentic_sdlc/skills/asdlc-code-review/SKILL.md`
- `src/agentic_sdlc/skills/asdlc-stage-gates/SKILL.md`

**Fix:** Require evidence for every test/coverage claim:
- exact command run
- exit code
- timestamp
- summary output pasted into the artifact or linked to a CI artifact
- coverage report path, if coverage is claimed

If the command cannot run, the gate must fail or record an explicit HITL acceptance of unverifiable test status.

---

## Tier 2 — High (Gate enforcement gaps — artifacts required but never verified)

### 8. `data-domain.md` never written

**Current status:** Partially valid. The current implementation-planning gate requires the file, but the Scale Guide says tiny single-module projects may have no interface contracts. That can be misread as "no `data-domain.md` file required," while downstream skills still read it.

**Problem:** `asdlc-implementation-planning` requires writing `docs/architecture/data-domain.md` (interface contracts). It was never created. Three downstream skills reference it (`asdlc-critical-review`, `asdlc-implementation`, `asdlc-troubleshooting`), so they silently operated without locked contracts.

**Affected File:** `src/agentic_sdlc/skills/asdlc-implementation-planning/SKILL.md`

**Fix:** Add to gate as hard blocker: `[ ] data-domain.md written to docs/architecture/ — even if "No cross-module contracts" for tiny projects`. Scale Guide should allow a one-liner but the file must physically exist.

---

### 9. `task-graph.md` and EPIC manifest never written

**Current status:** Mostly covered in current skill text. Keep this as an evidence-backed gate concern: the skill now requires these files, but the dummy exercise shows agents can still skip them unless gates require physical-file verification.

**Problem:** `asdlc-story-breakdown` requires `docs/sdlc/epics/task-graph.md` and an EPIC manifest. Neither was produced. The critical-review reads `task-graph.md` as input, so the adversarial review operated without the full dependency picture.

**Affected File:** `src/agentic_sdlc/skills/asdlc-story-breakdown/SKILL.md`

**Fix:** Add to gate: `[ ] task-graph.md physically exists at docs/sdlc/epics/task-graph.md`. Scale Guide: "Tiny: flat story list, no DAG — but file must exist."

---

### 10. Workspace file never created during implementation

**Problem:** The implementation skill says "Copy `workspace-template.md` to `docs/sdlc/workspaces/workspace-STORY-[ID].md`." This was never done. Token logging depends on this file. The gate checks "Token usage logged in workspace YAML" without verifying the file exists.

**Affected File:** `src/agentic_sdlc/skills/asdlc-implementation/SKILL.md`

**Fix:** Add to gate: `[ ] Workspace file exists at docs/sdlc/workspaces/workspace-STORY-[ID].md with YAML fields populated`.

---

### 11. BRD status never updated from "Draft" to "Approved"

**Current status:** Partially fixed but entangled with Tier 1 item 5. Inception now says to update status after approval, and stage-gates require approved status, but the approval-order conflict still enables either deadlock or self-approval.

**Problem:** The inception checklist says "Update status to Approved." It stayed `Draft` the entire lifecycle. The `asdlc-stage-gates` skill says "Ensure the primary artifact has Status: Approved" but the inception gate doesn't explicitly check this.

**Affected Files:**
- `src/agentic_sdlc/skills/asdlc-inception/SKILL.md`
- `src/agentic_sdlc/skills/asdlc-stage-gates/SKILL.md`

**Fix:** Add to inception gate: `[ ] BRD status field is set to 'Approved'`. Add general rule to stage-gates: "After HITL approval, immediately update artifact Status to Approved and commit."

---

### 12. ADR files never written to `docs/architecture/adrs/`

**Current status:** Mostly covered in current skill text. Keep this as an evidence-backed gate concern: tech-architecture now requires ADR files, but the dummy exercise skipped them.

**Problem:** The tech-architecture listed 3 ADRs in a summary table, but no individual ADR files were created in `docs/architecture/adrs/`. The skill provides an `adr-template.md` that was never used.

**Affected File:** `src/agentic_sdlc/skills/asdlc-tech-architecture/SKILL.md`

**Fix:** Add to gate: `[ ] ADR files exist at docs/architecture/adrs/ADR-NNN.md for each decision — OR Scale Guide permits fewer (rationale documented)`.

---

### 13. Story identity drift is not caught

**Problem:** In the dummy app, `STORY-002` means "Implement Local Persistence" in `implementation-plan.md`, but later means "Add Quote Categories" in the BRD append and brownfield tech plan. Story IDs must be immutable; otherwise review, test, branch, and retrospective artifacts can refer to different work under the same ID.

**Affected Files:**
- `src/agentic_sdlc/skills/asdlc-story-breakdown/SKILL.md`
- `src/agentic_sdlc/skills/asdlc-brownfield-brainstorm/SKILL.md`
- `src/agentic_sdlc/skills/asdlc-brownfield-tech-plan/SKILL.md`
- `src/agentic_sdlc/skills/asdlc-implementation/SKILL.md`

**Fix:** Add a story registry or require `task-graph.md` to be the canonical ID index. Every stage that creates or updates story-scoped artifacts must verify:
- story ID exists exactly once
- title matches the canonical title
- status transition is valid
- artifact filename, branch name, workspace, review files, and commits all use the same ID

---

### 14. Architecture and context claims can drift from repository reality

**Problem:** The dummy app docs claim Compose, Hilt, Room, Retrofit, SQLite, Gradle, and runnable tests, but the repo only contains a small Kotlin source tree with no Android build files. Architecture docs must distinguish planned architecture from implemented/current architecture.

**Affected Files:**
- `src/agentic_sdlc/skills/asdlc-context-harvest/SKILL.md`
- `src/agentic_sdlc/skills/asdlc-tech-architecture/SKILL.md`
- `src/agentic_sdlc/skills/asdlc-code-review/SKILL.md`

**Fix:** Add a repository-reality verification step:
- stack claims must be backed by build/config files or marked `planned`
- context-harvest must label each technology as `present`, `planned`, or `not found`
- code-review must fail documentation if README/architecture run commands do not work

---

### 15. Retrospective requirement fidelity can be declared without evidence

**Problem:** The dummy retrospective marks `FR-001` as fully implemented even though the code only defines a data model and repository interface. No implementation fetches one quote every 24 hours. The retrospective currently has no hard requirement to trace fidelity claims to actual tests and code.

**Affected Files:**
- `src/agentic_sdlc/skills/asdlc-retrospective/SKILL.md`
- `src/agentic_sdlc/skills/asdlc-critical-review/SKILL.md`
- `src/agentic_sdlc/skills/asdlc-testing/SKILL.md`

**Fix:** Require every retrospective fidelity row to include evidence:
- story ID(s)
- acceptance criterion ID(s)
- passing test command or test name
- source file reference
- unresolved gap, if any

If evidence is missing, the fidelity status must be `partial` or `not implemented`, never `complete`.

---

### 16. Story status is marked `DONE` too early

**Problem:** `asdlc-implementation` marks a story `DONE` before critical-review, testing, and code-review. That makes "done" mean "locally implemented" rather than "accepted and merged." Gates and dashboards can then overstate progress.

**Affected Files:**
- `src/agentic_sdlc/skills/asdlc-implementation/SKILL.md`
- `src/agentic_sdlc/skills/asdlc-story-breakdown/story-template.md`
- `docs/workflow-greenfield.md`
- `docs/workflow-brownfield.md`

**Fix:** Introduce explicit story states, for example:

```
TO_DO → IN_PROGRESS → IMPLEMENTED → CRITICAL_REVIEWED → TESTED → APPROVED → MERGED
```

Only set `DONE` or `MERGED` after the configured merge target receives the story and final regression passes.

---

### 17. Canonical task graph can go stale during implementation

**Problem:** Workflow docs say implementation marks stories complete in `task-graph.md`, but the implementation skill only updates the story file. If the task graph is the dependency source of truth, it must be updated when story status changes.

**Affected Files:**
- `src/agentic_sdlc/skills/asdlc-implementation/SKILL.md`
- `src/agentic_sdlc/skills/asdlc-story-breakdown/SKILL.md`
- `docs/workflow-greenfield.md`

**Fix:** Define one canonical status source:
- Option A: `task-graph.md` is canonical and story files are detail pages.
- Option B: story files are canonical and `task-graph.md` is regenerated/updated from them.

Then update implementation gates to verify both views are synchronized.

---

### 18. No safe command to update installed project skills

**Problem:** `asdlc init` copies packaged skills into a target project at `.agents/skills/`. After the framework is upgraded, existing projects have no safe, explicit command to refresh only those installed skills. The only obvious workaround is `asdlc init --force`, but that is too broad because it can overwrite initialized project files such as `AGENTS.md` and docs stubs.

**Affected Files:**
- `src/agentic_sdlc/cli.py`
- `tests/test_cli.py`
- `README.md`
- `docs/installation.md`
- `docs/getting-started.md`

**Fix:** Add a dedicated command:

```bash
asdlc update-skills /path/to/your/project
```

Expected behavior:
- refresh `.agents/skills/` from the currently installed Agentic SDLC package
- preserve project `docs/` artifacts
- preserve project-specific `AGENTS.md` context by default
- print the old and new skill versions or at least a changed-file summary
- support `--dry-run` to show what would change
- support `--include-agents` to update the base `AGENTS.md` template while preserving the `## Project Context` block
- support `--force` only for deliberate overwrite of local skill edits

Recommended post-upgrade workflow for users:

```bash
python -m pip install --upgrade agentic-sdlc
asdlc update-skills /path/to/your/project --dry-run
asdlc update-skills /path/to/your/project
```

Add tests proving `update-skills` updates `.agents/skills/` without modifying `docs/` or destroying project-specific `AGENTS.md` content.

---

## Tier 3 — Nice to Have (Quality & polish improvements)

### 19. `critical-review.md` and `code-review.md` overwrite on each story

**Current status:** Partially valid. `critical-review.md` is still a fixed path and retrospective reads only that file. Code-review is less fixed now, but review history can still be lost.

**Problem:** Both files get overwritten per story, losing review history. The retrospective skill reads the critical review file, so previous stories' findings are lost.

**Fix:** Use story-scoped filenames: `critical-review-STORY-NNN.md` and `code-review-STORY-NNN.md`. Update the retrospective skill to glob-read `critical-review-*.md`.

---

### 20. Domain model has no template

**Problem:** `asdlc-inception` says "Write domain-model.md" but provides no template (unlike BRD which has `brd-template.md`). The domain model was freeform — no Status/Version frontmatter, no field types, no relationships section.

**Fix:** Add a `domain-model-template.md` with sections for entities (with field types), relationships, bounded contexts, glossary, and Status/Version frontmatter.

---

### 21. Brownfield BRD appending creates a growing log

**Problem:** `asdlc-brownfield-brainstorm` says "append a story section to brd.md." Over time the BRD mixes project-level requirements with story-level brainstorms, becoming an append-only log.

**Fix:** Use separate files: `docs/product/features/story-brd-STORY-NNN.md`. Or add a `## Story Brainstorms` delimiter section to the BRD template.

---

### 22. `accessibility.md` never written as a separate file

**Current status:** Mostly covered in current skill text. Keep this only as a historical exercise finding unless a future run shows the current gate still lets agents inline accessibility.

**Problem:** The design-system skill says "Write `docs/product/accessibility.md`" but accessibility was inlined into `design-system.md`. The brownfield-design skill references it as an update target, so brownfield stages skip accessibility deltas.

**Fix:** Either enforce separate file in gate, or update all references to accept accessibility as a section within `design-system.md`. Add Scale Guide row.

---

### 23. No "When to Skip" guidance for `asdlc-ui-mockups`

**Current status:** Partially valid. The skill has "When to Use," and workflow docs mention skip cases, but the skill itself still lacks an explicit skip section and skip artifact rule.

**Problem:** `asdlc-design-system` says "invoke ui-mockups if redesign." But the mockups skill itself has no "When to Skip" section, unlike design-system which has one. It's unclear for brand-new tiny projects whether mockups are needed.

**Fix:** Add "When to Skip" section: skip if purely backend, if design-system provides sufficient direction for tiny project, or if UI is standard CRUD with no visual ambiguity. Document skip decision in `docs/product/mockups.md`.

---

### 24. No gate catches domain model drift after brownfield changes

**Problem:** When STORY-002 added `category` to `Quote`, `domain-model.md` was NOT updated. No skill or gate catches this. Over multiple stories, the domain model goes stale.

**Fix:** Add to `asdlc-implementation` checklist: `[ ] docs/architecture/domain-model.md updated if any entity field was added/removed/renamed`. Or add to critical-review under "Integration": `[ ] domain-model.md still reflects implemented entities`.

---

### 25. Story template YAML is richer than what agents produce

**Problem:** The `story-template.md` has fields like `epic_id`, `milestone`, `track`, `depends_on`, `owner`, `branch`, etc. In practice agents only fill `story_id`, `status`, `complexity`, `risk`. No gate enforces the full template.

**Fix:** Add Scale Guide: "Tiny: only story_id, status, complexity, risk required. Small+: full template." Don't enforce unused fields on small projects.
