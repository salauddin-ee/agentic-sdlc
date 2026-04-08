A two-workflow agentic software development lifecycle framework for autonomous or semi-autonomous agents. Workflow 1 targets greenfield projects; Workflow 2 targets brownfield (story-level) changes to existing systems.

---

## ⚠️ The Prime Directive

**Check for a relevant skill BEFORE taking any action — including asking clarifying questions.**

If there is even a 1% chance a skill applies, invoke it. Skills override default behavior. User instructions override skills.

Instruction priority:
1. **User's explicit instructions** — highest
2. **Agentic SDLC skills** — override default agent behavior
3. **Default agent behavior** — lowest priority

---

## Core principles

- Every stage produces explicit, file-backed artifacts — no implicit state
- Every stage boundary has an exit gate with defined criteria
- Human-in-the-loop (HITL) checkpoints are mandatory before irreversible actions
- All retrospective output feeds back into the skills library for future runs
- Parallelism is opt-in and requires an explicit dependency graph before execution
- The agent must not proceed past a gate on partial output

---

## Agent memory protocol

The agent carries context across stages via a set of versioned markdown files written to a distributed `docs/` directory structure at the project root. Each stage declares which files it reads (inputs) and which it writes or updates (outputs). No stage should rely on conversation memory alone.

```
docs/
  architecture/domain-model.md       ← inception
  product/features/brd.md            ← inception
  product/design-system.md           ← design-system
  product/accessibility.md           ← design-system
  architecture/tech-architecture.md  ← tech-architecture
  architecture/adrs/                 ← tech-architecture
  architecture/coding-standards.md   ← tech-architecture / coding-constitution
  sdlc/epics/implementation-plan.md  ← implementation-planning
  architecture/data-domain.md        ← implementation-planning / implementation
  sdlc/epics/task-graph.md           ← story-breakdown
  sdlc/stories/STORY-*.md            ← story-breakdown
  sdlc/test-plans/test-plan.md       ← testing
  sdlc/retrospectives/retrospective.md ← critical-review / retrospective
  architecture/existing-system.md    ← context-harvest (brownfield)
```

---

## Shared infrastructure (both workflows)

### Skills library

Each skill is a discrete, reusable prompt module with:

| Field | Description |
|---|---|
| `trigger` | Conditions under which this skill is invoked |
| `inputs` | Required context files and parameters |
| `outputs` | Artifacts produced |
| `quality criteria` | Checklist the agent self-evaluates against before exiting |
| `language/platform` | e.g. Java Spring Boot, Python FastAPI, React |

Skills are stored in `/skills` and versioned. The retrospective stage may propose new skills or edits to existing ones.

Example skill categories: REST controller generation, database migration, test generation (unit / integration / e2e), OpenAPI spec generation, ADR authoring, accessibility review, security checklist.

### Stage gates

Every stage ends with a self-evaluated gate. If the gate fails, the agent loops within the stage — it does not proceed.

Gate format:

```
GATE [stage name]
[ ] criterion 1
[ ] criterion 2
[ ] criterion 3
RESULT: PASS | FAIL — reason if fail
```

### HITL checkpoints

Mandatory human approval is required at:

Mandatory human approval is required at these points (HARD-GATES):

1. **Inception End**: After BRD is written and before design/architecture (Stage 1 exit).
2. **Architecture End**: After tech stack, diagrams, and ADRs are approved (Stage 3 exit).
3. **Task Graph Approval**: After story breakdown but before any code is written (Stage 5 exit).
4. **Architectural Deviation**: If implementation reveals a Stage 3 decision was wrong (Stage 6 rollback).
5. **Contract Change**: Any change to `interface-contracts.md` mid-implementation.
6. **Destructive Operations**: Before any production DB migration or data deletion.
7. **Ambiguity**: When the agent is blocked and cannot resolve a requirement autonomously.

HITL prompt format:

```
HITL REQUIRED
Stage: [name]
Question: [specific question or decision needed]
Context: [brief summary of relevant state]
Options: [A] ... [B] ... [C] ...
Default if no response in [timeout]: [option]
```

### Coding constitution

Written at Stage 3 (greenfield) or inherited at Stage 0 (brownfield). Covers:

