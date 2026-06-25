# CashUPI Review Findings and ASDLC Improvement Notes

> Date: 2026-05-12
> Scope: Lessons extracted from reviewing the `cash-upi` app as an Agentic SDLC project, with emphasis on multi-agent execution, end-stage drift, prompt quality, and framework gaps.

## Why this note exists

This document captures what was learned from reviewing the CashUPI repository as an ASDLC-driven build. The goal is not to re-review the app itself. The goal is to extract concrete framework lessons that can improve Agentic SDLC for future multi-agent projects.

## Review context

- The reviewed project was an existing codebase that contained a substantial ASDLC artifact trail:
  - BRD
  - architecture docs
  - epics and story files
  - workspaces
  - test plans
  - critical review and code review notes
  - handoff notes
- The project appears to have been built with multiple agents contributing across implementation, docs, and review stages.
- The strongest concern from the review was that the ending stages were weaker than the planning and implementation stages.

## What worked well

- ASDLC produced useful early and mid-stage structure.
- The repository had visible evidence of requirements thinking before implementation.
- Story decomposition was present and generally understandable.
- Workspaces and story files made it easier to reconstruct intent.
- The framework clearly helped with planning discipline more than ad hoc prompting alone would have.

## Main findings

### 1. Front-half discipline was stronger than end-stage discipline

The repo showed solid planning artifacts, but weaker closure discipline. The problem was not "no process." The problem was that the final stages became easier to drift away from repo reality.

Observed pattern:
- planning docs existed
- implementation notes existed
- reviews existed
- handoff existed
- but final truth across these artifacts was not consistently reconciled

### 2. The most important gap was stale or false green evidence

Several closing artifacts claimed green status while current repo checks were not fully green at review time.

Examples from the reviewed repo state:
- Story/task graph status drift existed.
- Review and handoff documents reported clean verification that no longer matched current repo reality.
- Full-suite regression and audit truth were weaker than some story-level documents implied.

Core lesson:
- ASDLC records evidence, but it does not yet enforce evidence freshness strongly enough.

### 3. Multi-agent execution likely amplified the drift

Multi-agent work does not inherently cause failure, but it raises the cost of keeping a single source of truth.

Likely failure mode:
- one agent updated code
- another agent updated a story file
- another agent updated the task graph
- another agent wrote handoff/review notes
- nobody owned final reconciliation

That creates a repo that looks procedurally complete while being operationally inconsistent.

### 4. Status reconciliation is too weak in the current framework

The framework expects artifacts to be updated, but the practical enforcement of cross-artifact consistency is not yet strong enough.

The important consistency links are:
- story frontmatter status
- task graph status
- review verdicts
- test-plan status
- handoff claims
- actual repo verification commands

If any one of these says "green" while another says "not done" or the repo itself is red, the stage should fail immediately.

### 5. Prompt quality clearly matters, but it did not replace framework needs

One repeated lesson from the CashUPI review was that good prompts often help agents perform better than vague ASDLC usage.

That does not mean prompt-only is enough.

What prompts improved:
- scope sharpness
- acceptance criteria clarity
- ownership clarity
- reduced drift during implementation

What prompts did not replace:
- artifact trail
- stage ordering
- HITL checkpoints
- gate enforcement
- reconciliation after multiple agents contribute

The conclusion is not "prompting is better than ASDLC." The conclusion is "ASDLC should embed stronger prompt patterns inside the stages."

## Exact framework lessons

### Lesson 1: planning support is already useful

Agentic SDLC is already good at:
- forcing up-front decomposition
- making work visible
- producing artifacts that survive beyond chat memory

This part should be preserved.

### Lesson 2: closure support is under-specified

Agentic SDLC is weaker at:
- proving that evidence is current
- reconciling multiple artifacts
- preventing "paper green / repo red"
- defining who owns the final truth in multi-agent runs

This is the main area that needs improvement.

### Lesson 3: multi-agent mode needs explicit framework support

The current skills assume disciplined execution, but they do not define enough operational rules for parallel or distributed agent work.

