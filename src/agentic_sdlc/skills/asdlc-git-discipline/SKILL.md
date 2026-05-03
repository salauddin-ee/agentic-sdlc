---
name: asdlc-git-discipline
description: Use when performing ANY git operation — commits, branch creation, merges — throughout the SDLC. Defines exactly when and how to commit at every stage boundary, HITL checkpoint, and story lifecycle point.
version: 1.0.0
---

Every code change and every approved artifact must be committed. No work exists unless it is in git.

## The Iron Law

```
NO APPROVED ARTIFACT OR COMPLETED STORY WITHOUT A GIT COMMIT.
```

This applies to docs, code, configuration — everything. If it isn't committed, it didn't happen.

## Branch Strategy

Read `docs/architecture/coding-standards.md` before any story branch or merge. The project must have a `## Merge strategy` section written during `asdlc-implementation-planning`.

If the section is missing or ambiguous, use **Epic branch** as the default. Do not assume direct-to-main.

| Branch type | Naming | Purpose | Merged after |
|---|---|---|---|
| Stage artifact branch | `docs/{stage-name}` | Holds stage outputs until HITL approval | HITL approval |
| Epic integration branch | `feature/EPIC-{ID}` | Default target where completed stories accumulate before `main` | Full regression + HITL approval |
| Story feature branch | `feature/STORY-{ID}-{short-desc}` | Holds implementation work for one story | Code-review PASS into the configured target |

Supported merge strategies:

| Strategy | When to use | Story merge target | `main` merge rule |
|---|---|---|---|
| Epic branch (default) | Safe default for solo or team work | `feature/EPIC-{ID}` | Only after full regression on the epic branch and explicit HITL approval |
| Direct to main | Solo-dev fallback only when the user explicitly selected it | `main` | Each story may squash-merge after code-review PASS |
| PR-based | Team workflow with CI and remote review | Remote PR target recorded in coding standards, commonly `main` | Merge only through the PR system after CI/review |

`main` only ever contains **approved** content:
- Stage artifacts merged in after HITL sign-off
- Epic branches merged in after full regression and HITL sign-off
- Direct story merges only when the user explicitly selected Direct to main
- PR merges only when the configured PR workflow passes

Never commit directly to `main`. Always go through the configured branch or PR flow.

## Stage Artifact Protocol

Each planning/documentation stage (asdlc-inception, asdlc-design-system, asdlc-ui-mockups, asdlc-tech-architecture, asdlc-implementation-planning, asdlc-story-breakdown) follows this pattern:

```
1. Create branch:
   git checkout main
   git pull origin main
   git checkout -b docs/{stage-name}
   # e.g. docs/inception, docs/ui-mockups, docs/tech-architecture

2. Do the stage work (write artifacts to docs/)

3. When stage gate PASSES — commit all artifacts:
   git add docs/
   git commit -m "docs({stage-name}): stage complete — gate passed"

4. HITL checkpoint — human reviews the branch diff:
   (human reviews and approves)

5. After HITL approval — merge to main:
   # Option A: Team Workflow (PR)
   git push origin docs/{stage-name}
   # -> Create PR on GitHub/GitLab
   # -> Squash merge via PR UI
   # -> git checkout main && git pull origin main

   # Option B: Solo Workflow (Local Merge)
   git checkout main
   git merge --squash docs/{stage-name}
   git commit -m "docs({stage-name}): approved — merge to main"
   git branch -d docs/{stage-name}
```

**If HITL requests changes:** make changes on the same branch, re-commit, request HITL again. Do not merge until approved.

## Story Implementation Protocol

Each story follows this pattern. When a merge step shows multiple strategies, run **only the strategy selected in `docs/architecture/coding-standards.md`**. Do not run the other strategy examples.

```
1. Read docs/architecture/coding-standards.md → ## Merge strategy.
   Missing section = Epic branch default.

2. Ensure the merge target exists:
   Epic branch: create or update feature/EPIC-{ID} from main before the first story:
     git checkout main
     git pull origin main
     git checkout -B feature/EPIC-{ID}
   Direct to main: use main as the target only if explicitly selected.
   PR-based: use the configured PR base branch.

3. Create feature branch (at story start) from the configured target:
   # Epic branch default
   git checkout feature/EPIC-{ID}
   git pull origin feature/EPIC-{ID}  # if remote exists
   git checkout -b feature/STORY-{ID}-{short-desc}

4. Implement the story (TDD: RED → GREEN → REFACTOR)
   — all work stays on the feature branch throughout

5. When story is complete (all tasks done, tests green, security checked):
   git add .
   git commit -m "{type}(STORY-{ID}): {story title}"
   # type = feat | fix | refactor depending on the story nature

6. After code-review PASS — merge according to the configured strategy. Run exactly one of these paths:

   # Strategy A: Epic branch (default)
   git checkout feature/EPIC-{ID}
   git merge --squash feature/STORY-{ID}-{short-desc}
   git commit -m "feat(STORY-{ID}): {story title}"
   git branch -d feature/STORY-{ID}-{short-desc}

   # Strategy B: Direct to main (explicit solo-dev opt-in only)
   git checkout main
   git pull origin main
   git merge --squash feature/STORY-{ID}-{short-desc}
   git commit -m "feat(STORY-{ID}): {story title}"
   git branch -d feature/STORY-{ID}-{short-desc}
   git push origin main

   # Strategy C: PR-based
   git push origin feature/STORY-{ID}-{short-desc}
   # -> Create PR against the configured base branch
   # -> CI runs, team reviews
   # -> Merge only through the PR system
```