- Language-specific standards (see per-language skill)
- Test pyramid targets (unit / integration / e2e ratios)
- Security non-negotiables (auth on every endpoint, input validation, secrets management, dependency scanning)
- Clean code principles: SOLID, DRY, YAGNI, KISS
- Naming conventions
- Error handling patterns
- Logging standards
- Forbidden patterns (magic numbers, God classes, raw SQL with user input, etc.)
- TDD workflow: red → green → refactor
- BDD: Given / When / Then for acceptance tests

---

## Workflow 1 — Greenfield projects

### Stage 1 — Brainstorm / inception

**Purpose:** Establish shared understanding before anything is built.

**Inputs:** Initial prompt or brief from user.

**Process:**

1. Identify the problem domain. Write `domain.md` with relevant domain knowledge — regulatory context, industry conventions, key entities, glossary.
2. Run the skills constitution: ask clarifying questions across these axes:
   - Business objective and measurable success criteria
   - User personas and their jobs-to-be-done
   - Constraints (timeline, budget, compliance, existing systems)
   - Out-of-scope (explicit)
   - Non-functional requirements (latency, availability, scale, geography)
3. Produce `brd.md` — Business Requirements Document.

**BRD structure:**

```markdown
# Business requirements document

## Objective
[One paragraph. What problem does this solve and for whom?]

## Success metrics
[Measurable. e.g. "P95 API latency < 200ms", "checkout conversion > X%"]

## User personas
[Name, role, primary goal, pain point]

## Functional requirements
[FR-001] ...
[FR-002] ...

## Non-functional requirements
[NFR-001] Availability: 99.9% uptime
[NFR-002] Security: OWASP Top 10 compliance
...

## Constraints
[Budget, timeline, technology mandates, compliance requirements]

## Out of scope
[Explicit list]

## Open questions
[Unresolved items requiring HITL before proceeding]
```

**Gate:**

```
[ ] Business objective is stated and measurable
[ ] At least 3 user personas defined
[ ] Success metrics are quantified
[ ] NFRs captured
[ ] Out-of-scope is explicit
[ ] No open questions remain (or HITL scheduled)
```

**HITL:** Required before proceeding to Stage 2.

---

### Stage 2 — Design system

**Purpose:** Establish visual and interaction language before technical decisions lock in. (Stages 2 and 3 may run in either order depending on whether UI is primary.)

**Inputs:** `brd.md`, `domain.md`

**Outputs:** `design-system.md`, `accessibility.md`, component inventory

**Process:**

