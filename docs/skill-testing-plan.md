# Skill Testing Plan

## Goal

Build the smallest useful verification loop for Agentic SDLC skills:

- catch structural mistakes in `SKILL.md` files
- catch drift across skills, templates, docs, and CLI bootstrap behavior
- catch regressions in the highest-risk discipline skills

This plan intentionally avoids a large benchmark platform or broad model-scoring system.

## Eval-Driven Skill Improvement

Evals do not just verify skills — they **drive skill quality**. The workflow mirrors TDD:

```
NO SKILL CHANGE WITHOUT A FAILING EVAL FIRST.
```

### The Loop

```
1. Write eval → define the ideal behavior you want from the skill
2. Run eval  → the current skill may fail (that is expected and good)
3. Fix skill → improve the skill text until the eval passes
4. Commit    → the eval now permanently guards against regression
5. Repeat    → new failure pattern observed? Add a fixture first, then fix the skill
```

### Why Order Matters

| Approach | Risk |
|---|---|
| Fix skills first, add evals after | Evals just rubber-stamp the current state — they prove nothing |
| Build evals that match current skills | You are codifying the status quo, not improving it |
| **Write evals to ideal behavior, fix skills to pass** | Evals drive improvement and guard against regression |

### What "Ideal Behavior" Means

For each eval, ask: *"If an agent follows this skill perfectly, what would be unambiguously true?"*

- The skill text **must contain** explicit refusal language for the shortcut pattern
- The skill text **must not** leave room for rationalization on gate-crossing
- The skill text **must reference** the correct artifact paths and templates

Write the assertion first. Then look at the current skill. If it falls short — fix it.

### Built-In Fix Passes

Each milestone below includes a fix pass:

| Milestone | Eval layer | Fix pass |
|---|---|---|
| Phase 1 | Static validation | Fix all structural issues in skills before proceeding to Phase 2 |
| Phase 2 | Consistency checks | Fix all path/reference drift before proceeding to Phase 3 |
| Phase 3–4 | Scenario evals | Write evals to ideal behavior; fix skills that fall short |
| Phase 5 | Regression capture | Add fixture first, then fix the skill |

> A milestone is not complete until its eval layer passes **and** any skill improvements it surfaces have been made.

## Scope

### Do now

1. Static validation for every `SKILL.md`
2. Cross-file consistency checks
3. Small scenario eval suite for the highest-risk skills
4. Regression cases for failures already observed in real use

### Do not do now

1. Large benchmark infrastructure
2. Broad model scoring dashboards
3. Dozens of evals for every skill before the basics work

## Phase 1: Static Validator

Add a validator that checks every skill file for:

1. Valid YAML frontmatter
2. Required fields: `name`, `description`, `version`
3. Description rules:
   - starts with `Use when...`
   - describes trigger conditions, not workflow
4. Required sections where applicable:
   - main body content
   - `## Gate` for gated skills
   - `## Red Flags` for discipline-oriented skills
5. Broken or inconsistent skill references
6. Placeholder content such as `TODO`, `TBD`, or `fill in later`

## Phase 2: Cross-File Consistency Checks

Add checks that compare:

1. Skill instructions vs. templates
2. Skill instructions vs. README/docs
3. Skill instructions vs. CLI-generated project structure
4. Referenced artifact paths vs. actual intended file locations

Examples of the consistency problems this should catch:

- `docs/sdlc/...` vs `docs/architecture/...` / `docs/product/...`
- `coding-constitution.md` vs `coding-standards.md`
- `interface-contracts.md` vs `data-domain.md`
- references to non-existent bootstrap scripts

## Phase 3: Initial Scenario Eval Suite

Start with only these five skills:

1. `asdlc-using-agentic-sdlc`
2. `asdlc-implementation`
3. `asdlc-stage-gates`
4. `asdlc-hitl-protocol`
5. `asdlc-git-discipline`

For each skill, create 2-4 fixtures covering:

1. Normal compliant case
2. Shortcut-pressure case
3. Ambiguity case
4. Conflicting-instruction case where relevant

## Eval Rubric

Each scenario should check for:

1. Correct skill selection
2. Correct sequence of required steps
3. Gate or HITL compliance
4. Required artifact creation or update
5. Refusal of invalid shortcut behavior

Use pass/fail assertions first. Do not add complex scoring yet.

## Phase 4: Lightweight Eval Harness

Implement a simple local harness that:

1. Loads a scenario fixture
2. Runs the evaluation flow
3. Captures output
4. Applies rule-based assertions
5. Writes a pass/fail result with failure reasons

Keep the harness file-based and minimal. Optimize for maintainability, not scale.

## Phase 5: Regression Capture

Whenever a real failure is seen:

1. Add the exact failure pattern as a fixture
2. Add the expected correct behavior
3. Re-run the suite
4. Update the relevant skill if the instructions were too weak or ambiguous

Observed failures should become permanent regression cases.

## CLI Surface

> **Note:** `validate-skills` and `eval-skills` are internal dev subcommands on the `asdlc-dev` CLI (`asdlc-dev validate-skills`, `asdlc-dev eval-skills`). They are not exported in the public `asdlc` CLI.

## CI Rollout

Roll out in this order:

1. Run static validation in CI first
2. Add scenario evals after the harness is stable
3. Block merges on validator failures
4. Decide later whether scenario eval failures should be blocking

## Immediate Priority Order

1. Implement static validator
2. **Run it — fix all skill issues it surfaces** (fix pass)
3. Implement cross-file consistency checks
4. **Run it — fix all drift it surfaces** (fix pass)
5. Add the 5-skill scenario suite (write evals to ideal behavior first)
6. **Fix skills that fail the scenario evals** (fix pass)
7. Start capturing regressions from real failures

## Success Criteria

This plan is successful when:

1. path and artifact drift is caught automatically
2. the highest-risk skills have repeatable regression coverage
3. adding or editing a skill has a clear validation workflow
4. the framework gains confidence without adding heavy infrastructure
5. every known skill weakness surfaced by an eval has been fixed in the skill text
6. the eval-driven improvement loop is the default workflow for all future skill changes
