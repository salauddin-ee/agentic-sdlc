---
name: asdlc-tech-architecture
description: Use when making technology stack or architecture decisions for a project — before any code is written. Also use when a major architectural decision must be made mid-project.
version: 1.0.0
---

Produce a defensible, documented technical architecture before any code is written. Every significant decision gets an ADR. No silent choices.

<HARD-GATE>
Do NOT write any production code until tech-architecture.md, at least one ADR per major decision (or fewer per Scale Guide), and coding-standards.md are written and the user has approved them via HITL.
</HARD-GATE>

## Checklist

1. **Read inputs**: `docs/product/features/brd.md`, `docs/product/design-system.md` (if exists)
2. **Tech stack selection** — evaluate options against NFRs, constraints, ecosystem maturity
3. **Research selected stack** — before committing to any technology:
   - Search for known gotchas, version-specific bugs, and anti-patterns for the selected stack
   - Search for community-recommended project structure and coding conventions
   - Search for any recent deprecations or upcoming breaking changes
   - Document findings in a "Research notes" subsection of the ADR for each major decision
4. **Write ADRs** — one file per major decision in `docs/architecture/adrs/` using the `adr-template.md` file in this skill's directory
5. **System context diagram** — C4 Level 1 (or skip per Scale Guide)
6. **Container diagram** — C4 Level 2 (or skip per Scale Guide)
7. **Sequence diagrams** — 2-3 most critical flows (or fewer per Scale Guide)
8. **Directory structure** — canonical directory tree in markdown
9. **Write coding constitution** — invoke `asdlc-coding-constitution` skill
10. **Write `docs/architecture/tech-architecture.md`** — using format below
11. **Self-review** — check all ADR decisions are reflected in architecture, no gaps
12. **Present to user** — section by section
13. **HITL checkpoint** — required before any code is written
14. **Update AGENTS.md** — enrichment Phase 2 (see detailed instructions below)
15. **Transition** — invoke `asdlc-implementation-planning` skill


**Decisions that typically require an ADR (subject to Scale Guide):**
- Programming language selection
- Framework selection (frontend, backend, testing)
- Database technology
- Authentication strategy
- Deployment platform
- Caching strategy (if applicable)
- Event/messaging system (if applicable)

## Architecture Document Format

`docs/architecture/tech-architecture.md`:

```markdown
# Technical Architecture

> **Status:** Draft | Approved
> **Version:** 0.1.0

## System context (C4 Level 1)
[Mermaid diagram — actors, system boundary, external integrations]

## Container diagram (C4 Level 2)
[Mermaid diagram — services, databases, frontends, message queues]

## Key sequence diagrams
### [Flow 1: e.g. User authentication]
[Mermaid sequence diagram]

### [Flow 2: e.g. Core business transaction]
[Mermaid sequence diagram]

## Directory structure
[Canonical directory tree — every top-level dir explained]

## ADR summary
| ADR | Decision | Status |
|---|---|---|
| ADR-001 | [title] | Accepted |

## Security approach
- Auth strategy: [e.g. JWT with refresh tokens]
- Secrets management: [e.g. environment variables, no hardcoding]
- Input validation: [e.g. Zod at API boundary]
- Dependency scanning: [e.g. npm audit in CI]
```

## AGENTS.md Enrichment (Phase 2)

Once technical architecture and coding standards are approved via the HITL checkpoint, you must update the `AGENTS.md` file in the project root to include project-specific context. This helps future agent sessions operate with the correct constraints.

Append a `## Project Context` section to `AGENTS.md` containing:
- **Tech Stack**: Summary of decisions from `tech-architecture.md` (Language, Framework, DB, Auth).
- **Directory Structure**: Important paths defined in `tech-architecture.md`.
- **Coding Standards**: Crucial rules extracted from `coding-standards.md`.
- **Project-specific Agent Instructions**: Any project-specific constraints.

## Gate

Read `asdlc-stage-gates` skill and evaluate:

```
[ ] Tech stack justified via ADRs for each major component
[ ] Stack research completed — gotchas, anti-patterns, and community conventions documented in ADR research notes
[ ] At least one ADR per major decision (language, framework, DB, auth) — OR fewer per Scale Guide (tiny/small projects)
[ ] System context diagram present (C4 Level 1) — OR skipped per Scale Guide (tiny projects only) with rationale
[ ] Container diagram present (C4 Level 2) — OR skipped per Scale Guide (tiny/small projects) with rationale
[ ] At least 2 sequence diagrams for the most critical flows — OR fewer per Scale Guide with rationale
[ ] Directory structure defined and documented
[ ] Coding constitution written (invoke the `asdlc-coding-constitution` skill)
[ ] Security approach documented
[ ] All artifacts written to docs/architecture/ (and ADRs to docs/architecture/adrs/)
[ ] User has reviewed and approved via HITL
[ ] AGENTS.md has been updated with Project Context (Phase 2 enrichment)
```

## HITL Checkpoint

```
HITL REQUIRED
Stage: tech-architecture
Question: Does this architecture document and set of ADRs represent the right technical approach before we begin implementation?
Context: Architecture at docs/architecture/tech-architecture.md, ADRs at docs/architecture/adrs/
Options: [A] Approved — proceed to asdlc-implementation planning
         [B] Changes needed — specify which decisions to revisit
Default if no response: Wait for explicit approval
```

## Rollback Rule

If, during implementation, a Stage 3 architectural decision proves incorrect:
1. Stop implementation
2. Write a superseding ADR documenting the conflict and the new decision
3. Trigger HITL before continuing
4. Update `docs/architecture/tech-architecture.md` to reflect the change

## Red Flags

| Thought | Reality |
|---|---|
| "We'll figure out the architecture as we go" | Emergent architecture = inconsistent patterns + expensive refactors. |
| "This ADR is obvious, I don't need to write it" | If it's obvious now, the ADR takes 3 minutes. When it's questioned in 6 months, you'll wish you wrote it. |
| "We don't need sequence diagrams for simple flows" | Simple flows have edge cases. Drawing the diagram reveals them. |
| "The directory structure can be flexible" | Flexible = no structure. Lock it down and deviate intentionally. |
| "Security can be retrofitted" | Auth and input validation must be in the architecture from day one. |
| "I know this framework — no need to research it" | Framework knowledge goes stale. Search for current version-specific gotchas before committing. |

## Scale Guide

Adapt depth to project size. Every project needs architecture; output volume scales.

| Project size | Expected output depth | Examples |
|---|---|---|
| Tiny (1-day) | 1 ADR, no diagrams required, simple directory tree | Single-endpoint API, static site |
| Small (1-week) | 2-3 ADRs, C4 Level 1 only, 1 sequence diagram | Simple CRUD web app, CLI tool |
| Medium (1-month) | Full ADR set, C4 L1+L2, 2-3 sequence diagrams | Full-stack web application |
| Large (multi-month) | Full ADR set, all C4 levels, 5+ sequence diagrams, threat model | Enterprise platform, distributed system |