**One squash commit per story on the configured merge target.** The feature branch can have intermediate commits during development, but the target branch receives one clean squash commit per story.

## Epic Finalization Protocol

Use this protocol when the configured merge strategy is **Epic branch**.

```
1. Confirm every story in the epic has code-review PASS and is merged into feature/EPIC-{ID}.
2. Run full regression on feature/EPIC-{ID}. Record command, exit code, and summary in docs/sdlc/test-plans/test-plan.md.
3. Invoke asdlc-hitl-protocol:
   HITL REQUIRED
   Stage: epic-finalization
   Question: All stories are merged into feature/EPIC-{ID} and full regression passed. Approve merge to main?
   Context: Include test command, exit code, summary, and changed story list.
   Options: [A] Approved — squash merge feature/EPIC-{ID} to main
            [B] Hold — do not merge; I will request changes
   Default if no response: Wait for explicit approval
4. Only after explicit approval:
   git checkout main
   git pull origin main
   git merge --squash feature/EPIC-{ID}
   git commit -m "feat(EPIC-{ID}): complete {epic title}"
   git push origin main
```

## Commit Message Format

Use Conventional Commits:

```
{type}({scope}): {short description}

Types:  feat | fix | refactor | test | docs | chore
Scope:  STORY-{ID} | {stage-name} | {module-name}

Examples:
  feat(STORY-042): add user authentication endpoint
  docs(asdlc-inception): stage complete — gate passed
  docs(asdlc-tech-architecture): approved — merge to main
  fix(STORY-017): handle null user in session validator
```

Rules:
- Description is lowercase, present tense, imperative mood: "add" not "added"
- Max 72 characters on the first line
- No period at end

## Mandatory Commit Points

These are non-negotiable. Missing any of these is a process violation:

```
[ ] Branch created at the START of every stage and every story
[ ] Epic branch strategy: feature/EPIC-{ID} exists before the first story branch is created
[ ] Stage artifacts committed before HITL is requested
[ ] Decision recorded after HITL response (docs update committed)
[ ] Story committed before requesting critical-review
[ ] Story merged according to the configured merge strategy after code-review PASS
[ ] Epic branch strategy: full regression and HITL approval completed before merging epic to main
[ ] Feature/docs branch deleted after successful merge
```

## Handling Regressions

If a commit is found to have introduced a bug or broken a test:

```
DO:    git revert {sha}         ← creates a new revert commit, safe
DON'T: git reset --hard {sha}  ← rewrites history, dangerous on shared branches
```

Then fix the issue, re-commit, re-run the stage gate.

## HITL Commit Pattern

Before requesting HITL — always commit current state first:

```
git add .
git commit -m "wip({stage}): pre-HITL checkpoint — {brief context}"
```

After HITL decision is received and recorded in the artifact:

```
git add docs/
git commit -m "docs({stage}): HITL decision recorded — {option chosen}"
```

## Gate

Before exiting any stage or story, verify:

```
[ ] Working branch exists (not on main)
[ ] All changes committed (git status shows clean working tree)
[ ] Commit message follows Conventional Commits format
[ ] All committed files are in the expected location (docs/ for artifacts, src/ for code)
[ ] Merge strategy read from docs/architecture/coding-standards.md, or Epic branch default applied
[ ] Branch will be merged via HITL approval (docs), code-review PASS into the configured target (stories), or PR workflow
```

## Red Flags

| Thought | Reality |
|---|---|
| "I'll commit at the end of the session" | Sessions crash. Commit now. |
| "It's just a docs change — no need for a branch" | Docs branches enable human diff review at HITL. Always branch. |
| "I'll push directly to main to save time" | main is the record of approved work. Unreviewed pushes corrupt it. |
| "Direct to main is simpler, so I'll use it by default" | Direct to main is an explicit solo-dev opt-in. Missing configuration means Epic branch. |
| "Story tests passed, so the epic can go to main" | Story tests do not prove integrated stories work together. Run full regression on the epic branch and request HITL. |
| "I'll skip the squash merge — too many commands" | Squash merge is what makes the target branch readable. Run the commands. |
| "The revert will lose my work" | Revert preserves history. Hard reset destroys it. |
