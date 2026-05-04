---
name: asdlc-implementation-planning
description: Use when you have approved architecture and need to create a machine-readable execution plan before implementation begins.
version: 1.1.0
---

Produce a concrete execution plan that deconstructs the architecture into milestones, defines interface contracts before parallel work begins, identifies risks, and establishes a clear definition of done.

<HARD-GATE>
Do NOT begin implementation (Stage 6) until this plan is approved. All inter-module interface contracts must be locked in this stage — not discovered during implementation.
</HARD-GATE>

## Checklist

1. **Read inputs**: `docs/product/features/brd.md`, `docs/architecture/tech-architecture.md`, `docs/architecture/coding-standards.md`, `docs/product/mockups.md` (if present)
2. **Define milestones** — logical groupings of work with clear exit criteria
3. **Define interface contracts** — every module boundary documented before any code
4. **Write risk log** — likelihood × impact for each identified risk
5. **Write definition of done** — project-level checklist
6. **Write `docs/sdlc/epics/implementation-plan.md`** — using the `implementation-plan-template.md` file in this skill's directory; leave both HITL response field groups blank until each user response is recorded
7. **Ask for merge strategy via HITL** — before story-breakdown or any branch creation
8. **Record merge-strategy HITL evidence** — record `merge_strategy_hitl_prompt`, `merge_strategy_hitl_response`, `merge_strategy_hitl_decision`, `merge_strategy_hitl_approved_by`, and `merge_strategy_hitl_approved_at` in the implementation plan metadata. Do NOT use the plan-approval fields for this answer.
9. **Record merge strategy** — add or update `## Merge strategy` in `docs/architecture/coding-standards.md`
10. **Write `docs/architecture/data-domain.md`** — API contracts, event schemas, type defs
11. **Self-review** — check all FRs from BRD are traceable to a milestone
12. **Set artifact status** — update implementation plan status to `Ready for HITL` before final user approval
13. **Present to user** — get approval
14. **Record plan-approval HITL evidence** — only after explicit approval, populate `plan_approval_hitl_prompt`, `plan_approval_hitl_response`, `plan_approval_hitl_decision`, `plan_approval_hitl_approved_by`, `plan_approval_hitl_approved_at`, and set status to `Approved`. Never overwrite the merge-strategy HITL fields with the plan-approval response.
15. **Transition** — invoke `asdlc-story-breakdown` skill


## Interface Contracts Format

`docs/architecture/data-domain.md`:

```markdown
# Interface contracts

> **Status:** Draft | Ready for HITL | Approved
> **Version:** 0.1.0

## REST endpoints
### POST /api/users
**Request:**
```json
{ "email": "string", "password": "string" }
```
**Response 201:**
```json
{ "id": "uuid", "email": "string", "createdAt": "ISO8601" }
```
**Errors:** 400 (validation), 409 (email exists), 500

## Event schemas
### user.created
```json
{ "userId": "uuid", "email": "string", "timestamp": "ISO8601" }
```

## Shared types / interfaces
[TypeScript interfaces, Zod schemas, or language-equivalent type definitions]
```

## Merge Strategy HITL

Before story-breakdown begins, ask this exact HITL question and wait for an explicit response. If the user does not respond, record option A as the planned default but do not create story branches until the stage is approved.

```text
HITL REQUIRED
Stage: implementation-planning
Question: How should completed stories be merged?
Context: Stories will be broken down and implemented on feature branches.
Options: [A] Epic branch (recommended) — stories merge into feature/EPIC-{ID}, then the epic branch merges to main after full regression + your approval.
         [B] Direct to main — each story squash-merges to main after code-review (solo-dev workflow, no integration branch).
         [C] PR-based — stories push to remote and open PRs against main (team workflow with CI and remote review).
Default if no response: [A] Epic branch
```

Record the answer in `docs/architecture/coding-standards.md`:

```markdown
## Merge strategy

- Selected strategy: Epic branch | Direct to main | PR-based
- Selected by: [human name or "user"]
- Decision date: YYYY-MM-DD
- Rationale: [why this strategy fits the project]
- Epic integration branch: `feature/EPIC-{ID}` (required for Epic branch)
- Main merge approval: HITL required after full regression on the epic branch
```

If `docs/architecture/coding-standards.md` has no `## Merge strategy` section, downstream skills must treat the project as **Epic branch** by default.

## Gate

```
[ ] All milestones have explicit, verifiable exit criteria
[ ] Every FR from brd.md is traceable to at least one milestone
[ ] All inter-module interface contracts defined before story-breakdown begins
[ ] Risk log populated with at least 1 risk (3+ for small/medium/large per Scale Guide)
[ ] Assumptions explicitly listed
[ ] Definition of done agreed with user
[ ] Merge strategy HITL completed and recorded in docs/architecture/coding-standards.md
[ ] Merge-strategy HITL evidence (`merge_strategy_hitl_*` fields) populated in implementation-plan.md metadata
[ ] Plan-approval HITL evidence (`plan_approval_hitl_*` fields) populated in implementation-plan.md metadata before status flips to `Approved`
[ ] Merge-strategy and plan-approval HITL field groups are distinct — neither overwrites the other
[ ] implementation-plan.md physically exists at docs/sdlc/epics/implementation-plan.md
[ ] data-domain.md physically exists at docs/architecture/data-domain.md — even for tiny projects (can contain "No cross-module contracts" with justification)
```

## Red Flags

| Thought | Reality |
|---|---|
| "Interface contracts can be defined as we go" | Parallel work requires contracts upfront. Define them now. |
| "The milestones are obvious" | Undocumented milestones have no exit criteria. Write them. |
| "We don't have enough risks to list" | There are always risks. Identify at least 1 (3+ for larger projects per Scale Guide). |
| "Definition of done is too detailed" | Detailed DoD prevents "it's done... mostly" shipping. |

## Scale Guide

| Project size | Milestones | Interface contracts | Risk log |
|---|---|---|---|
| Tiny (1-day) | 1 milestone, 1-2 exit criteria | None required (file must exist with "None required" rationale) | 1-2 risks |
| Small (1-week) | 2-3 milestones | 1-3 contracts for key boundaries | 3 risks |
| Medium (1-month) | 3-5 milestones with sub-tasks | Full API + event schema | Top 5 risks |
| Large (multi-month) | Full milestone graph with owners | All contracts per ADR | Full risk register with mitigations |