A future multi-agent skill should define:
- implementation owner
- doc owner
- verification owner
- closure owner
- rules for who may update story status
- rules for who may declare a story tested/approved/merged

### Lesson 4: retrospective needs to extract process failures more aggressively

Retrospectives should not stop at "what went well / what went badly." They should explicitly ask:
- where did repo truth and doc truth diverge
- which stage allowed stale evidence to pass
- whether multiple agents contributed to closure drift
- which skill should be changed because of the failure

## Recommended ASDLC improvements

### Strengthen `asdlc-stage-gates`

Add hard-fail checks for:
- story status and task-graph status mismatch
- review verdict that is inconsistent with current command results
- handoff claims that are not backed by recorded evidence
- stale evidence older than relevant code changes
- epic/story marked merged while prerequisite artifacts remain incomplete

### Strengthen `asdlc-testing`

Add explicit rules:
- targeted tests can support a story, but cannot override a failing full regression
- evidence must include command, exit code, timestamp, and summary output
- evidence is invalid if it predates relevant touched-file changes
- `TESTED` cannot be set when full-suite regressions are red

### Strengthen `asdlc-code-review`

Require the reviewer to:
- run the current repo checks directly
- compare doc claims against repo reality
- treat stale or false verification claims as review findings
- fail the review when "docs green / repo red" is detected

### Strengthen `asdlc-retrospective`

Require explicit sections for:
- process failures
- stale evidence or false confidence
- multi-agent coordination failures
- skills to add or revise

### Strengthen `asdlc-implementation`

Add a multi-agent subsection with rules such as:
- one story has one closure owner
- only the closure owner can mark final story state transitions
- no agent may mark `APPROVED`, `TESTED`, or `MERGED` based only on another agent's report
- final verification must be re-run by the closure owner

## Recommended new skill

## `asdlc-multi-agent-coordination`

Suggested trigger:
- Use when more than one agent is working on the same epic, milestone, or tightly coupled set of stories.

Suggested responsibilities:
- assign ownership boundaries
- assign artifact ownership
- define the canonical source of truth
- define reconciliation rules before merge
- serialize final closure even if implementation was parallel

Suggested hard rules:
- one story, one closure owner
- status changes require local verification by the closure owner
- handoff claims must be backed by a recorded evidence artifact
- parallel implementation is allowed; final gate evaluation is serialized

## Recommended prompt-template improvements

Existing ASDLC skills would benefit from small prompt blocks inside the skill body.

Examples:

### Implementation prompt template

"Implement `STORY-[ID]` only. Limit touched files to the story's declared ownership boundary. Write failing tests first, record the RED result, then implement the minimum change to pass. Do not update story status, task graph, review docs, or handoff until full verification passes."

### Testing prompt template

"Run the current verification commands now. Record exact command, timestamp, exit code, and summary output. If full regression fails, do not mark the story `TESTED` even if targeted tests pass."

### Code-review prompt template

"Review adversarially. Compare current repo results against story docs, test plan, review notes, and handoff claims. Flag stale evidence, false green claims, status drift, and missing reconciliation."

### Multi-agent closure prompt template

"You are the closure owner for `STORY-[ID]`. Re-run verification yourself. Reconcile story file, task graph, review notes, test plan, and handoff. If any artifact disagrees with repo reality, fail closure and correct the artifacts before approval."

## High-confidence conclusion

The CashUPI review did not show that Agentic SDLC is ineffective. It showed that Agentic SDLC is stronger at initiation and decomposition than at end-stage reconciliation.

The framework already helps agents think before coding. The next improvement should focus on making it harder for a project to appear complete when its final evidence is stale, inconsistent, or owned by too many agents without a single closer.

## Useful comparison set for future analysis

To refine these conclusions, it would be useful to compare:
- one repo where ASDLC worked well end to end
- one repo where multi-agent coordination caused closure drift
- one repo built mostly through prompting without strong stage discipline

That comparison would make it easier to separate:
- framework strengths
- framework gaps
- prompt quality effects
- multi-agent coordination effects