1. Reference [component.gallery](https://component.gallery) for component patterns relevant to the domain.
2. Define design tokens: color palette, typography scale, spacing scale, border radii, shadow levels, motion.
3. Produce component inventory: list every UI component required, with state variants (default, hover, focus, disabled, error, loading).
4. Produce `accessibility.md`:
   - WCAG 2.2 AA as minimum target
   - Keyboard navigation requirements per component
   - Screen reader semantics (ARIA roles, labels, live regions)
   - Color contrast requirements (4.5:1 body, 3:1 large text)
   - Focus indicator requirements
5. Produce mocks or design tokens in agreed format (Figma variables JSON, CSS custom properties, or design-system.md tokens table).

**Design questions to resolve:**

- Is there an existing brand / design system to inherit from?
- What devices and breakpoints must be supported?
- Are there data density requirements (dashboards vs. consumer UI)?
- Internationalization and RTL requirements?
- Dark mode requirement?

**Gate:**

```
[ ] Design tokens defined (color, type, spacing)
[ ] Component inventory complete against FR list
[ ] Accessibility requirements documented
[ ] Responsive breakpoints defined
[ ] At least one layout mock produced for primary user flow
```

---

### Stage 3 — Tech brainstorm

**Purpose:** Produce a defensible, documented technical architecture before any code.

**Inputs:** `brd.md`, `design-system.md`

**Outputs:** `tech-architecture.md`, `adr/`, `coding-constitution.md`, directory structure

**Process:**

1. **Tech stack selection** — evaluate options against NFRs, team constraints, and ecosystem maturity. Document each decision as an ADR.
2. **Overall architecture** — produce Mermaid diagrams for:
   - System context (C4 level 1): what the system is, who uses it, what it integrates with
   - Container diagram (C4 level 2): major deployable units
   - Key component interactions: sequence diagrams for the 2-3 most critical flows
3. **Directory structure** — produce a canonical directory tree in markdown.
4. **ADR format** (one file per decision in `adr/`):

```markdown
# ADR-NNN: [Decision title]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Superseded

## Context
[Why does this decision need to be made?]

## Decision
[What was decided?]

## Rationale
[Why this option over alternatives?]

## Alternatives considered
[What else was evaluated and why rejected?]

## Consequences
[Trade-offs, risks, follow-up actions]
```

5. **Coding constitution** — write `coding-constitution.md` covering all items in the shared infrastructure section above, plus language-specific standards from the relevant skill.

**Gate:**

```
[ ] Tech stack justified via ADRs for each major component
[ ] System context diagram present
[ ] Container diagram present
[ ] At least 2 sequence diagrams for critical flows
[ ] Directory structure defined
[ ] Coding constitution written
[ ] Security approach documented (auth strategy, secrets management, input validation)
```

**HITL:** Required before proceeding to Stage 4.

---

### Stage 4 — Implementation plan

**Purpose:** Produce a machine-readable execution contract the agent follows in Stages 5–6.

**Inputs:** `brd.md`, `tech-architecture.md`, `coding-constitution.md`

**Output:** `implementation-plan.md`

**Structure:**

```markdown
# Implementation plan

## Milestones
| ID  | Name | Description | Exit criteria | Depends on |
|-----|------|-------------|--------------|------------|
| M1  | ...  | ...         | ...          | —          |
| M2  | ...  | ...         | ...          | M1         |

## Interface contracts (pre-implementation)
Defined before any parallel work begins. Every module boundary must have:
- API contract (endpoint, method, request schema, response schema, error codes)
- Event schema (if event-driven)
- Type definitions / interfaces

## Risk log
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| ...  | H/M/L     | H/M/L  | ...        |

## Assumptions
[Explicit list. If any assumption is wrong, flag for HITL before proceeding.]

## Definition of done (project level)
[ ] All FRs implemented and verified
[ ] All NFRs verified with evidence
[ ] Test pyramid targets met
[ ] Security checklist passed
[ ] Documentation complete
[ ] No P0/P1 open bugs
```

**Gate:**

```
[ ] All milestones have explicit exit criteria
[ ] All inter-module interface contracts defined before Stage 5
[ ] Risk log populated
[ ] Definition of done agreed
```

---

### Stage 5 — Story / task breakdown

**Purpose:** Decompose the implementation plan into atomic, executable tasks with a dependency graph.

**Inputs:** `implementation-plan.md`, `interface-contracts.md`

**Output:** `task-graph.md`

**Process:**

1. Break each milestone into stories. Each story:
   - Has a clear acceptance criterion (Given / When / Then)
   - Is independently testable
   - Is completable in one agent session (rough guide: < 400 lines of net new code)

2. Identify parallel tracks. Tasks with no shared file or interface dependency can run in parallel. Produce an explicit DAG:

```markdown
## Task dependency graph

Task A → Task B → Task D
Task A → Task C → Task D
              ↑
         (merge point)
```

3. For each parallel track, define:
   - Which files it owns exclusively
   - The merge strategy (feature branch, file-level split, or sequential with handoff file)
   - The conflict resolution rule if two tracks touch the same file

4. Flag any task that requires a HITL checkpoint before starting.

**Story format:**

```markdown
### STORY-NNN: [Title]

**Milestone:** M1
**Track:** A (parallel with B, C)
**Depends on:** STORY-NNN-1

**Acceptance criteria:**
- Given [context]
- When [action]
- Then [outcome]

**Tasks:**
- [ ] Write failing test(s)
- [ ] Implement to make tests pass
- [ ] Refactor
- [ ] Update interface contract if changed

**Files owned:** src/module/foo.ts, src/module/foo.test.ts
**Merge strategy:** Feature branch, squash merge to main
```

**HITL:** Required. Human reviews and approves task graph before implementation begins.

**Gate:**

```
[ ] Every story has Given/When/Then acceptance criteria
[ ] DAG is acyclic (no circular dependencies)
[ ] All parallel tracks have exclusive file ownership or explicit merge strategy
[ ] All interface contracts locked before parallel work begins
[ ] HITL checkpoint tasks marked
```

---

### Stage 6 — Implementation

**Purpose:** Write production-quality code following TDD, the coding constitution, and the task graph.

**Inputs:** `task-graph.md`, `interface-contracts.md`, `coding-constitution.md`, relevant skills

**Per-task loop:**

```
1. Load task from task-graph.md
2. Read relevant skill (language/platform-specific)
3. Write failing test(s) — unit first, then integration if needed
4. Run tests — confirm RED
5. Write minimal implementation to pass tests
6. Run tests — confirm GREEN
7. Refactor — apply coding constitution, clean code principles
8. Run full test suite — confirm no regression
9. Mark task complete in task-graph.md
10. Update interface-contracts.md if any contract changed (triggers HITL)
```

**Test pyramid targets (defaults — adjust per project NFRs):**

| Layer | Target | Characteristics |
|---|---|---|
| Unit | 70% of tests | Fast, isolated, no I/O |
| Integration | 20% of tests | Real DB/service, no UI |
| E2E / acceptance | 10% of tests | Full stack, Given/When/Then |

Reference: [Martin Fowler — Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)

**Security non-negotiables (checked per story):**

- [ ] Every authenticated endpoint verifies token/session
- [ ] Every user input validated and sanitized
- [ ] No secrets in source code or logs
- [ ] External calls have timeouts and error handling
- [ ] SQL / NoSQL queries use parameterization, never string concatenation
- [ ] Dependencies checked against known vulnerability database

**Rollback rule:** If implementation reveals that a Stage 3 architectural decision is wrong, the agent must halt, document the conflict in `adr/` as a superseding ADR, and trigger HITL before continuing.

---

### Stage 7 — Critical thinking review

**Purpose:** Evaluate completed implementation with fresh eyes against the original requirements. This stage is intentionally adversarial — the agent's job is to find problems, not confirm success.

**Inputs:** `brd.md`, `task-graph.md`, `interface-contracts.md`, full codebase

**Checklist (run against every story):**

**Requirements coverage:**
- [ ] Every FR has at least one passing test that validates it
- [ ] Every acceptance criterion in the story is verifiable in the code
- [ ] No FR is partially implemented

**Code quality:**
- [ ] No obvious code smells (God class, deep nesting > 3, function > 20 lines without justification)
- [ ] Error paths handled (not just happy path)
- [ ] No TODO comments left in production code
- [ ] Logging is present at appropriate levels (request in/out, errors, key state changes)

**Security:**
- [ ] Auth check on every protected endpoint — verify by reading the code, not by trusting the story
- [ ] Input validation present, not just assumed
- [ ] No sensitive data in logs or error responses

**Integration:**
- [ ] All interface contracts still match implementation
- [ ] No breaking changes introduced to existing consumers

**Output:** `critical-review.md` — list of findings categorised as P0 (block release), P1 (fix before merge), P2 (log as tech debt).

**Loop rule:** P0 and P1 findings must be fixed and re-reviewed before Stage 8. P2s are logged in `retrospective.md`.

---

### Stage 8 — Testing

**Purpose:** Execute the test plan and verify the application works end-to-end, including paths the agent did not implement directly.

**Inputs:** `test-plan.md`, codebase

**Test plan structure:**

```markdown
# Test plan

## Scope
[What is in scope for this test cycle]

## Environment
[Required infra, test data, mocks/stubs vs. real services]

## Test cases
| ID | Story | Type | Given | When | Then | Pass/Fail |
|----|-------|------|-------|------|------|-----------|

## Regression scope
[Which existing tests must remain green]

## Performance targets
[From NFRs — latency, throughput, load test targets]

## HITL test cases
[Scenarios the agent cannot verify alone — list the question and expected human response]
```

**Process:**

1. Run full automated test suite. All tests must be green before proceeding.
2. Run any HITL test cases — ask the human for input on scenarios requiring judgment.
3. Run load/performance test if NFRs specify targets.
4. Document results in `test-plan.md`.

**Gate:**

```
[ ] All automated tests passing (0 failures, 0 errors)
[ ] Test pyramid targets met or deviation documented with reason
[ ] All HITL test cases resolved
[ ] Performance targets met or deviation accepted via HITL
[ ] No P0 or P1 open findings from Stage 7
```

---

### Stage 9 — Code review

**Purpose:** Final structured review before handoff or merge.

**Checklist:**

**Standards compliance:**
- [ ] Coding constitution followed throughout
- [ ] All ADR decisions reflected in code (no silent deviations)
- [ ] No commented-out code
- [ ] All public APIs documented

**Test quality:**
- [ ] Tests test behavior, not implementation
- [ ] No tests that always pass regardless of code
- [ ] Test names describe the scenario, not the method

**Security:**
- [ ] Dependency audit run (`npm audit`, `pip-audit`, `gradle dependencyCheckAnalyze`, etc.)
- [ ] No new CVEs introduced at severity HIGH or above without documented acceptance

**Operability:**
- [ ] Structured logging in place
- [ ] Health check endpoint present (if applicable)
- [ ] Environment configuration via env vars, not hardcoded

**Documentation:**
- [ ] README updated
- [ ] API documentation updated
- [ ] Architecture diagrams updated if topology changed

---

### Stage 10 — Retrospective

**Purpose:** Close the loop. Account for what happened, extract knowledge into the skills library, and make the next run smarter.

**Output:** `retrospective.md`

**Structure:**

```markdown
# Retrospective — [Project name] — [Date]

## Execution summary
- Total token usage: [input / output / total]
- Total elapsed time: [wall time across all stages]
- Stages with HITL interventions: [list]
- Rollbacks triggered: [list with reason]

## Requirements fidelity
| FR ID | Implemented | Verified | Notes |
|-------|------------|---------|-------|

## What the plan got right
[Assumptions that held, architectural decisions that worked well]

## What the plan got wrong
[Assumptions that failed, decisions that had to be revised mid-execution]

## Surprises
[Anything the agent did not anticipate that affected the run]

## Tech debt logged
[P2 findings from Stage 7 not fixed this cycle]

## Skills library updates
[New skills proposed, existing skills to modify, patterns worth capturing]

## Process improvements
[Changes to this framework that would make the next run better]
```

---

## Workflow 2 — Brownfield (story-level)

### Stage 0 — Context harvest

**Purpose:** Build accurate understanding of the existing system before proposing any change.

**Process:**

1. Ingest available documentation: README, existing ADRs, API specs, architecture diagrams.
2. Fingerprint the codebase:
   - Detect tech stack and versions
   - Identify test coverage baseline (run existing test suite, record pass rate and coverage %)
   - Identify existing patterns (directory structure, naming conventions, error handling style)
   - Identify known tech debt (TODO comments, suppressed lint warnings, flagged issues)
3. Write `docs/architecture/existing-system.md`:
   - Tech stack
   - Test coverage baseline
   - Patterns in use
   - Known constraints and fragile areas
   - Integration points (external services, downstream consumers)

**Gate:**

```
[ ] Tech stack and versions documented
[ ] Test coverage baseline recorded
[ ] Existing patterns documented
[ ] Integration points identified
[ ] Fragile / high-risk areas flagged
```

---

### Stage 1 — Design (lite)

**Purpose:** Resolve design for this story only. Inherit from the existing design system where one exists.

**Inputs:** `docs/architecture/existing-system.md`, story brief, existing design system (if available)

**Outputs:** `design-system.md` (delta only if inheriting), `accessibility.md`

**Design questions to resolve:**

- Does this story introduce any new UI components? If so, do they conform to the existing design system?
- Are there accessibility implications (new form fields, modals, dynamic content)?
- Does this story change any existing visual contract visible to end users?

Reference [component.gallery](https://component.gallery) for component patterns.

---

### Stage 2 — Brainstorm (lite)

**Purpose:** Understand the business impact and user impact of this story in isolation.

**Per story / epic:**

- What is the user job-to-be-done this story serves?
- What is the measurable business outcome (conversion, retention, error rate reduction, etc.)?
- What are the acceptance criteria in Given / When / Then format?
- What is the definition of done for this story specifically?
- Are there dependencies on other in-flight stories?

---

### Stage 3 — Tech plan (lite)

**Purpose:** Plan the technical approach for this story without re-architecting the system.

**Principles:**

- **YAGNI** — You Aren't Gonna Need It. Implement exactly what the story requires.
- **KISS** — Keep It Simple. Prefer boring, obvious solutions over clever ones.
- **DRY** — Don't Repeat Yourself. Check whether existing code already handles this before writing new code.
- Prefer extending existing patterns over introducing new ones.

**Outputs:**

- `tech-plan-[story-id].md` — approach, files to be changed, new files required, interface changes
- Updated `interface-contracts.md` if any contract changes (triggers HITL)

**Regression risk assessment:**

- [ ] Which existing tests could be broken by this change?
- [ ] Which integration points does this change touch?
- [ ] Is a feature flag needed to safely deploy this?

---

### Stage 4 — Implementation plan

Same structure as Workflow 1 Stage 4, scoped to this story / epic.

Additionally:

- Explicitly state the test coverage baseline from Stage 0.
- Commit to not decreasing coverage.
- Identify which existing tests must remain green as a regression gate.

---

### Stage 5 — Story breakdown

Same structure as Workflow 1 Stage 5, scoped to this story.

For brownfield, additionally:
- Mark any task that modifies a file owned by another active story (conflict risk).
- Default merge strategy: feature branch per story, squash merge.

**HITL:** Required before implementation begins.

---

### Stage 6 — Implementation

Same TDD loop as Workflow 1 Stage 6, plus:

- After every task, run the full existing test suite (not just new tests).
- If any existing test breaks, treat as a P0 — stop and resolve before continuing.
- Do not modify existing tests to make them pass unless the behavior change is explicitly in scope and approved via HITL.

---

### Stage 7 — Critical thinking review

Same as Workflow 1 Stage 7, plus:

**Brownfield-specific checks:**

- [ ] No existing behavior changed outside the story's scope
- [ ] No new dependency introduced without ADR justification
- [ ] No new pattern introduced that conflicts with existing codebase conventions
- [ ] Feature flag present if story is behind a toggle
- [ ] Migration (if any) is reversible

---

### Stage 8 — Testing

Same as Workflow 1 Stage 8, plus:

- Regression test run is mandatory (run the full existing suite).
- Test coverage must not decrease from the Stage 0 baseline.
- If a bug is found in existing code unrelated to this story: log it, do not fix it in this cycle (scope creep risk), propose it as a separate story.

---

### Stage 9 — Code review

Same as Workflow 1 Stage 9.

Additional brownfield checks:

- [ ] No new tech debt introduced (or explicitly accepted via HITL and logged in retrospective)
- [ ] Clean code: no increase in cyclomatic complexity in modified files without justification
- [ ] Backwards compatibility maintained for any shared interface

---

### Stage 10 — Retrospective (story)

**Output:** Entry appended to `retrospective.md`

**Structure per story:**

```markdown
## Story retrospective — [STORY-ID]: [Title] — [Date]

### Execution
- Token usage: [input / output / total]
- Elapsed time: [wall time]
- HITL interventions: [count and reason]
- Rollbacks: [count and reason]

### Delivery fidelity
- Acceptance criteria met: [Y/N per criterion]
- Test coverage: before [X%] → after [Y%]
- Regression tests: [all pass / N failures]

### What changed from plan
[Any deviation from the Stage 3 tech plan and why]

### Bugs found
- In-scope bugs fixed: [list]
- Out-of-scope bugs logged as separate stories: [list]

### Tech debt
- Introduced (with justification): [list]
- Resolved incidentally: [list]

### Skills library updates
[Any pattern worth capturing for future stories]

### Process improvements
[What would make the next story run faster or safer]
```

---

## Language-specific skill references

Each language skill covers: project structure conventions, dependency management, linting and formatting setup, test framework and runner, common patterns (REST, messaging, persistence), security checklist items, and known pitfalls.

| Language / platform | Skill trigger |
|---|---|
| Java (Spring Boot) | Any story targeting Java services |
| Python | Any story targeting Python services |
| TypeScript / Node.js | Any story targeting backend TS |
| React / Next.js | Any story with frontend UI components |
| SQL / migrations | Any story touching database schema |
| Infrastructure / IaC | Any story touching deployment config |

Skills are loaded at the start of Stage 6 for each task, not loaded once globally. This keeps each task's context precise.

---

## References

- Test pyramid: https://martinfowler.com/articles/practical-test-pyramid.html
- Component patterns: https://component.gallery
- C4 architecture diagrams: https://c4model.com
- OWASP Top 10: https://owasp.org/www-project-top-ten
- WCAG 2.2: https://www.w3.org/TR/WCAG22
- ADR format: https://adr.github.io
